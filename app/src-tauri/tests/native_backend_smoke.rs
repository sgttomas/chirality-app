//! Parent-only real supplier/provider probe. Ordinary tests never run this.
//! No raw native journal, prompts, account/config/auth data is published.
use chirality_app_v4_lib::{
    hosting::{Host, HostConfig},
    role_supply::Role,
    runtime_session::{
        compose_role, seed_instructions, send_conversation_text, start_with_recovery,
        HistorySession, RecoveryStartup, RuntimeSession,
    },
    util::{opaque_id, sha256_hex},
};
use serde_json::{json, Value};
use std::{
    path::PathBuf,
    sync::{Arc, Mutex},
    time::{Duration, Instant},
};
const GATE: &str = "parent-authorized-0160-one-greeting";
const MODEL: &str = "gpt-6.1-sol";
const BINARY_SHA: &str = "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b";
const REPLY: &str = "Hello from the synthetic backend smoke.";
const PROMPT: &str = "Reply with exactly: Hello from the synthetic backend smoke. Do not use tools, read files, delegate, or take external actions.";
type ProbeResult<T> = Result<T, &'static str>;
struct Probe {
    root: PathBuf,
    host: Arc<Host>,
}
impl Drop for Probe {
    fn drop(&mut self) {
        // Existing production stop bounds the normal process-group shutdown.
        if !matches!(self.host.state().as_str(), "absent" | "refused" | "stopped") {
            let _ = self.host.stop("opt-in-backend-probe", "probe cleanup");
        }
        // Never remove or modify the Parent-controlled authenticated Codex home.
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn required_path(key: &str) -> ProbeResult<PathBuf> {
    let path = PathBuf::from(std::env::var_os(key).ok_or("required Parent path absent")?);
    if !path.is_absolute() {
        return Err("Parent paths must be absolute");
    }
    Ok(path)
}
fn inspect_item(
    item: &Value,
    complete: bool,
    prompt_seen: &mut bool,
    reply: &mut Option<String>,
) -> ProbeResult<()> {
    match item["type"].as_str() {
        Some("userMessage") => {
            for input in item["content"].as_array().into_iter().flatten() {
                if input["type"] == "text" && input["text"] == PROMPT {
                    *prompt_seen = true;
                }
            }
        }
        Some("agentMessage") => {
            if complete {
                *reply = item["text"].as_str().map(str::to_string);
            }
        }
        Some("reasoning") => {}
        _ => return Err("unexpected native item; no authorization supplied"),
    }
    Ok(())
}
fn inspect_snapshot(
    snapshot: &Value,
    generation: &Value,
    selected: Option<(&str, &str)>,
    prompt_seen: &mut bool,
    reply: &mut Option<String>,
) -> ProbeResult<()> {
    if snapshot["generation"] != *generation || snapshot["state"] != "ready" {
        return Err("native generation/state changed");
    }
    if snapshot["serverRequests"]
        .as_array()
        .into_iter()
        .flatten()
        .any(|r| r["generation"] == *generation)
    {
        return Err("unexpected native request; no approval or input supplied");
    }
    for turn in snapshot["conversationTurns"]
        .as_array()
        .into_iter()
        .flatten()
    {
        if turn["generation"] != *generation {
            return Err("native snapshot turn generation mismatch");
        }
        let Some((thread_id, turn_id)) = selected else {
            return Err("unselected native conversation activity");
        };
        if turn["threadId"] != thread_id || turn["turnId"] != turn_id {
            return Err("native turn tuple mismatch");
        }
        for item in turn["nativeTurn"]["items"].as_array().into_iter().flatten() {
            inspect_item(
                item,
                turn["terminalEventObserved"] == true,
                prompt_seen,
                reply,
            )?;
        }
    }
    Ok(())
}
fn reply_is_exact(reply: Option<&str>) -> bool {
    reply == Some(REPLY)
}
fn inspect_frame(
    frame: &Value,
    generation: &Value,
    thread: &str,
    turn: &str,
    prompt_seen: &mut bool,
    reply: &mut Option<String>,
) -> ProbeResult<()> {
    if frame["generation"] != *generation {
        return Err("native frame generation mismatch");
    }
    let native = &frame["frame"];
    let Some(method) = native["method"].as_str() else {
        return Ok(());
    };
    let params = &native["params"];
    if matches!(method, "item/started" | "item/completed") {
        if params["threadId"] != thread || params["turnId"] != turn {
            return Err("native item tuple mismatch");
        }
        inspect_item(
            &params["item"],
            method == "item/completed",
            prompt_seen,
            reply,
        )?;
    } else if matches!(method, "turn/started" | "turn/completed") {
        if params["threadId"] != thread || params["turn"]["id"] != turn {
            return Err("native turn notification tuple mismatch");
        }
        for item in params["turn"]["items"].as_array().into_iter().flatten() {
            inspect_item(item, method == "turn/completed", prompt_seen, reply)?;
        }
    } else if method.starts_with("item/agentMessage/") || method.starts_with("item/reasoning/") {
        if params["threadId"] != thread || params["turnId"] != turn {
            return Err("native item delta tuple mismatch");
        }
    } else if method.starts_with("item/") {
        return Err("unexpected native item notification; no authorization supplied");
    }
    Ok(())
}

fn interrupt_actual_live_turn(host: &Host, generation: &Value, thread: &str, turn: &str) {
    let snapshot = host.snapshot();
    if snapshot["generation"] == *generation
        && snapshot["conversationTurns"]
            .as_array()
            .into_iter()
            .flatten()
            .any(|t| {
                t["generation"] == *generation
                    && t["threadId"] == thread
                    && t["turnId"] == turn
                    && t["nativeTurn"]["status"] == "inProgress"
                    && t["terminalEventObserved"] != true
                    && t["observationEnded"] != true
            })
    {
        let _ = host.turn_interrupt(generation, thread, turn); // never a grant or human act
    }
}

#[test]
#[ignore = "Parent only: explicit opt-in, authorized auth home and inherited-policy/medium assessment required"]
fn parent_authorized_stock_native_one_greeting() -> ProbeResult<()> {
    // Gate precedes path lookup, scratch setup, supplier execution or auth access.
    if std::env::var("CHIRALITY_RUN_NATIVE_BACKEND_SMOKE")
        .ok()
        .as_deref()
        != Some(GATE)
    {
        return Err("Parent opt-in absent; no smoke execution");
    }
    if std::env::var("CHIRALITY_NATIVE_SMOKE_CONFIG_ASSERTION")
        .ok()
        .as_deref()
        != Some("parent-controls-medium-and-native-policy")
    {
        return Err("Parent config/policy assertion absent; no smoke execution");
    }
    let binary = required_path("CHIRALITY_NATIVE_SMOKE_BIN")?;
    let auth_home = required_path("CHIRALITY_NATIVE_SMOKE_AUTH_HOME")?;
    let provider =
        std::env::var("CHIRALITY_NATIVE_SMOKE_PROVIDER").map_err(|_| "Parent provider absent")?;
    if provider.is_empty() {
        return Err("Parent provider empty");
    }
    let root = std::env::temp_dir()
        .join(opaque_id("native-backend-smoke-").map_err(|_| "scratch identity failed")?);
    std::fs::create_dir(&root).map_err(|_| "scratch creation failed")?;
    let probe = Probe {
        root,
        host: Arc::new(Host::new()),
    };
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        std::fs::set_permissions(&probe.root, std::fs::Permissions::from_mode(0o700))
            .map_err(|_| "scratch privacy setup failed")?;
    }
    let workspace = probe.root.join("workspace");
    let app_data = probe.root.join("app-data");
    let instruction_root = app_data.join("instructions");
    let probe_template = probe.root.join("version-probe-XXXXXX");
    std::fs::create_dir(&workspace).map_err(|_| "workspace setup failed")?;
    // LOOP requires an actual mktemp -d Codex probe home, not a mkdir lookalike.
    let temporary = std::process::Command::new("mktemp")
        .arg("-d")
        .arg(&probe_template)
        .stdin(std::process::Stdio::null())
        .output()
        .map_err(|_| "mktemp probe-home command failed")?;
    if !temporary.status.success() {
        return Err("mktemp probe-home creation failed");
    }
    let native_path = temporary
        .stdout
        .strip_suffix(b"\n")
        .ok_or("mktemp probe-home path missing newline")?;
    #[cfg(unix)]
    let probe_home = {
        use std::os::unix::ffi::OsStringExt;
        PathBuf::from(std::ffi::OsString::from_vec(native_path.to_vec()))
    };
    #[cfg(not(unix))]
    let probe_home = PathBuf::from(
        std::str::from_utf8(native_path).map_err(|_| "mktemp path encoding unsupported")?,
    );
    if !probe_home.starts_with(&probe.root) {
        return Err("mktemp probe-home path outside owned scratch");
    }
    seed_instructions(&instruction_root).map_err(|_| "isolated guidance seed failed")?;
    let composition = compose_role(&instruction_root, Some(Role::HELP_HUMAN))
        .map_err(|_| "guidance composition failed")?;
    composition
        .verify()
        .map_err(|_| "guidance identity verification failed")?;
    let mut config = HostConfig::new(binary, auth_home, probe_home, workspace.clone());
    config.expected_sha256 = Some(BINARY_SHA.into());
    config.allow_unverified_dev = true; // approved main binary is not full supplier qualification
    config.wait_limit = Duration::from_secs(15);
    // No model/provider/effort/approval/sandbox/plugins override is added to Parent config.
    let startup = Mutex::new(RecoveryStartup::default());
    let ready = start_with_recovery(
        &probe.host,
        &startup,
        Ok(&app_data),
        Some(&config.codex_home),
        || probe.host.start(&config, "opt-in-backend-probe"),
    )
    .map_err(|_| "production supplier startup failed; details private")?;
    if startup.lock().unwrap().snapshot()["state"] != "configured" {
        return Err("private scratch ledger initialization not configured");
    }
    if ready["versionIdentity"]["observedVersionLabel"] != "codex-cli 0.160.0" {
        return Err("native supplier label mismatch");
    }
    let generation = ready["generation"].clone();
    let mut native_prompt_seen = false;
    let mut selected_reply = None;
    inspect_snapshot(
        &ready,
        &generation,
        None,
        &mut native_prompt_seen,
        &mut selected_reply,
    )?;
    let workspace_text = workspace
        .to_str()
        .ok_or("non-Unicode workspace unsupported by current thread API")?;
    // Exact primary-start orchestration used by lib.rs at checkpoint 24f807:
    // genuine source dispatch, one HistorySession preparation/reconcile, admission.
    let mut history = HistorySession::default();
    let supply_ref = opaque_id("sup:").map_err(|_| "start supply identity failed")?;
    let receipt = probe
        .host
        .thread_start_with_guidance_dispatch(
            &generation,
            workspace_text,
            MODEL,
            &provider,
            &composition.text,
        )
        .map_err(|_| "production primary dispatch failed; details private")?;
    history
        .start_dispatched(receipt.clone(), &composition, &supply_ref)
        .map_err(|_| "shared start preparation failed; details private")?;
    let start_evidence = probe
        .host
        .source_request_wait(&receipt, Duration::from_secs(20))
        .map_err(|_| "production source wait failed; details private")?;
    history.reconcile(&probe.host);
    if !history.start_admitted(&receipt) {
        return Err("shared primary start not operationally admitted");
    }
    let source = probe
        .host
        .source_request(&generation, receipt.request_id())
        .map_err(|_| "genuine source request unavailable")?;
    if source.request_ref() != receipt.request_ref()
        || start_evidence["writeResult"] != "written"
        || start_evidence["sourceCurrent"] != true
        || start_evidence["requestIdentity"] != *receipt.request_id()
        || start_evidence["sentFrame"] != *receipt.attempted_frame()
        || start_evidence["sentFrame"]["params"]["developerInstructions"] != composition.text
    {
        return Err("primary start source receipt does not bind actual dispatched guidance");
    }
    let thread_response = start_evidence["response"].clone();
    let result = &thread_response["result"];
    if result["model"] != MODEL || result["modelProvider"] != provider {
        return Err("native destination differs from requested Parent selection");
    }
    if result["reasoningEffort"] != "medium" {
        return Err("medium effort not natively reported; no effort inferred or overridden");
    }
    let thread = result["thread"]["id"]
        .as_str()
        .ok_or("native thread identity absent")?;
    let home = generation["home"]
        .as_str()
        .ok_or("native home identity absent")?;
    let binding = history
        .binding(home, thread)
        .ok_or("shared original role binding absent")?;
    let role_binding = binding.evidence();
    let role_in_force = history.role(home, thread);
    if binding.supply_ref() != supply_ref
        || binding.home() != home
        || binding.thread() != thread
        || role_binding["binding"]["original"]["identity"]
            != composition.carried["developerInstructions"]["content"]
        || role_binding["adoption"] != "unknown"
        || role_in_force["standing"] != "app-observed"
        || role_in_force["role"] != "HELP_HUMAN"
    {
        return Err("shared original role binding does not match source-admitted thread");
    }
    if !probe.host.snapshot()["threads"]
        .as_array()
        .into_iter()
        .flatten()
        .any(|t| t["generation"] == generation && t["threadId"] == thread)
    {
        return Err("source-admitted operational thread absent");
    }
    inspect_snapshot(
        &probe.host.snapshot(),
        &generation,
        None,
        &mut native_prompt_seen,
        &mut selected_reply,
    )?;
    let turn_response = send_conversation_text(
        &probe.host.snapshot(),
        &generation,
        thread,
        PROMPT,
        |g, t, text| probe.host.turn_start_text(g, t, text),
    )
    .map_err(|_| "production turn/start failed; details private")?;
    let turn = turn_response["result"]["turn"]["id"]
        .as_str()
        .ok_or("native turn identity absent")?;
    let mut receiver = RuntimeSession::default();
    let deadline = Instant::now() + Duration::from_secs(45);
    let outcome = (|| -> ProbeResult<String> {
        loop {
            let (cursor, position) = receiver.cursor();
            let observation = probe.host.observe(cursor, position);
            inspect_snapshot(
                &observation["snapshot"],
                &generation,
                Some((thread, turn)),
                &mut native_prompt_seen,
                &mut selected_reply,
            )?;
            for frame in observation["frames"].as_array().into_iter().flatten() {
                inspect_frame(
                    frame,
                    &generation,
                    thread,
                    turn,
                    &mut native_prompt_seen,
                    &mut selected_reply,
                )?;
            }
            receiver.receive(&observation); // actual production receiving path; raw data stays in memory
            let terminal = observation["snapshot"]["conversationTurns"]
                .as_array()
                .into_iter()
                .flatten()
                .find(|t| {
                    t["generation"] == generation
                        && t["threadId"] == thread
                        && t["turnId"] == turn
                        && t["terminalEventObserved"] == true
                });
            if let Some(terminal) = terminal {
                let status = terminal["nativeTurn"]["status"]
                    .as_str()
                    .ok_or("terminal status absent")?;
                if status != "completed" {
                    return Err("native terminal status was not completed; details private");
                }
                if !native_prompt_seen {
                    return Err(
                        "native received user text not observed; client write is not receipt proof",
                    );
                }
                if !reply_is_exact(selected_reply.as_deref()) {
                    return Err(
                        "reply was not the exact synthetic greeting; private text not published",
                    );
                }
                return Ok(status.into());
            }
            if Instant::now() >= deadline {
                return Err("native terminal wait deadline exceeded");
            }
            std::thread::sleep(Duration::from_millis(100));
        }
    })();
    if outcome.is_err() {
        interrupt_actual_live_turn(&probe.host, &generation, thread, turn);
    }
    let terminal = outcome?;
    let observed_reply = selected_reply.ok_or("selected native reply absent")?;
    let ledger_path = chirality_app_v4_lib::runtime_session::reviewed_ledger_path(&app_data);
    let ledger_bytes = std::fs::read(&ledger_path).map_err(|_| "scratch ledger read failed")?;
    let rows: Vec<Value> = ledger_bytes
        .split(|b| *b == b'\n')
        .filter(|b| !b.is_empty())
        .map(serde_json::from_slice)
        .collect::<Result<_, _>>()
        .map_err(|_| "scratch ledger parse failed")?;
    if rows
        .iter()
        .filter(|row| row["kind"] == "session_started")
        .count()
        != 1
    {
        return Err("scratch ledger session fact count mismatch");
    }
    if String::from_utf8_lossy(&ledger_bytes).contains(PROMPT)
        || String::from_utf8_lossy(&ledger_bytes).contains(REPLY)
    {
        return Err("conversation payload appeared in App pointer ledger");
    }
    if probe.host.snapshot()["recovery"]["oldRequestsAnswerable"] != false {
        return Err("ledger answerability limit absent");
    }
    probe
        .host
        .stop("opt-in-backend-probe", "one greeting probe finished")
        .map_err(|_| "production process-group cleanup failed; details private")?;
    if probe.host.snapshot()["lifecycle"]
        .as_array()
        .and_then(|v| v.last())
        .map(|e| &e["descendants"]["surviving"])
        != Some(&json!(0))
    {
        return Err("process-group cleanup not reported complete");
    }
    // Publish only allowlisted synthetic output and source/model/role/outcome facts.
    println!(
        "{}",
        json!({"probe":"real-production-backend-one-greeting","reply":observed_reply,"nativeReceivedTextObserved":true,"nativeTerminalEventObserved":true,"nativeTerminalStatus":terminal,
        "requestedModel":MODEL,"reportedModel":MODEL,"reportedReasoningEffort":"medium","providerMatchedParentSelection":true,
        "requestedRole":"HELP_HUMAN","roleAdoption":"not established","primaryStartPath":"production dispatch/HistorySession reconcile/finish","genuineSourceRequestBound":true,"sharedOriginalRoleBindingObserved":true,"compositionIdentity":composition.carried["developerInstructions"]["content"],
        "ledgerSessionEntries":1,"ledgerStanding":"App-observed pointers; not native act proof","supplierQualification":"unverified-development",
        "source":{"smoke":sha256_hex(include_bytes!("native_backend_smoke.rs")),"hosting":sha256_hex(include_bytes!("../src/hosting.rs")),"runtimeSession":sha256_hex(include_bytes!("../src/runtime_session.rs")),"nativeRequests":sha256_hex(include_bytes!("../src/native_requests.rs")),"lib":sha256_hex(include_bytes!("../src/lib.rs")),"roleLifecycle":sha256_hex(include_bytes!("../src/role_lifecycle.rs")),"nativeHistory":sha256_hex(include_bytes!("../src/native_history.rs")),"lockfile":sha256_hex(include_bytes!("../Cargo.lock"))}})
    );
    Ok(())
}

#[cfg(test)]
mod pure_smoke_evidence_tests {
    use super::*;
    fn generation() -> Value {
        json!({"appSession":"synthetic","home":"synthetic-home","spawnCounter":1})
    }
    fn user_item() -> Value {
        json!({"id":"user","type":"userMessage","content":[{"type":"text","text":PROMPT,"text_elements":[]}]})
    }
    #[test]
    fn foreign_same_thread_turn_cannot_supply_selected_prompt_reply_or_terminal_evidence() {
        let generation = generation();
        // Original case: sibling turn supplies echo/reply; selected terminal has none.
        let snapshot = json!({"generation":generation,"state":"ready","serverRequests":[],"conversationTurns":[
            {"generation":generation,"threadId":"thread","turnId":"foreign","terminalEventObserved":true,"nativeTurn":{"id":"foreign","status":"completed","items":[user_item(),{"id":"agent","type":"agentMessage","text":REPLY}]}},
            {"generation":generation,"threadId":"thread","turnId":"selected","terminalEventObserved":true,"nativeTurn":{"id":"selected","status":"completed","items":[]}}]});
        let mut prompt_seen = false;
        let mut reply = None;
        assert_eq!(
            inspect_snapshot(
                &snapshot,
                &generation,
                Some(("thread", "selected")),
                &mut prompt_seen,
                &mut reply
            )
            .unwrap_err(),
            "native turn tuple mismatch"
        );
        assert!(!prompt_seen);
        assert!(reply.is_none());
        for (frame_generation, thread, turn) in [
            (generation.clone(), "thread", "foreign"),
            (generation.clone(), "foreign-thread", "selected"),
            (
                json!({"appSession":"other","home":"synthetic-home","spawnCounter":1}),
                "thread",
                "selected",
            ),
        ] {
            let frame = json!({"generation":frame_generation,"frame":{"method":"item/completed","params":{"threadId":thread,"turnId":turn,"item":user_item()}}});
            assert!(inspect_frame(
                &frame,
                &generation,
                "thread",
                "selected",
                &mut prompt_seen,
                &mut reply
            )
            .is_err());
            assert!(!prompt_seen);
            assert!(reply.is_none());
        }
        let selected = json!({"generation":generation,"frame":{"method":"item/completed","params":{"threadId":"thread","turnId":"selected","item":user_item()}}});
        inspect_frame(
            &selected,
            &generation,
            "thread",
            "selected",
            &mut prompt_seen,
            &mut reply,
        )
        .unwrap();
        assert!(prompt_seen);
    }
    #[test]
    fn reply_equality_is_byte_exact_and_never_trims_or_publishes_a_substitute() {
        assert!(reply_is_exact(Some(REPLY)));
        assert!(!reply_is_exact(None));
        for observed in [
            format!("{REPLY}\n"),
            format!(" {REPLY}"),
            format!("{REPLY} "),
            format!("{REPLY}\r\n"),
        ] {
            assert!(!reply_is_exact(Some(&observed)));
        }
    }
}
