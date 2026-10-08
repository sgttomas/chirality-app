//! CSP-v0.1 transient evidence only: no route source/account, fact, duty or supply.
use crate::{
    attachments::native_path_identity,
    connector_source_fs::Root,
    util::{now_rfc3339, opaque_id, sha256_hex},
};
use serde::Deserialize;
use serde_json::{json, Value};
use std::{
    collections::HashMap,
    path::{Path, PathBuf},
    sync::{Arc, Mutex},
};
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Question {
    pub id: String,
    pub text: String,
    pub asked_revision: String,
    pub since_revision: Option<String>,
}
impl Question {
    fn view(&self) -> Value {
        json!({"id":self.id,"text":self.text,"askedRevision":self.asked_revision,"sinceRevision":self.since_revision,"revisionStanding":"caller request, not observed source revision"})
    }
}
struct Observation {
    selection_mechanism: &'static str,
    selected_path: PathBuf,
    reference: String,
    question: Question,
    bytes: Vec<u8>,
    view: Value,
    anchors: HashMap<String, Value>,
    revision: Value,
}
struct Prepared {
    token: String,
    generation: String,
    root: Arc<Root>,
    question: Question,
    trigger: String,
    responsible: Option<String>,
    operation: String,
    read_gap: Option<String>,
    excerpt_gap: Option<String>,
    observation: Option<Observation>,
    #[cfg(unix)]
    git: GitState,
}
#[derive(Default)]
pub struct Session {
    active: Option<Prepared>,
}
impl Session {
    pub fn prepare(
        &mut self,
        path: &Path,
        question: Question,
        trigger: String,
        responsible: Option<String>,
    ) -> Result<Value, String> {
        if question.id.trim().is_empty()
            || question.text.trim().is_empty()
            || question.asked_revision.trim().is_empty()
        {
            return Err("Question identity, text and requested revision are required".into());
        }
        if !matches!(trigger.as_str(), "absent" | "stale" | "partial" | "failing") {
            return Err("Choose a constructed absent/stale/partial/failing trigger".into());
        }
        // Invalidate old capabilities before attempting a newly requested basis.
        self.active = None;
        let root = Arc::new(Root::open(path)?);
        self.active = Some(Prepared {
            token: opaque_id("source-session-")?,
            generation: opaque_id("source-generation-")?,
            root,
            question,
            trigger,
            responsible: responsible.filter(|s| !s.trim().is_empty()),
            operation: "prepared".into(),
            read_gap: None,
            excerpt_gap: None,
            observation: None,
            #[cfg(unix)]
            git: GitState::default(),
        });
        Ok(self.snapshot())
    }
    fn current(&mut self, token: &str, generation: &str) -> Result<&mut Prepared, String> {
        self.active
            .as_mut()
            .filter(|a| a.token == token && a.generation == generation)
            .ok_or_else(|| {
                "Unknown or stale source session/generation; no capability recreated".into()
            })
    }
    pub fn snapshot(&self) -> Value {
        let Some(a) = &self.active else {
            return json!({"state":"unprepared"});
        };
        let mut gaps = vec![
            json!({"kind":"Revision","reason":"Local snapshot alone establishes no verified source revision; inspect separate Git result if requested","effect":"No source entry, account or revision-qualified reconstruction can be emitted","responsible":a.responsible,"assignmentStanding":"caller-assigned route; null means unassigned"}),
        ];
        if let Some(reason) = &a.read_gap {
            gaps.push(json!({"kind":"Selection/read","reason":reason,"effect":"No new source observation was produced; a retained prior buffer does not resolve this read failure","responsible":a.responsible,"assignmentStanding":"caller-assigned route; null means unassigned"}));
        }
        if let Some(reason) = &a.excerpt_gap {
            gaps.push(json!({"kind":"Excerpt","reason":reason,"effect":"This excerpt request produced no anchor; independent supported work is not blocked","responsible":a.responsible,"assignmentStanding":"caller-assigned route; null means unassigned"}));
        }
        let mut snapshot = json!({"state":"prepared","sessionToken":a.token,"generation":a.generation,"question":a.question.view(),"trigger":{"kind":a.trigger,"standing":"constructed caller context, no connector observation"},"operation":a.operation,"gaps":gaps,
        "observation":a.observation.as_ref().map(|o|json!({"reference":o.reference,"question":o.question.view(),"read":o.view,"revision":o.revision,"anchors":o.anchors.values().collect::<Vec<_>>(),"historical":a.operation!="observed"})),
        "limits":["Session memory only; process loss loses capabilities and previews","Opened capabilities are not continuous pathname containment; concurrent renames/transient writes may evade checks","Hash describes the buffer read, not a coherent historical revision or authoritative statements","No source/account/fact/conclusion/duty/save/send production; Git observations remain separate from local bytes"],
        "dutiesStanding":"Locate/compare, manager review/integration and necessary person coordination are unperformed/outstanding in this producer; no not-required or performed duty is authored"});
        #[cfg(unix)]
        {
            snapshot["git"] = a.git.view();
        }
        #[cfg(not(unix))]
        {
            snapshot["git"] = json!({"operation":"unsupported","error":"Git capability unavailable on this platform"});
        }
        snapshot
    }
    pub fn anchor(
        &mut self,
        token: &str,
        generation: &str,
        reference: &str,
        start: usize,
        end: usize,
        expected: Option<&str>,
    ) -> Result<Value, String> {
        let a = self.current(token, generation)?;
        let o = a
            .observation
            .as_mut()
            .filter(|o| o.reference == reference)
            .ok_or("Unknown observation; paths and exported DTOs cannot restore custody")?;
        let result = excerpt(&o.bytes, start, end, expected);
        match result {
            Ok(mut anchor) => {
                let id = opaque_id("source-anchor-")?;
                anchor["reference"] = json!(id);
                anchor["observationReference"] = json!(o.reference);
                o.anchors.insert(id, anchor);
                a.excerpt_gap = None;
            }
            Err(reason) => {
                a.excerpt_gap = Some(reason);
            }
        }
        Ok(self.snapshot())
    }
    pub fn revision(
        &mut self,
        token: &str,
        generation: &str,
        reference: &str,
        kind: &str,
        label: &str,
        anchor: Option<&str>,
    ) -> Result<Value, String> {
        let a = self.current(token, generation)?;
        let o = a
            .observation
            .as_mut()
            .filter(|o| o.reference == reference)
            .ok_or("Unknown observation")?;
        o.revision=match kind {
            "unavailable"=>json!({"kind":"unavailable","limit":"No revision evidence supplied"}),
            "caller_assertion" if !label.trim().is_empty()=>json!({"kind":kind,"label":label,"limit":"Caller assertion only; not observed metadata or Git evidence"}),
            "source_text_located" if !label.trim().is_empty()=>{let anchor=o.anchors.get(anchor.ok_or("Choose a host-checked excerpt")?).ok_or("Unknown anchor")?;json!({"kind":kind,"callerInterpretation":label,"anchor":anchor,"limit":"Exact byte inclusion only; meaning, truth, authority and Git provenance are unverified"})},
            _=>return Err("Unsupported revision treatment; Git verification and typed evidence are not available".into()),
        };
        Ok(self.snapshot())
    }
}
/// Only production native picker or explicitly synthetic test callback supplies paths.
pub fn select(
    state: &Mutex<Session>,
    token: &str,
    generation: &str,
    pick: impl FnOnce() -> Result<Option<PathBuf>, String>,
) -> Result<Value, String> {
    select_mechanism(state, token, generation, pick, "synthetic_test_callback")
}
pub fn select_native(
    state: &Mutex<Session>,
    token: &str,
    generation: &str,
    pick: impl FnOnce() -> Result<Option<PathBuf>, String>,
) -> Result<Value, String> {
    select_mechanism(state, token, generation, pick, "native_picker_callback")
}
fn select_mechanism(
    state: &Mutex<Session>,
    token: &str,
    generation: &str,
    pick: impl FnOnce() -> Result<Option<PathBuf>, String>,
    mechanism: &'static str,
) -> Result<Value, String> {
    let root = {
        let mut state = state.lock().map_err(|_| "Source session unavailable")?;
        let a = state.current(token, generation)?;
        if a.operation == "selecting" {
            return Err("Source selection already pending".into());
        }
        #[cfg(unix)]
        a.git
            .invalidate("Local source selection changed; Git results are historical");
        if let Err(error) = a.root.verify() {
            a.operation = "failed".into();
            a.read_gap = Some(error);
            return Ok(state.snapshot());
        }
        a.operation = "selecting".into();
        // Pending or cancelled selection does not resolve a prior read failure.
        a.root.clone()
    };
    let selected = pick();
    let outcome = match selected {
        Ok(Some(path)) => Some(root.read(&path).map(|read| (path, read))),
        Ok(None) => None,
        Err(e) => Some(Err(e)),
    };
    let mut state = state.lock().map_err(|_| "Source session unavailable")?;
    let a = state.current(token, generation)?; // stale completion never replaces newer state
    match outcome {
        None => {
            a.operation = "cancelled".into();
        }
        Some(Err(error)) => {
            a.operation = "failed".into();
            a.read_gap = Some(error);
        }
        Some(Ok((path, read))) => {
            let reference = opaque_id("source-observation-")?;
            let view = json!({"selectedPath":native_path_identity(&path),"displayPath":path.to_string_lossy(),"pathDisplayLimit":if path.to_str().is_none(){Some("Display is lossy; selectedPath is lossless")}else{None},"text":std::str::from_utf8(&read.bytes).unwrap(),"sha256":sha256_hex(&read.bytes),"byteLength":read.bytes.len(),"lineCount":line_spans(&read.bytes).len(),"openedFileIdentity":read.identity,"observedAt":now_rfc3339(),"timeProvenance":"observed_clock","mechanism":"native-picker callback / descriptor read; injected callbacks are synthetic tests, not person-act evidence","mutationLimit":"Ordinary metadata/path checks matched; transient writes may evade checks. No coherent historical revision or continuous pathname guarantee."});
            a.observation = Some(Observation {
                selection_mechanism: mechanism,
                reference,
                selected_path: path,
                question: a.question.clone(),
                bytes: read.bytes,
                view,
                anchors: HashMap::new(),
                revision: json!({"kind":"unavailable","limit":"No revision evidence supplied"}),
            });
            a.operation = "observed".into();
            a.read_gap = None;
            a.excerpt_gap = None; // A new buffer retires the old excerpt operation.
        }
    };
    Ok(state.snapshot())
}
fn line_spans(bytes: &[u8]) -> Vec<(usize, usize)> {
    let mut lines = Vec::new();
    let mut start = 0;
    for (i, b) in bytes.iter().enumerate() {
        if *b == b'\n' {
            lines.push((start, i + 1));
            start = i + 1;
        }
    }
    if start < bytes.len() {
        lines.push((start, bytes.len()));
    }
    lines
}
pub(crate) fn excerpt(
    bytes: &[u8],
    start: usize,
    end: usize,
    expected: Option<&str>,
) -> Result<Value, String> {
    let lines = line_spans(bytes);
    if start == 0 || end < start || end > lines.len() {
        return Err("Invalid/out-of-range line interval; no excerpt produced".into());
    }
    let (from, to) = (lines[start - 1].0, lines[end - 1].1);
    let selected = &bytes[from..to];
    let text = std::str::from_utf8(selected).map_err(|_| "Invalid UTF-8 snapshot")?;
    if expected.is_some_and(|e| e.as_bytes() != selected) {
        return Err("Expected excerpt mismatch; no approximate match or new anchor".into());
    }
    Ok(
        json!({"anchor":if start==end{format!("L{start}")}else{format!("L{start}-L{end}")},"byteStart":from,"byteEnd":to,"interval":"zero-based half-open original UTF-8 bytes","text":text,"sha256":sha256_hex(selected),"standing":"Exact location/inclusion only; no paraphrase, revision, truth or authority validation"}),
    )
}
#[cfg(all(test, unix))]
#[path = "connector_source_tests.rs"]
mod tests;

#[cfg(unix)]
#[derive(Default)]
struct GitState {
    pending: Option<std::sync::Arc<std::sync::atomic::AtomicBool>>,
    operation: String,
    error: Option<String>,
    result: Option<(String, String, crate::connector_git::Completed)>,
    anchors: Vec<Value>,
}
#[cfg(unix)]
impl GitState {
    fn invalidate(&mut self, reason: &str) {
        if self.pending.is_none() && self.result.is_none() {
            self.operation.clear();
            self.error = None;
            return;
        }
        if let Some(c) = &self.pending {
            c.store(true, std::sync::atomic::Ordering::SeqCst);
        }
        self.operation = "cancelled".into();
        self.error = Some(reason.into());
    }
    fn view(&self) -> Value {
        json!({"operation":if self.operation.is_empty(){"not-requested"}else{&self.operation},"error":self.error,"result":self.result.as_ref().map(|(reference,local,result)|json!({"reference":reference,"localObservationReference":local,"historical":self.operation!="completed","observation":result.view(),"anchors":self.anchors}))})
    }
}
#[cfg(unix)]
impl Drop for GitState {
    fn drop(&mut self) {
        if let Some(c) = &self.pending {
            c.store(true, std::sync::atomic::Ordering::SeqCst);
        }
    }
}
#[cfg(unix)]
pub fn git_read(
    state: &Mutex<Session>,
    token: &str,
    generation: &str,
    reference: &str,
    at: &str,
    since: Option<&str>,
) -> Result<Value, String> {
    git_read_with(state, token, generation, reference, at, since, |_| Ok(()))
}
#[cfg(unix)]
fn git_read_with(
    state: &Mutex<Session>,
    token: &str,
    generation: &str,
    reference: &str,
    at: &str,
    since: Option<&str>,
    hook: impl FnMut(&str) -> crate::connector_git_process::Result<()>,
) -> Result<Value, String> {
    use crate::connector_git_process::{Control, Failure};
    let (root, relative, cancel) = {
        let mut s = state.lock().map_err(|_| "Source state unavailable")?;
        let a = s.current(token, generation)?;
        if a.operation != "observed" {
            return Err("Git requires a current successful local selection; failed/cancelled historical observations are ineligible".into());
        }
        let o = a
            .observation
            .as_ref()
            .filter(|o| o.reference == reference)
            .ok_or("Unknown current local observation")?;
        if a.git.pending.is_some() {
            return Err("Git request already pending".into());
        }
        let location = match a.root.git_location(&o.selected_path) {
            Ok(location) => location,
            Err(error) => {
                a.git.operation = "failed".into();
                a.git.error = Some(format!("association_changed: {error}; no new Git result"));
                return Ok(s.snapshot());
            }
        };
        let cancel = Arc::new(std::sync::atomic::AtomicBool::new(false));
        a.git.pending = Some(cancel.clone());
        a.git.operation = "reading".into();
        a.git.error = None;
        (location.0, location.1, cancel)
    };
    let control = Control::new(cancel.clone());
    let mut result = crate::connector_git::read_with(&root, &relative, at, since, &control, hook);
    let mut s = state.lock().map_err(|_| "Source state unavailable")?;
    let a = s.current(token, generation)?;
    if a.operation != "observed"
        || a.observation
            .as_ref()
            .is_none_or(|o| o.reference != reference)
        || a.git
            .pending
            .as_ref()
            .is_none_or(|c| !Arc::ptr_eq(c, &cancel))
        || cancel.load(std::sync::atomic::Ordering::SeqCst)
    {
        result = Err(Failure::abort(
            "cancelled",
            "Session/current selection changed or request cancelled; entire new result discarded",
        ));
    }
    if let Err(e) = a.root.verify() {
        result = Err(Failure::abort("association_changed", e));
    }
    if let Err(e) = control.check() {
        result = Err(e);
    }
    a.git.pending = None;
    match result {
        Ok(result) => {
            a.git.result = Some((opaque_id("git-observation-")?, reference.into(), result));
            a.git.anchors.clear();
            a.git.operation = "completed".into();
            a.git.error = None;
        }
        Err(e) => {
            a.git.operation = if e.kind == "cancelled" {
                "cancelled"
            } else {
                "failed"
            }
            .into();
            a.git.error=Some(format!("{}: {}; effect: no new Git result; responsibility remains caller-assigned or unassigned",e.kind,e.detail));
        }
    }
    Ok(s.snapshot())
}
#[cfg(unix)]
pub fn git_cancel(state: &Mutex<Session>, token: &str, generation: &str) -> Result<Value, String> {
    let mut s = state.lock().map_err(|_| "Source state unavailable")?;
    s.current(token, generation)?
        .git
        .invalidate("User cancelled Git request; only prior historical result retained");
    Ok(s.snapshot())
}
#[cfg(unix)]
pub fn git_anchor(
    state: &Mutex<Session>,
    token: &str,
    generation: &str,
    reference: &str,
    side: &str,
    start: usize,
    end: usize,
    expected: Option<&str>,
) -> Result<Value, String> {
    let mut s = state.lock().map_err(|_| "Source state unavailable")?;
    let a = s.current(token, generation)?;
    let (r, _, result) = a
        .git
        .result
        .as_ref()
        .filter(|(r, _, _)| r == reference)
        .ok_or("Unknown Git observation; no DTO recreation")?;
    let selected = match side {
        "at" => Some(&result.at),
        "since" => result.since.as_ref(),
        _ => None,
    }
    .ok_or("Unknown Git side")?
    .as_ref()
    .map_err(|_| "Git side has no successful blob")?;
    let mut anchor = excerpt(&selected.bytes, start, end, expected)?;
    anchor["gitObservationReference"] = json!(r);
    anchor["side"] = json!(side);
    anchor["sideObservationReference"] = selected.view["reference"].clone();
    anchor["commit"] = selected.view["readCommit"].clone();
    anchor["blob"] = selected.view["blob"].clone();
    anchor["blobSha256"] = selected.view["sha256"].clone();
    anchor["reference"] = json!(opaque_id("git-anchor-")?);
    a.git.anchors.push(anchor);
    Ok(s.snapshot())
}

#[cfg(unix)]
pub(crate) struct MaterializationEvidence {
    pub root: Arc<Root>,
    pub project: PathBuf,
    pub relative: PathBuf,
    pub question: Value,
    pub trigger: String,
    pub responsible: Option<String>,
    pub mechanism: &'static str,
    pub local_reference: String,
    pub git_reference: String,
    pub at: Result<crate::connector_git::Side, crate::connector_git_process::Failure>,
    pub since: Option<Result<crate::connector_git::Side, crate::connector_git_process::Failure>>,
    pub association: Value,
    pub engine: Value,
    pub request: Value,
    pub anchors: Vec<Value>,
}
#[cfg(unix)]
impl Session {
    pub(crate) fn materialization_evidence(
        &mut self,
        token: &str,
        generation: &str,
        reference: &str,
    ) -> Result<MaterializationEvidence, String> {
        let a = self.current(token, generation)?;
        if a.operation != "observed" || a.git.operation != "completed" || a.git.pending.is_some() {
            return Err("Materialization requires current completed source/Git evidence".into());
        }
        let o = a.observation.as_ref().ok_or("Missing current selection")?;
        let (r, local, result) = a
            .git
            .result
            .as_ref()
            .filter(|(r, local, _)| r == reference && local == &o.reference)
            .ok_or("Unknown current Git reference")?;
        let (project, relative) = a.root.git_location(&o.selected_path)?;
        Ok(MaterializationEvidence {
            root: a.root.clone(),
            project,
            relative,
            question: a.question.view(),
            trigger: a.trigger.clone(),
            responsible: a.responsible.clone(),
            mechanism: o.selection_mechanism,
            local_reference: local.clone(),
            git_reference: r.clone(),
            at: result.at.clone(),
            since: result.since.clone(),
            association: result.association.clone(),
            engine: result.engine.clone(),
            request: result.request.clone(),
            anchors: a.git.anchors.clone(),
        })
    }
}
