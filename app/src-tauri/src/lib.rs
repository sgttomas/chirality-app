//! Chirality App v4 walking skeleton: Tauri 2 main process (V4-ARC-02).
//!
//! Modules and the contract sections they implement are listed in ../README.md.
//! The Rust main process owns the Codex child, the record writing and the act
//! capture (HOSTING §12 O-1 "Rust envelope core"; AAC §6.2 under R17-5). The
//! webview only reads snapshots and asks the host to act.

pub mod access;
pub mod act_control;
pub mod act_policy;
pub mod attachments;
pub mod canonical;
pub mod capture_seal;
mod installation;
pub mod catalog;
mod checkpoint_recorder;
mod model_turn_recorder;
pub mod codex_stop;
mod app_quit;
pub mod conversation_roles;
pub mod connector_standing;
pub mod connector_route_store;
mod connector_answer_only;
mod connector_route_view;
mod connector_source;
mod connector_materialization;
mod connector_reconstruction;
mod connector_source_fs;
#[cfg(unix)] mod connector_git;
#[cfg(unix)] mod connector_git_process;
pub mod decision_view;
mod file_act_root;
mod file_act_view;
mod file_act_lapse;
pub mod external_observation;
pub mod external_trace;
pub mod trace_receiving;
pub mod hosting;
#[cfg(unix)]
pub mod distribution_preflight;
mod compiled_development_selection;
pub mod distribution_semantics;
mod distribution_store;
mod distribution_s1;
pub mod home_resources;
mod desktop_startup;
mod desktop_setup_confirmation;
mod provider_endpoint_confirmation;
pub mod native_items;
pub mod native_history;
pub mod role_lifecycle;
pub mod role_observations;
pub mod native_requests;
mod native_request_answer;
pub mod receiving;
pub mod recorder;
pub mod records;
pub mod records_access;
mod fleet_records;
mod native_conversation_links;
mod after_run_end;
mod records_index;
pub mod record_lines;
pub mod records_store;
pub mod records_export;
use records_store::custody as records_package;
pub mod records_retention;
pub mod recovery;
mod recovery_root_view;
pub mod role_supply;
pub mod child_roles;
mod native_child_guidance;
mod instruction_store;
pub(crate) mod run_offers;
pub(crate) mod run_restart;
pub mod runtime_session;
mod waiting_requests;
mod native_waiting;
#[cfg(test)] mod waiting_requests_tests;
pub(crate) mod workflow_declaration;
pub(crate) mod workflow_workspace;
mod workflow_selection;
pub(crate) mod workflow_trial_transcript;
mod historical_run_learning;
mod workflow_learning_pointers;
pub(crate) mod host_tick;
pub(crate) mod delegation_availability;
pub(crate) mod execution_compatibility;
pub(crate) mod a15_native;
pub mod schema_validation;
pub mod standing;
pub mod storage;
pub mod stop_records;
pub mod util;

use act_control::{ActControl, InputSource};
use hosting::{Host, HostConfig};
use runtime_session::trial_flows::SendRefusal;
use serde_json::{json, Value};
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use tauri::{Manager, State};
use tauri_plugin_dialog::{DialogExt, MessageDialogButtons, MessageDialogKind};

pub struct AppState {
    desktop_setup: Option<Arc<Mutex<desktop_startup::DesktopSetup>>>,
    // Short metadata sections only; no Host IO/native callback while held.
    endpoint_edits: Arc<Mutex<hosting::provider_endpoint::Controller>>,
    compiled_development_selection: Value,
    connector_sources: Mutex<connector_source::Session>,
    connector_drafts: Mutex<connector_materialization::Registry>,
    workspace: Option<PathBuf>,
    act: Arc<Mutex<Option<ActControl>>>,
    workflows: Mutex<runtime_session::WorkflowRootSession>,
    file_acts: Mutex<file_act_root::FileActRoot>,
    file_act_lapses: Mutex<file_act_lapse::Observer>,
    decision_writer_status: Mutex<Value>,
    person_name: Mutex<Option<String>>,
    instructions_root: Mutex<Result<PathBuf, String>>,
    app_user_data_root: Mutex<Result<PathBuf, String>>,
    external_observation: Mutex<runtime_session::ExternalObservationSession>,
    trace_selection: Mutex<runtime_session::TraceSelectionSession>,
    attachment_selection: Mutex<Result<runtime_session::AttachmentSelectionSession, String>>,
    role_log: Result<Arc<role_observations::RoleLog>, String>,
    native_links: Mutex<native_conversation_links::Session>,
    project_context: recovery::ExplicitAppProjectContext,
    project_context_limit: Option<String>,
    homes: Mutex<runtime_session::HomeRouter>,
    home_bootstrap: Mutex<Result<Arc<runtime_session::HomeBootstrapSet>,String>>,
    native_namespaces: Mutex<Result<Arc<hosting::attachment_custody::NativeNamespaceBindings>,String>>,
    key_namespace_admission: Mutex<Value>,
    key_setup: Mutex<()>,
    root_home_inputs: Value,
    /// One Stop/Restart Codex question at a time.
    codex_stop_gate: Mutex<()>,
    /// Confirmed Stop/Restart Codex outcomes, newest last, in this process only
    /// (`codex_stop::RECORDS_LIMIT`).
    codex_stops: Mutex<Vec<Value>>,
    /// Open "Continue as ‹role›" handoffs (NIR §5.8; ROLE §3.3), this process only.
    continue_as: Mutex<conversation_roles::Handoffs>,
    /// The App quit question and whether the quit may proceed (K-4, SQ-Q).
    app_quit: app_quit::AppQuit,
}

impl AppState {
    fn validate_home_source(&self,home:&runtime_session::HomeSession)->Result<(),String>{
        if let Some(desktop) = &self.desktop_setup { desktop.try_lock().map_err(|_|"Desktop setup busy; no new start")?.recheck_active()?; }
        match &*self.home_bootstrap.lock().unwrap(){
            Ok(set)=>set.validate_binding(home.class(),home.host_config.as_ref().map_err(Clone::clone)?),
            Err(_) if home.class()==home_resources::HomeClass::Account=>Ok(()),
            Err(error)=>Err(error.clone()),
        }
    }
}

// Private source transaction, reused by the typed endpoint command below.
// Begin must precede an intended target replacement. A later native ACK/read
// alone cannot adopt it; complete requires a separate exact-candidate review.
struct PendingConfigResource {
    home: Arc<runtime_session::HomeSession>,
    generation: Value,
    cwd: String,
    slot: desktop_startup::ConfigSlotPreflight,
    endpoint_epoch: String,
}
fn begin_config_resource_continuation(state: &AppState) -> Result<PendingConfigResource, String> {
    let home = state.homes.lock().unwrap().active();
    if home.class() != home_resources::HomeClass::Account {
        return Err("Config continuation requires the admitted account source".into());
    }
    state.validate_home_source(&home)?;
    let config = home.host_config.as_ref().map_err(Clone::clone)?;
    let generation = home.host.snapshot()["generation"].clone();
    let expected_home = format!(
        "app-home:{}",
        util::sha256_hex(config.codex_home.as_os_str().as_encoded_bytes())
    );
    recovery::generation_ref(&generation)?;
    if generation["home"] != expected_home {
        return Err("Config continuation generation/home differs".into());
    }
    let cwd = config
        .cwd
        .to_str()
        .ok_or("Config continuation requires lossless native JSON cwd")?
        .to_owned();
    let slot = state
        .desktop_setup
        .as_ref()
        .ok_or("No admitted saved-desktop source")?
        .try_lock()
        .map_err(|_| "Desktop source busy")?
        .begin_config_continuation(config)?;
    Ok(PendingConfigResource {
        home,
        generation,
        cwd,
        slot,
        endpoint_epoch: state
            .endpoint_edits
            .lock()
            .map_err(|_| "Endpoint controller busy")?
            .epoch
            .clone(),
    })
}
fn complete_config_resource_continuation(
    state: &AppState,
    pending: PendingConfigResource,
    review: impl FnOnce(
        &hosting::config_resource_continuation::Candidate,
    ) -> Result<
        Option<hosting::config_resource_continuation::ReviewedCurrentObject>,
        (),
    >,
) -> Result<bool, String> {
    let desktop = state
        .desktop_setup
        .as_ref()
        .ok_or("No admitted saved-desktop source")?;
    let context = || {
        if state
            .endpoint_edits
            .lock()
            .map_err(|_| "Endpoint controller busy")?
            .epoch
            != pending.endpoint_epoch
        {
            return Err("Endpoint source epoch superseded".into());
        }
        if !Arc::ptr_eq(&state.homes.lock().unwrap().active(), &pending.home)
            || pending.home.host.snapshot()["generation"] != pending.generation
        {
            return Err("Original account/generation superseded".into());
        }
        let config = pending.home.host_config.as_ref().map_err(Clone::clone)?;
        if config.cwd.to_str() != Some(&pending.cwd) {
            return Err("Original effective cwd differs".into());
        }
        state
            .home_bootstrap
            .lock()
            .unwrap()
            .as_ref()
            .map_err(Clone::clone)?
            .validate_binding(home_resources::HomeClass::Account, config)
    };
    let wait = pending
        .home
        .host_config
        .as_ref()
        .map_err(Clone::clone)?
        .wait_limit
        .min(std::time::Duration::from_secs(10));
    hosting::config_resource_continuation::complete(
        desktop,
        pending.slot,
        &pending.home.host,
        &pending.generation,
        &pending.cwd,
        wait,
        context,
        review,
    )
}

/// A fresh probe home for the label probe (HOSTING §7.2 H-probe), in the temp directory.
fn probe_home() -> Result<PathBuf,String> {
    runtime_session::allocate_fresh_probe(&std::env::temp_dir())
}

/// Complete explicit environment route; no private supplier/home path is built in.
/// Desktop requests are a separate exclusive source, resolved before Root binding.
pub fn host_config_from_env(workspace: Option<&PathBuf>) -> Result<HostConfig, String> {
    host_config_from_inputs(workspace, |key|std::env::var_os(key), probe_home)
}

fn host_config_from_inputs(workspace: Option<&PathBuf>, input: impl Fn(&str)->Option<std::ffi::OsString>, probe: impl FnOnce()->Result<PathBuf,String>) -> Result<HostConfig,String> {
    let bin = input("CHIRALITY_CODEX_BIN").ok_or(()).map_err(|_| {
        "CHIRALITY_CODEX_BIN is not set: no supplier distribution resolved".to_string()
    })?;
    let home = input("CHIRALITY_CODEX_HOME").ok_or(()).map_err(|_| {
        "CHIRALITY_CODEX_HOME is not set: no App-owned Codex home given".to_string()
    })?;
    let cwd = workspace.cloned().unwrap_or_else(std::env::temp_dir);
    let mut cfg = HostConfig::new(bin.into(), home.into(), probe()?, cwd);
    cfg.records_project=workspace.is_some();
    cfg.expected_sha256 = input("CHIRALITY_CODEX_EXPECTED_SHA256").and_then(|v|v.into_string().ok());
    cfg.allow_unverified_dev = input("CHIRALITY_ALLOW_UNVERIFIED").is_some_and(|v|v == "1");
    Ok(cfg)
}

fn desktop_controller(state: &AppState) -> Result<Arc<Mutex<desktop_startup::DesktopSetup>>, String> {
    state.desktop_setup.clone().ok_or("Desktop setup controller unavailable".into())
}

fn invalidate_endpoint_edits(state: &AppState) -> Result<(), String> {
    endpoint_checkpoint(state).map(|_| ())
}
fn endpoint_checkpoint(state: &AppState) -> Result<String, String> {
    let mut controller = state
        .endpoint_edits
        .lock()
        .map_err(|_| "Endpoint controller busy")?;
    controller.invalidate()?;
    Ok(controller.epoch.clone())
}
#[tauri::command]
fn provider_endpoint_discard(state: State<'_, AppState>) -> Result<String, String> {
    endpoint_checkpoint(&state)
}
fn endpoint_offer_result(
    state: &AppState,
    generation: &Value,
    id: &str,
    endpoint: &str,
    expected_epoch: &str,
) -> Result<Value, String> {
    let epoch = {
        let mut controller = state
            .endpoint_edits
            .lock()
            .map_err(|_| "Endpoint controller busy")?;
        // A delayed IPC offer must not revive a draft after a newer input or
        // source invalidation, even if that invalidation ran before this task.
        if controller.epoch != expected_epoch || expected_epoch.is_empty() {
            return Err("Endpoint offer superseded".into());
        }
        controller.invalidate()?;
        if controller.saving.is_some() {
            return Err("An endpoint change is pending; no second offer".into());
        }
        controller.epoch.clone()
    };
    if state.homes.lock().unwrap().active().host.snapshot()["generation"] != *generation {
        return Err("Endpoint source unavailable".into());
    }
    let offer = hosting::provider_endpoint::offer(state, id, endpoint)?;
    let view = offer.view();
    let mut controller = state
        .endpoint_edits
        .lock()
        .map_err(|_| "Endpoint controller busy")?;
    if controller.epoch != epoch || offer.epoch() != epoch {
        return Err("Endpoint offer superseded".into());
    }
    controller.offer = Some(offer);
    drop(controller);
    hosting::provider_endpoint::expire_offer(
        &state.endpoint_edits,
        view["token"].as_str().ok_or("Endpoint token unavailable")?,
        hosting::provider_endpoint::OFFER_LIFETIME,
    )?;
    Ok(view)
}
#[tauri::command(async)]
fn provider_endpoint_offer(
    state: State<'_, AppState>,
    generation: Value,
    provider_id: String,
    endpoint: String,
    epoch: String,
) -> Result<Value, String> {
    endpoint_offer_result(&state, &generation, &provider_id, &endpoint, &epoch)
        .map_err(|_| "Endpoint edit unavailable; private values and diagnostics withheld".into())
}
fn endpoint_save_result(
    state: &AppState,
    token: &str,
    before: impl FnOnce(&Value) -> Result<tauri_plugin_dialog::MessageDialogResult, String>,
    after: impl FnOnce(
        &hosting::config_resource_continuation::Candidate,
        &Value,
    ) -> Result<
        Option<hosting::config_resource_continuation::ReviewedCurrentObject>,
        (),
    >,
) -> Result<Value, String> {
    let offer = {
        let mut controller = state
            .endpoint_edits
            .lock()
            .map_err(|_| "Endpoint controller busy")?;
        if controller.saving.is_some()
            || controller
                .offer
                .as_ref()
                .is_none_or(|o| o.view()["token"] != token)
        {
            return Err("Original endpoint offer unavailable or superseded".into());
        }
        controller.saving = Some(token.into());
        controller.offer.take().unwrap()
    };
    let result = hosting::provider_endpoint::save(state, offer, before, after);
    if let Ok(mut controller) = state.endpoint_edits.lock() {
        if controller.saving.as_deref() == Some(token) {
            controller.saving = None;
        }
    }
    result
}
fn create_offer_result(
    state: &AppState,
    generation: &Value,
    id: &str,
    name: &str,
    endpoint: &str,
    expected_epoch: &str,
) -> Result<Value, String> {
    let epoch = {
        let mut c = state
            .endpoint_edits
            .lock()
            .map_err(|_| "Provider controller unavailable")?;
        if c.epoch != expected_epoch || expected_epoch.is_empty() {
            return Err("Provider Add superseded".into());
        }
        c.invalidate()?;
        if c.saving.is_some() {
            return Err("A provider write is pending".into());
        }
        c.epoch.clone()
    };
    if state.homes.lock().unwrap().active().host.snapshot()["generation"] != *generation {
        return Err("Provider source unavailable".into());
    }
    let offer = hosting::provider_create::offer(state, id, name, endpoint)?;
    let view = offer.view();
    let mut c = state
        .endpoint_edits
        .lock()
        .map_err(|_| "Provider controller unavailable")?;
    if c.epoch != epoch || offer.epoch() != epoch {
        return Err("Provider Add superseded".into());
    }
    c.create_offer = Some(offer);
    drop(c);
    hosting::provider_endpoint::expire_create_offer(
        &state.endpoint_edits,
        view["token"].as_str().ok_or("Add token unavailable")?,
        hosting::provider_endpoint::OFFER_LIFETIME,
    )?;
    Ok(view)
}
fn create_save_result(
    state: &AppState,
    token: &str,
    window_current: impl Fn() -> Result<(), String>,
    before: impl FnOnce(&Value) -> Result<tauri_plugin_dialog::MessageDialogResult, String>,
    after: impl FnOnce(
        &hosting::config_resource_continuation::Candidate,
        &Value,
    ) -> Result<
        Option<hosting::config_resource_continuation::ReviewedCurrentObject>,
        (),
    >,
) -> Result<Value, String> {
    let offer = {
        let mut c = state
            .endpoint_edits
            .lock()
            .map_err(|_| "Provider controller unavailable")?;
        if c.saving.is_some()
            || c.create_offer
                .as_ref()
                .is_none_or(|o| o.view()["token"] != token)
        {
            return Err("Original Add offer unavailable or superseded".into());
        }
        c.saving = Some(token.into());
        c.create_offer.take().unwrap()
    };
    let result = hosting::provider_create::save(state, offer, window_current, before, after);
    if let Ok(mut c) = state.endpoint_edits.lock() {
        if c.saving.as_deref() == Some(token) {
            c.saving = None;
        }
    }
    result
}
#[tauri::command]
fn provider_create_discard(state: State<'_, AppState>) -> Result<String, String> {
    endpoint_checkpoint(&state)
}
#[tauri::command(async)]
fn provider_create_offer(
    state: State<'_, AppState>,
    generation: Value,
    provider_id: String,
    name: String,
    endpoint: String,
    epoch: String,
) -> Result<Value, String> {
    create_offer_result(&state, &generation, &provider_id, &name, &endpoint, &epoch)
        .map_err(|_| "Provider Add unavailable; private values and diagnostics withheld".into())
}
#[tauri::command(async)]
fn provider_create_save(
    window: tauri::Window,
    state: State<'_, AppState>,
    token: String,
) -> Result<Value, String> {
    let (epoch, remaining) = {
        let c = state
            .endpoint_edits
            .lock()
            .map_err(|_| "Provider controller unavailable")?;
        (
            c.epoch.clone(),
            c.create_offer
                .as_ref()
                .ok_or("Add offer unavailable")?
                .remaining(),
        )
    };
    create_save_result(
        &state,
        &token,
        || provider_endpoint_confirmation::recheck_original(&window),
        |effects| {
            provider_endpoint_confirmation::confirm_add(&window, effects, false, remaining, || {
                endpoint_question_current(&state, &epoch, &effects["scope"])
            })
        },
        |candidate, effects| {
            let choice = provider_endpoint_confirmation::confirm_add(
                &window,
                effects,
                true,
                hosting::provider_endpoint::OFFER_LIFETIME,
                || endpoint_question_current(&state, &epoch, &effects["scope"]),
            )
            .map_err(|_| ())?;
            Ok(act_control::native_statement::chose(
                &choice,
                provider_endpoint_confirmation::CONTINUE_ACTION,
            )
            .then(|| candidate.accept_checked_current_object()))
        },
    )
    .map_err(|_| {
        "Provider Add unavailable; no automatic retry; private diagnostics withheld".into()
    })
}
fn endpoint_question_current(state: &AppState, epoch: &str, scope: &Value) -> Result<(), String> {
    if state
        .endpoint_edits
        .lock()
        .map_err(|_| "Endpoint controller busy")?
        .epoch
        != epoch
    {
        return Err("Endpoint operation superseded".into());
    }
    let home = state
        .homes
        .try_lock()
        .map_err(|_| "Home source busy")?
        .active();
    let snapshot = home.host.snapshot();
    let cwd = home
        .host_config
        .as_ref()
        .map_err(Clone::clone)?
        .cwd
        .to_str()
        .ok_or("Native cwd unavailable")?
        .to_owned();
    if home.class() != home_resources::HomeClass::Account
        || snapshot["generation"] != scope["generation"]
        || snapshot["state"] != "ready"
        || snapshot["generationClosed"] == true
        || scope["cwd"] != cwd
        || home
            .host
            .configured_provider_revision(&scope["generation"], &cwd)
            != scope["readRevision"]
    {
        return Err("Original endpoint observation superseded or unavailable".into());
    }
    Ok(())
}
#[tauri::command(async)]
fn provider_endpoint_save(
    window: tauri::Window,
    state: State<'_, AppState>,
    token: String,
) -> Result<Value, String> {
    let epoch = state
        .endpoint_edits
        .lock()
        .map_err(|_| "Endpoint controller busy")?
        .epoch
        .clone();
    let remaining = state
        .endpoint_edits
        .lock()
        .map_err(|_| "Endpoint controller busy")?
        .offer
        .as_ref()
        .ok_or("Endpoint offer unavailable")?
        .remaining();
    endpoint_save_result(
        &state,
        &token,
        |effects| {
            provider_endpoint_confirmation::confirm(&window, effects, false, remaining, || {
                endpoint_question_current(&state, &epoch, &effects["scope"])
            })
        },
        |candidate, effects| {
            let choice = provider_endpoint_confirmation::confirm(
                &window,
                effects,
                true,
                hosting::provider_endpoint::OFFER_LIFETIME,
                || endpoint_question_current(&state, &epoch, &effects["scope"]),
            )
            .map_err(|_| ())?;
            Ok(act_control::native_statement::chose(
                &choice,
                provider_endpoint_confirmation::CONTINUE_ACTION,
            )
            .then(|| candidate.accept_checked_current_object()))
        },
    )
    .map_err(|_| {
        "Endpoint change unavailable; no automatic retry; inspect the current edit status".into()
    })
}

#[tauri::command(async)]
fn desktop_setup_pick(app: tauri::AppHandle, kind: String) -> Result<Value, String> {
    let file = match kind.as_str() {
        "config" => app.dialog().file().set_title("Choose the explicit shared config.toml reference").blocking_pick_file(),
        "agents" => app.dialog().file().set_title("Choose the explicit shared AGENTS.md reference").blocking_pick_file(),
        "skills" => app.dialog().file().set_title("Choose the explicit shared skills directory reference").blocking_pick_folder(),
        "project" => app.dialog().file().set_title("Choose the project for the next App launch").blocking_pick_folder(),
        _ => return Err("Unknown desktop setup location".into()),
    };
    file.map(|file|file.into_path().map(|path|json!({"displayPath":path.display().to_string(),"nativePath":attachments::native_path_identity(&path)})).map_err(|e|format!("Selected location is not a native filesystem path: {e}"))).transpose().map(|p|p.unwrap_or(Value::Null))
}
#[tauri::command(async)]
fn desktop_setup_preview(state: State<'_, AppState>, shared_paths: [Value; 3], project_path: Option<Value>, supplier_selection: String) -> Result<Value, String> {
    let [config, agents, skills] = shared_paths.map(desktop_startup::explicit_path);
    let controller = desktop_controller(&state)?;
    let result = controller.try_lock().map_err(|_|"Desktop setup busy; retry explicitly")?.preview([config?, agents?, skills?], project_path.map(desktop_startup::explicit_path).transpose()?, &supplier_selection);
    result
}
#[tauri::command(async)]
fn desktop_setup_project_preview(state: State<'_, AppState>, project_path: Option<Value>) -> Result<Value, String> {
    let controller = desktop_controller(&state)?;
    let result = controller.try_lock().map_err(|_|"Desktop setup busy; retry explicitly")?
        .preview_project(project_path.map(desktop_startup::explicit_path).transpose()?);
    result
}
#[tauri::command(async)]
fn desktop_setup_prepare(window: tauri::Window, state: State<'_, AppState>, preview_token: String) -> Result<Value, String> {
    let controller = desktop_controller(&state)?;
    desktop_setup_confirmation::prepare(&controller, &preview_token,
        |statement, action| desktop_setup_confirmation::confirm(&window, statement, action))
}

/// Person-requested metadata read. No Root guard spans Host/queue observation,
/// no ledger flush, and no supplier/native History operation is requested.
#[tauri::command(async)]
fn read_recovery_custody(state: State<'_, AppState>, mode_home_class: String, generation: Value) -> Result<Value,String> {
    read_recovery_custody_from_root(&state.homes, &mode_home_class, &generation)
}
fn read_recovery_custody_from_root(homes:&Mutex<runtime_session::HomeRouter>,mode_home_class:&str,generation:&Value)->Result<Value,String>{
    let home=homes.try_lock().map_err(|_|"Home selection busy; recovery read not performed")?.active();
    let view=recovery_root_view::read(&home,mode_home_class,generation)?;
    let active=homes.try_lock().map_err(|_|"Home selection busy after read; refresh recovery source")?.active();
    if !Arc::ptr_eq(&home,&active){return Err("Active recovery home changed while reading; original snapshot not reassigned".into());}
    Ok(view)
}

#[tauri::command(async)]
fn read_recovery_request_history(state: State<'_, AppState>, mode_home_class: String, generation: Value, cursor: Option<Value>) -> Result<Value,String> {
    read_recovery_request_history_from_root(&state.homes, &mode_home_class, &generation, cursor.as_ref())
}
fn read_recovery_request_history_from_root(homes: &Mutex<runtime_session::HomeRouter>, mode_home_class: &str, generation: &Value, cursor: Option<&Value>) -> Result<Value,String> {
    let home = homes.try_lock().map_err(|_|"Home selection busy; request-history read not performed")?.active();
    let view = recovery_root_view::read_request_history(&home, mode_home_class, generation, cursor)?;
    let active = homes.try_lock().map_err(|_|"Home selection busy after request-history read")?.active();
    if !Arc::ptr_eq(&home, &active) { return Err("Active request-history home changed; original page not reassigned".into()); }
    Ok(view)
}

/// RECOVERY §3.2 CV-15: the person asks for an unavailable conversation's
/// recovery reads again. The host reads it on this home's ready Codex
/// (`thread/read`, then its latest turns); nothing is resumed and nothing is
/// sent to the conversation. Returns the recovery view after the reads.
#[tauri::command(async)]
fn recovery_retry(state: State<'_, AppState>, mode_home_class: String, generation: Value, thread_id: String) -> Result<Value,String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    home.host.recovery_retry(&thread_id)?;
    host_tick::recovery_tick_home(&home);
    recovery_root_view::read(&home, &mode_home_class, &home.host.snapshot()["generation"])
}

#[tauri::command]
fn host_status(state: State<'_, AppState>) -> Value {
    let home = state.homes.lock().unwrap().active();
    let mut runtime = home.runtime.lock().unwrap();
    let (observation, received) = runtime.receive_native(&home.host);
    let mut s = observation["snapshot"].clone();
    if let Ok(mut edits)=state.endpoint_edits.lock(){edits.retire_source(&home,&s["generation"],s["state"]=="ready"&&s["generationClosed"]!=true);}
    for (key, value) in received.as_object().unwrap() {
        s[key] = value.clone();
    }
    s["accessSelection"] = home.access_selection
        .lock()
        .unwrap()
        .as_ref()
        .map(access::ConversationSelection::snapshot)
        .map_or(Value::Null, |v| v);
    s["recoveryInitialization"] = home.recovery_startup.lock().unwrap().snapshot();
    if let Err(e) = &home.host_config {
        s["configurationProblem"] = json!(e);
    }
    s["roleSupply"] = home.role_supply_status.lock().unwrap().clone();
    s["roleSet"] = role_set_metadata();
    s["compiledDevelopmentSelection"] = state.compiled_development_selection.clone();
    s["desktopSetup"] = state.desktop_setup.as_ref().map(|d|d.lock().unwrap().view()).unwrap_or(Value::Null);
    s["providerEndpointEdit"]=json!({"available":home.class()==home_resources::HomeClass::Account&&home.host_config.as_ref().ok().is_some_and(|cfg|state.desktop_setup.as_ref().is_some_and(|d|d.lock().unwrap().endpoint_source_available(cfg))),"standing":"Source metadata only; a fresh private user-layer offer and two explicit native decisions remain required"});
    s["providerCreate"]=json!({"available":s["providerEndpointEdit"]["available"],"standing":"Source metadata only; fresh private absence/version proof and two native decisions remain required"});
    // Native commands and the per-home Rust tick reconcile private receipts.
    // Status projects the last received history; polling does not write role
    // observations or admit a genuinely late native outcome.
    let (root,history) = host_tick::project_status_history(&home,&mut s,||state.instructions_root.lock().unwrap().clone());
    // NPTD §7.1: each conversation's delegation reading, as this home's host
    // last read it (the reads run on the host tick and when Try with the
    // authoring agent is pressed; host_status reads nothing from Codex).
    delegation_availability::annotate_threads(&mut s["threads"], &home.host.delegation_readings());
    // ROLE §6.2 LA-4: the limits shown where a role is chosen, as handed.
    s["roleLimits"] = conversation_roles::limit_account(root.as_deref().ok());
    let generation = s["generation"].clone();
    let targets = s["threads"].as_array().into_iter().flatten().filter(|thread|thread["generation"] == generation)
        .filter_map(|thread|thread["threadId"].as_str()).map(|thread|match runtime_session::observed_steering_target(&s, &generation, thread) {
            Ok(target) => json!({"generation":generation,"threadId":thread,"target":target}),
            Err(error) => json!({"generation":generation,"threadId":thread,"target":null,"reason":error}),
        }).collect::<Vec<_>>();
    s["steeringTargets"] = json!(targets);
    s["externalObservation"] = state.external_observation.lock().unwrap().snapshot();
    s["traceReceiving"] = state.trace_selection.lock().unwrap().snapshot();
    let custody = home.attachment_custody.lock().unwrap().clone();
    let mut selections = state.attachment_selection.lock().unwrap();
    if let (Ok(selection),Ok(custody)) = (selections.as_mut(),custody.as_ref()) { selection.refresh_submissions(&home.host,custody); }
    s["attachmentSelections"] = match selections.as_ref() {
        Ok(selection) => selection.snapshot(),
        Err(error) => json!({"state":"unavailable","reason":error,"submissionStanding":"nothing selected/sent; plain text controls remain independent"}),
    };
    s["attachmentCustody"] = match custody {Ok(custody)=>json!({"state":"opened","root":custody.root().display().to_string()}),Err(error)=>json!({"state":"unavailable","error":error,"scope":"attachment-bearing operations only"})};
    s["homeResources"] = match &*state.home_bootstrap.lock().unwrap() { Ok(set)=>set.inspect(),Err(error)=>json!({"state":"topology/resource descriptors unavailable","limit":error,"existingAccount":"legacy native account path remains available; no shared-source claim"}) };
    s["nativeNamespaces"] = match &*state.native_namespaces.lock().unwrap(){Ok(binding)=>binding.snapshot(),Err(error)=>json!({"state":"storage namespace closure unavailable","limit":error,"ordinaryNativeOperations":"independent of persistence availability"})};
    s["keyNamespaceAdmission"] = state.key_namespace_admission.lock().unwrap().clone();
    s["homeResources"]["sourceInputs"] = state.root_home_inputs.clone();
    if state.root_home_inputs["source"].as_str().is_some_and(|source|source != "explicit Root native environment path inputs") {
        s["attachmentSelections"]["launchAppProjectObservation"]["source"] = state.root_home_inputs["source"].clone();
    }
    {
        let homes = state.homes.lock().unwrap();
        s["homeRouting"] = homes.snapshot();
        s["waitingRequests"] = waiting_requests::overview(&homes);
    }
    s["homeAccess"] = home.account_view();
    // OI-008: host_status presents; it records nothing. The checkpoint recorder
    // and the trial reads run on the host's own tick (`host_tick`).
    s["hostTicks"] = host_tick::tick_state();
    s["workflowRoot"] = host_tick::workflow_status_after_history(&state.workflows, &home, &s["nativeView"], state.workspace.is_some(),history);
    let trial_homes = state.homes.lock().unwrap().entries();
    runtime_session::trial_flows::decorate_restart_sources(&state.workflows, &trial_homes, &mut s["workflowRoot"]);
    workflow_selection::publish_context(&mut s, &home);
    s["homeOAuth"] = runtime_session::native_oauth_observation(&home);
    s["continueAs"] = state.continue_as.lock().unwrap().view(&s);
    s["codexStops"] = json!({"outcomes":state.codex_stops.lock().unwrap().clone(),"stopWaitLimitSeconds":codex_stop::STOP_WAIT_LIMIT.as_secs(),"records":codex_stop::RECORDS_LIMIT});
    s["connectorRouteAvailability"] = connector_route_view::availability(state.workspace.as_deref(), &state.project_context, state.project_context_limit.as_deref());
    s["recordsStore"] = records_store::status(state.workspace.as_deref());
    s["nativeConversationLinks"] = state.native_links.lock().map(|links| links.snapshot()).unwrap_or_else(|_|json!({"state":"unavailable","limit":"native relationship recording session unavailable; native operation outcomes remain as observed"}));
    s["recordChain"] = records_index::chain_status(state.workspace.as_deref());
    s["currentAppProjectContext"] = state.project_context.view();
    s["configuredProviderReadRevision"] = if home.class() == home_resources::HomeClass::Account {
        home.host_config.as_ref().ok().and_then(|cfg|cfg.cwd.to_str())
            .map(|cwd|home.host.configured_provider_revision(&s["generation"],cwd)).unwrap_or(Value::Null)
    } else { Value::Null };

    s["currentAppProjectContextLimit"] = json!(state.project_context_limit);
    if let Err(e) = &*state.instructions_root.lock().unwrap() {
        s["instructionsProblem"] = json!(e);
    }
    s
}

/// RS §13.8 "Existing records": the person's explicit import of the project's
/// §13.7 records into the records store (byte-identical, verified copies).
#[tauri::command(async)]
fn records_store_import(state: State<'_, AppState>) -> Result<Value, String> {
    let project = state.workspace.as_ref().ok_or("no project is open; nothing imported")?;
    records_store::import(project)
}
/// RS §13.8 Tamper-evidence: each log's chain head of the open project, on
/// demand (the host status carries only bounded counts).
#[tauri::command(async)]
fn records_chain_heads(state: State<'_, AppState>) -> Result<Value, String> {
    let project = state.workspace.as_ref().ok_or("no project is open")?;
    Ok(records_index::chain_heads(project))
}
/// Manual DEL-06-01 source read: only the Root's selected workspace. The
/// webview supplies no path, graph selection, record or association.
#[tauri::command(async)]
fn read_fleet_records(state: State<'_, AppState>) -> Result<Value, String> {
    read_fleet_records_for_workspace(state.workspace.as_deref())
}
fn read_fleet_records_for_workspace(workspace: Option<&std::path::Path>) -> Result<Value,String> {
    fleet_records::read_for_workspace(workspace)
}
/// The person picks the parent of a new, verified records export package.
#[tauri::command(async)]
fn records_store_export(app: tauri::AppHandle, state: State<'_, AppState>) -> Result<Value, String> {
    let project = state.workspace.as_ref().ok_or("no project is open; nothing exported")?;
    let Some(parent) = workflow_native_folder(&app, "Choose a folder for the records export")? else { return Ok(json!({"state":"export cancelled"})); };
    let destination = parent.join(util::opaque_id("records-export-")?);
    records_export::export(project, &destination)
}
#[tauri::command(async)]
fn records_store_verify_export(app: tauri::AppHandle) -> Result<Value, String> {
    let Some(folder) = workflow_native_folder(&app, "Choose a records export to verify")? else { return Ok(json!({"state":"verification cancelled"})); };
    records_export::verify(&folder)
}
/// Source selection and the concrete import question remain native. The
/// renderer supplies only the offered operation, never a path or actor claim.
#[tauri::command(async)]
fn records_store_import_package(app:tauri::AppHandle,state:State<'_,AppState>,action:String)->Result<Value,String>{
    enum NativePackagePlan {
        Import(records_store::package::Plan),
        Repair(records_store::package::control_recovery::ControlPlan),
    }
    let project=state.workspace.as_deref().ok_or("no project is open")?;
    let home=state.homes.lock().unwrap().active();
    let observe=||->Result<(Value,Value),String>{
        let active=state.homes.lock().unwrap().active();
        if !Arc::ptr_eq(&active,&home){return Err("Native home selection changed; review again".into());}
        let (_,observed)=current_actor_context_for(&state,&home);
        let mut actor=act_control::person(observed["displayName"].as_str(),observed["osAccount"].as_str());
        if let Some(account)=observed["codexAccount"].as_str(){actor["codexAccount"]=json!(account);}
        Ok((actor,json!({"observedHome":observed,"modeHomeClass":home.class().as_str()})))
    };
    let (actor,observed)=observe()?;
    let plan=match action.as_str(){
        "import"|"restore"=>{
            let Some(folder)=workflow_native_folder(&app,"Choose the records package to import")? else{return Ok(json!({"state":"package import cancelled"}));};
            NativePackagePlan::Import(if action=="restore" {
                records_store::package::prepare_restore(project,&folder,&actor,&observed)?
            }else{records_store::package::prepare(project,&folder,&actor,&observed)?})
        },
        "resume"=>NativePackagePlan::Import(records_store::package::prepare_resume(project,&actor,&observed)?),
        "repair"=>{
            let source=if records_store::package::control_recovery::needs_package(project)? {
                let Some(folder)=workflow_native_folder(&app,"Locate the exact package named by the original import")? else{return Ok(json!({"state":"package control repair cancelled"}));};
                Some(folder)
            }else{None};
            NativePackagePlan::Repair(records_store::package::control_recovery::prepare(project,source.as_deref(),&actor,&observed)?)
        },
        _=>return Err("unknown package import action".into()),
    };
    let statement=match &plan {
        NativePackagePlan::Import(plan)=>records_store::package::statement(plan),
        NativePackagePlan::Repair(plan)=>records_store::package::control_recovery::statement(plan),
    };
    let perform=match action.as_str(){"resume"=>"Finish original import","restore"=>"Restore project from package","repair"=>"Repair package controls",_=>"Import package"};
    let mut refused=None;
    if !confirm_choice(&app,"Project records package",statement,"Leave records as they are",perform,&mut refused){
        return refused.map_or_else(||Ok(json!({"state":"cancelled; no package publication"})),Err);
    }
    let (actor,current)=observe()?;
    let links=state.native_links.try_lock().map_err(|_|"Native relationship recording busy; retry later")?;
    if links.has_pending(){return Err("Native relationship recording remains pending; retry it before package import".into());}
    let workflows=state.workflows.try_lock().map_err(|_|"Workflow operation busy; retry later")?;
    workflows.retention_ready()?;
    let acts=state.act.try_lock().map_err(|_|"Act recording busy; retry later")?;
    if acts.as_ref().is_some_and(|a|!a.writer_ready()){return Err("Native act recording remains pending; retry it before package import".into());}
    match plan {
        NativePackagePlan::Import(plan)=>records_store::package::apply(plan,&actor,&current),
        NativePackagePlan::Repair(plan)=>records_store::package::control_recovery::apply(plan,&actor,&current),
    }
}
/// RS §13.8: administrative retention acts are captured only by this native
/// question. The renderer supplies an offered action, never actor or evidence.
#[tauri::command(async)]
fn records_store_retention(app:tauri::AppHandle,state:State<'_,AppState>,action:String)->Result<Value,String>{
    let project=state.workspace.as_deref().ok_or("no project is open")?;
    let home=state.homes.lock().unwrap().active();
    let observe=||->Result<(Value,Value),String>{
        let active=state.homes.lock().unwrap().active();if !Arc::ptr_eq(&active,&home){return Err("Native home selection changed; review again".into());}
        let (_,observed)=current_actor_context_for(&state,&home);
        let mut actor=act_control::person(observed["displayName"].as_str(),observed["osAccount"].as_str());
        if let Some(account)=observed["codexAccount"].as_str(){actor["codexAccount"]=json!(account);}
        Ok((actor,json!({"observedHome":observed,"modeHomeClass":home.class().as_str()})))
    };
    if action=="close" {
        let links=state.native_links.try_lock().map_err(|_|"Native relationship recording is pending")?;
        if links.has_pending(){return Err("Native relationship records are still pending; wait for their recording before closing the project".into());}
        let workflows=state.workflows.try_lock().map_err(|_|"A workflow operation is pending")?;workflows.retention_ready()?;
        let acts=state.act.try_lock().map_err(|_|"An act operation is pending")?;
        if acts.as_ref().is_some_and(|a|!a.writer_ready()){return Err("A native act still has pending records; retry its recording before closing the project".into());}
    }
    let bag=if action=="dispose" {match workflow_native_folder(&app,"Choose the verified export of this closed project's current records")? {Some(path)=>Some(path),None=>return Ok(json!({"state":"disposal cancelled"}))}}else{None};
    let (actor,observed)=observe()?;
    let plan=records_retention::prepare(project,&action,bag.as_deref(),&actor,&observed)?;
    let (dont,perform)=match action.as_str(){"close"=>("Keep project open","Close project"),"reopen"=>("Keep project closed","Reopen project"),"set-hold"=>("Keep current hold state","Set legal hold"),"release-hold"=>("Keep legal hold","Release legal hold"),"dispose"=>("Keep records","Dispose of records"),"resume-disposal"=>("Leave incomplete","Finish disposal"),_=>return Err("unknown records retention action".into())};
    let mut refused=None;
    if !confirm_choice(&app,"Project records retention",records_retention::statement(&plan),dont,perform,&mut refused){return refused.map_or_else(||Ok(json!({"state":"cancelled; no retention act"})),Err);}
    let (actor,current)=observe()?;
    // Keep local record owners fixed during host revalidation/application.
    let links=state.native_links.try_lock().map_err(|_|"Native relationship recording busy; review again")?;
    if action=="close" && links.has_pending(){return Err("Native relationship records became pending; review again".into());}
    let workflows=state.workflows.try_lock().map_err(|_|"Workflow context busy; review again")?;
    let acts=state.act.try_lock().map_err(|_|"Act context busy; review again")?;
    if action=="close" {workflows.retention_ready()?;if acts.as_ref().is_some_and(|a|!a.writer_ready()){return Err("Native act records became pending; review again".into());}}
    records_retention::apply(plan,&actor,&current)
}
/// RS §13.8 "Project identity": the person resolves a project identity limit.
#[tauri::command(async)]
fn records_store_identity(state: State<'_, AppState>, action: String) -> Result<Value, String> {
    let project = state.workspace.as_ref().ok_or("no project is open; nothing changed")?;
    match action.as_str() {
        "adopt" => records_store::adopt(project),
        "new-identity" => records_store::new_identity(project),
        "restore-link" => records_store::restore_link(project),
        _ => Err("unknown records store identity action; nothing changed".into()),
    }
}
/// RS §13.8 "Placement": the person chooses where the records store is kept
/// (another volume, for example), from the next start.
#[tauri::command(async)]
fn records_store_choose(state: State<'_, AppState>, location: String) -> Result<Value, String> {
    let data = state.app_user_data_root.lock().unwrap().clone()?;
    let homes = state.homes.lock().unwrap();
    let configs: Vec<hosting::HostConfig> = [home_resources::HomeClass::Account, home_resources::HomeClass::ApiKey].into_iter()
        .filter_map(|class| homes.entry(class).ok()).filter_map(|home| home.host_config.as_ref().ok().cloned()).collect();
    drop(homes);
    records_store::choose_location(&data, std::path::Path::new(&location), state.workspace.as_deref(), &codex_homes(configs.iter()))
}
/// The App-owned and configured Codex homes (account, key and probe homes,
/// and the explicit home variables) the records store must stay out of.
fn codex_homes<'a>(configs: impl Iterator<Item = &'a hosting::HostConfig>) -> Vec<PathBuf> {
    let mut homes: Vec<PathBuf> = configs.flat_map(|cfg| [cfg.codex_home.clone(), cfg.probe_home.clone()]).collect();
    homes.extend(["CHIRALITY_CODEX_HOME", "CHIRALITY_KEY_HOME", "CODEX_HOME"].iter().filter_map(|key| std::env::var_os(key).filter(|v| !v.is_empty()).map(PathBuf::from)));
    homes.sort();
    homes.dedup();
    homes
}

#[tauri::command(async)]
fn read_connector_routes(state: State<'_ , AppState>) -> Value {
    connector_route_view::read(state.workspace.as_deref(), &state.project_context, state.project_context_limit.as_deref())
}


fn source_project(state:&AppState)->Result<&std::path::Path,String>{
    let access=connector_route_view::availability(state.workspace.as_deref(),&state.project_context,state.project_context_limit.as_deref());
    if access["enabled"]!=true{return Err(access.to_string());} Ok(state.workspace.as_deref().unwrap())
}
#[tauri::command]
fn prepare_connector_source(state:State<'_,AppState>,question:connector_source::Question,trigger:String,responsible:Option<String>)->Result<Value,String>{
    state.connector_sources.lock().map_err(|_|"Source state unavailable")?.prepare(source_project(&state)?,question,trigger,responsible)
}
#[tauri::command(async)]
fn select_connector_source(app:tauri::AppHandle,state:State<'_,AppState>,session_token:String,generation:String)->Result<Value,String>{
    source_project(&state)?;
    connector_source::select_native(&state.connector_sources,&session_token,&generation,||app.dialog().file().set_title("Observe one project text file (no send or save)").blocking_pick_file().map(|file|file.into_path().map_err(|e|format!("Selection is not a local file: {e}"))).transpose())
}
#[tauri::command]
fn anchor_connector_source(state:State<'_,AppState>,session_token:String,generation:String,observation_reference:String,start:usize,end:usize,expected:Option<String>)->Result<Value,String>{
    source_project(&state)?;state.connector_sources.lock().map_err(|_|"Source state unavailable")?.anchor(&session_token,&generation,&observation_reference,start,end,expected.as_deref())
}
#[tauri::command]
fn revise_connector_source(state:State<'_,AppState>,session_token:String,generation:String,observation_reference:String,kind:String,label:String,anchor_reference:Option<String>)->Result<Value,String>{
    source_project(&state)?;state.connector_sources.lock().map_err(|_|"Source state unavailable")?.revision(&session_token,&generation,&observation_reference,&kind,&label,anchor_reference.as_deref())
}


#[tauri::command(async)]
fn read_connector_git(state:State<'_,AppState>,session_token:String,generation:String,observation_reference:String,at:String,since:Option<String>)->Result<Value,String>{source_project(&state)?;
    #[cfg(unix)] {connector_source::git_read(&state.connector_sources,&session_token,&generation,&observation_reference,&at,since.as_deref())}
    #[cfg(not(unix))] {Err("Git adapter unsupported on this platform".into())}
}
#[tauri::command]
fn cancel_connector_git(state:State<'_,AppState>,session_token:String,generation:String)->Result<Value,String>{source_project(&state)?;
    #[cfg(unix)] {connector_source::git_cancel(&state.connector_sources,&session_token,&generation)}
    #[cfg(not(unix))] {Err("Git adapter unsupported on this platform".into())}
}
#[tauri::command]
fn anchor_connector_git(state:State<'_,AppState>,session_token:String,generation:String,observation_reference:String,side:String,start:usize,end:usize,expected:Option<String>)->Result<Value,String>{source_project(&state)?;
    #[cfg(unix)] {connector_source::git_anchor(&state.connector_sources,&session_token,&generation,&observation_reference,&side,start,end,expected.as_deref())}
    #[cfg(not(unix))] {Err("Git adapter unsupported on this platform".into())}
}

#[tauri::command(async)]
fn prepare_connector_reconstruction(state:State<'_,AppState>,input:connector_reconstruction::Input)->Result<Value,String>{
 let project=source_project(&state)?;
 #[cfg(any(target_os="macos",target_os="linux"))]
 {connector_reconstruction::prepare(&state.connector_drafts,&state.connector_sources,input,project)}
 #[cfg(not(any(target_os="macos",target_os="linux")))]
 {let _=(state,input,project);Err("Reconstruction unavailable on this platform".into())}
}
#[tauri::command(async)]
fn prepare_connector_draft(state:State<'_,AppState>,input:connector_materialization::PrepareInput)->Result<Value,String>{
    let project=source_project(&state)?;
    #[cfg(any(target_os="macos",target_os="linux"))] {connector_materialization::prepare(&state.connector_drafts,&state.connector_sources,input,project)}
    #[cfg(not(any(target_os="macos",target_os="linux")))] {Err("Materialization unsupported on this platform".into())}
}
#[tauri::command(async)]
fn publish_connector_draft(state:State<'_,AppState>,token:String,generation:String)->Result<Value,String>{
    #[cfg(any(target_os="macos",target_os="linux"))]
    if let Some(retained)=state.connector_drafts.lock().map_err(|_|"Draft registry unavailable")?.retained(&token,&generation)?{return Ok(retained);}
    let project=source_project(&state)?;
    #[cfg(any(target_os="macos",target_os="linux"))] {connector_materialization::publish(&state.connector_drafts,&state.connector_sources,&token,&generation,project)}
    #[cfg(not(any(target_os="macos",target_os="linux")))] {Err("Materialization unsupported on this platform".into())}
}
fn recheck_published_connector_for(state:&AppState,token:&str,generation:&str)->Result<Value,Value>{
    #[cfg(any(target_os="macos",target_os="linux"))]
    {connector_materialization::recheck(&state.connector_drafts,token,generation,||source_project(state).map(|p|p.to_path_buf()))}
    #[cfg(not(any(target_os="macos",target_os="linux")))]
    {let _=(state,token,generation);Err(json!({"kind":"unavailable","detail":"Published inspection unsupported on this platform"}))}
}
#[tauri::command(async)]
fn recheck_published_connector_draft(state:State<'_,AppState>,token:String,generation:String)->Result<Value,Value>{recheck_published_connector_for(&state,&token,&generation)}
#[tauri::command]
fn cancel_connector_draft(state:State<'_,AppState>,token:String,generation:String)->Result<Value,String>{
    #[cfg(any(target_os="macos",target_os="linux"))] {state.connector_drafts.lock().map_err(|_|"Draft registry unavailable")?.cancel(&token,&generation)}
    #[cfg(not(any(target_os="macos",target_os="linux")))] {Err("Materialization unsupported on this platform".into())}
}
#[tauri::command(async)]
fn reconcile_connector_draft(state:State<'_,AppState>,token:String,generation:String)->Result<Value,String>{
    #[cfg(any(target_os="macos",target_os="linux"))] {state.connector_drafts.lock().map_err(|_|"Draft registry unavailable")?.reconcile(&token,&generation)}
    #[cfg(not(any(target_os="macos",target_os="linux")))] {Err("Materialization unsupported on this platform".into())}
}
#[tauri::command]
fn inspect_connector_drafts(state:State<'_,AppState>)->Result<Value,String>{
    // Retained actual outcomes stay inspectable after source/project changes; no new file read.
    Ok(state.connector_drafts.lock().map_err(|_|"Draft registry unavailable")?.view())
}

fn home_class(mode: &str) -> Result<home_resources::HomeClass,String> {
    match mode { "account"=>Ok(home_resources::HomeClass::Account),"api-key"=>Ok(home_resources::HomeClass::ApiKey),_=>Err("Unknown active home class; no default/fallback".into()) }
}
#[tauri::command]
fn select_home(state: State<'_,AppState>, mode_home_class:String)->Result<Value,String>{
    let class=home_class(&mode_home_class)?;
    let mut homes=state.homes.lock().unwrap();
    homes.activate(class)?;
    let view=homes.snapshot();drop(homes);invalidate_endpoint_edits(&state)?;
    Ok(view)
}
#[tauri::command]
fn open_waiting_requests(state: State<'_, AppState>, mode_home_class: String, generation: Value, thread_id: Value) -> Result<Value, String> {
    waiting_requests::open(&mut state.homes.lock().unwrap(), &mode_home_class, &generation, &thread_id)
}
#[tauri::command(async)]
fn read_home_access(state:State<'_,AppState>,generation:Value,mode_home_class:String)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;
    if home.class()!=home_class(&mode_home_class)? {return Err("Selected class differs from the actual full-generation source".into());}
    state.validate_home_source(&home)?;
    let result=runtime_session::read_native_home_access(&home,&generation);
    state.validate_home_source(&home)?;
    result
}

#[tauri::command(async)]
fn read_configured_providers(state:State<'_,AppState>,generation:Value,mode_home_class:String)->Result<Value,String>{
    invalidate_endpoint_edits(&state)?;
    // Only the currently selected actual account source; no caller cwd/home,
    // alternate-home fallback, configuration write, model or capability read.
    let refused = || "Configured provider observation unavailable; original account source or scope changed; private diagnostic withheld".to_owned();
    let home=state.homes.lock().unwrap().active();
    if mode_home_class!="account" || home.class()!=home_resources::HomeClass::Account || home.host.snapshot()["generation"]!=generation {return Err(refused());}
    state.validate_home_source(&home).map_err(|_|refused())?;
    let cwd=home.host_config.as_ref().map_err(|_|refused())?.cwd.to_str().ok_or_else(refused)?.to_owned();
    let project=state.project_context.view();
    let view=home.host.configured_provider_read(&generation,&cwd,&project)?;
    state.validate_home_source(&home).map_err(|_|refused())?;
    let active=state.homes.lock().unwrap().active();
    if !Arc::ptr_eq(&active,&home) || home.host.snapshot()["generation"]!=generation || state.project_context.view()!=project
        || home.host.configured_provider_revision(&generation,&cwd)!=view["scope"]["readRevision"] {return Err(refused());}
    Ok(view)
}

#[tauri::command(async)]
fn logout_home(app:tauri::AppHandle,state:State<'_,AppState>,generation:Value,mode_home_class:String)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;
    if home.class()!=home_class(&mode_home_class)? {return Err("Logout mode differs from its actual source; no other-home fallback".into());}
    state.validate_home_source(&home)?;
    let bootstrap=state.home_bootstrap.lock().unwrap().as_ref().ok().cloned();
    let mut refused=None;
    let result=runtime_session::logout_native_home(&home,bootstrap.as_deref(),&generation,|assessment|confirm_bounded(&app,"Native home logout / remove key",act_control::native_statement::logout_statement(assessment),MessageDialogButtons::OkCancel,&mut refused));
    act_control::native_statement::refusal_or(refused,result)
}

#[tauri::command(async)]
fn oauth_start(app:tauri::AppHandle,state:State<'_,AppState>,generation:Value,mode:String)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;
    state.validate_home_source(&home)?;
    let mode=match mode.as_str(){"browser"=>hosting::NativeLoginMode::Browser,"device-code"=>hosting::NativeLoginMode::DeviceCode,_=>return Err("Unknown native sign-in mode; no default".into())};
    let bootstrap=state.home_bootstrap.lock().unwrap().as_ref().ok().cloned();
    let observed=runtime_session::start_native_oauth(&home,&generation,mode,bootstrap.as_deref(),||app.dialog().message("Sign in with your ChatGPT account through Codex in this original account home? A pending sign-in must be canceled first. The App receives safe observations only.").title("Native ChatGPT sign-in").buttons(MessageDialogButtons::OkCancel).blocking_show())?;
    runtime_session::automatic_native_oauth_presentation(&home,observed,bootstrap.as_deref()).map_err(|_|"Native sign-in presentation unavailable; original control/unknown state retained".into())
}
#[tauri::command(async)]
fn oauth_present(state:State<'_,AppState>,generation:Value)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;
    state.validate_home_source(&home)?;
    let bootstrap=state.home_bootstrap.lock().unwrap().as_ref().ok().cloned();
    runtime_session::present_native_oauth(&home,&generation,bootstrap.as_deref()).map_err(|_|"Native sign-in presentation unavailable; no raw material or replacement".into())
}
#[tauri::command(async)]
fn oauth_cancel(app:tauri::AppHandle,state:State<'_,AppState>,generation:Value)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;
    state.validate_home_source(&home)?;
    let bootstrap=state.home_bootstrap.lock().unwrap().as_ref().ok().cloned();
    let mut refused=None;
    let result=runtime_session::cancel_native_oauth(&home,&generation,bootstrap.as_deref(),|safe|confirm_bounded(&app,"Cancel original pending sign-in",act_control::native_statement::oauth_cancel_statement(safe),MessageDialogButtons::OkCancel,&mut refused));
    act_control::native_statement::refusal_or(refused,result)
}

#[tauri::command(async)]
fn add_api_key(app:tauri::AppHandle,state:State<'_,AppState>)->Result<Value,String>{
    let _operation=state.key_setup.try_lock().map_err(|_|"Another explicit key operation is pending; no duplicate/retry")?;
    let bootstrap=state.home_bootstrap.lock().unwrap().clone()?;
    bootstrap.key_plan()?;
    if !app.dialog().message("Add or replace an API key through the separate App key home? Its explicit resource links may be prepared and its Codex child started. Existing account conversations are not transferred.").title("Separate API-key home").buttons(MessageDialogButtons::OkCancel).blocking_show(){return Ok(json!({"state":"cancelled; no key setup/login"}));}
    let data=state.app_user_data_root.lock().unwrap().clone()?;
    let account=state.homes.lock().unwrap().entry(home_resources::HomeClass::Account)?;
    let app_custody=account.host.app_runtime_custody()?;
    let authority=account.attachment_custody.lock().unwrap().as_ref().map_err(Clone::clone)?.authority()?;
    let entries=state.homes.lock().unwrap().entries();
    let mut stores=Vec::new();for entry in &entries{let required=entry.host_config.as_ref().map_err(Clone::clone)?.distribution.is_some();if let Some(store)=entry.host.distribution_store_for_admission(required)?{if !stores.iter().any(|old|Arc::ptr_eq(old,&store)){stores.push(store);}}}
    let account_store=account.host.distribution_store_for_admission(account.host_config.as_ref().map_err(Clone::clone)?.distribution.is_some())?;
    let admitted=match runtime_session::prepare_native_key_namespace_coordinated(&bootstrap,&data,&app_custody,&authority,&stores,|admitted|{
        *state.native_namespaces.lock().unwrap()=Ok(admitted.namespaces.clone());
        *state.key_namespace_admission.lock().unwrap()=admitted.observation.clone();
        for entry in &entries{*entry.attachment_custody.lock().unwrap()=Ok(admitted.attachment.clone());}
    }) {
        Ok(admitted)=>admitted,
        Err(error)=>{*state.key_namespace_admission.lock().unwrap()=json!({"state":"key namespace/setup refused before admission; original bindings retained","limit":error,"existingAccount":"current ledger/custody bindings retained; physical preparation may remain"});return Err(error);}
    };
    let attachment=admitted.attachment;
    let existing=state.homes.lock().unwrap().entry(home_resources::HomeClass::ApiKey);
    let home=runtime_session::admitted_key_setup(&state.key_namespace_admission,&admitted.observation,||->Result<Arc<runtime_session::HomeSession>,String>{
        Ok(match existing{
            Ok(home)=>home,
            Err(_)=>{
                let account=state.homes.lock().unwrap().entry(home_resources::HomeClass::Account)?;
                let mut config=account.host_config.clone()?;
                config.codex_home=bootstrap.key_plan()?.native_path().to_path_buf();
                bootstrap.validate_binding(home_resources::HomeClass::ApiKey,&config)?;
                let custody=account.host.app_runtime_custody()?;
                let host=Arc::new(Host::new_with_app_custody(custody)?);
                if let Some(store)=&account_store{host.configure_distribution_store(Ok(store.clone()));}
                // RS §13.9: the same project's records capability on this home's conversations.
                if let Some(capability)=account.host.records_capability(){
                    if let Some(context)=account.host.records_project_context(){host.configure_records_capability_with_context(capability,context);}else{host.configure_records_capability(capability);}
                }
                let home=Arc::new(runtime_session::HomeSession::new(home_resources::HomeClass::ApiKey,host,Ok(config.clone()))?);
                home.history.lock().unwrap().configure_role_log_source(state.role_log.clone());
                *home.attachment_custody.lock().unwrap()=Ok(attachment.clone());
                home.recovery_startup.lock().unwrap().adopt_shared_source(&home.host);
                bootstrap.validate_binding(home.class(),&config)?;
                state.homes.lock().unwrap().bind_key(home.clone())?;
                home
            }
        })
    })?;
    let config=runtime_session::admitted_key_setup(&state.key_namespace_admission,&admitted.observation,|| {
    let config=home.host_config.clone()?;
    bootstrap.validate_binding(home.class(),&config)?;
    if home.host.snapshot()["state"]!="ready" {
        let data=state.app_user_data_root.lock().unwrap().clone()?;
        runtime_session::start_with_recovery(&home.host,&home.recovery_startup,Ok(data.as_path()),Some(&config.codex_home),||home.host.start(&config,"the person: add-key"))?;
    }
    bootstrap.validate_binding(home.class(),&config)?;Ok(config)})?;
    let _=config;
    let generation=home.host.snapshot()["generation"].clone();
    runtime_session::submit_native_home_key(&home,&bootstrap,&generation,||runtime_session::native_api_key_entry(&app))
}

#[tauri::command(async)]
fn host_start(state: State<'_, AppState>, mode_home_class:String) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().entry(home_class(&mode_home_class)?)?;
    start_home(&state, &home, "the person")
}
/// Start Codex for one home (Start Codex, and Restart Codex after its stop).
fn start_home(state: &AppState, home: &runtime_session::HomeSession, actor: &str) -> Result<Value, String> {
    invalidate_endpoint_edits(state)?;
    let cfg = home.host_config.clone()?;
    state.validate_home_source(home)?;
    let root = state.app_user_data_root.lock().unwrap().clone();
    runtime_session::start_with_recovery(
        &home.host,
        &home.recovery_startup,
        root.as_deref().map_err(String::as_str),
        Some(&cfg.codex_home),
        || home.host.start(&cfg, actor),
    )
}

/// Stop Codex and Restart Codex (DEL-01-04 §5.2, C-12). The person is always
/// asked first in a native question; there is no command that stops Codex
/// without it (the App quit path is separate). See `codex_stop`.
#[tauri::command(async)]
fn codex_stop(app: tauri::AppHandle, state: State<'_, AppState>, generation: Value, restart: bool) -> Result<Value, String> {
    let _question = codex_stop::question_gate(&state.codex_stop_gate)?;
    app_quit::admit_codex_stop(&state.app_quit)?;
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    if restart {
        codex_stop::restart_precheck(home.host_config.as_ref().map(|_| ()).map_err(Clone::clone), || state.validate_home_source(&home))?;
    }
    let (title, act) = if restart { ("Restart Codex", act_control::native_statement::RESTART_CODEX) } else { ("Stop Codex", act_control::native_statement::STOP_CODEX) };
    let mut refused = None;
    let person = stop_person(&state, &home);
    let result = codex_stop::stop_native_home(&home, &state.workflows, &generation, restart, &person,
        |view| confirm_choice(&app, title, act_control::native_statement::codex_stop_statement(view), act_control::native_statement::KEEP_CODEX, act, &mut refused),
        || start_home(&state, &home, "the person: Restart Codex"));
    codex_stop::finish(&state.codex_stops, title, refused, result)
}

/// The App's own Quit menu item (K-4). The predefined Quit item sends
/// `terminate:`, which ends the App without asking.
const QUIT_MENU_ID: &str = "chirality-quit";
/// Tauri's default menu with its predefined Quit replaced by the App's own,
/// at the same place and with the same shortcut.
fn app_menu(app: &tauri::AppHandle) -> tauri::Result<tauri::menu::Menu<tauri::Wry>> {
    use tauri::menu::{Menu, MenuItem, MenuItemKind, Submenu};
    let menu = Menu::default(app)?;
    #[cfg(target_os = "macos")]
    native_waiting::append_menu(app, &menu)?;
    let quit = MenuItem::with_id(app, QUIT_MENU_ID, format!("Quit {}", app.package_info().name), true, Some("CmdOrCtrl+Q"))?;
    for top in menu.items()? {
        let MenuItemKind::Submenu(sub) = top else { continue };
        for (at, item) in sub.items()?.into_iter().enumerate() {
            let MenuItemKind::Predefined(predefined) = item else { continue };
            let text = predefined.text()?;
            let text = text.trim_start_matches('&');
            if text.starts_with("Quit") || text.starts_with("Exit") {
                sub.remove_at(at)?;
                sub.insert(&quit, at)?;
                return Ok(menu);
            }
        }
    }
    menu.append(&Submenu::with_items(app, "File", true, &[&quit])?)?;
    Ok(menu)
}
// Menu dispatch only queues navigation; activation stays behind the App's guards.
fn request_native_waiting(app: &tauri::AppHandle, id: &str) {
    use tauri::Emitter;
    let state = app.state::<AppState>();
    let result = {
        let homes = state.homes.lock().unwrap();
        app.state::<Mutex<native_waiting::Registry>>().lock().unwrap().select(id, &homes)
    };
    show_main_window(app);
    if let Err(reason) = result {
        app.dialog().message(reason).title("Waiting requests").kind(MessageDialogKind::Info).show(|_| {});
    } else {
        // This is a wake-up only. The host retains the original pending target
        // even if there is no listener yet or this emit fails.
        let _ = app.emit_to("main", native_waiting::WAKE_EVENT, ());
    }
}
#[tauri::command]
fn checkpoint_native_waiting_ui(registry: State<'_, Mutex<native_waiting::Registry>>, consumer: String, revision: u64) -> Result<(), String> {
    registry.lock().unwrap().checkpoint(&consumer, revision)
}
#[tauri::command]
fn claim_native_waiting_intent(state: State<'_, AppState>, registry: State<'_, Mutex<native_waiting::Registry>>, consumer: String) -> Value {
    let homes = state.homes.lock().unwrap();
    registry.lock().unwrap().claim(&consumer, &homes)
}
#[tauri::command]
fn finish_native_waiting_intent(registry: State<'_, Mutex<native_waiting::Registry>>, consumer: String, intent_id: Option<String>) -> Result<(), String> {
    let mut registry = registry.lock().unwrap();
    match intent_id { Some(id) => registry.finish(&consumer, &id), None => { registry.abandon(&consumer); Ok(()) } }
}
/// DEF-1 / SQ-W W-4: show the App's window again (the Dock click on macOS,
/// or before the quit question so that content it names is visible).
fn show_main_window(app: &tauri::AppHandle) {
    if let Some(window) = app.webview_windows().into_values().next() {
        let _ = window.unminimize();
        let _ = window.show();
        let _ = window.set_focus();
    }
}
/// K-4 / SQ-Q: the person chose Quit. Runs off the main thread (the native
/// question blocks); one question at a time; the web view takes no part.
fn request_quit(app: tauri::AppHandle) {
    std::thread::spawn(move || {
        let state = app.state::<AppState>();
        if state.app_quit.proceeding().is_some() {
            app.exit(0);
            return;
        }
        // One operation over the Codex processes at a time (Stop/Restart
        // Codex or quit); a second Quit while the question is open (or this
        // quit is under way) is ignored, since that question is in front of
        // the person. Any other refusal is told in a dialog.
        let _held = match app_quit::admit_quit(&state.app_quit, &state.codex_stop_gate) {
            Ok(held) => held,
            Err(reason) if reason.starts_with("The quit question") => return,
            Err(reason) => {
                show_main_window(&app);
                let _ = app.dialog().message(reason).title("Quit Chirality").kind(MessageDialogKind::Info).buttons(MessageDialogButtons::Ok).blocking_show();
                return;
            }
        };
        let homes = state.homes.lock().unwrap().entries();
        let active = state.homes.lock().unwrap().active();
        let person = stop_person(&state, &active);
        let shown = app.clone();
        let mut ops = app_quit::HostQuit::new(homes, &state.workflows, &person, move |view: &Value| {
            use act_control::native_statement as ns;
            show_main_window(&shown);
            let mut refused = None;
            let chosen = confirm_choice(&shown, "Quit Chirality", ns::quit_statement(view), ns::KEEP_RUNNING, ns::QUIT_APP, &mut refused);
            match refused { Some(cause) => Err(cause), None => Ok(chosen) }
        });
        let decision = app_quit::quit_sequence(&mut ops, app_quit::QUIT_WAIT_LIMIT);
        drop(ops);
        if let app_quit::Decision::NotAsked(outcome) = &decision {
            eprintln!("chirality: {}", outcome["reading"].as_str().unwrap_or("quit question not shown"));
        }
        if state.app_quit.allow(&decision) {
            app.exit(0);
        }
    });
}
/// C-24 (DEL-01-04 §4.8): the count of supplier requests waiting for the
/// person, on the App's Dock icon, whether or not the window is shown.
fn show_waiting_indicator(app: &tauri::AppHandle, last: &mut Option<i64>, menu: &mut native_waiting::MenuObserver) {
    let state = app.state::<AppState>();
    let snapshots: Vec<Value> = state.homes.lock().unwrap().entries().iter().map(|home| home.host.snapshot()).collect();
    let overview = waiting_requests::overview(&state.homes.lock().unwrap());
    if let Err(error) = menu.update(app, app.state::<Mutex<native_waiting::Registry>>().inner(), &overview) {
        eprintln!("chirality: waiting menu update failed: {error}");
    }
    let count = app_quit::waiting_requests(&snapshots)["count"].as_i64().unwrap_or(0);
    if *last != Some(count) {
        if let Some(window) = app.webview_windows().into_values().next() {
            if window.set_badge_count((count > 0).then_some(count)).is_ok() {
                *last = Some(count);
            }
        }
    }
}

fn role_set_metadata() -> Value {
    let identity = role_supply::content(role_supply::BUNDLED_ROLE_SET);
    match role_supply::bundled_role_set() {
        // ROLE SL-1 (owner ruling 2026-10-10): the four standing roles stay in
        // the set; only those that may start a conversation are offered as one.
        Ok(set) => json!({"available":true,"roles":set.roles,"defaultRole":set.default_role(),
            "conversationRoles":role_supply::Role::ALL.into_iter().filter(|r|r.primary_entry()).collect::<Vec<_>>(),
            "identity":identity,"standing":"candidate; U-R6/U-R11 open"}),
        Err(reason) => json!({"available":false,"reason":reason,"identity":identity}),
    }
}
/// The App resources a non-dev build reads from `resource_dir()` in its
/// default configuration (PKG §4.1 P-2/P-3): `tauri.conf.json` `bundle.resources` maps
/// each from `resources/` (see `bundle_resources_tests`). Feature-gated
/// readers (`distribution-successor`'s `codex/` and `distribution-reference/`,
/// `synthetic-distribution-anchor`'s namespace) are supplied by their own
/// overlays.
const RESOURCE_INSTRUCTIONS: &str = "instructions";
const RESOURCE_WORKFLOWS: &str = "workflows";
/// Native build mode chooses the source, never file existence or a failed package check.
fn prepare_role_entry(
    root: &std::path::Path,
    role: Option<role_supply::Role>,
    development: bool,
    resource_root: impl FnOnce() -> Result<PathBuf, String>,
) -> Result<(role_supply::Composition, Value), String> {
    let package = if development {
        role_supply::bundled_role_set()?;
        json!({"standing":"development-embedded-candidate","roleSet":role_supply::content(role_supply::BUNDLED_ROLE_SET),"releaseQualified":false})
    } else {
        runtime_session::verify_production_instructions_root(&resource_root()?)?
    };
    let composition = runtime_session::compose_role(root, role)?;
    Ok((composition, package))
}
#[tauri::command(async)]
fn role_supply_history(state:State<'_,AppState>,generation:Value,thread:Option<String>)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;
    let name=generation["home"].as_str().ok_or("actual native home absent")?;
    let view=home.history.lock().unwrap().read_role_supply(name,thread.as_deref());if home.host.snapshot()["generation"]!=generation{return Err("native home generation changed during role history read; refresh the selection".into());}Ok(view)
}
fn refused_role_entry(role: Option<role_supply::Role>, reason: &str) -> Value {
    json!({"state":"refused-before-send","selection":role,"roleSet":role_supply::content(role_supply::BUNDLED_ROLE_SET),"reason":reason,"adoption":"unknown"})
}

#[tauri::command(async)]
#[allow(clippy::too_many_arguments)]
fn thread_start(
    app: tauri::AppHandle,
    state: State<'_, AppState>,
    model: String,
    model_provider: String,
    entry_id: String,
    mode_home_class: String,
    role: Option<role_supply::Role>,
    preselected: Option<bool>,
    continue_as: Option<String>,
) -> Result<Value, String> {
    start_conversation(&app, &state, model, model_provider, entry_id, &mode_home_class, role, continue_as, preselected)
}
/// A new conversation as `thread_start` starts it (ROLE T-2): also the start of
/// a clean trial's conversation (WR FT-4), which passes no `continue_as`.
#[allow(clippy::too_many_arguments)]
fn start_conversation(
    app: &tauri::AppHandle,
    state: &AppState,
    model: String,
    model_provider: String,
    entry_id: String,
    mode_home_class: &str,
    role: Option<role_supply::Role>,
    continue_as: Option<String>,
    preselected: Option<bool>,
) -> Result<Value, String> {
    let supply_ref=util::opaque_id("sup:")?;
    let home=home_class(mode_home_class).and_then(|class|state.homes.lock().unwrap().entry(class));
    let generation=home.as_ref().map(|home|home.host.snapshot()["generation"].clone()).unwrap_or(Value::Null);
    let mut dispatch_invoked=false;
    let mut resolved_continued_from=None;
    let result=start_conversation_inner(app,state,model,model_provider,entry_id,mode_home_class,role,continue_as,preselected,&supply_ref,&mut dispatch_invoked,&mut resolved_continued_from);
    if let Err(reason)=&result {
        if !dispatch_invoked {
            let mut history=runtime_session::HistorySession::default();history.configure_role_log_source(state.role_log.clone());
            let publication=history.role_refused_continuing(&supply_ref,&generation,role,preselected,reason,true,resolved_continued_from);
            if let Ok(home)=home{home.role_supply_status.lock().unwrap()["roleSupplyRecord"]=publication.clone();}
            return Err(format!("{reason}; role supply observation: {publication}"));
        }
    }
    result
}
#[allow(clippy::too_many_arguments)]
fn start_conversation_inner(app:&tauri::AppHandle,state:&AppState,model:String,model_provider:String,entry_id:String,mode_home_class:&str,role:Option<role_supply::Role>,continue_as:Option<String>,preselected:Option<bool>,supply_ref:&str,dispatch_invoked:&mut bool,resolved_continued_from:&mut Option<Value>)->Result<Value,String>{
    invalidate_endpoint_edits(state)?;
    let home = state.homes.lock().unwrap().entry(home_class(mode_home_class)?)?;
    home.history.lock().unwrap().configure_role_log_source(state.role_log.clone());
    // NIR CA-1/CA-3, ROLE CA-3: a "Continue as" start is an ordinary new start
    // with its own role composition; it only records its relation to the source.
    let (continued_from, continued_source) = conversation_roles::continuation_for_start_observed(&state.continue_as, &home, continue_as.as_deref(), role)?;
    *resolved_continued_from=continued_from.clone();
    let cwd = home.host_config
        .as_ref()
        .map_err(Clone::clone)?
        .cwd.to_str().ok_or("Native working directory is not Unicode; thread/start cannot carry a lossless JSON cwd, no request sent")?.to_owned();
    let allowed = match home.class() { home_resources::HomeClass::Account=>matches!(entry_id.as_str(),"chatgpt-account"|"local-provider"),home_resources::HomeClass::ApiKey=>entry_id=="api-key",home_resources::HomeClass::Probe=>false };
    if !allowed { return Err("Access entry differs from the selected actual home class; no native transfer/fallback".into()); }
    if let Ok(set) = &*state.home_bootstrap.lock().unwrap() { set.validate_binding(home.class(),home.host_config.as_ref().map_err(Clone::clone)?)?; }
    else if home.class()==home_resources::HomeClass::ApiKey {return Err("Explicit key source binding is unavailable".into());}
    let prepared = (|| {
        let root = state.instructions_root.lock().unwrap().clone()?;
        prepare_role_entry(&root, role, tauri::is_dev(), || {
            app.path().resource_dir().map(|path| path.join(RESOURCE_INSTRUCTIONS))
                .map_err(|error| format!("Production instruction resource directory unavailable: {error}"))
        })
    })();
    let (mut composition, package_correspondence) = match prepared {
        Ok(prepared) => prepared,
        Err(reason) => {
            *home.role_supply_status.lock().unwrap() = refused_role_entry(role, &reason);
            return Err(reason);
        }
    };
    composition.verify()?;
    let generation = home.host.snapshot()["generation"].clone();
    let mut provider_admission=home.host.provider_admission_read(&generation,&cwd,&entry_id,&model_provider,&model)?;
    if let Ok(set)=&*state.home_bootstrap.lock().unwrap(){
        if let Ok(Some(link))=set.child_role_config_link(home.class(),home.host_config.as_ref().map_err(Clone::clone)?){home.host.role_config_link(&mut provider_admission,link);}
    }
    let instruction_root=state.instructions_root.lock().unwrap().clone()?;
    let data_root=state.app_user_data_root.lock().unwrap().clone();
    match data_root {
        Ok(data)=>home.host.prepare_role_children(&mut provider_admission,&mut composition,&instruction_root,&data)?,
        Err(_)=>{crate::child_roles::prepare(&mut composition,Err("App data unavailable".into()),&instruction_root,std::path::Path::new("/unavailable"));},
    }
    let mut native_relationship = continued_source.map(|origin| (native_conversation_links::freeze_source(state.workspace.as_deref(), &home), origin));
    let attempt_id = util::opaque_id("conversation:")?;
    let frozen_project = state.project_context.clone();
    let mut selection = access::ConversationSelection::new_explicit(&attempt_id, frozen_project.reference())?;
    selection.choose(&entry_id, &model_provider, &model, false)?;
    selection.start_params(&generation, home.class().as_str(), false)?;
    let recovery_home = selection.recovery_home();
    // Serialize the claim; fallible no-effect preparation completes before
    // either shared state publishes Starting. Transport waits hold no slot lock.
    let supply_ref = {
        let mut slot = home.access_selection.lock().unwrap();
        let supply_ref = runtime_session::claim_start(&mut slot, selection, || Ok(supply_ref.to_owned()))?;
        *home.role_supply_status.lock().unwrap() = json!({"state":"starting","attemptId":attempt_id,"supplyRef":supply_ref,"selection":role,"roleSet":composition.role_set_identity(),"packageCorrespondence":package_correspondence,"generation":generation,"carried":composition.carried,"adoption":"unknown","nativeChildRoles":composition.carried["nativeChildRoles"],"childNamespaceObservation":composition.child_reading,"continuedFrom":continued_from});
        supply_ref
    };
    // Freeze the verified original composition before native dispatch. Actual
    // Host receipt IDs, exact sent bytes and correlated results bind its role.
    *dispatch_invoked=true;
    let dispatch = home.host.thread_start_with_role_dispatch(&provider_admission, &composition);
    // All post-claim failures flow through finalization; ? cannot strand Starting.
    let result = (|| -> Result<Value, String> { match dispatch {
        Ok(receipt) => {
            if let Some((context, origin)) = native_relationship.take() {
                // Retain the genuine receipt before any wait or role callback.
                // Recording limits never replace the native operation result.
                if let Ok(mut links) = state.native_links.lock() {
                    let _ = links.track_continued(context, Arc::clone(&home.host), receipt.clone(), origin);
                }
            }
            home.history.lock().unwrap().start_dispatched_selected(receipt.clone(), &composition, &supply_ref, continued_from.clone(), preselected)
                .map_err(|error| format!("Native start dispatched; original role preparation failed: {error}. Native effect remains as observed in the retained receipt; no automatic resend"))?;
            let waited = home.host.source_request_wait(&receipt, std::time::Duration::from_secs(20));
            home.history.lock().unwrap().reconcile(&home.host);
            match waited {
                Ok(evidence) if home.history.lock().unwrap().start_admitted(&receipt) => Ok(evidence["response"].clone()),
                Ok(evidence) => Err(format!("Native start remains {} (write {}); no automatic retry", evidence["outcome"], evidence["writeResult"])),
                Err(error) => Err(error),
            }
        },
        Err(error) => {
            let publication=home.history.lock().unwrap().role_refused_continuing(&supply_ref,&generation,role,preselected,&error,false,continued_from.clone());
            home.role_supply_status.lock().unwrap()["roleSupplyRecord"]=publication;
            Err(format!("{error}; role supply observation: {}",home.role_supply_status.lock().unwrap()["roleSupplyRecord"]))
        },
    } })();
    let record_status=home.history.lock().unwrap().role_record_status(&supply_ref);
    let record_status=if record_status.is_null(){home.role_supply_status.lock().unwrap()["roleSupplyRecord"].clone()}else{record_status};
    let result = {
        let mut slot = home.access_selection.lock().unwrap();
        let result = match slot.as_mut() {
            Some(selection) => runtime_session::finalize_start_attempt(selection, &attempt_id, &generation, &home.host.snapshot()["generation"], result),
            None => Err("Start selection unavailable; native effect remains as observed in retained receipts".into()),
        };
        let mut status = home.role_supply_status.lock().unwrap();
        if status["attemptId"] == attempt_id && status["generation"] == generation {
            *status = json!({"state":if result.is_ok(){"response-observed"}else{"start-failed-or-unknown"},"attemptId":attempt_id,"supplyRef":supply_ref,"selection":role,"roleSet":composition.role_set_identity(),"packageCorrespondence":package_correspondence,"generation":generation,"carried":composition.carried,"adoption":"unknown","nativeChildRoles":composition.carried["nativeChildRoles"],"childNamespaceObservation":composition.child_reading,"continuedFrom":continued_from});
        }
        if !record_status.is_null(){status["roleSupplyRecord"]=record_status.clone();}
        result
    };
    conversation_roles::mark_started(&state.continue_as, continue_as.as_deref(), &result, &generation);
    // The start's own generation, for a caller that continues in the new
    // conversation (a clean trial's first turn, WR FT-4).
    let result = result.map(|mut response| { response["startGeneration"] = generation.clone(); response["roleSupplyRecord"]=record_status.clone(); response });
    if let Ok(response) = &result {
        if let Some(thread) = response["result"]["thread"]["id"].as_str() {
            if let Some(home_kind) = recovery_home { home.thread_home_kinds.lock().unwrap().insert(serde_json::to_string(&json!([generation,thread])).unwrap(),home_kind); }
            let _ = home.host.observe_conversation_project(&generation,thread,recovery_home,&frozen_project);
        }
    }
    result
}

/// Stored history is a native read view. Only explicit Continue asks for resume;
/// the private Host receipt and current history revision govern active admission.
#[tauri::command(async)]
fn history_action(
    state: State<'_, AppState>, generation: Value, selection_epoch: u64,
    action: String, cursor: Option<String>, direction: String,
    reference: Option<String>,
) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    let query = {
        let mut history = home.history.lock().unwrap();
        history.reconcile(&home.host);
        history.prepare(&home.host.snapshot(), &generation, selection_epoch, &action, cursor.as_deref(), match direction.as_str() { "asc" => native_history::Direction::Asc, "desc" => native_history::Direction::Desc, _ => return Err("Invalid history paging direction".into()) }, reference.as_deref())?
    };
    let receipt = home.host.history_dispatch(&query)?;
    home.history.lock().unwrap().dispatched_manual(receipt.clone());
    let waited = home.host.history_wait(&receipt, std::time::Duration::from_secs(20));
    // Only the original accepted manual page can enter native activity. The
    // shared receiver also delivers pages accepted by an earlier host tick.
    home.reconcile_manual_history();
    waited?;
    let root = state.instructions_root.lock().unwrap().clone();
    let snapshot = home.history.lock().unwrap().snapshot(root.as_deref().ok());
    Ok(snapshot)
}
#[tauri::command]
fn history_select(state: State<'_, AppState>, generation: Value, selection_epoch: u64, thread_id: String) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    let mut history = home.history.lock().unwrap();
    history.reconcile(&home.host);
    history.select(&home.host.snapshot(), &generation, selection_epoch, &thread_id)?;
    let root = state.instructions_root.lock().unwrap().clone();
    Ok(history.snapshot(root.as_deref().ok()))
}
/// Read-only prior-work controls for an already privately admitted Continue.
/// Queueing never resumes a conversation or waits on native history IO.
#[tauri::command]
fn continuation_context_action(state: State<'_, AppState>, generation: Value, thread_id: String,
    resume_request_ref: String, revision: u64, action: String, cursor: Option<String>, direction: String, turn_id: Option<String>) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    let direction = match direction.as_str() { "asc" => native_history::Direction::Asc, "desc" => native_history::Direction::Desc, _ => return Err("Invalid context paging direction".into()) };
    home.host.continuation_context_action(&generation, &thread_id, &resume_request_ref, revision, &action, cursor.as_deref(), direction, turn_id.as_deref())
}

#[tauri::command(async)]
fn conversation_send_text(
    state: State<'_, AppState>, generation: Value, thread_id: String,
    text: String, mode: Option<String>, model: Option<String>,
) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    ordinary_send_text(&home, &state.workflows, &generation, &thread_id, &text, mode.as_deref(), model.as_deref())
}
/// Actual IPC consumer, also exercised with an invented native peer offline.
fn ordinary_send_text(home: &runtime_session::HomeSession, workflows: &std::sync::Mutex<runtime_session::WorkflowRootSession>, generation: &Value, thread: &str, text: &str, mode: Option<&str>, model: Option<&str>) -> Result<Value, String> {
    // TC-2: one original ordered notice/person frame, with the same mode/model.
    if let Some(sent) = runtime_session::send_with_pending_notice_model_observed(workflows, generation, thread, text, mode, model, &mut |_| {}) {
        return sent.result;
    }
    runtime_session::send_conversation_text(&home.host.snapshot(), generation, thread, text,
        |generation, thread, text| home.host.turn_start_ordinary_text(generation, thread, text, mode, model))
}

/// EX-2/EX-3 availability read for the plan-mode element.
#[tauri::command(async)]
fn collaboration_modes_read(state: State<'_, AppState>, generation: Value) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    home.host.collaboration_modes_read(&generation)
}

#[tauri::command(async)]
fn conversation_steer_text(
    state: State<'_, AppState>, generation: Value, thread_id: String,
    expected_turn_id: String, text: String,
) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    runtime_session::steer_conversation_turn(
        &home.host.snapshot(), &generation, &thread_id, &expected_turn_id, &text,
        |generation, thread, expected, text| home.host.turn_steer_text(generation, thread, expected, text),
    )
}

#[tauri::command(async)]
fn conversation_interrupt(
    state: State<'_, AppState>,
    generation: Value,
    thread_id: String,
    turn_id: String,
) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    // REC SR (DEL-01-02 §3.4): the stop request names the App-owned home and
    // the person as the App observes them; it is recorded before the send.
    let home_class = stop_records::home_class(home.class().as_str()).ok_or("This home has no App-owned home class; nothing sent")?;
    let person = stop_records::person(&stop_person(&state, &home));
    runtime_session::interrupt_conversation_turn(
        &home.host.snapshot(),
        &generation,
        &thread_id,
        &turn_id,
        |generation, thread, turn| home.host.turn_interrupt(generation, thread, turn, home_class, &person),
    )
}
/// The person as a stop request names them (K1-4): the App's name setting
/// and the OS account, never verified.
fn stop_person(state: &AppState, home: &Arc<runtime_session::HomeSession>) -> String {
    let (_, context) = current_actor_context_for(state, home);
    let actor = act_control::person(context["displayName"].as_str(), context["osAccount"].as_str());
    let line = act_control::native_statement::actor_line(&actor);
    line.strip_suffix(" (identity not verified)").unwrap_or(&line).to_owned()
}

/// NIR §5.8 CA-1/CA-2, ROLE §3.3: "Continue as ‹role›". Asks the source
/// conversation's agent for a handoff summary in a visible ordinary turn
/// there; the new conversation is started later by `thread_start` with this
/// handoff. The source conversation's role is unchanged.
#[tauri::command(async)]
fn continue_as_begin(state: State<'_, AppState>, generation: Value, thread_id: String, role: Option<role_supply::Role>) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    conversation_roles::continue_as_begin(&state.continue_as, &state.workflows, &home, &generation, &thread_id, role)
}

#[tauri::command]
fn continue_as_dismiss(state: State<'_, AppState>, id: String) -> Result<(), String> {
    state.continue_as.lock().unwrap().dismiss(&id)
}

#[tauri::command(async)]
fn continue_as_send(state: State<'_, AppState>, id: String, text: String) -> Result<Value, String> {
    conversation_roles::send_handoff(&state.continue_as, &state.homes, &state.workflows, &id, &text)
}

#[tauri::command(async)]
fn continue_as_send_read(state: State<'_, AppState>, id: String) -> Result<Value, String> {
    conversation_roles::read_handoff_send(&state.continue_as, &id)
}

/// NIR CA-4, ROLE F-1: "Fork (same role)".
#[tauri::command(async)]
fn conversation_fork(state: State<'_, AppState>, generation: Value, thread_id: String) -> Result<Value, String> {
    let routed=state.homes.lock().unwrap().for_generation(&generation);
    let home=match routed {Ok(home)=>home,Err(reason)=>{
        let mut history=runtime_session::HistorySession::default();history.configure_role_log_source(state.role_log.clone());
        let publication=history.fork_refused(&util::opaque_id("sup:")?,&Value::Null,&thread_id,&reason,true);
        return Err(format!("{reason}; role supply observation: {publication}"));
    }};
    let context = native_conversation_links::freeze_source(state.workspace.as_deref(), &home);
    let forked = conversation_roles::fork_conversation_tracked(&home, &generation, &thread_id, std::time::Duration::from_secs(20), |receipt| {
        if let Ok(mut links) = state.native_links.lock() {
            let _ = links.track_fork(context, Arc::clone(&home.host), receipt.clone());
        }
    })?;
    // WR TT-3b: a fork of a trial conversation is labelled and offers no run.
    if let Some(fork) = forked["thread"]["threadId"].as_str() {
        state.workflows.lock().unwrap().mark_fork(&thread_id, fork);
    }
    Ok(forked)
}

/// Paths come exclusively from native file selection; no path/origin is an IPC argument.
#[tauri::command(async)]
fn submit_attachments(state:State<'_,AppState>,owner_ref:String,list_revision:u64,selection_refs:Vec<String>,generation:Value,thread_id:String,expected_turn_id:Option<String>,text:String)->Result<Value,String>{
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    let context=state.project_context.clone();
    let recovery_home=home.thread_home_kinds.lock().unwrap().get(&serde_json::to_string(&json!([generation,thread_id])).unwrap()).copied();
    let custody=home.attachment_custody.lock().unwrap().clone();
    runtime_session::submit_attachments_with_pending_notice(&state.attachment_selection,&state.workflows,&home.host,custody,&owner_ref,list_revision,&selection_refs,&generation,&thread_id,expected_turn_id.as_deref(),&text,context,recovery_home)
}

/// The native selector is the only attachment path/body authority. JS carries
/// known owner/revision references only, never selected source bodies or paths.
#[tauri::command(async)]
fn select_attachment(app: tauri::AppHandle, state: State<'_, AppState>, owner_ref: String, list_revision: u64) -> Result<Value,String> {
    runtime_session::select_attachment_source(&state.attachment_selection,&owner_ref,list_revision,|| {
        app.dialog().file().set_title("Select a UTF-8 text attachment")
            .blocking_pick_file().map(|file|file.into_path().map_err(|error|format!("Native attachment selection is not a filesystem path: {error}"))).transpose()
    })
}
#[tauri::command]
fn remove_attachment(state:State<'_,AppState>,owner_ref:String,list_revision:u64,selection_ref:String)->Result<Value,String>{
    let mut state=state.attachment_selection.lock().unwrap();state.as_mut().map_err(|error|error.clone())?.remove(&owner_ref,list_revision,&selection_ref)
}
#[tauri::command]
fn reorder_attachments(state:State<'_,AppState>,owner_ref:String,list_revision:u64,selection_refs:Vec<String>)->Result<Value,String>{
    let mut state=state.attachment_selection.lock().unwrap();state.as_mut().map_err(|error|error.clone())?.reorder(&owner_ref,list_revision,&selection_refs)
}
#[tauri::command(async)]
fn reconfirm_attachment(app:tauri::AppHandle,state:State<'_,AppState>,owner_ref:String,list_revision:u64,selection_ref:String)->Result<Value,String>{
    let mut refused=None;
    let result=runtime_session::reconfirm_attachment_source(&state.attachment_selection,&owner_ref,list_revision,&selection_ref,|comparison| {
        confirm_bounded(&app,"Chirality — confirm current attachment source",act_control::native_statement::attachment_source_statement(comparison),
            MessageDialogButtons::OkCancelCustom("Use current source".into(),"Keep original selection".into()),&mut refused)
    });
    act_control::native_statement::refusal_or(refused,result)
}

/// The IPC accepts declared kinds only. Path and bytes originate exclusively
/// at this main-process native selector/once-opened receiver boundary.
#[tauri::command(async)]
fn select_trace_record(
    app: tauri::AppHandle, state: State<'_, AppState>,
    record_kind: String, evidence_kind: String,
) -> Result<Value, String> {
    runtime_session::select_trace_source(&state.trace_selection, &record_kind, &evidence_kind, || {
        app.dialog().file().set_title("Select supplied examination or XT record")
            .add_filter("JSON records", &["json"]).blocking_pick_file()
            .map(|file|file.into_path().map_err(|error|format!("Native selected trace file is not a filesystem path: {error}"))).transpose()
    })
}

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

/// Public reattachment queues only memory-owned history needs. Protocol reads
/// run on the background tick, never in this observer/IPC call. The current
/// owning source is distinct from an older or absent window cursor.
#[tauri::command]
fn host_observe(state: State<'_, AppState>, generation: Value, after: u64, source_generation: Option<Value>) -> Value {
    let source = source_generation.as_ref().unwrap_or(&generation);
    runtime_session::observe_home(&state.homes, source, &generation, after)
}

/// Attribution consumes the Host's current atomic observation rather than the
/// last one-second UI poll. The returned context is frozen for confirmation.
fn current_actor_context(state: &AppState) -> (Value, Value) {
    let home = state.homes.lock().unwrap().active();
    current_actor_context_for(state, &home)
}
fn current_actor_context_for(state: &AppState, home: &runtime_session::HomeSession) -> (Value, Value) {
    let name = state.person_name.lock().unwrap().clone();
    let os = util::os_account();
    let mut runtime = home.runtime.lock().unwrap();
    let (observation, _) = runtime.receive_native(&home.host);
    let context = runtime.actor_context(&observation, name.as_deref(), os.as_deref());
    (observation["snapshot"].clone(), context)
}

/// No actor, origin, rule name or error path is exposed to the webview.
#[tauri::command(async)]
fn answer_native_request(
    window: tauri::Window,
    state: State<'_, AppState>,
    generation: Value,
    request_id: Value,
    answer: Value,
) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    native_request_answer::answer(
        &generation,
        &request_id,
        &answer,
        || current_actor_context_for(&state, &home),
        |statement| native_request_answer::confirm(&window, statement),
        |actor| home.host.answer_server_request(
            &generation,
            &request_id,
            &answer,
            "person-via-interaction",
            Some(actor),
        ),
    )
}

/// J6: a native confirmation shows a bounded, readable statement, with any
/// content it names by digest shown whole in the App while it is open. When no
/// statement can be presented, the alert says why, nothing is chosen, and the
/// cause is kept in `refused` so the command reports a refusal, never the
/// person's cancel (V14 F4).
fn confirm_bounded(app:&tauri::AppHandle,title:&str,statement:Result<act_control::native_statement::NativeStatement,String>,buttons:MessageDialogButtons,refused:&mut Option<String>)->bool{
    match statement {
        Ok(s)=>act_control::native_statement::showing_in_app(s.in_app.as_ref(),||app.dialog().message(s.text.clone()).title(title).kind(MessageDialogKind::Info).buttons(buttons).blocking_show()),
        Err(cause)=>{app.dialog().message(cause.clone()).title(title).kind(MessageDialogKind::Info).buttons(MessageDialogButtons::Ok).blocking_show();*refused=Some(cause);false}
    }
}
/// `confirm_bounded` with the owner's default-safe layout (`act_buttons`):
/// only the explicit `act` button proceeds; Return, Escape and Cancel do not.
fn confirm_choice(app:&tauri::AppHandle,title:&str,statement:Result<act_control::native_statement::NativeStatement,String>,dont:&str,act:&str,refused:&mut Option<String>)->bool{
    use act_control::native_statement as ns;
    match statement {
        Ok(s)=>ns::showing_in_app(s.in_app.as_ref(),||ns::chose(&app.dialog().message(s.text.clone()).title(title).kind(MessageDialogKind::Info).buttons(ns::act_buttons(dont,act)).blocking_show_with_result(),act)),
        Err(cause)=>confirm_bounded(app,title,Err(cause),MessageDialogButtons::Ok,refused),
    }
}
/// Content an open native confirmation names by digest (read-only).
#[tauri::command]
fn native_confirmation_content()->Value{act_control::native_statement::shown_in_app()}
/// The host's digest of a review's complete presentation, as the A15
/// statement names it. A reading aid: the binding is checked host-side.
#[tauri::command(async)]
fn workflow_review_digest(state:State<'_,AppState>,review_ref:String)->Result<Value,String>{
    let review=state.workflows.lock().unwrap().reviews.get(&review_ref).cloned().ok_or("Review unavailable")?;
    let review=review.try_lock().map_err(|_|"Review held by an open native confirmation; its content is shown under the confirmation")?;
    let presentation=review.status.get("presentation").ok_or("Review presentation not available in this state")?;
    Ok(match act_control::review_digest(presentation){Ok(d)=>json!({"reviewRef":review_ref,"digest":d}),Err(cause)=>json!({"reviewRef":review_ref,"unavailable":cause})})
}
fn workflow_native_folder(app:&tauri::AppHandle,title:&str)->Result<Option<PathBuf>,String>{
    app.dialog().file().set_title(title).blocking_pick_folder().map(|path|path.into_path().map_err(|_|"Native folder has no local filesystem path".to_string())).transpose()
}
#[tauri::command(async)]
fn workflow_select_development(app:tauri::AppHandle,state:State<'_,AppState>,context:workflow_selection::Context)->Result<Value,String>{
    workflow_context_home(&state,&context)?;
    let Some(path)=workflow_native_folder(&app,"Select exact coordinated-knowledge-work development holding copy")? else{return Ok(json!({"state":"native selection dismissed"}));};
    noted_selection(&state,&context,|root,chat|root.select_development_copy(chat,path))
}
/// The displayed App source is an opaque HomeSession reference, usable even
/// before Codex starts. A changed active source refuses rather than redirecting.
fn workflow_context_home(state: &AppState, context: &workflow_selection::Context) -> Result<Arc<runtime_session::HomeSession>, String> {
    let home = state.homes.lock().unwrap().active();
    context.verify_home(&home)?;
    Ok(home)
}
/// Recheck at mutation after any native picker/queued operation. The expected
/// choice belongs only to the explicit chat, or to explicit no-chat inspection.
fn noted_selection(state: &AppState, context: &workflow_selection::Context,
    select: impl FnOnce(&mut runtime_session::WorkflowRootSession, Option<&workflow_selection::Chat>) -> Result<Value, String>) -> Result<Value, String> {
    workflow_selection::choose(&state.workflows,context,||state.homes.lock().unwrap().active(),select)
}
fn active_native_view(state:&AppState)->Value {
    let home=state.homes.lock().unwrap().active(); current_native_view(&home)
}
#[tauri::command(async)]
fn workflow_select_production_bundle(app:tauri::AppHandle,state:State<'_,AppState>,name:String,context:workflow_selection::Context)->Result<Value,String>{
    let root=app.path().resource_dir().map_err(|e|format!("App resources unavailable: {e}"))?.join(RESOURCE_WORKFLOWS);
    noted_selection(&state,&context,|workflows,chat|workflows.select_production_bundle(chat,root,&name))
}
#[tauri::command]
fn workflow_select_production_copy(state:State<'_,AppState>,name:String,context:workflow_selection::Context)->Result<Value,String>{
    noted_selection(&state,&context,|root,chat|{root.verify_library_context(&context)?;root.select_production_copy(chat,&name)})
}
#[tauri::command(async)]
fn workflow_open_library(app:tauri::AppHandle,state:State<'_,AppState>,origin:String,context:workflow_selection::Context)->Result<Value,String>{
    if !matches!(origin.as_str(),"project"|"user"){return Err("Choose project or user library; no default".into());}
    workflow_context_home(&state,&context)?;
    let Some(path)=workflow_native_folder(&app,"Open existing physical workflow library root")? else{return Ok(json!({"state":"native library selection dismissed"}));};
    let home=workflow_context_home(&state,&context)?;let view=host_tick::receive_view(&home);
    let mut root=state.workflows.lock().unwrap();workflow_context_home(&state,&context)?;root.verify_library_context(&context)?;
    root.open_library(path,&origin,state.workspace.as_deref(),state.act.clone())?;
    // WR SQ-D D-2: the opened library's drafts are listed at once.
    Ok(root.observe_drafts(&view["items"]).unwrap_or_else(|_|root.snapshot()))
}
/// "Select revision ‹n›" on a retained review: resolved from the revision
/// store (WR SL-4); no folder picker.
#[tauri::command(async)]
fn workflow_select_registered(state:State<'_,AppState>,review_ref:String,revision:String,context:workflow_selection::Context)->Result<Value,String>{
    noted_selection(&state,&context,|root,chat|root.select_hot_registered_copy(chat.ok_or("Choose the chat that will keep this selection")?,&review_ref,&revision))
}
/// WR LS-1 "Select (in such a process)", SL-1: the person selects a registered
/// revision from the active library's list; the host resolves it from the
/// revision store. No folder picker: the store is the library's own.
#[tauri::command(async)]
fn workflow_select_listed(state:State<'_,AppState>,library_ref:String,name:String,revision:String,context:workflow_selection::Context)->Result<Value,String>{
    noted_selection(&state,&context,|root,chat|root.select_listed_registered(chat.ok_or("Choose the chat that will keep this selection")?,&library_ref,&name,&revision))
}
/// WR SL-2: the person follows "newer revision ‹n› available"; a new selection
/// event citing the one it replaces.
#[tauri::command(async)]
fn workflow_follow_newer_revision(state:State<'_,AppState>,selection_ref:String,revision:String,context:workflow_selection::Context)->Result<Value,String>{
    noted_selection(&state,&context,|root,chat|root.follow_newer_revision(chat.ok_or("Choose the chat that keeps this selection")?,&selection_ref,&revision))
}
/// WR §3: the explicit App project's own library, without a folder picker.
#[tauri::command(async)]
fn workflow_open_project_library(state:State<'_,AppState>,context:workflow_selection::Context)->Result<Value,String>{
    let home=workflow_context_home(&state,&context)?;let view=host_tick::receive_view(&home);
    let mut root=state.workflows.lock().unwrap();workflow_context_home(&state,&context)?;root.verify_library_context(&context)?;
    root.open_project_library(state.workspace.as_deref(),state.act.clone())?;
    // The library is open either way; a listing that cannot run now says so in the list.
    Ok(root.observe_drafts(&view["items"]).unwrap_or_else(|_|root.snapshot()))
}
/// WR SQ-D D-2…D-4 in the host (OI-008 ruling): observe the active library's drafts now.
#[tauri::command(async)]
fn workflow_observe_drafts(state:State<'_,AppState>,context:workflow_selection::Context)->Result<Value,String>{
    let home=workflow_context_home(&state,&context)?;let view=host_tick::receive_view(&home);
    let mut root=state.workflows.lock().unwrap();workflow_context_home(&state,&context)?;root.verify_library_context(&context)?;
    root.observe_drafts(&view["items"])
}
/// WR ME-1: explicitly refresh the opened library's file entries. No native
/// contact, review, selection, registration or record write is performed.
#[tauri::command]
fn workflow_library_entries_refresh(state:State<'_,AppState>,library_ref:String,context:workflow_selection::Context)->Result<Value,String>{
    runtime_session::WorkflowRootSession::with_library_context(&state.workflows,&context,||state.homes.lock().unwrap().active(),|root,_|root.observe_library_entries(&library_ref))
}
/// WR ME-1/2: choose an ordered subset of one held observation. Names and
/// content are resolved by its original owner, never supplied by the renderer.
#[tauri::command]
fn workflow_review_library_entries(state:State<'_,AppState>,library_ref:String,listing_ref:String,entry_refs:Vec<String>,context:workflow_selection::Context)->Result<Value,String>{
    let home=workflow_context_home(&state,&context)?;state.validate_home_source(&home)?;
    let (_,observed)=current_actor_context_for(&state,&home);
    runtime_session::WorkflowRootSession::with_library_context(&state.workflows,&context,||state.homes.lock().unwrap().active(),|root,home|root.review_library_entries(home,observed,&library_ref,&listing_ref,&entry_refs))
}
/// WR TT-3, TT-3a, TT-3b (SQ-DT DT-1…DT-3, SQ-FT FT-1…FT-3): Try pressed on a
/// listed draft. The host takes the trial snapshot, composes the trial text and
/// keeps the pre-filled message; nothing is sent or recorded. `thread_id` is
/// the conversation selected when Try was pressed (the authoring conversation).
#[tauri::command(async)]
fn workflow_trial_prepare(state:State<'_,AppState>,name:String,kind:String,generation:Option<Value>,thread_id:Option<String>)->Result<Value,String>{
    let home=match &generation{Some(g)=>Some(state.homes.lock().unwrap().for_generation(g)?),None=>None};
    let authoring=generation.as_ref().zip(thread_id.as_deref());
    // NPTD §7.1, read at run time (R19-5) as the delegated composer is prepared.
    let signals=runtime_session::trial_flows::delegation_signals_for(&kind,home.as_deref(),authoring);
    state.workflows.lock().unwrap().prepare_trial_with(&kind,&name,authoring,home.as_deref(),state.workspace.as_deref(),signals.as_ref())
}
/// WR TT-11 Try again: a new trial of the draft's current version.
#[tauri::command(async)]
fn workflow_trial_again(state:State<'_,AppState>,reference:String)->Result<Value,String>{
    let homes=state.homes.lock().unwrap().entries();
    runtime_session::trial_flows::trial_again(&state.workflows,&reference,&homes,state.workspace.as_deref())
}
/// WR §5.5: removing the trial card cancels the trial; nothing is recorded.
#[tauri::command]
fn workflow_trial_cancel(state:State<'_,AppState>,reference:String)->Result<Value,String>{state.workflows.lock().unwrap().cancel_trial(&reference)}
/// WR DT-4 (and a clean trial's retry in its started conversation): the person
/// sends the pre-filled trial message; the trial link is written on Codex's
/// acknowledgment (TT-4).
#[tauri::command(async)]
fn workflow_trial_send(state:State<'_,AppState>,reference:String,generation:Value,thread_id:String,person_text:String)->Result<Value,SendRefusal>{
    let home=state.homes.lock().unwrap().for_generation(&generation).map_err(SendRefusal::kept)?;
    runtime_session::trial_flows::send_trial(&state.workflows,&home,&reference,&generation,&thread_id,&person_text)
}
/// WR FT-3, FT-4: the person sends a clean trial: a new conversation starts
/// with the role and model the person chose (no handoff, no `continuedFrom`),
/// then its first turn carries the trial text first and the person's text.
#[tauri::command(async)]
fn workflow_trial_start_clean(app:tauri::AppHandle,state:State<'_,AppState>,reference:String,model:String,model_provider:String,entry_id:String,mode_home_class:String,role:Option<role_supply::Role>,person_text:String)->Result<Value,SendRefusal>{
    let home=state.homes.lock().unwrap().entry(home_class(&mode_home_class).map_err(SendRefusal::kept)?).map_err(SendRefusal::kept)?;
    runtime_session::trial_flows::start_clean_trial(&state.workflows,&reference,
        ||start_conversation(&app,&state,model,model_provider,entry_id,&mode_home_class,role,None,None),
        |generation,thread|runtime_session::trial_flows::send_trial(&state.workflows,&home,&reference,generation,thread,&person_text))
}
fn trial_home(state:&AppState,reference:&str)->Result<Arc<runtime_session::HomeSession>,String>{
    let entries=state.homes.lock().unwrap().entries();
    runtime_session::trial_flows::trial_home(&state.workflows,&entries,reference)
}
/// WR TT-9: explicit Link as trial ‹n› / unlink controls; operator identity is not observed.
#[tauri::command]
fn workflow_trial_link(state:State<'_,AppState>,reference:String,child_thread:String)->Result<Value,String>{
    let view=trial_home(&state,&reference)?.runtime.lock().unwrap().native_view();
    state.workflows.lock().unwrap().link_trial_child(&reference,&child_thread,true,&view)
}
#[tauri::command]
fn workflow_trial_unlink(state:State<'_,AppState>,reference:String,child_thread:String)->Result<Value,String>{state.workflows.lock().unwrap().link_trial_child(&reference,&child_thread,false,&Value::Null)}
/// WR TT-9: the person opened the trial and asks to read it again.
#[tauri::command(async)]
fn workflow_trial_read(state:State<'_,AppState>,reference:String)->Result<Value,String>{
    let home=trial_home(&state,&reference)?;
    let view=home.runtime.lock().unwrap().native_view();
    runtime_session::trial_flows::read_trial_again(&state.workflows,&home,&reference,&view)
}
/// WR TT-10 Bring trial back to authoring (SQ-BB BB-1…BB-4): pre-filled, unsent.
#[tauri::command(async)]
fn workflow_trial_bring_back(state:State<'_,AppState>,reference:String,generation:Value,thread_id:String,include_native:bool)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;
    let homes=state.homes.lock().unwrap().entries();
    runtime_session::trial_flows::bring_back_with_homes(&state.workflows,&homes,state.workspace.as_deref(),&home,Some(&reference),None,&generation,&thread_id,include_native)
}
/// WR TT-10 Bring a real run back to authoring: pre-filled, unsent.
#[tauri::command(async)]
fn workflow_run_bring_back(state:State<'_,AppState>,run_ref:String,generation:Value,thread_id:String,include_native:bool)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;
    let homes=state.homes.lock().unwrap().entries();
    runtime_session::trial_flows::bring_back_with_homes(&state.workflows,&homes,state.workspace.as_deref(),&home,None,Some(&run_ref),&generation,&thread_id,include_native)
}
#[tauri::command]
fn workflow_bring_back_cancel(state:State<'_,AppState>,id:String)->Result<Value,String>{runtime_session::trial_flows::cancel_bring_back(&state.workflows,&id)}
/// WR SQ-BB BB-5: the person sends the transcript; *brought back* on acknowledgment.
#[tauri::command(async)]
fn workflow_bring_back_send(state:State<'_,AppState>,id:String,generation:Value,thread_id:String,person_text:String)->Result<Value,SendRefusal>{
    let home=state.homes.lock().unwrap().for_generation(&generation).map_err(SendRefusal::kept)?;
    runtime_session::trial_flows::send_bring_back(&state.workflows,&home,&id,&generation,&thread_id,&person_text)
}
/// WR TT-11 Compare: side by side, with the version difference; records nothing.
#[tauri::command(async)]
fn workflow_trial_compare(state:State<'_,AppState>,left:Value,right:Value)->Result<Value,String>{
    let homes=state.homes.lock().unwrap().entries();
    runtime_session::trial_flows::compare_with_homes(&state.workflows,&homes,state.workspace.as_deref(),&left,&right)
}
/// WR RB-1: review a draft chosen from the host's list, bound to the listed content.
#[tauri::command(async)]
fn workflow_review_draft(state:State<'_,AppState>,name:String)->Result<Value,String>{
    let home=state.homes.lock().unwrap().active();state.validate_home_source(&home)?;
    let (_,context)=current_actor_context_for(&state,&home);
    let view=current_native_view(&home);
    let mut root=state.workflows.lock().unwrap();
    root.review_listed_draft(home,context,&name)?;
    // The review is open either way; the list shows it at its next observation.
    Ok(root.observe_drafts(&view["items"]).unwrap_or_else(|_|root.snapshot()))
}
#[tauri::command]
fn workflow_create_draft(state:State<'_,AppState>,name:String,context:workflow_selection::Context)->Result<Value,String>{
    let home=workflow_context_home(&state,&context)?;
    let mut root=state.workflows.lock().unwrap();
    let chat=context.verify_home(&home)?;workflow_context_home(&state,&context)?;
    root.verify_choice_context(&context,chat.as_ref())?;root.verify_library_context(&context)?;
    root.create_selected_draft(chat.as_ref(),&name)
}
/// J8 (WR §4.6 RF-1): Refine a registered revision from the revision store; no selection.
#[tauri::command]
fn workflow_refine_registered(state:State<'_,AppState>,name:String,revision:String)->Result<Value,String>{state.workflows.lock().unwrap().refine_registered(&name,&revision)}
#[tauri::command]
fn workflow_review(state:State<'_,AppState>,names:Vec<String>,in_place:bool)->Result<Value,String>{
    let home=state.homes.lock().unwrap().active();state.validate_home_source(&home)?;
    let (_,context)=current_actor_context_for(&state,&home);
    state.workflows.lock().unwrap().begin_review(home,context,names,in_place)
}
fn workflow_review_observe(state:&AppState,home:&Arc<runtime_session::HomeSession>,library:&Arc<runtime_session::WorkflowLibraryContext>,review_ref:&str,original:&Value)->Result<(Value,Value),String>{
    let active=state.homes.lock().unwrap().active();if !Arc::ptr_eq(&active,home){return Err("Original review home selection changed; nothing captured, review again".into());}
    state.validate_home_source(home)?;storage::check_path(&library.root)?;
    {let root=state.workflows.lock().unwrap();if root.active_library.as_deref()!=Some(library.reference.as_str())||root.active_review.as_deref()!=Some(review_ref){return Err("Original library/review selection changed; no retarget".into());}}
    let (_,observed)=current_actor_context_for(state,home);
    if observed!=*original{return Err("Original observed actor/home context changed since review; review again".into());}
    let mut actor=act_control::person(observed["displayName"].as_str(),observed["osAccount"].as_str());
    if let Some(account)=observed["codexAccount"].as_str(){actor["codexAccount"]=json!(account);}
    let context=json!({"observedHome":observed,"modeHomeClass":home.class().as_str(),"libraryRef":library.reference,"libraryRoot":attachments::native_path_identity(&library.root),"origin":library.origin,"sourceRoot":library.source_root,"reviewRef":review_ref});
    Ok((actor,context))
}
#[tauri::command(async)]
fn workflow_register_native(app:tauri::AppHandle,state:State<'_,AppState>,review_ref:String)->Result<Value,String>{
    let original=state.workflows.lock().unwrap().reviews.get(&review_ref).cloned().ok_or("Actual original owner review unavailable")?;
    let mut original=original.try_lock().map_err(|_|"Original review native interaction already pending")?;
    if original.attempted_native{return Err("Original native attempt retained; continue it or review again, no duplicate capture".into());}
    let home=original.home.clone();let library=original.library.clone();let context=original.home_context.clone();
    workflow_review_observe(&state,&home,&library,&review_ref,&context)?;
    original.attempted_native=true;
    let result={
        let mut control=library.control.lock().unwrap();let control=control.as_mut().ok_or("Actual original library act owner unavailable")?;
        a15_native::confirm_native(&app,control,original.review.as_ref().ok_or("Original review already transferred")?,original.offer.as_ref().ok_or("Original opaque offer unavailable")?,||workflow_review_observe(&state,&home,&library,&review_ref,&context))
    };
    match result {
        Ok(Some(result))=>original.accept_result(result)?,
        Ok(None)=>{if let Some(review)=original.review.as_ref(){review.withdraw();}original.status=json!({"state":"native confirmation dismissed; no capture/registration"});},
        Err(error)=>{original.status=json!({"state":"native review/capture unavailable; original owner state retained","limit":error,"registration":"not completed; no fabricated receipt or retry"});return Ok(original.status.clone());}
    }
    Ok(original.status.clone())
}
#[tauri::command]
fn workflow_continue_registration(state:State<'_,AppState>,review_ref:String)->Result<Value,String>{
    let original=state.workflows.lock().unwrap().reviews.get(&review_ref).cloned().ok_or("Actual original registration owner unavailable")?;
    let mut original=original.try_lock().map_err(|_|"Original owner interaction pending")?;
    if original.transaction.is_some(){original.advance();return Ok(original.status.clone());}
    if !original.attempted_native{return Err("No original native attempt; no capture/receipt reconstruction".into());}
    let library=original.library.clone();
    let result=library.control.lock().unwrap().as_mut().ok_or("Original library act owner unavailable")?.continue_a15(original.offer.as_ref().ok_or("Original opaque offer not retained")?)?;
    original.accept_result(result)?;Ok(original.status.clone())
}
#[tauri::command]
fn workflow_prepare_run(state:State<'_,AppState>,generation:Value,thread_id:String,person_text:String,context:workflow_selection::Context)->Result<Value,String>{
    let home=workflow_context_home(&state,&context)?;state.validate_home_source(&home)?;
    if context.generation!=generation || context.thread_id.as_deref()!=Some(&thread_id) {return Err("The run target differs from the displayed workflow chat; nothing prepared".into());}
    // The exact displayed choice is rechecked under Root before composing.
    let reference=workflow_selection::prepare(&state.workflows,&context,||state.homes.lock().unwrap().active(),person_text,state.workspace.as_deref())?;
    Ok(json!({"reference":reference,"state":"original registered selection prepared; WR records pending; not sent"}))
}
#[tauri::command(async)]
fn workflow_retry_records(state:State<'_,AppState>,run_ref:String)->Result<Value,String>{
    let run=state.workflows.lock().unwrap().runs.get(&run_ref).cloned().ok_or("Actual prepared original run unavailable")?;
    let mut run=run.try_lock().map_err(|_|"Original run operation pending")?;run.retry_records()
}
/// Durable reading of the explicit project's WR records and R3 entries; writes nothing.
#[tauri::command(async)]
fn workflow_read_records(state:State<'_,AppState>)->Result<Value,String>{
    let root=state.workspace.as_ref().ok_or("No explicit App project (CHIRALITY_WORKSPACE); no WR records to read and no fallback")?;
    let project=workflow_workspace::publication::ProjectRecords::open(root)?;
    Ok(records::supply::read_project_supply(&project))
}
#[tauri::command(async)]
fn workflow_send_run(state:State<'_,AppState>,run_ref:String)->Result<Value,String>{
    let run=state.workflows.lock().unwrap().runs.get(&run_ref).cloned().ok_or("Actual prepared original run unavailable")?;
    {let run=run.try_lock().map_err(|_|"Original run operation pending")?;state.validate_home_source(&run.home)?;}
    // RE-7 / CH-1 rechecked at dispatch; a successor start supersedes a pending end notice.
    runtime_session::start_workflow_run(&state.workflows,&run_ref)
}
/// The current native view of a home, received the same way `host_status` does.
/// Callers hold no Root guard: `host_status` takes the receiver before Root.
fn current_native_view(home:&Arc<runtime_session::HomeSession>)->Value{
    let mut runtime=home.runtime.lock().unwrap();
    runtime.receive_native(&home.host).1["nativeView"].clone()
}
/// EXEC AE-7 / A-11: only the person's explicit end ends a run. FN-2: the cause is
/// *completed* only when the person ends it on the agent's finished report, which
/// the host re-reads from the message it observed; the caller cannot assert it.
#[tauri::command]
fn workflow_end_run(state:State<'_,AppState>,run_ref:String,finished_report:Option<Value>)->Result<Value,String>{
    let run=state.workflows.lock().unwrap().runs.get(&run_ref).cloned().ok_or("Actual run unavailable in this process")?;
    let home=run.try_lock().map_err(|_|"Original run operation pending")?.home.clone();
    let view=crate::host_tick::receive_view(&home); // with the server requests and custody events the recorder reads (CE-4, CE-13, CE-14)
    state.workflows.lock().unwrap().end_requested(&run_ref,&view,finished_report.as_ref())
}
/// RN-3/RN-4, PR-4: the person starts the workflow an agent message proposed (or,
/// with a run in force, ends it and starts the proposed one). The proposal is
/// re-read from the observed message; it never selects or starts anything itself.
#[tauri::command(async)]
fn workflow_start_proposed(state:State<'_,AppState>,generation:Value,message:Value,run_ref:Option<String>,person_text:String,proposal_context:runtime_session::ProposalContext)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;state.validate_home_source(&home)?;
    let view=crate::host_tick::receive_view(&home); // as workflow_end_run
    let next=state.workflows.lock().unwrap().start_proposed_disclosed(&view,home,&generation,&message,run_ref.as_deref(),person_text,state.workspace.as_deref(),&proposal_context)?;
    let started=runtime_session::start_workflow_run(&state.workflows,&next);
    Ok(json!({"ended":run_ref,"started":next,"start":match started{Ok(v)=>v,Err(e)=>json!({"state":"proposed workflow run prepared but not started","limit":e})}}))
}
/// CH-1 "End ‹A› and start ‹B›" as one confirmed step: A ends, B is prepared and started.
#[tauri::command(async)]
fn workflow_end_and_start(state:State<'_,AppState>,run_ref:String,generation:Value,thread_id:String,person_text:String,context:workflow_selection::Context)->Result<Value,String>{
    let home=workflow_context_home(&state,&context)?;state.validate_home_source(&home)?;
    let view=crate::host_tick::receive_view(&home); // as workflow_end_run
    if context.generation!=generation || context.thread_id.as_deref()!=Some(&thread_id) {return Err("The successor target differs from the displayed workflow chat; nothing ended".into());}
    let mut root=state.workflows.lock().unwrap();let chat=context.verify_home(&home)?.ok_or("Choose a workflow chat")?;workflow_context_home(&state,&context)?;root.verify_choice_context(&context,Some(&chat))?;
    let next=root.end_and_start_viewed(&view,&run_ref,home,&generation,&thread_id,person_text,state.workspace.as_deref())?;
    drop(root);
    let started=runtime_session::start_workflow_run(&state.workflows,&next);
    Ok(json!({"ended":run_ref,"started":next,"start":match started{Ok(v)=>v,Err(e)=>json!({"state":"successor not started","limit":e})}}))
}
/// V10 G-5: the person sends without the pending end notice (its record cannot be
/// written); the choice is recorded in the run log and never shown as supplied.
#[tauri::command]
fn workflow_skip_notice(state:State<'_,AppState>,run_ref:String)->Result<Value,String>{
    let run=state.workflows.lock().unwrap().runs.get(&run_ref).cloned().ok_or("Actual run unavailable in this process")?;
    let mut run=run.try_lock().map_err(|_|"Original run operation pending")?;run.skip_end_notice()
}
#[tauri::command(async)]
fn workflow_check_notice(state:State<'_,AppState>,run_ref:String)->Result<Value,String>{
    let run=state.workflows.lock().unwrap().runs.get(&run_ref).cloned().ok_or("Actual run unavailable in this process")?;
    let mut run=run.try_lock().map_err(|_|"Original run operation pending")?;state.validate_home_source(&run.home)?;run.check_end_notice_supply()
}
/// Reopen: the explicit project's WR/RS records plus the REC restart facts this process holds.
#[tauri::command(async)]
fn workflow_reopen(state:State<'_,AppState>)->Result<Value,String>{
    let root=state.workspace.as_ref().ok_or("No explicit App project (CHIRALITY_WORKSPACE); nothing to reopen and no fallback")?;
    let home=state.homes.lock().unwrap().active();
    let recovery=home.recovery_startup.lock().unwrap().snapshot();
    let mut events=restart_events(&recovery);
    // The REC custody projection is where the Host derives app_restart_interruption.
    for event in restart_events(&home.host.recovery_custody().snapshot()){if !events.contains(&event){events.push(event);}}
    let homes=state.homes.lock().unwrap().entries();
    state.workflows.lock().unwrap().reopen_for_learning(root,&events,&homes)
}
/// The person's explicit end of a run the record shows open and interrupted after relaunch.
#[tauri::command]
fn workflow_end_recorded(state:State<'_,AppState>,run_id:String,thread_id:Option<String>)->Result<Value,String>{
    let root=state.workspace.as_ref().ok_or("No explicit App project (CHIRALITY_WORKSPACE); nothing recorded and no fallback")?;
    let thread=thread_id.ok_or("The record names no conversation for this run; it cannot be ended from here")?;
    let home=conversation_home(&state,&thread,&run_id);
    // V10 G-7: a reopened run is ended only as the person's plain end (no completed).
    // WR TX-5 / SQ-END: its end notice is composed from the run's recorded identity facts,
    // keyed to the conversation's own home; with no established home, none is sent.
    let mut out=state.workflows.lock().unwrap().end_recorded_run(root,&run_id,&thread,false,home.as_ref().ok().cloned())?;
    if let Err(reason)=home{out["endNotice"]=json!({"state":format!("not composed: {reason}; no end notice is sent for this end (WR TX-5 / SQ-END)")});}
    Ok(out)
}
/// WR TX-5 / SQ-END: the Codex home of a conversation named by the record, from the
/// App's recovery ledger (`run_restart::conversation_home_class`); never a guess.
fn conversation_home(state:&State<'_,AppState>,thread:&str,run:&str)->Result<Arc<runtime_session::HomeSession>,String>{
    let homes=state.homes.lock().unwrap().entries();
    let (mut rows,mut events)=(Vec::new(),Vec::new());
    for home in &homes{rows.extend(home.host.recovery_entries());events.extend(restart_events(&home.host.recovery_custody().snapshot()));}
    let class=run_restart::conversation_home_class(&rows,&events,thread,run)?;
    homes.into_iter().find(|home|stop_records::home_class(home.class().as_str())==Some(class.as_str()))
        .ok_or_else(||format!("Codex home {class} of conversation {thread} is not available in this App process"))
}
/// WR TX-5 / SQ-END: "Retry the end-notice record" or "Send without the end notice" for a
/// run the person ended after a relaunch (`action`: "retry" or "skip").
#[tauri::command]
fn workflow_reopened_notice(state:State<'_,AppState>,run_id:String,action:String)->Result<Value,String>{
    let end=state.workflows.lock().unwrap().reopened_end(&run_id).ok_or("No end made after the relaunch is held for this run in this process")?;
    let mut end=end.try_lock().map_err(|_|"That run's end-notice operation is pending")?;
    match action.as_str(){"retry"=>end.retry_notice_record(),"skip"=>end.skip_end_notice(),_=>Err("unknown end-notice action".into())}
}
/// REC `app_restart_interruption` facts, wherever the recovery projection carries them.
fn restart_events(value:&Value)->Vec<Value>{
    match value{
        Value::Object(map)=>{let mut out:Vec<Value>=map.get("restartEvents").and_then(Value::as_array).cloned().unwrap_or_default();for (k,v) in map{if k!="restartEvents"{out.extend(restart_events(v));}}out}
        Value::Array(items)=>items.iter().flat_map(restart_events).collect(),
        _=>vec![],
    }
}
#[tauri::command(async)]
fn workflow_check_supply(state:State<'_,AppState>,run_ref:String)->Result<Value,String>{
    let run=state.workflows.lock().unwrap().runs.get(&run_ref).cloned().ok_or("Actual prepared original run unavailable")?;
    let mut run=run.try_lock().map_err(|_|"Original source-bound supply check pending")?;state.validate_home_source(&run.home)?;
    match run.check_native_supply(){Ok(v)=>Ok(v),Err(error)=>{run.supply=json!({"state":"native coverage/source unavailable; no supplied claim","limit":error,"adoption":"unknown"});Ok(run.supply.clone())}}
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
    let ws = state.workspace.as_ref().ok_or("CHIRALITY_WORKSPACE is not set")?;
    let mut view = runtime_session::read_decision_packages(ws);
    view["writerStatus"] = state.decision_writer_status.lock().unwrap().clone();
    Ok(view)
}

/// Explicit writer continuation; it is separate from every public read.
#[tauri::command]
fn continue_decision_recording(state: State<'_, AppState>) -> Result<Value, String> {
    let ws = state.workspace.as_ref().ok_or("CHIRALITY_WORKSPACE is not set")?;
    let mut control = state.act.lock().unwrap();
    let status = runtime_session::continue_decision_writer(ws, control.as_mut(), "explicit-command");
    *state.decision_writer_status.lock().unwrap() = status.clone();
    Ok(status)
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
    let statement = ac.confirmation_statement(&offer_id, &alternative, &actor)?;
    ac.present(&offer_id)?;
    // Owner's three-button layout: Return chooses "Don't decide"; an abort maps
    // to "Cancel"; only the middle "Decide" captures.
    use act_control::native_statement::{self as ns, DECIDE, DONT_DECIDE};
    let result = ns::showing_in_app(statement.in_app.as_ref(), || {
        app.dialog()
            .message(statement.text.clone())
            .title("Chirality — decide")
            .kind(MessageDialogKind::Warning)
            .buttons(ns::act_buttons(DONT_DECIDE, DECIDE))
            .blocking_show_with_result()
    });
    if !ns::chose(&result, DECIDE) {
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

// Observer takes no file Root/offer/control lock. Every outer lock is fail-fast,
// so a competing Root-held operation cannot invert native control ownership.
fn file_act_observe(state:&AppState, home:&Arc<runtime_session::HomeSession>) -> Result<(Value,Value),String> {
    let active=state.homes.try_lock().map_err(|_|"Home selection busy; review again")?.active();
    if !Arc::ptr_eq(&active,home){return Err("Original file-act home changed; review again".into());}
    let binding=state.home_bootstrap.try_lock().map_err(|_|"Home binding busy; review again")?;
    match &*binding { Ok(set)=>set.validate_binding(home.class(),home.host_config.as_ref().map_err(Clone::clone)?)?, Err(_) if home.class()==home_resources::HomeClass::Account=>{}, Err(e)=>return Err(e.clone()) }
    drop(binding);
    let name=state.person_name.try_lock().map_err(|_|"Actor setting busy; review again")?.clone();
    let os=util::os_account();
    let mut runtime=home.runtime.try_lock().map_err(|_|"Actor observation busy; review again")?;
    let (observed, _)=runtime.receive_native(&home.host);
    let current=runtime.actor_context(&observed,name.as_deref(),os.as_deref());
    let mut actor=act_control::person(current["displayName"].as_str(),current["osAccount"].as_str());
    if let Some(account)=current["codexAccount"].as_str(){actor["codexAccount"]=json!(account);}
    let workspace=state.workspace.as_ref().ok_or("No App workspace")?;
    storage::check_path(workspace)?;
    let context=json!({"observedHome":current,"modeHomeClass":home.class().as_str(),"workspace":attachments::native_path_identity(workspace)});
    Ok((actor,context))
}
#[tauri::command(async)]
fn file_act_select(app:tauri::AppHandle,state:State<'_,AppState>,kind:String,scope:String,purpose:String)->Result<Value,String>{
    let kind=match kind.as_str(){"A4"=>act_control::FileActKind::Check,"A6"=>act_control::FileActKind::Approve,"A7"=>act_control::FileActKind::Rely,_=>return Err("Choose A4, A6 or A7".into())};
    let home=state.homes.try_lock().map_err(|_|"Home selection busy")?.active();
    let (_,context)=file_act_observe(&state,&home)?;
    let selected=app.dialog().file().set_title("Select one App workspace file or saved output").blocking_pick_file();
    let Some(selected)=selected else{return Ok(json!({"state":"selection dismissed; nothing captured"}));};
    let path=selected.into_path().map_err(|_|"Native selection has no filesystem path")?;
    if file_act_observe(&state,&home)?.1!=context{return Err("Actor or context changed during selection; select again".into());}
    let mut control=state.act.try_lock().map_err(|_|"Act owner busy; select again")?;
    state.file_acts.try_lock().map_err(|_|"File offer state busy; select again")?.compose(control.as_mut().ok_or("No App workspace")?,&path,kind,&scope,&purpose,home,context)
}
#[tauri::command(async)]
fn file_act_confirm(app:tauri::AppHandle,state:State<'_,AppState>,reference:String)->Result<Value,String>{
    file_act_confirm_original(&state,&reference,|control,offer,observe|act_control::confirm_file_native(&app,control,offer,observe))
}
fn file_act_open_arrival_result(state:&AppState,run_ref:&str,arrival_record_id:&str)->Result<Value,String>{
    let root=state.workspace.as_ref().ok_or("No App workspace")?;
    let run=state.workflows.try_lock().map_err(|_|"Workflow owner busy; review again")?.runs.get(run_ref).cloned().ok_or("Original live run unavailable; cold records do not create live arrival custody")?;
    let source=runtime_session::ArrivalSource::open(run,root,run_ref,arrival_record_id)?;
    let (_,context)=file_act_observe(state,&source.home())?;
    let mut control=state.act.try_lock().map_err(|_|"Act owner busy; review again")?;
    state.file_acts.try_lock().map_err(|_|"File offer state busy; review again")?.compose_arrival(control.as_mut().ok_or("No App workspace")?,source,context)
}
#[tauri::command(async)]
fn file_act_open_arrival(state:State<'_,AppState>,run_ref:String,arrival_record_id:String)->Result<Value,String>{file_act_open_arrival_result(&state,&run_ref,&arrival_record_id)}
fn file_act_confirm_original(state:&AppState,reference:&str,
    confirm:impl FnOnce(&mut ActControl,&act_control::FileActOfferRef,&mut dyn FnMut()->Result<(Value,Value),String>)->Result<Option<Value>,String>
)->Result<Value,String>{
    let owner=state.file_acts.try_lock().map_err(|_|"File offer state busy")?.get(&reference)?;
    let mut owner=owner.try_lock().map_err(|_|"Original file operation pending")?;
    if owner.attempted{return Err("Original attempt retained; continue its recording or review a new offer".into());}
    let home=owner.home.clone();let original=owner.context.clone();let arrival=owner.arrival.clone();
    let mut control=state.act.try_lock().map_err(|_|"Act owner busy; no native attempt")?;
    let control=control.as_mut().ok_or("Original act owner absent")?;
    owner.attempted=true;
    let result=confirm(control,&owner.offer,&mut ||{
        let observed=file_act_observe(&state,&home)?;
        if let Some(source)=&arrival{source.validate()?;}
        if observed.1!=original{return Err("Actor or owning context changed since preview; review again".into());}
        Ok(observed)
    });
    owner.status=match result{Ok(Some(value))=>value,Ok(None)=>json!({"state":"dismissed; nothing captured","recorded":false}),Err(error)=>json!({"state":"native attempt returned an error; capture/record standing not established by this result","error":error})};
    Ok(owner.status.clone())
}
#[tauri::command(async)]
fn file_act_continue(state:State<'_,AppState>,reference:String)->Result<Value,String>{
    file_act_continue_result(&state,&reference)
}
fn file_act_continue_result(state:&AppState,reference:&str)->Result<Value,String>{
    let owner=state.file_acts.try_lock().map_err(|_|"File offer state busy")?.get(&reference)?;
    let mut owner=owner.try_lock().map_err(|_|"Original file operation pending")?;
    let mut control=state.act.try_lock().map_err(|_|"Act owner busy; original status retained")?;
    // Recording the original capture must not replace its historical actor with today's.
    let result=control.as_mut().ok_or("Original act owner absent")?.continue_file_act(&owner.offer)?;
    owner.status=result.clone();Ok(result)
}
#[tauri::command]
fn file_act_dismiss(state:State<'_,AppState>,reference:String)->Result<Value,String>{
    let owner=state.file_acts.try_lock().map_err(|_|"File offer state busy")?.get(&reference)?;
    let mut owner=owner.try_lock().map_err(|_|"Original file operation pending")?;
    if owner.attempted{return Err("Original native attempt retained; dismissal cannot erase it".into());}
    state.act.try_lock().map_err(|_|"Act owner busy")?.as_mut().ok_or("Original act owner absent")?.dismiss_file_act(&owner.offer);
    owner.attempted=true;owner.status=json!({"state":"dismissed; nothing captured","recorded":false});Ok(owner.status.clone())
}
#[tauri::command(async)]
fn file_act_read(state:State<'_,AppState>)->Result<Value,String>{
    let root=state.workspace.as_ref().ok_or("No App workspace")?;
    let mut view=file_act_view::read(root);
    view["hotOffers"]=state.file_acts.try_lock().map_err(|_|"File offer state busy")?.snapshot();
    view["lapseObservation"]=state.file_act_lapses.try_lock().map_err(|_|"File lapse observer busy")?.snapshot();
    Ok(view)
}
fn file_act_lapse_result(state:&AppState,retry:bool)->Result<Value,String>{
    let root=state.workspace.as_ref().ok_or("No App workspace")?;
    let observation={let mut owner=state.file_act_lapses.try_lock().map_err(|_|"File lapse observer busy")?;
        if retry{owner.retry(root)}else{owner.observe(root)}};
    let mut view=file_act_view::read(root);
    view["hotOffers"]=state.file_acts.try_lock().map_err(|_|"File offer state busy")?.snapshot();
    view["lapseObservation"]=observation;
    Ok(view)
}
#[tauri::command(async)]
fn file_act_observe_lapses(state:State<'_,AppState>)->Result<Value,String>{file_act_lapse_result(&state,false)}
#[tauri::command(async)]
fn file_act_retry_lapses(state:State<'_,AppState>)->Result<Value,String>{file_act_lapse_result(&state,true)}

fn explicit_environment_launch(
    input: impl Fn(&str)->Option<std::ffi::OsString>, data: &Result<PathBuf,String>, resources: &Result<PathBuf,String>, is_dev: bool,
    probe: impl FnOnce()->Result<PathBuf,String>,
) -> Option<desktop_startup::Launch> {
    const KEYS: &[&str] = &["CHIRALITY_CODEX_BIN", "CHIRALITY_CODEX_HOME", "CHIRALITY_WORKSPACE", "CHIRALITY_KEY_HOME", "CHIRALITY_SHARED_CONFIG", "CHIRALITY_SHARED_AGENTS", "CHIRALITY_SHARED_SKILLS", "CHIRALITY_CODEX_EXPECTED_SHA256", "CHIRALITY_ALLOW_UNVERIFIED", "CHIRALITY_DISTRIBUTION_SUCCESSOR"];
    if !KEYS.iter().any(|key|input(key).is_some()) { return None; }
    let workspace = input("CHIRALITY_WORKSPACE").map(PathBuf::from);
    let host_config = if is_dev || !cfg!(feature = "distribution-successor") {
        host_config_from_inputs(workspace.as_ref(), &input, probe).and_then(|mut cfg| {
            if is_dev && input("CHIRALITY_DISTRIBUTION_SUCCESSOR").is_some_and(|v|v == "1") {
                cfg.distribution = Some(hosting::successor::Distribution::development_from_binary(&cfg.codex_bin)?);
            }
            Ok(cfg)
        })
    } else {
        (|| {
            let resources = resources.as_ref().map_err(Clone::clone)?.clone();
            let data = data.as_ref().map_err(Clone::clone)?.clone();
            let home = input("CHIRALITY_CODEX_HOME").map(PathBuf::from).ok_or("No explicit App-owned account home")?;
            Ok(hosting::successor::production_config(resources, home, probe()?, workspace.clone().unwrap_or(data)))
        })()
    };
    let host_config = host_config.map(|mut cfg| { cfg.require_distribution_artifacts = cfg.distribution.is_some(); cfg });
    let key = input("CHIRALITY_KEY_HOME").map(PathBuf::from);
    let shared = ["CHIRALITY_SHARED_CONFIG", "CHIRALITY_SHARED_AGENTS", "CHIRALITY_SHARED_SKILLS"].map(|key|input(key).map(PathBuf::from));
    Some(desktop_startup::Launch::environment(workspace, host_config, key, shared))
}

fn freeze_startup_state(launch: desktop_startup::Launch, desktop: Arc<Mutex<desktop_startup::DesktopSetup>>, compiled_selection: Value) -> (AppState, Arc<runtime_session::HomeSession>) {
    let desktop_startup::Launch { workspace, host_config, key_path, shared_paths, bootstrap, namespaces, source } = launch;
    let source = if source == "explicit environment (exclusive)" { "explicit Root native environment path inputs" } else { source };
    let project = runtime_session::freeze_configured_project(workspace.as_deref());
    let project_context_limit = project.as_ref().err().cloned();
    let project_context = project.unwrap_or_else(|_|recovery::ExplicitAppProjectContext::unknown());
    let home = Arc::new(runtime_session::HomeSession::new(home_resources::HomeClass::Account,Arc::new(Host::new()),host_config.clone()).expect("account entry"));
    let state = AppState {
        desktop_setup: Some(desktop),
        endpoint_edits:Arc::new(Mutex::new(Default::default())),
        compiled_development_selection: compiled_selection,
        connector_sources: Mutex::new(connector_source::Session::default()),
        connector_drafts: Mutex::new(connector_materialization::Registry::default()),
        act: Arc::new(Mutex::new(workspace.as_ref().map(|w| ActControl::new(w)))),
        workflows: Mutex::new(runtime_session::WorkflowRootSession::default()),
        file_acts: Mutex::new(file_act_root::FileActRoot::default()),
        file_act_lapses: Mutex::new(file_act_lapse::Observer::default()),
        decision_writer_status: Mutex::new(json!({"state":"not-run","responsibility":"decision record writer continuation"})),
        workspace: workspace.clone(),
        person_name: Mutex::new(None),
        instructions_root: Mutex::new(Err("App instruction root not initialized".into())),
        app_user_data_root: Mutex::new(Err("App user-data root not initialized".into())),
        external_observation: Mutex::new(runtime_session::ExternalObservationSession::default()),
        trace_selection: Mutex::new(runtime_session::TraceSelectionSession::default()),
        attachment_selection: Mutex::new(runtime_session::AttachmentSelectionSession::new(workspace.clone())),
        role_log: workspace.as_deref().ok_or_else(||"explicit App project unavailable for role observations".to_string()).and_then(role_observations::RoleLog::open).map(Arc::new),
        native_links: Mutex::new(native_conversation_links::Session::default()),
        project_context, project_context_limit,
        homes: Mutex::new(runtime_session::HomeRouter::new(home.clone()).expect("explicit primary account class")),
        home_bootstrap: Mutex::new(bootstrap.ok_or_else(||"Explicit Root home descriptors not initialized".into())),
        native_namespaces: Mutex::new(namespaces.unwrap_or_else(||Err("Root native namespace bindings not initialized".into()))),
        key_namespace_admission: Mutex::new(json!({"state":"prospective key not admitted"})),
        key_setup: Mutex::new(()),
        root_home_inputs: json!({"source":source,"keyHome":key_path.as_ref().map(|path|attachments::native_path_identity(path)),"sharedConfig":shared_paths[0].as_ref().map(|path|attachments::native_path_identity(path)),"sharedGlobalAgents":shared_paths[1].as_ref().map(|path|attachments::native_path_identity(path)),"sharedSkills":shared_paths[2].as_ref().map(|path|attachments::native_path_identity(path)),"limit":"supplied references are not observed linked state, ownership or native discovery proof"}),
        codex_stop_gate: Mutex::new(()),
        codex_stops: Mutex::new(Vec::new()),
        continue_as: Mutex::new(conversation_roles::Handoffs::default()),
        app_quit: app_quit::AppQuit::default(),
    };
    (state, home)
}

/// One actual consumer join for admitted launch inputs. Desktop refusal gives
/// every operational consumer an unavailable data root, including records
/// overrides; the setup controller retains its separate local save capability.
fn initialize_startup_consumers(state: &AppState, home: &Arc<runtime_session::HomeSession>, data: Result<PathBuf,String>, allow_operational: bool, is_dev: bool, records_override: Option<PathBuf>, key_path: Option<PathBuf>, shared_paths: [Option<PathBuf>; 3]) {
    let workspace = state.workspace.clone();
    let host_config = home.host_config.clone();
    let host = &home.host;
    // RS §13.8: the App's records store, configured once before any
    // record is read or written; a store that cannot be used refuses
    // recording visibly, with no fallback. Opening the project gives it
    // its identity once (`.chirality/project.json`).
    {
        let codex_homes = codex_homes(home.host_config.as_ref().ok().into_iter());

        records_store::configure(if allow_operational { records_store::for_app(records_override, data.as_deref().map_err(Clone::clone), is_dev, workspace.as_deref(), &codex_homes) } else { Err(data.as_ref().err().cloned().unwrap_or_else(||"Desktop Root consumers not admitted".into())) });
        if let Some(ws) = workspace.as_ref() {
            if let Err(e) = records_store::attach(ws, true) { eprintln!("chirality: the project was not given its records identity at startup: {e}"); }
        }
    }
    // AAC §6.3 SEAL-C: this installation's capture-seal keys live in the
    // App data folder, outside every project.
    if let Ok(data) = data.as_ref() { capture_seal::install(data); installation::install(data); }
    home.history.lock().unwrap().configure_role_log_source(state.role_log.clone());
    if state.home_bootstrap.lock().unwrap().is_err() { *state.home_bootstrap.lock().unwrap() = (|| {
        let data=data.as_ref().map_err(Clone::clone)?;
        let cfg=home.host_config.as_ref().map_err(Clone::clone)?;
        runtime_session::freeze_root_home_descriptors(data,cfg,key_path.clone(),shared_paths.clone()).map(Arc::new)
    })(); }
    // Startup owns this separate writer continuation. Neither decision
    // view reads nor host/status polling invokes the writer.
    if let Some(ws) = state.workspace.as_ref() {
        let mut control = state.act.lock().unwrap();
        *state.decision_writer_status.lock().unwrap() = runtime_session::continue_decision_writer(ws, control.as_mut(), "app-startup-writer");
    }
    *state.app_user_data_root.lock().unwrap() = data.clone();
    // RS §13.9 (owner U-STORE-4): the agents' read-only records
    // capability in the current project. Each read is recorded in the
    // project's records store folder; the App-wide read log an earlier
    // build kept in App data stays there unchanged and is shown.
    if let Some(ws) = state.workspace.as_ref() {
        let capability = records_access::RecordsCapability::new(ws).map(|capability| match data.as_ref() {
            Ok(data) => capability.with_legacy_read_log(&data.join("runtime").join("records-reads.jsonl")),
            Err(_) => capability,
        });
        match capability {
            Ok(capability) => home.host.configure_records_capability_with_context(Arc::new(capability), state.project_context.clone()),
            Err(reason) => home.host.records_capability_unavailable(reason),
        }
    }
    // WR §3: App-kept draft bases live in the App data folder.
    if let Ok(data) = data.as_ref() { state.workflows.lock().unwrap().set_app_user_data(data.clone()); }
    // Current account/probe protection is independent of a bad new key
    // candidate; do not create/adopt K or replace an existing L binding.
    let namespaces=if state.native_namespaces.lock().unwrap().is_ok() { state.native_namespaces.lock().unwrap().clone() } else { (|| {
        let data=data.as_ref().map_err(Clone::clone)?;
        let cfg=home.host_config.as_ref().map_err(Clone::clone)?;
        runtime_session::freeze_root_home_descriptors(data,cfg,None,shared_paths.clone())?.native_namespaces(false)
    })() };
    *state.native_namespaces.lock().unwrap()=namespaces.clone();
    let namespace_authority=namespaces.clone().map(hosting::attachment_custody::NamespaceAuthority::new);
    if let Ok(cfg) = &home.host_config {
        if cfg.distribution.is_some() {
            let store = (|| {
                let data = data.as_ref().map_err(Clone::clone)?;
                let vendor = cfg.distribution.as_ref().unwrap().vendor_root();
                let store=match cfg.distribution.as_ref().unwrap() {
                    hosting::successor::Distribution::Production { resources } => {
                        let selected=distribution_preflight::selection::Selected::production(&resources.join("distribution-reference"))?;
                        crate::distribution_store::Store::open_selected(data,&vendor,namespaces.clone()?,selected)
                    },
                    // A supplied development tree is compared with the same compiled
                    // selection; an unresolvable closure is reported, never trusted.
                    hosting::successor::Distribution::Development { .. } => hosting::successor::development_reference_root()
                        .and_then(|root|distribution_preflight::selection::Selected::production(&root))
                        .and_then(|selected|crate::distribution_store::Store::open_selected(data,&vendor,namespaces.clone()?,selected)),
                }?;
                crate::distribution_store::Store::with_authority(store,namespace_authority.clone()?)
            })();
            host.configure_distribution_store(store);
        }
    }
    *home.attachment_custody.lock().unwrap()=data.as_ref().map_err(Clone::clone).and_then(|data|hosting::attachment_custody::AttachmentCustody::open_shared(data,namespace_authority.clone()?).map(Arc::new));
    home.recovery_startup.lock().unwrap().initialize_with_namespaces(
        &host,
        data.as_deref().map_err(String::as_str),
        host_config
            .as_ref()
            .ok()
            .map(|cfg| cfg.codex_home.as_path()),
        namespaces,
    );
    let root = data.clone().and_then(|data| {
        let root = data.join("instructions");
        runtime_session::seed_instructions(&root)?;
        Ok(root)
    });
    *state.instructions_root.lock().unwrap() = root;
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .menu(app_menu)
        .on_menu_event(|app, event| {
            if event.id() == QUIT_MENU_ID { request_quit(app.clone()); }
            else if event.id().as_ref().starts_with(native_waiting::ITEM_PREFIX) { request_native_waiting(app, event.id().as_ref()); }
        })
        // DEF-1, SQ-W: closing the window is not quit and stops nothing. The
        // window is hidden (macOS; the Dock click shows it again) or minimized
        // (platforms with no Dock), so the main process keeps observing and
        // the web view re-reads the host's snapshot when it is shown.
        .on_window_event(|window, event| if let tauri::WindowEvent::CloseRequested { api, .. } = event {
            api.prevent_close();
            #[cfg(target_os = "macos")]
            let _ = window.hide();
            #[cfg(not(target_os = "macos"))]
            let _ = window.minimize();
        })
        .setup(move |app| {
    let data = app.path().app_data_dir().map_err(|e| e.to_string());
    let resources = app.path().resource_dir().map_err(|e|e.to_string());
    let environment = explicit_environment_launch(|key|std::env::var_os(key), &data, &resources, tauri::is_dev(), probe_home);
    let mut desktop = desktop_startup::DesktopSetup::new(data.clone(), resources.clone());
    let launch = desktop.resolve(environment, tauri::is_dev(), probe_home);
    let desktop_startup::RootInputs { launch, data, allow_operational } = desktop.admit_root(launch, data);
    let host_config = launch.host_config.clone();
    let key_path = launch.key_path.clone();
    let shared_paths = launch.shared_paths.clone();
    let desktop = Arc::new(Mutex::new(desktop));
    let (state, home) = freeze_startup_state(launch, desktop.clone(), compiled_development_selection::observe_startup(|| resources.clone()));
    let host = Arc::clone(&home.host);
            app.manage(state);
            app.manage(Mutex::new(native_waiting::Registry::default()));
            initialize_startup_consumers(&app.state::<AppState>(), &home, data.clone(), allow_operational, tauri::is_dev(), std::env::var_os(records_store::OVERRIDE_ENV).filter(|p|!p.is_empty()).map(PathBuf::from), key_path, shared_paths);
            // OI-008: the host keeps its own records on its own tick, whether or
            // not the web view polls host_status.
            {
                let handle = app.handle().clone();
                std::thread::Builder::new().name("chirality-host-tick".into()).spawn(move || loop {
                    std::thread::sleep(host_tick::INTERVAL);
                    let state = handle.state::<AppState>();
                    host_tick::guarded("record", || host_tick::tick_project(&state.homes, &state.workflows, state.workspace.as_deref()));
                    // Native relationship publication runs independently of web reads.
                    host_tick::guarded("native-links", || {state.native_links.lock().unwrap().retry(state.workspace.as_deref());});
                }).map_err(|e| format!("host tick thread not started: {e}"))?;
                // TT-9 reads wait on Codex; their own thread never delays the record tick.
                let handle = app.handle().clone();
                std::thread::Builder::new().name("chirality-trial-tick".into()).spawn(move || loop {
                    std::thread::sleep(host_tick::INTERVAL);
                    let state = handle.state::<AppState>();
                    host_tick::guarded("trial", || host_tick::trial_tick(&state.homes, &state.workflows));
                }).map_err(|e| format!("trial tick thread not started: {e}"))?;
                // C-24: the waiting-request indicator, kept by the host.
                let handle = app.handle().clone();
                std::thread::Builder::new().name("chirality-waiting-indicator".into()).spawn(move || {
                    let mut last = None;
                    let mut menu = native_waiting::MenuObserver::default();
                    loop {
                        std::thread::sleep(host_tick::INTERVAL);
                        host_tick::guarded("indicator", || show_waiting_indicator(&handle, &mut last, &mut menu));
                    }
                }).map_err(|e| format!("waiting indicator thread not started: {e}"))?;
            }
            // EXEC §2.7 / RECOVERY §4.1, OI-008: the host writes RS "App-restart interruption" limits
            // from this session's REC restart facts, at startup, never on a web-view
            // request. Its outcome is shown by workflow_reopen.
            {
                let handle = app.handle().clone();
                std::thread::Builder::new().name("chirality-restart-limits".into()).spawn(move || {
                    let state = handle.state::<AppState>();
                    let homes = state.homes.lock().unwrap().entries();
                    // Held across the writer: the person's End of a recorded run
                    // (end_recorded_run) takes the same lock, so a limit is never
                    // written on a run the person has just ended.
                    let mut workflows = state.workflows.lock().unwrap();
                    let outcome = run_restart::startup(&homes, state.workspace.as_deref());
                    workflows.set_restart_limits(outcome);
                }).map_err(|e| format!("restart-limit thread not started: {e}"))?;
            }
            // App start-up starts the supplier (HOSTING §4.6 start, actor `app-startup`).
            if let Ok(cfg) = host_config {
                let h = Arc::clone(&host);
                let recovery = Arc::clone(&home.recovery_startup);
                std::thread::spawn(move || {
                    let _ = runtime_session::start_with_recovery(
                        &h,
                        &recovery,
                        data.as_deref().map_err(String::as_str),
                        Some(&cfg.codex_home),
                        || { desktop.lock().map_err(|_|"Desktop custody unavailable")?.recheck_active()?; h.start(&cfg, "app-startup") },
                    );
                });
            }
            Ok(())
        })
        // DEF-1: closing or reloading a window is not a stop (HOSTING §4.5); no window
        // event touches the child.
        .invoke_handler(tauri::generate_handler![
            desktop_setup_pick, desktop_setup_preview, desktop_setup_project_preview, desktop_setup_prepare,
            file_act_select, file_act_open_arrival, file_act_confirm, file_act_continue, file_act_dismiss, file_act_read, file_act_observe_lapses, file_act_retry_lapses,
            read_recovery_custody,
            read_recovery_request_history,
            recovery_retry,
            read_connector_routes,
            read_fleet_records,
            records_store_import, records_store_identity, records_store_choose, records_chain_heads, records_store_export, records_store_verify_export, records_store_import_package, records_store_retention,
            prepare_connector_source, select_connector_source, anchor_connector_source, revise_connector_source,
            read_connector_git, cancel_connector_git, anchor_connector_git,
            recheck_published_connector_draft, prepare_connector_reconstruction, prepare_connector_draft, publish_connector_draft, cancel_connector_draft, reconcile_connector_draft, inspect_connector_drafts,
            host_status,
            select_home,
            open_waiting_requests,
            claim_native_waiting_intent,
            checkpoint_native_waiting_ui,
            finish_native_waiting_intent,
            read_home_access, read_configured_providers, provider_endpoint_offer, provider_endpoint_save, provider_endpoint_discard, provider_create_offer, provider_create_save, provider_create_discard,
            add_api_key,
            oauth_start,oauth_present,oauth_cancel,
            logout_home,
            host_observe,
            select_external_observation,
            select_trace_record,
            select_attachment,
            submit_attachments,
            remove_attachment,
            reorder_attachments,
            reconfirm_attachment,
            answer_native_request,
            host_start,
            codex_stop,
            thread_start,
            role_supply_history,
            history_action,
            continuation_context_action,
            history_select,
            conversation_send_text,
            collaboration_modes_read,
            conversation_steer_text,
            conversation_interrupt,
            continue_as_begin,
            continue_as_dismiss,
            continue_as_send,
            continue_as_send_read,
            conversation_fork,
            set_person_name,
            workflow_select_development,workflow_select_production_bundle,workflow_select_production_copy,workflow_open_library,workflow_open_project_library,workflow_observe_drafts,workflow_library_entries_refresh,workflow_review_library_entries,workflow_trial_prepare,workflow_trial_again,workflow_trial_cancel,workflow_trial_send,workflow_trial_start_clean,workflow_trial_link,workflow_trial_unlink,workflow_trial_read,workflow_trial_bring_back,workflow_run_bring_back,workflow_bring_back_cancel,workflow_bring_back_send,workflow_trial_compare,workflow_review_draft,workflow_select_registered,workflow_select_listed,workflow_follow_newer_revision,workflow_create_draft,workflow_refine_registered,workflow_review,workflow_register_native,workflow_continue_registration,workflow_prepare_run,workflow_send_run,workflow_check_supply,workflow_retry_records,workflow_read_records,workflow_end_run,workflow_start_proposed,workflow_end_and_start,workflow_check_notice,workflow_skip_notice,workflow_reopen,workflow_end_recorded,workflow_reopened_notice,workflow_review_digest,native_confirmation_content,
            decision_view,
            continue_decision_recording,
            compose_offer,
            decide
        ])
        .build(tauri::generate_context!())
        .expect("error while building the Tauri application")
        .run(|app, event| match event {
            // K-4: an exit nobody decided is held; the last window going away
            // is DEF-1, not quit; a decided quit (AS-03 or confirmed) exits.
            tauri::RunEvent::ExitRequested { code, api, .. } => {
                let st: State<'_, AppState> = app.state();
                match app_quit::on_exit_requested(st.app_quit.proceeding().is_some(), code) {
                    app_quit::ExitAction::Allow => {}
                    app_quit::ExitAction::Keep => api.prevent_exit(),
                    app_quit::ExitAction::AskQuit => { api.prevent_exit(); request_quit(app.clone()); }
                }
            }
            // SQ-W W-4: the Dock click shows the window again; the web view
            // re-reads the host's snapshot.
            #[cfg(target_os = "macos")]
            tauri::RunEvent::Reopen { .. } => show_main_window(app),
            // Q-6, Q-7 (AS-08, AS-09) after a decided quit; AS-10 when the
            // system ends the App without the question (macOS `terminate:`
            // from the Dock's Quit, logout or shutdown).
            tauri::RunEvent::Exit => {
                let st: State<'_, AppState> = app.state();
                let homes = st.homes.lock().unwrap().entries();
                let _ = app_quit::finish_exit(&homes, st.app_quit.proceeding());
                records_index::close_all();
            }
            _ => {}
        });
}

#[cfg(all(test,unix))]
mod workflow_root_context_tests {
    use super::*;
    pub(super) fn fixture()->(PathBuf,AppState,Arc<runtime_session::HomeSession>,Arc<runtime_session::WorkflowLibraryContext>,String,Value){
        let root=std::fs::canonicalize(std::env::temp_dir()).unwrap().join(util::opaque_id("workflow-context-").unwrap());std::fs::create_dir(&root).unwrap();
        let home=Arc::new(runtime_session::HomeSession::new(home_resources::HomeClass::Account,Arc::new(Host::new()),Err("no supplier; offline registration allowed".into())).unwrap());
        let control=Arc::new(Mutex::new(Some(ActControl::new(&root))));
        let mut workflows=runtime_session::WorkflowRootSession::default();workflows.open_library(root.clone(),"project",Some(&root),control.clone()).unwrap();
        let library=workflows.active_library().unwrap();
        let state=AppState{desktop_setup:None,endpoint_edits:Arc::new(Mutex::new(Default::default())),compiled_development_selection:json!({"standing":"test-fixture-not-observed"}),connector_drafts:Mutex::new(connector_materialization::Registry::default()),connector_sources:Mutex::new(connector_source::Session::default()),workspace:Some(root.clone()),act:control,file_acts:Mutex::new(file_act_root::FileActRoot::default()),file_act_lapses:Mutex::new(file_act_lapse::Observer::default()),workflows:Mutex::new(workflows),decision_writer_status:Mutex::new(Value::Null),person_name:Mutex::new(None),instructions_root:Mutex::new(Err("unavailable".into())),app_user_data_root:Mutex::new(Err("unavailable".into())),external_observation:Mutex::new(Default::default()),trace_selection:Mutex::new(Default::default()),attachment_selection:Mutex::new(runtime_session::AttachmentSelectionSession::new(Some(root.clone()))),role_log:role_observations::RoleLog::open(&root).map(Arc::new),native_links:Mutex::new(native_conversation_links::Session::default()),project_context:recovery::ExplicitAppProjectContext::unknown(),project_context_limit:Some("unknown".into()),homes:Mutex::new(runtime_session::HomeRouter::new(home.clone()).unwrap()),home_bootstrap:Mutex::new(Err("descriptor unavailable; no inferred home".into())),native_namespaces:Mutex::new(Err("unavailable".into())),key_namespace_admission:Mutex::new(Value::Null),key_setup:Mutex::new(()),root_home_inputs:Value::Null,codex_stop_gate:Mutex::new(()),codex_stops:Mutex::new(Vec::new()),continue_as:Mutex::new(Default::default()),app_quit:Default::default()};
        let (_,context)=current_actor_context_for(&state,&home);
        let package=root.join(workflow_workspace::development_catalog::NAME);std::fs::create_dir(&package).unwrap();
        let catalog=workflow_workspace::development_catalog::DevelopmentCatalog::load().unwrap();for(name,bytes)in catalog.select_embedded().snapshot().files(){std::fs::write(package.join(name),bytes).unwrap();}
        let reference={let mut workflows=state.workflows.lock().unwrap();workflows.select_development_copy(None,package).unwrap();workflows.create_selected_draft(None,"coordinated-knowledge-work").unwrap();workflows.begin_review(home.clone(),context.clone(),vec!["coordinated-knowledge-work".into()],false).unwrap();workflows.active_review.clone().unwrap()};
        (root,state,home,library,reference,context)
    }
    #[test]
    fn file_act_actual_observer_checks_original_context_and_fails_fast_under_contention(){
        let(root,state,home,_,_,_)=fixture();
        let(actor,context)=file_act_observe(&state,&home).unwrap();
        assert_eq!(actor["identityVerified"],false);assert_eq!(context["observedHome"]["hostState"],"absent");
        // The actual confirmation owns act and original review, neither is taken by its observer.
        let held=state.act.lock().unwrap();assert!(file_act_observe(&state,&home).is_ok());drop(held);
        let held=state.homes.lock().unwrap();assert!(file_act_observe(&state,&home).is_err());drop(held);
        let held=home.runtime.lock().unwrap();assert!(file_act_observe(&state,&home).is_err());drop(held);
        let held=state.person_name.lock().unwrap();assert!(file_act_observe(&state,&home).is_err());drop(held);
        *state.person_name.lock().unwrap()=Some("changed person".into());assert_ne!(file_act_observe(&state,&home).unwrap().1,context);
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn j3_reopen_collects_rec_restart_facts_wherever_projected(){
        let e=|id:&str|json!({"kind":"app_restart_interruption","eventId":id,"threadId":"thread"});
        let projection=json!({"state":"initialized","projection":{"restartEvents":[e("a")],"historicalConversations":[{"restartEvents":[e("b")]}]},"other":[{"x":1}]});
        let found=restart_events(&projection);assert_eq!(found.len(),2);assert!(found.contains(&e("a"))&&found.contains(&e("b")));
        assert!(restart_events(&json!({"state":"not-initialized"})).is_empty());
    }
    #[test]
    fn workflow_root_actual_observe_preserves_offline_context_and_refuses_retarget(){
        let(root,state,home,library,reference,context)=fixture();
        let(actor,observed)=workflow_review_observe(&state,&home,&library,&reference,&context).unwrap();assert_eq!(actor["identityVerified"],false);assert_eq!(observed["observedHome"]["hostState"],"absent");
        *state.person_name.lock().unwrap()=Some("changed actor during native interaction".into());assert!(workflow_review_observe(&state,&home,&library,&reference,&context).is_err());
        *state.person_name.lock().unwrap()=None;state.workflows.lock().unwrap().active_review=Some("different-original-operation".into());assert!(workflow_review_observe(&state,&home,&library,&reference,&context).is_err());
        state.workflows.lock().unwrap().active_review=Some(reference.clone());state.workflows.lock().unwrap().active_library=None;assert!(workflow_review_observe(&state,&home,&library,&reference,&context).is_err());
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[cfg(all(test,unix))]
mod file_act_consumer_tests;
#[cfg(test)]
mod file_act_lapse_tests;

#[cfg(test)]
#[path = "../../tests/group_b_fixture_consumer.rs"]
mod group_b_fixture_consumer;

#[cfg(test)]
#[path = "p3_role_entry_tests.rs"]
mod p3_role_entry_tests;

// PKG §4.1 P-2/P-3: a bundle built from the default configuration carries every resource
// the default host reads from `resource_dir()`, at the place it reads it.
#[cfg(test)]
mod bundle_resources_tests {
    use super::*;
    use std::path::Path;
    fn manifest() -> &'static Path { Path::new(env!("CARGO_MANIFEST_DIR")) }
    #[test]
    fn every_default_resource_read_is_declared_in_bundle_resources() {
        let config: Value = serde_json::from_slice(&std::fs::read(manifest().join("tauri.conf.json")).unwrap()).unwrap();
        let declared = config["bundle"]["resources"].as_object().expect("tauri.conf.json declares bundle.resources as a source-to-destination map");
        for (read, source, required) in [(RESOURCE_INSTRUCTIONS, "resources/instructions/", "roles.json"), (RESOURCE_WORKFLOWS, "resources/production_workflows/", "MANIFEST.json")] {
            assert_eq!(declared.get(source).and_then(Value::as_str), Some(format!("{read}/").as_str()), "{source} must be bundled as {read}/");
            assert!(manifest().join(source).join(required).is_file(), "{source}{required} is the source tree");
        }
        assert_eq!(declared.len(), 2, "the default bundle carries only what the default host reads: {declared:?}");
        // The packaged instructions are what the host verifies against.
        runtime_session::verify_production_instructions_root(&manifest().join("resources/instructions")).unwrap();
        // Every `resource_dir()` read in the host names one of those, or is a
        // feature-gated reader supplied by its own packaging overlay.
        let gated = ["let resources = app.path().resource_dir()", "compiled_development_selection::observe_startup(|| app.path().resource_dir()"];
        let mut reads = 0;
        for entry in std::fs::read_dir(manifest().join("src")).unwrap() {
            let path = entry.unwrap().path();
            if path.extension().is_none_or(|e| e != "rs") { continue; }
            for line in std::fs::read_to_string(&path).unwrap().lines() {
                let code = line.trim_start();
                if code.starts_with("mod bundle_resources_tests") { break; }
                if code.starts_with("//") || !code.contains(".resource_dir()") { continue; }
                reads += 1;
                assert!(code.contains("RESOURCE_INSTRUCTIONS") || code.contains("RESOURCE_WORKFLOWS") || gated.iter().any(|g| code.contains(g)),
                    "{}: resource read not declared in bundle.resources: {code}", path.display());
            }
        }
        // Instruction root, workflow root and the shared startup resource root.
        // Startup now passes that same resolved root to compiled selection,
        // instead of resolving it a second time in the observer callback.
        assert!(reads >= 3, "the known resource reads were scanned: {reads}");
    }
}

#[cfg(all(test,unix))]
mod connector_git_guard_tests {
    use super::*;
    #[test]
    fn connector_published_recheck_actual_appstate_handler_and_project_guards(){
      for version in ["0.3","0.4"]{
       let(r,source,registry,token,generation)=connector_materialization::tests::published_fixture(version);
       let(root,mut state,_,_,_,_)=workflow_root_context_tests::fixture();state.workspace=Some(r.root.clone());state.connector_sources=source;state.connector_drafts=registry;
       assert!(recheck_published_connector_for(&state,&token,&generation).is_err());state.project_context_limit=None;
       state.project_context=recovery::ExplicitAppProjectContext::known(r.root.to_str().unwrap(),recovery::AppProjectSource::ConfiguredDirectory).unwrap();
       *state.connector_sources.lock().unwrap()=connector_source::Session::default();
       let result=recheck_published_connector_for(&state,&token,&generation).unwrap();assert_eq!(result["inspection"]["status"],"current_match");
       if let Ok(dir)=std::env::var("C3_PUB_RECHECK_TEST_OUTPUT"){let p=PathBuf::from(dir);std::fs::create_dir_all(&p).unwrap();std::fs::write(p.join(format!("handler-{version}.json")),serde_json::to_vec(&json!({"registry":state.connector_drafts.lock().unwrap().view(),"reply":result})).unwrap()).unwrap();}
       state.workspace=Some(r.root.join("mismatch"));assert!(recheck_published_connector_for(&state,&token,&generation).is_err());state.workspace=None;assert!(recheck_published_connector_for(&state,&token,&generation).is_err());
       std::fs::remove_dir_all(root).unwrap();
      }
    }
    #[test]
    fn connector_git_shared_command_guard_refuses_unknown_mismatch_and_absent_project() {
        let(root,mut state,_,_,_,_)=workflow_root_context_tests::fixture();
        assert!(source_project(&state).is_err());
        state.project_context_limit=None;
        assert!(source_project(&state).is_err());
        state.project_context=recovery::ExplicitAppProjectContext::known(root.to_str().unwrap(),recovery::AppProjectSource::ConfiguredDirectory).unwrap();
        assert_eq!(source_project(&state).unwrap(),root);
        state.workspace=Some(root.join("different"));assert!(source_project(&state).is_err());
        state.workspace=None;assert!(source_project(&state).is_err());
        std::fs::remove_dir_all(root).unwrap();
    }
}
