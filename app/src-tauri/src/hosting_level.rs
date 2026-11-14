//! DEL-01-01, DEL-01-02, DEL-04-02, PRD V4-AUT-06: the Host's side of the person's permission level beyond the
//! frame builder in `hosting.rs`: the checks before a Codex start, the checks each time a level is sent, the
//! level's App ledger entries (`level_chosen`, `level_sent`, `level_reported`), the reading of the recorded level at
//! launch, the level's status, and the lasting rules each App-owned Codex home holds.
//!
//! The level is the person's own setting, a plain setting with no confirmation and no seal. Nothing here is an
//! act-control act or a human-act record, and no entry carries an actor. The only paths that change the level in
//! force in production are [`Host::choose_level`] (the App's `set_level` command) and
//! [`Host::read_levels_at_launch`] (the recorded choices, or the App's default `codex_level::DEFAULT_LEVEL` where a
//! complete read finds none for the default scope).
//!
//! The project trust entry each start, resume and fork carries is read here too ([`Host::trust_reading`]).
use super::*;
use crate::codex_level::{self as cl, Level, Target};
use std::path::Path;

/// Where a level in force comes from (`origin` in the status).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Origin {
    /// The person's choice, recorded in the ledger.
    Chosen,
    /// The App's default, put in force by a complete launch read that found no valid choice for the default scope.
    /// Never written to the ledger.
    AppDefault,
    /// The person's choice, held in memory only because the App's records could not be read or saved.
    SessionOnly,
}
impl Origin {
    pub(crate) fn as_str(self) -> &'static str {
        match self { Self::Chosen => "chosen", Self::AppDefault => "app-default", Self::SessionOnly => "session-only" }
    }
}

/// A level in force for a scope: the ledger entry it was recorded as (None for the App's default and a
/// session-only choice), when, the level, and where it comes from.
#[derive(Clone, Debug)]
pub(crate) struct Chosen {
    pub(crate) entry: Option<String>,
    pub(crate) at: String,
    pub(crate) level: &'static Level,
    pub(crate) origin: Origin,
}

/// The App's default level (`codex_level::DEFAULT_LEVEL`), per Host. Only the `cfg(test)` setter
/// `Host::set_app_default_for_test` changes it.
#[derive(Clone, Copy, Debug)]
pub(crate) struct AppDefault(pub(crate) Option<&'static Level>);
impl Default for AppDefault {
    fn default() -> Self {
        AppDefault(cl::DEFAULT_LEVEL.map(|id| cl::level(id).expect("the App's default level is a row of the table")))
    }
}

/// The `config/read` the trust entry is read from is named so in the request record.
pub(crate) const TRUST_READING_INITIATOR: &str = "project-trust-reading";

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
    /// The App's default level for this Host.
    pub(crate) app_default: AppDefault,
    /// Why the person may choose a level for this session only: the launch read positively failed or was limited
    /// (`{reason, detail}`). None after a complete read, and never for an empty ledger.
    pub(crate) session_only: Option<Value>,
    /// Advanced by every attempted configuration write; a trust reading made before one is not current.
    pub(crate) config_writes: u64,
    /// The unit tests' Host makes no trust reading (its peers answer no `config/read`); a test turns it on.
    #[cfg(test)]
    pub(crate) trust_reads: bool,
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

fn chosen_view(chosen: Option<&Chosen>, level: Option<&'static Level>, scope: &str, session_only: Option<&Value>) -> Value {
    match (chosen, level) {
        (Some(c), _) => {
            let mut view = json!({"id": c.level.id, "dimensions": c.level.dimensions, "ledgerEntry": c.entry,
                "chosenAt": if c.origin == Origin::AppDefault { Value::Null } else { json!(c.at) }, "scope": scope, "reading": "not-limited",
                "origin": c.origin.as_str()});
            match c.origin {
                Origin::Chosen => {}
                Origin::AppDefault => {
                    view["originSentence"] = json!(cl::APP_DEFAULT_SENTENCE);
                    if c.level.id == "full" { view["explanation"] = json!(cl::APP_DEFAULT_EXPLAINED); }
                }
                Origin::SessionOnly => {
                    view["originSentence"] = json!(cl::SESSION_ONLY_SENTENCE);
                    view["sessionOnly"] = session_only.cloned().unwrap_or(Value::Null);
                }
            }
            view
        }
        // A level set without a record or an origin: only the test setters do this.
        (None, Some(level)) => json!({"id": level.id, "dimensions": level.dimensions, "ledgerEntry": null, "chosenAt": null, "scope": scope, "reading": "not-limited", "origin": null}),
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
        let entry = |c: Option<&Chosen>| c.and_then(|c| c.entry.clone());
        if new_choice {
            return entry(i.level.new_chosen.as_ref());
        }
        match method {
            cl::Method::ThreadStart => entry(i.level.default_chosen.as_ref()),
            _ if i.thread_levels.contains_key(thread) => entry(i.level.thread_chosen.get(thread)),
            _ => entry(i.level.default_chosen.as_ref()),
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
        let mut row = json!({"method": method, "requestRef": request_ref, "levelId": bound.level.id, "fields": bound.fields, "chosen": bound.chosen, "writeResult": write_result, "at": at});
        if let Some(trust) = &bound.trust { row["projectTrust"] = trust.status(); }
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

    // ---- The person's choice ----

    /// The person chose `level` for `scope` in the App's level control: a plain setting, with no confirmation. The
    /// `level_chosen` entry is written first; only once it is in the ledger does the level in force change, here
    /// and, for the default, in each Host of `also` (the App's other homes, which share this ledger). A new-
    /// conversation choice has no ledger scope of its own: its entry is written, as the conversation's, when the
    /// start or fork reply names the conversation.
    ///
    /// Where the launch read positively failed or was limited (never an empty ledger), and the choice cannot be
    /// written, it is held for this session only: in memory, never written, dropped at quit and by any later
    /// complete read. Otherwise a write that fails changes nothing and is returned as an error.
    pub(crate) fn choose_level(&self, scope: &LevelScope, level: &'static Level, also: &[Arc<Host>]) -> Result<Value, String> {
        let _writer = self.recovery_writer.lock().unwrap();
        self.drain_recovery_owned();
        let (ledger, session, home, session_only) = {
            let i = self.inner.0.lock().unwrap();
            (i.recovery.clone(), i.app_session.clone(), i.level.places.as_ref().and_then(|p| p.home_identity.clone()), i.level.session_only.is_some())
        };
        let entry_id = opaque_id("level-chosen:")?;
        let at = now_rfc3339();
        let scope_view = match scope { LevelScope::Default => json!("default"), LevelScope::Conversation(t) => json!({"conversation": t}), LevelScope::NewConversation => json!("new-conversation") };
        if let LevelScope::Conversation(thread) = scope {
            let known = self.inner.0.lock().unwrap().threads.iter().any(|t| t["threadId"] == thread.as_str());
            if !known { return Err("The conversation is not one this Codex home has open; the level was not changed".into()); }
        }
        // The App's records could not be read at launch, and this choice cannot be saved: held for this session.
        let for_this_session = |failure: Option<String>| -> Result<Value, String> {
            let chosen = Chosen { entry: None, at: at.clone(), level, origin: Origin::SessionOnly };
            Self::apply_chosen(&mut self.inner.0.lock().unwrap(), scope, chosen.clone());
            if *scope == LevelScope::Default {
                for other in also.iter().filter(|h| !std::ptr::eq(Arc::as_ptr(h), self)) {
                    Self::apply_chosen(&mut other.inner.0.lock().unwrap(), scope, chosen.clone());
                }
            }
            Ok(json!({"state": "chosen", "scope": scope_view, "levelId": level.id, "ledgerEntry": null, "origin": "session-only",
                "recorded": "not recorded", "sentence": cl::SESSION_ONLY_SENTENCE,
                "writeFailure": failure.map(|text| json!({"text": text, "standing": cl::NOT_THE_APPS_TEXT}))}))
        };
        let ledger_scope = match scope {
            LevelScope::Default => json!({"kind": "default-for-new-conversations"}),
            LevelScope::Conversation(thread) => match &home {
                Some(home) => json!({"kind": "conversation", "home": home, "threadId": thread}),
                None if session_only => return for_this_session(None),
                None => return Err("This conversation's Codex home is not established; the level was not changed".into()),
            },
            LevelScope::NewConversation => Value::Null,
        };
        let mut entry = json!({"kind": "level_chosen", "session": session, "entryId": entry_id, "at": at, "scope": ledger_scope,
            "level": cl::recorded_values(level), "previous": null});
        let Some(ledger) = ledger else {
            if session_only { return for_this_session(None); }
            return Err("The App ledger is unavailable, so the level could not be recorded; nothing was changed".into());
        };
        let chosen = Chosen { entry: Some(entry_id.clone()), at: at.clone(), level, origin: Origin::Chosen };
        if *scope == LevelScope::NewConversation {
            let mut i = self.inner.0.lock().unwrap();
            i.level.deferred.insert(entry_id.clone(), entry);
            Self::apply_chosen(&mut i, scope, chosen);
            return Ok(json!({"state": "chosen", "scope": "new-conversation", "levelId": level.id, "ledgerEntry": entry_id, "origin": "chosen", "recorded": "when the new conversation is named"}));
        }
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
        if let Err(e) = appended.0 {
            if session_only { return for_this_session(Some(e)); }
            return Err(format!("The level was not recorded in the App ledger ({e}); nothing was changed"));
        }
        Self::apply_chosen(&mut self.inner.0.lock().unwrap(), scope, chosen.clone());
        if *scope == LevelScope::Default {
            for other in also.iter().filter(|h| !std::ptr::eq(Arc::as_ptr(h), self)) {
                Self::apply_chosen(&mut other.inner.0.lock().unwrap(), scope, chosen.clone());
            }
        }
        Ok(json!({"state": "chosen", "scope": scope_view, "levelId": level.id, "ledgerEntry": entry_id, "previous": entry["previous"], "origin": "chosen", "recorded": "in the App ledger"}))
    }

    /// The one change of the level in force for a scope. Called only by [`Self::choose_level`] (a recorded or a
    /// session-only choice) and [`Self::read_levels_at_launch`] (a recorded choice, or the App's default).
    fn apply_chosen(i: &mut Inner, scope: &LevelScope, chosen: Chosen) {
        if let Some(entry) = &chosen.entry { i.level.by_entry.insert(entry.clone(), chosen.clone()); }
        match scope {
            LevelScope::Default => { i.default_level = Some(chosen.level); i.level.default_chosen = Some(chosen); }
            LevelScope::Conversation(t) => { i.thread_levels.insert(t.clone(), chosen.level); i.level.thread_chosen.insert(t.clone(), chosen); }
            LevelScope::NewConversation => { i.new_conversation_level = Some(chosen.level); i.level.new_chosen = Some(chosen); }
        }
        i.level_revision += 1;
    }

    /// Tests only: the App's default level for this Host (`None`: no default). A shipped build has no route here.
    #[cfg(test)]
    pub(crate) fn set_app_default_for_test(&self, id: Option<&str>) {
        self.inner.0.lock().unwrap().level.app_default = AppDefault(id.map(|id| cl::level(id).expect("a row of the table")));
    }

    // ---- Launch read ----

    /// At launch: the level for each scope is the latest `level_chosen` in that scope, accepted only if its id is
    /// in the table and its values (the table's digest among them) equal that row exactly. A recorded level that is
    /// not accepted is no level for that scope, never an earlier entry and never Codex's own setting. When the read
    /// is complete and no valid choice for the default scope is found, the App's default
    /// (`codex_level::DEFAULT_LEVEL`) is in force there, shown as the App's default and never written. A ledger
    /// that cannot be read, or is limited, puts nothing in force and lets the person choose for this session only.
    /// A complete read drops every session-only choice. `home` is this Host's `home_identity`.
    pub(crate) fn read_levels_at_launch(&self, home: Option<&str>) -> Value {
        let (ledger, limit) = {
            let i = self.inner.0.lock().unwrap();
            (i.recovery.clone(), i.recovery_initialization_error.clone())
        };
        let read = match (ledger, limit) {
            (Some(ledger), None) => Ok(ledger.lock().unwrap().current_entries().to_vec()),
            (_, Some(limit)) => Err((format!("The App ledger could not be read ({limit}), so no level is in force; choose a level before any conversation."),
                json!({"reason": cl::RECORDS_NOT_READ, "detail": {"text": limit, "standing": cl::NOT_THE_APPS_TEXT}}))),
            (None, None) => Err(("The App ledger is unavailable, so no level is in force; choose a level before any conversation.".into(),
                json!({"reason": cl::RECORDS_UNAVAILABLE, "detail": null}))),
        };
        let rows = match read {
            Ok(rows) => rows,
            Err((reason, session_only)) => {
                let view = json!({"state": "not-read", "reason": reason});
                let mut i = self.inner.0.lock().unwrap();
                i.level.launch = view.clone();
                i.level.session_only = Some(session_only);
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
        // A complete read governs: every session-only choice is dropped.
        i.level.session_only = None;
        let mut dropped = false;
        if i.level.default_chosen.as_ref().is_some_and(|c| c.origin == Origin::SessionOnly) { i.default_level = None; i.level.default_chosen = None; dropped = true; }
        if i.level.new_chosen.as_ref().is_some_and(|c| c.origin == Origin::SessionOnly) { i.new_conversation_level = None; i.level.new_chosen = None; dropped = true; }
        let session_threads: Vec<String> = i.level.thread_chosen.iter().filter(|(_, c)| c.origin == Origin::SessionOnly).map(|(t, _)| t.clone()).collect();
        for t in session_threads { i.thread_levels.remove(&t); i.level.thread_chosen.remove(&t); dropped = true; }
        if dropped { i.level_revision += 1; }
        let mut default_accepted = false;
        for (scope, row) in latest {
            let entry = row["entryId"].as_str().unwrap_or_default().to_owned();
            match cl::accept_recorded(&row["level"]) {
                Some(level) => {
                    let chosen = Chosen { entry: Some(entry.clone()), at: row["at"].as_str().unwrap_or_default().to_owned(), level, origin: Origin::Chosen };
                    if scope == LevelScope::Default { default_accepted = true; }
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
        let mut view = json!({"state": "read", "accepted": accepted, "refused": refused});
        // The App's default, where the complete read found no valid choice for the default scope.
        if let (false, Some(level)) = (default_accepted, i.level.app_default.0) {
            Self::apply_chosen(&mut i, &LevelScope::Default, Chosen { entry: None, at: now_rfc3339(), level, origin: Origin::AppDefault });
            view["appDefault"] = json!(level.id);
        }
        i.level.launch = view.clone();
        view
    }

    // ---- Status ----

    pub(super) fn level_status(i: &Inner, status: &mut Value) {
        let session_only = i.level.session_only.as_ref();
        status["levelDefault"] = chosen_view(i.level.default_chosen.as_ref(), i.default_level, "default", session_only);
        status["levelStartRefusal"] = json!(i.level.start_refusal);
        status["levelSendRefusal"] = json!(i.level.last_refusal);
        status["levelLaunchRead"] = i.level.launch.clone();
        status["levelAppDefault"] = json!(i.level.app_default.0.map(|l| l.id.as_str()));
        // Offered only when the launch read positively failed or was limited.
        status["levelSessionOnlyOffered"] = json!(session_only);
        if let Some(threads) = status["threads"].as_array_mut() {
            for row in threads.iter_mut() {
                let Some(t) = row["threadId"].as_str().map(str::to_owned) else { continue };
                let own = i.thread_levels.get(&t).copied();
                let chosen = match own {
                    Some(level) => chosen_view(i.level.thread_chosen.get(&t), Some(level), "conversation", session_only),
                    None => chosen_view(i.level.default_chosen.as_ref(), i.default_level, "default", session_only),
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
                let project_trust = sent.as_ref().map(|s| s["projectTrust"].clone()).filter(|v| !v.is_null());
                let mut level = json!({"chosen": chosen, "sent": sent, "reported": reported, "agreement": agreement, "takesEffect": takes_effect});
                if let Some(trust) = project_trust { level["projectTrust"] = trust; }
                if let Some(cause) = i.level.refused.get(&t) { level["refused"] = cause.clone(); }
                row["level"] = level;
            }
        }
    }

    // ---- Project trust ----

    /// The project trust a start, resume or fork carries, read just before its frame is built: the conversation's
    /// working folder (as sent, else the conversation's, else the folder Codex was started in), its project root as
    /// Codex computes it, and a `config/read` (that folder, layers included) of this generation. Only a whole reading
    /// whose user layers mark the root trusted gives "trusted"; anything else is untrusted, a failed or limited
    /// reading included. Holds no lock while it reads. None for a method that carries no trust entry, or when the
    /// folder is not known (the frame is then refused).
    pub(super) fn trust_reading(&self, method: &str, params: &Value, generation: Option<&Value>) -> Option<cl::TrustReading> {
        if !matches!(cl::Method::of(method)?, cl::Method::ThreadStart | cl::Method::ThreadResume | cl::Method::ThreadFork) { return None; }
        let (cwd, generation, epoch) = {
            let i = self.inner.0.lock().unwrap();
            let thread = params["threadId"].as_str();
            let process_cwd = i.level.places.as_ref().and_then(|p| p.process_cwd.clone());
            let cwd = params.get("cwd").and_then(Value::as_str).map(PathBuf::from)
                .or_else(|| thread.and_then(|t| i.threads.iter().rev().find(|r| r["threadId"] == t).and_then(|r| r["cwd"].as_str()).map(PathBuf::from)))
                .or_else(|| process_cwd.clone());
            let cwd = match cwd {
                Some(c) if c.is_relative() => process_cwd.map(|p| p.join(c)),
                other => other,
            };
            // A Host that is not ready sends nothing; its frame is refused for that reason.
            if i.state != "ready" { return cwd.map(|cwd| cl::TrustReading::not_read(cwd, cl::TRUST_READ_FAILED, None)); }
            #[cfg(test)]
            if !i.level.trust_reads { return cwd.map(|cwd| cl::TrustReading::not_read(cwd, cl::TRUST_READ_FAILED, None)); }
            (cwd?, generation.cloned().unwrap_or_else(|| i.generation.clone()), i.level.config_writes)
        };
        let deadline = std::time::Instant::now() + reading_gate::READING_DEFAULT_BUDGET;
        let params = json!({"cwd": cwd.to_string_lossy(), "includeLayers": true});
        let request = match self.request_reading("config/read", params, json!({"kind":"person-directed","name":TRUST_READING_INITIATOR}), &generation, true, deadline) {
            Ok(request) => request,
            Err(error) => return Some(cl::TrustReading::not_read(cwd, cl::TRUST_READ_FAILED, Some(error))),
        };
        let response = match self.wait_source_response(&request, deadline.saturating_duration_since(std::time::Instant::now())) {
            Ok(response) => response,
            Err(error) => { self.delegation_wait_ended(&request); return Some(cl::TrustReading::not_read(cwd, cl::TRUST_READ_FAILED, Some(error))); }
        };
        // A native error or a schema finding can quote configuration: neither is passed on, only an error's code.
        if let Some(error) = response.get("error") {
            let detail = error["code"].as_i64().map(|code| format!("config/read answered with an error (code {code})"));
            return Some(cl::TrustReading::not_read(cwd, cl::TRUST_READ_FAILED, detail));
        }
        let result = response.get("result").cloned().unwrap_or(Value::Null);
        if Self::validate_native_result("ConfigReadResponse", &result).is_err() {
            return Some(cl::TrustReading::not_read(cwd, cl::TRUST_READ_FAILED, None));
        }
        let mut reading = cl::TrustReading::not_read(cwd, cl::TRUST_READ_FAILED, None);
        match cl::person_mark(&result, &reading.root) {
            Ok(case) => {
                reading.case = case;
                reading.generation = Some(json!({"generation": generation, "configWrites": epoch}));
                reading.request_ref = Some(request.request_ref.clone());
                reading.read_at = Some(now_rfc3339());
            }
            Err(reason) => reading.case = cl::TrustCase::NotRead { reason, detail: None },
        }
        Some(reading)
    }

    /// The reading as the frame relies on it: still of this generation with no configuration write since, or else
    /// never trusted.
    pub(super) fn trust_current(i: &Inner, reading: cl::TrustReading) -> cl::TrustReading {
        let current = reading.generation.as_ref().is_some_and(|g| g["generation"] == i.generation && g["configWrites"] == i.level.config_writes);
        if current || matches!(reading.case, cl::TrustCase::NotRead { .. }) { reading } else { reading.stale() }
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
