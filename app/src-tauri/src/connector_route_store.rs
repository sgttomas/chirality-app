//! CRP-v0.3 bounded caller-account persistence. No source recovery, truth/custody
//! verification, duty performance, authority, UI or provider adoption is implied.
//! Handles constrain which directories receive writes, not their mutable location.
//! Even matching pre/post observations cannot exclude a transient external rename.
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    path::{Path, PathBuf},
    sync::OnceLock,
};

pub const DIRECTORY: &str = ".chirality/records/connectors/route-accounts";
const PARTS: &[&str] = &[".chirality", "records", "connectors", "route-accounts"];
const IDS: &[&str] = &[
    "urn:chirality:app-v4:del-07-02:route-account:0.1",
    "urn:chirality:app-v4:del-07-02:route-account:0.2",
    "urn:chirality:app-v4:del-07-02:route-account:0.3",
    "urn:chirality:app-v4:del-07-02:route-account:0.4",
];
const RESOURCES: &[(&str, &str)] = &[
    (
        "connector.route-account.v0.4.schema.json",
        include_str!("../resources/connector_route/connector.route-account.v0.4.schema.json"),
    ),
    (
        "connector.route-account.v0.3.schema.json",
        include_str!("../resources/connector_route/connector.route-account.v0.3.schema.json"),
    ),
    (
        "connector.route-account.schema.json",
        include_str!("../resources/connector_route/connector.route-account.schema.json"),
    ),
    (
        "connector.route-account.v0.2.schema.json",
        include_str!("../resources/connector_route/connector.route-account.v0.2.schema.json"),
    ),
    (
        "connector.standing.schema.json",
        include_str!("../resources/connector_route/connector.standing.schema.json"),
    ),
];

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FileIdentity {
    pub device: u64,
    pub inode: u64,
}
/// Complete binding; a bare account ID is insufficient. Filesystem observations
/// permit relocation of the same project, not silent adoption of copied records.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundReference {
    pub relative_path: String,
    pub account_id: String,
    pub format_version: String,
    pub sha256: String,
    /// Root followed by each directory ancestor, in traversal order.
    pub directories: Vec<FileIdentity>,
    pub file: FileIdentity,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FinalObservation {
    /// observed, absent, or unreadable; never a successful-commit assertion.
    pub state: String,
    pub file: Option<FileIdentity>,
    pub file_type: Option<String>,
    pub sha256: Option<String>,
    pub account_id: Option<String>,
    pub format_version: Option<String>,
    pub detail: Option<String>,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Attempt {
    pub resolved_project: PathBuf,
    pub temporary_relative_path: String,
    pub observed_final: Option<FinalObservation>,
    pub relative_path: String,
    pub account_id: String,
    pub format_version: String,
    pub sha256: String,
    pub directories: Vec<FileIdentity>,
    pub file: Option<FileIdentity>,
}
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ErrorKind {
    UnsupportedPlatform,
    UnsupportedCapability,
    InvalidInput,
    UnsupportedFormat,
    UnsupportedSubset,
    UnresolvedReference,
    InvalidAccount,
    Io,
    Missing,
    Collision,
    UnsafeEntry,
    LocationMismatch,
    ChangedContent,
    DuplicateIdentity,
    TemporaryLeftover,
    InvalidName,
    IncompleteDiscovery,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoreError {
    pub kind: ErrorKind,
    pub detail: String,
    /// True means bytes may be published. Never retry or relocate implicitly.
    pub uncertain_commit: bool,
    pub attempt: Option<Attempt>,
    /// Known temporary name requiring reconciliation; it can have been moved or
    /// substituted externally. Never an account, and never automatically unlinked.
    pub temporary_leftover: Option<String>,
}
impl StoreError {
    fn new(kind: ErrorKind, detail: impl Into<String>) -> Self {
        Self {
            kind,
            detail: detail.into(),
            uncertain_commit: false,
            attempt: None,
            temporary_leftover: None,
        }
    }
}
impl std::fmt::Display for StoreError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}: {}", self.kind, self.detail)
    }
}
impl std::error::Error for StoreError {}
type Result<T> = std::result::Result<T, StoreError>;

/// Declared 0.1/0.2 retain shape validation;0.3 also checks draft internal consistency.
/// No network/schema fallback; no cross-reference truth or performed-duty claim.
pub fn validate_account(account: &Value) -> Result<()> {
    let index = match (
        account["format"].as_str(),
        account["formatVersion"].as_str(),
    ) {
        (Some("chirality.connector.route-account"), Some("0.1")) => 0,
        (Some("chirality.connector.route-account"), Some("0.2")) => 1,
        (Some("chirality.connector.route-account"), Some("0.3")) => 2,
        (Some("chirality.connector.route-account"), Some("0.4")) => 3,
        _ => {
            return Err(StoreError::new(
                ErrorKind::UnsupportedFormat,
                "unsupported or missing declared format/version",
            ))
        }
    };
    static VALIDATORS: OnceLock<std::result::Result<Vec<jsonschema::Validator>, String>> =
        OnceLock::new();
    let validators = VALIDATORS
        .get_or_init(|| crate::schema_validation::compile_targets(RESOURCES, IDS, IDS))
        .as_ref()
        .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e.clone()))?;
    validators[index]
        .validate(account)
        .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e.to_string()))?;
    if index == 2 {
        crate::connector_materialization::validate_cold(account)
            .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e))?;
    }
    if index == 3 {
        crate::connector_reconstruction::validate_cold(account)
            .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e))?;
    }
    Ok(())
}
/// A cold observation of claimed file content. Its binding does not establish
/// that this store or any recorder successfully published the file.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ObservedAccount {
    pub reference: BoundReference,
    pub account: Value,
    #[serde(skip)]
    pub(crate) byte_length: usize,
    #[serde(skip)]
    pub(crate) answer_only: Option<Value>,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DiscoveryIssue {
    pub relative_path: String,
    pub kind: ErrorKind,
    pub detail: String,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Discovery {
    pub resolved_project: PathBuf,
    pub accounts: Vec<ObservedAccount>,
    /// All matching paths are retained; duplicates have no selected winner.
    pub by_account_id: BTreeMap<String, Vec<String>>,
    pub issues: Vec<DiscoveryIssue>,
    pub directory_absent: bool,
    pub enumeration_complete: bool,
}
fn canonical_name(name: &str) -> bool {
    let Some(key) = name.strip_suffix(".json") else {
        return false;
    };
    uuid::Uuid::parse_str(key).is_ok_and(|u| {
        u.to_string() == key
            && u.get_version_num() == 4
            && u.get_variant() == uuid::Variant::RFC4122
    })
}
fn relative_parts(path: &str) -> Result<Vec<&str>> {
    let parts: Vec<_> = path.split('/').collect();
    if parts.is_empty()
        || parts
            .iter()
            .any(|p| p.is_empty() || *p == "." || *p == ".." || p.contains(['\\', ':', '\0']))
    {
        return Err(StoreError::new(
            ErrorKind::InvalidInput,
            "expected normal project-relative components",
        ));
    }
    Ok(parts)
}

#[cfg(any(target_os = "macos", target_os = "linux"))]
mod platform {
    use super::*;
    use std::{
        ffi::{CStr, CString, OsStr},
        fs::{File, OpenOptions},
        io::{Read, Write},
        os::{
            fd::{AsRawFd, FromRawFd},
            unix::{
                ffi::OsStrExt,
                fs::{MetadataExt, OpenOptionsExt},
            },
        },
    };

    #[cfg(test)] thread_local!{static INSPECTION_AUDIT:std::cell::RefCell<Option<Vec<String>>>=const{std::cell::RefCell::new(None)};}
    #[cfg(test)] pub(super) fn audit_inspection<T>(f:impl FnOnce()->T)->(T,Vec<String>){INSPECTION_AUDIT.with(|a|*a.borrow_mut()=Some(Vec::new()));let value=f();let audit=INSPECTION_AUDIT.with(|a|a.borrow_mut().take().unwrap());(value,audit)}
    fn ioerr(context: &str, e: std::io::Error) -> StoreError {
        let kind = match e.raw_os_error() {
            Some(libc::ENOENT) => ErrorKind::Missing,
            Some(libc::EEXIST) => ErrorKind::Collision,
            Some(libc::ELOOP) | Some(libc::ENOTDIR) => ErrorKind::UnsafeEntry,
            _ => ErrorKind::Io,
        };
        StoreError::new(kind, format!("{context}: {e}"))
    }
    fn identity(file: &File) -> Result<FileIdentity> {
        let m = file.metadata().map_err(|e| ioerr("metadata", e))?;
        Ok(FileIdentity {
            device: m.dev(),
            inode: m.ino(),
        })
    }
    fn open_at(parent: &File, name: &OsStr, flags: i32) -> Result<File> {
        #[cfg(test)] INSPECTION_AUDIT.with(|a|{if let Some(v)=a.borrow_mut().as_mut(){v.push(format!("open:{}",name.to_string_lossy()));}});
        let name = CString::new(name.as_bytes())
            .map_err(|_| StoreError::new(ErrorKind::InvalidInput, "NUL in component"))?;
        // SAFETY: valid parent descriptor and NUL-terminated single component;
        // owned descriptor transferred to File exactly once on success.
        let fd = unsafe {
            libc::openat(
                parent.as_raw_fd(),
                name.as_ptr(),
                flags | libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK,
                0o600,
            )
        };
        if fd < 0 {
            Err(ioerr(
                "open relative entry",
                std::io::Error::last_os_error(),
            ))
        } else {
            Ok(unsafe { File::from_raw_fd(fd) })
        }
    }
    fn open_path(path: &Path) -> Result<File> {
        OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC)
            .open(path)
            .map_err(|e| ioerr("open resolved project", e))
    }
    fn sync(file: &File, context: &str) -> Result<()> {
        file.sync_all().map_err(|e| ioerr(context, e))
    }
    fn child(parent: &File, name: &str, create: bool) -> Result<File> {
        if create {
            let n = CString::new(name).unwrap();
            let rc = unsafe { libc::mkdirat(parent.as_raw_fd(), n.as_ptr(), 0o700) };
            if rc < 0 {
                let e = std::io::Error::last_os_error();
                if e.raw_os_error() != Some(libc::EEXIST) {
                    return Err(ioerr(name, e));
                }
            }
        }
        let dir = open_at(parent, OsStr::new(name), libc::O_RDONLY | libc::O_DIRECTORY)?;
        if create {
            // Includes concurrently created ancestors: success requires their
            // entries and contents to have completed the durability steps.
            sync(&dir, "sync child directory")?;
            sync(parent, "sync parent directory")?;
        }
        Ok(dir)
    }
    fn publish(dir: &File, temporary: &str, target: &str) -> std::io::Result<()> {
        let from = CString::new(temporary).unwrap();
        let to = CString::new(target).unwrap();
        // Atomic destination exclusion, but source is still a mutable name.
        // Never substitute replacing rename or link-plus-unlink on failure.
        #[cfg(target_os = "macos")]
        let rc = unsafe {
            libc::renameatx_np(
                dir.as_raw_fd(),
                from.as_ptr(),
                dir.as_raw_fd(),
                to.as_ptr(),
                libc::RENAME_EXCL,
            )
        };
        #[cfg(target_os = "linux")]
        let rc = unsafe {
            libc::renameat2(
                dir.as_raw_fd(),
                from.as_ptr(),
                dir.as_raw_fd(),
                to.as_ptr(),
                libc::RENAME_NOREPLACE,
            )
        };
        if rc == 0 {
            Ok(())
        } else {
            Err(std::io::Error::last_os_error())
        }
    }
    fn observe_final(dir: &File, name: &str) -> FinalObservation {
        let mut observation = FinalObservation {
            state: "unreadable".into(),
            file: None,
            file_type: None,
            sha256: None,
            account_id: None,
            format_version: None,
            detail: None,
        };
        let result = (|| -> Result<()> {
            let mut file = open_at(dir, OsStr::new(name), libc::O_RDONLY)?;
            observation.file = Some(identity(&file)?);
            let metadata = file
                .metadata()
                .map_err(|e| ioerr("observe final metadata", e))?;
            observation.file_type = Some(
                if metadata.is_file() {
                    "regular"
                } else {
                    "nonregular"
                }
                .into(),
            );
            if !metadata.is_file() {
                observation.state = "observed".into();
                return Ok(());
            }
            let mut bytes = Vec::new();
            file.read_to_end(&mut bytes)
                .map_err(|e| ioerr("observe final bytes", e))?;
            observation.sha256 = Some(crate::util::sha256_hex(&bytes));
            if let Ok(value) = serde_json::from_slice::<Value>(&bytes) {
                observation.account_id = value["account_id"].as_str().map(str::to_owned);
                observation.format_version = value["formatVersion"].as_str().map(str::to_owned);
            }
            observation.state = "observed".into();
            observation.detail = Some(
                "read-only observed buffer, not a stable snapshot or successful commit".into(),
            );
            Ok(())
        })();
        if let Err(e) = result {
            observation.state = if e.kind == ErrorKind::Missing {
                "absent"
            } else {
                "unreadable"
            }
            .into();
            observation.detail = Some(e.to_string());
        }
        observation
    }
    fn read_account(
        dir: &File,
        name: &str,
        path: &str,
        dirs: Vec<FileIdentity>,
    ) -> Result<ObservedAccount> {
        read_account_mode(dir, name, path, dirs, None, || {})
    }
    pub(super) fn read_account_mode(
        dir: &File,
        name: &str,
        path: &str,
        dirs: Vec<FileIdentity>,
        known: Option<&str>,
        before_read: impl FnOnce(),
    ) -> Result<ObservedAccount> {
        let mut file = open_at(dir, OsStr::new(name), libc::O_RDONLY)?;
        let before = file.metadata().map_err(|e| ioerr("account metadata", e))?;
        if !before.is_file() || before.nlink() != 1 {
            return Err(StoreError::new(
                ErrorKind::UnsafeEntry,
                "account must be regular and not hard-linked",
            ));
        }
        before_read();
        let bytes = if known.is_some() {
            crate::connector_answer_only::bounded_read(&mut file)
                .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e))?
        } else {
            let mut bytes = Vec::new();
            file.read_to_end(&mut bytes)
                .map_err(|e| ioerr("read account", e))?;
            bytes
        };
        let after = file
            .metadata()
            .map_err(|e| ioerr("account post-read metadata", e))?;
        let current = open_at(dir, OsStr::new(name), libc::O_RDONLY)?;
        if before.dev() != after.dev()
            || before.ino() != after.ino()
            || before.len() != after.len()
            || before.mtime() != after.mtime()
            || before.mtime_nsec() != after.mtime_nsec()
            || before.ctime() != after.ctime()
            || before.ctime_nsec() != after.ctime_nsec()
            || identity(&current)? != identity(&file)?
            || after.nlink() != 1
        {
            return Err(StoreError::new(
                ErrorKind::ChangedContent,
                "account changed during read",
            ));
        }
        let mut account: Value = serde_json::from_slice(&bytes).map_err(|e| {
            StoreError::new(ErrorKind::InvalidAccount, format!("malformed account: {e}"))
        })?;
        if let Some(version) = known {
            if account["formatVersion"] != version {
                return Err(StoreError::new(
                    ErrorKind::ChangedContent,
                    "known reference version changed; no wider fallback",
                ));
            }
        }
        let is_answer = account["formatVersion"] == "0.5";
        if matches!(
            account["formatVersion"].as_str(),
            Some("0.3" | "0.4" | "0.5")
        ) && bytes.len() > crate::connector_answer_only::LIMIT
        {
            return Err(StoreError::new(ErrorKind::InvalidAccount,"Identified format0.3/0.4/0.5 exceeds1MiB original bytes; acquisition already occurred"));
        }
        if is_answer || known == Some("0.4") {
            account = crate::connector_answer_only::parse(&bytes)
                .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e))?;
        }
        let answer_only = if is_answer {
            crate::connector_answer_only::shape(&account)
                .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e))?;
            if !crate::connector_answer_only::selected(&account) {
                return Err(StoreError::new(ErrorKind::UnsupportedSubset,"Recognized format0.5 outside ANSWER-ONLY subset: review, plan, integration and integration_attempt must be null"));
            }
            Some(
                json!({"rawAccountText":String::from_utf8(bytes.clone()).map_err(|e|StoreError::new(ErrorKind::InvalidAccount,e.to_string()))?}),
            )
        } else {
            validate_account(&account)?;
            None
        };
        Ok(ObservedAccount {
            reference: BoundReference {
                relative_path: path.to_owned(),
                account_id: account["account_id"].as_str().unwrap().to_owned(),
                format_version: account["formatVersion"].as_str().unwrap().to_owned(),
                sha256: crate::util::sha256_hex(&bytes),
                directories: dirs,
                file: identity(&file)?,
            },
            account,
            byte_length: bytes.len(),
            answer_only,
        })
    }
    struct Chain {
        handles: Vec<File>,
        ids: Vec<FileIdentity>,
    }
    impl Chain {
        fn last(&self) -> &File {
            self.handles.last().unwrap()
        }
    }
    /// Explicit project capability. Absolute project spelling is resolved once;
    /// no operation consults cwd. Descendants are always opened no-follow.
    #[derive(Debug)]
    pub struct ProjectRouteStore {
        root: PathBuf,
        directory: File,
        root_identity: FileIdentity,
    }
    #[derive(Clone, Copy, Debug, PartialEq, Eq)]
    pub(super) enum Stage {
        BeforeWrite,
        TempSynced,
        TempChecked,
        Published,
        Verified,
    }
    #[derive(Clone, Copy, Debug, PartialEq, Eq)]
    pub(crate) enum InspectionStep {
        BeforeRead,
        AfterRead,
        BeforePostcheck,
    }
    fn inspection_failure(e: StoreError) -> Value {
        let status = match e.kind {
            ErrorKind::Missing => "missing",
            ErrorKind::UnsafeEntry | ErrorKind::InvalidInput => "unsafe",
            ErrorKind::ChangedContent
            | ErrorKind::LocationMismatch
            | ErrorKind::InvalidAccount
            | ErrorKind::UnsupportedFormat => "changed",
            _ => "unavailable",
        };
        json!({"status":status,"detail":e.detail.chars().take(512).collect::<String>(),"limit":"Direct exact-file observation only; namespace uniqueness not checked; original publication outcome unchanged"})
    }
    impl ProjectRouteStore {
        pub fn open(explicit_project: &Path) -> Result<Self> {
            if !explicit_project.is_absolute()
                || explicit_project
                    .components()
                    .any(|p| matches!(p, std::path::Component::ParentDir))
            {
                return Err(StoreError::new(
                    ErrorKind::InvalidInput,
                    "explicit absolute project required; parent traversal refused",
                ));
            }
            let root = explicit_project
                .canonicalize()
                .map_err(|e| ioerr("resolve explicit project", e))?;
            let directory = open_path(&root)?;
            let root_identity = identity(&directory)?;
            let store = Self {
                root,
                directory,
                root_identity,
            };
            store.check_root()?;
            Ok(store)
        }
        pub(crate) fn project_identity(&self) -> FileIdentity {
            self.root_identity.clone()
        }
        pub fn resolved_project(&self) -> &Path {
            &self.root
        }
        fn check_root(&self) -> Result<()> {
            let current = open_path(&self.root).map_err(|e| {
                StoreError::new(
                    ErrorKind::LocationMismatch,
                    format!("project path comparison unavailable: {e}"),
                )
            })?;
            if identity(&current)? != self.root_identity {
                return Err(StoreError::new(ErrorKind::LocationMismatch, "opened project identity no longer at resolved path; caller reconciliation required"));
            }
            Ok(())
        }
        fn chain(&self, parts: &[&str], create: bool) -> Result<Chain> {
            let mut handles = vec![self
                .directory
                .try_clone()
                .map_err(|e| ioerr("duplicate project handle", e))?];
            let mut ids = vec![self.root_identity.clone()];
            for part in parts {
                let dir = child(handles.last().unwrap(), part, create)?;
                ids.push(identity(&dir)?);
                handles.push(dir);
            }
            Ok(Chain { handles, ids })
        }
        fn compare(&self, parts: &[&str], expected: &[FileIdentity]) -> Result<()> {
            self.check_root()?;
            let actual = self.chain(parts, false).map_err(|e| {
                StoreError::new(
                    ErrorKind::LocationMismatch,
                    format!("canonical ancestor comparison unavailable: {e}"),
                )
            })?;
            if actual.ids != expected {
                return Err(StoreError::new(
                    ErrorKind::LocationMismatch,
                    "canonical directory identities changed; caller reconciliation required",
                ));
            }
            Ok(())
        }
        fn inspection_chain(&self, expected: &[FileIdentity]) -> Result<Chain> {
            let mut handles = vec![self
                .directory
                .try_clone()
                .map_err(|e| ioerr("duplicate inspection root", e))?];
            let mut ids = vec![self.root_identity.clone()];
            for (index, part) in PARTS.iter().enumerate() {
                let dir = child(handles.last().unwrap(), part, false)?;
                let id = identity(&dir)?;
                if expected.get(index + 1) != Some(&id) {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "Original directory identity changed",
                    ));
                }
                ids.push(id);
                handles.push(dir);
            }
            Ok(Chain { handles, ids })
        }
        #[cfg(test)]
        pub(crate) fn retained_size(&self) -> usize {
            std::mem::size_of::<Self>() + self.root.capacity()
        }
        /// A direct, bounded comparison, deliberately not full unique reference resolution.
        pub(crate) fn inspect_published(&self, reference: &BoundReference, project: &Path) -> Value {
            self.inspect_published_with(reference, project, |_| Ok(()))
        }
        pub(super) fn inspect_published_with(
            &self,
            reference: &BoundReference,
            project: &Path,
            mut hook: impl FnMut(InspectionStep) -> std::io::Result<()>,
        ) -> Value {
            let run = (|| -> Result<Value> {
                if !matches!(reference.format_version.as_str(), "0.3" | "0.4") {
                    return Err(StoreError::new(
                        ErrorKind::UnsupportedCapability,
                        "Direct published inspection supports only known0.3/0.4",
                    ));
                }
                let parts = relative_parts(&reference.relative_path)?;
                let (name, ancestors) = parts.split_last().unwrap();
                if ancestors != PARTS
                    || !canonical_name(name)
                    || reference.directories.len() != PARTS.len() + 1
                    || reference.directories.first() != Some(&self.root_identity)
                {
                    return Err(StoreError::new(
                        ErrorKind::InvalidInput,
                        "Original canonical path/root binding required",
                    ));
                }
                let check_project = || -> Result<()> {
                    // Keep original errors, unlike the legacy compare wrapper.
                    let current = open_path(&self.root)?;
                    if identity(&current)? != self.root_identity {
                        return Err(StoreError::new(
                            ErrorKind::ChangedContent,
                            "Original project root was replaced",
                        ));
                    }
                    let resolved = project
                        .canonicalize()
                        .map_err(|e| ioerr("current explicit project", e))?;
                    if resolved != self.root {
                        return Err(StoreError::new(
                            ErrorKind::ChangedContent,
                            "Current project association differs from original store",
                        ));
                    }
                    Ok(())
                };
                check_project()?;
                let chain = self.inspection_chain(&reference.directories)?;
                if chain.ids != reference.directories {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "Original directory identities changed",
                    ));
                }
                let mut file = open_at(chain.last(), OsStr::new(name), libc::O_RDONLY)?;
                let before = file
                    .metadata()
                    .map_err(|e| ioerr("inspection metadata", e))?;
                if !before.is_file() || before.nlink() != 1 {
                    return Err(StoreError::new(
                        ErrorKind::UnsafeEntry,
                        "Inspection target must be regular and single-link",
                    ));
                }
                if identity(&file)? != reference.file {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "Original file identity changed",
                    ));
                }
                hook(InspectionStep::BeforeRead).map_err(|e| ioerr("inspection read", e))?;
                let mut bytes = Vec::new();
                (&mut file)
                    .take((crate::connector_materialization::BYTE_LIMIT + 1) as u64)
                    .read_to_end(&mut bytes)
                    .map_err(|e| ioerr("bounded inspection read", e))?;
                if bytes.len() > crate::connector_materialization::BYTE_LIMIT {
                    return Err(StoreError::new(
                        ErrorKind::UnsupportedCapability,
                        "Exact-file inspection exceeded1MiB sentinel; no wider read",
                    ));
                }
                #[cfg(test)]
                INSPECTION_AUDIT.with(|a| {
                    if let Some(v) = a.borrow_mut().as_mut() {
                        v.push(format!(
                            "raw-bytes:{};raw-capacity:{}",
                            bytes.len(),
                            bytes.capacity()
                        ));
                    }
                });
                hook(InspectionStep::AfterRead).map_err(|e| ioerr("inspection readback", e))?;
                let digest = crate::util::sha256_hex(&bytes);
                if digest != reference.sha256 {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "Original raw account hash changed",
                    ));
                }
                let account = crate::connector_answer_only::parse(&bytes).map_err(|_| {
                    StoreError::new(
                        ErrorKind::InvalidAccount,
                        "Strict JSON/UTF8/depth validation failed",
                    )
                })?;
                if account["formatVersion"] != reference.format_version
                    || account["account_id"] != reference.account_id
                {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "Original account ID/version changed",
                    ));
                }
                validate_account(&account).map_err(|_| {
                    StoreError::new(
                        ErrorKind::InvalidAccount,
                        "Owning account semantic/schema validation failed",
                    )
                })?;
                // No parsed content is retained or returned by this method.
                drop(account);
                let byte_length = bytes.len();
                drop(bytes);
                hook(InspectionStep::BeforePostcheck).map_err(|e| ioerr("inspection postcheck", e))?;
                let after = file
                    .metadata()
                    .map_err(|e| ioerr("inspection post-read metadata", e))?;
                if !after.is_file() || after.nlink() != 1 {
                    return Err(StoreError::new(
                        ErrorKind::UnsafeEntry,
                        "Inspection target no longer regular/single-link",
                    ));
                }
                if before.len() != after.len()
                    || before.mtime() != after.mtime()
                    || before.mtime_nsec() != after.mtime_nsec()
                    || before.ctime() != after.ctime()
                    || before.ctime_nsec() != after.ctime_nsec()
                {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "Account metadata changed during inspection",
                    ));
                }
                {
                    let named = open_at(chain.last(), OsStr::new(name), libc::O_RDONLY)?;
                    let m = named
                        .metadata()
                        .map_err(|e| ioerr("reopened inspection metadata", e))?;
                    if !m.is_file() || m.nlink() != 1 {
                        return Err(StoreError::new(
                            ErrorKind::UnsafeEntry,
                            "Reopened inspection target unsafe",
                        ));
                    }
                    if identity(&named)? != reference.file {
                        return Err(StoreError::new(
                            ErrorKind::ChangedContent,
                            "Named account replaced during inspection",
                        ));
                    }
                }
                check_project()?;
                let after_chain = self.inspection_chain(&reference.directories)?;
                if after_chain.ids != chain.ids {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "Directory chain changed during inspection",
                    ));
                }
                Ok(
                    json!({"status":"current_match","observed":{"accountId":reference.account_id,"formatVersion":reference.format_version,"sha256":digest,"byteLength":byte_length,"fileIdentity":{"device":reference.file.device.to_string(),"inode":reference.file.inode.to_string()}},"limit":"Direct exact-file observation only; namespace uniqueness not checked; no continuous pathname guarantee, source truth, duty or new publication proof"}),
                )
            })();
            run.unwrap_or_else(inspection_failure)
        }
        /// One explicit attempt; a collision or uncertain outcome is never retried.
        #[cfg(test)]
        pub(crate) fn test_write_uncertain(&self, account: &Value) -> Result<BoundReference> {
            let key = crate::util::opaque_id("").map_err(|e| StoreError::new(ErrorKind::Io, e))?;
            self.write_inner(account, &key, |stage| {
                if matches!(stage, Stage::Published) {
                    Err(StoreError::new(
                        ErrorKind::Io,
                        "injected post-publication failure",
                    ))
                } else {
                    Ok(())
                }
            })
        }
        pub fn write(&self, account: &Value) -> Result<BoundReference> {
            validate_account(account)?;
            let key = crate::util::opaque_id("").map_err(|e| StoreError::new(ErrorKind::Io, e))?;
            self.write_inner(account, &key, |_| Ok(()))
        }
        pub(super) fn write_inner(
            &self,
            account: &Value,
            key: &str,
            hook: impl FnMut(Stage) -> Result<()>,
        ) -> Result<BoundReference> {
            self.write_using(account, key, hook, publish)
        }
        pub(super) fn write_using(
            &self,
            account: &Value,
            key: &str,
            mut hook: impl FnMut(Stage) -> Result<()>,
            publisher: impl FnOnce(&File, &str, &str) -> std::io::Result<()>,
        ) -> Result<BoundReference> {
            validate_account(account)?;
            let name = format!("{key}.json");
            if !canonical_name(&name) {
                return Err(StoreError::new(
                    ErrorKind::InvalidInput,
                    "invalid UUID v4 storage identity",
                ));
            }
            let bytes = serde_json::to_vec(account)
                .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e.to_string()))?;
            self.check_root()?;
            let chain = self.chain(PARTS, true)?;
            let temporary = format!(
                ".route-{}.tmp",
                crate::util::opaque_id("").map_err(|e| StoreError::new(ErrorKind::Io, e))?
            );
            let mut attempt = Attempt {
                resolved_project: self.root.clone(),
                temporary_relative_path: format!("{DIRECTORY}/{temporary}"),
                observed_final: None,
                relative_path: format!("{DIRECTORY}/{name}"),
                account_id: account["account_id"].as_str().unwrap().to_owned(),
                format_version: account["formatVersion"].as_str().unwrap().to_owned(),
                sha256: crate::util::sha256_hex(&bytes),
                directories: chain.ids.clone(),
                file: None,
            };
            let mut temp_created = false;
            let mut published = false;
            let operation = (|| {
                hook(Stage::BeforeWrite)?;
                self.compare(PARTS, &chain.ids)?;
                let mut file = open_at(
                    chain.last(),
                    OsStr::new(&temporary),
                    libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL,
                )?;
                temp_created = true;
                attempt.file = Some(identity(&file)?);
                file.write_all(&bytes)
                    .map_err(|e| ioerr("write temporary account", e))?;
                file.flush()
                    .map_err(|e| ioerr("flush temporary account", e))?;
                sync(&file, "sync temporary account")?;
                // macOS full sync asks the device to flush its write cache too.
                #[cfg(target_os = "macos")]
                if unsafe { libc::fcntl(file.as_raw_fd(), libc::F_FULLFSYNC) } < 0 {
                    return Err(ioerr(
                        "full sync temporary account",
                        std::io::Error::last_os_error(),
                    ));
                }
                hook(Stage::TempSynced)?;
                // Exclusive rename resolves a name, not the retained descriptor.
                // Refuse observed inode/content substitution before publication;
                // a later concurrent name change remains a platform residual.
                let temporary_observation =
                    read_account(chain.last(), &temporary, &temporary, chain.ids.clone())?;
                if Some(&temporary_observation.reference.file) != attempt.file.as_ref()
                    || temporary_observation.reference.sha256 != attempt.sha256
                {
                    return Err(StoreError::new(ErrorKind::ChangedContent,
                        "temporary identity/hash changed before publication; no publication attempted"));
                }
                hook(Stage::TempChecked)?;
                if let Err(e) = publisher(chain.last(), &temporary, &name) {
                    let code = e.raw_os_error();
                    let unsupported = matches!(
                        code,
                        Some(libc::ENOSYS) | Some(libc::EINVAL) | Some(libc::EOPNOTSUPP)
                    );
                    // These documented refusals precede publication. I/O or
                    // otherwise ambiguous outcomes require explicit recovery.
                    let definite = unsupported
                        || matches!(
                            code,
                            Some(libc::EEXIST)
                                | Some(libc::ENOENT)
                                | Some(libc::EACCES)
                                | Some(libc::EPERM)
                                | Some(libc::EROFS)
                                | Some(libc::EXDEV)
                                | Some(libc::ENOTDIR)
                                | Some(libc::EISDIR)
                                | Some(libc::ENOTEMPTY)
                        );
                    published = !definite;
                    let mut error = ioerr("exclusive no-replace publication", e);
                    if unsupported {
                        error.kind = ErrorKind::UnsupportedCapability;
                    }
                    return Err(error);
                }
                published = true;
                temp_created = false; // rename consumed this source name atomically.
                hook(Stage::Published)?;
                sync(chain.last(), "sync published account directory")?;
                self.compare(PARTS, &chain.ids)?;
                let observed = read_account(
                    chain.last(),
                    &name,
                    &attempt.relative_path,
                    chain.ids.clone(),
                )?;
                if Some(&observed.reference.file) != attempt.file.as_ref()
                    || observed.reference.sha256 != attempt.sha256
                    || observed.reference.account_id != attempt.account_id
                    || observed.reference.format_version != attempt.format_version
                {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "published identity/hash/account/version mismatch",
                    ));
                }
                hook(Stage::Verified)?;
                Ok(observed.reference)
            })();
            operation.map_err(|mut e| {
                e.uncertain_commit = published;
                if temp_created {
                    e.temporary_leftover = Some(temporary);
                    e.detail.push_str("; temporary name retained for explicit reconciliation; no automatic cleanup");
                }
                if published { attempt.observed_final = Some(observe_final(chain.last(), &name)); }
                e.attempt = Some(attempt);
                e
            })
        }
        /// Discovery is observational, not a filesystem snapshot. Re-resolve a
        /// held binding at use; never interpret absence as no outstanding work.
        pub fn discover(&self) -> Discovery {
            self.discover_using(None, |_| {})
        }
        pub(super) fn discover_using(
            &self,
            known: Option<&BoundReference>,
            mut before_base: impl FnMut(&str),
        ) -> Discovery {
            let mut out = Discovery {
                resolved_project: self.root.clone(),
                accounts: vec![],
                by_account_id: BTreeMap::new(),
                issues: vec![],
                directory_absent: false,
                enumeration_complete: false,
            };
            let mut run = || -> Result<()> {
                self.check_root()?;
                let chain = match self.chain(PARTS, false) {
                    Ok(c) => c,
                    Err(e) if e.kind == ErrorKind::Missing => {
                        self.check_root()?;
                        out.directory_absent = true;
                        return Ok(());
                    }
                    Err(e) => return Err(e),
                };
                self.compare(PARTS, &chain.ids)?;
                let (names, enumeration_error) = names(chain.last())?;
                for name in names {
                    let path = format!("{DIRECTORY}/{}", name.to_string_lossy());
                    let result = match name.to_str() {
                        Some(s) if s.starts_with(".route-") && s.ends_with(".tmp") => {
                            Err(StoreError::new(
                                ErrorKind::TemporaryLeftover,
                                "interrupted temporary file; not an account",
                            ))
                        }
                        Some(s) if canonical_name(s) => read_account_mode(
                            chain.last(),
                            s,
                            &path,
                            chain.ids.clone(),
                            known.filter(|r| r.relative_path == path).map(|_| "0.5"),
                            || {},
                        ),
                        _ => Err(StoreError::new(
                            ErrorKind::InvalidName,
                            "noncanonical entry; not an account",
                        )),
                    };
                    match result {
                        Ok(account) => {
                            out.by_account_id
                                .entry(account.reference.account_id.clone())
                                .or_default()
                                .push(path);
                            out.accounts.push(account);
                        }
                        Err(e) => out.issues.push(DiscoveryIssue {
                            relative_path: path,
                            kind: e.kind,
                            detail: e.detail,
                        }),
                    }
                }
                self.compare(PARTS, &chain.ids)?;
                if let Some(e) = enumeration_error {
                    return Err(e);
                }
                Ok(())
            };
            match run() {
                Ok(()) => out.enumeration_complete = true,
                Err(e) => out.issues.push(DiscoveryIssue {
                    relative_path: DIRECTORY.into(),
                    kind: e.kind,
                    detail: e.detail,
                }),
            }
            for (id, paths) in &out.by_account_id {
                if paths.len() > 1 {
                    out.issues.push(DiscoveryIssue {
                        relative_path: paths.join(", "),
                        kind: ErrorKind::DuplicateIdentity,
                        detail: format!("duplicate account identity {id}; no winner selected"),
                    });
                }
            }
            // Move the existing observations, not a second cloned account cache.
            let observations = std::mem::take(&mut out.accounts);
            let index = &out.by_account_id;
            let base_bindings: Vec<_> = observations
                .iter()
                .filter(|a| a.reference.format_version == "0.4")
                .map(|a| &a.reference)
                .collect();
            let uncertain_index = !out.enumeration_complete
                || out.issues.iter().any(|i| {
                    !matches!(
                        i.kind,
                        ErrorKind::TemporaryLeftover
                            | ErrorKind::InvalidName
                            | ErrorKind::DuplicateIdentity
                    )
                });
            // Resolve each base independently from bounded original bytes. No0.5 recursion.
            let mut results = Vec::new();
            for a in &observations {
                if a.reference.format_version != "0.5" {
                    results.push(None);
                    continue;
                }
                before_base(&a.reference.relative_path);
                let result = (|| -> Result<Value> {
                    if uncertain_index {
                        return Err(StoreError::new(
                            ErrorKind::UnresolvedReference,
                            "Incomplete canonical identity index; exact base unresolved",
                        ));
                    }
                    let base = &a.account["base_account"];
                    let id = base["account_id"].as_str().unwrap();
                    let path = base["relative_path"].as_str().unwrap();
                    if index.get(id).map(|p| p.as_slice()) != Some(&[path.to_owned()][..]) {
                        return Err(StoreError::new(
                            ErrorKind::UnresolvedReference,
                            "Missing or ambiguous exact base identity/path; no alternate chosen",
                        ));
                    }
                    let recorded = base_bindings
                        .iter()
                        .find(|r| r.relative_path == path)
                        .ok_or_else(|| {
                            StoreError::new(
                                ErrorKind::UnresolvedReference,
                                "Exact base is not an observed0.4 record",
                            )
                        })?;
                    let b = self.read_base(base).map_err(|e| {
                        StoreError::new(
                            ErrorKind::UnresolvedReference,
                            format!("Exact base unresolved: {e}"),
                        )
                    })?;
                    if b.reference != **recorded {
                        return Err(StoreError::new(
                            ErrorKind::UnresolvedReference,
                            "Base identity changed since discovery",
                        ));
                    }
                    let answer = crate::connector_answer_only::validate(&a.account, &b.account)
                        .map_err(|e| StoreError::new(ErrorKind::InvalidAccount, e))?;
                    let parts = relative_parts(&a.reference.relative_path)?;
                    let (name, ancestors) = parts.split_last().unwrap();
                    let chain = self.chain(ancestors, false)?;
                    let again = read_account_mode(
                        chain.last(),
                        name,
                        &a.reference.relative_path,
                        chain.ids.clone(),
                        Some("0.5"),
                        || {},
                    )?;
                    self.compare(ancestors, &a.reference.directories)?;
                    if again.reference != a.reference {
                        return Err(StoreError::new(
                            ErrorKind::ChangedContent,
                            "Answer changed during base resolution",
                        ));
                    }
                    Ok(
                        json!({"answer":answer,"baseResolution":"exact0.4 bytes resolved at this read; no continuous snapshot guarantee","baseBindingText":serde_json::to_string_pretty(&b.reference).unwrap(),"baseQuestion":b.account["question"],"baseGaps":b.account["gaps"],"baseContradictions":b.account["contradictions"],"limit":"Cold recorded-content consistency only; receipt strings do not authenticate original authorship, role emission, permission or performed duties"}),
                    )
                })();
                results.push(Some(result));
            }
            drop(base_bindings);
            for (mut a, result) in observations.into_iter().zip(results) {
                match result {
                    None => out.accounts.push(a),
                    Some(Ok(mut evidence)) => {
                        evidence["rawAccountText"] =
                            a.answer_only.take().unwrap()["rawAccountText"].take();
                        a.answer_only = Some(evidence);
                        out.accounts.push(a);
                    }
                    Some(Err(e)) => out.issues.push(DiscoveryIssue {
                        relative_path: a.reference.relative_path,
                        kind: e.kind,
                        detail: e.detail,
                    }),
                }
            }
            out
        }
        fn read_base(&self, base: &Value) -> Result<ObservedAccount> {
            let identity = &base["project_identity"];
            if identity["device"] != self.root_identity.device.to_string()
                || identity["inode"] != self.root_identity.inode.to_string()
            {
                return Err(StoreError::new(
                    ErrorKind::LocationMismatch,
                    "Base recorded project identity differs from opened root",
                ));
            }
            let path = base["relative_path"]
                .as_str()
                .ok_or_else(|| StoreError::new(ErrorKind::InvalidInput, "Missing base path"))?;
            let parts = relative_parts(path)?;
            let (name, ancestors) = parts.split_last().unwrap();
            if ancestors != PARTS || !canonical_name(name) {
                return Err(StoreError::new(
                    ErrorKind::InvalidInput,
                    "Base must use canonical UUID account path",
                ));
            }
            let chain = self.chain(ancestors, false)?;
            self.compare(ancestors, &chain.ids)?;
            let observed = read_account_mode(
                chain.last(),
                name,
                path,
                chain.ids.clone(),
                Some("0.4"),
                || {},
            )?;
            self.compare(ancestors, &chain.ids)?;
            if observed.reference.account_id != base["account_id"]
                || observed.reference.sha256 != base["sha256"]
                || base["byte_length"].as_f64() != Some(observed.byte_length as f64)
            {
                return Err(StoreError::new(
                    ErrorKind::ChangedContent,
                    "Base original hash/length/ID differs",
                ));
            }
            Ok(observed)
        }
        /// Resolve the complete held binding in this explicit project. An explicit
        /// legacy relative binding uses the same checks; there is no legacy crawl.
        pub fn resolve(&self, reference: &BoundReference) -> Result<ObservedAccount> {
            if reference.format_version == "0.5" {
                let parts = relative_parts(&reference.relative_path)?;
                let (name, ancestors) = parts.split_last().unwrap();
                if ancestors != PARTS || !canonical_name(name) {
                    return Err(StoreError::new(
                        ErrorKind::InvalidInput,
                        "Known0.5 binding requires canonical path",
                    ));
                }
                self.compare(ancestors, &reference.directories)?;
                let mut discovery = self.discover_using(Some(reference), |_| {});
                if let Some(index) = discovery
                    .accounts
                    .iter()
                    .position(|a| &a.reference == reference)
                {
                    if discovery
                        .by_account_id
                        .get(&reference.account_id)
                        .is_some_and(|p| p.len() == 1)
                    {
                        return Ok(discovery.accounts.remove(index));
                    }
                }
                return Err(StoreError::new(
                    ErrorKind::UnresolvedReference,
                    format!(
                        "Known0.5 reference unresolved or ambiguous: {:?}",
                        discovery.issues
                    ),
                ));
            }
            let parts = relative_parts(&reference.relative_path)?;
            let (name, ancestors) = parts.split_last().unwrap();
            if reference.directories.len() != ancestors.len() + 1 {
                return Err(StoreError::new(
                    ErrorKind::InvalidInput,
                    "incomplete reference directory identity binding",
                ));
            }
            self.compare(ancestors, &reference.directories)?;
            let chain = self.chain(ancestors, false)?;
            let observed = read_account(
                chain.last(),
                name,
                &reference.relative_path,
                chain.ids.clone(),
            )?;
            self.compare(ancestors, &reference.directories)?;
            if &observed.reference != reference {
                return Err(StoreError::new(ErrorKind::ChangedContent, "held reference differs from current file identity, hash, account or format; reconciliation required"));
            }
            if ancestors == PARTS {
                let discovery = self.discover();
                if !discovery.enumeration_complete || discovery.directory_absent {
                    return Err(StoreError::new(
                        ErrorKind::IncompleteDiscovery,
                        "cannot establish canonical account index",
                    ));
                }
                if discovery
                    .by_account_id
                    .get(&reference.account_id)
                    .is_some_and(|p| p.len() > 1)
                {
                    return Err(StoreError::new(
                        ErrorKind::DuplicateIdentity,
                        "duplicate account identities require explicit reconciliation",
                    ));
                }
                if !discovery.accounts.iter().any(|a| &a.reference == reference) {
                    return Err(StoreError::new(
                        ErrorKind::ChangedContent,
                        "held binding changed between resolution and canonical discovery",
                    ));
                }
                // An unreadable/malformed entry can hide a second identity.
                if discovery.issues.iter().any(|i| {
                    !matches!(
                        i.kind,
                        ErrorKind::TemporaryLeftover
                            | ErrorKind::InvalidName
                            | ErrorKind::DuplicateIdentity
                    )
                }) {
                    return Err(StoreError::new(
                        ErrorKind::IncompleteDiscovery,
                        "unresolved canonical entries prevent complete identity discovery",
                    ));
                }
            }
            Ok(observed)
        }
        /// Read-only reconciliation at the originally intended relative target.
        /// Caller must explicitly open a relocated project; no outside search or
        /// adoption of replacement directories, no new write, no durability claim.
        pub fn reconcile(&self, attempt: &Attempt) -> Result<ObservedAccount> {
            let file = attempt.file.clone().ok_or_else(|| {
                StoreError::new(
                    ErrorKind::InvalidInput,
                    "attempt has no created file identity",
                )
            })?;
            self.resolve(&BoundReference {
                relative_path: attempt.relative_path.clone(),
                account_id: attempt.account_id.clone(),
                format_version: attempt.format_version.clone(),
                sha256: attempt.sha256.clone(),
                directories: attempt.directories.clone(),
                file,
            })
        }
    }
    /// Independent open file description, so concurrent enumerations do not share
    /// an offset. errno distinguishes an interrupted/failed readdir from EOF.
    fn names(dir: &File) -> Result<(Vec<std::ffi::OsString>, Option<StoreError>)> {
        #[cfg(test)] INSPECTION_AUDIT.with(|a|{if let Some(v)=a.borrow_mut().as_mut(){v.push("enumerate".into());}});
        use std::os::fd::IntoRawFd;
        let scan = open_at(dir, OsStr::new("."), libc::O_RDONLY | libc::O_DIRECTORY)?;
        let fd = scan.into_raw_fd();
        let stream = unsafe { libc::fdopendir(fd) };
        if stream.is_null() {
            let e = std::io::Error::last_os_error();
            unsafe {
                libc::close(fd);
            }
            return Err(ioerr("open directory enumeration", e));
        }
        let mut result = vec![];
        let error = loop {
            #[cfg(target_os = "macos")]
            let errno = unsafe { libc::__error() };
            #[cfg(target_os = "linux")]
            let errno = unsafe { libc::__errno_location() };
            unsafe {
                *errno = 0;
            }
            let entry = unsafe { libc::readdir(stream) };
            if entry.is_null() {
                let code = unsafe { *errno };
                break if code == 0 {
                    None
                } else {
                    Some(ioerr(
                        "partial directory enumeration",
                        std::io::Error::from_raw_os_error(code),
                    ))
                };
            }
            let bytes = unsafe { CStr::from_ptr((*entry).d_name.as_ptr()) }.to_bytes();
            if bytes != b"." && bytes != b".." {
                result.push(OsStr::from_bytes(bytes).to_owned());
            }
        };
        let rc = unsafe { libc::closedir(stream) };
        let error = error.or_else(|| {
            if rc < 0 {
                Some(ioerr("close enumeration", std::io::Error::last_os_error()))
            } else {
                None
            }
        });
        Ok((result, error))
    }
}
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use platform::ProjectRouteStore;
#[cfg(not(any(target_os = "macos", target_os = "linux")))]
#[derive(Debug)]
pub struct ProjectRouteStore;
#[cfg(not(any(target_os = "macos", target_os = "linux")))]
impl ProjectRouteStore {
    pub fn open(_: &Path) -> Result<Self> {
        Err(StoreError::new(ErrorKind::UnsupportedPlatform, "route persistence requires qualified no-follow directory handles and no-replace publication; no fallback"))
    }
}

#[cfg(all(test, any(target_os = "macos", target_os = "linux")))]
#[path = "connector_route_store_tests.rs"]
mod tests;

#[cfg(all(test, any(target_os = "macos", target_os = "linux")))]
#[path = "connector_answer_only_tests.rs"]
mod answer_only_tests;
