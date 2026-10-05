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
/// Root comes from the integrating native host, never a renderer path or fallback.
pub struct AttachmentCustody {
    root: PathBuf,
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
        Ok(Self { root })
    }
    pub fn root(&self) -> &Path {
        &self.root
    }
    pub fn supplies_path(&self, submission: &str) -> Result<PathBuf, String> {
        Ok(self
            .root
            .join("runtime/nir/attachment-supplies")
            .join(format!("{}.json", submission_key(submission)?)))
    }
    pub fn client_path(&self, g: &Value, id: &Value) -> Result<PathBuf, String> {
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
        owning_lock(&self.lock_path(), true)
    }
    pub fn publish_prepared(&self, records: &[Value], client: &Value) -> Result<(), String> {
        validate_client(client)?;
        if client["outcome"] != "prepared-not-sent"
            || client["writeResult"] != "not-attempted"
            || client.get("sendPosition").is_some()
        {
            return Err("prewrite observation differs".into());
        }
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
        validate_client(client)?;
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
            submission_key(submission)?;
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
