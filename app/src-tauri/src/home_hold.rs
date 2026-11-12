//! One App at a time on each Codex home (DEL-01-01, DEL-01-05).
//!
//! A home is held by an exclusive `flock` on the home directory's own inode:
//! the hold creates, renames and leaves no file inside the home. (The one
//! file the App does create in a home is its per-start process lock, taken
//! inside the held directory at each start of Codex: [`open_held`],
//! `native_local_provider::take_process_lock_in`.) `flock` conflicts
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
//! A holder whose state cannot be read is busy. A gone holder's kept hold
//! passes only once every process group it started is established settled;
//! each later start attempt on the home retries the settlement monitor of a
//! group whose monitor could not be started, and custody is never released to
//! do so. The kernel releases the lock when the process ends, however it ends.
//!
//! A conflicting lock shows that some process holds the home, not which one:
//! the refusals say what was observed and name no owner.
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

/// What a person is told when another process holds the home.
pub(crate) const IN_USE: &str = "Codex was not started on this home: the home is held by another process on this computer. If another Chirality App is using it, use that App or quit it first.";
/// What a person is told when this App still holds the home because a process
/// group an earlier Host of this App started is not established settled.
pub(crate) const KEPT: &str = "Codex was not started on this home: this App is still holding it because a Codex process it started has not been confirmed ended. Quitting Chirality releases it.";
/// What a person is told when a live Host of this App holds the home and may
/// still have a start or a Codex process on it.
pub(crate) const IN_USE_HERE: &str = "Codex was not started on this home: this App is already using it for another start of Codex, or for a Codex process not yet confirmed ended.";
/// What a person is told when the home's path no longer names the directory
/// this App holds.
pub(crate) const REPLACED: &str = "The Codex home was replaced after this App took it, so Codex was not started on it. Start again to use the home that is there now.";
/// What a person is told when the Codex home does not exist.
pub(crate) const MISSING: &str = "The Codex home does not exist, so Codex was not started on it.";

/// What a person is told when the App's process lock of a home is held and
/// this App knows nothing of the holder. A held lock establishes only that
/// something holds it: the sentence names what may, and asserts neither which
/// nor for how long. (The dedicated local home has its own sentence,
/// `native_local_provider::EARLIER_PROCESS`, with the same clauses; no
/// program of the person's settings is started there.)
pub(crate) const PROCESS_HELD: &str = "The App's lock for this Codex home is held, so Codex was not started there. A Codex process started earlier for that home, or a program it started, may hold it; that program may be one your own Codex settings start, such as a notifier or a hook. Try again in a minute. If it stays held, whatever holds it has to let go of it or end before Codex can start there; the App cannot tell which program it is.";
/// What a person is told when the App could not try its process lock of a
/// home at all. Never read as free.
pub(crate) const PROCESS_LOCK_UNAVAILABLE: &str = "The App could not check its lock for this Codex home, so Codex was not started there.";
/// What a person is told when the App's process lock of a home is held and
/// this App itself started a Codex process there that it has not established
/// ended: what the App knows, and its census of that process's group as just
/// taken. The census covers the original process group only.
pub(crate) fn process_held_here(census: &crate::hosting::process_group_custody::Census) -> String {
    use crate::hosting::process_group_custody::Census;
    let seen = match census {
        Census::Complete(0) => "When checked just now, no process of its group was running, so the holder is outside that group.",
        Census::Complete(_) => "When checked just now, processes of its group were running.",
        Census::Unknown(_) => "Its process group could not be checked.",
    };
    format!("The App's lock for this Codex home is held, so Codex was not started there. This App started a Codex process for that home and has not confirmed that it ended; that process, or a program it started, may hold the lock. {seen} Try again in a minute. If it stays held, whatever holds it has to let go of it or end before Codex can start there.")
}

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
    /// The holds this Host has of the home: one per start call that claimed
    /// it. The slot goes when the last is released.
    count: usize,
    owner: Weak<dyn HoldOwner>,
    starting: Arc<AtomicUsize>,
    /// Set when the owner went while a process group it started had not
    /// settled: what it left, kept until that is established.
    kept: Option<Arc<Kept>>,
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
impl HomeHold {
    /// Whether `other` is a hold of the same role on the same home by the same holder.
    pub(crate) fn same_as(&self, other: &HomeHold) -> bool {
        self.key == other.key && self.role == other.role && self.id == other.id
    }
}
impl std::fmt::Debug for HomeHold {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("HomeHold").field("role", &self.role).finish()
    }
}
impl Drop for HomeHold {
    fn drop(&mut self) {
        // What is taken out of the registry is dropped after its lock is
        // released: a kept slot may own holds whose own drop takes it.
        let (_slot, _entry);
        let mut registry = registry().lock().unwrap_or_else(|e| e.into_inner());
        let Some(entry) = registry.get_mut(&self.key) else {
            return;
        };
        match self.role {
            Role::Receiving => entry.receiving = false,
            // A home taken over by a later Host is no longer this one's to release.
            Role::Host => {
                if let Some(slot) = entry.host.as_mut().filter(|slot| slot.id == self.id) {
                    slot.count -= 1;
                    if slot.count == 0 {
                        _slot = entry.host.take();
                    }
                }
            }
        }
        if !entry.receiving && entry.host.is_none() {
            _entry = registry.remove(&self.key);
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
                if would_block(&e) {
                    IN_USE.to_string()
                } else {
                    format!("Codex home hold could not be taken, so Codex was not started: {e}")
                }
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
/// identity of the held directory. Each call that succeeds has its own hold
/// (a Host that already holds the home gets another, counted), so a call that
/// is later refused can drop its hold without releasing one another call of
/// the same Host relies on. A home that does not exist, or that could not be
/// checked, is refused.
pub(crate) fn claim_host(
    home: &Path,
    id: usize,
    owner: Weak<dyn HoldOwner>,
    starting: &Arc<AtomicUsize>,
) -> Result<(HomeHold, StartClaim, Identity), String> {
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
    // A slot replaced here is dropped, and what a gone holder left released,
    // after the registry's lock is released.
    let mut replaced: Option<HostSlot> = None;
    let mut registry = registry().lock().unwrap_or_else(|e| e.into_inner());
    let claim = |starting: &Arc<AtomicUsize>| {
        starting.fetch_add(1, Ordering::SeqCst);
        StartClaim(Arc::clone(starting))
    };
    if let Some(entry) = registry.get_mut(&key) {
        if let Some(slot) = entry.host.as_mut() {
            if slot.id == id {
                slot.count += 1;
                return Ok((HomeHold { key, role: Role::Host, id }, claim(starting), (dev, ino)));
            }
            if slot.starting.load(Ordering::SeqCst) > 0 {
                return Err(IN_USE_HERE.into());
            }
            match (slot.owner.upgrade(), &slot.kept) {
                // A live holder whose state cannot be read is busy.
                (Some(owner), _) if owner.may_have_child() => return Err(IN_USE_HERE.into()),
                (Some(_), _) => {}
                // A gone holder's hold passes only once what it started is
                // established settled; asking retries a monitor that could
                // not be started.
                (None, Some(kept)) if !kept.settled_now() => return Err(KEPT.into()),
                (None, Some(_)) => {}
                // Gone while its own release is under way.
                (None, None) => return Err(IN_USE_HERE.into()),
            }
        }
        replaced = entry.host.replace(HostSlot {
            id,
            count: 1,
            owner,
            starting: Arc::clone(starting),
            kept: None,
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
                    count: 1,
                    owner,
                    starting: Arc::clone(starting),
                    kept: None,
                }),
            },
        );
    }
    let claimed = claim(starting);
    drop(registry);
    if let Some(kept) = replaced.and_then(|slot| slot.kept) {
        kept.release_if_settled();
    }
    Ok((
        HomeHold {
            key,
            role: Role::Host,
            id,
        },
        claimed,
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

/// Opens `home` and returns the directory only when it is the one whose
/// identity is `held`; a path that names another directory, or none, or that
/// cannot be checked is refused as [`still_names`] refuses it. What is then
/// opened by name inside the returned directory is inside the held home,
/// whatever becomes of the path afterwards.
pub(crate) fn open_held(home: &Path, held: Identity) -> Result<File, String> {
    let opened = OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_DIRECTORY | libc::O_NONBLOCK | libc::O_CLOEXEC)
        .open(home);
    let file = match opened {
        Ok(file) => file,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Err(REPLACED.into()),
        Err(e) => return Err(format!("Codex home could not be checked, so Codex was not started on it: {e}")),
    };
    let meta = file.metadata().map_err(|e| format!("Codex home could not be checked, so Codex was not started on it: {e}"))?;
    if meta.is_dir() && (meta.dev(), meta.ino()) == held { Ok(file) } else { Err(REPLACED.into()) }
}

/// What a gone Host left: its unsettled process groups, and its home holds and
/// session liveness lock, kept until every group is established settled.
pub(crate) struct Kept {
    pending: Vec<Arc<crate::hosting::process_group_custody::OwnedProcess>>,
    holds: Mutex<Option<(Vec<HomeHold>, Option<Arc<crate::session_liveness::Hold>>)>>,
}
impl Kept {
    /// Whether every group is established settled. Each unsettled group is
    /// given its retirement monitor (again, if it could not be started
    /// before), which is what establishes settlement.
    fn settled_now(&self) -> bool {
        let mut settled = true;
        for process in &self.pending {
            if !process.settled() {
                process.maintain();
                settled = false;
            }
        }
        settled
    }
    /// Releases the holds, only once every group is established settled.
    /// Never called under the registry's lock (a hold's release takes it).
    fn release_if_settled(&self) -> bool {
        if !self.settled_now() {
            return false;
        }
        let left = self.holds.lock().unwrap_or_else(|e| e.into_inner()).take();
        drop(left);
        true
    }
    /// A group whose reservation was released without a known-empty
    /// observation: its settlement can no longer be established.
    fn stranded(&self) -> bool {
        self.pending.iter().any(|p| p.released() && !p.settled())
    }
}

/// What a Host leaves when it goes: its home holds and its session's
/// liveness lock stay held until every process group it started has
/// settled ([`crate::hosting::process_group_custody::OwnedProcess::settled`]: its
/// leader's exit observed and its group known empty). Each unsettled group is
/// given its retirement monitor, which establishes settlement, and each home
/// it held names what it left, so that a later start on the home is told why
/// it is refused ([`KEPT`]) and retries a monitor that could not be started.
/// A keeper thread polls and releases the holds once every group is settled.
/// A group whose settlement can no longer be established (its reservation was
/// released without a known-empty observation) keeps the holds for the life
/// of the process; so does a keeper that cannot be started, until a later
/// start attempt on the home finds the groups settled. The kernel releases
/// them when the process ends.
pub(crate) fn keep_until_settled(
    holds: Vec<HomeHold>,
    liveness: Option<Arc<crate::session_liveness::Hold>>,
    processes: Vec<Arc<crate::hosting::process_group_custody::OwnedProcess>>,
) {
    keep(holds, liveness, processes, true)
}
/// [`keep_until_settled`] as it is when neither the groups' retirement
/// monitors nor the keeper thread could be started.
#[cfg(test)]
pub(crate) fn keep_with_no_monitor_or_keeper_for_test(
    holds: Vec<HomeHold>,
    processes: Vec<Arc<crate::hosting::process_group_custody::OwnedProcess>>,
) {
    keep(holds, None, processes, false)
}
fn keep(
    holds: Vec<HomeHold>,
    liveness: Option<Arc<crate::session_liveness::Hold>>,
    processes: Vec<Arc<crate::hosting::process_group_custody::OwnedProcess>>,
    start: bool,
) {
    let pending: Vec<_> = processes.into_iter().filter(|p| !p.settled()).collect();
    if pending.is_empty() || (holds.is_empty() && liveness.is_none()) {
        return;
    }
    let ids: Vec<(Key, usize)> = holds.iter().filter(|h| h.role == Role::Host).map(|h| (h.key.clone(), h.id)).collect();
    let kept = Arc::new(Kept { pending, holds: Mutex::new(Some((holds, liveness))) });
    let mut named = false;
    {
        let mut registry = registry().lock().unwrap_or_else(|e| e.into_inner());
        for (key, id) in ids {
            if let Some(slot) = registry.get_mut(&key).and_then(|entry| entry.host.as_mut()).filter(|slot| slot.id == id) {
                slot.kept = Some(Arc::clone(&kept));
                named = true;
            }
        }
    }
    if !start {
        return;
    }
    for process in &kept.pending {
        process.maintain();
    }
    let keeper = Arc::clone(&kept);
    let started = std::thread::Builder::new().name("home-hold-settlement".into()).spawn(move || loop {
        if keeper.release_if_settled() {
            return;
        }
        if keeper.stranded() {
            // Settlement can no longer be established: kept for the life of the process.
            std::mem::forget(keeper);
            return;
        }
        std::thread::sleep(std::time::Duration::from_millis(25));
    });
    if started.is_err() && !named {
        // No keeper and no home names what was left: nothing could release
        // it once settled, so it is kept for the life of the process.
        std::mem::forget(kept);
    }
    // Otherwise, without a keeper, each home's slot keeps what was left until
    // a later start attempt on the home finds the groups settled.
}

/// A fresh identity for a Host's role.
pub(crate) fn next_id() -> usize {
    static NEXT: AtomicUsize = AtomicUsize::new(1);
    NEXT.fetch_add(1, Ordering::SeqCst)
}

#[cfg(test)]
#[path = "home_hold_tests.rs"]
mod tests;
