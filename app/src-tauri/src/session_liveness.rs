//! Whether an App session recorded in the App ledger is still running
//! (DEL-01-02).
//!
//! Each App session of this build holds an exclusive `flock` on its own lock
//! file for as long as its Host (and any process group it started that has
//! not settled) lives, taken before its `session_started` entry is written.
//! The file lives in the directory beside the ledger (`<ledger>.sessions/`),
//! named by the SHA-256 of the full session identity, and holds that identity
//! as text. The kernel releases the lock when the process ends, however it
//! ends; the file stays. Its `session_started` entry says so: it carries
//! [`FIELD`] (`"livenessLock": true`).
//!
//! A later session's startup reads each earlier session that has no recorded
//! end (no `session_ended` entry and no later `session_started` naming it as
//! its previous session):
//! - [`Liveness::Held`]: the session is alive. Nothing is inferred about it.
//! - [`Liveness::Unknown`]: the check could not be made, or what was found
//!   does not show that the session ended. Read as not ended.
//! - [`Liveness::Free`]: a lock file that names the session and whose holder
//!   has gone. Ended without a record.
//! - [`Liveness::Absent`]: no lock file, for a session whose `session_started`
//!   does not carry [`FIELD`] (recorded by a build that took no lock). Keeps
//!   the reading that build had: ended without a record.
//!
//! For a session that carries [`FIELD`], a missing file, one that is not a
//! regular file, one owned by another user, one that could not be opened,
//! read or checked, and one whose text is not that session's identity read as
//! [`Liveness::Unknown`], never as ended. [`resolve_not_known`] states the only
//! evidence that settles such a session as ended without a record.
//!
//! A lock file is removed only by a later session start ([`sweep`]), only
//! after the ledger records that session's end, and only while it is free and
//! still names that session; so the reading of a session whose end is not
//! recorded never rests on its file having been kept or swept.
use std::{
    collections::{BTreeSet, HashMap},
    ffi::CString,
    fs::{File, OpenOptions},
    io::{Read, Write},
    os::{
        fd::{AsRawFd, FromRawFd},
        unix::fs::{DirBuilderExt, MetadataExt, OpenOptionsExt},
    },
    path::{Path, PathBuf},
    sync::{Mutex, OnceLock},
};

/// The additive `session_started` field (ledger schema 0.5) by which a
/// session says it took a liveness lock.
pub(crate) const FIELD: &str = "livenessLock";

/// The liveness directory of the ledger at `ledger` (the ledger's configured
/// path, beside its database).
pub(crate) fn directory(ledger: &Path) -> PathBuf {
    ledger.with_extension("sessions")
}
fn file_name(session: &str) -> String {
    format!("{}.lock", crate::util::sha256_hex(session.as_bytes()))
}
/// The lock file of `session` on the ledger at `ledger`.
pub(crate) fn lock_path(ledger: &Path, session: &str) -> PathBuf {
    directory(ledger).join(file_name(session))
}

fn would_block(error: &std::io::Error) -> bool {
    matches!(error.raw_os_error(), Some(code) if code == libc::EWOULDBLOCK || code == libc::EAGAIN)
}
fn same_object(file: &File, path: &Path) -> bool {
    match (file.metadata(), std::fs::symlink_metadata(path)) {
        (Ok(held), Ok(named)) => named.is_file() && held.dev() == named.dev() && held.ino() == named.ino(),
        _ => false,
    }
}
fn euid() -> u32 {
    unsafe { libc::geteuid() }
}

/// Sessions whose liveness lock is held by a [`Hold`] alive in this process
/// (counted: a session's hold is taken once, but this is not relied on).
fn live_here() -> &'static Mutex<HashMap<String, usize>> {
    static LIVE: OnceLock<Mutex<HashMap<String, usize>>> = OnceLock::new();
    LIVE.get_or_init(|| Mutex::new(HashMap::new()))
}
fn note_live(session: &str) {
    *live_here().lock().unwrap_or_else(|e| e.into_inner()).entry(session.to_owned()).or_default() += 1;
}
fn note_gone(session: &str) {
    let mut live = live_here().lock().unwrap_or_else(|e| e.into_inner());
    if let Some(count) = live.get_mut(session) {
        *count -= 1;
        if *count == 0 {
            live.remove(session);
        }
    }
}

/// This session's held liveness lock. Dropping it releases the lock and keeps
/// the file, as the end of the process does.
pub(crate) struct Hold {
    file: Mutex<Option<File>>,
    path: PathBuf,
    session: String,
}
impl std::fmt::Debug for Hold {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Hold").field("path", &self.path).finish()
    }
}
impl Hold {
    pub(crate) fn acquire(ledger: &Path, session: &str) -> Result<Self, String> {
        if session.is_empty() {
            return Err("App session identity is empty; no liveness lock".into());
        }
        let dir = directory(ledger);
        match std::fs::DirBuilder::new().mode(0o700).create(&dir) {
            Ok(()) => {
                if let Some(parent) = dir.parent() {
                    let _ = File::open(parent).and_then(|f| f.sync_all());
                }
            }
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(e) => return Err(format!("App session liveness lock unavailable: {e}")),
        }
        // As strict as the ledger beside it: the directory itself is no link
        // and the lock file is opened without following one.
        let meta = std::fs::symlink_metadata(&dir)
            .map_err(|e| format!("App session liveness directory unavailable: {e}"))?;
        if !meta.is_dir() || meta.uid() != euid() {
            return Err("App session liveness location is not a directory owned by this user".into());
        }
        let path = dir.join(file_name(session));
        // A later startup may remove a free file between this open and the
        // lock; the lock is kept only on the file the path still names.
        for _ in 0..50 {
            let file = OpenOptions::new()
                .read(true)
                .write(true)
                .create(true)
                .mode(0o600)
                .custom_flags(libc::O_NOFOLLOW | libc::O_CLOEXEC)
                .open(&path)
                .map_err(|e| format!("App session liveness lock unavailable: {e}"))?;
            if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } != 0 {
                let error = std::io::Error::last_os_error();
                if would_block(&error) {
                    std::thread::sleep(std::time::Duration::from_millis(10));
                    continue;
                }
                return Err(format!("App session liveness lock unavailable: {error}"));
            }
            if !same_object(&file, &path) {
                continue;
            }
            // The identity and the file's directory entry are on disk before
            // the session_started entry that says this lock was taken.
            let mut writer = &file;
            file.set_len(0)
                .and_then(|_| writer.write_all(session.as_bytes()))
                .and_then(|_| file.sync_all())
                .and_then(|_| File::open(&dir).and_then(|d| d.sync_all()))
                .map_err(|e| format!("App session liveness lock not written: {e}"))?;
            note_live(session);
            return Ok(Self { file: Mutex::new(Some(file)), path, session: session.to_owned() });
        }
        Err("App session liveness lock could not be taken (the lock file kept changing or stayed held)".into())
    }
    pub(crate) fn path(&self) -> &Path {
        &self.path
    }
    pub(crate) fn session(&self) -> &str {
        &self.session
    }
    fn release(&self) {
        if let Some(file) = self.file.lock().unwrap_or_else(|e| e.into_inner()).take() {
            unsafe {
                libc::flock(file.as_raw_fd(), libc::LOCK_UN);
            }
            note_gone(&self.session);
        }
    }
    /// What the end of a killed process leaves: the file stays, its lock is
    /// free, and no hold of this session is alive in the process.
    #[cfg(test)]
    pub(crate) fn release_as_if_killed(&self) {
        self.release();
    }
}
impl Drop for Hold {
    fn drop(&mut self) {
        self.release();
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum Liveness {
    Absent,
    Free,
    Held,
    Unknown(String),
}
impl Liveness {
    /// Whether the session may be treated as ended without a record.
    pub(crate) fn ended(&self) -> bool {
        matches!(self, Self::Absent | Self::Free)
    }
}

/// Reads whether `session` holds its lock. Never creates anything.
/// `declared`: the session's `session_started` carries [`FIELD`], so it took
/// a lock here, and only a file that names it and is free shows it ended.
pub(crate) fn probe(ledger: &Path, session: &str, declared: bool) -> Liveness {
    let path = lock_path(ledger, session);
    let file = match OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK)
        .open(&path)
    {
        Ok(file) => file,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            return if declared {
                Liveness::Unknown(format!("{} is missing, though that session took its lock there", path.display()))
            } else {
                Liveness::Absent
            };
        }
        Err(e) => return Liveness::Unknown(format!("{} could not be opened: {e}", path.display())),
    };
    match file.metadata() {
        Ok(meta) if !meta.is_file() => return Liveness::Unknown(format!("{} is not a regular file", path.display())),
        Ok(meta) if declared && meta.uid() != euid() => {
            return Liveness::Unknown(format!("{} belongs to another user", path.display()))
        }
        Ok(_) => {}
        Err(e) => return Liveness::Unknown(format!("{} could not be read: {e}", path.display())),
    }
    if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_SH | libc::LOCK_NB) } != 0 {
        let error = std::io::Error::last_os_error();
        return if would_block(&error) {
            Liveness::Held
        } else {
            Liveness::Unknown(format!("{} could not be checked: {error}", path.display()))
        };
    }
    // Free. For a session that took its lock here, the file must name it.
    let named = if declared {
        let mut text = Vec::new();
        match (&file).take(session.len() as u64 + 1).read_to_end(&mut text) {
            Ok(_) if text == session.as_bytes() => Ok(()),
            Ok(_) => Err(format!("{} does not name this session", path.display())),
            Err(e) => Err(format!("{} could not be read: {e}", path.display())),
        }
    } else {
        Ok(())
    };
    unsafe {
        libc::flock(file.as_raw_fd(), libc::LOCK_UN);
    }
    match named {
        Ok(()) => Liveness::Free,
        Err(reason) => Liveness::Unknown(reason),
    }
}

/// Removes the lock files of the sessions in `ended`, whose end the ledger
/// records. A file is removed only while this process holds its lock, the
/// path still names it and it names its session, so a live holder's file and
/// a file this process cannot account for are never removed.
pub(crate) fn sweep(ledger: &Path, ended: &BTreeSet<&str>) {
    let Ok(entries) = std::fs::read_dir(directory(ledger)) else {
        return;
    };
    let names: HashMap<String, &str> = ended.iter().map(|session| (file_name(session), *session)).collect();
    for entry in entries.flatten() {
        let name = entry.file_name();
        let Some(session) = name.to_str().and_then(|name| names.get(name)) else { continue };
        let path = entry.path();
        let Ok(file) = OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK)
            .open(&path)
        else {
            continue;
        };
        if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } != 0 {
            continue;
        }
        let mut text = Vec::new();
        let names_it = (&file).take(session.len() as u64 + 1).read_to_end(&mut text).is_ok() && text == session.as_bytes();
        if names_it && same_object(&file, &path) {
            let _ = std::fs::remove_file(&path);
        }
        unsafe {
            libc::flock(file.as_raw_fd(), libc::LOCK_UN);
        }
    }
}

/// App data directories this process holds an exclusive lock on, each by the
/// identity of the held descriptor (device, inode).
fn held_app_data() -> &'static Mutex<Vec<(usize, File)>> {
    static HELD: OnceLock<Mutex<Vec<(usize, File)>>> = OnceLock::new();
    HELD.get_or_init(|| Mutex::new(Vec::new()))
}
/// The registration of an App data directory this process holds. The holder
/// creates it only after its exclusive lock was taken, and drops it before or
/// as it releases that lock.
pub(crate) struct AppDataHeld(usize);
impl Drop for AppDataHeld {
    fn drop(&mut self) {
        held_app_data().lock().unwrap_or_else(|e| e.into_inner()).retain(|(id, _)| *id != self.0);
    }
}
pub(crate) fn note_app_data_held(locked: &File) -> Result<AppDataHeld, String> {
    static NEXT: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(1);
    let file = locked.try_clone().map_err(|e| format!("App data custody could not be noted: {e}"))?;
    let id = NEXT.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
    held_app_data().lock().unwrap_or_else(|e| e.into_inner()).push((id, file));
    Ok(AppDataHeld(id))
}

fn open_directory_at(parent: Option<&File>, name: &str, path: &Path) -> Result<File, String> {
    let flags = libc::O_RDONLY | libc::O_DIRECTORY | libc::O_CLOEXEC;
    let fd = match parent {
        Some(parent) => {
            let name = CString::new(name).map_err(|e| e.to_string())?;
            unsafe { libc::openat(parent.as_raw_fd(), name.as_ptr(), flags) }
        }
        None => {
            let name = CString::new(path.as_os_str().as_encoded_bytes()).map_err(|e| e.to_string())?;
            unsafe { libc::open(name.as_ptr(), flags) }
        }
    };
    if fd < 0 {
        return Err(std::io::Error::last_os_error().to_string());
    }
    Ok(unsafe { File::from_raw_fd(fd) })
}

/// The positive evidence that settles an earlier session of this build whose
/// liveness is [`Liveness::Unknown`] as ended without a record. Both must hold:
///
/// 1. This process holds the exclusive lock on an App data directory: a
///    descriptor registered by [`note_app_data_held`] after its `flock`
///    (`LOCK_EX`) succeeded, and not yet released.
/// 2. That held directory contains this ledger, established by identity: the
///    directory that contains the ledger is opened, and it and each directory
///    above it (reached through `..` from the opened descriptor, never by path
///    text) is compared by device and inode with the held descriptor, until
///    one matches or the root is reached.
///
/// With both, no other participating App can be alive on this ledger: every
/// App takes that lock before it opens the ledger. A session whose hold is
/// still alive in this process is never settled this way. Without both, the
/// reason is returned and the caller refuses the session start.
pub(crate) fn resolve_not_known(ledger: &Path, session: &str) -> Result<(), String> {
    if live_here().lock().unwrap_or_else(|e| e.into_inner()).contains_key(session) {
        return Err("that session's lock is held in this process".into());
    }
    let held: Vec<(u64, u64)> = {
        let held = held_app_data().lock().unwrap_or_else(|e| e.into_inner());
        held.iter().filter_map(|(_, file)| file.metadata().ok().map(|m| (m.dev(), m.ino()))).collect()
    };
    if held.is_empty() {
        return Err("this App holds no App data directory, so no other App's absence is established".into());
    }
    let parent = ledger.parent().ok_or("the ledger has no containing directory")?;
    let mut current = open_directory_at(None, "", parent)
        .map_err(|e| format!("the ledger's directory could not be opened: {e}"))?;
    for _ in 0..4096 {
        let meta = current.metadata().map_err(|e| format!("the ledger's directory could not be read: {e}"))?;
        let here = (meta.dev(), meta.ino());
        if held.contains(&here) {
            return Ok(());
        }
        let up = open_directory_at(Some(&current), "..", parent)
            .map_err(|e| format!("a directory above the ledger could not be opened: {e}"))?;
        let above = up.metadata().map_err(|e| format!("a directory above the ledger could not be read: {e}"))?;
        if (above.dev(), above.ino()) == here {
            break;
        }
        current = up;
    }
    Err("the App data directory this App holds does not contain this ledger".into())
}

#[cfg(test)]
#[path = "session_liveness_tests.rs"]
mod tests;
