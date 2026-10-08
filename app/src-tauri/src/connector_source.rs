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
            json!({"kind":"Revision","reason":"No verified source revision or Git binding is established","effect":"No source entry, account or revision-qualified reconstruction can be emitted","responsible":a.responsible,"assignmentStanding":"caller-assigned route; null means unassigned"}),
        ];
        if let Some(reason) = &a.read_gap {
            gaps.push(json!({"kind":"Selection/read","reason":reason,"effect":"No new source observation was produced; a retained prior buffer does not resolve this read failure","responsible":a.responsible,"assignmentStanding":"caller-assigned route; null means unassigned"}));
        }
        if let Some(reason) = &a.excerpt_gap {
            gaps.push(json!({"kind":"Excerpt","reason":reason,"effect":"This excerpt request produced no anchor; independent supported work is not blocked","responsible":a.responsible,"assignmentStanding":"caller-assigned route; null means unassigned"}));
        }
        json!({"state":"prepared","sessionToken":a.token,"generation":a.generation,"question":a.question.view(),"trigger":{"kind":a.trigger,"standing":"constructed caller context, no connector observation"},"operation":a.operation,"gaps":gaps,
        "observation":a.observation.as_ref().map(|o|json!({"reference":o.reference,"question":o.question.view(),"read":o.view,"revision":o.revision,"anchors":o.anchors.values().collect::<Vec<_>>(),"historical":a.operation!="observed"})),
        "limits":["Session memory only; process loss loses capabilities and previews","Opened capabilities are not continuous pathname containment; concurrent renames/transient writes may evade checks","Hash describes the buffer read, not a coherent historical revision or authoritative statements","No source/account/fact/conclusion/duty/save/send/Git production"],
        "dutiesStanding":"Locate/compare, manager review/integration and necessary person coordination are unperformed/outstanding in this producer; no not-required or performed duty is authored"})
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
    let root = {
        let mut state = state.lock().map_err(|_| "Source session unavailable")?;
        let a = state.current(token, generation)?;
        if a.operation == "selecting" {
            return Err("Source selection already pending".into());
        }
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
                reference,
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
fn excerpt(
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
