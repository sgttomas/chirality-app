//! DEL-02-04's own immutable supply observations and exact App instruction bytes.
//! Reads are quoted file evidence; they never create RoleBindings or CCE owners.
use crate::{record_lines, records_store, role_supply, storage};
use serde_json::{json, Value};
use std::{
    ffi::CString,
    fs::File,
    io::{BufRead, BufReader, Read, Write},
    os::fd::{AsRawFd, FromRawFd},
    os::unix::fs::MetadataExt,
    path::{Component, Path, PathBuf},
    sync::OnceLock,
};

pub const FORMAT: &str = "chirality.role.supply.observation";
#[path = "role_record_source.rs"]
mod receiving;
#[cfg(test)]
pub(crate) use receiving::FAIL_CONTEXT_AFTER_FILE_SYNC;
pub(crate) use receiving::{PublishedRoleSupply, PreparedRoleRunSupply, read_r3, read_r3_with_relations, read_project_sources, BoundedRoleReading};

pub const OLD_SCHEMA: &str = include_str!("../resources/workflow_role/role-supply-observation-0.1.schema.json");
pub const PREVIOUS_SCHEMA: &str = include_str!("../resources/workflow_role/role-supply-observation-0.2.schema.json");
pub const SCHEMA: &str =
    include_str!("../resources/workflow_role/role-supply-observation.schema.json");
const FOLDER: &str = "role-supply";
const LOG: &str = "observations.jsonl";
pub(crate) const RELATIVE_LOG: &str = "role-supply/observations.jsonl";
const METADATA_BUDGET: &str = "role metadata source budget exceeded";
#[cfg(test)]
thread_local! {pub(crate) static METADATA_BEFORE_READ:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const {std::cell::RefCell::new(None)};}
const STANDING: &str = "Quoted App supply observations; mutable file provenance is unverified. No current role, CCE authority, provider adoption or human act is established.";
#[cfg(test)]
thread_local! {
    pub(crate) static BEFORE_APPEND: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) };
    pub(crate) static FAIL_AFTER_FILE_SYNC: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
}

fn open_at(parent: &File, name: &str, flags: i32) -> Result<File, String> {
    let name = CString::new(name).map_err(|_| "NUL in role observation path")?;
    let fd = unsafe {
        libc::openat(
            parent.as_raw_fd(),
            name.as_ptr(),
            flags | libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK,
            0o600,
        )
    };
    if fd < 0 {
        Err(std::io::Error::last_os_error().to_string())
    } else {
        Ok(unsafe { File::from_raw_fd(fd) })
    }
}
fn directory(path: &Path) -> Result<File, String> {
    if !path.is_absolute() {
        return Err("explicit absolute App project required".into());
    }
    let mut at = File::open("/").map_err(|e| e.to_string())?;
    for part in path.components() {
        match part {
            Component::RootDir => {}
            Component::Normal(name) => {
                at = open_at(
                    &at,
                    name.to_str().ok_or("non-UTF8 directory component")?,
                    libc::O_RDONLY | libc::O_DIRECTORY,
                )?
            }
            _ => return Err("non-normal role observation directory".into()),
        }
    }
    Ok(at)
}
fn child(parent: &File, name: &str, create: bool) -> Result<Option<File>, String> {
    if create {
        let name = CString::new(name).map_err(|_| "NUL directory")?;
        if unsafe { libc::mkdirat(parent.as_raw_fd(), name.as_ptr(), 0o700) } < 0
            && std::io::Error::last_os_error().kind() != std::io::ErrorKind::AlreadyExists
        {
            return Err(std::io::Error::last_os_error().to_string());
        }
    }
    match open_at(parent, name, libc::O_RDONLY | libc::O_DIRECTORY) {
        Ok(file) => {
            if create {
                file.sync_all().map_err(|e| e.to_string())?;
                parent.sync_all().map_err(|e| e.to_string())?;
            }
            Ok(Some(file))
        }
        Err(e) if !create => {
            let n = CString::new(name).unwrap();
            let mut s = std::mem::MaybeUninit::<libc::stat>::uninit();
            if unsafe {
                libc::fstatat(
                    parent.as_raw_fd(),
                    n.as_ptr(),
                    s.as_mut_ptr(),
                    libc::AT_SYMLINK_NOFOLLOW,
                )
            } < 0
                && std::io::Error::last_os_error().kind() == std::io::ErrorKind::NotFound
            {
                Ok(None)
            } else {
                Err(e)
            }
        }
        Err(e) => Err(e),
    }
}
fn plain(file: &File) -> Result<(), String> {
    let m = file.metadata().map_err(|e| e.to_string())?;
    if !m.is_file() || m.nlink() != 1 {
        Err("role observation leaf is not a singly linked regular file".into())
    } else {
        Ok(())
    }
}
fn identity(file: &File) -> Result<(u64, u64), String> {
    let m = file.metadata().map_err(|e| e.to_string())?;
    Ok((m.dev(), m.ino()))
}
fn verify_directory(path: &Path, file: &File) -> Result<(), String> {
    if identity(&directory(path)?)? != identity(file)? {
        Err("role observation directory was replaced during IO".into())
    } else {
        Ok(())
    }
}
fn verify_directory_child(parent:&File,name:&str,held:&File)->Result<(),String>{
    let named=open_at(parent,name,libc::O_RDONLY|libc::O_DIRECTORY)?;
    if identity(&named)?!=identity(held)?{Err("role source content directory replaced during read".into())}else{Ok(())}
}
fn verify_leaf(parent: &File, name: &str, file: &File) -> Result<(), String> {
    let current = open_at(parent, name, libc::O_RDONLY)?;
    plain(&current)?;
    if identity(&current)? != identity(file)? {
        Err("role observation leaf was replaced during IO".into())
    } else {
        Ok(())
    }
}
#[derive(Clone, Copy, PartialEq, Eq)]
struct LogBasis {
    device: u64,
    inode: u64,
    length: u64,
    mtime: i64,
    mtime_ns: i64,
    ctime: i64,
    ctime_ns: i64,
}
impl LogBasis {
    fn of(m: &std::fs::Metadata) -> Self {
        Self {
            device: m.dev(),
            inode: m.ino(),
            length: m.len(),
            mtime: m.mtime(),
            mtime_ns: m.mtime_nsec(),
            ctime: m.ctime(),
            ctime_ns: m.ctime_nsec(),
        }
    }
}
#[derive(Debug,Clone)]
struct PublicationBasis {path:PathBuf,folder:(u64,u64),log:(u64,u64)}
fn validate(value: &Value) -> Result<(), String> {
    static VALIDATORS: OnceLock<Result<std::collections::BTreeMap<&'static str,jsonschema::Validator>, String>> = OnceLock::new();
    VALIDATORS.get_or_init(|| [ ("0.1",OLD_SCHEMA),("0.2",PREVIOUS_SCHEMA),("0.3",SCHEMA) ].into_iter().map(|(version,schema)| {
        jsonschema::options().offline().build(&serde_json::from_str::<Value>(schema).map_err(|e|e.to_string())?).map(|v|(version,v)).map_err(|e|e.to_string())
    }).collect()).as_ref().map_err(Clone::clone)?.get(value["formatVersion"].as_str().unwrap_or(""))
        .ok_or("unsupported role observation format version")?.validate(value).map_err(|e|e.to_string())
}

fn payload_key(identity: &Value) -> Result<&str, String> {
    let s = identity["value"]
        .as_str()
        .ok_or("App payload identity absent")?;
    if identity["method"] != role_supply::CONTENT_METHOD
        || s.len() != 64
        || !s
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err("unsupported App payload identity".into());
    }
    Ok(s)
}
/// Opened once from the explicit Root App project; never inferred from native cwd.
#[derive(Debug)]
pub struct RoleLog {
    project: PathBuf,
    project_directory: File,
    project_identity: (u64, u64),
    writer: std::sync::Mutex<()>,
}
impl RoleLog {
    pub fn open(project: &Path) -> Result<Self, String> {
        let project_directory = directory(project)?;
        let project_identity = identity(&project_directory)?;
        Ok(Self {
            project: project.to_owned(),
            project_directory,
            project_identity,
            writer: std::sync::Mutex::new(()),
        })
    }
    fn check_project(&self) -> Result<(), String> {
        let current = directory(&self.project)?;
        if identity(&current)? != self.project_identity
            || identity(&self.project_directory)? != self.project_identity
        {
            Err(
                "original App project directory replaced; role observation scope unavailable"
                    .into(),
            )
        } else {
            Ok(())
        }
    }
    fn location(
        &self,
        write: bool,
    ) -> Result<
        Option<(
            PathBuf,
            File,
            Option<storage::Ownership>,
            Option<storage::Ownership>,
        )>,
        String,
    > {
        self.check_project()?;
        let dir = if write {
            records_store::write_dir(&self.project)?
        } else {
            let home = records_store::home(&self.project)?;
            if let Some(refusal) = home.attachment.refusal {
                return Err(refusal);
            }
            let Some(dir) = home.attachment.dir else {
                return Ok(None);
            };
            // Auxiliary observations cannot hide ordinary in-place history.
            if !home.store_mode && !records_store::legacy_census(&self.project)?.is_empty() {
                return Err("project records need explicit import before role observation history can be read".into());
            }
            dir
        };
        let admission = if write {
            crate::records_retention::write_path(&dir)?
        } else {
            crate::records_retention::read_path(&dir)?
        };
        let writer = if write {
            Some(records_store::writer_lock(&dir, true)?)
        } else {
            None
        };
        let parent = directory(&dir)?;
        let Some(folder) = child(&parent, FOLDER, write)? else {
            return Ok(None);
        };
        self.check_project()?;
        verify_directory(&dir.join(FOLDER), &folder)?;
        Ok(Some((dir.join(FOLDER), folder, admission, writer)))
    }
    fn read_lines(
        folder: &File,
        path: &Path,
    ) -> Result<(Vec<Value>, record_lines::Chain, Option<LogBasis>), String> {
        Self::read_lines_bounded(folder, path, None)
    }
    // The capability's read-side hook shares the full reader's chain/schema
    // checks. The descriptor's Take bound also caps newline-free/racing input;
    // overflow is never parsed as a successful truncated source.
    fn read_lines_bounded(
        folder: &File,
        path: &Path,
        limit: Option<usize>,
    ) -> Result<(Vec<Value>, record_lines::Chain, Option<LogBasis>), String> {
        let file = match open_at(folder, LOG, libc::O_RDONLY) {
            Ok(f) => f,
            Err(e) => {
                let n = CString::new(LOG).unwrap();
                let mut s = std::mem::MaybeUninit::<libc::stat>::uninit();
                if unsafe {
                    libc::fstatat(
                        folder.as_raw_fd(),
                        n.as_ptr(),
                        s.as_mut_ptr(),
                        libc::AT_SYMLINK_NOFOLLOW,
                    )
                } < 0
                    && std::io::Error::last_os_error().kind() == std::io::ErrorKind::NotFound
                {
                    return Ok((vec![], record_lines::Chain::default(), None));
                }
                return Err(e);
            }
        };
        plain(&file)?;
        let before = file.metadata().map_err(|e| e.to_string())?;
        if limit.is_some_and(|limit| before.len() > limit as u64) {
            return Err(METADATA_BUDGET.into());
        }
        #[cfg(test)]
        if limit.is_some() {
            if let Some(hook) = METADATA_BEFORE_READ.with(|h| h.borrow_mut().take()) { hook(); }
        }
        let mut reader = BufReader::new((&file).take(limit.map_or(u64::MAX, |n| n as u64 + 1)));
        let mut consumed = 0usize;
        let mut rows = vec![];
        let mut identities = std::collections::BTreeSet::new();
        let mut chain = record_lines::Chain::default();
        let mut raw = vec![];
        loop {
            raw.clear();
            if reader
                .read_until(b'\n', &mut raw)
                .map_err(|e| e.to_string())?
                == 0
            {
                break;
            }
            consumed = consumed.saturating_add(raw.len());
            if limit.is_some_and(|limit| consumed > limit) {
                return Err(METADATA_BUDGET.into());
            }
            if raw.pop() != Some(b'\n') {
                return Err(
                    "role observation log has a torn final line; nothing inferred or appended"
                        .into(),
                );
            }
            let row: Value = serde_json::from_slice(&raw)
                .map_err(|e| format!("unreadable role observation line: {e}"))?;
            if row["format"] == "chirality.role.supply" && row["formatVersion"] == "0.2" {
                // Retain older exact evidence without promoting its numeric generation.
                static LEGACY: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
                LEGACY
                    .get_or_init(|| {
                        jsonschema::options()
                            .offline()
                            .build(
                                &serde_json::from_str::<Value>(include_str!(
                                    "../resources/workflow_role/role-supply-record.schema.json"
                                ))
                                .map_err(|e| e.to_string())?,
                            )
                            .map_err(|e| e.to_string())
                    })
                    .as_ref()
                    .map_err(Clone::clone)?
                    .validate(&row)
                    .map_err(|e| e.to_string())?;
            } else {
                validate(&row)?;
                if row["request"]["generation"].is_object()
                    && row["request"]["generation"]["home"] != row["request"]["home"]
                {
                    return Err("role observation full generation/home disagree".into());
                }
                if !identities.insert(
                    row["observationId"]
                        .as_str()
                        .ok_or("observation identity absent")?
                        .to_owned(),
                ) {
                    return Err("duplicate role observation identity in log".into());
                }
                if row["seq"].as_u64() != Some(chain.lines as u64 + 1) {
                    return Err("role observation sequence differs from source order".into());
                }
            }
            chain.step(chain.lines + 1, &raw, row.get("prevLine"))?;
            rows.push(row);
        }
        let after = file.metadata().map_err(|e| e.to_string())?;
        if (
            before.len(),
            before.mtime(),
            before.mtime_nsec(),
            before.ctime(),
            before.ctime_nsec(),
        ) != (
            after.len(),
            after.mtime(),
            after.mtime_nsec(),
            after.ctime(),
            after.ctime_nsec(),
        ) {
            return Err("role observation log changed during read".into());
        }
        verify_leaf(folder, LOG, &file)?;
        if let Some(limit) =
            record_lines::links_removed(&path.join(LOG), "role supply observations", &chain)
        {
            return Err(limit);
        }
        Ok((rows, chain, Some(LogBasis::of(&after))))
    }
    fn publish_bytes(content: &File, bytes: &[u8]) -> Result<(Value, File), String> {
        let id = role_supply::content(bytes);
        let leaf = format!("{}.utf8", payload_key(&id)?);
        let file = match open_at(
            content,
            &leaf,
            libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL,
        ) {
            Ok(mut file) => {
                plain(&file)?;
                file.write_all(bytes).map_err(|e| e.to_string())?;
                file.sync_all().map_err(|e| e.to_string())?;
                verify_leaf(content, &leaf, &file)?;
                content.sync_all().map_err(|e| e.to_string())?;
                file
            }
            Err(_) => {
                let file = open_at(content, &leaf, libc::O_RDONLY)?;
                plain(&file)?;
                if Self::payload(content, &leaf, &id, bytes.len() as u64)? != bytes {
                    return Err("App payload collision or changed content".into());
                }
                file.sync_all().map_err(|e| e.to_string())?;
                content.sync_all().map_err(|e| e.to_string())?;
                file
            }
        };
        Ok((json!({"content":id,"byteLength":bytes.len()}), file))
    }
    fn verify_content(folder: &File, content: &File, held: &[(Value, File)]) -> Result<(), String> {
        let named = open_at(folder, "content", libc::O_RDONLY | libc::O_DIRECTORY)?;
        if identity(&named)? != identity(content)? {
            return Err("App source content directory replaced during publication".into());
        }
        for (reference, file) in held {
            let id = &reference["content"];
            let leaf = format!("{}.utf8", payload_key(id)?);
            verify_leaf(content, &leaf, file)?;
            Self::payload(
                content,
                &leaf,
                id,
                reference["byteLength"]
                    .as_u64()
                    .ok_or("payload length absent")?,
            )?;
            verify_leaf(content, &leaf, file)?;
        }
        let named = open_at(folder, "content", libc::O_RDONLY | libc::O_DIRECTORY)?;
        if identity(&named)? != identity(content)? {
            return Err("App source content directory replaced during verification".into());
        }
        Ok(())
    }
    fn payload(folder: &File, leaf: &str, id: &Value, len: u64) -> Result<Vec<u8>, String> {
        let mut file = open_at(folder, leaf, libc::O_RDONLY)?;
        plain(&file)?;
        let before = file.metadata().map_err(|e| e.to_string())?;
        if before.len() != len {
            return Err("App content length differs".into());
        }
        let mut bytes = vec![];
        file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
        let after = file.metadata().map_err(|e| e.to_string())?;
        if (
            before.len(),
            before.mtime(),
            before.mtime_nsec(),
            before.ctime(),
            before.ctime_nsec(),
        ) != (
            after.len(),
            after.mtime(),
            after.mtime_nsec(),
            after.ctime(),
            after.ctime_nsec(),
        ) || role_supply::content(&bytes) != *id
        {
            return Err("App content identity differs or changed during read".into());
        }
        let named=open_at(folder,leaf,libc::O_RDONLY)?;plain(&named)?;
        if LogBasis::of(&named.metadata().map_err(|e|e.to_string())?)!=LogBasis::of(&after){return Err("App content leaf changed before named-file check".into());}
        verify_leaf(folder, leaf, &file)?;
        Ok(bytes)
    }
    pub(crate) fn append(&self, row:Value, composition:Option<&role_supply::Composition>) -> Result<Value,String> {
        self.append_row(row,composition).map(|(status,_,_)|status)
    }
    fn append_row(
        &self,
        mut row: Value,
        composition: Option<&role_supply::Composition>,
    ) -> Result<(Value, Value, PublicationBasis), String> {
        // The Root shares this owner across homes. Serialize initial store
        // attachment too, before the cross-process log lock can be opened.
        let _owner = self
            .writer
            .lock()
            .map_err(|_| "role observation writer owner unavailable")?;
        let Some((path, folder, _admission, _writer)) = self.location(true)? else {
            return Err("role observation store unavailable".into());
        };
        let lock = open_at(&folder, ".writer.lock", libc::O_RDWR | libc::O_CREAT)?;
        plain(&lock)?;
        if unsafe { libc::flock(lock.as_raw_fd(), libc::LOCK_EX) } != 0 {
            return Err(std::io::Error::last_os_error().to_string());
        }
        let (rows, chain, basis) = Self::read_lines(&folder, &path)?;
        if rows
            .iter()
            .any(|v| v["observationId"] == row["observationId"])
        {
            return Err("role observation identity already exists; no duplicate append".into());
        }
        let mut content = None;
        let mut held = vec![];
        if let Some(composition) = composition {
            composition.verify()?;
            if row["carried"] != composition.carried {
                return Err("observed carrier differs from the pinned App composition".into());
            }
            let payloads =
                child(&folder, "content", true)?.ok_or("App content folder unavailable")?;
            let (composed, file) = Self::publish_bytes(&payloads, composition.text.as_bytes())?;
            held.push((composed.clone(), file));
            let mut parts = vec![];
            for p in composition.carried["developerInstructions"]["parts"]
                .as_array()
                .ok_or("App guidance parts absent")?
            {
                let start = usize::try_from(p["offset"].as_u64().ok_or("part offset absent")?)
                    .map_err(|e| e.to_string())?;
                let length = usize::try_from(p["length"].as_u64().ok_or("part length absent")?)
                    .map_err(|e| e.to_string())?;
                let end = start.checked_add(length).ok_or("part range overflow")?;
                let (reference, file) = Self::publish_bytes(
                    &payloads,
                    composition
                        .text
                        .as_bytes()
                        .get(start..end)
                        .ok_or("part range outside App bytes")?,
                )?;
                held.push((reference.clone(), file));
                parts.push(reference);
            }
            row["appBytes"] = if row["formatVersion"] == "0.1" {
                json!({"composed":composed,"parts":parts})
            } else {
                let account = crate::conversation_roles::frozen_limit_account(composition)?;
                receiving::validate_limit(&account)?;
                let bytes = serde_json::to_vec(&account).map_err(|e| e.to_string())?;
                let (limit, file) = Self::publish_bytes(&payloads, &bytes)?;
                held.push((limit.clone(), file));
                {
                    let mut native_children = vec![];
                    for child in &composition.children {
                        let (child_composed, file) =
                            Self::publish_bytes(&payloads, child.composition.text.as_bytes())?;
                        held.push((child_composed.clone(), file));
                        let (envelope, file) = Self::publish_bytes(&payloads, &child.envelope)?;
                        held.push((envelope.clone(), file));
                        let mut child_parts = vec![];
                        for part in child.composition.carried["developerInstructions"]["parts"]
                            .as_array()
                            .ok_or("child source parts absent")?
                        {
                            let start =
                                part["offset"].as_u64().ok_or("child offset absent")? as usize;
                            let length =
                                part["length"].as_u64().ok_or("child length absent")? as usize;
                            let bytes = child
                                .composition
                                .text
                                .as_bytes()
                                .get(
                                    start
                                        ..start
                                            .checked_add(length)
                                            .ok_or("child source overflow")?,
                                )
                                .ok_or("child source outside composition")?;
                            let (reference, file) = Self::publish_bytes(&payloads, bytes)?;
                            held.push((reference.clone(), file));
                            child_parts.push(reference);
                        }
                        let child_limit =
                            crate::conversation_roles::frozen_limit_account(&child.composition)?;
                        let (child_limit, file) = Self::publish_bytes(
                            &payloads,
                            &serde_json::to_vec(&child_limit).map_err(|e| e.to_string())?,
                        )?;
                        held.push((child_limit.clone(), file));
                        native_children.push(json!({"role":child.role,"carried":child.composition.carried,"composed":child_composed,"parts":child_parts,"file":envelope,"limitAccount":child_limit}));
                    }
                    let mut bytes = json!({"composed":composed,"parts":parts,"limitAccount":limit});
                    if row["formatVersion"] == "0.3" {
                        bytes["nativeChildren"] = json!(native_children);
                    }
                    bytes
                }
            };
            content = Some(payloads);
        }
        let project = records_store::attach(&self.project, false)?
            .project
            .ok_or("record store project identity absent")?;
        row["project"] = json!({"projectId":project,"sourceRoot":crate::attachments::native_path_identity(&self.project),"device":self.project_identity.0,"inode":self.project_identity.1});
        row["seq"] = json!(chain.lines + 1);
        row["prevLine"] = record_lines::link(chain.last.as_deref());
        row["recordedAt"] = json!(crate::util::now_rfc3339());
        validate(&row)?;
        let mut raw = serde_json::to_vec(&row).map_err(|e| e.to_string())?;
        raw.push(b'\n');
        #[cfg(test)]
        if let Some(hook) = BEFORE_APPEND.with(|slot| slot.borrow_mut().take()) {
            hook();
        }
        self.check_project()?;
        verify_directory(&path, &folder)?;
        if let Some(content) = &content {
            Self::verify_content(&folder, content, &held)?;
        }
        let mut file = open_at(
            &folder,
            LOG,
            libc::O_WRONLY
                | libc::O_APPEND
                | if basis.is_none() {
                    libc::O_CREAT | libc::O_EXCL
                } else {
                    0
                },
        )?;
        plain(&file)?;
        if let Some(basis) = basis {
            if LogBasis::of(&file.metadata().map_err(|e| e.to_string())?) != basis {
                return Err("role observation log changed or was replaced before append; no replacement written".into());
            }
        }
        file.write_all(&raw)
            .map_err(|e| format!("role observation append uncertain: {e}"))?;
        file.sync_all()
            .map_err(|e| format!("role observation file flush uncertain: {e}"))?;
        #[cfg(test)]
        if FAIL_AFTER_FILE_SYNC.with(|fail| fail.replace(false)) {
            return Err(
                "injected role observation publication unconfirmed after file flush".into(),
            );
        }
        folder
            .sync_all()
            .map_err(|e| format!("role observation directory flush uncertain: {e}"))?;
        verify_leaf(&folder, LOG, &file)?;
        self.check_project()?;
        verify_directory(&path, &folder)?;
        if let Some(content) = &content {
            Self::verify_content(&folder, content, &held)?;
        }
        Ok((
            json!({"state":"written","observationId":row["observationId"],"supplyId":row["supplyId"],"standing":"App observation publication confirmed; supplier adoption and current role authority remain separate"}),
            row,
            PublicationBasis {
                path,
                folder: identity(&folder)?,
                log: identity(&file)?,
            },
        ))
    }
    fn source_bytes(content: Option<&File>, row: &Value) -> Result<Value, String> {
        let folder = content.ok_or("App source content folder absent")?;
        let refs = &row["appBytes"];
        let get = |reference: &Value| -> Result<String, String> {
            let id = &reference["content"];
            let leaf = format!("{}.utf8", payload_key(id)?);
            let length = reference["byteLength"]
                .as_u64()
                .ok_or("source length absent")?;
            String::from_utf8(Self::payload(folder, &leaf, id, length)?).map_err(|e| e.to_string())
        };
        let composed = get(&refs["composed"])?;
        let part_refs = refs["parts"].as_array().ok_or("source part refs absent")?;
        let carried = &row["carried"]["developerInstructions"];
        let metadata = carried["parts"].as_array().ok_or("carried parts absent")?;
        if carried["content"] != role_supply::content(composed.as_bytes())
            || carried["byteLength"] != composed.len()
            || part_refs.len() != metadata.len()
        {
            return Err("quoted composition identity/parts differ".into());
        }
        let mut parts = vec![];
        for (part, reference) in metadata.iter().zip(part_refs) {
            let bytes = get(reference)?;
            let start = usize::try_from(part["offset"].as_u64().ok_or("part offset absent")?)
                .map_err(|e| e.to_string())?;
            let length = usize::try_from(part["length"].as_u64().ok_or("part length absent")?)
                .map_err(|e| e.to_string())?;
            let end = start.checked_add(length).ok_or("part range overflow")?;
            if part["content"] != role_supply::content(bytes.as_bytes())
                || composed.as_bytes().get(start..end) != Some(bytes.as_bytes())
            {
                return Err("quoted part bytes/range differ".into());
            }
            parts.push(json!({"source":part["source"],"kind":part["kind"],"role":part["role"],"text":bytes}));
        }
        let supplied = row["carried"]["nativeChildRoles"]
            .as_array()
            .into_iter()
            .flatten()
            .filter(|r| r["status"] == "supplied")
            .collect::<Vec<_>>();
        let mut expected = std::collections::BTreeSet::new();
        for child in &supplied {
            let role = child["role"]
                .as_str()
                .ok_or("quoted supplied child role absent")?;
            if !expected.insert(role.to_owned()) {
                return Err("quoted supplied child roles repeat".into());
            }
        }
        if row["formatVersion"] == "0.3" {
            let children = refs
                .get("nativeChildren")
                .and_then(Value::as_array)
                .ok_or("quoted native child payload set absent")?;
            let mut actual = std::collections::BTreeSet::new();
            for child in children {
                let role = child["role"]
                    .as_str()
                    .ok_or("quoted child payload role absent")?;
                if !actual.insert(role.to_owned()) {
                    return Err("quoted child payload roles repeat".into());
                }
            }
            if actual != expected {
                return Err("quoted native child payload set differs from supplied roles".into());
            }
        }
        let mut native_children = vec![];
        if let Some(children) = refs.get("nativeChildren").and_then(Value::as_array) {
            for child in children {
                let child_row = json!({"appBytes":{"composed":child["composed"],"parts":child["parts"]},"carried":child["carried"]});
                let mut bytes = Self::source_bytes(Some(folder), &child_row)?;
                let metadata = child["carried"]["developerInstructions"]["parts"]
                    .as_array()
                    .ok_or("quoted child parts absent")?;
                let role = child["role"].as_str().ok_or("quoted child role absent")?;
                if metadata.len() != 2
                    || metadata[0]["kind"] != "product-guidance"
                    || metadata[0]["source"]["path"] != "AGENTS.md"
                    || metadata[1]["kind"] != "role-guidance"
                    || metadata[1]["role"] != role
                    || metadata[1]["source"]["path"] != format!("agents/AGENT_{role}.md")
                {
                    return Err("quoted child role/source metadata differs".into());
                }
                let child_parts = bytes["parts"]
                    .as_array()
                    .ok_or("quoted child exact parts absent")?;
                if bytes["composed"]
                    != format!(
                        "{}\n\n# Active role: {role}\n\n{}",
                        child_parts[0]["text"]
                            .as_str()
                            .ok_or("quoted common text absent")?,
                        child_parts[1]["text"]
                            .as_str()
                            .ok_or("quoted role text absent")?
                    )
                {
                    return Err("quoted child framing differs".into());
                }

                if metadata[0] != row["carried"]["developerInstructions"]["parts"][0]
                    || child_parts[0]["text"] != parts[0]["text"]
                {
                    return Err("quoted child common source differs from original parent".into());
                }
                let envelope = get(&child["file"])?;
                let account = get(&child["limitAccount"])?;
                let parsed: toml::Value =
                    toml::from_str(&envelope).map_err(|_| "quoted child envelope invalid")?;
                let supplied = row["carried"]["nativeChildRoles"]
                    .as_array()
                    .ok_or("child supply account absent")?
                    .iter()
                    .find(|r| r["role"] == child["role"] && r["status"] == "supplied")
                    .ok_or("child has no carried supply")?;
                if parsed.as_table().is_none_or(|t| t.len() != 1)
                    || supplied["composed"] != child["composed"]["content"]
                    || supplied["file"] != child["file"]["content"]
                    || parsed["developer_instructions"].as_str() != bytes["composed"].as_str()
                {
                    return Err("quoted child composition/envelope differs".into());
                }
                let account: Value =
                    serde_json::from_str(&account).map_err(|_| "quoted child limits invalid")?;
                receiving::validate_limit(&account)?;
                let role: crate::role_supply::Role = serde_json::from_value(child["role"].clone())
                    .map_err(|_| "quoted child role unknown")?;
                let quoted = crate::role_supply::Composition::quoted(
                    Some(role),
                    row["selection"]["roleSet"].clone(),
                    bytes["composed"]
                        .as_str()
                        .ok_or("quoted child text absent")?
                        .to_owned(),
                    child["carried"].clone(),
                )?;
                let expected = crate::conversation_roles::frozen_limit_account(&quoted)?;
                if account != expected {
                    return Err("quoted child original limits/source comparison differs".into());
                }
                bytes["role"] = child["role"].clone();
                bytes["envelope"] = json!(envelope);
                bytes["limitAccount"] = account;
                native_children.push(bytes);
            }
        }
        Ok(json!({"composed":composed,"parts":parts,"nativeChildren":native_children}))
    }
    fn head(chain: &record_lines::Chain) -> Value {
        json!({"method":record_lines::LINE_METHOD,"head":chain.last,"lines":chain.lines,"linked":chain.linked,"unchained":chain.unchained,"unchainedLimit":chain.unchained_note("role supply observations"),"broken":[],"signedCheckpoints":"not written: they wait for App signing (OI-011)"})
    }
    pub fn read(&self, home: &str, thread: Option<&str>) -> Value {
        let result = (|| -> Result<Value, String> {
            let Some((path, folder, _admission, _writer)) = self.location(false)? else {
                return Ok(
                    json!({"observations":[],"limits":["no role supply log at this project's store"],"standing":STANDING,"currentRoleAuthorityRestored":false}),
                );
            };
            let (rows, chain, _basis) = Self::read_lines(&folder, &path)?;
            let content = child(&folder, "content", false)?;
            let mut out = vec![];
            let mut limits = vec![];
            if let Some(note) = chain.unchained_note("role supply observations") {
                limits.push(note);
            }
            for row in &rows {
                if row["format"] == "chirality.role.supply" {
                    if thread.is_none() {
                        out.push(json!({"record":row,"legacy":true,"sourceBytes":null,"limits":["legacy0.2 has no full H5/home provenance; preserved quoted evidence only"]}));
                    } else {
                        limits.push("Unattributed legacy0.2 role evidence is present; inspect the full project role history, never infer its native home".into());
                    }
                    continue;
                }
                if (row["request"]["home"] != home
                    && !(thread.is_none() && row["request"]["home"].is_null()))
                    || thread.is_some_and(|thread| row["thread"].as_str() != Some(thread))
                {
                    continue;
                }
                let mut row_limits = vec![];
                let source = if row["appBytes"].is_object() {
                    Self::source_bytes(content.as_ref(), &row)
                        .map_err(|error| row_limits.push(error))
                        .ok()
                } else {
                    None
                };
                let reference = row["lineage"]["inheritedFrom"]
                    .as_str()
                    .or_else(|| row["lineage"]["continuedFrom"]["sourceStartRecord"].as_str())
                    .or_else(||row["lineage"]["parentSupplyRef"].as_str())
                    .or_else(||row["lineage"]["originalParentSupplyRef"].as_str());
                let mut lineage = vec![];
                if let Some(reference) = reference {
                    lineage=rows.iter().filter(|candidate|candidate["format"]==FORMAT && candidate["supplyId"]==reference && candidate["request"]["home"]==home).map(|candidate|json!({"observationId":candidate["observationId"],"outcome":candidate["outcome"],"standing":"quoted source reference only"})).collect();
                    if lineage.is_empty() {
                        row_limits.push("Referenced source supply account not found in this project/home; no source observation or inherited guidance inferred".into());
                    }
                }
                out.push(json!({"record":row,"sourceBytes":source,"limits":row_limits,"lineageObservations":lineage}));
            }
            if let Some(content)=&content {verify_directory_child(&folder,"content",content)?;}
            self.check_project()?;
            verify_directory(&path, &folder)?;
            Ok(
                json!({"observations":out,"limits":limits,"standing":STANDING,"currentRoleAuthorityRestored":false}),
            )
        })();
        result.unwrap_or_else(|limit|json!({"observations":[],"limits":[limit],"standing":STANDING,"complete":false,"currentRoleAuthorityRestored":false}))
    }
}

/// Export copies and the person's on-demand head view use this format's
/// schema/chain reader; these observations are never parsed as R1 records.
pub(crate) fn copied_chain_head(path: &Path) -> Value {
    let result = (|| -> Result<Value, String> {
        if path.file_name().and_then(|v| v.to_str()) != Some(LOG) {
            return Err("unexpected role supply log name".into());
        }
        let parent = path.parent().ok_or("role supply folder absent")?;
        let folder = directory(parent)?;
        let (_rows, chain, basis) = RoleLog::read_lines(&folder, parent)?;
        if basis.is_none() {
            return Err("role supply log absent".into());
        }
        verify_directory(parent, &folder)?;
        Ok(RoleLog::head(&chain))
    })();
    result.unwrap_or_else(
        |error| json!({"state":"unreadable or invalid role supply chain","error":error}),
    )
}
pub(crate) fn project_chain_head(project: &Path) -> Result<Option<Value>, String> {
    let log = RoleLog::open(project)?;
    let Some((path, folder, _admission, _writer)) = log.location(false)? else {
        return Ok(None);
    };
    let (_rows, chain, basis) = RoleLog::read_lines(&folder, &path)?;
    if basis.is_none() {
        return Ok(None);
    }
    log.check_project()?;
    verify_directory(&path, &folder)?;
    let mut head = RoleLog::head(&chain);
    head["log"] = json!(path.join(LOG));
    Ok(Some(head))
}

pub(crate) fn row(
    supply_id: &str,
    trigger: &str,
    thread: Option<&str>,
    request: Value,
    selection: Value,
    outcome: &str,
    carried: Option<Value>,
    supplier_reported: Value,
    lineage: Value,
    limit: Option<&str>,
) -> Result<Value, String> {
    let mut row = json!({"format":FORMAT,"formatVersion":"0.3","observationId":crate::util::opaque_id("role-observation:v1:")?,"supplyId":supply_id,"recorder":"App DEL-02-04 role supply observer","trigger":trigger,"thread":thread,"request":request,"selection":selection,"outcome":outcome,"supplierReported":supplier_reported,"lineage":lineage,"adoption":"unknown"});
    if let Some(carried) = carried {
        row["carried"] = carried;
    }
    if let Some(limit) = limit {
        row["evidenceLimit"] = json!(limit);
    }
    Ok(row)
}
pub(crate) fn request(status: &Value) -> Value {
    json!({"home":status["home"],"generation":status["generation"],"requestIdentity":status["requestIdentity"],"requestRef":status["requestRef"],"method":status["sentFrame"]["method"],"writeResult":status["writeResult"],"outcome":status["outcome"],"sourceCurrent":status["sourceCurrent"]})
}
pub(crate) fn reported(status: &Value) -> Value {
    let r = &status["response"]["result"];
    json!({"instructionSources":r.get("instructionSources").filter(|v|v.as_array().is_some_and(|a|a.iter().all(Value::is_string))).cloned().unwrap_or(Value::Null),"agentRole":r["thread"].get("agentRole").filter(|v|v.is_string()).cloned().unwrap_or(Value::Null),"forkedFromId":r["thread"].get("forkedFromId").filter(|v|v.is_string()).cloned().unwrap_or(Value::Null)})
}

#[cfg(test)]
#[path = "role_observations_tests.rs"]
mod tests;
