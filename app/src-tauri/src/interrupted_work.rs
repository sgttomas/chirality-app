//! What the App session before this one last recorded as a turn in progress,
//! for the window to say after a relaunch (DEL-01-02 REQ-005, AC-006).
//!
//! A reading of the App's own records and nothing else: the CV-19 restart
//! facts the custody view derives from the ledger (`recovery::restart_facts`),
//! kept to one home, and execution custody's recovery reading of each, joined
//! by the full key (the source generation and the thread). It writes no
//! record, sends nothing and resumes nothing. A turn the App has not read
//! back, could not read back or did not find is reported as that, never as an
//! outcome; a reading another home holds is never joined.
//!
//! What this cannot show. Restart facts come only from the App session
//! immediately before this one. With sessions A, then B, then C, where B only
//! carried an A-generation conversation as recovery state (pending or
//! unavailable), C has no restart fact for it: the conversation drops out of
//! this reading although C's recovery still adopts and reads it, and its
//! outcome then appears only in History. Recovery readings are held in this
//! App process only, so a read B made is not shown in C either. Neither is
//! given a status here.
use crate::recovery::{generation_ref, restart_facts, RestartFact};
use crate::runtime_session::HomeSession;
use serde_json::{json, Value};

const STANDING: &str = "Conversations of this home whose last record from the App session before this one is a turn in progress, how that session's end is recorded, and what the App's recovery reads of Codex's history said of that turn in this App process. Reading back resumes nothing and resends nothing.";

/// The home a status reply is the status of, said in the reply itself: its
/// mode class, the App-owned home code and the physical home (null where not
/// established). The window shows a reading as a home's only when the reply,
/// the active home and any running generation all name that same home.
pub(crate) fn status_home(home: &HomeSession) -> Value {
    json!({"modeHomeClass": home.class().as_str(),
        "home": crate::stop_records::home_class(home.class().as_str()),
        "physicalHome": home.host_config.as_ref().ok().map(crate::hosting::physical_home)})
}

/// The reading for `home`, the home `host_status` is the status of. Takes
/// from under the Host lock only a handle on the held ledger entries, then
/// one lookup per restart fact of this home; the ledger scan runs outside it.
pub(crate) fn read_home(home: &HomeSession) -> Value {
    let app_home = crate::stop_records::home_class(home.class().as_str());
    let physical = home.host_config.as_ref().ok().map(crate::hosting::physical_home);
    let (session, rows) = home.host.held_ledger();
    let facts = rows.map(|rows| restart_facts(&session, &rows).0).unwrap_or_default();
    project(app_home, physical.as_deref(), facts, |keys| home.host.recovery_readings(keys))
}

/// `facts` kept to the home named by both its App-owned home class and its
/// physical home; with either unknown, none is this home's. `readings` gives
/// execution custody's reading for each full key, in order.
pub(crate) fn project(app_home: Option<&str>, physical: Option<&str>, facts: Vec<RestartFact>, readings: impl FnOnce(&[(String, String)]) -> Vec<Option<Value>>) -> Value {
    let (Some(app_home), Some(physical)) = (app_home, physical) else {
        return json!({"home":app_home,"physicalHome":physical,"conversations":[],"standing":STANDING,
            "limit":"This home's identity is not established; no restart fact is shown as this home's"});
    };
    let mine: Vec<(RestartFact, (String, String))> = facts.into_iter().filter_map(|fact| {
        if fact.event["home"] != app_home || fact.source["home"] != physical { return None; }
        let key = (generation_ref(&fact.source).ok()?, fact.event["threadId"].as_str()?.to_owned());
        Some((fact, key))
    }).collect();
    let found = if mine.is_empty() { Vec::new() } else { readings(&mine.iter().map(|(_, key)| key.clone()).collect::<Vec<_>>()) };
    let conversations: Vec<Value> = mine.iter().enumerate().filter_map(|(n, (fact, (_, thread)))| {
        let reading = found.get(n).cloned().flatten();
        let turns: Vec<Value> = fact.event["liveTurnsAtEnd"].as_array()?.iter().filter_map(|t| t["turnId"].as_str())
            .map(|turn| turn_reading(turn, reading.as_ref())).collect();
        if turns.is_empty() { return None; }
        let mut entry = json!({"threadId":thread,"home":app_home,"physicalHome":physical,"sourceGeneration":fact.source,
            "priorSession":fact.event["priorSession"],"priorSessionEnd":fact.event["priorSessionEnd"],
            "lastRecordedState":fact.execution["state"],"turns":turns});
        // A loss the App observed while its session went on: the record is
        // from when Codex ended or was stopped, before that session ended.
        if let Some(cause) = fact.execution["lostCause"].as_str().filter(|c| matches!(*c, "supplier-exit" | "supplier-stop")) {
            entry["lostBeforeSessionEnd"] = json!(cause);
        }
        Some(entry)
    }).collect();
    json!({"home":app_home,"physicalHome":physical,"conversations":conversations,"standing":STANDING})
}

/// One turn: the latest recovery attempt's outcome as `current`, and, where
/// that attempt read no status but an earlier one did, that earlier reading
/// apart as `earlier`. `reading`: execution custody's reading of the full key.
fn turn_reading(turn: &str, reading: Option<&Value>) -> Value {
    let Some(reading) = reading else {
        // This App process holds no custody of the key: never read here.
        return json!({"turnId":turn,"current":{"reading":"not-read","attempts":0}});
    };
    let attempts = reading["attempts"].as_u64().unwrap_or(0);
    let read = &reading["lastRead"];
    let of_read = |read: &Value| -> Value {
        let mut at = json!({"attempt":read["attempt"],"at":read["at"],"readBy":read["generation"]});
        if read["turnId"] != turn { at["reading"] = json!("turn-not-named"); return at; }
        match read["supplierStatus"].as_str() {
            Some("absent") => at["reading"] = json!("not-in-history"),
            Some(status) => { at["reading"] = json!("read"); at["codexStatus"] = json!(status); }
            None => at["reading"] = json!("turn-not-named"),
        }
        at
    };
    let latest_read = read.is_object() && read["attempt"].as_u64() == Some(attempts);
    let current = match reading["state"].as_str() {
        Some("indexed") if latest_read => of_read(read),
        Some("unavailable") => json!({"reading":"unavailable","attempt":attempts,"reason":reading["unavailableReason"]}),
        // Recovery pending or under way: no attempt has completed since.
        Some("recovery-pending" | "recovering") => json!({"reading":"not-read","attempts":attempts}),
        _ => json!({"reading":"not-established"}),
    };
    let mut entry = json!({"turnId":turn,"current":current});
    if read.is_object() && !latest_read {
        let earlier = of_read(read);
        if matches!(earlier["reading"].as_str(), Some("read" | "not-in-history")) { entry["earlier"] = earlier; }
    }
    entry
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::recovery::generation_from_ref;
    const PHYS: &str = "app-home:aaaa";
    fn g(session: &str, home: &str) -> Value { json!({"appSession":session,"home":home,"spawnCounter":1}) }
    fn fact(thread: &str, turn: &str, home: &str, physical: &str, end: &str) -> RestartFact {
        let source = g("app-session:A", physical);
        RestartFact { event: json!({"kind":"app_restart_interruption","threadId":thread,"home":home,"priorSession":"app-session:A","priorSessionEnd":end,"liveTurnsAtEnd":[{"threadId":thread,"turnId":turn}]}),
            source, execution: json!({"state":"turn-live","liveTurn":turn}) }
    }
    fn key(physical: &str, thread: &str) -> (String, String) { (generation_ref(&g("app-session:A", physical)).unwrap(), thread.to_owned()) }
    fn read(attempt: u64, turn: &str, status: &str) -> Value { json!({"attempt":attempt,"generation":"gen-B","at":"t","turnId":turn,"supplierStatus":status}) }
    fn custody(state: &str, attempts: u64, last: Option<Value>, reason: Option<&str>) -> Value { json!({"state":state,"attempts":attempts,"unavailableReason":reason,"lastRead":last}) }
    /// The reading of each key the closure is asked for, from `held`.
    fn lookup(held: Vec<((String, String), Value)>) -> impl FnOnce(&[(String, String)]) -> Vec<Option<Value>> {
        move |keys| keys.iter().map(|k| held.iter().find(|(h, _)| h == k).map(|(_, v)| v.clone())).collect()
    }
    fn current(view: &Value, n: usize) -> Value { view["conversations"][n]["turns"][0]["current"].clone() }

    #[test]
    fn two_homes_with_equal_conversation_and_turn_ids_never_take_each_others_reading() {
        let facts = || vec![fact("t", "u", "H-acct", PHYS, "ended-without-record"), fact("t", "u", "H-key", "app-home:bbbb", "system-terminated"), fact("t", "u", "H-acct", "app-home:cccc", "ended-without-record")];
        let held = || vec![(key(PHYS, "t"), custody("unavailable", 1, None, Some("Codex did not answer"))),
            (key("app-home:bbbb", "t"), custody("indexed", 1, Some(read(1, "u", "completed")), None)),
            (key("app-home:cccc", "t"), custody("indexed", 1, Some(read(1, "u", "failed")), None))];
        let view = project(Some("H-acct"), Some(PHYS), facts(), lookup(held()));
        assert_eq!(view["conversations"].as_array().unwrap().len(), 1, "another class, or the same class over another physical home, is not this home");
        assert_eq!((view["home"].as_str(), view["physicalHome"].as_str()), (Some("H-acct"), Some(PHYS)));
        let entry = &view["conversations"][0];
        assert_eq!((entry["home"].as_str(), entry["physicalHome"].as_str(), entry["priorSessionEnd"].as_str()), (Some("H-acct"), Some(PHYS), Some("ended-without-record")));
        assert_eq!(entry["sourceGeneration"], g("app-session:A", PHYS));
        assert_eq!(current(&view, 0), json!({"reading":"unavailable","attempt":1,"reason":"Codex did not answer"}), "the other homes' completed and failed reads are not this one's");
        let key_view = project(Some("H-key"), Some("app-home:bbbb"), facts(), lookup(held()));
        assert_eq!(current(&key_view, 0)["codexStatus"], "completed");
        for (home, physical) in [(None, Some(PHYS)), (Some("H-acct"), None)] {
            let unknown = project(home, physical, facts(), lookup(held()));
            assert_eq!(unknown["conversations"], json!([]), "a home not established shows nothing as its own");
            assert!(unknown["limit"].is_string());
        }
    }

    #[test]
    fn the_latest_attempt_is_the_current_reading_and_an_earlier_read_stays_apart() {
        let view = |state: &str, attempts: u64, last: Option<Value>, reason: Option<&str>| current(&project(Some("H-acct"), Some(PHYS), vec![fact("t", "u", "H-acct", PHYS, "ended-without-record")], lookup(vec![(key(PHYS, "t"), custody(state, attempts, last, reason))])), 0);
        assert_eq!(view("indexed", 2, Some(read(2, "u", "interrupted")), None), json!({"reading":"read","codexStatus":"interrupted","attempt":2,"at":"t","readBy":"gen-B"}));
        assert_eq!(view("indexed", 1, Some(read(1, "u", "absent")), None)["reading"], "not-in-history");
        assert_eq!(view("indexed", 1, Some(read(1, "other", "completed")), None)["reading"], "turn-not-named", "a read naming another turn says nothing of this one");
        assert_eq!(view("indexed", 1, None, None), json!({"reading":"not-established"}));
        assert_eq!(view("recovering", 3, None, None), json!({"reading":"not-read","attempts":3}));
        assert_eq!(view("recovery-pending", 0, None, None), json!({"reading":"not-read","attempts":0}));
        // A later failed attempt after an earlier read: the failure is current; the read is earlier, attributed.
        let both = project(Some("H-acct"), Some(PHYS), vec![fact("t", "u", "H-acct", PHYS, "ended-without-record")], lookup(vec![(key(PHYS, "t"), custody("unavailable", 2, Some(read(1, "u", "completed")), Some("no answer")))]));
        let turn = &both["conversations"][0]["turns"][0];
        assert_eq!(turn["current"], json!({"reading":"unavailable","attempt":2,"reason":"no answer"}));
        assert_eq!(turn["earlier"], json!({"reading":"read","codexStatus":"completed","attempt":1,"at":"t","readBy":"gen-B"}));
        assert!(view("unavailable", 2, Some(read(1, "u", "completed")), Some("no answer")).get("codexStatus").is_none());
        let pending = project(Some("H-acct"), Some(PHYS), vec![fact("t", "u", "H-acct", PHYS, "ended-without-record")], lookup(vec![(key(PHYS, "t"), custody("recovering", 2, Some(read(1, "u", "absent")), None))]));
        assert_eq!(pending["conversations"][0]["turns"][0]["earlier"]["reading"], "not-in-history");
        // No custody of the key in this process.
        let none = project(Some("H-acct"), Some(PHYS), vec![fact("t", "u", "H-acct", PHYS, "ended-without-record")], lookup(vec![]));
        assert_eq!(current(&none, 0), json!({"reading":"not-read","attempts":0}));
    }

    #[test]
    fn a_loss_recorded_before_the_session_ended_is_carried() {
        let mut lost = fact("t", "u", "H-acct", PHYS, "ended-without-record");
        lost.execution = json!({"state":"observation-lost","liveTurn":"u","lostCause":"supplier-exit"});
        let mut quit = fact("q", "u", "H-acct", PHYS, "quit-with-live-work");
        quit.execution = json!({"state":"observation-lost","liveTurn":"u","lostCause":"app-quit"});
        let view = project(Some("H-acct"), Some(PHYS), vec![lost, quit, fact("l", "u", "H-acct", PHYS, "system-terminated")], lookup(vec![]));
        let entries = view["conversations"].as_array().unwrap();
        assert_eq!((entries[0]["lastRecordedState"].as_str(), entries[0]["lostBeforeSessionEnd"].as_str()), (Some("observation-lost"), Some("supplier-exit")));
        assert!(entries[1].get("lostBeforeSessionEnd").is_none(), "a loss at the quit is not before the session's end");
        assert_eq!((entries[2]["lastRecordedState"].as_str(), entries[2]["priorSessionEnd"].as_str()), (Some("turn-live"), Some("system-terminated")));
        assert!(entries[2].get("lostBeforeSessionEnd").is_none());
    }

    /// Sessions A, B, C over one ledger: A leaves a turn live and ends with no
    /// record; B adopts A's conversation and its read fails (unavailable);
    /// C has no restart fact for it, because A is not C's preceding session.
    #[test]
    fn a_conversation_carried_through_a_second_relaunch_drops_out_of_this_reading() {
        let gen_a = generation_ref(&g("A", PHYS)).unwrap();
        let index = |session: &str, state: &str| json!({"kind":"conversation_index","session":session,"at":"t","threadId":"t","home":"H-acct","lastLoadedGeneration":gen_a,"lastObservedExecution":{"state":state,"at":"t","liveTurn":"u","openItems":[]}});
        let mut rows = vec![json!({"kind":"session_started","session":"A","at":"t0"}), index("A", "turn-live"),
            json!({"kind":"session_started","session":"B","previousSession":"A","at":"t1"})];
        let (in_b, _) = restart_facts("B", &rows);
        assert_eq!(in_b.len(), 1);
        assert_eq!((in_b[0].event["priorSessionEnd"].as_str(), generation_from_ref(&gen_a).unwrap()), (Some("ended-without-record"), in_b[0].source.clone()));
        let b = project(Some("H-acct"), Some(PHYS), in_b, lookup(vec![(key_for(&gen_a), custody("unavailable", 1, None, Some("no answer")))]));
        assert_eq!(current(&b, 0)["reading"], "unavailable");
        // B records the conversation as unavailable, then ends; C starts.
        rows.push(index("B", "unavailable"));
        rows.push(json!({"kind":"session_ended","session":"B","at":"t2","how":"quit"}));
        rows.push(json!({"kind":"session_started","session":"C","previousSession":"B","at":"t3"}));
        let (in_c, _) = restart_facts("C", &rows);
        assert!(in_c.is_empty(), "C's reading says nothing of the conversation, though recovery still holds it unsettled");
        assert_eq!(project(Some("H-acct"), Some(PHYS), in_c, lookup(vec![]))["conversations"], json!([]));
    }
    fn key_for(reference: &str) -> (String, String) { (reference.to_owned(), "t".to_owned()) }

    #[test]
    fn nothing_is_reported_without_a_restart_fact_and_a_fact_with_no_turn_is_skipped() {
        assert_eq!(project(Some("H-acct"), Some(PHYS), vec![], |_| panic!("no lookup without a fact"))["conversations"], json!([]));
        let mut empty = fact("t", "u", "H-acct", PHYS, "ended-without-record");
        empty.event["liveTurnsAtEnd"] = json!([]);
        assert_eq!(project(Some("H-acct"), Some(PHYS), vec![empty], lookup(vec![]))["conversations"], json!([]));
    }
}
