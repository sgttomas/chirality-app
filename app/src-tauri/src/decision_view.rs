//! Decision view model, derived from files only.
//!
//! DEL-06-02 DECISION_VIEW.md (DV-v0.1) §3 DV-1…DV-9, §4 row states, §6 failure
//! behaviour. A port of the Pass 4 prototype `E/decision_view.py`. It reads the RS
//! log and the package files the records cite; it writes nothing (DV-9).

use crate::records;
use crate::util::file_identity;
use serde_json::{json, Value};
use std::collections::{HashMap, HashSet};
use std::path::Path;

const PERSON_WORDING: &str = "identity not verified";

pub fn person_label(p: &Value) -> String {
    let names: Vec<&str> = ["displayName", "osAccount", "codexAccount", "hostActor"]
        .iter()
        .filter_map(|k| p.get(*k).and_then(|v| v.as_str()).filter(|s| !s.is_empty()))
        .collect();
    let who = if names.is_empty() { "person not named".to_string() } else { names.join(" / ") };
    if p.get("identityVerified") == Some(&json!(true)) { who } else { format!("{who} ({PERSON_WORDING})") }
}

pub fn derive(root: &Path, record_paths: &[&str]) -> Value {
    let mut entries = Vec::new();
    let mut limits: Vec<String> = Vec::new();
    for rp in record_paths {
        let (e, l) = records::read_log(&root.join(rp));
        entries.extend(e);
        limits.extend(l);
    }
    let by_id: HashMap<String, &Value> = entries
        .iter()
        .filter_map(|e| e["recordId"].as_str().map(|id| (id.to_string(), e)))
        .collect();
    // DV-1: a row per act_request that carries alternatives.
    let packages: Vec<&Value> = entries
        .iter()
        .filter(|e| e["kind"] == "act_request" && e["body"].get("alternatives").is_some())
        .collect();
    let acts: Vec<&Value> = entries.iter().filter(|e| e["kind"] == "human_act").collect();
    let mut rows = Vec::new();
    for p in packages {
        let b = &p["body"];
        let pid = p["recordId"].as_str().unwrap_or("");
        let alts = b["alternatives"].as_array().cloned().unwrap_or_default();
        let cons = b["consequences"].as_array().cloned().unwrap_or_default();
        let alt_ids: Vec<&str> = alts.iter().filter_map(|a| a["id"].as_str()).collect();
        let mut row_limits: Vec<String> = Vec::new();
        // DV-2
        if alt_ids.iter().collect::<HashSet<_>>().len() != alt_ids.len() {
            row_limits.push("alternative identities repeat within the package".into());
        }
        let mut orphans: Vec<&str> = cons.iter().filter_map(|c| c["alternative"].as_str())
            .filter(|a| !alt_ids.contains(a)).collect();
        orphans.sort();
        orphans.dedup();
        if !orphans.is_empty() {
            row_limits.push(format!("consequences name no alternative of the package: {orphans:?}"));
        }
        let missing: Vec<&str> = alt_ids.iter().copied()
            .filter(|a| !cons.iter().any(|c| c["alternative"] == json!(a))).collect();
        if !missing.is_empty() {
            row_limits.push(format!("no consequence stated for: {missing:?}"));
        }
        // DV-3
        let file_ref = b["evidence"]["ref"].as_str().unwrap_or("");
        let now = file_identity(&root.join(file_ref));
        let recorded = b["evidence"]["claimedIdentity"].as_str();
        match (&now, recorded) {
            (None, _) => row_limits.push("package file not available: its current content is unknown".into()),
            (Some(n), Some(r)) if n != r => row_limits.push("package file differs from the content the request recorded".into()),
            _ => {}
        }
        // DV-4, DV-5
        let mut decided: Vec<&Value> = Vec::new();
        for a in acts.iter().filter(|a| a["body"]["relations"]["requestRef"] == json!(pid)) {
            let ab = &a["body"];
            let rid = a["recordId"].as_str().unwrap_or("");
            if ab["actKind"] != b["actKind"] {
                row_limits.push(format!("{rid}: an act of kind {} cites this package; it is not the {} the package requests",
                    ab["actKind"].as_str().unwrap_or("?"), b["actKind"].as_str().unwrap_or("?")));
                continue;
            }
            let chosen = ab["relations"]["alternativeChosen"].as_str();
            if b["actKind"] == "A16" && !chosen.map(|c| alt_ids.contains(&c)).unwrap_or(false) {
                row_limits.push(format!("{rid}: act not counted: chosen alternative {chosen:?} is not one the package names"));
                continue;
            }
            decided.push(a);
        }
        let mut row = json!({
            "package": pid,
            "packageFile": file_ref,
            "actRequested": b["actKind"],
            "subject": b["subject"],
            "purpose": b["purpose"],
            "scope": b.get("scope"),
            "requestedBy": b["requester"].get("identity").unwrap_or(&b["requester"]["kind"]),
            "alternatives": alts.iter().map(|a| json!({
                "id": a["id"], "statement": a["statement"],
                "consequences": cons.iter().filter(|c| c["alternative"] == a["id"]).map(|c| c["statement"].clone()).collect::<Vec<_>>()
            })).collect::<Vec<_>>(),
            "state": "pending — awaiting the person's decision",
            "decision": Value::Null,
            "limits": [],
        });
        // DV-6: corrections replace what they correct; a later act supersedes an earlier one.
        let corrected: HashMap<String, String> = decided.iter()
            .filter_map(|a| a["corrects"].as_str().map(|c| (c.to_string(), a["recordId"].as_str().unwrap_or("").to_string())))
            .collect();
        let current: Vec<&&Value> = decided.iter()
            .filter(|a| !corrected.contains_key(a["recordId"].as_str().unwrap_or(""))).collect();
        if let Some(a) = current.last() {
            let ab = &a["body"];
            let chosen = ab["relations"]["alternativeChosen"].as_str().unwrap_or("");
            let bound = ab["boundContent"][0]["value"].as_str();
            // DV-7
            let lapse = match (&now, bound) {
                (None, _) => "unknown (unavailable)",
                (Some(n), Some(bv)) if n == bv => "not lapsed",
                _ => "lapsed — the package changed after the decision",
            };
            let arid = a["recordId"].as_str().unwrap_or("");
            row["state"] = json!("decided");
            row["decision"] = json!({
                "act": arid,
                "actKind": ab["actKind"],
                "alternativeChosen": chosen,
                "statement": alts.iter().find(|x| x["id"] == json!(chosen)).map(|x| x["statement"].clone()),
                // DV-8
                "decidedBy": person_label(&ab["decisionActor"]),
                "recordedBy": format!("{} {}", a["recorder"]["role"].as_str().unwrap_or(""), a["recorder"]["identity"].as_str().unwrap_or("")),
                "recordingMode": ab["recordingMode"],
                "captureEvidence": ab["captureEvidence"].as_array().map(|c| c.iter().map(|x| x["ref"].clone()).collect::<Vec<_>>()),
                "capturedAt": ab["captureTime"],
                "lapse": lapse,
                "earlierActs": decided.iter().filter(|x| x["recordId"] != a["recordId"]).map(|x| {
                    let xid = x["recordId"].as_str().unwrap_or("");
                    json!({"act": xid,
                           "relation": match corrected.get(xid) { Some(c) => format!("corrected by {c}"), None => format!("superseded by {arid}") },
                           "alternativeChosen": x["body"]["relations"]["alternativeChosen"]})
                }).collect::<Vec<_>>(),
            });
        }
        row["limits"] = json!(row_limits);
        rows.push(row);
    }
    // §6: an act citing a request the log does not hold is a view limit, on no row.
    for a in &acts {
        if let Some(r) = a["body"]["relations"]["requestRef"].as_str() {
            if by_id.get(r).map(|e| e["kind"] != "act_request").unwrap_or(true) {
                limits.push(format!("{}: cites request {r}, which this record set does not hold", a["recordId"].as_str().unwrap_or("")));
            }
        }
    }
    json!({"view": "decision packages (DEL-06-02; derived, not authority)", "rows": rows, "limits": limits})
}
