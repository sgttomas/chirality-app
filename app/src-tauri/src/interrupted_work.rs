//! What an earlier App session left with a turn live, for the window to say
//! after a relaunch (DEL-01-02 REQ-005, AC-006).
//!
//! A reading of the host's own recovery custody view and nothing else: the
//! restart facts it derives from the ledger, and what Codex's history said
//! when the host read each conversation back. It writes no record, sends
//! nothing and resumes nothing. A turn the host has not read back, could not
//! read back or did not find is reported as that, never as an outcome.
use serde_json::{json, Value};

/// `custody`: `RecoveryCustodyView::snapshot()` of one home's host.
pub(crate) fn read(custody: &Value) -> Value {
    let list = |value: &Value| value.as_array().cloned().unwrap_or_default();
    let events = list(&custody["live"]["events"]);
    let observations = list(&custody["live"]["observations"]);
    let mut conversations = Vec::new();
    for event in list(&custody["restartEvents"]) {
        let (Some(thread), Some(prior_end)) = (event["threadId"].as_str(), event["priorSessionEnd"].as_str()) else { continue };
        if event["kind"] != "app_restart_interruption" { continue; }
        let turns: Vec<Value> = list(&event["liveTurnsAtEnd"]).iter().filter_map(|turn| turn["turnId"].as_str()).map(|turn| {
            // The newest read of this conversation that names the turn.
            let read = events.iter().rev().filter(|e| e["kind"] == "observation_recovered" && e["threadId"] == thread)
                .find_map(|e| e["turns"].as_array()?.iter().find(|t| t["turnId"] == turn).cloned());
            let observation = observations.iter().rev().find(|o| o["threadId"] == thread);
            match (read.as_ref().and_then(|r| r["supplierStatus"].as_str()), observation.and_then(|o| o["state"].as_str())) {
                (Some("absent"), _) => json!({"turnId":turn,"reading":"not-in-history"}),
                (Some(status), _) => json!({"turnId":turn,"reading":"read","codexStatus":status}),
                // No read yet: the host is reading, waits for Codex to be ready, or has not begun.
                (None, Some("recovering" | "recovery-pending") | None) => json!({"turnId":turn,"reading":"not-read-yet"}),
                (None, Some("unavailable")) => json!({"turnId":turn,"reading":"unavailable","reason":observation.map_or(Value::Null, |o| o["unavailableReason"].clone())}),
                _ => json!({"turnId":turn,"reading":"not-established"}),
            }
        }).collect();
        if turns.is_empty() { continue; }
        conversations.push(json!({"threadId":thread,"home":event["home"],"priorSession":event["priorSession"],"priorSessionEnd":prior_end,"turns":turns}));
    }
    json!({"conversations":conversations,
        "standing":"Conversations the App's own ledger shows with a turn live when the App session before this one ended, and what Codex's history said of that turn when read back. Nothing was resumed or resent."})
}

#[cfg(test)]
mod tests {
    use super::*;
    fn restart(thread: &str, turn: &str, end: &str) -> Value {
        json!({"kind":"app_restart_interruption","threadId":thread,"home":"H-acct","priorSession":"app-session:earlier","priorSessionEnd":end,"liveTurnsAtEnd":[{"threadId":thread,"turnId":turn}]})
    }
    fn recovered(thread: &str, turn: &str, status: &str) -> Value {
        json!({"kind":"observation_recovered","threadId":thread,"turns":[{"turnId":turn,"supplierStatus":status,"appReading":"worded by the host"}]})
    }
    #[test]
    fn each_turn_reads_as_what_codex_history_said_or_as_not_known() {
        let custody = json!({
            "restartEvents":[restart("a","t1","ended-without-record"),restart("b","t2","quit-with-live-work"),restart("c","t3","system-terminated"),
                restart("d","t4","ended-without-record"),restart("e","t5","ended-without-record"),restart("f","t6","ended-without-record"),restart("g","t7","ended-without-record")],
            "live":{"events":[recovered("a","t1","interrupted"),recovered("b","other-turn","completed"),recovered("d","t4","absent"),recovered("f","t6","inProgress"),
                    {"kind":"turn_outcome","threadId":"b","turnId":"t2","outcome":"completed"}],
                "observations":[{"threadId":"b","state":"recovery-pending"},{"threadId":"c","state":"unavailable","unavailableReason":"Codex did not answer"},{"threadId":"e","state":"indexed"}]}});
        let view = read(&custody);
        let turn = |n: usize| view["conversations"][n]["turns"][0].clone();
        assert_eq!(view["conversations"][0], json!({"threadId":"a","home":"H-acct","priorSession":"app-session:earlier","priorSessionEnd":"ended-without-record","turns":[{"turnId":"t1","reading":"read","codexStatus":"interrupted"}]}));
        assert_eq!(turn(1), json!({"turnId":"t2","reading":"not-read-yet"}), "a read naming another turn, or an outcome event alone, establishes nothing for this turn");
        assert_eq!(view["conversations"][1]["priorSessionEnd"], "quit-with-live-work");
        assert_eq!(turn(2), json!({"turnId":"t3","reading":"unavailable","reason":"Codex did not answer"}));
        assert_eq!(turn(3), json!({"turnId":"t4","reading":"not-in-history"}));
        assert_eq!(turn(4), json!({"turnId":"t5","reading":"not-established"}), "a settled conversation with no read of the turn is not an outcome");
        assert_eq!(turn(5), json!({"turnId":"t6","reading":"read","codexStatus":"inProgress"}), "Codex's own word, even where it cannot be current");
        assert_eq!(turn(6), json!({"turnId":"t7","reading":"not-read-yet"}), "before the host has begun reading the conversation back");
    }
    #[test]
    fn nothing_is_reported_without_a_restart_fact_and_a_malformed_one_is_skipped() {
        assert_eq!(read(&json!({}))["conversations"], json!([]));
        assert_eq!(read(&json!({"live":{"events":[recovered("a","t1","interrupted")]}}))["conversations"], json!([]), "a recovery read alone is not a restart interruption");
        let custody = json!({"restartEvents":[{"kind":"app_restart_interruption","threadId":"a","priorSessionEnd":"ended-without-record","liveTurnsAtEnd":[]},
            {"kind":"app_restart_interruption","threadId":"b","liveTurnsAtEnd":[{"turnId":"t"}]},{"kind":"other","threadId":"c","priorSessionEnd":"x","liveTurnsAtEnd":[{"turnId":"t"}]}]});
        assert_eq!(read(&custody)["conversations"], json!([]));
    }
    #[test]
    fn the_newest_read_of_the_turn_is_the_one_reported() {
        let custody = json!({"restartEvents":[restart("a","t1","ended-without-record")],"live":{"events":[recovered("a","t1","inProgress"),recovered("a","t1","interrupted")]}});
        assert_eq!(read(&custody)["conversations"][0]["turns"][0]["codexStatus"], "interrupted");
    }
}
