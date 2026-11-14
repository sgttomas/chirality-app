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
//!
//! Quit waits on nothing it cannot name and on nothing without a bound. A key
//! operation holding the App's key setup is named from what it publishes
//! ([`KeyHold`]): one asking the person refuses the quit; one waiting on a
//! home's Codex is offered as part of quitting ([`admit_key_setup`]). The
//! question and answer records never wait on the App's recovery writer (they
//! queue in order). The session-end record is written on its own thread after
//! every home is settled and waited for at most [`RECORDING_WAIT_LIMIT`].

use crate::codex_stop::{interrupt_and_wait, Interrupts, Unsent, STOP_WAIT_LIMIT};
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
    /// Set when the person's confirming answer is queued; until then a
    /// dropped binding hands the queued question (and any keep-running
    /// answer) to an ordinary flush that nothing waits on.
    confirmed: bool,
}
/// A quit the person kept running, or one never asked: the queued question
/// and answer are written by an ordinary flush on its own thread, which the
/// App does not wait for (the person's answer is not delayed by the ledger).
impl<C> Drop for HostQuit<'_, C> {
    fn drop(&mut self) {
        if self.confirmed { return; }
        if let Some(home) = self.ledger_host().cloned() {
            let _ = std::thread::Builder::new().name("quit-kept-running-flush".into()).spawn(move || { home.host.flush_recovery_observations(); });
        }
    }
}
impl<'a, C> HostQuit<'a, C> {
    pub(crate) fn new(homes: Vec<Arc<HomeSession>>, workflows: &'a Mutex<WorkflowRootSession>, person: &str, confirm: C) -> Self {
        Self { homes, workflows, confirm, person: crate::stop_records::person(person), closed: Vec::new(), confirmed: false }
    }
    /// The ledger is the App's one REC custody; the account home's Host holds it.
    fn ledger_host(&self) -> Option<&Arc<HomeSession>> {
        self.homes.iter().find(|h| h.class() == crate::home_resources::HomeClass::Account).or(self.homes.first())
    }
    fn home_for(&self, generation: &Value) -> Option<&Arc<HomeSession>> {
        self.homes.iter().find(|h| h.host.snapshot_without_records()["generation"] == *generation)
    }
}

/// How long one assessment waits for every home's live work to be read, and
/// for the App's workflow runs: one deadline for all homes. A home's read
/// takes that home's observation (`home.runtime`), which the App's tick and
/// commands also hold, and Codex's delivered state, which reads the records
/// capability's view and the distribution store; any of them may wait on file
/// I/O. Execution lane's own bound (App Type 1), its to change.
pub(crate) const QUIT_ASSESSMENT_WAIT_LIMIT: Duration = Duration::from_secs(5);
/// What the question shows for a home whose live work was not read in time.
/// It counts as live work (`has_live_work`): what could not be read is
/// treated as possibly live, never as idle.
pub(crate) fn live_work_not_read(class: crate::home_resources::HomeClass) -> String {
    format!("{} home: live work could not be read within {} seconds", home_name(class), QUIT_ASSESSMENT_WAIT_LIMIT.as_secs())
}
/// Quit refused because the App's list of homes was held past the bound.
pub(crate) fn homes_not_read() -> String {
    format!("The App's list of Codex homes was held by another App activity for {} seconds, so quitting did not begin. The App is still running.", QUIT_ASSESSMENT_WAIT_LIMIT.as_secs())
}
/// What the question shows when the App's workflow runs were not read in time.
pub(crate) fn runs_not_read() -> String {
    format!("Workflow runs could not be read within {} seconds", QUIT_ASSESSMENT_WAIT_LIMIT.as_secs())
}
/// Every home's live work as Stop Codex assesses it, or the reason it is not
/// assessed, waited for until `deadline`. Each home is read on its own
/// thread, its state and generation included; a read not finished by the
/// deadline is left to finish on its own (it updates that home's observation
/// as any read does) and its result is never used. Absent, stopped and refused
/// homes have no Codex process. The workflow runs listed are those of each home
/// with a Codex process and of each home whose state was not read in time.
pub(crate) fn assess_homes(homes: &[Arc<HomeSession>], workflows: &Mutex<WorkflowRootSession>, deadline: Instant) -> (Vec<(Value, Value)>, Vec<Value>, Vec<Value>) {
    let (sent, received) = std::sync::mpsc::channel();
    let mut pending = Vec::new();
    let mut limits = Vec::new();
    for (index, home) in homes.iter().enumerate() {
        let class = home.class();
        // The home's state and generation are read in the reader too: reading
        // them takes the Host state, which a stalled activity can hold, and
        // the deadline must cover that wait.
        let (home, sent) = (Arc::clone(home), sent.clone());
        let reader = std::thread::Builder::new().name("quit-assessment".into()).spawn(move || {
            let _ = sent.send((index, assess_home(&home)));
        });
        match reader {
            Ok(_) => pending.push((index, class)),
            Err(error) => limits.push(json!(format!("{}: live work could not be read ({error})", class.as_str()))),
        }
    }
    drop(sent);
    let runs_by_home = match crate::util::lock_by(workflows, deadline) {
        Some(root) => Some(root.runs_in_force_by_home()),
        None => {
            limits.push(json!(runs_not_read()));
            None
        }
    };
    let mut rows: Vec<Option<(Value, Value)>> = vec![None; homes.len()];
    // The homes whose runs are listed: each home with a Codex process, and
    // each home whose state was not read in time (from its configuration).
    let mut home_ids: Vec<Option<String>> = homes.iter().map(|home| home.host_config.as_ref().ok().map(crate::hosting::home_reference)).collect();
    while !pending.is_empty() {
        let Ok((index, read)) = received.recv_timeout(deadline.saturating_duration_since(Instant::now())) else { break };
        let Some(at) = pending.iter().position(|(i, _)| *i == index) else { continue };
        let (_, class) = pending.remove(at);
        match read {
            None => home_ids[index] = None,
            Some((home_id, row, work)) => {
                home_ids[index] = home_id;
                match work {
                    Ok(work) => rows[index] = Some((row, work)),
                    Err(error) => {
                        rows[index] = Some((row, json!({})));
                        limits.push(json!(format!("{}: {error}", class.as_str())));
                    }
                }
            }
        }
    }
    limits.extend(pending.into_iter().map(|(_, class)| json!(live_work_not_read(class))));
    let runs = runs_by_home.map(|by_home| home_ids.iter().flatten().flat_map(|id| by_home.get(id).cloned().unwrap_or_default()).collect()).unwrap_or_default();
    (rows.into_iter().flatten().collect(), runs, limits)
}
/// One home's part of the assessment, on its reader thread: None where the
/// home has no Codex process (absent, stopped, refused, or no generation);
/// otherwise its generation's home reference, its row, and its live work read
/// (none read where Codex is not ready).
fn assess_home(home: &HomeSession) -> Option<(Option<String>, Value, Result<Value, String>)> {
    let snapshot = home.host.snapshot_without_records();
    let generation = snapshot["generation"].clone();
    let state = snapshot["state"].as_str().unwrap_or("not reported").to_owned();
    if matches!(state.as_str(), "absent" | "stopped" | "refused") || generation.is_null() {
        return None;
    }
    let home_id = generation["home"].as_str().map(str::to_owned);
    let mut row = json!({"modeHomeClass":home.class().as_str(),"generation":generation,"state":state});
    if state != "ready" {
        row["notReady"] = json!(format!("Codex is {state}, not ready: live work cannot be observed and nothing is sent to it; its process is stopped"));
        return Some((home_id, row, Ok(json!({}))));
    }
    let work = crate::runtime_session::assess_native_home_work(home, &generation).map(|work| work.snapshot());
    Some((home_id, row, work))
}

impl<C> Interrupts for HostQuit<'_, C> {
    type Pending = (Arc<crate::hosting::Host>, crate::hosting::SourceRequest);
    fn interrupt(&mut self, turn: &Value, deadline: Instant) -> Result<Self::Pending, Unsent> {
        let unsent = |reason: &str| Unsent::NotSent(reason.to_owned());
        let thread = turn["threadId"].as_str().ok_or_else(|| unsent("live turn without a conversation"))?;
        let id = turn["turnId"].as_str().ok_or_else(|| unsent("live turn without an identity"))?;
        let home = self.home_for(&turn["generation"]).ok_or_else(|| unsent("the turn's Codex process is no longer the current one; nothing sent"))?;
        let class = crate::stop_records::home_class(home.class().as_str()).ok_or_else(|| unsent("this home has no App-owned home class"))?;
        let host = Arc::clone(&home.host);
        let mut written = None;
        let person = &self.person;
        // The same guard as the person's Interrupt control; the request is
        // written (its SR-01 record first), not awaited, and its write is
        // waited for no later than the quit's stop deadline.
        crate::runtime_session::interrupt_conversation_turn(&host.snapshot_without_records(), &turn["generation"], thread, id, |g, t, u| {
            written = Some(host.turn_interrupt_within(g, t, u, crate::stop_records::Cause::Quit, class, person, deadline));
            Ok(Value::Null)
        }).map_err(Unsent::NotSent)?;
        let written: Result<crate::hosting::SourceRequest, Unsent> = written.map_or_else(|| Err(unsent("interrupt request not written")), Into::into);
        written.map(|w| (host, w))
    }
    fn acknowledgment(&mut self, pending: &Self::Pending, wait: Duration) -> Result<Value, String> {
        pending.0.turn_interrupt_acknowledgment_for_quit(&pending.1, wait)
    }
    fn turn_reading(&mut self, turn: &Value) -> Option<Value> {
        let home = self.home_for(&turn["generation"])?;
        home.host.conversation_turn(&turn["generation"], turn["threadId"].as_str().unwrap_or_default(), turn["turnId"].as_str().unwrap_or_default())
    }
}
impl<C: FnMut(&Value) -> Result<bool, String>> QuitOps for HostQuit<'_, C> {
    fn assess(&mut self) -> Assessment {
        let (homes, runs, limits) = assess_homes(&self.homes, self.workflows, Instant::now() + QUIT_ASSESSMENT_WAIT_LIMIT);
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
        self.confirmed |= confirmed;
        match self.ledger_host() {
            Some(home) => home.host.record_quit_answered(&self.person, confirmed),
            None => json!({"state":"not recorded","reading":"no App-owned home holds the App ledger"}),
        }
    }
    fn close_to_new_turns(&mut self) {
        for home in &self.homes {
            let snapshot = home.host.snapshot_without_records();
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
        let rows = home.host.snapshot_without_records()["stopRequests"]["records"].clone();
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

/// What a key operation holding the App's key setup has published about what
/// it waits on, read beside the key setup when Quit finds it held
/// (`AppState::key_hold`). The key operation publishes it while it holds the
/// key setup and clears it before letting go; quit only reads it. No key
/// operation publishes it yet (the key operations' publisher comes later), so
/// its variants are constructed only by tests until then.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[cfg_attr(not(test), allow(dead_code))]
pub(crate) enum KeyHold {
    /// The operation is asking the person (key entry, sign-in, capture
    /// sealing): quit refuses, the question being in front of the person.
    Asking,
    /// The operation is waiting on Codex for that home: quit can end that wait
    /// by stopping that home's Codex, and offers to.
    WaitingOnCodex(crate::home_resources::HomeClass),
}
/// Today's refusal while a key operation holds the key setup and has not
/// published that it waits on a home's Codex.
pub(crate) const KEY_OPERATION_UNDER_WAY: &str = "An explicit key operation is under way. The App is still running; choose Quit again when that operation has finished.";
/// How long quit waits for the key operation to let go of the key setup once
/// the home's Codex it waited on is stopped. Named in [`key_still_held`].
pub(crate) const KEY_RELEASE_WAIT_LIMIT: Duration = Duration::from_secs(10);
/// The buttons of the key-operation offer: Keep running (the default) changes
/// nothing; only Quit anyway acts.
pub(crate) const QUIT_ANYWAY: &str = "Quit anyway";
/// A home as the person reads its name in a sentence.
pub(crate) fn home_name(class: crate::home_resources::HomeClass) -> &'static str {
    use crate::home_resources::HomeClass;
    match class {
        HomeClass::Account => "account",
        HomeClass::ApiKey => "API-key",
        HomeClass::LocalProvider => "local model",
        HomeClass::Probe => "probe",
    }
}
fn article(name: &str) -> &'static str {
    if name.starts_with(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']) { "An" } else { "A" }
}
/// The offer when the key operation waits on that home's Codex.
pub(crate) fn key_wait_offer(class: crate::home_resources::HomeClass) -> String {
    let name = home_name(class);
    format!("{} {name} settings change is waiting for Codex for the {name} home. Quit anyway: Codex for that home is stopped first, and the settings are not changed.", article(name))
}
/// The refusal when the key operation still holds the key setup at the bound.
pub(crate) fn key_still_held(class: crate::home_resources::HomeClass) -> String {
    format!("A key operation for the {} home still holds the App's key setup {} seconds after Codex for that home was stopped. The App is still running.", home_name(class), KEY_RELEASE_WAIT_LIMIT.as_secs())
}
/// The refusal when that home's Codex could not be stopped.
pub(crate) fn key_home_not_stopped(class: crate::home_resources::HomeClass, error: &str) -> String {
    format!("Codex for the {} home could not be stopped ({error}), so the key operation waiting for it was not ended. The App is still running.", home_name(class))
}
/// Quit's admission past the key setup.
#[derive(Debug)]
pub(crate) enum KeyAdmission<'a> {
    /// The key setup is held for the quit; the quit sequence continues.
    Admitted(MutexGuard<'a, ()>),
    /// Quit is refused with this reason; nothing was recorded or asked.
    Refused(String),
    /// The person chose Keep running at the offer: nothing was done.
    KeptRunning,
    /// The offer could not be shown: nothing was done.
    NotAsked(String),
}
/// SQ-Q: Quit and a key operation holding the key setup. Free: taken for the
/// quit. Held with nothing published, or by an operation asking the person:
/// refused with today's words. Held by an operation waiting on a home's Codex:
/// the person is offered to stop that home's Codex as part of quitting. Their
/// answer applies to what the offer named: the published hold is read again
/// after the answer and, if it changed or cleared, assessed again from the
/// start (a cleared hold with the key setup free is taken without stopping
/// anything; a different home is offered again in its own words). On Quit
/// anyway with the hold unchanged, that home's Codex is stopped (the Host's
/// bounded stop, its source gate taken within `release_wait`), then the key
/// setup is waited for up to `release_wait`.
pub(crate) fn admit_key_setup<'a>(key_setup: &'a Mutex<()>, hold: &Mutex<Option<KeyHold>>, homes: &[Arc<HomeSession>], mut offer: impl FnMut(&str) -> Result<bool, String>, release_wait: Duration) -> KeyAdmission<'a> {
    let read = || *hold.lock().unwrap_or_else(|e| e.into_inner());
    let class = loop {
        if let Ok(held) = key_setup.try_lock() {
            return KeyAdmission::Admitted(held);
        }
        let published = read();
        let class = match published {
            Some(KeyHold::WaitingOnCodex(class)) => class,
            None | Some(KeyHold::Asking) => return KeyAdmission::Refused(KEY_OPERATION_UNDER_WAY.into()),
        };
        match offer(&key_wait_offer(class)) {
            Ok(true) => {}
            Ok(false) => return KeyAdmission::KeptRunning,
            Err(reason) => return KeyAdmission::NotAsked(reason),
        }
        if read() == published {
            break class;
        }
    };
    let stop_by = Instant::now() + release_wait;
    for home in homes.iter().filter(|home| home.class() == class) {
        if let Err(error) = home.host.stop_for_quit("the person", QUIT_STOP_REASON, stop_by) {
            let state = home.host.snapshot_without_records()["state"].as_str().unwrap_or_default().to_owned();
            if !matches!(state.as_str(), "absent" | "stopped" | "refused") {
                return KeyAdmission::Refused(key_home_not_stopped(class, &error));
            }
        }
    }
    let deadline = Instant::now() + release_wait;
    match crate::util::lock_by(key_setup, deadline) {
        Some(held) => KeyAdmission::Admitted(held),
        None => KeyAdmission::Refused(key_still_held(class)),
    }
}

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

/// What the person reads when a quit is withheld because a Codex process group the App started
/// can never be established ended in this App session (its reservation is lost and its group
/// is not known empty). The temporary case, where settlement was merely unavailable this time,
/// keeps its own sentence.
pub(crate) const QUIT_CANNOT_ESTABLISH: &str = "Chirality cannot establish whether a Codex process group it started has ended. Retrying Quit cannot resolve this in the current App session. You can end Chirality using macOS Force Quit, but that does not establish that Codex or its descendants have ended.";
/// How long the exit waits for the session-end record (and the App custody it
/// needs) to be confirmed written, from when that wait begins. The writing
/// thread is not ended at the bound; a result it reports later is not observed.
pub(crate) const RECORDING_WAIT_LIMIT: Duration = Duration::from_secs(10);
/// How long the exit waits, across every home, for a Codex start under way to
/// let go of its home's source gate so that the home can be fenced.
pub(crate) const QUIT_FENCE_WAIT_LIMIT: Duration = Duration::from_secs(10);
/// What this quit had done before a refusal at fencing or settlement, from
/// the phases it completed: the interrupts it asked for (the quit stop
/// requests), which are not withdrawn. Empty when it asked for none.
fn interrupts_before(interrupted: usize) -> String {
    match interrupted {
        0 => String::new(),
        1 => "This quit had already asked Codex to interrupt 1 running turn; that request is not withdrawn. ".into(),
        n => format!("This quit had already asked Codex to interrupt {n} running turns; those requests are not withdrawn. "),
    }
}
/// The person's quit refused at fencing: a home's request gate (which a Codex
/// start and the App's other requests to that Codex take) was not free within
/// the bound. It says what the quit had done and what it then did not do; it
/// does not say what held the gate, which is not established.
pub(crate) fn gate_not_free(class: crate::home_resources::HomeClass, interrupted: usize) -> String {
    format!("{}Another App activity held the request gate of Codex for the {} home for {} seconds, so this quit stopped there: it stopped no Codex process and recorded no end of this session. The App is still running.",
        interrupts_before(interrupted), home_name(class), QUIT_FENCE_WAIT_LIMIT.as_secs())
}
/// The person's quit refused at settlement: what this quit had done, which
/// homes it stopped Codex for before the failure, and that it recorded no end.
pub(crate) fn settlement_unavailable(interrupted: usize, settled: &[crate::home_resources::HomeClass], failures: &[String]) -> String {
    let stopped = match settled {
        [] => String::new(),
        homes => format!("It stopped Codex for the {} {}. ", homes.iter().map(|class| home_name(*class)).collect::<Vec<_>>().join(" and "), if homes.len() == 1 { "home" } else { "homes" }),
    };
    format!("{}{stopped}The App is still running: owned supplier settlement is unavailable ({}). No quit session-end record was written. Supervision is retained; inspect Host diagnostics before retrying Quit.",
        interrupts_before(interrupted), failures.join("; "))
}
/// What every notice before the person's quit exits says first: settlement
/// established that each home's original owned process group is empty.
const QUITTING: &str = "Chirality is quitting. The App's own processes for every Codex home have ended.";
/// The notice shown, with OK only, before the person's quit exits when the
/// session-end record was not confirmed within [`RECORDING_WAIT_LIMIT`].
pub(crate) const RECORDING_NOT_CONFIRMED: &str = "Chirality is quitting. The App's own processes for every Codex home have ended. Recording the end of this session was not confirmed within 10 seconds, so the record may or may not have been written; the next start reads it as it finds it.";
/// The same notice when the write returned before the bound with its outcome
/// unknown (the ledger refused the append): the host's own reason in place of
/// "within 10 seconds". The reason is what the host returned, not a reading.
pub(crate) fn recording_failed_notice(reason: &str) -> String {
    format!("{QUITTING} Recording the end of this session was not confirmed ({reason}), so the record may or may not have been written; the next start reads it as it finds it.")
}
/// The notice when no write of the session end was made (no ledger, no App
/// custody, the entry could not be formed or its thread not started), with
/// the host's own reason.
pub(crate) fn recording_not_written_notice(reason: &str) -> String {
    format!("{QUITTING} The end of this session was not recorded ({reason}); the next start reads the ledger as it finds it.")
}
/// `work` on its own thread, waited for at most `limit`; Err when it does not
/// report in time (it is not ended; a later result is not observed) or its
/// thread could not be started.
fn within<T: Send + 'static>(name: &str, limit: Duration, work: impl FnOnce() -> T + Send + 'static) -> Result<T, Within> {
    let (sent, received) = std::sync::mpsc::channel();
    std::thread::Builder::new().name(name.into()).spawn(move || { let _ = sent.send(work()); }).map_err(|error| Within::NotStarted(error.to_string()))?;
    received.recv_timeout(limit).map_err(|_| Within::NotInTime)
}
enum Within { NotStarted(String), NotInTime }
/// The exit's end of this session's delegation observations. `end` takes the
/// conversation links by the deadline it is given and records the ends, which
/// writes and syncs files; it runs on its own thread, and the exit waits for
/// it until `by`, never longer. Returns what the exit logs, if anything: the
/// links not had, the work not finished (what it had not written is left as a
/// crash leaves it), or the thread not started.
pub(crate) fn end_delegation_within(by: Instant, end: impl FnOnce(Instant) -> bool + Send + 'static) -> Option<String> {
    let limit = QUIT_ASSESSMENT_WAIT_LIMIT.as_secs();
    match within("delegation-exit", by.saturating_duration_since(Instant::now()), move || end(by)) {
        Ok(true) => None,
        Ok(false) => Some(format!("delegation observation not ended: the App's conversation links were held by another App activity for {limit} seconds")),
        Err(Within::NotInTime) => Some(format!("ending this session's delegation observations did not finish within {limit} seconds; what it had not written is left as a crash leaves it")),
        Err(Within::NotStarted(error)) => Some(format!("delegation observation not ended: its thread could not be started ({error})")),
    }
}
/// The session-end write (taking the App custody first if it is not yet
/// held) on its own thread, waited for at most `limit`. That thread drains
/// every home's queued recovery facts, in each home's order, before the end
/// entry. The observation the write reports, or `not-confirmed` with the
/// reason it was not observed.
fn record_session_end_within(homes: &[Arc<HomeSession>], how: &'static str, stops: Vec<Value>, limit: Duration) -> Result<Value, String> {
    let account = homes.iter().find(|home| home.class() == crate::home_resources::HomeClass::Account).cloned();
    let written = within("quit-session-end", limit, move || {
        let result = match &account {
            None => Err("no App-owned account home".to_owned()),
            Some(home) => home.host.app_runtime_custody().and_then(|custody| custody.record_app_session_end_as(how, &stops)),
        };
        #[cfg(test)]
        if let Some(home) = &account { home.host.after_quit_recording(); }
        result
    });
    match written {
        Ok(result) => result,
        Err(Within::NotStarted(error)) => Err(format!("the session-end recording could not be started: {error}")),
        Err(Within::NotInTime) => Ok(json!({"write":"not-confirmed","waitLimitSeconds":limit.as_secs(),
            "limit":format!("Recording the end of this session was not confirmed within {} seconds; the record may or may not have been written.", limit.as_secs()),
            "standing":"the write was not observed to complete; it may complete after this observation"})),
    }
}
/// After the system's early session end: the recovery facts settlement left
/// queued (drains being deferred once fenced), written on their own thread
/// and waited for at most `limit`.
fn drain_after_settlement_within(homes: &[Arc<HomeSession>], limit: Duration) -> Value {
    let Some(account) = homes.iter().find(|home| home.class() == crate::home_resources::HomeClass::Account).cloned() else {
        return json!({"standing":"no App-owned account home; queued facts not written"});
    };
    match within("quit-final-drain", limit, move || account.host.app_runtime_custody().map(|custody| custody.flush_captured_recovery())) {
        Ok(Ok(observation)) => observation,
        Ok(Err(error)) => json!({"standing":format!("queued facts not written: {error}")}),
        Err(Within::NotStarted(error)) => json!({"standing":format!("queued facts not written: the drain could not be started: {error}")}),
        Err(Within::NotInTime) => json!({"standing":format!("queued facts not confirmed written within {} seconds", limit.as_secs())}),
    }
}
/// Before deliberate exit: fence every App-owned home (within
/// [`QUIT_FENCE_WAIT_LIMIT`] across all of them), settle each home's actual
/// owned processes (Q-6, AS-08; HOSTING §4.5 closes the generation, so a quit
/// stop request Codex never reported ended gets SR-08), and only then record
/// `session_ended` with each quit stop request's state (Q-7, AS-09), waiting
/// for that record at most [`RECORDING_WAIT_LIMIT`]. A home not fenced in time
/// or a settlement failure refuses the person's quit before any recording.
/// From the fence on, nothing drains the recovery queues on this thread: the
/// recording thread drains them first. With no quit decided (AS-10) the
/// *system-terminated* record is written first, as the system allows, waited
/// for at most the same bound, then every home is fenced and settled, then
/// the facts settlement queued are written, waited for at most the same bound.
/// Returns the session-end observation.
pub(crate) fn finish_exit(homes: &[Arc<HomeSession>], proceeding: Option<Vec<String>>) -> Result<Value, String> {
    // AS-10: the system allows a final write; write it first (bounded), then
    // stop each home's process as the system allows.
    let early = if proceeding.is_none() { Some(record_session_end_within(homes, "system-terminated", vec![], RECORDING_WAIT_LIMIT)) } else { None };
    let (actor, reason) = if proceeding.is_some() { ("the person", QUIT_STOP_REASON) } else { ("the system", "system termination") };
    // Fence every home before settling any one of them, one deadline for all.
    // Retain these fences through session-end publication and the native exit.
    let fence_by = Instant::now() + QUIT_FENCE_WAIT_LIMIT;
    let interrupted = proceeding.as_ref().map_or(0, Vec::len);
    let mut failures = Vec::new();
    for home in homes {
        if let Err(error) = home.host.begin_quit_by(fence_by) {
            if proceeding.is_some() {
                for home in homes { home.host.cancel_quit(); }
                return Err(gate_not_free(home.class(), interrupted));
            }
            failures.push(format!("{}: {error}", home.class().as_str()));
        }
    }
    let mut settled = Vec::new();
    for home in homes {
        // A home the system's exit could not fence is not settled: its own
        // settlement refuses without the fence, and is reported as a limit.
        match home.host.settle_for_quit(actor, reason) {
            Ok(_) => settled.push(home.class()),
            Err(error) => failures.push(format!("{}: {error}", home.class().as_str())),
        }
    }
    let records: Vec<Value> = homes.iter().flat_map(|home| home.host.snapshot_without_records()["stopRequests"]["records"].as_array().cloned().unwrap_or_default()).collect();
    if let Some(early) = early {
        // AS-10 cannot delay system-forced termination. Report cleanup limits
        // separately instead of presenting them as normal Quit. No notice is
        // shown: the next start reads what the ledger holds.
        // The drain needs the same App writer as the early write: when that
        // write was not observed within its bound, the drain is not waited for.
        let drained = match &early {
            Ok(observation) if observation.get("waitLimitSeconds").is_some() => json!({"standing":"not attempted: the early session-end write was not observed within its bound, and this drain needs the same App writer"}),
            _ => drain_after_settlement_within(homes, RECORDING_WAIT_LIMIT),
        };
        if !failures.is_empty() { eprintln!("chirality: system termination cleanup unavailable: {}", failures.join("; ")); }
        if let Ok(observation) = &early {
            if observation["write"] == "not-confirmed" { eprintln!("chirality: {}", observation["limit"].as_str().unwrap_or("system termination session end not confirmed")); }
        }
        return early.map(|mut observation| { observation["ownedProcessCleanupLimits"] = json!(failures); observation["queuedAfterSettlement"] = drained; observation });
    }
    if !failures.is_empty() {
        for home in homes { home.host.cancel_quit(); }
        // A group whose reservation is lost and that is not known empty can never be established
        // settled in this App session: retrying cannot change it, and the App no longer
        // supervises that group. Selected by that established state, not by an error's text.
        // (Reached when a reservation is lost at creation or at any later observation.)
        if homes.iter().any(|home| home.host.has_unestablishable_process()) {
            return Err(QUIT_CANNOT_ESTABLISH.into());
        }
        return Err(settlement_unavailable(interrupted, &settled, &failures));
    }
    let (how, stops) = session_end(proceeding, &records);
    // Q-7: a ledger limit is a recording limit, not grounds to fabricate an
    // end or block an already settled exit. Every result other than the
    // confirmed write is told to the person before the exit, with the host's
    // own reason; the next start reads the ledger as it finds it.
    Ok(match record_session_end_within(homes, how, stops, RECORDING_WAIT_LIMIT) {
        Ok(mut observation) => {
            let reason = observation["limit"].as_str().map(str::to_owned).unwrap_or_else(|| format!("the host reported the write as {}", observation["write"]));
            let notice = match observation["write"].as_str() {
                Some("confirmed") => None,
                Some("not-confirmed") if observation.get("waitLimitSeconds").is_some() => Some(RECORDING_NOT_CONFIRMED.to_owned()),
                Some("not-attempted") => Some(recording_not_written_notice(&reason)),
                _ => Some(recording_failed_notice(&reason)),
            };
            if let Some(notice) = notice { observation["notice"] = json!(notice); }
            observation
        }
        // A failure the host returned before the bound: nothing was written.
        Err(error) => json!({"write":"not-confirmed","limit":error,"standing":"owned processes settled; session-end recording unavailable","notice":recording_not_written_notice(&error)}),
    })
}
/// The notice the person's quit shows before exit, when its session-end
/// observation carries one.
pub(crate) fn recording_notice(observation: &Value) -> Option<&str> {
    observation["notice"].as_str()
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
