//! DEL-06-01 RF facts and DEL-06-02 FV views over one stable, once-read packet.
//! No writer, dispatch, native identity join, or human-act admission.
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

/// The act records as the decision view reads them, from bytes this packet's
/// census read once, with each package file's identity as it was read.
struct DecisionRead {
    view: Value,
    packages: BTreeMap<String, crate::decision_view::FileObservation>,
}
fn contained(reference: &str) -> bool {
    let rel = Path::new(reference);
    !reference.is_empty()
        && !rel.is_absolute()
        && rel.components().all(|p| matches!(p, Component::Normal(_)))
}
fn census_logs(
    census: &mut Census,
    dir: &Path,
    exclude: &[std::path::PathBuf],
    out: &mut Vec<crate::decision_view::LogSource>,
) -> Result<(), String> {
    for path in census.directory(dir)? {
        let meta = census.metadata(&path)?.ok_or("act record source disappeared")?;
        if meta.is_dir() {
            census_logs(census, &path, exclude, out)?;
        } else if path.extension().is_some_and(|e| e == "jsonl") && !exclude.contains(&path) {
            let bytes = census.read(&path)?.ok_or("act log disappeared")?;
            out.push(crate::decision_view::LogSource { path, bytes: Ok(bytes) });
        }
    }
    Ok(())
}
/// A package file read once through the census, with every ancestor's
/// identity kept, as input files are; a link is never followed.
fn read_package(
    census: &mut Census,
    root: &Path,
    reference: &str,
    limits: &mut Vec<String>,
) -> crate::decision_view::FileObservation {
    use crate::decision_view::FileObservation;
    if !contained(reference) {
        limits.push("package file reference is not a contained relative path; content not observed".into());
        return FileObservation::of(None, false);
    }
    let path = root.join(reference);
    let mut ancestor = path.parent();
    while let Some(dir) = ancestor.filter(|d| d.starts_with(root)) {
        if let Err(e) = census.metadata(dir) {
            limits.push(format!("package file content not observed: {e}"));
            return FileObservation::of(None, false);
        }
        ancestor = dir.parent();
    }
    match census.read(&path) {
        Ok(Some(bytes)) => FileObservation::of(Some(&bytes), false),
        Ok(None) => FileObservation::of(None, true),
        Err(e) => {
            limits.push(format!("package file content not observed: {e}"));
            FileObservation::of(None, false)
        }
    }
}
/// Reads only. The decision view opens the configured records store, and
/// opening a store with no identity would create one, so an absent store or
/// identity leaves the act records unread and nothing is created.
fn read_decisions(census: &mut Census, root: &Path) -> Result<DecisionRead, String> {
    let configured = crate::records_store::current()?;
    let store = configured
        .root
        .canonicalize()
        .map_err(|_| "configured records store absent or unavailable; nothing created")?;
    let identity = census
        .read(&store.join("store.json"))?
        .ok_or("records store identity absent; nothing created")?;
    let identity: Value =
        serde_json::from_slice(&identity).map_err(|_| "records store identity unreadable")?;
    if identity["format"] != "chirality.records-store"
        || identity["storeId"].as_str().is_none_or(str::is_empty)
    {
        return Err("records store identity invalid".into());
    }
    census.read(&store.join("roots.jsonl"))?;
    census.read(&root.join(crate::records_store::PROJECT_LINK))?;
    decision_hook("after-identity");
    let home = crate::records_store::home(root)?;
    if let Some(refusal) = &home.attachment.refusal {
        return Err(format!("the project's records home is unresolved: {refusal}"));
    }
    let store_dir = if home.store_mode { home.attachment.dir.clone() } else { None };
    let imports = match &store_dir {
        Some(dir) => census.read(&dir.join("imports.jsonl"))?,
        None => None,
    };
    census.metadata(&crate::storage::registered_legacy_log(root)?)?;
    let sources = crate::storage::sources(root)?;
    let mut logs = Vec::new();
    for dir in &sources.walk {
        census_logs(census, dir, &sources.exclude, &mut logs)?;
    }
    for file in &sources.files {
        let bytes = census.read(file)?.ok_or("act log disappeared")?;
        logs.push(crate::decision_view::LogSource { path: file.clone(), bytes: Ok(bytes) });
    }
    // Package-import accounting is compared before and after, as the fleet
    // reader does for App observations.
    let provenance = store_dir.as_deref().map(crate::records_store::package::provenance_context);
    let set = crate::decision_view::RecordSet {
        logs,
        store_dir: store_dir.clone(),
        imports: Ok(imports),
        limits: Vec::new(),
    };
    let mut packages = BTreeMap::new();
    let view = crate::decision_view::derive_from(root, set, &mut |reference, limits| {
        decision_hook("before-package");
        let observed = read_package(census, root, reference, limits);
        packages.insert(
            reference.to_owned(),
            crate::decision_view::FileObservation {
                identity: observed.identity.clone(),
                absent: observed.absent,
            },
        );
        observed
    });
    decision_hook("after-derive");
    if store_dir.as_deref().map(crate::records_store::package::provenance_context) != provenance {
        return Err("package import accounting changed while reading".into());
    }
    Ok(DecisionRead { view, packages })
}
#[cfg(test)]
thread_local! { pub(super) static DECISION_READ: std::cell::RefCell<Option<Box<dyn FnMut(&str)>>> = const { std::cell::RefCell::new(None) }; }
/// A test's stand-in for a concurrent writer at a named point of the read.
fn decision_hook(_point: &str) {
    #[cfg(test)]
    DECISION_READ.with(|h| {
        if let Some(hook) = h.borrow_mut().as_mut() {
            hook(_point)
        }
    });
}
fn sources_text(sources: &Value) -> String {
    let at: Vec<_> = array(sources)
        .iter()
        .map(|s| format!("{} seq {}", text(&s["log"]), s["seq"]))
        .collect();
    if at.is_empty() {
        "source not located".into()
    } else {
        at.join(", ")
    }
}
/// DEL-06-01 Need (decision) and REQ-004, through the decision view's reading
/// of the request and act records; nothing here reinterprets an act. The ref
/// names a request record identity, or a contained project-relative path of
/// the decision package file (the form the App's guidance gives agents).
fn decision_need(
    census: &mut Census,
    root: &Path,
    read: &Result<DecisionRead, String>,
    reference: &str,
) -> Value {
    let unknown = |why: String| json!({"state":"unknown","why":why});
    let read = match read {
        Ok(read) => read,
        Err(reason) => {
            return unknown(format!(
                "act records not read ({reason}); whether an act of the person settles {reference} is not established"
            ))
        }
    };
    if read.view["recordSetComplete"] != true {
        let first = read.view["limits"][0].as_str().unwrap_or("a record could not be read");
        return unknown(format!(
            "act records not fully read ({first}); whether an act of the person settles {reference} is not established"
        ));
    }
    let rows = array(&read.view["rows"]);
    let names = |r: &Value, key: &str| array(&r[key]).iter().any(|id| id == reference);
    let by_id: Vec<&Value> = rows
        .iter()
        .filter(|r| names(r, "requests") || names(r, "correctedRequests"))
        .collect();
    let row = match by_id[..] {
        [row] => row,
        [_, _, ..] => {
            return unknown(format!("decision request {reference} appears in several package rows; no package is established"))
        }
        [] => {
            if !contained(reference) {
                return unknown(format!("{reference} names no decision request and is not a contained project path of a package file"));
            }
            let mut limits = Vec::new();
            let current = match read.packages.get(reference) {
                Some(seen) => crate::decision_view::FileObservation { identity: seen.identity.clone(), absent: seen.absent },
                None => read_package(census, root, reference, &mut limits),
            };
            let for_file: Vec<&Value> = rows.iter().filter(|r| r["packageFile"] == reference).collect();
            match for_file[..] {
                [] if current.identity.is_some() => {
                    return json!({"state":"outstanding","why":format!(
                        "decision package file {reference} has not yet been recorded as a request; no act of the person can cite it"),
                        "request":{"recordId":null,"packageFile":reference}})
                }
                [] => {
                    return unknown(format!(
                        "{reference} names no decision request and no readable package file{}",
                        limits.first().map(|l| format!(" ({l})")).unwrap_or_default()
                    ))
                }
                [row] => row,
                _ => {
                    let now = current.identity.as_ref().map(|c| c.value.as_str());
                    let matching: Vec<&Value> = for_file
                        .iter()
                        .copied()
                        .filter(|r| now.is_some() && r["packageIdentity"]["value"].as_str() == now)
                        .collect();
                    match matching[..] {
                        [row] => row,
                        _ => return unknown(format!(
                            "several requests name package file {reference} with different contents, and the file's current content selects none of them"
                        )),
                    }
                }
            }
        }
    };
    let request = format!(
        "package file {} (request {}; {})",
        text(&row["packageFile"]),
        array(&row["requests"]).iter().map(text).collect::<Vec<_>>().join(", "),
        sources_text(&row["requestSources"])
    );
    let corrected = if names(row, "correctedRequests") {
        format!("request {reference} is corrected and read through {}; ", text(&row["package"]))
    } else {
        String::new()
    };
    let limits: Vec<_> = array(&row["limits"]).iter().map(text).collect();
    let noted = if limits.is_empty() {
        String::new()
    } else {
        format!("; recorded and not counted: {}", limits.join("; "))
    };
    let mut value = match text(&row["state"]) {
        "decided" => {
            let d = &row["decision"];
            let act = d["act"].as_str().or_else(|| row["currentCandidates"][0].as_str()).unwrap_or("");
            let lapse = text(&d["lapse"]);
            let state = match lapse {
                "not lapsed" => "satisfied",
                "matches c0 again after observed lapse" => "outstanding",
                l if l.starts_with("lapsed") => "outstanding",
                _ => "unknown",
            };
            let why = format!(
                "{corrected}act {act} ({}) records {} choosing {} on {request}, recorded by {}; lapse: {lapse}{}",
                sources_text(&d["recordSources"]),
                text(&d["decidedBy"]),
                text(&d["alternativeChosen"]),
                text(&d["recordedBy"]),
                match state {
                    "satisfied" => "",
                    "outstanding" => "; a lapsed decision does not settle the need",
                    _ => "; whether the decision still holds is not established",
                }
            );
            let quoted = &d["actRecord"];
            let mut value = json!({"state":state,"why":why});
            value["decision"] = json!({"act":act,"alternativeChosen":d["alternativeChosen"],"statement":d["statement"],
                "decisionActor":quoted["decisionActor"],"decidedBy":d["decidedBy"],
                "recorder":quoted["recorder"],"recordedBy":d["recordedBy"],
                "boundContent":quoted["boundContent"],"scope":quoted["scope"],"purpose":quoted["purpose"],
                "capturedAt":d["capturedAt"],"lapse":lapse,"recordSources":d["recordSources"],
                "origin":d["origin"],"captureProvenance":d["captureProvenance"]});
            value
        }
        "ambiguous current standing" => unknown(format!(
            "{corrected}several decisions on {request} whose order the records do not establish, or an act whose origin is not established ({}){noted}",
            array(&row["currentCandidates"]).iter().map(text).collect::<Vec<_>>().join(", ")
        )),
        s if s == crate::decision_view::DECIDED_INCOMPLETE || s == crate::decision_view::PENDING_INCOMPLETE => unknown(format!(
            "{corrected}{request} reads as {s}{noted}")),
        s if s == crate::decision_view::PENDING => json!({"state":"outstanding","why":format!(
            "{corrected}no recorded act of the person of kind {} in this installation's records store cites {request} and chooses an alternative the package names{noted}",
            text(&row["actRequested"])
        )}),
        other => unknown(format!("{corrected}{request} reads as {other}{noted}")),
    };
    value["request"] = json!({"recordId":row["package"],"requests":row["requests"],"sources":row["requestSources"],
        "packageFile":row["packageFile"],"actRequested":row["actRequested"],"claims":row["claims"]});
    value
}

/// References are relative to the fixed Fleet folder, never arbitrary host paths.
/// All source bytes and absent leaves join the existing whole-packet census.
pub(super) fn read_inputs(census: &mut Census, root: &Path, graphs: &[Row]) -> Inputs {
    let mut out = Inputs::new();
    let mut decisions = None;
    for graph in graphs {
        for item in array(&graph.record["body"]["items"]) {
            for need in array(&item["needs"]) {
                let kind = text(&need["kind"]);
                if !matches!(kind, "input" | "connector" | "decision") {
                    continue;
                }
                let reference = text(&need["ref"]);
                let key = (kind.to_owned(), reference.to_owned());
                // Connector declarations may disagree, so cache raw observations,
                // not a conclusion derived under the first declaration.
                if out.contains_key(&key) {
                    continue;
                }
                if kind == "decision" {
                    let read = decisions.get_or_insert_with(|| read_decisions(census, root));
                    let observation = decision_need(census, root, read, reference);
                    out.insert(key, Input { bytes: None, observation });
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
        let incomplete = !log.complete || !duplicates.is_empty() || !notes.is_empty();
        let observed: Vec<_> = observations.iter().filter(|o|o["record"]["formatVersion"]=="0.1" && o["record"]["undertaking"]==undertaking).map(|o|&o["record"]).collect();
        let dispatched: BTreeSet<_> = observed.iter().filter(|o|o["kind"]=="dispatch_observed").map(|o|text(&o["body"]["childThread"])).collect();
        let orphaned: BTreeSet<_> = observed.iter().filter(|o|matches!(text(&o["kind"]),"child_observed"|"observation_ended") && !dispatched.contains(text(&o["body"]["childThread"]))).map(|o|text(&o["body"]["childThread"])).collect();
        let unassociated = observed.iter().filter(|o|o["kind"]=="dispatch_observed" && o["body"]["association"]["brief"].is_null()).count() + orphaned.len();
        let untrusted = rows.iter().any(|r|OBSERVED.contains(&r.kind())
            && !observations.iter().any(|o|array(&o["projectCounterparts"]).contains(&r.source)));
        if incomplete { notes.push("coordination log incomplete or conflicting; non-done states are unknown and the queue is not complete".into()); }
        if untrusted { notes.push("App-named project observations lack a healthy protected counterpart; native execution is not established".into()); }
        if !orphaned.is_empty() { notes.push(format!("orphaned child observations: {}",orphaned.iter().copied().collect::<Vec<_>>().join(", "))); }
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
            if let Some(done)=done {
                category="done";
                causes.insert(0,if done.kind()=="integration_recorded" {"integration recorded".into()} else {format!("external result recorded ({})",actor(&done.record["body"]["owner"]))});
            } else if ret.is_some() {
                category="returned";causes.push(return_state(review).into());
            } else if needs.iter().any(|n|n["state"]=="unknown") {
                category="unknown";
            } else if needs.iter().any(|n|n["state"]=="outstanding") {
                category="waiting";
            } else if item["owner"]["kind"]=="external" {
                category="waiting";causes.push(format!("waits for external owner {}; no result recorded",actor(&item["owner"])));
            } else if !item["brief"].is_null() && brief.is_none() {
                category="unknown";causes.push("named brief absent or ambiguous; assignment basis not established".into());
            } else {
                category="ready";causes.push(if brief.is_some(){"inputs satisfied; brief prepared; no dispatch observed"}else{"inputs satisfied; no dispatch observed"}.into());
            }
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
                "readinessQualified":qualified,"causes":causes,"needs":needs,"next":item["next"],"writeScope":item["writeScope"],
                "sources":{"graph":sourced(graph),"return":ret.map(sourced),"review":review.map(sourced),"done":done.map(sourced)}}));
        }
        result["graph"]=json!(graph.id());result["revision"]=graph.record["body"]["revision"].clone();
        result["selector"]=sourced(selector);result["graphSource"]=sourced(graph);
        result["currentGraphEstablished"]=json!(!incomplete);
        result["queueComplete"]=json!(!incomplete && orphaned.is_empty() && !untrusted);
        result["queue"]=json!(queue);result["waiting"]=json!(waiting);result["notes"]=json!(notes);result
    }).collect();
    json!({"standing":"Derived file-based coordination claims, not native execution, permission, human acceptance or authority. Rebuild writes nothing.",
        "graphIdentityMethod":crate::util::FILE_IDENTITY_METHOD,"undertakings":views,
        "limits":["A decision need names an act request's record identity or the decision package file's project path, and reads the act records as the decision view does: satisfied only by an unlapsed act of the person in this installation's records store, of the kind the package names, citing its request and choosing an alternative it names; outstanding when there is none, the package is not yet recorded as a request, or the decision lapsed; unknown when the act records cannot be read, the reference names neither a request nor a file, or several decisions on the package are unordered. Project-file, imported and legacy-imported acts are listed as claims and decide nothing. The act record is a recorded claim; its native capture origin is not verified.",
            "Legacy 0.1 child observations do not establish a current native relationship. The native dispatch producer remains unavailable."]})
}

#[cfg(test)]
#[path = "fleet_views_tests.rs"]
mod tests;
