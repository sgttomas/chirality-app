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
pub mod catalog;
mod checkpoint_recorder;
pub mod codex_stop;
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
pub mod native_items;
pub mod native_history;
pub mod role_lifecycle;
pub mod native_requests;
pub mod receiving;
pub mod recorder;
pub mod records;
pub mod recovery;
mod recovery_root_view;
pub mod role_supply;
pub(crate) mod run_offers;
pub mod runtime_session;
pub(crate) mod workflow_declaration;
pub(crate) mod workflow_workspace;
pub(crate) mod execution_compatibility;
pub(crate) mod a15_native;
pub mod schema_validation;
pub mod standing;
pub mod storage;
pub mod stop_records;
pub mod util;

use act_control::{ActControl, InputSource};
use hosting::{Host, HostConfig};
use serde_json::{json, Value};
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use tauri::{Manager, State};
use tauri_plugin_dialog::{DialogExt, MessageDialogButtons, MessageDialogKind};

pub struct AppState {
    compiled_development_selection: Value,
    connector_sources: Mutex<connector_source::Session>,
    connector_drafts: Mutex<connector_materialization::Registry>,
    workspace: Option<PathBuf>,
    act: Arc<Mutex<Option<ActControl>>>,
    workflows: Mutex<runtime_session::WorkflowRootSession>,
    file_acts: Mutex<file_act_root::FileActRoot>,
    decision_writer_status: Mutex<Value>,
    person_name: Mutex<Option<String>>,
    instructions_root: Mutex<Result<PathBuf, String>>,
    app_user_data_root: Mutex<Result<PathBuf, String>>,
    external_observation: Mutex<runtime_session::ExternalObservationSession>,
    trace_selection: Mutex<runtime_session::TraceSelectionSession>,
    attachment_selection: Mutex<Result<runtime_session::AttachmentSelectionSession, String>>,
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
}

impl AppState {
    fn validate_home_source(&self,home:&runtime_session::HomeSession)->Result<(),String>{
        match &*self.home_bootstrap.lock().unwrap(){
            Ok(set)=>set.validate_binding(home.class(),home.host_config.as_ref().map_err(Clone::clone)?),
            Err(_) if home.class()==home_resources::HomeClass::Account=>Ok(()),
            Err(error)=>Err(error.clone()),
        }
    }
}

/// A fresh probe home for the label probe (HOSTING §7.2 H-probe), in the temp directory.
fn probe_home() -> Result<PathBuf,String> {
    runtime_session::allocate_fresh_probe(&std::env::temp_dir())
}

/// Configuration comes only from the environment; no path is built in (owner rule).
pub fn host_config_from_env(workspace: Option<&PathBuf>) -> Result<HostConfig, String> {
    let bin = std::env::var_os("CHIRALITY_CODEX_BIN").ok_or(()).map_err(|_| {
        "CHIRALITY_CODEX_BIN is not set: no supplier distribution resolved".to_string()
    })?;
    let home = std::env::var_os("CHIRALITY_CODEX_HOME").ok_or(()).map_err(|_| {
        "CHIRALITY_CODEX_HOME is not set: no App-owned Codex home given".to_string()
    })?;
    let cwd = workspace.cloned().unwrap_or_else(std::env::temp_dir);
    let mut cfg = HostConfig::new(bin.into(), home.into(), probe_home()?, cwd);
    cfg.expected_sha256 = std::env::var("CHIRALITY_CODEX_EXPECTED_SHA256").ok();
    cfg.allow_unverified_dev = std::env::var("CHIRALITY_ALLOW_UNVERIFIED")
        .map(|v| v == "1")
        .unwrap_or(false);
    Ok(cfg)
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

#[tauri::command]
fn host_status(state: State<'_, AppState>) -> Value {
    let home = state.homes.lock().unwrap().active();
    let mut runtime = home.runtime.lock().unwrap();
    let (generation, position) = runtime.cursor();
    let observation = home.host.observe(generation, position);
    let received = runtime.receive(&observation);
    let mut s = observation["snapshot"].clone();
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
    let mut history = home.history.lock().unwrap();
    history.reconcile(&home.host);
    let root = state.instructions_root.lock().unwrap().clone();
    s["nativeHistory"] = history.snapshot(root.as_deref().ok());
    s["roleSupply"]["originalStartReceipts"] = s["nativeHistory"]["startReceipts"].clone();
    for thread in s["threads"].as_array_mut().into_iter().flatten() {
        if let (Some(home), Some(id)) = (thread["generation"]["home"].as_str(), thread["threadId"].as_str()) {
            let role = history.role_details(home, id, root.as_deref().ok());
            thread["appRole"] = role["appRole"].clone();
            thread["roleRelation"] = role["roleRelation"].clone();
            thread["futureGuidanceNotices"] = role["futureGuidanceNotices"].clone();
        }
    }
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
    s["homeRouting"] = state.homes.lock().unwrap().snapshot();
    s["homeAccess"] = home.account_view();
    // EXEC §2.4: the checkpoint recorder reads this home's view for its open
    // runs before the run panel is read (runtime -> attachments -> Root -> run).
    runtime_session::record_run_observations(&state.workflows, &s["nativeView"]);
    {
        let root = state.workflows.lock().unwrap();
        s["workflowRoot"] = root.snapshot();
        // RN-3…RN-7: offers from agent messages observed live; display data only.
        s["workflowRoot"]["offers"] = root.offers(&s["nativeView"]);
        // WR §3: the explicit App project can be opened as its own project library.
        s["workflowRoot"]["projectLibraryAvailable"] = json!(state.workspace.is_some());
    }
    s["homeOAuth"] = runtime_session::native_oauth_observation(&home);
    s["continueAs"] = state.continue_as.lock().unwrap().view(&s);
    s["codexStops"] = json!({"outcomes":state.codex_stops.lock().unwrap().clone(),"stopWaitLimitSeconds":codex_stop::STOP_WAIT_LIMIT.as_secs(),"records":codex_stop::RECORDS_LIMIT});
    s["connectorRouteAvailability"] = connector_route_view::availability(state.workspace.as_deref(), &state.project_context, state.project_context_limit.as_deref());
    s["currentAppProjectContext"] = state.project_context.view();
    s["currentAppProjectContextLimit"] = json!(state.project_context_limit);
    if let Err(e) = &*state.instructions_root.lock().unwrap() {
        s["instructionsProblem"] = json!(e);
    }
    s
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
    Ok(homes.snapshot())
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
                let home=Arc::new(runtime_session::HomeSession::new(home_resources::HomeClass::ApiKey,host,Ok(config.clone()))?);
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
fn refused_role_entry(role: Option<role_supply::Role>, reason: &str) -> Value {
    json!({"state":"refused-before-send","selection":role,"roleSet":role_supply::content(role_supply::BUNDLED_ROLE_SET),"reason":reason,"adoption":"unknown"})
}

#[tauri::command(async)]
fn thread_start(
    app: tauri::AppHandle,
    state: State<'_, AppState>,
    model: String,
    model_provider: String,
    entry_id: String,
    mode_home_class: String,
    role: Option<role_supply::Role>,
    continue_as: Option<String>,
) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().entry(home_class(&mode_home_class)?)?;
    // NIR CA-1/CA-3, ROLE CA-3: a "Continue as" start is an ordinary new start
    // with its own role composition; it only records its relation to the source.
    let continued_from = conversation_roles::continuation_for_start(&state.continue_as, &home, continue_as.as_deref(), role)?;
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
            app.path().resource_dir().map(|path| path.join("instructions"))
                .map_err(|error| format!("Production instruction resource directory unavailable: {error}"))
        })
    })();
    let (composition, package_correspondence) = match prepared {
        Ok(prepared) => prepared,
        Err(reason) => {
            *home.role_supply_status.lock().unwrap() = refused_role_entry(role, &reason);
            return Err(reason);
        }
    };
    composition.verify()?;
    let generation = home.host.snapshot()["generation"].clone();
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
        let supply_ref = runtime_session::claim_start(&mut slot, selection, || util::opaque_id("sup:"))?;
        *home.role_supply_status.lock().unwrap() = json!({"state":"starting","attemptId":attempt_id,"selection":role,"roleSet":composition.role_set_identity(),"packageCorrespondence":package_correspondence,"generation":generation,"carried":composition.carried,"adoption":"unknown","nativeChildRoles":composition.child_status(None,false),"continuedFrom":continued_from});
        supply_ref
    };
    // Freeze the verified original composition before native dispatch. Actual
    // Host receipt IDs, exact sent bytes and correlated results bind its role.
    let dispatch = home.host.thread_start_with_guidance_dispatch(&generation, &cwd, &model, &model_provider, &composition.text);
    // All post-claim failures flow through finalization; ? cannot strand Starting.
    let result = (|| -> Result<Value, String> { match dispatch {
        Ok(receipt) => {
            home.history.lock().unwrap().start_dispatched_continuing(receipt.clone(), &composition, &supply_ref, continued_from.clone())
                .map_err(|error| format!("Native start dispatched; original role preparation failed: {error}. Native effect remains as observed in the retained receipt; no automatic resend"))?;
            let waited = home.host.source_request_wait(&receipt, std::time::Duration::from_secs(20));
            home.history.lock().unwrap().reconcile(&home.host);
            match waited {
                Ok(evidence) if home.history.lock().unwrap().start_admitted(&receipt) => Ok(evidence["response"].clone()),
                Ok(evidence) => Err(format!("Native start remains {} (write {}); no automatic retry", evidence["outcome"], evidence["writeResult"])),
                Err(error) => Err(error),
            }
        },
        Err(error) => Err(error),
    } })();
    let result = {
        let mut slot = home.access_selection.lock().unwrap();
        let result = match slot.as_mut() {
            Some(selection) => runtime_session::finalize_start_attempt(selection, &attempt_id, &generation, &home.host.snapshot()["generation"], result),
            None => Err("Start selection unavailable; native effect remains as observed in retained receipts".into()),
        };
        let mut status = home.role_supply_status.lock().unwrap();
        if status["attemptId"] == attempt_id && status["generation"] == generation {
            *status = json!({"state":if result.is_ok(){"response-observed"}else{"start-failed-or-unknown"},"attemptId":attempt_id,"selection":role,"roleSet":composition.role_set_identity(),"packageCorrespondence":package_correspondence,"generation":generation,"carried":composition.carried,"adoption":"unknown","nativeChildRoles":composition.child_status(None,false),"continuedFrom":continued_from});
        }
        result
    };
    conversation_roles::mark_started(&state.continue_as, continue_as.as_deref(), &result, &generation);
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
    home.history.lock().unwrap().dispatched(receipt.clone());
    let waited = home.host.history_wait(&receipt, std::time::Duration::from_secs(20));
    // The page also feeds the readable native view (DEL-01-03 REQ-001: plan and
    // other items are recovered from Codex history). Runtime before history lock,
    // matching host_status's order.
    if let Ok(evidence) = &waited {
        if let Some(result) = evidence["response"].get("result") {
            home.runtime.lock().unwrap().receive_history(query.generation(), query.home(), query.method(), query.params(), result);
        }
    }
    let mut history = home.history.lock().unwrap();
    history.reconcile(&home.host);
    waited?;
    let root = state.instructions_root.lock().unwrap().clone();
    Ok(history.snapshot(root.as_deref().ok()))
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

#[tauri::command(async)]
fn conversation_send_text(
    state: State<'_, AppState>,
    generation: Value,
    thread_id: String,
    text: String,
    mode: Option<String>,
) -> Result<Value, String> {
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    if let Some(mode) = mode {
        runtime_session::mode_send_blocked_by_notice(&state.workflows, &generation, &thread_id)?;
        return runtime_session::send_conversation_text(
            &home.host.snapshot(), &generation, &thread_id, &text,
            |generation, thread, text| home.host.turn_start_text_mode(generation, thread, text, &mode),
        );
    }
    // WR TX-5 / SQ-END: when a run in this conversation ended with no successor,
    // this next ordinary turn carries its end notice first, exactly once.
    if let Some(result) = runtime_session::send_with_pending_notice(&state.workflows, &generation, &thread_id, &text) {
        return result;
    }
    runtime_session::send_conversation_text(
        &home.host.snapshot(),
        &generation,
        &thread_id,
        &text,
        |generation, thread, text| home.host.turn_start_text(generation, thread, text),
    )
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

/// NIR CA-4, ROLE F-1: "Fork (same role)".
#[tauri::command(async)]
fn conversation_fork(state: State<'_, AppState>, generation: Value, thread_id: String) -> Result<Value, String> {
    conversation_roles::fork_command(&state.homes, &generation, &thread_id, std::time::Duration::from_secs(20))
}

/// Paths come exclusively from native file selection; no path/origin is an IPC argument.
#[tauri::command(async)]
fn submit_attachments(state:State<'_,AppState>,owner_ref:String,list_revision:u64,selection_refs:Vec<String>,generation:Value,thread_id:String,expected_turn_id:Option<String>,text:String)->Result<Value,String>{
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    let context=state.project_context.clone();
    let recovery_home=home.thread_home_kinds.lock().unwrap().get(&serde_json::to_string(&json!([generation,thread_id])).unwrap()).copied();
    let custody=home.attachment_custody.lock().unwrap().clone();
    runtime_session::submit_attachments_with_draft_trials(&state.attachment_selection,&state.workflows,&home.host,custody,&owner_ref,list_revision,&selection_refs,&generation,&thread_id,expected_turn_id.as_deref(),&text,context,recovery_home)
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

/// Public reattachment is read-only and always uses the complete owning tuple.
#[tauri::command]
fn host_observe(state: State<'_, AppState>, generation: Value, after: u64) -> Value {
    let home = match state.homes.lock().unwrap().for_generation(&generation) { Ok(home)=>home,Err(error)=>return json!({"error":error,"generation":generation,"frames":[]}) };
    home.host.observe(&generation, after)
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
    let (generation, position) = runtime.cursor();
    let observation = home.host.observe(generation, position);
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
    let home = state.homes.lock().unwrap().for_generation(&generation)?;
    let (snapshot, context) = current_actor_context_for(&state, &home);
    let actor = runtime_session::actor_reference(
        context["displayName"].as_str(),
        context["osAccount"].as_str(),
        context["codexAccount"].as_str(),
    );
    let preview =
        runtime_session::answer_preview(&snapshot, &generation, &request_id, &answer, &actor)?;
    // Owner's three-button layout: Return chooses "Don't send"; an abort maps
    // to "Cancel"; only the middle "Send answer" sends. A statement too long for
    // the alert names the preview by digest while the App shows it whole.
    use act_control::native_statement::{self as ns, DONT_SEND, SEND_ANSWER};
    let statement = ns::request_answer_statement(&preview)?;
    let result = ns::showing_in_app(statement.in_app.as_ref(), || {
        app.dialog()
            .message(statement.text.clone())
            .title("Chirality — answer native request")
            .kind(MessageDialogKind::Warning)
            .buttons(ns::act_buttons(DONT_SEND, SEND_ANSWER))
            .blocking_show_with_result()
    });
    if !ns::chose(&result, SEND_ANSWER) {
        return Ok(json!({"state":"dismissed","replyWriteResult":"not-attempted"}));
    }
    let (snapshot, current) = current_actor_context_for(&state, &home);
    if current != context {
        return Err("Attribution or owning host context changed during confirmation; review and confirm again".into());
    }
    runtime_session::answer_preview(&snapshot, &generation, &request_id, &answer, &actor)?;
    home.host.answer_server_request(
        &generation,
        &request_id,
        &answer,
        "person-via-interaction",
        Some(&actor),
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
fn workflow_select_development(app:tauri::AppHandle,state:State<'_,AppState>)->Result<Value,String>{
    let Some(path)=workflow_native_folder(&app,"Select exact coordinated-knowledge-work development holding copy")? else{return Ok(json!({"state":"native selection dismissed"}));};
    let view=active_native_view(&state);
    noted_selection(&state,&view,|root|root.select_development_copy(path))
}
/// The active home's native view, read before a selection takes the Root guard.
fn active_native_view(state:&AppState)->Value{
    let home=state.homes.lock().unwrap().active();
    current_native_view(&home)
}
/// WR PR-5: a successful selection by the person supersedes agent proposals
/// received up to `view`; a failed one changes nothing.
fn noted_selection(state:&AppState,view:&Value,select:impl FnOnce(&mut runtime_session::WorkflowRootSession)->Result<Value,String>)->Result<Value,String>{
    let mut root=state.workflows.lock().unwrap();
    let selected=select(&mut root)?;
    root.note_selection(view);
    Ok(selected)
}
#[tauri::command(async)]
fn workflow_select_production_bundle(app:tauri::AppHandle,state:State<'_,AppState>,name:String)->Result<Value,String>{
    let root=app.path().resource_dir().map_err(|e|format!("App resources unavailable: {e}"))?.join("workflows");
    let view=active_native_view(&state);
    noted_selection(&state,&view,|workflows|workflows.select_production_bundle(root,&name))
}
#[tauri::command]
fn workflow_select_production_copy(state:State<'_,AppState>,name:String)->Result<Value,String>{
    let view=active_native_view(&state);
    noted_selection(&state,&view,|root|root.select_production_copy(&name))
}
#[tauri::command(async)]
fn workflow_open_library(app:tauri::AppHandle,state:State<'_,AppState>,origin:String)->Result<Value,String>{
    if !matches!(origin.as_str(),"project"|"user"){return Err("Choose project or user library; no default".into());}
    let Some(path)=workflow_native_folder(&app,"Open existing physical workflow library root")? else{return Ok(json!({"state":"native library selection dismissed"}));};
    let view=active_native_view(&state);
    let mut root=state.workflows.lock().unwrap();root.open_library(path,&origin,state.workspace.as_deref(),state.act.clone())?;
    // WR SQ-D D-2: the opened library's drafts are listed at once.
    Ok(root.observe_drafts(&view["items"]).unwrap_or_else(|_|root.snapshot()))
}
#[tauri::command(async)]
fn workflow_select_registered(app:tauri::AppHandle,state:State<'_,AppState>,review_ref:String,revision:String)->Result<Value,String>{
    let Some(path)=workflow_native_folder(&app,"Select actual holding copy of this hot registered revision")? else{return Ok(json!({"state":"native selection dismissed"}));};
    let view=active_native_view(&state);
    noted_selection(&state,&view,|root|root.select_hot_registered_copy(&review_ref,&revision,path))
}
/// WR §3: the explicit App project's own library, without a folder picker.
#[tauri::command(async)]
fn workflow_open_project_library(state:State<'_,AppState>)->Result<Value,String>{
    let view=active_native_view(&state);
    let mut root=state.workflows.lock().unwrap();root.open_project_library(state.workspace.as_deref(),state.act.clone())?;
    // The library is open either way; a listing that cannot run now says so in the list.
    Ok(root.observe_drafts(&view["items"]).unwrap_or_else(|_|root.snapshot()))
}
/// WR SQ-D D-2…D-4 in the host (OI-008 ruling): observe the active library's drafts now.
#[tauri::command(async)]
fn workflow_observe_drafts(state:State<'_,AppState>)->Result<Value,String>{
    let view=active_native_view(&state);
    state.workflows.lock().unwrap().observe_drafts(&view["items"])
}
/// WR TT-3 / NIR AT-8: pre-fill the attachment list with a listed draft's files.
/// Never sends; the person sends with the ordinary attachment-bearing control.
#[tauri::command(async)]
fn workflow_try_draft(state:State<'_,AppState>,owner_ref:String,list_revision:u64,name:String)->Result<Value,String>{
    let sources=state.workflows.lock().unwrap().draft_trial_sources(&name)?;
    let mut selection=state.attachment_selection.lock().unwrap();
    selection.as_mut().map_err(|error|error.clone())?.prefill_draft(&owner_ref,list_revision,sources)
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
fn workflow_create_draft(state:State<'_,AppState>,name:String)->Result<Value,String>{state.workflows.lock().unwrap().create_selected_draft(&name)}
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
fn workflow_prepare_run(state:State<'_,AppState>,generation:Value,thread_id:String,person_text:String)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;state.validate_home_source(&home)?;
    // WR WP-1: the explicit App project owns WR records; None is refused with no fallback.
    let mut root=state.workflows.lock().unwrap();let reference=root.prepare_run(home,&generation,&thread_id,person_text,state.workspace.as_deref())?;Ok(json!({"reference":reference,"state":"original registered selection prepared; WR records pending; not sent"}))
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
    let (generation,position)=runtime.cursor();
    let observation=home.host.observe(generation,position);
    runtime.receive(&observation)["nativeView"].clone()
}
/// EXEC AE-7 / A-11: only the person's explicit end ends a run. FN-2: the cause is
/// *completed* only when the person ends it on the agent's finished report, which
/// the host re-reads from the message it observed; the caller cannot assert it.
#[tauri::command]
fn workflow_end_run(state:State<'_,AppState>,run_ref:String,finished_report:Option<Value>)->Result<Value,String>{
    let run=state.workflows.lock().unwrap().runs.get(&run_ref).cloned().ok_or("Actual run unavailable in this process")?;
    let home=run.try_lock().map_err(|_|"Original run operation pending")?.home.clone();
    let view=current_native_view(&home);
    state.workflows.lock().unwrap().end_requested(&run_ref,&view,finished_report.as_ref())
}
/// RN-3/RN-4, PR-4: the person starts the workflow an agent message proposed (or,
/// with a run in force, ends it and starts the proposed one). The proposal is
/// re-read from the observed message; it never selects or starts anything itself.
#[tauri::command(async)]
fn workflow_start_proposed(state:State<'_,AppState>,generation:Value,message:Value,run_ref:Option<String>,person_text:String)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;state.validate_home_source(&home)?;
    let view=current_native_view(&home);
    let next=state.workflows.lock().unwrap().start_proposed(&view,home,&generation,&message,run_ref.as_deref(),person_text,state.workspace.as_deref())?;
    let started=runtime_session::start_workflow_run(&state.workflows,&next);
    Ok(json!({"ended":run_ref,"started":next,"start":match started{Ok(v)=>v,Err(e)=>json!({"state":"proposed workflow run prepared but not started","limit":e})}}))
}
/// CH-1 "End ‹A› and start ‹B›" as one confirmed step: A ends, B is prepared and started.
#[tauri::command(async)]
fn workflow_end_and_start(state:State<'_,AppState>,run_ref:String,generation:Value,thread_id:String,person_text:String)->Result<Value,String>{
    let home=state.homes.lock().unwrap().for_generation(&generation)?;state.validate_home_source(&home)?;
    let view=current_native_view(&home);
    let next=state.workflows.lock().unwrap().end_and_start_viewed(&view,&run_ref,home,&generation,&thread_id,person_text,state.workspace.as_deref())?;
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
    let events=restart_events(&recovery);
    state.workflows.lock().unwrap().reopen(root,&events)
}
/// The person's explicit end of a run the record shows open and interrupted after relaunch.
#[tauri::command]
fn workflow_end_recorded(state:State<'_,AppState>,run_id:String,thread_id:Option<String>)->Result<Value,String>{
    let root=state.workspace.as_ref().ok_or("No explicit App project (CHIRALITY_WORKSPACE); nothing recorded and no fallback")?;
    let thread=thread_id.ok_or("The record names no conversation for this run; it cannot be ended from here")?;
    // V10 G-7: a reopened run is ended only as the person's plain end (no completed).
    state.workflows.lock().unwrap().end_recorded_run(root,&run_id,&thread,false)
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
    let (generation,position)=runtime.cursor();
    let observed=home.host.observe(generation,position);
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
fn file_act_confirm_original(state:&AppState,reference:&str,
    confirm:impl FnOnce(&mut ActControl,&act_control::FileActOfferRef,&mut dyn FnMut()->Result<(Value,Value),String>)->Result<Option<Value>,String>
)->Result<Value,String>{
    let owner=state.file_acts.try_lock().map_err(|_|"File offer state busy")?.get(&reference)?;
    let mut owner=owner.try_lock().map_err(|_|"Original file operation pending")?;
    if owner.attempted{return Err("Original attempt retained; continue its recording or review a new offer".into());}
    let home=owner.home.clone();let original=owner.context.clone();
    let mut control=state.act.try_lock().map_err(|_|"Act owner busy; no native attempt")?;
    let control=control.as_mut().ok_or("Original act owner absent")?;
    owner.attempted=true;
    let result=confirm(control,&owner.offer,&mut ||{
        let observed=file_act_observe(&state,&home)?;
        if observed.1!=original{return Err("Actor or owning context changed since preview; review again".into());}
        Ok(observed)
    });
    owner.status=match result{Ok(Some(value))=>value,Ok(None)=>json!({"state":"dismissed; nothing captured","recorded":false}),Err(error)=>json!({"state":"native attempt returned an error; capture/record standing not established by this result","error":error})};
    Ok(owner.status.clone())
}
#[tauri::command(async)]
fn file_act_continue(state:State<'_,AppState>,reference:String)->Result<Value,String>{
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
    Ok(view)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let workspace = std::env::var_os("CHIRALITY_WORKSPACE").map(PathBuf::from);
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .setup(move |app| {
    let host_config = if tauri::is_dev() || !cfg!(feature = "distribution-successor") {
        host_config_from_env(workspace.as_ref()).and_then(|mut cfg| {
            if tauri::is_dev() && std::env::var("CHIRALITY_DISTRIBUTION_SUCCESSOR").as_deref() == Ok("1") {
                cfg.distribution = Some(hosting::successor::Distribution::development_from_binary(&cfg.codex_bin)?);
            }
            Ok(cfg)
        })
    } else {
        (|| {
            let resources = app.path().resource_dir().map_err(|e|e.to_string())?;
            let data = app.path().app_data_dir().map_err(|e|e.to_string())?;
            let home = std::env::var_os("CHIRALITY_CODEX_HOME").map(PathBuf::from).ok_or("No explicit App-owned account home")?;
            Ok(hosting::successor::production_config(resources, home, probe_home()?, workspace.clone().unwrap_or(data)))
        })()
    };
    let host_config = host_config.map(|mut cfg| { cfg.require_distribution_artifacts = cfg.distribution.is_some(); cfg });
    let project = runtime_session::freeze_configured_project(workspace.as_deref());
    let project_context_limit = project.as_ref().err().cloned();
    let project_context = project.unwrap_or_else(|_|recovery::ExplicitAppProjectContext::unknown());
    let home = Arc::new(runtime_session::HomeSession::new(home_resources::HomeClass::Account,Arc::new(Host::new()),host_config.clone()).expect("account entry"));
    let key_path = std::env::var_os("CHIRALITY_KEY_HOME").map(PathBuf::from);
    let shared_paths = ["CHIRALITY_SHARED_CONFIG","CHIRALITY_SHARED_AGENTS","CHIRALITY_SHARED_SKILLS"].map(|key|std::env::var_os(key).map(PathBuf::from));
    let state = AppState {
        compiled_development_selection: compiled_development_selection::observe_startup(|| app.path().resource_dir().map_err(|e| e.to_string())),
        connector_sources: Mutex::new(connector_source::Session::default()),
        connector_drafts: Mutex::new(connector_materialization::Registry::default()),
        act: Arc::new(Mutex::new(workspace.as_ref().map(|w| ActControl::new(w)))),
        workflows: Mutex::new(runtime_session::WorkflowRootSession::default()),
        file_acts: Mutex::new(file_act_root::FileActRoot::default()),
        decision_writer_status: Mutex::new(json!({"state":"not-run","responsibility":"decision record writer continuation"})),
        workspace: workspace.clone(),
        person_name: Mutex::new(None),
        instructions_root: Mutex::new(Err("App instruction root not initialized".into())),
        app_user_data_root: Mutex::new(Err("App user-data root not initialized".into())),
        external_observation: Mutex::new(runtime_session::ExternalObservationSession::default()),
        trace_selection: Mutex::new(runtime_session::TraceSelectionSession::default()),
        attachment_selection: Mutex::new(runtime_session::AttachmentSelectionSession::new(workspace.clone())),
        project_context, project_context_limit,
        homes: Mutex::new(runtime_session::HomeRouter::new(home.clone()).expect("explicit primary account class")),
        home_bootstrap: Mutex::new(Err("Explicit Root home descriptors not initialized".into())),
        native_namespaces: Mutex::new(Err("Root native namespace bindings not initialized".into())),
        key_namespace_admission: Mutex::new(json!({"state":"prospective key not admitted"})),
        key_setup: Mutex::new(()),
        root_home_inputs: json!({"source":"explicit Root native environment path inputs","keyHome":key_path.as_ref().map(|path|attachments::native_path_identity(path)),"sharedConfig":shared_paths[0].as_ref().map(|path|attachments::native_path_identity(path)),"sharedGlobalAgents":shared_paths[1].as_ref().map(|path|attachments::native_path_identity(path)),"sharedSkills":shared_paths[2].as_ref().map(|path|attachments::native_path_identity(path)),"limit":"supplied references are not observed linked state, ownership or native discovery proof"}),
        codex_stop_gate: Mutex::new(()),
        codex_stops: Mutex::new(Vec::new()),
        continue_as: Mutex::new(conversation_roles::Handoffs::default()),
    };
    let host = Arc::clone(&home.host);
            app.manage(state);
            let data = app.path().app_data_dir().map_err(|e| e.to_string());
            let state = app.state::<AppState>();
            *state.home_bootstrap.lock().unwrap() = (|| {
                let data=data.as_ref().map_err(Clone::clone)?;
                let cfg=home.host_config.as_ref().map_err(Clone::clone)?;
                runtime_session::freeze_root_home_descriptors(data,cfg,key_path.clone(),shared_paths.clone()).map(Arc::new)
            })();
            // Startup owns this separate writer continuation. Neither decision
            // view reads nor host/status polling invokes the writer.
            if let Some(ws) = state.workspace.as_ref() {
                let mut control = state.act.lock().unwrap();
                *state.decision_writer_status.lock().unwrap() = runtime_session::continue_decision_writer(ws, control.as_mut(), "app-startup-writer");
            }
            *state.app_user_data_root.lock().unwrap() = data.clone();
            // WR §3: App-kept draft bases live in the App data folder.
            if let Ok(data) = data.as_ref() { state.workflows.lock().unwrap().set_app_user_data(data.clone()); }
            // Current account/probe protection is independent of a bad new key
            // candidate; do not create/adopt K or replace an existing L binding.
            let namespaces=(|| {
                let data=data.as_ref().map_err(Clone::clone)?;
                let cfg=home.host_config.as_ref().map_err(Clone::clone)?;
                runtime_session::freeze_root_home_descriptors(data,cfg,None,shared_paths.clone())?.native_namespaces(false)
            })();
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
                            hosting::successor::Distribution::Development { .. } => crate::distribution_store::Store::open(data,&vendor,namespaces.clone()?),
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
                        || h.start(&cfg, "app-startup"),
                    );
                });
            }
            Ok(())
        })
        // DEF-1: closing or reloading a window is not a stop (HOSTING §4.5); no window
        // event touches the child.
        .invoke_handler(tauri::generate_handler![
            file_act_select, file_act_confirm, file_act_continue, file_act_dismiss, file_act_read,
            read_recovery_custody,
            read_connector_routes,
            prepare_connector_source, select_connector_source, anchor_connector_source, revise_connector_source,
            read_connector_git, cancel_connector_git, anchor_connector_git,
            recheck_published_connector_draft, prepare_connector_reconstruction, prepare_connector_draft, publish_connector_draft, cancel_connector_draft, reconcile_connector_draft, inspect_connector_drafts,
            host_status,
            select_home,
            read_home_access,
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
            history_action,
            history_select,
            conversation_send_text,
            collaboration_modes_read,
            conversation_steer_text,
            conversation_interrupt,
            continue_as_begin,
            continue_as_dismiss,
            conversation_fork,
            set_person_name,
            workflow_select_development,workflow_select_production_bundle,workflow_select_production_copy,workflow_open_library,workflow_open_project_library,workflow_observe_drafts,workflow_try_draft,workflow_review_draft,workflow_select_registered,workflow_create_draft,workflow_refine_registered,workflow_review,workflow_register_native,workflow_continue_registration,workflow_prepare_run,workflow_send_run,workflow_check_supply,workflow_retry_records,workflow_read_records,workflow_end_run,workflow_start_proposed,workflow_end_and_start,workflow_check_notice,workflow_skip_notice,workflow_reopen,workflow_end_recorded,workflow_review_digest,native_confirmation_content,
            decision_view,
            continue_decision_recording,
            compose_offer,
            decide
        ])
        .build(tauri::generate_context!())
        .expect("error while building the Tauri application")
        .run(|app, event| {
            // A confirmed App quit is a deliberate stop (DEF-6 -> DEF-5a).
            if let tauri::RunEvent::Exit = event {
                let st: State<'_, AppState> = app.state();
                let homes=st.homes.lock().unwrap().entries();
                if let Some(account)=homes.iter().find(|home|home.class()==home_resources::HomeClass::Account){if let Ok(custody)=account.host.app_runtime_custody(){custody.close_distribution_publication();}}
                for home in &homes { let _=home.host.stop("the person","App quit"); }
                // DEF-5 native process-stop facts remain in each actual Host's
                // lifecycle. They are not DEF-3 REC stopRequestId references.
                // Empty here means no owned REC stop references supplied, not
                // no interrupted work, child stop or successful termination.
                if let Some(account)=homes.iter().find(|home|home.class()==home_resources::HomeClass::Account){if let Ok(custody)=account.host.app_runtime_custody(){let _=custody.record_app_session_end(&[]);}}
            }
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
        let state=AppState{compiled_development_selection:json!({"standing":"test-fixture-not-observed"}),connector_drafts:Mutex::new(connector_materialization::Registry::default()),connector_sources:Mutex::new(connector_source::Session::default()),workspace:Some(root.clone()),act:control,file_acts:Mutex::new(file_act_root::FileActRoot::default()),workflows:Mutex::new(workflows),decision_writer_status:Mutex::new(Value::Null),person_name:Mutex::new(None),instructions_root:Mutex::new(Err("unavailable".into())),app_user_data_root:Mutex::new(Err("unavailable".into())),external_observation:Mutex::new(Default::default()),trace_selection:Mutex::new(Default::default()),attachment_selection:Mutex::new(runtime_session::AttachmentSelectionSession::new(Some(root.clone()))),project_context:recovery::ExplicitAppProjectContext::unknown(),project_context_limit:Some("unknown".into()),homes:Mutex::new(runtime_session::HomeRouter::new(home.clone()).unwrap()),home_bootstrap:Mutex::new(Err("descriptor unavailable; no inferred home".into())),native_namespaces:Mutex::new(Err("unavailable".into())),key_namespace_admission:Mutex::new(Value::Null),key_setup:Mutex::new(()),root_home_inputs:Value::Null,codex_stop_gate:Mutex::new(()),codex_stops:Mutex::new(Vec::new()),continue_as:Mutex::new(Default::default())};
        let (_,context)=current_actor_context_for(&state,&home);
        let package=root.join(workflow_workspace::development_catalog::NAME);std::fs::create_dir(&package).unwrap();
        let catalog=workflow_workspace::development_catalog::DevelopmentCatalog::load().unwrap();for(name,bytes)in catalog.select_embedded().snapshot().files(){std::fs::write(package.join(name),bytes).unwrap();}
        let reference={let mut workflows=state.workflows.lock().unwrap();workflows.select_development_copy(package).unwrap();workflows.create_selected_draft("coordinated-knowledge-work").unwrap();workflows.begin_review(home.clone(),context.clone(),vec!["coordinated-knowledge-work".into()],false).unwrap();workflows.active_review.clone().unwrap()};
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
#[path = "../../tests/group_b_fixture_consumer.rs"]
mod group_b_fixture_consumer;

#[cfg(test)]
#[path = "p3_role_entry_tests.rs"]
mod p3_role_entry_tests;

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
