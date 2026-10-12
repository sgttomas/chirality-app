use super::*;

struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let path = std::env::temp_dir().canonicalize().unwrap()
            .join(crate::util::opaque_id("request-restart-").unwrap());
        std::fs::create_dir(&path).unwrap();
        Self(path)
    }
    fn ledger(&self) -> RecoveryLedger {
        RecoveryLedger::open(self.0.join("ledger.jsonl")).unwrap()
    }
}
impl Drop for Scratch {
    fn drop(&mut self) { let _ = std::fs::remove_dir_all(&self.0); }
}
fn request(session: &str, home: &str, counter: u64, id: Value, state: &str) -> Value {
    json!({"generation":{"appSession":session,"home":home,"spawnCounter":counter},
        "requestId":id,"method":"item/fileChange/requestApproval","state":state,
        "replyWriteResult":if state=="answered"{"written"}else{"not-attempted"},
        "acknowledgment":null,"nativeParameters":{"threadId":"thread","itemId":"item"}})
}
fn endings(ledger: &RecoveryLedger) -> Vec<Value> {
    ledger.entries.iter().filter(|e| e["transition"] == "RQ-06").cloned().collect()
}

#[test]
fn unrecorded_session_requests_close_at_startup_without_a_reply() {
    let f = Scratch::new(); let mut ledger = f.ledger();
    ledger.start_session("old", "candidate").unwrap();
    ledger.request_summary(&request("old", "home", 1, json!(1), "outstanding")).unwrap();
    ledger.start_session("new", "candidate").unwrap();
    let closed = endings(&ledger);
    assert_eq!(closed.len(), 1, "RQ-06 must close the prior listed request");
    assert_eq!(closed[0]["state"], "closed");
    assert_eq!(closed[0]["endedAs"], "ended-unanswered(process-exit)");
    assert_eq!(closed[0]["context"], "app-ended-without-record");
    assert_eq!(closed[0]["session"], "new");
    assert_eq!(closed[0]["replyWrite"], "not-attempted");
    assert_eq!(closed[0]["acknowledgment"], "not-observed");
    assert_eq!(closed[0]["generation"], generation_ref(&request("old", "home", 1, json!(1), "outstanding")["generation"]).unwrap());
    assert_eq!(ledger.snapshot()["oldRequestsAnswerable"], false);
}

#[test]
fn exact_generation_and_request_identities_stay_separate_and_closed_entries_stay_closed() {
    let f = Scratch::new(); let mut ledger = f.ledger();
    ledger.start_session("old", "candidate").unwrap();
    for (home, counter, id) in [("home-a", 1, json!(1)), ("home-b", 1, json!(1)),
        ("home-a", 2, json!(1)), ("home-a", 1, json!("1"))] {
        ledger.request_summary(&request("old", home, counter, id, "outstanding")).unwrap();
    }
    let settled = request("old", "home-a", 1, json!(2), "outstanding");
    ledger.request_summary(&settled).unwrap();
    ledger.request_summary(&request("old", "home-a", 1, json!(2), "answered")).unwrap();
    // A delayed/stale listed pointer cannot reopen an already closed identity.
    ledger.request_summary(&settled).unwrap();
    ledger.start_session("new", "candidate").unwrap();
    let closed = endings(&ledger); assert_eq!(closed.len(), 4);
    let keys: std::collections::BTreeSet<_> = closed.iter()
        .map(|r| (r["generation"].as_str().unwrap(), r["requestIdentity"].as_str().unwrap())).collect();
    assert_eq!(keys.len(), 4);
    assert!(closed.iter().all(|r| r["requestIdentity"] != "2"));
    assert!(RecoveryCustodyView::from_owner("new", Some(&ledger.snapshot()), json!({}), 0, None)
        .snapshot()["limits"].as_array().unwrap().iter().any(|s| s.as_str().unwrap().contains("later listed summary")));
}

#[test]
fn startup_retry_finishes_an_older_batch_after_later_session_markers() {
    let f = Scratch::new(); let mut ledger = f.ledger();
    ledger.start_session("old", "candidate").unwrap();
    for id in [1, 2] { ledger.request_summary(&request("old", "home", 1, json!(id), "outstanding")).unwrap(); }
    // A first startup landed its marker and one ending, then stopped before
    // the remaining append. No session-ended record was supplied.
    ledger.append(json!({"kind":"session_started","session":"partial-start","at":"recorded-start",
        "previousSession":"old","previousSessionEnd":"ended-without-record","candidate":"candidate"})).unwrap();
    let first = startup_request_closures(&ledger.entries, "partial-start").0.remove(0);
    ledger.append(first.clone()).unwrap(); drop(ledger);
    let mut reopened = f.ledger(); reopened.start_session("next-start", "candidate").unwrap();
    let closed = endings(&reopened); assert_eq!(closed.len(), 2);
    assert_eq!(closed.iter().filter(|e| *e == &first).count(), 1);
    assert_eq!(closed.iter().filter(|e| e["session"] == "next-start").count(), 1);
    let before = recorded_startup_request_events(&reopened.entries);
    reopened.start_session("later-start", "candidate").unwrap();
    assert_eq!(endings(&reopened), closed);
    assert_eq!(recorded_startup_request_events(&reopened.entries), before);
}

#[test]
fn reopened_same_session_retry_keeps_the_original_prior_session_link() {
    let f = Scratch::new(); let mut ledger = f.ledger();
    ledger.start_session("old", "candidate").unwrap();
    ledger.request_summary(&request("old", "home", 1, json!(1), "outstanding")).unwrap();
    ledger.append(json!({"kind":"session_started","session":"retry-session","at":"recorded-start",
        "previousSession":"old","previousSessionEnd":"ended-without-record","candidate":"candidate"})).unwrap();
    let marker = ledger.entries.last().unwrap().clone(); drop(ledger);
    let mut reopened = f.ledger(); reopened.start_session("retry-session", "candidate").unwrap();
    assert_eq!(reopened.entries.iter().filter(|r| r["kind"] == "session_started" && r["session"] == "retry-session").count(), 1);
    assert!(reopened.entries.contains(&marker)); assert_eq!(endings(&reopened).len(), 1);
}

#[test]
fn recorded_session_ends_current_generations_and_unknown_history_do_not_acquire_rq06() {
    for how in ["quit", "system-terminated"] {
        let f = Scratch::new(); let mut ledger = f.ledger();
        ledger.start_session("old", "candidate").unwrap();
        ledger.request_summary(&request("old", "home", 1, json!(1), "outstanding")).unwrap();
        ledger.append(RecoveryLedger::session_end_entry("old", how, &[]).unwrap()).unwrap();
        ledger.start_session("new", "candidate").unwrap();
        assert!(endings(&ledger).is_empty());
    }
    let f = Scratch::new(); let mut ledger = f.ledger();
    ledger.start_session("old", "candidate").unwrap();
    ledger.request_summary(&request("unrecorded-source", "home", 1, json!(1), "outstanding")).unwrap();
    ledger.request_summary(&request("new", "home", 1, json!(1), "outstanding")).unwrap();
    let mut legacy = ledger.entries.last().unwrap().clone();
    legacy["generation"] = json!("legacy-opaque-generation"); ledger.append(legacy).unwrap();
    ledger.start_session("new", "candidate").unwrap();
    assert!(endings(&ledger).is_empty());
    let view = RecoveryCustodyView::from_owner("new", Some(&ledger.snapshot()), json!({}), 0, None).snapshot();
    assert!(view["limits"].as_array().unwrap().iter().any(|s| s.as_str().unwrap().contains("canonical full generation")));
    assert!(view["limits"].as_array().unwrap().iter().any(|s| s.as_str().unwrap().contains("session start is unavailable")));
}

#[test]
fn failed_startup_writer_refuses_reuse_and_reopen_reconciles_landed_bytes() {
    let f = Scratch::new(); let mut ledger = f.ledger();
    ledger.start_session("old", "candidate").unwrap();
    ledger.request_summary(&request("old", "home", 1, json!(1), "outstanding")).unwrap();
    let path = f.0.join("ledger.jsonl"); let saved = f.0.join("saved");
    std::fs::rename(&path, &saved).unwrap(); std::fs::create_dir(&path).unwrap();
    assert!(ledger.start_session("failed", "candidate").is_err());
    std::fs::remove_dir(&path).unwrap(); std::fs::rename(&saved, &path).unwrap();
    let before = std::fs::read(&path).unwrap();
    assert!(ledger.start_session("retry", "candidate").unwrap_err().contains("reopen"));
    assert!(ledger.append(RecoveryLedger::session_end_entry("old", "quit", &[]).unwrap()).unwrap_err().contains("reopen"));
    assert_eq!(std::fs::read(&path).unwrap(), before);
    // Reproduce a full closure line landing without entering the writer's
    // in-memory index, as can happen when the subsequent sync is unconfirmed.
    let landed = startup_request_closures(&ledger.entries, "failed").0.remove(0);
    let mut file = OpenOptions::new().append(true).open(&path).unwrap();
    let mut raw = serde_json::to_vec(&landed).unwrap(); raw.push(b'\n'); file.write_all(&raw).unwrap(); drop(file);
    drop(ledger);
    let mut reopened = f.ledger(); reopened.start_session("retry", "candidate").unwrap();
    assert_eq!(endings(&reopened), vec![landed]);
}

#[test]
fn persisted_request_events_keep_source_time_identity_and_reply_observations() {
    let f = Scratch::new(); let mut ledger = f.ledger();
    ledger.start_session("old", "candidate").unwrap();
    ledger.request_summary(&request("old", "home", 1, json!("opaque:id"), "outstanding")).unwrap();
    let original = ledger.entries.last().unwrap().clone();
    ledger.start_session("new", "candidate").unwrap();
    let closed = endings(&ledger).remove(0);
    for key in ["generation", "requestIdentity", "method", "subject", "replyWrite", "acknowledgment"] {
        assert_eq!(closed[key], original[key]);
    }
    let view = RecoveryCustodyView::from_owner("new", Some(&ledger.snapshot()), json!({}), 0, None).snapshot();
    assert_eq!(view["restartEvents"], json!([]));
    assert_eq!(view["requestEndEvents"].as_array().unwrap().len(), 1);
    let event = &view["requestEndEvents"][0];
    assert_eq!(event["appSession"], "new"); assert_eq!(event["at"], closed["at"]);
    let schema: Value = serde_json::from_str(include_str!("../resources/runtime_core/recovery.custody-event.schema.json")).unwrap();
    jsonschema::options().offline().build(&schema).unwrap().validate(event).unwrap();
    drop(ledger); let mut reopened = f.ledger(); reopened.start_session("later", "candidate").unwrap();
    let later = RecoveryCustodyView::from_owner("later", Some(&reopened.snapshot()), json!({}), 0, None).snapshot();
    assert_eq!(later["requestEndEvents"], view["requestEndEvents"]);
    assert_eq!(later["automaticResume"], false);
}

#[test]
fn actual_host_configuration_exposes_endings_without_restoring_native_requests() {
    let f = Scratch::new(); let mut ledger = f.ledger();
    ledger.start_session("old", "candidate").unwrap();
    ledger.request_summary(&request("old", "home", 1, json!(1), "outstanding")).unwrap(); drop(ledger);
    let host = crate::hosting::Host::new(); host.configure_recovery(f.0.join("ledger.jsonl")).unwrap();
    assert_eq!(host.snapshot()["state"], "absent");
    assert_eq!(host.snapshot()["serverRequests"], json!([]));
    assert_eq!(host.recovery_custody().snapshot()["requestEndEvents"].as_array().unwrap().len(), 1);
}
