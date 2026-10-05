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

use crate::native_requests::RequestRegister;
use crate::recovery::RecoveryLedger;
use crate::util::{now_rfc3339, opaque_id, sha256_hex};
use serde_json::{json, Value};
use std::collections::HashMap;
use std::io::{BufRead, BufReader, Read, Write};
use std::os::unix::process::CommandExt;
use std::path::PathBuf;
use std::process::{Child, ChildStdin, Command, Stdio};
use std::sync::mpsc::{channel, Receiver, Sender};
use std::sync::{Arc, Condvar, Mutex};
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
    lifecycle: Vec<Value>,
    client_requests: Vec<Value>,
    /// Frames received before ready (H4), in received order.
    held: Vec<Value>,
    /// Frames delivered to receivers, in received order, each {generation, position, class, frame}.
    journal: Vec<Value>,
    receipt_position: u64,
    malformed: u64,
    pending: HashMap<String, (usize, Sender<Value>)>,
    server_requests: RequestRegister,
    recovery: Option<RecoveryLedger>,
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
    turn_request_threads: HashMap<String, (Value, String)>,
    interrupt_requests: Vec<Value>,
    stderr_bytes: u64,
    child_pid: Option<i32>,
}

pub struct Host {
    inner: Arc<(Mutex<Inner>, Condvar)>,
    stdin: Mutex<Option<ChildStdin>>,
    child: Mutex<Option<Child>>,
    #[cfg(test)]
    before_thread_insert: Mutex<Option<Box<dyn FnOnce() + Send>>>,
    #[cfg(test)]
    before_turn_result: Mutex<Option<Box<dyn FnOnce() + Send>>>,
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
            inner: Arc::new((Mutex::new(inner), Condvar::new())),
            stdin: Mutex::new(None),
            child: Mutex::new(None),
            #[cfg(test)]
            before_thread_insert: Mutex::new(None),
            #[cfg(test)]
            before_turn_result: Mutex::new(None),
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
    pub fn snapshot(&self) -> Value {
        let i = self.inner.0.lock().unwrap();
        Self::snapshot_inner(&i)
    }
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
            "clientRequests": i.client_requests,
            "serverRequests": i.server_requests.records(),
            "recovery": i.recovery.as_ref().map(RecoveryLedger::snapshot),
            "recoveryPersistenceError": i.recovery_error,
            "journal": i.journal,
            "malformedFrames": i.malformed,
            "threads": i.threads,
            "conversationTurns": i.conversation_turns,
            "turnInterruptRequests": i.interrupt_requests.iter().map(|entry| {
                let request = i.client_requests.iter().find(|r| r["generation"] == entry["generation"] && r["requestIdentity"] == entry["requestIdentity"]);
                json!({"binding":entry,"clientRequest":request,"turnOutcome":"determined by native turn events, not interrupt acknowledgment"})
            }).collect::<Vec<_>>(),
            "modelTurnExercised": if i.client_requests.iter().any(|r| r["method"] == "turn/start") { Value::Null } else { json!(false) },
            "modelTurnEvidence": {"standing":"provider/model execution not established by request or mock result", "protocolRequests":i.client_requests.iter().filter(|r| r["method"] == "turn/start").collect::<Vec<_>>()},
        })
    }

    /// Open an App-local pointer ledger before start; never a native-content cache.
    pub fn configure_recovery(&self, path: PathBuf) -> Result<(), String> {
        let mut i = self.inner.0.lock().unwrap();
        if i.state != "absent" { return Err("recovery must be configured before supplier start".into()); }
        let mut ledger = RecoveryLedger::open(path)?;
        if i.app_session.is_empty() { i.app_session = opaque_id("app-session:")?; }
        ledger.start_session(&i.app_session, "chirality-app-v4-unqualified")?;
        i.recovery = Some(ledger); Ok(())
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
    fn persist_requests(i: &mut Inner) {
        let entries = i.server_requests.entries();
        if let Some(ledger) = i.recovery.as_mut() {
            for entry in entries {
                if let Err(error) = ledger.request_summary(&entry) { i.recovery_error = Some(error); break; }
            }
        }
    }

    /// The child's process id, which is also its process-group id (H11).
    pub fn child_pid(&self) -> Option<i32> {
        self.inner.0.lock().unwrap().child_pid
    }
    pub fn lifecycle_events(&self) -> Vec<Value> {
        self.inner.0.lock().unwrap().lifecycle.clone()
    }
    pub fn client_requests(&self) -> Vec<Value> {
        self.inner.0.lock().unwrap().client_requests.clone()
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
        *self.stdin.lock().unwrap() = child.stdin.take();
        let pid = child.id() as i32;
        *self.child.lock().unwrap() = Some(child);
        {
            let mut i = self.inner.0.lock().unwrap();
            i.spawn_counter += 1;
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
                r["outcome"] = json!("unknown-no-response");
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

    /// Serialized with receipt processing: a resolution cannot race a write and
    /// become a fabricated acknowledgment. Full H5 identity is supplied by the caller.
    pub fn answer_server_request(&self, generation: &Value, id: &Value, answer: &Value,
        origin: &str, actor: Option<&str>) -> Result<Value, String> {
        let mut i = self.inner.0.lock().unwrap();
        let frame = i.server_requests.prepare(generation, id, answer, origin, actor)?;
        let result = self.write_frame(&frame);
        i.server_requests.written(generation, id, result.is_ok());
        Self::persist_requests(&mut i);
        result?;
        Ok(json!({"replyWriteResult":"written","acknowledgment":"not-observed"}))
    }

    /// The explicit-error operation carries a named App rule/boundary error;
    /// person interaction answers never enter this protocol-error path.
    pub fn error_server_request(&self, generation: &Value, id: &Value, error: &Value,
        origin: &str) -> Result<Value, String> {
        let mut i = self.inner.0.lock().unwrap();
        let frame = i.server_requests.prepare_error(generation, id, error, origin)?;
        let result = self.write_frame(&frame);
        i.server_requests.written(generation, id, result.is_ok());
        Self::persist_requests(&mut i);
        result?;
        Ok(json!({"replyWriteResult":"written","acknowledgment":"not-observed"}))
    }

    fn write_frame(&self, frame: &Value) -> Result<(), String> {
        let mut g = self.stdin.lock().unwrap();
        Self::write_to_pipe(g.as_mut(), frame)
    }

    fn write_to_pipe(pipe: Option<&mut ChildStdin>, frame: &Value) -> Result<(), String> {
        let w = pipe.ok_or("input closed")?;
        let mut line = serde_json::to_string(frame).map_err(|e| e.to_string())?;
        line.push('\n');
        w.write_all(line.as_bytes()).and_then(|_| w.flush()).map_err(|e| e.to_string())
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
        let (tx, rx): (Sender<Value>, Receiver<Value>) = channel();
        let id;
        let mut scoped_written = false;
        {
            let mut i = self.inner.0.lock().unwrap();
            let ok_state = if handshake { i.state == "handshaking" } else { i.state == "ready" };
            if !ok_state {
                let gen = i.generation.clone();
                i.client_requests.push(json!({
                    "recordKind": "client-request", "generation": gen,
                    "requestIdentity": null, "method": method, "initiator": initiator,
                    "writeResult": "not-attempted", "outcome": "refused-not-sent", "refusalReason": "not-ready"}));
                return Err(format!("refused-not-sent(not-ready): state {}", i.state));
            }
            if expected_generation.map(|g| g != &i.generation || i.server_requests.is_closed(g)).unwrap_or(false) {
                return Err(format!("refused-not-sent: {method} generation changed before request registration"));
            }
            if expected_generation.is_some() && matches!(method, "turn/start" | "turn/interrupt") {
                Self::check_conversation_request(&i, method, &params)?;
            }
            i.next_id += 1;
            id = i.next_id;
            i.send_position += 1;
            let rec = json!({
                "recordKind": "client-request", "generation": i.generation, "requestIdentity": id,
                "method": method, "initiator": initiator, "sendPosition": i.send_position,
                "writeResult": "written", "outcome": "pending"});
            i.client_requests.push(rec);
            let idx = i.client_requests.len() - 1;
            i.pending.insert(id.to_string(), (idx, tx));
            if expected_generation.is_some() && method == "turn/start" {
                let gen = i.generation.clone();
                i.turn_request_threads.insert(id.to_string(), (gen, params["threadId"].as_str().unwrap().into()));
            }
            if expected_generation.is_some() && method == "turn/interrupt" {
                let gen = i.generation.clone();
                i.interrupt_requests.push(json!({"generation":gen,"threadId":params["threadId"],"turnId":params["turnId"],"requestIdentity":id,"initiator":"person-directed"}));
            }

            if expected_generation.is_some() {
                // Acquire the actual source pipe while generation registration
                // is locked. Keep that pipe through writing, then release it
                // before re-locking state; readers may process supplier output
                // while a large guidance frame is being written.
                let mut pipe = self.stdin.lock().unwrap();
                let frame = json!({"jsonrpc":"2.0","id":id,"method":method,"params":params});
                drop(i);
                let write_result = Self::write_to_pipe(pipe.as_mut(), &frame);
                drop(pipe);
                if let Err(error) = write_result {
                    let mut i = self.inner.0.lock().unwrap();
                    i.pending.remove(&id.to_string());
                    i.client_requests[idx]["writeResult"] = json!("write-failed");
                    if i.client_requests[idx]["outcome"] == "pending" {
                        i.client_requests[idx]["outcome"] = json!("unknown-no-response");
                    }
                    return Err(format!("write failed: {error}"));
                }
                scoped_written = true;
            }
        }
        let frame = json!({"jsonrpc": "2.0", "id": id, "method": method, "params": params});
        if let Err(e) = if scoped_written { Ok(()) } else { self.write_frame(&frame) } {
            let mut i = self.inner.0.lock().unwrap();
            if let Some((idx, _)) = i.pending.remove(&id.to_string()) {
                i.client_requests[idx]["writeResult"] = json!("write-failed");
                i.client_requests[idx]["outcome"] = json!("unknown-no-response");
            }
            return Err(format!("write failed: {e}"));
        }
        match rx.recv_timeout(wait) {
            Ok(resp) => Ok(resp),
            Err(_) => {
                // CR-08: a wait limit ends waiting, not the outcome (H10).
                let mut i = self.inner.0.lock().unwrap();
                if let Some((idx, _)) = i.pending.get(&id.to_string()).cloned() {
                    i.client_requests[idx]["waitingEnded"] = json!(true);
                }
                Err(format!("no response to {method} within the wait limit (outcome stays pending/unknown)"))
            }
        }
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
        if let Some(t) = r.get("result").and_then(|x| x.get("thread")) {
            let mut i = self.inner.0.lock().unwrap();
            if i.generation != sent_generation || i.server_requests.is_closed(&sent_generation) {
                // request_inner already journaled the untouched native result.
                // Never associate its old thread with the successor generation.
                return Err("thread/start response belongs to a closed or replaced generation; native response retained in journal".into());
            }
            let gen = sent_generation;
            let standing = i.supplier_standing.clone();
            i.threads.push(json!({
                "generation": gen,
                "threadId": t.get("id"),
                "status": t.get("status"),
                "model": r["result"].get("model"),
                "modelProvider": r["result"].get("modelProvider"),
                "cwd": r["result"].get("cwd"),
                "supplierStanding": standing,
                "requestedDestination": {"source": "person-selected", "model": model, "modelProvider": model_provider},
                "reportedDestination": {"scope": "thread", "model": r["result"].get("model"), "modelProvider": r["result"].get("modelProvider")},
                "networkDisclosure": network_disclosure(),
            }));
            Ok(r)
        } else {
            Err(format!("thread/start answered with an error: {}", r.get("error").cloned().unwrap_or(Value::Null)))
        }
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

    fn text_turn_params(thread_id: &str, text: &str) -> Result<Value, String> {
        if thread_id.is_empty() || text.is_empty() { return Err("thread identity and text required".into()); }
        Ok(json!({"threadId":thread_id,"input":[{"type":"text","text":text,"text_elements":[]}]}))
    }

    fn conversation_operation(&self, method: &str, generation: &Value, params: Value, wait: Duration) -> Result<Value, String> {
        crate::recovery::generation_ref(generation)?;
        let response = self.request_inner_scoped(method, params, json!({"kind":"person-directed"}), wait, false, Some(generation))?;
        #[cfg(test)]
        if let Some(hook) = self.before_turn_result.lock().unwrap().take() { hook(); }
        let i = self.inner.0.lock().unwrap();
        if i.generation != *generation || i.server_requests.is_closed(generation) || i.state != "ready" {
            return Err(format!("{method} response belongs to closed/replaced generation; native response retained in journal"));
        }
        if let Some(error) = response.get("error") { return Err(format!("{method} native error: {error}")); }
        if method == "turn/start" {
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

    fn check_conversation_request(i: &Inner, method: &str, params: &Value) -> Result<(), String> {
        let thread = params["threadId"].as_str().filter(|s| !s.is_empty()).ok_or("thread identity required")?;
        if !i.threads.iter().any(|t| t["generation"] == i.generation && t["threadId"] == thread) { return Err("conversation-not-loaded-in-current-home-generation".into()); }
        if method == "turn/interrupt" {
            let turn = &params["turnId"];
            if !i.conversation_turns.iter().any(|t| t["generation"] == i.generation && t["threadId"] == thread && t["turnId"] == *turn && t["nativeTurn"]["status"] == "inProgress" && t["terminalEventObserved"] != true && t["observationEnded"] != true) { return Err("no-live-turn".into()); }
            if i.interrupt_requests.iter().any(|e| e["generation"] == i.generation && e["threadId"] == thread && e["turnId"] == *turn
                && i.client_requests.iter().any(|r| r["generation"] == e["generation"] && r["requestIdentity"] == e["requestIdentity"]
                    && (r["outcome"] == "response-observed-result" || (r["outcome"] == "pending" && r["writeResult"] == "written")))) { return Err("stop-already-requested".into()); }
        }
        Ok(())
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
        if &i.generation != generation || i.server_requests.is_closed(generation) {
            let frame = serde_json::from_str::<Value>(text).unwrap_or_else(|_| json!(text));
            i.journal.push(json!({"generation": generation, "class": "closed-generation-frame", "frame": frame}));
            return;
        }
        i.receipt_position += 1;
        let pos = i.receipt_position;
        let gen = i.generation.clone();
        let parsed: Option<Value> = serde_json::from_str(text).ok();
        let (class, frame) = match parsed {
            Some(f) if f.is_object() => {
                let has_id = f.get("id").is_some();
                let has_method = f.get("method").is_some();
                let class = if has_method && has_id {
                    "server-request"
                } else if has_method {
                    "notification"
                } else if has_id && (f.get("result").is_some() || f.get("error").is_some()) {
                    "response"
                } else {
                    "malformed"
                };
                (class, f)
            }
            _ => ("malformed", json!(text)),
        };
        if class == "server-request" {
            let capabilities = i.declared_capabilities.clone().unwrap_or(Value::Null);
            match i.server_requests.receive(&gen, pos, &frame, &capabilities) {
                Ok(Some(reply)) => {
                    let written = self.write_frame(&reply).is_ok();
                    i.server_requests.written(&gen, &frame["id"], written);
                }
                Ok(None) => {
                    if frame["method"] == "currentTime/read" && capabilities["experimentalApi"] == true {
                        let seconds = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs();
                        if let Ok(reply) = i.server_requests.prepare(&gen, &frame["id"], &json!({"currentTimeAt":seconds}), "app-rule:current-time", None) {
                            let written = self.write_frame(&reply).is_ok();
                            i.server_requests.written(&gen, &frame["id"], written);
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
                let outcome = if frame.get("result").is_some() { "response-observed-result" } else { "response-observed-error" };
                let r = &mut i.client_requests[idx];
                r["outcome"] = json!(outcome);
                r["responseReceiptPosition"] = json!(pos);
                if let Some(e) = frame.get("error") {
                    r["error"] = json!({"code": e.get("code").cloned().unwrap_or(json!(0)),
                                        "message": e.get("message").cloned().unwrap_or(json!(""))});
                }
                if i.client_requests[idx]["method"] == "turn/start" {
                    if let Some((source_gen, thread)) = i.turn_request_threads.remove(&key) {
                        if source_gen == gen {
                            if let Some(turn) = frame.get("result").and_then(|r| r.get("turn")) { Self::remember_turn(&mut i, &gen, &thread, turn, "turn/start response", pos); }
                        }
                    }
                }
                let _ = tx.send(frame.clone());
                // Responses are also journaled, with their metadata beside the native frame (H6).
                let entry = json!({"generation": gen, "position": pos, "class": class, "frame": frame});
                if i.state == "handshaking" { i.held.push(entry); } else { i.journal.push(entry); }
                return;
            }
            // Uncorrelated response: surfaced, never dropped (§5).
            let entry = json!({"generation": gen, "position": pos, "class": "uncorrelated-response", "frame": frame});
            if i.state == "handshaking" { i.held.push(entry); } else { i.journal.push(entry); }
            return;
        }
        let entry = json!({"generation": gen, "position": pos, "class": class, "frame": frame});
        if i.state == "handshaking" {
            i.held.push(entry); // H4
        } else {
            i.journal.push(entry);
        }
    }

    fn on_eof(&self, generation: &Value) {
        if self.inner.0.lock().unwrap().generation != *generation { return; }
        // Reap the child to read its exit status.
        let status = self.child.lock().unwrap().as_mut().and_then(|c| c.wait().ok());
        let mut i = self.inner.0.lock().unwrap();
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
            self.inner.1.notify_all();
            return;
        }
        if i.state == "ready" {
            // LT-12: ended with no App stop record, whatever the exit status (S-F-07).
            self.lt(&mut i, "LT-12", "child-ended-without-stop-record", "exited-unexpectedly",
                    json!({"exitFacts": exit, "closedGeneration": counts}));
        }
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
        let pid;
        {
            let mut i = self.inner.0.lock().unwrap();
            if matches!(i.state.as_str(), "absent" | "stopped" | "refused") {
                return Err(format!("stop not accepted in state {}", i.state));
            }
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
        }
        *self.stdin.lock().unwrap() = None; // close input: polite end
        let mut forced = false;
        if let Some(pid) = pid {
            let deadline = std::time::Instant::now() + Duration::from_secs(3);
            while Self::group_alive(pid) && std::time::Instant::now() < deadline {
                std::thread::sleep(Duration::from_millis(50));
            }
            if Self::group_alive(pid) {
                forced = true;
                self.kill_group();
                std::thread::sleep(Duration::from_millis(200));
            }
        }
        let surviving = pid.map(|p| if Self::group_alive(p) { 1 } else { 0 }).unwrap_or(0);
        // Wait for the reader to observe EOF.
        let (lock, cv) = &*self.inner;
        let mut i = lock.lock().unwrap();
        let deadline = std::time::Instant::now() + Duration::from_secs(3);
        while !i.journal.iter().any(|e| e["class"] == "exit" && e["generation"] == json!(i.generation))
            && std::time::Instant::now() < deadline
        {
            let (g, _) = cv.wait_timeout(i, Duration::from_millis(100)).unwrap();
            i = g;
        }
        let mut exit = i.journal.iter().rev().find(|e| e["class"] == "exit").map(|e| e["exitFacts"].clone())
            .unwrap_or(json!({"exitCode": null, "signal": null}));
        exit["forcedAfterGrace"] = json!(forced);
        let counts = Self::close_generation(&mut i);
        self.lt(&mut i, "LT-23", "tree-ended", "stopped", json!({
            "exitFacts": exit,
            "descendants": {"checked": true, "surviving": surviving, "handling": if surviving > 0 { "recorded; not ended" } else { "none surviving" }},
            "closedGeneration": counts}));
        Ok(json!({"state": i.state}))
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
            i.client_requests.push(json!({"generation":current,"outcome":"pending"}));
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
        let error=host.thread_start_with_guidance("/invented","m","p","exact guidance").unwrap_err();assert!(error.contains("write failed"));
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
        assert!(host.turn_start_text(&g(),"thread","text").unwrap_err().contains("write failed"));assert_eq!(host.client_requests()[1]["outcome"],"unknown-no-response");assert_eq!(host.client_requests()[1]["writeResult"],"write-failed");
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
}
