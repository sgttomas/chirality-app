//! Decision view model, derived from files only.
//!
//! DEL-06-02 DECISION_VIEW.md (DV-v0.1) §3 DV-1…DV-9, §4 row states, §6 failure
//! behaviour. A port of the Pass 4 prototype `E/decision_view.py`. It reads the RS
//! log and the package files the records cite; it writes nothing (DV-9).

#[path = "record_relations.rs"]
pub mod record_relations;

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
    unresolved: &HashSet<String>,
) -> Vec<&'a Value> {
    entries
        .iter()
        .filter(|e| {
            let b = &e["body"];
            e["kind"] == "act_lapsed"
                && !unresolved.contains(e["recordId"].as_str().unwrap_or(""))
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

fn same_capture(a: &Value, b: &Value) -> bool {
    let refs = |e: &Value| {
        e["body"]["captureEvidence"]
            .as_array()
            .map(|v| {
                v.iter()
                    .filter_map(|x| x["ref"].as_str().map(str::to_owned))
                    .collect::<HashSet<_>>()
            })
            .unwrap_or_default()
    };
    let a = refs(a);
    let b = refs(b);
    !a.is_empty() && a == b
}
fn reported_native_observation(e: &Value) -> bool {
    e["kind"] == "human_act"
        && e["body"]["actKind"] == "A16"
        && e["body"]["recordingMode"] == "direct capture"
        && e["recorder"]["role"] == records::APP_INTERFACE.role
        && e["recorder"]["identity"] == records::APP_INTERFACE.identity
        && e["observedAt"]
            .as_str()
            .is_some_and(|at| !at.is_empty() && e["body"]["captureTime"] == at)
}
fn same_capture_facts(a: &Value, b: &Value) -> bool {
    [
        "actKind",
        "actClass",
        "decisionActor",
        "boundSubject",
        "boundContent",
        "scope",
        "purpose",
        "captureTime",
    ]
    .iter()
    .all(|key| a["body"][key] == b["body"][key])
        && a["body"]["relations"]["requestRef"] == b["body"]["relations"]["requestRef"]
        && a["body"]["relations"]["alternativeChosen"]
            == b["body"]["relations"]["alternativeChosen"]
}
fn reaches(from: &str, target: &str, edges: &HashMap<String, Vec<String>>) -> bool {
    let mut todo = vec![from.to_owned()];
    let mut seen = HashSet::new();
    while let Some(at) = todo.pop() {
        if !seen.insert(at.clone()) {
            continue;
        }
        if let Some(next) = edges.get(&at) {
            if next.iter().any(|v| v == target) {
                return true;
            }
            todo.extend(next.iter().cloned());
        }
    }
    false
}

pub fn derive(root: &Path, record_paths: &[&str]) -> Value {
    let mut entries = Vec::new();
    let mut limits: Vec<String> = Vec::new();
    // Owning-log provenance is retained for observation order, never performance order.
    let paths = if record_paths.is_empty() {
        match crate::storage::discover(root) {
            Ok(paths) => paths,
            Err(e) => {
                limits.push(e);
                Vec::new()
            }
        }
    } else {
        record_paths.iter().map(|rp| root.join(rp)).collect()
    };
    let mut sources: HashMap<String, Vec<Value>> = HashMap::new();
    let mut source_claims = Vec::new();
    let mut complete_logs = HashSet::new();
    for path in paths {
        if let Err(e) = crate::storage::check_path(&path) {
            limits.push(e);
            continue;
        }
        let (read, found_limits) = records::read_log(&path);
        let log = path
            .strip_prefix(root)
            .unwrap_or(&path)
            .to_string_lossy()
            .into_owned();
        if found_limits.is_empty() {
            complete_logs.insert(log.clone());
        }
        for e in &read {
            source_claims.push(json!({"record":e,"source":{"log":log,"seq":e["seq"]}}));
            if let Some(id) = e["recordId"].as_str() {
                sources
                    .entry(id.to_owned())
                    .or_default()
                    .push(json!({"log":log,"seq":e["seq"]}));
            }
        }
        entries.extend(read);
        limits.extend(found_limits);
    }
    let record_corrections = record_relations::project_from_read_claims(&source_claims, &complete_logs);
    let mut grouped: HashMap<String, Vec<&Value>> = HashMap::new();
    for e in &entries {
        if let Some(id) = e["recordId"].as_str() {
            grouped.entry(id.to_owned()).or_default().push(e);
        }
    }
    let duplicates: HashSet<String> = grouped
        .iter()
        .filter(|(_, v)| v.iter().any(|e| *e != v[0]))
        .map(|(id, _)| id.clone())
        .collect();
    for (id, values) in &grouped {
        if values.len() > 1 && !duplicates.contains(id) {
            limits.push(format!(
                "identical copies of record {id}; one unchanged claim, all sources retained"
            ));
        }
    }
    for id in &duplicates {
        limits.push(format!("ambiguous duplicate record identity: {id}"));
    }
    let by_id: HashMap<String, &Value> = entries
        .iter()
        .filter_map(|e| {
            let id = e["recordId"].as_str()?;
            (!duplicates.contains(id)).then_some((id.to_owned(), e))
        })
        .collect();
    let mut invalid_corrections = HashSet::new();
    let mut correction_links: HashMap<String, String> = HashMap::new();
    for e in &entries {
        let Some(target) = e["corrects"].as_str() else {
            continue;
        };
        let id = e["recordId"].as_str().unwrap_or("");
        let reason = e["correctionReason"]
            .as_str()
            .is_some_and(|v| !v.is_empty());
        let target_entry = by_id.get(target);
        let same_kind = target_entry.is_some_and(|t| t["kind"] == e["kind"]);
        let contradicted_log_order =
            sources
                .get(id)
                .zip(sources.get(target))
                .is_some_and(|(a, b)| {
                    a.len() == 1
                        && b.len() == 1
                        && a[0]["log"] == b[0]["log"]
                        && a[0]["seq"].as_u64() <= b[0]["seq"].as_u64()
                });
        if duplicates.contains(id)
            || !reason
            || !same_kind
            || id == target
            || contradicted_log_order
        {
            invalid_corrections.insert(id.to_owned());
            limits.push(format!("{id}: correction target {target} unresolvable/ambiguous, wrong kind, missing reason or contradictory relation; not applied"));
        } else {
            correction_links.insert(id.to_owned(), target.to_owned());
        }
    }
    // Explicit links must not form a cycle, including cycles spanning independent logs.
    for id in correction_links.keys() {
        let mut seen = HashSet::new();
        let mut at = id.as_str();
        while let Some(target) = correction_links.get(at) {
            if !seen.insert(at.to_owned()) {
                invalid_corrections.extend(seen);
                limits.push(format!("{id}: cyclic correction relation; not applied"));
                break;
            }
            at = target;
        }
    }
    let mut edges: HashMap<String, Vec<String>> = HashMap::new();
    let mut corrected: HashMap<String, Vec<String>> = HashMap::new();
    for (id, target) in &correction_links {
        if !invalid_corrections.contains(id) && !invalid_corrections.contains(target) {
            edges.entry(target.clone()).or_default().push(id.clone());
            corrected
                .entry(target.clone())
                .or_default()
                .push(id.clone());
        }
    }
    // Same-stream corrections of a common target may order recorded corrections.
    // This rule never orders separate human performances or uses a wall clock.
    for (a, target_a) in &correction_links {
        for (b, target_b) in &correction_links {
            if a == b
                || target_a != target_b
                || invalid_corrections.contains(a)
                || invalid_corrections.contains(b)
            {
                continue;
            }
            if let Some((sa, sb)) = sources.get(a).zip(sources.get(b)) {
                if sa.len() == 1
                    && sb.len() == 1
                    && sa[0]["log"] == sb[0]["log"]
                    && complete_logs.contains(sa[0]["log"].as_str().unwrap_or(""))
                    && sa[0]["seq"].as_u64() < sb[0]["seq"].as_u64()
                {
                    edges.entry(a.clone()).or_default().push(b.clone());
                }
            }
        }
    }
    // P0's admitted native writer queue preserves original capture observation order,
    // including late writes before fresh continuation. Consume that bounded reported
    // stream contract, not mere seq or clock comparison, and never verify native origin.
    let mut admission_order = Vec::new();
    for a in &entries {
        for b in &entries {
            let aid = a["recordId"].as_str().unwrap_or("");
            let bid = b["recordId"].as_str().unwrap_or("");
            if aid == bid
                || duplicates.contains(aid)
                || duplicates.contains(bid)
                || a.get("corrects").is_some()
                || b.get("corrects").is_some()
                || !reported_native_observation(a)
                || !reported_native_observation(b)
                || same_capture(a, b)
                || a["body"]["relations"]["requestRef"] != b["body"]["relations"]["requestRef"]
            {
                continue;
            }
            if let Some((sa, sb)) = sources.get(aid).zip(sources.get(bid)) {
                if sa.len() == 1
                    && sb.len() == 1
                    && sa[0]["log"] == sb[0]["log"]
                    && complete_logs.contains(sa[0]["log"].as_str().unwrap_or(""))
                    && sa[0]["seq"].as_u64() < sb[0]["seq"].as_u64()
                {
                    edges
                        .entry(aid.to_owned())
                        .or_default()
                        .push(bid.to_owned());
                    admission_order.push(json!({"before":aid,"after":bid,"source":"reported ordered native capture admission stream (P0); not native-origin verification"}));
                }
            }
        }
    }
    // A separately stated supersession link is evidence of a recorded relation,
    // not native verification. A repeated capture is never a later performance.
    for e in &entries {
        let Some(target) = e["body"]["relations"]["supersededBy"].as_str() else {
            continue;
        };
        let id = e["recordId"].as_str().unwrap_or("");
        if let Some(t) = by_id.get(target) {
            if !duplicates.contains(id)
                && id != target
                && e["kind"] == "human_act"
                && t["kind"] == e["kind"]
                && e["body"]["actKind"] == t["body"]["actKind"]
                && e["body"]["relations"]["requestRef"] == t["body"]["relations"]["requestRef"]
                && !same_capture(e, t)
            {
                edges
                    .entry(id.to_owned())
                    .or_default()
                    .push(target.to_owned());
                continue;
            }
        }
        limits.push(format!("{id}: supersession target {target} unresolvable/ambiguous or not a distinct compatible capture; not applied"));
    }
    // Contradictory precedence cannot erase either contender.
    let cyclic: HashSet<String> = edges
        .keys()
        .filter(|id| {
            edges
                .get(*id)
                .is_some_and(|next| next.iter().any(|n| reaches(n, id, &edges)))
        })
        .cloned()
        .collect();
    for id in &cyclic {
        limits.push(format!(
            "{id}: cyclic precedence; current relation unresolved"
        ));
    }
    edges.retain(|id, _| !cyclic.contains(id));
    for next in edges.values_mut() {
        next.retain(|id| !cyclic.contains(id));
    }
    let unresolved_observations: HashSet<String> = duplicates
        .iter()
        .chain(invalid_corrections.iter())
        .chain(cyclic.iter())
        .cloned()
        .collect();
    // DV-1: a row per act_request that carries alternatives.
    let mut seen_packages = HashSet::new();
    let packages: Vec<&Value> = entries
        .iter()
        .filter(|e| e["kind"] == "act_request" && e["body"].get("alternatives").is_some())
        .filter(|e| {
            duplicates.contains(e["recordId"].as_str().unwrap_or(""))
                || seen_packages.insert(e["recordId"].as_str().unwrap_or("").to_owned())
        })
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
        let mut seen_acts = HashSet::new();
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
            if duplicates.contains(rid) || seen_acts.insert(rid.to_owned()) {
                decided.push(a);
            }
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
            "requestResolution": if duplicates.contains(pid) { "conflicting identity" } else if sources.get(pid).is_some_and(|v|v.len()>1) { "unique claim (identical copies)" } else { "unique claim" },
            "requestSources": sources.get(pid),
            "limits": [],
        });
        // Retain a projection for each readable claim, including unresolved corrections.
        let mut projections = Vec::new();
        for a in &decided {
            let claim_limit_start = row_limits.len();
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
            let history_records: Vec<&str> = decided
                .iter()
                .filter(|other| same_capture(a, other) && same_capture_facts(a, other))
                .filter_map(|other| other["recordId"].as_str())
                .collect();
            let history: Vec<&Value> = history_records
                .iter()
                .flat_map(|id| {
                    lapse_history(
                        &entries,
                        id,
                        &expected_subject,
                        &bound,
                        &unresolved_observations,
                    )
                })
                .collect();
            let mut history_refs = history
                .iter()
                .map(|e| e["recordId"].clone())
                .collect::<Vec<_>>();
            history_refs.sort_by(|a, b| a.as_str().cmp(&b.as_str()));
            history_refs.dedup(); // identity display only
            let observation_claims: Vec<Value> = source_claims
                .iter()
                .filter(|c| {
                    c["record"]["kind"] == "act_lapsed"
                        && history_records
                            .iter()
                            .any(|id| c["record"]["body"]["act"]["recordId"] == *id)
                })
                .map(|c| {
                    let mut claim = c.clone();
                    claim["resolution"] = json!(if unresolved_observations
                        .contains(c["record"]["recordId"].as_str().unwrap_or(""))
                    {
                        "unknown/unresolvable observation identity or relation"
                    } else {
                        "unique recorded observation claim"
                    });
                    claim
                })
                .collect();
            let history_incomplete = observation_claims.iter().any(|c| {
                unresolved_observations.contains(c["record"]["recordId"].as_str().unwrap_or(""))
            });
            // A separate resolved witness establishes existential prior lapse even
            // when another observation is unresolved; it does not complete history.
            let history_unknown = history_incomplete && history.is_empty();
            if history_unknown {
                row_limits.push(format!("{arid}: past lapse history unknown; observation identity/relation is unresolved, current content is reported separately"));
            } else if history_incomplete {
                row_limits.push(format!("{arid}: prior lapse has an independent resolved recorded witness; total history remains incomplete with unresolved observations"));
            }
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
            let current_content = now
                .identity
                .as_ref()
                .map(CurrentContent::Present)
                .unwrap_or(if now.absent {
                    CurrentContent::Absent
                } else {
                    CurrentContent::Unavailable
                });
            let current_relation = if !same_subject_scope {
                "incomparable subject/scope"
            } else {
                match compare(&bound, current_content, false) {
                    Lapse::NotLapsed => "matches bound content",
                    Lapse::Lapsed => "differs from bound content",
                    Lapse::SubjectAbsent => "subject absent",
                    Lapse::Incomparable => "incomparable content method",
                    _ => "current content unavailable",
                }
            };
            let lapse = if history_unknown {
                "unknown (lapse history unresolved)"
            } else {
                label(state)
            };
            let projection = json!({
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
                "lapseHistory": history_refs,
                "lapseHistoryProvenance": "recorded observations; native origin not verified",
                "historyResolution": if history_unknown {"unknown/unresolvable past observation"} else if history_incomplete {"established prior lapse; history incomplete"} else {"resolved recorded history"},
                "historyIncomplete": history_incomplete,
                "lapseObservationClaims": observation_claims,
                "historyRecordRefs": history_records,
                "currentContentComparison": current_relation,
                "recordSources": sources.get(arid),
                "recordedAt": a["writtenAt"],
                "observedAt": a.get("observedAt"),
                "orderingMeaning": "recorded observations; entry order alone does not establish human performance chronology",
                "correctionTarget": a.get("corrects"),
                "correctedBy": corrected.get(arid),
                "relationUnresolved": duplicates.contains(arid) || invalid_corrections.contains(arid) || cyclic.contains(arid),
                "claimLimits": &row_limits[claim_limit_start..],
            });
            projections.push(projection);
        }
        let eligible: Vec<&Value> = decided
            .iter()
            .copied()
            .filter(|a| {
                let id = a["recordId"].as_str().unwrap_or("");
                !duplicates.contains(id)
                    && !invalid_corrections.contains(id)
                    && !cyclic.contains(id)
            })
            .collect();
        let maxima: Vec<&Value> = eligible
            .iter()
            .copied()
            .filter(|a| {
                !eligible.iter().any(|b| {
                    a["recordId"] != b["recordId"]
                        && reaches(
                            a["recordId"].as_str().unwrap_or(""),
                            b["recordId"].as_str().unwrap_or(""),
                            &edges,
                        )
                })
            })
            .collect();
        let conflict = maxima.iter().enumerate().any(|(i, a)| {
            maxima
                .iter()
                .skip(i + 1)
                .any(|b| same_capture(a, b) && !same_capture_facts(a, b))
        });
        if conflict {
            row_limits.push("recorders disagree: one capture has incompatible readable claims, not later performances".into());
        }
        let unresolved = decided.iter().any(|a| {
            duplicates.contains(a["recordId"].as_str().unwrap_or(""))
                || cyclic.contains(a["recordId"].as_str().unwrap_or(""))
        }) || duplicates.contains(pid);
        let equivalent_capture = !maxima.is_empty()
            && maxima
                .iter()
                .all(|a| same_capture(a, maxima[0]) && same_capture_facts(a, maxima[0]));
        if !decided.is_empty()
            && (unresolved || maxima.is_empty() || (maxima.len() != 1 && !equivalent_capture))
        {
            row["state"] = json!("ambiguous current standing");
            row_limits.push("ambiguous/unresolved current recorded claims; no warranted total order or later human performance".into());
        } else if let Some(current) = maxima
            .iter()
            .find(|a| a["body"]["recordingMode"] == "direct capture")
            .or_else(|| maxima.first())
        {
            row["state"] = json!("decided");
            let id = current["recordId"].as_str().unwrap_or("");
            let mut projection = projections
                .iter()
                .find(|p| p["act"] == id)
                .cloned()
                .unwrap();
            if equivalent_capture && maxima.len() > 1 {
                let direct_count = maxima
                    .iter()
                    .filter(|a| a["body"]["recordingMode"] == "direct capture")
                    .count();
                if direct_count != 1 {
                    projection["act"] = Value::Null;
                    projection["recordedBy"] =
                        json!("multiple records of the same capture; see contenders");
                    projection["recordedAt"] = Value::Null;
                    projection["observedAt"] = Value::Null;
                    projection["recordSources"] = json!(maxima
                        .iter()
                        .flat_map(|a| sources
                            .get(a["recordId"].as_str().unwrap_or(""))
                            .into_iter()
                            .flatten()
                            .cloned())
                        .collect::<Vec<_>>());
                }
            }
            let mut equivalent_ids = maxima
                .iter()
                .map(|a| a["recordId"].clone())
                .collect::<Vec<_>>();
            equivalent_ids.sort_by(|a, b| a.as_str().cmp(&b.as_str())); // display only; never precedence
            projection["orderingEvidence"] = json!(admission_order
                .iter()
                .filter(|w| maxima.iter().any(|a| a["recordId"] == w["after"]))
                .collect::<Vec<_>>());
            projection["equivalentCaptureRecords"] = json!(equivalent_ids);
            if equivalent_capture && maxima.len() > 1 {
                let mut histories = projections
                    .iter()
                    .filter(|p| maxima.iter().any(|a| a["recordId"] == p["act"]))
                    .flat_map(|p| p["lapseHistory"].as_array().unwrap().iter().cloned())
                    .collect::<Vec<_>>();
                histories.sort_by(|a, b| a.as_str().cmp(&b.as_str()));
                histories.dedup();
                projection["lapseHistory"] = json!(histories);
                let past_incomplete = projections.iter().any(|p| {
                    maxima.iter().any(|a| a["recordId"] == p["act"])
                        && p["historyIncomplete"] == true
                });
                let past_unknown =
                    past_incomplete && projection["lapseHistory"].as_array().unwrap().is_empty();
                projection["historyIncomplete"] = json!(past_incomplete);
                projection["lapseObservationClaims"] = json!(projections
                    .iter()
                    .filter(|p| maxima.iter().any(|a| a["recordId"] == p["act"]))
                    .flat_map(|p| p["lapseObservationClaims"]
                        .as_array()
                        .unwrap()
                        .iter()
                        .cloned())
                    .collect::<Vec<_>>());
                if past_unknown {
                    projection["historyResolution"] =
                        json!("unknown/unresolvable past observation");
                    projection["lapse"] = json!("unknown (lapse history unresolved)");
                } else if past_incomplete {
                    projection["historyResolution"] =
                        json!("established prior lapse; history incomplete");
                }
                // The facts agree; one capture's history may be linked through either record.
                let bound = identity(&current["body"]["boundContent"][0]);
                let current_content = now
                    .identity
                    .as_ref()
                    .map(CurrentContent::Present)
                    .unwrap_or(if now.absent {
                        CurrentContent::Absent
                    } else {
                        CurrentContent::Unavailable
                    });
                if !past_unknown
                    && projection["standingComparison"]["recordedSubjectScopeMatchesRequest"]
                        == true
                {
                    projection["lapse"] = json!(label(compare(
                        &bound,
                        current_content,
                        !projection["lapseHistory"].as_array().unwrap().is_empty()
                    )));
                }
            }
            projection["earlierActs"] = json!(decided.iter().filter(|a| a["recordId"]!=current["recordId"]).map(|a| {
                let aid=a["recordId"].as_str().unwrap_or("");
                let relation=if corrected.get(aid).is_some_and(|v|v.iter().any(|cid| reaches(cid,id,&edges) || cid==id)) { format!("corrected by {id}") }
                    else if reaches(aid,id,&edges) { if admission_order.iter().any(|w|w["before"]==aid && w["after"]==id) {format!("superseded by {id} (reported ordered native admission stream; origin unverified)")} else {format!("superseded by {id} (explicit recorded relation)")} }
                    else if same_capture(a,current) && same_capture_facts(a,current) { "same capture recorded again; not a later performance".into() }
                    else { "unresolved relation; claim retained".into() };
                json!({"act":aid,"relation":relation,"alternativeChosen":a["body"]["relations"]["alternativeChosen"]})
            }).collect::<Vec<_>>());
            row["decision"] = projection;
        }
        if duplicates.contains(pid) {
            row["state"] = json!("unresolvable request identity");
            row["decision"] = Value::Null;
            row_limits.push("request record identity has conflicting facts; no unique package/offer binding resolved".into());
        }
        row["currentCandidates"] = json!(maxima
            .iter()
            .map(|a| a["recordId"].clone())
            .collect::<Vec<_>>());
        row["contenders"] = json!(projections);
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
    json!({"view": "decision packages (DEL-06-02; derived, not authority)", "rows": rows, "recordCorrections":record_corrections, "limits": limits, "unresolvedRecords": entries.iter().filter(|e| duplicates.contains(e["recordId"].as_str().unwrap_or("")) || invalid_corrections.contains(e["recordId"].as_str().unwrap_or(""))).collect::<Vec<_>>()})
}
