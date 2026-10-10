//! The Rust host's own observation tick. Under the owner's OI-008 ruling ("The
//! Rust host owns everything that writes the person's files or the App's
//! records, talks to Codex, or captures a person's act. The web view presents,
//! and sends only what the person initiates.") the host keeps its records
//! whether or not the web view polls: each tick receives every home's native
//! frames, lets the checkpoint recorder record what the view shows of the open
//! runs (EXEC §2.4), and makes the trial reads that are due (WR TT-9).
//! `host_status` only reads (`workflow_status`).
use crate::runtime_session::{record_run_observations, trial_flows, HomeRouter, HomeSession, WorkflowRootSession};
use serde_json::{json, Value};
use std::sync::Mutex;

/// The tick's interval (the web view polls `host_status` at about the same rate).
pub(crate) const INTERVAL: std::time::Duration = std::time::Duration::from_secs(1);

/// One home's current native view: its new frames received, as `host_status`
/// receives them (runtime lock only; no Root guard is held).
pub(crate) fn receive_view(home: &HomeSession) -> Value {
    let mut runtime = home.runtime.lock().unwrap();
    let (generation, position) = runtime.cursor();
    let observation = home.host.observe(generation, position);
    runtime.receive(&observation)["nativeView"].clone()
}

/// One tick for one home: receive, record checkpoint observations of its open
/// runs, then perform and record the trial reads now due. Lock order as
/// `host_status`: runtime, then Root, then a run; no lock is held across a
/// Codex read.
pub(crate) fn tick_home(home: &HomeSession, workflows: &Mutex<WorkflowRootSession>) -> Vec<Value> {
    let view = receive_view(home);
    record_run_observations(workflows, &view);
    let Some(home_key) = view["home"].as_str() else { return vec![] };
    let due = workflows.lock().unwrap().trial_reads_due(home_key, &view);
    if due.is_empty() {
        return vec![];
    }
    let results = trial_flows::perform_trial_reads(home, due);
    workflows.lock().unwrap().apply_trial_reads(results)
}

/// One tick for every home the App holds.
pub(crate) fn tick(homes: &Mutex<HomeRouter>, workflows: &Mutex<WorkflowRootSession>) {
    let entries = homes.lock().unwrap().entries();
    for home in entries {
        tick_home(&home, workflows);
    }
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
