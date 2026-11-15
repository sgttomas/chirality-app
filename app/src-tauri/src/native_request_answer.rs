//! Only the native request-answer confirmation and its original-source checks.
use crate::{act_control::native_statement as ns, runtime_session};
use raw_window_handle::{
    DisplayHandle, HandleError, HasDisplayHandle, HasWindowHandle, WindowHandle,
};
use serde_json::{json, Value};
use std::sync::mpsc;
use tauri_plugin_dialog::{DialogExt, MessageDialogKind, MessageDialogResult};

#[cfg(test)]
pub(crate) fn answer(
    generation: &Value,
    request_id: &Value,
    answer: &Value,
    observe_original: impl FnMut() -> (Value, Value),
    confirm: impl FnOnce(&ns::NativeStatement) -> Result<MessageDialogResult, String>,
    write_original: impl FnOnce(&str) -> Result<Value, String>,
) -> Result<Value, String> {
    answer_with_choice(
        generation,
        request_id,
        answer,
        None,
        observe_original,
        confirm,
        write_original,
    )
}

pub(crate) fn answer_with_choice(
    generation: &Value,
    request_id: &Value,
    answer: &Value,
    presentation_choice: Option<&str>,
    mut observe_original: impl FnMut() -> (Value, Value),
    confirm: impl FnOnce(&ns::NativeStatement) -> Result<MessageDialogResult, String>,
    write_original: impl FnOnce(&str) -> Result<Value, String>,
) -> Result<Value, String> {
    let (snapshot, context) = observe_original();
    let actor = runtime_session::actor_reference(
        context["displayName"].as_str(),
        context["osAccount"].as_str(),
        context["codexAccount"].as_str(),
    );
    let preview =
        runtime_session::answer_preview(&snapshot, generation, request_id, answer, &actor)?;
    let prepared = if crate::request_answer_presentation::supported(&preview["method"]) {
        Some(crate::request_answer_sheet::prepare(
            &snapshot,
            generation,
            request_id,
            &preview,
            presentation_choice,
        )?)
    } else {
        if presentation_choice.is_some() {
            return Err("A question choice does not belong to this request; nothing sent".into());
        }
        None
    };
    let legacy;
    let statement = if let Some(p) = &prepared {
        &p.statement
    } else {
        legacy = ns::request_answer_statement(&preview)?;
        &legacy
    };
    struct CloseCompanion<'a>(&'a Value, &'a Value);
    impl Drop for CloseCompanion<'_> {
        fn drop(&mut self) {
            crate::request_answer_presentation::closed(self.0, self.1);
        }
    }
    let _close = prepared.as_ref().map(|p| {
        crate::request_answer_presentation::publish(generation, request_id, &p.digest, &p.content);
        CloseCompanion(generation, request_id)
    });
    let result = ns::showing_in_app(statement.in_app.as_ref(), || confirm(statement))?;
    if !ns::chose(&result, ns::SEND_ANSWER) {
        return Ok(json!({"state":"dismissed","replyWriteResult":"not-attempted"}));
    }
    let (snapshot, current) = observe_original();
    if current != context {
        return Err("Attribution or owning host context changed during confirmation; review and confirm again".into());
    }
    if let Some(p) = &prepared {
        let current =
            crate::request_answer_presentation::context(&snapshot, generation, request_id)
                .map_err(|_| crate::request_answer_sheet::STALE.to_owned())?;
        if crate::request_answer_presentation::typed(&current)
            != crate::request_answer_presentation::typed(&p.context)
        {
            return Err(crate::request_answer_sheet::STALE.into());
        }
    }
    runtime_session::answer_preview(&snapshot, generation, request_id, answer, &actor)?;
    write_original(&actor)
}

/// Cache both successful lookups: the plugin's `parent` silently ignores a
/// failed lookup. Giving it these borrowed handles cannot select that fallback.
struct Parent<'a> {
    window: WindowHandle<'a>,
    display: DisplayHandle<'a>,
}
impl HasWindowHandle for Parent<'_> {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
        Ok(self.window)
    }
}
impl HasDisplayHandle for Parent<'_> {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
        Ok(self.display)
    }
}
fn checked_parent(
    window: &(impl HasWindowHandle + HasDisplayHandle),
) -> Result<Parent<'_>, String> {
    Ok(Parent {
        window: window.window_handle().map_err(|_| {
            "Invoking App window unavailable; native answer confirmation refused".to_string()
        })?,
        display: window.display_handle().map_err(|_| {
            "Invoking App display unavailable; native answer confirmation refused".to_string()
        })?,
    })
}

/// The command supplies its actual invoker, never a label/focus lookup. Handle
/// validation, plugin parenting and sheet creation share one main-thread turn.
/// Only this async command's worker waits; the main thread uses the callback API.
pub(crate) fn confirm(
    invoking: &tauri::Window,
    statement: &ns::NativeStatement,
) -> Result<MessageDialogResult, String> {
    let (send, receive) = mpsc::channel();
    let window = invoking.clone();
    let text = statement.text.clone();
    let title = if statement
        .in_app
        .as_ref()
        .is_some_and(|c| c.content["type"] == "object")
    {
        "Chirality — answer Codex's request"
    } else {
        "Chirality — answer native request"
    };
    invoking.run_on_main_thread(move || {
        let parent = match checked_parent(&window) {
            Ok(parent) => parent,
            Err(error) => { let _ = send.send(Err(error)); return; }
        };
        window.dialog()
            .message(text)
            .title(title)
            .kind(MessageDialogKind::Warning)
            .buttons(ns::act_buttons(ns::DONT_SEND, ns::SEND_ANSWER))
            .parent(&parent)
            .show_with_result({
                let window = window.clone();
                move |result| {
                    if !ns::chose(&result, ns::SEND_ANSWER) {
                        let _ = send.send(Ok(result));
                        return;
                    }
                    // A sheet result cannot authorize a reply after its original
                    // window was destroyed. Recheck that same window, not a replacement.
                    let original = window.clone();
                    let failure = send.clone();
                    if window.run_on_main_thread(move || {
                        let checked = result_in_parent(&original, result);
                        let _ = send.send(checked);
                    }).is_err() {
                        let _ = failure.send(Err("Invoking App window could not be revalidated; native answer confirmation refused".into()));
                    }
                }
            });
    }).map_err(|_| "Invoking App window could not present native answer confirmation".to_string())?;
    receive.recv().map_err(|_| {
        "Native answer confirmation ended without a result; no reply attempted".to_string()
    })?
}

fn result_in_parent(
    window: &(impl HasWindowHandle + HasDisplayHandle),
    result: MessageDialogResult,
) -> Result<MessageDialogResult, String> {
    if ns::chose(&result, ns::SEND_ANSWER) {
        checked_parent(window)?;
    }
    Ok(result)
}

#[cfg(test)]
#[path = "native_request_answer_tests.rs"]
mod tests;
