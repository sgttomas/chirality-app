//! Parent-only real supplier/provider probe. Ordinary tests never run this.
//! No raw native journal, prompts, account/config/auth data is published.
use chirality_app_v4_lib::{
    hosting::{Host, HostConfig},
    native_history::{Direction, HistoryQuery, NativeHistory},
    role_supply::Role,
    runtime_session::{
        compose_role, seed_instructions, send_conversation_text, start_with_recovery,
        HistorySession, RecoveryStartup, RuntimeSession,
    },
    util::{opaque_id, sha256_hex},
};
use serde_json::{json, Value};
use std::{
    path::{Path, PathBuf},
    sync::{Arc, Mutex},
    time::{Duration, Instant},
};
const GATE: &str = "parent-authorized-0160-one-greeting";
const MODEL: &str = "gpt-6.1-sol";
/// Local deterministic route: a distinct gate, an invented model and a private
/// loopback Responses fixture. No inference, credential or owner home is used.
const LOCAL_GATE: &str = "parent-authorized-0160-local-responses-fixture";
const FIXTURE_MODEL: &str = "chirality-fixture-model";
const FIXTURE_PROVIDER: &str = "chirality-smoke-local";
const BINARY_SHA: &str = "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b";
const REPLY: &str = "Hello from the synthetic backend smoke.";
const PROMPT: &str = "Reply with exactly: Hello from the synthetic backend smoke. Do not use tools, read files, delegate, or take external actions.";
type ProbeResult<T> = Result<T, &'static str>;

/// The two routes one greeting can take. `Parent` is the existing authenticated
/// cloud route, unchanged. `LocalFixture` uses a fresh private Codex home inside
/// the owned scratch and the deterministic loopback Responses fixture below.
enum Route {
    Parent {
        binary: PathBuf,
        auth_home: PathBuf,
        provider: String,
    },
    LocalFixture {
        binary: PathBuf,
    },
}

/// The deterministic loopback Responses peer (shared test support). For the
/// greeting it answers every `POST …/responses` with one message carrying `REPLY`.
#[allow(dead_code)]
#[path = "support/responses_fixture.rs"]
mod responses_fixture;
use responses_fixture::ResponsesFixture;
fn greeting_fixture() -> ProbeResult<ResponsesFixture> {
    ResponsesFixture::start(
        vec![vec![responses_fixture::message("msg_fixture_1", REPLY)]],
        vec![("prompt", PROMPT.to_string())],
    )
}
/// A fresh private Codex home inside the owned scratch: exactly the App's own
/// local provider literal (`provider_create.rs`), no auth, no owner settings.
fn write_fixture_home(home: &Path, base_url: &str) -> ProbeResult<()> {
    std::fs::create_dir(home).map_err(|_| "fixture Codex home creation failed")?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        std::fs::set_permissions(home, std::fs::Permissions::from_mode(0o700))
            .map_err(|_| "fixture Codex home privacy setup failed")?;
    }
    let config = format!(
        "model = \"{FIXTURE_MODEL}\"\nmodel_provider = \"{FIXTURE_PROVIDER}\"\n\n[model_providers.{FIXTURE_PROVIDER}]\nname = \"Chirality smoke fixture\"\nbase_url = \"{base_url}\"\nwire_api = \"responses\"\nrequires_openai_auth = false\n"
    );
    std::fs::write(home.join("config.toml"), config).map_err(|_| "fixture Codex config write failed")
}
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
/// Reads the finished turn back through the existing public history path
/// (`NativeHistory` factories, `Host::history_dispatch`/`history_wait`, and the
/// view's own `receive` validation) and checks the prompt and reply items.
fn read_back_history(
    host: &Host,
    generation: &Value,
    home: &str,
    thread: &str,
    turn: &str,
) -> ProbeResult<Value> {
    let mut view =
        NativeHistory::new(home, generation.clone()).map_err(|_| "history view setup failed")?;
    let fetch = |view: &mut NativeHistory, query: HistoryQuery| -> ProbeResult<Value> {
        let dispatch = host
            .history_dispatch(&query)
            .map_err(|_| "history read dispatch failed")?;
        let evidence = host
            .history_wait(&dispatch, Duration::from_secs(10))
            .map_err(|_| "history read wait failed")?;
        if evidence["response"].get("error").is_some() {
            return Err("history read answered with an error");
        }
        let result = evidence["response"]["result"].clone();
        view.receive(&query, home, generation, &result)
            .map_err(|_| "history view refused the native result")?;
        Ok(result)
    };
    let query = view
        .list_threads(None, Direction::Desc)
        .map_err(|_| "history list query failed")?;
    let list = fetch(&mut view, query)?;
    if !list["data"].as_array().into_iter().flatten().any(|t| t["id"] == thread) {
        return Err("history list does not contain the conversation");
    }
    view.select(thread).map_err(|_| "history selection failed")?;
    let query = view
        .turns_page(None, Direction::Desc)
        .map_err(|_| "history turns query failed")?;
    let turns = fetch(&mut view, query)?;
    if !turns["data"].as_array().into_iter().flatten().any(|t| t["id"] == turn && t["status"] == "completed") {
        return Err("history turns do not contain the completed turn");
    }
    let query = view
        .items_page(turn, None, Direction::Asc)
        .map_err(|_| "history items query failed")?;
    let items = fetch(&mut view, query)?;
    // `thread/items/list` entries wrap each item: {item, turnId, startedAtMs, completedAtMs}.
    let items: Vec<Value> = items["data"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|entry| entry["turnId"] == turn)
        .map(|entry| entry["item"].clone())
        .collect();
    let prompt = items.iter().any(|i| {
        i["type"] == "userMessage"
            && i["content"].as_array().into_iter().flatten().any(|c| c["type"] == "text" && c["text"] == PROMPT)
    });
    let reply = items.iter().any(|i| i["type"] == "agentMessage" && i["text"] == REPLY);
    if !prompt || !reply {
        // Structure only (types and field names), never text, for diagnosis.
        let shape: Vec<Value> = items.iter().map(|i| json!({"type":i["type"],"keys":i.as_object().map(|o| o.keys().cloned().collect::<Vec<_>>()),
            "contentTypes":i["content"].as_array().map(|c| c.iter().map(|x| x["type"].clone()).collect::<Vec<_>>())})).collect();
        eprintln!("history item shape: {}", json!(shape));
        return Err("history items do not contain the exact prompt and reply");
    }
    Ok(json!({"threadListed":true,"turnCompleted":true,"items":items.len(),"promptItem":true,"replyItem":true,
        "path":"NativeHistory list/select/turns/items via Host::history_dispatch"}))
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
        let _ = host.turn_interrupt(generation, thread, turn, "H-acct", &chirality_app_v4_lib::stop_records::person("")); // never a grant or human act
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
    run_one_greeting(Route::Parent {
        binary,
        auth_home,
        provider,
    })
}

#[test]
#[ignore = "Parent only: explicit local Responses fixture opt-in; no model, credential or owner home"]
fn parent_authorized_stock_native_local_responses_fixture() -> ProbeResult<()> {
    // Distinct gate; precedes path lookup, scratch setup or supplier execution.
    if std::env::var("CHIRALITY_RUN_NATIVE_BACKEND_SMOKE")
        .ok()
        .as_deref()
        != Some(LOCAL_GATE)
    {
        return Err("Parent local fixture opt-in absent; no smoke execution");
    }
    let binary = required_path("CHIRALITY_NATIVE_SMOKE_BIN")?;
    run_one_greeting(Route::LocalFixture { binary })
}

fn run_one_greeting(route: Route) -> ProbeResult<()> {
    let binary = match &route {
        Route::Parent { binary, .. } | Route::LocalFixture { binary } => binary.clone(),
    };
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
    // The local route's fixture is declared after `probe`, so it stops first.
    let (codex_home, model, provider, fixture) = match &route {
        Route::Parent {
            auth_home,
            provider,
            ..
        } => (auth_home.clone(), MODEL.to_string(), provider.clone(), None),
        Route::LocalFixture { .. } => {
            let fixture = greeting_fixture()?;
            let home = probe.root.join("fixture-codex-home");
            write_fixture_home(&home, &fixture.base_url())?;
            (
                home,
                FIXTURE_MODEL.to_string(),
                FIXTURE_PROVIDER.to_string(),
                Some(fixture),
            )
        }
    };
    let mut config = HostConfig::new(binary, codex_home, probe_home, workspace.clone());
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
            &model,
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
    if result["model"] != model.as_str() || result["modelProvider"] != provider.as_str() {
        return Err("native destination differs from requested Parent selection");
    }
    if matches!(route, Route::Parent { .. }) && result["reasoningEffort"] != "medium" {
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
    // Local route: the existing public history path reads the turn back.
    let history_readback = if fixture.is_some() {
        Some(read_back_history(&probe.host, &generation, home, thread, turn)?)
    } else {
        None
    };
    // The recovery ledger is database-backed (recovery::database_path); its
    // recorded entries are read through the running host's own ledger handle,
    // not a second opener or the retired JSON-lines file.
    let recorded = probe.host.recorded_recovery_entries();
    let rows: Vec<Value> = recorded
        .as_array()
        .cloned()
        .ok_or("scratch ledger entries unavailable")?;
    let ledger_bytes = recorded.to_string().into_bytes();
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
    let source = json!({"smoke":sha256_hex(include_bytes!("native_backend_smoke.rs")),"hosting":sha256_hex(include_bytes!("../src/hosting.rs")),"runtimeSession":sha256_hex(include_bytes!("../src/runtime_session.rs")),"nativeRequests":sha256_hex(include_bytes!("../src/native_requests.rs")),"lib":sha256_hex(include_bytes!("../src/lib.rs")),"roleLifecycle":sha256_hex(include_bytes!("../src/role_lifecycle.rs")),"nativeHistory":sha256_hex(include_bytes!("../src/native_history.rs")),"lockfile":sha256_hex(include_bytes!("../Cargo.lock"))});
    let Some(fixture) = fixture else {
        // Publish only allowlisted synthetic output and source/model/role/outcome facts.
        println!(
            "{}",
            json!({"probe":"real-production-backend-one-greeting","reply":observed_reply,"nativeReceivedTextObserved":true,"nativeTerminalEventObserved":true,"nativeTerminalStatus":terminal,
            "requestedModel":MODEL,"reportedModel":MODEL,"reportedReasoningEffort":"medium","providerMatchedParentSelection":true,
            "requestedRole":"HELP_HUMAN","roleAdoption":"not established","primaryStartPath":"production dispatch/HistorySession reconcile/finish","genuineSourceRequestBound":true,"sharedOriginalRoleBindingObserved":true,"compositionIdentity":composition.carried["developerInstructions"]["content"],
            "ledgerSessionEntries":1,"ledgerStanding":"App-observed pointers; not native act proof","supplierQualification":"unverified-development",
            "source":source})
        );
        return Ok(());
    };
    // Local route: every request the app-server made reached this private
    // loopback fixture, and the turn's request carried the model and prompt.
    let requests = fixture.requests();
    drop(fixture);
    let responses: Vec<&Value> = requests.iter().filter(|r| r["answered"] == "sse").collect();
    if responses.is_empty() {
        return Err("no Responses request reached the private fixture");
    }
    if requests.iter().any(|r| r["loopbackPeer"] != true || r["parsed"] != true) {
        return Err("a fixture request was not a parsed loopback request");
    }
    if responses.iter().any(|r| {
        r["contentEncoding"] != Value::Null
            || r["bodyComplete"] != true
            || r["model"] != FIXTURE_MODEL
            || r["stream"] != true
    }) {
        return Err("a Responses request did not carry the fixture model, streaming and an uncompressed body");
    }
    if !responses.iter().any(|r| r["markers"]["prompt"] == true) {
        return Err("no Responses request carried the synthetic prompt");
    }
    println!(
        "{}",
        json!({"probe":"real-production-backend-local-responses-fixture","reply":observed_reply,"replyExact":true,"nativeReceivedTextObserved":true,"nativeTerminalEventObserved":true,"nativeTerminalStatus":terminal,
        "requestedModel":FIXTURE_MODEL,"reportedModel":result["model"],"reportedModelProvider":result["modelProvider"],"reportedReasoningEffort":result["reasoningEffort"],
        "requestedRole":"HELP_HUMAN","roleAdoption":"not established","primaryStartPath":"production dispatch/HistorySession reconcile/finish","genuineSourceRequestBound":true,"sharedOriginalRoleBindingObserved":true,"compositionIdentity":composition.carried["developerInstructions"]["content"],
        "historyReadback":history_readback,
        "fixture":{"responsesRequests":responses.len(),"otherRequests":requests.iter().filter(|r| r["answered"] != "sse").map(|r| json!({"method":r["method"],"path":r["path"]})).collect::<Vec<_>>(),"allLoopback":true},
        "ledgerSessionEntries":1,"ledgerStanding":"App-observed pointers; not native act proof","supplierQualification":"unverified-development",
        "standing":"deterministic loopback Responses fixture; no inference, model, credential or owner home; not model, J1/J2 or native qualification",
        "source":source})
    );
    Ok(())
}

#[cfg(test)]
mod pure_smoke_evidence_tests {
    use super::*;
    use std::{
        io::{Read, Write},
        net::TcpStream,
    };
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
    // The local fixture alone (no Codex): a Responses POST gets the canned SSE
    // stream ending in response.completed; anything else gets 404; facts only.
    #[test]
    fn local_responses_fixture_answers_canned_sse_and_records_request_facts() {
        let fixture = greeting_fixture().unwrap();
        let exchange = |request: String| {
            let mut stream = TcpStream::connect(("127.0.0.1", fixture.port)).unwrap();
            stream.write_all(request.as_bytes()).unwrap();
            let mut answer = String::new();
            stream.read_to_string(&mut answer).unwrap();
            answer
        };
        let body = json!({"model":FIXTURE_MODEL,"stream":true,"input":[{"role":"user","content":[{"type":"input_text","text":PROMPT}]}]}).to_string();
        let answer = exchange(format!("POST /v1/responses HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Type: application/json\r\nContent-Length: {}\r\n\r\n{}", body.len(), body));
        assert!(answer.starts_with("HTTP/1.1 200 OK\r\n") && answer.contains("Content-Type: text/event-stream"), "{answer}");
        let completed = answer.find("event: response.completed").unwrap();
        assert!(answer.find("event: response.output_item.done").unwrap() < completed);
        assert!(answer.contains(&format!("\"text\":{}", json!(REPLY))));
        let other = exchange("GET /v1/models HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n".into());
        assert!(other.starts_with("HTTP/1.1 404"), "{other}");
        let deadline = Instant::now() + Duration::from_secs(5);
        while fixture.requests().len() < 2 && Instant::now() < deadline {
            std::thread::sleep(Duration::from_millis(10));
        }
        let requests = fixture.requests();
        assert_eq!(requests.len(), 2);
        assert_eq!(requests[0]["answered"], "sse");
        assert_eq!(requests[0]["model"], FIXTURE_MODEL);
        assert_eq!(requests[0]["stream"], true);
        assert_eq!(requests[0]["markers"]["prompt"], true);
        assert_eq!(requests[0]["scriptStep"], 0);
        assert_eq!(requests[0]["loopbackPeer"], true);
        assert_eq!(requests[1]["answered"], "404");
        assert_eq!(requests[1]["path"], "/v1/models");
        assert!(!requests[0].to_string().contains("input_text"), "only facts are kept, never the body");
        assert!(fixture.base_url().starts_with("http://127.0.0.1:"));
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
