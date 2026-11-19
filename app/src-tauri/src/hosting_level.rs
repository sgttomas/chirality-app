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

use crate::codex_level::LevelOrigin as Origin;

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
    /// Latest setting-write outcome, separate from the level currently in force.
    pub(crate) choice_save: Option<Value>,
    pub(crate) thread_chosen: HashMap<String, Chosen>,
    /// Every recorded choice by entry id, so a request's bound `chosen` can be followed.
    pub(crate) by_entry: HashMap<String, Chosen>,
    /// (conversation, chosen entry) to the `level_sent` entry written for it: once per conversation per choice.
    pub(crate) sent_keys: HashMap<(String, String), String>,
    /// A start's or fork's `level_sent` entry by request key, until the reply names the conversation.
    pub(crate) sent_by_request: HashMap<String, String>,
    /// What was last sent to each conversation (`threads[].level.sent`), and a start's or fork's by request key.
    pub(crate) last_sent: HashMap<String, Value>,
    pub(crate) request_sent: HashMap<String, Value>,
    /// What Codex last reported for each conversation (`threads[].level.reported`).
    pub(crate) reported: HashMap<String, Value>,
    /// Association entries queued for this session, and those read back from a validated launch cut.
    pub(crate) inherited: HashMap<String, String>,
    pub(crate) inherited_read: std::collections::HashSet<String>,
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
    /// The ask for the default scope (V4-AUT-06's one exception): the launch read found no earlier session in a
    /// complete record, or a recorded default that no longer matches the table, or could not read the record, while
    /// this home holds state from an earlier Codex start. No default applies until the person chooses.
    pub(crate) record_missing: bool,
    /// The ask for one conversation: its recorded level no longer matches the table. It does not fall to the default.
    pub(crate) thread_asks: std::collections::HashSet<String>,
    /// The App's default applies although the launch read could not read the records (a first run by the home's
    /// evidence): `levelRecordsUnread` discloses the read failure and separate choice-saving outcome.
    pub(crate) records_unread: bool,
    /// Advanced by every attempted configuration write; a trust reading made before one is not current.
    pub(crate) config_writes: u64,
    /// DEL-01-01: the App's projects and their trust, as the last trust reading found it configured.
    pub(crate) project_trust: Option<Arc<crate::project_trust::ProjectTrust>>,
    /// The last start, resume or fork Codex refused because a trusted project's own settings file could not be
    /// loaded (`codex_level::project_settings_refusal`), and each conversation's.
    /// Each with the count of the person's switches off when it was noted: one noted before a later switch off is
    /// no longer shown.
    pub(crate) settings_refusal: Option<(Value, u64)>,
    pub(crate) thread_settings_refusal: HashMap<String, (Value, u64)>,
    /// A test's own budget for the trust reading, in place of the reading default.
    #[cfg(test)]
    pub(crate) trust_budget: Option<std::time::Duration>,
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
                "chosenAt": if c.origin == Origin::AppDefault { Value::Null } else { json!(c.at) }, "scope": scope, "reading": "not-limited", "readingSentence": cl::READING_SENTENCE,
                "origin": c.origin.as_str(), "recorded": match c.origin { Origin::Chosen => "recorded", Origin::SaveUnconfirmed => "not-confirmed", _ => "not-recorded" }});
            match c.origin {
                Origin::Chosen => {}
                Origin::SaveUnconfirmed => { view["originSentence"] = json!(cl::SAVE_UNCONFIRMED_APPLIED); }
                Origin::AppDefault => {
                    view["originSentence"] = json!(cl::APP_DEFAULT_SENTENCE);
                    if c.level.id == "full" { view["explanation"] = json!(cl::APP_DEFAULT_EXPLAINED); }
                }
                Origin::SessionOnly => {
                    view["originSentence"] = json!(cl::SESSION_ONLY_SENTENCE);
                    view["sessionOnly"] = session_only.cloned().unwrap_or(Value::Null);
                }
            }
            if c.level.approval_policy != "never" { view["allowing"] = json!(cl::SUPERVISED_ALLOWING); }
            view
        }
        // A level set without a record or an origin: only the test setters do this.
        (None, Some(level)) => json!({"id": level.id, "dimensions": level.dimensions, "ledgerEntry": null, "chosenAt": null, "scope": scope, "reading": "not-limited", "readingSentence": cl::READING_SENTENCE, "origin": null}),
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
                .or_else(|| (method == "thread/start").then(|| places.process_cwd.clone()).flatten());
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
    pub(super) fn level_origin_for(i: &Inner, method: cl::Method, thread: &str) -> Option<Chosen> {
        match method {
            cl::Method::ThreadStart => i.level.default_chosen.clone(),
            _ if i.thread_levels.contains_key(thread) => i.level.thread_chosen.get(thread).cloned(),
            _ => i.level.default_chosen.clone(),
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
        if let Some(trust) = &bound.trust {
            row["projectTrust"] = trust.status_for_write(written);
            if trust.choice.is_some() {
                if let Some(projects) = &i.level.project_trust { projects.note_sent(row["projectTrust"].clone()); }
            }
        }
        match &thread { Some(t) => { i.level.last_sent.insert(t.clone(), row); } None => { i.level.request_sent.insert(key.to_owned(), row); } }
        let Some(chosen) = bound.chosen.clone() else { return };
        if let Some(t) = &thread {
            if i.level.sent_keys.contains_key(&(t.clone(), chosen.clone())) { return; }
        }
        let Some(home) = Self::level_home(i) else { return };
        let Ok(entry_id) = opaque_id("level-sent:") else { return };
        let entry = json!({"kind": "level_sent", "session": i.app_session, "entryId": entry_id, "at": at, "chosen": chosen, "home": home,
            "threadId": thread, "method": method, "requestRef": request_ref, "writeResult": write_result, "takesEffect": takes_effect});
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
        if let Some(error) = frame.get("error") {
            // DEL-01-01: a trusted entry sent, and Codex could not load the configuration: the project's own
            // settings file stopped the start. Other refusals are left as they are.
            if let Some(mut refusal) = bound.trust.as_ref().and_then(|trust| cl::project_settings_refusal(trust, error)) {
                let thread = match &bound.target { Target::Conversation(t) | Target::ForkOf(t) => Some(t.clone()), Target::New => None };
                refusal["method"] = json!(e.request.frame["method"]);
                refusal["requestRef"] = json!(request_ref);
                refusal["threadId"] = json!(thread);
                refusal["at"] = json!(now_rfc3339());
                let offs = i.level.project_trust.as_ref().map_or(0, |projects| projects.offs());
                if let Target::Conversation(t) = &bound.target { i.level.thread_settings_refusal.insert(t.clone(), (refusal.clone(), offs)); }
                i.level.settings_refusal = Some((refusal, offs));
            }
            i.level.request_sent.remove(key);
            i.level.sent_by_request.remove(key);
            return;
        }
        // A later start, resume or fork of the same conversation or project that Codex accepted: the refusal no
        // longer stands.
        if let Some(trust) = &bound.trust {
            let root = json!(trust.root.to_string_lossy());
            if i.level.settings_refusal.as_ref().is_some_and(|(r, _)| r["projectRoot"] == root) { i.level.settings_refusal = None; }
            if let Target::Conversation(t) = &bound.target { i.level.thread_settings_refusal.remove(t); }
            i.level.thread_settings_refusal.retain(|_, (r, _)| r["projectRoot"] != root);
        }
        let result = &frame["result"];
        let thread = match &bound.target {
            Target::New | Target::ForkOf(_) => result["thread"]["id"].as_str().map(str::to_owned),
            Target::Conversation(t) => Some(t.clone()),
        };
        let Some(thread) = thread.filter(|t| !t.is_empty()) else { return };
        if matches!(bound.target, Target::New | Target::ForkOf(_)) {
            let fresh = !i.thread_levels.contains_key(&thread);
            i.thread_levels.entry(thread.clone()).or_insert(bound.level);
            if let Some(origin) = bound.origin {
                let chosen = Chosen { entry:bound.chosen.clone(), at:bound.chosen_at.clone().unwrap_or_default(), level:bound.level, origin };
                i.level.thread_chosen.entry(thread.clone()).or_insert(chosen.clone());
                // This records an inherited association, not a person's new choice. Session-only choices
                // and defaults selected while records were unreadable never acquire a durable association.
                if fresh && !matches!(origin, Origin::SessionOnly | Origin::SaveUnconfirmed) && i.level.session_only.is_none() {
                    let entry_id = opaque_id("level-inherited:").unwrap_or_default();
                    i.level.inherited.insert(thread.clone(), entry_id.clone());
                    if !entry_id.is_empty() {
                        if let Some(home) = Self::level_home(i) {
                            Self::queue_level_entry(i, json!({"kind":"level_inherited", "session":i.app_session,
                                "entryId":entry_id,"at":now_rfc3339(),"scope":{"kind":"conversation","home":home,"threadId":thread},
                                "level":cl::recorded_values(bound.level),"origin":origin.as_str(),"chosen":chosen.entry,
                                "chosenAt":if origin==Origin::AppDefault {Value::Null} else {json!(chosen.at)}}));
                        }
                    }
                }
            }
            if let Some(row) = i.level.request_sent.remove(key) { i.level.last_sent.insert(thread.clone(), row); }
            if let Some(chosen) = bound.chosen.clone() {
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
        i.level.reported.insert(thread.clone(), json!({"from": from, "at": at, "requestRef": request_ref, "requestedLevelId": bound.level.id,
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
    /// A failed launch read permits an in-session fallback. No usable writer means established
    /// non-persistence; an attempted append error means saving is unconfirmed, possibly after commit.
    /// Without fallback, a failed append leaves the current level unchanged and reports the uncertainty.
    pub(crate) fn choose_level(&self, scope: &LevelScope, level: &'static Level, also: &[Arc<Host>]) -> Result<Value, String> {
        let _writer = self.recovery_writer.lock().unwrap();
        self.drain_recovery_owned();
        let (ledger, session, home, session_only) = {
            let i = self.inner.0.lock().unwrap();
            (i.recovery.clone(), i.app_session.clone(), i.level.places.as_ref().and_then(|p| p.home_identity.clone()), i.level.session_only.is_some())
        };
        let entry_id = opaque_id("level-chosen:")?;
        let at = now_rfc3339();
        let scope_view = match scope { LevelScope::Default => json!("default"), LevelScope::Conversation(t) => json!({"conversation": t}) };
        if let LevelScope::Conversation(thread) = scope {
            let known = self.inner.0.lock().unwrap().threads.iter().any(|t| t["threadId"] == thread.as_str());
            if !known { return Err("The conversation is not one this Codex home has open; the level was not changed".into()); }
        }
        // The App's records could not be read at launch, and this choice cannot be saved: held for this session.
        let for_this_session = |failure: Option<String>| -> Result<Value, String> {
            let attempted = failure.is_some();
            let chosen = Chosen { entry: None, at: at.clone(), level, origin: if attempted { Origin::SaveUnconfirmed } else { Origin::SessionOnly } };
            Self::apply_chosen(&mut self.inner.0.lock().unwrap(), scope, chosen.clone());
            if *scope == LevelScope::Default {
                for other in also.iter().filter(|h| !std::ptr::eq(Arc::as_ptr(h), self)) {
                    Self::apply_chosen(&mut other.inner.0.lock().unwrap(), scope, chosen.clone());
                }
            }
            let outcome = json!({"state": "chosen", "scope": scope_view, "levelId": level.id, "ledgerEntry": null,
                "origin": chosen.origin.as_str(), "applied": true,
                "recorded": if attempted { "not-confirmed" } else { "not-recorded" },
                "sentence": if attempted { cl::SAVE_UNCONFIRMED_APPLIED } else { cl::SESSION_ONLY_SENTENCE },
                "writeFailure": failure.map(|text| json!({"text": text, "standing": cl::NOT_THE_APPS_TEXT}))});
            self.inner.0.lock().unwrap().level.choice_save = Some(outcome.clone());
            if *scope == LevelScope::Default { for other in also.iter().filter(|h| !std::ptr::eq(Arc::as_ptr(h), self)) {
                other.inner.0.lock().unwrap().level.choice_save = Some(outcome.clone());
            }}
            Ok(outcome)
        };
        let ledger_scope = match scope {
            LevelScope::Default => json!({"kind": "default-for-new-conversations"}),
            LevelScope::Conversation(thread) => match &home {
                Some(home) => json!({"kind": "conversation", "home": home, "threadId": thread}),
                None if session_only => return for_this_session(None),
                None => return Err("This conversation's Codex home is not established; the level was not changed".into()),
            },
        };
        let mut entry = json!({"kind": "level_chosen", "session": session, "entryId": entry_id, "at": at, "scope": ledger_scope,
            "level": cl::recorded_values(level), "previous": null});
        let Some(ledger) = ledger else {
            if session_only { return for_this_session(None); }
            return Err("The App ledger is unavailable, so the level could not be recorded; nothing was changed".into());
        };
        let chosen = Chosen { entry: Some(entry_id.clone()), at: at.clone(), level, origin: Origin::Chosen };
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
            self.inner.0.lock().unwrap().level.choice_save = Some(json!({"scope":scope_view,"levelId":level.id,
                "recorded":"not-confirmed","applied":false,"sentence":cl::SAVE_UNCONFIRMED_NOT_APPLIED,
                "writeFailure":{"text":e,"standing":cl::NOT_THE_APPS_TEXT}}));
            return Err(cl::SAVE_UNCONFIRMED_NOT_APPLIED.into());
        }
        Self::apply_chosen(&mut self.inner.0.lock().unwrap(), scope, chosen.clone());
        if *scope == LevelScope::Default {
            for other in also.iter().filter(|h| !std::ptr::eq(Arc::as_ptr(h), self)) {
                Self::apply_chosen(&mut other.inner.0.lock().unwrap(), scope, chosen.clone());
            }
        }
        let outcome = json!({"state":"chosen","scope":scope_view,"levelId":level.id,"ledgerEntry":entry_id,
            "previous":entry["previous"],"origin":"chosen","recorded":"recorded","applied":true});
        self.inner.0.lock().unwrap().level.choice_save = Some(outcome.clone());
        if *scope == LevelScope::Default { for other in also.iter().filter(|h| !std::ptr::eq(Arc::as_ptr(h), self)) {
            other.inner.0.lock().unwrap().level.choice_save = Some(outcome.clone());
        }}
        Ok(outcome)
    }

    /// The one change of the level in force for a scope. Called only by [`Self::choose_level`] (a recorded or a
    /// session-only choice) and [`Self::read_levels_at_launch`] (a recorded choice, or the App's default).
    fn apply_chosen(i: &mut Inner, scope: &LevelScope, chosen: Chosen) {
        if let Some(entry) = &chosen.entry { i.level.by_entry.insert(entry.clone(), chosen.clone()); }
        match scope {
            LevelScope::Default => {
                // A level in force for the default scope answers a missing record.
                i.level.record_missing = false;
                i.default_level = Some(chosen.level); i.level.default_chosen = Some(chosen);
            }
            LevelScope::Conversation(t) => { i.level.inherited.remove(t); i.level.thread_asks.remove(t); i.thread_levels.insert(t.clone(), chosen.level); i.level.thread_chosen.insert(t.clone(), chosen); }
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
    /// (`codex_level::DEFAULT_LEVEL`) applies subject to the account-home evidence, shown as the App's default
    /// and never written as a choice. Failed reads preserve known levels; a first run established by absent
    /// Codex state can use the default with its unread-records disclosure, otherwise the person is asked.
    /// A complete read drops every session-only choice. `home` is this Host's `home_identity`.
    pub(crate) fn read_levels_at_launch(&self, home: Option<&str>) -> Value {
        self.read_levels_at_launch_in(home, None)
    }

    /// Select from a fresh, guarded, fully validated cut of this session's original ledger, under its writer.
    /// No recorded choice means only that none was found, not that the person never chose. With no earlier
    /// session entry and earlier Codex state in the account home, ask rather than take the default. A failed
    /// home probe is unknown, never absence. Individual entry removal/replacement by an outside writer is not
    /// detected (LIM-022); ordinary failed writes and detected corruption are not excluded by that limitation.
    /// A failed fresh read preserves levels already known and exposes its failure beside any first-run default.
    /// The home is probed by one symlink_metadata call; no file contents or other folder are read.
    pub(crate) fn read_levels_at_launch_in(&self, home: Option<&str>, codex_home: Option<&std::path::Path>) -> Value {
        self.read_levels_with_account_state(home, codex_home.map(cl::home_has_codex_state))
    }
    pub(crate) fn read_levels_with_account_state(&self, home: Option<&str>, home_state: Option<Result<bool, String>>) -> Value {
        // Selection and a person's choice share the existing writer; no selection can overtake a choice.
        let _writer = self.recovery_writer.lock().unwrap();
        self.drain_recovery_owned();
        let home_unknown = home_state.as_ref().and_then(|state| state.as_ref().err()).map(|error|
            json!({"state":"unknown", "detail":{"text":error,"standing":cl::NOT_THE_APPS_TEXT}}));
        let (ledger, limit) = {
            let i = self.inner.0.lock().unwrap();
            (i.recovery.clone(), i.recovery_initialization_error.clone())
        };
        let unreadable = |detail: String| (cl::RECORDS_NOT_READ.to_owned(),
            json!({"reason":cl::RECORDS_NOT_READ,"detail":{"text":detail,"standing":cl::NOT_THE_APPS_TEXT}}));
        let read = match (ledger, limit) {
            (Some(ledger), None) => ledger.lock().unwrap().read_current_entries().map(|(_, rows)| rows).map_err(unreadable),
            (_, Some(limit)) => Err(unreadable(limit)),
            (None, None) => Err((cl::RECORDS_UNAVAILABLE.to_owned(),
                json!({"reason": cl::RECORDS_UNAVAILABLE, "detail": null}))),
        };
        let rows = match read {
            Ok(rows) => rows,
            Err((reason, session_only)) => {
                let mut view = json!({"state": "not-read", "reason": reason});
                if let Some(state) = &home_unknown { view["homeState"] = state.clone(); }
                let mut i = self.inner.0.lock().unwrap();
                i.level.session_only = Some(session_only);
                // The App's default only on positive evidence of a first run: this home holds no state from an earlier
                // Codex start. Otherwise the ask, with the session-only choice.
                if let Some(level) = i.level.app_default.0.filter(|_| i.default_level.is_none()) {
                    if matches!(home_state, Some(Ok(false))) {
                        Self::apply_chosen(&mut i, &LevelScope::Default, Chosen { entry: None, at: now_rfc3339(), level, origin: Origin::AppDefault });
                        i.level.records_unread = true;
                        view["appDefault"] = json!(level.id);
                    } else {
                        i.level.record_missing = true;
                        view["recordMissing"] = json!(cl::RECORD_MISSING_SENTENCE);
                    }
                }
                i.level.launch = view.clone();
                return view;
            }
        };
        let mut latest: Vec<(LevelScope, Value)> = Vec::new();
        for row in rows.iter().filter(|r| matches!(r["kind"].as_str(), Some("level_chosen" | "level_inherited"))) {
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
        i.level.choice_save = None;
        let mut dropped = false;
        if i.level.default_chosen.as_ref().is_some_and(|c| matches!(c.origin, Origin::SessionOnly | Origin::SaveUnconfirmed)) { i.default_level = None; i.level.default_chosen = None; dropped = true; }
        let session_threads: Vec<String> = i.level.thread_chosen.iter().filter(|(_, c)| matches!(c.origin, Origin::SessionOnly | Origin::SaveUnconfirmed)).map(|(t, _)| t.clone()).collect();
        for t in session_threads { i.thread_levels.remove(&t); i.level.thread_chosen.remove(&t); dropped = true; }
        if dropped { i.level_revision += 1; }
        let mut default_accepted = false;
        let mut default_refused = false;
        i.level.thread_asks.clear();
        i.level.records_unread = false;
        for (scope, row) in latest {
            let entry = row["entryId"].as_str().unwrap_or_default().to_owned();
            match cl::accept_recorded(&row["level"]) {
                Some(level) => {
                    let inherited = row["kind"] == "level_inherited";
                    let chosen = if inherited {
                        Chosen {entry:row["chosen"].as_str().map(str::to_owned), at:row["chosenAt"].as_str().unwrap_or_default().to_owned(), level,
                            origin:if row["origin"]=="app-default" {Origin::AppDefault} else {Origin::Chosen}}
                    } else { Chosen { entry: Some(entry.clone()), at: row["at"].as_str().unwrap_or_default().to_owned(), level, origin: Origin::Chosen } };
                    if scope == LevelScope::Default { default_accepted = true; }
                    Self::apply_chosen(&mut i, &scope, chosen);
                    if inherited { if let LevelScope::Conversation(thread) = &scope {
                        i.level.inherited.insert(thread.clone(), entry.clone());
                        i.level.inherited_read.insert(entry.clone());
                    }}
                    accepted.push(json!({"entryId": entry, "levelId": level.id}));
                }
                None => {
                    // No level for this scope: the recorded level is withdrawn, not replaced by another.
                    // A record that cannot be used is asked about, never answered by the App's default: a spoiled record
                    // must not raise a level as a removed one would.
                    match &scope {
                        LevelScope::Default => { i.default_level = None; i.level.default_chosen = None; default_refused = true; }
                        LevelScope::Conversation(t) => { i.thread_levels.remove(t); i.level.thread_chosen.remove(t); i.level.thread_asks.insert(t.clone()); }
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
        if let Some(state) = &home_unknown { view["homeState"] = state.clone(); }
        i.level.record_missing = false;
        // The default where no usable choice was found, subject to the explicit missing/unknown-state cases.
        if let (false, Some(level)) = (default_accepted, i.level.app_default.0) {
            let current = i.app_session.clone();
            let used_before = rows.iter().any(|r| r["session"].as_str().is_some_and(|s| s != current));
            if default_refused || home_unknown.is_some() || (!used_before && matches!(home_state, Some(Ok(true)))) {
                i.default_level = None;
                i.level.default_chosen = None;
                i.level_revision += 1;
                // No earlier session in the record, yet this home holds state from an earlier Codex start: the
                // record of the level is missing, not a first run.
                i.level.record_missing = true;
                view["recordMissing"] = json!(cl::RECORD_MISSING_SENTENCE);
            } else {
                Self::apply_chosen(&mut i, &LevelScope::Default, Chosen { entry: None, at: now_rfc3339(), level, origin: Origin::AppDefault });
                view["appDefault"] = json!(level.id);
            }
        }
        i.level.launch = view.clone();
        view
    }

    // ---- Status ----

    pub(super) fn level_status(i: &Inner, status: &mut Value) {
        let session_only = i.level.session_only.as_ref();
        status["levelDefaultScopeSentence"] = json!(cl::DEFAULT_SCOPE_SENTENCE);
        status["levelChoiceSave"] = json!(i.level.choice_save);
        status["levelDefault"] = chosen_view(i.level.default_chosen.as_ref(), i.default_level, "default", session_only);
        status["levelStartRefusal"] = json!(i.level.start_refusal);
        status["levelSendRefusal"] = json!(i.level.last_refusal);
        // A refusal noted before the person's latest switch off no longer stands.
        let offs = i.level.project_trust.as_ref().map_or(0, |projects| projects.offs());
        let standing = |noted: &(Value, u64)| (noted.1 == offs).then(|| noted.0.clone());
        status["projectSettingsRefusal"] = json!(i.level.settings_refusal.as_ref().and_then(standing));
        status["levelLaunchRead"] = i.level.launch.clone();
        status["levelRecordMissing"] = if i.level.record_missing { json!(cl::RECORD_MISSING_SENTENCE) } else { Value::Null };
        // The level preselected in the ask: the App's default, one press away.
        status["levelAskPreselected"] = if i.level.record_missing || !i.level.thread_asks.is_empty() { json!(i.level.app_default.0.map(|l| l.id.as_str())) } else { Value::Null };
        status["levelRecordsUnread"] = if i.level.records_unread && i.level.default_chosen.as_ref().is_some_and(|c| c.origin == Origin::AppDefault) { json!(cl::RECORDS_UNREAD_SENTENCE) } else { Value::Null };
        status["levelAppDefault"] = json!(i.level.app_default.0.map(|l| l.id.as_str()));
        // Offered only when the launch read positively failed or was limited.
        status["levelSessionOnlyOffered"] = json!(session_only);
        if let Some(threads) = status["threads"].as_array_mut() {
            for row in threads.iter_mut() {
                let Some(t) = row["threadId"].as_str().map(str::to_owned) else { continue };
                let own = i.thread_levels.get(&t).copied();
                let asked = own.is_none() && i.level.thread_asks.contains(&t);
                let chosen = match own {
                    Some(level) => chosen_view(i.level.thread_chosen.get(&t), Some(level), "conversation", session_only),
                    None if asked => Value::Null,
                    None => chosen_view(i.level.default_chosen.as_ref(), i.default_level, "default", session_only),
                };
                let in_force = if asked { None } else { own.or(i.default_level) };
                let sent = i.level.last_sent.get(&t).cloned();
                let reported = i.level.reported.get(&t).cloned();
                // Confirmed only by a start, resume or fork reply for the level now in force: a change sent on a turn
                // is not confirmed until the next such reply.
                let agreement = match (&reported, in_force) {
                    (Some(r), Some(level)) if r["requestedLevelId"] == level.id.as_str() => r["agreement"].clone(),
                    _ => json!("not-confirmed"),
                };
                let changed = match (&sent, in_force) { (Some(s), Some(level)) => s["levelId"] != level.id.as_str(), _ => false };
                let takes_effect = if changed && Self::current_live_turn(i, &t).is_some() { "from-next-turn" } else { "now" };
                let project_trust = sent.as_ref().map(|s| s["projectTrust"].clone()).filter(|v| !v.is_null());
                let mut level = json!({"chosen": chosen, "sent": sent, "reported": reported, "agreement": agreement, "takesEffect": takes_effect});
                if level["chosen"]["scope"] == "default" { level["scopeSentence"] = json!(cl::FOLLOWS_DEFAULT_SENTENCE); }
                if takes_effect == "from-next-turn" { level["takesEffectSentence"] = json!(cl::NEXT_TURN_SENTENCE); }
                if let Some(entry) = i.level.inherited.get(&t) {
                    let recorded = i.level.inherited_read.contains(entry) || i.recovery_snapshot.as_ref()
                        .is_some_and(|cut| cut.rows.iter().any(|row| row["kind"]=="level_inherited" && row["entryId"]==*entry));
                    if !recorded {
                        let failure = i.recovery_error.as_ref().or(i.recovery_initialization_error.as_ref());
                        if failure.is_some() || i.recovery.is_none() || entry.is_empty() {
                            level["inheritancePersistence"] = json!({"state":"not-confirmed","sentence":cl::INHERITANCE_NOT_RECORDED,
                                "detail":failure.map(|text|json!({"text":text,"standing":cl::NOT_THE_APPS_TEXT}))});
                        } else { level["inheritancePersistence"] = json!({"state":"pending"}); }
                    }
                }
                if let Some(trust) = project_trust { level["projectTrust"] = trust; }
                if let Some(refusal) = i.level.thread_settings_refusal.get(&t).and_then(standing) { level["projectSettingsRefusal"] = refusal; }
                if let Some(cause) = i.level.refused.get(&t) { level["refused"] = cause.clone(); }
                // This conversation's recorded level could not be used: the ask, with the App's default preselected.
                if asked { level["ask"] = json!({"sentence": cl::RECORD_MISSING_SENTENCE, "preselected": i.level.app_default.0.map(|l| l.id.as_str())}); }
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
    ///
    /// DEL-01-01: the App's own choice for the project the folder is (`project_trust`) is read here too, just
    /// after the settings, and joins the case table (`codex_level::TrustReading::row`). A folder that is not the
    /// App's project carries no choice, and today's rule applies.
    pub(super) fn trust_reading(&self, method: &str, params: &Value, generation: Option<&Value>) -> Option<cl::TrustReading> {
        let mut reading = self.trust_reading_settings(method, params, generation)?;
        let projects = self.project_trust.lock().unwrap().clone();
        if let Some(projects) = &projects { reading.choice = projects.choice_for(&reading.cwd); }
        self.inner.0.lock().unwrap().level.project_trust = projects;
        Some(reading)
    }

    /// DEL-01-01: every home made from this Host's App custody applies `projects` from its next start, resume or
    /// fork.
    pub(crate) fn configure_project_trust(&self, projects: Arc<crate::project_trust::ProjectTrust>) {
        *self.project_trust.lock().unwrap() = Some(projects);
    }
    pub(crate) fn project_trust(&self) -> Option<Arc<crate::project_trust::ProjectTrust>> {
        self.project_trust.lock().unwrap().clone()
    }

    fn trust_reading_settings(&self, method: &str, params: &Value, generation: Option<&Value>) -> Option<cl::TrustReading> {
        if !matches!(cl::Method::of(method)?, cl::Method::ThreadStart | cl::Method::ThreadResume | cl::Method::ThreadFork) { return None; }
        let (cwd, generation, epoch) = {
            let i = self.inner.0.lock().unwrap();
            let thread = params["threadId"].as_str();
            let process_cwd = i.level.places.as_ref().and_then(|p| p.process_cwd.clone());
            let cwd = params.get("cwd").and_then(Value::as_str).map(PathBuf::from)
                .or_else(|| thread.and_then(|t| i.threads.iter().rev().find(|r| r["threadId"] == t).and_then(|r| r["cwd"].as_str()).map(PathBuf::from)))
                .or_else(|| (method == "thread/start").then(|| process_cwd.clone()).flatten());
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
        #[cfg(test)]
        let budget = self.inner.0.lock().unwrap().level.trust_budget.unwrap_or(reading_gate::READING_DEFAULT_BUDGET);
        #[cfg(not(test))]
        let budget = reading_gate::READING_DEFAULT_BUDGET;
        let deadline = std::time::Instant::now() + budget;
        // The reading's write and its reply wait run on a worker, so that the start waits for them only until the one
        // deadline, even when the write itself is blocked; a reading that has not completed by then is not used (the
        // entry goes untrusted), and its late completion changes nothing. Without the Host's own handle (some unit
        // tests' Hosts), it runs here under the same deadline for each phase.
        let round = {
            let host = self.this.lock().unwrap().upgrade();
            let (cwd_text, generation_for) = (cwd.to_string_lossy().into_owned(), generation.clone());
            match host {
                Some(host) => {
                    let (tx, rx) = std::sync::mpsc::channel();
                    std::thread::Builder::new().name("chirality-trust-reading".into()).spawn(move || {
                        let _ = tx.send(host.trust_reading_round(&cwd_text, &generation_for, deadline));
                    }).map_err(|e| format!("the trust reading could not start: {e}"))
                        .and_then(|_| rx.recv_timeout(deadline.saturating_duration_since(std::time::Instant::now()))
                            .map_err(|_| cl::TRUST_READ_TIMED_OUT.to_string())
                            .and_then(|round| round))
                }
                None => self.trust_reading_round(&cwd_text, &generation_for, deadline),
            }
        };
        let (request_ref, response) = match round {
            Ok(round) => round,
            Err(error) if error == cl::TRUST_READ_TIMED_OUT => return Some(cl::TrustReading::not_read(cwd, cl::TRUST_READ_TIMED_OUT, None)),
            Err(error) => return Some(cl::TrustReading::not_read(cwd, cl::TRUST_READ_FAILED, Some(error))),
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
                reading.request_ref = Some(request_ref);
                reading.read_at = Some(now_rfc3339());
            }
            Err(reason) => reading.case = cl::TrustCase::NotRead { reason, detail: None },
        }
        Some(reading)
    }

    /// One trust reading's request and reply, each phase within `deadline`. Returns the request's reference and the
    /// reply.
    fn trust_reading_round(&self, cwd: &str, generation: &Value, deadline: std::time::Instant) -> Result<(String, Value), String> {
        let params = json!({"cwd": cwd, "includeLayers": true});
        let request = self.request_reading("config/read", params, json!({"kind":"person-directed","name":TRUST_READING_INITIATOR}), generation, true, deadline)?;
        match self.wait_source_response(&request, deadline.saturating_duration_since(std::time::Instant::now())) {
            Ok(response) => Ok((request.request_ref.clone(), response)),
            Err(error) => { self.delegation_wait_ended(&request); Err(error) }
        }
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
