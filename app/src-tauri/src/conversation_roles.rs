//! Conversation roles after the start: "Continue as ‹role›" and "Fork"
//! (DEL-01-04 NIR §5.8 CA-1…CA-4; DEL-02-04 ROLE §3.2, §3.3 CA-1…CA-3, F-1),
//! and the role limit account shown where a role is chosen (ROLE §6.2, LA-4).
//!
//! A conversation's role is fixed for its life (DECISION-L L-2). Nothing here
//! changes an existing conversation's role or supply: "Continue as" starts a
//! new conversation with the chosen role's own composition, and a fork is a
//! same-role copy whose guidance is the source's. The handoff summary is
//! conversation text the person edits and sends; it is not supplied guidance.
use crate::role_lifecycle::RoleInForce;
use crate::role_supply::Role;
use serde_json::{json, Value};

/// CA-2 request wording (PROPOSED in NIR U-NIR-9; chosen here). It names what
/// the summary should cover and asks for nothing else.
pub fn handoff_request_text(target: Option<Role>) -> String {
    let continuing = match target {
        Some(role) => format!("a new conversation with the role {}", role.name()),
        None => "a new conversation with no role".into(),
    };
    format!("Please draft a handoff summary of this conversation for {continuing}. \
Cover: my last request; the last workflow run in this conversation and how it ended, or that there was none; \
and the attachments supplied in this conversation, by name and content identity. Write only the summary.")
}

/// How a source conversation's role is named in the header and the relation.
pub fn role_label(role: &RoleInForce) -> String {
    match role {
        RoleInForce::AppObserved { role: Some(role), .. } => format!("role {}", role.name()),
        RoleInForce::AppObserved { role: None, .. } => "no role".into(),
        RoleInForce::Unknown { .. } => "role not established in this App process".into(),
    }
}

/// CA-2: the one App-written header. It names the source conversation and
/// its role, and instructs nothing.
pub fn handoff_header(source_thread: &str, role: &RoleInForce) -> String {
    format!("Handoff from conversation {source_thread} ({}).", role_label(role))
}

/// A send refused before any frame was written (the Host's `refused-not-sent`
/// convention, or the selection check before the Host is called).
/// Anchored at the start: the Host's pre-write refusals begin with
/// `refused-not-sent`, and the selection check's errors with their own fixed
/// words. A later native error that merely mentions those words is a written
/// request and keeps the header-only fallback.
fn not_sent(reason: &str) -> bool {
    reason.starts_with("refused-not-sent") || reason.starts_with("conversation selection is stale") || reason.starts_with("conversation is not loaded")
}

#[derive(Clone, Debug)]
struct Handoff {
    id: String,
    generation: Value,
    source_thread: String,
    source_role: RoleInForce,
    target: Option<Role>,
    request_text: String,
    /// `{"state":"sent","turnId":…}` or `{"state":"failed","reason":…}`.
    request: Value,
    started: Option<Value>,
}

/// App process memory only: open "Continue as" handoffs. A dismissed or
/// started handoff leaves the source conversation exactly as it was.
#[derive(Default)]
pub struct Handoffs {
    open: Vec<Handoff>,
}

impl Handoffs {
    /// CA-1, CA-2: ask the source conversation's agent, in a visible ordinary
    /// turn of that conversation, for a handoff summary. `send` is the real
    /// text-send path. A request refused before anything was written closes
    /// the handoff and is returned as an error; a written request that failed
    /// is kept as the CA-2 fallback (header only). Nothing is retried.
    pub fn begin(
        &mut self,
        generation: &Value,
        source_thread: &str,
        source_role: RoleInForce,
        target: Option<Role>,
        send: impl FnOnce(&str) -> Result<Value, String>,
    ) -> Result<Value, String> {
        let (id, text) = self.reserve(generation, source_thread, source_role, target)?;
        self.sent(&id, send(&text))
    }
    /// The first half of `begin`: checks the choice and opens the handoff with
    /// its request "sending", so no lock is held while Codex answers and a
    /// second press is refused meanwhile.
    pub fn reserve(
        &mut self,
        generation: &Value,
        source_thread: &str,
        source_role: RoleInForce,
        target: Option<Role>,
    ) -> Result<(String, String), String> {
        crate::recovery::generation_ref(generation)?;
        if source_thread.is_empty() {
            return Err("choose the conversation to continue from".into());
        }
        if let Some(role) = target {
            if !role.primary_entry() {
                return Err(format!("{} is a bounded executor for delegated work, not a conversation role here; choose another role or no role. Nothing sent", role.name()));
            }
        }
        if self.open.iter().any(|h| h.generation == *generation && h.source_thread == source_thread && h.started.is_none()) {
            return Err("A Continue-as handoff from this conversation is already open; use it or close it first. Nothing sent".into());
        }
        let handoff = Handoff {
            id: crate::util::opaque_id("continue-as:")?,
            generation: generation.clone(),
            source_thread: source_thread.into(),
            source_role,
            target,
            request_text: handoff_request_text(target),
            request: json!({"state":"sending"}),
            started: None,
        };
        let reserved = (handoff.id.clone(), handoff.request_text.clone());
        self.open.push(handoff);
        Ok(reserved)
    }
    /// The second half of `begin`: the send's outcome. A request refused
    /// before any frame was written (`refused-not-sent`, or a stale or
    /// not-ready selection) asked the source agent nothing: the handoff is
    /// closed and the refusal returned, so the person can try again. A written
    /// request whose turn failed or whose outcome is unknown is kept as the
    /// CA-2 fallback (header only); nothing is retried.
    pub fn sent(&mut self, id: &str, outcome: Result<Value, String>) -> Result<Value, String> {
        let request = match outcome {
            Ok(response) => match response["result"]["turn"]["id"].as_str() {
                Some(turn) => json!({"state":"sent","turnId":turn}),
                None => json!({"state":"failed","reason":"Codex's response named no turn; the summary cannot be read from it"}),
            },
            Err(reason) if not_sent(&reason) => {
                self.open.retain(|h| h.id != id);
                return Err(format!("{reason}. No summary was requested; the Continue-as handoff was closed"));
            }
            Err(reason) => json!({"state":"failed","reason":reason}),
        };
        if let Some(h) = self.open.iter_mut().find(|h| h.id == id) {
            h.request = request.clone();
        }
        Ok(json!({"id":id,"request":request}))
    }

    /// CA-3: the relation a "Continue as" start records, read from the open
    /// handoff. The chosen role must be the one the handoff was opened for.
    pub fn continuation(&self, id: &str, generation: &Value, role: Option<Role>) -> Result<Value, String> {
        let h = self.open.iter().find(|h| h.id == id).ok_or("This Continue-as handoff is no longer open; start again from the conversation")?;
        if h.started.is_some() {
            return Err("This Continue-as handoff already started its new conversation".into());
        }
        if h.generation["home"] != generation["home"] {
            return Err("Continue-as starts the new conversation in the source conversation's Codex home".into());
        }
        if h.target != role {
            return Err("The role chosen for the new conversation differs from the Continue-as choice; nothing started".into());
        }
        let start_record = match &h.source_role {
            RoleInForce::AppObserved { supply_ref, .. } => json!(supply_ref),
            RoleInForce::Unknown { reason } => json!({"standing":"unknown","reason":reason}),
        };
        Ok(json!({"sourceThread":h.source_thread,"sourceGeneration":h.generation,"sourceStartRecord":start_record,
            "sourceRole":h.source_role,"handoff":h.id}))
    }

    pub fn started(&mut self, id: &str, thread: &str, generation: &Value) {
        if let Some(h) = self.open.iter_mut().find(|h| h.id == id) {
            h.started = Some(json!({"threadId":thread,"generation":generation}));
        }
    }

    pub fn dismiss(&mut self, id: &str) -> Result<(), String> {
        let before = self.open.len();
        self.open.retain(|h| h.id != id);
        if self.open.len() == before {
            return Err("This Continue-as handoff is no longer open".into());
        }
        Ok(())
    }

    /// Readable state of each open handoff, with its draft read from what
    /// this App observed live in the source conversation (CA-2).
    pub fn view(&self, snapshot: &Value) -> Value {
        json!(self.open.iter().map(|h| {
            let header = handoff_header(&h.source_thread, &h.source_role);
            let draft = match h.request["turnId"].as_str() {
                Some(turn) => handoff_draft(snapshot, &h.generation, &h.source_thread, turn),
                None if h.request["state"] == "sending" => json!({"state":"waiting","reading":"Sending the summary request to the source conversation."}),
                None => json!({"state":"header-only","reading":format!("The summary request was not sent ({}). The draft holds the header only; write the summary yourself.", h.request["reason"].as_str().unwrap_or("reason not reported"))}),
            };
            let text = match draft["summary"].as_str() {
                Some(summary) => format!("{header}\n\n{summary}"),
                None => header.clone(),
            };
            json!({"id":h.id,"generation":h.generation,"sourceThread":h.source_thread,"sourceRole":h.source_role,
                "sourceRoleLabel":role_label(&h.source_role),"targetRole":h.target,"requestText":h.request_text,"request":h.request,
                "header":header,"draft":draft,"draftText":text,"started":h.started,
                "standing":"Draft only: nothing is sent to the new conversation until you send it. The summary is the source agent's text, not supplied guidance."})
        }).collect::<Vec<_>>())
    }
}

/// CA-2: the summary is the last completed agent message of the request turn,
/// as observed live in this App. A failed or interrupted turn, or a turn that
/// completed with no such message, leaves the header only.
pub fn handoff_draft(snapshot: &Value, generation: &Value, thread: &str, turn: &str) -> Value {
    let turns = snapshot["conversationTurns"].as_array().into_iter().flatten();
    let status = turns
        .filter(|t| t["generation"] == *generation && t["threadId"] == thread && t["turnId"] == turn)
        .find_map(|t| t["nativeTurn"]["status"].as_str().map(str::to_owned));
    let message = snapshot["nativeView"]["items"].as_array().into_iter().flatten()
        .filter(|row| row["threadId"] == thread && row["turnId"] == turn
            && row["native"]["type"] == "agentMessage" && row["displayState"] == "completed"
            && row["standing"] == "live-observed" && row["native"]["text"].is_string())
        .max_by_key(|row| row["observedOrder"].as_u64().unwrap_or(0))
        .and_then(|row| row["native"]["text"].as_str().map(str::to_owned));
    match (status.as_deref(), message) {
        (Some("completed"), Some(summary)) => json!({"state":"drafted","summary":summary,"turnId":turn,"reading":"Drafted by the source conversation's agent in a visible turn there. Edit it before you send it."}),
        (Some("completed"), None) => json!({"state":"header-only","turnId":turn,"reading":"The source turn completed with no agent message this App observed. The draft holds the header only; write the summary yourself."}),
        (Some(other @ ("failed" | "interrupted")), _) => json!({"state":"header-only","turnId":turn,"reading":format!("The source turn ended {other}. The draft holds the header only; write the summary yourself.")}),
        _ => json!({"state":"waiting","turnId":turn,"reading":"Waiting for the source conversation's agent to finish the summary turn."}),
    }
}

/// ROLE §6.2: each role's stated limits with their standing, as handed by the
/// role-limit account (format `chirality.role.limits` 0.2). A modified role
/// copy makes its limits unknown (LA-2); a file not read is reported, never
/// guessed.
pub fn limit_account(root: Option<&std::path::Path>) -> Value {
    let set = match crate::role_supply::bundled_role_set() {
        Ok(set) => set,
        Err(reason) => return json!({"available":false,"reason":reason}),
    };
    let all = json!({"limitId":"L-ALL-1","statement":"Work within the brief's write targets","basis":"A brief is text; Codex sandbox and approval are the person's own settings (D3), not role enforcement","notEnforcement":["brief-text","worktree","sandbox","approval-policy"]});
    let task = json!({"limitId":"L-TASK-1","statement":"A task agent does not delegate","basis":"DECISION-K3 K-10; stated in the shipped TASK guidance; no supplier control is named at the pin","notEnforcement":["approval-policy","sandbox","user-configuration","depth-limit"]});
    let mut roles = vec![];
    let mut not_read = vec![];
    for definition in &set.roles {
        let path = format!("agents/AGENT_{}.md", definition.name.name());
        let guidance = match root {
            Some(root) => crate::role_supply::Guidance::read_seeded(root, &path, crate::runtime_session::INSTRUCTION_RELEASE, crate::runtime_session::role_default(definition.name)),
            None => Err("App instruction store unavailable".into()),
        };
        let guidance = match guidance {
            Ok(g) => g,
            Err(reason) => {
                not_read.push(json!({"role":definition.name,"reason":reason,"reading":"Limits not known: this role's guidance copy could not be read"}));
                continue;
            }
        };
        let modified = guidance.modified();
        let mut limits = vec![];
        for limit in if definition.name == Role::TASK { vec![&task, &all] } else { vec![&all] } {
            let mut limit = limit.clone();
            if modified {
                limit["standing"] = json!("unknown");
                limit["presentedAs"] = json!("Not known whether the supplied guidance states this");
                limit["basis"] = json!(format!("the role's guidance copy is modified (LA-2); {}", limit["basis"].as_str().unwrap_or("")));
            } else {
                limit["standing"] = json!("stated-not-enforced");
                limit["presentedAs"] = json!("Stated, not enforced");
            }
            limits.push(limit);
        }
        roles.push(json!({"role":definition.name,"meaning":definition.meaning,"delegation":definition.delegation,
            "guidanceState":if modified {"modified"} else {"default"},"guidanceContent":crate::role_supply::content(guidance.bytes()),"limits":limits}));
    }
    let account = json!({"format":"chirality.role.limits","formatVersion":"0.2",
        "accountId":format!("lim:{}", crate::role_supply::content(crate::role_supply::BUNDLED_ROLE_SET)["value"].as_str().unwrap_or("")),
        "appRelease":crate::runtime_session::INSTRUCTION_RELEASE,"supplierPin":"0.160.0","roles":roles});
    json!({"available":true,"account":account,"notRead":not_read,
        "standing":"Stated in the role's guidance; Codex does not enforce it. Approval policy, sandbox, your configuration and the depth limit are not this limit's enforcement."})
}

/// NIR CA-4 / ROLE F-1 through the real Host: `thread/fork` with the thread
/// id and no instructions (plus `deferGoalContinuation`, see
/// `Host::thread_fork_dispatch`), the forked conversation admitted from its
/// correlated result, and its role bound as inherited from the source's
/// original binding.
pub fn fork_conversation(home: &crate::runtime_session::HomeSession, generation: &Value, source_thread: &str, wait: std::time::Duration) -> Result<Value, String> {
    let receipt = home.host.thread_fork_dispatch(generation, source_thread)?;
    let evidence = home.host.source_request_wait(&receipt, wait)?;
    let row = home.host.thread_fork_finish(&receipt).map_err(|e| format!("{e} (fork request outcome: {})", evidence["outcome"]))?;
    let binding = home.history.lock().unwrap().fork_observed(&home.host, &receipt, source_thread);
    Ok(json!({"thread":row,"role":binding.unwrap_or_else(|error| json!({"standing":"unknown","reason":format!("the fork's role binding was refused: {error}")})),
        "standing":"Same-role copy: thread/fork carried no instructions, so the fork keeps the source's guidance; the source conversation is unchanged."}))
}

/// The `conversation_fork` command body: route to the home that owns the
/// generation, then fork there.
pub(crate) fn fork_command(homes: &std::sync::Mutex<crate::runtime_session::HomeRouter>, generation: &Value, source_thread: &str, wait: std::time::Duration) -> Result<Value, String> {
    let home = homes.lock().unwrap().for_generation(generation)?;
    fork_conversation(&home, generation, source_thread, wait)
}

/// The `continue_as_begin` command body (CA-1, CA-2). Checks, before anything
/// is opened or sent: a pending run-end notice must go with ordinary text first
/// (as for attachments, WR TX-5), and the source must be a current conversation
/// of a ready Codex. Then one visible ordinary turn asks for the summary.
pub(crate) fn continue_as_begin(
    handoffs: &std::sync::Mutex<Handoffs>,
    workflows: &std::sync::Mutex<crate::runtime_session::WorkflowRootSession>,
    home: &crate::runtime_session::HomeSession,
    generation: &Value,
    thread: &str,
    target: Option<Role>,
) -> Result<Value, String> {
    crate::runtime_session::mode_send_blocked_by_notice(workflows, generation, thread)?;
    crate::runtime_session::current_conversation(&home.host.snapshot(), generation, thread)
        .map_err(|e| format!("{e}; nothing sent"))?;
    let home_name = generation["home"].as_str().ok_or("generation home required")?.to_owned();
    let source_role = home.history.lock().unwrap().binding(&home_name, thread)
        .map(|binding| binding.role_in_force(&home_name, thread))
        .unwrap_or(RoleInForce::Unknown { reason: "original App supply binding not established".into() });
    let (id, text) = handoffs.lock().unwrap().reserve(generation, thread, source_role, target)?;
    let outcome = crate::runtime_session::send_conversation_text(&home.host.snapshot(), generation, thread, &text,
        |generation, thread, text| home.host.turn_start_text(generation, thread, text));
    handoffs.lock().unwrap().sent(&id, outcome)
}

/// `thread_start` with `continue_as` (CA-3): the relation to record, read from
/// the open handoff in the start's own home, or a refusal before anything is sent.
pub(crate) fn continuation_for_start(handoffs: &std::sync::Mutex<Handoffs>, home: &crate::runtime_session::HomeSession, continue_as: Option<&str>, role: Option<Role>) -> Result<Option<Value>, String> {
    match continue_as {
        Some(id) => handoffs.lock().unwrap().continuation(id, &home.host.snapshot()["generation"], role).map(Some),
        None => Ok(None),
    }
}

/// `thread_start` with `continue_as`: an admitted start marks its handoff started.
pub(crate) fn mark_started(handoffs: &std::sync::Mutex<Handoffs>, continue_as: Option<&str>, result: &Result<Value, String>, generation: &Value) {
    if let (Some(id), Ok(response)) = (continue_as, result) {
        if let Some(thread) = response["result"]["thread"]["id"].as_str() {
            handoffs.lock().unwrap().started(id, thread, generation);
        }
    }
}

#[cfg(test)]
#[path = "conversation_roles_tests.rs"]
mod tests;
