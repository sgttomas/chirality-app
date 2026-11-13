//! REC stop requests: schema copy, transitions SR-01…SR-13, labels, the
//! `codex_stop` ledger entry and the read-back after a relaunch.
use super::*;

fn g() -> Value {
    json!({"appSession":"session-a","home":"native-home","spawnCounter":1})
}
fn requested(cause: Cause) -> StopRequest {
    StopRequest::requested(&g(), "H-acct", "thread", "turn", cause, &person("R · OS account r")).unwrap()
}

#[test]
fn embedded_schema_examples_hold() {
    let valid: Value = serde_json::from_str(include_str!("../resources/runtime_core/recovery.stop-request.example.valid.json")).unwrap();
    validate(&valid).unwrap();
    let invalid: Value = serde_json::from_str(include_str!("../resources/runtime_core/recovery.stop-request.example.invalid.json")).unwrap();
    let cases: Vec<Value> = match &invalid { Value::Array(items) => items.clone(), other => vec![other.clone()] };
    for case in cases {
        let record = case.get("instance").cloned().unwrap_or(case);
        assert!(validate(&record).is_err(), "{record}");
    }
}

#[test]
fn person_interrupt_records_request_send_answer_and_observed_end_apart() {
    let mut sr = requested(Cause::PersonInterrupt);
    let first = sr.record().clone();
    assert_eq!((first["state"].as_str(), first["transition"].as_str(), first["send"].as_str()), (Some("requested"), Some("SR-01"), Some("pending")));
    assert_eq!(first["requestedBy"], json!({"kind":"person","identity":"R · OS account r","identityStatus":"identity not verified"}));
    assert_eq!(first["generation"], crate::recovery::generation_ref(&g()).unwrap());
    assert!(first["stopRequestId"].as_str().unwrap().starts_with("stop:"));
    let sent = sr.sent("host-request:x:client:4", &json!(4)).unwrap();
    assert_eq!((sent["state"].as_str(), sent["clientRequest"].as_str()), (Some("sent"), Some("host-request:x:client:4")));
    assert!(sr.sent("again", &json!(5)).is_err(), "sent once");
    let accepted = sr.response(&json!({"id":4,"result":{}})).unwrap().unwrap();
    assert_eq!((accepted["state"].as_str(), accepted["response"].as_str(), accepted["turnOutcome"].as_str()), (Some("accepted"), Some("result"), Some("pending")), "an empty result is acceptance, not the turn's end");
    assert!(accepted.get("outcomeLabel").is_none());
    let settled = sr.turn_completed("interrupted").unwrap().unwrap();
    assert_eq!((settled["state"].as_str(), settled["transition"].as_str(), settled["outcomeLabel"].as_str(), settled["outcomeSource"].as_str()), (Some("settled"), Some("SR-06"), Some("interrupted by the person"), Some("observed")));
    assert!(sr.turn_completed("completed").unwrap().is_none(), "a settled request does not change");
    assert!(sr.generation_closed().unwrap().is_none(), "no SR-08 after a final status");
    for record in [first, sent, accepted, settled] {
        validate(&record).unwrap();
    }
}

#[test]
fn every_cause_and_final_status_has_its_schema_label() {
    for (cause, status, expected) in [
        (Cause::PersonInterrupt, "completed", "completed (stop requested)"),
        (Cause::PersonInterrupt, "failed", "failed (stop requested)"),
        (Cause::CodexStop, "interrupted", "interrupted by Stop Codex"),
        (Cause::CodexStop, "completed", "completed (Stop Codex requested)"),
        (Cause::CodexStop, "failed", "failed (Stop Codex requested)"),
    ] {
        let mut sr = requested(cause);
        sr.sent("cr", &json!(1)).unwrap();
        let settled = sr.turn_completed(status).unwrap().unwrap();
        assert_eq!(settled["outcomeLabel"], expected);
        assert_eq!(settled["transition"], if status == "interrupted" { "SR-06" } else { "SR-07" });
    }
    assert_eq!(label("quit", "unknown"), Some("interrupted by quit (final status not observed)"));
    assert_eq!(label("codex-stop", "inProgress"), None);
}

#[test]
fn closed_generation_refusal_wait_and_late_response_keep_their_own_rows() {
    // SR-10 then SR-08: no response and no turn end before the generation closed.
    let mut sr = requested(Cause::CodexStop);
    sr.sent("cr", &json!(9)).unwrap();
    let waited = sr.waiting_ended().unwrap().unwrap();
    assert_eq!((waited["state"].as_str(), waited["waitingEnded"].as_bool(), waited["transition"].as_str()), (Some("sent"), Some(true), Some("SR-10")));
    assert!(sr.waiting_ended().unwrap().is_none(), "recorded once");
    let unknown = sr.generation_closed().unwrap().unwrap();
    assert_eq!((unknown["state"].as_str(), unknown["response"].as_str(), unknown["turnOutcome"].as_str(), unknown["outcomeLabel"].as_str()),
        (Some("outcome-unknown"), Some("unknown-no-response"), Some("unknown"), Some("interrupted by Stop Codex (final status not observed)")));
    // What is shown for an outcome-unknown record says what is recorded, and does not say that
    // Codex's process stopped: the same record is written at a later start for an earlier App
    // session's request, where no stop of Codex was observed.
    let session = unknown["appSession"].as_str().unwrap().to_owned();
    for current in [session.as_str(), "a-later-session"] {
        let held = [json!({"kind":"session_started","session":session,"at":"t","previousSessionEnd":"none","candidate":"c"}), ledger_entry(&session, &unknown)];
        let shown = outcomes(&held, &[], current);
        let reading = shown["records"][0]["reading"].as_str().unwrap();
        assert_eq!(reading, "No final turn status is recorded for this stop request. That does not establish that Codex's process ended.");
        assert!(!reading.contains("Codex stopped") && !reading.contains("before Codex"), "{reading}");
    }
    // SR-05: Codex refused; the turn continues as observed until it ends.
    let mut refused = requested(Cause::PersonInterrupt);
    refused.sent("cr", &json!(2)).unwrap();
    let error = refused.response(&json!({"id":2,"error":{"code":-32600,"message":"no active turn"}})).unwrap().unwrap();
    assert_eq!((error["state"].as_str(), error["responseError"].as_str()), (Some("refused"), Some("no active turn")));
    assert_eq!(refused.turn_completed("completed").unwrap().unwrap()["outcomeLabel"], "completed (stop requested)");
    // SR-12: a response after turn/completed is recorded; the outcome is unchanged.
    let mut late = requested(Cause::PersonInterrupt);
    late.sent("cr", &json!(3)).unwrap();
    late.turn_completed("interrupted").unwrap().unwrap();
    let twelve = late.response(&json!({"id":3,"result":{}})).unwrap().unwrap();
    assert_eq!((twelve["transition"].as_str(), twelve["response"].as_str(), twelve["outcomeLabel"].as_str()), (Some("SR-12"), Some("result"), Some("interrupted by the person")));
    // SR-03: nothing sent (no write began).
    let mut unsent = requested(Cause::PersonInterrupt);
    let not_sent = unsent.not_sent("refused before sending: fixture").unwrap();
    assert_eq!((not_sent["state"].as_str(), not_sent["send"].as_str(), not_sent["response"].as_str()), (Some("not-sent"), Some("not-sent(not-ready)"), Some("not-applicable")));
    assert!(unsent.turn_completed("interrupted").unwrap().is_none(), "an unsent request never takes a turn's end");
    assert!(unsent.generation_closed().unwrap().is_none());
}

#[test]
fn a_record_the_schema_refuses_is_not_formed() {
    assert!(StopRequest::requested(&g(), "account", "thread", "turn", Cause::PersonInterrupt, &person("")).is_err(), "home must be the App-owned home class");
    assert!(StopRequest::requested(&json!({"appSession":"s"}), "H-acct", "thread", "turn", Cause::PersonInterrupt, &person("")).is_err(), "full generation required");
    assert_eq!(person("  ")["identity"], "the person (no name set in the App)");
    assert_eq!(home_class("account"), Some("H-acct"));
    assert_eq!(home_class("api-key"), Some("H-key"));
    assert_eq!(home_class("probe"), None);
}

#[test]
fn codex_stop_entry_carries_the_confirmed_list_and_validates() {
    let material = json!({"observedLiveTurns":[{"generation":g(),"threadId":"thread","turnId":"turn"}],
        "observedOutstandingRequests":[{"generation":g(),"requestIdentity":7,"method":"item/tool/requestUserInput","threadId":"thread","turnId":"turn"}]});
    let entry = codex_stop_entry("session-a", &person("R"), "H-acct", true, &material).unwrap();
    assert_eq!(entry["kind"], "codex_stop");
    assert_eq!(entry["homes"], json!(["H-acct"]));
    assert_eq!(entry["restart"], true);
    assert_eq!(entry["liveTurns"], json!([{"threadId":"thread","turnId":"turn"}]));
    assert_eq!(entry["outstandingEntries"][0]["requestIdentity"], "7");
    assert_eq!(entry["outstandingEntries"][0]["subject"], json!({"threadId":"thread","turnId":"turn"}));
    assert_eq!(entry["outstandingEntries"][0]["generation"], crate::recovery::generation_ref(&g()).unwrap());
    assert!(codex_stop_entry("session-a", &person("R"), "account", false, &material).is_err(), "ledger schema refuses a home that is not H-acct/H-key");
}

#[test]
fn read_back_after_relaunch_keeps_labels_and_claims_no_unrecorded_end() {
    let mut settled = requested(Cause::CodexStop);
    settled.sent("cr", &json!(1)).unwrap();
    settled.turn_completed("interrupted").unwrap();
    let mut open = StopRequest::requested(&g(), "H-key", "thread-2", "turn-2", Cause::PersonInterrupt, &person("")).unwrap();
    open.sent("cr", &json!(2)).unwrap();
    // The earlier session has its start record in the ledger, as every session that wrote
    // through the App has: its end is what the later session's start established.
    let ledger = json!([
        {"kind":"session_started","session":"session-a","at":"t","previousSessionEnd":"none","candidate":"c"},
        ledger_entry("session-a", settled.record()),
        ledger_entry("session-a", open.record()),
        {"kind":"stop_request","session":"session-a","at":"t","record":{"kind":"stop_request"}},
    ]);
    // Without that start record nothing establishes that the session has ended: the records are
    // shown as recorded, no label is derived for the open one, it is not called an earlier
    // session, and the view says so as a limit. A recorded label stays what was recorded.
    let orphaned: Vec<Value> = ledger.as_array().unwrap().iter().filter(|e| e["kind"] != "session_started").cloned().collect();
    let orphan = outcomes(&orphaned, &[], "session-b");
    let rows = orphan["records"].as_array().unwrap();
    assert_eq!((rows[1]["label"].as_str(), rows[1]["labelDerived"].as_bool(), rows[1]["reading"].as_str()), (None, Some(false), Some(SOURCE_END_NOT_ESTABLISHED)), "{}", rows[1]);
    assert_eq!((rows[1]["earlierSession"].as_bool(), rows[1]["sourceSessionEnd"].as_str()), (Some(false), Some("not-established")));
    assert!(!rows[1]["reading"].as_str().unwrap().contains("session ended"), "no ending is asserted");
    assert_eq!((rows[0]["label"].as_str(), rows[0]["labelDerived"].as_bool(), rows[0]["sourceSessionEnd"].as_str()), (Some("interrupted by Stop Codex"), Some(false), Some("not-established")));
    assert!(orphan["limits"].as_array().unwrap().iter().any(|l| l == SOURCE_SESSION_UNAVAILABLE), "{orphan}");
    let view = outcomes(ledger.as_array().unwrap(), &[], "session-b");
    assert!(!view["limits"].as_array().unwrap().iter().any(|l| l == SOURCE_SESSION_UNAVAILABLE));
    assert_eq!(view["records"][1]["sourceSessionEnd"], "established");
    let rows = view["records"].as_array().unwrap();
    assert_eq!(rows.len(), 2);
    assert_eq!((rows[0]["label"].as_str(), rows[0]["codexReported"].as_str(), rows[0]["earlierSession"].as_bool()), (Some("interrupted by Stop Codex"), Some("interrupted"), Some(true)));
    assert_eq!(rows[0]["persistence"], "recorded in the App ledger");
    // A request left `sent` by an earlier session: its outcome is unknown, never inferred.
    assert_eq!(rows[1]["label"], "outcome unknown (stop requested)");
    assert!(rows[1]["codexReported"].is_null());
    assert!(rows[1]["reading"].as_str().unwrap().contains("ended before a final status was recorded"));
    assert_eq!((rows[1]["labelDerived"].as_bool(), rows[0]["labelDerived"].as_bool()), (Some(true), Some(false)), "a derived label is marked; a recorded one is not");
    assert_eq!(view["limits"].as_array().unwrap().len(), 1, "an invalid record is a visible limit, not a row");
    // The same request in this session, not yet in the ledger: the newer live record is shown with its persistence.
    let mut later = settled.record().clone();
    later["transition"] = json!("SR-12");
    later["response"] = json!("result");
    let current = outcomes(ledger.as_array().unwrap(), &[(later, "not yet written to the App ledger; kept in this App process".into())], "session-a");
    assert_eq!(current["records"][0]["transition"], "SR-12");
    assert_eq!(current["records"][0]["earlierSession"], false);
    assert!(current["records"][0]["persistence"].as_str().unwrap().starts_with("not yet written"));
    assert_eq!(current["records"][1]["label"], Value::Null, "a request of this session without a final status has no label yet");
}

// The view's index reads each appended ledger entry once, and is rebuilt if
// the ledger no longer continues what it read.
#[test]
fn the_ledger_index_reads_appended_entries_once_and_rebuilds_on_a_different_ledger() {
    let g = json!({"appSession":"session-a","home":"native-home","spawnCounter":1});
    let mut request = StopRequest::requested(&g, "H-acct", "thread", "turn", Cause::PersonInterrupt, &person("")).unwrap();
    let first = ledger_entry("session-a", request.record());
    request.sent("app:client:1", &json!(1)).unwrap();
    let second = ledger_entry("session-a", request.record());
    let bad = json!({"kind":"stop_request","session":"session-a","at":"t","record":{"kind":"stop_request"}});
    // The earlier session's start record, as a real ledger has it (without one the view adds its
    // own limit for a source session whose end is not established).
    let started = json!({"kind":"session_started","session":"session-a","at":"t","previousSessionEnd":"none","candidate":"c"});
    let mut index = LedgerIndex::default();
    index.update(json!([started.clone(), first.clone(), bad.clone()]).as_array().unwrap());
    index.update(json!([started.clone(), first.clone(), bad.clone()]).as_array().unwrap());
    let view = outcomes_indexed(&index, &[], "session-b");
    assert_eq!(view["limits"].as_array().unwrap().len(), 1, "an entry already read is not read again");
    assert!(index.contains(&first) && !index.contains(&second));
    index.update(json!([started.clone(), first.clone(), bad.clone(), second.clone()]).as_array().unwrap());
    assert!(index.contains(&second));
    assert_eq!(outcomes_indexed(&index, &[], "session-b")["records"][0]["transition"], "SR-02");
    index.update(json!([started.clone(), second.clone()]).as_array().unwrap());
    assert!(!index.contains(&first) && index.contains(&second), "a ledger that does not continue the read prefix is read afresh");
    assert!(outcomes_indexed(&index, &[], "session-b")["limits"].as_array().unwrap().is_empty());
}

// ---- SR-13 (send unknown) and rows of the 0.2 schema.

const SEND_UNKNOWN: &str = "Stop requested; the interrupt's write began and its completion was not observed, so whether it reached Codex is not known.";
const WRITE_FAILED_OLD: &str = "An earlier App build recorded an interrupt write failure; whether the interrupt reached Codex is not established.";

fn v0_2() -> jsonschema::Validator {
    jsonschema::options().offline().build(&serde_json::from_str::<Value>(SCHEMA_V0_2).unwrap()).unwrap()
}
/// A row as the 0.2 App wrote it for a write that failed after it began.
fn old_write_failed(cause: Cause) -> Value {
    let mut r = requested(cause).record().clone();
    for (k, v) in [("send", json!("not-sent(write-failed)")), ("response", json!("not-applicable")), ("responseError", json!("write failed: Broken pipe (os error 32)")), ("state", json!("not-sent")), ("transition", json!("SR-03"))] {
        r[k] = v;
    }
    r
}
/// A row as the 0.2 App wrote it for a request refused before any write.
fn old_not_ready(cause: Cause) -> Value {
    let mut r = old_write_failed(cause);
    r["send"] = json!("not-sent(not-ready)");
    r["responseError"] = json!("refused before sending: fixture reason");
    r
}

#[test]
fn the_schema_version_moved_and_the_earlier_one_is_kept() {
    let current: Value = serde_json::from_str(SCHEMA).unwrap();
    let earlier: Value = serde_json::from_str(SCHEMA_V0_2).unwrap();
    assert_eq!(current["$id"], "urn:chirality:app-v4:del-01-02:stop-request:0.3");
    assert_eq!(earlier["$id"], "urn:chirality:app-v4:del-01-02:stop-request:0.2");
    assert!(!earlier["properties"]["state"]["enum"].as_array().unwrap().contains(&json!("send-unknown")));
    // Every 0.2 row stays valid under 0.3 and is read.
    for row in [requested(Cause::Quit).record().clone(), old_write_failed(Cause::CodexStop), old_not_ready(Cause::PersonInterrupt)] {
        assert!(v0_2().is_valid(&row), "{row}");
        validate(&row).unwrap();
        validate_stored(&row).unwrap();
        StopRequest::from_record(&row).unwrap();
    }
}

#[test]
fn sr13_send_unknown_is_neither_sent_nor_not_sent_and_takes_no_later_transition() {
    for cause in [Cause::PersonInterrupt, Cause::Quit, Cause::CodexStop] {
        let mut sr = requested(cause);
        let record = sr.send_unknown("host-request:x:client:9").unwrap();
        assert_eq!((record["state"].as_str(), record["send"].as_str(), record["response"].as_str(), record["transition"].as_str()),
            (Some("send-unknown"), Some("unknown(write-incomplete)"), Some("unknown-no-response"), Some("SR-13")));
        assert_eq!((record["turnOutcome"].as_str(), record["outcomeSource"].as_str()), (Some("pending"), Some("not-observed")));
        assert_eq!(record["clientRequest"], "host-request:x:client:9");
        assert!(record.get("outcomeLabel").is_none());
        assert!(!v0_2().is_valid(&record), "a 0.3 state");
        // Only from requested, and once.
        assert!(sr.send_unknown("again").is_err());
        assert!(sr.not_sent("x").is_err() && sr.sent("x", &json!(1)).is_err());
        // No response is linked, no turn end, no SR-08 at the generation's
        // end or at a later App's start, no wait end, no recovery.
        assert!(sr.response(&json!({"id":9,"result":{}})).unwrap().is_none());
        assert!(sr.turn_completed("interrupted").unwrap().is_none());
        assert!(sr.generation_closed().unwrap().is_none());
        assert!(sr.waiting_ended().unwrap().is_none());
        assert!(sr.recovered("interrupted").unwrap().is_none());
        assert!(closed_at_restart(sr.record()).unwrap().is_none());
        assert_eq!(sr.record()["state"], "send-unknown");
    }
    // Not reachable from any later state.
    let mut sent = requested(Cause::CodexStop);
    sent.sent("cr", &json!(1)).unwrap();
    assert!(sent.send_unknown("cr").is_err());
    let mut unsent = requested(Cause::CodexStop);
    unsent.not_sent("refused before sending: x").unwrap();
    assert!(unsent.send_unknown("cr").is_err());
}

#[test]
fn the_schema_holds_send_unknown_to_its_own_values() {
    let mut sr = requested(Cause::CodexStop);
    let good = sr.send_unknown("cr").unwrap();
    for (key, value) in [("send", json!("sent")), ("send", json!("not-sent(write-failed)")), ("response", json!("pending")), ("response", json!("result")), ("turnOutcome", json!("interrupted"))] {
        let mut bad = good.clone();
        bad[key] = value.clone();
        assert!(validate(&bad).is_err(), "send-unknown with {key}={value}");
    }
    let mut no_request = good.clone();
    no_request.as_object_mut().unwrap().remove("clientRequest");
    assert!(validate(&no_request).is_err(), "an attempted write names its client request");
    for state in ["sent", "not-sent", "requested", "outcome-unknown"] {
        let mut bad = good.clone();
        bad["state"] = json!(state);
        assert!(validate(&bad).is_err(), "unknown(write-incomplete) only with send-unknown, not {state}");
    }
}

#[test]
fn every_reading_of_send_unknown_and_of_old_rows_says_neither_sent_nor_interrupted() {
    let mut unknown = requested(Cause::CodexStop);
    let unknown = unknown.send_unknown("cr").unwrap();
    let cases = [
        (unknown, SEND_UNKNOWN.to_owned()),
        (old_write_failed(Cause::PersonInterrupt), WRITE_FAILED_OLD.to_owned()),
        (old_write_failed(Cause::Quit), WRITE_FAILED_OLD.to_owned()),
        (old_not_ready(Cause::CodexStop), "Stop not sent: refused before sending: fixture reason".to_owned()),
    ];
    for (record, expected) in cases {
        let session = record["appSession"].as_str().unwrap().to_owned();
        let entry = ledger_entry(&session, &record);
        // In this App session (live and from the ledger) and in a later one.
        for (held, live, current) in [(vec![], vec![(record.clone(), "kept".to_owned())], session.as_str()), (vec![entry.clone()], vec![], session.as_str()), (vec![entry.clone()], vec![], "later-session")] {
            let view = outcomes(&held, &live, current);
            let row = &view["records"][0];
            // In a later session with no start record for session-a, unit 1's
            // source rule reads the row as another session's whose end is not
            // established: that sentence comes first, and a send-unknown row
            // keeps its own reading after it.
            let expected = if current != session && record["state"] == "send-unknown" {
                format!("Recorded by another App session whose end is not established. No final status is recorded for this turn, and no label is derived. {expected}")
            } else {
                expected.clone()
            };
            assert_eq!(row["reading"], expected.as_str(), "{row}");
            assert!(row["label"].is_null() && row["labelDerived"] == false && row["codexReported"].is_null(), "{row}");
            let shown = format!("{} {} {}", row["reading"], row["label"], row["state"]);
            assert!(!shown.contains("interrupted"), "{shown}");
            if record["send"] != "not-sent(not-ready)" {
                assert!(!shown.contains("not sent") && !shown.contains("was sent."), "{shown}");
            }
        }
    }
}

#[test]
fn the_ledger_index_reads_rows_of_both_versions() {
    let mut unknown = requested(Cause::Quit);
    let unknown = unknown.send_unknown("cr").unwrap();
    let rows = vec![ledger_entry("session-a", &old_write_failed(Cause::Quit)), ledger_entry("session-a", &unknown)];
    let mut index = LedgerIndex::default();
    index.update(&rows);
    assert!(index.limits.is_empty(), "{:?}", index.limits);
    let all = index.all_for(&crate::recovery::generation_ref(&g()).unwrap(), "thread", "turn");
    assert_eq!(all.len(), 2);
    assert!(index.contains(&rows[0]) && index.contains(&rows[1]));
}

#[test]
fn the_startup_closure_and_session_end_leave_send_unknown_and_old_rows_as_they_are() {
    let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("sr13-").unwrap());
    std::fs::create_dir_all(&root).unwrap();
    let path = root.join("ledger.jsonl");
    let mut unknown = requested(Cause::CodexStop);
    let unknown = unknown.send_unknown("cr").unwrap();
    let records = [unknown.clone(), old_write_failed(Cause::PersonInterrupt), old_not_ready(Cause::Quit)];
    {
        let mut ledger = crate::recovery::RecoveryLedger::open(path.clone()).unwrap();
        ledger.start_session("session-a", "candidate").unwrap();
        for r in &records { ledger.append(ledger_entry("session-a", r)).unwrap(); }
        // session_ended carries the state as held; its schema admits it.
        let stops: Vec<Value> = records.iter().map(|r| json!({"stopRequestId":r["stopRequestId"],"state":r["state"]})).collect();
        let ids: Vec<String> = records.iter().map(|r| r["stopRequestId"].as_str().unwrap().to_owned()).collect();
        let (how, carried) = crate::app_quit::session_end(Some(ids), &records);
        assert_eq!((how, carried.clone()), ("quit", stops.clone()));
        assert_eq!(carried[0]["state"], "send-unknown");
        ledger.append(crate::recovery::RecoveryLedger::session_end_entry("session-a", "quit", &carried).unwrap()).unwrap();
    }
    let mut later = crate::recovery::RecoveryLedger::open(path.clone()).unwrap();
    let before = crate::recovery::stored_entries(&path).len();
    later.start_session("session-b", "candidate").unwrap();
    assert!(later.close_earlier_stop_requests("session-b").is_empty());
    let added: Vec<Value> = crate::recovery::stored_entries(&path)[before..].iter().filter(|e| e["kind"] == "stop_request").cloned().collect();
    assert!(added.is_empty(), "nothing written for them: {added:?}");
    std::fs::remove_dir_all(root).unwrap();
}
