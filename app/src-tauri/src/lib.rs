//! Chirality App v4 walking skeleton: Tauri 2 main process (V4-ARC-02).
//!
//! Modules and the contract sections they implement are listed in ../README.md.
//! The Rust main process owns the Codex child, the record writing and the act
//! capture (HOSTING §12 O-1 "Rust envelope core"; AAC §6.2 under R17-5). The
//! webview only reads snapshots and asks the host to act.

pub mod act_control;
pub mod canonical;
pub mod decision_view;
pub mod hosting;
pub mod recorder;
pub mod records;
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
}

/// A fresh probe home for the label probe (HOSTING §7.2 H-probe), in the temp directory.
fn probe_home() -> PathBuf {
    let n = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_nanos();
    let p = std::env::temp_dir().join(format!("cxp.{}.{}", std::process::id(), n));
    let _ = std::fs::create_dir_all(&p);
    p
}

/// Configuration comes only from the environment; no path is built in (owner rule).
pub fn host_config_from_env(workspace: Option<&PathBuf>) -> Result<HostConfig, String> {
    let bin = std::env::var("CHIRALITY_CODEX_BIN").map_err(|_| "CHIRALITY_CODEX_BIN is not set: no supplier distribution resolved".to_string())?;
    let home = std::env::var("CHIRALITY_CODEX_HOME").map_err(|_| "CHIRALITY_CODEX_HOME is not set: no App-owned Codex home given".to_string())?;
    let cwd = workspace.cloned().unwrap_or_else(std::env::temp_dir);
    let mut cfg = HostConfig::new(bin.into(), home.into(), probe_home(), cwd);
    cfg.expected_sha256 = std::env::var("CHIRALITY_CODEX_EXPECTED_SHA256").ok();
    cfg.allow_unverified_dev = std::env::var("CHIRALITY_ALLOW_UNVERIFIED").map(|v| v == "1").unwrap_or(false);
    Ok(cfg)
}

#[tauri::command]
fn host_status(state: State<'_, AppState>) -> Value {
    let mut s = state.host.snapshot();
    if let Err(e) = &state.host_config {
        s["configurationProblem"] = json!(e);
    }
    s
}

#[tauri::command(async)]
fn host_start(state: State<'_, AppState>) -> Result<Value, String> {
    let cfg = state.host_config.clone()?;
    state.host.start(&cfg, "the person")
}

#[tauri::command(async)]
fn host_stop(state: State<'_, AppState>) -> Result<Value, String> {
    state.host.stop("the person", "Stop Codex")
}

#[tauri::command(async)]
fn thread_start(state: State<'_, AppState>) -> Result<Value, String> {
    let cwd = state.host_config.as_ref().map(|c| c.cwd.display().to_string()).map_err(|e| e.clone())?;
    state.host.thread_start(&cwd)
}

#[tauri::command]
fn set_person_name(state: State<'_, AppState>, name: String) {
    *state.person_name.lock().unwrap() = if name.trim().is_empty() { None } else { Some(name.trim().to_string()) };
}

#[tauri::command]
fn decision_view(state: State<'_, AppState>) -> Result<Value, String> {
    let ws = state.workspace.as_ref().ok_or("CHIRALITY_WORKSPACE is not set")?;
    // The recorder identifies package files (RS §13.6) before the view is derived.
    let written = recorder::identify_packages(ws)?;
    let mut v = decision_view::derive(ws, &[recorder::LOG]);
    v["requestsRecordedNow"] = json!(written.len());
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
fn decide(app: tauri::AppHandle, state: State<'_, AppState>, offer_id: String, alternative: String) -> Result<Value, String> {
    let actor = act_control::person(state.person_name.lock().unwrap().as_deref(), util::os_account().as_deref());
    let mut g = state.act.lock().unwrap();
    let ac = g.as_mut().ok_or("CHIRALITY_WORKSPACE is not set")?;
    let text = ac.confirmation_text(&offer_id, &alternative, &actor)?;
    ac.present(&offer_id)?;
    let confirmed = app
        .dialog()
        .message(text)
        .title("Chirality — decide")
        .kind(MessageDialogKind::Warning)
        .buttons(MessageDialogButtons::OkCancelCustom("Decide".into(), "Cancel".into()))
        .blocking_show();
    if !confirmed {
        ac.dismiss(&offer_id);
        return Ok(json!({"state": "AC-5 dismissed", "recorded": false}));
    }
    ac.confirm(&offer_id, &alternative, InputSource::HostNativeConfirmation, actor)
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
    };
    let host = Arc::clone(&state.host);
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .manage(state)
        .setup(move |_app| {
            // App start-up starts the supplier (HOSTING §4.6 start, actor `app-startup`).
            if let Ok(cfg) = host_config {
                let h = Arc::clone(&host);
                std::thread::spawn(move || {
                    let _ = h.start(&cfg, "app-startup");
                });
            }
            Ok(())
        })
        // DEF-1: closing or reloading a window is not a stop (HOSTING §4.5); no window
        // event touches the child.
        .invoke_handler(tauri::generate_handler![
            host_status, host_start, host_stop, thread_start, set_person_name,
            decision_view, compose_offer, decide
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
