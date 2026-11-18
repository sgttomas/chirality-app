//! DEL-02-03 REQ-008: the host side of a point placed in conversation
//! ([`crate::points`]): the offer, admission of an actual live call, the
//! placement (record, then pointer, then receipt) one at a time, completion
//! of a pointer that was not saved, the offer restored on an explicit resume,
//! the run marks, and the conversation's reading for the interface.
//!
//! Placement binds through the store's own writer binding
//! ([`crate::records_store::bind_writer`]) and reading through its reader
//! binding ([`crate::records_store::bind_reader`]), which registers and
//! attaches nothing; both are checked against the physical project folder the
//! records capability admitted, and the record and pointer carry the store's
//! stable project identity.
//!
//! What the reading costs, per status read: where no current conversation has
//! something to join (a pointer, an owed pointer, a mark of this session, or
//! records this session wrote or found on resume), nothing is read. Otherwise the project's points log is bound and its file
//! examined once; it is parsed again only when its stamp changed, the reading
//! is shared (no copy per conversation), each record's soundness and digest
//! are computed once per parse, and each conversation looks up only its own
//! records through an index. The 100-point limit bounds one conversation's
//! pointers, not the project's log, which grows with every placement in the
//! project (each at most the App's 16,384-byte limit of terms and its
//! envelope); a parse is linear in it.
use crate::points::{self, Conversation, LogReading, Outcome, Source};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};

/// One placement, completion or restoration at a time in this process, for
/// the whole of its reconcile, lookup, count, append and pointer.
static PLACEMENT: Mutex<()> = Mutex::new(());
fn one_at_a_time() -> std::sync::MutexGuard<'static, ()> {
    PLACEMENT.lock().unwrap_or_else(|poisoned| poisoned.into_inner())
}

/// A conversation offered the point tool in a generation.
#[derive(Clone, Debug)]
pub(super) struct Offer {
    generation: Value,
    thread: String,
    /// The App's home class (H-acct, H-key, H-omlx), once the conversation is
    /// indexed under a project; without it no point can be kept.
    home: Option<String>,
    /// "start": offered on the thread/start this App session sent;
    /// "restored": an earlier offer, restored on explicit resume.
    basis: &'static str,
}
/// A call whose recording the App could not establish.
#[derive(Clone, Debug)]
struct Uncertain {
    thread: String,
    source: Source,
    reason: String,
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
    uncertain: Vec<Uncertain>,
    /// Why the App could not check a conversation's records on resume: (generation, conversation, reason).
    unchecked: Vec<(Value, String, String)>,
    /// Conversations (home class, conversation) whose records this App
    /// session wrote, or found on resume: their reading always reads the log,
    /// so that a record without a pointer, or one that cannot be established,
    /// is reported and never read as no point.
    watched: Vec<(String, String)>,
    /// The last reading of a points log: its path, stamp and store project.
    cache: Option<(PathBuf, crate::records_index::Stamp, String, Arc<LogReading>)>,
    /// Receipts as prepared, for tests.
    #[cfg(test)]
    pub(super) receipts: Vec<Value>,
    /// Run with no Host lock held just before a reply is written (tests).
    #[cfg(test)]
    pub(super) before_reply: Option<Box<dyn FnOnce() + Send>>,
}
/// The App's refusal sentences.
const NO_PROJECT: &str = "No App project is known for this conversation, so the point could not be kept; no point was placed.";
const ENDED: &str = "This Codex session ended before the point could be recorded; no point was placed.";
const STORE_OTHER: &str = "This conversation's points are kept in other records than the records this project folder belongs to now, so the point could not be kept; no point was placed.";
fn kept_refusal(reason: &str) -> String {
    let mut chars = reason.chars();
    let first = chars.next().map(|c| c.to_uppercase().collect::<String>()).unwrap_or_default();
    format!("{first}{}, so the point could not be kept; no point was placed.", chars.as_str())
}
fn store_refused(e: &str) -> String {
    format!("The App's records store did not take the point ({e}), so it could not be kept; no point was placed.")
}
fn at_cap() -> String {
    format!("This conversation already holds the App's own limit of {} points; no point was recorded.", points::POINTS_PER_CONVERSATION)
}
const OTHER_OPEN: &str = "this conversation's App project is not the project the App has open now";

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
    observed: Value,
}

/// The home class and App project the ledger indexes a conversation under,
/// whether or not the tool is offered in this App session.
fn scope_of(rows: &[Value], thread: &str) -> Result<Option<(String, String)>, String> {
    let mut homes: Vec<&str> = rows.iter().filter(|r| r["kind"] == "conversation_index" && r["threadId"] == thread).filter_map(|r| r["home"].as_str()).collect();
    homes.sort();
    homes.dedup();
    match homes.as_slice() {
        [] => Ok(None),
        [home] => Ok(rows.iter().rev().find(|r| r["kind"] == "conversation_index" && r["home"] == *home && r["threadId"] == thread)
            .and_then(|r| r["project"].as_str()).map(|p| (home.to_string(), p.to_owned()))),
        _ => Err("the App's ledger names this conversation in more than one home".into()),
    }
}
/// The conversation's pointers of this owner, decoded, and how many tags of
/// this owner could not be read as a pointer.
fn pointers_of(rows: &[Value], home: &str, thread: &str) -> (Vec<Value>, Vec<Value>, usize) {
    let (mut placed, mut offered, mut unread) = (vec![], vec![], 0);
    for tag in crate::recovery::tags_of(rows, home, thread, points::TAG_OWNER) {
        match tag["value"].as_str().and_then(points::decode) {
            Some(v) if v["kind"] == "placed" => placed.push(v),
            Some(v) => offered.push(v),
            None => unread += 1,
        }
    }
    (placed, offered, unread)
}
fn same_folder(bound: (u64, u64), physical: &Value) -> Result<(), String> {
    if (physical["device"].as_u64(), physical["inode"].as_u64()) == (Some(bound.0), Some(bound.1)) { Ok(()) }
    else { Err("the project folder the records store binds is not the folder the App admitted for this project".into()) }
}
/// The store's writer binding for the project folder and the points log in
/// it: checked against the admitted physical folder and proved for writing.
fn bind_for_write(root: &Path, physical: &Value) -> Result<(crate::records_store::WriterBinding, PathBuf), String> {
    let binding = crate::records_store::bind_writer(root)?;
    same_folder(binding.project_folder(), physical)?;
    binding.prove_for_write()?;
    let log = binding.records_dir().join(crate::storage::log_rel(None, points::WRITER));
    Ok((binding, log))
}
/// The store's reader binding for the project folder: the store's project
/// identity and the points log, through the store's read decision. It
/// registers and attaches nothing: the identity is taken from the store's
/// binding of an already attached project (which mints nothing), and both
/// bindings must name the same project folder and records folder.
fn bind_for_read(root: &Path, physical: &Value) -> Result<(String, PathBuf), String> {
    let reader = crate::records_store::bind_reader(root, crate::records_store::ReaderDecision::Records)?;
    reader.prove().map_err(String::from)?;
    same_folder(reader.project_folder(), physical)?;
    let (dir, _) = reader.records_folder().ok_or("this project's records are read in place, where no points log is kept")?;
    let attached = crate::records_store::bind_writer_if_attached(root)?.ok_or("this project has no records in the App's records store")?;
    if attached.project_folder() != reader.project_folder() || attached.records_dir() != dir {
        return Err("the project's records association changed while it was read".into());
    }
    Ok((attached.project_id().to_owned(), dir.join(crate::storage::log_rel(None, points::WRITER))))
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
    /// generation, a well-formed server request (no result or error, the
    /// call's identities present) not on a private account channel, the exact
    /// tool with no namespace, from a conversation offered it in this
    /// generation. It reads the state only.
    pub(super) fn point_call_look(i: &super::Inner, generation: &Value, frame: &Value, private_auth: bool) -> bool {
        i.generation == *generation && !i.server_requests.is_closed(generation)
            && super::frame_class(frame) == "server-request" && !private_auth
            && points::frame_ok(frame) && frame["params"]["namespace"].is_null()
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
            Some((_, _, run, "open")) => points::run_in(run),
            Some((_, _, _, "start sent")) => points::run_not_established("start-sent-not-yet-open"),
            _ if restored => points::run_not_established("resumed-earlier-run-unknown"),
            _ => points::run_none(),
        };
        let turn = s(&p["turnId"]);
        let started = i.conversation_turns.iter().find(|t| t["generation"] == *generation && t["threadId"] == thread.as_str() && t["turnId"] == turn.as_str())
            .and_then(|t| t.get("appTurnStart")).and_then(|sent| sent["requestRef"].as_str());
        let observed = match started {
            Some(reference) => {
                let person = i.source_requests.values().any(|e| e.request.generation == *generation && e.request.request_ref == reference && e.observation_base["initiator"]["kind"] == "person-directed");
                points::observed(person.then_some(reference), true)
            }
            None => points::observed(None, false),
        };
        Call { generation: generation.clone(), thread, turn, call: s(&p["callId"]), request: frame["id"].clone(), arguments: p["arguments"].clone(),
            home: offer.and_then(|o| o.home.clone()), run, observed }
    }
    /// Answers an admitted point call: placed (or refused) with no Host lock
    /// held, then the receipt is prepared and written as the register's named
    /// replies are. A receipt that cannot be written leaves the record kept.
    pub(super) fn answer_point_call(&self, call: Call) {
        let outcome = self.place_point(&call);
        let receipt = points::receipt(&outcome, &call.run);
        let point = match &outcome { Outcome::Recorded { point, .. } => Some(point.clone()), Outcome::NotEstablished { point, .. } => point.clone(), Outcome::NotRecorded { .. } => None };
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
        #[cfg(test)]
        { let hook = self.inner.0.lock().unwrap().points.before_reply.take(); if let Some(hook) = hook { hook(); } }
        if let Some((bound, frame)) = prepared { let _ = self.write_reply(bound, &frame); }
        self.flush_recovery_observations();
    }
    fn refuse(&self, call: &Call, reason: String) -> Outcome {
        let mut i = self.inner.0.lock().unwrap();
        let mine = i.points.refused.iter().filter(|(g, t, _)| *g == call.generation && *t == call.thread).count();
        if mine >= points::REFUSALS_KEPT {
            if let Some(at) = i.points.refused.iter().position(|(g, t, _)| *g == call.generation && *t == call.thread) { i.points.refused.remove(at); }
        }
        i.points.refused.push((call.generation.clone(), call.thread.clone(), json!({"reason":reason,"at":crate::util::now_rfc3339()})));
        Outcome::NotRecorded { reason }
    }
    /// A call whose recording the App could not establish: remembered, so
    /// that the conversation's reading is not whole until a read resolves it.
    fn not_established(&self, source: &Source, point: Option<String>, reason: String) -> Outcome {
        self.inner.0.lock().unwrap().points.uncertain.push(Uncertain { thread: source.thread.clone(), source: source.clone(), reason: reason.clone() });
        Outcome::NotEstablished { point, reason: points::not_established(&reason) }
    }
    fn ledger_rows(&self) -> Arc<Vec<Value>> {
        self.inner.0.lock().unwrap().recovery_snapshot.as_ref().map(|o| Arc::clone(&o.rows)).unwrap_or_default()
    }
    /// The open project's folder and its admitted physical identity, when the
    /// conversation's App project is the project the App has open now.
    fn open_project(&self, project: &str) -> Result<(PathBuf, Value), String> {
        let (capability, open) = {
            let i = self.inner.0.lock().unwrap();
            (i.records_capability.clone(), i.records_project_context.as_ref().and_then(|c| c.reference()).map(str::to_owned))
        };
        if open.as_deref() != Some(project) { return Err(OTHER_OPEN.into()); }
        let capability = capability.ok_or(OTHER_OPEN)?;
        let physical = capability.project_identity().map_err(|e| format!("this project's folder is not the folder the App admitted ({e})"))?;
        Ok((capability.project_folder().to_path_buf(), physical))
    }
    /// One placement, under the one placement lock for the whole of it: every
    /// refusal the App can decide without writing, then owed pointers of this
    /// conversation, then the record (or the one already bound to this call),
    /// then its pointer.
    fn place_point(&self, call: &Call) -> Outcome {
        let _one = one_at_a_time();
        if let Err(reason) = points::validate(&call.arguments) { return self.refuse(call, reason); }
        let (Some(native), Ok(generation)) = (call.generation["home"].as_str(), crate::recovery::generation_ref(&call.generation)) else { return self.refuse(call, ENDED.into()) };
        let unscoped = { let i = self.inner.0.lock().unwrap(); Self::context_scope(&i, &call.generation, &call.thread, None).is_err() };
        if unscoped { return self.refuse(call, ENDED.into()); }
        let rows = self.ledger_rows();
        let (home, project) = match scope_of(&rows, &call.thread) {
            Ok(Some(scope)) if call.home.as_deref() == Some(scope.0.as_str()) => scope,
            Ok(_) => return self.refuse(call, NO_PROJECT.into()),
            Err(reason) => return self.refuse(call, kept_refusal(&reason)),
        };
        let (root, physical) = match self.open_project(&project) { Ok(found) => found, Err(reason) => return self.refuse(call, kept_refusal(&reason)) };
        let (binding, log) = match bind_for_write(&root, &physical) { Ok(bound) => bound, Err(e) => return self.refuse(call, store_refused(&e)) };
        let store_project = binding.project_id().to_owned();
        self.watch(&home, &call.thread);
        let conversation = Conversation { home: native, home_class: &home, thread: &call.thread, project: &project, store_project: &store_project };
        let source = Source { home: native.into(), home_class: home.clone(), generation, thread: call.thread.clone(), turn: call.turn.clone(), call: call.call.clone(), request: call.request.clone() };
        let (placed, _, _) = pointers_of(&rows, &home, &call.thread);
        if placed.iter().any(|p| p["storeProject"] != store_project.as_str()) { return self.refuse(call, STORE_OTHER.into()); }
        let reading = match LogReading::read(&log) { Ok(reading) => reading, Err(e) => return self.refuse(call, store_refused(&e)) };
        // The call itself, met again: the lookup by its identity is the guard
        // that an unresolved write is never doubled.
        if reading.tail_is(&source) {
            return self.not_established(&source, None, "the record for this call is the last line of the points log and is not yet terminated".into());
        }
        let existing = match reading.for_call(&source).as_slice() {
            [] => None,
            [i] if reading.soundness(*i).is_ok() && conversation.names(&reading.lines[*i].entry["body"]) => Some(reading.lines[*i].entry.clone()),
            _ => return self.not_established(&source, None, "the App's records hold a record for this call that it cannot establish".into()),
        };
        let entry = match existing {
            Some(entry) => entry,
            None => {
                if let Some(reason) = (!reading.limits.is_empty() || !reading.refused.is_empty()).then(|| reading.inventory_reasons().join("; ")) {
                    return self.refuse(call, format!("The App could not read this project's points log whole ({reason}), so it cannot establish that this call was not recorded before; no point was placed."));
                }
                let held = reading.for_thread(&call.thread).iter().filter(|i| conversation.names(&reading.lines[**i].entry["body"])).count();
                if held >= points::POINTS_PER_CONVERSATION { return self.refuse(call, at_cap()); }
                // Owed pointers of this conversation, completed first.
                self.complete_pointers(&call.generation, &conversation, &reading);
                let (point, record) = match (crate::util::opaque_id("pt-"), crate::util::opaque_id("rec:app:")) {
                    (Ok(point), Ok(record)) => (point, record),
                    (Err(e), _) | (_, Err(e)) => return self.refuse(call, store_refused(&e)),
                };
                let digest = match points::digest(&call.arguments) { Ok(d) => d, Err(e) => return self.refuse(call, store_refused(&e)) };
                let body = points::record_body(&point, &source, &project, &store_project, &call.run, &call.observed, &call.arguments, &digest, &crate::util::now_rfc3339());
                if let Err(e) = binding.prove_for_write() { return self.refuse(call, store_refused(&e)); }
                match crate::records::append_reserved(&log, points::KIND, &crate::records::APP_WRITER, body, record.clone(), None, None, crate::records::RecordSet::Complete, crate::schema_validation::bundled()) {
                    Ok(entry) => entry,
                    // The writer can fail after the line, or part of it, was
                    // written: the log is read again before anything is said.
                    Err(e) => match LogReading::read(&log) {
                        Ok(again) => match again.for_call(&source).as_slice() {
                            [i] if again.soundness(*i).is_ok() && conversation.names(&again.lines[*i].entry["body"]) => again.lines[*i].entry.clone(),
                            [] if again.whole() => return self.refuse(call, store_refused(&e)),
                            _ => return self.not_established(&source, Some(point), format!("the write reported {e}, and the App's records do not show whether it landed")),
                        },
                        Err(again) => return self.not_established(&source, Some(point), format!("the write reported {e}, and the points log could not be read again: {again}")),
                    },
                }
            }
        };
        let point = entry["body"]["point"].as_str().unwrap_or_default().to_owned();
        let persistence = self.save_pointer(&call.generation, &call.thread, &home, &entry);
        Outcome::Recorded { point, persistence, run: entry["body"]["run"].clone() }
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
    /// Completes the pointer of each sound record of this conversation and
    /// store project that no pointer names, from the record's own identities.
    /// A record of another home, conversation or project, or one that is not
    /// sound, is never given a pointer.
    fn complete_pointers(&self, generation: &Value, conversation: &Conversation, reading: &LogReading) {
        let rows = self.ledger_rows();
        let (placed, _, _) = pointers_of(&rows, conversation.home_class, conversation.thread);
        let named: Vec<&Value> = placed.iter().map(|p| &p["point"]).collect();
        for &i in reading.for_thread(conversation.thread) {
            let body = &reading.lines[i].entry["body"];
            if !conversation.names(body) || reading.soundness(i).is_err() || named.contains(&&body["point"]) { continue; }
            self.save_pointer(generation, conversation.thread, conversation.home_class, &reading.lines[i].entry);
        }
    }
    /// On an explicit resume (after `restore_records_receipt`): the earlier
    /// offer is restored from its pointer when it names this Codex home and
    /// conversation and the definition offered now; and, whether or not it is
    /// restored, sound records of this conversation whose pointer was not
    /// saved get their pointer. The records are read through the store's read
    /// binding, which registers and attaches nothing.
    pub(super) fn restore_point_offer(&self, generation: &Value, thread: &str) {
        let _one = one_at_a_time();
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
            drop(i);
            self.ledger_rows()
        };
        let (home, project) = match scope_of(&rows, thread) {
            Ok(Some(scope)) => scope,
            Ok(None) => return,
            Err(reason) => return self.point_unchecked(generation, thread, &reason),
        };
        let (placed, offers, _) = pointers_of(&rows, &home, thread);
        if offers.iter().any(|v| v["home"] == native.as_str() && v["thread"] == thread && v["definition"] == points::definition_digest()) {
            let mut i = self.inner.0.lock().unwrap();
            if Self::context_scope(&i, generation, thread, None).is_err() { return; }
            if !i.points.offers.iter().any(|o| o.generation == *generation && o.thread == thread) {
                i.points.offers.push(Offer { generation: generation.clone(), thread: thread.into(), home: Some(home.clone()), basis: "restored" });
            }
        }
        // A conversation never offered the tool and holding no pointer has no
        // record to complete; another project's are read when it is open.
        if placed.is_empty() && offers.is_empty() { return; }
        let checked = self.open_project(&project).and_then(|(root, physical)| {
            let (store, log) = bind_for_read(&root, &physical)?;
            Ok((store, LogReading::read(&log)?))
        });
        match checked {
            Ok((store, reading)) => {
                if !reading.for_thread(thread).is_empty() || reading.tail != points::Tail::None { self.watch(&home, thread); }
                let conversation = Conversation { home: &native, home_class: &home, thread, project: &project, store_project: &store };
                self.complete_pointers(generation, &conversation, &reading);
            }
            Err(reason) if reason == OTHER_OPEN => {}
            Err(reason) => self.point_unchecked(generation, thread, &format!("the App could not check its records for this conversation's points: {reason}")),
        }
    }
    fn watch(&self, home: &str, thread: &str) {
        let mut i = self.inner.0.lock().unwrap();
        if !i.points.watched.iter().any(|(h, t)| h == home && t == thread) { i.points.watched.push((home.into(), thread.into())); }
    }
    fn point_unchecked(&self, generation: &Value, thread: &str, reason: &str) {
        self.inner.0.lock().unwrap().points.unchecked.push((generation.clone(), thread.into(), reason.into()));
    }
    /// A points log read through the store's reader, shared while the file's
    /// stamp and the store's project identity are unchanged.
    fn read_points_log(&self, log: &Path, store: &str) -> Result<Arc<LogReading>, String> {
        let stamp = match std::fs::metadata(log) {
            Ok(m) => crate::records_index::Stamp::of(&m),
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return LogReading::read(log).map(Arc::new),
            Err(e) => return Err(format!("the App's points log could not be read ({e})")),
        };
        if let Some((path, held, project, reading)) = &self.inner.0.lock().unwrap().points.cache {
            if path == log && *held == stamp && project == store { return Ok(Arc::clone(reading)); }
        }
        let reading = Arc::new(LogReading::read(log)?);
        self.inner.0.lock().unwrap().points.cache = Some((log.to_path_buf(), stamp, store.to_owned(), Arc::clone(&reading)));
        Ok(reading)
    }
    /// Each current conversation's points as the App reads them now: from the
    /// pointers in the ledger, each joined to its sound record. The reading's
    /// scope (home, project, log) comes from the ledger and the store, not
    /// from whether the tool is offered. Read with no Host lock held while
    /// the log is read; marks this read resolves are cleared.
    pub(super) fn points_view(&self) -> Value {
        struct Row { thread: String, offer: Option<Offer>, scope: Result<Option<(String, String)>, String>, placed: Vec<Value>, unread: usize, refused: Vec<Value>, watched: bool,
            pending: Vec<(String, String)>, uncertain: Vec<Uncertain>, unchecked: Vec<String> }
        let (generation, rows, health, threads) = {
            let i = self.inner.0.lock().unwrap();
            let generation = i.generation.clone();
            if generation.is_null() { return json!([]); }
            let health = if i.recovery_initialization_error.is_some() || i.recovery_error.is_some() || i.recovery_snapshot.is_none() {
                Some("the App's recovery ledger could not be read".to_owned())
            } else {
                i.recovery_snapshot.as_ref().and_then(|o| o.summary["historyLimits"].as_array().filter(|l| !l.is_empty()).map(|_| "the App's recovery ledger history is incomplete".to_owned()))
            };
            let rows: Arc<Vec<Value>> = i.recovery_snapshot.as_ref().map(|o| Arc::clone(&o.rows)).unwrap_or_default();
            let threads: Vec<Row> = i.threads.iter().filter(|t| t["generation"] == generation).filter_map(|t| t["threadId"].as_str()).map(|thread| {
                let scope = scope_of(&rows, thread);
                let (placed, _, unread) = match &scope { Ok(Some((home, _))) => pointers_of(&rows, home, thread), _ => (vec![], vec![], 0) };
                let watched = matches!(&scope, Ok(Some((home, _))) if i.points.watched.iter().any(|(h, t)| h == home && t == thread));
                Row { thread: thread.into(), offer: i.points.offers.iter().find(|o| o.generation == generation && o.thread == thread).cloned(), scope, placed, unread, watched,
                    refused: i.points.refused.iter().filter(|(g, t, _)| *g == generation && t == thread).map(|(_, _, r)| r.clone()).collect(),
                    pending: i.points.pending.iter().filter(|(_, t, _, _)| t == thread).map(|(_, _, p, why)| (p.clone(), why.clone())).collect(),
                    uncertain: i.points.uncertain.iter().filter(|u| u.thread == thread).cloned().collect(),
                    unchecked: i.points.unchecked.iter().filter(|(g, t, _)| *g == generation && t == thread).map(|(_, _, why)| why.clone()).collect() }
            }).collect();
            (generation, rows, health, threads)
        };
        drop(rows);
        let native = generation["home"].as_str().unwrap_or_default().to_owned();
        // The project's log, bound and read once for every conversation that has something to join.
        type Bound = Result<(String, Arc<LogReading>), String>;
        let mut bound: Vec<(String, Bound)> = vec![];
        let (mut resolved_pending, mut resolved_uncertain, mut checked_threads, mut later_refused) = (vec![], vec![], vec![], vec![]);
        let views: Vec<Value> = threads.into_iter().map(|row| {
            let mut reasons: Vec<String> = health.iter().cloned().collect();
            let offer = match &row.offer {
                Some(o) if o.basis == "start" => json!({"state":"offered at start in this App session"}),
                Some(_) => json!({"state":"offered when this conversation started; restored when it was resumed"}),
                None => json!({"state":"not offered in this App session"}),
            };
            let mut shown: Vec<Value> = vec![];
            let mut refused = row.refused.clone();
            match &row.scope {
                Err(why) => reasons.push(why.clone()),
                Ok(None) => {}
                Ok(Some((home, project))) => {
                    if row.unread > 0 { reasons.push(format!("{} pointer(s) kept for this conversation could not be read", row.unread)); }
                    let something = row.watched || !row.placed.is_empty() || !row.pending.is_empty() || !row.uncertain.is_empty() || !row.unchecked.is_empty();
                    if something {
                        let read = match bound.iter().find(|(p, _)| p == project) {
                            Some((_, read)) => read.clone(),
                            None => {
                                let read = self.open_project(project).and_then(|(root, physical)| {
                                    let (store, log) = bind_for_read(&root, &physical)?;
                                    Ok((store.clone(), self.read_points_log(&log, &store)?))
                                });
                                bound.push((project.clone(), read.clone()));
                                read
                            }
                        };
                        let store = read.as_ref().map(|(s, _)| s.clone()).unwrap_or_default();
                        let log = read.as_ref().map(|(_, r)| Arc::clone(r)).map_err(Clone::clone);
                        let conversation = Conversation { home: &native, home_class: home, thread: &row.thread, project, store_project: &store };
                        shown = row.placed.iter().map(|p| points::join(p, &log, &conversation)).collect();
                        match &log {
                            Err(e) => reasons.push(format!("the App could not read this conversation's records: {e}")),
                            Ok(reading) => {
                                reasons.extend(reading.inventory_reasons());
                                if reading.missing && !row.placed.is_empty() { reasons.push("the points log was not found in this project's records".into()); }
                                let named: Vec<&Value> = row.placed.iter().map(|p| &p["point"]).collect();
                                for &i in reading.for_thread(&row.thread) {
                                    let body = &reading.lines[i].entry["body"];
                                    if !conversation.names(body) || named.contains(&&body["point"]) { continue; }
                                    let point = body["point"].as_str().unwrap_or_default();
                                    match reading.soundness(i) {
                                        Ok(()) => reasons.push(match row.pending.iter().find(|(p, _)| p == point) {
                                            Some((_, why)) => format!("point {point} is in the App's records, but its pointer in this conversation could not be saved ({why}); the App completes it before a later placement in this conversation or when the conversation is resumed"),
                                            None => format!("point {point} is in the App's records without its pointer in this conversation; the App completes it before a later placement in this conversation or when the conversation is resumed"),
                                        }),
                                        Err(why) => reasons.push(format!("a record naming this conversation could not be established ({why})")),
                                    }
                                }
                                for (point, _) in &row.pending { if named.iter().any(|n| *n == point.as_str()) { resolved_pending.push((row.thread.clone(), point.clone())); } }
                                for mark in &row.uncertain {
                                    match reading.for_call(&mark.source).as_slice() {
                                        [i] if reading.soundness(*i).is_ok() => resolved_uncertain.push(mark.source.clone()),
                                        [] if reading.whole() => {
                                            resolved_uncertain.push(mark.source.clone());
                                            later_refused.push((row.thread.clone(), json!({"reason":"The App has since read this conversation's records whole: the call whose recording it could not establish was not recorded.","at":crate::util::now_rfc3339()})));
                                            refused.push(later_refused.last().unwrap().1.clone());
                                        }
                                        _ => reasons.push(mark.reason.clone()),
                                    }
                                }
                                checked_threads.push(row.thread.clone());
                            }
                        }
                        if log.is_err() { reasons.extend(row.uncertain.iter().map(|m| m.reason.clone())); reasons.extend(row.unchecked.iter().cloned()); }
                    }
                }
            }
            json!({"generation":generation,"threadId":row.thread,"offer":offer,
                "reading":{"whole":reasons.is_empty(),"reasons":reasons},"points":shown,"refused":refused})
        }).collect();
        if !(resolved_pending.is_empty() && resolved_uncertain.is_empty() && checked_threads.is_empty()) {
            let mut i = self.inner.0.lock().unwrap();
            i.points.pending.retain(|(_, t, p, _)| !resolved_pending.iter().any(|(rt, rp)| rt == t && rp == p));
            i.points.uncertain.retain(|u| !resolved_uncertain.contains(&u.source));
            i.points.unchecked.retain(|(g, t, _)| !(*g == generation && checked_threads.contains(t)));
            for (thread, entry) in later_refused { i.points.refused.push((generation.clone(), thread, entry)); }
        }
        json!(views)
    }
}

#[cfg(test)]
#[path = "hosting_points_tests.rs"]
mod tests;
