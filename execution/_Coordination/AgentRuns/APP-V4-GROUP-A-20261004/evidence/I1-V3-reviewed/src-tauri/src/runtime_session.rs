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

/// Prepared source path only. Caller must wait for reviewed ledger adoption.
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
