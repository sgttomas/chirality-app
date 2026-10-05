//! Physical owning NIR source and HOSTING client custody. No native payload cache.
use crate::{attachments, recovery, schema_validation::compile_targets, storage, util::sha256_hex};
use serde_json::{json, Value};
use std::collections::HashSet;
use std::fs::{File, OpenOptions};
use std::io::Read;
use std::os::fd::AsRawFd;
use std::path::{Path, PathBuf};
use std::sync::OnceLock;

pub const CLIENT_SCHEMA_ID: &str =
    "urn:chirality:del-01-01:hosting-boundary:v0.10:client-request-record";
pub const CLIENT_SCHEMA: &str =
    include_str!("../resources/hosting/hosting.client-request-record.schema.json");
pub const REDACTED_ERROR: &str =
    "[attachment custody: native error text withheld; original source may be unavailable]";
fn validate_client(value: &Value) -> Result<(), String> {
    static V: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
    V.get_or_init(|| {
        compile_targets(
            &[("hosting.client-request-record.schema.json", CLIENT_SCHEMA)],
            &[CLIENT_SCHEMA_ID],
            &[CLIENT_SCHEMA_ID],
        )
        .map(|mut v| v.remove(0))
    })
    .as_ref()
    .map_err(Clone::clone)?
    .validate(value)
    .map_err(|e| format!("client custody schema: {e}"))?;
    if let Some(error) = value.get("error") {
        if error["message"] != REDACTED_ERROR
            || error.get("data").is_some()
            || error["code"].as_i64().is_none()
            || value["outcome"] != "response-observed-error"
        {
            return Err("owning client error metadata must contain actual integer code and explicit fixed redaction only".into());
        }
    }
    Ok(())
}
fn resolved(path: &Path) -> Result<PathBuf, String> {
    if !path.is_absolute()
        || path.components().any(|c| {
            matches!(
                c,
                std::path::Component::ParentDir | std::path::Component::CurDir
            )
        })
    {
        return Err("owning root must be absolute without traversal".into());
    }
    let mut parent = path;
    let mut tail = vec![];
    while !parent.try_exists().map_err(|e| e.to_string())? {
        tail.push(parent.file_name().ok_or("root resolution failed")?);
        parent = parent.parent().ok_or("root resolution failed")?;
    }
    let mut result = parent.canonicalize().map_err(|e| e.to_string())?;
    for name in tail.into_iter().rev() {
        result.push(name);
    }
    Ok(result)
}
/// Integer 1 and string "1" retain distinct storage keys; bytes inside remain authority.
pub fn rpc_key(id: &Value) -> Result<String, String> {
    if !(id.as_str().is_some_and(|s| !s.is_empty())
        || id.as_i64().is_some()
        || id.as_u64().is_some())
    {
        return Err("RPC identity is not integer/nonempty string".into());
    }
    Ok(sha256_hex(
        &serde_json::to_vec(id).map_err(|e| e.to_string())?,
    ))
}
pub fn generation_key(g: &Value) -> Result<String, String> {
    recovery::generation_ref(g)?;
    let ordered = json!([g["appSession"], g["home"], g["spawnCounter"]]);
    Ok(sha256_hex(
        &serde_json::to_vec(&ordered).map_err(|e| e.to_string())?,
    ))
}
fn submission_key(reference: &str) -> Result<String, String> {
    let id = reference
        .strip_prefix("submission:")
        .ok_or("submission namespace differs")?;
    uuid::Uuid::parse_str(id).map_err(|_| "submission token malformed")?;
    Ok(sha256_hex(reference.as_bytes()))
}
/// Nonblocking open plus actual regular descriptor check, not pathname-only check.
pub fn read_metadata(path: &Path) -> Result<Value, String> {
    storage::check_path(path)?;
    let mut options = OpenOptions::new();
    options.read(true);
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        options.custom_flags(libc::O_NONBLOCK | libc::O_NOCTTY | libc::O_NOFOLLOW);
    }
    let file = options
        .open(path)
        .map_err(|e| format!("source read unavailable: {e}"))?;
    if !file
        .metadata()
        .map_err(|e| e.to_string())?
        .file_type()
        .is_file()
    {
        return Err("source descriptor is not a regular metadata file".into());
    }
    reject_hard_alias(&file)?;
    // Metadata only. A visible limit is refusal, never partial-list acceptance.
    const LIMIT: u64 = 64 * 1024 * 1024;
    let mut bytes = vec![];
    file.take(LIMIT + 1)
        .read_to_end(&mut bytes)
        .map_err(|e| e.to_string())?;
    if bytes.len() as u64 > LIMIT {
        return Err("owning metadata exceeds 64MiB read bound".into());
    }
    serde_json::from_slice(&bytes).map_err(|e| format!("source metadata malformed: {e}"))
}
fn reject_hard_alias(file: &File) -> Result<(), String> {
    #[cfg(unix)]
    {
        use std::os::unix::fs::MetadataExt;
        if file.metadata().map_err(|e| e.to_string())?.nlink() != 1 {
            return Err("owning leaf descriptor has unsafe hard aliases".into());
        }
    }
    Ok(())
}
pub(crate) struct CustodyOwnership(File);
impl Drop for CustodyOwnership {
    fn drop(&mut self) {
        unsafe {
            libc::flock(self.0.as_raw_fd(), libc::LOCK_UN);
        }
    }
}
fn owning_lock(path: &Path, create: bool) -> Result<CustodyOwnership, String> {
    storage::check_path(path)?;
    if create {
        storage::ensure_directory(path.parent().ok_or("lock parent absent")?)?;
    }
    let mut options = OpenOptions::new();
    options
        .read(true)
        .write(create)
        .create(create)
        .truncate(false);
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        options.custom_flags(libc::O_NONBLOCK | libc::O_NOCTTY | libc::O_NOFOLLOW);
    }
    let file = options
        .open(path)
        .map_err(|e| format!("owning source lock unavailable: {e}"))?;
    if !file
        .metadata()
        .map_err(|e| e.to_string())?
        .file_type()
        .is_file()
    {
        return Err("owning lock descriptor is not regular".into());
    }
    reject_hard_alias(&file)?;
    let mode = if create { libc::LOCK_EX } else { libc::LOCK_SH };
    if unsafe { libc::flock(file.as_raw_fd(), mode) } != 0 {
        return Err(format!(
            "owning source lock: {}",
            std::io::Error::last_os_error()
        ));
    }
    let guard = CustodyOwnership(file);
    reject_hard_alias(&guard.0)?;
    Ok(guard)
}
/// Actual Root descriptors only; neither this type nor its binding is hydrated
/// from a renderer snapshot, H5 digest, or a claimed completeness Boolean.
#[derive(Clone)]
pub struct NativeHomeNamespace {
    source: NamespaceHomeSource,
    received_targets: Option<crate::home_resources::SharedResourceTargets>,
}
#[derive(Clone)]
enum NamespaceHomeSource {
    Received(crate::home_resources::ExistingHomeReference),
    Planned(crate::home_resources::OwnedHomePlan),
}
impl NativeHomeNamespace {
    pub fn received(home:&crate::home_resources::ExistingHomeReference,targets:Option<&crate::home_resources::SharedResourceTargets>)->Self {
        Self{source:NamespaceHomeSource::Received(home.clone()),received_targets:targets.cloned()}
    }
    pub fn planned(home:&crate::home_resources::OwnedHomePlan)->Self {
        Self{source:NamespaceHomeSource::Planned(home.clone()),received_targets:None}
    }
    fn observe(&self)->Result<(PathBuf,String,crate::home_resources::HomeClass,Vec<(String,Option<PathBuf>)>,bool),String>{
        match &self.source {
            NamespaceHomeSource::Planned(plan)=>{
                let observed=plan.inspect()?;
                if observed.resources.iter().any(|r|matches!(r.state,crate::home_resources::ResourceState::Conflict|crate::home_resources::ResourceState::TargetMissing|crate::home_resources::ResourceState::TargetTypeMismatch)){return Err("owned fixed native resource relationship is conflicted/unavailable".into());}
                let targets=observed.resources.iter().map(|r|(r.name.to_owned(),r.intended_target.clone())).collect();
                Ok((observed.native_path,observed.opaque_home_id,observed.class,targets,observed.class!=crate::home_resources::HomeClass::Probe))
            },
            NamespaceHomeSource::Received(home)=>{
                let observed=home.inspect()?;
                let targets=match &self.received_targets{Some(t)=>vec![("config.toml".into(),Some(t.config_toml.clone())),("AGENTS.md".into(),Some(t.global_agents_md.clone())),("skills".into(),Some(t.skills.clone()))],None=>vec![("config.toml".into(),None),("AGENTS.md".into(),None),("skills".into(),None)]};
                Ok((observed.native_path,observed.opaque_home_id,observed.class,targets,false))
            }
        }
    }
}
/// Finite explicitly known current/prospective native set. Re-observes only
/// the three named entries/declared sources, never native directory contents.
pub struct NativeNamespaceBindings { homes:Vec<NativeHomeNamespace> }
#[derive(Clone)]
struct ProtectedNamespace { path:PathBuf, resolved:PathBuf, directory:bool }
impl NativeNamespaceBindings {
    pub fn from_root(homes:Vec<NativeHomeNamespace>)->Result<std::sync::Arc<Self>,String>{
        if homes.is_empty(){return Err("Root native namespace set is absent; no empty-set safety claim".into());}
        let binding=std::sync::Arc::new(Self{homes});binding.protected()?;Ok(binding)
    }
    fn protected(&self)->Result<Vec<ProtectedNamespace>,String>{
        let mut output=vec![];let mut ids=HashSet::new();let mut home_paths:Vec<(PathBuf,PathBuf)>=vec![];let mut classes=HashSet::new();
        for home in &self.homes {
            let(path,id,class,targets,required)=home.observe()?;
            if !ids.insert(id)||!classes.insert(class.as_str()){return Err("Root native home ID/class duplicated; no map-last interpretation".into());}
            storage::check_path(&path)?;let actual=resolved(&path)?;
            for (prior_path,prior) in &home_paths{if overlap(&actual,prior)||physical_alias(&path,prior_path)?{return Err("Root native homes alias/overlap".into());}}
            home_paths.push((path.clone(),actual.clone()));output.push(ProtectedNamespace{path:path.clone(),resolved:actual,directory:true});
            for(name,target)in targets{
                let slot=path.join(&name);let directory=name=="skills";
                if required&&target.is_none(){return Err(format!("required M-A source {name} not configured; native metadata closure unavailable"));}
                let declared=match target{
                    Some(target)=>{
                        let actual_target=target.canonicalize().map_err(|e|format!("declared native {name} source closure unavailable: {e}"))?;
                        let meta=std::fs::metadata(&actual_target).map_err(|e|e.to_string())?;
                        if (directory&&!meta.is_dir())||(!directory&&!meta.is_file()){return Err(format!("declared native {name} source type differs"));}
                        output.push(ProtectedNamespace{path:target.clone(),resolved:actual_target.clone(),directory});Some(actual_target)
                    },None=>None,
                };
                match std::fs::symlink_metadata(&slot){
                    Ok(meta)if meta.file_type().is_symlink()=>{
                        let actual_slot=slot.canonicalize().map_err(|e|format!("fixed native {name} target closure unavailable: {e}"))?;
                        let Some(expected)=declared.as_ref() else{return Err(format!("foreign fixed native {name} link has no declared source closure"));};
                        if actual_slot!=*expected{return Err(format!("fixed native {name} link drifted from declared source"));}
                        let actual_meta=std::fs::metadata(&actual_slot).map_err(|e|e.to_string())?;
                        if (directory&&!actual_meta.is_dir())||(!directory&&!actual_meta.is_file()){return Err(format!("fixed native {name} target type differs"));}
                        output.push(ProtectedNamespace{path:slot,resolved:actual_slot,directory});
                    },
                    Ok(meta)=>{
                        if required{return Err(format!("required M-A fixed native {name} link missing/wrong-type"));}
                        if (directory&&!meta.is_dir())||(!directory&&!meta.is_file()){return Err(format!("direct native {name} entry type differs"));}
                        output.push(ProtectedNamespace{path:slot.clone(),resolved:slot.canonicalize().map_err(|e|e.to_string())?,directory});
                    },
                    Err(e)if e.kind()==std::io::ErrorKind::NotFound=>{
                        if required&&path.try_exists().map_err(|e|e.to_string())?{return Err(format!("required M-A fixed native {name} entry absent in existing home"));}
                        // Planned links may not exist before setup; their actual
                        // declared targets remain protected now. Received absent
                        // slots are an observation, not invented M-A sharing.
                    },
                    Err(e)=>return Err(format!("fixed native {name} observation unavailable: {e}")),
                }
            }
        }Ok(output)
    }
    /// Independent per-feature actual domains/leaf check, not a reusable safe
    /// Boolean. No arbitrary write to the shared App-data ancestor is granted.
    pub(crate) fn guard_domains(&self,domains:&[PathBuf])->Result<(),String>{
        let protected=self.protected()?;
        for domain in domains {
            storage::check_path(domain)?;let actual=resolved(domain)?;
            for native in &protected {
                if overlap(domain,&native.path)||overlap(&actual,&native.resolved)||physical_alias(domain,&native.path)? {
                    return Err(format!("owning metadata namespace intersects native protected {}",if native.directory{"directory"}else{"file"}));
                }
            }
        }Ok(())
    }
    pub(crate) fn guard_app_root(&self,app_root:&Path)->Result<(),String>{
        for home in &self.homes{let(path,_,_,_,_)=home.observe()?;let h=resolved(&path)?;if app_root==h||app_root.starts_with(&h){return Err("App data root is equal to/inside a native home".into());}}Ok(())
    }
    pub(crate) fn contains_home_id(&self,id:&str)->Result<(),String>{self.protected()?;if self.homes.iter().any(|home|home.observe().map(|h|h.1==id).unwrap_or(false)){Ok(())}else{Err("receiving generation home is absent from actual Root namespace bindings".into())}}
    pub fn snapshot(&self)->Value {
        match self.protected(){Ok(protected)=>json!({"state":"current fixed native namespace metadata observed","protectedLocations":protected.len(),"standing":"Root descriptors/current metadata only; no contents/census/native proof or future race guarantee"}),Err(error)=>json!({"state":"native metadata closure unavailable","limit":error})}
    }
}
fn overlap(a:&Path,b:&Path)->bool{a==b||a.starts_with(b)||b.starts_with(a)}
fn physical_alias(a:&Path,b:&Path)->Result<bool,String>{
    use std::os::unix::fs::MetadataExt;
    let read=|p:&Path|->Result<Option<std::fs::Metadata>,String>{match std::fs::metadata(p){Ok(m)=>Ok(Some(m)),Err(e)if e.kind()==std::io::ErrorKind::NotFound=>Ok(None),Err(e)=>Err(e.to_string())}};
    match(read(a)?,read(b)?){(Some(a),Some(b))=>Ok(a.dev()==b.dev()&&a.ino()==b.ino()),_=>Ok(false)}
}
/// Root comes from the integrating native host, never a renderer path or fallback.
pub struct AttachmentCustody {
    root: PathBuf,
    namespaces:Option<std::sync::Arc<NativeNamespaceBindings>>,
}
impl AttachmentCustody {
    pub fn open(app_data: &Path, codex_home: &Path) -> Result<Self, String> {
        storage::check_path(app_data)?;
        let root = resolved(app_data)?;
        let home = resolved(codex_home)?;
        if root.starts_with(&home) || home.starts_with(&root) {
            return Err("App attachment custody and Codex home overlap".into());
        }
        storage::ensure_directory(&root.join("runtime"))?;
        Ok(Self { root, namespaces:None })
    }
    pub fn open_with_namespaces(app_data:&Path,namespaces:std::sync::Arc<NativeNamespaceBindings>)->Result<Self,String>{
        storage::check_path(app_data)?;let root=resolved(app_data)?;namespaces.guard_app_root(&root)?;
        let owner=Self{root,namespaces:Some(namespaces)};owner.guard_scope()?;storage::ensure_directory(&owner.root.join("runtime"))?;owner.guard_scope()?;Ok(owner)
    }
    fn guard_scope(&self)->Result<(),String>{
        if let Some(bindings)=&self.namespaces{bindings.guard_app_root(&self.root)?;bindings.guard_domains(&[self.root.join("runtime/nir/attachment-supplies"),self.root.join("runtime/hosting/client-requests"),self.lock_path()])?;}Ok(())
    }
    fn guard_generation(&self,g:&Value)->Result<(),String>{recovery::generation_ref(g)?;if let Some(bindings)=&self.namespaces{bindings.contains_home_id(g["home"].as_str().unwrap())?;}Ok(())}
    fn guard_leaf(&self,path:&Path)->Result<(),String>{self.guard_scope()?;if let Some(bindings)=&self.namespaces{bindings.guard_domains(&[path.to_owned()])?;}Ok(())}
    pub fn root(&self) -> &Path {
        &self.root
    }
    pub fn supplies_path(&self, submission: &str) -> Result<PathBuf, String> {
        self.guard_scope()?;
        Ok(self
            .root
            .join("runtime/nir/attachment-supplies")
            .join(format!("{}.json", submission_key(submission)?)))
    }
    pub fn client_path(&self, g: &Value, id: &Value) -> Result<PathBuf, String> {
        self.guard_scope()?;self.guard_generation(g)?;
        Ok(self
            .root
            .join("runtime/hosting/client-requests")
            .join(generation_key(g)?)
            .join(format!("{}.json", rpc_key(id)?)))
    }
    fn lock_path(&self) -> PathBuf {
        self.root.join("runtime/hosting/.client-custody.lock")
    }
    pub(crate) fn lock_sources(&self) -> Result<CustodyOwnership, String> {
        self.guard_leaf(&self.lock_path())?;owning_lock(&self.lock_path(), true)
    }
    pub fn publish_prepared(&self, records: &[Value], client: &Value) -> Result<(), String> {
        validate_client(client)?;
        if client["outcome"] != "prepared-not-sent"
            || client["writeResult"] != "not-attempted"
            || client.get("sendPosition").is_some()
        {
            return Err("prewrite observation differs".into());
        }
        self.guard_scope()?;self.guard_generation(&client["generation"])?;
        let association = &client["submissionAssociation"];
        validate_list(records, association)?;
        let _lock = self.lock_sources()?;
        storage::create_json(
            &self.supplies_path(association["submissionRef"].as_str().unwrap())?,
            &json!(records),
        )?;
        storage::create_json(
            &self.client_path(&client["generation"], &client["requestIdentity"])?,
            client,
        )?;
        self.check_prepared(records, client)
    }
    pub fn check_prepared(&self, records: &[Value], client: &Value) -> Result<(), String> {
        self.guard_scope()?;validate_client(client)?;
        let actual =
            read_metadata(&self.client_path(&client["generation"], &client["requestIdentity"])?)?;
        if actual != *client {
            return Err("durable client binding differs from reserved observation".into());
        }
        let array = read_metadata(
            &self.supplies_path(
                client["submissionAssociation"]["submissionRef"]
                    .as_str()
                    .ok_or("submission absent")?,
            )?,
        )?;
        let items = array
            .as_array()
            .ok_or("owning supply source is not ordered array")?;
        validate_list(items, &client["submissionAssociation"])?;
        if items != records {
            return Err("complete owning supply list differs from prepared input".into());
        }
        Ok(())
    }
    /// Atomic state update of the same source; original values are immutable.
    pub fn replace_observation(&self, record: &Value) -> Result<(), String> {
        validate_client(record)?;
        let _lock = self.lock_sources()?;
        let path = self.client_path(&record["generation"], &record["requestIdentity"])?;
        let old = read_metadata(&path)?;
        validate_client(&old)?;
        for field in [
            "recordKind",
            "generation",
            "requestIdentity",
            "method",
            "initiator",
            "submissionAssociation",
        ] {
            if old.get(field) != record.get(field) {
                return Err(format!("immutable client field changed: {field}"));
            }
        }
        // A stale pending/written snapshot cannot erase a settled first reply.
        if matches!(
            old["outcome"].as_str(),
            Some("response-observed-result" | "response-observed-error")
        ) && record["outcome"] != old["outcome"]
        {
            return Err("settled custody observation cannot be replaced by stale outcome".into());
        }
        storage::replace_json(&path, record)?;
        let check = read_metadata(&path)?;
        if check != *record {
            return Err("client observation readback differs".into());
        }
        Ok(())
    }
    /// Source reader. Disk claims never create a hot capability/native turn proof.
    pub fn resolve_cold(&self, submission: &str) -> Value {
        let result = (|| -> Result<Value, String> {
            submission_key(submission)?;self.guard_scope()?;
            let _read_lock = owning_lock(&self.lock_path(), false)?;
            let clients = self.root.join("runtime/hosting/client-requests");
            let mut found = vec![];
            if !clients.try_exists().map_err(|e| e.to_string())? {
                return Err("owning client custody unavailable".into());
            }
            storage::check_path(&clients)?;
            for entry in std::fs::read_dir(&clients).map_err(|e| e.to_string())? {
                let dir = entry.map_err(|e| e.to_string())?.path();
                storage::check_path(&dir)?;
                if !dir.is_dir() {
                    return Err("unexpected entry in client generation source".into());
                }
                for entry in std::fs::read_dir(&dir).map_err(|e| e.to_string())? {
                    let path = entry.map_err(|e| e.to_string())?.path();
                    if path.extension().is_none_or(|e| e != "json") {
                        continue;
                    }
                    let record = read_metadata(&path)?;
                    validate_client(&record)?;
                    if path
                        != self.client_path(&record["generation"], &record["requestIdentity"])?
                    {
                        return Err(
                            "source path key differs from authoritative typed fields".into()
                        );
                    }
                    if record["submissionAssociation"]["submissionRef"] == submission {
                        found.push(record);
                    }
                }
            }
            if found.len() != 1 {
                return Err("submission source missing or conflicting".into());
            }
            let record = found.pop().unwrap();
            let records = read_metadata(&self.supplies_path(submission)?)?;
            validate_list(
                records.as_array().ok_or("supply source is not array")?,
                &record["submissionAssociation"],
            )?;
            Ok(
                json!({"submissionRef":submission,"clientMetadata":record,"supplyRecords":records,"nativeTurnRef":null,"dispatch":"unknown/unavailable cold evidence","standing":"unverified source claims; no imported Host receipt or acceptance proof","limits":["Native write/result/journal source is unavailable in this cold reader; prepared-only never proves no send and never permits retry.","Stored outcome is App metadata, not a native turn or provider adoption proof."],"automaticRetry":false}),
            )
        })();
        match result {
            Ok(v) => v,
            Err(error) => {
                json!({"submissionRef":submission,"nativeTurnRef":null,"dispatch":"unknown/unavailable","limits":[error],"automaticRetry":false})
            }
        }
    }
}
pub fn validate_list(records: &[Value], association: &Value) -> Result<(), String> {
    let reference = association["submissionRef"]
        .as_str()
        .ok_or("submission reference absent")?;
    submission_key(reference)?;
    let refs = association["supplyRefs"]
        .as_array()
        .ok_or("ordered supply references absent")?;
    if refs.is_empty() || records.len() != refs.len() {
        return Err("complete supply/reference list length differs".into());
    }
    let mut seen = HashSet::new();
    for (record, reference_id) in records.iter().zip(refs) {
        attachments::validate_supply(record)?;
        let id = record["attachmentId"]
            .as_str()
            .ok_or("attachment identity absent")?;
        if record["turnRef"] != reference
            || reference_id != &json!(format!("attachment:{id}"))
            || !seen.insert(id)
        {
            return Err("owning ordered identity/token/reference differs or repeats".into());
        }
    }
    Ok(())
}
/// Allowlisted projection only; no response body/native message/data is persisted.
pub fn project_observation(
    client: &Value,
    response: Option<&Value>,
    position: Option<u64>,
) -> Result<(Value, Option<String>), String> {
    let mut record = client.clone();
    record
        .as_object_mut()
        .ok_or("client is not object")?
        .remove("error");
    let mut limit = None;
    if let Some(frame) = response {
        if frame.get("id") != record.get("requestIdentity")
            || frame.get("method").is_some()
            || !frame.is_object()
            || frame.get("error").is_some() && frame.get("result").is_some()
        {
            record["outcome"] = json!("unknown-no-response");
            limit = Some("malformed/contradictory native response; no settled native proof".into());
        } else if let Some(error) = frame.get("error") {
            if error["code"].as_i64().is_some()
                && error["message"].is_string()
                && position.is_some()
            {
                record["outcome"] = json!("response-observed-error");
                record["error"] = json!({"code":error["code"],"message":REDACTED_ERROR});
            } else {
                record["outcome"] = json!("unknown-no-response");
                limit=Some("native error code/message/position missing or malformed; no invented error code".into());
            }
        } else if frame.get("result").is_some() && position.is_some() {
            record["outcome"] = json!("response-observed-result");
        } else {
            record["outcome"] = json!("unknown-no-response");
            limit = Some("native response result/position unavailable".into());
        }
        if let Some(p) = position {
            record["responseReceiptPosition"] = json!(p);
        }
    }
    validate_client(&record)?;
    Ok((record, limit))
}
