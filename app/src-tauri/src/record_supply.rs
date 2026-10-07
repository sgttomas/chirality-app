//! CC-RS-WR-SUPPLY-FIT: WR/RS correspondence.
//!
//! Resolved immutable evidence can reconstruct a historical claim, but cannot
//! recreate the source-owned comparison or authorize a new supplied_guidance
//! append. Only the live path below appends R3, and only from a typed
//! `PublishedSupplyCheck` that Root minted at the genuine native boundary.
use crate::workflow_workspace::publication::{
    ProjectRecords, PublishedSupplyCheck, ResolvedRecord,
};
use serde_json::{json, Value};

/// Storage key of the App's live workflow-supply R3 writer (one log per run).
pub(crate) const LIVE_WRITER: &str = "app-workflow-supply-writer";

/// One pending live R3 observation (W-1/W-2). The reserved record identity and
/// the original observation time (the check's read time) survive failed writes;
/// it is held in memory only, so a stopped process loses it (WP-5, W-2).
#[derive(Debug)]
pub struct PendingSuppliedGuidance {
    run: String,
    record_id: String,
    observed_at: String,
    check_ref: String,
    body: Value,
    failure: Option<String>,
}
impl PendingSuppliedGuidance {
    pub fn record_id(&self) -> &str {
        &self.record_id
    }
    pub fn body(&self) -> &Value {
        &self.body
    }
    pub fn failure(&self) -> Option<&str> {
        self.failure.as_deref()
    }
}
/// Prepare R3 from a check this process minted and published. Both supplier
/// references must resolve in the explicit project (RS §13.6a).
pub(crate) fn prepare_live(
    project: &ProjectRecords,
    published: &PublishedSupplyCheck,
) -> Result<PendingSuppliedGuidance, CorrespondenceError> {
    let joined = correspond(project, published.run_text(), published.check())?;
    let observed_at = published.check().envelope()["observed_at"]
        .as_str()
        .filter(|s| !s.is_empty())
        .ok_or_else(|| invalid("check observation time absent"))?
        .to_owned();
    Ok(PendingSuppliedGuidance {
        run: joined.run,
        record_id: crate::util::opaque_id("rec:app:").map_err(invalid)?,
        observed_at,
        check_ref: published.check().reference().to_owned(),
        body: joined.body,
        failure: None,
    })
}
/// Append (or late-append) one live R3 entry. Joins are re-validated at write
/// time; an uncertain earlier write that did land is recognised by its reserved
/// identity and exact body, never written twice; a late write is followed by
/// W-2's "record write failed" limit. Nothing here sends or re-reads native data.
pub(crate) fn append_live(
    project: &ProjectRecords,
    published: &PublishedSupplyCheck,
    pending: &mut PendingSuppliedGuidance,
) -> Result<Value, String> {
    let root = project.root().to_owned();
    let current =
        correspond(project, published.run_text(), published.check()).map_err(|e| e.to_string())?;
    if current.body != pending.body
        || current.run != pending.run
        || published.check().reference() != pending.check_ref
    {
        return Err("R3 supplier joins changed since preparation; nothing written".into());
    }
    let (entries, limits) = crate::storage::read_all(&root);
    if !limits.is_empty() {
        let error = format!("RS record set incomplete; nothing written: {limits:?}");
        pending.failure.get_or_insert(error.clone());
        return Err(error);
    }
    let written = match entries
        .iter()
        .find(|e| e["recordId"].as_str() == Some(pending.record_id.as_str()))
    {
        Some(existing)
            if existing["kind"] == "supplied_guidance"
                && existing["body"] == pending.body
                && existing["runId"] == pending.run.as_str()
                && existing["observedAt"] == pending.observed_at.as_str() =>
        {
            existing.clone()
        }
        Some(_) => {
            return Err(format!(
                "R3 identity {} already holds other content; nothing written",
                pending.record_id
            ))
        }
        None => match crate::records::append_project_reserved(
            &root,
            &pending.run,
            LIVE_WRITER,
            "supplied_guidance",
            &crate::records::APP_WRITER,
            pending.body.clone(),
            &pending.record_id,
            &pending.observed_at,
        ) {
            Ok(entry) => entry,
            Err(error) => {
                pending.failure.get_or_insert(error.clone());
                return Err(error);
            }
        },
    };
    if let Some(failure) = &pending.failure {
        crate::records::note_project_late_write(
            &root,
            &pending.run,
            LIVE_WRITER,
            &pending.record_id,
            &format!("supplied_guidance written after its original observation; first failure: {failure}"),
        )?;
    }
    Ok(written)
}

/// One pending RS lifecycle entry (`run_opened`, `run_ended`) for a run log.
/// Its reserved identity and original observation time survive failed writes.
#[derive(Debug, Clone)]
pub struct PendingRunEntry {
    pub kind: &'static str,
    pub body: Value,
    pub record_id: String,
    pub observed_at: String,
    pub failure: Option<String>,
    pub written: Option<Value>,
}
impl PendingRunEntry {
    pub fn new(kind: &'static str, body: Value, observed_at: String) -> Result<Self, String> {
        Ok(Self {
            kind,
            body,
            record_id: crate::util::opaque_id("rec:app:")?,
            observed_at,
            failure: None,
            written: None,
        })
    }
}
/// W-1/W-2 for one lifecycle entry in the run's log: idempotent for an uncertain
/// earlier write (same identity and content), late writes followed by "record
/// write failed". Never sends or reads native data.
pub(crate) fn append_run_entry(
    root: &std::path::Path,
    run: &str,
    entry: &mut PendingRunEntry,
) -> Result<Value, String> {
    if let Some(written) = &entry.written {
        return Ok(written.clone());
    }
    let (entries, limits) = crate::storage::read_all(root);
    if !limits.is_empty() {
        let error = format!("RS record set incomplete; nothing written: {limits:?}");
        entry.failure.get_or_insert(error.clone());
        return Err(error);
    }
    let written = match entries
        .iter()
        .find(|e| e["recordId"].as_str() == Some(entry.record_id.as_str()))
    {
        Some(existing)
            if existing["kind"] == entry.kind
                && existing["body"] == entry.body
                && existing["runId"] == run
                && existing["observedAt"] == entry.observed_at.as_str() =>
        {
            existing.clone()
        }
        Some(_) => {
            return Err(format!(
                "RS identity {} already holds other content; nothing written",
                entry.record_id
            ))
        }
        None => match crate::records::append_project_reserved(
            root,
            run,
            LIVE_WRITER,
            entry.kind,
            &crate::records::APP_WRITER,
            entry.body.clone(),
            &entry.record_id,
            &entry.observed_at,
        ) {
            Ok(written) => written,
            Err(error) => {
                entry.failure.get_or_insert(error.clone());
                return Err(error);
            }
        },
    };
    if let Some(failure) = &entry.failure {
        crate::records::note_project_late_write(
            root,
            run,
            LIVE_WRITER,
            &entry.record_id,
            &format!("{} written after its original observation; first failure: {failure}", entry.kind),
        )?;
    }
    entry.written = Some(written.clone());
    Ok(written)
}

/// One run's lifecycle as the project's records show it after process-state
/// loss (EXEC RE-4, RE-7; RS R1/R8). Never derived from native turns.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RecordedLifecycle {
    /// `run_opened` without `run_ended`, in a complete record: still live (RE-7);
    /// after relaunch it is interrupted (RE-4), not ended.
    OpenInterrupted,
    Ended { stopped_by: String, cause: String },
    /// A published run-start text with no `run_opened`: the start was not
    /// confirmed in the record (refused, unknown outcome, or a lost write).
    StartNotConfirmed,
    Unknown(String),
}
#[derive(Debug, Clone)]
pub struct RecordedRun {
    pub run: String,
    pub conversation: Option<String>,
    pub follows: Option<String>,
    pub workflow: Value,
    pub lifecycle: RecordedLifecycle,
    pub restart_interruptions: Vec<Value>,
}
#[derive(Debug, Clone)]
pub struct RunsReading {
    pub runs: Vec<RecordedRun>,
    pub limits: Vec<String>,
}
impl RunsReading {
    /// Runs this record shows as live (opened, not ended) in a conversation.
    pub fn live_in(&self, conversation: &str) -> Vec<&RecordedRun> {
        self.runs
            .iter()
            .filter(|r| {
                r.conversation.as_deref() == Some(conversation)
                    && r.lifecycle == RecordedLifecycle::OpenInterrupted
            })
            .collect()
    }
    pub fn view(&self) -> Value {
        json!({"runs":self.runs.iter().map(|r|{
            let (state,detail)=match &r.lifecycle{
                RecordedLifecycle::OpenInterrupted=>("open; interrupted (no run_ended recorded)",json!(null)),
                RecordedLifecycle::Ended{stopped_by,cause}=>("ended",json!({"stoppedBy":stopped_by,"cause":cause})),
                RecordedLifecycle::StartNotConfirmed=>("start not confirmed in record",json!("published run-start text without run_opened")),
                RecordedLifecycle::Unknown(reason)=>("unknown",json!(reason)),
            };
            json!({"run":r.run,"conversation":r.conversation,"follows":r.follows,"workflow":r.workflow,"state":state,"detail":detail,"restartInterruptions":r.restart_interruptions})
        }).collect::<Vec<_>>(),"limits":self.limits,
        "standing":"reopened from project records only; completion is never inferred from a native turn, and no live process run is claimed"})
    }
}
/// Reopen: read the explicit project's RS logs and WR records (and the REC
/// restart facts the caller supplies) into each run's recorded lifecycle.
/// Read-only: nothing is written, ended or repaired here.
pub fn read_project_runs(project: &ProjectRecords, restart_events: &[Value]) -> RunsReading {
    let (entries, rs_limits) = crate::storage::read_all(project.root());
    let mut limits: Vec<String> = rs_limits.clone();
    let complete = rs_limits.is_empty();
    let mut ids: Vec<String> = Vec::new();
    let mut opened: std::collections::BTreeMap<String, Vec<&Value>> = Default::default();
    let mut ended: std::collections::BTreeMap<String, Vec<&Value>> = Default::default();
    for e in &entries {
        let Some(run) = e["runId"].as_str() else { continue };
        match e["kind"].as_str() {
            Some("run_opened") => opened.entry(run.into()).or_default().push(e),
            Some("run_ended") => ended.entry(run.into()).or_default().push(e),
            _ => continue,
        }
        if !ids.iter().any(|i| i == run) {
            ids.push(run.into());
        }
    }
    let mut starts: std::collections::BTreeMap<String, Value> = Default::default();
    match project.list_references() {
        Ok(references) => {
            for reference in references {
                match project.resolve(&reference) {
                    Ok(record)
                        if record.body()["record_kind"] == "run_text"
                            && record.body()["purpose"] == "run start" =>
                    {
                        let run = record.body()["run"].as_str().unwrap_or("").to_owned();
                        if !ids.contains(&run) {
                            ids.push(run.clone());
                        }
                        starts.insert(run, record.body().clone());
                    }
                    Ok(_) => {}
                    Err(e) => limits.push(format!("WR {reference}: {e:?}")),
                }
            }
        }
        Err(e) => limits.push(format!("WR records unreadable: {e}")),
    }
    let runs = ids
        .into_iter()
        .map(|run| {
            let o = opened.get(&run).cloned().unwrap_or_default();
            let x = ended.get(&run).cloned().unwrap_or_default();
            let start = starts.get(&run);
            let conversation = o
                .first()
                .and_then(|e| e["body"]["conversationRef"].as_str())
                .or_else(|| start.and_then(|s| s["conversation"].as_str()))
                .map(str::to_owned);
            let lifecycle = if o.len() > 1 || x.len() > 1 {
                RecordedLifecycle::Unknown("conflicting run_opened/run_ended entries".into())
            } else if let Some(end) = x.first() {
                if o.is_empty() {
                    RecordedLifecycle::Unknown("run_ended without run_opened in the record".into())
                } else {
                    RecordedLifecycle::Ended {
                        stopped_by: end["body"]["stoppedBy"].as_str().unwrap_or("").into(),
                        cause: end["body"]["cause"].as_str().unwrap_or("").into(),
                    }
                }
            } else if !o.is_empty() {
                if complete {
                    RecordedLifecycle::OpenInterrupted
                } else {
                    RecordedLifecycle::Unknown("run_opened recorded; the record set is incomplete, so a run_ended may be unreadable".into())
                }
            } else if complete {
                RecordedLifecycle::StartNotConfirmed
            } else {
                RecordedLifecycle::Unknown("no run_opened readable; the record set is incomplete".into())
            };
            let workflow = o
                .first()
                .map(|e| e["body"]["workflow"].clone())
                .or_else(|| start.map(|s| s["workflow"].clone()))
                .unwrap_or(Value::Null);
            let restart_interruptions = conversation
                .as_deref()
                .map(|c| {
                    restart_events
                        .iter()
                        .filter(|e| e["kind"] == "app_restart_interruption" && e["threadId"] == c)
                        .cloned()
                        .collect()
                })
                .unwrap_or_default();
            RecordedRun {
                follows: o
                    .first()
                    .and_then(|e| e["body"]["follows"].as_str())
                    .map(str::to_owned),
                run,
                conversation,
                workflow,
                lifecycle,
                restart_interruptions,
            }
        })
        .collect();
    RunsReading { runs, limits }
}

/// Durable reading of one explicit project's WR supplier records and their R3
/// entries, for a later process. Historical only: no active run, run end,
/// completion, adoption or live native witness is inferred.
pub fn read_project_supply(project: &ProjectRecords) -> Value {
    let references = match project.list_references() {
        Ok(r) => r,
        Err(e) => {
            return json!({"state":"WR records unreadable","limit":e,"standing":HISTORICAL_LIMIT})
        }
    };
    let (entries, rs_limits) = crate::storage::read_all(project.root());
    let r3: Vec<&Value> = entries
        .iter()
        .filter(|e| e["kind"] == "supplied_guidance")
        .collect();
    let records: Vec<Value> = references
        .iter()
        .map(|reference| match project.resolve(reference) {
            Err(e) => json!({"reference":reference,"resolution":format!("{e:?}")}),
            Ok(record) => {
                let body = record.body();
                let mut view = json!({"reference":reference,"resolution":"resolved","kind":body["record_kind"],"observedAt":record.envelope()["observed_at"],"basis":record.envelope()["basis_records"]});
                for key in ["run", "conversation", "purpose", "state", "turn", "selection_id"] {
                    if let Some(v) = body.get(key) {
                        view[key] = v.clone();
                    }
                }
                if body["record_kind"] == "supply_check" {
                    let citing: Vec<Value> = r3
                        .iter()
                        .filter(|e| e["body"]["supplyCheckRecord"]["ref"] == reference.as_str())
                        .map(|e| {
                            let reading = read_correspondence(project, e);
                            json!({"recordId":e["recordId"],"standing":format!("{:?}",reading.standing),"limits":reading.limits})
                        })
                        .collect();
                    view["r3"] = if citing.is_empty() {
                        json!("missing in record")
                    } else {
                        json!(citing)
                    };
                }
                view
            }
        })
        .collect();
    json!({"project":crate::attachments::native_path_identity(project.root()),"records":records,"rsLimits":rs_limits,"standing":HISTORICAL_LIMIT})
}

const HISTORICAL_LIMIT: &str = "historical correspondence only; no live native witness, model adoption, registration or run lifecycle inferred";

/// Deliberately no Deserialize, Clone, or conversion to a writer capability.
#[derive(Debug)]
pub struct HistoricalSupply {
    run: String,
    body: Value,
    limits: Vec<String>,
}
impl HistoricalSupply {
    pub fn run(&self) -> &str {
        &self.run
    }
    pub fn recorded_claim(&self) -> &Value {
        &self.body
    }
    pub fn limits(&self) -> &[String] {
        &self.limits
    }
}
#[derive(Debug, PartialEq, Eq)]
pub enum CorrespondenceError {
    MissingNativeTurn,
    Invalid(String),
}
impl std::fmt::Display for CorrespondenceError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::MissingNativeTurn => write!(
                f,
                "R3 unavailable: source-bound native turn absent; WR evidence retained"
            ),
            Self::Invalid(reason) => write!(f, "R3 correspondence refused: {reason}"),
        }
    }
}
fn invalid(reason: impl Into<String>) -> CorrespondenceError {
    CorrespondenceError::Invalid(reason.into())
}
fn text<'a>(v: &'a Value, key: &str) -> Result<&'a str, CorrespondenceError> {
    v.get(key)
        .and_then(Value::as_str)
        .filter(|s| !s.is_empty())
        .ok_or_else(|| invalid(format!("{key} absent/empty")))
}
fn identity(v: &Value) -> Result<(), CorrespondenceError> {
    text(v, "method")?;
    text(v, "value")?;
    Ok(())
}
/// The full tuple is retained as a JSON string, not hashed, shortened, or minted.
/// Its meaning comes from the resolved supplier record, not the string encoding.
fn source_identity(workflow: &Value) -> Result<String, CorrespondenceError> {
    for key in [
        "kind",
        "origin",
        "source_root",
        "name",
        "revision",
        "revision_method",
    ] {
        text(workflow, key)?;
    }
    serde_json::to_string(workflow).map_err(|e| invalid(e.to_string()))
}
fn equivalent_identity(a: &Value, b: &Value) -> bool {
    a.get("method").and_then(Value::as_str) == b.get("method").and_then(Value::as_str)
        && a.get("value").and_then(Value::as_str) == b.get("value").and_then(Value::as_str)
}

/// Reconstruct only a historical claim from WR records resolved by their owner.
/// Neither this value nor a successful schema check is accepted by an append API.
pub fn correspond(
    project: &ProjectRecords,
    run_text: &ResolvedRecord,
    check: &ResolvedRecord,
) -> Result<HistoricalSupply, CorrespondenceError> {
    if !run_text.same_project(check) {
        return Err(invalid("different owning projects"));
    }
    // Re-resolve in the explicit project, rather than trusting a pathname or an
    // earlier resolution after its owning basis disappears.
    let current = project
        .resolve(run_text.reference())
        .map_err(|e| invalid(format!("run_text resolution failed: {e:?}")))?;
    if !current.same_project(run_text) || current.body() != run_text.body() {
        return Err(invalid("run_text does not match current owning project"));
    }
    let original = if run_text.body()["purpose"] == "run end notice" {
        let refs = current.envelope()["basis_records"]
            .as_array()
            .ok_or_else(|| invalid("end-notice basis absent"))?;
        if refs.len() != 1 {
            return Err(invalid(
                "end notice requires exactly one original run-start reference",
            ));
        }
        let reference = refs[0]
            .as_str()
            .ok_or_else(|| invalid("end-notice basis is not a reference"))?;
        let start = project
            .resolve(reference)
            .map_err(|e| invalid(format!("original run-start resolution failed: {e:?}")))?;
        if !start.same_project(run_text) {
            return Err(invalid("original run start belongs to another project"));
        }
        Some(start)
    } else {
        None
    };
    correspond_bodies(
        run_text.reference(),
        run_text.body(),
        check.reference(),
        check.body(),
        check.envelope(),
        original.as_ref().map(ResolvedRecord::body),
    )
}
fn correspond_bodies(
    run_ref: &str,
    run_text: &Value,
    check_ref: &str,
    check: &Value,
    check_envelope: &Value,
    original_start: Option<&Value>,
) -> Result<HistoricalSupply, CorrespondenceError> {
    if text(run_text, "record_kind")? != "run_text" || text(check, "record_kind")? != "supply_check"
    {
        return Err(invalid("wrong WR kinds"));
    }
    if run_ref == check_ref {
        return Err(invalid("run_text and check share a reference"));
    }
    let basis = check_envelope
        .get("basis_records")
        .and_then(Value::as_array)
        .ok_or_else(|| invalid("check basis absent"))?;
    if !basis.iter().any(|v| v.as_str() == Some(run_ref)) {
        return Err(invalid("check does not cite this immutable run_text"));
    }
    for field in ["run", "conversation", "purpose"] {
        if text(run_text, field)? != text(check, field)? {
            return Err(invalid(format!("{field} disagrees")));
        }
    }
    let native_turn = check
        .get("turn")
        .and_then(Value::as_str)
        .filter(|s| !s.is_empty())
        .ok_or(CorrespondenceError::MissingNativeTurn)?;
    let form = match text(run_text, "purpose")? {
        "run start" => "workflow run start (turn text)",
        "run end notice" => "workflow run end notice (turn text)",
        _ => return Err(invalid("unknown text purpose")),
    };
    identity(&run_text["text_identity"])?;
    identity(&check["expected_text"])?;
    if !equivalent_identity(&run_text["text_identity"], &check["expected_text"]) {
        return Err(invalid("composed text method/value differs"));
    }
    if let Some(expected) = check.get("expected_workflow") {
        identity(expected)?;
        let source = &run_text["workflow_file"]["content"];
        identity(source)?;
        if !equivalent_identity(expected, source) {
            return Err(invalid("expected workflow method/value differs"));
        }
    }
    let state = text(check, "state")?;
    if ![
        "verified",
        "text differs, workflow bytes equal",
        "text differs, workflow bytes differ",
        "incomparable",
        "not found",
        "unreadable",
    ]
    .contains(&state)
    {
        return Err(invalid("unrecognized WR state"));
    }
    if [
        "verified",
        "text differs, workflow bytes equal",
        "text differs, workflow bytes differ",
        "incomparable",
    ]
    .contains(&state)
    {
        identity(&check["observed_text"])?;
        text(check, "item")?;
        text(check, "located_by")?;
        if state == "verified"
            && !equivalent_identity(&check["expected_text"], &check["observed_text"])
        {
            return Err(invalid("verified claim has unequal text method/value"));
        }
    }
    let mut limits: Vec<String> = check
        .get("evidence_limits")
        .and_then(Value::as_array)
        .ok_or_else(|| invalid("evidence limits absent"))?
        .iter()
        .map(|v| {
            v.as_str()
                .map(str::to_owned)
                .ok_or_else(|| invalid("non-text evidence limit"))
        })
        .collect::<Result<_, _>>()?;
    limits.push(HISTORICAL_LIMIT.into());
    let source = if run_text["purpose"] == "run end notice" {
        let start =
            original_start.ok_or_else(|| invalid("original run-start source unavailable"))?;
        if start["record_kind"] != "run_text"
            || start["purpose"] != "run start"
            || text(start, "run")? != text(run_text, "run")?
            || text(start, "conversation")? != text(run_text, "conversation")?
        {
            return Err(invalid("original run-start source scope disagrees"));
        }
        &start["workflow"]
    } else {
        &run_text["workflow"]
    };
    let body = json!({"supplyForm":form,"thread":run_text["conversation"],"nativeTurn":native_turn,"sourceIdentity":source_identity(source)?,"content":run_text["text_identity"],"supplyRecord":{"kind":"supply record","ref":run_ref,"resolutionAtWrite":"resolved"},"supplyCheck":state,"supplyCheckRecord":{"kind":"supply record","ref":check_ref,"resolutionAtWrite":"resolved"},"adoption":"unknown"});
    Ok(HistoricalSupply {
        run: text(run_text, "run")?.into(),
        body,
        limits,
    })
}

#[derive(Debug, PartialEq, Eq)]
pub enum ReadStanding {
    HistoricalCorrespondence,
    LegacyOrdinalRetained,
    Limited,
}
#[derive(Debug)]
pub struct SupplyReading {
    pub standing: ReadStanding,
    pub limits: Vec<String>,
}
impl SupplyReading {
    fn limited(reason: impl Into<String>) -> Self {
        Self {
            standing: ReadStanding::Limited,
            limits: vec![reason.into(), HISTORICAL_LIMIT.into()],
        }
    }
}
/// Re-resolve in the explicitly opened project. Recorded resolutionAtWrite is
/// history, not proof that a supplier reference resolves today.
pub fn read_correspondence(project: &ProjectRecords, entry: &Value) -> SupplyReading {
    if let Err(e) = crate::schema_validation::bundled().and_then(|v| v.validate(entry)) {
        return SupplyReading::limited(format!("invalid RS entry: {e}"));
    }
    if entry["kind"] != "supplied_guidance" {
        return SupplyReading::limited("not supplied_guidance");
    }
    let body = &entry["body"];
    if ![
        "workflow run start (turn text)",
        "workflow run end notice (turn text)",
    ]
    .contains(&body["supplyForm"].as_str().unwrap_or(""))
    {
        return SupplyReading::limited("not a workflow supply form");
    }
    if body.get("nativeTurn").is_none() {
        return SupplyReading {
            standing: ReadStanding::LegacyOrdinalRetained,
            limits: vec![
                "legacy coordinate preserved; no native turn correspondence established".into(),
                HISTORICAL_LIMIT.into(),
            ],
        };
    }
    let run_ref = match body["supplyRecord"]["ref"].as_str() {
        Some(v) => v,
        None => return SupplyReading::limited("run_text reference absent"),
    };
    let check_ref = match body["supplyCheckRecord"]["ref"].as_str() {
        Some(v) => v,
        None => return SupplyReading::limited("check reference absent"),
    };
    let run_text = match project.resolve(run_ref) {
        Ok(v) => v,
        Err(e) => return SupplyReading::limited(format!("run_text resolution failed: {e:?}")),
    };
    let check = match project.resolve(check_ref) {
        Ok(v) => v,
        Err(e) => return SupplyReading::limited(format!("check resolution failed: {e:?}")),
    };
    let resolved = match correspond(project, &run_text, &check) {
        Ok(v) => v,
        Err(e) => return SupplyReading::limited(e.to_string()),
    };
    if entry["runId"].as_str() != Some(resolved.run()) {
        return SupplyReading::limited("RS runId disagrees with WR");
    }
    // Do not rewrite historical resolutionAtWrite, but compare the remaining
    // semantic fields to the owning records that actually resolve now.
    for key in [
        "supplyForm",
        "thread",
        "nativeTurn",
        "sourceIdentity",
        "content",
        "supplyCheck",
        "adoption",
    ] {
        if body.get(key) != resolved.body.get(key) {
            return SupplyReading::limited(format!("RS {key} disagrees with WR"));
        }
    }
    SupplyReading {
        standing: ReadStanding::HistoricalCorrespondence,
        limits: resolved.limits,
    }
}

#[cfg(test)]
#[path = "record_supply_tests.rs"]
mod tests;
