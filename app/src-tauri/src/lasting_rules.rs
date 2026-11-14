//! DEL-01-01, DEL-04-02, PRD V4-AUT-06: the lasting rules a Codex home holds (`<home>/rules/*.rules`), read and
//! shown, never removed (decided for 4.0.0: read only). The App reads the files line by line and never evaluates
//! them: a line of exactly the form Codex writes for a prefix rule or a network rule is kept, with its fields and
//! the raw line; a blank line or a comment is ignored; every other line is only counted. The words, lines and
//! paths are text the App did not write and are kept raw, in their own fields, never inside an App sentence.
use serde_json::{json, Value};
use std::path::Path;

/// Said by the App beside every reading, verbatim.
pub const APP_SENTENCE: &str = "Conversations already open hold the rules as they were when Codex started them, so this is the file as read at the time shown, not necessarily what a running conversation applies.";

/// The most bytes read from one rules file; a larger file is not read and the reading is not known.
pub const FILE_LIMIT: u64 = 1024 * 1024;

const PREFIX_START: &str = "prefix_rule(pattern=[";
const PREFIX_END: &str = "], decision=\"allow\")";

/// `<home>/rules`, read as Codex chooses its files there: every entry whose own file type is a regular file and
/// whose name ends ".rules", links not followed. Any other entry is counted as skipped.
pub fn read(home: &Path) -> Value {
    let read_at = crate::util::now_rfc3339();
    let folder = home.join("rules");
    let not_known = |reason: String| json!({"state":"not-known","readAt":read_at,"files":[],"skippedEntries":0,"reason":reason});
    match std::fs::symlink_metadata(&folder) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return json!({"state":"none","readAt":read_at,"files":[],"skippedEntries":0}),
        Err(e) => return not_known(format!("The rules folder could not be examined: {e}")),
        Ok(meta) if meta.file_type().is_symlink() => return not_known("The rules folder is a link; the App does not follow it.".into()),
        Ok(meta) if !meta.is_dir() => return not_known("The rules entry in the Codex folder is not a folder.".into()),
        Ok(_) => {}
    }
    let entries = match std::fs::read_dir(&folder) {
        Ok(entries) => entries,
        Err(e) => return not_known(format!("The rules folder could not be read: {e}")),
    };
    let mut names: Vec<std::ffi::OsString> = Vec::new();
    let mut skipped = 0u64;
    for entry in entries {
        let entry = match entry {
            Ok(entry) => entry,
            Err(e) => return not_known(format!("The rules folder could not be read: {e}")),
        };
        // The entry's own type (`DirEntry::file_type` does not follow a link).
        let regular = entry.file_type().map(|t| t.is_file()).unwrap_or(false);
        let name = entry.file_name();
        if regular && name.to_string_lossy().ends_with(".rules") {
            names.push(name);
        } else {
            skipped += 1;
        }
    }
    names.sort();
    let mut files = Vec::new();
    let mut failures = Vec::new();
    for name in names {
        let path = folder.join(&name);
        match read_file(&path) {
            Ok(bytes) => files.push(parse(&path, &bytes)),
            Err(reason) => failures.push(json!({"path": path.to_string_lossy(), "reason": reason})),
        }
    }
    let state = if !failures.is_empty() { "not-known" } else if files.is_empty() { "none" } else { "read" };
    let mut out = json!({"state":state,"readAt":read_at,"files":files,"skippedEntries":skipped});
    if !failures.is_empty() {
        out["reason"] = json!("A rules file could not be read; see unreadFiles.");
        out["unreadFiles"] = Value::Array(failures);
    }
    out
}

/// The file's bytes, opened without following a link (the entry was a regular file when listed).
fn read_file(path: &Path) -> Result<Vec<u8>, String> {
    use std::io::Read;
    use std::os::unix::fs::OpenOptionsExt;
    let file = std::fs::OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC).open(path)
        .map_err(|e| format!("could not be opened: {e}"))?;
    let meta = file.metadata().map_err(|e| format!("could not be examined: {e}"))?;
    if !meta.is_file() {
        return Err("is no longer a regular file".into());
    }
    if meta.len() > FILE_LIMIT {
        return Err(format!("is larger than {FILE_LIMIT} bytes and was not read"));
    }
    let mut bytes = Vec::new();
    file.take(FILE_LIMIT + 1).read_to_end(&mut bytes).map_err(|e| format!("could not be read: {e}"))?;
    if bytes.len() as u64 > FILE_LIMIT {
        return Err(format!("is larger than {FILE_LIMIT} bytes and was not read"));
    }
    Ok(bytes)
}

/// One file's lines, as `{path, prefixRules, networkRules, unreadLines}`.
pub fn parse(path: &Path, bytes: &[u8]) -> Value {
    let mut prefix_rules = Vec::new();
    let mut network_rules = Vec::new();
    let mut unread = 0u64;
    let mut lines: Vec<&[u8]> = bytes.split(|b| *b == b'\n').collect();
    if lines.last().is_some_and(|l| l.is_empty()) {
        lines.pop();
    }
    for raw in lines {
        let raw = raw.strip_suffix(b"\r").unwrap_or(raw);
        let Ok(line) = std::str::from_utf8(raw) else { unread += 1; continue };
        if line.trim().is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some(words) = prefix_rule(line) {
            prefix_rules.push(json!({"words": words, "line": line}));
        } else if let Some(mut rule) = network_rule(line) {
            rule["line"] = json!(line);
            network_rules.push(rule);
        } else {
            unread += 1;
        }
    }
    json!({"path": path.to_string_lossy(), "prefixRules": prefix_rules, "networkRules": network_rules, "unreadLines": unread})
}

/// The words of a line exactly `prefix_rule(pattern=[<JSON strings, comma-space separated>], decision="allow")`.
fn prefix_rule(line: &str) -> Option<Vec<String>> {
    let middle = line.strip_prefix(PREFIX_START)?.strip_suffix(PREFIX_END)?;
    let words: Vec<String> = serde_json::from_str(&format!("[{middle}]")).ok()?;
    if words.is_empty() {
        return None;
    }
    // Exactly the form: each word as its JSON string, separated by a comma and one space, nothing else.
    let canonical = words.iter().map(|w| serde_json::to_string(w).expect("a string serializes")).collect::<Vec<_>>().join(", ");
    (canonical == middle).then_some(words)
}

/// The fields of a line exactly `network_rule(host="...", protocol="...", decision="...")`, optionally with
/// `, justification="..."` before the closing parenthesis.
fn network_rule(line: &str) -> Option<Value> {
    let rest = line.strip_prefix("network_rule(host=")?;
    let (host, rest) = json_string(rest)?;
    let rest = rest.strip_prefix(", protocol=")?;
    let (protocol, rest) = json_string(rest)?;
    let rest = rest.strip_prefix(", decision=")?;
    let (decision, rest) = json_string(rest)?;
    let (justification, rest) = match rest.strip_prefix(", justification=") {
        Some(rest) => {
            let (text, rest) = json_string(rest)?;
            (Some(text), rest)
        }
        None => (None, rest),
    };
    if rest != ")" {
        return None;
    }
    let mut rule = json!({"host": host, "protocol": protocol, "decision": decision});
    if let Some(text) = justification {
        rule["justification"] = json!(text);
    }
    Some(rule)
}

/// A JSON string at the start of `text`, decoded, and what follows it.
fn json_string(text: &str) -> Option<(String, &str)> {
    if !text.starts_with('"') {
        return None;
    }
    let bytes = text.as_bytes();
    let mut i = 1;
    while i < bytes.len() {
        match bytes[i] {
            b'\\' => i += 2,
            b'"' => {
                let decoded: String = serde_json::from_str(&text[..=i]).ok()?;
                return Some((decoded, &text[i + 1..]));
            }
            _ => i += 1,
        }
    }
    None
}

#[cfg(test)]
#[path = "lasting_rules_tests.rs"]
mod tests;
