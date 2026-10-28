// Actual Host guards and source observations survive removal of diagnostic replay.
// Clearing the vectors here is a test stimulus, not an activated retention policy.
use super::*;

fn clear_replay(host: &Host) {
    let mut i = host.inner.0.lock().unwrap();
    i.journal.clear();
    i.held.clear();
}

fn emit(host: &Host, frame: Value) {
    host.on_line(&serde_json::to_vec(&frame).unwrap(), &g());
}

#[test]
fn journal_independent_turn_boundaries_keep_host_and_receiving_target_in_agreement() {
    let host = host();
    let mut next = turn("inProgress");
    next["id"] = json!("new-turn");
    // The actual App request precedes the new native event; its delayed reply
    // must not make that older request's turn the current steering target.
    let (reply, _) = exchange(
        &host,
        Some(json!({"result":{"turn":turn("inProgress")}})),
        vec![json!({"method":"turn/started","params":{"threadId":"thread","turn":next}})],
        || host.turn_start_text(&g(), "thread", "exact old input"),
    );
    assert!(reply.is_ok());
    for deceptive in [false, true] {
        clear_replay(&host);
        if deceptive {
            host.inner.0.lock().unwrap().journal.push(json!({"generation":g(),"position":9999,"frame":{"method":"turn/started","params":{"threadId":"thread","turn":turn("inProgress")}}}));
        }
        assert_eq!(
            Host::current_live_turn(&host.inner.0.lock().unwrap(), "thread").unwrap()["turnId"],
            "new-turn"
        );
        assert_eq!(
            crate::runtime_session::observed_steering_target(&host.snapshot(), &g(), "thread")
                .unwrap()["turnId"],
            "new-turn"
        );
        assert!(Host::check_conversation_request(
            &host.inner.0.lock().unwrap(),
            "turn/steer",
            &json!({"threadId":"thread","expectedTurnId":"turn"})
        )
        .is_err());
        assert!(Host::check_conversation_request(
            &host.inner.0.lock().unwrap(),
            "turn/steer",
            &json!({"threadId":"thread","expectedTurnId":"new-turn"})
        )
        .is_ok());
    }
}

#[test]
fn journal_independent_unknown_and_terminal_boundaries_never_revive_old_memos() {
    for status in ["completed", "unknown-future-status"] {
        let host = host();
        event(&host, "inProgress");
        let mut boundary = turn(status);
        boundary["id"] = json!("new-turn");
        emit(
            &host,
            json!({"method":if status=="completed"{"turn/completed"}else{"turn/started"},"params":{"threadId":"thread","turn":boundary}}),
        );
        clear_replay(&host);
        assert!(Host::current_live_turn(&host.inner.0.lock().unwrap(), "thread").is_none());
        assert!(
            crate::runtime_session::observed_steering_target(&host.snapshot(), &g(), "thread")
                .is_err()
        );
        let before = host.snapshot()["turnEventBoundaries"].clone();
        let mut foreign = g();
        foreign["home"] = json!("other-home");
        host.on_line(&serde_json::to_vec(&json!({"method":"turn/started","params":{"threadId":"thread","turn":turn("inProgress")}})).unwrap(), &foreign);
        assert_eq!(
            host.snapshot()["turnEventBoundaries"],
            before,
            "a late foreign receipt is diagnostic only"
        );
        assert!(Host::current_live_turn(&host.inner.0.lock().unwrap(), "thread").is_none());
    }
}

#[test]
fn journal_independent_resolutions_preserve_typed_request_and_full_source_scope() {
    // A source resolution seen before a later request was already a guard in
    // the journal implementation. Keep that conservative behavior too.
    for resolution_first in [true, false] {
        let host = host();
        let request = json!({"id":1,"method":"item/tool/requestUserInput","params":{"threadId":"thread","turnId":"turn","itemId":"item","questions":[]}});
        let resolved =
            json!({"method":"serverRequest/resolved","params":{"threadId":"thread","requestId":1}});
        if resolution_first {
            emit(&host, resolved.clone());
        }
        emit(&host, request);
        let reply = host
            .inner
            .0
            .lock()
            .unwrap()
            .server_requests
            .prepare_error(
                &g(),
                &json!(1),
                &json!({"code":-32000,"message":"test reply"}),
                "app-rule:fixture",
            )
            .unwrap();
        if !resolution_first {
            for wrong in [
                json!({"method":"serverRequest/resolved","params":{"threadId":"thread","requestId":"1"}}),
                json!({"method":"serverRequest/resolved","params":{"threadId":"other","requestId":1}}),
            ] {
                emit(&host, wrong);
                clear_replay(&host);
                assert!(Host::reply_eligible(
                    &host.inner.0.lock().unwrap(),
                    &g(),
                    &reply
                ));
            }
            emit(&host, resolved);
        }
        clear_replay(&host);
        assert!(!Host::reply_eligible(
            &host.inner.0.lock().unwrap(),
            &g(),
            &reply
        ));
        assert_ne!(
            host.inner.0.lock().unwrap().server_requests.entries()[0]["replyWriteResult"],
            "written"
        );
        assert!(!host.inner.0.lock().unwrap().observation_facts.resolved(
            &json!({"appSession":"other","home":"conversation-home","spawnCounter":1}),
            &json!(1),
            &json!("thread")
        ));
    }
}

#[test]
fn journal_independent_account_aba_changes_invalidate_the_assessment_material() {
    let host = host();
    let home = crate::runtime_session::HomeSession::new(
        crate::home_resources::HomeClass::Account,
        Arc::clone(&host),
        Err("no supplier configuration in this test".into()),
    )
    .unwrap();
    let read = || {
        crate::runtime_session::assess_native_home_work(&home, &g())
            .unwrap()
            .snapshot()["account"]["namespaceRevision"]
            .clone()
    };
    let before = read();
    for _ in 0..2 {
        emit(
            &host,
            json!({"method":"account/updated","params":{"authMode":"chatgpt"}}),
        );
        clear_replay(&host);
        let after = read();
        assert_ne!(
            after, before,
            "an identical/redacted account event is still a namespace change"
        );
    }
    let after = read();
    assert_eq!(after["lastChangeReceiptPosition"], 2);
    assert_eq!(read(), after, "another read alone is not an account change");
    let mut foreign = g();
    foreign["spawnCounter"] = json!(2);
    host.on_line(
        &serde_json::to_vec(&json!({"method":"account/updated","params":{"authMode":"chatgpt"}}))
            .unwrap(),
        &foreign,
    );
    assert_eq!(
        read(),
        after,
        "a foreign source cannot invalidate or rebind this namespace"
    );
}

#[test]
fn journal_independent_stop_retains_actual_original_exit_facts() {
    use std::os::unix::process::CommandExt;
    let host = host();
    let process = process_group_custody::OwnedProcess::spawn(
        Command::new("/bin/sh")
            .args(["-c", "exit 23"])
            .env_clear()
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .process_group(0),
    )
    .unwrap();
    process.bind(&g()).unwrap();
    host.inner.0.lock().unwrap().child_pid = Some(process.id() as i32);
    *host.child.lock().unwrap() = Some(Arc::clone(&process));
    emit(&host, json!({"method":"fixture/receipt","params":{}}));
    host.on_eof_process(&g(), Some(process));
    assert_eq!(host.state(), "exited-unexpectedly");
    clear_replay(&host);
    assert_eq!(
        host.stop("fixture:person", "codex-stop").unwrap()["state"],
        "stopped"
    );
    let stopped = host
        .lifecycle_events()
        .into_iter()
        .find(|e| e["transitionId"] == "LT-23")
        .unwrap();
    assert_eq!(stopped["generation"], g());
    assert_eq!(stopped["exitFacts"]["exitCode"], 23);
    assert_eq!(stopped["exitFacts"]["lastReceiptPosition"], 1);
    assert_eq!(stopped["exitFacts"]["malformedFrameCount"], 0);
}
