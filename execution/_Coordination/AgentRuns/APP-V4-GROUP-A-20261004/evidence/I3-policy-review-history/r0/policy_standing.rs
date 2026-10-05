#[path = "../src/act_policy.rs"]
mod act_policy;
#[path = "../src/schema_validation.rs"]
mod schema_validation;
#[path = "../src/standing.rs"]
mod standing;
use act_policy::*;
use serde_json::Value;
use standing::*;
fn fixture(name: &str) -> Value {
    serde_json::from_str(
        &std::fs::read_to_string(
            std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("resources/policy_standing")
                .join(name),
        )
        .unwrap(),
    )
    .unwrap()
}
fn subject(name: &str, value: &str) -> BoundSubject {
    BoundSubject {
        referent: name.into(),
        content: ContentIdentity {
            method: "fixture-opaque".into(),
            value: value.into(),
        },
    }
}
fn act(kind: ActKind, subjects: Vec<BoundSubject>) -> AdmittedAct {
    AdmittedAct {
        record_ref: "rec:fixture".into(),
        kind,
        actor: "fixture person".into(),
        recorder: "fixture facility".into(),
        capture_ref: "cap:fixture".into(),
        purpose: "fixture purpose".into(),
        subjects,
    }
}
fn scope() -> OperationScope {
    OperationScope {
        workspace: "workspace".into(),
        objects: vec!["row1".into()],
        run: "run1".into(),
        period: None,
        consequence: None,
    }
}
fn grant() -> ConfirmedGrant {
    let setting_content = subject("setting", "direct-row1");
    ConfirmedGrant {
        class_ref: "policy:P-03".into(),
        value: GrantValue::Direct,
        scope: Scope {
            workspace: Some("workspace".into()),
            objects: Some(vec!["row1".into()]),
            run: Some("run1".into()),
            ..Scope::default()
        },
        setting_act: act(ActKind::A12, vec![setting_content.clone()]),
        setting_content,
        control_evidence_ref: "control:fixture".into(),
    }
}
#[test]
fn maintained_contract_examples_validate_without_semantic_admission() {
    let claim =
        SchemaClaim::receive(fixture("ACT_POLICY_CLASS_RECORD.valid.example.json"), false).unwrap();
    assert_eq!(claim.document()["format"], "chirality.act.policy");
    for name in [
        "ACT_POLICY_CLASS_RECORD.invalid.examples.json",
        "AS_SETTINGS_IN.invalid.examples.json",
    ] {
        for case in fixture(name).as_array().unwrap() {
            assert!(
                SchemaClaim::receive(case["instance"].clone(), name.starts_with("AS_")).is_err(),
                "{}",
                case["case"]
            );
        }
    }
    for case in fixture("AS_SETTINGS_IN.valid.examples.json")
        .as_array()
        .unwrap()
    {
        SchemaClaim::receive(case["instance"].clone(), true).unwrap();
    }
    let mut dup = claim.document().clone();
    let item = dup["records"][0].clone();
    dup["records"].as_array_mut().unwrap().push(item);
    assert!(SchemaClaim::receive(dup, false).is_err());
}
#[test]
fn scope_and_real_setting_and_confirmation_are_all_required() {
    let mut g = grant();
    let run = |g: &ConfirmedGrant, s: &OperationScope| {
        resolve(
            Actor::EmbeddedAgent,
            false,
            Class::MayApply,
            "policy:P-03",
            None,
            Intent::Direct,
            s,
            Some(g),
            None,
            true,
        )
    };
    assert_eq!(run(&g, &scope()), Treatment::ApplyDirectly);
    let mut outside = scope();
    outside.objects.push("row2".into());
    assert!(matches!(run(&g, &outside), Treatment::NotPermitted(_)));
    outside = scope();
    outside.run = "run2".into();
    assert!(matches!(run(&g, &outside), Treatment::NotPermitted(_)));
    g.control_evidence_ref.clear();
    assert!(matches!(run(&g, &scope()), Treatment::NotPermitted(_)));
    g = grant();
    g.setting_act.kind = ActKind::A8;
    assert!(matches!(run(&g, &scope()), Treatment::NotPermitted(_)));
    g = grant();
    g.setting_act.capture_ref.clear();
    assert!(matches!(run(&g, &scope()), Treatment::NotPermitted(_)));
    g = grant();
    g.setting_content.content.value = "different".into();
    assert!(matches!(run(&g, &scope()), Treatment::NotPermitted(_)));
    g = grant();
    g.scope.consequence = Some("UNRESOLVED{U-02}".into());
    assert!(matches!(run(&g, &scope()), Treatment::NotPermitted(_)));
}
#[test]
fn reserved_operations_and_default_do_not_create_acceptance() {
    for kind in [
        ActKind::A4,
        ActKind::A5,
        ActKind::A6,
        ActKind::A7,
        ActKind::A10,
        ActKind::A12,
        ActKind::A13,
        ActKind::A15,
        ActKind::A16,
    ] {
        assert_eq!(
            resolve(
                Actor::EmbeddedAgent,
                true,
                Class::MayApply,
                "policy:P-03",
                Some(kind),
                Intent::Direct,
                &scope(),
                Some(&grant()),
                None,
                true
            ),
            Treatment::RequestPerson(Some(kind))
        );
    }
    let default = AdmittedDefault {
        class_ref: "policy:P-03".into(),
        value: GrantValue::Propose,
        decision_basis: "fixture decision".into(),
        host_adoption_evidence: "fixture host".into(),
    };
    assert!(matches!(
        resolve(
            Actor::EmbeddedAgent,
            true,
            Class::MayApply,
            "policy:P-03",
            None,
            Intent::Direct,
            &scope(),
            None,
            Some(&default),
            true
        ),
        Treatment::NotPermitted(_)
    ));
    assert_eq!(
        resolve(
            Actor::ExternalAgent,
            false,
            Class::None,
            "read",
            None,
            Intent::Execute,
            &scope(),
            None,
            None,
            true
        ),
        Treatment::ChannelNotEnabled
    );
    assert_eq!(
        resolve(
            Actor::EmbeddedAgent,
            true,
            Class::NoPolicyBasis,
            "unset",
            None,
            Intent::Propose,
            &scope(),
            None,
            None,
            true
        ),
        Treatment::Propose
    );
    assert!(matches!(
        resolve(
            Actor::EmbeddedAgent,
            true,
            Class::ProposalOnly,
            "p",
            None,
            Intent::Direct,
            &scope(),
            Some(&grant()),
            None,
            true
        ),
        Treatment::NotPermitted(_)
    ));
}
#[test]
fn lapse_compares_opaque_method_and_keeps_observed_history() {
    let s = subject("row1", "v1");
    let changed = subject("row1", "v2");
    assert_eq!(
        compare(&s.content, CurrentContent::Present(&changed.content), false),
        Lapse::Lapsed
    );
    assert_eq!(
        compare(&s.content, CurrentContent::Present(&s.content), true),
        Lapse::MatchesAgainAfterLapse
    );
    let mut other = s.clone();
    other.content.method = "different-method".into();
    assert_eq!(
        compare(&s.content, CurrentContent::Present(&other.content), false),
        Lapse::Incomparable
    );
    assert_eq!(
        compare(&s.content, CurrentContent::Absent, false),
        Lapse::SubjectAbsent
    );
    assert_eq!(
        compare(&s.content, CurrentContent::Unavailable, false),
        Lapse::Unavailable
    );
    assert_eq!(
        compare(&s.content, CurrentContent::NotEvaluated, false),
        Lapse::NotEvaluated
    );
}
#[test]
fn joint_answer_and_non_acts_and_mixed_items() {
    let unchanged = subject("row1", "v1");
    let changed = subject("row2", "v2");
    let earlier = act(ActKind::A4, vec![unchanged.clone(), subject("row2", "v1")]);
    let later = act(ActKind::A4, vec![changed.clone()]);
    assert_eq!(
        joint_answer(
            ActKind::A4,
            &[unchanged.clone(), changed.clone()],
            "fixture purpose",
            &[
                StandingAct {
                    established_setting: None,
                    act: &earlier,
                    subjects: vec![(unchanged.clone(), Lapse::NotLapsed)]
                },
                StandingAct {
                    established_setting: None,
                    act: &later,
                    subjects: vec![(changed.clone(), Lapse::NotLapsed)]
                }
            ]
        )
        .len(),
        2
    );
    assert!(joint_answer(
        ActKind::A4,
        &[unchanged.clone(), changed],
        "fixture purpose",
        &[StandingAct {
            established_setting: None,
            act: &earlier,
            subjects: vec![(unchanged.clone(), Lapse::NotLapsed)]
        }]
    )
    .is_empty());
    for kind in [ActKind::A2, ActKind::A8, ActKind::A9, ActKind::A14] {
        assert!(joint_answer(
            ActKind::A4,
            &[unchanged.clone()],
            "fixture purpose",
            &[StandingAct {
                established_setting: None,
                act: &act(kind, vec![unchanged.clone()]),
                subjects: vec![(unchanged.clone(), Lapse::NotLapsed)]
            }]
        )
        .is_empty());
    }
    let mixed = mixed_items(&[
        ItemDecision::Accepted,
        ItemDecision::Rejected,
        ItemDecision::LeftWithoutDecision,
    ]);
    assert_eq!(mixed.disposition, Disposition::Performed);
    assert!(mixed.partial);
    assert!(!mixed.all_accepted);
    assert_eq!(
        mixed_items(&[ItemDecision::Accepted, ItemDecision::Unknown]).disposition,
        Disposition::Unknown
    );
    assert_eq!(
        mixed_items(&[ItemDecision::Queued]).disposition,
        Disposition::Waiting
    );
    assert_eq!(
        mixed_items(&[ItemDecision::Rejected]).disposition,
        Disposition::ResolvedNegatively
    );
}
#[test]
fn phase_one_lapse_does_not_rehold_or_resume_ended_run() {
    let after = phase_one_overlay(
        Some(ActKind::A4),
        true,
        true,
        Disposition::Performed,
        true,
        false,
        true,
        true,
    );
    assert_eq!(after.disposition, Disposition::Performed);
    assert_eq!(after.label, "act lapsed after resume");
    assert!(after.guidance);
    assert_eq!(
        phase_one_overlay(
            Some(ActKind::A4),
            true,
            true,
            Disposition::Performed,
            false,
            false,
            true,
            false
        )
        .disposition,
        Disposition::Waiting
    );
    assert_eq!(
        phase_one_overlay(
            Some(ActKind::A4),
            true,
            true,
            Disposition::Performed,
            true,
            true,
            true,
            false
        )
        .disposition,
        Disposition::Lapsed
    );
    assert_eq!(
        phase_one_overlay(
            Some(ActKind::A4),
            true,
            true,
            Disposition::Waiting,
            false,
            true,
            false,
            false
        )
        .disposition,
        Disposition::Waiting
    );
    assert_eq!(
        phase_one_overlay(
            Some(ActKind::A15),
            true,
            true,
            Disposition::Waiting,
            false,
            false,
            false,
            false
        )
        .disposition,
        Disposition::Invalid
    );
    assert_eq!(
        phase_one_overlay(
            None,
            false,
            true,
            Disposition::Waiting,
            false,
            false,
            false,
            false
        )
        .disposition,
        Disposition::NotEstablished
    );
}
#[test]
fn pending_request_and_refusal_never_supersede_governing_grant() {
    let prior = grant();
    for state in [
        GrantDisplay::RequestedByAgent,
        GrantDisplay::PendingControl,
        GrantDisplay::Refused,
    ] {
        let view = grant_overlay(Some(&prior), state, None).unwrap();
        assert!(std::ptr::eq(view.governing.unwrap(), &prior));
        assert_eq!(view.annotation, state);
    }
    assert!(grant_overlay(Some(&prior), GrantDisplay::Unconfirmed, None)
        .unwrap()
        .governing
        .is_none());
    assert!(grant_overlay(Some(&prior), GrantDisplay::PersonSet, None).is_err());
}
#[test]
fn returning_to_old_identity_never_silently_restores_checkpoint_act() {
    let s = subject("row1", "v1");
    let a = act(ActKind::A4, vec![s.clone()]);
    for state in [
        Lapse::MatchesAgainAfterLapse,
        Lapse::Incomparable,
        Lapse::Unavailable,
        Lapse::NotEvaluated,
        Lapse::Lapsed,
    ] {
        assert!(joint_answer(
            ActKind::A4,
            &[s.clone()],
            "fixture purpose",
            &[StandingAct {
                established_setting: None,
                act: &a,
                subjects: vec![(s.clone(), state)]
            }]
        )
        .is_empty());
    }
}
#[test]
fn setting_checkpoint_requires_control_establishment_not_only_an_act() {
    let g = grant();
    let pending = StandingAct {
        act: &g.setting_act,
        subjects: vec![(g.setting_content.clone(), Lapse::NotLapsed)],
        established_setting: None,
    };
    assert!(joint_answer(
        ActKind::A12,
        &[g.setting_content.clone()],
        "fixture purpose",
        &[pending]
    )
    .is_empty());
    let confirmed = StandingAct {
        act: &g.setting_act,
        subjects: vec![],
        established_setting: Some(&g),
    };
    assert_eq!(
        joint_answer(
            ActKind::A12,
            &[g.setting_content.clone()],
            "fixture purpose",
            &[confirmed]
        )
        .len(),
        1
    );
}
