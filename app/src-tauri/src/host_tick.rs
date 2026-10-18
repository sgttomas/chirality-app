//! The Rust host's own observation ticks. Under the owner's OI-008 ruling ("The
//! Rust host owns everything that writes the person's files or the App's
//! records, talks to Codex, or captures a person's act. The web view presents,
//! and sends only what the person initiates.") the host keeps its records
//! whether or not the web view polls:
//! - the record tick receives every home's native frames and lets the
//!   checkpoint recorder record what the view shows of the open runs (EXEC §2.4);
//! - the trial tick, on its own thread so that a slow Codex read never delays
//!   the record tick, makes the recovery reads due once a home's Codex is
//!   ready after a restart (RECOVERY §3.2 CV-11…CV-15), the trial reads that
//!   are due (WR TT-9) and the delegation readings of conversations not read
//!   yet (NPTD §7.1).
//!
//! `host_status` only reads (`workflow_status`, `tick_state`).
use crate::runtime_session::{record_run_observations, trial_flows, HomeRouter, HomeSession, WorkflowRootSession};
use serde_json::{json, Value};
use std::sync::Mutex;

/// The ticks' interval (the web view polls `host_status` at about the same rate).
pub(crate) const INTERVAL: std::time::Duration = std::time::Duration::from_secs(1);

/// One home's current native view: its new frames received, as `host_status`
/// receives them (runtime lock only; no Root guard is held).
pub(crate) fn receive_view(home: &HomeSession) -> Value {
    receive_views(home).0
}

// Both readers share one receiving owner. Status may incorporate delivery but
// cannot remove closed source projections needed by a later record tick.
fn receive_views(home: &HomeSession) -> (Value, Vec<Value>) {
    let (mut current, mut recording, snapshot) = {
        let mut runtime = home.runtime.lock().unwrap();
        let (observation, received) = runtime.receive_native(&home.host);
        (received["nativeView"].clone(), runtime.recording_views(), observation["snapshot"].clone())
    };
    let access = home.access_selection.lock().unwrap().as_ref().map(|selection| (selection.owning_generation().cloned(), selection.snapshot()));
    for view in std::iter::once(&mut current).chain(recording.iter_mut()) {
        if !view.is_object() { continue; }
        // All metadata belongs to the same Host delivery cut. A later close
        // cannot overtake still-unincorporated native item/turn receipts.
        let generation = view["generation"].clone();
        for (target, source) in [("serverRequests","serverRequests"),("hostThreads","threads"),("hostTurns","conversationTurns")] {
            view[target] = json!(snapshot[source].as_array().into_iter().flatten()
                .filter(|row|row["generation"]==generation).collect::<Vec<_>>());
        }
        view["roleLimitObservations"]=home.history.lock().unwrap().child_limit_observations();
        view["custodyEvents"] = json!(snapshot["sourceCustodyEvents"].as_array().into_iter().flatten()
            .filter(|owned|owned["generation"]==generation).map(|owned|&owned["event"]).collect::<Vec<_>>());
        // Do not fill a closed source's mode from a later source/selection.
        view["conversationAccess"] = json!(access.as_ref().filter(|(generation, selection)|
            generation.as_ref()==Some(&view["generation"]) && selection["thread"]["threadId"].is_string())
            .map(|(_, selection)| vec![json!({"threadId":selection["thread"]["threadId"],"entryId":selection["selection"]["entryId"]})])
            .unwrap_or_default());
    }
    (current, recording)
}

/// The record tick for one home: receive, then record checkpoint
/// observations of its open runs. Lock order as `host_status`: runtime, then
/// Root, then a run.
pub(crate) fn tick_home(home: &HomeSession, workflows: &Mutex<WorkflowRootSession>) {
    // Reconcile only this home's retained private receipts. A genuinely late
    // role outcome is recorded even when no web view polls this home. Release
    // History before runtime/Root/run locks: host_status takes runtime then
    // History, so retaining this guard across receive_view would invert order.
    {
        let mut history = home.history.lock().unwrap();
        history.reconcile(&home.host);
    }
    let (_, recording) = receive_views(home);
    for view in recording { record_run_observations(workflows, &view); }
}

/// The record tick for every home the App holds.
pub(crate) fn tick(homes: &Mutex<HomeRouter>, workflows: &Mutex<WorkflowRootSession>) {
    let entries = homes.lock().unwrap().entries();
    for home in entries {
        tick_home(&home, workflows);
    }
}

/// The App's actual record tick also observes ended project arrivals without
/// requiring a running supplier or a web-view read.
pub(crate) fn tick_project(homes:&Mutex<HomeRouter>,workflows:&Mutex<WorkflowRootSession>,project:Option<&std::path::Path>) {
    tick(homes,workflows);
    if let Some(project)=project {if let Ok(mut root)=workflows.try_lock(){root.observe_ended_runs(project);}}
}

/// The trial tick for one home: the TT-9 reads due in the view as last
/// received (it consumes no frames), performed with no App lock held, then
/// recorded.
pub(crate) fn trial_tick_home(home: &HomeSession, workflows: &Mutex<WorkflowRootSession>) -> Vec<Value> {
    let view = home.runtime.lock().unwrap().native_view();
    let Some(home_key) = view["home"].as_str() else { return vec![] };
    let due = workflows.lock().unwrap().trial_reads_due(home_key, &view);
    if due.is_empty() {
        return vec![];
    }
    let results = trial_flows::perform_trial_reads(home, due);
    workflows.lock().unwrap().apply_trial_reads(results)
}

/// Delegation readings (NPTD §7.1, read at run time per R19-5) taken per tick
/// per home at most. The tick reads only on need: a conversation model,
/// provider and folder with no reading yet, or a *missing* reading older than
/// `DELEGATION_MISSING_REFRESH`. Try with the authoring agent and Try again
/// read their conversation at the press.
pub(crate) const DELEGATION_READS_PER_TICK: usize = 1;
/// A *missing* reading's age after which the tick reads it again (it hides
/// the press that would re-read it). Other readings are not refreshed here.
pub(crate) const DELEGATION_MISSING_REFRESH: std::time::Duration = std::time::Duration::from_secs(120);

/// The delegation reads due in one home: conversations whose model became
/// known (started, resumed or forked) and have no reading, or a stale
/// *missing* one. Holds no App lock.
pub(crate) fn delegation_tick_home(home: &HomeSession) -> usize {
    delegation_tick_home_aged(home, DELEGATION_MISSING_REFRESH)
}
pub(crate) fn delegation_tick_home_aged(home: &HomeSession, max_age: std::time::Duration) -> usize {
    let due = home.host.delegation_reads_due(DELEGATION_READS_PER_TICK, max_age);
    for (generation, thread) in &due {
        home.host.delegation_signals_read(generation, thread, json!({"kind":"app-rule","name":"delegation-availability-read"}));
    }
    due.len()
}

/// RECOVERY §3.2 CV-11…CV-15, §5 R-4 / X-3…X-5: the recovery reads due in one
/// home in its ready generation, made by the host with no App lock held; the
/// pages Codex returned are then read into the native view (which first
/// follows the ready generation) as recovered-from-supplier rows. Returns the
/// number of pages.
pub(crate) fn recovery_tick_home(home: &HomeSession) -> usize {
    let pages = home.host.recovery_reads(crate::hosting::recovery_reads::RECOVERY_READ_WAIT);
    if pages.is_empty() {
        return 0;
    }
    receive_view(home);
    let mut runtime = home.runtime.lock().unwrap();
    for page in &pages {
        runtime.receive_recovered_history(page.query.generation(), page.query.home(), page.query.method(), page.query.params(), &page.result);
    }
    pages.len()
}

/// The trial tick for every home the App holds (recovery reads, TT-9 reads,
/// then the delegation readings; all wait on Codex).
pub(crate) fn trial_tick(homes: &Mutex<HomeRouter>, workflows: &Mutex<WorkflowRootSession>) {
    let entries = homes.lock().unwrap().entries();
    for home in entries {
        recovery_tick_home(&home);
        // OA window gaps do not change CV recovery custody or the live native
        // projection. Read at most one queued target on this existing worker.
        home.host.observer_rebuild_reads(crate::hosting::recovery_reads::RECOVERY_READ_WAIT);
        home.host.continuation_context_reads(crate::hosting::recovery_reads::RECOVERY_READ_WAIT);
        trial_tick_home(&home, workflows);
        delegation_tick_home(&home);
    }
}

/// What the ticks report about themselves (H-1): each tick runs under
/// `catch_unwind`, so one failing tick neither stops the loop nor goes unseen.
static TICK_STATE: Mutex<Option<Value>> = Mutex::new(None);

/// Runs one tick named `name`; a panic is caught, counted and kept for
/// `host_status`, and the loop goes on.
pub(crate) fn guarded(name: &str, tick: impl FnOnce()) {
    let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(tick));
    let mut state = TICK_STATE.lock().unwrap_or_else(|p| p.into_inner());
    let entry = state.get_or_insert_with(|| json!({}));
    let slot = &mut entry[name];
    slot["lastTickAt"] = json!(crate::util::now_rfc3339());
    if let Err(panic) = outcome {
        let message = panic
            .downcast_ref::<&str>()
            .map(|s| (*s).to_owned())
            .or_else(|| panic.downcast_ref::<String>().cloned())
            .unwrap_or_else(|| "panic without a message".into());
        slot["failures"] = json!(slot["failures"].as_u64().unwrap_or(0) + 1);
        slot["lastFailure"] = json!({"at":crate::util::now_rfc3339(),"message":message});
    }
}

/// The ticks' state for `host_status` (read only).
pub(crate) fn tick_state() -> Value {
    let state = TICK_STATE.lock().unwrap_or_else(|p| p.into_inner());
    json!({"ticks":state.clone(),"standing":"the host's own record and trial ticks; a failed tick is counted here and the next tick runs"})
}

/// `host_status`'s workflow part: a read. It records and sends nothing.
pub(crate) fn workflow_status(workflows: &Mutex<WorkflowRootSession>, view: &Value, project_library: bool) -> Value {
    let root = workflows.lock().unwrap();
    let mut status = root.snapshot();
    // RN-3…RN-7: offers from agent messages observed live; display data only.
    status["offers"] = root.offers(view);
    // WR §3: the explicit App project can be opened as its own project library.
    status["projectLibraryAvailable"] = json!(project_library);
    // WR §4.2: trials, pre-filled messages, headers and labels (display only).
    root.decorate_status(&mut status, view);
    status
}
