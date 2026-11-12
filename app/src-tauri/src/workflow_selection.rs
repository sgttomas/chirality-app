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
/// How long one press waits for the history context while another reader holds it.
const HISTORY_WAIT: std::time::Duration = std::time::Duration::from_secs(3);
const HISTORY_RETRY: std::time::Duration = std::time::Duration::from_millis(5);
const HISTORY_BUSY: &str = "Native history context is busy; refresh the workflow choice";

/// One press's retry for the history context. The checks it is passed to share
/// it, so together they retry for no longer than `HISTORY_WAIT`. It bounds
/// only that retry: other locks a command takes, and a native picker, are
/// outside it, and a command that opens a picker starts a second one after it.
#[derive(Clone, Copy)]
pub(crate) struct Wait(std::time::Instant);
impl Wait {
    pub(crate) fn for_press() -> Self { Self(std::time::Instant::now() + HISTORY_WAIT) }
    fn remains(self) -> bool { std::time::Instant::now() < self.0 }
}

/// Why one look at the displayed context did not pass.
enum Refusal {
    /// Another reader held the history context at that moment; nothing was compared.
    Busy,
    Changed(String),
}

impl Context {
    /// One look, without waiting: the form to use while Root is held.
    fn verify_now(&self, home: &crate::runtime_session::HomeSession) -> Result<Option<Chat>, Refusal> {
        if self.source_ref != home.workflow_source_ref {
            return Err(Refusal::Changed("Workflow App home source changed; refresh the displayed choice".into()));
        }
        let host = home.host.snapshot();
        if host["generation"] != self.generation {
            return Err(Refusal::Changed("Workflow native generation changed; refresh the displayed choice".into()));
        }
        let epoch = home.history.try_lock().map_err(|_| Refusal::Busy)?.snapshot(None)["selectionEpoch"].as_u64();
        if epoch != self.history_epoch {
            return Err(Refusal::Changed("Native history selection changed; refresh the displayed workflow choice".into()));
        }
        match self.thread_id.as_deref() {
            None => Ok(None),
            Some(thread) => {
                crate::runtime_session::current_conversation(&host, &self.generation, thread).map_err(Refusal::Changed)?;
                Ok(Some(Chat::in_home(home, thread)))
            }
        }
    }
    /// The displayed context still holds. Other readers (a status read, a
    /// host tick, a history command) hold the history context for a moment at
    /// a time, so this looks again while the press's wait remains before it
    /// reports busy. It sleeps between looks and never blocks on the lock, so
    /// it imposes no lock order. It is not for use while Root is held (see
    /// `lock_root`), and it sleeps, so its callers run off the main thread.
    pub(crate) fn verify_home_within(&self, home: &crate::runtime_session::HomeSession, wait: Wait) -> Result<Option<Chat>, String> {
        loop {
            match self.verify_now(home) {
                Ok(chat) => return Ok(chat),
                Err(Refusal::Changed(reason)) => return Err(reason),
                Err(Refusal::Busy) if wait.remains() => std::thread::sleep(HISTORY_RETRY),
                Err(Refusal::Busy) => return Err(HISTORY_BUSY.into()),
            }
        }
    }
    /// `verify_home_within` for a press that makes this one check.
    #[cfg(test)]
    pub fn verify_home(&self, home: &crate::runtime_session::HomeSession) -> Result<Option<Chat>, String> {
        self.verify_home_within(home, Wait::for_press())
    }
}

/// Root for a press, with the displayed context checked against the active
/// home while Root is held. With Root held the check never waits: when the
/// history context is held at that moment, Root is released and the whole
/// check is made again within the press's wait. A press therefore neither
/// fails on a passing reader nor keeps Root from others while it waits.
pub(crate) fn lock_root<'a>(
    workflows: &'a std::sync::Mutex<crate::runtime_session::WorkflowRootSession>,
    context: &Context,
    active_home: impl Fn() -> std::sync::Arc<crate::runtime_session::HomeSession>,
    wait: Wait,
) -> Result<(std::sync::MutexGuard<'a, crate::runtime_session::WorkflowRootSession>, std::sync::Arc<crate::runtime_session::HomeSession>, Option<Chat>), String> {
    loop {
        context.verify_home_within(&active_home(), wait)?;
        let root = workflows.lock().unwrap();
        let current = active_home();
        match context.verify_now(&current) {
            Ok(chat) => return Ok((root, current, chat)),
            Err(Refusal::Changed(reason)) => return Err(reason),
            Err(Refusal::Busy) if wait.remains() => { drop(root); std::thread::sleep(HISTORY_RETRY); }
            Err(Refusal::Busy) => return Err(HISTORY_BUSY.into()),
        }
    }
}

/// Recheck the captured source and choice at mutation, including a queued
/// command whose displayed source changed while it waited for Root.
pub(crate) fn with_choice<T>(
    workflows: &std::sync::Mutex<crate::runtime_session::WorkflowRootSession>,
    context: &Context,
    active_home: impl Fn() -> std::sync::Arc<crate::runtime_session::HomeSession>,
    wait: Wait,
    action: impl FnOnce(&mut crate::runtime_session::WorkflowRootSession, std::sync::Arc<crate::runtime_session::HomeSession>, Option<&Chat>) -> Result<T, String>,
) -> Result<T, String> {
    let home = active_home(); context.verify_home_within(&home, wait)?;
    let (mut root, current, chat) = lock_root(workflows, context, &active_home, wait)?;
    if !std::sync::Arc::ptr_eq(&home, &current) {
        return Err("Workflow App source changed; nothing selected or prepared".into());
    }
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
    let wait = Wait::for_press();
    let home = active_home(); context.verify_home_within(&home, wait)?;
    let view = crate::host_tick::receive_view(&home);
    with_choice(workflows, context, active_home, wait, |root, _, chat| {
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
    active_home: impl Fn() -> std::sync::Arc<crate::runtime_session::HomeSession>, wait: Wait,
    person_text: String, project: Option<&std::path::Path>,
) -> Result<String,String> {
    with_choice(workflows,context,active_home,wait,|root,home,chat| {
        let chat=chat.ok_or("Choose the chat that keeps this workflow selection")?;
        root.prepare_run(home,&context.generation,&chat.thread,person_text,project)
    })
}
