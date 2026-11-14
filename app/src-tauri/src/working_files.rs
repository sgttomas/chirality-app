//! DEL-01-01: the App's working folders, kept beside the App data folder in
//! "<App data folder's name> Working Files" and never in a temporary folder.
//! Each folder the App makes there is made by [`WorkingFiles::allocate`]:
//! - the label probe's home (`probe-homes/`);
//! - the connector's working folder (`connector/`);
//! - the temporary folder Codex is given as its TMPDIR (`codex-tmp/`).
//!
//! **The claim** (with its boundary in the pull request that made this): the
//! App allocates no working state at a location a sandboxed Codex can write.
//! These folders are outside the App data folder and outside every temporary
//! folder. Codex's TMPDIR is made writable to Codex on purpose; it is one
//! folder inside its subtree, never the subtree or another folder.
//!
//! **What shows a folder handed out is the one the App made.** Checked in
//! [`WorkingFiles::allocate`], once, before the path is returned:
//! - the Working Files folder and the subtree are opened with no link followed,
//!   and each is the folder established (device and inode), private and this
//!   user's;
//! - the folder is made with `mkdirat` inside that subtree's descriptor, opened
//!   from it with no link followed, and is a folder of this user, private,
//!   empty, and created no earlier than just before it was made;
//! - after its record is written, its name in the subtree still leads to that
//!   same folder, compared with the opened descriptor.
//!
//! Any of these failing refuses the start. The descriptor is closed when
//! `allocate` returns: the evidence holds at that moment and shows nothing
//! afterwards. Codex, the probe and the connector then reach the folder by its
//! path. The path leads to the folder only while the directory entry that names
//! it, and the entry of each ancestor up to the file system's root, cannot be
//! replaced by a writer the App defends against. What protects that after
//! allocation is that, under the permissions Codex actually has, it cannot
//! write in the folder holding the entry or in any ancestor of it. That is a
//! matter of effective permissions (the pull request that made this states it
//! for each configuration). The App removes nothing through these paths.
//!
//! **Nothing is removed.** No folder here, and nothing in one, is removed or
//! emptied by this version (LIM-021); a later unit reclaims them.
//!
//! **The record.** One file per folder made (`.made-<name>.json`, beside it in
//! its subtree), created exclusively with no link followed, before the folder
//! is used. Nothing in this version reads it or acts on it, and it is never
//! replaced: it is written for the later unit, and is not a control.
use std::ffi::{CString, OsStr};
use std::fs::File;
use std::os::fd::{AsRawFd, FromRawFd};
use std::os::unix::ffi::OsStrExt;
use std::os::unix::fs::{DirBuilderExt, MetadataExt, OpenOptionsExt};
use std::path::{Path, PathBuf};

/// What the Working Files folder's name adds to the App data folder's name.
pub const SUFFIX: &str = " Working Files";
/// Every record's name begins so; the rest is the folder's name.
const RECORD_PREFIX: &str = ".made-";

/// The one place the Working Files folder's path is derived: the App data
/// folder's own name and [`SUFFIX`], beside it. A folder is never taken as the
/// App's by this name alone; [`establish`] checks what it is.
pub fn folder_for(app_data: &Path) -> Result<PathBuf, String> {
    let (Some(parent), Some(name)) = (app_data.parent(), app_data.file_name()) else {
        return Err(format!("Chirality's data folder {} has no parent folder to keep its working files beside", app_data.display()));
    };
    let mut leaf = name.to_os_string();
    leaf.push(SUFFIX);
    Ok(parent.join(leaf))
}

/// How many folders are in the Working Files subtrees of `app_data` now,
/// listed by name only: every folder this and earlier launches made, which
/// this version keeps. `None` when a subtree cannot be listed.
pub fn kept_count(app_data: &Path) -> Option<usize> {
    let root = folder_for(app_data).ok()?;
    let mut count = 0;
    for kind in Kind::ALL {
        match std::fs::read_dir(root.join(kind.subtree())) {
            Ok(entries) => {
                count += entries.flatten().filter(|e| !e.file_name().to_string_lossy().starts_with(".made")).count();
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
            Err(_) => return None,
        }
    }
    Some(count)
}

/// The kinds of folder the App makes here, each in its own subtree.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    ProbeHome,
    Connector,
    CodexTmp,
}
impl Kind {
    pub const ALL: [Kind; 3] = [Kind::ProbeHome, Kind::Connector, Kind::CodexTmp];
    fn subtree(self) -> &'static str {
        match self {
            Kind::ProbeHome => "probe-homes",
            Kind::Connector => "connector",
            Kind::CodexTmp => "codex-tmp",
        }
    }
    fn prefix(self) -> &'static str {
        match self {
            Kind::ProbeHome => "probe-",
            Kind::Connector => "connector-",
            Kind::CodexTmp => "tmp-",
        }
    }
    fn index(self) -> usize {
        self as usize
    }
}

/// A folder's identity as recorded: device, inode and creation time.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Stamp {
    dev: u64,
    ino: u64,
    created_secs: i64,
    created_nanos: i64,
}
impl Stamp {
    /// The creation (birth) time where the system keeps one (macOS does);
    /// otherwise the status-change time.
    #[cfg(any(target_os = "macos", target_os = "ios"))]
    fn of_stat(st: &libc::stat) -> Stamp {
        Stamp { dev: st.st_dev as u64, ino: st.st_ino, created_secs: st.st_birthtime, created_nanos: st.st_birthtime_nsec }
    }
    #[cfg(not(any(target_os = "macos", target_os = "ios")))]
    fn of_stat(st: &libc::stat) -> Stamp {
        Stamp { dev: st.st_dev as u64, ino: st.st_ino as u64, created_secs: st.st_ctime as i64, created_nanos: st.st_ctime_nsec as i64 }
    }
    fn to_json(self, name: &str) -> serde_json::Value {
        serde_json::json!({"name": name, "dev": self.dev.to_string(), "ino": self.ino.to_string(),
            "createdSecs": self.created_secs.to_string(), "createdNanos": self.created_nanos.to_string()})
    }
}

/// A folder the App made here, with the identity it was recorded under.
#[derive(Clone, Debug)]
pub struct Made {
    pub path: PathBuf,
    pub kind: Kind,
    #[cfg_attr(not(test), allow(dead_code))]
    name: String,
    #[cfg_attr(not(test), allow(dead_code))]
    stamp: Stamp,
}

/// A folder's device and inode.
type Id = (u64, u64);

/// The Working Files folder, established: a real private folder of this user
/// beside the App data folder, with its three subtrees.
#[derive(Clone, Debug)]
pub struct WorkingFiles {
    root: PathBuf,
    root_id: Id,
    subtrees: [Id; 3],
}

fn euid() -> u32 {
    unsafe { libc::geteuid() }
}
/// Whether `meta` is a real private folder of this user; otherwise what it is,
/// in the person's words.
fn private_folder(path: &Path, meta: &std::fs::Metadata) -> Result<(), String> {
    let kind = meta.file_type();
    if kind.is_symlink() {
        return Err(format!("a link to {}", std::fs::read_link(path).unwrap_or_default().display()));
    }
    if !kind.is_dir() {
        return Err(if kind.is_file() { "a file".into() } else { "something that is not a folder".into() });
    }
    if meta.uid() != euid() {
        return Err("a folder that belongs to another account".into());
    }
    if meta.mode() & 0o077 != 0 {
        return Err("a folder that other accounts can use".into());
    }
    Ok(())
}
/// Makes `path` (0700) only where it is established to be absent, then checks
/// it is a real private folder of this user. Never removes or replaces what is
/// there. The error is what the person is told.
fn establish_folder(path: &Path, what: &str) -> Result<Id, String> {
    let refused = |why: String| format!("Chirality keeps {what} at {}. {why} Move it aside (do not delete what a link points to) and start Chirality again.", path.display());
    match std::fs::symlink_metadata(path) {
        Ok(_) => {}
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            match std::fs::DirBuilder::new().mode(0o700).create(path) {
                Ok(()) => {
                    if let Some(parent) = path.parent() {
                        crate::storage::sync_dir(parent).map_err(|e| refused(format!("It could not be made: {e}.")))?;
                    }
                }
                Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
                Err(e) => return Err(refused(format!("It could not be made: {e}."))),
            }
        }
        Err(e) => return Err(refused(format!("It could not be examined: {e}."))),
    }
    let meta = std::fs::symlink_metadata(path).map_err(|e| refused(format!("It could not be examined: {e}.")))?;
    private_folder(path, &meta).map_err(|what| refused(format!("Something else is there now: {what}.")))?;
    Ok((meta.dev(), meta.ino()))
}

/// The start's step that makes the Working Files folder and its subtrees. The
/// App data folder must already exist and be held. Refused, with words the
/// person can act on, when a folder cannot be made or is not the App's own;
/// there is no fall-back to a temporary folder.
pub fn establish(app_data: &Path) -> Result<WorkingFiles, String> {
    let root = folder_for(app_data)?;
    let root_id = establish_folder(&root, "its working files")?;
    let data = std::fs::metadata(app_data).map_err(|e| format!("Chirality's data folder {} could not be examined: {e}", app_data.display()))?;
    if (data.dev(), data.ino()) == root_id {
        return Err(format!("Chirality's working files {} are its data folder under another name; move one of them aside and start Chirality again.", root.display()));
    }
    let mut subtrees = [(0, 0); 3];
    for kind in Kind::ALL {
        subtrees[kind.index()] = establish_folder(&root.join(kind.subtree()), "a working folder")?;
    }
    Ok(WorkingFiles { root, root_id, subtrees })
}

// Descriptor steps. Every open here follows no link at its last name, and every
// name is a single entry of the folder whose descriptor is given.
fn c_name(name: &OsStr) -> std::io::Result<CString> {
    CString::new(name.as_bytes()).map_err(|_| std::io::Error::new(std::io::ErrorKind::InvalidInput, "a name holding a NUL"))
}
fn open_dir(path: &Path) -> std::io::Result<File> {
    std::fs::OpenOptions::new().read(true).custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC).open(path)
}
fn open_dir_at(dir: &File, name: &OsStr) -> std::io::Result<File> {
    let name = c_name(name)?;
    // SAFETY: a valid descriptor and NUL-terminated name; on success the new descriptor is ours.
    let fd = unsafe { libc::openat(dir.as_raw_fd(), name.as_ptr(), libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC) };
    if fd < 0 { Err(std::io::Error::last_os_error()) } else { Ok(unsafe { File::from_raw_fd(fd) }) }
}
fn stat_of(file: &File) -> std::io::Result<libc::stat> {
    // SAFETY: a valid descriptor; `st` is written by the system.
    let mut st: libc::stat = unsafe { std::mem::zeroed() };
    if unsafe { libc::fstat(file.as_raw_fd(), &mut st) } != 0 { Err(std::io::Error::last_os_error()) } else { Ok(st) }
}
fn stat_at(dir: &File, name: &OsStr) -> std::io::Result<libc::stat> {
    let name = c_name(name)?;
    // SAFETY: as above; the entry itself is examined, never what a link names.
    let mut st: libc::stat = unsafe { std::mem::zeroed() };
    if unsafe { libc::fstatat(dir.as_raw_fd(), name.as_ptr(), &mut st, libc::AT_SYMLINK_NOFOLLOW) } != 0 { Err(std::io::Error::last_os_error()) } else { Ok(st) }
}
fn is_dir(st: &libc::stat) -> bool {
    st.st_mode & libc::S_IFMT == libc::S_IFDIR
}
fn id_of(st: &libc::stat) -> Id {
    (st.st_dev as u64, st.st_ino as u64)
}

impl WorkingFiles {
    pub fn root(&self) -> &Path {
        &self.root
    }
    fn subtree(&self, kind: Kind) -> PathBuf {
        self.root.join(kind.subtree())
    }
    /// `kind`'s subtree, opened through the Working Files folder, each with no
    /// link followed and each the folder established, private and this user's.
    fn open_subtree(&self, kind: Kind) -> Result<File, String> {
        let changed = |what: &Path, why: String| format!("Chirality's working folder {} {why}; move it aside and start Chirality again.", what.display());
        let check = |file: &File, path: &Path, id: Id| -> Result<(), String> {
            let st = stat_of(file).map_err(|e| changed(path, format!("could not be examined ({e})")))?;
            if id_of(&st) != id || st.st_uid != euid() || st.st_mode & 0o077 != 0 {
                return Err(changed(path, "is no longer the folder Chirality made".into()));
            }
            Ok(())
        };
        let root = open_dir(&self.root).map_err(|e| changed(&self.root, format!("could not be opened as a folder ({e})")))?;
        check(&root, &self.root, self.root_id)?;
        let path = self.subtree(kind);
        let subtree = open_dir_at(&root, OsStr::new(kind.subtree())).map_err(|e| changed(&path, format!("could not be opened as a folder ({e})")))?;
        check(&subtree, &path, self.subtrees[kind.index()])?;
        Ok(subtree)
    }
    /// Makes a new folder of `kind` inside the subtree as established, checks
    /// it is the new, empty, private folder made, records it, and checks that
    /// its name still leads to it, before its path is returned for use.
    pub fn allocate(&self, kind: Kind) -> Result<Made, String> {
        let subtree = self.open_subtree(kind)?;
        let name = crate::util::opaque_id(kind.prefix())?;
        let path = self.subtree(kind).join(&name);
        let before = std::time::SystemTime::now();
        let c = c_name(OsStr::new(&name)).map_err(|e| e.to_string())?;
        // SAFETY: as in the descriptor steps; fails if anything has the name.
        if unsafe { libc::mkdirat(subtree.as_raw_fd(), c.as_ptr(), 0o700) } != 0 {
            return Err(format!("Chirality could not make the working folder {}: {}", path.display(), std::io::Error::last_os_error()));
        }
        let (folder, stamp) = Self::made_folder(&subtree, OsStr::new(&name), before)
            .map_err(|why| format!("Chirality could not use the working folder it made at {} ({why}); it is not used, and the start was refused.", path.display()))?;
        Self::write_record(&subtree, &name, stamp)
            .map_err(|why| format!("Chirality could not record the working folder {} ({why}); it is not used, and the start was refused.", path.display()))?;
        Self::still_named(&subtree, OsStr::new(&name), &folder)
            .map_err(|why| format!("Chirality could not use the working folder it made at {} ({why}); it is not used, and the start was refused.", path.display()))?;
        Ok(Made { path, kind, name, stamp })
    }
    /// The folder `name` of `subtree`, opened with no link followed, if it is
    /// a folder of this user, private, empty and created no earlier than
    /// `before`: the one just made.
    fn made_folder(subtree: &File, name: &OsStr, before: std::time::SystemTime) -> Result<(File, Stamp), String> {
        let folder = open_dir_at(subtree, name).map_err(|e| format!("it could not be opened as a folder: {e}"))?;
        let st = stat_of(&folder).map_err(|e| format!("it could not be examined: {e}"))?;
        if st.st_uid != euid() || st.st_mode & 0o077 != 0 {
            return Err("it is not a private folder of this account".into());
        }
        let empty = crate::workflow_workspace::names_in(&folder).map_err(|e| format!("what it holds could not be listed: {e}"))?.is_empty();
        if !empty {
            return Err("it is not empty".into());
        }
        let stamp = Stamp::of_stat(&st);
        let made_at = std::time::UNIX_EPOCH + std::time::Duration::new(stamp.created_secs.max(0) as u64, stamp.created_nanos.clamp(0, 999_999_999) as u32);
        // The filesystem's clock and this one: a second's allowance either way.
        if made_at + std::time::Duration::from_secs(1) < before {
            return Err("it was created before Chirality made it".into());
        }
        Ok((folder, stamp))
    }
    /// The record of one folder made, created exclusively beside it, with no
    /// link followed, and never read or replaced by this version.
    fn write_record(subtree: &File, name: &str, stamp: Stamp) -> Result<(), String> {
        use std::io::Write;
        let bytes = serde_json::to_vec(&stamp.to_json(name)).map_err(|e| e.to_string())?;
        let record = c_name(OsStr::new(&format!("{RECORD_PREFIX}{name}.json"))).map_err(|e| e.to_string())?;
        // SAFETY: as in the descriptor steps; made new, never through a link.
        let fd = unsafe { libc::openat(subtree.as_raw_fd(), record.as_ptr(), libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC, 0o600 as libc::c_uint) };
        if fd < 0 {
            return Err(std::io::Error::last_os_error().to_string());
        }
        let mut file = unsafe { File::from_raw_fd(fd) };
        file.write_all(&bytes).and_then(|()| file.sync_all()).map_err(|e| e.to_string())?;
        subtree.sync_all().map_err(|e| e.to_string())
    }
    /// Whether `name` in `subtree` still leads to the opened `folder`.
    fn still_named(subtree: &File, name: &OsStr, folder: &File) -> Result<(), String> {
        let named = stat_at(subtree, name).map_err(|e| format!("its name no longer leads to a folder: {e}"))?;
        let opened = stat_of(folder).map_err(|e| format!("it could not be examined: {e}"))?;
        if !is_dir(&named) || id_of(&named) != id_of(&opened) {
            return Err("its name now leads somewhere else".into());
        }
        Ok(())
    }
}

/// The Working Files of the App data folder this launch holds, established
/// once at its first use.
static LAUNCH: std::sync::Mutex<Option<(PathBuf, WorkingFiles)>> = std::sync::Mutex::new(None);
/// The Working Files of `app_data` for this launch.
pub fn for_launch(app_data: &Path) -> Result<WorkingFiles, String> {
    let mut launch = LAUNCH.lock().unwrap_or_else(|e| e.into_inner());
    if let Some((data, working)) = launch.as_ref() {
        if data == app_data {
            return Ok(working.clone());
        }
    }
    let working = establish(app_data)?;
    *launch = Some((app_data.to_path_buf(), working.clone()));
    Ok(working)
}
/// The Working Files this launch established, for a caller that does not
/// know the App data folder. Refused when none is established: there is no
/// fall-back to a temporary folder. Tests that make none get their own, under
/// a temporary folder of the test run.
pub fn launch() -> Result<WorkingFiles, String> {
    // Tests share one process: a fixture's Working Files may be gone by the time another test
    // asks, so tests always use their own.
    #[cfg(not(test))]
    if let Some((_, working)) = LAUNCH.lock().unwrap_or_else(|e| e.into_inner()).as_ref() {
        return Ok(working.clone());
    }
    #[cfg(test)]
    {
        static TEST: std::sync::OnceLock<Result<WorkingFiles, String>> = std::sync::OnceLock::new();
        return TEST.get_or_init(|| {
            let data = std::fs::canonicalize(std::env::temp_dir()).map_err(|e| e.to_string())?.join(crate::util::opaque_id("test-app-data-")?);
            std::fs::create_dir_all(&data).map_err(|e| e.to_string())?;
            establish(&data)
        }).clone();
    }
    #[allow(unreachable_code)]
    Err("Chirality's working files are not set up for this launch, so nothing was made".into())
}

#[cfg(test)]
#[path = "working_files_tests.rs"]
mod tests;
