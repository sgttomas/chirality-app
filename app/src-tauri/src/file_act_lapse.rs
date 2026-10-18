//! Explicit standalone App-file content observations (RS §7 L-1…L-11).
//! Reading never calls this writer. Held observations retain their first bytes,
//! time and source custody; retry only writes that metadata, never a new act.
use crate::{
    checkpoint_recorder::{self, Current},
    file_act_view::{self, FileSource, SourceClaims},
    records::{self, RecordSet, APP_WRITER},
    workflow_workspace::publication::{ProjectRecords, ProjectSourceBinding},
};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

pub(crate) struct History {
    pub claims: Vec<Value>,
    pub limited: Vec<Value>,
    pub limits: Vec<String>,
}
/// History is ordered only in the one owning log, never by directory order or
/// asserted timestamps. All rejected candidates retain their source/relations.
pub(crate) fn history(
    record: &Value,
    source: &SourceClaims,
    relations: &Value,
    log: Option<&Path>,
) -> History {
    history_in_log(record, source, relations, log, false)
}
/// Display preserves valid checkpoint history on a standing act that later
/// answered an arrival. Different source logs are separate unordered chains.
pub(crate) fn display_history(record: &Value, source: &SourceClaims, relations: &Value) -> History {
    let mut logs = std::collections::BTreeSet::new();
    for c in relations["claims"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|c| {
            c["record"]["kind"] == "act_lapsed"
                && c["record"]["body"]["act"]["recordId"] == record["recordId"]
        })
    {
        if let Some(log) = c["source"]["log"].as_str() {
            logs.insert(log.to_owned());
        }
    }
    let mut result = History {
        claims: vec![],
        limited: vec![],
        limits: vec![],
    };
    if logs.len() > 1 {
        result.limits.push("History has several source logs; order between those logs is not established; each log retains its own sequence".into());
    }
    for log in logs {
        let history = history_in_log(record, source, relations, Some(Path::new(&log)), true);
        result.claims.extend(history.claims);
        result.limited.extend(history.limited);
        for limit in history.limits {
            if !result.limits.contains(&limit) {
                result.limits.push(limit);
            }
        }
    }
    result
}
fn history_in_log(
    record: &Value,
    source: &SourceClaims,
    relations: &Value,
    log: Option<&Path>,
    display: bool,
) -> History {
    let mut result = History {
        claims: vec![],
        limited: vec![],
        limits: vec![],
    };
    let id = &record["recordId"];
    let all = relations["claims"]
        .as_array()
        .map(Vec::as_slice)
        .unwrap_or(&[]);
    let unique_current = |entry: &Value| {
        let id = &entry["recordId"];
        source
            .claims
            .iter()
            .filter(|c| c["record"]["recordId"] == *id)
            .count()
            == 1
            && relations["correctionGroups"]
                .as_array()
                .into_iter()
                .flatten()
                .any(|g| {
                    g["sourceIncomplete"] == false
                        && g["currentCandidates"]
                            .as_array()
                            .is_some_and(|v| v.len() == 1 && v[0] == *id)
                })
    };
    for candidate in all.iter().filter(|c| {
        c["record"]["kind"] == "act_lapsed" && c["record"]["body"]["act"]["recordId"] == *id
    }) {
        if display && log.is_some_and(|log| candidate["source"]["log"].as_str() != log.to_str()) {
            continue;
        }
        let e = &candidate["record"];
        let b = &e["body"];
        let bound = &record["body"]["boundContent"][0];
        let standalone = record.get("runId").is_none();
        let reason = if !source.limits.is_empty() {
            Some("Project source set incomplete; history is limited")
        } else if record["kind"] != "human_act" || !unique_current(record) {
            Some("Act source is not a unique current claim")
        } else if !unique_current(e) {
            Some("Lapse source is corrected, conflicting, duplicated or unresolved")
        } else if candidate["relationLimit"].is_string() {
            Some("Lapse correction relation unresolved")
        } else if log.is_none_or(|log| candidate["source"]["log"].as_str() != log.to_str()) {
            Some("Lapse is outside the one established owning log; interval order not established")
        } else if e["recorder"]["role"] != APP_WRITER.role
            || e["recorder"]["identity"] != APP_WRITER.identity
        {
            Some("Lapse recorder is not the App writer")
        } else if b["act"]["actKind"] != record["body"]["actKind"]
            || b["act"]["capturedAt"] != record["body"]["captureTime"]
            || b["act"]["capturingSurface"] != "app_act_control"
            || b["referents"] != record["body"]["boundSubject"]
            || b["c0"] != *bound
        {
            Some("Lapse does not match this act, capture, subject and original content")
        } else if !display
            && standalone
            && (e.get("runId").is_some() || b.get("arrival").is_some() || b.get("when").is_some())
        {
            Some("Arrival/run lapse is separate from standalone observation history")
        } else if !valid_state(b, bound) {
            Some("Lapse state and content identities do not correspond")
        } else {
            None
        };
        if let Some(reason) = reason {
            let mut limited = candidate.clone();
            limited["historyLimit"] = json!(reason);
            result.limited.push(limited);
            if !result.limits.iter().any(|r| r == reason) {
                result.limits.push(reason.into());
            }
        } else {
            result.claims.push(candidate.clone());
        }
    }
    result
        .claims
        .sort_by_key(|c| c["record"]["seq"].as_u64().unwrap_or(0));
    // A return label cannot itself establish a missing interval. Keep it as a
    // limited source claim unless an earlier determinate lapse was read here.
    let mut observed = false;
    result.claims.retain(|c| {
        let state = c["record"]["body"]["state"].as_str().unwrap_or("");
        if state == "matches c0 again after observed lapse" && !observed {
            let mut limited = c.clone();
            limited["historyLimit"] =
                json!("Return-to-c0 claim has no earlier qualifying lapse in this log");
            result.limited.push(limited);
            result
                .limits
                .push("Return-to-c0 claim has no earlier qualifying lapse in this log".into());
            false
        } else {
            observed |= matches!(
                state,
                "lapsed" | "lapsed (subject absent)" | "partially lapsed"
            );
            true
        }
    });
    result
}
fn valid_state(b: &Value, bound: &Value) -> bool {
    match b["state"].as_str() {
        Some("lapsed" | "partially lapsed") => {
            b["c1"]["method"] == bound["method"]
                && b["c1"]["value"].as_str().is_some_and(|s| !s.is_empty())
                && b["c1"] != *bound
        }
        Some("lapsed (subject absent)") => b["c1"] == "subject absent",
        Some("matches c0 again after observed lapse") => b["c1"] == *bound,
        Some("unknown (incomparable)") => {
            b["c1"]["notObtainable"] == true || b["c1"]["method"] != bound["method"]
        }
        Some("unknown (unavailable)") => b["c1"]["notObtainable"] == true,
        _ => false,
    }
}

struct Owner {
    project: ProjectRecords,
    source: ProjectSourceBinding,
    project_id: String,
    store_root: PathBuf,
    store_identity: FileSource,
    link: Vec<u8>,
    _activity: Option<crate::storage::Ownership>,
}
impl Owner {
    fn open(root: &Path) -> Result<Self, String> {
        let project = ProjectRecords::open(root)?;
        let home = crate::records_store::home(root)?;
        if let Some(reason) = home.attachment.refusal {
            return Err(reason);
        }
        if !home.store_mode || !home.attachment.limits.is_empty() {
            return Err("Standalone lapse observations require the current attached store with no identity limits; no import or identity is created".into());
        }
        let project_id = home
            .attachment
            .project
            .ok_or("Project identity unavailable")?;
        let store_root =
            crate::records_store::store_root().ok_or("Original records store is unavailable")?;
        let store_identity = FileSource::directory_at(&store_root)?;
        let activity = crate::records_retention::activity(root)?;
        let source = project.source_binding()?;
        let link =
            crate::records_retention::read_plain(&root.join(crate::records_store::PROJECT_LINK))?;
        Ok(Self {
            project,
            source,
            project_id,
            store_root,
            store_identity,
            link,
            _activity: activity,
        })
    }
    fn validate(&self, root: &Path) -> Result<(), String> {
        if self.project.root() != root {
            return Err(
                "Original lapse project changed; held observations are not relocated".into(),
            );
        }
        let current = self.project.source_binding()?;
        let home = crate::records_store::home(root)?;
        if !self.source.same_source(&current)
            || FileSource::directory_at(&self.store_root)? != self.store_identity
            || !home.store_mode
            || home.attachment.project.as_deref() != Some(&self.project_id)
            || home.attachment.refusal.is_some()
            || !home.attachment.limits.is_empty()
            || crate::records_retention::read_plain(&root.join(crate::records_store::PROJECT_LINK))?
                != self.link
        {
            return Err(
                "Original lapse project/store source binding changed; no relocation or rebinding"
                    .into(),
            );
        }
        if crate::records_store::write_dir(root)? != self.source.records_root() {
            return Err("Original lapse target changed; nothing written".into());
        }
        Ok(())
    }
    fn log(&self) -> PathBuf {
        self.source.records_root().join(crate::recorder::LOG)
    }
}
struct Pending {
    claim: Value,
    log_source: FileSource,
    capture: Value,
    capture_path: PathBuf,
    capture_stamp: crate::records_index::Stamp,
    body: Value,
    id: String,
    observed_at: String,
    failure: Option<String>,
    limit_id: String,
    limit_body: Option<Value>,
    target_source: Option<FileSource>,
    written: Option<Value>,
}
fn recoverable_own_tail(source: &SourceClaims, log: &Path) -> bool {
    !source.incomplete
        && source.partial_logs.len() == 1
        && log
            .to_str()
            .is_some_and(|log| source.partial_logs.contains(log))
}
impl Pending {
    fn view(&self) -> Value {
        json!({"recordId":self.id,"observedAt":self.observed_at,"kind":"act_lapsed","body":self.body,"source":self.claim["source"],"failure":self.failure,"observationDurable":self.written.is_some(),"recordedEntry":self.written,"lateWriteDisclosurePending":self.written.is_some() && self.failure.is_some(),"standing":if self.written.is_some(){"observation saved; required late-write disclosure pending; retry only finishes original metadata"}else{"held observation in this process only; durable save not established; retry records these original values without recomputing this observation from today's subject content"}})
    }
    fn validate(
        &self,
        owner: &Owner,
        source: &SourceClaims,
        allow_own_tail: bool,
    ) -> Result<(), String> {
        owner.validate(owner.project.root())?;
        if !source.limits.is_empty()
            && !(allow_own_tail && recoverable_own_tail(source, &owner.log()))
        {
            return Err(format!(
                "Project source set incomplete: {:?}",
                source.limits
            ));
        }
        let id = self.claim["record"]["recordId"]
            .as_str()
            .ok_or("Original act identity absent")?;
        let candidates: Vec<_> = source
            .claims
            .iter()
            .filter(|c| c["record"]["recordId"] == id)
            .collect();
        if candidates.len() != 1
            || candidates[0] != &self.claim
            || source
                .files
                .get(self.claim["source"]["log"].as_str().unwrap_or(""))
                != Some(&self.log_source)
        {
            return Err("Original act log/physical source/sequence/record changed; held observation not rebound".into());
        }
        let admitted = checkpoint_recorder::project_act_records(owner.project.root())?;
        if !admitted
            .acts
            .iter()
            .any(|a| a["record"] == self.claim["record"])
        {
            return Err("Original act is no longer an admitted unique current capture; held observation not written".into());
        }
        let capture =
            file_act_view::observe_capture(owner.project.root(), &self.claim["record"]["body"]);
        if capture.result.as_ref().ok() != Some(&self.capture)
            || capture
                .watch
                .as_ref()
                .is_none_or(|w| w.path != self.capture_path || w.stamp != Some(self.capture_stamp))
        {
            return Err(
                "Original capture source changed or unavailable; held observation not rebound"
                    .into(),
            );
        }
        if !unique_capture(&self.capture, source) {
            return Err("Several source records cite the original capture (RS R-8); held observation not written".into());
        }
        if arrival_bound(&self.claim["record"], &self.capture, source) {
            return Err(
                "Act is arrival/run bound; standalone observer does not duplicate its observations"
                    .into(),
            );
        }
        if let Some(expected) = self.target_source {
            if FileSource::at(&owner.log())? != expected {
                return Err(
                    "Original lapse target log was replaced; held observation not relocated".into(),
                );
            }
        }
        Ok(())
    }
    fn append(&mut self, owner: &Owner, source: &SourceClaims) -> Result<Value, String> {
        self.validate(owner, source, true)?;
        let log = owner.log();
        if source
            .partial_logs
            .contains(log.to_str().ok_or("Original log path is not UTF-8")?)
        {
            // Recover only the already pinned owning target. A whole tail can
            // expose a correction or shared capture: reread and admit the
            // recovered source before writing any held observation metadata.
            records::open_owning_log(owner.project.root(), &log)?;
            self.validate(
                owner,
                &file_act_view::source_claims(owner.project.root()),
                false,
            )?;
        }
        let result = append_exact(
            owner.project.root(),
            &log,
            "act_lapsed",
            &self.body,
            &self.id,
            &self.observed_at,
        );
        if self.target_source.is_none() {
            self.target_source = FileSource::at(&log).ok();
        }
        let entry = result?;
        self.written = Some(entry.clone());
        if let Some(failure) = &self.failure {
            let body = self.limit_body.get_or_insert_with(|| json!({"label":"record write failed","subjectRef":self.id,"detail":format!("Standalone act_lapsed saved after its original observation; first failure: {failure}; original content observation and time retained, no act recaptured")}));
            #[cfg(test)]
            before_late_limit();
            append_exact(
                owner.project.root(),
                &log,
                "evidence_limit",
                body,
                &self.limit_id,
                &self.observed_at,
            )?;
        }
        Ok(entry)
    }
}
fn append_exact(
    root: &Path,
    log: &Path,
    kind: &str,
    body: &Value,
    id: &str,
    at: &str,
) -> Result<Value, String> {
    let (all, own) = records::append_record_set(root, log, RecordSet::Complete, id)?;
    if all.len() > 1
        || all.iter().any(|e| {
            e["kind"] != kind
                || e["body"] != *body
                || e["observedAt"] != at
                || e.get("runId").is_some()
                || e["recorder"]["role"] != APP_WRITER.role
                || e["recorder"]["identity"] != APP_WRITER.identity
        })
    {
        return Err("Reserved lapse observation identity is duplicated or holds different content; nothing written".into());
    }
    if !all.is_empty() && own.len() != 1 {
        return Err(
            "Reserved lapse observation exists outside its original owning log; nothing rebound"
                .into(),
        );
    }
    if let Some(entry) = own.first() {
        crate::storage::sync_publication(log)?;
        return Ok(entry.clone());
    }
    records::append_reserved(
        log,
        kind,
        &APP_WRITER,
        body.clone(),
        id.into(),
        None,
        Some(at),
        RecordSet::Complete,
        crate::schema_validation::bundled(),
    )
}
fn unique_capture(capture: &Value, source: &SourceClaims) -> bool {
    source
        .claims
        .iter()
        .filter(|c| {
            matches!(
                c["record"]["kind"].as_str(),
                Some("human_act" | "act_declined")
            ) && c["record"]["body"]["captureEvidence"]
                .as_array()
                .is_some_and(|refs| refs.iter().any(|r| r["ref"] == capture["captureId"]))
        })
        .count()
        == 1
}
fn arrival_bound(record: &Value, capture: &Value, source: &SourceClaims) -> bool {
    record.get("runId").is_some()
        || capture["answers"]["standing"] != "no arrival: a standing act (RC-6)"
        || source.claims.iter().any(|c| {
            let e = &c["record"];
            let b = &e["body"];
            let id = &record["recordId"];
            (matches!(
                e["kind"].as_str(),
                Some("act_counted" | "act_not_counted" | "act_lapsed")
            ) && b["act"]["recordId"] == *id
                && (e.get("runId").is_some() || b.get("arrival").is_some()))
                || b["answeredBy"]
                    .as_array()
                    .is_some_and(|ids| ids.contains(id))
        })
}
fn observation(record: &Value, current: Current, history: &[Value], at: &str) -> Option<Value> {
    let b = &record["body"];
    let c0 = &b["boundContent"][0];
    let had_lapse = history.iter().any(|c| {
        matches!(
            c["record"]["body"]["state"].as_str(),
            Some("lapsed" | "lapsed (subject absent)" | "partially lapsed")
        )
    });
    let (state, c1) = if c0["method"] != crate::util::FILE_IDENTITY_METHOD
        || c0["value"].as_str().is_none_or(str::is_empty)
    {
        (
            "unknown (incomparable)",
            match current {
                Current::Present(value) => {
                    json!({"method":crate::util::FILE_IDENTITY_METHOD,"value":value})
                }
                _ => {
                    json!({"notObtainable":true,"reason":"No current identity comparable with the original method; no lapse or currency is claimed"})
                }
            },
        )
    } else {
        match current {
            Current::Present(value) if c0["value"] != value => (
                "lapsed",
                json!({"method":crate::util::FILE_IDENTITY_METHOD,"value":value}),
            ),
            Current::Present(value) if had_lapse => (
                "matches c0 again after observed lapse",
                json!({"method":crate::util::FILE_IDENTITY_METHOD,"value":value}),
            ),
            Current::Present(_) => return None,
            Current::Absent => ("lapsed (subject absent)", json!("subject absent")),
            Current::Unavailable(reason) => (
                "unknown (unavailable)",
                json!({"notObtainable":true,"reason":format!("{reason}; no lapse or currency is claimed")}),
            ),
        }
    };
    // Unknown readings never end a determinate interval. A later return/change
    // is compared with the latest determinate entry; repeated unknowns are quiet.
    let previous = if state.starts_with("unknown") {
        history.last()
    } else {
        history.iter().rev().find(|c| {
            !c["record"]["body"]["state"]
                .as_str()
                .unwrap_or("")
                .starts_with("unknown")
        })
    };
    if previous.is_some_and(|p| {
        p["record"]["body"]["state"] == state
            && (state.starts_with("unknown") || p["record"]["body"]["c1"] == c1)
    }) {
        return None;
    }
    Some(
        json!({"act":{"recordId":record["recordId"],"actKind":b["actKind"],"capturedAt":b["captureTime"],"capturingSurface":"app_act_control"},"state":state,"referents":b["boundSubject"],"c0":c0,"c1":c1,"time":at}),
    )
}
#[derive(Default)]
pub(crate) struct Observer {
    owner: Option<Owner>,
    pending: Vec<Pending>,
    state: String,
    limits: Vec<String>,
}
impl Observer {
    pub(crate) fn snapshot(&self) -> Value {
        json!({"state":if self.state.is_empty(){"not observed"}else{&self.state},"recorded":[],"pending":self.pending.iter().map(Pending::view).collect::<Vec<_>>(),"limits":self.limits,"standing":"Content observation metadata only; no human act, capture, run, send, current standing or reauthorization is created. Unsaved observations survive only in this process."})
    }
    pub(crate) fn observe(&mut self, root: &Path) -> Value {
        if !self.pending.is_empty() {
            self.state =
                "held observations require metadata-only retry; no new content observation".into();
            return self.snapshot();
        }
        self.limits.clear();
        self.state = "content observed; no new lapse observation needed".into();
        if let Err(error) = self.prepare(root) {
            self.limits.push(error);
            self.state = "content observation limited; durable save not established".into();
        }
        self.flush(root)
    }
    fn prepare(&mut self, root: &Path) -> Result<(), String> {
        let owner = Owner::open(root)?;
        owner.validate(root)?;
        let mut source = file_act_view::source_claims(root);
        if recoverable_own_tail(&source, &owner.log()) {
            let log = owner.log();
            if source
                .files
                .get(log.to_str().ok_or("Original log path is not UTF-8")?)
                != Some(&FileSource::at(&log)?)
            {
                return Err(
                    "Original owning log changed before W-0; no new content observation".into(),
                );
            }
            records::open_owning_log(root, &log)?;
            owner.validate(root)?;
            source = file_act_view::source_claims(root);
        }
        if !source.limits.is_empty() {
            return Err(format!(
                "Project source set incomplete; no content observed: {:?}",
                source.limits
            ));
        }
        let read = checkpoint_recorder::project_act_records(root)?;
        self.owner = Some(owner);
        let owner = self.owner.as_ref().expect("original observation owner");
        let relations = crate::decision_view::record_relations::project_from_read_claims(
            &source.claims,
            &source.complete,
        );
        for act in &read.acts {
            let record = &act["record"];
            if record["kind"] != "human_act" || record.get("corrects").is_some() {
                continue;
            }
            let id = &record["recordId"];
            let claims: Vec<_> = source
                .claims
                .iter()
                .filter(|c| c["record"]["recordId"] == *id)
                .collect();
            if claims.len() != 1 || claims[0]["record"] != *record {
                self.limits.push(format!(
                    "Act {id}: original source is duplicated or differs; no lapse observation"
                ));
                continue;
            }
            let claim = claims[0];
            let b = &record["body"];
            let (Some([subject]), Some([_])) = (
                b["boundSubject"].as_array().map(Vec::as_slice),
                b["boundContent"].as_array().map(Vec::as_slice),
            ) else {
                continue;
            };
            let Some(path) = subject.as_str().map(Path::new) else {
                continue;
            };
            if !path.is_absolute()
                || !path.starts_with(root)
                || path == root
                || path.components().any(|c| {
                    !matches!(
                        c,
                        std::path::Component::RootDir | std::path::Component::Normal(_)
                    )
                })
            {
                self.limits.push(format!(
                    "Act {id}: subject scope is not a contained physical App path"
                ));
                continue;
            }
            let capture = file_act_view::observe_capture(root, b);
            let original = capture.result?;
            if !file_act_view::corresponds(&original, record) {
                return Err("Act/capture correspondence changed before content observation".into());
            }
            if !unique_capture(&original, &source) {
                self.limits.push(format!("Act {id}: several source records cite one capture (RS R-8); no lapse observation"));
                continue;
            }
            if arrival_bound(record, &original, &source) {
                continue;
            }
            let history = history(record, &source, &relations, Some(&owner.log()));
            if !history.limited.is_empty() {
                self.limits.extend(history.limits);
                continue;
            }
            let at = crate::util::now_rfc3339();
            let reserved_id = crate::util::opaque_id("rec:app:")?;
            let limit_id = crate::util::opaque_id("rec:app:")?;
            let Some(body) = observation(
                record,
                file_act_view::current_content(root, path),
                &history.claims,
                &at,
            ) else {
                continue;
            };
            let watch = capture
                .watch
                .ok_or("Original capture physical source unavailable")?;
            self.pending.push(Pending {
                claim: claim.clone(),
                log_source: *source
                    .files
                    .get(claim["source"]["log"].as_str().unwrap_or(""))
                    .ok_or("Original act log source unavailable")?,
                capture: original,
                capture_path: watch.path,
                capture_stamp: watch.stamp.ok_or("Original capture stamp unavailable")?,
                body,
                id: reserved_id,
                observed_at: at,
                failure: None,
                limit_id,
                limit_body: None,
                target_source: FileSource::at(&owner.log()).ok(),
                written: None,
            });
        }
        for unresolved in &read.unresolved {
            self.limits.push(format!(
                "Act {} not observed: {}",
                unresolved["record"]["recordId"], unresolved["reason"]
            ));
        }
        Ok(())
    }
    pub(crate) fn retry(&mut self, root: &Path) -> Value {
        self.limits.clear();
        self.state = if self.pending.is_empty() {
            "no held observations; no content read"
        } else {
            "retrying held observation metadata only"
        }
        .into();
        self.flush(root)
    }
    fn flush(&mut self, root: &Path) -> Value {
        let mut recorded = Vec::new();
        if !self.pending.is_empty() {
            let result = (|| {
                let owner = self
                    .owner
                    .as_ref()
                    .ok_or("Original observation owner unavailable")?;
                owner.validate(root)?;
                while !self.pending.is_empty() {
                    let source = file_act_view::source_claims(root);
                    match self.pending[0].append(owner, &source) {
                        Ok(entry) => {
                            recorded.push(entry);
                            self.pending.remove(0);
                        }
                        Err(error) => {
                            self.pending[0].failure.get_or_insert(error.clone());
                            return Err(error);
                        }
                    }
                }
                Ok::<_, String>(())
            })();
            if let Err(error) = result {
                if let Some(pending) = self.pending.first_mut() {
                    pending.failure.get_or_insert(error.clone());
                }
                self.limits.push(error);
                self.state = if self.pending.first().is_some_and(|p| p.written.is_some()) {
                    "observation saved; required late-write disclosure pending"
                } else {
                    "observation held; durable save not established; retry original metadata only"
                }
                .into();
            } else {
                self.state = "observations saved to the project's act log".into();
            }
        }
        if self.pending.is_empty() {
            self.owner = None;
        }
        let mut status = self.snapshot();
        status["recorded"] = json!(recorded);
        status
    }
}

#[cfg(test)]
thread_local! { static BEFORE_LATE_LIMIT: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) }; }
#[cfg(test)]
pub(crate) fn before_late_limit_for_test(hook: impl FnOnce() + 'static) {
    BEFORE_LATE_LIMIT.with(|slot| *slot.borrow_mut() = Some(Box::new(hook)));
}
#[cfg(test)]
fn before_late_limit() {
    if let Some(hook) = BEFORE_LATE_LIMIT.with(|slot| slot.borrow_mut().take()) {
        hook();
    }
}
