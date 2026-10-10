//! Workflow trials in the Rust host (WR §4.2 TT-3, TT-4, TT-8, TT-9; §5.5),
//! under the owner's OI-008 ruling for the draft workspace.
//!
//! - `LibraryOwner::prepare_trial`: the trial snapshot (TT-8, a content-
//!   addressed copy under `.chirality/workflow-trials/`) and the trial text
//!   (TT-3, `TrialText`). Nothing is recorded: a trial that is never sent
//!   leaves only the snapshot folder (§5.5 *pre-filled*).
//! - `TrialLinks`: the App-kept trial links (`trial_pointer` with `trial`,
//!   create-once, one per trial, written when the host acknowledges the send)
//!   and their later `trial_observation` records, beside the earlier attachment
//!   trial pointers in `runtime/wr/trial-pointers/`.
//!
//! A trial is never a workflow run, registration, checking or acceptance
//! (TT-2): nothing here opens a run, writes a `run_text` or `supply_check`, or
//! names a workflow identity in a record.
use super::{prescan, read_folder, LibraryOwner, DRAFTS, TRIAL_POINTERS};
use crate::storage;
use crate::workflow_workspace::package_copy::{self, ContentCopy, CopyStanding};
use crate::workflow_workspace::{
    relative_folder_label, valid_name, valid_trial_reference, FidelityReading, Snapshot, TrialText,
    SNAPSHOT_METHOD, TRIAL_AREA,
};
use serde_json::{json, Value};
use std::{
    fs,
    path::{Path, PathBuf},
};

/// TT-4's fixed standing sentence for a CC-WR-TRIALS trial link.
pub(crate) const LINK_STANDING: &str =
    "trial of a draft; not a run of any workflow identity; not registration, checking or acceptance";
/// The fixed standing sentence of a `trial_observation`.
pub(crate) const OBSERVATION_STANDING: &str =
    "observation of a trial; not a run record, registration, checking or acceptance";

/// A trial ready to pre-fill: its text and the draft version it tries. The
/// snapshot folder exists; nothing else was written.
#[derive(Debug, Clone)]
pub(crate) struct PreparedTrial {
    pub text: TrialText,
    /// The WR `draft_key` of the draft.
    pub key: Value,
    /// The draft content identity {method, value}.
    pub content: Value,
    /// The trial snapshot folder (TT-8) and whether this call wrote it.
    pub snapshot: ContentCopy,
}

impl LibraryOwner {
    /// TT-8 then TT-3 for draft `name` as listed with content identity
    /// `listed`: hygiene and HY-2 as at listing; the folder named in the files
    /// line must be project- or `~`-relative; the trial text is composed; the
    /// draft's regular files are copied (no-follow) into the content-addressed
    /// snapshot folder, which is recomputed; and the live draft is recomputed
    /// after copying. Any difference from `listed` reads "the draft changed
    /// while it was read; try again". `sequence` is the draft's next trial
    /// number (`TrialLinks::next_sequence`).
    pub(crate) fn prepare_trial(
        &self,
        name: &str,
        listed: &str,
        sequence: u64,
        project: Option<&Path>,
        home: Option<&Path>,
    ) -> Result<PreparedTrial, String> {
        if !valid_name(name) {
            return Err(format!("cannot be tried: {name:?} is not a draft name of this library"));
        }
        let path = self.root.join(DRAFTS).join(name);
        storage::check_path(&path).map_err(|e| format!("cannot be tried: {e}"))?;
        match fs::symlink_metadata(&path) {
            Ok(m) if m.file_type().is_dir() => {}
            Ok(_) => return Err(format!("cannot be tried: {name} is not a draft folder")),
            Err(e) => return Err(format!("cannot be tried: draft {name} not found ({e})")),
        }
        let reading = read_folder(name, &path);
        let snapshot = reading
            .content
            .map_err(|cause| format!("cannot be tried: content identity not established ({cause})"))?;
        if !reading.findings.is_empty() {
            return Err(format!("cannot be tried: {}", reading.findings.join("; ")));
        }
        if snapshot.revision() != listed {
            return Err(CHANGED_WHILE_READ.into());
        }
        let dest = package_copy::content_folder(&self.root, TRIAL_AREA, name, snapshot.revision());
        let (label, _) = relative_folder_label(&dest, project, home).ok_or_else(|| {
            format!(
                "cannot be tried: the trial snapshot folder {} is inside neither the opened project nor the home folder, so the trial's agent could not be told where its files are",
                dest.display()
            )
        })?;
        let reference = crate::util::opaque_id("trial:")?;
        let text = TrialText::compose(&self.origin, &self.source_root, name, &snapshot, sequence, &reference, &label)?;
        let copy = package_copy::write_content_copy(&snapshot, &dest)
            .map_err(|e| format!("cannot be tried: trial snapshot not written: {e}"))?;
        prescan(&path).map_err(|_| CHANGED_WHILE_READ.to_string())?;
        let live = Snapshot::capture(&path).map_err(|_| CHANGED_WHILE_READ.to_string())?;
        if live.revision() != listed {
            return Err(CHANGED_WHILE_READ.into());
        }
        Ok(PreparedTrial {
            text,
            key: self.draft_key(name),
            content: json!({"method":SNAPSHOT_METHOD,"value":snapshot.revision()}),
            snapshot: copy,
        })
    }
    /// TT-8 for Compare and Bring back: whether a trial's snapshot folder
    /// still holds the version it is named for.
    pub(crate) fn trial_snapshot_standing(&self, name: &str, revision: &str) -> CopyStanding {
        if !valid_name(name) {
            return CopyStanding::NotAvailable("not a draft name".into());
        }
        package_copy::copy_standing(&package_copy::content_folder(&self.root, TRIAL_AREA, name, revision), revision)
    }
}
const CHANGED_WHILE_READ: &str = "the draft changed while it was read; try again";

/// Which kind of trial was sent (TT-3a, TT-3b).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum TrialKind {
    Delegated,
    Clean,
}
impl TrialKind {
    fn text(self) -> &'static str {
        match self {
            Self::Delegated => "delegated",
            Self::Clean => "clean",
        }
    }
}
/// What the host acknowledged when the trial message was sent (TT-4).
#[derive(Debug, Clone)]
pub(crate) struct SentTrial {
    pub kind: TrialKind,
    pub authoring_conversation: String,
    pub client_message: String,
    /// The turn the acknowledgment named, when it named one.
    pub turn: Option<String>,
    /// The fresh conversation of a clean trial; None for a delegated one.
    pub clean_conversation: Option<String>,
}
/// A later fact about a trial (TT-4, TT-9, TT-10).
#[derive(Debug, Clone)]
pub(crate) enum TrialObservation {
    SubAgentLinked { child_thread: String, by_person: bool },
    SubAgentUnlinked { child_thread: String },
    Fidelity { read_thread: Option<String>, reading: FidelityReading, limits: Vec<String> },
    BroughtBack { target_conversation: String, transcript: String, shortenings: Vec<String> },
}

/// The trial links and observations kept in the App data folder, read at
/// open. Each record is its own create-once file: a link is named by its trial
/// reference (`trial-<uuid>.json`), an observation by its identity
/// (`observation-<uuid>.json`), and earlier attachment pointers keep their
/// names. Writes are atomic (temporary file, sync, exclusive link, directory
/// sync); a file that cannot be read back, does not conform, or breaks a
/// reader check is reported in `limits`, never dropped silently or rewritten.
#[derive(Default)]
pub(crate) struct TrialLinks {
    dir: Option<PathBuf>,
    /// Set when an App data folder is attached but its trial folder is
    /// refused (for example a link in its path): writes are then refused with
    /// this cause, never kept in memory as if no folder were attached.
    refused: Option<String>,
    /// trial_pointer records: earlier attachment pointers and trial links.
    pointers: Vec<Value>,
    observations: Vec<Value>,
    limits: Vec<String>,
}
impl TrialLinks {
    /// Reads every record already kept under `app_data`.
    pub(crate) fn open(app_data: &Path) -> Self {
        let dir = app_data.join(TRIAL_POINTERS);
        let mut store = Self { dir: Some(dir.clone()), ..Self::default() };
        if let Err(cause) = storage::check_path(&dir) {
            store.limits.push(format!("trial pointers not readable: {cause}"));
            store.dir = None;
            store.refused = Some(cause);
            return store;
        }
        let entries = match fs::read_dir(&dir) {
            Ok(entries) => entries,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return store,
            Err(e) => {
                store.limits.push(format!("trial pointers unreadable: {}: {e}", dir.display()));
                return store;
            }
        };
        let mut files: Vec<PathBuf> = vec![];
        for entry in entries {
            match entry {
                Ok(entry) => files.push(entry.path()),
                Err(e) => store.limits.push(format!("trial pointers listing incomplete: {}: {e}", dir.display())),
            }
        }
        // Hidden entries are staging files of an interrupted write: never
        // records, but reported (left as they are). Any other entry that is
        // not a `.json` file is reported too, never dropped silently.
        let mut records: Vec<PathBuf> = vec![];
        for p in files {
            let name = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
            if name.starts_with('.') {
                store.limits.push(format!(
                    "trial pointers: staging file left by an interrupted write, not a record (left as it is): {}",
                    p.display()
                ));
            } else if p.extension().is_some_and(|x| x == "json") {
                records.push(p);
            } else {
                store.limits.push(format!("trial pointers: not a record (not a .json file), not listed: {}", p.display()));
            }
        }
        let mut files = records;
        files.sort();
        for file in files {
            let shown = file.display().to_string();
            let read = crate::workflow_workspace::read_regular_file(&file)
                .map_err(|e| format!("trial pointer unreadable: {shown}: {e}"))
                .and_then(|bytes| {
                    serde_json::from_slice::<Value>(&bytes).map_err(|e| format!("trial pointer malformed: {shown}: {e}"))
                });
            let value = match read {
                Ok(value) => value,
                Err(limit) => {
                    store.limits.push(limit);
                    continue;
                }
            };
            let stem = file.file_stem().and_then(|s| s.to_str()).unwrap_or_default().to_owned();
            match value["record_kind"].as_str() {
                Some("trial_pointer") => match check_pointer(&value, &stem) {
                    Ok(()) => {
                        let reference = &value["trial"]["reference"];
                        if !reference.is_null() && store.pointers.iter().any(|p| &p["trial"]["reference"] == reference) {
                            store.limits.push(format!("trial pointer malformed: {shown}: a second link for trial {reference}; not listed"));
                        } else {
                            store.pointers.push(value);
                        }
                    }
                    Err(e) => store.limits.push(format!("trial pointer malformed: {shown}: {e}")),
                },
                Some("trial_observation") => match check_observation(&value, &stem) {
                    Ok(()) => store.observations.push(value),
                    Err(e) => store.limits.push(format!("trial observation malformed: {shown}: {e}")),
                },
                _ => store.limits.push(format!("trial pointer malformed: {shown}: not a trial_pointer or trial_observation record")),
            }
        }
        // Reader check: an observation cites an existing trial link.
        let (known, orphans): (Vec<Value>, Vec<Value>) = std::mem::take(&mut store.observations)
            .into_iter()
            .partition(|o| store.pointers.iter().any(|p| p["trial"]["reference"] == o["trial"]));
        store.observations = known;
        for o in orphans {
            store.limits.push(format!(
                "trial observation {} cites trial {}, which has no trial link here; not listed",
                o["observation_id"], o["trial"]
            ));
        }
        // Links of one draft in the same millisecond keep their trial order.
        store.pointers.sort_by(|a, b| {
            (a["time"].as_str(), a["trial"]["sequence"].as_u64().unwrap_or(0))
                .cmp(&(b["time"].as_str(), b["trial"]["sequence"].as_u64().unwrap_or(0)))
        });
        store.observations.sort_by(|a, b| a["time"].as_str().cmp(&b["time"].as_str()));
        store
    }

    /// TT-4: the trial link, written once when the host acknowledged the send
    /// of `prepared`'s trial message. One link per trial reference: a second
    /// call for the same trial returns the existing link when it records the
    /// same send, and is refused otherwise.
    pub(crate) fn record_sent(&mut self, prepared: &PreparedTrial, sent: &SentTrial) -> Result<Value, String> {
        let text = &prepared.text;
        let conversation = match (sent.kind, &sent.clean_conversation) {
            (TrialKind::Delegated, None) => sent.authoring_conversation.clone(),
            (TrialKind::Clean, Some(clean)) => clean.clone(),
            _ => return Err("a clean trial names its fresh conversation and a delegated trial none".into()),
        };
        let trial = json!({"reference":text.reference(),"sequence":text.sequence(),"kind":sent.kind.text(),
            "text_identity":text.identity(),"text_bytes":text.bytes(),"snapshot_folder":text.snapshot_folder(),
            "authoring_conversation":sent.authoring_conversation,"client_message":sent.client_message,
            "turn":sent.turn,"clean_conversation":sent.clean_conversation});
        if let Some(existing) = self.link(text.reference()) {
            if existing["trial"] == trial && existing["draft"] == prepared.key && existing["content"] == prepared.content {
                return Ok(existing.clone());
            }
            return Err(format!("trial {} already has its link; one link per trial", text.reference()));
        }
        let link = json!({"record_kind":"trial_pointer","draft":prepared.key,"content":prepared.content,
            "conversation":conversation,"time":crate::util::now_rfc3339(),"standing":LINK_STANDING,"trial":trial});
        crate::workflow_workspace::wr_validate("trial_pointer", &link)?;
        check_pointer(&link, &link_stem(text.reference()))?;
        self.keep(&format!("{}.json", link_stem(text.reference())), &link)?;
        self.pointers.push(link.clone());
        Ok(link)
    }

    /// A later fact about trial `reference`, in its own create-once record.
    pub(crate) fn record_observation(&mut self, reference: &str, observation: TrialObservation) -> Result<Value, String> {
        if self.link(reference).is_none() {
            return Err(format!("no trial link for {reference}; nothing recorded"));
        }
        let id = crate::util::opaque_id("trial-observation:")?;
        let mut record = json!({"record_kind":"trial_observation","observation_id":id,"trial":reference,
            "time":self.later_time(reference),"standing":OBSERVATION_STANDING});
        match observation {
            TrialObservation::SubAgentLinked { child_thread, by_person } => {
                record["observation"] = json!("sub-agent linked");
                record["child_thread"] = json!(child_thread);
                record["linked_by"] = json!(if by_person { "by the person" } else { "begin marker found" });
            }
            TrialObservation::SubAgentUnlinked { child_thread } => {
                record["observation"] = json!("sub-agent unlinked");
                record["child_thread"] = json!(child_thread);
            }
            TrialObservation::Fidelity { read_thread, reading, limits } => {
                record["observation"] = json!("fidelity");
                record["fidelity"] = reading.record(read_thread.as_deref(), limits);
            }
            TrialObservation::BroughtBack { target_conversation, transcript, shortenings } => {
                record["observation"] = json!("brought back");
                record["target_conversation"] = json!(target_conversation);
                record["transcript"] = json!({"identity":crate::role_supply::content(transcript.as_bytes()),
                    "bytes":transcript.len(),"shortenings":shortenings});
            }
        }
        crate::workflow_workspace::wr_validate("trial_observation", &record)?;
        self.keep(&format!("{}.json", observation_stem(&id)), &record)?;
        self.observations.push(record.clone());
        Ok(record)
    }

    /// The observation time: the clock, read again (for at most about 50 ms)
    /// until it is later than this trial's latest observation, so that the
    /// observations of one trial are totally ordered by `time` after a relaunch
    /// ("the latest link or unlink stands"). A clock set back further than
    /// that gives the reading as it is.
    fn later_time(&self, reference: &str) -> String {
        let latest = self
            .observations
            .iter()
            .filter(|o| o["trial"] == reference)
            .filter_map(|o| o["time"].as_str())
            .max()
            .map(str::to_owned);
        later_than(latest.as_deref(), crate::util::now_rfc3339, || {
            std::thread::sleep(std::time::Duration::from_millis(1))
        })
    }

    /// One create-once file; an uncertain outcome is settled by reading the
    /// file back (equal bytes: written; absent: not written; other bytes:
    /// refused, nothing overwritten).
    fn keep(&mut self, file: &str, value: &Value) -> Result<(), String> {
        if let Some(cause) = &self.refused {
            return Err(format!("trial record not written: the App data trial folder is refused ({cause})"));
        }
        let Some(dir) = &self.dir else {
            self.limits
                .push("trial record held in process memory only: App data folder not attached (WR §3)".into());
            return Ok(());
        };
        let path = dir.join(file);
        match storage::create_json(&path, value) {
            Ok(()) => Ok(()),
            Err(error) => match crate::workflow_workspace::read_regular_file(&path)
                .ok()
                .and_then(|b| serde_json::from_slice::<Value>(&b).ok())
            {
                Some(found) if &found == value => Ok(()),
                Some(_) => Err(format!("{}: another record already has this name; nothing overwritten ({error})", path.display())),
                None => Err(format!("trial record not written: {error}")),
            },
        }
    }

    /// Every CC-WR-TRIALS trial link (earlier attachment pointers excluded), oldest first.
    pub(crate) fn all_links(&self) -> Vec<Value> {
        self.pointers.iter().filter(|p| p.get("trial").is_some()).cloned().collect()
    }
    /// The trial link of `reference`, if this store holds it.
    pub(crate) fn link(&self, reference: &str) -> Option<&Value> {
        self.pointers.iter().find(|p| p["trial"]["reference"] == reference)
    }
    /// The draft's next trial number (display only; TT-3 ‹n›).
    pub(crate) fn next_sequence(&self, key: &Value) -> u64 {
        1 + self
            .pointers
            .iter()
            .filter(|p| &p["draft"] == key)
            .filter_map(|p| p["trial"]["sequence"].as_u64())
            .max()
            .unwrap_or(0)
    }
    /// Every trial_pointer record of one draft key, oldest first.
    pub(crate) fn for_draft(&self, key: &Value) -> Vec<Value> {
        self.pointers.iter().filter(|p| &p["draft"] == key).cloned().collect()
    }
    /// The observations of one trial, oldest first.
    pub(crate) fn observations(&self, reference: &str) -> Vec<Value> {
        self.observations.iter().filter(|o| o["trial"] == reference).cloned().collect()
    }
    /// TT-4's listing of one draft's trials, newest first: kind (an earlier
    /// pointer is "earlier attachment trial"), content identity marked current
    /// or earlier against `current` (the draft's listed content value), the
    /// conversations, the latest sub-agent link, the latest fidelity reading,
    /// and every bring-back. Display only.
    pub(crate) fn trials_for_draft(&self, key: &Value, current: Option<&str>) -> Vec<Value> {
        let mut rows: Vec<Value> = self
            .for_draft(key)
            .into_iter()
            .map(|p| {
                let version = if current.is_some_and(|c| p["content"]["value"] == c) { "current" } else { "earlier" };
                let Some(trial) = p.get("trial") else {
                    return json!({"kind":"earlier attachment trial","content":p["content"],"version":version,
                        "conversation":p["conversation"],"time":p["time"],"link":p});
                };
                let reference = trial["reference"].as_str().unwrap_or_default();
                let observed = self.observations(reference);
                let latest = |kinds: &[&str]| observed.iter().rev().find(|o| o["observation"].as_str().is_some_and(|k| kinds.contains(&k))).cloned();
                let sub_agent = match latest(&["sub-agent linked", "sub-agent unlinked"]) {
                    Some(o) if o["observation"] == "sub-agent linked" => json!({"state":"linked","thread":o["child_thread"],"linkedBy":o["linked_by"]}),
                    Some(o) => json!({"state":"sub-agent not linked","unlinked":o["child_thread"]}),
                    None if trial["kind"] == "delegated" => json!({"state":"sub-agent not linked"}),
                    None => Value::Null,
                };
                json!({"reference":reference,"sequence":trial["sequence"],"kind":trial["kind"],
                    "content":p["content"],"version":version,
                    "authoringConversation":trial["authoring_conversation"],"trialConversation":trial["clean_conversation"],
                    "subAgent":sub_agent,
                    "fidelity":latest(&["fidelity"]).map(|o|o["fidelity"].clone()).unwrap_or(json!({"state":"not checked","limits":["no fidelity reading yet"]})),
                    "broughtBack":observed.iter().filter(|o|o["observation"]=="brought back").map(|o|json!({"time":o["time"],"to":o["target_conversation"]})).collect::<Vec<_>>(),
                    "time":p["time"],"link":p,"standing":LINK_STANDING})
            })
            .collect();
        rows.reverse();
        rows
    }
    pub(crate) fn limits(&self) -> &[String] {
        &self.limits
    }
}
/// The first clock reading later than `latest`, reading again (with `wait`
/// between readings) at most 50 times; after that the last reading as it is.
fn later_than(latest: Option<&str>, mut now: impl FnMut() -> String, mut wait: impl FnMut()) -> String {
    let mut reading = now();
    for _ in 0..50 {
        if latest.is_none_or(|l| reading.as_str() > l) {
            break;
        }
        wait();
        reading = now();
    }
    reading
}
fn link_stem(reference: &str) -> String {
    format!("trial-{}", reference.trim_start_matches("trial:"))
}
fn observation_stem(id: &str) -> String {
    format!("observation-{}", id.trim_start_matches("trial-observation:"))
}
/// WR §8 reader checks for a trial_pointer, beyond the schema.
fn check_pointer(value: &Value, stem: &str) -> Result<(), String> {
    crate::workflow_workspace::wr_validate("trial_pointer", value)?;
    let Some(trial) = value.get("trial") else {
        return Ok(()); // an earlier attachment pointer
    };
    let reference = trial["reference"].as_str().unwrap_or_default();
    if !valid_trial_reference(reference) || stem != link_stem(reference) {
        return Err(format!("file name does not name trial {reference}"));
    }
    let expected = match trial["kind"].as_str() {
        Some("delegated") => &trial["authoring_conversation"],
        _ => &trial["clean_conversation"],
    };
    if &value["conversation"] != expected {
        return Err("conversation is not the trial's (delegated: authoring; clean: the fresh conversation)".into());
    }
    Ok(())
}
fn check_observation(value: &Value, stem: &str) -> Result<(), String> {
    crate::workflow_workspace::wr_validate("trial_observation", value)?;
    let id = value["observation_id"].as_str().unwrap_or_default();
    if stem != observation_stem(id) {
        return Err(format!("file name does not name observation {id}"));
    }
    Ok(())
}

#[cfg(test)]
#[path = "workflow_trials_tests.rs"]
mod tests;
