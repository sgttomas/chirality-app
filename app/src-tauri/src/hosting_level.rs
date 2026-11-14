//! DEL-01-01, DEL-01-02, DEL-04-02, PRD V4-AUT-06: the Host's side of the person's permission level beyond the
//! frame builder in `hosting.rs`: the checks before a Codex start, the checks each time a level is sent, the
//! level's App ledger entries (`level_chosen`, `level_sent`, `level_reported`), the reading of the recorded level at
//! launch, the level's status, and the lasting rules each App-owned Codex home holds.
//!
//! The level is the person's own setting. Nothing here is an act-control act or a human-act record, and no entry
//! carries an actor. The only paths that change the level in force in production are [`Host::choose_level`] (the
//! App's `set_level` command, after the person's native confirmation) and [`Host::read_levels_at_launch`].
use super::*;
use crate::codex_level::{self as cl, Level, Target};
use std::path::Path;

/// One recorded choice of the person: its ledger entry, when they confirmed it, and the level.
#[derive(Clone, Debug)]
pub(crate) struct Chosen {
    pub(crate) entry: String,
    pub(crate) at: String,
    pub(crate) level: &'static Level,
}

/// Where a choice applies (the `set_level` command's scope).
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum LevelScope {
    /// New conversations, and every conversation without a level of its own from its next request.
    Default,
    /// One conversation of this Host's home.
    Conversation(String),
    /// The conversation the next start or fork creates.
    NewConversation,
}

/// The App's own folders and the start's working folder, as the send-time checks need them.
#[derive(Clone, Debug, Default)]
pub(crate) struct Places {
    pub(crate) app_data: Option<PathBuf>,
    /// This Host's Codex home and probe home.
    pub(crate) own_homes: Vec<PathBuf>,
    /// The other App-owned Codex homes, as the App's home router publishes them.
    pub(crate) other_homes: Vec<PathBuf>,
    /// The folder Codex was started in: a conversation's project when nothing names another.
    pub(crate) process_cwd: Option<PathBuf>,
    /// `home_identity` of this Host's configured Codex home: the ledger's `home`.
    pub(crate) home_identity: Option<String>,
    /// This Host's Codex home, made absolute where the child resolves it.
    pub(crate) codex_home: Option<PathBuf>,
}

#[derive(Default)]
pub(crate) struct LevelState {
    pub(crate) places: Option<Places>,
    /// Homes published before this Host started (kept for the start that sets `places`).
    pub(crate) published_homes: Vec<PathBuf>,
    /// `levelStartRefusal`: why the last start of Codex was refused by the level's start checks.
    pub(crate) start_refusal: Option<Value>,
    pub(crate) default_chosen: Option<Chosen>,
    pub(crate) thread_chosen: HashMap<String, Chosen>,
    pub(crate) new_chosen: Option<Chosen>,
    /// Every recorded choice by entry id, so a request's bound `chosen` can be followed.
    pub(crate) by_entry: HashMap<String, Chosen>,
    /// A new-conversation choice's `level_chosen`, written when the start or fork reply names the conversation.
    pub(crate) deferred: HashMap<String, Value>,
    /// A new conversation's `level_sent`, held with its deferred choice until the reply names the conversation.
    pub(crate) deferred_sent: HashMap<String, Value>,
    /// (conversation, chosen entry) to the `level_sent` entry written for it: once per conversation per choice.
    pub(crate) sent_keys: HashMap<(String, String), String>,
    /// A start's or fork's `level_sent` entry by request key, until the reply names the conversation.
    pub(crate) sent_by_request: HashMap<String, String>,
    /// What was last sent to each conversation (`threads[].level.sent`), and a start's or fork's by request key.
    pub(crate) last_sent: HashMap<String, Value>,
    pub(crate) request_sent: HashMap<String, Value>,
    /// What Codex last reported for each conversation (`threads[].level.reported`).
    pub(crate) reported: HashMap<String, Value>,
    /// The cause a level was last not sent for each conversation (`threads[].level.refused`).
    pub(crate) refused: HashMap<String, Value>,
    /// The last refusal of any send, a start's included (`levelSendRefusal`).
    pub(crate) last_refusal: Option<Value>,
    /// What the launch read found (`levelLaunchRead`).
    pub(crate) launch: Value,
    /// This Host's home's lasting rules as last read.
    pub(crate) rules: Option<Value>,
}

impl Places {
    /// The unit tests' Host: a working folder and no App folders, so a level is checked and sent.
    #[cfg(test)]
    pub(crate) fn for_test() -> Self {
        Places { process_cwd: Some(PathBuf::from("/invented")), ..Default::default() }
    }
    fn protected(&self) -> Vec<(&'static str, PathBuf)> {
        let mut out: Vec<(&'static str, PathBuf)> = self.app_data.iter().map(|d| ("app-data", d.clone())).collect();
        for home in self.own_homes.iter().chain(self.other_homes.iter()) {
            if !home.as_os_str().is_empty() && !out.iter().any(|(_, p)| p == home) {
                out.push(("codex-home", home.clone()));
            }
        }
        out
    }
}

/// Whether an answer adds a lasting rule (an exec-policy or a network-policy amendment).
pub(crate) fn adds_lasting_rule(answer: &Value) -> bool {
    match answer {
        Value::Object(o) => o.iter().any(|(k, v)| k == "acceptWithExecpolicyAmendment" || k == "applyNetworkPolicyAmendment" || adds_lasting_rule(v)),
        Value::Array(a) => a.iter().any(adds_lasting_rule),
        Value::String(s) => s == "acceptWithExecpolicyAmendment" || s == "applyNetworkPolicyAmendment",
        _ => false,
    }
}

fn takes_effect_now(i: &Inner, thread: Option<&str>) -> &'static str {
    match thread {
        Some(t) if Host::current_live_turn(i, t).is_some() => "from-next-turn",
        _ => "now",
    }
}

fn chosen_view(chosen: Option<&Chosen>, level: Option<&'static Level>, scope: &str) -> Value {
    match (chosen, level) {
        (Some(c), _) => json!({"id": c.level.id, "dimensions": c.level.dimensions, "ledgerEntry": c.entry, "chosenAt": c.at, "scope": scope, "reading": "not-limited"}),
        (None, Some(level)) => json!({"id": level.id, "dimensions": level.dimensions, "ledgerEntry": null, "chosenAt": null, "scope": scope, "reading": "not-limited"}),
        (None, None) => Value::Null,
    }
}

impl Host {
    // ---- Start checks (item 3) ----

    /// Before every Codex start in an App-owned home: the home's path and `environments.toml`. A refusal is kept
    /// in `levelStartRefusal`, and its reason returned for `lastStartRefusal` (class "home").
    pub(super) fn level_start_check(&self, cfg: &HostConfig) -> Result<(), String> {
        let home = std::path::absolute(cfg.cwd.join(&cfg.codex_home)).unwrap_or_else(|_| cfg.cwd.join(&cfg.codex_home));
        let refusal = cl::start_refusal(&home);
        let mut i = self.inner.0.lock().unwrap();
        i.level.start_refusal = refusal.as_ref().map(cl::StartRefusal::status);
        match refusal {
            Some(r) => Err(r.reason()),
            None => Ok(()),
        }
    }

    /// The start admitted a spawn: the App folders, this Host's homes and the working folder, for the send-time
    /// checks, and the home's identity for the ledger.
    pub(super) fn level_places_at_start(i: &mut Inner, cfg: &HostConfig) {
        let absolute = |p: PathBuf| std::path::absolute(&p).unwrap_or(p);
        let codex_home = absolute(cfg.cwd.join(&cfg.codex_home));
        let other_homes = i.level.published_homes.clone();
        i.level.places = Some(Places {
            app_data: cfg.app_data.clone(),
            own_homes: vec![codex_home.clone(), absolute(cfg.probe_home.clone())],
            other_homes,
            process_cwd: Some(cfg.cwd.clone()),
            home_identity: Some(home_identity(&cfg.codex_home)),
            codex_home: Some(codex_home),
        });
    }

    /// The App's home router names every App-owned Codex home; each is protected from an edits level.
    pub(crate) fn publish_app_homes(&self, homes: Vec<PathBuf>) {
        let mut i = self.inner.0.lock().unwrap();
        if let Some(places) = i.level.places.as_mut() {
            places.other_homes = homes.clone();
        }
        i.level.published_homes = homes;
    }

    // ---- Send-time rules (item 4) ----

    /// The checks made each time a level is about to be sent: Codex's last report for the conversation (a turn is
    /// refused while it differs), then `codex_level::refusal` (the App's own folders by identity, the double quote in the project's path; the
    /// no-project folder exempt). A refusal writes nothing and is kept on the conversation.
    pub(super) fn level_send_check(i: &mut Inner, method: &str, built: &Value, level: &'static Level, target: &Target) -> Result<(), String> {
        let thread = match target {
            Target::Conversation(t) | Target::ForkOf(t) => Some(t.clone()),
            Target::New => None,
        };
        let row_cwd = |t: &str| i.threads.iter().rev().find(|r| r["threadId"] == t).and_then(|r| r["cwd"].as_str()).map(PathBuf::from);
        let outcome: Result<(), Value> = (|| {
            // unit-b-design 1.3: a reply that reported other than the level sent blocks the next turn, and says why,
            // until a start, resume or fork reply agrees.
            if method == "turn/start" {
                if let Some(report) = thread.as_deref().and_then(|t| i.level.reported.get(t)) {
                    if report["agreement"] == "differs" {
                        return Err(json!({"refused": "codex-reported-another-level", "reported": report}));
                    }
                }
            }
            if !level.sandboxed() {
                return Ok(());
            }
            let Some(places) = i.level.places.as_ref() else {
                return Err(json!({"refused": "app-folders-not-established"}));
            };
            let project = built.get("cwd").and_then(Value::as_str).map(PathBuf::from)
                .or_else(|| thread.as_deref().and_then(row_cwd))
                .or_else(|| places.process_cwd.clone());
            let Some(project) = project else { return Err(json!({"refused": "project-not-established"})) };
            // A relative folder is where Codex resolves it: in the folder it was started in.
            let project = if project.is_relative() {
                match &places.process_cwd { Some(cwd) => cwd.join(project), None => return Err(json!({"refused": "project-not-established"})) }
            } else { project };
            let protected = places.protected();
            let protected: Vec<(&'static str, &Path)> = protected.iter().map(|(w, p)| (*w, p.as_path())).collect();
            let exempt = places.app_data.as_deref().map(crate::working_folder::no_project_folder);
            match cl::refusal(level, &project, &protected, exempt.as_deref()) {
                Some(refusal) => Err(refusal.cause()),
                None => Ok(()),
            }
        })();
        match outcome {
            Ok(()) => {
                if let Some(t) = &thread { i.level.refused.remove(t); }
                if i.level.last_refusal.as_ref().is_some_and(|r| r["threadId"].as_str() == thread.as_deref()) { i.level.last_refusal = None; }
                Ok(())
            }
            Err(cause) => {
                let what = cause["refused"].as_str().unwrap_or("refused").to_owned();
                if let Some(t) = &thread { i.level.refused.insert(t.clone(), cause.clone()); }
                i.level.last_refusal = Some(json!({"method": method, "threadId": thread, "levelId": level.id, "cause": cause, "at": now_rfc3339()}));
                Err(format!("refused-not-sent: the level {} is not sent for this conversation ({what}); {method} was not sent", level.id))
            }
        }
    }

    /// The recorded choice behind the level a frame resolved to, by where it came from.
    pub(super) fn level_chosen_for(i: &Inner, method: cl::Method, thread: &str, new_choice: bool) -> Option<String> {
        if new_choice {
            return i.level.new_chosen.as_ref().map(|c| c.entry.clone());
        }
        match method {
            cl::Method::ThreadStart => i.level.default_chosen.as_ref().map(|c| c.entry.clone()),
            _ if i.thread_levels.contains_key(thread) => i.level.thread_chosen.get(thread).map(|c| c.entry.clone()),
            _ => i.level.default_chosen.as_ref().map(|c| c.entry.clone()),
        }
    }

    // ---- Ledger: level_sent at the write, level_reported at the reply (item 6) ----

    fn level_home(i: &Inner) -> Option<String> {
        i.level.places.as_ref().and_then(|p| p.home_identity.clone())
            .or_else(|| i.generation["home"].as_str().filter(|h| !h.is_empty()).map(str::to_owned))
    }
    fn queue_level_entry(i: &mut Inner, entry: Value) {
        if i.recovery.is_some() {
            i.pending_recovery.facts.lock().unwrap().push_back(entry);
        }
    }

    /// After a leveled request's write attempt: what was sent, and `level_sent` once per conversation per chosen
    /// level. A re-send of the same choice to the same conversation writes nothing.
    pub(super) fn level_write_noted(i: &mut Inner, key: &str, written: bool) {
        let Some(e) = i.source_requests.get(key) else { return };
        if e.attempt_position.is_none() { return; }
        let Some(bound) = e.request.level.clone() else { return };
        let request_ref = e.request.request_ref.clone();
        let method = e.request.frame["method"].as_str().unwrap_or_default().to_owned();
        let thread = match &bound.target { Target::Conversation(t) => Some(t.clone()), _ => None };
        let at = now_rfc3339();
        let write_result = if written { "written" } else { "not-established" };
        let takes_effect = takes_effect_now(i, thread.as_deref());
        let row = json!({"method": method, "requestRef": request_ref, "levelId": bound.level.id, "fields": bound.fields, "chosen": bound.chosen, "writeResult": write_result, "at": at});
        match &thread { Some(t) => { i.level.last_sent.insert(t.clone(), row); } None => { i.level.request_sent.insert(key.to_owned(), row); } }
        let Some(chosen) = bound.chosen.clone() else { return };
        if let Some(t) = &thread {
            if i.level.sent_keys.contains_key(&(t.clone(), chosen.clone())) { return; }
        }
        let Some(home) = Self::level_home(i) else { return };
        let Ok(entry_id) = opaque_id("level-sent:") else { return };
        let entry = json!({"kind": "level_sent", "session": i.app_session, "entryId": entry_id, "at": at, "chosen": chosen, "home": home,
            "threadId": thread, "method": method, "requestRef": request_ref, "writeResult": write_result, "takesEffect": takes_effect});
        if i.level.deferred.contains_key(&chosen) {
            // A new-conversation choice: its level_chosen and this entry are written when the reply names it.
            i.level.deferred_sent.insert(key.to_owned(), entry);
            return;
        }
        match &thread {
            Some(t) => { i.level.sent_keys.insert((t.clone(), chosen), entry_id); }
            None => { i.level.sent_by_request.insert(key.to_owned(), entry_id); }
        }
        Self::queue_level_entry(i, entry);
    }

    /// A reply to a leveled request: a created conversation keeps the level its frame carried (and the choice it
    /// came from), and a start's, resume's or fork's reply is compared with the level sent (`level_reported`).
    pub(super) fn level_reply(i: &mut Inner, key: &str, frame: &Value) {
        let Some(e) = i.source_requests.get(key) else { return };
        let Some(bound) = e.request.level.clone() else { return };
        let request_ref = e.request.request_ref.clone();
        if frame.get("error").is_some() {
            if let Some(c) = &bound.chosen { if matches!(bound.target, Target::New | Target::ForkOf(_)) { i.level.deferred.remove(c); } }
            i.level.deferred_sent.remove(key);
            i.level.request_sent.remove(key);
            i.level.sent_by_request.remove(key);
            return;
        }
        let result = &frame["result"];
        let thread = match &bound.target {
            Target::New | Target::ForkOf(_) => result["thread"]["id"].as_str().map(str::to_owned),
            Target::Conversation(t) => Some(t.clone()),
        };
        let Some(thread) = thread.filter(|t| !t.is_empty()) else { return };
        if matches!(bound.target, Target::New | Target::ForkOf(_)) {
            i.thread_levels.entry(thread.clone()).or_insert(bound.level);
            if let Some(c) = bound.chosen.as_ref().and_then(|c| i.level.by_entry.get(c)).cloned() {
                i.level.thread_chosen.entry(thread.clone()).or_insert(c);
            }
            if let Some(row) = i.level.request_sent.remove(key) { i.level.last_sent.insert(thread.clone(), row); }
            let home = Self::level_home(i);
            if let (Some(chosen), Some(home)) = (bound.chosen.clone(), home) {
                if let Some(mut entry) = i.level.deferred.remove(&chosen) {
                    entry["scope"] = json!({"kind": "conversation", "home": home, "threadId": thread});
                    Self::queue_level_entry(i, entry);
                }
                if let Some(mut sent) = i.level.deferred_sent.remove(key) {
                    sent["threadId"] = json!(thread);
                    if let Some(id) = sent["entryId"].as_str() { i.level.sent_keys.insert((thread.clone(), chosen.clone()), id.to_owned()); }
                    Self::queue_level_entry(i, sent);
                }
                if let Some(sent) = i.level.sent_by_request.remove(key) { i.level.sent_keys.insert((thread.clone(), chosen), sent); }
            }
        }
        if bound.method == cl::Method::TurnStart { return; }
        // Codex confirms a level only in these replies; a reply without the fields confirms nothing.
        if result.get("approvalPolicy").is_none() && result.get("sandbox").is_none() { return; }
        let (agreement, differs) = match cl::agreement(bound.level, result) {
            cl::Agreement::Agrees => ("agrees", vec![]),
            cl::Agreement::Differs(fields) => ("differs", fields),
        };
        let from = match bound.method { cl::Method::ThreadStart => "thread/start", cl::Method::ThreadResume => "thread/resume", _ => "thread/fork" };
        let at = now_rfc3339();
        i.level.reported.insert(thread.clone(), json!({"from": from, "at": at, "requestRef": request_ref, "levelId": bound.level.id,
            "approvalPolicy": result.get("approvalPolicy"), "approvalsReviewer": result.get("approvalsReviewer"), "sandbox": result.get("sandbox"),
            "agreement": agreement, "differs": differs}));
        let Some(chosen) = bound.chosen.clone() else { return };
        let (Some(sent), Some(home)) = (i.level.sent_keys.get(&(thread.clone(), chosen.clone())).cloned(), Self::level_home(i)) else { return };
        let Ok(entry_id) = opaque_id("level-reported:") else { return };
        let entry = json!({"kind": "level_reported", "session": i.app_session, "entryId": entry_id, "at": at, "chosen": chosen, "sent": sent,
            "home": home, "threadId": thread, "from": from, "approvalPolicy": result.get("approvalPolicy").cloned().unwrap_or(Value::Null),
            "approvalsReviewer": result.get("approvalsReviewer").cloned().unwrap_or(Value::Null),
            "sandbox": result.get("sandbox").cloned().unwrap_or(Value::Null), "agreement": agreement});
        Self::queue_level_entry(i, entry);
    }

    // ---- The person's choice (item 5) ----

    /// The person confirmed `level` for `scope` in the App's native statement (`statement_digest`). The
    /// `level_chosen` entry is written first; only once it is in the ledger does the level in force change, here
    /// and, for the default, in each Host of `also` (the App's other homes, which share this ledger). A write that
    /// fails changes nothing and is returned as an error. A new-conversation choice has no ledger scope of its
    /// own: its entry is written, as the conversation's, when the start or fork reply names the conversation.
    pub(crate) fn choose_level(&self, scope: &LevelScope, level: &'static Level, statement_digest: &str, also: &[Arc<Host>]) -> Result<Value, String> {
        if statement_digest.len() != 64 || !statement_digest.bytes().all(|b| b.is_ascii_hexdigit() && !b.is_ascii_uppercase()) {
            return Err("The level's native statement has no digest; nothing was changed".into());
        }
        let _writer = self.recovery_writer.lock().unwrap();
        self.drain_recovery_owned();
        let (ledger, session, home) = {
            let i = self.inner.0.lock().unwrap();
            (i.recovery.clone(), i.app_session.clone(), i.level.places.as_ref().and_then(|p| p.home_identity.clone()))
        };
        let entry_id = opaque_id("level-chosen:")?;
        let at = now_rfc3339();
        let chosen = Chosen { entry: entry_id.clone(), at: at.clone(), level };
        let ledger_scope = match scope {
            LevelScope::Default => json!({"kind": "default-for-new-conversations"}),
            LevelScope::Conversation(thread) => {
                let home = home.ok_or("This conversation's Codex home is not established; the level was not changed")?;
                let known = self.inner.0.lock().unwrap().threads.iter().any(|t| t["threadId"] == thread.as_str());
                if !known { return Err("The conversation is not one this Codex home has open; the level was not changed".into()); }
                json!({"kind": "conversation", "home": home, "threadId": thread})
            }
            LevelScope::NewConversation => Value::Null,
        };
        let mut entry = json!({"kind": "level_chosen", "session": session, "entryId": entry_id, "at": at, "scope": ledger_scope,
            "level": cl::recorded_values(level), "previous": null, "confirmation": {"kind": "native", "statementDigest": statement_digest}});
        if *scope == LevelScope::NewConversation {
            if ledger.is_none() { return Err("The App ledger is unavailable, so the level could not be recorded; nothing was changed".into()); }
            let mut i = self.inner.0.lock().unwrap();
            i.level.deferred.insert(entry_id.clone(), entry);
            Self::apply_chosen(&mut i, scope, chosen);
            return Ok(json!({"state": "chosen", "scope": "new-conversation", "levelId": level.id, "ledgerEntry": entry_id, "recorded": "when the new conversation is named"}));
        }
        let ledger = ledger.ok_or("The App ledger is unavailable, so the level could not be recorded; nothing was changed")?;
        let appended = {
            let mut ledger = ledger.lock().unwrap();
            let previous = ledger.current_entries().iter().rev()
                .find(|e| e["kind"] == "level_chosen" && e["scope"] == entry["scope"])
                .and_then(|e| e["entryId"].as_str().map(str::to_owned));
            entry["previous"] = json!(previous);
            let appended = ledger.append(entry.clone());
            (appended, ledger.observation())
        };
        self.inner.0.lock().unwrap().recovery_snapshot = Some(appended.1);
        appended.0.map_err(|e| format!("The level was not recorded in the App ledger ({e}); nothing was changed"))?;
        Self::apply_chosen(&mut self.inner.0.lock().unwrap(), scope, chosen.clone());
        if *scope == LevelScope::Default {
            for other in also.iter().filter(|h| !std::ptr::eq(Arc::as_ptr(h), self)) {
                Self::apply_chosen(&mut other.inner.0.lock().unwrap(), scope, chosen.clone());
            }
        }
        Ok(json!({"state": "chosen", "scope": match scope { LevelScope::Default => json!("default"), LevelScope::Conversation(t) => json!({"conversation": t}), LevelScope::NewConversation => json!("new-conversation") },
            "levelId": level.id, "ledgerEntry": entry_id, "previous": entry["previous"], "recorded": "in the App ledger"}))
    }

    /// The one change of the level in force from a recorded choice. Called only by [`Self::choose_level`] and
    /// [`Self::read_levels_at_launch`].
    fn apply_chosen(i: &mut Inner, scope: &LevelScope, chosen: Chosen) {
        i.level.by_entry.insert(chosen.entry.clone(), chosen.clone());
        match scope {
            LevelScope::Default => { i.default_level = Some(chosen.level); i.level.default_chosen = Some(chosen); }
            LevelScope::Conversation(t) => { i.thread_levels.insert(t.clone(), chosen.level); i.level.thread_chosen.insert(t.clone(), chosen); }
            LevelScope::NewConversation => { i.new_conversation_level = Some(chosen.level); i.level.new_chosen = Some(chosen); }
        }
        i.level_revision += 1;
    }

    /// Whether a turn is running in the conversation now (a level then takes effect from its next turn).
    pub(crate) fn level_turn_running(&self, thread: &str) -> bool {
        Self::current_live_turn(&self.inner.0.lock().unwrap(), thread).is_some()
    }

    // ---- Launch read (item 6) ----

    /// At launch: the level for each scope is the latest `level_chosen` in that scope, accepted only if its id is
    /// in the table, its values equal that row exactly and its table digest matches. Otherwise there is no level
    /// for that scope, and the person chooses before any conversation; nothing falls back to Codex's own setting,
    /// to an earlier entry or to a recommended level. `home` is this Host's `home_identity`.
    pub(crate) fn read_levels_at_launch(&self, home: Option<&str>) -> Value {
        let (ledger, limit) = {
            let i = self.inner.0.lock().unwrap();
            (i.recovery.clone(), i.recovery_initialization_error.clone())
        };
        let read = match (ledger, limit) {
            (Some(ledger), None) => Ok(ledger.lock().unwrap().current_entries().to_vec()),
            (_, Some(limit)) => Err(format!("The App ledger could not be read ({limit}), so no level is in force; choose a level before any conversation.")),
            (None, None) => Err("The App ledger is unavailable, so no level is in force; choose a level before any conversation.".into()),
        };
        let rows = match read {
            Ok(rows) => rows,
            Err(reason) => {
                let view = json!({"state": "not-read", "reason": reason});
                self.inner.0.lock().unwrap().level.launch = view.clone();
                return view;
            }
        };
        let mut latest: Vec<(LevelScope, Value)> = Vec::new();
        for row in rows.iter().filter(|r| r["kind"] == "level_chosen") {
            let scope = match row["scope"]["kind"].as_str() {
                Some("default-for-new-conversations") => LevelScope::Default,
                Some("conversation") if home.is_some_and(|h| row["scope"]["home"] == h) => match row["scope"]["threadId"].as_str() {
                    Some(t) => LevelScope::Conversation(t.to_owned()),
                    None => continue,
                },
                _ => continue,
            };
            latest.retain(|(s, _)| *s != scope);
            latest.push((scope, row.clone()));
        }
        let mut accepted = Vec::new();
        let mut refused = Vec::new();
        let mut i = self.inner.0.lock().unwrap();
        for (scope, row) in latest {
            let entry = row["entryId"].as_str().unwrap_or_default().to_owned();
            match cl::accept_recorded(&row["level"]) {
                Some(level) => {
                    let chosen = Chosen { entry: entry.clone(), at: row["at"].as_str().unwrap_or_default().to_owned(), level };
                    Self::apply_chosen(&mut i, &scope, chosen);
                    accepted.push(json!({"entryId": entry, "levelId": level.id}));
                }
                None => {
                    // No level for this scope: the recorded level is withdrawn, not replaced by another.
                    match &scope {
                        LevelScope::Default => { i.default_level = None; i.level.default_chosen = None; }
                        LevelScope::Conversation(t) => { i.thread_levels.remove(t); i.level.thread_chosen.remove(t); }
                        LevelScope::NewConversation => {}
                    }
                    i.level_revision += 1;
                    refused.push(json!({"entryId": entry, "reason": "The recorded level does not match the App's level table exactly; choose a level again."}));
                }
            }
        }
        for row in rows.iter().filter(|r| r["kind"] == "level_sent" && home.is_none_or(|h| r["home"] == h)) {
            if let (Some(t), Some(c), Some(id)) = (row["threadId"].as_str(), row["chosen"].as_str(), row["entryId"].as_str()) {
                i.level.sent_keys.insert((t.to_owned(), c.to_owned()), id.to_owned());
            }
        }
        let view = json!({"state": "read", "accepted": accepted, "refused": refused});
        i.level.launch = view.clone();
        view
    }

    // ---- Status (item 7) ----

    pub(super) fn level_status(i: &Inner, status: &mut Value) {
        status["levelDefault"] = chosen_view(i.level.default_chosen.as_ref(), i.default_level, "default");
        status["levelStartRefusal"] = json!(i.level.start_refusal);
        status["levelSendRefusal"] = json!(i.level.last_refusal);
        status["levelLaunchRead"] = i.level.launch.clone();
        status["levelRecommended"] = json!(cl::RECOMMENDED_LEVEL);
        if let Some(threads) = status["threads"].as_array_mut() {
            for row in threads.iter_mut() {
                let Some(t) = row["threadId"].as_str().map(str::to_owned) else { continue };
                let own = i.thread_levels.get(&t).copied();
                let chosen = match own {
                    Some(level) => chosen_view(i.level.thread_chosen.get(&t), Some(level), "conversation"),
                    None => chosen_view(i.level.default_chosen.as_ref(), i.default_level, "default"),
                };
                let in_force = own.or(i.default_level);
                let sent = i.level.last_sent.get(&t).cloned();
                let reported = i.level.reported.get(&t).cloned();
                // Confirmed only by a start, resume or fork reply for the level now in force: a change sent on a turn
                // is not confirmed until the next such reply.
                let agreement = match (&reported, in_force) {
                    (Some(r), Some(level)) if r["levelId"] == level.id.as_str() => r["agreement"].clone(),
                    _ => json!("not-confirmed"),
                };
                let changed = match (&sent, in_force) { (Some(s), Some(level)) => s["levelId"] != level.id.as_str(), _ => false };
                let takes_effect = if changed && Self::current_live_turn(i, &t).is_some() { "from-next-turn" } else { "now" };
                let mut level = json!({"chosen": chosen, "sent": sent, "reported": reported, "agreement": agreement, "takesEffect": takes_effect});
                if let Some(cause) = i.level.refused.get(&t) { level["refused"] = cause.clone(); }
                row["level"] = level;
            }
        }
    }

    // ---- Lasting rules (item 8) ----

    /// Reads this Host's home's lasting rules now (at launch, after each start reaches ready, and after an answer
    /// that adds a rule is sent). `home` is used when the start has not yet established it.
    pub(crate) fn read_lasting_rules(&self, home: Option<&Path>) {
        let home = home.map(Path::to_path_buf).or_else(|| self.inner.0.lock().unwrap().level.places.as_ref().and_then(|p| p.codex_home.clone()));
        let Some(home) = home else { return };
        let reading = crate::lasting_rules::read(&home);
        self.inner.0.lock().unwrap().level.rules = Some(json!({"home": home.to_string_lossy(), "lastingRules": reading}));
    }
    /// This Host's home's lasting rules as last read (None before any reading).
    pub(crate) fn lasting_rules(&self) -> Option<Value> {
        self.inner.0.lock().unwrap().level.rules.clone()
    }
}

#[cfg(test)]
#[path = "hosting_level_tests.rs"]
mod tests;
