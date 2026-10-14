//! Current ROLE→RS receiving. Only bound, confirmed hot publication mints the
//! private receipt. File resolution returns quoted values, never this receipt.
use super::*;
use std::sync::Arc;
const CONTEXT_SCHEMA: &str =
    include_str!("../resources/workflow_role/role-run-context.schema.json");
#[cfg(test)]
thread_local! {pub(crate) static FAIL_CONTEXT_AFTER_FILE_SYNC:std::cell::Cell<bool>=const {std::cell::Cell::new(false)};}
const CONTEXT_STANDING:&str="App observation of the original run start; unsigned file provenance is unverified; no current native authority restored";
const LIMIT_SCHEMA: &str =
    include_str!("../resources/workflow_role/role-limit-observation.schema.json");
pub(super) fn validate_limit(value: &Value) -> Result<(), String> {
    static V: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
    V.get_or_init(|| {
        jsonschema::options()
            .offline()
            .build(&serde_json::from_str::<Value>(LIMIT_SCHEMA).map_err(|e| e.to_string())?)
            .map_err(|e| e.to_string())
    })
    .as_ref()
    .map_err(Clone::clone)?
    .validate(value)
    .map_err(|e| e.to_string())
}
fn validate_context(value: &Value) -> Result<(), String> {
    static V: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
    V.get_or_init(|| {
        jsonschema::options()
            .offline()
            .build(&serde_json::from_str::<Value>(CONTEXT_SCHEMA).map_err(|e| e.to_string())?)
            .map_err(|e| e.to_string())
    })
    .as_ref()
    .map_err(Clone::clone)?
    .validate(value)
    .map_err(|e| e.to_string())
}
/// The original private role/run join plus its immutable context bytes. No file
/// parser constructs it; an original unconfirmed write may retry these bytes.
#[derive(Debug)]
pub(crate) struct PreparedRoleRunSupply {
    source: Arc<PublishedRoleSupply>,
    context: Vec<u8>,
    payload: Value,
}
impl PreparedRoleRunSupply {
    pub(crate) fn publish_or_verify(&self, project: &Path) -> Result<(), String> {
        self.source.verify(project)?;
        {
            let owner = &self.source.owner;
            let _owner = owner
                .writer
                .lock()
                .map_err(|_| "role context writer owner unavailable")?;
            let Some((path, folder, _admission, _writer)) = owner.location(true)? else {
                return Err("role context store unavailable".into());
            };
            if path != self.source.basis.path || identity(&folder)? != self.source.basis.folder {
                return Err("original role context folder changed".into());
            }
            let content =
                child(&folder, "content", true)?.ok_or("role context content unavailable")?;
            let (reference, file) = RoleLog::publish_bytes(&content, &self.context)?;
            #[cfg(test)]
            if FAIL_CONTEXT_AFTER_FILE_SYNC.with(|f| f.replace(false)) {
                return Err(
                    "injected role-run context publication unconfirmed after file flush".into(),
                );
            }
            if reference != self.payload {
                return Err("original role context identity changed".into());
            }
            RoleLog::verify_content(&folder, &content, &[(reference, file)])?;
            owner.check_project()?;
            verify_directory(&path, &folder)?;
        }
        self.source.verify(project)
    }
}
// This identifies the App JSON body value, not the original log-line bytes.
// Source/payload identities continue to hash the exact bytes actually retained.
fn body_identity(body: &Value) -> Result<Value, String> {
    Ok(
        json!({"method":"chirality.app.rs.body-json.sha256/v1","value":crate::util::sha256_hex(&serde_json::to_vec(body).map_err(|e|e.to_string())?)}),
    )
}
fn source_ref<R: std::borrow::Borrow<Value>>(project: &str, rows: &[R]) -> String {
    format!(
        "role-record:v1:{}",
        json!([
            project,
            rows.iter()
                .map(|r| std::borrow::Borrow::<Value>::borrow(r)["observationId"].clone())
                .collect::<Vec<_>>()
        ])
    )
}
fn limit_ref(project: &str, source: &Value) -> Result<String, String> {
    Ok(format!(
        "role-limit:v1:{}",
        json!([
            project,
            payload_key(&source["appBytes"]["limitAccount"]["content"])?
        ])
    ))
}
/// Deliberately no Deserialize or public constructor. The original admitted
/// binding and confirmed named-file publication are required to mint it.
#[derive(Debug)]
pub(crate) struct PublishedRoleSupply {
    owner: Arc<RoleLog>,
    basis: PublicationBasis,
    rows: Vec<Arc<Value>>,
    reference: String,
    limit_reference: String,
    content: Value,
}
impl PublishedRoleSupply {
    pub(crate) fn home(&self) -> &str {
        self.rows[0]["request"]["home"].as_str().unwrap()
    }
    pub(crate) fn thread(&self) -> &str {
        self.rows[0]["thread"].as_str().unwrap()
    }
    pub(crate) fn supply_id(&self) -> &str {
        self.rows[0]["supplyId"].as_str().unwrap()
    }
    pub(crate) fn role(&self) -> &str {
        self.rows[0]["selection"]["role"].as_str().unwrap()
    }
    pub(crate) fn verify(&self, project: &Path) -> Result<(), String> {
        if project != self.owner.project {
            return Err("original role publication belongs to another App project".into());
        }
        let Some((path, folder, _admission, _writer)) = self.owner.location(false)? else {
            return Err("original role publication store unavailable".into());
        };
        let file = open_at(&folder, LOG, libc::O_RDONLY)?;
        plain(&file)?;
        if path != self.basis.path
            || identity(&folder)? != self.basis.folder
            || identity(&file)? != self.basis.log
        {
            return Err("original role publication physical log/folder was replaced".into());
        }
        let (rows, _chain, _basis) = RoleLog::read_lines(&folder, &path)?;
        for held in &self.rows {
            unique_success(&rows, held)?;
            if rows
                .iter()
                .filter(|r| r["observationId"] == held["observationId"])
                .count()
                != 1
                || !rows.iter().any(|r| r == held.as_ref())
            {
                return Err("original role publication row changed or became ambiguous".into());
            }
        }
        let source = self.rows.last().ok_or("role source absent")?;
        let content =
            child(&folder, "content", false)?.ok_or("original role source payload unavailable")?;
        checked_sources(&content, source)?;
        verify_directory_child(&folder, "content", &content)?;
        self.owner.check_project()?;
        verify_directory(&path, &folder)?;
        verify_leaf(&folder, LOG, &file)
    }
    pub(crate) fn reference(&self) -> &str {
        &self.reference
    }
    pub(crate) fn verify_target(
        &self,
        project: &Path,
        home: &str,
        thread: &str,
    ) -> Result<(), String> {
        if home != self.home() || thread != self.thread() {
            return Err("role receipt belongs to another native home/thread".into());
        }
        self.verify(project)
    }
    #[allow(clippy::too_many_arguments)]
    pub(crate) fn prepare_run(
        self: &Arc<Self>,
        project: &crate::workflow_workspace::publication::ProjectRecords,
        published: &crate::workflow_workspace::publication::PublishedRunText,
        host: &crate::hosting::Host,
        native: &crate::hosting::SourceRequest,
        opened: &crate::records::supply::PendingRunEntry,
        person_text: &str,
        client: &str,
        native_turn: &str,
    ) -> Result<
        (
            crate::records::supply::PendingRunEntry,
            PreparedRoleRunSupply,
        ),
        String,
    > {
        let scope = published.prepared().scope();
        self.verify_target(project.root(), &scope.home, &scope.conversation)?;
        let status = host.source_request_status(native)?;
        if status["home"] != scope.home
            || status["generation"] != scope.generation
            || status["sentFrame"]["method"] != "turn/start"
            || status["writeResult"] != "written"
            || status["outcome"] != "response-observed-result"
            || status["sentFrame"]["params"]
                != published.prepared().turn_params(person_text, client)?
            || status["response"]["result"]["turn"]["id"] != native_turn
            || opened.kind != "run_opened"
            || opened.body["runId"] != scope.run
            || opened.body["conversationRef"] != scope.conversation
        {
            return Err(
                "role R3 run context differs from actual private run-start source/scope".into(),
            );
        }
        let project_id = self.rows[0]["project"]["projectId"].as_str().unwrap();
        let context = json!({"format":"chirality.role.run.context","formatVersion":"0.1","projectId":project_id,
            "run":scope.run,"writer":crate::records::supply::LIVE_WRITER,"home":scope.home,"thread":scope.conversation,"generation":scope.generation,
            "requestRef":status["requestRef"],"requestIdentity":status["requestIdentity"],"requestMethod":"turn/start","writeResult":status["writeResult"],"outcome":status["outcome"],"sourceCurrent":status["sourceCurrent"],
            "nativeTurn":native_turn,"observedTurnStatus":status["response"]["result"]["turn"]["status"],"roleSource":self.reference,"limitAccount":self.limit_reference,
            "runText":published.run_text_record().reference(),"selectionRecord":published.selection_record().reference(),
            "opened":{"recordId":opened.record_id,"content":body_identity(&opened.body)?,"observedAt":opened.observed_at},
            "scope":{"sourceRoot":scope.source_root,"holdingLibrary":scope.holding_library,"selectionRef":scope.selection_ref,"revisionStore":crate::attachments::native_path_identity(&scope.revision_store)},"standing":CONTEXT_STANDING});
        validate_context(&context)?;
        let bytes = serde_json::to_vec(&context).map_err(|e| e.to_string())?;
        let payload = json!({"content":role_supply::content(&bytes),"byteLength":bytes.len()});
        let reference = format!(
            "role-run:v1:{}",
            json!([
                project_id,
                self.rows
                    .iter()
                    .map(|r| r["observationId"].clone())
                    .collect::<Vec<_>>(),
                payload
            ])
        );
        let entry = crate::records::supply::PendingRunEntry::new(
            "supplied_guidance",
            json!({
                "supplyForm":if self.rows[0]["trigger"]=="fork"{"role guidance inherited at fork"}else{"role guidance at conversation start"},
                "thread":scope.conversation,"sourceIdentity":self.reference,"content":self.content,
                "supplyRecord":{"kind":"supply record","ref":reference,"resolutionAtWrite":"resolved"},
                "limitAccount":{"kind":"limit account","ref":self.limit_reference,"resolutionAtWrite":"resolved"},"adoption":"unknown"
            }),
            opened.observed_at.clone(),
        )?;
        Ok((
            entry,
            PreparedRoleRunSupply {
                source: self.clone(),
                context: bytes,
                payload,
            },
        ))
    }
}
impl RoleLog {
    pub(crate) fn publish_bound(
        self: &Arc<Self>,
        row: Value,
        composition: Option<&role_supply::Composition>,
        binding: &crate::role_lifecycle::RoleBinding,
        parent: Option<&Arc<PublishedRoleSupply>>,
    ) -> Result<(Value, Option<Arc<PublishedRoleSupply>>), String> {
        binding.verify_supply_observation(&row, composition)?;
        let mut chain = vec![];
        if row["trigger"] == "fork" {
            let Some(parent) = parent else {
                let (status, _, _) = self.append_row(row, composition)?;
                let mut status = status;
                status["r3Limit"]=json!("exact original parent publication receipt unavailable; quoted fork observation supplies no R3 grant");
                return Ok((status, None));
            };
            if !Arc::ptr_eq(self, &parent.owner)
                || parent.home() != binding.home()
                || row["lineage"]["sourceThread"] != parent.thread()
                || row["lineage"]["inheritedFrom"] != parent.supply_id()
                || binding.original_content() != &parent.content
            {
                return Err(
                    "fork publication parent receipt/source differs from original binding".into(),
                );
            }
            parent.verify(&self.project)?;
            chain = parent.rows.clone();
        }
        let (status, row, basis) = self.append_row(row, composition)?;
        let project = row["project"]["projectId"]
            .as_str()
            .ok_or("role project identity absent")?;
        let project = project.to_owned();
        chain.insert(0, Arc::new(row));
        let content = binding.original_content().clone();
        let reference = source_ref(&project, &chain);
        let limit_reference = limit_ref(&project, chain.last().unwrap())?;
        let receipt = Arc::new(PublishedRoleSupply {
            owner: self.clone(),
            basis,
            rows: chain,
            reference,
            limit_reference,
            content,
        });
        receipt.verify(&self.project)?;
        Ok((status, Some(receipt)))
    }
}
fn checked_sources(content: &File, source: &Value) -> Result<(Value, Value), String> {
    let bytes = RoleLog::source_bytes(Some(content), source)?;
    let reference = &source["appBytes"]["limitAccount"];
    let id = &reference["content"];
    let len = reference["byteLength"]
        .as_u64()
        .ok_or("historical limit payload length absent")?;
    let raw = RoleLog::payload(content, &format!("{}.utf8", payload_key(id)?), id, len)?;
    let account: Value = serde_json::from_slice(&raw).map_err(|e| e.to_string())?;
    validate_limit(&account)?;
    let part = source["carried"]["developerInstructions"]["parts"]
        .as_array()
        .ok_or("original parts absent")?
        .iter()
        .find(|p| p["kind"] == "role-guidance");
    let expected = part
        .map(|p| json!({"content":p["content"],"source":p["source"]}))
        .unwrap_or(Value::Null);
    if account["role"] != source["selection"]["role"]
        || account["roleSet"] != source["selection"]["roleSet"]
        || account["composedContent"] != source["carried"]["developerInstructions"]["content"]
        || account["roleGuidance"] != expected
    {
        return Err("historical limit account differs from original supplied composition".into());
    }
    if account["role"] == "none" && account["limits"].as_array().is_none_or(|a| !a.is_empty()) {
        return Err("no-role account invents role limits".into());
    }
    if expected["source"]["state"] == "modified"
        && account["limits"]
            .as_array()
            .is_some_and(|a| a.iter().any(|v| v["standing"] != "unknown"))
    {
        return Err("modified role account upgrades original limits".into());
    }
    Ok((bytes, account))
}
fn unique_success(rows: &[Value], held: &Value) -> Result<(), String> {
    let account = rows.iter().filter(|r| {
        r["format"] == FORMAT
            && r["request"]["home"] == held["request"]["home"]
            && r["supplyId"] == held["supplyId"]
    });
    if account
        .filter(|r| {
            ["supplied", "inherited", "request-failed"]
                .contains(&r["outcome"].as_str().unwrap_or(""))
        })
        .count()
        != 1
    {
        return Err(
            "role supply account has duplicate or conflicting terminal observations".into(),
        );
    }
    Ok(())
}
/// Exact referenced observations only: no latest-by-supplyId inference. A fork
/// reference names its distinct observation and every exact inherited source.
fn resolve(log: &RoleLog, reference: &str) -> Result<(Vec<Value>, Value, Value, Value), String> {
    let encoded = reference
        .strip_prefix("role-run:v1:")
        .ok_or("unsupported role supply reference")?;
    let tuple: Value = serde_json::from_str(encoded).map_err(|e| e.to_string())?;
    let project = tuple[0].as_str().ok_or("role reference project absent")?;
    let ids = tuple[1]
        .as_array()
        .filter(|a| !a.is_empty())
        .ok_or("role reference observation chain absent")?;
    if tuple.as_array().is_none_or(|a| a.len() != 3) {
        return Err("role reference shape invalid".into());
    }
    let Some((path, folder, _admission, _writer)) = log.location(false)? else {
        return Err("role observation store unavailable".into());
    };
    let current = records_store::attach(&log.project, false)?
        .project
        .ok_or("role project identity unavailable")?;
    if current != project {
        return Err("role reference belongs to another project".into());
    }
    let (all, _chain, _basis) = RoleLog::read_lines(&folder, &path)?;
    let mut rows = vec![];
    let mut seen = std::collections::BTreeSet::new();
    for id in ids {
        let id = id
            .as_str()
            .filter(|s| seen.insert((*s).to_owned()))
            .ok_or("role reference cycle/duplicate observation")?;
        let found = all
            .iter()
            .filter(|r| r["format"] == FORMAT && r["observationId"] == id)
            .collect::<Vec<_>>();
        if found.len() != 1 {
            return Err("role source observation absent or ambiguous".into());
        }
        let row = found[0];
        unique_success(&all, row)?;
        if row["project"]["projectId"] != project
            || !["supplied", "inherited"].contains(&row["outcome"].as_str().unwrap_or(""))
        {
            return Err("role source is not a quoted successful supply observation".into());
        }
        rows.push(row.clone());
    }
    for pair in rows.windows(2) {
        let (fork, parent) = (&pair[0], &pair[1]);
        if fork["trigger"] != "fork"
            || fork["outcome"] != "inherited"
            || fork["lineage"]["inheritedFrom"] != parent["supplyId"]
            || fork["lineage"]["sourceThread"] != parent["thread"]
            || fork["request"]["home"] != parent["request"]["home"]
            || fork["request"]["generation"]["appSession"]
                != parent["request"]["generation"]["appSession"]
            || fork["selection"]["role"] != parent["selection"]["role"]
        {
            return Err("quoted fork lineage disagrees with exact original source".into());
        }
    }
    let source = rows.last().unwrap();
    if source["trigger"] != "thread-start" || source["outcome"] != "supplied" {
        return Err("quoted original start source absent".into());
    }
    let content = child(&folder, "content", false)?.ok_or("role payload folder absent")?;
    let (bytes, account) = checked_sources(&content, source)?;
    let context_ref = &tuple[2];
    let id = &context_ref["content"];
    let length = context_ref["byteLength"]
        .as_u64()
        .ok_or("run context length absent")?;
    let raw = RoleLog::payload(&content, &format!("{}.utf8", payload_key(id)?), id, length)?;
    let context: Value = serde_json::from_slice(&raw).map_err(|e| e.to_string())?;
    validate_context(&context)?;
    if context["projectId"] != project
        || context["roleSource"] != source_ref(project, &rows)
        || context["limitAccount"] != limit_ref(project, source)?
        || context["home"] != rows[0]["request"]["home"]
        || context["thread"] != rows[0]["thread"]
        || context["generation"]["home"] != context["home"]
        || context["generation"]["appSession"] != rows[0]["request"]["generation"]["appSession"]
    {
        return Err("quoted run context differs from exact role source home/thread/lineage".into());
    }
    verify_directory_child(&folder, "content", &content)?;
    log.check_project()?;
    verify_directory(&path, &folder)?;
    Ok((rows, bytes, account, context))
}
// This new cold receiver reads only the actual owning source. Reuse the
// descriptor-bound nonblocking opener; a FIFO/link is never a source, even
// if somebody supplies schema-valid bytes through it.
fn read_owning_run(path: &Path) -> Result<(Vec<Value>, Vec<String>, Option<String>), String> {
    let parent_path = path.parent().ok_or("owning role run folder absent")?;
    let parent = crate::records_index::open_directory(parent_path).map_err(|e| e.to_string())?;
    let mut file = crate::records_index::open_log(path).map_err(|e| e.to_string())?;
    plain(&file)?;
    let opened = LogBasis::of(&file.metadata().map_err(|e| e.to_string())?);
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
    let named = crate::records_index::open_log(path).map_err(|e| e.to_string())?;
    plain(&named)?;
    if opened != LogBasis::of(&file.metadata().map_err(|e| e.to_string())?)
        || opened != LogBasis::of(&named.metadata().map_err(|e| e.to_string())?)
        || identity(&parent)?
            != identity(
                &crate::records_index::open_directory(parent_path).map_err(|e| e.to_string())?,
            )?
    {
        return Err("owning role run log or folder changed while read".into());
    }
    let name = path
        .file_name()
        .ok_or("owning role run log name absent")?
        .to_string_lossy();
    let parsed = crate::record_lines::parse(&bytes, &name, 0, 0, 1, Default::default());
    let mut limits = Vec::new();
    let mut entries = Vec::new();
    for line in parsed.lines {
        limits.extend(line.limits);
        entries.extend(line.entries);
    }
    limits.extend(crate::record_lines::links_removed(
        path,
        &name,
        &parsed.chain,
    ));
    Ok((entries, limits, parsed.partial_tail))
}
/// The project relation projection reads each physical RS source once. Each
/// R3 also rechecks its owning log before quoting correspondence. Query selection
/// retains every connected correction claim (including conflicting identities
/// and wrong-kind targets); all relation decisions remain in the shared R6 reader.
pub(crate) fn read_project_sources(project: &Path) -> (Vec<Value>, Vec<String>, Value) {
    use std::collections::{BTreeMap, BTreeSet, HashSet};
    let mut entries = Vec::new();
    let mut source_names = Vec::new();
    let mut complete = HashSet::new();
    let mut limits = Vec::new();
    let mut ids = HashSet::new();
    let mut partials = Vec::new();
    match crate::storage::discover(project) {
        Err(error) => limits.push(error),
        Ok(paths) => {
            for path in paths {
                let name = path.to_string_lossy().into_owned();
                match read_owning_run(&path) {
                    Err(error) => {
                        limits.push(format!("incomplete record: {}: {error}", path.display()))
                    }
                    Ok((read, errors, partial)) => {
                        if errors.is_empty() && partial.is_none() {
                            complete.insert(name.clone());
                        }
                        limits.extend(errors);
                        partials.extend(partial);
                        // The prior project reader names every repeated identity,
                        // including copies outside the role relation query.
                        for entry in &read {
                            if let Some(id) = entry["recordId"].as_str() {
                                if !ids.insert(id.to_owned()) {
                                    limits.push(format!("duplicate record identity: {id}"));
                                }
                            }
                        }
                        source_names.extend(std::iter::repeat_n(name, read.len()));
                        entries.extend(read);
                    }
                }
            }
        }
    }
    limits.extend(partials);
    let role_runs: BTreeSet<_> = entries
        .iter()
        .filter(|e| is_role(e))
        .filter_map(|e| e["runId"].as_str())
        .collect();
    let mut relevant: BTreeSet<String> = entries
        .iter()
        .filter(|e| {
            is_role(e)
                || (e["kind"] == "run_opened"
                    && e["runId"].as_str().is_some_and(|r| role_runs.contains(r)))
        })
        .filter_map(|e| e["recordId"].as_str().map(str::to_owned))
        .collect();
    let mut adjacent: BTreeMap<&str, BTreeSet<&str>> = BTreeMap::new();
    for e in &entries {
        if let (Some(id), Some(target)) = (e["recordId"].as_str(), e["corrects"].as_str()) {
            adjacent.entry(id).or_default().insert(target);
            adjacent.entry(target).or_default().insert(id);
        }
    }
    let mut todo: Vec<_> = relevant.iter().cloned().collect();
    while let Some(id) = todo.pop() {
        for next in adjacent.get(id.as_str()).into_iter().flatten() {
            if relevant.insert((*next).to_owned()) {
                todo.push((*next).to_owned());
            }
        }
    }
    let claims: Vec<_> = entries
        .iter()
        .zip(source_names)
        .filter(|(e, _)| {
            e["recordId"]
                .as_str()
                .is_some_and(|id| relevant.contains(id))
        })
        .map(|(e, log)| json!({"record":e,"source":{"log":log,"seq":e["seq"]}}))
        .collect();
    let mut relations =
        crate::decision_view::record_relations::project_from_read_claims(&claims, &complete);
    relations["readLimits"] = json!(limits);
    (entries, limits, relations)
}
fn is_role(entry: &Value) -> bool {
    entry["kind"] == "supplied_guidance"
        && [
            "role guidance at conversation start",
            "role guidance inherited at fork",
        ]
        .contains(&entry["body"]["supplyForm"].as_str().unwrap_or(""))
}
fn relation_disclosure(relations: &Value, id: &Value) -> Value {
    let claims: Vec<_> = relations["claims"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|c| c["record"]["recordId"] == *id)
        .collect();
    let groups: Vec<_> = relations["correctionGroups"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|g| {
            g["recordIds"]
                .as_array()
                .is_some_and(|ids| ids.contains(id))
        })
        .collect();
    let mut related = std::collections::BTreeSet::new();
    if let Some(id) = id.as_str() {
        related.insert(id.to_owned());
    }
    for group in &groups {
        related.extend(
            group["recordIds"]
                .as_array()
                .into_iter()
                .flatten()
                .filter_map(Value::as_str)
                .map(str::to_owned),
        );
    }
    for claim in relations["claims"].as_array().into_iter().flatten() {
        if claim["record"]["corrects"] == *id {
            if let Some(id) = claim["record"]["recordId"].as_str() {
                related.insert(id.to_owned());
            }
        }
    }
    let diagnostics: Vec<_> = relations["diagnostics"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|d| {
            d["recordId"]
                .as_str()
                .is_some_and(|id| related.contains(id))
        })
        .collect();
    let corrected = claims
        .first()
        .map(|c| c["correctedBy"].clone())
        .unwrap_or_else(|| json!([]));
    let identity = claims
        .first()
        .map(|c| c["identityResolution"].clone())
        .unwrap_or(Value::Null);
    let relation_limit = claims
        .first()
        .map(|c| c["relationLimit"].clone())
        .unwrap_or(Value::Null);
    let mut limits = Vec::<String>::new();
    if claims.is_empty() {
        limits.push("Record not found in guarded project relation sources; correction standing is unresolved".into());
    }
    if corrected.as_array().is_some_and(|c| !c.is_empty()) {
        limits.push(
            "This recorded claim has corrections; its original quoted source remains retained"
                .into(),
        );
    }
    if identity == "conflicting identity" {
        limits.push("Conflicting record identity; no unique current recorded claim".into());
    }
    if let Some(reason) = relation_limit.as_str() {
        limits.push(reason.into());
    }
    for group in &groups {
        if group["resolution"] != "unique recorded correction/claim" {
            limits.push(
                group["resolution"]
                    .as_str()
                    .unwrap_or("unresolved correction group")
                    .into(),
            );
        }
        if group["sourceIncomplete"] == true {
            limits.push("A correction group's source is incomplete".into());
        }
    }
    limits.extend(
        diagnostics
            .iter()
            .filter_map(|d| d["reason"].as_str())
            .map(str::to_owned),
    );
    limits.extend(
        relations["readLimits"]
            .as_array()
            .into_iter()
            .flatten()
            .filter_map(Value::as_str)
            .map(str::to_owned),
    );
    let unresolved = claims.is_empty()
        || identity == "conflicting identity"
        || !relation_limit.is_null()
        || !diagnostics.is_empty()
        || groups.iter().any(|g| {
            g["resolution"] != "unique recorded correction/claim" || g["sourceIncomplete"] == true
        })
        || relations["readLimits"]
            .as_array()
            .is_some_and(|l| !l.is_empty());
    json!({"correctedBy":corrected,"identityResolution":identity,"relationLimit":relation_limit,"correctionGroups":groups,"relationDiagnostics":diagnostics,"relationLimits":limits,
        "currentClaimStanding":if unresolved{"unresolved recorded relations; original quote only"}else if corrected.as_array().is_some_and(|c|!c.is_empty()){"corrected recorded claim; original quote retained"}else{"unique recorded claim; no native authority established"}})
}
pub(crate) fn read_r3(project: &Path, entry: &Value) -> Value {
    let (_, _, relations) = read_project_sources(project);
    read_r3_with_relations(project, entry, &relations)
}
pub(crate) fn read_r3_with_relations(project: &Path, entry: &Value, relations: &Value) -> Value {
    let reading = (|| -> Result<Value, String> {
        crate::schema_validation::bundled()?.validate(entry)?;
        let body = &entry["body"];
        if entry["kind"] != "supplied_guidance"
            || ![
                "role guidance at conversation start",
                "role guidance inherited at fork",
            ]
            .contains(&body["supplyForm"].as_str().unwrap_or(""))
        {
            return Err("not a role supply form".into());
        }
        let reference = body["supplyRecord"]["ref"]
            .as_str()
            .ok_or("role supply reference absent")?;
        let log = RoleLog::open(project)?;
        let (rows, bytes, account, context) = resolve(&log, reference)?;
        let first = &rows[0];
        let source = rows.last().unwrap();
        let form = if first["trigger"] == "fork" {
            "role guidance inherited at fork"
        } else {
            "role guidance at conversation start"
        };
        if body["supplyForm"] != form
            || body["thread"] != first["thread"]
            || body["sourceIdentity"] != context["roleSource"]
            || body["content"] != source["carried"]["developerInstructions"]["content"]
            || body["adoption"] != "unknown"
            || body["limitAccount"]["ref"]
                != limit_ref(first["project"]["projectId"].as_str().unwrap(), source)?
        {
            return Err(
                "RS role guidance differs from referenced original supply/limit evidence".into(),
            );
        }
        let run = entry["runId"]
            .as_str()
            .ok_or("role R3 run identity absent")?;
        let home = records_store::home(project)?;
        if let Some(refusal) = home.attachment.refusal {
            return Err(refusal);
        }
        let directory = if home.store_mode {
            home.attachment
                .dir
                .ok_or("owning role run store unavailable")?
        } else {
            project.join(storage::LEGACY_RECORDS)
        };
        let log = directory.join(storage::log_rel(
            Some(run),
            crate::records::supply::LIVE_WRITER,
        ));
        let (entries, mut limits, partial) = read_owning_run(&log)?;
        limits.extend(partial);
        if entries
            .iter()
            .filter(|e| e["recordId"] == entry["recordId"])
            .count()
            != 1
            || !entries.iter().any(|e| e == entry)
        {
            return Err("role R3 is absent or ambiguous in its actual owning log".into());
        }
        if !limits.is_empty() {
            return Err(format!("role R3 owning run source incomplete: {limits:?}"));
        }
        let opened = entries
            .iter()
            .filter(|e| e["kind"] == "run_opened" && e["runId"] == run)
            .collect::<Vec<_>>();
        if context["run"] != run
            || opened.len() != 1
            || opened[0]["recordId"] != context["opened"]["recordId"]
            || opened[0]["observedAt"] != context["opened"]["observedAt"]
            || body_identity(&opened[0]["body"])? != context["opened"]["content"]
            || opened[0]["body"]["conversationRef"] != first["thread"]
            || opened[0]["body"]["workflow"]["sourceRoot"] != context["scope"]["sourceRoot"]
            || opened[0]["body"].get("seatRole").is_some_and(|r| {
                r != if account["role"] == "none" {
                    "no role"
                } else {
                    account["role"].as_str().unwrap_or("")
                }
            })
        {
            return Err("role R3 does not match its owning run/conversation/seat role".into());
        }
        let wr = crate::workflow_workspace::publication::ProjectRecords::open(project)?;
        let run_text = wr
            .resolve(
                context["runText"]
                    .as_str()
                    .ok_or("run text reference absent")?,
            )
            .map_err(|e| format!("run context WR run text unavailable: {e:?}"))?;
        let selection = wr
            .resolve(
                context["selectionRecord"]
                    .as_str()
                    .ok_or("selection reference absent")?,
            )
            .map_err(|e| format!("run context WR selection unavailable: {e:?}"))?;
        if run_text.body()["record_kind"] != "run_text"
            || run_text.body()["purpose"] != "run start"
            || run_text.body()["run"] != run
            || run_text.body()["conversation"] != first["thread"]
            || run_text.body()["selection"] != context["scope"]["selectionRef"]
            || selection.body()["selection_id"] != context["scope"]["selectionRef"]
            || selection.body()["identity"]["source_root"] != context["scope"]["sourceRoot"]
            || selection.body()["conversation"] != first["thread"]
            || run_text.body()["holding_library"] != context["scope"]["holdingLibrary"]
        {
            return Err(
                "quoted role run context disagrees with actual WR run/selection sources".into(),
            );
        }
        Ok(
            json!({"state":"quoted historical correspondence","recordId":entry["recordId"],"runId":entry["runId"],"sourceObservations":rows,
            "sourceBytes":bytes,"limitAccount":account,"runContext":context,"adoption":"unknown","currentRoleAuthorityRestored":false,
            "limits":[STANDING]}),
        )
    })();
    let mut reading=reading.unwrap_or_else(|limit|json!({"state":"limited","recordId":entry["recordId"],"runId":entry["runId"],"limits":[limit,STANDING],"currentRoleAuthorityRestored":false,"adoption":"unknown"}));
    if !relations["claims"]
        .as_array()
        .into_iter()
        .flatten()
        .any(|claim| claim["record"] == *entry)
    {
        reading["state"] = json!("limited");
    }
    let disclosed = relation_disclosure(relations, &entry["recordId"]);
    reading["limits"].as_array_mut().unwrap().extend(
        disclosed["relationLimits"]
            .as_array()
            .unwrap()
            .iter()
            .cloned(),
    );
    if let Some(opened) = reading["runContext"]["opened"]["recordId"].as_str() {
        reading["runOpenedRelations"] = relation_disclosure(relations, &json!(opened));
    }
    reading.as_object_mut().unwrap().extend(
        disclosed
            .as_object()
            .unwrap()
            .iter()
            .map(|(k, v)| (k.clone(), v.clone())),
    );
    reading
}
