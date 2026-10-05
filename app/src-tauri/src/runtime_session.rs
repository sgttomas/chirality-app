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
        if self.attempted {
            return self.snapshot();
        }
        self.attempted = true;
        let mut configured = false;
        let mut selected_path = None;
        let mut existing = false;
        let result = (|| -> Result<(), String> {
            let root = app_data.map_err(str::to_string)?;
            let path = reviewed_ledger_path(root);
            selected_path = Some(path.clone());
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
            host.configure_recovery(path)?;
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
        Err(error) => {
            status["captureRecovery"] =
                json!([{"state":"AC-8 record pending","writeFailure":error}])
        }
    }
    match requests {
        Ok(requests) => status["requestsRecordedNow"] = json!(requests.len()),
        Err(error) => status["limits"] = json!([error]),
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
