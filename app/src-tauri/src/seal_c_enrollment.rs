//! Menu-event joining of the inactive SEAL-C prepared provider intent.
//! Menu-event origin is not authenticated: existing core:menu permissions may
//! let web content request a question, never answer it or supply provider authority.
//! No direct SEAL-C command/MCP/CLI/path input or startup enrollment. None hides AND
//! rejects dispatch. The provider still owns signature, policy and filesystem
//! revalidation; this module owns the question and key_setup/Quit ordering.
use crate::{
    act_control::native_statement as ns, app_quit::AppQuit, capture_seal_keychain as provider,
};
use serde_json::Value;
use std::sync::{
    atomic::{AtomicBool, Ordering},
    Mutex,
};
use tauri::Manager;

pub(crate) const MENU_ID: &str = "chirality-prepare-capture-sealing";
const TITLE: &str = "Prepare capture sealing";
const LEAVE: &str = "Leave unchanged";
const PREPARE: &str = "Prepare capture sealing";

pub(crate) fn menu_entry() -> Option<(&'static str, &'static str)> {
    provider::enrollment_compiled_available().then_some((MENU_ID, "Prepare capture sealing…"))
}
fn dispatch_if_configured(action: impl FnOnce()) {
    if menu_entry().is_some() {
        action();
    }
}
struct Questions {
    active: AtomicBool,
}
impl Questions {
    const fn new() -> Self {
        Self {
            active: AtomicBool::new(false),
        }
    }
    fn acquire(&self) -> Result<Question<'_>, String> {
        self.active
            .compare_exchange(false, true, Ordering::SeqCst, Ordering::SeqCst)
            .map(|_| Question { owner: self })
            .map_err(|_| "Capture sealing question already pending".into())
    }
}
struct Question<'a> {
    owner: &'a Questions,
}
impl Drop for Question<'_> {
    fn drop(&mut self) {
        self.owner.active.store(false, Ordering::SeqCst);
    }
}
static QUESTIONS: Questions = Questions::new();

#[derive(Debug, PartialEq, Eq)]
enum Outcome {
    Cancelled,
    ProviderReturnedSuccess,
}
fn quit_clear(quit: &AppQuit) -> Result<(), String> {
    if quit.busy() || quit.proceeding().is_some() {
        return Err("The App is quitting; capture sealing was not started".into());
    }
    Ok(())
}
/// Shared actual ordering and injected source tests. There is no successful
/// path around the same native choice, actual key mutex and actual Quit state.
fn coordinate<I>(
    _question: &Question<'_>,
    key_setup: &Mutex<()>,
    quit: &AppQuit,
    prepare: impl FnOnce() -> Result<I, String>,
    confirm: impl FnOnce(&I) -> Result<bool, String>,
    revalidate_original: impl FnOnce() -> Result<(), String>,
    consume: impl FnOnce(I) -> Result<(), String>,
) -> Result<Outcome, String> {
    quit_clear(quit)?;
    let intent = prepare()?;
    // Neither key_setup nor provider locks span the human question.
    if !confirm(&intent)? {
        return Ok(Outcome::Cancelled);
    }
    quit_clear(quit)?; // preserve the actual Quit refusal before contention wording
    let _key_setup = key_setup.try_lock().map_err(|error| match error {
        std::sync::TryLockError::WouldBlock => {
            "Another explicit key operation is pending; capture sealing was not started"
        }
        std::sync::TryLockError::Poisoned(_) => {
            "Key-operation admission is unavailable; capture sealing was not started"
        }
    })?;
    // Keep the shared mutex guard outside the unwind boundary for every final
    // admission/provider operation. Unexpected failure is unknown, never retry;
    // it must not poison unrelated key setup or permanently block menu Quit.
    std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        quit_clear(quit)?;
        revalidate_original()?;
        // Main-thread window validation is an interval: check Quit again.
        quit_clear(quit)?;
        consume(intent)?;
        Ok(Outcome::ProviderReturnedSuccess)
    }))
    .map_err(|_| "Capture sealing ended unexpectedly; outcome unknown; not retried".to_owned())?
}
fn statement(preview: &Value) -> Result<ns::NativeStatement, String> {
    let field = |name| {
        preview[name]
            .as_str()
            .ok_or_else(|| format!("Prepared capture-seal {name} unavailable"))
    };
    let marker = if preview["marker"].is_null() {
        "none observed".to_owned()
    } else {
        preview["marker"].to_string()
    };
    let whole=format!("Prepare capture sealing for this installation?\nLocation: {}\nService: {}\nAccount: {}\nAccess group: {}\nCommitted and pending key IDs: {}\nExisting keys are retained. Development keys are not imported.",
        field("app_data")?,field("service")?,field("account")?,field("access_group")?,marker);
    ns::whole_or_in_app(
        "Capture sealing",
        "prepared capture-seal installation",
        whole,
        preview,
        |digest| {
            format!(
        "Prepare capture sealing for the installation shown in the App under Content named by an open native confirmation? sha-256: {digest}\nExisting keys are retained; development keys are not imported.")
        },
    )
}

/// Called only from lib.rs's native menu event. Retain main once, before the
/// worker; never resolve a focused/first/replacement window after preparation.
pub(crate) fn request(app: tauri::AppHandle) {
    dispatch_if_configured(|| {
        let original = app
            .get_webview_window("main")
            .map(|w| w.as_ref().window().clone());
        let Ok(question) = QUESTIONS.acquire() else {
            return;
        };
        std::thread::spawn(move || {
            // A second event during prepare/question/consume is ignored, never
            // queued for a later automatic retry. Result notices grant no act.
            let _question = question;
            let result = (|| {
                let window = original
                    .as_ref()
                    .ok_or("Original App window unavailable; capture sealing refused")?;
                let state = app
                    .try_state::<crate::AppState>()
                    .ok_or("App state unavailable; capture sealing refused")?;
                coordinate(
                    &_question,
                    &state.key_setup,
                    &state.app_quit,
                    || {
                        crate::native_lifecycle_confirmation::revalidate_original(window)?;
                        // Request visibility only for the retained original; a
                        // successful call is not a foreground/native witness.
                        window
                            .unminimize()
                            .map_err(|_| "Original App window could not be restored")?;
                        window
                            .show()
                            .map_err(|_| "Original App window could not be shown")?;
                        window
                            .set_focus()
                            .map_err(|_| "Original App window focus request failed")?;
                        provider::prepare_enrollment()
                    },
                    |intent| {
                        crate::native_lifecycle_confirmation::confirm(
                            window,
                            TITLE,
                            statement(&intent.preview()),
                            LEAVE,
                            PREPARE,
                        )
                    },
                    || crate::native_lifecycle_confirmation::revalidate_original(window),
                    provider::enroll_initial,
                )
            })();
            drop(_question); // cancellation/error/success release admission before notice
            match result {
                Ok(Outcome::Cancelled) => (),
                Ok(Outcome::ProviderReturnedSuccess) => {
                    crate::native_lifecycle_confirmation::notice(
                        original.as_ref(),
                        TITLE,
                        "Capture sealing check completed for the prepared installation.".into(),
                    )
                }
                Err(reason) => {
                    crate::native_lifecycle_confirmation::notice(original.as_ref(), TITLE, reason)
                }
            }
        });
    });
}

#[cfg(test)]
#[path = "seal_c_enrollment_tests.rs"]
mod tests;
