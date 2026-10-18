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
fn observer_rebuild_queue_deduplicates_coalesces_and_never_claims_old_cut_coverage() {
    let generation = generation(1);
    let mut queue = ObserverRebuild::default();
    queue.request(&generation, 4, vec!["thread".into(), "thread".into()]);
    let before = queue.snapshot();
    queue.request(&generation, 4, vec!["thread".into()]);
    assert_eq!(queue.snapshot(), before);
    let old = queue.begin(&generation).unwrap();
    assert_eq!(queue.snapshot()["targets"][0]["status"], "reading");
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
    let first = queue.begin(&generation).unwrap();
    assert_eq!(first.thread, "a");
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
