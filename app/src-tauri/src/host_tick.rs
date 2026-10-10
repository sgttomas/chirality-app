//! The Rust host's own observation ticks. Under the owner's OI-008 ruling ("The
//! Rust host owns everything that writes the person's files or the App's
//! records, talks to Codex, or captures a person's act. The web view presents,
//! and sends only what the person initiates.") the host keeps its records
//! whether or not the web view polls:
//! - the record tick receives every home's native frames and lets the
//!   checkpoint recorder record what the view shows of the open runs (EXEC §2.4);
//! - the trial tick, on its own thread so that a slow Codex read never delays
//!   the record tick, makes the trial reads that are due (WR TT-9).
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
    let mut runtime = home.runtime.lock().unwrap();
    let (generation, position) = runtime.cursor();
    let observation = home.host.observe(generation, position);
    runtime.receive(&observation)["nativeView"].clone()
}

/// The record tick for one home: receive, then record checkpoint
/// observations of its open runs. Lock order as `host_status`: runtime, then
/// Root, then a run.
pub(crate) fn tick_home(home: &HomeSession, workflows: &Mutex<WorkflowRootSession>) {
    let view = receive_view(home);
    record_run_observations(workflows, &view);
}

/// The record tick for every home the App holds.
pub(crate) fn tick(homes: &Mutex<HomeRouter>, workflows: &Mutex<WorkflowRootSession>) {
    let entries = homes.lock().unwrap().entries();
    for home in entries {
        tick_home(&home, workflows);
    }
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

/// The trial tick for every home the App holds.
pub(crate) fn trial_tick(homes: &Mutex<HomeRouter>, workflows: &Mutex<WorkflowRootSession>) {
    let entries = homes.lock().unwrap().entries();
    for home in entries {
        trial_tick_home(&home, workflows);
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
