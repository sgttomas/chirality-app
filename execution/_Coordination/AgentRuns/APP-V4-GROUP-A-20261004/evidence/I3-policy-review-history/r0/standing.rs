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
}
/// Disposition is the admitted observation before this overlay. Later acts do
/// not resume an ended run; a lapse after resume is annotated, never re-held.
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
    } else if lapsed && prior == Disposition::Performed {
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
                _ => "waiting",
            },
        )
    };
    CheckpointOverlay {
        disposition,
        guidance: true,
        governed_declared: governed,
        label,
        after_run_end: ended,
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
