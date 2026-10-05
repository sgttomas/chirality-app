//! Chirality App v4 walking skeleton: Tauri 2 main process (V4-ARC-02).
//!
//! Modules and the contract sections they implement are listed in ../README.md.
//! The Rust main process owns the Codex child, the record writing and the act
//! capture (HOSTING §12 O-1 "Rust envelope core"; AAC §6.2 under R17-5). The
//! webview only reads snapshots and asks the host to act.

pub mod access;
pub mod act_control;
pub mod canonical;
pub mod catalog;
pub mod decision_view;
pub mod external_observation;
pub mod hosting;
pub mod native_items;
pub mod native_requests;
pub mod receiving;
pub mod recorder;
pub mod records;
pub mod recovery;
pub mod role_supply;
pub mod runtime_session;
pub mod schema_validation;
pub mod storage;
pub mod util;

use act_control::{ActControl, InputSource};
use hosting::{Host, HostConfig};
use serde_json::{json, Value};
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use tauri::{Manager, State};
use tauri_plugin_dialog::{DialogExt, MessageDialogButtons, MessageDialogKind};

pub struct AppState {
    host: Arc<Host>,
    host_config: Result<HostConfig, String>,
    workspace: Option<PathBuf>,
    act: Mutex<Option<ActControl>>,
    person_name: Mutex<Option<String>>,
    runtime: Mutex<runtime_session::RuntimeSession>,
    access_selection: Mutex<Option<access::ConversationSelection>>,
    instructions_root: Mutex<Result<PathBuf, String>>,
    app_user_data_root: Mutex<Result<PathBuf, String>>,
    recovery_startup: Arc<Mutex<runtime_session::RecoveryStartup>>,
    role_supply_status: Mutex<Value>,
    external_observation: Mutex<runtime_session::ExternalObservationSession>,
}

/// A fresh probe home for the label probe (HOSTING §7.2 H-probe), in the temp directory.
fn probe_home() -> PathBuf {
    let n = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos();
    let p = std::env::temp_dir().join(format!("cxp.{}.{}", std::process::id(), n));
    let _ = std::fs::create_dir_all(&p);
    p
}

/// Configuration comes only from the environment; no path is built in (owner rule).
pub fn host_config_from_env(workspace: Option<&PathBuf>) -> Result<HostConfig, String> {
    let bin = std::env::var("CHIRALITY_CODEX_BIN").map_err(|_| {
        "CHIRALITY_CODEX_BIN is not set: no supplier distribution resolved".to_string()
    })?;
    let home = std::env::var("CHIRALITY_CODEX_HOME").map_err(|_| {
        "CHIRALITY_CODEX_HOME is not set: no App-owned Codex home given".to_string()
    })?;
    let cwd = workspace.cloned().unwrap_or_else(std::env::temp_dir);
    let mut cfg = HostConfig::new(bin.into(), home.into(), probe_home(), cwd);
    cfg.expected_sha256 = std::env::var("CHIRALITY_CODEX_EXPECTED_SHA256").ok();
    cfg.allow_unverified_dev = std::env::var("CHIRALITY_ALLOW_UNVERIFIED")
        .map(|v| v == "1")
        .unwrap_or(false);
    Ok(cfg)
}

#[tauri::command]
fn host_status(state: State<'_, AppState>) -> Value {
    let mut runtime = state.runtime.lock().unwrap();
    let (generation, position) = runtime.cursor();
    let observation = state.host.observe(generation, position);
    let received = runtime.receive(&observation);
    let mut s = observation["snapshot"].clone();
    for (key, value) in received.as_object().unwrap() {
        s[key] = value.clone();
    }
    s["accessSelection"] = state
        .access_selection
        .lock()
        .unwrap()
        .as_ref()
        .map(access::ConversationSelection::snapshot)
        .map_or(Value::Null, |v| v);
    s["recoveryInitialization"] = state.recovery_startup.lock().unwrap().snapshot();
    if let Err(e) = &state.host_config {
        s["configurationProblem"] = json!(e);
    }
    s["roleSupply"] = state.role_supply_status.lock().unwrap().clone();
    s["externalObservation"] = state.external_observation.lock().unwrap().snapshot();
    if let Err(e) = &*state.instructions_root.lock().unwrap() {
        s["instructionsProblem"] = json!(e);
    }
    s
}

#[tauri::command(async)]
fn host_start(state: State<'_, AppState>) -> Result<Value, String> {
    let cfg = state.host_config.clone()?;
    let root = state.app_user_data_root.lock().unwrap().clone();
    runtime_session::start_with_recovery(
        &state.host,
        &state.recovery_startup,
        root.as_deref().map_err(String::as_str),
        Some(&cfg.codex_home),
        || state.host.start(&cfg, "the person"),
    )
}

#[tauri::command(async)]
fn host_stop(state: State<'_, AppState>) -> Result<Value, String> {
    state.host.stop("the person", "Stop Codex")
}

#[tauri::command(async)]
fn thread_start(
    state: State<'_, AppState>,
    model: String,
    model_provider: String,
    entry_id: String,
    role: Option<role_supply::Role>,
) -> Result<Value, String> {
    let cwd = state
        .host_config
        .as_ref()
        .map(|c| c.cwd.display().to_string())
        .map_err(|e| e.clone())?;
    if !matches!(entry_id.as_str(), "chatgpt-account" | "local-provider") {
        return Err("entry unavailable: this path owns only the configured account home; API-key home not connected".into());
    }
    let root = state.instructions_root.lock().unwrap().clone()?;
    let composition = runtime_session::compose_role(&root, role)?;
    composition.verify()?;
    let generation = state.host.snapshot()["generation"].clone();
    let mut selection =
        access::ConversationSelection::new(&util::opaque_id("conversation:")?, &cwd)?;
    selection.choose(&entry_id, &model_provider, &model, false)?;
    selection.start_params(&generation, "account", false)?;
    // Serialize starts while leaving observer/status reads independent of transport wait.
    {
        let mut slot = state.access_selection.lock().unwrap();
        if slot
            .as_ref()
            .map(|s| s.snapshot()["state"] == "starting")
            .unwrap_or(false)
        {
            return Err("thread start in progress".into());
        }
        *slot = Some(selection);
    }
    *state.role_supply_status.lock().unwrap() = json!({"state":"starting","selection":role,"generation":generation,"carried":composition.carried,"adoption":"unknown","nativeChildRoles":composition.child_status(None,false)});
    let result =
        state
            .host
            .thread_start_with_guidance(&cwd, &model, &model_provider, &composition.text);
    *state.role_supply_status.lock().unwrap() = json!({"state":if result.is_ok(){"response-observed"}else{"start-failed-or-unknown"},"selection":role,"generation":generation,"carried":composition.carried,"adoption":"unknown","nativeChildRoles":composition.child_status(None,false)});
    let mut slot = state.access_selection.lock().unwrap();
    let selection = slot.as_mut().ok_or("selection unavailable")?;
    match &result {
        Ok(response) if state.host.snapshot()["generation"] == generation => {
            selection.started(&generation, &response["result"])?;
        }
        Ok(_) => {
            selection.start_failed("unknown: owning generation changed during thread start")?;
            return Err("owning generation changed during thread start".into());
        }
        Err(e) => {
            selection.start_failed(e)?;
        }
    }
    result
}

#[tauri::command(async)]
fn conversation_send_text(
    state: State<'_, AppState>,
    generation: Value,
    thread_id: String,
    text: String,
) -> Result<Value, String> {
    runtime_session::send_conversation_text(
        &state.host.snapshot(),
        &generation,
        &thread_id,
        &text,
        |generation, thread, text| state.host.turn_start_text(generation, thread, text),
    )
}

#[tauri::command(async)]
fn conversation_interrupt(
    state: State<'_, AppState>,
    generation: Value,
    thread_id: String,
    turn_id: String,
) -> Result<Value, String> {
    runtime_session::interrupt_conversation_turn(
        &state.host.snapshot(),
        &generation,
        &thread_id,
        &turn_id,
        |generation, thread, turn| state.host.turn_interrupt(generation, thread, turn),
    )
}

/// Paths come exclusively from native file selection; no path/origin is an IPC argument.
#[tauri::command(async)]
fn select_external_observation(
    app: tauri::AppHandle,
    state: State<'_, AppState>,
) -> Result<Value, String> {
    runtime_session::receive_external_selection(
        &state.external_observation,
        |stage| {
            let title = match stage {
                "catalog" => "Select person-supplied catalog JSON",
                "read" => "Select person-supplied read JSON",
                _ => "Select optional person-supplied counterpart JSON",
            };
            app.dialog()
                .file()
                .set_title(title)
                .add_filter("JSON documents", &["json"])
                .blocking_pick_file()
                .map(|file| {
                    file.into_path().map_err(|e| {
                        format!("Native selected file is not a local filesystem path: {e}")
                    })
                })
                .transpose()
        },
        || {
            app.dialog().message("Include an optional counterpart read document? This compares only supplied document content; host origin remains unverified.")
            .title("Chirality — supplied counterpart")
            .buttons(MessageDialogButtons::OkCancelCustom("Choose counterpart".into(),"No counterpart".into())).blocking_show()
        },
    )
}

/// Public reattachment is read-only and always uses the complete owning tuple.
#[tauri::command]
fn host_observe(state: State<'_, AppState>, generation: Value, after: u64) -> Value {
    state.host.observe(&generation, after)
}

/// Attribution consumes the Host's current atomic observation rather than the
/// last one-second UI poll. The returned context is frozen for confirmation.
fn current_actor_context(state: &AppState) -> (Value, Value) {
    let name = state.person_name.lock().unwrap().clone();
    let os = util::os_account();
    let mut runtime = state.runtime.lock().unwrap();
    let (generation, position) = runtime.cursor();
    let observation = state.host.observe(generation, position);
    let context = runtime.actor_context(&observation, name.as_deref(), os.as_deref());
    (observation["snapshot"].clone(), context)
}

/// No actor, origin, rule name or error path is exposed to the webview.
#[tauri::command(async)]
fn answer_native_request(
    app: tauri::AppHandle,
    state: State<'_, AppState>,
    generation: Value,
    request_id: Value,
    answer: Value,
) -> Result<Value, String> {
    let (snapshot, context) = current_actor_context(&state);
    let actor = runtime_session::actor_reference(
        context["displayName"].as_str(),
        context["osAccount"].as_str(),
        context["codexAccount"].as_str(),
    );
    let preview =
        runtime_session::answer_preview(&snapshot, &generation, &request_id, &answer, &actor)?;
    let confirmed = app
        .dialog()
        .message(format!(
            "Send this native request answer?\n{}",
            serde_json::to_string_pretty(&preview).map_err(|e| e.to_string())?
        ))
        .title("Chirality — answer native request")
        .kind(MessageDialogKind::Warning)
        .buttons(MessageDialogButtons::OkCancelCustom(
            "Send answer".into(),
            "Keep waiting".into(),
        ))
        .blocking_show();
    if !confirmed {
        return Ok(json!({"state":"dismissed","replyWriteResult":"not-attempted"}));
    }
    let (snapshot, current) = current_actor_context(&state);
    if current != context {
        return Err("Attribution or owning host context changed during confirmation; review and confirm again".into());
    }
    runtime_session::answer_preview(&snapshot, &generation, &request_id, &answer, &actor)?;
    state.host.answer_server_request(
        &generation,
        &request_id,
        &answer,
        "person-via-interaction",
        Some(&actor),
    )
}

#[tauri::command]
fn set_person_name(state: State<'_, AppState>, name: String) {
    *state.person_name.lock().unwrap() = if name.trim().is_empty() {
        None
    } else {
        Some(name.trim().to_string())
    };
}

#[tauri::command]
fn decision_view(state: State<'_, AppState>) -> Result<Value, String> {
    let ws = state
        .workspace
        .as_ref()
        .ok_or("CHIRALITY_WORKSPACE is not set")?;
    // Writer continuation flushes admitted native pending work before ordinary recorder appends.
    let mut g = state.act.lock().unwrap();
    let (recovery, written) = if let Some(ac) = g.as_mut() {
        let (recovery, written) = ac.refresh_recording();
        (Some(recovery), written)
    } else {
        (
            None,
            Err("native writer state unavailable; recorder continuation held".into()),
        )
    };
    let mut v = decision_view::derive(ws, &[]);
    match written {
        Ok(written) => v["requestsRecordedNow"] = json!(written.len()),
        Err(e) => v["limits"].as_array_mut().unwrap().push(json!(e)),
    }
    if let Some(recovery) = recovery {
        match recovery {
            Ok(results) => v["captureRecovery"] = json!(results),
            Err(e) => {
                v["captureRecovery"] = json!([{"state":"AC-8 record pending","writeFailure":e}])
            }
        }
    }
    v["workspace"] = json!(ws.display().to_string());
    Ok(v)
}

/// AI-9: the person opens the control from a pending row; the host composes the offer.
#[tauri::command]
fn compose_offer(state: State<'_, AppState>, request_ref: String) -> Result<Value, String> {
    let mut g = state.act.lock().unwrap();
    let ac = g.as_mut().ok_or("CHIRALITY_WORKSPACE is not set")?;
    ac.compose_a16(&request_ref)
}

/// AAC §4.1 steps 3-7 with the §6.2 P-2 placement: the host presents a native
/// confirmation it fills from the offer; only that confirmation captures.
#[tauri::command(async)]
fn decide(
    app: tauri::AppHandle,
    state: State<'_, AppState>,
    offer_id: String,
    alternative: String,
) -> Result<Value, String> {
    let (_, context) = current_actor_context(&state);
    let mut actor = act_control::person(
        context["displayName"].as_str(),
        context["osAccount"].as_str(),
    );
    if let Some(account) = context["codexAccount"].as_str() {
        actor["codexAccount"] = json!(account);
    }
    let mut g = state.act.lock().unwrap();
    let ac = g.as_mut().ok_or("CHIRALITY_WORKSPACE is not set")?;
    let text = ac.confirmation_text(&offer_id, &alternative, &actor)?;
    ac.present(&offer_id)?;
    let confirmed = app
        .dialog()
        .message(text)
        .title("Chirality — decide")
        .kind(MessageDialogKind::Warning)
        .buttons(MessageDialogButtons::OkCancelCustom(
            "Decide".into(),
            "Cancel".into(),
        ))
        .blocking_show();
    if !confirmed {
        ac.dismiss(&offer_id);
        return Ok(json!({"state": "AC-5 dismissed", "recorded": false}));
    }
    let (_, current) = current_actor_context(&state);
    if current != context {
        ac.dismiss(&offer_id);
        return Err("Attribution or owning host context changed during confirmation; review and confirm again".into());
    }
    ac.confirm(
        &offer_id,
        &alternative,
        InputSource::HostNativeConfirmation,
        actor,
    )
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let workspace = std::env::var("CHIRALITY_WORKSPACE").ok().map(PathBuf::from);
    let host_config = host_config_from_env(workspace.as_ref());
    let state = AppState {
        host: Arc::new(Host::new()),
        host_config: host_config.clone(),
        act: Mutex::new(workspace.as_ref().map(|w| ActControl::new(w))),
        workspace,
        person_name: Mutex::new(None),
        runtime: Mutex::new(runtime_session::RuntimeSession::default()),
        access_selection: Mutex::new(None),
        instructions_root: Mutex::new(Err("App instruction root not initialized".into())),
        app_user_data_root: Mutex::new(Err("App user-data root not initialized".into())),
        recovery_startup: Arc::new(Mutex::new(runtime_session::RecoveryStartup::default())),
        role_supply_status: Mutex::new(json!({"state":"not-supplied","adoption":"unknown"})),
        external_observation: Mutex::new(runtime_session::ExternalObservationSession::default()),
    };
    let host = Arc::clone(&state.host);
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .manage(state)
        .setup(move |app| {
            let data = app.path().app_data_dir().map_err(|e| e.to_string());
            let state = app.state::<AppState>();
            *state.app_user_data_root.lock().unwrap() = data.clone();
            state.recovery_startup.lock().unwrap().initialize(
                &host,
                data.as_deref().map_err(String::as_str),
                host_config
                    .as_ref()
                    .ok()
                    .map(|cfg| cfg.codex_home.as_path()),
            );
            let root = data.clone().and_then(|data| {
                let root = data.join("instructions");
                runtime_session::seed_instructions(&root)?;
                Ok(root)
            });
            *state.instructions_root.lock().unwrap() = root;
            // App start-up starts the supplier (HOSTING §4.6 start, actor `app-startup`).
            if let Ok(cfg) = host_config {
                let h = Arc::clone(&host);
                let recovery = Arc::clone(&state.recovery_startup);
                std::thread::spawn(move || {
                    let _ = runtime_session::start_with_recovery(
                        &h,
                        &recovery,
                        data.as_deref().map_err(String::as_str),
                        Some(&cfg.codex_home),
                        || h.start(&cfg, "app-startup"),
                    );
                });
            }
            Ok(())
        })
        // DEF-1: closing or reloading a window is not a stop (HOSTING §4.5); no window
        // event touches the child.
        .invoke_handler(tauri::generate_handler![
            host_status,
            host_observe,
            select_external_observation,
            answer_native_request,
            host_start,
            host_stop,
            thread_start,
            conversation_send_text,
            conversation_interrupt,
            set_person_name,
            decision_view,
            compose_offer,
            decide
        ])
        .build(tauri::generate_context!())
        .expect("error while building the Tauri application")
        .run(|app, event| {
            // A confirmed App quit is a deliberate stop (DEF-6 -> DEF-5a).
            if let tauri::RunEvent::Exit = event {
                let st: State<'_, AppState> = app.state();
                let _ = st.host.stop("the person", "App quit");
            }
        });
}
