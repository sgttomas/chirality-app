//! DEL-06-01: the App's record of what it observes of Codex's native
//! delegation. Three facts, each from its own source and none inferred from
//! another: a dispatch (a completed spawn item, received live, naming a new
//! child thread), the child's status as Codex last reported it, and the end of
//! observation. They are published through the same store-first, identical-line
//! writer as related conversations, in the order they were observed. A
//! dispatch establishes the child and its parent only; no work done, return,
//! review or integration follows from it. A session records the end of its
//! own observation, on evidence it holds itself, and one other end: at its
//! start it records the end, cause "App relaunch", of each observation an
//! earlier session of this App left without one, once the App ledger has
//! established that session ended ([`Session::end_earlier_observations`]).
//! Neither end says anything of the child's outcome.
use super::{line, published_at, read_log, rows, settle, validate_record, Pending, Scope, Session, SourceContext};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::path::Path;
use std::sync::Arc;

/// The one line by which a delegating agent's spawn prompt names its brief:
/// `Chirality-Brief: briefs/<file>.json sha256:<64 lowercase hex>`. The path is
/// relative to the project's fleet folder and the digest is of the file's
/// exact bytes. Nothing else in a prompt is read as a reference.
pub(crate) const BRIEF_REFERENCE: &str = "Chirality-Brief:";
const FLEET: &str = ".chirality/fleet";
const KINDS: [&str; 3] = ["dispatch_observed", "child_observed", "observation_ended"];

#[derive(Default)]
pub(super) struct State {
    /// Status last recorded this session for a child in a generation.
    statuses: BTreeMap<String, String>,
    /// The recording context frozen when a child was first recorded, for each
    /// child this session has recorded: a child is a thread in a home,
    /// whatever generation of Codex reports it. Every later fact of that
    /// child is published through this context, so the writer's own physical
    /// check applies to it; it is never captured afresh.
    contexts: BTreeMap<String, SourceContext>,
    /// Children this session recorded, in each generation it recorded them
    /// in, so that the end of that generation's observation is recorded once.
    watched: BTreeMap<String, Value>,
    /// Observations left unrecorded because their conversation's folder is
    /// not the selected project, or is not known. Decided once per key.
    outside: BTreeSet<String>,
    /// Facts not yet fully published, in the order they were observed, each
    /// with the child it concerns. A later fact of a child is not written to
    /// the store while an earlier fact of that child is unwritten.
    order: Vec<(String, String)>,
    /// For each view, what it held when it was last read with nothing left
    /// waiting; an unchanged view is not read again.
    seen: BTreeMap<String, String>,
    /// The reconciliation of earlier sessions' observations, once it has run
    /// to its end in this session: what it did, and the ends it took.
    reconciled: Option<(Value, Vec<String>)>,
    /// Why it has not yet run to its end; it is tried again at the next record tick.
    unreconciled: Option<String>,
}
enum Taken {
    Recorded,
    /// The recording context is unavailable; a later tick finds it again.
    Waits,
    Refused,
}
pub(super) fn is_delegation(record: &Value) -> bool {
    KINDS.contains(&record["kind"].as_str().unwrap_or(""))
}
/// The frozen context of a child already recorded, for one more fact of it:
/// the same physical project, store and identities, checked as the writer
/// checks them, with recording custody taken anew. Where that context no
/// longer holds, the result carries the reason and nothing can be written.
fn resume(original: &SourceContext) -> SourceContext {
    let mut context = original.clone();
    context.activity = None;
    if let Ok(scope) = &context.scope {
        let held = scope.check()
            .and_then(|()| crate::records_retention::check_write(&scope.dir.path))
            .and_then(|()| crate::records_retention::activity(&scope.project.path)?
                .ok_or_else(|| "original project activity custody unavailable".to_owned()));
        match held {
            Ok(lease) => context.activity = Some(Arc::new(lease)),
            Err(reason) => context.scope = Err(format!("the context this child was first recorded under no longer holds ({reason}); nothing is written of it under another")),
        }
    }
    context
}
/// The context to keep for a child: the one its first fact was recorded under, without the custody that fact held.
fn kept(context: &SourceContext) -> SourceContext {
    let mut context = context.clone();
    context.activity = None;
    context
}
fn child_slot(home: &str, child: &str) -> String {
    key(json!([home, child]))
}

fn key(parts: Value) -> String {
    parts.to_string()
}
fn identity(bytes: &[u8]) -> Value {
    json!({"method":crate::util::FILE_IDENTITY_METHOD,"value":crate::util::sha256_hex(bytes)})
}
fn brief_file(reference: &str) -> bool {
    reference.strip_prefix("briefs/").and_then(|name| name.strip_suffix(".json")).is_some_and(|stem| {
        !stem.is_empty() && stem.bytes().all(|b| b.is_ascii_alphanumeric() || matches!(b, b'.' | b'_' | b'-'))
    })
}

/// The association of one dispatch, from the prompt Codex supplied and the
/// brief file as it is now. A match shows which brief the prompt named and
/// what its bytes were, not that the child received or read it; a mismatch
/// shows only that the file's bytes are not those referenced, not which of
/// the two changed. An absent prompt, an absent reference and a reference
/// that cannot be resolved are each recorded as such.
pub(super) fn associate(project: &Path, prompt: Option<&str>) -> Value {
    let unresolved = |reason: &str, references: &[(String, String)]| {
        json!({"state":"brief reference not resolved","reason":reason,
            "references":references.iter().map(|(file,digest)|json!({"briefFile":file,
                "referencedContent":{"method":crate::util::FILE_IDENTITY_METHOD,"value":digest}})).collect::<Vec<_>>()})
    };
    let mut references: Vec<(String, String)> = Vec::new();
    let mut malformed = false;
    for line in prompt.unwrap_or("").lines() {
        let Some(rest) = line.trim().strip_prefix(BRIEF_REFERENCE) else { continue };
        let mut parts = rest.split_whitespace();
        match (parts.next(), parts.next().and_then(|d| d.strip_prefix("sha256:")), parts.next()) {
            (Some(file), Some(digest), None)
                if digest.len() == 64 && digest.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)) =>
            {
                let reference = (file.to_owned(), digest.to_owned());
                if !references.contains(&reference) {
                    references.push(reference);
                }
            }
            _ => malformed = true,
        }
    }
    if malformed {
        return unresolved("a brief reference line in the prompt is malformed", &references);
    }
    let [(file, referenced)] = references.as_slice() else {
        return if references.is_empty() {
            json!({"state":"no brief reference"})
        } else {
            unresolved("the prompt names more than one brief", &references)
        };
    };
    if !brief_file(file) {
        return unresolved("the reference is not a brief file path in the fleet folder", &references);
    }
    let path = project.join(FLEET).join(file);
    if let Err(reason) = crate::storage::check_path(&path) {
        return unresolved(&format!("the referenced brief file was not read: {reason}"), &references);
    }
    match std::fs::symlink_metadata(&path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            return unresolved("the referenced brief file is not present", &references)
        }
        Err(e) => return unresolved(&format!("the referenced brief file was not read: {e}"), &references),
        Ok(_) => {}
    }
    let bytes = match read_log(&path) {
        Ok(bytes) => bytes,
        Err(reason) => return unresolved(&format!("the referenced brief file was not read: {reason}"), &references),
    };
    // What the brief record itself states, read from the bytes whose identity
    // is recorded: this is the tie, fixed now and never worked out again.
    let brief = crate::fleet_records::validate_line(&bytes).ok().filter(|r| r["kind"] == "brief"
        && r["recordId"].is_string() && r["undertaking"].is_string() && r["body"]["workItem"].is_string() && r["body"]["briefId"].is_string());
    // A file that is not a brief record ties nothing, whatever its digest.
    let Some(brief) = brief else {
        return unresolved("the referenced file is not a readable brief record", &references);
    };
    let mut association = json!({"brief":brief["body"]["briefId"],"briefRecord":brief["recordId"],
        "workItem":brief["body"]["workItem"],"undertaking":brief["undertaking"],"briefFile":file});
    if &crate::util::sha256_hex(&bytes) == referenced {
        association["state"] = json!("brief referenced");
        association["briefContent"] = identity(&bytes);
    } else {
        association["state"] = json!("brief referenced; content does not match the reference");
        association["referencedContent"] = json!({"method":crate::util::FILE_IDENTITY_METHOD,"value":referenced});
        association["currentContent"] = identity(&bytes);
    }
    association
}

/// Whether the conversation an item was received in runs in the selected
/// project. A sub-agent's thread is placed by the conversation the App
/// started or resumed above it; a folder that is not known places nothing.
fn in_project(view: &Value, thread: &str, project: &Path) -> Result<(), &'static str> {
    let mut current = thread.to_owned();
    for _ in 0..=view["descendants"].as_array().map_or(0, Vec::len) {
        if let Some(row) = view["hostThreads"].as_array().into_iter().flatten().rev().find(|row| row["threadId"] == current.as_str()) {
            let folder = row["cwd"].as_str().ok_or("its conversation's folder is not known")?;
            return if Path::new(folder).canonicalize().ok().as_deref() == Some(project) {
                Ok(())
            } else {
                Err("its conversation's folder is not the selected project")
            };
        }
        match view["descendants"].as_array().into_iter().flatten().find(|node| node["threadId"] == current.as_str())
            .and_then(|node| node["parentThreadId"].as_str())
        {
            Some(parent) => current = parent.to_owned(),
            None => break,
        }
    }
    Err("its conversation's folder is not known")
}

fn fact(context: SourceContext, kind: &str, body: Value) -> Result<Pending, String> {
    let record = json!({"format":"chirality.fleet.record","formatVersion":"0.2","observationId":crate::util::opaque_id("fl:app:")?,
        "kind":kind,"recorder":{"kind":"App","identity":"app-writer:local"},"observedAt":crate::util::now_rfc3339(),"body":body});
    let permanent = context.scope.as_ref().err().cloned()
        .or_else(|| context.native_home.as_ref().err().cloned())
        .or_else(|| context.custody_limit.clone());
    if permanent.is_none() {
        validate_record(&record)?;
    }
    Ok(Pending { bytes: line(&record)?, record, context, store_done: false, project_done: false, first_failure: [None, None], events: vec![], permanent })
}

impl Session {
    /// The one place a recording context is decided for a fact of a child,
    /// whichever fact it is and whichever generation reports it. A child this
    /// session has ever recorded gets its kept context, resumed; only a child
    /// never recorded gets a fresh one, from `capture`. Nothing else in this
    /// module captures or chooses a context.
    fn context_of(&self, home: &str, child: &str, capture: &mut dyn FnMut() -> Option<SourceContext>) -> SourceContext {
        match self.delegation.contexts.get(&child_slot(home, child)) {
            Some(first) => resume(first),
            None => capture().unwrap_or_else(|| {
                let none = "no recording context was kept for this child; nothing is written of it";
                SourceContext { scope: Err(none.into()), native_home: Err(none.into()), generation: Value::Null, activity: None, custody_limit: None }
            }),
        }
    }
    /// A fact of a child was taken for recording under `context`: the child's
    /// first context is kept, and its generation is watched for its end.
    fn recorded_child(&mut self, home: &str, generation: &Value, child: &str, context: SourceContext) {
        self.delegation.contexts.entry(child_slot(home, child)).or_insert(context);
        self.delegation.watched.entry(key(json!(["ended", home, generation, child]))).or_insert_with(|| json!({"threadId":child,"generation":generation}));
    }
    fn delegation_limit(&mut self, reason: String) {
        if !self.limits.contains(&reason) {
            self.limits.push(reason);
        }
    }
    /// An observation whose recording context is unavailable (no attached
    /// store, a changed project link, a closed project, or a context that no
    /// longer holds) is left for a later tick, which finds it in the same
    /// view; it is neither dropped nor recorded under another context.
    fn delegation_fact(&mut self, key: String, of: String, context: SourceContext, kind: &str, body: Value) -> Taken {
        match fact(context, kind, body) {
            Ok(pending) if pending.permanent.is_some() => {
                self.delegation_limit(format!("Native delegation observation ({kind}) waits to be recorded: {}", pending.permanent.unwrap()));
                Taken::Waits
            }
            Ok(pending) => {
                self.facts.insert(key.clone(), pending);
                self.delegation.order.push((of, key));
                self.settle_delegation();
                Taken::Recorded
            }
            Err(reason) => {
                self.delegation_limit(format!("Native delegation observation ({kind}) not recorded: {reason}"));
                self.delegation.outside.insert(key);
                Taken::Refused
            }
        }
    }
    /// Publishes each child's facts in the order observed. A fact the store
    /// does not yet hold stops every later fact of that child, so that a
    /// delayed status is never written after the end of its own observation.
    pub(super) fn settle_delegation(&mut self) {
        let mut blocked = BTreeSet::new();
        let mut owed = Vec::new();
        for (of, key) in std::mem::take(&mut self.delegation.order) {
            let Some(pending) = self.facts.get_mut(&key) else { continue };
            if !blocked.contains(&of) {
                settle(pending);
                if !pending.store_done {
                    blocked.insert(of.clone());
                }
            }
            if !(pending.store_done && pending.project_done && pending.events.iter().all(|e| e.store_done && e.project_done)) {
                owed.push((of, key));
            }
        }
        self.delegation.order = owed;
    }
    /// One reading of the native views the record tick received. `freeze`
    /// captures the recording context of a generation, for a child not yet
    /// recorded; `cause` says how a generation's observation ended, or `None`
    /// while that is not yet known.
    pub(super) fn observe_delegation_views(
        &mut self,
        project: Option<&Path>,
        views: &[Value],
        freeze: &mut dyn FnMut(&Value) -> SourceContext,
        cause: &dyn Fn(&Value) -> Option<&'static str>,
    ) {
        let Some(project) = project.and_then(|p| p.canonicalize().ok()) else { return };
        for view in views {
            let generation = &view["generation"];
            let Some(home) = generation["home"].as_str().filter(|_| crate::recovery::generation_ref(generation).is_ok()) else { continue };
            // A view that has received nothing since it was last read through,
            // with nothing left waiting, holds nothing new to record.
            let slot = key(json!([home, generation]));
            let held = key(json!([view["position"], view["items"].as_array().map_or(0, Vec::len),
                view["descendants"].as_array().into_iter().flatten().filter(|node| node["observationEnded"] == true).count(),
                view["hostThreads"].as_array().map_or(0, Vec::len)]));
            if self.delegation.seen.get(&slot) == Some(&held) {
                continue;
            }
            let mut waiting = false;
            let mut fresh: Option<SourceContext> = None;
            let mut collab: Vec<(u64, &Value)> = view["items"].as_array().into_iter().flatten()
                .filter(|row| row["native"]["type"] == "collabAgentToolCall" && row["standing"] == "live-observed" && row["receipt"]["generation"] == *generation)
                .filter_map(|row| row["receipt"]["completed"].as_u64().max(row["receipt"]["started"].as_u64()).map(|position| (position, row)))
                .collect();
            collab.sort_by_key(|(position, _)| *position);
            let item_ref = |row: &Value| json!({"threadId":row["threadId"],"turnId":row["turnId"],"itemId":row["native"]["id"]});
            for (_, row) in &collab {
                let native = &row["native"];
                let (Some(position), Some(sender), Some(thread)) = (row["receipt"]["completed"].as_u64(), native["senderThreadId"].as_str().filter(|s| !s.is_empty()), row["threadId"].as_str()) else { continue };
                if native["tool"] != "spawnAgent" || native["status"] != "completed" {
                    continue;
                }
                for child in native["receiverThreadIds"].as_array().into_iter().flatten().filter_map(Value::as_str).filter(|id| !id.is_empty() && *id != sender) {
                    let dispatch = key(json!(["dispatch", home, child]));
                    if self.facts.contains_key(&dispatch) || self.delegation.outside.contains(&dispatch) {
                        continue;
                    }
                    if let Err(reason) = in_project(view, thread, &project) {
                        self.delegation.outside.insert(dispatch);
                        self.delegation_limit(format!("A native dispatch was observed and not recorded in this project: {reason}."));
                        continue;
                    }
                    let context = self.context_of(home, child, &mut || Some(fresh.get_or_insert_with(|| freeze(generation)).clone()));
                    let prompt = native["prompt"].as_str();
                    let body = json!({"mechanism":"Codex native subagent",
                        "parent":{"threadId":sender,"generation":generation},"child":{"threadId":child,"generation":generation},
                        "parentSource":"collabAgentToolCall.senderThreadId","nativeHome":context.native_home.as_ref().ok(),
                        "spawnItem":item_ref(row),
                        "spawnPrompt":match prompt {
                            Some(text) => json!({"state":"supplied","content":identity(text.as_bytes()),"bytes":text.len()}),
                            None => json!({"state":"not supplied"}),
                        },
                        "association":associate(&project, prompt),
                        "observation":{"source":"item/completed notification, received live","position":position},
                        "typesPin":crate::hosting::DECLARED_PIN});
                    let keep = kept(&context);
                    match self.delegation_fact(dispatch, child_slot(home, child), context, "dispatch_observed", body) {
                        Taken::Recorded => self.recorded_child(home, generation, child, keep),
                        Taken::Waits => waiting = true,
                        Taken::Refused => {}
                    }
                }
            }
            // The status Codex last reported for each child, by receipt order.
            let mut latest: BTreeMap<&str, (&Value, &str)> = BTreeMap::new();
            for (_, row) in &collab {
                for (child, state) in row["native"]["agentsStates"].as_object().into_iter().flatten() {
                    if let Some(status) = state["status"].as_str().filter(|s| !s.is_empty()) {
                        latest.insert(child.as_str(), (*row, status));
                    }
                }
            }
            for (child, (row, status)) in latest {
                let recorded = key(json!([home, generation, child]));
                let end = key(json!(["ended", home, generation, child]));
                // A status of a generation whose end this session recorded is not recorded after it.
                if self.facts.contains_key(&end) {
                    continue;
                }
                if self.delegation.statuses.get(&recorded).is_some_and(|last| last == status) {
                    continue;
                }
                let observed = key(json!(["status", home, generation, child, item_ref(row), status]));
                if self.facts.contains_key(&observed) || self.delegation.outside.contains(&observed) {
                    continue;
                }
                let placed = if self.delegation.outside.contains(&key(json!(["dispatch", home, child]))) {
                    Err("its dispatch was observed outside the selected project")
                } else {
                    row["threadId"].as_str().ok_or("its conversation is not identified").and_then(|thread| in_project(view, thread, &project))
                };
                if placed.is_err() {
                    self.delegation.outside.insert(observed);
                    continue;
                }
                let context = self.context_of(home, child, &mut || Some(fresh.get_or_insert_with(|| freeze(generation)).clone()));
                let body = json!({"child":{"threadId":child,"generation":generation},"status":status,
                    "statusSource":"collabAgentToolCall.agentsStates","sourceItem":item_ref(row),
                    "nativeHome":context.native_home.as_ref().ok(),"typesPin":crate::hosting::DECLARED_PIN});
                let keep = kept(&context);
                match self.delegation_fact(observed, child_slot(home, child), context, "child_observed", body) {
                    Taken::Recorded => {
                        self.delegation.statuses.insert(recorded, status.to_owned());
                        self.recorded_child(home, generation, child, keep);
                    }
                    Taken::Waits => waiting = true,
                    Taken::Refused => {}
                }
            }
            // A closed view marks every descendant's observation ended.
            let ended: Vec<&str> = view["descendants"].as_array().into_iter().flatten()
                .filter(|node| node["observationEnded"] == true).filter_map(|node| node["threadId"].as_str()).collect();
            for child in ended {
                let end = key(json!(["ended", home, generation, child]));
                if self.facts.contains_key(&end) || !self.delegation.watched.contains_key(&end) {
                    continue;
                }
                let Some(cause) = cause(generation) else {
                    waiting = true;
                    continue;
                };
                if matches!(self.end_watched(&end, cause), Taken::Waits) {
                    waiting = true;
                }
            }
            if waiting {
                self.delegation.seen.remove(&slot);
            } else {
                self.delegation.seen.insert(slot, held);
            }
        }
    }
    /// The end of this session's observation of one child it recorded,
    /// through the context that child was first recorded under.
    fn end_watched(&mut self, end: &str, cause: &str) -> Taken {
        let child = self.delegation.watched[end].clone();
        let (home, thread) = (child["generation"]["home"].as_str().unwrap_or_default().to_owned(), child["threadId"].as_str().unwrap_or_default().to_owned());
        // An end is only ever of a child already recorded: there is nothing to capture.
        let context = self.context_of(&home, &thread, &mut || None);
        let last = self.delegation.statuses.get(&key(json!([home, child["generation"], thread]))).cloned();
        let body = json!({"child":child,"cause":cause,"lastObserved":last,"nativeHome":context.native_home.as_ref().ok()});
        self.delegation_fact(end.to_owned(), child_slot(&home, &thread), context, "observation_ended", body)
    }
    /// The session's start, for the selected project, run at each record tick
    /// until it has run to its end: for each child an earlier App session of
    /// this App recorded and left without an end of its observation, this
    /// session records that end, with the cause "App relaunch" and the status
    /// last recorded. It is this session's observation that the earlier one is
    /// over, and says nothing of the child's outcome.
    ///
    /// `sessions` is this session and the sessions the App ledger established
    /// as ended at this session's start ([`crate::recovery::established_ended_sessions`]).
    /// Only a child of one of those is ended. A session not among them (still
    /// running, another App's, or of liveness not established) is not ended by
    /// this session, is not looked at again in it, and is stated as a limit.
    /// Only this installation's stored lines are read: the store's copy governs,
    /// and a line that entered by import is quoted evidence, given no end. No
    /// native source is consulted.
    pub(super) fn end_earlier_observations(&mut self, project: Option<&Path>, sessions: &dyn Fn() -> Result<(String, BTreeSet<String>), String>) {
        if self.delegation.reconciled.is_some() {
            return;
        }
        let sessions = sessions();
        let Some(project) = project.and_then(|p| p.canonicalize().ok()) else {
            self.delegation.reconciled = Some((json!({"state":"not needed","reason":"no selected App project"}), vec![]));
            return;
        };
        let (current, ended) = match sessions {
            Ok(sessions) => sessions,
            Err(reason) => {
                self.delegation.reconciled = Some((json!({"state":"unavailable",
                    "limit":format!("An earlier App session's end could not be established ({reason}); this session records no end of an earlier session's observations, and they are left as last recorded")}), vec![]));
                return;
            }
        };
        match self.reconcile(&project, &current, &ended) {
            Ok(done) => {
                self.delegation.reconciled = Some(done);
                self.delegation.unreconciled = None;
            }
            Err(reason) => self.delegation.unreconciled = Some(reason),
        }
    }
    fn reconcile(&mut self, project: &Path, current: &str, established: &BTreeSet<String>) -> Result<(Value, Vec<String>), String> {
        let scope = Scope::capture(project)?;
        crate::records_retention::check_write(&scope.dir.path)?;
        if crate::records_retention::terminal(&scope.dir.path)? {
            return Ok((json!({"state":"not needed","reason":"the project's records are closed"}), vec![]));
        }
        let bytes = read_log(&published_at(&scope, 0))?;
        let imported = crate::records_store::package::quoted_prefix(&scope.dir.path, &format!("fleet/{}", super::LOG), &bytes)?;
        let stored = rows(&bytes, true)?;
        scope.check()?;
        let mut children: BTreeMap<String, (Value, Value)> = BTreeMap::new();
        let mut statuses: BTreeMap<String, String> = BTreeMap::new();
        let mut ended = BTreeSet::new();
        let mut start = 0u64;
        for (row, line) in &stored {
            let local = start >= imported;
            start += line.len() as u64;
            if !local || row["formatVersion"] != "0.2" || !KINDS.contains(&row["kind"].as_str().unwrap_or("")) {
                continue;
            }
            let child = &row["body"]["child"];
            let (Some(home), Some(thread)) = (child["generation"]["home"].as_str(), child["threadId"].as_str()) else { continue };
            let end = key(json!(["ended", home, child["generation"], thread]));
            match row["kind"].as_str() {
                Some("observation_ended") => {
                    ended.insert(end);
                }
                Some(kind) => {
                    if kind == "child_observed" {
                        statuses.insert(end.clone(), row["body"]["status"].as_str().unwrap_or_default().to_owned());
                    }
                    children.entry(end).or_insert_with(|| (child.clone(), row["body"]["nativeHome"].clone()));
                }
                None => {}
            }
        }
        let mut taken = Vec::new();
        let mut not_established = BTreeSet::new();
        for (end, (child, native_home)) in children {
            let session = child["generation"]["appSession"].as_str().unwrap_or_default().to_owned();
            if ended.contains(&end) || self.facts.contains_key(&end) || session == current {
                continue;
            }
            if !established.contains(&session) {
                not_established.insert(session);
                continue;
            }
            let (home, thread) = (child["generation"]["home"].as_str().unwrap_or_default().to_owned(), child["threadId"].as_str().unwrap_or_default().to_owned());
            let activity = crate::records_retention::activity(&scope.project.path)?.ok_or("recording custody unavailable")?;
            let context = SourceContext { scope: Ok(scope.clone()), native_home: Ok(native_home.clone()), generation: child["generation"].clone(),
                activity: Some(Arc::new(activity)), custody_limit: None };
            let body = json!({"child":child,"cause":"App relaunch","lastObserved":statuses.get(&end),"nativeHome":native_home});
            match self.delegation_fact(end.clone(), child_slot(&home, &thread), context, "observation_ended", body) {
                Taken::Recorded => taken.push(end),
                Taken::Waits | Taken::Refused => {
                    return Err(self.limits.last().cloned().unwrap_or_else(|| "an earlier observation's end could not be taken for recording".into()));
                }
            }
        }
        let mut done = json!({"state":"ran"});
        if !not_established.is_empty() {
            done["limit"] = json!("An earlier App session's end could not be established, so this session records no end of that session's observations of delegated children; they are left as last recorded");
            done["sessionsNotEstablished"] = json!(not_established);
        }
        Ok((done, taken))
    }
    /// What the reconciliation has done in this session, in words a reader of
    /// the App's view is shown beside the records. Memory only.
    pub(super) fn reconciliation_status(&self) -> Value {
        match (&self.delegation.reconciled, &self.delegation.unreconciled) {
            (Some((done, taken)), _) => {
                let mut status = done.clone();
                let unwritten = taken.iter().filter_map(|end| self.facts.get(end)).find(|p| !(p.store_done && p.project_done));
                match unwritten {
                    Some(pending) if done["state"] == "ran" => {
                        status["state"] = json!("unavailable");
                        status["limit"] = json!(format!("The end of an earlier App session's observation of a delegated child is not yet written ({}); retried at the next record tick",
                            pending.first_failure.iter().flatten().next().cloned().unwrap_or_else(|| "write not yet attempted".into())));
                    }
                    _ if done["state"] == "ran" => status["state"] = json!("recorded"),
                    _ => {}
                }
                status["endsRecorded"] = json!(taken.len());
                status
            }
            (None, Some(reason)) => json!({"state":"unavailable","limit":format!("The end of an earlier App session's observations of delegated children could not be recorded ({reason}); retried at the next record tick")}),
            (None, None) => json!({"state":"pending","limit":"Earlier App sessions' observations of delegated children have not yet been reconciled in this session"}),
        }
    }
    /// At the App's own exit, this session's observation of every child it
    /// recorded ends. `cause` says how a generation's observation ended, or
    /// `None` where the session no longer holds that generation's home.
    /// Nothing is recorded for a child this session did not itself record.
    pub(super) fn end_own_delegation(&mut self, cause: &dyn Fn(&Value) -> Option<&'static str>) {
        let unended: Vec<(String, Value)> = self.delegation.watched.iter()
            .filter(|(end, _)| !self.facts.contains_key(*end)).map(|(end, child)| (end.clone(), child["generation"].clone())).collect();
        for (end, generation) in unended {
            if let Some(cause) = cause(&generation) {
                self.end_watched(&end, cause);
            }
        }
    }
}

#[cfg(test)]
#[path = "native_delegation_records_tests.rs"]
mod tests;
