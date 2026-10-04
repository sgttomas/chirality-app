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
//! Not implemented in the skeleton: restart rules (§4.4), the outstanding
//! server-request register (§6) beyond listing server requests as received,
//! the per-home config link (§4.2 step 3, option C), journal replay for
//! re-attaching observers (§4.6).

use crate::util::{now_rfc3339, sha256_hex};
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
pub const DECLARED_PIN: &str = "0.158.0";
/// Generated-output identity: the pin and generator the protocol types came from
/// (HOSTING §7.1; DEL-01-01 Design/generated/0.158.0, manifest 42b95826…).
pub const GENERATED_OUTPUT_IDENTITY: &str =
    "codex app-server generate-json-schema --experimental @ 0.158.0 (manifest sha256 42b95826…69e)";

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
    /// Expected distribution content identity (sha-256 hex of the binary), recorded when
    /// the pin is qualified (§7.1). None: no qualification exists.
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
    generation: u64,
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
    next_id: u64,
    send_position: u64,
    version_identity: Option<Value>,
    verification: Option<Value>,
    declared_capabilities: Option<Value>,
    configuration_identity: Option<Value>,
    stop_record: Option<Value>,
    threads: Vec<Value>,
    stderr_bytes: u64,
    child_pid: Option<i32>,
}

pub struct Host {
    inner: Arc<(Mutex<Inner>, Condvar)>,
    stdin: Mutex<Option<ChildStdin>>,
    child: Mutex<Option<Child>>,
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
            ..Default::default()
        };
        Host {
            inner: Arc::new((Mutex::new(inner), Condvar::new())),
            stdin: Mutex::new(None),
            child: Mutex::new(None),
        }
    }

    fn lt(&self, inner: &mut Inner, id: &str, event: &str, to: &str, extra: Value) {
        let gen = if inner.generation == 0 { Value::Null } else { json!(inner.generation) };
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
        json!({
            "state": i.state,
            "generation": if i.generation == 0 { Value::Null } else { json!(i.generation) },
            "verification": i.verification,
            "versionIdentity": i.version_identity,
            "declaredCapabilities": i.declared_capabilities,
            "configurationIdentity": i.configuration_identity,
            "lifecycle": i.lifecycle,
            "clientRequests": i.client_requests,
            "journal": i.journal,
            "malformedFrames": i.malformed,
            "threads": i.threads,
            "modelTurnExercised": false,
        })
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
        let label = Command::new(&cfg.codex_bin)
            .arg("--version")
            .env("CODEX_HOME", &cfg.probe_home)
            .env_remove("OPENAI_API_KEY")
            .env_remove("CODEX_API_KEY")
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
        if label != format!("codex-cli {DECLARED_PIN}") {
            return (json!({"result": "mismatch", "element": "observed version label"}), Some(label), dist);
        }
        match &cfg.expected_sha256 {
            Some(exp) if exp.eq_ignore_ascii_case(&content) => (json!({"result": "verified"}), Some(label), dist),
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
            // U-06: an unverified distribution may run for development; it is never
            // labelled the pinned supplier. LT-04's guard is `verified`; under U-06 the
            // skeleton writes LT-04 with the actual (unverifiable) result and a reason.
            let extra = if verified {
                json!({"verificationResult": result})
            } else {
                json!({"verificationResult": result,
                       "reason": "U-06 development run: unverified distribution, not the pinned supplier"})
            };
            self.lt(&mut i, "LT-04", "verification-passed", "spawning", extra);
            i.version_identity = Some(json!({
                "declaredPin": DECLARED_PIN,
                "observedVersionLabel": label.clone().unwrap_or_default(),
                "distributionContentIdentity": dist,
                "launcherRecord": {"launcher": "vendor-binary", "addedEnvironment": []},
                "handshakeReportedIdentity": {},
                "handshakeConsistency": "no-version-found",
                "generatedOutputIdentity": GENERATED_OUTPUT_IDENTITY,
                "supplementIdentity": "empty at 0.158.0",
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
            i.generation = i.spawn_counter; // H5: new generation at spawn.
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
        self.spawn_reader(stdout);
        self.spawn_stderr(stderr);

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
                // initialized notice (whether it is required is U-19; it is sent).
                let _ = self.write_frame(&json!({"jsonrpc": "2.0", "method": "initialized"}));
                let mut i = self.inner.0.lock().unwrap();
                let ua = result.get("userAgent").and_then(|v| v.as_str()).unwrap_or("");
                let consistency = match ua.split('/').nth(1).and_then(|s| s.split_whitespace().next()) {
                    Some(v) if v == DECLARED_PIN => "consistent",
                    Some(_) => "contradicts-declared-pin",
                    None => "no-version-found",
                };
                if let Some(vi) = i.version_identity.as_mut() {
                    vi["handshakeReportedIdentity"] = result.clone();
                    vi["handshakeConsistency"] = json!(consistency);
                }
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
                let counts = Self::close_generation(&mut i);
                // Held frames are delivered marked as from a generation that never became ready.
                let held: Vec<Value> = std::mem::take(&mut i.held)
                    .into_iter()
                    .map(|mut f| { f["generationNeverReady"] = json!(true); f })
                    .collect();
                i.journal.extend(held);
                self.lt(&mut i, "LT-11", "handshake-failed", "halted-after-repeated-failure",
                        json!({"failure": failure.clone(), "failureCount": 1, "closedGeneration": counts}));
                Err(failure)
            }
        }
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
        json!({"unknownNoResponse": unknown, "endedUnanswered": 0})
    }

    fn write_frame(&self, frame: &Value) -> Result<(), String> {
        let mut g = self.stdin.lock().unwrap();
        let w = g.as_mut().ok_or("input closed")?;
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
        let (tx, rx): (Sender<Value>, Receiver<Value>) = channel();
        let id;
        {
            let mut i = self.inner.0.lock().unwrap();
            let ok_state = if handshake { i.state == "handshaking" } else { i.state == "ready" };
            if !ok_state {
                let gen = if i.generation == 0 { Value::Null } else { json!(i.generation) };
                i.client_requests.push(json!({
                    "recordKind": "client-request", "generation": gen,
                    "requestIdentity": null, "method": method, "initiator": initiator,
                    "writeResult": "not-attempted", "outcome": "refused-not-sent", "refusalReason": "not-ready"}));
                return Err(format!("refused-not-sent(not-ready): state {}", i.state));
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
        }
        let frame = json!({"jsonrpc": "2.0", "id": id, "method": method, "params": params});
        if let Err(e) = self.write_frame(&frame) {
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
    pub fn thread_start(&self, cwd: &str) -> Result<Value, String> {
        let r = self.request("thread/start", json!({"cwd": cwd}), json!({"kind": "person-directed"}))?;
        if let Some(t) = r.get("result").and_then(|x| x.get("thread")) {
            let mut i = self.inner.0.lock().unwrap();
            let gen = i.generation;
            i.threads.push(json!({
                "generation": gen,
                "threadId": t.get("id"),
                "status": t.get("status"),
                "model": r["result"].get("model"),
                "modelProvider": r["result"].get("modelProvider"),
                "cwd": r["result"].get("cwd"),
            }));
            Ok(r)
        } else {
            Err(format!("thread/start answered with an error: {}", r.get("error").cloned().unwrap_or(Value::Null)))
        }
    }

    fn spawn_reader(self: &Arc<Self>, stdout: std::process::ChildStdout) {
        let me = Arc::clone(self);
        std::thread::spawn(move || {
            let mut rd = BufReader::new(stdout);
            let mut line = Vec::new();
            loop {
                line.clear();
                match rd.read_until(b'\n', &mut line) {
                    Ok(0) | Err(_) => break,
                    Ok(_) => me.on_line(&line),
                }
            }
            me.on_eof();
        });
    }

    fn spawn_stderr(self: &Arc<Self>, mut stderr: std::process::ChildStderr) {
        let me = Arc::clone(self);
        std::thread::spawn(move || {
            // Diagnostic output is counted, never parsed as protocol (§5). Bounded: only the count is kept.
            let mut buf = [0u8; 4096];
            while let Ok(n) = stderr.read(&mut buf) {
                if n == 0 {
                    break;
                }
                me.inner.0.lock().unwrap().stderr_bytes += n as u64;
            }
        });
    }

    fn on_line(&self, raw: &[u8]) {
        let text = String::from_utf8_lossy(raw);
        let text = text.trim_end_matches(['\n', '\r']);
        if text.is_empty() {
            return;
        }
        let mut i = self.inner.0.lock().unwrap();
        i.receipt_position += 1;
        let pos = i.receipt_position;
        let gen = i.generation;
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
        if class == "malformed" {
            i.malformed += 1;
        }
        if class == "response" {
            let key = match &frame["id"] {
                Value::String(s) => s.clone(),
                other => other.to_string(),
            };
            if let Some((idx, tx)) = i.pending.remove(&key) {
                let outcome = if frame.get("result").is_some() { "response-observed-result" } else { "response-observed-error" };
                let r = &mut i.client_requests[idx];
                r["outcome"] = json!(outcome);
                r["responseReceiptPosition"] = json!(pos);
                if let Some(e) = frame.get("error") {
                    r["error"] = json!({"code": e.get("code").cloned().unwrap_or(json!(0)),
                                        "message": e.get("message").cloned().unwrap_or(json!(""))});
                }
                let _ = tx.send(frame.clone());
                // Responses are also journaled, with their metadata beside the native frame (H6).
                let entry = json!({"generation": gen, "position": pos, "class": class, "frame": frame});
                i.journal.push(entry);
                return;
            }
            // Uncorrelated response: surfaced, never dropped (§5).
            let entry = json!({"generation": gen, "position": pos, "class": "uncorrelated-response", "frame": frame});
            i.journal.push(entry);
            return;
        }
        let entry = json!({"generation": gen, "position": pos, "class": class, "frame": frame});
        if i.state == "handshaking" {
            i.held.push(entry); // H4
        } else {
            i.journal.push(entry);
        }
    }

    fn on_eof(&self) {
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
            let gen = i.generation;
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
