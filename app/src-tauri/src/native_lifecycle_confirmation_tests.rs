//! Offline stand-ins only. No platform handles are dereferenced or dialogs shown.
use super::*;
use std::cell::Cell;

struct Handles {
    available: Cell<bool>,
    window_reads: Cell<usize>,
    display_reads: Cell<usize>,
    display: bool,
}
impl Handles {
    fn new(display: bool) -> Self {
        Self {
            available: Cell::new(true),
            window_reads: Cell::new(0),
            display_reads: Cell::new(0),
            display,
        }
    }
}
impl HasWindowHandle for Handles {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
        self.window_reads.set(self.window_reads.get() + 1);
        if !self.available.get() {
            return Err(HandleError::Unavailable);
        }
        // Web IDs contain no pointer; fixtures never pass them to native code.
        Ok(unsafe { WindowHandle::borrow_raw(raw_window_handle::WebWindowHandle::new(17).into()) })
    }
}
impl HasDisplayHandle for Handles {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
        self.display_reads.set(self.display_reads.get() + 1);
        if self.display {
            Ok(DisplayHandle::web())
        } else {
            Err(HandleError::Unavailable)
        }
    }
}
fn statement() -> Result<ns::NativeStatement, String> {
    ns::codex_stop_statement(&serde_json::json!({
        "generation":{"appSession":"fixture-session","home":"fixture-home","spawnCounter":1},
        "modeHomeClass":"account", "state":"ready", "notReady":null,
        "observedLiveTurns":[], "observedOutstandingRequests":[], "observedActiveChildren":[],
        "knownChildActivityUnknown":[], "coverage":{"turns":{"unresolved":[]}}, "runsInForce":[]
    }))
}
#[test]
fn parent_caches_both_handles_before_plugin_lookup() {
    let original = Handles::new(true);
    checked(&original, |parent| {
        original.available.set(false);
        for _ in 0..2 {
            assert_eq!(
                parent.window_handle().unwrap().as_raw(),
                raw_window_handle::WebWindowHandle::new(17).into()
            );
            assert_eq!(parent.display_handle().unwrap(), DisplayHandle::web());
        }
    })
    .unwrap();
    assert_eq!(original.window_reads.get(), 1);
    assert_eq!(original.display_reads.get(), 1);
}
#[test]
fn unavailable_window_or_display_never_presents() {
    for display in [false, true] {
        let original = Handles::new(display);
        original.available.set(!display);
        assert!(checked(&original, |_| panic!("must not present parentless")).is_err());
    }
}
#[test]
fn destroyed_original_refuses_affirmative_without_reselection() {
    let original = Handles::new(true);
    checked(&original, |_| ()).unwrap();
    original.available.set(false);
    assert!(result_in_original(
        &original,
        MessageDialogResult::Custom(ns::STOP_CODEX.into()),
        ns::STOP_CODEX
    )
    .is_err());
    // Dismissal never becomes an act, even if the original has gone away.
    assert!(matches!(
        result_in_original(&original, MessageDialogResult::Cancel, ns::STOP_CODEX).unwrap(),
        MessageDialogResult::Cancel
    ));
}
#[test]
fn only_explicit_act_proceeds_for_stop_restart_and_quit() {
    for (dont, act) in [
        (ns::KEEP_CODEX, ns::STOP_CODEX),
        (ns::KEEP_CODEX, ns::RESTART_CODEX),
        (ns::KEEP_RUNNING, ns::QUIT_APP),
    ] {
        for (how, result) in ns::dialog_model::outcomes(&ns::act_buttons(dont, act)) {
            let result = choose(statement(), dont, act, |text, buttons| {
                assert!(text.contains("fixture-session"));
                assert_eq!(
                    format!("{buttons:?}"),
                    format!("{:?}", ns::act_buttons(dont, act))
                );
                Ok(result)
            })
            .unwrap();
            assert_eq!(result, how == "middle");
        }
    }
}
#[test]
fn presentation_failure_is_refusal_not_cancellation() {
    assert_eq!(
        choose(statement(), ns::KEEP_CODEX, ns::STOP_CODEX, |_, _| Err(
            UNAVAILABLE.into()
        ))
        .unwrap_err(),
        UNAVAILABLE
    );
}
#[test]
fn invalid_statement_stays_refusal_with_or_without_explanatory_alert() {
    for display in [true, false] {
        let result = choose(
            Err("statement unavailable".into()),
            ns::KEEP_CODEX,
            ns::STOP_CODEX,
            |text, buttons| {
                assert_eq!(text, "statement unavailable");
                assert!(matches!(buttons, MessageDialogButtons::Ok));
                if display {
                    Ok(MessageDialogResult::Ok)
                } else {
                    Err(UNAVAILABLE.into())
                }
            },
        );
        assert_eq!(result.unwrap_err(), "statement unavailable");
    }
}

// The posted side of the question, on Tauri's mock runtime. Before the mock
// event loop runs, it executes a posted task in place, on the calling thread,
// so an unwind that escaped `post` would fail the test. No dialog plugin is
// registered and no native window exists.
fn mock_window() -> (tauri::App<tauri::test::MockRuntime>, tauri::Window<tauri::test::MockRuntime>) {
    let app = tauri::test::mock_app();
    let window = tauri::WebviewWindowBuilder::new(&app, "main", tauri::WebviewUrl::App("index.html".into()))
        .build()
        .unwrap()
        .as_ref()
        .window()
        .clone();
    (app, window)
}
#[test]
fn a_fault_in_posted_work_is_contained_and_sent_as_the_refusal() {
    let (_app, window) = mock_window();
    let (send, receive) = mpsc::channel::<Result<bool, String>>();
    post(&window, send, |_send| panic!("injected fault on the executing side")).unwrap();
    assert_eq!(receive.recv().unwrap().unwrap_err(), FAULTED);
    assert!(receive.recv().is_err(), "one result, and no Ok");
    let (send, receive) = mpsc::channel::<Result<bool, String>>();
    post(&window, send, |send| {
        let _ = send.send(Ok(false));
    })
    .unwrap();
    assert_eq!(receive.recv().unwrap(), Ok(false), "work that does not fault is unchanged");
}
#[test]
fn a_fault_presenting_the_question_is_a_refusal_for_stop_restart_and_quit() {
    // The posted presentation validates the original, then looks up the
    // dialog plugin, which this mock App never registered: that lookup panics
    // inside the posted closure.
    let (_app, window) = mock_window();
    for (dont, act) in [
        (ns::KEEP_CODEX, ns::STOP_CODEX),
        (ns::KEEP_CODEX, ns::RESTART_CODEX),
        (ns::KEEP_RUNNING, ns::QUIT_APP),
        ("Keep verified approval", "Allow disk records"),
    ] {
        assert_eq!(confirm(&window, "fixture", statement(), dont, act).unwrap_err(), FAULTED);
    }
}
#[test]
fn the_answer_is_handled_with_its_fault_contained() {
    let (_app, window) = mock_window();
    for (result, chosen) in [
        (MessageDialogResult::Custom(ns::STOP_CODEX.into()), true),
        (MessageDialogResult::Custom(ns::KEEP_CODEX.into()), false),
        (MessageDialogResult::Cancel, false),
    ] {
        let (send, receive) = mpsc::channel();
        answered(&window, result, ns::STOP_CODEX.into(), send);
        assert_eq!(ns::chose(&receive.recv().unwrap().unwrap(), ns::STOP_CODEX), chosen);
    }
    // The dialog's callback runs `answered` inside `contained`.
    let (send, receive) = mpsc::channel::<Result<MessageDialogResult, String>>();
    contained(&send, || panic!("injected fault while handling the answer"));
    assert_eq!(receive.recv().unwrap().unwrap_err(), FAULTED);
    assert!(revalidate_original(&window).is_ok());
}
#[test]
fn callers_keep_the_fault_refusal_apart_from_the_answer() {
    // Stop and Restart Codex (lib.rs `codex_stop`).
    let mut refused = None;
    assert!(!refusal_kept(&mut refused, Err(FAULTED.into())));
    assert_eq!(refused.as_deref(), Some(FAULTED));
    let mut refused = None;
    assert!(!refusal_kept(&mut refused, Ok(false)));
    assert!(refused.is_none(), "Keep Codex is not a refusal");
    // Workflow approval: only Ok(true) is the lowering.
    let lower = |answer: Result<bool, String>| {
        crate::act_control::assurance_lowering("fixture-settings".into(), 3, true, move |_| answer)
    };
    assert_eq!(lower(Err(FAULTED.into())).err().as_deref(), Some(FAULTED));
    assert!(lower(Ok(false)).unwrap().is_none());
    assert!(lower(Ok(true)).unwrap().unwrap().matches("fixture-settings", 3));
}
