//! EXEC §2.7 / RECOVERY §4.1: DEL-02-03's REC run tag (EXEC A-2, §2.7; RECOVERY §4.1) and the
//! startup writer of RS's "App-restart interruption" limit (RS §14.1 row
//! "Relaunch with a run interrupted"; §14.3 FC-9; EXEC RE-4, AE-6).
//!
//! OI-008 placement: both run in the Rust host. The tag is written when the App
//! writer takes up `run_opened` for writing, before the write itself (a tag may
//! therefore name a run whose `run_opened` was never written; the limit writer
//! then establishes no current run); the limit writer runs from the startup closure,
//! never on a web-view request. Neither writes `run_ended`: RE-4's run-owner end
//! "interruption not recovered" is not written automatically (EXEC §2.7 / RECOVERY §4.1).
use serde_json::{json, Value};

/// The REC tag owner token of DEL-02-03's run starter (RECOVERY §4.1, EXEC §2.7).
/// REC stores the value (the run reference) without interpreting it (R17-10).
pub(crate) const RUN_TAG_OWNER: &str = "DEL-02-03";
/// RS R11 label (RS_RECORD.schema.json `evidenceLimitLabel`).
pub(crate) const RESTART_LABEL: &str = "App-restart interruption";

/// EXEC A-2: tag the run's conversation with its run reference through the REC
/// ledger of the run's own home. Returns the tag's state for the run view; a tag
/// that cannot be stored lives in the run's memory only and never blocks the run.
pub(crate) fn tag_run(
    home: &crate::runtime_session::HomeSession,
    scope: &crate::workflow_workspace::RunScope,
) -> Value {
    let class = crate::stop_records::home_class(home.class().as_str());
    home.host.tag_conversation(&scope.generation, &scope.conversation, class, RUN_TAG_OWNER, &scope.run)
}

/// WR TX-5 / SQ-END: the App-owned home class (H-acct, H-key) of a conversation the
/// record names, for an end made after a relaunch. From, in order: a REC restart
/// fact naming the conversation; the run's own REC tag; the conversation's REC
/// index rows (one home only). Otherwise the home is not established and no end
/// notice is keyed (never a guess such as the active home).
pub(crate) fn conversation_home_class(rows: &[Value], restart_events: &[Value], thread: &str, run: &str) -> Result<String, String> {
    if let Some(home) = restart_events.iter().find(|e| e["threadId"] == thread).and_then(|e| e["home"].as_str()) {
        return Ok(home.to_owned());
    }
    if let Some((home, _)) = crate::recovery::look_up(rows, RUN_TAG_OWNER, run).into_iter().find(|(_, t)| t == thread) {
        return Ok(home);
    }
    let mut homes: Vec<&str> = rows.iter().filter(|r| r["kind"] == "conversation_index" && r["threadId"] == thread).filter_map(|r| r["home"].as_str()).collect();
    homes.sort_unstable();
    homes.dedup();
    match homes.as_slice() {
        [home] => Ok((*home).to_owned()),
        [] => Err(format!("the App's recovery ledger does not say which Codex home holds conversation {thread}")),
        _ => Err(format!("the App's recovery ledger names conversation {thread} in more than one Codex home")),
    }
}

/// RS "Relaunch with a run interrupted": for each REC `app_restart_interruption`
/// fact, write one `evidence_limit` "App-restart interruption" on the run that was
/// current in that conversation at the end — the run opened last there with no
/// `run_ended`, which DEL-02-03 picks from `tags of` plus its own RS records. The
/// limit's `subjectRef` is the restart fact's eventId. Idempotent: the run's log
/// is re-read first, and a limit for the same run and fact is never written twice.
/// With no stored run tag, `run_opened.conversationRef` finds the run, and the
/// limit's detail says so. Earlier ended runs are untouched; no `run_ended` is
/// written. Returns one outcome per fact (written / already written / not written,
/// with the reason).
pub(crate) fn write_restart_limits(project: &std::path::Path, events: &[Value], rows: &[Value]) -> Vec<Value> {
    events
        .iter()
        .filter(|e| e["kind"] == "app_restart_interruption")
        .map(|event| write_one(project, event, rows))
        .collect()
}

fn write_one(project: &std::path::Path, event: &Value, rows: &[Value]) -> Value {
    let mut outcome = json!({"eventId":event["eventId"],"threadId":event["threadId"],"home":event["home"],"priorSession":event["priorSession"]});
    let finish = |mut outcome: Value, state: &str, detail: Value| {
        outcome["outcome"] = json!(state);
        outcome["detail"] = detail;
        outcome
    };
    let (Some(event_id), Some(thread)) = (event["eventId"].as_str(), event["threadId"].as_str()) else {
        return finish(outcome, "not written", json!("the restart fact names no eventId or thread"));
    };
    let (entries, limits) = crate::storage::read_all(project);
    if !limits.is_empty() {
        return finish(outcome, "not written", json!(format!("the project's run records are incomplete, so the run current in the conversation cannot be established: {limits:?}")));
    }
    let tags = crate::recovery::tags_of(rows, event["home"].as_str().unwrap_or(""), thread, RUN_TAG_OWNER);
    let opened_of = |run: &str| entries.iter().find(|e| e["kind"] == "run_opened" && e["runId"] == run);
    // (run, run_opened observation time, REC tag seq)
    let mut candidates: Vec<(String, String, Option<u64>)> = Vec::new();
    let mut tagged_unrecorded: Vec<(String, u64)> = Vec::new();
    for tag in &tags {
        let (Some(run), seq) = (tag["value"].as_str(), tag["seq"].as_u64().unwrap_or(0)) else { continue };
        match opened_of(run) {
            Some(opened) if !candidates.iter().any(|c| c.0 == run) => candidates.push((run.to_owned(), opened["observedAt"].as_str().unwrap_or("").to_owned(), Some(seq))),
            Some(_) => {}
            None => tagged_unrecorded.push((run.to_owned(), seq)),
        }
    }
    for opened in entries.iter().filter(|e| e["kind"] == "run_opened" && e["body"]["conversationRef"] == thread) {
        let Some(run) = opened["runId"].as_str() else { continue };
        if !candidates.iter().any(|c| c.0 == run) {
            candidates.push((run.to_owned(), opened["observedAt"].as_str().unwrap_or("").to_owned(), None));
        }
    }
    let current = candidates.iter().max_by(|a, b| a.1.cmp(&b.1).then(a.2.cmp(&b.2))).cloned();
    let last_seq = candidates.iter().filter_map(|c| c.2).max();
    if let Some((run, seq)) = tagged_unrecorded.iter().max_by_key(|t| t.1) {
        if last_seq.is_none_or(|s| *seq > s) {
            return finish(outcome, "not written", json!(format!("the conversation's last REC run tag names {run} (seq {seq}), which has no run_opened in the project's records; which run was current cannot be established")));
        }
    }
    let Some((run, _, seq)) = current else {
        return finish(outcome, "not written", json!("no run is recorded in this conversation (no REC run tag and no run_opened naming it)"));
    };
    outcome["run"] = json!(run);
    if entries.iter().any(|e| e["kind"] == "run_ended" && e["runId"] == run.as_str()) {
        return finish(outcome, "not written", json!(format!("the run opened last in this conversation ({run}) had ended, so no run was current at the end; earlier ended runs are untouched")));
    }
    if let Some(existing) = entries.iter().find(|e| {
        e["kind"] == "evidence_limit" && e["runId"] == run.as_str() && e["body"]["label"] == RESTART_LABEL && e["body"]["subjectRef"] == event_id
    }) {
        return finish(outcome, "already written", json!({"recordId":existing["recordId"]}));
    }
    let how = match seq {
        Some(seq) => format!("by its REC run tag (owner {RUN_TAG_OWNER}, seq {seq}) and this project's run records"),
        None if tags.is_empty() => "by this project's run_opened.conversationRef, because no REC run tag is stored for this conversation (the tag could not be stored)".to_owned(),
        None => "by this project's run_opened.conversationRef, because its REC run tag is not stored (the conversation's other run tags name earlier runs)".to_owned(),
    };
    let detail = format!(
        "App restart fact {event_id}: App session {} ended ({}) with live work in conversation {thread}. This run was current there at the end (the run opened last with no run_ended), found {how}. It stays interrupted, not ended (EXEC RE-4); nothing was written for it automatically besides this limit.",
        event["priorSession"].as_str().unwrap_or("unknown"),
        event["priorSessionEnd"].as_str().unwrap_or("unknown"),
    );
    let mut entry = match crate::records::supply::PendingRunEntry::new(
        "evidence_limit",
        json!({"label":RESTART_LABEL,"subjectRef":event_id,"detail":detail}),
        crate::util::now_rfc3339(),
    ) {
        Ok(entry) => entry,
        Err(e) => return finish(outcome, "not written", json!(format!("record identity unavailable: {e}"))),
    };
    match crate::records::supply::append_run_entry(project, &run, &mut entry) {
        Ok(written) => finish(outcome, "written", json!({"recordId":written["recordId"],"foundBy":if seq.is_some(){"REC run tag"}else{"run_opened.conversationRef (no run tag stored)"}})),
        Err(e) => finish(outcome, "not written", json!(format!("the run log could not be written: {e}"))),
    }
}

/// Startup (lib.rs setup): each home's REC recovery projection for this session,
/// then the limit writer over the explicit App project. Host-owned; the result is
/// what `workflow_reopen` shows.
pub(crate) fn startup(homes: &[std::sync::Arc<crate::runtime_session::HomeSession>], project: Option<&std::path::Path>) -> Value {
    let Some(project) = project else {
        return json!({"state":"not run","reason":"no explicit App project (CHIRALITY_WORKSPACE); no run records to write"});
    };
    let mut outcomes = Vec::new();
    let mut limits = Vec::new();
    for home in homes {
        let recovery = home.recovery_startup.lock().unwrap().snapshot();
        if recovery["state"] != "configured" {
            limits.push(json!({"home":home.class().as_str(),"limit":format!("REC recovery projection not available ({}); no restart facts read",recovery["state"])}));
            continue;
        }
        let projection = home.host.recovery_custody().snapshot();
        let events = projection["restartEvents"].as_array().cloned().unwrap_or_default();
        outcomes.extend(write_restart_limits(project, &events, &home.host.recovery_entries()));
    }
    json!({"state":"run at startup","at":crate::util::now_rfc3339(),"outcomes":outcomes,"limits":limits,
        "standing":"RS 'App-restart interruption' limits written by the host at startup; no run_ended is written automatically (RE-4's 'interruption not recovered' is not implemented, EXEC §2.7 / RECOVERY §4.1)"})
}
