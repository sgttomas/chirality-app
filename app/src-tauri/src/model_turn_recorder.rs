//! RS R5 `model_turn` entries for an App run (DEL-04-03 RS R5, §11 "Each
//! turn's model | `model_turn` | DEL-01-01 (App)"; DEL-01-01 HOSTING §8.3).
//!
//! What it records, in the run's own RS log through the App writer:
//! - for the thread-level destination reports of the run's conversation (the
//!   thread start, resume or fork response, HOSTING §8.3), one entry each with
//!   `scope` *thread* and no turn, written beside the turns and never copied
//!   into any of them (U-27);
//! - for each turn of the run (the conversation's turns from the run's start
//!   turn on, observed live while the run is open; the checkpoint recorder's
//!   attribution), one entry with `scope` *turn* and the turn's ordinal in the
//!   run, written when the turn is observed to end, or at the run's end for a
//!   turn still in progress, before `run_ended`. Its `effective` value comes
//!   only from a `model/rerouted` report naming that turn; otherwise it is
//!   *unknown*, even when the thread or an earlier turn has a value. Each
//!   re-route is recorded with its turn: a turn with several gets one entry
//!   per re-route (`reroute` true); `reroute` is omitted when none was
//!   observed, which is not evidence that none happened (HOSTING U-19);
//! - a `model/rerouted` report received after its turn's entry was written is
//!   recorded as a further entry for that turn; the earlier one is not rewritten.
//!
//! A turn's `requested` comes from the App's own `turn/start` for it, as the
//! host correlated it: a `collaborationMode` turn asked for that mode's model;
//! a plain turn carries no model and runs under the latest mode the App sent
//! the conversation in the same Codex process, or else under the provider and
//! model the App requested at thread start. A turn the App did not start, one
//! after a mode sent in an earlier process, and a conversation the App did not
//! start in this session have *unknown*. The destination class
//! is DEL-01-05's mapping of the conversation's access entry (ACCESS-v0.2 §2),
//! known only for the conversation the home last started; otherwise *unknown*.
//!
//! Recording is not a reaction: nothing here sends, asks or changes anything,
//! and nothing is observed after the run's end.
use serde_json::{json, Value};
use std::collections::BTreeSet;

/// Where the run is, as this recorder needs it.
pub(crate) struct RunScope<'a> {
    pub home: &'a str,
    pub conversation: &'a str,
    pub start: crate::run_offers::RunStart,
    /// The spawn counter of the Codex generation the run opened in.
    pub start_spawn: u64,
}

#[derive(Debug)]
struct Turn {
    id: String,
    ordinal: u64,
    written: bool,
    /// The `toModel` of each re-route naming this turn observed before its
    /// entry, in receipt order; each is recorded with its turn.
    rerouted_to: Vec<String>,
    /// What the App's own `turn/start` asked for (see [`ModelTurnRecorder::turn_requested`]).
    requested: String,
}

#[derive(Debug, Default)]
pub(crate) struct ModelTurnRecorder {
    turns: Vec<Turn>,
    thread_reports: BTreeSet<String>,
    reroutes_seen: BTreeSet<String>,
    requested: Option<String>,
    class: Option<String>,
}

/// "‹provider›/‹model›", "‹model›" when no provider is reported, or *unknown*.
fn destination(provider: &Value, model: &Value) -> String {
    match (provider.as_str().filter(|p| !p.is_empty()), model.as_str().filter(|m| !m.is_empty())) {
        (Some(p), Some(m)) => format!("{p}/{m}"),
        (None, Some(m)) => m.to_owned(),
        _ => "unknown".to_owned(),
    }
}

/// DEL-01-05's access-entry mapping (ACCESS-v0.2 §2; HOSTING §8.3).
fn class_of(entry: &Value) -> &'static str {
    match entry.as_str() {
        Some("chatgpt-account" | "api-key") => "user-chosen cloud",
        Some("local-provider") => "local model server",
        _ => "unknown",
    }
}

impl ModelTurnRecorder {
    /// `reroute` is written only when a re-route was observed: none observed
    /// is not evidence that none happened (HOSTING U-19).
    fn turn_body(&self, ordinal: u64, requested: &str, rerouted_to: Option<&str>) -> Value {
        let mut body = json!({"turn":ordinal,"scope":"turn","requested":requested,
            "effective":rerouted_to.unwrap_or("unknown"),"destinationClass":self.class.as_deref().unwrap_or("unknown")});
        if rerouted_to.is_some() {
            body["reroute"] = json!(true);
        }
        body
    }
    /// The turn's entries: one per re-route observed for it, or one *unknown*.
    fn turn_bodies(&self, turn: &Turn) -> Vec<Value> {
        if turn.rerouted_to.is_empty() {
            return vec![self.turn_body(turn.ordinal, &turn.requested, None)];
        }
        turn.rerouted_to.iter().map(|to| self.turn_body(turn.ordinal, &turn.requested, Some(to))).collect()
    }
    /// RS R5 *requested* for one turn, from the App's own `turn/start` as the
    /// host correlated it: a `collaborationMode` turn asked for that mode's
    /// model; a plain turn carries no model, so it runs under the latest mode
    /// the App sent this conversation in the same Codex process (Codex keeps
    /// it), or else the conversation's thread-start request. A turn the App did
    /// not start, or one after a mode sent in an earlier process, is *unknown*.
    fn turn_requested(&self, view: &Value, scope: &RunScope, turn: &str) -> String {
        let session = &view["generation"]["appSession"];
        let rows: Vec<&Value> = view["hostTurns"].as_array().into_iter().flatten()
            .filter(|t| t["threadId"] == scope.conversation && t["generation"]["appSession"] == *session && t["generation"]["home"] == scope.home && t["appTurnStart"].is_object())
            .collect();
        let Some(this) = rows.iter().find(|t| t["turnId"] == turn) else { return "unknown".into() };
        if this["appTurnStart"]["collaborationMode"] == true {
            return destination(&Value::Null, &this["appTurnStart"]["model"]);
        }
        let spawn = |t: &Value| t["generation"]["spawnCounter"].as_u64().unwrap_or(0);
        let order = |t: &Value| t["turnId"].as_str().and_then(|id| crate::run_offers::turn_order(view, scope.conversation, id));
        let mut earlier_mode = false;
        let mut latest: Option<(u64, String)> = None;
        for mode in rows.iter().filter(|t| t["appTurnStart"]["collaborationMode"] == true && t["turnId"] != turn) {
            if spawn(mode) < spawn(this) {
                earlier_mode = true;
                continue;
            }
            match (order(mode), order(this)) {
                (Some(m), Some(t)) if spawn(mode) == spawn(this) && m < t => {
                    if latest.as_ref().is_none_or(|(o, _)| m > *o) {
                        latest = Some((m, destination(&Value::Null, &mode["appTurnStart"]["model"])));
                    }
                }
                (None, _) | (_, None) if spawn(mode) == spawn(this) => earlier_mode = true,
                _ => {}
            }
        }
        match latest {
            Some((_, model)) => model,
            None if earlier_mode => "unknown".into(),
            None => self.requested.clone().unwrap_or_else(|| "unknown".into()),
        }
    }

    /// Reads the run's conversation in `view` and returns the `model_turn`
    /// bodies to write, in order. Each report and turn is written once.
    pub(crate) fn observe(&mut self, view: &Value, scope: &RunScope) -> Vec<Value> {
        if view["home"] != scope.home {
            return vec![];
        }
        let session = view["generation"]["appSession"].clone();
        let mine = |generation: &Value| generation["appSession"] == session && generation["home"] == scope.home;
        let mut written = Vec::new();
        if let Some(access) = view["conversationAccess"].as_array().into_iter().flatten().find(|a| a["threadId"] == scope.conversation) {
            self.class = Some(class_of(&access["entryId"]).to_owned());
        }
        // Thread-level reports: requested at the App's start; reported by start, resume or fork.
        let mut occurrence = std::collections::BTreeMap::<String, u64>::new();
        for row in view["hostThreads"].as_array().into_iter().flatten() {
            if row["threadId"] != scope.conversation || !mine(&row["generation"]) {
                continue;
            }
            let generation = serde_json::to_string(&row["generation"]).unwrap_or_default();
            let nth = occurrence.entry(generation.clone()).or_insert(0);
            *nth += 1;
            if row["requestedDestination"]["source"] == "person-selected" {
                self.requested = Some(destination(&row["requestedDestination"]["modelProvider"], &row["requestedDestination"]["model"]));
            }
            if row["generation"]["spawnCounter"].as_u64().unwrap_or(0) < scope.start_spawn {
                continue;
            }
            let key = format!("{generation}\u{0}{nth}");
            if self.thread_reports.insert(key) {
                let reported = if row["reportedDestination"].is_object() { &row["reportedDestination"] } else { row };
                written.push(json!({"scope":"thread","requested":self.requested.as_deref().unwrap_or("unknown"),
                    "effective":destination(&reported["modelProvider"], &reported["model"]),
                    "destinationClass":self.class.as_deref().unwrap_or("unknown")}));
            }
        }
        // The run's turns, in the order this App first received them.
        let in_run = |turn: &str| crate::run_offers::turn_order(view, scope.conversation, turn).is_some_and(|order| scope.start.includes(order));
        let mut found: Vec<(u64, String)> = Vec::new();
        for row in view["items"].as_array().into_iter().flatten() {
            if row["threadId"] != scope.conversation || row["standing"] != "live-observed" || row["receipt"]["generation"]["appSession"] != session {
                continue;
            }
            let Some(turn) = row["turnId"].as_str() else { continue };
            if !in_run(turn) || self.turns.iter().any(|t| t.id == turn) || found.iter().any(|(_, t)| t == turn) {
                continue;
            }
            if let Some(order) = crate::run_offers::turn_order(view, scope.conversation, turn) {
                found.push((order, turn.to_owned()));
            }
        }
        found.sort();
        for (_, id) in found {
            let ordinal = self.turns.len() as u64 + 1;
            self.turns.push(Turn { id, ordinal, written: false, rerouted_to: vec![], requested: "unknown".into() });
        }
        // Requested as the host correlated each unwritten turn's start (read again until written).
        for index in 0..self.turns.len() {
            if !self.turns[index].written {
                self.turns[index].requested = self.turn_requested(view, scope, &self.turns[index].id);
            }
        }
        // Re-routes naming a turn of the run.
        for reroute in view["modelReroutes"].as_array().into_iter().flatten() {
            if reroute["threadId"] != scope.conversation || !mine(&reroute["generation"]) {
                continue;
            }
            let key = format!("{}\u{0}{}", serde_json::to_string(&reroute["generation"]).unwrap_or_default(), reroute["receiptPosition"]);
            if self.reroutes_seen.contains(&key) {
                continue;
            }
            let (Some(turn), Some(to)) = (reroute["turnId"].as_str(), reroute["toModel"].as_str()) else { continue };
            match self.turns.iter().position(|t| t.id == turn) {
                Some(index) => {
                    self.reroutes_seen.insert(key);
                    if self.turns[index].written {
                        written.push(self.turn_body(self.turns[index].ordinal, &self.turns[index].requested, Some(to)));
                    } else {
                        self.turns[index].rerouted_to.push(to.to_owned());
                    }
                }
                // A turn with no row yet is read again later; one outside the run is not this run's.
                None if crate::run_offers::turn_order(view, scope.conversation, turn).is_some() => {
                    self.reroutes_seen.insert(key);
                }
                None => {}
            }
        }
        // Turns observed to end.
        let records = view["turnRecords"].as_array().cloned().unwrap_or_default();
        let natives = view["turns"].as_array().cloned().unwrap_or_default();
        let ended = |id: &str| records.iter().zip(natives.iter()).any(|(r, n)| r["threadId"] == scope.conversation && r["turnId"] == id && n["status"].is_string() && n["status"] != "inProgress");
        for index in 0..self.turns.len() {
            if !self.turns[index].written && ended(&self.turns[index].id) {
                self.turns[index].written = true;
                written.extend(self.turn_bodies(&self.turns[index]));
            }
        }
        written
    }

    /// At the run's end, before `run_ended`: an entry for each turn of the run
    /// not yet written (a turn still in progress), with what was observed.
    pub(crate) fn end(&mut self) -> Vec<Value> {
        let mut written = Vec::new();
        for index in 0..self.turns.len() {
            if !self.turns[index].written {
                self.turns[index].written = true;
                written.extend(self.turn_bodies(&self.turns[index]));
            }
        }
        written
    }

    pub(crate) fn view(&self) -> Value {
        json!({"turns":self.turns.len(),"written":self.turns.iter().filter(|t|t.written).count(),"threadReports":self.thread_reports.len(),
            "standing":"RS R5 per turn: requested and effective kept separate; effective only from a re-route naming the turn, otherwise unknown (HOSTING §8.3)"})
    }
}

#[cfg(test)]
#[path = "model_turn_recorder_tests.rs"]
mod tests;
