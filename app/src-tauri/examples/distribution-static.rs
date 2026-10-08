//! Read-only static inventory CLI. No supplier, host, selection or store operations.
use std::io::Write;

#[cfg(unix)]
fn run() -> Result<(), String> {
    use chirality_app_v4_lib::distribution_preflight::{equal, scan, Inventory};
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    let mut output = match args.first().and_then(|v| v.to_str()) {
        Some("scan") if args.len() == 2 => {
            let inventory = scan(std::path::Path::new(&args[1]))?;
            serde_json::to_vec(&inventory).map_err(|e| e.to_string())?
        }
        Some("compare") if args.len() == 3 => {
            let read = |path: &std::ffi::OsStr| -> Result<Inventory, String> {
                let bytes = std::fs::read(path).map_err(|e| format!("inventory read failed: {e}"))?;
                serde_json::from_slice(&bytes).map_err(|e| format!("inventory JSON invalid: {e}"))
            };
            let expected = read(&args[1])?;
            let actual = read(&args[2])?;
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
