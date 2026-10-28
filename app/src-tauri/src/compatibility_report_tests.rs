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

// ---- J2: production entry point, EXEC report publication and R14 receipt ----

const DESIGN_SCHEMA: &str = include_str!("../../../execution/PKG-02/DEL-02-03/Design/compatibility-report.schema.json");
const DESIGN_VALID: &str = include_str!("../../../execution/PKG-02/DEL-02-03/Design/compatibility-report.example.valid.json");
const DESIGN_INVALID: &str = include_str!("../../../execution/PKG-02/DEL-02-03/Design/compatibility-report.example.invalid.json");

/// Independent of the production validator: compiles the Design file's own bytes
/// through the existing declared-ID registry (no rewrite, no retrieval).
fn assert_design_valid(body: &Value) {
    let validator = crate::schema_validation::compile_targets(
        &[("compatibility-report.schema.json", DESIGN_SCHEMA)],
        &[REPORT_SCHEMA_ID],
        &[REPORT_SCHEMA_ID],
    )
    .unwrap()
    .remove(0);
    let errors: Vec<String> = validator.iter_errors(body).map(|e| e.to_string()).collect();
    assert!(errors.is_empty(), "{errors:?}\n{body:#}");
}
fn selection_of(value: Value) -> Selection {
    let text = format!("# Fixture\n\n```workflow-declaration\n{value}\n```\n");
    let snapshot = crate::workflow_workspace::Snapshot::from_files(BTreeMap::from([(
        "WORKFLOW.md".to_string(),
        text.into_bytes(),
    )]))
    .unwrap();
    let identity = snapshot
        .identity("bundled", "synthetic-bundled-root", "compat-fixture", None)
        .unwrap();
    Selection::synthetic_shipped(snapshot, identity).unwrap()
}
fn host_tool(name: &str, operation: &str, necessity: &str) -> Value {
    let mut tool = json!({"name":name,"class":"host_operation","operation":operation,"versions":["1"],"purpose":format!("use {name}"),"necessity":necessity,"stages":["Method"]});
    if necessity == "optional" {
        tool["fallback"] = json!(format!("continue without {name}"));
    }
    tool
}
fn harness_tool(name: &str, capability: &str) -> Value {
    json!({"name":name,"class":"harness_capability","capability":capability,"purpose":format!("use {name}"),"necessity":"required","stages":["Method"]})
}
fn wd(tools: Vec<Value>, roles: Value, checkpoints: Vec<Value>) -> Value {
    let mut value = json!({"declaration_contract_version":"WD-v0.8","required_tools":tools,"checkpoints":checkpoints,"returned_outputs":[],"returned_evidence":[]});
    if !roles.is_null() {
        value["compatible_roles"] = roles;
    }
    value
}
fn op(version: &str, exposure: Option<bool>, availability: Option<bool>) -> Operation {
    Operation {
        version: version.into(),
        exposure,
        availability,
    }
}
fn full_basis(edition: &str) -> Basis {
    Basis {
        environment_observation: Some("observation:1".into()),
        catalog_edition: Some(edition.into()),
        ..basis()
    }
}
fn inventory(catalog: CatalogCoverage, channel: Option<bool>) -> Inventory {
    Inventory {
        origin: InventoryOrigin::CallerSupplied {
            source: "test-supplied explicit facts".into(),
        },
        host_id: Some("synthetic host".into()),
        observations: Observations {
            catalog,
            channel_enabled: channel,
            harness_signals: None,
        },
    }
}
fn role(name: crate::role_supply::Role) -> RoleInForce {
    RoleInForce::AppObserved {
        role: Some(name),
        supply_ref: "original".into(),
    }
}
fn request<'a>(
    selection: &'a Selection,
    role: RoleInForce,
    basis: Basis,
    occasion: Occasion,
    inventory: Inventory,
) -> Request<'a> {
    Request {
        selection,
        holding_library: Some("synthetic-holding".into()),
        role,
        basis,
        occasion,
        evaluated_at: "2026-10-07T00:00:00Z".into(),
        inventory,
        model_destination: Some(ModelDestination {
            selected: "skeleton-no-model".into(),
            class: DestinationClass::Local,
        }),
    }
}
fn published(evaluation: &Evaluation) -> &PublishedReport {
    evaluation
        .published
        .as_ref()
        .unwrap_or_else(|refusal| panic!("publication refused: {refusal:?}"))
}
fn refusal(evaluation: &Evaluation) -> String {
    match &evaluation.published {
        Ok(report) => panic!("published without required facts: {:#}", report.body()),
        Err(reasons) => reasons.join("; "),
    }
}
fn checkpoint() -> Value {
    json!({"name":"cp-read","required_act":"A4","reached_when":{"kind":"before_dispatch","tool":"read"},"subject":{"class":"targets_of_held_call"},"position":"before read","scope":"read targets","purpose":"check before reading","actor":"the_person","expected_act_evidence":{"capturing_surface":"app_act_control","description":"A4 capture"}})
}

#[test]
fn j2_ck1_passes_with_complete_schema_valid_report() {
    let selection = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        json!(["WORKING_ITEMS"]),
        vec![checkpoint()],
    ));
    let catalog = CatalogCoverage::Complete(BTreeMap::from([(
        "example.read".into(),
        op("1", Some(true), None),
    )]));
    let evaluation = evaluate(request(
        &selection,
        role(crate::role_supply::Role::WORKING_ITEMS),
        full_basis("e1"),
        Occasion::Selection,
        inventory(catalog, Some(true)),
    ))
    .unwrap();
    assert_eq!(evaluation.prepared.result(), &Check::Compatible);
    let body = published(&evaluation).body();
    assert_design_valid(body);
    assert_eq!(body["check_result"], "passes");
    assert_eq!(body["phase"], "current");
    assert_eq!(body["occasion"]["occasion"], "CK-1");
    assert_eq!(
        body["host"],
        json!({"host_id":"synthetic host","catalog_edition":"e1","catalog_readable":true})
    );
    assert_eq!(
        body["surface"],
        json!({"surface":"X","channel_state":"enabled"})
    );
    assert_eq!(body["workflow"]["holding_library"], "synthetic-holding");
    assert_eq!(
        body["workflow"]["identity"]["revision"],
        selection.identity().revision
    );
    assert!(body["workflow"]["identity"]
        .get("revision_method")
        .is_none());
    assert_eq!(
        body["requirements"][0]["entry"],
        json!({"operation_id":"example.read","version":"1"})
    );
    assert_eq!(body["requirements"][0]["exposure"], "exposed");
    assert_eq!(body["requirements"][0]["outcome"], "present");
    assert_eq!(
        body["checkpoints"],
        json!([{"name":"cp-read","required_act":"A4","reached_when_kind":"a","subject_class":"targets of the held call","held_actions":"absent_derived","governed":false,"declaration_status":"valid","phase_reading":"guidance"}])
    );
    assert_eq!(body["evidence_standing"], "illustrative");
    assert_eq!(
        body["model_destination"],
        json!({"selected":"skeleton-no-model","class":"local","information_only":true})
    );
    let limits = body["limitations"].to_string();
    assert!(limits.contains("supplied explicitly by test-supplied explicit facts"));
    assert!(limits.contains("equality only"));
    assert!(limits.contains(crate::workflow_workspace::SNAPSHOT_METHOD));
    // The preparation identity is never the published report identity.
    assert_ne!(
        published(&evaluation).id(),
        evaluation.prepared.view(&full_basis("e1"))["preparation"]["id"]
    );
}

#[test]
fn j2_ck2_known_missing_does_not_pass_and_stays_advisory() {
    let selection = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        Value::Null,
        vec![],
    ));
    let evaluation = evaluate(request(
        &selection,
        no_role(),
        full_basis("e1"),
        Occasion::BeforeFirstAction,
        inventory(CatalogCoverage::Complete(BTreeMap::new()), Some(true)),
    ))
    .expect("a nonpass check is still a report, never a refusal to start");
    let body = published(&evaluation).body();
    assert_design_valid(body);
    assert_eq!(body["check_result"], "does_not_pass");
    assert_eq!(body["occasion"]["occasion"], "CK-2");
    assert_eq!(body["requirements"][0]["outcome"], "missing");
    assert_eq!(body["requirements"][0]["entry"], Value::Null);
    assert_eq!(body["requirements"][0]["exposure"], "not_read");
    let view = evaluation.view(&full_basis("e1"));
    assert_eq!(view["advisory"], true);
    assert_eq!(view["occasion"], "CK-2");
    assert!(view["statement"]
        .as_str()
        .unwrap()
        .contains("may still start"));
    assert_eq!(view["inventoryOrigin"]["kind"], "caller-supplied");
}

#[test]
fn j2_ck3_edition_change_is_a_new_report_and_earlier_is_not_current() {
    let selection = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        Value::Null,
        vec![],
    ));
    let complete = || {
        CatalogCoverage::Complete(BTreeMap::from([(
            "example.read".into(),
            op("1", Some(true), None),
        )]))
    };
    let earlier = evaluate(request(
        &selection,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(complete(), Some(true)),
    ))
    .unwrap();
    let earlier_body = published(&earlier).body().clone();
    let change = Occasion::EditionChange {
        earlier_report: published(&earlier).id().into(),
        earlier_edition: "e1".into(),
    };
    let later = evaluate(request(
        &selection,
        no_role(),
        full_basis("e2"),
        change,
        inventory(CatalogCoverage::Partial(BTreeMap::new()), Some(true)),
    ))
    .unwrap();
    let body = published(&later).body();
    assert_design_valid(body);
    assert_eq!(body["occasion"]["occasion"], "CK-3");
    assert_eq!(body["check_result"], "not_established");
    assert_eq!(body["host"]["catalog_edition"], "e2");
    assert_ne!(published(&later).id(), published(&earlier).id());
    assert_eq!(earlier.view(&full_basis("e2"))["notCurrent"], true);
    assert_eq!(earlier.view(&full_basis("e1"))["notCurrent"], false);
    assert_eq!(
        published(&earlier).body(),
        &earlier_body,
        "earlier report never rewritten"
    );
    // CK-3 needs an actual new edition; an unchanged or unknown edition is not one.
    for basis in [
        full_basis("e1"),
        Basis {
            catalog_edition: None,
            ..full_basis("e1")
        },
    ] {
        let unchanged = Occasion::EditionChange {
            earlier_report: published(&earlier).id().into(),
            earlier_edition: "e1".into(),
        };
        assert!(evaluate(request(
            &selection,
            no_role(),
            basis,
            unchanged,
            inventory(complete(), Some(true)),
        ))
        .is_err());
    }
}

#[test]
fn j2_published_rows_cover_each_requirement_outcome() {
    let names = ["a", "b", "c", "d", "e", "f"];
    let tools = names
        .iter()
        .map(|n| host_tool(n, &format!("op.{n}"), "required"))
        .collect();
    let selection = selection_of(wd(tools, Value::Null, vec![]));
    let catalog = CatalogCoverage::Complete(BTreeMap::from([
        ("op.a".into(), op("1", Some(true), Some(true))),
        ("op.c".into(), op("2", Some(true), None)),
        ("op.d".into(), op("1", Some(false), None)),
        ("op.e".into(), op("1", None, None)),
        ("op.f".into(), op("1", Some(true), Some(false))),
    ]));
    let evaluation = evaluate(request(
        &selection,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(catalog, Some(true)),
    ))
    .unwrap();
    let body = published(&evaluation).body();
    assert_design_valid(body);
    let outcomes: Vec<&str> = body["requirements"]
        .as_array()
        .unwrap()
        .iter()
        .map(|r| r["outcome"].as_str().unwrap())
        .collect();
    assert_eq!(
        outcomes,
        [
            "present",
            "missing",
            "version_mismatch",
            "not_exposed_on_this_surface",
            "not_established",
            "present_currently_unavailable"
        ]
    );
    assert_eq!(body["check_result"], "does_not_pass");
    let rows = &body["requirements"];
    assert_eq!(rows[0]["availability"]["result"], "available");
    assert_eq!(rows[0]["availability"]["evaluated_basis"], "observation:1");
    assert_eq!(rows[2]["entry"]["version"], "2");
    assert_eq!(rows[2]["declared_versions"], json!(["1"]));
    assert_eq!(rows[3]["exposure"], "not_exposed_on_this_surface");
    assert_eq!(rows[4]["exposure"], "unagreed");
    assert_eq!(rows[5]["availability"]["result"], "unavailable");
    assert_eq!(
        body["runtime_holds"],
        json!([{"reference":"f","reason":rows[5]["reason"],"evaluated_basis":"observation:1"}])
    );
    // Channel known not enabled is reported per row as channel_not_enabled, never missing.
    let selection = selection_of(wd(
        vec![host_tool("a", "op.a", "required")],
        Value::Null,
        vec![],
    ));
    let disabled = evaluate(request(
        &selection,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(
            CatalogCoverage::Complete(BTreeMap::from([("op.a".into(), op("1", Some(true), None))])),
            Some(false),
        ),
    ))
    .unwrap();
    let body = published(&disabled).body();
    assert_design_valid(body);
    assert_eq!(body["surface"]["channel_state"], "not_enabled");
    assert_eq!(body["requirements"][0]["outcome"], "channel_not_enabled");
    assert_eq!(body["check_result"], "does_not_pass");
}

#[test]
fn j2_unknown_inventory_is_never_missing() {
    let selection = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        Value::Null,
        vec![],
    ));
    let run = |catalog| {
        evaluate(request(
            &selection,
            no_role(),
            full_basis("e1"),
            Occasion::Selection,
            inventory(catalog, Some(true)),
        ))
        .unwrap()
    };
    // Not observed: the preparation says not established; no report claims readability.
    let unobserved = run(CatalogCoverage::Unobserved);
    assert_eq!(unobserved.prepared.result(), &Check::NotEstablished);
    assert!(refusal(&unobserved).contains("catalog not observed"));
    // Partial: omission is not established, never missing.
    let partial = run(CatalogCoverage::Partial(BTreeMap::new()));
    let body = published(&partial).body();
    assert_design_valid(body);
    assert_eq!(body["requirements"][0]["outcome"], "not_established");
    assert_eq!(body["check_result"], "not_established");
    assert!(body["limitations"].to_string().contains("partial"));
    // Attempted and unreadable: catalog_readable false, reference not established.
    let unreadable = run(CatalogCoverage::Unreadable);
    let body = published(&unreadable).body();
    assert_design_valid(body);
    assert_eq!(body["host"]["catalog_readable"], false);
    assert_eq!(body["requirements"][0]["outcome"], "not_established");
    assert_eq!(body["check_result"], "not_established");
}

#[test]
fn j2_known_no_role_is_not_unknown_in_published_report() {
    let selection = selection_of(wd(vec![], json!(["WORKING_ITEMS"]), vec![]));
    let run = |role_in_force| {
        evaluate(request(
            &selection,
            role_in_force,
            full_basis("e1"),
            Occasion::Selection,
            inventory(CatalogCoverage::Complete(BTreeMap::new()), Some(true)),
        ))
        .unwrap()
    };
    let none = run(no_role());
    let body = published(&none).body();
    assert_design_valid(body);
    assert_eq!(body["declared_part_status"], "declared_empty");
    assert_eq!(body["check_result"], "does_not_pass");
    assert_eq!(
        body["workflow_unsupported"],
        json!([{"reason_kind":"role","checkpoints":[]}])
    );
    assert!(body["limitations"].to_string().contains("no role in force"));
    let unknown_role = run(unknown());
    let body = published(&unknown_role).body();
    assert_design_valid(body);
    assert_eq!(body["check_result"], "not_established");
    assert_eq!(body["workflow_unsupported"], json!([]));
    assert!(body["limitations"]
        .to_string()
        .contains("role in force not established"));
    let matching = run(role(crate::role_supply::Role::WORKING_ITEMS));
    assert_eq!(published(&matching).body()["check_result"], "passes");
    // Known TASK with required delegation: the delegation reason, stated not enforced.
    let delegating = selection_of(wd(
        vec![harness_tool("delegate", "agent-delegation")],
        Value::Null,
        vec![],
    ));
    let task = evaluate(request(
        &delegating,
        role(crate::role_supply::Role::TASK),
        full_basis("e1"),
        Occasion::Selection,
        inventory(CatalogCoverage::Complete(BTreeMap::new()), Some(true)),
    ))
    .unwrap();
    let body = published(&task).body();
    assert_design_valid(body);
    assert_eq!(body["check_result"], "does_not_pass");
    assert_eq!(
        body["workflow_unsupported"],
        json!([{"reason_kind":"delegation","checkpoints":[]}])
    );
}

#[test]
fn j2_current_pin_does_not_borrow_0158_account_in_published_report() {
    let selection = selection_of(wd(
        vec![harness_tool("draw", "image-generation")],
        Value::Null,
        vec![],
    ));
    let signals = json!({"provider_capabilities":{"imageGeneration":false}});
    let run = |pin: &str| {
        let mut inv = inventory(CatalogCoverage::Complete(BTreeMap::new()), Some(true));
        inv.observations.harness_signals = Some(signals.clone());
        evaluate(request(
            &selection,
            no_role(),
            Basis {
                acting_pin: pin.into(),
                ..full_basis("e1")
            },
            Occasion::Selection,
            inv,
        ))
        .unwrap()
    };
    // Sanity: under the adopted 0.158.0 account this signal reads missing.
    assert_eq!(
        run("App Codex 0.158.0").prepared.result(),
        &Check::Unsupported
    );
    let current = run("App Codex 0.160.0");
    assert_eq!(current.prepared.result(), &Check::NotEstablished);
    let body = published(&current).body();
    assert_design_valid(body);
    assert_eq!(body["requirements"][0]["outcome"], "not_established");
    assert!(body["requirements"][0]["reason"]
        .as_str()
        .unwrap()
        .contains("no adopted supplier availability account"));
    assert_eq!(body["check_result"], "not_established");
    assert!(body["limitations"]
        .to_string()
        .contains("App Codex 0.160.0"));
}

#[test]
fn j2_publication_refused_without_required_supplied_facts() {
    let selection = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        Value::Null,
        vec![],
    ));
    let complete = || {
        CatalogCoverage::Complete(BTreeMap::from([(
            "example.read".into(),
            op("1", Some(true), None),
        )]))
    };
    let base = || {
        request(
            &selection,
            no_role(),
            full_basis("e1"),
            Occasion::Selection,
            inventory(complete(), Some(true)),
        )
    };
    assert!(evaluate(base()).unwrap().published.is_ok());
    let mut cases: Vec<(Request, &str)> = vec![];
    let mut r = base();
    r.inventory.host_id = None;
    cases.push((r, "host identity"));
    let mut r = base();
    r.basis.catalog_edition = None;
    cases.push((r, "catalog edition"));
    let mut r = base();
    r.inventory.observations.channel_enabled = None;
    cases.push((r, "channel state"));
    let mut r = base();
    r.holding_library = None;
    cases.push((r, "holding library"));
    let mut r = base();
    r.basis.environment_observation = None;
    cases.push((r, "environment observation"));
    let mut r = base();
    r.basis.surface = "App".into();
    cases.push((r, "acting surface"));
    let mut r = base();
    r.inventory.observations.catalog = CatalogCoverage::Unobserved;
    cases.push((r, "catalog not observed"));
    for (req, expected) in cases {
        let evaluation = evaluate(req).expect("advisory preparation still produced");
        let reason = refusal(&evaluation);
        assert!(reason.contains(expected), "{expected}: {reason}");
        assert_eq!(evaluation.view(&full_basis("e1"))["advisory"], true);
    }
    // An element the report cannot represent is refused, never dropped or guessed.
    let bogus = selection_of(wd(
        vec![
            json!({"name":"odd","class":"bogus","purpose":"p","necessity":"required","stages":["Method"]}),
        ],
        Value::Null,
        vec![],
    ));
    let evaluation = evaluate(request(
        &bogus,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(complete(), Some(true)),
    ))
    .unwrap();
    assert_eq!(evaluation.prepared.result(), &Check::NotEstablished);
    assert!(refusal(&evaluation).contains("not representable"));
    // An invalid checkpoint (A3 is not a checkpoint act, FB-03) cannot be listed
    // in CR-9 rows; publication is refused, and in Phase 1 it does not change
    // the check result (PH-3).
    let mut bad = checkpoint();
    bad["required_act"] = json!("A3");
    let invalid_checkpoint = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        Value::Null,
        vec![bad],
    ));
    let evaluation = evaluate(request(
        &invalid_checkpoint,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(complete(), Some(true)),
    ))
    .unwrap();
    assert_eq!(evaluation.prepared.result(), &Check::Compatible);
    assert!(refusal(&evaluation).contains("checkpoint element 0 not representable"));
}

#[test]
fn j2_r14_receipt_only_from_published_report_with_checked_resolution() {
    let rs = crate::schema_validation::compile_targets(
        crate::schema_validation::RESOURCES,
        &[crate::schema_validation::RS_ID],
        &["urn:chirality:app-v4:del-04-03:rs-record:0.1#/$defs/compatibilityReportRef"],
    )
    .unwrap()
    .remove(0);
    let selection = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        Value::Null,
        vec![],
    ));
    let run = |catalog| {
        evaluate(request(
            &selection,
            no_role(),
            full_basis("e1"),
            Occasion::BeforeFirstAction,
            inventory(catalog, Some(true)),
        ))
        .unwrap()
    };
    let pass = run(CatalogCoverage::Complete(BTreeMap::from([(
        "example.read".into(),
        op("1", Some(true), None),
    )])));
    let report = published(&pass);
    let unstored = report.r14_body(None).unwrap();
    assert_eq!(
        unstored,
        json!({"report":{"kind":"compatibility report","ref":report.id(),"resolutionAtWrite":"not supplied"},"occasion":"CK-2 run start","passResult":"pass"})
    );
    assert!(rs.validate(&unstored).is_ok());
    let stored = serde_json::to_vec(report.body()).unwrap();
    let resolved = report.r14_body(Some(&stored)).unwrap();
    assert_eq!(resolved["report"]["resolutionAtWrite"], "resolved");
    assert!(rs.validate(&resolved).is_ok());
    let mut tampered: Value = serde_json::from_slice(&stored).unwrap();
    tampered["check_result"] = json!("does_not_pass");
    assert!(report
        .r14_body(Some(&serde_json::to_vec(&tampered).unwrap()))
        .is_err());
    assert!(report.r14_body(Some(b"not json")).is_err());
    let missing = run(CatalogCoverage::Complete(BTreeMap::new()));
    assert_eq!(
        published(&missing).r14_body(None).unwrap()["passResult"],
        "does not pass"
    );
    let partial = run(CatalogCoverage::Partial(BTreeMap::new()));
    let body = published(&partial).r14_body(None).unwrap();
    assert_eq!(body["passResult"], "not established");
    assert!(rs.validate(&body).is_ok());
}

#[test]
fn j2_unrecognized_optional_required_tool_element_is_never_a_pass() {
    // WD §3.4: an unrecognized element in the required-tool category makes the
    // required-tool result not established, never a pass, whatever its necessity.
    let mut tool = host_tool("extra", "example.extra", "optional");
    tool.as_object_mut().unwrap().remove("fallback");
    let d = crate::workflow_declaration::read(&format!(
        "```workflow-declaration\n{}\n```\n",
        wd(
            vec![host_tool("read", "example.read", "required"), tool],
            Value::Null,
            vec![]
        )
    ))
    .unwrap();
    assert_ne!(d.elements["required_tools"][1].reading, Reading::Recognized);
    let observations = Observations {
        catalog: CatalogCoverage::Complete(BTreeMap::from([
            ("example.read".into(), op("1", Some(true), None)),
            ("example.extra".into(), op("1", Some(true), None)),
        ])),
        channel_enabled: Some(true),
        harness_signals: None,
    };
    assert_eq!(
        report_check(&d, &basis(), &observations, &no_role()).result,
        Check::NotEstablished
    );
}

#[test]
fn j2_inventory_origin_sets_standing_and_never_claims_actual_host() {
    let selection = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        Value::Null,
        vec![],
    ));
    let mut inv = inventory(
        CatalogCoverage::Complete(BTreeMap::from([(
            "example.read".into(),
            op("1", Some(true), None),
        )])),
        Some(true),
    );
    inv.origin = InventoryOrigin::TestDouble {
        fixture: "FX-J2".into(),
    };
    let mut req = request(
        &selection,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inv,
    );
    req.model_destination = Some(ModelDestination {
        selected: "remote-model".into(),
        class: DestinationClass::Cloud,
    });
    let evaluation = evaluate(req).unwrap();
    let body = published(&evaluation).body();
    assert_design_valid(body);
    assert_eq!(body["evidence_standing"], "test_double");
    assert!(body["limitations"]
        .to_string()
        .contains("evaluated on a test double (FX-J2)"));
    assert_eq!(body["model_destination"]["class"], "cloud");
    // Destination is information only: the same facts with an unknown destination
    // give the same check result.
    let mut req = request(
        &selection,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(
            CatalogCoverage::Complete(BTreeMap::from([(
                "example.read".into(),
                op("1", Some(true), None),
            )])),
            Some(true),
        ),
    );
    req.model_destination = Some(ModelDestination {
        selected: "unstated".into(),
        class: DestinationClass::Unknown,
    });
    let other = evaluate(req).unwrap();
    assert_eq!(
        published(&other).body()["check_result"],
        body["check_result"]
    );
    assert_ne!(published(&other).body()["evidence_standing"], "actual_host");
}

// ---- V8 repairs (F-1…F-4) ----

fn publish_wd(value: Value, catalog: CatalogCoverage) -> Evaluation {
    let selection = selection_of(value);
    evaluate(request(
        &selection,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(catalog, Some(true)),
    ))
    .unwrap()
}
fn read_ok() -> CatalogCoverage {
    CatalogCoverage::Complete(BTreeMap::from([(
        "example.read".into(),
        op("1", Some(true), None),
    )]))
}

#[test]
fn v8_f1_runtime_holds_list_required_references_only() {
    let evaluation = publish_wd(
        wd(
            vec![
                host_tool("need", "op.need", "required"),
                host_tool("nice", "op.nice", "optional"),
            ],
            Value::Null,
            vec![],
        ),
        CatalogCoverage::Complete(BTreeMap::from([
            ("op.need".into(), op("1", Some(true), Some(false))),
            ("op.nice".into(), op("1", Some(true), Some(false))),
        ])),
    );
    let body = published(&evaluation).body();
    assert_design_valid(body);
    assert_eq!(
        body["requirements"][1]["outcome"],
        "present_currently_unavailable"
    );
    let holds: Vec<&str> = body["runtime_holds"]
        .as_array()
        .unwrap()
        .iter()
        .map(|h| h["reference"].as_str().unwrap())
        .collect();
    assert_eq!(holds, ["need"], "CR-11: required references only");
}

#[test]
fn v8_f2_duplicate_key_stored_bytes_never_resolve() {
    let evaluation = publish_wd(
        wd(
            vec![host_tool("read", "example.read", "required")],
            Value::Null,
            vec![],
        ),
        read_ok(),
    );
    let report = published(&evaluation);
    assert_eq!(report.body()["check_result"], "passes");
    let text = serde_json::to_string(report.body()).unwrap();
    // A duplicate key placed before and after the real one: a last-wins reader
    // would see this report, whichever copy it keeps.
    let first = format!("{{\"check_result\":\"does_not_pass\",{}", &text[1..]);
    let last = format!(
        "{},\"check_result\":\"does_not_pass\"}}",
        &text[..text.len() - 1]
    );
    for tampered in [first, last] {
        assert!(report.r14_body(Some(tampered.as_bytes())).is_err());
    }
    assert_eq!(
        report.r14_body(Some(text.as_bytes())).unwrap()["report"]["resolutionAtWrite"],
        "resolved"
    );
}

#[test]
fn v8_f3_unrecognized_governed_value_refuses_publication() {
    let mut cp = checkpoint();
    cp["governed"] = json!("no");
    let evaluation = publish_wd(
        wd(
            vec![host_tool("read", "example.read", "required")],
            Value::Null,
            vec![cp],
        ),
        read_ok(),
    );
    // Phase 1: the checkpoint does not change the check (PH-3).
    assert_eq!(evaluation.prepared.result(), &Check::Compatible);
    let reason = refusal(&evaluation);
    assert!(reason.contains("checkpoint element 0 not representable"));
    assert!(reason.contains("governed"), "{reason}");
    // The recognized value is still published as declared.
    let mut cp = checkpoint();
    cp["governed"] = json!("yes");
    let evaluation = publish_wd(
        wd(
            vec![host_tool("read", "example.read", "required")],
            Value::Null,
            vec![cp],
        ),
        read_ok(),
    );
    assert_eq!(
        published(&evaluation).body()["checkpoints"][0]["governed"],
        true
    );
}

#[test]
fn v8_f4_declared_part_status_values() {
    let status = |evaluation: &Evaluation| {
        let body = published(evaluation).body().clone();
        assert_design_valid(&body);
        (
            body["declared_part_status"].as_str().unwrap().to_owned(),
            body["check_result"].as_str().unwrap().to_owned(),
        )
    };
    let declared = publish_wd(
        wd(
            vec![host_tool("read", "example.read", "required")],
            Value::Null,
            vec![],
        ),
        read_ok(),
    );
    assert_eq!(status(&declared), ("declared".into(), "passes".into()));
    // No declared part at all (PS-4).
    let snapshot = crate::workflow_workspace::Snapshot::from_files(BTreeMap::from([(
        "WORKFLOW.md".to_string(),
        b"# Prose only\n".to_vec(),
    )]))
    .unwrap();
    let identity = snapshot
        .identity("bundled", "synthetic-bundled-root", "prose-only", None)
        .unwrap();
    let prose = Selection::synthetic_shipped(snapshot, identity).unwrap();
    let undeclared = evaluate(request(
        &prose,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(read_ok(), Some(true)),
    ))
    .unwrap();
    assert_eq!(
        status(&undeclared),
        ("undeclared".into(), "not_established".into())
    );
    assert!(published(&undeclared).body()["limitations"]
        .to_string()
        .contains("requirements undeclared"));
    // Declared part present, required-tool category omitted.
    let mut omitted = wd(vec![], Value::Null, vec![]);
    omitted.as_object_mut().unwrap().remove("required_tools");
    assert_eq!(
        status(&publish_wd(omitted, read_ok())),
        ("undeclared".into(), "not_established".into())
    );
    // Category present but not an array.
    let mut malformed = wd(vec![], Value::Null, vec![]);
    malformed["required_tools"] = json!("none");
    assert_eq!(
        status(&publish_wd(malformed, read_ok())),
        ("not_established".into(), "not_established".into())
    );
    // Newer contract version: the whole declared part is not established.
    let mut newer = wd(vec![], Value::Null, vec![]);
    newer["declaration_contract_version"] = json!("WD-v0.9");
    assert_eq!(
        status(&publish_wd(newer, read_ok())),
        ("not_established".into(), "not_established".into())
    );
    // A representable but unrecognized element (optional without its fallback).
    let mut tool = host_tool("extra", "example.read", "optional");
    tool.as_object_mut().unwrap().remove("fallback");
    assert_eq!(
        status(&publish_wd(wd(vec![tool], Value::Null, vec![]), read_ok())),
        ("not_established".into(), "not_established".into())
    );
}

#[test]
fn v8_f4_partial_catalog_is_readable_and_fallback_is_in_purpose() {
    let evaluation = publish_wd(
        wd(
            vec![host_tool("nice", "example.read", "optional")],
            Value::Null,
            vec![],
        ),
        CatalogCoverage::Partial(BTreeMap::from([(
            "example.read".into(),
            op("1", Some(true), None),
        )])),
    );
    let body = published(&evaluation).body();
    assert_design_valid(body);
    assert_eq!(body["host"]["catalog_readable"], true);
    assert_eq!(
        body["requirements"][0]["purpose"],
        "use nice (fallback: continue without nice)"
    );
}

#[test]
fn v8_f4_checkpoint_declaration_status_other_than_valid() {
    // FB-13: before_dispatch naming no usable required tool -> invalid.
    let mut invalid = checkpoint();
    invalid["reached_when"]["tool"] = json!("absent");
    // A schema-required field missing -> not established, still representable.
    let mut unestablished = checkpoint();
    unestablished["name"] = json!("cp-two");
    unestablished.as_object_mut().unwrap().remove("position");
    let evaluation = publish_wd(
        wd(
            vec![host_tool("read", "example.read", "required")],
            Value::Null,
            vec![invalid, unestablished],
        ),
        read_ok(),
    );
    let body = published(&evaluation).body();
    assert_design_valid(body);
    assert_eq!(body["checkpoints"][0]["declaration_status"], "invalid");
    assert_eq!(
        body["checkpoints"][1]["declaration_status"],
        "not_established"
    );
    // PH-3: invalid checkpoints leave the Phase-1 check unchanged.
    assert_eq!(body["check_result"], "passes");
}

#[test]
fn v8_f4_ck3_requires_earlier_report_and_known_earlier_edition() {
    let selection = selection_of(wd(
        vec![host_tool("read", "example.read", "required")],
        Value::Null,
        vec![],
    ));
    let run = |earlier_report: &str, earlier_edition: &str| {
        evaluate(request(
            &selection,
            no_role(),
            full_basis("e2"),
            Occasion::EditionChange {
                earlier_report: earlier_report.into(),
                earlier_edition: earlier_edition.into(),
            },
            inventory(read_ok(), Some(true)),
        ))
    };
    assert!(run("compatibility-report:earlier", "e1").is_ok());
    // An unpublished earlier evaluation is named by its preparation id.
    let unpublished = evaluate(request(
        &selection,
        no_role(),
        full_basis("e1"),
        Occasion::Selection,
        inventory(CatalogCoverage::Unobserved, Some(true)),
    ))
    .unwrap();
    assert!(unpublished.published.is_err());
    assert!(run(unpublished.prepared.id(), "e1").is_ok());
    assert!(run("", "e1").is_err(), "empty earlier report");
    assert!(
        run("compatibility-report:earlier", "").is_err(),
        "unknown earlier edition"
    );
}

#[test]
fn j2_embedded_schema_is_design_bytes_and_design_examples_classify() {
    assert_eq!(REPORT_SCHEMA, DESIGN_SCHEMA);
    let valid: Value = serde_json::from_str(DESIGN_VALID).unwrap();
    let invalid: Value = serde_json::from_str(DESIGN_INVALID).unwrap();
    assert!(validate_report(&valid).is_ok());
    assert!(validate_report(&invalid).is_err());
    assert_design_valid(&valid);
}
