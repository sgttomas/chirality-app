//! App-observed durable pointers. This ledger never replaces Codex history and
//! never makes an old supplier request answerable after process loss/relaunch.
use crate::util::now_rfc3339;
use serde_json::{json, Value};
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, Read, Seek, SeekFrom, Write};
use std::path::PathBuf;
use std::sync::{Arc,OnceLock};
use crate::hosting::attachment_custody::NativeNamespaceBindings;

fn validator() -> Result<&'static jsonschema::Validator, String> {
    static VALIDATOR: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
    VALIDATOR
        .get_or_init(|| {
            let schema: Value = serde_json::from_str(include_str!(
                "../resources/runtime_core/recovery.app-ledger-entry.schema.json"
            ))
            .map_err(|e| e.to_string())?;
            jsonschema::options()
                .offline()
                .build(&schema)
                .map_err(|e| e.to_string())
        })
        .as_ref()
        .map_err(Clone::clone)
}
/// CC-REC-GEN preserves the source-confirmed full H5 tuple at the ledger seam.
/// No spawn, missing context or a legacy opaque string can mint a generation.
pub fn generation_ref(generation: &Value) -> Result<String, String> {
    if generation.as_object().map(|o| o.len() != 3).unwrap_or(true)
        || generation["appSession"]
            .as_str()
            .map(str::is_empty)
            .unwrap_or(true)
        || generation["home"]
            .as_str()
            .map(str::is_empty)
            .unwrap_or(true)
        || generation["spawnCounter"].as_u64().unwrap_or(0) == 0
    {
        return Err("invalid generation identity".into());
    }
    let hex = |value: &str| {
        value
            .as_bytes()
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect::<String>()
    };
    Ok(format!(
        "gen:v1:s:{}:h:{}:n:{}",
        hex(generation["appSession"].as_str().unwrap()),
        hex(generation["home"].as_str().unwrap()),
        generation["spawnCounter"]
    ))
}
pub fn generation_from_ref(reference: &str) -> Result<Value, String> {
    let parts: Vec<_> = reference.split(':').collect();
    if parts.len() != 8
        || parts[0] != "gen"
        || parts[1] != "v1"
        || parts[2] != "s"
        || parts[4] != "h"
        || parts[6] != "n"
    {
        return Err("not a canonical full generation reference".into());
    }
    fn unhex(value: &str) -> Result<String, String> {
        if value.is_empty()
            || value.len() % 2 != 0
            || !value
                .bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
        {
            return Err("invalid generation hex".into());
        }
        let bytes: Result<Vec<u8>, _> = value
            .as_bytes()
            .chunks(2)
            .map(|c| u8::from_str_radix(std::str::from_utf8(c).unwrap(), 16))
            .collect();
        String::from_utf8(bytes.map_err(|e| e.to_string())?)
            .map_err(|e| format!("invalid generation UTF-8: {e}"))
    }
    if parts[7].starts_with('0') || !parts[7].bytes().all(|b| b.is_ascii_digit()) {
        return Err("noncanonical spawn counter".into());
    }
    let counter: u64 = parts[7].parse().map_err(|_| "invalid spawn counter")?;
    let generation =
        json!({"appSession":unhex(parts[3])?,"home":unhex(parts[5])?,"spawnCounter":counter});
    if generation_ref(&generation)? != reference {
        return Err("noncanonical generation reference".into());
    }
    Ok(generation)
}

/// Root/native caller's source-qualified project observation, never deserialized
/// from renderer, native cwd/projectId, Codex home or workflow run metadata.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum AppProjectSource {
    ConfiguredDirectory,
    OpenedDirectory,
}
#[derive(Clone, Debug)]
pub struct ExplicitAppProjectContext {
    reference: Option<String>,
    source: Option<AppProjectSource>,
}
impl ExplicitAppProjectContext {
    pub fn known(reference: &str, source: AppProjectSource) -> Result<Self, String> {
        if reference.is_empty() {
            return Err("explicit App project reference must be nonempty".into());
        }
        Ok(Self {
            reference: Some(reference.into()),
            source: Some(source),
        })
    }
    pub fn unknown() -> Self {
        Self {
            reference: None,
            source: None,
        }
    }
    pub fn reference(&self) -> Option<&str> {
        self.reference.as_deref()
    }
    pub fn source_caption(&self) -> &'static str {
        match self.source {
            Some(AppProjectSource::ConfiguredDirectory) => "configured App directory",
            Some(AppProjectSource::OpenedDirectory) => "opened App directory",
            None => "App project not established",
        }
    }
    pub fn view(&self) -> Value {
        json!({"reference":self.reference,"sourceCaption":self.source_caption(),"standing":"explicit frozen Root observation; no native/actor authority inferred"})
    }
}
pub const NIR_CONTEXT_OWNER: &str = "DEL-01-04";
/// NIR receiver interpretation of REC's unchanged opaque tag value.
pub fn encode_submission_context(
    submission: &str,
    project: Option<&str>,
) -> Result<String, String> {
    if !submission
        .strip_prefix("submission:")
        .is_some_and(|s| !s.is_empty())
        || project.is_some_and(str::is_empty)
    {
        return Err(
            "actual submission token/nonempty explicit App reference or absence required".into(),
        );
    }
    serde_json::to_string(&json!([submission, project])).map_err(|e| e.to_string())
}
fn decode_submission_context(tag: &Value) -> Option<(String, Option<String>)> {
    if tag["owner"] != NIR_CONTEXT_OWNER {
        return None;
    }
    let raw = tag["value"].as_str()?;
    let pair: Value = serde_json::from_str(raw).ok()?;
    let values = pair.as_array()?;
    if values.len() != 2 {
        return None;
    }
    let submission = values[0].as_str()?;
    let project = if values[1].is_null() {
        None
    } else {
        Some(values[1].as_str()?)
    };
    if encode_submission_context(submission, project)
        .ok()?
        .as_str()
        != raw
    {
        return None;
    }
    Some((submission.into(), project.map(str::to_owned)))
}
/// Merge ALL historical/durable and hot claims. Unknown opaque values remain
/// untouched; interpretation cannot manufacture a private/native capability.
pub fn submission_context_plan(
    index: Option<&Value>,
    all_durable_tags: &[Value],
    hot_tags: &[Value],
    submission: &str,
    project: Option<&str>,
) -> Result<Value, String> {
    let value = encode_submission_context(submission, project)?;
    let historical = index.and_then(|i| i["project"].as_str());
    if index.is_some() && historical.is_none_or(str::is_empty) {
        return Err("known REC index lacks actual nonempty project".into());
    }
    let mut all = all_durable_tags.to_vec();
    for tag in hot_tags {
        if !all.contains(tag) {
            all.push(tag.clone());
        }
    }
    let matches: Vec<_> = all
        .iter()
        .filter_map(|tag| {
            decode_submission_context(tag)
                .filter(|(s, _)| s == submission)
                .map(|(_, p)| (tag, p))
        })
        .collect();
    if matches.iter().any(|(_, p)| p.as_deref() != project) {
        return Err(
            "immutable submission context ambiguous/conflicting; no retag or transfer".into(),
        );
    }
    let idempotent = !matches.is_empty();
    let tag = if let Some((tag, _)) = matches.first() {
        (*tag).clone()
    } else {
        let seq = all
            .iter()
            .filter_map(|t| t["seq"].as_u64())
            .max()
            .unwrap_or(0)
            .checked_add(1)
            .ok_or("tag sequence exhausted")?;
        json!({"owner":NIR_CONTEXT_OWNER,"value":value,"seq":seq})
    };
    let durable = all_durable_tags
        .iter()
        .any(|t| t["owner"] == NIR_CONTEXT_OWNER && t["value"] == value);
    let relation = match (historical, project) {
        (Some(p), Some(q)) if p == q => "same",
        (Some(_), Some(_)) => "different; no transfer",
        _ => "unbound",
    };
    Ok(
        json!({"historicalProject":historical,"currentSubmissionProject":project,"relation":relation,"tag":tag,"idempotent":idempotent,"durableBindingObserved":durable,
        "limit":if index.is_none(){Some("project index absent: no row, context tag memory-only; cold lookup unavailable")}else if idempotent&&!durable{Some("known project index lacks this hot binding: tag memory-only; cold lookup unavailable")}else{None}}),
    )
}

pub struct RecoveryLedger {
    path: PathBuf,
    entries: Vec<Value>,
    namespaces:Option<Arc<NativeNamespaceBindings>>,
}
impl RecoveryLedger {
    pub fn open(path: PathBuf) -> Result<Self, String> {Self::open_inner(path,None)}
    pub fn open_with_namespaces(path:PathBuf,namespaces:Arc<NativeNamespaceBindings>)->Result<Self,String>{Self::open_inner(path,Some(namespaces))}
    fn open_inner(path:PathBuf,namespaces:Option<Arc<NativeNamespaceBindings>>)->Result<Self,String>{
        if let Some(binding)=&namespaces{binding.guard_domains(&[path.clone()])?;crate::storage::check_path(&path)?;}
        let mut entries = Vec::new();
        let mut options=OpenOptions::new();options.read(true);
        if namespaces.is_some(){use std::os::unix::fs::OpenOptionsExt;options.custom_flags(libc::O_NONBLOCK|libc::O_NOCTTY|libc::O_NOFOLLOW);}
        match options.open(&path) {
            Ok(file) => {
                if let Some(binding)=&namespaces{Self::guard_descriptor(&path,binding,&file)?;}
                let mut reader = BufReader::new(file);
                let mut line = Vec::new();
                loop {
                    line.clear();
                    let count = reader
                        .read_until(b'\n', &mut line)
                        .map_err(|e| format!("App history unavailable: {e}"))?;
                    if count == 0 {
                        break;
                    }
                    if line.last() != Some(&b'\n') {
                        return Err("App history unavailable: final ledger record is not newline-closed; bytes preserved".into());
                    }
                    let entry: Value = serde_json::from_slice(&line)
                        .map_err(|e| format!("App history unavailable: {e}"))?;
                    validator()?
                        .validate(&entry)
                        .map_err(|e| format!("App history unavailable: {e}"))?;
                    entries.push(entry);
                }
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
            Err(e) => return Err(format!("App history unavailable: {e}")),
        }
        Ok(Self { path, entries, namespaces })
    }
    pub(crate) fn preflight_namespaces(&self,binding:&Arc<NativeNamespaceBindings>)->Result<(),String>{
        Self::preflight_path(&self.path,binding)
    }
    pub(crate) fn preflight_path(path:&std::path::Path,binding:&Arc<NativeNamespaceBindings>)->Result<(),String>{
        binding.guard_domains(&[path.to_owned()])?;crate::storage::check_path(path)?;
        match std::fs::symlink_metadata(path){Ok(meta)=>{use std::os::unix::fs::MetadataExt;if !meta.is_file()||meta.nlink()!=1{return Err("REC owning leaf is not a regular single-link source".into());}},Err(e)if e.kind()==std::io::ErrorKind::NotFound=>{},Err(e)=>return Err(format!("REC owning leaf metadata unavailable: {e}"))}Ok(())
    }
    pub(crate) fn bind_namespaces(&mut self,binding:Arc<NativeNamespaceBindings>)->Result<(),String>{self.preflight_namespaces(&binding)?;self.namespaces=Some(binding);Ok(())}
    fn guard_descriptor(path:&std::path::Path,binding:&Arc<NativeNamespaceBindings>,file:&File)->Result<(),String>{
        use std::os::unix::fs::MetadataExt;binding.guard_domains(&[path.to_owned()])?;crate::storage::check_path(path)?;let fd=file.metadata().map_err(|e|e.to_string())?;let named=std::fs::symlink_metadata(path).map_err(|e|e.to_string())?;
        if !fd.is_file()||fd.nlink()!=1||!named.is_file()||named.nlink()!=1||fd.dev()!=named.dev()||fd.ino()!=named.ino(){return Err("REC owning regular leaf/descriptor association is redirected or hard-aliased".into());}Ok(())
    }
    pub(crate) fn validate_pointer_entry(entry:&Value)->Result<(),String>{
        validator()?.validate(entry).map_err(|e|format!("execution pointer schema refused: {e}"))
    }
    pub fn append(&mut self, entry: Value) -> Result<(), String> {
        if let Some(binding)=&self.namespaces{self.preflight_namespaces(binding)?;}
        validator()?
            .validate(&entry)
            .map_err(|e| format!("recovery ledger validation refused: {e}"))?;
        let mut bytes = serde_json::to_vec(&entry).map_err(|e| e.to_string())?;
        bytes.push(b'\n');
        let mut options=OpenOptions::new();options.create(true).read(true).append(true);
        if self.namespaces.is_some(){use std::os::unix::fs::OpenOptionsExt;options.custom_flags(libc::O_NONBLOCK|libc::O_NOCTTY|libc::O_NOFOLLOW);}
        let mut file=options.open(&self.path).map_err(|e|e.to_string())?;
        if let Some(binding)=&self.namespaces{Self::guard_descriptor(&self.path,binding,&file)?;}
        // Recheck the actual tail for an external change or a previous partial
        // write. Never concatenate a fresh record onto unclosed bytes, even
        // when those bytes happen to parse as a complete JSON value.
        let length = file.seek(SeekFrom::End(0)).map_err(|e| e.to_string())?;
        if length > 0 {
            file.seek(SeekFrom::End(-1)).map_err(|e| e.to_string())?;
            let mut last = [0u8; 1];
            file.read_exact(&mut last).map_err(|e| e.to_string())?;
            if last[0] != b'\n' {
                return Err(
                    "recovery ledger append refused: unclosed final record; bytes preserved".into(),
                );
            }
        }
        file.write_all(&bytes)
            .and_then(|_| file.sync_data())
            .map_err(|e| format!("recovery ledger append not confirmed: {e}"))?;
        self.entries.push(entry);
        Ok(())
    }
    pub(crate) fn session_end_entry(session:&str,stop_requests:&[Value])->Result<Value,String>{
        let entry=json!({"kind":"session_ended","session":session,"at":now_rfc3339(),"how":"quit","stopRequests":stop_requests});
        validator()?.validate(&entry).map_err(|_|"App session end pointer metadata shape invalid; no end append".to_string())?;Ok(entry)
    }
    pub fn start_session(&mut self, session: &str, candidate: &str) -> Result<(), String> {
        let previous = self
            .entries
            .iter()
            .rev()
            .find(|e| e["kind"] == "session_started");
        let previous_id = previous
            .and_then(|e| e["session"].as_str())
            .map(str::to_owned);
        let end = previous_id.as_deref().and_then(|id| {
            self.entries
                .iter()
                .rev()
                .find(|e| e["kind"] == "session_ended" && e["session"] == id)
        });
        let previous_end = match (previous_id.as_ref(), end) {
            (None, _) => "none",
            (_, None) => "ended-without-record",
            (_, Some(e)) if e["how"] == "system-terminated" => "system-terminated",
            _ => "clean",
        };
        let mut entry = json!({"kind":"session_started","session":session,"at":now_rfc3339(),"previousSessionEnd":previous_end,"candidate":candidate});
        if let Some(id) = previous_id {
            entry["previousSession"] = json!(id);
        }
        self.append(entry)
    }
    pub fn request_summary(&mut self, request: &Value) -> Result<(), String> {
        match Self::request_summary_entry(request, &self.entries)? {
            Some(entry) => self.append(entry),
            None => Ok(()),
        }
    }
    /// Pure immutable pointer projection; callers may queue it before IO.
    pub fn request_summary_entry(
        request: &Value,
        prior_entries: &[Value],
    ) -> Result<Option<Value>, String> {
        let generation = &request["generation"];
        let state = request["state"].as_str().ok_or("request has no state")?;
        let listed = matches!(state, "received" | "outstanding" | "settling");
        let mut entry = json!({"kind":"register_entry_summary","session":generation["appSession"],"at":now_rfc3339(),
            "generation":generation_ref(generation)?,"requestIdentity":serde_json::to_string(&request["requestId"]).map_err(|e|e.to_string())?,
            "method":request["method"],"state":if listed{"listed"}else{"closed"},"transition":if listed{"RQ-01"}else{"RQ-03"},
            "replyWrite":request["replyWriteResult"],"acknowledgment":if request["acknowledgment"].is_object(){"observed"}else{"not-observed"}});
        let mut subject = serde_json::Map::new();
        for key in ["threadId", "turnId", "itemId", "callId"] {
            if let Some(v) = request["nativeParameters"].get(key) {
                // Native MCP elicitations may have no correlated turn. The
                // ledger carries optional pointer strings, not null/guessed IDs.
                if key == "turnId" && v.is_null() {
                    continue;
                }
                subject.insert(key.into(), v.clone());
            }
        }
        if !subject.is_empty() {
            entry["subject"] = Value::Object(subject);
        }
        if !listed {
            entry["endedAs"] = json!(if state == "ended-unanswered" {
                "ended-unanswered(process-exit)"
            } else {
                state
            });
            if state == "ended-unanswered" {
                entry["transition"] = json!("RQ-04");
            }
        }
        let later_error = request["classification"] == "known-answerable"
            && request["laterProtocolError"] == true;
        if later_error {
            let origin = request["settlement"]["origin"].as_str().unwrap_or("");
            if (origin != "app-explicit-error"
                && !origin
                    .strip_prefix("app-rule:")
                    .map(|rule| !rule.is_empty())
                    .unwrap_or(false))
                || request["settlement"]["error"]["code"].as_i64().is_none()
                || request["settlement"]["error"]["message"].as_str().is_none()
            {
                return Err(
                    "recovery later-error mapping refused: invalid RT14/RT09 source settlement"
                        .into(),
                );
            }
        }
        if state == "errored" {
            if request["classification"] == "known-answerable" {
                if !later_error || request["replyWriteResult"] != "written" {
                    return Err(
                        "recovery later-error mapping refused: no admitted RT14 written error"
                            .into(),
                    );
                }
                // RT14 is a later settlement of an already listed request.
                entry["transition"] = json!("RQ-03");
            } else {
                entry["transition"] = json!("RQ-08");
            }
        }
        let previous = prior_entries.iter().rev().find(|e| {
            e["kind"] == "register_entry_summary"
                && e["generation"] == entry["generation"]
                && e["requestIdentity"] == entry["requestIdentity"]
        });
        let written_settlement =
            matches!(state, "answered" | "declined") || (state == "errored" && later_error);
        if request["acknowledgment"].is_object() {
            let ack = &request["acknowledgment"];
            if request["replyWriteResult"] != "written" || !written_settlement {
                return Err(
                    "recovery acknowledgment mapping refused: no written RT12/13/15 settlement"
                        .into(),
                );
            }
            if ack["generation"] != *generation
                || ack["native"]["requestId"] != request["requestId"]
                || ack["native"]["threadId"] != request["nativeParameters"]["threadId"]
            {
                return Err(
                    "recovery acknowledgment mapping refused: foreign generation/request/thread"
                        .into(),
                );
            }
            if previous.is_none() {
                return Err(
                    "recovery acknowledgment mapping refused: no same-generation request history"
                        .into(),
                );
            }
            let durable_closed = previous
                .map(|e| matches!(e["transition"].as_str(), Some("RQ-04" | "RQ-05" | "RQ-06")))
                .unwrap_or(false);
            if (request["closedGeneration"] == true || durable_closed)
                && previous
                    .map(|e| e["acknowledgment"] != "observed")
                    .unwrap_or(true)
            {
                return Err(
                    "recovery acknowledgment mapping refused: new observation after closure".into(),
                );
            }
            entry["transition"] = json!("RQ-09");
        } else if request["closedGeneration"] == true
            && request["replyWriteResult"] == "written"
            && written_settlement
        {
            entry["transition"] = json!("RQ-05");
        }
        if let Some(origin) = request["settlement"].get("origin") {
            entry["origin"] = origin.clone();
        }
        if let Some(previous) = prior_entries.iter().rev().find(|e| {
            e["kind"] == "register_entry_summary"
                && e["generation"] == entry["generation"]
                && e["requestIdentity"] == entry["requestIdentity"]
        }) {
            let mut comparable = previous.clone();
            comparable["at"] = entry["at"].clone();
            if comparable == entry {
                return Ok(None);
            }
        }
        Ok(Some(entry))
    }
    /// Earlier sessions are historical observations, never replayed as live entries.
    pub fn snapshot(&self) -> Value {
        json!({"standing":"App-observed","entries":self.entries,"oldRequestsAnswerable":false})
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn path() -> PathBuf {
        std::env::temp_dir().join(format!(
            "chirality-recovery-{}.jsonl",
            crate::util::opaque_id("test").unwrap()
        ))
    }
    #[test]
    fn relaunch_keeps_full_generation_and_never_payload_or_answer() {
        let path = path();
        let generation = json!({"appSession":"old","home":"h","spawnCounter":1});
        let request = json!({"generation":generation,"requestId":9,"method":"item/tool/requestUserInput","state":"outstanding",
            "replyWriteResult":"not-attempted","acknowledgment":"not-observed","nativeParameters":{"threadId":"t","questions":[{"text":"must-not-persist"}]}});
        {
            let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
            ledger.start_session("old", "candidate").unwrap();
            ledger.request_summary(&request).unwrap();
        }
        let bytes = std::fs::read_to_string(&path).unwrap();
        assert!(!bytes.contains("must-not-persist"));
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        ledger.start_session("new", "candidate").unwrap();
        let snapshot = ledger.snapshot();
        assert_eq!(
            snapshot["entries"][2]["previousSessionEnd"],
            "ended-without-record"
        );
        assert_eq!(snapshot["oldRequestsAnswerable"], false);
        assert_eq!(
            generation_from_ref(snapshot["entries"][1]["generation"].as_str().unwrap()).unwrap(),
            generation
        );
        std::fs::remove_file(path).unwrap();
    }
    #[test]
    fn malformed_or_payload_bearing_ledger_fails_closed_without_write() {
        let path = path();
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        let bad = json!({"kind":"session_started","session":"s","at":"now","previousSessionEnd":"none","candidate":"candidate","payload":"secret"});
        assert!(ledger.append(bad).is_err());
        assert!(!path.exists());
        std::fs::write(&path, "{\n").unwrap();
        assert!(RecoveryLedger::open(path.clone()).is_err());
        assert_eq!(std::fs::read_to_string(&path).unwrap(), "{\n");
        std::fs::remove_file(path).unwrap();
        assert!(generation_ref(&json!(1)).is_err());
    }
}

#[cfg(test)]
mod generation_tests {
    use super::*;
    #[test]
    fn tagged_generation_roundtrips_and_distinguishes_unicode_home_and_session() {
        let strings = ["s", ":/\0", "é", "e\u{301}", "家😀"];
        let mut refs = std::collections::HashSet::new();
        for session in strings {
            for home in strings {
                for counter in [1, u64::MAX] {
                    let generation =
                        json!({"appSession":session,"home":home,"spawnCounter":counter});
                    let reference = generation_ref(&generation).unwrap();
                    assert!(refs.insert(reference.clone()));
                    assert_eq!(generation_from_ref(&reference).unwrap(), generation);
                }
            }
        }
        for bad in [
            "gen:v1:s:73:h:68:n:0",
            "gen:v1:s:73:h:68:n:01",
            "gen:v1:s:73:h:68:n:+1",
            "gen:v1:s:7:h:68:n:1",
            "gen:v1:s:FF:h:68:n:1",
            "gen:v1:s:ff:h:68:n:1",
            "gen:v1:s:eda080:h:68:n:1",
            "gen:v1:s::h:68:n:1",
            "old/opaque/g1",
        ] {
            assert!(generation_from_ref(bad).is_err(), "{bad}");
        }
    }
    #[test]
    fn no_spawn_has_no_generation_required_ledger_event() {
        let path = std::env::temp_dir().join(format!(
            "recovery-no-spawn-{}",
            crate::util::opaque_id("test").unwrap()
        ));
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        for g in [
            Value::Null,
            json!(1),
            json!({"appSession":"s","home":"h","spawnCounter":0}),
            json!({"appSession":"s","home":"h","spawnCounter":true}),
            json!({"appSession":"s","home":"h","spawnCounter":1,"extra":true}),
        ] {
            assert!(generation_ref(&g).is_err());
            assert!(ledger.request_summary(&json!({"generation":g,"requestId":1,"method":"request","state":"outstanding","replyWriteResult":"not-attempted","acknowledgment":"not-observed"})).is_err());
            assert!(!path.exists());
        }
    }
}

#[cfg(test)]
mod framing_repair_tests {
    use super::*;
    #[test]
    fn complete_unclosed_and_torn_tail_are_rejected_without_modifying_bytes() {
        let path = std::env::temp_dir().join(format!(
            "recovery-tail-{}",
            crate::util::opaque_id("test").unwrap()
        ));
        let complete=serde_json::to_vec(&json!({"kind":"session_started","session":"s","at":"now","previousSessionEnd":"none","candidate":"c"})).unwrap();
        for tail in [
            complete.clone(),
            br#"{"kind":"session_started","session":"torn"#.to_vec(),
        ] {
            std::fs::write(&path, &tail).unwrap();
            let error = RecoveryLedger::open(path.clone()).err().unwrap();
            assert!(error.contains("not newline-closed"));
            assert_eq!(std::fs::read(&path).unwrap(), tail);
            std::fs::remove_file(&path).unwrap();
        }
        // An already-open owner must also refuse after a torn/unclosed append,
        // including a partial-write retry; opening once is not enough.
        for tail in [complete, br#"{"kind":"session_started"#.to_vec()] {
            let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
            std::fs::write(&path, &tail).unwrap();
            let error = ledger.start_session("new", "c").unwrap_err();
            assert!(error.contains("unclosed final record"));
            assert_eq!(std::fs::read(&path).unwrap(), tail);
            assert_eq!(ledger.snapshot()["entries"], json!([]));
            std::fs::remove_file(&path).unwrap();
        }
        // The same complete JSON with its committed delimiter remains usable.
        let mut closed=serde_json::to_vec(&json!({"kind":"session_started","session":"s","at":"now","previousSessionEnd":"none","candidate":"c"})).unwrap();
        closed.push(b'\n');
        std::fs::write(&path, &closed).unwrap();
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        ledger.start_session("new", "c").unwrap();
        assert_eq!(
            RecoveryLedger::open(path.clone()).unwrap().snapshot()["entries"]
                .as_array()
                .unwrap()
                .len(),
            2
        );
        std::fs::remove_file(&path).unwrap();
    }
}

#[cfg(test)]
mod transition_repair_tests {
    use super::*;
    #[test]
    fn receipt_errors_and_observed_ack_use_their_adopted_custody_rows() {
        let path = std::env::temp_dir().join(format!(
            "recovery-rows-{}",
            crate::util::opaque_id("test").unwrap()
        ));
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        let mut request = json!({"generation":{"appSession":"s","home":"h","spawnCounter":1},"requestId":1,"method":"future/request","classification":"unfamiliar","state":"errored","replyWriteResult":"write-failed","acknowledgment":"not-observed","settlement":{"origin":"app-explicit-error"}});
        ledger.request_summary(&request).unwrap();
        assert_eq!(ledger.snapshot()["entries"][0]["transition"], "RQ-08");
        request["requestId"] = json!(2);
        request["method"] = json!("item/fileChange/requestApproval");
        request["classification"] = json!("known-answerable");
        request["state"] = json!("declined");
        request["replyWriteResult"] = json!("written");
        request["settlement"] = json!({"origin":"app-rule:invented-negative"});
        ledger.request_summary(&request).unwrap();
        assert_eq!(ledger.snapshot()["entries"][1]["transition"], "RQ-03");
        request["nativeParameters"] = json!({"threadId":"t"});
        request["acknowledgment"] = json!({"observed":"serverRequest/resolved after written reply","generation":request["generation"],"native":{"threadId":"t","requestId":request["requestId"]}});
        ledger.request_summary(&request).unwrap();
        assert_eq!(ledger.snapshot()["entries"][2]["transition"], "RQ-09");
        assert_eq!(
            ledger.snapshot()["entries"][2]["acknowledgment"],
            "observed"
        );
        std::fs::remove_file(path).unwrap();
    }
}

#[cfg(test)]
mod connected_transition_repair_tests {
    use super::*;
    use crate::native_requests::RequestRegister;
    #[test]
    fn actual_reducer_error_settlement_ack_and_closure_map_to_distinct_rows() {
        let path = std::env::temp_dir().join(format!(
            "recovery-connected-{}",
            crate::util::opaque_id("test").unwrap()
        ));
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        let mut r = RequestRegister::default();
        let g = json!({"appSession":"s","home":"h","spawnCounter":1});
        r.receive(
            &g,
            1,
            &json!({"id":1,"method":"future/request","params":{"threadId":"t"}}),
            &json!({}),
        )
        .unwrap();
        r.written(&g, &json!(1), false);
        r.resolved(&g, &json!({"threadId":"t","requestId":1}));
        ledger.request_summary(&r.entries()[0]).unwrap();
        assert_eq!(ledger.snapshot()["entries"][0]["transition"], "RQ-08");
        assert_eq!(
            ledger.snapshot()["entries"][0]["acknowledgment"],
            "not-observed"
        );
        for id in [2, 3, 4] {
            r.receive(&g,id,&json!({"id":id,"method":"item/fileChange/requestApproval","params":{"threadId":"t"}}),&json!({})).unwrap();
            ledger.request_summary(r.entries().last().unwrap()).unwrap();
            if id != 4 {
                r.prepare(
                    &g,
                    &json!(id),
                    &json!({"decision":"decline"}),
                    "app-rule:invented-negative",
                    None,
                )
                .unwrap();
                r.written(&g, &json!(id), true);
                ledger.request_summary(r.entries().last().unwrap()).unwrap();
            }
        }
        r.resolved(&g, &json!({"threadId":"t","requestId":2}));
        ledger.request_summary(&r.entries()[1]).unwrap();
        r.close(&g);
        for entry in r.entries() {
            ledger.request_summary(&entry).unwrap();
        }
        let entries = ledger.snapshot()["entries"].as_array().unwrap().clone();
        let rows = |id: u64| {
            entries
                .iter()
                .filter(|e| e["requestIdentity"] == id.to_string())
                .map(|e| e["transition"].as_str().unwrap())
                .collect::<Vec<_>>()
        };
        assert_eq!(rows(1), vec!["RQ-08"]);
        assert_eq!(rows(2), vec!["RQ-01", "RQ-03", "RQ-09"]);
        assert_eq!(rows(3), vec!["RQ-01", "RQ-03", "RQ-05"]);
        assert_eq!(rows(4), vec!["RQ-01", "RQ-04"]);
        std::fs::remove_file(path).unwrap();
    }
}

#[cfg(test)]
mod reviewed_later_error_adoption_tests {
    use super::*;
    use crate::native_requests::RequestRegister;
    fn g() -> Value {
        json!({"appSession":"s","home":"h","spawnCounter":1})
    }
    fn path() -> PathBuf {
        std::env::temp_dir().join(format!(
            "recovery-rt-adoption-{}",
            crate::util::opaque_id("test").unwrap()
        ))
    }
    fn receive(r: &mut RequestRegister, id: u64, method: &str) {
        r.receive(
            &g(),
            id,
            &json!({"id":id,"method":method,"params":if method=="mcpServer/elicitation/request" {json!({"threadId":"t","serverName":"invented-server","turnId":null,"mode":"url","message":"invented request","elicitationId":"invented-elicitation","url":"https://example.invalid/verification"})}else{json!({"threadId":"t"})}}),
            &json!({}),
        )
        .unwrap();
    }
    fn rows(ledger: &RecoveryLedger, id: u64) -> Vec<String> {
        ledger.snapshot()["entries"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|e| e["requestIdentity"] == id.to_string())
            .map(|e| e["transition"].as_str().unwrap().into())
            .collect()
    }
    #[test]
    fn actual_later_error_write_ack_failure_and_closure_adopt_rt14_rt15() {
        let path = path();
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        let mut r = RequestRegister::default();
        for (id, origin, success) in [
            (1, "app-rule:invented", true),
            (2, "app-explicit-error", true),
            (3, "app-rule:invented", false),
        ] {
            receive(&mut r, id, "mcpServer/elicitation/request");
            ledger.request_summary(r.entries().last().unwrap()).unwrap();
            assert_eq!(
                r.entries().last().unwrap()["nativeParameters"]["turnId"],
                Value::Null
            );
            assert!(ledger.snapshot()["entries"]
                .as_array()
                .unwrap()
                .last()
                .unwrap()["subject"]
                .get("turnId")
                .is_none());
            r.prepare_error(
                &g(),
                &json!(id),
                &json!({"code":-32603,"message":"invented error","data":{"preserve":"native"}}),
                origin,
            )
            .unwrap();
            r.written(&g(), &json!(id), success);
            ledger.request_summary(r.entries().last().unwrap()).unwrap();
            assert_eq!(r.entries().last().unwrap()["laterProtocolError"], true);
            assert_eq!(
                r.entries().last().unwrap()["state"],
                if success {
                    "errored"
                } else {
                    "settle-write-failed"
                }
            );
        }
        let foreign = json!({"appSession":"foreign","home":"h","spawnCounter":1});
        r.resolved(&foreign, &json!({"threadId":"t","requestId":1}));
        assert_eq!(r.entries()[0]["acknowledgment"], "not-observed");
        r.resolved(&g(), &json!({"threadId":"t","requestId":1}));
        ledger.request_summary(&r.entries()[0]).unwrap();
        r.resolved(&g(), &json!({"threadId":"t","requestId":3}));
        ledger.request_summary(&r.entries()[2]).unwrap();
        assert_eq!(r.entries()[2]["acknowledgment"], "not-observed");
        r.close(&g());
        for entry in r.entries() {
            ledger.request_summary(&entry).unwrap();
        }
        assert_eq!(rows(&ledger, 1), vec!["RQ-01", "RQ-03", "RQ-09"]);
        assert_eq!(rows(&ledger, 2), vec!["RQ-01", "RQ-03", "RQ-05"]);
        assert_eq!(rows(&ledger, 3), vec!["RQ-01", "RQ-03"]);
        let before = ledger.snapshot();
        r.resolved(&g(), &json!({"threadId":"t","requestId":2}));
        ledger.request_summary(&r.entries()[1]).unwrap();
        assert_eq!(ledger.snapshot(), before);
        let entries = before["entries"].as_array().unwrap();
        assert!(entries
            .iter()
            .filter(|e| e["requestIdentity"] == "3")
            .any(|e| e["endedAs"] == "settle-write-failed"
                && e["replyWrite"] == "write-failed"
                && e["acknowledgment"] == "not-observed"));
        assert!(entries
            .iter()
            .filter(|e| e["requestIdentity"] == "1")
            .all(|e| e["origin"].is_null() || e["origin"] == "app-rule:invented"));
        assert_eq!(
            generation_from_ref(entries[0]["generation"].as_str().unwrap()).unwrap(),
            g()
        );
        std::fs::remove_file(path).unwrap();
    }
    #[test]
    fn receipt_errors_remain_rq08_and_refused_later_errors_create_no_summary() {
        let path = path();
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        let mut r = RequestRegister::default();
        for (id, method, success) in [(1, "future/request", true), (2, "item/tool/call", false)] {
            receive(&mut r, id, method);
            r.written(&g(), &json!(id), success);
            r.resolved(&g(), &json!({"threadId":"t","requestId":id}));
            ledger.request_summary(r.entries().last().unwrap()).unwrap();
            assert_eq!(r.entries().last().unwrap()["state"], "errored");
            assert_eq!(
                r.entries().last().unwrap()["laterProtocolError"],
                Value::Null
            );
            assert_eq!(rows(&ledger, id), vec!["RQ-08"]);
        }
        receive(&mut r, 3, "mcpServer/elicitation/request");
        ledger.request_summary(&r.entries()[2]).unwrap();
        let before = ledger.snapshot();
        let state = r.entries();
        for origin in ["person-via-interaction", "agent", "app-rule:"] {
            assert!(r
                .prepare_error(
                    &g(),
                    &json!(3),
                    &json!({"code":-32603,"message":"invented"}),
                    origin
                )
                .is_err());
        }
        assert!(r
            .prepare_error(
                &g(),
                &json!(3),
                &json!({"message":"invalid"}),
                "app-rule:invented"
            )
            .is_err());
        assert_eq!(r.entries(), state);
        ledger.request_summary(&r.entries()[2]).unwrap();
        assert_eq!(ledger.snapshot(), before);
        std::fs::remove_file(path).unwrap();
    }
    #[test]
    fn receiving_guard_rejects_foreign_post_close_and_failed_write_ack_shapes() {
        let path = path();
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        let mut r = RequestRegister::default();
        receive(&mut r, 1, "mcpServer/elicitation/request");
        ledger.request_summary(&r.entries()[0]).unwrap();
        r.prepare_error(
            &g(),
            &json!(1),
            &json!({"code":-32603,"message":"invented"}),
            "app-rule:invented",
        )
        .unwrap();
        r.written(&g(), &json!(1), true);
        ledger.request_summary(&r.entries()[0]).unwrap();
        r.resolved(&g(), &json!({"threadId":"t","requestId":1}));
        let genuine = r.entries()[0].clone();
        let before = std::fs::read(&path).unwrap();
        let mut variants = Vec::new();
        let mut foreign = genuine.clone();
        foreign["acknowledgment"]["generation"]["appSession"] = json!("foreign");
        variants.push(foreign);
        let mut foreign_request = genuine.clone();
        foreign_request["acknowledgment"]["native"]["requestId"] = json!(2);
        variants.push(foreign_request);
        let mut after_close = genuine.clone();
        after_close["closedGeneration"] = json!(true);
        variants.push(after_close);
        let mut failed = genuine.clone();
        failed["state"] = json!("settle-write-failed");
        failed["replyWriteResult"] = json!("write-failed");
        variants.push(failed);
        for candidate in variants {
            assert!(ledger.request_summary(&candidate).is_err());
            assert_eq!(std::fs::read(&path).unwrap(), before);
        }
        ledger.request_summary(&genuine).unwrap();
        assert_eq!(rows(&ledger, 1), vec!["RQ-01", "RQ-03", "RQ-09"]);
        std::fs::remove_file(path).unwrap();
    }
}

/// Read-only custody projection issued by the owning Host. There is deliberately
/// no Deserialize/JSON constructor or conversion to a live source capability.
#[derive(Clone, Debug)]
pub struct RecoveryCustodyView { document: Value }
impl RecoveryCustodyView {
    pub fn snapshot(&self)->Value {self.document.clone()}
    pub(crate) fn from_owner(session:&str,ledger:Option<&Value>,live:Value,pending:usize,error:Option<&str>)->Self {
        let rows=ledger.and_then(|l|l["entries"].as_array()).cloned().unwrap_or_default();
        let mut limits=Vec::<String>::new();
        if ledger.is_none(){limits.push("App history unavailable; no cold execution custody established".into());}
        if pending>0{limits.push("Captured pointer observations remain unpersisted; restart coverage is incomplete".into());}
        if let Some(error)=error{limits.push(error.into());}
        let starts:Vec<_>=rows.iter().enumerate().filter(|(_,r)|r["kind"]=="session_started").collect();
        let current=starts.iter().rev().find(|(_,r)|r["session"]==session).map(|(_,r)|*r);
        let prior=current.and_then(|r|r["previousSession"].as_str());
        let end=prior.and_then(|s|rows.iter().rev().find(|r|r["kind"]=="session_ended"&&r["session"]==s));
        // Delayed old source appends cannot eclipse a later App session or a
        // later generation of the same physical home. Equal-thread references
        // in different home namespaces are never merged.
        let mut latest=std::collections::BTreeMap::<(String,String,String),(usize,u64,usize,Value)>::new();
        let mut metadata=std::collections::BTreeMap::<(String,String,String),(usize,usize,Value)>::new();
        for (position,row) in rows.iter().enumerate().filter(|(_,r)|r["kind"]=="conversation_index") {
            let Some(reference)=row["lastLoadedGeneration"].as_str() else{continue;};
            let Ok(g)=generation_from_ref(reference) else{limits.push("Historical execution row lacks canonical full generation; retained in ledger, not joined".into());continue;};
            let Some(rank)=starts.iter().find(|(_,s)|s["session"]==g["appSession"]).map(|(n,_)|*n) else{limits.push("Historical execution source session start unavailable; not joined".into());continue;};
            let Some(append_rank)=starts.iter().find(|(_,s)|s["session"]==row["session"]).map(|(n,_)|*n) else{limits.push("Historical metadata append session start unavailable; not joined".into());continue;};
            let (Some(home),Some(thread),Some(physical))=(row["home"].as_str(),row["threadId"].as_str(),g["home"].as_str()) else{continue;};
            let key=(home.to_string(),physical.to_string(),thread.to_string());
            if metadata.get(&key).is_none_or(|(a,b,_)|(append_rank,position)>(*a,*b)){metadata.insert(key.clone(),(append_rank,position,row.clone()));}
            let order=(rank,g["spawnCounter"].as_u64().unwrap(),position);
            if latest.get(&key).is_none_or(|(a,b,c,_)|order>(*a,*b,*c)) {latest.insert(key,(order.0,order.1,order.2,row.clone()));}
        }
        let mut historical=Vec::new();let mut events=Vec::new();
        for (key,(_,_,_,row)) in latest {
            let thread=&key.2;
            let execution=&row["lastObservedExecution"];
            let source=generation_from_ref(row["lastLoadedGeneration"].as_str().unwrap()).unwrap();
            let is_prior=prior.is_some_and(|p|source["appSession"]==p);
            let live_turn=execution["liveTurn"].as_str().filter(|s|!s.is_empty());
            if is_prior&&matches!(execution["state"].as_str(),Some("turn-live"|"interrupt-pending"|"observation-lost")) {
                if let Some(turn)=live_turn {
                    // A clean session end does not prove a live turn survived to
                    // quit. Only a captured app-quit loss supplies that reading.
                    let prior_end=match end {
                        None=>Some("ended-without-record"),
                        Some(e) if e["how"]=="system-terminated"=>Some("system-terminated"),
                        Some(_) if execution["lostCause"]=="app-quit"=>Some("quit-with-live-work"),
                        _=>None,
                    };
                    if let (Some(prior_end),Some(current))=(prior_end,current) {
                        events.push(json!({"kind":"app_restart_interruption","eventId":format!("cev:restart:{}:{}:{}",session,row["lastLoadedGeneration"].as_str().unwrap(),thread),"appSession":session,"at":current["at"],"standing":"App-observed","threadId":thread,"home":row["home"],"priorSession":source["appSession"],"priorSessionEnd":prior_end,"liveTurnsAtEnd":[{"threadId":thread,"turnId":turn}]}));
                    } else {limits.push(format!("{thread}: prior loss/live observation retained; live work at clean App end is not established"));}
                }
            }
            let associations=execution["openItems"].as_array().into_iter().flatten().map(|item| {
                let turn=item["turnId"].as_str().filter(|s|!s.is_empty());
                json!({"generation":source,"home":row["home"],"threadId":thread,"turnId":turn,"itemId":item["itemId"],"itemType":item["itemType"],"correlation":if turn.is_some(){"known persisted association"}else{"unknown; historical row supplies no per-item turn"},"fullTuple":turn.map(|turn|json!({"generation":source,"home":row["home"],"threadId":thread,"turnId":turn,"itemId":item["itemId"]})),"standing":"Historical App pointer; not current liveness, recovered native content or operation authority"})
            }).collect::<Vec<_>>();
            historical.push(json!({"index":row,"metadataIndex":metadata.get(&key).map(|(_,_,r)|r),"executionGeneration":source,"standing":"Last persisted App execution pointer observation; metadataIndex preserves latest append provenance separately; neither is current Codex state or live authority","openItemAssociations":associations,"openItemCorrelation":"Per-item known/unknown from persisted turnId only; never backfilled from liveTurn, selection, tags or native history.","nativeHistory":"read separately from Codex; not supplied by this projection"}));
        }
        Self{document:json!({"live":live,"restartEvents":events,"historicalConversations":historical,"pendingPointerFacts":pending,"limits":limits,"standing":"App-observed metadata only; no native history, human act, workflow run or external operation inferred","automaticResume":false})}
    }
}
