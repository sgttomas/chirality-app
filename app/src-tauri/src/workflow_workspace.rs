//! Immutable workflow package snapshots and source-qualified selection (WR/WD).
//! Registration consumes verified A15 evidence from the act owner; files alone are not an act.
use crate::util::sha256_hex;
use crate::workflow_declaration::{self, Declaration};
use serde::{Deserialize, Serialize};
use std::{collections::BTreeMap, fs, path::Path};

/// Reviewed CC-CONTENT-IDENTITY App-only package method; no host/global adoption.
pub const SNAPSHOT_METHOD: &str = "chirality.app.workflow-package.sha256/v1";
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct WorkflowIdentity {
    pub kind: String,
    pub origin: String,
    pub source_root: String,
    pub name: String,
    pub revision: String,
    pub revision_method: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub derived_from: Option<Box<WorkflowIdentity>>,
}
impl WorkflowIdentity {
    pub fn validate(&self) -> Result<(), String> {
        if self.kind != "workflow"
            || !["project", "user", "bundled", "host"].contains(&self.origin.as_str())
            || self.source_root.is_empty()
            || self.source_root.contains(['\n', '\r'])
            || !valid_name(&self.name)
            || self.revision.is_empty()
            || self.revision_method.is_empty()
        {
            return Err("workflow content identity not established".into());
        }
        if let Some(d) = &self.derived_from {
            d.validate()?
        }
        Ok(())
    }
    pub fn same_slot(&self, other: &Self) -> bool {
        self.origin == other.origin
            && self.source_root == other.source_root
            && self.name == other.name
    }
}
pub fn valid_name(n: &str) -> bool {
    !n.is_empty()
        && n.len() <= 64
        && n.split('-').all(|s| {
            !s.is_empty()
                && s.bytes()
                    .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit())
        })
}
#[derive(Debug, Clone)]
pub struct Snapshot {
    files: BTreeMap<String, Vec<u8>>,
    revision: String,
}
impl Snapshot {
    pub fn capture(root: &Path) -> Result<Self, String> {
        if fs::symlink_metadata(root)
            .map_err(|e| e.to_string())?
            .file_type()
            .is_symlink()
        {
            return Err("non-regular package root".into());
        }
        let mut files = BTreeMap::new();
        walk(root, root, &mut files)?;
        Self::from_files(files)
    }
    pub fn from_files(files: BTreeMap<String, Vec<u8>>) -> Result<Self, String> {
        for path in files.keys() {
            let p = Path::new(path);
            if p.is_absolute()
                || p.components()
                    .any(|c| !matches!(c, std::path::Component::Normal(_)))
                || path.is_empty()
            {
                return Err(format!("package relative path not established: {path}"));
            }
        }
        let wf = files.get("WORKFLOW.md").ok_or("HY-1: no WORKFLOW.md")?;
        std::str::from_utf8(wf).map_err(|_| "HY-7: WORKFLOW.md is not UTF-8")?;
        let mut preimage = Vec::new();
        preimage.extend_from_slice(SNAPSHOT_METHOD.as_bytes());
        preimage.push(0);
        preimage.extend_from_slice(&(files.len() as u64).to_be_bytes());
        for (path, bytes) in &files {
            preimage.extend_from_slice(&(path.len() as u64).to_be_bytes());
            preimage.extend_from_slice(path.as_bytes());
            preimage.extend_from_slice(&(bytes.len() as u64).to_be_bytes());
            preimage.extend_from_slice(bytes);
        }
        Ok(Self {
            files,
            revision: sha256_hex(&preimage),
        })
    }
    pub fn manifest(&self) -> Vec<serde_json::Value> {
        self.files.iter().map(|(path,bytes)|serde_json::json!({"path":path,"bytes":bytes.len(),"content":{"method":crate::role_supply::CONTENT_METHOD,"value":sha256_hex(bytes)}})).collect()
    }
    pub fn hygiene_findings(&self) -> Vec<String> {
        let mut findings = if self.files.len() > 1000
            || self.files.values().map(Vec::len).sum::<usize>() > 16 * 1024 * 1024
        {
            vec!["HY-5: package exceeds review bound (1000 files / 16 MiB)".into()]
        } else {
            vec![]
        };
        findings.extend(
            self.files
                .keys()
                .filter(|path| {
                    Path::new(path).components().any(|c| {
                        let s = c.as_os_str().to_string_lossy();
                        [
                            ".DS_Store",
                            "Thumbs.db",
                            "desktop.ini",
                            "Icon\r",
                            ".localized",
                            ".Spotlight-V100",
                            ".Trashes",
                            ".fseventsd",
                            "__MACOSX",
                        ]
                        .contains(&s.as_ref())
                            || s.starts_with("._")
                    })
                })
                .map(|path| format!("HY-4: operating-system entry {path}"))
                .collect::<Vec<String>>(),
        );
        findings
    }

    pub fn revision(&self) -> &str {
        &self.revision
    }
    pub fn files(&self) -> &BTreeMap<String, Vec<u8>> {
        &self.files
    }
    pub fn workflow_text(&self) -> &str {
        std::str::from_utf8(&self.files["WORKFLOW.md"]).expect("validated UTF-8")
    }
    pub fn declaration(&self) -> Result<Declaration, String> {
        workflow_declaration::read(self.workflow_text())
    }
    pub fn identity(
        &self,
        origin: &str,
        source_root: &str,
        name: &str,
        derived_from: Option<WorkflowIdentity>,
    ) -> Result<WorkflowIdentity, String> {
        let id = WorkflowIdentity {
            kind: "workflow".into(),
            origin: origin.into(),
            source_root: source_root.into(),
            name: name.into(),
            revision: self.revision.clone(),
            revision_method: SNAPSHOT_METHOD.into(),
            derived_from: derived_from.map(Box::new),
        };
        id.validate()?;
        Ok(id)
    }
    pub fn publish_new(&self, destination: &Path) -> Result<(), String> {
        // Exclusive new directory; callers own library lock, ledger, fsync and interruption recovery.
        fs::create_dir(destination).map_err(|e| e.to_string())?;
        for (p, b) in &self.files {
            let target = destination.join(p);
            if let Some(parent) = target.parent() {
                fs::create_dir_all(parent).map_err(|e| e.to_string())?;
            }
            let mut f = fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(target)
                .map_err(|e| e.to_string())?;
            use std::io::Write;
            f.write_all(b).map_err(|e| e.to_string())?;
            f.sync_all().map_err(|e| e.to_string())?;
        }
        Ok(())
    }
}
fn walk(base: &Path, dir: &Path, out: &mut BTreeMap<String, Vec<u8>>) -> Result<(), String> {
    for entry in fs::read_dir(dir).map_err(|e| e.to_string())? {
        let entry = entry.map_err(|e| e.to_string())?;
        let path = entry.path();
        let ty = fs::symlink_metadata(&path)
            .map_err(|e| e.to_string())?
            .file_type();
        if ty.is_dir() {
            walk(base, &path, out)?;
        } else if ty.is_file() {
            let rel = path
                .strip_prefix(base)
                .map_err(|e| e.to_string())?
                .to_str()
                .ok_or("package path not UTF-8")?
                .replace(std::path::MAIN_SEPARATOR, "/");
            out.insert(rel, fs::read(&path).map_err(|e| e.to_string())?);
        } else {
            return Err(format!("HY-3: non-regular entry {}", path.display()));
        }
    }
    Ok(())
}
#[derive(Debug, Clone, serde::Serialize)]
pub struct DraftKey {
    pub draft_location: String,
    pub draft_root: String,
    pub name: String,
}
#[derive(Debug, Clone)]
pub struct Review {
    snapshot: Snapshot,
    pub identity: WorkflowIdentity,
    pub prior: Option<WorkflowIdentity>,
    pub draft_key: String,
    pub draft: DraftKey,
    pub review_ref: String,
}
impl Review {
    pub fn open(
        snapshot: Snapshot,
        live: &Snapshot,
        list_revision: &str,
        identity: WorkflowIdentity,
        prior: Option<WorkflowIdentity>,
        draft: DraftKey,
        review_ref: String,
    ) -> Result<Self, String> {
        identity.validate()?;
        let hygiene = snapshot.hygiene_findings();
        if !hygiene.is_empty() {
            return Err(hygiene.join("; "));
        }
        if !["project", "user"].contains(&identity.origin.as_str()) {
            return Err("registration target must be project or user".into());
        }
        if snapshot.revision != live.revision
            || snapshot.revision != list_revision
            || identity.revision != snapshot.revision
            || identity.revision_method != SNAPSHOT_METHOD
        {
            return Err("DS-6: draft changed while read; review again".into());
        }
        let normalized = snapshot
            .workflow_text()
            .replace("\r\n", "\n")
            .replace('\r', "\n");
        let name = normalized
            .as_str()
            .strip_prefix("---\n")
            .and_then(|s| s.split_once("\n---"))
            .and_then(|(fm, _)| {
                fm.lines()
                    .find_map(|l| l.strip_prefix("name:").map(str::trim))
            });
        if name != Some(identity.name.as_str()) {
            return Err("HY-2: front-matter name differs from target".into());
        }
        if let Some(existing) = &prior {
            if !identity.same_slot(existing) {
                return Err("prior revision belongs to another slot".into());
            }
            if identity
                .derived_from
                .as_deref()
                .is_none_or(|base| !base.same_slot(existing))
            {
                return Err(
                    "DS-3: same-name draft without registered origin; choose a new name".into(),
                );
            }
            if identity.revision == existing.revision {
                return Err("DS-4: identical revision already registered".into());
            }
        }
        if !["project", "user"].contains(&draft.draft_location.as_str())
            || draft.draft_root.is_empty()
            || draft.name != identity.name
            || review_ref.is_empty()
        {
            return Err("review references required".into());
        }
        let draft_key = format!(
            "draft:{}:{}@{}",
            draft.draft_location, draft.name, snapshot.revision
        );
        Ok(Self {
            snapshot,
            identity,
            prior,
            draft_key,
            draft,
            review_ref,
        })
    }
    pub fn snapshot(&self) -> &Snapshot {
        &self.snapshot
    }
    pub fn is_current(&self, live: &Snapshot, latest: Option<&WorkflowIdentity>) -> bool {
        live.revision == self.snapshot.revision && latest == self.prior.as_ref()
    }
    pub fn descriptor(&self) -> serde_json::Value {
        let bound = serde_json::json!({"method":SNAPSHOT_METHOD,"value":self.snapshot.revision});
        serde_json::json!({"record_kind":"a15_descriptor","descriptor_id":format!("descriptor:{}",self.review_ref),"act_kind":"A15","wording":"register workflow revision","subject":self.identity,"bound_content":bound,"relations":{"reviewed_draft":{"draft":self.draft,"content":bound},"prior_revision":self.prior,"derived_from":self.identity.derived_from},"disposition":if self.prior.is_some(){"new revision"}else{"new workflow"},"scope":self.identity.source_root,"purpose":format!("make it available in the {} library",self.identity.origin),"review_ref":self.review_ref,"freshness":{"draft_content":bound,"slot_latest":self.prior.as_ref().map(|p|serde_json::json!({"method":p.revision_method,"value":p.revision}))}})
    }
}
/// Unverified adapter DTO. Field consistency is not an actual capture-owner
/// capability or evidence that A15 occurred; it can never grant selection.
pub struct RegistrationAdapterClaim {
    pub act_ref: String,
    pub subject: WorkflowIdentity,
    pub reviewed_draft: String,
    pub review_ref: String,
    pub prior: Option<WorkflowIdentity>,
}
#[derive(Debug, Clone)]
pub struct RegistrationClaimMatch {
    identity: WorkflowIdentity,
    snapshot: Snapshot,
    claimed_act_ref: String,
}
impl RegistrationClaimMatch {
    pub fn compare(
        review: &Review,
        live: &Snapshot,
        latest: Option<&WorkflowIdentity>,
        claim: RegistrationAdapterClaim,
    ) -> Result<Self, String> {
        if review.identity.revision != review.snapshot.revision
            || review.identity.revision_method != SNAPSHOT_METHOD
        {
            return Err("review identity no longer binds snapshot".into());
        }
        if !review.is_current(live, latest) {
            return Err("changed since review — review again".into());
        }
        if claim.act_ref.is_empty()
            || claim.subject != review.identity
            || claim.reviewed_draft != review.draft_key
            || claim.review_ref != review.review_ref
            || claim.prior != review.prior
        {
            return Err("adapter claim does not match reviewed content and prior slot".into());
        }
        Ok(Self {
            identity: review.identity.clone(),
            snapshot: review.snapshot.clone(),
            claimed_act_ref: claim.act_ref,
        })
    }
    pub fn identity(&self) -> &WorkflowIdentity {
        &self.identity
    }
    pub fn snapshot(&self) -> &Snapshot {
        &self.snapshot
    }
    pub fn claimed_act_ref(&self) -> &str {
        &self.claimed_act_ref
    }
    pub fn selection_eligible(&self) -> bool {
        false
    }
    pub fn evidence(&self) -> serde_json::Value {
        serde_json::json!({"identity":self.identity,"claimedActRef":self.claimed_act_ref,"registrationAuthority":"unverified adapter claim","selectionEligible":false})
    }
}
/// Authority-bearing revision has no DTO constructor. Actual capture-owner
/// capability construction is unavailable until that owner supplies its seam.
#[derive(Debug, Clone)]
pub struct RegisteredRevision {
    identity: WorkflowIdentity,
    snapshot: Snapshot,
    act_ref: String,
}
impl RegisteredRevision {
    pub fn identity(&self) -> &WorkflowIdentity {
        &self.identity
    }
    pub fn act_ref(&self) -> &str {
        &self.act_ref
    }
    pub fn select(&self) -> Selection {
        Selection {
            identity: self.identity.clone(),
            snapshot: self.snapshot.clone(),
        }
    }
}
#[derive(Debug, Clone)]
pub struct Selection {
    identity: WorkflowIdentity,
    snapshot: Snapshot,
}
impl Selection {
    /// Synthetic fixture admission only. Production shipping requires its owning
    /// closed release capability; caller fields/hashes do not establish it.
    #[cfg(test)]
    pub fn synthetic_shipped(
        snapshot: Snapshot,
        identity: WorkflowIdentity,
    ) -> Result<Self, String> {
        identity.validate()?;
        if identity.origin != "bundled"
            || identity.revision != snapshot.revision
            || identity.revision_method != SNAPSHOT_METHOD
        {
            return Err("shipped identity does not bind bytes".into());
        }
        Ok(Self { identity, snapshot })
    }
    pub fn identity(&self) -> &WorkflowIdentity {
        &self.identity
    }
    pub fn snapshot(&self) -> &Snapshot {
        &self.snapshot
    }
    pub fn verify_store(&self, path: &Path) -> Result<(), String> {
        let read = Snapshot::capture(path)
            .map_err(|e| format!("selected revision not resolvable: {e}"))?;
        if read.revision != self.identity.revision {
            return Err("revision not verified".into());
        }
        Ok(())
    }
    /// WR-FRAME-1. The person's brief travels in a second text element.
    pub fn run_start_text(&self, run: &str, folder_label: &str) -> Result<String, String> {
        if run.is_empty() || run.contains(['\n', '\r']) || folder_label.contains(['\n', '\r']) {
            return Err("run reference / folder label must be single line".into());
        }
        let id = &self.identity;
        let rev = &id.revision[..id.revision.len().min(12)];
        let start=format!("[Chirality] Workflow run start: {} from the {} library \"{}\", revision {}, run {}. Follow the workflow between the two markers below for this run, until the person ends the run.",id.name,id.origin,id.source_root.replace('"',"'"),rev,run);
        let proposal=format!("[Chirality] When you judge this workflow finished, end the message with a line of its own \"Workflow finished: {}:{}\". To propose that another registered workflow runs next, end the message with a line of its own \"Next workflow: <origin>:<name>\", where <origin> is project, user, bundled or host; when you write both, the finished line comes just before it. The person decides; nothing ends or starts until they confirm.",id.origin,id.name);
        let mut lines = vec![start, proposal];
        let others: Vec<_> = self
            .snapshot
            .files
            .iter()
            .filter(|(p, _)| p.as_str() != "WORKFLOW.md")
            .map(|(p, b)| format!("{p} (sha256 {})", &sha256_hex(b)[..12]))
            .collect();
        if !others.is_empty() {
            if folder_label.is_empty() || Path::new(folder_label).is_absolute() {
                return Err(
                    "project-relative or home-relative holding-folder label required".into(),
                );
            }
            lines.push(format!(
                "[Chirality] Other files of this revision, in the folder \"{}\": {}",
                folder_label,
                others.join("; ")
            ));
        }
        lines.push(format!(
            "<<<chirality-workflow {}@{} begin>>>",
            id.name, rev
        ));
        Ok(format!(
            "{}\n{}\n<<<chirality-workflow {}@{} end>>>",
            lines.join("\n"),
            self.snapshot.workflow_text(),
            id.name,
            rev
        ))
    }
    pub fn run_turn_params(
        &self,
        thread: &str,
        run: &str,
        folder_label: &str,
        person_text: &str,
        client_id: &str,
    ) -> Result<serde_json::Value, String> {
        if thread.is_empty() || client_id.is_empty() {
            return Err("thread and clientUserMessageId required".into());
        }
        let text = self.run_start_text(run, folder_label)?;
        let mut input = vec![serde_json::json!({"type":"text","text":text,"text_elements":[]})];
        if !person_text.is_empty() {
            input.push(serde_json::json!({"type":"text","text":person_text,"text_elements":[]}));
        }
        Ok(serde_json::json!({"threadId":thread,"clientUserMessageId":client_id,"input":input}))
    }
}
/// Collision inventory includes every origin; a selected tuple never follows discovery changes.
pub fn collisions<'a>(name: &str, entries: &'a [WorkflowIdentity]) -> Vec<&'a WorkflowIdentity> {
    entries.iter().filter(|e| e.name == name).collect()
}

#[derive(Debug, Clone, serde::Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum UntrustedPageComparisonState {
    EqualClaimedText,
    TextDiffersWorkflowBytesEqual,
    TextDiffersWorkflowBytesDiffer,
    NotFound,
    Unreadable,
}
#[derive(Debug, Clone, serde::Serialize)]
pub struct UntrustedPageComparison {
    pub state: UntrustedPageComparisonState,
    pub expected_text: serde_json::Value,
    pub observed_text: Option<serde_json::Value>,
    pub turn: String,
    pub item: Option<String>,
    pub located_by: Option<String>,
    pub adoption: String,
    pub evidence_limits: Vec<String>,
}
/// Compare untrusted purported pages as data only. This route cannot report
/// native verification/supply; actual supply requires the Core-owned capability.
pub fn compare_untrusted_pages(
    expected: &str,
    turn: &str,
    client_id: &str,
    mut read: impl FnMut(Option<&str>) -> Result<serde_json::Value, String>,
) -> UntrustedPageComparison {
    let cid = |text: &str| serde_json::json!({"method":crate::role_supply::CONTENT_METHOD,"value":sha256_hex(text.as_bytes())});
    let mut result = UntrustedPageComparison {
        state: UntrustedPageComparisonState::Unreadable,
        expected_text: cid(expected),
        observed_text: None,
        turn: turn.into(),
        item: None,
        located_by: None,
        adoption: "unknown".into(),
        evidence_limits:vec!["untrusted purported pages; byte comparison is not native verification, supplied guidance, active run, A15 or adoption".into()],
    };
    let mut cursor: Option<String> = None;
    let mut seen = std::collections::BTreeSet::new();
    let mut messages = vec![];
    loop {
        let Ok(page) = read(cursor.as_deref()) else {
            return result;
        };
        let Some(data) = page["data"].as_array() else {
            return result;
        };
        for entry in data {
            if entry["turnId"].as_str() != Some(turn) {
                continue;
            }
            let Some(item) = entry.get("item") else {
                return result;
            };
            if item["type"] == "userMessage" {
                messages.push(item.clone());
            }
        }
        match page.get("nextCursor") {
            None | Some(serde_json::Value::Null) => break,
            Some(serde_json::Value::String(c)) if !c.is_empty() && seen.insert(c.clone()) => {
                cursor = Some(c.clone())
            }
            _ => return result,
        }
    }
    let matched = messages.iter().find(|item| item["clientId"] == client_id);
    let selected = matched.or_else(|| messages.first());
    let Some(item) = selected else {
        result.state = UntrustedPageComparisonState::NotFound;
        return result;
    };
    result.item = item["id"].as_str().map(String::from);
    result.located_by = Some(
        if matched.is_some() {
            "client_user_message_id"
        } else {
            "first_user_message"
        }
        .into(),
    );
    let text = item["content"]
        .as_array()
        .and_then(|a| a.iter().find(|v| v["type"] == "text"))
        .and_then(|v| v["text"].as_str());
    if let Some(text) = text {
        result.observed_text = Some(cid(text));
        result.state = if text == expected {
            UntrustedPageComparisonState::EqualClaimedText
        } else {
            if expected_marker_body(expected, expected).is_some()
                && expected_marker_body(expected, expected) == expected_marker_body(expected, text)
            {
                UntrustedPageComparisonState::TextDiffersWorkflowBytesEqual
            } else {
                UntrustedPageComparisonState::TextDiffersWorkflowBytesDiffer
            }
        };
    } else {
        result.state = UntrustedPageComparisonState::NotFound;
    }
    result
}

fn expected_marker_body<'a>(expected: &str, observed: &'a str) -> Option<&'a str> {
    let begin = expected
        .lines()
        .find(|line| line.starts_with("<<<chirality-workflow ") && line.ends_with(" begin>>>"))?;
    let end = begin.strip_suffix(" begin>>>")?.to_owned() + " end>>>";
    let start = observed
        .match_indices(&(begin.to_owned() + "\n"))
        .find(|(i, _)| *i == 0 || observed.as_bytes().get(i - 1) == Some(&b'\n'))?
        .0
        + begin.len()
        + 1;
    let marker = "\n".to_owned() + &end;
    let finish = observed
        .match_indices(&marker)
        .filter(|(i, _)| {
            let after = i + marker.len();
            after == observed.len() || observed.as_bytes().get(after) == Some(&b'\n')
        })
        .last()?
        .0;
    observed.get(start..finish)
}

/// App-owned preparing scope. It does not establish an active native run or a
/// registration act; selection admission and actual callbacks belong to owners.
#[derive(Clone, Debug)]
pub struct RunScope {
    pub run: String,
    pub conversation: String,
    pub home: String,
    pub generation: serde_json::Value,
    pub source_root: String,
    pub holding_library: String,
    pub selection_ref: String,
    pub revision_store: std::path::PathBuf,
}
impl RunScope {
    fn validate(&self, selection: &Selection) -> Result<(), String> {
        if [
            &self.run,
            &self.conversation,
            &self.home,
            &self.source_root,
            &self.holding_library,
            &self.selection_ref,
        ]
        .iter()
        .any(|s| s.is_empty() || s.contains(['\n', '\r']))
            || self.generation.as_object().is_none_or(|o| o.len() != 3)
            || self.generation["home"] != self.home
            || self.generation["appSession"]
                .as_str()
                .is_none_or(str::is_empty)
            || self.generation["spawnCounter"].as_u64().unwrap_or(0) == 0
            || self.source_root != selection.identity.source_root
        {
            return Err("run/source/home/full-generation scope not established".into());
        }
        Ok(())
    }
}
#[derive(Clone, Debug)]
pub enum RunEndReason {
    ByPerson,
    Completed,
    ToStart(String),
}
impl RunEndReason {
    fn text(&self) -> Result<String, String> {
        match self {
            Self::ByPerson => Ok("ended by the person".into()),
            Self::Completed => Ok("completed".into()),
            Self::ToStart(name) if valid_name(name) => Ok(format!("ended to start {name}")),
            _ => Err("end successor name invalid".into()),
        }
    }
}
/// This is an owning EXEC/RECOVERY callback contract, not proof minted by a
/// serialized marker or the agent's completion sentence. No Deserialize path.
#[derive(Clone, Debug)]
pub struct OwnerRunEnd {
    pub home: String,
    pub conversation: String,
    pub run: String,
    pub workflow: WorkflowIdentity,
    pub reason: RunEndReason,
}
#[derive(Clone, Debug)]
pub struct PreparedRunText {
    scope: RunScope,
    workflow: WorkflowIdentity,
    text: String,
    record: serde_json::Value,
}
fn exact_text_identity(text: &str) -> serde_json::Value {
    crate::role_supply::content(text.as_bytes())
}
fn wr_validate(target: &str, value: &serde_json::Value) -> Result<(), String> {
    let wd: serde_json::Value =
        serde_json::from_str(crate::workflow_declaration::SCHEMA).map_err(|e| e.to_string())?;
    let wr: serde_json::Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/workspace-registration.schema.json"
    ))
    .map_err(|e| e.to_string())?;
    let mut registry = jsonschema::Registry::new();
    for schema in [wd, wr.clone()] {
        registry = registry
            .add(
                schema["$id"].as_str().ok_or("WR/WD ID absent")?,
                schema.clone(),
            )
            .map_err(|e| e.to_string())?;
    }
    let registry = registry.prepare().map_err(|e| e.to_string())?;
    let validator=jsonschema::options().with_registry(&registry).offline().build(&serde_json::json!({"$ref":format!("{}#/$defs/{target}",wr["$id"].as_str().ok_or("WR ID absent")?)})).map_err(|e|e.to_string())?;
    validator
        .validate(value)
        .map_err(|e| format!("WR {target} refused: {e}"))
}
impl PreparedRunText {
    pub fn start(
        selection: &Selection,
        scope: RunScope,
        folder_label: &str,
        prior: Option<&OwnerRunEnd>,
    ) -> Result<Self, String> {
        scope.validate(selection)?;
        selection.verify_store(&scope.revision_store)?;
        let mut text = selection.run_start_text(&scope.run, folder_label)?;
        let mut chain = serde_json::Value::Null;
        if let Some(prior) = prior {
            prior.workflow.validate()?;
            if prior.home != scope.home
                || prior.conversation != scope.conversation
                || prior.run.is_empty()
                || prior.run == scope.run
            {
                return Err("prior run end belongs to another scope".into());
            }
            let reason = prior.reason.text()?;
            let line=format!("[Chirality] Previous workflow run ended: {} revision {} (run {}, {}). Its instructions no longer apply.",prior.workflow.name,&prior.workflow.revision.chars().take(12).collect::<String>(),prior.run,reason);
            text = format!("{line}\n{text}");
            chain = serde_json::json!({"prior_run":prior.run,"prior_workflow":prior.workflow,"ended":reason});
        }
        let mut lines = serde_json::Map::new();
        for line in text
            .lines()
            .take_while(|s| !s.starts_with("<<<chirality-workflow "))
        {
            let key = if line.starts_with("[Chirality] Previous") {
                "chain_line"
            } else if line.starts_with("[Chirality] Workflow run start") {
                "start_line"
            } else if line.starts_with("[Chirality] When") {
                "proposal_line"
            } else {
                "files_line"
            };
            lines.insert(key.into(), line.into());
        }
        let revision = &selection.identity.revision[..selection.identity.revision.len().min(12)];
        lines.insert(
            "begin_marker".into(),
            format!(
                "<<<chirality-workflow {}@{} begin>>>",
                selection.identity.name, revision
            )
            .into(),
        );
        lines.insert(
            "end_marker".into(),
            format!(
                "<<<chirality-workflow {}@{} end>>>",
                selection.identity.name, revision
            )
            .into(),
        );
        let body = selection.snapshot.workflow_text();
        let mut record = serde_json::json!({"record_kind":"run_text","purpose":"run start","framing":"WR-FRAME-1","run":scope.run,"conversation":scope.conversation,"workflow":selection.identity,"holding_library":scope.holding_library,
            "workflow_file":{"path":"WORKFLOW.md","content":exact_text_identity(body),"bytes":body.len()},"chain":chain,"origin_of_start":"selected by the person","selection":scope.selection_ref,"lines":lines,"text_identity":exact_text_identity(&text),"text_bytes":text.len()});
        let other: Vec<_> = selection
            .snapshot
            .files
            .iter()
            .filter(|(p, _)| p.as_str() != "WORKFLOW.md")
            .map(|(path, b)| serde_json::json!({"path":path,"sha256":sha256_hex(b)}))
            .collect();
        if !other.is_empty() {
            record["other_files"] = serde_json::json!(other);
        }
        wr_validate("run_text", &record)?;
        Ok(Self {
            scope,
            workflow: selection.identity.clone(),
            text,
            record,
        })
    }
    pub fn text(&self) -> &str {
        &self.text
    }
    pub fn record(&self) -> &serde_json::Value {
        &self.record
    }
    pub fn scope(&self) -> &RunScope {
        &self.scope
    }
    pub fn turn_params(
        &self,
        person_text: &str,
        client_id: &str,
    ) -> Result<serde_json::Value, String> {
        if client_id.is_empty() {
            return Err("client message identity absent".into());
        }
        let mut input =
            vec![serde_json::json!({"type":"text","text":self.text,"text_elements":[]})];
        if !person_text.is_empty() {
            input.push(serde_json::json!({"type":"text","text":person_text,"text_elements":[]}));
        }
        Ok(
            serde_json::json!({"threadId":self.scope.conversation,"clientUserMessageId":client_id,"input":input}),
        )
    }
    pub fn end_notice(&self, end: &OwnerRunEnd) -> Result<(String, serde_json::Value), String> {
        if end.home != self.scope.home
            || end.conversation != self.scope.conversation
            || end.run != self.scope.run
            || end.workflow != self.workflow
        {
            return Err("end event does not identify this run".into());
        }
        let reason = end.reason.text()?;
        if matches!(&end.reason, RunEndReason::ToStart(_)) {
            return Err("successor start uses chain line, not end notice".into());
        }
        let text = format!(
            "[Chirality] Workflow run ended: {} revision {} (run {}, {}). No workflow is in force.",
            self.workflow.name,
            &self.workflow.revision[..self.workflow.revision.len().min(12)],
            self.scope.run,
            reason
        );
        let record = serde_json::json!({"record_kind":"run_text","purpose":"run end notice","framing":"WR-FRAME-1","run":self.scope.run,"conversation":self.scope.conversation,"lines":{"end_line":text},"text_identity":exact_text_identity(&text),"text_bytes":text.len()});
        wr_validate("run_text", &record)?;
        Ok((text, record))
    }
    /// TX3 locates this selected tuple's exact marker lines, not an arbitrary
    /// workflow-shaped pair from observed text. No source-byte normalization.
    fn selected_body<'a>(&self, observed: &'a str) -> Option<&'a str> {
        let revision = self.workflow.revision.chars().take(12).collect::<String>();
        let begin = format!(
            "<<<chirality-workflow {}@{} begin>>>\n",
            self.workflow.name, revision
        );
        let end = format!(
            "\n<<<chirality-workflow {}@{} end>>>",
            self.workflow.name, revision
        );
        let start = observed
            .match_indices(&begin)
            .find(|(i, _)| *i == 0 || observed.as_bytes().get(i - 1) == Some(&b'\n'))?
            .0
            + begin.len();
        let finish = observed
            .match_indices(&end)
            .filter(|(i, _)| {
                let after = i + end.len();
                after == observed.len() || observed.as_bytes().get(after) == Some(&b'\n')
            })
            .last()?
            .0;
        if finish < start {
            return None;
        }
        observed.get(start..finish)
    }
    /// Pure content comparison only. A supply_check record may be emitted only
    /// after the owning native accepted-page capability is available; arbitrary
    /// JSON/pages cannot mint that observation here.
    pub fn compare_observed_text(
        &self,
        expected_text: &serde_json::Value,
        expected_body: &serde_json::Value,
        observed: &str,
    ) -> Result<TextComparison, String> {
        wr_validate("text_identity", expected_text)?;
        wr_validate("text_identity", expected_body)?;
        let actual = exact_text_identity(observed);
        let mut limits=vec!["content comparison alone establishes no native supply, A15, active run or model adoption".into()];
        let state = if expected_text["method"] != actual["method"] {
            limits.push("text identity methods incomparable".into());
            "incomparable"
        } else if expected_text == &actual {
            "equal composed text"
        } else if let Some(body) = self.selected_body(observed) {
            if expected_body["method"] != crate::role_supply::CONTENT_METHOD {
                limits.push("body identity methods incomparable; no value-only fallback".into());
                "incomparable"
            } else if expected_body == &exact_text_identity(body) {
                "text differs, workflow bytes equal"
            } else {
                "text differs, workflow bytes differ"
            }
        } else {
            "text differs, workflow bytes differ"
        };
        Ok(TextComparison {
            state: state.into(),
            observed_text: actual,
            evidence_limits: limits,
        })
    }
}
#[derive(Clone, Debug, serde::Serialize)]
pub struct TextComparison {
    pub state: String,
    pub observed_text: serde_json::Value,
    pub evidence_limits: Vec<String>,
}
