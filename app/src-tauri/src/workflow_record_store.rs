//! WR WP-1..7. Evidence resolution is historical, never a live native capability.
use super::{PreparedRunText, Selection, SelectionAdmission};
use serde_json::{json, Value};
use std::{
    ffi::CString,
    fs::File,
    io::{Read, Write},
    os::fd::{AsRawFd, FromRawFd},
    os::unix::fs::MetadataExt,
    path::{Path, PathBuf},
};
const PREFIX: &str = "wr-record:v1:";
const SCHEMA: &str =
    include_str!("../resources/workflow_role/workflow-record-envelope.schema.json");
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ResolutionError {
    Missing,
    Unreadable(String),
    Invalid(String),
    Unsupported,
    Conflicting,
}
fn key(reference: &str) -> Result<&str, ResolutionError> {
    let s = reference
        .strip_prefix(PREFIX)
        .ok_or_else(|| ResolutionError::Invalid("WR reference prefix".into()))?;
    if s.len() != 36
        || s.bytes().enumerate().any(|(i, b)| {
            if [8, 13, 18, 23].contains(&i) {
                b != b'-'
            } else {
                !b.is_ascii_digit() && !(b'a'..=b'f').contains(&b)
            }
        })
    {
        return Err(ResolutionError::Invalid("WR reference UUID".into()));
    }
    Ok(s)
}
fn ioerr(e: std::io::Error) -> ResolutionError {
    if e.kind() == std::io::ErrorKind::NotFound {
        ResolutionError::Missing
    } else {
        ResolutionError::Unreadable(e.to_string())
    }
}
fn name(s: &str) -> Result<CString, String> {
    CString::new(s).map_err(|_| "NUL in owning path".into())
}
fn open_at(dir: &File, leaf: &str, flags: i32) -> Result<File, std::io::Error> {
    let n = CString::new(leaf)
        .map_err(|_| std::io::Error::new(std::io::ErrorKind::InvalidInput, "NUL"))?;
    let fd = unsafe {
        libc::openat(
            dir.as_raw_fd(),
            n.as_ptr(),
            flags | libc::O_NOFOLLOW | libc::O_CLOEXEC,
            0o600,
        )
    };
    if fd < 0 {
        Err(std::io::Error::last_os_error())
    } else {
        Ok(unsafe { File::from_raw_fd(fd) })
    }
}
fn child(dir: &File, leaf: &str, create: bool) -> Result<File, String> {
    if create {
        let n = name(leaf)?;
        if unsafe { libc::mkdirat(dir.as_raw_fd(), n.as_ptr(), 0o700) } < 0 {
            let e = std::io::Error::last_os_error();
            if e.kind() != std::io::ErrorKind::AlreadyExists {
                return Err(e.to_string());
            }
        }
    }
    let f = open_at(dir, leaf, libc::O_RDONLY | libc::O_DIRECTORY).map_err(|e| e.to_string())?;
    if create {
        f.sync_all().map_err(|e| e.to_string())?;
        dir.sync_all().map_err(|e| e.to_string())?;
    }
    Ok(f)
}
/// Opens `leaf` under `dir` as a plain directory without following symlinks.
/// Ok(None) only when the entry is absent; a symlink or other entry is an error.
fn plain_dir_at(dir: &File, leaf: &str) -> Result<Option<File>, String> {
    match open_at(dir, leaf, libc::O_RDONLY | libc::O_DIRECTORY) {
        Ok(f) => Ok(Some(f)),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            // ENOENT from openat with O_NOFOLLOW means the name itself is absent
            // (a dangling symlink reports ELOOP or ENOTDIR, not ENOENT).
            Ok(None)
        }
        Err(e) => Err(format!(
            "WR record path entry '{leaf}' is not a plain directory (symlink or other): {e}"
        )),
    }
}
/// Names in a directory, read through a duplicate of its pinned descriptor.
fn dir_names(dir: &File) -> Result<Vec<String>, String> {
    let fd = unsafe { libc::dup(dir.as_raw_fd()) };
    if fd < 0 {
        return Err(std::io::Error::last_os_error().to_string());
    }
    let stream = unsafe { libc::fdopendir(fd) };
    if stream.is_null() {
        let e = std::io::Error::last_os_error();
        unsafe { libc::close(fd) };
        return Err(e.to_string());
    }
    unsafe { libc::rewinddir(stream) };
    let mut names = Vec::new();
    loop {
        let entry = unsafe { libc::readdir(stream) };
        if entry.is_null() {
            break;
        }
        let name = unsafe { std::ffi::CStr::from_ptr((*entry).d_name.as_ptr()) };
        if let Ok(name) = name.to_str() {
            if name != "." && name != ".." {
                names.push(name.to_owned());
            }
        }
    }
    unsafe { libc::closedir(stream) };
    Ok(names)
}
fn validate(envelope: &Value) -> Result<(), String> {
    let wr: Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/workspace-registration.schema.json"
    ))
    .map_err(|e| e.to_string())?;
    let wd: Value =
        serde_json::from_str(crate::workflow_declaration::SCHEMA).map_err(|e| e.to_string())?;
    let schema: Value = serde_json::from_str(SCHEMA).map_err(|e| e.to_string())?;
    let mut registry = jsonschema::Registry::new();
    for s in [wd, wr] {
        registry = registry
            .add(s["$id"].as_str().ok_or("schema ID absent")?, s.clone())
            .map_err(|e| e.to_string())?;
    }
    let registry = registry.prepare().map_err(|e| e.to_string())?;
    jsonschema::options()
        .with_registry(&registry)
        .offline()
        .build(&schema)
        .map_err(|e| e.to_string())?
        .validate(envelope)
        .map_err(|e| e.to_string())
}
/// Explicit opened-project scope. Directory descriptor traversal never follows symlinks.
#[derive(Debug)]
pub struct ProjectRecords {
    root: PathBuf,
    directory: File,
    identity: (u64, u64),
}
impl ProjectRecords {
    pub fn open(explicit_root: &Path) -> Result<Self, String> {
        if !explicit_root.is_absolute() {
            return Err("explicit absolute opened project required; no cwd fallback".into());
        }
        // Pin every component, rejecting symlinks and parent traversal before use.
        let mut directory = File::open("/").map_err(|e| e.to_string())?;
        for part in explicit_root.components() {
            match part {
                std::path::Component::RootDir => {}
                std::path::Component::Normal(s) => {
                    directory = child(
                        &directory,
                        s.to_str().ok_or("non-UTF8 project component")?,
                        false,
                    )?;
                }
                _ => return Err("non-normal opened-project path".into()),
            }
        }
        let m = directory.metadata().map_err(|e| e.to_string())?;
        Ok(Self {
            root: explicit_root.to_owned(),
            directory,
            identity: (m.dev(), m.ino()),
        })
    }
    /// The explicit opened-project path this handle was opened from.
    pub fn root(&self) -> &Path {
        &self.root
    }
    /// References of this project's own published WR records (non-recursive;
    /// no other project or library is searched). Staging files are excluded.
    /// V9 F-5: every step is relative to the pinned project descriptor and never
    /// follows a symlink. An absent store is "no records"; a symlinked (even
    /// dangling) or otherwise non-plain `.chirality`, `records` or `workflow`
    /// entry is reported as an error, never as "no records".
    pub fn list_references(&self) -> Result<Vec<String>, String> {
        let Some(a) = plain_dir_at(&self.directory, ".chirality")? else {
            return Ok(vec![]);
        };
        let Some(b) = plain_dir_at(&a, "records")? else {
            return Ok(vec![]);
        };
        let Some(dir) = plain_dir_at(&b, "workflow")? else {
            return Ok(vec![]);
        };
        let mut references = Vec::new();
        for name in dir_names(&dir)? {
            if let Some(stem) = name.strip_suffix(".json") {
                let reference = format!("{PREFIX}{stem}");
                if key(&reference).is_ok() {
                    references.push(reference);
                }
            }
        }
        references.sort();
        Ok(references)
    }
    fn records(&self, create: bool) -> Result<File, String> {
        let a = child(&self.directory, ".chirality", create)?;
        let b = child(&a, "records", create)?;
        child(&b, "workflow", create)
    }
    fn read_raw(&self, reference: &str) -> Result<ResolvedRecord, ResolutionError> {
        let k = key(reference)?;
        let dir = self.records(false).map_err(ResolutionError::Unreadable)?;
        let mut f = open_at(&dir, &format!("{k}.json"), libc::O_RDONLY).map_err(ioerr)?;
        if !f.metadata().map_err(ioerr)?.is_file() {
            return Err(ResolutionError::Invalid("not regular file".into()));
        }
        let mut bytes = Vec::new();
        f.read_to_end(&mut bytes).map_err(ioerr)?;
        let envelope: Value =
            serde_json::from_slice(&bytes).map_err(|e| ResolutionError::Invalid(e.to_string()))?;
        if envelope["version"] != 1 {
            return Err(ResolutionError::Unsupported);
        }
        validate(&envelope).map_err(ResolutionError::Invalid)?;
        if envelope["record_id"] != reference {
            return Err(ResolutionError::Conflicting);
        }
        Ok(ResolvedRecord {
            root: self.root.clone(),
            project: self.identity,
            envelope,
            bytes,
        })
    }
    fn relations(&self, e: &Value) -> Result<(), ResolutionError> {
        let b = &e["body"];
        let refs = e["basis_records"]
            .as_array()
            .ok_or_else(|| ResolutionError::Invalid("basis absent".into()))?;
        let kind = b["record_kind"].as_str().unwrap_or("");
        let expected = match kind {
            "selection_record" => None,
            "run_text" if b["purpose"] == "run start" => Some("selection_record"),
            "run_text" if b["purpose"] == "run end notice" => Some("run_text"),
            "supply_check" => Some("run_text"),
            _ => None,
        };
        if refs.len() != usize::from(expected.is_some()) {
            return Err(ResolutionError::Invalid("wrong WR basis count".into()));
        }
        if let Some(expected) = expected {
            let source = self.read_raw(refs[0].as_str().unwrap_or(""))?;
            let a = source.body();
            if a["record_kind"] != expected || a["conversation"] != b["conversation"] {
                return Err(ResolutionError::Conflicting);
            }
            if kind == "run_text" && b["purpose"] == "run start" {
                if a["selection_id"] != b["selection"]
                    || a["identity"] != b["workflow"]
                    || a["holding_library"] != b["holding_library"]
                {
                    return Err(ResolutionError::Conflicting);
                }
            } else if kind == "run_text" {
                if a["purpose"] != "run start" || a["run"] != b["run"] {
                    return Err(ResolutionError::Conflicting);
                }
                self.relations(source.envelope())?;
            } else {
                self.relations(source.envelope())?;
                if a["run"] != b["run"]
                    || a["purpose"] != b["purpose"]
                    || a["text_identity"] != b["expected_text"]
                    || (a["purpose"] == "run start"
                        && b.get("expected_workflow").is_some()
                        && a["workflow_file"]["content"] != b["expected_workflow"])
                {
                    return Err(ResolutionError::Conflicting);
                }
            }
        }
        Ok(())
    }
    pub fn resolve(&self, reference: &str) -> Result<ResolvedRecord, ResolutionError> {
        let r = self.read_raw(reference)?;
        self.relations(r.envelope())?;
        Ok(r)
    }
    pub fn publish(&self, pending: &PendingRecord) -> Result<ResolvedRecord, String> {
        if pending.project != self.identity {
            return Err("pending WR record belongs to another project".into());
        }
        validate(&pending.envelope)?;
        self.relations(&pending.envelope)
            .map_err(|e| format!("WR basis: {e:?}"))?;
        let reference = pending.reference();
        let k = key(reference).map_err(|e| format!("{e:?}"))?;
        let dir = self.records(true)?;
        let final_name = format!("{k}.json");
        // A prior uncertain successful link is retried with the original bytes.
        if let Ok(mut f) = open_at(&dir, &final_name, libc::O_RDONLY) {
            let mut existing = Vec::new();
            f.read_to_end(&mut existing).map_err(|e| e.to_string())?;
            if existing != pending.bytes {
                return Err("WR identity collision; refusing overwrite".into());
            }
            f.sync_all().map_err(|e| e.to_string())?;
            dir.sync_all().map_err(|e| e.to_string())?;
            return self.resolve(reference).map_err(|e| format!("{e:?}"));
        }
        let staging = crate::util::opaque_id(".pending-")?;
        let mut file = open_at(
            &dir,
            &staging,
            libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL,
        )
        .map_err(|e| e.to_string())?;
        let result = (|| {
            file.write_all(&pending.bytes).map_err(|e| e.to_string())?;
            file.sync_all().map_err(|e| e.to_string())?;
            let from = name(&staging)?;
            let to = name(&final_name)?;
            if unsafe {
                libc::linkat(
                    dir.as_raw_fd(),
                    from.as_ptr(),
                    dir.as_raw_fd(),
                    to.as_ptr(),
                    0,
                )
            } < 0
            {
                return Err(format!(
                    "WR no-replace publication: {}",
                    std::io::Error::last_os_error()
                ));
            }
            publication_boundary()?;
            dir.sync_all().map_err(|e| e.to_string())?;
            self.resolve(reference).map_err(|e| format!("{e:?}"))
        })();
        if let Ok(n) = name(&staging) {
            unsafe { libc::unlinkat(dir.as_raw_fd(), n.as_ptr(), 0) };
        }
        result
    }
}
/// Durable historical evidence only. There is deliberately no deserializer or send API.
#[derive(Debug)]
pub struct ResolvedRecord {
    root: PathBuf,
    project: (u64, u64),
    envelope: Value,
    bytes: Vec<u8>,
}
impl ResolvedRecord {
    pub fn reference(&self) -> &str {
        self.envelope["record_id"].as_str().unwrap()
    }
    pub fn body(&self) -> &Value {
        &self.envelope["body"]
    }
    pub fn envelope(&self) -> &Value {
        &self.envelope
    }
    pub fn project_root(&self) -> &Path {
        &self.root
    }
    pub fn same_project(&self, other: &Self) -> bool {
        self.project == other.project
    }
    pub fn bytes(&self) -> &[u8] {
        &self.bytes
    }
}
/// Minted only at the genuine native comparison boundary: a consumed Host
/// coverage seal plus pages the issuing Host confirms are its retained results
/// for that traversal; for *unreadable*, the Host-issued item dispatches; for a
/// refused start, the Host's typed refusal. No public constructor, Deserialize
/// or Clone; JSON or a cold record cannot mint one.
#[derive(Debug)]
pub struct CompletedSupplyCheck {
    body: Value,
    sources: Vec<String>,
}
const CHECK_LIMIT: &str = "one source-bound native item traversal checked at its final owning guard; not ongoing native authority";
const SUPPLY_LIMIT: &str = "supplied is not adopted: model uptake unknown; no run opening, run end, A15 or completion inferred";
impl CompletedSupplyCheck {
    /// SC-3/SC-4 at the genuine boundary. The seal is consumed: one traversal
    /// mints at most one check. The pages must equal, byte for byte and in order,
    /// the results the issuing Host retained for the sealed source requests
    /// (V9 F-3: `Host::native_coverage_pages_match`), not merely their count.
    pub(crate) fn from_native_coverage(
        host: &crate::hosting::Host,
        seal: crate::hosting::NativeItemCoverageSeal,
        pages: &[Value],
        published: &dyn PublishedText,
        turn: &str,
        client_id: &str,
        check: &str,
        read_at: &str,
    ) -> Result<Self, String> {
        let run_text = published.run_text_record().body();
        let query = seal.query();
        if query.method() != "thread/items/list"
            || query.params()["threadId"] != run_text["conversation"]
            || query.params()["turnId"] != turn
        {
            return Err("native coverage belongs to another thread/turn".into());
        }
        if pages.is_empty() {
            return Err("checked pages differ from the sealed native coverage".into());
        }
        host.native_coverage_pages_match(&seal, pages)?;
        let mut index = 0;
        let located = super::locate_turn_text(turn, client_id, |_| {
            let page = pages.get(index).cloned().ok_or("no sealed native page")?;
            index += 1;
            Ok(page)
        });
        let body = check_body(
            run_text,
            published.prepared(),
            Observation::Located(located),
            turn,
            client_id,
            check,
            read_at,
        )?;
        let sources = seal
            .source_receipts()
            .map(|(_, reference, _)| reference.to_owned())
            .collect();
        Ok(Self { body, sources })
    }
    /// SC-3 *unreadable*: an item read was issued for this turn and failed
    /// before coverage completed. Requires the Host-issued dispatches.
    pub(crate) fn unreadable_after_dispatch(
        issued: &[crate::hosting::HistoryDispatch],
        published: &dyn PublishedText,
        turn: &str,
        client_id: &str,
        check: &str,
        read_at: &str,
        error: &str,
    ) -> Result<Self, String> {
        let run_text = published.run_text_record().body();
        if issued.is_empty()
            || issued.iter().any(|d| {
                d.query().method() != "thread/items/list"
                    || d.query().params()["threadId"] != run_text["conversation"]
                    || d.query().params()["turnId"] != turn
            })
        {
            return Err("no native item read was issued for this thread/turn; nothing checked".into());
        }
        let body = check_body(
            run_text,
            published.prepared(),
            Observation::ReadFailed(error),
            turn,
            client_id,
            check,
            read_at,
        )?;
        let sources = issued
            .iter()
            .map(|d| d.source().request_ref().to_owned())
            .collect();
        Ok(Self { body, sources })
    }
}
impl CompletedSupplyCheck {
    /// V9 F-1, WR §16.4 / RN-4: Codex definitely refused this exact `turn/start`
    /// before any item was recorded, so the check is *not found*, with no turn or
    /// item. Consumes the Host-issued refusal; the source is that request's
    /// receipt. An unknown outcome has no refusal value and cannot reach here.
    pub(crate) fn not_found_after_refusal(
        refusal: crate::hosting::NativeTurnRefusal,
        published: &dyn PublishedText,
        client_id: &str,
        check: &str,
        read_at: &str,
    ) -> Result<Self, String> {
        let run_text = published.run_text_record().body();
        if run_text["record_kind"] != "run_text"
            || refusal.thread() != run_text["conversation"]
            || refusal.client_id() != client_id
            || published.prepared().record() != run_text
        {
            return Err("refusal belongs to another conversation, client message or text".into());
        }
        if [client_id, check, read_at].iter().any(|s| s.is_empty()) {
            return Err("check/client/read identity required".into());
        }
        let mut body = json!({"record_kind":"supply_check","check":check,"run":run_text["run"],"conversation":run_text["conversation"],"client_user_message_id":client_id,"purpose":run_text["purpose"],"expected_text":run_text["text_identity"],"state":"not found","read_at":read_at,
            "evidence_limits":[SUPPLY_LIMIT,format!("turn/start refused by Codex (correlated native error at receipt position {}); no turn or item was recorded (WR §16.4, RN-4); the run start is not confirmed",refusal.response_position()),format!("native error: {}",refusal.error())]});
        if run_text["purpose"] == "run start" {
            body["expected_workflow"] = run_text["workflow_file"]["content"].clone();
        }
        super::wr_validate("supply_check", &body)?;
        Ok(Self {
            body,
            sources: vec![refusal.request_ref().to_owned()],
        })
    }
}
enum Observation<'a> {
    Located(super::LocatedTurnText),
    ReadFailed(&'a str),
}
/// Sealing module: `Sealed` is private to this module, so no type outside it
/// can implement `PublishedText`, and crate code cannot wrap a cold-read
/// `ResolvedRecord` or JSON into something the check constructors accept.
mod sealed {
    pub trait Sealed {}
    impl Sealed for super::PublishedRunText {}
    impl Sealed for super::PublishedEndNotice {}
}
/// A text this process composed and published before sending: its immutable
/// run_text record and the typed composed text. Sealed (V9 J3 note): only
/// `PublishedRunText` and `PublishedEndNotice`, whose only constructors are their
/// typed publications, implement it; a resolved JSON record alone is neither.
///
/// Compile-time note: implementing this trait for a type anywhere outside this file
/// fails with E0277 (`X: sealed::Sealed` not satisfied) and `sealed::Sealed` is
/// not nameable there. The test `published_text_is_sealed_to_two_types` guards
/// that this file implements it for exactly the two typed results.
pub trait PublishedText: sealed::Sealed {
    fn run_text_record(&self) -> &ResolvedRecord;
    fn prepared(&self) -> &PreparedRunText;
}
impl PublishedText for PublishedRunText {
    fn run_text_record(&self) -> &ResolvedRecord {
        &self.text
    }
    fn prepared(&self) -> &PreparedRunText {
        &self.prepared
    }
}
impl PublishedText for PublishedEndNotice {
    fn run_text_record(&self) -> &ResolvedRecord {
        &self.record
    }
    fn prepared(&self) -> &PreparedRunText {
        &self.notice
    }
}
fn check_body(
    run_text: &Value,
    prepared: &PreparedRunText,
    observation: Observation<'_>,
    turn: &str,
    client_id: &str,
    check: &str,
    read_at: &str,
) -> Result<Value, String> {
    if run_text["purpose"] == "run end notice" {
        notice_check_body(run_text, prepared, observation, turn, client_id, check, read_at)
    } else {
        supply_check_body(run_text, prepared, observation, turn, client_id, check, read_at)
    }
}
/// WR §16.4 state mapping for a run-start text. Pure; minting stays with the
/// constructors above.
fn supply_check_body(
    run_text: &Value,
    prepared: &PreparedRunText,
    observation: Observation<'_>,
    turn: &str,
    client_id: &str,
    check: &str,
    read_at: &str,
) -> Result<Value, String> {
    if run_text["record_kind"] != "run_text" || run_text["purpose"] != "run start" {
        return Err("live supply check requires a published run-start run_text".into());
    }
    if [turn, client_id, check, read_at].iter().any(|s| s.is_empty()) {
        return Err("check/turn/client/read identity required".into());
    }
    let mut body = json!({"record_kind":"supply_check","check":check,"run":run_text["run"],"conversation":run_text["conversation"],"turn":turn,"client_user_message_id":client_id,"purpose":"run start","expected_text":run_text["text_identity"],"expected_workflow":run_text["workflow_file"]["content"],"read_at":read_at});
    let mut limits = vec![CHECK_LIMIT.to_owned(), SUPPLY_LIMIT.to_owned()];
    let state = map_observation(
        &mut body,
        &mut limits,
        observation,
        prepared,
        &run_text["text_identity"],
        &run_text["workflow_file"]["content"],
    )?;
    body["state"] = json!(state);
    body["evidence_limits"] = json!(limits);
    super::wr_validate("supply_check", &body)?;
    Ok(body)
}
/// SQ-END EN-3: the check of a published end notice (TX-5). The notice has no
/// workflow bytes, so no expected_workflow is written (WP-2) and a differing
/// text can only read "text differs, workflow bytes differ".
fn notice_check_body(
    run_text: &Value,
    notice: &PreparedRunText,
    observation: Observation<'_>,
    turn: &str,
    client_id: &str,
    check: &str,
    read_at: &str,
) -> Result<Value, String> {
    if run_text["record_kind"] != "run_text"
        || run_text["purpose"] != "run end notice"
        || notice.record() != run_text
    {
        return Err("end-notice check requires the published end notice it was composed as".into());
    }
    if [turn, client_id, check, read_at].iter().any(|s| s.is_empty()) {
        return Err("check/turn/client/read identity required".into());
    }
    let mut body = json!({"record_kind":"supply_check","check":check,"run":run_text["run"],"conversation":run_text["conversation"],"turn":turn,"client_user_message_id":client_id,"purpose":"run end notice","expected_text":run_text["text_identity"],"read_at":read_at});
    let mut limits = vec![
        CHECK_LIMIT.to_owned(),
        SUPPLY_LIMIT.to_owned(),
        "end notice carries no workflow bytes; a differing text is reported as 'text differs, workflow bytes differ' (WR §16.4 has no notice-specific state)".to_owned(),
    ];
    let state = map_observation(
        &mut body,
        &mut limits,
        observation,
        notice,
        &run_text["text_identity"],
        &run_text["text_identity"],
    )?;
    body["state"] = json!(state);
    body["evidence_limits"] = json!(limits);
    super::wr_validate("supply_check", &body)?;
    Ok(body)
}
fn map_observation(
    body: &mut Value,
    limits: &mut Vec<String>,
    observation: Observation<'_>,
    prepared: &PreparedRunText,
    expected_text: &Value,
    expected_body: &Value,
) -> Result<String, String> {
    let located_by = |by_client: bool| {
        if by_client {
            "client id"
        } else {
            "first user message of the turn"
        }
    };
    let state = match observation {
        Observation::ReadFailed(error) => {
            limits.push(format!("the App observed its own send; Codex's copy could not be read ({error}); read again later (SC-6)"));
            "unreadable".to_owned()
        }
        Observation::Located(super::LocatedTurnText::Unreadable) => {
            limits.push("a sealed native page was not usable for location (shape or cursor); read again later (SC-6)".into());
            "unreadable".to_owned()
        }
        Observation::Located(super::LocatedTurnText::NotFound { item, by_client }) => {
            if let (Some(item), Some(by_client)) = (item, by_client) {
                body["item"] = json!(item);
                body["located_by"] = json!(located_by(by_client));
                limits.push("the located user message has no text element".into());
            } else {
                limits.push("no user message in the turn's items".into());
            }
            "not found".to_owned()
        }
        Observation::Located(super::LocatedTurnText::Text {
            item,
            by_client,
            text,
        }) => match item {
            None => {
                limits.push("the located user message has no item identity; observation not attributable; read again later (SC-6)".into());
                "unreadable".to_owned()
            }
            Some(item) => {
                if !by_client {
                    limits.push("client id not matched; first user message of the turn used (clientId echo is an inference, U-WR-15)".into());
                }
                let comparison =
                    prepared.compare_observed_text(expected_text, expected_body, &text)?;
                limits.extend(comparison.evidence_limits);
                body["observed_text"] = comparison.observed_text;
                body["item"] = json!(item);
                body["located_by"] = json!(located_by(by_client));
                match comparison.state.as_str() {
                    "equal composed text" => "verified".to_owned(),
                    other => other.to_owned(),
                }
            }
        },
    };
    Ok(state)
}

/// Original immutable bytes remain with the owner across failed attempts.
#[derive(Debug)]
pub struct PendingRecord {
    project: (u64, u64),
    envelope: Value,
    bytes: Vec<u8>,
}
impl PendingRecord {
    fn new(
        project: &ProjectRecords,
        body: Value,
        basis: Vec<String>,
        sources: Vec<String>,
        writer: &str,
        observed_at: &str,
    ) -> Result<Self, String> {
        let envelope = json!({"version":1,"record_id":crate::util::opaque_id(PREFIX)?,"writer":writer,"observed_at":observed_at,"body":body,"basis_records":basis,"source_references":sources});
        validate(&envelope)?;
        let bytes = serde_json::to_vec(&envelope).map_err(|e| e.to_string())?;
        Ok(Self {
            project: project.identity,
            envelope,
            bytes,
        })
    }
    pub fn reference(&self) -> &str {
        self.envelope["record_id"].as_str().unwrap()
    }
    /// The owning native producer supplies its actual check; persistence adds no
    /// native authority. Schema-valid JSON is never sufficient for live send/check.
    pub(crate) fn supply_check(
        project: &ProjectRecords,
        completed: CompletedSupplyCheck,
        run_text: &ResolvedRecord,
        writer: &str,
    ) -> Result<Self, String> {
        let CompletedSupplyCheck { body, sources } = completed;
        if run_text.project != project.identity
            || run_text.body()["record_kind"] != "run_text"
            || body["record_kind"] != "supply_check"
        {
            return Err("check basis/project mismatch".into());
        }
        let observed = body["read_at"]
            .as_str()
            .ok_or("check read time absent")?
            .to_owned();
        Self::new(
            project,
            body,
            vec![run_text.reference().into()],
            sources,
            writer,
            &observed,
        )
    }
}
/// One live check's original pending record (WP-5: a retry preserves its
/// identity, bytes and read_at). Built only from a CompletedSupplyCheck.
#[derive(Debug)]
pub struct PendingSupplyCheck {
    record: PendingRecord,
    run_text: String,
}
/// Typed published-check token for the live R3 writer: no public constructor,
/// Deserialize or Clone. Only PendingSupplyCheck::publish creates it.
#[derive(Debug)]
pub struct PublishedSupplyCheck {
    run_text: ResolvedRecord,
    check: ResolvedRecord,
}
impl PendingSupplyCheck {
    pub(crate) fn new(
        project: &ProjectRecords,
        completed: CompletedSupplyCheck,
        published: &dyn PublishedText,
        writer: &str,
    ) -> Result<Self, String> {
        Ok(Self {
            record: PendingRecord::supply_check(
                project,
                completed,
                published.run_text_record(),
                writer,
            )?,
            run_text: published.run_text_record().reference().into(),
        })
    }
    pub fn reference(&self) -> &str {
        self.record.reference()
    }
    pub fn body(&self) -> &Value {
        &self.record.envelope["body"]
    }
    #[cfg(test)]
    pub fn bytes(&self) -> &[u8] {
        &self.record.bytes
    }
    /// Publishes the original bytes, then re-resolves the cited run_text in the
    /// same explicit project. Never re-reads native history or resends.
    pub fn publish(&self, project: &ProjectRecords) -> Result<PublishedSupplyCheck, String> {
        let check = project.publish(&self.record)?;
        let run_text = project
            .resolve(&self.run_text)
            .map_err(|e| format!("cited run_text: {e:?}"))?;
        Ok(PublishedSupplyCheck { run_text, check })
    }
}
impl PublishedSupplyCheck {
    pub fn run_text(&self) -> &ResolvedRecord {
        &self.run_text
    }
    pub fn check(&self) -> &ResolvedRecord {
        &self.check
    }
}
/// Owns the original typed prepared text; a cold read cannot construct this.
#[derive(Debug)]
pub struct PreparedRunPublication {
    prepared: PreparedRunText,
    selection: PendingRecord,
    text: PendingRecord,
}
#[derive(Debug)]
pub struct PublishedRunText {
    prepared: PreparedRunText,
    selection: ResolvedRecord,
    text: ResolvedRecord,
}
impl PreparedRunPublication {
    pub fn new(
        project: &ProjectRecords,
        selection: &Selection,
        prepared: PreparedRunText,
        writer: &str,
        selected_at: &str,
        prepared_at: &str,
    ) -> Result<Self, String> {
        if !matches!(
            selection.admission(),
            SelectionAdmission::RegisteredRevision
        ) || selection.identity() != &prepared.workflow
            || selection.admission() != prepared.admission()
        {
            return Err("registered typed selection required; development evidence cannot become registered".into());
        }
        selection.verify_store(&prepared.scope.revision_store)?;
        if prepared.record["text_identity"] != super::exact_text_identity(prepared.text())
            || prepared.record["text_bytes"] != prepared.text().len()
        {
            return Err("prepared text changed".into());
        }
        let body = json!({"record_kind":"selection_record","selection_id":prepared.scope.selection_ref,"identity":selection.identity(),"holding_library":prepared.scope.holding_library,"standing":"registered","selected_by":"the person (App interface)","how":"explicit","conversation":prepared.scope.conversation,"selected_at":selected_at});
        // WR PR-4: a confirmed agent proposal is recorded as such, citing the proposal.
        let mut body = body;
        if let Some(proposal) = prepared.proposal() {
            body["how"] = json!("agent proposal confirmed by the person");
            body["proposal"] = proposal.clone();
        }
        // SL-7: a selection for a chained run records prior_run as a relation, from
        // the same owner end the chain line was composed from (CH-2).
        if let Some(chain) = prepared.record["chain"].as_object() {
            body["prior_run"] = json!({"run":chain["prior_run"],"workflow":chain["prior_workflow"],"ended":chain["ended"]});
        }
        let selection = PendingRecord::new(project, body, vec![], vec![], writer, selected_at)?;
        let text = PendingRecord::new(
            project,
            prepared.record.clone(),
            vec![selection.reference().into()],
            vec![],
            writer,
            prepared_at,
        )?;
        Ok(Self {
            prepared,
            selection,
            text,
        })
    }
    pub fn prepared(&self) -> &PreparedRunText {
        &self.prepared
    }
    pub fn selection_reference(&self) -> &str {
        self.selection.reference()
    }
    pub fn run_text_reference(&self) -> &str {
        self.text.reference()
    }
    /// On error ownership stays here for an original-byte retry. Success consumes
    /// no native send: Root's separate dispatch owner decides that transition.
    pub fn publish(&self, project: &ProjectRecords) -> Result<PublishedRunText, String> {
        let snapshot = super::Snapshot::capture(&self.prepared.scope.revision_store)?;
        if snapshot.revision != self.prepared.workflow.revision
            || super::exact_text_identity(snapshot.workflow_text())
                != self.prepared.record["workflow_file"]["content"]
        {
            return Err("linked workflow revision no longer resolves exactly".into());
        }
        let selection = project.publish(&self.selection)?;
        let text = project.publish(&self.text)?;
        Ok(PublishedRunText {
            prepared: self.prepared.clone(),
            selection,
            text,
        })
    }
}
impl PublishedRunText {
    pub fn prepared(&self) -> &PreparedRunText {
        &self.prepared
    }
    pub fn run_text_record(&self) -> &ResolvedRecord {
        &self.text
    }
    pub fn selection_record(&self) -> &ResolvedRecord {
        &self.selection
    }
}
#[cfg(test)]
#[path = "workflow_record_store_tests.rs"]
mod tests;

#[cfg(test)]
thread_local! { pub(crate) static FAIL_AFTER_LINK: std::cell::Cell<bool> = const { std::cell::Cell::new(false) }; }
fn publication_boundary() -> Result<(), String> {
    #[cfg(test)]
    if FAIL_AFTER_LINK.with(|v| v.replace(false)) {
        return Err("injected uncertainty after no-replace link".into());
    }
    Ok(())
}
/// Typed owner callback remains required for end-notice preparation; cold evidence
/// does not create a lifecycle event or a new sendable notice.
#[derive(Debug)]
pub struct PreparedEndPublication {
    text: String,
    notice: PreparedRunText,
    record: PendingRecord,
}
#[derive(Debug)]
pub struct PublishedEndNotice {
    text: String,
    notice: PreparedRunText,
    record: ResolvedRecord,
}
impl PreparedEndPublication {
    pub fn new(
        project: &ProjectRecords,
        prepared: &PreparedRunText,
        end: &super::OwnerRunEnd,
        original_start: &ResolvedRecord,
        writer: &str,
        observed_at: &str,
    ) -> Result<Self, String> {
        Self::for_turn(
            project,
            prepared,
            end,
            original_start,
            writer,
            observed_at,
            &prepared.scope.generation,
        )
    }
    /// As `new`, with the notice scoped to the current generation of the same
    /// home, for the person's next ordinary turn (TX-5).
    pub fn for_turn(
        project: &ProjectRecords,
        prepared: &PreparedRunText,
        end: &super::OwnerRunEnd,
        original_start: &ResolvedRecord,
        writer: &str,
        observed_at: &str,
        current_generation: &Value,
    ) -> Result<Self, String> {
        let notice = prepared.notice_turn(end, current_generation)?;
        let (text, body) = (notice.text().to_owned(), notice.record().clone());
        if original_start.project != project.identity {
            return Err("original start belongs to another project".into());
        }
        let original = project
            .resolve(original_start.reference())
            .map_err(|e| format!("original start: {e:?}"))?;
        if original.body() != prepared.record() || original.body()["purpose"] != "run start" {
            return Err("original start does not identify this prepared run".into());
        }
        let record = PendingRecord::new(
            project,
            body,
            vec![original.reference().into()],
            vec![],
            writer,
            observed_at,
        )?;
        Ok(Self {
            text,
            notice,
            record,
        })
    }
    pub fn reference(&self) -> &str {
        self.record.reference()
    }
    pub fn publish(&self, project: &ProjectRecords) -> Result<PublishedEndNotice, String> {
        Ok(PublishedEndNotice {
            text: self.text.clone(),
            notice: self.notice.clone(),
            record: project.publish(&self.record)?,
        })
    }
}
impl PublishedEndNotice {
    pub fn text(&self) -> &str {
        &self.text
    }
    pub fn run_text_record(&self) -> &ResolvedRecord {
        &self.record
    }
}
