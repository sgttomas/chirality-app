//! DEL-01-04 (capturing it), PRD V4-AUT-06: the person sets the permission level through the App's `set_level`
//! command, from the level control in the window. The level is a plain setting: the person's choice in the App is
//! the act, with no native confirmation and nothing sealed. It is not an act-control act, not a human-act record,
//! not A12, and no entry about it names an actor.
use crate::codex_level as cl;
use crate::hosting::{Host, LevelScope};
use serde_json::Value;
use std::sync::Arc;

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

/// The `set_level` command. `target` is the Host the scope names (the active home); `all` every App home's Host,
/// which a default level reaches. The `level_chosen` entry is written, then the level in force changes
/// ([`Host::choose_level`]); where the App's records could not be read at launch, the choice is held for this
/// session only.
pub(crate) fn set_level(target: &Arc<Host>, all: &[Arc<Host>], scope: &Value, level_id: &str) -> Result<Value, String> {
    let scope = parse_scope(scope)?;
    let level = cl::level(level_id).ok_or_else(|| format!("No level named {level_id} is offered; nothing was changed"))?;
    target.choose_level(&scope, level, all)
}

#[cfg(test)]
#[path = "level_choice_tests.rs"]
mod tests;
