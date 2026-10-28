//! Queue rules plus actual Host history dispatch over an owned local pipe.
//! The peer is /bin/cat transport only; no Codex, model or account is started.
use super::*;
use std::io::{BufRead, BufReader};
use std::os::fd::AsRawFd;
use std::process::{Child, ChildStdout, Command, Stdio};

fn generation(counter: u64) -> Value {
    json!({"appSession":"observer-session","home":"observer-home","spawnCounter":counter})
}

fn native_thread(id: &str) -> Value {
    json!({"id":id,"cliVersion":"0.160.0","createdAt":1,"updatedAt":2,
        "cwd":"/invented","ephemeral":false,"modelProvider":"fixture-provider","preview":"observer fixture",
        "projectId":null,"sessionId":"fixture-session","source":"appServer","status":{"type":"notLoaded"},"turns":[]})
}

fn turns(cursor: Value) -> Value {
    json!({"data":[{"id":"turn","status":"completed","items":[],"error":null,"itemsView":"summary"}],"nextCursor":cursor})
}

fn queue(host: &Host, cut: u64, threads: &[&str]) {
    let mut inner = host.inner.0.lock().unwrap();
    let generation = inner.generation.clone();
    inner.observer_rebuild.request(
        &generation,
        cut,
        threads.iter().map(|thread| (*thread).to_owned()).collect(),
    );
}

fn status(host: &Host) -> Value {
    host.inner.0.lock().unwrap().observer_rebuild.snapshot()
}

fn target(host: &Host) -> Value {
    status(host)["targets"][0].clone()
}

struct Fixture {
    host: Arc<Host>,
    generation: Value,
    root: PathBuf,
}

impl Fixture {
    fn new() -> Self {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(opaque_id("observer-rebuild-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let host = Arc::new(Host::new());
        host.configure_recovery(root.join("recovery.ledger.jsonl"))
            .unwrap();
        let generation = {
            let mut inner = host.inner.0.lock().unwrap();
            let generation =
                json!({"appSession":inner.app_session,"home":"observer-home","spawnCounter":1});
            inner.generation = generation.clone();
            inner.journal.begin_generation(generation.clone());
            inner.observer_rebuild.reset(&generation);
            inner.state = "ready".into();
            inner.threads.push(json!({"generation":generation,"threadId":"thread","model":"fixture-model","modelProvider":"fixture-provider"}));
            generation
        };
        Self {
            host,
            generation,
            root,
        }
    }
    fn ledger(&self) -> Vec<Value> {
        crate::recovery::stored_entries(&self.root.join("recovery.ledger.jsonl"))
    }
}

impl Drop for Fixture {
    fn drop(&mut self) {
        std::fs::remove_dir_all(&self.root).unwrap();
    }
}

fn pipe(host: &Host) -> (Child, BufReader<ChildStdout>) {
    let mut child = Command::new("/bin/cat")
        .env_clear()
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .unwrap();
    *host.stdin.lock().unwrap() = child.stdin.take();
    let reader = BufReader::new(child.stdout.take().unwrap());
    (child, reader)
}

fn rpc(reader: &mut BufReader<ChildStdout>) -> Value {
    let mut poll = libc::pollfd {
        fd: reader.get_ref().as_raw_fd(),
        events: libc::POLLIN,
        revents: 0,
    };
    assert!(
        unsafe { libc::poll(&mut poll, 1, 5_000) } > 0,
        "actual history RPC was not written"
    );
    let mut line = String::new();
    assert!(reader.read_line(&mut line).unwrap() > 0);
    serde_json::from_str(&line).unwrap()
}

fn exchange<T>(
    host: &Arc<Host>,
    replies: Vec<Value>,
    operation: impl FnOnce() -> T,
) -> (T, Vec<Value>) {
    let (mut child, mut reader) = pipe(host);
    let source = Arc::clone(host);
    let generation = host.snapshot()["generation"].clone();
    let worker = std::thread::spawn(move || {
        let mut wire = Vec::new();
        for mut response in replies {
            let request = rpc(&mut reader);
            response["id"] = request["id"].clone();
            source.on_line(&serde_json::to_vec(&response).unwrap(), &generation);
            wire.push(request);
        }
        wire
    });
    let result = operation();
    let wire = worker.join().unwrap();
    *host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
    (result, wire)
}

#[test]
fn observer_rebuild_oversized_own_replies_do_not_feed_an_automatic_read_loop() {
    let fixture = Fixture::new();
    let host = &fixture.host;
    {
        let mut inner = host.inner.0.lock().unwrap();
        inner.journal = super::super::observer_journal::ObserverJournal::with_limits(20, 512);
        inner.journal.begin_generation(fixture.generation.clone());
    }
    let ledger = fixture.ledger();
    let custody = host.custody_events();
    let metadata = json!({"thread":native_thread("thread"),"nativeUnknownField":"original metadata extension".repeat(100)});
    let summaries = json!({"data":[],"nextCursor":null,"nativeUnknownField":"original summary extension".repeat(100)});
    let before = host.observe_scoped(&fixture.generation, &Value::Null, 0);
    assert_eq!(before["gap"], true);
    let (attempts, wire) = exchange(
        host,
        vec![
            json!({"result":metadata.clone()}),
            json!({"result":summaries.clone()}),
        ],
        || {
            let attempts = host.observer_rebuild_reads(Duration::from_secs(1));
            let read = target(host);
            assert_eq!(read["status"], "partial");
            assert_eq!(read["cut"], 0);
            assert_eq!(read["metadata"], metadata);
            assert_eq!(read["turns"], summaries);
            let floor = host.inner.0.lock().unwrap().journal.omitted_through();
            assert_eq!(
                floor, 2,
                "both original oversized replies still advance the public omitted-through cut"
            );
            for _ in 0..3 {
                let attached = host.observe_scoped(&fixture.generation, &fixture.generation, 0);
                assert_eq!(attached["gap"], true, "the gap remains public truth");
                assert_eq!(
                    host.observer_rebuild_reads(Duration::from_millis(5)),
                    0,
                    "the OA reader's own oversized replies must not cause more history RPCs"
                );
            }
            let held = target(host);
            assert_eq!(held["status"], "partial");
            assert_eq!(
                held["cut"], 0,
                "the old read never claims the new omission cut"
            );
            assert_eq!(held["suppressedCut"], 2);
            assert_eq!(
                held["suppressionReason"],
                "no-new-non-observer-source-activity"
            );
            attempts
        },
    );
    assert_eq!(
        (attempts, wire.len(), host.client_requests().len()),
        (1, 2, 2)
    );
    for (request, expected) in wire.iter().zip([&metadata, &summaries]) {
        let source = host
            .source_request(&fixture.generation, &request["id"])
            .unwrap();
        assert_eq!(
            &source.evidence()["response"]["result"],
            expected,
            "private original response remains whole"
        );
    }
    // New admitted non-reader source input plus a new omission cut enables
    // one further attempt; that attempt's own replies become quiet again.
    let external = json!({"method":"fixture/external-native-input","params":{"nativeUnknownField":"external notification".repeat(100)}});
    host.on_line(&serde_json::to_vec(&external).unwrap(), &fixture.generation);
    assert_eq!(host.inner.0.lock().unwrap().journal.omitted_through(), 3);
    host.observe_scoped(&fixture.generation, &fixture.generation, 0);
    let (_, next) = exchange(
        host,
        vec![json!({"result":metadata}), json!({"result":summaries})],
        || {
            assert_eq!(host.observer_rebuild_reads(Duration::from_secs(1)), 1);
            assert_eq!(target(host)["cut"], 3);
            host.observe_scoped(&fixture.generation, &fixture.generation, 0);
            assert_eq!(host.observer_rebuild_reads(Duration::from_millis(5)), 0);
        },
    );
    assert_eq!((next.len(), host.client_requests().len()), (2, 4));
    assert_eq!(host.inner.0.lock().unwrap().journal.omitted_through(), 5);
    assert_eq!(target(host)["suppressedCut"], 5);
    assert_eq!(fixture.ledger(), ledger);
    assert_eq!(host.custody_events(), custody);
}

#[test]
fn observer_rebuild_own_cut_suppression_preserves_failure_and_admits_new_targets_once() {
    let generation = generation(1);
    let mut queue = ObserverRebuild::default();
    queue.request(&generation, 0, vec!["a".into()]);
    queue.record_source_activity(&generation, 1);
    let failed = queue.begin(&generation).unwrap();
    queue.finish(
        &failed,
        failed.result(
            Reading::default(),
            Some(Failure::Unavailable("fixture-unavailable")),
        ),
    );
    queue.request(&generation, 4, vec!["a".into()]);
    assert!(queue.begin(&generation).is_none());
    let held = queue.snapshot()["targets"][0].clone();
    assert_eq!(held["status"], "unavailable");
    assert_eq!(held["cut"], 0);
    assert_eq!(held["requestedCut"], 4);
    assert_eq!(held["suppressedCut"], 4);
    assert_eq!(held["sourceActivityPosition"], 1);
    queue.request(&generation, 4, vec!["a".into(), "b".into()]);
    let new_target = queue.begin(&generation).unwrap();
    assert_eq!(
        new_target.thread, "b",
        "another target's read never suppresses a genuinely new target"
    );
    queue.finish(&new_target, new_target.result(Reading::default(), None));
    assert!(queue.begin(&generation).is_none());
    queue.record_source_activity(&generation, 6);
    assert!(
        queue.begin(&generation).is_some(),
        "a previously requested newer gap is eligible after actual external activity"
    );
}

#[test]
fn observer_rebuild_source_activity_is_original_correlation_not_native_labels_or_server_ids() {
    let fixture = Fixture::new();
    let host = &fixture.host;
    let (mut child, mut reader) = pipe(host);
    let query = crate::native_history::workspace_read(
        "observer-home",
        &fixture.generation,
        "thread/read",
        json!({"threadId":"thread","includeTurns":false}),
    )
    .unwrap();
    let own = host
        .history_dispatch_by(
            &query,
            json!({"kind":"app-rule","name":"observer-history-read"}),
        )
        .unwrap();
    let request = rpc(&mut reader);
    let activity = || status(host)["sourceActivityPosition"].as_u64().unwrap();
    assert_eq!(activity(), 0);
    // The incoming ID alone cannot hide an independent server request.
    host.on_line(&serde_json::to_vec(&json!({"id":request["id"],"method":"item/fileChange/requestApproval","params":{"threadId":"thread","turnId":"turn","itemId":"item"},"initiator":{"kind":"app-rule","name":"observer-history-read"}})).unwrap(), &fixture.generation);
    assert_eq!(activity(), 1);
    assert_eq!(host.snapshot()["serverRequests"][0]["state"], "outstanding");
    // Same spelling, different native ID type: this is not the pending client.
    host.on_line(&serde_json::to_vec(&json!({"id":request["id"].as_u64().unwrap().to_string(),"result":{},"initiator":{"kind":"app-rule","name":"observer-history-read"}})).unwrap(), &fixture.generation);
    assert_eq!(activity(), 2);
    assert!(own.evidence()["response"].is_null());
    let reply = json!({"id":request["id"],"result":{"thread":native_thread("thread")}});
    host.on_line(&serde_json::to_vec(&reply).unwrap(), &fixture.generation);
    assert_eq!(
        activity(),
        2,
        "only the actual original pending OA response is excluded"
    );
    assert_eq!(own.evidence()["response"], reply);
    host.on_line(&serde_json::to_vec(&reply).unwrap(), &fixture.generation);
    assert_eq!(
        activity(),
        4,
        "an uncorrelated duplicate is not a new matching pending response"
    );
    let person = host.history_dispatch(&query).unwrap();
    let person_request = rpc(&mut reader);
    host.on_line(&serde_json::to_vec(&json!({"id":person_request["id"],"result":{"thread":native_thread("thread")},"initiator":{"kind":"app-rule","name":"observer-history-read"},"requestRef":own.source().request_ref()})).unwrap(), &fixture.generation);
    assert_eq!(
        activity(),
        5,
        "an incoming label/reference cannot rewrite the person's original private initiator"
    );
    assert!(!person.evidence()["response"].is_null());
    let mut foreign = fixture.generation.clone();
    foreign["home"] = json!("other-home");
    host.on_line(
        &serde_json::to_vec(&json!({"method":"fixture/foreign"})).unwrap(),
        &foreign,
    );
    assert_eq!(activity(), 5);
    {
        Host::close_generation(&mut host.inner.0.lock().unwrap());
    }
    host.on_line(
        &serde_json::to_vec(&json!({"method":"fixture/closed"})).unwrap(),
        &fixture.generation,
    );
    assert_eq!(
        activity(),
        5,
        "only actual current/open receipt admission updates activity"
    );
    let mut next = fixture.generation.clone();
    next["spawnCounter"] = json!(2);
    {
        let mut inner = host.inner.0.lock().unwrap();
        inner.generation = next.clone();
        inner.journal.begin_generation(next.clone());
        inner.observer_rebuild.reset(&next);
        inner.state = "ready".into();
    }
    assert_eq!(
        activity(),
        0,
        "the actual source installation reset does not inherit an old generation's activity"
    );
    host.on_line(
        &serde_json::to_vec(&json!({"method":"fixture/old-source-after-install"})).unwrap(),
        &fixture.generation,
    );
    assert_eq!(
        activity(),
        0,
        "a late old-source frame cannot create activity in the new generation"
    );
    *host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
}

#[test]
fn observer_rebuild_external_activity_during_an_own_read_remains_eligible_after_finish() {
    let fixture = Fixture::new();
    let host = &fixture.host;
    {
        let mut inner = host.inner.0.lock().unwrap();
        inner.journal = super::super::observer_journal::ObserverJournal::with_limits(20, 512);
        inner.journal.begin_generation(fixture.generation.clone());
    }
    host.observe_scoped(&fixture.generation, &Value::Null, 0);
    let (mut child, mut reader) = pipe(host);
    let source = Arc::clone(host);
    let generation = fixture.generation.clone();
    let worker = std::thread::spawn(move || {
        for (index, result) in [
            json!({"thread":native_thread("thread")}),
            json!({"data":[],"nextCursor":null}),
        ]
        .into_iter()
        .enumerate()
        {
            let request = rpc(&mut reader);
            if index == 0 {
                source.on_line(&serde_json::to_vec(&json!({"method":"fixture/external-during-read","params":{"extension":"source activity".repeat(100)}})).unwrap(), &generation);
                source.observe_scoped(&generation, &generation, 0);
            }
            source.on_line(
                &serde_json::to_vec(&json!({"id":request["id"],"result":result})).unwrap(),
                &generation,
            );
        }
    });
    assert_eq!(host.observer_rebuild_reads(Duration::from_secs(1)), 1);
    worker.join().unwrap();
    *host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
    let queued = target(host);
    assert_eq!(queued["status"], "queued");
    assert_eq!(queued["cut"], 1);
    assert_eq!(
        queued["previousAttempt"]["sourceActivityPosition"], 0,
        "capture activity at begin, not finish"
    );
    assert_eq!(status(host)["sourceActivityPosition"], 1);
    exchange(
        host,
        vec![
            json!({"result":{"thread":native_thread("thread")}}),
            json!({"result":{"data":[],"nextCursor":null}}),
        ],
        || {
            assert_eq!(host.observer_rebuild_reads(Duration::from_secs(1)), 1);
            assert_eq!(target(host)["cut"], 1);
            assert_eq!(target(host)["sourceActivityPosition"], 1);
            assert_eq!(host.observer_rebuild_reads(Duration::from_millis(5)), 0);
        },
    );
}

#[test]
fn observer_rebuild_queue_deduplicates_coalesces_and_never_claims_old_cut_coverage() {
    let generation = generation(1);
    let mut queue = ObserverRebuild::default();
    queue.request(&generation, 4, vec!["thread".into(), "thread".into()]);
    queue.record_source_activity(&generation, 4);
    let before = queue.snapshot();
    queue.request(&generation, 4, vec!["thread".into()]);
    assert_eq!(queue.snapshot(), before);
    let old = queue.begin(&generation).unwrap();
    assert_eq!(queue.snapshot()["targets"][0]["status"], "reading");
    queue.record_source_activity(&generation, 8);
    queue.request(&generation, 9, vec!["thread".into()]);
    queue.request(&generation, 7, vec!["thread".into()]);
    assert!(
        queue.begin(&generation).is_none(),
        "one original attempt stays in flight"
    );
    assert!(queue.finish(&old, old.result(Reading::default(), None)));
    let waiting = queue.snapshot();
    assert_eq!(waiting["targets"][0]["cut"], 9);
    assert_eq!(waiting["targets"][0]["status"], "queued");
    assert_eq!(
        waiting["targets"][0]["previousAttempt"]["status"],
        "superseded"
    );
    assert_eq!(waiting["targets"][0]["previousAttempt"]["cut"], 4);
    let newest = queue.begin(&generation).unwrap();
    assert_eq!(newest.cut, 9);
    assert!(queue.finish(
        &newest,
        newest.result(
            Reading::default(),
            Some(Failure::Unavailable("fixture-unavailable"))
        )
    ));
    queue.request(&generation, 9, vec!["thread".into()]);
    assert!(
        queue.begin(&generation).is_none(),
        "failed reads never become a same-cut poll"
    );
    assert_eq!(queue.snapshot()["targets"][0]["status"], "unavailable");
}

#[test]
fn observer_rebuild_advancing_first_target_cannot_starve_an_unread_target() {
    let generation = generation(1);
    let mut queue = ObserverRebuild::default();
    queue.request(&generation, 1, vec!["a".into(), "b".into()]);
    queue.record_source_activity(&generation, 1);
    let first = queue.begin(&generation).unwrap();
    assert_eq!(first.thread, "a");
    queue.record_source_activity(&generation, 2);
    queue.request(&generation, 2, vec!["a".into()]);
    queue.finish(&first, first.result(Reading::default(), None));
    queue.request(&generation, 3, vec!["a".into()]);
    let unread = queue.begin(&generation).unwrap();
    assert_eq!(
        unread.thread, "b",
        "new cuts do not jump ahead of another pending target"
    );
    queue.finish(&unread, unread.result(Reading::default(), None));
    let next = queue.begin(&generation).unwrap();
    assert_eq!((next.thread.as_str(), next.cut), ("a", 3));
    queue.record_source_activity(&generation, 4);
    queue.request(&generation, 4, vec!["a".into(), "b".into()]);
    queue.finish(&next, next.result(Reading::default(), None));
    assert_eq!(
        queue.begin(&generation).unwrap().thread,
        "b",
        "rotation also survives coalescing while a target is running"
    );
}

#[test]
fn observer_rebuild_empty_targets_and_new_generation_keep_honest_source_scope() {
    let first = generation(1);
    let next = generation(2);
    let mut queue = ObserverRebuild::default();
    queue.request(&first, 0, vec![]);
    assert_eq!(queue.snapshot()["status"], "unavailable");
    assert_eq!(queue.snapshot()["limit"], "no-known-loaded-threads");
    assert_eq!(queue.snapshot()["targets"], json!([]));
    queue.request(&first, 0, vec!["thread".into()]);
    let old = queue.begin(&first).unwrap();
    queue.reset(&next);
    assert!(!queue.finish(&old, old.result(Reading::default(), None)));
    assert_eq!(queue.snapshot()["generation"], next);
    assert_eq!(queue.snapshot()["targets"], json!([]));
}

#[test]
fn observer_rebuild_enqueue_and_status_send_nothing_and_change_no_custody_or_ledger() {
    let fixture = Fixture::new();
    let host = &fixture.host;
    let before = (
        host.client_requests(),
        host.custody_events(),
        fixture.ledger(),
    );
    let (mut child, reader) = pipe(host);
    queue(host, 7, &["thread"]);
    assert_eq!(target(host)["status"], "queued");
    assert_eq!(status(host), status(host));
    let mut poll = libc::pollfd {
        fd: reader.get_ref().as_raw_fd(),
        events: libc::POLLIN,
        revents: 0,
    };
    assert_eq!(
        unsafe { libc::poll(&mut poll, 1, 0) },
        0,
        "queue/status may not write native bytes"
    );
    assert_eq!(
        (
            host.client_requests(),
            host.custody_events(),
            fixture.ledger()
        ),
        before
    );
    *host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
}

#[test]
fn observer_rebuild_actual_reads_are_partial_source_bound_and_neutral_to_live_projection() {
    let fixture = Fixture::new();
    let host = &fixture.host;
    let home = crate::runtime_session::HomeSession::new(
        crate::home_resources::HomeClass::Account,
        Arc::clone(host),
        Err("synthetic fixture has no supplier configuration".into()),
    )
    .unwrap();
    host.on_line(&serde_json::to_vec(&json!({"method":"turn/started","params":{"threadId":"thread","turn":{"id":"turn","status":"inProgress","items":[],"error":null,"itemsView":"notLoaded"}}})).unwrap(), &fixture.generation);
    let live = crate::host_tick::receive_view(&home);
    let custody = host.custody_events();
    let ledger = fixture.ledger();
    queue(host, 8, &["thread"]);
    let (attempts, wire) = exchange(
        host,
        vec![
            json!({"result":{"thread":native_thread("thread")}}),
            json!({"result":turns(json!("more-turns"))}),
        ],
        || host.observer_rebuild_reads(Duration::from_secs(1)),
    );
    assert_eq!(attempts, 1);
    assert_eq!(
        wire.iter()
            .map(|request| request["method"].as_str().unwrap())
            .collect::<Vec<_>>(),
        ["thread/read", "thread/turns/list"]
    );
    assert_eq!(
        wire[0]["params"],
        json!({"threadId":"thread","includeTurns":false})
    );
    assert_eq!(
        wire[1]["params"],
        json!({"threadId":"thread","sortDirection":"desc","itemsView":"summary"})
    );
    let result = target(host);
    assert_eq!(result["status"], "partial");
    assert_eq!(result["cut"], 8);
    assert_eq!(result["generation"], fixture.generation);
    assert_eq!(
        result["metadata"],
        json!({"thread":native_thread("thread")})
    );
    assert_eq!(result["turns"], turns(json!("more-turns")));
    assert_eq!(
        result["turnCursor"],
        json!({"status":"reported","value":"more-turns"})
    );
    assert_eq!(result["fullHistoryRebuilt"], false);
    assert_eq!(result["itemsRequested"], false);
    assert_eq!(result["receipts"].as_array().unwrap().len(), 2);
    for receipt in result["receipts"].as_array().unwrap() {
        let original = host
            .source_request(&fixture.generation, &receipt["requestIdentity"])
            .unwrap();
        assert_eq!(receipt["requestRef"], original.request_ref());
        assert_eq!(receipt["params"], original.attempted_frame()["params"]);
        assert_eq!(receipt["resultAccepted"], true);
    }
    assert!(host
        .client_requests()
        .iter()
        .all(|request| request["initiator"]
            == json!({"kind":"app-rule","name":"observer-history-read"})));
    let after = crate::host_tick::receive_view(&home);
    for field in ["items", "turns", "revisions"] {
        assert_eq!(
            after[field], live[field],
            "history side result cannot replace canonical {field}"
        );
    }
    assert_eq!(
        host.snapshot()["conversationTurns"][0]["nativeTurn"]["status"],
        "inProgress"
    );
    assert_eq!(host.custody_events(), custody);
    assert_eq!(fixture.ledger(), ledger);
    queue(host, 8, &["thread"]);
    assert_eq!(host.observer_rebuild_reads(Duration::from_millis(5)), 0);
    assert_eq!(
        host.client_requests().len(),
        2,
        "no same-cut polling or resume"
    );
}

#[test]
fn observer_rebuild_supplier_schema_and_subject_failures_are_masked_and_not_retried() {
    const PRIVATE: &str = "OBSERVER_REBUILD_REJECTED_NATIVE_CANARY";
    let mut invalid = native_thread("thread");
    invalid["id"] = Value::Null;
    invalid["echo"] = json!(PRIVATE);
    for (reply, cause) in [
        (
            json!({"error":{"code":-32600,"message":PRIVATE,"data":{"echo":PRIVATE}}}),
            "supplier-history-error",
        ),
        (
            json!({"result":{"thread":invalid}}),
            "invalid-native-history-response",
        ),
        (
            json!({"result":{"thread":native_thread("different-thread")}}),
            "metadata-thread-mismatch",
        ),
    ] {
        let fixture = Fixture::new();
        queue(&fixture.host, 3, &["thread"]);
        let (attempts, wire) = exchange(&fixture.host, vec![reply], || {
            fixture.host.observer_rebuild_reads(Duration::from_secs(1))
        });
        assert_eq!(attempts, 1);
        assert_eq!(
            wire.len(),
            1,
            "failed metadata must not trigger another read"
        );
        let result = target(&fixture.host);
        assert_eq!(result["status"], "unavailable");
        assert_eq!(result["limit"], cause);
        assert!(result["metadata"].is_null());
        assert!(
            !status(&fixture.host).to_string().contains(PRIVATE),
            "rejected native payload is not a queue diagnostic"
        );
        let actual = fixture
            .host
            .source_request(&fixture.generation, &wire[0]["id"])
            .unwrap();
        if cause != "metadata-thread-mismatch" {
            assert!(
                actual.evidence()["response"].to_string().contains(PRIVATE),
                "original transient Host response remains unchanged"
            );
        }
        queue(&fixture.host, 3, &["thread"]);
        assert_eq!(
            fixture
                .host
                .observer_rebuild_reads(Duration::from_millis(5)),
            0
        );
    }
}

#[test]
fn observer_rebuild_partial_metadata_and_empty_turn_page_preserve_actual_extent() {
    for malformed in [false, true] {
        let fixture = Fixture::new();
        queue(&fixture.host, 1, &["thread"]);
        let page = if malformed {
            json!({"data":"REJECTED_TURN_PAGE_CANARY","nextCursor":null})
        } else {
            json!({"data":[],"nextCursor":null})
        };
        exchange(
            &fixture.host,
            vec![
                json!({"result":{"thread":native_thread("thread")}}),
                json!({"result":page.clone()}),
            ],
            || fixture.host.observer_rebuild_reads(Duration::from_secs(1)),
        );
        let result = target(&fixture.host);
        assert_eq!(
            result["metadata"],
            json!({"thread":native_thread("thread")})
        );
        if malformed {
            assert_eq!(result["status"], "unavailable");
            assert!(result["turns"].is_null());
            assert!(!result.to_string().contains("REJECTED_TURN_PAGE_CANARY"));
        } else {
            assert_eq!(result["status"], "partial");
            assert_eq!(result["turns"], page);
            assert_eq!(result["turnCursor"], json!({"status":"exhausted"}));
        }
        assert_eq!(result["fullHistoryRebuilt"], false);
    }
}

#[test]
fn observer_rebuild_timeout_keeps_real_written_receipt_without_retry() {
    let fixture = Fixture::new();
    queue(&fixture.host, 5, &["thread"]);
    let (mut child, mut reader) = pipe(&fixture.host);
    assert_eq!(
        fixture
            .host
            .observer_rebuild_reads(Duration::from_millis(5)),
        1
    );
    let written = rpc(&mut reader);
    assert_eq!(written["method"], "thread/read");
    let result = target(&fixture.host);
    assert_eq!(result["status"], "unavailable");
    assert_eq!(result["limit"], "history-result-not-observed");
    assert_eq!(result["receipts"][0]["writeResult"], "written");
    assert_eq!(result["receipts"][0]["waitingEnded"], true);
    assert_eq!(
        fixture
            .host
            .observer_rebuild_reads(Duration::from_millis(5)),
        0
    );
    *fixture.host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
}

#[test]
fn observer_rebuild_changed_source_during_wait_never_publishes_into_successor() {
    let fixture = Fixture::new();
    queue(&fixture.host, 6, &["thread"]);
    let (mut child, mut reader) = pipe(&fixture.host);
    let source = Arc::clone(&fixture.host);
    let old = fixture.generation.clone();
    let worker = std::thread::spawn(move || {
        let request = rpc(&mut reader);
        let next = {
            let mut inner = source.inner.0.lock().unwrap();
            Host::close_generation(&mut inner);
            let mut next = old.clone();
            next["spawnCounter"] = json!(2);
            inner.generation = next.clone();
            inner.state = "ready".into();
            inner.observer_rebuild.reset(&next);
            next
        };
        source.on_line(
            &serde_json::to_vec(
                &json!({"id":request["id"],"result":{"thread":native_thread("thread")}}),
            )
            .unwrap(),
            &old,
        );
        next
    });
    assert_eq!(
        fixture
            .host
            .observer_rebuild_reads(Duration::from_millis(30)),
        1
    );
    let next = worker.join().unwrap();
    assert_eq!(status(&fixture.host)["generation"], next);
    assert_eq!(status(&fixture.host)["targets"], json!([]));
    assert_eq!(
        fixture.host.client_requests().len(),
        1,
        "the successor receives no old target's second read"
    );
    *fixture.host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
}
