//! Advisory compatibility evaluation (EXEC §3, CK-1…CK-3). The in-memory
//! preparation is always produced; the schema-valid EXEC report body and its RS
//! R14 body are produced only from supplied facts. Storage and the RS write stay
//! with the caller; nothing here gates a start or touches Codex configuration.
use super::*;
use crate::role_lifecycle::RoleInForce;
use crate::workflow_workspace::Selection;

#[derive(Clone, Debug, Serialize, PartialEq, Eq)]
pub enum Occasion {
    /// CK-1: a workflow is selected or offered for a run.
    Selection,
    /// CK-2: immediately before the run's first action.
    BeforeFirstAction,
    /// CK-3: the host published a new edition while a report is shown or a run
    /// is live. The earlier report stays as it is; its view becomes not current.
    EditionChange {
        earlier_report: String,
        earlier_edition: String,
    },
}
#[derive(Clone, Debug, Serialize, PartialEq, Eq)]
pub struct Basis {
    pub home: String,
    pub generation: Value,
    pub conversation: String,
    pub acting_pin: String,
    pub surface: String,
    pub environment_observation: Option<String>,
    pub catalog_edition: Option<String>,
}
/// Supplied only by the owning environment collector, not deserialized from the UI.
/// Partial means listed entries may be evaluated, but omission proves nothing.
pub enum CatalogCoverage {
    Unobserved,
    /// The collector attempted the read and the catalog was unreadable (RF-1).
    /// Distinct from Unobserved: only this one may publish `catalog_readable: false`.
    Unreadable,
    Partial(BTreeMap<String, Operation>),
    Complete(BTreeMap<String, Operation>),
}
pub struct Observations {
    pub catalog: CatalogCoverage,
    pub channel_enabled: Option<bool>,
    pub harness_signals: Option<Value>,
}
impl Default for Observations {
    fn default() -> Self {
        Self {
            catalog: CatalogCoverage::Unobserved,
            channel_enabled: None,
            harness_signals: None,
        }
    }
}
#[derive(Clone, Debug, Serialize)]
pub struct RequirementDisplay {
    pub name: String,
    pub purpose: Value,
    pub fallback: Value,
    pub outcome: Outcome,
    pub reason: String,
}
#[derive(Clone, Debug, Serialize)]
pub struct PreparedReport {
    id: String,
    basis: Basis,
    occasion: Occasion,
    evaluated_at: String,
    workflow: Value,
    declaration: Declaration,
    role: RoleInForce,
    check: Compatibility,
    requirements: Vec<RequirementDisplay>,
}
fn is_blocking(outcome: &Outcome) -> bool {
    matches!(
        outcome,
        Outcome::Missing
            | Outcome::VersionMismatch
            | Outcome::NotExposedOnThisSurface
            | Outcome::ChannelNotEnabled
    )
}
fn report_check(
    declaration: &Declaration,
    basis: &Basis,
    observations: &Observations,
    role: &RoleInForce,
) -> Compatibility {
    let catalog = match &observations.catalog {
        CatalogCoverage::Unobserved | CatalogCoverage::Unreadable => None,
        CatalogCoverage::Partial(v) | CatalogCoverage::Complete(v) => Some(v.clone()),
    };
    let environment = Environment {
        catalog,
        channel_enabled: observations.channel_enabled.unwrap_or(true),
        harness_signals: observations.harness_signals.clone(),
        harness_pin: Some(basis.acting_pin.clone()),
    };
    let mut result = Compatibility::check(declaration, &environment);
    for (entry, row) in declaration
        .elements
        .get("required_tools")
        .into_iter()
        .flatten()
        .zip(result.tools.iter_mut())
    {
        if entry.value["class"] != "host_operation" {
            continue;
        }
        if matches!(observations.catalog, CatalogCoverage::Partial(_))
            && row.outcome == Outcome::Missing
        {
            row.outcome = Outcome::NotEstablished;
            row.reason =
                "operation absent from partial observation; absence not established".into();
        }
        if observations.channel_enabled.is_none()
            && matches!(
                row.outcome,
                Outcome::Present | Outcome::PresentCurrentlyUnavailable
            )
        {
            row.outcome = Outcome::NotEstablished;
            row.reason = "acting channel state not observed".into();
        }
    }
    let blocked = result
        .tools
        .iter()
        .any(|r| r.necessity == "required" && is_blocking(&r.outcome));
    let unknown = declaration.reading != Reading::Recognized
        || !matches!(
            declaration.categories.get("required_tools"),
            Some(Reading::Recognized | Reading::DeclaredEmpty)
        )
        // WD §3.4: an unrecognized element in the required-tool category makes
        // the required-tool result not established, never a pass, whatever its
        // stated necessity.
        || declaration
            .elements
            .get("required_tools")
            .into_iter()
            .flatten()
            .any(|e| e.reading != Reading::Recognized)
        || result.tools.iter().any(|r| {
            !matches!(r.necessity.as_str(), "required" | "optional")
                || (r.necessity == "required" && r.outcome == Outcome::NotEstablished)
        });
    result.result = if blocked {
        Check::Unsupported
    } else if unknown {
        Check::NotEstablished
    } else {
        Check::Compatible
    };
    match role {
        RoleInForce::AppObserved { role, .. } => {
            // Reuse role semantics without letting the legacy environment evaluation
            // replace the explicitly partial/unknown inventory result above.
            let mut role_only = declaration.clone();
            role_only.elements.remove("required_tools");
            role_only
                .categories
                .insert("required_tools".into(), Reading::DeclaredEmpty);
            // Preserve delegation requirement for the known TASK special case.
            if role.as_ref().is_some_and(|r| r.name() == "TASK") {
                role_only.elements.insert(
                    "required_tools".into(),
                    declaration
                        .elements
                        .get("required_tools")
                        .into_iter()
                        .flatten()
                        .filter(|e| e.value["capability"] == "agent-delegation")
                        .cloned()
                        .collect(),
                );
            }
            let checked = Compatibility::check_for_role(
                &role_only,
                &Environment::default(),
                role.as_ref().map(|r| r.name()),
            );
            if checked.result == Check::Unsupported {
                result.result = Check::Unsupported;
            } else if checked.result == Check::NotEstablished && result.result != Check::Unsupported
            {
                result.result = Check::NotEstablished;
            }
            result.findings.extend(checked.findings);
        }
        RoleInForce::Unknown { reason } => {
            let constrained = declaration
                .raw
                .as_ref()
                .and_then(|v| v.get("compatible_roles"))
                .is_some()
                || declaration
                    .elements
                    .get("required_tools")
                    .into_iter()
                    .flatten()
                    .any(|e| {
                        e.value["capability"] == "agent-delegation"
                            && e.value["necessity"] == "required"
                    });
            if constrained && result.result != Check::Unsupported {
                result.result = Check::NotEstablished;
            }
            result.findings.push(format!(
                "original role not established: {reason}; not a deliberate no-role selection"
            ));
        }
    }
    result
}
impl PreparedReport {
    pub fn prepare(
        selection: &Selection,
        basis: Basis,
        occasion: Occasion,
        evaluated_at: String,
        observations: &Observations,
        role: RoleInForce,
    ) -> Result<Self, String> {
        if basis.home.is_empty()
            || basis.conversation.is_empty()
            || basis.acting_pin.is_empty()
            || basis.surface.is_empty()
            || evaluated_at.is_empty()
        {
            return Err("report basis/occasion time absent".into());
        }
        let declaration = selection.snapshot().declaration()?;
        let check = report_check(&declaration, &basis, observations, &role);
        let requirements = declaration
            .elements
            .get("required_tools")
            .into_iter()
            .flatten()
            .zip(&check.tools)
            .map(|(e, r)| RequirementDisplay {
                name: r.name.clone(),
                purpose: e.value["purpose"].clone(),
                fallback: e.value["fallback"].clone(),
                outcome: r.outcome.clone(),
                reason: r.reason.clone(),
            })
            .collect();
        Ok(Self {
            id: crate::util::opaque_id("compatibility-preparation:")?,
            basis,
            occasion,
            evaluated_at,
            workflow: serde_json::to_value(selection.identity()).map_err(|e| e.to_string())?,
            declaration,
            role,
            check,
            requirements,
        })
    }
    pub fn result(&self) -> &Check {
        &self.check.result
    }
    /// Currency is a view; the original report and its basis remain immutable.
    pub fn view(&self, current_basis: &Basis) -> Value {
        let statement = match self.check.result {
            Check::Compatible => format!(
                "requirement check passes against {} on {} at {}",
                self.basis.catalog_edition.as_deref().unwrap_or(
                    "catalog not observed; no catalog-dependent requirement established"
                ),
                self.basis.surface,
                self.evaluated_at
            ),
            Check::Unsupported => {
                "requirement check does not pass; the person may still start".into()
            }
            Check::NotEstablished => {
                "requirement check not established; the person may still start".into()
            }
        };
        serde_json::json!({"preparation":self,"occasion":occasion_label(&self.occasion),"notCurrent":&self.basis!=current_basis,"statement":statement,"recording":"not published; no EXEC report or RS R14 receipt","advisory":true,"adoption":"unknown"})
    }
}

fn occasion_label(occasion: &Occasion) -> &'static str {
    match occasion {
        Occasion::Selection => "CK-1",
        Occasion::BeforeFirstAction => "CK-2",
        Occasion::EditionChange { .. } => "CK-3",
    }
}
fn occasion_record_label(occasion: &Occasion) -> &'static str {
    match occasion {
        Occasion::Selection => "CK-1 selection",
        Occasion::BeforeFirstAction => "CK-2 run start",
        Occasion::EditionChange { .. } => "CK-3 edition change",
    }
}

/// Where the environment facts came from. No authentic environment collector
/// exists yet, so every current origin is an explicit input and none can yield
/// the `actual_host` evidence standing (CR-13). An actual collector is a later,
/// separately reviewed origin; it is not inferred from caller fields.
#[derive(Clone, Debug, Serialize, PartialEq, Eq)]
#[serde(tag = "kind", rename_all = "kebab-case")]
pub enum InventoryOrigin {
    /// Facts the caller supplies explicitly, naming their source. Standing `illustrative`.
    CallerSupplied { source: String },
    /// Facts from a named test double. Standing `test_double`.
    TestDouble { fixture: String },
}
/// The environment inventory with its origin. `observations` keeps unknowns
/// unknown: an unobserved catalog, channel or signal is never read as absent.
pub struct Inventory {
    pub origin: InventoryOrigin,
    pub host_id: Option<String>,
    pub observations: Observations,
}
#[derive(Clone, Debug, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum DestinationClass {
    Local,
    Cloud,
    Unknown,
}
/// CR-14: the model destination selected at report time; information only,
/// never an outcome, gate or pass condition.
#[derive(Clone, Debug, Serialize, PartialEq, Eq)]
pub struct ModelDestination {
    pub selected: String,
    pub class: DestinationClass,
}

/// # Root seam (J2 → J1)
///
/// One call per occasion: [`evaluate`]. Root passes, all from the same home,
/// full generation and conversation:
///
/// - `selection`: the exact current `workflow_workspace::Selection` held for
///   the conversation (`WorkflowRootSession`'s selected state or the run's
///   selection). Its snapshot's declaration is what is checked.
/// - `holding_library`: the holding library of that selection (the run scope's
///   `holding_library`, or the opened library's label). `None` refuses publication.
/// - `role`: the conversation's fixed role in force, typed: the same value as
///   `RoleBindings::selected_role(home, thread)`, i.e. `HistorySession::binding(home,
///   thread).map(|b| b.role_in_force(home, thread))`, else `RoleInForce::Unknown`
///   ("original App supply binding not established"). A fork uses its owning
///   binding. Never a new-chat selector value; a missing binding stays `Unknown`
///   and is never turned into no-role.
/// - `basis`: home, full `{appSession, home, spawnCounter}` generation, thread,
///   acting pin (`"App Codex 0.160.0"` for the current supplier), surface
///   (`"X"` for App runs), the identity of the environment observation the
///   inventory came from, and the catalog edition when one is known.
/// - `occasion`: CK-1 on selection, CK-2 immediately before the run's first
///   action (a new evaluation, never a reused CK-1), CK-3 when a new edition is
///   observed, naming the earlier report and its edition.
/// - `evaluated_at`: the evaluation time Root observes.
/// - `inventory`: host identity, catalog coverage, channel state and harness
///   signals, with their origin. Pass `Unobserved`/`None` for anything not
///   actually read; never a guessed edition, enabled channel or tool.
/// - `model_destination`: the destination selected at report time, if known.
///
/// Result and use:
///
/// - `Err` only when no evaluation can be made (absent basis, unreadable
///   selection, or a CK-3 without a new edition). It never refuses a start.
/// - `Evaluation::view(current_basis)` is the display value for the workflow
///   panel: qualified statement, rows with purpose/fallback/reason, occasion,
///   currency, inventory origin and publication state. Keep each evaluation
///   keyed to its selection and occasion; a changed basis marks it not current.
/// - `Evaluation::published` is a schema-valid EXEC report body, or the list of
///   facts that were not supplied. Root stores the body where it keeps run
///   evidence; then, when an RS run log exists, `PublishedReport::r14_body`
///   with the stored bytes read back gives the R14 `compatibility_report_ref`
///   body for the RS writer (`resolutionAtWrite` is `resolved` only when those
///   bytes are this report).
/// - The report is advisory. The person may start whatever it says (CC-3,
///   SL-7). Nothing here reads, edits or vetoes the user's Codex configuration.
pub struct Request<'a> {
    pub selection: &'a Selection,
    pub holding_library: Option<String>,
    pub role: RoleInForce,
    pub basis: Basis,
    pub occasion: Occasion,
    pub evaluated_at: String,
    pub inventory: Inventory,
    pub model_destination: Option<ModelDestination>,
}

/// A schema-valid EXEC report body (`exec-compatibility-report/proposed-0.6`),
/// held in memory. It is not a stored record until Root stores it.
#[derive(Clone, Debug)]
pub struct PublishedReport {
    report_id: String,
    occasion: &'static str,
    pass_result: &'static str,
    body: Value,
}
impl PublishedReport {
    pub fn id(&self) -> &str {
        &self.report_id
    }
    pub fn body(&self) -> &Value {
        &self.body
    }
    /// RS R14 `compatibility_report_ref` body for the RS writer. `stored` is the
    /// report's bytes as read back from where Root stored them: equal content
    /// gives `resolved`; `None` gives `not supplied`; other bytes are refused.
    /// A preparation never has an R14 body.
    pub fn r14_body(&self, stored: Option<&[u8]>) -> Result<Value, String> {
        let resolution = match stored {
            None => "not supplied",
            Some(bytes) => {
                let read: Value = serde_json::from_slice(bytes)
                    .map_err(|e| format!("stored report unreadable: {e}"))?;
                if read != self.body {
                    return Err(
                        "stored bytes are not this report; no resolved reference written".into(),
                    );
                }
                "resolved"
            }
        };
        let body = serde_json::json!({"report":{"kind":"compatibility report","ref":self.report_id,"resolutionAtWrite":resolution},"occasion":self.occasion,"passResult":self.pass_result});
        r14_validator()?
            .validate(&body)
            .map_err(|e| format!("R14 body validation refused: {e}"))?;
        Ok(body)
    }
}

/// One evaluation: the advisory preparation always, and the EXEC report body
/// only when every fact it requires was supplied.
pub struct Evaluation {
    pub prepared: PreparedReport,
    pub inventory_origin: InventoryOrigin,
    pub published: Result<PublishedReport, Vec<String>>,
}
impl Evaluation {
    pub fn view(&self, current_basis: &Basis) -> Value {
        let mut view = self.prepared.view(current_basis);
        view["inventoryOrigin"] = serde_json::json!(self.inventory_origin);
        match &self.published {
            Ok(report) => {
                view["publication"] = serde_json::json!({"state":"published in memory","reportId":report.report_id,"checkResult":report.body["check_result"],"report":report.body,"stored":"by the caller only"});
                view["recording"] = "EXEC report body published in memory; not stored here; R14 written only by the RS writer".into();
            }
            Err(missing) => {
                view["publication"] =
                    serde_json::json!({"state":"not published","factsNotSupplied":missing});
            }
        }
        view
    }
}

pub(crate) const REPORT_SCHEMA: &str =
    include_str!("../resources/workflow_role/compatibility-report.schema.json");
pub(crate) const REPORT_SCHEMA_ID: &str =
    "chirality:del-02-03/exec-compatibility-report/proposed-0.6";
const R14_TARGET: &str =
    "urn:chirality:app-v4:del-04-03:rs-record:0.1#/$defs/compatibilityReportRef";

fn report_validator() -> Result<&'static jsonschema::Validator, String> {
    static VALIDATOR: std::sync::OnceLock<Result<jsonschema::Validator, String>> =
        std::sync::OnceLock::new();
    VALIDATOR
        .get_or_init(|| {
            crate::schema_validation::compile_targets(
                &[("compatibility-report.schema.json", REPORT_SCHEMA)],
                &[REPORT_SCHEMA_ID],
                &[REPORT_SCHEMA_ID],
            )
            .map(|mut v| v.remove(0))
        })
        .as_ref()
        .map_err(Clone::clone)
}
fn r14_validator() -> Result<&'static jsonschema::Validator, String> {
    static VALIDATOR: std::sync::OnceLock<Result<jsonschema::Validator, String>> =
        std::sync::OnceLock::new();
    VALIDATOR
        .get_or_init(|| {
            crate::schema_validation::compile_targets(
                crate::schema_validation::RESOURCES,
                &[crate::schema_validation::RS_ID],
                &[R14_TARGET],
            )
            .map(|mut v| v.remove(0))
        })
        .as_ref()
        .map_err(Clone::clone)
}
/// Fail closed: a body the Design schema refuses is never published.
pub(crate) fn validate_report(body: &Value) -> Result<(), String> {
    report_validator()?
        .validate(body)
        .map_err(|e| format!("EXEC report validation refused: {e}"))
}

fn nonempty(value: Option<&str>) -> Option<&str> {
    value.filter(|s| !s.trim().is_empty())
}
/// CR-2 identity tuple; the report's identity has no slot for the revision method.
fn report_identity(identity: &Value) -> Option<Value> {
    let mut out = serde_json::Map::new();
    for key in ["kind", "origin", "source_root", "name", "revision"] {
        out.insert(key.into(), nonempty(identity[key].as_str())?.into());
    }
    if let Some(from) = identity.get("derived_from").filter(|v| !v.is_null()) {
        out.insert("derived_from".into(), report_identity(from)?);
    }
    Some(Value::Object(out))
}
fn declared_part_status(declaration: &Declaration) -> &'static str {
    match declaration.reading {
        Reading::Undeclared => "undeclared",
        Reading::Recognized => match declaration.categories.get("required_tools") {
            Some(Reading::DeclaredEmpty) => "declared_empty",
            Some(Reading::Recognized)
                if declaration
                    .elements
                    .get("required_tools")
                    .into_iter()
                    .flatten()
                    .all(|e| e.reading == Reading::Recognized) =>
            {
                "declared"
            }
            Some(Reading::Undeclared) | None => "undeclared",
            _ => "not_established",
        },
        _ => "not_established",
    }
}
const ROLE_NAMES: [&str; 4] = ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"];
/// CR-8 current-phase reasons, read as `Compatibility::check_for_role` reads them.
fn role_reasons(declaration: &Declaration, role: &RoleInForce) -> Vec<&'static str> {
    let RoleInForce::AppObserved { role, .. } = role else {
        return vec![];
    };
    let name = role.map(|r| r.name());
    let mut reasons = vec![];
    if let Some(list) = declaration
        .raw
        .as_ref()
        .and_then(|v| v.get("compatible_roles"))
        .and_then(Value::as_array)
    {
        let established = !list.is_empty()
            && list
                .iter()
                .all(|v| v.as_str().is_some_and(|s| ROLE_NAMES.contains(&s)));
        if established && !list.iter().any(|v| v.as_str() == name) {
            reasons.push("role");
        }
    }
    if name == Some("TASK")
        && declaration
            .elements
            .get("required_tools")
            .into_iter()
            .flatten()
            .any(|e| {
                e.reading == Reading::Recognized
                    && e.value["capability"] == "agent-delegation"
                    && e.value["necessity"] == "required"
            })
    {
        reasons.push("delegation");
    }
    reasons
}
fn requirement_row(
    element: &crate::workflow_declaration::Element,
    row: &ToolResult,
    catalog: Option<&BTreeMap<String, Operation>>,
    observation: &str,
) -> Result<Value, String> {
    let v = &element.value;
    let reference = nonempty(v["name"].as_str()).ok_or("reference name not established")?;
    let class = v["class"]
        .as_str()
        .filter(|c| matches!(*c, "host_operation" | "harness_capability"))
        .ok_or("class not established")?;
    let necessity = v["necessity"]
        .as_str()
        .filter(|n| matches!(*n, "required" | "optional"))
        .ok_or("necessity not established")?;
    let mut purpose = v["purpose"].as_str().unwrap_or("").to_owned();
    if let Some(fallback) = nonempty(v["fallback"].as_str()) {
        purpose = format!("{purpose} (fallback: {fallback})")
            .trim()
            .to_owned();
    }
    let declared_versions: Vec<String> = match v.get("versions") {
        None => vec![],
        Some(Value::Array(versions)) => versions
            .iter()
            .map(|x| nonempty(x.as_str()).map(String::from))
            .collect::<Option<_>>()
            .ok_or("declared version not established")?,
        Some(_) => return Err("declared versions not established".into()),
    };
    let found = (class == "host_operation")
        .then(|| v["operation"].as_str())
        .flatten()
        .and_then(|operation| catalog?.get(operation).map(|op| (operation, op)));
    let entry = match found {
        None => Value::Null,
        Some((operation, op)) => {
            nonempty(Some(&op.version)).ok_or("catalog entry version not established")?;
            serde_json::json!({"operation_id":operation,"version":op.version})
        }
    };
    let exposure = match found {
        None => "not_read",
        Some((_, op)) => match op.exposure {
            Some(true) => "exposed",
            Some(false) => "not_exposed_on_this_surface",
            None => "unagreed",
        },
    };
    // Availability is reported only where it was evaluated (EV-10).
    let availability = match (found, &row.outcome) {
        (Some((_, op)), Outcome::Present | Outcome::PresentCurrentlyUnavailable) => {
            match op.availability {
                Some(true) => {
                    serde_json::json!({"result":"available","reason":"evaluated runtime precondition available","evaluated_basis":observation})
                }
                Some(false) => {
                    serde_json::json!({"result":"unavailable","reason":row.reason,"evaluated_basis":observation})
                }
                None => Value::Null,
            }
        }
        _ => Value::Null,
    };
    Ok(serde_json::json!({
        "reference": reference,
        "class": class,
        "necessity": necessity,
        "purpose": purpose,
        "declared_versions": declared_versions,
        "entry": entry,
        "exposure": exposure,
        "availability": availability,
        "outcome": row.outcome,
        "reason": row.reason,
    }))
}
/// CR-9 Phase 1: listed as plan guidance, with no hold-support value (PH-3).
fn checkpoint_row(element: &crate::workflow_declaration::Element) -> Result<Value, String> {
    let v = &element.value;
    let name = nonempty(v["name"].as_str()).ok_or("checkpoint name not established")?;
    let act = v["required_act"]
        .as_str()
        .filter(|a| ["A4", "A5", "A6", "A7", "A12"].contains(a))
        .ok_or("required act not established")?;
    let kind = match v["reached_when"]["kind"].as_str() {
        Some("before_dispatch") => "a",
        Some("output_produced") => "b",
        Some("host_outcome") => "c",
        _ => return Err("reached-when kind not established".into()),
    };
    let subject = match v["subject"]["class"].as_str() {
        Some("change_items_of_named_proposal") => "change items of a named proposal",
        Some("named_output") => "named output",
        Some("objects_named_output_concerns") => "objects a named output concerns",
        Some("objects_changed_by_named_outcome") => "objects changed by a named outcome",
        Some("targets_of_held_call") => "targets of the held call",
        Some("grant_setting") => "grant setting",
        _ => return Err("subject class not established".into()),
    };
    // EXEC HS-5 / R7-3: A5 and kind (a) without the element have derived held actions.
    let held = match v.get("held_actions") {
        None if act == "A5" || kind == "a" => "absent_derived",
        None => "absent_default",
        Some(h) => match h["form"].as_str() {
            Some("host_operations_only") => "host_operations_only",
            Some("listed_steps") => "listed_steps",
            _ => return Err("held-actions form not established".into()),
        },
    };
    let status = match element.reading {
        Reading::Recognized => "valid",
        Reading::Invalid => "invalid",
        _ => "not_established",
    };
    Ok(serde_json::json!({
        "name": name,
        "required_act": act,
        "reached_when_kind": kind,
        "subject_class": subject,
        "held_actions": held,
        "governed": v["governed"] == "yes",
        "declaration_status": status,
        "phase_reading": "guidance",
    }))
}
fn publish(
    prepared: &PreparedReport,
    inventory: &Inventory,
    holding_library: Option<&str>,
    model_destination: Option<&ModelDestination>,
) -> Result<PublishedReport, Vec<String>> {
    let basis = &prepared.basis;
    let declaration = &prepared.declaration;
    let check = &prepared.check;
    let observations = &inventory.observations;
    let mut missing = vec![];
    let host_id = nonempty(inventory.host_id.as_deref());
    if host_id.is_none() {
        missing.push("host identity not supplied (CR-4)".to_string());
    }
    let edition = nonempty(basis.catalog_edition.as_deref());
    if edition.is_none() {
        missing.push("catalog edition not supplied (CR-4); never guessed".into());
    }
    let (readable, catalog) = match &observations.catalog {
        CatalogCoverage::Unobserved => {
            missing.push(
                "catalog not observed: readability not supplied (CR-4); unknown is not unreadable"
                    .into(),
            );
            (None, None)
        }
        CatalogCoverage::Unreadable => (Some(false), None),
        CatalogCoverage::Partial(c) | CatalogCoverage::Complete(c) => (Some(true), Some(c)),
    };
    let channel = match observations.channel_enabled {
        Some(true) => Some("enabled"),
        Some(false) => Some("not_enabled"),
        None => {
            missing
                .push("acting channel state not observed (CR-5); never reported as enabled".into());
            None
        }
    };
    if !["H", "E", "X"].contains(&basis.surface.as_str()) {
        missing.push(format!(
            "acting surface {:?} is not one of H, E, X (CR-5)",
            basis.surface
        ));
    }
    let holding = nonempty(holding_library);
    if holding.is_none() {
        missing.push("holding library not supplied (CR-2)".into());
    }
    let observation = nonempty(basis.environment_observation.as_deref());
    if observation.is_none() {
        missing
            .push("environment observation identity not supplied; evaluated basis unknown".into());
    }
    let identity = report_identity(&prepared.workflow);
    if identity.is_none() {
        missing.push("workflow identity tuple not representable (CR-2)".into());
    }
    let elements: Vec<_> = declaration
        .elements
        .get("required_tools")
        .into_iter()
        .flatten()
        .collect();
    let mut requirements = vec![];
    if elements.len() != check.tools.len() {
        missing.push("requirement rows do not correspond to declared elements".into());
    } else {
        for (i, (element, row)) in elements.iter().zip(&check.tools).enumerate() {
            match requirement_row(element, row, catalog, observation.unwrap_or("")) {
                Ok(r) => requirements.push(r),
                Err(e) => missing.push(format!(
                    "required-tool element {i} not representable in the report: {e}"
                )),
            }
        }
    }
    let mut checkpoints = vec![];
    for (i, element) in declaration
        .elements
        .get("checkpoints")
        .into_iter()
        .flatten()
        .enumerate()
    {
        match checkpoint_row(element) {
            Ok(r) => checkpoints.push(r),
            Err(e) => missing.push(format!(
                "checkpoint element {i} not representable in the report: {e}"
            )),
        }
    }
    let report_id = match crate::util::opaque_id("compatibility-report:") {
        Ok(id) => Some(id),
        Err(e) => {
            missing.push(format!("report identity not allocated: {e}"));
            None
        }
    };
    let (
        Some(host_id),
        Some(edition),
        Some(readable),
        Some(channel),
        Some(holding),
        Some(observation),
        Some(identity),
        Some(report_id),
        true,
    ) = (
        host_id,
        edition,
        readable,
        channel,
        holding,
        observation,
        identity,
        report_id,
        missing.is_empty(),
    )
    else {
        return Err(missing);
    };

    let (check_result, pass_result) = match check.result {
        Check::Compatible => ("passes", "pass"),
        Check::Unsupported => ("does_not_pass", "does not pass"),
        Check::NotEstablished => ("not_established", "not established"),
    };
    let standing = match &inventory.origin {
        InventoryOrigin::CallerSupplied { .. } => "illustrative",
        InventoryOrigin::TestDouble { .. } => "test_double",
    };
    let mut limitations = vec![match &inventory.origin {
        InventoryOrigin::CallerSupplied { source } => format!(
            "environment facts supplied explicitly by {source}; not read by an environment collector"
        ),
        InventoryOrigin::TestDouble { fixture } => {
            format!("evaluated on a test double ({fixture})")
        }
    }];
    limitations.push(format!(
        "evaluated basis: environment observation {observation} on acting pin {}",
        basis.acting_pin
    ));
    limitations.push("version compatibility: equality only".into());
    match &observations.catalog {
        CatalogCoverage::Partial(_) => limitations.push(
            "catalog observation partial: an operation absent from it is not established, never missing"
                .into(),
        ),
        CatalogCoverage::Unreadable => limitations.push(
            "catalog unreadable (RF-1): host-operation references not established".into(),
        ),
        _ => {}
    }
    if elements
        .iter()
        .any(|e| e.value["class"] == "harness_capability")
    {
        if basis.acting_pin != "App Codex 0.158.0" {
            limitations.push(format!(
                "no adopted supplier availability account at acting pin {}; the 0.158.0 account is not borrowed, so harness capabilities are not established",
                basis.acting_pin
            ));
        } else if observations.harness_signals.is_none() {
            limitations.push("harness availability signals not read".into());
        }
    }
    limitations.push(match &prepared.role {
        RoleInForce::AppObserved { role: Some(r), .. } => {
            format!("role in force: {} (fixed for the conversation)", r.name())
        }
        RoleInForce::AppObserved { role: None, .. } => {
            "no role in force (deliberate selection, fixed for the conversation)".into()
        }
        RoleInForce::Unknown { reason } => {
            format!("role in force not established: {reason}; not a deliberate no-role selection")
        }
    });
    if let Some(method) = nonempty(prepared.workflow["revision_method"].as_str()) {
        limitations.push(format!(
            "workflow revision method {method} is not carried by the report identity"
        ));
    }
    match declaration.reading {
        Reading::Recognized => {}
        Reading::Undeclared => {
            limitations.push("requirements undeclared — check not established".into())
        }
        _ => limitations.push("declared part not established — check not established".into()),
    }
    match declaration.categories.get("checkpoints") {
        Some(Reading::Undeclared) => limitations.push("checkpoints undeclared; none listed".into()),
        Some(Reading::NotEstablished) => {
            limitations.push("checkpoint category not established; none listed".into())
        }
        _ => {}
    }
    if model_destination.is_none() {
        limitations.push("model destination not supplied".into());
    }
    limitations.extend(
        check
            .findings
            .iter()
            .filter(|f| !f.trim().is_empty())
            .map(|f| format!("finding: {f}")),
    );
    limitations.push(
        "advisory: the check informs and never gates starting the run; the person may still start (CC-3)"
            .into(),
    );
    let unsupported: Vec<Value> = role_reasons(declaration, &prepared.role)
        .into_iter()
        .map(|kind| serde_json::json!({"reason_kind":kind,"checkpoints":[]}))
        .collect();
    let runtime_holds: Vec<Value> = requirements
        .iter()
        .filter(|r| r["outcome"] == "present_currently_unavailable")
        .map(|r| serde_json::json!({"reference":r["reference"],"reason":r["reason"],"evaluated_basis":observation}))
        .collect();
    // A report is never relabelled; currency is a view (CC-1), so no not_current here.
    let occasion = serde_json::json!({"occasion":occasion_label(&prepared.occasion),"evaluated_at":prepared.evaluated_at});
    let body = serde_json::json!({
        "format": "exec-compatibility-report/proposed-0.6",
        "phase": "current",
        "report_id": report_id,
        "workflow": {"identity": identity, "holding_library": holding},
        "declared_part_status": declared_part_status(declaration),
        "host": {"host_id": host_id, "catalog_edition": edition, "catalog_readable": readable},
        "surface": {"surface": basis.surface, "channel_state": channel},
        "occasion": occasion,
        "requirements": requirements,
        "workflow_unsupported": unsupported,
        "checkpoints": checkpoints,
        "check_result": check_result,
        "runtime_holds": runtime_holds,
        "limitations": limitations,
        "evidence_standing": standing,
        "model_destination": model_destination.map(|d| serde_json::json!({"selected":d.selected,"class":d.class,"information_only":true})),
    });
    validate_report(&body).map_err(|e| vec![e])?;
    Ok(PublishedReport {
        report_id,
        occasion: occasion_record_label(&prepared.occasion),
        pass_result,
        body,
    })
}

/// The one production entry point: evaluate the selected workflow against the
/// conversation's fixed role in force and the supplied inventory, for CK-1,
/// CK-2 or CK-3. See [`Request`] for the Root seam.
pub fn evaluate(request: Request<'_>) -> Result<Evaluation, String> {
    if let Occasion::EditionChange {
        earlier_report,
        earlier_edition,
    } = &request.occasion
    {
        match nonempty(request.basis.catalog_edition.as_deref()) {
            Some(edition) if edition != earlier_edition && !earlier_report.is_empty() => {}
            _ => {
                return Err(
                    "CK-3 requires the earlier report and a new catalog edition different from its edition"
                        .into(),
                )
            }
        }
    }
    let prepared = PreparedReport::prepare(
        request.selection,
        request.basis,
        request.occasion,
        request.evaluated_at,
        &request.inventory.observations,
        request.role,
    )?;
    let published = publish(
        &prepared,
        &request.inventory,
        request.holding_library.as_deref(),
        request.model_destination.as_ref(),
    );
    Ok(Evaluation {
        prepared,
        inventory_origin: request.inventory.origin,
        published,
    })
}

#[cfg(test)]
#[path = "compatibility_report_tests.rs"]
mod tests;
