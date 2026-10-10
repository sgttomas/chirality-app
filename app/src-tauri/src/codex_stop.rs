//! Stop Codex and Restart Codex (DEL-01-02 §4.1 "assess live work" and "stop
//! Codex / restart Codex", C-12, DEF-5a; DEL-01-04 §5.2).
//!
//! The person is asked first, with no timeout, and shown the live work in
//! force: live turns, outstanding requests, delegated agents and workflow runs.
//! Cancel changes nothing. On confirm each observed live turn is interrupted
//! (SR-01, cause *codex-stop*), the App waits for Codex to report those turns
//! ended, and then stops the Codex process (HOSTING §4.5), all within the stop
//! wait limit. Restart then starts Codex again the way Start Codex does; no
//! conversation is continued until the person chooses Continue (R-6).
//!
//! A stop is the person's operational choice, not a recorded act. Neither
//! stop ends a workflow run or answers a request (DEF-5).
//!
//! Limit: the App writes no REC stop-request (SR) record and no ledger
//! `codex_stop` record; no writer for them exists yet. The outcome below is
//! kept in this App process's memory only, so after a relaunch the App cannot
//! say that a turn was interrupted by Stop Codex.

use crate::runtime_session::{HomeSession, WorkflowRootSession};
use serde_json::{json, Value};
use std::sync::Mutex;
use std::time::{Duration, Instant};

/// U-R4 stop wait limit, a TEST VALUE owned by the App implementation owner.
/// It bounds the interrupt requests and the wait for their turns to end; the
/// HOSTING grace period (3 s) for the process tree follows it. At 0.158.0 an
/// interrupt's acknowledgment came 21 ms after the request and the turn ended
/// within a millisecond of it (RECOVERY §3.4, OBS-2 §4); 10 s leaves room for
/// a running tool command to wind down while keeping the person's wait short.
pub const STOP_WAIT_LIMIT: Duration = Duration::from_secs(10);
/// Kept in memory for display; older outcomes are dropped first.
pub const OUTCOMES_KEPT: usize = 20;

pub(crate) const RECORDS_LIMIT: &str = "Kept in this App process only. The App writes no recovery stop record (REC SR) and no ledger codex_stop record, so after the App is relaunched it cannot say that a turn was interrupted by Stop Codex.";

fn action(restart: bool) -> &'static str {
    if restart {
        "Restart Codex"
    } else {
        "Stop Codex"
    }
}

/// The live-work assessment shown in the question. `material` is what must
/// stay unchanged between the question and the stop; it excludes the clock.
pub struct Assessment {
    material: Value,
    view: Value,
}
impl Assessment {
    pub fn view(&self) -> &Value {
        &self.view
    }
    fn new(material: Value, restart: bool) -> Self {
        let mut view = material.clone();
        view["restart"] = json!(restart);
        view["observedAt"] = json!(crate::util::now_rfc3339());
        view["stopWaitLimitSeconds"] = json!(STOP_WAIT_LIMIT.as_secs());
        view["limit"] = json!("None observed is not none: coverage of turns, requests and delegated agents is not complete. Workflow runs listed are those this App process holds.");
        Self { material, view }
    }
}

/// DEL-01-02 §4.1 "assess live work" for one home's current Codex process,
/// with the workflow runs in force in that home. Nothing is sent or changed.
pub(crate) fn assess(
    home: &HomeSession,
    workflows: &Mutex<WorkflowRootSession>,
    generation: &Value,
    restart: bool,
) -> Result<Assessment, String> {
    crate::recovery::generation_ref(generation)?;
    let snapshot = home.host.snapshot();
    if snapshot["generation"] != *generation {
        return Err("Codex changed since this view (another Codex process); refresh and choose again. Nothing stopped".into());
    }
    let state = snapshot["state"].as_str().unwrap_or("not reported").to_owned();
    if matches!(state.as_str(), "absent" | "stopped" | "refused" | "stopping") {
        let hint = if restart { "; use Start Codex" } else { "" };
        return Err(format!("Codex is not running here (state {state}); nothing to stop{hint}"));
    }
    let (work, not_ready) = if state == "ready" {
        (crate::runtime_session::assess_native_home_work(home, generation)?.snapshot(), Value::Null)
    } else {
        (json!({}), json!(format!("Codex is {state}, not ready: live work cannot be observed and no interrupt can be sent")))
    };
    let list = |key: &str| work.get(key).cloned().unwrap_or_else(|| json!([]));
    let runs = generation["home"]
        .as_str()
        .map(|id| workflows.lock().unwrap().runs_in_force_in_home(id))
        .unwrap_or_default();
    let material = json!({
        "modeHomeClass": home.class().as_str(),
        "generation": generation,
        "state": state,
        "notReady": not_ready,
        "observedLiveTurns": list("observedLiveTurns"),
        "observedOutstandingRequests": list("observedOutstandingRequests"),
        "observedActiveChildren": list("observedActiveChildren"),
        "knownChildActivityUnknown": list("knownChildActivityUnknown"),
        "coverage": {"turns": {"unresolved": work["coverage"]["turns"]["unresolved"].as_array().cloned().unwrap_or_default()}},
        "runsInForce": runs,
    });
    Ok(Assessment::new(material, restart))
}

/// TO-4 / RECOVERY §3.4 labels for cause *codex-stop* (Stop and Restart alike).
/// `status` is the turn's status from an observed `turn/completed`, never from
/// an interrupt acknowledgment.
pub(crate) fn outcome_label(status: Option<&str>, stopped: bool) -> &'static str {
    match status {
        Some("interrupted") => "interrupted by Stop Codex",
        Some("completed") => "completed (Stop Codex requested)",
        Some("failed") => "failed (Stop Codex requested)",
        Some(_) => "outcome unknown (Stop Codex requested)",
        None if stopped => "interrupted by Stop Codex (final status not observed)",
        None => "outcome unknown (Stop Codex requested)",
    }
}

/// The turn's terminal status as this App observed it (`turn/completed`).
fn observed_end(turn: Option<Value>) -> Option<String> {
    let turn = turn?;
    (turn["terminalEventObserved"] == true)
        .then(|| turn["nativeTurn"]["status"].as_str().unwrap_or("not reported").to_owned())
}

/// The ask, interrupt, wait, stop and (for Restart) start sequence, apart from
/// Tauri and the Host so that tests reach it. `Ok` carries the outcome, also
/// for a cancel; `Err` means nothing was interrupted or stopped.
#[allow(clippy::too_many_arguments)]
pub(crate) fn stop_or_restart(
    restart: bool,
    wait_limit: Duration,
    mut assess: impl FnMut() -> Result<Assessment, String>,
    mut confirm: impl FnMut(&Value) -> bool,
    mut interrupt: impl FnMut(&Value, Duration) -> Result<Value, String>,
    mut turn_reading: impl FnMut(&Value) -> Option<Value>,
    stop: impl FnOnce() -> Result<Value, String>,
    start: impl FnOnce() -> Result<Value, String>,
) -> Result<Value, String> {
    let action = action(restart);
    // AS-04/AS-07: the question stays open with no timeout; when live work
    // changes while it is open, it is asked again with the current list.
    let mut asked = assess()?;
    let mut changed = false;
    let confirmed = loop {
        let mut view = asked.view.clone();
        if changed {
            view["changedWhileAsking"] = json!(true);
        }
        if !confirm(&view) {
            return Ok(json!({"action":action,"state":"cancelled","reading":"You kept Codex running. Nothing was interrupted, stopped or sent.","assessment":view}));
        }
        let current = assess().map_err(|e| format!("{e}. Nothing was interrupted or stopped"))?;
        if current.material == asked.material {
            break current;
        }
        asked = current;
        changed = true;
    };
    let confirmed_at = crate::util::now_rfc3339();
    let deadline = Instant::now() + wait_limit;
    // SR-01: interrupts are requested before the stop.
    let mut turns = Vec::new();
    for turn in confirmed.material["observedLiveTurns"].as_array().into_iter().flatten() {
        let remaining = deadline.saturating_duration_since(Instant::now());
        let request = if remaining.is_zero() {
            json!({"state":"not sent","reading":"the stop wait limit passed before this interrupt could be sent"})
        } else {
            match interrupt(turn, remaining) {
                Ok(ack) => json!({"state":"acknowledged","reading":"Codex acknowledged the interrupt request. An acknowledgment is not the turn's end.","acknowledgment":ack.get("result").cloned().unwrap_or(Value::Null)}),
                Err(error) => json!({"state":"not acknowledged","reading":error}),
            }
        };
        turns.push(json!({"generation":turn["generation"],"threadId":turn["threadId"],"turnId":turn["turnId"],"interruptRequest":request}));
    }
    // Q-5: wait until each turn is observed ended or the stop wait limit passes.
    let mut ends: Vec<Option<String>> = turns.iter().map(|t| observed_end(turn_reading(t))).collect();
    while ends.iter().any(Option::is_none) && Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(25));
        ends = turns.iter().map(|t| observed_end(turn_reading(t))).collect();
    }
    let stop = stop();
    let stopped = stop.is_ok();
    let mut live_at_stop = false;
    for (turn, end) in turns.iter_mut().zip(&ends) {
        live_at_stop |= end.is_none();
        turn["codexReported"] = json!(end);
        turn["label"] = json!(outcome_label(end.as_deref(), stopped));
    }
    let start = match (restart, &stop) {
        (true, Ok(_)) => Some(match start() {
            Ok(started) => json!({"state":"started","codex":started}),
            Err(error) => json!({"state":"not started","reading":error}),
        }),
        (true, Err(_)) => Some(json!({"state":"not started","reading":"Codex was not stopped, so it was not started again"})),
        _ => None,
    };
    let requests = confirmed.material["observedOutstandingRequests"].as_array().map_or(0, Vec::len);
    Ok(json!({
        "action": action,
        "state": if stopped { "stopped" } else { "stop refused" },
        "actor": "the person",
        "standing": "your operational choice; not a recorded act",
        "confirmedAt": confirmed_at,
        "modeHomeClass": confirmed.material["modeHomeClass"],
        "generation": confirmed.material["generation"],
        "stopWaitLimitSeconds": wait_limit.as_secs(),
        "assessment": confirmed.view,
        "turns": turns,
        "outstandingRequests": {"count": requests, "reading": "Not answered by the App; they end unanswered with the Codex process."},
        "runsInForce": {"rows": confirmed.material["runsInForce"], "reading": "Stopping Codex ends no workflow run."},
        "stop": match &stop { Ok(result) => json!({"state":"stopped","result":result}), Err(error) => json!({"state":"refused","reading":error}) },
        "start": start,
        "conversations": if restart { json!("No conversation was continued automatically. To continue one, read stored conversations, select it and choose Continue selected conversation.") } else { Value::Null },
        "historyNote": if live_at_stop && stopped { json!("A turn still live at the stop: Codex may write into its history that the user interrupted the turn on purpose. That note comes from this stop.") } else { Value::Null },
        "records": RECORDS_LIMIT,
    }))
}

/// The real binding: this home's Host, its observed turns and the App's
/// workflow runs. `confirm` shows the native question; `start` starts Codex
/// the way Start Codex does (Restart only).
pub(crate) fn stop_native_home(
    home: &HomeSession,
    workflows: &Mutex<WorkflowRootSession>,
    generation: &Value,
    restart: bool,
    confirm: impl FnMut(&Value) -> bool,
    start: impl FnOnce() -> Result<Value, String>,
) -> Result<Value, String> {
    stop_native_home_within(home, workflows, generation, restart, STOP_WAIT_LIMIT, confirm, start)
}

pub(crate) fn stop_native_home_within(
    home: &HomeSession,
    workflows: &Mutex<WorkflowRootSession>,
    generation: &Value,
    restart: bool,
    wait_limit: Duration,
    confirm: impl FnMut(&Value) -> bool,
    start: impl FnOnce() -> Result<Value, String>,
) -> Result<Value, String> {
    stop_or_restart(
        restart,
        wait_limit,
        || assess(home, workflows, generation, restart),
        confirm,
        |turn, wait| {
            let thread = turn["threadId"].as_str().ok_or("live turn without a conversation")?;
            let id = turn["turnId"].as_str().ok_or("live turn without an identity")?;
            crate::runtime_session::interrupt_conversation_turn(&home.host.snapshot(), generation, thread, id, |g, t, u| {
                home.host.turn_interrupt_within(g, t, u, wait)
            })
        },
        |turn| home.host.conversation_turn(&turn["generation"], turn["threadId"].as_str().unwrap_or_default(), turn["turnId"].as_str().unwrap_or_default()),
        || home.host.stop_scoped(generation, "the person", action(restart)),
        || {
            start()?;
            let now = home.host.snapshot();
            Ok(json!({"state":now["state"],"generation":now["generation"]}))
        },
    )
}

#[cfg(test)]
#[path = "codex_stop_tests.rs"]
mod tests;
