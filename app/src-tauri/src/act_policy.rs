//! ACT §2/§5 producer→consumer policy unit. This is not an admission or capture facility.
//! Schema-valid documents remain claims; trusted inputs must come from the owning
//! host route/native capture admission, never from deserializing writable files.
use crate::schema_validation::compile_targets;
use serde_json::Value;

pub const POLICY_ID: &str = "urn:chirality:app-v4:del-04-01:policy-class-record:0.1";
pub const SETTINGS_ID: &str = "urn:chirality:app-v4:del-04-02:settings-in:0.1";
/// Validated shape only. No conversion into AdmittedAct or ConfirmedGrant exists.
#[derive(Debug)]
pub struct SchemaClaim(Value);
impl SchemaClaim {
    pub fn receive(value: Value, settings: bool) -> Result<Self, String> {
        let resources = [
            (
                "policy",
                include_str!("../schemas/ACT_POLICY_CLASS_RECORD.schema.json"),
            ),
            (
                "settings",
                include_str!("../schemas/AS_SETTINGS_IN.schema.json"),
            ),
        ];
        let target = if settings { SETTINGS_ID } else { POLICY_ID };
        let validator =
            compile_targets(&resources, &[POLICY_ID, SETTINGS_ID], &[target])?.remove(0);
        validator
            .validate(&value)
            .map_err(|e| format!("policy/settings schema refused: {e}"))?;
        if !settings {
            let mut ids = std::collections::HashSet::new();
            for record in value["records"].as_array().unwrap() {
                if !ids.insert(record["recordId"].as_str().unwrap()) {
                    return Err("duplicate policy record identity".into());
                }
                if record["humanActClass"] == "reserved to the person"
                    && record["widenable"] != "no"
                {
                    return Err("reserved policy record is widenable".into());
                }
            }
        }
        Ok(Self(value))
    }
    pub fn document(&self) -> &Value {
        &self.0
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ActKind {
    A1,
    A2,
    A3,
    A4,
    A5,
    A6,
    A7,
    A8,
    A9,
    A10,
    A11,
    A12,
    A13,
    A14,
    A15,
    A16,
}
impl ActKind {
    pub fn person_only(self) -> bool {
        matches!(
            self,
            Self::A4
                | Self::A5
                | Self::A6
                | Self::A7
                | Self::A10
                | Self::A12
                | Self::A13
                | Self::A15
                | Self::A16
        )
    }
    pub fn checkpoint_eligible(self) -> bool {
        matches!(self, Self::A4 | Self::A5 | Self::A6 | Self::A7 | Self::A12)
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContentIdentity {
    pub method: String,
    pub value: String,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundSubject {
    pub referent: String,
    pub content: ContentIdentity,
}
/// Caller-owned admission assertion, NOT cryptographic evidence or a file reader.
/// Must be constructed only after actual actor, native/host capture, kind, scope,
/// purpose and evidence have been admitted by the owning facility.
#[derive(Debug, Clone)]
pub struct AdmittedAct {
    pub record_ref: String,
    pub kind: ActKind,
    pub actor: String,
    pub recorder: String,
    pub capture_ref: String,
    pub purpose: String,
    pub subjects: Vec<BoundSubject>,
}
impl AdmittedAct {
    pub fn has_required_fields(&self) -> bool {
        !self.record_ref.is_empty()
            && !self.actor.is_empty()
            && !self.recorder.is_empty()
            && !self.capture_ref.is_empty()
            && !self.purpose.is_empty()
            && !self.subjects.is_empty()
            && self.subjects.iter().all(|s| {
                !s.referent.is_empty()
                    && !s.content.method.is_empty()
                    && !s.content.value.is_empty()
            })
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Actor {
    Person,
    EmbeddedAgent,
    ExternalAgent,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Class {
    None,
    MayApply,
    ProposalOnly,
    Reserved,
    NoPolicyBasis,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Intent {
    Execute,
    Direct,
    Propose,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GrantValue {
    Direct,
    Propose,
}
/// Period and consequence are opaque. The owning control must evaluate those
/// dimensions explicitly; absence of that evaluation never implies coverage.
#[derive(Debug, Clone, Default)]
pub struct Scope {
    pub workspace: Option<String>,
    pub objects: Option<Vec<String>>,
    pub run: Option<String>,
    pub period: Option<String>,
    pub consequence: Option<String>,
}
#[derive(Debug)]
pub struct OperationScope {
    pub workspace: String,
    pub objects: Vec<String>,
    pub run: String,
    pub period: Option<String>,
    pub consequence: Option<String>,
}
impl Scope {
    pub fn covers(&self, op: &OperationScope) -> bool {
        self.workspace.as_ref().is_none_or(|v| v == &op.workspace)
            && self.run.as_ref().is_none_or(|v| v == &op.run)
            && self
                .objects
                .as_ref()
                .is_none_or(|v| op.objects.iter().all(|o| v.contains(o)))
            && self
                .period
                .as_ref()
                .is_none_or(|v| op.period.as_ref() == Some(v))
            && self
                .consequence
                .as_ref()
                .is_none_or(|v| v != "UNRESOLVED{U-02}" && op.consequence.as_ref() == Some(v))
    }
}
#[derive(Debug)]
pub struct ConfirmedGrant {
    pub class_ref: String,
    pub value: GrantValue,
    pub scope: Scope,
    pub setting_act: AdmittedAct,
    pub setting_content: BoundSubject,
    pub control_evidence_ref: String,
}
impl ConfirmedGrant {
    fn effective_for(&self, class_ref: &str, scope: &OperationScope) -> bool {
        self.class_ref == class_ref
            && !self.control_evidence_ref.is_empty()
            && self.setting_act.kind == ActKind::A12
            && self.setting_act.has_required_fields()
            && self.setting_act.subjects.contains(&self.setting_content)
            && self.scope.covers(scope)
    }
}
/// Default is a separately admitted policy value, not a schema claim. Host
/// adoption and the decision basis must be supplied by the route owner.
#[derive(Debug)]
pub struct AdmittedDefault {
    pub class_ref: String,
    pub value: GrantValue,
    pub decision_basis: String,
    pub host_adoption_evidence: String,
}
#[derive(Debug, PartialEq, Eq)]
pub enum Treatment {
    Execute,
    ApplyDirectly,
    Propose,
    RequestPerson(Option<ActKind>),
    NotPermitted(&'static str),
    ChannelNotEnabled,
    NoPolicyBasis(&'static str),
}
/// Pure resolution at validation AND application. Phase-1 declarations do not
/// enter this function as enforced constraints. It creates no act or request.
pub fn resolve(
    actor: Actor,
    external_access_admitted: bool,
    class: Class,
    class_ref: &str,
    performs: Option<ActKind>,
    intent: Intent,
    scope: &OperationScope,
    grant: Option<&ConfirmedGrant>,
    default: Option<&AdmittedDefault>,
    effectful_none_basis: bool,
) -> Treatment {
    if actor == Actor::ExternalAgent && !external_access_admitted {
        return Treatment::ChannelNotEnabled;
    }
    if actor == Actor::Person {
        return Treatment::Execute;
    }
    if performs.is_some_and(ActKind::person_only) || class == Class::Reserved {
        return Treatment::RequestPerson(performs);
    }
    match class {
        Class::NoPolicyBasis => {
            if intent == Intent::Propose {
                Treatment::Propose
            } else {
                Treatment::NoPolicyBasis("no policy basis — held")
            }
        }
        Class::ProposalOnly => {
            if intent == Intent::Direct {
                Treatment::NotPermitted("proposal only")
            } else {
                Treatment::Propose
            }
        }
        Class::MayApply => {
            let effective = grant
                .filter(|g| g.effective_for(class_ref, scope))
                .map(|g| g.value)
                .or_else(|| {
                    default
                        .filter(|d| {
                            d.class_ref == class_ref
                                && !d.decision_basis.is_empty()
                                && !d.host_adoption_evidence.is_empty()
                        })
                        .map(|d| d.value)
                });
            if intent == Intent::Direct {
                if effective == Some(GrantValue::Direct) {
                    Treatment::ApplyDirectly
                } else {
                    Treatment::NotPermitted("no effective direct grant in scope")
                }
            } else {
                Treatment::Propose
            }
        }
        Class::None => {
            if effectful_none_basis {
                Treatment::Execute
            } else {
                Treatment::NoPolicyBasis("effectful none needs decision basis")
            }
        }
        Class::Reserved => unreachable!(),
    }
}
/// Non-effective observations are annotations beside the governing state. They
/// never supersede it. Confirmation loss clears current authority explicitly.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GrantDisplay {
    PersonSet,
    PolicyDefault,
    RequestedByAgent,
    PendingControl,
    Unconfirmed,
    NotSet,
    Refused,
}
#[derive(Debug)]
pub struct GrantOverlay<'a> {
    pub governing: Option<&'a ConfirmedGrant>,
    pub annotation: GrantDisplay,
}
pub fn grant_overlay<'a>(
    prior: Option<&'a ConfirmedGrant>,
    change: GrantDisplay,
    established: Option<&'a ConfirmedGrant>,
) -> Result<GrantOverlay<'a>, String> {
    let governing = match change {
        GrantDisplay::PersonSet => {
            let next =
                established.ok_or("person-set needs admitted A12 and established control")?;
            if next.setting_act.kind != ActKind::A12
                || !next.setting_act.has_required_fields()
                || next.control_evidence_ref.is_empty()
                || !next.setting_act.subjects.contains(&next.setting_content)
            {
                return Err("person-set needs admitted A12 and established control".into());
            }
            Some(next)
        }
        GrantDisplay::RequestedByAgent | GrantDisplay::PendingControl | GrantDisplay::Refused => {
            prior
        }
        GrantDisplay::Unconfirmed | GrantDisplay::NotSet | GrantDisplay::PolicyDefault => None,
    };
    Ok(GrantOverlay {
        governing,
        annotation: change,
    })
}
