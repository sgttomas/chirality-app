//! REC stop requests: schema copy, transitions SR-01…SR-12, labels, the
//! `codex_stop` ledger entry and the read-back after a relaunch.
use super::*;

fn g() -> Value {
    json!({"appSession":"session-a","home":"native-home","spawnCounter":1})
}
fn requested(cause: Cause) -> StopRequest {
    StopRequest::requested(&g(), "H-acct", "thread", "turn", cause, &person("R · OS account r")).unwrap()
}

#[test]
fn embedded_schema_is_the_design_schema_and_its_examples_hold() {
    assert_eq!(SCHEMA.as_bytes(), include_bytes!("../../../execution/PKG-01/DEL-01-02/Design/recovery.stop-request.schema.json"), "embedded copy is byte-identical to the Design schema");
    let valid: Value = serde_json::from_str(include_str!("../../../execution/PKG-01/DEL-01-02/Design/recovery.stop-request.example.valid.json")).unwrap();
    validate(&valid).unwrap();
    let invalid: Value = serde_json::from_str(include_str!("../../../execution/PKG-01/DEL-01-02/Design/recovery.stop-request.example.invalid.json")).unwrap();
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
    // SR-03: nothing sent.
    let mut unsent = requested(Cause::PersonInterrupt);
    let not_sent = unsent.not_sent(true, "write failed: broken pipe").unwrap();
    assert_eq!((not_sent["state"].as_str(), not_sent["send"].as_str(), not_sent["response"].as_str()), (Some("not-sent"), Some("not-sent(write-failed)"), Some("not-applicable")));
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
    let ledger = json!({"entries":[
        ledger_entry("session-a", settled.record()),
        ledger_entry("session-a", open.record()),
        {"kind":"stop_request","session":"session-a","at":"t","record":{"kind":"stop_request"}},
    ]});
    let view = outcomes(Some(&ledger), &[], "session-b");
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
    let current = outcomes(Some(&ledger), &[(later, "not yet written to the App ledger; kept in this App process".into())], "session-a");
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
    let mut index = LedgerIndex::default();
    index.update(Some(&json!({"entries":[first.clone(), bad.clone()]})));
    index.update(Some(&json!({"entries":[first.clone(), bad.clone()]})));
    let view = outcomes_indexed(&index, &[], "session-b");
    assert_eq!(view["limits"].as_array().unwrap().len(), 1, "an entry already read is not read again");
    assert!(index.contains(&first) && !index.contains(&second));
    index.update(Some(&json!({"entries":[first.clone(), bad.clone(), second.clone()]})));
    assert!(index.contains(&second));
    assert_eq!(outcomes_indexed(&index, &[], "session-b")["records"][0]["transition"], "SR-02");
    index.update(Some(&json!({"entries":[second.clone()]})));
    assert!(!index.contains(&first) && index.contains(&second), "a ledger that does not continue the read prefix is read afresh");
    assert!(outcomes_indexed(&index, &[], "session-b")["limits"].as_array().unwrap().is_empty());
}
