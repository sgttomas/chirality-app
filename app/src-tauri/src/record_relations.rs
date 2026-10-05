//! RS W-3/R-6 correction projection from once-read, schema-checked claims.
//! No writer, native provenance/admission or general R-7 policy is introduced.
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet, HashSet};
use std::path::PathBuf;

pub fn read_logs(paths: &[PathBuf]) -> Value {
    let mut claims = Vec::new();
    let mut complete = HashSet::new();
    let mut read_limits = Vec::new();
    for path in paths {
        let log = path.to_string_lossy().into_owned();
        let (entries, limits) = crate::records::read_log(path);
        if limits.is_empty() {
            complete.insert(log.clone());
        }
        for record in entries {
            claims.push(json!({"source":{"log":log,"seq":record["seq"]},"record":record}));
        }
        read_limits.extend(limits);
    }
    let mut projected = project_from_read_claims(&claims, &complete);
    projected["readLimits"] = json!(read_limits);
    projected
}
fn reaches(edges: &BTreeMap<String, BTreeSet<String>>, from: &str, to: &str) -> bool {
    let mut todo = vec![from.to_owned()];
    let mut seen = BTreeSet::new();
    while let Some(at) = todo.pop() {
        if !seen.insert(at.clone()) {
            continue;
        }
        for next in edges.get(&at).into_iter().flatten() {
            if next == to {
                return true;
            }
            todo.push(next.clone());
        }
    }
    false
}
/// Display-source strings identify the supplied owning logs; no sorting supplies
/// precedence. Sorting output IDs only makes an inspectable deterministic list.
pub fn project_from_read_claims(claims: &[Value], complete_logs: &HashSet<String>) -> Value {
    let mut grouped: BTreeMap<String, Vec<&Value>> = BTreeMap::new();
    let mut diagnostics = Vec::new();
    for claim in claims {
        let record = &claim["record"];
        if let Err(error) = crate::schema_validation::bundled().and_then(|v| v.validate(record)) {
            diagnostics.push(
                json!({"recordId":record["recordId"],"state":"nonconformant","reason":error}),
            );
            continue;
        }
        if let Some(id) = record["recordId"].as_str() {
            grouped.entry(id.into()).or_default().push(claim);
        }
    }
    let conflicts: BTreeSet<_> = grouped
        .iter()
        .filter(|(_, copies)| copies.iter().any(|c| c["record"] != copies[0]["record"]))
        .map(|(id, _)| id.clone())
        .collect();
    let mut links = BTreeMap::new();
    let mut refused = BTreeMap::new();
    for (id, copies) in &grouped {
        if conflicts.contains(id) {
            refused.insert(id.clone(), "conflicting record identity");
            continue;
        }
        let record = &copies[0]["record"];
        let Some(target) = record["corrects"].as_str() else {
            continue;
        };
        let reason = record["correctionReason"]
            .as_str()
            .is_some_and(|r| !r.is_empty());
        let Some(target_copies) = grouped.get(target) else {
            refused.insert(id.clone(), "unresolvable correction target");
            continue;
        };
        if conflicts.contains(target) {
            refused.insert(id.clone(), "ambiguous correction target identity");
            continue;
        }
        if !reason || record["kind"] != target_copies[0]["record"]["kind"] {
            refused.insert(
                id.clone(),
                "nonconformant correction: reason/same-kind rule",
            );
            continue;
        }
        if id == target {
            refused.insert(id.clone(), "self correction relation");
            continue;
        }
        if copies.len() == 1
            && target_copies.len() == 1
            && copies[0]["source"]["log"] == target_copies[0]["source"]["log"]
            && record["seq"].as_u64() <= target_copies[0]["record"]["seq"].as_u64()
        {
            refused.insert(id.clone(), "contradictory owning-log correction order");
            continue;
        }
        links.insert(id.clone(), target.to_owned());
    }
    for id in links.keys() {
        let mut at = id.as_str();
        let mut visited = BTreeSet::new();
        while let Some(target) = links.get(at) {
            if !visited.insert(at.to_owned()) {
                for member in visited {
                    refused.insert(member, "cyclic correction dependency");
                }
                break;
            }
            at = target;
        }
    }
    let mut edges: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    let mut corrected: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    for (id, target) in &links {
        if refused.contains_key(id) || refused.contains_key(target) {
            continue;
        }
        edges.entry(target.clone()).or_default().insert(id.clone());
        corrected
            .entry(target.clone())
            .or_default()
            .insert(id.clone());
    }
    for (a, target_a) in &links {
        for (b, target_b) in &links {
            if a == b || target_a != target_b || refused.contains_key(a) || refused.contains_key(b)
            {
                continue;
            }
            let (aa, bb) = (&grouped[a], &grouped[b]);
            if aa.len() == 1
                && bb.len() == 1
                && aa[0]["source"]["log"] == bb[0]["source"]["log"]
                && complete_logs.contains(aa[0]["source"]["log"].as_str().unwrap_or(""))
                && aa[0]["record"]["seq"].as_u64() < bb[0]["record"]["seq"].as_u64()
            {
                edges.entry(a.clone()).or_default().insert(b.clone());
            }
        }
    }
    // Weak correction components retain original plus every readable correction.
    let mut visited = BTreeSet::new();
    let mut groups = Vec::new();
    for id in grouped.keys() {
        if visited.contains(id) {
            continue;
        }
        let mut todo = vec![id.clone()];
        let mut members = BTreeSet::new();
        while let Some(at) = todo.pop() {
            if !members.insert(at.clone()) {
                continue;
            }
            for (correction, target) in &links {
                if correction == &at {
                    todo.push(target.clone());
                }
                if target == &at {
                    todo.push(correction.clone());
                }
            }
        }
        visited.extend(members.clone());
        let mut current: Vec<_> = members
            .iter()
            .filter(|a| {
                !refused.contains_key(*a)
                    && !members.iter().any(|b| a != &b && reaches(&edges, a, b))
            })
            .cloned()
            .collect();
        if members.iter().any(|id| refused.contains_key(id)) {
            current.clear();
        }
        let incomplete = members.iter().any(|id| {
            grouped[id]
                .iter()
                .any(|c| !complete_logs.contains(c["source"]["log"].as_str().unwrap_or("")))
        });
        groups.push(json!({"recordIds":members,"currentCandidates":current,"resolution":if current.len()==1{"unique recorded correction/claim"}else if current.len()>1{"ambiguous/unresolved correction branches"}else{"unresolvable correction relation"},"sourceIncomplete":incomplete,"provenance":"recorded claims; no native origin or human chronology verified"}));
    }
    for (id, reason) in &refused {
        diagnostics.push(json!({"recordId":id,"state":if reason.starts_with("nonconformant"){"nonconformant"}else{"unresolved relation"},"reason":reason}));
    }
    let projections:Vec<_>=claims.iter().map(|claim| {
        let id=claim["record"]["recordId"].as_str().unwrap_or("");
        json!({"record":claim["record"],"source":claim["source"],"correctedBy":corrected.get(id).cloned().unwrap_or_default(),"relationLimit":refused.get(id),"identityResolution":if conflicts.contains(id){"conflicting identity"}else if grouped.get(id).is_some_and(|v|v.len()>1){"one unchanged claim; identical sources retained"}else{"unique readable identity"},"provenance":"recorded claim; not verified native evidence"})
    }).collect();
    json!({"view":"RS W-3/R-6 correction relations; derived, not authority","claims":projections,"correctionGroups":groups,"diagnostics":diagnostics,"scope":"same-kind correction relations only; other R-7 rules/admission remain with owning consumers"})
}
