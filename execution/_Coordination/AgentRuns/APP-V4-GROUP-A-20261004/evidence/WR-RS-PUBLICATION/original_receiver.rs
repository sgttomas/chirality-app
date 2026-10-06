//! CC-RS-WR-SUPPLY-FIT: historical WR/RS correspondence, never live supply authority.
//!
//! Resolved immutable evidence can reconstruct a claim, but cannot recreate the
//! source-owned comparison or authorize a new supplied_guidance append. Root's
//! completed-check producer must supply that separate capability at integration.
use crate::workflow_workspace::publication::{ProjectRecords, ResolvedRecord};
use serde_json::{json, Value};

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
    run_text: &ResolvedRecord,
    check: &ResolvedRecord,
) -> Result<HistoricalSupply, CorrespondenceError> {
    if !run_text.same_project(check) {
        return Err(invalid("different owning projects"));
    }
    correspond_bodies(
        run_text.reference(),
        run_text.body(),
        check.reference(),
        check.body(),
        check.envelope(),
    )
}
fn correspond_bodies(
    run_ref: &str,
    run_text: &Value,
    check_ref: &str,
    check: &Value,
    check_envelope: &Value,
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
    let body = json!({"supplyForm":form,"thread":run_text["conversation"],"nativeTurn":native_turn,"sourceIdentity":source_identity(&run_text["workflow"] )?,"content":run_text["text_identity"],"supplyRecord":{"kind":"supply record","ref":run_ref,"resolutionAtWrite":"resolved"},"supplyCheck":state,"supplyCheckRecord":{"kind":"supply record","ref":check_ref,"resolutionAtWrite":"resolved"},"adoption":"unknown"});
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
    let resolved = match correspond(&run_text, &check) {
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
