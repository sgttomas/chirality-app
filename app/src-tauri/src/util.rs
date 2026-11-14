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

/// The operating-system account of the user running the App (AAC §7: always present).
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
