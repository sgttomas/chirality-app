//! Explicit person-opened file arrival entry. This is a child of
//! runtime_session so original run custody need not become a renderer API.
use super::{HomeSession, RunLifecycle, WorkflowRun};
use crate::{
    act_control::FileActKind,
    file_act_view::{FileSource, SourceClaims},
    workflow_workspace::publication::ProjectRecords,
};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    path::{Path, PathBuf},
    sync::{Arc, Mutex},
};

#[derive(Clone, PartialEq)]
struct Candidate {
    arrival: Value,
    path: PathBuf,
    kind: FileActKind,
    scope: String,
    purpose: String,
    record: Value,
}
fn candidate(run: &WorkflowRun, id: &str) -> Result<Candidate, String> {
    if run.lifecycle != RunLifecycle::Open {
        return Err("Only an original live owned run offers an arrival file act".into());
    }
    let entries: Vec<_> = run
        .entries
        .iter()
        .filter(|e| e.record_id == id && e.kind == "checkpoint_arrival")
        .collect();
    let [entry] = entries.as_slice() else {
        return Err("Original arrival identity is absent or ambiguous".into());
    };
    let record = entry
        .written
        .as_ref()
        .ok_or("Arrival is not yet durably written; no contextual offer")?;
    if entry.refused.is_some() || record.get("corrects").is_some() {
        return Err("Corrected or refused arrival is not a contextual act source".into());
    }
    let b = &entry.body;
    let declaration = run.selection.snapshot().declaration()?;
    let checkpoints: Vec<_> = declaration
        .elements
        .get("checkpoints")
        .into_iter()
        .flatten()
        .filter(|e| {
            e.reading == crate::workflow_declaration::Reading::Recognized
                && e.value["name"] == b["checkpoint"]
        })
        .collect();
    let [checkpoint] = checkpoints.as_slice() else {
        return Err("Arrival has no unique recognized original checkpoint".into());
    };
    let cp = &checkpoint.value;
    let kind = match b["requiredAct"].as_str() {
        Some("A4") => FileActKind::Check,
        Some("A6") => FileActKind::Approve,
        Some("A7") => FileActKind::Rely,
        _ => return Err("This entry serves only A4, A6 and A7 App-file arrivals".into()),
    };
    if cp["required_act"] != b["requiredAct"]
        || cp["scope"] != b["scope"]
        || cp["purpose"] != b["purpose"]
        || cp["expected_act_evidence"]["capturing_surface"] != "app_act_control"
        || cp["subject"]["class"] != "named_output"
        || b["subjectClass"] != "named output"
        || cp["reached_when"]["kind"] != "output_produced"
        || cp["subject"]["output"] != cp["reached_when"]["output"]
    {
        return Err("Arrival does not match the original declared App-file checkpoint".into());
    }
    let output = cp["subject"]["output"]
        .as_str()
        .ok_or("Declared output absent")?;
    let outputs: Vec<_> = declaration
        .elements
        .get("returned_outputs")
        .into_iter()
        .flatten()
        .filter(|e| {
            e.reading == crate::workflow_declaration::Reading::Recognized
                && e.value["name"] == output
        })
        .collect();
    let [declared] = outputs.as_slice() else {
        return Err("Declared file output is absent or ambiguous".into());
    };
    if declared.value["form"] != "file" {
        return Err("This arrival has no single App file; message, host and multi-subject acts are not offered here".into());
    }
    let declared_path = declared.value["path"]
        .as_str()
        .ok_or("Declared file path absent")?;
    // AW-7 normalizes '.' and repeated separators. Match that existing
    // declaration meaning while retaining absolute/parent-path refusals.
    let parts: Vec<_> = declared_path
        .split('/')
        .filter(|p| !p.is_empty() && *p != ".")
        .collect();
    if declared_path.starts_with('/') || parts.is_empty() || parts.contains(&"..") {
        return Err("Declared file path is not a plain contained project path".into());
    }
    let relative = parts.join("/");
    let refs = b["referents"]
        .as_array()
        .ok_or("Arrival referents absent")?;
    if refs.len() != 1 || refs[0]["subject"] != format!("output {output}: file {relative}") {
        return Err("Arrival does not identify exactly its original declared file output".into());
    }
    let scope = b["scope"]
        .as_str()
        .filter(|s| !s.trim().is_empty())
        .ok_or("Arrival scope is not established")?
        .to_owned();
    let purpose = b["purpose"]
        .as_str()
        .filter(|s| !s.trim().is_empty())
        .ok_or("Arrival purpose is not established")?
        .to_owned();
    Ok(Candidate {
        arrival: json!({"checkpoint":b["checkpoint"],"arrivalOrdinal":b["arrivalOrdinal"]}),
        path: run.project_root.join(&relative),
        kind,
        scope,
        purpose,
        record: record.clone(),
    })
}

/// Metadata-only entry hints. Authority and file bytes are checked only after
/// the person's explicit command; a snapshot never opens a dialog or a file.
pub(super) fn entry_views(run: &WorkflowRun) -> Value {
    let mut entries = serde_json::Map::new();
    for entry in run
        .entries
        .iter()
        .filter(|e| e.kind == "checkpoint_arrival")
    {
        let view = match candidate(run, &entry.record_id) {
            Ok(_) => {
                json!({"state":"candidate","reason":"Review the original saved arrival source and current file bytes; opening a preview performs no act"})
            }
            Err(reason) => json!({"state":"unavailable","reason":reason}),
        };
        entries.insert(entry.record_id.clone(), view);
    }
    Value::Object(entries)
}

#[derive(PartialEq)]
struct Basis {
    candidate: Candidate,
    claims: Vec<Value>,
    files: BTreeMap<String, FileSource>,
    content: Value,
    request: Option<String>,
}
fn original_claim(
    record: &Value,
    source: &SourceClaims,
    relations: &Value,
) -> Result<Value, String> {
    let id = &record["recordId"];
    let claims: Vec<_> = source
        .claims
        .iter()
        .filter(|c| c["record"]["recordId"] == *id)
        .collect();
    let [claim] = claims.as_slice() else {
        return Err("Original arrival-related record is absent, duplicated or conflicting".into());
    };
    if claim["record"] != *record
        || record.get("corrects").is_some()
        || !relations["correctionGroups"]
            .as_array()
            .into_iter()
            .flatten()
            .any(|g| {
                g["sourceIncomplete"] == false
                    && g["currentCandidates"]
                        .as_array()
                        .is_some_and(|ids| ids.len() == 1 && ids[0] == *id)
            })
    {
        return Err("Original arrival-related source changed or is corrected/unresolved".into());
    }
    Ok((*claim).clone())
}
fn basis(run: &WorkflowRun, id: &str) -> Result<Basis, String> {
    let candidate = candidate(run, id)?;
    let source = crate::file_act_view::source_claims(&run.project_root);
    if !source.limits.is_empty() {
        return Err(format!(
            "Arrival source set incomplete; no contextual offer: {:?}",
            source.limits
        ));
    }
    let relations = crate::decision_view::record_relations::project_from_read_claims(
        &source.claims,
        &source.complete,
    );
    let mut claims = vec![original_claim(&candidate.record, &source, &relations)?];
    let run_id = &run.prepared().scope().run;
    let coordinates: Vec<_> = source
        .claims
        .iter()
        .filter(|c| {
            c["record"]["kind"] == "checkpoint_arrival"
                && c["record"]["runId"] == *run_id
                && c["record"]["body"]["checkpoint"] == candidate.arrival["checkpoint"]
                && c["record"]["body"]["arrivalOrdinal"] == candidate.arrival["arrivalOrdinal"]
        })
        .collect();
    if coordinates.len() != 1 || coordinates[0]["record"] != candidate.record {
        return Err("Original run/arrival coordinate has duplicated, corrected or conflicting source claims".into());
    }
    if source
        .claims
        .iter()
        .any(|c| c["record"]["kind"] == "run_ended" && c["record"]["runId"] == *run_id)
    {
        return Err("The run source records an end; no live arrival offer".into());
    }
    let openings: Vec<_> = run
        .entries
        .iter()
        .filter(|e| e.kind == "run_opened")
        .collect();
    let [opening] = openings.as_slice() else {
        return Err("Original run opening is absent or ambiguous".into());
    };
    claims.push(original_claim(
        opening
            .written
            .as_ref()
            .ok_or("Original run opening is not durably saved")?,
        &source,
        &relations,
    )?);
    let source_openings: Vec<_> = source
        .claims
        .iter()
        .filter(|claim| {
            claim["record"]["kind"] == "run_opened" && claim["record"]["runId"] == *run_id
        })
        .collect();
    if source_openings.len() != 1 || source_openings[0]["record"] != claims[1]["record"] {
        return Err("Original run opening has conflicting source claims".into());
    }
    let log = crate::records::supply::run_log(&run.project_root, run_id)?;
    if candidate.record["runId"] != *run_id
        || claims
            .iter()
            .any(|claim| claim["source"]["log"] != log.to_string_lossy().as_ref())
    {
        return Err("Arrival is outside its original run/writer source".into());
    }
    let mut content = candidate.record["body"]["referents"][0]["content"].clone();
    let known_related: Vec<_> = run
        .entries
        .iter()
        .filter(|e| {
            matches!(e.kind, "act_lapsed" | "act_request") && e.body["arrival"] == candidate.arrival
        })
        .map(|e| e.record_id.as_str())
        .collect();
    if source.claims.iter().any(|c| {
        c["record"]["runId"] == *run_id
            && matches!(
                c["record"]["kind"].as_str(),
                Some("act_lapsed" | "act_request")
            )
            && c["record"]["body"]["arrival"] == candidate.arrival
            && c["record"]["recordId"]
                .as_str()
                .is_none_or(|id| !known_related.contains(&id))
    }) {
        return Err(
            "Arrival content/request source has claims outside the original live observer".into(),
        );
    }
    for entry in run
        .entries
        .iter()
        .filter(|e| e.kind == "act_lapsed" && e.body["arrival"] == candidate.arrival)
    {
        let record = entry
            .written
            .as_ref()
            .ok_or("Arrival content observation is not durably saved")?;
        let claim = original_claim(record, &source, &relations)?;
        if record["runId"] != *run_id || claim["source"]["log"] != log.to_string_lossy().as_ref() {
            return Err("Arrival content basis is outside its original owning log".into());
        }
        if !entry.body["state"]
            .as_str()
            .is_some_and(|s| s.starts_with("unknown"))
        {
            content = entry.body["c1"].clone();
        }
        claims.push(claim);
    }
    if content["method"] != crate::util::FILE_IDENTITY_METHOD
        || content["value"].as_str().is_none_or(str::is_empty)
        || content["notObtainable"] == true
    {
        return Err(
            "Arrival has no comparable present App-file content basis; no contextual offer".into(),
        );
    }
    let requests: Vec<_> = run
        .entries
        .iter()
        .filter(|e| {
            e.kind == "act_request"
                && e.body["arrival"] == candidate.arrival
                && e.body["association"] == "associated with the current arrival"
        })
        .collect();
    let request = if let [entry] = requests.as_slice() {
        let record = entry
            .written
            .as_ref()
            .ok_or("Associated request is not durably saved")?;
        let claim = original_claim(record, &source, &relations)?;
        if record["runId"] != *run_id || claim["source"]["log"] != log.to_string_lossy().as_ref() {
            return Err("Associated request is outside its original run source".into());
        }
        claims.push(claim);
        Some(entry.record_id.clone())
    } else {
        None
    };
    let mut files = BTreeMap::new();
    for claim in &claims {
        let log = claim["source"]["log"].as_str().ok_or("Source log absent")?;
        files.insert(
            log.to_owned(),
            *source.files.get(log).ok_or("Physical source log absent")?,
        );
    }
    Ok(Basis {
        candidate,
        claims,
        files,
        content,
        request,
    })
}

/// Original live run and physical project/store custody. This is never
/// reconstructed from the preview DTO or a cold historical run.
pub(crate) struct ArrivalSource {
    run: Arc<Mutex<WorkflowRun>>,
    project: ProjectRecords,
    records_root: PathBuf,
    records_identity: FileSource,
    _records_directory: std::fs::File,
    store: PathBuf,
    store_identity: FileSource,
    _store_directory: std::fs::File,
    link: Vec<u8>,
    original: Basis,
    home: Arc<HomeSession>,
}
impl ArrivalSource {
    pub(crate) fn open(
        run: Arc<Mutex<WorkflowRun>>,
        workspace: &Path,
        run_ref: &str,
        id: &str,
    ) -> Result<Self, String> {
        let owner = run
            .try_lock()
            .map_err(|_| "Original run operation pending; review again")?;
        if owner.project_root != workspace || owner.prepared().scope().run != run_ref {
            return Err("Arrival run belongs to another project or identity".into());
        }
        let project = ProjectRecords::open(workspace)?;
        let binding = project.source_binding()?;
        if !binding.same_source(&owner.project.source_binding()?) {
            return Err("Original run project/store source changed".into());
        }
        let records_root = binding.records_root().to_path_buf();
        let records_identity = FileSource::directory_at(&records_root)?;
        let records_directory =
            crate::records_index::open_directory(&records_root).map_err(|e| e.to_string())?;
        let store =
            crate::records_store::store_root().ok_or("Original records store unavailable")?;
        let store_identity = FileSource::directory_at(&store)?;
        let store_directory =
            crate::records_index::open_directory(&store).map_err(|e| e.to_string())?;
        let link = crate::records_retention::read_plain(
            &workspace.join(crate::records_store::PROJECT_LINK),
        )?;
        let original = basis(&owner, id)?;
        let home = owner.home.clone();
        drop(owner);
        drop(binding); // no retained admission lease on a displayable offer
        let source = Self {
            run,
            project,
            records_root,
            records_identity,
            _records_directory: records_directory,
            store,
            store_identity,
            _store_directory: store_directory,
            link,
            original,
            home,
        };
        source.validate()?;
        Ok(source)
    }
    pub(crate) fn validate(&self) -> Result<(), String> {
        self.validate_recording()?;
        let owner = self
            .run
            .try_lock()
            .map_err(|_| "Original run operation pending; review again")?;
        if !Arc::ptr_eq(&self.home, &owner.home)
            || !self
                .project
                .source_binding()?
                .same_source(&owner.project.source_binding()?)
            || basis(
                &owner,
                self.original.candidate.record["recordId"]
                    .as_str()
                    .ok_or("Original arrival identity absent")?,
            )? != self.original
        {
            return Err("Original run/arrival/content/request source changed; review again".into());
        }
        let current = crate::file_act_view::current_content(
            self.project.root(),
            &self.original.candidate.path,
        );
        if current
            != crate::checkpoint_recorder::Current::Present(
                self.original.content["value"].as_str().unwrap_or("").into(),
            )
        {
            return Err("Current file does not match the arrival's recorded comparable content basis; no contextual offer".into());
        }
        Ok(())
    }
    /// Once a native act exists, run progress/content changes do not erase it.
    /// Continuation still belongs to the original physical record sources.
    pub(crate) fn validate_recording(&self) -> Result<(), String> {
        if self.project.source_binding()?.records_root() != self.records_root
            || FileSource::directory_at(&self.records_root)? != self.records_identity
            || FileSource::directory_at(&self.store)? != self.store_identity
            || crate::records_retention::read_plain(
                &self.project.root().join(crate::records_store::PROJECT_LINK),
            )? != self.link
        {
            return Err("Original arrival project/store binding changed; no rebinding".into());
        }
        let source = crate::file_act_view::source_claims(self.project.root());
        for (path, identity) in &self.original.files {
            if source.files.get(path) != Some(identity) {
                return Err("Original arrival log was replaced; no recording relocation".into());
            }
        }
        for original in &self.original.claims {
            if !source.claims.iter().any(|claim| claim == original) {
                return Err("Original arrival source bytes/sequence changed; historical act metadata is held".into());
            }
        }
        Ok(())
    }
    pub(crate) fn home(&self) -> Arc<HomeSession> {
        self.home.clone()
    }
    pub(crate) fn path(&self) -> &Path {
        &self.original.candidate.path
    }
    pub(crate) fn kind(&self) -> FileActKind {
        self.original.candidate.kind
    }
    pub(crate) fn scope(&self) -> &str {
        &self.original.candidate.scope
    }
    pub(crate) fn purpose(&self) -> &str {
        &self.original.candidate.purpose
    }
    pub(crate) fn answers(&self) -> Value {
        json!({"runId":self.original.candidate.record["runId"],"arrival":self.original.candidate.arrival})
    }
    pub(crate) fn request_ref(&self) -> Option<&str> {
        self.original.request.as_deref()
    }
    pub(crate) fn matches_identity(&self, identity: &Value) -> bool {
        identity["method"] == self.original.content["method"]
            && identity["value"] == self.original.content["value"]
    }
}
