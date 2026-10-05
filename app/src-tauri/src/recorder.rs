//! Identifying decision package files and recording their `act_request` (R16).
//!
//! DEL-04-03 RECORD_SEMANTICS.md §13.6 "Decision packages" and its mapping
//! file -> record (R23-24); the body is DEL-02-03 `checkpoint-record-entries.schema.json`
//! `$defs/actRequest` (CE-4, form "decision package file"); the file's shape is
//! `$defs/decisionPackageFile`. This is DEL-02-03 `prototype/run_all.py`
//! `request_from_file`, ported.

use crate::records::{self, APP_WRITER};
use crate::util::{
    now_rfc3339, package_snapshot, sha256_hex, FILE_IDENTITY_METHOD, LEGACY_FILE_IDENTITY_METHOD,
};
use serde_json::{json, Value};
use std::path::Path;

pub const DECISIONS_DIR: &str = "project/decisions";
pub const LOG: &str = ".chirality/records/acts/f8cb9d6c0500d9aa8d2a357335fa57ee813f7f1faed6b3dead34cfcad82662b8.jsonl";

/// RS §13.6 mapping. From the file: actKind, subject, purpose, scope, alternatives
/// {id, statement}, one consequence entry per statement. From the recorder: requester,
/// form, association, time, evidence. packageId and reservedBy stay in the file.
pub fn request_from_file(
    pkg: &Value,
    rel_path: &str,
    identity: &str,
    requester: Value,
    time: &str,
) -> Value {
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
        alts.iter()
            .map(|a| json!({"id": a["id"], "statement": a["statement"]}))
            .collect(),
    );
    body["consequences"] = Value::Array(
        alts.iter()
            .flat_map(|a| {
                let id = a["id"].clone();
                a["consequences"]
                    .as_array()
                    .cloned()
                    .unwrap_or_default()
                    .into_iter()
                    .map(move |c| json!({"alternative": id.clone(), "statement": c}))
            })
            .collect(),
    );
    body
}

/// Writes an `act_request` for each package file whose current bytes have no request yet.
/// A request is never identified from message text (§13.6); only files are read here.
pub fn identify_packages(workspace: &Path) -> Result<Vec<Value>, String> {
    let dir = workspace.join(DECISIONS_DIR);
    let log = workspace.join(LOG);
    let mut written = Vec::new();
    let mut files: Vec<_> = match std::fs::read_dir(&dir) {
        Ok(rd) => rd
            .filter_map(|e| e.ok())
            .map(|e| e.path())
            .filter(|p| p.extension().map(|x| x == "json").unwrap_or(false))
            .collect(),
        Err(_) => return Ok(written),
    };
    files.sort();
    let (entries, limits) = crate::storage::read_all(workspace);
    if !limits.is_empty() {
        return Err(format!("incomplete record set: {limits:?}"));
    }
    // Only the explicitly registered skeleton log has this known historical producer route.
    // Reobserve its own exact-byte designation for discovery idempotence; never translate history
    // into the selected method or claim comparable human-act standing.
    let (legacy_entries, legacy_limits) =
        records::read_log(&workspace.join(crate::storage::LEGACY_LOG));
    if !legacy_limits.is_empty() {
        return Err(format!(
            "incomplete registered legacy record: {legacy_limits:?}"
        ));
    }
    // Repair a missing separate requester limit after an interrupted recorder append.
    for req in entries.iter().filter(|e| {
        e["kind"] == "act_request"
            && e["body"]["form"] == "decision package file"
            && e["body"]["requester"].get("identity").is_none()
    }) {
        if !entries.iter().any(|e| {
            e["kind"] == "evidence_limit"
                && e["body"]["label"] == "requester identity not established"
                && e["body"]["subjectRef"] == req["recordId"]
        }) {
            records::append(
                &log,
                "evidence_limit",
                &APP_WRITER,
                json!({"label":"requester identity not established","subjectRef":req["recordId"],"detail":"package file observed; writer of the identified bytes not observed"}),
            )?;
        }
    }
    for path in files {
        let rel = format!(
            "{DECISIONS_DIR}/{}",
            path.file_name().unwrap().to_string_lossy()
        );
        let bytes = std::fs::read(&path).map_err(|e| e.to_string())?;
        let Ok((pkg, identity)) = package_snapshot(&bytes) else {
            continue;
        };
        let same_current = entries.iter().chain(written.iter()).any(|e| {
            e["kind"] == "act_request"
                && e["body"]["form"] == "decision package file"
                && e["body"]["evidence"]["ref"] == rel
                && e["body"]["evidence"]["method"] == FILE_IDENTITY_METHOD
                && e["body"]["evidence"]["claimedIdentity"] == identity
        });
        // The original claimed value is compared as an opaque token under its own known method.
        // No prefix is stripped, no historical identity is rewritten, and no unknown method is read.
        let legacy_observation = format!("sha256:{}", sha256_hex(&bytes));
        let same_registered_legacy = legacy_entries.iter().any(|e| {
            e["kind"] == "act_request"
                && e["body"]["form"] == "decision package file"
                && e["body"]["evidence"]["ref"] == rel
                && e["body"]["evidence"]["method"] == LEGACY_FILE_IDENTITY_METHOD
                && e["body"]["evidence"]["claimedIdentity"] == legacy_observation
        });
        let already = same_current || same_registered_legacy;
        if already {
            continue;
        }
        // CONTRACT_ISSUES CI-3: no rule says how the recorder establishes which agent wrote a
        // file it finds; the skeleton records the requester kind without an identity.
        let body = request_from_file(
            &pkg,
            &rel,
            &identity,
            json!({"kind": "agent"}),
            &now_rfc3339(),
        );
        let request = records::append(&log, "act_request", &APP_WRITER, body)?;
        records::append(
            &log,
            "evidence_limit",
            &APP_WRITER,
            json!({"label":"requester identity not established","subjectRef":request["recordId"],"detail":"package file observed; writer of the identified bytes not observed"}),
        )?;
        written.push(request);
    }
    Ok(written)
}
