//! DEL-01-04 (capturing it), PRD V4-AUT-06: the person sets the permission level, through the App's `set_level`
//! command and the App's native statement (`act_control::native_statement`, as desktop setup and answers take
//! theirs). The level is the person's own setting: not an act-control act, not a human-act record, not A12, and
//! no entry about it names an actor. No test-build stand-in answers this confirmation: only the window's own
//! native sheet does ([`confirm`]).
use crate::act_control::native_statement as ns;
use crate::codex_level::{self as cl, Level};
use crate::hosting::{Host, LevelScope};
use raw_window_handle::{DisplayHandle, HandleError, HasDisplayHandle, HasWindowHandle, WindowHandle};
use serde_json::{json, Value};
use std::sync::{mpsc, Arc};
use tauri_plugin_dialog::{DialogExt, MessageDialogKind, MessageDialogResult};

/// The statement's act and don't-act labels.
pub(crate) const SET_LEVEL: &str = "Set level";
pub(crate) const DONT_SET: &str = "Don't change";

/// `"default"`, `{"conversation": threadId}` or `"new-conversation"`.
pub(crate) fn parse_scope(scope: &Value) -> Result<LevelScope, String> {
    match scope {
        Value::String(s) if s == "default" => Ok(LevelScope::Default),
        Value::String(s) if s == "new-conversation" => Ok(LevelScope::NewConversation),
        Value::Object(o) if o.len() == 1 => match o.get("conversation").and_then(Value::as_str) {
            Some(thread) if !thread.is_empty() => Ok(LevelScope::Conversation(thread.to_owned())),
            _ => Err("A conversation's level names its conversation; nothing was changed".into()),
        },
        _ => Err("The level's scope is \"default\", {\"conversation\": id} or \"new-conversation\"; nothing was changed".into()),
    }
}

fn writes(level: &Level) -> &'static str {
    match level.dimensions["writes"].as_str() {
        Some("nowhere") => "nowhere",
        Some("project") => "in the project only",
        Some("everywhere") => "anywhere your Mac account can write",
        _ => "as the level's table states",
    }
}
fn network(level: &Level) -> &'static str {
    if level.dimensions["network"] == "on" { "on" } else { "off" }
}
fn asks(level: &Level) -> &'static str {
    match level.dimensions["asks"].as_str() {
        Some("before-a-command-not-known-safe") => "before any command it does not know to be safe",
        Some("when-beyond-the-sandbox") => "when a command needs more than this level gives",
        Some("never") if level.sandboxed() => "never; what needs more than this level gives fails",
        Some("never") => "never",
        _ => "as the level's table states",
    }
}

/// The native statement: the scope, the level's dimensions, that reading is not limited, and when it takes
/// effect; for full access, also [`cl::FULL_ACCESS_STATEMENT`] verbatim. `running`: a turn is running in the
/// conversation the scope names.
pub(crate) fn statement(scope: &LevelScope, level: &Level, running: bool) -> Result<ns::NativeStatement, String> {
    let applies = match scope {
        LevelScope::Default => "new conversations, and every conversation without a level of its own".to_owned(),
        LevelScope::Conversation(thread) => format!("this conversation ({thread})"),
        LevelScope::NewConversation => "the next conversation you start or fork".to_owned(),
    };
    let effect = match scope {
        LevelScope::Default => "It takes effect for each new conversation from its start, and for each conversation without a level of its own from its next request. A turn already running keeps the level it started with.",
        LevelScope::Conversation(_) if running => "A turn is running in this conversation: the level takes effect from its next turn. The running turn, and any command it leaves running, keep the level they started with.",
        LevelScope::Conversation(_) => "It takes effect now, from this conversation's next request.",
        LevelScope::NewConversation => "It takes effect from that conversation's first request.",
    };
    let mut lines = vec![
        format!("Set the permission level for {applies} to: {}.", level.id),
        String::new(),
        format!("Where commands may write: {}.", writes(level)),
        format!("Network for the commands the agent runs: {}.", network(level)),
        format!("When the agent asks you: {}.", asks(level)),
        "Reading is not limited at any level: Codex can read any file your Mac account can read.".to_owned(),
        String::new(),
        effect.to_owned(),
    ];
    if level.id == "full" {
        lines.push(String::new());
        lines.push(cl::FULL_ACCESS_STATEMENT.to_owned());
    }
    let text = ns::bounded("The permission level", lines.join("\n"))?;
    Ok(ns::NativeStatement { text, in_app: None })
}

/// The `set_level` command. `target` is the Host the scope names (the active home); `all` every App home's Host,
/// which a default level reaches. The person's native confirmation comes first; declining or closing it changes
/// nothing and writes nothing. On confirmation the `level_chosen` entry is written, then the level in force
/// changes ([`Host::choose_level`]).
pub(crate) fn set_level(
    target: &Arc<Host>,
    all: &[Arc<Host>],
    scope: &Value,
    level_id: &str,
    confirm: impl FnOnce(&ns::NativeStatement) -> Result<MessageDialogResult, String>,
) -> Result<Value, String> {
    let scope = parse_scope(scope)?;
    let level = cl::level(level_id).ok_or_else(|| format!("No level named {level_id} is offered; nothing was changed"))?;
    let running = match &scope { LevelScope::Conversation(t) => target.level_turn_running(t), _ => false };
    let statement = statement(&scope, level, running)?;
    let digest = crate::util::sha256_hex(statement.text.as_bytes());
    let result = ns::showing_in_app(statement.in_app.as_ref(), || confirm(&statement))?;
    if !ns::chose(&result, SET_LEVEL) {
        return Ok(json!({"state": "dismissed", "changed": false}));
    }
    target.choose_level(&scope, level, &digest, all)
}

/// Both successful lookups, cached: the plugin's `parent` silently ignores a failed one.
struct Parent<'a> {
    window: WindowHandle<'a>,
    display: DisplayHandle<'a>,
}
impl HasWindowHandle for Parent<'_> {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> { Ok(self.window) }
}
impl HasDisplayHandle for Parent<'_> {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> { Ok(self.display) }
}
fn checked_parent(window: &(impl HasWindowHandle + HasDisplayHandle)) -> Result<Parent<'_>, String> {
    Ok(Parent {
        window: window.window_handle().map_err(|_| "Invoking App window unavailable; the level was not changed".to_string())?,
        display: window.display_handle().map_err(|_| "Invoking App display unavailable; the level was not changed".to_string())?,
    })
}

/// The level's native sheet on the invoking window, as the answer confirmation presents its own. A chosen act
/// is accepted only while that same window still exists.
pub(crate) fn confirm(invoking: &tauri::Window, statement: &ns::NativeStatement) -> Result<MessageDialogResult, String> {
    let (send, receive) = mpsc::channel();
    let window = invoking.clone();
    let text = statement.text.clone();
    invoking.run_on_main_thread(move || {
        let parent = match checked_parent(&window) {
            Ok(parent) => parent,
            Err(error) => { let _ = send.send(Err(error)); return; }
        };
        window.dialog()
            .message(text)
            .title("Chirality — permission level")
            .kind(MessageDialogKind::Warning)
            .buttons(ns::act_buttons(DONT_SET, SET_LEVEL))
            .parent(&parent)
            .show_with_result({
                let window = window.clone();
                move |result| {
                    if !ns::chose(&result, SET_LEVEL) { let _ = send.send(Ok(result)); return; }
                    let original = window.clone();
                    let failure = send.clone();
                    if window.run_on_main_thread(move || {
                        let checked = checked_parent(&original).map(|_| result);
                        let _ = send.send(checked);
                    }).is_err() {
                        let _ = failure.send(Err("Invoking App window could not be revalidated; the level was not changed".into()));
                    }
                }
            });
    }).map_err(|_| "Invoking App window could not present the level's confirmation".to_string())?;
    receive.recv().map_err(|_| "The level's confirmation ended without a result; nothing was changed".to_string())?
}

#[cfg(test)]
#[path = "level_choice_tests.rs"]
mod tests;
