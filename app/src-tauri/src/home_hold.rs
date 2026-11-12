//! One App at a time on each Codex home (DEL-01-01, DEL-01-05).
//!
//! A home is held by an exclusive `flock` on the home directory's own inode:
//! no file is created, renamed or left inside the home. `flock` conflicts
//! between two open file descriptions even inside one process, so this
//! process keeps exactly one locked descriptor per home and shares it between
//! the two roles that hold a home: the saved desktop route's receiving
//! source ([`Role::Receiving`]) and the Host that starts Codex on it
//! ([`Role::Host`]). Each role admits one holder. Another process gets
//! `EWOULDBLOCK` and is refused; a lock that could not be taken for any other
//! reason also refuses, never reads as free. A home that does not exist is
//! refused before anything is started: the hold is always on the actual
//! existing directory, and a process is handed the home's path only while
//! that path still names the held directory ([`still_names`]).
//!
//! A Host's hold lasts while the Host lives, and past it while a process
//! group it started has not settled ([`keep_until_settled`]). Inside one
//! process a later Host may take the home over only from a Host that is
//! certainly idle: no child that may still be alive and no start under way.
//! A holder whose state cannot be read, or that is gone while its hold is
//! kept, is busy. The kernel releases the lock when the process ends, however
//! it ends.
use std::{
    collections::HashMap,
    fs::{File, OpenOptions},
    os::{
        fd::AsRawFd,
        unix::fs::{MetadataExt, OpenOptionsExt},
    },
    path::Path,
    sync::{
        atomic::{AtomicUsize, Ordering},
        Arc, Mutex, OnceLock, Weak,
    },
};

/// What a person is told when another App holds the home.
pub(crate) const IN_USE: &str = "Chirality is already running with this Codex home: another Chirality App is using it. Codex was not started on this home. Use the Chirality window that is already open, or quit that App first and then start again.";
/// What a person is told when the home's path no longer names the directory
/// this App holds.
pub(crate) const REPLACED: &str = "The Codex home was replaced after this App took it, so Codex was not started on it. Start again to use the home that is there now.";
/// What a person is told when the Codex home does not exist.
pub(crate) const MISSING: &str = "The Codex home does not exist, so Codex was not started on it.";

/// A held home directory's identity: (device, inode).
pub(crate) type Identity = (u64, u64);

/// Whether the holder of a home role may still have a Codex child on it.
pub(crate) trait HoldOwner: Send + Sync {
    /// `true` unless the holder is certainly idle. A holder whose state cannot
    /// be read at once answers `true`.
    fn may_have_child(&self) -> bool;
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Role {
    Receiving,
    Host,
}

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
enum Key {
    /// An existing home directory (device, inode).
    Inode(u64, u64),
}

struct HostSlot {
    id: usize,
    owner: Weak<dyn HoldOwner>,
    starting: Arc<AtomicUsize>,
}
struct Entry {
    /// The one locked descriptor of this home in this process.
    file: Option<File>,
    receiving: bool,
    host: Option<HostSlot>,
}
impl Drop for Entry {
    fn drop(&mut self) {
        if let Some(file) = &self.file {
            unsafe {
                libc::flock(file.as_raw_fd(), libc::LOCK_UN);
            }
        }
    }
}

fn registry() -> &'static Mutex<HashMap<Key, Entry>> {
    static REGISTRY: OnceLock<Mutex<HashMap<Key, Entry>>> = OnceLock::new();
    REGISTRY.get_or_init(|| Mutex::new(HashMap::new()))
}

/// A held role on a home. Dropping it releases that role; the home's lock is
/// released when no role holds it.
pub(crate) struct HomeHold {
    key: Key,
    role: Role,
    id: usize,
}
impl std::fmt::Debug for HomeHold {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("HomeHold").field("role", &self.role).finish()
    }
}
impl Drop for HomeHold {
    fn drop(&mut self) {
        let mut registry = registry().lock().unwrap_or_else(|e| e.into_inner());
        let Some(entry) = registry.get_mut(&self.key) else {
            return;
        };
        match self.role {
            Role::Receiving => entry.receiving = false,
            // A home taken over by a later Host is no longer this one's to release.
            Role::Host => {
                if entry.host.as_ref().is_some_and(|slot| slot.id == self.id) {
                    entry.host = None;
                }
            }
        }
        if !entry.receiving && entry.host.is_none() {
            registry.remove(&self.key);
        }
    }
}

/// A start in progress on a held home: while it lives the home cannot be
/// taken over in this process.
pub(crate) struct StartClaim(Arc<AtomicUsize>);
impl Drop for StartClaim {
    fn drop(&mut self) {
        self.0.fetch_sub(1, Ordering::SeqCst);
    }
}

fn os_lock(file: &File) -> Result<File, std::io::Error> {
    // A duplicate shares the open file description, so the lock taken here
    // is the one every role of this process holds.
    let held = file.try_clone()?;
    if unsafe { libc::flock(held.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } != 0 {
        return Err(std::io::Error::last_os_error());
    }
    Ok(held)
}

fn would_block(error: &std::io::Error) -> bool {
    matches!(error.raw_os_error(), Some(code) if code == libc::EWOULDBLOCK || code == libc::EAGAIN)
}

fn inode_key(file: &File) -> Result<Key, String> {
    let meta = file
        .metadata()
        .map_err(|e| format!("Codex home could not be checked: {e}"))?;
    if !meta.is_dir() {
        return Err("Codex home is not a directory".into());
    }
    Ok(Key::Inode(meta.dev(), meta.ino()))
}

/// The receiving role on an account home already opened (O_DIRECTORY) by the
/// saved desktop route.
pub(crate) fn hold_receiving(home: &File) -> Result<HomeHold, String> {
    let key = inode_key(home)?;
    let mut registry = registry().lock().unwrap_or_else(|e| e.into_inner());
    match registry.get_mut(&key) {
        Some(entry) if entry.receiving => {
            return Err("account home already has a participating owner in this App (no wait)".into())
        }
        Some(entry) => entry.receiving = true,
        None => {
            let file = os_lock(home).map_err(|e| {
                format!("account home already has a participating owner or custody is unavailable (no wait): {e}")
            })?;
            registry.insert(
                key.clone(),
                Entry {
                    file: Some(file),
                    receiving: true,
                    host: None,
                },
            );
        }
    }
    Ok(HomeHold {
        key,
        role: Role::Receiving,
        id: 0,
    })
}

/// The Host role on `home` for the Host `id`, a claim for its start, and the
/// identity of the held directory. Returns a new hold when the Host did not
/// already hold the home. A home that does not exist, or that could not be
/// checked, is refused.
pub(crate) fn claim_host(
    home: &Path,
    id: usize,
    owner: Weak<dyn HoldOwner>,
    starting: &Arc<AtomicUsize>,
) -> Result<(Option<HomeHold>, StartClaim, Identity), String> {
    let opened = OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_DIRECTORY | libc::O_NONBLOCK | libc::O_CLOEXEC)
        .open(home);
    let file = match opened {
        Ok(file) => file,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Err(MISSING.into()),
        Err(e) => return Err(format!("Codex home could not be checked, so Codex was not started: {e}")),
    };
    let key = inode_key(&file)?;
    let Key::Inode(dev, ino) = key;
    let mut registry = registry().lock().unwrap_or_else(|e| e.into_inner());
    let claim = |starting: &Arc<AtomicUsize>| {
        starting.fetch_add(1, Ordering::SeqCst);
        StartClaim(Arc::clone(starting))
    };
    if let Some(entry) = registry.get_mut(&key) {
        if let Some(slot) = &entry.host {
            if slot.id == id {
                return Ok((None, claim(starting), (dev, ino)));
            }
            // A holder that is gone while its hold is kept (its processes
            // have not settled), or whose state cannot be read, is busy.
            let busy = slot.starting.load(Ordering::SeqCst) > 0
                || slot.owner.upgrade().map_or(true, |owner| owner.may_have_child());
            if busy {
                return Err("Codex is already started on this home by this App; a second Codex was not started on it".into());
            }
        }
        entry.host = Some(HostSlot {
            id,
            owner,
            starting: Arc::clone(starting),
        });
    } else {
        let locked = os_lock(&file).map_err(|e| {
            if would_block(&e) {
                IN_USE.to_string()
            } else {
                format!("Codex home hold could not be taken, so Codex was not started: {e}")
            }
        })?;
        registry.insert(
            key.clone(),
            Entry {
                file: Some(locked),
                receiving: false,
                host: Some(HostSlot {
                    id,
                    owner,
                    starting: Arc::clone(starting),
                }),
            },
        );
    }
    Ok((
        Some(HomeHold {
            key,
            role: Role::Host,
            id,
        }),
        claim(starting),
        (dev, ino),
    ))
}

/// `Ok` only while `home` names the directory whose identity is `held`; a
/// path that names another directory, or none, or that cannot be checked is
/// refused.
pub(crate) fn still_names(home: &Path, held: Identity) -> Result<(), String> {
    match std::fs::metadata(home) {
        Ok(meta) if meta.is_dir() && (meta.dev(), meta.ino()) == held => Ok(()),
        Ok(_) => Err(REPLACED.into()),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Err(REPLACED.into()),
        Err(e) => Err(format!("Codex home could not be checked, so Codex was not started on it: {e}")),
    }
}

/// What a Host leaves when it goes: its home holds and its session's
/// liveness lock stay held until every process group it started has
/// settled ([`crate::hosting::process_group_custody::OwnedProcess::settled`]: its
/// leader's exit observed and its group known empty). Each unsettled group is
/// given its retirement monitor, which establishes settlement. A group whose
/// settlement can no longer be established (its reservation was released
/// without a known-empty observation), or a keeper that cannot be started,
/// keeps the holds for the life of the process; the kernel releases them when
/// the process ends.
pub(crate) fn keep_until_settled(
    holds: Vec<HomeHold>,
    liveness: Option<Arc<crate::session_liveness::Hold>>,
    processes: Vec<Arc<crate::hosting::process_group_custody::OwnedProcess>>,
) {
    let pending: Vec<_> = processes.into_iter().filter(|p| !p.settled()).collect();
    if pending.is_empty() || (holds.is_empty() && liveness.is_none()) {
        return;
    }
    for process in &pending {
        process.maintain();
    }
    let kept = Arc::new(Mutex::new(Some((holds, liveness))));
    let keeper = Arc::clone(&kept);
    let started = std::thread::Builder::new().name("home-hold-settlement".into()).spawn(move || loop {
        if pending.iter().all(|p| p.settled()) {
            drop(keeper.lock().unwrap_or_else(|e| e.into_inner()).take());
            return;
        }
        if pending.iter().any(|p| p.released() && !p.settled()) {
            std::mem::forget(keeper.lock().unwrap_or_else(|e| e.into_inner()).take());
            return;
        }
        std::thread::sleep(std::time::Duration::from_millis(25));
    });
    if started.is_err() {
        std::mem::forget(kept.lock().unwrap_or_else(|e| e.into_inner()).take());
    }
}

/// A fresh identity for a Host's role.
pub(crate) fn next_id() -> usize {
    static NEXT: AtomicUsize = AtomicUsize::new(1);
    NEXT.fetch_add(1, Ordering::SeqCst)
}

#[cfg(test)]
#[path = "home_hold_tests.rs"]
mod tests;
