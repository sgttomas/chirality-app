//! Real App command helpers with explicit synthetic/mock transport and native
//! envelopes. No supplier child/model turn, native window or account is used.
use chirality_app_v4_lib::{
    native_requests::RequestRegister,
    recovery::RecoveryLedger,
    runtime_session::{
        interrupt_conversation_turn, reviewed_ledger_path, send_conversation_text, RuntimeSession,
    },
};
use serde_json::{json, Value};
fn g() -> Value {
    json!({"appSession":"synthetic","home":"synthetic-home","spawnCounter":1})
}
fn snapshot() -> Value {
    json!({"state":"ready","generation":g(),"threads":[{"generation":g(),"threadId":"thread","model":"existing-model","modelProvider":"existing-provider"}],"conversationTurns":[{"generation":g(),"threadId":"thread","turnId":"turn","nativeTurn":{"id":"turn","items":[],"status":"inProgress"},"observationEnded":false}],"turnInterruptRequests":[]})
}
#[test]
fn text_control_passes_exact_selected_namespace_text_and_unmodified_mock_response() {
    let text = "  text unchanged\n包括 whitespace \n";
    let response = json!({"id":7,"result":{"turn":{"id":"turn","items":[],"status":"inProgress","nativeUnknown":42}}});
    let result = send_conversation_text(
        &snapshot(),
        &g(),
        "thread",
        text,
        |generation, thread, received| {
            assert_eq!(generation, &g());
            assert_eq!(thread, "thread");
            assert_eq!(received, text);
            Ok(response.clone())
        },
    )
    .unwrap();
    assert_eq!(result, response);
    // Whitespace is text, not silently trimmed or framed as role/workflow instructions.
    send_conversation_text(&snapshot(), &g(), "thread", " \n ", |_, _, text| {
        assert_eq!(text, " \n ");
        Ok(json!({}))
    })
    .unwrap();
}
#[test]
fn stale_scalar_unloaded_and_empty_selections_never_invoke_transport() {
    let mut unavailable = snapshot();
    unavailable["state"] = json!("failed");
    let mut foreign = g();
    foreign["home"] = json!("other-home");
    for (state, generation, thread, text) in [
        (snapshot(), foreign, "thread", "text"),
        (snapshot(), json!(1), "thread", "text"),
        (unavailable, g(), "thread", "text"),
        (snapshot(), g(), "unloaded", "text"),
        (snapshot(), g(), "thread", ""),
    ] {
        assert!(
            send_conversation_text(&state, &generation, thread, text, |_, _, _| panic!(
                "refused selection must not send"
            ))
            .is_err()
        );
    }
}
#[test]
fn failed_send_or_interrupt_is_returned_once_without_mutating_observed_native_state() {
    let state = snapshot();
    let original = state.clone();
    let count = std::cell::Cell::new(0);
    let error = send_conversation_text(&state, &g(), "thread", "keep draft", |_, _, _| {
        count.set(count.get() + 1);
        Err("synthetic write/wait failure; outcome unknown".into())
    })
    .unwrap_err();
    assert_eq!(count.get(), 1);
    assert!(error.contains("outcome unknown"));
    assert_eq!(state, original);
    let response = json!({"id":8,"result":{}});
    assert_eq!(
        interrupt_conversation_turn(
            &state,
            &g(),
            "thread",
            "turn",
            |generation, thread, turn| {
                assert_eq!(generation, &g());
                assert_eq!((thread, turn), ("thread", "turn"));
                Ok(response.clone())
            }
        )
        .unwrap(),
        response
    );
    assert_eq!(
        state["conversationTurns"][0]["nativeTurn"]["status"],
        "inProgress"
    );
    assert_eq!(state, original);
    let error = interrupt_conversation_turn(&state, &g(), "thread", "turn", |_, _, _| {
        Err("synthetic native interrupt refusal".into())
    })
    .unwrap_err();
    assert_eq!(error, "synthetic native interrupt refusal");
    assert_eq!(state, original);
}
#[test]
fn ended_foreign_or_already_requested_turn_cannot_interrupt_again() {
    let mut states = Vec::new();
    let mut contradictory = snapshot();
    contradictory["conversationTurns"][0]["terminalEventObserved"] = json!(true);
    contradictory["conversationTurns"][0]["inconsistencyLimits"] =
        json!(["synthetic exact terminal-then-progress contradiction"]);
    assert_eq!(
        contradictory["conversationTurns"][0]["nativeTurn"]["status"],
        "inProgress"
    );
    states.push(contradictory);
    let mut ended = snapshot();
    ended["conversationTurns"][0]["nativeTurn"]["status"] = json!("interrupted");
    states.push(ended);
    let mut lost = snapshot();
    lost["conversationTurns"][0]["observationEnded"] = json!(true);
    states.push(lost);
    let mut foreign = snapshot();
    foreign["conversationTurns"][0]["generation"]["spawnCounter"] = json!(2);
    states.push(foreign);
    for outcome in ["pending", "response-observed-result"] {
        let mut sent = snapshot();
        sent["turnInterruptRequests"] = json!([{"binding":{"generation":g(),"threadId":"thread","turnId":"turn","requestIdentity":8},"clientRequest":{"writeResult":"written","outcome":outcome}}]);
        states.push(sent);
    }
    for state in states {
        assert!(
            interrupt_conversation_turn(&state, &g(), "thread", "turn", |_, _, _| panic!(
                "no native repeat"
            ))
            .is_err()
        );
    }
}
#[test]
fn selected_text_control_to_native_activity_request_and_pointer_ledger_keeps_outcome_separate() {
    let mut state = snapshot();
    let mut view = RuntimeSession::default();
    let mut requests = RequestRegister::default();
    send_conversation_text(
        &state,
        &g(),
        "thread",
        "synthetic request-producing text",
        |_, _, _| {
            Ok(json!({"id":7,"result":{"turn":{"id":"turn","items":[],"status":"inProgress"}}}))
        },
    )
    .unwrap();
    requests.receive(&g(),2,&json!({"id":"r","method":"item/fileChange/requestApproval","params":{"threadId":"thread","turnId":"turn","itemId":"item","reason":"synthetic native request"}}),&json!({})).unwrap();
    state["serverRequests"] = json!(requests.records());
    let activity = json!({"generation":g(),"position":1,"class":"notification","frame":{"method":"item/started","params":{"threadId":"thread","turnId":"turn","item":{"id":"item","type":"fileChange","status":"inProgress","changes":[],"nativeUnknown":"kept"}}}});
    let observed =
        view.receive(&json!({"generation":g(),"snapshot":state,"gap":false,"frames":[activity]}));
    assert_eq!(
        observed["nativeView"]["items"][0]["displayState"],
        "waiting-on-request"
    );
    assert_eq!(
        observed["nativeView"]["items"][0]["native"]["nativeUnknown"],
        "kept"
    );
    let root = std::env::temp_dir()
        .join(chirality_app_v4_lib::util::opaque_id("conversation-ledger-").unwrap());
    let path = reviewed_ledger_path(&root);
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
    ledger.start_session("synthetic", "synthetic-test").unwrap();
    ledger.request_summary(&requests.entries()[0]).unwrap();
    let bytes = std::fs::read_to_string(&path).unwrap();
    assert!(!bytes.contains("synthetic native request"));
    assert!(!bytes.contains("synthetic request-producing text"));
    interrupt_conversation_turn(&state, &g(), "thread", "turn", |_, _, _| {
        Ok(json!({"result":{}}))
    })
    .unwrap();
    assert_eq!(
        state["conversationTurns"][0]["nativeTurn"]["status"],
        "inProgress"
    );
    let ended = json!({"generation":g(),"position":3,"class":"notification","frame":{"method":"turn/completed","params":{"threadId":"thread","turn":{"id":"turn","items":[],"status":"interrupted","error":{"message":"native error remains interrupted"}}}}});
    let end_view =
        view.receive(&json!({"generation":g(),"snapshot":state,"gap":false,"frames":[ended]}));
    assert_eq!(end_view["nativeView"]["turns"][0]["status"], "interrupted");
    assert!(end_view["nativeView"]["turns"][0]["error"].is_object());
    std::fs::remove_dir_all(root).unwrap();
}
