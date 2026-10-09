//! CAM-v0.1 source-evidence drafts. No facts, reliance or performed actor duties.
use serde_json::{json, Value};
use std::collections::HashSet;
pub const BYTE_LIMIT: usize = 1048576;
fn text<'a>(v: &'a Value, key: &str) -> Result<&'a str, String> {
    v[key]
        .as_str()
        .ok_or_else(|| format!("Missing text: {key}"))
}
fn array<'a>(v: &'a Value, key: &str) -> Result<&'a Vec<Value>, String> {
    v[key]
        .as_array()
        .ok_or_else(|| format!("Missing array: {key}"))
}
fn literal_path(s: &str) -> bool {
    !s.is_empty()
        && !s.starts_with('/')
        && !s.contains('\0')
        && s.split('/').all(|p| !p.is_empty() && p != "." && p != "..")
}
/// Internal consistency only. Original receipt buffers/custody cannot be recovered cold.
pub fn validate_cold(v: &Value) -> Result<(), String> {
    if serde_json::to_vec(v).map_err(|e| e.to_string())?.len() > BYTE_LIMIT {
        return Err("Format0.3 exceeds1MiB serialized bytes".into());
    }
    validate_common(v)
}
pub(crate) fn validate_common(v: &Value) -> Result<(), String> {
    let req = &v["evidence"]["git_request"];
    if v["question"]["at_revision"] != req["at"] || v["question"]["since_revision"] != req["since"]
    {
        return Err("Question/request revision mismatch".into());
    }
    if !array(&v["trigger"], "receiving_records")?.is_empty() {
        return Err("Draft receiving records must be empty".into());
    }
    let mut ids = HashSet::new();
    let mut source_ids = HashSet::new();
    let mut excerpt_ids = HashSet::new();
    let mut sides = HashSet::new();
    let mut observations = HashSet::new();
    let mut paths = HashSet::new();
    for s in array(v, "sources")? {
        let id = text(s, "source_id")?;
        if !ids.insert(id) {
            return Err("Duplicate identifier".into());
        }
        source_ids.insert(id);
        if !literal_path(text(s, "path")?) {
            return Err("Invalid literal source path".into());
        }
        paths.insert(text(s, "path")?);
        let p = &s["provenance"];
        if !observations.insert(text(p, "observation_reference")?) {
            return Err("Duplicate source observation reference".into());
        }
        let side = text(p, "side")?;
        if !sides.insert(side) {
            return Err("Duplicate selected side".into());
        }
        if s["revision"] != p["commit"] || p["commit"] != req[side] {
            return Err("Source/provenance/request revision mismatch".into());
        }
        let n = match text(p, "object_format")? {
            "sha1" => 40,
            "sha256" => 64,
            _ => return Err("Unsupported object format".into()),
        };
        if text(req, "at")?.len() != n || req["since"].as_str().is_some_and(|s| s.len() != n) {
            return Err("Requested object formats differ".into());
        }
        for k in ["commit", "root_tree", "blob"] {
            if text(p, k)?.len() != n {
                return Err("Object ID length/format mismatch".into());
            }
        }
        for e in array(s, "excerpts")? {
            let id = text(e, "excerpt_id")?;
            if !ids.insert(id) {
                return Err("Duplicate identifier".into());
            }
            excerpt_ids.insert(id);
            let bytes = text(e, "text")?.as_bytes();
            let start = e["byte_start"].as_u64().ok_or("Invalid excerpt start")?;
            let end = e["byte_end"].as_u64().ok_or("Invalid excerpt end")?;
            if end <= start
                || end - start != bytes.len() as u64
                || e["sha256"] != crate::util::sha256_hex(bytes)
            {
                return Err("Excerpt interval/digest mismatch".into());
            }
            let a = text(e, "anchor")?;
            let pieces: Vec<_> = a.split("-L").collect();
            let from = pieces[0]
                .trim_start_matches('L')
                .parse::<u64>()
                .map_err(|_| "Invalid line anchor")?;
            let to = if pieces.len() == 2 {
                pieces[1]
                    .parse::<u64>()
                    .map_err(|_| "Invalid line anchor")?
            } else {
                from
            };
            if to < from {
                return Err("Reversed line anchor".into());
            }
            let count = bytes.iter().filter(|b| **b == b'\n').count()
                + usize::from(bytes.last() != Some(&b'\n'));
            if count as u64 != to - from + 1 || from == 1 && start != 0 {
                return Err("Excerpt line/interval internal mismatch".into());
            }
        }
    }
    for i in array(v, "interpretations")? {
        if !ids.insert(text(i, "interpretation_id")?) {
            return Err("Duplicate identifier".into());
        }
        for (key, known) in [("source_ids", &source_ids), ("excerpt_ids", &excerpt_ids)] {
            let mut seen = HashSet::new();
            for r in array(i, key)? {
                let r = r.as_str().ok_or("Invalid reference")?;
                if !known.contains(r) || !seen.insert(r) {
                    return Err("Dangling/duplicate interpretation reference".into());
                }
            }
        }
    }
    let mut duties = HashSet::new();
    for d in array(v, "duties")? {
        if !duties.insert(text(d, "duty")?) {
            return Err("Duplicate duty".into());
        }
    }
    if duties
        != HashSet::from([
            "locate_compare",
            "review_integrate",
            "cross_undertaking_coordination",
        ])
    {
        return Err("Exactly one of each duty required".into());
    }
    for g in array(v, "gaps")? {
        let c = &g["context"];
        let side = text(c, "side")?;
        if side == "general" {
            if !c["requested_commit"].is_null() {
                return Err("General gap cannot assert side commit".into());
            }
        } else if c["requested_commit"] != req[side] || req[side].is_null() {
            return Err("Gap/request revision mismatch".into());
        }
        if let Some(p) = c["path"].as_str() {
            if !literal_path(p) {
                return Err("Invalid gap path".into());
            }
        }
        if g["origin"] == "observed_git_failure"
            && (side == "general" || c["path"].is_null() || sides.contains(side))
        {
            return Err("Inconsistent observed failed-side gap".into());
        }
    }
    for g in array(v, "gaps")? {
        if g["origin"] == "observed_git_failure" {
            paths.insert(text(&g["context"], "path")?);
        }
    }
    if paths.len() > 1
        || req["since"]
            .as_str()
            .is_some_and(|s| s.len() != req["at"].as_str().unwrap_or("").len())
    {
        return Err("Inconsistent single-path/request format receipt".into());
    }
    Ok(())
}
use serde::Deserialize;
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SourceChoice {
    pub reference: String,
    pub role: String,
    pub anchors: Vec<String>,
}
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct InterpretationInput {
    pub statement: String,
    pub asserted_by: String,
    pub source_references: Vec<String>,
    pub anchor_references: Vec<String>,
}
#[derive(Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DutyInput {
    pub duty: String,
    pub standing: String,
    pub reason: String,
}
#[derive(Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Responsibility {
    pub standing: String,
    pub identity: Option<String>,
}
#[derive(Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GapInput {
    pub gap: String,
    pub effect: String,
    pub responsible: Responsibility,
}
#[derive(Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct UnsupportedInput {
    pub conclusion: String,
    pub why: String,
}
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct PrepareInput {
    pub session_token: String,
    pub generation: String,
    pub git_reference: String,
    pub connector: String,
    pub sources: Vec<SourceChoice>,
    pub interpretations: Vec<InterpretationInput>,
    pub gaps: Vec<GapInput>,
    pub unsupported: Vec<UnsupportedInput>,
    pub duties: Vec<DutyInput>,
}
#[cfg(unix)]
pub(crate) fn compose(
    e: &crate::connector_source::MaterializationEvidence,
    input: &PrepareInput,
    recorder: &str,
) -> Result<Value, String> {
    let account = compose_base(e, input, recorder)?;
    crate::connector_route_store::validate_account(&account).map_err(|e| e.to_string())?;
    Ok(account)
}
#[cfg(unix)]
pub(crate) fn compose_base(
    e: &crate::connector_source::MaterializationEvidence,
    input: &PrepareInput,
    recorder: &str,
) -> Result<Value, String> {
    use crate::util::{now_rfc3339, opaque_id, sha256_hex};
    use std::collections::HashMap;
    if e.question["askedRevision"] != e.request["at"]
        || e.question["sinceRevision"] != e.request["since"]
    {
        return Err(format!("Frozen question/Git pins mismatch: question at {} since {}; Git at {} since {}. Start a new explicit question preparation.",e.question["askedRevision"],e.question["sinceRevision"],e.request["at"],e.request["since"]));
    }
    let path = e
        .relative
        .to_str()
        .filter(|p| literal_path(p))
        .ok_or("Selected path cannot materialize as exact UTF-8 relative text")?;
    let project = e
        .project
        .to_str()
        .ok_or("Project spelling cannot materialize as exact UTF-8")?;
    if input.sources.len() > 2 || input.interpretations.len() > 32 || input.gaps.len() > 32 {
        return Err("Draft selection count limit exceeded".into());
    }
    if !matches!(input.connector.as_str(), "pec" | "domains") {
        return Err("Explicit pec/domains connector label required".into());
    }
    let responsibility = match &e.responsible {
        Some(id) => json!({"standing":"caller_assigned","identity":id}),
        None => json!({"standing":"unassigned","identity":null}),
    };
    let mut sources = Vec::new();
    let mut source_refs = HashMap::new();
    let mut anchor_refs = HashMap::new();
    let sides = [("at", Some(&e.at)), ("since", e.since.as_ref())];
    for choice in &input.sources {
        if choice.role.trim().is_empty() {
            return Err("Explicit nonempty caller source role required".into());
        }
        if choice.anchors.len() > 16 {
            return Err("At most16 excerpts per source".into());
        }
        let (side, found) = sides
            .iter()
            .find_map(|(side, result)| {
                result
                    .and_then(|r| r.as_ref().ok())
                    .filter(|r| r.view["reference"] == choice.reference)
                    .map(|r| (*side, r))
            })
            .ok_or("Unknown/non-successful selected side reference")?;
        if source_refs.contains_key(&choice.reference) {
            return Err("Duplicate source selection".into());
        }
        let v = &found.view;
        if v["readCommit"] != e.request[side] || v["sha256"] != sha256_hex(&found.bytes) {
            return Err("Retained source bytes/revision mismatch".into());
        }
        let raw = found
            .raw_objects
            .first()
            .filter(|(id, _)| v["readCommit"] == id.as_str())
            .ok_or("Missing retained raw commit")?;
        if v["rawCommitSha256"] != sha256_hex(&raw.1) {
            return Err("Retained commit receipt mismatch".into());
        }
        let source_id = opaque_id("source-")?;
        source_refs.insert(choice.reference.clone(), source_id.clone());
        let mut excerpts = Vec::new();
        for reference in &choice.anchors {
            if anchor_refs.contains_key(reference) {
                return Err("Duplicate excerpt selection".into());
            }
            let a = e
                .anchors
                .iter()
                .find(|a| a["reference"] == reference.as_str())
                .ok_or("Unknown excerpt reference")?;
            if a["gitObservationReference"] != e.git_reference
                || a["sideObservationReference"] != choice.reference
                || a["commit"] != v["readCommit"]
                || a["blob"] != v["blob"]
                || a["blobSha256"] != v["sha256"]
                || a["side"] != side
            {
                return Err("Excerpt belongs to a different source observation".into());
            }
            let start = a["byteStart"].as_u64().ok_or("Invalid excerpt interval")? as usize;
            let end = a["byteEnd"].as_u64().ok_or("Invalid excerpt interval")? as usize;
            let bytes = found
                .bytes
                .get(start..end)
                .ok_or("Excerpt outside retained blob")?;
            let excerpt_text = text(a, "text")?;
            if bytes != excerpt_text.as_bytes() || a["sha256"] != sha256_hex(bytes) {
                return Err("Altered excerpt digest/bytes".into());
            }
            let anchor = text(a, "anchor")?;
            let mut pieces = anchor.split("-L");
            let from = pieces
                .next()
                .unwrap()
                .trim_start_matches('L')
                .parse::<usize>()
                .map_err(|_| "Invalid checked anchor")?;
            let to = pieces
                .next()
                .map(str::parse::<usize>)
                .transpose()
                .map_err(|_| "Invalid checked anchor")?
                .unwrap_or(from);
            let checked =
                crate::connector_source::excerpt(&found.bytes, from, to, Some(excerpt_text))?;
            if checked["byteStart"] != a["byteStart"] || checked["byteEnd"] != a["byteEnd"] {
                return Err("Checked line/byte interval mismatch".into());
            }
            let id = opaque_id("excerpt-")?;
            anchor_refs.insert(reference.clone(), id.clone());
            excerpts.push(json!({"excerpt_id":id,"anchor":anchor,"byte_start":start,"byte_end":end,"text":excerpt_text,"sha256":sha256_hex(bytes),"standing":"exact_byte_inclusion_only"}));
        }
        sources.push(json!({"source_id":source_id,"path":path,"revision":v["readCommit"],"sha256":sha256_hex(&found.bytes),"role":choice.role,"role_standing":"caller_assertion","provenance":{"side":side,"object_format":e.association["objectFormat"],"commit":v["readCommit"],"root_tree":v["rootTree"],"blob":v["blob"],"mode":v["mode"],"raw_commit_sha256":sha256_hex(&raw.1),"traversal_sha256":sha256_hex(&serde_json::to_vec(&v["traversed"]).map_err(|e|e.to_string())?),"observed_at":v["observedAt"],"time_provenance":"observed_clock","verification":"same_engine_object_id_consistency","observation_reference":choice.reference},"excerpts":excerpts}));
    }
    let mut interpretations = Vec::new();
    for i in &input.interpretations {
        let refs = i
            .source_references
            .iter()
            .map(|r| {
                source_refs
                    .get(r)
                    .cloned()
                    .ok_or("Interpretation references unselected source")
            })
            .collect::<Result<Vec<_>, _>>()?;
        let anchors = i
            .anchor_references
            .iter()
            .map(|r| {
                anchor_refs
                    .get(r)
                    .cloned()
                    .ok_or("Interpretation references unselected excerpt")
            })
            .collect::<Result<Vec<_>, _>>()?;
        interpretations.push(json!({"interpretation_id":opaque_id("interpretation-")?,"statement":i.statement,"asserted_by":i.asserted_by,"attribution_standing":"caller_asserted_identity","standing":"unreviewed_caller_interpretation","source_ids":refs,"excerpt_ids":anchors}));
    }
    let mut gaps = Vec::new();
    for (side, result) in sides {
        if let Some(Err(f)) = result {
            gaps.push(json!({"origin":"observed_git_failure","gap":format!("{}: {}",f.kind,f.detail),"effect":"No successful source evidence for this requested side","responsible":responsibility,"context":{"side":side,"requested_commit":e.request[side],"path":path}}));
        }
    }
    gaps.push(json!({"origin":"producer_limit","gap":"Source evidence draft only; factual reconstruction and reliance remain unestablished","effect":"No facts, supported conclusions or performed duties","responsible":responsibility,"context":{"side":"general","requested_commit":null,"path":null}}));
    for g in &input.gaps {
        gaps.push(json!({"origin":"caller_reported","gap":g.gap,"effect":g.effect,"responsible":{"standing":g.responsible.standing,"identity":g.responsible.identity},"context":{"side":"general","requested_commit":null,"path":null}}));
    }
    let mut duties = Vec::new();
    for d in &input.duties {
        let role = match d.duty.as_str() {
            "locate_compare" => "agent",
            "review_integrate" => "manager",
            "cross_undertaking_coordination" => "person",
            _ => return Err("Unknown duty".into()),
        };
        if d.reason.trim().is_empty() {
            return Err("Explicit duty reason required".into());
        }
        duties.push(json!({"duty":d.duty,"actor_role":role,"standing":d.standing,"reason":d.reason,"assertion_standing":"caller_reported_unverified"}));
    }
    let identity = e.root.project_identity()?;
    let mut question = json!({"id":e.question["id"],"text":e.question["text"],"at_revision":e.question["askedRevision"]});
    if !e.question["sinceRevision"].is_null() {
        question["since_revision"] = e.question["sinceRevision"].clone();
    }
    let mut unsupported = vec![
        json!({"conclusion":"Factual reconstruction and reliance","why":"Source-evidence draft only; no reviewed reconstruction or reliance established"}),
    ];
    unsupported.extend(
        input
            .unsupported
            .iter()
            .map(|u| json!({"conclusion":u.conclusion,"why":u.why})),
    );
    let account = json!({"format":"chirality.connector.route-account","formatVersion":"0.3","account_id":format!("ra:{}",opaque_id("")?),"standing":"source_evidence_draft","question":question,"trigger":{"connector":input.connector,"why":format!("Constructed {} trigger; no actual connector standing established",e.trigger),"standing":"constructed","receiving_records":[]},"sources":sources,"facts":[],"interpretations":interpretations,"gaps":gaps,"conclusions":{"supported":[],"unsupported":unsupported,"prohibited":["no_work","ready","permitted","correct_by_presence"]},"duties":duties,"recorder":{"kind":"app","identity":recorder},"written_at":now_rfc3339(),"written_at_source":"observed_clock","evidence":{"kind":"host_observed_git_receipt","project_identity":{"device":identity.device.to_string(),"inode":identity.inode.to_string()},"project_display":project,"association_sha256":sha256_hex(&serde_json::to_vec(&e.association).map_err(|e|e.to_string())?),"engine_sha256":sha256_hex(&serde_json::to_vec(&e.engine).map_err(|e|e.to_string())?),"git_request":{"at":e.request["at"],"since":e.request["since"]},"selection_mechanism":e.mechanism,"verification_limit":"same_engine_consistency_not_truth_authorship_or_authority","custody_limit":"stored_receipt_not_hot_capability_or_independent_reverification"}});
    Ok(account)
}
#[cfg(all(test, any(target_os = "macos", target_os = "linux")))]
#[path = "connector_materialization_tests.rs"]
pub(crate) mod tests;
#[cfg(any(target_os = "macos", target_os = "linux"))]
mod registry {
    use super::*;
    use crate::{
        connector_route_store::{Attempt, BoundReference, ProjectRouteStore, StoreError},
        connector_source::{MaterializationEvidence, Session},
        connector_source_fs::Root,
        util::{opaque_id, sha256_hex},
    };
    use std::{
        collections::BTreeMap,
        path::{Path, PathBuf},
        sync::{Arc, Mutex},
    };
    const CAPACITY: usize = 64;
    struct Payload {
        bytes: Vec<u8>,
        session: String,
        source_generation: String,
        git: String,
        local: String,
        root: Arc<Root>,
        store: Arc<ProjectRouteStore>,
        relative: PathBuf,
        association: String,
    }
    struct PublishedCustody { store:Arc<ProjectRouteStore>, reference:BoundReference, project:PathBuf }
    struct Entry {
        generation: String,
        account_id: String,
        status: &'static str,
        payload: Option<Payload>,
        outcome: Value,
        reconciliation: Value,
        recovery: Option<(Arc<ProjectRouteStore>, Attempt)>,
        published:Option<Arc<PublishedCustody>>,
        custody_revision:u64,
    }
    pub struct Registry {
        recorder: Result<String, String>,
        entries: BTreeMap<String, Entry>,
        inflight: Option<String>,
        revision: u128,
        inspection:Option<u64>,
        next_inspection:u64,
    }
    impl Default for Registry {
        fn default() -> Self {
            Self {
                recorder: opaque_id("app-instance-"),
                entries: BTreeMap::new(),
                inflight: None,
                revision: 0,
                inspection:None,next_inspection:0,
            }
        }
    }
    impl Registry {
        pub fn view(&self) -> Value {
            json!({"revision":self.revision.to_string(),"capacity":CAPACITY,"used":self.entries.len(),"inflight":self.inflight,"limit":"Development safety bound, not final product capacity. No eviction/reset/retry or restart recovery is provided.","entries":self.entries.iter().map(|(token,e)|json!({"token":token,"generation":e.generation,"accountId":e.account_id,"status":e.status,"recheckAvailable":e.status=="published"&&e.published.as_ref().is_some_and(|p|matches!(p.reference.format_version.as_str(),"0.3"|"0.4")),"outcomeText":serde_json::to_string_pretty(&e.outcome).unwrap(),"reconciliationText":serde_json::to_string_pretty(&e.reconciliation).unwrap(),"draft":e.payload.as_ref().map(|p|json!({"account":serde_json::from_slice::<Value>(&p.bytes).unwrap(),"byteLength":p.bytes.len(),"sha256":sha256_hex(&p.bytes)}))})).collect::<Vec<_>>()})
        }
        fn entry(&mut self, token: &str, generation: &str) -> Result<&mut Entry, String> {
            self.entries
                .get_mut(token)
                .filter(|e| e.generation == generation)
                .ok_or_else(|| {
                    "Unknown draft identity/generation; cold records cannot revive tokens".into()
                })
        }
        pub fn retained(&self, token: &str, generation: &str) -> Result<Option<Value>, String> {
            let e = self
                .entries
                .get(token)
                .filter(|e| e.generation == generation)
                .ok_or("Unknown draft identity/generation")?;
            Ok(if e.status == "prepared" {
                None
            } else {
                Some(self.view())
            })
        }
        pub fn cancel(&mut self, token: &str, generation: &str) -> Result<Value, String> {
            let e = self.entry(token, generation)?;
            if e.status == "prepared" {
                e.status = "cancelled";
                e.payload = None;
                e.outcome = json!({"state":"cancelled_before_publish","effect":"No publication attempted; token consumed"});
            }
            // Publishing/completed outcomes are never replaced by a cancellation claim.
            self.revision += 1;
            Ok(self.view())
        }
        pub fn reconcile(&mut self, token: &str, generation: &str) -> Result<Value, String> {
            let e = self.entry(token, generation)?;
            if let Some((store, attempt)) = &e.recovery {
                e.reconciliation = match store.reconcile(attempt) {
                    Ok(observed) => {
                        json!({"state":"observed_after_uncertainty","reference":observed.reference,"limit":"Original uncertain publication retained; this read does not establish prior durability/success"})
                    }
                    Err(error) => json!({"state":"reconciliation_failed","error":error}),
                };
            }
            self.revision += 1;
            Ok(self.view())
        }
    }
    pub fn prepare(
        registry: &Mutex<Registry>,
        source: &Mutex<Session>,
        input: PrepareInput,
        project: &Path,
    ) -> Result<Value, String> {
        prepare_with(registry, source, input, project, || {})
    }
    pub(super) fn prepare_with(
        registry: &Mutex<Registry>,
        source: &Mutex<Session>,
        input: PrepareInput,
        project: &Path,
        hook: impl FnOnce(),
    ) -> Result<Value, String> {
        prepare_composed(registry, source, input, project, hook, compose)
    }
    pub(crate) fn prepare_composed(
        registry: &Mutex<Registry>,
        source: &Mutex<Session>,
        input: PrepareInput,
        project: &Path,
        hook: impl FnOnce(),
        composer: impl FnOnce(&MaterializationEvidence, &PrepareInput, &str) -> Result<Value, String>,
    ) -> Result<Value, String> {
        let mut registry = registry.lock().map_err(|_| "Draft registry unavailable")?;
        if registry.inflight.is_some() {
            return Err("Publication in flight; no second payload or new preparation".into());
        }
        if registry.entries.len() >= CAPACITY {
            return Err("App-instance64 identity development capacity reached; retained outcomes remain available for inspection/reconciliation. No slot reset or retry offered".into());
        }
        let e = source
            .lock()
            .map_err(|_| "Source state unavailable")?
            .materialization_evidence(
                &input.session_token,
                &input.generation,
                &input.git_reference,
            )?;
        if e.project != project.canonicalize().map_err(|e| e.to_string())? {
            return Err("Explicit App project differs from source project".into());
        }
        let store = Arc::new(ProjectRouteStore::open(project).map_err(|e| e.to_string())?);
        if store.project_identity() != e.root.project_identity()? {
            return Err("Opened writer/source project identity mismatch".into());
        }
        e.root.verify()?;
        crate::connector_git::recheck_association(
            &e.project,
            &e.relative,
            &sha256_hex(&serde_json::to_vec(&e.association).map_err(|e| e.to_string())?),
        )?;
        let account = composer(
            &e,
            &input,
            registry.recorder.as_ref().map_err(Clone::clone)?,
        )?;
        let bytes = serde_json::to_vec(&account).map_err(|e| e.to_string())?;
        if bytes.len() > BYTE_LIMIT {
            return Err("Frozen serialization exceeds1MiB".into());
        }
        hook();
        // Registry then source is the sole nested lock order. Hold source through atomic freeze.
        let mut source_guard = source
            .lock()
            .map_err(|_| "Source state unavailable at freeze")?;
        let latest = source_guard.materialization_evidence(
            &input.session_token,
            &input.generation,
            &input.git_reference,
        )?;
        if latest.local_reference != e.local_reference
            || latest.root.project_identity()? != store.project_identity()
            || latest.association != e.association
        {
            return Err("Source became stale during preparation; no identity reserved".into());
        }
        crate::connector_git::recheck_association(
            &latest.project,
            &latest.relative,
            &account["evidence"]["association_sha256"].as_str().unwrap(),
        )?;
        // All failure-prone work precedes reservation/replacement. Final IDs are private until this insertion.
        let token = opaque_id("draft-")?;
        let generation = opaque_id("draft-generation-")?;
        let payload = Payload {
            bytes,
            session: input.session_token,
            source_generation: input.generation,
            git: e.git_reference,
            local: e.local_reference,
            root: e.root,
            store,
            relative: e.relative,
            association: account["evidence"]["association_sha256"]
                .as_str()
                .unwrap()
                .into(),
        };
        for old in registry.entries.values_mut() {
            if old.status == "prepared" {
                old.status = "superseded";
                old.payload = None;
                old.outcome = json!({"state":"superseded_before_publish","effect":"No publication; token consumed by explicit replacement"});
            }
        }
        registry.entries.insert(
            token,
            Entry {
                generation,
                account_id: account["account_id"].as_str().unwrap().into(),
                status: "prepared",
                payload: Some(payload),
                outcome: Value::Null,
                reconciliation: Value::Null,
                recovery: None,
                published:None,custody_revision:0,
            },
        );
        registry.revision += 1;
        Ok(registry.view())
    }
    fn prepublish(
        payload: &Payload,
        source: &Mutex<Session>,
        project: &Path,
    ) -> Result<Value, String> {
        let current: MaterializationEvidence = source
            .lock()
            .map_err(|_| "Source state unavailable")?
            .materialization_evidence(&payload.session, &payload.source_generation, &payload.git)?;
        if current.local_reference != payload.local
            || current.root.project_identity()? != payload.store.project_identity()
        {
            return Err("Source/writer capability changed".into());
        }
        if project.canonicalize().map_err(|e| e.to_string())? != payload.store.resolved_project() {
            return Err("App project changed before publication".into());
        }
        payload.root.verify()?;
        crate::connector_git::recheck_association(
            payload.store.resolved_project(),
            &payload.relative,
            &payload.association,
        )?;
        let account: Value = serde_json::from_slice(&payload.bytes).map_err(|e| e.to_string())?;
        crate::connector_route_store::validate_account(&account).map_err(|e| e.to_string())?;
        if serde_json::to_vec(&account).map_err(|e| e.to_string())? != payload.bytes {
            return Err("Frozen publication serialization mismatch".into());
        }
        let discovery = payload.store.discover();
        if !discovery.enumeration_complete
            || discovery
                .by_account_id
                .values()
                .any(|paths| paths.len() > 1)
        {
            return Err(format!(
                "Duplicate identities or incomplete account discovery; no write: {}",
                json!({"issues":discovery.issues,"byAccountId":discovery.by_account_id,"enumerationComplete":discovery.enumeration_complete})
            ));
        }
        if discovery
            .by_account_id
            .contains_key(account["account_id"].as_str().unwrap())
        {
            return Err("Account identity already exists; no duplicate publication".into());
        }
        Ok(account)
    }
    fn refusal(kind: &str, detail: impl Into<String>) -> Value {
        json!({"kind":kind,"detail":detail.into()})
    }
    struct InspectionLease<'a> {
        registry: &'a Mutex<Registry>,
        revision: u64,
    }
    impl Drop for InspectionLease<'_> {
        fn drop(&mut self) {
            // All registry guards are in inner scopes and drop before this lease.
            let mut r = self
                .registry
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            if r.inspection == Some(self.revision) {
                r.inspection = None;
            }
        }
    }
    pub fn recheck(
        registry: &Mutex<Registry>,
        token: &str,
        generation: &str,
        project: impl FnMut() -> Result<PathBuf, String>,
    ) -> Result<Value, Value> {
        recheck_using(registry, token, generation, project, |s, r, p| {
            s.inspect_published(r, p)
        })
    }
    pub(super) fn recheck_using(
        registry: &Mutex<Registry>,
        token: &str,
        generation: &str,
        mut project: impl FnMut() -> Result<PathBuf, String>,
        inspect: impl FnOnce(&ProjectRouteStore, &BoundReference, &Path) -> Value,
    ) -> Result<Value, Value> {
        let before = project().map_err(|e| refusal("unavailable", e))?;
        let (custody, entry_cut, lease_cut) = {
            let mut r = registry.try_lock().map_err(|e| match e {
                std::sync::TryLockError::WouldBlock => {
                    refusal("busy", "Registry busy; no inspection queued")
                }
                std::sync::TryLockError::Poisoned(_) => refusal("unavailable", "Registry unavailable"),
            })?;
            if r.inspection.is_some() {
                return Err(refusal(
                    "busy",
                    "An inspection is already in flight; no second read queued",
                ));
            }
            let e = r
                .entries
                .get(token)
                .filter(|e| e.generation == generation)
                .ok_or_else(|| refusal("invalid_token", "Unknown original token/generation"))?;
            let custody = e
                .published
                .as_ref()
                .filter(|_| e.status == "published")
                .cloned()
                .ok_or_else(|| {
                    refusal(
                        "unavailable",
                        "Original typed published custody unavailable; no JSON/cold reconstruction",
                    )
                })?;
            if !matches!(custody.reference.format_version.as_str(), "0.3" | "0.4") {
                return Err(refusal(
                    "unavailable",
                    "Published version is outside direct inspection",
                ));
            }
            if before != custody.project {
                return Err(refusal(
                    "stale",
                    "Current explicit project association differs from publication",
                ));
            }
            let entry_cut = e.custody_revision;
            let lease_cut = r
                .next_inspection
                .checked_add(1)
                .ok_or_else(|| refusal("unavailable", "Inspection revision exhausted"))?;
            r.next_inspection = lease_cut;
            r.inspection = Some(lease_cut);
            (custody, entry_cut, lease_cut)
        };
        let lease = InspectionLease {
            registry,
            revision: lease_cut,
        };
        let observation = inspect(&custody.store, &custody.reference, &before);
        let after = project().map_err(|e| refusal("stale", e))?;
        if before != after {
            return Err(refusal(
                "stale",
                "Project association changed during inspection",
            ));
        }
        {
            let r = registry
                .lock()
                .map_err(|_| refusal("unavailable", "Registry unavailable after inspection"))?;
            let valid = r.inspection == Some(lease_cut)
                && r.entries.get(token).is_some_and(|e| {
                    e.generation == generation
                        && e.status == "published"
                        && e.custody_revision == entry_cut
                        && e.published
                            .as_ref()
                            .is_some_and(|p| Arc::ptr_eq(p, &custody))
                });
            if !valid {
                return Err(refusal(
                    "stale",
                    "Entry/custody/inspection changed; result discarded",
                ));
            }
        }
        drop(lease);
        Ok(
            json!({"token":token,"generation":generation,"inspectionRevision":lease_cut.to_string(),"inspection":observation}),
        )
    }
    #[cfg(test)]
    impl Registry {
        pub(super) fn test_forget_published(&mut self, token: &str) {
            self.entries.get_mut(token).unwrap().published = None;
        }
        pub(super) fn test_change_entry_cut(&mut self, token: &str) {
            self.entries.get_mut(token).unwrap().custody_revision += 1;
        }
        pub(super) fn test_replace_lease(&mut self) -> u64 {
            self.next_inspection += 1;
            self.inspection = Some(self.next_inspection);
            self.next_inspection
        }
        pub(super) fn test_lease(&self) -> Option<u64> {
            self.inspection
        }
        pub(super) fn test_resources(&self) -> (usize, usize, usize) {
            let mut roots = std::collections::HashSet::new();
            let mut metadata = 0;
            let mut payload = 0;
            for e in self.entries.values() {
                if let Some(p) = &e.published {
                    roots.insert(Arc::as_ptr(&p.store) as usize);
                    metadata += std::mem::size_of::<PublishedCustody>()
                        + 4 * std::mem::size_of::<usize>()
                        + p.store.retained_size()
                        + p.project.capacity()
                        + p.reference.relative_path.capacity()
                        + p.reference.account_id.capacity()
                        + p.reference.format_version.capacity()
                        + p.reference.sha256.capacity()
                        + p.reference.directories.capacity()
                            * std::mem::size_of::<crate::connector_route_store::FileIdentity>();
                }
                if let Some(p) = &e.payload {
                    payload += p.bytes.capacity();
                }
            }
            (roots.len(), metadata, payload)
        }
    }
    pub fn publish(
        registry: &Mutex<Registry>,
        source: &Mutex<Session>,
        token: &str,
        generation: &str,
        project: &Path,
    ) -> Result<Value, String> {
        publish_with(
            registry,
            source,
            token,
            generation,
            project,
            |store, account| store.write(account),
        )
    }
    pub(super) fn publish_with(
        registry: &Mutex<Registry>,
        source: &Mutex<Session>,
        token: &str,
        generation: &str,
        project: &Path,
        writer: impl FnOnce(&ProjectRouteStore, &Value) -> Result<BoundReference, StoreError>,
    ) -> Result<Value, String> {
        let payload = {
            let mut r = registry.lock().map_err(|_| "Draft registry unavailable")?;
            let e = r.entry(token, generation)?;
            if e.status != "prepared" {
                return Ok(r.view());
            }
            let p = e.payload.take().ok_or("Prepared payload unavailable")?;
            e.status = "publishing";
            r.inflight = Some(token.into());
            r.revision += 1;
            p
        };
        let (status, outcome, recovery, published) = match prepublish(&payload, source, project) {
            Err(reason) => (
                "refused",
                json!({"state":"refused_before_write","reason":reason,"effect":"No writer invocation; token consumed"}),
                None,None,
            ),
            Ok(account) => match writer(&payload.store, &account) {
                Ok(reference) => (
                    "published",
                    json!({"state":"published","reference":reference,"limit":"Exact CRP result; no source truth or duty claim"}),
                    None,Some(Arc::new(PublishedCustody{store:payload.store.clone(),reference,project:project.to_path_buf()})),
                ),
                Err(error) => {
                    let recovery = error
                        .attempt
                        .as_ref()
                        .map(|a| (payload.store.clone(), a.clone()));
                    (
                        if error.uncertain_commit {
                            "uncertain"
                        } else {
                            "refused"
                        },
                        json!({"state":if error.uncertain_commit{"uncertain"}else{"definite_refusal"},"error":error,"limit":"No automatic retry, rollback or unlink"}),
                        recovery,None,
                    )
                }
            },
        };
        drop(payload); // No retained full payload after an actual outcome.
        let mut r = registry
            .lock()
            .map_err(|_| format!("Draft registry installation unavailable after writer returned; actual writer outcome (not an admitted entry): {outcome}"))?;
        let e = r.entry(token, generation).map_err(|error|format!("{error}; registry installation failed; actual writer outcome (not an admitted entry): {outcome}"))?;
        e.status = status;
        e.outcome = outcome;
        e.recovery = recovery;
        e.published=published;
        if e.published.is_some(){e.custody_revision=1;}
        r.inflight = None;
        r.revision += 1;
        Ok(r.view())
    }
}
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub(crate) use registry::prepare_composed;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use registry::{prepare, publish, recheck, Registry};
#[cfg(not(any(target_os = "macos", target_os = "linux")))]
#[derive(Default)]
pub struct Registry;
#[cfg(not(any(target_os = "macos", target_os = "linux")))]
impl Registry {
    pub fn view(&self) -> Value {
        json!({"unsupported":"Materialization requires supported project/writer capabilities"})
    }
}
