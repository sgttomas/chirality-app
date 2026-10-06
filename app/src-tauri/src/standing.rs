//! AS §4/§8 current-phase standing overlay; opaque identities are never computed.
use crate::act_policy::{ActKind, AdmittedAct, BoundSubject, ConfirmedGrant, ContentIdentity};
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Lapse {
    NotLapsed,
    Lapsed,
    SubjectAbsent,
    MatchesAgainAfterLapse,
    Incomparable,
    Unavailable,
    NotEvaluated,
}
#[derive(Debug)]
pub enum CurrentContent<'a> {
    Present(&'a ContentIdentity),
    Absent,
    Unavailable,
    NotEvaluated,
}
pub fn compare(
    bound: &ContentIdentity,
    current: CurrentContent<'_>,
    observed_lapse: bool,
) -> Lapse {
    match current {
        CurrentContent::Absent => Lapse::SubjectAbsent,
        CurrentContent::Unavailable => Lapse::Unavailable,
        CurrentContent::NotEvaluated => Lapse::NotEvaluated,
        CurrentContent::Present(now)
            if bound.method != now.method
                || bound.method.is_empty()
                || now.value.is_empty()
                || bound.value.is_empty() =>
        {
            Lapse::Incomparable
        }
        CurrentContent::Present(now) if bound.value != now.value => Lapse::Lapsed,
        CurrentContent::Present(_) if observed_lapse => Lapse::MatchesAgainAfterLapse,
        CurrentContent::Present(_) => Lapse::NotLapsed,
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ItemDecision {
    Accepted,
    Rejected,
    Queued,
    LeftWithoutDecision,
    Unknown,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Disposition {
    NotReached,
    Waiting,
    Performed,
    ResolvedNegatively,
    Lapsed,
    Unknown,
    Invalid,
    NotEstablished,
}
#[derive(Debug, PartialEq, Eq)]
pub struct MixedStanding {
    pub disposition: Disposition,
    pub partial: bool,
    pub all_accepted: bool,
    pub left_items: usize,
}
pub fn mixed_items(items: &[ItemDecision]) -> MixedStanding {
    use ItemDecision::*;
    let left_items = items.iter().filter(|i| **i == LeftWithoutDecision).count();
    let active: Vec<_> = items
        .iter()
        .filter(|i| **i != LeftWithoutDecision)
        .collect();
    let accepted = active.iter().filter(|i| ***i == Accepted).count();
    let rejected = active.iter().filter(|i| ***i == Rejected).count();
    let disposition = if active.iter().any(|i| **i == Unknown) {
        Disposition::Unknown
    } else if active.is_empty() || active.iter().any(|i| **i == Queued) {
        Disposition::Waiting
    } else if rejected == active.len() {
        Disposition::ResolvedNegatively
    } else {
        Disposition::Performed
    };
    MixedStanding {
        disposition,
        partial: left_items > 0 || (accepted > 0 && rejected > 0),
        all_accepted: !items.is_empty() && accepted == items.len(),
        left_items,
    }
}
/// Actual admitted acts can jointly cover the current scope. Request, A9, A14,
/// effect and ACK claims have no route to this function's act evidence.
#[derive(Debug)]
pub struct StandingAct<'a> {
    pub act: &'a AdmittedAct,
    pub subjects: Vec<(BoundSubject, Lapse)>,
    pub established_setting: Option<&'a ConfirmedGrant>,
}
pub fn joint_answer(
    required: ActKind,
    subjects: &[BoundSubject],
    purpose: &str,
    acts: &[StandingAct<'_>],
) -> Vec<String> {
    if !required.checkpoint_eligible() || subjects.is_empty() {
        return vec![];
    }
    let eligible: Vec<_> = acts
        .iter()
        .filter(|a| {
            a.act.kind == required && a.act.purpose == purpose && a.act.has_required_fields()
        })
        .collect();
    let covers = |a: &StandingAct<'_>, s: &BoundSubject| {
        a.act.subjects.contains(s)
            && if required == ActKind::A12 {
                a.established_setting.is_some_and(|g| {
                    g.setting_act.kind == ActKind::A12
                        && g.setting_act.record_ref == a.act.record_ref
                        && !g.control_evidence_ref.is_empty()
                        && g.setting_content == *s
                        && g.setting_act.has_required_fields()
                        && g.setting_act.subjects.contains(s)
                })
            } else {
                a.subjects
                    .iter()
                    .any(|(bound, state)| bound == s && *state == Lapse::NotLapsed)
            }
    };
    if subjects
        .iter()
        .any(|s| !eligible.iter().any(|a| covers(a, s)))
    {
        return vec![];
    }
    eligible
        .into_iter()
        .filter(|a| subjects.iter().any(|s| covers(a, s)))
        .map(|a| a.act.record_ref.clone())
        .collect()
}
#[derive(Debug, PartialEq, Eq)]
pub struct CheckpointOverlay {
    pub disposition: Disposition,
    pub guidance: bool,
    pub governed_declared: bool,
    pub label: &'static str,
    pub after_run_end: bool,
    pub evidence_limit: Option<&'static str>,
}
/// Disposition is the admitted observation before this overlay. Later acts do
/// not resume an ended run; a lapse after resume is annotated, never re-held.
/// A12 is never lapse-evaluated (RS L-0 / ACT §4.3). Its established
/// successor changes current setting standing, not this arrival's performed
/// disposition. A generic content-lapse observation therefore cannot affect A12.
pub fn phase_one_overlay(
    required: Option<ActKind>,
    recognized: bool,
    reached: bool,
    prior: Disposition,
    resumed: bool,
    ended: bool,
    lapsed: bool,
    governed: bool,
) -> CheckpointOverlay {
    let (disposition, label) = if !recognized {
        (Disposition::NotEstablished, "act kind not established")
    } else if !required.is_some_and(ActKind::checkpoint_eligible) {
        (Disposition::Invalid, "invalid checkpoint act")
    } else if !reached {
        (Disposition::NotReached, "not reached")
    } else if lapsed && prior == Disposition::Performed && required != Some(ActKind::A12) {
        if ended {
            (Disposition::Lapsed, "act lapsed")
        } else if resumed {
            (prior, "act lapsed after resume")
        } else {
            (Disposition::Waiting, "waiting — lapsed")
        }
    } else {
        (
            prior,
            match prior {
                Disposition::Performed => "performed",
                Disposition::ResolvedNegatively => "resolved negatively",
                Disposition::Unknown => "unknown",
                Disposition::Waiting => "waiting",
                Disposition::NotReached => "not reached",
                Disposition::Lapsed => "act lapsed",
                Disposition::Invalid => "invalid checkpoint",
                Disposition::NotEstablished => "not established",
            },
        )
    };
    CheckpointOverlay {
        disposition,
        guidance: true,
        governed_declared: governed,
        label,
        after_run_end: ended,
        evidence_limit: (required == Some(ActKind::A12) && lapsed)
            .then_some("content lapse reported for A12; not applicable — setting standing requires control evidence"),
    }
}
/// Facets remain separately attributed. No combined verified/approved/reliance
/// label is produced by a check result, receipt, or agent examination.
#[derive(Debug, Clone)]
pub struct StandingFacets {
    pub temporal: String,
    pub host_checks: Vec<String>,
    pub host_check_basis: Option<String>,
    pub limitations: Vec<String>,
    pub human_acts: Vec<(String, Lapse)>,
    pub agent_findings: Vec<String>,
    pub evidence_limits: Vec<String>,
    pub outcomes: Vec<String>,
}

/// Reader-supplied scope of comparison, not current control or grant authority.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SettingsRecordRead {
    Written,
    ReadLimited,
    RefusedVersion(String),
}
#[derive(Debug, Clone, Copy, PartialEq, Eq, serde::Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum SettingsComparisonState {
    Match,
    Mismatch,
    #[serde(rename = "missing in record")]
    MissingInRecord,
    #[serde(rename = "missing in display")]
    MissingInDisplay,
}
/// Original claims are retained; duplicate versions never choose a winner.
/// This report has no conversion into AdmittedAct, ConfirmedGrant or treatment.
#[derive(Debug, serde::Serialize)]
pub struct SettingsVersionComparison {
    pub version: String,
    pub state: SettingsComparisonState,
    pub display_claims: Vec<serde_json::Value>,
    pub record_claims: Vec<serde_json::Value>,
    pub metadata_differences: Vec<String>,
    pub operation_grant_differences: Vec<String>,
    pub destination_differences: Vec<String>,
    pub defects: Vec<String>,
    pub limits: Vec<String>,
}
#[derive(Debug, serde::Serialize)]
pub struct SettingsComparison {
    pub versions: Vec<SettingsVersionComparison>,
    pub limits: Vec<String>,
}
/// AS §6 / RS §8: settings documents versus settings_version entry bodies.
/// `record_entries` uses read_log's existing Value entries. ReadLimited bodies
/// contain only known elements supplied by the reader; omission is not absence.
/// RefusedVersion ignores all unreadable record bodies. Supplied read limits,
/// including "destinations not observed", are retained verbatim, never inferred
/// as an empty contact list. Contact/event entries are not settings comparisons.
pub fn compare_settings_versions(
    displayed: &[serde_json::Value],
    record_entries: &[serde_json::Value],
    read: &SettingsRecordRead,
    read_limits: &[String],
) -> SettingsComparison {
    use serde_json::Value;
    use std::collections::BTreeMap;
    let mut display: BTreeMap<String, Vec<Value>> = BTreeMap::new();
    let mut recorded: BTreeMap<String, Vec<Value>> = BTreeMap::new();
    let mut limits = read_limits.to_vec();
    match read {
        SettingsRecordRead::RefusedVersion(v) => limits.push(format!("missing in record (unreadable version {v})")),
        SettingsRecordRead::ReadLimited => limits.push("read limited; compared on supplied known elements only".into()),
        SettingsRecordRead::Written => {},
    }
    let mut collect = |body: &Value, into: &mut BTreeMap<String, Vec<Value>>, side: &str| {
        if let Some(id) = body.get("settingsVersionId").and_then(Value::as_str).filter(|s| !s.is_empty()) {
            into.entry(id.into()).or_default().push(body.clone());
        } else {
            limits.push(format!("{side}: settings version identity not supplied; claim not associated"));
        }
    };
    for body in displayed { collect(body, &mut display, "display"); }
    if !matches!(read, SettingsRecordRead::RefusedVersion(_)) {
        for entry in record_entries {
            if entry.get("kind").and_then(Value::as_str) == Some("settings_version") {
                collect(&entry["body"], &mut recorded, "record");
            }
        }
    }
    let keys: std::collections::BTreeSet<_> = display.keys().chain(recorded.keys()).cloned().collect();
    let mut versions = Vec::new();
    for version in keys {
        let d = display.remove(&version).unwrap_or_default();
        let r = recorded.remove(&version).unwrap_or_default();
        let mut row = SettingsVersionComparison {
            version, state: SettingsComparisonState::Match,
            display_claims: d, record_claims: r,
            metadata_differences: vec![], operation_grant_differences: vec![],
            destination_differences: vec![], defects: vec![], limits: limits.clone(),
        };
        if matches!(read, SettingsRecordRead::RefusedVersion(_)) {
            row.state = SettingsComparisonState::MissingInRecord;
        } else if row.display_claims.is_empty() {
            row.state = SettingsComparisonState::MissingInDisplay;
        } else if row.record_claims.is_empty() {
            row.state = SettingsComparisonState::MissingInRecord;
        }
        if row.display_claims.len() > 1 || row.record_claims.len() > 1 {
            row.state = SettingsComparisonState::Mismatch;
            row.defects.push("duplicate settings version claims; no filename, entry order or content winner selected".into());
        }
        for (side, claims, complete) in [
            ("display", &row.display_claims, true),
            ("record", &row.record_claims, matches!(read, SettingsRecordRead::Written)),
        ] {
            for claim in claims {
                if complete {
                    if let Err(reason) = crate::act_policy::SchemaClaim::receive(claim.clone(), true) {
                        row.defects.push(format!("{side}: invalid settings claim; not an established grant: {reason}"));
                    }
                }
                settings_reference_defects(claim, side, complete, &mut row.defects);
            }
        }
        if row.display_claims.len() == 1 && row.record_claims.len() == 1 {
            let d = &row.display_claims[0]; let r = &row.record_claims[0];
            let partial = matches!(read, SettingsRecordRead::ReadLimited);
            for field in ["settingsVersionId", "runId", "sourceOfControl", "changeKind", "afterOperationEntry"] {
                if (!partial || r.get(field).is_some()) && d.get(field) != r.get(field) {
                    row.metadata_differences.push(field.into());
                }
            }
            compare_settings_part(d.get("operationClassGrants"), r.get("operationClassGrants"),
                "operationClassGrants", partial, &mut row.operation_grant_differences, &mut row.limits);
            compare_settings_part(d.get("destinationSettings"), r.get("destinationSettings"),
                "destinationSettings", partial, &mut row.destination_differences, &mut row.limits);
            if !row.metadata_differences.is_empty() || !row.operation_grant_differences.is_empty()
                || !row.destination_differences.is_empty() || !row.defects.is_empty() {
                row.state = SettingsComparisonState::Mismatch;
            }
        }
        if matches!(read, SettingsRecordRead::RefusedVersion(_)) {
            row.state = SettingsComparisonState::MissingInRecord;
        }
        versions.push(row);
    }
    SettingsComparison { versions, limits }
}
fn settings_reference_defects(body: &serde_json::Value, side: &str, complete: bool, defects: &mut Vec<String>) {
    let missing = |v: &serde_json::Value, field: &str| v.get(field).is_none_or(|s| s.as_str().is_none_or(str::is_empty));
    if let Some(grants) = body["operationClassGrants"].as_array() {
        for (i, g) in grants.iter().enumerate() {
            if (complete || g.get("settingActRef").is_some()) && matches!(g["displayState"].as_str(), Some("effective (person-set)" | "set by person, not yet confirmed by control" | "refused (reason)")) && missing(g, "settingActRef") {
                defects.push(format!("{side}: operationClassGrants/{i}: person-set state lacks A12 reference; not an established setting"));
            }
            if complete && g["displayState"] == "effective (policy default)" &&
                (g["policyDefault"]["policyRecord"]["recordId"].as_str().is_none_or(str::is_empty) ||
                 g["policyDefault"]["policyRecord"]["policyRevision"].as_str().is_none_or(str::is_empty)) {
                defects.push(format!("{side}: operationClassGrants/{i}: policy default lacks policy-class reference; not an established setting"));
            }
        }
    }
    for field in ["categorySwitches", "namedEntries", "alwaysOffItems", "inWorkGrants"] {
        if let Some(items) = body["destinationSettings"][field].as_array() {
            for (i, item) in items.iter().enumerate() {
                let effective = item["displayState"] == "effective (person-set)" || item["state"] == "in force" || item["on"] == true;
                if (complete || item.get("settingActRef").is_some()) && effective && missing(item, "settingActRef") {
                    defects.push(format!("{side}: destinationSettings/{field}/{i}: in-force/on entry lacks A12 reference; not a grant"));
                }
            }
        }
    }
}
// Bounded AS fields only. Known-object members compare recursively; arrays use
// their contract referents, never position/filename/time as a precedence rule.
fn settings_item_key(path: &str, item: &serde_json::Value) -> Option<String> {
    use serde_json::json;
    let key = match path.rsplit('/').next()? {
        "operationClassGrants" => {
            let policy = item.get("policyRecord")?;
            let revision = policy.get("policyRevision")?;
            let id = policy.get("recordId")?;
            let scope = item.get("scope")?;
            json!([revision,id,scope.get("modelOrWorkspace"),scope.get("objectSet"),scope.get("run"),scope.get("period"),scope.get("consequence")])
        },
        "categorySwitches" => json!([item.get("category")?]),
        "namedEntries" => json!([item.get("destination")?,item.get("category")?,item.get("source")?]),
        "alwaysOffItems" => json!([item.get("item")?]),
        "inWorkGrants" => {
            let target = item.get("target")?;
            json!([item.get("requestRef")?, target.get("destination"),target.get("category"),item.get("scope")?])
        },
        "agentRequests" => json!([item.get("requestRef")?]),
        _ => return None,
    };
    Some(key.to_string())
}
fn compare_settings_part(
    displayed: Option<&serde_json::Value>, recorded: Option<&serde_json::Value>,
    path: &str, partial: bool, differences: &mut Vec<String>, limits: &mut Vec<String>,
) {
    use serde_json::Value;
    if partial && recorded.is_none() { return; }
    match (displayed, recorded) {
        (None, None) => {},
        (Some(Value::Object(d)), Some(Value::Object(r))) => {
            let keys: std::collections::BTreeSet<_> = if partial { r.keys().collect() }
                else { d.keys().chain(r.keys()).collect() };
            for key in keys {
                compare_settings_part(d.get(key), r.get(key), &format!("{path}/{key}"), partial, differences, limits);
            }
        },
        (Some(Value::Array(d)), Some(Value::Array(r))) if matches!(path.rsplit('/').next(), Some("operationClassGrants" | "categorySwitches" | "namedEntries" | "alwaysOffItems" | "inWorkGrants" | "agentRequests")) => {
            if partial && path == "operationClassGrants" {
                compare_known_operation_grants(d, r, differences, limits);
                return;
            }
            let mut dm = std::collections::BTreeMap::new(); let mut rm = std::collections::BTreeMap::new();
            for (side, items, map) in [("display", d, &mut dm), ("record", r, &mut rm)] {
                for item in items {
                    let Some(key) = settings_item_key(path, item) else {
                        limits.push(format!("{side}: {path}: known entry referent incomplete; no positional comparison")); continue;
                    };
                    map.entry(key).or_insert_with(Vec::new).push(item);
                }
            }
            let keys: std::collections::BTreeSet<_> = if partial { rm.keys().collect() } else { dm.keys().chain(rm.keys()).collect() };
            for key in keys {
                match (dm.get(key), rm.get(key)) {
                    (Some(ds), Some(rs)) if ds.len()==1 && rs.len()==1 => compare_settings_part(Some(ds[0]),Some(rs[0]),&format!("{path}/{key}"),partial,differences,limits),
                    (Some(ds), Some(rs)) if ds.len()>1 || rs.len()>1 => differences.push(format!("{path}/{key}: duplicate/conflicting entries; no winner selected")),
                    (Some(ds), _) if ds.len()>1 => differences.push(format!("{path}/{key}: duplicate display entries; no winner selected")),
                    (_, Some(rs)) if rs.len()>1 => differences.push(format!("{path}/{key}: duplicate record entries; no winner selected")),
                    _ => differences.push(format!("{path}/{key}: entry missing on one comparison side")),
                }
            }
        },
        (Some(d), Some(r)) if d == r => {},
        _ => differences.push(path.into()),
    }
}

// AS §6 limited comparison retains every supplied scope dimension. Missing
// dimensions are unknown: several compatible full scopes are an evidence limit,
// never duplicate/conflicting grants or a position-selected current grant.
fn compare_known_operation_grants(
    displayed: &[serde_json::Value], recorded: &[serde_json::Value],
    differences: &mut Vec<String>, limits: &mut Vec<String>,
) {
    use serde_json::Value;
    let mut full_display_keys = std::collections::HashSet::new();
    for item in displayed {
        if let Some(key) = settings_item_key("operationClassGrants", item) {
            if !full_display_keys.insert(key) {
                differences.push("operationClassGrants: duplicate/conflicting displayed complete scope; no winner selected".into());
            }
        }
    }
    let mut observed = std::collections::HashSet::new();
    for item in recorded {
        let Some(policy) = item.get("policyRecord").filter(|p| p.get("policyRevision").is_some() && p.get("recordId").is_some()) else {
            limits.push("record: operationClassGrants: known policy referent incomplete; no comparison winner".into());
            continue;
        };
        let candidates: Vec<_> = displayed.iter().enumerate().filter(|(_, d)| {
            d.get("policyRecord").is_some_and(|p| p.get("policyRevision") == policy.get("policyRevision") && p.get("recordId") == policy.get("recordId"))
                && match item.get("scope") {
                    None => true,
                    Some(Value::Object(scope)) => d.get("scope").and_then(Value::as_object).is_some_and(|full| scope.iter().all(|(k,v)|full.get(k)==Some(v))),
                    Some(scope) => d.get("scope") == Some(scope),
                }
        }).collect();
        match candidates.as_slice() {
            [] => differences.push("operationClassGrants: known policy/scope has no matching displayed entry".into()),
            [(index, d)] => {
                // An identical complete scope identifies a repeated claim; an
                // incomplete scope cannot prove repeated referents.
                let complete_scope = item.get("scope") == d.get("scope");
                if complete_scope && !observed.insert(*index) {
                    differences.push("operationClassGrants: duplicate/conflicting recorded complete scope; no winner selected".into());
                    continue;
                }
                compare_settings_part(Some(d), Some(item), "operationClassGrants/known-scope", true, differences, limits);
            },
            _ => limits.push("read limited: operationClassGrants: supplied scope matches multiple displayed entries; scope association unknown; no winner selected".into()),
        }
    }
}
