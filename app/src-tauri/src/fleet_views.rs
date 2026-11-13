//! DEL-06-01 RF facts and DEL-06-02 FV views over one stable, once-read packet.
//! No writer, native identity join, or human-act admission. A dispatch is read
//! only from the App's own recorded observation and its recorded association.
use super::{Census, LogRead, Row, FOLDER, OBSERVED};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::path::{Component, Path};
use std::sync::OnceLock;

pub(super) struct Input {
    bytes: Option<Vec<u8>>,
    observation: Value,
}
type Inputs = BTreeMap<(String, String), Input>;
fn text(v: &Value) -> &str {
    v.as_str().unwrap_or("")
}
fn array(v: &Value) -> &[Value] {
    v.as_array().map(Vec::as_slice).unwrap_or(&[])
}
fn actor(v: &Value) -> String {
    let who = v["identity"].as_str().unwrap_or("not recorded");
    if v["kind"] == "person" && v["identityVerified"] != true {
        format!("{who} (identity not verified)")
    } else {
        who.into()
    }
}
fn standing_validator() -> Result<&'static jsonschema::Validator, String> {
    static V: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
    V.get_or_init(|| {
        let id = "urn:chirality:app-v4:del-07-02:connector-standing:0.1";
        crate::schema_validation::compile_targets(
            &[(
                "connector.standing.schema.json",
                include_str!("../resources/connector_route/connector.standing.schema.json"),
            )],
            &[id],
            &[&format!("{id}#/$defs/standing")],
        )
        .map(|mut v| v.remove(0))
    })
    .as_ref()
    .map_err(Clone::clone)
}

fn connector(need: &Value, bytes: &[u8]) -> Value {
    let unknown = |why: String| json!({"state":"unknown","why":why});
    let Ok(record) = serde_json::from_slice::<Value>(bytes) else {
        return unknown("connector receiving record is unreadable JSON".into());
    };
    let Ok(validator) = standing_validator() else {
        return unknown("connector standing reader unavailable".into());
    };
    let st = &record["response_standing"];
    if validator.validate(st).is_err() || st["connector"] != need["connector"] {
        return unknown("connector standing does not conform or names another connector".into());
    }
    let mut unrelied = Vec::new();
    let mut advisory = Vec::new();
    if !record["claims"].is_null() && !record["claims"].is_array() {
        return unknown("connector claims are unreadable".into());
    }
    for claim in array(&record["claims"]) {
        let cs = &claim["standing"];
        let name = claim["claim_id"].as_str().unwrap_or("unnamed claim");
        if validator.validate(cs).is_err() || cs["connector"] != need["connector"] {
            unrelied.push(format!(
                "{name}: standing unreadable, nonconformant or another connector"
            ));
        } else if cs["supports_reliance"] != true {
            if cs["claim_tier"] == "presence_advisory" {
                advisory.push(name.to_owned());
            } else {
                unrelied.push(format!("{name}: {}", text(&cs["condition"])));
            }
        }
    }
    let route = &record["route"];
    let route_usable =
        route["needed"] == true && route["account_ref"].as_str().is_some_and(|s| !s.is_empty());
    let relies = st["supports_reliance"] == true;
    let state = if relies
        && ((!unrelied.is_empty() && !route_usable) || (route["needed"] == true && !route_usable))
    {
        "unknown"
    } else if relies {
        "satisfied"
    } else if st["condition"] == "unknown" {
        "unknown"
    } else {
        "outstanding"
    };
    let mut why = format!(
        "connector {}: envelope {}, condition {}, tier {}; receiving record {} reports reliance {}",
        text(&need["connector"]),
        text(&st["envelope"]),
        text(&st["condition"]),
        text(&st["claim_tier"]),
        record["record_id"].as_str().unwrap_or(text(&need["ref"])),
        if relies { "supported" } else { "not supported" }
    );
    if !unrelied.is_empty() {
        why.push_str(&format!("; claims not relied: {}", unrelied.join(", ")));
    }
    if !advisory.is_empty() {
        why.push_str(&format!("; advisory only: {}", advisory.join(", ")));
    }
    if route_usable {
        why.push_str(&format!(
            "; source-file route {} still needed for uncovered parts",
            text(&route["account_ref"])
        ));
    }
    if state == "unknown" && relies {
        why.push_str("; required source-file route not established");
    }
    json!({"state":state,"why":why,"connectorNeed":true,"record":record["record_id"],
        "standing":st,"route":route,"unreliedClaims":unrelied,"advisoryClaims":advisory,
        "provenance":"receiving-file claim; no live connector adoption or source truth established"})
}

/// References are relative to the fixed Fleet folder, never arbitrary host paths.
/// All source bytes and absent leaves join the existing whole-packet census.
pub(super) fn read_inputs(census: &mut Census, root: &Path, graphs: &[Row]) -> Inputs {
    let mut out = Inputs::new();
    for graph in graphs {
        for item in array(&graph.record["body"]["items"]) {
            for need in array(&item["needs"]) {
                let kind = text(&need["kind"]);
                if !matches!(kind, "input" | "connector") {
                    continue;
                }
                let reference = text(&need["ref"]);
                let key = (kind.to_owned(), reference.to_owned());
                // Connector declarations may disagree, so cache raw observations,
                // not a conclusion derived under the first declaration.
                if out.contains_key(&key) {
                    continue;
                }
                let rel = Path::new(reference);
                let mut observed_bytes = None;
                let value = if reference.is_empty()
                    || rel.is_absolute()
                    || rel.components().any(|p| !matches!(p, Component::Normal(_)))
                {
                    json!({"state":"unknown","why":"input reference is not a contained Fleet-relative path"})
                } else {
                    let path = root.join(FOLDER).join(rel);
                    // Retain ancestor identities as well as the leaf. Neither
                    // links nor a swapped directory may reassign this snapshot.
                    let mut ancestor = path.parent();
                    let mut error = None;
                    while let Some(dir) = ancestor.filter(|d| d.starts_with(root)) {
                        if let Err(e) = census.metadata(dir) {
                            error = Some(e);
                            break;
                        }
                        ancestor = dir.parent();
                    }
                    match error.map_or_else(|| census.read(&path), Err) {
                        Ok(Some(bytes)) => {
                            let source = json!({"home":"selected project","path":format!("{FOLDER}/{reference}"),
                                "content":{"method":crate::util::FILE_IDENTITY_METHOD,"value":crate::util::sha256_hex(&bytes)}});
                            observed_bytes = Some(bytes);
                            json!({"state":"read","source":source})
                        }
                        Ok(None) => json!({"state":"outstanding","why":"input file not present"}),
                        Err(reason) => {
                            json!({"state":"unknown","why":format!("input unreadable: {reason}")})
                        }
                    }
                };
                out.insert(
                    key,
                    Input {
                        bytes: observed_bytes,
                        observation: value,
                    },
                );
            }
        }
    }
    out
}

fn need_input(need: &Value, inputs: &Inputs) -> Value {
    let key = (
        text(&need["kind"]).to_owned(),
        text(&need["ref"]).to_owned(),
    );
    let Some(input) = inputs.get(&key) else {
        return json!({"state":"unknown","why":"input was not observed"});
    };
    let observation = &input.observation;
    let Some(bytes) = input.bytes.as_deref() else {
        return observation.clone();
    };
    let mut state = if need["kind"] == "connector" {
        connector(need, bytes)
    } else if serde_json::from_slice::<Value>(bytes)
        .ok()
        .is_some_and(|v| v.get("response_standing").is_some())
    {
        json!({"state":"unknown","why":"connector receiving record named as a plain input; declare a connector need"})
    } else {
        json!({"state":"satisfied","why":"input file present and readable; its content is quoted, not validated as true"})
    };
    state["source"] = observation["source"].clone();
    state
}

/// A correction is a new same-kind claim in this undertaking. Ambiguous,
/// forward, cross-kind or missing targets qualify the complete projection.
fn active<'a>(rows: &[&'a Row], duplicates: &BTreeSet<String>) -> (Vec<&'a Row>, Vec<String>) {
    let mut corrected = BTreeSet::new();
    let mut refused = BTreeSet::new();
    let mut notes = Vec::new();
    let mut targets: BTreeMap<&str, usize> = BTreeMap::new();
    for row in rows {
        if let Some(target) = row.record["corrects"].as_str() {
            *targets.entry(target).or_default() += 1;
        }
    }
    for (index, row) in rows.iter().enumerate() {
        if duplicates.contains(row.id()) {
            refused.insert(row.id());
        }
        let Some(target) = row.record["corrects"].as_str() else {
            continue;
        };
        if targets[target] != 1
            || row.record["correctionReason"]
                .as_str()
                .is_none_or(str::is_empty)
            || !rows[..index]
                .iter()
                .any(|old| old.id() == target && old.kind() == row.kind())
            || duplicates.contains(target)
            || refused.contains(target)
        {
            refused.insert(row.id());
            notes.push(format!(
                "{}: correction target/reason/order is unresolved; no state promotion",
                row.id()
            ));
        } else {
            corrected.insert(target);
        }
    }
    // Conflicting corrections cannot leave the original looking current.
    for (target, count) in targets {
        if count > 1 {
            refused.insert(target);
        }
    }
    (
        rows.iter()
            .copied()
            .filter(|r| !corrected.contains(r.id()) && !refused.contains(r.id()))
            .collect(),
        notes,
    )
}

fn event<'a>(rows: &[&'a Row], kind: &str, item: &str) -> Option<&'a Row> {
    rows.iter()
        .rev()
        .copied()
        .find(|r| r.kind() == kind && r.record["body"]["workItem"] == item)
}
fn return_events<'a>(rows: &[&'a Row], kind: &str, item: &str, ret: &str) -> Option<&'a Row> {
    rows.iter().rev().copied().find(|r| {
        r.kind() == kind
            && r.record["body"]["workItem"] == item
            && r.record["body"]["returnRef"] == ret
    })
}
fn return_state(review: Option<&Row>) -> &'static str {
    match review.map(|r| text(&r.record["body"]["verdict"])) {
        None => "awaiting review",
        Some("findings to repair") => "reviewed — findings to repair",
        Some("not concluded") => "review not concluded",
        _ => "reviewed — awaiting integration",
    }
}
fn sourced(row: &Row) -> Value {
    json!({"recordId":row.id(),"source":row.source,"recorder":row.record["recorder"]})
}

const DELEGATION: [&str; 3] = ["dispatch_observed", "child_observed", "observation_ended"];
fn child_key(record: &Value) -> String {
    let child = &record["body"]["child"];
    json!([child["generation"]["home"], child["threadId"]]).to_string()
}
/// The App's own 0.2 delegation observations, in protected order. They carry
/// no undertaking: only a dispatch's recorded association ties it to a brief.
/// Each entry is the observation with its source and governing order.
struct Delegation<'a> {
    dispatches: Vec<&'a Value>,
    /// The last status or end of observation recorded for each child.
    last: BTreeMap<String, &'a Value>,
    /// Children with a status or an end recorded and no dispatch.
    orphaned: Vec<&'a str>,
}
fn observation_source(observation: &Value) -> Value {
    json!({"recordId":observation["record"]["observationId"],"source":observation["source"],
        "protectedOrder":observation["protectedOrder"],"recorder":observation["record"]["recorder"]})
}
impl<'a> Delegation<'a> {
    fn read(observations: &'a [Value]) -> Self {
        let rows: Vec<&Value> = observations.iter()
            .filter(|o| o["record"]["formatVersion"] == "0.2" && DELEGATION.contains(&text(&o["record"]["kind"]))).collect();
        let dispatches: Vec<&Value> = rows.iter().copied().filter(|o| o["record"]["kind"] == "dispatch_observed").collect();
        let mut last = BTreeMap::new();
        // An ended generation stays ended: a status of that generation written
        // after its end (a delayed write) never supersedes the end. A status
        // from a later generation does.
        let mut ended_generations = BTreeSet::new();
        for row in rows.iter().copied().filter(|o| o["record"]["kind"] != "dispatch_observed") {
            let record = &row["record"];
            let generation = json!([child_key(record), record["body"]["child"]["generation"]]).to_string();
            if record["kind"] == "observation_ended" {
                ended_generations.insert(generation.clone());
                // An end of one generation's observation never replaces what a
                // different generation, not ended, recorded of the child: a late
                // end of an earlier generation (an App relaunch end written after
                // a fresh observation) leaves the fresh one.
                let fresher = last.get(&child_key(record)).map(|seen: &&Value| json!([child_key(&seen["record"]), seen["record"]["body"]["child"]["generation"]]).to_string())
                    .is_some_and(|seen| seen != generation && !ended_generations.contains(&seen));
                if fresher {
                    continue;
                }
            } else if ended_generations.contains(&generation) {
                continue;
            }
            last.insert(child_key(record), row);
        }
        let dispatched: BTreeSet<String> = dispatches.iter().map(|d| child_key(&d["record"])).collect();
        let orphaned = last.iter().filter(|(key, _)| !dispatched.contains(*key)).map(|(_, o)| text(&o["record"]["body"]["child"]["threadId"])).collect();
        Self { dispatches, last, orphaned }
    }
    /// An end of this child's observation is the last thing recorded of it.
    fn ended(&self, record: &Value) -> bool {
        self.last.get(&child_key(record)).is_some_and(|o| o["record"]["kind"] == "observation_ended")
    }
    /// What was last recorded of a dispatched child, in words that claim
    /// nothing about the child now, and whether its observation ended.
    fn observed(&self, dispatch: &'a Value) -> (String, bool, Option<&'a Value>) {
        match self.last.get(&child_key(&dispatch["record"])).copied() {
            Some(o) if o["record"]["kind"] == "observation_ended" => (format!("observation ended ({}) as recorded {}, last recorded status {}; outcome unknown",
                text(&o["record"]["body"]["cause"]), text(&o["record"]["observedAt"]), o["record"]["body"]["lastObserved"].as_str().unwrap_or("none")), true, Some(o)),
            Some(o) => (format!("child last observed {} as recorded {}; nothing has been recorded of it since",
                text(&o["record"]["body"]["status"]), text(&o["record"]["observedAt"])), false, Some(o)),
            None => (format!("no child status recorded since the dispatch was recorded {}", text(&dispatch["record"]["observedAt"])), false, None),
        }
    }
}

pub(super) fn derive(
    briefs: &[Row],
    graphs: &[Row],
    log: &LogRead,
    duplicates: &BTreeSet<String>,
    observations: &[Value],
    inputs: &Inputs,
    stable: bool,
) -> Value {
    let undertakings: BTreeSet<_> = graphs
        .iter()
        .chain(log.rows.iter())
        .map(|r| text(&r.record["undertaking"]))
        .filter(|s| !s.is_empty())
        .collect();
    let delegation = Delegation::read(observations);
    // The tie is the one recorded with the dispatch: the work item and
    // undertaking the referenced brief record named when the dispatch was
    // recorded. Nothing in the project's files is consulted to tie anything.
    fn tie(record: &Value) -> Option<(&str, &str)> {
        let association = &record["body"]["association"];
        Some((association["undertaking"].as_str()?, association["workItem"].as_str()?))
    }
    // Children with no ending of their observation recorded that the record ties to no work item.
    let untied = delegation.dispatches.iter().filter(|d| tie(&d["record"]).is_none() && !delegation.ended(&d["record"])).count()
        + delegation.last.iter().filter(|(key, o)| o["record"]["kind"] != "observation_ended"
            && !delegation.dispatches.iter().any(|d| &child_key(&d["record"]) == *key)).count();
    // A project line of an App-only kind is the App's observation only where
    // the protected copy holds the identical line.
    let delegation_claims: Vec<&Row> = log.rows.iter()
        .filter(|r| r.record["formatVersion"] == "0.2" && DELEGATION.contains(&r.kind())).collect();
    let unprotected_claims = delegation_claims.iter()
        .any(|r| !observations.iter().any(|o| array(&o["projectCounterparts"]).contains(&r.source)));
    let views: Vec<_> = undertakings.into_iter().map(|undertaking| {
        let rows: Vec<_> = log.rows.iter().filter(|r| r.record["undertaking"] == undertaking).collect();
        let (mut active, mut notes) = active(&rows, duplicates);
        let mut unresolved_relations = BTreeSet::new();
        for row in active.iter().filter(|r| matches!(r.kind(), "review_recorded" | "integration_recorded")) {
            let body = &row.record["body"];
            let ret = active.iter().find(|r| r.kind()=="return_recorded" && r.record["recordId"]==body["returnRef"]
                && r.record["body"]["workItem"]==body["workItem"]);
            let review_ok = body["reviewRef"].as_str().is_none_or(|reference| active.iter().any(|r|
                r.kind()=="review_recorded" && r.id()==reference && r.record["body"]["returnRef"]==body["returnRef"]
                    && r.record["body"]["workItem"]==body["workItem"]));
            if ret.is_none() || !review_ok {
                unresolved_relations.insert(row.id());
                notes.push(format!("{}: return/review reference is missing, corrected or mismatched; relation not used", row.id()));
            }
        }
        active.retain(|row| !unresolved_relations.contains(row.id()));
        let mut result = json!({"undertaking":undertaking,"graph":null,"revision":null,
            "currentGraphEstablished":false,"queueComplete":false,"queue":[],"waiting":[],"notes":[]});
        if !stable { result["notes"] = json!(["source snapshot changed; refresh before using any derived state"]); return result; }
        let Some(selector) = rows.iter().rev().find(|r|r.kind()=="current_graph") else {
            result["notes"] = json!(["no current graph selected; no empty-work conclusion"]); return result;
        };
        // Never fall back to an earlier selector when the latest is ambiguous,
        // unsupported, corrected away, missing, or has different bytes.
        if !active.iter().any(|r|r.id()==selector.id()) {
            result["notes"] = json!(["latest selector is unresolved; no earlier graph substituted"]); return result;
        }
        let target = &selector.record["body"];
        let candidates: Vec<_> = graphs.iter().filter(|g|g.record["recordId"]==target["graph"] && g.record["undertaking"]==undertaking).collect();
        if candidates.len()!=1 || duplicates.contains(text(&target["graph"])) {
            result["notes"] = json!(["selected graph missing, duplicated or belongs to another undertaking"]); return result;
        }
        let graph = candidates[0];
        if target["graphContent"]["method"] != crate::util::FILE_IDENTITY_METHOD
            || target["graphContent"]["value"] != crate::util::sha256_hex(&graph.bytes) {
            result["notes"] = json!(["selected graph content differs or identity method unsupported; historical TEST VALUE selectors are not rebound"]); return result;
        }
        let items = array(&graph.record["body"]["items"]);
        let ids: BTreeSet<_> = items.iter().map(|i| text(&i["itemId"])).collect();
        if ids.len() != items.len() { result["notes"] = json!(["selected graph repeats item identities; no item chosen"]); return result; }
        // Workers with no ending of their observation recorded whose recorded item is not a selected item of this graph (removed or unselected).
        let selected: BTreeSet<_> = items.iter().filter(|i| i["selected"] == true).map(|i| text(&i["itemId"])).collect();
        let outside_selection: Vec<String> = delegation.dispatches.iter().filter(|d| !delegation.ended(&d["record"]))
            .filter_map(|d| tie(&d["record"]).filter(|(u, item)| *u == undertaking && !selected.contains(item)).map(|(_, item)| item.to_owned())).collect();
        let incomplete = !log.complete || !duplicates.is_empty() || !notes.is_empty();
        let observed: Vec<_> = observations.iter().filter(|o|o["record"]["formatVersion"]=="0.1" && o["record"]["undertaking"]==undertaking).map(|o|&o["record"]).collect();
        let dispatched: BTreeSet<_> = observed.iter().filter(|o|o["kind"]=="dispatch_observed").map(|o|text(&o["body"]["childThread"])).collect();
        let orphaned: BTreeSet<_> = observed.iter().filter(|o|matches!(text(&o["kind"]),"child_observed"|"observation_ended") && !dispatched.contains(text(&o["body"]["childThread"]))).map(|o|text(&o["body"]["childThread"])).collect();
        let unassociated = observed.iter().filter(|o|o["kind"]=="dispatch_observed" && o["body"]["association"]["brief"].is_null()).count() + orphaned.len()
            + untied + outside_selection.len();
        let untrusted = unprotected_claims || rows.iter().any(|r|OBSERVED.contains(&r.kind())
            && !observations.iter().any(|o|array(&o["projectCounterparts"]).contains(&r.source)));
        if incomplete { notes.push("coordination log incomplete or conflicting; non-done states are unknown and the queue is not complete".into()); }
        if untrusted { notes.push("App-named project observations lack a healthy protected counterpart; native execution is not established".into()); }
        if !orphaned.is_empty() { notes.push(format!("orphaned child observations: {}",orphaned.iter().copied().collect::<Vec<_>>().join(", "))); }
        if !outside_selection.is_empty() { notes.push(format!("a worker was last observed, with no ending of that observation recorded, for work that is not selected in the current graph: {}", outside_selection.join(", "))); }
        if !delegation.orphaned.is_empty() { notes.push(format!("child observations with no recorded dispatch: {}",delegation.orphaned.join(", "))); }
        let item_return = |id:&str| event(&active,"return_recorded",id);
        let integrated = |id:&str| item_return(id).and_then(|r|return_events(&active,"integration_recorded",id,r.id()));
        let external = |id:&str| event(&active,"external_result",id);
        let mut queue = Vec::new();
        let mut waiting = Vec::new();
        // Queue membership belongs to the return, not to the current graph's
        // item list. Removing an item cannot silently integrate its return.
        for ret in active.iter().copied().filter(|r|r.kind()=="return_recorded") {
            let id=text(&ret.record["body"]["workItem"]);
            if return_events(&active,"integration_recorded",id,ret.id()).is_some() { continue; }
            let item=items.iter().find(|i|i["itemId"]==id);
            let return_brief=ret.record["body"]["brief"].as_str();
            let brief_id=return_brief
                .or_else(||item.and_then(|i|i["brief"].as_str()));
            let matching:Vec<_>=briefs.iter().filter(|b|b.record["undertaking"]==undertaking && b.record["body"]["workItem"]==id
                && brief_id.is_some_and(|id|b.record["body"]["briefId"]==id)).collect();
            let brief=(matching.len()==1 && !duplicates.contains(matching[0].id())).then(||matching[0]);
            let review=return_events(&active,"review_recorded",id,ret.id());
            queue.push(json!({"item":id,"outcome":item.map(|i|i["outcome"].clone()).unwrap_or(json!("outcome not in the current graph")),
                "inCurrentGraph":item.is_some(),"returnRef":ret.id(),"state":return_state(review),
                "returnedBy":actor(&ret.record["body"]["returnedBy"]),"recordedBy":actor(&ret.record["recorder"]),
                "examines":brief.map(|b|format!("{} (prepared the brief)",actor(&b.record["body"]["preparedBy"]))).unwrap_or("examiner not established".into()),
                "examinesProvenance":{"basis":if return_brief.is_some(){"return-brief"}else{"current-graph-brief"},
                    "briefId":brief_id,"referenceSource":if return_brief.is_some(){Some(sourced(ret))}else{item.map(|_|sourced(graph))},
                    "briefSource":brief.map(sourced)},
                "examiner":review.map(|r|actor(&r.record["body"]["reviewer"])),
                "returned":ret.record["body"]["returned"],"evidence":ret.record["body"]["evidence"],
                "sources":[sourced(ret),review.map(sourced),brief.map(sourced)]}));
        }
        for item in items {
            let id = text(&item["itemId"]);
            let brief_matches:Vec<_> = briefs.iter().filter(|b|b.record["undertaking"]==undertaking && b.record["body"]["workItem"]==id && b.record["body"]["briefId"]==item["brief"] && !item["brief"].is_null()).collect();
            let brief = (brief_matches.len()==1 && !duplicates.contains(brief_matches[0].id())).then(||brief_matches[0]);
            if item["selected"] != true { continue; }
            let ret = item_return(id);
            let review = ret.and_then(|r|return_events(&active,"review_recorded",id,r.id()));
            let done = integrated(id).or_else(||external(id));
            let mut causes = Vec::<String>::new();
            let needs: Vec<_> = array(&item["needs"]).iter().map(|need| {
                let mut value = match text(&need["kind"]) {
                    "item" => {
                        let other = text(&need["ref"]);
                        if !ids.contains(other) { json!({"state":"unknown","why":"item not in the selected graph"}) }
                        else if integrated(other).is_some() || external(other).is_some() {
                            json!({"state":"satisfied","why":"integrated return or external result recorded","source":integrated(other).or_else(||external(other)).map(sourced)})
                        } else { json!({"state":"outstanding","why":"no integration of the current return or external result recorded"}) }
                    },
                    "decision" => json!({"state":"unknown","why":"current human-act standing is not admitted by the Fleet reader; inspect the decision package and its provenance/lapse limits"}),
                    _ => need_input(need, inputs),
                };
                if incomplete && value["state"] == "satisfied" && need["kind"]=="item" {
                    value["state"]=json!("unknown");value["why"]=json!("coordination log incomplete; later returns or corrections may be unread");
                }
                value["need"]=need.clone();value
            }).collect();
            for need in &needs {
                causes.push(format!("{} {}: {} ({})",text(&need["need"]["kind"]),text(&need["need"]["ref"]),text(&need["state"]),text(&need["why"])));
                if let Some(condition)=need["need"]["condition"].as_str(){causes.push(format!("recorded condition: {condition}"));}
            }
            let mut category;
            let mut ready_cause = None;
            if let Some(done)=done {
                category="done";
                causes.insert(0,if done.kind()=="integration_recorded" {"integration recorded".into()} else {format!("external result recorded ({})",actor(&done.record["body"]["owner"]))});
            } else if ret.is_some() {
                category="returned";causes.push(return_state(review).into());
            } else if needs.iter().any(|n|n["state"]=="unknown") {
                category="unknown";
            } else if !item["brief"].is_null() && brief.is_none() {
                // Unknown takes precedence over waiting.
                category="unknown";causes.push("named brief absent or ambiguous; assignment basis not established".into());
            } else if needs.iter().any(|n|n["state"]=="outstanding") {
                category="waiting";
            } else if item["owner"]["kind"]=="external" {
                category="waiting";causes.push(format!("waits for external owner {}; no result recorded",actor(&item["owner"])));
            } else {
                category="ready";ready_cause=Some(causes.len());
                causes.push(if brief.is_some(){"inputs satisfied; brief prepared; no dispatch observed"}else{"inputs satisfied; no dispatch observed"}.into());
            }
            // The recorded dispatches that hold this item, one entry for each
            // worker, in a form a view can show without reading the cause text.
            let mut workers: Vec<Value> = Vec::new();
            // Historical 0.1 facts remain source-recorded statements. They never
            // identify a current native conversation, role, home or active child.
            if done.is_none() && ret.is_none() {
                let dispatch = observed.iter().rev().find(|o|o["kind"]=="dispatch_observed" && !item["brief"].is_null() && o["body"]["association"]["brief"]==item["brief"]);
                if let Some(dispatch)=dispatch {
                    let last=observed.iter().rev().find(|o|matches!(text(&o["kind"]),"child_observed"|"observation_ended") && o["body"]["childThread"]==dispatch["body"]["childThread"]);
                    category="unknown";
                    causes.push(format!("protected Fleet record reports dispatch of {}; current native relationship/status not established{}",text(&dispatch["body"]["childThread"]),last.map(|o|format!("; last recorded {} {}",text(&o["kind"]),text(&o["body"]["status"]))).unwrap_or_default()));
                } else if rows.iter().any(|r|r.kind()=="dispatch_observed" && !item["brief"].is_null() && r.record["body"]["association"]["brief"]==item["brief"]) {
                    category="unknown";causes.push("project dispatch claim lacks protected App provenance".into());
                }
                // The App's own observation: the item is held by a worker until a
                // return is recorded. Nothing about the work or its outcome follows.
                // A dispatch holds this item where its record says so: the brief
                // record its prompt referenced named this item and undertaking when
                // the dispatch was recorded. The project's files now say only whether
                // that brief still has the referenced content and is still current.
                let for_item: Vec<&Value> = delegation.dispatches.iter().copied()
                    .filter(|d| tie(&d["record"]) == Some((undertaking, id))).collect();
                for dispatch in &for_item {
                    let record = &dispatch["record"];
                    let association = &record["body"]["association"];
                    let (observed, ended, last) = delegation.observed(dispatch);
                    // The brief record named at dispatch, if it is still among the project's brief files.
                    let named: Vec<&Row> = briefs.iter().filter(|b| b.record["recordId"] == association["briefRecord"] && b.record["undertaking"] == undertaking).collect();
                    let named = (named.len() == 1 && !duplicates.contains(named[0].id())).then(|| named[0]);
                    let current = named.is_some() && brief.is_some_and(|b| Some(b.id()) == named.map(Row::id));
                    let digest = if association["briefContent"].is_object() { &association["briefContent"]["value"] } else { &association["referencedContent"]["value"] };
                    let matches_now = named.map(|b| *digest == crate::util::sha256_hex(&b.bytes));
                    let matched_then = association["state"] == "brief referenced";
                    let content = match (matched_then, matches_now) {
                        (_, None) => "the brief record it named is not among the project's brief files now",
                        (true, Some(true)) => "the brief file has the content the prompt referenced",
                        (true, Some(false)) => "the brief file had the content the prompt referenced when the dispatch was recorded and does not have it now",
                        (false, Some(false)) => "the brief file does not have the content the prompt referenced",
                        (false, Some(true)) => "the brief file did not have the content the prompt referenced when the dispatch was recorded and has it now",
                    };
                    let earlier = if current { String::new() } else {
                        format!("; dispatched under {}, not the item's current brief {}: preparing a new brief releases nothing",
                            text(&association["brief"]), item["brief"].as_str().unwrap_or("(none named)"))
                    };
                    workers.push(json!({"child":record["body"]["child"]["threadId"],"parent":record["body"]["parent"]["threadId"],
                        "association":association["state"],"briefNamed":association["brief"],"briefRecord":association["briefRecord"],"briefFile":association["briefFile"],
                        "briefIsCurrent":current,"currentBrief":item["brief"],
                        "briefContentMatches":matches_now,"briefContentMatchedWhenRecorded":matched_then,
                        "recordedAt":record["observedAt"],"lastObserved":observed,"observationEnded":ended,
                        "sources":{"dispatch":observation_source(dispatch),"lastObservation":last.map(observation_source),"brief":named.map(sourced)}}));
                    causes.push(format!("App observed dispatch of child {} by {}; its spawn prompt named {} ({}){earlier}; {content}; {observed}",
                        text(&record["body"]["child"]["threadId"]), text(&record["body"]["parent"]["threadId"]),
                        text(&association["briefFile"]), text(&association["brief"])));
                }
                if !workers.is_empty() {
                    // The sentence that no dispatch was observed is written only where none was.
                    if let Some(index) = ready_cause { causes.remove(index); }
                    if workers.iter().all(|w| w["observationEnded"] == true) {
                        category = "unknown";
                    } else if category != "unknown" {
                        category = "dispatched";
                    }
                } else if delegation_claims.iter().any(|r| r.kind()=="dispatch_observed" && tie(&r.record) == Some((undertaking, id))) {
                    category="unknown";causes.push("a dispatch line in the project's log lacks protected App provenance: the records store now attached holds no identical line. It is its recorder's claim, and nothing further can be recorded of that child here (the project's records identity may have changed)".into());
                }
            }
            if done.is_none() {
                for change in active.iter().filter(|r|r.kind()=="basis_changed" && array(&r.record["body"]["affectedItems"]).iter().any(|i|i==id)) {
                    causes.push(format!("basis changed since: {}",change.id()));
                }
                if incomplete { category="unknown";causes.insert(0,"coordination log incomplete; this item's current state cannot be established".into()); }
            }
            let qualified=category=="ready" && (unassociated>0 || untrusted);
            if qualified { category="ready (qualified)";causes.insert(0,"child observations without a usable brief/dispatch association; a dispatch for this item may be unrecorded".into()); }
            waiting.push(json!({"item":id,"outcome":item["outcome"],"owner":actor(&item["owner"]),"category":category,
                "readinessQualified":qualified,"causes":causes,"dispatches":workers,"needs":needs,"next":item["next"],"writeScope":item["writeScope"],
                "sources":{"graph":sourced(graph),"return":ret.map(sourced),"review":review.map(sourced),"done":done.map(sourced)}}));
        }
        result["graph"]=json!(graph.id());result["revision"]=graph.record["body"]["revision"].clone();
        result["selector"]=sourced(selector);result["graphSource"]=sourced(graph);
        result["currentGraphEstablished"]=json!(!incomplete);
        result["queueComplete"]=json!(!incomplete && orphaned.is_empty() && unassociated==0 && !untrusted);
        result["queue"]=json!(queue);result["waiting"]=json!(waiting);result["notes"]=json!(notes);result
    }).collect();
    json!({"standing":"Derived file-based coordination claims, not native execution, permission, human acceptance or authority. Rebuild writes nothing.",
        "graphIdentityMethod":crate::util::FILE_IDENTITY_METHOD,"undertakings":views,
        "limits":["Decision needs remain unknown until their current human-act standing is available; a recorded decision alone is insufficient.",
            "A dispatch is shown only from the App's own recorded observation, tied to an item only by what its record says the brief its spawn prompt named was for, read when the dispatch was recorded; that shows which brief was named, not that the child received or read it. It establishes a child and its parent, never work done, a return, a review or an integration. Legacy 0.1 child observations do not establish a current native relationship."]})
}

#[cfg(test)]
#[path = "fleet_views_tests.rs"]
mod tests;
