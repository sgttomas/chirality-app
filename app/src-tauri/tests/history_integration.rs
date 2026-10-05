//! Actual App-owned history/session and text receiving helpers with invented native
//! frames. Private transport receipts are exercised by Host inline joined tests;
//! these checks launch no supplier, account, model or native window.
use chirality_app_v4_lib::{
    native_history::Direction,
    role_lifecycle::{PreparedStart, RoleBindings},
    role_supply::{Composition, Guidance, Role},
    runtime_session::{send_conversation_text, HistorySession},
};
use serde_json::{json, Value};
fn g() -> Value {
    json!({"home":"mock-home","appSession":"mock-session","spawnCounter":1})
}
fn host() -> Value {
    json!({"generation":g(),"state":"ready","threads":[]})
}
fn thread(id: &str, status: &str) -> Value {
    json!({"id":id,"cliVersion":"0.160.0","createdAt":1,"updatedAt":2,"cwd":"/mock","ephemeral":false,"modelProvider":"mock-provider","preview":"native preview","projectId":null,"sessionId":"mock-native-session","source":"appServer","status":{"type":status},"turns":[],"agentRole":"TASK"})
}
fn native_result(id: &str) -> Value {
    json!({"thread":thread(id,"idle"),"model":"mock-model","modelProvider":"mock-provider","cwd":"/mock","approvalPolicy":"on-request","approvalsReviewer":"user","sandbox":{"type":"readOnly"},"instructionSources":[]})
}
fn listed() -> HistorySession {
    let mut session = HistorySession::default();
    let q = session
        .prepare(&host(), &g(), 0, "list", None, Direction::Desc, None)
        .unwrap();
    session.history_mut().unwrap().receive(&q,"mock-home",&g(),&json!({"data":[thread("stored","notLoaded"),thread("other","idle")],"nextCursor":"opaque-next","backwardsCursor":null})).unwrap();
    session
}
#[test]
fn readonly_selection_metadata_and_pages_never_enable_text_or_infer_app_role() {
    let mut session = listed();
    session.select(&host(), &g(), 0, "stored").unwrap();
    let metadata = session
        .prepare(&host(), &g(), 1, "metadata", None, Direction::Desc, None)
        .unwrap();
    session
        .history_mut()
        .unwrap()
        .receive(
            &metadata,
            "mock-home",
            &g(),
            &json!({"thread":thread("stored","notLoaded")}),
        )
        .unwrap();
    let turns = session
        .prepare(&host(), &g(), 1, "turns", None, Direction::Desc, None)
        .unwrap();
    session.history_mut().unwrap().receive(&turns,"mock-home",&g(),&json!({"data":[{"id":"turn","status":"completed","items":[],"itemsView":"summary","error":null}],"nextCursor":null})).unwrap();
    let items = session
        .prepare(
            &host(),
            &g(),
            1,
            "items",
            None,
            Direction::Desc,
            Some("turn"),
        )
        .unwrap();
    session
        .history_mut()
        .unwrap()
        .receive(
            &items,
            "mock-home",
            &g(),
            &json!({"data":[],"nextCursor":null}),
        )
        .unwrap();
    let view = session.snapshot(None);
    assert_eq!(view["selected"]["metadata"]["thread"]["agentRole"], "TASK");
    assert_eq!(view["selected"]["appRole"]["standing"], "unknown");
    assert_eq!(
        view["selected"]["turnsPage"]["data"][0]["itemsView"],
        "summary"
    );
    assert_eq!(view["selected"]["itemsPage"]["data"], json!([]));
    assert_eq!(view["activeBindingPerformed"], false);
    assert!(
        send_conversation_text(&host(), &g(), "stored", "unchanged", |_, _, _| panic!(
            "read-only must not dispatch text"
        ))
        .is_err()
    );
}
#[test]
fn generation_epoch_and_received_identity_guards_refuse_before_query_issue() {
    let mut session = listed();
    session.select(&host(), &g(), 0, "stored").unwrap();
    for (generation, epoch, action, reference) in [
        (json!(1), 1, "metadata", None),
        (g(), 0, "continue", None),
        (g(), 1, "items", Some("unreceived-turn")),
        (g(), 1, "child", Some("native-hint-only")),
    ] {
        assert!(session
            .prepare(
                &host(),
                &generation,
                epoch,
                action,
                None,
                Direction::Desc,
                reference
            )
            .is_err());
    }
    assert!(session
        .prepare(
            &host(),
            &g(),
            1,
            "turns",
            Some("invented-cursor"),
            Direction::Desc,
            None
        )
        .is_err());
    assert!(session
        .prepare(
            &host(),
            &g(),
            1,
            "list",
            Some("opaque-next"),
            Direction::Asc,
            None
        )
        .is_err());
    assert!(session.select(&host(), &g(), 1, "not-listed").is_err());
    let old = session
        .prepare(&host(), &g(), 1, "metadata", None, Direction::Desc, None)
        .unwrap();
    session.select(&host(), &g(), 1, "other").unwrap();
    assert!(session
        .history_mut()
        .unwrap()
        .receive(
            &old,
            "mock-home",
            &g(),
            &json!({"thread":thread("stored","idle")})
        )
        .is_err());
    assert_eq!(session.snapshot(None)["selected"]["threadId"], "other");
}
#[test]
fn continue_is_exact_native_id_and_current_receiving_candidate_only() {
    let mut session = listed();
    session.select(&host(), &g(), 0, "stored").unwrap();
    let q = session
        .prepare(&host(), &g(), 1, "continue", None, Direction::Desc, None)
        .unwrap();
    assert_eq!(q.method(), "thread/resume");
    assert_eq!(q.params(), &json!({"threadId":"stored"}));
    session.history_mut().unwrap().waiting_ended(&q).unwrap();
    assert_eq!(session.snapshot(None)["pending"][0]["waitingEnded"], true);
    assert!(session.history().unwrap().resumed_thread().is_none());
    session
        .history_mut()
        .unwrap()
        .receive(&q, "mock-home", &g(), &native_result("stored"))
        .unwrap();
    assert!(session.history().unwrap().resumed_thread().is_some());
    assert_eq!(session.snapshot(None)["activeBindingPerformed"], false);
    let pending = session
        .prepare(&host(), &g(), 1, "metadata", None, Direction::Desc, None)
        .unwrap();
    assert!(session.history().unwrap().resumed_thread().is_none());
    session
        .history_mut()
        .unwrap()
        .receive(
            &pending,
            "mock-home",
            &g(),
            &json!({"thread":thread("stored","notLoaded")}),
        )
        .unwrap();
    assert!(session.history().unwrap().resumed_thread().is_none());
}
#[test]
fn native_error_pending_null_goal_and_closed_generation_remain_distinct() {
    let mut session = listed();
    session.select(&host(), &g(), 0, "stored").unwrap();
    let q = session
        .prepare(&host(), &g(), 1, "goal", None, Direction::Desc, None)
        .unwrap();
    assert!(session.snapshot(None)["selected"]["goalAvailability"]
        .as_str()
        .unwrap()
        .starts_with("pending"));
    session
        .history_mut()
        .unwrap()
        .receive_error(
            &q,
            "mock-home",
            &g(),
            &json!({"code":-1,"message":"mock native failure"}),
        )
        .unwrap();
    assert_eq!(
        session.snapshot(None)["selected"]["goalAvailability"],
        "unavailable"
    );
    let q = session
        .prepare(&host(), &g(), 1, "goal", None, Direction::Desc, None)
        .unwrap();
    session
        .history_mut()
        .unwrap()
        .receive(&q, "mock-home", &g(), &json!({"goal":null}))
        .unwrap();
    assert_eq!(
        session.snapshot(None)["selected"]["goalAvailability"],
        "no-goal-reported"
    );
    assert_eq!(
        session.snapshot(None)["selected"]["errorHistory"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    let mut ended = host();
    ended["state"] = json!("stopped");
    session.synchronize(&ended);
    assert!(session.history().is_none());
    session.synchronize(&host());
    assert!(session.history().is_none());
    let mut next = host();
    next["generation"]["spawnCounter"] = json!(2);
    session.synchronize(&next);
    assert!(session.history().is_some());
    assert!(session.snapshot(None)["selected"].is_null());
}
fn composition(role: Option<Role>) -> Composition {
    let common = Guidance::seeded(
        "AGENTS.md",
        "mock-release",
        b"original common".to_vec(),
        b"original common",
    )
    .unwrap();
    let active = role.map(|r| {
        Guidance::seeded(
            &format!("agents/AGENT_{}.md", r.name()),
            "mock-release",
            b"original role".to_vec(),
            b"original role",
        )
        .unwrap()
    });
    Composition::new(&common, role.zip(active.as_ref()), false).unwrap()
}
#[test]
fn original_mock_role_binding_remains_fixed_and_cold_imported_state_unknown() {
    for role in [Some(Role::HELP_HUMAN), None] {
        let c = composition(role);
        let prepared = PreparedStart::new(
            "mock-home",
            g(),
            json!(99),
            "mock-rpc:99",
            "sup:mock-99",
            &c,
        )
        .unwrap();
        let actual_sent = json!({"id":99,"method":"thread/start","params":{"developerInstructions":c.text,"model":"mock-model","modelProvider":"mock-provider","cwd":"/mock"}});
        let binding = prepared
            .observe(
                &g(),
                &actual_sent,
                &json!({"id":99,"result":native_result("stored")}),
            )
            .unwrap();
        let original = binding.evidence();
        let mut session = listed();
        session.bind(binding).unwrap();
        session.select(&host(), &g(), 0, "stored").unwrap();
        let view = session.snapshot(None);
        assert_eq!(view["selected"]["appRole"]["standing"], "app-observed");
        assert_eq!(view["selected"]["appRole"]["role"], json!(role));
        assert_eq!(view["selected"]["originalRoleSupply"], original);
        assert!(view["selected"]["futureGuidanceNotices"]
            .as_array()
            .unwrap()
            .iter()
            .all(|n| n["appliesTo"] == "future-conversations"
                && n["currentConversationRoleChanged"] == false));
        assert_eq!(
            json!(RoleBindings::imported_role(&original))["standing"],
            "unknown"
        );
        assert_eq!(
            HistorySession::default().role("mock-home", "stored")["standing"],
            "unknown"
        );
        assert_eq!(
            session.role("foreign-home", "stored")["standing"],
            "unknown"
        );
        assert_eq!(
            session.snapshot(None)["selected"]["originalRoleSupply"],
            original
        );
    }
}

fn start_selection(id: &str) -> chirality_app_v4_lib::access::ConversationSelection {
    let mut selection =
        chirality_app_v4_lib::access::ConversationSelection::new(id, "/mock").unwrap();
    selection
        .choose("chatgpt-account", "mock-provider", "mock-model", false)
        .unwrap();
    selection.start_params(&g(), "account", false).unwrap();
    selection
}
#[test]
fn failed_no_effect_preclaim_preserves_previous_selection_and_can_claim_again() {
    use chirality_app_v4_lib::runtime_session::claim_start;
    let mut previous =
        chirality_app_v4_lib::access::ConversationSelection::new("previous", "/mock").unwrap();
    previous
        .choose(
            "chatgpt-account",
            "previous-provider",
            "previous-model",
            false,
        )
        .unwrap();
    let before = previous.snapshot();
    let mut slot = Some(previous);
    assert!(claim_start(&mut slot, start_selection("failed"), || Err(
        "injected entropy failure before dispatch".into()
    ))
    .is_err());
    assert_eq!(slot.as_ref().unwrap().snapshot(), before);
    assert_eq!(
        claim_start(&mut slot, start_selection("second"), || Ok(
            "sup:second".into()
        ))
        .unwrap(),
        "sup:second"
    );
    assert_eq!(slot.as_ref().unwrap().snapshot()["state"], "starting");
}
#[test]
fn every_postclaim_error_finalizes_without_synthetic_native_success_or_resend() {
    use chirality_app_v4_lib::runtime_session::{claim_start, finalize_start_attempt};
    let mut newer = start_selection("newer-attempt");
    let newer_before = newer.snapshot();
    assert!(finalize_start_attempt(
        &mut newer,
        "old-attempt",
        &g(),
        &g(),
        Err("old operation failed".into())
    )
    .is_err());
    assert_eq!(newer.snapshot(), newer_before);
    let mut old_generation = g();
    old_generation["appSession"] = json!("old-session");
    assert!(finalize_start_attempt(
        &mut newer,
        "newer-attempt",
        &old_generation,
        &g(),
        Err("old generation failed".into())
    )
    .is_err());
    assert_eq!(newer.snapshot(), newer_before);

    let mut changed = g();
    changed["spawnCounter"] = json!(2);
    for (id, current, result) in [
        ("dispatch-refused", g(), Err("refused-not-sent: not-ready".into())),
        ("postdispatch-role", g(), Err("Native start dispatched; original role preparation failed; unknown native effect in retained receipt".into())),
        ("malformed-result", g(), Ok(json!({"id":99,"result":{"thread":{"id":""}}}))),
        ("changed-generation", changed, Ok(json!({"id":99,"result":native_result("native-thread")}))),
        ("mixed-envelope", g(), Ok(json!({"id":99,"result":native_result("native-thread"),"error":{"code":-1,"message":"error"}}))),
    ] {
        let mut slot = None;
        claim_start(&mut slot, start_selection(id), || Ok(format!("sup:{id}"))).unwrap();
        assert!(finalize_start_attempt(slot.as_mut().unwrap(), id, &g(), &current, result).is_err());
        let failed = slot.as_ref().unwrap().snapshot();
        assert_eq!(failed["state"], "start-failed", "{id}");
        assert!(failed["refusal"]["text"].as_str().unwrap().len() > 0);
        assert!(failed["thread"].is_null());
        // Only an explicit independently requested attempt claims again.
        claim_start(&mut slot, start_selection("explicit-next"), || Ok("sup:next".into())).unwrap();
        assert_eq!(slot.as_ref().unwrap().snapshot()["state"], "starting");
    }
}
