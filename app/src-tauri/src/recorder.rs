//! Identifying decision package files and recording their `act_request` (R16).
//!
//! DEL-04-03 RECORD_SEMANTICS.md §13.6 "Decision packages" and its mapping
//! file -> record (R23-24); the body is DEL-02-03 `checkpoint-record-entries.schema.json`
//! `$defs/actRequest` (CE-4, form "decision package file"); the file's shape is
//! `$defs/decisionPackageFile`. This is DEL-02-03 `prototype/run_all.py`
//! `request_from_file`, ported.

use crate::records::{self, APP_WRITER};
use crate::util::{file_identity, now_rfc3339, FILE_IDENTITY_METHOD};
use serde_json::{json, Value};
use std::path::Path;

pub const DECISIONS_DIR: &str = "project/decisions";
pub const LOG: &str = "records/coordination.rs.jsonl";

/// RS §13.6 mapping. From the file: actKind, subject, purpose, scope, alternatives
/// {id, statement}, one consequence entry per statement. From the recorder: requester,
/// form, association, time, evidence. packageId and reservedBy stay in the file.
pub fn request_from_file(pkg: &Value, rel_path: &str, identity: &str, requester: Value, time: &str) -> Value {
    let mut body = json!({
        "requester": requester,
        "form": "decision package file",
        "actKind": pkg["actKind"],
        "subject": pkg["subject"],
        "purpose": pkg["purpose"],
    });
    if let Some(s) = pkg.get("scope") {
        body["scope"] = s.clone();
    }
    let alts = pkg["alternatives"].as_array().cloned().unwrap_or_default();
    body["association"] = json!("not at a checkpoint");
    body["evidence"] = json!({
        "kind": "content identity", "ref": rel_path, "claimedIdentity": identity,
        "method": FILE_IDENTITY_METHOD, "resolutionAtWrite": "resolved"});
    body["time"] = json!(time);
    body["alternatives"] = Value::Array(
        alts.iter().map(|a| json!({"id": a["id"], "statement": a["statement"]})).collect());
    body["consequences"] = Value::Array(
        alts.iter()
            .flat_map(|a| {
                let id = a["id"].clone();
                a["consequences"].as_array().cloned().unwrap_or_default()
                    .into_iter().map(move |c| json!({"alternative": id.clone(), "statement": c}))
            })
            .collect());
    body
}

/// A minimal shape check of `$defs/decisionPackageFile` (the full check is the schema's).
fn looks_like_package(v: &Value) -> bool {
    v.get("format") == Some(&json!("chirality.decision-package"))
        && v.get("actKind").is_some()
        && v.get("subject").map(|s| s.is_array()).unwrap_or(false)
        && v.get("purpose").is_some()
        && v.get("alternatives").and_then(|a| a.as_array()).map(|a| a.len() >= 2).unwrap_or(false)
}

/// Writes an `act_request` for each package file whose current bytes have no request yet.
/// A request is never identified from message text (§13.6); only files are read here.
pub fn identify_packages(workspace: &Path) -> Result<Vec<Value>, String> {
    let dir = workspace.join(DECISIONS_DIR);
    let log = workspace.join(LOG);
    let mut written = Vec::new();
    let mut files: Vec<_> = match std::fs::read_dir(&dir) {
        Ok(rd) => rd.filter_map(|e| e.ok()).map(|e| e.path())
            .filter(|p| p.extension().map(|x| x == "json").unwrap_or(false)).collect(),
        Err(_) => return Ok(written),
    };
    files.sort();
    let (entries, _) = records::read_log(&log);
    for path in files {
        let rel = format!("{DECISIONS_DIR}/{}", path.file_name().unwrap().to_string_lossy());
        let Some(identity) = file_identity(&path) else { continue };
        let already = entries.iter().chain(written.iter()).any(|e| {
            e["kind"] == "act_request"
                && e["body"]["evidence"]["ref"] == json!(rel)
                && e["body"]["evidence"]["claimedIdentity"] == json!(identity)
        });
        if already {
            continue;
        }
        let Ok(pkg) = serde_json::from_slice::<Value>(&std::fs::read(&path).map_err(|e| e.to_string())?) else { continue };
        if !looks_like_package(&pkg) {
            continue;
        }
        // CONTRACT_ISSUES CI-3: no rule says how the recorder establishes which agent wrote a
        // file it finds; the skeleton records the requester kind without an identity.
        let body = request_from_file(&pkg, &rel, &identity, json!({"kind": "agent"}), &now_rfc3339());
        written.push(records::append(&log, "act_request", &APP_WRITER, body)?);
    }
    Ok(written)
}
