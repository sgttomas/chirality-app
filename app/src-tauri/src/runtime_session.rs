//! Disposable receiving views backed by the main-process full-generation observer.
//! No supplier history or submitted answer is copied to durable App storage.
use crate::{
    access::AccountObservation, native_items::NativeView, native_requests::RequestRegister,
};
use serde_json::{json, Value};

#[derive(Default)]
pub struct RuntimeSession {
    generation: Value,
    position: u64,
    view: Option<NativeView>,
    account: Option<AccountObservation>,
    closed: bool,
    limits: Vec<String>,
    account_revision: u64,
    prior_views: Vec<Value>,
    closed_generations: Vec<Value>,
}
impl RuntimeSession {
    pub fn cursor(&self) -> (&Value, u64) {
        (&self.generation, self.position)
    }
    pub fn receive(&mut self, observation: &Value) -> Value {
        let snapshot = &observation["snapshot"];
        let generation = &observation["generation"];
        let active = snapshot["state"] == "ready";
        if generation != &self.generation {
            let previous = self.generation.clone();
            let mut losses = Vec::new();
            if let Some(view) = self.view.as_mut() {
                view.close(&previous)
                    .unwrap_or_else(|e| self.limits.push(e));
                let ended = view.snapshot();
                for gap in ended["checklistGaps"].as_array().into_iter().flatten() {
                    losses.push(format!(
                        "Prior generation {} · thread {} · turn {}: {}",
                        previous, gap["threadId"], gap["turnId"], gap["reason"]
                    ));
                }
                self.prior_views.push(json!({"generation":previous,"standing":"observation-ended; not live custody","view":ended,"receivingLimits":self.limits}));
                if !self.closed_generations.contains(&previous) {
                    self.closed_generations.push(previous);
                }
            }
            self.view = None;
            self.account = None;
            self.account_revision = self.account_revision.saturating_add(1);
            self.position = 0;
            self.closed = self.closed_generations.contains(generation);
            self.limits = losses;
            if !self.prior_views.is_empty() {
                self.limits.push("Observation lost across generation boundary; Codex history has not been read or rebuilt by this App path".into());
            }
            if self.closed {
                self.limits
                    .push("Closed receiving generation cannot be reactivated".into());
            }
            self.generation = generation.clone();
        }
        if active && self.view.is_none() && !self.closed {
            if let Some(home) = generation["home"].as_str() {
                match NativeView::new(home.into()).and_then(|mut view| {
                    view.ready(
                        generation.clone(),
                        snapshot["versionIdentity"].clone(),
                        snapshot["supplierStanding"].clone(),
                    )?;
                    Ok(view)
                }) {
                    Ok(view) => self.view = Some(view),
                    Err(e) => self.limits.push(e),
                }
                self.account = AccountObservation::new(home.into(), generation.clone()).ok();
            }
        }
        // Deliver admitted unseen frames of the known open generation before its
        // terminal close. Already-closed generations are never replayed as live.
        if self.view.is_some() && !self.closed {
            for frame in observation["frames"].as_array().into_iter().flatten() {
                let Some(position) = frame["position"].as_u64() else {
                    continue;
                };
                if position <= self.position {
                    continue;
                }
                if frame["class"] == "closed-generation-frame" {
                    self.limits.push("post-closure native frame refused".into());
                    continue;
                }
                if frame["generation"] != self.generation {
                    self.limits.push("foreign observer envelope refused".into());
                    continue;
                }
                if let Some(view) = self.view.as_mut() {
                    if let Err(e) = view.consume(frame) {
                        self.limits.push(format!("native view at {position}: {e}"));
                    }
                }
                // Account information comes only from a correlated native account/read
                // response of this generation; this consumer issues no account request.
                let native = &frame["frame"];
                if native["method"] == "account/updated" {
                    self.account_revision = self.account_revision.saturating_add(1);
                    // A change notice is not an account identity. Invalidate the last
                    // report until another same-generation read actually supplies it.
                    if let Some(account) = self.account.as_mut() {
                        account.lost();
                    }
                }
                let correlated = snapshot["clientRequests"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .any(|r| {
                        r["generation"] == self.generation
                            && r["method"] == "account/read"
                            && r["requestIdentity"] == native["id"]
                            && r["outcome"] == "response-observed-result"
                    });
                if frame["class"] == "response" && correlated {
                    self.account_revision = self.account_revision.saturating_add(1);
                    if let Some(account) = self.account.as_mut() {
                        if let Err(e) = account.read(&self.generation, &native["result"]) {
                            self.limits.push(e);
                        }
                    }
                }
                self.position = position;
            }
        }
        if !active && self.view.is_some() && !self.closed && snapshot["state"] != "handshaking" {
            if let Some(view) = self.view.as_mut() {
                let _ = view.close(&self.generation);
            }
            if let Some(account) = self.account.as_mut() {
                account.lost();
            }
            self.closed = true;
            if !self.closed_generations.contains(&self.generation) {
                self.closed_generations.push(self.generation.clone());
            }
            self.account_revision = self.account_revision.saturating_add(1);
        }
        let requests = snapshot["serverRequests"]
            .as_array()
            .cloned()
            .unwrap_or_default();
        json!({"nativeView":self.view.as_ref().map(|v|v.snapshot_with_requests(&requests)),
            "accountObservation":self.account.as_ref().map(AccountObservation::snapshot),
            "nativeViewLimits":self.limits,"observerCursor":{"generation":self.generation,"position":self.position},
            "observerGap":observation["gap"],"priorNativeViews":self.prior_views,"nativeViewObservationEnded":self.closed,
            "observerRecovery":{"historyRebuilt":false,"historyRead":"not implemented in this App path","standing":"App-observed receiving state; not recovered Codex history"}})
    }
    /// Consume the current atomic Host observation before freezing attribution.
    /// Revisions also detect an account change followed by a same-email reread.
    pub fn actor_context(
        &mut self,
        observation: &Value,
        name: Option<&str>,
        os: Option<&str>,
    ) -> Value {
        self.receive(observation);
        json!({"generation":observation["generation"],"hostState":observation["snapshot"]["state"],
            "displayName":name,"osAccount":os,"codexAccount":self.codex_account_for(&observation["generation"]),
            "accountRevision":self.account_revision})
    }
    pub fn codex_account_for(&self, generation: &Value) -> Option<String> {
        if generation != &self.generation || self.closed {
            return None;
        }
        self.account
            .as_ref()
            .and_then(AccountObservation::codex_account)
    }
}

/// Derive attribution from App-owned inputs, never a caller-supplied actor/origin.
pub fn actor_reference(name: Option<&str>, os: Option<&str>, account: Option<&str>) -> String {
    format!(
        "person:{} / {} / {} (identity not verified)",
        name.unwrap_or("unnamed"),
        os.unwrap_or("unknown OS account"),
        account.unwrap_or("no Codex account reported")
    )
}

/// Validate against the live card and native offered shapes before native confirmation.
/// The temporary register is not authoritative custody and never writes anything.
pub fn answer_preview(
    snapshot: &Value,
    generation: &Value,
    id: &Value,
    answer: &Value,
    actor: &str,
) -> Result<Value, String> {
    if snapshot["generation"] != *generation || snapshot["state"] != "ready" {
        return Err("generation is not ready".into());
    }
    let request = snapshot["serverRequests"]
        .as_array()
        .into_iter()
        .flatten()
        .find(|r| r["generation"] == *generation && r["requestIdentity"] == *id)
        .ok_or("no-such-request")?;
    if request["state"] != "outstanding" {
        return Err(format!("request is {}", request["state"]));
    }
    if request["classification"] != "known-answerable" || request["originClass"] == "named-service"
    {
        return Err("not a person-answerable request".into());
    }
    let mut parameters = request["nativeParameters"].clone();
    if request["method"] == "mcpServer/elicitation/request" && answer["action"] == "accept" {
        match parameters["mode"].as_str() {
            Some("openai/userVerification") => return Err("device verification acceptance is not supported by this App path; no proof supplied".into()),
            Some("form" | "openai/form" | "openaiForm") => parameters["mode"] = json!("form"),
            Some("url") => {},
            _ => return Err("unsupported elicitation mode".into()),
        }
    }
    let mut check = RequestRegister::default();
    check.receive(
        generation,
        1,
        &json!({"id":id,"method":request["method"],"params":parameters}),
        &json!({}),
    )?;
    check.prepare(
        generation,
        id,
        answer,
        "person-via-interaction",
        Some(actor),
    )?;
    // Secret values are neither put in confirmation text nor returned to the UI.
    let mut preview = answer.clone();
    for question in request["nativeParameters"]["questions"]
        .as_array()
        .into_iter()
        .flatten()
    {
        if question["isSecret"] == true {
            if let Some(id) = question["id"].as_str() {
                if preview["answers"].get(id).is_some() {
                    preview["answers"][id] = json!({"answers":["[secret value masked]"]});
                }
            }
        }
    }
    if request["method"] == "mcpServer/elicitation/request"
        && preview["action"] == "accept"
        && !preview["content"].is_null()
    {
        preview["content"] = json!("[form content masked; supplied unchanged]");
    }
    Ok(
        json!({"method":request["method"],"generation":generation,"requestIdentity":id,"answer":preview,"actorRef":actor}),
    )
}

/// Reviewed App-owned ledger location; never derived from a supplier/project home.
pub fn reviewed_ledger_path(app_user_data: &std::path::Path) -> std::path::PathBuf {
    app_user_data.join("runtime").join("recovery.ledger.jsonl")
}

pub const INSTRUCTION_RELEASE: &str = "chirality-app-v4-unqualified-group-a-entry";
// Exact v4-owned defaults independently READY in V0-INSTRUCTION-TRANCHE.
pub const COMMON_DEFAULT: &[u8] = include_bytes!("../resources/instructions/AGENTS.md");
pub fn role_default(role: crate::role_supply::Role) -> &'static [u8] {
    use crate::role_supply::Role::*;
    match role {
        HELP_HUMAN => include_bytes!("../resources/instructions/agents/AGENT_HELP_HUMAN.md"),
        HELPS_HUMANS => include_bytes!("../resources/instructions/agents/AGENT_HELPS_HUMANS.md"),
        WORKING_ITEMS => include_bytes!("../resources/instructions/agents/AGENT_WORKING_ITEMS.md"),
        TASK => include_bytes!("../resources/instructions/agents/AGENT_TASK.md"),
    }
}
/// Create initial editable copies without overwriting any human edits.
/// Failure has no alternate storage location and is shown by the entry surface.
pub fn seed_instructions(root: &std::path::Path) -> Result<(), String> {
    use std::io::Write;
    if COMMON_DEFAULT.is_empty() {
        return Err("reviewed v4 product instruction basis not supplied".into());
    }
    let initial = match std::fs::symlink_metadata(root) {
        Ok(meta) if meta.file_type().is_symlink() => {
            return Err("instruction directory is a symbolic link".into())
        }
        Ok(_) => false,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => true,
        Err(e) => return Err(e.to_string()),
    };
    if !initial {
        // First seed is distinct from repairing a known existing user store.
        // Missing, unreadable, non-UTF8 or linked copies are errors, never fallback.
        crate::role_supply::Guidance::read_seeded(
            root,
            "AGENTS.md",
            INSTRUCTION_RELEASE,
            COMMON_DEFAULT,
        )?;
        for role in crate::role_supply::Role::ALL {
            crate::role_supply::Guidance::read_seeded(
                root,
                &format!("agents/AGENT_{}.md", role.name()),
                INSTRUCTION_RELEASE,
                role_default(role),
            )?;
        }
        return Ok(());
    }
    for directory in [root.to_path_buf(), root.join("agents")] {
        std::fs::create_dir_all(&directory).map_err(|e| e.to_string())?;
        if std::fs::symlink_metadata(&directory)
            .map_err(|e| e.to_string())?
            .file_type()
            .is_symlink()
        {
            return Err("instruction directory is a symbolic link".into());
        }
    }
    let defaults = std::iter::once(("AGENTS.md".into(), COMMON_DEFAULT)).chain(
        crate::role_supply::Role::ALL
            .into_iter()
            .map(|r| (format!("agents/AGENT_{}.md", r.name()), role_default(r))),
    );
    for (path, bytes) in defaults {
        match std::fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(root.join(path))
        {
            Ok(mut file) => {
                file.write_all(bytes)
                    .and_then(|_| file.sync_all())
                    .map_err(|e| e.to_string())?;
            }
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(e) => return Err(e.to_string()),
        }
    }
    Ok(())
}
pub fn compose_role(
    root: &std::path::Path,
    role: Option<crate::role_supply::Role>,
) -> Result<crate::role_supply::Composition, String> {
    use crate::role_supply::{Composition, Guidance};
    let common = Guidance::read_seeded(root, "AGENTS.md", INSTRUCTION_RELEASE, COMMON_DEFAULT)?;
    let active = role
        .map(|r| {
            Guidance::read_seeded(
                root,
                &format!("agents/AGENT_{}.md", r.name()),
                INSTRUCTION_RELEASE,
                role_default(r),
            )
        })
        .transpose()?;
    Composition::new(&common, role.zip(active.as_ref()), false)
}

/// Memory-only custody of documents picked through the native App boundary.
#[derive(Default)]
pub struct ExternalObservationSession {
    selection: Value,
    observation: Option<crate::external_observation::ExternalObservation>,
}
impl ExternalObservationSession {
    pub fn snapshot(&self) -> Value {
        json!({"selection":if self.selection.is_null(){json!({"state":"not-selected"})}else{self.selection.clone()},
            "observation":self.observation.as_ref().map(crate::external_observation::ExternalObservation::snapshot)})
    }
    fn begin(&mut self) -> Result<(), String> {
        if self.selection["state"] == "selecting" {
            return Err("External document selection is already in progress".into());
        }
        self.selection =
            json!({"state":"selecting","previousObservationRetained":self.observation.is_some()});
        Ok(())
    }
    fn finish_selection(&mut self, state: &str, stage: &str, reason: Option<&str>) -> Value {
        self.selection = json!({"state":state,"stage":stage,"reason":reason,"previousObservationRetained":self.observation.is_some()});
        self.snapshot()
    }
}

/// Production supplies the native picker; tests explicitly inject scratch selections.
/// Nothing here accepts a renderer path/origin, dispatches, or writes a document.
pub fn receive_external_selection(
    state: &std::sync::Mutex<ExternalObservationSession>,
    mut pick: impl FnMut(&str) -> Result<Option<std::path::PathBuf>, String>,
    include_counterpart: impl FnOnce() -> bool,
) -> Result<Value, String> {
    use crate::external_observation::{ExternalObservation, SelectedPaths};
    state.lock().unwrap().begin()?;
    let mut selected = Vec::new();
    for stage in ["catalog", "read"] {
        match pick(stage) {
            Ok(Some(path)) => selected.push(path),
            Ok(None) => {
                return Ok(state
                    .lock()
                    .unwrap()
                    .finish_selection("cancelled", stage, None))
            }
            Err(e) => {
                state
                    .lock()
                    .unwrap()
                    .finish_selection("selection-failed", stage, Some(&e));
                return Err(e);
            }
        }
    }
    let counterpart = if include_counterpart() {
        match pick("counterpart") {
            Ok(Some(path)) => Some(path),
            Ok(None) => {
                return Ok(state
                    .lock()
                    .unwrap()
                    .finish_selection("cancelled", "counterpart", None))
            }
            Err(e) => {
                state
                    .lock()
                    .unwrap()
                    .finish_selection("selection-failed", "counterpart", Some(&e));
                return Err(e);
            }
        }
    } else {
        None
    };
    let counterpart_selected = counterpart.is_some();
    let observation = ExternalObservation::load(SelectedPaths {
        catalog: selected.remove(0),
        read: selected.remove(0),
        counterpart,
    });
    let mut state = state.lock().unwrap();
    state.observation = Some(observation);
    state.selection = json!({"state":"loaded","counterpartSelection":if counterpart_selected{"selected"}else{"not-requested"},"source":"native-file-selection; person-supplied documents"});
    Ok(state.snapshot())
}

/// One App-session initialization attempt, separate from supplier lifecycle.
#[derive(Default)]
pub struct RecoveryStartup {
    attempted: bool,
    status: Value,
}
impl RecoveryStartup {
    /// Adopt the genuine shared App source, never reopen another writer/path or
    /// infer restored native state from pointer metadata.
    pub fn adopt_shared_source(&mut self, host: &crate::hosting::Host) -> Value {
        if !self.attempted {
            self.attempted = true;
            let observed = host.shared_recovery_observation();
            self.status = json!({"state":if observed["configured"]==true{"shared-source-configured"}else{"shared-source-unavailable"},"sourceObservation":observed,"blocksSupplierStart":false,"standing":"same actual App custody; no new ledger/session or cold live reconstruction"});
        }
        self.snapshot()
    }
    pub fn snapshot(&self) -> Value {
        if self.status.is_null() {
            json!({"state":"not-initialized","blocksSupplierStart":false})
        } else {
            self.status.clone()
        }
    }
    pub fn initialize(
        &mut self,
        host: &crate::hosting::Host,
        app_data: Result<&std::path::Path, &str>,
        codex_home: Option<&std::path::Path>,
    ) -> Value {
        self.initialize_inner(host, app_data, codex_home, Ok(None))
    }
    pub fn initialize_with_namespaces(
        &mut self,
        host: &crate::hosting::Host,
        app_data: Result<&std::path::Path, &str>,
        codex_home: Option<&std::path::Path>,
        namespaces: Result<
            std::sync::Arc<crate::hosting::attachment_custody::NativeNamespaceBindings>,
            String,
        >,
    ) -> Value {
        self.initialize_inner(host, app_data, codex_home, namespaces.map(Some))
    }
    fn initialize_inner(
        &mut self,
        host: &crate::hosting::Host,
        app_data: Result<&std::path::Path, &str>,
        codex_home: Option<&std::path::Path>,
        namespaces: Result<
            Option<std::sync::Arc<crate::hosting::attachment_custody::NativeNamespaceBindings>>,
            String,
        >,
    ) -> Value {
        if self.attempted {
            return self.snapshot();
        }
        self.attempted = true;
        let mut configured = false;
        let mut selected_path = None;
        let mut existing = false;
        let result = (|| -> Result<(), String> {
            let root = app_data.map_err(str::to_string)?;
            let binding = namespaces.as_ref().map_err(Clone::clone)?;
            let path = reviewed_ledger_path(root);
            selected_path = Some(path.clone());
            if let Some(binding) = binding {
                // On an initial physical refusal, use the genuine guarded Core
                // receiving API once. It retains the actual declared REC leaf
                // and original error before returning; no legacy open/retry or
                // replacement ledger follows from restoring metadata later.
                if binding
                    .guard_domains(&[path.clone()])
                    .and_then(|_| crate::recovery::RecoveryLedger::preflight_path(&path, binding))
                    .is_err()
                {
                    host.configure_recovery_with_namespaces(
                        path.clone(),
                        std::sync::Arc::clone(binding),
                    )?;
                    // A concurrent restoration may let Core's repeated current
                    // guard succeed. Its actual result owns that observation.
                    configured = true;
                }
            }
            if !root.is_absolute() {
                return Err(
                    "App user-data root is not absolute; ledger location not established".into(),
                );
            }
            if let Some(home) = codex_home {
                if !home.is_absolute() {
                    return Err(
                        "Cannot establish ledger separation from a relative Codex home".into(),
                    );
                }
                if resolved_location(&path)?.starts_with(resolved_location(home)?) {
                    return Err("App ledger location falls inside the configured Codex home; no alternate location selected".into());
                }
            }
            // Reject redirection of the App-owned root/runtime/file, preserving it.
            for target in [root.to_path_buf(), root.join("runtime"), path.clone()] {
                match std::fs::symlink_metadata(&target) {
                    Ok(meta) if meta.file_type().is_symlink() => {
                        return Err(format!(
                            "Ledger location is a symbolic link: {}",
                            target.display()
                        ))
                    }
                    Ok(_) if target == path => existing = true,
                    Ok(_) => {}
                    Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
                    Err(e) => return Err(e.to_string()),
                }
            }
            let directory = path
                .parent()
                .ok_or("Ledger parent unavailable")?
                .to_path_buf();
            let mut created = Vec::new();
            let mut cursor = directory.as_path();
            while !cursor.try_exists().map_err(|e| e.to_string())? {
                created.push(cursor.to_path_buf());
                cursor = cursor
                    .parent()
                    .ok_or("Ledger directory has no existing ancestor")?;
            }
            std::fs::create_dir_all(&directory).map_err(|e| e.to_string())?;
            if !configured {
                match binding {
                    Some(binding) => host
                        .configure_recovery_with_namespaces(path, std::sync::Arc::clone(binding))?,
                    None => host.configure_recovery(path)?,
                };
            }
            configured = true;
            // Core syncs appended file data. Publish the file and any new directory
            // entries before reporting initialization configured. No crash proof inferred.
            sync_directory(&directory)?;
            for made in created {
                if let Some(parent) = made.parent() {
                    sync_directory(parent)?;
                }
            }
            Ok(())
        })();
        let path = selected_path.as_ref().map(|p|json!({"displayPath":p.to_string_lossy(),
            "nativePath":{"encoding":"native_encoded_bytes","platform":std::env::consts::OS,"bytes":p.as_os_str().as_encoded_bytes()},
            "pathDisplayLimit":if p.to_str().is_some(){None}else{Some("native path is not Unicode; display is lossy")}}));
        let succeeded = result.is_ok();
        self.status = json!({"state":if succeeded{"configured"}else{"initialization-failed"},
            "hostConfigured":configured,"path":path,"historyFile":if existing{"existing"}else if configured{"new"}else{"not-established"},
            "configurationError":result.err(),"directoryPublication":if succeeded{"sync-calls-succeeded"}else{"not-confirmed"},
            "blocksSupplierStart":false,"standing":"App-observed recovery pointers; no native human-act proof"});
        self.snapshot()
    }
}
fn sync_directory(path: &std::path::Path) -> Result<(), String> {
    std::fs::File::open(path)
        .and_then(|f| f.sync_all())
        .map_err(|e| {
            format!(
                "Ledger directory publication not confirmed at {}: {e}",
                path.display()
            )
        })
}
fn resolved_location(path: &std::path::Path) -> Result<std::path::PathBuf, String> {
    let mut cursor = path.to_path_buf();
    let mut suffix = Vec::new();
    loop {
        match std::fs::canonicalize(&cursor) {
            Ok(mut found) => {
                for component in suffix.into_iter().rev() {
                    found.push(component);
                }
                return Ok(found);
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                suffix.push(
                    cursor
                        .file_name()
                        .ok_or("Cannot resolve ledger/home location")?
                        .to_os_string(),
                );
                if !cursor.pop() {
                    return Err("Cannot resolve ledger/home location".into());
                }
            }
            Err(e) => return Err(e.to_string()),
        }
    }
}
/// Shared by automatic and manual start: recording failure remains visible but
/// never prevents the supplier boundary from receiving or replying to requests.
pub fn start_with_recovery<T>(
    host: &crate::hosting::Host,
    startup: &std::sync::Mutex<RecoveryStartup>,
    app_data: Result<&std::path::Path, &str>,
    codex_home: Option<&std::path::Path>,
    start: impl FnOnce() -> Result<T, String>,
) -> Result<T, String> {
    startup
        .lock()
        .unwrap()
        .initialize(host, app_data, codex_home);
    start()
}

/// Plain conversation controls use only current native identities and supplied text.
fn current_conversation(
    snapshot: &Value,
    generation: &Value,
    thread_id: &str,
) -> Result<(), String> {
    crate::recovery::generation_ref(generation)?;
    if snapshot["state"] != "ready" || snapshot["generation"] != *generation {
        return Err("conversation selection is stale or host is not ready".into());
    }
    if !snapshot["threads"]
        .as_array()
        .into_iter()
        .flatten()
        .any(|t| {
            t["generation"] == *generation && t["threadId"] == thread_id && !thread_id.is_empty()
        })
    {
        return Err("conversation is not loaded in this home generation".into());
    }
    Ok(())
}
pub fn send_conversation_text(
    snapshot: &Value,
    generation: &Value,
    thread_id: &str,
    text: &str,
    send: impl FnOnce(&Value, &str, &str) -> Result<Value, String>,
) -> Result<Value, String> {
    current_conversation(snapshot, generation, thread_id)?;
    if text.is_empty() {
        return Err("text required".into());
    }
    // Do not trim, frame as workflow text, or add guidance/settings/actor fields.
    send(generation, thread_id, text)
}
pub fn interrupt_conversation_turn(
    snapshot: &Value,
    generation: &Value,
    thread_id: &str,
    turn_id: &str,
    interrupt: impl FnOnce(&Value, &str, &str) -> Result<Value, String>,
) -> Result<Value, String> {
    current_conversation(snapshot, generation, thread_id)?;
    if !snapshot["conversationTurns"]
        .as_array()
        .into_iter()
        .flatten()
        .any(|t| {
            t["generation"] == *generation
                && t["threadId"] == thread_id
                && t["turnId"] == turn_id
                && !turn_id.is_empty()
                && t["nativeTurn"]["status"] == "inProgress"
                && t["observationEnded"] != true
                && t["terminalEventObserved"] != true
        })
    {
        return Err("no live selected native turn".into());
    }
    let already = snapshot["turnInterruptRequests"]
        .as_array()
        .into_iter()
        .flatten()
        .any(|r| {
            r["binding"]["generation"] == *generation
                && r["binding"]["threadId"] == thread_id
                && r["binding"]["turnId"] == turn_id
                && (r["clientRequest"]["outcome"] == "response-observed-result"
                    || (r["clientRequest"]["outcome"] == "pending"
                        && r["clientRequest"]["writeResult"] == "written"))
        });
    if already {
        return Err("interrupt already requested; await native turn status".into());
    }
    // A returned acknowledgment changes no turn/item state and implies no rollback.
    interrupt(generation, thread_id, turn_id)
}

/// Disposable observed steering projection. Native receipt order/fresh response
/// boundaries avoid selecting an older active-looking memo. The actual scoped
/// Host remains authoritative at registration and response; this is no outcome.
pub fn observed_steering_target(
    snapshot: &Value,
    generation: &Value,
    thread_id: &str,
) -> Result<Value, String> {
    current_conversation(snapshot, generation, thread_id)?;
    let eligible = snapshot["conversationTurns"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|turn| {
            turn["generation"] == *generation
                && turn["threadId"] == thread_id
                && turn["turnId"].as_str().is_some_and(|id| !id.is_empty())
                && turn["nativeTurn"]["id"] == turn["turnId"]
                && turn["nativeTurn"]["status"] == "inProgress"
                && turn["terminalEventObserved"] != true
                && turn["observationEnded"] != true
        })
        .collect::<Vec<_>>();
    let latest = snapshot["journal"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|frame| {
            frame["generation"] == *generation
                && frame["frame"]["params"]["threadId"] == thread_id
                && matches!(
                    frame["frame"]["method"].as_str(),
                    Some("turn/started" | "turn/completed")
                )
                && frame["position"].as_u64().is_some()
        })
        .max_by_key(|frame| frame["position"].as_u64().unwrap());
    let boundary = latest.and_then(|frame| frame["position"].as_u64());
    let fresh = eligible
        .iter()
        .copied()
        .filter(|turn| {
            turn["source"] == "turn/start response"
                && boundary
                    .map(|position| {
                        turn["startResponseIssuedAfterReceipt"]
                            .as_u64()
                            .is_some_and(|issued| issued >= position)
                    })
                    .unwrap_or(true)
        })
        .collect::<Vec<_>>();
    let target = if fresh.len() == 1 {
        Some(fresh[0])
    } else if fresh.len() > 1 {
        None
    } else {
        latest
            .filter(|frame| {
                frame["frame"]["method"] == "turn/started"
                    && frame["frame"]["params"]["turn"]["status"] == "inProgress"
            })
            .and_then(|frame| {
                eligible
                    .iter()
                    .copied()
                    .find(|turn| turn["turnId"] == frame["frame"]["params"]["turn"]["id"])
            })
    }
    .ok_or(
        "current live steering target is unavailable or ambiguous; refresh native observations",
    )?;
    Ok(
        json!({"generation":generation,"threadId":thread_id,"turnId":target["turnId"],"source":target["source"],"receiptPosition":target["receiptPosition"],"standing":"current observed target; actual Host rechecks full source/generation/target at send and response; no lifecycle outcome inferred"}),
    )
}

/// Actual IPC consuming guard: unchanged plain text, one explicit expected native
/// turn, no fallback start or role/config/policy inputs and no automatic resend.
pub fn steer_conversation_turn(
    snapshot: &Value,
    generation: &Value,
    thread_id: &str,
    expected_turn: &str,
    text: &str,
    steer: impl FnOnce(&Value, &str, &str, &str) -> Result<Value, String>,
) -> Result<Value, String> {
    if text.is_empty() || expected_turn.is_empty() {
        return Err("steering requires text and the observed expected turn ID".into());
    }
    let current = observed_steering_target(snapshot, generation, thread_id)?;
    if current["turnId"] != expected_turn {
        return Err(
            "expected live steering turn changed; refresh and review the retained draft".into(),
        );
    }
    let response = steer(generation, thread_id, expected_turn, text)?;
    if response.get("error").is_some() {
        return Err(format!(
            "native steering error: {}; no successful steering inferred",
            response["error"]
        ));
    }
    if response["result"]["turnId"] != expected_turn {
        return Err("native steering response reports another turn; no target rebind or turn start inferred".into());
    }
    // This acknowledgment never changes turn/item state or implies replacement/end.
    Ok(response)
}
/// Memory-only selected native history and original App role evidence. A history
/// view is never an operational thread register or a trusted cold-replay source.
#[derive(Default)]
pub struct HistorySession {
    history: Option<crate::native_history::NativeHistory>,
    roles: crate::role_lifecycle::RoleBindings,
    limits: Vec<String>,
    dispatches: Vec<HistoryPending>,
    starts: Vec<StartPending>,
    closed_history_generations: Vec<Value>,
    list_direction: Option<String>,
    turn_direction: Option<String>,
    item_direction: Option<String>,
    item_turn: Option<String>,
}
struct HistoryPending {
    receipt: crate::hosting::HistoryDispatch,
    finished: bool,
    evidence: Value,
}
struct StartPending {
    receipt: crate::hosting::SourceRequest,
    prepared: Option<crate::role_lifecycle::PreparedStart>,
    finished: bool,
    evidence: Value,
}
impl HistorySession {
    pub fn synchronize(&mut self, host: &Value) {
        let generation = &host["generation"];
        if self
            .history
            .as_ref()
            .map(|h| h.generation() != generation || host["state"] != "ready")
            .unwrap_or(false)
        {
            if let Some(mut old) = self.history.take() {
                let old_generation = old.generation().clone();
                let _ = old.close_generation(&old_generation);
                if !self.closed_history_generations.contains(&old_generation) {
                    self.closed_history_generations.push(old_generation);
                }
            }
            self.limits.push("History receiving generation ended; pages discarded. Original role evidence is memory-only; cold replay is unknown.".into());
        }
        if host["state"] == "ready"
            && self.history.is_none()
            && !self.closed_history_generations.contains(generation)
        {
            if let Some(home) = generation["home"].as_str() {
                match crate::native_history::NativeHistory::new(home, generation.clone()) {
                    Ok(history) => self.history = Some(history),
                    Err(error) => self.limits.push(error),
                }
            }
        }
    }
    fn scoped(
        &mut self,
        host: &Value,
        generation: &Value,
        epoch: u64,
    ) -> Result<&mut crate::native_history::NativeHistory, String> {
        self.synchronize(host);
        if host["state"] != "ready" || &host["generation"] != generation {
            return Err("History action belongs to a non-ready or changed Host generation".into());
        }
        let history = self
            .history
            .as_mut()
            .ok_or("History receiving scope unavailable")?;
        if history.generation() != generation || history.selection_epoch() != epoch {
            return Err(
                "History generation or selected-thread epoch changed; refresh and select again"
                    .into(),
            );
        }
        Ok(history)
    }
    pub fn select(
        &mut self,
        host: &Value,
        generation: &Value,
        epoch: u64,
        thread: &str,
    ) -> Result<(), String> {
        self.scoped(host, generation, epoch)?.select(thread)?;
        self.turn_direction = None;
        self.item_direction = None;
        self.item_turn = None;
        Ok(())
    }
    pub fn prepare(
        &mut self,
        host: &Value,
        generation: &Value,
        epoch: u64,
        action: &str,
        cursor: Option<&str>,
        direction: crate::native_history::Direction,
        reference: Option<&str>,
    ) -> Result<crate::native_history::HistoryQuery, String> {
        let history = self.scoped(host, generation, epoch)?;
        match action {
            "list" => history.list_threads(cursor, direction),
            "metadata" => history.read_metadata(),
            "turns" => history.turns_page(cursor, direction),
            "items" => history.items_page(
                reference.ok_or("Select a received turn")?,
                cursor,
                direction,
            ),
            "goal" => history.read_goal(),
            "child" => history.read_child(reference.ok_or("Select a received child")?),
            "continue" => history.continue_query(),
            _ => Err("Unsupported history action".into()),
        }
    }
    pub fn dispatched(&mut self, receipt: crate::hosting::HistoryDispatch) {
        self.dispatches.push(HistoryPending {
            evidence: receipt_summary(&receipt.evidence()),
            receipt,
            finished: false,
        });
    }
    pub fn start_dispatched(
        &mut self,
        receipt: crate::hosting::SourceRequest,
        composition: &crate::role_supply::Composition,
        supply_ref: &str,
    ) -> Result<(), String> {
        let e = receipt.evidence();
        let prepared = (|| {
            crate::role_lifecycle::PreparedStart::new(
                e["home"].as_str().ok_or("start home absent")?,
                e["generation"].clone(),
                e["requestIdentity"].clone(),
                e["requestRef"]
                    .as_str()
                    .ok_or("start request reference absent")?,
                supply_ref,
                composition,
            )
        })();
        let error = prepared.as_ref().err().cloned();
        let mut summary = receipt_summary(&e);
        if let Some(error) = error.as_ref() {
            summary["rolePreparationError"] = json!(error);
        }
        // Registration already happened at Host. Keep its actual receipt even
        // when role preparation fails; neither no-send nor automatic retry follows.
        self.starts.push(StartPending {
            receipt,
            prepared: prepared.ok(),
            finished: false,
            evidence: summary,
        });
        match error {
            Some(error) => Err(error),
            None => Ok(()),
        }
    }

    /// Only private Host receipts select responses. Renderer JSON cannot supply
    /// receipt/source evidence or original role buffers. Waiting never resends.
    pub fn reconcile(&mut self, host: &crate::hosting::Host) {
        self.synchronize(&host.snapshot());
        for pending in &mut self.starts {
            if pending.finished {
                continue;
            }
            let status = match host.source_request_status(&pending.receipt) {
                Ok(status) => status,
                Err(error) => {
                    self.limits.push(error);
                    continue;
                }
            };
            let preparation_error = pending.evidence.get("rolePreparationError").cloned();
            pending.evidence = receipt_summary(&status);
            if let Some(error) = preparation_error {
                pending.evidence["rolePreparationError"] = error;
            }
            if status["sourceCurrent"] != true {
                pending.finished = true;
                continue;
            }
            if status["writeResult"] != "written" || status["response"].is_null() {
                continue;
            }
            pending.finished = true;
            if status["outcome"] != "response-observed-result" {
                continue;
            }
            let Some(prepared) = pending.prepared.take() else {
                continue;
            };
            match prepared.observe(
                &status["generation"],
                &status["sentFrame"],
                &status["response"],
            ) {
                Ok(binding) => match host.thread_start_dispatch_finish(&pending.receipt) {
                    Ok(_) => {
                        pending.evidence["activeAdmission"] = json!(true);
                        if let Err(error) = self.roles.insert(binding) {
                            self.limits.push(error);
                        }
                    }
                    Err(error) => self.limits.push(error),
                },
                Err(error) => self
                    .limits
                    .push(format!("Original role binding refused: {error}")),
            }
        }
        for pending in &mut self.dispatches {
            if pending.finished {
                continue;
            }
            let status = match host.history_dispatch_status(&pending.receipt) {
                Ok(status) => status,
                Err(error) => {
                    self.limits.push(error);
                    continue;
                }
            };
            pending.evidence = receipt_summary(&status);
            pending.evidence["localQuery"] = json!(pending.receipt.query());
            if status["sourceCurrent"] != true {
                pending.finished = true;
                continue;
            }
            let Some(history) = self.history.as_mut() else {
                continue;
            };
            if history.generation() != pending.receipt.query().generation() {
                pending.finished = true;
                continue;
            }
            if status["waitingEnded"] == true {
                let _ = history.waiting_ended(pending.receipt.query());
            }
            if status["writeResult"] != "written" || status["response"].is_null() {
                continue;
            }
            pending.finished = true;
            let result = if status["outcome"] == "response-observed-result" {
                history.receive(
                    pending.receipt.query(),
                    status["home"].as_str().unwrap_or(""),
                    &status["generation"],
                    &status["response"]["result"],
                )
            } else {
                history.receive_error(
                    pending.receipt.query(),
                    status["home"].as_str().unwrap_or(""),
                    &status["generation"],
                    &status["response"]["error"],
                )
            };
            if let Err(error) = result {
                self.limits
                    .push(format!("History receiving refused: {error}"));
                continue;
            }
            if status["outcome"] == "response-observed-result" {
                let params = pending.receipt.query().params();
                let direction = params["sortDirection"].as_str().map(str::to_owned);
                match pending.receipt.query().method() {
                    "thread/list" => self.list_direction = direction,
                    "thread/turns/list" => self.turn_direction = direction,
                    "thread/items/list" => {
                        self.item_direction = direction;
                        self.item_turn = params["turnId"].as_str().map(str::to_owned);
                    }
                    _ => (),
                }
            }
            if pending.receipt.query().method() == "thread/resume"
                && status["outcome"] == "response-observed-result"
            {
                // Known original bindings are checked against this exact metadata-only
                // resume; an absent binding stays Unknown and does not prevent native use.
                if let Some(thread) = history.selected_thread() {
                    if let Some(binding) = self.roles.get(history.home(), thread) {
                        let observed = binding
                            .resume(
                                history.home(),
                                status["generation"].clone(),
                                status["requestIdentity"].clone(),
                                status["requestRef"].as_str().unwrap_or(""),
                            )
                            .and_then(|request| {
                                request.observe(
                                    &status["generation"],
                                    &status["sentFrame"],
                                    &status["response"],
                                )
                            });
                        if let Err(error) = observed {
                            self.limits
                                .push(format!("Original resume role evidence refused: {error}"));
                            continue;
                        }
                    }
                }
                match host.history_admit_resume(history, &pending.receipt) {
                    Ok(admission) => pending.evidence["activeAdmission"] = admission,
                    Err(error) => self
                        .limits
                        .push(format!("Continue active admission refused: {error}")),
                }
            }
        }
    }
    pub fn start_admitted(&self, receipt: &crate::hosting::SourceRequest) -> bool {
        self.starts.iter().any(|p| {
            p.receipt.request_ref() == receipt.request_ref()
                && p.evidence["activeAdmission"] == true
        })
    }
    pub fn history(&self) -> Option<&crate::native_history::NativeHistory> {
        self.history.as_ref()
    }
    pub fn history_mut(&mut self) -> Option<&mut crate::native_history::NativeHistory> {
        self.history.as_mut()
    }
    pub fn bind(&mut self, binding: crate::role_lifecycle::RoleBinding) -> Result<(), String> {
        self.roles.insert(binding)
    }
    pub fn role(&self, home: &str, thread: &str) -> Value {
        json!(self.roles.selected_role(home, thread))
    }
    pub fn binding(&self, home: &str, thread: &str) -> Option<&crate::role_lifecycle::RoleBinding> {
        self.roles.get(home, thread)
    }
    pub fn role_details(&self, home: &str, thread: &str, root: Option<&std::path::Path>) -> Value {
        let Some(binding) = self.binding(home, thread) else {
            return json!({"appRole":self.role(home,thread),"futureGuidanceNotices":[]});
        };
        let mut current = std::collections::BTreeMap::new();
        let read = |path: &str, default| match root {
            Some(root) => {
                crate::role_supply::Guidance::read_seeded(root, path, INSTRUCTION_RELEASE, default)
                    .map(|g| g.bytes().to_vec())
            }
            None => Err("App instruction root unavailable; current guidance not read".into()),
        };
        current.insert("AGENTS.md".into(), read("AGENTS.md", COMMON_DEFAULT));
        for role in crate::role_supply::Role::ALL {
            current.insert(
                format!("agents/AGENT_{}.md", role.name()),
                read(
                    &format!("agents/AGENT_{}.md", role.name()),
                    role_default(role),
                ),
            );
        }
        json!({"appRole":self.role(home,thread),"originalRoleSupply":binding.evidence(),"futureGuidanceNotices":binding.changes(&current)})
    }
    pub fn snapshot(&self, instruction_root: Option<&std::path::Path>) -> Value {
        let Some(history) = self.history.as_ref() else {
            return json!({"state":"unavailable","limits":self.limits,"durableNativeData":false});
        };
        let mut view = history.snapshot();
        view["selectionEpoch"] = json!(history.selection_epoch());
        view["listDirection"] = json!(self.list_direction);
        view["receivingLimits"] = json!(self.limits);
        view["dispatches"] = json!(self
            .dispatches
            .iter()
            .map(|p| &p.evidence)
            .collect::<Vec<_>>());
        view["startReceipts"] = json!(self.starts.iter().map(|p| &p.evidence).collect::<Vec<_>>());
        for row in view["threads"].as_array_mut().into_iter().flatten() {
            if let Some(thread) = row["native"]["id"].as_str() {
                row["appRole"] = self.role(history.home(), thread);
            }
        }
        if let Some(thread) = history.selected_thread() {
            view["selected"]["turnDirection"] = json!(self.turn_direction);
            view["selected"]["itemDirection"] = json!(self.item_direction);
            view["selected"]["itemTurnId"] = json!(self.item_turn);
            view["selected"]["appRole"] = self.role(history.home(), thread);
            let details = self.role_details(history.home(), thread, instruction_root);
            view["selected"]["originalRoleSupply"] = details["originalRoleSupply"].clone();
            view["selected"]["futureGuidanceNotices"] = details["futureGuidanceNotices"].clone();
        }
        view
    }
}

fn receipt_summary(e: &Value) -> Value {
    json!({"generation":e["generation"],"home":e["home"],"requestIdentity":e["requestIdentity"],"requestRef":e["requestRef"],"writeResult":e["writeResult"],"outcome":e["outcome"],"waitingEnded":e["waitingEnded"],"sourceCurrent":e["sourceCurrent"],"writeError":e["writeError"]})
}

/// Complete every claimed start once. Local receiving errors remain distinct
/// from the already-sent native operation, whose receipt is retained separately.
pub fn finalize_start_attempt(
    selection: &mut crate::access::ConversationSelection,
    attempt_id: &str,
    generation: &Value,
    current_generation: &Value,
    result: Result<Value, String>,
) -> Result<Value, String> {
    if selection.snapshot()["conversation"] != attempt_id
        || selection.owning_generation() != Some(generation)
    {
        return Err("Start claim was replaced; newer operation state preserved, original native receipt retained".into());
    }
    let result = result.and_then(|response| {
        if generation != current_generation { return Err("unknown: owning generation changed during thread start; native receipt retained".into()); }
        if response.get("error").is_some() { return Err(format!("Native start error observed: {}; no successful start inferred", response["error"])); }
        selection.started(generation, &response["result"])
            .map_err(|error| format!("Start response could not be received: {error}; native effect remains as observed in retained receipt"))?;
        Ok(response)
    });
    if let Err(error) = result.as_ref() {
        if selection.snapshot()["state"] == "starting" {
            selection.start_failed(error)?;
        }
    }
    result
}

/// Publish a prepared start only after fallible no-effect preparation succeeds.
/// An error preserves the previous selection and its truthful state.
pub fn claim_start(
    slot: &mut Option<crate::access::ConversationSelection>,
    selection: crate::access::ConversationSelection,
    prepare_supply_ref: impl FnOnce() -> Result<String, String>,
) -> Result<String, String> {
    if slot
        .as_ref()
        .is_some_and(|previous| previous.snapshot()["state"] == "starting")
    {
        return Err("thread start in progress".into());
    }
    let supply_ref = prepare_supply_ref()?;
    *slot = Some(selection);
    Ok(supply_ref)
}

/// Public decision-view command's receiving path. No writer/control is available
/// to this function: reading cannot append, replay captures or repair backlinks.
pub fn read_decision_packages(workspace: &std::path::Path) -> Value {
    let mut view = crate::decision_view::derive(workspace, &[]);
    view["workspace"] = json!(workspace.display().to_string());
    view["readOnly"] = json!(true);
    view
}

/// Separately invoked writer responsibility, preserving native pending-before-
/// ordinary-recorder ordering. Reading a view never invokes this continuation.
pub fn continue_decision_writer(
    workspace: &std::path::Path,
    control: Option<&mut crate::act_control::ActControl>,
    trigger: &str,
) -> Value {
    let mut status = json!({"responsibility":"decision record writer continuation","trigger":trigger,"workspace":workspace.display().to_string(),"state":"writer-continuation","requestsRecordedNow":0,"captureRecovery":[],"limits":[]});
    let Some(control) = control else {
        status["state"] = json!("unavailable");
        status["limits"] = json!(["native writer state unavailable; recorder continuation held"]);
        return status;
    };
    let (recovery, requests) = control.refresh_recording();
    match recovery {
        Ok(results) => status["captureRecovery"] = json!(results),
        Err(error) => status["limits"].as_array_mut().unwrap().push(json!(format!(
            "Capture recovery unavailable: {error}; pending capture status not established by this attempt"
        ))),
    }
    match requests {
        Ok(requests) => status["requestsRecordedNow"] = json!(requests.len()),
        Err(error) => status["limits"].as_array_mut().unwrap().push(json!(error)),
    }
    status
}

/// Independent selected-source trace imports. No App/current supplier context
/// enters the receiver or becomes a candidate/date/build default.
#[derive(Default)]
pub struct TraceSelectionSession {
    receiving: crate::trace_receiving::TraceReceivingSession,
    selection: Value,
}
impl TraceSelectionSession {
    pub fn snapshot(&self) -> Value {
        json!({"selection":if self.selection.is_null(){json!({"state":"not-selected"})}else{self.selection.clone()},"receiving":self.receiving.snapshot()})
    }
    fn begin(&mut self, record: &str, evidence: &str) -> Result<(), String> {
        if self.selection["state"] == "selecting" {
            return Err("Trace selection already in progress".into());
        }
        self.selection = json!({"state":"selecting","recordKind":record,"declaredEvidenceCategory":evidence,"previousImportsRetained":true});
        Ok(())
    }
    fn finish(&mut self, state: &str, reason: Option<&str>) -> Value {
        self.selection["state"] = json!(state);
        self.selection["reason"] = json!(reason);
        self.snapshot()
    }
}

/// Actual command helper: one native-selection callback and one opened regular
/// source read. Renderer cannot supply path/buffer/candidate identity or date.
pub fn select_trace_source(
    state: &std::sync::Mutex<TraceSelectionSession>,
    record: &str,
    evidence: &str,
    pick: impl FnOnce() -> Result<Option<std::path::PathBuf>, String>,
) -> Result<Value, String> {
    use crate::external_trace::{EvidenceKind, RecordKind};
    let kind = match record {
        "exam_result" => RecordKind::ExaminationResult,
        "xt_result" => RecordKind::XtResult,
        "xt_work" => RecordKind::XtWork,
        _ => return Err("Unsupported trace record kind".into()),
    };
    let tier = match evidence {
        "own_code" => EvidenceKind::OwnCode,
        "native_supplier" => EvidenceKind::NativeSupplier,
        "actual_host" => EvidenceKind::ActualHost,
        "extension" => EvidenceKind::Extension,
        "definition_or_rehearsal" => EvidenceKind::DefinitionOrRehearsal,
        _ => return Err("Unsupported declared trace evidence category".into()),
    };
    state.lock().unwrap().begin(record, evidence)?;
    let path = match pick() {
        Ok(Some(path)) => path,
        Ok(None) => return Ok(state.lock().unwrap().finish("cancelled", None)),
        Err(error) => {
            state
                .lock()
                .unwrap()
                .finish("selection-failed", Some(&error));
            return Err(error);
        }
    };
    // No metadata pre-read, alternative origin or filename reopen; the reviewed
    // receiver owns the actual descriptor/buffer/hash/shape/semantic custody.
    let source = crate::trace_receiving::ActualSelectedSource::read(path);
    let mut session = state.lock().unwrap();
    let index = session
        .receiving
        .receive_selected_source(source, kind, tier);
    session.selection["importIndex"] = json!(index);
    session.selection["mechanism"] =
        json!("native-file-selection; source claims remain unverified");
    Ok(session.finish("source-received", None))
}

/// Native-picked private handles, ordered independently of conversation/home/cwd.
/// Launch workspace is a source observation, not a fabricated REC project/index.
pub struct AttachmentSelectionSession {
    owner: String,
    revision: u64,
    launch_workspace: Option<std::path::PathBuf>,
    slots: Vec<AttachmentSelectionSlot>,
    operation: Value,
    submissions: Vec<AttachmentSubmissionState>,
}
struct AttachmentSubmissionState {
    prepared: std::sync::Arc<crate::hosting::PreparedAttachmentDispatch>,
    context: crate::recovery::ExplicitAppProjectContext,
    context_binding: Value,
    outcome: Value,
}
struct AttachmentSelectionSlot {
    selected: crate::attachments::SelectedTextAttachment,
    native_path: std::path::PathBuf,
}
impl AttachmentSelectionSession {
    pub fn new(launch_workspace: Option<std::path::PathBuf>) -> Result<Self, String> {
        Ok(Self {
            owner: crate::util::opaque_id("attachment-owner:")?,
            revision: 0,
            launch_workspace,
            slots: vec![],
            operation: json!({"state":"not-selected"}),
            submissions: vec![],
        })
    }
    pub fn refresh_submissions(
        &mut self,
        host: &crate::hosting::Host,
        custody: &std::sync::Arc<crate::hosting::attachment_custody::AttachmentCustody>,
    ) {
        for submission in &mut self.submissions {
            let source = submission.prepared.source().generation();
            let current = host.snapshot()["generation"].clone();
            if source["home"] != current["home"] || source["appSession"] != current["appSession"] {
                continue;
            }
            submission.outcome["resolution"] =
                host.resolve_attachment_submission(custody, submission.prepared.submission_ref());
        }
    }
    pub fn snapshot(&self) -> Value {
        json!({"ownerRef":self.owner,"listRevision":self.revision,
            "selections":self.slots.iter().enumerate().map(|(position,slot)|json!({"position":position,"selection":slot.selected.snapshot()})).collect::<Vec<_>>(),
            "operation":self.operation,"submissions":self.submissions.iter().map(|submission|json!({"submissionRef":submission.prepared.submission_ref(),"state":submission.prepared.state(),"frozenAppContext":submission.context.view(),"contextBinding":submission.context_binding,"outcome":submission.outcome,"limits":"private hot capability; no imported source or provider adoption"})).collect::<Vec<_>>(),"launchAppProjectObservation":{"source":"explicit App launch CHIRALITY_WORKSPACE","nativeRoot":self.launch_workspace.as_ref().map(|path|crate::attachments::native_path_identity(path)),
                "associationStanding":"launch source only; no accepted REC context/persistent thread-project binding established by this picker"},
            "workflowRun":"not supplied; WR prefix/draft association is a separate producer join",
            "submissionStanding":"private source handles; each immutable submission has its own source outcome below","custody":"private App memory; DTO/path/hash cannot construct a selection"})
    }
    fn check(&self, owner: &str, revision: u64) -> Result<(), String> {
        if owner != self.owner || revision != self.revision {
            return Err("Attachment owner/list revision changed; refresh selected sources".into());
        }
        if matches!(
            self.operation["state"].as_str(),
            Some("selecting" | "reconfirming")
        ) {
            return Err("Native attachment operation already in progress".into());
        }
        Ok(())
    }
    fn cancel_unsent(&self) {
        for submission in &self.submissions {
            let _ = submission.prepared.cancel();
        }
    }
    fn next_revision(&self) -> Result<u64, String> {
        self.revision
            .checked_add(1)
            .ok_or("Attachment list revision exhausted".into())
    }
    pub fn remove(&mut self, owner: &str, revision: u64, reference: &str) -> Result<Value, String> {
        self.check(owner, revision)?;
        let position = self
            .slots
            .iter()
            .position(|slot| slot.selected.selection_ref() == reference)
            .ok_or("Unknown private attachment handle")?;
        let next = self.next_revision()?;
        self.cancel_unsent();
        self.slots.remove(position);
        self.revision = next;
        self.operation = json!({"state":"removed","selectionRef":reference});
        Ok(self.snapshot())
    }
    pub fn reorder(
        &mut self,
        owner: &str,
        revision: u64,
        order: &[String],
    ) -> Result<Value, String> {
        self.check(owner, revision)?;
        let known = self
            .slots
            .iter()
            .map(|slot| slot.selected.selection_ref().to_owned())
            .collect::<std::collections::HashSet<_>>();
        let proposed = order
            .iter()
            .cloned()
            .collect::<std::collections::HashSet<_>>();
        if order.len() != self.slots.len() || proposed.len() != order.len() || known != proposed {
            return Err("Reorder must name every known private attachment exactly once; no subset/foreign/duplicate handles".into());
        }
        let next = self.next_revision()?;
        self.cancel_unsent();
        let mut old = std::mem::take(&mut self.slots);
        self.slots = order
            .iter()
            .map(|reference| {
                let position = old
                    .iter()
                    .position(|slot| slot.selected.selection_ref() == reference)
                    .unwrap();
                old.remove(position)
            })
            .collect();
        self.revision = next;
        self.operation = json!({"state":"reordered"});
        Ok(self.snapshot())
    }
    /// References alone cannot create selected bodies. All-or-nothing producer
    /// preparation uses the actual retained native sources and selection order.
    pub fn prepare_selected(
        &self,
        owner: &str,
        revision: u64,
        order: &[String],
        submission: &str,
        recorded_at: &str,
    ) -> Result<crate::attachments::PreparedAttachmentList, String> {
        self.check(owner, revision)?;
        let current = self
            .slots
            .iter()
            .map(|slot| slot.selected.selection_ref().to_owned())
            .collect::<Vec<_>>();
        if current != order {
            return Err("Attachment submission must use the entire current private list in its current order".into());
        }
        let selected = self
            .slots
            .iter()
            .map(|slot| slot.selected.clone())
            .collect::<Vec<_>>();
        crate::attachments::prepare_ordered(&selected, submission, recorded_at)
            .map_err(|hold| hold.message)
    }
    fn finish_hold(&mut self, hold: &crate::attachments::AttachmentHold) -> Value {
        self.operation = json!({"state":"held","reason":format!("{:?}",hold.reason),"message":hold.message,"nativePath":hold.native_path,"displayPath":hold.display_path,"priorSelectionsRetained":true});
        self.snapshot()
    }
}

/// Native selection only; no JS path, text, selected-body or draft/source DTO.
pub fn select_attachment_source(
    state: &std::sync::Mutex<Result<AttachmentSelectionSession, String>>,
    owner: &str,
    revision: u64,
    pick: impl FnOnce() -> Result<Option<std::path::PathBuf>, String>,
) -> Result<Value, String> {
    {
        let mut state = state.lock().unwrap();
        let session = state.as_mut().map_err(|error| error.clone())?;
        session.check(owner, revision)?;
        session.operation = json!({"state":"selecting"});
    }
    let path = match pick() {
        Ok(Some(path)) => path,
        Ok(None) => {
            let mut state = state.lock().unwrap();
            let session = state.as_mut().map_err(|error| error.clone())?;
            session.operation = json!({"state":"cancelled","priorSelectionsRetained":true});
            return Ok(session.snapshot());
        }
        Err(error) => {
            if let Ok(session) = state.lock().unwrap().as_mut() {
                session.operation = json!({"state":"selection-failed","message":error,"priorSelectionsRetained":true});
            }
            return Err(error);
        }
    };
    let selected =
        crate::attachments::SelectedTextAttachment::from_native_selection(path.clone(), None);
    let mut state = state.lock().unwrap();
    let session = state.as_mut().map_err(|error| error.clone())?;
    if session.owner != owner
        || session.revision != revision
        || session.operation["state"] != "selecting"
    {
        return Err(
            "Attachment owner/list changed during native selection; newer state preserved".into(),
        );
    }
    match selected {
        Ok(selected) => {
            let next = match session.next_revision() {
                Ok(next) => next,
                Err(error) => {
                    session.operation = json!({"state":"held","message":error});
                    return Err(error);
                }
            };
            let reference = selected.selection_ref().to_owned();
            session.cancel_unsent();
            session.slots.push(AttachmentSelectionSlot {
                selected,
                native_path: path,
            });
            session.revision = next;
            session.operation = json!({"state":"selected-not-sent","selectionRef":reference});
            Ok(session.snapshot())
        }
        Err(hold) => Ok(session.finish_hold(&hold)),
    }
}

/// Explicit normal-input source confirmation. Tentative identity is read from
/// the private original PathBuf; cancellation never installs a new observation.
pub fn reconfirm_attachment_source(
    state: &std::sync::Mutex<Result<AttachmentSelectionSession, String>>,
    owner: &str,
    revision: u64,
    reference: &str,
    confirm: impl FnOnce(&Value) -> bool,
) -> Result<Value, String> {
    let (path, old) = {
        let mut state = state.lock().unwrap();
        let session = state.as_mut().map_err(|error| error.clone())?;
        session.check(owner, revision)?;
        let slot = session
            .slots
            .iter()
            .find(|slot| slot.selected.selection_ref() == reference)
            .ok_or("Unknown private attachment handle")?;
        let values = (slot.native_path.clone(), slot.selected.snapshot());
        session.operation = json!({"state":"reconfirming","selectionRef":reference});
        values
    };
    let tentative =
        match crate::attachments::SelectedTextAttachment::from_native_selection(path, None) {
            Ok(selected) => selected,
            Err(hold) => {
                let mut state = state.lock().unwrap();
                return Ok(state
                    .as_mut()
                    .map_err(|error| error.clone())?
                    .finish_hold(&hold));
            }
        };
    let comparison = json!({"oldSelection":old,"tentativeSelection":tentative.snapshot(),"standing":"explicit normal-input source refresh; no send/native act/workflow registration or run"});
    let accepted = confirm(&comparison);
    let mut state = state.lock().unwrap();
    let session = state.as_mut().map_err(|error| error.clone())?;
    if !accepted {
        session.operation =
            json!({"state":"confirmation-cancelled","priorSelectionsRetained":true});
        return Ok(session.snapshot());
    }
    if session.owner != owner || session.revision != revision {
        return Err(
            "Attachment owner/list changed during confirmation; newer selection state preserved"
                .into(),
        );
    }
    let next = match session.next_revision() {
        Ok(next) => next,
        Err(error) => {
            session.operation = json!({"state":"held","message":error});
            return Err(error);
        }
    };
    session.cancel_unsent();
    let slot = session
        .slots
        .iter_mut()
        .find(|slot| slot.selected.selection_ref() == reference)
        .ok_or("Original attachment handle no longer available")?;
    let replacement = tentative.selection_ref().to_owned();
    slot.selected = tentative;
    session.revision = next;
    session.operation = json!({"state":"explicit-source-confirmed-not-sent","oldSelectionRef":reference,"selectionRef":replacement,"sourceRecheck":"required again at actual submission; no automatic drift replacement"});
    Ok(session.snapshot())
}

/// Caller-owned explicit launch/open directory, never native cwd/home/projectId.
/// Native tagging supplies a lossless reference when no Unicode path exists;
/// this is a directory reference, not a content hash/acceptance algorithm.
pub fn freeze_configured_project(
    workspace: Option<&std::path::Path>,
) -> Result<crate::recovery::ExplicitAppProjectContext, String> {
    match workspace {
        Some(path) => {
            let reference = path
                .to_str()
                .map(str::to_owned)
                .unwrap_or_else(|| crate::attachments::native_path_identity(path).to_string());
            crate::recovery::ExplicitAppProjectContext::known(
                &reference,
                crate::recovery::AppProjectSource::ConfiguredDirectory,
            )
        }
        None => Ok(crate::recovery::ExplicitAppProjectContext::unknown()),
    }
}

/// One-shot actual private list→durable Core preparation→owning context binding→
/// scoped native dispatch. An error never retries or falls back to person-only.
pub fn submit_selected_attachments(
    state: &std::sync::Mutex<Result<AttachmentSelectionSession, String>>,
    host: &crate::hosting::Host,
    custody: std::sync::Arc<crate::hosting::attachment_custody::AttachmentCustody>,
    owner: &str,
    revision: u64,
    order: &[String],
    generation: &Value,
    thread: &str,
    expected_turn: Option<&str>,
    text: &str,
    context: crate::recovery::ExplicitAppProjectContext,
    home: Option<&str>,
) -> Result<Value, String> {
    let selected = {
        let state = state.lock().unwrap();
        let session = state.as_ref().map_err(|error| error.clone())?;
        session.check(owner, revision)?;
        let known = session
            .slots
            .iter()
            .map(|slot| slot.selected.selection_ref().to_owned())
            .collect::<Vec<_>>();
        if known != order || known.is_empty() {
            return Err("Attachment-bearing submission requires the entire nonempty private list in current order".into());
        }
        session
            .slots
            .iter()
            .map(|slot| slot.selected.clone())
            .collect::<Vec<_>>()
    };
    current_conversation(&host.snapshot(), generation, thread)?;
    if let Some(expected) = expected_turn {
        if observed_steering_target(&host.snapshot(), generation, thread)?["turnId"] != expected {
            return Err("Expected live attachment steering target changed".into());
        }
    }
    let prepared = std::sync::Arc::new(host.prepare_attachment_turn(
        custody.clone(),
        generation,
        thread,
        expected_turn,
        text,
        &selected,
    )?);
    {
        let mut state = state.lock().unwrap();
        let session = state.as_mut().map_err(|error| error.clone())?;
        if session.owner != owner || session.revision != revision {
            let _ = prepared.cancel();
            return Err("Attachment list changed during preparation; actual unsent packet cancelled, original evidence retained".into());
        }
        session.submissions.push(AttachmentSubmissionState {
            prepared: prepared.clone(),
            context: context.clone(),
            context_binding: Value::Null,
            outcome: json!({"state":"prepared; not sent"}),
        });
    }
    let binding = match host.bind_attachment_context(&prepared, &context, home) {
        Ok(binding) => binding,
        Err(error) => {
            let _ = prepared.cancel();
            let mut state = state.lock().unwrap();
            if let Ok(session) = state.as_mut() {
                if let Some(submission) = session.submissions.iter_mut().find(|submission| {
                    submission.prepared.submission_ref() == prepared.submission_ref()
                }) {
                    submission.outcome =
                        json!({"state":"context held; nothing sent","error":error});
                }
            }
            return Err(error);
        }
    };
    {
        let mut state = state.lock().unwrap();
        if let Ok(session) = state.as_mut() {
            if let Some(submission) = session.submissions.iter_mut().find(|submission| {
                submission.prepared.submission_ref() == prepared.submission_ref()
            }) {
                submission.context_binding = binding;
            }
        }
    }
    let result = host
        .dispatch_attachment_turn(&prepared)
        .and_then(|source| host.attachment_wait(&source, std::time::Duration::from_secs(20)));
    let resolved = host.resolve_attachment_submission(&custody, prepared.submission_ref());
    {
        let mut state = state.lock().unwrap();
        if let Ok(session) = state.as_mut() {
            if let Some(submission) = session.submissions.iter_mut().find(|submission| {
                submission.prepared.submission_ref() == prepared.submission_ref()
            }) {
                submission.outcome = json!({"resolution":resolved,"result":match &result {Ok(evidence)=>evidence["outcome"].as_str().unwrap_or("source facts unresolved"),Err(_)=>"failed/unknown; no resend"},"error":result.as_ref().err()});
            }
        }
    }
    result?;
    current_conversation(&host.snapshot(), generation, thread)?;
    if let Some(expected) = expected_turn {
        if observed_steering_target(&host.snapshot(), generation, thread)?["turnId"] != expected {
            return Err("Attachment steering target changed after native reply; original submission evidence retained".into());
        }
    }
    if resolved["nativeTurnRef"].is_null() || resolved["sourceWriteConfirmed"] != true {
        return Err("Attachment submission not currently acknowledged by a matching native source; outcome retained, no automatic resend".into());
    }
    Ok(resolved)
}

/// Explicit Root-supplied receiving set. Paths retain native bytes; this object
/// is not a registry, credential authority or native discovery witness.
pub struct HomeBootstrapSet {
    account: crate::home_resources::ExistingHomeReference,
    key: Option<crate::home_resources::OwnedHomePlan>,
    probe: crate::home_resources::ExistingHomeReference,
    shared_root_targets: Option<crate::home_resources::SharedResourceTargets>,
}
impl HomeBootstrapSet {
    pub fn new(
        account: crate::home_resources::ExistingHomeReference,
        key: Option<crate::home_resources::OwnedHomePlan>,
        probe: crate::home_resources::ExistingHomeReference,
    ) -> Result<Self, String> {
        use crate::home_resources::HomeClass;
        if account.class() != HomeClass::Account
            || key
                .as_ref()
                .is_some_and(|key| key.class() != HomeClass::ApiKey)
            || probe.class() != HomeClass::Probe
        {
            return Err("Incorrect explicit home mode classes".into());
        }
        let set = Self {
            account,
            key,
            probe,
            shared_root_targets: None,
        };
        set.revalidate()?;
        Ok(set)
    }
    pub fn revalidate(&self) -> Result<(), String> {
        use crate::home_resources::HomeBinding;
        let mut bindings = vec![
            HomeBinding::Existing(&self.account),
            HomeBinding::Existing(&self.probe),
        ];
        if let Some(key) = &self.key {
            bindings.push(HomeBinding::Owned(key));
        }
        crate::home_resources::validate_home_bindings(&bindings)
    }
    pub fn native_namespaces(
        &self,
        include_key: bool,
    ) -> Result<std::sync::Arc<crate::hosting::attachment_custody::NativeNamespaceBindings>, String>
    {
        use crate::hosting::attachment_custody::{NativeHomeNamespace, NativeNamespaceBindings};
        // Received direct/absent slots can close themselves without asserting
        // M-A setup. Only a foreign-link closure needs the supplied references.
        let build = |targets: Option<&crate::home_resources::SharedResourceTargets>| {
            let mut homes = vec![
                NativeHomeNamespace::received(&self.account, targets),
                NativeHomeNamespace::received(&self.probe, None),
            ];
            if include_key {
                homes.push(NativeHomeNamespace::planned(self.key_plan()?));
            }
            NativeNamespaceBindings::from_root(homes)
        };
        match build(None) {
            Ok(binding) => Ok(binding),
            Err(original) => match self.shared_root_targets.as_ref() {
                Some(targets) => build(Some(targets)),
                None => Err(original),
            },
        }
    }
    pub fn key_plan(&self) -> Result<&crate::home_resources::OwnedHomePlan, String> {
        self.key.as_ref().ok_or_else(|| {
            "Key home/resource descriptors not explicitly configured; no account fallback".into()
        })
    }
    pub fn prepare_key(&self) -> Result<Value, String> {
        self.revalidate()?;
        let prepared = self.key_plan()?.prepare();
        self.revalidate()?;
        prepared.map(|observation| home_resource_view(&observation))
    }
    pub fn inspect(&self) -> Value {
        let mut rows = vec![];
        for reference in [&self.account, &self.probe] {
            rows.push(match reference.inspect() {
                Ok(observation) => home_resource_view(&observation),
                Err(error) => json!({"modeHomeClass":reference.class().as_str(),"limit":error}),
            });
        }
        rows.push(match self.key_plan().and_then(|key| key.inspect()) {
            Ok(observation) => home_resource_view(&observation),
            Err(error) => json!({"modeHomeClass":"api-key","limit":error}),
        });
        json!({"homes":rows,"keyConfigured":self.key.is_some(),"wholeSetLimit":self.revalidate().err(),"existingAccountResources":"setup/link ownership not established by existing reference; no legacy startup veto","standing":"current physical source/resource observations only; no credential or native discovery qualification"})
    }
    pub fn validate_binding(
        &self,
        class: crate::home_resources::HomeClass,
        config: &crate::hosting::HostConfig,
    ) -> Result<(), String> {
        // A prospective key is not an authority over the existing account.
        // Current account/probe source checks remain required; key admission
        // validates the complete set before and after its own setup.
        if class == crate::home_resources::HomeClass::Account {
            crate::home_resources::validate_home_bindings(&[
                crate::home_resources::HomeBinding::Existing(&self.account),
                crate::home_resources::HomeBinding::Existing(&self.probe),
            ])?;
        } else {
            self.revalidate()?;
        }
        let path = match class {
            crate::home_resources::HomeClass::Account => self.account.native_path(),
            crate::home_resources::HomeClass::ApiKey => self.key_plan()?.native_path(),
            crate::home_resources::HomeClass::Probe => {
                return Err("Probe is not an active Host entry".into())
            }
        };
        if config.codex_home != path || config.probe_home != self.probe.native_path() {
            return Err(
                "Actual Host home/probe differs from explicit source descriptors; no fallback"
                    .into(),
            );
        }
        Ok(())
    }
}
/// Actual Root key setup receiving operation. All storage preflights precede
/// home creation; failed candidates never install a replacement REC binding.
/// The caller retains current bindings until this operation returns successfully.
pub struct NativeKeyAdmission {
    pub namespaces: std::sync::Arc<crate::hosting::attachment_custody::NativeNamespaceBindings>,
    pub attachment: std::sync::Arc<crate::hosting::attachment_custody::AttachmentCustody>,
    pub observation: Value,
}
pub fn prepare_native_key_namespace(
    bootstrap: &HomeBootstrapSet,
    app_data: &std::path::Path,
    app_custody: &std::sync::Arc<crate::hosting::AppRuntimeCustody>,
) -> Result<NativeKeyAdmission, String> {
    use crate::hosting::attachment_custody::AttachmentCustody;
    let proposed = bootstrap.native_namespaces(true)?;
    let preflight = app_custody.preflight_native_namespaces(&proposed)?;
    // Check actual S/C/lock geometry before materializing the key home.
    AttachmentCustody::open_with_namespaces(app_data, proposed)?;
    bootstrap.prepare_key()?;
    let namespaces = bootstrap.native_namespaces(true)?;
    app_custody.preflight_native_namespaces(&namespaces)?;
    let attachment = std::sync::Arc::new(AttachmentCustody::open_with_namespaces(
        app_data,
        namespaces.clone(),
    )?);
    let committed = app_custody.bind_native_namespaces(namespaces.clone())?;
    Ok(NativeKeyAdmission {
        namespaces,
        attachment,
        observation: json!({"state":"actual namespace candidate received","preflight":preflight,"rec":committed,"qualification":"metadata geometry only; no native/auth/discovery claim"}),
    })
}
fn home_resource_view(observation: &crate::home_resources::HomeObservation) -> Value {
    json!({"modeHomeClass":observation.class.as_str(),"homeIdentity":observation.opaque_home_id,"nativePath":crate::attachments::native_path_identity(&observation.native_path),"displayPath":observation.display_path(),"resources":observation.resources.iter().map(|resource| json!({"name":resource.name,"destination":crate::attachments::native_path_identity(&resource.destination),"intendedTarget":resource.intended_target.as_ref().map(|path|crate::attachments::native_path_identity(path)),"state":format!("{:?}",resource.state),"limit":resource.limit})).collect::<Vec<_>>(),"limit":"resource relationship is a current observation; resolved config target is not future write authority"})
}

/// Disposable state for one actual native home. A mode label selects a source;
/// it never substitutes for the Host's opaque full generation or transfers threads.
pub struct HomeSession {
    pub(crate) class: crate::home_resources::HomeClass,
    pub(crate) host: std::sync::Arc<crate::hosting::Host>,
    pub(crate) host_config: Result<crate::hosting::HostConfig, String>,
    pub(crate) runtime: std::sync::Mutex<RuntimeSession>,
    pub(crate) history: std::sync::Mutex<HistorySession>,
    pub(crate) access_selection: std::sync::Mutex<Option<crate::access::ConversationSelection>>,
    pub(crate) recovery_startup: std::sync::Arc<std::sync::Mutex<RecoveryStartup>>,
    pub(crate) role_supply_status: std::sync::Mutex<Value>,
    pub(crate) attachment_custody: std::sync::Mutex<
        Result<std::sync::Arc<crate::hosting::attachment_custody::AttachmentCustody>, String>,
    >,
    pub(crate) thread_home_kinds: std::sync::Mutex<std::collections::HashMap<String, &'static str>>,
    pub(crate) account_sources: std::sync::Mutex<Vec<crate::hosting::SourceRequest>>,
    // Actual Host-issued capability stays private. No renderer pointer can mint it.
    oauth_login: std::sync::Mutex<Option<std::sync::Arc<crate::hosting::OAuthLogin>>>,
    oauth_start_gate: std::sync::Mutex<()>,
}
impl HomeSession {
    pub fn new(
        class: crate::home_resources::HomeClass,
        host: std::sync::Arc<crate::hosting::Host>,
        config: Result<crate::hosting::HostConfig, String>,
    ) -> Result<Self, String> {
        if class == crate::home_resources::HomeClass::Probe {
            return Err("Probe is not an active conversation/account entry".into());
        }
        Ok(Self {
            class,
            host,
            host_config: config,
            runtime: std::sync::Mutex::new(RuntimeSession::default()),
            history: std::sync::Mutex::new(HistorySession::default()),
            access_selection: std::sync::Mutex::new(None),
            recovery_startup: std::sync::Arc::new(
                std::sync::Mutex::new(RecoveryStartup::default()),
            ),
            role_supply_status: std::sync::Mutex::new(
                json!({"state":"not-supplied","adoption":"unknown"}),
            ),
            attachment_custody: std::sync::Mutex::new(Err(
                "Attachment custody not initialized for this home".into(),
            )),
            thread_home_kinds: std::sync::Mutex::new(std::collections::HashMap::new()),
            account_sources: std::sync::Mutex::new(vec![]),
            oauth_login: std::sync::Mutex::new(None),
            oauth_start_gate: std::sync::Mutex::new(()),
        })
    }
    pub fn source(&self) -> &std::sync::Arc<crate::hosting::Host> {
        &self.host
    }
    pub fn class(&self) -> crate::home_resources::HomeClass {
        self.class
    }
    pub fn account_view(&self) -> Value {
        let sources = self.account_sources.lock().unwrap();
        json!({"modeHomeClass":self.class.as_str(),"observations":sources.iter().map(|source|self.host.account_rpc_observation(source).unwrap_or_else(|error|json!({"limit":error,"source":source.evidence()}))).collect::<Vec<_>>(),"limit":"native source facts; credential validity and actor identity are not inferred"})
    }
}
pub struct HomeRouter {
    account: std::sync::Arc<HomeSession>,
    key: Option<std::sync::Arc<HomeSession>>,
    active: crate::home_resources::HomeClass,
}
impl HomeRouter {
    pub fn new(account: std::sync::Arc<HomeSession>) -> Result<Self, String> {
        if account.class != crate::home_resources::HomeClass::Account {
            return Err("Primary entry must be the explicit account source".into());
        }
        Ok(Self {
            account,
            key: None,
            active: crate::home_resources::HomeClass::Account,
        })
    }
    pub fn active(&self) -> std::sync::Arc<HomeSession> {
        self.entry(self.active).expect("active entry is retained")
    }
    pub fn entry(
        &self,
        class: crate::home_resources::HomeClass,
    ) -> Result<std::sync::Arc<HomeSession>, String> {
        match class {
            crate::home_resources::HomeClass::Account => Ok(self.account.clone()),
            crate::home_resources::HomeClass::ApiKey => self
                .key
                .clone()
                .ok_or_else(|| "Separate key entry is not configured; no account fallback".into()),
            crate::home_resources::HomeClass::Probe => {
                Err("Probe is not a conversation entry".into())
            }
        }
    }
    pub fn activate(&mut self, class: crate::home_resources::HomeClass) -> Result<(), String> {
        self.entry(class)?;
        self.active = class;
        Ok(())
    }
    pub fn bind_key(&mut self, key: std::sync::Arc<HomeSession>) -> Result<(), String> {
        if self.key.is_some() || key.class != crate::home_resources::HomeClass::ApiKey {
            return Err("Key entry already bound or wrong mode; no source replacement".into());
        }
        let account = self.account.host_config.as_ref().map_err(Clone::clone)?;
        let config = key.host_config.as_ref().map_err(Clone::clone)?;
        if account.codex_home == config.codex_home {
            return Err("Account/key native source paths are identical".into());
        }
        let original = self.account.host.app_runtime_custody()?;
        let receiving = key.host.app_runtime_custody()?;
        if !std::sync::Arc::ptr_eq(&original, &receiving) {
            return Err("Key source does not share the actual App session/sole writer custody; no source substitution".into());
        }
        self.key = Some(key);
        Ok(())
    }
    /// Resolve an actual full tuple, including retained closed generations in its
    /// owning App session. Stale/closed operational admission remains Host-owned.
    pub fn for_generation(
        &self,
        generation: &Value,
    ) -> Result<std::sync::Arc<HomeSession>, String> {
        crate::recovery::generation_ref(generation)?;
        let matches = self
            .entries()
            .into_iter()
            .filter(|entry| {
                let current = entry.host.snapshot()["generation"].clone();
                current["home"] == generation["home"]
                    && current["appSession"] == generation["appSession"]
            })
            .collect::<Vec<_>>();
        if matches.len() != 1 {
            return Err(
                "Full native home/session has no unique owning App source; no active-home fallback"
                    .into(),
            );
        }
        Ok(matches[0].clone())
    }
    pub fn entries(&self) -> Vec<std::sync::Arc<HomeSession>> {
        let mut entries = vec![self.account.clone()];
        if let Some(key) = &self.key {
            entries.push(key.clone());
        }
        entries
    }
    pub fn snapshot(&self) -> Value {
        json!({"activeModeHomeClass":self.active.as_str(),"entries":self.entries().iter().map(|entry|json!({"modeHomeClass":entry.class.as_str(),"generation":entry.host.snapshot()["generation"],"state":entry.host.snapshot()["state"],"configurationLimit":entry.host_config.as_ref().err()})).collect::<Vec<_>>(),"limit":"mode selection does not transfer native threads; each source retains its full generation/home"})
    }
}

/// Native secure-field delivery only. No renderer argument or replayable value.
/// Tests do not invoke this platform control; source is not a UI witness.
pub(crate) fn native_api_key_entry(app: &tauri::AppHandle) -> Result<Option<String>, ()> {
    #[cfg(target_os = "macos")]
    {
        let (sender, receiver) = std::sync::mpsc::sync_channel(1);
        app.run_on_main_thread(move || {
            let value = unsafe { mac_secure_entry::show() };
            let _ = sender.send(value);
        })
        .map_err(|_| ())?;
        receiver.recv().map_err(|_| ())?
    }
    #[cfg(not(target_os = "macos"))]
    {
        let _ = app;
        Err(())
    }
}
#[cfg(target_os = "macos")]
mod mac_secure_entry {
    use std::ffi::{c_char, c_void};
    type Id = *mut c_void;
    #[repr(C)]
    #[derive(Clone, Copy)]
    struct Point {
        x: f64,
        y: f64,
    }
    #[repr(C)]
    #[derive(Clone, Copy)]
    struct Size {
        width: f64,
        height: f64,
    }
    #[repr(C)]
    #[derive(Clone, Copy)]
    struct Rect {
        origin: Point,
        size: Size,
    }
    #[link(name = "AppKit", kind = "framework")]
    extern "C" {}
    #[link(name = "objc")]
    extern "C" {
        fn objc_getClass(name: *const c_char) -> Id;
        fn sel_registerName(name: *const c_char) -> Id;
        fn objc_msgSend();
    }
    unsafe fn selector(name: &'static [u8]) -> Id {
        sel_registerName(name.as_ptr().cast())
    }
    unsafe fn class(name: &'static [u8]) -> Id {
        objc_getClass(name.as_ptr().cast())
    }
    unsafe fn id(receiver: Id, name: &'static [u8]) -> Id {
        let f: unsafe extern "C" fn(Id, Id) -> Id = std::mem::transmute(objc_msgSend as *const ());
        f(receiver, selector(name))
    }
    unsafe fn object(receiver: Id, name: &'static [u8], value: Id) {
        let f: unsafe extern "C" fn(Id, Id, Id) = std::mem::transmute(objc_msgSend as *const ());
        f(receiver, selector(name), value);
    }
    unsafe fn string(text: &'static [u8]) -> Id {
        let f: unsafe extern "C" fn(Id, Id, *const c_char) -> Id =
            std::mem::transmute(objc_msgSend as *const ());
        f(
            class(b"NSString\0"),
            selector(b"stringWithUTF8String:\0"),
            text.as_ptr().cast(),
        )
    }
    unsafe fn release(value: Id) {
        let f: unsafe extern "C" fn(Id, Id) = std::mem::transmute(objc_msgSend as *const ());
        f(value, selector(b"release\0"));
    }
    pub(super) unsafe fn show() -> Result<Option<String>, ()> {
        let pool = id(class(b"NSAutoreleasePool\0"), b"new\0");
        let alert = id(class(b"NSAlert\0"), b"new\0");
        let allocated = id(class(b"NSSecureTextField\0"), b"alloc\0");
        let initialize: unsafe extern "C" fn(Id, Id, Rect) -> Id =
            std::mem::transmute(objc_msgSend as *const ());
        let field = initialize(
            allocated,
            selector(b"initWithFrame:\0"),
            Rect {
                origin: Point { x: 0., y: 0. },
                size: Size {
                    width: 360.,
                    height: 26.,
                },
            },
        );
        if pool.is_null() || alert.is_null() || field.is_null() {
            if !field.is_null() {
                release(field);
            }
            if !alert.is_null() {
                release(alert);
            }
            if !pool.is_null() {
                release(pool);
            }
            return Err(());
        }
        object(
            alert,
            b"setMessageText:\0",
            string(b"Add or replace API key through Codex\0"),
        );
        object(alert,b"setInformativeText:\0",string(b"The key is delivered once to this separate App key home. Native acknowledgment does not establish validity until actual use.\0"));
        object(alert, b"setAccessoryView:\0", field);
        let add: unsafe extern "C" fn(Id, Id, Id) -> Id =
            std::mem::transmute(objc_msgSend as *const ());
        add(
            alert,
            selector(b"addButtonWithTitle:\0"),
            string(b"Submit key\0"),
        );
        add(
            alert,
            selector(b"addButtonWithTitle:\0"),
            string(b"Cancel\0"),
        );
        let modal: unsafe extern "C" fn(Id, Id) -> isize =
            std::mem::transmute(objc_msgSend as *const ());
        let accepted = modal(alert, selector(b"runModal\0")) == 1000;
        let result = if accepted {
            let value = id(field, b"stringValue\0");
            let length: unsafe extern "C" fn(Id, Id, usize) -> usize =
                std::mem::transmute(objc_msgSend as *const ());
            let n = length(value, selector(b"lengthOfBytesUsingEncoding:\0"), 4);
            let pointer: unsafe extern "C" fn(Id, Id) -> *const u8 =
                std::mem::transmute(objc_msgSend as *const ());
            let bytes = pointer(value, selector(b"UTF8String\0"));
            if bytes.is_null() || n == 0 {
                Err(())
            } else {
                std::str::from_utf8(std::slice::from_raw_parts(bytes, n))
                    .map(|text| Some(text.to_owned()))
                    .map_err(|_| ())
            }
        } else {
            Ok(None)
        };
        // Release the secure field before the caller receives its one transient
        // buffer. Ordinary drop/release is not allocator/OS physical erasure.
        object(field, b"setStringValue:\0", string(b"\0"));
        release(field);
        release(alert);
        release(pool);
        result
    }
}

/// Explicit native source read; no credential/config filesystem access or automatic refresh.
pub fn read_native_home_access(home: &HomeSession, generation: &Value) -> Result<Value, String> {
    for method in ["configRequirements/read", "account/read"] {
        let source = match method {
            "configRequirements/read" => home.host.account_requirements_read_scoped(generation)?,
            _ => home.host.account_read_scoped(generation)?,
        };
        home.account_sources.lock().unwrap().push(source.clone());
        home.host
            .source_request_wait(&source, std::time::Duration::from_secs(20))?;
    }
    Ok(home.account_view())
}

/// Consumes explicit Root OS paths. Existing account/probe are observations,
/// never relocated or claimed as newly App-owned plans to fit this constructor.
pub fn freeze_root_home_descriptors(
    app_data: &std::path::Path,
    config: &crate::hosting::HostConfig,
    key_path: Option<std::path::PathBuf>,
    targets: [Option<std::path::PathBuf>; 3],
) -> Result<HomeBootstrapSet, String> {
    use crate::home_resources::{
        ExistingHomeReference, HomeClass, OwnedHomePlan, SharedResourceTargets,
    };
    let account = ExistingHomeReference::new(config.codex_home.clone(), HomeClass::Account)?;
    let probe = ExistingHomeReference::new(config.probe_home.clone(), HomeClass::Probe)?;
    let shared_root_targets = match &targets {
        [Some(config), Some(agents), Some(skills)] => Some(SharedResourceTargets {
            config_toml: config.clone(),
            global_agents_md: agents.clone(),
            skills: skills.clone(),
        }),
        _ => None,
    };
    let key = match key_path {
        None => None,
        Some(path) => {
            let [config_toml, global_agents_md, skills] = targets;
            let shared = SharedResourceTargets {
                config_toml: config_toml.ok_or("Explicit shared config source not supplied")?,
                global_agents_md: global_agents_md
                    .ok_or("Explicit shared global AGENTS source not supplied")?,
                skills: skills.ok_or("Explicit shared skills source not supplied")?,
            };
            Some(OwnedHomePlan::new(
                app_data.to_path_buf(),
                path,
                HomeClass::ApiKey,
                Some(shared),
            )?)
        }
    };
    let mut set = HomeBootstrapSet::new(account, key, probe)?;
    set.shared_root_targets = shared_root_targets;
    Ok(set)
}

/// Genuine private native-entry submission; source binding is checked before
/// opening the field and again before giving its transient buffer to Host.
pub fn submit_native_home_key<F: FnOnce() -> Result<Option<String>, ()>>(
    home: &HomeSession,
    bootstrap: &HomeBootstrapSet,
    generation: &Value,
    entry: F,
) -> Result<Value, String> {
    if home.class() != crate::home_resources::HomeClass::ApiKey {
        return Err("Native key entry requires the separate configured key source".into());
    }
    let config = home.host_config.as_ref().map_err(Clone::clone)?;
    bootstrap.validate_binding(home.class(), config)?;
    let policy = home.host.account_requirements_read_scoped(generation)?;
    home.account_sources.lock().unwrap().push(policy.clone());
    home.host
        .source_request_wait(&policy, std::time::Duration::from_secs(20))?;
    let source =
        home.host
            .account_login_api_key_from_native_entry(generation, Some(&policy), || {
                let input = entry()?;
                if bootstrap.validate_binding(home.class(), config).is_err() {
                    return Err(());
                }
                Ok(input)
            })?;
    match source {
        None => Ok(
            json!({"state":"native secure entry cancelled; no key RPC or resend","home":home.class().as_str()}),
        ),
        Some(source) => {
            home.account_sources.lock().unwrap().push(source.clone());
            home.host
                .source_request_wait(&source, std::time::Duration::from_secs(20))?;
            Ok(home.account_view())
        }
    }
}

/// Source-created immutable runtime assessment, not a durable record or a
/// deserializable native authorization. Its comparison excludes clock passage.
pub struct HomeLogoutAssessment {
    generation: Value,
    material: Value,
    view: Value,
}
impl HomeLogoutAssessment {
    pub fn snapshot(&self) -> Value {
        self.view.clone()
    }
}
pub fn assess_native_home_work(
    home: &HomeSession,
    generation: &Value,
) -> Result<HomeLogoutAssessment, String> {
    crate::recovery::generation_ref(generation)?;
    let mut runtime = home.runtime.lock().unwrap();
    let (cursor, position) = runtime.cursor();
    let observation = home.host.observe(cursor, position);
    let snapshot = &observation["snapshot"];
    if snapshot["generation"] != *generation || snapshot["state"] != "ready" {
        return Err("Selected native home/full generation is unavailable for assessment; no window/home fallback".into());
    }
    let received = runtime.receive(&observation);
    drop(runtime);
    let mut live = vec![];
    let mut unresolved_turns = vec![];
    for thread in snapshot["threads"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|thread| thread["generation"] == *generation)
    {
        let Some(id) = thread["threadId"].as_str() else {
            continue;
        };
        match observed_steering_target(snapshot,generation,id){
            Ok(target)=>live.push(json!({"generation":generation,"threadId":id,"turnId":target["turnId"],"status":"inProgress","source":target["source"]})),
            Err(error)=>if snapshot["conversationTurns"].as_array().into_iter().flatten().any(|turn|turn["generation"]==*generation&&turn["threadId"]==id&&turn["nativeTurn"]["status"]=="inProgress") {unresolved_turns.push(json!({"threadId":id,"limit":error}));},
        }
    }
    for turn in snapshot["conversationTurns"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|turn| {
            turn["generation"] == *generation && turn["nativeTurn"]["status"] == "inProgress"
        })
    {
        if !live
            .iter()
            .any(|row| row["threadId"] == turn["threadId"] && row["turnId"] == turn["turnId"])
        {
            unresolved_turns.push(json!({"threadId":turn["threadId"],"turnId":turn["turnId"],"reportedStatus":turn["nativeTurn"]["status"],"terminalEventObserved":turn["terminalEventObserved"],"observationEnded":turn["observationEnded"],"limit":"progress memo lacks current target warrant or is contradictory; activity not established, no ended inference"}));
        }
    }
    let requests=snapshot["serverRequests"].as_array().into_iter().flatten().filter(|request|request["generation"]==*generation&&request["state"]=="outstanding").map(|request|json!({"generation":request["generation"],"requestIdentity":request["requestIdentity"],"method":request["method"],"state":request["state"],"threadId":request["nativeParameters"]["threadId"],"turnId":request["nativeParameters"]["turnId"]})).collect::<Vec<_>>();
    let native = &received["nativeView"];
    let valid_view =
        native["generation"] == *generation && received["nativeViewObservationEnded"] != true;
    let mut children = vec![];
    let mut unknown = vec![];
    if valid_view {
        for child in native["descendants"].as_array().into_iter().flatten() {
            let state = child["lastObservedStatus"]["status"].as_str();
            let row = json!({"generation":native["generation"],"threadId":child["threadId"],"parentThreadId":child["parentThreadId"],"reportedStatus":state,"source":child["statusSource"],"limit":"last native reported activity; no complete process/child census"});
            if child["observationEnded"] != true && matches!(state, Some("running" | "pendingInit"))
            {
                children.push(row);
            } else {
                unknown.push(row);
            }
        }
    }
    let history = home.history.lock().unwrap().snapshot(None);
    if history["generation"] == *generation {
        for child in history["selected"]["knownChildren"]
            .as_array()
            .into_iter()
            .flatten()
        {
            if !children
                .iter()
                .chain(unknown.iter())
                .any(|row| row["threadId"] == child["threadId"])
            {
                unknown.push(json!({"generation":history["generation"],"threadId":child["threadId"],"parentThreadId":child["parentThreadId"],"source":"selected native stored-history edge","reportedStatus":null,"limit":"history-only relation; current activity unknown"}));
            }
        }
    }
    // Set ordering only makes material comparison stable; it assigns no
    // chronology, precedence, winner or authority to an identity.
    for rows in [
        &mut live,
        &mut unresolved_turns,
        &mut children,
        &mut unknown,
    ] {
        rows.sort_by_key(Value::to_string);
    }
    let mut requests = requests;
    requests.sort_by_key(Value::to_string);
    let coverage = json!({"turns":{"scope":"current selected-home source","available":snapshot["conversationTurns"].is_array(),"complete":false,"unresolved":unresolved_turns},"requests":{"scope":"current received register","available":snapshot["serverRequests"].is_array(),"complete":false},"children":{"receivingViewAvailable":valid_view,"complete":false,"limit":"child visibility/completeness not established; additional work may exist"},"receivingLimits":received["nativeViewLimits"]});
    let namespace_events=snapshot["journal"].as_array().into_iter().flatten().filter(|event|event["generation"]==*generation&&event["frame"]["method"]=="account/updated").map(|event|json!({"generation":event["generation"],"receiptPosition":event["position"],"method":event["frame"]["method"]})).collect::<Vec<_>>();
    let operations=snapshot["clientRequests"].as_array().into_iter().flatten().filter(|request|request["generation"]==*generation&&matches!(request["method"].as_str(),Some("account/login/start"|"account/login/cancel"|"account/logout"))).map(|request|json!({"requestIdentity":request["requestIdentity"],"method":request["method"],"writeResult":request["writeResult"],"outcome":request["outcome"]})).collect::<Vec<_>>();
    let latest_read = snapshot["clientRequests"]
        .as_array()
        .into_iter()
        .flatten()
        .rev()
        .find(|request| request["generation"] == *generation && request["method"] == "account/read")
        .and_then(|request| {
            home.host
                .source_request(generation, &request["requestIdentity"])
                .ok()
        })
        .map(|source| source.evidence());
    let read_availability = match latest_read.as_ref() {
        Some(evidence)
            if evidence["outcome"] == "response-observed-result"
                && evidence["authResponseShapeValid"] == true =>
        {
            "typed native account read observed"
        }
        Some(evidence) if evidence["outcome"] == "response-observed-error" => {
            "native account read error; current account unknown"
        }
        Some(_) => "native account read pending/shape unavailable; prior report only",
        None => "no source-bound account read available",
    };
    let current_account=latest_read.as_ref().filter(|evidence|evidence["outcome"]=="response-observed-result"&&evidence["authResponseShapeValid"]==true).map(|evidence|match evidence["response"]["result"].get("account"){
        None=>json!({"state":"account omitted; unknown/unavailable","nativeType":null}),
        Some(Value::Null)=>json!({"state":"native null account reported; not pending-login cancellation","nativeType":null}),
        Some(account) if matches!(account["type"].as_str(),Some("chatgpt"|"apiKey"|"chatgptAuthTokens"))=>json!({"state":"native type reported; identity not established","nativeType":account["type"]}),
        Some(_)=>json!({"state":"redacted/unavailable account; unknown","nativeType":null}),
    }).unwrap_or_else(||json!({"state":"current native report unavailable; previous read is only last observed","nativeType":null}));
    let account = json!({"state":received["accountObservation"]["state"],"nativeType":received["accountObservation"]["nativeAccount"]["type"],"readAvailability":read_availability,"currentReport":current_account,"namespaceEvents":namespace_events,"operations":operations,"identityVerified":false,"unchangedIdentityProven":false,"limit":"redacted/unavailable equality does not prove unchanged identity; another identical read/clock tick alone is not a namespace change"});
    let material = json!({"modeHomeClass":home.class.as_str(),"generation":generation,"account":account,"observedLiveTurns":live,"observedOutstandingRequests":requests,"observedActiveChildren":children,"knownChildActivityUnknown":unknown,"coverage":coverage});
    let view = json!({"modeHomeClass":home.class.as_str(),"generation":generation,"observedAt":crate::util::now_rfc3339(),"sourceCursor":received["observerCursor"],"account":account,"observedLiveTurns":live,"observedOutstandingRequests":requests,"observedActiveChildren":children,"knownChildActivityUnknown":unknown,"coverage":coverage,"warning":"None observed is not none. Child visibility/completeness is not established; additional work may exist. Logout acknowledgment does not end turns/children, delete history or prove credential-store removal."});
    Ok(HomeLogoutAssessment {
        generation: generation.clone(),
        material,
        view,
    })
}
pub fn logout_native_home<F: FnOnce(&Value) -> bool>(
    home: &HomeSession,
    bootstrap: Option<&HomeBootstrapSet>,
    generation: &Value,
    confirm: F,
) -> Result<Value, String> {
    let config = home.host_config.as_ref().map_err(Clone::clone)?;
    if let Some(bootstrap) = bootstrap {
        bootstrap.validate_binding(home.class(), config)?;
    } else if home.class != crate::home_resources::HomeClass::Account {
        return Err("Key source physical binding unavailable; no fallback".into());
    }
    let frozen = assess_native_home_work(home, generation)?;
    if !confirm(&frozen.view) {
        return Ok(
            json!({"state":"native confirmation cancelled; no logout request","assessment":frozen.view}),
        );
    }
    if let Some(bootstrap) = bootstrap {
        bootstrap.validate_binding(home.class(), config)?;
    }
    let current = assess_native_home_work(home, &frozen.generation)?;
    if current.material != frozen.material {
        return Err("Selected source/account or observed work/coverage changed during native confirmation; refresh and confirm again, no logout sent".into());
    }
    let source = home.host.account_logout_scoped(&frozen.generation)?;
    home.account_sources.lock().unwrap().push(source.clone());
    let waited = home
        .host
        .source_request_wait(&source, std::time::Duration::from_secs(20));
    let evidence = source.evidence();
    if evidence["authResponseShapeValid"] == true
        && evidence["outcome"] == "response-observed-result"
        && evidence["sourceCurrent"] == true
    {
        if let Some(selection) = home.access_selection.lock().unwrap().as_mut() {
            let entry = selection.snapshot()["selection"]["entryId"].clone();
            let affected = (home.class == crate::home_resources::HomeClass::Account
                && entry == "chatgpt-account")
                || (home.class == crate::home_resources::HomeClass::ApiKey && entry == "api-key");
            if affected && selection.owning_generation() == Some(&frozen.generation) {
                let _=selection.unavailable("Codex reported logout for this entry; no home transfer or credential-file inspection");
            }
        }
    }
    // Allowed native read reconciles the report; it is not a retry/removal or a
    // token-refresh/credential-store inspection, and never uses another home.
    let after_read = match home.host.account_read_scoped(&frozen.generation) {
        Ok(read) => {
            home.account_sources.lock().unwrap().push(read.clone());
            let wait = home
                .host
                .source_request_wait(&read, std::time::Duration::from_secs(20));
            json!({"observation":home.host.account_rpc_observation(&read).ok(),"waitError":wait.err()})
        }
        Err(error) => json!({"state":"same-source account reread unavailable","limit":error}),
    };
    Ok(
        json!({"assessment":frozen.view,"source":home.host.account_rpc_observation(&source)?,"waitError":waited.err(),"accountReadAfterLogout":after_read,"limit":"Native send/acknowledgment/account observation are separate; no credential inspection, turn/child ending, history deletion or automatic resend"}),
    )
}

/// Allocate a new probe using the physical OS temp parent and mktemp -d. This
/// resolves an allocation source, never relocates an existing received home.
pub fn allocate_fresh_probe(temp_parent: &std::path::Path) -> Result<std::path::PathBuf, String> {
    let parent = std::fs::canonicalize(temp_parent)
        .map_err(|_| "OS scratch parent unavailable; no probe default")?;
    crate::storage::check_path(&parent)?;
    let before =
        std::fs::metadata(&parent).map_err(|_| "OS scratch parent metadata unavailable")?;
    if !before.is_dir() {
        return Err("OS scratch parent is not a directory".into());
    }
    let output = std::process::Command::new("mktemp")
        .arg("-d")
        .arg(parent.join("chirality-codex-probe.XXXXXX"))
        .output()
        .map_err(|_| "Fresh mktemp probe allocation unavailable")?;
    if !output.status.success() {
        return Err("Fresh mktemp probe allocation failed; no fallback".into());
    }
    let bytes = output
        .stdout
        .strip_suffix(b"\n")
        .ok_or("mktemp probe result is not newline closed")?;
    #[cfg(unix)]
    let path = {
        use std::os::unix::ffi::OsStringExt;
        std::path::PathBuf::from(std::ffi::OsString::from_vec(bytes.to_vec()))
    };
    #[cfg(not(unix))]
    let path = std::path::PathBuf::from(
        std::str::from_utf8(bytes)
            .map_err(|_| "Probe path cannot be represented losslessly on this platform")?,
    );
    if path.parent() != Some(parent.as_path()) {
        return Err("mktemp result is outside the actual supplied scratch parent".into());
    }
    crate::storage::check_path(&path)?;
    let after =
        std::fs::metadata(&parent).map_err(|_| "OS scratch parent changed during allocation")?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::MetadataExt;
        if before.dev() != after.dev() || before.ino() != after.ino() {
            return Err(
                "Actual OS scratch parent changed during allocation; probe binding unavailable"
                    .into(),
            );
        }
    }
    if !after.is_dir()
        || std::fs::canonicalize(&parent)
            .map_err(|_| "Scratch parent unavailable after allocation")?
            != parent
        || !path.is_dir()
    {
        return Err("Probe/parent physical binding unavailable after allocation".into());
    }
    Ok(path)
}

/// Safe reader only. Public observation references cannot reconstruct this handle.
pub(crate) fn native_oauth_observation(home: &HomeSession) -> Value {
    let original = home.oauth_login.lock().unwrap().clone();
    match original {
        None => {
            json!({"state":"unavailable","limit":"no original private sign-in control received"})
        }
        Some(login) => native_oauth_observation_for(home, &login),
    }
}
fn native_oauth_observation_for(home: &HomeSession, login: &crate::hosting::OAuthLogin) -> Value {
    match home.host.account_oauth_observation(login) {
        Ok(view) => {
            json!({"state":"source-observed","source":view,"accountConfirmation":"matched success still requires native account/read; no signed-in identity inferred"})
        }
        Err(_) => {
            json!({"state":"unknown/source-unavailable","generation":login.source().generation(),"requestIdentity":login.source().request_id(),"limit":"original sign-in source unavailable; no retarget, cancel success or signed-out inference"})
        }
    }
}
fn check_native_oauth_home(
    home: &HomeSession,
    bootstrap: Option<&HomeBootstrapSet>,
    expected: &Value,
) -> Result<(), String> {
    if home.class() != crate::home_resources::HomeClass::Account {
        return Err("ChatGPT sign-in requires the original account home".into());
    }
    if let Some(bootstrap) = bootstrap {
        bootstrap.validate_binding(
            home.class(),
            home.host_config.as_ref().map_err(Clone::clone)?,
        )?;
    }
    let snapshot = home.host.snapshot();
    if snapshot["generation"] != *expected || snapshot["state"] != "ready" {
        return Err(
            "Requested original account generation unavailable; no sign-in/control retarget".into(),
        );
    }
    Ok(())
}
fn capture_native_oauth(
    home: &HomeSession,
    bootstrap: Option<&HomeBootstrapSet>,
    requested: &Value,
) -> Result<std::sync::Arc<crate::hosting::OAuthLogin>, String> {
    check_native_oauth_home(home, bootstrap, requested)?;
    let original = home
        .oauth_login
        .lock()
        .unwrap()
        .clone()
        .ok_or("Original private sign-in control unavailable")?;
    if original.source().generation() != requested {
        return Err(
            "Requested full generation differs from original sign-in wrapper; no successor control"
                .into(),
        );
    }
    check_native_oauth_home(home, bootstrap, requested)?;
    Ok(original)
}
fn check_native_oauth_original(
    home: &HomeSession,
    bootstrap: Option<&HomeBootstrapSet>,
    requested: &Value,
    original: &std::sync::Arc<crate::hosting::OAuthLogin>,
) -> Result<(), String> {
    if original.source().generation() != requested {
        return Err("Original sign-in wrapper differs from requested generation".into());
    }
    check_native_oauth_home(home, bootstrap, requested)?;
    if !home
        .oauth_login
        .lock()
        .unwrap()
        .as_ref()
        .is_some_and(|received| std::sync::Arc::ptr_eq(received, original))
    {
        return Err(
            "Original issued sign-in operation superseded; no replacement interaction".into(),
        );
    }
    Ok(())
}
// Private start return carries the actual issued wrapper through wait and automatic
// presentation. No Serde/Debug/public constructor or DTO authority.
pub(crate) struct NativeOAuthStart {
    original: Option<std::sync::Arc<crate::hosting::OAuthLogin>>,
    observed: Value,
}
pub(crate) fn start_native_oauth<F: FnOnce() -> bool>(
    home: &HomeSession,
    generation: &Value,
    mode: crate::hosting::NativeLoginMode,
    bootstrap: Option<&HomeBootstrapSet>,
    confirm: F,
) -> Result<NativeOAuthStart, String> {
    let gate = home
        .oauth_start_gate
        .try_lock()
        .map_err(|_| "Another native sign-in start is pending; no replacement/retry")?;
    check_native_oauth_home(home, bootstrap, generation)?;
    if !confirm() {
        return Ok(NativeOAuthStart {
            original: None,
            observed: json!({"state":"native start confirmation dismissed; no sign-in RPC"}),
        });
    }
    check_native_oauth_home(home, bootstrap, generation)?;
    let policy = home.host.account_requirements_read_scoped(generation)?;
    home.account_sources.lock().unwrap().push(policy.clone());
    home.host
        .source_request_wait(&policy, std::time::Duration::from_secs(20))?;
    check_native_oauth_home(home, bootstrap, generation)?;
    let login = std::sync::Arc::new(home.host.account_oauth_start(
        generation,
        mode,
        Some(&policy),
    )?);
    *home.oauth_login.lock().unwrap() = Some(login.clone());
    home.account_sources
        .lock()
        .unwrap()
        .push(login.source().clone());
    drop(gate);
    home.host
        .source_request_wait(login.source(), std::time::Duration::from_secs(20))?;
    let observed = native_oauth_observation_for(home, &login);
    Ok(NativeOAuthStart {
        original: Some(login),
        observed,
    })
}
pub(crate) fn present_native_oauth(
    home: &HomeSession,
    requested: &Value,
    bootstrap: Option<&HomeBootstrapSet>,
) -> Result<Value, String> {
    present_requested_native_oauth(home, requested, bootstrap, |view, lease, current| {
        native_oauth_display::present(view, lease, current)
    })
}
fn present_requested_native_oauth<F>(
    home: &HomeSession,
    requested: &Value,
    bootstrap: Option<&HomeBootstrapSet>,
    callback: F,
) -> Result<Value, String>
where
    F: FnOnce(
        crate::hosting::NativeLoginView<'_>,
        crate::hosting::NativeLoginLease,
        &(dyn Fn() -> bool + Sync),
    ) -> crate::hosting::NativeLoginPresentation,
{
    let original = capture_native_oauth(home, bootstrap, requested)?;
    present_bound_native_oauth(home, requested, bootstrap, &original, callback)
}
fn present_bound_native_oauth<F>(
    home: &HomeSession,
    requested: &Value,
    bootstrap: Option<&HomeBootstrapSet>,
    original: &std::sync::Arc<crate::hosting::OAuthLogin>,
    callback: F,
) -> Result<Value, String>
where
    F: FnOnce(
        crate::hosting::NativeLoginView<'_>,
        crate::hosting::NativeLoginLease,
        &(dyn Fn() -> bool + Sync),
    ) -> crate::hosting::NativeLoginPresentation,
{
    check_native_oauth_original(home, bootstrap, requested, original)?;
    let current = || check_native_oauth_original(home, bootstrap, requested, original).is_ok();
    let result = present_original_native_oauth(home, original, |view, lease| {
        if !current() {
            return crate::hosting::NativeLoginPresentation::Unavailable;
        }
        callback(view, lease, &current)
    })?;
    check_native_oauth_home(home, bootstrap, requested)?;
    Ok(result)
}
pub(crate) fn automatic_native_oauth_presentation(
    home: &HomeSession,
    started: NativeOAuthStart,
    bootstrap: Option<&HomeBootstrapSet>,
) -> Result<Value, String> {
    automatic_native_oauth_presentation_with(home, started, bootstrap, |view, lease, current| {
        native_oauth_display::present(view, lease, current)
    })
}
fn automatic_native_oauth_presentation_with<F>(
    home: &HomeSession,
    started: NativeOAuthStart,
    bootstrap: Option<&HomeBootstrapSet>,
    callback: F,
) -> Result<Value, String>
where
    F: FnOnce(
        crate::hosting::NativeLoginView<'_>,
        crate::hosting::NativeLoginLease,
        &(dyn Fn() -> bool + Sync),
    ) -> crate::hosting::NativeLoginPresentation,
{
    let Some(original) = started.original else {
        return Ok(started.observed);
    };
    let requested = original.source().generation();
    check_native_oauth_original(home, bootstrap, requested, &original)?;
    let observed = native_oauth_observation_for(home, &original);
    if observed["source"]["presentationAvailable"] == true {
        present_bound_native_oauth(home, requested, bootstrap, &original, callback)
    } else {
        Ok(observed)
    }
}
// The production wrapper and cfg(test) callbacks consume the same genuinely
// issued one-use view/lease. This seam creates no native/source proof DTO.
fn present_original_native_oauth<F>(
    home: &HomeSession,
    login: &crate::hosting::OAuthLogin,
    callback: F,
) -> Result<Value, String>
where
    F: FnOnce(
        crate::hosting::NativeLoginView<'_>,
        crate::hosting::NativeLoginLease,
    ) -> crate::hosting::NativeLoginPresentation,
{
    let delivered = home.host.account_oauth_present(login, callback)?;
    Ok(json!({"delivery":delivered,"observation":native_oauth_observation_for(home,login)}))
}
pub(crate) fn cancel_native_oauth<F: FnOnce(&Value) -> bool>(
    home: &HomeSession,
    requested: &Value,
    bootstrap: Option<&HomeBootstrapSet>,
    confirm: F,
) -> Result<Value, String> {
    let original = capture_native_oauth(home, bootstrap, requested)?;
    check_native_oauth_original(home, bootstrap, requested, &original)?;
    let before = home.host.account_oauth_observation(&original)?;
    if before["cancelAvailable"] != true {
        return Err("Original sign-in cancel unavailable/unknown; no request or retry".into());
    }
    if !confirm(&before) {
        return Ok(
            json!({"state":"native cancellation confirmation dismissed; original pending control retained"}),
        );
    }
    check_native_oauth_original(home, bootstrap, requested, &original)?;
    let cancel = home.host.account_oauth_cancel(&original)?;
    home.account_sources.lock().unwrap().push(cancel.clone());
    home.host
        .source_request_wait(&cancel, std::time::Duration::from_secs(20))?;
    let observed = home.host.account_oauth_observation(&original)?;
    let state = match observed["cancelStatus"].as_str() {
        Some("canceled") => "signed-out; original pending sign-in canceled by Codex",
        Some("notFound") => "signed-out; Codex had no pending sign-in",
        _ => "unknown/error; no cancellation or signed-out inference, no retry",
    };
    Ok(
        json!({"state":state,"source":observed,"standing":"sign-in lifecycle only; no credential-file removal, history deletion or turn/child/run end"}),
    )
}

#[cfg(not(target_os = "macos"))]
mod native_oauth_display {
    pub(super) fn present(
        _: crate::hosting::NativeLoginView<'_>,
        _: crate::hosting::NativeLoginLease,
        _: &(dyn Fn() -> bool + Sync),
    ) -> crate::hosting::NativeLoginPresentation {
        crate::hosting::NativeLoginPresentation::Unavailable
    }
}
#[cfg(target_os = "macos")]
mod native_oauth_display {
    use crate::hosting::{NativeLoginLease, NativeLoginPresentation, NativeLoginView};
    use std::ffi::{c_char, c_void};
    type Id = *mut c_void;
    #[link(name = "objc")]
    extern "C" {
        fn objc_getClass(name: *const c_char) -> Id;
        fn sel_registerName(name: *const c_char) -> Id;
        fn objc_msgSend();
    }
    #[link(name = "AppKit", kind = "framework")]
    extern "C" {}
    extern "C" {
        static _dispatch_main_q: u8;
        fn dispatch_sync_f(
            queue: Id,
            context: *mut c_void,
            work: unsafe extern "C" fn(*mut c_void),
        );
    }
    unsafe fn class(n: &'static [u8]) -> Id {
        objc_getClass(n.as_ptr().cast())
    }
    unsafe fn sel(n: &'static [u8]) -> Id {
        sel_registerName(n.as_ptr().cast())
    }
    unsafe fn id(o: Id, n: &'static [u8]) -> Id {
        let f: unsafe extern "C" fn(Id, Id) -> Id = std::mem::transmute(objc_msgSend as *const ());
        f(o, sel(n))
    }
    unsafe fn object(o: Id, n: &'static [u8], arg: Id) {
        let f: unsafe extern "C" fn(Id, Id, Id) = std::mem::transmute(objc_msgSend as *const ());
        f(o, sel(n), arg)
    }
    unsafe fn release(o: Id) {
        if !o.is_null() {
            let f: unsafe extern "C" fn(Id, Id) = std::mem::transmute(objc_msgSend as *const ());
            f(o, sel(b"release\0"))
        }
    }
    unsafe fn string(s: &str) -> Id {
        let allocated = id(class(b"NSString\0"), b"alloc\0");
        let f: unsafe extern "C" fn(Id, Id, *const u8, usize, usize) -> Id =
            std::mem::transmute(objc_msgSend as *const ());
        f(
            allocated,
            sel(b"initWithBytes:length:encoding:\0"),
            s.as_ptr(),
            s.len(),
            4,
        )
    }
    struct Context<'a> {
        view: Option<NativeLoginView<'a>>,
        lease: NativeLoginLease,
        current: &'a (dyn Fn() -> bool + Sync),
        result: NativeLoginPresentation,
    }
    pub(super) fn present(
        view: NativeLoginView<'_>,
        lease: NativeLoginLease,
        current: &(dyn Fn() -> bool + Sync),
    ) -> NativeLoginPresentation {
        let mut context = Context {
            view: Some(view),
            lease,
            current,
            result: NativeLoginPresentation::Unavailable,
        };
        // Synchronous dispatch keeps the one-use borrowed view alive until the
        // native callback returns. No 'static payload clone or detached worker.
        unsafe {
            let f: unsafe extern "C" fn(Id, Id) -> bool =
                std::mem::transmute(objc_msgSend as *const ());
            if f(class(b"NSThread\0"), sel(b"isMainThread\0")) {
                show((&mut context as *mut Context<'_>).cast())
            } else {
                dispatch_sync_f(
                    std::ptr::addr_of!(_dispatch_main_q).cast_mut().cast(),
                    (&mut context as *mut Context<'_>).cast(),
                    show,
                )
            }
        }
        context.result
    }
    unsafe extern "C" fn show(raw: *mut c_void) {
        let c = &mut *(raw as *mut Context<'_>);
        let pool = id(class(b"NSAutoreleasePool\0"), b"new\0");
        if pool.is_null() {
            return;
        }
        if c.lease.is_active() && (c.current)() {
            match c.view.take().unwrap() {
                NativeLoginView::Browser { auth_url } => {
                    let text = string(auth_url);
                    let f: unsafe extern "C" fn(Id, Id, Id) -> Id =
                        std::mem::transmute(objc_msgSend as *const ());
                    let url = f(class(b"NSURL\0"), sel(b"URLWithString:\0"), text);
                    let open: unsafe extern "C" fn(Id, Id, Id) -> bool =
                        std::mem::transmute(objc_msgSend as *const ());
                    if !url.is_null()
                        && c.lease.is_active()
                        && (c.current)()
                        && open(
                            id(class(b"NSWorkspace\0"), b"sharedWorkspace\0"),
                            sel(b"openURL:\0"),
                            url,
                        )
                    {
                        c.result = NativeLoginPresentation::Presented;
                    }
                    release(text); // OS/browser custody cannot be reclaimed/erased by App.
                }
                NativeLoginView::Device {
                    verification_url,
                    user_code,
                } => {
                    let alert = id(class(b"NSAlert\0"), b"new\0");
                    if !alert.is_null() {
                        let title = string("Sign in with your ChatGPT account (through Codex)");
                        object(alert, b"setMessageText:\0", title);
                        release(title);
                        // Native-only bounded display copies; never JSON, a Rust
                        // diagnostic, clipboard, external cache or retained matcher.
                        let text = id(class(b"NSMutableString\0"), b"new\0");
                        for part in ["Open this verification page:\n",verification_url,"\n\nEnter this code:\n",user_code,"\n\nDismiss clears this display; pending sign-in may still be canceled."]{
                            let piece=string(part);object(text,b"appendString:\0",piece);release(piece);
                        }
                        object(alert, b"setInformativeText:\0", text);
                        release(text);
                        let button = string("Dismiss");
                        let add: unsafe extern "C" fn(Id, Id, Id) -> Id =
                            std::mem::transmute(objc_msgSend as *const ());
                        add(alert, sel(b"addButtonWithTitle:\0"), button);
                        release(button);
                        let app = id(class(b"NSApplication\0"), b"sharedApplication\0");
                        let window = id(alert, b"window\0");
                        let begin: unsafe extern "C" fn(Id, Id, Id) -> Id =
                            std::mem::transmute(objc_msgSend as *const ());
                        let poll: unsafe extern "C" fn(Id, Id, Id) -> isize =
                            std::mem::transmute(objc_msgSend as *const ());
                        let session = if c.lease.is_active() && (c.current)() {
                            begin(app, sel(b"beginModalSessionForWindow:\0"), window)
                        } else {
                            std::ptr::null_mut()
                        };
                        if !session.is_null() {
                            loop {
                                if c.lease.revoked(std::time::Duration::from_millis(5))
                                    || !(c.current)()
                                {
                                    break;
                                }
                                if poll(app, sel(b"runModalSession:\0"), session) != -1002 {
                                    break;
                                }
                            }
                            object(app, b"endModalSession:\0", session);
                            c.result = NativeLoginPresentation::Dismissed;
                        }
                        let empty = string("");
                        object(alert, b"setInformativeText:\0", empty);
                        object(alert, b"setMessageText:\0", empty);
                        release(empty);
                        object(window, b"orderOut:\0", std::ptr::null_mut());
                        release(alert);
                    }
                }
            }
        }
        release(pool);
    }
}

#[cfg(all(test, unix))]
mod oauth_root_tests {
    use super::*;
    use crate::hosting::{
        Host, HostConfig, NativeLoginMode, NativeLoginPresentation, NativeLoginView,
    };
    use std::{
        path::PathBuf,
        sync::Arc,
        time::{Duration, Instant},
    };
    const PRIVATE: &str = "OWNED_ROOT_OAUTH_PRIVATE_CANARY";
    struct Fixture {
        root: PathBuf,
        home: Arc<HomeSession>,
        generation: Value,
    }
    impl Fixture {
        fn new() -> Self {
            use std::os::unix::fs::PermissionsExt;
            let root = std::fs::canonicalize(std::env::temp_dir())
                .unwrap()
                .join(crate::util::opaque_id("oauth-root-fixture-").unwrap());
            for name in ["account", "probe"] {
                std::fs::create_dir_all(root.join(name)).unwrap();
            }
            let peer = root.join("owned-peer.py");
            std::fs::write(&peer,r#"#!/usr/bin/python3
import sys,json,threading,time,os
if '--version' in sys.argv:
 print('codex-cli 0.160.0');sys.exit(0)
lock=threading.Lock()
private='OWNED_ROOT_OAUTH_PRIVATE_CANARY'
def emit(value):
 with lock: print(json.dumps(value),flush=True)
def events():
 while True:
  try:
   os.rename('queued-event.json','reading-event.json')
   with open('reading-event.json') as f: value=json.load(f)
   os.unlink('reading-event.json');emit(value)
  except FileNotFoundError: pass
  time.sleep(0.002)
threading.Thread(target=events,daemon=True).start()
for line in sys.stdin:
 frame=json.loads(line)
 with open('wire.jsonl','a') as f: f.write(json.dumps(frame)+'\n')
 try:
  with open('behavior.json') as f: behavior=json.load(f)
 except FileNotFoundError: behavior={}
 method=frame.get('method')
 if method=='initialize': result={'userAgent':'unqualified-root-owned-fixture'}
 elif method=='configRequirements/read': result={'requirements':{'allowedLoginMethods':behavior.get('allowed',['chatgpt']),'cliAuthCredentialsStore':'auto'}}
 elif method=='account/read': result={'account':None,'requiresOpenaiAuth':True}
 elif method=='account/login/start':
  if frame['params']['type']=='chatgpt': result={'type':'chatgpt','loginId':private,'authUrl':'https://fixture.invalid/'+private}
  else: result={'type':'chatgptDeviceCode','loginId':private,'verificationUrl':'https://fixture.invalid/'+private,'userCode':private}
 elif method=='account/login/cancel':
  if behavior.get('cancel')=='error':
   emit({'id':frame['id'],'error':{'code':-32000,'message':private}});continue
  result={'status':behavior.get('cancel','canceled')}
 else: continue
 emit({'id':frame['id'],'result':result})
"#).unwrap();
            std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
            let mut cfg =
                HostConfig::new(peer, root.join("account"), root.join("probe"), root.clone());
            cfg.allow_unverified_dev = true;
            cfg.wait_limit = Duration::from_secs(2);
            let host = Arc::new(Host::new());
            host.start(&cfg, "owned unqualified Root fixture").unwrap();
            assert_eq!(
                host.snapshot()["supplierStanding"],
                "unverified-development"
            );
            let generation = host.snapshot()["generation"].clone();
            let home = Arc::new(
                HomeSession::new(crate::home_resources::HomeClass::Account, host, Ok(cfg)).unwrap(),
            );
            Self {
                root,
                home,
                generation,
            }
        }
        fn behavior(&self, value: Value) {
            std::fs::write(
                self.root.join("behavior.json"),
                serde_json::to_vec(&value).unwrap(),
            )
            .unwrap();
        }
        fn wire(&self) -> Vec<Value> {
            std::fs::read_to_string(self.root.join("wire.jsonl"))
                .unwrap()
                .lines()
                .map(|line| serde_json::from_str(line).unwrap())
                .collect()
        }
        fn count(&self, method: &str) -> usize {
            self.wire().iter().filter(|f| f["method"] == method).count()
        }
        fn emit(&self, event: Value) {
            let tmp = self.root.join("new-event.json");
            std::fs::write(&tmp, serde_json::to_vec(&event).unwrap()).unwrap();
            std::fs::rename(tmp, self.root.join("queued-event.json")).unwrap();
        }
        fn wait_phase(&self, phase: &str) {
            let deadline = Instant::now() + Duration::from_secs(2);
            while native_oauth_observation(&self.home)["source"]["phase"] != phase {
                assert!(
                    Instant::now() < deadline,
                    "expected phase {phase}: {}",
                    native_oauth_observation(&self.home)
                );
                std::thread::sleep(Duration::from_millis(2));
            }
        }
        fn start(&self, mode: NativeLoginMode) {
            start_native_oauth(&self.home, &self.generation, mode, None, || true).unwrap();
            self.wait_phase("Pending");
        }
        fn safe(&self) {
            for value in [
                self.home.host.snapshot(),
                native_oauth_observation(&self.home),
                self.home.account_view(),
            ] {
                assert!(
                    !serde_json::to_string(&value).unwrap().contains(PRIVATE),
                    "private fixture material leaked into public Root/Host view"
                );
            }
        }
        fn login(&self) -> Arc<crate::hosting::OAuthLogin> {
            self.home.oauth_login.lock().unwrap().clone().unwrap()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = self.home.host.stop("owned Root fixture", "bounded cleanup");
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    fn oauth_root_browser_once_original_cancel_and_safe_observations() {
        let f = Fixture::new();
        f.start(NativeLoginMode::Browser);
        let login = f.login();
        let seen = std::cell::Cell::new(0);
        let delivered = present_original_native_oauth(&f.home, &login, |view, lease| {
            assert!(lease.is_active());
            match view {
                NativeLoginView::Browser { auth_url } => {
                    assert_eq!(auth_url, format!("https://fixture.invalid/{PRIVATE}"))
                }
                _ => panic!("wrong native mode"),
            };
            seen.set(seen.get() + 1);
            NativeLoginPresentation::Presented
        })
        .unwrap();
        assert_eq!(delivered["delivery"]["presentation"], "Presented");
        assert_eq!(seen.get(), 1);
        assert!(
            present_original_native_oauth(&f.home, &login, |_, _| panic!(
                "one-use view must not be repeated"
            ))
            .is_err()
        );
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            true
        );
        let result = cancel_native_oauth(&f.home, &f.generation, None, |safe| {
            assert_eq!(safe["generation"], f.generation);
            assert!(!safe.to_string().contains(PRIVATE));
            true
        })
        .unwrap();
        assert_eq!(result["source"]["cancelStatus"], "canceled");
        assert!(result["state"].as_str().unwrap().contains("signed-out"));
        assert_eq!(f.count("account/login/start"), 1);
        assert_eq!(f.count("account/login/cancel"), 1);
        assert_eq!(
            f.wire()
                .iter()
                .find(|r| r["method"] == "account/login/cancel")
                .unwrap()["params"],
            json!({"loginId":PRIVATE})
        );
        f.safe();
    }
    #[test]
    fn oauth_root_device_dismiss_and_null_account_preserve_notfound_cancel() {
        let f = Fixture::new();
        f.behavior(json!({"cancel":"notFound"}));
        f.start(NativeLoginMode::DeviceCode);
        present_original_native_oauth(&f.home, &f.login(), |view, lease| {
            assert!(lease.is_active());
            match view {
                NativeLoginView::Device {
                    verification_url,
                    user_code,
                } => {
                    assert!(verification_url.contains(PRIVATE));
                    assert_eq!(user_code, PRIVATE)
                }
                _ => panic!("device required"),
            };
            NativeLoginPresentation::Dismissed
        })
        .unwrap();
        read_native_home_access(&f.home, &f.generation).unwrap();
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["phase"],
            "Pending"
        );
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            true
        );
        let result = cancel_native_oauth(&f.home, &f.generation, None, |_| true).unwrap();
        assert_eq!(result["source"]["cancelStatus"], "notFound");
        assert!(result["state"]
            .as_str()
            .unwrap()
            .contains("Codex had no pending sign-in"));
        assert!(
            cancel_native_oauth(&f.home, &f.generation, None, |_| panic!(
                "terminal cannot confirm again"
            ))
            .is_err()
        );
        assert_eq!(f.count("account/login/cancel"), 1);
        f.safe();
    }
    #[test]
    fn oauth_root_device_live_view_is_revoked_by_matched_completion_without_host_lock() {
        let f = Fixture::new();
        f.start(NativeLoginMode::DeviceCode);
        present_original_native_oauth(&f.home,&f.login(),|view,lease|{
            assert!(matches!(view,NativeLoginView::Device{..}));assert!(lease.is_active());
            f.emit(json!({"method":"account/login/completed","params":{"loginId":PRIVATE,"success":true,"error":null}}));
            assert!(lease.revoked(Duration::from_secs(2)),"actual source must revoke active native lease");
            assert!(!lease.is_active());NativeLoginPresentation::Dismissed
        }).unwrap();
        f.wait_phase("CompletedSuccess");
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            false
        );
        assert_eq!(f.count("account/login/cancel"), 0);
        f.safe();
    }
    #[test]
    fn oauth_root_terminal_before_delivery_and_missing_identity_do_not_create_authority() {
        let f = Fixture::new();
        f.start(NativeLoginMode::Browser);
        let position = f.home.host.observe(&f.generation, 0)["position"].as_u64();
        f.emit(json!({"method":"account/login/completed","params":{"loginId":null,"success":true,"error":null}}));
        let deadline = Instant::now() + Duration::from_secs(2);
        while f.home.host.observe(&f.generation, 0)["position"].as_u64() == position {
            assert!(Instant::now() < deadline);
            std::thread::sleep(Duration::from_millis(2));
        }
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["phase"],
            "Pending"
        );
        f.emit(json!({"method":"account/login/completed","params":{"loginId":PRIVATE,"success":false,"error":PRIVATE}}));
        f.wait_phase("CompletedFailure");
        assert!(
            present_original_native_oauth(&f.home, &f.login(), |_, _| panic!(
                "terminal private payload must not be presented"
            ))
            .is_err()
        );
        assert!(
            cancel_native_oauth(&f.home, &f.generation, None, |_| panic!(
                "terminal cannot cancel"
            ))
            .is_err()
        );
        f.safe();
    }
    #[test]
    fn oauth_root_native_cancel_confirmation_preserves_original_dismissal_and_source_loss() {
        let f = Fixture::new();
        f.start(NativeLoginMode::Browser);
        assert!(
            cancel_native_oauth(&f.home, &f.generation, None, |_| false).unwrap()["state"]
                .as_str()
                .unwrap()
                .contains("dismissed")
        );
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            true
        );
        assert_eq!(f.count("account/login/cancel"), 0);
        assert!(cancel_native_oauth(&f.home, &f.generation, None, |_| {
            f.home
                .host
                .stop_scoped(
                    &f.generation,
                    "fixture",
                    "source changed during original native confirmation",
                )
                .unwrap();
            true
        })
        .is_err());
        assert_eq!(f.count("account/login/cancel"), 0);
        f.safe();
    }
    #[test]
    fn oauth_root_original_wrapper_cannot_be_retargeted_by_home_switch() {
        let f = Fixture::new();
        f.start(NativeLoginMode::Browser);
        let captured = f.login();
        let mut config = f.home.host_config.clone().unwrap();
        config.codex_home = f.root.join("key");
        std::fs::create_dir(&config.codex_home).unwrap();
        config.cwd = config.codex_home.clone();
        let other = Arc::new(
            Host::new_with_app_custody(f.home.host.app_runtime_custody().unwrap()).unwrap(),
        );
        struct Guard(Arc<Host>);
        impl Drop for Guard {
            fn drop(&mut self) {
                let _ = self.0.stop("owned fixture", "bounded cleanup");
            }
        }
        let _guard = Guard(other.clone());
        other.start(&config, "owned separate key fixture").unwrap();
        let key = Arc::new(
            HomeSession::new(
                crate::home_resources::HomeClass::ApiKey,
                other.clone(),
                Ok(config.clone()),
            )
            .unwrap(),
        );
        let mut router = HomeRouter::new(f.home.clone()).unwrap();
        router.bind_key(key).unwrap();
        assert!(other.account_oauth_observation(&captured).is_err());
        assert!(other.account_oauth_cancel(&captured).is_err());
        let result = cancel_native_oauth(&f.home, &f.generation, None, |safe| {
            router
                .activate(crate::home_resources::HomeClass::ApiKey)
                .unwrap();
            assert!(Arc::ptr_eq(router.active().source(), &other));
            assert!(Arc::ptr_eq(
                router.for_generation(&f.generation).unwrap().source(),
                &f.home.host
            ));
            assert_eq!(safe["generation"], f.generation);
            assert_ne!(
                safe["generation"]["home"],
                other.snapshot()["generation"]["home"]
            );
            true
        })
        .unwrap();
        assert_eq!(result["source"]["cancelStatus"], "canceled");
        let key_wire = std::fs::read_to_string(config.cwd.join("wire.jsonl")).unwrap();
        assert!(!key_wire.contains("account/login/cancel"));
        assert_eq!(f.count("account/login/cancel"), 1);
        f.safe();
    }
    #[test]
    fn oauth_root_policy_exclusion_native_dismissal_and_cancel_error_stay_unknown_without_retry() {
        let f = Fixture::new();
        assert!(start_native_oauth(
            &f.home,
            &f.generation,
            NativeLoginMode::Browser,
            None,
            || false
        )
        .unwrap()
        .observed["state"]
            .as_str()
            .unwrap()
            .contains("dismissed"));
        assert_eq!(f.count("configRequirements/read"), 0);
        assert_eq!(f.count("account/login/start"), 0);
        f.behavior(json!({"allowed":[]}));
        assert!(start_native_oauth(
            &f.home,
            &f.generation,
            NativeLoginMode::Browser,
            None,
            || true
        )
        .is_err());
        assert_eq!(f.count("account/login/start"), 0);
        f.behavior(json!({"cancel":"error"}));
        f.start(NativeLoginMode::Browser);
        let canceled = cancel_native_oauth(&f.home, &f.generation, None, |_| true);
        assert!(
            canceled.is_err()
                || canceled.as_ref().unwrap()["state"]
                    .as_str()
                    .unwrap()
                    .contains("unknown/error")
        );
        assert!(cancel_native_oauth(&f.home, &f.generation, None, |_| true).is_err());
        assert_eq!(f.count("account/login/cancel"), 1);
        f.safe();
    }
    fn restart_pending(f: &Fixture) -> Value {
        f.start(NativeLoginMode::Browser);
        f.emit(json!({"method":"account/login/completed","params":{"loginId":PRIVATE,"success":true,"error":null}}));
        f.wait_phase("CompletedSuccess");
        f.home
            .host
            .stop_scoped(&f.generation, "fixture", "genuine same-home restart")
            .unwrap();
        f.home
            .host
            .start(
                f.home.host_config.as_ref().unwrap(),
                "owned fixture successor",
            )
            .unwrap();
        let successor = f.home.host.snapshot()["generation"].clone();
        assert_eq!(successor["appSession"], f.generation["appSession"]);
        assert_eq!(successor["home"], f.generation["home"]);
        assert_ne!(successor["spawnCounter"], f.generation["spawnCounter"]);
        start_native_oauth(
            &f.home,
            &successor,
            NativeLoginMode::DeviceCode,
            None,
            || true,
        )
        .unwrap();
        f.wait_phase("Pending");
        successor
    }
    #[test]
    fn oauth_root_or1_stale_same_home_present_does_not_consume_successor() {
        let f = Fixture::new();
        let successor = restart_pending(&f);
        let router = HomeRouter::new(f.home.clone()).unwrap();
        let selected = router.for_generation(&f.generation).unwrap();
        let presented = std::cell::Cell::new(0);
        let result = present_requested_native_oauth(&selected, &f.generation, None, |_, _, _| {
            presented.set(presented.get() + 1);
            NativeLoginPresentation::Presented
        });
        assert_eq!(
            presented.get(),
            0,
            "stale same-home request presented replacement sign-in"
        );
        assert!(result.is_err());
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["generation"],
            successor
        );
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["presentationAvailable"],
            true
        );
        present_requested_native_oauth(&selected, &successor, None, |view, lease, current| {
            assert!(current());
            assert!(lease.is_active());
            assert!(matches!(view, NativeLoginView::Device { .. }));
            NativeLoginPresentation::Dismissed
        })
        .unwrap();
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            true
        );
        f.safe();
    }
    #[test]
    fn oauth_root_or1_stale_same_home_cancel_does_not_confirm_or_dispatch_successor() {
        let f = Fixture::new();
        let successor = restart_pending(&f);
        let router = HomeRouter::new(f.home.clone()).unwrap();
        let selected = router.for_generation(&f.generation).unwrap();
        let confirmed = std::cell::Cell::new(0);
        let result = cancel_native_oauth(&selected, &f.generation, None, |_| {
            confirmed.set(confirmed.get() + 1);
            true
        });
        assert_eq!(
            confirmed.get(),
            0,
            "stale same-home request confirmed replacement sign-in cancel"
        );
        assert!(result.is_err());
        assert_eq!(f.count("account/login/cancel"), 0);
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["generation"],
            successor
        );
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            true
        );
        let inverse = cancel_native_oauth(&selected, &successor, None, |safe| {
            assert_eq!(safe["generation"], successor);
            true
        })
        .unwrap();
        assert_eq!(inverse["source"]["cancelStatus"], "canceled");
        assert_eq!(f.count("account/login/cancel"), 1);
        f.safe();
    }
    #[test]
    fn oauth_root_or1_old_start_auto_continuation_does_not_present_same_g_replacement() {
        let f = Fixture::new();
        let first = start_native_oauth(
            &f.home,
            &f.generation,
            NativeLoginMode::Browser,
            None,
            || true,
        )
        .unwrap();
        f.emit(json!({"method":"account/login/completed","params":{"loginId":PRIVATE,"success":true,"error":null}}));
        f.wait_phase("CompletedSuccess");
        let second = start_native_oauth(
            &f.home,
            &f.generation,
            NativeLoginMode::DeviceCode,
            None,
            || true,
        )
        .unwrap();
        assert_ne!(
            first.observed["source"]["requestIdentity"],
            second.observed["source"]["requestIdentity"]
        );
        let presented = std::cell::Cell::new(0);
        let _result = automatic_native_oauth_presentation_with(&f.home, first, None, |_, _, _| {
            presented.set(presented.get() + 1);
            NativeLoginPresentation::Presented
        });
        assert_eq!(
            presented.get(),
            0,
            "old start act presented replacement sign-in under same full generation"
        );
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["presentationAvailable"],
            true
        );
        assert_eq!(f.count("account/login/cancel"), 0);
        automatic_native_oauth_presentation_with(&f.home, second, None, |view, lease, current| {
            assert!(current());
            assert!(lease.is_active());
            assert!(matches!(view, NativeLoginView::Device { .. }));
            NativeLoginPresentation::Dismissed
        })
        .unwrap();
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            true
        );
        f.safe();
    }
    fn physical_set(f: &Fixture) -> HomeBootstrapSet {
        let data = f.root.join("app-data");
        std::fs::create_dir(&data).unwrap();
        freeze_root_home_descriptors(
            &data,
            f.home.host_config.as_ref().unwrap(),
            None,
            [None, None, None],
        )
        .unwrap()
    }
    fn redirect_account(f: &Fixture) {
        let cfg = f.home.host_config.as_ref().unwrap();
        std::fs::rename(&cfg.codex_home, f.root.join("saved-account")).unwrap();
        std::os::unix::fs::symlink(&cfg.probe_home, &cfg.codex_home).unwrap();
    }
    fn restore_account(f: &Fixture) {
        let path = &f.home.host_config.as_ref().unwrap().codex_home;
        std::fs::remove_file(path).unwrap();
        std::fs::rename(f.root.join("saved-account"), path).unwrap();
    }
    #[test]
    fn oauth_root_physical_start_rechecks_after_native_confirmation() {
        let f = Fixture::new();
        let basis = physical_set(&f);
        assert!(start_native_oauth(
            &f.home,
            &f.generation,
            NativeLoginMode::Browser,
            Some(&basis),
            || {
                redirect_account(&f);
                true
            }
        )
        .is_err());
        assert_eq!(f.count("account/login/start"), 0);
        assert_eq!(f.count("configRequirements/read"), 0);
        restore_account(&f);
        f.safe();
    }
    #[test]
    fn oauth_root_physical_cancel_rechecks_without_ending_original_pending_control() {
        let f = Fixture::new();
        let basis = physical_set(&f);
        f.start(NativeLoginMode::Browser);
        assert!(
            cancel_native_oauth(&f.home, &f.generation, Some(&basis), |_| {
                redirect_account(&f);
                true
            })
            .is_err()
        );
        assert_eq!(f.count("account/login/cancel"), 0);
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            true
        );
        restore_account(&f);
        let result = cancel_native_oauth(&f.home, &f.generation, Some(&basis), |_| true).unwrap();
        assert_eq!(result["source"]["cancelStatus"], "canceled");
        assert_eq!(f.count("account/login/cancel"), 1);
        f.safe();
    }
    #[test]
    fn oauth_root_physical_display_current_callback_refuses_changed_metadata() {
        let f = Fixture::new();
        let basis = physical_set(&f);
        f.start(NativeLoginMode::DeviceCode);
        let delivered = present_requested_native_oauth(
            &f.home,
            &f.generation,
            Some(&basis),
            |_, lease, current| {
                assert!(current());
                redirect_account(&f);
                assert!(!current());
                assert!(lease.is_active());
                NativeLoginPresentation::Dismissed
            },
        );
        assert!(delivered.is_err());
        assert_eq!(
            native_oauth_observation(&f.home)["source"]["cancelAvailable"],
            true
        );
        restore_account(&f);
        f.safe();
    }
}

// Actual Root-held workflow selection/review/registration state. Public summaries
// are observations; none can construct a closed selection, A15 event or receipt.
pub(crate) struct WorkflowLibraryContext {
    pub reference: String,
    pub root: std::path::PathBuf,
    pub origin: String,
    pub source_root: String,
    pub owner: std::sync::Mutex<crate::workflow_workspace::registration::LibraryOwner>,
    pub control: std::sync::Arc<std::sync::Mutex<Option<crate::act_control::ActControl>>>,
}
pub(crate) struct WorkflowReviewContext {
    pub reference: String,
    pub library: std::sync::Arc<WorkflowLibraryContext>,
    pub home: std::sync::Arc<HomeSession>,
    pub home_context: Value,
    pub review: Option<crate::workflow_workspace::registration::ReviewSession>,
    pub offer: Option<crate::act_control::A15OfferRef>,
    pub attempted_native: bool,
    pub transaction: Option<crate::workflow_workspace::registration::HotRegistrationAttempt>,
    pub status: Value,
    pub registered:
        std::collections::HashMap<String, crate::workflow_workspace::RegisteredRevision>,
}
struct WorkflowSelectionState {
    reference: String,
    selection: crate::workflow_workspace::Selection,
    package: std::path::PathBuf,
    /// The person's original selection time (WR selection_record.selected_at).
    selected_at: String,
}
/// WR TT-1 (SETTLED) and TX-1: only registered (LS-1), bundled (LS-5), host-listed
/// (LS-6) or shipped-held (LS-8) revisions are composed and run. The App holds no
/// bundled/host/shipped capability yet, so only an actual hot registered revision
/// runs here. Development evidence is never laundered into a selection (WP-6; CI-18).
fn run_admission(selection: &crate::workflow_workspace::Selection) -> Result<(), String> {
    match selection.admission() {
        crate::workflow_workspace::SelectionAdmission::RegisteredRevision => Ok(()),
        other => Err(format!("Selected workflow is not runnable ({}): WR TT-1/TX-1 compose and run only registered (LS-1), bundled (LS-5), host-listed (LS-6) or shipped-held (LS-8) revisions. Register a reviewed copy (draft, review, A15) and select that registered revision. Nothing prepared, recorded or sent (CONTRACT_ISSUES CI-18).", other.standing())),
    }
}
pub(crate) struct WorkflowRootSession {
    selected: Option<WorkflowSelectionState>,
    pub libraries: std::collections::HashMap<String, std::sync::Arc<WorkflowLibraryContext>>,
    pub active_library: Option<String>,
    pub reviews:
        std::collections::HashMap<String, std::sync::Arc<std::sync::Mutex<WorkflowReviewContext>>>,
    pub active_review: Option<String>,
    pub runs: std::collections::HashMap<String, std::sync::Arc<std::sync::Mutex<WorkflowRun>>>,
    /// Runs prepared in this process per (home, conversation), in order (RE-7).
    conversations: std::collections::HashMap<(String, String), Vec<String>>,
    /// Last durable reopen of the explicit project's records (display only).
    reopened: Option<Value>,
}
impl Default for WorkflowRootSession {
    fn default() -> Self {
        Self {
            selected: None,
            libraries: Default::default(),
            active_library: None,
            reviews: Default::default(),
            active_review: None,
            runs: Default::default(),
            conversations: Default::default(),
            reopened: None,
        }
    }
}
impl WorkflowRootSession {
    pub fn snapshot(&self) -> Value {
        json!({"selection":self.selected.as_ref().map(|s|json!({"reference":s.reference,"identity":s.selection.identity(),"standing":s.selection.admission().standing(),"package":crate::attachments::native_path_identity(&s.package),"currentLimit":s.selection.verify_store(&s.package).err(),"selectedAt":s.selected_at,"runnable":run_admission(&s.selection).is_ok(),"runLimit":run_admission(&s.selection).err()})),
            "libraries":self.libraries.values().map(|l|json!({"reference":l.reference,"root":crate::attachments::native_path_identity(&l.root),"origin":l.origin,"sourceRoot":l.source_root})).collect::<Vec<_>>(),"activeLibrary":self.active_library,"activeReview":self.active_review,
            "reviews":self.reviews.iter().map(|(id,review)|match review.try_lock(){Ok(review)=>json!({"reference":id,"status":review.status}),Err(_)=>json!({"reference":id,"state":"original native review interaction pending"})}).collect::<Vec<_>>(),
            "runs":self.runs.iter().map(|(id,run)|match run.try_lock(){Ok(run)=>run.view(id),Err(_)=>json!({"reference":id,"state":"original run operation pending"})}).collect::<Vec<_>>(),
            "reopened":self.reopened,
            "limit":"closed development/actual hot registrations only; development selections are shown, never run (TT-1/TX-1); runs open and end only by their recorded lifecycle; compatibility is advisory; no cold file authority or model adoption claim"})
    }
    pub fn select_development_copy(&mut self, path: std::path::PathBuf) -> Result<Value, String> {
        let catalog = crate::workflow_workspace::development_catalog::DevelopmentCatalog::load()?;
        let held = catalog.recognize_holding_copy(&path)?;
        held.verify_current()?;
        self.selected = Some(WorkflowSelectionState {
            reference: crate::util::opaque_id("workflow-selection:")?,
            selection: held.selection().clone(),
            package: path,
            selected_at: crate::util::now_rfc3339(),
        });
        Ok(self.snapshot())
    }
    pub fn open_library(
        &mut self,
        root: std::path::PathBuf,
        origin: &str,
        workspace: Option<&std::path::Path>,
        workspace_control: std::sync::Arc<std::sync::Mutex<Option<crate::act_control::ActControl>>>,
    ) -> Result<String, String> {
        crate::storage::check_path(&root)?;
        if !root.is_absolute() || !root.is_dir() {
            return Err("Native-picked existing physical library root required".into());
        }
        if let Some(existing) = self.libraries.values().find(|l| l.root == root) {
            if existing.origin != origin {
                return Err("Actual library root already opened with a different source origin; no reinterpretation".into());
            }
            let id = existing.reference.clone();
            self.active_library = Some(id.clone());
            return Ok(id);
        }
        let source_root=root.to_str().ok_or("Native library root is not Unicode; source-qualified identity cannot be encoded losslessly")?.to_owned();
        let control=match workspace {
            Some(ws) if ws==root.as_path()=>workspace_control,
            Some(ws) if std::fs::canonicalize(ws).ok().as_ref()==Some(&root)=>return Err("Existing workspace writer uses an alias of this library root; no second control or silent relocation".into()),
            _=>std::sync::Arc::new(std::sync::Mutex::new(Some(crate::act_control::ActControl::new(&root)))),
        };
        let owner = crate::workflow_workspace::registration::LibraryOwner::open(
            root.clone(),
            origin,
            &source_root,
        )?;
        let id = crate::util::opaque_id("workflow-library:")?;
        self.libraries.insert(
            id.clone(),
            std::sync::Arc::new(WorkflowLibraryContext {
                reference: id.clone(),
                root,
                origin: origin.into(),
                source_root,
                owner: std::sync::Mutex::new(owner),
                control,
            }),
        );
        self.active_library = Some(id.clone());
        Ok(id)
    }
    pub fn active_library(&self) -> Result<std::sync::Arc<WorkflowLibraryContext>, String> {
        self.active_library
            .as_ref()
            .and_then(|r| self.libraries.get(r))
            .cloned()
            .ok_or("No actual native library context selected".into())
    }
    pub fn select_hot_registered_copy(
        &mut self,
        review_ref: &str,
        revision: &str,
        path: std::path::PathBuf,
    ) -> Result<Value, String> {
        let review = self
            .reviews
            .get(review_ref)
            .cloned()
            .ok_or("Original hot review not retained; ledger/JSON cannot select")?;
        let review = review.try_lock().map_err(|_| "Original review owner busy/unavailable; selection pending, no transfer")?;
        let actual = review
            .registered
            .get(revision)
            .ok_or("Actual hot registered revision unavailable")?;
        let selection = actual.select();
        selection.verify_store(&path)?;
        self.selected = Some(WorkflowSelectionState {
            reference: crate::util::opaque_id("workflow-selection:")?,
            selection,
            package: path,
            selected_at: crate::util::now_rfc3339(),
        });
        drop(review);
        Ok(self.snapshot())
    }
    pub fn create_selected_draft(&mut self, name: &str) -> Result<Value, String> {
        if !crate::workflow_workspace::valid_name(name) {
            return Err("Invalid workflow draft name".into());
        }
        let selected = self
            .selected
            .as_ref()
            .ok_or("Select an actual closed workflow holding copy first")?;
        selected.selection.verify_store(&selected.package)?;
        let library = self.active_library()?;
        let mut owner = library.owner.try_lock().map_err(|_| "Original library owner busy/unavailable; draft operation pending")?;
        let target = library.root.join(".chirality/workflow-drafts").join(name);
        crate::storage::check_path(&target)?;
        if target.exists() {
            return Err("Existing draft preserved; no overwrite".into());
        }
        std::fs::create_dir_all(&target).map_err(|e| e.to_string())?;
        for (relative, bytes) in selected.selection.snapshot().files() {
            let path = target.join(relative);
            crate::storage::check_path(&path)?;
            if let Some(parent) = path.parent() {
                std::fs::create_dir_all(parent).map_err(|e| e.to_string())?;
            }
            std::fs::write(path, bytes).map_err(|e| e.to_string())?;
        }
        owner.record_base(name, &selected.selection)?;
        Ok(
            json!({"state":"draft copied from actual closed selection","library":library.reference,"name":name,"base":selected.selection.identity(),"registration":"not captured/registered; edit then Review"}),
        )
    }
    pub fn begin_review(
        &mut self,
        home: std::sync::Arc<HomeSession>,
        context: Value,
        names: Vec<String>,
        in_place: bool,
    ) -> Result<Value, String> {
        let library = self.active_library()?;
        // The caller holds Root. Never wait for an owner retained by native
        // interaction, whose observer must acquire Root before/after the dialog.
        let mut control_guard = library.control.try_lock().map_err(|_| "Original capture owner busy/unavailable; review pending, no capture")?;
        let control = control_guard.as_mut().ok_or("Actual owning library control unavailable")?;
        let owner = library.owner.try_lock().map_err(|_| "Original library owner busy/unavailable; review pending")?;
        let review = if in_place {
            owner.review_in_place(&names)?
        } else {
            if names.len() != 1 {
                return Err("One draft name required".into());
            }
            let revision=owner.listed_draft_revision(&names[0])?;
            owner.review_draft(&names[0],&revision)?
        };
        let view = review.current()?;
        let reference = view.review_ref().to_owned();
        let presentation = view.review_presentation().clone();
        let offer = control.compose_a15(&view)?;
        drop(owner);
        drop(control_guard);
        self.reviews.insert(reference.clone(),std::sync::Arc::new(std::sync::Mutex::new(WorkflowReviewContext{reference:reference.clone(),library,home,home_context:context,review:Some(review),offer:Some(offer),attempted_native:false,transaction:None,registered:Default::default(),status:json!({"state":"reviewed; native A15 not captured","presentation":presentation})})));
        self.active_review = Some(reference);
        Ok(self.snapshot())
    }
    /// Prepares one run's WR records for the explicit App project. Nothing is
    /// recorded or sent here: publication happens before dispatch in `send`.
    pub fn prepare_run(
        &mut self,
        home: std::sync::Arc<HomeSession>,
        generation: &Value,
        thread: &str,
        person_text: String,
        project: Option<&std::path::Path>,
    ) -> Result<String, String> {
        current_conversation(&home.host.snapshot(), generation, thread)?;
        let selected = self
            .selected
            .as_ref()
            .ok_or("No actual closed workflow selection")?;
        run_admission(&selected.selection)?;
        // WP-1: only the explicitly opened App project owns WR records; no
        // source-root, library, cwd or user-data fallback.
        let project_root = project
            .ok_or("No explicit App project (CHIRALITY_WORKSPACE): WR recording unavailable, so the workflow run is not prepared or sent; no fallback store")?
            .to_path_buf();
        let records = crate::workflow_workspace::publication::ProjectRecords::open(&project_root)
            .map_err(|e| format!("Explicit App project not openable for WR records ({e}); nothing prepared or sent; no fallback store"))?;
        selected.selection.verify_store(&selected.package)?;
        let home_key = generation["home"]
            .as_str()
            .ok_or("Native home absent")?
            .to_owned();
        // RE-7 / CH-1: one live run per conversation. A run reopened from the
        // project's records without run_ended is interrupted and still live.
        let prior = self.conversation_prior(&home_key, thread, &records)?;
        // App-local opaque run reference until EXEC supplies its lifecycle identity;
        // the `run:` form is RS $defs/runId, so R3 can be recorded under it.
        let run = crate::util::opaque_id("run:workflow:")?;
        let scope = crate::workflow_workspace::RunScope {
            run: run.clone(),
            conversation: thread.into(),
            home: home_key.clone(),
            generation: generation.clone(),
            source_root: selected.selection.identity().source_root.clone(),
            holding_library: selected
                .package
                .parent()
                .ok_or("Holding library path unavailable")?
                .to_str()
                .ok_or("Holding library path is not Unicode")?
                .into(),
            selection_ref: selected.reference.clone(),
            revision_store: selected.package.clone(),
        };
        let prepared = crate::workflow_workspace::PreparedRunText::start(
            &selected.selection,
            scope,
            "selected native workflow holding copy",
            prior.as_ref().map(|(_, end)| end),
        )?;
        let publication = crate::workflow_workspace::publication::PreparedRunPublication::new(
            &records,
            &selected.selection,
            prepared,
            WR_WRITER,
            &selected.selected_at,
            &crate::util::now_rfc3339(),
        )?;
        let client_id = crate::util::opaque_id("workflow-message:")?;
        let mut workflow_run = WorkflowRun {
            home,
            project: records,
            project_root,
            selection: selected.selection.clone(),
            publication,
            published: None,
            publication_failure: None,
            person_text,
            client_id,
            source: None,
            attempted: false,
            turn_id: None,
            status: json!({"state":"prepared; WR records pending; not sent","recorded":false,"sent":false,"supplied":"not supplied","adoption":"unknown","runStanding":"not opened: a run opens when its start turn is observed"}),
            supply: Value::Null,
            checks: Vec::new(),
            follows: prior.map(|(run, _)| run),
            lifecycle: RunLifecycle::Prepared,
            entries: Vec::new(),
            end: None,
            notice: NoticeState::None,
            notice_checks: Vec::new(),
            compatibility: Vec::new(),
        };
        // EXEC §3.1 CK-1: the selection is now bound to this conversation for a run.
        workflow_run.evaluate_compatibility(crate::execution_compatibility::report::Occasion::Selection);
        self.runs.insert(
            run.clone(),
            std::sync::Arc::new(std::sync::Mutex::new(workflow_run)),
        );
        self.conversations
            .entry((home_key, thread.to_owned()))
            .or_default()
            .push(run.clone());
        Ok(run)
    }
    /// CH-1/RE-7 for a new start in this conversation: refuses while a run is
    /// live (hot, or interrupted in the record), and returns the run this one
    /// follows with its owner end (the chain line, `follows`, `prior_run`).
    fn conversation_prior(
        &self,
        home: &str,
        thread: &str,
        records: &crate::workflow_workspace::publication::ProjectRecords,
    ) -> Result<Option<(String, crate::workflow_workspace::OwnerRunEnd)>, String> {
        let mut prior = None;
        let hot = self
            .conversations
            .get(&(home.to_owned(), thread.to_owned()))
            .cloned()
            .unwrap_or_default();
        for reference in &hot {
            let run = self.runs.get(reference).ok_or("conversation run index inconsistent")?;
            let run = run.try_lock().map_err(|_| format!("Run {reference} has an operation pending in this conversation; whether it is live cannot be established now. Nothing prepared"))?;
            match &run.lifecycle {
                RunLifecycle::Open => return Err(format!("A workflow run is live in this conversation ({reference}). End it first, or confirm \"End and start\" (RE-7, CH-1). Nothing prepared")),
                RunLifecycle::Ended => {
                    if let Some(end) = &run.end {
                        prior = Some((reference.clone(), end.clone()));
                    }
                }
                RunLifecycle::Prepared | RunLifecycle::StartNotConfirmed => {}
            }
        }
        let reading = crate::records::supply::read_project_runs(records, &[]);
        if let Some(cold) = reading
            .live_in(thread)
            .into_iter()
            .find(|r| !hot.contains(&r.run))
        {
            return Err(format!("A workflow run recorded in this conversation is still open (interrupted, no run_ended): {}. End it first (RE-4, RE-7). Nothing prepared", cold.run));
        }
        Ok(prior)
    }
    fn conversation_run(
        &self,
        reference: &str,
    ) -> Result<std::sync::Arc<std::sync::Mutex<WorkflowRun>>, String> {
        self.runs
            .get(reference)
            .cloned()
            .ok_or_else(|| format!("Actual run {reference} unavailable in this process"))
    }
    /// The ended run in this conversation whose end notice the next ordinary turn
    /// must carry (TX-5), if any.
    pub fn pending_notice_for(
        &self,
        home: &str,
        thread: &str,
    ) -> Result<Option<std::sync::Arc<std::sync::Mutex<WorkflowRun>>>, String> {
        for reference in self
            .conversations
            .get(&(home.to_owned(), thread.to_owned()))
            .into_iter()
            .flatten()
        {
            let run = self.conversation_run(reference)?;
            let pending = {
                let guard = run.try_lock().map_err(|_| "A run operation is pending in this conversation; the end-notice state cannot be established now; nothing sent")?;
                guard.notice.awaiting_turn()
            };
            if pending {
                return Ok(Some(run));
            }
        }
        Ok(None)
    }
    /// Runs in the conversation of `run` that a successor start supersedes (their
    /// pending end notice is replaced by the successor's chain line, TX-5).
    fn superseded_notices(&self, run: &str) -> Vec<std::sync::Arc<std::sync::Mutex<WorkflowRun>>> {
        self.conversations
            .values()
            .find(|runs| runs.iter().any(|r| r == run))
            .into_iter()
            .flatten()
            .filter(|r| r.as_str() != run)
            .filter_map(|r| self.runs.get(r).cloned())
            .collect()
    }
    /// Durable reopen for display: the explicit project's records only.
    pub fn reopen(&mut self, project: &std::path::Path, restart_events: &[Value]) -> Result<Value, String> {
        let records = crate::workflow_workspace::publication::ProjectRecords::open(project)?;
        let view = crate::records::supply::read_project_runs(&records, restart_events).view();
        self.reopened = Some(view.clone());
        Ok(view)
    }
}
/// Starts a prepared run (CH-1 rechecked at dispatch). The Root lock is not held
/// across the native wait. A successor start supersedes the predecessor's pending
/// end notice: its chain line says the same (TX-5).
pub(crate) fn start_workflow_run(
    root: &std::sync::Mutex<WorkflowRootSession>,
    reference: &str,
) -> Result<Value, String> {
    let (run, others) = {
        let root = root.lock().unwrap();
        let run = root.conversation_run(reference)?;
        let others = root.superseded_notices(reference);
        for other in &others {
            let other = other.try_lock().map_err(|_| "Another run operation is pending in this conversation; whether a run is live cannot be established; nothing sent")?;
            if other.lifecycle == RunLifecycle::Open {
                return Err("A workflow run is live in this conversation; end it first (RE-7, CH-1). Nothing sent".into());
            }
        }
        (run, others)
    };
    let mut run = run.try_lock().map_err(|_| "Original run operation pending")?;
    let result = run.send();
    if run.attempted {
        for other in others {
            if let Ok(mut other) = other.try_lock() {
                other.notice.supersede(reference);
            }
        }
    }
    result
}
/// SQ-END / TX-5: the person's next ordinary turn in a conversation whose run
/// ended without a successor carries the end notice first, exactly once. Returns
/// None when no notice is pending (ordinary sending applies unchanged).
pub(crate) fn send_with_pending_notice(
    root: &std::sync::Mutex<WorkflowRootSession>,
    generation: &Value,
    thread: &str,
    person_text: &str,
) -> Option<Result<Value, String>> {
    let home = generation["home"].as_str()?.to_owned();
    let pending = match root.lock().unwrap().pending_notice_for(&home, thread) {
        Ok(p) => p?,
        Err(e) => return Some(Err(e)),
    };
    let mut run = match pending.try_lock() {
        Ok(run) => run,
        Err(_) => return Some(Err("Original run operation pending; nothing sent".into())),
    };
    Some(run.send_end_notice(generation, person_text))
}
/// RS run_ended cause for the person's end (WR CH-1/CH-2 wording; R20-11 (4)).
fn run_end_cause(reason: &crate::workflow_workspace::RunEndReason) -> String {
    match reason {
        crate::workflow_workspace::RunEndReason::ByPerson => "ended by the person".into(),
        crate::workflow_workspace::RunEndReason::Completed => "completed".into(),
        crate::workflow_workspace::RunEndReason::ToStart(name)
            if crate::workflow_workspace::valid_name(name) =>
        {
            format!("ended to start {name}")
        }
        _ => "invalid".into(),
    }
}
/// Runtime lifecycle of one App run (EXEC AE-7, RE-4, RE-6, RE-7).
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum RunLifecycle {
    /// Prepared, not sent. Not a run yet.
    Prepared,
    /// The start turn was refused or its outcome is unknown (A-3): the run is
    /// not opened and is not live.
    StartNotConfirmed,
    /// `run_opened`: the start turn was observed. Only an explicit end ends it.
    Open,
    /// The person's explicit end (DEF-4), with its cause.
    Ended,
}
/// TX-5 end notice for a run ended with no successor.
enum NoticeState {
    None,
    /// The next ordinary turn in the conversation must carry it.
    AwaitingTurn,
    /// Publication failed before send; the original pending bytes are kept.
    Prepared(crate::workflow_workspace::publication::PreparedEndPublication),
    /// Dispatched once (never again), with its outcome.
    Sent {
        published: crate::workflow_workspace::publication::PublishedEndNotice,
        client_id: String,
        turn: Option<String>,
        generation: Value,
        outcome: Value,
    },
    /// A successor run started in the conversation; its chain line said it.
    Superseded(String),
    /// The run ended to start a successor; the chain line carries the end.
    ByChain,
}
impl NoticeState {
    fn awaiting_turn(&self) -> bool {
        matches!(self, Self::AwaitingTurn | Self::Prepared(_))
    }
    fn supersede(&mut self, successor: &str) {
        if self.awaiting_turn() {
            *self = Self::Superseded(successor.to_owned());
        }
    }
    fn view(&self) -> Value {
        match self {
            Self::None => Value::Null,
            Self::AwaitingTurn => json!({"state":"pending: the next ordinary turn in this conversation carries it"}),
            Self::Prepared(p) => json!({"state":"pending: publication failed; nothing sent; retried with the next turn","record":p.reference()}),
            Self::Sent{published,turn,outcome,..} => json!({"state":"sent once with the next ordinary turn","record":published.run_text_record().reference(),"turn":turn,"outcome":outcome}),
            Self::Superseded(run) => json!({"state":"not sent: the successor run's chain line said the run ended","successor":run}),
            Self::ByChain => json!({"state":"not composed: ended to start a successor; its chain line carries the end"}),
        }
    }
}
/// Advisory compatibility evaluation kept with its occasion and basis (EXEC §3).
struct CompatibilitySlot {
    occasion: &'static str,
    basis: crate::execution_compatibility::report::Basis,
    result: Result<crate::execution_compatibility::report::Evaluation, String>,
}
/// Supplier writer label carried in WR envelopes.
const WR_WRITER: &str = "app-writer:local";
/// One native read's check: original pending record, its publication and its R3.
struct WorkflowCheckSlot {
    pending: crate::workflow_workspace::publication::PendingSupplyCheck,
    published: Option<crate::workflow_workspace::publication::PublishedSupplyCheck>,
    publication_failure: Option<String>,
    r3: WorkflowR3,
}
enum WorkflowR3 {
    /// The check is not yet published; R3 needs resolvable supplier records.
    AwaitingCheck,
    /// R3 could not be prepared from the resolved joins (no entry possible).
    Unavailable(String),
    Pending(crate::records::supply::PendingSuppliedGuidance),
    Recorded(Value),
}
impl WorkflowCheckSlot {
    /// Publish the original check bytes if needed, then prepare/append R3.
    /// Never re-reads native history and never sends.
    /// `record_ready`: the lifecycle entry this R3 follows in the run log is
    /// written (run_opened for the start text, run_ended for the end notice).
    fn advance(
        &mut self,
        project: &crate::workflow_workspace::publication::ProjectRecords,
        record_ready: bool,
    ) {
        if self.published.is_none() {
            match self.pending.publish(project) {
                Ok(p) => {
                    self.published = Some(p);
                    self.publication_failure = None;
                }
                Err(e) => {
                    self.publication_failure = Some(e);
                    return;
                }
            }
        }
        let published = self.published.as_ref().unwrap();
        if matches!(self.r3, WorkflowR3::AwaitingCheck) {
            self.r3 = match crate::records::supply::prepare_live(project, published) {
                Ok(p) => WorkflowR3::Pending(p),
                Err(e) => WorkflowR3::Unavailable(e.to_string()),
            };
        }
        if !record_ready {
            return;
        }
        if let WorkflowR3::Pending(pending) = &mut self.r3 {
            if let Ok(entry) = crate::records::supply::append_live(project, published, pending) {
                self.r3 = WorkflowR3::Recorded(entry);
            }
        }
    }
    fn view(&self) -> Value {
        let body = self.pending.body();
        let r3 = match &self.r3 {
            WorkflowR3::AwaitingCheck => json!({"state":"not recorded; awaits the published check"}),
            WorkflowR3::Unavailable(e) => json!({"state":"unavailable","limit":e}),
            WorkflowR3::Pending(p) => json!({"state":"pending write; missing in record","recordId":p.record_id(),"limit":p.failure(),"retry":"retry writes the same identity and observation time"}),
            WorkflowR3::Recorded(entry) => json!({"state":"recorded","recordId":entry["recordId"],"observedAt":entry["observedAt"],"writtenAt":entry["writtenAt"],"supplyCheck":entry["body"]["supplyCheck"],"adoption":entry["body"]["adoption"]}),
        };
        json!({"reference":self.pending.reference(),"check":body["check"],"state":body["state"],"supplyReading":if body["state"]=="verified"{"supplied"}else{"supplied — not verified"},"readAt":body["read_at"],"turn":body["turn"],"locatedBy":body["located_by"],
            "published":self.published.is_some(),"publicationLimit":self.publication_failure,"r3":r3,"adoption":"unknown"})
    }
}
pub(crate) struct WorkflowRun {
    pub home: std::sync::Arc<HomeSession>,
    project: crate::workflow_workspace::publication::ProjectRecords,
    project_root: std::path::PathBuf,
    publication: crate::workflow_workspace::publication::PreparedRunPublication,
    published: Option<crate::workflow_workspace::publication::PublishedRunText>,
    publication_failure: Option<Value>,
    pub person_text: String,
    pub client_id: String,
    pub source: Option<crate::hosting::SourceRequest>,
    pub attempted: bool,
    pub turn_id: Option<String>,
    pub status: Value,
    pub supply: Value,
    checks: Vec<WorkflowCheckSlot>,
    selection: crate::workflow_workspace::Selection,
    /// RS `run_opened.follows`: the run this one follows in the conversation.
    follows: Option<String>,
    pub(crate) lifecycle: RunLifecycle,
    /// Ordered RS lifecycle entries for this run's log (W-2 order kept).
    entries: Vec<crate::records::supply::PendingRunEntry>,
    end: Option<crate::workflow_workspace::OwnerRunEnd>,
    notice: NoticeState,
    notice_checks: Vec<WorkflowCheckSlot>,
    compatibility: Vec<CompatibilitySlot>,
}
impl WorkflowReviewContext {
    pub fn accept_result(
        &mut self,
        result: crate::act_control::HotA15Result,
    ) -> Result<(), String> {
        match result {
            crate::act_control::HotA15Result::Recorded(receipt) => {
                self.status = json!({"state":"actual hot A15 recorded; registration handoff pending/not completed"});
                let session = self
                    .review
                    .take()
                    .ok_or("Original owner review already transferred")?;
                self.transaction = Some(session.begin_hot_registration(receipt)?);
                self.status =
                    json!({"state":"actual hot A15 recorded; registration attempt retained"});
                self.advance();
            }
            crate::act_control::HotA15Result::RecordPending { capture_id, reason } => {
                self.status = json!({"state":"actual captured A15 record pending","captureId":capture_id,"reason":reason,"registration":"not authorized until actual hot receipt"})
            }
            crate::act_control::HotA15Result::AlreadyTransferred {
                capture_id,
                record_id,
            } => {
                self.status = json!({"state":"original receipt already transferred; no second transaction","captureId":capture_id,"recordId":record_id})
            }
        }
        Ok(())
    }
    pub fn advance(&mut self) {
        if let Some(attempt) = self.transaction.as_mut() {
            let outcomes = attempt.advance();
            for outcome in &outcomes {
                if let crate::workflow_workspace::registration::EntryOutcome::Registered {
                    revision,
                    ..
                } = outcome
                {
                    self.registered
                        .insert(revision.identity().revision.clone(), revision.clone());
                }
            }
            self.status = json!({"state":"original registration attempt advanced","entries":outcomes.iter().map(|o|match o{
                crate::workflow_workspace::registration::EntryOutcome::Registered{revision,publication}=>json!({"state":"registered","identity":revision.identity(),"actRef":revision.act_ref(),"publication":format!("{publication:?}")}),
                crate::workflow_workspace::registration::EntryOutcome::NotCompleted{identity,reason}=>json!({"state":"not completed","identity":identity,"reason":reason}),
                crate::workflow_workspace::registration::EntryOutcome::Pending{identity,reason}=>json!({"state":"pending; not registered","identity":identity,"reason":reason}),
            }).collect::<Vec<_>>()});
        }
    }
}
impl WorkflowRun {
    pub fn prepared(&self) -> &crate::workflow_workspace::PreparedRunText {
        self.publication.prepared()
    }
    fn record_state(&self, reference: &str) -> Value {
        match self.project.resolve(reference) {
            Ok(_) => json!({"reference":reference,"state":"recorded (resolves)"}),
            Err(crate::workflow_workspace::publication::ResolutionError::Missing) => {
                json!({"reference":reference,"state":"not recorded"})
            }
            Err(e) => json!({"reference":reference,"state":"not confirmed","limit":format!("{e:?}")}),
        }
    }
    pub fn view(&self, reference: &str) -> Value {
        let publication = match &self.published {
            Some(p) => json!({"state":"selection and run_text recorded before send","selection":p.selection_record().reference(),"runText":p.run_text_record().reference()}),
            None => json!({"state":"pending; not recorded","selection":self.publication.selection_reference(),"runText":self.publication.run_text_reference(),"lastFailure":self.publication_failure}),
        };
        json!({"reference":reference,"runText":self.prepared().record(),"project":crate::attachments::native_path_identity(&self.project_root),"publication":publication,
            "source":self.source.as_ref().map(|s|s.evidence()),"turn":self.turn_id,"status":self.status,"supply":self.supply,
            "checks":self.checks.iter().map(WorkflowCheckSlot::view).collect::<Vec<_>>(),"pendingRecords":self.has_pending_records(),
            "lifecycle":self.lifecycle_view(),"conversation":self.prepared().scope().conversation,
            "endNotice":self.notice.view(),"noticeChecks":self.notice_checks.iter().map(WorkflowCheckSlot::view).collect::<Vec<_>>(),
            "compatibility":self.compatibility_view(),
            "adoption":"unknown","runStanding":"lifecycle as recorded below; completion is never inferred from a native turn"})
    }
    fn lifecycle_view(&self) -> Value {
        let state = match self.lifecycle {
            RunLifecycle::Prepared => "prepared; not a run until its start turn is observed",
            RunLifecycle::StartNotConfirmed => "start not confirmed (turn refused or outcome unknown); not opened, not live",
            RunLifecycle::Open => "open (live); only the person's explicit end ends it",
            RunLifecycle::Ended => "ended by the person",
        };
        json!({"state":state,"follows":self.follows,"end":self.end.as_ref().map(|e|json!({"run":e.run,"cause":run_end_cause(&e.reason)})),
            "records":self.entries.iter().map(|e|json!({"kind":e.kind,"recordId":e.record_id,"observedAt":e.observed_at,"written":e.written.is_some(),"limit":e.failure})).collect::<Vec<_>>()})
    }
    pub fn has_pending_records(&self) -> bool {
        let pending_check = |c: &WorkflowCheckSlot| {
            c.published.is_none() || matches!(c.r3, WorkflowR3::Pending(_) | WorkflowR3::AwaitingCheck)
        };
        self.published.is_none()
            || self.entries.iter().any(|e| e.written.is_none())
            || self.checks.iter().any(pending_check)
            || self.notice_checks.iter().any(pending_check)
    }
    fn entry_written(&self, kind: &str) -> bool {
        self.entries
            .iter()
            .any(|e| e.kind == kind && e.written.is_some())
    }
    /// Writes pending lifecycle entries in their original order; stops at the
    /// first failure so later entries never overtake it (W-2).
    fn flush_entries(&mut self) {
        let run = self.prepared().scope().run.clone();
        for entry in &mut self.entries {
            if entry.written.is_some() {
                continue;
            }
            if crate::records::supply::append_run_entry(&self.project_root, &run, entry).is_err() {
                break;
            }
        }
    }
    fn advance_checks(&mut self) {
        let opened = self.entry_written("run_opened");
        let ended = self.entry_written("run_ended");
        for slot in &mut self.checks {
            slot.advance(&self.project, opened);
        }
        for slot in &mut self.notice_checks {
            slot.advance(&self.project, ended);
        }
    }
    /// EXEC §3.1 CK-1/CK-2 through J2's seam, from this run's own selection,
    /// holding library, home, generation and conversation. Advisory only: the
    /// result never gates a start, and no R14 is written when publication is
    /// refused (the normal case without an environment collector).
    fn evaluate_compatibility(
        &mut self,
        occasion: crate::execution_compatibility::report::Occasion,
    ) {
        use crate::execution_compatibility::report as report;
        let scope = self.prepared().scope().clone();
        let basis = report::Basis {
            home: scope.home.clone(),
            generation: scope.generation.clone(),
            conversation: scope.conversation.clone(),
            acting_pin: "App Codex 0.160.0".into(),
            surface: "X".into(),
            environment_observation: None,
            catalog_edition: None,
        };
        // Same-conversation obligation: the role binding is looked up for this
        // run's own home and conversation; a missing binding stays Unknown.
        let role = match self.home.history.try_lock() {
            Ok(history) => history
                .binding(&scope.home, &scope.conversation)
                .map(|b| b.role_in_force(&scope.home, &scope.conversation))
                .unwrap_or(crate::role_lifecycle::RoleInForce::Unknown {
                    reason: "original App supply binding not established".into(),
                }),
            Err(_) => crate::role_lifecycle::RoleInForce::Unknown {
                reason: "role binding owner busy; not read".into(),
            },
        };
        let label = match occasion {
            report::Occasion::Selection => "CK-1 selection",
            report::Occasion::BeforeFirstAction => "CK-2 run start",
            report::Occasion::EditionChange { .. } => "CK-3 edition change",
        };
        let result = report::evaluate(report::Request {
            selection: &self.selection,
            holding_library: Some(scope.holding_library.clone()),
            role,
            basis: basis.clone(),
            occasion,
            evaluated_at: crate::util::now_rfc3339(),
            inventory: report::Inventory {
                origin: report::InventoryOrigin::CallerSupplied {
                    source: "App Root: no environment collector; nothing observed".into(),
                },
                host_id: None,
                observations: report::Observations::default(),
            },
            model_destination: None,
        });
        self.compatibility.push(CompatibilitySlot {
            occasion: label,
            basis,
            result,
        });
    }
    fn compatibility_view(&self) -> Value {
        let current = self.prepared().scope();
        json!(self.compatibility.iter().map(|slot|{
            let current_basis = crate::execution_compatibility::report::Basis{generation:current.generation.clone(),..slot.basis.clone()};
            let mut view = match &slot.result {
                Ok(evaluation) => evaluation.view(&current_basis),
                Err(e) => json!({"state":"no evaluation","limit":e}),
            };
            view["occasion"] = json!(slot.occasion);
            view["advisory"] = json!("informs only; never gates a start (CC-3)");
            view["r14"] = json!(match &slot.result {
                Ok(e) if e.published.is_ok() => "EXEC report published in memory only; the App has no allocated report store, so no R14 is written (CI-20)",
                _ => "no report published; no R14 written (run's R14 stays 'no report evaluated')",
            });
            view
        }).collect::<Vec<_>>())
    }
    /// WP-5 pre-send publication of the original selection and run_text. On
    /// failure nothing is sent and the original pending bytes are kept.
    fn publish_pre_send(&mut self) -> Result<(), String> {
        if self.published.is_some() {
            return Ok(());
        }
        match self.publication.publish(&self.project) {
            Ok(published) => {
                self.published = Some(published);
                self.publication_failure = None;
                Ok(())
            }
            Err(error) => {
                let recorded = json!({"selection":self.record_state(self.publication.selection_reference()),"runText":self.record_state(self.publication.run_text_reference())});
                self.publication_failure = Some(json!({"limit":error,"recorded":recorded}));
                self.status = json!({"state":"WR pre-send publication failed; nothing sent","sent":false,"supplied":"not supplied","recorded":recorded,"limit":error,"retry":"Retry publishes the same original records; sending stays a separate once-only step","adoption":"unknown","runStanding":"no active run inferred"});
                Err(format!("WR selection/run_text not durably recorded; nothing sent: {error}"))
            }
        }
    }
    pub fn send(&mut self) -> Result<Value, String> {
        if self.attempted {
            return Err("Original workflow source attempt retained; no resend".into());
        }
        current_conversation(
            &self.home.host.snapshot(),
            &self.prepared().scope().generation,
            &self.prepared().scope().conversation,
        )?;
        self.publish_pre_send()?;
        let (selection_ref, text_ref) = {
            let published = self.published.as_ref().unwrap();
            // WP-3: the exact composed text is rechecked against the published identity.
            let body = published.run_text_record().body();
            let text = published.prepared().text();
            if body["text_identity"] != crate::role_supply::content(text.as_bytes())
                || body["text_bytes"] != text.len()
                || published.prepared().record() != body
            {
                return Err("Composed text differs from the published run_text; nothing sent".into());
            }
            (
                published.selection_record().reference().to_owned(),
                published.run_text_record().reference().to_owned(),
            )
        };
        let records = json!({"selection":selection_ref,"runText":text_ref});
        // EXEC §3.1 CK-2: a new evaluation immediately before the run's first
        // action. Advisory: its outcome is not consulted below.
        self.evaluate_compatibility(
            crate::execution_compatibility::report::Occasion::BeforeFirstAction,
        );
        self.attempted = true;
        let prepared = self.publication.prepared().clone();
        let source = match self.home.host.turn_start_prepared_run_text(
            &prepared.scope().generation,
            &prepared,
            &self.person_text,
            &self.client_id,
        ) {
            Ok(source) => source,
            Err(error) => {
                self.lifecycle = RunLifecycle::StartNotConfirmed;
                self.status = json!({"state":"native workflow-text send not started; original records retained","records":records,"limit":error,"sent":"not observed","automaticRetry":false,"run":"not opened (EXEC A-3)","supplyCheck":"not recorded: no Host receipt of a turn/start refusal; outcome not established (CI-20)","r3":"unavailable: no source-bound native turn","adoption":"unknown"});
                return Err(error);
            }
        };
        self.source = Some(source.clone());
        match self.home.host.turn_start_prepared_finish(
            &source,
            &prepared,
            &self.person_text,
            &self.client_id,
            std::time::Duration::from_secs(20),
        ) {
            Ok(native) => {
                self.turn_id = Some(native.turn_id().to_owned());
                self.status = json!({"state":"native workflow-text turn observed; run opened","records":records,"replyStatus":native.reply_status(),"observedStatus":native.observed_status(),"supplied":"not yet checked","adoption":"unknown","runStanding":"open until the person ends it; a failed or completed native turn does not end it"});
            }
            Err(error) => {
                self.lifecycle = RunLifecycle::StartNotConfirmed;
                // V9 F-1: only Codex's definite refusal of this exact turn/start
                // grounds a supply_check *not found* (WR §16.4, RN-4). An unknown
                // outcome mints nothing that claims not found (CI-20).
                let refusal = self.home.host.prepared_turn_refusal(&source);
                let definite = refusal.is_some();
                let check = match refusal {
                    Some(refusal) => self.record_refused_start(refusal),
                    None => Value::Null,
                };
                self.status = json!({"state":if definite {"native workflow-text turn/start refused by Codex; original source retained"} else {"native workflow-text send outcome unknown; original source retained"},
                    "records":records,"limit":error,"automaticRetry":false,"run":"not opened (EXEC A-3): start not confirmed",
                    "supplyCheck":if definite {"not found (RN-4): turn/start refused by Codex"} else {"not recorded: turn/start outcome unknown (CI-20)"},
                    "check":check,"r3":"unavailable: no source-bound native turn","adoption":"unknown"});
                return Err("Original native workflow source outcome unavailable; inspect retained source, no resend".into());
            }
        }
        self.open_run();
        Ok(self.status.clone())
    }
    /// V9 F-1: publish the *not found* check for a definitely refused start. R3
    /// stays unavailable: no source-bound native turn exists (RS §13.6a).
    fn record_refused_start(&mut self, refusal: crate::hosting::NativeTurnRefusal) -> Value {
        let minted = (|| {
            let published = self.published.as_ref().ok_or("run text not published")?;
            let completed = crate::workflow_workspace::publication::CompletedSupplyCheck::not_found_after_refusal(
                refusal,
                published,
                &self.client_id,
                &crate::util::opaque_id("workflow-check:")?,
                &crate::util::now_rfc3339(),
            )?;
            crate::workflow_workspace::publication::PendingSupplyCheck::new(&self.project, completed, published, WR_WRITER)
        })();
        match minted {
            Ok(pending) => {
                self.checks.push(WorkflowCheckSlot {
                    pending,
                    published: None,
                    publication_failure: None,
                    r3: WorkflowR3::AwaitingCheck,
                });
                self.advance_checks();
                self.checks.last().map(WorkflowCheckSlot::view).unwrap_or(Value::Null)
            }
            Err(e) => json!({"state":"not found check not minted","limit":e}),
        }
    }
    /// EXEC A-2: the start turn was observed, so the run opens and the App writer
    /// records `run_opened` (with `follows` for a sequential run, RE-7).
    fn open_run(&mut self) {
        let scope = self.prepared().scope().clone();
        let id = self.prepared().workflow().clone();
        let mut body = json!({"runId":scope.run,"startedBy":{"kind":"person"},"surface":"App run",
            "workflow":{"kind":id.kind,"origin":id.origin,"sourceRoot":id.source_root,"name":id.name,"revision":id.revision,"revisionVerification":"verified"},
            "conversationRef":scope.conversation});
        if let Some(prior) = &self.follows {
            body["follows"] = json!(prior);
        }
        // R5a: the role in force from this conversation's own App supply binding.
        if let Ok(history) = self.home.history.try_lock() {
            if let Some(crate::role_lifecycle::RoleInForce::AppObserved { role, .. }) = history
                .binding(&scope.home, &scope.conversation)
                .map(|b| b.role_in_force(&scope.home, &scope.conversation))
            {
                body["seatRole"] = json!(role.map(|r| r.name()).unwrap_or("no role"));
            }
        }
        self.lifecycle = RunLifecycle::Open;
        match crate::records::supply::PendingRunEntry::new(
            "run_opened",
            body,
            crate::util::now_rfc3339(),
        ) {
            Ok(entry) => self.entries.push(entry),
            Err(e) => self.status["recordLimit"] = json!(format!("run_opened identity unavailable: {e}")),
        }
        self.flush_entries();
    }
    /// EXEC AE-7 / A-11: only the person's explicit end ends a run. `successor`
    /// is set for "End ‹A› and start ‹B›": no end notice, the chain line says it.
    pub fn end_run(&mut self, completed: bool, successor: Option<&str>) -> Result<Value, String> {
        if self.lifecycle != RunLifecycle::Open {
            return Err("Only an open run can be ended; nothing recorded".into());
        }
        let scope = self.prepared().scope().clone();
        let reason = match successor {
            Some(name) => crate::workflow_workspace::RunEndReason::ToStart(name.to_owned()),
            None if completed => crate::workflow_workspace::RunEndReason::Completed,
            None => crate::workflow_workspace::RunEndReason::ByPerson,
        };
        let cause = run_end_cause(&reason);
        if successor.is_some() && cause == "invalid" {
            return Err("successor workflow name invalid; nothing ended".into());
        }
        let entry = crate::records::supply::PendingRunEntry::new(
            "run_ended",
            json!({"stoppedBy":"the person","cause":cause,"waitingArrivals":[]}),
            crate::util::now_rfc3339(),
        )?;
        self.end = Some(crate::workflow_workspace::OwnerRunEnd {
            home: scope.home.clone(),
            conversation: scope.conversation.clone(),
            run: scope.run.clone(),
            workflow: self.prepared().workflow().clone(),
            reason,
        });
        self.lifecycle = RunLifecycle::Ended;
        self.notice = if successor.is_some() {
            NoticeState::ByChain
        } else {
            NoticeState::AwaitingTurn
        };
        self.entries.push(entry);
        self.flush_entries();
        self.advance_checks();
        self.status = json!({"state":"run ended by the person","cause":cause,"recorded":self.entry_written("run_ended"),"endNotice":self.notice.view(),"adoption":"unknown"});
        Ok(self.status.clone())
    }
    /// TX-5: publish the end notice, then send it as the first text element of
    /// the person's next ordinary turn. Dispatched at most once; a publication
    /// failure sends nothing and keeps the original pending bytes.
    pub fn send_end_notice(&mut self, generation: &Value, person_text: &str) -> Result<Value, String> {
        if !self.notice.awaiting_turn() {
            return Err("No end notice is pending for this run; nothing sent".into());
        }
        let scope = self.prepared().scope().clone();
        current_conversation(&self.home.host.snapshot(), generation, &scope.conversation)?;
        if person_text.is_empty() {
            return Err("text required".into());
        }
        if matches!(self.notice, NoticeState::AwaitingTurn) {
            let end = self.end.clone().ok_or("owner end absent")?;
            let start = self.published.as_ref().ok_or("original run start not published")?;
            let publication = crate::workflow_workspace::publication::PreparedEndPublication::for_turn(
                &self.project,
                start.prepared(),
                &end,
                start.run_text_record(),
                WR_WRITER,
                &crate::util::now_rfc3339(),
                generation,
            )?;
            self.notice = NoticeState::Prepared(publication);
        }
        let NoticeState::Prepared(publication) = &self.notice else {
            unreachable!()
        };
        let published = match publication.publish(&self.project) {
            Ok(p) => p,
            Err(e) => {
                self.status = json!({"state":"end notice not recorded; nothing sent","limit":e,"retry":"the next send retries the same original notice record"});
                return Err(format!("End notice not durably recorded; nothing sent: {e}"));
            }
        };
        let client_id = crate::util::opaque_id("workflow-message:")?;
        let notice = crate::workflow_workspace::publication::PublishedText::prepared(&published).clone();
        let mut outcome = json!({"state":"dispatch attempted"});
        let mut turn = None;
        match self.home.host.turn_start_prepared_run_text(generation, &notice, person_text, &client_id) {
            Err(e) => outcome = json!({"state":"native send not started","limit":e,"automaticRetry":false}),
            Ok(source) => match self.home.host.turn_start_prepared_finish(&source, &notice, person_text, &client_id, std::time::Duration::from_secs(20)) {
                Ok(native) => {
                    turn = Some(native.turn_id().to_owned());
                    outcome = json!({"state":"native turn observed","observedStatus":native.observed_status(),"source":source.evidence()});
                }
                Err(e) => outcome = json!({"state":"native send failed/unknown; not resent","limit":e,"source":source.evidence()}),
            },
        }
        self.notice = NoticeState::Sent {
            published,
            client_id,
            turn,
            generation: generation.clone(),
            outcome: outcome.clone(),
        };
        if outcome["state"] == "native turn observed" {
            Ok(json!({"state":"end notice and the person's text sent once","endNotice":self.notice.view()}))
        } else {
            Err(format!("End notice turn outcome unavailable; not resent: {outcome}"))
        }
    }
    /// Retries only pending original records (WP-5): pre-send publication, check
    /// publication and R3 late writes. Never sends and never re-reads native data.
    pub fn retry_records(&mut self) -> Result<Value, String> {
        if self.published.is_none() {
            self.publish_pre_send()?;
            if !self.attempted {
                self.status = json!({"state":"selection and run_text recorded; not sent","sent":false,"supplied":"not supplied","next":"Send remains a separate once-only step","adoption":"unknown","runStanding":"no active run inferred"});
            }
        }
        self.flush_entries();
        self.advance_checks();
        Ok(json!({"status":self.status,"lifecycle":self.lifecycle_view(),"checks":self.checks.iter().map(WorkflowCheckSlot::view).collect::<Vec<_>>(),"noticeChecks":self.notice_checks.iter().map(WorkflowCheckSlot::view).collect::<Vec<_>>(),"pendingRecords":self.has_pending_records()}))
    }
    /// SC-3..SC-6: one genuine native read, minted into a new immutable check,
    /// published and recorded as R3. Each call is a new check (SC-6).
    pub fn check_native_supply(&mut self) -> Result<Value, String> {
        if self.published.is_none() {
            return Err("No published run_text; nothing was sent or checked".into());
        }
        let turn = self
            .turn_id
            .clone()
            .ok_or("Original native turn identity not received; no page guess")?;
        let generation = self.prepared().scope().generation.clone();
        let client = self.client_id.clone();
        self.check_text(false, &generation, &turn, &client)
    }
    /// SQ-END EN-3: a check of the end notice against Codex's history.
    pub fn check_end_notice_supply(&mut self) -> Result<Value, String> {
        let NoticeState::Sent { turn, client_id, generation, .. } = &self.notice else {
            return Err("No end notice was sent; nothing to check".into());
        };
        let turn = turn.clone().ok_or("End-notice turn identity not received; no page guess")?;
        let (generation, client) = (generation.clone(), client_id.clone());
        self.check_text(true, &generation, &turn, &client)
    }
    fn check_text(
        &mut self,
        notice: bool,
        generation: &Value,
        turn: &str,
        client: &str,
    ) -> Result<Value, String> {
        let thread = self.prepared().scope().conversation.clone();
        let mut issued = Vec::new();
        let outcome = self.read_native_items(generation, &thread, turn, &mut issued);
        let read_at = crate::util::now_rfc3339();
        let check = crate::util::opaque_id("workflow-check:")?;
        let published: &dyn crate::workflow_workspace::publication::PublishedText = if notice {
            match &self.notice {
                NoticeState::Sent { published, .. } => published,
                _ => return Err("end notice not published".into()),
            }
        } else {
            self.published.as_ref().ok_or("run text not published")?
        };
        let expected_text = published.prepared().text().to_owned();
        let (turn, client_id) = (turn.to_owned(), client.to_owned());
        let (completed, display) = match outcome {
            Ok((seal, pages)) => {
                let mut index = 0;
                let comparison = crate::workflow_workspace::compare_untrusted_pages(
                    &expected_text,
                    &turn,
                    &client_id,
                    |_| {
                        let page = pages.get(index).cloned().ok_or("No checked native page")?;
                        index += 1;
                        Ok(page)
                    },
                );
                let display = json!({"state":"genuine current native pages checked; text comparison below","comparison":comparison,"generation":generation,"thread":thread,"turn":turn,"pageCount":seal.page_count(),"sourceReceipts":seal.source_receipts().map(|(id,reference,position)|json!({"requestIdentity":id,"sourceRef":reference,"receiptPosition":position})).collect::<Vec<_>>(),"adoption":"unknown","runStanding":"no active/completed workflow run inferred","limits":["final source/owner guard at one check boundary, not permanent authority","native user-message text is not model uptake, workflow registration or successful execution"]});
                let completed = crate::workflow_workspace::publication::CompletedSupplyCheck::from_native_coverage(
                    seal, &pages, published, &turn, &client_id, &check, &read_at,
                )?;
                (completed, display)
            }
            Err(error) if !issued.is_empty() => {
                let completed = crate::workflow_workspace::publication::CompletedSupplyCheck::unreadable_after_dispatch(
                    &issued, published, &turn, &client_id, &check, &read_at, &error,
                )?;
                (completed, json!({"state":"native item read failed after dispatch; recorded as unreadable","limit":error,"turn":turn,"adoption":"unknown","runStanding":"no active/completed workflow run inferred"}))
            }
            Err(error) => return Err(error),
        };
        let pending = crate::workflow_workspace::publication::PendingSupplyCheck::new(
            &self.project,
            completed,
            published,
            WR_WRITER,
        )?;
        let mut slot = WorkflowCheckSlot {
            pending,
            published: None,
            publication_failure: None,
            r3: WorkflowR3::AwaitingCheck,
        };
        // R3 follows its lifecycle entry in the run log: run_opened for the start
        // text, run_ended for the end notice (RS §4 R3).
        slot.advance(&self.project, self.entry_written(if notice { "run_ended" } else { "run_opened" }));
        let mut supply = display;
        supply["check"] = slot.view();
        if notice {
            self.notice_checks.push(slot);
        } else {
            self.checks.push(slot);
            self.supply = supply.clone();
        }
        Ok(supply)
    }
    /// The existing source-owned traversal. Every Host-issued dispatch is kept so
    /// a later failure can still be recorded as *unreadable* against it.
    fn read_native_items(
        &self,
        generation: &Value,
        thread: &str,
        turn: &str,
        issued: &mut Vec<crate::hosting::HistoryDispatch>,
    ) -> Result<(crate::hosting::NativeItemCoverageSeal, Vec<Value>), String> {
        current_conversation(&self.home.host.snapshot(), generation, thread)?;
        let query = {
            let mut receiver = self.home.history.lock().unwrap();
            receiver.reconcile(&self.home.host);
            let h = receiver
                .history_mut()
                .ok_or("Native History owner unavailable")?;
            if h.selected_thread() != Some(thread) {
                return Err("Select this original conversation in native History and load its turns before checking supply".into());
            }
            h.items_page(turn, None, crate::native_history::Direction::Asc)?
        };
        let mut query = query;
        let mut check = None;
        let mut pages = Vec::new();
        loop {
            let dispatch = match check.as_mut() {
                None => self.home.host.history_dispatch(&query)?,
                Some(check) => self
                    .home
                    .host
                    .dispatch_next_native_items_supply_page(check, &query)?,
            };
            issued.push(dispatch.clone());
            self.home
                .history
                .lock()
                .unwrap()
                .dispatched(dispatch.clone());
            self.home
                .host
                .history_wait(&dispatch, std::time::Duration::from_secs(20))?;
            let mut receiver = self.home.history.lock().unwrap();
            receiver.reconcile(&self.home.host);
            let h = receiver
                .history_mut()
                .ok_or("Original NativeHistory owner ended")?;
            let observed = h.accepted_items_observation(&query)?;
            let accepted = self
                .home
                .host
                .mint_accepted_items_page(&dispatch, observed)?;
            self.home.host.revalidate_accepted_items_page(&accepted)?;
            pages.push(accepted.page().clone()); // Bounded transient comparison; never a proof/cache.
            if let Some(check) = check.as_mut() {
                self.home
                    .host
                    .accept_next_native_items_supply_page(check, &accepted)?;
            } else {
                check = Some(self.home.host.begin_native_items_supply_check(&accepted)?);
            }
            drop(accepted);
            let next = check.as_ref().unwrap().next_cursor().map(str::to_owned);
            if let Some(next) = next {
                query = h.items_page(turn, Some(&next), crate::native_history::Direction::Asc)?;
                continue;
            }
            let seal = self.home.host.finish_native_items_supply_check(
                check.take().unwrap(),
                h.accepted_items_observation(&query)?,
            )?;
            return Ok((seal, pages));
        }
    }
}

#[cfg(all(test,unix))]
mod workflow_root_tests {
    use super::*;
    use std::{path::PathBuf,sync::{Arc,Mutex},time::Duration};
    struct Fixture {root:PathBuf,package:PathBuf}
    impl Fixture {
        fn new()->Self {
            let root=std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("workflow-root-fixture-").unwrap());
            std::fs::create_dir(&root).unwrap();let package=root.join(crate::workflow_workspace::development_catalog::NAME);std::fs::create_dir(&package).unwrap();
            let catalog=crate::workflow_workspace::development_catalog::DevelopmentCatalog::load().unwrap();
            for(name,bytes)in catalog.select_embedded().snapshot().files(){std::fs::write(package.join(name),bytes).unwrap();}
            Self{root,package}
        }
        fn selected(&self)->WorkflowRootSession{let mut root=WorkflowRootSession::default();root.select_development_copy(self.package.clone()).unwrap();root}
        /// The ordinary journey (TT-1): development copy -> draft -> review -> A15 -> hot registered selection.
        fn registered(&self)->WorkflowRootSession{
            let mut root=self.selected();let control=Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&self.root))));
            root.open_library(self.root.clone(),"project",Some(&self.root),control.clone()).unwrap();
            root.create_selected_draft("coordinated-knowledge-work").unwrap();
            let home=Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account,Arc::new(crate::hosting::Host::new()),Err("supplier intentionally unavailable".into())).unwrap());
            root.begin_review(home,json!({"hostState":"absent","identityVerified":false}),vec!["coordinated-knowledge-work".into()],false).unwrap();
            let reference=root.active_review.clone().unwrap();
            let revision={let review=root.reviews[&reference].clone();let mut review=review.lock().unwrap();
                let library=review.library.clone();let offer=review.offer.as_ref().unwrap();let current=review.review.as_ref().unwrap().current().unwrap();
                let actor=crate::act_control::person(Some("synthetic native fixture"),Some("fixture OS"));let context=json!({"library":library.reference,"home":"explicit absent/unknown fixture source","identityVerified":false});
                let mut owner_guard=control.lock().unwrap();let owner=owner_guard.as_mut().unwrap();
                owner.a15_confirmation_text(offer,&current,&actor,&context).unwrap();owner.present_a15(offer).unwrap();
                let event=crate::a15_native::ConfirmedA15Event::synthetic_for_test(offer.id().into(),owner.frozen_a15_offer_digest(offer).unwrap().clone(),actor,context);
                let result=owner.confirm_a15_after_native_event(offer,event,&current).unwrap();drop(current);drop(owner_guard);
                review.attempted_native=true;review.accept_result(result).unwrap();
                review.registered.values().next().unwrap().identity().revision.clone()};
            root.select_hot_registered_copy(&reference,&revision,self.root.join(".chirality/workflows/coordinated-knowledge-work")).unwrap();
            assert_eq!(root.snapshot()["selection"]["standing"],"registered revision");
            root
        }
        fn wr_files(&self)->Vec<String>{let mut v:Vec<String>=std::fs::read_dir(self.root.join(".chirality/records/workflow")).map(|d|d.filter_map(|e|e.ok()).map(|e|e.file_name().to_string_lossy().into_owned()).filter(|n|n.ends_with(".json")&&!n.starts_with('.')).collect()).unwrap_or_default();v.sort();v}
        fn rs_entries(&self)->Vec<Value>{let(entries,limits)=crate::storage::read_all(&self.root);assert!(limits.is_empty(),"{limits:?}");entries}
    }
    impl Drop for Fixture{fn drop(&mut self){let _=std::fs::remove_dir_all(&self.root);}}
    #[test]
    fn workflow_root_closed_selection_real_review_hot_receipt_and_transaction(){
        let f=Fixture::new();let mut root=f.selected();let control=Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&f.root))));
        let library_ref=root.open_library(f.root.clone(),"project",Some(&f.root),control.clone()).unwrap();
        assert!(Arc::ptr_eq(&root.active_library().unwrap().control,&control));
        assert_eq!(root.open_library(f.root.clone(),"project",Some(&f.root),control.clone()).unwrap(),library_ref);
        root.create_selected_draft("coordinated-knowledge-work").unwrap();
        let home=Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account,Arc::new(crate::hosting::Host::new()),Err("supplier intentionally unavailable".into())).unwrap());
        root.begin_review(home,json!({"hostState":"absent","identityVerified":false}),vec!["coordinated-knowledge-work".into()],false).unwrap();
        let reference=root.active_review.clone().unwrap();let review=root.reviews[&reference].clone();let mut review=review.lock().unwrap();
        let library=review.library.clone();let offer=review.offer.as_ref().unwrap();
        let current=review.review.as_ref().unwrap().current().unwrap();
        let actor=crate::act_control::person(Some("synthetic native fixture"),Some("fixture OS"));let context=json!({"library":library.reference,"home":"explicit absent/unknown fixture source","identityVerified":false});
        let mut owner_guard=control.lock().unwrap();let owner=owner_guard.as_mut().unwrap();
        owner.a15_confirmation_text(offer,&current,&actor,&context).unwrap();owner.present_a15(offer).unwrap();
        let event=crate::a15_native::ConfirmedA15Event::synthetic_for_test(offer.id().into(),owner.frozen_a15_offer_digest(offer).unwrap().clone(),actor,context);
        let result=owner.confirm_a15_after_native_event(offer,event,&current).unwrap();drop(current);drop(owner_guard);
        review.attempted_native=true;review.accept_result(result).unwrap();
        let revision=review.registered.values().next().unwrap().identity().revision.clone();
        assert_eq!(review.status["entries"][0]["state"],"registered");drop(review);
        root.select_hot_registered_copy(&reference,&revision,f.root.join(".chirality/workflows/coordinated-knowledge-work")).unwrap();
        assert_eq!(root.snapshot()["selection"]["standing"],"registered revision");
        let mut cold=WorkflowRootSession::default();assert!(cold.select_hot_registered_copy(&reference,&revision,f.package.clone()).is_err(),"readable ledger/tuple cannot recreate hot registration authority");
        assert!(cold.select_development_copy(f.root.join(".chirality/workflows/coordinated-knowledge-work")).is_ok(),"exact copy can separately retain development admission, not old A15");
    }
    #[test]
    fn workflow_root_whole_selected_copy_changes_and_library_alias_are_refused(){
        let f=Fixture::new();let mut root=f.selected();let control=Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&f.root))));
        root.open_library(f.root.clone(),"project",Some(&f.root),control.clone()).unwrap();
        std::fs::write(f.package.join("REVIEW-NOTES.md"),"changed separate package file").unwrap();
        assert!(root.create_selected_draft("kept-draft").is_err());assert!(!f.root.join(".chirality/workflow-drafts/kept-draft").exists());
        let alias=f.root.join("aliased-library");std::os::unix::fs::symlink(&f.root,&alias).unwrap();
        assert!(root.open_library(alias,"project",Some(&f.root),control).is_err());
    }
    struct Peer { fixture:Fixture,home:Arc<HomeSession>,generation:Value }
    impl Peer {
        fn new()->Self {
            use std::os::unix::fs::PermissionsExt;
            let fixture=Fixture::new();for name in ["account","probe"]{std::fs::create_dir(fixture.root.join(name)).unwrap();}
            let script=fixture.root.join("owned-peer.py");
            std::fs::write(&script,r#"#!/usr/bin/python3
import sys,json,os
if '--version' in sys.argv:
 print('codex-cli 0.160.0');sys.exit(0)
def emit(v):print(json.dumps(v),flush=True)
def thread():return {'id':'thread','cliVersion':'0.160.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'own native-shaped fixture','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':'idle'},'turns':[],'agentRole':'TASK'}
def turn():return {'id':'turn','status':'failed','items':[],'error':None,'itemsView':'summary'}
text='';client=''
def mode(name):
 return open(name).read().strip() if os.path.exists(name) else ''
def wr():
 d='.chirality/records/workflow'
 return sorted(n for n in os.listdir(d) if n.endswith('.json') and not n.startswith('.')) if os.path.isdir(d) else []
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log:log.write(json.dumps(f)+'\n')
 method=f.get('method')
 if method=='initialize':result={'userAgent':'unqualified-workflow-root-fixture'}
 elif method=='thread/start':result={'thread':thread(),'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
 elif method=='turn/start':
  # Publish-before-send witness: the WR records the peer can see when the turn arrives.
  with open('turn-start-wr.jsonl','a') as log:log.write(json.dumps(wr())+'\n')
  if mode('turn-mode')=='error':
   emit({'id':f['id'],'error':{'code':-32000,'message':'fixture refused turn/start'}});continue
  if mode('turn-mode')=='exit':
   sys.exit(0)
  text=f['params']['input'][0]['text'];client=f['params']['clientUserMessageId'];result={'turn':turn()}
 elif method=='thread/list':result={'data':[thread()],'nextCursor':None,'backwardsCursor':None}
 elif method=='thread/turns/list':result={'data':[turn()],'nextCursor':None}
 elif method=='thread/items/list':
  m=mode('items-mode');seen=text;cid=client
  if m=='error':
   emit({'id':f['id'],'error':{'code':-32000,'message':'fixture unreadable items'}});continue
  if m=='framing':seen=text.replace('[Chirality] Workflow run start:','[Chirality] Workflow run started:',1)
  if m=='differ':seen=text.replace('\n','\r\n')
  if m=='noclient':cid='other-client'
  message={'type':'userMessage','id':'message','clientId':cid,'content':[{'type':'text','text':seen}]}
  data=[] if m=='absent' else [{'turnId':'turn','item':message}]
  if m=='paged' and f['params'].get('cursor') is None:result={'data':[],'nextCursor':'page-2'}
  else:result={'data':data,'nextCursor':None}
 else:continue
 emit({'id':f['id'],'result':result})
"#).unwrap();std::fs::set_permissions(&script,std::fs::Permissions::from_mode(0o700)).unwrap();
            let mut cfg=crate::hosting::HostConfig::new(script,fixture.root.join("account"),fixture.root.join("probe"),fixture.root.clone());cfg.allow_unverified_dev=true;cfg.wait_limit=Duration::from_secs(2);
            let host=Arc::new(crate::hosting::Host::new());host.start(&cfg,"owned workflow source fixture").unwrap();assert_eq!(host.snapshot()["supplierStanding"],"unverified-development");
            let generation=host.snapshot()["generation"].clone();host.thread_start_with_guidance(&cfg.cwd.to_string_lossy(),"fixture-model","fixture-provider","existing role unchanged").unwrap();
            let home=Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account,host,Ok(cfg)).unwrap());Self{fixture,home,generation}
        }
        fn wire(&self)->Vec<Value>{std::fs::read_to_string(self.fixture.root.join("wire.jsonl")).unwrap().lines().map(|line|serde_json::from_str(line).unwrap()).collect()}
        fn turn_starts(&self)->usize{self.wire().iter().filter(|f|f["method"]=="turn/start").count()}
        /// WR record files the peer saw at each turn/start, in arrival order.
        fn wr_at_turn_start(&self)->Vec<Vec<String>>{std::fs::read_to_string(self.fixture.root.join("turn-start-wr.jsonl")).unwrap_or_default().lines().map(|line|serde_json::from_str(line).unwrap()).collect()}
        fn set_mode(&self,name:&str,value:&str){std::fs::write(self.fixture.root.join(name),value).unwrap();}
        /// The explicit App project (CHIRALITY_WORKSPACE stand-in) owning WR and RS records.
        fn project(&self)->Option<&std::path::Path>{Some(&self.fixture.root)}
        fn select_history(&self){
            let list={let mut receiver=self.home.history.lock().unwrap();receiver.reconcile(&self.home.host);receiver.history_mut().unwrap().list_threads(None,crate::native_history::Direction::Asc).unwrap()};
            self.receive(list);
            self.home.history.lock().unwrap().history_mut().unwrap().select("thread").unwrap();
            let turns=self.home.history.lock().unwrap().history_mut().unwrap().turns_page(None,crate::native_history::Direction::Asc).unwrap();self.receive(turns);
        }
        fn receive(&self,query:crate::native_history::HistoryQuery){let dispatch=self.home.host.history_dispatch(&query).unwrap();self.home.history.lock().unwrap().dispatched(dispatch.clone());self.home.host.history_wait(&dispatch,Duration::from_secs(2)).unwrap();self.home.history.lock().unwrap().reconcile(&self.home.host);}
    }
    impl Drop for Peer{fn drop(&mut self){let _=self.home.host.stop("owned fixture cleanup","test ended");}}
    #[test]
    // CI-18: moved from a development selection to the ordinary registered route; assertions unchanged.
    fn workflow_root_closed_prepare_scoped_send_failed_turn_and_genuine_pages(){
        let peer=Peer::new();let mut root=peer.fixture.registered();let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person exact\r\ntext".into(),peer.project()).unwrap();
        let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();
        run.send().unwrap();assert_eq!(run.turn_id.as_deref(),Some("turn"));assert_eq!(run.status["observedStatus"],"failed");
        let attempted=peer.wire().into_iter().find(|f|f["method"]=="turn/start").unwrap();assert_eq!(attempted["params"],run.prepared().turn_params("person exact\r\ntext",&run.client_id).unwrap());
        assert!(run.send().is_err());assert_eq!(peer.wire().iter().filter(|f|f["method"]=="turn/start").count(),1);
        peer.select_history();let supply=run.check_native_supply().unwrap();assert_eq!(supply["pageCount"],1);assert_eq!(supply["comparison"]["state"],"equal_claimed_text");assert_eq!(supply["adoption"],"unknown");assert_eq!(supply["sourceReceipts"].as_array().unwrap().len(),1);
    }
    #[test]
    // CI-18: moved from a development selection to the ordinary registered route; assertions unchanged.
    fn workflow_root_stale_prepared_scope_keeps_original_receipt_without_resend(){
        let peer=Peer::new();let mut root=peer.fixture.registered();let mut stale=peer.generation.clone();stale["spawnCounter"]=json!(999);
        assert!(root.prepare_run(peer.home.clone(),&stale,"thread","text".into(),peer.project()).is_err());
        let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","text".into(),peer.project()).unwrap();let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();run.send().unwrap();let original=run.source.as_ref().unwrap().request_ref().to_owned();
        peer.home.host.stop_scoped(&peer.generation,"fixture","source loss").unwrap();assert!(run.check_native_supply().is_err());assert!(run.send().is_err());assert_eq!(run.source.as_ref().unwrap().request_ref(),original);assert_eq!(run.status["adoption"],"unknown");
    }
    // J1 control: WR TT-1/TX-1/WP-6. A development selection may be shown, never run.
    #[test]
    fn workflow_root_development_selection_run_is_refused_tt1_tx1(){
        let peer=Peer::new();let mut root=peer.fixture.selected();
        assert_eq!(root.snapshot()["selection"]["standing"],crate::workflow_workspace::development_catalog::STANDING);
        let refused=root.prepare_run(peer.home.clone(),&peer.generation,"thread","text".into(),peer.project());
        assert!(refused.as_ref().is_err_and(|e|e.contains("TT-1")&&e.contains("TX-1")),"{refused:?}");
        assert!(root.runs.is_empty());assert_eq!(peer.turn_starts(),0);assert!(peer.fixture.wr_files().is_empty());
    }
    // J1 control: WR SC-1/WP-5 publish-before-send, SC-6 new check per read, RS R3 per check.
    #[test]
    fn workflow_root_registered_run_publishes_before_send_and_records_each_check(){
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();run.send().unwrap();
        let seen=peer.wr_at_turn_start();assert_eq!(seen.len(),1);assert_eq!(seen[0].len(),2,"selection and run_text must be durable before turn/start: {seen:?}");
        peer.select_history();run.check_native_supply().unwrap();run.check_native_supply().unwrap();
        assert_eq!(peer.fixture.wr_files().len(),4,"each native read is a new immutable supply_check");
        let r3:Vec<Value>=peer.fixture.rs_entries().into_iter().filter(|e|e["kind"]=="supplied_guidance").collect();
        assert_eq!(r3.len(),2,"{}",run.view("run")["checks"]);for e in &r3{assert_eq!(e["body"]["supplyCheck"],"verified");assert_eq!(e["body"]["adoption"],"unknown");}
        assert_eq!(peer.turn_starts(),1);
    }
    fn item_reads(peer:&Peer)->usize{peer.wire().iter().filter(|f|f["method"]=="thread/items/list").count()}
    fn wr_dir(peer:&Peer)->PathBuf{peer.fixture.root.join(".chirality/records/workflow")}
    // WP-5: failed pre-send publication sends nothing; a retry republishes the same original bytes.
    #[test]
    fn workflow_root_publication_failure_sends_nothing_and_retry_keeps_original_bytes(){
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();
        let pending=run.view(&reference)["publication"].clone();assert_eq!(pending["state"],"pending; not recorded");
        // Definite failure: the WR directory cannot be created.
        std::fs::write(wr_dir(&peer),b"not a directory").unwrap();
        assert!(run.send().unwrap_err().contains("nothing sent"));
        assert_eq!(peer.turn_starts(),0);assert!(!run.attempted);assert!(run.source.is_none());
        assert_eq!(run.status["sent"],false);assert_eq!(run.status["supplied"],"not supplied");
        assert_ne!(run.status["recorded"]["selection"]["state"],"recorded (resolves)");assert_ne!(run.status["recorded"]["runText"]["state"],"recorded (resolves)");
        assert!(run.retry_records().is_err());assert_eq!(peer.turn_starts(),0);
        std::fs::remove_file(wr_dir(&peer)).unwrap();
        // Uncertain failure: the selection is linked, then the result is lost.
        crate::workflow_workspace::publication::FAIL_AFTER_LINK.with(|v|v.set(true));
        assert!(run.send().is_err());assert_eq!(peer.turn_starts(),0);assert!(!run.attempted);
        assert_eq!(run.status["recorded"]["selection"]["state"],"recorded (resolves)");assert_eq!(run.status["recorded"]["runText"]["state"],"not recorded");
        let selection_ref=pending["selection"].as_str().unwrap();let text_ref=pending["runText"].as_str().unwrap();
        let file=|r:&str|wr_dir(&peer).join(format!("{}.json",r.strip_prefix("wr-record:v1:").unwrap()));
        let original=std::fs::read(file(selection_ref)).unwrap();
        let retried=run.retry_records().unwrap();assert_eq!(retried["status"]["state"],"selection and run_text recorded; not sent");assert_eq!(peer.turn_starts(),0,"retry publishes only; it never sends");
        assert_eq!(std::fs::read(file(selection_ref)).unwrap(),original,"same identity, same original bytes");assert!(file(text_ref).exists());
        let view=run.view(&reference);assert_eq!(view["publication"]["selection"],selection_ref);assert_eq!(view["publication"]["runText"],text_ref);
        let reopened=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
        let selection=reopened.resolve(selection_ref).unwrap();assert_eq!(selection.envelope()["observed_at"],root.snapshot()["selection"]["selectedAt"],"original selection time, not retry time");
        run.send().unwrap();assert_eq!(peer.turn_starts(),1);
        let name=|r:&str|file(r).file_name().unwrap().to_string_lossy().into_owned();
        let seen=peer.wr_at_turn_start();assert_eq!(seen.len(),1);assert!(seen[0].contains(&name(selection_ref))&&seen[0].contains(&name(text_ref)),"{seen:?}");
        assert!(run.send().is_err());assert_eq!(peer.turn_starts(),1);
    }
    // WP-1: an unknown or unopenable project is refused with no fallback store.
    #[test]
    fn workflow_root_unknown_project_is_refused_without_fallback(){
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let none=root.prepare_run(peer.home.clone(),&peer.generation,"thread","text".into(),None);
        assert!(none.as_ref().is_err_and(|e|e.contains("No explicit App project")&&e.contains("no fallback")),"{none:?}");
        assert!(root.prepare_run(peer.home.clone(),&peer.generation,"thread","text".into(),Some(std::path::Path::new("relative-project"))).is_err());
        assert!(root.prepare_run(peer.home.clone(),&peer.generation,"thread","text".into(),Some(peer.fixture.root.join("absent-project").as_path())).is_err());
        assert!(root.runs.is_empty());assert_eq!(peer.turn_starts(),0);assert!(peer.fixture.wr_files().is_empty());
        assert!(!peer.fixture.root.join("absent-project").exists());
    }
    // SC-3/SC-4 and §16.4: each mode is a new native read and a new immutable check; R3 copies the state.
    #[test]
    fn workflow_root_each_read_maps_state_faithfully_into_new_check_and_r3(){
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();run.send().unwrap();peer.select_history();
        let cases=[("","verified",Some("client id")),("noclient","verified",Some("first user message of the turn")),("paged","verified",Some("client id")),
            ("framing","text differs, workflow bytes equal",Some("client id")),("differ","text differs, workflow bytes differ",Some("client id")),("absent","not found",None),("error","unreadable",None)];
        let project=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
        let text_ref=run.view(&reference)["publication"]["runText"].as_str().unwrap().to_owned();
        let mut seen=std::collections::BTreeSet::new();
        for (mode,state,located) in cases {
            peer.set_mode("items-mode",mode);
            let supply=run.check_native_supply().unwrap_or_else(|e|panic!("{mode}: {e}"));
            let check=&supply["check"];assert_eq!(check["state"],state,"{mode}");assert_eq!(check["published"],true,"{mode}");assert_eq!(check["r3"]["state"],"recorded","{mode}: {check}");
            assert!(seen.insert(check["reference"].as_str().unwrap().to_owned()),"each read is a new check identity");
            let record=project.resolve(check["reference"].as_str().unwrap()).unwrap();let body=record.body();
            assert_eq!(body["state"],state);assert_eq!(body["turn"],"turn");assert_eq!(body["client_user_message_id"],run.client_id.as_str());
            assert_eq!(record.envelope()["basis_records"],json!([text_ref]));assert_eq!(record.envelope()["observed_at"],body["read_at"]);
            assert!(!record.envelope()["source_references"].as_array().unwrap().is_empty(),"actual native source receipts");
            match located{Some(by)=>{assert_eq!(body["located_by"],by);assert_eq!(body["item"],"message");assert!(body.get("observed_text").is_some());},None=>assert!(body.get("observed_text").is_none())}
            if mode=="paged"{assert_eq!(supply["pageCount"],2);}
            let r3=peer.fixture.rs_entries().into_iter().find(|e|e["recordId"]==check["r3"]["recordId"]).unwrap();
            assert_eq!(r3["kind"],"supplied_guidance");assert_eq!(r3["body"]["supplyCheck"],state);assert_eq!(r3["body"]["adoption"],"unknown");
            assert_eq!(r3["body"]["nativeTurn"],"turn");assert_eq!(r3["body"]["thread"],"thread");assert_eq!(r3["body"]["supplyRecord"]["ref"],text_ref.as_str());
            assert_eq!(r3["body"]["supplyCheckRecord"]["ref"],check["reference"]);assert_eq!(r3["observedAt"],body["read_at"]);assert_eq!(r3["runId"],reference.as_str());
            assert_eq!(check["supplyReading"],if state=="verified"{"supplied"}else{"supplied — not verified"});
        }
        assert_eq!(peer.turn_starts(),1,"checks never resend");
    }
    // V9 F-1, WR §16.4 / RN-4: Codex's definite refusal of the exact turn/start mints a
    // supply_check *not found* grounded in that Host receipt; R3 stays unavailable (RS §13.6a).
    #[test]
    fn workflow_root_refused_send_records_not_found_check_and_keeps_r3_unavailable(){
        let peer=Peer::new();let mut root=peer.fixture.registered();peer.set_mode("turn-mode","error");
        let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();
        assert!(run.send().is_err());assert_eq!(peer.turn_starts(),1);assert!(run.turn_id.is_none());
        assert_eq!(peer.wr_at_turn_start()[0].len(),2,"records were durable before the refused send");
        assert_eq!(run.status["supplyCheck"],"not found (RN-4): turn/start refused by Codex");assert!(run.status["r3"].as_str().unwrap().starts_with("unavailable"));
        assert_eq!(peer.fixture.wr_files().len(),3,"one supply_check not found");
        let check=run.view(&reference)["checks"][0].clone();assert_eq!(check["state"],"not found");assert_eq!(check["published"],true);assert_eq!(check["r3"]["state"],"unavailable");
        let project=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
        let record=project.resolve(check["reference"].as_str().unwrap()).unwrap();let body=record.body();
        assert!(body.get("turn").is_none()&&body.get("item").is_none()&&body.get("observed_text").is_none(),"no turn or item exists for a refused start: {body}");
        assert_eq!(body["client_user_message_id"],run.client_id.as_str());assert_eq!(body["purpose"],"run start");
        assert_eq!(record.envelope()["source_references"],json!([run.source.as_ref().unwrap().request_ref()]),"grounded in the exact turn/start receipt");
        assert!(run.check_native_supply().is_err());assert!(run.send().is_err());assert_eq!(peer.turn_starts(),1);
        assert!(peer.fixture.rs_entries().iter().all(|e|e["kind"]!="supplied_guidance"));
    }
    // V9 F-1: a genuinely unknown outcome (transport loss before any response) mints nothing
    // claiming *not found*; status stays "outcome unknown"; no resend (CI-20).
    #[test]
    fn workflow_root_unknown_send_outcome_mints_no_check_and_never_resends(){
        let peer=Peer::new();let mut root=peer.fixture.registered();peer.set_mode("turn-mode","exit");
        let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();
        assert!(run.send().is_err());assert_eq!(peer.turn_starts(),1);assert!(run.turn_id.is_none());
        assert_eq!(run.status["supplyCheck"],"not recorded: turn/start outcome unknown (CI-20)");
        assert_eq!(peer.fixture.wr_files().len(),2,"no supply_check claims not found for an unknown outcome");
        assert!(run.view(&reference)["checks"].as_array().unwrap().is_empty());
        assert!(run.send().is_err());assert_eq!(peer.turn_starts(),1);
    }
    // WP-5/W-2: post-send check publication and R3 failures keep original facts, never resend or re-read.
    #[test]
    fn workflow_root_post_send_record_failures_retry_without_resend(){
        use std::os::unix::fs::PermissionsExt;
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();run.send().unwrap();peer.select_history();
        // 1. RS writer unavailable: WR check published, R3 pending.
        let runs=peer.fixture.root.join(".chirality/records/runs");std::fs::write(&runs,b"blocked").unwrap();
        let first=run.check_native_supply().unwrap()["check"].clone();
        assert_eq!(first["published"],true);assert_eq!(first["r3"]["state"],"pending write; missing in record");
        let r3_id=first["r3"]["recordId"].as_str().unwrap().to_owned();
        // 2. WR check publication unavailable: the check is pending with its original bytes.
        std::fs::set_permissions(wr_dir(&peer),std::fs::Permissions::from_mode(0o500)).unwrap();
        let second=run.check_native_supply().unwrap()["check"].clone();
        std::fs::set_permissions(wr_dir(&peer),std::fs::Permissions::from_mode(0o700)).unwrap();
        assert_eq!(second["published"],false);assert!(second["publicationLimit"].is_string());assert_eq!(second["r3"]["state"],"not recorded; awaits the published check");
        let second_ref=second["reference"].as_str().unwrap().to_owned();assert!(!peer.fixture.wr_files().iter().any(|n|second_ref.ends_with(n.trim_end_matches(".json"))));
        assert!(run.has_pending_records());
        let (reads,starts)=(item_reads(&peer),peer.turn_starts());
        std::fs::remove_file(&runs).unwrap();
        let retried=run.retry_records().unwrap();assert_eq!(retried["pendingRecords"],false,"{retried}");
        assert_eq!(item_reads(&peer),reads,"retry never re-reads native history");assert_eq!(peer.turn_starts(),starts);assert_eq!(starts,1);
        let checks=run.view(&reference)["checks"].clone();assert_eq!(checks[0]["r3"]["recordId"],r3_id.as_str(),"late R3 keeps its reserved identity");
        assert_eq!(checks[1]["reference"],second_ref.as_str(),"publication retry keeps the check identity");assert_eq!(checks[1]["readAt"],second["readAt"]);
        let entries=peer.fixture.rs_entries();
        let late=entries.iter().find(|e|e["recordId"]==r3_id.as_str()).unwrap();assert_eq!(late["observedAt"],first["readAt"],"original observation time");
        assert!(entries.iter().any(|e|e["kind"]=="evidence_limit"&&e["body"]["label"]=="record write failed"&&e["body"]["subjectRef"]==r3_id.as_str()));
        assert_eq!(entries.iter().filter(|e|e["kind"]=="supplied_guidance").count(),2);
        let project=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
        assert_eq!(project.resolve(&second_ref).unwrap().body()["read_at"],second["readAt"]);
        // A further retry is a no-op: no duplicate R3 or limit.
        run.retry_records().unwrap();assert_eq!(peer.fixture.rs_entries().len(),entries.len());
    }
    // Outcome 5: a later process resolves every published record from the project alone.
    #[test]
    fn workflow_root_fresh_process_resolves_records_without_run_claims(){
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        let (selection_ref,text_ref,check_ref,orphan_ref)={let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();run.send().unwrap();peer.select_history();
            let check=run.check_native_supply().unwrap()["check"]["reference"].as_str().unwrap().to_owned();
            // A stopped writer: R3 for this check never reaches the record (WP-5).
            let blocked=peer.fixture.root.join(".chirality/records/runs");std::fs::rename(&blocked,peer.fixture.root.join("runs-aside")).unwrap();std::fs::write(&blocked,b"blocked").unwrap();
            let orphan=run.check_native_supply().unwrap()["check"]["reference"].as_str().unwrap().to_owned();
            std::fs::remove_file(&blocked).unwrap();std::fs::rename(peer.fixture.root.join("runs-aside"),&blocked).unwrap();
            let view=run.view(&reference);(view["publication"]["selection"].as_str().unwrap().to_owned(),view["publication"]["runText"].as_str().unwrap().to_owned(),check,orphan)};
        drop(root); // process state lost; pending R3 for the orphan is gone with it
        let project=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
        let check=project.resolve(&check_ref).unwrap();assert_eq!(check.envelope()["basis_records"],json!([text_ref]));
        let text=project.resolve(&text_ref).unwrap();assert_eq!(text.envelope()["basis_records"],json!([selection_ref]));
        let selection=project.resolve(&selection_ref).unwrap();assert_eq!(selection.body()["standing"],"registered");
        let reading=crate::records::supply::read_project_supply(&project);
        let records=reading["records"].as_array().unwrap();assert_eq!(records.len(),4);assert!(records.iter().all(|r|r["resolution"]=="resolved"),"{reading}");
        let find=|r:&str|records.iter().find(|v|v["reference"]==r).unwrap().clone();
        assert_eq!(find(&check_ref)["r3"][0]["standing"],"HistoricalCorrespondence");assert_eq!(find(&orphan_ref)["r3"],"missing in record");
        assert!(reading["standing"].as_str().unwrap().contains("no live native witness, model adoption, registration or run lifecycle inferred"));
        let kinds:Vec<Value>=peer.fixture.rs_entries().iter().map(|e|e["kind"].clone()).collect();
        assert!(!kinds.iter().any(|k|k=="run_opened"||k=="run_ended"),"no active-run or completion claim: {kinds:?}");
        let fresh=WorkflowRootSession::default();assert!(fresh.snapshot()["runs"].as_array().unwrap().is_empty(),"records do not recreate a live run");
    }
    fn kinds_for(peer:&Peer,run:&str)->Vec<String>{peer.fixture.rs_entries().iter().filter(|e|e["runId"]==run).map(|e|e["kind"].as_str().unwrap().to_owned()).collect()}
    // J3 control: EXEC A-2/RE-7 and RS R1. Opening writes run_opened; a second live start is refused.
    #[test]
    fn j3_open_writes_run_opened_and_second_live_start_is_refused(){
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let a=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        root.runs[&a].clone().lock().unwrap().send().unwrap();
        assert_eq!(kinds_for(&peer,&a).first().map(String::as_str),Some("run_opened"),"opening writes run_opened first");
        let second=root.prepare_run(peer.home.clone(),&peer.generation,"thread","again".into(),peer.project());
        assert!(second.as_ref().is_err_and(|e|e.contains("live")),"{second:?}");assert_eq!(peer.turn_starts(),1);
    }
    // J3 control: RE-7 / CH-1 alone, so the refusal is observed independently of run_opened.
    #[test]
    fn j3_second_live_start_in_conversation_is_refused(){
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let a=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        root.runs[&a].clone().lock().unwrap().send().unwrap();
        let second=root.prepare_run(peer.home.clone(),&peer.generation,"thread","again".into(),peer.project());
        assert!(second.as_ref().is_err_and(|e|e.contains("live")&&e.contains(&a)),"{second:?}");assert_eq!(root.runs.len(),1);assert_eq!(peer.turn_starts(),1);
    }
    // J3 control: EXEC §3.1 CK-1 at selection for a run and CK-2 before the first action.
    #[test]
    fn j3_compatibility_ck1_and_ck2_are_evaluated_advisory_only(){
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let a=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        let run=root.runs[&a].clone();let mut run=run.lock().unwrap();run.send().unwrap();
        let view=run.view(&a);let occasions:Vec<Value>=view["compatibility"].as_array().map(|v|v.iter().map(|e|e["occasion"].clone()).collect()).unwrap_or_default();
        assert_eq!(occasions,vec![json!("CK-1 selection"),json!("CK-2 run start")],"{}",view["compatibility"]);
    }
    #[test]
    fn workflow_root_wrc1_busy_capture_owner_refuses_without_blocking_observer_root(){
        let f=Fixture::new();let mut root=f.selected();let control=Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&f.root))));
        root.open_library(f.root.clone(),"project",Some(&f.root),control.clone()).unwrap();root.create_selected_draft("coordinated-knowledge-work").unwrap();
        let root=Arc::new(Mutex::new(root));let held=control.lock().unwrap();let shared=root.clone();
        let(started_tx,started_rx)=std::sync::mpsc::channel();let(done_tx,done_rx)=std::sync::mpsc::channel();
        let worker=std::thread::spawn(move||{let mut root=shared.lock().unwrap();started_tx.send(()).unwrap();let home=Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account,Arc::new(crate::hosting::Host::new()),Err("offline fixture".into())).unwrap());let result=root.begin_review(home,json!({"hostState":"absent"}),vec!["coordinated-knowledge-work".into()],false);drop(root);done_tx.send(result.is_err()).unwrap();});
        started_rx.recv_timeout(Duration::from_secs(2)).unwrap();
        let outcome=done_rx.recv_timeout(Duration::from_millis(200));
        let observer_root_available=root.try_lock().is_ok();
        drop(held);worker.join().unwrap();
        assert_eq!(outcome.ok(),Some(true),"busy original capture owner must return explicit pending refusal; no workflow-root wait");
        assert!(observer_root_available,"native pre/post observer must still acquire actual global workflow state");
    }
    #[test]
    fn workflow_root_wrc1_busy_review_selection_refuses_without_global_wait(){
        let f=Fixture::new();let mut root=f.selected();let control=Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&f.root))));root.open_library(f.root.clone(),"project",Some(&f.root),control).unwrap();root.create_selected_draft("coordinated-knowledge-work").unwrap();
        let home=Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account,Arc::new(crate::hosting::Host::new()),Err("offline fixture".into())).unwrap());root.begin_review(home,json!({"hostState":"absent"}),vec!["coordinated-knowledge-work".into()],false).unwrap();
        let reference=root.active_review.clone().unwrap();let original=root.reviews[&reference].clone();let held=original.lock().unwrap();let root=Arc::new(Mutex::new(root));let shared=root.clone();let package=f.package.clone();
        let(started_tx,started_rx)=std::sync::mpsc::channel();let(done_tx,done_rx)=std::sync::mpsc::channel();
        let worker=std::thread::spawn(move||{let mut root=shared.lock().unwrap();started_tx.send(()).unwrap();let result=root.select_hot_registered_copy(&reference,"not-a-replayable-registered-identity",package);drop(root);done_tx.send(result.is_err()).unwrap();});
        started_rx.recv_timeout(Duration::from_secs(2)).unwrap();let outcome=done_rx.recv_timeout(Duration::from_millis(200));let observer_root_available=root.try_lock().is_ok();drop(held);worker.join().unwrap();
        assert_eq!(outcome.ok(),Some(true),"busy original review must return pending, not block workflow root");assert!(observer_root_available);
    }

}
