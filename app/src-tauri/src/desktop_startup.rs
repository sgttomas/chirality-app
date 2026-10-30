//! Explicit desktop requests. A profile names sources; it grants no custody,
//! supplier qualification, credential access, or permission to change a live Root.
use crate::{
    attachments::native_path_identity,
    home_resources::{HomeClass, OwnedHomePlan, SharedResourceTargets},
    hosting::{attachment_custody::NativeNamespaceBindings, HostConfig},
    runtime_session, storage,
};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::{
    fs::{File, OpenOptions},
    io::{Read, Write},
    os::{
        fd::AsRawFd,
        unix::{
            ffi::OsStringExt,
            fs::{DirBuilderExt, MetadataExt, OpenOptionsExt},
        },
    },
    path::{Component, Path, PathBuf},
    sync::Arc,
};

const PROFILE: &str = "desktop-startup/request.json";
const LIMIT: u64 = 64 * 1024;
const SUPPLIER: &str = "bundled-owner-use-development";

/// Same lossless tagged native path representation used by attachments. Display
/// strings are presentation only; native picker paths never round-trip through them.
#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(tag = "encoding", deny_unknown_fields)]
enum NativePath {
    #[serde(rename = "unix_bytes")]
    Unix { bytes: Vec<u8> },
}
impl NativePath {
    fn new(path: &Path) -> Self {
        serde_json::from_value(native_path_identity(path)).expect("Unix native path")
    }
    fn path(&self) -> Result<PathBuf, String> {
        let Self::Unix { bytes } = self;
        if bytes.is_empty() || bytes.len() > 16_384 || bytes.contains(&0) {
            return Err("native path is empty, over bound or contains NUL".into());
        }
        let path = PathBuf::from(std::ffi::OsString::from_vec(bytes.clone()));
        clean(&path)?;
        Ok(path)
    }
}
pub(crate) fn explicit_path(value: Value) -> Result<PathBuf, String> {
    serde_json::from_value::<NativePath>(value)
        .map_err(|e| format!("explicit native path invalid: {e}"))?
        .path()
}

/// Metadata reference, never content identity, authentication or a lock receipt.
#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
struct ObjectRef {
    device: u64,
    inode: u64,
}
impl ObjectRef {
    fn of(meta: &std::fs::Metadata) -> Self {
        Self {
            device: meta.dev(),
            inode: meta.ino(),
        }
    }
}
#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
struct Reference {
    location: NativePath,
    resolved: NativePath,
    object: Option<ObjectRef>,
}
impl Reference {
    fn observe(path: &Path) -> Result<Self, String> {
        clean(path)?;
        let object = match std::fs::metadata(path) {
            Ok(meta) => Some(ObjectRef::of(&meta)),
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
            Err(e) => return Err(format!("source metadata unavailable: {e}")),
        };
        Ok(Self {
            location: NativePath::new(path),
            resolved: NativePath::new(&location(path)?),
            object,
        })
    }
    fn current(&self, receiving: bool) -> Result<PathBuf, String> {
        let path = self.location.path()?;
        if location(&path)? != self.resolved.path()? {
            return Err(
                "requested source path/alias now resolves elsewhere; review setup again".into(),
            );
        }
        if receiving {
            storage::check_path(&path)?;
        }
        match std::fs::metadata(&path) {
            Ok(meta) => {
                if !receiving && meta.is_file() && meta.nlink() != 1 {
                    return Err(
                        "shared source has ambiguous hard aliases; review setup again".into(),
                    );
                }
                if receiving && !meta.is_dir() {
                    return Err("receiving source is not a directory".into());
                }
                if self
                    .object
                    .as_ref()
                    .is_some_and(|id| *id != ObjectRef::of(&meta))
                {
                    return Err("requested source identity was replaced; review setup again".into());
                }
                if receiving && self.object.is_none() {
                    return Err("receiving source identity missing".into());
                }
            }
            // ACCESS CL-2/CL-5/CL-6: an explicit resource reference may be
            // absent. That source limit is not a home-start veto.
            Err(e) if !receiving && e.kind() == std::io::ErrorKind::NotFound => {}
            Err(e) => return Err(format!("receiving/source metadata unavailable: {e}")),
        }
        Ok(path)
    }
}
#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
struct RequestedInputs {
    version: u8,
    supplier: String,
    app_data: Reference,
    account: Reference,
    shared: [Reference; 3],
    project: Option<Reference>,
}

fn clean(path: &Path) -> Result<(), String> {
    if !path.is_absolute()
        || path
            .components()
            .any(|c| matches!(c, Component::ParentDir | Component::CurDir))
    {
        return Err("explicit absolute path without relative aliases required".into());
    }
    Ok(())
}
/// Canonical existing ancestor plus missing suffix; no directory-content read.
fn location(path: &Path) -> Result<PathBuf, String> {
    clean(path)?;
    location_with_links(path, 0)
}
fn location_with_links(path: &Path, depth: usize) -> Result<PathBuf, String> {
    if depth > 40 {
        return Err("source link cycle/depth; relationship unavailable".into());
    }
    let mut at = path;
    let mut suffix = vec![];
    loop {
        match std::fs::symlink_metadata(at) {
            Ok(meta) => {
                let mut result = if meta.file_type().is_symlink() {
                    let target = std::fs::read_link(at).map_err(|e| e.to_string())?;
                    let target = if target.is_absolute() {
                        target
                    } else {
                        at.parent().ok_or("link parent absent")?.join(target)
                    };
                    location_with_links(&target, depth + 1)?
                } else {
                    at.canonicalize()
                        .map_err(|e| format!("source relationship unavailable: {e}"))?
                };
                for item in suffix.into_iter().rev() {
                    result.push(item);
                }
                return Ok(result);
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                suffix.push(at.file_name().ok_or("path ancestor absent")?.to_os_string());
                at = at.parent().ok_or("path ancestor absent")?;
            }
            Err(e) => return Err(format!("source relationship unavailable: {e}")),
        }
    }
}
fn overlaps(a: &Path, b: &Path) -> bool {
    a.starts_with(b) || b.starts_with(a)
}
fn disjoint(a: &Path, b: &Path) -> Result<(), String> {
    if overlaps(&location(a)?, &location(b)?) {
        return Err("requested source namespaces overlap".into());
    }
    if let (Ok(a), Ok(b)) = (std::fs::metadata(a), std::fs::metadata(b)) {
        if ObjectRef::of(&a) == ObjectRef::of(&b) {
            return Err("requested sources are physical aliases".into());
        }
    }
    Ok(())
}

/// Locks the *directory inode*, not a replaceable lock-file pathname. The App
/// data directory is outside the native homes/project. A second spelling of
/// the same directory conflicts in the kernel. No lock file is serialized,
/// removed, or recreated; retained descriptors are rechecked against paths.
struct DirectoryLease {
    file: File,
    path: PathBuf,
    object: ObjectRef,
}
impl DirectoryLease {
    fn acquire(path: &Path) -> Result<Self, String> {
        storage::check_path(path)?;
        let file = OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC)
            .open(path)
            .map_err(|e| format!("desktop directory custody unavailable: {e}"))?;
        let meta = file.metadata().map_err(|e| e.to_string())?;
        if !meta.is_dir() || meta.uid() != unsafe { libc::geteuid() } || meta.mode() & 0o022 != 0 {
            return Err(
                "desktop custody directory must be owned by this user and not writable by others"
                    .into(),
            );
        }
        if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } != 0 {
            return Err(format!(
                "desktop profile/home is already in use or custody unavailable (no wait): {}",
                std::io::Error::last_os_error()
            ));
        }
        let lease = Self {
            file,
            path: path.to_owned(),
            object: ObjectRef::of(&meta),
        };
        lease.recheck()?;
        Ok(lease)
    }
    fn recheck(&self) -> Result<(), String> {
        storage::check_path(&self.path)?;
        let meta = std::fs::symlink_metadata(&self.path).map_err(|e| e.to_string())?;
        if !meta.is_dir()
            || meta.uid() != unsafe { libc::geteuid() }
            || meta.mode() & 0o022 != 0
            || ObjectRef::of(&meta) != self.object
            || ObjectRef::of(&self.file.metadata().map_err(|e| e.to_string())?) != self.object
        {
            return Err("desktop custody directory path was replaced; no binding".into());
        }
        Ok(())
    }
}
impl Drop for DirectoryLease {
    fn drop(&mut self) {
        unsafe {
            libc::flock(self.file.as_raw_fd(), libc::LOCK_UN);
        }
    }
}

/// Held receiving descriptor detects path replacement independently of the
/// profile claim. App-data inode custody excludes other desktop binders.
struct ReceivingSource {
    file: File,
    reference: Reference,
}
/// Native entry metadata only: do not follow a receiving link or read content.
/// A stable missing/broken/conflicting entry remains its admitted source limit.
#[derive(Clone, Debug, PartialEq, Eq)]
enum ReceivingEntry {
    Missing,
    Present {
        object: ObjectRef,
        file_type: std::fs::FileType,
        link: Option<PathBuf>,
    },
}
impl ReceivingEntry {
    fn observe(path: &Path) -> Result<Self, String> {
        let meta = match std::fs::symlink_metadata(path) {
            Ok(meta) => meta,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(Self::Missing),
            Err(e) => return Err(format!("receiving entry metadata unavailable: {e}")),
        };
        let object = ObjectRef::of(&meta);
        let file_type = meta.file_type();
        let link = if meta.file_type().is_symlink() {
            Some(std::fs::read_link(path).map_err(|e| format!("receiving link unavailable: {e}"))?)
        } else {
            None
        };
        let current = std::fs::symlink_metadata(path)
            .map_err(|e| format!("receiving entry changed during observation: {e}"))?;
        if ObjectRef::of(&current) != object || current.file_type() != file_type {
            return Err("receiving entry replaced during observation".into());
        }
        Ok(Self::Present {
            object,
            file_type,
            link,
        })
    }
}
impl ReceivingSource {
    fn open(reference: &Reference) -> Result<Self, String> {
        let path = reference.current(true)?;
        let file = OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC)
            .open(path)
            .map_err(|e| e.to_string())?;
        let result = Self {
            file,
            reference: reference.clone(),
        };
        // No native lock file is created. Hold the actual receiving directory
        // inode exclusively for this process, independently of profile custody.
        if unsafe { libc::flock(result.file.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } != 0 {
            return Err(format!("account home already has a participating owner or custody is unavailable (no wait): {}", std::io::Error::last_os_error()));
        }
        result.recheck()?;
        Ok(result)
    }
    fn recheck(&self) -> Result<(), String> {
        self.reference.current(true)?;
        let metadata = self.file.metadata().map_err(|e| e.to_string())?;
        if metadata.uid() != unsafe { libc::geteuid() } || metadata.mode() & 0o077 != 0 {
            return Err(
                "receiving account directory is no longer private/current-user owned".into(),
            );
        }
        if self.reference.object.as_ref()
            != Some(&ObjectRef::of(
                &self.file.metadata().map_err(|e| e.to_string())?,
            ))
        {
            return Err("receiving descriptor identity changed".into());
        }
        Ok(())
    }
    fn entries(&self) -> Result<[ReceivingEntry; 3], String> {
        self.recheck()?;
        let home = self.reference.location.path()?;
        let entries = [
            ReceivingEntry::observe(&home.join("config.toml"))?,
            ReceivingEntry::observe(&home.join("AGENTS.md"))?,
            ReceivingEntry::observe(&home.join("skills"))?,
        ];
        self.recheck()?;
        Ok(entries)
    }
}
impl Drop for ReceivingSource {
    fn drop(&mut self) {
        unsafe {
            libc::flock(self.file.as_raw_fd(), libc::LOCK_UN);
        }
    }
}

fn protected_directory(path: &Path) -> Result<(), String> {
    storage::check_path(path)?;
    if !path.exists() {
        let mut missing = Vec::new();
        let mut ancestor = path;
        while !ancestor.exists() {
            missing.push(ancestor.to_owned());
            ancestor = ancestor
                .parent()
                .ok_or("private directory ancestor absent")?;
        }
        std::fs::DirBuilder::new()
            .recursive(true)
            .mode(0o700)
            .create(path)
            .map_err(|e| e.to_string())?;
        for directory in missing {
            storage::sync_dir(&directory)?;
        }
        storage::sync_dir(ancestor)?;
    }
    let meta = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    if !meta.is_dir() || meta.uid() != unsafe { libc::geteuid() } || meta.mode() & 0o077 != 0 {
        return Err(
            "desktop profile directory must be private (0700) and owned by this user".into(),
        );
    }
    Ok(())
}
#[derive(Clone, Debug, PartialEq, Eq)]
struct ProfileBaseline {
    object: ObjectRef,
    digest: String,
}
#[derive(Clone)]
struct LoadedProfile {
    baseline: ProfileBaseline,
    request: RequestedInputs,
}
struct AdmittedDesktop {
    profile: LoadedProfile,
    // An unavailable initial observation disables retaining, not home startup.
    // This native snapshot is never persisted as an admission/profile claim.
    receiving_entries: Result<[ReceivingEntry; 3], String>,
}

// These capabilities never have a renderer/profile constructor. The old file
// descriptor is retained across replacement; a pathname alone is insufficient.
pub(crate) struct ConfigSlotPreflight {
    admission: Arc<AdmittedDesktop>,
    epoch: String,
    old: ConfigObject,
    siblings: [(Reference, ReceivingEntry); 2],
}
impl ConfigSlotPreflight {
    pub(crate) fn target(&self) -> Result<PathBuf, String> {
        self.old.path()
    }
    pub(crate) fn receiving_config(&self) -> Result<PathBuf, String> {
        Ok(self
            .admission
            .profile
            .request
            .account
            .location
            .path()?
            .join("config.toml"))
    }
}

pub(crate) struct ConfigObject {
    file: File,
    reference: Reference,
    state: ConfigObjectState,
}
#[derive(PartialEq, Eq)]
struct ConfigObjectState {
    object: ObjectRef,
    size: u64,
    modified: (i64, i64),
    changed: (i64, i64),
    mode: u32,
}
impl ConfigObjectState {
    fn of(meta: &std::fs::Metadata) -> Result<Self, String> {
        if !meta.is_file() || meta.nlink() != 1 || meta.uid() != unsafe { libc::geteuid() } {
            return Err(
                "Config continuation requires an owned, singly linked regular target".into(),
            );
        }
        Ok(Self {
            object: ObjectRef::of(meta),
            size: meta.len(),
            modified: (meta.mtime(), meta.mtime_nsec()),
            changed: (meta.ctime(), meta.ctime_nsec()),
            mode: meta.mode(),
        })
    }
}
impl ConfigObject {
    fn open(reference: Reference) -> Result<Self, String> {
        let path = reference.location.path()?;
        if path != reference.resolved.path()? {
            return Err("Config continuation requires the exact canonical target reference".into());
        }
        storage::check_path(&path)?;
        let file = OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_NONBLOCK | libc::O_NOFOLLOW | libc::O_CLOEXEC)
            .open(&path)
            .map_err(|_| "Config target descriptor unavailable")?;
        let state = ConfigObjectState::of(
            &file
                .metadata()
                .map_err(|_| "Config target descriptor unavailable")?,
        )?;
        let object = Self {
            file,
            reference,
            state,
        };
        object.check()?;
        Ok(object)
    }
    pub(crate) fn path(&self) -> Result<PathBuf, String> {
        self.reference.resolved.path()
    }
    pub(crate) fn check(&self) -> Result<(), String> {
        self.reference.current(false)?;
        let path = self.path()?;
        let now =
            std::fs::symlink_metadata(&path).map_err(|_| "Config current object unavailable")?;
        if ConfigObjectState::of(&now)? != self.state
            || ConfigObjectState::of(
                &self
                    .file
                    .metadata()
                    .map_err(|_| "Config held object unavailable")?,
            )? != self.state
        {
            return Err("Config checked current object changed".into());
        }
        Ok(())
    }
}

fn read_profile_bytes(path: &Path) -> Result<(Vec<u8>, ProfileBaseline), String> {
    storage::check_path(path)?;
    let file = OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NONBLOCK | libc::O_NOFOLLOW | libc::O_CLOEXEC)
        .open(path)
        .map_err(|e| format!("desktop setup request unavailable: {e}"))?;
    let meta = file.metadata().map_err(|e| e.to_string())?;
    if !meta.is_file()
        || meta.nlink() != 1
        || meta.uid() != unsafe { libc::geteuid() }
        || meta.mode() & 0o077 != 0
    {
        return Err(
            "desktop request must be a private, singly linked regular file owned by this user"
                .into(),
        );
    }
    let mut bytes = vec![];
    (&file)
        .take(LIMIT + 1)
        .read_to_end(&mut bytes)
        .map_err(|e| e.to_string())?;
    if bytes.len() as u64 > LIMIT {
        return Err("desktop request exceeds 64KiB bound".into());
    }
    let current = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    if !current.is_file() || current.nlink() != 1 || ObjectRef::of(&current) != ObjectRef::of(&meta)
    {
        return Err("desktop request source replaced during read".into());
    }
    let baseline = ProfileBaseline {
        object: ObjectRef::of(&current),
        digest: crate::util::sha256_hex(&bytes),
    };
    Ok((bytes, baseline))
}
#[cfg(test)]
fn read_profile(path: &Path) -> Result<RequestedInputs, String> {
    let (bytes, _) = read_profile_bytes(path)?;
    serde_json::from_slice(&bytes)
        .map_err(|e| format!("desktop request is incomplete or invalid: {e}"))
}
fn write_profile(path: &Path, requested: &RequestedInputs) -> Result<(), String> {
    storage::check_path(path)?;
    // Explicit setup may replace malformed request *bytes*, but must not
    // overwrite a symlink, special file, foreign owner or hard alias.
    match std::fs::symlink_metadata(path) {
        Ok(meta)
            if !meta.is_file() || meta.nlink() != 1 || meta.uid() != unsafe { libc::geteuid() } =>
        {
            return Err(
                "desktop request destination is not a singly linked owned regular file".into(),
            )
        }
        Ok(_) => {}
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
        Err(e) => return Err(e.to_string()),
    }
    let bytes = serde_json::to_vec_pretty(requested).map_err(|e| e.to_string())?;
    if bytes.len() as u64 > LIMIT {
        return Err("desktop request exceeds 64KiB bound".into());
    }
    let parent = path.parent().ok_or("profile parent absent")?;
    protected_directory(parent)?;
    let temporary = parent.join(crate::util::opaque_id(".request-")?);
    let result = (|| {
        let mut file = OpenOptions::new()
            .write(true)
            .create_new(true)
            .mode(0o600)
            .custom_flags(libc::O_NOFOLLOW | libc::O_CLOEXEC)
            .open(&temporary)
            .map_err(|e| e.to_string())?;
        file.write_all(&bytes)
            .and_then(|_| file.sync_all())
            .map_err(|e| e.to_string())?;
        std::fs::rename(&temporary, path).map_err(|e| e.to_string())?;
        storage::sync_dir(parent)
    })();
    if temporary.exists() {
        let _ = std::fs::remove_file(temporary);
    }
    result
}

pub(crate) struct Launch {
    pub workspace: Option<PathBuf>,
    pub host_config: Result<HostConfig, String>,
    pub key_path: Option<PathBuf>,
    pub shared_paths: [Option<PathBuf>; 3],
    pub bootstrap: Option<Arc<runtime_session::HomeBootstrapSet>>,
    pub namespaces: Option<Result<Arc<NativeNamespaceBindings>, String>>,
    pub source: &'static str,
}
/// The *only* desktop input handed to operational Root initialization. Setup's
/// own local data capability stays inside DesktopSetup and is not this value.
pub(crate) struct RootInputs {
    pub launch: Launch,
    pub data: Result<PathBuf, String>,
    pub allow_operational: bool,
}
impl Launch {
    pub fn environment(
        workspace: Option<PathBuf>,
        host_config: Result<HostConfig, String>,
        key_path: Option<PathBuf>,
        shared_paths: [Option<PathBuf>; 3],
    ) -> Self {
        Self {
            workspace,
            host_config,
            key_path,
            shared_paths,
            bootstrap: None,
            namespaces: None,
            source: "explicit environment (exclusive)",
        }
    }
    fn setup(reason: String) -> Self {
        Self {
            workspace: None,
            host_config: Err(format!("Desktop setup required: {reason}")),
            key_path: None,
            shared_paths: [None, None, None],
            bootstrap: None,
            namespaces: None,
            source: "desktop setup required",
        }
    }
}

enum PreviewKind {
    NewHome,
    RetainProject {
        admission: Arc<AdmittedDesktop>,
        request: RequestedInputs,
    },
}
struct Preview {
    token: String,
    kind: PreviewKind,
    account: PathBuf,
    shared: SharedResourceTargets,
    project: Option<PathBuf>,
    source_refs: [Reference; 3],
    project_ref: Option<Reference>,
}
pub(crate) struct DesktopSetup {
    data: Result<PathBuf, String>,
    resources: Result<PathBuf, String>,
    lease: Option<DirectoryLease>,
    profile_directory: Option<DirectoryLease>,
    receiving: Option<ReceivingSource>,
    requested: Option<RequestedInputs>,
    loaded_profile: Option<LoadedProfile>,
    admitted: Option<Arc<AdmittedDesktop>>,
    preview: Option<Preview>,
    pub(crate) launch_state: Value,
    pending: Value,
    config_epoch: Option<String>,
    config_publication_unknown: bool,
    config_edit_unconfirmed: bool,
    #[cfg(test)]
    after_config_publication: Option<Box<dyn FnOnce() + Send>>,
}
impl DesktopSetup {
    pub fn new(data: Result<PathBuf, String>, resources: Result<PathBuf, String>) -> Self {
        let data = data.and_then(|data| location(&data));
        Self {
            data,
            resources,
            lease: None,
            profile_directory: None,
            receiving: None,
            requested: None,
            loaded_profile: None,
            admitted: None,
            preview: None,
            launch_state: json!({"state":"setup-required","reason":"No explicit desktop request saved"}),
            pending: Value::Null,
            config_epoch: None,
            config_publication_unknown: false,
            config_edit_unconfirmed: false,
            #[cfg(test)]
            after_config_publication: None,
        }
    }
    pub fn admit_root(
        &mut self,
        launch: Launch,
        environment_data: Result<PathBuf, String>,
    ) -> RootInputs {
        self.admitted = None;
        if launch.source == "explicit environment (exclusive)" {
            // Preserve the complete legacy route, including its independently
            // configured records override when App-data itself is unavailable.
            return RootInputs {
                launch,
                data: environment_data,
                allow_operational: true,
            };
        }
        let admitted = (|| {
            launch.host_config.as_ref().map_err(Clone::clone)?;
            if self.lease.is_none()
                || self.profile_directory.is_none()
                || self.receiving.is_none()
                || self.requested.is_none()
                || self.loaded_profile.is_none()
            {
                return Err("desktop held source admission unavailable".to_string());
            }
            self.recheck()?;
            let (_, current) =
                read_profile_bytes(&self.data.as_ref().map_err(Clone::clone)?.join(PROFILE))?;
            if current != self.loaded_profile.as_ref().unwrap().baseline {
                return Err("Pending desktop request changed before Root admission".into());
            }
            let receiving_entries = self.receiving.as_ref().unwrap().entries();
            // A resource-observation limit does not veto startup. Lost held
            // source/custody still refuses operational admission independently.
            self.recheck()?;
            self.data.clone().map(|data| (data, receiving_entries))
        })();
        match admitted {
            Ok((data, receiving_entries)) => {
                self.admitted = Some(Arc::new(AdmittedDesktop {
                    profile: self.loaded_profile.clone().unwrap(),
                    receiving_entries,
                }));
                RootInputs {
                    launch,
                    data: Ok(data),
                    allow_operational: true,
                }
            }
            Err(reason) => {
                self.receiving = None;
                self.requested = None;
                self.loaded_profile = None;
                self.admitted = None;
                self.launch_state = json!({"state":"setup-required","reason":reason,"operationalData":"not admitted; setup-only local input capability retained"});
                RootInputs {
                    launch: Launch::setup(reason.clone()),
                    data: Err(format!("Desktop operational data not admitted: {reason}")),
                    allow_operational: false,
                }
            }
        }
    }
    pub fn resolve(
        &mut self,
        environment: Option<Launch>,
        is_dev: bool,
        probe: impl FnOnce() -> Result<PathBuf, String>,
    ) -> Launch {
        self.admitted = None;
        self.loaded_profile = None;
        if let Some(launch) = environment {
            self.launch_state = json!({"state":"environment","reason":launch.host_config.as_ref().err(),"standing":"Environment inputs are exclusive, including errors; saved desktop requests are not read"});
            return launch;
        }
        match self.saved_launch(is_dev, probe) {
            Ok(launch) => {
                self.launch_state = json!({"state":"saved-request","standing":"Fresh launch revalidated explicit desktop sources; supplier qualification remains unavailable"});
                launch
            }
            Err(reason) => {
                self.receiving = None;
                self.requested = None;
                self.loaded_profile = None;
                self.admitted = None;
                self.launch_state = json!({"state":"setup-required","reason":reason});
                Launch::setup(reason)
            }
        }
    }
    fn acquire(&mut self) -> Result<(), String> {
        let data = self.data.as_ref().map_err(Clone::clone)?;
        storage::check_path(data)?;
        if self.lease.is_none() {
            // The actual Tauri App-data root may be 0755; only its profile
            // child is required to be 0700. Never chmod an existing root.
            if !data.exists() {
                protected_directory(data)?;
            }
            self.lease = Some(DirectoryLease::acquire(data)?);
        }
        self.lease.as_ref().unwrap().recheck()?;
        let directory = data.join("desktop-startup");
        protected_directory(&directory)?;
        if self.profile_directory.is_none() {
            self.profile_directory = Some(DirectoryLease::acquire(&directory)?);
        }
        self.profile_directory.as_ref().unwrap().recheck()
    }
    fn validate(
        &self,
        request: &RequestedInputs,
    ) -> Result<(PathBuf, SharedResourceTargets, Option<PathBuf>), String> {
        if request.version != 1 || request.supplier != SUPPLIER {
            return Err("unsupported/incomplete explicit desktop request".into());
        }
        let data = self.data.as_ref().map_err(Clone::clone)?;
        if request.app_data.current(true)? != *data {
            return Err("desktop request belongs to a different actual App-data root".into());
        }
        let account = request.account.current(true)?;
        let shared = request.shared.each_ref().map(|r| r.current(false));
        let [config, agents, skills] = shared;
        let shared = SharedResourceTargets {
            config_toml: config?,
            global_agents_md: agents?,
            skills: skills?,
        };
        let project = request
            .project
            .as_ref()
            .map(|p| p.current(true))
            .transpose()?;
        self.relationships(&account, &shared, project.as_deref())?;
        OwnedHomePlan::new(
            data.clone(),
            account.clone(),
            HomeClass::Account,
            Some(shared.clone()),
        )?
        .inspect()?;
        Ok((account, shared, project))
    }
    fn relationships(
        &self,
        account: &Path,
        shared: &SharedResourceTargets,
        project: Option<&Path>,
    ) -> Result<(), String> {
        let data = self.data.as_ref().map_err(Clone::clone)?;
        // Only this allocation namespace can be received from a saved request;
        // setup creates a new leaf and cannot adopt an existing foreign home.
        if account.parent() != Some(data.join("account-homes").as_path()) {
            return Err(
                "desktop account must be a new leaf in the actual App-data account-homes directory"
                    .into(),
            );
        }
        storage::check_path(account)?;
        let sources = [
            &shared.config_toml,
            &shared.global_agents_md,
            &shared.skills,
        ];
        let protected = [
            data.join("desktop-startup"),
            data.join("records"),
            data.join("runtime"),
            data.join("instructions"),
            data.join("capture-seal"),
            data.join("installation.json"),
            data.join("account-homes"),
        ];
        for source in sources {
            clean(source)?;
            for domain in &protected {
                disjoint(source, domain)?;
            }
            disjoint(source, account)?;
        }
        for (i, a) in sources.iter().enumerate() {
            for b in sources.iter().skip(i + 1) {
                disjoint(a, b)?;
            }
        }
        if let Some(project) = project {
            clean(project)?;
            storage::check_path(project)?;
            if !project.is_dir() {
                return Err("explicit project is not an existing directory".into());
            }
            disjoint(project, data)?;
            for source in sources {
                disjoint(project, source)?;
            }
        }
        Ok(())
    }
    fn saved_launch(
        &mut self,
        is_dev: bool,
        probe: impl FnOnce() -> Result<PathBuf, String>,
    ) -> Result<Launch, String> {
        let data = self.data.as_ref().map_err(Clone::clone)?.clone();
        // No request => no automatic home preparation or supplier work.
        if !data.join(PROFILE).try_exists().map_err(|e| e.to_string())? {
            return Err("No explicit desktop request saved".into());
        }
        self.acquire()?;
        let (bytes, baseline) = read_profile_bytes(&data.join(PROFILE))?;
        let mut requested: RequestedInputs = serde_json::from_slice(&bytes)
            .map_err(|e| format!("desktop request is incomplete or invalid: {e}"))?;
        self.loaded_profile = Some(LoadedProfile {
            baseline,
            request: requested.clone(),
        });
        let (account, shared, workspace) = self.validate(&requested)?;
        // A reference explicitly absent at setup can become available (CL-6).
        // Freeze its actual object for this launch's later source checks; this
        // observation is not persisted as a new request or admission receipt.
        for reference in &mut requested.shared {
            if reference.object.is_none() {
                *reference = Reference::observe(&reference.location.path()?)?;
            }
        }
        self.receiving = Some(ReceivingSource::open(&requested.account)?);
        self.requested = Some(requested);
        let resources = self.resources.as_ref().map_err(Clone::clone)?.clone();
        let probe = probe()?;
        disjoint(&probe, &data)?;
        if let Some(project) = &workspace {
            disjoint(&probe, project)?;
        }
        for target in [
            &shared.config_toml,
            &shared.global_agents_md,
            &shared.skills,
        ] {
            disjoint(&probe, target)?;
        }
        let mut config = if !is_dev && cfg!(feature = "distribution-successor") {
            // A desktop development selection cannot weaken a compiled
            // production route. Existing installed-custody refusal is retained.
            crate::hosting::successor::production_config(
                resources,
                account,
                probe,
                workspace.clone().unwrap_or(data.clone()),
            )
        } else {
            if !cfg!(debug_assertions) {
                return Err("owner-use desktop supplier selection is available in debug development builds only".into());
            }
            let mut cfg = HostConfig::new(
                resources.join("codex/bin/codex"),
                account,
                probe,
                workspace.clone().unwrap_or(data.clone()),
            );
            cfg.expected_sha256 = Some(development_binary_assertion()?);
            cfg.allow_unverified_dev = true;
            cfg
        };
        config.records_project = workspace.is_some();
        config.require_distribution_artifacts = config.distribution.is_some();
        let shared_paths = [
            Some(shared.config_toml),
            Some(shared.global_agents_md),
            Some(shared.skills),
        ];
        let bootstrap = Arc::new(runtime_session::freeze_root_home_descriptors(
            &data,
            &config,
            None,
            shared_paths.clone(),
        )?);
        // Native namespace closure may be unavailable for a missing/broken
        // shared resource. Preserve that per-feature refusal, ACCESS Q-1.
        let namespaces = bootstrap.native_namespaces(false);
        if let Ok(bindings) = &namespaces {
            bindings.guard_app_root(&data)?;
            bindings.guard_domains(&[
                data.join("desktop-startup"),
                data.join("records"),
                data.join("runtime"),
                data.join("instructions"),
                data.join("capture-seal"),
                data.join("installation.json"),
            ])?;
        }
        self.recheck()?;
        Ok(Launch {
            workspace,
            host_config: Ok(config),
            key_path: None,
            shared_paths,
            bootstrap: Some(bootstrap),
            namespaces: Some(namespaces),
            source: "explicit saved desktop request, revalidated this launch",
        })
    }
    fn recheck_storage(&self) -> Result<(), String> {
        if let Some(lease) = &self.lease {
            lease.recheck()?;
        }
        if let Some(lease) = &self.profile_directory {
            lease.recheck()?;
        }
        if let Some(lease) = &self.profile_directory {
            if lease.file.metadata().map_err(|e| e.to_string())?.mode() & 0o077 != 0 {
                return Err("desktop profile directory is no longer private".into());
            }
        }
        Ok(())
    }
    pub fn recheck(&self) -> Result<(), String> {
        if self.config_publication_unknown { return Err("Config request publication outcome unknown; fresh admission required".into()); }
        self.recheck_storage()?;
        if let Some(source) = &self.receiving {
            source.recheck()?;
        }
        if let Some(requested) = &self.requested {
            self.validate(requested)?;
        }
        Ok(())
    }
    pub fn recheck_active(&self) -> Result<(), String> {
        if self.config_edit_unconfirmed { return Err("Endpoint write may have changed configuration; current source has not been continued".into()); }
        if self.requested.is_some() {
            self.recheck()?;
        }
        // A pending desktop request cannot impose desktop locks/source guards
        // on the independently frozen, exclusive environment route.
        Ok(())
    }
    pub fn view(&self) -> Value {
        let active_resources = self
            .requested
            .as_ref()
            .map(|request| {
                let (account, shared, _) = self.validate(request)?;
                let plan = OwnedHomePlan::new(
                    self.data.as_ref().map_err(Clone::clone)?.clone(),
                    account,
                    HomeClass::Account,
                    Some(shared),
                )?;
                resource_view(&plan)
            })
            .transpose();
        let retain = match self.retained_source() {
            Ok(_) => {
                json!({"available":true,"accountHome":self.requested.as_ref().and_then(|r|r.account.location.path().ok()).map(|p|p.display().to_string())})
            }
            Err(reason) => json!({"available":false,"reason":reason}),
        };
        json!({"retainProject":retain,"launch":self.launch_state,"appData":self.data.as_ref().ok().map(|p|p.display().to_string()),"appDataProblem":self.data.as_ref().err(),"supplier":{"selection":SUPPLIER,"path":self.resources.as_ref().ok().map(|p|p.join("codex/bin/codex").display().to_string()),"standing":"Explicit owner-use development only. Label/generated-reference/binary assertion checks still apply; derived byte identity is not authenticated qualification. A compiled production successor still refuses without installed custody."},"pending":self.pending,"activeResources":active_resources.as_ref().ok().and_then(|r|r.as_ref()),"activeResourceProblem":active_resources.as_ref().err(),"custodyProblem":self.recheck().err(),"nextLaunch":"Preparation/save changes only a pending request. Quit normally when ready and launch again; no automatic quit, restart, login, conversation or model selection."})
    }
    fn retained_source(&self) -> Result<Arc<AdmittedDesktop>, String> {
        let admission = self.admitted.as_ref().ok_or("Retaining an account requires this process's admitted saved-desktop source; no environment, pending or setup-only adoption")?;
        self.check_retained(admission)?;
        Ok(admission.clone())
    }
    fn check_retained(&self, admission: &Arc<AdmittedDesktop>) -> Result<(), String> {
        if !self
            .admitted
            .as_ref()
            .is_some_and(|current| Arc::ptr_eq(current, admission))
            || self.lease.is_none()
            || self.profile_directory.is_none()
            || self.receiving.is_none()
            || self.requested.is_none()
        {
            return Err("Original admitted desktop source is no longer held".into());
        }
        self.recheck()?;
        let admitted_entries = admission.receiving_entries.as_ref().map_err(Clone::clone)?;
        if self.receiving.as_ref().unwrap().entries()? != *admitted_entries {
            return Err("Admitted receiving entries changed or were replaced; retained project save refused".into());
        }
        let data = self.data.as_ref().map_err(Clone::clone)?;
        let (_, current) = read_profile_bytes(&data.join(PROFILE))?;
        if current != admission.profile.baseline {
            return Err("Pending desktop request changed or was replaced; launch that request before another retained project change".into());
        }
        Ok(())
    }
    pub(crate) fn begin_config_continuation(
        &mut self,
        config: &HostConfig,
    ) -> Result<ConfigSlotPreflight, String> {
        if self.config_publication_unknown {
            return Err(
                "Previous config publication outcome unknown; fresh launch required".into(),
            );
        }
        let admission = self.retained_source()?;
        let active = self
            .requested
            .as_ref()
            .ok_or("Admitted desktop source absent")?;
        let expected_cwd = active
            .project
            .as_ref()
            .map(|p| p.location.path())
            .transpose()?
            .unwrap_or(self.data.as_ref().map_err(Clone::clone)?.clone());
        if config.codex_home != active.account.location.path()? || config.cwd != expected_cwd {
            return Err("Actual account/cwd differs from admitted desktop source".into());
        }
        let old = ConfigObject::open(active.shared[0].clone())?;
        // This private seam is limited to the existing linked config slot.
        let entries = admission.receiving_entries.as_ref().map_err(Clone::clone)?;
        if !matches!(&entries[0], ReceivingEntry::Present { file_type, link:Some(_), .. } if file_type.is_symlink())
        {
            return Err("Admitted linked config slot unavailable".into());
        }
        if std::fs::canonicalize(config.codex_home.join("config.toml"))
            .map_err(|_| "Receiving config target unavailable")?
            != old.path()?
        {
            return Err("Receiving config does not identify the held shared target".into());
        }
        let epoch = crate::util::opaque_id("config-slot-epoch-")?;
        self.config_epoch = Some(epoch.clone());
        self.preview = None;
        let siblings = [1, 2]
            .map(|index| {
                let path = active.shared[index].location.path()?;
                Ok((Reference::observe(&path)?, ReceivingEntry::observe(&path)?))
            })
            .into_iter()
            .collect::<Result<Vec<_>, String>>()?
            .try_into()
            .unwrap();
        Ok(ConfigSlotPreflight {
            admission,
            epoch,
            old,
            siblings,
        })
    }
    pub(crate) fn endpoint_source_available(&self, config: &HostConfig) -> bool {
        (|| -> Result<(), String> {
            if self.config_edit_unconfirmed {
                return Err("Endpoint source unconfirmed".into());
            }
            self.retained_source()?;
            let active = self.requested.as_ref().ok_or("No admitted request")?;
            if config.cwd.to_str().is_none()
                || config.codex_home != active.account.location.path()?
                || config.cwd
                    != active
                        .project
                        .as_ref()
                        .map(|p| p.location.path())
                        .transpose()?
                        .unwrap_or(self.data.as_ref().map_err(Clone::clone)?.clone())
            {
                return Err("Actual source differs".into());
            }
            let object = ConfigObject::open(active.shared[0].clone())?;
            if object.path()?.to_str().is_none()
                || !std::fs::symlink_metadata(config.codex_home.join("config.toml"))
                    .map_err(|_| "Receiving config unavailable")?
                    .file_type()
                    .is_symlink()
                || std::fs::canonicalize(config.codex_home.join("config.toml"))
                    .map_err(|_| "Receiving target unavailable")?
                    != object.path()?
            {
                return Err("Receiving config source unavailable".into());
            }
            Ok(())
        })()
        .is_ok()
    }
    fn check_config_original(
        &self,
        preflight: &ConfigSlotPreflight,
        candidate: &ConfigObject,
    ) -> Result<RequestedInputs, String> {
        if self.config_publication_unknown
            || self.lease.is_none()
            || self.profile_directory.is_none()
            || self.config_epoch.as_ref() != Some(&preflight.epoch)
            || !self
                .admitted
                .as_ref()
                .is_some_and(|a| Arc::ptr_eq(a, &preflight.admission))
        {
            return Err("Config continuation superseded or unavailable".into());
        }
        self.recheck_storage()?;
        let receiving = self.receiving.as_ref().ok_or("Receiving custody absent")?;
        if receiving.entries()?
            != *preflight
                .admission
                .receiving_entries
                .as_ref()
                .map_err(Clone::clone)?
        {
            return Err("Original receiving entries changed".into());
        }
        if std::fs::canonicalize(preflight.receiving_config()?).map_err(|_|"Receiving target unavailable")?!=candidate.path()? {return Err("Receiving configuration target differs".into());}
        // The unlinked old descriptor still pins its inode. Its link count and
        // ctime may change as a normal consequence of atomic target replacement.
        if ObjectRef::of(
            &preflight
                .old
                .file
                .metadata()
                .map_err(|_| "Old descriptor unavailable")?,
        ) != preflight.old.state.object
        {
            return Err("Old config descriptor differs".into());
        }
        if candidate.reference.location != preflight.old.reference.location
            || candidate.reference.resolved != preflight.old.reference.resolved
        {
            return Err("Candidate target path differs".into());
        }
        let data = self.data.as_ref().map_err(Clone::clone)?;
        if read_profile_bytes(&data.join(PROFILE))?.1 != preflight.admission.profile.baseline {
            return Err("Original/pending profile superseded".into());
        }
        candidate.check()?;
        let mut active = self
            .requested
            .as_ref()
            .ok_or("Active source absent")?
            .clone();
        for (index, (reference, entry)) in preflight.siblings.iter().enumerate() {
            let path = active.shared[index + 1].location.path()?;
            if Reference::observe(&path)? != *reference || ReceivingEntry::observe(&path)? != *entry
            {
                return Err("Sibling shared resource changed".into());
            }
        }
        active.shared[0] = candidate.reference.clone();
        self.validate(&active)?; // Every sibling, namespace and relationship stays guarded.
        let mut request = preflight.admission.profile.request.clone();
        request.shared[0] = candidate.reference.clone();
        self.validate(&request)?;
        Ok(request)
    }
    pub(crate) fn observe_config_candidate(
        &self,
        preflight: &ConfigSlotPreflight,
    ) -> Result<ConfigObject, String> {
        let reference = Reference::observe(&preflight.old.path()?)?;
        let candidate = ConfigObject::open(reference)?;
        self.check_config_original(preflight, &candidate)?;
        Ok(candidate)
    }
    pub(crate) fn check_endpoint_before_write(&self, preflight:&ConfigSlotPreflight)->Result<(),String> {
        if self.config_edit_unconfirmed { return Err("Previous endpoint write remains unconfirmed".into()); }
        self.check_config_original(preflight,&preflight.old).map(|_|())
    }
    pub(crate) fn endpoint_write_attempt(&mut self, preflight:&ConfigSlotPreflight)->Result<(),String> {
        self.check_endpoint_before_write(preflight)?;
        self.config_edit_unconfirmed=true;
        Ok(())
    }
    pub(crate) fn check_config_candidate(
        &self,
        preflight: &ConfigSlotPreflight,
        candidate: &ConfigObject,
    ) -> Result<(), String> {
        self.check_config_original(preflight, candidate).map(|_| ())
    }
    pub(crate) fn publish_config_continuation(
        &mut self,
        preflight: ConfigSlotPreflight,
        candidate: ConfigObject,
        source_current: impl Fn() -> Result<(), String>,
    ) -> Result<(), String> {
        let request = self.check_config_original(&preflight, &candidate)?;
        let expected =
            serde_json::to_vec_pretty(&request).map_err(|_| "Config request encoding failed")?;
        source_current()?;
        self.check_config_original(&preflight, &candidate)?;
        let path = self.data.as_ref().map_err(Clone::clone)?.join(PROFILE);
        // From this point a failure is an explicit uncertain publication. No
        // rollback or memory promotion, even if later bytes appear favourable.
        self.config_publication_unknown = true;
        self.preview = None;
        let published = (|| {
            write_profile(&path, &request)?;
            #[cfg(test)]
            if let Some(hook) = self.after_config_publication.take() {
                hook();
            }
            let (bytes, baseline) = read_profile_bytes(&path)?;
            if bytes != expected {
                return Err("Published config request bytes differ".into());
            }
            self.recheck_storage()?;
            if self.lease.is_none()
                || self.profile_directory.is_none()
                || self.config_epoch.as_ref() != Some(&preflight.epoch)
                || !self
                    .admitted
                    .as_ref()
                    .is_some_and(|a| Arc::ptr_eq(a, &preflight.admission))
                || self
                    .receiving
                    .as_ref()
                    .ok_or("Receiving custody absent")?
                    .entries()?
                    != *preflight
                        .admission
                        .receiving_entries
                        .as_ref()
                        .map_err(Clone::clone)?
            {
                return Err("Original source changed during publication".into());
            }
            candidate.check()?;
            let mut active = self
                .requested
                .as_ref()
                .ok_or("Active source absent")?
                .clone();
            for (index, (reference, entry)) in preflight.siblings.iter().enumerate() {
                let path = active.shared[index + 1].location.path()?;
                if Reference::observe(&path)? != *reference
                    || ReceivingEntry::observe(&path)? != *entry
                {
                    return Err("Sibling shared resource changed during publication".into());
                }
            }
            active.shared[0] = candidate.reference.clone();
            self.validate(&active)?;
            self.validate(&request)?;
            source_current()?;
            // Check the exact published object again, including inode and bytes.
            let (bytes, again) = read_profile_bytes(&path)?;
            if bytes != expected || again != baseline {
                return Err("Published request superseded".into());
            }
            candidate.check()?;
            Ok((active, LoadedProfile { baseline, request }))
        })();
        let (active,profile) = published.map_err(|_:String|"Config request publication outcome unknown; no in-memory continuation; fresh admission is a separate observation")?;
        self.requested = Some(active);
        self.loaded_profile = Some(profile.clone());
        self.admitted = Some(Arc::new(AdmittedDesktop {
            profile,
            receiving_entries: preflight.admission.receiving_entries.clone(),
        }));
        self.config_epoch = None;
        self.config_publication_unknown = false;
        self.config_edit_unconfirmed = false;
        Ok(())
    }
    pub fn preview_project(&mut self, project: Option<PathBuf>) -> Result<Value, String> {
        self.config_epoch = None;
        let admission = self.retained_source()?;
        let active = self
            .requested
            .as_ref()
            .ok_or("Admitted desktop request unavailable")?;
        let (account, shared, _) = self.validate(active)?;
        self.relationships(&account, &shared, project.as_deref())?;
        let project_ref = project
            .as_ref()
            .map(|p| Reference::observe(p))
            .transpose()?;
        let mut request = admission.profile.request.clone();
        request.project = project_ref.clone();
        self.validate(&request)?;
        let plan = OwnedHomePlan::new(
            self.data.as_ref().map_err(Clone::clone)?.clone(),
            account.clone(),
            HomeClass::Account,
            Some(shared.clone()),
        )?;
        let token = crate::util::opaque_id("desktop-project-preview-")?;
        let result = json!({"token":token,"kind":"retain-account-project","affirmative":"Save project for next launch","accountHome":account.display().to_string(),"project":project.as_ref().map(|p|p.display().to_string()),"effects":[format!("Retain the currently admitted account directory {}",account.display()),format!("Project on next launch: {}",project.as_ref().map(|p|p.display().to_string()).unwrap_or_else(||"explicitly absent".into())),"Save only a pending project request; create no home, links or credentials"],"resources":resource_view(&plan)?,"standing":"Original admitted account/shared/supplier references are retained; active workspace and all current owners/choices remain unchanged"});
        self.preview = Some(Preview {
            token,
            kind: PreviewKind::RetainProject { admission, request },
            account,
            shared,
            project,
            source_refs: active.shared.clone(),
            project_ref,
        });
        Ok(result)
    }
    pub fn preview_action(&self, token: &str) -> Result<&'static str, String> {
        let preview = self
            .preview
            .as_ref()
            .filter(|p| p.token == token)
            .ok_or("Setup preview changed; review the effects again")?;
        Ok(match preview.kind {
            PreviewKind::NewHome => "Prepare home and save for next launch",
            PreviewKind::RetainProject { .. } => "Save project for next launch",
        })
    }
    pub fn preview_statement(&self, token: &str) -> Result<String, String> {
        let preview = self
            .preview
            .as_ref()
            .filter(|p| p.token == token)
            .ok_or("Setup preview changed; review the effects again")?;
        if let PreviewKind::RetainProject { admission, .. } = &preview.kind {
            self.check_retained(admission)?;
            return Ok(format!("Retain the currently admitted App-owned account directory: {}\nProject on next launch: {}\nKeep its exact shared references and supplier selection.\nCreate no home, link or credential; no re-preparation or relink.\nSave a pending project request only. Current workspace, account/home, records, attachments, recovery, model choices and prepared messages stay unchanged. No automatic quit/restart/login/conversation.", preview.account.display(), preview.project.as_ref().map(|p|p.display().to_string()).unwrap_or_else(||"explicitly absent".into())));
        }
        Ok(format!("Create NEW App-owned account directory: {}\nCreate links (no content copy or credential import):\nconfig.toml → {}\nAGENTS.md → {}\nskills → {}\nProject for next launch: {}\nSave a private pending request in {}.\nSupplier: {} ({SUPPLIER}); unqualified owner-use development.\nThe current workspace, homes, account/model choices, records and prepared messages stay unchanged. No automatic quit/restart/login/conversation.",preview.account.display(),preview.shared.config_toml.display(),preview.shared.global_agents_md.display(),preview.shared.skills.display(),preview.project.as_ref().map(|p|p.display().to_string()).unwrap_or_else(||"explicitly absent".into()),self.data.as_ref().map_err(Clone::clone)?.join(PROFILE).display(),self.resources.as_ref().map_err(Clone::clone)?.join("codex/bin/codex").display()))
    }
    /// Paths originate in explicit person input or a native picker. This preview
    /// performs metadata/path validation only; no filesystem creation or save.
    pub fn preview(
        &mut self,
        shared: [PathBuf; 3],
        project: Option<PathBuf>,
        supplier: &str,
    ) -> Result<Value, String> {
        self.config_epoch = None;
        if supplier != SUPPLIER {
            return Err("explicit owner-use development supplier selection required".into());
        }
        let data = self.data.as_ref().map_err(Clone::clone)?;
        let account = data
            .join("account-homes")
            .join(crate::util::opaque_id("account-")?);
        let [config_toml, global_agents_md, skills] = shared;
        let shared = SharedResourceTargets {
            config_toml,
            global_agents_md,
            skills,
        };
        self.relationships(&account, &shared, project.as_deref())?;
        let plan = OwnedHomePlan::new(
            data.clone(),
            account.clone(),
            HomeClass::Account,
            Some(shared.clone()),
        )?;
        let token = crate::util::opaque_id("desktop-preview-")?;
        let effects = json!({"token":token,"kind":"new-home","affirmative":"Prepare home and save for next launch","accountHome":account.display().to_string(),"effects":[format!("Create new account directory {}",account.display()),format!("Create config.toml link → {}",shared.config_toml.display()),format!("Create AGENTS.md link → {}",shared.global_agents_md.display()),format!("Create skills link → {}",shared.skills.display()),format!("Save private pending request {}",data.join(PROFILE).display())],"project":project.as_ref().map(|p|p.display().to_string()),"resources":resource_view(&plan)?,"standing":"No credential import or existing-home adoption. Only the explicit prepare/save action creates these paths. Missing targets remain visible source limits."});
        let source_refs = [
            &shared.config_toml,
            &shared.global_agents_md,
            &shared.skills,
        ]
        .map(|p| Reference::observe(p))
        .into_iter()
        .collect::<Result<Vec<_>, _>>()?
        .try_into()
        .unwrap();
        let project_ref = project
            .as_ref()
            .map(|p| Reference::observe(p))
            .transpose()?;
        self.preview = Some(Preview {
            token,
            kind: PreviewKind::NewHome,
            account,
            shared,
            project,
            source_refs,
            project_ref,
        });
        Ok(effects)
    }
    /// Deliberate setup event; never receives or mutates AppState/live owners.
    pub fn prepare_and_save(&mut self, token: &str) -> Result<Value, String> {
        let preview = self
            .preview
            .take()
            .ok_or("Preview the directory/link effects first")?;
        if preview.token != token {
            return Err("setup preview changed; review the effects again".into());
        }
        if let PreviewKind::RetainProject { admission, request } = &preview.kind {
            self.check_retained(admission)?;
            for reference in &preview.source_refs {
                reference.current(false)?;
            }
            if let Some(reference) = &preview.project_ref {
                reference.current(true)?;
            }
            self.validate(request)?;
            self.check_retained(admission)?;
            let data = self.data.as_ref().map_err(Clone::clone)?;
            write_profile(&data.join(PROFILE), request)?;
            let plan = OwnedHomePlan::new(
                data.clone(),
                preview.account.clone(),
                HomeClass::Account,
                Some(preview.shared.clone()),
            )?;
            self.pending = json!({"state":"saved-for-next-launch","kind":"retain-account-project","accountHome":preview.account.display().to_string(),"project":preview.project.as_ref().map(|p|p.display().to_string()),"resources":resource_view(&plan)?,"standing":"Pending project request only; retained account directory and links were not prepared or changed; all active Root owners and choices remain unchanged"});
            return Ok(self.view());
        }
        self.acquire()?;
        self.recheck_storage()?;
        for reference in &preview.source_refs {
            reference.current(false)?;
        }
        if let Some(reference) = &preview.project_ref {
            reference.current(true)?;
        }
        self.relationships(
            &preview.account,
            &preview.shared,
            preview.project.as_deref(),
        )?;
        let data = self.data.as_ref().map_err(Clone::clone)?.clone();
        protected_directory(&data.join("account-homes"))?;
        // Reserve a NEW directory atomically: OwnedHomePlan's create-only links
        // must never turn setup into implicit adoption of a pre-existing home.
        std::fs::DirBuilder::new()
            .mode(0o700)
            .create(&preview.account)
            .map_err(|e| {
                format!("new home was not created; existing homes are never adopted: {e}")
            })?;
        storage::sync_dir(preview.account.parent().unwrap())?;
        let plan = OwnedHomePlan::new(
            data.clone(),
            preview.account.clone(),
            HomeClass::Account,
            Some(preview.shared.clone()),
        )?;
        let observed = plan.prepare()?;
        let requested = RequestedInputs {
            version: 1,
            supplier: SUPPLIER.into(),
            app_data: Reference::observe(&data)?,
            account: Reference::observe(&preview.account)?,
            shared: preview.source_refs,
            project: preview.project_ref,
        };
        self.validate(&requested)?;
        self.recheck_storage()?;
        write_profile(&data.join(PROFILE), &requested)?;
        self.pending = json!({"state":"saved-for-next-launch","accountHome":preview.account.display().to_string(),"project":preview.project.as_ref().map(|p|p.display().to_string()),"resources":observed.resources.iter().map(|r|json!({"name":r.name,"state":format!("{:?}",r.state),"limit":r.limit})).collect::<Vec<_>>(),"standing":"Pending request only; the current workspace, homes, records, attachments, recovery, choices and prepared messages are unchanged"});
        Ok(self.view())
    }
}
fn resource_view(plan: &OwnedHomePlan) -> Result<Value, String> {
    let o = plan.inspect()?;
    Ok(json!(o
        .resources
        .iter()
        .map(|r| {
            let source = r
                .intended_target
                .as_ref()
                .map(|path| match std::fs::metadata(path) {
                    Ok(meta)
                        if (r.name == "skills" && meta.is_dir())
                            || (r.name != "skills" && meta.is_file()) =>
                    {
                        "expected source type available"
                    }
                    Ok(_) => "source type differs; resource unavailable",
                    Err(_) => "source unavailable; no fallback or content copy",
                });
            json!({"name":r.name,"state":format!("{:?}",r.state),"source":source,"limit":r.limit})
        })
        .collect::<Vec<_>>()))
}
fn development_binary_assertion() -> Result<String, String> {
    // Reuse the maintained selected-reference bytes as a development assertion,
    // not a newly invented supplier qualification or a persisted trust receipt.
    let expected: Value = serde_json::from_str(include_str!("../resources/distribution-reference/distribution-s1/references/codex-0.160.0-macos-arm64/expected.json")).map_err(|e|e.to_string())?;
    expected["inventory"]["entries"]
        .as_array()
        .into_iter()
        .flatten()
        .find(|e| e["path"] == "bin/codex")
        .and_then(|e| e["sha256"].as_str())
        .map(str::to_owned)
        .ok_or("compiled development binary assertion missing".into())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{hosting::Host, records_store};
    use std::os::unix::fs::PermissionsExt;
    use std::sync::Mutex;

    struct Fixture {
        root: PathBuf,
        data: PathBuf,
        resources: PathBuf,
        shared: [PathBuf; 3],
        project: PathBuf,
        /// The process store before this fixture; its startup joins may configure another.
        previous_store: Option<Result<records_store::Store, String>>,
    }
    impl Fixture {
        fn new() -> Self {
            let root = std::env::temp_dir()
                .canonicalize()
                .unwrap()
                .join(crate::util::opaque_id("desktop-fixture-").unwrap());
            std::fs::create_dir(&root).unwrap();
            let data = root.join("app-data");
            protected_directory(&data).unwrap();
            let resources = root.join("bundle-resources");
            let sources = root.join("explicit-shared");
            std::fs::create_dir(&sources).unwrap();
            let shared = [
                sources.join("config.toml"),
                sources.join("AGENTS.md"),
                sources.join("skills"),
            ];
            std::fs::write(&shared[0], b"fixture, never parsed by setup").unwrap();
            std::fs::write(&shared[1], b"fixture guidance, never read by setup").unwrap();
            std::fs::create_dir(&shared[2]).unwrap();
            let project = root.join("explicit-project");
            std::fs::create_dir(&project).unwrap();
            let previous_store = records_store::configured_for_test();
            records_store::use_store_for_test(Some(Ok(records_store::Store {
                root: data.join("records"),
                placement: records_store::Placement::Test,
                limits: vec![],
            })));
            Self {
                root,
                data,
                resources,
                shared,
                project,
                previous_store,
            }
        }
        fn setup(&self) -> DesktopSetup {
            DesktopSetup::new(Ok(self.data.clone()), Ok(self.resources.clone()))
        }
        fn prepare(&self, setup: &mut DesktopSetup, project: bool) -> Value {
            let preview = setup
                .preview(
                    self.shared.clone(),
                    project.then(|| self.project.clone()),
                    SUPPLIER,
                )
                .unwrap();
            assert!(!Path::new(preview["accountHome"].as_str().unwrap()).exists());
            setup
                .prepare_and_save(preview["token"].as_str().unwrap())
                .unwrap()
        }
        fn probe(&self) -> Result<PathBuf, String> {
            runtime_session::allocate_fresh_probe(&self.root)
        }
        fn resolve(&self, setup: &mut DesktopSetup) -> Launch {
            setup.resolve(None, true, || self.probe())
        }
        fn continuation(
            &self,
        ) -> (
            Arc<Mutex<DesktopSetup>>,
            crate::AppState,
            Arc<runtime_session::HomeSession>,
            crate::hosting::config_resource_continuation::TestPeer,
        ) {
            let mut setup = self.setup();
            self.prepare(&mut setup, true);
            drop(setup);
            self.admitted_continuation()
        }
        fn admitted_continuation(
            &self,
        ) -> (
            Arc<Mutex<DesktopSetup>>,
            crate::AppState,
            Arc<runtime_session::HomeSession>,
            crate::hosting::config_resource_continuation::TestPeer,
        ) {
            let mut setup = self.setup();
            let mut launch = self.resolve(&mut setup);
            launch.host_config.as_mut().unwrap().wait_limit = std::time::Duration::from_millis(30);
            let RootInputs {
                launch,
                data,
                allow_operational,
            } = setup.admit_root(launch, Ok(self.data.clone()));
            assert!(allow_operational);
            let desktop = Arc::new(Mutex::new(setup));
            let (state, home) = crate::freeze_startup_state(launch, desktop.clone(), Value::Null);
            crate::initialize_startup_consumers(
                &state,
                &home,
                data,
                allow_operational,
                true,
                Some(self.data.join("records")),
                None,
                self.shared.clone().map(Some),
            );
            let peer = crate::hosting::config_resource_continuation::TestPeer::for_config_continuation(
                home.host.clone(),
                &home.host_config.as_ref().unwrap().codex_home,
            );
            (desktop, state, home, peer)
        }
        fn replace_config(&self) {
            let replacement = self
                .root
                .join(crate::util::opaque_id("replacement-").unwrap());
            std::fs::write(
                &replacement,
                b"invented config object, no actual configuration",
            )
            .unwrap();
            std::fs::rename(replacement, &self.shared[0]).unwrap();
        }
        fn private_config(&self) -> Value {
            json!({"config":{"developer_instructions":"INVENTED_PRIVATE_PROVIDER_CANARY_481","model_providers":{"private":{"experimental_bearer_token":"INVENTED_PRIVATE_PROVIDER_CANARY_481"}}},"origins":{},"layers":[{"name":{"type":"user","file":self.shared[0]},"config":{},"version":"INVENTED_NATIVE_VERSION_PRIVATE_52","disabledReason":null}]})
        }
        fn public_endpoint_records_safe(&self) {
            fn inspect(path: &Path) {
                if !path.exists() {
                    return;
                }
                for entry in std::fs::read_dir(path).unwrap() {
                    let path = entry.unwrap().path();
                    let meta = std::fs::symlink_metadata(&path).unwrap();
                    assert!(!meta.file_type().is_symlink());
                    if meta.is_dir() {
                        inspect(&path);
                    } else {
                        let bytes = std::fs::read(&path).unwrap();
                        for marker in [
                            b"INVENTED_PRIVATE_PROVIDER_CANARY_481".as_slice(),
                            b"INVENTED_PRIVATE_OLD_VERSION".as_slice(),
                        ] {
                            assert!(
                                !bytes.windows(marker.len()).any(|w| w == marker),
                                "private native material reached an actual public record file"
                            );
                        }
                    }
                }
            }
            inspect(&self.data.join("records"));
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            records_store::use_store_for_test(None);
            records_store::restore_configured_for_test(self.previous_store.take());
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }

    #[test]
    fn access_provider_create_mounted_join() {
        let Ok(directory) = std::env::var("CHIRALITY_CREATE_JOIN") else {
            return;
        };
        let directory = PathBuf::from(directory);
        let mode = std::env::var("CHIRALITY_CREATE_MODE").unwrap_or_else(|_| "ok".into());
        let f = Fixture::new();
        let (desktop, state, home, peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        let frames = peer.create_replies(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.new",
            &mode,
        );
        let host_view = || {
            let mut view = home.host.snapshot();
            view["homeRouting"] = json!({"activeModeHomeClass":"account"});
            view["currentAppProjectContext"] = state.project_context.view();
            view["configuredProviderReadRevision"] = home
                .host
                .configured_provider_revision(&peer.g, f.project.to_str().unwrap());
            let available = desktop
                .lock()
                .unwrap()
                .endpoint_source_available(home.host_config.as_ref().unwrap());
            view["providerEndpointEdit"] = json!({"available":available});
            view["providerCreate"] = json!({"available":available});
            view
        };
        let write = |name: &str, value: &Value| {
            let tmp = directory.join("output.tmp");
            std::fs::write(&tmp, serde_json::to_vec(value).unwrap()).unwrap();
            std::fs::rename(tmp, directory.join(name)).unwrap();
        };
        write("ready.json", &host_view());
        let mut sequence = 0;
        let mut continued = false;
        loop {
            let path = directory.join(format!("command-{sequence}.json"));
            let deadline = std::time::Instant::now() + std::time::Duration::from_secs(120);
            while !path.exists() {
                assert!(
                    std::time::Instant::now() < deadline,
                    "owned Create fixture deadline"
                );
                std::thread::sleep(std::time::Duration::from_millis(3));
            }
            let command: Value = serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap();
            if command["command"] == "finish" {
                break;
            }
            let args = &command["args"];
            let result = match command["command"].as_str().unwrap() {
                "provider_create_discard" | "provider_endpoint_discard" => {
                    crate::endpoint_checkpoint(&state).map(Value::String)
                }
                "provider_create_offer" => crate::create_offer_result(
                    &state,
                    &args["generation"],
                    args["providerId"].as_str().unwrap(),
                    args["name"].as_str().unwrap(),
                    args["endpoint"].as_str().unwrap(),
                    args["epoch"].as_str().unwrap_or(""),
                ),
                "provider_create_save" => crate::create_save_result(
                    &state,
                    args["token"].as_str().unwrap(),
                    || Ok(()),
                    |_| {
                        if mode == "pre-window-error" {
                            return Err("invented original window failure".into());
                        }
                        Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                            if mode == "cancel-before" {
                                "Leave providers unchanged"
                            } else if mode == "nonexact" {
                                "Add local provider "
                            } else {
                                crate::hosting::provider_create::WRITE_ACTION
                            }
                            .into(),
                        ))
                    },
                    |candidate, _| {
                        if mode == "post-window-error" {
                            return Err(());
                        }
                        Ok(if mode == "cancel-after" {
                            None
                        } else {
                            Some(candidate.accept_checked_current_object())
                        })
                    },
                ),
                "read_configured_providers" => {
                    crate::invalidate_endpoint_edits(&state).unwrap();
                    state.validate_home_source(&home).and_then(|_| {
                        home.host.configured_provider_read_within(
                            &peer.g,
                            f.project.to_str().unwrap(),
                            &state.project_context.view(),
                            std::time::Duration::from_millis(30),
                        )
                    })
                }
                "thread_start" => state
                    .validate_home_source(&home)
                    .and_then(|_| {
                        home.host.provider_admission_read_within(
                            &peer.g,
                            f.project.to_str().unwrap(),
                            args["entryId"].as_str().unwrap_or(""),
                            args["modelProvider"].as_str().unwrap_or(""),
                            args["model"].as_str().unwrap_or(""),
                            std::time::Duration::from_millis(30),
                        )
                    })
                    .and_then(|proof| {
                        home.host.thread_start_with_access_dispatch(
                            &proof,
                            "invented explicit instructions",
                        )
                    })
                    .map(|source| source.evidence()),
                _ => panic!("unallocated Create fixture command"),
            };
            if result.as_ref().is_ok_and(|v| v["state"] == "continued") {
                continued = true;
            }
            peer.create_private_taps();
            f.public_endpoint_records_safe();
            let packet = json!({"response":match result{Ok(value)=>json!({"ok":true,"value":value}),Err(_)=>json!({"ok":false,"error":"Provider Add unavailable; private diagnostics withheld"})},"host":host_view()});
            assert!(!packet.to_string().contains("INVENTED_PRIVATE"));
            write(&format!("response-{sequence}.json"), &packet);
            sequence += 1;
        }
        assert_eq!(
            frames
                .lock()
                .unwrap()
                .iter()
                .filter(|f| f["method"] == "config/batchWrite")
                .count(),
            if continued
                || matches!(
                    mode.as_str(),
                    "cancel-after"
                        | "write-error"
                        | "write-timeout"
                        | "overridden"
                        | "override-reread-timeout"
                        | "post-window-error"
                )
            {
                1
            } else {
                0
            }
        );
        peer.retire_create_fixture();
        drop(frames);
        drop(peer);
        drop(home);
        drop(state);
        drop(desktop);
        if continued {
            let mut setup = f.setup();
            let launch = f.resolve(&mut setup);
            let RootInputs {
                launch,
                data,
                allow_operational,
            } = setup.admit_root(launch, Ok(f.data.clone()));
            assert!(allow_operational);
            let (state, home) =
                crate::freeze_startup_state(launch, Arc::new(Mutex::new(setup)), Value::Null);
            crate::initialize_startup_consumers(
                &state,
                &home,
                data,
                allow_operational,
                true,
                Some(f.data.join("records")),
                None,
                f.shared.clone().map(Some),
            );
            state.validate_home_source(&home).unwrap();
            assert_eq!(home.host_config.as_ref().unwrap().codex_home, h);
            assert_eq!(state.workspace.as_ref(), Some(&f.project));
        }
    }

    #[test]
    fn access_provider_create_original_window_rechecked_after_reread_and_at_commit() {
        for fail_on in [1, 2, 3] {
            let f = Fixture::new();
            let (_, state, home, peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            peer.create_replies(
                f.shared[0].clone(),
                h.join("config.toml"),
                "fixture.new",
                "ok",
            );
            let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
            let view = crate::create_offer_result(
                &state,
                &peer.g,
                "fixture.new",
                "Submitted name",
                "https://example.invalid/new",
                &crate::endpoint_checkpoint(&state).unwrap(),
            )
            .unwrap();
            let checks = std::cell::Cell::new(0);
            let result = crate::create_save_result(
                &state,
                view["token"].as_str().unwrap(),
                || {
                    checks.set(checks.get() + 1);
                    assert_eq!(
                        peer.endpoint_wire_count(),
                        2,
                        "the same-source fresh reread must precede the window recheck"
                    );
                    if checks.get() == fail_on {
                        Err("invented original window destroyed".into())
                    } else {
                        Ok(())
                    }
                },
                |_| {
                    Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                        crate::hosting::provider_create::WRITE_ACTION.into(),
                    ))
                },
                |_, _| panic!("destroyed original window cannot authorize source"),
            )
            .unwrap();
            assert_eq!(result["state"], "refused-not-sent");
            assert_eq!(checks.get(), fail_on);
            assert_eq!(peer.endpoint_wire_count(), 2);
            assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), before);
            state.validate_home_source(&home).unwrap();
            assert!(state.endpoint_edits.lock().unwrap().saving.is_none());
            peer.create_private_taps();
            peer.retire_create_fixture();
        }
    }

    fn create_ack_source_loss(mode: &str, expected: &str) {
        let f = Fixture::new();
        let (desktop, state, home, peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        let frames = peer.create_replies(f.shared[0].clone(), h.join("config.toml"), "fixture.new", mode);
        let profile = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
        let requested = desktop.lock().unwrap().requested.clone();
        let receiving = desktop.lock().unwrap().receiving.as_ref().unwrap().entries().unwrap();
        let bootstrap = state.home_bootstrap.lock().unwrap().as_ref().unwrap().clone();
        let namespaces = state.native_namespaces.lock().unwrap().as_ref().unwrap().clone();
        let attachments = home.attachment_custody.lock().unwrap().as_ref().unwrap().clone();
        let recovery = home.recovery_startup.lock().unwrap().snapshot();
        let selection = home.access_selection.lock().unwrap().as_ref().map(|s| s.canonical_record());
        let view = crate::create_offer_result(&state, &peer.g, "fixture.new", "Submitted name", "https://example.invalid/new", &crate::endpoint_checkpoint(&state).unwrap()).unwrap();
        let result = crate::create_save_result(&state, view["token"].as_str().unwrap(), || Ok(()), |_| Ok(tauri_plugin_dialog::MessageDialogResult::Custom(crate::hosting::provider_create::WRITE_ACTION.into())), |_, _| panic!("lost source cannot reach candidate acceptance")).unwrap();
        // All wire effects and receipt assertions precede the outcome assertion
        // so the original broken implementation proves this exact interval.
        let wire = frames.lock().unwrap();
        assert_eq!(wire.len(), 3, "no post-ACK read or retry: {mode}");
        assert_eq!(wire.iter().filter(|f| f["method"] == "config/batchWrite").count(), 1);
        assert_eq!(wire.iter().filter(|f| f["method"] == "config/read").count(), 2);
        assert!(wire.iter().all(|f| f["method"] != "thread/start"));
        drop(wire);
        assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), profile);
        assert_eq!(desktop.lock().unwrap().requested, requested);
        assert_eq!(desktop.lock().unwrap().receiving.as_ref().unwrap().entries().unwrap(), receiving);
        assert!(state.validate_home_source(&home).is_err(), "unaccepted replacement stays stale");
        assert!(Arc::ptr_eq(&state.homes.lock().unwrap().active(), &home));
        assert!(Arc::ptr_eq(state.home_bootstrap.lock().unwrap().as_ref().unwrap(), &bootstrap));
        assert!(Arc::ptr_eq(state.native_namespaces.lock().unwrap().as_ref().unwrap(), &namespaces));
        assert!(Arc::ptr_eq(home.attachment_custody.lock().unwrap().as_ref().unwrap(), &attachments));
        assert_eq!(home.recovery_startup.lock().unwrap().snapshot(), recovery);
        assert_eq!(home.access_selection.lock().unwrap().as_ref().map(|s| s.canonical_record()), selection);
        assert_eq!(state.workspace.as_ref(), Some(&f.project));
        assert!(state.endpoint_edits.lock().unwrap().saving.is_none());
        assert!(crate::create_save_result(&state, view["token"].as_str().unwrap(), || Ok(()), |_| panic!("spent token"), |_, _| panic!("spent token")).is_err());
        peer.create_private_taps();
        f.public_endpoint_records_safe();
        peer.retire_create_fixture();
        assert_eq!(result["state"], expected, "{mode}");
    }
    #[test]
    fn access_provider_create_ack_close_retains_fact() { create_ack_source_loss("ack-close", "write-observed-source-unconfirmed"); }
    #[test]
    fn access_provider_create_ack_detach_retains_fact() { create_ack_source_loss("ack-detach", "write-observed-source-unconfirmed"); }
    #[test]
    fn access_provider_create_ack_override_close_retains_fact() { create_ack_source_loss("override-ack-close", "overridden"); }
    #[test]
    fn access_provider_create_ack_override_detach_retains_fact() { create_ack_source_loss("override-ack-detach", "overridden"); }
    #[test]
    fn access_provider_create_ack_unestablished_is_not_promoted() {
        for mode in ["ack-after-close", "ack-after-detach", "malformed-ack", "unmatched-ack", "wrong-target-ack"] {
            create_ack_source_loss(mode, "unknown");
        }
    }

    #[test]
    fn access_provider_create_notification_metadata_is_private() {
        let f = Fixture::new();
        let (desktop, state, home, mut peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        peer.create_replies(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.new",
            "notification-reflection",
        );
        let view = crate::create_offer_result(
            &state,
            &peer.g,
            "fixture.new",
            "Submitted name",
            "https://example.invalid/new",
            &crate::endpoint_checkpoint(&state).unwrap(),
        )
        .unwrap();
        assert_eq!(
            crate::create_save_result(
                &state,
                view["token"].as_str().unwrap(),
                || Ok(()),
                |_| Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                    crate::hosting::provider_create::WRITE_ACTION.into()
                )),
                |candidate, _| Ok(Some(candidate.accept_checked_current_object()))
            )
            .unwrap()["state"],
            "continued"
        );
        assert!(desktop.lock().unwrap().requested.is_some());
        peer.create_diagnostic_and_collision_probe();
        peer.create_private_taps();
        f.public_endpoint_records_safe();
        peer.retire_create_fixture();
    }

    #[test]
    fn access_provider_create_wait_drift_and_expiry_cannot_write_or_promote() {
        for mode in [
            "pre-epoch",
            "pre-generation",
            "pre-profile",
            "pre-pending",
            "pre-link",
            "pre-target",
            "pre-custody",
            "pre-endpoint",
            "post-epoch",
            "post-profile",
            "post-target",
            "post-window",
        ] {
            let f = Fixture::new();
            let (desktop, state, home, peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            peer.create_replies(
                f.shared[0].clone(),
                h.join("config.toml"),
                "fixture.new",
                "ok",
            );
            let view = crate::create_offer_result(
                &state,
                &peer.g,
                "fixture.new",
                "Submitted name",
                "https://example.invalid/new",
                &crate::endpoint_checkpoint(&state).unwrap(),
            )
            .unwrap();
            let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
            let mutate_profile = || {
                write_profile(
                    &f.data.join(PROFILE),
                    &read_profile(&f.data.join(PROFILE)).unwrap(),
                )
                .unwrap()
            };
            let mut baseline_after = before.clone();
            let result = crate::create_save_result(
                &state,
                view["token"].as_str().unwrap(),
                || Ok(()),
                |_| {
                    match mode {
                        "pre-epoch" => crate::invalidate_endpoint_edits(&state).unwrap(),
                        "pre-generation" => peer.supersede_config_generation(),
                        "pre-profile" => mutate_profile(),
                        "pre-pending" => {
                            let preview = desktop.lock().unwrap().preview_project(None).unwrap();
                            desktop
                                .lock()
                                .unwrap()
                                .prepare_and_save(preview["token"].as_str().unwrap())
                                .unwrap();
                            baseline_after = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
                        }
                        "pre-link" => {
                            std::fs::remove_file(h.join("config.toml")).unwrap();
                            std::os::unix::fs::symlink(&f.shared[0], h.join("config.toml"))
                                .unwrap();
                        }
                        "pre-target" => f.replace_config(),
                        "pre-custody" => {
                            std::fs::rename(&h, f.root.join("old-held-home")).unwrap();
                            std::fs::create_dir(&h).unwrap();
                        }
                        "pre-endpoint" => {
                            assert!(crate::endpoint_offer_result(
                                &state,
                                &peer.g,
                                "fixture.dot",
                                "https://example.invalid/new",
                                &crate::endpoint_checkpoint(&state).unwrap()
                            )
                            .is_err());
                        }
                        _ => {}
                    }
                    Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                        crate::hosting::provider_create::WRITE_ACTION.into(),
                    ))
                },
                |candidate, _| {
                    match mode {
                        "post-epoch" => crate::invalidate_endpoint_edits(&state).unwrap(),
                        "post-profile" => mutate_profile(),
                        "post-target" => f.replace_config(),
                        "post-window" => return Err(()),
                        _ => panic!("{mode} reached acceptance"),
                    }
                    Ok(Some(candidate.accept_checked_current_object()))
                },
            );
            if mode.starts_with("pre-") {
                assert!(result.is_err(), "{mode}");
                assert_eq!(peer.endpoint_wire_count(), 1);
            } else {
                assert_eq!(
                    result.unwrap()["state"],
                    "write-observed-source-unconfirmed",
                    "{mode}"
                );
                assert_eq!(peer.endpoint_wire_count(), 4);
            }
            // An intentional competing pending plan is preserved, never overwritten.
            assert_eq!(
                read_profile_bytes(&f.data.join(PROFILE)).unwrap().0,
                baseline_after.0
            );
            assert!(state.endpoint_edits.lock().unwrap().saving.is_none());
            assert!(Arc::ptr_eq(&state.homes.lock().unwrap().active(), &home));
            peer.create_private_taps();
            f.public_endpoint_records_safe();
            peer.retire_create_fixture();
        }
        let f = Fixture::new();
        let (_, state, home, peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        peer.create_replies(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.new",
            "ok",
        );
        let view = crate::create_offer_result(
            &state,
            &peer.g,
            "fixture.new",
            "Submitted name",
            "https://example.invalid/new",
            &crate::endpoint_checkpoint(&state).unwrap(),
        )
        .unwrap();
        let token = view["token"].as_str().unwrap();
        crate::hosting::provider_endpoint::expire_create_offer(
            &state.endpoint_edits,
            token,
            std::time::Duration::from_millis(10),
        )
        .unwrap();
        let deadline = std::time::Instant::now() + std::time::Duration::from_secs(1);
        while state.endpoint_edits.lock().unwrap().create_offer.is_some() {
            assert!(std::time::Instant::now() < deadline);
            std::thread::sleep(std::time::Duration::from_millis(1));
        }
        assert!(crate::create_save_result(
            &state,
            token,
            || Ok(()),
            |_| panic!("expired"),
            |_, _| panic!("expired")
        )
        .is_err());
        assert_eq!(peer.endpoint_wire_count(), 1);
        peer.retire_create_fixture();
    }

    #[test]
    fn access_provider_create_collision_schema_version_and_reported_defaults_fail_closed() {
        for mode in [
            "user-collision",
            "effective-collision",
            "missing-user-map",
            "malformed-effective-map",
            "late-collision",
            "stale-version",
            "missing-default",
            "native-name-drift",
            "other-settings",
        ] {
            let f = Fixture::new();
            let (desktop, state, home, peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            peer.create_replies(
                f.shared[0].clone(),
                h.join("config.toml"),
                "fixture.new",
                mode,
            );
            let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
            let view = crate::create_offer_result(
                &state,
                &peer.g,
                "fixture.new",
                "Submitted name",
                "https://example.invalid/new",
                &crate::endpoint_checkpoint(&state).unwrap(),
            );
            if matches!(
                mode,
                "user-collision"
                    | "effective-collision"
                    | "missing-user-map"
                    | "malformed-effective-map"
            ) {
                assert!(view.is_err(), "{mode}");
                assert_eq!(peer.endpoint_wire_count(), 1);
            } else {
                let view = view.unwrap();
                let result = crate::create_save_result(
                    &state,
                    view["token"].as_str().unwrap(),
                    || Ok(()),
                    |_| {
                        Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                            crate::hosting::provider_create::WRITE_ACTION.into(),
                        ))
                    },
                    |_, _| panic!("{mode} cannot reach acceptance"),
                );
                if matches!(mode, "late-collision" | "stale-version") {
                    assert!(result.is_err(), "{mode}");
                    assert_eq!(peer.endpoint_wire_count(), 2);
                } else {
                    assert_eq!(
                        result.unwrap()["state"],
                        "write-observed-source-unconfirmed",
                        "{mode}"
                    );
                    assert_eq!(peer.endpoint_wire_count(), 4);
                    assert!(state.validate_home_source(&home).is_err());
                }
            }
            assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), before);
            assert!(desktop.lock().unwrap().requested.is_some());
            peer.create_private_taps();
            f.public_endpoint_records_safe();
            peer.retire_create_fixture();
        }
    }

    #[test]
    fn access_provider_create_draft_bounds_reserved_id_and_cross_intent_tokens_refuse() {
        for (id, name, url) in [
            ("openai", "Name", "https://example.invalid/new"),
            ("1bad", "Name", "https://example.invalid/new"),
            ("fixture.new", "   ", "https://example.invalid/new"),
            ("fixture.new", "line\nname", "https://example.invalid/new"),
            ("fixture.new", "é", "https://example.invalid/new"),
            (
                "fixture.new",
                "Name",
                "https://user:private@example.invalid/new",
            ),
            ("fixture.new", "Name", "https://example.invalid/%61"),
        ] {
            let f = Fixture::new();
            let (_, state, home, peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            peer.create_replies(
                f.shared[0].clone(),
                h.join("config.toml"),
                "fixture.new",
                "ok",
            );
            assert!(crate::create_offer_result(
                &state,
                &peer.g,
                id,
                name,
                url,
                &crate::endpoint_checkpoint(&state).unwrap()
            )
            .is_err());
            assert_eq!(peer.endpoint_wire_count(), 1);
            state.validate_home_source(&home).unwrap();
            peer.create_private_taps();
            peer.retire_create_fixture();
        }
        let f = Fixture::new();
        let (_, state, home, peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        peer.create_replies(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.new",
            "ok",
        );
        let view = crate::create_offer_result(
            &state,
            &peer.g,
            "fixture.new",
            "Submitted name",
            "https://example.invalid/new",
            &crate::endpoint_checkpoint(&state).unwrap(),
        )
        .unwrap();
        let token = view["token"].as_str().unwrap();
        assert!(crate::endpoint_save_result(
            &state,
            token,
            |_| panic!("wrong intent"),
            |_, _| panic!("wrong intent")
        )
        .is_err());
        assert_eq!(
            crate::create_save_result(
                &state,
                token,
                || Ok(()),
                |_| Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                    crate::hosting::provider_endpoint::WRITE_ACTION.into()
                )),
                |_, _| panic!("nonexact Add action")
            )
            .unwrap()["state"],
            "not-sent"
        );
        assert_eq!(peer.endpoint_wire_count(), 1);
        peer.retire_create_fixture();
        let f = Fixture::new();
        let (_, state, home, peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        peer.endpoint_replies(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.dot",
            "https://example.invalid/new",
        );
        let view = crate::endpoint_offer_result(
            &state,
            &peer.g,
            "fixture.dot",
            "https://example.invalid/new",
            &crate::endpoint_checkpoint(&state).unwrap(),
        )
        .unwrap();
        assert!(crate::create_save_result(
            &state,
            view["token"].as_str().unwrap(),
            || Ok(()),
            |_| panic!("wrong intent"),
            |_, _| panic!("wrong intent")
        )
        .is_err());
        assert_eq!(peer.endpoint_wire_count(), 1);
    }

    #[test]
    fn access_provider_create_private_draft_reflection_and_unknown_auth_refuse() {
        for mode in [
            "name-reflection",
            "id-reflection",
            "url-reflection",
            "unknown-auth",
        ] {
            let f = Fixture::new();
            let (desktop, state, home, peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            peer.create_replies(
                f.shared[0].clone(),
                h.join("config.toml"),
                "fixture.new",
                mode,
            );
            let old = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
            let id = if mode == "id-reflection" {
                "INVENTED_PRIVATE_PROVIDER_CANARY_481"
            } else {
                "fixture.new"
            };
            let name = if mode == "name-reflection" {
                "INVENTED_PRIVATE_PROVIDER_CANARY_481"
            } else {
                "Explicit new name"
            };
            let url = if mode == "url-reflection" {
                "https://example.invalid/INVENTED_PRIVATE_PROVIDER_CANARY_481"
            } else {
                "https://example.invalid/new"
            };
            let offer = crate::create_offer_result(
                &state,
                &peer.g,
                id,
                name,
                url,
                &crate::endpoint_checkpoint(&state).unwrap(),
            );
            if mode == "unknown-auth" {
                let view = offer.unwrap();
                let result = crate::create_save_result(
                    &state,
                    view["token"].as_str().unwrap(),
                    || Ok(()),
                    |_| {
                        Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                            crate::hosting::provider_create::WRITE_ACTION.into(),
                        ))
                    },
                    |_, _| panic!("unknown auth cannot reach acceptance"),
                )
                .unwrap();
                assert_eq!(result["state"], "write-observed-source-unconfirmed");
                assert!(state.validate_home_source(&home).is_err());
                assert_eq!(peer.endpoint_wire_count(), 4);
            } else {
                assert!(offer.is_err());
                assert!(!offer.unwrap_err().contains("INVENTED_PRIVATE"));
                assert_eq!(peer.endpoint_wire_count(), 1);
                state.validate_home_source(&home).unwrap();
            }
            assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), old);
            assert!(desktop.lock().unwrap().requested.is_some());
            peer.create_private_taps();
            f.public_endpoint_records_safe();
            peer.retire_create_fixture();
        }
    }

    #[test]
    fn access_provider_create_private_write_readmission_and_fresh_consumers() {
        for receiving_alias in [false, true] {
            let f = Fixture::new();
            let (desktop, state, home, peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            let layer = if receiving_alias {
                h.join("config.toml")
            } else {
                f.shared[0].clone()
            };
            let frames =
                peer.create_replies(f.shared[0].clone(), layer.clone(), "fixture.new", "ok");
            let before = read_profile(&f.data.join(PROFILE)).unwrap();
            let receiving = desktop
                .lock()
                .unwrap()
                .receiving
                .as_ref()
                .unwrap()
                .entries()
                .unwrap();
            let bootstrap = state
                .home_bootstrap
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let namespaces = state
                .native_namespaces
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let custody = home
                .attachment_custody
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let recovery = home.recovery_startup.lock().unwrap().snapshot();
            let name = "Person's \\\"quoted\\\" name \\ exact";
            let view = crate::create_offer_result(
                &state,
                &peer.g,
                "fixture.new",
                name,
                "https://example.invalid/new",
                &crate::endpoint_checkpoint(&state).unwrap(),
            )
            .unwrap();
            assert_eq!(view["submittedName"], name);
            assert!(!view.to_string().contains("INVENTED_PRIVATE"));
            let result = crate::create_save_result(
                &state,
                view["token"].as_str().unwrap(),
                || Ok(()),
                |review| {
                    assert_eq!(review, &view);
                    assert!(desktop.try_lock().is_ok());
                    Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                        crate::hosting::provider_create::WRITE_ACTION.into(),
                    ))
                },
                |candidate, review| {
                    assert_eq!(review["submittedName"], name);
                    assert_eq!(
                        candidate.private_reading().0["layers"][0]["name"]["file"],
                        json!(layer)
                    );
                    assert!(
                        state.validate_home_source(&home).is_err(),
                        "ACK cannot continue old source"
                    );
                    assert!(desktop.try_lock().is_ok());
                    Ok(Some(candidate.accept_checked_current_object()))
                },
            )
            .unwrap();
            assert_eq!(result["state"], "continued");
            state.validate_home_source(&home).unwrap();
            let observed = home
                .host
                .configured_provider_read_within(
                    &peer.g,
                    f.project.to_str().unwrap(),
                    &state.project_context.view(),
                    std::time::Duration::from_millis(30),
                )
                .unwrap();
            assert_eq!(observed["rows"].as_array().unwrap().len(), 1);
            assert_eq!(observed["rows"][0]["id"], "fixture.new");
            assert_eq!(observed["rows"][0]["label"], "Configured local provider");
            assert!(!observed.to_string().contains(name));
            let wire = frames.lock().unwrap();
            assert_eq!(wire.len(), 5);
            assert_eq!(
                wire.iter()
                    .filter(|f| f["method"] == "config/batchWrite")
                    .count(),
                1
            );
            assert!(wire
                .iter()
                .all(|f| f["method"] == "config/read" || f["method"] == "config/batchWrite"));
            assert_eq!(wire[2]["params"]["edits"][0]["value"]["name"], name);
            drop(wire);
            assert!(Arc::ptr_eq(&state.homes.lock().unwrap().active(), &home));
            assert_eq!(state.workspace.as_ref(), Some(&f.project));
            assert!(Arc::ptr_eq(
                state.home_bootstrap.lock().unwrap().as_ref().unwrap(),
                &bootstrap
            ));
            assert!(Arc::ptr_eq(
                state.native_namespaces.lock().unwrap().as_ref().unwrap(),
                &namespaces
            ));
            assert!(Arc::ptr_eq(
                home.attachment_custody.lock().unwrap().as_ref().unwrap(),
                &custody
            ));
            assert_eq!(home.recovery_startup.lock().unwrap().snapshot(), recovery);
            assert_eq!(
                desktop
                    .lock()
                    .unwrap()
                    .receiving
                    .as_ref()
                    .unwrap()
                    .entries()
                    .unwrap(),
                receiving
            );
            let mut expected = before;
            let current = read_profile(&f.data.join(PROFILE)).unwrap();
            expected.shared[0] = current.shared[0].clone();
            assert_eq!(expected, current);
            let project = desktop
                .lock()
                .unwrap()
                .preview_project(Some(f.project.clone()))
                .unwrap();
            assert_eq!(project["accountHome"], json!(h));
            desktop
                .lock()
                .unwrap()
                .prepare_and_save(project["token"].as_str().unwrap())
                .unwrap();
            peer.create_private_taps();
            f.public_endpoint_records_safe();
            peer.retire_create_fixture();
            drop(frames);
            drop(peer);
            drop(home);
            drop(state);
            drop(desktop);
            let mut setup = f.setup();
            let launch = f.resolve(&mut setup);
            let RootInputs {
                launch,
                data,
                allow_operational,
            } = setup.admit_root(launch, Ok(f.data.clone()));
            assert!(allow_operational);
            let (state, home) =
                crate::freeze_startup_state(launch, Arc::new(Mutex::new(setup)), Value::Null);
            crate::initialize_startup_consumers(
                &state,
                &home,
                data,
                allow_operational,
                true,
                Some(f.data.join("records")),
                None,
                f.shared.clone().map(Some),
            );
            state.validate_home_source(&home).unwrap();
            assert_eq!(home.host_config.as_ref().unwrap().codex_home, h);
            assert_eq!(state.workspace.as_ref(), Some(&f.project));
        }
    }
    #[test]
    fn access_provider_endpoint_delayed_offer_cannot_overwrite_newer_input_checkpoint() {
        let f = Fixture::new();
        let (desktop, state, home, peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        peer.endpoint_replies(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.dot",
            "https://example.invalid/new",
        );
        let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
        let old = crate::endpoint_checkpoint(&state).unwrap();
        let newer = crate::endpoint_checkpoint(&state).unwrap();
        let view = crate::endpoint_offer_result(
            &state,
            &peer.g,
            "fixture.dot",
            "https://example.invalid/new",
            &newer,
        )
        .unwrap();
        let epoch = state.endpoint_edits.lock().unwrap().epoch.clone();
        let reads = peer.endpoint_wire_count();
        assert!(crate::endpoint_offer_result(
            &state,
            &peer.g,
            "fixture.dot",
            "https://example.invalid/old",
            &old
        )
        .is_err());
        let controller = state.endpoint_edits.lock().unwrap();
        assert_eq!(controller.epoch, epoch);
        assert_eq!(controller.offer.as_ref().unwrap().view(), view);
        drop(controller);
        assert_eq!(peer.endpoint_wire_count(), reads);
        assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), before);
        assert!(Arc::ptr_eq(&state.homes.lock().unwrap().active(), &home));
        state.validate_home_source(&home).unwrap();
        assert!(desktop.lock().unwrap().requested.is_some());
        peer.endpoint_private_taps();
        f.public_endpoint_records_safe();
    }
    #[test]
    fn access_provider_endpoint_private_unused_offer_expires_without_write_or_replay() {
        let f = Fixture::new();
        let (desktop, state, home, peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        peer.endpoint_replies(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.dot",
            "https://example.invalid/new",
        );
        let view = crate::endpoint_offer_result(
            &state,
            &peer.g,
            "fixture.dot",
            "https://example.invalid/new",
            &crate::endpoint_checkpoint(&state).unwrap(),
        )
        .unwrap();
        let token = view["token"].as_str().unwrap();
        crate::hosting::provider_endpoint::expire_offer(
            &state.endpoint_edits,
            token,
            std::time::Duration::from_millis(10),
        )
        .unwrap();
        let deadline = std::time::Instant::now() + std::time::Duration::from_secs(1);
        while state.endpoint_edits.lock().unwrap().offer.is_some() {
            assert!(std::time::Instant::now() < deadline);
            std::thread::sleep(std::time::Duration::from_millis(1));
        }
        assert!(crate::endpoint_save_result(
            &state,
            token,
            |_| panic!("expired offer"),
            |_, _| panic!("expired offer")
        )
        .is_err());
        assert!(state.endpoint_edits.lock().unwrap().saving.is_none());
        assert_eq!(peer.endpoint_wire_count(), 1);
        state.validate_home_source(&home).unwrap();
        assert!(desktop.lock().unwrap().requested.is_some());
        peer.endpoint_private_taps();
        f.public_endpoint_records_safe();
    }

    #[test]
    fn access_provider_endpoint_offer_scope_and_both_decision_supersession_refuse() {
        for mode in [
            "input",
            "new-read",
            "new-offer",
            "pre-window-error",
            "post-window-error",
            "post-input",
            "post-target",
            "session-only",
            "definition-mismatch",
            "sibling-settings",
            "reread-version",
            "reflected-draft",
        ] {
            let f = Fixture::new();
            let (desktop, state, home, mut peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            peer.endpoint_replies_mode(
                f.shared[0].clone(),
                h.join("config.toml"),
                "fixture.dot",
                "https://example.invalid/new",
                mode,
            );
            let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
            let original = desktop.lock().unwrap().requested.clone().unwrap();
            let endpoint = if mode == "reflected-draft" {
                "https://example.invalid/INVENTED_PRIVATE_PROVIDER_CANARY_481"
            } else {
                "https://example.invalid/new"
            };
            let offered = crate::endpoint_offer_result(
                &state, &peer.g, "fixture.dot", endpoint,
                &crate::endpoint_checkpoint(&state).unwrap(),
            );
            if matches!(
                mode,
                "session-only" | "definition-mismatch" | "reflected-draft"
            ) {
                assert!(offered.is_err(), "{mode}");
                assert!(state.endpoint_edits.lock().unwrap().offer.is_none());
            } else {
                let token = offered.unwrap()["token"].as_str().unwrap().to_owned();
                let before_called = std::cell::Cell::new(false);
                let result = crate::endpoint_save_result(
                    &state,
                    &token,
                    |_| {
                        before_called.set(true);
                        match mode {
                            "input" => crate::invalidate_endpoint_edits(&state).unwrap(),
                            "new-read" => {
                                home.host
                                    .configured_provider_read_within(
                                        &peer.g,
                                        f.project.to_str().unwrap(),
                                        &state.project_context.view(),
                                        std::time::Duration::from_millis(30),
                                    )
                                    .unwrap();
                            }
                            "new-offer" => {
                                assert!(crate::endpoint_offer_result(
                                    &state,
                                    &peer.g,
                                    "fixture.dot",
                                    "https://example.invalid/other",
                                    &crate::endpoint_checkpoint(&state).unwrap(),
                                )
                                .is_err());
                            }
                            "pre-window-error" => {
                                return Err("invented original-window failure".into())
                            }
                            _ => {}
                        }
                        Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                            crate::hosting::provider_endpoint::WRITE_ACTION.into(),
                        ))
                    },
                    |candidate, _| {
                        match mode {
                            "post-window-error" => return Err(()),
                            "post-input" => crate::invalidate_endpoint_edits(&state).unwrap(),
                            "post-target" => f.replace_config(),
                            "sibling-settings" | "reread-version" => {
                                panic!("different reread cannot reach source decision")
                            }
                            _ => {}
                        }
                        Ok(Some(candidate.accept_checked_current_object()))
                    },
                );
                assert!(before_called.get(), "{mode}: actual first decision was not reached");
                if matches!(
                    mode,
                    "input" | "new-read" | "new-offer" | "pre-window-error"
                ) {
                    assert!(result.is_err(), "{mode}");
                } else {
                    assert_eq!(
                        result.unwrap()["state"],
                        "write-observed-source-unconfirmed",
                        "{mode}"
                    );
                }
                assert!(state.endpoint_edits.lock().unwrap().saving.is_none());
                assert!(crate::endpoint_save_result(
                    &state,
                    &token,
                    |_| panic!("spent token"),
                    |_, _| panic!("spent token")
                )
                .is_err());
            }
            assert_eq!(
                read_profile_bytes(&f.data.join(PROFILE)).unwrap(),
                before,
                "{mode}"
            );
            assert_eq!(
                desktop.lock().unwrap().requested.as_ref().unwrap(),
                &original
            );
            let count = peer.endpoint_wire_count();
            for _ in 0..count {
                let frame = peer.continuation_frame();
                assert!(matches!(
                    frame["method"].as_str(),
                    Some("config/read" | "config/batchWrite")
                ));
            }
            peer.endpoint_private_taps();
            f.public_endpoint_records_safe();
        }
    }

    #[test]
    fn access_provider_endpoint_mounted_join() {
        let Ok(directory) = std::env::var("CHIRALITY_ENDPOINT_JOIN") else {
            return;
        };
        let directory = PathBuf::from(directory);
        let mode = std::env::var("CHIRALITY_ENDPOINT_MODE").unwrap_or_else(|_| "ok".into());
        let f = Fixture::new();
        let (desktop, state, home, mut peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        peer.endpoint_replies_mode(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.dot",
            "https://example.invalid/new",
            &mode,
        );
        let generation = peer.g.clone();
        let host_view = || {
            let mut view = home.host.snapshot();
            view["homeRouting"] = state.homes.lock().unwrap().snapshot();
            view["providerEndpointEdit"] = json!({"available":desktop.lock().unwrap().endpoint_source_available(home.host_config.as_ref().unwrap())});
            view["currentAppProjectContext"] = state.project_context.view();
            view["configuredProviderReadRevision"] = home
                .host
                .configured_provider_revision(&generation, f.project.to_str().unwrap());
            view
        };
        let write = |name: &str, value: &Value| {
            assert!(!value.to_string().contains("INVENTED_PRIVATE"));
            let tmp = directory.join("output.tmp");
            std::fs::write(&tmp, serde_json::to_vec(value).unwrap()).unwrap();
            std::fs::rename(tmp, directory.join(name)).unwrap();
        };
        write("ready.json", &host_view());
        let mut sequence = 0;
        let mut continued = false;
        loop {
            let path = directory.join(format!("command-{sequence}.json"));
            let deadline = std::time::Instant::now() + std::time::Duration::from_secs(120);
            while !path.exists() {
                assert!(
                    std::time::Instant::now() < deadline,
                    "mounted endpoint fixture deadline"
                );
                std::thread::sleep(std::time::Duration::from_millis(3));
            }
            let command: Value = serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap();
            let args = &command["args"];
            if command["command"] == "finish" {
                break;
            }
            let result = match command["command"].as_str().unwrap() {
                "read_configured_providers" => {
                    crate::invalidate_endpoint_edits(&state).unwrap();
                    home.host.configured_provider_read_within(
                        &peer.g,
                        f.project.to_str().unwrap(),
                        &state.project_context.view(),
                        std::time::Duration::from_millis(30),
                    )
                }
                "provider_endpoint_offer" => crate::endpoint_offer_result(
                    &state,
                    &args["generation"],
                    args["providerId"].as_str().unwrap(),
                    args["endpoint"].as_str().unwrap(),
                    args["epoch"].as_str().unwrap_or(""),
                ),
                "provider_endpoint_discard" => {
                    crate::endpoint_checkpoint(&state).map(Value::String)
                }
                "provider_endpoint_save" => crate::endpoint_save_result(
                    &state,
                    args["token"].as_str().unwrap(),
                    |_| {
                        Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                            if mode == "cancel-before" {
                                "Leave endpoint unchanged"
                            } else {
                                crate::hosting::provider_endpoint::WRITE_ACTION
                            }
                            .into(),
                        ))
                    },
                    |candidate, _| {
                        if mode == "cancel-after" {
                            Ok(None)
                        } else {
                            Ok(Some(candidate.accept_checked_current_object()))
                        }
                    },
                ),
                "thread_start" => {
                    crate::invalidate_endpoint_edits(&state).unwrap();
                    if mode == "start-credentialed" {
                        peer.endpoint_credentialed_start();
                    }
                    state
                        .validate_home_source(&home)
                        .and_then(|_| {
                            home.host.provider_admission_read_within(
                                &peer.g,
                                f.project.to_str().unwrap(),
                                args["entryId"].as_str().unwrap(),
                                args["modelProvider"].as_str().unwrap(),
                                args["model"].as_str().unwrap(),
                                std::time::Duration::from_millis(30),
                            )
                        })
                        .and_then(|proof| {
                            home.host.thread_start_with_access_dispatch(
                                &proof,
                                "invented explicit instruction",
                            )
                        })
                        .map(|source| source.evidence())
                }
                _ => panic!("unallocated mounted command"),
            };
            if let Ok(ref value) = result {
                if value["state"] == "continued" {
                    continued = true;
                }
            }
            peer.endpoint_private_taps();
            f.public_endpoint_records_safe();
            let packet = json!({"response":match result{Ok(value)=>json!({"ok":true,"value":value}),Err(_)=>json!({"ok":false,"error":"Endpoint operation unavailable; private diagnostics withheld"})},"host":host_view()});
            write(&format!("response-{sequence}.json"), &packet);
            sequence += 1;
        }
        // Assert actual wire methods privately; raw native versions never enter
        // the mounted/public packet or its evidence.
        let count = peer.endpoint_wire_count();
        let mut seen = 0;
        while seen < count {
            let frame = peer.continuation_frame();
            if frame.get("method").is_none() {
                assert!(frame["result"]["currentTimeAt"].as_u64().is_some());
                continue;
            }
            assert!(matches!(
                frame["method"].as_str(),
                Some("config/read" | "config/batchWrite" | "thread/start")
            ));
            seen += 1;
        }
        drop(peer);
        drop(home);
        drop(state);
        drop(desktop);
        if continued {
            let mut setup = f.setup();
            let launch = f.resolve(&mut setup);
            let RootInputs {
                launch,
                data,
                allow_operational,
            } = setup.admit_root(launch, Ok(f.data.clone()));
            assert!(allow_operational);
            let (state, home) =
                crate::freeze_startup_state(launch, Arc::new(Mutex::new(setup)), Value::Null);
            crate::initialize_startup_consumers(
                &state,
                &home,
                data,
                allow_operational,
                true,
                Some(f.data.join("records")),
                None,
                f.shared.clone().map(Some),
            );
            state.validate_home_source(&home).unwrap();
            assert_eq!(home.host_config.as_ref().unwrap().codex_home, h);
            assert_eq!(state.workspace.as_ref(), Some(&f.project));
        }
    }

    #[test]
    fn access_provider_endpoint_private_outcomes_keep_effects_unknown_and_id_spaces_distinct() {
        for mode in [
            "error",
            "timeout",
            "closed",
            "override",
            "collision",
            "cancel-before",
            "cancel-after",
        ] {
            let f = Fixture::new();
            let (desktop, state, home, mut peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            peer.endpoint_replies_mode(
                f.shared[0].clone(),
                h.join("config.toml"),
                "fixture.dot",
                "https://example.invalid/new",
                mode,
            );
            let profile = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
            let old = desktop.lock().unwrap().requested.clone().unwrap();
            let offer = crate::hosting::provider_endpoint::offer(
                &state,
                "fixture.dot",
                "https://example.invalid/new",
            )
            .unwrap();
            let outcome = crate::hosting::provider_endpoint::save(
                &state,
                offer,
                |_| {
                    Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                        if mode == "cancel-before" {
                            "Leave endpoint unchanged"
                        } else {
                            crate::hosting::provider_endpoint::WRITE_ACTION
                        }
                        .into(),
                    ))
                },
                |candidate, _| {
                    if mode == "collision" {
                        Ok(Some(candidate.accept_checked_current_object()))
                    } else if mode == "cancel-after" {
                        Ok(None)
                    } else {
                        panic!("{mode} cannot authorize postwrite continuation")
                    }
                },
            )
            .unwrap();
            let expected = match mode {
                "collision" => "continued",
                "override" => "overridden",
                "cancel-before" => "not-sent",
                "cancel-after" => "write-observed-source-unconfirmed",
                _ => "unknown",
            };
            assert_eq!(outcome["state"], expected, "{mode}");
            assert_eq!(peer.continuation_frame()["method"], "config/read");
            if mode != "cancel-before" {
                let write = peer.continuation_frame();
                assert_eq!(write["method"], "config/batchWrite");
                if mode == "collision" {
                    let answer = peer.continuation_frame();
                    assert_eq!(answer["id"], write["id"]);
                    assert!(answer["result"]["currentTimeAt"].as_u64().is_some());
                }
            }
            if matches!(mode, "override" | "collision" | "cancel-after") {
                assert_eq!(peer.continuation_frame()["method"], "config/read");
            }
            if matches!(mode, "timeout" | "closed") {
                peer.endpoint_late_reply();
            }
            if mode != "collision" {
                assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), profile);
                assert_eq!(desktop.lock().unwrap().requested.as_ref().unwrap(), &old);
            }
            if mode == "cancel-before" {
                state.validate_home_source(&home).unwrap();
            } else if mode != "collision" {
                assert!(state.validate_home_source(&home).is_err());
            }
            assert!(!outcome.to_string().contains("INVENTED_PRIVATE"));
            peer.endpoint_private_taps();
            f.public_endpoint_records_safe();
        }
    }

    #[test]
    fn access_provider_endpoint_observed_ack_survives_target_or_receiving_loss() {
        for mode in [
            "ack-link-missing",
            "ack-target-missing",
            "ack-link-replaced",
            "override-link-missing",
        ] {
            endpoint_post_ack_failure(
                mode,
                if mode.starts_with("override-") {
                    "overridden"
                } else {
                    "write-observed-source-unconfirmed"
                },
                2,
            );
        }
    }

    #[test]
    fn access_provider_endpoint_observed_override_survives_failed_private_reread() {
        for mode in ["override-reread-timeout", "override-reread-error"] {
            endpoint_post_ack_failure(mode, "overridden", 3);
        }
    }

    #[test]
    fn access_provider_endpoint_unvalidated_ack_remains_unknown() {
        for mode in ["unmatched-ack", "invalid-ack-target", "invalid-ack-shape"] {
            endpoint_post_ack_failure(mode, "unknown", 2);
        }
    }

    fn endpoint_post_ack_failure(mode: &str, expected: &str, requests: usize) {
        let f = Fixture::new();
        let (desktop, state, home, mut peer) = f.continuation();
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        peer.endpoint_replies_mode(
            f.shared[0].clone(),
            h.join("config.toml"),
            "fixture.dot",
            "https://example.invalid/new",
            mode,
        );
        let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
        let original = desktop.lock().unwrap().requested.clone().unwrap();
        let bootstrap = state
            .home_bootstrap
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .clone();
        let namespaces = state
            .native_namespaces
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .clone();
        let custody = home
            .attachment_custody
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .clone();
        let recovery = home.recovery_startup.lock().unwrap().snapshot();
        let view = crate::endpoint_offer_result(
            &state,
            &peer.g,
            "fixture.dot",
            "https://example.invalid/new",
            &crate::endpoint_checkpoint(&state).unwrap(),
        )
        .unwrap();
        let token = view["token"].as_str().unwrap();
        let decisions = std::cell::Cell::new(0);
        let result = crate::endpoint_save_result(
            &state,
            token,
            |_| {
                decisions.set(decisions.get() + 1);
                Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                    crate::hosting::provider_endpoint::WRITE_ACTION.into(),
                ))
            },
            |_, _| panic!("{mode}: failed post-ACK source cannot reach acceptance"),
        );
        assert!(
            result.is_ok(),
            "{mode}: validated write facts escaped as a generic command error: {result:?}"
        );
        let outcome = result.unwrap();
        assert_eq!(
            outcome["state"], expected,
            "{mode}: validated write/override fact lost"
        );
        assert_eq!(decisions.get(), 1);
        assert!(state.endpoint_edits.lock().unwrap().saving.is_none());
        assert!(crate::endpoint_save_result(
            &state,
            token,
            |_| panic!("spent token"),
            |_, _| panic!("spent token")
        )
        .is_err());
        assert_eq!(
            peer.endpoint_wire_count(),
            requests,
            "{mode}: unexpected retry/read/write"
        );
        for position in 0..requests {
            assert_eq!(
                peer.continuation_frame()["method"],
                if position == 1 {
                    "config/batchWrite"
                } else {
                    "config/read"
                }
            );
        }
        assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), before);
        assert_eq!(
            desktop.lock().unwrap().requested.as_ref().unwrap(),
            &original
        );
        assert!(state.validate_home_source(&home).is_err());
        assert!(Arc::ptr_eq(&state.homes.lock().unwrap().active(), &home));
        assert!(Arc::ptr_eq(
            state.home_bootstrap.lock().unwrap().as_ref().unwrap(),
            &bootstrap
        ));
        assert!(Arc::ptr_eq(
            state.native_namespaces.lock().unwrap().as_ref().unwrap(),
            &namespaces
        ));
        assert!(Arc::ptr_eq(
            home.attachment_custody.lock().unwrap().as_ref().unwrap(),
            &custody
        ));
        assert_eq!(home.recovery_startup.lock().unwrap().snapshot(), recovery);
        assert_eq!(state.workspace.as_ref(), Some(&f.project));
        assert!(!outcome.to_string().contains("INVENTED_PRIVATE"));
        assert!(!outcome.to_string().contains(f.shared[0].to_str().unwrap()));
        peer.endpoint_private_taps();
        f.public_endpoint_records_safe();
    }
    #[test]
    fn access_provider_endpoint_private_writer_checked_link_and_real_consumers() {
        for receiving_alias in [false, true] {
            let f = Fixture::new();
            let (desktop, state, home, mut peer) = f.continuation();
            let h = home.host_config.as_ref().unwrap().codex_home.clone();
            let layer = if receiving_alias {
                h.join("config.toml")
            } else {
                f.shared[0].clone()
            };
            peer.endpoint_replies(
                f.shared[0].clone(),
                layer.clone(),
                "fixture.dot",
                "https://example.invalid/new",
            );
            let original = read_profile(&f.data.join(PROFILE)).unwrap();
            let links = desktop
                .lock()
                .unwrap()
                .receiving
                .as_ref()
                .unwrap()
                .entries()
                .unwrap();
            let bootstrap = state
                .home_bootstrap
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let namespaces = state
                .native_namespaces
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let custody = home
                .attachment_custody
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let recovery = home.recovery_startup.lock().unwrap().snapshot();
            let offer = crate::hosting::provider_endpoint::offer(
                &state,
                "fixture.dot",
                "https://example.invalid/new",
            )
            .unwrap();
            assert!(!offer.view().to_string().contains("INVENTED_PRIVATE"));
            let outcome = crate::hosting::provider_endpoint::save(
                &state,
                offer,
                |effects| {
                    assert_eq!(effects["currentEndpoint"], "https://example.invalid/old");
                    assert!(desktop.try_lock().is_ok());
                    Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                        crate::hosting::provider_endpoint::WRITE_ACTION.into(),
                    ))
                },
                |candidate, effects| {
                    assert_eq!(
                        candidate.private_reading().0["layers"][0]["name"]["file"],
                        json!(layer),
                        "the native spelling was not rewritten"
                    );
                    assert!(
                        state.validate_home_source(&home).is_err(),
                        "ACK alone cannot continue source"
                    );
                    assert_eq!(effects["currentEndpoint"], "https://example.invalid/new");
                    assert!(desktop.try_lock().is_ok());
                    Ok(Some(candidate.accept_checked_current_object()))
                },
            )
            .unwrap();
            assert_eq!(outcome["state"], "continued");
            let read = peer.continuation_frame();
            assert_eq!(read["method"], "config/read");
            let write = peer.continuation_frame();
            assert_eq!(write["method"], "config/batchWrite");
            assert_eq!(
                write["params"],
                json!({"edits":[{"keyPath":"model_providers.\"fixture.dot\".base_url","value":"https://example.invalid/new","mergeStrategy":"replace"}],"filePath":f.shared[0],"expectedVersion":"INVENTED_PRIVATE_OLD_VERSION","reloadUserConfig":false})
            );
            assert_eq!(peer.continuation_frame()["method"], "config/read");
            peer.endpoint_private_taps();
            f.public_endpoint_records_safe();
            state.validate_home_source(&home).unwrap();
            assert!(Arc::ptr_eq(&state.homes.lock().unwrap().active(), &home));
            assert!(Arc::ptr_eq(
                state.home_bootstrap.lock().unwrap().as_ref().unwrap(),
                &bootstrap
            ));
            assert!(Arc::ptr_eq(
                state.native_namespaces.lock().unwrap().as_ref().unwrap(),
                &namespaces
            ));
            assert!(Arc::ptr_eq(
                home.attachment_custody.lock().unwrap().as_ref().unwrap(),
                &custody
            ));
            assert_eq!(home.recovery_startup.lock().unwrap().snapshot(), recovery);
            assert_eq!(
                desktop
                    .lock()
                    .unwrap()
                    .receiving
                    .as_ref()
                    .unwrap()
                    .entries()
                    .unwrap(),
                links
            );
            let mut expected = original;
            let current = read_profile(&f.data.join(PROFILE)).unwrap();
            expected.shared[0] = current.shared[0].clone();
            assert_eq!(expected, current);
            assert!(desktop
                .lock()
                .unwrap()
                .preview_project(Some(f.project.clone()))
                .is_ok());
            drop(peer);
            drop(home);
            drop(state);
            drop(desktop);
            drop(custody);
            drop(bootstrap);
            drop(namespaces);
            let mut fresh = f.setup();
            let launch = f.resolve(&mut fresh);
            let RootInputs {
                launch,
                data,
                allow_operational,
            } = fresh.admit_root(launch, Ok(f.data.clone()));
            assert!(allow_operational);
            let (state, home) =
                crate::freeze_startup_state(launch, Arc::new(Mutex::new(fresh)), Value::Null);
            crate::initialize_startup_consumers(
                &state,
                &home,
                data,
                allow_operational,
                true,
                Some(f.data.join("records")),
                None,
                f.shared.clone().map(Some),
            );
            state.validate_home_source(&home).unwrap();
            assert_eq!(home.host_config.as_ref().unwrap().codex_home, h);
            assert_eq!(state.workspace.as_ref(), Some(&f.project));
            assert!(home.attachment_custody.lock().unwrap().is_ok());
        }
    }
    #[test]
    fn config_continuation_acceptance_is_one_shot_and_prior_tokens_do_not_admit() {
        let f = Fixture::new();
        let (desktop, state, home, mut peer) = f.continuation();
        let preview = desktop.lock().unwrap().preview_project(None).unwrap();
        let token = preview["token"].as_str().unwrap();
        let first = crate::begin_config_resource_continuation(&state).unwrap();
        assert!(desktop.lock().unwrap().preview_statement(token).is_err());
        let pending = crate::begin_config_resource_continuation(&state).unwrap();
        f.replace_config();
        peer.answer(f.private_config());
        assert!(
            crate::complete_config_resource_continuation(&state, first, |_| panic!(
                "superseded preflight"
            ))
            .is_err()
        );
        let mut old_acceptance = None;
        assert!(
            crate::complete_config_resource_continuation(&state, pending, |candidate| {
                old_acceptance = Some(candidate.accept_checked_current_object());
                Ok(Some(candidate.accept_checked_current_object()))
            })
            .unwrap()
        );
        assert_eq!(peer.continuation_frame()["method"], "config/read");
        let pending = crate::begin_config_resource_continuation(&state).unwrap();
        f.replace_config();
        let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
        assert!(
            crate::complete_config_resource_continuation(&state, pending, |_| Ok(
                old_acceptance.take()
            ))
            .is_err()
        );
        assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), before);
        assert_eq!(peer.continuation_frame()["method"], "config/read");
        peer.continuation_private_taps();
        assert!(state.validate_home_source(&home).is_err());
        // An unaccepted replacement cannot mint its own new preflight.
        assert!(crate::begin_config_resource_continuation(&state).is_err());
    }

    #[test]
    fn config_continuation_native_layer_scope_and_private_wait_fail_closed() {
        for case in [
            "missing-layers",
            "different-target",
            "foreign-alias",
            "receiving-dot-spelling",
            "duplicate-user",
            "disabled-user",
            "missing-version",
            "oversize-version",
            "malformed",
            "error",
            "timeout-late",
        ] {
            let f = Fixture::new();
            let (desktop, state, home, mut peer) = f.continuation();
            let pending = crate::begin_config_resource_continuation(&state).unwrap();
            f.replace_config();
            let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
            let original = desktop.lock().unwrap().requested.clone().unwrap();
            let mut reply = f.private_config();
            let mut delayed = None;
            match case {
                "missing-layers" => reply
                    .as_object_mut()
                    .unwrap()
                    .remove("layers")
                    .map(|_| ())
                    .unwrap(),
                "different-target" => reply["layers"][0]["name"]["file"] = json!(f.shared[1]),
                "foreign-alias" => {
                    let alias = f.root.join("unapproved-alias");
                    std::os::unix::fs::symlink(&f.shared[0], &alias).unwrap();
                    reply["layers"][0]["name"]["file"] = json!(alias);
                }
                "receiving-dot-spelling" => {
                    let expected = home
                        .host_config
                        .as_ref()
                        .unwrap()
                        .codex_home
                        .join("config.toml");
                    let spelling = format!(
                        "{}/./config.toml",
                        home.host_config.as_ref().unwrap().codex_home.display()
                    );
                    assert_ne!(Path::new(&spelling).as_os_str(), expected.as_os_str());
                    assert_eq!(std::fs::canonicalize(&spelling).unwrap(), f.shared[0]);
                    reply["layers"][0]["name"]["file"] = json!(spelling);
                }
                "duplicate-user" => {
                    let layer = reply["layers"][0].clone();
                    reply["layers"].as_array_mut().unwrap().push(layer);
                }
                "disabled-user" => {
                    reply["layers"][0]["disabledReason"] =
                        json!("INVENTED_PRIVATE_PROVIDER_CANARY_481")
                }
                "missing-version" => {
                    reply["layers"][0]
                        .as_object_mut()
                        .unwrap()
                        .remove("version");
                }
                "oversize-version" => reply["layers"][0]["version"] = json!("v".repeat(4097)),
                "malformed" => reply["config"] = Value::Null,
                "error" => peer.config_read_error(),
                "timeout-late" => delayed = Some(peer.unanswered_config_read()),
                _ => unreachable!(),
            }
            if case != "error" && case != "timeout-late" {
                peer.answer(reply.clone());
            }
            let result = crate::complete_config_resource_continuation(&state, pending, |_| {
                panic!("{case}: invalid private observation reached review")
            });
            let error = result.unwrap_err();
            assert!(!error.contains("INVENTED_"));
            assert_eq!(read_profile_bytes(&f.data.join(PROFILE)).unwrap(), before);
            assert_eq!(
                desktop.lock().unwrap().requested.as_ref().unwrap(),
                &original
            );
            assert_eq!(peer.continuation_frame()["method"], "config/read");
            if let Some(delayed) = delayed {
                let source = delayed.lock().unwrap().take().unwrap();
                peer.host.native_frame_for_test(
                    source.generation(),
                    &json!({"id":source.request_id(),"result":reply}),
                );
                assert!(!source
                    .evidence()
                    .to_string()
                    .contains("INVENTED_PRIVATE_PROVIDER_CANARY_481"));
            }
            peer.continuation_private_taps();
            assert!(!desktop
                .lock()
                .unwrap()
                .view()
                .to_string()
                .contains("INVENTED_NATIVE_VERSION_PRIVATE_52"));
            assert!(!json!(peer.host.journal())
                .to_string()
                .contains("INVENTED_PRIVATE_PROVIDER_CANARY_481"));
        }
    }
    #[test]
    fn config_continuation_requires_actual_admission_and_preserves_stable_unavailable_siblings() {
        for case in [
            "setup-only",
            "resolve-only",
            "pending-plan",
            "foreign-config",
            "missing-agents",
            "broken-skills",
        ] {
            let f = Fixture::new();
            let mut setup = f.setup();
            let invented = HostConfig::new(
                f.root.join("never-executed"),
                f.root.join("not-admitted"),
                f.root.join("probe"),
                f.project.clone(),
            );
            if case == "setup-only" {
                assert!(setup.begin_config_continuation(&invented).is_err());
                continue;
            }
            let saved = f.prepare(&mut setup, true);
            drop(setup);
            if case == "resolve-only" {
                let mut setup = f.setup();
                let launch = f.resolve(&mut setup);
                assert!(setup
                    .begin_config_continuation(launch.host_config.as_ref().unwrap())
                    .is_err());
                continue;
            }
            if case == "missing-agents" {
                std::fs::remove_file(&f.shared[1]).unwrap();
            }
            if case == "broken-skills" {
                let path =
                    PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap()).join("skills");
                std::fs::remove_file(&path).unwrap();
                std::os::unix::fs::symlink(f.root.join("explicitly-unavailable-skills"), path)
                    .unwrap();
            }
            let (desktop, state, home, mut peer) = f.admitted_continuation();
            if case == "foreign-config" {
                assert!(desktop
                    .lock()
                    .unwrap()
                    .begin_config_continuation(&invented)
                    .is_err());
                state.validate_home_source(&home).unwrap();
                continue;
            }
            if case == "pending-plan" {
                let preview = desktop.lock().unwrap().preview_project(None).unwrap();
                desktop
                    .lock()
                    .unwrap()
                    .prepare_and_save(preview["token"].as_str().unwrap())
                    .unwrap();
                assert!(crate::begin_config_resource_continuation(&state).is_err());
                continue;
            }
            let entries = desktop
                .lock()
                .unwrap()
                .receiving
                .as_ref()
                .unwrap()
                .entries()
                .unwrap();
            let pending = crate::begin_config_resource_continuation(&state).unwrap();
            f.replace_config();
            peer.answer(f.private_config());
            assert!(
                crate::complete_config_resource_continuation(&state, pending, |c| Ok(Some(
                    c.accept_checked_current_object()
                )))
                .unwrap()
            );
            assert_eq!(
                desktop
                    .lock()
                    .unwrap()
                    .receiving
                    .as_ref()
                    .unwrap()
                    .entries()
                    .unwrap(),
                entries
            );
            assert!(desktop.lock().unwrap().preview_project(None).is_ok());
            state.validate_home_source(&home).unwrap();
            assert_eq!(peer.continuation_frame()["method"], "config/read");
            peer.continuation_private_taps();
        }
    }

    #[test]
    fn config_continuation_review_drift_and_supersession_refuse_without_publication() {
        for case in [
            "cancel",
            "nonexact",
            "review-error",
            "same-bytes-new-inode",
            "in-place-change",
            "config-link",
            "agents-link",
            "skills-link",
            "missing-config",
            "target-alias",
            "hardlink",
            "profile-same-bytes",
            "pending-plan",
            "lost-home-custody",
            "lost-profile-custody",
            "lost-app-custody",
            "sibling-missing",
            "sibling-replaced",
            "preview-superseded",
            "read-revision",
            "generation",
        ] {
            let f = Fixture::new();
            let (desktop, state, home, mut peer) = f.continuation();
            let pending = crate::begin_config_resource_continuation(&state).unwrap();
            f.replace_config();
            let before = read_profile_bytes(&f.data.join(PROFILE)).unwrap();
            let original = desktop.lock().unwrap().requested.clone().unwrap();
            let bootstrap = state
                .home_bootstrap
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let attachment = home
                .attachment_custody
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let context = state.project_context.view();
            let recovery = home.recovery_startup.lock().unwrap().snapshot();
            peer.answer(f.private_config());
            let mut expected_profile = before.0.clone();
            let result =
                crate::complete_config_resource_continuation(&state, pending, |candidate| {
                    match case {
                        "cancel" => return Ok(None),
                        "nonexact" => return Ok(Some(candidate.nonexact_for_test())),
                        "review-error" => return Err(()),
                        "same-bytes-new-inode" => f.replace_config(),
                        "in-place-change" => {
                            std::fs::write(&f.shared[0], b"different invented current bytes")
                                .unwrap()
                        }
                        "config-link" | "agents-link" | "skills-link" => {
                            let name = match case {
                                "config-link" => "config.toml",
                                "agents-link" => "AGENTS.md",
                                _ => "skills",
                            };
                            let path = home.host_config.as_ref().unwrap().codex_home.join(name);
                            let target = std::fs::read_link(&path).unwrap();
                            std::fs::remove_file(&path).unwrap();
                            std::os::unix::fs::symlink(target, path).unwrap();
                        }
                        "missing-config" => std::fs::remove_file(&f.shared[0]).unwrap(),
                        "target-alias" => {
                            let elsewhere = f.root.join("different-target");
                            std::fs::rename(&f.shared[0], &elsewhere).unwrap();
                            std::os::unix::fs::symlink(elsewhere, &f.shared[0]).unwrap();
                        }
                        "hardlink" => {
                            std::fs::hard_link(&f.shared[0], f.root.join("hard-alias")).unwrap()
                        }
                        "profile-same-bytes" => {
                            let replacement = f.root.join("profile-replacement");
                            std::fs::write(&replacement, &before.0).unwrap();
                            std::fs::set_permissions(
                                &replacement,
                                std::fs::Permissions::from_mode(0o600),
                            )
                            .unwrap();
                            std::fs::rename(replacement, f.data.join(PROFILE)).unwrap();
                        }
                        "pending-plan" => {
                            let mut request = read_profile(&f.data.join(PROFILE)).unwrap();
                            request.project = None;
                            write_profile(&f.data.join(PROFILE), &request).unwrap();
                            expected_profile = std::fs::read(f.data.join(PROFILE)).unwrap();
                        }
                        "lost-home-custody" => {
                            desktop.lock().unwrap().receiving.take();
                        }
                        "lost-profile-custody" => {
                            desktop.lock().unwrap().profile_directory.take();
                        }
                        "lost-app-custody" => {
                            desktop.lock().unwrap().lease.take();
                        }
                        "sibling-missing" => std::fs::remove_file(&f.shared[1]).unwrap(),
                        "sibling-replaced" => {
                            let path = f.root.join("agents-replacement");
                            std::fs::write(&path, b"invented guidance replacement").unwrap();
                            std::fs::rename(path, &f.shared[1]).unwrap();
                        }
                        "preview-superseded" => {
                            assert!(desktop.lock().unwrap().preview_project(None).is_err());
                        }
                        "read-revision" => {
                            peer.host
                                .configured_provider_read_within(
                                    &peer.g,
                                    f.project.to_str().unwrap(),
                                    &Value::Null,
                                    std::time::Duration::from_millis(30),
                                )
                                .unwrap();
                        }
                        "generation" => peer.supersede_config_generation(),
                        _ => unreachable!(),
                    }
                    Ok(Some(candidate.accept_checked_current_object()))
                });
            if case == "cancel" {
                assert_eq!(result.unwrap(), false);
            } else {
                assert!(result.is_err(), "{case} unexpectedly accepted");
            }
            assert_eq!(
                std::fs::read(f.data.join(PROFILE)).unwrap(),
                expected_profile,
                "{case}: no unintended profile write"
            );
            assert_eq!(
                desktop.lock().unwrap().requested.as_ref().unwrap(),
                &original,
                "{case}: no memory promotion"
            );
            assert!(Arc::ptr_eq(&state.homes.lock().unwrap().active(), &home));
            assert!(Arc::ptr_eq(
                state.home_bootstrap.lock().unwrap().as_ref().unwrap(),
                &bootstrap
            ));
            assert!(Arc::ptr_eq(
                home.attachment_custody.lock().unwrap().as_ref().unwrap(),
                &attachment
            ));
            assert_eq!(state.project_context.view(), context);
            assert_eq!(home.recovery_startup.lock().unwrap().snapshot(), recovery);
            assert_eq!(peer.continuation_frame()["method"], "config/read");
            if case == "read-revision" {
                assert_eq!(peer.continuation_frame()["method"], "config/read");
            }
            peer.continuation_private_taps();
        }
    }

    #[test]
    fn config_continuation_unknown_publication_never_promotes_or_recovers_by_token() {
        for case in [
            "target-after-publication",
            "profile-after-publication",
            "source-after-publication",
        ] {
            let f = Fixture::new();
            let (desktop, state, home, mut peer) = f.continuation();
            let old = desktop.lock().unwrap().requested.clone().unwrap();
            let pending = crate::begin_config_resource_continuation(&state).unwrap();
            f.replace_config();
            peer.answer(f.private_config());
            let config = f.shared[0].clone();
            let profile = f.data.join(PROFILE);
            let path = f.root.join("publication-drift");
            desktop.lock().unwrap().after_config_publication = Some(Box::new(move || match case {
                "target-after-publication" => {
                    std::fs::write(&path, b"unreviewed invented object").unwrap();
                    std::fs::rename(&path, &config).unwrap();
                }
                "profile-after-publication" => {
                    let mut requested = read_profile(&profile).unwrap();
                    requested.project = None;
                    write_profile(&profile, &requested).unwrap();
                }
                "source-after-publication" => {}
                _ => unreachable!(),
            }));
            if case == "source-after-publication" {
                // Use a genuine new scoped private read to supersede the receipt
                // during publication, without killing/restarting any process.
                let host = home.host.clone();
                let generation = peer.g.clone();
                let cwd = f.project.to_str().unwrap().to_owned();
                desktop.lock().unwrap().after_config_publication = Some(Box::new(move || {
                    host.configured_provider_read_within(
                        &generation,
                        &cwd,
                        &Value::Null,
                        std::time::Duration::from_millis(30),
                    )
                    .unwrap();
                }));
            }
            let result = crate::complete_config_resource_continuation(&state, pending, |c| {
                Ok(Some(c.accept_checked_current_object()))
            });
            assert!(
                result
                    .unwrap_err()
                    .starts_with("Config request publication outcome unknown;"),
                "{case}"
            );
            assert_eq!(desktop.lock().unwrap().requested.as_ref().unwrap(), &old);
            assert!(desktop.lock().unwrap().config_publication_unknown);
            assert!(state.validate_home_source(&home).is_err());
            assert!(crate::begin_config_resource_continuation(&state).is_err());
            assert_eq!(peer.continuation_frame()["method"], "config/read");
            if case == "source-after-publication" {
                assert_eq!(peer.continuation_frame()["method"], "config/read");
            }
            peer.continuation_private_taps();
        }
    }

    #[test]
    fn config_continuation_joined_private_read_publication_retained_and_fresh_consumers() {
        let f = Fixture::new();
        let mut setup = f.setup();
        f.prepare(&mut setup, true);
        drop(setup);
        let mut active = f.setup();
        let launch = f.resolve(&mut active);
        let RootInputs {
            launch,
            data,
            allow_operational,
        } = active.admit_root(launch, Ok(f.data.clone()));
        assert!(allow_operational);
        let desktop = Arc::new(Mutex::new(active));
        let (state, home) = crate::freeze_startup_state(launch, desktop.clone(), Value::Null);
        crate::initialize_startup_consumers(
            &state,
            &home,
            data,
            allow_operational,
            true,
            Some(f.data.join("records")),
            None,
            f.shared.clone().map(Some),
        );
        let h = home.host_config.as_ref().unwrap().codex_home.clone();
        let mut peer =
            crate::hosting::config_resource_continuation::TestPeer::for_config_continuation(
                home.host.clone(),
                &h,
            );
        let old_request =
            serde_json::to_value(read_profile(&f.data.join(PROFILE)).unwrap()).unwrap();
        let old_ref = desktop.lock().unwrap().requested.as_ref().unwrap().shared[0].clone();
        let links = desktop
            .lock()
            .unwrap()
            .receiving
            .as_ref()
            .unwrap()
            .entries()
            .unwrap();
        let bootstrap = state
            .home_bootstrap
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .clone();
        let namespaces = state
            .native_namespaces
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .clone();
        let custody = home
            .attachment_custody
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .clone();
        let recovery = home.recovery_startup.lock().unwrap().snapshot();
        let context = state.project_context.view();
        let attachments = state
            .attachment_selection
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .snapshot();
        let mut selection = crate::access::ConversationSelection::new_explicit(
            "invented-conversation",
            Some("invented-project"),
        )
        .unwrap();
        selection
            .choose("local-provider", "manual-provider", "manual-model", false)
            .unwrap();
        *home.access_selection.lock().unwrap() = Some(selection);
        let choice = home
            .access_selection
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .snapshot();
        let records = records_store::current().unwrap().root;
        let pending = crate::begin_config_resource_continuation(&state).unwrap();
        let replacement = f.root.join("replacement");
        std::fs::write(
            &replacement,
            b"invented replacement, never parsed by desktop",
        )
        .unwrap();
        std::fs::rename(replacement, &f.shared[0]).unwrap();
        assert!(old_ref.current(false).is_err());
        assert!(state.validate_home_source(&home).is_err());
        let private = json!({"config":{"developer_instructions":"INVENTED_PRIVATE_PROVIDER_CANARY_481"},"origins":{},"layers":[{"name":{"type":"user","file":f.shared[0]},"config":{},"version":"native-invented-version","disabledReason":null}]});
        peer.answer(private);
        let continued =
            crate::complete_config_resource_continuation(&state, pending, |candidate| {
                assert_eq!(candidate.private_reading().1, "native-invented-version");
                assert_eq!(
                    candidate.private_reading().0["config"]["developer_instructions"],
                    "INVENTED_PRIVATE_PROVIDER_CANARY_481"
                );
                assert!(desktop.try_lock().is_ok(), "review holds no desktop lock");
                Ok(Some(candidate.accept_checked_current_object()))
            })
            .unwrap();
        assert!(continued);
        let wire = peer.continuation_frame();
        assert_eq!(wire["method"], "config/read");
        assert_eq!(wire["params"]["cwd"], f.project.to_str().unwrap());
        assert_eq!(wire["params"]["includeLayers"], true);
        peer.continuation_private_taps();
        assert!(home.host.snapshot()["conversations"]
            .as_array()
            .is_none_or(|v| v.is_empty()));
        state.validate_home_source(&home).unwrap();
        let now_request =
            serde_json::to_value(read_profile(&f.data.join(PROFILE)).unwrap()).unwrap();
        let mut expected = old_request;
        expected["shared"][0] = now_request["shared"][0].clone();
        assert_eq!(now_request, expected);
        assert_ne!(
            now_request["shared"][0]["object"],
            serde_json::to_value(old_ref.object.clone()).unwrap()
        );
        let assert_owners = || {
            assert!(Arc::ptr_eq(&state.homes.lock().unwrap().active(), &home));
            assert_eq!(state.workspace.as_ref(), Some(&f.project));
            assert!(Arc::ptr_eq(
                state.home_bootstrap.lock().unwrap().as_ref().unwrap(),
                &bootstrap
            ));
            assert!(Arc::ptr_eq(
                state.native_namespaces.lock().unwrap().as_ref().unwrap(),
                &namespaces
            ));
            assert!(Arc::ptr_eq(
                home.attachment_custody.lock().unwrap().as_ref().unwrap(),
                &custody
            ));
            assert_eq!(home.recovery_startup.lock().unwrap().snapshot(), recovery);
            assert_eq!(state.project_context.view(), context);
            assert_eq!(
                state
                    .attachment_selection
                    .lock()
                    .unwrap()
                    .as_ref()
                    .unwrap()
                    .snapshot(),
                attachments
            );
            assert_eq!(
                home.access_selection
                    .lock()
                    .unwrap()
                    .as_ref()
                    .unwrap()
                    .snapshot(),
                choice
            );
            assert_eq!(records_store::current().unwrap().root, records);
            assert_eq!(
                desktop
                    .lock()
                    .unwrap()
                    .receiving
                    .as_ref()
                    .unwrap()
                    .entries()
                    .unwrap(),
                links
            );
        };
        assert_owners();
        let preview = desktop
            .lock()
            .unwrap()
            .preview_project(Some(f.project.clone()))
            .unwrap();
        assert_eq!(preview["accountHome"], h.to_str().unwrap());
        // Preview success exercises genuine retained-source guards. Do not save
        // a second pending plan: fresh admission below consumes the exact config
        // continuation request with H/P unchanged.
        assert_owners();
        drop(peer);
        drop(home);
        drop(state);
        drop(desktop);
        let mut fresh = f.setup();
        let launch = f.resolve(&mut fresh);
        let RootInputs {
            launch,
            data,
            allow_operational,
        } = fresh.admit_root(launch, Ok(f.data.clone()));
        assert!(allow_operational);
        assert_eq!(launch.shared_paths[0].as_ref(), Some(&f.shared[0]));
        assert_eq!(launch.workspace.as_ref(), Some(&f.project));
        let (state, home) =
            crate::freeze_startup_state(launch, Arc::new(Mutex::new(fresh)), Value::Null);
        crate::initialize_startup_consumers(
            &state,
            &home,
            data,
            allow_operational,
            true,
            Some(f.data.join("records")),
            None,
            f.shared.clone().map(Some),
        );
        assert_eq!(home.host_config.as_ref().unwrap().codex_home, h);
        state.validate_home_source(&home).unwrap();
        state
            .native_namespaces
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .guard_app_root(&f.data)
            .unwrap();
        assert!(state.instructions_root.lock().unwrap().is_ok());
        assert!(home.attachment_custody.lock().unwrap().is_ok());
        assert_eq!(state.workspace.as_ref(), Some(&f.project));
    }
    #[test]
    fn retained_project_receiving_entry_drift_during_confirmation_refuses_without_rebinding() {
        let previous_store = records_store::configured_for_test();
        let mut incorrectly_accepted = Vec::new();
        for name in ["config.toml", "AGENTS.md", "skills"] {
            for replacement in [
                "same-target-link",
                "different-target-link",
                "ordinary-file",
                "missing",
            ] {
                let f = Fixture::new();
                let q = f.root.join("explicit-next-project");
                std::fs::create_dir(&q).unwrap();
                let mut setup = f.setup();
                let saved = f.prepare(&mut setup, true);
                drop(setup);
                let h = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
                let mut active = f.setup();
                let launch = f.resolve(&mut active);
                let RootInputs {
                    launch,
                    data,
                    allow_operational,
                } = active.admit_root(launch, Ok(f.data.clone()));
                assert!(allow_operational);
                let desktop = Arc::new(Mutex::new(active));
                let (state, home) =
                    crate::freeze_startup_state(launch, desktop.clone(), Value::Null);
                crate::initialize_startup_consumers(
                    &state,
                    &home,
                    data,
                    allow_operational,
                    true,
                    Some(f.data.join("records")),
                    None,
                    f.shared.clone().map(Some),
                );
                let original_home = state.homes.lock().unwrap().active();
                let original_bootstrap = state
                    .home_bootstrap
                    .lock()
                    .unwrap()
                    .as_ref()
                    .unwrap()
                    .clone();
                let original_namespaces = state
                    .native_namespaces
                    .lock()
                    .unwrap()
                    .as_ref()
                    .unwrap()
                    .clone();
                let original_context = state.project_context.view();
                let original_attachments = state
                    .attachment_selection
                    .lock()
                    .unwrap()
                    .as_ref()
                    .unwrap()
                    .snapshot();
                let original_recovery = home.recovery_startup.lock().unwrap().snapshot();
                let original_choices = home
                    .access_selection
                    .lock()
                    .unwrap()
                    .as_ref()
                    .map(|s| s.snapshot());
                let original_records = records_store::current().unwrap().root;
                let original_request = std::fs::read(f.data.join(PROFILE)).unwrap();
                let preview = desktop.lock().unwrap().preview_project(Some(q)).unwrap();
                let token = preview["token"].as_str().unwrap().to_owned();
                let (result, available_after_change) = std::thread::scope(|scope| {
                    let (ready_send, ready_receive) = std::sync::mpsc::channel();
                    let (resume_send, resume_receive) = std::sync::mpsc::channel();
                    let controller = desktop.clone();
                    let worker = scope.spawn(move || {
                        crate::desktop_setup_confirmation::prepare(
                            &controller,
                            &token,
                            |_, action| {
                                assert_eq!(action, "Save project for next launch");
                                ready_send.send(()).unwrap();
                                resume_receive
                                    .recv_timeout(std::time::Duration::from_secs(5))
                                    .unwrap();
                                Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                                    action.into(),
                                ))
                            },
                        )
                    });
                    ready_receive
                        .recv_timeout(std::time::Duration::from_secs(5))
                        .unwrap();
                    let receiving = h.join(name);
                    let target = std::fs::read_link(&receiving).unwrap();
                    // Retain the old inode so same-target replacement cannot be
                    // mistaken for filesystem inode reuse in this fixture.
                    std::fs::rename(&receiving, h.join(format!("fixture-original-{name}")))
                        .unwrap();
                    match replacement {
                        "same-target-link" => {
                            std::os::unix::fs::symlink(target, &receiving).unwrap()
                        }
                        "different-target-link" => std::os::unix::fs::symlink(
                            f.root.join("invented-other-target"),
                            &receiving,
                        )
                        .unwrap(),
                        "ordinary-file" => {
                            std::fs::write(&receiving, b"invented receiving conflict; never read")
                                .unwrap()
                        }
                        "missing" => {}
                        _ => unreachable!(),
                    }
                    let available =
                        desktop.lock().unwrap().view()["retainProject"]["available"].clone();
                    resume_send.send(()).unwrap();
                    (worker.join().unwrap(), available)
                });
                match result {
                    Ok(_) => incorrectly_accepted.push(format!("{name}: {replacement}")),
                    Err(reason) => {
                        assert!(reason.contains("receiving"), "{reason}");
                        assert_eq!(available_after_change, false);
                        assert!(desktop.lock().unwrap().preview_project(None).is_err());
                        assert_eq!(
                            std::fs::read(f.data.join(PROFILE)).unwrap(),
                            original_request
                        );
                    }
                }
                assert!(Arc::ptr_eq(
                    &original_home,
                    &state.homes.lock().unwrap().active()
                ));
                assert!(Arc::ptr_eq(
                    &original_bootstrap,
                    state.home_bootstrap.lock().unwrap().as_ref().unwrap()
                ));
                assert!(Arc::ptr_eq(
                    &original_namespaces,
                    state.native_namespaces.lock().unwrap().as_ref().unwrap()
                ));
                assert_eq!(state.workspace.as_deref(), Some(f.project.as_path()));
                assert_eq!(home.host_config.as_ref().unwrap().cwd, f.project);
                assert_eq!(state.project_context.view(), original_context);
                assert_eq!(
                    state
                        .attachment_selection
                        .lock()
                        .unwrap()
                        .as_ref()
                        .unwrap()
                        .snapshot(),
                    original_attachments
                );
                assert_eq!(
                    home.recovery_startup.lock().unwrap().snapshot(),
                    original_recovery
                );
                assert_eq!(
                    home.access_selection
                        .lock()
                        .unwrap()
                        .as_ref()
                        .map(|s| s.snapshot()),
                    original_choices
                );
                assert_eq!(records_store::current().unwrap().root, original_records);
                assert_eq!(
                    std::fs::read_dir(f.data.join("account-homes"))
                        .unwrap()
                        .count(),
                    1
                );
            }
        }
        records_store::restore_configured_for_test(previous_store);
        assert!(
            incorrectly_accepted.is_empty(),
            "receiving replacements incorrectly saved: {incorrectly_accepted:?}"
        );
    }

    #[test]
    fn retained_project_stable_receiving_resource_limits_remain_available_and_unchanged() {
        let f = Fixture::new();
        std::fs::remove_file(&f.shared[0]).unwrap();
        let mut setup = f.setup();
        let saved = f.prepare(&mut setup, true);
        drop(setup);
        let h = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
        // All are initial source limits: dangling expected config link, missing
        // AGENTS entry, and a divergent dangling skills link. None is repaired.
        std::fs::remove_file(h.join("AGENTS.md")).unwrap();
        std::fs::remove_file(h.join("skills")).unwrap();
        let other = f.root.join("explicitly-unavailable-invented-skills");
        std::os::unix::fs::symlink(&other, h.join("skills")).unwrap();
        let before = serde_json::to_value(read_profile(&f.data.join(PROFILE)).unwrap()).unwrap();
        let config_inode =
            ObjectRef::of(&std::fs::symlink_metadata(h.join("config.toml")).unwrap());
        let skills_inode = ObjectRef::of(&std::fs::symlink_metadata(h.join("skills")).unwrap());
        let mut active = f.setup();
        let launch = f.resolve(&mut active);
        assert!(
            active
                .admit_root(launch, Ok(f.data.clone()))
                .allow_operational
        );
        assert_eq!(active.view()["retainProject"]["available"], true);
        let preview = active.preview_project(None).unwrap();
        let result = crate::desktop_setup_confirmation::prepare(
            &Mutex::new(active),
            preview["token"].as_str().unwrap(),
            |_, action| {
                assert_eq!(action, "Save project for next launch");
                Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                    action.into(),
                ))
            },
        )
        .unwrap();
        assert_eq!(result["pending"]["kind"], "retain-account-project");
        let mut expected = before;
        expected["project"] = Value::Null;
        assert_eq!(
            serde_json::to_value(read_profile(&f.data.join(PROFILE)).unwrap()).unwrap(),
            expected
        );
        assert_eq!(
            ObjectRef::of(&std::fs::symlink_metadata(h.join("config.toml")).unwrap()),
            config_inode
        );
        assert_eq!(
            std::fs::read_link(h.join("config.toml")).unwrap(),
            f.shared[0]
        );
        assert!(!f.shared[0].exists());
        assert!(std::fs::symlink_metadata(h.join("AGENTS.md")).is_err());
        assert_eq!(
            ObjectRef::of(&std::fs::symlink_metadata(h.join("skills")).unwrap()),
            skills_inode
        );
        assert_eq!(std::fs::read_link(h.join("skills")).unwrap(), other);
        assert!(!other.exists());
        assert_eq!(
            std::fs::read_dir(f.data.join("account-homes"))
                .unwrap()
                .count(),
            1
        );
    }

    #[test]
    fn retained_project_preserves_absent_source_reference_and_broken_link_without_repreparing() {
        let f = Fixture::new();
        std::fs::remove_file(&f.shared[0]).unwrap();
        let mut setup = f.setup();
        let saved = f.prepare(&mut setup, true);
        drop(setup);
        let h = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
        std::fs::write(
            &f.shared[0],
            b"invented resource appeared after explicit absent reference",
        )
        .unwrap();
        std::fs::remove_file(h.join("AGENTS.md")).unwrap();
        std::fs::write(h.join("AGENTS.md"), b"invented divergent receiving file").unwrap();
        let original = ObjectRef::of(&std::fs::symlink_metadata(h.join("AGENTS.md")).unwrap());
        let before = serde_json::to_value(read_profile(&f.data.join(PROFILE)).unwrap()).unwrap();
        assert!(before["shared"][0]["object"].is_null());
        let mut active = f.setup();
        let launch = f.resolve(&mut active);
        assert!(
            active
                .admit_root(launch, Ok(f.data.clone()))
                .allow_operational
        );
        assert!(active.requested.as_ref().unwrap().shared[0]
            .object
            .is_some());
        let preview = active.preview_project(None).unwrap();
        active
            .prepare_and_save(preview["token"].as_str().unwrap())
            .unwrap();
        let mut expected = before;
        expected["project"] = Value::Null;
        assert_eq!(
            serde_json::to_value(read_profile(&f.data.join(PROFILE)).unwrap()).unwrap(),
            expected
        );
        assert_eq!(
            ObjectRef::of(&std::fs::symlink_metadata(h.join("AGENTS.md")).unwrap()),
            original
        );
        assert!(!std::fs::symlink_metadata(h.join("AGENTS.md"))
            .unwrap()
            .file_type()
            .is_symlink());
        assert_eq!(
            std::fs::read_dir(f.data.join("account-homes"))
                .unwrap()
                .count(),
            1
        );
    }

    #[test]
    fn retained_project_joined_real_consumers_keep_h_and_change_only_next_project() {
        let previous_store = records_store::configured_for_test();
        for with_project in [true, false] {
            let f = Fixture::new();
            let q = f.root.join("explicit-next-project");
            std::fs::create_dir(&q).unwrap();
            let mut setup = f.setup();
            let saved = f.prepare(&mut setup, true);
            drop(setup);
            let h = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
            let before_request =
                serde_json::to_value(read_profile(&f.data.join(PROFILE)).unwrap()).unwrap();
            let links = || {
                ["config.toml", "AGENTS.md", "skills"].map(|name| {
                    let path = h.join(name);
                    let m = std::fs::symlink_metadata(&path).unwrap();
                    (ObjectRef::of(&m), std::fs::read_link(path).ok())
                })
            };
            let original_links = links();
            let home_count = || {
                std::fs::read_dir(f.data.join("account-homes"))
                    .unwrap()
                    .count()
            };
            let mut active = f.setup();
            let launch = f.resolve(&mut active);
            assert!(
                active.preview_project(Some(q.clone())).is_err(),
                "resolve alone is not Root admission"
            );
            let RootInputs {
                launch,
                data,
                allow_operational,
            } = active.admit_root(launch, Ok(f.data.clone()));
            assert!(allow_operational);
            let desktop = Arc::new(Mutex::new(active));
            let (state, home) = crate::freeze_startup_state(launch, desktop.clone(), Value::Null);
            crate::initialize_startup_consumers(
                &state,
                &home,
                data,
                allow_operational,
                true,
                Some(f.data.join("records")),
                None,
                f.shared.clone().map(Some),
            );
            let original_home = state.homes.lock().unwrap().active();
            let original_bootstrap = state
                .home_bootstrap
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let original_namespaces = state
                .native_namespaces
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .clone();
            let context = state.project_context.view();
            let attachments = state
                .attachment_selection
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .snapshot();
            let recovery = home.recovery_startup.lock().unwrap().snapshot();
            let choices = home
                .access_selection
                .lock()
                .unwrap()
                .as_ref()
                .map(|s| s.snapshot());
            let records_root = records_store::current().unwrap().root;
            let target = with_project.then(|| q.clone());
            let preview = desktop
                .lock()
                .unwrap()
                .preview_project(target.clone())
                .unwrap();
            assert_eq!(preview["affirmative"], "Save project for next launch");
            assert!(!desktop
                .lock()
                .unwrap()
                .preview_statement(preview["token"].as_str().unwrap())
                .unwrap()
                .contains("Create NEW"));
            let result = crate::desktop_setup_confirmation::prepare(
                &desktop,
                preview["token"].as_str().unwrap(),
                |_, action| {
                    assert_eq!(action, "Save project for next launch");
                    Ok(tauri_plugin_dialog::MessageDialogResult::Custom(
                        action.into(),
                    ))
                },
            )
            .unwrap();
            assert_eq!(
                result["pending"]["accountHome"],
                saved["pending"]["accountHome"]
            );
            assert_eq!(links(), original_links);
            assert_eq!(home_count(), 1);
            let mut expected = before_request.clone();
            expected["project"] =
                serde_json::to_value(target.as_ref().map(|p| Reference::observe(p).unwrap()))
                    .unwrap();
            assert_eq!(
                serde_json::to_value(read_profile(&f.data.join(PROFILE)).unwrap()).unwrap(),
                expected
            );
            assert!(Arc::ptr_eq(
                &original_home,
                &state.homes.lock().unwrap().active()
            ));
            assert!(Arc::ptr_eq(
                &original_bootstrap,
                state.home_bootstrap.lock().unwrap().as_ref().unwrap()
            ));
            assert!(Arc::ptr_eq(
                &original_namespaces,
                state.native_namespaces.lock().unwrap().as_ref().unwrap()
            ));
            assert_eq!(state.workspace.as_deref(), Some(f.project.as_path()));
            assert_eq!(home.host_config.as_ref().unwrap().cwd, f.project);
            assert_eq!(state.project_context.view(), context);
            assert_eq!(
                state
                    .attachment_selection
                    .lock()
                    .unwrap()
                    .as_ref()
                    .unwrap()
                    .snapshot(),
                attachments
            );
            assert_eq!(home.recovery_startup.lock().unwrap().snapshot(), recovery);
            assert_eq!(
                home.access_selection
                    .lock()
                    .unwrap()
                    .as_ref()
                    .map(|s| s.snapshot()),
                choices
            );
            assert_eq!(records_store::current().unwrap().root, records_root);
            assert!(desktop.lock().unwrap().recheck_active().is_ok());
            assert!(desktop
                .lock()
                .unwrap()
                .preview_project(None)
                .unwrap_err()
                .contains("Pending desktop request"));
            drop((
                state,
                home,
                desktop,
                original_home,
                original_bootstrap,
                original_namespaces,
            ));

            let mut fresh = f.setup();
            let launch = f.resolve(&mut fresh);
            let RootInputs {
                launch,
                data,
                allow_operational,
            } = fresh.admit_root(launch, Ok(f.data.clone()));
            assert!(allow_operational);
            let cfg = launch.host_config.as_ref().unwrap();
            assert_eq!(cfg.codex_home, h);
            assert_eq!(cfg.cwd, target.clone().unwrap_or(f.data.clone()));
            assert_eq!(cfg.records_project, with_project);
            let (next, next_home) =
                crate::freeze_startup_state(launch, Arc::new(Mutex::new(fresh)), Value::Null);
            crate::initialize_startup_consumers(
                &next,
                &next_home,
                data,
                allow_operational,
                true,
                Some(f.data.join("records")),
                None,
                f.shared.clone().map(Some),
            );
            assert_eq!(next.workspace, target);
            assert_eq!(next_home.host_config.as_ref().unwrap().codex_home, h);
            next.home_bootstrap
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .validate_binding(HomeClass::Account, next_home.host_config.as_ref().unwrap())
                .unwrap();
            assert!(next.native_namespaces.lock().unwrap().is_ok());
            assert_eq!(
                next.app_user_data_root.lock().unwrap().as_ref().unwrap(),
                &f.data
            );
            assert_eq!(
                next_home
                    .attachment_custody
                    .lock()
                    .unwrap()
                    .as_ref()
                    .unwrap()
                    .root(),
                f.data
            );
            assert_eq!(
                next.attachment_selection
                    .lock()
                    .unwrap()
                    .as_ref()
                    .unwrap()
                    .snapshot()["launchAppProjectObservation"]["nativeRoot"],
                target
                    .as_ref()
                    .map(|p| native_path_identity(p))
                    .unwrap_or(Value::Null)
            );
            assert_eq!(next_home.host.snapshot()["state"], "absent");
            assert!(next_home.host.snapshot()["generation"].is_null());
            assert_eq!(links(), original_links);
            assert_eq!(home_count(), 1);
            assert!(!h.join("auth.json").exists());
        }
        records_store::restore_configured_for_test(previous_store);
    }

    #[test]
    fn retained_project_requires_admission_and_refuses_stale_or_superseded_sources() {
        for case in [
            "setup-only",
            "pending-only",
            "refused",
            "environment",
            "home",
            "shared",
            "old-project",
            "next-project",
            "custody",
            "disk-replaced",
            "new-pending",
            "overlap",
        ] {
            let f = Fixture::new();
            let q = f.root.join("Q");
            std::fs::create_dir(&q).unwrap();
            let mut setup = f.setup();
            if case == "setup-only" {
                assert!(setup.preview_project(Some(q)).is_err());
                continue;
            }
            let saved = f.prepare(&mut setup, true);
            if case == "pending-only" {
                setup.launch_state = json!({"state":"saved-request"});
                assert!(setup.preview_project(Some(q)).is_err());
                continue;
            }
            if case == "refused" {
                let mut refused = f.setup();
                let launch =
                    refused.resolve(None, true, || panic!("contending owner must not bind"));
                assert!(
                    !refused
                        .admit_root(launch, Ok(f.data.clone()))
                        .allow_operational
                );
                assert!(refused.preview_project(Some(q)).is_err());
                continue;
            }
            drop(setup);
            let mut active = f.setup();
            let env = if case == "environment" {
                crate::explicit_environment_launch(
                    |key| (key == "CHIRALITY_CODEX_BIN").then(|| "/invented/bin/codex".into()),
                    &Ok(f.data.clone()),
                    &Ok(f.resources.clone()),
                    true,
                    || panic!("incomplete environment"),
                )
            } else {
                None
            };
            let launch = active.resolve(env, true, || f.probe());
            active.admit_root(launch, Ok(f.data.clone()));
            if case == "environment" {
                assert!(active.preview_project(Some(q)).is_err());
                continue;
            }
            let h = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
            if case == "overlap" {
                assert!(active.preview_project(Some(h)).is_err());
                continue;
            }
            let preview = active.preview_project(Some(q.clone())).unwrap();
            let token = preview["token"].as_str().unwrap();
            match case {
                "home" => {
                    std::fs::rename(&h, h.with_extension("old")).unwrap();
                    std::fs::create_dir(&h).unwrap();
                }
                "shared" => {
                    std::fs::rename(&f.shared[0], f.shared[0].with_extension("old")).unwrap();
                    std::fs::write(&f.shared[0], b"replacement fixture").unwrap();
                }
                "old-project" => {
                    std::fs::rename(&f.project, f.project.with_extension("old")).unwrap();
                    std::fs::create_dir(&f.project).unwrap();
                }
                "next-project" => {
                    std::fs::rename(&q, q.with_extension("old")).unwrap();
                    std::fs::create_dir(&q).unwrap();
                }
                "custody" => {
                    std::fs::rename(f.data.join("desktop-startup"), f.data.join("old-profile"))
                        .unwrap();
                    protected_directory(&f.data.join("desktop-startup")).unwrap();
                }
                "disk-replaced" => {
                    let request = read_profile(&f.data.join(PROFILE)).unwrap();
                    write_profile(&f.data.join(PROFILE), &request).unwrap();
                }
                "new-pending" => {
                    f.prepare(&mut active, false);
                }
                _ => unreachable!(),
            }
            let before = std::fs::read(f.data.join(PROFILE)).ok();
            assert!(active.prepare_and_save(token).is_err(), "{case}");
            assert_eq!(std::fs::read(f.data.join(PROFILE)).ok(), before, "{case}");
        }
    }

    #[test]
    fn joined_empty_setup_prepare_protected_request_fresh_root_and_native_consumers() {
        let f = Fixture::new();
        let mut setup = f.setup();
        let empty = setup.resolve(None, true, || {
            panic!("empty setup must not allocate/probe/execute a supplier")
        });
        assert!(empty.workspace.is_none());
        assert!(empty
            .host_config
            .unwrap_err()
            .contains("Desktop setup required"));
        assert_eq!(setup.view()["launch"]["state"], "setup-required");
        assert!(!f.data.join(PROFILE).exists());
        let saved = f.prepare(&mut setup, true);
        let account = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
        assert_eq!(
            std::fs::read_link(account.join("config.toml")).unwrap(),
            f.shared[0]
        );
        assert!(!account.join("auth.json").exists());
        let profile = f.data.join(PROFILE);
        assert_eq!(std::fs::metadata(&profile).unwrap().mode() & 0o777, 0o600);
        assert_eq!(
            std::fs::metadata(profile.parent().unwrap()).unwrap().mode() & 0o777,
            0o700
        );
        let serialized = std::fs::read_to_string(&profile).unwrap();
        assert!(
            !serialized.contains("credential")
                && !serialized.contains("model")
                && !serialized.contains("provider")
                && !serialized.contains("trust")
                && !serialized.contains("lock")
        );
        assert_eq!(
            setup.view()["launch"]["state"],
            "setup-required",
            "save cannot promote the live tuple"
        );
        drop(setup); // simulated fresh process releases actual OS-held ownership
        let mut fresh = f.setup();
        let launch = f.resolve(&mut fresh);
        let RootInputs {
            launch,
            data,
            allow_operational,
        } = fresh.admit_root(launch, Ok(f.data.clone()));
        assert!(allow_operational);
        let cfg = launch.host_config.as_ref().unwrap();
        assert_eq!(cfg.codex_home, account);
        assert_eq!(cfg.cwd, f.project);
        assert!(cfg.records_project);
        assert_eq!(cfg.codex_bin, f.resources.join("codex/bin/codex"));
        assert_eq!(
            cfg.expected_sha256.as_deref(),
            Some("112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b")
        );
        assert!(cfg.allow_unverified_dev);
        assert!(cfg.distribution.is_none());
        let bootstrap = launch.bootstrap.as_ref().unwrap();
        bootstrap.validate_binding(HomeClass::Account, cfg).unwrap();
        assert!(launch.namespaces.as_ref().unwrap().is_ok());
        let desktop = Arc::new(Mutex::new(fresh));
        let (state, home) = crate::freeze_startup_state(launch, desktop.clone(), Value::Null);
        assert_eq!(state.workspace.as_deref(), Some(f.project.as_path()));
        assert!(state
            .project_context
            .view()
            .to_string()
            .contains(f.project.to_str().unwrap()));
        assert_eq!(home.host_config.as_ref().unwrap().codex_home, account);
        assert!(state
            .home_bootstrap
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .validate_binding(HomeClass::Account, home.host_config.as_ref().unwrap())
            .is_ok());
        assert_eq!(
            state
                .attachment_selection
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .snapshot()["launchAppProjectObservation"]["nativeRoot"],
            native_path_identity(&f.project)
        );
        // The very initializer called by run receives the admitted Root data.
        // Its actual records/install/capture/attachment/REC/instruction joins
        // execute on invented data only, and never call Host::start.
        let previous_store = records_store::configured_for_test();
        crate::initialize_startup_consumers(
            &state,
            &home,
            data,
            allow_operational,
            true,
            Some(f.data.join("records")),
            None,
            [
                Some(f.shared[0].clone()),
                Some(f.shared[1].clone()),
                Some(f.shared[2].clone()),
            ],
        );
        assert_eq!(
            state.app_user_data_root.lock().unwrap().as_ref().unwrap(),
            &f.data
        );
        assert_eq!(
            home.attachment_custody
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .root(),
            f.data
        );
        assert!(state.instructions_root.lock().unwrap().is_ok());
        records_store::restore_configured_for_test(previous_store);
        assert_eq!(home.host.snapshot()["state"], "absent");
        assert!(home.host.snapshot()["generation"].is_null());
        assert!(home.host.snapshot()["threads"]
            .as_array()
            .is_none_or(|t| t.is_empty()));
        assert!(!account.join("auth.json").exists());
        assert!(
            !f.resources.exists(),
            "the joined proof never executes/reads a supplier"
        );
        let original_home = state.homes.lock().unwrap().active();
        let original_context = state.project_context.view();
        let original_attachments = state
            .attachment_selection
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .snapshot();
        let original_recovery = home.recovery_startup.lock().unwrap().snapshot();
        let original_bootstrap = state
            .home_bootstrap
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .clone();
        f.prepare(&mut desktop.lock().unwrap(), false);
        assert!(Arc::ptr_eq(
            &original_home,
            &state.homes.lock().unwrap().active()
        ));
        assert!(Arc::ptr_eq(
            &original_bootstrap,
            state.home_bootstrap.lock().unwrap().as_ref().unwrap()
        ));
        assert_eq!(state.project_context.view(), original_context);
        assert_eq!(
            state
                .attachment_selection
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .snapshot(),
            original_attachments
        );
        assert_eq!(
            home.recovery_startup.lock().unwrap().snapshot(),
            original_recovery
        );
        assert_eq!(state.workspace.as_deref(), Some(f.project.as_path()));
        assert_eq!(home.host.snapshot()["state"], "absent");
        assert!(state.act.lock().unwrap().is_some());
        assert!(state.role_log.is_ok());
    }

    #[test]
    fn saved_home_has_no_implicit_project_and_explicit_missing_resources_do_not_veto_start() {
        let f = Fixture::new();
        for p in [&f.shared[0], &f.shared[1]] {
            std::fs::remove_file(p).unwrap();
        }
        let mut setup = f.setup();
        let saved = f.prepare(&mut setup, false);
        assert!(saved["pending"]["resources"]
            .as_array()
            .unwrap()
            .iter()
            .any(|r| r["state"] == "TargetMissing"));
        drop(setup);
        let mut fresh = f.setup();
        let launch = f.resolve(&mut fresh);
        let cfg = launch.host_config.as_ref().unwrap();
        assert!(!cfg.records_project);
        assert_eq!(cfg.cwd, f.data);
        assert!(launch.workspace.is_none());
        assert!(launch.bootstrap.is_some());
        assert!(
            launch.namespaces.as_ref().unwrap().is_err(),
            "existing feature-level namespace refusal is retained"
        );
        assert!(crate::runtime_session::freeze_configured_project(None)
            .unwrap()
            .view()["reference"]
            .is_null());
        assert_eq!(Host::new().snapshot()["state"], "absent");
    }

    #[test]
    fn incomplete_environment_is_exclusive_and_keeps_original_error_without_profile_fallback() {
        let f = Fixture::new();
        let mut setup = f.setup();
        f.prepare(&mut setup, true);
        drop(setup);
        let env = crate::explicit_environment_launch(
            |key| (key == "CHIRALITY_CODEX_BIN").then(|| "/invented/bin/codex".into()),
            &Ok(f.data.clone()),
            &Ok(f.resources.clone()),
            true,
            || panic!("incomplete environment cannot allocate probe"),
        )
        .unwrap();
        let mut setup = f.setup();
        let launch = setup.resolve(Some(env), true, || panic!("no fallback/probe"));
        assert_eq!(
            launch.host_config.unwrap_err(),
            "CHIRALITY_CODEX_HOME is not set: no App-owned Codex home given"
        );
        assert!(launch.workspace.is_none());
        assert!(setup.lease.is_none());
        assert!(setup.requested.is_none());
        assert_eq!(setup.view()["launch"]["state"], "environment");
        let launch = Launch::environment(
            None,
            Err("explicit environment error".into()),
            None,
            [None, None, None],
        );
        let inputs = setup.admit_root(launch, Err("environment App data unavailable".into()));
        assert!(
            inputs.allow_operational,
            "preserve independent environment records override semantics"
        );
        assert_eq!(inputs.data.unwrap_err(), "environment App data unavailable");
    }

    #[test]
    fn unavailable_and_broken_resource_metadata_is_visible_without_new_home_start_veto() {
        let f = Fixture::new();
        let mut setup = f.setup();
        std::fs::remove_file(&f.shared[0]).unwrap();
        let saved = f.prepare(&mut setup, false);
        drop(setup);
        let account = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
        // CL-4/Q-1: a divergent receiving file is preserved and shown; there is
        // no automatic relink/copy and no stronger startup veto.
        std::fs::remove_file(account.join("AGENTS.md")).unwrap();
        std::fs::write(
            account.join("AGENTS.md"),
            b"invented divergent receiving file",
        )
        .unwrap();
        let mut fresh = f.setup();
        let launch = f.resolve(&mut fresh);
        assert!(launch.host_config.is_ok());
        let resources = fresh.view()["activeResources"].as_array().unwrap().clone();
        assert!(resources
            .iter()
            .any(|r| r["name"] == "config.toml" && r["state"] == "TargetMissing"));
        assert!(resources
            .iter()
            .any(|r| r["name"] == "AGENTS.md" && r["state"] == "Conflict"));
        assert!(!std::fs::symlink_metadata(account.join("AGENTS.md"))
            .unwrap()
            .file_type()
            .is_symlink());
        drop(fresh);
        // CL-6: the originally absent explicit target can appear. Its actual
        // object is frozen in memory on this launch, never written as trust.
        std::fs::write(&f.shared[0], b"invented now-available resource").unwrap();
        let mut fresh = f.setup();
        assert!(f.resolve(&mut fresh).host_config.is_ok());
        assert!(fresh.requested.as_ref().unwrap().shared[0].object.is_some());
        assert!(read_profile(&f.data.join(PROFILE)).unwrap().shared[0]
            .object
            .is_none());
        std::fs::rename(&f.shared[0], f.shared[0].with_extension("old")).unwrap();
        std::fs::write(&f.shared[0], b"replacement inode").unwrap();
        assert!(fresh.recheck().unwrap_err().contains("replaced"));
    }

    #[test]
    fn compiled_successor_does_not_take_the_desktop_development_fallback() {
        if !cfg!(feature = "distribution-successor") {
            return;
        }
        let f = Fixture::new();
        let mut setup = f.setup();
        f.prepare(&mut setup, false);
        drop(setup);
        let mut fresh = f.setup();
        let launch = fresh.resolve(None, false, || f.probe());
        let cfg = launch.host_config.unwrap();
        assert!(matches!(
            cfg.distribution,
            Some(crate::hosting::successor::Distribution::Production { .. })
        ));
        assert!(
            !cfg.allow_unverified_dev
                && cfg.expected_sha256.is_none()
                && cfg.require_distribution_artifacts
        );
        assert!(
            !f.resources.exists(),
            "this source-selection fixture never probes/executes a supplier"
        );
    }

    #[test]
    fn refused_admission_cannot_reach_actual_root_data_consumers_even_with_records_override() {
        let previous_store = records_store::configured_for_test();
        for case in [
            "empty",
            "profile-owner",
            "home-owner",
            "stale-before-resolve",
            "stale-after-resolve",
        ] {
            let f = Fixture::new();
            let mut setup = f.setup();
            let mut profile_owner = None;
            let mut home_owner = None;
            let account = if case == "empty" {
                None
            } else {
                let saved = f.prepare(&mut setup, true);
                drop(setup);
                setup = f.setup();
                Some(PathBuf::from(
                    saved["pending"]["accountHome"].as_str().unwrap(),
                ))
            };
            match case {
                "profile-owner" => profile_owner = Some(DirectoryLease::acquire(&f.data).unwrap()),
                "home-owner" => {
                    let alias = f.root.join("receiving-home-alias");
                    std::os::unix::fs::symlink(account.as_ref().unwrap(), &alias).unwrap();
                    // An invented cooperating holder opens the actual inode
                    // through an alias, without holding the App-data lease.
                    let file = File::open(alias).unwrap();
                    assert_eq!(
                        unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) },
                        0
                    );
                    home_owner = Some(file);
                }
                "stale-before-resolve" => {
                    let account = account.as_ref().unwrap();
                    std::fs::rename(account, account.with_extension("old")).unwrap();
                    std::fs::create_dir(account).unwrap();
                }
                _ => {}
            }
            let mut probe_called = false;
            let launch = setup.resolve(None, true, || {
                probe_called = true;
                f.probe()
            });
            if case == "stale-after-resolve" {
                assert!(launch.host_config.is_ok());
                let account = account.as_ref().unwrap();
                std::fs::rename(account, account.with_extension("old")).unwrap();
                std::fs::create_dir(account).unwrap();
            } else {
                assert!(!probe_called, "{case}");
            }
            // No hand-written Err: this exact adapter is called by run, and
            // supplies all arguments to its real operational consumer join.
            let RootInputs {
                launch,
                data,
                allow_operational,
            } = setup.admit_root(launch, Ok(f.data.clone()));
            assert!(!allow_operational, "{case}");
            assert!(data.is_err(), "{case}");
            assert!(launch.workspace.is_none());
            assert!(launch.host_config.is_err());
            assert!(launch.bootstrap.is_none());
            let desktop = Arc::new(Mutex::new(setup));
            let (state, home) = crate::freeze_startup_state(launch, desktop.clone(), Value::Null);
            let entries = || {
                let mut paths: Vec<_> = std::fs::read_dir(&f.data)
                    .unwrap()
                    .map(|e| e.unwrap().file_name())
                    .collect();
                paths.sort();
                paths
            };
            let before = entries();
            crate::initialize_startup_consumers(
                &state,
                &home,
                data,
                allow_operational,
                true,
                Some(f.root.join("must-not-open-records")),
                None,
                [None, None, None],
            );
            records_store::use_store_for_test(None);
            assert!(
                records_store::current()
                    .unwrap_err()
                    .contains("not admitted"),
                "{case}"
            );
            assert!(!f.root.join("must-not-open-records").exists());
            assert_eq!(
                entries(),
                before,
                "refusal must not install/capture/seed/open Root data: {case}"
            );
            assert!(state.workspace.is_none());
            assert!(state.act.lock().unwrap().is_none());
            assert!(state.role_log.is_err());
            assert!(state.app_user_data_root.lock().unwrap().is_err());
            assert!(state.instructions_root.lock().unwrap().is_err());
            assert!(state.home_bootstrap.lock().unwrap().is_err());
            assert!(state.native_namespaces.lock().unwrap().is_err());
            assert!(home.attachment_custody.lock().unwrap().is_err());
            assert!(state
                .attachment_selection
                .lock()
                .unwrap()
                .as_ref()
                .unwrap()
                .snapshot()["launchAppProjectObservation"]["nativeRoot"]
                .is_null());
            assert_eq!(home.host.snapshot()["state"], "absent");
            assert!(home.host.snapshot()["generation"].is_null());
            assert_eq!(
                desktop.lock().unwrap().view()["launch"]["state"],
                "setup-required"
            );
            // Metadata preview is still a setup-only capability, with no
            // operational root admitted or active owner replaced.
            assert!(desktop
                .lock()
                .unwrap()
                .preview(f.shared.clone(), None, SUPPLIER)
                .is_ok());
            drop((profile_owner, home_owner));
        }
        records_store::restore_configured_for_test(previous_store);
    }

    #[test]
    fn app_owned_key_and_identity_domains_refuse_shared_preview_and_saved_admission() {
        let mut failures = Vec::new();
        for present in [false, true] {
            for (relative, index, slot) in [
                ("capture-seal/keys.json", 0, "config.toml"),
                ("installation.json", 0, "config.toml"),
                ("capture-seal", 2, "skills"),
            ] {
                let f = Fixture::new();
                let collision = f.data.join(relative);
                if present {
                    if slot == "skills" {
                        protected_directory(&collision).unwrap();
                    } else {
                        protected_directory(collision.parent().unwrap()).unwrap();
                        std::fs::write(
                            &collision,
                            b"invented operational metadata; no keys or credentials",
                        )
                        .unwrap();
                    }
                }
                let case = format!("{relative}, target present={present}");
                let mut shared = f.shared.clone();
                shared[index] = collision.clone();
                let mut setup = f.setup();
                match setup.preview(shared, Some(f.project.clone()), SUPPLIER) {
                    Err(reason) => assert!(reason.contains("overlap"), "{case}: {reason}"),
                    Ok(_) => failures.push(format!("colliding preview accepted: {case}")),
                }
                assert!(
                    !f.data.join(PROFILE).exists(),
                    "preview must not persist: {case}"
                );
                assert!(
                    !f.data.join("account-homes").exists(),
                    "preview must not prepare: {case}"
                );

                // Produce a real protected request/home through the ordinary
                // prepare event, then model a previously saved colliding choice.
                // Both the reference and actual receiving link name the collision;
                // this is not a JSON-only model or an engine/credential fixture.
                let saved = f.prepare(&mut setup, true);
                let account = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
                let mut requested = read_profile(&f.data.join(PROFILE)).unwrap();
                requested.shared[index] = Reference::observe(&collision).unwrap();
                std::fs::remove_file(account.join(slot)).unwrap();
                std::os::unix::fs::symlink(&collision, account.join(slot)).unwrap();
                write_profile(&f.data.join(PROFILE), &requested).unwrap();
                drop(setup);

                let mut fresh = f.setup();
                let mut probe_called = false;
                let launch = fresh.resolve(None, true, || {
                    probe_called = true;
                    f.probe()
                });
                let inputs = fresh.admit_root(launch, Ok(f.data.clone()));
                if probe_called
                    || inputs.allow_operational
                    || inputs.data.is_ok()
                    || inputs.launch.workspace.is_some()
                    || inputs.launch.host_config.is_ok()
                    || inputs.launch.bootstrap.is_some()
                    || inputs.launch.namespaces.is_some()
                {
                    failures.push(format!(
                        "colliding saved request reached startup admission: {case}"
                    ));
                } else {
                    assert_eq!(fresh.view()["launch"]["state"], "setup-required", "{case}");
                    assert!(
                        fresh.view()["launch"]["reason"]
                            .as_str()
                            .unwrap()
                            .contains("overlap"),
                        "{case}"
                    );
                }
                assert_eq!(
                    collision.exists(),
                    present,
                    "admission must not publish operational metadata: {case}"
                );
            }
        }
        assert!(failures.is_empty(), "{}", failures.join("\n"));
    }

    #[test]
    fn malformed_stale_overlapping_and_replaced_sources_refuse_before_root_binding() {
        for case in [
            "incomplete",
            "receiving-replaced",
            "source-replaced",
            "source-alias",
            "source-hardalias",
            "receiving-public",
            "profile-fifo",
            "injected-flag",
            "overlap",
            "profile-hardlink",
            "profile-public",
            "oversize",
        ] {
            let f = Fixture::new();
            let mut setup = f.setup();
            let saved = f.prepare(&mut setup, true);
            drop(setup);
            let account = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
            match case {
                "incomplete" => std::fs::write(f.data.join(PROFILE), b"{}").unwrap(),
                "receiving-replaced" => {
                    std::fs::rename(&account, account.with_extension("old")).unwrap();
                    std::fs::create_dir(&account).unwrap();
                }
                "source-replaced" => {
                    std::fs::rename(&f.shared[0], f.shared[0].with_extension("old")).unwrap();
                    std::fs::write(&f.shared[0], b"new identity").unwrap();
                }
                "source-alias" => {
                    std::fs::rename(&f.shared[0], f.shared[0].with_extension("old")).unwrap();
                    std::os::unix::fs::symlink(&f.shared[1], &f.shared[0]).unwrap();
                }
                "source-hardalias" => {
                    std::fs::hard_link(&f.shared[0], f.root.join("aliased-shared-file")).unwrap();
                }
                "receiving-public" => {
                    std::fs::set_permissions(&account, std::fs::Permissions::from_mode(0o755))
                        .unwrap();
                }
                "injected-flag" => {
                    let mut request: Value =
                        serde_json::from_slice(&std::fs::read(f.data.join(PROFILE)).unwrap())
                            .unwrap();
                    request["allowUnverified"] = json!(true);
                    std::fs::write(f.data.join(PROFILE), serde_json::to_vec(&request).unwrap())
                        .unwrap();
                }
                "profile-fifo" => {
                    std::fs::remove_file(f.data.join(PROFILE)).unwrap();
                    use std::os::unix::ffi::OsStrExt;
                    let path = std::ffi::CString::new(f.data.join(PROFILE).as_os_str().as_bytes())
                        .unwrap();
                    assert_eq!(unsafe { libc::mkfifo(path.as_ptr(), 0o600) }, 0);
                }
                "overlap" => {
                    let mut request = read_profile(&f.data.join(PROFILE)).unwrap();
                    request.project = Some(Reference::observe(&account).unwrap());
                    write_profile(&f.data.join(PROFILE), &request).unwrap();
                }
                "profile-hardlink" => {
                    std::fs::hard_link(f.data.join(PROFILE), f.root.join("alias-request")).unwrap()
                }
                "profile-public" => std::fs::set_permissions(
                    f.data.join(PROFILE),
                    std::fs::Permissions::from_mode(0o644),
                )
                .unwrap(),
                "oversize" => {
                    std::fs::write(f.data.join(PROFILE), vec![b' '; LIMIT as usize + 1]).unwrap()
                }
                _ => unreachable!(),
            }
            let mut fresh = f.setup();
            let launch = fresh.resolve(None, true, || {
                panic!("invalid source must refuse before probe allocation/binding")
            });
            assert!(launch.host_config.is_err(), "{case}");
            assert!(launch.workspace.is_none(), "{case}");
            assert!(launch.bootstrap.is_none());
            assert_eq!(fresh.view()["launch"]["state"], "setup-required");
        }
    }

    #[test]
    fn held_inode_custody_refuses_competitors_aliases_and_directory_replacement() {
        let f = Fixture::new();
        let mut setup = f.setup();
        f.prepare(&mut setup, true);
        drop(setup);
        let mut first = f.setup();
        assert!(f.resolve(&mut first).host_config.is_ok());
        let peer = std::process::Command::new(std::env::current_exe().unwrap())
            .args([
                "--exact",
                "desktop_startup::tests::custody_peer",
                "--nocapture",
            ])
            .env("CHIRALITY_DESKTOP_FIXTURE_LOCK", &f.data)
            .output()
            .unwrap();
        assert!(
            peer.status.success(),
            "invented peer process: {}",
            String::from_utf8_lossy(&peer.stderr)
        );
        let home = first
            .requested
            .as_ref()
            .unwrap()
            .account
            .location
            .path()
            .unwrap();
        let peer = std::process::Command::new(std::env::current_exe().unwrap())
            .args([
                "--exact",
                "desktop_startup::tests::custody_peer",
                "--nocapture",
            ])
            .env("CHIRALITY_DESKTOP_FIXTURE_LOCK", home)
            .output()
            .unwrap();
        assert!(
            peer.status.success(),
            "receiving-home inode lease must also exclude the separate peer"
        );
        let mut second = f.setup();
        let blocked = second.resolve(None, true, || panic!("competing owner must not bind"));
        assert!(blocked.host_config.unwrap_err().contains("already in use"));
        let alias = f.root.join("data-alias");
        std::os::unix::fs::symlink(&f.data, &alias).unwrap();
        let mut alias_setup = DesktopSetup::new(Ok(alias), Ok(f.resources.clone()));
        assert!(alias_setup
            .resolve(None, true, || panic!("alias owner must not bind"))
            .host_config
            .unwrap_err()
            .contains("already in use"));
        // Replacing a child lock/profile pathname cannot replace the actual
        // held App-data directory inode lock.
        std::fs::rename(
            f.data.join("desktop-startup"),
            f.data.join("desktop-startup-old"),
        )
        .unwrap();
        protected_directory(&f.data.join("desktop-startup")).unwrap();
        std::fs::copy(
            f.data.join("desktop-startup-old/request.json"),
            f.data.join(PROFILE),
        )
        .unwrap();
        assert!(first.recheck().unwrap_err().contains("replaced"));
        assert!(DirectoryLease::acquire(&f.data)
            .err()
            .unwrap()
            .contains("already in use"));
        std::fs::rename(&f.data, f.root.join("moved-data")).unwrap();
        protected_directory(&f.data).unwrap();
        assert!(first.recheck().is_err());
        // A copied request still names the original source inode/location.
        protected_directory(&f.data.join("desktop-startup")).unwrap();
        std::fs::copy(
            f.root.join("moved-data/desktop-startup/request.json"),
            f.data.join(PROFILE),
        )
        .unwrap();
        let mut replaced = f.setup();
        assert!(replaced
            .resolve(None, true, || panic!("replaced data source must not bind"))
            .host_config
            .is_err());
    }

    #[test]
    fn custody_peer() {
        let Some(path) = std::env::var_os("CHIRALITY_DESKTOP_FIXTURE_LOCK") else {
            return;
        };
        assert!(DirectoryLease::acquire(Path::new(&path))
            .err()
            .unwrap()
            .contains("already in use"));
    }

    #[test]
    fn mounted_setup_packets() {
        let f = Fixture::new();
        let mut setup = f.setup();
        let empty = setup.resolve(None, true, || panic!("setup has no probe"));
        let RootInputs {
            launch,
            data,
            allow_operational,
        } = setup.admit_root(empty, Ok(f.data.clone()));
        assert!(launch.host_config.is_err() && data.is_err() && !allow_operational);
        let initial = setup.view();
        let preview = setup
            .preview(f.shared.clone(), Some(f.project.clone()), SUPPLIER)
            .unwrap();
        let saved = setup
            .prepare_and_save(preview["token"].as_str().unwrap())
            .unwrap();
        assert_eq!(saved["launch"]["state"], "setup-required");
        let mut busy = f.setup();
        let launch = busy.resolve(None, true, || panic!("busy source does not bind"));
        busy.admit_root(launch, Ok(f.data.clone()));
        let busy = busy.view();
        drop(setup);
        let mut fresh = f.setup();
        let launch = f.resolve(&mut fresh);
        let RootInputs {
            launch,
            data,
            allow_operational,
        } = fresh.admit_root(launch, Ok(f.data.clone()));
        assert!(launch.host_config.is_ok() && data.is_ok() && allow_operational);
        let fresh_view = fresh.view();
        std::fs::remove_file(&f.shared[0]).unwrap();
        let receiving = fresh
            .requested
            .as_ref()
            .unwrap()
            .account
            .location
            .path()
            .unwrap();
        std::fs::remove_file(receiving.join("AGENTS.md")).unwrap();
        std::fs::write(
            receiving.join("AGENTS.md"),
            b"invented broken link receiving file",
        )
        .unwrap();
        let resource_limits = fresh.view();
        let mut environment = f.setup();
        environment.resolve(
            Some(Launch::environment(
                Some(f.project.clone()),
                Ok(HostConfig::new(
                    f.resources.join("codex/bin/codex"),
                    f.root.join("explicit-env-home"),
                    f.root.join("explicit-env-probe"),
                    f.project.clone(),
                )),
                None,
                [None, None, None],
            )),
            true,
            || panic!("environment fixture does not execute a supplier"),
        );
        let keep = Fixture::new();
        let mut setup = keep.setup();
        keep.prepare(&mut setup, true);
        drop(setup);
        let mut active = keep.setup();
        let launch = keep.resolve(&mut active);
        assert!(
            active
                .admit_root(launch, Ok(keep.data.clone()))
                .allow_operational
        );
        let retain_initial = active.view();
        let q = keep.root.join("explicit-project-Q");
        std::fs::create_dir(&q).unwrap();
        let retain_preview = active.preview_project(Some(q.clone())).unwrap();
        let retain_saved = active
            .prepare_and_save(retain_preview["token"].as_str().unwrap())
            .unwrap();
        let conflict = active.view();
        let superseded = active
            .prepare_and_save(retain_preview["token"].as_str().unwrap())
            .unwrap_err();
        drop(active);
        let mut fresh_q = keep.setup();
        let launch = keep.resolve(&mut fresh_q);
        assert!(
            fresh_q
                .admit_root(launch, Ok(keep.data.clone()))
                .allow_operational
        );
        let q_view = fresh_q.view();
        let none_preview = fresh_q.preview_project(None).unwrap();
        let none_saved = fresh_q
            .prepare_and_save(none_preview["token"].as_str().unwrap())
            .unwrap();
        let retained = json!({"initial":retain_initial,"preview":retain_preview,"saved":retain_saved,"conflict":conflict,"supersededError":superseded,"freshQ":q_view,"nonePreview":none_preview,"noneSaved":none_saved,"project":native_path_identity(&q),"currentProject":native_path_identity(&keep.project)});
        println!(
            "DESKTOP_SETUP_PACKETS={}",
            json!({"retained":retained,"initial":initial,"preview":preview,"saved":saved,"busy":busy,"fresh":fresh_view,"resourceLimits":resource_limits,"environment":environment.view(),"inputs":{"shared":f.shared.each_ref().map(|p|native_path_identity(p)),"project":native_path_identity(&f.project)}})
        );
    }

    #[test]
    fn owning_plan_rejects_existing_home_and_nonlossless_paths_are_not_used() {
        let f = Fixture::new();
        let mut setup = f.setup();
        let preview = setup.preview(f.shared.clone(), None, SUPPLIER).unwrap();
        let account = PathBuf::from(preview["accountHome"].as_str().unwrap());
        protected_directory(account.parent().unwrap()).unwrap();
        std::fs::create_dir(&account).unwrap();
        assert!(setup
            .prepare_and_save(preview["token"].as_str().unwrap())
            .unwrap_err()
            .contains("never adopted"));
        assert!(!account.join("config.toml").exists());
        assert!(!f.data.join(PROFILE).exists());
        let raw = f.root.join(std::ffi::OsString::from_vec(vec![b'x', 0xff]));
        assert_eq!(NativePath::new(&raw).path().unwrap(), raw);
    }
}
