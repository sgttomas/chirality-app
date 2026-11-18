//! Stop/Restart and Quit questions attached to their retained App window.
//! No parentless fallback: rfd's macOS parentless path is a CF user alert,
//! whereas a supplied parent selects the App's NSAlert sheet path.
use crate::act_control::native_statement as ns;
use raw_window_handle::{
    DisplayHandle, HandleError, HasDisplayHandle, HasWindowHandle, WindowHandle,
};
use std::io::Write;
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::sync::mpsc;
use tauri::Runtime;
use tauri_plugin_dialog::{
    DialogExt, MessageDialogButtons, MessageDialogKind, MessageDialogResult,
};

const UNAVAILABLE: &str = "Original App window unavailable; native lifecycle confirmation refused";
/// The refusal a waiting caller receives when work posted for its question
/// faults. It is an `Err`, never an answer: no caller reads it as Keep running
/// or as the act.
pub(crate) const FAULTED: &str = "A fault interrupted the native lifecycle confirmation; no act authorized";

type Reply<T> = mpsc::Sender<Result<T, String>>;

/// Run work where it was posted. An unwind stops here instead of reaching the
/// event loop: the waiting caller receives [`FAULTED`] and a best-effort line
/// goes to standard error. A fault never sends `Ok`.
fn contained<T>(reply: &Reply<T>, work: impl FnOnce()) {
    if let Err(payload) = catch_unwind(AssertUnwindSafe(work)) {
        // Dropping the payload could run code that unwinds again here.
        std::mem::forget(payload);
        let _ = writeln!(std::io::stderr(), "chirality: {FAULTED}");
        let _ = reply.send(Err(FAULTED.into()));
    }
}

/// Post `work` to the main thread with its fault contained. Every main-thread
/// task of this module goes through here.
fn post<R: Runtime, T: Send + 'static>(
    window: &tauri::Window<R>,
    reply: Reply<T>,
    work: impl FnOnce(Reply<T>) + Send + 'static,
) -> Result<(), String> {
    window
        .run_on_main_thread(move || {
            let fault = reply.clone();
            contained(&fault, move || work(reply))
        })
        .map_err(|_| UNAVAILABLE.to_owned())
}

/// Post `work` and wait, off the main thread, for its one result.
fn ask<R: Runtime, T: Send + 'static>(
    window: &tauri::Window<R>,
    ended: &str,
    work: impl FnOnce(Reply<T>) + Send + 'static,
) -> Result<T, String> {
    let (send, receive) = mpsc::channel();
    post(window, send, work)?;
    receive.recv().map_err(|_| ended.to_owned())?
}

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
/// A fault in the posted work, or in the answer's handling, is a refusal.
pub(crate) fn confirm<R: Runtime>(
    window: &tauri::Window<R>,
    title: &str,
    statement: Result<ns::NativeStatement, String>,
    dont: &str,
    act: &str,
) -> Result<bool, String> {
    choose(statement, dont, act, |text, buttons| {
        let original = window.clone();
        let title = title.to_owned();
        let act = act.to_owned();
        ask(
            window,
            "Native lifecycle confirmation ended without a result; no act authorized",
            move |send| {
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
                                let fault = send.clone();
                                contained(&fault, move || answered(&original, result, act, send))
                            }
                        });
                }) {
                    let _ = failure.send(Err(error));
                }
            },
        )
    })
}

/// The dialog's answer. Anything but the act is sent as it is. The act cannot
/// authorize a lifecycle act if the original App window has since been
/// destroyed, which is checked on the main thread.
fn answered<R: Runtime>(
    original: &tauri::Window<R>,
    result: MessageDialogResult,
    act: String,
    send: Reply<MessageDialogResult>,
) {
    if !ns::chose(&result, &act) {
        let _ = send.send(Ok(result));
        return;
    }
    let retained = original.clone();
    let failure = send.clone();
    if post(original, send, move |send| {
        let _ = send.send(result_in_original(&retained, result, &act));
    })
    .is_err()
    {
        let _ = failure.send(Err(UNAVAILABLE.into()));
    }
}

/// Read-only final check for a retained original, from an off-main-thread
/// worker. This establishes handle availability at this check, not an atomic
/// lifetime lease throughout subsequent provider work. Never reselect a window.
pub(crate) fn revalidate_original<R: Runtime>(window: &tauri::Window<R>) -> Result<(), String> {
    let original = window.clone();
    ask(window, "Original-window validation ended without a result", move |send| {
        let _ = send.send(checked(&original, |_| ()));
    })
}

/// A caller that keeps a refusal apart from the answer: the refusal is kept
/// for its report and the act is not chosen.
pub(crate) fn refusal_kept(refused: &mut Option<String>, answer: Result<bool, String>) -> bool {
    match answer {
        Ok(chosen) => chosen,
        Err(cause) => {
            *refused = Some(cause);
            false
        }
    }
}

/// Explanatory Quit refusals also must not fall back to an unowned alert.
/// Logging remains available if the original window cannot present the notice.
pub(crate) fn notice(window: Option<&tauri::Window>, title: &str, message: String) {
    // Ignore stderr write errors. The notice still tries to use the retained
    // window.
    crate::app_quit::diagnostic(&message);
    if let Some(window) = window {
        let _ = confirm(window, title, Err(message), "", "");
    }
}

#[cfg(test)]
#[path = "native_lifecycle_confirmation_tests.rs"]
mod tests;

// Staged backend: lifetime/presentation selection precedes production wiring.
#[cfg(target_os = "macos")]
#[path = "lifecycle_sheet_lease.rs"]
mod lease;
#[cfg(target_os = "macos")]
#[path = "lifecycle_sheet_macos.rs"]
mod macos;
