//! Disposable prior-work pages owned by an actual admitted Continue receipt.
//! Separate from CV recovery, observer replay, native projections and recording.
use super::*;
use crate::native_history::{Direction, NativeHistory};
use std::collections::BTreeMap;

const TURN_LIMIT: u32 = 20;
const ITEM_LIMIT: u32 = 50;

#[derive(Clone)]
enum Read {
    Turns {
        cursor: Option<String>,
        direction: Direction,
        select_latest: bool,
    },
    Items {
        turn: String,
        cursor: Option<String>,
        direction: Direction,
    },
}
#[derive(Clone)]
struct Work {
    read: Read,
    query: HistoryQuery,
    automatic: bool,
}

pub(super) struct Context {
    admission: HistoryDispatch,
    admission_selection_epoch: u64,
    thread: String,
    history: NativeHistory,
    revision: u64,
    work: Option<Work>,
    running: bool,
    failed: Option<Read>,
    selected_turn: Option<String>,
    state: &'static str,
    error: Option<String>,
    receipts: BTreeMap<String, Value>,
}
struct Job {
    thread: String,
    admission_ref: String,
    generation: Value,
    revision: u64,
    work: Work,
}

impl Context {
    pub(super) fn admitted(
        admission: HistoryDispatch,
        epoch: u64,
        thread: &str,
    ) -> Result<Self, String> {
        let history = NativeHistory::for_admitted_thread(
            admission.query.home(),
            admission.query.generation().clone(),
            thread,
        )?;
        let mut context = Self {
            admission,
            admission_selection_epoch: epoch,
            thread: thread.into(),
            history,
            revision: 1,
            work: None,
            running: false,
            failed: None,
            selected_turn: None,
            state: "queued",
            error: None,
            receipts: BTreeMap::new(),
        };
        context.queue(
            Read::Turns {
                cursor: None,
                direction: Direction::Desc,
                select_latest: true,
            },
            true,
        )?;
        Ok(context)
    }
    fn query(&mut self, read: &Read) -> Result<HistoryQuery, String> {
        match read {
            Read::Turns {
                cursor, direction, ..
            } => self
                .history
                .turns_page_limit(cursor.as_deref(), *direction, Some(TURN_LIMIT)),
            Read::Items {
                turn,
                cursor,
                direction,
            } => {
                self.history
                    .items_page_limit(turn, cursor.as_deref(), *direction, Some(ITEM_LIMIT))
            }
        }
    }
    fn queue(&mut self, read: Read, automatic: bool) -> Result<(), String> {
        let query = self.query(&read)?;
        if let Read::Items { turn, .. } = &read {
            self.selected_turn = Some(turn.clone());
        }
        self.work = Some(Work {
            query,
            read,
            automatic,
        });
        self.running = false;
        self.error = None;
        self.failed = None;
        self.state = "queued";
        Ok(())
    }
    fn snapshot(&self, current: bool) -> Value {
        let mut history = self.history.snapshot();
        history["selectionEpoch"] = json!(self.history.selection_epoch());
        json!({"home":self.admission.query.home(),"generation":self.admission.query.generation(),
            "threadId":self.thread,"resumeRequestRef":self.admission.source.request_ref,
            "admissionSelectionEpoch":self.admission_selection_epoch,"revision":self.revision,
            "sourceCurrent":current,"state":if current{self.state}else{"observation-ended"},"error":self.error,
            "selectedTurnId":self.selected_turn,"pageLimits":{"turns":TURN_LIMIT,"items":ITEM_LIMIT},
            "partial":true,"fullHistoryRebuilt":false,"durableNativeData":false,
            "history":history,"receipts":self.receipts.values().collect::<Vec<_>>(),
            "standing":"Read-only native pages from this admitted conversation; no current execution, act, role, CCE, return, review or integration authority."})
    }
}

impl Host {
    fn continuation_context_current(i: &Inner, context: &Context) -> bool {
        let admission = &context.admission;
        let q = &admission.query;
        if i.state != "ready"
            || i.generation != *q.generation()
            || i.server_requests.is_closed(q.generation())
        {
            return false;
        }
        if !i.threads.iter().any(|row| {
            row["generation"] == *q.generation()
                && row["threadId"] == context.thread
                && row["nativeResumeObserved"] == true
                && row["resumeRequestRef"] == admission.source.request_ref
        }) {
            return false;
        }
        i.source_requests
            .get(&admission.source.request_id().to_string())
            .is_some_and(|e| {
                e.request.frame == admission.source.frame
                    && e.request.generation == *q.generation()
                    && e.request.request_ref == admission.source.request_ref
                    && e.written
                    && !e.write_attempt_in_progress
                    && e.write_error.is_none()
                    && e.source_limit.is_none()
                    && e.response_position.is_some()
                    && e.source_pipe
                        .is_some_and(|(epoch, _)| epoch == i.attachment_pipe_epoch)
                    && e.response.as_ref().is_some_and(|r| {
                        r.get("id") == Some(admission.source.request_id())
                            && r.get("method").is_none()
                            && r.get("error").is_none()
                            && r["result"]["thread"]["id"] == context.thread
                    })
            })
    }
    pub(super) fn continuation_contexts_snapshot(i: &Inner) -> Vec<Value> {
        i.continuation_contexts
            .values()
            .map(|context| context.snapshot(Self::continuation_context_current(i, context)))
            .collect()
    }
    /// Queue a person-requested read only. The JSON coordinates select an
    /// already privately admitted owner; they cannot manufacture one.
    #[allow(clippy::too_many_arguments)]
    pub(crate) fn continuation_context_action(
        &self,
        generation: &Value,
        thread: &str,
        resume_ref: &str,
        revision: u64,
        action: &str,
        cursor: Option<&str>,
        direction: Direction,
        turn: Option<&str>,
    ) -> Result<Value, String> {
        let mut i = self.inner.0.lock().unwrap();
        let context = i
            .continuation_contexts
            .get(thread)
            .ok_or("No admitted continuation context for this conversation")?;
        if context.admission.query.generation() != generation
            || context.admission.source.request_ref != resume_ref
            || context.revision != revision
            || !Self::continuation_context_current(&i, context)
        {
            return Err(
                "Continuation source, admission or selected page changed; refresh before reading"
                    .into(),
            );
        }
        let read = match action {
            "turns" if turn.is_none() => Read::Turns {
                cursor: cursor.map(str::to_owned),
                direction,
                select_latest: false,
            },
            "items" => Read::Items {
                turn: turn
                    .filter(|id| !id.is_empty())
                    .ok_or("Select a received turn")?
                    .into(),
                cursor: cursor.map(str::to_owned),
                direction,
            },
            "retry" if cursor.is_none() && turn.is_none() => context
                .failed
                .clone()
                .ok_or("There is no failed context read to retry")?,
            _ => return Err("Unsupported continuation context read".into()),
        };
        // Validate before superseding a useful in-flight request. Its native
        // factory also validates known turns and received cursor/direction.
        let context = i.continuation_contexts.get_mut(thread).unwrap();
        let query = context.query(&read)?;
        if let Some(old) = &context.work {
            context.history.supersede_read(&old.query);
        }
        context.revision = context
            .revision
            .checked_add(1)
            .ok_or("Continuation revision exhausted")?;
        if let Read::Items { turn, .. } = &read {
            context.selected_turn = Some(turn.clone());
        }
        context.work = Some(Work {
            query,
            read,
            automatic: false,
        });
        context.running = false;
        context.failed = None;
        context.error = None;
        context.state = "queued";
        Ok(context.snapshot(true))
    }
    fn continuation_job_current(i: &Inner, job: &Job) -> bool {
        i.continuation_contexts
            .get(&job.thread)
            .is_some_and(|context| {
                context.revision == job.revision
                    && context.admission.source.request_ref == job.admission_ref
                    && context.admission.query.generation() == &job.generation
                    && context
                        .work
                        .as_ref()
                        .is_some_and(|work| work.query == job.work.query)
                    && Self::continuation_context_current(i, context)
            })
    }
    fn continuation_begin(&self) -> Option<Job> {
        let mut i = self.inner.0.lock().unwrap();
        let thread = i
            .continuation_contexts
            .iter()
            .find(|(_, context)| {
                context.work.is_some()
                    && !context.running
                    && Self::continuation_context_current(&i, context)
            })?
            .0
            .clone();
        let context = i.continuation_contexts.get_mut(&thread).unwrap();
        context.running = true;
        context.state = "reading";
        Some(Job {
            thread,
            admission_ref: context.admission.source.request_ref.clone(),
            generation: context.admission.query.generation().clone(),
            revision: context.revision,
            work: context.work.clone().unwrap(),
        })
    }
    fn continuation_receipt(dispatch: &HistoryDispatch, e: &Value, position: Option<u64>) -> Value {
        json!({"query":dispatch.query,"requestRef":dispatch.source.request_ref,"generation":dispatch.query.generation(),"home":dispatch.query.home(),
            "requestIdentity":dispatch.source.request_id(),"sourceCurrent":e["sourceCurrent"],
            "writeResult":e["writeResult"],"outcome":e["outcome"],"receiptPosition":position,"observedAt":now_rfc3339()})
    }
    /// Accept only the actual retained response to this Host's own complete
    /// write on its original pipe, never a renderer-provided result object.
    fn continuation_response(
        &self,
        i: &Inner,
        dispatch: &HistoryDispatch,
    ) -> Result<Value, String> {
        let source = dispatch
            .source
            .source
            .upgrade()
            .ok_or("Context read Host unavailable")?;
        if !Arc::ptr_eq(&source, &self.inner) {
            return Err("Context read belongs to another Host".into());
        }
        let e = i
            .source_requests
            .get(&dispatch.source.request_id().to_string())
            .ok_or("Context source record unavailable")?;
        if e.request.frame != dispatch.source.frame
            || e.request.request_ref != dispatch.source.request_ref
            || e.request.generation != *dispatch.query.generation()
            || dispatch.source.frame["method"] != dispatch.query.method()
            || dispatch.source.frame["params"] != *dispatch.query.params()
            || !e.written
            || e.write_attempt_in_progress
            || e.write_error.is_some()
            || e.source_limit.is_some()
            || e.attempt_position.is_none()
            || e.auth_projection
        {
            return Err("Context read has no original complete native write".into());
        }
        let (epoch, identity) = e
            .source_pipe
            .ok_or("Context read original pipe unavailable")?;
        if epoch != i.attachment_pipe_epoch {
            return Err("Context read pipe epoch changed".into());
        }
        let stdin = self.stdin.lock().unwrap();
        if stdin
            .as_ref()
            .map(Self::pipe_identity)
            .transpose()?
            .as_ref()
            != Some(&identity)
        {
            return Err("Context read original pipe changed".into());
        }
        let response = e
            .response
            .as_ref()
            .ok_or("Context read result not observed before waiting ended")?;
        if response.get("id") != Some(dispatch.source.request_id())
            || response.get("method").is_some()
            || e.response_position.is_none()
        {
            return Err("Context read response is not the original correlated receipt".into());
        }
        Ok(response.clone())
    }
    fn continuation_fail(&self, job: &Job, reason: String) {
        let mut i = self.inner.0.lock().unwrap();
        if !Self::continuation_job_current(&i, job) {
            return;
        }
        let context = i.continuation_contexts.get_mut(&job.thread).unwrap();
        let _ = context.history.read_unavailable(&job.work.query, &reason);
        context.failed = Some(job.work.read.clone());
        context.error = Some(reason);
        context.work = None;
        context.running = false;
        context.state = "unavailable";
    }
    fn continuation_abandon(&self, job: &Job) {
        let mut i = self.inner.0.lock().unwrap();
        if let Some(context) = i
            .continuation_contexts
            .get_mut(&job.thread)
            .filter(|context| {
                context.revision == job.revision
                    && context.admission.source.request_ref == job.admission_ref
                    && context
                        .work
                        .as_ref()
                        .is_some_and(|work| work.query == job.work.query)
            })
        {
            let reason =
                "The original conversation source changed or stopped during the context read";
            let _ = context.history.read_unavailable(&job.work.query, reason);
            context.failed = Some(job.work.read.clone());
            context.error = Some(reason.into());
            context.running = false;
            context.work = None;
            context.state = "unavailable";
        }
    }
    /// At most one context's bounded initial pair, or one explicitly requested
    /// page, per worker pass. No App/context lock is held through native IO.
    pub(crate) fn continuation_context_reads(&self, wait: Duration) -> usize {
        let Some(mut job) = self.continuation_begin() else {
            return 0;
        };
        let mut read_count = 0;
        loop {
            let current = {
                let i = self.inner.0.lock().unwrap();
                Self::continuation_job_current(&i, &job)
            };
            if !current {
                self.continuation_abandon(&job);
                return read_count;
            }
            let initiator = if job.work.automatic {
                json!({"kind":"app-rule","name":"continuation-context-read"})
            } else {
                json!({"kind":"person-directed"})
            };
            let dispatch = match self.history_dispatch_by(&job.work.query, initiator) {
                Ok(dispatch) => dispatch,
                Err(error) => {
                    self.continuation_fail(&job, error);
                    return read_count;
                }
            };
            let evidence = self
                .history_wait(&dispatch, wait)
                .unwrap_or_else(|_| dispatch.evidence());
            read_count += 1;
            let next = {
                let mut i = self.inner.0.lock().unwrap();
                if !Self::continuation_job_current(&i, &job) {
                    drop(i);
                    self.continuation_abandon(&job);
                    return read_count;
                }
                let response = self.continuation_response(&i, &dispatch);
                let position = i
                    .source_requests
                    .get(&dispatch.source.request_id().to_string())
                    .and_then(|e| e.response_position);
                let context = i.continuation_contexts.get_mut(&job.thread).unwrap();
                context.receipts.insert(
                    job.work.query.method().into(),
                    Self::continuation_receipt(&dispatch, &evidence, position),
                );
                let response = match response {
                    Ok(response) => response,
                    Err(error) => {
                        drop(i);
                        self.continuation_fail(&job, error);
                        return read_count;
                    }
                };
                if response["result"]["data"].as_array().is_some_and(|data| {
                    data.len() as u64 > job.work.query.params()["limit"].as_u64().unwrap_or(0)
                }) {
                    drop(i);
                    self.continuation_fail(
                        &job,
                        "Codex returned more entries than the requested context page limit".into(),
                    );
                    return read_count;
                }
                let accepted = if let Some(error) = response.get("error") {
                    context
                        .history
                        .receive_error(
                            &job.work.query,
                            dispatch.query.home(),
                            &job.generation,
                            error,
                        )
                        .and_then(|_| {
                            Err(format!(
                                "Codex history read failed: {}",
                                error["message"].as_str().unwrap_or("native error")
                            ))
                        })
                } else if let Some(result) = response.get("result") {
                    context.history.receive(
                        &job.work.query,
                        dispatch.query.home(),
                        &job.generation,
                        result,
                    )
                } else {
                    Err("Context native response has no result".into())
                };
                if let Err(error) = accepted {
                    drop(i);
                    self.continuation_fail(&job, error);
                    return read_count;
                }
                let page = &response["result"];
                if matches!(
                    job.work.read,
                    Read::Turns {
                        select_latest: true,
                        ..
                    }
                ) {
                    if let Some(turn) = page["data"]
                        .as_array()
                        .and_then(|turns| turns.first())
                        .and_then(|turn| turn["id"].as_str())
                    {
                        let read = Read::Items {
                            turn: turn.into(),
                            cursor: None,
                            direction: Direction::Desc,
                        };
                        if let Err(error) = context.queue(read, true) {
                            drop(i);
                            self.continuation_fail(&job, error);
                            return read_count;
                        }
                        context.running = true;
                        context.state = "reading";
                        Some(Job {
                            work: context.work.clone().unwrap(),
                            ..job
                        })
                    } else {
                        context.work = None;
                        context.running = false;
                        context.state = "empty";
                        None
                    }
                } else {
                    context.work = None;
                    context.running = false;
                    context.state = if page["data"].as_array().is_some_and(Vec::is_empty) {
                        "empty"
                    } else {
                        "partial"
                    };
                    None
                }
            };
            match next {
                Some(next) => job = next,
                None => return read_count,
            }
        }
    }
}

#[cfg(test)]
#[path = "hosting_continuation_context_tests.rs"]
mod tests;
