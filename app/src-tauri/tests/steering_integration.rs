//! Actual steering IPC helper/projection with authored mock-native observations.
//! No supplier/model/window or human act; source-gated Host transport is separately reviewed.
use chirality_app_v4_lib::runtime_session::{
    observed_steering_target, steer_conversation_turn, RuntimeSession,
};
use serde_json::{json, Value};
use std::cell::Cell;
fn g() -> Value {
    json!({"home":"steer-home","appSession":"steer-session","spawnCounter":1})
}
fn turn(id: &str, status: &str) -> Value {
    json!({"id":id,"items":[],"status":status})
}
fn event(id: &str, status: &str, position: u64) -> Value {
    json!({"generation":g(),"position":position,"class":"notification","frame":{"method":if status=="inProgress"{"turn/started"}else{"turn/completed"},"params":{"threadId":"thread","turn":turn(id,status)}}})
}
fn boundary(id: &str, status: &str, position: u64) -> Value {
    json!({"generation":g(),"position":position,"method":if status=="inProgress"{"turn/started"}else{"turn/completed"},"threadId":"thread","turnId":id,"status":status})
}
fn memo(id: &str, status: &str, source: &str, position: u64) -> Value {
    json!({"generation":g(),"threadId":"thread","turnId":id,"nativeTurn":turn(id,status),"source":source,"receiptPosition":position,"observationEnded":false,"terminalEventObserved":false})
}
fn snapshot() -> Value {
    json!({"state":"ready","generation":g(),"threads":[{"generation":g(),"threadId":"thread","model":"existing-model","modelProvider":"existing-provider","appRole":{"standing":"unknown"}}],"conversationTurns":[memo("turn","inProgress","turn/started",1)],"turnEventBoundaries":[boundary("turn","inProgress",1)],"journal":[event("turn","inProgress",1)],"clientRequests":[],"serverRequests":[],"turnInterruptRequests":[],"supplierStanding":"synthetic","versionIdentity":"synthetic"})
}
#[test]
fn exact_current_expected_turn_and_plain_text_ack_preserve_observed_state() {
    let state = snapshot();
    let before = state.clone();
    let text="  exact steer\n包括 é\n{\"model\":\"not an override\",\"approvalPolicy\":\"text only\"}\n ";
    let reply = json!({"id":91,"result":{"turnId":"turn","nativeExtra":"retained"}});
    let calls = Cell::new(0);
    let returned = steer_conversation_turn(
        &state,
        &g(),
        "thread",
        "turn",
        text,
        |generation, thread, expected, actual| {
            calls.set(calls.get() + 1);
            assert_eq!(generation, &g());
            assert_eq!((thread, expected), ("thread", "turn"));
            assert_eq!(actual, text);
            Ok(reply.clone())
        },
    )
    .unwrap();
    assert_eq!(calls.get(), 1);
    assert_eq!(returned, reply);
    assert_eq!(state, before);
    assert_eq!(
        state["conversationTurns"][0]["nativeTurn"]["status"],
        "inProgress"
    );
    assert_eq!(
        observed_steering_target(&state, &g(), "thread").unwrap()["turnId"],
        "turn"
    );
    steer_conversation_turn(&state, &g(), "thread", "turn", " \n ", |_, _, _, text| {
        assert_eq!(text, " \n ");
        Ok(reply)
    })
    .unwrap();
}
#[test]
fn unavailable_foreign_empty_ended_and_unproven_targets_never_invoke_transport() {
    let mut cases = vec![];
    let mut failed = snapshot();
    failed["state"] = json!("failed");
    cases.push((failed, g(), "thread", "turn", "text"));
    for field in ["home", "appSession", "spawnCounter"] {
        let mut other = g();
        other[field] = if field == "spawnCounter" {
            json!(2)
        } else {
            json!("foreign")
        };
        cases.push((snapshot(), other, "thread", "turn", "text"));
    }
    cases.push((snapshot(), json!(1), "thread", "turn", "text"));
    cases.push((snapshot(), g(), "unknown", "turn", "text"));
    cases.push((snapshot(), g(), "thread", "", "text"));
    cases.push((snapshot(), g(), "thread", "turn", ""));
    for field in ["terminalEventObserved", "observationEnded"] {
        let mut ended = snapshot();
        ended["conversationTurns"][0][field] = json!(true);
        cases.push((ended, g(), "thread", "turn", "text"));
    }
    let mut completed = snapshot();
    completed["journal"] = json!([event("turn", "completed", 2)]);
    completed["turnEventBoundaries"] = json!([boundary("turn", "completed", 2)]);
    completed["conversationTurns"][0]["nativeTurn"]["status"] = json!("completed");
    cases.push((completed, g(), "thread", "turn", "text"));
    let mut unproven = snapshot();
    unproven["journal"] = json!([]);
    unproven["turnEventBoundaries"] = json!([]);
    unproven["conversationTurns"][0]["source"] = json!("unknown source");
    cases.push((unproven, g(), "thread", "turn", "text"));
    for (state, generation, thread, expected, text) in cases {
        assert!(steer_conversation_turn(
            &state,
            &generation,
            thread,
            expected,
            text,
            |_, _, _, _| panic!("guard must refuse before any transport or fallback")
        )
        .is_err());
    }
}
#[test]
fn later_native_event_supersedes_delayed_response_and_ambiguous_projection_has_no_winner() {
    let mut state = snapshot();
    let mut delayed = memo("old", "inProgress", "turn/start response", 11);
    delayed["startResponseIssuedAfterReceipt"] = json!(0);
    state["conversationTurns"] = json!([delayed, memo("new", "inProgress", "turn/started", 10)]);
    state["journal"] = json!([event("new", "inProgress", 10)]);
    state["turnEventBoundaries"] = json!([boundary("new", "inProgress", 10)]);
    assert_eq!(
        observed_steering_target(&state, &g(), "thread").unwrap()["turnId"],
        "new"
    );
    assert!(steer_conversation_turn(
        &state,
        &g(),
        "thread",
        "old",
        "retained draft",
        |_, _, _, _| panic!("old memo cannot steer")
    )
    .is_err());
    steer_conversation_turn(
        &state,
        &g(),
        "thread",
        "new",
        "new input",
        |_, _, expected, _| Ok(json!({"id":92,"result":{"turnId":expected}})),
    )
    .unwrap();
    let mut fresh = memo("fresh", "inProgress", "turn/start response", 13);
    fresh["startResponseIssuedAfterReceipt"] = json!(12);
    state["journal"] = json!([event("new", "completed", 12)]);
    state["turnEventBoundaries"] = json!([boundary("new", "completed", 12)]);
    state["conversationTurns"] = json!([fresh.clone()]);
    assert_eq!(
        observed_steering_target(&state, &g(), "thread").unwrap()["turnId"],
        "fresh"
    );
    let mut second = fresh;
    second["turnId"] = json!("second");
    second["nativeTurn"]["id"] = json!("second");
    state["conversationTurns"]
        .as_array_mut()
        .unwrap()
        .push(second);
    assert!(observed_steering_target(&state, &g(), "thread")
        .unwrap_err()
        .contains("ambiguous"));
    assert!(steer_conversation_turn(
        &state,
        &g(),
        "thread",
        "fresh",
        "draft",
        |_, _, _, _| panic!("no arbitrary source winner")
    )
    .is_err());
}
#[test]
fn failed_wait_write_native_error_and_mismatched_ack_return_once_without_rebind() {
    let state = snapshot();
    let before = state.clone();
    for error in [
        "native expected turn refusal",
        "write failed; outcome unknown",
        "wait limit ended; request pending",
        "actual Host source/generation changed after response",
    ] {
        let calls = Cell::new(0);
        let returned = steer_conversation_turn(
            &state,
            &g(),
            "thread",
            "turn",
            "keep draft",
            |_, _, _, _| {
                calls.set(calls.get() + 1);
                Err(error.into())
            },
        )
        .unwrap_err();
        assert_eq!(returned, error);
        assert_eq!(calls.get(), 1);
        assert_eq!(state, before);
    }
    for response in [
        json!({"id":93,"result":{"turnId":"other"}}),
        json!({"id":94,"result":{}}),
        json!({"id":95,"result":{"turnId":"turn"},"error":{"code":-1,"message":"native error"}}),
    ] {
        let calls = Cell::new(0);
        assert!(steer_conversation_turn(
            &state,
            &g(),
            "thread",
            "turn",
            "keep draft",
            |_, _, _, _| {
                calls.set(calls.get() + 1);
                Ok(response)
            }
        )
        .is_err());
        assert_eq!(calls.get(), 1);
        assert_eq!(state, before);
    }
}
#[test]
fn actual_receiving_view_ack_is_separate_from_later_native_completion_and_guard_refusal() {
    let mut session = RuntimeSession::default();
    let mut state = snapshot();
    let started = event("turn", "inProgress", 1);
    let received =
        session.receive(&json!({"generation":g(),"frames":[started],"gap":false,"snapshot":state}));
    assert_eq!(received["nativeView"]["turns"][0]["status"], "inProgress");
    steer_conversation_turn(&state, &g(), "thread", "turn", "input", |_, _, _, _| {
        Ok(json!({"id":96,"result":{"turnId":"turn"}}))
    })
    .unwrap();
    assert_eq!(
        state["conversationTurns"][0]["nativeTurn"]["status"],
        "inProgress"
    );
    let completed = event("turn", "completed", 2);
    state["journal"]
        .as_array_mut()
        .unwrap()
        .push(completed.clone());
    state["conversationTurns"][0]["nativeTurn"]["status"] = json!("completed");
    state["turnEventBoundaries"] = json!([boundary("turn", "completed", 2)]);
    state["conversationTurns"][0]["terminalEventObserved"] = json!(true);
    let received = session
        .receive(&json!({"generation":g(),"frames":[completed],"gap":false,"snapshot":state}));
    assert_eq!(received["nativeView"]["turns"][0]["status"], "completed");
    assert!(steer_conversation_turn(
        &state,
        &g(),
        "thread",
        "turn",
        "keep draft",
        |_, _, _, _| panic!("completion must not fallback start")
    )
    .is_err());
}

#[test]
fn diagnostic_journal_changes_neither_current_target_nor_later_boundary_refusal() {
    let journals = [
        None,
        Some(json!([])),
        Some(json!([event("turn", "completed", 900)])),
        Some(json!([event("journal-only", "inProgress", 999)])),
    ];
    for journal in journals {
        let mut state = snapshot();
        if let Some(journal) = journal {
            state["journal"] = journal;
        } else {
            state.as_object_mut().unwrap().remove("journal");
        }
        assert_eq!(
            observed_steering_target(&state, &g(), "thread").unwrap()["turnId"],
            "turn"
        );
        let calls = Cell::new(0);
        steer_conversation_turn(&state, &g(), "thread", "turn", "input", |_, _, _, _| {
            calls.set(calls.get() + 1);
            Ok(json!({"id":97,"result":{"turnId":"turn"}}))
        })
        .unwrap();
        assert_eq!(calls.get(), 1);
    }

    let unknown = json!({"generation":g(),"position":2,"method":"turn/started","threadId":"thread","turnId":null,"status":null});
    for latest in [boundary("turn", "completed", 2), unknown] {
        for journal in [json!([]), json!([event("turn", "inProgress", 999)])] {
            let mut state = snapshot();
            // Retained active-looking memos are not revived by removing a
            // diagnostic completion or replacing it with an old-looking start.
            state["turnEventBoundaries"] = json!([boundary("turn", "inProgress", 1), latest]);
            state["journal"] = journal;
            assert!(observed_steering_target(&state, &g(), "thread").is_err());
            assert!(steer_conversation_turn(
                &state,
                &g(),
                "thread",
                "turn",
                "retained draft",
                |_, _, _, _| panic!("raw diagnostics cannot revive an older active memo")
            )
            .is_err());
        }
    }
}

#[test]
fn missing_foreign_unknown_or_invalid_boundary_facts_do_not_authorize_transport() {
    let mut cases = vec![];
    let mut missing = snapshot();
    missing
        .as_object_mut()
        .unwrap()
        .remove("turnEventBoundaries");
    cases.push(missing);
    for unavailable in [Value::Null, json!({}), json!([])] {
        let mut state = snapshot();
        state["turnEventBoundaries"] = unavailable;
        cases.push(state);
    }
    let mut facts = vec![];
    for field in ["home", "appSession", "spawnCounter"] {
        let mut foreign = boundary("turn", "inProgress", 999);
        foreign["generation"][field] = if field == "spawnCounter" {
            json!(2)
        } else {
            json!("foreign")
        };
        facts.push(foreign);
    }
    for (field, value) in [
        ("generation", Value::Null),
        ("threadId", json!("foreign-thread")),
        ("method", json!("item/started")),
        ("turnId", Value::Null),
        ("turnId", json!("other-turn")),
        ("status", Value::Null),
        ("status", json!("unknown")),
        ("position", Value::Null),
        ("position", json!(-1)),
        ("position", json!("999")),
        ("position", json!(1.5)),
        ("position", json!(true)),
    ] {
        let mut fact = boundary("turn", "inProgress", 999);
        fact[field] = value;
        facts.push(fact);
    }
    for field in [
        "generation",
        "position",
        "method",
        "threadId",
        "turnId",
        "status",
    ] {
        let mut fact = boundary("turn", "inProgress", 999);
        fact.as_object_mut().unwrap().remove(field);
        facts.push(fact);
    }
    for fact in facts {
        let mut state = snapshot();
        state["turnEventBoundaries"] = json!([fact]);
        cases.push(state);
    }
    for state in cases {
        assert!(
            observed_steering_target(&state, &g(), "thread").is_err(),
            "{state}"
        );
        assert!(steer_conversation_turn(
            &state,
            &g(),
            "thread",
            "turn",
            "retain input",
            |_, _, _, _| panic!("an unavailable boundary cannot authorize transport")
        )
        .is_err());
    }
}

#[test]
fn foreign_invalid_and_older_facts_cannot_displace_known_newer_boundary() {
    let mut distractors = vec![boundary("old", "inProgress", 1)];
    for field in ["home", "appSession", "spawnCounter"] {
        let mut foreign = boundary("old", "inProgress", 999);
        foreign["generation"][field] = if field == "spawnCounter" {
            json!(2)
        } else {
            json!("foreign")
        };
        distractors.push(foreign);
    }
    for (field, value) in [
        ("threadId", json!("foreign-thread")),
        ("method", json!("item/started")),
        ("position", json!("999")),
        ("position", json!(-1)),
        ("position", Value::Null),
    ] {
        let mut fact = boundary("old", "inProgress", 999);
        fact[field] = value;
        distractors.push(fact);
    }
    distractors.push(json!({"generation":g(),"position":9,"method":"turn/started","threadId":"thread","turnId":null,"status":null}));
    for distractor in distractors {
        for facts in [
            json!([distractor, boundary("new", "inProgress", 10)]),
            json!([boundary("new", "inProgress", 10), distractor]),
        ] {
            let mut state = snapshot();
            state["conversationTurns"] = json!([
                memo("old", "inProgress", "turn/started", 1),
                memo("new", "inProgress", "turn/started", 10),
            ]);
            state["turnEventBoundaries"] = facts;
            state["journal"] = json!([event("old", "inProgress", 999)]);
            assert_eq!(
                observed_steering_target(&state, &g(), "thread").unwrap()["turnId"],
                "new"
            );
            assert!(steer_conversation_turn(
                &state,
                &g(),
                "thread",
                "old",
                "retained old draft",
                |_, _, _, _| panic!("foreign or invalid facts cannot select the old memo")
            )
            .is_err());
            steer_conversation_turn(&state, &g(), "thread", "new", "new input", |_, _, _, _| {
                Ok(json!({"id":98,"result":{"turnId":"new"}}))
            })
            .unwrap();
        }
    }
}

#[test]
fn empty_source_boundary_array_preserves_fresh_response_but_missing_field_refuses() {
    let mut state = snapshot();
    let mut fresh = memo("fresh", "inProgress", "turn/start response", 13);
    fresh["startResponseIssuedAfterReceipt"] = json!(12);
    state["conversationTurns"] = json!([fresh]);
    state["turnEventBoundaries"] = json!([]);
    state["journal"] = json!([event("diagnostic-only", "completed", 999)]);
    assert_eq!(
        observed_steering_target(&state, &g(), "thread").unwrap()["turnId"],
        "fresh"
    );
    steer_conversation_turn(&state, &g(), "thread", "fresh", "input", |_, _, _, _| {
        Ok(json!({"id":99,"result":{"turnId":"fresh"}}))
    })
    .unwrap();

    let mut missing = state.clone();
    missing
        .as_object_mut()
        .unwrap()
        .remove("turnEventBoundaries");
    assert!(observed_steering_target(&missing, &g(), "thread").is_err());
    assert!(steer_conversation_turn(
        &missing,
        &g(),
        "thread",
        "fresh",
        "retain input",
        |_, _, _, _| panic!("a missing source fact array cannot fall back to the journal")
    )
    .is_err());

    state["turnEventBoundaries"] = json!([{"generation":g(),"position":12,"method":"turn/started","threadId":"thread","turnId":null,"status":null}]);
    assert_eq!(
        observed_steering_target(&state, &g(), "thread").unwrap()["turnId"],
        "fresh"
    );
    state["conversationTurns"][0]["startResponseIssuedAfterReceipt"] = json!(11);
    assert!(observed_steering_target(&state, &g(), "thread").is_err());
    assert!(steer_conversation_turn(
        &state,
        &g(),
        "thread",
        "fresh",
        "retain delayed response draft",
        |_, _, _, _| panic!("a delayed response cannot cross a newer unknown boundary")
    )
    .is_err());
}
