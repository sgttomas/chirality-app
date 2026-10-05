//! Stock Codex hosting boundary, main-process side.
//!
//! Implements a thin subset of DEL-01-01 HOSTING_BOUNDARY.md (v0.9):
//! - §4.1/§4.7 lifecycle states and the LT rows on the start and stop paths
//!   (LT-01, LT-04, LT-05, LT-06, LT-09, LT-10, LT-12, LT-17, LT-23), each
//!   written as a `hosting.lifecycle-event.schema.json` record;
//! - §4.2 start: resolve, verify (§7.2), spawn with an App-owned CODEX_HOME,
//!   handshake (`initialize` with the declared capabilities, then the
//!   `initialized` notice), ready;
//! - §5 framing (newline-delimited JSON, version member not required),
//!   classification, correlation, and §5.1/§5.2 client-request records
//!   (`hosting.client-request-record.schema.json`);
//! - invariants H2 (only this process holds the pipe), H4 (frames before
//!   ready are held and delivered in order with ready), H5 (generation tag on
//!   every frame and record), H6 (native frames kept unchanged, metadata
//!   beside them), H7 (no notification opt-out; malformed frames counted and
//!   surfaced), H10 (no response observed -> unknown), H11 (the child runs in
//!   its own process group; a stop ends the group).
//!
//! Runtime core adds §6 request custody and native answer/error paths, atomic
//! cursor re-attachment snapshots and optional durable summary recording.
//! Still outstanding: automatic restart rules (§4.4), native recovery reads,
//! quit/relaunch integration and the per-home configuration link.

#[path = "attachment_custody.rs"]
pub mod attachment_custody;
use attachment_custody::AttachmentCustody;
#[path = "auth_rpc.rs"]
pub(crate) mod auth_rpc;
use crate::attachments::{self, PreparedAttachmentList, SelectedTextAttachment};
use crate::native_requests::RequestRegister;
use crate::native_history::{HistoryQuery, NativeHistory};
use crate::recovery::RecoveryLedger;
use crate::util::{now_rfc3339, opaque_id, sha256_hex};
use serde_json::{json, Value};
use std::collections::{HashMap, VecDeque};
use std::io::{BufRead, BufReader, Read, Write};
use std::os::unix::process::CommandExt;
use std::path::PathBuf;
use std::process::{Child, ChildStdin, Command, Stdio};
use std::sync::mpsc::{channel, Receiver, Sender};
use std::sync::{Arc, Condvar, Mutex, Weak};
use std::time::Duration;

/// The pin the App candidate declares (HOSTING §7.1, D4).
pub const DECLARED_PIN: &str = "0.160.0";
/// Generated-output identity: the pin and generator the protocol types came from
/// (HOSTING §7.0; maintained supplier resources mirror Design/generated/0.160.0).
pub const GENERATED_OUTPUT_IDENTITY: &str =
    "codex app-server generate-json-schema --experimental @ 0.160.0 (manifest sha256 411ea5d47035908768562eecfed33f16e2cb3de944c84c96fd8e70ca7086b8be; root sha256 7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5; v2 sha256 e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c)";

/// Environment variables never passed to the child (ACCESS CR-7: no credential variable).
const CREDENTIAL_VARS: &[&str] = &[
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
    "OPENAI_ORG_ID",
    "OPENAI_PROJECT_ID",
    "AZURE_OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
];

#[derive(Clone, Debug)]
pub struct HostConfig {
    /// The supplier distribution's binary (resolved from CHIRALITY_CODEX_BIN by the caller).
    pub codex_bin: PathBuf,
    /// The App-owned account home (HOSTING §4.2 step 3). Never the person's real home.
    pub codex_home: PathBuf,
    /// A separate probe home for the version label probe (HOSTING §7.2, H-probe).
    pub probe_home: PathBuf,
    /// Working directory of the child.
    pub cwd: PathBuf,
    /// Optional main-binary development assertion. A match cannot qualify the
    /// full executed distribution; a mismatch always refuses the start.
    pub expected_sha256: Option<String>,
    /// HOSTING §7.2 / U-06: run an unverified distribution for development, labelled so.
    pub allow_unverified_dev: bool,
    /// Session flags (`-c key=value`), the K-12 traffic settings (ACCESS §9).
    pub session_flags: Vec<String>,
    /// Wait limit for the handshake and for requests (value unselected in HOSTING).
    pub wait_limit: Duration,
}

impl HostConfig {
    pub fn new(codex_bin: PathBuf, codex_home: PathBuf, probe_home: PathBuf, cwd: PathBuf) -> Self {
        HostConfig {
            codex_bin,
            codex_home,
            probe_home,
            cwd,
            expected_sha256: None,
            allow_unverified_dev: false,
            // ACCESS §9 K-12: analytics off in the session flags. Plugins follow the
            // person's own setting (L-3), so the App passes nothing for them.
            session_flags: vec!["analytics.enabled=false".into()],
            wait_limit: Duration::from_secs(20),
        }
    }
}

#[derive(Default)]
struct Inner {
    state: String,
    generation: Value,
    app_session: String,
    home: String,
    supplier_standing: Option<String>,
    spawn_counter: u64,
    attachment_pipe_epoch: u64,
    lifecycle: Vec<Value>,
    client_requests: Vec<Value>,
    /// Frames received before ready (H4), in received order.
    held: Vec<Value>,
    /// Frames delivered to receivers, in received order, each {generation, position, class, frame}.
    journal: Vec<Value>,
    receipt_position: u64,
    malformed: u64,
    pending: HashMap<String, (usize, Sender<Value>)>,
    source_requests: HashMap<String, SourceEvidence>,
    server_requests: RequestRegister,
    recovery: Option<Arc<Mutex<RecoveryLedger>>>,
    recovery_snapshot: Option<Value>,
    pending_recovery: VecDeque<Value>,
    recovery_projection_errors: Vec<Value>,
    submission_contexts: Vec<Value>,
    account_channels: Vec<Value>,
    recovery_error: Option<String>,
    next_id: u64,
    send_position: u64,
    version_identity: Option<Value>,
    verification: Option<Value>,
    declared_capabilities: Option<Value>,
    configuration_identity: Option<Value>,
    stop_record: Option<Value>,
    threads: Vec<Value>,
    conversation_turns: Vec<Value>,
    turn_request_threads: HashMap<String, (Value, String, u64)>,
    interrupt_requests: Vec<Value>,
    stderr_bytes: u64,
    child_pid: Option<i32>,
}

// Non-deserializable capabilities issued only by the actual Host sender.
#[derive(Clone)]
pub struct SourceRequest {
    source: Weak<(Mutex<Inner>, Condvar)>,
    generation: Value,
    frame: Value,
    request_ref: String,
    receiver: Arc<Mutex<Receiver<Value>>>,
}
struct SourceEvidence {
    request: SourceRequest,
    index: usize,
    written: bool,
    write_error: Option<String>,
    response: Option<Value>,
    attachment: Option<AttachmentLink>,
    reserved_sender: Option<Sender<Value>>,
    write_attempt_in_progress: bool,
    attempt_position: Option<u64>,
    response_position: Option<u64>,
    observation_base: Value,
    source_limit: Option<String>,
    auth_projection: bool,
    auth_policy_standing: Option<String>,
    auth_response_shape: Option<bool>,
}
impl SourceRequest {
    pub fn generation(&self) -> &Value { &self.generation }
    pub fn request_id(&self) -> &Value { &self.frame["id"] }
    pub fn request_ref(&self) -> &str { &self.request_ref }
    pub fn attempted_frame(&self) -> &Value { &self.frame }
    pub fn evidence(&self) -> Value {
        let Some(source) = self.source.upgrade() else {return json!({"outcome":"source-host-unavailable"});};
        let i = source.0.lock().unwrap();
        let Some(e) = i.source_requests.get(&self.frame["id"].to_string()) else { return json!({"outcome":"source-record-unavailable"}); };
        let record = &i.client_requests[e.index];
        json!({"generation":self.generation,"home":self.generation["home"],"requestIdentity":self.frame["id"],"requestRef":self.request_ref,
            "frameEvidence":if e.auth_projection{"explicit redacted account projection; not original wire bytes"}else{"original source frame"},"sensitiveFieldsRedacted":e.auth_projection,"authPolicyStanding":e.auth_policy_standing,"authResponseShapeValid":e.auth_response_shape,"attemptedFrame":self.frame,"sentFrame":if e.written {Some(&self.frame)}else{None},"writeAttemptInProgress":e.write_attempt_in_progress,"effectiveWriteOutcome":if e.write_attempt_in_progress {"unknown while actual write is in progress"}else if e.written{"complete source write observed"}else{"no complete source write observed"},"lastClientObservation":record,"writeResult":if e.write_attempt_in_progress {"write-in-progress"}else if e.written {"written"}else if e.write_error.is_some(){"write-failed"}else if record["writeResult"]=="not-attempted"{"last-prewrite-observation"}else{"reserved/no complete write observation"},"actualWriteAttemptObserved":e.attempt_position.is_some(),"noAttemptCause":if e.attempt_position.is_none(){e.source_limit.as_ref()}else{None},"canonicalProjectionAvailable":record.is_object()&&e.source_limit.is_none()&&!(e.write_error.is_some()&&e.response.is_some()),"sourceLimit":e.source_limit,
            "outcome":if e.write_attempt_in_progress{json!("unknown/in-progress")}else if e.write_error.is_some()&&e.response.is_some(){json!("native response and failed write both observed; canonical projection unavailable")}else if e.written&&e.response.is_some()&&e.source_limit.is_some(){json!(if e.response.as_ref().unwrap().get("result").is_some(){"response-observed-result"}else{"response-observed-error"})}else if record.is_object(){record["outcome"].clone()}else if e.written&&e.response.is_some(){json!(if e.response.as_ref().unwrap().get("result").is_some(){"response-observed-result"}else{"response-observed-error"})}else{json!("reserved/canonical projection unavailable; outcome unknown")},
            "waitingEnded":record.get("waitingEnded").and_then(Value::as_bool).or_else(||e.observation_base.get("waitingEnded").and_then(Value::as_bool)).unwrap_or(false),"response":e.response,"writeError":e.write_error,
            "sourceCurrent":i.generation==self.generation&&i.state=="ready"&&!i.server_requests.is_closed(&self.generation)})
    }
}
#[derive(Clone)]
pub struct HistoryDispatch { query: HistoryQuery, source: SourceRequest }
impl HistoryDispatch {
    pub fn query(&self) -> &HistoryQuery { &self.query }
    pub fn source(&self) -> &SourceRequest { &self.source }
    pub fn evidence(&self) -> Value { self.source.evidence() }
}

struct AttachmentLink { custody: Arc<AttachmentCustody>, records: Vec<Value>, original: Value, limit: Option<String> }
/// One-shot transient packet. No deserialization or durable native inputs.
pub struct PreparedAttachmentDispatch {
    source: SourceRequest,
    custody: Arc<AttachmentCustody>,
    list: PreparedAttachmentList,
    selections: Vec<SelectedTextAttachment>,
    client: Value,
    pipe_identity: (u64,u64),
    pipe_epoch: u64,
    state: Mutex<&'static str>,
}
impl PreparedAttachmentDispatch {
    pub fn submission_ref(&self)->&str {self.list.submission_ref()}
    pub fn source(&self)->&SourceRequest {&self.source}
    pub fn supply_records(&self)->Vec<Value>{self.list.supply_records()}
    pub fn cancel(&self)->bool{let mut state=self.state.lock().unwrap();if matches!(*state,"prepared"|"validating"){*state="cancelled";true}else{false}}
    pub fn state(&self)->&'static str{*self.state.lock().unwrap()}
}

struct BoundPipe { file: std::fs::File, generation: Value, epoch: u64, identity: (u64,u64) }

pub struct Host {
    recovery_writer: Mutex<()>,
    frame_write: Mutex<()>,
    attachment_gate: Mutex<()>,
    inner: Arc<(Mutex<Inner>, Condvar)>,
    stdin: Mutex<Option<ChildStdin>>,
    child: Mutex<Option<Child>>,
    #[cfg(test)]
    before_thread_insert: Mutex<Option<Box<dyn FnOnce() + Send>>>,
    #[cfg(test)]
    before_turn_result: Mutex<Option<Box<dyn FnOnce() + Send>>>,
    #[cfg(test)]
    before_eof_gate: Mutex<Option<Box<dyn FnOnce() + Send>>>,
}

impl Default for Host {
    fn default() -> Self {
        Self::new()
    }
}

impl Host {
    pub fn new() -> Self {
        let inner = Inner {
            state: "absent".into(),
            generation: Value::Null,

            ..Default::default()
        };
        Host {
            recovery_writer: Mutex::new(()),
            frame_write: Mutex::new(()),
            attachment_gate: Mutex::new(()),
            inner: Arc::new((Mutex::new(inner), Condvar::new())),
            stdin: Mutex::new(None),
            child: Mutex::new(None),
            #[cfg(test)]
            before_thread_insert: Mutex::new(None),
            #[cfg(test)]
            before_turn_result: Mutex::new(None),
            #[cfg(test)]
            before_eof_gate: Mutex::new(None),
        }
    }

    fn lt(&self, inner: &mut Inner, id: &str, event: &str, to: &str, extra: Value) {
        let gen = inner.generation.clone();
        let mut rec = json!({
            "recordKind": "lifecycle-event",
            "sequence": inner.lifecycle.len() + 1,
            "transitionId": id,
            "generation": gen,
            "fromState": inner.state,
            "event": event,
            "toState": to,
            "at": now_rfc3339(),
        });
        if let (Some(o), Value::Object(e)) = (rec.as_object_mut(), extra) {
            for (k, v) in e {
                o.insert(k, v);
            }
        }
        if let Some(standing) = &inner.supplier_standing {
            rec["supplierStanding"] = json!(standing);
        }
        inner.lifecycle.push(rec);
        inner.state = to.to_string();
        self.inner.1.notify_all();
    }

    pub fn state(&self) -> String {
        self.inner.0.lock().unwrap().state.clone()
    }

    /// A snapshot for the interface: state, generation, identity records, lifecycle
    /// events, client requests, delivered frames (H6: native frames unchanged), threads.
    pub fn snapshot(&self) -> Value {let i=self.inner.0.lock().unwrap();Self::snapshot_inner(&i)}
    fn snapshot_inner(i: &Inner) -> Value {
        json!({
            "state": i.state,
            "generation": i.generation,
            "supplierStanding": i.supplier_standing,
            "networkDisclosure": network_disclosure(),
            "verification": i.verification,
            "versionIdentity": i.version_identity,
            "declaredCapabilities": i.declared_capabilities,
            "configurationIdentity": i.configuration_identity,
            "lifecycle": i.lifecycle,
            "clientRequests": i.client_requests.iter().filter(|r|r.is_object()).cloned().collect::<Vec<_>>(),
            "clientRequestObservationStanding": "Canonical rows are last observations; an in-flight native write has unknown current outcome, never a current no-send or complete-write proof.",
            "reservedNativeRequests": i.source_requests.values().filter(|e|!i.client_requests[e.index].is_object()).map(|e|json!({"generation":e.request.generation,"requestIdentity":e.request.request_id(),"method":e.request.frame["method"],"effectiveOutcome":"unknown/reserved; no complete write proof","writeAttemptInProgress":e.write_attempt_in_progress,"waitingEnded":e.observation_base.get("waitingEnded").and_then(Value::as_bool).unwrap_or(false)})).collect::<Vec<_>>(),
            "inFlightNativeWrites": i.source_requests.values().filter(|e|e.write_attempt_in_progress).map(|e|json!({"generation":e.request.generation,"requestIdentity":e.request.request_id(),"attemptPosition":e.attempt_position,"effectiveOutcome":"unknown/in-progress","lastClientObservationOnly":true})).collect::<Vec<_>>(),
            "serverRequests": i.server_requests.records(),
            "recovery": i.recovery_snapshot,"recoveryPendingObservations":i.pending_recovery,"recoveryProjectionLimits":i.recovery_projection_errors,
            "recoveryPersistenceError": i.recovery_error,
            "journal": i.journal,
            "malformedFrames": i.malformed,
            "threads": i.threads,
            "conversationTurns": i.conversation_turns,
            "turnInterruptRequests": i.interrupt_requests.iter().map(|entry| {
                let request = i.client_requests.iter().find(|r| r["generation"] == entry["generation"] && r["requestIdentity"] == entry["requestIdentity"]);
                json!({"binding":entry,"clientRequest":request,"turnOutcome":"determined by native turn events, not interrupt acknowledgment"})
            }).collect::<Vec<_>>(),
            "modelTurnExercised": if i.source_requests.values().any(|e|e.request.frame["method"]=="turn/start")||i.client_requests.iter().any(|r| r["method"] == "turn/start") { Value::Null } else { json!(false) },
            "modelTurnEvidence": {"standing":"provider/model execution not established by request or mock result", "protocolRequests":i.client_requests.iter().filter(|r| r["method"] == "turn/start").collect::<Vec<_>>()},
        })
    }

    /// Open an App-local pointer ledger before start; never a native-content cache.
    pub fn configure_recovery(&self,path:PathBuf)->Result<(),String>{
        let _writer=self.recovery_writer.lock().unwrap();let session={let mut i=self.inner.0.lock().unwrap();if i.state!="absent"{return Err("recovery must be configured before supplier start".into());}if i.app_session.is_empty(){i.app_session=opaque_id("app-session:")?;}i.app_session.clone()};
        let mut ledger=RecoveryLedger::open(path)?;ledger.start_session(&session,"chirality-app-v4-unqualified")?;let snapshot=ledger.snapshot();let mut i=self.inner.0.lock().unwrap();if i.state!="absent"||i.app_session!=session{return Err("recovery configuration source changed during IO; not attached".into());}i.recovery=Some(Arc::new(Mutex::new(ledger)));i.recovery_snapshot=Some(snapshot);Ok(())
    }

    /// Snapshot then all later frames in receipt order. Detach is simply ceasing
    /// calls; it never touches the pipe. A foreign/closed cursor gets a gap marker.
    pub fn observe(&self, generation: &Value, after: u64) -> Value {
        let i = self.inner.0.lock().unwrap();
        let snapshot = Self::snapshot_inner(&i);
        let gap = *generation != i.generation || after > i.receipt_position || !matches!(i.state.as_str(), "ready" | "handshaking");
        let frames: Vec<_> = i.journal.iter().filter(|e| {
            e["generation"] == i.generation && e["position"].as_u64().map(|p| gap || p > after).unwrap_or(false)
        }).cloned().collect();
        json!({"snapshot":snapshot,"generation":i.generation,"position":i.receipt_position,"gap":gap,"frames":frames})
    }
    fn persist_requests(i:&mut Inner){
        if i.recovery.is_none(){return;}
        for request in i.server_requests.entries(){let mut history=i.recovery_snapshot.as_ref().and_then(|s|s["entries"].as_array()).cloned().unwrap_or_default();history.extend(i.pending_recovery.iter().cloned());match RecoveryLedger::request_summary_entry(&request,&history){Ok(Some(entry))=>i.pending_recovery.push_back(entry),Ok(None)=>{},Err(error)=>{i.recovery_error=Some(error.clone());i.recovery_projection_errors.push(json!({"generation":request["generation"],"requestIdentity":request["requestId"],"method":request["method"],"limit":error,"standing":"pointer projection unavailable; original request source retained"}));}}}
    }
    /// Nonblocking writer admission: captured facts stay queued when another
    /// actual writer owns IO. No service/store or silent drop is introduced.
    pub fn flush_recovery_observations(&self)->Value{
        let _writer=match self.recovery_writer.try_lock(){Ok(writer)=>writer,Err(_)=>{let mut i=self.inner.0.lock().unwrap();if !i.pending_recovery.is_empty(){i.recovery_error=Some("REC writer busy; captured pointer observations remain queued/unpersisted".into());}return json!({"pending":i.pending_recovery.len(),"standing":"writer busy; captured facts retained"});}};
        self.drain_recovery_owned()
    }
    /// Caller owns recovery_writer, with no Inner guard held.
    fn drain_recovery_owned(&self)->Value {
        let(ledger,entries)={let i=self.inner.0.lock().unwrap();(i.recovery.clone(),i.pending_recovery.iter().cloned().collect::<Vec<_>>())};let Some(ledger)=ledger else{return json!({"standing":"ledger unavailable","pending":entries.len()});};
        let mut stored=0;let mut error=None;let snapshot={let mut ledger=ledger.lock().unwrap();for entry in &entries{if let Err(reason)=ledger.append(entry.clone()){error=Some(reason);break;}stored+=1;}ledger.snapshot()};
        let mut i=self.inner.0.lock().unwrap();for entry in entries.iter().take(stored){if i.pending_recovery.front()==Some(entry){i.pending_recovery.pop_front();}else{i.recovery_error=Some("REC captured observation order conflict; facts retained".into());break;}}
        i.recovery_snapshot=Some(snapshot);if let Some(error)=error{i.recovery_error=Some(error);}else if i.pending_recovery.is_empty(){i.recovery_error=None;}json!({"appended":stored,"pending":i.pending_recovery.len(),"limit":i.recovery_error})
    }


    fn context_scope(i:&Inner,generation:&Value,thread:&str,home:Option<&str>)->Result<(),String>{
        crate::recovery::generation_ref(generation)?;if i.generation!=*generation||i.state!="ready"||i.server_requests.is_closed(generation)||thread.is_empty()||!i.threads.iter().any(|t|t["generation"]==*generation&&t["threadId"]==thread){return Err("context source is not current operational home/thread/full generation".into());}
        if home.is_some_and(|h|!matches!(h,"H-acct"|"H-key")){return Err("REC home class must come actual configured ACCESS home kind or absence".into());}Ok(())
    }
    fn context_rows(snapshot:Option<&Value>)->Vec<Value>{snapshot.and_then(|v|v["entries"].as_array()).map(|rows|rows.iter().filter(|e|e["kind"]=="conversation_index").cloned().collect()).unwrap_or_default()}
    /// New CURRENT known admission only; historical P is never overwritten by Q.
    pub fn observe_conversation_project(&self,generation:&Value,thread:&str,home:Option<&str>,context:&crate::recovery::ExplicitAppProjectContext)->Result<Value,String>{
        {let i=self.inner.0.lock().unwrap();Self::context_scope(&i,generation,thread,home)?;}
        let _writer=self.recovery_writer.lock().unwrap();self.drain_recovery_owned();
        let(ledger,rows)={let i=self.inner.0.lock().unwrap();Self::context_scope(&i,generation,thread,home)?;(i.recovery.clone(),Self::context_rows(i.recovery_snapshot.as_ref()))};
        let existing=home.and_then(|h|rows.iter().rev().find(|e|e["home"]==h&&e["threadId"]==thread)).cloned();
        if let Some(index)=existing{return Ok(json!({"indexSnapshot":index,"projectContext":context.view(),"standing":"historical App index retained; current reference does not transfer/backfill it"}));}
        let(Some(home),Some(project),Some(ledger))=(home,context.reference(),ledger)else{return Ok(json!({"indexSnapshot":null,"projectContext":context.view(),"limit":"known owning home/project/index ledger absent: no project-bearing row; hot-only/cold lookup unavailable"}));};
        let at=now_rfc3339();let entry=json!({"kind":"conversation_index","session":generation["appSession"],"at":at,"threadId":thread,"home":home,"project":project,"tags":[],"lastObservedExecution":{"state":"indexed","at":at},"lastLoadedGeneration":crate::recovery::generation_ref(generation)?});
        {let i=self.inner.0.lock().unwrap();Self::context_scope(&i,generation,thread,Some(home))?;}
        let(result,snapshot)={let mut ledger=ledger.lock().unwrap();let result=ledger.append(entry.clone());(result,ledger.snapshot())};let mut i=self.inner.0.lock().unwrap();i.recovery_snapshot=Some(snapshot);if let Err(error)=result{i.recovery_error=Some(error.clone());return Ok(json!({"indexSnapshot":null,"projectContext":context.view(),"limit":format!("CURRENT index append unavailable: {error}; no durable association claimed")}));}
        let changed=i.generation!=*generation||i.server_requests.is_closed(generation);Ok(json!({"indexSnapshot":entry,"projectContext":context.view(),"standing":"CURRENT App admission observation indexed; not earlier-history/native provenance","scopeChangedDuringIO":changed}))
    }
    /// Owning NIR interpretation of existing REC opaque tags. Real prepared
    /// submission/native namespace remains the private Host source authority.
    pub fn bind_attachment_context(&self,prepared:&PreparedAttachmentDispatch,context:&crate::recovery::ExplicitAppProjectContext,home:Option<&str>)->Result<Value,String>{
        self.check_source(prepared.source())?;let generation=prepared.source().generation();let thread=prepared.source().attempted_frame()["params"]["threadId"].as_str().ok_or("prepared native thread absent")?;
        {let i=self.inner.0.lock().unwrap();Self::context_scope(&i,generation,thread,home)?;}
        let _writer=self.recovery_writer.lock().unwrap();self.drain_recovery_owned();
        let(ledger,rows,hot)={let i=self.inner.0.lock().unwrap();Self::context_scope(&i,generation,thread,home)?;(i.recovery.clone(),Self::context_rows(i.recovery_snapshot.as_ref()),i.submission_contexts.clone())};
        // All durable/hot claims constrain immutable token; index provenance
        // and current Root reference remain independent, never inferred by cwd.
        let index=home.and_then(|h|rows.iter().rev().find(|e|e["home"]==h&&e["threadId"]==thread)).cloned();
        let durable:Vec<Value>=rows.iter().flat_map(|e|e["tags"].as_array().into_iter().flatten().cloned()).collect();
        let hot_tags:Vec<Value>=hot.iter().map(|h|h["tag"].clone()).collect();
        let mut result=crate::recovery::submission_context_plan(index.as_ref(),&durable,&hot_tags,prepared.submission_ref(),context.reference())?;
        if hot.iter().any(|h|h["submissionRef"]==prepared.submission_ref()&&(h["nativeHome"]!=generation["home"]||h["threadId"]!=thread)){return Err("same submission token has conflicting native home/thread source; no rebinding".into());}
        let hot_entry=json!({"submissionRef":prepared.submission_ref(),"nativeHome":generation["home"],"generation":generation,"threadId":thread,"recoveryHome":home,"tag":result["tag"],"projectContext":context.view()});
        {let mut i=self.inner.0.lock().unwrap();Self::context_scope(&i,generation,thread,home)?;if !i.submission_contexts.iter().any(|h|h["submissionRef"]==prepared.submission_ref()){i.submission_contexts.push(hot_entry);}}
        result["projectContext"]=context.view();result["nativeScope"]=json!({"generation":generation,"threadId":thread,"standing":"source binding only; context tag is not native receipt/actor/run proof"});result["indexSnapshot"]=json!(index);
        let Some(index)=index else{result["persistence"]=json!("memory-only");result["limit"]=json!("project-bearing index/home class absent: no row, owning tag hot-only; cold lookup unavailable");return Ok(result);};
        if result["idempotent"]==true{result["persistence"]=json!(if result["durableBindingObserved"]==true{"recorded metadata observed"}else{"memory-only"});return Ok(result);}
        let Some(ledger)=ledger else{result["persistence"]=json!("memory-only");result["limit"]=json!("ledger unavailable; hot tag retained, cold lookup unavailable");return Ok(result);};
        let mut entry=index;entry["session"]=generation["appSession"].clone();entry["at"]=json!(now_rfc3339());entry["tags"].as_array_mut().ok_or("REC index tags absent")?.push(result["tag"].clone());
        {let i=self.inner.0.lock().unwrap();Self::context_scope(&i,generation,thread,home)?;}
        let(appended,snapshot)={let mut ledger=ledger.lock().unwrap();let appended=ledger.append(entry.clone());(appended,ledger.snapshot())};let mut i=self.inner.0.lock().unwrap();i.recovery_snapshot=Some(snapshot);result["scopeChangedDuringIO"]=json!(i.generation!=*generation||i.server_requests.is_closed(generation));
        match appended{Ok(())=>{result["indexSnapshot"]=entry;result["persistence"]=json!("durable App metadata");result["durableBindingObserved"]=json!(true);},Err(error)=>{i.recovery_error=Some(error.clone());result["persistence"]=json!("memory-only");result["limit"]=json!(format!("context append unavailable: {error}; hot binding retained, cold lookup unavailable"));}}
        Ok(result)
    }

    /// The child's process id, which is also its process-group id (H11).
    pub fn child_pid(&self) -> Option<i32> {
        self.inner.0.lock().unwrap().child_pid
    }
    pub fn lifecycle_events(&self) -> Vec<Value> {
        self.inner.0.lock().unwrap().lifecycle.clone()
    }
    pub fn client_requests(&self) -> Vec<Value> {
        self.inner.0.lock().unwrap().client_requests.iter().filter(|r|r.is_object()).cloned().collect()
    }
    pub fn journal(&self) -> Vec<Value> {
        self.inner.0.lock().unwrap().journal.clone()
    }

    /// HOSTING §7.1/§7.2: label probe in the probe home, content identity of the binary,
    /// generated-output identity naming the pin.
    fn verify(cfg: &HostConfig) -> (Value, Option<String>, Vec<Value>) {
        let mut probe = Command::new(&cfg.codex_bin);
        for name in CREDENTIAL_VARS { probe.env_remove(name); }
        let label = probe
            .arg("--version")
            .env("CODEX_HOME", &cfg.probe_home)

            .stdin(Stdio::null())
            .output();
        let label = match label {
            Ok(o) if o.status.success() => String::from_utf8_lossy(&o.stdout).trim().to_string(),
            Ok(o) => {
                return (
                    json!({"result": "unverifiable", "reason": format!("version probe exited with {:?}", o.status.code())}),
                    None,
                    vec![],
                )
            }
            Err(e) => {
                return (
                    json!({"result": "unverifiable", "reason": format!("distribution not found or not runnable: {e}")}),
                    None,
                    vec![],
                )
            }
        };
        // An observed contradiction cannot be downgraded by a later content-read failure.
        if label != format!("codex-cli {DECLARED_PIN}") {
            return (json!({"result": "mismatch", "element": "observed version label"}), Some(label), vec![]);
        }
        let content = match std::fs::read(&cfg.codex_bin) {
            Ok(b) => sha256_hex(&b),
            Err(e) => {
                return (
                    json!({"result": "unverifiable", "reason": format!("binary not readable: {e}")}),
                    Some(label),
                    vec![],
                )
            }
        };
        // Composition of the distribution identity is U-17; the skeleton hashes the main binary only.
        let dist = vec![json!({"path": "bin/codex", "identity": {"algorithm": "sha-256", "value": content}})];
        if !generated_outputs_match() {
            return (json!({"result": "mismatch", "element": "generated output identity"}), Some(label), dist);
        }
        match &cfg.expected_sha256 {
            Some(exp) if exp.eq_ignore_ascii_case(&content) => (
                json!({"result": "unverifiable", "reason": "main binary matches development assertion; qualified full distribution identity absent"}), Some(label), dist),
            Some(_) => (json!({"result": "mismatch", "element": "distribution content identity"}), Some(label), dist),
            None => (
                json!({"result": "unverifiable", "reason": "no expected distribution content identity recorded (pin not qualified)"}),
                Some(label),
                dist,
            ),
        }
    }

    /// HOSTING §4.2 start sequence. Returns the `ready` snapshot or the reason it did not get there.
    pub fn start(self: &Arc<Self>, cfg: &HostConfig, actor: &str) -> Result<Value, String> {
        {
            let mut i = self.inner.0.lock().unwrap();
            if !(i.state == "absent" || i.state == "stopped" || i.state == "refused") {
                return Err(format!("start not accepted in state {}", i.state));
            }
            if i.app_session.is_empty() { i.app_session = opaque_id("app-session:")?; }
            i.supplier_standing = None;
            i.version_identity = None;
            let id = match i.state.as_str() {
                "absent" => "LT-01",
                "stopped" => "LT-02",
                _ => "LT-03",
            };
            self.lt(&mut i, id, "start-requested", "verifying", json!({"actor": actor}));
        }
        // Steps 1-2: resolve and verify.
        let (result, label, dist) = Self::verify(cfg);
        let verified = result["result"] == "verified";
        let dev_ok = !verified && cfg.allow_unverified_dev && result["result"] == "unverifiable" && label.is_some();
        {
            let mut i = self.inner.0.lock().unwrap();
            i.verification = Some(result.clone());
            if !(verified || dev_ok) {
                self.lt(&mut i, "LT-05", "verification-failed", "refused", json!({"verificationResult": result}));
                return Err(format!("refused: {}", result));
            }
            // LT-24 explicitly permits labelled development; LT-04 remains verified-only.
            let extra = if verified {
                json!({"verificationResult": result})
            } else {
                json!({"verificationResult": result,
                       "reason": "U-06 development run: unverified distribution, not the pinned supplier"})
            };
            i.supplier_standing = Some(if verified { "verified" } else { "unverified-development" }.into());
            self.lt(&mut i, if verified { "LT-04" } else { "LT-24" },
                if verified { "verification-passed" } else { "development-start-authorized" }, "spawning", extra);
            i.version_identity = Some(json!({
                "declaredPin": DECLARED_PIN,
                "observedVersionLabel": label.clone().unwrap_or_default(),
                "distributionContentIdentity": dist,
                "launcherRecord": {"launcher": "vendor-binary", "addedEnvironment": []},
                "handshakeReportedIdentity": {},
                "handshakeConsistency": "no-version-found",
                "generatedOutputIdentity": GENERATED_OUTPUT_IDENTITY,
                "supplementIdentity": "empty at 0.160.0",
            }));
        }
        // Step 3: spawn.
        let mut args: Vec<String> = Vec::new();
        for f in &cfg.session_flags {
            args.push("-c".into());
            args.push(f.clone());
        }
        args.push("app-server".into());
        let mut cmd = Command::new(&cfg.codex_bin);
        cmd.args(&args)
            .current_dir(&cfg.cwd)
            .env("CODEX_HOME", &cfg.codex_home)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .process_group(0); // H11: the supplier and its descendants are one unit.
        for v in CREDENTIAL_VARS {
            cmd.env_remove(v);
        }
        let mut child = match cmd.spawn() {
            Ok(c) => c,
            Err(e) => {
                let mut i = self.inner.0.lock().unwrap();
                // LT-07/08: the restart bound is not implemented; one failure halts.
                self.lt(&mut i, "LT-08", "spawn-failed", "halted-after-repeated-failure",
                        json!({"failure": format!("spawn failed: {e}"), "failureCount": 1}));
                return Err(format!("spawn failed: {e}"));
            }
        };
        let stdout = child.stdout.take().unwrap();
        let stderr = child.stderr.take().unwrap();
        let source_gate = self.attachment_gate.lock().unwrap();
        *self.stdin.lock().unwrap() = child.stdin.take();
        let pid = child.id() as i32;
        *self.child.lock().unwrap() = Some(child);
        {
            let mut i = self.inner.0.lock().unwrap();
            i.spawn_counter += 1;
            i.attachment_pipe_epoch += 1;
            // Opaque stable home identity: never expose the filesystem path as identity.
            i.home = format!("app-home:{}", sha256_hex(cfg.codex_home.as_os_str().as_encoded_bytes()));
            i.generation = json!({"appSession": i.app_session, "home": i.home, "spawnCounter": i.spawn_counter});
            i.receipt_position = 0;
            i.held.clear();
            i.child_pid = Some(pid);
            i.stop_record = None;
            let conf = json!({
                "launcher": cfg.codex_bin.display().to_string(),
                "arguments": args,
                "environment": {"CODEX_HOME": "App-owned home (path recorded by the App, not here)"},
                "removedEnvironment": CREDENTIAL_VARS,
                "sessionFlags": cfg.session_flags,
            });
            i.configuration_identity = Some(conf.clone());
            if let Some(vi) = i.version_identity.as_mut() {
                vi["configurationIdentity"] = conf;
            }
            self.lt(&mut i, "LT-06", "spawned", "handshaking", json!({}));
        }
        drop(source_gate);
        let generation = self.inner.0.lock().unwrap().generation.clone();
        self.spawn_reader(stdout, generation.clone());
        self.spawn_stderr(stderr, generation);

        // Step 4: handshake.
        let caps = json!({"experimentalApi": true, "requestAttestation": false, "explicitGatewayOauth": true});
        let params = json!({
            "clientInfo": {"name": "chirality-app-v4", "title": "Chirality App v4 (walking skeleton)", "version": env!("CARGO_PKG_VERSION")},
            "capabilities": caps,
        });
        self.inner.0.lock().unwrap().declared_capabilities = Some(caps.clone());
        let resp = self.request_inner("initialize", params, json!({"kind": "app-rule", "name": "handshake"}), cfg.wait_limit, true);
        match resp {
            Ok(r) if r.get("result").is_some() => {
                let result = r["result"].clone();
                let reported = result.get("userAgent").and_then(Value::as_str).unwrap_or("");
                let consistency = match reported.split('/').nth(1).and_then(|v| v.split_whitespace().next()) {
                    Some(v) if v == DECLARED_PIN => "consistent",
                    Some(_) => "contradicts-declared-pin",
                    None => "no-version-found",
                };
                {
                    let mut i = self.inner.0.lock().unwrap();
                    if let Some(vi) = i.version_identity.as_mut() {
                        vi["handshakeReportedIdentity"] = result.clone();
                        vi["handshakeConsistency"] = json!(consistency);
                    }
                }
                if reported.split('/').nth(1).and_then(|v| v.split_whitespace().next())
                    .is_some_and(|version| version != DECLARED_PIN) {
                    self.kill_group();
                    let mut i = self.inner.0.lock().unwrap();
                    Self::deliver_never_ready(&mut i);
                    let counts = Self::close_generation(&mut i);
                    let failure = "handshake reported version contradicts declared pin";
                    self.lt(&mut i, "LT-11", "handshake-failed", "halted-after-repeated-failure",
                        json!({"failure": failure, "failureCount": 1, "closedGeneration": counts}));
                    return Err(failure.into());
                }
                // initialized notice (whether it is required is U-19; it is sent).
                let _ = self.write_frame(&json!({"jsonrpc": "2.0", "method": "initialized"}));
                let mut i = self.inner.0.lock().unwrap();
                let vi = i.version_identity.clone().unwrap();
                self.lt(&mut i, "LT-09", "handshake-completed", "ready",
                        json!({"versionIdentity": vi, "declaredCapabilities": caps}));
                // Step 5: deliver held frames in received order (H4).
                let held: Vec<Value> = std::mem::take(&mut i.held);
                i.journal.extend(held);
                drop(i);
                Ok(self.snapshot())
            }
            other => {
                let failure = match other {
                    Ok(r) => format!("initialize error: {}", r.get("error").cloned().unwrap_or(Value::Null)),
                    Err(e) => e,
                };
                self.kill_group();
                let mut i = self.inner.0.lock().unwrap();
                Self::deliver_never_ready(&mut i);
                let counts = Self::close_generation(&mut i);
                self.lt(&mut i, "LT-11", "handshake-failed", "halted-after-repeated-failure",
                        json!({"failure": failure.clone(), "failureCount": 1, "closedGeneration": counts}));
                Err(failure)
            }
        }
    }

    fn deliver_never_ready(i: &mut Inner) {
        // Receipt order and every native frame survive a failed handshake and later spawn.
        i.journal.extend(std::mem::take(&mut i.held).into_iter().map(|mut frame| {
            frame["generationNeverReady"] = json!(true);
            frame
        }));
    }

    /// H10: every pending client request of the closing generation becomes unknown.
    fn close_generation(i: &mut Inner) -> Value {
        let mut unknown = 0;
        for (_, (idx, _)) in i.pending.drain() {
            if let Some(r) = i.client_requests.get_mut(idx) {
                if r.is_object()&&r["writeResult"] != "not-attempted" { r["outcome"] = json!("unknown-no-response"); }
                unknown += 1;
            }
        }
        let generation = i.generation.clone();
        let ended = i.server_requests.close(&generation);
        Self::persist_requests(i);
        for turn in &mut i.conversation_turns {
            if turn["generation"] == generation { turn["observationEnded"] = json!(true); }
        }
        json!({"unknownNoResponse": unknown, "endedUnanswered": ended})
    }

    /// Origin/answer admission remains the register's; actual IO is outside
    /// lifecycle/state locks, bound to the source captured at preparation.
    pub fn answer_server_request(&self, generation:&Value,id:&Value,answer:&Value,origin:&str,actor:Option<&str>)->Result<Value,String>{
        let(frame,bound)={let mut i=self.inner.0.lock().unwrap();let frame=i.server_requests.prepare(generation,id,answer,origin,actor)?;let bound=self.capture_pipe(&i);(frame,bound)};
        let result=bound.and_then(|bound|self.write_reply(bound,&frame));
        if result.is_err(){let mut i=self.inner.0.lock().unwrap();if i.generation==*generation&&!i.server_requests.is_closed(generation){i.server_requests.written(generation,id,false);Self::persist_requests(&mut i);}}
        self.flush_recovery_observations();result?;Ok(json!({"replyWriteResult":"written","acknowledgment":"not-observed"}))
    }
    pub fn error_server_request(&self,generation:&Value,id:&Value,error:&Value,origin:&str)->Result<Value,String>{
        let(frame,bound)={let mut i=self.inner.0.lock().unwrap();let frame=i.server_requests.prepare_error(generation,id,error,origin)?;let bound=self.capture_pipe(&i);(frame,bound)};
        let result=bound.and_then(|bound|self.write_reply(bound,&frame));
        if result.is_err(){let mut i=self.inner.0.lock().unwrap();if i.generation==*generation&&!i.server_requests.is_closed(generation){i.server_requests.written(generation,id,false);Self::persist_requests(&mut i);}}
        self.flush_recovery_observations();result?;Ok(json!({"replyWriteResult":"written","acknowledgment":"not-observed"}))
    }
    fn capture_pipe(&self,i:&Inner)->Result<BoundPipe,String>{
        use std::os::fd::{AsRawFd,FromRawFd};let pipe=self.stdin.lock().unwrap();let source=pipe.as_ref().ok_or("input closed")?;let identity=Self::pipe_identity(source)?;
        let fd=unsafe{libc::fcntl(source.as_raw_fd(),libc::F_DUPFD_CLOEXEC,0)};if fd<0{return Err(std::io::Error::last_os_error().to_string());}
        Ok(BoundPipe{file:unsafe{std::fs::File::from_raw_fd(fd)},generation:i.generation.clone(),epoch:i.attachment_pipe_epoch,identity})
    }
    fn check_bound(&self,i:&Inner,bound:&BoundPipe)->Result<(),String>{
        if i.generation!=bound.generation||i.server_requests.is_closed(&bound.generation)||i.attachment_pipe_epoch!=bound.epoch||!matches!(i.state.as_str(),"ready"|"handshaking"){return Err("captured source generation/pipe closed or changed before write".into());}
        let pipe=self.stdin.lock().unwrap();if Self::pipe_identity(pipe.as_ref().ok_or("source pipe closed before write")?)?!=bound.identity{return Err("captured source pipe replaced before write".into());}Ok(())
    }
    fn frame_bytes(frame:&Value)->Result<Vec<u8>,String>{let mut bytes=serde_json::to_vec(frame).map_err(|e|e.to_string())?;bytes.push(b'\n');Ok(bytes)}
    fn write_complete(file:&mut std::fs::File,bytes:&[u8])->Result<(),String>{file.write_all(bytes).and_then(|_|file.flush()).map_err(|e|e.to_string())}
    fn write_frame(&self,frame:&Value)->Result<(),String>{
        let mut bound={let i=self.inner.0.lock().unwrap();self.capture_pipe(&i)?};let bytes=Self::frame_bytes(frame)?;let serial=self.frame_write.lock().unwrap();
        {let _gate=self.attachment_gate.lock().unwrap();let i=self.inner.0.lock().unwrap();self.check_bound(&i,&bound)?;}
        let result=Self::write_complete(&mut bound.file,&bytes);drop(serial);result
    }
    fn reply_eligible(i:&Inner,generation:&Value,frame:&Value)->bool{
        let entry=i.server_requests.entries().into_iter().find(|e|e["generation"]==*generation&&e["requestId"]==frame["id"]&&e["state"]=="settling"&&e["replyWriteResult"]=="not-attempted");
        let Some(entry)=entry else{return false;};
        // A source resolution that arrived while queued is not an ack and
        // cannot be overwritten by a late locally prepared reply.
        !i.journal.iter().chain(i.held.iter()).any(|e|e["generation"]==*generation&&e["frame"]["method"]=="serverRequest/resolved"&&e["frame"]["params"]["requestId"]==frame["id"]&&e["frame"]["params"]["threadId"]==entry["nativeParameters"]["threadId"])
    }
    fn write_reply(&self,mut bound:BoundPipe,frame:&Value)->Result<(),String>{
        let bytes=Self::frame_bytes(frame)?;let serial=self.frame_write.lock().unwrap();
        {let _gate=self.attachment_gate.lock().unwrap();let i=self.inner.0.lock().unwrap();self.check_bound(&i,&bound)?;if !Self::reply_eligible(&i,&bound.generation,frame){return Err("reply no longer eligible after source/frame wait; nothing sent".into());}}
        let result=Self::write_complete(&mut bound.file,&bytes);drop(serial);
        let mut i=self.inner.0.lock().unwrap();if i.generation!=bound.generation||i.server_requests.is_closed(&bound.generation){return Err("reply write finished for closed/superseded source; no successor settlement inferred".into());}
        i.server_requests.written(&bound.generation,&frame["id"],result.is_ok());Self::persist_requests(&mut i);drop(i);self.flush_recovery_observations();result
    }

    /// HOSTING §5.1 send: a client request with its record. Refused unless ready (CR-03).
    pub fn request(&self, method: &str, params: Value, initiator: Value) -> Result<Value, String> {
        let wait = Duration::from_secs(20);
        self.request_inner(method, params, initiator, wait, false)
    }

    fn request_inner(&self, method: &str, params: Value, initiator: Value, wait: Duration, handshake: bool) -> Result<Value, String> {
        self.request_inner_scoped(method, params, initiator, wait, handshake, None)
    }

    fn request_inner_scoped(&self, method: &str, params: Value, initiator: Value,
        wait: Duration, handshake: bool, expected_generation: Option<&Value>) -> Result<Value, String> {
        let request = self.request_begin_scoped(method, params, initiator, handshake, expected_generation)?;
        self.wait_source_response(&request, wait)
    }

    fn request_begin_scoped(&self, method: &str, params: Value, initiator: Value,
        handshake: bool, expected_generation: Option<&Value>) -> Result<SourceRequest, String> {
        auth_rpc::generic_guard(method,&params)?;
        self.request_begin_scoped_private(method,params,initiator,handshake,expected_generation,false)
    }
    fn request_begin_scoped_private(&self, method: &str, params: Value, initiator: Value,
        handshake: bool, expected_generation: Option<&Value>, private_credential: bool) -> Result<SourceRequest, String> {
        let (tx, rx) = channel();
        let mut i = self.inner.0.lock().unwrap();
        let ok_state = if handshake {i.state=="handshaking"} else {i.state=="ready"};
        if !ok_state {
            let gen=i.generation.clone();i.client_requests.push(json!({"recordKind":"client-request","generation":gen,"requestIdentity":null,"method":method,"initiator":initiator,"writeResult":"not-attempted","outcome":"refused-not-sent","refusalReason":"not-ready"}));
            return Err(format!("refused-not-sent(not-ready): state {}",i.state));
        }
        if expected_generation.map(|g|g!=&i.generation||i.server_requests.is_closed(g)).unwrap_or(false) {return Err(format!("refused-not-sent: {method} generation changed before request registration"));}
        if expected_generation.is_some()&&matches!(method,"turn/start"|"turn/interrupt"|"turn/steer") {Self::check_conversation_request(&i,method,&params)?;}
        i.next_id+=1;let id=i.next_id;
        let raw_frame=json!({"jsonrpc":"2.0","id":id,"method":method,"params":params});
        let(frame,auth_projection)=auth_rpc::project_frame(&raw_frame,Some(method));
        let bytes=Self::frame_bytes(&raw_frame)?;drop(raw_frame);
        if auth_rpc::account_method(method)&&!i.account_channels.contains(&i.generation){let g=i.generation.clone();i.account_channels.push(g);}
        let request=SourceRequest {source:Arc::downgrade(&self.inner),generation:i.generation.clone(),frame:frame.clone(),request_ref:format!("{}:client:{id}",opaque_id("host-request")?),receiver:Arc::new(Mutex::new(rx))};
        // This private receipt account is separate from the published client
        // record schema; only completion of the actual write sets sentFrame.
        let rec=json!({"recordKind":"client-request","generation":i.generation,"requestIdentity":id,"method":method,"initiator":initiator});
        i.client_requests.push(Value::Null);let idx=i.client_requests.len()-1;i.pending.insert(id.to_string(),(idx,tx));
        i.source_requests.insert(id.to_string(),SourceEvidence {request:request.clone(),index:idx,written:false,write_error:None,response:None,attachment:None,reserved_sender:None,write_attempt_in_progress:false,attempt_position:None,response_position:None,observation_base:rec,source_limit:None,auth_projection,auth_policy_standing:None,auth_response_shape:None});
        if expected_generation.is_some()&&method=="turn/start" {let gen=i.generation.clone();let pos=i.receipt_position;i.turn_request_threads.insert(id.to_string(),(gen,frame["params"]["threadId"].as_str().unwrap().into(),pos));}
        if expected_generation.is_some()&&method=="turn/interrupt" {let gen=i.generation.clone();i.interrupt_requests.push(json!({"generation":gen,"threadId":frame["params"]["threadId"],"turnId":frame["params"]["turnId"],"requestIdentity":id,"initiator":"person-directed"}));}
        let captured=self.capture_pipe(&i);drop(i);
        let write_result=(||->Result<(),String>{let mut bound=captured?;let serial=if private_credential{
            let deadline=std::time::Instant::now()+Duration::from_secs(20);loop{match self.frame_write.try_lock(){Ok(serial)=>break serial,Err(std::sync::TryLockError::Poisoned(_))=>return Err("frame writer unavailable; transient input released".into()),Err(std::sync::TryLockError::WouldBlock)=>{let i=self.inner.0.lock().unwrap();if i.generation!=request.generation||i.server_requests.is_closed(&request.generation)||i.state!="ready"||std::time::Instant::now()>=deadline{return Err("credential source lost/cancelled/queue limit; transient input released, no retry".into());}drop(i);std::thread::sleep(Duration::from_millis(2));}}}
        }else{self.frame_write.lock().unwrap()};
            {let _gate=self.attachment_gate.lock().unwrap();let mut i=self.inner.0.lock().unwrap();self.check_bound(&i,&bound)?;
                if !i.pending.contains_key(&id.to_string()){return Err("request no longer pending before actual source write".into());}
                if expected_generation.is_some()&&matches!(method,"turn/start"|"turn/interrupt"|"turn/steer"){Self::check_conversation_request_excluding(&i,method,&frame["params"],Some(&json!(id)))?;}
                i.send_position+=1;let position=i.send_position;let e=i.source_requests.get_mut(&id.to_string()).unwrap();e.write_attempt_in_progress=true;e.attempt_position=Some(position);}
            let result=Self::write_complete(&mut bound.file,&bytes);drop(serial);result})();
        drop(bytes);
        let mut i=self.inner.0.lock().unwrap();let key=id.to_string();let closed=i.generation!=request.generation||i.server_requests.is_closed(&request.generation)||!matches!(i.state.as_str(),"ready"|"handshaking");
        let e=i.source_requests.get_mut(&key).unwrap();e.write_attempt_in_progress=false;let mut record=e.observation_base.clone();let response=e.response.clone();let response_position=e.response_position;if let Some(position)=e.attempt_position{record["sendPosition"]=json!(position);}
        match write_result {
            Ok(())=> {i.source_requests.get_mut(&key).unwrap().written=true;record["writeResult"]=json!("written");record["outcome"]=json!(if closed{"unknown-no-response"}else{"pending"});
                match Self::completed_client_response(&mut record,response.as_ref(),response_position){Ok(())=>i.client_requests[idx]=record,Err(error)=>i.source_requests.get_mut(&key).unwrap().source_limit=Some(error)}
                if !closed&&method=="turn/start"&&response.is_some(){if let Some((source_gen,thread,sent_after_receipt))=i.turn_request_threads.remove(&key){if source_gen==i.generation{if let Some(turn)=response.as_ref().and_then(|r|r.get("result")).and_then(|r|r.get("turn")){let position=response_position.unwrap_or(i.receipt_position);Self::remember_turn(&mut i,&source_gen,&thread,turn,"turn/start response",position);if let Some(e)=i.conversation_turns.iter_mut().find(|e|e["generation"]==source_gen&&e["threadId"]==thread&&e["turnId"]==turn["id"]&&e["source"]=="turn/start response"&&e["receiptPosition"]==position){e["startResponseIssuedAfterReceipt"]=json!(sent_after_receipt);}}}}}
            }
            Err(error)=> {i.pending.remove(&key);i.turn_request_threads.remove(&key);let e=i.source_requests.get_mut(&key).unwrap();
                if e.attempt_position.is_none(){e.source_limit=Some(format!("No actual write attempt: reserved source invalidated/refused before pipe commit: {error}; native reply facts retained if present"));}
                else{e.write_error=Some(error);if response.is_some(){e.source_limit=Some("Matching native reply and write failure both observed; v0.10 cannot faithfully project that combination; raw source retained".into());}
                    else{record["writeResult"]=json!("write-failed");record["outcome"]=json!("unknown-no-response");i.client_requests[idx]=record;}}
            }
        }
        Ok(request)
    }

    fn completed_client_response(record:&mut Value,response:Option<&Value>,position:Option<u64>)->Result<(),String>{
        let Some(frame)=response else{return Ok(());};let position=position.ok_or("Native reply position unavailable; canonical settlement projection unavailable")?;
        if frame.get("id")!=record.get("requestIdentity")||frame.get("method").is_some()||!frame.is_object()||frame.get("error").is_some()&&frame.get("result").is_some(){return Err("Native reply envelope malformed/contradictory; canonical settlement projection unavailable".into());}
        if let Some(error)=frame.get("error"){if error["code"].as_i64().is_none()||!error["message"].is_string(){return Err("Actual native error code/message unavailable; no invented canonical error".into());}record["outcome"]=json!("response-observed-error");record["error"]=json!({"code":error["code"],"message":error["message"]});}
        else if frame.get("result").is_some(){record["outcome"]=json!("response-observed-result");}
        else{return Err("Native reply result missing; canonical settlement projection unavailable".into());}
        record["responseReceiptPosition"]=json!(position);Ok(())
    }
    /// Unit A private source only. No UI/real-key constructor or H-key routing
    /// qualification is supplied by this synthetic prerequisite primitive.
    pub(crate) fn account_login_api_key(&self,generation:&Value,input:auth_rpc::TransientApiKey,policy:Option<&SourceRequest>)->Result<SourceRequest,String>{
        crate::recovery::generation_ref(generation)?;
        let policy_frame=if let Some(source)=policy{self.check_source(source)?;if source.generation()!=generation||source.attempted_frame()["method"]!="configRequirements/read"{return Err("native login policy source/full generation differs".into());}source.evidence().get("response").filter(|v|!v.is_null()).cloned()}else{None};
        if policy_frame.is_some()&&policy.is_some_and(|s|s.evidence()["authResponseShapeValid"]!=true){return Err("native policy shape malformed/unavailable; no key frame written".into());}
        let policy_standing=auth_rpc::login_policy(policy_frame.as_ref())?;
        let params=input.into_params();Self::validate_native_result("LoginAccountParams",&params).map_err(|_|"native API-key input shape invalid; sensitive diagnostic withheld".to_string())?;
        let source=self.request_begin_scoped_private("account/login/start",params,json!({"kind":"person-directed"}),false,Some(generation),true)?;
        let mut i=self.inner.0.lock().unwrap();if let Some(e)=i.source_requests.get_mut(&source.request_id().to_string()){e.auth_policy_standing=Some(format!("{policy_standing}; Unit A transport only, native secure-entry/H-key owner not qualified; validity unknown until actual use"));}Ok(source)
    }
    pub(crate) fn account_rpc_observation(&self,source:&SourceRequest)->Result<Value,String>{self.check_source(source)?;let e=source.evidence();let frame=e.get("response").filter(|f|!f.is_null());Ok(json!({"source":e,"accountObservation":frame.map(|frame|auth_rpc::typed_observation(source.attempted_frame()["method"].as_str().unwrap_or(""),frame,e["authResponseShapeValid"]==true,source.attempted_frame()["params"]["type"].as_str())),"standing":"redacted source facts only; no credential validity/home/actor qualification"}))}
    fn check_source(&self, request: &SourceRequest) -> Result<(), String> {
        let source=request.source.upgrade().ok_or("receipt source Host unavailable")?;
        if !Arc::ptr_eq(&self.inner,&source) {return Err("receipt belongs to another Host".into());}
        let i=self.inner.0.lock().unwrap();let e=i.source_requests.get(&request.request_id().to_string()).ok_or("source receipt unavailable")?;
        if e.request.generation!=request.generation||e.request.frame!=request.frame||e.request.request_ref!=request.request_ref {return Err("source receipt binding differs".into());}Ok(())
    }
    fn wait_source_response(&self, request: &SourceRequest, wait: Duration) -> Result<Value,String> {
        self.check_source(request)?;let evidence=request.evidence();
        if evidence["actualWriteAttemptObserved"]==false&&!evidence["noAttemptCause"].is_null(){return Err(format!("refused-not-sent before actual attempt: {}",evidence["noAttemptCause"]));}
        if evidence["writeResult"]=="write-failed" {return Err(format!("write failed: {}",evidence["writeError"]));}
        if !evidence["response"].is_null() {return Ok(evidence["response"].clone());}
        match request.receiver.lock().unwrap().recv_timeout(wait) {
            Ok(response)=>Ok(response),
            Err(_)=> {let mut i=self.inner.0.lock().unwrap();if let Some((idx,_))=i.pending.get(&request.request_id().to_string()).cloned() {if i.client_requests[idx].is_object(){i.client_requests[idx]["waitingEnded"]=json!(true);}else if let Some(e)=i.source_requests.get_mut(&request.request_id().to_string()){e.observation_base["waitingEnded"]=json!(true);}}Err(format!("no response to {} within the wait limit (outcome stays pending/unknown)",request.frame["method"]))}
        }
    }
    pub fn source_request_wait(&self, request: &SourceRequest, wait: Duration) -> Result<Value,String> {
        self.check_source(request)?;let _=self.wait_source_response(request,wait);Ok(request.evidence())
    }
    pub fn source_request_status(&self, request: &SourceRequest) -> Result<Value,String> {self.check_source(request)?;Ok(request.evidence())}
    /// Genuine retained start evidence for a synchronous wrapper response.
    pub fn source_request(&self, generation: &Value, rpc_id: &Value) -> Result<SourceRequest,String> {
        let i=self.inner.0.lock().unwrap();let e=i.source_requests.get(&rpc_id.to_string()).ok_or("actual supplier RPC request not retained")?;
        if e.request.generation!=*generation {return Err("source request full generation differs".into());}Ok(e.request.clone())
    }

    pub fn history_dispatch(&self, query: &HistoryQuery) -> Result<HistoryDispatch,String> {
        crate::recovery::generation_ref(query.generation())?;
        if query.generation()["home"]!=query.home() {return Err("history home and full generation differ".into());}
        if !matches!(query.method(),"thread/list"|"thread/read"|"thread/turns/list"|"thread/items/list"|"thread/goal/get"|"thread/resume") {return Err("unsupported history factory method".into());}
        let source=self.request_begin_scoped(query.method(),query.params().clone(),json!({"kind":"person-directed"}),false,Some(query.generation()))?;
        Ok(HistoryDispatch {query:query.clone(),source})
    }
    pub fn history_wait(&self, dispatch: &HistoryDispatch, wait: Duration) -> Result<Value,String> {self.source_request_wait(&dispatch.source,wait)}
    pub fn history_dispatch_status(&self, dispatch: &HistoryDispatch) -> Result<Value,String> {self.source_request_status(&dispatch.source)}

    pub fn history_admit_resume(&self, history: &NativeHistory, dispatch: &HistoryDispatch) -> Result<Value,String> {
        self.check_source(&dispatch.source)?;
        if dispatch.query.method()!="thread/resume"||dispatch.query.params()!=&json!({"threadId":history.selected_thread()}) {return Err("only original explicit Continue packet can admit".into());}
        let candidate=history.resumed_thread().ok_or("latest history state is not an eligible Continue response")?;
        let snapshot=history.snapshot();let query=serde_json::to_value(&dispatch.query).map_err(|e|e.to_string())?;
        if snapshot["selected"]["streamResolutions"]["thread-state"]["query"]!=query||snapshot["selected"]["streamResolutions"]["thread-state"]["outcome"]!="native-result-observed" {return Err("Continue receipt is not latest resolved thread-state query".into());}
        let mut i=self.inner.0.lock().unwrap();let evidence=i.source_requests.get(&dispatch.source.request_id().to_string()).ok_or("Continue source record unavailable")?;
        if !evidence.written||i.client_requests[evidence.index]["outcome"]!="response-observed-result" {return Err("Continue has no successful write and correlated native result".into());}
        let response=evidence.response.as_ref().ok_or("Continue native response unavailable")?;
        if response["id"]!=*dispatch.source.request_id()||response.get("error").is_some()||response["result"]!=snapshot["selected"]["resume"]||response["result"]["thread"]!=candidate["native"] {return Err("Continue receipt and validated native receiving state differ".into());}
        let generation=dispatch.query.generation();
        if history.generation()!=generation||history.home()!=dispatch.query.home()||i.generation!=*generation||i.state!="ready"||i.server_requests.is_closed(generation) {return Err("Continue admission belongs to foreign/stale/closed generation".into());}
        let native=&candidate["native"];if !matches!(native["status"]["type"].as_str(),Some("idle"|"active"))||native["canAcceptDirectInput"]==false||native["id"]!=dispatch.query.params()["threadId"] {return Err("native thread cannot accept direct input".into());}
        if i.threads.iter().any(|t|t["generation"]==*generation&&t["threadId"]==native["id"]) {return Err("thread already operationally admitted in generation".into());}
        let result=&response["result"];let row=json!({"generation":generation,"threadId":native["id"],"status":native["status"],"model":result.get("model"),"modelProvider":result.get("modelProvider"),"cwd":result.get("cwd"),"supplierStanding":i.supplier_standing,"resumeRequestRef":dispatch.source.request_ref,"nativeResumeObserved":true,"appRole":{"standing":"unknown"},"networkDisclosure":network_disclosure()});i.threads.push(row.clone());Ok(row)
    }

    pub fn thread_start_with_guidance_dispatch(&self, generation: &Value, cwd: &str, model: &str, model_provider: &str, guidance: &str) -> Result<SourceRequest,String> {
        crate::recovery::generation_ref(generation)?;let params=Self::thread_start_params(cwd,model,model_provider,Some(guidance))?;
        self.request_begin_scoped("thread/start",params,json!({"kind":"person-directed"}),false,Some(generation))
    }
    pub fn thread_start_dispatch_finish(&self, request: &SourceRequest) -> Result<Value,String> {
        self.check_source(request)?;let evidence=request.evidence();
        if request.frame["method"]!="thread/start"||evidence["writeResult"]!="written"||evidence["outcome"]!="response-observed-result"||evidence["sentFrame"].is_null() {return Err("start receipt lacks actual successful start write/result".into());}
        let response=evidence["response"].clone();
        if !response.is_object() || response.get("id") != Some(request.request_id()) || response.get("method").is_some() || response.get("error").is_some() || response.get("result").is_none() {
            return Err("start response envelope is uncorrelated or failed; raw native evidence retained, no operational admission".into());
        }
        Self::validate_native_result("ThreadStartResponse",&response["result"])?;
        self.insert_start_response(request.generation(),&request.frame["params"],&response,true)?;Ok(response)
    }
    fn validate_native_result(target: &str, result: &Value) -> Result<(),String> {
        let mut schema:Value=serde_json::from_str(include_str!("../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json")).map_err(|e|e.to_string())?;schema["$ref"]=json!(format!("#/definitions/v2/{target}"));
        jsonschema::options().offline().build(&schema).map_err(|e|e.to_string())?.validate(result).map_err(|e|format!("native {target} schema: {e}"))
    }


    fn pipe_identity(pipe:&ChildStdin)->Result<(u64,u64),String>{
        use std::os::fd::AsRawFd;let mut stat=std::mem::MaybeUninit::<libc::stat>::uninit();
        if unsafe{libc::fstat(pipe.as_raw_fd(),stat.as_mut_ptr())}!=0{return Err(std::io::Error::last_os_error().to_string());}
        let stat=unsafe{stat.assume_init()};Ok((stat.st_dev as u64,stat.st_ino as u64))
    }
    /// Caller supplies the explicit native App-data owner and private picker selections.
    pub fn prepare_attachment_turn(&self,custody:Arc<AttachmentCustody>,generation:&Value,thread:&str,expected_turn:Option<&str>,text:&str,selections:&[SelectedTextAttachment])->Result<PreparedAttachmentDispatch,String>{
        crate::recovery::generation_ref(generation)?;if thread.is_empty()||expected_turn.is_some_and(str::is_empty){return Err("native thread/expected-turn identity required".into());}
        let submission=attachments::new_submission_ref()?;let list=attachments::prepare_ordered(selections,&submission,&now_rfc3339()).map_err(|e|e.message)?;
        let mut input=vec![];if !text.is_empty(){input.push(json!({"type":"text","text":text,"text_elements":[]}));}input.extend(list.native_inputs());
        let method=if expected_turn.is_some(){"turn/steer"}else{"turn/start"};let mut params=json!({"threadId":thread,"input":input});if let Some(turn)=expected_turn{params["expectedTurnId"]=json!(turn);}
        Self::validate_native_result(if expected_turn.is_some(){"TurnSteerParams"}else{"TurnStartParams"},&params)?;
        let(tx,rx)=channel();let(source,client,pipe_identity,pipe_epoch)={
            let mut i=self.inner.0.lock().unwrap();if i.generation!=*generation||i.state!="ready"||i.server_requests.is_closed(generation){return Err("attachment preparation scope is stale/closed/non-ready".into());}
            Self::check_conversation_request(&i,method,&params)?;let pipe=self.stdin.lock().unwrap();let identity=Self::pipe_identity(pipe.as_ref().ok_or("actual source pipe unavailable; nothing reserved")?)?;drop(pipe);
            i.next_id+=1;let id=i.next_id;let frame=json!({"jsonrpc":"2.0","id":id,"method":method,"params":params});
            let source=SourceRequest{source:Arc::downgrade(&self.inner),generation:generation.clone(),frame,request_ref:opaque_id("host-attachment-request:")?,receiver:Arc::new(Mutex::new(rx))};
            let mut association=json!({"submissionRef":submission,"threadId":thread,"supplyRefs":list.supply_refs()});if let Some(turn)=expected_turn{association["expectedTurnId"]=json!(turn);}
            let client=json!({"recordKind":"client-request","generation":generation,"requestIdentity":id,"method":method,"initiator":{"kind":"person-directed"},"writeResult":"not-attempted","outcome":"prepared-not-sent","submissionAssociation":association});
            i.client_requests.push(client.clone());let index=i.client_requests.len()-1;
            i.source_requests.insert(id.to_string(),SourceEvidence{request:source.clone(),index,written:false,write_error:None,response:None,reserved_sender:Some(tx),write_attempt_in_progress:false,attempt_position:None,response_position:None,observation_base:client.clone(),source_limit:None,auth_projection:false,auth_policy_standing:None,auth_response_shape:None,attachment:Some(AttachmentLink{custody:Arc::clone(&custody),records:list.supply_records(),original:client.clone(),limit:None})});(source,client,identity,i.attachment_pipe_epoch)
        };
        // Never hold Inner across file operations. Failure consumes its reserved
        // RPC; partial/uncertain publication cannot authorize native write.
        if let Err(error)=custody.publish_prepared(&list.supply_records(),&client){self.attachment_limit(&source,error.clone());return Err(format!("attachment metadata unavailable; nothing sent: {error}"));}
        Ok(PreparedAttachmentDispatch{source,custody,list,selections:selections.to_vec(),client,pipe_identity,pipe_epoch,state:Mutex::new("prepared")})
    }
    fn attachment_limit(&self,source:&SourceRequest,error:String){let mut i=self.inner.0.lock().unwrap();if let Some(e)=i.source_requests.get_mut(&source.request_id().to_string()){if let Some(a)=e.attachment.as_mut(){a.limit=Some(error);}}}
    pub fn dispatch_attachment_turn(&self,prepared:&PreparedAttachmentDispatch)->Result<SourceRequest,String>{
        self.check_source(&prepared.source)?;
        {let mut state=prepared.state.lock().unwrap();if *state!="prepared"{return Err(format!("attachment dispatch is {state}; no resend"));}*state="validating";}
        let result=(||->Result<SourceRequest,String>{
            prepared.custody.check_prepared(&prepared.list.supply_records(),&prepared.client)?;
            // Revalidation uses actual original picker source; generated new
            // preparation IDs are discarded, never substituted into the list.
            let recheck=attachments::prepare_ordered(&prepared.selections,prepared.submission_ref(),&now_rfc3339()).map_err(|e|e.message)?;
            if recheck.native_inputs()!=prepared.list.native_inputs(){return Err("attachment source/input changed after durable preparation; nothing sent".into());}
            let frame=prepared.source.attempted_frame();let bytes=Self::frame_bytes(frame)?;
            let serial=self.frame_write.lock().unwrap();
            let source_lock=prepared.custody.lock_sources()?;
            prepared.custody.check_prepared(&prepared.list.supply_records(),&prepared.client)?;
            let gate=self.attachment_gate.lock().unwrap();let mut state=prepared.state.lock().unwrap();if *state!="validating"{return Err("attachment cancelled before commit; nothing sent".into());}
            let mut i=self.inner.0.lock().unwrap();let generation=prepared.source.generation();if i.generation!=*generation||i.state!="ready"||i.server_requests.is_closed(generation)||i.attachment_pipe_epoch!=prepared.pipe_epoch{return Err("attachment generation/pipe drift before commit; nothing sent".into());}
            Self::check_conversation_request(&i,frame["method"].as_str().unwrap(),&frame["params"])?;
            let mut bound=self.capture_pipe(&i)?;if bound.identity!=prepared.pipe_identity{return Err("actual source pipe changed; nothing sent".into());}
            let key=prepared.source.request_id().to_string();let index=i.source_requests[&key].index;let sender=i.source_requests.get_mut(&key).unwrap().reserved_sender.take().ok_or("reserved RPC already consumed")?;
            i.send_position+=1;let position=i.send_position;let e=i.source_requests.get_mut(&key).unwrap();e.write_attempt_in_progress=true;e.attempt_position=Some(position);i.pending.insert(key.clone(),(index,sender));
            if frame["method"]=="turn/start"{let pos=i.receipt_position;i.turn_request_threads.insert(key.clone(),(generation.clone(),frame["params"]["threadId"].as_str().unwrap().into(),pos));}
            *state="attempted";drop(state);drop(i);drop(gate);drop(source_lock);
            let written=Self::write_complete(&mut bound.file,&bytes);drop(bound);drop(serial);
            let mut i=self.inner.0.lock().unwrap();let closed=i.generation!=*generation||i.server_requests.is_closed(generation)||i.state!="ready";
            let e=i.source_requests.get_mut(&key).unwrap();e.write_attempt_in_progress=false;let response=e.response.clone();let response_position=e.response_position;
            i.client_requests[index]["sendPosition"]=json!(position);
            match written {Ok(())=>{i.source_requests.get_mut(&key).unwrap().written=true;i.client_requests[index]["writeResult"]=json!("written");i.client_requests[index]["outcome"]=json!(if closed{"unknown-no-response"}else{"pending"});
                if response.is_some(){let(record,limit)=attachment_custody::project_observation(&i.client_requests[index],response.as_ref(),response_position)?;i.client_requests[index]=record;if let Some(limit)=limit{if let Some(a)=i.source_requests.get_mut(&key).unwrap().attachment.as_mut(){a.limit=Some(limit);}}}}
                Err(error)=>{i.pending.remove(&key);let e=i.source_requests.get_mut(&key).unwrap();e.write_error=Some(error);if response.is_some(){e.source_limit=Some("Matching native reply and write failure both observed; canonical projection unavailable".into());if let Some(a)=e.attachment.as_mut(){a.limit=Some("Combined failed write and observed reply cannot be projected into v0.10; last prewrite source is historical only".into());}i.client_requests[index]=prepared.client.clone();}else{i.client_requests[index]["writeResult"]=json!("write-failed");i.client_requests[index]["outcome"]=json!("unknown-no-response");}}}
            drop(i);let _=self.persist_attachment_observation(&prepared.source);Ok(prepared.source.clone())
        })();if let Err(error)=&result{*prepared.state.lock().unwrap()="refused";self.attachment_limit(&prepared.source,error.clone());}result
    }
    pub fn persist_attachment_observation(&self,source:&SourceRequest)->Result<Value,String>{
        self.check_source(source)?;let(custody,record,limit)={let i=self.inner.0.lock().unwrap();let e=i.source_requests.get(&source.request_id().to_string()).ok_or("source unavailable")?;let a=e.attachment.as_ref().ok_or("source is not attachment-bearing")?;
            if e.write_error.is_some()&&e.response.is_some(){return Err("Combined write failure and matching reply has no faithful canonical v0.10 projection; last observation/raw facts retained".into());}
            if e.write_attempt_in_progress||!e.written&&e.write_error.is_none(){return Err("write not completed; last prepared metadata is not current no-send proof".into());}
            let raw=&i.client_requests[e.index];let mut client=a.original.clone();for field in ["writeResult","outcome","sendPosition","responseReceiptPosition","waitingEnded"]{if let Some(v)=raw.get(field){client[field]=v.clone();}}
            let(projected,limit)=attachment_custody::project_observation(&client,e.response.as_ref(),raw["responseReceiptPosition"].as_u64())?;(Arc::clone(&a.custody),projected,limit)};
        if let Some(limit)=limit{self.attachment_limit(source,limit);}
        match custody.replace_observation(&record){Ok(())=>Ok(record),Err(error)=>{self.attachment_limit(source,format!("durable outcome unavailable: {error}"));Err(error)}}
    }
    pub fn attachment_wait(&self,source:&SourceRequest,wait:Duration)->Result<Value,String>{
        let mut evidence=self.source_request_wait(source,wait)?;let _=self.persist_attachment_observation(source);
        let i=self.inner.0.lock().unwrap();let a=i.source_requests.get(&source.request_id().to_string()).and_then(|e|e.attachment.as_ref()).ok_or("source is not attachment-bearing")?;evidence["custodyLimit"]=json!(a.limit);Ok(evidence)
    }
    pub fn resolve_attachment_submission(&self,custody:&Arc<AttachmentCustody>,submission:&str)->Value{
        let mut view=custody.resolve_cold(submission);if view.get("clientMetadata").is_none(){return view;}
        let record=view["clientMetadata"].clone();let i=self.inner.0.lock().unwrap();let Some(e)=i.source_requests.get(&record["requestIdentity"].to_string())else{return view;};let Some(a)=e.attachment.as_ref()else{return view;};
        if !Arc::ptr_eq(custody,&a.custody)||e.request.generation!=record["generation"]||a.original["submissionAssociation"]!=record["submissionAssociation"]||view["supplyRecords"].as_array()!=Some(&a.records) {return view;}
        view["sourceStanding"]=json!("genuine hot Host source; immutable owning metadata resolved");
        view["writeAttemptInProgress"]=json!(e.write_attempt_in_progress);view["nativeReplyObserved"]=json!(e.response.is_some());view["lastClientMetadataStanding"]=json!("Historical canonical observation; current hot write facts below are separate");
        if e.write_attempt_in_progress{view["dispatch"]=json!("unknown/in-progress: source write attempt is active; last prewrite row is not current no-send or written proof");return view;}
        if e.write_error.is_some(){view["dispatch"]=json!(if e.response.is_some(){"native reply and failed write both observed; canonical projection unavailable"}else{"actual write failed; native effect unknown"});if let Some(limit)=&e.source_limit{view["limits"].as_array_mut().unwrap().push(json!(limit));}return view;}
view["sourceObservation"]=e.request.frame["method"].clone();view["sourceWriteConfirmed"]=json!(e.written);view["automaticRetry"]=json!(false);
        if let Some(limit)=&a.limit{view["limits"].as_array_mut().unwrap().push(json!(limit));}
        if !e.written||i.client_requests[e.index]["writeResult"]!="written"{view["dispatch"]=json!(if i.client_requests[e.index]["writeResult"]=="not-attempted"{"hot prepared; no actual attempt observed"}else{"unknown write outcome"});return view;}
        view["dispatch"]=json!("actual source write observed; provider adoption not observed");
        let correlation=(||->Result<Value,String>{let frame=e.response.as_ref().ok_or("matching native response unavailable")?;
            if frame.get("id")!=Some(e.request.request_id())||frame.get("method").is_some()||frame.get("error").is_some(){return Err("native envelope uncorrelated or failed".into());}
            let result=frame.get("result").filter(|r|r.is_object()).ok_or("native result missing/null/malformed")?;let association=&record["submissionAssociation"];
            if result.get("threadId").is_some_and(|t|t!=&association["threadId"]){return Err("native reported thread conflicts with original association".into());}
            let id=if record["method"]=="turn/start"{Self::validate_native_result("TurnStartResponse",result)?;result["turn"]["id"].as_str().filter(|s|!s.is_empty()).ok_or("native turn identity absent")?}else{Self::validate_native_result("TurnSteerResponse",result)?;if result["turnId"]!=association["expectedTurnId"]{return Err("native steer result differs from actual expected target".into());}result["turnId"].as_str().filter(|s|!s.is_empty()).ok_or("native steer identity absent")?};
            Ok(json!({"generation":e.request.generation,"threadId":association["threadId"],"turnId":id,"requestIdentity":e.request.request_id(),"source":"matching native result; immutable submission remains distinct"}))})();
        match correlation{Ok(reference)=>view["nativeTurnRef"]=reference,Err(limit)=>view["limits"].as_array_mut().unwrap().push(json!(limit))};view
    }

    /// `thread/start`, person-directed (§5 initiator). Records the thread for the interface.
    pub fn thread_start(&self, _cwd: &str) -> Result<Value, String> {
        Err("not started — no model selected (explicit model and model provider required)".into())
    }

    pub fn thread_start_selected(&self, cwd: &str, model: &str, model_provider: &str) -> Result<Value, String> {
        self.thread_start_inner(cwd, model, model_provider, None)
    }

    /// The caller verifies composed role bytes/provenance. Carry those bytes
    /// only through Codex's additive native developerInstructions input.
    pub fn thread_start_with_guidance(&self, cwd: &str, model: &str, model_provider: &str,
        developer_instructions: &str) -> Result<Value, String> {
        self.thread_start_inner(cwd, model, model_provider, Some(developer_instructions))
    }

    fn thread_start_params(cwd: &str, model: &str, model_provider: &str,
        developer_instructions: Option<&str>) -> Result<Value, String> {
        if model.trim().is_empty() || model_provider.trim().is_empty() {
            return Err("not started — no model selected (explicit model and model provider required)".into());
        }
        let mut params = json!({"cwd":cwd,"model":model,"modelProvider":model_provider});
        if let Some(text) = developer_instructions { params["developerInstructions"] = json!(text); }
        Ok(params)
    }

    fn thread_start_inner(&self, cwd: &str, model: &str, model_provider: &str,
        developer_instructions: Option<&str>) -> Result<Value, String> {
        let params = Self::thread_start_params(cwd, model, model_provider, developer_instructions)?;
        let sent_generation = self.inner.0.lock().unwrap().generation.clone();
        let r = self.request_inner_scoped("thread/start", params, json!({"kind": "person-directed"}),
            Duration::from_secs(20), false, Some(&sent_generation))?;
        #[cfg(test)]
        if let Some(hook) = self.before_thread_insert.lock().unwrap().take() { hook(); }
        self.insert_start_response(&sent_generation,&Self::thread_start_params(cwd,model,model_provider,developer_instructions)?,&r,false)?;
        Ok(r)
    }
    fn insert_start_response(&self, generation: &Value, params: &Value, response: &Value, no_duplicate: bool) -> Result<(),String> {
        let t=response.get("result").and_then(|x|x.get("thread")).ok_or_else(||format!("thread/start answered with an error: {}",response.get("error").cloned().unwrap_or(Value::Null)))?;
        let mut i=self.inner.0.lock().unwrap();
        if i.generation!=*generation||i.server_requests.is_closed(generation) {return Err("thread/start response belongs to a closed or replaced generation; native response retained in journal".into());}
        if no_duplicate&&i.state!="ready" {return Err("thread/start result is not ready for operational admission".into());}
        if no_duplicate&&i.threads.iter().any(|e|e["generation"]==*generation&&e["threadId"]==t["id"]) {return Err("thread already operationally admitted in generation".into());}
        let standing=i.supplier_standing.clone();i.threads.push(json!({"generation":generation,"threadId":t.get("id"),"status":t.get("status"),"model":response["result"].get("model"),"modelProvider":response["result"].get("modelProvider"),"cwd":response["result"].get("cwd"),"supplierStanding":standing,"requestedDestination":{"source":"person-selected","model":params["model"],"modelProvider":params["modelProvider"]},"reportedDestination":{"scope":"thread","model":response["result"].get("model"),"modelProvider":response["result"].get("modelProvider")},"networkDisclosure":network_disclosure()}));Ok(())
    }

    /// Plain text only, with complete native text input; all thread settings
    /// and fixed-lifetime guidance are inherited. No actor/policy override input.
    pub fn turn_start_text(&self, generation: &Value, thread_id: &str, text: &str) -> Result<Value, String> {
        self.conversation_operation("turn/start", generation,
            Self::text_turn_params(thread_id, text)?, Duration::from_secs(20))
    }

    /// Native interrupt acknowledgment is distinct from turn completion.
    pub fn turn_interrupt(&self, generation: &Value, thread_id: &str, turn_id: &str) -> Result<Value, String> {
        if thread_id.is_empty() || turn_id.is_empty() { return Err("thread and turn identity required".into()); }
        self.conversation_operation("turn/interrupt", generation,
            json!({"threadId":thread_id,"turnId":turn_id}), Duration::from_secs(20))
    }

    /// Native expected-turn precondition, never a fallback start or settings edit.
    pub fn turn_steer_text(&self, generation: &Value, thread_id: &str, expected_live_turn: &str, text: &str) -> Result<Value, String> {
        let params = Self::steer_text_params(thread_id, expected_live_turn, text)?;
        self.conversation_operation("turn/steer", generation, params, Duration::from_secs(20))
    }
    fn steer_text_params(thread_id: &str, expected_turn: &str, text: &str) -> Result<Value, String> {
        if expected_turn.is_empty() { return Err("expected live turn identity required".into()); }
        let mut params = Self::text_turn_params(thread_id, text)?;
        params["expectedTurnId"] = json!(expected_turn);
        Ok(params)
    }

    fn text_turn_params(thread_id: &str, text: &str) -> Result<Value, String> {
        if thread_id.is_empty() || text.is_empty() { return Err("thread identity and text required".into()); }
        Ok(json!({"threadId":thread_id,"input":[{"type":"text","text":text,"text_elements":[]}]}))
    }

    fn conversation_operation(&self, method: &str, generation: &Value, params: Value, wait: Duration) -> Result<Value, String> {
        crate::recovery::generation_ref(generation)?;
        let steering_target = if method == "turn/steer" { Some(params.clone()) } else { None };
        let response = self.request_inner_scoped(method, params, json!({"kind":"person-directed"}), wait, false, Some(generation))?;
        #[cfg(test)]
        if let Some(hook) = self.before_turn_result.lock().unwrap().take() { hook(); }
        let i = self.inner.0.lock().unwrap();
        if i.generation != *generation || i.server_requests.is_closed(generation) || i.state != "ready" {
            return Err(format!("{method} response belongs to closed/replaced generation; native response retained in journal"));
        }
        if let Some(error) = response.get("error") { return Err(format!("{method} native error: {error}")); }
        if let Some(target) = steering_target {
            if response.get("result").and_then(|r| r.get("turnId")) != target.get("expectedTurnId") {
                return Err("turn/steer reported turn differs from expected target; native response retained, no rebind".into());
            }
            Self::check_conversation_request(&i, method, &target).map_err(|error| format!("turn/steer target changed before result consumption: {error}; native response retained"))?;
        } else if method == "turn/start" {
            let turn = response.get("result").and_then(|r| r.get("turn")).ok_or("turn/start has no native turn result")?;
            if !Self::native_turn_shape(turn) { return Err("turn/start native turn result has invalid shape".into()); }
        } else if !response.get("result").map(Value::is_object).unwrap_or(false) {
            return Err("turn/interrupt has no native acknowledgment object".into());
        }
        Ok(response)
    }

    fn native_turn_shape(turn: &Value) -> bool {
        turn["id"].as_str().map(|s| !s.is_empty()).unwrap_or(false)
            && turn["items"].is_array()
            && matches!(turn["status"].as_str(), Some("inProgress" | "completed" | "interrupted" | "failed"))
    }

    fn remember_turn(i: &mut Inner, generation: &Value, thread: &str, native: &Value, source: &str, position: u64) {
        if !Self::native_turn_shape(native) { return; }
        if let Some(entry) = i.conversation_turns.iter_mut().find(|t| t["generation"] == *generation && t["threadId"] == thread && t["turnId"] == native["id"]) {
            // Preserve terminal lifecycle for this exact tuple. Contradictory
            // native evidence stays in the journal; this is a guarded reading,
            // never a rewrite of the received frame.
            if entry["terminalEventObserved"] == true && (native["status"] == "inProgress" || source == "turn/start response") {
                let limit = json!({"reason":"terminal turn cannot be revived by a later active-like observation or start response","source":source,"receiptPosition":position,"reportedStatus":native["status"],"nativeEvidence":"unchanged frame retained in generation journal"});
                if entry.get("inconsistencyLimits").is_none() { entry["inconsistencyLimits"] = json!([]); }
                entry["inconsistencyLimits"].as_array_mut().unwrap().push(limit);
                return;
            }
            entry["nativeTurn"] = native.clone(); entry["source"] = json!(source); entry["receiptPosition"] = json!(position);
            if source == "turn/completed" { entry["terminalEventObserved"] = json!(true); }
        } else {
            i.conversation_turns.push(json!({"generation":generation,"threadId":thread,"turnId":native["id"],"nativeTurn":native,"source":source,"receiptPosition":position,"terminalEventObserved":source=="turn/completed","observationEnded":false}));
        }
    }

    fn check_conversation_request(i: &Inner, method: &str, params: &Value) -> Result<(), String> { Self::check_conversation_request_excluding(i,method,params,None) }
    fn check_conversation_request_excluding(i: &Inner, method: &str, params: &Value, own_rpc: Option<&Value>) -> Result<(), String> {
        let thread = params["threadId"].as_str().filter(|s| !s.is_empty()).ok_or("thread identity required")?;
        if !i.threads.iter().any(|t| t["generation"] == i.generation && t["threadId"] == thread) { return Err("conversation-not-loaded-in-current-home-generation".into()); }
        if method == "turn/steer" {
            let current = Self::current_live_turn(i, thread).ok_or("current-live-turn-not-established")?;
            if current["turnId"] != params["expectedTurnId"] { return Err("expected-live-turn-mismatch".into()); }
        }
        if method == "turn/interrupt" {
            let turn = &params["turnId"];
            if !i.conversation_turns.iter().any(|t| t["generation"] == i.generation && t["threadId"] == thread && t["turnId"] == *turn && t["nativeTurn"]["status"] == "inProgress" && t["terminalEventObserved"] != true && t["observationEnded"] != true) { return Err("no-live-turn".into()); }
            if i.interrupt_requests.iter().any(|e| own_rpc!=Some(&e["requestIdentity"])&&e["generation"] == i.generation && e["threadId"] == thread && e["turnId"] == *turn
                && (i.client_requests.iter().any(|r| r["generation"] == e["generation"] && r["requestIdentity"] == e["requestIdentity"]
                    && (r["outcome"] == "response-observed-result" || (r["outcome"] == "pending" && r["writeResult"] == "written")))
                    || i.source_requests.get(&e["requestIdentity"].to_string()).is_some_and(|source|source.request.generation==e["generation"]&&i.pending.contains_key(&e["requestIdentity"].to_string())))) { return Err("stop-already-requested".into()); }
        }
        Ok(())
    }

    fn current_live_turn<'a>(i: &'a Inner, thread: &str) -> Option<&'a Value> {
        let latest_event = i.journal.iter().chain(i.held.iter()).filter(|e| e["generation"] == i.generation && e["frame"]["params"]["threadId"] == thread && matches!(e["frame"]["method"].as_str(),Some("turn/started"|"turn/completed"))).max_by_key(|e|e["position"].as_u64().unwrap_or(0));
        let boundary = latest_event.and_then(|e|e["position"].as_u64());
        let fresh_responses: Vec<_> = i.conversation_turns.iter().filter(|e| e["generation"] == i.generation && e["threadId"] == thread && e["source"] == "turn/start response" && e["nativeTurn"]["status"] == "inProgress" && e["terminalEventObserved"] != true && e["observationEnded"] != true && boundary.map(|p|e["startResponseIssuedAfterReceipt"].as_u64().map(|sent|sent>=p).unwrap_or(false)).unwrap_or(true)).collect();
        if fresh_responses.len() == 1 { return Some(fresh_responses[0]); }
        if fresh_responses.len() > 1 { return None; }
        let event = latest_event?;
        if event["frame"]["method"] != "turn/started" || event["frame"]["params"]["turn"]["status"] != "inProgress" { return None; }
        i.conversation_turns.iter().find(|e|e["generation"]==i.generation&&e["threadId"]==thread&&e["turnId"]==event["frame"]["params"]["turn"]["id"]&&e["nativeTurn"]["status"]=="inProgress"&&e["terminalEventObserved"]!=true&&e["observationEnded"]!=true)
    }

    fn spawn_reader(self: &Arc<Self>, stdout: std::process::ChildStdout, generation: Value) {
        let me = Arc::clone(self);
        std::thread::spawn(move || {
            let mut rd = BufReader::new(stdout);
            let mut line = Vec::new();
            loop {
                line.clear();
                match rd.read_until(b'\n', &mut line) {
                    Ok(0) | Err(_) => break,
                    Ok(_) => me.on_line(&line, &generation),
                }
            }
            me.on_eof(&generation);
        });
    }

    fn spawn_stderr(self: &Arc<Self>, mut stderr: std::process::ChildStderr, generation: Value) {
        let me = Arc::clone(self);
        std::thread::spawn(move || {
            // Diagnostic output is counted, never parsed as protocol (§5). Bounded: only the count is kept.
            let mut buf = [0u8; 4096];
            while let Ok(n) = stderr.read(&mut buf) {
                if n == 0 {
                    break;
                }
                let mut i = me.inner.0.lock().unwrap();
                if i.generation == generation { i.stderr_bytes += n as u64; }
            }
        });
    }

    fn on_line(&self, raw: &[u8], generation: &Value) {
        let text = String::from_utf8_lossy(raw);
        let text = text.trim_end_matches(['\n', '\r']);
        if text.is_empty() {
            return;
        }
        let mut i = self.inner.0.lock().unwrap();
        let parsed:Option<Value>=serde_json::from_str(text).ok();
        let correlated_method=parsed.as_ref().and_then(|f|f.get("id")).and_then(|id|i.source_requests.get(&id.to_string())).filter(|e|e.request.generation==*generation).and_then(|e|e.request.frame["method"].as_str());
        let auth_shape=correlated_method.filter(|m|auth_rpc::account_method(m)).map(|method|{
            let raw=parsed.as_ref().unwrap();if raw.get("method").is_some()||raw.get("result").is_some()&&raw.get("error").is_some(){return false;}
            if let Some(error)=raw.get("error"){return error.is_object()&&error["code"].as_i64().is_some()&&error["message"].is_string();}
            let definition=match method{"account/login/start"=>"LoginAccountResponse","account/read"=>"GetAccountResponse","account/logout"=>"LogoutAccountResponse","configRequirements/read"=>"ConfigRequirementsReadResponse",_=>return false};
            raw.get("result").is_some_and(|r|Self::validate_native_result(definition,r).is_ok())
        });
        let known_account_channel=i.account_channels.contains(generation);
        let (frame,projected)=match parsed{Some(frame)if frame.is_object()&&(!known_account_channel||auth_rpc::protocol_envelope(&frame))=>auth_rpc::project_frame(&frame,correlated_method),_ if known_account_channel=>(json!({"observation":"nonprotocol or unparseable diagnostic from known original account source withheld; unattributed, no RPC/method invented"}),true),_ =>(json!(text),false)};
        if &i.generation != generation || i.server_requests.is_closed(generation) {
            i.journal.push(json!({"generation":generation,"class":"closed-generation-frame","frame":frame,"sourceProjection":if projected{Some("sensitive account projection; not original bytes")}else{None}}));return;
        }
        i.receipt_position+=1;let pos=i.receipt_position;let gen=i.generation.clone();
        let class=if frame.is_object()&&frame.get("observation").is_none(){let has_id=frame.get("id").is_some();let has_method=frame.get("method").is_some();if has_method&&has_id{"server-request"}else if has_method{"notification"}else if has_id&&(frame.get("result").is_some()||frame.get("error").is_some()){"response"}else{"malformed"}}else{"malformed"};
        let mut automatic_reply=None;
        if class == "server-request" {
            let capabilities = i.declared_capabilities.clone().unwrap_or(Value::Null);
            match i.server_requests.receive(&gen, pos, &frame, &capabilities) {
                Ok(Some(reply)) => {
                    match self.capture_pipe(&i){Ok(bound)=>automatic_reply=Some((bound,reply)),Err(_)=>i.server_requests.written(&gen,&frame["id"],false)}
                }
                Ok(None) => {
                    if frame["method"] == "currentTime/read" && capabilities["experimentalApi"] == true {
                        let seconds = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs();
                        if let Ok(reply) = i.server_requests.prepare(&gen, &frame["id"], &json!({"currentTimeAt":seconds}), "app-rule:current-time", None) {
                            match self.capture_pipe(&i){Ok(bound)=>automatic_reply=Some((bound,reply)),Err(_)=>i.server_requests.written(&gen,&frame["id"],false)}
                        }
                    }
                }
                Err(reason) => {
                    // Duplicate identities remain visible; never replace their existing custody.
                    i.journal.push(json!({"generation":gen,"class":"request-custody-refused","reason":reason,"receiptPosition":pos}));
                }
            }
        } else if class == "notification" && frame["method"] == "serverRequest/resolved" {
            i.server_requests.resolved(&gen, &frame["params"]);
        }
        if class == "server-request" || (class == "notification" && frame["method"] == "serverRequest/resolved") {
            Self::persist_requests(&mut i);
        }
        if class == "notification" && matches!(frame["method"].as_str(), Some("turn/started" | "turn/completed")) {
            if let Some(thread) = frame["params"]["threadId"].as_str() {
                Self::remember_turn(&mut i, &gen, thread, &frame["params"]["turn"], frame["method"].as_str().unwrap(), pos);
            }
        }
        if class == "malformed" {
            i.malformed += 1;
        }
        if class == "response" {
            let key = frame["id"].to_string();
            if let Some((idx, tx)) = i.pending.remove(&key) {
                let deferred=!i.client_requests[idx].is_object()||i.source_requests.get(&key).is_some_and(|e|e.write_attempt_in_progress);
                if !deferred {
                    let mut record=i.client_requests[idx].clone();
                    match Self::completed_client_response(&mut record,Some(&frame),Some(pos)){Ok(())=>i.client_requests[idx]=record,Err(error)=>if let Some(e)=i.source_requests.get_mut(&key){e.source_limit=Some(error)}}
                }
                if !deferred&&i.client_requests[idx]["method"] == "turn/start" {
                    if let Some((source_gen, thread, sent_after_receipt)) = i.turn_request_threads.remove(&key) {
                        if source_gen == gen {
                            if let Some(turn) = frame.get("result").and_then(|r| r.get("turn")) {
                                Self::remember_turn(&mut i, &gen, &thread, turn, "turn/start response", pos);
                                if let Some(entry) = i.conversation_turns.iter_mut().find(|e| e["generation"] == gen && e["threadId"] == thread && e["turnId"] == turn["id"] && e["source"] == "turn/start response" && e["receiptPosition"] == pos) { entry["startResponseIssuedAfterReceipt"] = json!(sent_after_receipt); }
                            }
                        }
                    }
                }
                if let Some(e) = i.source_requests.get_mut(&key) { e.response = Some(frame.clone()); e.response_position=Some(pos); e.auth_response_shape=auth_shape; }
                let _ = tx.send(frame.clone());
                // Responses are also journaled, with their metadata beside the native frame (H6).
                let entry = json!({"generation": gen, "position": pos, "class": class, "frame": frame,"sourceProjection":if projected{Some("sensitive account projection; not original bytes")}else{None}});
                if i.state == "handshaking" { i.held.push(entry); } else { i.journal.push(entry); }
                let attachment_source = i.source_requests.get(&key).filter(|e|e.attachment.is_some()).map(|e|e.request.clone());
                drop(i);
                if let Some(source) = attachment_source { let _ = self.persist_attachment_observation(&source); }
                return;
            }
            // Uncorrelated response: surfaced, never dropped (§5).
            let entry = json!({"generation": gen, "position": pos, "class": "uncorrelated-response", "frame": frame,"sourceProjection":if projected{Some("sensitive account projection; not original bytes")}else{None}});
            if i.state == "handshaking" { i.held.push(entry); } else { i.journal.push(entry); }
            return;
        }
        let entry = json!({"generation": gen, "position": pos, "class": class, "frame": frame,"sourceProjection":if projected{Some("sensitive account projection; not original bytes")}else{None}});
        if i.state == "handshaking" {
            i.held.push(entry); // H4
        } else {
            i.journal.push(entry);
        }
        drop(i);
        self.flush_recovery_observations();
        if let Some((bound,reply))=automatic_reply{let generation=bound.generation.clone();let id=reply["id"].clone();if self.write_reply(bound,&reply).is_err(){let mut i=self.inner.0.lock().unwrap();if i.generation==generation&&!i.server_requests.is_closed(&generation){i.server_requests.written(&generation,&id,false);Self::persist_requests(&mut i);}}}
    }

    fn on_eof(&self, generation: &Value) {
        let source_pid={let mut i=self.inner.0.lock().unwrap();i.account_channels.retain(|g|g!=generation);if i.generation!=*generation{return;}i.child_pid};
        // Reap only the captured owning child, never a successor installed
        // between the first scope check and the final source gate.
        let status=self.child.lock().unwrap().as_mut().filter(|c|Some(c.id() as i32)==source_pid).and_then(|c|c.wait().ok());
        #[cfg(test)]
        if let Some(hook) = self.before_eof_gate.lock().unwrap().take() { hook(); }
        let _source_gate = self.attachment_gate.lock().unwrap();
        let mut i = self.inner.0.lock().unwrap();
        if i.generation != *generation {
            i.journal.push(json!({"generation":generation,"class":"superseded-generation-eof","standing":"EOF observer belongs to a superseded source; no successor closure inferred"}));
            return;
        }
        let exit = json!({
            "exitCode": status.and_then(|s| s.code()),
            "signal": status.and_then(|s| std::os::unix::process::ExitStatusExt::signal(&s)).map(|s| s.to_string()),
            "lastReceiptPosition": i.receipt_position,
            "malformedFrameCount": i.malformed,
            "diagnosticOutputBytes": i.stderr_bytes,
        });
        let counts = Self::close_generation(&mut i);
        if i.state == "stopping" {
            // LT-23 is written by stop(), which owns the descendant check.
            let gen = i.generation.clone();
            i.journal.push(json!({"generation": gen, "class": "exit", "exitFacts": exit}));
            self.inner.1.notify_all();drop(i);drop(_source_gate);self.flush_recovery_observations();
            return;
        }
        if i.state == "ready" {
            // LT-12: ended with no App stop record, whatever the exit status (S-F-07).
            self.lt(&mut i, "LT-12", "child-ended-without-stop-record", "exited-unexpectedly",
                    json!({"exitFacts": exit, "closedGeneration": counts}));
        }
        drop(i);drop(_source_gate);self.flush_recovery_observations();
    }

    fn kill_group(&self) {
        if let Some(pid) = self.inner.0.lock().unwrap().child_pid {
            // SAFETY: plain signal to the process group created at spawn (H11).
            unsafe {
                libc::killpg(pid, libc::SIGKILL);
            }
        }
    }

    fn group_alive(pid: i32) -> bool {
        // SAFETY: signal 0 only checks for existence of the group.
        unsafe { libc::killpg(pid, 0) == 0 }
    }

    /// HOSTING §4.5 deliberate stop (DEF-5a): stop record first, then close input,
    /// then end the whole process group after a grace period (H11).
    pub fn stop(&self, actor: &str, reason: &str) -> Result<Value, String> {
        let source_gate = self.attachment_gate.lock().unwrap();
        let pid;let target_generation;
        {
            let mut i = self.inner.0.lock().unwrap();
            if matches!(i.state.as_str(), "absent" | "stopped" | "refused") {
                return Err(format!("stop not accepted in state {}", i.state));
            }
            if i.state=="stopping" {return Err("stop already requested for this source generation".into());}
            target_generation=i.generation.clone();
            let stop_record = json!({"actor": actor, "reason": reason,
                "outstandingEntryHandling": "left-to-end-with-process", "endingMeans": "close-input"});
            i.stop_record = Some(stop_record.clone());
            let id = match i.state.as_str() {
                "ready" => "LT-17",
                "handshaking" => "LT-18",
                _ => "LT-19",
            };
            self.lt(&mut i, id, "stop-requested", "stopping", json!({"actor": actor, "stopRecord": stop_record}));
            pid = i.child_pid;
            i.attachment_pipe_epoch += 1;
        }
        *self.stdin.lock().unwrap() = None; // close input: polite end
        drop(source_gate);
        let mut forced = false;
        if let Some(pid) = pid {
            let deadline = std::time::Instant::now() + Duration::from_secs(3);
            while Self::group_alive(pid) && std::time::Instant::now() < deadline {
                std::thread::sleep(Duration::from_millis(50));
            }
            if Self::group_alive(pid) {
                forced = true;
                unsafe {libc::killpg(pid,libc::SIGKILL);}
                std::thread::sleep(Duration::from_millis(200));
            }
        }
        let surviving = pid.map(|p| if Self::group_alive(p) { 1 } else { 0 }).unwrap_or(0);
        // Wait for the reader to observe EOF.
        let (lock, cv) = &*self.inner;
        let mut i = lock.lock().unwrap();
        let deadline = std::time::Instant::now() + Duration::from_secs(3);
        while i.generation==target_generation&&!i.journal.iter().any(|e| e["class"] == "exit" && e["generation"] == target_generation)
            && std::time::Instant::now() < deadline
        {
            let (g, _) = cv.wait_timeout(i, Duration::from_millis(100)).unwrap();
            i = g;
        }
        let mut exit = i.journal.iter().rev().find(|e| e["class"] == "exit" && e["generation"] == target_generation).map(|e| e["exitFacts"].clone())
            .unwrap_or(json!({"exitCode": null, "signal": null}));
        exit["forcedAfterGrace"] = json!(forced);
        if i.generation!=target_generation {
            i.journal.push(json!({"generation":target_generation,"class":"superseded-generation-stop","capturedProcessGroup":pid,"forced":forced,"survivingDescendantCount":surviving,"standing":"captured old target handled; successor is not stopped or closed"}));
            return Err("Stop target generation was replaced while waiting; no successor closure inferred".into());
        }
        let counts = Self::close_generation(&mut i);
        self.lt(&mut i, "LT-23", "tree-ended", "stopped", json!({
            "exitFacts": exit,
            "descendants": {"checked": true, "surviving": surviving, "handling": if surviving > 0 { "recorded; not ended" } else { "none surviving" }},
            "closedGeneration": counts}));
        let response=json!({"state":i.state});drop(i);self.flush_recovery_observations();Ok(response)
    }
}

/// Historical supplier observation, separate from current App socket observation.
fn network_disclosure() -> Value {
    json!({
        "currentSupplierVersion": DECLARED_PIN,
        "observationSourceVersion": "0.158.0",
        "source": "expected-at-pin",
        "observedByApp": false,
        "samplingLimits": "historical bounded observations; current child sockets not sampled by this snapshot",
        "entries": [
            {"phase": "startup", "purpose": "supplier-service", "destination": "chatgpt.com; github.com/openai/plugins", "condition": "provider/plugin/account dependent; plugins follow user configuration"},
            {"phase": "thread-start", "purpose": "model", "destination": "selected model provider", "detail": "Responses websocket prewarm can contact the selected model provider before a turn; default hosted provider observed at 0.158.0"}
        ]
    })
}

fn generated_outputs_match() -> bool {
    [
        (include_bytes!("../resources/supplier/0.160.0/MANIFEST.sha256").as_slice(), "411ea5d47035908768562eecfed33f16e2cb3de944c84c96fd8e70ca7086b8be"),
        (include_bytes!("../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json").as_slice(), "7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5"),
        (include_bytes!("../resources/supplier/0.160.0/codex_app_server_protocol.v2.schemas.json").as_slice(), "e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c"),
    ].iter().all(|(bytes, expected)| sha256_hex(bytes) == *expected)
}

#[cfg(test)]
fn install_broken_test_input(host:&Host){let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::null()).stderr(Stdio::null()).spawn().unwrap();let pipe=child.stdin.take();child.kill().unwrap();child.wait().unwrap();*host.stdin.lock().unwrap()=pipe;}

#[cfg(test)]
mod hosting_identity_tests {
    use super::*;
    #[test]
    fn foreign_session_home_or_counter_cannot_correlate_a_response() {
        let host = Host::new();
        let current = json!({"appSession":"session-a", "home":"home-a", "spawnCounter":1});
        let (tx, rx) = channel();
        {
            let mut i = host.inner.0.lock().unwrap();
            i.generation = current.clone();
            i.state = "ready".into();
            i.client_requests.push(json!({"recordKind":"client-request","generation":current,"requestIdentity":1,"method":"thread/list","initiator":{"kind":"person-directed"},"writeResult":"written","outcome":"pending"}));
            i.pending.insert("1".into(), (0, tx));
        }
        for foreign in [
            json!({"appSession":"session-b","home":"home-a","spawnCounter":1}),
            json!({"appSession":"session-a","home":"home-b","spawnCounter":1}),
            json!({"appSession":"session-a","home":"home-a","spawnCounter":2}),
            json!(1),
        ] {
            host.on_line(br#"{"id":1,"result":{"foreign":true}}"#, &foreign);
            assert!(rx.try_recv().is_err());
            assert_eq!(host.client_requests()[0]["outcome"], "pending");
        }
        host.on_line(br#"{"id":1,"result":{"current":true}}"#, &current);
        assert_eq!(rx.try_recv().unwrap()["result"]["current"], true);
        assert_eq!(host.client_requests()[0]["outcome"], "response-observed-result");
    }
    #[test]
    fn generated_resource_bytes_match_reviewed_pin() {
        assert!(generated_outputs_match());
    }
}

#[cfg(test)]
mod request_transport_tests {
    use super::*;
    fn host() -> Host {
        let host = Host::new();
        let mut i = host.inner.0.lock().unwrap();
        i.generation = json!({"appSession":"s","home":"h","spawnCounter":1});
        i.state = "ready".into();
        i.declared_capabilities = Some(json!({"experimentalApi":false}));
        drop(i); host
    }
    #[test]
    fn observer_reload_preserves_order_and_request_custody_without_writing() {
        let host = host(); let generation = host.snapshot()["generation"].clone();
        host.on_line(br#"{"method":"future/notification","params":{"raw":1},"extra":true}"#,&generation);
        host.on_line(br#"{"id":"r","method":"item/fileChange/requestApproval","params":{"threadId":"t","itemId":"i"},"extra":42}"#,&generation);
        let initial = host.observe(&generation,0);
        assert_eq!(initial["frames"].as_array().unwrap().len(),2);
        assert_eq!(initial["frames"][1]["frame"]["extra"],42);
        assert_eq!(initial["snapshot"]["serverRequests"][0]["state"],"outstanding");
        // No observer object owns the process; closing a window needs no mutation.
        host.on_line(br#"{"method":"future/notification","params":{"raw":2}}"#,&generation);
        let next = host.observe(&generation,2);
        assert_eq!(next["frames"].as_array().unwrap().len(),1);
        assert_eq!(next["frames"][0]["position"],3);
        assert_eq!(host.inner.0.lock().unwrap().send_position,0);
        assert_eq!(host.snapshot()["serverRequests"][0]["state"],"outstanding");
        assert_eq!(host.observe(&json!(1),0)["gap"],true);
    }
    #[test]
    fn unknown_transport_write_failure_is_visible_and_generation_close_never_grants() {
        let host = host(); let generation = host.snapshot()["generation"].clone();
        host.on_line(br#"{"id":1,"method":"future/request","params":{"threadId":"t"}}"#,&generation);
        assert_eq!(host.snapshot()["serverRequests"][0]["state"],"errored");
        assert_eq!(host.snapshot()["serverRequests"][0]["replyWriteResult"],"write-failed");
        host.on_line(br#"{"id":2,"method":"item/fileChange/requestApproval","params":{"threadId":"t"}}"#,&generation);
        let counts = Host::close_generation(&mut host.inner.0.lock().unwrap());
        assert_eq!(counts["endedUnanswered"],1);
        assert_eq!(host.snapshot()["serverRequests"][1]["state"],"ended-unanswered");
        assert_eq!(host.answer_server_request(&generation,&json!(2),&json!({"decision":"accept"}),"person-via-interaction",Some("person:Invented/test/unknown (identity not verified)")).unwrap_err(),"generation-closed");
    }
}

#[cfg(test)]
mod closed_receipt_repair_tests {
    use super::*;
    #[test]
    fn same_tuple_after_close_is_journaled_without_live_registry_mutation() {
        let host=Host::new();let generation=json!({"appSession":"s","home":"h","spawnCounter":1});
        {let mut i=host.inner.0.lock().unwrap();i.generation=generation.clone();i.state="ready".into();}
        host.on_line(br#"{"id":1,"method":"item/fileChange/requestApproval","params":{"threadId":"t"}}"#,&generation);
        Host::close_generation(&mut host.inner.0.lock().unwrap());let before=host.snapshot()["serverRequests"].clone();let pos=host.inner.0.lock().unwrap().receipt_position;
        for late in [br#"{"id":2,"method":"item/fileChange/requestApproval","params":{"threadId":"t"},"nativeExtra":true}"#.as_slice(),br#"{"id":3,"method":"future/request","params":{"threadId":"t"},"nativeExtra":"unknown"}"#.as_slice()] {
            host.on_line(late,&generation);assert_eq!(host.snapshot()["serverRequests"],before);assert_eq!(host.inner.0.lock().unwrap().receipt_position,pos);
            let journal=host.journal();let last=journal.last().unwrap();assert_eq!(last["class"],"closed-generation-frame");assert_eq!(last["frame"],serde_json::from_slice::<Value>(late).unwrap());
        }
        let successor=json!({"appSession":"s","home":"h","spawnCounter":2});{host.inner.0.lock().unwrap().generation=successor.clone();}
        host.on_line(br#"{"id":4,"method":"item/fileChange/requestApproval","params":{"threadId":"t"}}"#,&successor);let successor_before=host.snapshot()["serverRequests"].clone();
        host.on_line(br#"{"id":5,"method":"future/request","params":{"threadId":"t"}}"#,&generation);assert_eq!(host.snapshot()["serverRequests"],successor_before);
    }
}

#[cfg(test)]
mod missing_custody_mapping_tests {
    use super::*;
    #[test]
    fn later_known_request_rule_error_records_native_settlement_in_reviewed_rq03() {
        let path=std::env::temp_dir().join(format!("recovery-known-error-{}",opaque_id("test").unwrap()));
        let host=Host::new();host.configure_recovery(path.clone()).unwrap();let generation;
        {let mut i=host.inner.0.lock().unwrap();generation=json!({"appSession":i.app_session,"home":"h","spawnCounter":1});i.generation=generation.clone();i.state="ready".into();}
        host.on_line(br#"{"id":1,"method":"mcpServer/elicitation/request","params":{"threadId":"t","turnId":null,"serverName":"invented-server","mode":"url","message":"invented request","elicitationId":"invented-elicitation","url":"https://example.invalid/request"}}"#,&generation);
        let error=json!({"code":-32603,"message":"invented named-rule error","data":{"nativeExtra":"preserved"}});
        assert_eq!(host.error_server_request(&generation,&json!(1),&error,"person-via-interaction").unwrap_err(),"origin-not-permitted");
        // Echo-only stdio double: no supplier/model/account or network operation.
        let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();
        let result=host.error_server_request(&generation,&json!(1),&error,"app-rule:invented-error").unwrap();assert_eq!(result["replyWriteResult"],"written");assert_eq!(result["acknowledgment"],"not-observed");
        let mut line=String::new();BufReader::new(child.stdout.take().unwrap()).read_line(&mut line).unwrap();assert_eq!(serde_json::from_str::<Value>(&line).unwrap(),json!({"id":1,"error":error}));*host.stdin.lock().unwrap()=None;assert!(child.wait().unwrap().success());
        let snapshot=host.snapshot();let entry=&snapshot["serverRequests"][0];assert_eq!(entry["generation"],generation);assert_eq!(entry["requestIdentity"],1);assert_eq!(entry["settlement"]["nativeContent"],error);assert_eq!(entry["settlement"]["origin"],json!({"class":"app-rule","ruleName":"invented-error"}));assert_eq!(entry["state"],"errored");assert_eq!(entry["replyWriteResult"],"written");assert_eq!(entry["acknowledgmentObservation"]["status"],"not-observed");assert_eq!(snapshot["recoveryPersistenceError"],Value::Null);
        let entries=snapshot["recovery"]["entries"].as_array().unwrap();assert_eq!(entries.len(),3);assert_eq!(entries[1]["transition"],"RQ-01");assert_eq!(entries[2]["transition"],"RQ-03");assert_eq!(entries[2]["endedAs"],"errored");assert_eq!(entries[2]["replyWrite"],"written");assert_eq!(entries[2]["origin"],"app-rule:invented-error");assert_eq!(crate::recovery::generation_from_ref(entries[2]["generation"].as_str().unwrap()).unwrap(),generation);assert!(entries.iter().all(|e|e["transition"]!="RQ-08"&&e["kind"]!="human_act"));assert!(entries[2]["subject"].get("turnId").is_none());std::fs::remove_file(path).unwrap();
    }
}

#[cfg(test)]
mod additive_guidance_transport_tests {
    use super::*;
    #[test]
    fn additive_params_are_native_valid_and_preserve_bytes_without_policy_or_base_fields() {
        let text="Common guidance\n\nTASK role: é / 家\n";
        let params=Host::thread_start_params("/invented/work","explicit-model","explicit-provider",Some(text)).unwrap();
        assert_eq!(params,json!({"cwd":"/invented/work","model":"explicit-model","modelProvider":"explicit-provider","developerInstructions":text}));
        let mut schema:Value=serde_json::from_str(include_str!("../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json")).unwrap();schema["$ref"]=json!("#/definitions/v2/ThreadStartParams");jsonschema::options().offline().build(&schema).unwrap().validate(&params).unwrap();
        assert_eq!(Host::thread_start_params("/invented/work","m","p",None).unwrap(),json!({"cwd":"/invented/work","model":"m","modelProvider":"p"}));
        assert!(Host::thread_start_params("/invented/work"," ","p",Some(text)).is_err());assert!(Host::thread_start_params("/invented/work","m","",Some(text)).is_err());
    }
    struct MockRun { result: Result<Value,String>, outbound: Value, native_response: Value, snapshot: Value, generation: Value }
    fn mock_thread_start(guidance: Option<&str>, successor: Option<Value>) -> MockRun {
        let host=Arc::new(Host::new());let generation=json!({"appSession":"mock-session","home":"mock-home","spawnCounter":1});
        {let mut i=host.inner.0.lock().unwrap();i.generation=generation.clone();i.state="ready".into();i.supplier_standing=Some("unverified-development".into());}
        if let Some(successor)=successor {
            let me=Arc::clone(&host);
            *host.before_thread_insert.lock().unwrap()=Some(Box::new(move|| {
                // Deterministic boundary: the actual response is already received
                // and journaled, while the wrapper has not inserted its thread.
                let mut i=me.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation=successor;i.state="ready".into();
            }));
        }
        // cat is an echo-only transport double, not Codex or a model. Clear
        // the environment and exercise the actual ChildStdin write/correlation.
        let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();
        *host.stdin.lock().unwrap()=child.stdin.take();let stdout=child.stdout.take().unwrap();let me=Arc::clone(&host);let g=generation.clone();let (tx,rx)=channel();
        let worker=std::thread::spawn(move|| {
            let mut line=String::new();BufReader::new(stdout).read_line(&mut line).unwrap();let frame:Value=serde_json::from_str(&line).unwrap();
            let response=json!({"id":frame["id"],"result":{"thread":{"id":"mock-thread","status":"idle"},"model":"reported-model","modelProvider":"reported-provider","cwd":"/reported/work"}});
            tx.send((frame,response.clone())).unwrap();me.on_line(&serde_json::to_vec(&response).unwrap(),&g);
        });
        let result=match guidance {Some(text)=>host.thread_start_with_guidance("/invented/work","chosen-model","chosen-provider",text),None=>host.thread_start_selected("/invented/work","chosen-model","chosen-provider")};
        let (outbound,native_response)=rx.recv().unwrap();worker.join().unwrap();*host.stdin.lock().unwrap()=None;assert!(child.wait().unwrap().success());
        MockRun { result,outbound,native_response,snapshot:host.snapshot(),generation }
    }
    #[test]
    fn both_public_wrappers_use_the_same_stdio_correlation_and_thread_snapshot_path() {
        for guidance in [None,Some("Exact role bytes\n\né / 家\n")] {
            let run=mock_thread_start(guidance,None);let response=run.result.unwrap();
            assert_eq!(run.outbound["method"],"thread/start");assert_eq!(run.outbound["params"],Host::thread_start_params("/invented/work","chosen-model","chosen-provider",guidance).unwrap());assert_eq!(response,run.native_response);
            let thread=&run.snapshot["threads"][0];assert_eq!(thread["generation"],run.generation);assert_eq!(thread["supplierStanding"],"unverified-development");assert_eq!(thread["requestedDestination"]["model"],"chosen-model");assert_eq!(thread["reportedDestination"]["model"],"reported-model");assert_eq!(run.snapshot["clientRequests"][0]["outcome"],"response-observed-result");assert_eq!(run.snapshot["journal"][0]["frame"],run.native_response);
        }
    }
    #[test]
    fn scoped_start_refuses_replaced_registration_and_keeps_write_failure_unknown() {
        let host=Host::new();let old=json!({"appSession":"s","home":"h","spawnCounter":1});let current=json!({"appSession":"s","home":"h","spawnCounter":2});
        {let mut i=host.inner.0.lock().unwrap();i.state="ready".into();i.generation=current.clone();}
        let error=host.request_inner_scoped("thread/start",json!({"model":"m","modelProvider":"p"}),json!({"kind":"person-directed"}),Duration::from_secs(1),false,Some(&old)).unwrap_err();
        assert!(error.contains("generation changed before request registration"));assert_eq!(host.snapshot()["clientRequests"],json!([]));assert_eq!(host.inner.0.lock().unwrap().send_position,0);
        install_broken_test_input(&host);let error=host.thread_start_with_guidance("/invented","m","p","exact guidance").unwrap_err();assert!(error.contains("write failed"));
        let snapshot=host.snapshot();assert_eq!(snapshot["clientRequests"][0]["generation"],current);assert_eq!(snapshot["clientRequests"][0]["writeResult"],"write-failed");assert_eq!(snapshot["clientRequests"][0]["outcome"],"unknown-no-response");assert_eq!(snapshot["threads"],json!([]));
    }
    #[test]
    fn response_before_generation_transition_never_mutates_successor_thread_snapshot() {
        for guidance in [None,Some("Exact role bytes\n\né / 家\n")] {
            for successor in [json!({"appSession":"mock-session","home":"mock-home","spawnCounter":2}),json!({"appSession":"next-session","home":"mock-home","spawnCounter":1}),json!({"appSession":"mock-session","home":"next-home","spawnCounter":1})] {
                let run=mock_thread_start(guidance,Some(successor.clone()));
                assert!(run.result.unwrap_err().contains("closed or replaced generation"));assert_eq!(run.snapshot["generation"],successor);assert_eq!(run.snapshot["threads"],json!([]));
                assert_eq!(run.outbound["params"],Host::thread_start_params("/invented/work","chosen-model","chosen-provider",guidance).unwrap());assert_eq!(run.snapshot["clientRequests"][0]["generation"],run.generation);assert_eq!(run.snapshot["clientRequests"][0]["outcome"],"response-observed-result");assert_eq!(run.snapshot["journal"][0]["generation"],run.generation);assert_eq!(run.snapshot["journal"][0]["frame"],run.native_response);
            }
        }
    }
}

#[cfg(test)]
mod conversation_transport_tests {
    use super::*;
    fn g()->Value {json!({"appSession":"conversation-session","home":"conversation-home","spawnCounter":1})}
    fn host()->Arc<Host> {
        let host=Arc::new(Host::new());{let mut i=host.inner.0.lock().unwrap();i.state="ready".into();i.generation=g();i.threads.push(json!({"generation":g(),"threadId":"thread","model":"selected","modelProvider":"selected-provider"}));}host
    }
    fn turn(status:&str)->Value {json!({"id":"turn","status":status,"items":[],"itemsView":"full","nativeExtra":{"unchanged":true}})}
    fn event(host:&Host,status:&str) {host.on_line(&serde_json::to_vec(&json!({"method":if status=="inProgress"{"turn/started"}else{"turn/completed"},"params":{"threadId":"thread","turn":turn(status)}})).unwrap(),&g());}
    fn exchange<F>(host:&Arc<Host>,response:Option<Value>,before:Vec<Value>,operation:F)->(Result<Value,String>,Value)
        where F:FnOnce()->Result<Value,String> {
        let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();let stdout=child.stdout.take().unwrap();let me=Arc::clone(host);let(tx,rx)=channel();
        let worker=std::thread::spawn(move|| {
            let mut line=String::new();BufReader::new(stdout).read_line(&mut line).unwrap();let outbound:Value=serde_json::from_str(&line).unwrap();tx.send(outbound.clone()).unwrap();
            for frame in before {me.on_line(&serde_json::to_vec(&frame).unwrap(),&g());}
            if let Some(mut frame)=response {frame["id"]=outbound["id"].clone();me.on_line(&serde_json::to_vec(&frame).unwrap(),&g());}
        });
        let result=operation();let outbound=rx.recv().unwrap();worker.join().unwrap();*host.stdin.lock().unwrap()=None;assert!(child.wait().unwrap().success());(result,outbound)
    }
    #[test]
    fn required_native_text_and_interrupt_params_match_generated_schema_without_overrides() {
        let text="Exact\n\né / 家\n{\"approvalPolicy\":\"never\"}";let params=Host::text_turn_params("thread",text).unwrap();assert_eq!(params,json!({"threadId":"thread","input":[{"type":"text","text":text,"text_elements":[]}]}));
        let source:Value=serde_json::from_str(include_str!("../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json")).unwrap();for (target,params) in [("TurnStartParams",params),("TurnInterruptParams",json!({"threadId":"thread","turnId":"turn"}))] {let mut schema=source.clone();schema["$ref"]=json!(format!("#/definitions/v2/{target}"));jsonschema::options().offline().build(&schema).unwrap().validate(&params).unwrap();}
        assert!(Host::text_turn_params("",text).is_err());assert!(Host::text_turn_params("thread","").is_err());
    }
    #[test]
    fn actual_text_pipe_response_and_interrupt_ack_do_not_invent_turn_end_or_model_witness() {
        let host=host();let text="exact text\n\né / 家";
        let (result,outbound)=exchange(&host,Some(json!({"result":{"turn":turn("inProgress")}})),vec![],||host.turn_start_text(&g(),"thread",text));assert_eq!(result.unwrap()["result"]["turn"],turn("inProgress"));assert_eq!(outbound["method"],"turn/start");assert_eq!(outbound["params"],Host::text_turn_params("thread",text).unwrap());let snapshot=host.snapshot();assert_eq!(snapshot["conversationTurns"][0]["nativeTurn"]["status"],"inProgress");assert_eq!(snapshot["modelTurnExercised"],Value::Null);assert_eq!(snapshot["modelTurnEvidence"]["protocolRequests"][0]["outcome"],"response-observed-result");
        let (ack,outbound)=exchange(&host,Some(json!({"result":{}})),vec![],||host.turn_interrupt(&g(),"thread","turn"));assert_eq!(ack.unwrap()["result"],json!({}));assert_eq!(outbound["params"],json!({"threadId":"thread","turnId":"turn"}));assert_eq!(host.snapshot()["conversationTurns"][0]["nativeTurn"]["status"],"inProgress");
        let count=host.client_requests().len();assert_eq!(host.turn_interrupt(&g(),"thread","turn").unwrap_err(),"stop-already-requested");assert_eq!(host.client_requests().len(),count);event(&host,"interrupted");assert_eq!(host.snapshot()["conversationTurns"][0]["nativeTurn"]["status"],"interrupted");assert_eq!(host.turn_interrupt(&g(),"thread","turn").unwrap_err(),"no-live-turn");
    }
    #[test]
    fn foreign_closed_unknown_thread_and_unknown_turn_are_not_registered_or_written() {
        let host=host();for foreign in [json!(1),json!({"appSession":"other","home":"conversation-home","spawnCounter":1}),json!({"appSession":"conversation-session","home":"other","spawnCounter":1}),json!({"appSession":"conversation-session","home":"conversation-home","spawnCounter":2})] {assert!(host.turn_start_text(&foreign,"thread","text").is_err());}
        assert!(host.turn_start_text(&g(),"unknown","text").unwrap_err().contains("conversation-not-loaded"));assert_eq!(host.turn_interrupt(&g(),"thread","unknown").unwrap_err(),"no-live-turn");assert_eq!(host.inner.0.lock().unwrap().send_position,0);assert!(host.client_requests().is_empty());Host::close_generation(&mut host.inner.0.lock().unwrap());assert!(host.turn_start_text(&g(),"thread","text").is_err());assert_eq!(host.inner.0.lock().unwrap().send_position,0);
    }
    #[test]
    fn native_error_failed_write_and_wait_limit_keep_distinct_evidence_and_late_response() {
        let host=host();let error=json!({"code":-32600,"message":"invented refusal","data":{"native":"kept"}});let (result,_)=exchange(&host,Some(json!({"error":error})),vec![],||host.turn_start_text(&g(),"thread","text"));assert!(result.unwrap_err().contains("native error"));assert_eq!(host.journal().last().unwrap()["frame"]["error"],error);assert_eq!(host.client_requests()[0]["outcome"],"response-observed-error");assert_eq!(host.snapshot()["conversationTurns"],json!([]));
        install_broken_test_input(&host);assert!(host.turn_start_text(&g(),"thread","text").unwrap_err().contains("write failed"));assert_eq!(host.client_requests()[1]["outcome"],"unknown-no-response");assert_eq!(host.client_requests()[1]["writeResult"],"write-failed");
        let (result,outbound)=exchange(&host,None,vec![],||host.conversation_operation("turn/start",&g(),Host::text_turn_params("thread","late text").unwrap(),Duration::from_millis(15)));assert!(result.unwrap_err().contains("wait limit"));assert_eq!(host.client_requests()[2]["outcome"],"pending");assert_eq!(host.client_requests()[2]["waitingEnded"],true);
        host.on_line(&serde_json::to_vec(&json!({"id":outbound["id"],"result":{"turn":turn("inProgress")}})).unwrap(),&g());assert_eq!(host.client_requests()[2]["outcome"],"response-observed-result");assert_eq!(host.snapshot()["conversationTurns"][0]["nativeTurn"]["status"],"inProgress");
    }
    #[test]
    fn completion_before_start_response_is_not_revived_by_late_in_progress_result() {
        let host=host();let completed=json!({"method":"turn/completed","params":{"threadId":"thread","turn":turn("completed")},"nativeExtra":"event"});let (result,_)=exchange(&host,Some(json!({"result":{"turn":turn("inProgress")}})),vec![completed.clone()],||host.turn_start_text(&g(),"thread","text"));assert_eq!(result.unwrap()["result"]["turn"]["status"],"inProgress");assert_eq!(host.snapshot()["conversationTurns"][0]["nativeTurn"]["status"],"completed");assert_eq!(host.journal()[0]["frame"],completed);
    }
    #[test]
    fn interrupt_error_timeout_and_closure_do_not_claim_effect_or_automatic_retry() {
        let host=host();event(&host,"inProgress");let (result,_)=exchange(&host,Some(json!({"error":{"code":-32600,"message":"interrupt refused"}})),vec![],||host.turn_interrupt(&g(),"thread","turn"));assert!(result.unwrap_err().contains("native error"));assert_eq!(host.snapshot()["conversationTurns"][0]["nativeTurn"]["status"],"inProgress");
        let (result,_)=exchange(&host,None,vec![],||host.conversation_operation("turn/interrupt",&g(),json!({"threadId":"thread","turnId":"turn"}),Duration::from_millis(15)));assert!(result.is_err());assert_eq!(host.turn_interrupt(&g(),"thread","turn").unwrap_err(),"stop-already-requested");let count=host.client_requests().len();Host::close_generation(&mut host.inner.0.lock().unwrap());assert_eq!(host.client_requests().len(),count);assert_eq!(host.client_requests().last().unwrap()["outcome"],"unknown-no-response");let turn=&host.snapshot()["conversationTurns"][0];assert_eq!(turn["nativeTurn"]["status"],"inProgress");assert_eq!(turn["observationEnded"],true);
    }
    #[test]
    fn exact_completed_then_started_repro_preserves_terminal_and_raw_inconsistency() {
        let host=host();event(&host,"completed");let before=host.snapshot()["conversationTurns"][0].clone();
        let late=json!({"method":"turn/started","params":{"threadId":"thread","turn":turn("inProgress")},"nativeExtra":"contradictory source preserved"});
        host.on_line(&serde_json::to_vec(&late).unwrap(),&g());let snapshot=host.snapshot();let record=&snapshot["conversationTurns"][0];
        assert_eq!(record["nativeTurn"],before["nativeTurn"]);assert_eq!(record["source"],before["source"]);assert_eq!(record["receiptPosition"],before["receiptPosition"]);assert_eq!(record["terminalEventObserved"],true);assert_eq!(record["inconsistencyLimits"][0]["source"],"turn/started");assert_eq!(record["inconsistencyLimits"][0]["reportedStatus"],"inProgress");assert_eq!(host.journal().last().unwrap()["frame"],late);
        assert_eq!(Host::check_conversation_request(&host.inner.0.lock().unwrap(),"turn/interrupt",&json!({"threadId":"thread","turnId":"turn"})).unwrap_err(),"no-live-turn");assert_eq!(host.turn_interrupt(&g(),"thread","turn").unwrap_err(),"no-live-turn");assert_eq!(host.inner.0.lock().unwrap().send_position,0);
        // Terminal guard is independent of raw-payload status, even if a
        // future reading accidentally supplies an active-looking payload.
        host.inner.0.lock().unwrap().conversation_turns[0]["nativeTurn"]["status"]=json!("inProgress");assert_eq!(host.turn_interrupt(&g(),"thread","turn").unwrap_err(),"no-live-turn");
    }
    #[test]
    fn all_processed_active_like_sources_and_late_start_response_stay_non_live() {
        let host=host();event(&host,"interrupted");let terminal=host.snapshot()["conversationTurns"][0]["nativeTurn"].clone();
        let active_completed=json!({"method":"turn/completed","params":{"threadId":"thread","turn":turn("inProgress")}});host.on_line(&serde_json::to_vec(&active_completed).unwrap(),&g());assert_eq!(host.snapshot()["conversationTurns"][0]["nativeTurn"],terminal);
        let (response,_)=exchange(&host,Some(json!({"result":{"turn":turn("inProgress")}})),vec![],||host.turn_start_text(&g(),"thread","exact text"));assert_eq!(response.unwrap()["result"]["turn"]["status"],"inProgress");let record=host.snapshot()["conversationTurns"][0].clone();assert_eq!(record["nativeTurn"],terminal);assert_eq!(record["inconsistencyLimits"].as_array().unwrap().len(),2);assert_eq!(host.turn_interrupt(&g(),"thread","turn").unwrap_err(),"no-live-turn");
        // A distinct native turn ID in the same thread is an ordinary new turn,
        // not revival of the completed tuple.
        let mut next=turn("inProgress");next["id"]=json!("next-turn");host.on_line(&serde_json::to_vec(&json!({"method":"turn/started","params":{"threadId":"thread","turn":next}})).unwrap(),&g());assert!(Host::check_conversation_request(&host.inner.0.lock().unwrap(),"turn/interrupt",&json!({"threadId":"thread","turnId":"next-turn"})).is_ok());
    }
    #[test]
    fn full_tuple_transition_after_response_cannot_mutate_successor_turn_state() {
        for method in ["turn/start","turn/interrupt"] {for successor in [json!({"appSession":"conversation-session","home":"conversation-home","spawnCounter":2}),json!({"appSession":"other","home":"conversation-home","spawnCounter":1}),json!({"appSession":"conversation-session","home":"other","spawnCounter":1})] {
            let host=host();if method=="turn/interrupt" {event(&host,"inProgress");}let me=Arc::clone(&host);let next=successor.clone();*host.before_turn_result.lock().unwrap()=Some(Box::new(move||{let mut i=me.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation=next;i.state="ready".into();}));
            let response=if method=="turn/start" {json!({"result":{"turn":turn("inProgress")}})}else{json!({"result":{}})};let (result,outbound)=exchange(&host,Some(response.clone()),vec![],||if method=="turn/start" {host.turn_start_text(&g(),"thread","exact text")}else{host.turn_interrupt(&g(),"thread","turn")});assert!(result.unwrap_err().contains("closed/replaced generation"));let snapshot=host.snapshot();assert_eq!(snapshot["generation"],successor);assert!(snapshot["conversationTurns"].as_array().unwrap().iter().all(|t|t["generation"]==g()));assert_eq!(snapshot["clientRequests"][0]["generation"],g());let mut expected=response;expected["id"]=outbound["id"].clone();assert_eq!(host.journal().last().unwrap()["frame"],expected);
        }}
    }

    #[test]
    fn steering_exact_native_body_schema_and_ack_keep_live_target_without_overrides() {
        let host=host();event(&host,"inProgress");let text="Exact steering\n\né / 家\n{\"model\":\"not an override\"}";
        let params=Host::steer_text_params("thread","turn",text).unwrap();assert_eq!(params,json!({"threadId":"thread","expectedTurnId":"turn","input":[{"type":"text","text":text,"text_elements":[]}]}));
        let source:Value=serde_json::from_str(include_str!("../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json")).unwrap();for(target,value)in [("TurnSteerParams",params.clone()),("TurnSteerResponse",json!({"turnId":"turn"}))] {let mut schema=source.clone();schema["$ref"]=json!(format!("#/definitions/v2/{target}"));jsonschema::options().offline().build(&schema).unwrap().validate(&value).unwrap();}
        let before=host.snapshot()["conversationTurns"].clone();let(result,outbound)=exchange(&host,Some(json!({"result":{"turnId":"turn","nativeExtra":"kept"}})),vec![],||host.turn_steer_text(&g(),"thread","turn",text));assert_eq!(outbound["method"],"turn/steer");assert_eq!(outbound["params"],params);assert_eq!(result.unwrap()["result"]["nativeExtra"],"kept");assert_eq!(host.snapshot()["conversationTurns"],before);assert_eq!(host.client_requests()[0]["outcome"],"response-observed-result");assert_eq!(host.snapshot()["threads"][0]["model"],"selected");
        assert!(Host::steer_text_params("thread","",text).is_err());assert!(Host::steer_text_params("thread","turn","").is_err());
    }
    #[test]
    fn steering_stale_expected_terminal_foreign_and_unknown_never_register_or_fallback() {
        let host=host();event(&host,"inProgress");assert_eq!(host.turn_steer_text(&g(),"thread","old","text").unwrap_err(),"expected-live-turn-mismatch");
        for foreign in [json!({"appSession":"other","home":"conversation-home","spawnCounter":1}),json!({"appSession":"conversation-session","home":"other","spawnCounter":1}),json!({"appSession":"conversation-session","home":"conversation-home","spawnCounter":2})] {assert!(host.turn_steer_text(&foreign,"thread","turn","text").is_err());}
        assert!(host.turn_steer_text(&g(),"unknown","turn","text").is_err());event(&host,"completed");event(&host,"inProgress");host.inner.0.lock().unwrap().conversation_turns[0]["nativeTurn"]["status"]=json!("inProgress");assert_eq!(host.turn_steer_text(&g(),"thread","turn","text").unwrap_err(),"current-live-turn-not-established");assert_eq!(host.inner.0.lock().unwrap().send_position,0);assert!(host.client_requests().is_empty());Host::close_generation(&mut host.inner.0.lock().unwrap());assert!(host.turn_steer_text(&g(),"thread","turn","text").is_err());
    }
    #[test]
    fn steering_native_error_reported_mismatch_write_failure_and_wait_preserve_uncertainty() {
        let host=host();event(&host,"inProgress");let error=json!({"code":-32600,"message":"expected turn mismatch","data":{"native":"kept"}});let(result,outbound)=exchange(&host,Some(json!({"error":error})),vec![],||host.turn_steer_text(&g(),"thread","turn","text"));assert!(result.unwrap_err().contains("native error"));assert_eq!(outbound["method"],"turn/steer");assert_eq!(host.journal().last().unwrap()["frame"]["error"],error);
        let(result,_)=exchange(&host,Some(json!({"result":{"turnId":"other"}})),vec![],||host.turn_steer_text(&g(),"thread","turn","text"));assert!(result.unwrap_err().contains("no rebind"));assert_eq!(host.snapshot()["conversationTurns"][0]["turnId"],"turn");assert_eq!(host.client_requests()[1]["outcome"],"response-observed-result");
        install_broken_test_input(&host);assert!(host.turn_steer_text(&g(),"thread","turn","text").unwrap_err().contains("write failed"));assert_eq!(host.client_requests()[2]["writeResult"],"write-failed");assert_eq!(host.client_requests()[2]["outcome"],"unknown-no-response");
        let(result,outbound)=exchange(&host,None,vec![],||host.conversation_operation("turn/steer",&g(),Host::steer_text_params("thread","turn","late").unwrap(),Duration::from_millis(15)));assert!(result.unwrap_err().contains("wait limit"));assert_eq!(host.client_requests()[3]["outcome"],"pending");host.on_line(&serde_json::to_vec(&json!({"id":outbound["id"],"result":{"turnId":"turn"}})).unwrap(),&g());assert_eq!(host.client_requests()[3]["outcome"],"response-observed-result");assert_eq!(host.snapshot()["conversationTurns"][0]["nativeTurn"]["status"],"inProgress");assert!(host.client_requests().iter().all(|r|r["method"]=="turn/steer"));
    }
    #[test]
    fn steering_response_cannot_rebind_changed_target_or_full_generation() {
        for transition in ["target","terminal","session","home","counter"] {
            let host=host();event(&host,"inProgress");let me=Arc::clone(&host);let transition=transition.to_string();*host.before_turn_result.lock().unwrap()=Some(Box::new(move|| {
                if transition=="terminal" {event(&me,"completed");} else if transition=="target" {let mut next=turn("inProgress");next["id"]=json!("next");me.on_line(&serde_json::to_vec(&json!({"method":"turn/started","params":{"threadId":"thread","turn":next}})).unwrap(),&g());} else {let mut i=me.inner.0.lock().unwrap();Host::close_generation(&mut i);let field=match transition.as_str(){"session"=>"appSession","home"=>"home",_=>"spawnCounter"};i.generation[field]=if field=="spawnCounter"{json!(2)}else{json!("other")};i.state="ready".into();}
            }));let(result,outbound)=exchange(&host,Some(json!({"result":{"turnId":"turn"}})),vec![],||host.turn_steer_text(&g(),"thread","turn","exact text"));assert!(result.is_err());assert_eq!(outbound["params"]["expectedTurnId"],"turn");assert_eq!(host.client_requests()[0]["outcome"],"response-observed-result");assert!(host.journal().iter().any(|e|e["frame"]==json!({"id":outbound["id"],"result":{"turnId":"turn"}})));
        }
    }
    #[test]
    fn steering_live_target_uses_native_event_not_delayed_prior_start_response() {
        let host=host();let mut next=turn("inProgress");next["id"]=json!("next");let frame=json!({"method":"turn/started","params":{"threadId":"thread","turn":next}});
        let(result,_)=exchange(&host,Some(json!({"result":{"turn":turn("inProgress")}})),vec![frame],||host.turn_start_text(&g(),"thread","first"));assert!(result.is_ok());assert_eq!(host.turn_steer_text(&g(),"thread","turn","text").unwrap_err(),"expected-live-turn-mismatch");let(result,_)=exchange(&host,Some(json!({"result":{"turnId":"next"}})),vec![],||host.turn_steer_text(&g(),"thread","next","text"));assert!(result.is_ok());
        // A response-only fresh start is usable; a completed event then a new
        // request/response is also a new target, rather than terminal revival.
        event(&host,"completed");let mut fresh=turn("inProgress");fresh["id"]=json!("fresh");let(result,_)=exchange(&host,Some(json!({"result":{"turn":fresh}})),vec![],||host.turn_start_text(&g(),"thread","new"));assert!(result.is_ok());let(result,_)=exchange(&host,Some(json!({"result":{"turnId":"fresh"}})),vec![],||host.turn_steer_text(&g(),"thread","fresh","text"));assert!(result.is_ok());
    }

    fn history_thread(status:&str)->Value {json!({"id":"stored","cliVersion":"0.160.0","createdAt":1,"updatedAt":2,"cwd":"/invented","ephemeral":false,"modelProvider":"configured","preview":"invented","projectId":null,"sessionId":"native-session","source":"appServer","status":{"type":status},"turns":[],"agentRole":"TASK","nativeExtra":{"kept":true}})}
    fn history_resume(status:&str,direct:bool)->Value {let mut native=history_thread(status);native["canAcceptDirectInput"]=json!(direct);json!({"thread":native,"model":"reported","modelProvider":"configured","cwd":"/invented","approvalPolicy":"on-request","approvalsReviewer":"user","sandbox":{"type":"readOnly"},"instructionSources":["/native/instructions"],"nativeExtra":true})}
    fn history_selected()->NativeHistory {let mut view=NativeHistory::new("conversation-home",g()).unwrap();let q=view.list_threads(None,crate::native_history::Direction::Desc).unwrap();view.receive(&q,"conversation-home",&g(),&json!({"data":[history_thread("notLoaded")],"nextCursor":null})).unwrap();view.select("stored").unwrap();view}
    fn history_exchange(host:&Arc<Host>,query:&HistoryQuery,response:Option<Value>)->(HistoryDispatch,Value,Value) {let mut receipt=None;let(result,outbound)=exchange(host,response,vec![],||{let r=host.history_dispatch(query)?;let evidence=host.history_wait(&r,Duration::from_millis(15))?;receipt=Some(r);Ok(evidence)});(receipt.unwrap(),result.unwrap(),outbound)}
    #[test]
    fn history_bridge_actual_rpc_receipt_before_wait_timeout_clone_and_late_correlation() {
        let host=host();host.inner.0.lock().unwrap().next_id=40;let mut view=history_selected();let query=view.read_metadata().unwrap();let(receipt,evidence,outbound)=history_exchange(&host,&query,None);
        assert_ne!(receipt.source().request_id(),&json!(query.id()));assert_eq!(receipt.source().request_id(),&json!(41));assert_eq!(receipt.query(),&query);assert_eq!(evidence["sentFrame"],outbound);assert_eq!(outbound["params"],*query.params());assert_eq!(evidence["writeResult"],"written");assert_eq!(evidence["outcome"],"pending");assert_eq!(evidence["waitingEnded"],true);assert!(evidence["response"].is_null());assert!(!receipt.source().request_ref().is_empty());assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),1);
        let clone=receipt.clone();let response=json!({"id":outbound["id"],"result":{"thread":history_thread("notLoaded")}});host.on_line(&serde_json::to_vec(&response).unwrap(),&g());let late=host.history_dispatch_status(&clone).unwrap();assert_eq!(late["response"],response);assert_eq!(late["outcome"],"response-observed-result");assert_eq!(late["waitingEnded"],true);view.receive(&query,"conversation-home",&g(),&response["result"]).unwrap();assert!(host.history_admit_resume(&view,&clone).is_err());assert_eq!(host.client_requests().len(),1);
    }
    #[test]
    fn history_bridge_continue_actual_receive_admit_once_and_text_control() {
        let host=host();let mut view=history_selected();let query=view.continue_query().unwrap();let native=history_resume("idle",true);let(receipt,evidence,outbound)=history_exchange(&host,&query,Some(json!({"result":native})));assert_eq!(outbound["method"],"thread/resume");assert_eq!(outbound["params"],json!({"threadId":"stored"}));assert!(view.resumed_thread().is_none());assert!(host.history_admit_resume(&view,&receipt).is_err());assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),1);
        view.receive(&query,"conversation-home",&g(),&evidence["response"]["result"]).unwrap();let admitted=host.history_admit_resume(&view,&receipt).unwrap();assert_eq!(admitted["threadId"],"stored");assert_eq!(admitted["generation"],g());assert_eq!(admitted["resumeRequestRef"],receipt.source().request_ref());assert!(host.history_admit_resume(&view,&receipt).is_err());assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),2);
        let(result,outbound)=exchange(&host,Some(json!({"result":{"turn":turn("inProgress")}})),vec![],||host.turn_start_text(&g(),"stored","continued exact text"));assert!(result.is_ok());assert_eq!(outbound["params"]["threadId"],"stored");assert!(outbound["params"].get("developerInstructions").is_none());
    }
    #[test]
    fn history_bridge_failed_write_foreign_latest_revision_and_closed_refuse_admission() {
        let host=host();let mut view=history_selected();let query=view.continue_query().unwrap();install_broken_test_input(&host);let failed=host.history_dispatch(&query).unwrap();let evidence=failed.evidence();assert!(evidence["sentFrame"].is_null());assert_eq!(evidence["writeResult"],"write-failed");assert_eq!(evidence["outcome"],"unknown-no-response");view.receive(&query,"conversation-home",&g(),&history_resume("idle",true)).unwrap();assert!(host.history_admit_resume(&view,&failed).is_err());let other=super::conversation_transport_tests::host();assert!(other.history_dispatch_status(&failed).is_err());
        let query=view.continue_query().unwrap();let(receipt,evidence,_)=history_exchange(&host,&query,Some(json!({"result":history_resume("idle",true)})));view.receive(&query,"conversation-home",&g(),&evidence["response"]["result"]).unwrap();assert!(view.resumed_thread().is_some());let newer=view.read_metadata().unwrap();assert!(host.history_admit_resume(&view,&receipt).is_err());view.receive(&newer,"conversation-home",&g(),&json!({"thread":history_thread("notLoaded")})).unwrap();assert!(host.history_admit_resume(&view,&receipt).is_err());
        let query=view.continue_query().unwrap();let(receipt,evidence,_)=history_exchange(&host,&query,Some(json!({"result":history_resume("idle",true)})));view.receive(&query,"conversation-home",&g(),&evidence["response"]["result"]).unwrap();let count=host.client_requests().len();{let mut i=host.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation["spawnCounter"]=json!(2);i.state="ready".into();}assert!(host.history_admit_resume(&view,&receipt).is_err());assert!(host.history_dispatch(&query).is_err());assert_eq!(host.client_requests().len(),count);assert_eq!(receipt.evidence()["sourceCurrent"],false);assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),1);
    }
    #[test]
    fn history_bridge_notloaded_direct_false_malformed_and_native_error_keep_raw_no_activation() {
        for (status,direct) in [("notLoaded",true),("idle",false)] {let host=host();let mut view=history_selected();let q=view.continue_query().unwrap();let(r,e,_)=history_exchange(&host,&q,Some(json!({"result":history_resume(status,direct)})));view.receive(&q,"conversation-home",&g(),&e["response"]["result"]).unwrap();assert!(host.history_admit_resume(&view,&r).is_err());assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),1);}
        let host=host();let mut view=history_selected();let q=view.continue_query().unwrap();let error=json!({"code":-32600,"message":"resume refused","data":{"kept":"native"}});let(r,e,_)=history_exchange(&host,&q,Some(json!({"error":error})));assert_eq!(e["response"]["error"],error);view.receive_error(&q,"conversation-home",&g(),&error).unwrap();assert!(host.history_admit_resume(&view,&r).is_err());
        let q=view.continue_query().unwrap();let mut wrong=history_resume("idle",true);wrong["thread"]["id"]=json!("foreign-thread");let(r,e,_)=history_exchange(&host,&q,Some(json!({"result":wrong})));assert!(view.receive(&q,"conversation-home",&g(),&e["response"]["result"]).is_err());assert!(host.history_admit_resume(&view,&r).is_err());assert_eq!(host.journal().last().unwrap()["frame"],e["response"]);
    }
    #[test]
    fn history_bridge_genuine_start_receipt_exact_guidance_finish_and_lookup() {
        let host=host();let text="Frozen guidance\n\né / 家";let mut receipt=None;let native=history_resume("idle",true);let(result,outbound)=exchange(&host,Some(json!({"result":native})),vec![],||{let r=host.thread_start_with_guidance_dispatch(&g(),"/invented","selected","configured",text)?;let e=host.source_request_wait(&r,Duration::from_millis(15))?;receipt=Some(r);Ok(e)});let evidence=result.unwrap();let receipt=receipt.unwrap();assert_eq!(outbound["params"],Host::thread_start_params("/invented","selected","configured",Some(text)).unwrap());assert_eq!(evidence["sentFrame"],outbound);assert_eq!(receipt.attempted_frame(),&outbound);assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),1);assert_eq!(host.source_request(&g(),receipt.request_id()).unwrap().request_ref(),receipt.request_ref());assert_eq!(host.source_request_status(&receipt).unwrap()["response"],evidence["response"]);
        assert!(host.thread_start_dispatch_finish(&receipt).is_ok());assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),2);assert!(host.thread_start_dispatch_finish(&receipt).is_err());assert!(host.source_request(&json!({"appSession":"foreign","home":"conversation-home","spawnCounter":1}),receipt.request_id()).is_err());
        let mut bad_receipt=None;let(result,_)=exchange(&host,Some(json!({"result":{"thread":{"id":"malformed"}}})),vec![],||{let r=host.thread_start_with_guidance_dispatch(&g(),"/invented","selected","configured",text)?;let e=host.source_request_wait(&r,Duration::from_millis(15))?;bad_receipt=Some(r);Ok(e)});assert_eq!(result.unwrap()["outcome"],"response-observed-result");assert!(host.thread_start_dispatch_finish(&bad_receipt.unwrap()).is_err());assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),2);
    }

    #[test]
    fn history_bridge_joined_session_consumes_genuine_history_and_frozen_role_start_receipts() {
        use crate::native_history::Direction;
        use crate::role_supply::{Composition,Guidance,Role};
        let host=host();host.inner.0.lock().unwrap().threads.clear();let mut session=crate::runtime_session::HistorySession::default();session.synchronize(&host.snapshot());
        let query=session.prepare(&host.snapshot(),&g(),0,"list",None,Direction::Desc,None).unwrap();let(receipt,_,_)=history_exchange(&host,&query,Some(json!({"result":{"data":[history_thread("notLoaded")],"nextCursor":null}})));session.dispatched(receipt);session.reconcile(&host);assert!(host.snapshot()["threads"].as_array().unwrap().is_empty());session.select(&host.snapshot(),&g(),0,"stored").unwrap();assert_eq!(session.snapshot(None)["selectionEpoch"],1);
        let query=session.prepare(&host.snapshot(),&g(),1,"continue",None,Direction::Desc,None).unwrap();let(receipt,_,outbound)=history_exchange(&host,&query,Some(json!({"result":history_resume("idle",true)})));assert_eq!(outbound["params"],json!({"threadId":"stored"}));assert!(host.snapshot()["threads"].as_array().unwrap().is_empty());session.dispatched(receipt);session.reconcile(&host);assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),1);assert_eq!(session.snapshot(None)["selected"]["resumeEligibilityCurrent"],true);assert_eq!(session.role("conversation-home","stored")["standing"],"unknown");
        let common=Guidance::seeded("AGENTS.md","test-release",b"Frozen common bytes\r\n".to_vec(),b"default common").unwrap();let role=Guidance::seeded("agents/AGENT_TASK.md","test-release",b"Frozen TASK bytes\r\n".to_vec(),b"default role").unwrap();let composition=Composition::new(&common,Some((Role::TASK,&role)),true).unwrap();let original=composition.text.clone();let mut native=history_resume("idle",true);native["thread"]["id"]=json!("role-thread");let mut start=None;
        let(result,outbound)=exchange(&host,Some(json!({"result":native})),vec![],||{let receipt=host.thread_start_with_guidance_dispatch(&g(),"/invented","selected","configured",&composition.text)?;session.start_dispatched(receipt.clone(),&composition,"sup:fixture")?;let evidence=host.source_request_wait(&receipt,Duration::from_millis(15))?;start=Some(receipt);Ok(evidence)});assert_eq!(result.unwrap()["writeResult"],"written");assert_eq!(outbound["params"]["developerInstructions"],original);assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),1);session.reconcile(&host);assert!(session.start_admitted(&start.unwrap()));assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),2);let role=session.role("conversation-home","role-thread");assert_eq!(role["standing"],"app-observed");assert_eq!(role["role"],"TASK");assert!(session.snapshot(None)["receivingLimits"].as_array().unwrap().is_empty());
        // Role preparation is local and occurs after a genuine native send.
        // Its refusal must retain that source outcome without admission/retry.
        let before_threads=host.snapshot()["threads"].clone();let before_requests=host.client_requests().len();let mut refused_native=history_resume("idle",true);refused_native["thread"]["id"]=json!("rejected-role-thread");let mut refused_receipt=None;
        let(result,outbound)=exchange(&host,Some(json!({"result":refused_native})),vec![],|| {
            let receipt=host.thread_start_with_guidance_dispatch(&g(),"/invented","selected","configured",&composition.text)?;
            assert!(session.start_dispatched(receipt.clone(),&composition,"invalid-supply-ref").is_err());
            let retained=session.snapshot(None)["startReceipts"].as_array().unwrap().last().unwrap().clone();assert_eq!(retained["requestIdentity"],*receipt.request_id());assert_eq!(retained["requestRef"],receipt.request_ref());assert_eq!(retained["writeResult"],"written");assert!(matches!(retained["outcome"].as_str(),Some("pending"|"response-observed-result")));assert!(retained["rolePreparationError"].is_string());
            let evidence=host.source_request_wait(&receipt,Duration::from_millis(15))?;refused_receipt=Some(receipt);Ok(evidence)
        });let evidence=result.unwrap();let refused_receipt=refused_receipt.unwrap();assert_eq!(evidence["sentFrame"],outbound);assert_eq!(evidence["outcome"],"response-observed-result");session.reconcile(&host);
        let retained=session.snapshot(None)["startReceipts"].as_array().unwrap().last().unwrap().clone();assert_eq!(retained["requestIdentity"],*refused_receipt.request_id());assert_eq!(retained["requestRef"],refused_receipt.request_ref());assert_eq!(retained["writeResult"],"written");assert_eq!(retained["outcome"],"response-observed-result");assert!(!session.start_admitted(&refused_receipt));assert_eq!(session.role("conversation-home","rejected-role-thread")["standing"],"unknown");assert_eq!(host.snapshot()["threads"],before_threads);assert_eq!(host.client_requests().len(),before_requests+1);assert_eq!(host.source_request_status(&refused_receipt).unwrap()["response"],evidence["response"]);

    }

    #[test]
    fn history_bridge_start_mixed_result_error_envelope_never_admits_and_preserves_raw() {
        for error in [json!({"code":-32600,"message":"native start refused","data":{"native":"retained"}}),Value::Null] {
            let host=host();let mut receipt=None;let native=history_resume("idle",true);let(result,outbound)=exchange(&host,Some(json!({"result":native,"error":error})),vec![],||{let r=host.thread_start_with_guidance_dispatch(&g(),"/invented","selected","configured","frozen bytes")?;let e=host.source_request_wait(&r,Duration::from_millis(15))?;receipt=Some(r);Ok(e)});let evidence=result.unwrap();let receipt=receipt.unwrap();assert_eq!(evidence["writeResult"],"written");assert_eq!(evidence["sentFrame"],outbound);assert_eq!(evidence["outcome"],"response-observed-result");assert_eq!(evidence["response"]["result"],native);assert!(evidence["response"].get("error").is_some());assert_eq!(evidence["response"]["error"],error);
            let before=host.snapshot()["threads"].clone();let refusal=host.thread_start_dispatch_finish(&receipt).unwrap_err();assert!(refusal.contains("envelope is uncorrelated or failed"));assert_eq!(host.snapshot()["threads"],before);assert_eq!(host.journal().last().unwrap()["frame"],evidence["response"]);assert_eq!(host.source_request_status(&receipt).unwrap()["response"],evidence["response"]);
        }
        // An actual foreign RPC frame is retained uncorrelated and never
        // promoted to the private matching receipt while waiting times out.
        let host=host();let mut receipt=None;let wrong=json!({"id":999,"result":history_resume("idle",true)});let(result,_)=exchange(&host,None,vec![wrong.clone()],||{let r=host.thread_start_with_guidance_dispatch(&g(),"/invented","selected","configured","frozen bytes")?;let e=host.source_request_wait(&r,Duration::from_millis(15))?;receipt=Some(r);Ok(e)});let evidence=result.unwrap();assert_eq!(evidence["outcome"],"pending");assert!(evidence["response"].is_null());assert!(host.thread_start_dispatch_finish(&receipt.unwrap()).is_err());assert_eq!(host.journal().last().unwrap()["frame"],wrong);assert_eq!(host.snapshot()["threads"].as_array().unwrap().len(),1);
    }

    fn attachment_fixture()->(std::path::PathBuf,Arc<AttachmentCustody>,Vec<SelectedTextAttachment>){let root=std::env::temp_dir().join(opaque_id("attachment-host-").unwrap());std::fs::create_dir(&root).unwrap();let root=root.canonicalize().unwrap();let owner=Arc::new(AttachmentCustody::open(&root.join("app"),&root.join("codex")).unwrap());let mut selections=vec![];for(name,text)in [("first.txt","Exact first bytes\n家"),("second.txt","Exact second bytes\né")]{let path=root.join(name);std::fs::write(&path,text).unwrap();selections.push(SelectedTextAttachment::from_native_selection(path,None).unwrap());}(root,owner,selections)}
    fn no_attachment_write<F>(host:&Arc<Host>,operation:F) where F:FnOnce(){let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();let mut stdout=child.stdout.take().unwrap();operation();*host.stdin.lock().unwrap()=None;assert!(child.wait().unwrap().success());let mut bytes=vec![];stdout.read_to_end(&mut bytes).unwrap();assert!(bytes.is_empty(),"unexpected actual native bytes: {bytes:?}");}
    fn complete_turn()->Value{let mut value=turn("inProgress");value["error"]=Value::Null;value}
    #[test]
    fn attachment_host_actual_ordered_metadata_barrier_pipe_and_hot_late_cold_resolver(){
        let host=host();let(root,owner,selections)=attachment_fixture();let mut prepared=None;
        let(result,outbound)=exchange(&host,None,vec![],||{let packet=host.prepare_attachment_turn(Arc::clone(&owner),&g(),"thread",None,"Person exact text",&selections)?;let cold=owner.resolve_cold(packet.submission_ref());assert_eq!(cold["clientMetadata"]["outcome"],"prepared-not-sent");assert!(cold["clientMetadata"].get("sendPosition").is_none());assert_eq!(cold["supplyRecords"],json!(packet.supply_records()));let source=host.dispatch_attachment_turn(&packet)?;let e=host.attachment_wait(&source,Duration::from_millis(15))?;prepared=Some(packet);Ok(e)});let evidence=result.unwrap();let prepared=prepared.unwrap();assert_eq!(outbound["method"],"turn/start");assert_eq!(outbound["params"]["input"][0]["text"],"Person exact text");assert_eq!(outbound["params"]["input"].as_array().unwrap().len(),3);for(index,record)in prepared.supply_records().iter().enumerate(){assert_eq!(sha256_hex(outbound["params"]["input"][index+1]["text"].as_str().unwrap().as_bytes()),record["elementIdentity"]["value"]);}
        assert_eq!(evidence["outcome"],"pending");assert!(host.dispatch_attachment_turn(&prepared).is_err());let token=prepared.submission_ref();assert!(owner.resolve_cold(token)["nativeTurnRef"].is_null());let response=json!({"id":outbound["id"],"result":{"turn":complete_turn()}});host.on_line(&serde_json::to_vec(&response).unwrap(),&g());let hot=host.resolve_attachment_submission(&owner,token);assert_eq!(hot["nativeTurnRef"]["turnId"],"turn");assert_eq!(hot["nativeTurnRef"]["threadId"],"thread");assert_eq!(hot["nativeTurnRef"]["generation"],g());let cold_owner=Arc::new(AttachmentCustody::open(&root.join("app"),&root.join("codex")).unwrap());assert!(host.resolve_attachment_submission(&cold_owner,token)["nativeTurnRef"].is_null());assert_eq!(owner.resolve_cold(token)["clientMetadata"]["submissionAssociation"]["supplyRefs"],json!(prepared.list.supply_refs()));
        let bytes=std::fs::read_to_string(owner.client_path(&g(),prepared.source().request_id()).unwrap()).unwrap();assert!(!bytes.contains("Person exact text"));assert!(!bytes.contains("Exact first bytes"));assert!(!bytes.contains("nativeTurn"));
        let mut second=None;let(result,_)=exchange(&host,Some(json!({"result":{"turn":complete_turn()}})),vec![],||{let packet=host.prepare_attachment_turn(Arc::clone(&owner),&g(),"thread",None,"Explicit new send",&selections)?;let source=host.dispatch_attachment_turn(&packet)?;let evidence=host.attachment_wait(&source,Duration::from_millis(15))?;second=Some(packet);Ok(evidence)});assert_eq!(result.unwrap()["outcome"],"response-observed-result");let second=second.unwrap();assert_ne!(second.submission_ref(),prepared.submission_ref());assert_ne!(second.source().request_id(),prepared.source().request_id());assert_ne!(second.list.supply_refs(),prepared.list.supply_refs());assert_eq!(host.resolve_attachment_submission(&owner,second.submission_ref())["nativeTurnRef"]["turnId"],"turn");assert_eq!(host.resolve_attachment_submission(&owner,prepared.submission_ref())["nativeTurnRef"]["turnId"],"turn");assert_eq!(owner.resolve_cold(prepared.submission_ref())["clientMetadata"]["submissionAssociation"]["supplyRefs"],json!(prepared.list.supply_refs()));std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn attachment_host_cancel_source_generation_pipe_target_and_metadata_drift_send_no_bytes(){
        for change in ["cancel","file","session","home","counter","pipe","target","metadata"]{let host=host();let(root,owner,selections)=attachment_fixture();event(&host,"inProgress");let mut replacement=None;no_attachment_write(&host,||{let packet=host.prepare_attachment_turn(Arc::clone(&owner),&g(),"thread",Some("turn"),"Person text",&selections).unwrap();match change{"cancel"=>{assert!(packet.cancel());},"file"=>std::fs::write(root.join("first.txt"),"changed").unwrap(),"session"|"home"|"counter"=>{let mut i=host.inner.0.lock().unwrap();let field=match change{"session"=>"appSession","home"=>"home",_=>"spawnCounter"};i.generation[field]=if field=="spawnCounter"{json!(2)}else{json!("other")};},"pipe"=>{let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();host.inner.0.lock().unwrap().attachment_pipe_epoch+=1;replacement=Some(child);},"target"=>event(&host,"completed"),_=>{let mut records=packet.supply_records();records[0]["displayName"]=json!("changed metadata");std::fs::write(owner.supplies_path(packet.submission_ref()).unwrap(),serde_json::to_vec(&records).unwrap()).unwrap();}}
            assert!(host.dispatch_attachment_turn(&packet).is_err());assert_eq!(host.inner.0.lock().unwrap().send_position,0);assert_eq!(packet.source().evidence()["lastClientObservation"]["writeResult"],"not-attempted");assert_eq!(packet.source().evidence()["writeAttemptInProgress"],false);assert!(packet.source().evidence()["sentFrame"].is_null());assert!(host.dispatch_attachment_turn(&packet).is_err());});if let Some(mut child)=replacement{assert!(child.wait().unwrap().success());let mut bytes=vec![];child.stdout.take().unwrap().read_to_end(&mut bytes).unwrap();assert!(bytes.is_empty());}std::fs::remove_dir_all(root).unwrap();}
    }
    #[test]
    fn attachment_host_actual_partial_and_sync_publication_failures_never_send(){
        for failure in ["array","client","sync"]{let host=host();let(root,owner,selections)=attachment_fixture();match failure{"array"=>{std::fs::write(owner.root().join("runtime/nir"),"obstruction").unwrap();},"client"=>{std::fs::create_dir_all(owner.root().join("runtime/hosting")).unwrap();std::fs::write(owner.root().join("runtime/hosting/client-requests"),"obstruction").unwrap();},_=>{crate::storage::ensure_directory(&owner.root().join("runtime/nir/attachment-supplies")).unwrap();crate::storage::fail_directory_for_test(Some(owner.root().join("runtime/nir/attachment-supplies")));}}
            no_attachment_write(&host,||{assert!(host.prepare_attachment_turn(Arc::clone(&owner),&g(),"thread",None,"text",&selections).is_err());assert_eq!(host.inner.0.lock().unwrap().send_position,0);assert_eq!(host.client_requests()[0]["requestIdentity"],1);assert_eq!(host.client_requests()[0]["outcome"],"prepared-not-sent");});crate::storage::fail_directory_for_test(None);assert_eq!(host.inner.0.lock().unwrap().next_id,1);std::fs::remove_dir_all(root).unwrap();}
    }
    #[test]
    fn attachment_host_steer_exact_expected_target_error_redaction_malformed_and_repeat(){
        for response in [json!({"result":{"turnId":"turn"}}),json!({"result":{"turnId":"wrong"}}),json!({"error":{"code":-32600,"message":"secret payload","data":{"secret":"hidden"}}}),json!({"error":{"message":"missing real code"}}),json!({"result":null})]{let host=host();event(&host,"inProgress");let(root,owner,selections)=attachment_fixture();let mut packet=None;let(result,outbound)=exchange(&host,Some(response.clone()),vec![],||{let p=host.prepare_attachment_turn(Arc::clone(&owner),&g(),"thread",Some("turn"),"steer bytes",&selections)?;let source=host.dispatch_attachment_turn(&p)?;let e=host.attachment_wait(&source,Duration::from_millis(15))?;packet=Some(p);Ok(e)});let e=result.unwrap();let packet=packet.unwrap();assert_eq!(outbound["method"],"turn/steer");assert_eq!(outbound["params"]["expectedTurnId"],"turn");assert!(outbound["params"].get("submissionAssociation").is_none());let view=host.resolve_attachment_submission(&owner,packet.submission_ref());if response==json!({"result":{"turnId":"turn"}}){assert_eq!(view["nativeTurnRef"]["turnId"],"turn");}else{assert!(view["nativeTurnRef"].is_null());}
            let before=e["response"].clone();host.on_line(&serde_json::to_vec(&json!({"id":outbound["id"],"result":{"turnId":"conflicting-repeat"}})).unwrap(),&g());assert_eq!(packet.source().evidence()["response"],before);assert_eq!(host.journal().last().unwrap()["class"],"uncorrelated-response");let bytes=std::fs::read_to_string(owner.client_path(&g(),packet.source().request_id()).unwrap()).unwrap();assert!(!bytes.contains("secret payload"));assert!(!bytes.contains("hidden"));if response["error"].get("code").is_some(){assert!(bytes.contains("native error text withheld"));}if response["error"].get("message")==Some(&json!("missing real code")){let record:Value=serde_json::from_str(&bytes).unwrap();assert_eq!(record["outcome"],"unknown-no-response");assert!(record.get("error").is_none());}std::fs::remove_dir_all(root).unwrap();}
    }
    #[test]
    fn attachment_host_real_broken_pipe_and_later_metadata_failure_keep_source_uncertainty(){
        let host=host();let(root,owner,selections)=attachment_fixture();let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::null()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();let packet=host.prepare_attachment_turn(Arc::clone(&owner),&g(),"thread",None,"text",&selections).unwrap();child.kill().unwrap();child.wait().unwrap();let source=host.dispatch_attachment_turn(&packet).unwrap();assert_eq!(source.evidence()["writeResult"],"write-failed");assert_eq!(source.evidence()["outcome"],"unknown-no-response");assert!(host.resolve_attachment_submission(&owner,packet.submission_ref())["nativeTurnRef"].is_null());*host.stdin.lock().unwrap()=None;std::fs::remove_dir_all(root).unwrap();
        let host=super::conversation_transport_tests::host();let(root,owner,selections)=attachment_fixture();let mut packet=None;let(result,_)=exchange(&host,Some(json!({"result":{"turn":complete_turn()}})),vec![],||{let p=host.prepare_attachment_turn(Arc::clone(&owner),&g(),"thread",None,"text",&selections)?;let source=host.dispatch_attachment_turn(&p)?;let e=host.attachment_wait(&source,Duration::from_millis(15))?;packet=Some(p);Ok(e)});let e=result.unwrap();let packet=packet.unwrap();let path=owner.client_path(&g(),packet.source().request_id()).unwrap();std::fs::remove_file(&path).unwrap();std::fs::create_dir(&path).unwrap();assert!(host.persist_attachment_observation(packet.source()).is_err());assert_eq!(packet.source().evidence()["response"],e["response"]);let view=host.resolve_attachment_submission(&owner,packet.submission_ref());assert!(view["nativeTurnRef"].is_null());assert!(!view["limits"].as_array().unwrap().is_empty());assert!(host.dispatch_attachment_turn(&packet).is_err());std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn attachment_host_queued_old_eof_never_closes_actual_successor_request_or_turn() {
        for field in ["appSession","home","spawnCounter"] {
            let host=host();let gate=host.attachment_gate.lock().unwrap();let(tx,rx)=channel();let(proceed,continue_eof)=channel();*host.before_eof_gate.lock().unwrap()=Some(Box::new(move||{tx.send(()).unwrap();continue_eof.recv_timeout(Duration::from_secs(2)).unwrap();}));let observer=Arc::clone(&host);let worker=std::thread::spawn(move||observer.on_eof(&g()));rx.recv_timeout(Duration::from_secs(1)).unwrap();
            let mut successor=g();successor[field]=if field=="spawnCounter"{json!(2)}else{json!("successor")};{let mut i=host.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation=successor.clone();i.state="ready".into();i.threads.push(json!({"generation":successor,"threadId":"successor-thread"}));}
            let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::null()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();drop(gate);let source=host.thread_start_with_guidance_dispatch(&successor,"/invented","selected","configured","exact successor").unwrap();host.on_line(&serde_json::to_vec(&json!({"method":"turn/started","params":{"threadId":"successor-thread","turn":complete_turn()}})).unwrap(),&successor);let before=host.snapshot();proceed.send(()).unwrap();worker.join().unwrap();let after=host.snapshot();assert_eq!(after["generation"],successor);assert_eq!(after["state"],"ready");assert_eq!(after["clientRequests"],before["clientRequests"]);assert_eq!(source.evidence()["outcome"],"pending");assert_eq!(after["conversationTurns"],before["conversationTurns"]);assert!(!host.inner.0.lock().unwrap().server_requests.is_closed(&successor));assert_eq!(after["journal"].as_array().unwrap().last().unwrap()["generation"],g());assert_eq!(after["journal"].as_array().unwrap().last().unwrap()["class"],"superseded-generation-eof");*host.stdin.lock().unwrap()=None;assert!(child.wait().unwrap().success());
        }
    }

    #[test]
    #[ignore = "owned subprocess probe; parent watchdog invokes exact case"]
    fn attachment_host_nonreader_probe() {
        let log=std::path::PathBuf::from(std::env::var_os("CHIRALITY_NONREADER_LOG").unwrap());let host=host();let(root,owner,selections)=attachment_fixture();let mut child=Command::new("/bin/sleep").arg("60").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).process_group(0).spawn().unwrap();let pid=child.id() as i32;std::fs::write(log.join("owned-pid"),pid.to_string()).unwrap();*host.stdin.lock().unwrap()=child.stdin.take();let stdout=child.stdout.take().unwrap();*host.child.lock().unwrap()=Some(child);host.inner.0.lock().unwrap().child_pid=Some(pid);host.spawn_reader(stdout,g());
        let packet=Arc::new(host.prepare_attachment_turn(Arc::clone(&owner),&g(),"thread",None,&"x".repeat(4*1024*1024),&selections).unwrap());let sender=Arc::clone(&host);let prepared=Arc::clone(&packet);let(tx,rx)=channel();let writer=std::thread::spawn(move||assert!(tx.send(sender.dispatch_attachment_turn(&prepared)).is_ok()));
        let deadline=std::time::Instant::now()+Duration::from_secs(2);while host.inner.0.lock().unwrap().send_position==0&&std::time::Instant::now()<deadline{std::thread::sleep(Duration::from_millis(5));}assert_eq!(host.inner.0.lock().unwrap().send_position,1);assert!(matches!(rx.recv_timeout(Duration::from_millis(200)),Err(std::sync::mpsc::RecvTimeoutError::Timeout)));
        let reply_mode=std::env::var("CHIRALITY_NONREADER_MODE").is_ok_and(|m|m=="reply");let known_reply=json!({"id":packet.source().request_id(),"result":{"turn":complete_turn()}});if reply_mode{host.on_line(&serde_json::to_vec(&known_reply).unwrap(),&g());}
        let evidence=packet.source().evidence();let mid=host.snapshot();let resolution=host.resolve_attachment_submission(&owner,packet.submission_ref());std::fs::write(log.join("midwrite.json"),serde_json::to_vec(&json!({"clientObservation":mid["clientRequests"].as_array().unwrap().last(),"sourceWriteResult":evidence["writeResult"],"sourceAttemptInProgress":evidence.get("writeAttemptInProgress"),"resolver":resolution,"sentFramePresent":!evidence["sentFrame"].is_null(),"stopCalled":true})).unwrap()).unwrap();let started=std::time::Instant::now();let stopped=host.stop("person:fixture","codex-stop").unwrap();assert!(started.elapsed()<Duration::from_secs(5));let source=rx.recv_timeout(Duration::from_secs(1)).unwrap().unwrap();writer.join().unwrap();assert_eq!(source.evidence()["writeResult"],"write-failed");if reply_mode{let e=source.evidence();assert_eq!(e["response"],known_reply);assert_eq!(e["canonicalProjectionAvailable"],false);assert!(e["outcome"].as_str().unwrap().contains("both observed"));let view=host.resolve_attachment_submission(&owner,packet.submission_ref());assert_eq!(view["nativeReplyObserved"],true);assert!(view["dispatch"].as_str().unwrap().contains("reply and failed write"));assert!(view["nativeTurnRef"].is_null());}else{assert_eq!(source.evidence()["outcome"],"unknown-no-response");}assert_ne!(mid["clientRequests"].as_array().unwrap().last().unwrap()["writeResult"],"written");assert_eq!(evidence["writeAttemptInProgress"],true);assert_eq!(resolution["writeAttemptInProgress"],true);assert!(resolution["dispatch"].as_str().unwrap().contains("unknown/in-progress"));assert!(resolution["nativeTurnRef"].is_null());assert!(!evidence["sentFrame"].is_object());assert_eq!(stopped["state"],"stopped");std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn attachment_host_nonreader_stop_and_midwrite_status_actual_bounded_watchdog() {
        for mode in ["plain","reply"] {
        let root=std::env::temp_dir().join(opaque_id("nonreader-watchdog-").unwrap());std::fs::create_dir(&root).unwrap();let root=root.canonicalize().unwrap();let stdout=std::fs::File::create(root.join("worker-output")).unwrap();let mut child=Command::new(std::env::current_exe().unwrap()).args(["--ignored","--exact","hosting::conversation_transport_tests::attachment_host_nonreader_probe","--nocapture"]).env_clear().env("CHIRALITY_NONREADER_LOG",&root).env("CHIRALITY_NONREADER_MODE",mode).stdin(Stdio::null()).stdout(Stdio::from(stdout)).stderr(Stdio::null()).process_group(0).spawn().unwrap();let deadline=std::time::Instant::now()+Duration::from_secs(7);let status=loop{if let Some(status)=child.try_wait().unwrap(){break Some(status);}if std::time::Instant::now()>=deadline{break None;}std::thread::sleep(Duration::from_millis(20));};
        if !status.as_ref().is_some_and(|s|s.success()){if let Ok(pid)=std::fs::read_to_string(root.join("owned-pid")).and_then(|s|s.parse::<i32>().map_err(|_|std::io::Error::other("bad fixture pid"))){unsafe{libc::killpg(pid,libc::SIGKILL);}}unsafe{libc::killpg(child.id() as i32,libc::SIGKILL);}let _=child.wait();}
        let observation=std::fs::read_to_string(root.join("midwrite.json")).unwrap_or_else(|e|format!("probe observation unavailable: {e}"));let output=std::fs::read_to_string(root.join("worker-output")).unwrap();std::fs::remove_dir_all(&root).unwrap();assert!(status.as_ref().is_some_and(|s|s.success()),"owned nonreader Stop/write watchdog failure: status={status:?}; observation={observation}; worker={output}");
        }
    }

    #[test]
    fn attachment_host_complete_large_client_manual_and_automatic_reply_frames_serialize() {
        let host=host();host.on_line(&serde_json::to_vec(&json!({"id":"manual","method":"item/tool/requestUserInput","params":{"threadId":"thread","turnId":"turn","itemId":"item","questions":[]}})).unwrap(),&g());
        let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();let stdout=child.stdout.take().unwrap();let observer=Arc::clone(&host);let reader=std::thread::spawn(move||{let mut input=BufReader::new(stdout);let mut frames=vec![];for _ in 0..3{let mut line=String::new();input.read_line(&mut line).unwrap();let frame:Value=serde_json::from_str(&line).unwrap();if frame["method"]=="turn/start"{observer.on_line(&serde_json::to_vec(&json!({"id":frame["id"],"result":{"turn":complete_turn()}})).unwrap(),&g());}frames.push(frame);}frames});
        let one=Arc::clone(&host);let client=std::thread::spawn(move||one.turn_start_text(&g(),"thread",&"c".repeat(1024*1024)));let two=Arc::clone(&host);let manual=std::thread::spawn(move||two.error_server_request(&g(),&json!("manual"),&json!({"code":-32000,"message":"m".repeat(512*1024)}),"app-rule:frame-integrity"));let three=Arc::clone(&host);let automatic=std::thread::spawn(move||three.on_line(&serde_json::to_vec(&json!({"id":"automatic","method":"unknown/frame-probe","params":{"threadId":"thread"}})).unwrap(),&g()));assert!(client.join().unwrap().is_ok());assert!(manual.join().unwrap().is_ok());automatic.join().unwrap();let frames=reader.join().unwrap();assert_eq!(frames.len(),3);assert_eq!(frames.iter().find(|f|f["method"]=="turn/start").unwrap()["params"]["input"][0]["text"],"c".repeat(1024*1024));assert_eq!(frames.iter().find(|f|f["id"]=="manual").unwrap()["error"]["message"],"m".repeat(512*1024));assert_eq!(frames.iter().find(|f|f["id"]=="automatic").unwrap()["error"]["code"],-32601);*host.stdin.lock().unwrap()=None;assert!(child.wait().unwrap().success());
    }
    #[test]
    fn attachment_host_queued_reply_closed_source_or_native_resolution_never_writes() {
        for change in ["generation","resolution"] {let host=host();host.on_line(&serde_json::to_vec(&json!({"id":"manual","method":"item/tool/requestUserInput","params":{"threadId":"thread","turnId":"turn","itemId":"item","questions":[]}})).unwrap(),&g());no_attachment_write(&host,||{let serial=host.frame_write.lock().unwrap();let caller=Arc::clone(&host);let writer=std::thread::spawn(move||caller.error_server_request(&g(),&json!("manual"),&json!({"code":-32000,"message":"queued"}),"app-rule:queued-error"));let deadline=std::time::Instant::now()+Duration::from_secs(1);while host.inner.0.lock().unwrap().server_requests.entries()[0]["state"]!="settling"&&std::time::Instant::now()<deadline{std::thread::sleep(Duration::from_millis(5));}assert_eq!(host.inner.0.lock().unwrap().server_requests.entries()[0]["state"],"settling");if change=="generation"{let mut i=host.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation["spawnCounter"]=json!(2);i.state="ready".into();}else{host.on_line(&serde_json::to_vec(&json!({"method":"serverRequest/resolved","params":{"threadId":"thread","requestId":"manual"}})).unwrap(),&g());}drop(serial);assert!(writer.join().unwrap().is_err());assert_ne!(host.inner.0.lock().unwrap().server_requests.entries()[0]["replyWriteResult"],"written");});}
    }
    #[test]
    fn attachment_host_stop_target_repeated_and_old_exit_facts_do_not_rebind() {
        let host=host();{let mut i=host.inner.0.lock().unwrap();i.journal.push(json!({"generation":{"appSession":"old","home":"old","spawnCounter":99},"class":"exit","exitFacts":{"exitCode":77,"signal":"wrong-old"}}));}let caller=Arc::clone(&host);let(tx,rx)=channel();let worker=std::thread::spawn(move||assert!(tx.send(caller.stop("person:first","codex-stop")).is_ok()));let deadline=std::time::Instant::now()+Duration::from_secs(1);while host.state()!="stopping"&&std::time::Instant::now()<deadline{std::thread::sleep(Duration::from_millis(5));}assert_eq!(host.state(),"stopping");assert!(host.stop("person:second","codex-stop").unwrap_err().contains("already requested"));{let mut i=host.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation["spawnCounter"]=json!(2);i.state="ready".into();host.inner.1.notify_all();}assert!(rx.recv_timeout(Duration::from_secs(1)).unwrap().is_err());worker.join().unwrap();assert_eq!(host.state(),"ready");assert_eq!(host.snapshot()["generation"]["spawnCounter"],2);assert_eq!(host.journal().last().unwrap()["class"],"superseded-generation-stop");
        let host=super::conversation_transport_tests::host();{let mut i=host.inner.0.lock().unwrap();i.journal.push(json!({"generation":{"appSession":"old","home":"old","spawnCounter":99},"class":"exit","exitFacts":{"exitCode":77,"signal":"wrong-old"}}));}let snapshot=host.stop("person:first","codex-stop").unwrap();assert_eq!(snapshot["state"],"stopped");let event=host.lifecycle_events().into_iter().find(|e|e["transitionId"]=="LT-23").unwrap();assert_eq!(event["generation"],g());assert_ne!(event["exitFacts"]["exitCode"],77);assert_ne!(event["exitFacts"]["signal"],"wrong-old");
    }

    #[test]
    fn attachment_host_queued_generic_noattempt_retains_real_source_without_failed_projection() {
        for reply_before_close in [false,true] {
            let host=host();no_attachment_write(&host,||{let serial=host.frame_write.lock().unwrap();let caller=Arc::clone(&host);let writer=std::thread::spawn(move||caller.request_begin_scoped("thread/read",json!({"threadId":"thread","includeTurns":false}),json!({"kind":"person-directed"}),false,Some(&g())));
                let deadline=std::time::Instant::now()+Duration::from_secs(1);while host.inner.0.lock().unwrap().source_requests.is_empty()&&std::time::Instant::now()<deadline{std::thread::sleep(Duration::from_millis(5));}let source=host.source_request(&g(),&json!(1)).unwrap();let reference=source.request_ref().to_owned();assert_eq!(source.evidence()["actualWriteAttemptObserved"],false);assert!(host.client_requests().is_empty());let raw=json!({"id":1,"result":{"raw":"retained-before-noattempt"}});if reply_before_close{host.on_line(&serde_json::to_vec(&raw).unwrap(),&g());}
                {let mut i=host.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation["spawnCounter"]=json!(2);i.state="ready".into();}drop(serial);let returned=writer.join().unwrap().unwrap();assert_eq!(returned.request_ref(),reference);let evidence=returned.evidence();assert_eq!(evidence["actualWriteAttemptObserved"],false);assert_eq!(evidence["writeAttemptInProgress"],false);assert_ne!(evidence["writeResult"],"write-failed");assert_eq!(evidence["canonicalProjectionAvailable"],false);assert!(evidence["noAttemptCause"].as_str().unwrap().contains("No actual write attempt"));assert!(evidence["sentFrame"].is_null());assert!(host.client_requests().is_empty());assert!(host.inner.0.lock().unwrap().pending.is_empty());assert!(host.inner.0.lock().unwrap().turn_request_threads.is_empty());assert_eq!(host.inner.0.lock().unwrap().send_position,0);if reply_before_close{assert_eq!(evidence["response"],raw);}assert!(host.wait_source_response(&returned,Duration::from_millis(10)).unwrap_err().contains("before actual attempt"));});
        }
    }

    #[test]
    fn attachment_host_private_wait_fact_visible_before_canonical_completion_and_close() {
        for close_first in [false,true] {
            let host=host();let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();let mut stdout=child.stdout.take().unwrap();let serial=host.frame_write.lock().unwrap();let caller=Arc::clone(&host);let writer=std::thread::spawn(move||caller.request_begin_scoped("thread/read",json!({"threadId":"thread","includeTurns":false}),json!({"kind":"person-directed"}),false,Some(&g())));
            let deadline=std::time::Instant::now()+Duration::from_secs(1);while host.inner.0.lock().unwrap().source_requests.is_empty()&&std::time::Instant::now()<deadline{std::thread::sleep(Duration::from_millis(5));}let source=host.source_request(&g(),&json!(1)).unwrap();let reference=source.request_ref().to_owned();let waited=host.source_request_wait(&source,Duration::from_millis(10)).unwrap();assert_eq!(waited["waitingEnded"],true);assert_eq!(waited["actualWriteAttemptObserved"],false);assert_eq!(waited["canonicalProjectionAvailable"],false);assert_eq!(host.snapshot()["reservedNativeRequests"][0]["waitingEnded"],true);assert!(host.client_requests().is_empty());
            if close_first{let mut i=host.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation["spawnCounter"]=json!(2);i.state="ready".into();}drop(serial);let returned=writer.join().unwrap().unwrap();assert_eq!(returned.request_ref(),reference);assert_eq!(returned.evidence()["waitingEnded"],true);*host.stdin.lock().unwrap()=None;assert!(child.wait().unwrap().success());let mut bytes=vec![];stdout.read_to_end(&mut bytes).unwrap();if close_first{assert!(bytes.is_empty());assert!(host.client_requests().is_empty());assert_eq!(returned.evidence()["actualWriteAttemptObserved"],false);}else{let frame:Value=serde_json::from_slice(&bytes).unwrap();assert_eq!(frame["id"],1);assert_eq!(frame["method"],"thread/read");assert_eq!(host.client_requests()[0]["waitingEnded"],true);assert_eq!(returned.evidence()["outcome"],"pending");let raw=json!({"id":1,"result":{"thread":"raw late evidence"}});host.on_line(&serde_json::to_vec(&raw).unwrap(),&g());assert_eq!(returned.evidence()["waitingEnded"],true);assert_eq!(returned.evidence()["response"],raw);}
        }
    }

    fn context_fixture()->(Arc<Host>,Value,std::path::PathBuf,Arc<AttachmentCustody>,Vec<SelectedTextAttachment>){let(root,owner,selections)=attachment_fixture();let host=Arc::new(Host::new());host.configure_recovery(owner.root().join("runtime/recovery.ledger.jsonl")).unwrap();let generation={let mut i=host.inner.0.lock().unwrap();let generation=json!({"appSession":i.app_session,"home":"opaque-native-home","spawnCounter":1});i.generation=generation.clone();i.state="ready".into();i.threads.push(json!({"generation":generation,"threadId":"thread","cwd":"/different/native/Q","projectId":"native-project-not-app"}));generation};(host,generation,root,owner,selections)}
    fn context_packet(host:&Arc<Host>,owner:&Arc<AttachmentCustody>,generation:&Value,selections:&[SelectedTextAttachment])->PreparedAttachmentDispatch{let mut packet=None;no_attachment_write(host,||{packet=Some(host.prepare_attachment_turn(Arc::clone(owner),generation,"thread",None,"ordinary input without WR prefix",selections).unwrap());});packet.unwrap()}
    #[test]
    fn explicit_context_host_actual_index_p_tag_q_absence_and_idempotence_preserve_source(){
        use crate::recovery::{ExplicitAppProjectContext as Context,AppProjectSource};let(host,g,root,owner,selections)=context_fixture();let p=Context::known("explicit App P",AppProjectSource::ConfiguredDirectory).unwrap();let q=Context::known("explicit App Q / 家",AppProjectSource::OpenedDirectory).unwrap();let admission=host.observe_conversation_project(&g,"thread",Some("H-acct"),&p).unwrap();assert_eq!(admission["indexSnapshot"]["project"],"explicit App P");assert_eq!(host.observe_conversation_project(&g,"thread",Some("H-acct"),&q).unwrap()["indexSnapshot"]["project"],"explicit App P");let packet=context_packet(&host,&owner,&g,&selections);let bound=host.bind_attachment_context(&packet,&q,Some("H-acct")).unwrap();assert_eq!(bound["historicalProject"],"explicit App P");assert_eq!(bound["currentSubmissionProject"],"explicit App Q / 家");assert_eq!(bound["relation"],"different; no transfer");assert_eq!(bound["persistence"],"durable App metadata");let value=crate::recovery::encode_submission_context(packet.submission_ref(),q.reference()).unwrap();assert_eq!(bound["tag"]["value"],value);let count=host.snapshot()["recovery"]["entries"].as_array().unwrap().len();assert_eq!(host.bind_attachment_context(&packet,&q,Some("H-acct")).unwrap()["idempotent"],true);assert_eq!(host.snapshot()["recovery"]["entries"].as_array().unwrap().len(),count);assert!(host.bind_attachment_context(&packet,&p,Some("H-acct")).is_err());let second=context_packet(&host,&owner,&g,&selections);let none=host.bind_attachment_context(&second,&Context::unknown(),Some("H-acct")).unwrap();assert_eq!(none["historicalProject"],"explicit App P");assert!(none["currentSubmissionProject"].is_null());assert_eq!(none["relation"],"unbound");let ledger=RecoveryLedger::open(owner.root().join("runtime/recovery.ledger.jsonl")).unwrap().snapshot();let indexes:Vec<_>=ledger["entries"].as_array().unwrap().iter().filter(|e|e["kind"]=="conversation_index").collect();assert!(indexes.iter().all(|e|e["project"]=="explicit App P"));assert_eq!(indexes.last().unwrap()["tags"].as_array().unwrap().len(),2);assert!(packet.source().attempted_frame()["params"].get("cwd").is_none());assert!(packet.source().attempted_frame()["params"].get("project").is_none());std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn explicit_context_host_no_index_or_home_and_real_append_failure_keep_hot_conflicts(){
        use crate::recovery::{ExplicitAppProjectContext as Context,AppProjectSource};let(host,g,root,owner,selections)=context_fixture();let q=Context::known("Q",AppProjectSource::ConfiguredDirectory).unwrap();let r=Context::known("R",AppProjectSource::OpenedDirectory).unwrap();let packet=context_packet(&host,&owner,&g,&selections);let hot=host.bind_attachment_context(&packet,&q,None).unwrap();assert!(hot["indexSnapshot"].is_null());assert_eq!(hot["persistence"],"memory-only");assert!(hot["limit"].as_str().unwrap().contains("cold lookup unavailable"));assert!(host.bind_attachment_context(&packet,&r,Some("H-acct")).is_err());assert!(host.snapshot()["recovery"]["entries"].as_array().unwrap().iter().all(|e|e["kind"]!="conversation_index"));
        let p=Context::known("P",AppProjectSource::ConfiguredDirectory).unwrap();host.observe_conversation_project(&g,"thread",Some("H-acct"),&p).unwrap();let second=context_packet(&host,&owner,&g,&selections);use std::io::Write;let path=owner.root().join("runtime/recovery.ledger.jsonl");std::fs::OpenOptions::new().append(true).open(&path).unwrap().write_all(b"{torn").unwrap();let failed=host.bind_attachment_context(&second,&q,Some("H-acct")).unwrap();assert_eq!(failed["historicalProject"],"P");assert_eq!(failed["persistence"],"memory-only");assert!(failed["limit"].as_str().unwrap().contains("append unavailable"));assert!(host.bind_attachment_context(&second,&r,Some("H-acct")).is_err());let same=host.bind_attachment_context(&second,&q,Some("H-acct")).unwrap();assert_eq!(same["idempotent"],true);assert_eq!(same["persistence"],"memory-only");assert!(same["limit"].as_str().unwrap().contains("cold lookup unavailable"));assert!(std::fs::read(&path).unwrap().ends_with(b"{torn"));std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn explicit_context_paused_ledger_preserves_summary_order_and_allows_actual_stop(){
        use crate::recovery::{ExplicitAppProjectContext as Context,AppProjectSource};let(host,g,root,owner,selections)=context_fixture();let packet=Arc::new(context_packet(&host,&owner,&g,&selections));let ledger=host.inner.0.lock().unwrap().recovery.clone().unwrap();let paused=ledger.lock().unwrap();let caller=Arc::clone(&host);let prepared=Arc::clone(&packet);let writer=std::thread::spawn(move||caller.bind_attachment_context(&prepared,&Context::known("Q",AppProjectSource::ConfiguredDirectory).unwrap(),Some("H-acct")));let deadline=std::time::Instant::now()+Duration::from_secs(1);while host.recovery_writer.try_lock().is_ok()&&std::time::Instant::now()<deadline{std::thread::sleep(Duration::from_millis(5));}assert!(host.recovery_writer.try_lock().is_err());
        host.on_line(&serde_json::to_vec(&json!({"id":"request","method":"item/tool/requestUserInput","params":{"threadId":"thread","turnId":"turn","itemId":"item","questions":[]}})).unwrap(),&g);assert!(!host.snapshot()["recoveryPendingObservations"].as_array().unwrap().is_empty());let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).process_group(0).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();let stdout=child.stdout.take().unwrap();let pid=child.id() as i32;*host.child.lock().unwrap()=Some(child);host.inner.0.lock().unwrap().child_pid=Some(pid);host.spawn_reader(stdout,g.clone());let started=std::time::Instant::now();assert_eq!(host.stop("person:fixture","codex-stop").unwrap()["state"],"stopped");assert!(started.elapsed()<Duration::from_secs(2));assert!(!host.snapshot()["recoveryPendingObservations"].as_array().unwrap().is_empty());drop(paused);assert!(writer.join().unwrap().is_err());host.flush_recovery_observations();let view=host.snapshot();assert!(view["recoveryPendingObservations"].as_array().unwrap().is_empty());let summaries:Vec<_>=view["recovery"]["entries"].as_array().unwrap().iter().filter(|e|e["kind"]=="register_entry_summary").collect();assert_eq!(summaries[0]["state"],"listed");assert_eq!(summaries.last().unwrap()["state"],"closed");assert!(view["recovery"]["entries"].as_array().unwrap().iter().all(|e|e["kind"]!="conversation_index"));std::fs::remove_dir_all(root).unwrap();
    }

    // Shared consumer join uses actual private selection/Prepared/SourceRequest
    // through the owning callback and pipe, never reconstructed DTO evidence.
    fn shared_attachment_selected(root:&std::path::Path)->(Mutex<Result<crate::runtime_session::AttachmentSelectionSession,String>>,String,u64,Vec<String>){let state=Mutex::new(crate::runtime_session::AttachmentSelectionSession::new(Some(root.join("explicit-App-P"))));let view=state.lock().unwrap().as_ref().unwrap().snapshot();let owner=view["ownerRef"].as_str().unwrap().to_owned();let next=crate::runtime_session::select_attachment_source(&state,&owner,0,||Ok(Some(root.join("first.txt")))).unwrap();let revision=next["listRevision"].as_u64().unwrap();let order=next["selections"].as_array().unwrap().iter().map(|r|r["selection"]["selectionRef"].as_str().unwrap().to_owned()).collect();(state,owner,revision,order)}
    fn shared_attachment_exchange<F>(host:&Arc<Host>,generation:&Value,response:Value,operation:F)->Result<Value,String>where F:FnOnce()->Result<Value,String>{let mut child=Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();*host.stdin.lock().unwrap()=child.stdin.take();let stdout=child.stdout.take().unwrap();let source=Arc::clone(host);let generation=generation.clone();let worker=std::thread::spawn(move||{let mut line=String::new();BufReader::new(stdout).read_line(&mut line).unwrap();let outbound:Value=serde_json::from_str(&line).unwrap();let mut response=response;response["id"]=outbound["id"].clone();source.on_line(&serde_json::to_vec(&response).unwrap(),&generation);outbound});let result=operation();let outbound=worker.join().unwrap();assert_eq!(outbound["params"]["input"].as_array().unwrap().len(),2);assert!(outbound["params"].get("project").is_none());assert!(outbound["params"].get("cwd").is_none());*host.stdin.lock().unwrap()=None;assert!(child.wait().unwrap().success());result}
    #[test]
    fn shared_attachment_submit_actual_context_and_capabilities(){
        use crate::recovery::{ExplicitAppProjectContext as Context,AppProjectSource};for known in [false,true]{let(host,g,root,custody,_)=context_fixture();let(state,owner,revision,order)=shared_attachment_selected(&root);let context=if known{host.observe_conversation_project(&g,"thread",Some("H-acct"),&Context::known("explicit App P",AppProjectSource::ConfiguredDirectory).unwrap()).unwrap();Context::known("frozen current Root Q",AppProjectSource::OpenedDirectory).unwrap()}else{Context::unknown()};let home=if known{Some("H-acct")}else{None};let result=shared_attachment_exchange(&host,&g,json!({"result":{"turn":complete_turn()}}),||crate::runtime_session::submit_selected_attachments(&state,&host,Arc::clone(&custody),&owner,revision,&order,&g,"thread",None,"explicit ordinary text without WR prefix",context.clone(),home)).unwrap();assert_eq!(result["sourceWriteConfirmed"],true);assert_eq!(result["nativeTurnRef"]["threadId"],"thread");let view=state.lock().unwrap().as_ref().unwrap().snapshot();assert_eq!(view["submissions"].as_array().unwrap().len(),1);let binding=&view["submissions"][0]["contextBinding"];if known{assert_eq!(binding["historicalProject"],"explicit App P");assert_eq!(binding["currentSubmissionProject"],"frozen current Root Q");assert_eq!(binding["persistence"],"durable App metadata");}else{assert!(binding["indexSnapshot"].is_null());assert_eq!(binding["persistence"],"memory-only");assert!(binding["limit"].as_str().unwrap().contains("cold lookup unavailable"));}let count=host.client_requests().len();state.lock().unwrap().as_mut().unwrap().refresh_submissions(&host,&custody);assert_eq!(host.client_requests().len(),count);std::fs::remove_dir_all(root).unwrap();}
    }
    #[test]
    fn shared_attachment_submit_drift_stale_source_and_native_error_preserve_no_retry(){
        use crate::recovery::ExplicitAppProjectContext as Context;for stale in [false,true]{let(host,g,root,custody,_)=context_fixture();let(state,owner,revision,order)=shared_attachment_selected(&root);if stale{host.inner.0.lock().unwrap().generation["spawnCounter"]=json!(2);}else{std::fs::write(root.join("first.txt"),"changed since native selection").unwrap();}no_attachment_write(&host,||{assert!(crate::runtime_session::submit_selected_attachments(&state,&host,Arc::clone(&custody),&owner,revision,&order,&g,"thread",None,"person text",Context::unknown(),None).is_err());});assert_eq!(host.inner.0.lock().unwrap().send_position,0);assert_eq!(state.lock().unwrap().as_ref().unwrap().snapshot()["selections"].as_array().unwrap().len(),1);std::fs::remove_dir_all(root).unwrap();}
        let(host,g,root,custody,_)=context_fixture();let(state,owner,revision,order)=shared_attachment_selected(&root);let result=shared_attachment_exchange(&host,&g,json!({"error":{"code":-32600,"message":"synthetic refusal"}}),||crate::runtime_session::submit_selected_attachments(&state,&host,Arc::clone(&custody),&owner,revision,&order,&g,"thread",None,"person text",Context::unknown(),None));assert!(result.is_err());let count=host.client_requests().len();state.lock().unwrap().as_mut().unwrap().refresh_submissions(&host,&custody);let view=state.lock().unwrap().as_ref().unwrap().snapshot();assert_eq!(view["submissions"].as_array().unwrap().len(),1);assert!(view["submissions"][0]["outcome"]["resolution"]["nativeTurnRef"].is_null());assert_eq!(host.client_requests().len(),count);assert_eq!(view["selections"].as_array().unwrap().len(),1);std::fs::remove_dir_all(root).unwrap();
    }

    const AUTH_CANARY:&str="SYNTHETIC_UNIT_A_KEY_CANARY_9b71_not_a_real_credential";
    fn assert_auth_retained_safe(host:&Host,source:Option<&SourceRequest>){let mut all=json!({"snapshot":host.snapshot(),"clients":host.client_requests(),"journal":host.journal()});if let Some(source)=source{all["source"]=source.evidence();all["attempted"]=source.attempted_frame().clone();all["observation"]=host.account_rpc_observation(source).unwrap();}let text=serde_json::to_string(&all).unwrap();assert!(!text.contains(AUTH_CANARY),"synthetic canary leaked into retained output");assert!(!format!("{all:?}").contains(AUTH_CANARY));}
    #[test]
    fn credential_rpc_private_wire_once_and_redacted_receipt_typed_presence(){let host=host();let mut source=None;let(result,outbound)=exchange(&host,Some(json!({"result":{"type":"apiKey","apiKey":AUTH_CANARY,"extraEcho":AUTH_CANARY}})),vec![],||{let r=host.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),None)?;let e=host.source_request_wait(&r,Duration::from_millis(20))?;source=Some(r);Ok(e)});let e=result.unwrap();let source=source.unwrap();assert_eq!(outbound["params"],json!({"type":"apiKey","apiKey":AUTH_CANARY}));assert_eq!(serde_json::to_string(&outbound).unwrap().matches(AUTH_CANARY).count(),1);assert_eq!(e["writeResult"],"written");assert_eq!(e["outcome"],"response-observed-result");assert_eq!(e["sensitiveFieldsRedacted"],true);assert!(e["frameEvidence"].as_str().unwrap().contains("not original"));assert_eq!(e["response"]["result"],json!({"type":"apiKey"}));assert_eq!(host.account_rpc_observation(&source).unwrap()["accountObservation"]["credentialValidity"],"unknown");assert_auth_retained_safe(&host,Some(&source));let count=host.client_requests().len();host.source_request_status(&source).unwrap();assert_eq!(host.client_requests().len(),count);}
    #[test]
    fn credential_rpc_delayed_released_key_error_closed_channel_and_unrelated_notification(){let host=host();let mut source=None;let(result,outbound)=exchange(&host,None,vec![],||{let r=host.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),None)?;let e=host.source_request_wait(&r,Duration::from_millis(10))?;source=Some(r);Ok(e)});assert_eq!(result.unwrap()["waitingEnded"],true);let source=source.unwrap();assert_auth_retained_safe(&host,Some(&source));let error=json!({"id":outbound["id"],"error":{"code":-32000,"message":format!("native auth echoed {AUTH_CANARY}"),"data":{"secret":AUTH_CANARY}}});host.on_line(&serde_json::to_vec(&error).unwrap(),&g());assert_eq!(source.evidence()["outcome"],"response-observed-error");assert_eq!(source.evidence()["response"]["error"]["code"],-32000);assert_auth_retained_safe(&host,Some(&source));let ordinary=json!({"method":"unrelated/native-notification","params":{"text":"ordinary source bytes","extra":7}});host.on_line(&serde_json::to_vec(&ordinary).unwrap(),&g());assert_eq!(host.journal().last().unwrap()["frame"],ordinary);
        host.on_line(&serde_json::to_vec(&json!({"method":"account/login/completed","params":{"loginId":AUTH_CANARY,"success":AUTH_CANARY,"error":null}})).unwrap(),&g());assert_eq!(host.journal().last().unwrap()["frame"]["params"]["success"],auth_rpc::REDACTED);assert_auth_retained_safe(&host,Some(&source));
        Host::close_generation(&mut host.inner.0.lock().unwrap());host.on_line(&serde_json::to_vec(&json!({"method":"account/login/completed","params":{"loginId":"observed-login","success":false,"error":AUTH_CANARY,"authUrl":AUTH_CANARY,"verificationUrl":AUTH_CANARY,"userCode":AUTH_CANARY}})).unwrap(),&g());host.on_line(format!("unparseable original auth diagnostic {AUTH_CANARY}").as_bytes(),&g());assert_eq!(host.journal().last().unwrap()["class"],"closed-generation-frame");assert!(host.journal().last().unwrap()["frame"]["observation"].as_str().unwrap().contains("unattributed"));assert_auth_retained_safe(&host,Some(&source));assert_eq!(host.client_requests().len(),1);}
    #[test]
    fn credential_rpc_generic_bypass_and_known_native_policy_exclusion_send_no_key(){let host=host();no_attachment_write(&host,||{for params in [json!({"type":"apiKey","apiKey":AUTH_CANARY}),json!({"type":"chatgpt","apiKey":AUTH_CANARY}),json!({"type":"chatgptAuthTokens","accessToken":AUTH_CANARY}),json!({"type":"amazonBedrockAccessKeys","secretAccessKey":AUTH_CANARY,"sessionToken":AUTH_CANARY})]{let error=host.request("account/login/start",params,json!({"kind":"person-directed"})).unwrap_err();assert!(!error.contains(AUTH_CANARY));}assert!(host.request("account/read",json!({"refreshToken":true}),json!({"kind":"app-rule","name":"read"})).is_err());assert!(host.client_requests().is_empty());});assert_auth_retained_safe(&host,None);
        for methods in [json!([]),json!(["chatgpt"])]{let mut policy=None;let(result,_)=exchange(&host,Some(json!({"result":{"requirements":{"allowedLoginMethods":methods,"cliAuthCredentialsStore":"auto"}}})),vec![],||{let source=host.request_begin_scoped("configRequirements/read",json!({}),json!({"kind":"person-directed"}),false,Some(&g()))?;let e=host.source_request_wait(&source,Duration::from_millis(20))?;policy=Some(source);Ok(e)});assert_eq!(result.unwrap()["outcome"],"response-observed-result");let count=host.client_requests().len();no_attachment_write(&host,||{let error=host.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),policy.as_ref()).err().unwrap();assert!(error.contains("excludes"));assert!(!error.contains(AUTH_CANARY));});assert_eq!(host.client_requests().len(),count);assert_auth_retained_safe(&host,None);}}
    #[test]
    fn credential_rpc_known_source_nonprotocol_diagnostics_fresh_and_closed_are_unattributed(){
        let host=host();let mut source=None;let(result,_)=exchange(&host,None,vec![],||{let r=host.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),None)?;let e=host.source_request_wait(&r,Duration::from_millis(5))?;source=Some(r);Ok(e)});assert_eq!(result.unwrap()["waitingEnded"],true);let source=source.unwrap();
        for closed in [false,true]{if closed{Host::close_generation(&mut host.inner.0.lock().unwrap());}
            for raw in [serde_json::to_vec(&json!({"message":AUTH_CANARY})).unwrap(),serde_json::to_vec(&json!([AUTH_CANARY])).unwrap(),serde_json::to_vec(&json!(AUTH_CANARY)).unwrap(),format!("non JSON {AUTH_CANARY}").into_bytes()]{
                host.on_line(&raw,&g());let entry=host.journal().last().unwrap().clone();assert_eq!(entry["class"],if closed{"closed-generation-frame"}else{"malformed"});assert!(entry["frame"]["observation"].as_str().unwrap().contains("unattributed"));assert!(entry["frame"].get("id").is_none());assert!(entry["frame"].get("method").is_none());assert_auth_retained_safe(&host,Some(&source));
            }
            for frame in [json!({"method":"turn/unknown-notification","params":{"text":"ordinary source bytes"}}),json!({"method":"supplier/future-notification","params":{"text":"opaque native value","field":7}})]{host.on_line(&serde_json::to_vec(&frame).unwrap(),&g());assert_eq!(host.journal().last().unwrap()["frame"],frame);}
        }
        assert!(source.evidence()["response"].is_null());assert_eq!(host.client_requests().len(),1);
        // Deliberate inverse: no released-key matcher/global DLP on an unrelated
        // valid notification, even when its test text equals the synthetic canary.
        let unrelated=json!({"method":"supplier/future-notification","params":{"text":AUTH_CANARY}});host.on_line(&serde_json::to_vec(&unrelated).unwrap(),&g());assert_eq!(host.journal().last().unwrap()["frame"],unrelated);assert!(!serde_json::to_string(&source.evidence()).unwrap().contains(AUTH_CANARY));
        // Outside a known account source there is no diagnostic attribution/filter.
        let ordinary=super::conversation_transport_tests::host();let raw=json!({"message":"ordinary unrelated diagnostic"});ordinary.on_line(&serde_json::to_vec(&raw).unwrap(),&g());assert_eq!(ordinary.journal().last().unwrap()["frame"],raw);
    }
    #[test]
    fn credential_rpc_nominal_fields_and_mismatched_modes_never_become_safe_identity(){
        for result in [json!({"type":AUTH_CANARY}),json!({"type":"apiKey","loginId":AUTH_CANARY}),json!({"type":"chatgpt","loginId":AUTH_CANARY,"authUrl":AUTH_CANARY}),json!({"type":"chatgptDeviceCode","loginId":AUTH_CANARY,"userCode":AUTH_CANARY,"verificationUrl":AUTH_CANARY}),json!({"type":"chatgpt"}),json!(AUTH_CANARY)]{
            let host=host();let mut source=None;let(outcome,_)=exchange(&host,Some(json!({"result":result})),vec![],||{let r=host.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),None)?;let e=host.source_request_wait(&r,Duration::from_millis(20))?;source=Some(r);Ok(e)});
            assert_eq!(outcome.unwrap()["outcome"],"response-observed-result");let source=source.unwrap();let view=host.account_rpc_observation(&source).unwrap();let state=view["accountObservation"]["state"].as_str().unwrap();
            if result["type"]=="apiKey"{assert!(state.contains("presence reported"));assert!(source.evidence()["response"]["result"].get("loginId").is_none());}else{assert!(state.contains("unknown"));}
            assert_auth_retained_safe(&host,Some(&source));
            // Actual attempt buffer is now dropped. Duplicate is unadmitted;
            // closed original source still gets nominal-field projection.
            let late=json!({"id":source.request_id(),"result":result});host.on_line(&serde_json::to_vec(&late).unwrap(),&g());assert_eq!(host.journal().last().unwrap()["class"],"uncorrelated-response");assert_auth_retained_safe(&host,Some(&source));
            Host::close_generation(&mut host.inner.0.lock().unwrap());host.on_line(&serde_json::to_vec(&late).unwrap(),&g());assert_eq!(host.journal().last().unwrap()["class"],"closed-generation-frame");assert_auth_retained_safe(&host,Some(&source));
        }
    }
    #[test]
    fn credential_rpc_policy_valid_api_omitted_null_and_malformed_are_distinct(){
        for requirements in [None,Some(Value::Null),Some(json!({"allowedLoginMethods":["api"]})),Some(json!({"allowedLoginMethods":[AUTH_CANARY]}))]{
            let host=host();let mut result=json!({});if let Some(req)=requirements.clone(){result["requirements"]=req;}let mut policy=None;
            let(outcome,_)=exchange(&host,Some(json!({"result":result})),vec![],||{let r=host.request_begin_scoped("configRequirements/read",json!({}),json!({"kind":"person-directed"}),false,Some(&g()))?;let e=host.source_request_wait(&r,Duration::from_millis(20))?;policy=Some(r);Ok(e)});assert_eq!(outcome.unwrap()["outcome"],"response-observed-result");let policy=policy.unwrap();assert_auth_retained_safe(&host,Some(&policy));
            if requirements.as_ref().is_some_and(|r|r["allowedLoginMethods"][0]==AUTH_CANARY){no_attachment_write(&host,||{assert!(host.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),Some(&policy)).err().unwrap().contains("malformed"));});}else{let(outcome,_)=exchange(&host,Some(json!({"result":{"type":"apiKey"}})),vec![],||{let r=host.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),Some(&policy))?;host.source_request_wait(&r,Duration::from_millis(20))});assert_eq!(outcome.unwrap()["outcome"],"response-observed-result");assert_auth_retained_safe(&host,None);}
        }
    }
    #[test]
    fn credential_rpc_typed_read_logout_policy_require_actual_native_shape(){
        for (method,result) in [("account/read",json!({"account":{"type":AUTH_CANARY},"requiresOpenaiAuth":AUTH_CANARY})),("account/read",json!({"account":{"type":"chatgpt"},"requiresOpenaiAuth":true})),("account/read",json!({})),("account/logout",json!(AUTH_CANARY)),("configRequirements/read",json!({"requirements":{"allowedLoginMethods":[AUTH_CANARY]}}))]{
            let host=host();let mut source=None;let(outcome,_)=exchange(&host,Some(json!({"result":result})),vec![],||{let r=host.request_begin_scoped(method,json!({}),json!({"kind":"person-directed"}),false,Some(&g()))?;let e=host.source_request_wait(&r,Duration::from_millis(20))?;source=Some(r);Ok(e)});
            assert_eq!(outcome.unwrap()["outcome"],"response-observed-result");let source=source.unwrap();assert_eq!(source.evidence()["authResponseShapeValid"],false);assert!(host.account_rpc_observation(&source).unwrap()["accountObservation"]["state"].as_str().unwrap().contains("unknown"));assert_auth_retained_safe(&host,Some(&source));
        }
    }
    #[test]
    fn credential_rpc_actual_failed_write_and_logout_do_not_claim_validity_or_turn_end(){
        let host=host();install_broken_test_input(&host);
        let source=host.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),None).unwrap();
        let e=source.evidence();assert_eq!(e["actualWriteAttemptObserved"],true);assert_eq!(e["writeResult"],"write-failed");assert!(e["sentFrame"].is_null());assert_eq!(e["outcome"],"unknown-no-response");assert_auth_retained_safe(&host,Some(&source));
        let n=host.client_requests().len();host.source_request_wait(&source,Duration::from_millis(1)).unwrap();assert_eq!(host.client_requests().len(),n);
        // Failure removes pending admission; a later native error remains redacted, uncorrelated journal evidence.
        host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"error":{"code":-32001,"message":AUTH_CANARY}})).unwrap(),&g());
        assert!(source.evidence()["response"].is_null());assert_eq!(host.journal().last().unwrap()["class"],"uncorrelated-response");assert_eq!(host.journal().last().unwrap()["frame"]["error"]["code"],-32001);assert_auth_retained_safe(&host,Some(&source));
        event(&host,"inProgress");let before=host.snapshot()["conversationTurns"].clone();let mut logout=None;
        let(result,outbound)=exchange(&host,Some(json!({"result":{}})),vec![],||{let r=host.request_begin_scoped("account/logout",json!({}),json!({"kind":"person-directed"}),false,Some(&g()))?;let e=host.source_request_wait(&r,Duration::from_millis(20))?;logout=Some(r);Ok(e)});
        assert_eq!(outbound["params"],json!({}));assert_eq!(result.unwrap()["outcome"],"response-observed-result");assert_eq!(host.snapshot()["conversationTurns"],before);
        let logout=logout.unwrap();assert!(host.account_rpc_observation(&logout).unwrap()["accountObservation"]["state"].as_str().unwrap().contains("no filesystem removal"));assert_auth_retained_safe(&host,Some(&logout));
        assert_eq!(auth_rpc::login_policy(Some(&json!({"result":{"requirements":null}}))).unwrap(),"restriction absent/null; policy permission unknown");
    }
    #[test]
    fn credential_rpc_queued_loss_foreign_home_and_account_read_omission_keep_unknown(){let host=host();no_attachment_write(&host,||{let serial=host.frame_write.lock().unwrap();let caller=Arc::clone(&host);let worker=std::thread::spawn(move||caller.account_login_api_key(&g(),auth_rpc::TransientApiKey::synthetic(AUTH_CANARY),None));let deadline=std::time::Instant::now()+Duration::from_secs(1);while host.inner.0.lock().unwrap().source_requests.is_empty()&&std::time::Instant::now()<deadline{std::thread::sleep(Duration::from_millis(5));}let source=host.source_request(&g(),&json!(1)).unwrap();assert_auth_retained_safe(&host,Some(&source));let foreign=json!({"appSession":"conversation-session","home":"other-home","spawnCounter":1});host.on_line(&serde_json::to_vec(&json!({"id":1,"error":{"code":-32000,"message":"foreign harmless"}})).unwrap(),&foreign);assert!(source.evidence()["response"].is_null());{let mut i=host.inner.0.lock().unwrap();Host::close_generation(&mut i);i.generation=foreign;i.state="ready".into();}let returned=worker.join().unwrap().unwrap();drop(serial);assert_eq!(returned.evidence()["actualWriteAttemptObserved"],false);assert!(returned.evidence()["noAttemptCause"].as_str().unwrap().contains("transient input released"));assert_auth_retained_safe(&host,Some(&returned));});
        let host=super::conversation_transport_tests::host();for account in [None,Some(Value::Null),Some(json!({"type":"apiKey","apiKey":AUTH_CANARY,"email":AUTH_CANARY}))]{let mut result=json!({"requiresOpenaiAuth":true});if let Some(account)=account.clone(){result["account"]=account;}let mut source=None;let(outcome,outbound)=exchange(&host,Some(json!({"result":result})),vec![],||{let r=host.request_begin_scoped("account/read",json!({}),json!({"kind":"person-directed"}),false,Some(&g()))?;let e=host.source_request_wait(&r,Duration::from_millis(20))?;source=Some(r);Ok(e)});assert_eq!(outbound["params"],json!({}));assert_eq!(outcome.unwrap()["outcome"],"response-observed-result");let source=source.unwrap();let view=host.account_rpc_observation(&source).unwrap();assert_eq!(view["accountObservation"]["identityVerified"],false);if account.is_none(){assert!(view["accountObservation"]["state"].as_str().unwrap().contains("omitted"));}assert_auth_retained_safe(&host,Some(&source));}}
}
