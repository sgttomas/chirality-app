//! DEL-06-01: the App's record of what it observes of Codex's native
//! delegation. Three facts, each from its own source and none inferred from
//! another: a dispatch (a completed spawn item, received live, naming a new
//! child thread), the child's status as Codex last reported it, and the end of
//! observation. They are published through the same store-first, identical-line
//! writer as related conversations, in the order they were observed. A
//! dispatch establishes the child and its parent only; no work done, return,
//! review or integration follows from it. A session records the end only of
//! its own observation, on evidence it holds itself: nothing is ever recorded
//! about a child another session observed.
use super::{line, read_log, settle, validate_record, Pending, Session, SourceContext};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::path::Path;

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
    /// Facts not yet fully published, in the order they were observed. A
    /// later one is not written to the store while an earlier one is unwritten.
    order: Vec<String>,
    /// For each view, what it held when it was last read with nothing left
    /// waiting; an unchanged view is not read again.
    seen: BTreeMap<String, String>,
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
    // A file that is not a brief record ties nothing, whatever its digest.
    let Some(brief) = brief else {
        return unresolved("the referenced file is not a readable brief record", &references);
    };
    if &crate::util::sha256_hex(&bytes) == referenced {
        json!({"state":"brief referenced","brief":brief,"briefFile":file,"briefContent":identity(&bytes)})
    } else {
        json!({"state":"brief referenced; content does not match the reference","brief":brief,"briefFile":file,
            "referencedContent":{"method":crate::util::FILE_IDENTITY_METHOD,"value":referenced},"currentContent":identity(&bytes)})
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
    /// An observation whose recording context is unavailable (no attached
    /// store, a changed project link, a closed project) is left for a later
    /// tick, which finds it in the same view; it is neither dropped nor
    /// recorded under another context.
    fn delegation_fact(&mut self, key: String, context: SourceContext, kind: &str, body: Value) -> Taken {
        match fact(context, kind, body) {
            Ok(pending) if pending.permanent.is_some() => {
                self.delegation_limit(format!("Native delegation observation ({kind}) waits to be recorded: {}", pending.permanent.unwrap()));
                Taken::Waits
            }
            Ok(pending) => {
                self.facts.insert(key.clone(), pending);
                self.delegation.order.push(key);
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
    /// Publishes in the order observed. A fact the store does not yet hold
    /// stops everything after it, so that a delayed status is never written
    /// after the end of its own observation.
    pub(super) fn settle_delegation(&mut self) {
        let mut blocked = false;
        let mut owed = Vec::new();
        for key in std::mem::take(&mut self.delegation.order) {
            let Some(pending) = self.facts.get_mut(&key) else { continue };
            if !blocked {
                settle(pending);
                blocked = !pending.store_done;
            }
            if !(pending.store_done && pending.project_done && pending.events.iter().all(|e| e.store_done && e.project_done)) {
                owed.push(key);
            }
        }
        self.delegation.order = owed;
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
                    match self.delegation_fact(dispatch, context, "dispatch_observed", body) {
                        Taken::Recorded => {
                            self.delegation.watched.insert(key(json!(["ended", home, generation, child])), json!({"threadId":child,"generation":generation}));
                        }
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
                let slot = key(json!([home, generation, child]));
                // A status of a generation whose end this session recorded is not recorded after it.
                if self.facts.contains_key(&key(json!(["ended", home, generation, child]))) {
                    continue;
                }
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
                match self.delegation_fact(observed, context, "child_observed", body) {
                    Taken::Recorded => {
                        self.delegation.statuses.insert(slot, status.to_owned());
                        self.delegation.watched.insert(key(json!(["ended", home, generation, child])), json!({"threadId":child,"generation":generation}));
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
                let context = context.get_or_insert_with(|| freeze(generation)).clone();
                let last = self.delegation.statuses.get(&key(json!([home, generation, child]))).cloned();
                let body = json!({"child":self.delegation.watched[&end],"cause":cause,"lastObserved":last,"nativeHome":context.native_home.as_ref().ok()});
                if matches!(self.delegation_fact(end, context, "observation_ended", body), Taken::Waits) {
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
    /// At the App's own exit, this session's observation of every child it
    /// recorded ends. `resolve` gives the recording context of a generation
    /// and how its observation ended, or `None` where the session no longer
    /// holds that generation's home. Nothing is recorded for a child this
    /// session did not itself record.
    pub(super) fn end_own_delegation(&mut self, resolve: &mut dyn FnMut(&Value) -> Option<(SourceContext, &'static str)>) {
        for (end, child) in self.delegation.watched.clone() {
            if self.facts.contains_key(&end) {
                continue;
            }
            let Some((context, cause)) = resolve(&child["generation"]) else { continue };
            let last = self.delegation.statuses.get(&key(json!([child["generation"]["home"], child["generation"], child["threadId"]]))).cloned();
            let body = json!({"child":child,"cause":cause,"lastObserved":last,"nativeHome":context.native_home.as_ref().ok()});
            self.delegation_fact(end, context, "observation_ended", body);
        }
    }
}

#[cfg(test)]
#[path = "native_delegation_records_tests.rs"]
mod tests;
