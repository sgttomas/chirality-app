//! Small helpers shared by the modules: clock text and content identity.

use sha2::{Digest, Sha256};
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};

/// Historical designation, retained verbatim for reading; never rewrite old records.
pub const LEGACY_FILE_IDENTITY_METHOD: &str =
    "file content identity (method unselected; TEST VALUE: sha-256 of the file bytes)";
/// Selected bounded App exact-byte method (RS §6.2a CC-CONTENT-RX).
/// New identities are lowercase 64-hex SHA-256 over the exact observed buffer.
pub const FILE_IDENTITY_METHOD: &str = "chirality.app.exact-bytes.sha256/v1";

pub fn sha256_hex(bytes: &[u8]) -> String {
    let mut h = Sha256::new();
    h.update(bytes);
    h.finalize().iter().map(|b| format!("{:02x}", b)).collect()
}

/// Selected exact-byte identity, or None when the file cannot be read.
pub fn file_identity(path: &Path) -> Option<String> {
    std::fs::read(path).ok().map(|b| sha256_hex(&b))
}

/// UTC time as RFC 3339 text with milliseconds. RS §13.2 leaves the
/// representation of `writtenAt` unselected; this is the skeleton's choice.
pub fn now_rfc3339() -> String {
    let d = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default();
    let secs = d.as_secs() as i64;
    let ms = d.subsec_millis();
    let days = secs.div_euclid(86_400);
    let sod = secs.rem_euclid(86_400);
    let (y, m, dd) = civil_from_days(days);
    format!(
        "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}.{:03}Z",
        y,
        m,
        dd,
        sod / 3600,
        (sod % 3600) / 60,
        sod % 60,
        ms
    )
}

/// RFC 3339 UTC text with milliseconds for a Unix time in milliseconds, such
/// as a supplier `startedAtMs` / `completedAtMs` value.
pub fn rfc3339_from_ms(ms: i64) -> String {
    let secs = ms.div_euclid(1000);
    let days = secs.div_euclid(86_400);
    let sod = secs.rem_euclid(86_400);
    let (y, m, dd) = civil_from_days(days);
    format!("{:04}-{:02}-{:02}T{:02}:{:02}:{:02}.{:03}Z", y, m, dd, sod / 3600, (sod % 3600) / 60, sod % 60, ms.rem_euclid(1000))
}

// Howard Hinnant's days-to-civil algorithm.
fn civil_from_days(z: i64) -> (i64, u32, u32) {
    let z = z + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097);
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let y = yoe + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = (doy - (153 * mp + 2) / 5 + 1) as u32;
    let m = if mp < 10 { mp + 3 } else { mp - 9 } as u32;
    (if m <= 2 { y + 1 } else { y }, m, d)
}

/// The name of the operating-system account the App runs as, read once for
/// the App's session on a thread of its own, and not at each act. The App
/// never changes its credentials (nothing in its source calls setuid, seteuid,
/// setgid or setgroups); the mapping from its uid to a name can change outside
/// the App, so this is what was read, when it was read.
pub(crate) static OS_ACCOUNT: AccountObservation = AccountObservation::new(os_account);
/// How long an act that requires the account waits for the session's
/// observation (this lane's own bound, which it may change).
pub(crate) const ACCOUNT_WAIT_LIMIT: std::time::Duration = std::time::Duration::from_secs(3);
/// Shown to the person when an act that records the account cannot have it in time.
pub(crate) const ACCOUNT_NOT_YET_READ: &str = "Chirality has not yet been able to read the name of the account it is running as, which this act records. Try again in a moment.";
/// One observation, read once on its own thread. Callers never make the read
/// on their own thread: they look at it, or wait for it within a bound.
pub(crate) struct AccountObservation {
    read: fn() -> Option<String>,
    started: std::sync::atomic::AtomicBool,
    value: std::sync::Mutex<Option<Option<String>>>,
    ready: std::sync::Condvar,
}
impl AccountObservation {
    pub(crate) const fn new(read: fn() -> Option<String>) -> Self {
        Self { read, started: std::sync::atomic::AtomicBool::new(false), value: std::sync::Mutex::new(None), ready: std::sync::Condvar::new() }
    }
    /// An observation whose read has already finished, for tests.
    #[cfg(test)]
    pub(crate) fn finished(read: Option<&str>) -> &'static Self {
        let observation: &'static Self = Box::leak(Box::new(Self::new(|| None)));
        observation.started.store(true, std::sync::atomic::Ordering::SeqCst);
        *observation.value.lock().unwrap() = Some(read.map(str::to_owned));
        observation
    }
    /// Starts the read on its own thread, once; false where it could not start.
    pub(crate) fn start(&'static self) -> bool {
        if self.started.swap(true, std::sync::atomic::Ordering::SeqCst) { return true; }
        std::thread::Builder::new().name("os-account".into()).spawn(move || {
            let read = (self.read)();
            *self.value.lock().unwrap_or_else(|e| e.into_inner()) = Some(read);
            self.ready.notify_all();
        }).map_err(|_| self.started.store(false, std::sync::atomic::Ordering::SeqCst)).is_ok()
    }
    /// The observation if it is there, never waited for: None where the read
    /// has not finished, could not start, or found no name.
    pub(crate) fn observed(&self) -> Option<String> {
        self.value.lock().unwrap_or_else(|e| e.into_inner()).clone().flatten()
    }
    /// For an act that requires the account: the observation, waiting for it
    /// at most `limit` (starting the read if it was never started). Some(read)
    /// once the read has finished; None if it has not within the limit.
    pub(crate) fn within(&'static self, limit: std::time::Duration) -> Option<Option<String>> {
        self.start();
        let deadline = std::time::Instant::now() + limit;
        let mut value = self.value.lock().unwrap_or_else(|e| e.into_inner());
        while value.is_none() {
            let left = deadline.saturating_duration_since(std::time::Instant::now());
            if left.is_zero() { return None; }
            value = self.ready.wait_timeout(value, left).unwrap_or_else(|e| e.into_inner()).0;
        }
        value.clone()
    }
}

/// The operating-system account of the user running the App (AAC §7): the
/// lookup itself, made only by [`OS_ACCOUNT`]'s own thread.
pub fn os_account() -> Option<String> {
    // SAFETY: getpwuid returns a pointer into static storage or null; we copy out at once.
    unsafe {
        let pw = libc::getpwuid(libc::getuid());
        if pw.is_null() || (*pw).pw_name.is_null() {
            return std::env::var("USER").ok();
        }
        Some(
            std::ffi::CStr::from_ptr((*pw).pw_name)
                .to_string_lossy()
                .into_owned(),
        )
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn epoch_formats() {
        assert_eq!(super::civil_from_days(0), (1970, 1, 1));
        assert_eq!(super::civil_from_days(20_000), (2024, 10, 4));
    }
}

/// Secure, opaque identity; entropy failure never falls back to a counter or clock.
pub fn opaque_id(prefix: &str) -> Result<String, String> {
    opaque_id_with(prefix, |bytes| {
        getrandom::fill(bytes).map_err(|e| e.to_string())
    })
}
pub fn opaque_id_with(
    prefix: &str,
    entropy: impl FnOnce(&mut [u8; 16]) -> Result<(), String>,
) -> Result<String, String> {
    let mut bytes = [0; 16];
    entropy(&mut bytes).map_err(|e| format!("secure identity entropy unavailable: {e}"))?;
    Ok(format!(
        "{prefix}{}",
        uuid::Builder::from_random_bytes(bytes).into_uuid()
    ))
}

/// Parse and identify one immutable observed buffer, never a separate file read.
pub fn package_snapshot(bytes: &[u8]) -> Result<(serde_json::Value, String), String> {
    let package: serde_json::Value =
        serde_json::from_slice(bytes).map_err(|e| format!("package snapshot unreadable: {e}"))?;
    crate::schema_validation::validate_package(&package)?;
    Ok((package, sha256_hex(bytes)))
}

/// The mutex, taken by `deadline` or not at all: polls `try_lock` so that the
/// caller's wait has the deadline as its bound whatever the holder is doing.
/// A poisoned mutex is taken as it is.
pub fn lock_by<T>(mutex: &std::sync::Mutex<T>, deadline: std::time::Instant) -> Option<std::sync::MutexGuard<'_, T>> {
    loop {
        match mutex.try_lock() {
            Ok(guard) => return Some(guard),
            Err(std::sync::TryLockError::Poisoned(poisoned)) => return Some(poisoned.into_inner()),
            Err(std::sync::TryLockError::WouldBlock) => {}
        }
        let now = std::time::Instant::now();
        if now >= deadline {
            return None;
        }
        std::thread::sleep((deadline - now).min(std::time::Duration::from_millis(5)));
    }
}

/// What releasing a value on its own thread came to.
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum Released { Done, NotTaken, NotStarted, NotHanded, NotInTime }
/// Drops a value on a thread of its own and waits for that until `deadline`,
/// never longer. The thread is started (by `start`) before the value is taken
/// (by `take`) and handed to it, so the value is never dropped on this caller:
/// where the thread cannot start, or cannot receive it, the value is leaked,
/// as a crash leaves it. A release not finished by the deadline goes on, and
/// is not waited for.
pub(crate) fn release_off_thread<T: Send + 'static>(
    start: impl FnOnce(Box<dyn FnOnce() + Send>) -> std::io::Result<()>,
    take: impl FnOnce() -> Option<T>,
    deadline: std::time::Instant,
) -> Released {
    let (handed, values) = std::sync::mpsc::channel::<T>();
    let (done, finished) = std::sync::mpsc::channel();
    let started = start(Box::new(move || { if let Ok(value) = values.recv() { drop(value); let _ = done.send(()); } }));
    let Some(value) = take() else { return Released::NotTaken };
    if started.is_err() {
        std::mem::forget(value);
        return Released::NotStarted;
    }
    if let Err(std::sync::mpsc::SendError(value)) = handed.send(value) {
        std::mem::forget(value);
        return Released::NotHanded;
    }
    match finished.recv_timeout(deadline.saturating_duration_since(std::time::Instant::now())) {
        Ok(()) => Released::Done,
        Err(_) => Released::NotInTime,
    }
}

/// How many diagnostics wait to be written before a new one is dropped.
pub(crate) const DIAGNOSTIC_QUEUE: usize = 64;
static DIAGNOSTICS: std::sync::OnceLock<std::sync::mpsc::SyncSender<String>> = std::sync::OnceLock::new();
static DIAGNOSTICS_DROPPED: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);
/// Starts the thread that writes diagnostics to standard error, at App start.
/// A full or stalled standard error then stalls only that thread.
pub(crate) fn start_diagnostics() {
    let (sender, lines) = std::sync::mpsc::sync_channel::<String>(DIAGNOSTIC_QUEUE);
    let started = std::thread::Builder::new().name("diagnostics".into()).spawn(move || {
        for line in lines {
            let dropped = DIAGNOSTICS_DROPPED.swap(0, std::sync::atomic::Ordering::SeqCst);
            if dropped > 0 { eprintln!("chirality: {dropped} diagnostics could not be written"); }
            eprintln!("{line}");
        }
    });
    if started.is_ok() { let _ = DIAGNOSTICS.set(sender); }
}
/// One diagnostic line, best effort, never waited for: queued for the
/// diagnostics thread if there is room at once, otherwise dropped and
/// counted. The count is written before the next line that is written, if any
/// is; nothing flushes, drains or joins the thread. Before the thread has
/// started, or where it could not start, the line is dropped and counted.
/// Nothing a person must read goes only through here.
pub(crate) fn diagnostic(line: String) {
    let queued = DIAGNOSTICS.get().is_some_and(|sender| sender.try_send(line).is_ok());
    if !queued { DIAGNOSTICS_DROPPED.fetch_add(1, std::sync::atomic::Ordering::SeqCst); }
}
