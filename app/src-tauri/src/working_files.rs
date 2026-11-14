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
//! folder inside its subtree, never the subtree, its record or another folder.
//!
//! **Allocation.** The Working Files folder and each subtree are opened with no
//! link followed and must be the folders established; a folder is made inside
//! the subtree's descriptor, opened from it with no link followed, checked to
//! be new, empty and private, recorded, and its descriptor held for the rest of
//! the launch.
//!
//! **What authorises disposal.** Only a verified allocation of this launch, and
//! only its contents: what is in a folder the App made and still holds is
//! removed through that held descriptor, never by looking its name up again,
//! and the folder itself is kept. Excluded whatever contains them, and keeping
//! everything still in that folder when found:
//! - the protected folders (the App data folder and the person's own Codex
//!   home, by identity, following links);
//! - an entry named as Codex names a file in its home (looked for by name, never
//!   opened);
//! - a folder, or a file with a single name, whose creation time is earlier
//!   than the made folder's recorded creation time: it was moved in from
//!   elsewhere;
//! - anything on another device: a volume mounted there.
//!
//! Nothing is opened but folders, from their parent's descriptor with no link
//! followed.
//!
//! **Reach.** The disposal removes nothing that whoever may write in that folder
//! could not remove themselves. An entry made there is one its writer can
//! unlink. An entry moved in took write on the folder it came from, which is the
//! right to remove it there. A link is removed as a link, never followed. A file
//! with another name elsewhere loses only this name.
//!
//! **Not removed in this version.** The emptied folders, and whatever an
//! earlier launch left (one that ended without emptying its folders): they are
//! kept and reported at the next start. No record is trusted to authorise a
//! removal; the record is written before each folder is used, for the later
//! unit that reclaims them.
use std::ffi::{CString, OsStr, OsString};
use std::fs::File;
use std::os::fd::{AsRawFd, FromRawFd};
use std::os::unix::ffi::OsStrExt;
use std::os::unix::fs::{DirBuilderExt, MetadataExt, OpenOptionsExt};
use std::path::{Path, PathBuf};

/// What the Working Files folder's name adds to the App data folder's name.
pub const SUFFIX: &str = " Working Files";
/// The names under which Codex keeps files in its home: its sign-in, its
/// settings and its history (HOSTING, DEL-01-05). Looked for by name only;
/// never opened here.
const CODEX_HOME_FILES: [&str; 3] = ["auth.json", "config.toml", "history.jsonl"];
const RECORD: &str = ".made.json";
/// One writer of the records at a time in this process; the App's process lock
/// keeps other processes out of this App data folder's working files.
static RECORDS: std::sync::Mutex<()> = std::sync::Mutex::new(());
fn records_lock() -> std::sync::MutexGuard<'static, ()> {
    RECORDS.lock().unwrap_or_else(|e| e.into_inner())
}

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
/// listed by name only: what this and earlier launches made, which this
/// version keeps. `None` when a subtree cannot be listed.
pub fn kept_count(app_data: &Path) -> Option<usize> {
    let root = folder_for(app_data).ok()?;
    let mut count = 0;
    for kind in Kind::ALL {
        match std::fs::read_dir(root.join(kind.subtree())) {
            Ok(entries) => {
                count += entries.flatten().filter(|e| {
                    let name = e.file_name().to_string_lossy().into_owned();
                    name != RECORD && !name.starts_with(&format!("{RECORD}."))
                }).count();
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

/// A folder's identity as recorded: device, inode and creation time. An inode
/// can be reused after a folder is removed from outside; the creation time
/// makes a later folder with a reused number fail the check.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Stamp {
    dev: u64,
    ino: u64,
    created_secs: i64,
    created_nanos: i64,
}
impl Stamp {
    /// The creation (birth) time where the system keeps one (macOS does);
    /// otherwise the status-change time, which a later folder with a reused
    /// inode also fails to match.
    #[cfg(any(target_os = "macos", target_os = "ios"))]
    fn of_stat(st: &libc::stat) -> Stamp {
        Stamp { dev: st.st_dev as u64, ino: st.st_ino, created_secs: st.st_birthtime, created_nanos: st.st_birthtime_nsec }
    }
    #[cfg(not(any(target_os = "macos", target_os = "ios")))]
    fn of_stat(st: &libc::stat) -> Stamp {
        Stamp { dev: st.st_dev as u64, ino: st.st_ino as u64, created_secs: st.st_ctime as i64, created_nanos: st.st_ctime_nsec as i64 }
    }
    #[cfg(test)]
    fn of(meta: &std::fs::Metadata) -> Stamp {
        #[cfg(any(target_os = "macos", target_os = "ios"))]
        let (created_secs, created_nanos) = {
            let d = meta.created().unwrap().duration_since(std::time::UNIX_EPOCH).unwrap();
            (d.as_secs() as i64, d.subsec_nanos() as i64)
        };
        #[cfg(not(any(target_os = "macos", target_os = "ios")))]
        let (created_secs, created_nanos) = (meta.ctime(), meta.ctime_nsec());
        Stamp { dev: meta.dev(), ino: meta.ino(), created_secs, created_nanos }
    }
    fn made_before(self, other: Stamp) -> bool {
        (self.created_secs, self.created_nanos) < (other.created_secs, other.created_nanos)
    }
    fn to_json(self, name: &str) -> serde_json::Value {
        serde_json::json!({"name": name, "dev": self.dev.to_string(), "ino": self.ino.to_string(),
            "createdSecs": self.created_secs.to_string(), "createdNanos": self.created_nanos.to_string()})
    }
    fn from_json(v: &serde_json::Value) -> Option<(String, Stamp)> {
        let text = |k: &str| v.get(k).and_then(serde_json::Value::as_str);
        Some((text("name")?.to_owned(), Stamp {
            dev: text("dev")?.parse().ok()?,
            ino: text("ino")?.parse().ok()?,
            created_secs: text("createdSecs")?.parse().ok()?,
            created_nanos: text("createdNanos")?.parse().ok()?,
        }))
    }
}

/// A folder the App made here, with the identity it was recorded under.
#[derive(Clone, Debug)]
pub struct Made {
    pub path: PathBuf,
    pub kind: Kind,
    /// The name it was recorded under, beside its identity.
    #[cfg_attr(not(test), allow(dead_code))]
    name: String,
    stamp: Stamp,
    /// The folder as made, held open: its contents are removed through this,
    /// never through its name.
    folder: std::sync::Arc<File>,
}

/// What a cleaning did: what it removed, and what it kept and why.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Cleaning {
    pub removed: Vec<PathBuf>,
    pub kept: Vec<(PathBuf, String)>,
}

/// A folder's device and inode.
type Id = (u64, u64);

/// The Working Files folder, established: a real private folder of this user
/// beside the App data folder, with its three subtrees, and the folders no
/// cleaning may remove.
#[derive(Clone, Debug)]
pub struct WorkingFiles {
    root: PathBuf,
    root_id: Id,
    subtrees: [Id; 3],
    /// The App data folder and the person's own Codex home: their identities
    /// are taken, following links, when established and again at each use.
    protected: Vec<PathBuf>,
    protected_ids: Vec<Id>,
    /// The folders this launch made and holds, until each is emptied.
    held: std::sync::Arc<std::sync::Mutex<Vec<Made>>>,
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
/// The folders a cleaning protects for `app_data`: the App data folder and the
/// person's own Codex home.
fn protected_for(app_data: &Path) -> Vec<PathBuf> {
    let mut protected = vec![app_data.to_path_buf()];
    if let Some(home) = std::env::var_os("HOME") {
        protected.push(PathBuf::from(home).join(".codex"));
    }
    protected
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
    let mut working = WorkingFiles { root, root_id, subtrees, protected: Vec::new(), protected_ids: Vec::new(), held: Default::default() };
    working.protect(&protected_for(app_data))?;
    Ok(working)
}

// Descriptor steps. Every open here follows no link at its last name, and every
// name is a single entry of the folder whose descriptor is given.
const DIR_FLAGS: libc::c_int = libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC;
fn c_name(name: &OsStr) -> std::io::Result<CString> {
    CString::new(name.as_bytes()).map_err(|_| std::io::Error::new(std::io::ErrorKind::InvalidInput, "a name holding a NUL"))
}
fn last_error<T>() -> std::io::Result<T> {
    Err(std::io::Error::last_os_error())
}
fn open_dir(path: &Path) -> std::io::Result<File> {
    std::fs::OpenOptions::new().read(true).custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC).open(path)
}
fn open_dir_at(dir: &File, name: &OsStr) -> std::io::Result<File> {
    let name = c_name(name)?;
    // SAFETY: a valid descriptor and NUL-terminated name; on success the new descriptor is ours.
    let fd = unsafe { libc::openat(dir.as_raw_fd(), name.as_ptr(), DIR_FLAGS) };
    if fd < 0 { last_error() } else { Ok(unsafe { File::from_raw_fd(fd) }) }
}
fn stat_of(file: &File) -> std::io::Result<libc::stat> {
    // SAFETY: a valid descriptor; `st` is written by the system.
    let mut st: libc::stat = unsafe { std::mem::zeroed() };
    if unsafe { libc::fstat(file.as_raw_fd(), &mut st) } != 0 { last_error() } else { Ok(st) }
}
fn stat_at(dir: &File, name: &OsStr) -> std::io::Result<libc::stat> {
    let name = c_name(name)?;
    // SAFETY: as above; the entry itself is examined, never what a link names.
    let mut st: libc::stat = unsafe { std::mem::zeroed() };
    if unsafe { libc::fstatat(dir.as_raw_fd(), name.as_ptr(), &mut st, libc::AT_SYMLINK_NOFOLLOW) } != 0 { last_error() } else { Ok(st) }
}
fn unlink_at(dir: &File, name: &OsStr, folder: bool) -> std::io::Result<()> {
    let name = c_name(name)?;
    let flags = if folder { libc::AT_REMOVEDIR } else { 0 };
    // SAFETY: as above. A folder is removed only when empty.
    if unsafe { libc::unlinkat(dir.as_raw_fd(), name.as_ptr(), flags) } != 0 { last_error() } else { Ok(()) }
}
fn is_dir(st: &libc::stat) -> bool {
    st.st_mode & libc::S_IFMT == libc::S_IFDIR
}
fn is_link(st: &libc::stat) -> bool {
    st.st_mode & libc::S_IFMT == libc::S_IFLNK
}
fn is_file(st: &libc::stat) -> bool {
    st.st_mode & libc::S_IFMT == libc::S_IFREG
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
    /// Adds folders no cleaning may remove, by identity following links.
    fn protect(&mut self, paths: &[PathBuf]) -> Result<(), String> {
        for path in paths {
            match std::fs::metadata(path) {
                Ok(meta) => self.protected_ids.push((meta.dev(), meta.ino())),
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
                Err(e) => return Err(format!("{} could not be examined ({e})", path.display())),
            }
            self.protected.push(path.clone());
        }
        Ok(())
    }
    #[cfg(test)]
    fn protecting(mut self, paths: &[PathBuf]) -> WorkingFiles {
        self.protect(paths).unwrap();
        self
    }
    /// The protected identities now: those taken when established, and each
    /// protected folder's as it is found now, following links. A protected
    /// folder that cannot be examined stops the cleaning.
    fn protected_now(&self) -> Result<Vec<Id>, String> {
        let mut ids = self.protected_ids.clone();
        for path in &self.protected {
            match std::fs::metadata(path) {
                Ok(meta) => ids.push((meta.dev(), meta.ino())),
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
                Err(e) => return Err(format!("{} could not be examined ({e}), so nothing was removed", path.display())),
            }
        }
        Ok(ids)
    }
    /// `kind`'s subtree, opened through the Working Files folder, each with no
    /// link followed and each the folder established.
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
    /// The record of the subtree: `Ok(empty)` when there is none yet, `Err`
    /// when it cannot be read, is not a regular file, or does not parse.
    fn read_record_in(subtree: &File, path: &Path) -> Result<Vec<(String, Stamp)>, String> {
        use std::io::Read;
        let name = c_name(OsStr::new(RECORD)).map_err(|e| e.to_string())?;
        // SAFETY: as in the descriptor steps; a link in the record's place is refused (ELOOP).
        let fd = unsafe { libc::openat(subtree.as_raw_fd(), name.as_ptr(), libc::O_RDONLY | libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK) };
        if fd < 0 {
            let e = std::io::Error::last_os_error();
            return if e.kind() == std::io::ErrorKind::NotFound { Ok(Vec::new()) } else { Err(format!("the record {} could not be read ({e})", path.display())) };
        }
        let mut file = unsafe { File::from_raw_fd(fd) };
        match stat_of(&file) {
            // One name only: a record that is also another file's name is not read.
            Ok(st) if is_file(&st) && st.st_uid == euid() && st.st_nlink == 1 => {}
            _ => return Err(format!("the record {} is not a file Chirality wrote", path.display())),
        }
        let mut bytes = Vec::new();
        file.read_to_end(&mut bytes).map_err(|e| format!("the record {} could not be read ({e})", path.display()))?;
        let value: serde_json::Value = serde_json::from_slice(&bytes).map_err(|_| format!("the record {} does not parse", path.display()))?;
        value.get("made").and_then(serde_json::Value::as_array)
            .ok_or_else(|| format!("the record {} does not parse", path.display()))?
            .iter()
            .map(|entry| Stamp::from_json(entry).ok_or_else(|| format!("the record {} does not parse", path.display())))
            .collect()
    }
    #[cfg(test)]
    fn read_record(&self, kind: Kind) -> Result<Vec<(String, Stamp)>, String> {
        Self::read_record_in(&self.open_subtree(kind)?, &self.subtree(kind).join(RECORD))
    }
    /// Writes the subtree's record whole to a new file and renames it into place.
    fn write_record_in(subtree: &File, path: &Path, made: &[(String, Stamp)]) -> Result<(), String> {
        use std::io::Write;
        let failed = |e: std::io::Error| format!("the record in {} could not be written: {e}", path.display());
        let bytes = serde_json::to_vec(&serde_json::json!({"made": made.iter().map(|(name, stamp)| stamp.to_json(name)).collect::<Vec<_>>()}))
            .map_err(|e| e.to_string())?;
        let temporary = OsString::from(format!("{RECORD}.{}", crate::util::opaque_id("new-")?));
        let c_temporary = c_name(&temporary).map_err(failed)?;
        // SAFETY: as in the descriptor steps; made new, never through a link.
        let fd = unsafe { libc::openat(subtree.as_raw_fd(), c_temporary.as_ptr(), libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC, 0o600 as libc::c_uint) };
        if fd < 0 {
            return Err(failed(std::io::Error::last_os_error()));
        }
        let mut file = unsafe { File::from_raw_fd(fd) };
        if let Err(e) = file.write_all(&bytes).and_then(|()| file.sync_all()) {
            let _ = unlink_at(subtree, &temporary, false);
            return Err(failed(e));
        }
        let record = c_name(OsStr::new(RECORD)).map_err(failed)?;
        // SAFETY: both names are entries of the same subtree descriptor.
        if unsafe { libc::renameat(subtree.as_raw_fd(), c_temporary.as_ptr(), subtree.as_raw_fd(), record.as_ptr()) } != 0 {
            let e = std::io::Error::last_os_error();
            let _ = unlink_at(subtree, &temporary, false);
            return Err(failed(e));
        }
        subtree.sync_all().map_err(failed)
    }
    #[cfg(test)]
    fn write_record(&self, kind: Kind, made: &[(String, Stamp)]) -> Result<(), String> {
        Self::write_record_in(&self.open_subtree(kind)?, &self.subtree(kind).join(RECORD), made)
    }
    /// Makes a new folder of `kind`, exclusively and private (0700), in the
    /// subtree as established, and records its identity before it is returned
    /// for use.
    pub fn allocate(&self, kind: Kind) -> Result<Made, String> {
        let _records = records_lock();
        let subtree = self.open_subtree(kind)?;
        let record_path = self.subtree(kind).join(RECORD);
        let mut record = Self::read_record_in(&subtree, &record_path).map_err(|why| format!("Chirality could not make a working folder: {why}; nothing was made."))?;
        let name = crate::util::opaque_id(kind.prefix())?;
        let path = self.subtree(kind).join(&name);
        let c = c_name(OsStr::new(&name)).map_err(|e| e.to_string())?;
        // SAFETY: as in the descriptor steps; fails if anything has the name.
        if unsafe { libc::mkdirat(subtree.as_raw_fd(), c.as_ptr(), 0o700) } != 0 {
            return Err(format!("Chirality could not make the working folder {}: {}", path.display(), std::io::Error::last_os_error()));
        }
        let unexamined = || format!("Chirality could not examine the working folder it made at {}; it was kept and is not used", path.display());
        let folder = open_dir_at(&subtree, OsStr::new(&name)).map_err(|_| unexamined())?;
        let st = stat_of(&folder).map_err(|_| unexamined())?;
        let empty = crate::workflow_workspace::names_in(&folder).map(|n| n.is_empty()).unwrap_or(false);
        if st.st_uid != euid() || st.st_mode & 0o077 != 0 || !empty {
            return Err(unexamined());
        }
        let stamp = Stamp::of_stat(&st);
        record.push((name.clone(), stamp));
        if let Err(why) = Self::write_record_in(&subtree, &record_path, &record) {
            // Not recorded, so never used; it is left empty and reported at the next start.
            return Err(format!("Chirality could not make a working folder: {why}; nothing was made."));
        }
        let made = Made { path, kind, name, stamp, folder: std::sync::Arc::new(folder) };
        self.held.lock().unwrap_or_else(|e| e.into_inner()).push(made.clone());
        Ok(made)
    }
    /// Removes what is in a folder this launch made and still holds, through
    /// its held descriptor; the folder itself is kept. Nothing is removed from
    /// a folder this value did not make.
    pub fn empty(&self, made: &Made) -> Cleaning {
        let mut cleaning = Cleaning::default();
        let held = {
            let mut held = self.held.lock().unwrap_or_else(|e| e.into_inner());
            let at = held.iter().position(|h| std::sync::Arc::ptr_eq(&h.folder, &made.folder));
            at.map(|at| held.remove(at))
        };
        let Some(held) = held else {
            cleaning.kept.push((made.path.clone(), "this launch does not hold it, so nothing in it was removed".into()));
            return cleaning;
        };
        let outcome = self.protected_now().and_then(|protected| {
            walk(&held.folder, held.stamp, &protected, false)?;
            walk(&held.folder, held.stamp, &protected, true).map_err(|why| format!("{why}; part of what it held may have been removed before that was found"))
        });
        match outcome {
            Ok(()) => cleaning.removed.push(held.path.clone()),
            Err(why) => cleaning.kept.push((held.path.clone(), why)),
        }
        cleaning
    }
    /// Empties every folder this launch made and still holds.
    pub fn empty_all(&self) -> Cleaning {
        let held: Vec<Made> = self.held.lock().unwrap_or_else(|e| e.into_inner()).clone();
        let mut cleaning = Cleaning::default();
        for made in held {
            let one = self.empty(&made);
            cleaning.removed.extend(one.removed);
            cleaning.kept.extend(one.kept);
        }
        cleaning
    }
    /// What is in the subtrees beside the records: the folders this and
    /// earlier launches made, which this version keeps. Reported, never removed.
    pub fn kept_folders(&self) -> Vec<PathBuf> {
        let mut kept = Vec::new();
        for kind in Kind::ALL {
            let Ok(subtree) = self.open_subtree(kind) else { continue };
            for entry in crate::workflow_workspace::names_in(&subtree).unwrap_or_default() {
                let name = entry.to_string_lossy();
                if name != RECORD && !name.starts_with(&format!("{RECORD}.")) {
                    kept.push(self.subtree(kind).join(&entry));
                }
            }
        }
        kept
    }
}

/// Everything beneath the opened `folder`, made at `made`: checked, or (with
/// `remove`) checked again folder by folder and removed. Nothing is opened but
/// folders, from their parent's descriptor with no link followed; no file is
/// opened and nothing in a file is read.
fn walk(folder: &File, made: Stamp, protected: &[Id], remove: bool) -> Result<(), String> {
    let here = stat_of(folder).map_err(|e| format!("what it holds could not be examined ({e})"))?;
    if protected.contains(&id_of(&here)) {
        return Err("it is, or contains, a folder Chirality protects (its data folder or the person's own Codex home)".into());
    }
    let names = crate::workflow_workspace::names_in(folder).map_err(|e| format!("what it holds could not be examined ({e})"))?;
    let mut entries = Vec::with_capacity(names.len());
    for name in names {
        if CODEX_HOME_FILES.iter().any(|n| OsStr::new(n) == name) {
            return Err(format!("it holds an entry named {}, as Codex names a file in its home; nothing in it was read", name.to_string_lossy()));
        }
        let st = stat_at(folder, &name).map_err(|e| format!("what it holds could not be examined ({e})"))?;
        if is_dir(&st) && protected.contains(&id_of(&st)) {
            return Err("it is, or contains, a folder Chirality protects (its data folder or the person's own Codex home)".into());
        }
        // Another device beneath it is a volume mounted there, whose writer is not this
        // folder's: kept.
        if st.st_dev as u64 != made.dev {
            return Err(format!("it holds {}, which is on another volume, so kept", name.to_string_lossy()));
        }
        // A folder, or a file with a single name, made before this folder was
        // moved in from elsewhere. A link, or a file with other names, loses
        // nothing when this name of it goes.
        let moved_in = !is_link(&st) && (is_dir(&st) || st.st_nlink == 1) && Stamp::of_stat(&st).made_before(made);
        if moved_in {
            return Err(format!("it holds {}, made before this folder was: moved in from elsewhere, so kept", name.to_string_lossy()));
        }
        entries.push((name, is_dir(&st)));
    }
    for (name, folder_entry) in entries {
        if folder_entry {
            let child = open_dir_at(folder, &name).map_err(|e| format!("what it holds could not be opened ({e})"))?;
            walk(&child, made, protected, remove)?;
        }
        if remove {
            unlink_at(folder, &name, folder_entry).map_err(|e| format!("{} could not be removed ({e})", name.to_string_lossy()))?;
        }
    }
    Ok(())
}

/// The Working Files of the App data folder this launch holds, established
/// once at its first use, which also reports the folders earlier launches
/// left.
static LAUNCH: std::sync::Mutex<Option<(PathBuf, WorkingFiles)>> = std::sync::Mutex::new(None);
fn report(cleaning: &Cleaning) {
    for (path, why) in &cleaning.kept {
        eprintln!("chirality: a working folder was kept: {} ({why})", path.display());
    }
}
/// The Working Files of `app_data` for this launch.
pub fn for_launch(app_data: &Path) -> Result<WorkingFiles, String> {
    let mut launch = LAUNCH.lock().unwrap_or_else(|e| e.into_inner());
    if let Some((data, working)) = launch.as_ref() {
        if data == app_data {
            return Ok(working.clone());
        }
    }
    let working = establish(app_data)?;
    if launch.is_none() {
        let kept = working.kept_folders();
        if !kept.is_empty() {
            eprintln!("chirality: {} working folder(s) from earlier starts are kept in {} (this version empties the folders a launch makes at its exit, and removes none); they can be removed while Chirality is not running", kept.len(), working.root().display());
        }
    }
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
/// At the App's exit: empties the folders this launch made and still holds.
pub fn clean_at_exit() {
    let launch = LAUNCH.lock().unwrap_or_else(|e| e.into_inner()).clone();
    if let Some((_, working)) = launch {
        report(&working.empty_all());
    }
}

#[cfg(test)]
#[path = "working_files_tests.rs"]
mod tests;
