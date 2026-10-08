//! Read-only static inventory CLI. No supplier, host, selection or store operations.
use std::io::Write;

/// Bound caller-owned comparison inputs; these are equality inputs, not trust roots.
#[cfg(unix)]
fn read_inventory(
    path: &std::ffi::OsStr,
) -> Result<chirality_app_v4_lib::distribution_preflight::Inventory, String> {
    use std::io::Read;
    use std::os::unix::fs::{MetadataExt, OpenOptionsExt};
    const MAX_BYTES: u64 = 64 * 1024 * 1024;
    let metadata =
        std::fs::symlink_metadata(path).map_err(|e| format!("inventory metadata failed: {e}"))?;
    if !metadata.file_type().is_file() || metadata.len() > MAX_BYTES {
        return Err("inventory must be a regular non-link file of at most 64 MiB".into());
    }
    let file = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC)
        .open(path)
        .map_err(|e| format!("inventory no-follow read failed: {e}"))?;
    let opened = file.metadata().map_err(|e| e.to_string())?;
    if !opened.is_file()
        || opened.len() > MAX_BYTES
        || opened.dev() != metadata.dev()
        || opened.ino() != metadata.ino()
    {
        return Err("inventory source is nonregular, too large or changed before read".into());
    }
    let mut bytes = Vec::new();
    (&file)
        .take(MAX_BYTES + 1)
        .read_to_end(&mut bytes)
        .map_err(|e| format!("inventory read failed: {e}"))?;
    if bytes.len() as u64 > MAX_BYTES {
        return Err("inventory exceeds 64 MiB".into());
    }
    let after = file.metadata().map_err(|e| e.to_string())?;
    if after.len() != opened.len()
        || after.mtime() != opened.mtime()
        || after.mtime_nsec() != opened.mtime_nsec()
        || after.ctime() != opened.ctime()
        || after.ctime_nsec() != opened.ctime_nsec()
        || bytes.len() as u64 != opened.len()
    {
        return Err("inventory changed during read".into());
    }
    serde_json::from_slice(&bytes).map_err(|e| format!("inventory JSON invalid: {e}"))
}

#[cfg(unix)]
fn run() -> Result<(), String> {
    use chirality_app_v4_lib::distribution_preflight::{equal, scan};
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    let mut output = match args.first().and_then(|v| v.to_str()) {
        Some("scan") if args.len() == 2 => {
            let inventory = scan(std::path::Path::new(&args[1]))?;
            serde_json::to_vec(&inventory).map_err(|e| e.to_string())?
        }
        Some("compare") if args.len() == 3 => {
            let expected = read_inventory(&args[1])?;
            let actual = read_inventory(&args[2])?;
            serde_json::to_vec(&serde_json::json!({"equal":equal(&expected, &actual)})).map_err(|e| e.to_string())?
        }
        _ => return Err("usage: distribution-static scan ABSOLUTE_TREE | compare EXPECTED_JSON ACTUAL_JSON (Unix only)".into()),
    };
    output.push(b'\n');
    std::io::stdout()
        .lock()
        .write_all(&output)
        .map_err(|e| e.to_string())
}
#[cfg(not(unix))]
fn run() -> Result<(), String> {
    Err("distribution-static supports Unix only".into())
}
fn main() -> std::process::ExitCode {
    match run() {
        Ok(()) => std::process::ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("distribution-static: {error}");
            std::process::ExitCode::FAILURE
        }
    }
}
