//! Whether an App session recorded in the App ledger is still running
//! (DEL-01-02).
//!
//! Each App session holds an exclusive `flock` on its own lock file for as
//! long as its Host lives (in the App, the life of the process), taken
//! before its `session_started` entry is written. The file lives in the
//! directory beside the ledger (`<ledger>.sessions/`), named by the SHA-256 of
//! the full session identity, so one session's lock cannot stand for another's;
//! it also holds that identity as text. The kernel releases the lock when the
//! process ends, however it ends.
//!
//! A later session's startup reads each earlier session that has no end
//! record:
//! - [`Liveness::Held`]: the session is alive. Nothing is inferred about it.
//! - [`Liveness::Unknown`]: the check could not be made. Read as not ended.
//! - [`Liveness::Free`]: a lock file whose holder has gone. Ended without a record.
//! - [`Liveness::Absent`]: no lock file. Sessions recorded by builds before
//!   locks existed have none, and a relaunch is a new App session whose earlier
//!   processes do not survive, so this keeps today's reading: ended without a
//!   record. A lock file is only removed by its holder as it ends, or by a
//!   later startup while it is free, so absence never hides a live holder that
//!   took its lock here.
use std::{
    fs::{File, OpenOptions},
    io::Write,
    os::{
        fd::AsRawFd,
        unix::fs::{DirBuilderExt, MetadataExt, OpenOptionsExt},
    },
    path::{Path, PathBuf},
};

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

/// This session's held liveness lock. Dropping it removes the file while
/// still holding the lock, then releases it.
pub(crate) struct Hold {
    file: std::sync::Mutex<Option<File>>,
    path: PathBuf,
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
        if !meta.is_dir() || meta.uid() != unsafe { libc::geteuid() } {
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
            let mut writer = &file;
            file.set_len(0)
                .and_then(|_| writer.write_all(session.as_bytes()))
                .map_err(|e| format!("App session liveness lock not written: {e}"))?;
            return Ok(Self { file: std::sync::Mutex::new(Some(file)), path });
        }
        Err("App session liveness lock could not be taken (the lock file kept changing or stayed held)".into())
    }
    pub(crate) fn path(&self) -> &Path {
        &self.path
    }
    /// What a killed process leaves: the file stays, its lock is free.
    #[cfg(test)]
    pub(crate) fn release_as_if_killed(&self) {
        if let Some(file) = self.file.lock().unwrap_or_else(|e| e.into_inner()).take() {
            unsafe {
                libc::flock(file.as_raw_fd(), libc::LOCK_UN);
            }
        }
    }
}
impl Drop for Hold {
    fn drop(&mut self) {
        let Some(file) = self.file.get_mut().unwrap_or_else(|e| e.into_inner()).take() else {
            return;
        };
        if same_object(&file, &self.path) {
            let _ = std::fs::remove_file(&self.path);
        }
        unsafe {
            libc::flock(file.as_raw_fd(), libc::LOCK_UN);
        }
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
pub(crate) fn probe(ledger: &Path, session: &str) -> Liveness {
    let path = lock_path(ledger, session);
    let file = match OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK)
        .open(&path)
    {
        Ok(file) => file,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Liveness::Absent,
        Err(e) => return Liveness::Unknown(format!("{} could not be opened: {e}", path.display())),
    };
    match file.metadata() {
        Ok(meta) if meta.is_file() => {}
        Ok(_) => return Liveness::Unknown(format!("{} is not a regular file", path.display())),
        Err(e) => return Liveness::Unknown(format!("{} could not be read: {e}", path.display())),
    }
    if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_SH | libc::LOCK_NB) } == 0 {
        unsafe {
            libc::flock(file.as_raw_fd(), libc::LOCK_UN);
        }
        return Liveness::Free;
    }
    let error = std::io::Error::last_os_error();
    if would_block(&error) {
        Liveness::Held
    } else {
        Liveness::Unknown(format!("{} could not be checked: {error}", path.display()))
    }
}

/// Removes the lock files no session holds: those of sessions that ended,
/// however they ended. A file is removed only while this process holds its
/// lock and the path still names it, so a live holder's file is never removed.
pub(crate) fn sweep(ledger: &Path) {
    let Ok(entries) = std::fs::read_dir(directory(ledger)) else {
        return;
    };
    for entry in entries.flatten() {
        let name = entry.file_name();
        let Some(name) = name.to_str() else { continue };
        let Some(stem) = name.strip_suffix(".lock") else { continue };
        if stem.len() != 64 || !stem.bytes().all(|b| b.is_ascii_hexdigit()) {
            continue;
        }
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
        if same_object(&file, &path) {
            let _ = std::fs::remove_file(&path);
        }
        unsafe {
            libc::flock(file.as_raw_fd(), libc::LOCK_UN);
        }
    }
}

#[cfg(test)]
#[path = "session_liveness_tests.rs"]
mod tests;
