// Genuine Host replies through the manual stored-history receiving seam.
use super::*;
use crate::native_history::Direction;
use crate::runtime_session::HomeSession;

struct ManualHistory {
    pipe: NativePagePipe,
    home: HomeSession,
}
impl ManualHistory {
    fn new() -> Self {
        Self::with_received_view(true)
    }
    fn with_received_view(receive: bool) -> Self {
        let pipe = NativePagePipe::new();
        let home = HomeSession::new(
            crate::home_resources::HomeClass::Account,
            Arc::clone(&pipe.host),
            Err("synthetic manual-history pipe".into()),
        )
        .unwrap();
        if receive {
            home.runtime.lock().unwrap().receive_native(&home.host);
        }
        let mut fixture = Self { pipe, home };
        let list = fixture.query("list", None, Direction::Asc);
        fixture.setup(
            &list,
            json!({"data":[history_thread("notLoaded")],"nextCursor":null}),
        );
        fixture
            .home
            .history
            .lock()
            .unwrap()
            .select(&fixture.home.host.snapshot(), &g(), 0, "stored")
            .unwrap();
        let turns = fixture.query("turns", None, Direction::Asc);
        fixture.setup(
            &turns,
            json!({"data":[
            {"id":"turn-a","status":"completed","items":[],"itemsView":"summary","error":null},
            {"id":"turn-b","status":"completed","items":[],"itemsView":"summary","error":null}
        ],"nextCursor":null}),
        );
        fixture
    }
    fn query(&self, action: &str, reference: Option<&str>, direction: Direction) -> HistoryQuery {
        let mut history = self.home.history.lock().unwrap();
        history.reconcile(&self.home.host);
        let epoch = history.snapshot(None)["selectionEpoch"].as_u64().unwrap();
        history
            .prepare(
                &self.home.host.snapshot(),
                &g(),
                epoch,
                action,
                None,
                direction,
                reference,
            )
            .unwrap()
    }
    fn setup(&mut self, query: &HistoryQuery, result: Value) {
        let dispatch = self.pipe.dispatch(query, &result);
        let mut history = self.home.history.lock().unwrap();
        history.dispatched(dispatch);
        history.reconcile(&self.home.host);
    }
    fn manual(&mut self, query: &HistoryQuery, result: &Value) -> HistoryDispatch {
        let dispatch = self.begin_manual(query);
        self.pipe.reply(&dispatch, result);
        dispatch
    }
    fn begin_manual(&self, query: &HistoryQuery) -> HistoryDispatch {
        let dispatch = self.home.host.history_dispatch(query).unwrap();
        self.home
            .history
            .lock()
            .unwrap()
            .dispatched_manual(dispatch.clone());
        dispatch
    }
    fn finish(&self, dispatch: &HistoryDispatch) -> Value {
        let evidence = self
            .home
            .host
            .history_wait(dispatch, Duration::from_millis(20))
            .unwrap();
        self.home.reconcile_manual_history();
        evidence
    }
    fn projection(&self) -> (Value, Value) {
        let mut runtime = self.home.runtime.lock().unwrap();
        let (_, received) = runtime.receive_native(&self.home.host);
        (runtime.native_view(), received["observerRecovery"].clone())
    }
}
fn plan_entry(turn: &str, id: &str) -> Value {
    json!({"turnId":turn,"item":{"id":id,"type":"plan","text":format!("native plan {id}")}})
}
fn child_entry() -> Value {
    json!({"turnId":"turn-a","item":{"id":"spawn","type":"subAgentActivity","kind":"started","agentThreadId":"native-child","agentPath":"/root/child"}})
}
fn assert_recovered_only(view: &Value) {
    assert!(view["items"]
        .as_array()
        .unwrap()
        .iter()
        .all(|row| row["standing"] == "recovered-from-supplier"
            && row.get("sourceFrame").is_none()
            && row.get("receipt").is_none()
            && row.get("requestRef").is_none()));
    assert!(view["revisions"]
        .as_array()
        .unwrap()
        .iter()
        .all(|revision| revision["kind"] == "plan-item"
            && revision["standing"] == "recovered-from-supplier"));
    assert_eq!(view["checklistGaps"], json!([]));
}

#[test]
fn history_bridge_manual_wrong_turn_never_projects_before_acceptance() {
    let mut f = ManualHistory::new();
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    let raw = json!({"data":[plan_entry("turn-b", "foreign-plan")],"nextCursor":null});
    let dispatch = f.manual(&query, &raw);
    let before = f.projection();
    let evidence = f.finish(&dispatch);
    assert_eq!(
        evidence["response"]["result"], raw,
        "raw genuine reply is retained"
    );
    let history = f.home.history.lock().unwrap().snapshot(None);
    assert!(history["receivingLimits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|limit| limit
            .as_str()
            .unwrap()
            .contains("native item turn identity differs")));
    assert_eq!(
        f.projection(),
        before,
        "a refused page must not change native content or history counters"
    );
}

#[test]
fn history_bridge_manual_schema_valid_semantic_failure_is_atomic() {
    let mut f = ManualHistory::new();
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    let raw = json!({"data":[plan_entry("turn-a", "valid-first"),child_entry(),plan_entry("turn-a", "")],"nextCursor":null});
    let dispatch = f.manual(&query, &raw);
    let before = f.projection();
    f.finish(&dispatch);
    assert_eq!(
        f.home.history.lock().unwrap().snapshot(None)["selected"]["itemsPage"],
        raw,
        "the pinned schema permits an empty item ID; browser acceptance remains separate"
    );
    assert_eq!(
        f.projection(),
        before,
        "a later semantic refusal must roll back the entire native page and its counter"
    );
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    let dispatch = f.manual(
        &query,
        &json!({"data":[plan_entry("turn-a", "after-refusal")],"nextCursor":null}),
    );
    f.finish(&dispatch);
    let (view, counters) = f.projection();
    assert_eq!(
        view["items"][0]["observedOrder"], 0,
        "failed application must not consume the hidden next_order counter"
    );
    assert_eq!(counters["historyPagesRead"], 1);
    assert_eq!(counters["recoveryPagesRead"], 0);
}

#[test]
fn history_bridge_manual_malformed_superseded_and_closed_replies_do_not_project() {
    for change in ["malformed", "selection", "query", "closed"] {
        let mut f = ManualHistory::new();
        let query = f.query("items", Some("turn-a"), Direction::Asc);
        let mut raw = json!({"data":[plan_entry("turn-a", "must-stay-out")],"nextCursor":null});
        if change == "malformed" {
            raw["data"][0]["item"]
                .as_object_mut()
                .unwrap()
                .remove("text");
        }
        let dispatch = f.manual(&query, &raw);
        let before = f.projection();
        match change {
            "selection" => f
                .home
                .history
                .lock()
                .unwrap()
                .select(&f.home.host.snapshot(), &g(), 1, "stored")
                .unwrap(),
            "query" => {
                f.home
                    .history
                    .lock()
                    .unwrap()
                    .history_mut()
                    .unwrap()
                    .items_page("turn-a", None, Direction::Asc)
                    .unwrap();
            }
            "closed" => {
                Host::close_generation(&mut f.home.host.inner.0.lock().unwrap());
            }
            _ => (),
        }
        let evidence = f.finish(&dispatch);
        assert_eq!(evidence["response"]["result"], raw);
        assert_eq!(
            f.projection(),
            before,
            "{change}: rejected content and counters must remain unchanged"
        );
        if change != "closed" {
            assert!(
                !f.home.history.lock().unwrap().snapshot(None)["receivingLimits"]
                    .as_array()
                    .unwrap()
                    .is_empty(),
                "{change}: refusal is inspectable"
            );
        } else {
            assert_eq!(evidence["sourceCurrent"], false);
        }
    }
}

#[test]
fn history_bridge_manual_accepted_pages_survive_prior_reconcile_and_deliver_once_in_order() {
    let mut f = ManualHistory::new();
    let first = f.query("items", Some("turn-a"), Direction::Asc);
    let dispatch = f.manual(&first, &json!({"data":[plan_entry("turn-a", "one"),plan_entry("turn-a", "two")],"nextCursor":null}));
    f.home.history.lock().unwrap().reconcile(&f.home.host);
    let second = f.query("items", Some("turn-a"), Direction::Desc);
    let last = f.manual(&second, &json!({"data":[plan_entry("turn-a", "four"),plan_entry("turn-a", "three")],"nextCursor":null}));
    f.home.history.lock().unwrap().reconcile(&f.home.host);
    f.home
        .history
        .lock()
        .unwrap()
        .select(&f.home.host.snapshot(), &g(), 1, "stored")
        .unwrap();
    assert_eq!(f.projection().1["historyPagesRead"], 0);
    let sends = f.home.host.client_requests().len();
    let workflows = std::sync::Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    crate::host_tick::tick_home(&f.home, &workflows);
    let projected = f.projection();
    for (id, order) in [("one", 0), ("two", 1), ("three", 2), ("four", 3)] {
        let row = projected.0["items"]
            .as_array()
            .unwrap()
            .iter()
            .find(|row| row["native"]["id"] == id)
            .unwrap();
        assert_eq!(row["observedOrder"], order);
    }
    assert_eq!(projected.1["historyPagesRead"], 2);
    assert_eq!(projected.1["recoveryPagesRead"], 0);
    assert_recovered_only(&projected.0);
    f.finish(&last);
    f.finish(&dispatch);
    crate::host_tick::tick_home(&f.home, &workflows);
    assert_eq!(
        f.projection(),
        projected,
        "no latest-page substitution or repeated projection"
    );
    assert_eq!(
        f.home.host.client_requests().len(),
        sends,
        "projection sends no native operation"
    );
    assert_eq!(
        f.home.host.snapshot()["threads"].as_array().unwrap().len(),
        1
    );
    assert_eq!(
        f.home
            .history
            .lock()
            .unwrap()
            .role("conversation-home", "stored")["standing"],
        "unknown"
    );
}

#[test]
fn history_bridge_manual_queued_page_rechecks_closed_source_despite_runtime_lag() {
    let mut f = ManualHistory::new();
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    let raw = json!({"data":[plan_entry("turn-a", "accepted-before-close")],"nextCursor":null});
    let dispatch = f.manual(&query, &raw);
    f.home.history.lock().unwrap().reconcile(&f.home.host);
    let before = f.projection();
    Host::close_generation(&mut f.home.host.inner.0.lock().unwrap());
    assert!(
        !f.home.runtime.lock().unwrap().native_view().is_null(),
        "runtime has not consumed closure yet"
    );
    f.finish(&dispatch);
    assert_eq!(f.projection(), before);
    assert_eq!(dispatch.source().evidence()["response"]["result"], raw);
    let received = f
        .home
        .runtime
        .lock()
        .unwrap()
        .receive_native(&f.home.host)
        .1;
    assert!(received["nativeViewLimits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|limit| limit
            .as_str()
            .unwrap()
            .contains("original manual history source is no longer current")));
}

#[test]
fn history_bridge_manual_first_completion_establishes_actual_ready_view_and_late_reply_projects_once(
) {
    let mut first = ManualHistory::with_received_view(false);
    let query = first.query("items", Some("turn-a"), Direction::Asc);
    let dispatch = first.manual(
        &query,
        &json!({"data":[plan_entry("turn-a", "first-page")],"nextCursor":null}),
    );
    assert!(
        first.home.runtime.lock().unwrap().native_view().is_null(),
        "no status read initialized Runtime before completion"
    );
    first.finish(&dispatch);
    let projected = first.projection();
    assert_eq!(projected.0["items"][0]["native"]["id"], "first-page");
    assert_eq!(projected.1["historyPagesRead"], 1);
    drop(first);

    let mut f = ManualHistory::with_received_view(false);
    assert!(f.home.runtime.lock().unwrap().native_view().is_null());
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    let dispatch = f.begin_manual(&query);
    let waited = f
        .home
        .host
        .history_wait(&dispatch, Duration::from_millis(1))
        .unwrap();
    assert_eq!(waited["waitingEnded"], true);
    f.home.reconcile_manual_history();
    assert_eq!(f.projection().1["historyPagesRead"], 0);
    f.pipe.reply(
        &dispatch,
        &json!({"data":[plan_entry("turn-a", "late")],"nextCursor":null}),
    );
    let workflows = std::sync::Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    crate::host_tick::tick_home(&f.home, &workflows);
    let projected = f.projection();
    assert_eq!(projected.0["items"][0]["native"]["id"], "late");
    assert_eq!(projected.1["historyPagesRead"], 1);
    f.finish(&dispatch);
    assert_eq!(f.projection(), projected);
}

#[test]
fn history_bridge_manual_readonly_methods_keep_exact_metadata_turn_goal_and_child_queries() {
    let mut f = ManualHistory::new();
    let query = f.query("metadata", None, Direction::Asc);
    let mut native = history_thread("notLoaded");
    native["turns"] = json!([{"id":"metadata-turn","status":"completed","items":[{"id":"metadata-plan","type":"plan","text":"from metadata"}],"error":null}]);
    let dispatch = f.manual(&query, &json!({"thread":native}));
    f.finish(&dispatch);
    let query = f.query("turns", None, Direction::Asc);
    let raw = json!({"data":[{"id":"embedded-turn","status":"completed","items":[{"id":"embedded-plan","type":"plan","text":"from turns"}],"error":null}],"nextCursor":null});
    let dispatch = f.manual(&query, &raw);
    f.finish(&dispatch);
    let query = f.query("goal", None, Direction::Asc);
    let goal = json!({"threadId":"stored","objective":"native objective","status":"active","createdAt":1,"updatedAt":2,"timeUsedSeconds":0,"tokensUsed":0,"tokenBudget":null});
    let dispatch = f.manual(&query, &json!({"goal":goal}));
    f.finish(&dispatch);
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    let dispatch = f.manual(&query, &json!({"data":[child_entry()],"nextCursor":null}));
    f.finish(&dispatch);
    let query = f.query("child", Some("native-child"), Direction::Asc);
    assert_eq!(
        query.params()["threadId"],
        "native-child",
        "child read intentionally differs from the browser selection"
    );
    let mut child = history_thread("notLoaded");
    child["id"] = json!("native-child");
    child["parentThreadId"] = json!("stored");
    child["turns"] = json!([{"id":"child-turn","status":"completed","items":[{"id":"child-plan","type":"plan","text":"from child"}],"error":null}]);
    let dispatch = f.manual(&query, &json!({"thread":child}));
    let sends = f.home.host.client_requests().len();
    f.finish(&dispatch);
    let (view, counters) = f.projection();
    for id in ["metadata-plan", "embedded-plan", "child-plan"] {
        assert!(
            view["items"]
                .as_array()
                .unwrap()
                .iter()
                .any(|item| item["native"]["id"] == id),
            "{id}"
        );
    }
    assert_eq!(view["goals"]["stored"]["native"], goal);
    assert_eq!(view["descendants"][0]["nativeThread"]["id"], "native-child");
    assert_eq!(counters["historyPagesRead"], 5);
    assert_eq!(counters["recoveryPagesRead"], 0);
    assert_recovered_only(&view);
    assert_eq!(f.home.host.client_requests().len(), sends);
    assert_eq!(f.home.host.snapshot()["conversationTurns"], json!([]));
}

#[test]
fn history_bridge_manual_preserves_live_terminal_items_and_internal_dispatch_semantics() {
    let mut f = ManualHistory::new();
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    f.setup(
        &query,
        json!({"data":[plan_entry("turn-a", "internal-only")],"nextCursor":null}),
    );
    f.home.reconcile_manual_history();
    assert_eq!(
        f.projection().1["historyPagesRead"],
        0,
        "ordinary internal supply-check registration does not project"
    );
    let query = f.query("list", None, Direction::Asc);
    let dispatch = f.manual(
        &query,
        &json!({"data":[history_thread("notLoaded")],"nextCursor":null}),
    );
    f.finish(&dispatch);
    assert_eq!(
        f.projection().1["historyPagesRead"],
        0,
        "manual catalog results never project"
    );
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    let dispatch = f.begin_manual(&query);
    let mut line = String::new();
    f.pipe.reader.read_line(&mut line).unwrap();
    let outbound: Value = serde_json::from_str(&line).unwrap();
    assert_eq!(outbound["id"], *dispatch.source().request_id());
    let error = json!({"code":-32600,"message":"synthetic native read refusal"});
    f.home.host.on_line(
        &serde_json::to_vec(&json!({"id":outbound["id"],"error":error})).unwrap(),
        &g(),
    );
    assert_eq!(f.finish(&dispatch)["response"]["error"], error);
    assert_eq!(
        f.projection().1["historyPagesRead"],
        0,
        "native error replies never project"
    );
    let query = f.query("continue", None, Direction::Asc);
    let mut resume = history_resume("idle", true);
    resume["thread"]["turns"] = json!([{"id":"resume-turn","status":"completed","items":[{"id":"resume-plan","type":"plan","text":"resume response only"}],"error":null}]);
    let dispatch = f.manual(&query, &resume);
    f.finish(&dispatch);
    assert_eq!(
        f.projection().1["historyPagesRead"],
        0,
        "explicit Continue admission does not project its response as a manual read"
    );
    assert_eq!(f.projection().0["items"], json!([]));
    f.home.host.on_line(&serde_json::to_vec(&json!({"method":"item/completed","params":{"threadId":"stored","turnId":"turn-a","item":{"id":"terminal","type":"plan","text":"live terminal"}}})).unwrap(), &g());
    f.projection();
    let query = f.query("items", Some("turn-a"), Direction::Asc);
    let dispatch = f.manual(&query, &json!({"data":[plan_entry("turn-a", "terminal"),plan_entry("turn-a", "new-history")],"nextCursor":null}));
    f.finish(&dispatch);
    let (view, counters) = f.projection();
    let terminal = view["items"]
        .as_array()
        .unwrap()
        .iter()
        .find(|row| row["native"]["id"] == "terminal")
        .unwrap();
    assert_eq!(terminal["native"]["text"], "live terminal");
    assert_eq!(terminal["standing"], "live-observed");
    assert_eq!(terminal["observedOrder"], 0);
    let recovered = view["items"]
        .as_array()
        .unwrap()
        .iter()
        .find(|row| row["native"]["id"] == "new-history")
        .unwrap();
    assert_eq!(recovered["observedOrder"], 1);
    assert_eq!(recovered["standing"], "recovered-from-supplier");
    assert_eq!(counters["historyPagesRead"], 1);
    assert_eq!(counters["recoveryPagesRead"], 0);
}
