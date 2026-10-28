//! Two separate endpoint decisions, attached to the actual IPC invoker.
use crate::act_control::native_statement as ns;
use raw_window_handle::{
    DisplayHandle, HandleError, HasDisplayHandle, HasWindowHandle, WindowHandle,
};
use serde_json::{json, Value};
use std::sync::mpsc;
use tauri_plugin_dialog::{DialogExt, MessageDialogKind, MessageDialogResult};

pub(crate) const CONTINUE_ACTION: &str = "Continue using this configuration";
const LIMIT: &str = "Original App window could not confirm the endpoint operation";
#[derive(Clone, Copy)]
enum Kind {
    Endpoint,
    Add,
}
#[cfg(test)]
fn statement(effects: &Value, post: bool) -> Result<ns::NativeStatement, String> {
    statement_kind(effects, post, Kind::Endpoint)
}
fn statement_kind(effects: &Value, post: bool, kind: Kind) -> Result<ns::NativeStatement, String> {
    let text = if matches!(kind, Kind::Add) {
        let name = serde_json::to_string(effects["submittedName"].as_str().ok_or(LIMIT)?)
            .map_err(|_| LIMIT)?;
        let effects=format!("Submitted ID: {}\nSubmitted name (quoted data): {}\nEndpoint: {}\nAnonymous Responses definition (requires_openai_auth: false).",effects["providerId"].as_str().ok_or(LIMIT)?,name,effects["endpoint"].as_str().ok_or(LIMIT)?);
        if post {
            format!("Provider addition write observed.\n{effects}\nA fresh private reading matched the submitted definition. Continue using this checked configuration for future actions?\nCurrent conversations, project, choices and drafts stay unchanged; no existing conversation is reloaded.")
        } else {
            format!("Add one configured local provider.\n{effects}\nWrite this one definition to your shared Codex configuration, which other Codex clients also read.\nThis does not choose or start a provider/model, or reload existing conversations.")
        }
    } else if post {
        format!("Endpoint write observed for configured local provider {}.\nA fresh configuration reading reports endpoint: {}\nContinue using this checked configuration for future actions?\nOther private settings are withheld. Current conversations, project, choices and drafts stay unchanged; existing conversations are not reloaded.",effects["providerId"].as_str().ok_or(LIMIT)?,effects["currentEndpoint"].as_str().ok_or(LIMIT)?)
    } else {
        format!("Change endpoint for configured local provider {}.\nCurrent endpoint: {}\nProposed endpoint: {}\nWrite this one endpoint to your shared Codex configuration, which other Codex clients also read.\nThis does not choose or start a provider/model, or reload existing conversations.",effects["providerId"].as_str().ok_or(LIMIT)?,effects["currentEndpoint"].as_str().ok_or(LIMIT)?,effects["proposedEndpoint"].as_str().ok_or(LIMIT)?)
    };
    let title = if post {
        "Continue with checked configuration"
    } else if matches!(kind, Kind::Add) {
        "Add configured local provider"
    } else {
        "Change configured provider endpoint"
    };
    let text = format!(
        "{text}\nSelected account source: {}\nCurrent working folder: {}",
        effects["scope"]["generation"]["home"]
            .as_str()
            .ok_or(LIMIT)?,
        effects["scope"]["cwd"].as_str().ok_or(LIMIT)?
    );
    let content = json!({"effects":text});
    ns::whole_or_in_app(
        title,
        if matches!(kind, Kind::Add) {
            "provider Add effects"
        } else {
            "provider endpoint effects"
        },
        text,
        &content,
        |digest| {
            format!("Review the complete {} effects shown in the App under Content named by an open native confirmation. sha-256: {digest}",if matches!(kind,Kind::Add){"provider Add"}else{"provider endpoint"})
        },
    )
}
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
fn checked<T>(
    window: &(impl HasWindowHandle + HasDisplayHandle),
    present: impl FnOnce(&Parent<'_>) -> T,
) -> Result<T, String> {
    let parent = Parent {
        window: window.window_handle().map_err(|_| LIMIT)?,
        display: window.display_handle().map_err(|_| LIMIT)?,
    };
    Ok(present(&parent))
}
fn result_in_original(
    window: &(impl HasWindowHandle + HasDisplayHandle),
    result: MessageDialogResult,
    action: &str,
) -> Result<MessageDialogResult, String> {
    if ns::chose(&result, action) {
        checked(window, |_| ())?;
    }
    Ok(result)
}
static QUESTION_OPEN: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);
struct QuestionLease;
impl Drop for QuestionLease {
    fn drop(&mut self) {
        QUESTION_OPEN.store(false, std::sync::atomic::Ordering::Release);
    }
}
fn public_presentation(
    statement: ns::NativeStatement,
    present: impl FnOnce(&ns::NativeStatement) -> Result<MessageDialogResult, String> + Send + 'static,
) -> Result<mpsc::Receiver<Result<MessageDialogResult, String>>, String> {
    if QUESTION_OPEN
        .compare_exchange(
            false,
            true,
            std::sync::atomic::Ordering::AcqRel,
            std::sync::atomic::Ordering::Acquire,
        )
        .is_err()
    {
        return Err(
            "An endpoint question is still open; close it before another endpoint operation".into(),
        );
    }
    let (send, receive) = mpsc::channel();
    if std::thread::Builder::new()
        .name("endpoint-public-question".into())
        .spawn(move || {
            let lease = QuestionLease;
            // This worker owns allowlisted effects only. It keeps their named
            // content available until the actual callback ends, even if private
            // operation authority has expired/superseded in the waiting caller.
            let result = ns::showing_in_app(statement.in_app.as_ref(), || present(&statement));
            drop(lease);
            let _ = send.send(result);
        })
        .is_err()
    {
        QUESTION_OPEN.store(false, std::sync::atomic::Ordering::Release);
        return Err(LIMIT.into());
    }
    Ok(receive)
}
fn current_result(
    receive: mpsc::Receiver<Result<MessageDialogResult, String>>,
    current: impl Fn() -> Result<(), String>,
    limit: std::time::Duration,
) -> Result<MessageDialogResult, String> {
    let deadline = std::time::Instant::now() + limit;
    loop {
        current()?;
        let remaining = deadline.saturating_duration_since(std::time::Instant::now());
        if remaining.is_zero() {
            return Err("Endpoint confirmation expired; nothing automatically accepted".into());
        }
        match receive.recv_timeout(remaining.min(std::time::Duration::from_millis(50))) {
            Ok(result) => {
                current()?;
                return result;
            }
            Err(mpsc::RecvTimeoutError::Timeout) => {}
            Err(mpsc::RecvTimeoutError::Disconnected) => return Err(LIMIT.into()),
        }
    }
}
fn confirm_kind(
    invoking: &tauri::Window,
    effects: &Value,
    post: bool,
    limit: std::time::Duration,
    current: impl Fn() -> Result<(), String>,
    kind: Kind,
) -> Result<MessageDialogResult, String> {
    current()?;
    let statement = statement_kind(effects, post, kind)?;
    let invoking = invoking.clone();
    let receive = public_presentation(statement, move |statement| {
        let (send, receive) = mpsc::channel();
        let window = invoking.clone();
        let text = statement.text.clone();
        let title = if post {
            "Continue with checked configuration"
        } else if matches!(kind, Kind::Add) {
            "Add configured local provider"
        } else {
            "Change configured provider endpoint"
        };
        let action = if post {
            CONTINUE_ACTION
        } else if matches!(kind, Kind::Add) {
            crate::hosting::provider_create::WRITE_ACTION
        } else {
            crate::hosting::provider_endpoint::WRITE_ACTION
        };
        let leave = if post {
            "Do not continue source"
        } else if matches!(kind, Kind::Add) {
            "Leave providers unchanged"
        } else {
            "Leave endpoint unchanged"
        };
        invoking
            .run_on_main_thread(move || {
                let done = send.clone();
                let original = window.clone();
                let shown = checked(&window, |parent| {
                    window
                        .dialog()
                        .message(text)
                        .title(title)
                        .kind(MessageDialogKind::Info)
                        .buttons(ns::act_buttons(leave, action))
                        .parent(parent)
                        .show_with_result(move |result| {
                            if !ns::chose(&result, action) {
                                let _ = done.send(Ok(result));
                                return;
                            }
                            let current = original.clone();
                            let failed = done.clone();
                            if original
                                .run_on_main_thread(move || {
                                    let _ = done.send(result_in_original(&current, result, action));
                                })
                                .is_err()
                            {
                                let _ = failed.send(Err(LIMIT.into()));
                            }
                        });
                });
                if let Err(error) = shown {
                    let _ = send.send(Err(error));
                }
            })
            .map_err(|_| LIMIT.to_owned())?;
        receive.recv().map_err(|_| LIMIT.to_owned())?
    })?;
    current_result(receive, current, limit)
}

pub(crate) fn confirm(
    invoking: &tauri::Window,
    effects: &Value,
    post: bool,
    limit: std::time::Duration,
    current: impl Fn() -> Result<(), String>,
) -> Result<MessageDialogResult, String> {
    confirm_kind(invoking, effects, post, limit, current, Kind::Endpoint)
}
pub(crate) fn confirm_add(
    invoking: &tauri::Window,
    effects: &Value,
    post: bool,
    limit: std::time::Duration,
    current: impl Fn() -> Result<(), String>,
) -> Result<MessageDialogResult, String> {
    confirm_kind(invoking, effects, post, limit, current, Kind::Add)
}

/// The Add prewrite reread/queue can outlive its affirmative callback. Check
/// BOTH handles on the SAME original window again outside Host/controller
/// guards. This is a handle check only, never another choice or acceptance.
pub(crate) fn recheck_original(invoking: &tauri::Window) -> Result<(), String> {
    let (send, receive) = mpsc::channel();
    let original = invoking.clone();
    invoking
        .run_on_main_thread(move || {
            let _ = send.send(checked(&original, |_| ()));
        })
        .map_err(|_| LIMIT)?;
    receive
        .recv_timeout(std::time::Duration::from_secs(5))
        .map_err(|_| LIMIT.to_owned())?
}

#[cfg(test)]
mod tests {
    use super::*;
    use raw_window_handle::{RawDisplayHandle, RawWindowHandle, WebDisplayHandle, WebWindowHandle};
    #[test]
    fn access_provider_create_confirmation_quotes_only_submitted_name_and_same_parent_rules() {
        let name = "  Data \\\"quoted\\\" name \\ exact  ";
        let effects = json!({"providerId":"fixture.new","submittedName":name,"endpoint":"https://example.invalid/new","scope":{"generation":{"home":"invented-home"},"cwd":"/invented/work"}});
        for post in [false, true] {
            let s = statement_kind(&effects, post, Kind::Add).unwrap();
            assert!(s.text.contains(&serde_json::to_string(name).unwrap()));
            let action = if post {
                CONTINUE_ACTION
            } else {
                crate::hosting::provider_create::WRITE_ACTION
            };
            for (window, display) in [(false, true), (true, false), (false, false)] {
                let h = Handles { window, display };
                assert!(checked(&h, |_| panic!("missing parent")).is_err());
                assert!(
                    result_in_original(&h, MessageDialogResult::Custom(action.into()), action)
                        .is_err()
                );
            }
            for choice in [
                "Leave providers unchanged",
                "Do not continue source",
                "Add local provider ",
                "Write endpoint change",
            ] {
                assert!(!ns::chose(
                    &MessageDialogResult::Custom(choice.into()),
                    action
                ));
            }
        }
    }
    struct Handles {
        window: bool,
        display: bool,
    }
    // Inspection only: these invented handles never enter a platform consumer.
    impl HasWindowHandle for Handles {
        fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
            if !self.window {
                return Err(HandleError::Unavailable);
            }
            Ok(unsafe { WindowHandle::borrow_raw(RawWindowHandle::Web(WebWindowHandle::new(19))) })
        }
    }
    impl HasDisplayHandle for Handles {
        fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
            if !self.display {
                return Err(HandleError::Unavailable);
            }
            Ok(
                unsafe {
                    DisplayHandle::borrow_raw(RawDisplayHandle::Web(WebDisplayHandle::new()))
                },
            )
        }
    }
    #[test]
    fn access_provider_endpoint_private_wait_retires_while_allowlisted_question_content_stays_pending(
    ) {
        let effects = json!({"providerId":"fixture","scope":{"generation":{"home":"invented-home"},"cwd":"/invented/work"},"currentEndpoint":format!("https://example.invalid/{}","a".repeat(1800)),"proposedEndpoint":format!("https://example.invalid/{}","b".repeat(1800))});
        let s = statement(&effects, false).unwrap();
        let digest = s.in_app.as_ref().unwrap().digest.clone();
        let (send, await_close) = mpsc::channel();
        let receive =
            public_presentation(s, move |_| await_close.recv().map_err(|_| LIMIT.to_owned()))
                .unwrap();
        let deadline = std::time::Instant::now() + std::time::Duration::from_secs(1);
        while !ns::shown_in_app().to_string().contains(&digest) {
            assert!(std::time::Instant::now() < deadline);
            std::thread::yield_now();
        }
        assert!(current_result(
            receive,
            || Err("superseded private source".into()),
            std::time::Duration::from_secs(1)
        )
        .is_err());
        assert!(ns::shown_in_app().to_string().contains(&digest));
        assert!(QUESTION_OPEN.load(std::sync::atomic::Ordering::Acquire));
        send.send(MessageDialogResult::Cancel).unwrap();
        while QUESTION_OPEN.load(std::sync::atomic::Ordering::Acquire) {
            assert!(std::time::Instant::now() < deadline);
            std::thread::yield_now();
        }
        assert!(!ns::shown_in_app().to_string().contains(&digest));
        let (_send, receive) = mpsc::channel();
        assert!(current_result(receive, || Ok(()), std::time::Duration::from_millis(1)).is_err());
    }

    #[test]
    fn access_provider_endpoint_confirmation_requires_both_original_handles_for_each_exact_action()
    {
        for post in [false, true] {
            let action = if post {
                CONTINUE_ACTION
            } else {
                crate::hosting::provider_endpoint::WRITE_ACTION
            };
            for (window, display) in [(false, true), (true, false), (false, false)] {
                let h = Handles { window, display };
                assert!(checked(&h, |_| panic!("missing parent cannot present")).is_err());
                assert!(
                    result_in_original(&h, MessageDialogResult::Custom(action.into()), action)
                        .is_err()
                );
            }
            let h = Handles {
                window: true,
                display: true,
            };
            assert!(
                result_in_original(&h, MessageDialogResult::Custom(action.into()), action).is_ok()
            );
            for result in [
                MessageDialogResult::Cancel,
                MessageDialogResult::Custom("Leave endpoint unchanged".into()),
                MessageDialogResult::Custom("Do not continue source".into()),
                MessageDialogResult::Custom(format!("{action} ")),
            ] {
                assert!(!ns::chose(&result, action));
            }
        }
    }
    #[test]
    fn access_provider_endpoint_confirmation_long_effects_retain_matching_content() {
        let effects = json!({"providerId":"fixture","scope":{"generation":{"home":"invented-home"},"cwd":"/invented/work"},"currentEndpoint":format!("https://example.invalid/{}","a".repeat(1800)),"proposedEndpoint":format!("https://example.invalid/{}","b".repeat(1800))});
        for post in [false, true] {
            let s = statement(&effects, post).unwrap();
            assert!(s.text.contains("configuration") || s.in_app.is_some());
            ns::showing_in_app(s.in_app.as_ref(), || Ok::<_, String>(())).unwrap();
        }
    }
}
