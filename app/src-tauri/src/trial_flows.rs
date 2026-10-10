//! Workflow trial flows in the Rust host (WR §4.2 TT-2…TT-13, §5.5, §6 SQ-DT,
//! SQ-FT, SQ-BB; §17 steps 5–7), under the owner's OI-008 ruling: the host
//! prepares every trial message, sends it only on the person's Send, writes
//! the trial link on Codex's acknowledgment, reads Codex's history for linking,
//! fidelity, bring-back and Compare, and keeps the trial records. The web view
//! presents what `decorate_status` reports and names a trial back by its
//! reference.
//!
//! A trial is never a workflow run, registration, checking or acceptance
//! (TT-2): nothing here selects a workflow, opens a run, writes a `run_text`
//! or `supply_check`, or offers Start or End run.
use super::{current_conversation, HomeSession, RunLifecycle, WorkflowRootSession};
use crate::workflow_trial_transcript::{self as transcript, TranscriptInput, TranscriptSource, TrialTextLine, TurnRead};
use crate::workflow_workspace::package_copy::{self, CopyStanding};
use crate::workflow_workspace::registration::drafts::trials::{PreparedTrial, SentTrial, TrialKind, TrialObservation};
use crate::workflow_workspace::{FidelityReading, Snapshot, TrialText, TRIAL_AREA};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::sync::Mutex;
use std::time::Duration;

/// Who a workspace read is journalled as: the person (Read again, Bring back,
/// Compare) or the App rule of TT-9's linking read on the host tick (H-4).
pub(crate) fn person_read() -> Value {
    json!({"kind":"person-directed"})
}
pub(crate) fn rule_read() -> Value {
    json!({"kind":"app-rule","name":"trial-linking-read"})
}
/// How long one history page read waits for Codex.
const READ_WAIT: Duration = Duration::from_secs(10);
/// Pages read per list at most (a list that goes on is named incomplete).
const MAX_PAGES: usize = 100;
/// Linking reads done per tick at most; the rest wait for the next tick.
const READS_PER_TICK: usize = 4;

/// NPTD §7.1 (R21-1's order) for the authoring conversation: `signals` are
/// `model_multi_agent_version` (`model/list`), `effective_config`
/// (`config/read`) and `provider_capabilities` (`modelProvider/capabilities/read`).
/// The App reads none of these yet, so in the App the reading is *not
/// established*; Try with the authoring agent is then offered with that note.
pub(crate) fn delegation_availability(signals: Option<&Value>) -> Value {
    const UNREAD: &str = "not established: this App does not read the model's multiAgentVersion (model/list), the provider's namespaceTools (modelProvider/capabilities/read) or features.multi_agent (config/read) yet (NPTD §7.1); the authoring agent may be unable to start a sub-agent";
    let Some(s) = signals else {
        return json!({"reading":"not established","reason":UNREAD});
    };
    let version = &s["model_multi_agent_version"];
    let config = &s["effective_config"];
    let caps = &s["provider_capabilities"];
    if version == "disabled" {
        return json!({"reading":"missing","reason":"the selected model's multiAgentVersion is disabled (NPTD §7.1 (1)); use Try in a fresh conversation"});
    }
    if config["features"]["multi_agent"] == false {
        return json!({"reading":"missing","reason":"the effective configuration sets features.multi_agent = false (NPTD §7.1 (2)); use Try in a fresh conversation"});
    }
    if caps["namespaceTools"] == false {
        return json!({"reading":"missing","reason":"the provider reports namespaceTools false, so Codex sends no delegation tools (NPTD §7.1 (3)); use Try in a fresh conversation"});
    }
    let version_read = version == "v1" || version == "v2";
    if !version_read || !config.is_object() || caps["namespaceTools"] != true {
        return json!({"reading":"not established","reason":"not established: one of multiAgentVersion, the effective configuration or namespaceTools was not read (NPTD §7.1 (4))"});
    }
    json!({"reading":"present","reason":null})
}

fn kind_text(kind: TrialKind) -> &'static str {
    match kind {
        TrialKind::Delegated => "delegated",
        TrialKind::Clean => "clean",
    }
}
fn rev12(value: &str) -> &str {
    &value[..value.len().min(12)]
}
/// A refusal the Host made before any frame was written (nothing reached Codex).
fn not_written(reason: &str) -> bool {
    reason.starts_with("refused-not-sent")
        || reason.contains("conversation-not-loaded")
        || reason.starts_with("conversation selection is stale")
        || reason.starts_with("conversation is not loaded")
}

/// Codex answered the `turn/start` with an error: a definite refusal, no turn.
fn refused(reason: &str) -> bool {
    reason.starts_with("turn/start native error")
}

/// A trial pre-filled and not yet sent (§5.5 *pre-filled*). Process memory only.
struct PendingTrial {
    prepared: PreparedTrial,
    kind: TrialKind,
    library: String,
    draft: String,
    /// The authoring conversation (generation, thread).
    authoring: Option<(Value, String)>,
    /// A clean trial's conversation once started (its message not yet sent).
    clean: Option<(Value, String)>,
    client: String,
    message: String,
    work_folder: String,
    delegation: Option<Value>,
    run_in_force: Option<String>,
    in_flight: bool,
}
/// A trial whose message Codex acknowledged in this process: what TT-9's
/// automatic reads need.
struct SentState {
    reference: String,
    kind: TrialKind,
    text: TrialText,
    home: String,
    generation: Value,
    authoring: String,
    turn: Option<String>,
    clean: Option<String>,
    client: String,
    /// Descendants already in the native view when the message was sent.
    baseline: BTreeSet<String>,
    /// Children read (TT-9): Ok(given this trial's workflow) or the failure
    /// with the child's descendant node as it was when read (a child whose
    /// first turn was not in Codex's history yet is read again only after the
    /// view shows new activity of it).
    read: BTreeMap<String, Result<bool, (String, String)>>,
    /// Further children whose first input carried this trial's begin marker.
    also_given: BTreeSet<String>,
    /// A clean trial's first-turn fidelity read was made.
    fidelity_read: bool,
}
/// A bring-back transcript pre-filled and not yet sent (TT-10).
struct PendingBringBack {
    trial: Option<String>,
    run: Option<String>,
    target: (Value, String),
    prompt: String,
    transcript: String,
    card: String,
    shortenings: Vec<String>,
    include_native: bool,
    client: String,
    in_flight: bool,
}

/// Trial state the host keeps in process memory beside the trial link store.
#[derive(Default)]
pub(crate) struct TrialDesk {
    pending: BTreeMap<String, PendingTrial>,
    sent: BTreeMap<String, SentState>,
    bring_backs: BTreeMap<String, PendingBringBack>,
    /// Trial conversation marks (WR §3): clean trial conversations from their
    /// start and forks of them, kept in the App data folder.
    marks: crate::workflow_workspace::registration::drafts::trials::TrialConversationMarks,
    /// Problems writing marks, shown with the trial pointer limits.
    limits: Vec<String>,
    /// Runs for which a `Workflow finished:` line raises no End-run offer: a
    /// trial of a draft of the run's own workflow was sent during the run (TT-2).
    finished_offer_suppressed: BTreeSet<String>,
}

/// One automatic TT-9 read due at a tick.
pub(crate) enum TrialRead {
    Child { reference: String, generation: Value, child: String },
    CleanFirstTurn { reference: String, generation: Value, thread: String, turn: String, client: String },
}
pub(crate) struct TrialReadResult {
    read: TrialRead,
    texts: Result<Vec<String>, String>,
}

impl WorkflowRootSession {
    fn listed_content(&self, library: &str, name: &str) -> Option<String> {
        self.drafts
            .get(library)
            .and_then(|l| l.observation.drafts.iter().find(|d| d["name"] == name))
            .and_then(|d| d["content"]["value"].as_str().map(str::to_owned))
    }
    /// The trial link of `reference` and the library holding its draft.
    fn link_and_library(&self, reference: &str) -> Result<(Value, std::sync::Arc<super::WorkflowLibraryContext>), String> {
        let link = self.trials.link(reference).cloned().ok_or_else(|| format!("No trial link {reference} in this App"))?;
        let library = self
            .libraries
            .values()
            .find(|l| l.owner.try_lock().is_ok_and(|o| o.draft_key(link["draft"]["name"].as_str().unwrap_or_default()) == link["draft"]))
            .cloned()
            .ok_or("The library holding this trial's draft is not open in this App; open it first")?;
        Ok((link, library))
    }
    /// The trial text of a sent trial: kept in this process, or recomposed from
    /// the trial snapshot folder (TT-8) and checked against the link's identity.
    fn trial_text(&self, reference: &str) -> Result<TrialText, String> {
        if let Some(sent) = self.trial_desk.sent.get(reference) {
            return Ok(sent.text.clone());
        }
        let (link, library) = self.link_and_library(reference)?;
        let trial = &link["trial"];
        let name = link["draft"]["name"].as_str().unwrap_or_default();
        let content = link["content"]["value"].as_str().unwrap_or_default();
        let folder = package_copy::content_folder(&library.root, TRIAL_AREA, name, content);
        let snapshot = Snapshot::capture(&folder).map_err(|e| format!("trial text not recomposed: trial snapshot not readable ({e})"))?;
        if snapshot.revision() != content {
            return Err("trial text not recomposed: trial snapshot changed after the trial".into());
        }
        let text = TrialText::compose(
            &library.origin,
            &library.source_root,
            name,
            &snapshot,
            trial["sequence"].as_u64().unwrap_or(0),
            reference,
            trial["snapshot_folder"].as_str().unwrap_or_default(),
        )?;
        if text.identity() != trial["text_identity"] {
            return Err("trial text not recomposed: the recomposed text differs from the text this trial sent".into());
        }
        Ok(text)
    }

    /// TT-3, TT-3a, TT-3b, TT-8: Try pressed on draft `name`. Takes the trial
    /// snapshot, composes the trial text and keeps the pre-filled message in
    /// this process; nothing is sent or recorded (§5.5 *pre-filled*).
    /// `authoring` is the conversation selected when Try was pressed (required
    /// for a delegated trial).
    pub fn prepare_trial(
        &mut self,
        kind: &str,
        name: &str,
        authoring: Option<(&Value, &str)>,
        home: Option<&HomeSession>,
        project: Option<&std::path::Path>,
    ) -> Result<Value, String> {
        self.prepare_trial_with(kind, name, authoring, home, project, None)
    }
    pub(crate) fn prepare_trial_with(
        &mut self,
        kind: &str,
        name: &str,
        authoring: Option<(&Value, &str)>,
        home: Option<&HomeSession>,
        project: Option<&std::path::Path>,
        delegation_signals: Option<&Value>,
    ) -> Result<Value, String> {
        let kind = match kind {
            "delegated" => TrialKind::Delegated,
            "clean" => TrialKind::Clean,
            other => return Err(format!("{other:?} is not a trial kind (delegated or clean)")),
        };
        let library = self.active_library()?;
        let listed = self.listed_content(&library.reference, name).ok_or_else(|| {
            format!("No listed draft named {name} with a content identity; refresh the draft list. Nothing pre-filled")
        })?;
        let mut delegation = None;
        let mut run_in_force = None;
        if let Some((generation, thread)) = authoring {
            let home = home.ok_or("Codex home not available; nothing pre-filled")?;
            current_conversation(&home.host.snapshot(), generation, thread).map_err(|e| format!("{e}; nothing pre-filled"))?;
            let home_key = generation["home"].as_str().ok_or("generation home required")?;
            if self.trial_conversation(thread).is_some() {
                return Err("This conversation is a trial conversation; choose the authoring conversation instead. Nothing pre-filled".into());
            }
            if let Some((_, run)) = self.run_in_force(home_key, thread)? {
                let name = run.try_lock().map(|r| r.prepared().workflow().name.clone()).unwrap_or_else(|_| "a workflow".into());
                run_in_force = Some(format!("{name} is in force in this conversation; the trial opens no run and {name} stays in force"));
            }
        }
        if kind == TrialKind::Delegated {
            if authoring.is_none() {
                return Err("Choose the authoring conversation for Try with the authoring agent, or use Try in a fresh conversation. Nothing pre-filled".into());
            }
            let reading = delegation_availability(delegation_signals);
            if reading["reading"] == "missing" {
                return Err(format!("Try with the authoring agent is not available: {}. Nothing pre-filled", reading["reason"].as_str().unwrap_or_default()));
            }
            delegation = Some(reading);
        }
        let owner = library.owner.try_lock().map_err(|_| "Original library owner busy/unavailable; nothing pre-filled")?;
        let key = owner.draft_key(name);
        let pending_max = self.trial_desk.pending.values().filter(|p| p.prepared.key == key).map(|p| p.prepared.text.sequence()).max().unwrap_or(0);
        let sequence = self.trials.next_sequence(&key).max(pending_max + 1);
        let home_folder = std::env::var_os("HOME").map(std::path::PathBuf::from).filter(|p| p.is_absolute());
        let prepared = owner.prepare_trial(name, &listed, sequence, project, home_folder.as_deref())?;
        drop(owner);
        let reference = prepared.text.reference().to_owned();
        let short = reference.trim_start_matches("trial:").chars().take(8).collect::<String>();
        let work_folder = format!(".chirality/trial-work/trial-{sequence}-{short}/");
        let rev = rev12(prepared.text.content()).to_owned();
        let message = match kind {
            TrialKind::Delegated => format!("Please try draft {name} (trial {sequence}, content {rev}). Start one sub-agent and give it the trial text below, exactly as written, as its task; don't follow the workflow yourself. Let it work in {work_folder} rather than in the project's files. Watch what it does, follow up with it if it gets stuck or asks, then tell me how it went: what it did, where it departed from the workflow, and what you would change in the draft."),
            TrialKind::Clean => format!("Inputs for this trial: …. Work in {work_folder} rather than in the project's files."),
        };
        let pending = PendingTrial {
            prepared,
            kind,
            library: library.reference.clone(),
            draft: name.to_owned(),
            authoring: authoring.map(|(g, t)| (g.clone(), t.to_owned())),
            clean: None,
            client: crate::util::opaque_id("trial-message:")?,
            message,
            work_folder,
            delegation,
            run_in_force,
            in_flight: false,
        };
        let view = self.pending_view(&pending);
        self.trial_desk.pending.insert(reference, pending);
        Ok(view)
    }
    /// TT-11 Try again: a new trial of the draft's current version, same kind
    /// and authoring conversation by default.
    pub fn trial_again(&mut self, reference: &str, home: Option<&HomeSession>, project: Option<&std::path::Path>) -> Result<Value, String> {
        let (link, library) = self.link_and_library(reference)?;
        if self.active_library.as_deref() != Some(library.reference.as_str()) {
            return Err("Open the library holding this draft first; nothing pre-filled".into());
        }
        let trial = &link["trial"];
        let kind = trial["kind"].as_str().unwrap_or_default().to_owned();
        let name = link["draft"]["name"].as_str().unwrap_or_default().to_owned();
        let authoring = trial["authoring_conversation"].as_str().map(str::to_owned);
        let generation = home.map(|h| h.host.snapshot()["generation"].clone());
        let current = match (&authoring, &generation, home) {
            (Some(thread), Some(generation), Some(home)) => current_conversation(&home.host.snapshot(), generation, thread).is_ok(),
            _ => false,
        };
        let authoring = if current { authoring.as_deref().zip(generation.as_ref()).map(|(t, g)| (g, t)) } else { None };
        if kind == "delegated" && authoring.is_none() {
            return Err("The authoring conversation of that trial is not loaded now; choose an authoring conversation and press Try with the authoring agent. Nothing pre-filled".into());
        }
        self.prepare_trial(&kind, &name, authoring, home, project)
    }
    /// §5.5: removing the trial card cancels the trial; nothing is recorded.
    pub fn cancel_trial(&mut self, reference: &str) -> Result<Value, String> {
        match self.trial_desk.pending.get(reference) {
            Some(p) if p.in_flight => Err("This trial message is being sent now; it can no longer be removed".into()),
            Some(_) => {
                self.trial_desk.pending.remove(reference);
                Ok(json!({"reference":reference,"state":"removed; nothing recorded"}))
            }
            None => Err(format!("No pre-filled trial {reference}")),
        }
    }
    /// FT-3: the person pressed Send on a pre-filled clean trial whose
    /// conversation is not started yet. Held until the start's outcome, so a
    /// second press starts no second conversation.
    pub fn begin_clean_start(&mut self, reference: &str) -> Result<(), String> {
        let p = self.trial_desk.pending.get_mut(reference).ok_or_else(|| format!("No pre-filled trial {reference}; press Try again"))?;
        if p.kind != TrialKind::Clean {
            return Err("Only a clean trial starts a new conversation".into());
        }
        if p.in_flight {
            return Err("This trial is being started now; nothing started again".into());
        }
        if p.clean.is_some() {
            return Err("This trial's conversation already started; send the trial message there".into());
        }
        p.in_flight = true;
        Ok(())
    }
    /// The new conversation did not start (ROLE T-2's states): still pre-filled.
    pub fn abort_clean_start(&mut self, reference: &str) {
        if let Some(p) = self.trial_desk.pending.get_mut(reference) {
            p.in_flight = false;
        }
    }
    /// A clean trial conversation was started for `reference` (FT-4): from now
    /// on that conversation is the trial's and offers no workflow run.
    pub fn mark_clean_started(&mut self, reference: &str, generation: &Value, thread: &str) {
        let Some(p) = self.trial_desk.pending.get_mut(reference) else { return };
        p.clean = Some((generation.clone(), thread.to_owned()));
        p.in_flight = false;
        let (sequence, draft) = (p.prepared.text.sequence(), p.draft.clone());
        // TT-2 "for its life": the mark outlives the pre-fill and the process.
        if let Err(cause) = self.trial_desk.marks.mark(thread, reference, sequence, &draft, None) {
            self.trial_desk.limits.push(cause);
        }
    }
    /// The new conversation's start was dispatched but its outcome or identity
    /// is not established: the pre-fill is withdrawn (nothing recorded).
    pub fn withdraw_clean_start(&mut self, reference: &str) {
        self.trial_desk.pending.remove(reference);
    }
    /// Opens the App-kept trial conversation marks (App start).
    pub(crate) fn open_trial_marks(&mut self, app_data: &std::path::Path) {
        self.trial_desk.marks = crate::workflow_workspace::registration::drafts::trials::TrialConversationMarks::open(app_data);
    }
    /// Problems of the trial conversation marks, shown beside the trial pointer limits.
    pub(crate) fn trial_mark_limits(&self) -> Vec<String> {
        self.trial_desk.marks.limits().iter().cloned().chain(self.trial_desk.limits.iter().cloned()).collect()
    }
    /// TT-3b Fork: a fork of a trial conversation (or of such a fork) is
    /// labelled "fork of trial ‹n›", has no trial link, and offers no workflow run.
    pub fn mark_fork(&mut self, source: &str, fork: &str) {
        let Some((reference, _)) = self.trial_conversation(source) else { return };
        let sequence = self.trial_sequence(&reference).parse::<u64>().unwrap_or(0);
        let draft = self.trial_draft_name(&reference);
        if let Err(cause) = self.trial_desk.marks.mark(fork, &reference, sequence, &draft, Some(source)) {
            self.trial_desk.limits.push(cause);
        }
    }
    fn trial_draft_name(&self, reference: &str) -> String {
        self.trials.link(reference).and_then(|l| l["draft"]["name"].as_str().map(str::to_owned))
            .or_else(|| self.trial_desk.pending.get(reference).map(|p| p.draft.clone()))
            .or_else(|| self.trial_desk.marks.find_trial(reference).and_then(|m| m["draft"].as_str().map(str::to_owned)))
            .unwrap_or_default()
    }
    /// The thread whose Codex home a trial's reads go to (H-5): the clean
    /// trial conversation, or the delegated trial's authoring conversation.
    pub(crate) fn trial_home_thread(&self, reference: &str) -> Option<String> {
        let link = self.trials.link(reference)?;
        let trial = &link["trial"];
        let thread = if trial["kind"] == "clean" { &trial["clean_conversation"] } else { &trial["authoring_conversation"] };
        thread.as_str().map(str::to_owned)
    }
    /// The trial a conversation belongs to as a clean trial conversation (or a
    /// fork of one): (trial reference, is a fork).
    pub(crate) fn trial_conversation(&self, thread: &str) -> Option<(String, bool)> {
        if let Some(mark) = self.trial_desk.marks.find(thread) {
            return mark["trial"].as_str().map(|r| (r.to_owned(), !mark["fork_of"].is_null()));
        }
        if let Some((reference, _)) = self.trial_desk.pending.iter().find(|(_, p)| p.clean.as_ref().is_some_and(|(_, t)| t == thread)) {
            return Some((reference.clone(), false));
        }
        self.trials
            .all_links()
            .into_iter()
            .find(|l| l["trial"]["kind"] == "clean" && l["trial"]["clean_conversation"] == thread)
            .and_then(|l| l["trial"]["reference"].as_str().map(|r| (r.to_owned(), false)))
    }
    /// The trial whose sub-agent `thread` is (its latest link), if any.
    fn trial_child(&self, thread: &str) -> Option<String> {
        self.trials.all_links().into_iter().find_map(|l| {
            let reference = l["trial"]["reference"].as_str()?;
            (self.linked_child(reference).as_deref() == Some(thread)).then(|| reference.to_owned())
        })
    }
    /// The latest linked sub-agent of a delegated trial ("the latest link or
    /// unlink stands").
    fn linked_child(&self, reference: &str) -> Option<String> {
        let latest = self
            .trials
            .observations(reference)
            .into_iter()
            .rev()
            .find(|o| o["observation"] == "sub-agent linked" || o["observation"] == "sub-agent unlinked")?;
        (latest["observation"] == "sub-agent linked").then(|| latest["child_thread"].as_str().map(str::to_owned)).flatten()
    }
    /// TT-2: why proposal and finished lines of this agent message offer
    /// nothing, if they do not: a clean trial conversation or a fork of one, a
    /// trial's sub-agent, or the turn that carries a trial message.
    pub(crate) fn trial_offer_refusal(&self, thread: &str, turn: &str) -> Option<String> {
        if let Some((reference, fork)) = self.trial_conversation(thread) {
            let n = self.trial_sequence(&reference);
            return Some(if fork {
                format!("this conversation is a fork of trial {n}; it offers no workflow start or end")
            } else {
                format!("this conversation is trial {n}; it offers no workflow start or end; start runs in another conversation")
            });
        }
        if let Some(reference) = self.trial_child(thread) {
            return Some(format!("this sub-agent is trial {}'s; its lines offer nothing", self.trial_sequence(&reference)));
        }
        self.trials
            .all_links()
            .into_iter()
            .find(|l| l["trial"]["kind"] == "delegated" && l["trial"]["authoring_conversation"] == thread && l["trial"]["turn"] == turn)
            .map(|l| format!("this turn carries trial {}'s message; its lines offer nothing", l["trial"]["sequence"]))
    }
    /// TT-2: the native view as the checkpoint recorder reads it: rows of a
    /// turn that carries a trial message and of a linked trial sub-agent are
    /// not a run's activity, so they record no checkpoint arrival.
    pub(crate) fn without_trial_activity(&self, view: &Value) -> Value {
        let links = self.trials.all_links();
        let turns: Vec<(String, String)> = links.iter().filter(|l| l["trial"]["kind"] == "delegated").filter_map(|l| {
            Some((l["trial"]["authoring_conversation"].as_str()?.to_owned(), l["trial"]["turn"].as_str()?.to_owned()))
        }).collect();
        let children: Vec<String> = links.iter().filter_map(|l| l["trial"]["reference"].as_str().and_then(|r| self.linked_child(r))).collect();
        if turns.is_empty() && children.is_empty() {
            return view.clone();
        }
        let mut filtered = view.clone();
        if let Some(items) = filtered["items"].as_array_mut() {
            items.retain(|row| {
                let thread = row["threadId"].as_str().unwrap_or_default();
                let turn = row["turnId"].as_str().unwrap_or_default();
                !children.iter().any(|c| c == thread) && !turns.iter().any(|(t, u)| t == thread && u == turn)
            });
        }
        filtered
    }
    /// TT-2: a `Workflow finished:` line raises no End-run offer for this run.
    pub(crate) fn finished_offer_suppressed(&self, run: &str) -> bool {
        self.trial_desk.finished_offer_suppressed.contains(run)
    }
    fn trial_sequence(&self, reference: &str) -> String {
        self.trials
            .link(reference)
            .map(|l| l["trial"]["sequence"].to_string())
            .or_else(|| self.trial_desk.pending.get(reference).map(|p| p.prepared.text.sequence().to_string()))
            .or_else(|| self.trial_desk.marks.find_trial(reference).map(|m| m["sequence"].to_string()))
            .unwrap_or_else(|| "?".into())
    }

    fn pending_view(&self, p: &PendingTrial) -> Value {
        let text = &p.prepared.text;
        let rev = rev12(text.content());
        let changed = match self.listed_content(&p.library, &p.draft) {
            Some(now) if now == text.content() => None,
            _ => Some("draft changed since this trial text was made; Try again for the current version"),
        };
        let place = |c: &Option<(Value, String)>| c.as_ref().map(|(g, t)| json!({"generation":g,"threadId":t}));
        json!({"reference":text.reference(),"sequence":text.sequence(),"kind":kind_text(p.kind),"draftName":p.draft,"location":text.location(),
            "content":p.prepared.content,"rev12":rev,
            "card":format!("trial {} of draft {} at content {rev} — not registered; not a workflow run",text.sequence(),p.draft),
            "header":text.header(),"text":text.text(),"textIdentity":text.identity(),"bytes":text.bytes(),"message":p.message,
            "authoring":place(&p.authoring),"cleanConversation":place(&p.clean),"delegation":p.delegation,"runInForce":p.run_in_force,
            "draftChanged":changed,"workFolder":p.work_folder,
            "state":if p.clean.is_some(){"started; trial message not sent"}else{"pre-filled"},"limit":Value::Null,
            "standing":"pre-filled, not sent: nothing is sent or recorded until you press Send; the trial text is changed by changing the draft and pressing Try again"})
    }

    /// TT-4's listing of one draft's trials with what the native view shows
    /// now (live turn, files changed outside the trial work folder) and the
    /// trial snapshot's standing (TT-8). Display only.
    fn trial_rows(&self, key: &Value, current: Option<&str>, view: &Value) -> Vec<Value> {
        let mut rows = self.trials.trials_for_draft(key, current);
        for row in rows.iter_mut() {
            let Some(reference) = row["reference"].as_str().map(str::to_owned) else { continue };
            let link = self.trials.link(&reference).cloned().unwrap_or(Value::Null);
            let sequence = link["trial"]["sequence"].as_u64().unwrap_or(0);
            let short = reference.trim_start_matches("trial:").chars().take(8).collect::<String>();
            let work = format!(".chirality/trial-work/trial-{sequence}-{short}/");
            let source = if row["kind"] == "clean" { row["trialConversation"].as_str().map(str::to_owned) } else { self.linked_child(&reference) };
            if let Some(sent) = self.trial_desk.sent.get(&reference) {
                let unread: Vec<&String> = sent.read.iter().filter(|(_, r)| r.as_ref().is_err_and(|(cause, _)| cause != IN_PROGRESS)).map(|(c, _)| c).collect();
                row["subAgent"]["alsoGiven"] = json!(sent.also_given);
                row["subAgent"]["unread"] = json!(unread);
            }
            row["live"] = json!(source.as_deref().is_some_and(|t| thread_live(view, t)));
            row["filesOutsideWorkFolder"] = match source.as_deref() {
                Some(thread) => {
                    let count = files_outside(view, thread, &work);
                    json!({"count":count,"reading":format!("files changed outside the trial work folder: {count} (from file-change items; shell writes not observed)")})
                }
                None => Value::Null,
            };
            row["workFolder"] = json!(work);
            let name = link["draft"]["name"].as_str().unwrap_or_default();
            let content = link["content"]["value"].as_str().unwrap_or_default();
            row["snapshot"] = match self.link_and_library(&reference) {
                Ok((_, library)) => match library.owner.try_lock() {
                    Ok(owner) => match owner.trial_snapshot_standing(name, content) {
                        CopyStanding::Current => json!({"state":"current","reading":"trial snapshot holds the tried version"}),
                        CopyStanding::Changed(cause) => json!({"state":"changed","reading":format!("trial snapshot changed after the trial: {cause}")}),
                        CopyStanding::NotAvailable(cause) => json!({"state":"not available","reading":cause}),
                    },
                    Err(_) => json!({"state":"not available","reading":"library owner busy; not read now"}),
                },
                Err(cause) => json!({"state":"not available","reading":cause}),
            };
        }
        rows
    }

    /// The trial part of `host_status`'s `workflowRoot` (a read: nothing is
    /// recorded or sent here). Replaces each listed draft's trial rows with
    /// TT-4's listing, and adds the pre-filled trials and bring-backs, the
    /// trial conversation headers, trial turn and sub-agent labels, and each
    /// draft review's last clean trial line (TT-13).
    pub fn decorate_status(&self, root: &mut Value, view: &Value) {
        if let Some(drafts) = root["drafts"]["drafts"].as_array_mut() {
            for draft in drafts.iter_mut() {
                let current = draft["content"]["value"].as_str().map(str::to_owned);
                draft["trials"] = json!(self.trial_rows(&draft["reference"]["draft"], current.as_deref(), view));
            }
        }
        root["pendingTrials"] = json!(self.trial_desk.pending.values().map(|p| self.pending_view(p)).collect::<Vec<_>>());
        root["pendingBringBacks"] = json!(self.trial_desk.bring_backs.iter().map(|(id, b)| json!({"id":id,"trial":b.trial,"run":b.run,
            "target":{"generation":b.target.0,"threadId":b.target.1},"prompt":b.prompt,"transcript":b.transcript,"card":b.card,
            "textIdentity":crate::role_supply::content(b.transcript.as_bytes()),"bytes":b.transcript.len(),"shortenings":b.shortenings,"includeNative":b.include_native,
            "standing":"pre-filled, not sent: the transcript is read from Codex's history; once you send it, it is your message, not supply, a run text or evidence of a run"})).collect::<Vec<_>>());
        let links = self.trials.all_links();
        let mut conversations = vec![];
        let mut started_here: BTreeMap<String, Vec<Value>> = BTreeMap::new();
        let mut turns = vec![];
        let mut children = vec![];
        let run_names: BTreeMap<String, String> = self
            .runs
            .values()
            .filter_map(|r| r.try_lock().ok().filter(|r| r.lifecycle == RunLifecycle::Open).map(|r| (r.prepared().scope().conversation.clone(), r.prepared().workflow().name.clone())))
            .collect();
        for link in &links {
            let trial = &link["trial"];
            let (Some(reference), Some(n)) = (trial["reference"].as_str(), trial["sequence"].as_u64()) else { continue };
            let name = link["draft"]["name"].as_str().unwrap_or_default();
            let rev = rev12(link["content"]["value"].as_str().unwrap_or_default()).to_owned();
            let authoring = trial["authoring_conversation"].as_str().unwrap_or_default();
            started_here.entry(authoring.to_owned()).or_default().push(json!({"reference":reference,"sequence":n,"draftName":name,"kind":trial["kind"]}));
            if let Some(clean) = trial["clean_conversation"].as_str() {
                conversations.push(json!({"threadId":clean,"reference":reference,"sequence":n,"draftName":name,"rev12":rev,"fork":false,
                    "header":format!("Trial {n} of draft {name} at content {rev} — not registered; not a workflow run · authoring conversation {authoring}")}));
            }
            if trial["kind"] == "delegated" {
                if let Some(turn) = trial["turn"].as_str() {
                    let label = match run_names.get(authoring) {
                        Some(workflow) => format!("trial {n} of draft {name}; not a step of {workflow}'s run"),
                        None => format!("trial {n} of draft {name}; not a workflow run"),
                    };
                    turns.push(json!({"threadId":authoring,"turnId":turn,"reference":reference,"label":label}));
                }
                if let Some(child) = self.linked_child(reference) {
                    children.push(json!({"threadId":child,"reference":reference,"label":format!("trial {n} of draft {name}; not a workflow run")}));
                }
            }
        }
        for (reference, p) in &self.trial_desk.pending {
            if let Some((_, thread)) = &p.clean {
                let n = p.prepared.text.sequence();
                let rev = rev12(p.prepared.text.content());
                let authoring = p.authoring.as_ref().map(|(_, t)| t.as_str()).unwrap_or("none chosen");
                conversations.push(json!({"threadId":thread,"reference":reference,"sequence":n,"draftName":p.draft,"rev12":rev,"fork":false,
                    "header":format!("Trial {n} of draft {} at content {rev} — not registered; not a workflow run · authoring conversation {authoring}",p.draft)}));
            }
        }
        // Marked conversations not covered above: forks, and clean trial
        // conversations whose message was not acknowledged (outcome unknown or
        // card removed). They keep their trial standing (TT-2).
        for mark in self.trial_desk.marks.all() {
            let thread = mark["thread"].as_str().unwrap_or_default();
            if conversations.iter().any(|c| c["threadId"] == thread) {
                continue;
            }
            let n = mark["sequence"].clone();
            let header = if mark["fork_of"].is_null() {
                format!("Trial {n} of draft {} — the trial message was not acknowledged here (outcome unknown, or not sent); not registered; not a workflow run; it offers no workflow run", mark["draft"].as_str().unwrap_or_default())
            } else {
                format!("fork of trial {n}; it offers no workflow run")
            };
            conversations.push(json!({"threadId":thread,"reference":mark["trial"],"sequence":n,"draftName":mark["draft"],"fork":!mark["fork_of"].is_null(),"header":header}));
        }
        root["trialConversations"] = json!(conversations);
        // TT-10: a real run is brought back by default to the authoring
        // conversation of the latest trial of a draft of that run's slot.
        root["runBringBackDefaults"] = json!(self.runs.iter().filter_map(|(run_ref, run)| {
            let run = run.try_lock().ok()?;
            let w = run.prepared().workflow();
            let latest = links.iter().rev().find(|l| l["draft"]["name"] == w.name.as_str()
                && self.libraries.values().any(|lib| lib.origin == w.origin && lib.owner.try_lock().is_ok_and(|o| o.draft_key(&w.name) == l["draft"])))?;
            Some(json!({"run":run_ref,"threadId":latest["trial"]["authoring_conversation"]}))
        }).collect::<Vec<_>>());
        root["trialsStartedHere"] = json!(started_here.into_iter().map(|(t, trials)| json!({"threadId":t,"trials":trials})).collect::<Vec<_>>());
        root["trialTurns"] = json!(turns);
        root["trialChildren"] = json!(children);
        if let Some(reviews) = root["reviews"].as_array_mut() {
            for row in reviews.iter_mut() {
                let Some(review) = row["reference"].as_str().and_then(|r| self.reviews.get(r)) else { continue };
                row["lastCleanTrial"] = review.try_lock().ok().and_then(|r| {
                    let session = r.review.as_ref()?;
                    let name = session.draft_name()?.to_owned();
                    let content = session.reviewed_draft_content()?.to_owned();
                    let key = r.library.owner.try_lock().ok()?.draft_key(&name);
                    Some(self.last_clean_trial(&key, &name, &content))
                }).unwrap_or(Value::Null);
            }
        }
    }
    /// TT-13: the review's information line. It gates nothing.
    pub(crate) fn last_clean_trial(&self, key: &Value, name: &str, reviewed: &str) -> Value {
        let latest = self.trials.for_draft(key).into_iter().filter(|l| l["trial"]["kind"] == "clean").next_back();
        match latest {
            None => json!({"state":"none","draftName":name,"reading":"Last clean trial: none. A clean trial is optional; registration does not need one"}),
            Some(link) => {
                let content = link["content"]["value"].as_str().unwrap_or_default();
                let (state, words) = if content == reviewed { ("matches", "matches the version under review") } else { ("differs", "differs from the version under review") };
                json!({"state":state,"draftName":name,"content":link["content"],"reference":link["trial"]["reference"],
                    "reading":format!("Last clean trial: content {} — {words}. Information only; registration does not depend on it",rev12(content))})
            }
        }
    }

    /// TT-9's automatic reads due now for `home_key` (no polling: each child is
    /// read once, when first seen; a clean trial's first turn once, when its
    /// user message or the turn completed). Reads nothing itself.
    pub(crate) fn trial_reads_due(&mut self, home_key: &str, view: &Value) -> Vec<TrialRead> {
        let mut due = vec![];
        for sent in self.trial_desk.sent.values_mut() {
            if sent.home != home_key {
                continue;
            }
            match sent.kind {
                TrialKind::Delegated => {
                    for child in descendants_of(view, &sent.authoring) {
                        if sent.baseline.contains(&child) || due.len() >= READS_PER_TICK {
                            continue;
                        }
                        let signature = node_signature(view, &child);
                        match sent.read.get(&child) {
                            None if child_started(view, &child) => {}
                            // A first turn not yet in Codex's history is read again
                            // once the view shows new activity of the child.
                            Some(Err((cause, seen))) if (cause == NOT_YET_TURN || cause == NOT_YET_MESSAGE) && *seen != signature => {}
                            _ => continue,
                        }
                        // Marked before the read runs: one automatic read per observed state.
                        sent.read.insert(child.clone(), Err((IN_PROGRESS.into(), signature)));
                        due.push(TrialRead::Child { reference: sent.reference.clone(), generation: sent.generation.clone(), child });
                    }
                }
                TrialKind::Clean => {
                    let (Some(thread), Some(turn)) = (&sent.clean, &sent.turn) else { continue };
                    if sent.fidelity_read || due.len() >= READS_PER_TICK || !first_message_settled(view, thread, turn) {
                        continue;
                    }
                    sent.fidelity_read = true;
                    due.push(TrialRead::CleanFirstTurn { reference: sent.reference.clone(), generation: sent.generation.clone(), thread: thread.clone(), turn: turn.clone(), client: sent.client.clone() });
                }
            }
        }
        due
    }
    /// Records what TT-9's reads found: a child whose first input carries the
    /// trial's begin marker is linked (the first one) or listed "also given
    /// this trial's workflow"; the linked child's and a clean trial's first
    /// input get a fidelity observation. A failed child read leaves the child
    /// listed "input not read" (Link as trial ‹n› is offered).
    pub(crate) fn apply_trial_reads(&mut self, results: Vec<TrialReadResult>) -> Vec<Value> {
        let mut recorded = vec![];
        for result in results {
            match result.read {
                TrialRead::Child { reference, child, .. } => {
                    let Some(text) = self.trial_desk.sent.get(&reference).map(|s| s.text.clone()) else { continue };
                    match result.texts {
                        Err(cause) => {
                            if let Some(s) = self.trial_desk.sent.get_mut(&reference) {
                                let seen = match s.read.get(&child) {
                                    Some(Err((_, seen))) => seen.clone(),
                                    _ => String::new(),
                                };
                                s.read.insert(child, Err((cause, seen)));
                            }
                        }
                        Ok(texts) => {
                            let marker = text.begin_marker();
                            let given = texts.iter().any(|t| t.contains(&marker));
                            if let Some(s) = self.trial_desk.sent.get_mut(&reference) {
                                s.read.insert(child.clone(), Ok(given));
                            }
                            if !given {
                                continue;
                            }
                            if self.linked_child(&reference).is_some() {
                                if let Some(s) = self.trial_desk.sent.get_mut(&reference) {
                                    s.also_given.insert(child);
                                }
                                continue;
                            }
                            let refs: Vec<&str> = texts.iter().map(String::as_str).collect();
                            let reading = text.fidelity(&refs);
                            for observation in [
                                TrialObservation::SubAgentLinked { child_thread: child.clone(), by_person: false },
                                TrialObservation::Fidelity { read_thread: Some(child.clone()), reading, limits: vec!["first user message read on the child (thread/turns/list, thread/items/list); text the authoring agent added around the trial text is not judged".into()] },
                            ] {
                                recorded.push(self.trials.record_observation(&reference, observation).unwrap_or_else(|e| json!({"trial":reference,"limit":e})));
                            }
                        }
                    }
                }
                TrialRead::CleanFirstTurn { reference, thread, .. } => {
                    let Some(text) = self.trial_desk.sent.get(&reference).map(|s| s.text.clone()) else { continue };
                    let reading = match &result.texts {
                        Ok(texts) => text.fidelity(&texts.iter().map(String::as_str).collect::<Vec<_>>()),
                        Err(cause) => FidelityReading::NotChecked { limits: vec![format!("the first turn could not be read: {cause}; read again later")] },
                    };
                    let observation = TrialObservation::Fidelity { read_thread: Some(thread), reading, limits: vec!["first user message of the clean trial's first turn, located by its client message identity (SC-3)".into()] };
                    recorded.push(self.trials.record_observation(&reference, observation).unwrap_or_else(|e| json!({"trial":reference,"limit":e})));
                }
            }
        }
        recorded
    }

    /// TT-9 by the person: Link as trial ‹n› / unlink. A display relation, not an act.
    pub fn link_trial_child(&mut self, reference: &str, child: &str, link: bool, view: &Value) -> Result<Value, String> {
        let record = self.trials.link(reference).cloned().ok_or_else(|| format!("No trial link {reference}"))?;
        if record["trial"]["kind"] != "delegated" {
            return Err("Only a delegated trial links a sub-agent".into());
        }
        if child.is_empty() || record["trial"]["authoring_conversation"] == child {
            return Err("Choose a sub-agent of the authoring conversation".into());
        }
        let authoring = record["trial"]["authoring_conversation"].as_str().unwrap_or_default();
        if link && !descendants_of(view, authoring).iter().any(|c| c == child) {
            return Err(format!("{child} is not a sub-agent of the authoring conversation {authoring} in what this App observes; nothing linked"));
        }
        let observation = if link {
            if self.linked_child(reference).as_deref() == Some(child) {
                return Err("That sub-agent is already linked to this trial".into());
            }
            TrialObservation::SubAgentLinked { child_thread: child.to_owned(), by_person: true }
        } else {
            if self.linked_child(reference).as_deref() != Some(child) {
                return Err("That sub-agent is not linked to this trial".into());
            }
            TrialObservation::SubAgentUnlinked { child_thread: child.to_owned() }
        };
        self.trials.record_observation(reference, observation)
    }
}

/// Codex's response to one workspace read (TT-9, TT-10), or why it failed.
fn read_page(home: &HomeSession, generation: &Value, method: &str, params: Value, by: &Value) -> Result<Value, String> {
    let home_key = generation["home"].as_str().ok_or("generation home required")?;
    let query = crate::native_history::workspace_read(home_key, generation, method, params)?;
    let dispatch = home.host.history_dispatch_by(&query, by.clone())?;
    let evidence = home.host.history_wait(&dispatch, READ_WAIT)?;
    let response = &evidence["response"];
    if let Some(error) = response.get("error") {
        return Err(format!("{method} answered with an error: {error}"));
    }
    response
        .get("result")
        .filter(|r| r.is_object())
        .cloned()
        .ok_or_else(|| format!("{method} returned no result (outcome {})", evidence["outcome"]))
}
/// All turns of `thread`, oldest first, and why the list is incomplete if it is.
pub(crate) fn read_turns(home: &HomeSession, generation: &Value, thread: &str, by: &Value) -> (Vec<Value>, Option<String>) {
    let mut turns = vec![];
    let mut cursor: Option<String> = None;
    let mut seen = BTreeSet::new();
    for _ in 0..MAX_PAGES {
        let mut params = json!({"threadId":thread,"sortDirection":"asc","itemsView":"summary"});
        if let Some(c) = &cursor {
            params["cursor"] = json!(c);
        }
        let page = match read_page(home, generation, "thread/turns/list", params, by) {
            Ok(page) => page,
            Err(cause) => return (turns, Some(cause)),
        };
        turns.extend(page["data"].as_array().cloned().unwrap_or_default());
        match page["nextCursor"].as_str() {
            Some(next) if !next.is_empty() && seen.insert(next.to_owned()) => cursor = Some(next.to_owned()),
            Some(_) => return (turns, Some("the turn list repeated a page cursor".into())),
            None => return (turns, None),
        }
    }
    (turns, Some(format!("more than {MAX_PAGES} pages of turns")))
}
/// The items of one turn, in order, every page.
pub(crate) fn read_items(home: &HomeSession, generation: &Value, thread: &str, turn: &str, by: &Value) -> Result<Vec<Value>, String> {
    let mut items = vec![];
    let mut cursor: Option<String> = None;
    let mut seen = BTreeSet::new();
    for _ in 0..MAX_PAGES {
        let mut params = json!({"threadId":thread,"turnId":turn,"sortDirection":"asc"});
        if let Some(c) = &cursor {
            params["cursor"] = json!(c);
        }
        let page = read_page(home, generation, "thread/items/list", params, by)?;
        for entry in page["data"].as_array().into_iter().flatten() {
            if entry["turnId"] == turn {
                items.push(entry["item"].clone());
            }
        }
        match page["nextCursor"].as_str() {
            Some(next) if !next.is_empty() && seen.insert(next.to_owned()) => cursor = Some(next.to_owned()),
            Some(_) => return Err("an item page repeated its cursor".into()),
            None => return Ok(items),
        }
    }
    Err(format!("more than {MAX_PAGES} pages of items"))
}
/// The text elements of a turn's first user message (the one carrying
/// `client` when given, else the first), as TT-9 reads them.
fn first_user_texts(items: &[Value], client: Option<&str>) -> Result<Vec<String>, String> {
    let messages: Vec<&Value> = items.iter().filter(|i| i["type"] == "userMessage").collect();
    let chosen = client
        .and_then(|c| messages.iter().find(|m| m["clientId"] == c).copied())
        .or_else(|| messages.first().copied())
        .ok_or(NOT_YET_MESSAGE)?;
    Ok(chosen["content"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|e| e["type"] == "text")
        .filter_map(|e| e["text"].as_str().map(str::to_owned))
        .collect())
}
const NOT_YET_TURN: &str = "the sub-agent has no turn in Codex's history yet";
const NOT_YET_MESSAGE: &str = "the turn holds no user message yet";
/// TT-9's read of a child's (or a clean trial's) first user message.
fn read_first_user_texts(home: &HomeSession, generation: &Value, thread: &str, turn: Option<&str>, client: Option<&str>, by: &Value) -> Result<Vec<String>, String> {
    let turn = match turn {
        Some(turn) => turn.to_owned(),
        None => {
            let mut params = json!({"threadId":thread,"sortDirection":"asc","itemsView":"summary"});
            params["limit"] = json!(1);
            let page = read_page(home, generation, "thread/turns/list", params, by)?;
            page["data"][0]["id"].as_str().map(str::to_owned).ok_or(NOT_YET_TURN)?
        }
    };
    let items = read_items(home, generation, thread, &turn, by)?;
    first_user_texts(&items, client)
}
/// Performs the reads `trial_reads_due` returned. Holds no App lock.
pub(crate) fn perform_trial_reads(home: &HomeSession, reads: Vec<TrialRead>) -> Vec<TrialReadResult> {
    reads
        .into_iter()
        .map(|read| {
            let texts = match &read {
                TrialRead::Child { generation, child, .. } => read_first_user_texts(home, generation, child, None, None, &rule_read()),
                TrialRead::CleanFirstTurn { generation, thread, turn, client, .. } => read_first_user_texts(home, generation, thread, Some(turn), Some(client), &rule_read()),
            };
            TrialReadResult { read, texts }
        })
        .collect()
}

const IN_PROGRESS: &str = "read in progress";
/// The child's descendant node as the view shows it now (its last native call,
/// activity, status and thread read), compared to decide a re-read.
fn node_signature(view: &Value, child: &str) -> String {
    view["descendants"].as_array().into_iter().flatten().find(|d| d["threadId"] == child).map(Value::to_string).unwrap_or_default()
}
/// The view shows the child past its spawn: an item or turn of its own, a
/// status other than `pendingInit`, or a subagent activity row. Its first turn
/// should then be in Codex's history (H-7).
fn child_started(view: &Value, child: &str) -> bool {
    let own = view["items"].as_array().into_iter().flatten().any(|r| r["threadId"] == child)
        || view["turns"].as_array().into_iter().flatten().any(|t| t["threadId"] == child);
    let node = view["descendants"].as_array().into_iter().flatten().find(|d| d["threadId"] == child);
    let status = node.and_then(|n| n["lastObservedStatus"]["status"].as_str());
    own || node.is_some_and(|n| !n["lastNativeActivity"].is_null()) || status.is_some_and(|s| s != "pendingInit")
}
/// Descendant threads the native view shows under `parent` (DEL-01-03 §7.2).
fn descendants_of(view: &Value, parent: &str) -> Vec<String> {
    view["descendants"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|d| d["parentThreadId"] == parent)
        .filter_map(|d| d["threadId"].as_str().map(str::to_owned))
        .collect()
}
fn all_descendants(view: &Value) -> BTreeSet<String> {
    view["descendants"].as_array().into_iter().flatten().filter_map(|d| d["threadId"].as_str().map(str::to_owned)).collect()
}
/// A turn of `thread` is live in the native view.
fn thread_live(view: &Value, thread: &str) -> bool {
    view["turns"].as_array().into_iter().flatten().any(|t| t["threadId"] == thread && t["status"] == "inProgress")
}
/// The clean trial's first user message completed, or its turn ended (SC-3).
fn first_message_settled(view: &Value, thread: &str, turn: &str) -> bool {
    let ended = view["turns"].as_array().into_iter().flatten().any(|t| t["threadId"] == thread && t["id"] == turn && t["status"].as_str().is_some_and(|s| s != "inProgress"));
    let message = view["items"].as_array().into_iter().flatten().any(|row| {
        row["threadId"] == thread && row["turnId"] == turn && row["native"]["type"] == "userMessage" && row["displayState"] == "completed"
    });
    ended || message
}
/// TT-12 (a): file-change items of `thread` naming a path outside `work`.
fn files_outside(view: &Value, thread: &str, work: &str) -> usize {
    view["items"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|row| row["threadId"] == thread && row["native"]["type"] == "fileChange")
        .flat_map(|row| row["native"]["changes"].as_array().cloned().unwrap_or_default())
        .filter(|change| {
            let path = change["path"].as_str().unwrap_or_default();
            !(path.starts_with(work) || path.contains(&format!("/{work}")))
        })
        .count()
}

/// SQ-DT DT-4 and SQ-FT FT-4: the person pressed Send on a pre-filled trial
/// message in conversation `thread`. The turn's input is the person's text
/// then the trial text (delegated), or the trial text then the person's text
/// (clean), with the pre-filled client message identity. The trial link is
/// written only when Codex acknowledges the `turn/start` (TT-4); a send the
/// Host refused before writing leaves the trial pre-filled; a written send
/// whose outcome is not established leaves no link and is never resent. No
/// App lock is held while Codex answers.
pub(crate) fn send_trial(root: &Mutex<WorkflowRootSession>, home: &HomeSession, reference: &str, generation: &Value, thread: &str, person_text: &str) -> Result<Value, String> {
    let home_key = generation["home"].as_str().ok_or("generation home required")?.to_owned();
    current_conversation(&home.host.snapshot(), generation, thread).map_err(|e| format!("{e}; nothing sent"))?;
    // Runtime before Root (host_status's lock order).
    let baseline = all_descendants(&home.runtime.lock().unwrap().native_view());
    let (elements, client, kind) = {
        let mut root = root.lock().unwrap();
        if root.pending_notice_for(&home_key, thread)?.is_some() {
            return Err("A workflow run ended in this conversation and its end notice goes first with the next message (WR TX-5); send that message first, then send the trial. Nothing sent; the trial stays pre-filled".into());
        }
        let clean_here = root.trial_conversation(thread);
        let p = root.trial_desk.pending.get_mut(reference).ok_or_else(|| format!("No pre-filled trial {reference}; press Try again"))?;
        if p.in_flight {
            return Err("This trial message is being sent now; nothing sent again".into());
        }
        match p.kind {
            TrialKind::Delegated => {
                if clean_here.is_some() {
                    return Err("A delegated trial is sent in an authoring conversation, not in a trial conversation. Nothing sent".into());
                }
                p.authoring = Some((generation.clone(), thread.to_owned()));
            }
            TrialKind::Clean => match &p.clean {
                Some((g, t)) if g == generation && t == thread => {}
                _ => return Err("A clean trial is sent in its own new conversation: start it with Send in the new trial conversation. Nothing sent".into()),
            },
        }
        p.in_flight = true;
        let text = p.prepared.text.text().to_owned();
        let elements: Vec<String> = match p.kind {
            TrialKind::Delegated => [person_text.to_owned(), text].into_iter().filter(|e| !e.is_empty()).collect(),
            TrialKind::Clean => [text, person_text.to_owned()].into_iter().filter(|e| !e.is_empty()).collect(),
        };
        (elements, p.client.clone(), p.kind)
    };
    let refs: Vec<&str> = elements.iter().map(String::as_str).collect();
    let outcome = home.host.turn_start_texts(generation, thread, &refs, &client);
    let mut root = root.lock().unwrap();
    let turn = match outcome {
        Ok(response) => response["result"]["turn"]["id"].as_str().map(str::to_owned),
        Err(reason) if not_written(&reason) || refused(&reason) => {
            if let Some(p) = root.trial_desk.pending.get_mut(reference) {
                p.in_flight = false;
            }
            return Err(format!("{reason}. No trial link was written; the trial stays pre-filled (WR §5.5)"));
        }
        Err(reason) => {
            root.trial_desk.pending.remove(reference);
            return Err(format!("{reason}. The send's outcome is not established: no trial link was written and nothing is resent (WR TT-4); press Try again for a new trial"));
        }
    };
    let p = root.trial_desk.pending.remove(reference).ok_or("pre-filled trial lost while sending")?;
    let (authoring, clean) = match kind {
        TrialKind::Delegated => (thread.to_owned(), None),
        TrialKind::Clean => (p.authoring.as_ref().map(|(_, t)| t.clone()).unwrap_or_else(|| "none chosen".into()), Some(thread.to_owned())),
    };
    let sent = SentTrial { kind, authoring_conversation: authoring.clone(), client_message: client.clone(), turn: turn.clone(), clean_conversation: clean.clone() };
    let link = root.trials.record_sent(&p.prepared, &sent);
    // TT-2: a trial of a draft of the run's own workflow raises no End-run
    // offer for the rest of that run.
    if kind == TrialKind::Delegated {
        if let Ok(Some((run_ref, run))) = root.run_in_force(&home_key, thread) {
            let own = run.try_lock().is_ok_and(|r| {
                let w = r.prepared().workflow();
                root.libraries.get(&p.library).is_some_and(|l| l.origin == w.origin) && w.name == p.draft
            });
            if own {
                root.trial_desk.finished_offer_suppressed.insert(run_ref);
            }
        }
    }
    root.trial_desk.sent.insert(
        reference.to_owned(),
        SentState {
            reference: reference.to_owned(),
            kind,
            text: p.prepared.text.clone(),
            home: home_key,
            generation: generation.clone(),
            authoring,
            turn: turn.clone(),
            clean,
            client,
            baseline,
            read: BTreeMap::new(),
            also_given: BTreeSet::new(),
            fidelity_read: false,
        },
    );
    match link {
        Ok(link) => Ok(json!({"reference":reference,"turn":turn,"link":link,"standing":"trial message sent by the person; trial link written on Codex's acknowledgment. Not a run, registration, checking or acceptance"})),
        Err(cause) => Err(format!("The trial message was sent (turn {}) but its trial link could not be written: {cause}. Nothing is resent", turn.unwrap_or_else(|| "not named".into()))),
    }
}

/// `workflow_trial_read`: the person opened the trial and asked to read again
/// (TT-9: a failed read is repeated only when the person opens the trial or the
/// child; after a relaunch this is how a trial is read). A delegated trial:
/// the linked sub-agent's first input, or each candidate whose input was not
/// read; a clean trial: its first turn. Each read is a new observation.
pub(crate) fn read_trial_again(root: &Mutex<WorkflowRootSession>, home: &HomeSession, reference: &str, view: &Value) -> Result<Value, String> {
    let (link, text, linked, candidates) = {
        let root = root.lock().unwrap();
        let link = root.trials.link(reference).cloned().ok_or_else(|| format!("No trial link {reference}"))?;
        let text = root.trial_text(reference);
        let linked = root.linked_child(reference);
        let mut candidates: BTreeSet<String> = root.trial_desk.sent.get(reference).map(|s| s.read.iter().filter(|(_, r)| r.is_err()).map(|(c, _)| c.clone()).collect()).unwrap_or_default();
        if linked.is_none() {
            if let Some(authoring) = link["trial"]["authoring_conversation"].as_str() {
                candidates.extend(descendants_of(view, authoring));
            }
        }
        (link, text, linked, candidates)
    };
    let generation = home.host.snapshot()["generation"].clone();
    let trial = &link["trial"];
    let mut results = vec![];
    if trial["kind"] == "clean" {
        let thread = trial["clean_conversation"].as_str().unwrap_or_default().to_owned();
        let turn = trial["turn"].as_str().map(str::to_owned);
        let reading = match (&text, turn.as_deref()) {
            (Err(cause), _) => FidelityReading::NotChecked { limits: vec![cause.clone()] },
            (_, None) => FidelityReading::NotChecked { limits: vec!["Codex's acknowledgment named no turn".into()] },
            (Ok(text), Some(turn)) => match read_first_user_texts(home, &generation, &thread, Some(turn), trial["client_message"].as_str(), &person_read()) {
                Ok(texts) => text.fidelity(&texts.iter().map(String::as_str).collect::<Vec<_>>()),
                Err(cause) => FidelityReading::NotChecked { limits: vec![format!("the first turn could not be read: {cause}")] },
            },
        };
        let observation = TrialObservation::Fidelity { read_thread: Some(thread), reading, limits: vec!["read again at the person's request".into()] };
        results.push(root.lock().unwrap().trials.record_observation(reference, observation)?);
        return Ok(json!({"reference":reference,"recorded":results}));
    }
    let text = text?;
    if let Some(child) = linked {
        let reading = match read_first_user_texts(home, &generation, &child, None, None, &person_read()) {
            Ok(texts) => text.fidelity(&texts.iter().map(String::as_str).collect::<Vec<_>>()),
            Err(cause) => FidelityReading::NotChecked { limits: vec![format!("the sub-agent's first turn could not be read: {cause}")] },
        };
        let observation = TrialObservation::Fidelity { read_thread: Some(child), reading, limits: vec!["read again at the person's request".into()] };
        results.push(root.lock().unwrap().trials.record_observation(reference, observation)?);
        return Ok(json!({"reference":reference,"recorded":results}));
    }
    let marker = text.begin_marker();
    let mut unread = vec![];
    for child in candidates {
        match read_first_user_texts(home, &generation, &child, None, None, &person_read()) {
            Ok(texts) if texts.iter().any(|t| t.contains(&marker)) => {
                let mut root = root.lock().unwrap();
                if root.linked_child(reference).is_some() {
                    if let Some(s) = root.trial_desk.sent.get_mut(reference) {
                        s.also_given.insert(child);
                    }
                    continue;
                }
                let reading = text.fidelity(&texts.iter().map(String::as_str).collect::<Vec<_>>());
                results.push(root.trials.record_observation(reference, TrialObservation::SubAgentLinked { child_thread: child.clone(), by_person: false })?);
                results.push(root.trials.record_observation(reference, TrialObservation::Fidelity { read_thread: Some(child), reading, limits: vec!["read at the person's request".into()] })?);
            }
            Ok(_) => {}
            Err(cause) => unread.push(json!({"thread":child,"limit":cause})),
        }
    }
    Ok(json!({"reference":reference,"recorded":results,"inputNotRead":unread}))
}

/// The source a bring-back or Compare reads: conversation and its turn range.
struct HistorySource {
    thread: String,
    /// First turn to include (a run's start turn), or all.
    from_turn: Option<String>,
    /// A run reference whose end notice or chain line ends the range.
    run_end: Option<String>,
    label: TranscriptSource,
    trial_line: Option<TrialTextLine>,
}
fn read_source(home: &HomeSession, generation: &Value, source: &HistorySource) -> (Vec<TurnRead>, Option<String>) {
    let (turns, mut limit) = read_turns(home, generation, &source.thread, &person_read());
    let mut reads = vec![];
    let mut started = source.from_turn.is_none();
    for turn in turns {
        let id = turn["id"].as_str().unwrap_or_default().to_owned();
        if !started {
            if Some(&id) != source.from_turn.as_ref() {
                continue;
            }
            started = true;
        }
        let items = read_items(home, generation, &source.thread, &id, &person_read());
        if let (Some(run), Ok(items)) = (&source.run_end, &items) {
            let ends = items.iter().filter(|i| i["type"] == "userMessage").flat_map(|i| i["content"].as_array().cloned().unwrap_or_default()).any(|e| {
                e["text"].as_str().is_some_and(|t| (t.starts_with("[Chirality] Workflow run ended:") || t.starts_with("[Chirality] Previous workflow run ended:")) && t.contains(&format!("(run {run}")))
            });
            if ends && !reads.is_empty() {
                break;
            }
        }
        reads.push(TurnRead { turn, items });
    }
    if !started {
        limit = Some(limit.unwrap_or_else(|| "the run's start turn was not found in Codex's history".into()));
    }
    (reads, limit)
}
impl WorkflowRootSession {
    fn trial_source(&self, reference: &str) -> Result<HistorySource, String> {
        let link = self.trials.link(reference).cloned().ok_or_else(|| format!("No trial link {reference}"))?;
        let trial = &link["trial"];
        let clean = trial["kind"] == "clean";
        let thread = if clean {
            trial["clean_conversation"].as_str().map(str::to_owned).ok_or("the clean trial names no conversation")?
        } else {
            self.linked_child(reference).ok_or_else(|| format!("No sub-agent is linked to trial {}; link one first", trial["sequence"]))?
        };
        let line = self.trial_text(reference).ok().map(|text| {
            let fidelity = self.trials.observations(reference).into_iter().rev().find(|o| o["observation"] == "fidelity").map(|o| o["fidelity"]["state"].as_str().unwrap_or("not checked").to_owned()).unwrap_or_else(|| "not checked".into());
            TrialTextLine { run_text: text.run_text().to_owned(), line: format!("[trial text of trial {}: identity {}, {} bytes; fidelity {fidelity}]", trial["sequence"], rev12(text.identity()["value"].as_str().unwrap_or_default()), text.bytes()) }
        });
        Ok(HistorySource {
            thread: thread.clone(),
            from_turn: None,
            run_end: None,
            label: TranscriptSource::Trial {
                sequence: trial["sequence"].as_u64().unwrap_or(0),
                draft_name: link["draft"]["name"].as_str().unwrap_or_default().to_owned(),
                rev12: rev12(link["content"]["value"].as_str().unwrap_or_default()).to_owned(),
                clean,
                thread,
            },
            trial_line: line,
        })
    }
    fn run_source(&self, run_ref: &str) -> Result<(HistorySource, std::collections::BTreeMap<String, Vec<u8>>, String), String> {
        let run = self.runs.get(run_ref).ok_or_else(|| format!("No run {run_ref} held in this App process; runs recorded by earlier App sessions cannot be brought back here"))?;
        let run = run.try_lock().map_err(|_| "That run has an operation pending; try again")?;
        let scope = run.prepared().scope().clone();
        let workflow = run.prepared().workflow().clone();
        let start = run.turn_id.clone().ok_or("The run's start turn was not acknowledged; nothing to bring back")?;
        let files = run.selection.snapshot().files().clone();
        Ok((
            HistorySource {
                thread: scope.conversation.clone(),
                from_turn: Some(start),
                run_end: Some(scope.run.clone()),
                label: TranscriptSource::Run { run: scope.run.clone(), origin: workflow.origin.clone(), name: workflow.name.clone(), rev12: rev12(&workflow.revision).to_owned(), thread: scope.conversation.clone() },
                trial_line: None,
            },
            files,
            format!("{}:{}", workflow.origin, workflow.name),
        ))
    }
}

/// SQ-BB BB-1…BB-4: read the trial's conversation (clean) or linked
/// sub-agent (delegated), or a real run's turns from its start turn to its end
/// mark, through Codex's history, and pre-fill the transcript in `thread`'s
/// composer, unsent. Waits (refuses) while a turn is live in the source.
pub(crate) fn bring_back(root: &Mutex<WorkflowRootSession>, home: &HomeSession, trial: Option<&str>, run: Option<&str>, generation: &Value, thread: &str, include_native: bool) -> Result<Value, String> {
    current_conversation(&home.host.snapshot(), generation, thread).map_err(|e| format!("{e}; nothing pre-filled"))?;
    let view = home.runtime.lock().unwrap().native_view();
    let source = {
        let root = root.lock().unwrap();
        match (trial, run) {
            (Some(reference), None) => root.trial_source(reference)?,
            (None, Some(run_ref)) => root.run_source(run_ref)?.0,
            _ => return Err("Bring back takes one trial or one run".into()),
        }
    };
    if thread_live(&view, &source.thread) {
        return Err("A turn is live in that conversation; Bring back waits until none is live".into());
    }
    let read_at = crate::util::now_rfc3339();
    let (turns, turns_limit) = read_source(home, generation, &source);
    let composed = transcript::compose_transcript(&TranscriptInput {
        source: source.label.clone(),
        read_at,
        turns: &turns,
        turns_limit,
        trial_text: source.trial_line.clone(),
        include_native,
        bound: transcript::TRANSCRIPT_BOUND,
    });
    let (card, prompt) = match &source.label {
        TranscriptSource::Trial { sequence, draft_name, rev12, .. } => (
            format!("transcript of trial {sequence} of draft {draft_name} @ {rev12}, read from Codex history"),
            format!("Here is how trial {sequence} went. Please assess it against the draft: where the agent followed the workflow, where it departed or got stuck, and what you would change."),
        ),
        TranscriptSource::Run { run, origin, name, .. } => (
            format!("transcript of run {run} of {origin}:{name}, read from Codex history"),
            format!("Here is how a real run of {origin}:{name} went. Please assess it against the workflow: where the agent followed it, where it departed or got stuck, and what you would change in a new revision."),
        ),
    };
    let id = crate::util::opaque_id("bring-back:")?;
    let pending = PendingBringBack {
        trial: trial.map(str::to_owned),
        run: run.map(str::to_owned),
        target: (generation.clone(), thread.to_owned()),
        prompt,
        transcript: composed.text,
        card,
        shortenings: composed.shortenings,
        include_native,
        client: crate::util::opaque_id("bring-back-message:")?,
        in_flight: false,
    };
    let view = json!({"id":id,"card":pending.card,"bytes":pending.transcript.len(),"shortenings":pending.shortenings,"state":"pre-filled; not sent"});
    root.lock().unwrap().trial_desk.bring_backs.insert(id, pending);
    Ok(view)
}
pub(crate) fn cancel_bring_back(root: &Mutex<WorkflowRootSession>, id: &str) -> Result<Value, String> {
    let mut root = root.lock().unwrap();
    match root.trial_desk.bring_backs.get(id) {
        Some(b) if b.in_flight => Err("This transcript is being sent now; it can no longer be removed".into()),
        Some(_) => {
            root.trial_desk.bring_backs.remove(id);
            Ok(json!({"id":id,"state":"removed; nothing recorded"}))
        }
        None => Err(format!("No pre-filled transcript {id}")),
    }
}
/// SQ-BB BB-5: the person sends the prompt and the transcript; a trial's
/// *brought back* observation is written on Codex's acknowledgment. A real
/// run brought back has no trial link, so nothing is recorded for it.
pub(crate) fn send_bring_back(root: &Mutex<WorkflowRootSession>, home: &HomeSession, id: &str, generation: &Value, thread: &str, person_text: &str) -> Result<Value, String> {
    current_conversation(&home.host.snapshot(), generation, thread).map_err(|e| format!("{e}; nothing sent"))?;
    let home_key = generation["home"].as_str().ok_or("generation home required")?.to_owned();
    let (elements, client) = {
        let mut root = root.lock().unwrap();
        if root.pending_notice_for(&home_key, thread)?.is_some() {
            return Err("A workflow run ended in this conversation and its end notice goes first with the next message (WR TX-5); send that message first. Nothing sent; the transcript stays pre-filled".into());
        }
        let b = root.trial_desk.bring_backs.get_mut(id).ok_or_else(|| format!("No pre-filled transcript {id}"))?;
        if b.in_flight {
            return Err("This transcript is being sent now; nothing sent again".into());
        }
        b.in_flight = true;
        b.target = (generation.clone(), thread.to_owned());
        ([person_text.to_owned(), b.transcript.clone()].into_iter().filter(|e| !e.is_empty()).collect::<Vec<_>>(), b.client.clone())
    };
    let refs: Vec<&str> = elements.iter().map(String::as_str).collect();
    let outcome = home.host.turn_start_texts(generation, thread, &refs, &client);
    let mut root = root.lock().unwrap();
    match outcome {
        Ok(response) => {
            let b = root.trial_desk.bring_backs.remove(id).ok_or("pre-filled transcript lost while sending")?;
            let turn = response["result"]["turn"]["id"].clone();
            let recorded = match &b.trial {
                Some(reference) => Some(root.trials.record_observation(reference, TrialObservation::BroughtBack { target_conversation: thread.to_owned(), transcript: b.transcript.clone(), shortenings: b.shortenings.clone() })),
                None => None,
            };
            match recorded {
                Some(Err(cause)) => Err(format!("The transcript was sent (turn {turn}) but its brought-back observation could not be written: {cause}. Nothing is resent")),
                Some(Ok(observation)) => Ok(json!({"id":id,"turn":turn,"observation":observation})),
                None => Ok(json!({"id":id,"turn":turn,"observation":null,"limit":"a real run brought back has no trial link; nothing is recorded for it"})),
            }
        }
        Err(reason) if not_written(&reason) || refused(&reason) => {
            if let Some(b) = root.trial_desk.bring_backs.get_mut(id) {
                b.in_flight = false;
            }
            Err(format!("{reason}. Nothing recorded; the transcript stays pre-filled"))
        }
        Err(reason) => {
            root.trial_desk.bring_backs.remove(id);
            Err(format!("{reason}. The send's outcome is not established; nothing is recorded or resent"))
        }
    }
}

/// TT-11 Compare: two trials, or a trial and a real run of a revision of the
/// same slot, side by side with the difference between their versions (read
/// from the trial snapshots and the revision store). Scores and judges nothing;
/// records nothing.
pub(crate) fn compare(root: &Mutex<WorkflowRootSession>, resolve: &dyn Fn(&str) -> Option<std::sync::Arc<HomeSession>>, left: &Value, right: &Value) -> Result<Value, String> {
    struct Side {
        /// The conversation whose Codex home this side is read from (H-5).
        home_thread: Option<String>,
        label: String,
        kind: String,
        version: Value,
        conversation: Value,
        snapshot: Value,
        files: Option<std::collections::BTreeMap<String, Vec<u8>>>,
        slot: String,
        source: Result<HistorySource, String>,
    }
    let side = |root: &WorkflowRootSession, spec: &Value| -> Result<Side, String> {
        if let Some(reference) = spec["trial"].as_str() {
            let (link, library) = root.link_and_library(reference)?;
            let name = link["draft"]["name"].as_str().unwrap_or_default().to_owned();
            let content = link["content"]["value"].as_str().unwrap_or_default().to_owned();
            let folder = package_copy::content_folder(&library.root, TRIAL_AREA, &name, &content);
            let (snapshot, files) = match package_copy::copy_standing(&folder, &content) {
                CopyStanding::Current => (json!({"state":"current"}), Snapshot::capture(&folder).ok().map(|s| s.files().clone())),
                CopyStanding::Changed(cause) => (json!({"state":"changed","reading":format!("trial snapshot changed after the trial: {cause}")}), None),
                CopyStanding::NotAvailable(_) => (json!({"state":"not available","reading":"version bytes not available"}), None),
            };
            let trial = &link["trial"];
            return Ok(Side {
                home_thread: root.trial_home_thread(reference),
                label: format!("trial {} of draft {name}", trial["sequence"]),
                kind: trial["kind"].as_str().unwrap_or_default().into(),
                version: link["content"].clone(),
                conversation: json!({"authoring":trial["authoring_conversation"],"trial":trial["clean_conversation"],"subAgent":root.linked_child(reference)}),
                snapshot,
                files,
                slot: format!("{}:{name}", library.origin),
                source: root.trial_source(reference),
            });
        }
        if let Some(run_ref) = spec["run"].as_str() {
            let (source, files, slot) = root.run_source(run_ref)?;
            let run = root.runs.get(run_ref).and_then(|r| r.try_lock().ok().map(|r| json!({"method":r.prepared().workflow().revision_method,"value":r.prepared().workflow().revision}))).unwrap_or(Value::Null);
            return Ok(Side { home_thread: Some(source.thread.clone()), label: format!("run {run_ref} of {slot}"), kind: "registered run".into(), version: run, conversation: json!({"run":source.thread}), snapshot: json!({"state":"revision store","reading":"read from the revision this run selected"}), files: Some(files), slot, source: Ok(source) });
        }
        Err("Each side of Compare is a trial or a run".into())
    };
    let (a, b) = {
        let root = root.lock().unwrap();
        (side(&root, left)?, side(&root, right)?)
    };
    let runs = [&a, &b].iter().filter(|s| s.kind == "registered run").count();
    if runs == 2 {
        return Err("Compare takes two trials, or a trial and a real run".into());
    }
    if runs == 1 && a.slot != b.slot {
        return Err(format!("Compare takes a trial and a real run of a revision of the same slot ({} and {} differ)", a.slot, b.slot));
    }
    let summarize = |s: &Side| -> Value {
        let home = s.home_thread.as_deref().and_then(resolve);
        let source = match (&s.source, home) {
            (Ok(source), Some(home)) => Ok((source, home)),
            (Ok(_), None) => Err("this side's conversation is not loaded in a Codex home now; its activity was not read".to_owned()),
            (Err(cause), _) => Err(cause.clone()),
        };
        match source {
            Ok((source, home)) => {
                let generation = home.host.snapshot()["generation"].clone();
                let (turns, limit) = read_source(&home, &generation, source);
                transcript::activity_summary(&turns, limit.as_deref())
            }
            Err(cause) => json!({"turns":0,"endings":[],"commands":{"run":0,"failed":0,"list":[]},"fileChanges":[],"finalAgentMessage":null,"limits":[cause]}),
        }
    };
    // The one shape the web view renders, pinned by tests/fixtures/trial-compare.json.
    let view = |s: &Side| transcript::CompareSide {
        label: s.label.clone(),
        kind: s.kind.clone(),
        version: s.version.clone(),
        conversation: s.conversation.clone(),
        snapshot: s.snapshot.clone(),
        summary: summarize(s),
    };
    let difference = match (&a.files, &b.files) {
        (Some(x), Some(y)) => transcript::version_difference(x, y),
        _ => json!({"limit":"version bytes not available for one side; no difference shown"}),
    };
    Ok(transcript::compare_result(&view(&a), &view(&b), difference))
}

