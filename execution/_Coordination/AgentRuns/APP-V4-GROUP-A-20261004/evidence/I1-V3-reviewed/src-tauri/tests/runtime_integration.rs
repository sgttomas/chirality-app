//! Synthetic producer→consumer checks. No supplier, native UI or model is launched.
use chirality_app_v4_lib::{
    native_requests::RequestRegister,
    recovery::RecoveryLedger,
    role_supply::{Composition, Guidance, Role},
    runtime_session::{actor_reference, answer_preview, reviewed_ledger_path, RuntimeSession},
};
use serde_json::{json, Value};
fn g(home: &str, counter: u64) -> Value {
    json!({"appSession":"synthetic-session","home":home,"spawnCounter":counter})
}
fn envelope(g: &Value, pos: u64, method: &str, params: Value) -> Value {
    json!({"generation":g,"position":pos,"class":"notification","frame":{"method":method,"params":params}})
}
fn observation(g: &Value, state: &str, frames: Vec<Value>, requests: Vec<Value>) -> Value {
    json!({"generation":g,"gap":false,"frames":frames,"snapshot":{"generation":g,"state":state,"serverRequests":requests,"clientRequests":[],"versionIdentity":"synthetic pin","supplierStanding":"synthetic"}})
}
fn register(g: &Value) -> RequestRegister {
    let mut r = RequestRegister::default();
    r.receive(g,2,&json!({"id":"r","method":"item/fileChange/requestApproval","params":{"threadId":"t","turnId":"u","itemId":"i","availableDecisions":["accept","decline"]}}),&json!({})).unwrap();
    r
}
#[test]
fn receiving_request_tool_answer_ack_and_explicit_scratch_ledger_are_connected() {
    let generation = g("home:a", 1);
    let mut r = register(&generation);
    let mut session = RuntimeSession::default();
    let frames = vec![envelope(
        &generation,
        1,
        "item/started",
        json!({"threadId":"t","turnId":"u","item":{"id":"i","type":"fileChange","status":"inProgress","changes":[],"nativeUnknown":42}}),
    )];
    let o = observation(&generation, "ready", frames, r.records());
    let before = session.receive(&o);
    assert_eq!(
        before["nativeView"]["items"][0]["displayState"],
        "waiting-on-request"
    );
    assert_eq!(
        before["nativeView"]["items"][0]["native"]["nativeUnknown"],
        42
    );
    let actor = actor_reference(Some("Synthetic"), Some("scratch-user"), None);
    let answer = json!({"decision":"decline"});
    answer_preview(&o["snapshot"], &generation, &json!("r"), &answer, &actor).unwrap();
    let root = std::env::temp_dir().join(format!(
        "i1-integration-{}",
        chirality_app_v4_lib::util::opaque_id("scratch-").unwrap()
    ));
    std::fs::create_dir_all(&root).unwrap();
    let path = reviewed_ledger_path(&root);
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
    ledger
        .start_session("synthetic-session", "synthetic-test")
        .unwrap();
    ledger.request_summary(&r.entries()[0]).unwrap();
    assert_eq!(
        r.prepare(
            &generation,
            &json!("r"),
            &answer,
            "person-via-interaction",
            Some(&actor)
        )
        .unwrap()["result"],
        answer
    );
    r.written(&generation, &json!("r"), true);
    ledger.request_summary(&r.entries()[0]).unwrap();
    assert_eq!(
        r.records()[0]["acknowledgmentObservation"]["status"],
        "not-observed"
    );
    let answered = session.receive(&observation(&generation, "ready", vec![], r.records()));
    assert_ne!(
        answered["nativeView"]["items"][0]["displayState"],
        "waiting-on-request"
    );
    r.resolved(&generation, &json!({"threadId":"t","requestId":"r"}));
    ledger.request_summary(&r.entries()[0]).unwrap();
    assert_eq!(
        r.records()[0]["acknowledgmentObservation"]["status"],
        "observed"
    );
    let disk = std::fs::read_to_string(path).unwrap();
    assert!(!disk.contains("nativeUnknown"));
    assert!(!disk.contains("availableDecisions"));
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn repeated_observer_and_full_home_transition_never_mix_items_or_account() {
    let a = g("a", 1);
    let b = g("b", 1);
    let mut session = RuntimeSession::default();
    // Starting/handshaking state does not prematurely close a generation.
    session.receive(&observation(&a, "starting", vec![], vec![]));
    let update = envelope(
        &a,
        1,
        "turn/plan/updated",
        json!({"threadId":"t","turnId":"u","plan":[{"step":"synthetic","status":"inProgress"}]}),
    );
    let o = observation(&a, "ready", vec![update], vec![]);
    let first = session.receive(&o);
    let repeated = session.receive(&o);
    assert_eq!(
        first["nativeView"]["revisions"],
        repeated["nativeView"]["revisions"]
    );
    assert_eq!(
        repeated["nativeView"]["revisions"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    let closed = session.receive(&observation(&a, "failed", vec![], vec![]));
    assert!(closed["nativeView"]["revisions"]
        .as_array()
        .unwrap()
        .is_empty());
    let mut successor = observation(
        &b,
        "ready",
        vec![envelope(&a, 2, "future/native", json!({"extra":true}))],
        vec![],
    );
    successor["gap"] = json!(true);
    let next = session.receive(&successor);
    assert_eq!(next["nativeView"]["home"], "b");
    assert_eq!(next["observerGap"], true);
    assert_eq!(session.codex_account_for(&a), None);
    assert!(next["nativeViewLimits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|v| v == "foreign observer envelope refused"));
}
#[test]
fn answer_preview_rejects_foreign_offers_privileged_origin_and_masks_secrets() {
    let generation = g("a", 1);
    let mut r = register(&generation);
    let actor = actor_reference(None, Some("scratch"), None);
    let o = observation(&generation, "ready", vec![], r.records());
    assert!(answer_preview(
        &o["snapshot"],
        &g("b", 1),
        &json!("r"),
        &json!({"decision":"accept"}),
        &actor
    )
    .is_err());
    assert!(answer_preview(
        &o["snapshot"],
        &generation,
        &json!("r"),
        &json!({"decision":"cancel"}),
        &actor
    )
    .is_err());
    assert!(answer_preview(
        &o["snapshot"],
        &generation,
        &json!("r"),
        &json!({"decision":"accept"}),
        "app-rule:automatic"
    )
    .is_err());
    r.receive(&generation,3,&json!({"id":"q","method":"item/tool/requestUserInput","params":{"questions":[{"id":"secret","isSecret":true,"isOther":true}]}}),&json!({})).unwrap();
    let secret = json!({"answers":{"secret":{"answers":["synthetic-secret"]}}});
    let o = observation(&generation, "ready", vec![], r.records());
    let preview =
        answer_preview(&o["snapshot"], &generation, &json!("q"), &secret, &actor).unwrap();
    assert!(!preview.to_string().contains("synthetic-secret"));
    r.receive(&generation, 4, &json!({"id":"form","method":"mcpServer/elicitation/request","params":{"mode":"form","requestedSchema":{"type":"object","properties":{"secret":{"type":"string"}},"required":["secret"]}}}), &json!({})).unwrap();
    let o = observation(&generation, "ready", vec![], r.records());
    let preview = answer_preview(
        &o["snapshot"],
        &generation,
        &json!("form"),
        &json!({"action":"accept","content":{"secret":"synthetic-form-secret"},"_meta":null}),
        &actor,
    )
    .unwrap();
    assert!(!preview.to_string().contains("synthetic-form-secret"));
}
#[test]
fn explicit_fixture_role_guidance_preserves_bytes_and_refuses_primary_task() {
    let common = Guidance::seeded(
        "AGENTS.md",
        "synthetic",
        b"fixture common".to_vec(),
        b"fixture common",
    )
    .unwrap();
    for role in Role::ALL {
        let path = format!("agents/AGENT_{}.md", role.name());
        let guide = Guidance::seeded(
            &path,
            "synthetic",
            b"fixture role".to_vec(),
            b"fixture role",
        )
        .unwrap();
        let c = Composition::new(&common, Some((role, &guide)), false);
        if role == Role::TASK {
            assert!(c.is_err());
        } else {
            let c = c.unwrap();
            let params = c.start_params().unwrap();
            assert!(params.get("baseInstructions").is_none());
            assert!(c.text.starts_with("fixture common"));
            assert!(c.text.ends_with("fixture role"));
            assert_eq!(c.child_status(None, false)[0]["status"], "not-supplied");
        }
    }
}

#[test]
fn account_attribution_requires_correlated_same_generation_native_result_and_is_lost_on_exit() {
    let generation = g("a", 1);
    let mut session = RuntimeSession::default();
    let frame = json!({"generation":generation,"position":1,"class":"response","frame":{"id":7,"result":{"account":{"type":"chatgpt","email":"synthetic@example.invalid","planType":"synthetic"}}}});
    let mut o = observation(&generation, "ready", vec![frame.clone()], vec![]);
    session.receive(&o);
    assert_eq!(session.codex_account_for(&generation), None);
    o["frames"][0]["position"] = json!(2);
    o["snapshot"]["clientRequests"] = json!([{"generation":g("b",1),"requestIdentity":7,"method":"account/read","outcome":"response-observed-result"}]);
    session.receive(&o);
    assert_eq!(session.codex_account_for(&generation), None);
    o["frames"][0]["position"] = json!(3);
    o["snapshot"]["clientRequests"][0]["generation"] = generation.clone();
    session.receive(&o);
    assert_eq!(
        session.codex_account_for(&generation).as_deref(),
        Some("synthetic@example.invalid")
    );
    session.receive(&observation(
        &generation,
        "ready",
        vec![envelope(
            &generation,
            4,
            "account/updated",
            json!({"authMode":null}),
        )],
        vec![],
    ));
    assert_eq!(session.codex_account_for(&generation), None);
    o["frames"][0]["position"] = json!(5);
    session.receive(&o);
    assert!(session.codex_account_for(&generation).is_some());
    session.receive(&observation(&generation, "failed", vec![], vec![]));
    assert_eq!(session.codex_account_for(&generation), None);
}

#[test]
fn partial_questions_and_form_aliases_keep_native_shapes_device_accept_is_unsupported() {
    let generation = g("a", 1);
    let actor = actor_reference(None, Some("synthetic"), None);
    let mut r = RequestRegister::default();
    r.receive(&generation,1,&json!({"id":"q","method":"item/tool/requestUserInput","params":{"questions":[{"id":"one","isOther":true},{"id":"two","isOther":true}]}}), &json!({})).unwrap();
    let o = observation(&generation, "ready", vec![], r.records());
    for answer in [
        json!({"answers":{}}),
        json!({"answers":{"one":{"answers":[""]}}}),
        json!({"answers":{"one":{"answers":[]}}}),
    ] {
        answer_preview(&o["snapshot"], &generation, &json!("q"), &answer, &actor).unwrap();
    }
    for mode in [
        "form",
        "openai/form",
        "openaiForm",
        "openai/userVerification",
    ] {
        r.receive(&generation,2,&json!({"id":mode,"method":"mcpServer/elicitation/request","params":{"mode":mode,"challenge":"synthetic-not-device-proof","requestedSchema":{"type":"object","properties":{"field":{"type":"string"}},"required":["field"]}}}),&json!({})).unwrap();
        let o = observation(&generation, "ready", vec![], r.records());
        let accepts = answer_preview(
            &o["snapshot"],
            &generation,
            &json!(mode),
            &json!({"action":"accept","content":{"field":"synthetic"},"_meta":null}),
            &actor,
        );
        if mode == "openai/userVerification" {
            assert!(accepts.unwrap_err().contains("no proof supplied"));
        } else {
            assert!(accepts.is_ok());
            assert!(answer_preview(
                &o["snapshot"],
                &generation,
                &json!(mode),
                &json!({"action":"accept","content":{},"_meta":null}),
                &actor
            )
            .is_err());
        }
        for action in ["decline", "cancel"] {
            answer_preview(
                &o["snapshot"],
                &generation,
                &json!(mode),
                &json!({"action":action,"content":null,"_meta":null}),
                &actor,
            )
            .unwrap();
        }
    }
}

#[test]
fn confirmation_context_consumes_fresh_account_change_terminal_and_successor_not_ui_poll() {
    let generation = g("a", 1);
    let mut session = RuntimeSession::default();
    let mut o = observation(
        &generation,
        "ready",
        vec![
            json!({"generation":generation,"position":1,"class":"response","frame":{"id":7,"result":{"account":{"type":"chatgpt","email":"synthetic@example.invalid"}}}}),
        ],
        vec![],
    );
    o["snapshot"]["clientRequests"] = json!([{"generation":generation,"requestIdentity":7,"method":"account/read","outcome":"response-observed-result"}]);
    let frozen = session.actor_context(&o, Some("synthetic"), Some("scratch"));
    assert_eq!(frozen["codexAccount"], "synthetic@example.invalid");
    // Without any intervening UI/status call, actor freezing itself consumes the change.
    let changed = observation(
        &generation,
        "ready",
        vec![envelope(
            &generation,
            2,
            "account/updated",
            json!({"authMode":null}),
        )],
        vec![],
    );
    let now = session.actor_context(&changed, Some("synthetic"), Some("scratch"));
    assert_ne!(frozen, now);
    assert!(now["codexAccount"].is_null());
    o["frames"][0]["position"] = json!(3);
    let reread = session.actor_context(&o, Some("synthetic"), Some("scratch"));
    assert_eq!(reread["codexAccount"], frozen["codexAccount"]);
    assert_ne!(reread, frozen);
    let terminal = session.actor_context(
        &observation(&generation, "failed", vec![], vec![]),
        Some("synthetic"),
        Some("scratch"),
    );
    assert!(terminal["codexAccount"].is_null());
    assert_ne!(terminal, reread);
    let successor = session.actor_context(
        &observation(&g("b", 1), "ready", vec![], vec![]),
        Some("synthetic"),
        Some("scratch"),
    );
    assert!(successor["codexAccount"].is_null());
    assert_ne!(successor, terminal);
}

#[test]
fn reviewed_v4_seed_entry_preserves_edits_and_old_composition_new_entry_reads_new_bytes() {
    use chirality_app_v4_lib::runtime_session::{
        compose_role, role_default, seed_instructions, COMMON_DEFAULT,
    };
    let scratch =
        std::env::temp_dir().join(chirality_app_v4_lib::util::opaque_id("i1-seed-").unwrap());
    let root = scratch.join("instructions");
    seed_instructions(&root).unwrap();
    assert_eq!(
        std::fs::read(root.join("AGENTS.md")).unwrap(),
        COMMON_DEFAULT
    );
    // Independent V0-INSTRUCTION-TRANCHE admitted source identities.
    assert_eq!(
        chirality_app_v4_lib::util::sha256_hex(COMMON_DEFAULT),
        "d9233f5af0393e045f0d50fe14b60ede6ec3558da625c1a0deec84fae07afc27"
    );
    for role in Role::ALL {
        assert_eq!(
            std::fs::read(root.join(format!("agents/AGENT_{}.md", role.name()))).unwrap(),
            role_default(role)
        );
    }
    for (role, expected) in [
        (
            Role::HELP_HUMAN,
            "11e619e41acad799b90552dda19a3d49c4d3921bcebbce7317254a58d03e04be",
        ),
        (
            Role::HELPS_HUMANS,
            "9306048b3229f63170cde5dbbb1280e048aae8aa434b1934085598bf8e649158",
        ),
        (
            Role::WORKING_ITEMS,
            "4be2e37da843353cde22bd2ed65f8756f00a865171939f1ac2c6d65adf025914",
        ),
        (
            Role::TASK,
            "aaab8c8c20b1d5c3592f04d1337b3335f82ff44428a2304614c191cce71ba3cc",
        ),
    ] {
        assert_eq!(
            chirality_app_v4_lib::util::sha256_hex(role_default(role)),
            expected
        );
    }
    let initial = compose_role(&root, Some(Role::HELP_HUMAN)).unwrap();
    assert_eq!(
        initial.carried["developerInstructions"]["parts"][0]["source"]["state"],
        "default"
    );
    let initial_params = initial.start_params().unwrap();
    let edit = [
        COMMON_DEFAULT,
        b"\nSynthetic edited guidance for a new entry.\n",
    ]
    .concat();
    std::fs::write(root.join("AGENTS.md"), &edit).unwrap();
    seed_instructions(&root).unwrap();
    assert_eq!(std::fs::read(root.join("AGENTS.md")).unwrap(), edit);
    assert_eq!(initial.start_params().unwrap(), initial_params); // active composition fixed
    let next = compose_role(&root, Some(Role::WORKING_ITEMS)).unwrap();
    assert!(next
        .text
        .contains("Synthetic edited guidance for a new entry."));
    assert_eq!(
        next.carried["developerInstructions"]["parts"][0]["source"]["state"],
        "modified"
    );
    assert_eq!(next.role, Some(Role::WORKING_ITEMS));
    assert!(compose_role(&root, Some(Role::TASK)).is_err());
    assert!(next
        .start_params()
        .unwrap()
        .get("baseInstructions")
        .is_none());
    std::fs::remove_file(root.join("AGENTS.md")).unwrap();
    assert!(seed_instructions(&root).is_err()); // known missing copy is never silently reseeded
    assert!(!root.join("AGENTS.md").exists());
    std::fs::write(root.join("AGENTS.md"), [0xff]).unwrap();
    assert!(seed_instructions(&root).is_err());
    std::fs::remove_file(root.join("AGENTS.md")).unwrap();
    #[cfg(unix)]
    {
        std::os::unix::fs::symlink(
            root.join("agents/AGENT_HELP_HUMAN.md"),
            root.join("AGENTS.md"),
        )
        .unwrap();
        assert!(seed_instructions(&root).is_err());
        std::fs::remove_file(root.join("AGENTS.md")).unwrap();
    }
    std::fs::remove_dir_all(scratch).unwrap();
}

#[test]
fn direct_ready_successor_retains_checklist_loss_scoped_to_old_full_namespace() {
    let old = g("same-home", 1);
    let successor = g("same-home", 2);
    let mut session = RuntimeSession::default();
    let first = session.receive(&observation(
        &old,
        "ready",
        vec![envelope(
            &old,
            1,
            "turn/plan/updated",
            json!({"threadId":"t","turnId":"u","plan":[{"step":"work","status":"inProgress"}]}),
        )],
        vec![],
    ));
    assert_eq!(
        first["nativeView"]["revisions"].as_array().unwrap().len(),
        1
    );
    // No intermediate failed/closed poll is available to the consumer.
    let mut next = observation(&successor, "ready", vec![], vec![]);
    next["gap"] = json!(true);
    let received = session.receive(&next);
    assert!(received["nativeView"]["revisions"]
        .as_array()
        .unwrap()
        .is_empty());
    assert_eq!(received["priorNativeViews"].as_array().unwrap().len(), 1);
    let prior = &received["priorNativeViews"][0];
    assert_eq!(prior["generation"], old);
    assert_eq!(prior["view"]["generation"], old);
    assert_eq!(prior["view"]["home"], "same-home");
    assert_eq!(prior["standing"], "observation-ended; not live custody");
    assert!(prior["view"]["revisions"].as_array().unwrap().is_empty());
    assert_eq!(prior["view"]["checklistGaps"][0]["threadId"], "t");
    assert_eq!(prior["view"]["checklistGaps"][0]["turnId"], "u");
    assert!(prior["view"]["checklistGaps"][0]["reason"]
        .as_str()
        .unwrap()
        .contains("not recoverable after restart or relaunch"));
    assert!(received["nativeViewLimits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|v| v.as_str().unwrap().contains("Prior generation")
            && v.as_str().unwrap().contains("not recoverable")));
    assert_eq!(received["observerRecovery"]["historyRebuilt"], false);
    assert_eq!(
        session.receive(&next)["priorNativeViews"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    // An old full tuple must never be reactivated as new live request/view custody.
    let stale = session.receive(&observation(&old, "ready", vec![], vec![]));
    assert!(stale["nativeView"].is_null());
    assert_eq!(stale["nativeViewObservationEnded"], true);
}

#[test]
fn admitted_unseen_terminal_completion_precedes_close_foreign_and_postclosed_frames_refuse() {
    let generation = g("a", 1);
    let mut session = RuntimeSession::default();
    let item = json!({"threadId":"t","turnId":"u","item":{"id":"i","type":"commandExecution","status":"inProgress","command":"synthetic","nativeUnknown":"start"}});
    session.receive(&observation(
        &generation,
        "ready",
        vec![envelope(&generation, 1, "item/started", item)],
        vec![],
    ));
    let completed = json!({"threadId":"t","turnId":"u","item":{"id":"i","type":"commandExecution","status":"completed","exitCode":0,"nativeUnknown":"last admitted completion"}});
    let mut terminal = observation(
        &generation,
        "failed",
        vec![envelope(&generation, 2, "item/completed", completed)],
        vec![],
    );
    terminal["gap"] = json!(true);
    let received = session.receive(&terminal);
    let row = &received["nativeView"]["items"][0];
    assert_eq!(row["displayState"], "completed");
    assert_eq!(row["native"]["nativeUnknown"], "last admitted completion");
    assert_eq!(received["observerCursor"]["position"], 2);
    assert_eq!(received["nativeViewObservationEnded"], true);
    let late = envelope(
        &generation,
        3,
        "item/completed",
        json!({"threadId":"t","turnId":"u","item":{"id":"i","type":"commandExecution","status":"failed","nativeUnknown":"late must not replace"}}),
    );
    let foreign = envelope(
        &g("b", 1),
        4,
        "item/completed",
        json!({"threadId":"t","turnId":"u","item":{"id":"foreign","type":"commandExecution","status":"completed"}}),
    );
    let refused = session.receive(&observation(
        &generation,
        "failed",
        vec![late, foreign],
        vec![],
    ));
    assert_eq!(
        refused["nativeView"]["items"],
        received["nativeView"]["items"]
    );
    assert_eq!(refused["observerCursor"]["position"], 2);
}
