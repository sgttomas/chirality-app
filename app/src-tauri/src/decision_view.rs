//! Decision view model, derived from files only.
//!
//! DEL-06-02 DECISION_VIEW.md (DV-v0.1) §3 DV-1…DV-9, §4 row states, §6 failure
//! behaviour. A port of the Pass 4 prototype `E/decision_view.py`. It reads the RS
//! log and the package files the records cite; it writes nothing (DV-9).

use crate::act_policy::ContentIdentity;
use crate::records;
use crate::standing::{compare, CurrentContent, Lapse};
use crate::util::{sha256_hex, FILE_IDENTITY_METHOD};
use serde_json::{json, Value};
use std::collections::{HashMap, HashSet};
use std::path::Path;

const PERSON_WORDING: &str = "identity not verified";

pub fn person_label(p: &Value) -> String {
    let names: Vec<&str> = ["displayName", "osAccount", "codexAccount", "hostActor"]
        .iter()
        .filter_map(|k| p.get(*k).and_then(|v| v.as_str()).filter(|s| !s.is_empty()))
        .collect();
    let who = if names.is_empty() {
        "person not named".to_string()
    } else {
        names.join(" / ")
    };
    if p.get("identityVerified") == Some(&json!(true)) {
        who
    } else {
        format!("{who} ({PERSON_WORDING})")
    }
}

/// One coherent current buffer; no record, capture, or native-origin admission.
struct FileObservation {
    identity: Option<ContentIdentity>,
    absent: bool,
}
fn observe_file(root: &Path, reference: &str, limits: &mut Vec<String>) -> FileObservation {
    let rel = Path::new(reference);
    if reference.is_empty()
        || rel.is_absolute()
        || rel
            .components()
            .any(|c| !matches!(c, std::path::Component::Normal(_)))
    {
        limits.push(
            "package file reference is not a contained relative path; content not observed".into(),
        );
        return FileObservation {
            identity: None,
            absent: false,
        };
    }
    let path = root.join(rel);
    if let Err(e) = crate::storage::check_path(&path) {
        limits.push(format!("package file content not observed: {e}"));
        return FileObservation {
            identity: None,
            absent: false,
        };
    }
    match std::fs::read(path) {
        Ok(bytes) => FileObservation {
            identity: Some(ContentIdentity {
                method: FILE_IDENTITY_METHOD.into(),
                value: sha256_hex(&bytes),
            }),
            absent: false,
        },
        Err(e) => FileObservation {
            identity: None,
            absent: e.kind() == std::io::ErrorKind::NotFound,
        },
    }
}
fn identity(value: &Value) -> ContentIdentity {
    ContentIdentity {
        method: value["method"].as_str().unwrap_or("").into(),
        value: value["value"].as_str().unwrap_or("").into(),
    }
}
fn label(state: Lapse) -> &'static str {
    match state {
        Lapse::NotLapsed => "not lapsed",
        Lapse::Lapsed => "lapsed — the package changed after the decision",
        Lapse::SubjectAbsent => "lapsed (subject absent)",
        Lapse::MatchesAgainAfterLapse => "matches c0 again after observed lapse",
        Lapse::Incomparable => "unknown (incomparable)",
        Lapse::Unavailable => "unknown (unavailable)",
        Lapse::NotEvaluated => "not yet evaluated",
    }
}
/// Recorded lapse observations are claims too. Match the exact act, kind,
/// referent and original method/value; another act/package supplies no history.
fn lapse_history<'a>(
    entries: &'a [Value],
    act_id: &str,
    subject: &str,
    bound: &ContentIdentity,
) -> Vec<&'a Value> {
    entries
        .iter()
        .filter(|e| {
            let b = &e["body"];
            e["kind"] == "act_lapsed"
                && b["act"]["recordId"] == act_id
                && b["act"]["actKind"] == "A16"
                && b["referents"]
                    .as_array()
                    .is_some_and(|v| v.len() == 1 && v[0] == subject)
                && identity(&b["c0"]) == *bound
                && match b["state"].as_str() {
                    Some("lapsed" | "partially lapsed") => {
                        let changed = identity(&b["c1"]);
                        changed.method == bound.method
                            && !changed.value.is_empty()
                            && changed.value != bound.value
                    }
                    Some("lapsed (subject absent)") => b["c1"] == "subject absent",
                    _ => false,
                }
        })
        .collect()
}

pub fn derive(root: &Path, record_paths: &[&str]) -> Value {
    let mut entries = Vec::new();
    let mut limits: Vec<String> = Vec::new();
    for rp in record_paths {
        let (e, l) = records::read_log(&root.join(rp));
        entries.extend(e);
        limits.extend(l);
    }
    if record_paths.is_empty() {
        let (e, l) = crate::storage::read_all(root);
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
    let acts: Vec<&Value> = entries
        .iter()
        .filter(|e| e["kind"] == "human_act")
        .collect();
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
        let mut orphans: Vec<&str> = cons
            .iter()
            .filter_map(|c| c["alternative"].as_str())
            .filter(|a| !alt_ids.contains(a))
            .collect();
        orphans.sort();
        orphans.dedup();
        if !orphans.is_empty() {
            row_limits.push(format!(
                "consequences name no alternative of the package: {orphans:?}"
            ));
        }
        let missing: Vec<&str> = alt_ids
            .iter()
            .copied()
            .filter(|a| !cons.iter().any(|c| c["alternative"] == json!(a)))
            .collect();
        if !missing.is_empty() {
            row_limits.push(format!("no consequence stated for: {missing:?}"));
        }
        // DV-3
        let file_ref = b["evidence"]["ref"].as_str().unwrap_or("");
        let now = observe_file(root, file_ref, &mut row_limits);
        let requested = ContentIdentity {
            method: b["evidence"]["method"].as_str().unwrap_or("").into(),
            value: b["evidence"]["claimedIdentity"]
                .as_str()
                .unwrap_or("")
                .into(),
        };
        let request_state = compare(
            &requested,
            now.identity
                .as_ref()
                .map(CurrentContent::Present)
                .unwrap_or(CurrentContent::Unavailable),
            false,
        );
        match request_state {
            Lapse::Unavailable => row_limits.push("package file not available: its current content is unknown".into()),
            Lapse::Incomparable => row_limits.push("package request identity method is incomparable with current observed method; historical identities are not relabelled".into()),
            Lapse::Lapsed => row_limits.push("package file differs from the content the request recorded".into()),
            _ => {},
        }
        // DV-4, DV-5
        let mut decided: Vec<&Value> = Vec::new();
        for a in acts
            .iter()
            .filter(|a| a["body"]["relations"]["requestRef"] == json!(pid))
        {
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
            "requestedBy": b["requester"].get("identity").cloned().unwrap_or(json!("requester identity not established")),
            "alternatives": alts.iter().map(|a| json!({
                "id": a["id"], "statement": a["statement"],
                "consequences": cons.iter().filter(|c| c["alternative"] == a["id"]).map(|c| c["statement"].clone()).collect::<Vec<_>>()
            })).collect::<Vec<_>>(),
            "state": "pending — awaiting the person's decision",
            "decision": Value::Null,
            "limits": [],
        });
        // DV-6: corrections replace what they correct; a later act supersedes an earlier one.
        let corrected: HashMap<String, String> = decided
            .iter()
            .filter_map(|a| {
                a["corrects"].as_str().map(|c| {
                    (
                        c.to_string(),
                        a["recordId"].as_str().unwrap_or("").to_string(),
                    )
                })
            })
            .collect();
        let current: Vec<&&Value> = decided
            .iter()
            .filter(|a| !corrected.contains_key(a["recordId"].as_str().unwrap_or("")))
            .collect();
        if let Some(a) = current.last() {
            let ab = &a["body"];
            let chosen = ab["relations"]["alternativeChosen"].as_str().unwrap_or("");
            let bound = identity(&ab["boundContent"][0]);
            let arid = a["recordId"].as_str().unwrap_or("");
            let expected_subject = format!("decision package {pid}");
            let expected_scope = b["scope"]
                .as_str()
                .filter(|s| !s.is_empty())
                .unwrap_or("not named by the package");
            let same_subject_scope = ab["actKind"] == "A16"
                && ab["boundSubject"]
                    .as_array()
                    .is_some_and(|v| v.len() == 1 && v[0] == expected_subject)
                && ab["boundContent"].as_array().is_some_and(|v| v.len() == 1)
                && ab["scope"] == expected_scope
                && ab["purpose"] == b["purpose"];
            let history = lapse_history(&entries, arid, &expected_subject, &bound);
            for e in entries.iter().filter(|e| {
                e["kind"] == "act_lapsed"
                    && e["body"]["act"]["recordId"] == arid
                    && matches!(
                        e["body"]["state"].as_str(),
                        Some("lapsed" | "lapsed (subject absent)" | "partially lapsed")
                    )
            }) {
                if !history.iter().any(|accepted| std::ptr::eq(*accepted, e)) {
                    row_limits.push(format!("{}: recorded lapse observation does not establish a comparable change on this bound referent; not used as lapse history", e["recordId"].as_str().unwrap_or("?")));
                }
            }
            let state = if !same_subject_scope {
                row_limits.push("recorded act subject/scope/purpose does not match this package request; standing incomparable".into());
                Lapse::Incomparable
            } else {
                let current = if let Some(c) = now.identity.as_ref() {
                    CurrentContent::Present(c)
                } else if now.absent {
                    CurrentContent::Absent
                } else {
                    CurrentContent::Unavailable
                };
                compare(&bound, current, !history.is_empty())
            };
            if state == Lapse::Incomparable {
                row_limits.push("recorded act and current file identity are incomparable; no lapse or current human-act standing established".into());
            }
            if !history.is_empty() {
                row_limits.push(
                    "lapse history is a recorded observation claim; native origin not verified"
                        .into(),
                );
            }
            let lapse = label(state);
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
                "captureProvenance": "recorded claim; native capture origin not verified by this unsealed reader",
                "captureEvidence": ab["captureEvidence"].as_array().map(|c| c.iter().map(|x| x["ref"].clone()).collect::<Vec<_>>()),
                "capturedAt": ab["captureTime"],
                "lapse": lapse,
                "standingComparison": {"bound": ab["boundContent"][0], "current": now.identity.as_ref().map(|c| json!({"method":c.method,"value":c.value})), "recordedSubjectScopeMatchesRequest": same_subject_scope},
                "lapseHistory": history.iter().map(|e| e["recordId"].clone()).collect::<Vec<_>>(),
                "lapseHistoryProvenance": "recorded observations; native origin not verified",
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
            if by_id
                .get(r)
                .map(|e| e["kind"] != "act_request")
                .unwrap_or(true)
            {
                limits.push(format!(
                    "{}: cites request {r}, which this record set does not hold",
                    a["recordId"].as_str().unwrap_or("")
                ));
            }
        }
    }
    json!({"view": "decision packages (DEL-06-02; derived, not authority)", "rows": rows, "limits": limits})
}
