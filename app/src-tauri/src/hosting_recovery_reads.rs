//! Automatic recovery reads after a Codex restart (DEL-01-02 RECOVERY §3.2
//! CV-11…CV-15, CV-19, CV-22; §3.4 SR-09; §5 SQ-R R-4, SQ-X X-3…X-5).
//!
//! When this home's process is ready, every conversation whose generation
//! closed while it was loaded, or that an earlier App session left unsettled,
//! is read from Codex history on this process: `thread/read` (metadata only,
//! no `includeTurns`), then `thread/turns/list` descending, paged until the
//! turn last seen live is found. Reads carry initiator
//! `app-rule:recovery-read` (§6); they change nothing in Codex. Nothing is
//! resumed and no prompt is re-sent (HOSTING §4.4); a closed generation is
//! never read (U-R10). A failed read leaves the conversation unavailable,
//! read again on the person's retry or at the next ready; a process that
//! ends during the reads leaves it recovery-pending (CV-22).
use super::execution_custody::{RecoveredStop, RecoveryTarget};
use super::*;
use std::collections::BTreeMap;

/// The turn pages read per conversation before the turn last seen live is
/// reported not found within them (a limit, not "absent from history").
pub(crate) const RECOVERY_TURN_PAGES: usize = 20;
/// One recovery read's wait; a read that waits it out fails (CV-14).
pub(crate) const RECOVERY_READ_WAIT: Duration = Duration::from_secs(20);

/// A page Codex returned to a recovery read, for the native view.
pub(crate) struct RecoveryPage { pub(crate) query: HistoryQuery, pub(crate) result: Value }

impl Host {
    /// One recovery pass in the ready generation (none when not ready or
    /// nothing is due; an idle pass takes no App writer). Returns the pages
    /// Codex returned, in order. Once a read gets no answer within `wait`,
    /// the pass reads nothing more: the conversations left are unavailable
    /// with that reason, so a Codex that stops answering holds the tick up
    /// for one wait, not one per conversation.
    pub(crate) fn recovery_reads(&self, wait: Duration) -> Vec<RecoveryPage> {
        {
            let i = self.inner.0.lock().unwrap();
            if i.state != "ready" || !i.execution_custody.recovery_due(&i.generation) { return Vec::new(); }
        }
        let (generation, targets) = {
            let _writer = self.recovery_writer.lock().unwrap();
            let mut i = self.inner.0.lock().unwrap();
            if i.state != "ready" || crate::recovery::generation_ref(&i.generation).is_err() { return Vec::new(); }
            let generation = i.generation.clone();
            let rows = Self::recovery_history(&i);
            let session = i.app_session.clone();
            i.execution_custody.adopt(&session, &generation, &rows);
            let targets = i.execution_custody.begin_recovery(&generation, &now_rfc3339());
            if targets.is_empty() { return Vec::new(); }
            Self::persist_recovery(&mut i);
            drop(i);
            self.drain_recovery_owned();
            (generation, targets)
        };
        let mut threads: BTreeMap<String, Vec<RecoveryTarget>> = BTreeMap::new();
        for target in targets { threads.entry(target.key.1.clone()).or_default().push(target); }
        let mut pages = Vec::new();
        let mut unanswered: Option<String> = None;
        for (thread, targets) in threads {
            let wanted: Vec<&str> = targets.iter().filter_map(|t| t.turn.as_deref()).collect();
            let read = match &unanswered {
                Some(reason) => Err(format!("not read in this pass: Codex did not answer an earlier recovery read ({reason})")),
                None => {
                    let mut no_answer = false;
                    let read = self.recovery_read(&generation, &thread, &wanted, wait, &mut pages, &mut no_answer);
                    if no_answer { unanswered = read.as_ref().err().cloned(); }
                    read
                }
            };
            {
                let _writer = self.recovery_writer.lock().unwrap();
                let mut i = self.inner.0.lock().unwrap();
                let at = now_rfc3339();
                for target in &targets {
                    if !i.execution_custody.recovering_in(&target.key, &generation) { continue; }
                    match &read {
                        Err(reason) => i.execution_custody.recovery_failed(&target.key, &generation, reason, &at),
                        Ok(statuses) => {
                            let status = target.turn.as_deref().and_then(|t| statuses.get(t)).map(String::as_str);
                            let stop = target.turn.as_deref().and_then(|t| Self::stop_request_recovered(&mut i, &target.key.0, &thread, t, status));
                            i.execution_custody.recovered(&target.key, &generation, status, stop, &at);
                        }
                    }
                }
                Self::persist_recovery(&mut i);
                drop(i);
                self.drain_recovery_owned();
            }
        }
        pages
    }
    /// The reads for one conversation: each wanted turn's status as history
    /// reports it (a turn missing from the map is not in history), or why
    /// the reads failed.
    fn recovery_read(&self, generation: &Value, thread: &str, wanted: &[&str], wait: Duration, pages: &mut Vec<RecoveryPage>, no_answer: &mut bool) -> Result<BTreeMap<String, String>, String> {
        let metadata = self.recovery_page(generation, "thread/read", json!({"threadId":thread,"includeTurns":false}), wait, pages, no_answer)?;
        if metadata["thread"]["id"] != thread { return Err("thread/read returned another conversation".into()); }
        let mut statuses = BTreeMap::new();
        let mut cursor: Option<String> = None;
        for _ in 0..RECOVERY_TURN_PAGES {
            let mut params = json!({"threadId":thread,"sortDirection":"desc","itemsView":"summary"});
            if let Some(c) = &cursor { params["cursor"] = json!(c); }
            let page = self.recovery_page(generation, "thread/turns/list", params, wait, pages, no_answer)?;
            for turn in page["data"].as_array().into_iter().flatten() {
                if let (Some(id), Some(status)) = (turn["id"].as_str(), turn["status"].as_str()) { statuses.entry(id.to_owned()).or_insert_with(|| status.to_owned()); }
            }
            if wanted.iter().all(|t| statuses.contains_key(*t)) { return Ok(statuses); }
            match page["nextCursor"].as_str().filter(|c| !c.is_empty()) {
                Some(next) if cursor.as_deref() != Some(next) => cursor = Some(next.to_owned()),
                Some(_) => return Err("thread/turns/list repeated a page cursor".into()),
                None => return Ok(statuses),
            }
        }
        Err(format!("the turn last seen live was not found in the first {RECOVERY_TURN_PAGES} pages of Codex history"))
    }
    /// One read and its result; `no_answer` is set when Codex sent nothing back.
    fn recovery_page(&self, generation: &Value, method: &str, params: Value, wait: Duration, pages: &mut Vec<RecoveryPage>, no_answer: &mut bool) -> Result<Value, String> {
        let home = generation["home"].as_str().ok_or("generation home required")?;
        let query = crate::native_history::workspace_read(home, generation, method, params)?;
        let dispatch = self.history_dispatch_by(&query, json!({"kind":"app-rule","name":"recovery-read"}))?;
        let evidence = self.history_wait(&dispatch, wait)?;
        let response = &evidence["response"];
        *no_answer = response.is_null();
        if let Some(error) = response.get("error") {
            return Err(format!("{method} answered with an error: {}", error["message"].as_str().map(str::to_owned).unwrap_or_else(|| error.to_string())));
        }
        let result = response.get("result").filter(|r| r.is_object()).cloned().ok_or_else(|| format!("{method} returned no result (outcome {})", evidence["outcome"]))?;
        crate::native_history::validate_read_response(method, &result)?;
        pages.push(RecoveryPage { query, result: result.clone() });
        Ok(result)
    }
    /// SR-09 for the lost turn's stop request, of this process or (after a
    /// relaunch) of the ledger, when history reports a final status. Its
    /// cause and identity go on `turn_outcome` whenever it was sent.
    fn stop_request_recovered(i: &mut Inner, generation: &str, thread: &str, turn: &str, status: Option<&str>) -> Option<RecoveredStop> {
        let mine = |r: &crate::stop_records::StopRequest| r.record()["generation"] == generation && r.record()["threadId"] == thread && r.record()["turnId"] == turn;
        let id = match i.stop_requests.iter().rev().find(|r| mine(r) && r.record()["send"] == "sent") {
            Some(r) => r.id().to_owned(),
            None => {
                let record = {
                    let mut index = i.stop_ledger_index.lock().unwrap();
                    index.update(i.recovery_snapshot.as_ref());
                    index.latest_for(generation, thread, turn).cloned()
                }.filter(|r| r["send"] == "sent")?;
                let request = crate::stop_records::StopRequest::from_record(&record).ok()?;
                let id = request.id().to_owned();
                i.stop_requests.push(request);
                id
            }
        };
        let record = i.stop_requests.iter().find(|r| r.id() == id)?.record().clone();
        // Its generation is closed: an earlier session's request with no SR-08
        // recorded gets it first, then SR-09 for a final status.
        Self::stop_request_update(i, &id, |r| r.generation_closed());
        if let Some(status) = status { Self::stop_request_update(i, &id, |r| r.recovered(status)); }
        Some(RecoveredStop { cause: record["cause"].as_str().unwrap_or_default().to_owned(), id })
    }
    /// CV-15 by the person: the unavailable conversation is read again by the
    /// next recovery pass in a ready process (at once when Codex is ready,
    /// otherwise when it is next ready). Refused when it is not unavailable.
    pub(crate) fn recovery_retry(&self, thread: &str) -> Result<(), String> {
        let mut i = self.inner.0.lock().unwrap();
        if i.execution_custody.request_retry(thread) == 0 {
            return Err(format!("conversation {thread} is not unavailable here; nothing to read again"));
        }
        Ok(())
    }
    fn recovery_history(i: &Inner) -> Vec<Value> {
        let mut history = i.recovery_snapshot.as_ref().and_then(|s| s["entries"].as_array()).cloned().unwrap_or_default();
        history.extend(i.pending_recovery.facts.lock().unwrap().iter().cloned());
        history
    }
    /// Queues the recovery states' ledger rows, validated like every pointer row.
    pub(super) fn persist_recovery(i: &mut Inner) {
        let history = Self::recovery_history(i);
        let session = i.app_session.clone();
        for row in i.execution_custody.recovery_rows(&session, &history) {
            match RecoveryLedger::validate_pointer_entry(&row) {
                Ok(()) if i.recovery.is_some() => i.pending_recovery.facts.lock().unwrap().push_back(row),
                Ok(()) => i.recovery_error = Some("recovery state is memory-only; App ledger unavailable".into()),
                Err(error) => { i.recovery_error = Some(error.clone()); i.recovery_projection_errors.push(json!({"generation":i.generation,"limit":error,"standing":"recovery state row refused; no native payload copied"})); }
            }
        }
    }
}

#[cfg(test)]
#[path = "hosting_recovery_reads_tests.rs"]
mod tests;
