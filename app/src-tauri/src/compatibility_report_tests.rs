use super::*;
use serde_json::json;
fn declaration(roles: Value, required: bool) -> Declaration {
    let mut value = json!({"declaration_contract_version":"WD-v0.8","required_tools":[],"checkpoints":[],"returned_outputs":[],"returned_evidence":[]});
    if required {
        value["required_tools"] = json!([{"name":"read","class":"host_operation","operation":"example.read","purpose":"Read basis","necessity":"required","stages":["Method"]}]);
    }
    if !roles.is_null() {
        value["compatible_roles"] = roles;
    }
    crate::workflow_declaration::read(&format!("```workflow-declaration\n{value}\n```\n")).unwrap()
}
fn basis() -> Basis {
    Basis {
        home: "h".into(),
        generation: json!({"home":"h","appSession":"s","spawnCounter":1}),
        conversation: "t".into(),
        acting_pin: "App Codex 0.160.0".into(),
        surface: "X".into(),
        environment_observation: None,
        catalog_edition: None,
    }
}
fn unknown() -> RoleInForce {
    RoleInForce::Unknown {
        reason: "original missing".into(),
    }
}
fn no_role() -> RoleInForce {
    RoleInForce::AppObserved {
        role: None,
        supply_ref: "original".into(),
    }
}
#[test]
fn original_negative_known_tool_failure_survives_unknown_role_declaration() {
    let d = declaration(json!("invalid"), true);
    let env = Environment {
        catalog: Some(BTreeMap::new()),
        channel_enabled: true,
        ..Default::default()
    };
    assert_eq!(
        Compatibility::check_for_role(&d, &env, None).result,
        Check::Unsupported
    );
}
#[test]
fn partial_absence_is_unknown_complete_absence_is_missing() {
    let d = declaration(Value::Null, true);
    let partial = Observations {
        catalog: CatalogCoverage::Partial(BTreeMap::new()),
        channel_enabled: Some(true),
        harness_signals: None,
    };
    assert_eq!(
        report_check(&d, &basis(), &partial, &unknown()).result,
        Check::NotEstablished
    );
    let complete = Observations {
        catalog: CatalogCoverage::Complete(BTreeMap::new()),
        ..partial
    };
    assert_eq!(
        report_check(&d, &basis(), &complete, &unknown()).result,
        Check::Unsupported
    );
}
#[test]
fn explicit_no_role_and_unknown_original_are_distinct() {
    let d = declaration(json!(["WORKING_ITEMS"]), false);
    assert_eq!(
        report_check(&d, &basis(), &Observations::default(), &no_role()).result,
        Check::Unsupported
    );
    assert_eq!(
        report_check(&d, &basis(), &Observations::default(), &unknown()).result,
        Check::NotEstablished
    );
    let actual = RoleInForce::AppObserved {
        role: Some(crate::role_supply::Role::WORKING_ITEMS),
        supply_ref: "original".into(),
    };
    assert_eq!(
        report_check(&d, &basis(), &Observations::default(), &actual).result,
        Check::Compatible
    );
}
#[test]
fn unknown_channel_is_not_disabled_and_optional_does_not_block() {
    let mut d = declaration(Value::Null, true);
    let observations = Observations {
        catalog: CatalogCoverage::Complete(BTreeMap::from([(
            "example.read".into(),
            Operation {
                version: "1".into(),
                exposure: Some(true),
                availability: Some(false),
            },
        )])),
        ..Default::default()
    };
    assert_eq!(
        report_check(&d, &basis(), &observations, &no_role()).result,
        Check::NotEstablished
    );
    d.elements.get_mut("required_tools").unwrap()[0].value["necessity"] = json!("optional");
    assert_eq!(
        report_check(&d, &basis(), &observations, &no_role()).result,
        Check::Compatible
    );
}
#[test]
fn unknown_role_does_not_erase_known_missing() {
    let d = declaration(json!(["WORKING_ITEMS"]), true);
    let observations = Observations {
        catalog: CatalogCoverage::Complete(BTreeMap::new()),
        channel_enabled: Some(true),
        harness_signals: None,
    };
    assert_eq!(
        report_check(&d, &basis(), &observations, &unknown()).result,
        Check::Unsupported
    );
}
#[test]
fn current_pin_does_not_borrow_old_presence_account() {
    let env = Environment {
        harness_pin: Some("App Codex 0.160.0".into()),
        harness_signals: Some(
            json!({"thread_start":{"approvalPolicy":"never","sandbox":"read-only"}}),
        ),
        ..Default::default()
    };
    assert_eq!(
        super::super::harness_presence("shell-command", &env).0,
        Outcome::NotEstablished
    );
}
#[test]
fn currency_is_view_only_and_not_a_start_gate_or_receipt() {
    let d = declaration(Value::Null, false);
    let b = basis();
    let report = PreparedReport {
        id: "private-test".into(),
        basis: b.clone(),
        occasion: Occasion::Selection,
        evaluated_at: "observed-time".into(),
        workflow: json!({}),
        declaration: d.clone(),
        role: no_role(),
        check: report_check(&d, &b, &Observations::default(), &no_role()),
        requirements: vec![],
    };
    let original = serde_json::to_value(&report).unwrap();
    let mut changed = b.clone();
    changed.environment_observation = Some("later".into());
    assert_eq!(report.view(&b)["notCurrent"], false);
    assert_eq!(report.view(&changed)["notCurrent"], true);
    assert_eq!(serde_json::to_value(&report).unwrap(), original);
    assert_eq!(report.view(&changed)["advisory"], true);
    assert!(report.view(&changed)["recording"]
        .as_str()
        .unwrap()
        .contains("not published"));
}
