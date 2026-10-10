//! Stop Codex and Restart Codex (DEL-01-02 §4.1 "assess live work" and "stop
//! Codex / restart Codex", C-12, DEF-5a; DEL-01-04 §5.2).
//!
//! The person is asked first, with no timeout, and shown the live work in
//! force: live turns, outstanding requests, delegated agents and workflow runs.
//! Cancel changes nothing. On confirm the Host is closed to new turns for that
//! Codex process, the live work is assessed again (a changed list is asked
//! again), every observed live turn is sent an interrupt (SR-01, cause
//! *codex-stop*), the App waits for the acknowledgments and for Codex to report
//! those turns ended on one shared deadline, and then stops the Codex process
//! (HOSTING §4.5), all within the stop wait limit. Restart then starts Codex
//! again the way Start Codex does; no conversation is continued until the
//! person chooses Continue (R-6).
//!
//! Process state: interrupts are sent only to a `ready` process (DEL-01-02
//! §4.1: "a process not ready is reported, nothing is sent"). The process
//! itself may be stopped in any state except `absent`, `stopped` and `refused`,
//! as HOSTING §4.6's stop operation gives for the person's "Stop Codex" /
//! "Restart Codex" (LT-17…LT-22), so a stuck handshake can still be ended.
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
use std::sync::{Mutex, MutexGuard, TryLockError};
use std::time::{Duration, Instant};

/// U-R4 stop wait limit, a TEST VALUE owned by the App implementation owner.
/// It bounds the interrupt acknowledgments and the wait for their turns to
/// end; the HOSTING grace period (3 s) for the process tree follows it. At
/// 0.158.0 an interrupt's acknowledgment came 21 ms after the request and the
/// turn ended within a millisecond of it (RECOVERY §3.4, OBS-2 §4); 10 s leaves
/// room for a running tool command to wind down while keeping the wait short.
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
    // HOSTING §4.6 stop: every state except absent, stopped and refused
    // (`stopping` already has its stop under way).
    if matches!(state.as_str(), "absent" | "stopped" | "refused" | "stopping") {
        let hint = if restart { "; use Start Codex" } else { "" };
        return Err(format!("Codex is not running here (state {state}); nothing to stop{hint}"));
    }
    let (work, not_ready) = if state == "ready" {
        (crate::runtime_session::assess_native_home_work(home, generation)?.snapshot(), Value::Null)
    } else {
        // DEL-01-02 §4.1: a process not ready is reported; nothing is sent to it.
        (json!({}), json!(format!("Codex is {state}, not ready: live work cannot be observed and nothing is sent to it; only the process is stopped")))
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

/// RECOVERY §3.4 `outcomeLabel` values for cause *codex-stop* ("the same
/// four"; Stop and Restart alike), given only after Codex was stopped.
/// `status` is the turn's status from an observed `turn/completed`, never from
/// an interrupt acknowledgment. A status outside the three final ones is not a
/// final status observed.
pub(crate) fn outcome_label(status: Option<&str>) -> &'static str {
    match status {
        Some("interrupted") => "interrupted by Stop Codex",
        Some("completed") => "completed (Stop Codex requested)",
        Some("failed") => "failed (Stop Codex requested)",
        _ => "interrupted by Stop Codex (final status not observed)",
    }
}

/// The turn's terminal status as this App observed it (`turn/completed`).
fn observed_end(turn: Option<Value>) -> Option<String> {
    let turn = turn?;
    (turn["terminalEventObserved"] == true)
        .then(|| turn["nativeTurn"]["status"].as_str().unwrap_or("not reported").to_owned())
}

/// What the sequence needs from the world; the real Host binding is
/// `HostStop`, tests use doubles.
pub(crate) trait StopOps {
    /// A written interrupt request whose acknowledgment may still come.
    type Pending;
    fn assess(&mut self) -> Result<Assessment, String>;
    /// The native question; true only for the explicit Stop/Restart button.
    fn confirm(&mut self, view: &Value) -> bool;
    /// From now on no new turn or steer is sent to this Codex process.
    fn close_to_new_turns(&mut self) -> Result<(), String>;
    fn reopen_to_new_turns(&mut self);
    /// Writes one interrupt request; does not wait for its acknowledgment.
    fn interrupt(&mut self, turn: &Value) -> Result<Self::Pending, String>;
    fn acknowledgment(&mut self, pending: &Self::Pending, wait: Duration) -> Result<Value, String>;
    fn turn_reading(&mut self, turn: &Value) -> Option<Value>;
    fn stop(&mut self) -> Result<Value, String>;
    fn start(&mut self) -> Result<Value, String>;
}

/// The ask, close, interrupt, wait, stop and (for Restart) start sequence.
/// `Ok` carries the outcome, also for a cancel; `Err` means nothing was
/// interrupted or stopped.
pub(crate) fn stop_or_restart<O: StopOps>(ops: &mut O, restart: bool, wait_limit: Duration) -> Result<Value, String> {
    let action = action(restart);
    // AS-04/AS-07: no timeout. The Host is closed to new turns before the
    // final reassessment, so no work starts between it and the interrupts; a
    // list that changed while the question was open is asked again.
    let mut asked = ops.assess()?;
    let mut changed = false;
    let confirmed = loop {
        let mut view = asked.view.clone();
        if changed {
            view["changedWhileAsking"] = json!(true);
        }
        if !ops.confirm(&view) {
            return Ok(json!({"action":action,"state":"cancelled","reading":"You kept Codex running. Nothing was interrupted, stopped or sent.","assessment":view}));
        }
        ops.close_to_new_turns().map_err(|e| format!("{e}. Nothing was interrupted or stopped"))?;
        let current = match ops.assess() {
            Ok(current) => current,
            Err(e) => {
                ops.reopen_to_new_turns();
                return Err(format!("{e}. Nothing was interrupted or stopped"));
            }
        };
        if current.material == asked.material {
            break current;
        }
        ops.reopen_to_new_turns();
        asked = current;
        changed = true;
    };
    let confirmed_at = crate::util::now_rfc3339();
    let deadline = Instant::now() + wait_limit;
    // SR-01: every interrupt is written before any wait and before the stop.
    let live: Vec<Value> = confirmed.material["observedLiveTurns"].as_array().cloned().unwrap_or_default();
    let pending: Vec<Result<O::Pending, String>> = live.iter().map(|turn| ops.interrupt(turn)).collect();
    // One shared deadline: an unanswered interrupt cannot starve the others.
    let mut turns = Vec::new();
    for (turn, written) in live.iter().zip(&pending) {
        let request = match written {
            Err(error) => json!({"state":"not sent","reading":error}),
            Ok(written) => match ops.acknowledgment(written, deadline.saturating_duration_since(Instant::now())) {
                Ok(ack) => json!({"state":"acknowledged","reading":"Codex acknowledged the interrupt request. An acknowledgment is not the turn's end.","acknowledgment":ack.get("result").cloned().unwrap_or(Value::Null)}),
                Err(error) => json!({"state":"sent; not acknowledged","reading":error}),
            },
        };
        turns.push(json!({"generation":turn["generation"],"threadId":turn["threadId"],"turnId":turn["turnId"],"interruptRequest":request}));
    }
    // Q-5: wait until each turn is observed ended or the stop wait limit passes.
    let mut ends: Vec<Option<String>> = turns.iter().map(|t| observed_end(ops.turn_reading(t))).collect();
    while ends.iter().any(Option::is_none) && Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(25));
        ends = turns.iter().map(|t| observed_end(ops.turn_reading(t))).collect();
    }
    let stop = ops.stop();
    let stopped = stop.is_ok();
    if !stopped {
        ops.reopen_to_new_turns();
    }
    let mut live_at_stop = false;
    for (turn, end) in turns.iter_mut().zip(&ends) {
        live_at_stop |= end.is_none();
        turn["codexReported"] = json!(end);
        // A refused stop is reported as a refusal; no turn gets a Stop label.
        turn["label"] = if stopped { json!(outcome_label(end.as_deref())) } else { Value::Null };
    }
    let start = match (restart, stopped) {
        (true, true) => Some(match ops.start() {
            Ok(started) => json!({"state":"started","codex":started}),
            Err(error) => json!({"state":"not started","reading":error}),
        }),
        (true, false) => Some(json!({"state":"not started","reading":"Codex was not stopped, so it was not started again"})),
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
        "outstandingRequests": {"count": requests, "reading": if stopped { "Not answered by the App; they end unanswered with the Codex process." } else { "Not answered by the App; Codex was not stopped, so they stay as observed." }},
        "runsInForce": {"rows": confirmed.material["runsInForce"], "reading": "Stopping Codex ends no workflow run."},
        "stop": match &stop { Ok(result) => json!({"state":"stopped","result":result}), Err(error) => json!({"state":"refused","reading":error}) },
        "start": start,
        "conversations": if restart && stopped { json!("No conversation was continued automatically. To continue one, read stored conversations, select it and choose Continue selected conversation.") } else { Value::Null },
        "historyNote": if live_at_stop && stopped { json!("A turn still live at the stop: Codex may write into its history that the user interrupted the turn on purpose. That note comes from this stop.") } else { Value::Null },
        "records": RECORDS_LIMIT,
    }))
}

/// The real binding: this home's Host, its observed turns and the App's
/// workflow runs. `confirm` shows the native question; `start` starts Codex
/// the way Start Codex does (Restart only).
pub(crate) struct HostStop<'a, C, S> {
    pub(crate) home: &'a HomeSession,
    pub(crate) workflows: &'a Mutex<WorkflowRootSession>,
    pub(crate) generation: &'a Value,
    pub(crate) restart: bool,
    pub(crate) confirm: C,
    pub(crate) start: Option<S>,
}
impl<C: FnMut(&Value) -> bool, S: FnOnce() -> Result<Value, String>> StopOps for HostStop<'_, C, S> {
    type Pending = crate::hosting::SourceRequest;
    fn assess(&mut self) -> Result<Assessment, String> {
        assess(self.home, self.workflows, self.generation, self.restart)
    }
    fn confirm(&mut self, view: &Value) -> bool {
        (self.confirm)(view)
    }
    fn close_to_new_turns(&mut self) -> Result<(), String> {
        self.home.host.close_to_new_turns(self.generation)
    }
    fn reopen_to_new_turns(&mut self) {
        self.home.host.reopen_to_new_turns(self.generation)
    }
    fn interrupt(&mut self, turn: &Value) -> Result<Self::Pending, String> {
        let thread = turn["threadId"].as_str().ok_or("live turn without a conversation")?;
        let id = turn["turnId"].as_str().ok_or("live turn without an identity")?;
        let host = &self.home.host;
        let mut written = None;
        // The same guard as the person's Interrupt control (live turn, no
        // interrupt already requested); the request is written, not awaited.
        crate::runtime_session::interrupt_conversation_turn(&host.snapshot(), self.generation, thread, id, |g, t, u| {
            written = Some(host.turn_interrupt_begin(g, t, u)?);
            Ok(Value::Null)
        })?;
        written.ok_or_else(|| "interrupt request not written".to_owned())
    }
    fn acknowledgment(&mut self, pending: &Self::Pending, wait: Duration) -> Result<Value, String> {
        self.home.host.turn_interrupt_acknowledgment(pending, wait)
    }
    fn turn_reading(&mut self, turn: &Value) -> Option<Value> {
        self.home.host.conversation_turn(&turn["generation"], turn["threadId"].as_str().unwrap_or_default(), turn["turnId"].as_str().unwrap_or_default())
    }
    fn stop(&mut self) -> Result<Value, String> {
        self.home.host.stop_scoped(self.generation, "the person", action(self.restart))
    }
    fn start(&mut self) -> Result<Value, String> {
        (self.start.take().ok_or("Codex start already attempted")?)()?;
        let now = self.home.host.snapshot();
        Ok(json!({"state":now["state"],"generation":now["generation"]}))
    }
}

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
    let mut ops = HostStop { home, workflows, generation, restart, confirm, start: Some(start) };
    stop_or_restart(&mut ops, restart, wait_limit)
}

// ---- Command glue (lib.rs `codex_stop`), here so tests reach it without Tauri.

/// One Stop/Restart question at a time. A gate poisoned by an earlier panic
/// guards no data, so it is recovered rather than reported as busy forever.
pub(crate) fn question_gate(gate: &Mutex<()>) -> Result<MutexGuard<'_, ()>, String> {
    match gate.try_lock() {
        Ok(guard) => Ok(guard),
        Err(TryLockError::Poisoned(poisoned)) => Ok(poisoned.into_inner()),
        Err(TryLockError::WouldBlock) => Err("A Stop or Restart Codex question is already open; nothing else asked".into()),
    }
}

/// Restart must be able to start Codex again; otherwise nothing is stopped
/// and nothing is asked.
pub(crate) fn restart_precheck(config: Result<(), String>, source: impl FnOnce() -> Result<(), String>) -> Result<(), String> {
    config.and_then(|()| source()).map_err(|e| format!("Restart Codex cannot start Codex again here ({e}); nothing stopped"))
}

/// Maps the sequence's result to the command's: a presentation refusal is a
/// refusal (never the person's cancel), a cancel is returned unkept, a
/// confirmed outcome is kept (bounded), and a refused stop is an error.
pub(crate) fn finish(kept: &Mutex<Vec<Value>>, title: &str, refused: Option<String>, result: Result<Value, String>) -> Result<Value, String> {
    let outcome = crate::act_control::native_statement::refusal_or(refused, result)?;
    if outcome["state"] == "cancelled" {
        return Ok(outcome);
    }
    {
        let mut kept = kept.lock().unwrap_or_else(|e| e.into_inner());
        kept.push(outcome.clone());
        let excess = kept.len().saturating_sub(OUTCOMES_KEPT);
        kept.drain(..excess);
    }
    if outcome["state"] != "stopped" {
        return Err(format!("{title}: Codex was not stopped: {}", outcome["stop"]["reading"].as_str().unwrap_or("reason not reported")));
    }
    Ok(outcome)
}

#[cfg(test)]
#[path = "codex_stop_tests.rs"]
mod tests;
