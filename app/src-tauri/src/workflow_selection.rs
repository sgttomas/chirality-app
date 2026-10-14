//! Pending workflow choices belong to one actual App home source and chat.
//! A source reference is issued by HomeSession; it is never a mode or thread default.
use serde::Deserialize;
use serde_json::Value;

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub(crate) struct Chat {
    pub source: String,
    pub thread: String,
}
impl Chat {
    pub fn in_home(home: &crate::runtime_session::HomeSession, thread: &str) -> Self {
        Self { source: home.workflow_source_ref.clone(), thread: thread.into() }
    }
}
/// Join the workflow control context onto the status packet the renderer sees.
/// History is published by host_status as nativeHistory; the same packet's
/// epoch must be carried back by a press, including an explicit no-chat press.
pub(crate) fn publish_context(status: &mut Value, home: &crate::runtime_session::HomeSession) {
    status["workflowRoot"]["context"] = serde_json::json!({
        "sourceRef":home.workflow_source_ref,"generation":status["generation"],
        "historyEpoch":status["nativeHistory"]["selectionEpoch"]
    });
}

/// The source and choice the person saw when pressing a control. Null thread
/// explicitly means inspection without a chat, never the next chat's selection.
#[derive(Clone, Debug, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub(crate) struct Context {
    pub source_ref: String,
    pub generation: Value,
    pub history_epoch: Option<u64>,
    pub thread_id: Option<String>,
    pub selection_ref: Option<String>,
    pub inspection_ref: Option<String>,
    pub library_ref: Option<String>,
}
impl Context {
    pub fn verify_home(&self, home: &crate::runtime_session::HomeSession) -> Result<Option<Chat>, String> {
        if self.source_ref != home.workflow_source_ref {
            return Err("Workflow App home source changed; refresh the displayed choice".into());
        }
        let host = home.host.snapshot();
        if host["generation"] != self.generation {
            return Err("Workflow native generation changed; refresh the displayed choice".into());
        }
        let epoch = home.history.try_lock().map_err(|_| "Native history context is busy; refresh the workflow choice")?.snapshot(None)["selectionEpoch"].as_u64();
        if epoch != self.history_epoch {
            return Err("Native history selection changed; refresh the displayed workflow choice".into());
        }
        match self.thread_id.as_deref() {
            None => Ok(None),
            Some(thread) => {
                crate::runtime_session::current_conversation(&host, &self.generation, thread)?;
                Ok(Some(Chat::in_home(home, thread)))
            }
        }
    }
}

/// Recheck the captured source and choice at mutation, including a queued
/// command whose displayed source changed while it waited for Root.
pub(crate) fn with_choice<T>(
    workflows: &std::sync::Mutex<crate::runtime_session::WorkflowRootSession>,
    context: &Context,
    active_home: impl Fn() -> std::sync::Arc<crate::runtime_session::HomeSession>,
    action: impl FnOnce(&mut crate::runtime_session::WorkflowRootSession, std::sync::Arc<crate::runtime_session::HomeSession>, Option<&Chat>) -> Result<T, String>,
) -> Result<T, String> {
    let home = active_home(); context.verify_home(&home)?;
    let mut root = workflows.lock().unwrap();
    let current = active_home(); context.verify_home(&current)?;
    if !std::sync::Arc::ptr_eq(&home, &current) {
        return Err("Workflow App source changed; nothing selected or prepared".into());
    }
    let chat = context.verify_home(&home)?;
    root.verify_choice_context(context, chat.as_ref())?;
    action(&mut root, home, chat.as_ref())
}
/// Selection supersedes proposals only in the chat whose choice changed.
pub(crate) fn choose(
    workflows: &std::sync::Mutex<crate::runtime_session::WorkflowRootSession>,
    context: &Context,
    active_home: impl Fn() -> std::sync::Arc<crate::runtime_session::HomeSession>,
    select: impl FnOnce(&mut crate::runtime_session::WorkflowRootSession, Option<&Chat>) -> Result<Value, String>,
) -> Result<Value, String> {
    let home = active_home(); context.verify_home(&home)?;
    let view = crate::host_tick::receive_view(&home);
    with_choice(workflows, context, active_home, |root, _, chat| {
        if let Some(chat)=chat {
            if root.trial_conversation(&chat.thread).is_some() {
                return Err("A clean trial conversation or its fork offers no workflow selection for a run; inspect library content with no chat selected".into());
            }
        }
        let selected=select(root,chat)?;
        if let Some(chat)=chat {root.note_selection(&view,&chat.thread);}
        Ok(selected)
    })
}
pub(crate) fn prepare(
    workflows: &std::sync::Mutex<crate::runtime_session::WorkflowRootSession>, context: &Context,
    active_home: impl Fn() -> std::sync::Arc<crate::runtime_session::HomeSession>,
    person_text: String, project: Option<&std::path::Path>,
) -> Result<String,String> {
    with_choice(workflows,context,active_home,|root,home,chat| {
        let chat=chat.ok_or("Choose the chat that keeps this workflow selection")?;
        root.prepare_run(home,&context.generation,&chat.thread,person_text,project)
    })
}
