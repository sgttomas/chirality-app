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
/// No production constructor yet: Root must mint at the genuine native
/// comparison boundary. Neither a coverage seal alone nor JSON can mint this.
#[derive(Debug)]
pub struct CompletedSupplyCheck {
    body: Value,
    sources: Vec<String>,
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
thread_local! { static FAIL_AFTER_LINK: std::cell::Cell<bool> = const { std::cell::Cell::new(false) }; }
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
    record: PendingRecord,
}
#[derive(Debug)]
pub struct PublishedEndNotice {
    text: String,
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
        let (text, body) = prepared.end_notice(end)?;
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
        Ok(Self { text, record })
    }
    pub fn publish(&self, project: &ProjectRecords) -> Result<PublishedEndNotice, String> {
        Ok(PublishedEndNotice {
            text: self.text.clone(),
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
