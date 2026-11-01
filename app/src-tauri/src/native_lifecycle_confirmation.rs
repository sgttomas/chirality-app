//! Stop/Restart and Quit questions attached to their retained App window.
//! No parentless fallback: rfd's macOS parentless path is a CF user alert,
//! whereas a supplied parent selects the App's NSAlert sheet path.
use crate::act_control::native_statement as ns;
use raw_window_handle::{
    DisplayHandle, HandleError, HasDisplayHandle, HasWindowHandle, WindowHandle,
};
use std::sync::mpsc;
use tauri_plugin_dialog::{
    DialogExt, MessageDialogButtons, MessageDialogKind, MessageDialogResult,
};

const UNAVAILABLE: &str = "Original App window unavailable; native lifecycle confirmation refused";

// The plugin silently ignores failed handle lookups. Cache both successful
// borrows so its .parent() call cannot fall back to a parentless dialog.
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
        window: window.window_handle().map_err(|_| UNAVAILABLE)?,
        display: window.display_handle().map_err(|_| UNAVAILABLE)?,
    };
    Ok(present(&parent))
}
fn result_in_original(
    window: &(impl HasWindowHandle + HasDisplayHandle),
    result: MessageDialogResult,
    act: &str,
) -> Result<MessageDialogResult, String> {
    if ns::chose(&result, act) {
        checked(window, |_| ())?;
    }
    Ok(result)
}

fn choose(
    statement: Result<ns::NativeStatement, String>,
    dont: &str,
    act: &str,
    present: impl FnOnce(String, MessageDialogButtons) -> Result<MessageDialogResult, String>,
) -> Result<bool, String> {
    match statement {
        Ok(s) => ns::showing_in_app(s.in_app.as_ref(), || {
            present(s.text.clone(), ns::act_buttons(dont, act))
                .map(|result| ns::chose(&result, act))
        }),
        Err(cause) => {
            // Preserve the statement refusal even if its explanatory alert
            // cannot be displayed. Neither outcome is a person's cancellation.
            let _ = present(cause.clone(), MessageDialogButtons::Ok);
            Err(cause)
        }
    }
}

/// Called only by async IPC/workers. Validate, parent and schedule the sheet
/// in one main-thread turn; never block that thread awaiting the answer.
/// Stop supplies its IPC invoker; menu Quit supplies its already-retained main.
pub(crate) fn confirm(
    window: &tauri::Window,
    title: &str,
    statement: Result<ns::NativeStatement, String>,
    dont: &str,
    act: &str,
) -> Result<bool, String> {
    choose(statement, dont, act, |text, buttons| {
        let (send, receive) = mpsc::channel();
        let original = window.clone();
        let title = title.to_owned();
        let act = act.to_owned();
        window
            .run_on_main_thread(move || {
                let failure = send.clone();
                if let Err(error) = checked(&original, |parent| {
                    original
                        .dialog()
                        .message(text)
                        .title(title)
                        .kind(MessageDialogKind::Info)
                        .buttons(buttons)
                        .parent(parent)
                        .show_with_result({
                            let original = original.clone();
                            move |result| {
                                if !ns::chose(&result, &act) {
                                    let _ = send.send(Ok(result));
                                    return;
                                }
                                // The answer cannot authorize a lifecycle act if
                                // the original App window has since been destroyed.
                                let retained = original.clone();
                                let failure = send.clone();
                                if original
                                    .run_on_main_thread(move || {
                                        let _ =
                                            send.send(result_in_original(&retained, result, &act));
                                    })
                                    .is_err()
                                {
                                    let _ = failure.send(Err(UNAVAILABLE.into()));
                                }
                            }
                        });
                }) {
                    let _ = failure.send(Err(error));
                }
            })
            .map_err(|_| UNAVAILABLE.to_string())?;
        receive.recv().map_err(|_| {
            "Native lifecycle confirmation ended without a result; no act authorized".to_string()
        })?
    })
}

/// Explanatory Quit refusals also must not fall back to an unowned alert.
/// Logging remains available if the original window cannot present the notice.
pub(crate) fn notice(window: Option<&tauri::Window>, title: &str, message: String) {
    eprintln!("chirality: {message}");
    if let Some(window) = window {
        let _ = confirm(window, title, Err(message), "", "");
    }
}

#[cfg(test)]
#[path = "native_lifecycle_confirmation_tests.rs"]
mod tests;
