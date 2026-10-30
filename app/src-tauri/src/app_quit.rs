//! App quit, asked first (DEL-01-02 DEF-6, K-4, §3.1 AS-03…AS-10, SQ-Q
//! Q-1…Q-7; DEL-01-04 §5.2 presents the question), and the window rules that
//! keep work alive when the window closes (DEF-1, SQ-W), with the App-level
//! indicator of waiting requests (DEL-01-04 §4.8 C-24).
//!
//! The person's quit is captured by the host through a native question (owner
//! OI-008 ruling: "The Rust host owns everything that writes the person's
//! files or the App's records, talks to Codex, or captures a person's act.
//! The web view presents, and sends only what the person initiates."). The
//! web view takes no part in it.
//!
//! Sequence: assess live work across every App-owned home (the same
//! assessment Stop/Restart Codex use); record `quit_requested` with the lists
//! (AS-03, AS-04). With nothing live nothing is asked and the quit proceeds
//! (AS-03). Otherwise the person is asked, with no timeout (Q-2). Cancel or
//! Keep running records `quit_answered` *cancelled* and changes nothing else
//! (AS-05). On Quit every ready home is closed to new turns and live work is
//! assessed again; a list that changed is recorded again and asked again
//! (AS-07). On the final confirmation `quit_answered` *confirmed* is
//! recorded, then each live turn's stop request (SR-01, cause *quit*) before
//! its interrupt is sent (AS-06, Q-4); the App waits until each turn is
//! observed ended or the quit wait limit passes (Q-5, AS-08). Before allowing
//! native exit every home's actual owned processes are settled (Q-6), then
//! `session_ended` *quit* is attempted with each quit stop request's state
//! (Q-7, AS-09). Unknown settlement keeps the App running and supervised.
//! A quit ends no workflow run and answers no request.

use crate::codex_stop::{interrupt_and_wait, Interrupts, STOP_WAIT_LIMIT};
use crate::runtime_session::{HomeSession, WorkflowRootSession};
use serde_json::{json, Value};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex, MutexGuard};
use std::time::{Duration, Instant};

/// U-R4 quit wait limit: the Stop Codex wait limit, a TEST VALUE owned by the
/// App implementation owner (see `codex_stop::STOP_WAIT_LIMIT`).
pub const QUIT_WAIT_LIMIT: Duration = STOP_WAIT_LIMIT;

/// The live-work assessment across homes. `material` is what must stay
/// unchanged between the question and the interrupts; it excludes the clock.
pub(crate) struct Assessment {
    pub(crate) material: Value,
    pub(crate) view: Value,
}
impl Assessment {
    pub(crate) fn new(material: Value) -> Self {
        let mut view = material.clone();
        view["observedAt"] = json!(crate::util::now_rfc3339());
        view["stopWaitLimitSeconds"] = json!(QUIT_WAIT_LIMIT.as_secs());
        view["limit"] = json!("None observed is not none: coverage of turns, requests and delegated agents is not complete. Workflow runs listed are those this App process holds.");
        Self { material, view }
    }
}

const LISTS: [&str; 4] = ["observedLiveTurns", "observedOutstandingRequests", "observedActiveChildren", "knownChildActivityUnknown"];

/// AS-03 / AS-04 guard: live work is a live turn, an outstanding entry or a
/// delegated child observed active, plus anything the assessment could not
/// resolve (a child of unknown activity, an unresolved turn observation, a
/// ready home it could not assess): none observed is not none, so those ask.
/// Workflow runs in force are listed in the question but alone ask nothing:
/// a quit ends no run.
pub(crate) fn has_live_work(material: &Value) -> bool {
    let any = |v: &Value| v.as_array().is_some_and(|a| !a.is_empty());
    LISTS.iter().any(|k| any(&material[*k])) || any(&material["coverage"]["turns"]["unresolved"]) || any(&material["assessmentLimits"])
}

/// One home's assessment folded into the App-wide lists.
pub(crate) fn merge(homes: Vec<(Value, Value)>, runs: Vec<Value>, limits: Vec<Value>) -> Value {
    let mut lists: Vec<Vec<Value>> = vec![Vec::new(); LISTS.len()];
    let mut unresolved = Vec::new();
    let mut rows = Vec::new();
    for (row, work) in homes {
        for (i, key) in LISTS.iter().enumerate() {
            lists[i].extend(work[*key].as_array().cloned().unwrap_or_default());
        }
        unresolved.extend(work["coverage"]["turns"]["unresolved"].as_array().cloned().unwrap_or_default());
        rows.push(row);
    }
    let mut material = json!({"homes":rows,"coverage":{"turns":{"unresolved":unresolved}},"runsInForce":runs,"assessmentLimits":limits});
    for (i, key) in LISTS.iter().enumerate() {
        material[*key] = Value::Array(std::mem::take(&mut lists[i]));
    }
    material
}

/// What the quit sequence needs from the world; `HostQuit` is the real
/// binding, tests use doubles.
pub(crate) trait QuitOps: Interrupts {
    fn assess(&mut self) -> Assessment;
    /// L `quit_requested` with the lists (AS-03, AS-04, AS-07).
    fn record_requested(&mut self, material: &Value) -> Value;
    /// The native question: Ok(true) only for the explicit Quit button;
    /// Err when the question could not be presented (never the person's cancel).
    fn confirm(&mut self, view: &Value) -> Result<bool, String>;
    /// L `quit_answered` (AS-05, AS-06).
    fn record_answered(&mut self, confirmed: bool) -> Value;
    /// Each ready home closed to new turns (no new turn or steer is sent).
    fn close_to_new_turns(&mut self);
    fn reopen_to_new_turns(&mut self);
    /// The turn's quit stop-request record as the App now holds it.
    fn stop_record(&mut self, turn: &Value) -> Value;
}

/// The person's decision and what was done before the App exits.
#[derive(Debug)]
pub(crate) enum Decision {
    /// AS-05: nothing was interrupted, stopped or sent.
    Cancelled(Value),
    /// The question could not be presented: no answer is recorded, nothing
    /// was interrupted, stopped or sent, and the App keeps running.
    NotAsked(Value),
    /// AS-03 or AS-06…AS-08: the App may now exit; `stopRequests` names the
    /// quit stop requests whose final state `session_ended` carries.
    Quit(Value),
}

pub(crate) fn quit_sequence<O: QuitOps>(ops: &mut O, wait_limit: Duration) -> Decision {
    let mut asked = ops.assess();
    let mut records = vec![ops.record_requested(&asked.material)];
    if !has_live_work(&asked.material) {
        // AS-03: close every ready home to new turns, so that no turn starts
        // between this assessment and the exit, and assess again. Still
        // nothing live: nothing is asked. Work started meanwhile is asked.
        ops.close_to_new_turns();
        let current = ops.assess();
        if !has_live_work(&current.material) {
            return Decision::Quit(json!({"state":"quit","asked":false,"assessment":current.view,"records":records,"turns":[],"stopRequests":[]}));
        }
        ops.reopen_to_new_turns();
        records.push(ops.record_requested(&current.material));
        asked = current;
    }
    let mut changed = false;
    let confirmed = loop {
        let mut view = asked.view.clone();
        if changed {
            view["changedWhileAsking"] = json!(true);
        }
        let chosen = match ops.confirm(&view) {
            Ok(chosen) => chosen,
            Err(refusal) => {
                ops.reopen_to_new_turns();
                return Decision::NotAsked(json!({"state":"not asked","reading":format!("The quit question could not be shown ({refusal}); the App keeps running. Nothing was interrupted, stopped or sent."),"assessment":view,"records":records}));
            }
        };
        if !chosen {
            ops.reopen_to_new_turns();
            records.push(ops.record_answered(false));
            return Decision::Cancelled(json!({"state":"cancelled","reading":"You kept the App running. Nothing was interrupted, stopped or sent.","assessment":view,"records":records}));
        }
        ops.close_to_new_turns();
        let current = ops.assess();
        // Work that ended meanwhile needs no new question: the person
        // confirmed a quit with more live; new or different work is asked.
        if current.material == asked.material || !has_live_work(&current.material) {
            break current;
        }
        ops.reopen_to_new_turns();
        records.push(ops.record_requested(&current.material));
        asked = current;
        changed = true;
    };
    records.push(ops.record_answered(true));
    let live: Vec<Value> = confirmed.material["observedLiveTurns"].as_array().cloned().unwrap_or_default();
    let (mut turns, ends) = interrupt_and_wait(ops, &live, Instant::now() + wait_limit);
    let mut stop_requests = Vec::new();
    for (turn, end) in turns.iter_mut().zip(&ends) {
        turn["codexReported"] = json!(end);
        let record = ops.stop_record(turn);
        if let Some(id) = record["stopRequestId"].as_str() {
            stop_requests.push(json!(id));
        }
        turn["stopRequest"] = record;
    }
    Decision::Quit(json!({"state":"quit","asked":true,"assessment":confirmed.view,"records":records,"turns":turns,"stopRequests":stop_requests,
        "outstandingRequests":"Not answered by the App; they end unanswered with the Codex processes (U-10).",
        "runsInForce":"Quitting ends no workflow run."}))
}

/// The real binding: every App-owned home, the App's workflow runs and the
/// person as the App observes them. `confirm` shows the native question.
pub(crate) struct HostQuit<'a, C> {
    pub(crate) homes: Vec<Arc<HomeSession>>,
    pub(crate) workflows: &'a Mutex<WorkflowRootSession>,
    pub(crate) confirm: C,
    /// The person as the App observes them (K1-4), for the records.
    pub(crate) person: Value,
    closed: Vec<(Arc<HomeSession>, Value)>,
}
impl<'a, C> HostQuit<'a, C> {
    pub(crate) fn new(homes: Vec<Arc<HomeSession>>, workflows: &'a Mutex<WorkflowRootSession>, person: &str, confirm: C) -> Self {
        Self { homes, workflows, confirm, person: crate::stop_records::person(person), closed: Vec::new() }
    }
    /// The ledger is the App's one REC custody; the account home's Host holds it.
    fn ledger_host(&self) -> Option<&Arc<HomeSession>> {
        self.homes.iter().find(|h| h.class() == crate::home_resources::HomeClass::Account).or(self.homes.first())
    }
    fn home_for(&self, generation: &Value) -> Option<&Arc<HomeSession>> {
        self.homes.iter().find(|h| h.host.snapshot()["generation"] == *generation)
    }
}

/// One home's live work as Stop Codex assesses it, or the reason it is not
/// assessed. Absent, stopped and refused homes have no Codex process.
pub(crate) fn assess_home(home: &HomeSession, workflows: &Mutex<WorkflowRootSession>) -> (Option<(Value, Value)>, Vec<Value>, Option<Value>) {
    let snapshot = home.host.snapshot();
    let generation = snapshot["generation"].clone();
    let state = snapshot["state"].as_str().unwrap_or("not reported").to_owned();
    let class = home.class().as_str();
    if matches!(state.as_str(), "absent" | "stopped" | "refused") || generation.is_null() {
        return (None, vec![], None);
    }
    let runs = generation["home"].as_str().map(|id| workflows.lock().unwrap().runs_in_force_in_home(id)).unwrap_or_default();
    let mut row = json!({"modeHomeClass":class,"generation":generation,"state":state});
    if state != "ready" {
        row["notReady"] = json!(format!("Codex is {state}, not ready: live work cannot be observed and nothing is sent to it; its process is stopped"));
        return (Some((row, json!({}))), runs, None);
    }
    match crate::runtime_session::assess_native_home_work(home, &generation) {
        Ok(work) => (Some((row, work.snapshot())), runs, None),
        Err(error) => (Some((row, json!({}))), runs, Some(json!(format!("{class}: {error}")))),
    }
}

impl<C> Interrupts for HostQuit<'_, C> {
    type Pending = (Arc<crate::hosting::Host>, crate::hosting::SourceRequest);
    fn interrupt(&mut self, turn: &Value) -> Result<Self::Pending, String> {
        let thread = turn["threadId"].as_str().ok_or("live turn without a conversation")?;
        let id = turn["turnId"].as_str().ok_or("live turn without an identity")?;
        let home = self.home_for(&turn["generation"]).ok_or("the turn's Codex process is no longer the current one; nothing sent")?;
        let class = crate::stop_records::home_class(home.class().as_str()).ok_or("this home has no App-owned home class")?;
        let host = Arc::clone(&home.host);
        let mut written = None;
        let person = &self.person;
        // The same guard as the person's Interrupt control; the request is
        // written (its SR-01 record first), not awaited.
        crate::runtime_session::interrupt_conversation_turn(&host.snapshot(), &turn["generation"], thread, id, |g, t, u| {
            written = Some(host.turn_interrupt_begin(g, t, u, crate::stop_records::Cause::Quit, class, person)?);
            Ok(Value::Null)
        })?;
        written.map(|w| (host, w)).ok_or_else(|| "interrupt request not written".to_owned())
    }
    fn acknowledgment(&mut self, pending: &Self::Pending, wait: Duration) -> Result<Value, String> {
        pending.0.turn_interrupt_acknowledgment(&pending.1, wait)
    }
    fn turn_reading(&mut self, turn: &Value) -> Option<Value> {
        let home = self.home_for(&turn["generation"])?;
        home.host.conversation_turn(&turn["generation"], turn["threadId"].as_str().unwrap_or_default(), turn["turnId"].as_str().unwrap_or_default())
    }
}
impl<C: FnMut(&Value) -> Result<bool, String>> QuitOps for HostQuit<'_, C> {
    fn assess(&mut self) -> Assessment {
        let (mut homes, mut runs, mut limits) = (Vec::new(), Vec::new(), Vec::new());
        for home in &self.homes {
            let (row, home_runs, limit) = assess_home(home, self.workflows);
            homes.extend(row);
            runs.extend(home_runs);
            limits.extend(limit);
        }
        Assessment::new(merge(homes, runs, limits))
    }
    fn record_requested(&mut self, material: &Value) -> Value {
        match self.ledger_host() {
            Some(home) => home.host.record_quit_requested(&self.person, material),
            None => json!({"state":"not recorded","reading":"no App-owned home holds the App ledger"}),
        }
    }
    fn confirm(&mut self, view: &Value) -> Result<bool, String> {
        (self.confirm)(view)
    }
    fn record_answered(&mut self, confirmed: bool) -> Value {
        match self.ledger_host() {
            Some(home) => home.host.record_quit_answered(&self.person, confirmed),
            None => json!({"state":"not recorded","reading":"no App-owned home holds the App ledger"}),
        }
    }
    fn close_to_new_turns(&mut self) {
        for home in &self.homes {
            let snapshot = home.host.snapshot();
            // Only a process this quit closed is recorded, so the quit reopens
            // only what it closed, never one a Stop/Restart closed.
            if snapshot["state"] == "ready" && home.host.close_to_new_turns(&snapshot["generation"]) == Ok(true) {
                self.closed.push((Arc::clone(home), snapshot["generation"].clone()));
            }
        }
    }
    fn reopen_to_new_turns(&mut self) {
        for (home, generation) in self.closed.drain(..) {
            home.host.reopen_to_new_turns(&generation);
        }
    }
    fn stop_record(&mut self, turn: &Value) -> Value {
        let Some(home) = self.home_for(&turn["generation"]) else { return Value::Null };
        let generation = crate::recovery::generation_ref(&turn["generation"]).unwrap_or_default();
        let rows = home.host.snapshot()["stopRequests"]["records"].clone();
        rows.as_array().into_iter().flatten().rev()
            .find(|r| r["generation"] == generation.as_str() && r["threadId"] == turn["threadId"] && r["turnId"] == turn["turnId"] && r["cause"] == "quit")
            .cloned().unwrap_or(Value::Null)
    }
}

/// The App's quit state, held in `AppState`.
#[derive(Default)]
pub(crate) struct AppQuit {
    /// One quit question at a time: set while a quit question is open or a
    /// quit is under way, by the [`QuestionGuard`] that `gate()` returns. A
    /// flag, not a lock, so that `busy()` only reads it and never takes
    /// anything a Quit pressed at that instant could find taken.
    open: AtomicBool,
    /// Set once the quit may proceed (AS-03 or a confirmed quit): the quit
    /// stop-request identities whose final states `session_ended` carries.
    proceed: Mutex<Option<Vec<String>>>,
}
/// Held while the quit question is open or the quit is under way; clears the
/// flag when dropped (also while unwinding from a panic).
#[must_use]
#[derive(Debug)]
pub(crate) struct QuestionGuard<'a>(&'a AtomicBool);
impl Drop for QuestionGuard<'_> {
    fn drop(&mut self) {
        self.0.store(false, Ordering::SeqCst);
    }
}
impl AppQuit {
    /// The question gate. None only while another guard is alive, that is
    /// while a quit question is truly open or a quit is under way; a second
    /// Quit then is ignored, the open question being in front of the person.
    pub(crate) fn gate(&self) -> Option<QuestionGuard<'_>> {
        self.open.compare_exchange(false, true, Ordering::SeqCst, Ordering::SeqCst).ok().map(|_| QuestionGuard(&self.open))
    }
    /// True while a quit question is open or a quit is under way (Stop and
    /// Restart Codex refuse meanwhile). Reads the flag; takes no lock.
    pub(crate) fn busy(&self) -> bool {
        self.open.load(Ordering::SeqCst)
    }
    /// Publish permission to exit only after actual owned-process settlement.
    /// A failed settlement leaves the App alive and the quit retryable.
    pub(crate) fn allow(&self, decision: &Decision, settle: impl FnOnce(&[String]) -> Result<Value, String>) -> Result<bool, String> {
        match decision {
            Decision::Quit(outcome) => {
                let ids: Vec<String> = outcome["stopRequests"].as_array().into_iter().flatten().filter_map(|v| v.as_str().map(str::to_owned)).collect();
                settle(&ids)?;
                *self.proceed.lock().unwrap_or_else(|e| e.into_inner()) = Some(ids);
                Ok(true)
            }
            Decision::Cancelled(_) | Decision::NotAsked(_) => Ok(false),
        }
    }
    /// The quit stop requests, once the quit may proceed; None otherwise.
    pub(crate) fn proceeding(&self) -> Option<Vec<String>> {
        self.proceed.lock().unwrap_or_else(|e| e.into_inner()).clone()
    }
}

/// One operation at a time over the Codex processes: a quit holds its own
/// question gate and the Stop/Restart Codex gate while its question is open
/// and its sequence runs (or until the person keeps the App running). The
/// guards are released when the sequence returns, which for a decided quit is
/// right after the App is asked to exit and before it has exited; from the
/// decision until the exit, Stop and Restart Codex are refused because the
/// quit is proceeding (`admit_codex_stop`), not by these guards. While Stop or
/// Restart Codex is under way the quit is refused with the reason, and nothing
/// is recorded or asked.
pub(crate) fn admit_quit<'a>(quit: &'a AppQuit, stop_gate: &'a Mutex<()>) -> Result<(QuestionGuard<'a>, MutexGuard<'a, ()>), String> {
    let question = quit.gate().ok_or("The quit question is already open.")?;
    let stop = crate::codex_stop::question_gate(stop_gate)
        .map_err(|_| "Stop or Restart Codex is under way, so Quit was not started. Choose Quit again when it has finished.".to_owned())?;
    Ok((question, stop))
}
/// The Stop/Restart Codex side: refused while a quit is open or under way,
/// and from a decided quit until the App has exited.
pub(crate) fn admit_codex_stop(quit: &AppQuit) -> Result<(), String> {
    if quit.proceeding().is_some() {
        return Err("The App is quitting; Stop or Restart Codex was not started".into());
    }
    if quit.busy() {
        return Err("The App quit is under way; Stop or Restart Codex was not started".into());
    }
    Ok(())
}

/// The HOSTING stop reason for a confirmed quit (AS-08); the recovery
/// projection reads it as cause *app-quit*.
pub(crate) const QUIT_STOP_REASON: &str = "quit confirmed by the person";

/// What to do with a request to exit the event loop (Tauri `ExitRequested`).
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum ExitAction {
    /// The quit was decided (AS-03 or confirmed): let the App exit.
    Allow,
    /// Prevent the exit and ask as for Quit (an exit nobody asked for).
    AskQuit,
    /// Prevent the exit only: the last window went away (DEF-1, not quit).
    Keep,
}
/// `code` is None when the event loop asks because the last window was
/// destroyed (DEF-1), Some for a programmatic exit.
pub(crate) fn on_exit_requested(proceeding: bool, code: Option<i32>) -> ExitAction {
    match (proceeding, code) {
        (true, _) => ExitAction::Allow,
        (false, None) => ExitAction::Keep,
        (false, Some(_)) => ExitAction::AskQuit,
    }
}

/// How the session ends on exit (AS-09 after a decided quit, else AS-10: the
/// system ended the App without the question, for example macOS `terminate:`
/// from the Dock's Quit, logout or shutdown) and each quit stop request's
/// final state as the homes now hold it.
pub(crate) fn session_end(proceeding: Option<Vec<String>>, records: &[Value]) -> (&'static str, Vec<Value>) {
    match proceeding {
        None => ("system-terminated", vec![]),
        Some(ids) => ("quit", ids.iter().filter_map(|id| {
            let last = records.iter().rev().find(|r| r["stopRequestId"] == id.as_str())?;
            Some(json!({"stopRequestId":id,"state":last["state"]}))
        }).collect()),
    }
}

/// Before deliberate exit: stop each App-owned home's Codex process (Q-6, AS-08;
/// HOSTING §4.5 closes the generation, so a quit stop request Codex never
/// reported ended gets SR-08), then write `session_ended` with each quit stop
/// request's state (Q-7, AS-09), or *system-terminated* (AS-10) when no quit
/// was decided. Returns the session-end observation.
pub(crate) fn finish_exit(homes: &[Arc<HomeSession>], proceeding: Option<Vec<String>>) -> Result<Value, String> {
    let custody = homes.iter().find(|home| home.class() == crate::home_resources::HomeClass::Account)
        .ok_or_else(|| "no App-owned account home".to_owned()).and_then(|home| home.host.app_runtime_custody());
    // AS-10: the system allows a final write; write it first, then stop each
    // home's process as the system allows.
    let early = if proceeding.is_none() { Some(custody.as_ref().map_err(Clone::clone).and_then(|c| c.record_app_session_end_as("system-terminated", &[]))) } else { None };
    let (actor, reason) = if proceeding.is_some() { ("the person", QUIT_STOP_REASON) } else { ("the system", "system termination") };
    // Fence every home before settling any one of them. Retain these fences
    // through successful session-end publication and the native exit.
    for home in homes { home.host.begin_quit(); }
    let mut failures = Vec::new();
    for home in homes {
        if let Err(error) = home.host.settle_for_quit(actor, reason) {
            failures.push(format!("{}: {error}", home.class().as_str()));
        }
    }
    let records: Vec<Value> = homes.iter().flat_map(|home| home.host.snapshot()["stopRequests"]["records"].as_array().cloned().unwrap_or_default()).collect();
    if let Some(early) = early {
        // AS-10 cannot delay system-forced termination. Report cleanup limits
        // separately instead of presenting them as normal Quit.
        if !failures.is_empty() { eprintln!("chirality: system termination cleanup unavailable: {}", failures.join("; ")); }
        return early.map(|mut observation| { observation["ownedProcessCleanupLimits"] = json!(failures); observation });
    }
    if !failures.is_empty() {
        for home in homes { home.host.cancel_quit(); }
        return Err(format!("The App is still running: owned supplier settlement is unavailable ({}). No quit session-end record was written. Supervision is retained; inspect Host diagnostics before retrying Quit.", failures.join("; ")));
    }
    let (how, stops) = session_end(proceeding, &records);
    // Q-7: ledger failure is a recording limit, not grounds to fabricate an
    // end or block an already settled exit. Recovery reads ended-without-record.
    Ok(custody.and_then(|c| c.record_app_session_end_as(how, &stops))
        .unwrap_or_else(|error| json!({"write":"not-confirmed","limit":error,"standing":"owned processes settled; session-end recording unavailable"})))
}

/// C-24 (DEL-01-04 §4.8 WI-1, WI-2): supplier requests waiting for the
/// person's answer across every App-owned home, counted from each home's
/// current register whether or not a window shows them. Checkpoint arrivals
/// are not supplier requests and never count.
pub(crate) fn waiting_requests(snapshots: &[Value]) -> Value {
    let mut conversations = std::collections::BTreeSet::new();
    let mut count = 0;
    for snapshot in snapshots {
        for request in snapshot["serverRequests"].as_array().into_iter().flatten() {
            if request["state"] == "outstanding" && request["generation"] == snapshot["generation"] && !snapshot["generation"].is_null() {
                count += 1;
                if let Some(thread) = request["nativeParameters"]["threadId"].as_str() {
                    conversations.insert(thread.to_owned());
                }
            }
        }
    }
    json!({"count":count,"conversations":conversations.into_iter().collect::<Vec<_>>()})
}

#[cfg(test)]
#[path = "app_quit_tests.rs"]
mod tests;
