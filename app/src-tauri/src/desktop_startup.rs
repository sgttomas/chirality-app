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
/// App-owned settings created only by the explicit new-settings setup: a new
/// leaf per setup, beside (never inside) the protected App-data domains.
const SETTINGS: &str = "shared-settings";
/// What a person is told when another process holds this App data
/// (DEL-01-02). A conflicting lock shows that some process holds it, not
/// which one; and environment startup may have created a missing App data
/// directory before it found it held, so this says nothing operational was
/// started, not that nothing changed.
pub(crate) const DATA_HELD: &str = "Chirality did not start here: its data is held by another process on this computer. Nothing operational was started. If a Chirality window is already open, use it; otherwise quit whatever is using this data, then open Chirality again.";
/// A launch refused because a Codex home the saved request names is held: by
/// another process, or still by this App. Setup is not what is needed then.
fn home_held(reason: &str) -> bool {
    [crate::home_hold::IN_USE, crate::home_hold::IN_USE_HERE, crate::home_hold::KEPT].iter().any(|held| reason.contains(held))
}
fn data_held(reason: &str) -> bool {
    reason.contains(DATA_HELD)
}

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

/// The folder in the App data folder where desktop setup plans every account
/// home: each planned home is a new leaf directly in it. It only calculates
/// the path; it creates nothing. The records store's placement check
/// protects this whole folder, so every planned, pending and future desktop
/// account home is protected whether or not it exists yet.
pub(crate) fn desktop_account_homes(app_data: &Path) -> PathBuf {
    app_data.join("account-homes")
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
    /// For the App data directory: this process's note that it holds it, the
    /// positive evidence a session start may rely on
    /// ([`crate::session_liveness::establish_ended`]).
    app_data: Option<crate::session_liveness::AppDataHeld>,
}
impl DirectoryLease {
    /// The lease on the App data directory itself, noted as held.
    fn acquire_app_data(path: &Path) -> Result<Self, String> {
        let mut lease = Self::acquire_or(path, DATA_HELD)?;
        lease.app_data = Some(crate::session_liveness::note_app_data_held(&lease.file)?);
        Ok(lease)
    }
    fn acquire(path: &Path) -> Result<Self, String> {
        Self::acquire_or(path, "This directory is held by another process on this computer, so it was not used here (no wait)")
    }
    /// `held`: what is said when another open file description holds the lock.
    fn acquire_or(path: &Path, held: &str) -> Result<Self, String> {
        #[cfg(test)]
        crate::records_effect_guard::mutation_for_test("desktop_startup::DirectoryLease::acquire_or");
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
            let error = std::io::Error::last_os_error();
            // Held by some other process (which one is not known). Any
            // other failure is not "free" either.
            if matches!(error.raw_os_error(), Some(code) if code == libc::EWOULDBLOCK || code == libc::EAGAIN) {
                return Err(held.into());
            }
            return Err(format!(
                "desktop profile/home custody unavailable, so it is not treated as free (no wait): {error}"
            ));
        }
        let lease = Self {
            file,
            path: path.to_owned(),
            object: ObjectRef::of(&meta),
            app_data: None,
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
        // The note goes before the lock is released, never after.
        drop(self.app_data.take());
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
    /// The account home's inode lock, shared in this process with the Host
    /// that starts Codex on the same home (one holder per role).
    _hold: crate::home_hold::HomeHold,
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
        // No native lock file is created. Hold the actual receiving directory
        // inode exclusively for this process, independently of profile custody.
        let hold = crate::home_hold::hold_receiving(&file)?;
        let result = Self {
            file,
            reference: reference.clone(),
            _hold: hold,
        };
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

fn protected_directory(path: &Path) -> Result<(), String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("desktop_startup::protected_directory");
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
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("desktop_startup::write_profile");
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
    /// Another process holds this App data: nothing operational starts.
    fn data_held() -> Self {
        Self {
            workspace: None,
            host_config: Err(DATA_HELD.into()),
            key_path: None,
            shared_paths: [None, None, None],
            bootstrap: None,
            namespaces: None,
            source: "another process holds this App data",
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
    /// A new home whose three link targets are new, empty App-owned files and
    /// folder created at the confirmed prepare, in `settings` only.
    NewSettings { settings: PathBuf },
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
            // One App at a time holds an App data directory, on this route as
            // on the saved one: before the ledger opens or anything is written.
            // App data that did not resolve is never treated as held: nothing
            // operational starts, the records override included.
            let held = environment_data
                .as_ref()
                .map_err(Clone::clone)
                .and_then(|data| self.hold_environment_data(data));
            if let Err(reason) = held {
                return self.refuse_environment(&reason);
            }
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
            Err(reason) if data_held(&reason) => {
                self.receiving = None;
                self.requested = None;
                self.loaded_profile = None;
                self.admitted = None;
                self.launch_state = json!({"state":"data-held","reason":DATA_HELD,"operationalData":"not admitted; nothing operational started"});
                RootInputs {
                    launch: Launch::data_held(),
                    data: Err(format!("Desktop operational data not admitted: {DATA_HELD}")),
                    allow_operational: false,
                }
            }
            Err(reason) => {
                self.receiving = None;
                self.requested = None;
                self.loaded_profile = None;
                self.admitted = None;
                // A held home is not a missing setup: the saved request stands and is not shown as needed.
                self.launch_state = if home_held(&reason) {
                    json!({"state":"home-held","reason":reason,"operationalData":"not admitted; nothing operational started"})
                } else {
                    json!({"state":"setup-required","reason":reason,"operationalData":"not admitted; setup-only local input capability retained"})
                };
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
                if data_held(&reason) {
                    self.launch_state = json!({"state":"data-held","reason":DATA_HELD});
                    return Launch::data_held();
                }
                self.launch_state = json!({"state": if home_held(&reason) { "home-held" } else { "setup-required" }, "reason": reason});
                Launch::setup(reason)
            }
        }
    }
    /// The environment route refused because its App data did not resolve or
    /// could not be held: nothing operational starts and the actual reason is
    /// shown where the environment route's startup errors are shown.
    pub(crate) fn refuse_environment(&mut self, reason: &str) -> RootInputs {
        self.admitted = None;
        let refused = data_held(reason);
        let reason = if refused {
            DATA_HELD.to_string()
        } else {
            format!("App data could not be resolved and held, so nothing was started: {reason}")
        };
        self.launch_state = if refused {
            json!({"state":"data-held","reason":DATA_HELD,"operationalData":"not admitted; nothing operational started"})
        } else {
            json!({"state":"environment","reason":reason,"operationalData":"not admitted"})
        };
        RootInputs {
            launch: if refused {
                Launch::data_held()
            } else {
                Launch {
                    host_config: Err(reason.clone()),
                    workspace: None,
                    key_path: None,
                    shared_paths: [None, None, None],
                    bootstrap: None,
                    namespaces: None,
                    source: "explicit environment (App data not held)",
                }
            },
            data: Err(format!("App operational data not admitted: {reason}")),
            allow_operational: false,
        }
    }
    /// The environment route's App data hold: the same directory-inode lease
    /// the saved route takes, kept for the life of this setup (the process).
    pub(crate) fn hold_environment_data(&mut self, data: &Path) -> Result<(), String> {
        storage::check_path(data)?;
        if self.lease.is_none() {
            if !data.try_exists().map_err(|e| format!("App data unavailable: {e}"))? {
                protected_directory(data)?;
            }
            self.lease = Some(DirectoryLease::acquire_app_data(data)?);
        }
        self.lease.as_ref().unwrap().recheck()
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
            self.lease = Some(DirectoryLease::acquire_app_data(data)?);
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
        if account.parent() != Some(desktop_account_homes(&data).as_path()) {
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
            desktop_account_homes(&data),
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
        // One App at a time holds this App data, with or without a saved
        // request. The lease creates nothing; absent data has nothing to hold.
        if self.lease.is_none() && data.try_exists().map_err(|e| e.to_string())? {
            self.lease = Some(DirectoryLease::acquire_app_data(&data)?);
        }
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
        // On every route, before each Codex start: this App still holds its
        // App data, and its path still names the held directory (by device
        // and inode). App data not held starts nothing operational.
        match &self.lease {
            Some(lease) => lease.recheck().map_err(|e| format!("App data custody lost, so nothing was started: {e}"))?,
            None => return Err("App data is not held by this App, so nothing was started".into()),
        }
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
        let result = json!({"defaults":Self::first_use_defaults("retain-account-project"),"token":token,"kind":"retain-account-project","affirmative":"Save project for next launch","accountHome":account.display().to_string(),"project":project.as_ref().map(|p|p.display().to_string()),"effects":[format!("Retain the currently admitted account directory {}",account.display()),format!("Project on next launch: {}",project.as_ref().map(|p|p.display().to_string()).unwrap_or_else(||"explicitly absent".into())),"Save only a pending project request; create no home, links or credentials"],"resources":resource_view(&plan)?,"standing":"Original admitted account/shared/supplier references are retained; active workspace and all current owners/choices remain unchanged"});
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
            PreviewKind::NewSettings { .. } => "Create settings and save for next launch",
            PreviewKind::RetainProject { .. } => "Save project for next launch",
        })
    }
    /// What the review page says, before confirming, about what Codex can read and where a sign-in is
    /// kept. The App sets none of these: on the new-settings route Codex's own defaults apply (the
    /// pinned Codex's read-only profile, on-request approval and file credential storage, as read
    /// from its source and observed in one start), so they are said as defaults; on the other routes
    /// the settings in use decide and are not restated. What Codex reports for a launch or a
    /// conversation is shown after setup (Connection and access), never a default in its place.
    fn first_use_defaults(kind: &str) -> Value {
        match kind {
            "new-settings" => json!({"heading":"What applies by default","sentences":[
                "With new settings, Codex's own defaults apply; the App sets none of these.",
                "By default, Codex can read any file your Mac account can read, inside and outside your project, so choose a project folder with that in mind.",
                "By default your ChatGPT sign-in is kept as a file, auth.json, in the sign-in folder listed under Exact locations, readable only by your account. Connection and access shows where Codex keeps it before you sign in.",
                "After you reopen the App, Connection and access shows what Codex reports for this launch.",
            ]}),
            "new-home" => json!({"heading":"What applies","sentences":[
                "Your own Codex settings decide what Codex may read and change, and where your sign-in is kept. The App does not change them and does not restate them here; after you reopen the App, Connection and access shows what Codex reports for this launch.",
            ]}),
            _ => json!({"heading":"What applies","sentences":[
                "This keeps your current sign-in folder and the settings it uses: what Codex may read and change, and where your sign-in is kept, stay as they are. After you reopen the App, Connection and access shows what Codex reports for this launch.",
            ]}),
        }
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
        if let PreviewKind::NewSettings { settings } = &preview.kind {
            return Ok(format!("Create NEW App-owned settings folder: {}\nwith an empty config.toml, an empty AGENTS.md and a skills folder. Codex adds its own system skills there, and its own working files to the account directory, when it starts.\nCreate NEW App-owned account directory: {}\nLink its config.toml, AGENTS.md and skills to those new settings.\nRead, import or change no other Codex settings, home or credential.\nProject for next launch: {}\nSave a private pending request in {}.\nCodex: the copy included with this App ({SUPPLIER}).\nThe current workspace, homes, account/model choices, records and prepared messages stay unchanged. No automatic quit/restart/login/conversation.",settings.display(),preview.account.display(),preview.project.as_ref().map(|p|p.display().to_string()).unwrap_or_else(||"none".into()),self.data.as_ref().map_err(Clone::clone)?.join(PROFILE).display()));
        }
        Ok(format!("Create NEW App-owned account directory: {}\nCreate links (no content copy or credential import):\nconfig.toml → {}\nAGENTS.md → {}\nskills → {}\nProject for next launch: {}\nSave a private pending request in {}.\nSupplier: {} ({SUPPLIER}); unqualified owner-use development.\nThe current workspace, homes, account/model choices, records and prepared messages stay unchanged. No automatic quit/restart/login/conversation.",preview.account.display(),preview.shared.config_toml.display(),preview.shared.global_agents_md.display(),preview.shared.skills.display(),preview.project.as_ref().map(|p|p.display().to_string()).unwrap_or_else(||"explicitly absent".into()),self.data.as_ref().map_err(Clone::clone)?.join(PROFILE).display(),self.resources.as_ref().map_err(Clone::clone)?.join("codex/bin/codex").display()))
    }
    /// Paths originate in explicit person input or a native picker. This preview
    /// performs metadata/path validation only; no filesystem creation or save.
    /// First-use route: plan a new App-owned settings folder with empty
    /// `config.toml`, `AGENTS.md` and `skills/`, and a new home linked to them.
    /// Metadata/path validation only; nothing is created until the confirmed
    /// `prepare_and_save`. No other Codex settings or home is read.
    pub fn preview_new_settings(&mut self, project: Option<PathBuf>) -> Result<Value, String> {
        self.config_epoch = None;
        let data = self.data.as_ref().map_err(Clone::clone)?.clone();
        let settings = data.join(SETTINGS).join(crate::util::opaque_id("settings-")?);
        if settings.exists() {
            return Err("new settings folder already exists; existing settings are never adopted".into());
        }
        let targets = [settings.join("config.toml"), settings.join("AGENTS.md"), settings.join("skills")];
        let mut effects = self.preview(targets, project, SUPPLIER)?;
        let preview = self.preview.as_mut().ok_or("setup preview unavailable")?;
        preview.kind = PreviewKind::NewSettings { settings: settings.clone() };
        effects["kind"] = json!("new-settings");
        effects["affirmative"] = json!("Create settings and save for next launch");
        effects["settings"] = json!(settings.display().to_string());
        // Plain effects for review; the exact internal locations are listed
        // separately and are also named in the native confirmation statement.
        effects["effects"] = json!([
            "Create a new settings folder for this App, inside its data folder",
            "In it, create an empty config.toml, an empty AGENTS.md and a skills folder; Codex adds its own system skills there, and its own working files to the sign-in folder, when it starts",
            "Create a new sign-in folder for this App, linked to those settings",
            format!("Project when you next open the App: {}", preview.project.as_ref().map(|p| p.display().to_string()).unwrap_or_else(|| "none".into())),
            "Save these choices privately for the next launch",
        ]);
        effects["locations"] = json!([
            {"name":"Settings folder","path":settings.display().to_string()},
            {"name":"Sign-in folder","path":preview.account.display().to_string()},
            {"name":"Saved choices","path":data.join(PROFILE).display().to_string()},
        ]);
        effects["standing"] = json!("Nothing is created until you confirm. No other Codex settings, home or credential is read, imported or changed.");
        effects["defaults"] = Self::first_use_defaults("new-settings");
        Ok(effects)
    }
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
        let account = desktop_account_homes(data)
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
        let effects = json!({"defaults":Self::first_use_defaults("new-home"),"token":token,"kind":"new-home","affirmative":"Prepare home and save for next launch","accountHome":account.display().to_string(),"effects":[format!("Create new account directory {}",account.display()),format!("Create config.toml link → {}",shared.config_toml.display()),format!("Create AGENTS.md link → {}",shared.global_agents_md.display()),format!("Create skills link → {}",shared.skills.display()),format!("Save private pending request {}",data.join(PROFILE).display())],"project":project.as_ref().map(|p|p.display().to_string()),"resources":resource_view(&plan)?,"standing":"No credential import or existing-home adoption. Only the explicit prepare/save action creates these paths. Missing targets remain visible source limits."});
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
        #[cfg(test)]
        crate::records_effect_guard::mutation_for_test("desktop_startup::DesktopSetup::prepare_and_save");
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
        let mut source_refs = preview.source_refs;
        let mut created = None;
        if let PreviewKind::NewSettings { settings } = &preview.kind {
            let made = create_settings(&data, settings, &preview.shared)?;
            // Bind the saved request to the objects actually created: the
            // identities come from the held handles, and the path reading
            // must agree with them (no new baseline from a replacement).
            let objects = made.verify(&data, settings)?;
            let mut refs: [Reference; 3] = [&preview.shared.config_toml, &preview.shared.global_agents_md, &preview.shared.skills]
                .map(|p| Reference::observe(p)).into_iter().collect::<Result<Vec<_>, _>>()?.try_into().unwrap();
            for (reference, object) in refs.iter_mut().zip(objects) {
                if reference.object.as_ref() != Some(&object) {
                    return Err("a new settings file was replaced after it was created; nothing was saved".into());
                }
                reference.object = Some(object);
            }
            source_refs = refs;
            created = Some((made, settings.clone()));
        }
        protected_directory(&desktop_account_homes(&data))?;
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
            shared: source_refs,
            project: preview.project_ref,
        };
        self.validate(&requested)?;
        self.recheck_storage()?;
        // Custody runs through publication: the created objects are re-proved
        // immediately before the request naming them is written.
        if let Some((made, settings)) = &created {
            settings_hook("before-publish");
            let objects = made.verify(&data, settings)?;
            if requested.shared.iter().zip(objects.iter()).any(|(r, o)| r.object.as_ref() != Some(o)) {
                return Err("a new settings file was replaced before saving; nothing was saved".into());
            }
        }
        write_profile(&data.join(PROFILE), &requested)?;
        drop(created);
        self.pending = json!({"state":"saved-for-next-launch","accountHome":preview.account.display().to_string(),"project":preview.project.as_ref().map(|p|p.display().to_string()),"resources":observed.resources.iter().map(|r|json!({"name":r.name,"state":format!("{:?}",r.state),"limit":r.limit})).collect::<Vec<_>>(),"standing":"Pending request only; the current workspace, homes, records, attachments, recovery, choices and prepared messages are unchanged"});
        Ok(self.view())
    }
}
#[cfg(test)]
thread_local! {
    /// Deterministic interleavings for the new-settings regression tests.
    static SETTINGS_HOOK: std::cell::RefCell<Option<Box<dyn FnMut(&str)>>> = std::cell::RefCell::new(None);
}
fn settings_hook(_at: &str) {
    #[cfg(test)]
    SETTINGS_HOOK.with(|hook| if let Some(hook) = hook.borrow_mut().as_mut() { hook(_at) });
}
/// The created settings, held open from creation through publication, with
/// the identities taken from those handles (never from a later path read).
struct CreatedSettings {
    parent: File,
    leaf: File,
    objects: [(PathBuf, File); 3],
}
impl CreatedSettings {
    /// Each path must still name exactly the object created through the held
    /// handles, with no symlink on the way; otherwise nothing is published.
    fn verify(&self, data: &Path, settings: &Path) -> Result<[ObjectRef; 3], String> {
        let same = |path: &Path, held: &File, what: &str| -> Result<ObjectRef, String> {
            storage::check_path(path)?;
            let at = std::fs::symlink_metadata(path).map_err(|e| format!("{what} is no longer present: {e}"))?;
            let own = held.metadata().map_err(|e| format!("{what} handle unavailable: {e}"))?;
            if at.file_type().is_symlink() || ObjectRef::of(&at) != ObjectRef::of(&own) {
                return Err(format!("{what} was replaced after it was created; nothing was saved"));
            }
            Ok(ObjectRef::of(&own))
        };
        same(&data.join(SETTINGS), &self.parent, "the App settings directory")?;
        same(settings, &self.leaf, "the new settings folder")?;
        let refs = self.objects.each_ref().map(|(path, held)| same(path, held, "a new settings file or folder"));
        let [a, b, c] = refs;
        Ok([a?, b?, c?])
    }
}
fn c_name(name: &str) -> Result<std::ffi::CString, String> {
    std::ffi::CString::new(name).map_err(|_| "settings name contains NUL".to_owned())
}
fn open_dir_at(parent: &File, name: &str) -> Result<File, String> {
    use std::os::fd::FromRawFd;
    let fd = unsafe { libc::openat(parent.as_raw_fd(), c_name(name)?.as_ptr(), libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC) };
    if fd < 0 { return Err(format!("{name} could not be opened without following links: {}", std::io::Error::last_os_error())); }
    Ok(unsafe { File::from_raw_fd(fd) })
}
fn private_dir(file: &File, what: &str) -> Result<(), String> {
    let meta = file.metadata().map_err(|e| e.to_string())?;
    if !meta.is_dir() || meta.uid() != unsafe { libc::geteuid() } || meta.mode() & 0o077 != 0 {
        return Err(format!("{what} must be a private directory owned by this user"));
    }
    Ok(())
}
/// Create the new App-owned settings leaf and its three empty targets. Every
/// creation is relative to a held directory handle opened without following
/// links, create-only (an existing entry is never adopted or overwritten),
/// private to this user; a replaced directory or symlink makes it fail rather
/// than write elsewhere. A failure leaves only what was created inside the
/// new leaf.
fn create_settings(data: &Path, settings: &Path, shared: &SharedResourceTargets) -> Result<CreatedSettings, String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("desktop_startup::create_settings");
    use std::os::fd::FromRawFd;
    let leaf = settings.file_name().and_then(|n| n.to_str()).ok_or("new settings leaf name unavailable")?;
    if settings.parent() != Some(data.join(SETTINGS).as_path())
        || shared.config_toml != settings.join("config.toml")
        || shared.global_agents_md != settings.join("AGENTS.md")
        || shared.skills != settings.join("skills")
    {
        return Err("new settings must be the reviewed App-owned leaf".into());
    }
    protected_directory(&data.join(SETTINGS))?;
    settings_hook("after-parent-check");
    let parent = OpenOptions::new().read(true)
        .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC)
        .open(data.join(SETTINGS))
        .map_err(|e| format!("the App settings directory could not be opened without following links: {e}"))?;
    private_dir(&parent, "the App settings directory")?;
    if unsafe { libc::mkdirat(parent.as_raw_fd(), c_name(leaf)?.as_ptr(), 0o700) } != 0 {
        return Err(format!("new settings folder was not created; existing settings are never adopted: {}", std::io::Error::last_os_error()));
    }
    settings_hook("after-leaf-create");
    let leaf_dir = open_dir_at(&parent, leaf)?;
    private_dir(&leaf_dir, "the new settings folder")?;
    let file_at = |name: &str| -> Result<File, String> {
        let fd = unsafe { libc::openat(leaf_dir.as_raw_fd(), c_name(name)?.as_ptr(), libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC, 0o600 as libc::c_uint) };
        if fd < 0 { return Err(format!("new settings file {name} was not created: {}", std::io::Error::last_os_error())); }
        let file = unsafe { File::from_raw_fd(fd) };
        file.sync_all().map_err(|e| format!("new settings file not persisted: {e}"))?;
        Ok(file)
    };
    let config = file_at("config.toml")?;
    let agents = file_at("AGENTS.md")?;
    if unsafe { libc::mkdirat(leaf_dir.as_raw_fd(), c_name("skills")?.as_ptr(), 0o700) } != 0 {
        return Err(format!("new skills folder was not created: {}", std::io::Error::last_os_error()));
    }
    let skills = open_dir_at(&leaf_dir, "skills")?;
    private_dir(&skills, "the new skills folder")?;
    leaf_dir.sync_all().map_err(|e| format!("new settings folder not persisted: {e}"))?;
    parent.sync_all().map_err(|e| format!("App settings directory not persisted: {e}"))?;
    let created = CreatedSettings { parent, leaf: leaf_dir,
        objects: [(shared.config_toml.clone(), config), (shared.global_agents_md.clone(), agents), (shared.skills.clone(), skills)] };
    settings_hook("after-create");
    created.verify(data, settings)?;
    Ok(created)
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
    // The installed npm generator identifies the current development main only.
    // Historical archive attestations do not qualify this new distribution.
    Ok(crate::hosting::ASSESSMENT_SUPPLIER_SHA256.to_owned())
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
                .configured_provider_observation_revision(&peer.g, f.project.to_str().unwrap());
            view["providerOfferReadRevision"] = home
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
                .configured_provider_observation_revision(&generation, f.project.to_str().unwrap());
            view["providerOfferReadRevision"] = home
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
    /// At the confirmed write's final admission, a configuration reading registers and stays
    /// unanswered, so the configuration reading after the write is refused at the reading gate.
    fn reading_outstanding_at_the_write(host: &Arc<crate::hosting::Host>) {
        let held = Arc::clone(host);
        *host.before_request_write.lock().unwrap() = Some(Box::new(move |h| {
            if h.writing_method_for_test().as_deref() != Some("config/batchWrite") { return reading_outstanding_at_the_write(&held); }
            let (registered_tx, registered) = std::sync::mpsc::channel();
            *h.reading_after_register.lock().unwrap() = Some(Box::new(move |_| { let _ = registered_tx.send(()); }));
            let (reader, generation) = (Arc::clone(&held), h.snapshot()["generation"].clone());
            std::thread::spawn(move || reader.request_reading("config/read", json!({"cwd":"/invented/elsewhere","includeLayers":false}), json!({"kind":"synthetic reader"}), &generation, false, std::time::Instant::now() + std::time::Duration::from_secs(5)));
            registered.recv_timeout(std::time::Duration::from_secs(5)).expect("the reading registers while the write holds the writer");
        }));
    }
    /// A configuration reading registers now and stays unanswered (the stand-in answers only the
    /// fixture's own private reads), so the next reading of this home waits at the gate.
    fn reading_outstanding_now(host: &Arc<crate::hosting::Host>) {
        let (registered_tx, registered) = std::sync::mpsc::channel();
        *host.reading_after_register.lock().unwrap() = Some(Box::new(move |_| { let _ = registered_tx.send(()); }));
        let (reader, generation) = (Arc::clone(host), host.snapshot()["generation"].clone());
        std::thread::spawn(move || reader.request_reading("config/read", json!({"cwd":"/invented/elsewhere","includeLayers":false}), json!({"kind":"synthetic reader"}), &generation, false, std::time::Instant::now() + std::time::Duration::from_secs(5)));
        registered.recv_timeout(std::time::Duration::from_secs(5)).expect("the reading registers");
    }
    /// Add's save reads the configuration again before its write. Refused there (the writer busy
    /// past its deadline, or an earlier reading registered after the save's currency check and
    /// still unanswered), the save writes nothing and the command returns that sentence alone.
    #[test]
    fn access_provider_add_save_refused_at_its_reading_before_the_write_returns_the_sentence_and_writes_nothing() {
        use crate::hosting::reading_gate::{READING_GATE, READING_WITHDRAWN};
        for expected in [READING_WITHDRAWN, READING_GATE] {
            let f = Fixture::new();
            let (_desktop, state, _home, peer) = f.continuation();
            peer.create_replies(f.shared[0].clone(), f.shared[0].clone(), "fixture.new", "ok");
            let view = crate::create_offer_result(&state, &peer.g, "fixture.new", "Invented name", "https://example.invalid/new", &crate::endpoint_checkpoint(&state).unwrap()).unwrap();
            let held = Arc::clone(&peer.host);
            if expected == READING_GATE {
                *crate::hosting::provider_create::BEFORE_REREAD.lock().unwrap() = Some(Box::new(move || reading_outstanding_now(&held)));
            } else {
                *crate::hosting::provider_create::BEFORE_REREAD.lock().unwrap() = Some(Box::new(move || held.hold_frame_writer_for_test(std::time::Duration::from_millis(400))));
            }
            let error = crate::create_save_result(
                &state,
                view["token"].as_str().unwrap(),
                || Ok(()),
                |_| Ok(tauri_plugin_dialog::MessageDialogResult::Custom(crate::hosting::provider_create::WRITE_ACTION.into())),
                |candidate, _| Ok(Some(candidate.accept_checked_current_object())),
            ).unwrap_err();
            assert_eq!(error, expected, "the reading before the write was not sent");
            assert_eq!(crate::create_save_refusal(error), expected, "the command passes it on as it is");
            assert!(peer.host.client_requests().iter().all(|r| r["method"] != "config/batchWrite"), "nothing was written");
        }
        assert_eq!(crate::create_save_refusal("INVENTED_PRIVATE_SAVE_DIAGNOSTIC".into()), "Provider Add unavailable; no automatic retry; private diagnostics withheld");
    }
    /// A start or fork refused at its configuration reading returns that sentence alone; any other
    /// refusal keeps its role supply observation. Key entry refused at its reading states the key
    /// home's known setup first, then the sentence; anything else is unchanged.
    #[test]
    fn access_provider_start_fork_and_key_entry_refusals_carry_the_reading_sentences() {
        use crate::hosting::reading_gate::{READING_GATE, READING_WITHDRAWN};
        let publication = json!({"state":"refused"});
        for sentence in [READING_GATE, READING_WITHDRAWN] {
            assert_eq!(crate::role_supply_refusal(sentence, &publication), sentence);
            assert_eq!(crate::key_entry_refusal(sentence.into()), format!("The separate key home is set up; the key field was not opened, so no key was sent or saved. {sentence}"));
        }
        assert_eq!(crate::role_supply_refusal("refused-not-sent: invented", &publication), format!("refused-not-sent: invented; role supply observation: {publication}"));
        assert_eq!(crate::role_supply_refusal(&format!("{READING_GATE} "), &publication), format!("{READING_GATE} ; role supply observation: {publication}"), "only the exact sentence");
        assert_eq!(crate::key_entry_refusal("native key entry refused".into()), "native key entry refused");
        // Exact, not by suffix: a message ending in a sentence after any other prefix is not a
        // reading refusal. The start keeps its role supply observation; the fork's record does not
        // say refused before send.
        use crate::hosting::reading_gate::WRITE_THEN_READING;
        let later = format!("{WRITE_THEN_READING}{READING_GATE}");
        assert_eq!(crate::role_supply_refusal(&later, &publication), format!("{later}; role supply observation: {publication}"));
    }
    /// The fork's role-supply record calls a refusal "before send" for an exact reading refusal
    /// (either sentence alone, or the child-role prefix then either sentence), never for a message
    /// that merely ends in a sentence after another prefix.
    #[test]
    fn access_provider_fork_record_counts_only_an_exact_reading_refusal_as_before_send() {
        use crate::hosting::reading_gate::{CHILD_ROLES_IN_PLACE, READING_GATE, READING_WITHDRAWN, WRITE_THEN_READING};
        assert!(!crate::conversation_roles::fork_refused_before_send(&format!("{WRITE_THEN_READING}{READING_GATE}")), "a sentence after another prefix is not before send");
        assert!(crate::conversation_roles::fork_refused_before_send(READING_WITHDRAWN));
        assert!(crate::conversation_roles::fork_refused_before_send(&format!("{CHILD_ROLES_IN_PLACE}{READING_GATE}")));
        assert!(crate::conversation_roles::fork_refused_before_send("refused-not-sent: invented"));
    }
    /// The endpoint and Add offer commands pass either reading sentence on as it is and keep their
    /// fixed sentence for anything else.
    #[test]
    fn access_provider_offer_commands_pass_the_reading_sentences_on_unchanged() {
        use crate::hosting::reading_gate::{READING_GATE, READING_WITHDRAWN};
        for (label, refusal, fixed) in [
            ("endpoint", crate::endpoint_offer_refusal as fn(String) -> String, "Endpoint edit unavailable; private values and diagnostics withheld"),
            ("Add", crate::create_offer_refusal, "Provider Add unavailable; private values and diagnostics withheld"),
        ] {
            for sentence in [READING_GATE, READING_WITHDRAWN] { assert_eq!(refusal(sentence.into()), sentence, "{label}"); }
            assert_eq!(refusal("INVENTED_PRIVATE_OFFER_DIAGNOSTIC".into()), fixed, "{label}: anything else is withheld");
            assert_eq!(refusal(format!("{READING_GATE} ")), fixed, "{label}: only the exact sentence passes");
        }
    }
    /// A save whose configuration reading after the write is not sent states the write first and
    /// unqualified, then that reading's own sentence; endpoint and Add alike.
    #[test]
    fn access_provider_saves_state_the_write_first_when_reading_again_is_not_sent() {
        use crate::hosting::reading_gate::{READING_GATE, WRITE_THEN_READING};
        let f = Fixture::new();
        let (_desktop, state, _home, mut peer) = f.continuation();
        peer.endpoint_replies(f.shared[0].clone(), f.shared[0].clone(), "fixture.dot", "https://example.invalid/new");
        let offer = crate::hosting::provider_endpoint::offer(&state, "fixture.dot", "https://example.invalid/new").unwrap();
        reading_outstanding_at_the_write(&peer.host);
        let outcome = crate::hosting::provider_endpoint::save(
            &state,
            offer,
            |_| Ok(tauri_plugin_dialog::MessageDialogResult::Custom(crate::hosting::provider_endpoint::WRITE_ACTION.into())),
            |candidate, _| Ok(Some(candidate.accept_checked_current_object())),
        ).unwrap();
        assert_eq!(outcome["message"], format!("{WRITE_THEN_READING}{READING_GATE}"), "endpoint: {outcome}");
        assert_eq!(peer.continuation_frame()["method"], "config/read");
        assert_eq!(peer.continuation_frame()["method"], "config/batchWrite", "the write was made");
        let f = Fixture::new();
        let (_desktop, state, _home, peer) = f.continuation();
        peer.create_replies(f.shared[0].clone(), f.shared[0].clone(), "fixture.new", "ok");
        let view = crate::create_offer_result(&state, &peer.g, "fixture.new", "Invented name", "https://example.invalid/new", &crate::endpoint_checkpoint(&state).unwrap()).unwrap();
        reading_outstanding_at_the_write(&peer.host);
        let outcome = crate::create_save_result(
            &state,
            view["token"].as_str().unwrap(),
            || Ok(()),
            |_| Ok(tauri_plugin_dialog::MessageDialogResult::Custom(crate::hosting::provider_create::WRITE_ACTION.into())),
            |candidate, _| Ok(Some(candidate.accept_checked_current_object())),
        ).unwrap();
        assert_eq!(outcome["message"], format!("{WRITE_THEN_READING}{READING_GATE}"), "Add: {outcome}");
        assert_eq!(outcome["state"], "write-observed-source-unconfirmed");
    }
    /// A confirmed provider write's attempt, made through the real endpoint write, leaves no
    /// configuration reading of the generation current; the offer reading's reply arriving again
    /// after the attempt restores nothing.
    #[test]
    fn access_provider_endpoint_write_attempt_clears_reading_currency_and_a_late_reply_restores_nothing() {
        let f = Fixture::new();
        let (_desktop, state, _home, mut peer) = f.continuation();
        peer.endpoint_replies(f.shared[0].clone(), f.shared[0].clone(), "fixture.dot", "https://example.invalid/new");
        let offered: Arc<Mutex<Option<Value>>> = Arc::default();
        let kept = offered.clone();
        *peer.host.reading_after_register.lock().unwrap() = Some(Box::new(move |h| {
            *kept.lock().unwrap() = h.reading_request_id_for_test().map(|id| serde_json::from_str::<Value>(&id).unwrap());
        }));
        let offer = crate::hosting::provider_endpoint::offer(&state, "fixture.dot", "https://example.invalid/new").unwrap();
        let offer_id = offered.lock().unwrap().clone().expect("the offer's reading registered");
        assert!(peer.host.reading_current_for_test().is_some(), "the offer's reading is the newest");
        let observed: Arc<Mutex<Option<(String, Option<String>, Option<String>)>>> = Arc::default();
        let seen = observed.clone();
        *peer.host.before_request_write.lock().unwrap() = Some(Box::new(move |h| {
            // The first request after the offer is the write itself, past its final admission.
            let method = h.writing_method_for_test().unwrap_or_default();
            let after_attempt = h.reading_current_for_test();
            let generation = h.snapshot()["generation"].clone();
            h.native_frame_for_test(&generation, &json!({"id":offer_id,"result":{"config":{},"origins":{}}}));
            *seen.lock().unwrap() = Some((method, after_attempt, h.reading_current_for_test()));
        }));
        let _ = crate::hosting::provider_endpoint::save(
            &state,
            offer,
            |_| Ok(tauri_plugin_dialog::MessageDialogResult::Custom(crate::hosting::provider_endpoint::WRITE_ACTION.into())),
            |candidate, _| Ok(Some(candidate.accept_checked_current_object())),
        );
        let (method, after_attempt, after_late_reply) = observed.lock().unwrap().clone().expect("the write reached its attempt");
        assert_eq!(method, "config/batchWrite");
        assert_eq!(after_attempt, None, "the attempt cleared the generation's currency");
        assert_eq!(after_late_reply, None, "the offer reading's late reply restored nothing");
        assert_eq!(peer.continuation_frame()["method"], "config/read");
        assert_eq!(peer.continuation_frame()["method"], "config/batchWrite");
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
            Some(crate::hosting::ASSESSMENT_SUPPLIER_SHA256)
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
        // App data that did not resolve is never treated as held: nothing
        // operational starts (the records override included) and the actual
        // error is shown on the environment route's launch state.
        let inputs = setup.admit_root(launch, Err("environment App data unavailable".into()));
        assert!(!inputs.allow_operational, "unresolved App data starts nothing operational");
        assert!(inputs.data.unwrap_err().contains("environment App data unavailable"));
        assert!(inputs.launch.host_config.unwrap_err().contains("environment App data unavailable"));
        assert_eq!(setup.view()["launch"]["state"], "environment");
        assert!(setup.view()["launch"]["reason"].as_str().unwrap().contains("environment App data unavailable"));
    }

    /// The environment route's input contract: a Codex home, the key home or a
    /// shared path supplied through the environment that is relative, empty or
    /// has a `.` or `..` component is refused at admission, by name, before the
    /// probe home is allocated (the probe panics if asked) and before any
    /// configuration is built. The values are carried as received: a refused
    /// value never reads as not supplied.
    #[test]
    fn environment_paths_that_are_relative_empty_or_dotted_are_refused_at_admission() {
        let f = Fixture::new();
        let absolute = f.root.join("environment-home").into_os_string();
        let must = |name: &str| format!("{name} must be an absolute path without . or .. components");
        let empty = |name: &str| format!("{name} is empty: it must be an absolute path without . or .. components");
        let dotted_in = { let mut v = f.root.clone().into_os_string(); v.push("/./environment-home"); v };
        let dotted_up = { let mut v = f.root.clone().into_os_string(); v.push("/x/../environment-home"); v };
        let cases: Vec<(Vec<(&str, std::ffi::OsString)>, String)> = vec![
            (vec![("CHIRALITY_CODEX_HOME", "relative/home".into())], must("CHIRALITY_CODEX_HOME")),
            (vec![("CHIRALITY_CODEX_HOME", "".into())], empty("CHIRALITY_CODEX_HOME")),
            (vec![("CHIRALITY_CODEX_HOME", dotted_in)], must("CHIRALITY_CODEX_HOME")),
            (vec![("CHIRALITY_CODEX_HOME", dotted_up)], must("CHIRALITY_CODEX_HOME")),
            (vec![("CHIRALITY_CODEX_HOME", absolute.clone()), ("CHIRALITY_KEY_HOME", "key-home".into())], must("CHIRALITY_KEY_HOME")),
            (vec![("CHIRALITY_CODEX_HOME", absolute.clone()), ("CHIRALITY_SHARED_SKILLS", "".into())], empty("CHIRALITY_SHARED_SKILLS")),
            (vec![("CHIRALITY_CODEX_HOME", "home".into()), ("CHIRALITY_SHARED_CONFIG", "config.toml".into())], format!("{}; {}", must("CHIRALITY_CODEX_HOME"), must("CHIRALITY_SHARED_CONFIG"))),
        ];
        for (given, expected) in cases {
            let input = |key: &str| -> Option<std::ffi::OsString> {
                if key == "CHIRALITY_CODEX_BIN" { return Some("/invented/bin/codex".into()); }
                given.iter().find(|(name, _)| *name == key).map(|(_, value)| value.clone())
            };
            let env = crate::explicit_environment_launch(&input, &Ok(f.data.clone()), &Ok(f.resources.clone()), true, || panic!("a refused environment allocates no probe home")).unwrap();
            assert_eq!(env.host_config.as_ref().unwrap_err(), &expected, "{given:?}");
            assert_eq!(env.key_path, input("CHIRALITY_KEY_HOME").map(PathBuf::from), "the key home is carried as received");
            assert_eq!(env.shared_paths[2], input("CHIRALITY_SHARED_SKILLS").map(PathBuf::from), "a shared path is carried as received");
            let mut setup = f.setup();
            let launch = setup.resolve(Some(env), true, || panic!("no fallback to a saved request"));
            assert_eq!(launch.host_config.as_ref().unwrap_err(), &expected);
            assert!(setup.lease.is_none() && setup.requested.is_none(), "nothing admitted from a saved request");
            assert_eq!(setup.view()["launch"]["state"], "environment");
            assert_eq!(setup.view()["launch"]["reason"], expected.as_str());
            // No value is echoed in the reason.
            assert!(!expected.contains("relative/home") && !expected.contains("environment-home") && !expected.contains("config.toml"));
        }
    }

    /// The accepted forms on the development route: an absolute home with no
    /// `.` or `..` component is admitted as it was, and absent key or shared
    /// paths stay absent.
    #[test]
    fn an_absolute_environment_home_is_admitted_as_before() {
        let f = Fixture::new();
        let home = f.root.join("environment-home");
        let probe = f.root.join("probe-home");
        let input = |key: &str| -> Option<std::ffi::OsString> {
            match key {
                "CHIRALITY_CODEX_BIN" => Some("/invented/bin/codex".into()),
                "CHIRALITY_CODEX_HOME" => Some(home.clone().into_os_string()),
                _ => None,
            }
        };
        let env = crate::explicit_environment_launch(&input, &Ok(f.data.clone()), &Ok(f.resources.clone()), true, || Ok(probe.clone())).unwrap();
        let cfg = env.host_config.as_ref().unwrap();
        assert_eq!((cfg.codex_home.as_path(), cfg.probe_home.as_path(), cfg.cwd.clone()), (home.as_path(), probe.as_path(), std::env::temp_dir()));
        assert!(env.key_path.is_none() && env.shared_paths.iter().all(Option::is_none));
    }

    /// The same contract on the production branch of the environment route
    /// (a build with distribution-successor that is not a development run).
    #[cfg(feature = "distribution-successor")]
    #[test]
    fn the_release_environment_route_refuses_a_relative_or_empty_home_and_admits_an_absolute_one() {
        let f = Fixture::new();
        for (value, expected) in [
            (std::ffi::OsString::from("records"), "CHIRALITY_CODEX_HOME must be an absolute path without . or .. components"),
            (std::ffi::OsString::from(""), "CHIRALITY_CODEX_HOME is empty: it must be an absolute path without . or .. components"),
        ] {
            let input = |key: &str| (key == "CHIRALITY_CODEX_HOME").then(|| value.clone());
            let env = crate::explicit_environment_launch(&input, &Ok(f.data.clone()), &Ok(f.resources.clone()), false, || panic!("a refused environment allocates no probe home")).unwrap();
            assert_eq!(env.host_config.as_ref().unwrap_err(), expected);
        }
        let home = f.root.join("environment-home");
        let input = |key: &str| (key == "CHIRALITY_CODEX_HOME").then(|| home.clone().into_os_string());
        let env = crate::explicit_environment_launch(&input, &Ok(f.data.clone()), &Ok(f.resources.clone()), false, || Ok(f.root.join("probe-home"))).unwrap();
        let cfg = env.host_config.as_ref().unwrap();
        assert_eq!((cfg.codex_home.as_path(), cfg.cwd.as_path()), (home.as_path(), f.data.as_path()));
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
            // A holder of this App data is shown as held, and so is a holder of
            // a Codex home the saved request names (which process is not known;
            // DEL-01-02 REQ-010): neither is a missing setup, and showing setup
            // as needed would be untrue. Every other refusal is setup.
            assert_eq!(
                desktop.lock().unwrap().view()["launch"]["state"],
                match case { "profile-owner" => "data-held", "home-owner" => "home-held", _ => "setup-required" },
                "{case}"
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
        assert!(blocked.host_config.unwrap_err().contains("held by another process"));
        let alias = f.root.join("data-alias");
        std::os::unix::fs::symlink(&f.data, &alias).unwrap();
        let mut alias_setup = DesktopSetup::new(Ok(alias), Ok(f.resources.clone()));
        assert!(alias_setup
            .resolve(None, true, || panic!("alias owner must not bind"))
            .host_config
            .unwrap_err()
            .contains("held by another process"));
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
            .contains("held by another process"));
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
            .contains("held by another process"));
    }

    /// Every directory and file under `root`, each file with its bytes and
    /// each link with its target: the App data, byte for byte.
    fn tree(root: &Path) -> Vec<(PathBuf, Option<Vec<u8>>)> {
        fn walk(at: &Path, out: &mut Vec<(PathBuf, Option<Vec<u8>>)>) {
            for entry in std::fs::read_dir(at).unwrap() {
                let path = entry.unwrap().path();
                let meta = std::fs::symlink_metadata(&path).unwrap();
                if meta.file_type().is_symlink() {
                    let target = std::fs::read_link(&path).unwrap();
                    out.push((path, Some(target.into_os_string().into_vec())));
                } else if meta.is_dir() {
                    out.push((path.clone(), None));
                    walk(&path, out);
                } else {
                    out.push((path.clone(), Some(std::fs::read(&path).unwrap())));
                }
            }
        }
        let mut out = Vec::new();
        walk(root, &mut out);
        out.sort();
        out
    }
    /// A second App process on `data`, on `route`, through the same startup
    /// as `run` up to where Codex would start ([`second_app_peer`]).
    fn second_app(route: &str, data: &Path, resources: &Path) -> std::process::Output {
        std::process::Command::new(std::env::current_exe().unwrap())
            .args(["--exact", "desktop_startup::tests::second_app_peer", "--nocapture", "--test-threads=1"])
            .env(
                "CHIRALITY_SECOND_APP_FIXTURE",
                json!({"route":route,"data":data,"resources":resources}).to_string(),
            )
            .output()
            .unwrap()
    }
    fn assert_second_app_refused(route: &str, data: &Path, resources: &Path) {
        let out = second_app(route, data, resources);
        let stdout = String::from_utf8_lossy(&out.stdout);
        assert!(
            out.status.success() && stdout.contains("SECOND_APP_REFUSED"),
            "{route}: {stdout}\n{}",
            String::from_utf8_lossy(&out.stderr)
        );
    }

    #[test]
    fn second_app_peer() {
        let Ok(fixture) = std::env::var("CHIRALITY_SECOND_APP_FIXTURE") else {
            return;
        };
        let fixture: Value = serde_json::from_str(&fixture).unwrap();
        let data = PathBuf::from(fixture["data"].as_str().unwrap());
        let resources = PathBuf::from(fixture["resources"].as_str().unwrap());
        let environment = fixture["route"] == "environment";
        let variables = json!({"CHIRALITY_APP_DATA":data,"CHIRALITY_CODEX_BIN":"/invented/bin/codex","CHIRALITY_CODEX_HOME":data.join("invented-environment-home"),"CHIRALITY_ALLOW_UNVERIFIED":"1"});
        let input = |key: &str| {
            environment
                .then(|| variables[key].as_str().map(std::ffi::OsString::from))
                .flatten()
        };
        // The environment route names its App data; the platform's is not used.
        let platform = if environment { PathBuf::from("/invented/platform-app-data") } else { data.clone() };
        let (desktop, inputs) = crate::admitted_startup(input, Ok(platform), Ok(resources), true, || {
            panic!("a second App allocates no probe home")
        });
        assert!(!inputs.allow_operational);
        assert!(inputs.data.is_err());
        assert_eq!(inputs.launch.host_config.as_ref().unwrap_err(), DATA_HELD);
        assert!(inputs.launch.workspace.is_none());
        let view = desktop.view();
        assert_eq!(view["launch"]["state"], "data-held");
        assert_eq!(view["launch"]["reason"], DATA_HELD);
        // The rest of startup as `run` performs it: nothing operational starts.
        let RootInputs { launch, data, allow_operational } = inputs;
        let (key, shared) = (launch.key_path.clone(), launch.shared_paths.clone());
        let (state, home) = crate::freeze_startup_state(launch, Arc::new(Mutex::new(desktop)), Value::Null);
        crate::initialize_startup_consumers(&state, &home, data, allow_operational, true, None, key, shared);
        assert!(home.host_config.is_err(), "no Codex start is reachable");
        assert_eq!(home.host.snapshot()["state"], "absent");
        assert_eq!(home.recovery_startup.lock().unwrap().snapshot()["state"], "initialization-failed");
        assert!(state.workspace.is_none());
        println!("SECOND_APP_REFUSED");
    }

    /// DEL-01-02: one App at a time holds an App data directory. With a first
    /// App holding it (saved route, its recovery ledger started), a second App
    /// process on the saved route and one on the environment route each start
    /// nothing operational and leave the ledger and the App data unchanged.
    #[test]
    fn a_second_app_on_held_app_data_starts_nothing_and_changes_nothing_on_either_route() {
        let f = Fixture::new();
        let mut setup = f.setup();
        f.prepare(&mut setup, true);
        drop(setup);
        let (first, inputs) = crate::admitted_startup(|_| None, Ok(f.data.clone()), Ok(f.resources.clone()), true, || f.probe());
        assert!(inputs.allow_operational);
        std::fs::create_dir_all(f.data.join("runtime")).unwrap();
        let ledger_path = f.data.join("runtime/recovery.ledger.jsonl");
        let host = Arc::new(Host::new());
        host.configure_recovery(ledger_path.clone()).unwrap();
        let ledger = || crate::recovery::stored_entries(&ledger_path);
        let (entries, files) = (ledger(), tree(&f.data));
        assert_eq!(entries.len(), 1, "the first App's session start");
        for route in ["saved", "environment"] {
            assert_second_app_refused(route, &f.data, &f.resources);
            assert_eq!(ledger(), entries, "{route}: ledger entries unchanged");
            assert_eq!(tree(&f.data), files, "{route}: App data unchanged byte for byte");
        }
        drop(host);
        drop(first);
        // Once the first App has gone, the next one on the same data is admitted.
        let (_next, inputs) = crate::admitted_startup(|_| None, Ok(f.data.clone()), Ok(f.resources.clone()), true, || f.probe());
        assert!(inputs.allow_operational);
    }

    /// The same with the first App on the environment route, which names its
    /// App data (`CHIRALITY_APP_DATA`); a second App on either route is refused,
    /// and a run naming a different App data is not.
    #[test]
    fn an_environment_route_app_holds_its_named_app_data_against_both_routes() {
        let f = Fixture::new();
        let named = |data: PathBuf| move |key: &str| (key == crate::APP_DATA_ENV).then(|| data.clone().into_os_string());
        let (first, inputs) = crate::admitted_startup(named(f.data.clone()), Ok(PathBuf::from("/invented/platform-app-data")), Ok(f.resources.clone()), true, || panic!("incomplete environment allocates no probe"));
        assert!(inputs.allow_operational, "the environment route keeps its own errors");
        assert_eq!(first.view()["launch"]["state"], "environment");
        let files = tree(&f.data);
        for route in ["saved", "environment"] {
            assert_second_app_refused(route, &f.data, &f.resources);
            assert_eq!(tree(&f.data), files, "{route}: App data unchanged byte for byte");
        }
        let other = f.root.join("other-app-data");
        let (_other, inputs) = crate::admitted_startup(named(other.clone()), Ok(f.data.clone()), Ok(f.resources.clone()), true, || panic!("incomplete environment allocates no probe"));
        assert!(inputs.allow_operational, "parallel runs that name their own App data are not refused");
        assert!(other.is_dir());
        drop(first);
        let (_again, inputs) = crate::admitted_startup(named(f.data.clone()), Ok(PathBuf::from("/invented/platform-app-data")), Ok(f.resources.clone()), true, || panic!("incomplete environment allocates no probe"));
        assert!(inputs.allow_operational);
    }

    /// `CHIRALITY_APP_DATA` is a development input. A built App does not read
    /// it: it stays on its own App data and its own launch route, and nothing
    /// is created at the named path.
    #[test]
    fn a_built_app_does_not_read_the_app_data_input() {
        let f = Fixture::new();
        let elsewhere = f.root.join("named-by-the-environment");
        let named = |data: PathBuf| move |key: &str| (key == crate::APP_DATA_ENV).then(|| data.clone().into_os_string());
        let (built, inputs) = crate::admitted_startup(named(elsewhere.clone()), Ok(f.data.clone()), Ok(f.resources.clone()), false, || f.probe());
        // With no saved setup the built App is at its own first-use setup, on its own App data.
        assert_eq!(built.view()["launch"]["state"], "setup-required", "the input alone does not select the environment route in a built App");
        assert!(!inputs.allow_operational);
        assert!(inputs.data.as_ref().is_err_and(|e| !e.contains("named-by-the-environment")), "{:?}", inputs.data);
        assert!(!elsewhere.exists(), "nothing is created at the named path");
        // The same input in a development run names the data and selects the route.
        drop(built);
        let (dev, inputs) = crate::admitted_startup(named(elsewhere.clone()), Ok(f.data.clone()), Ok(f.resources.clone()), true, || panic!("incomplete environment allocates no probe"));
        assert_eq!(inputs.data.as_deref(), Ok(elsewhere.as_path()));
        assert_eq!(dev.view()["launch"]["state"], "environment");
    }

    /// Finding 4 (the reviewer's reproduction, as a maintained test): on the
    /// environment route, App data that does not resolve (an invalid
    /// `CHIRALITY_APP_DATA`, an unavailable platform path) allocates no probe
    /// home and builds no operational input; the actual error is shown.
    #[test]
    fn unresolved_app_data_on_the_environment_route_starts_nothing_operational() {
        let f = Fixture::new();
        let cases: [(Option<&str>, Result<PathBuf, String>, &str); 2] = [
            (Some("relative/app-data"), Ok(f.data.clone()), "must be an absolute path"),
            (None, Err("platform App data unavailable (invented)".into()), "platform App data unavailable (invented)"),
        ];
        for (named, platform, expected) in cases {
            let home = f.root.join("environment-home").into_os_string();
            let input = |key: &str| -> Option<std::ffi::OsString> {
                match key {
                    "CHIRALITY_APP_DATA" => named.map(Into::into),
                    "CHIRALITY_CODEX_BIN" => Some("/invented/bin/codex".into()),
                    "CHIRALITY_CODEX_HOME" => Some(home.clone()),
                    "CHIRALITY_ALLOW_UNVERIFIED" => Some("1".into()),
                    _ => None,
                }
            };
            let (desktop, inputs) = crate::admitted_startup(input, platform, Ok(f.resources.clone()), true, || {
                panic!("no probe home is allocated without held App data")
            });
            assert!(!inputs.allow_operational, "{expected}");
            assert!(inputs.data.as_ref().is_err_and(|e| e.contains(expected)), "{:?}", inputs.data);
            assert!(inputs.launch.host_config.as_ref().is_err_and(|e| e.contains(expected)), "no Codex configuration");
            assert!(inputs.launch.workspace.is_none() && inputs.launch.namespaces.is_none());
            let view = desktop.view();
            assert_eq!(view["launch"]["state"], "environment");
            assert!(view["launch"]["reason"].as_str().unwrap().contains(expected), "{view}");
            assert!(desktop.recheck_active().is_err(), "no later start is admitted either");
        }
        assert!(!f.root.join("relative").exists());
    }

    /// A CHIRALITY_APP_DATA that is set and empty, or that has a `.` or `..`
    /// component, is refused by name. In particular an empty value no longer
    /// selects the environment route and then holds the platform App data
    /// folder: the platform folder is never created or held, no probe home is
    /// allocated, nothing operational starts. A clean absolute value is held
    /// as before.
    #[test]
    fn an_empty_or_dotted_app_data_is_refused_and_the_platform_folder_is_not_held() {
        let f = Fixture::new();
        let platform = f.root.join("platform-app-data-never-held");
        let dotted_in = { let mut v = f.root.clone().into_os_string(); v.push("/./dotted-app-data"); v };
        let dotted_up = { let mut v = f.root.clone().into_os_string(); v.push("/x/../dotted-app-data"); v };
        for (value, expected) in [
            (std::ffi::OsString::new(), "CHIRALITY_APP_DATA is empty: it must be an absolute path without . or .. components"),
            (dotted_in, "CHIRALITY_APP_DATA must be an absolute path without . or .. components"),
            (dotted_up, "CHIRALITY_APP_DATA must be an absolute path without . or .. components"),
        ] {
            let input = |key: &str| (key == crate::APP_DATA_ENV).then(|| value.clone());
            let (desktop, inputs) = crate::admitted_startup(input, Ok(platform.clone()), Ok(f.resources.clone()), true, || {
                panic!("no probe home is allocated without held App data")
            });
            assert!(!inputs.allow_operational, "{expected}");
            assert!(inputs.data.as_ref().is_err_and(|e| e.contains(expected)), "{:?}", inputs.data);
            assert!(desktop.view()["launch"]["reason"].as_str().unwrap().contains(expected), "{}", desktop.view());
            assert!(!platform.exists(), "the platform App data folder is neither created nor held");
            assert!(!f.root.join("dotted-app-data").exists() && !f.root.join("x").exists(), "no folder is made for the dotted value");
        }
        // A clean absolute value is held, as before.
        let held = f.root.join("named-app-data");
        let input = |key: &str| (key == crate::APP_DATA_ENV).then(|| held.clone().into_os_string());
        let (_desktop, inputs) = crate::admitted_startup(input, Ok(platform.clone()), Ok(f.resources.clone()), true, || panic!("incomplete environment allocates no probe home"));
        assert_eq!(inputs.data.as_ref().ok(), Some(&held));
        assert!(!platform.exists());
    }

    /// Finding 6: the environment route's App data custody is rechecked by
    /// identity before each start, with no saved request.
    #[test]
    fn the_environment_routes_app_data_is_rechecked_before_each_start() {
        let f = Fixture::new();
        let named = |data: PathBuf| move |key: &str| (key == crate::APP_DATA_ENV).then(|| data.clone().into_os_string());
        let (desktop, inputs) = crate::admitted_startup(named(f.data.clone()), Ok(PathBuf::from("/invented/platform-app-data")), Ok(f.resources.clone()), true, || panic!("incomplete environment allocates no probe"));
        assert!(inputs.allow_operational);
        desktop.recheck_active().unwrap();
        std::fs::rename(&f.data, f.root.join("moved-app-data")).unwrap();
        protected_directory(&f.data).unwrap();
        let refused = desktop.recheck_active().unwrap_err();
        assert!(refused.contains("App data custody lost"), "{refused}");
    }


    /// A stand-in for Codex in `root`: answers the label probe and the
    /// handshake, and appends one line to `root/server-starts` each time an
    /// app-server is started. No real Codex is run.
    fn stand_in(root: &Path) -> PathBuf {
        let path = root.join("stand-in.py");
        std::fs::write(&path, "#!/usr/bin/python3\nimport sys,json,os\nif '--version' in sys.argv:\n print('codex-cli 0.167.0');sys.exit(0)\nopen(os.path.join(os.path.dirname(os.path.abspath(__file__)),'server-starts'),'a').write(os.environ.get('CODEX_HOME','')+'\\n')\nfor line in sys.stdin:\n f=json.loads(line)\n if f.get('method')=='initialize': print(json.dumps({'id':f['id'],'result':{'userAgent':'stand-in'}}),flush=True)\n").unwrap();
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o700)).unwrap();
        path
    }
    fn server_starts(root: &Path) -> usize {
        std::fs::read_to_string(root.join("server-starts")).map_or(0, |text| text.lines().count())
    }
    /// The environment route's inputs: its own App data, a Codex home and the
    /// stand-in, given to the startup as `run` reads its inputs (never set in
    /// this process's environment).
    fn environment_input(data: &Path, home: Option<&Path>, bin: Option<&Path>) -> impl Fn(&str) -> Option<std::ffi::OsString> {
        let (data, home, bin) = (data.to_owned(), home.map(Path::to_owned), bin.map(Path::to_owned));
        move |key: &str| match key {
            crate::APP_DATA_ENV => Some(data.clone().into_os_string()),
            "CHIRALITY_CODEX_HOME" => home.clone().map(PathBuf::into_os_string),
            "CHIRALITY_CODEX_BIN" => bin.clone().map(PathBuf::into_os_string),
            "CHIRALITY_ALLOW_UNVERIFIED" => bin.as_ref().map(|_| "1".into()),
            _ => None,
        }
    }
    /// The whole launch as `run` performs it, up to and including the
    /// automatic start of Codex when there is a configuration to start.
    fn complete_startup(
        input: impl Fn(&str) -> Option<std::ffi::OsString>,
        platform: PathBuf,
        resources: PathBuf,
        probe_root: &Path,
    ) -> (crate::AppState, Arc<runtime_session::HomeSession>, Arc<Mutex<DesktopSetup>>, Option<Result<Value, String>>) {
        let (desktop, RootInputs { launch, data, allow_operational }) =
            crate::admitted_startup(input, Ok(platform), Ok(resources), true, || runtime_session::allocate_fresh_probe(probe_root));
        let (key, shared) = (launch.key_path.clone(), launch.shared_paths.clone());
        let host_config = launch.host_config.clone();
        let desktop = Arc::new(Mutex::new(desktop));
        let (state, home) = crate::freeze_startup_state(launch, desktop.clone(), Value::Null);
        crate::initialize_startup_consumers(&state, &home, data.clone(), allow_operational, true, None, key, shared);
        let started = host_config.ok().map(|cfg| {
            crate::automatic_start(&home.host, &home.recovery_startup, data.as_deref().map_err(String::as_str), &cfg, &desktop)
        });
        (state, home, desktop, started)
    }

    /// The child half of the two-process route tests: one App through its
    /// complete launch on the route its fixture names, alive until its stdin
    /// closes. It prints `READY <state>` with what its start reached.
    #[test]
    fn route_app_peer() {
        let Ok(fixture) = std::env::var("CHIRALITY_ROUTE_APP_FIXTURE") else {
            return;
        };
        let fixture: Value = serde_json::from_str(&fixture).unwrap();
        let path = |key: &str| fixture[key].as_str().map(PathBuf::from);
        let (data, root, resources) = (path("data").unwrap(), path("root").unwrap(), path("resources").unwrap());
        let (state, home, desktop, started) = if fixture["route"] == "environment" {
            complete_startup(environment_input(&data, path("home").as_deref(), path("bin").as_deref()), PathBuf::from("/invented/platform-app-data"), resources, &root)
        } else {
            complete_startup(|_| None, data.clone(), resources, &root)
        };
        if fixture["ledger"] == true {
            // The ledger part of the automatic start, where no Codex is started here.
            runtime_session::start_with_recovery(&home.host, &home.recovery_startup, Ok(&data), None, || Ok(())).unwrap();
            let recovery = home.recovery_startup.lock().unwrap().snapshot();
            assert_eq!(recovery["state"], "configured", "{recovery}");
        }
        if fixture["request"] == true {
            // The stand-in asks for an approval after the handshake: wait until this App's ledger lists it.
            let ledger = runtime_session::reviewed_ledger_path(&data);
            let end = std::time::Instant::now() + std::time::Duration::from_secs(10);
            while !crate::recovery::stored_entries(&ledger).iter().any(|e| e["transition"] == "RQ-01") {
                assert!(std::time::Instant::now() < end, "the request was listed: {:?}", crate::recovery::stored_entries(&ledger));
                std::thread::sleep(std::time::Duration::from_millis(20));
            }
        }
        let session = home.host.shared_recovery_observation()["appSession"].as_str().unwrap_or("").to_owned();
        let reached = started.map_or_else(|| "no-start".to_owned(), |r| r.map_or_else(|e| format!("refused {e}"), |v| v["state"].as_str().unwrap_or("").to_owned()));
        println!("READY {} SESSION {session}", reached.replace('\n', " "));
        std::io::Write::flush(&mut std::io::stdout()).unwrap();
        let mut line = String::new();
        let _ = std::io::stdin().read_line(&mut line);
        let _ = home.host.stop("fixture", "peer ended");
        drop((state, home, desktop));
    }
    fn route_peer(fixture: Value) -> (std::process::Child, String) {
        use std::io::BufRead;
        let mut child = std::process::Command::new(std::env::current_exe().unwrap())
            .args(["--exact", "desktop_startup::tests::route_app_peer", "--nocapture", "--test-threads=1"])
            .env("CHIRALITY_ROUTE_APP_FIXTURE", fixture.to_string())
            .stdin(std::process::Stdio::piped())
            .stdout(std::process::Stdio::piped())
            .spawn()
            .unwrap();
        let mut lines = std::io::BufReader::new(child.stdout.take().unwrap()).lines();
        let seen = loop {
            let line = lines.next().expect("the peer reported").unwrap();
            // libtest prints "test <name> ... " before the body, without a newline.
            if let Some((_, seen)) = line.split_once("READY ") {
                break seen.trim().to_owned();
            }
        };
        std::thread::spawn(move || lines.for_each(drop));
        (child, seen)
    }
    fn end_peer(mut child: std::process::Child) {
        drop(child.stdin.take());
        child.wait().unwrap();
    }

    /// Finding 6: saved startup against a Codex home an environment-route App
    /// holds, the two Apps on separate App data (so App data contention cannot
    /// mask the home check). The environment-route peer has Codex (a stand-in)
    /// ready on the home; this App's complete saved launch, whose account home
    /// is that home, is refused with the home sentence, starts nothing
    /// operational and starts no second Codex on the home.
    #[test]
    fn saved_startup_is_refused_a_home_an_environment_route_app_holds() {
        let f = Fixture::new();
        let mut setup = f.setup();
        let saved = f.prepare(&mut setup, true);
        drop(setup);
        let home = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
        assert!(home.is_dir());
        let bin = stand_in(&f.root);
        let other = f.root.join("environment-app-data");
        let (peer, seen) = route_peer(json!({"route":"environment","data":other,"root":f.root,"resources":f.resources,"home":home,"bin":bin}));
        assert!(seen.starts_with("ready"), "the environment-route App has Codex ready on the home: {seen}");
        assert_eq!(server_starts(&f.root), 1);
        let (state, app_home, desktop, started) = complete_startup(|_| None, f.data.clone(), f.resources.clone(), &f.root);
        let view = desktop.lock().unwrap().view();
        let reason = view["launch"]["reason"].as_str().unwrap_or_default().to_owned();
        assert!(reason.contains(crate::home_hold::IN_USE), "refused with the home sentence: {view}");
        assert_eq!(view["launch"]["state"], "home-held", "a held home is not shown as setup being needed: {view}");
        assert!(started.is_none(), "no Codex configuration is admitted, so no automatic start");
        assert!(app_home.host_config.is_err());
        assert_eq!(app_home.host.snapshot()["state"], "absent");
        assert!(state.workspace.is_none(), "nothing operational");
        assert_eq!(server_starts(&f.root), 1, "no second Codex on the home");
        drop((state, app_home, desktop));
        end_peer(peer);
    }

    /// Finding 6, the reverse: environment startup against a Codex home a
    /// saved-route App holds (its account home, held from its launch), on
    /// separate App data. This App's complete environment launch is admitted
    /// on its own App data; its automatic start of Codex on the held home is
    /// refused with the home sentence, kept for the window, and starts nothing.
    #[test]
    fn environment_startup_is_refused_a_home_a_saved_route_app_holds() {
        let f = Fixture::new();
        let mut setup = f.setup();
        let saved = f.prepare(&mut setup, true);
        drop(setup);
        let home = PathBuf::from(saved["pending"]["accountHome"].as_str().unwrap());
        let (peer, seen) = route_peer(json!({"route":"saved","data":f.data,"root":f.root,"resources":f.resources}));
        assert!(!seen.is_empty(), "{seen}");
        let bin = stand_in(&f.root);
        let other = f.root.join("environment-app-data");
        let (state, app_home, desktop, started) = complete_startup(environment_input(&other, Some(&home), Some(&bin)), PathBuf::from("/invented/platform-app-data"), f.resources.clone(), &f.root);
        assert_eq!(desktop.lock().unwrap().view()["launch"]["state"], "environment", "its own App data is admitted");
        let refused = started.expect("the automatic start is reached").unwrap_err();
        assert_eq!(refused, crate::home_hold::IN_USE);
        let status = app_home.host.snapshot();
        assert_eq!(status["state"], "absent", "nothing spawned or recorded in the lifecycle");
        assert_eq!(status["lastStartRefusal"]["reason"], crate::home_hold::IN_USE, "kept for the window");
        assert_eq!(status["lastStartRefusal"]["home"], crate::hosting::home_identity(&home));
        assert_eq!(server_starts(&f.root), 0, "no Codex on the held home");
        drop((state, app_home, desktop));
        end_peer(peer);
    }

    /// Decision A: a person whose last App session crashed is read as before,
    /// on each route. A first App goes through the real launch on the route
    /// (App data held before the ledger opens) and starts its session on the
    /// ledger; it is killed (SIGKILL). The next App's real launch on the same
    /// route and data is admitted and reads that session as ended without a
    /// record; nothing strands it.
    #[test]
    fn a_crashed_app_session_is_read_as_ended_by_the_next_launch_on_each_route() {
        for route in ["saved", "environment"] {
            let f = Fixture::new();
            if route == "saved" {
                let mut setup = f.setup();
                f.prepare(&mut setup, true);
            }
            // The environment route needs a Codex configuration to configure
            // its ledger at launch: a stand-in on a home of its own.
            let (home, bin) = (f.root.join("environment-home"), stand_in(&f.root));
            std::fs::create_dir(&home).unwrap();
            let (mut peer, seen) = route_peer(json!({"route":route,"data":f.data,"root":f.root,"resources":f.resources,"ledger":true,"home":home,"bin":bin}));
            let crashed = seen.split_once("SESSION ").unwrap_or_else(|| panic!("{route}: {seen}")).1.trim().to_owned();
            assert!(crashed.starts_with("app-session:"), "{route}: {seen}");
            assert_eq!(unsafe { libc::kill(peer.id() as i32, libc::SIGKILL) }, 0);
            peer.wait().unwrap();
            let environment = environment_input(&f.data, Some(&home), Some(&bin));
            let input = |key: &str| if route == "environment" { environment(key) } else { None };
            let platform = if route == "environment" { PathBuf::from("/invented/platform-app-data") } else { f.data.clone() };
            let (state, app_home, desktop, _) = complete_startup(input, platform, f.resources.clone(), &f.root);
            runtime_session::start_with_recovery(&app_home.host, &app_home.recovery_startup, Ok(&f.data), None, || Ok(())).unwrap();
            assert_eq!(app_home.recovery_startup.lock().unwrap().snapshot()["state"], "configured", "{route}: {}", app_home.recovery_startup.lock().unwrap().snapshot());
            let entries = crate::recovery::stored_entries(&runtime_session::reviewed_ledger_path(&f.data));
            let start = entries.iter().rev().find(|e| e["kind"] == "session_started").unwrap();
            assert_eq!(start["previousSession"], crashed.as_str(), "{route}");
            assert_eq!(start["previousSessionEnd"], "ended-without-record", "{route}");
            let _ = app_home.host.stop("fixture", "test ended");
            drop((state, app_home, desktop));
        }
    }


    /// A stand-in for Codex that outlives the App that started it, as the
    /// supplier's app-server can for a time after its input closes: it asks
    /// for one approval after the handshake, and when its input closes it
    /// stays alive until `root/release` exists. It records its process number
    /// in `root/stand-in-pid`. No real Codex is run.
    fn surviving_stand_in(root: &Path) -> PathBuf {
        let path = root.join("surviving-stand-in.py");
        std::fs::write(&path, "#!/usr/bin/python3\nimport sys,json,os,time\nif '--version' in sys.argv:\n print('codex-cli 0.167.0');sys.exit(0)\nroot=os.path.dirname(os.path.abspath(__file__))\nopen(os.path.join(root,'server-starts'),'a').write(os.environ.get('CODEX_HOME','')+'\\n')\nopen(os.path.join(root,'stand-in-pid'),'w').write(str(os.getpid()))\nfor line in sys.stdin:\n f=json.loads(line)\n if f.get('method')=='initialize':\n  print(json.dumps({'id':f['id'],'result':{'userAgent':'stand-in'}}),flush=True)\n  print(json.dumps({'id':'approval-1','method':'item/fileChange/requestApproval','params':{'threadId':'thread','itemId':'item'}}),flush=True)\nwhile not os.path.exists(os.path.join(root,'release')): time.sleep(0.02)\n").unwrap();
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o700)).unwrap();
        path
    }

    /// AC-010, the crash a third review reproduced: an App is killed
    /// (SIGKILL) while the Codex it started is alive and a request is listed.
    /// The next App's complete launch on the same App data and home is
    /// admitted (the earlier App is gone and its session is read as ended);
    /// its ledger records the request as open at that session's end, never as
    /// ended by a process exit, and its custody view shows neither a process
    /// exit nor "unanswered" for it; and its automatic start of Codex on the
    /// home is refused while the first stand-in lives, by the lock that
    /// stand-in holds, so no second stand-in is started. Each is compared
    /// with what is observed from outside: the stand-in's process, an
    /// independent attempt on the lock, and the count of stand-ins started.
    /// Once the first stand-in has ended, the same App starts Codex.
    #[test]
    fn after_an_app_is_killed_its_living_codex_gets_no_process_exit_ending_and_no_successor_on_its_home() {
        use crate::native_local_provider::{take_process_lock, EARLIER_PROCESS, PROCESS_LOCK};
        let alive = |pid: i32| (unsafe { libc::kill(pid, 0) }) == 0;
        let until = |what: &str, done: &dyn Fn() -> bool| {
            let end = std::time::Instant::now() + std::time::Duration::from_secs(10);
            while !done() { assert!(std::time::Instant::now() < end, "{what}"); std::thread::sleep(std::time::Duration::from_millis(20)); }
        };
        let f = Fixture::new();
        let (home, bin) = (f.root.join("environment-home"), surviving_stand_in(&f.root));
        std::fs::create_dir(&home).unwrap();
        let (mut peer, seen) = route_peer(json!({"route":"environment","data":f.data,"root":f.root,"resources":f.resources,"home":home,"bin":bin,"request":true}));
        assert!(seen.starts_with("ready"), "the first App has Codex ready on the home: {seen}");
        let crashed = seen.split_once("SESSION ").unwrap().1.trim().to_owned();
        let first: i32 = std::fs::read_to_string(f.root.join("stand-in-pid")).unwrap().parse().unwrap();
        struct End<'a>(&'a Path, i32);
        impl Drop for End<'_> { fn drop(&mut self) { let _ = std::fs::write(self.0.join("release"), "x"); unsafe { libc::kill(self.1, libc::SIGKILL); } } }
        let _end = End(&f.root, first);
        assert_eq!(unsafe { libc::kill(peer.id() as i32, libc::SIGKILL) }, 0);
        peer.wait().unwrap();
        // Observed from outside: the stand-in outlived its App and holds the home's lock.
        assert!(alive(first), "the stand-in Codex is alive after its App was killed");
        assert_eq!(take_process_lock(&home.join(PROCESS_LOCK)).unwrap_err(), EARLIER_PROCESS, "an independent attempt finds the lock held");
        assert_eq!(server_starts(&f.root), 1);
        let ledger = runtime_session::reviewed_ledger_path(&f.data);
        let before = crate::recovery::stored_entries(&ledger);
        assert!(before.iter().any(|e| e["transition"] == "RQ-01") && !before.iter().any(|e| ["RQ-04", "RQ-06"].contains(&e["transition"].as_str().unwrap_or(""))), "listed and not ended when the App was killed: {before:?}");

        let (state, app_home, desktop, started) = complete_startup(environment_input(&f.data, Some(&home), Some(&bin)), PathBuf::from("/invented/platform-app-data"), f.resources.clone(), &f.root);
        assert_eq!(desktop.lock().unwrap().view()["launch"]["state"], "environment", "the App data of a killed App is admitted");
        let refused = started.expect("the automatic start is reached").unwrap_err();
        assert_eq!(refused, crate::home_hold::PROCESS_HELD);
        let status = app_home.host.snapshot();
        assert_eq!(status["state"], "absent", "nothing spawned or recorded in the lifecycle");
        assert_eq!(status["lastStartRefusal"]["reason"], crate::home_hold::PROCESS_HELD, "kept for the window");
        assert_eq!(status["lastStartRefusal"]["home"], crate::hosting::home_identity(&home));
        assert!(alive(first) && server_starts(&f.root) == 1, "no second stand-in while the first lives");

        // The ledger, against what was observed: the earlier session is read as ended without a
        // record; the request it left listed is recorded open at that session's end; nothing
        // says the living stand-in exited.
        let after = crate::recovery::stored_entries(&ledger);
        let start = after.iter().rev().find(|e| e["kind"] == "session_started").unwrap();
        assert_eq!((start["previousSession"].as_str(), start["previousSessionEnd"].as_str()), (Some(crashed.as_str()), Some("ended-without-record")));
        let endings: Vec<_> = after.iter().filter(|e| e["transition"] == "RQ-06").collect();
        assert_eq!(endings.len(), 1, "{after:?}");
        assert_eq!((endings[0]["endedAs"].as_str(), endings[0]["context"].as_str()), (Some("open-at-app-session-end"), Some("app-ended-without-record")));
        let written = serde_json::to_string(&after[before.len()..]).unwrap();
        assert!(!written.contains("process-exit") && !written.contains("RQ-04") && !written.contains("unanswered"), "no process exit and no missing reply is recorded for a Codex seen alive: {written}");
        let custody = app_home.host.recovery_custody().snapshot();
        let events = custody["requestEndEvents"].as_array().unwrap();
        assert_eq!(events.len(), 1, "{custody}");
        assert_eq!((events[0]["kind"].as_str(), events[0]["standing"].as_str()), (Some("request_open_at_app_session_end"), Some("App-recorded")));
        let shown = serde_json::to_string(&json!([custody["requestEndEvents"], custody["restartEvents"]])).unwrap();
        assert!(!shown.contains("unanswered") && !shown.contains("process-exit") && !shown.contains("process_exit"), "the custody view shows no process exit and no \"unanswered\": {shown}");

        // The first stand-in ends; the same App's start is then admitted and starts the second.
        std::fs::write(f.root.join("release"), "x").unwrap();
        until("the first stand-in has ended", &|| !alive(first));
        drop(take_process_lock(&home.join(PROCESS_LOCK)).expect("free once the earlier Codex has ended"));
        let cfg = app_home.host_config.clone().unwrap();
        let ready = crate::automatic_start(&app_home.host, &app_home.recovery_startup, Ok(&f.data), &cfg, &desktop).unwrap();
        assert_eq!(ready["state"], "ready");
        assert_eq!(server_starts(&f.root), 2);
        assert!(app_home.host.snapshot()["lastStartRefusal"].is_null());
        let second: i32 = std::fs::read_to_string(f.root.join("stand-in-pid")).unwrap().parse().unwrap();
        let _ = app_home.host.stop("fixture", "test ended");
        until("the second stand-in has ended", &|| !alive(second));
        drop((state, app_home, desktop));
    }

    /// A stand-in for Codex that ends when its input closes but leaves a program holding the
    /// home's process lock: at its start it runs /bin/sleep in a new session with only the lock's
    /// descriptor passed to it, as a notifier or a hook left running might hold it. It records
    /// its own process number in `root/stand-in-pid` and the sleeper's in `root/holder-pid`.
    fn stand_in_leaving_a_holder(root: &Path) -> PathBuf {
        let path = root.join("stand-in-leaving-a-holder.py");
        std::fs::write(&path, "#!/usr/bin/python3\nimport sys,json,os,subprocess\nif '--version' in sys.argv:\n print('codex-cli 0.167.0');sys.exit(0)\nroot=os.path.dirname(os.path.abspath(__file__))\nopen(os.path.join(root,'server-starts'),'a').write(os.environ.get('CODEX_HOME','')+'\\n')\nlock=os.stat(os.path.join(os.environ['CODEX_HOME'],'chirality-codex-process.lock')).st_ino\nfd=[int(n) for n in os.listdir('/dev/fd') if int(n)>2 and os.path.exists('/dev/fd/'+n) and os.fstat(int(n)).st_ino==lock][0]\np=subprocess.Popen(['/bin/sleep','60'],close_fds=True,pass_fds=(fd,),start_new_session=True,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\nopen(os.path.join(root,'holder-pid'),'w').write(str(p.pid))\nopen(os.path.join(root,'stand-in-pid'),'w').write(str(os.getpid()))\nfor line in sys.stdin:\n f=json.loads(line)\n if f.get('method')=='initialize': print(json.dumps({'id':f['id'],'result':{'userAgent':'stand-in'}}),flush=True)\n").unwrap();
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o700)).unwrap();
        path
    }

    /// VER-010: an App is killed and its Codex ends, but a program that Codex started still
    /// holds the home's process lock. The next App's complete launch is admitted on the App
    /// data and its start of Codex on the home is refused by the lock, with the Codex stand-in
    /// itself observed gone, and no second stand-in is started. Once the holder has ended the
    /// same App starts Codex.
    #[test]
    fn after_an_app_is_killed_a_program_its_codex_left_holding_the_lock_keeps_the_home_from_a_successor() {
        use crate::native_local_provider::{take_process_lock, EARLIER_PROCESS, PROCESS_LOCK};
        let alive = |pid: i32| (unsafe { libc::kill(pid, 0) }) == 0;
        let until = |what: &str, done: &dyn Fn() -> bool| {
            let end = std::time::Instant::now() + std::time::Duration::from_secs(10);
            while !done() { assert!(std::time::Instant::now() < end, "{what}"); std::thread::sleep(std::time::Duration::from_millis(20)); }
        };
        let pid_in = |root: &Path, name: &str| std::fs::read_to_string(root.join(name)).ok().and_then(|text| text.trim().parse::<i32>().ok());
        let f = Fixture::new();
        let (home, bin) = (f.root.join("environment-home"), stand_in_leaving_a_holder(&f.root));
        std::fs::create_dir(&home).unwrap();
        struct EndHolders<'a>(&'a Path);
        impl Drop for EndHolders<'_> {
            fn drop(&mut self) {
                for name in ["holder-pid", "stand-in-pid"] {
                    if let Some(pid) = std::fs::read_to_string(self.0.join(name)).ok().and_then(|text| text.trim().parse::<i32>().ok()) { unsafe { libc::kill(pid, libc::SIGKILL); } }
                }
            }
        }
        let _end = EndHolders(&f.root);
        let (mut peer, seen) = route_peer(json!({"route":"environment","data":f.data,"root":f.root,"resources":f.resources,"home":home,"bin":bin}));
        assert!(seen.starts_with("ready"), "the first App has Codex ready on the home: {seen}");
        let (codex, holder) = (pid_in(&f.root, "stand-in-pid").unwrap(), pid_in(&f.root, "holder-pid").unwrap());
        assert_eq!(unsafe { libc::kill(peer.id() as i32, libc::SIGKILL) }, 0);
        peer.wait().unwrap();
        // Observed from outside: the stand-in Codex ended with its App; the program it started
        // lives on and holds the lock.
        until("the stand-in Codex has ended", &|| !alive(codex));
        assert!(alive(holder), "the program it left behind is alive");
        assert_eq!(take_process_lock(&home.join(PROCESS_LOCK)).unwrap_err(), EARLIER_PROCESS, "an independent attempt finds the lock held");
        let (state, app_home, desktop, started) = complete_startup(environment_input(&f.data, Some(&home), Some(&bin)), PathBuf::from("/invented/platform-app-data"), f.resources.clone(), &f.root);
        assert_eq!(desktop.lock().unwrap().view()["launch"]["state"], "environment", "the App data of a killed App is admitted");
        assert_eq!(started.expect("the automatic start is reached").unwrap_err(), crate::home_hold::PROCESS_HELD);
        let status = app_home.host.snapshot();
        assert_eq!((status["state"].as_str(), status["lastStartRefusal"]["reason"].as_str()), (Some("absent"), Some(crate::home_hold::PROCESS_HELD)));
        assert!(alive(holder) && server_starts(&f.root) == 1, "no second stand-in while the holder lives");
        unsafe { libc::kill(holder, libc::SIGKILL); }
        until("the holder has ended", &|| !alive(holder));
        let cfg = app_home.host_config.clone().unwrap();
        let ready = crate::automatic_start(&app_home.host, &app_home.recovery_startup, Ok(&f.data), &cfg, &desktop).unwrap();
        assert_eq!((ready["state"].as_str(), server_starts(&f.root)), (Some("ready"), 2));
        let _ = app_home.host.stop("fixture", "test ended");
        drop((state, app_home, desktop));
    }

    /// The child half of the first-save test: an App on never-used App data
    /// (at setup, holding nothing), which saves setup when told to and then
    /// lives until its stdin closes.
    #[test]
    fn first_save_peer() {
        let Ok(fixture) = std::env::var("CHIRALITY_FIRST_SAVE_FIXTURE") else {
            return;
        };
        use std::io::BufRead;
        let fixture: Value = serde_json::from_str(&fixture).unwrap();
        let path = |key: &str| PathBuf::from(fixture[key].as_str().unwrap());
        let (data, root) = (path("data"), path("root"));
        let shared = [path("config"), path("agents"), path("skills")];
        let mut setup = DesktopSetup::new(Ok(data.clone()), Ok(path("resources")));
        let launch = setup.resolve(None, true, || runtime_session::allocate_fresh_probe(&root));
        assert!(launch.host_config.is_err());
        println!("AT-SETUP {}", setup.view()["launch"]["state"]);
        std::io::Write::flush(&mut std::io::stdout()).unwrap();
        let mut lines = std::io::stdin().lock().lines();
        let _ = lines.next();
        let preview = setup.preview(shared, None, SUPPLIER).unwrap();
        let saved = setup.prepare_and_save(preview["token"].as_str().unwrap());
        println!("SAVED {}", saved.is_ok());
        std::io::Write::flush(&mut std::io::stdout()).unwrap();
        let _ = lines.next();
    }

    /// VER-010, first setup saves: two Apps on a never-used machine (App data
    /// that does not exist yet) both sit at setup holding nothing, and neither
    /// creates the App data directory by launching. The first to save creates
    /// it and holds it; the second's save is refused with the App data
    /// sentence and writes nothing.
    #[test]
    fn two_apps_at_first_setup_both_show_setup_and_the_second_save_is_refused() {
        use std::io::{BufRead, Write};
        let f = Fixture::new();
        let data = f.root.join("never-used-app-data");
        let mut child = std::process::Command::new(std::env::current_exe().unwrap())
            .args(["--exact", "desktop_startup::tests::first_save_peer", "--nocapture", "--test-threads=1"])
            .env("CHIRALITY_FIRST_SAVE_FIXTURE", json!({"data":data,"root":f.root,"resources":f.resources,"config":f.shared[0],"agents":f.shared[1],"skills":f.shared[2]}).to_string())
            .stdin(std::process::Stdio::piped())
            .stdout(std::process::Stdio::piped())
            .spawn()
            .unwrap();
        let mut lines = std::io::BufReader::new(child.stdout.take().unwrap()).lines();
        let mut next = |marker: &str| loop {
            let line = lines.next().expect("the peer reported").unwrap();
            if let Some((_, rest)) = line.split_once(marker) {
                break rest.trim().to_owned();
            }
        };
        assert_eq!(next("AT-SETUP "), "\"setup-required\"");
        let mut here = DesktopSetup::new(Ok(data.clone()), Ok(f.resources.clone()));
        let launch = here.resolve(None, true, || f.probe());
        assert!(launch.host_config.is_err());
        assert_eq!(here.view()["launch"]["state"], "setup-required", "this App shows setup too");
        assert!(!data.exists(), "neither App created the App data by launching");
        let preview = here.preview(f.shared.clone(), None, SUPPLIER).unwrap();
        let mut stdin = child.stdin.take().unwrap();
        writeln!(stdin, "save").unwrap();
        assert_eq!(next("SAVED "), "true", "the first to save holds the App data");
        let before = tree(&data);
        let refused = here.prepare_and_save(preview["token"].as_str().unwrap()).unwrap_err();
        assert_eq!(refused, DATA_HELD);
        assert_eq!(tree(&data), before, "the refused save wrote nothing");
        drop(stdin);
        child.wait().unwrap();
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
        // A second App on data this one holds: its own native view.
        let mut second = keep.setup();
        let launch = second.resolve(None, true, || panic!("a second App on held data allocates no probe"));
        assert!(!second.admit_root(launch, Ok(keep.data.clone())).allow_operational);
        let data_held = second.view();
        drop(second);
        let none_preview = fresh_q.preview_project(None).unwrap();
        let none_saved = fresh_q
            .prepare_and_save(none_preview["token"].as_str().unwrap())
            .unwrap();
        let fresh_use = Fixture::new();
        let mut first = fresh_use.setup();
        let launch = first.resolve(None, true, || panic!("setup has no probe"));
        first.admit_root(launch, Ok(fresh_use.data.clone()));
        let new_settings_preview = first.preview_new_settings(Some(fresh_use.project.clone())).unwrap();
        let new_settings_saved = first.prepare_and_save(new_settings_preview["token"].as_str().unwrap()).unwrap();
        let retained = json!({"initial":retain_initial,"preview":retain_preview,"saved":retain_saved,"conflict":conflict,"supersededError":superseded,"freshQ":q_view,"nonePreview":none_preview,"noneSaved":none_saved,"project":native_path_identity(&q),"currentProject":native_path_identity(&keep.project)});
        println!(
            "DESKTOP_SETUP_PACKETS={}",
            json!({"dataHeld":data_held,"newSettings":{"preview":new_settings_preview,"saved":new_settings_saved,"project":native_path_identity(&fresh_use.project)},"retained":retained,"initial":initial,"preview":preview,"saved":saved,"busy":busy,"fresh":fresh_view,"resourceLimits":resource_limits,"environment":environment.view(),"inputs":{"shared":f.shared.each_ref().map(|p|native_path_identity(p)),"project":native_path_identity(&f.project)}})
        );
    }

    /// First use with new App-owned settings: nothing exists after review; the
    /// confirmed prepare creates only the new settings leaf, the new home and
    /// the pending request, which the next launch admits.
    // The routes that use existing settings say the settings in use decide, and restate nothing.
    #[test]
    fn first_use_routes_with_existing_settings_say_their_settings_decide_and_restate_nothing() {
        let shared = DesktopSetup::first_use_defaults("new-home");
        assert_eq!(shared["sentences"][0], "Your own Codex settings decide what Codex may read and change, and where your sign-in is kept. The App does not change them and does not restate them here; after you reopen the App, Connection and access shows what Codex reports for this launch.");
        let kept = DesktopSetup::first_use_defaults("retain-account-project");
        assert!(kept["sentences"][0].as_str().unwrap().starts_with("This keeps your current sign-in folder and the settings it uses"));
        for view in [shared, kept] {
            let text = view.to_string();
            assert!(!text.contains("read-only") && !text.contains("auth.json") && !text.contains("by default"), "no default is restated as the settings in use");
        }
    }
    #[test]
    fn new_settings_are_created_only_at_confirmed_prepare_inside_the_app_data() {
        use std::os::unix::fs::PermissionsExt;
        let f = Fixture::new();
        let outside = |root: &Path| -> Vec<PathBuf> {
            fn walk(at: &Path, skip: &Path, out: &mut Vec<PathBuf>) { for e in std::fs::read_dir(at).unwrap() { let p = e.unwrap().path(); if p.starts_with(skip) { continue; } out.push(p.clone()); if p.is_dir() && !p.is_symlink() { walk(&p, skip, out); } } }
            let mut out = vec![]; walk(root, &f.data, &mut out); out.sort(); out
        };
        let before = outside(&f.root);
        let mut setup = f.setup();
        let launch = setup.resolve(None, true, || panic!("setup has no probe"));
        setup.admit_root(launch, Ok(f.data.clone()));
        let preview = setup.preview_new_settings(Some(f.project.clone())).unwrap();
        let settings = PathBuf::from(preview["settings"].as_str().unwrap());
        let account = PathBuf::from(preview["accountHome"].as_str().unwrap());
        assert_eq!(preview["kind"], "new-settings");
        assert!(preview["effects"].as_array().unwrap().iter().all(|e| !e.as_str().unwrap().contains(f.data.to_str().unwrap())), "review effects name no internal path");
        assert_eq!(preview["locations"][0]["path"], settings.display().to_string());
        assert_eq!(preview["locations"][1]["path"], preview["accountHome"]);
        let statement = setup.preview_statement(preview["token"].as_str().unwrap()).unwrap();
        assert!(statement.contains(&settings.display().to_string()) && statement.contains(preview["accountHome"].as_str().unwrap()), "the native statement still names the exact locations");
        assert_eq!(settings.parent().unwrap(), f.data.join(SETTINGS));
        assert!(!settings.exists() && !account.exists(), "review creates nothing");
        assert!(setup.preview_statement(preview["token"].as_str().unwrap()).unwrap().contains("Read, import or change no other Codex settings, home or credential"));
        // Before confirming, the review page says what Codex may do by default and where a sign-in is
        // kept, as Codex's defaults; the sheet says what Codex adds when it starts and no more.
        assert_eq!(preview["defaults"]["heading"], "What applies by default");
        let defaults: Vec<&str> = preview["defaults"]["sentences"].as_array().unwrap().iter().map(|s| s.as_str().unwrap()).collect();
        assert_eq!(defaults.first(), Some(&"With new settings, Codex's own defaults apply; the App sets none of these."));
        assert!(defaults.contains(&"By default, Codex can read any file your Mac account can read, inside and outside your project, so choose a project folder with that in mind."));
        assert!(defaults.iter().any(|s| s.starts_with("By default your ChatGPT sign-in is kept as a file, auth.json, in the sign-in folder")));
        // Nothing says or implies the agent asks before it changes something (the owner, 14 November).
        assert!(defaults.iter().all(|s| !s.contains("allow") && !s.contains("ask") && !s.contains("permission")), "no sentence rests on asking before change");
        assert!(statement.contains("with an empty config.toml, an empty AGENTS.md and a skills folder. Codex adds its own system skills there, and its own working files to the account directory, when it starts.\n"));
        assert!(!statement.contains("an empty skills folder") && !statement.contains("Codex's defaults then apply"), "the sheet carries only the corrected line");
        assert!(preview["effects"][1].as_str().unwrap().contains("a skills folder; Codex adds its own system skills there"));
        assert_eq!(setup.preview_action(preview["token"].as_str().unwrap()).unwrap(), "Create settings and save for next launch");
        let saved = setup.prepare_and_save(preview["token"].as_str().unwrap()).unwrap();
        assert_eq!(saved["pending"]["state"], "saved-for-next-launch", "{saved}");
        for (name, dir) in [("config.toml", false), ("AGENTS.md", false), ("skills", true)] {
            let target = settings.join(name);
            let meta = std::fs::symlink_metadata(&target).unwrap();
            assert_eq!(meta.is_dir(), dir, "{name}"); assert!(!meta.file_type().is_symlink());
            assert_eq!(meta.permissions().mode() & 0o777, if dir { 0o700 } else { 0o600 }, "{name}");
            if dir { assert_eq!(std::fs::read_dir(&target).unwrap().count(), 0); } else { assert_eq!(meta.len(), 0); assert_eq!(meta.nlink(), 1); }
            assert_eq!(location(&account.join(name)).unwrap(), location(&target).unwrap(), "{name}: the home links to the new settings");
        }
        assert_eq!(std::fs::symlink_metadata(&settings).unwrap().permissions().mode() & 0o777, 0o700);
        assert_eq!(outside(&f.root), before, "nothing outside the App data is created or changed");
        drop(setup);
        let mut next = f.setup();
        let launch = f.resolve(&mut next);
        assert!(next.admit_root(launch, Ok(f.data.clone())).allow_operational, "the next launch admits the saved request");

        // A path created at a reviewed target before confirmation is never adopted or overwritten.
        let g = Fixture::new();
        let mut setup = g.setup();
        let launch = setup.resolve(None, true, || panic!("setup has no probe"));
        setup.admit_root(launch, Ok(g.data.clone()));
        let preview = setup.preview_new_settings(None).unwrap();
        assert!(preview["project"].is_null());
        let settings = PathBuf::from(preview["settings"].as_str().unwrap());
        protected_directory(settings.parent().unwrap()).unwrap();
        std::fs::DirBuilder::new().mode(0o700).create(&settings).unwrap();
        std::fs::write(settings.join("config.toml"), b"invented existing settings").unwrap();
        let refused = setup.prepare_and_save(preview["token"].as_str().unwrap()).unwrap_err();
        assert!(refused.contains("never adopted"), "{refused}");
        assert_eq!(std::fs::read(settings.join("config.toml")).unwrap(), b"invented existing settings");
        assert!(!PathBuf::from(preview["accountHome"].as_str().unwrap()).exists(), "no home without its settings");
        assert!(setup.view()["pending"].is_null() || setup.view()["pending"]["state"] != "saved-for-next-launch");
    }

    /// Review finding (PR #111): a same-user swap of a directory or a created
    /// file at each step must neither write outside App data nor publish a
    /// request naming a replacement.
    #[test]
    fn new_settings_creation_refuses_directory_swaps_and_replaced_files() {
        fn run(step: &'static str, act: fn(&Path, &Path, &Path)) -> (String, PathBuf, Fixture) {
            let f = Fixture::new();
            let outside = f.root.join("outside-target");
            std::fs::create_dir(&outside).unwrap();
            let mut setup = f.setup();
            let launch = setup.resolve(None, true, || panic!("setup has no probe"));
            setup.admit_root(launch, Ok(f.data.clone()));
            let preview = setup.preview_new_settings(None).unwrap();
            let settings = PathBuf::from(preview["settings"].as_str().unwrap());
            let (data, leaf, out) = (f.data.clone(), settings.clone(), outside.clone());
            SETTINGS_HOOK.with(|h| *h.borrow_mut() = Some(Box::new(move |at| if at == step { act(&data, &leaf, &out); })));
            let result = setup.prepare_and_save(preview["token"].as_str().unwrap());
            SETTINGS_HOOK.with(|h| *h.borrow_mut() = None);
            let error = result.unwrap_err();
            assert_eq!(std::fs::read_dir(&outside).unwrap().count(), 0, "{step}: nothing is written outside App data");
            assert!(!f.data.join(PROFILE).exists(), "{step}: no request is saved");
            (error, settings, f)
        }
        let (error, _, _) = run("after-parent-check", |data, _, out| {
            std::fs::rename(data.join(SETTINGS), data.join("moved-settings")).unwrap();
            std::os::unix::fs::symlink(out, data.join(SETTINGS)).unwrap();
        });
        assert!(error.contains("without following links"), "{error}");
        let (error, _, _) = run("after-leaf-create", |_, leaf, out| {
            std::fs::rename(leaf, leaf.with_extension("moved")).unwrap();
            std::os::unix::fs::symlink(out, leaf).unwrap();
        });
        assert!(error.contains("without following links"), "{error}");
        for step in ["after-create", "before-publish"] {
            let (error, settings, _kept) = run(step, |_, leaf, _| {
                std::fs::remove_file(leaf.join("config.toml")).unwrap();
                std::fs::write(leaf.join("config.toml"), b"invented replacement settings").unwrap();
            });
            assert!(error.contains("replaced"), "{step}: {error}");
            assert_eq!(std::fs::read(settings.join("config.toml")).unwrap(), b"invented replacement settings", "{step}: the replacement is not adopted or overwritten");
        }
        let (error, _, _) = run("before-publish", |data, _, out| {
            std::fs::rename(data.join(SETTINGS), data.join("moved-settings")).unwrap();
            std::os::unix::fs::symlink(out, data.join(SETTINGS)).unwrap();
        });
        assert!(error.contains("symlink") || error.contains("replaced"), "{error}");
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
