// REC stop requests through the actual Host (DEL-01-02 §3.4, SQ-I): SR-01 is
// on disk before the interrupt is written, refusals before the send write
// nothing, a ledger failure is visible and never blocks the stop, and the
// outcome reads back after a relaunch. The pipe peer is `/bin/cat`; native
// frames are injected; nothing here establishes supplier behaviour.
use super::*;
use std::path::{Path, PathBuf};

fn scratch() -> PathBuf {
    let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(opaque_id("stop-records-").unwrap());
    std::fs::create_dir(&root).unwrap();
    root
}
/// A ready Host with a configured App ledger and one loaded conversation.
fn ledger_host(root: &Path) -> (Arc<Host>, Value, PathBuf) {
    let host = Arc::new(Host::new());
    let path = root.join("recovery.ledger.jsonl");
    host.configure_recovery(path.clone()).unwrap();
    let g = {
        let mut i = host.inner.0.lock().unwrap();
        let g = json!({"appSession":i.app_session,"home":"native-home","spawnCounter":1});
        i.state = "ready".into();
        i.generation = g.clone();
        i.threads.push(json!({"generation":g,"threadId":"thread","model":"m","modelProvider":"p"}));
        g
    };
    (host, g, path)
}
fn turn(id: &str, status: &str) -> Value {
    json!({"id":id,"status":status,"items":[],"itemsView":"full"})
}
fn event(host: &Host, g: &Value, id: &str, status: &str) {
    let method = if status == "inProgress" { "turn/started" } else { "turn/completed" };
    host.on_line(&serde_json::to_vec(&json!({"method":method,"params":{"threadId":"thread","turn":turn(id,status)}})).unwrap(), g);
}
fn person() -> Value {
    crate::stop_records::person("R · OS account r")
}
fn ledger_rows(path: &Path) -> Vec<Value> {
    crate::recovery::stored_entries(path)
}
fn transitions(path: &Path) -> Vec<String> {
    ledger_rows(path).iter().filter(|e| e["kind"] == "stop_request").map(|e| e["record"]["transition"].as_str().unwrap().to_owned()).collect()
}
/// Runs `operation` against a `/bin/cat` pipe. When the request frame is
/// read, `at_send` runs first (it sees the world as of the write), then the
/// `response` is delivered.
fn exchange<T>(host: &Arc<Host>, g: &Value, response: Option<Value>, at_send: impl FnOnce() + Send + 'static, operation: impl FnOnce() -> T) -> (T, Value) {
    let mut child = Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();
    *host.stdin.lock().unwrap() = child.stdin.take();
    let stdout = child.stdout.take().unwrap();
    let me = Arc::clone(host);
    let generation = g.clone();
    let (tx, rx) = channel();
    let worker = std::thread::spawn(move || {
        let mut line = String::new();
        BufReader::new(stdout).read_line(&mut line).unwrap();
        let outbound: Value = serde_json::from_str(&line).unwrap();
        at_send();
        tx.send(outbound.clone()).unwrap();
        if let Some(mut frame) = response {
            frame["id"] = outbound["id"].clone();
            me.on_line(&serde_json::to_vec(&frame).unwrap(), &generation);
        }
    });
    let result = operation();
    let outbound = rx.recv().unwrap();
    worker.join().unwrap();
    *host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
    (result, outbound)
}

#[test]
fn person_interrupt_writes_sr01_before_the_send_and_settles_from_the_observed_end() {
    let root = scratch();
    let (host, g, path) = ledger_host(&root);
    event(&host, &g, "turn", "inProgress");
    let ledger = path.clone();
    // At the send (the host's own hook, just before the frame is written):
    // SR-01, and nothing later, is already durable. Reading the ledger from the
    // peer's side is not ordered with the host's next write, so it is not used.
    let (seen_tx, seen_rx) = channel::<Vec<String>>();
    *host.before_interrupt_send.lock().unwrap() = Some(Box::new(move || {
        seen_tx.send(transitions(&ledger)).unwrap();
    }));
    let (ack, outbound) = exchange(&host, &g, Some(json!({"result":{}})), || {}, || host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()));
    assert_eq!(seen_rx.recv_timeout(Duration::from_secs(5)).unwrap(), ["SR-01"], "SR-01 is on disk before the interrupt reaches Codex");
    assert_eq!(ack.unwrap()["result"], json!({}));
    assert_eq!(outbound["method"], "turn/interrupt");
    let row = host.snapshot()["stopRequests"]["records"][0].clone();
    assert_eq!(row["state"], "accepted", "acknowledged, not ended");
    assert!(row["label"].is_null(), "no label from an acknowledgment");
    event(&host, &g, "turn", "interrupted");
    host.flush_recovery_observations();
    assert_eq!(transitions(&path), ["SR-01", "SR-02", "SR-04", "SR-06"]);
    let rows = ledger_rows(&path);
    let records: Vec<&Value> = rows.iter().filter(|e| e["kind"] == "stop_request").map(|e| &e["record"]).collect();
    for record in &records {
        crate::stop_records::validate(record).unwrap();
        assert_eq!(record["stopRequestId"], records[0]["stopRequestId"], "one stop request, append-only transitions");
    }
    assert_eq!(records[1]["clientRequest"].as_str().map(|r| r.contains(":client:")), Some(true));
    assert_eq!(records[3]["outcomeLabel"], "interrupted by the person");
    assert_eq!(records[3]["requestedBy"]["identityStatus"], "identity not verified");
    assert_eq!(records[0]["generation"], crate::recovery::generation_ref(&g).unwrap());
    // Every ledger line validates; nothing but pointers was written.
    RecoveryLedger::open(path.clone()).unwrap();
    assert!(!serde_json::to_string(&ledger_rows(&path)).unwrap().contains("\"text\""));
    assert!(!String::from_utf8_lossy(&crate::recovery::stored_bytes(&path)).contains("\"text\""));
    // Relaunch: a new App session reads the outcome back from the ledger alone.
    drop(host);
    let relaunched = Host::new();
    relaunched.configure_recovery(path.clone()).unwrap();
    let back = relaunched.snapshot()["stopRequests"]["records"][0].clone();
    assert_eq!((back["label"].as_str(), back["codexReported"].as_str(), back["earlierSession"].as_bool(), back["persistence"].as_str()),
        (Some("interrupted by the person"), Some("interrupted"), Some(true), Some("recorded in the App ledger")));
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn an_interrupt_refused_before_sending_writes_no_stop_request() {
    let root = scratch();
    let (host, g, path) = ledger_host(&root);
    assert_eq!(host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()).unwrap_err(), "no-live-turn");
    event(&host, &g, "turn", "inProgress");
    let mut other = g.clone();
    other["spawnCounter"] = json!(2);
    assert!(host.turn_interrupt(&other, "thread", "turn", "H-acct", &person()).is_err(), "foreign generation");
    assert!(transitions(&path).is_empty(), "SQ-I I-1: a refusal before SR-01 writes nothing");
    let (ack, _) = exchange(&host, &g, Some(json!({"result":{}})), || {}, || host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()));
    ack.unwrap();
    // SR-11: a second press is refused while the first is requested, sent or accepted; no second record.
    assert_eq!(host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()).unwrap_err(), "stop-already-requested");
    let ids: std::collections::BTreeSet<String> = ledger_rows(&path).iter().filter(|e| e["kind"] == "stop_request").map(|e| e["record"]["stopRequestId"].as_str().unwrap().to_owned()).collect();
    assert_eq!(ids.len(), 1);
    host.inner.0.lock().unwrap().state = "stopping".into();
    assert!(host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()).unwrap_err().contains("not-ready"));
    let after: std::collections::BTreeSet<String> = ledger_rows(&path).iter().filter(|e| e["kind"] == "stop_request").map(|e| e["record"]["stopRequestId"].as_str().unwrap().to_owned()).collect();
    assert_eq!(after, ids, "a refusal while not ready writes nothing");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_ledger_that_refuses_the_write_is_visible_and_the_stop_still_proceeds() {
    let root = scratch();
    let (host, g, path) = ledger_host(&root);
    event(&host, &g, "turn", "inProgress");
    let saved = root.join("ledger-aside");
    let database = crate::recovery::database_path(&path);
    std::fs::rename(&database, &saved).unwrap();
    std::fs::create_dir(&database).unwrap();
    let (ack, outbound) = exchange(&host, &g, Some(json!({"result":{}})), || {}, || host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()));
    ack.unwrap();
    assert_eq!(outbound["method"], "turn/interrupt", "I-2: the person's stop is not blocked by bookkeeping");
    let snapshot = host.snapshot();
    let row = &snapshot["stopRequests"]["records"][0];
    assert!(row["persistence"].as_str().unwrap().starts_with("not yet written to the App ledger"), "{row}");
    assert!(snapshot["recoveryPersistenceError"].is_string(), "the failure is visible");
    // Never relocated: nothing was written anywhere else.
    assert_eq!(std::fs::read_dir(&root).unwrap().count(), 2);
    std::fs::remove_dir(&database).unwrap();
    std::fs::rename(&saved, &database).unwrap();
    host.flush_recovery_observations();
    assert_eq!(transitions(&path), ["SR-01", "SR-02", "SR-04"], "kept in order and written once the ledger accepts it");
    assert_eq!(host.snapshot()["stopRequests"]["records"][0]["persistence"], "recorded in the App ledger");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn no_response_and_a_closed_generation_give_wait_ended_and_outcome_unknown() {
    let root = scratch();
    let (host, g, path) = ledger_host(&root);
    event(&host, &g, "turn", "inProgress");
    let (begun, _) = exchange(&host, &g, None, || {}, || host.turn_interrupt_begin(&g, "thread", "turn", crate::stop_records::Cause::CodexStop, "H-key", &person()));
    let source = begun.unwrap();
    assert!(host.turn_interrupt_acknowledgment(&source, Duration::from_millis(20)).unwrap_err().contains("wait limit"));
    Host::close_generation(&mut host.inner.0.lock().unwrap());
    host.flush_recovery_observations();
    assert_eq!(transitions(&path), ["SR-01", "SR-02", "SR-10", "SR-08"]);
    let last = ledger_rows(&path).into_iter().filter(|e| e["kind"] == "stop_request").last().unwrap()["record"].clone();
    assert_eq!((last["state"].as_str(), last["response"].as_str(), last["outcomeLabel"].as_str(), last["home"].as_str()),
        (Some("outcome-unknown"), Some("unknown-no-response"), Some("interrupted by Stop Codex (final status not observed)"), Some("H-key")));
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn without_a_ledger_the_record_is_kept_in_this_process_and_says_so() {
    let host = Arc::new(Host::new());
    let g = json!({"appSession":"memory-session","home":"native-home","spawnCounter":1});
    {
        let mut i = host.inner.0.lock().unwrap();
        i.state = "ready".into();
        i.generation = g.clone();
        i.threads.push(json!({"generation":g,"threadId":"thread"}));
    }
    event(&host, &g, "turn", "inProgress");
    let (ack, _) = exchange(&host, &g, Some(json!({"result":{}})), || {}, || host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()));
    ack.unwrap();
    event(&host, &g, "turn", "completed");
    let row = host.snapshot()["stopRequests"]["records"][0].clone();
    assert_eq!(row["label"], "completed (stop requested)");
    assert!(row["persistence"].as_str().unwrap().contains("App ledger unavailable"), "{row}");
    assert_eq!(row["earlierSession"], false);
}

// The App-wide writer is not held across the pipe write: SR-01 is durable
// before the send, another writer can take the App writer during the send,
// and SR-02 then waits, in order and visibly, until that writer is done.
#[test]
fn the_app_writer_is_released_before_the_send_and_later_records_wait_for_it() {
    let root = scratch();
    let (host, g, path) = ledger_host(&root);
    event(&host, &g, "turn", "inProgress");
    let (release_tx, release_rx) = channel::<()>();
    let (held_tx, held_rx) = channel::<()>();
    let writer = Arc::clone(&host.recovery_writer);
    let ledger = path.clone();
    *host.before_interrupt_send.lock().unwrap() = Some(Box::new(move || {
        assert_eq!(transitions(&ledger), ["SR-01"], "SR-01 is durable before the send");
        std::thread::spawn(move || {
            let _guard = writer.lock().unwrap();
            held_tx.send(()).unwrap();
            release_rx.recv().unwrap();
        });
        held_rx.recv_timeout(Duration::from_secs(5)).expect("another writer can take the App writer while this interrupt is sent");
    }));
    let (begun, outbound) = exchange(&host, &g, None, || {}, || host.turn_interrupt_begin(&g, "thread", "turn", crate::stop_records::Cause::PersonInterrupt, "H-acct", &person()));
    begun.unwrap();
    assert_eq!(outbound["method"], "turn/interrupt");
    assert_eq!(transitions(&path), ["SR-01"], "SR-02 is not written past the busy writer");
    let row = host.snapshot()["stopRequests"]["records"][0].clone();
    assert_eq!(row["transition"], "SR-02");
    assert!(row["persistence"].as_str().unwrap().starts_with("not yet written to the App ledger"), "{row}");
    release_tx.send(()).unwrap();
    drop(host.recovery_writer.lock().unwrap());
    host.flush_recovery_observations();
    assert_eq!(transitions(&path), ["SR-01", "SR-02"], "written in order once the writer is free");
    std::fs::remove_dir_all(root).unwrap();
}

// A generation that closes after the frame is written but before the request
// is linked still settles it (SR-08), instead of leaving it sent.
#[test]
fn a_generation_closed_between_the_write_and_the_link_still_settles_the_request() {
    let root = scratch();
    let (host, g, path) = ledger_host(&root);
    event(&host, &g, "turn", "inProgress");
    let inner = Arc::clone(&host.inner);
    *host.after_interrupt_send.lock().unwrap() = Some(Box::new(move || {
        Host::close_generation(&mut inner.0.lock().unwrap());
    }));
    let (begun, _) = exchange(&host, &g, None, || {}, || host.turn_interrupt_begin(&g, "thread", "turn", crate::stop_records::Cause::CodexStop, "H-acct", &person()));
    begun.unwrap();
    host.flush_recovery_observations();
    assert_eq!(transitions(&path), ["SR-01", "SR-02", "SR-08"]);
    let row = host.snapshot()["stopRequests"]["records"][0].clone();
    assert_eq!((row["state"].as_str(), row["label"].as_str()), (Some("outcome-unknown"), Some("interrupted by Stop Codex (final status not observed)")));
    std::fs::remove_dir_all(root).unwrap();
}

// A transition that was not recorded stays visible even when the latest
// queued record is in the ledger.
#[test]
fn a_transition_that_was_not_recorded_is_shown_beside_the_recorded_one() {
    let root = scratch();
    let (host, g, _path) = ledger_host(&root);
    event(&host, &g, "turn", "inProgress");
    let (ack, _) = exchange(&host, &g, Some(json!({"result":{}})), || {}, || host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()));
    ack.unwrap();
    host.flush_recovery_observations();
    let id = host.inner.0.lock().unwrap().stop_requests[0].id().to_owned();
    assert!(!Host::stop_request_update(&mut host.inner.0.lock().unwrap(), &id, |_| Err("forced failure".into())));
    let row = host.snapshot()["stopRequests"]["records"][0].clone();
    assert_eq!(row["persistence"], "a transition was not recorded: forced failure; its latest queued record is recorded in the App ledger", "{row}");
    std::fs::remove_dir_all(root).unwrap();
}

// DEL-01-02 §7: a commit that lands but whose folder flush fails is reported
// not confirmed, so the fact stays queued and the next drain appends it again.
// The readers read a ledger with those repeated entries as they read it with
// one copy of each: compared at each relaunch with a twin ledger made from the
// same entries, each once.
fn with_failed_flush<T>(host: &Host, operation: impl FnOnce() -> T) -> T {
    use crate::recovery::store::FAIL_FLUSH_AFTER_COMMIT as FAIL;
    FAIL.with(|f| f.set(true));
    let result = operation();
    if FAIL.with(|f| f.get()) {
        host.flush_recovery_observations();
    }
    assert!(!FAIL.with(|f| f.get()), "a commit landed and its flush failed");
    // The next drain: the landed fact is still queued and is appended again.
    host.flush_recovery_observations();
    result
}
fn relaunch(path: &Path, session: &str) -> Host {
    let host = Host::new();
    host.inner.0.lock().unwrap().app_session = session.to_owned();
    host.configure_recovery(path.to_path_buf()).unwrap();
    host
}
/// The ledger at `path` with each entry once, as an earlier build's JSON
/// Lines ledger in a fresh folder, relaunched as the same App session. Also
/// returns what was repeated: each kind, a stop request by its transition.
fn twin(path: &Path, session: &str) -> (Host, PathBuf, PathBuf, Vec<String>) {
    let mut once: Vec<Value> = Vec::new();
    let mut repeated = Vec::new();
    for entry in ledger_rows(path) {
        if once.contains(&entry) {
            repeated.push(entry["record"]["transition"].as_str().or(entry["kind"].as_str()).unwrap().to_owned());
        } else {
            once.push(entry);
        }
    }
    let root = scratch();
    let twin = root.join("recovery.ledger.jsonl");
    let mut lines = Vec::new();
    for entry in &once {
        lines.extend(serde_json::to_vec(entry).unwrap());
        lines.push(b'\n');
    }
    std::fs::write(&twin, lines).unwrap();
    (relaunch(&twin, session), twin, root, repeated)
}
/// What a relaunch reads: its startup entries (the session marker with the
/// earlier session's end, RQ-06 endings, SR-08 records), the stop requests,
/// the custody view (RQ-06 events, restart events, conversations, limits) and
/// CV-19's latest execution rows. Times are left out.
fn readings(host: &Host, path: &Path, session: &str) -> Value {
    fn untimed(v: &mut Value) {
        match v {
            Value::String(s) if s.len() >= 19 && s.as_bytes()[4] == b'-' && s.as_bytes()[7] == b'-' && s.as_bytes()[10] == b'T' => *v = json!("<time>"),
            Value::Array(a) => a.iter_mut().for_each(untimed),
            Value::Object(o) => o.values_mut().for_each(untimed),
            _ => {}
        }
    }
    let rows = ledger_rows(path);
    let start = rows.iter().position(|e| e["kind"] == "session_started" && e["session"] == session).unwrap();
    let held = host.inner.0.lock().unwrap().recovery_snapshot.as_ref().map(|o| Arc::clone(&o.rows)).unwrap();
    let mut readings = json!({
        "startup": rows[start..],
        "stopRequests": host.snapshot()["stopRequests"],
        "custody": host.recovery_custody().snapshot(),
        "latestExecution": crate::recovery::latest_execution_rows(crate::recovery::History::new(&held, &[])),
    });
    untimed(&mut readings);
    readings
}

#[test]
fn entries_repeated_by_a_retried_drain_read_as_one_copy() {
    let root = scratch();
    let (host, g, path) = ledger_host(&root);
    host.observe_conversation_project(&g, "thread", Some("H-acct"), &crate::recovery::ExplicitAppProjectContext::known("P", crate::recovery::AppProjectSource::ConfiguredDirectory).unwrap()).unwrap();
    event(&host, &g, "turn", "inProgress");
    host.flush_recovery_observations();
    // A request left listed, a stop request left without a final status
    // (SR-01, SR-02, SR-10) and a Codex stop, with repeated entries.
    with_failed_flush(&host, || host.on_line(&serde_json::to_vec(&json!({"id":7,"method":"item/commandExecution/requestApproval","params":{"threadId":"thread","turnId":"turn","itemId":"item"}})).unwrap(), &g));
    let (begun, _) = with_failed_flush(&host, || exchange(&host, &g, None, || {}, || host.turn_interrupt_begin(&g, "thread", "turn", crate::stop_records::Cause::CodexStop, "H-acct", &person())));
    let source = begun.unwrap();
    with_failed_flush(&host, || assert!(host.turn_interrupt_acknowledgment(&source, Duration::from_millis(20)).is_err()));
    let material = json!({"observedLiveTurns":[{"threadId":"thread","turnId":"turn"}]});
    assert_eq!(with_failed_flush(&host, || host.record_codex_stop(&person(), "H-acct", false, &material))["state"], "not yet recorded");
    let first = host.inner.0.lock().unwrap().app_session.clone();
    // The App ends without an end record: the next start ends the request
    // (RQ-06) and the stop request (SR-08).
    drop(host);
    let second = opaque_id("app-session:").unwrap();
    let a = relaunch(&path, &second);
    let (b, twin_path, twin_root, repeated) = twin(&path, &second);
    let rows = ledger_rows(&path);
    assert_eq!(repeated, ["register_entry_summary", "SR-01", "SR-10", "codex_stop"], "each written twice");
    assert_eq!(readings(&a, &path, &second), readings(&b, &twin_path, &second));
    let startup = &rows[rows.iter().position(|e| e["session"] == second).unwrap()..];
    assert_eq!(startup.iter().filter(|e| e["transition"] == "RQ-06").count(), 1, "one RQ-06 ending: {startup:#?}");
    assert_eq!(startup.iter().filter(|e| e["record"]["transition"] == "SR-08").count(), 1, "one SR-08 record: {startup:#?}");
    assert_eq!(startup[0]["previousSession"], first);
    // This session's quit answers are repeated too; the next start reads its end.
    let asked = json!({"observedLiveTurns":[{"threadId":"thread","turnId":"turn"}]});
    with_failed_flush(&a, || a.record_quit_requested(&person(), &asked));
    with_failed_flush(&a, || a.record_quit_answered(&person(), true));
    a.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    drop((a, b));
    let third = opaque_id("app-session:").unwrap();
    let a = relaunch(&path, &third);
    let (b, twin_path_2, twin_root_2, repeated) = twin(&path, &third);
    assert_eq!(repeated, ["register_entry_summary", "SR-01", "SR-10", "codex_stop", "quit_requested", "quit_answered"], "and the quit request and answer");
    let reading = readings(&a, &path, &third);
    assert_eq!(reading, readings(&b, &twin_path_2, &third));
    assert_eq!(reading["startup"][0]["previousSessionEnd"], "quit-with-live-work");
    assert_eq!(reading["custody"]["requestEndEvents"].as_array().unwrap().len(), 1, "{reading:#}");
    for root in [root, twin_root, twin_root_2] {
        std::fs::remove_dir_all(root).unwrap();
    }
}
