//! DEL-02-03 REQ-008: the host side of a point placed in conversation
//! ([`crate::points`]): the offer, admission of an actual live call, the
//! placement (record, then pointer, then receipt), completion of a pointer
//! that was not saved, the offer restored on an explicit resume, the run
//! marks, and the conversation's reading for the interface.
use crate::points::{self, LogReading, Source};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

/// A conversation offered the point tool in a generation.
#[derive(Clone, Debug)]
pub(super) struct Offer {
    generation: Value,
    thread: String,
    /// The App's home class (H-acct, H-key, H-omlx), once the conversation is
    /// indexed under a project; without it no point can be kept.
    home: Option<String>,
    /// "start": offered on the thread/start this App session sent;
    /// "restored": an earlier session's offer, restored on explicit resume.
    basis: &'static str,
}
/// The points state this Host keeps in memory. Nothing here is a point: a
/// point is shown only from its pointer and its record.
#[derive(Default)]
pub(super) struct State {
    offers: Vec<Offer>,
    /// (generation, conversation, run, mark): "start sent", "not opened", "open", "ended".
    runs: Vec<(Value, String, String, &'static str)>,
    /// Calls refused in this App session: (generation, conversation, {reason, at}).
    refused: Vec<(Value, String, Value)>,
    /// Records written whose pointer could not be saved: (home class, conversation, point, reason).
    pending: Vec<(String, String, String, String)>,
    /// Why the App could not check a conversation's records in this session: (generation, conversation, reason).
    unchecked: Vec<(Value, String, String)>,
    /// The points log of each project folder, as resolved by the store when it was last written or checked.
    logs: Vec<(PathBuf, PathBuf)>,
    /// The last reading of a points log, with the file's stamp when read.
    cache: Option<(PathBuf, crate::records_index::Stamp, LogReading)>,
    /// Receipts as prepared, for tests (they have no Codex pipe to read the reply from).
    #[cfg(test)]
    receipts: Vec<Value>,
}
/// The App's refusal sentences.
const NO_PROJECT: &str = "No App project is known for this conversation, so the point could not be kept; no point was placed.";
const OTHER_PROJECT: &str = "This conversation's App project is not the project the App has open now, so the point could not be kept; no point was placed.";
const ENDED: &str = "This Codex session ended before the point could be recorded; no point was placed.";
fn store_refused(e: &str) -> String {
    format!("The App's records store did not take the point ({e}), so it could not be kept; no point was placed.")
}
fn at_cap() -> String {
    format!("This conversation already holds the App's own limit of {} points; no point was recorded.", points::POINTS_PER_CONVERSATION)
}
const REFUSED_KEPT: usize = 20;

/// One admitted call, with what the App observed at its admission.
pub(super) struct Call {
    generation: Value,
    thread: String,
    turn: String,
    call: String,
    request: Value,
    arguments: Value,
    home: Option<String>,
    run: Value,
    placer: Value,
}

impl super::Host {
    /// Called where a `thread/start` result is admitted: the start's own
    /// parameters carried the point tool's definition exactly once.
    pub(super) fn note_point_offer(i: &mut super::Inner, generation: &Value, thread: &Value, params: &Value) {
        let offered = params["dynamicTools"].as_array().is_some_and(|tools| {
            let named: Vec<&Value> = tools.iter().filter(|t| t["name"] == points::TOOL).collect();
            named.len() == 1 && *named[0] == points::definition()
        });
        if let (true, Some(thread)) = (offered, thread.as_str()) {
            if !i.points.offers.iter().any(|o| o.generation == *generation && o.thread == thread) {
                i.points.offers.push(Offer { generation: generation.clone(), thread: thread.into(), home: None, basis: "start" });
            }
        }
    }
    /// Where the conversation is indexed under its project at start: its home
    /// class is taken for the offer, and the offer pointer is written.
    pub(super) fn persist_point_offer(&self, generation: &Value, thread: &str, home: Option<&str>) {
        let Some(home) = home else { return };
        let offered = {
            let mut i = self.inner.0.lock().unwrap();
            match i.points.offers.iter_mut().find(|o| o.generation == *generation && o.thread == thread && o.basis == "start") {
                Some(offer) => { offer.home = Some(home.into()); true }
                None => false,
            }
        };
        let (Some(native), Ok(reference)) = (generation["home"].as_str(), crate::recovery::generation_ref(generation)) else { return };
        if offered {
            let _ = self.tag_conversation(generation, thread, Some(home), points::TAG_OWNER, &points::offer_pointer(native, &reference, thread));
        }
    }
    /// The run marks DEL-02-03's run makes for its conversation.
    pub(crate) fn note_conversation_run(&self, generation: &Value, thread: &str, run: &str, mark: &'static str) {
        let mut i = self.inner.0.lock().unwrap();
        i.points.runs.retain(|(g, t, r, _)| !(g == generation && t == thread && r == run));
        i.points.runs.push((generation.clone(), thread.into(), run.into(), mark));
    }
    /// The checks a received line meets to be a point call: the current
    /// generation, a server request not on a private account channel, the
    /// exact tool with no namespace, from a conversation offered it in this
    /// generation. It reads the state only.
    pub(super) fn point_call_look(i: &super::Inner, generation: &Value, frame: &Value, private_auth: bool) -> bool {
        i.generation == *generation && !i.server_requests.is_closed(generation)
            && super::frame_class(frame) == "server-request" && !private_auth
            && frame["method"] == "item/tool/call" && frame["params"]["tool"] == points::TOOL && frame["params"]["namespace"].is_null()
            && i.points.offers.iter().any(|o| o.generation == *generation && frame["params"]["threadId"] == o.thread.as_str())
    }
    /// The facts of an admitted point call, read under Inner at its admission.
    pub(super) fn point_call(i: &super::Inner, generation: &Value, frame: &Value) -> Call {
        let p = &frame["params"];
        let s = |v: &Value| v.as_str().unwrap_or_default().to_owned();
        let thread = s(&p["threadId"]);
        let offer = i.points.offers.iter().find(|o| o.generation == *generation && o.thread == thread);
        let restored = offer.is_some_and(|o| o.basis == "restored");
        let mark = i.points.runs.iter().rev().find(|(g, t, _, _)| g == generation && *t == thread);
        let run = match mark {
            Some((_, _, run, "open")) => json!({"state":"in run","run":run}),
            Some((_, _, _, "start sent")) => json!({"state":"not established","reason":"a run's start was sent in this conversation and the App had not yet recorded it opened"}),
            _ if restored => json!({"state":"not established","reason":"this conversation was resumed after the App restarted, and whether a run opened before then is still open is not known here"}),
            _ => json!({"state":"no run","reason":"no run open in this conversation in this App session"}),
        };
        let turn = s(&p["turnId"]);
        let started = i.conversation_turns.iter().find(|t| t["generation"] == *generation && t["threadId"] == thread.as_str() && t["turnId"] == turn.as_str())
            .and_then(|t| t.get("appTurnStart")).and_then(|sent| sent["requestRef"].as_str());
        let placer = match started {
            Some(reference) => {
                let person = i.source_requests.values().any(|e| e.request.generation == *generation && e.request.request_ref == reference && e.observation_base["initiator"]["kind"] == "person-directed");
                if person { json!({"observed":{"caller":"this conversation's agent, through the App's point tool","turnStart":{"by":"the App, at a press of the person's","requestRef":reference}}}) }
                else { json!({"observed":{"caller":"this conversation's agent, through the App's point tool","turnStart":null,"turnStartLimit":"the App started this turn, not at a press of the person's"}}) }
            }
            None => json!({"observed":{"caller":"this conversation's agent, through the App's point tool","turnStart":null,"turnStartLimit":"the App did not observe starting this turn"}}),
        };
        Call { generation: generation.clone(), thread, turn, call: s(&p["callId"]), request: frame["id"].clone(), arguments: p["arguments"].clone(),
            home: offer.and_then(|o| o.home.clone()), run, placer }
    }
    /// Answers an admitted point call: placed (or refused) with no Host lock
    /// held, then the receipt is prepared and written as the register's named
    /// replies are. A receipt that cannot be written leaves the record kept.
    pub(super) fn answer_point_call(&self, call: Call) {
        let (receipt, point) = self.place_point(&call);
        #[cfg(test)]
        self.inner.0.lock().unwrap().points.receipts.push(receipt.clone());
        let text = receipt["contentItems"][0]["text"].as_str().unwrap_or_default().to_owned();
        let reference = json!({"point":point,"bytes":text.len(),"content":{"method":crate::util::FILE_IDENTITY_METHOD,"value":crate::util::sha256_hex(text.as_bytes())},"success":receipt["success"]});
        if let Err(reason) = self.check_local_reply() {
            self.inner.0.lock().unwrap().journal.push(json!({"generation":call.generation,"class":"local-reply-refused","requestIdentity":call.request,"reason":reason}));
            self.flush_recovery_observations();
            return;
        }
        let prepared = {
            let mut i = self.inner.0.lock().unwrap();
            match i.server_requests.prepare_named_tool(&call.generation, &call.request, &receipt, points::RULE, reference) {
                Ok(frame) => match self.capture_pipe(&i) {
                    Ok(bound) => Some((bound, frame)),
                    Err(reason) => { i.journal.push(json!({"generation":call.generation,"class":"point-call-reply-not-attempted","reason":reason,"requestIdentity":call.request})); None }
                },
                Err(reason) => { i.journal.push(json!({"generation":call.generation,"class":"point-call-not-answered","reason":reason,"requestIdentity":call.request})); None }
            }
        };
        if let Some((bound, frame)) = prepared { let _ = self.write_reply(bound, &frame); }
        self.flush_recovery_observations();
    }
    fn refuse(&self, call: &Call, reason: String) -> (Value, Option<String>) {
        let mut i = self.inner.0.lock().unwrap();
        let mine = i.points.refused.iter().filter(|(g, t, _)| *g == call.generation && *t == call.thread).count();
        if mine >= REFUSED_KEPT {
            if let Some(at) = i.points.refused.iter().position(|(g, t, _)| *g == call.generation && *t == call.thread) { i.points.refused.remove(at); }
        }
        i.points.refused.push((call.generation.clone(), call.thread.clone(), json!({"reason":reason,"at":crate::util::now_rfc3339()})));
        (points::receipt(None, Some(&reason), None, &call.run), None)
    }
    /// The conversation's project, the project folder to write under and
    /// the ledger rows, as the App knows them now.
    fn point_project(&self, generation: &Value, thread: &str, home: &str) -> Result<(String, PathBuf, Vec<Value>), String> {
        let i = self.inner.0.lock().unwrap();
        Self::context_scope(&i, generation, thread, Some(home)).map_err(|_| ENDED.to_owned())?;
        let rows = Self::context_rows(i.recovery_snapshot.as_ref());
        let project = rows.iter().rev().find(|r| r["home"] == home && r["threadId"] == thread).and_then(|r| r["project"].as_str()).map(str::to_owned).ok_or(NO_PROJECT)?;
        let capability = i.records_capability.clone().ok_or(OTHER_PROJECT)?;
        if i.records_project_context.as_ref().and_then(|c| c.reference()) != Some(project.as_str()) {
            return Err(OTHER_PROJECT.into());
        }
        Ok((project, capability.project_folder().to_path_buf(), rows))
    }
    /// The project's points log for a write, as the store resolves it now.
    fn points_log(&self, root: &Path) -> Result<PathBuf, String> {
        let log = crate::storage::project_log(root, None, points::WRITER)?;
        let mut i = self.inner.0.lock().unwrap();
        i.points.logs.retain(|(r, _)| r != root);
        i.points.logs.push((root.to_path_buf(), log.clone()));
        Ok(log)
    }
    /// One placement: the record (or the one already bound to this call),
    /// then its pointer, then the receipt. Returns the receipt and the point.
    fn place_point(&self, call: &Call) -> (Value, Option<String>) {
        if let Err(reason) = points::validate(&call.arguments) { return self.refuse(call, reason); }
        let Some(home) = call.home.clone() else { return self.refuse(call, NO_PROJECT.into()) };
        let (Some(native), Ok(generation)) = (call.generation["home"].as_str(), crate::recovery::generation_ref(&call.generation)) else { return self.refuse(call, ENDED.into()) };
        let source = Source { home: native.into(), home_class: home.clone(), generation, thread: call.thread.clone(), turn: call.turn.clone(), call: call.call.clone(), request: call.request.clone() };
        let (project, root, rows) = match self.point_project(&call.generation, &call.thread, &home) { Ok(found) => found, Err(reason) => return self.refuse(call, reason) };
        let log = match self.points_log(&root) { Ok(log) => log, Err(e) => return self.refuse(call, store_refused(&e)) };
        let reading = match LogReading::read(&log) { Ok(reading) => reading, Err(e) => return self.refuse(call, store_refused(&e)) };
        // Pointers this conversation's earlier records are owed, completed first.
        self.complete_pointers(&call.generation, &call.thread, &home, &project, &reading);
        let existing = reading.for_call(&source).first().map(|l| l.entry.clone());
        let entry = match existing {
            // One placement per call: the record already bound to this call identity.
            Some(entry) => entry,
            None => {
                let held = crate::recovery::tags_of(&rows, &home, &call.thread, points::TAG_OWNER).iter()
                    .filter(|t| t["value"].as_str().and_then(points::decode).is_some_and(|v| v["kind"] == "placed")).count();
                if held >= points::POINTS_PER_CONVERSATION { return self.refuse(call, at_cap()); }
                let point = match crate::util::opaque_id("pt-") { Ok(point) => point, Err(e) => return self.refuse(call, store_refused(&e)) };
                let digest = match points::digest(&call.arguments) { Ok(d) => d, Err(e) => return self.refuse(call, store_refused(&e)) };
                let body = points::record_body(&point, &source, &project, &call.run, &call.placer, &call.arguments, &digest, &crate::util::now_rfc3339());
                match crate::records::append_project(&root, None, points::WRITER, points::KIND, &crate::records::APP_WRITER, body) {
                    Ok(entry) => entry,
                    Err(e) => return self.refuse(call, store_refused(&e)),
                }
            }
        };
        let point = entry["body"]["point"].as_str().unwrap_or_default().to_owned();
        let persistence = self.save_pointer(&call.generation, &call.thread, &home, &entry);
        (points::receipt(Some(&point), None, Some(&persistence), &entry["body"]["run"]), Some(point))
    }
    /// The pointer for a written record, through the conversation's tag.
    /// Returns the receipt's persistence sentence; a pointer not saved is
    /// remembered so that the conversation's reading is not whole until it is.
    fn save_pointer(&self, generation: &Value, thread: &str, home: &str, entry: &Value) -> String {
        let point = entry["body"]["point"].as_str().unwrap_or_default().to_owned();
        let saved = match points::pointer(entry) {
            Ok(value) => {
                let tagged = self.tag_conversation(generation, thread, Some(home), points::TAG_OWNER, &value);
                if tagged["persistence"] == "durable App metadata" { Ok(()) } else { Err(tagged["limit"].as_str().unwrap_or("the pointer could not be saved").to_owned()) }
            }
            Err(e) => Err(e),
        };
        let mut i = self.inner.0.lock().unwrap();
        i.points.pending.retain(|(h, t, p, _)| !(h == home && t == thread && *p == point));
        match saved {
            Ok(()) => points::KEPT.to_owned(),
            Err(reason) => {
                i.points.pending.push((home.into(), thread.into(), point, reason.clone()));
                points::pointer_pending(&reason)
            }
        }
    }
    /// Completes the pointer of each record of this conversation and project
    /// that no pointer names, from the record's own binding. A record of
    /// another home, conversation or project is never touched.
    fn complete_pointers(&self, generation: &Value, thread: &str, home: &str, project: &str, reading: &LogReading) {
        let native = generation["home"].as_str().unwrap_or_default();
        let rows = { let i = self.inner.0.lock().unwrap(); Self::context_rows(i.recovery_snapshot.as_ref()) };
        let named: Vec<Value> = crate::recovery::tags_of(&rows, home, thread, points::TAG_OWNER).iter()
            .filter_map(|t| t["value"].as_str().and_then(points::decode)).filter(|v| v["kind"] == "placed").map(|v| v["point"].clone()).collect();
        for line in &reading.entries {
            let body = &line.entry["body"];
            let src = &body["source"];
            if src["home"] != native || src["homeClass"] != home || src["thread"] != thread || body["project"] != project || named.contains(&body["point"]) { continue; }
            self.save_pointer(generation, thread, home, &line.entry);
        }
    }
    /// On an explicit resume (after `restore_records_receipt`): the earlier
    /// offer is restored from its pointer when it names this Codex home and
    /// conversation and the definition offered now, and records of this
    /// conversation whose pointer was not saved are completed.
    pub(super) fn restore_point_offer(&self, generation: &Value, thread: &str) {
        let native = generation["home"].as_str().unwrap_or_default().to_owned();
        let rows = {
            let _writer = self.recovery_writer.lock().unwrap();
            self.drain_recovery_owned();
            self.refresh_recovery_observation();
            let i = self.inner.0.lock().unwrap();
            if Self::context_scope(&i, generation, thread, None).is_err() { return; }
            if i.recovery_initialization_error.is_some() || i.recovery_error.is_some() || i.recovery_snapshot.is_none() {
                drop(i);
                return self.point_unchecked(generation, thread, "the App's recovery ledger could not be read");
            }
            Self::context_rows(i.recovery_snapshot.as_ref())
        };
        let homes: Vec<String> = {
            let mut homes: Vec<String> = rows.iter().filter(|r| r["threadId"] == thread).filter_map(|r| r["home"].as_str().map(str::to_owned)).collect();
            homes.sort(); homes.dedup(); homes
        };
        let offered: Vec<String> = homes.iter().filter(|home| crate::recovery::tags_of(&rows, home, thread, points::TAG_OWNER).iter()
            .filter_map(|t| t["value"].as_str().and_then(points::decode))
            .any(|v| v["kind"] == "offered" && v["home"] == native.as_str() && v["thread"] == thread && v["definition"] == points::definition_digest())).cloned().collect();
        let home = match (offered.as_slice(), homes.as_slice()) {
            ([one], _) => {
                let mut i = self.inner.0.lock().unwrap();
                if Self::context_scope(&i, generation, thread, None).is_err() { return; }
                i.points.offers.push(Offer { generation: generation.clone(), thread: thread.into(), home: Some(one.clone()), basis: "restored" });
                one.clone()
            }
            ([], [one]) => one.clone(),
            ([], []) => return,
            _ => return self.point_unchecked(generation, thread, "the App's ledger names this conversation in more than one home"),
        };
        let checked = self.point_project(generation, thread, &home)
            .and_then(|(project, root, _)| { let log = self.points_log(&root)?; Ok((project, LogReading::read(&log)?)) });
        match checked {
            Ok((project, reading)) => self.complete_pointers(generation, thread, &home, &project, &reading),
            Err(reason) if reason == NO_PROJECT => {}
            Err(reason) => self.point_unchecked(generation, thread, &format!("the App could not check its records for this conversation's points: {reason}")),
        }
    }
    fn point_unchecked(&self, generation: &Value, thread: &str, reason: &str) {
        self.inner.0.lock().unwrap().points.unchecked.push((generation.clone(), thread.into(), reason.into()));
    }
    /// A points log read through the store's reader, reused while the file's
    /// stamp is unchanged.
    fn read_points_log(&self, log: &Path) -> Result<LogReading, String> {
        let stamp = match std::fs::metadata(log) {
            Ok(m) => Some(crate::records_index::Stamp::of(&m)),
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
            Err(e) => return Err(format!("the App's points log could not be read ({e})")),
        };
        if let Some(stamp) = stamp {
            if let Some((path, held, reading)) = &self.inner.0.lock().unwrap().points.cache {
                if path == log && *held == stamp { return Ok(reading.clone()); }
            }
        }
        let reading = LogReading::read(log)?;
        if let Some(stamp) = stamp { self.inner.0.lock().unwrap().points.cache = Some((log.to_path_buf(), stamp, reading.clone())); }
        Ok(reading)
    }
    /// Each current conversation's points as the App reads them now: from the
    /// pointers in the ledger, each joined to its record. Read with no Host
    /// lock held while the log is read.
    pub(super) fn points_view(&self) -> Value {
        struct Row { thread: String, offer: Option<Offer>, project: Option<String>, pointers: Vec<Value>, refused: Vec<Value>, reasons: Vec<String> }
        let (generation, rows, capability, context) = {
            let i = self.inner.0.lock().unwrap();
            let generation = i.generation.clone();
            if generation.is_null() { return json!([]); }
            let ledger = Self::context_rows(i.recovery_snapshot.as_ref());
            let health = if i.recovery_initialization_error.is_some() || i.recovery_error.is_some() || i.recovery_snapshot.is_none() {
                Some("the App's recovery ledger could not be read".to_owned())
            } else {
                i.recovery_snapshot.as_ref().and_then(|o| o.summary["historyLimits"].as_array().filter(|l| !l.is_empty()).map(|_| "the App's recovery ledger history is incomplete".to_owned()))
            };
            let rows: Vec<Row> = i.threads.iter().filter(|t| t["generation"] == generation).filter_map(|t| t["threadId"].as_str()).map(|thread| {
                let offer = i.points.offers.iter().find(|o| o.generation == generation && o.thread == thread).cloned();
                let home = offer.as_ref().and_then(|o| o.home.clone());
                let mut reasons: Vec<String> = health.iter().cloned().collect();
                reasons.extend(i.points.pending.iter().filter(|(h, t, _, _)| Some(h) == home.as_ref() && t == thread)
                    .map(|(_, _, p, why)| format!("the pointer to point {p} could not be saved ({why}); the App completes it when it next can")));
                reasons.extend(i.points.unchecked.iter().filter(|(g, t, _)| *g == generation && t == thread).map(|(_, _, why)| why.clone()));
                let pointers = home.as_deref().map(|home| crate::recovery::tags_of(&ledger, home, thread, points::TAG_OWNER).iter()
                    .filter_map(|t| t["value"].as_str().and_then(points::decode)).filter(|v| v["kind"] == "placed").collect()).unwrap_or_default();
                let project = home.as_deref().and_then(|home| ledger.iter().rev().find(|r| r["home"] == home && r["threadId"] == thread)).and_then(|r| r["project"].as_str()).map(str::to_owned);
                let refused = i.points.refused.iter().filter(|(g, t, _)| *g == generation && t == thread).map(|(_, _, r)| r.clone()).collect();
                Row { thread: thread.into(), offer, project, pointers, refused, reasons }
            }).collect();
            let capability = i.records_capability.as_ref().and_then(|c| i.points.logs.iter().find(|(root, _)| root == c.project_folder()).map(|(_, log)| log.clone()));
            (generation, rows, capability, i.records_project_context.as_ref().and_then(|c| c.reference()).map(str::to_owned))
        };
        let native = generation["home"].as_str().unwrap_or_default();
        let views: Vec<Value> = rows.into_iter().map(|mut row| {
            let offer = match &row.offer {
                Some(o) if o.basis == "start" => json!({"state":"offered at start in this App session"}),
                Some(_) => json!({"state":"offered when this conversation started, restored after the App restarted"}),
                None => json!({"state":"not offered in this App session"}),
            };
            let home = row.offer.as_ref().and_then(|o| o.home.clone());
            let points: Vec<Value> = match (&home, &row.project) {
                (Some(home), Some(project)) if !row.pointers.is_empty() => {
                    let log = match (&capability, &context) {
                        (Some(log), Some(open)) if open == project => self.read_points_log(log),
                        (_, Some(open)) if open != project => Err("this conversation's App project is not the project the App has open now".to_owned()),
                        _ => Err("the App has not opened this project's points log in this App session".to_owned()),
                    };
                    let conversation = points::Conversation { home: native, home_class: home, thread: &row.thread, project };
                    row.pointers.iter().map(|p| points::join(p, &log, &conversation)).collect()
                }
                // Pointers whose conversation's project the ledger no longer
                // names are not shown, and the reading says it is not whole.
                _ => {
                    if !row.pointers.is_empty() { row.reasons.push("this conversation's App project could not be read from the App's ledger".into()); }
                    vec![]
                }
            };
            json!({"generation":generation,"threadId":row.thread,"offer":offer,
                "reading":{"whole":row.reasons.is_empty(),"reasons":row.reasons},"points":points,"refused":row.refused})
        }).collect();
        json!(views)
    }
}

#[cfg(test)]
#[path = "hosting_points_tests.rs"]
mod tests;
