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
use crate::workflow_workspace::registration::drafts::trials::{PreparedTrial, SentTrial, TrialKind, TrialLinkMethod, TrialObservation};
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

/// NPTD §7.1 (R21-1's order) for the authoring conversation, from the signals
/// the host read for it (`delegation_availability::signals`): *missing*
/// refuses Try with the authoring agent with the first reason; *not
/// established* offers it with that note.
pub(crate) fn delegation_availability(signals: Option<&Value>) -> Value {
    crate::delegation_availability::evaluate(signals)
}
/// The signals for a delegated trial's authoring conversation, read now from
/// its Codex home (R19-5: at run time, as the composer is prepared). Nothing is
/// read for a clean trial or without an authoring conversation.
pub(crate) fn delegation_signals_for(kind: &str, home: Option<&HomeSession>, authoring: Option<(&Value, &str)>) -> Option<Value> {
    match (kind, home, authoring) {
        ("delegated", Some(home), Some((generation, thread))) => Some(home.host.delegation_signals_read(generation, thread, person_read())),
        _ => None,
    }
}

/// A trial or bring-back send the host refused or could not complete, with
/// whether the message is still pre-filled (so the view offers to send it
/// again only then).
#[derive(Clone, Debug, serde::Serialize)]
#[serde(rename_all = "camelCase")]
pub struct SendRefusal {
    pub message: String,
    pub prefill_kept: bool,
}
impl SendRefusal {
    /// Refused with the message still pre-filled.
    pub fn kept(message: impl Into<String>) -> Self {
        Self { message: message.into(), prefill_kept: true }
    }
    /// Refused with nothing pre-filled to send again (withdrawn, sent, absent or in flight).
    pub fn not_kept(message: impl Into<String>) -> Self {
        Self { message: message.into(), prefill_kept: false }
    }
}
impl std::ops::Deref for SendRefusal {
    type Target = str;
    fn deref(&self) -> &str {
        &self.message
    }
}
impl std::fmt::Display for SendRefusal {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.message)
    }
}

/// WR TT-9, H-5: the home among `homes` whose current generation holds `thread`.
pub(crate) fn home_holding(homes: &[std::sync::Arc<HomeSession>], thread: &str) -> Option<std::sync::Arc<HomeSession>> {
    let mut matches = homes
        .iter()
        .filter(|home| {
            let snapshot = home.host.snapshot();
            current_conversation(&snapshot, &snapshot["generation"], thread).is_ok()
        });
    let first = matches.next()?.clone();
    matches.next().is_none().then_some(first)
}
/// WR TT-9, H-5: the home holding the trial's own conversation (a clean
/// trial's conversation, a delegated trial's authoring conversation), where
/// Read again, Try again and Compare go.
pub(crate) fn trial_home(root: &Mutex<WorkflowRootSession>, homes: &[std::sync::Arc<HomeSession>], reference: &str) -> Result<std::sync::Arc<HomeSession>, String> {
    let thread = root.lock().unwrap().trial_home_thread(reference).ok_or_else(|| format!("No trial link {reference}"))?;
    home_holding(homes, &thread).ok_or_else(|| format!("The trial's conversation {thread} is not loaded in a Codex home now; nothing read or recorded"))
}

/// TT-11 Try again in the host: the delegation signals of a delegated trial's
/// authoring conversation are read first (no App lock held while Codex
/// answers), then the trial is pre-filled.
pub(crate) fn trial_again(root: &Mutex<WorkflowRootSession>, reference: &str, home: &HomeSession, project: Option<&std::path::Path>) -> Result<Value, String> {
    let authoring = root.lock().unwrap().trials.link(reference).and_then(|l| (l["trial"]["kind"] == "delegated").then(|| l["trial"]["authoring_conversation"].as_str().map(str::to_owned)).flatten());
    let generation = home.host.snapshot()["generation"].clone();
    let signals = authoring.as_deref().and_then(|thread| delegation_signals_for("delegated", Some(home), Some((&generation, thread))));
    root.lock().unwrap().trial_again_with(reference, Some(home), project, signals.as_ref())
}

/// SQ-FT FT-3, FT-4 (H-2): the person sends a clean trial. `start` starts the
/// new conversation; every outcome after the press releases or withdraws the
/// pre-fill. A start that failed, or whose thread id was not reported, may
/// still have reached Codex, so the pre-fill is withdrawn (a second press
/// cannot start a second conversation). The trial conversation's generation
/// is the one the start result reports, and `send` sends the trial message there.
pub(crate) fn start_clean_trial(
    root: &Mutex<WorkflowRootSession>,
    reference: &str,
    start: impl FnOnce() -> Result<Value, String>,
    send: impl FnOnce(&Value, &str) -> Result<Value, SendRefusal>,
) -> Result<Value, SendRefusal> {
    {
        let mut root = root.lock().unwrap();
        if let Err(message) = root.begin_clean_start(reference) {
            // Refused before anything started: still pre-filled unless absent
            // or another press is starting it now.
            let prefill_kept = root.trial_desk.pending.get(reference).is_some_and(|p| !p.in_flight);
            return Err(SendRefusal { message, prefill_kept });
        }
    }
    let started = match start() {
        Ok(started) => started,
        Err(error) => {
            root.lock().unwrap().withdraw_clean_start(reference);
            return Err(SendRefusal::not_kept(format!("{error}. The trial conversation was not started (or its start was not acknowledged); the pre-filled trial was withdrawn and nothing was recorded; press Try again")));
        }
    };
    let generation = started["startGeneration"].clone();
    let thread = started["result"]["thread"]["id"].as_str().map(str::to_owned).filter(|_| crate::recovery::generation_ref(&generation).is_ok());
    let Some(thread) = thread else {
        root.lock().unwrap().withdraw_clean_start(reference);
        return Err(SendRefusal::not_kept("The new conversation's identity or generation was not reported; the pre-filled trial was withdrawn and nothing was sent or recorded; press Try again"));
    };
    root.lock().unwrap().mark_clean_started(reference, &generation, &thread);
    match send(&generation, &thread) {
        Ok(mut value) => {
            value["conversation"] = json!({"generation":generation,"threadId":thread});
            value["thread"] = value["conversation"].clone();
            Ok(value)
        }
        Err(error) => Err(SendRefusal {
            message: format!("The trial conversation {thread} started (it stays trial-only), but the trial message was not acknowledged: {error}"),
            prefill_kept: error.prefill_kept,
        }),
    }
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
    source: Value,
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
                return Err(format!("Try with the authoring agent is not available: {}; use Try in a fresh conversation. Nothing pre-filled", reading["reason"].as_str().unwrap_or_default()));
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
    pub fn trial_again_with(&mut self, reference: &str, home: Option<&HomeSession>, project: Option<&std::path::Path>, delegation_signals: Option<&Value>) -> Result<Value, String> {
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
        self.prepare_trial_with(&kind, &name, authoring, home, project, delegation_signals)
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
            let linked = self.linked_child(&reference);
            let source = if row["kind"] == "clean" { row["trialConversation"].as_str().map(str::to_owned) } else { linked.clone() };
            let mut linked_cause: Option<String> = None;
            if let Some(sent) = self.trial_desk.sent.get(&reference) {
                // A child already linked to this trial is never offered as a
                // candidate for it again (Link as trial ‹n›).
                let mut unread = vec![];
                let mut unread_reasons = vec![];
                let mut not_checkable_children = vec![];
                for (child, read) in &sent.read {
                    let Err((cause, _)) = read else { continue };
                    if cause == IN_PROGRESS {
                        continue;
                    }
                    if linked.as_deref() == Some(child.as_str()) {
                        linked_cause = Some(cause.clone());
                    } else if not_checkable(cause) {
                        not_checkable_children.push(json!({"thread":child,"reading":cause,"final":not_checkable_final(cause)}));
                    } else {
                        unread.push(json!(child));
                        unread_reasons.push(json!({"thread":child,"reason":cause}));
                    }
                }
                row["subAgent"]["alsoGiven"] = json!(sent.also_given.iter().filter(|c| linked.as_deref() != Some(c.as_str())).collect::<Vec<_>>());
                row["subAgent"]["unread"] = json!(unread);
                row["subAgent"]["unreadReasons"] = json!(unread_reasons);
                row["subAgent"]["notCheckable"] = json!(not_checkable_children);
            }
            // TT-9: a fidelity that cannot be checked reads so, from the latest
            // recorded reading or the linked child's read, and Read again is
            // not offered as if a later read could tell more.
            if row["kind"] == "delegated" {
                let unchecked = row["fidelity"]["state"] == "not checked";
                let recorded = row["fidelity"]["limits"].as_array().into_iter().flatten().filter_map(Value::as_str).find(|l| not_checkable(l)).map(str::to_owned);
                let never_read = row["fidelity"]["read_thread"].is_null();
                let cause = recorded.or_else(|| linked_cause.clone().filter(|c| not_checkable(c) && never_read));
                if let Some(cause) = cause.filter(|_| unchecked) {
                    row["fidelity"]["checkable"] = json!(false);
                    row["fidelity"]["reading"] = json!(cause);
                }
                let candidates_not_checkable = linked.is_none()
                    && row["subAgent"]["unread"].as_array().is_none_or(|u| u.is_empty())
                    && row["subAgent"]["notCheckable"].as_array().is_some_and(|n| !n.is_empty() && n.iter().all(|c| c["final"] == true));
                let final_reading = row["fidelity"]["reading"].as_str().is_some_and(not_checkable_final);
                row["readAgain"] = if row["fidelity"]["checkable"] == false && final_reading {
                    json!({"offered":false,"reason":"reading again would read the same: the sub-agent's input is not checkable"})
                } else if candidates_not_checkable {
                    json!({"offered":false,"reason":"reading again would read the same: no sub-agent's input here is checkable; link the one that ran the trial"})
                } else {
                    json!({"offered":true})
                };
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
            "sequence":b.trial.as_deref().and_then(|t| self.trials.link(t)).map(|l| l["trial"]["sequence"].clone()),"draftName":b.trial.as_deref().map(|t| self.trial_draft_name(t)),
            "target":{"generation":b.target.0,"threadId":b.target.1},"source":b.source,"prompt":b.prompt,"transcript":b.transcript,"card":b.card,
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
                            Some(Err((cause, seen))) if (cause == NOT_YET_TURN || cause == NOT_YET_MESSAGE || cause == INPUT_NOT_A_USER_MESSAGE) && *seen != signature => {}
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
                                TrialObservation::SubAgentLinked { child_thread: child.clone(), method: TrialLinkMethod::BeginMarker },
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

    /// TT-9 explicit link control / unlink. A display relation, not an act; no operator identity is captured.
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
            TrialObservation::SubAgentLinked { child_thread: child.to_owned(), method: TrialLinkMethod::ExplicitControl }
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
    let result = response
        .get("result")
        .filter(|r| r.is_object())
        .cloned()
        .ok_or_else(|| format!("{method} returned no result (outcome {})", evidence["outcome"]))?;
    crate::native_history::validate_read_response(method, &result)?;
    Ok(result)
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
/// `client` when given, else the first), as TT-9 reads them. For a sub-agent
/// (no `client`), a first turn holding items but no user message reads "not
/// checkable": `INPUT_ENCRYPTED`, final, when an item shows Codex's
/// inter-agent task with encrypted content; else `INPUT_NOT_A_USER_MESSAGE`,
/// which is read again on new activity and by Read again, since a user message
/// may still be listed. A clean trial's turn (with `client`) and a turn with no
/// items yet read "not yet".
fn first_user_texts(items: &[Value], client: Option<&str>, kind: TrialKind) -> Result<Vec<String>, String> {
    let messages: Vec<&Value> = items.iter().filter(|i| i["type"] == "userMessage").collect();
    if kind == TrialKind::Delegated && messages.is_empty() && !items.is_empty() {
        return Err(if items.iter().any(inter_agent_task) { INPUT_ENCRYPTED } else { INPUT_NOT_A_USER_MESSAGE }.into());
    }
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
/// TT-9: a sub-agent input the App cannot read. Each starts with
/// `NOT_CHECKABLE`. Only `INPUT_ENCRYPTED` is final (reading again reads the
/// same, so Read again is not offered); `INPUT_NOT_A_USER_MESSAGE` rests on
/// the absence of a user message and stays open to reading again.
const NOT_CHECKABLE: &str = "not checkable: ";
pub(crate) const INPUT_ENCRYPTED: &str =
    "not checkable: the sub-agent's task arrived as an encrypted inter-agent message (Codex 0.160.0 delivers a spawned sub-agent's task this way), not as a user message, so the App cannot read what it was given";
pub(crate) const INPUT_NOT_A_USER_MESSAGE: &str =
    "not checkable: the sub-agent's first turn, as read, holds no user message, so the App cannot read what it was given (at Codex 0.160.0 a spawned sub-agent's task arrives as an encrypted inter-agent message); Read again reads it again";
pub(crate) fn not_checkable(cause: &str) -> bool {
    cause.starts_with(NOT_CHECKABLE)
}
/// A not-checkable reading that reading again cannot change.
pub(crate) fn not_checkable_final(cause: &str) -> bool {
    cause == INPUT_ENCRYPTED
}
/// An item showing Codex's inter-agent task message rather than a user
/// message: an agent message whose content carries `encrypted_content`, or
/// whose readable header names a new task (the shape of the 0.160.0 rollout's
/// `agent_message` with author and recipient).
fn inter_agent_task(item: &Value) -> bool {
    let kind = item["type"].as_str().unwrap_or_default();
    if !matches!(kind, "agentMessage" | "agent_message") {
        return false;
    }
    let content = || item["content"].as_array().into_iter().flatten();
    let encrypted = content().any(|e| e["type"] == "encrypted_content" || e.get("encrypted_content").is_some());
    let header = |t: &str| t.trim_start().starts_with("Message Type: NEW_TASK");
    let headed = item["text"].as_str().is_some_and(header) || content().any(|e| e["text"].as_str().is_some_and(header));
    encrypted || headed
}
/// TT-9's read of a child's (or a clean trial's) first user message.
fn read_first_user_texts(home: &HomeSession, generation: &Value, thread: &str, turn: Option<&str>, client: Option<&str>, kind: TrialKind, by: &Value) -> Result<Vec<String>, String> {
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
    first_user_texts(&items, client, kind)
}
/// Performs the reads `trial_reads_due` returned. Holds no App lock.
pub(crate) fn perform_trial_reads(home: &HomeSession, reads: Vec<TrialRead>) -> Vec<TrialReadResult> {
    reads
        .into_iter()
        .map(|read| {
            let texts = match &read {
                TrialRead::Child { generation, child, .. } => read_first_user_texts(home, generation, child, None, None, TrialKind::Delegated, &rule_read()),
                TrialRead::CleanFirstTurn { generation, thread, turn, client, .. } => read_first_user_texts(home, generation, thread, Some(turn), Some(client), TrialKind::Clean, &rule_read()),
            };
            TrialReadResult { read, texts }
        })
        .collect()
}

const IN_PROGRESS: &str = "read in progress";
/// The child as the view shows it now, compared to decide a re-read: its
/// descendant node (last native call, activity, status, thread read) and the
/// counts of its own items and turns (H-7). A node first seen through
/// `subAgentActivity` is built once and does not change, so the child's own
/// rows are what show its new activity.
fn node_signature(view: &Value, child: &str) -> String {
    let node = view["descendants"].as_array().into_iter().flatten().find(|d| d["threadId"] == child).map(Value::to_string).unwrap_or_default();
    let items = view["items"].as_array().into_iter().flatten().filter(|r| r["threadId"] == child).count();
    let turns = view["turns"].as_array().into_iter().flatten().filter(|t| t["threadId"] == child).count();
    format!("{node}|items:{items}|turns:{turns}")
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
pub(crate) fn send_trial(root: &Mutex<WorkflowRootSession>, home: &HomeSession, reference: &str, generation: &Value, thread: &str, person_text: &str) -> Result<Value, SendRefusal> {
    // A refusal before anything is written leaves the trial as it was: still
    // pre-filled unless it was absent or another send of it is under way.
    let still = |root: &WorkflowRootSession| root.trial_desk.pending.get(reference).is_some_and(|p| !p.in_flight);
    let refuse = |root: &WorkflowRootSession, message: String| SendRefusal { prefill_kept: still(root), message };
    let Some(home_key) = generation["home"].as_str().map(str::to_owned) else {
        return Err(refuse(&root.lock().unwrap(), "generation home required; nothing sent".into()));
    };
    if let Err(e) = current_conversation(&home.host.snapshot(), generation, thread) {
        return Err(refuse(&root.lock().unwrap(), format!("{e}; nothing sent")));
    }
    // Runtime before Root (host_status's lock order).
    let baseline = all_descendants(&home.runtime.lock().unwrap().native_view());
    let (elements, client, kind) = {
        let mut root = root.lock().unwrap();
        match root.pending_notice_for(&home_key, thread) {
            Err(e) => return Err(refuse(&root, format!("{e}; nothing sent"))),
            Ok(Some(_)) => return Err(refuse(&root, "A workflow run ended in this conversation and its end notice goes first with the next message (WR TX-5); send that message first, then send the trial. Nothing sent; the trial stays pre-filled".into())),
            Ok(None) => {}
        }
        let clean_here = root.trial_conversation(thread);
        let Some(p) = root.trial_desk.pending.get_mut(reference) else {
            return Err(SendRefusal::not_kept(format!("No pre-filled trial {reference}; press Try again")));
        };
        if p.in_flight {
            return Err(SendRefusal::not_kept("This trial message is being sent now; nothing sent again"));
        }
        match p.kind {
            TrialKind::Delegated => {
                if clean_here.is_some() {
                    return Err(SendRefusal::kept("A delegated trial is sent in an authoring conversation, not in a trial conversation. Nothing sent"));
                }
                p.authoring = Some((generation.clone(), thread.to_owned()));
            }
            TrialKind::Clean => match &p.clean {
                Some((g, t)) if g == generation && t == thread => {}
                _ => return Err(SendRefusal::kept("A clean trial is sent in its own new conversation: start it with Send in the new trial conversation. Nothing sent")),
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
            return Err(SendRefusal::kept(format!("{reason}. No trial link was written; the trial stays pre-filled (WR §5.5)")));
        }
        Err(reason) => {
            root.trial_desk.pending.remove(reference);
            return Err(SendRefusal::not_kept(format!("{reason}. The send's outcome is not established: no trial link was written and nothing is resent (WR TT-4); press Try again for a new trial")));
        }
    };
    let p = root.trial_desk.pending.remove(reference).ok_or_else(|| SendRefusal::not_kept("pre-filled trial lost while sending"))?;
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
        Err(cause) => Err(SendRefusal::not_kept(format!("The trial message was sent (turn {}) but its trial link could not be written: {cause}. Nothing is resent", turn.unwrap_or_else(|| "not named".into())))),
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
            (Ok(text), Some(turn)) => match read_first_user_texts(home, &generation, &thread, Some(turn), trial["client_message"].as_str(), TrialKind::Clean, &person_read()) {
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
        let reading = match read_first_user_texts(home, &generation, &child, None, None, TrialKind::Delegated, &person_read()) {
            Ok(texts) => text.fidelity(&texts.iter().map(String::as_str).collect::<Vec<_>>()),
            Err(cause) if not_checkable(&cause) => FidelityReading::NotChecked { limits: vec![cause] },
            Err(cause) => FidelityReading::NotChecked { limits: vec![format!("the sub-agent's first turn could not be read: {cause}")] },
        };
        let observation = TrialObservation::Fidelity { read_thread: Some(child), reading, limits: vec!["read again at the person's request".into()] };
        results.push(root.lock().unwrap().trials.record_observation(reference, observation)?);
        return Ok(json!({"reference":reference,"recorded":results}));
    }
    let marker = text.begin_marker();
    let mut unread = vec![];
    let mut not_checkable_children = vec![];
    for child in candidates {
        match read_first_user_texts(home, &generation, &child, None, None, TrialKind::Delegated, &person_read()) {
            Ok(texts) if texts.iter().any(|t| t.contains(&marker)) => {
                let mut root = root.lock().unwrap();
                if root.linked_child(reference).is_some() {
                    if let Some(s) = root.trial_desk.sent.get_mut(reference) {
                        s.also_given.insert(child);
                    }
                    continue;
                }
                let reading = text.fidelity(&texts.iter().map(String::as_str).collect::<Vec<_>>());
                results.push(root.trials.record_observation(reference, TrialObservation::SubAgentLinked { child_thread: child.clone(), method: TrialLinkMethod::BeginMarker })?);
                results.push(root.trials.record_observation(reference, TrialObservation::Fidelity { read_thread: Some(child), reading, limits: vec!["read at the person's request".into()] })?);
            }
            Ok(_) => {}
            Err(cause) if not_checkable(&cause) => {
                if let Some(s) = root.lock().unwrap().trial_desk.sent.get_mut(reference) {
                    s.read.insert(child.clone(), Err((cause.clone(), String::new())));
                }
                not_checkable_children.push(json!({"thread":child,"reading":cause}));
            }
            Err(cause) => {
                if let Some(s) = root.lock().unwrap().trial_desk.sent.get_mut(reference) {
                    s.read.insert(child.clone(), Err((cause.clone(), String::new())));
                }
                unread.push(json!({"thread":child,"limit":cause}));
            }
        }
    }
    Ok(json!({"reference":reference,"recorded":results,"inputNotRead":unread,"inputNotCheckable":not_checkable_children}))
}

/// A boundary is an original run/check correspondence, never marker text.
#[derive(Clone)]
struct ExactBoundary {
    turn: String,
    client: String,
    text: Value,
}
impl From<&crate::historical_run_learning::Boundary> for ExactBoundary {
    fn from(value: &crate::historical_run_learning::Boundary) -> Self {
        Self {
            turn: value.turn.clone(),
            client: value.client_message.clone(),
            text: value.text_identity.clone(),
        }
    }
}
/// The source a bring-back or Compare reads: conversation and exact turn range.
struct HistorySource {
    thread: String,
    start: Option<ExactBoundary>,
    stops: Vec<ExactBoundary>,
    label: TranscriptSource,
    trial_line: Option<TrialTextLine>,
}
fn current_history_source(home: &HomeSession, generation: &Value) -> Result<(), String> {
    crate::recovery::generation_ref(generation)?;
    let snapshot = home.host.snapshot();
    if snapshot["state"] != "ready" || snapshot["generation"] != *generation {
        return Err("native history source generation is stale or unavailable".into());
    }
    Ok(())
}
fn source_live(home: &HomeSession, generation: &Value, thread: &str) -> bool {
    let view = home.runtime.lock().unwrap().native_view();
    view["generation"] == *generation && thread_live(&view, thread)
}
fn check_boundary(items: &[Value], boundary: &ExactBoundary) -> Result<(), String> {
    let matching: Vec<_> = items
        .iter()
        .filter(|item| item["type"] == "userMessage" && item["clientId"] == boundary.client)
        .collect();
    let [message] = matching.as_slice() else {
        return Err(
            "the record-correlated native boundary has no unique exact client message".into(),
        );
    };
    let text = message["content"]
        .as_array()
        .and_then(|content| content.first())
        .filter(|element| element["type"] == "text")
        .and_then(|element| element["text"].as_str())
        .ok_or("the record-correlated boundary's first text element is unavailable")?;
    if crate::role_supply::content(text.as_bytes()) != boundary.text {
        return Err(
            "the record-correlated boundary text differs or uses an unsupported identity method"
                .into(),
        );
    }
    Ok(())
}
fn read_source(
    home: &HomeSession,
    generation: &Value,
    source: &HistorySource,
) -> Result<(Vec<TurnRead>, Option<String>), String> {
    current_history_source(home, generation)?;
    let (turns, limit) = read_turns(home, generation, &source.thread, &person_read());
    if let Some(reason) = &limit {
        return Err(format!("source conversation's current turn list is incomplete; no inactive-source reading established: {reason}"));
    }
    if turns.iter().any(|turn| turn["status"] == "inProgress") {
        return Err(
            "A turn is live in that source conversation; Bring back waits until none is live"
                .into(),
        );
    }
    let reading: Vec<_> = turns
        .iter()
        .map(|turn| json!({"id":turn["id"],"status":turn["status"]}))
        .collect();
    let position = |boundary: &ExactBoundary| -> Result<usize, String> {
        let found: Vec<_> = turns
            .iter()
            .enumerate()
            .filter(|(_, turn)| turn["id"] == boundary.turn)
            .map(|(i, _)| i)
            .collect();
        match found.as_slice() {
            [position] => Ok(*position),
            _ => Err(
                "the original run boundary turn is missing or ambiguous in native history".into(),
            ),
        }
    };
    let first = source
        .start
        .as_ref()
        .map(&position)
        .transpose()?
        .unwrap_or(0);
    let mut last = turns.len();
    for stop in &source.stops {
        let end = position(stop)?;
        if end <= first {
            return Err("the original end boundary does not follow this run's start".into());
        }
        let items = read_items(home, generation, &source.thread, &stop.turn, &person_read())?;
        check_boundary(&items, stop)?;
        last = last.min(end);
    }
    let mut reads = Vec::new();
    for (position, turn) in turns.into_iter().enumerate().take(last).skip(first) {
        let id = turn["id"]
            .as_str()
            .filter(|id| !id.is_empty())
            .ok_or("native history returned an unnamed turn")?;
        if turn["status"] == "inProgress" {
            return Err(
                "A turn is live in that source conversation; Bring back waits until none is live"
                    .into(),
            );
        }
        let items = read_items(home, generation, &source.thread, id, &person_read());
        if position == first {
            if let Some(start) = &source.start {
                check_boundary(items.as_ref().map_err(Clone::clone)?, start)?;
            }
        }
        reads.push(TurnRead { turn, items });
    }
    current_history_source(home, generation)?;
    let (after, limit) = read_turns(home, generation, &source.thread, &person_read());
    if limit.is_some()
        || after
            .iter()
            .map(|turn| json!({"id":turn["id"],"status":turn["status"]}))
            .collect::<Vec<_>>()
            != reading
    {
        return Err("source conversation's turn range changed or became unreadable during history reading; read again".into());
    }
    Ok((reads, limit))
}
impl WorkflowRootSession {
    fn trial_source(&self, reference: &str) -> Result<HistorySource, String> {
        let link = self
            .trials
            .link(reference)
            .cloned()
            .ok_or_else(|| format!("No trial link {reference}"))?;
        let trial = &link["trial"];
        let clean = trial["kind"] == "clean";
        let thread = if clean {
            trial["clean_conversation"]
                .as_str()
                .map(str::to_owned)
                .ok_or("the clean trial names no conversation")?
        } else {
            self.linked_child(reference).ok_or_else(|| {
                format!(
                    "No sub-agent is linked to trial {}; link one first",
                    trial["sequence"]
                )
            })?
        };
        let line = self.trial_text(reference).ok().map(|text| {
            let fidelity = self
                .trials
                .observations(reference)
                .into_iter()
                .rev()
                .find(|o| o["observation"] == "fidelity")
                .map(|o| {
                    o["fidelity"]["state"]
                        .as_str()
                        .unwrap_or("not checked")
                        .to_owned()
                })
                .unwrap_or_else(|| "not checked".into());
            TrialTextLine {
                run_text: text.run_text().to_owned(),
                line: format!(
                    "[trial text of trial {}: identity {}, {} bytes; fidelity {fidelity}]",
                    trial["sequence"],
                    rev12(text.identity()["value"].as_str().unwrap_or_default()),
                    text.bytes()
                ),
            }
        });
        Ok(HistorySource {
            thread: thread.clone(),
            start: if clean {
                Some(ExactBoundary {
                    turn: trial["turn"]
                        .as_str()
                        .filter(|s| !s.is_empty())
                        .ok_or("clean trial's original turn acknowledgment is unavailable")?
                        .into(),
                    client: trial["client_message"]
                        .as_str()
                        .filter(|s| !s.is_empty())
                        .ok_or("clean trial's original client message is unavailable")?
                        .into(),
                    text: trial["text_identity"].clone(),
                })
            } else {
                None
            },
            stops: Vec::new(),
            label: TranscriptSource::Trial {
                sequence: trial["sequence"].as_u64().unwrap_or(0),
                draft_name: link["draft"]["name"]
                    .as_str()
                    .unwrap_or_default()
                    .to_owned(),
                rev12: rev12(link["content"]["value"].as_str().unwrap_or_default()).to_owned(),
                clean,
                thread,
            },
            trial_line: line,
        })
    }
}

fn live_stop(
    root: &WorkflowRootSession,
    run: &super::WorkflowRun,
) -> Result<Option<ExactBoundary>, String> {
    if run.lifecycle == RunLifecycle::Open {
        return Ok(None);
    }
    if run.lifecycle != RunLifecycle::Ended {
        return Err("The run start was not established; nothing to read".into());
    }
    if let super::NoticeState::Sent {
        published,
        client_id,
        turn: Some(turn),
        ..
    } = &run.notice
    {
        return Ok(Some(ExactBoundary {
            turn: turn.clone(),
            client: client_id.clone(),
            text: published.run_text_record().body()["text_identity"].clone(),
        }));
    }
    let scope = run.prepared().scope();
    let mut following = Vec::new();
    for (reference, owner) in &root.runs {
        if reference == &scope.run {
            continue;
        }
        let Ok(other) = owner.try_lock() else {
            continue;
        };
        let prepared = other.prepared();
        if prepared.scope().home == scope.home
            && prepared.scope().conversation == scope.conversation
            && prepared.record()["chain"]["prior_run"] == scope.run
        {
            if let Some(turn) = &other.turn_id {
                following.push(ExactBoundary {
                    turn: turn.clone(),
                    client: other.client_id.clone(),
                    text: prepared.record()["text_identity"].clone(),
                });
            }
        }
    }
    match following.len() {
        1 => Ok(following.pop()),
        _ => Err("the ended run has no unique original carried end notice or following-run boundary; later turns are not read as this run".into()),
    }
}
fn slot(workflow: &Value, _holding: &str) -> Value {
    json!({"origin":workflow["origin"],"sourceRoot":workflow["source_root"],"name":workflow["name"]})
}
pub(crate) fn recovery_facts(homes: &[std::sync::Arc<HomeSession>]) -> (Vec<Value>, Vec<Value>) {
    fn events(value: &Value, out: &mut Vec<Value>) {
        match value {
            Value::Object(map) => {
                if let Some(rows) = map.get("restartEvents").and_then(Value::as_array) {
                    out.extend(rows.iter().cloned());
                }
                for (key, child) in map {
                    if key != "restartEvents" {
                        events(child, out);
                    }
                }
            }
            Value::Array(values) => {
                for child in values {
                    events(child, out);
                }
            }
            _ => {}
        }
    }
    let (mut rows, mut restart) = (Vec::new(), Vec::new());
    for home in homes {
        rows.extend(home.host.recovery_entries());
        events(&home.host.recovery_custody().snapshot(), &mut restart);
    }
    (rows, restart)
}
fn recorded_home(
    homes: &[std::sync::Arc<HomeSession>],
    class: &str,
    thread: &str,
) -> Result<std::sync::Arc<HomeSession>, String> {
    let candidates: Vec<_> = homes
        .iter()
        .filter(|home| crate::stop_records::home_class(home.class().as_str()) == Some(class))
        .collect();
    let [home] = candidates.as_slice() else {
        return Err(format!(
            "native home {class} is missing or ambiguous; no active-home fallback"
        ));
    };
    let snapshot = home.host.snapshot();
    if thread.is_empty() {
        return Err("native history source conversation unavailable".into());
    }
    current_history_source(home, &snapshot["generation"])?;
    Ok((*home).clone())
}
fn live_context(root: &WorkflowRootSession, run: &super::WorkflowRun) -> Result<Value, String> {
    let end = live_stop(root, run)?;
    let scope = run.prepared().scope();
    Ok(
        json!({"prepared":run.prepared().record(),"scope":{"run":scope.run,"conversation":scope.conversation,"home":scope.home,"generation":scope.generation,"holdingLibrary":scope.holding_library},"client":run.client_id,"turn":run.turn_id,
        "ended":run.lifecycle==RunLifecycle::Ended,"end":end.map(|e|json!({"turn":e.turn,"client":e.client,"text":e.text}))}),
    )
}
enum LearningProof {
    Trial {
        reference: String,
        link: Value,
        home_thread: String,
    },
    Live {
        reference: String,
        owner: std::sync::Arc<Mutex<super::WorkflowRun>>,
        context: Value,
        binding: crate::workflow_workspace::publication::ProjectSourceBinding,
    },
    Historical {
        records: crate::workflow_workspace::publication::ProjectRecords,
        run: crate::historical_run_learning::HistoricalRun,
        home: crate::historical_run_learning::SourceHome,
    },
}
struct LearningSource {
    history: HistorySource,
    home: std::sync::Arc<HomeSession>,
    generation: Value,
    proof: LearningProof,
    version: Value,
    slot: Value,
    files: Option<BTreeMap<String, Vec<u8>>>,
    standing: String,
}
impl LearningSource {
    fn recheck(
        &self,
        root: &Mutex<WorkflowRootSession>,
        homes: &[std::sync::Arc<HomeSession>],
    ) -> Result<(), String> {
        current_history_source(&self.home, &self.generation)?;
        if source_live(&self.home, &self.generation, &self.history.thread) {
            return Err("A turn became live in the source conversation; nothing pre-filled".into());
        }
        match &self.proof {
            LearningProof::Trial {
                reference,
                link,
                home_thread,
            } => {
                let root = root.lock().unwrap();
                if root.trials.link(reference) != Some(link)
                    || root.trial_source(reference)?.thread != self.history.thread
                {
                    return Err("trial source changed during native history reading".into());
                }
                if root.trial_home_thread(reference).as_deref() != Some(home_thread) {
                    return Err("trial's native home anchor changed".into());
                }
                let home = home_holding(homes, home_thread)
                    .ok_or("trial native source became missing or ambiguous")?;
                if !std::sync::Arc::ptr_eq(&home, &self.home) {
                    return Err("trial native source home changed".into());
                }
            }
            LearningProof::Live {
                reference,
                owner,
                context,
                binding,
            } => {
                let root = root.lock().unwrap();
                if !root
                    .runs
                    .get(reference)
                    .is_some_and(|now| std::sync::Arc::ptr_eq(now, owner))
                {
                    return Err("original run owner changed".into());
                }
                let run = owner
                    .try_lock()
                    .map_err(|_| "original run operation pending")?;
                if live_context(&root, &run)? != *context
                    || !binding.same_source(&run.project.source_binding()?)
                {
                    return Err(
                        "original run/project records source changed during native history reading"
                            .into(),
                    );
                }
            }
            LearningProof::Historical { records, run, home } => {
                let (rows, events) = recovery_facts(homes);
                run.recheck_with_recovery(records, &rows)?;
                let now = run.source_home(&rows, &events)?;
                if now.home_class != home.home_class
                    || now.recorded_generations != home.recorded_generations
                    || now.evidence != home.evidence
                {
                    return Err("historical REC source correspondence changed during native history reading".into());
                }
                let current = recorded_home(homes, &home.home_class, &run.conversation)?;
                if !std::sync::Arc::ptr_eq(&current, &self.home) {
                    return Err("historical native source home changed".into());
                }
            }
        }
        Ok(())
    }
    fn source_view(&self) -> Value {
        let mut view = json!({"threadId":self.history.thread,"generation":self.generation,"modeHomeClass":self.home.class().as_str(),"standing":self.standing});
        if let LearningProof::Historical { records, run, home } = &self.proof {
            view["project"] = json!(records.root());
            view["workflow"] = run.workflow.clone();
            view["limits"] = json!(run.limits);
            view["recordedNativeSource"] = json!({"homeClass":home.home_class,"generations":home.recorded_generations,"evidence":home.evidence,
                "standing":"quoted original REC provenance, including recorded paths; no current path or native authority inferred"});
        }
        view
    }
}
fn resolve_learning(
    root: &Mutex<WorkflowRootSession>,
    homes: &[std::sync::Arc<HomeSession>],
    project: Option<&std::path::Path>,
    trial: Option<&str>,
    run: Option<&str>,
) -> Result<LearningSource, String> {
    if let (Some(reference), None) = (trial, run) {
        let root = root.lock().unwrap();
        let history = root.trial_source(reference)?;
        let home_thread = root
            .trial_home_thread(reference)
            .ok_or("trial's native home anchor unavailable")?;
        let home = home_holding(homes, &home_thread)
            .ok_or("trial native history source is not loaded or is ambiguous across homes")?;
        let generation = home.host.snapshot()["generation"].clone();
        return Ok(LearningSource {
            history,
            home,
            generation,
            proof: LearningProof::Trial {
                reference: reference.into(),
                home_thread,
                link: root
                    .trials
                    .link(reference)
                    .cloned()
                    .ok_or("trial link unavailable")?,
            },
            version: Value::Null,
            slot: Value::Null,
            files: None,
            standing: "trial history reading; no workflow run or act inferred".into(),
        });
    }
    let (None, Some(reference)) = (trial, run) else {
        return Err("Bring back takes one trial or one run".into());
    };
    {
        let root = root.lock().unwrap();
        if let Some(owner) = root.runs.get(reference) {
            let run = owner
                .try_lock()
                .map_err(|_| "original run operation pending")?;
            if let Some(project) = project {
                if run.project_root != project {
                    return Err("run belongs to another opened project".into());
                }
            }
            let prepared = run.prepared();
            let scope = prepared.scope();
            let workflow = prepared.workflow();
            let history = HistorySource {
                thread: scope.conversation.clone(),
                start: Some(ExactBoundary {
                    turn: run
                        .turn_id
                        .clone()
                        .ok_or("original run start was not acknowledged")?,
                    client: run.client_id.clone(),
                    text: prepared.record()["text_identity"].clone(),
                }),
                stops: live_stop(&root, &run)?.into_iter().collect(),
                label: TranscriptSource::Run {
                    run: scope.run.clone(),
                    origin: workflow.origin.clone(),
                    name: workflow.name.clone(),
                    rev12: rev12(&workflow.revision).into(),
                    thread: scope.conversation.clone(),
                },
                trial_line: None,
            };
            let files = run.selection.snapshot().files().clone();
            let home = run.home.clone();
            if !homes
                .iter()
                .any(|candidate| std::sync::Arc::ptr_eq(candidate, &home))
            {
                return Err("original run native source home is not available".into());
            }
            let generation = home.host.snapshot()["generation"].clone();
            current_history_source(&home, &generation)?;
            let workflow =
                serde_json::to_value(run.prepared().workflow()).map_err(|e| e.to_string())?;
            return Ok(LearningSource {
                history,
                home,
                generation,
                proof: LearningProof::Live {
                    reference: reference.into(),
                    owner: owner.clone(),
                    context: live_context(&root, &run)?,
                    binding: run.project.source_binding()?,
                },
                version: json!({"method":workflow["revision_method"],"value":workflow["revision"]}),
                slot: slot(&workflow, &run.prepared().scope().holding_library),
                files: Some(files),
                standing:
                    "original run owner and exact native history correspondence; transcript only"
                        .into(),
            });
        }
    }
    let records = crate::workflow_workspace::publication::ProjectRecords::open(
        project.ok_or("historical run reading requires the explicit opened project")?,
    )?;
    let (rows, events) = recovery_facts(homes);
    let historical = crate::historical_run_learning::HistoricalRun::read_with_recovery(
        &records, reference, &rows,
    )?;
    if historical.recorded_ended && historical.end_candidates.is_empty() {
        return Err("closed historical run has no original native end boundary; later turns are not read as its activity".into());
    }
    let source_home = historical.source_home(&rows, &events)?;
    let home = recorded_home(homes, &source_home.home_class, &historical.conversation)?;
    let generation = home.host.snapshot()["generation"].clone();
    let workflow = historical.workflow.clone();
    let holding = historical.holding_library.clone();
    let files = historical_files(root, &workflow, &holding);
    let history = HistorySource {
        thread: historical.conversation.clone(),
        start: Some((&historical.start).into()),
        stops: historical.end_candidates.iter().map(Into::into).collect(),
        label: TranscriptSource::Run {
            run: historical.run.clone(),
            origin: workflow["origin"].as_str().unwrap_or_default().into(),
            name: workflow["name"].as_str().unwrap_or_default().into(),
            rev12: rev12(workflow["revision"].as_str().unwrap_or_default()).into(),
            thread: historical.conversation.clone(),
        },
        trial_line: None,
    };
    Ok(LearningSource { history, home, generation, proof:LearningProof::Historical { records, run:historical, home:source_home },
        version:json!({"method":workflow["revision_method"],"value":workflow["revision"]}), slot:slot(&workflow,&holding), files,
        standing:"historical quoted record and native-history correspondence; unsigned evidence, no live run, supply, selection or act custody restored".into() })
}
fn historical_files(
    root: &Mutex<WorkflowRootSession>,
    workflow: &Value,
    holding: &str,
) -> Option<BTreeMap<String, Vec<u8>>> {
    let identity: crate::workflow_workspace::WorkflowIdentity =
        serde_json::from_value(workflow.clone()).ok()?;
    let libraries: Vec<_> = root
        .lock()
        .ok()?
        .libraries
        .values()
        .filter(|library| {
            library.origin == identity.origin && library.source_root == identity.source_root
        })
        .cloned()
        .collect();
    let [library] = libraries.as_slice() else {
        return None;
    };
    let owner = library.owner.try_lock().ok()?;
    let stored = owner.store_copy(&identity);
    if stored.parent()?.to_str() != Some(holding) {
        return None;
    }
    let snapshot = Snapshot::capture(&stored).ok()?;
    (identity.revision_method == crate::workflow_workspace::SNAPSHOT_METHOD
        && snapshot.revision() == identity.revision)
        .then(|| snapshot.files().clone())
}
/// Cheap availability only: strict record and native-history correspondence is
/// read on the person's press, never N full project scans while rendering.
pub(crate) fn learning_status(
    homes: &[std::sync::Arc<HomeSession>],
    project: Option<&std::path::Path>,
    run: &str,
    conversation: Option<&str>,
) -> Value {
    let (rows, events) = recovery_facts(homes);
    learning_status_with_facts(homes, project, run, conversation, &rows, &events)
}

/// Reuse one REC snapshot for all reopened runs; no native-history reads.
pub(crate) fn learning_status_with_facts(
    homes: &[std::sync::Arc<HomeSession>],
    project: Option<&std::path::Path>,
    run: &str,
    conversation: Option<&str>,
    rows: &[Value],
    events: &[Value],
) -> Value {
    let result = (|| -> Result<(), String> {
        if project.is_none() {
            return Err("explicit opened project unavailable".into());
        }
        let thread = conversation
            .filter(|s| !s.is_empty())
            .ok_or("recorded conversation unavailable")?;
        let source =
            crate::historical_run_learning::source_home_for_run(run, thread, rows, events)?;
        recorded_home(homes, &source.home_class, thread)?;
        Ok(())
    })();
    let offered = result.is_ok();
    let reason = result.err();
    let version_candidate = project.is_some() && !run.is_empty();
    json!({"bringBack":{"offered":offered,"reason":reason},"compare":{"offered":version_candidate,"reason":if version_candidate {None}else{Some("explicit project and recorded run required")},"activityLimit":reason},
        "standing":"historical records; exact record and native-history correspondence read on request; no live run, selection or act custody restored"})
}

/// SQ-BB BB-1…BB-4: read the trial's conversation (clean) or linked
/// sub-agent (delegated), or a real run's turns from its start turn to its end
/// mark, through Codex's history, and pre-fill the transcript in `thread`'s
/// composer, unsent. Waits (refuses) while a turn is live in the source.
pub(crate) fn bring_back_with_homes(
    root: &Mutex<WorkflowRootSession>,
    homes: &[std::sync::Arc<HomeSession>],
    project: Option<&std::path::Path>,
    target_home: &HomeSession,
    trial: Option<&str>,
    run: Option<&str>,
    generation: &Value,
    thread: &str,
    include_native: bool,
) -> Result<Value, String> {
    current_conversation(&target_home.host.snapshot(), generation, thread)
        .map_err(|e| format!("{e}; nothing pre-filled"))?;
    let source = resolve_learning(root, homes, project, trial, run)?;
    if source_live(&source.home, &source.generation, &source.history.thread) {
        return Err(
            "A turn is live in that source conversation; Bring back waits until none is live"
                .into(),
        );
    }
    let (turns, turns_limit) = read_source(&source.home, &source.generation, &source.history)?;
    source.recheck(root, homes)?;
    current_conversation(&target_home.host.snapshot(), generation, thread)
        .map_err(|e| format!("{e}; target changed while reading; nothing pre-filled"))?;
    let composed = transcript::compose_transcript(&TranscriptInput {
        source: source.history.label.clone(),
        read_at: crate::util::now_rfc3339(),
        turns: &turns,
        turns_limit,
        trial_text: source.history.trial_line.clone(),
        include_native,
        bound: transcript::TRANSCRIPT_BOUND,
    });
    let (card,prompt)=match &source.history.label {
        TranscriptSource::Trial { sequence,draft_name,rev12,.. }=>(format!("transcript of trial {sequence} of draft {draft_name} @ {rev12}, read from Codex history"),
            format!("Here is how trial {sequence} went. Please assess it against the draft: where the agent followed the workflow, where it departed or got stuck, and what you would change.")),
        TranscriptSource::Run {run,origin,name,..}=>(format!("transcript of run {run} of {origin}:{name}, read from Codex history; {}",source.standing),
            format!("Here is how a real run of {origin}:{name} went. Please assess it against the workflow: where the agent followed it, where it departed or got stuck, and what you would change in a new revision.")),
    };
    let id = crate::util::opaque_id("bring-back:")?;
    let pending = PendingBringBack {
        trial: trial.map(str::to_owned),
        run: run.map(str::to_owned),
        target: (generation.clone(), thread.into()),
        prompt,
        transcript: composed.text,
        card,
        shortenings: composed.shortenings,
        include_native,
        client: crate::util::opaque_id("bring-back-message:")?,
        in_flight: false,
        source: source.source_view(),
    };
    let view = json!({"id":id,"card":pending.card,"source":pending.source,"bytes":pending.transcript.len(),"shortenings":pending.shortenings,"state":"pre-filled; not sent"});
    // The source and target are checked again immediately before publication;
    // none of this constructs a live run, selection, supply or act capability.
    source.recheck(root, homes)?;
    current_conversation(&target_home.host.snapshot(), generation, thread)?;
    root.lock()
        .unwrap()
        .trial_desk
        .bring_backs
        .insert(id, pending);
    Ok(view)
}
#[cfg(test)]
pub(crate) fn bring_back(
    root: &Mutex<WorkflowRootSession>,
    home: &std::sync::Arc<HomeSession>,
    trial: Option<&str>,
    run: Option<&str>,
    generation: &Value,
    thread: &str,
    include_native: bool,
) -> Result<Value, String> {
    bring_back_with_homes(
        root,
        std::slice::from_ref(home),
        None,
        home,
        trial,
        run,
        generation,
        thread,
        include_native,
    )
}
pub(crate) fn cancel_bring_back(
    root: &Mutex<WorkflowRootSession>,
    id: &str,
) -> Result<Value, String> {
    let mut root = root.lock().unwrap();
    match root.trial_desk.bring_backs.get(id) {
        Some(b) if b.in_flight => {
            Err("This transcript is being sent now; it can no longer be removed".into())
        }
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
pub(crate) fn send_bring_back(
    root: &Mutex<WorkflowRootSession>,
    home: &HomeSession,
    id: &str,
    generation: &Value,
    thread: &str,
    person_text: &str,
) -> Result<Value, SendRefusal> {
    let still = |root: &WorkflowRootSession| {
        root.trial_desk
            .bring_backs
            .get(id)
            .is_some_and(|b| !b.in_flight)
    };
    let refuse = |root: &WorkflowRootSession, message: String| SendRefusal {
        prefill_kept: still(root),
        message,
    };
    if let Err(e) = current_conversation(&home.host.snapshot(), generation, thread) {
        return Err(refuse(&root.lock().unwrap(), format!("{e}; nothing sent")));
    }
    let Some(home_key) = generation["home"].as_str().map(str::to_owned) else {
        return Err(refuse(
            &root.lock().unwrap(),
            "generation home required; nothing sent".into(),
        ));
    };
    let (elements, client) = {
        let mut root = root.lock().unwrap();
        match root.pending_notice_for(&home_key, thread) {
            Err(e) => return Err(refuse(&root, format!("{e}; nothing sent"))),
            Ok(Some(_)) => return Err(refuse(&root, "A workflow run ended in this conversation and its end notice goes first with the next message (WR TX-5); send that message first. Nothing sent; the transcript stays pre-filled".into())),
            Ok(None) => {}
        }
        let Some(b) = root.trial_desk.bring_backs.get_mut(id) else {
            return Err(SendRefusal::not_kept(format!(
                "No pre-filled transcript {id}"
            )));
        };
        if b.in_flight {
            return Err(SendRefusal::not_kept(
                "This transcript is being sent now; nothing sent again",
            ));
        }
        b.in_flight = true;
        b.target = (generation.clone(), thread.to_owned());
        (
            [person_text.to_owned(), b.transcript.clone()]
                .into_iter()
                .filter(|e| !e.is_empty())
                .collect::<Vec<_>>(),
            b.client.clone(),
        )
    };
    let refs: Vec<&str> = elements.iter().map(String::as_str).collect();
    let outcome = home
        .host
        .turn_start_texts(generation, thread, &refs, &client);
    let mut root = root.lock().unwrap();
    match outcome {
        Ok(response) => {
            let b =
                root.trial_desk.bring_backs.remove(id).ok_or_else(|| {
                    SendRefusal::not_kept("pre-filled transcript lost while sending")
                })?;
            let turn = response["result"]["turn"]["id"].clone();
            let recorded = match &b.trial {
                Some(reference) => Some(root.trials.record_observation(
                    reference,
                    TrialObservation::BroughtBack {
                        target_conversation: thread.to_owned(),
                        transcript: b.transcript.clone(),
                        shortenings: b.shortenings.clone(),
                    },
                )),
                None => None,
            };
            match recorded {
                Some(Err(cause)) => Err(SendRefusal::not_kept(format!("The transcript was sent (turn {turn}) but its brought-back observation could not be written: {cause}. Nothing is resent"))),
                Some(Ok(observation)) => Ok(json!({"id":id,"turn":turn,"observation":observation})),
                None => Ok(json!({"id":id,"turn":turn,"observation":null,"limit":"a real run brought back has no trial link; nothing is recorded for it"})),
            }
        }
        Err(reason) if not_written(&reason) || refused(&reason) => {
            if let Some(b) = root.trial_desk.bring_backs.get_mut(id) {
                b.in_flight = false;
            }
            Err(SendRefusal::kept(format!(
                "{reason}. Nothing recorded; the transcript stays pre-filled"
            )))
        }
        Err(reason) => {
            root.trial_desk.bring_backs.remove(id);
            Err(SendRefusal::not_kept(format!(
                "{reason}. The send's outcome is not established; nothing is recorded or resent"
            )))
        }
    }
}

/// TT-11 Compare: two trials, or a trial and a real run of a revision of the
/// same slot, side by side with the difference between their versions (read
/// from the trial snapshots and the revision store). Scores and judges nothing;
/// records nothing.
pub(crate) fn compare_with_homes(
    root: &Mutex<WorkflowRootSession>,
    homes: &[std::sync::Arc<HomeSession>],
    project: Option<&std::path::Path>,
    left: &Value,
    right: &Value,
) -> Result<Value, String> {
    struct Side {
        label: String,
        kind: String,
        version: Value,
        conversation: Value,
        snapshot: Value,
        files: Option<BTreeMap<String, Vec<u8>>>,
        slot: Value,
        source: Result<LearningSource, String>,
        version_proof: Option<(
            crate::workflow_workspace::publication::ProjectRecords,
            crate::historical_run_learning::HistoricalVersion,
        )>,
    }
    let side = |spec: &Value| -> Result<Side, String> {
        if let Some(reference) = spec["trial"].as_str() {
            let (label, kind, version, conversation, snapshot, files, slot) = {
                let locked = root.lock().unwrap();
                let (link, library) = locked.link_and_library(reference)?;
                let name = link["draft"]["name"].as_str().unwrap_or_default();
                let content = link["content"]["value"].as_str().unwrap_or_default();
                let folder = package_copy::content_folder(&library.root, TRIAL_AREA, name, content);
                let standing = package_copy::copy_standing(&folder, content);
                let files = if matches!(standing, CopyStanding::Current) {
                    Snapshot::capture(&folder)
                        .ok()
                        .filter(|snapshot| snapshot.revision() == content)
                        .map(|snapshot| snapshot.files().clone())
                } else {
                    None
                };
                let trial = &link["trial"];
                (
                    format!("trial {} of draft {name}", trial["sequence"]),
                    trial["kind"].as_str().unwrap_or_default().to_owned(),
                    link["content"].clone(),
                    transcript::trial_conversation(
                        &trial["authoring_conversation"],
                        &trial["clean_conversation"],
                        locked.linked_child(reference).as_deref(),
                    ),
                    transcript::trial_snapshot(&standing),
                    files,
                    json!({"origin":library.origin,"sourceRoot":library.source_root,"name":name}),
                )
            };
            return Ok(Side {
                label,
                kind,
                version,
                conversation,
                snapshot,
                files,
                slot,
                source: resolve_learning(root, homes, project, Some(reference), None),
                version_proof: None,
            });
        }
        if let Some(reference) = spec["run"].as_str() {
            match resolve_learning(root, homes, project, None, Some(reference)) {
                Ok(source) => {
                    return Ok(Side {
                        label: format!(
                            "run {reference} of {}:{}",
                            source.slot["origin"].as_str().unwrap_or_default(),
                            source.slot["name"].as_str().unwrap_or_default()
                        ),
                        kind: "registered run".into(),
                        version: source.version.clone(),
                        conversation: transcript::run_conversation(&source.history.thread),
                        snapshot: transcript::run_snapshot(),
                        files: source.files.clone(),
                        slot: source.slot.clone(),
                        source: Ok(source),
                        version_proof: None,
                    })
                }
                Err(reason) => {
                    if root.lock().unwrap().runs.contains_key(reference) {
                        return Err(reason);
                    }
                    let records = crate::workflow_workspace::publication::ProjectRecords::open(
                        project.ok_or("historical Compare requires the explicit opened project")?,
                    )?;
                    let version = crate::historical_run_learning::HistoricalVersion::read(
                        &records, reference,
                    )?;
                    let files = historical_files(root, &version.workflow, &version.holding_library);
                    let mut snapshot = transcript::run_snapshot();
                    snapshot["reading"]=json!("historical recorded version only; native activity correspondence unavailable; no live run or selection restored");
                    return Ok(Side {
                        label: format!(
                            "run {reference} of {}:{}",
                            version.workflow["origin"].as_str().unwrap_or_default(),
                            version.workflow["name"].as_str().unwrap_or_default()
                        ),
                        kind: "registered run".into(),
                        version: json!({"method":version.workflow["revision_method"],"value":version.workflow["revision"]}),
                        conversation: transcript::run_conversation(&version.conversation),
                        snapshot,
                        files,
                        slot: slot(&version.workflow, &version.holding_library),
                        source: Err(reason),
                        version_proof: Some((records, version)),
                    });
                }
            }
        }
        Err("Each side of Compare is a trial or a run".into())
    };
    let (a, b) = (side(left)?, side(right)?);
    let runs = [&a, &b]
        .iter()
        .filter(|side| side.kind == "registered run")
        .count();
    if runs == 2 {
        return Err("Compare takes two trials, or a trial and a real run".into());
    }
    if runs == 1 && a.slot != b.slot {
        return Err("Compare takes a trial and a real run of a revision of the same full source-qualified slot".into());
    }
    let summarize = |side: &Side| -> Result<Value, String> {
        let mut summary = match &side.source {
            Ok(source) => {
                let reading = read_source(&source.home, &source.generation, &source.history);
                source.recheck(root, homes)?;
                let mut summary = match reading {
                    Ok((turns, limit)) => transcript::activity_summary(&turns, limit.as_deref()),
                    Err(reason) => {
                        json!({"turns":0,"endings":[],"commands":{"run":0,"failed":0,"list":[]},"fileChanges":[],"finalAgentMessage":null,"limits":[reason]})
                    }
                };
                if let Some(limits) = summary["limits"].as_array_mut() {
                    limits.push(json!(source.standing));
                }
                if let LearningProof::Historical { run, .. } = &source.proof {
                    if let Some(limits) = summary["limits"].as_array_mut() {
                        limits.extend(run.limits.iter().map(|limit| json!(limit)));
                    }
                }
                summary
            }
            Err(reason) => {
                let mut limits = vec![json!(reason)];
                if let Some((_, version)) = &side.version_proof {
                    limits.extend(version.limits.iter().map(|limit| json!(limit)));
                }
                json!({"turns":0,"endings":[],"commands":{"run":0,"failed":0,"list":[]},"fileChanges":[],"finalAgentMessage":null,"limits":limits})
            }
        };
        if !summary.is_object() {
            summary = json!({"limits":["activity summary unavailable"]});
        }
        Ok(summary)
    };
    let (a_summary, b_summary) = (summarize(&a)?, summarize(&b)?);
    for side in [&a, &b] {
        if let Ok(source) = &side.source {
            source.recheck(root, homes)?;
        }
        if let Some((records, version)) = &side.version_proof {
            version.recheck(records)?;
        }
    }
    let view = |side: &Side, summary: Value| transcript::CompareSide {
        label: side.label.clone(),
        kind: side.kind.clone(),
        version: side.version.clone(),
        conversation: side.conversation.clone(),
        snapshot: side.snapshot.clone(),
        summary,
    };
    let difference = match (&a.files, &b.files) {
        (Some(x), Some(y)) => transcript::version_difference(x, y),
        _ => {
            json!({"limit":"exact source-qualified revision bytes are unavailable for one side; no version difference shown"})
        }
    };
    Ok(transcript::compare_result(
        &view(&a, a_summary),
        &view(&b, b_summary),
        difference,
    ))
}
#[cfg(test)]
pub(crate) fn compare(
    root: &Mutex<WorkflowRootSession>,
    resolve: &dyn Fn(&str) -> Option<std::sync::Arc<HomeSession>>,
    left: &Value,
    right: &Value,
) -> Result<Value, String> {
    let mut homes = Vec::new();
    for spec in [left, right] {
        let thread = {
            let locked = root.lock().unwrap();
            if let Some(reference) = spec["trial"].as_str() {
                locked.trial_home_thread(reference)
            } else {
                spec["run"]
                    .as_str()
                    .and_then(|reference| locked.runs.get(reference))
                    .and_then(|run| {
                        run.try_lock()
                            .ok()
                            .map(|run| run.prepared().scope().conversation.clone())
                    })
            }
        };
        if let Some(home) = thread.as_deref().and_then(resolve) {
            if !homes
                .iter()
                .any(|existing| std::sync::Arc::ptr_eq(existing, &home))
            {
                homes.push(home);
            }
        }
    }
    compare_with_homes(root, &homes, None, left, right)
}
