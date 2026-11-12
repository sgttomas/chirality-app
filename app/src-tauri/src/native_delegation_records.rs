//! DEL-06-01: the App's record of what it observes of Codex's native
//! delegation. Three facts, each from its own source and none inferred from
//! another: a dispatch (a completed spawn item, received live, naming a new
//! child thread), the child's status as Codex last reported it, and the end of
//! observation. They are published through the same store-first, identical-line
//! writer as related conversations. A dispatch establishes the child and its
//! parent only; no work done, return, review or integration follows from it.
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
    /// Children this session recorded in a generation, so that the end of
    /// their observation is recorded once it is observed.
    watched: BTreeMap<String, Value>,
    /// Observations left unrecorded because their conversation's folder is
    /// not the selected project, or is not known. Decided once per key.
    outside: BTreeSet<String>,
    /// The project and live sources whose earlier sessions were read for
    /// unended children. Their stored lines do not change within a session.
    relaunch_read: Option<String>,
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
    let brief = crate::fleet_records::validate_line(&bytes).ok().filter(|r| r["kind"] == "brief")
        .and_then(|r| r["body"]["briefId"].as_str().map(str::to_owned));
    let current = crate::util::sha256_hex(&bytes);
    if &current == referenced {
        match brief {
            Some(brief) => json!({"state":"brief referenced","brief":brief,"briefFile":file,"briefContent":identity(&bytes)}),
            None => unresolved("the referenced file is not a readable brief record", &references),
        }
    } else {
        let mut value = json!({"state":"brief referenced; content does not match the reference","briefFile":file,
            "referencedContent":{"method":crate::util::FILE_IDENTITY_METHOD,"value":referenced},"currentContent":identity(&bytes)});
        if let Some(brief) = brief {
            value["brief"] = json!(brief);
        }
        value
    }
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
    fn delegation_limit(&mut self, reason: String) {
        if !self.limits.contains(&reason) {
            self.limits.push(reason);
        }
    }
    /// Whether the fact was taken for recording. An observation whose
    /// recording context is unavailable (no attached store, a changed project
    /// link, a closed project) is left for a later tick, which finds it in the
    /// same view; it is neither dropped nor recorded under another context.
    fn delegation_fact(&mut self, key: String, context: SourceContext, kind: &str, body: Value) -> bool {
        match fact(context, kind, body) {
            Ok(pending) if pending.permanent.is_some() => {
                self.delegation_limit(format!("Native delegation observation ({kind}) waits to be recorded: {}", pending.permanent.unwrap()));
                false
            }
            Ok(mut pending) => {
                settle(&mut pending);
                self.facts.insert(key, pending);
                true
            }
            Err(reason) => {
                self.delegation_limit(format!("Native delegation observation ({kind}) not recorded: {reason}"));
                false
            }
        }
    }
    /// One reading of the native views the record tick received. `freeze`
    /// captures the recording context of a generation; `cause` says how a
    /// generation's observation ended, or `None` while that is not yet known.
    pub(super) fn observe_delegation_views(
        &mut self,
        project: Option<&Path>,
        views: &[Value],
        freeze: &mut dyn FnMut(&Value) -> SourceContext,
        cause: &dyn Fn(&Value) -> Option<&'static str>,
    ) {
        let Some(project) = project.and_then(|p| p.canonicalize().ok()) else { return };
        let mut live = BTreeMap::new();
        for view in views {
            let generation = &view["generation"];
            let Some(home) = generation["home"].as_str().filter(|_| crate::recovery::generation_ref(generation).is_ok()) else { continue };
            let mut context: Option<SourceContext> = None;
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
                    let context = context.get_or_insert_with(|| freeze(generation)).clone();
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
                    if self.delegation_fact(dispatch, context, "dispatch_observed", body) {
                        self.delegation.watched.insert(key(json!(["ended", home, generation, child])), json!({"threadId":child,"generation":generation}));
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
                let slot = key(json!([home, generation, child]));
                if self.delegation.statuses.get(&slot).is_some_and(|last| last == status) {
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
                let context = context.get_or_insert_with(|| freeze(generation)).clone();
                let body = json!({"child":{"threadId":child,"generation":generation},"status":status,
                    "statusSource":"collabAgentToolCall.agentsStates","sourceItem":item_ref(row),
                    "nativeHome":context.native_home.as_ref().ok(),"typesPin":crate::hosting::DECLARED_PIN});
                if self.delegation_fact(observed, context, "child_observed", body) {
                    self.delegation.statuses.insert(slot, status.to_owned());
                    self.delegation.watched.insert(key(json!(["ended", home, generation, child])), json!({"threadId":child,"generation":generation}));
                }
            }
            // A closed view marks every descendant's observation ended.
            let ended: Vec<&str> = view["descendants"].as_array().into_iter().flatten()
                .filter(|node| node["observationEnded"] == true).filter_map(|node| node["threadId"].as_str()).collect();
            if ended.is_empty() {
                live.insert(home.to_owned(), generation["appSession"].clone());
            }
            for child in ended {
                let end = key(json!(["ended", home, generation, child]));
                if self.facts.contains_key(&end) || !self.delegation.watched.contains_key(&end) {
                    continue;
                }
                let Some(cause) = cause(generation) else { continue };
                let context = context.get_or_insert_with(|| freeze(generation)).clone();
                let last = self.delegation.statuses.get(&key(json!([home, generation, child]))).cloned();
                let body = json!({"child":self.delegation.watched[&end],"cause":cause,"lastObserved":last,"nativeHome":context.native_home.as_ref().ok()});
                self.delegation_fact(end, context, "observation_ended", body);
            }
        }
        if let Err(reason) = self.delegation_relaunch(&project, &live) {
            self.delegation_limit(format!("Earlier native delegation observations were not read for their end: {reason}"));
        }
    }
    /// A child recorded by an earlier App session, whose observation was never
    /// recorded as ended, is no longer observed by anyone once this session
    /// holds that home's Codex: an App-owned home is hosted by one App at a
    /// time. Its end is recorded with the cause "App relaunch" and the status
    /// last recorded, which says nothing of the child's outcome. Only this
    /// installation's stored lines are read: a line that entered by import is
    /// quoted evidence of another source and is given no end here. No native
    /// source is consulted.
    fn delegation_relaunch(&mut self, project: &Path, live: &BTreeMap<String, Value>) -> Result<(), String> {
        let read = key(json!([project.to_string_lossy(), live]));
        if live.is_empty() || self.delegation.relaunch_read.as_ref() == Some(&read) {
            return Ok(());
        }
        let scope = Scope::capture(project)?;
        crate::records_retention::check_write(&scope.dir.path)?;
        if crate::records_retention::terminal(&scope.dir.path)? {
            return Ok(());
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
        for (end, (child, native_home)) in children {
            let home = child["generation"]["home"].as_str().unwrap_or_default();
            if ended.contains(&end) || self.facts.contains_key(&end) || live.get(home).is_none_or(|session| *session == child["generation"]["appSession"]) {
                continue;
            }
            let activity = crate::records_retention::activity(&scope.project.path)?.ok_or("recording custody unavailable")?;
            let context = SourceContext { scope: Ok(scope.clone()), native_home: Ok(native_home.clone()), generation: child["generation"].clone(),
                activity: Some(Arc::new(activity)), custody_limit: None };
            let body = json!({"child":child,"cause":"App relaunch","lastObserved":statuses.get(&end),"nativeHome":native_home});
            self.delegation_fact(end, context, "observation_ended", body);
        }
        self.delegation.relaunch_read = Some(read);
        Ok(())
    }
}

#[cfg(test)]
impl Session {
    /// The relaunch reading alone, for a session that holds `home` under `app_session`.
    pub(crate) fn delegation_relaunch_for_test(&mut self, project: &Path, home: &str, app_session: &str) -> Result<(), String> {
        self.delegation_relaunch(project, &BTreeMap::from([(home.to_owned(), json!(app_session))]))
    }
}

#[cfg(test)]
#[path = "native_delegation_records_tests.rs"]
mod tests;
