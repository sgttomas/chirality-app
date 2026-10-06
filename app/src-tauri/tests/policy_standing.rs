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
#[test]
fn reviewer_a12_generic_lapse_never_changes_performed_arrival() {
    for resumed in [false, true] {
        for ended in [false, true] {
            let view = phase_one_overlay(
                Some(ActKind::A12),
                true,
                true,
                Disposition::Performed,
                resumed,
                ended,
                true,
                true,
            );
            assert_eq!(view.disposition, Disposition::Performed);
            assert_eq!(view.label, "performed");
            assert!(view.evidence_limit.is_some());
            assert!(view.guidance);
        }
    }
}
#[test]
fn reviewer_labels_preserve_every_admitted_disposition() {
    for (prior, label) in [
        (Disposition::Lapsed, "act lapsed"),
        (Disposition::Invalid, "invalid checkpoint"),
        (Disposition::NotEstablished, "not established"),
        (Disposition::NotReached, "not reached"),
        (Disposition::Unknown, "unknown"),
        (Disposition::Waiting, "waiting"),
        (Disposition::Performed, "performed"),
        (Disposition::ResolvedNegatively, "resolved negatively"),
    ] {
        let view = phase_one_overlay(
            Some(ActKind::A4),
            true,
            true,
            prior,
            true,
            false,
            false,
            true,
        );
        assert_eq!(view.disposition, prior);
        assert_eq!(view.label, label);
        assert!(view.guidance);
    }
}
#[test]
fn a12_established_successor_changes_setting_but_not_checkpoint_performance() {
    let prior = grant();
    let mut next = grant();
    next.setting_act.record_ref = "rec:successor".into();
    next.value = GrantValue::Propose;
    next.setting_content = subject("setting", "propose-row1");
    next.setting_act.subjects = vec![next.setting_content.clone()];
    next.control_evidence_ref = "control:successor".into();
    let view = grant_overlay(Some(&prior), GrantDisplay::PersonSet, Some(&next)).unwrap();
    assert!(std::ptr::eq(view.governing.unwrap(), &next));
    let before = resolve(
        Actor::EmbeddedAgent,
        false,
        Class::MayApply,
        "policy:P-03",
        None,
        Intent::Direct,
        &scope(),
        Some(&prior),
        None,
        true,
    );
    let after = resolve(
        Actor::EmbeddedAgent,
        false,
        Class::MayApply,
        "policy:P-03",
        None,
        Intent::Direct,
        &scope(),
        view.governing,
        None,
        true,
    );
    assert_eq!(before, Treatment::ApplyDirectly);
    assert!(matches!(after, Treatment::NotPermitted(_)));
    assert_eq!(
        phase_one_overlay(
            Some(ActKind::A12),
            true,
            true,
            Disposition::Performed,
            true,
            false,
            true,
            true
        )
        .disposition,
        Disposition::Performed
    );
    // Refused/pending successors have no effect: the established prior remains direct.
    for state in [
        GrantDisplay::PendingControl,
        GrantDisplay::Refused,
        GrantDisplay::RequestedByAgent,
    ] {
        let unchanged = grant_overlay(Some(&prior), state, None).unwrap();
        assert_eq!(
            resolve(
                Actor::EmbeddedAgent,
                false,
                Class::MayApply,
                "policy:P-03",
                None,
                Intent::Direct,
                &scope(),
                unchanged.governing,
                None,
                true
            ),
            Treatment::ApplyDirectly
        );
    }
}
#[test]
fn reviewer_exact_ended_projection_retains_lapse_and_declaration_labels() {
    for (prior, label) in [
        (Disposition::Lapsed, "act lapsed"),
        (Disposition::Invalid, "invalid checkpoint"),
        (Disposition::NotEstablished, "not established"),
    ] {
        let out = phase_one_overlay(
            Some(ActKind::A4),
            true,
            true,
            prior,
            true,
            true,
            true,
            false,
        );
        assert_eq!(out.disposition, prior);
        assert_eq!(out.label, label);
        assert!(out.evidence_limit.is_none());
        let repeated = phase_one_overlay(
            Some(ActKind::A4),
            true,
            true,
            out.disposition,
            true,
            true,
            true,
            false,
        );
        assert_eq!(repeated.label, label);
    }
    // The exact review reproductions keep governed=false; A12's generic
    // content flag cannot invent lapse before resume or after run end.
    for (resumed, ended) in [(false, false), (true, true)] {
        let out = phase_one_overlay(
            Some(ActKind::A12),
            true,
            true,
            Disposition::Performed,
            resumed,
            ended,
            true,
            false,
        );
        assert_eq!(out.disposition, Disposition::Performed);
        assert!(out.evidence_limit.is_some());
    }
}

fn settings_example() -> Value {
    fixture("AS_SETTINGS_IN.valid.examples.json")[0]["instance"].clone()
}
fn settings_record(body: Value) -> Value {
    serde_json::json!({"kind":"settings_version", "body":body})
}
#[test]
fn settings_comparison_match_missing_and_exact_scope_grant_are_read_only() {
    let display = settings_example();
    let entries = vec![settings_record(display.clone())];
    let original = (display.clone(), entries.clone());
    let matched = compare_settings_versions(&[display.clone()], &entries, &SettingsRecordRead::Written, &[]);
    assert_eq!(matched.versions[0].state, SettingsComparisonState::Match);
    assert!(matched.versions[0].defects.is_empty());
    let mut changed = display.clone();
    changed["operationClassGrants"][0]["scope"]["run"] = "different-run".into();
    changed["operationClassGrants"][0]["grantValue"] = "direct".into();
    let mismatch = compare_settings_versions(&[changed], &entries, &SettingsRecordRead::Written, &[]);
    assert_eq!(mismatch.versions[0].state, SettingsComparisonState::Mismatch);
    assert!(!mismatch.versions[0].operation_grant_differences.is_empty());
    assert!(mismatch.versions[0].destination_differences.is_empty());
    let missing_record = compare_settings_versions(&[display.clone()], &[], &SettingsRecordRead::Written, &[]);
    assert_eq!(missing_record.versions[0].state, SettingsComparisonState::MissingInRecord);
    let missing_display = compare_settings_versions(&[], &entries, &SettingsRecordRead::Written, &[]);
    assert_eq!(missing_display.versions[0].state, SettingsComparisonState::MissingInDisplay);
    assert_eq!((display, entries), original);
}
#[test]
fn settings_comparison_refused_version_and_known_elements_keep_limits() {
    let display = settings_example();
    let entries = vec![settings_record(display.clone())];
    let limits = vec!["destinations not observed".to_string(), "process network not observed".to_string()];
    let refused = compare_settings_versions(&[display.clone()], &entries, &SettingsRecordRead::RefusedVersion("0.99".into()), &limits);
    assert_eq!(refused.versions[0].state, SettingsComparisonState::MissingInRecord);
    assert!(refused.versions[0].record_claims.is_empty());
    assert!(refused.versions[0].limits.iter().any(|s| s == "missing in record (unreadable version 0.99)"));
    assert!(refused.limits.contains(&limits[0]));
    let mut partial = serde_json::json!({"settingsVersionId":display["settingsVersionId"], "sourceOfControl":display["sourceOfControl"]});
    let limited = compare_settings_versions(&[display.clone()], &[settings_record(partial.clone())], &SettingsRecordRead::ReadLimited, &limits);
    assert_eq!(limited.versions[0].state, SettingsComparisonState::Match);
    assert!(limited.versions[0].limits.iter().any(|s| s.contains("read limited")));
    assert!(limited.versions[0].operation_grant_differences.is_empty());
    partial["sourceOfControl"] = if display["sourceOfControl"] == "App" { "host" } else { "App" }.into();
    let mismatch = compare_settings_versions(&[display], &[settings_record(partial)], &SettingsRecordRead::ReadLimited, &limits);
    assert_eq!(mismatch.versions[0].state, SettingsComparisonState::Mismatch);
    assert_eq!(mismatch.versions[0].metadata_differences, vec!["sourceOfControl"]);
    assert!(!serde_json::to_string(&mismatch).unwrap().contains("no destinations contacted"));
}
#[test]
fn settings_comparison_known_partial_grant_does_not_compare_omitted_scope_fields() {
    let display = settings_example();
    let g = &display["operationClassGrants"][0];
    let partial = serde_json::json!({"settingsVersionId":display["settingsVersionId"],"operationClassGrants":[{"policyRecord":g["policyRecord"], "scope":{}, "grantValue":g["grantValue"]}]});
    let result = compare_settings_versions(&[display.clone()], &[settings_record(partial.clone())], &SettingsRecordRead::ReadLimited, &[]);
    assert_eq!(result.versions[0].state, SettingsComparisonState::Match);
    let mut changed = partial; changed["operationClassGrants"][0]["grantValue"] = if g["grantValue"]=="direct" {"propose"} else {"direct"}.into();
    let result = compare_settings_versions(&[display], &[settings_record(changed)], &SettingsRecordRead::ReadLimited, &[]);
    assert_eq!(result.versions[0].state, SettingsComparisonState::Mismatch);
    assert!(result.versions[0].operation_grant_differences.iter().any(|s|s.ends_with("grantValue")));
}
#[test]
fn settings_comparison_destination_separation_and_required_references_are_defects() {
    let cases = fixture("AS_SETTINGS_IN.valid.examples.json");
    let display = cases.as_array().unwrap().iter().map(|c|&c["instance"]).find(|d|d.get("destinationSettings").is_some()).unwrap().clone();
    let mut changed = display.clone();
    changed["destinationSettings"]["modelService"]["service"] = "different-service".into();
    let result = compare_settings_versions(&[display.clone()], &[settings_record(changed)], &SettingsRecordRead::Written, &[]);
    assert_eq!(result.versions[0].state, SettingsComparisonState::Mismatch);
    assert!(result.versions[0].operation_grant_differences.is_empty());
    assert!(!result.versions[0].destination_differences.is_empty());
    let mut invalid = display.clone();
    invalid["destinationSettings"]["inWorkGrants"] = serde_json::json!([{"target":{"destination":"example.test"},"scope":"once","state":"in force","requestRef":"rec:request"}]);
    let original = invalid.clone();
    let result = compare_settings_versions(&[invalid.clone()], &[settings_record(invalid.clone())], &SettingsRecordRead::Written, &[]);
    assert_eq!(result.versions[0].state, SettingsComparisonState::Mismatch);
    assert!(result.versions[0].defects.iter().any(|s| s.contains("not a grant")));
    assert_eq!(invalid, original);
    let mut invalid = settings_example();
    invalid["operationClassGrants"][0]["displayState"]="effective (person-set)".into();
    invalid["operationClassGrants"][0].as_object_mut().unwrap().remove("settingActRef");
    let result = compare_settings_versions(&[invalid.clone()], &[settings_record(invalid)], &SettingsRecordRead::Written, &[]);
    assert!(result.versions[0].defects.iter().any(|s|s.contains("lacks A12 reference")));
    let mut invalid = settings_example();
    invalid["operationClassGrants"][0]["displayState"]="effective (policy default)".into();
    invalid["operationClassGrants"][0].as_object_mut().unwrap().remove("policyDefault");
    let result = compare_settings_versions(&[invalid.clone()], &[settings_record(invalid)], &SettingsRecordRead::Written, &[]);
    assert!(result.versions[0].defects.iter().any(|s|s.contains("lacks policy-class reference")));
}
#[test]
fn settings_comparison_duplicates_never_select_a_version_or_collection_winner() {
    let display = settings_example();
    let mut other = display.clone(); other["sourceOfControl"]="host".into();
    for records in [vec![settings_record(display.clone()),settings_record(other.clone())],vec![settings_record(other),settings_record(display.clone())]] {
        let result = compare_settings_versions(&[display.clone()], &records, &SettingsRecordRead::Written, &[]);
        assert_eq!(result.versions[0].state, SettingsComparisonState::Mismatch);
        assert_eq!(result.versions[0].record_claims.len(), 2);
        assert!(result.versions[0].defects.iter().any(|s|s.contains("no filename")));
    }
    let mut duplicate = display.clone();
    let g = duplicate["operationClassGrants"][0].clone();
    duplicate["operationClassGrants"].as_array_mut().unwrap().push(g);
    let result = compare_settings_versions(&[duplicate.clone()], &[settings_record(duplicate)], &SettingsRecordRead::Written, &[]);
    assert_eq!(result.versions[0].state, SettingsComparisonState::Mismatch);
    assert!(result.versions[0].operation_grant_differences.iter().any(|s|s.contains("no winner")));
    let result = compare_settings_versions(&[display.clone(),display.clone()], &[settings_record(display)], &SettingsRecordRead::Written, &[]);
    assert_eq!(result.versions[0].display_claims.len(),2);
    assert_eq!(result.versions[0].state,SettingsComparisonState::Mismatch);
}
#[test]
fn settings_comparison_empty_inventory_retains_record_read_state() {
    let refused = compare_settings_versions(&[], &[], &SettingsRecordRead::RefusedVersion("0.99".into()), &[]);
    assert!(refused.versions.is_empty());
    assert!(refused.limits.iter().any(|s|s.contains("unreadable version 0.99")));
    let limited = compare_settings_versions(&[], &[], &SettingsRecordRead::ReadLimited, &[]);
    assert!(limited.versions.is_empty());
    assert!(limited.limits.iter().any(|s|s.contains("read limited")));
}
#[test]
fn settings_comparison_known_two_scopes_survive_limited_read() {
    let mut body=settings_example();
    let mut a=body["operationClassGrants"][0].clone();a["scope"]=serde_json::json!({"run":"A"});
    let mut b=a.clone();b["scope"]["run"]="B".into();
    body["operationClassGrants"]=serde_json::json!([a,b]);
    SchemaClaim::receive(body.clone(),true).unwrap();
    for state in [SettingsRecordRead::Written,SettingsRecordRead::ReadLimited] {
        let report=compare_settings_versions(&[body.clone()],&[settings_record(body.clone())],&state,&[]);
        assert_eq!(report.versions[0].state,SettingsComparisonState::Match,"{state:?}: {:?}",report.versions[0].operation_grant_differences);
        assert!(report.versions[0].defects.is_empty());
    }
}
#[test]
fn settings_comparison_incomplete_scope_ambiguity_is_a_limit_not_conflict() {
    let mut body=settings_example();
    let mut a=body["operationClassGrants"][0].clone();a["scope"]=serde_json::json!({"run":"A"});
    let mut b=a.clone();b["scope"]["run"]="B".into();
    body["operationClassGrants"]=serde_json::json!([a,b]);
    let mut known=body.clone();
    known["operationClassGrants"]=serde_json::json!([{"policyRecord":body["operationClassGrants"][0]["policyRecord"],"scope":{}}]);
    let original=(body.clone(),known.clone());
    let report=compare_settings_versions(&[body.clone()],&[settings_record(known.clone())],&SettingsRecordRead::ReadLimited,&[]);
    assert_eq!(report.versions[0].state,SettingsComparisonState::Match);
    assert!(report.versions[0].operation_grant_differences.is_empty());
    assert!(report.versions[0].limits.iter().any(|s|s.contains("scope association unknown; no winner selected")));
    assert_eq!((body.clone(),known),original);
    let mut changed=body.clone();changed["operationClassGrants"][0]["grantValue"]="direct".into();
    let report=compare_settings_versions(&[body.clone()],&[settings_record(changed)],&SettingsRecordRead::ReadLimited,&[]);
    assert_eq!(report.versions[0].state,SettingsComparisonState::Mismatch);
    assert!(!report.versions[0].operation_grant_differences.is_empty());
    let mut absent=body.clone();absent["operationClassGrants"][0]["scope"]["run"]="C".into();
    let report=compare_settings_versions(&[body],&[settings_record(absent)],&SettingsRecordRead::ReadLimited,&[]);
    assert_eq!(report.versions[0].state,SettingsComparisonState::Mismatch);
}
