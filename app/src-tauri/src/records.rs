//! RS format 0.1 log writer and reader (DEL-04-03 RECORD_SEMANTICS.md §13.1 S-A,
//! §13.2 entry header, §14.1 W-0/W-1, §14.2 R-2).
//!
//! One append-only JSON Lines log per writer; one entry per line; `seq` taken only
//! by a successful write; a written entry is never rewritten (OF-5).
//!
//! Skeleton limits (see README and EVIDENCE):
//! - W-1 says the writer validates each entry against `RS_RECORD.schema.json`
//!   before writing. No JSON Schema validator crate is in the offline cargo cache,
//!   so the writer does not validate; the automated test validates every entry the
//!   skeleton writes with Ajv (draft 2020-12) against the schema as it is.
//! - W-0's repair of an unterminated last line and W-2's late write are not
//!   implemented: a log ending in a partial line is refused.

use crate::util::now_rfc3339;
use serde_json::{json, Value};
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;

pub struct Recorder<'a> {
    pub role: &'a str,
    pub identity: &'a str,
}

pub const APP_WRITER: Recorder<'static> = Recorder { role: "App writer", identity: "app-writer:local" };
pub const APP_INTERFACE: Recorder<'static> =
    Recorder { role: "App interface (capturing surface)", identity: "app-interface:local" };

/// R-2: entries in written order; an unreadable line is kept as a limit, never used.
pub fn read_log(path: &Path) -> (Vec<Value>, Vec<String>) {
    let mut entries = Vec::new();
    let mut limits = Vec::new();
    let text = match std::fs::read_to_string(path) {
        Ok(t) => t,
        Err(_) => return (entries, limits),
    };
    let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let n_lines = text.lines().count();
    for (n, line) in text.lines().enumerate() {
        if line.trim().is_empty() {
            continue;
        }
        match serde_json::from_str::<Value>(line) {
            Ok(v) => entries.push(v),
            Err(_) if n + 1 == n_lines && !text.ends_with('\n') => {
                limits.push(format!("{name}: partial entry at end (not read)"))
            }
            Err(_) => limits.push(format!("{name}: unreadable line {}", n + 1)),
        }
    }
    (entries, limits)
}

/// W-0 + W-1: open, take the next seq, complete the header, write one line in one write, sync.
pub fn append(log: &Path, kind: &str, recorder: &Recorder, body: Value) -> Result<Value, String> {
    if let Some(dir) = log.parent() {
        std::fs::create_dir_all(dir).map_err(|e| format!("log directory: {e}"))?;
    }
    let existing = std::fs::read(log).unwrap_or_default();
    if !existing.is_empty() && !existing.ends_with(b"\n") {
        return Err("the log ends in a partial line (W-0 repair not in the skeleton); nothing written".into());
    }
    let (entries, _) = read_log(log);
    let seq = entries.iter().filter_map(|e| e.get("seq").and_then(|s| s.as_u64())).max().unwrap_or(0) + 1;
    // Record identity minting is unselected (RS §13.2); the skeleton uses the fixture's form.
    let entry = json!({
        "format": "chirality.rs.record",
        "formatVersion": "0.1",
        "recordId": format!("rec:app:coord:{:04}", seq),
        "kind": kind,
        "recorder": {"role": recorder.role, "identity": recorder.identity},
        "context": {"surface": "App"},
        "seq": seq,
        "writtenAt": now_rfc3339(),
        "body": body,
    });
    let mut line = serde_json::to_string(&entry).map_err(|e| e.to_string())?;
    line.push('\n');
    let mut f = OpenOptions::new().create(true).append(true).open(log).map_err(|e| format!("open log: {e}"))?;
    f.write_all(line.as_bytes()).map_err(|e| format!("write: {e}"))?;
    f.sync_all().map_err(|e| format!("sync: {e}"))?;
    Ok(entry)
}
