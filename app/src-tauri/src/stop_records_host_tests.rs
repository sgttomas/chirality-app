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
    std::fs::read_to_string(path).unwrap_or_default().lines().map(|l| serde_json::from_str(l).unwrap()).collect()
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
    let (ack, outbound) = exchange(&host, &g, Some(json!({"result":{}})), move || {
        // The request is being written now: SR-01, and nothing later, is already durable.
        assert_eq!(transitions(&ledger), ["SR-01"], "SR-01 is on disk before the interrupt reaches Codex");
    }, || host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()));
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
    assert!(!std::fs::read_to_string(&path).unwrap().contains("\"text\""));
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
    std::fs::rename(&path, &saved).unwrap();
    std::fs::create_dir(&path).unwrap();
    let (ack, outbound) = exchange(&host, &g, Some(json!({"result":{}})), || {}, || host.turn_interrupt(&g, "thread", "turn", "H-acct", &person()));
    ack.unwrap();
    assert_eq!(outbound["method"], "turn/interrupt", "I-2: the person's stop is not blocked by bookkeeping");
    let snapshot = host.snapshot();
    let row = &snapshot["stopRequests"]["records"][0];
    assert!(row["persistence"].as_str().unwrap().starts_with("not yet written to the App ledger"), "{row}");
    assert!(snapshot["recoveryPersistenceError"].is_string(), "the failure is visible");
    // Never relocated: nothing was written anywhere else.
    assert_eq!(std::fs::read_dir(&root).unwrap().count(), 2);
    std::fs::remove_dir(&path).unwrap();
    std::fs::rename(&saved, &path).unwrap();
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
