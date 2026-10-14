//! FR §4: source-issued native conversation relationships. Publication records
//! the observed fact; it grants no native, role, workflow or work-state authority.
use crate::{
    conversation_roles::ContinuationSource,
    hosting::{Host, SourceRequest},
    runtime_session::HomeSession,
};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    os::unix::fs::MetadataExt,
    path::{Path, PathBuf},
    sync::{Arc, LazyLock, Mutex, OnceLock},
};
const LOG: &str = "coordination.fleet.jsonl";
const ID: &str = "urn:chirality:app-v4:del-06-01:fleet-native-links:0.2";
pub(crate) fn validate_record(record: &Value) -> Result<(), String> {
    static SCHEMA: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
    SCHEMA
        .get_or_init(|| {
            crate::schema_validation::compile_targets(
                &[(
                    "fleet.native-links.schema.json",
                    include_str!("../schemas/fleet.native-links.schema.json"),
                )],
                &[ID],
                &[ID],
            )
            .map(|mut v| v.remove(0))
        })
        .as_ref()
        .map_err(Clone::clone)?
        .validate(record)
        .map_err(|e| e.to_string())?;
    let b = &record["body"];
    if record["kind"] == "related_conversation" {
        if b["source"]["threadId"] == b["thread"]["threadId"]
            || b["source"]["generation"]["home"] != b["nativeHome"]["homeId"]
            || b["thread"]["generation"]["home"] != b["nativeHome"]["homeId"]
            || (b["relation"] == "forked from"
                && (b["rpc"]["method"] != "thread/fork"
                    || b["source"]["generation"] != b["thread"]["generation"]))
            || (b["relation"] == "continued from" && b["rpc"]["method"] != "thread/start")
        {
            return Err("native relationship endpoints/method/home disagree".into());
        }
    } else if b["originalObservationId"] == record["observationId"] {
        return Err("mechanical observation cannot reference itself".into());
    }
    Ok(())
}
fn valid_result(request: &SourceRequest, response: &Value) -> Result<(), String> {
    if !response.is_object()
        || response.get("id") != Some(request.request_id())
        || response.get("method").is_some()
        || response.get("error").is_some()
        || response.get("result").is_none()
    {
        return Err("native relationship response is uncorrelated or failed".into());
    }
    static VALIDATORS: OnceLock<Result<Vec<jsonschema::Validator>, String>> = OnceLock::new();
    let validators = VALIDATORS
        .get_or_init(|| {
            let schema: Value = serde_json::from_str(include_str!(
                "../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json"
            ))
            .map_err(|e| e.to_string())?;
            ["ThreadStartResponse", "ThreadForkResponse"]
                .iter()
                .map(|name| {
                    let mut s = schema.clone();
                    s["$ref"] = json!(format!("#/definitions/v2/{name}"));
                    jsonschema::options()
                        .offline()
                        .build(&s)
                        .map_err(|e| e.to_string())
                })
                .collect()
        })
        .as_ref()
        .map_err(Clone::clone)?;
    let fork = request.attempted_frame()["method"] == "thread/fork";
    validators[usize::from(fork)]
        .validate(&response["result"])
        .map_err(|e| format!("native relationship response shape invalid: {e}"))?;
    let id = &response["result"]["thread"]["id"];
    if id.as_str().is_none_or(str::is_empty)
        || (fork
            && (id == &request.attempted_frame()["params"]["threadId"]
                || response["result"]["thread"]["forkedFromId"]
                    != request.attempted_frame()["params"]["threadId"]))
    {
        return Err(
            "fork response does not identify a new conversation from the original source".into(),
        );
    }
    Ok(())
}
#[derive(Clone, PartialEq, Eq)]
struct Physical {
    path: PathBuf,
    device: u64,
    inode: u64,
}
impl Physical {
    fn capture(path: &Path) -> Result<Self, String> {
        let path = path.canonicalize().map_err(|e| e.to_string())?;
        crate::storage::check_path(&path)?;
        let m = std::fs::symlink_metadata(&path).map_err(|e| e.to_string())?;
        if !m.is_dir() {
            return Err("source is not a physical folder".into());
        }
        Ok(Self {
            path,
            device: m.dev(),
            inode: m.ino(),
        })
    }
    fn check(&self) -> Result<(), String> {
        if Self::capture(&self.path)? != *self {
            return Err(
                "frozen physical source changed; original observation cannot be reassociated"
                    .into(),
            );
        }
        Ok(())
    }
}
#[derive(Clone)]
struct Scope {
    project: Physical,
    store: Physical,
    dir: Physical,
    store_id: String,
    project_id: String,
}
impl Scope {
    fn capture(root: &Path) -> Result<Self, String> {
        let project = Physical::capture(root)?;
        let configured = crate::records_store::current()?;
        let store = Physical::capture(&configured.root)?;
        let identity: Value = serde_json::from_slice(&crate::records_retention::read_plain(
            &store.path.join("store.json"),
        )?)
        .map_err(|e| e.to_string())?;
        if identity["format"] != "chirality.records-store"
            || identity["formatVersion"] != "0.1"
            || identity["storeId"].as_str().is_none_or(str::is_empty)
        {
            return Err("original configured store identity unavailable".into());
        }
        let roots = administrative_lines(
            &store.path.join("roots.jsonl"),
            "chirality.records-store.root",
        )?;
        let mut active = BTreeMap::new();
        for row in roots {
            if row["projectId"].as_str().is_none_or(str::is_empty)
                || row["root"].as_str().is_none_or(str::is_empty)
                || !matches!(
                    row["how"].as_str(),
                    Some("minted" | "registered" | "adopted" | "released")
                )
            {
                return Err("original root association has unknown shape/transition".into());
            }
            active.insert(
                (
                    row["projectId"].as_str().unwrap().to_owned(),
                    row["root"].as_str().unwrap().to_owned(),
                ),
                row["how"] != "released",
            );
        }
        let here: Vec<_> = active
            .iter()
            .filter(|((_, root), on)| **on && root == project.path.to_str().unwrap_or(""))
            .map(|((id, _), _)| id.clone())
            .collect();
        if here.len() != 1
            || active.iter().any(|((id, root), on)| {
                *on && id == &here[0] && root != project.path.to_str().unwrap_or("")
            })
        {
            return Err("original source lacks one uniquely attached project identity".into());
        }
        // Check before the compatibility attachment route: a nonplain member
        // cannot make a new native observation wait on filesystem input.
        let link: Value = serde_json::from_slice(&crate::records_retention::read_plain(
            &project.path.join(crate::records_store::PROJECT_LINK),
        )?)
        .map_err(|_| "original project link is not JSON")?;
        if link["format"] != "chirality.project-link"
            || link["formatVersion"] != "0.1"
            || link["projectId"].as_str().is_none_or(str::is_empty)
            || link["storeId"].as_str().is_none_or(str::is_empty)
        {
            return Err("original project link has unsupported format/version or typed identity; no reassociation".into());
        }
        let attached = crate::records_store::attach(&project.path, false)?;
        if let Some(reason) = attached.refusal {
            return Err(reason);
        }
        let attached_dir = attached
            .dir
            .ok_or("no existing project/store association; recording context unavailable")?;
        crate::storage::check_path(&attached_dir)?;
        let dir = Physical::capture(&attached_dir)?;
        if dir.path != attached_dir {
            return Err("original attached payload is an alias; no reassociation".into());
        }
        let project_id = attached.project.ok_or("project identity unavailable")?;
        let payload_identity: Value =
            serde_json::from_slice(&read_log(&dir.path.join("project.json"))?)
                .map_err(|_| "protected payload project identity missing or not JSON")?;
        if payload_identity["format"] != "chirality.records-store.project"
            || payload_identity["formatVersion"] != "0.1"
            || payload_identity["projectId"] != project_id
            || project_id != here[0]
        {
            return Err("original protected payload project identity is unknown or inconsistent; no reassociation".into());
        }
        Ok(Self {
            project,
            store,
            dir,
            store_id: identity["storeId"].as_str().unwrap().into(),
            project_id,
        })
    }
    fn check(&self) -> Result<(), String> {
        self.project.check()?;
        self.store.check()?;
        self.dir.check()?;
        let fresh = Self::capture(&self.project.path)?;
        if fresh.store_id != self.store_id
            || fresh.project_id != self.project_id
            || fresh.dir != self.dir
            || fresh.store != self.store
        {
            return Err("original project/store association changed; no reassociation".into());
        }
        Ok(())
    }
}
/// Frozen before the native operation. Missing source facts are permanent
/// recording limits for that operation, never an invitation to bind later data.
#[derive(Clone)]
pub(crate) struct SourceContext {
    scope: Result<Scope, String>,
    native_home: Result<Value, String>,
    generation: Value,
    activity: Option<Arc<crate::storage::Ownership>>,
    custody_limit: Option<String>,
}
pub(crate) fn freeze_source(project: Option<&Path>, home: &HomeSession) -> SourceContext {
    let generation = home.host.snapshot()["generation"].clone();
    let native_home = (|| {
        crate::recovery::generation_ref(&generation)?;
        let config = home.host_config.as_ref().map_err(Clone::clone)?;
        let root = Physical::capture(&config.codex_home)?;
        Ok(
            json!({"homeId":generation["home"],"root":crate::attachments::native_path_identity(&root.path),"physical":{"device":root.device,"inode":root.inode}}),
        )
    })();
    let scope = project
        .ok_or_else(|| {
            "no explicit selected App project; native relation recording unavailable".into()
        })
        .and_then(Scope::capture)
        .and_then(|scope| {
            crate::records_retention::check_write(&scope.dir.path)?;
            Ok(scope)
        });
    let mut scope = scope;
    let activity = if native_home.is_ok() {
        match scope.as_ref() {
            Ok(source) => match crate::records_retention::activity(&source.project.path) {
                Ok(Some(lease)) => match source.check() {
                    Ok(()) => Some(Arc::new(lease)),
                    Err(e) => {
                        scope = Err(e);
                        None
                    }
                },
                Ok(None) => {
                    scope = Err("original project activity custody unavailable".into());
                    None
                }
                Err(e) => {
                    scope = Err(e);
                    None
                }
            },
            Err(_) => None,
        }
    } else {
        None
    };
    SourceContext {
        scope,
        activity,
        custody_limit: None,
        native_home,
        generation,
    }
}
struct Pending {
    context: SourceContext,
    record: Value,
    bytes: Vec<u8>,
    store_done: bool,
    project_done: bool,
    first_failure: [Option<String>; 2],
    events: Vec<Mechanical>,
    permanent: Option<String>,
}
struct Mechanical {
    record: Value,
    bytes: Vec<u8>,
    store_done: bool,
    project_done: bool,
    failure: Option<String>,
}
struct Attempt {
    context: SourceContext,
    host: Arc<Host>,
    request: SourceRequest,
    origin: Option<ContinuationSource>,
    fact: bool,
    limit: Option<String>,
}
#[derive(Default)]
pub(crate) struct Session {
    attempts: BTreeMap<String, Attempt>,
    facts: BTreeMap<String, Pending>,
    copies: BTreeMap<String, Pending>,
    completed_copies: std::collections::BTreeSet<String>,
    recovery_basis: Option<(
        Scope,
        Option<crate::records_index::Stamp>,
        Option<crate::records_index::Stamp>,
    )>,
    recovery_limit: Option<String>,
    limits: Vec<String>,
}
impl Session {
    pub(crate) fn has_pending(&self) -> bool {
        if self
            .attempts
            .values()
            .any(|a| !a.fact && a.context.activity.is_some())
        {
            return true;
        }
        self.facts.values().chain(self.copies.values()).any(|p| {
            p.permanent.is_none() && (!p.project_done || p.events.iter().any(|e| !e.project_done))
        })
    }
    pub(crate) fn track_fork(
        &mut self,
        context: SourceContext,
        host: Arc<Host>,
        request: SourceRequest,
    ) -> Result<Value, String> {
        let result = self.track(context, host, request, None);
        self.receiving(result)
    }
    fn receiving(&mut self, result: Result<Value, String>) -> Result<Value, String> {
        if let Err(reason) = &result {
            if !self.limits.contains(reason) {
                self.limits.push(reason.clone());
            }
        }
        result
    }
    pub(crate) fn track_continued(
        &mut self,
        context: SourceContext,
        host: Arc<Host>,
        request: SourceRequest,
        origin: ContinuationSource,
    ) -> Result<Value, String> {
        if !origin.belongs_to(&host) {
            return self.receiving(Err("Continue-as source belongs to another or unobserved actual native Host; no native relation tracked".into()));
        }
        let result = self.track(context, host, request, Some(origin));
        self.receiving(result)
    }
    fn track(
        &mut self,
        context: SourceContext,
        host: Arc<Host>,
        request: SourceRequest,
        origin: Option<ContinuationSource>,
    ) -> Result<Value, String> {
        host.source_request_status(&request)?;
        let method = if origin.is_some() {
            "thread/start"
        } else {
            "thread/fork"
        };
        if request.attempted_frame()["method"] != method
            || context.generation != *request.generation()
        {
            return Err(
                "original native receipt differs from frozen source/method; no reassociation"
                    .into(),
            );
        }
        self.attempts
            .entry(request.request_ref().to_owned())
            .or_insert(Attempt {
                context,
                host,
                request,
                origin,
                fact: false,
                limit: None,
            });
        self.progress();
        Ok(self.snapshot())
    }
    fn progress(&mut self) {
        let mut ready = Vec::new();
        for (key, attempt) in self.attempts.iter_mut().filter(|(_, a)| !a.fact) {
            let evidence = match attempt.host.source_request_status(&attempt.request) {
                Ok(e) => e,
                Err(e) => {
                    attempt.context.activity.take();
                    attempt.context.custody_limit = Some(
                        "original native source receipt unavailable; no fresh recording custody"
                            .into(),
                    );
                    attempt.limit = Some(e);
                    continue;
                }
            };
            if evidence["sourceCurrent"] == false
                && evidence["writeAttemptInProgress"] == false
                && evidence["response"].is_null()
            {
                attempt.context.activity.take();
                attempt.context.custody_limit=Some("original native source closed with outcome unknown; no relation or new recording reservation".into());
            }
            if evidence["outcome"] != "response-observed-result"
                || evidence["writeResult"] != "written"
            {
                if evidence["writeAttemptInProgress"] == false
                    && (evidence["outcome"] == "response-observed-error"
                        || evidence["writeResult"] == "write-failed"
                        || (evidence["actualWriteAttemptObserved"] == false
                            && !evidence["noAttemptCause"].is_null()))
                {
                    attempt.context.activity.take();
                    attempt.context.custody_limit=Some("original native request failed or was definitely not attempted; no new recording reservation".into());
                }
                attempt.limit=Some(format!("Native relationship is not known: {} (write {}, original source current {}). No relation fabricated or native request resent.",evidence["outcome"],evidence["writeResult"],evidence["sourceCurrent"]));
                continue;
            }
            if let Err(e) = valid_result(&attempt.request, &evidence["response"]) {
                attempt.context.activity.take();
                attempt.limit = Some(e);
                continue;
            }
            let origin = attempt
                .origin
                .as_ref()
                .map(|o| o.thread().to_owned())
                .or_else(|| {
                    attempt.request.attempted_frame()["params"]["threadId"]
                        .as_str()
                        .map(str::to_owned)
                });
            let Some(origin) = origin else {
                attempt.limit = Some("original source conversation absent".into());
                continue;
            };
            let origin_generation = attempt
                .origin
                .as_ref()
                .map(|o| o.generation().clone())
                .unwrap_or_else(|| attempt.request.generation().clone());
            let target = evidence["response"]["result"]["thread"]["id"]
                .as_str()
                .unwrap()
                .to_owned();
            ready.push((
                key.clone(),
                attempt.context.clone(),
                attempt.host.clone(),
                attempt.request.clone(),
                origin,
                origin_generation,
                target,
                attempt.origin.is_some(),
            ));
        }
        for (key, context, host, request, origin, generation, target, continued) in ready {
            match self.observe(
                context,
                &host,
                &request,
                if continued {
                    "continued from"
                } else {
                    "forked from"
                },
                &origin,
                &generation,
                &target,
            ) {
                Ok(_) => {
                    let a = self.attempts.get_mut(&key).unwrap();
                    a.fact = true;
                    a.context.activity.take();
                    a.limit = None;
                }
                Err(e) => self.attempts.get_mut(&key).unwrap().limit = Some(e),
            }
        }
    }
    fn observe(
        &mut self,
        context: SourceContext,
        host: &Host,
        request: &SourceRequest,
        relation: &str,
        origin: &str,
        origin_generation: &Value,
        target: &str,
    ) -> Result<Value, String> {
        let evidence = host.source_request_status(request)?;
        let method = if relation == "forked from" {
            "thread/fork"
        } else {
            "thread/start"
        };
        let response = &evidence["response"];
        if request.attempted_frame()["method"] != method
            || evidence["writeResult"] != "written"
            || evidence["outcome"] != "response-observed-result"
            || response.get("id") != Some(request.request_id())
            || response.get("error").is_some()
            || response["result"]["thread"]["id"] != target
            || origin.is_empty()
            || target.is_empty()
            || origin == target
        {
            return Err("native relationship lacks its original successful correlated request/result; no observation captured".into());
        }
        if relation == "forked from" && response["result"]["thread"]["forkedFromId"] != origin {
            return Err("fork did not report its original source".into());
        }
        crate::recovery::generation_ref(origin_generation)?;
        if context.generation != *request.generation()
            || origin_generation["home"] != request.generation()["home"]
        {
            return Err("frozen native source/generation differs; no relationship captured".into());
        }
        let key = serde_json::to_string(&json!([
            request.generation(),
            request.request_ref(),
            request.request_id(),
            method,
            origin_generation,
            origin,
            target
        ]))
        .map_err(|e| e.to_string())?;
        if !self.facts.contains_key(&key) {
            let record = json!({"format":"chirality.fleet.record","formatVersion":"0.2","observationId":crate::util::opaque_id("fl:app:")?,"kind":"related_conversation","recorder":{"kind":"App","identity":"app-writer:local"},"observedAt":crate::util::now_rfc3339(),"body":{"relation":relation,"source":{"threadId":origin,"generation":origin_generation},"thread":{"threadId":target,"generation":request.generation()},"nativeHome":context.native_home.as_ref().ok(),"rpc":{"method":method,"requestId":request.request_id(),"requestRef":request.request_ref()},"typesPin":crate::hosting::DECLARED_PIN}});
            let permanent = context
                .scope
                .as_ref()
                .err()
                .cloned()
                .or_else(|| context.native_home.as_ref().err().cloned())
                .or_else(|| context.custody_limit.clone());
            if permanent.is_none() {
                validate_record(&record)?;
            }
            let bytes = line(&record)?;
            self.facts.insert(
                key.clone(),
                Pending {
                    context,
                    record,
                    bytes,
                    store_done: false,
                    project_done: false,
                    first_failure: [None, None],
                    events: vec![],
                    permanent,
                },
            );
        }
        if let Some(p) = self.facts.get_mut(&key) {
            settle(p);
        }
        Ok(self.snapshot())
    }
    pub(crate) fn retry(&mut self, project: Option<&Path>) -> Value {
        self.progress();
        if let Some(project) = project {
            if let Err(reason) = self.recover(project) {
                self.recovery_limit = Some(reason);
            }
        }
        for fact in self.facts.values_mut().filter(|p| p.permanent.is_none()) {
            if project.is_some_and(|root| {
                fact.context
                    .scope
                    .as_ref()
                    .is_ok_and(|s| root.canonicalize().ok().as_ref() == Some(&s.project.path))
            }) {
                settle(fact);
            }
        }
        for copy in self.copies.values_mut() {
            if project.is_some_and(|root| {
                copy.context
                    .scope
                    .as_ref()
                    .is_ok_and(|s| root.canonicalize().ok().as_ref() == Some(&s.project.path))
            }) {
                settle(copy);
            }
        }
        let complete: Vec<_> = self
            .copies
            .iter()
            .filter(|(_, p)| {
                p.store_done
                    && p.project_done
                    && p.events.iter().all(|e| e.store_done && e.project_done)
            })
            .map(|(key, _)| key.clone())
            .collect();
        for key in complete {
            if let Some(copy) = self.copies.remove(&key) {
                self.completed_copies
                    .insert(copy.record["observationId"].as_str().unwrap().to_owned());
            }
        }
        self.snapshot()
    }
    fn recover(&mut self, project: &Path) -> Result<(), String> {
        let scope = Scope::capture(project)?;
        // Closure cannot create a new cold W2 copy obligation. Previously
        // owed facts stay separate and keep their original recording context.
        crate::records_retention::check_write(&scope.dir.path)?;
        if crate::records_retention::terminal(&scope.dir.path)? {
            return Err(
                "native link copy recovery unavailable: project disposed or disposal incomplete"
                    .into(),
            );
        }
        let source = published_at(&scope, 0);
        let dest = published_at(&scope, 1);
        let stamp = |path: &Path| -> Result<Option<crate::records_index::Stamp>, String> {
            crate::storage::check_path(path)?;
            match std::fs::symlink_metadata(path) {
                Ok(m) if m.is_file() && m.nlink() == 1 => {
                    Ok(Some(crate::records_index::Stamp::of(&m)))
                }
                Ok(_) => Err("Fleet recovery source not a single-link regular file".into()),
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(None),
                Err(e) => Err(e.to_string()),
            }
        };
        let (before, project_before) = (stamp(&source)?, stamp(&dest)?);
        if self.recovery_basis.as_ref().is_some_and(|(basis, a, b)| {
            basis.project == scope.project
                && basis.store == scope.store
                && basis.dir == scope.dir
                && basis.store_id == scope.store_id
                && basis.project_id == scope.project_id
                && a == &before
                && b == &project_before
        }) {
            return Ok(());
        }
        let original = read_log(&source)?;
        let stored = rows(&original, true)?;
        let project_bytes = read_log(&dest)?;
        rows(&project_bytes, false)?;
        if stamp(&source)? != before {
            return Err("governing Fleet changed during recovery; no copies adopted".into());
        }
        scope.check()?;
        accept_prefix(&scope, &original, 0)?;
        if stamp(&dest)? != project_before {
            return Err("co-written Fleet changed during recovery; no copies adopted".into());
        }
        accept_prefix(&scope, &project_bytes, 1)?;
        let mut phases: BTreeMap<(String, usize), Option<String>> = BTreeMap::new();
        for (row, _) in &stored {
            if row["formatVersion"] == "0.2"
                && ["recording_limit", "recording_recovered"]
                    .contains(&row["kind"].as_str().unwrap_or(""))
            {
                let key = (
                    row["body"]["originalObservationId"]
                        .as_str()
                        .unwrap()
                        .to_owned(),
                    usize::from(row["body"]["phase"] == "project"),
                );
                phases.insert(
                    key,
                    if row["kind"] == "recording_limit" {
                        Some(row["body"]["statement"].as_str().unwrap().to_owned())
                    } else {
                        None
                    },
                );
            }
        }
        for (record, bytes) in stored
            .into_iter()
            .filter(|(r, _)| r["formatVersion"] == "0.2")
        {
            let key = format!(
                "{}:{}:{}",
                scope.store_id,
                scope.project_id,
                record["observationId"].as_str().unwrap()
            );
            if self
                .facts
                .values()
                .any(|p| p.record["observationId"] == record["observationId"])
            {
                continue;
            }
            let phase_failure = |phase| {
                phases
                    .get(&(record["observationId"].as_str().unwrap().to_owned(), phase))
                    .cloned()
                    .flatten()
            };
            let failures = if record["kind"] == "related_conversation" {
                [phase_failure(0), phase_failure(1)]
            } else {
                [None, None]
            };
            if failures.iter().all(Option::is_none)
                && project_bytes
                    .split_inclusive(|b| *b == b'\n')
                    .filter(|line| *line == bytes.as_slice())
                    .count()
                    == 1
            {
                continue;
            }
            if self.copies.contains_key(&key) {
                continue;
            }
            let activity = Arc::new(
                crate::records_retention::activity(&scope.project.path)?
                    .ok_or("original cold copy activity custody unavailable")?,
            );
            scope.check()?;
            self.copies.insert(
                key,
                Pending {
                    context: SourceContext {
                        scope: Ok(scope.clone()),
                        native_home: Err("quoted stored line; no cold native source proof".into()),
                        generation: Value::Null,
                        activity: Some(activity),
                        custody_limit: None,
                    },
                    record,
                    bytes,
                    store_done: failures[0].is_none(),
                    project_done: false,
                    first_failure: failures,
                    events: vec![],
                    permanent: None,
                },
            );
        }
        self.recovery_basis = Some((scope, before, project_before));
        self.recovery_limit = None;
        Ok(())
    }
    pub(crate) fn snapshot(&self) -> Value {
        json!({"nativeAttempts":self.attempts.values().map(|a|json!({"generation":a.request.generation(),"requestId":a.request.request_id(),"requestRef":a.request.request_ref(),"method":a.request.attempted_frame()["method"],"factObserved":a.fact,"limit":a.limit})).collect::<Vec<_>>(),"observations":self.facts.values().map(|p|json!({"observation":if p.context.native_home.is_ok(){Some(&p.record)}else{None},"unrecordedSourceLimitedFact":if p.context.native_home.is_err(){Some(json!({"observationId":p.record["observationId"],"observedAt":p.record["observedAt"],"nativeResult":p.record["body"],"limit":p.context.native_home.as_ref().err()}))}else{None},"storeRecorded":p.store_done,"projectCopied":p.project_done,"permanentRecordingLimit":p.permanent,"firstFailures":p.first_failure,"recordingEvents":p.events.iter().map(|e|json!({"record":e.record,"storeRecorded":e.store_done,"projectCopied":e.project_done,"limit":e.failure})).collect::<Vec<_>>()})).collect::<Vec<_>>(),"quotedCopyRecovery":{"standing":"Existing stored exact lines only; no cold native observation or authority minted","limit":self.recovery_limit,"completedCopies":self.completed_copies,"copies":self.copies.values().map(|p|json!({"observationId":p.record["observationId"],"storeRecorded":p.store_done,"projectCopied":p.project_done,"firstFailures":p.first_failure,"recordingEvents":p.events.iter().map(|e|json!({"record":e.record,"storeRecorded":e.store_done,"projectCopied":e.project_done,"limit":e.failure})).collect::<Vec<_>>()})).collect::<Vec<_>>()},"pending":self.has_pending(),"limits":self.limits,"standing":"Observed native conversation relationships; recording status is separate from native operation success. No role, workflow, dispatch or work state is restored or derived."})
    }
}
fn line(v: &Value) -> Result<Vec<u8>, String> {
    let mut bytes = serde_json::to_vec(v).map_err(|e| e.to_string())?;
    bytes.push(b'\n');
    Ok(bytes)
}
fn mechanical(
    p: &Pending,
    phase: usize,
    kind: &str,
    statement: String,
) -> Result<Mechanical, String> {
    let record = json!({"format":"chirality.fleet.record","formatVersion":"0.2","observationId":crate::util::opaque_id("fl:app:")?,"kind":kind,"recorder":{"kind":"App","identity":"app-writer:local"},"observedAt":crate::util::now_rfc3339(),"body":{"originalObservationId":p.record["observationId"],"phase":if phase==0{"store"}else{"project"},"statement":statement}});
    validate_record(&record)?;
    Ok(Mechanical {
        bytes: line(&record)?,
        record,
        store_done: false,
        project_done: false,
        failure: None,
    })
}
fn settle(p: &mut Pending) {
    if p.permanent.is_some() {
        p.context.activity.take();
        return;
    }
    let Some(scope) = p.context.scope.as_ref().ok() else {
        return;
    };
    let scope = scope.clone();
    for phase in 0..2 {
        if (phase == 0 && p.store_done) || (phase == 1 && p.project_done) {
            continue;
        }
        match publish(&scope, &p.record, &p.bytes, phase) {
            Ok(()) => {
                if phase == 0 {
                    p.store_done = true
                } else {
                    p.project_done = true
                };
                if p.first_failure[phase].is_some() && p.record["kind"] == "related_conversation" {
                    match mechanical(p,phase,"recording_recovered","The exact original line is now proved present and synced; the earlier failed/unconfirmed callback is not changed to success.".into()){Ok(e)=>p.events.push(e),Err(reason)=>p.first_failure[phase]=Some(reason)}
                }
            }
            Err(reason) => {
                if p.first_failure[phase].is_none() {
                    p.first_failure[phase] = Some(reason.clone());
                    if p.record["kind"] == "related_conversation" {
                        if let Ok(event)=mechanical(p,phase,"recording_limit",format!("Original recording callback failed or was unconfirmed: {reason}. Native operation outcome remains as originally observed.")){p.events.push(event);}
                    }
                }
                break;
            }
        }
    }
    for event in &mut p.events {
        if !event.store_done {
            match publish_bound(
                &scope,
                &event.record,
                &event.bytes,
                0,
                Some((&p.record, &p.bytes)),
            ) {
                Ok(()) => event.store_done = true,
                Err(e) => {
                    event.failure = Some(e);
                    continue;
                }
            }
        }
        if !event.project_done {
            match publish_bound(
                &scope,
                &event.record,
                &event.bytes,
                1,
                Some((&p.record, &p.bytes)),
            ) {
                Ok(()) => {
                    event.project_done = true;
                    event.failure = None
                }
                Err(e) => event.failure = Some(e),
            }
        }
    }
    if p.store_done && p.project_done && p.events.iter().all(|e| e.store_done && e.project_done) {
        p.context.activity.take();
    }
}
#[derive(Clone, Ord, PartialOrd, Eq, PartialEq)]
struct ProjectPrefix {
    project: PathBuf,
    store_id: String,
    project_id: String,
}
static PROJECT_PREFIXES: LazyLock<Mutex<BTreeMap<ProjectPrefix, (usize, String)>>> =
    LazyLock::new(|| Mutex::new(BTreeMap::new()));
fn accept_prefix(scope: &Scope, bytes: &[u8], phase: usize) -> Result<(), String> {
    if phase == 0 {
        return crate::fleet_records::writer_prefix(
            &scope.project.path,
            &scope.store.path,
            &scope.store_id,
            &scope.project_id,
            &scope.dir.path,
            bytes,
        );
    }
    let key = ProjectPrefix {
        project: scope.project.path.clone(),
        store_id: scope.store_id.clone(),
        project_id: scope.project_id.clone(),
    };
    let mut known = PROJECT_PREFIXES.lock().unwrap_or_else(|p| p.into_inner());
    if let Some((length, digest)) = known.get(&key) {
        if !bytes
            .get(..*length)
            .is_some_and(|prefix| crate::util::sha256_hex(prefix) == *digest)
        {
            return Err("previously accepted co-written Fleet prefix changed/disappeared; original copy remains pending".into());
        }
    }
    if known
        .get(&key)
        .is_none_or(|(length, _)| bytes.len() > *length)
    {
        known.insert(key, (bytes.len(), crate::util::sha256_hex(bytes)));
    }
    Ok(())
}
fn opened_at(parent: &std::fs::File, name: &str, flags: i32) -> Result<std::fs::File, String> {
    use std::os::fd::{AsRawFd, FromRawFd};
    let name = std::ffi::CString::new(name).map_err(|e| e.to_string())?;
    let fd = unsafe {
        libc::openat(
            parent.as_raw_fd(),
            name.as_ptr(),
            flags | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC,
            0o600,
        )
    };
    if fd < 0 {
        return Err(std::io::Error::last_os_error().to_string());
    }
    Ok(unsafe { std::fs::File::from_raw_fd(fd) })
}
fn child(parent: &std::fs::File, name: &str) -> Result<std::fs::File, String> {
    use std::os::fd::AsRawFd;
    let name_c = std::ffi::CString::new(name).map_err(|e| e.to_string())?;
    if unsafe { libc::mkdirat(parent.as_raw_fd(), name_c.as_ptr(), 0o700) } != 0
        && std::io::Error::last_os_error().kind() != std::io::ErrorKind::AlreadyExists
    {
        return Err(std::io::Error::last_os_error().to_string());
    }
    let dir = opened_at(parent, name, libc::O_RDONLY | libc::O_DIRECTORY)?;
    dir.sync_all()
        .and_then(|()| parent.sync_all())
        .map_err(|e| e.to_string())?;
    Ok(dir)
}
fn plain(file: &std::fs::File) -> Result<crate::records_index::Stamp, String> {
    let m = file.metadata().map_err(|e| e.to_string())?;
    if !m.is_file() || m.nlink() != 1 {
        return Err("Fleet log is not a single-link regular file".into());
    }
    Ok(crate::records_index::Stamp::of(&m))
}
fn read_log(path: &Path) -> Result<Vec<u8>, String> {
    use std::io::Read;
    let expected = match std::fs::symlink_metadata(path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            crate::storage::check_path(path)?;
            return Ok(vec![]);
        }
        Err(e) => return Err(e.to_string()),
        Ok(m) if !m.is_file() || m.nlink() != 1 => {
            return Err("Fleet source not a single-link regular file".into())
        }
        Ok(m) => crate::records_index::Stamp::of(&m),
    };
    let mut file = crate::records_index::open_log(path).map_err(|e| e.to_string())?;
    let before = plain(&file)?;
    if before != expected {
        return Err("Fleet descriptor differs from checked source".into());
    }
    let mut bytes = vec![];
    file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
    let current = crate::records_index::open_log(path).map_err(|e| e.to_string())?;
    if plain(&file)? != before || plain(&current)? != before {
        return Err("Fleet source changed while reading".into());
    }
    Ok(bytes)
}
fn administrative_lines(path: &Path, format: &str) -> Result<Vec<Value>, String> {
    let bytes = read_log(path)?;
    if !bytes.is_empty() && !bytes.ends_with(b"\n") {
        return Err("original association/import source has an unclosed final line; no new Fleet publication".into());
    }
    bytes
        .split_inclusive(|b| *b == b'\n')
        .map(|line| {
            let row: Value = serde_json::from_slice(line)
                .map_err(|_| "original association/import source is not JSON")?;
            if row["format"] != format || row["formatVersion"] != "0.1" {
                return Err("original association/import format is unknown".into());
            }
            Ok(row)
        })
        .collect()
}
fn check_import_source(dir: &Path) -> Result<(), String> {
    for row in administrative_lines(&dir.join("imports.jsonl"), "chirality.records-store.import")? {
        if row["importId"].as_str().is_none_or(str::is_empty)
            || !matches!(row["event"].as_str(), Some("started" | "completed"))
            || (row["event"] == "completed"
                && (!row["files"].is_array() || !row["conflicts"].is_array()))
        {
            return Err(
                "original project import state is unknown; Fleet publication withheld".into(),
            );
        }
    }
    Ok(())
}
fn rows(bytes: &[u8], protected: bool) -> Result<Vec<(Value, Vec<u8>)>, String> {
    if !bytes.is_empty() && !bytes.ends_with(b"\n") {
        return Err("Fleet has an unclosed final line; no automatic repair or truncation".into());
    }
    let mut out = vec![];
    let mut ids = std::collections::BTreeSet::new();
    let mut receipts = std::collections::BTreeSet::new();
    for bytes in bytes.split_inclusive(|b| *b == b'\n') {
        let row = crate::fleet_records::validate_line(bytes)?;
        let id = row["observationId"]
            .as_str()
            .or_else(|| row["recordId"].as_str())
            .ok_or("Fleet identity absent")?;
        if !ids.insert(id.to_owned()) {
            return Err(
                "Fleet contains duplicate/conflicting observation identity; no copy chosen".into(),
            );
        }
        if protected
            && (row["recorder"]["kind"] != "App"
                || ![
                    "dispatch_observed",
                    "child_observed",
                    "observation_ended",
                    "related_conversation",
                    "recording_limit",
                    "recording_recovered",
                ]
                .contains(&row["kind"].as_str().unwrap_or("")))
        {
            return Err("protected Fleet source includes non-App/non-observation rows".into());
        }
        if row["formatVersion"] == "0.2"
            && row["kind"] == "related_conversation"
            && !receipts.insert(receipt_key(&row)?)
        {
            return Err("Fleet has duplicate/conflicting original native request relationship; no copy chosen".into());
        }
        out.push((row, bytes.to_vec()));
    }
    Ok(out)
}
pub(crate) fn receipt_key(record: &Value) -> Result<String, String> {
    let b = &record["body"];
    serde_json::to_string(&json!([
        b["nativeHome"],
        b["thread"]["generation"],
        b["rpc"]
    ]))
    .map_err(|e| e.to_string())
}
fn published_at(scope: &Scope, phase: usize) -> PathBuf {
    if phase == 0 {
        scope.dir.path.join("fleet").join(LOG)
    } else {
        scope.project.path.join(".chirality/fleet").join(LOG)
    }
}
#[cfg(test)]
thread_local! {static BEFORE_APPEND:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};static FAIL_AFTER_WRITE:std::cell::Cell<Option<usize>>=const{std::cell::Cell::new(None)};}
fn publish(scope: &Scope, record: &Value, bytes: &[u8], phase: usize) -> Result<(), String> {
    publish_bound(scope, record, bytes, phase, None)
}
fn publish_bound(
    scope: &Scope,
    record: &Value,
    bytes: &[u8],
    phase: usize,
    origin: Option<(&Value, &[u8])>,
) -> Result<(), String> {
    use std::io::Write;
    scope.check()?;
    validate_record(record)?;
    let _admission = crate::records_retention::write_path(&scope.dir.path)?;
    check_import_source(&scope.dir.path)?;
    let dir = crate::records_store::write_dir(&scope.project.path)?;
    if dir != scope.dir.path {
        return Err("original store project changed; no reassociation".into());
    }
    let _writer = crate::records_store::writer_lock(&dir, false)?;
    check_import_source(&dir)?;
    scope.check()?;
    // The project side is never first and never gets bytes absent from the
    // healthy governing source, including on cold copy recovery.
    let governing = if phase == 1 {
        let path = published_at(scope, 0);
        let parent = crate::records_index::open_directory(path.parent().unwrap())
            .map_err(|e| e.to_string())?;
        let leaf = crate::records_index::open_log(&path).map_err(|e| e.to_string())?;
        let stamp = plain(&leaf)?;
        let source = read_log(&published_at(scope, 0))?;
        rows(&source, true)?;
        accept_prefix(scope, &source, 0)?;
        if source
            .split_inclusive(|b| *b == b'\n')
            .filter(|line| *line == bytes)
            .count()
            != 1
        {
            return Err(
                "exact original line unavailable in governing Fleet store; project copy withheld"
                    .into(),
            );
        }
        if plain(&leaf)? != stamp {
            return Err("governing Fleet changed before project copy".into());
        }
        Some((parent, leaf, stamp))
    } else {
        None
    };
    let path = published_at(scope, phase);
    let base = if phase == 0 {
        &scope.dir.path
    } else {
        &scope.project.path
    };
    let owner = crate::records_index::open_directory(base).map_err(|e| e.to_string())?;
    let intermediate = if phase == 1 {
        Some(child(&owner, ".chirality")?)
    } else {
        None
    };
    let folder = child(intermediate.as_ref().unwrap_or(&owner), "fleet")?;
    let folder_path = path.parent().unwrap();
    let current_folder =
        crate::records_index::open_directory(folder_path).map_err(|e| e.to_string())?;
    let folder_meta = folder.metadata().map_err(|e| e.to_string())?;
    let same_inode =
        |a: &std::fs::Metadata, b: &std::fs::Metadata| a.dev() == b.dev() && a.ino() == b.ino();
    if !same_inode(
        &folder_meta,
        &current_folder.metadata().map_err(|e| e.to_string())?,
    ) {
        return Err("Fleet folder replaced before publication".into());
    }
    let original = read_log(&path)?;
    let prior = rows(&original, phase == 0)?;
    accept_prefix(scope, &original, phase)?;
    if let Some((original, expected)) = origin {
        if prior.iter().any(|(r, line)| {
            r["observationId"] == original["observationId"] && line.as_slice() != expected
        }) {
            return Err(
                "original fact identity conflicts; no mechanical logger append possible".into(),
            );
        }
    }
    let id = &record["observationId"];
    let duplicate = prior.iter().find(|(row, _)| row["observationId"] == *id);
    if duplicate.is_some_and(|(_, line)| line.as_slice() != bytes) {
        return Err("original observation identity conflicts with stored bytes".into());
    }
    if record["kind"] == "related_conversation"
        && prior.iter().any(|(row, line)| {
            row["formatVersion"] == "0.2"
                && row["kind"] == "related_conversation"
                && receipt_key(row).ok() == receipt_key(record).ok()
                && line.as_slice() != bytes
        })
    {
        return Err("original native receipt already has another frozen relation line; no remint or copy chosen".into());
    }
    let mut file = opened_at(&folder, LOG, libc::O_RDWR | libc::O_APPEND | libc::O_CREAT)?;
    let before = plain(&file)?;
    if file.metadata().map_err(|e| e.to_string())?.len() != original.len() as u64 {
        return Err("Fleet source length changed before publication".into());
    }
    #[cfg(test)]
    BEFORE_APPEND.with(|h| {
        if let Some(h) = h.borrow_mut().take() {
            h();
        }
    });
    scope.check()?;
    let current_folder =
        crate::records_index::open_directory(folder_path).map_err(|e| e.to_string())?;
    if !same_inode(
        &folder_meta,
        &current_folder.metadata().map_err(|e| e.to_string())?,
    ) {
        return Err("Fleet parent association changed before append".into());
    }
    check_import_source(&dir)?;
    let recheck = crate::records_index::open_log(&path).map_err(|e| e.to_string())?;
    if plain(&recheck)? != before || read_log(&path)? != original {
        return Err("Fleet source replaced/changed before append".into());
    }
    if duplicate.is_none() {
        file.write_all(bytes)
            .map_err(|e| format!("Fleet append failed/unconfirmed: {e}"))?;
    }
    #[cfg(test)]
    if FAIL_AFTER_WRITE.with(|f| f.get() == Some(phase)) {
        return Err("injected visible append with unconfirmed sync".into());
    }
    file.sync_all()
        .map_err(|e| format!("Fleet file sync uncertain: {e}"))?;
    folder
        .sync_all()
        .map_err(|e| format!("Fleet folder sync uncertain: {e}"))?;
    if let Some(intermediate) = intermediate {
        intermediate.sync_all().map_err(|e| e.to_string())?;
    }
    owner.sync_all().map_err(|e| e.to_string())?;
    // Re-establish every surviving ancestor link even after an earlier failed
    // creation/sync. These folders already exist, so this creates nothing.
    for parent in base.ancestors() {
        crate::records_index::open_directory(parent)
            .map_err(|e| e.to_string())?
            .sync_all()
            .map_err(|e| e.to_string())?;
        if parent == scope.store.path || phase == 1 {
            break;
        }
    }
    scope.check()?;
    let current_folder =
        crate::records_index::open_directory(folder_path).map_err(|e| e.to_string())?;
    if !same_inode(
        &folder_meta,
        &current_folder.metadata().map_err(|e| e.to_string())?,
    ) {
        return Err(
            "Fleet parent association changed after append; publication unconfirmed".into(),
        );
    }
    if let Some((parent, leaf, stamp)) = governing {
        let path = published_at(scope, 0);
        let current_parent = crate::records_index::open_directory(path.parent().unwrap())
            .map_err(|e| e.to_string())?;
        let current_leaf = crate::records_index::open_log(&path).map_err(|e| e.to_string())?;
        if !same_inode(
            &parent.metadata().map_err(|e| e.to_string())?,
            &current_parent.metadata().map_err(|e| e.to_string())?,
        ) || plain(&leaf)? != stamp
            || plain(&current_leaf)? != stamp
        {
            return Err(
                "governing Fleet changed during project copy; publication unconfirmed".into(),
            );
        }
    }
    let current = crate::records_index::open_log(&path).map_err(|e| e.to_string())?;
    if plain(&current)? != plain(&file)? {
        return Err("Fleet leaf changed after append; publication unconfirmed".into());
    }
    let mut expected = original;
    if duplicate.is_none() {
        expected.extend_from_slice(bytes);
    }
    if read_log(&path)? != expected {
        return Err("Fleet bytes changed during publication; original receipt retained".into());
    }
    accept_prefix(scope, &expected, phase)?;
    Ok(())
}

#[cfg(test)]
#[path = "native_conversation_links_tests.rs"]
mod tests;
