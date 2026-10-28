#[path = "../src/native_history.rs"]
mod native_history;
use native_history::{Direction, HistoryQuery, NativeHistory};
use serde_json::{json, Value};
fn g() -> Value {
    json!({"appSession":"history-session","home":"history-home","spawnCounter":1})
}
fn view() -> NativeHistory {
    NativeHistory::new("history-home", g()).unwrap()
}
fn thread(id: &str, status: &str) -> Value {
    json!({"id":id,"cliVersion":"0.160.0","createdAt":1,"updatedAt":2,"cwd":"/invented","ephemeral":false,"modelProvider":"configured","preview":"invented preview","projectId":null,"sessionId":"native-session","source":"appServer","status":{"type":status},"turns":[],"agentRole":"TASK","forkedFromId":"source-thread","nativeExtra":{"preserved":true}})
}
fn turn(id: &str, status: &str, view: &str) -> Value {
    json!({"id":id,"status":status,"items":[],"itemsView":view,"error":null,"nativeExtra":"preserved"})
}
fn accept(v: &mut NativeHistory, q: &HistoryQuery, result: Value) {
    v.receive(q, "history-home", &g(), &result).unwrap();
}
fn selected() -> NativeHistory {
    let mut v = view();
    let q = v.list_threads(None, Direction::Desc).unwrap();
    accept(
        &mut v,
        &q,
        json!({"data":[thread("thread","notLoaded"),thread("second","idle")],"nextCursor":null}),
    );
    v.select("thread").unwrap();
    v
}
fn resume(id: &str, status: &str) -> Value {
    let mut t = thread(id, status);
    if status == "active" {
        t["status"] = json!({"type":"active","activeFlags":["waitingOnUserInput"]});
    }
    t["canAcceptDirectInput"] = json!(true);
    json!({"thread":t,"model":"reported","modelProvider":"configured","cwd":"/invented","approvalPolicy":"on-request","approvalsReviewer":"user","sandbox":{"type":"readOnly"},"instructionSources":["/native/instructions"],"nativeExtra":true})
}
#[test]
fn exact_native_query_factories_and_continue_have_no_guidance_or_execution_overrides() {
    let mut v = selected();
    assert_eq!(v.home(), "history-home");
    assert_eq!(v.generation(), &g());
    assert_eq!(v.selected_thread(), Some("thread"));
    assert_eq!(v.selection_epoch(), 1);
    let read = v.read_metadata().unwrap();
    assert_eq!(read.method(), "thread/read");
    assert_eq!(
        read.params(),
        &json!({"threadId":"thread","includeTurns":false})
    );
    assert_eq!(read.home(), "history-home");
    assert_eq!(read.generation(), &g());
    let turns = v.turns_page(None, Direction::Desc).unwrap();
    assert_eq!(
        turns.params(),
        &json!({"threadId":"thread","sortDirection":"desc","itemsView":"summary"})
    );
    accept(
        &mut v,
        &turns,
        json!({"data":[turn("turn","completed","summary")]}),
    );
    let items = v.items_page("turn", None, Direction::Asc).unwrap();
    assert_eq!(
        items.params(),
        &json!({"threadId":"thread","turnId":"turn","sortDirection":"asc"})
    );
    let goal = v.read_goal().unwrap();
    assert_eq!(goal.params(), &json!({"threadId":"thread"}));
    let continued = v.continue_query().unwrap();
    assert_eq!(continued.method(), "thread/resume");
    assert_eq!(continued.params(), &json!({"threadId":"thread","excludeTurns":true}));
    assert_eq!(v.resumed_thread(), None);
    for q in [read, turns, items, goal, continued] {
        let params = q.params().as_object().unwrap();
        for field in [
            "developerInstructions",
            "baseInstructions",
            "config",
            "model",
            "modelProvider",
            "approvalPolicy",
            "approvalsReviewer",
            "permissions",
            "sandbox",
            "history",
            "path",
        ] {
            assert!(!params.contains_key(field));
        }
    }
}
#[test]
fn indexed_not_loaded_and_summary_are_distinct_from_absent_and_role_is_unknown() {
    let mut v = selected();
    let q = v.read_metadata().unwrap();
    let native = json!({"thread":thread("thread","notLoaded")});
    accept(&mut v, &q, native.clone());
    let q = v.turns_page(None, Direction::Desc).unwrap();
    let page = json!({"data":[turn("ended","interrupted","summary"),turn("live-at-read","inProgress","notLoaded")],"nextCursor":null});
    accept(&mut v, &q, page.clone());
    let snapshot = v.snapshot();
    assert_eq!(snapshot["selected"]["state"], "indexed-read-only");
    assert_eq!(snapshot["selected"]["metadata"], native);
    assert_eq!(snapshot["selected"]["turnsPage"], page);
    assert_eq!(
        snapshot["selected"]["turnsPage"]["data"][1]["status"],
        "inProgress"
    );
    assert_eq!(snapshot["selected"]["appRole"]["standing"], "unknown");
    assert_eq!(snapshot["activeBindingPerformed"], false);
    assert_eq!(v.resumed_thread(), None);
    assert!(snapshot["selected"]["checklists"]
        .as_str()
        .unwrap()
        .contains("cannot be reconstructed"));
    // Native agentRole/fork relation/instruction paths do not assign an App role.
    let q = v.continue_query().unwrap();
    accept(&mut v, &q, resume("thread", "idle"));
    assert_eq!(v.snapshot()["selected"]["appRole"]["standing"], "unknown");
    assert_eq!(
        v.resumed_thread().unwrap()["appRole"]["standing"],
        "unknown"
    );
    assert_eq!(v.snapshot()["activeBindingPerformed"], false);
}
#[test]
fn opaque_cursors_keep_stream_direction_and_missing_null_states() {
    let mut v = view();
    let q = v.list_threads(None, Direction::Desc).unwrap();
    accept(&mut v, &q, json!({"data":[thread("thread","notLoaded")]}));
    assert_eq!(v.snapshot()["listCursor"]["state"], "not-reported");
    assert!(v.list_threads(Some("invented"), Direction::Desc).is_err());
    let q = v.list_threads(None, Direction::Desc).unwrap();
    accept(
        &mut v,
        &q,
        json!({"data":[],"nextCursor":"opaque:/é.next","backwardsCursor":"opaque:/é.back"}),
    );
    let next = v
        .list_threads(Some("opaque:/é.next"), Direction::Desc)
        .unwrap();
    assert_eq!(next.params()["cursor"], "opaque:/é.next");
    assert!(v
        .list_threads(Some("opaque:/é.back"), Direction::Desc)
        .is_err());
    let back = v
        .list_threads(Some("opaque:/é.back"), Direction::Asc)
        .unwrap();
    assert_eq!(back.params()["cursor"], "opaque:/é.back");
    assert!(v
        .receive(
            &next,
            "history-home",
            &g(),
            &json!({"data":[],"nextCursor":null})
        )
        .is_err());
    accept(&mut v, &back, json!({"data":[],"nextCursor":null}));
    assert_eq!(v.snapshot()["listCursor"]["state"], "exhausted");
    v.select("thread").unwrap();
    let q = v.turns_page(None, Direction::Desc).unwrap();
    accept(
        &mut v,
        &q,
        json!({"data":[turn("turn","completed","summary")],"nextCursor":"turn-cursor"}),
    );
    let q = v.items_page("turn", None, Direction::Asc).unwrap();
    accept(&mut v, &q, json!({"data":[],"nextCursor":"item-cursor"}));
    assert!(v.turns_page(Some("item-cursor"), Direction::Desc).is_err());
    assert!(v
        .items_page("turn", Some("turn-cursor"), Direction::Asc)
        .is_err());
    assert_eq!(
        v.items_page("turn", Some("item-cursor"), Direction::Asc)
            .unwrap()
            .params()["cursor"],
        "item-cursor"
    );
}
#[test]
fn foreign_full_tuple_selection_and_factory_results_cannot_mutate_this_view() {
    let mut v = selected();
    let q = v.read_metadata().unwrap();
    let before = v.snapshot();
    for foreign in [
        json!(1),
        json!({"appSession":"foreign","home":"history-home","spawnCounter":1}),
        json!({"appSession":"history-session","home":"other","spawnCounter":1}),
        json!({"appSession":"history-session","home":"history-home","spawnCounter":2}),
    ] {
        assert!(v
            .receive(
                &q,
                "history-home",
                &foreign,
                &json!({"thread":thread("thread","notLoaded")})
            )
            .is_err());
        assert_eq!(v.snapshot(), before);
    }
    assert!(v
        .receive(
            &q,
            "other",
            &g(),
            &json!({"thread":thread("thread","notLoaded")})
        )
        .is_err());
    assert_eq!(v.snapshot(), before);
    let mut another = selected();
    let foreign_query = another.read_metadata().unwrap();
    assert!(v
        .receive(
            &foreign_query,
            "history-home",
            &g(),
            &json!({"thread":thread("thread","notLoaded")})
        )
        .is_err());
    assert_eq!(v.snapshot(), before);
    v.select("second").unwrap();
    let before = v.snapshot();
    assert!(v
        .receive(
            &q,
            "history-home",
            &g(),
            &json!({"thread":thread("thread","notLoaded")})
        )
        .is_err());
    assert_eq!(v.snapshot(), before);
}
#[test]
fn schema_and_relational_identity_refusals_are_atomic_with_native_extras_preserved() {
    let mut v = selected();
    let q = v.read_metadata().unwrap();
    let before = v.snapshot();
    assert!(v
        .receive(
            &q,
            "history-home",
            &g(),
            &json!({"thread":thread("wrong","notLoaded")})
        )
        .is_err());
    assert!(v
        .receive(&q, "history-home", &g(), &json!({"thread":{"id":"thread"}}))
        .is_err());
    assert_eq!(v.snapshot(), before);
    let native = json!({"thread":thread("thread","notLoaded"),"extraTop":"native"});
    accept(&mut v, &q, native.clone());
    assert_eq!(v.snapshot()["selected"]["metadata"], native);
    let mut v = view();
    let q = v.list_threads(None, Direction::Desc).unwrap();
    let before = v.snapshot();
    assert!(v
        .receive(
            &q,
            "history-home",
            &g(),
            &json!({"data":[thread("valid","notLoaded"),thread("","notLoaded")]})
        )
        .is_err());
    assert_eq!(v.snapshot(), before);
}

#[test]
fn malformed_native_history_diagnostics_never_include_rejected_payload() {
    let mut v = selected();
    let metadata = v.read_metadata().unwrap();
    let before = v.snapshot();
    let private = "invented-native-content-not-for-diagnostics";
    let mut invalid = json!({"thread":thread("thread","notLoaded")});
    invalid["thread"]["preview"] = json!({"private":private});
    let error = v.receive(&metadata, "history-home", &g(), &invalid).unwrap_err();
    assert!(error.starts_with("native history schema refused ThreadReadResponse:"));
    assert!(!error.contains(private), "the diagnostic may become a durable reading limit");
    assert_eq!(v.snapshot(), before, "refusal stays atomic");

    let turns = v.turns_page(None, Direction::Desc).unwrap();
    accept(&mut v, &turns, json!({"data":[turn("turn","completed","summary")]}));
    let items = v.items_page("turn", None, Direction::Asc).unwrap();
    let before = v.snapshot();
    let invalid = json!({"data":[{"turnId":"turn","item":{"type":"agentMessage","id":"task","content":[{"type":"encrypted_content","encrypted_content":private}]}}],"nextCursor":null});
    let error = v.receive(&items, "history-home", &g(), &invalid).unwrap_err();
    assert!(error.starts_with("native history schema refused ThreadItemsListResponse:"));
    assert!(!error.contains(private));
    assert_eq!(v.snapshot(), before);
}
#[test]
fn goals_missing_null_and_value_keep_their_native_availability() {
    let mut v = selected();
    let q = v.read_goal().unwrap();
    accept(&mut v, &q, json!({}));
    assert_eq!(v.snapshot()["selected"]["goalAvailability"], "not-reported");
    let q = v.read_goal().unwrap();
    accept(&mut v, &q, json!({"goal":null}));
    assert_eq!(
        v.snapshot()["selected"]["goalAvailability"],
        "no-goal-reported"
    );
    let goal = json!({"threadId":"thread","objective":"invented","status":"complete","createdAt":1,"updatedAt":2,"tokensUsed":3,"timeUsedSeconds":4,"tokenBudget":null});
    let q = v.read_goal().unwrap();
    accept(&mut v, &q, json!({"goal":goal}));
    assert_eq!(v.snapshot()["selected"]["goal"]["goal"], goal);
    assert_eq!(v.snapshot()["selected"]["state"], "indexed-read-only");
}
#[test]
fn explicit_resume_success_error_wait_and_generation_close_have_separate_meanings() {
    let mut v = selected();
    let q = v.continue_query().unwrap();
    v.waiting_ended(&q).unwrap();
    assert_eq!(v.snapshot()["pending"][0]["waitingEnded"], true);
    assert_eq!(v.resumed_thread(), None);
    let error = json!({"code":-32600,"message":"native refusal","data":{"extra":"preserved"}});
    v.receive_error(&q, "history-home", &g(), &error).unwrap();
    assert_eq!(v.snapshot()["selected"]["error"]["error"], error);
    assert_eq!(v.resumed_thread(), None);
    let q = v.continue_query().unwrap();
    accept(&mut v, &q, resume("thread", "active"));
    let binding = v.resumed_thread().unwrap();
    assert_eq!(binding["generation"], g());
    assert_eq!(binding["home"], "history-home");
    assert_eq!(
        binding["native"]["status"]["activeFlags"],
        json!(["waitingOnUserInput"])
    );
    assert_eq!(v.snapshot()["activeBindingPerformed"], false);
    let q = v.read_goal().unwrap();
    assert!(v.close_generation(&json!(1)).is_err());
    v.close_generation(&g()).unwrap();
    assert_eq!(v.resumed_thread(), None);
    assert_eq!(v.snapshot()["selected"], Value::Null);
    assert_eq!(v.snapshot()["threads"], json!([]));
    assert!(v
        .receive(&q, "history-home", &g(), &json!({"goal":null}))
        .is_err());
    assert!(v.continue_query().is_err());
}
#[test]
fn item_turn_anchors_and_known_child_reads_keep_owner_and_do_not_infer_child_completion() {
    let mut v = selected();
    assert!(v.read_child("arbitrary-child").is_err());
    let q = v.turns_page(None, Direction::Desc).unwrap();
    accept(
        &mut v,
        &q,
        json!({"data":[turn("turn","completed","summary"),turn("second-turn","completed","summary")]}),
    );
    let q = v.items_page("turn", None, Direction::Asc).unwrap();
    let plan = json!({"id":"same-item-id","type":"plan","text":"invented completed plan","nativeExtra":true});
    let spawn = json!({"id":"spawn","type":"collabAgentToolCall","tool":"spawnAgent","status":"completed","senderThreadId":"thread","receiverThreadIds":["child"],"agentsStates":{}});
    let page = json!({"data":[{"turnId":"turn","item":plan,"completedAtMs":null},{"turnId":"turn","item":spawn,"completedAtMs":null}],"nextCursor":null});
    accept(&mut v, &q, page.clone());
    assert_eq!(v.snapshot()["selected"]["itemsPage"], page);
    assert_eq!(
        v.snapshot()["selected"]["knownChildren"][0]["parentSource"],
        "collabAgentToolCall.senderThreadId"
    );
    let child = v.read_child("child").unwrap();
    assert_eq!(
        child.params(),
        &json!({"threadId":"child","includeTurns":false})
    );
    let mut child_thread = thread("child", "active");
    child_thread["status"] = json!({"type":"active","activeFlags":[]});
    child_thread["parentThreadId"] = json!("thread");
    accept(&mut v, &child, json!({"thread":child_thread.clone()}));
    assert_eq!(
        v.snapshot()["selected"]["childReads"]["child"]["native"]["thread"],
        child_thread
    );
    assert_eq!(
        v.snapshot()["selected"]["childReads"]["child"]["appRole"]["standing"],
        "unknown"
    );
    assert_eq!(v.resumed_thread(), None);
    let q = v.items_page("second-turn", None, Direction::Asc).unwrap();
    let before = v.snapshot();
    assert!(v
        .receive(
            &q,
            "history-home",
            &g(),
            &json!({"data":[{"turnId":"turn","item":plan}]})
        )
        .is_err());
    assert_eq!(v.snapshot(), before);
    accept(
        &mut v,
        &q,
        json!({"data":[{"turnId":"second-turn","item":plan}]}),
    );
    assert_eq!(
        v.snapshot()["selected"]["itemsPage"]["data"][0]["turnId"],
        "second-turn"
    );
}

#[test]
fn newer_thread_state_and_pending_continue_invalidate_prior_resume_eligibility() {
    let mut v = selected();
    let q = v.continue_query().unwrap();
    accept(&mut v, &q, resume("thread", "idle"));
    assert!(v.resumed_thread().is_some());
    let read = v.read_metadata().unwrap();
    assert_eq!(v.resumed_thread(), None);
    let mut unloaded = thread("thread", "notLoaded");
    unloaded["canAcceptDirectInput"] = json!(false);
    let native = json!({"thread":unloaded});
    accept(&mut v, &read, native.clone());
    assert_eq!(v.resumed_thread(), None);
    assert_eq!(v.snapshot()["selected"]["metadata"], native);
    assert_eq!(v.snapshot()["selected"]["state"], "indexed-read-only");
    let q = v.continue_query().unwrap();
    accept(&mut v, &q, resume("thread", "idle"));
    assert!(v.resumed_thread().is_some());
    let pending = v.continue_query().unwrap();
    assert_eq!(v.resumed_thread(), None);
    v.waiting_ended(&pending).unwrap();
    assert_eq!(v.resumed_thread(), None);
    accept(&mut v, &pending, resume("thread", "idle"));
    assert!(v.resumed_thread().is_some());
    // Superseded pending metadata must not block a later completed Resume.
    let old = v.read_metadata().unwrap();
    let current = v.continue_query().unwrap();
    accept(&mut v, &current, resume("thread", "idle"));
    assert!(v.resumed_thread().is_some());
    let before = v.snapshot();
    assert!(v
        .receive(
            &old,
            "history-home",
            &g(),
            &json!({"thread":thread("thread","notLoaded")})
        )
        .is_err());
    assert_eq!(v.snapshot(), before);
}
#[test]
fn same_stream_goal_success_resolves_failure_but_keeps_raw_error_history() {
    let mut v = selected();
    let failed = v.read_goal().unwrap();
    let error =
        json!({"code":-32600,"message":"goal read refused","data":{"nativeExtra":"preserved"}});
    v.receive_error(&failed, "history-home", &g(), &error)
        .unwrap();
    assert_eq!(v.snapshot()["selected"]["state"], "unavailable");
    assert_eq!(v.snapshot()["selected"]["goalAvailability"], "unavailable");
    let recovered = v.read_goal().unwrap();
    accept(&mut v, &recovered, json!({"goal":null,"nativeExtra":true}));
    let snapshot = v.snapshot();
    assert_eq!(snapshot["selected"]["state"], "indexed-read-only");
    assert_eq!(snapshot["selected"]["error"], Value::Null);
    assert_eq!(snapshot["selected"]["errorsByStream"], json!({}));
    assert_eq!(snapshot["selected"]["goalAvailability"], "no-goal-reported");
    assert_eq!(snapshot["selected"]["errorHistory"][0]["error"], error);
    assert_eq!(
        snapshot["selected"]["streamResolutions"]["goal"]["query"]["query_id"],
        recovered.id()
    );
    assert_eq!(
        snapshot["selected"]["streamResolutions"]["goal"]["outcome"],
        "native-result-observed"
    );
}
#[test]
fn unrelated_metadata_success_cannot_erase_goal_failure_or_its_query_binding() {
    let mut v = selected();
    let failed = v.read_goal().unwrap();
    let error = json!({"code":-32600,"message":"goal unavailable"});
    v.receive_error(&failed, "history-home", &g(), &error)
        .unwrap();
    let metadata = v.read_metadata().unwrap();
    accept(
        &mut v,
        &metadata,
        json!({"thread":thread("thread","notLoaded")}),
    );
    let snapshot = v.snapshot();
    assert_eq!(snapshot["selected"]["state"], "unavailable");
    assert_eq!(snapshot["selected"]["error"]["error"], error);
    assert_eq!(
        snapshot["selected"]["errorsByStream"]["goal"]["query"]["query_id"],
        failed.id()
    );
    assert_eq!(
        snapshot["selected"]["streamResolutions"]["thread-state"]["outcome"],
        "native-result-observed"
    );
    assert_eq!(
        snapshot["selected"]["streamResolutions"]["goal"]["outcome"],
        "native-error-observed"
    );
}
#[test]
fn only_completed_spawn_establishes_child_edge_other_calls_preserve_references() {
    let mut v = selected();
    let q = v.turns_page(None, Direction::Desc).unwrap();
    accept(
        &mut v,
        &q,
        json!({"data":[turn("turn","completed","summary")]}),
    );
    for (tool, status, id) in [
        ("spawnAgent", "inProgress", "pending-child"),
        ("spawnAgent", "failed", "failed-child"),
        ("sendInput", "completed", "receiver"),
        ("wait", "completed", "wait-receiver"),
        ("closeAgent", "completed", "closed-receiver"),
        ("resumeAgent", "completed", "resumed-receiver"),
    ] {
        let q = v.items_page("turn", None, Direction::Asc).unwrap();
        let call = json!({"id":"call","type":"collabAgentToolCall","tool":tool,"status":status,"senderThreadId":"thread","receiverThreadIds":[id],"agentsStates":{}});
        let page = json!({"data":[{"turnId":"turn","item":call}]});
        accept(&mut v, &q, page.clone());
        assert_eq!(v.snapshot()["selected"]["itemsPage"], page);
        assert!(v.read_child(id).is_err());
        assert_eq!(v.snapshot()["selected"]["knownChildren"], json!([]));
        assert!(v.snapshot()["selected"]["receiverReferences"]
            .as_array()
            .unwrap()
            .iter()
            .any(|r| r["threadId"] == id && r["tool"] == tool));
    }
    let q = v.items_page("turn", None, Direction::Asc).unwrap();
    let spawn = json!({"id":"spawn","type":"collabAgentToolCall","tool":"spawnAgent","status":"completed","senderThreadId":"thread","receiverThreadIds":["child"],"agentsStates":{}});
    accept(&mut v, &q, json!({"data":[{"turnId":"turn","item":spawn}]}));
    let original = v.snapshot()["selected"]["knownChildren"][0].clone();
    assert_eq!(original["edgeEvidence"], "completed spawnAgent");
    assert!(v.read_child("child").is_ok());
    let q = v.items_page("turn", None, Direction::Asc).unwrap();
    let update = json!({"id":"later","type":"collabAgentToolCall","tool":"sendInput","status":"completed","senderThreadId":"different-sender","receiverThreadIds":["child","unestablished"],"agentsStates":{}});
    accept(
        &mut v,
        &q,
        json!({"data":[{"turnId":"turn","item":update}]}),
    );
    let child = v.snapshot()["selected"]["knownChildren"][0].clone();
    for key in [
        "parentThreadId",
        "parentSource",
        "sourceItemId",
        "edgeEvidence",
    ] {
        assert_eq!(child[key], original[key]);
    }
    assert_eq!(child["lastObservedReference"]["sourceItemId"], "later");
    assert!(v.read_child("unestablished").is_err());
    assert_eq!(v.snapshot()["selected"]["appRole"]["standing"], "unknown");
}
#[test]
fn child_stream_failure_is_not_erased_by_goal_and_its_own_success_clears_only_current_error() {
    let mut v = selected();
    let q = v.turns_page(None, Direction::Desc).unwrap();
    accept(
        &mut v,
        &q,
        json!({"data":[turn("turn","completed","summary")]}),
    );
    let q = v.items_page("turn", None, Direction::Asc).unwrap();
    let spawn = json!({"id":"spawn","type":"collabAgentToolCall","tool":"spawnAgent","status":"completed","senderThreadId":"thread","receiverThreadIds":["child"],"agentsStates":{}});
    accept(&mut v, &q, json!({"data":[{"turnId":"turn","item":spawn}]}));
    let failed = v.read_child("child").unwrap();
    let error = json!({"code":-32600,"message":"child read unavailable","data":{"nativeExtra":"preserved"}});
    v.receive_error(&failed, "history-home", &g(), &error)
        .unwrap();
    let goal = v.read_goal().unwrap();
    accept(&mut v, &goal, json!({"goal":null}));
    assert_eq!(
        v.snapshot()["selected"]["errorsByStream"]["child:child"]["error"],
        error
    );
    assert_eq!(v.snapshot()["selected"]["state"], "unavailable");
    let recovered = v.read_child("child").unwrap();
    let mut metadata = thread("child", "idle");
    metadata["parentThreadId"] = json!("different-reported-parent");
    accept(&mut v, &recovered, json!({"thread":metadata.clone()}));
    let snapshot = v.snapshot();
    assert_eq!(snapshot["selected"]["errorsByStream"], json!({}));
    assert_eq!(snapshot["selected"]["errorHistory"][0]["error"], error);
    assert_eq!(snapshot["selected"]["state"], "indexed-read-only");
    assert_eq!(
        snapshot["selected"]["childReads"]["child"]["native"]["thread"],
        metadata
    );
    assert_eq!(
        snapshot["selected"]["knownChildren"][0]["parentThreadId"],
        "thread"
    );
    assert_eq!(snapshot["selected"]["appRole"]["standing"], "unknown");
    assert_eq!(v.resumed_thread(), None);
}

#[test]
fn current_started_activity_can_request_only_native_child_metadata() {
    let mut v = selected();
    let q = v.turns_page(None, Direction::Desc).unwrap();
    accept(
        &mut v,
        &q,
        json!({"data":[turn("turn","completed","summary")]}),
    );
    let q = v.items_page("turn", None, Direction::Asc).unwrap();
    let item = json!({"id":"current-start","type":"subAgentActivity","kind":"started","agentPath":"/root/task","agentThreadId":"current-child"});
    accept(
        &mut v,
        &q,
        json!({"data":[{"turnId":"turn","item":item,"completedAtMs":1}]}),
    );
    let discovered = v.snapshot()["selected"]["knownChildren"][0].clone();
    assert!(discovered.get("parentThreadId").is_none());
    assert_eq!(discovered["sourceQuery"], serde_json::to_value(&q).unwrap());
    assert_eq!(discovered["sourceThreadId"], "thread");
    assert_eq!(discovered["sourceTurnId"], "turn");
    assert_eq!(discovered["sourceItemId"], "current-start");
    let child = v
        .read_child("current-child")
        .expect("current native started reference must reach its metadata read");
    assert_eq!(child.method(), "thread/read");
    assert_eq!(
        child.params(),
        &json!({"threadId":"current-child","includeTurns":false})
    );
    let mut native = thread("current-child", "active");
    native["status"] = json!({"type":"active","activeFlags":[]});
    native["parentThreadId"] = json!("thread");
    accept(&mut v, &child, json!({"thread":native.clone()}));
    let snapshot = v.snapshot();
    assert_eq!(
        snapshot["selected"]["childReads"]["current-child"]["native"]["thread"],
        native
    );
    assert_eq!(
        snapshot["selected"]["childReads"]["current-child"]["appRole"]["standing"],
        "unknown"
    );
    assert_eq!(
        snapshot["selected"]["childReads"]["current-child"]["parentRelationship"]["standing"],
        "native-parent-confirmed"
    );
    assert_eq!(
        snapshot["selected"]["knownChildren"][0]["parentThreadId"],
        "thread"
    );
    assert_eq!(v.resumed_thread(), None);
    assert_eq!(snapshot["activeBindingPerformed"], false);
}

fn current_history() -> NativeHistory {
    let mut v = selected();
    let q = v.turns_page(None, Direction::Desc).unwrap();
    accept(
        &mut v,
        &q,
        json!({"data":[turn("turn","completed","summary")]}),
    );
    v
}
fn activity(v: &mut NativeHistory, id: &str, kind: &str, child: &str, path: &str) -> HistoryQuery {
    let q = v.items_page("turn", None, Direction::Asc).unwrap();
    accept(
        v,
        &q,
        json!({"data":[{"turnId":"turn","item":{"id":id,"type":"subAgentActivity","kind":kind,"agentPath":path,"agentThreadId":child},"completedAtMs":1}]}),
    );
    q
}
#[test]
fn current_non_started_root_self_and_empty_references_do_not_enable_child_reads() {
    let mut v = current_history();
    for (item, kind, child, path) in [
        ("interacted", "interacted", "receiver", "/root/receiver"),
        (
            "interrupted",
            "interrupted",
            "interrupted",
            "/root/interrupted",
        ),
        ("completed", "completed", "completed", "/root/completed"),
        ("root", "started", "root", "/root"),
        ("self", "started", "thread", "/root/self"),
        ("empty", "started", "", "/root/empty"),
        ("", "started", "empty-item", "/root/empty-item"),
    ] {
        activity(&mut v, item, kind, child, path);
        assert!(v.read_child(child).is_err(), "{item}");
    }
    assert_eq!(v.snapshot()["selected"]["knownChildren"], json!([]));
    activity(&mut v, "without-path", "started", "without-path", "");
    assert!(
        v.read_child("without-path").is_ok(),
        "an opaque path does not replace the reported thread identity"
    );
}
#[test]
fn current_parent_metadata_missing_wrong_or_conflicting_keeps_edge_unknown() {
    let mut v = current_history();
    activity(&mut v, "start", "started", "child", "/root/task");
    for parent in [None, Some("wrong-parent"), Some("thread")] {
        let q = v.read_child("child").unwrap();
        let mut native = thread("child", "idle");
        if let Some(parent) = parent {
            native["parentThreadId"] = json!(parent);
        }
        if parent == Some("thread") {
            native["source"] = json!({"subAgent":{"thread_spawn":{"depth":1,"parent_thread_id":"conflicting-parent"}}});
        }
        accept(&mut v, &q, json!({"thread":native.clone()}));
        let snapshot = v.snapshot();
        let row = &snapshot["selected"]["knownChildren"][0];
        assert!(row.get("parentThreadId").is_none());
        assert!(row["parentLimit"].is_string());
        assert_eq!(
            snapshot["selected"]["childReads"]["child"]["native"]["thread"],
            native
        );
        assert_eq!(
            snapshot["selected"]["childReads"]["child"]["parentRelationship"]["standing"],
            "unknown"
        );
        assert_eq!(
            snapshot["selected"]["childReads"]["child"]["appRole"]["standing"],
            "unknown"
        );
    }
}
#[test]
fn current_source_survives_later_activity_and_conflicting_started_paths_stay_unknown() {
    let mut v = current_history();
    let original_query = activity(&mut v, "start", "started", "child", "/root/task");
    let original = v.snapshot()["selected"]["knownChildren"][0].clone();
    let pending = v.read_child("child").unwrap();
    activity(&mut v, "interaction", "interacted", "child", "/root/task");
    let mut native = thread("child", "idle");
    native["parentThreadId"] = json!("thread");
    accept(&mut v, &pending, json!({"thread":native.clone()}));
    assert_eq!(
        v.snapshot()["selected"]["childReads"]["child"]["parentRelationship"]["standing"],
        "native-parent-confirmed"
    );
    activity(&mut v, "same-path", "started", "child", "/root/task");
    let pending = v.read_child("child").unwrap();
    activity(
        &mut v,
        "different-path",
        "started",
        "child",
        "/root/different",
    );
    accept(&mut v, &pending, json!({"thread":native}));
    let snapshot = v.snapshot();
    let row = &snapshot["selected"]["knownChildren"][0];
    for field in [
        "sourceThreadId",
        "sourceTurnId",
        "sourceItemId",
        "sourceQuery",
        "sourceRevision",
        "agentPath",
    ] {
        assert_eq!(row[field], original[field]);
    }
    assert_eq!(
        row["sourceQuery"],
        serde_json::to_value(original_query).unwrap()
    );
    assert_eq!(
        row["lastObservedReference"]["sourceItemId"],
        "different-path"
    );
    assert!(row.get("parentThreadId").is_none());
    assert_eq!(
        snapshot["selected"]["childReads"]["child"]["parentRelationship"]["standing"],
        "unknown"
    );
    assert!(v.read_child("child").is_err());
}

#[test]
fn current_copied_ancestor_rows_and_new_parent_evidence_never_confirm_child_edges() {
    let mut v = current_history();
    activity(
        &mut v,
        "before-metadata",
        "started",
        "parent",
        "/root/parent",
    );
    let pending = v.read_child("parent").unwrap();
    let q = v.read_metadata().unwrap();
    let mut own = thread("thread", "idle");
    own["parentThreadId"] = json!("parent");
    own["source"] = json!({"subAgent":{"thread_spawn":{"depth":2,"parent_thread_id":"parent","agent_path":"/root/parent/selected"}}});
    accept(&mut v, &q, json!({"thread":own}));
    let mut parent = thread("parent", "idle");
    parent["parentThreadId"] = json!("thread");
    accept(&mut v, &pending, json!({"thread":parent}));
    assert_eq!(
        v.snapshot()["selected"]["childReads"]["parent"]["parentRelationship"]["standing"],
        "unknown"
    );
    assert!(v.read_child("parent").is_err());
    // An omitted later parent is a limit, not erasure of the observed ancestor.
    let q = v.read_metadata().unwrap();
    accept(&mut v, &q, json!({"thread":thread("thread", "idle")}));
    assert!(v.read_child("parent").is_err());
    activity(
        &mut v,
        "copied-parent",
        "started",
        "parent",
        "/root/some-path",
    );
    assert!(v.read_child("parent").is_err());
    let q = v.read_metadata().unwrap();
    let mut own = thread("thread", "idle");
    own["source"] = json!({"subAgent":{"thread_spawn":{"depth":3,"parent_thread_id":"parent","agent_path":"/root/ancestor/parent/selected"}}});
    accept(&mut v, &q, json!({"thread":own}));
    activity(
        &mut v,
        "copied-ancestor",
        "started",
        "ancestor",
        "/root/ancestor",
    );
    assert!(v.read_child("ancestor").is_err());
}

#[test]
fn current_child_metadata_errors_and_scope_changes_preserve_source_and_unknown_role() {
    let mut v = current_history();
    activity(&mut v, "start", "started", "child", "/root/task");
    let q = v.read_child("child").unwrap();
    let error = json!({"code":-32000,"message":"child metadata unavailable"});
    v.receive_error(&q, "history-home", &g(), &error).unwrap();
    let unrelated = v.read_goal().unwrap();
    accept(&mut v, &unrelated, json!({"goal":null}));
    assert_eq!(
        v.snapshot()["selected"]["errorsByStream"]["child:child"]["error"],
        error
    );
    let q = v.read_child("child").unwrap();
    let mut native = thread("child", "idle");
    native["parentThreadId"] = json!("thread");
    let reply = json!({"thread":native});
    assert!(v.receive(&q, "other-home", &g(), &reply).is_err());
    let mut stale = g();
    stale["spawnCounter"] = json!(2);
    assert!(v.receive(&q, "history-home", &stale, &reply).is_err());
    let superseding = v.read_child("child").unwrap();
    assert!(v.receive(&q, "history-home", &g(), &reply).is_err());
    let before = v.snapshot();
    let mut wrong = reply.clone();
    wrong["thread"]["id"] = json!("different-native-child");
    assert!(v
        .receive(&superseding, "history-home", &g(), &wrong)
        .is_err());
    assert_eq!(v.snapshot(), before);
    accept(&mut v, &superseding, reply.clone());
    assert_eq!(v.snapshot()["selected"]["errorsByStream"], json!({}));
    assert_eq!(
        v.snapshot()["selected"]["childReads"]["child"]["appRole"]["standing"],
        "unknown"
    );
    let q = v.read_child("child").unwrap();
    v.select("second").unwrap();
    assert!(v.receive(&q, "history-home", &g(), &reply).is_err());
    v.select("thread").unwrap();
    assert!(v.read_child("child").is_err());
}

#[test]
fn path_ancestor_exclusion_survives_optional_path_omission_before_any_candidate() {
    let mut v = current_history();
    let q = v.read_metadata().unwrap();
    let mut own = thread("thread", "idle");
    own["parentThreadId"] = json!("parent");
    own["source"] = json!({"subAgent":{"thread_spawn":{"depth":3,"parent_thread_id":"parent","agent_path":"/root/ancestor/parent/selected"}}});
    accept(&mut v, &q, json!({"thread":own}));
    activity(
        &mut v,
        "ancestor-first",
        "started",
        "ancestor",
        "/root/ancestor",
    );
    assert!(v.read_child("ancestor").is_err());
    assert_eq!(v.snapshot()["selected"]["knownChildren"], json!([]));
    let q = v.read_metadata().unwrap();
    let mut own = thread("thread", "idle");
    own["parentThreadId"] = json!("parent");
    own["source"] = json!({"subAgent":{"thread_spawn":{"depth":3,"parent_thread_id":"parent"}}});
    accept(&mut v, &q, json!({"thread":own}));
    activity(
        &mut v,
        "ancestor-again",
        "started",
        "ancestor",
        "/root/ancestor",
    );
    assert!(v.read_child("ancestor").is_err());
    assert_eq!(v.snapshot()["selected"]["knownChildren"], json!([]));
}

#[test]
fn initially_empty_started_path_does_not_hide_later_conflicting_known_paths() {
    let mut v = current_history();
    activity(&mut v, "original-empty", "started", "child", "");
    let original = v.snapshot()["selected"]["knownChildren"][0].clone();
    let pending = v.read_child("child").unwrap();
    activity(&mut v, "first-known", "started", "child", "/root/first");
    activity(&mut v, "second-known", "started", "child", "/root/second");
    let mut native = thread("child", "idle");
    native["parentThreadId"] = json!("thread");
    accept(&mut v, &pending, json!({"thread":native}));
    let snapshot = v.snapshot();
    let child = &snapshot["selected"]["knownChildren"][0];
    assert_eq!(child["sourceQuery"], original["sourceQuery"]);
    assert_eq!(child["sourceItemId"], "original-empty");
    assert_eq!(child["agentPath"], "");
    assert!(child.get("parentThreadId").is_none());
    assert!(child["discoveryLimit"].is_string());
    assert_eq!(
        snapshot["selected"]["childReads"]["child"]["parentRelationship"]["standing"],
        "unknown"
    );
    assert!(v.read_child("child").is_err());
}
