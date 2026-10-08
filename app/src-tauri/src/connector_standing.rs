//! Provider-independent DEL-07-02 CFB §2–3 projection. Inputs are semantic
//! assessments from receiving owners, not provider wire data. This module
//! neither establishes adoption nor reads sources, performs duties or places
//! route accounts. Simulated assessments remain visibly simulated.
use serde::Serialize;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Connector {
    Pec,
    Domains,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Envelope {
    Adopted,
    NotAdopted,
    OutsideCoverage,
    Unknown,
}
/// Declaration order is CFB §2.2 precedence, not freshness derivation.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Condition {
    Absent,
    Failing,
    Partial,
    Stale,
    Unknown,
    Current,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ClaimTier {
    Record,
    PresenceAdvisory,
    Admitted,
    LocatedNotAdmitted,
    Unknown,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(tag = "kind", content = "basis", rename_all = "snake_case")]
pub enum InputBasis {
    Simulated(String),
    ReceivingOwnerAssessment(String),
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct Assessment<T> {
    pub value: T,
    pub basis: String,
}
/// Metadata describes the supplied basis; no thresholds or provider terms are
/// inferred. Missing metadata stays None, not complete/fresh/authoritative.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct MaterialInput {
    pub item_ref: String,
    pub source_identity: Option<String>,
    pub coverage: Option<String>,
    pub freshness: Option<String>,
    pub envelope: Option<Assessment<Envelope>>,
    pub conditions: Vec<Assessment<Condition>>,
    pub claim_tier: Option<Assessment<ClaimTier>>,
    pub input_basis: InputBasis,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct Reason {
    facet: &'static str,
    value: String,
    basis: String,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct Standing {
    connector: Connector,
    envelope: Envelope,
    condition: Condition,
    claim_tier: ClaimTier,
    supports_reliance: bool,
    reasons: Vec<Reason>,
}
impl Standing {
    pub fn supports_reliance(&self) -> bool {
        self.supports_reliance
    }
    pub fn condition(&self) -> Condition {
        self.condition
    }
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct MaterialProjection {
    pub input: MaterialInput,
    pub standing: Standing,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ProjectionError {
    EmptyBasis,
    EmptyIdentity,
    WrongConnectorTier,
    DuplicatePart,
    DuplicateItem,
}
fn nonempty(s: &str) -> bool {
    !s.trim().is_empty()
}
fn reason<T: Serialize>(facet: &'static str, value: T, basis: String) -> Reason {
    let value = serde_json::to_value(value)
        .expect("enum serialization")
        .as_str()
        .unwrap()
        .to_owned();
    Reason {
        facet,
        value,
        basis,
    }
}

pub fn project_material(
    connector: Connector,
    input: MaterialInput,
) -> Result<MaterialProjection, ProjectionError> {
    if !nonempty(&input.item_ref) {
        return Err(ProjectionError::EmptyIdentity);
    }
    let basis = match &input.input_basis {
        InputBasis::Simulated(s) | InputBasis::ReceivingOwnerAssessment(s) => s,
    };
    if !nonempty(basis)
        || input.envelope.as_ref().is_some_and(|a| !nonempty(&a.basis))
        || input
            .claim_tier
            .as_ref()
            .is_some_and(|a| !nonempty(&a.basis))
        || input.conditions.iter().any(|a| !nonempty(&a.basis))
    {
        return Err(ProjectionError::EmptyBasis);
    }
    let tier = input
        .claim_tier
        .as_ref()
        .map_or(ClaimTier::Unknown, |a| a.value);
    if matches!(
        (connector, tier),
        (
            Connector::Pec,
            ClaimTier::Admitted | ClaimTier::LocatedNotAdmitted
        ) | (
            Connector::Domains,
            ClaimTier::Record | ClaimTier::PresenceAdvisory
        )
    ) {
        return Err(ProjectionError::WrongConnectorTier);
    }
    let condition = input
        .conditions
        .iter()
        .map(|a| a.value)
        .min()
        .unwrap_or(Condition::Unknown);
    let absent = condition == Condition::Absent;
    let envelope = if absent {
        Envelope::Unknown
    } else {
        input
            .envelope
            .as_ref()
            .map_or(Envelope::Unknown, |a| a.value)
    };
    let tier = if absent { ClaimTier::Unknown } else { tier };
    let mut reasons: Vec<_> = input
        .conditions
        .iter()
        .map(|a| reason("condition", a.value, a.basis.clone()))
        .collect();
    if input.conditions.is_empty() {
        reasons.push(reason(
            "condition",
            Condition::Unknown,
            "No condition assessment supplied".into(),
        ));
    }
    reasons.push(reason(
        "envelope",
        envelope,
        if absent {
            "No response; no material envelope".into()
        } else {
            input
                .envelope
                .as_ref()
                .map_or("Envelope basis not supplied".into(), |a| a.basis.clone())
        },
    ));
    reasons.push(reason(
        "claim_tier",
        tier,
        if absent {
            "No response; no material tier".into()
        } else {
            input
                .claim_tier
                .as_ref()
                .map_or("Claim tier not supplied".into(), |a| a.basis.clone())
        },
    ));
    let reliable = matches!(
        (connector, tier),
        (Connector::Pec, ClaimTier::Record) | (Connector::Domains, ClaimTier::Admitted)
    );
    let standing = Standing {
        connector,
        envelope,
        condition,
        claim_tier: tier,
        supports_reliance: envelope == Envelope::Adopted
            && condition == Condition::Current
            && reliable,
        reasons,
    };
    Ok(MaterialProjection { input, standing })
}
/// required_items is the receiving owner's trusted assertion of complete
/// coverage; optional coverage text is retained, not verified here.
/// Receiving owners select complete question coverage. Empty required_items is
/// uncovered. A missing required item is an absent/unknown input, never omitted.
#[derive(Clone, Debug)]
pub struct QuestionPart {
    pub id: String,
    pub text: String,
    pub required_items: Vec<MaterialInput>,
}
#[derive(Clone, Debug)]
pub struct Question {
    pub id: String,
    pub at_revision: String,
    pub since_revision: Option<String>,
    pub parts: Vec<QuestionPart>,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum PartRoute {
    ConnectorReliance,
    SourceRouteNeeded,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct Unsupported {
    pub conclusion: String,
    pub why: String,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct PartProjection {
    pub id: String,
    pub text: String,
    pub route: PartRoute,
    pub items: Vec<MaterialProjection>,
    pub unsupported: Vec<Unsupported>,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct QuestionProjection {
    pub connector: Connector,
    pub question_id: String,
    pub at_revision: String,
    pub since_revision: Option<String>,
    pub parts: Vec<PartProjection>,
    pub source_route_needed: bool,
    pub prohibited: [&'static str; 4],
    pub unsupported: Vec<Unsupported>,
    pub limits: Vec<&'static str>,
}
/// No other connector state, readiness or human act participates in this call.
pub fn project_question(
    connector: Connector,
    question: Question,
) -> Result<QuestionProjection, ProjectionError> {
    if !nonempty(&question.id)
        || !nonempty(&question.at_revision)
        || question
            .since_revision
            .as_ref()
            .is_some_and(|r| !nonempty(r))
    {
        return Err(ProjectionError::EmptyIdentity);
    }
    let mut parts = Vec::new();
    let mut ids = std::collections::HashSet::new();
    for part in question.parts {
        if !nonempty(&part.id) || !nonempty(&part.text) {
            return Err(ProjectionError::EmptyIdentity);
        }
        if !ids.insert(part.id.clone()) {
            return Err(ProjectionError::DuplicatePart);
        }
        let mut item_ids = std::collections::HashSet::new();
        let mut items = Vec::new();
        for item in part.required_items {
            if !item_ids.insert(item.item_ref.clone()) {
                return Err(ProjectionError::DuplicateItem);
            }
            items.push(project_material(connector, item)?);
        }
        let supported = !items.is_empty() && items.iter().all(|i| i.standing.supports_reliance());
        let unsupported = if supported {
            Vec::new()
        } else {
            vec![Unsupported {
                conclusion: part.text.clone(),
                why: if items.is_empty() {
                    "No covering material supplied; locate underlying sources and identify missing inputs".into()
                } else {
                    format!("Required material does not support reliance: {}. Locate and compare underlying sources; unresolved inputs remain unsatisfied",
                    items.iter().filter(|i| !i.standing.supports_reliance()).map(|i| i.input.item_ref.as_str()).collect::<Vec<_>>().join(", "))
                },
            }]
        };
        parts.push(PartProjection {
            id: part.id,
            text: part.text,
            route: if supported {
                PartRoute::ConnectorReliance
            } else {
                PartRoute::SourceRouteNeeded
            },
            items,
            unsupported,
        });
    }
    let source_route_needed = parts.is_empty()
        || parts
            .iter()
            .any(|p| p.route == PartRoute::SourceRouteNeeded);
    Ok(QuestionProjection {
        connector, question_id: question.id, at_revision: question.at_revision, since_revision: question.since_revision, parts, source_route_needed,
        prohibited: ["no_work", "ready", "permitted", "correct_by_presence"],
        unsupported: vec![Unsupported {
            conclusion: "No work remains; any item is ready to start, may be dispatched, is permitted, complete or done; anything is correct because of presence".into(),
            why: "CFB CS-R2/CS-R5: connector material establishes none of these; a relied PEC record reports only what its cited record states at its pin".into(),
        }],
        limits: vec!["Projection only: receiving owners establish assessments and coverage; no provider qualification or adoption is established here",
            "Independent work may continue on its own sound basis; a connector-only part waits for its named missing inputs",
            "Source route requires agent location/comparison, manager review/integration and any necessary human cross-undertaking coordination; this projection performs none of those duties",
            "Reading sources alone establishes no authority; gaps and contradictions require resolution by their owners"],
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    fn assessed<T>(value: T) -> Assessment<T> {
        Assessment {
            value,
            basis: "constructed assessment".into(),
        }
    }
    fn input(connector: Connector, condition: Condition) -> MaterialInput {
        MaterialInput {
            item_ref: "item-1".into(),
            source_identity: Some("fixture@revision".into()),
            coverage: Some("part-a".into()),
            freshness: Some("constructed comparison".into()),
            envelope: Some(assessed(Envelope::Adopted)),
            conditions: vec![assessed(condition)],
            claim_tier: Some(assessed(if connector == Connector::Pec {
                ClaimTier::Record
            } else {
                ClaimTier::Admitted
            })),
            input_basis: InputBasis::Simulated(
                "invented input; no provider or adoption evidence".into(),
            ),
        }
    }
    fn question(items: Vec<MaterialInput>) -> Question {
        Question {
            id: "Q1".into(),
            at_revision: "asked".into(),
            since_revision: Some("since".into()),
            parts: vec![QuestionPart {
                id: "a".into(),
                text: "What does the cited record state?".into(),
                required_items: items,
            }],
        }
    }
    #[test]
    fn exhaustive_reliance_and_schema_vocabulary() {
        let mut schema: serde_json::Value = serde_json::from_str(include_str!(concat!(env!("CARGO_MANIFEST_DIR"),
            "/../../execution/PKG-07_PEC receiving and connector fallback/1_Working/DEL-07-02_Connector limitation and source-file recovery paths/Design/connector.standing.schema.json"))).unwrap();
        schema["$ref"] = serde_json::json!("#/$defs/standing");
        let validator = jsonschema::validator_for(&schema).unwrap();
        for connector in [Connector::Pec, Connector::Domains] {
            for envelope in [
                Envelope::Adopted,
                Envelope::NotAdopted,
                Envelope::OutsideCoverage,
                Envelope::Unknown,
            ] {
                for condition in [
                    Condition::Absent,
                    Condition::Failing,
                    Condition::Partial,
                    Condition::Stale,
                    Condition::Unknown,
                    Condition::Current,
                ] {
                    for tier in [
                        ClaimTier::Record,
                        ClaimTier::PresenceAdvisory,
                        ClaimTier::Admitted,
                        ClaimTier::LocatedNotAdmitted,
                        ClaimTier::Unknown,
                    ] {
                        let mut i = input(connector, condition);
                        i.envelope = Some(assessed(envelope));
                        i.claim_tier = Some(assessed(tier));
                        let valid_tier = match connector {
                            Connector::Pec => matches!(
                                tier,
                                ClaimTier::Record
                                    | ClaimTier::PresenceAdvisory
                                    | ClaimTier::Unknown
                            ),
                            Connector::Domains => matches!(
                                tier,
                                ClaimTier::Admitted
                                    | ClaimTier::LocatedNotAdmitted
                                    | ClaimTier::Unknown
                            ),
                        };
                        let result = project_material(connector, i);
                        if !valid_tier {
                            assert_eq!(result.unwrap_err(), ProjectionError::WrongConnectorTier);
                            continue;
                        }
                        let p = result.unwrap();
                        let expected = envelope == Envelope::Adopted
                            && condition == Condition::Current
                            && matches!(
                                (connector, tier),
                                (Connector::Pec, ClaimTier::Record)
                                    | (Connector::Domains, ClaimTier::Admitted)
                            );
                        assert_eq!(p.standing.supports_reliance(), expected);
                        assert!(validator.is_valid(&serde_json::to_value(&p.standing).unwrap()));
                        if condition == Condition::Absent {
                            assert_eq!(p.standing.envelope, Envelope::Unknown);
                        }
                    }
                }
            }
        }
    }
    #[test]
    fn every_condition_subset_obeys_precedence_without_dropping_reasons() {
        let ordered = [
            Condition::Absent,
            Condition::Failing,
            Condition::Partial,
            Condition::Stale,
            Condition::Unknown,
            Condition::Current,
        ];
        for mask in 0..64 {
            let mut i = input(Connector::Pec, Condition::Current);
            i.conditions = ordered
                .iter()
                .enumerate()
                .filter(|(n, _)| mask & (1 << n) != 0)
                .map(|(_, c)| assessed(*c))
                .collect();
            let expected = i.conditions.first().map_or(Condition::Unknown, |a| a.value);
            i.conditions.reverse();
            let p = project_material(Connector::Pec, i.clone()).unwrap();
            assert_eq!(p.standing.condition(), expected);
            for c in &i.conditions {
                assert!(p.standing.reasons.contains(&reason(
                    "condition",
                    c.value,
                    c.basis.clone()
                )));
            }
        }
    }
    #[test]
    fn missing_metadata_and_assessments_remain_unknown() {
        let mut i = input(Connector::Pec, Condition::Current);
        i.source_identity = None;
        i.coverage = None;
        i.freshness = None;
        i.envelope = None;
        i.claim_tier = None;
        i.conditions.clear();
        let p = project_material(Connector::Pec, i).unwrap();
        assert_eq!(p.standing.condition, Condition::Unknown);
        assert_eq!(p.standing.envelope, Envelope::Unknown);
        assert_eq!(p.standing.claim_tier, ClaimTier::Unknown);
        assert!(!p.standing.supports_reliance());
        let value = serde_json::to_value(p).unwrap();
        for field in ["source_identity", "coverage", "freshness"] {
            assert!(value["input"][field].is_null());
        }
        assert_eq!(value["input"]["input_basis"]["kind"], "simulated");
    }
    #[test]
    fn same_question_routes_all_limitation_cases_and_preserves_identity() {
        for connector in [Connector::Pec, Connector::Domains] {
            for condition in [
                Condition::Absent,
                Condition::Failing,
                Condition::Partial,
                Condition::Stale,
                Condition::Unknown,
                Condition::Current,
            ] {
                let p = project_question(connector, question(vec![input(connector, condition)]))
                    .unwrap();
                assert_eq!(
                    (
                        &*p.question_id,
                        &*p.at_revision,
                        p.since_revision.as_deref()
                    ),
                    ("Q1", "asked", Some("since"))
                );
                assert_eq!(p.source_route_needed, condition != Condition::Current);
                assert_eq!(
                    p.prohibited,
                    ["no_work", "ready", "permitted", "correct_by_presence"]
                );
                assert!(p.unsupported[0].conclusion.contains("complete or done"));
                if p.source_route_needed {
                    assert!(p.parts[0].unsupported[0].why.contains("item-1"));
                }
            }
        }
    }
    #[test]
    fn mixed_parts_all_needed_items_and_uncovered_parts() {
        let mut q = question(vec![input(Connector::Pec, Condition::Current)]);
        let mut stale = input(Connector::Pec, Condition::Stale);
        stale.item_ref = "item-2".into();
        q.parts.push(QuestionPart {
            id: "b".into(),
            text: "Whole change list".into(),
            required_items: vec![input(Connector::Pec, Condition::Current), stale],
        });
        q.parts.push(QuestionPart {
            id: "c".into(),
            text: "Uncovered question".into(),
            required_items: vec![],
        });
        let p = project_question(Connector::Pec, q).unwrap();
        assert_eq!(
            p.parts.iter().map(|p| &p.route).collect::<Vec<_>>(),
            vec![
                &PartRoute::ConnectorReliance,
                &PartRoute::SourceRouteNeeded,
                &PartRoute::SourceRouteNeeded
            ]
        );
        assert!(p.source_route_needed);
        assert!(p.parts[1].unsupported[0].why.contains("item-2"));
        assert!(!p.parts[2].unsupported.is_empty());
        assert!(
            project_question(Connector::Pec, question(vec![]))
                .unwrap()
                .source_route_needed
        );
        let mut empty = question(vec![]);
        empty.parts.clear();
        assert!(
            project_question(Connector::Pec, empty)
                .unwrap()
                .source_route_needed
        );
    }
    #[test]
    fn connector_independence_and_later_join_do_not_rewrite_earlier_projection() {
        let before = project_question(
            Connector::Pec,
            question(vec![input(Connector::Pec, Condition::Absent)]),
        )
        .unwrap();
        let saved = before.clone();
        for pec in [Condition::Absent, Condition::Current] {
            for domains in [Condition::Absent, Condition::Current, Condition::Stale] {
                let p =
                    project_question(Connector::Pec, question(vec![input(Connector::Pec, pec)]))
                        .unwrap();
                let d = project_question(
                    Connector::Domains,
                    question(vec![input(Connector::Domains, domains)]),
                )
                .unwrap();
                assert_eq!(p.source_route_needed, pec == Condition::Absent);
                assert_eq!(d.source_route_needed, domains != Condition::Current);
            }
        }
        assert_eq!(before, saved);
        let mut unadopted = input(Connector::Pec, Condition::Current);
        unadopted.envelope = Some(assessed(Envelope::NotAdopted));
        assert!(
            project_question(Connector::Pec, question(vec![unadopted]))
                .unwrap()
                .source_route_needed
        );
    }
    #[test]
    fn invalid_identity_basis_and_ambiguous_duplicate_inputs_are_rejected() {
        let mut i = input(Connector::Pec, Condition::Current);
        i.conditions[0].basis = " ".into();
        assert_eq!(
            project_material(Connector::Pec, i).unwrap_err(),
            ProjectionError::EmptyBasis
        );
        let i = input(Connector::Pec, Condition::Current);
        assert_eq!(
            project_question(Connector::Pec, question(vec![i.clone(), i])).unwrap_err(),
            ProjectionError::DuplicateItem
        );
        let mut q = question(vec![]);
        q.parts.push(q.parts[0].clone());
        assert_eq!(
            project_question(Connector::Pec, q).unwrap_err(),
            ProjectionError::DuplicatePart
        );
        let mut q = question(vec![]);
        q.at_revision = String::new();
        assert_eq!(
            project_question(Connector::Pec, q).unwrap_err(),
            ProjectionError::EmptyIdentity
        );
    }
}
