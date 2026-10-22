//! Desktop setup's invoking-window confirmation and confirmation-to-save join.
//! No window lookup, unparented fallback, persistence policy or live Root change.
use crate::{act_control::native_statement as ns, desktop_startup::DesktopSetup};
use raw_window_handle::{
    DisplayHandle, HandleError, HasDisplayHandle, HasWindowHandle, WindowHandle,
};
use serde_json::{json, Value};
use std::sync::{mpsc, Mutex};
use tauri_plugin_dialog::{DialogExt, MessageDialogKind, MessageDialogResult};

const TITLE: &str = "Desktop setup — next launch only";
const LEAVE: &str = "Leave setup unchanged";
#[cfg(test)]
const PREPARE: &str = "Prepare home and save for next launch";

/// Shared by the actual command and injected-confirmation fixtures. No controller
/// guard spans the pending dialog. Its reviewed effects and token stay frozen;
/// the one real prepare call revalidates its existing source/custody conditions.
pub(crate) fn prepare(
    controller: &Mutex<DesktopSetup>,
    preview_token: &str,
    confirm: impl FnOnce(&ns::NativeStatement, &str) -> Result<MessageDialogResult, String>,
) -> Result<Value, String> {
    let (effects, action) = {
        let controller = controller.try_lock().map_err(|_| "Desktop setup busy")?;
        (
            controller.preview_statement(preview_token)?,
            controller.preview_action(preview_token)?,
        )
    };
    let content = json!({"effects":effects});
    let statement = ns::whole_or_in_app(
        "Desktop setup",
        "desktop setup effects",
        effects.clone(),
        &content,
        |digest| {
            format!("{action}. Complete reviewed effects are shown in the App under Content named by an open native confirmation. sha-256: {digest}\nCurrent owners and choices stay unchanged; applies on next launch only.")
        },
    )?;
    let result = ns::showing_in_app(statement.in_app.as_ref(), || confirm(&statement, action))?;
    if !ns::chose(&result, action) {
        // The plugin also maps opaque backend Cancel to the cancel label; that
        // result grants no authority and cannot support a failure diagnosis.
        return Ok(json!({"state":"cancelled; no setup paths or saved request changed"}));
    }
    let mut controller = controller
        .try_lock()
        .map_err(|_| "Desktop setup busy after native question; preview again")?;
    if controller.preview_statement(preview_token)? != effects
        || controller.preview_action(preview_token)? != action
    {
        return Err("Desktop setup effects changed during confirmation; review again".into());
    }
    controller.prepare_and_save(preview_token)
}

/// The plugin's parent() silently ignores failed handle lookups. Only these
/// already successful borrowed handles are supplied to it, on the main thread.
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
fn with_checked_parent<T>(
    original: &(impl HasWindowHandle + HasDisplayHandle),
    present: impl FnOnce(&Parent<'_>) -> T,
) -> Result<T, String> {
    let parent = Parent {
        window: original
            .window_handle()
            .map_err(|_| "Invoking App window unavailable; desktop setup confirmation refused")?,
        display: original
            .display_handle()
            .map_err(|_| "Invoking App display unavailable; desktop setup confirmation refused")?,
    };
    Ok(present(&parent))
}
fn result_in_parent(
    original: &(impl HasWindowHandle + HasDisplayHandle),
    result: MessageDialogResult,
    action: &str,
) -> Result<MessageDialogResult, String> {
    if ns::chose(&result, action) {
        with_checked_parent(original, |_| ())?;
    }
    Ok(result)
}
fn receive_result(
    receive: mpsc::Receiver<Result<MessageDialogResult, String>>,
) -> Result<MessageDialogResult, String> {
    receive.recv().map_err(|_| {
        "Desktop setup confirmation ended without a result; no setup saved".to_string()
    })?
}

/// The IPC command supplies its actual invoker. Handle caching and parented
/// callback presentation share a main-thread turn; only the async worker waits.
pub(crate) fn confirm(
    invoking: &tauri::Window,
    statement: &ns::NativeStatement,
    action: &str,
) -> Result<MessageDialogResult, String> {
    let (send, receive) = mpsc::channel();
    let window = invoking.clone();
    let text = statement.text.clone();
    let action = action.to_owned();
    invoking.run_on_main_thread(move || {
        let callback_send = send.clone();
        let callback_window = window.clone();
        let shown = with_checked_parent(&window, |parent| {
            window.dialog().message(text).title(TITLE).kind(MessageDialogKind::Info)
                .buttons(ns::act_buttons(LEAVE, &action)).parent(parent)
                .show_with_result(move |result| {
                    if !ns::chose(&result, &action) {
                        let _ = callback_send.send(Ok(result));
                        return;
                    }
                    let original = callback_window.clone();
                    let failure = callback_send.clone();
                    if callback_window.run_on_main_thread(move || {
                        let _ = callback_send.send(result_in_parent(&original, result, &action));
                    }).is_err() {
                        let _ = failure.send(Err("Invoking App window could not be revalidated; desktop setup confirmation refused".into()));
                    }
                });
        });
        if let Err(error) = shown { let _ = send.send(Err(error)); }
    }).map_err(|_| "Invoking App window could not present desktop setup confirmation".to_string())?;
    receive_result(receive)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{
        cell::{Cell, RefCell},
        os::unix::fs::DirBuilderExt,
        path::PathBuf,
        time::Duration,
    };

    struct Fixture {
        root: PathBuf,
        data: PathBuf,
        shared: [PathBuf; 3],
        controller: Mutex<DesktopSetup>,
        token: String,
        home: PathBuf,
    }
    impl Fixture {
        fn admitted_project() -> Self {
            let mut f = Self::new(false);
            f.controller
                .lock()
                .unwrap()
                .prepare_and_save(&f.token)
                .unwrap();
            let mut fresh = DesktopSetup::new(
                Ok(f.data.clone()),
                Ok(f.root.join("invented-bundle-resources")),
            );
            let old = std::mem::replace(
                &mut f.controller,
                Mutex::new(DesktopSetup::new(
                    Err("unused fixture placeholder".into()),
                    Err("unused".into()),
                )),
            );
            drop(old);
            let launch = fresh.resolve(None, true, || {
                crate::runtime_session::allocate_fresh_probe(&f.root)
            });
            assert!(
                fresh
                    .admit_root(launch, Ok(f.data.clone()))
                    .allow_operational
            );
            let project = f.root.join("explicit-next-project");
            std::fs::create_dir(&project).unwrap();
            let preview = fresh.preview_project(Some(project)).unwrap();
            f.token = preview["token"].as_str().unwrap().into();
            f.home = PathBuf::from(preview["accountHome"].as_str().unwrap());
            f.controller = Mutex::new(fresh);
            f
        }
        fn new(long: bool) -> Self {
            let root = std::env::temp_dir()
                .canonicalize()
                .unwrap()
                .join(crate::util::opaque_id("desktop-confirm-fixture-").unwrap());
            std::fs::create_dir(&root).unwrap();
            let data = root.join("app-data");
            std::fs::DirBuilder::new()
                .mode(0o700)
                .create(&data)
                .unwrap();
            let sources = root.join("explicit-shared");
            std::fs::create_dir(&sources).unwrap();
            let tail = if long {
                "x".repeat(220)
            } else {
                "fixture".into()
            };
            let shared = [
                sources.join(format!("config-{tail}")),
                sources.join(format!("AGENTS-{tail}")),
                sources.join(format!("skills-{tail}")),
            ];
            std::fs::write(
                &shared[0],
                b"invented configuration; never read by this adapter",
            )
            .unwrap();
            std::fs::write(&shared[1], b"invented guidance; never read by this adapter").unwrap();
            std::fs::create_dir(&shared[2]).unwrap();
            let mut setup =
                DesktopSetup::new(Ok(data.clone()), Ok(root.join("invented-bundle-resources")));
            let preview = setup
                .preview(shared.clone(), None, "bundled-owner-use-development")
                .unwrap();
            Self {
                root,
                data,
                shared,
                token: preview["token"].as_str().unwrap().into(),
                home: PathBuf::from(preview["accountHome"].as_str().unwrap()),
                controller: Mutex::new(setup),
            }
        }
        fn profile(&self) -> PathBuf {
            self.data.join("desktop-startup/request.json")
        }
        fn home_count(&self) -> usize {
            match std::fs::read_dir(self.data.join("account-homes")) {
                Ok(entries) => entries.count(),
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => 0,
                Err(e) => panic!("fixture home census: {e}"),
            }
        }
        fn assert_unsaved(&self) {
            assert!(!self.profile().exists());
            assert!(!self.home.exists());
            assert_eq!(self.home_count(), 0);
        }
        fn new_preview(&mut self) {
            let preview = self
                .controller
                .lock()
                .unwrap()
                .preview(self.shared.clone(), None, "bundled-owner-use-development")
                .unwrap();
            self.token = preview["token"].as_str().unwrap().into();
            self.home = PathBuf::from(preview["accountHome"].as_str().unwrap());
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }

    struct HandleFixture {
        window_available: Cell<bool>,
        display_available: Cell<bool>,
        window_reads: Cell<usize>,
        display_reads: Cell<usize>,
        max_reads: usize,
    }
    impl HandleFixture {
        fn valid() -> Self {
            Self {
                window_available: Cell::new(true),
                display_available: Cell::new(true),
                window_reads: Cell::new(0),
                display_reads: Cell::new(0),
                max_reads: usize::MAX,
            }
        }
    }
    impl HasWindowHandle for HandleFixture {
        fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
            let reads = self.window_reads.get() + 1;
            self.window_reads.set(reads);
            if !self.window_available.get() || reads > self.max_reads {
                return Err(HandleError::Unavailable);
            }
            // SAFETY: Web IDs have no pointers and their validity is excluded
            // from raw-window-handle's borrow guarantees. Inspection ONLY: no
            // fake handle is ever passed to a platform/plugin/window consumer.
            Ok(unsafe {
                WindowHandle::borrow_raw(raw_window_handle::WebWindowHandle::new(29).into())
            })
        }
    }
    impl HasDisplayHandle for HandleFixture {
        fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
            let reads = self.display_reads.get() + 1;
            self.display_reads.set(reads);
            if !self.display_available.get() || reads > self.max_reads {
                return Err(HandleError::Unavailable);
            }
            Ok(DisplayHandle::web())
        }
    }
    fn affirmative() -> MessageDialogResult {
        MessageDialogResult::Custom(PREPARE.into())
    }
    // Inject only the native presentation/result boundary. These are the same
    // checked-parent/result functions used by confirm; all setup orchestration
    // and the actual OwnedHomePlan/private save remain the production prepare().
    fn injected_confirmation(
        original: &HandleFixture,
        result: MessageDialogResult,
        pending: impl FnOnce(),
    ) -> Result<MessageDialogResult, String> {
        with_checked_parent(original, |parent| {
            assert!(parent.window_handle().is_ok() && parent.display_handle().is_ok());
            pending();
        })?;
        result_in_parent(original, result, PREPARE)
    }

    #[test]
    fn retained_project_native_wait_refuses_external_pending_supersession() {
        use std::os::unix::fs::PermissionsExt;
        let f = Fixture::admitted_project();
        std::thread::scope(|scope| {
            let (ready_send, ready_receive) = mpsc::channel();
            let (resume_send, resume_receive) = mpsc::channel();
            let fixture = &f;
            let worker = scope.spawn(move || {
                let original = HandleFixture::valid();
                prepare(&fixture.controller, &fixture.token, |statement, action| {
                    with_checked_parent(&original, |_| ())?;
                    assert_eq!(action, "Save project for next launch");
                    assert!(!statement.text.contains("Create NEW"));
                    ready_send.send(()).unwrap();
                    resume_receive.recv_timeout(Duration::from_secs(5)).unwrap();
                    result_in_parent(
                        &original,
                        MessageDialogResult::Custom(action.into()),
                        action,
                    )
                })
            });
            ready_receive.recv_timeout(Duration::from_secs(5)).unwrap();
            assert!(f.controller.try_lock().is_ok());
            let bytes = std::fs::read(f.profile()).unwrap();
            std::fs::rename(f.profile(), f.root.join("original-private-request")).unwrap();
            std::fs::write(f.profile(), &bytes).unwrap();
            std::fs::set_permissions(f.profile(), std::fs::Permissions::from_mode(0o600)).unwrap();
            resume_send.send(()).unwrap();
            assert!(worker
                .join()
                .unwrap()
                .unwrap_err()
                .contains("Pending desktop request"));
            assert_eq!(std::fs::read(f.profile()).unwrap(), bytes);
            assert_eq!(f.home_count(), 1);
        });
    }

    #[test]
    fn retained_project_confirmation_uses_its_exact_action_and_original_parent() {
        for outcome in ["default", "new-home-action", "destroyed", "affirmative"] {
            let f = Fixture::admitted_project();
            let original = HandleFixture::valid();
            let before = std::fs::read(f.profile()).unwrap();
            let result = prepare(&f.controller, &f.token, |statement, action| {
                assert_eq!(action, "Save project for next launch");
                assert!(!statement.text.contains("Create NEW"));
                with_checked_parent(&original, |_| ())?;
                let result = match outcome {
                    "default" => MessageDialogResult::Custom(LEAVE.into()),
                    "new-home-action" => MessageDialogResult::Custom(PREPARE.into()),
                    "destroyed" => {
                        original.window_available.set(false);
                        MessageDialogResult::Custom(action.into())
                    }
                    _ => MessageDialogResult::Custom(action.into()),
                };
                result_in_parent(&original, result, action)
            });
            match outcome {
                "affirmative" => {
                    assert_eq!(result.unwrap()["pending"]["kind"], "retain-account-project");
                    assert_ne!(std::fs::read(f.profile()).unwrap(), before);
                }
                "destroyed" => {
                    assert!(result.is_err());
                    assert_eq!(std::fs::read(f.profile()).unwrap(), before);
                }
                _ => {
                    assert!(result.unwrap()["state"]
                        .as_str()
                        .unwrap()
                        .contains("cancelled"));
                    assert_eq!(std::fs::read(f.profile()).unwrap(), before);
                }
            }
            assert_eq!(f.home_count(), 1);
        }
    }

    #[test]
    fn caches_both_successful_handles_before_parenting_without_fallible_relookup() {
        let original = HandleFixture {
            max_reads: 1,
            ..HandleFixture::valid()
        };
        with_checked_parent(&original, |parent| {
            for _ in 0..2 {
                assert_eq!(
                    parent.window_handle().unwrap().as_raw(),
                    raw_window_handle::WebWindowHandle::new(29).into()
                );
                assert_eq!(parent.display_handle().unwrap(), DisplayHandle::web());
            }
        })
        .unwrap();
        assert_eq!(
            (original.window_reads.get(), original.display_reads.get()),
            (1, 1)
        );
    }

    #[test]
    fn missing_window_or_display_refuses_before_presentation_or_save() {
        for missing in ["window", "display"] {
            let f = Fixture::new(false);
            let original = HandleFixture::valid();
            if missing == "window" {
                original.window_available.set(false);
            } else {
                original.display_available.set(false);
            }
            let presented = Cell::new(false);
            let error = prepare(&f.controller, &f.token, |_, _| {
                injected_confirmation(&original, affirmative(), || presented.set(true))
            })
            .unwrap_err();
            assert!(error.contains(&format!("Invoking App {missing} unavailable")));
            assert!(!presented.get());
            f.assert_unsaved();
        }
    }

    #[test]
    fn destroyed_original_window_or_display_cannot_be_replaced_before_affirmative_save() {
        for missing in ["window", "display"] {
            let f = Fixture::new(false);
            let original = HandleFixture::valid();
            let replacement = HandleFixture::valid();
            let error = prepare(&f.controller, &f.token, |_, _| {
                injected_confirmation(&original, affirmative(), || {
                    if missing == "window" {
                        original.window_available.set(false);
                    } else {
                        original.display_available.set(false);
                    }
                })
            })
            .unwrap_err();
            assert!(error.contains(&format!("Invoking App {missing} unavailable")));
            assert_eq!(
                (
                    replacement.window_reads.get(),
                    replacement.display_reads.get()
                ),
                (0, 0)
            );
            assert_eq!(original.window_reads.get(), 2);
            f.assert_unsaved();
        }
    }

    #[test]
    fn default_cancel_close_and_nonexact_results_never_save() {
        let buttons = ns::act_buttons(LEAVE, PREPARE);
        let tauri_plugin_dialog::MessageDialogButtons::YesNoCancelCustom(default, act, cancel) =
            &buttons
        else {
            panic!("default-safe layout changed")
        };
        assert_eq!(
            (default.as_str(), act.as_str(), cancel.as_str()),
            (LEAVE, PREPARE, "Cancel")
        );
        assert_eq!(TITLE, "Desktop setup — next launch only");
        let mut results = ns::dialog_model::outcomes(&buttons)
            .into_iter()
            .filter(|(_, result)| !ns::chose(result, PREPARE))
            .map(|(_, result)| result)
            .collect::<Vec<_>>();
        results.extend([
            MessageDialogResult::Cancel,
            MessageDialogResult::Ok,
            MessageDialogResult::Yes,
            MessageDialogResult::No,
            MessageDialogResult::Custom(PREPARE.to_lowercase()),
            MessageDialogResult::Custom(format!("{PREPARE} ")),
        ]);
        for result in results {
            let f = Fixture::new(false);
            let original = HandleFixture::valid();
            let outcome = prepare(&f.controller, &f.token, |_, _| {
                injected_confirmation(&original, result, || {})
            })
            .unwrap();
            assert_eq!(
                outcome["state"],
                "cancelled; no setup paths or saved request changed"
            );
            assert_eq!(original.window_reads.get(), 1);
            f.assert_unsaved();
        }
    }

    #[test]
    fn exact_affirmative_rechecks_original_and_reaches_one_real_prepare_save() {
        let f = Fixture::new(false);
        let original = HandleFixture::valid();
        let initial = f.controller.lock().unwrap().view()["launch"].clone();
        let result = prepare(&f.controller, &f.token, |_, _| {
            injected_confirmation(&original, affirmative(), || f.assert_unsaved())
        })
        .unwrap();
        assert_eq!(
            (original.window_reads.get(), original.display_reads.get()),
            (2, 2)
        );
        assert_eq!(result["pending"]["state"], "saved-for-next-launch");
        assert_eq!(result["launch"], initial, "no hot launch/source promotion");
        assert_eq!(f.home_count(), 1);
        assert!(f.profile().is_file());
        for (slot, target) in ["config.toml", "AGENTS.md", "skills"]
            .into_iter()
            .zip(&f.shared)
        {
            assert_eq!(std::fs::read_link(f.home.join(slot)).unwrap(), *target);
        }
        assert!(!f.home.join("auth.json").exists());
        let saved = std::fs::read(f.profile()).unwrap();
        assert!(prepare(&f.controller, &f.token, |_, _| panic!(
            "consumed token presented again"
        ))
        .is_err());
        assert_eq!(f.home_count(), 1);
        assert_eq!(std::fs::read(f.profile()).unwrap(), saved);
    }

    #[test]
    fn changed_token_source_or_held_custody_refuses_after_confirmation_without_save() {
        for mutation in ["token", "source", "custody"] {
            let mut f = Fixture::new(false);
            if mutation == "custody" {
                f.controller
                    .lock()
                    .unwrap()
                    .prepare_and_save(&f.token)
                    .unwrap();
                f.new_preview();
            }
            let homes_before = f.home_count();
            let original = HandleFixture::valid();
            let result = prepare(&f.controller, &f.token, |_, _| {
                injected_confirmation(&original, affirmative(), || match mutation {
                    "token" => {
                        f.controller
                            .lock()
                            .unwrap()
                            .preview(f.shared.clone(), None, "bundled-owner-use-development")
                            .unwrap();
                    }
                    "source" => {
                        std::fs::rename(&f.shared[0], f.shared[0].with_extension("old")).unwrap();
                        std::fs::write(&f.shared[0], b"replacement invented source").unwrap();
                    }
                    "custody" => {
                        std::fs::rename(
                            f.data.join("desktop-startup"),
                            f.data.join("retained-original-profile"),
                        )
                        .unwrap();
                        std::fs::DirBuilder::new()
                            .mode(0o700)
                            .create(f.data.join("desktop-startup"))
                            .unwrap();
                    }
                    _ => unreachable!(),
                })
            });
            assert!(result.is_err(), "{mutation}");
            assert!(!f.profile().exists(), "{mutation}");
            assert!(!f.home.exists(), "{mutation}");
            assert_eq!(f.home_count(), homes_before, "{mutation}");
        }
    }

    #[test]
    fn busy_controller_and_known_presentation_or_result_failures_remain_errors() {
        let f = Fixture::new(false);
        let held = f.controller.lock().unwrap();
        assert!(prepare(&f.controller, &f.token, |_, _| panic!(
            "busy controller presented"
        ))
        .unwrap_err()
        .contains("busy"));
        drop(held);
        for disconnected in [false, true] {
            let error = prepare(&f.controller, &f.token, |_, _| {
                if !disconnected {
                    return Err("invented main-thread presentation dispatch failed".into());
                }
                let (send, receive) = mpsc::channel();
                drop(send);
                receive_result(receive)
            })
            .unwrap_err();
            assert!(error.contains(if disconnected {
                "without a result"
            } else {
                "presentation dispatch failed"
            }));
            f.assert_unsaved();
        }
        let held = RefCell::new(None);
        let original = HandleFixture::valid();
        let error = prepare(&f.controller, &f.token, |_, _| {
            injected_confirmation(&original, affirmative(), || {
                *held.borrow_mut() = Some(f.controller.lock().unwrap());
            })
        })
        .unwrap_err();
        assert!(error.contains("busy after native question"));
        drop(held);
        f.assert_unsaved();
    }

    #[test]
    fn long_reviewed_content_and_digest_stay_whole_while_injected_confirmation_is_pending() {
        let f = Fixture::new(true);
        let effects = f
            .controller
            .lock()
            .unwrap()
            .preview_statement(&f.token)
            .unwrap();
        assert!(effects.chars().count() > ns::MAX_CHARS);
        let before = ns::shown_in_app();
        std::thread::scope(|scope| {
            let (ready_send, ready_receive) = mpsc::channel();
            let (resume_send, resume_receive) = mpsc::channel();
            let fixture = &f;
            let worker = scope.spawn(move || {
                let original = HandleFixture::valid();
                prepare(&fixture.controller, &fixture.token, |statement, _| {
                    with_checked_parent(&original, |_| ())?;
                    let content = statement
                        .in_app
                        .as_ref()
                        .ok_or("long effects were not retained whole")?;
                    ready_send
                        .send((statement.text.clone(), content.digest.clone()))
                        .map_err(|e| e.to_string())?;
                    let result = resume_receive
                        .recv_timeout(Duration::from_secs(5))
                        .map_err(|e| e.to_string())?;
                    result_in_parent(&original, result, PREPARE)
                })
            });
            let (native, digest) = ready_receive.recv_timeout(Duration::from_secs(5)).unwrap();
            assert!(native.contains(&digest));
            let shown = ns::shown_in_app();
            let full = shown
                .as_array()
                .unwrap()
                .iter()
                .find(|v| v["digest"] == digest)
                .unwrap();
            assert_eq!(full["content"], json!({"effects":effects}));
            assert_eq!(
                ns::content_digest("Desktop setup", &full["content"]).unwrap(),
                digest
            );
            assert!(
                f.controller.try_lock().is_ok(),
                "pending native confirmation must not retain the setup lock"
            );
            f.assert_unsaved();
            resume_send.send(affirmative()).unwrap();
            assert_eq!(
                worker.join().unwrap().unwrap()["pending"]["state"],
                "saved-for-next-launch"
            );
        });
        assert_eq!(
            ns::shown_in_app(),
            before,
            "whole content withdrawn after pending result"
        );
        assert_eq!(f.home_count(), 1);
    }
}
