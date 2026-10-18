//! Memory-only OA-02 history reads for a public observer's replay gap.
//!
//! The owning Host queues actual source/target coordinates. Only the background
//! reader dispatches RPCs; queue/status reads neither contact Codex nor touch
//! execution custody, the recovery ledger, HistorySession or native projections.
//! Results are a partial read view, never current operational or recording input.

use super::*;
use std::collections::BTreeMap;

#[derive(Default)]
pub(super) struct ObserverRebuild {
    generation: Value,
    requested_cut: Option<u64>,
    requested_at: Option<String>,
    no_known_targets: bool,
    targets: BTreeMap<String, Target>,
    last_started: Option<String>,
    source_activity_position: u64,
}

struct Target {
    cut: u64,
    requested_at: String,
    running: Option<Running>,
    result: Option<Value>,
    last_attempt: Option<Attempt>,
}

#[derive(Clone, Copy)]
struct Attempt {
    cut: u64,
    source_activity_position: u64,
}

struct Running {
    key: Arc<()>,
    cut: u64,
    started_at: String,
    source_activity_position: u64,
}

// An original in-process attempt, not reconstructed from its public status.
struct Job {
    key: Arc<()>,
    generation: Value,
    thread: String,
    cut: u64,
    requested_at: String,
    started_at: String,
    source_activity_position: u64,
}

#[derive(Default)]
struct Reading {
    receipts: Vec<Value>,
    metadata: Option<Value>,
    turns: Option<Value>,
}

enum Failure {
    Unavailable(&'static str),
    Superseded,
}

impl ObserverRebuild {
    pub(super) fn reset(&mut self, generation: &Value) {
        if self.generation != *generation {
            *self = Self {
                generation: generation.clone(),
                ..Self::default()
            };
        }
    }

    /// The Host calls this only after current/open primary-receipt admission,
    /// excluding original correlated responses to this reader's own requests.
    /// Incoming labels and public cursor positions never supply this value.
    pub(super) fn record_source_activity(&mut self, generation: &Value, position: u64) {
        if self.generation == *generation {
            self.source_activity_position = self.source_activity_position.max(position);
        }
    }

    fn eligible(&self, target: &Target) -> bool {
        target.last_attempt.is_none_or(|attempt| {
            target.cut > attempt.cut
                && self.source_activity_position > attempt.source_activity_position
        })
    }

    /// Called with actual current Host coordinates, never a requested future
    /// cursor. `cut` is omitted-through, not the moving receipt high-water.
    pub(super) fn request(&mut self, generation: &Value, cut: u64, targets: Vec<String>) {
        self.reset(generation);
        if self.requested_cut.is_none_or(|previous| cut > previous) {
            self.requested_cut = Some(cut);
            self.requested_at = Some(now_rfc3339());
        }
        let targets: std::collections::BTreeSet<_> =
            targets.into_iter().filter(|id| !id.is_empty()).collect();
        self.no_known_targets = targets.is_empty();
        for thread in targets {
            match self.targets.get_mut(&thread) {
                Some(target) if cut > target.cut => {
                    target.cut = cut;
                    target.requested_at = now_rfc3339();
                }
                Some(_) => (), // Includes completed failures: no polling retry.
                None => {
                    self.targets.insert(
                        thread,
                        Target {
                            cut,
                            requested_at: now_rfc3339(),
                            running: None,
                            result: None,
                            last_attempt: None,
                        },
                    );
                }
            }
        }
    }

    fn begin(&mut self, generation: &Value) -> Option<Job> {
        if self.generation != *generation
            || self.targets.values().any(|target| target.running.is_some())
        {
            return None;
        }
        // Round-robin among pending target IDs. A continually advancing cut
        // on the first sorted thread must not starve an unread later thread.
        let pending: Vec<_> = self
            .targets
            .iter()
            .filter(|(_, target)| self.eligible(target))
            .map(|(thread, _)| thread.clone())
            .collect();
        let thread = pending
            .iter()
            .find(|thread| self.last_started.as_ref().is_none_or(|last| *thread > last))
            .or_else(|| pending.first())?
            .clone();
        self.last_started = Some(thread.clone());
        let target = self.targets.get_mut(&thread).unwrap();
        let source_activity_position = self.source_activity_position;
        target.last_attempt = Some(Attempt {
            cut: target.cut,
            source_activity_position,
        });
        let key = Arc::new(());
        let started_at = now_rfc3339();
        target.running = Some(Running {
            key: Arc::clone(&key),
            cut: target.cut,
            started_at: started_at.clone(),
            source_activity_position,
        });
        Some(Job {
            key,
            generation: generation.clone(),
            thread,
            cut: target.cut,
            requested_at: target.requested_at.clone(),
            started_at,
            source_activity_position,
        })
    }

    fn finish(&mut self, job: &Job, mut result: Value) -> bool {
        if self.generation != job.generation {
            return false;
        }
        let Some(target) = self.targets.get_mut(&job.thread) else {
            return false;
        };
        if !target
            .running
            .as_ref()
            .is_some_and(|running| Arc::ptr_eq(&running.key, &job.key))
        {
            return false;
        }
        if target.cut > job.cut && self.source_activity_position > job.source_activity_position {
            result["attemptStatus"] = result["status"].clone();
            result["status"] = json!("superseded");
            result["supersededByCut"] = json!(target.cut);
        }
        target.result = Some(result);
        target.running = None;
        true
    }

    pub(super) fn snapshot(&self) -> Value {
        let targets: Vec<_> = self.targets.iter().map(|(thread, target)| {
            let suppressed = target.last_attempt.filter(|attempt| target.cut > attempt.cut
                && self.source_activity_position == attempt.source_activity_position);
            let mut view = if let Some(result) = target.result.as_ref().filter(|_| target.running.is_none() && !self.eligible(target)) {
                result.clone()
            } else {
            let reading = target.running.as_ref().filter(|running| running.cut == target.cut
                || self.source_activity_position == running.source_activity_position);
            json!({"threadId":thread,"cut":reading.map_or(target.cut, |running| running.cut),"status":if reading.is_some(){"reading"}else{"queued"},
                "requestedAt":target.requested_at,"startedAt":target.running.as_ref().map(|running| &running.started_at),
                "readAt":null,"completedAt":null,"metadata":null,"turns":null,"methodsRead":[],"receipts":[],"limit":null,
                "inFlightCut":target.running.as_ref().map(|running| running.cut),"previousAttempt":target.result,
                "sourceActivityPosition":reading.map(|running| running.source_activity_position),
                "fullHistoryRebuilt":false,"itemsRequested":false})
            };
            view["requestedCut"] = json!(target.cut);
            view["suppressedCut"] = json!(suppressed.map(|_| target.cut));
            view["suppressionReason"] = json!(suppressed.map(|_| "no-new-non-observer-source-activity"));
            view["waitingForSourceActivity"] = json!(suppressed.is_some());
            view
        }).collect();
        let status = if self.no_known_targets {
            "unavailable"
        } else if targets.iter().any(|target| target["status"] == "reading") {
            "reading"
        } else if targets.iter().any(|target| target["status"] == "queued") {
            "queued"
        } else if targets.iter().any(|target| target["status"] == "partial") {
            "partial"
        } else if !targets.is_empty()
            && targets
                .iter()
                .all(|target| target["status"] == "superseded")
        {
            "superseded"
        } else {
            "unavailable"
        };
        json!({"generation":self.generation,"requestedCut":self.requested_cut,"requestedAt":self.requested_at,
            "sourceActivityPosition":self.source_activity_position,
            "status":status,"targets":targets,"noKnownTargets":self.no_known_targets,
            "limit":if self.no_known_targets {Some("no-known-loaded-threads")} else if self.requested_cut.is_none() {Some("not-requested")} else {None},
            "fullHistoryRebuilt":false,"itemsRequested":false,"durableNativeData":false,
            "standing":"Memory-only partial supplier-history reads for a public replay gap; not current control, execution-custody recovery, recorded arrival, resume or complete history."})
    }
}

impl Job {
    fn result(&self, reading: Reading, failure: Option<Failure>) -> Value {
        let (status, limit) = match failure {
            None => ("partial", None),
            Some(Failure::Unavailable(limit)) => ("unavailable", Some(limit)),
            Some(Failure::Superseded) => ("superseded", Some("original-source-no-longer-ready")),
        };
        let methods: Vec<_> = reading
            .receipts
            .iter()
            .map(|receipt| receipt["method"].clone())
            .collect();
        let cursor = match reading
            .turns
            .as_ref()
            .and_then(|turns| turns.get("nextCursor"))
        {
            None => json!({"status":"not-reported"}),
            Some(Value::Null) => json!({"status":"exhausted"}),
            Some(value) => json!({"status":"reported","value":value}),
        };
        json!({"generation":self.generation,"threadId":self.thread,"cut":self.cut,"status":status,
            "sourceActivityPosition":self.source_activity_position,
            "requestedAt":self.requested_at,"startedAt":self.started_at,"readAt":reading.receipts.last().map(|receipt| &receipt["observedAt"]),
            "completedAt":now_rfc3339(),"methodsRead":methods,"receipts":reading.receipts,
            "metadata":reading.metadata,"turns":reading.turns,"turnCursor":cursor,"limit":limit,
            "fullHistoryRebuilt":false,"itemsRequested":false,"allItemsRead":false,
            "extent":"Metadata and the first descending turn-summary page only. Earlier turns and item pages are not requested; unavailable checklist revisions are not reconstructed.",
            "standing":"Read from supplier history; separate from the canonical live native projection and recording input."})
    }
}

impl Host {
    /// Only original current pending-client registration can identify one of
    /// this reader's responses. Native server ID space and incoming labels are
    /// independent and cannot suppress an actual source-activity observation.
    pub(super) fn observer_rebuild_own_response(
        inner: &Inner,
        generation: &Value,
        frame: &Value,
        class: &str,
    ) -> bool {
        if class != "response" || frame.get("method").is_some() {
            return false;
        }
        let Some(id) = frame.get("id") else {
            return false;
        };
        let key = id.to_string();
        let Some(source) = inner.source_requests.get(&key) else {
            return false;
        };
        source.request.generation == *generation
            && source.request.request_id() == id
            && inner
                .pending
                .get(&key)
                .is_some_and(|(index, _)| *index == source.index)
            && source.observation_base["initiator"]
                == json!({"kind":"app-rule","name":"observer-history-read"})
    }

    /// Perform at most one queued target attempt, outside source/state locks.
    /// Returns selected target attempts (0 or 1), not success or page counts.
    /// Same-cut failures are not retried by later ticks.
    pub(crate) fn observer_rebuild_reads(&self, wait: Duration) -> usize {
        let job = {
            let mut inner = self.inner.0.lock().unwrap();
            if inner.state != "ready" || inner.server_requests.is_closed(&inner.generation) {
                return 0;
            }
            let generation = inner.generation.clone();
            inner.observer_rebuild.begin(&generation)
        };
        let Some(job) = job else {
            return 0;
        };
        let mut reading = Reading::default();
        let outcome = (|| {
            let metadata = self.observer_rebuild_page(
                &job,
                "thread/read",
                json!({"threadId":job.thread,"includeTurns":false}),
                wait,
                &mut reading,
            )?;
            reading.metadata = Some(metadata);
            let turns = self.observer_rebuild_page(
                &job,
                "thread/turns/list",
                json!({"threadId":job.thread,"sortDirection":"desc","itemsView":"summary"}),
                wait,
                &mut reading,
            )?;
            reading.turns = Some(turns);
            self.observer_rebuild_source(&job)
        })();
        let mut failure = outcome.err();
        let mut inner = self.inner.0.lock().unwrap();
        // This final source check and publication are one atomic state cut.
        if inner.generation != job.generation
            || inner.state != "ready"
            || inner.server_requests.is_closed(&job.generation)
        {
            failure = Some(Failure::Superseded);
        } else if !inner.threads.iter().any(|thread| {
            thread["generation"] == job.generation && thread["threadId"] == job.thread
        }) {
            failure = Some(Failure::Unavailable("target-no-longer-loaded"));
        }
        inner
            .observer_rebuild
            .finish(&job, job.result(reading, failure));
        1
    }

    fn observer_rebuild_source(&self, job: &Job) -> Result<(), Failure> {
        let inner = self.inner.0.lock().unwrap();
        if inner.generation != job.generation
            || inner.state != "ready"
            || inner.server_requests.is_closed(&job.generation)
        {
            return Err(Failure::Superseded);
        }
        if !inner.threads.iter().any(|thread| {
            thread["generation"] == job.generation && thread["threadId"] == job.thread
        }) {
            return Err(Failure::Unavailable("target-no-longer-loaded"));
        }
        Ok(())
    }

    fn observer_rebuild_page(
        &self,
        job: &Job,
        method: &str,
        params: Value,
        wait: Duration,
        reading: &mut Reading,
    ) -> Result<Value, Failure> {
        self.observer_rebuild_source(job)?;
        let home = job.generation["home"]
            .as_str()
            .ok_or(Failure::Unavailable("original-home-unavailable"))?;
        let query = crate::native_history::workspace_read(home, &job.generation, method, params)
            .map_err(|_| Failure::Unavailable("history-query-unavailable"))?;
        let dispatch = self
            .history_dispatch_by(
                &query,
                json!({"kind":"app-rule","name":"observer-history-read"}),
            )
            .map_err(|_| Failure::Unavailable("history-dispatch-unavailable"))?;
        reading.receipts.push(Self::observer_rebuild_receipt(
            &dispatch,
            &dispatch.evidence(),
        ));
        let evidence = self
            .history_wait(&dispatch, wait)
            .map_err(|_| Failure::Unavailable("history-receipt-unavailable"))?;
        *reading.receipts.last_mut().unwrap() =
            Self::observer_rebuild_receipt(&dispatch, &evidence);
        self.observer_rebuild_source(job)?;
        if evidence["writeResult"] != "written" {
            return Err(Failure::Unavailable("history-request-not-written"));
        }
        let response = &evidence["response"];
        if response.get("error").is_some() {
            return Err(Failure::Unavailable("supplier-history-error"));
        }
        let result = response
            .get("result")
            .filter(|result| result.is_object())
            .ok_or(Failure::Unavailable("history-result-not-observed"))?;
        if evidence["outcome"] != "response-observed-result" {
            return Err(Failure::Unavailable("history-result-not-observed"));
        }
        crate::native_history::validate_read_response(method, result)
            .map_err(|_| Failure::Unavailable("invalid-native-history-response"))?;
        if method == "thread/read" && result["thread"]["id"] != job.thread {
            return Err(Failure::Unavailable("metadata-thread-mismatch"));
        }
        reading.receipts.last_mut().unwrap()["resultAccepted"] = json!(true);
        Ok(result.clone())
    }

    fn observer_rebuild_receipt(dispatch: &HistoryDispatch, evidence: &Value) -> Value {
        let response = &evidence["response"];
        json!({"generation":dispatch.query().generation(),"method":dispatch.query().method(),"params":dispatch.query().params(),
            "requestRef":dispatch.source().request_ref(),"requestIdentity":dispatch.source().request_id(),
            "writeResult":evidence["writeResult"],"outcome":evidence["outcome"],"waitingEnded":evidence["waitingEnded"],
            "responseObserved":!response.is_null(),"errorCode":response["error"]["code"].as_i64(),
            "resultAccepted":false,"observedAt":now_rfc3339(),
            "standing":"Original private Host history receipt observed; this serialized reference grants no operational authority. Supplier error text/data are withheld."})
    }
}

#[cfg(test)]
#[path = "hosting_observer_rebuild_tests.rs"]
mod tests;
