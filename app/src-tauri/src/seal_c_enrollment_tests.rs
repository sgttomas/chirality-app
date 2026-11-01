//! Actual caller gates with invented one-use subjects and injected presentation.
//! No App instance, native dialog, SecItem, signing or supplier execution.
use super::*;
use std::{
    cell::RefCell,
    sync::{atomic::AtomicUsize, Arc},
};
struct Intent {
    id: u64,
    drops: Arc<AtomicUsize>,
}
impl Drop for Intent {
    fn drop(&mut self) {
        self.drops.fetch_add(1, Ordering::SeqCst);
    }
}
fn intent(drops: &Arc<AtomicUsize>) -> Intent {
    Intent {
        id: 17,
        drops: drops.clone(),
    }
}
fn run<I>(
    questions: &Questions,
    key: &Mutex<()>,
    quit: &AppQuit,
    prepare: impl FnOnce() -> Result<I, String>,
    confirm: impl FnOnce(&I) -> Result<bool, String>,
    window: impl FnOnce() -> Result<(), String>,
    consume: impl FnOnce(I) -> Result<(), String>,
) -> Result<Outcome, String> {
    let question = questions.acquire()?;
    coordinate(&question, key, quit, prepare, confirm, window, consume)
}
#[test]
fn seal_enrollment_none_hides_and_rejects_dispatch_without_preparation() {
    assert!(menu_entry().is_none());
    assert!(!provider::enrollment_compiled_available());
    dispatch_if_configured(|| panic!("None must not resolve a window, spawn a worker or prepare"));
}
#[test]
fn seal_enrollment_question_holds_no_key_lock_and_consumes_same_intent_once() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let drops = Arc::new(AtomicUsize::new(0));
    let events = RefCell::new(vec![]);
    let result = run(
        &q,
        &key,
        &quit,
        || {
            events.borrow_mut().push("prepare");
            Ok(intent(&drops))
        },
        |p| {
            assert_eq!(p.id, 17);
            assert!(key.try_lock().is_ok(), "no key lock across question");
            assert!(q.acquire().is_err(), "one question only");
            events.borrow_mut().push("confirm");
            Ok(true)
        },
        || {
            assert!(matches!(
                key.try_lock(),
                Err(std::sync::TryLockError::WouldBlock)
            ));
            events.borrow_mut().push("window");
            Ok(())
        },
        |p| {
            assert_eq!(p.id, 17);
            assert!(matches!(
                key.try_lock(),
                Err(std::sync::TryLockError::WouldBlock)
            ));
            events.borrow_mut().push("consume");
            Ok(())
        },
    )
    .unwrap();
    assert_eq!(result, Outcome::ProviderReturnedSuccess);
    assert_eq!(
        *events.borrow(),
        vec!["prepare", "confirm", "window", "consume"]
    );
    assert_eq!(drops.load(Ordering::SeqCst), 1);
    assert!(key.try_lock().is_ok());
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_cancel_and_presentation_error_drop_subject_and_release_question() {
    for fail in [false, true] {
        let q = Questions::new();
        let key = Mutex::new(());
        let quit = AppQuit::default();
        let drops = Arc::new(AtomicUsize::new(0));
        let result = run(
            &q,
            &key,
            &quit,
            || Ok(intent(&drops)),
            |_| {
                if fail {
                    Err("synthetic parent/presentation unavailable".into())
                } else {
                    Ok(false)
                }
            },
            || panic!("cancel/error has no final window phase"),
            |_| panic!("must not consume"),
        );
        if fail {
            assert!(result.is_err());
        } else {
            assert_eq!(result.unwrap(), Outcome::Cancelled);
        }
        assert_eq!(drops.load(Ordering::SeqCst), 1);
        assert!(key.try_lock().is_ok());
        assert!(q.acquire().is_ok());
    }
}
#[test]
fn seal_enrollment_preparation_refusal_and_duplicate_question_do_not_consume() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    assert!(run::<()>(
        &q,
        &key,
        &quit,
        || Err("None or unavailable root".into()),
        |_| panic!(),
        || panic!(),
        |_| panic!()
    )
    .is_err());
    assert!(q.acquire().is_ok());
    let held = q.acquire().unwrap();
    assert!(run::<()>(
        &q,
        &key,
        &quit,
        || panic!("duplicate must not prepare"),
        |_| panic!(),
        || panic!(),
        |_| panic!()
    )
    .is_err());
    drop(held);
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_key_setup_contention_after_choice_refuses_without_window_or_provider() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let drops = Arc::new(AtomicUsize::new(0));
    let held = RefCell::new(None);
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(intent(&drops)),
        |_| {
            *held.borrow_mut() = Some(key.lock().unwrap());
            Ok(true)
        },
        || panic!("key operation won"),
        |_| panic!("no provider effects"),
    );
    assert!(result.unwrap_err().contains("key operation"));
    assert_eq!(drops.load(Ordering::SeqCst), 1);
    drop(held);
    assert!(key.try_lock().is_ok());
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_quit_before_prepare_or_during_question_refuses() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let stop = Mutex::new(());
    let held = crate::app_quit::admit_quit(&quit, &stop).unwrap();
    assert!(run::<()>(
        &q,
        &key,
        &quit,
        || panic!("Quit first"),
        |_| panic!(),
        || panic!(),
        |_| panic!()
    )
    .is_err());
    drop(held);
    let drops = Arc::new(AtomicUsize::new(0));
    let held = RefCell::new(None);
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(intent(&drops)),
        |_| {
            assert!(key.try_lock().is_ok());
            *held.borrow_mut() = Some(crate::app_quit::admit_quit(&quit, &stop).unwrap());
            Ok(true)
        },
        || panic!("Quit during question"),
        |_| panic!(),
    );
    assert!(result.is_err());
    assert_eq!(drops.load(Ordering::SeqCst), 1);
    drop(held);
    assert!(key.try_lock().is_ok());
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_decided_quit_is_not_only_the_question_busy_flag() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    quit.allow(
        &crate::app_quit::Decision::Quit(serde_json::json!({"stopRequests":[]})),
        |_| Ok(Value::Null),
    )
    .unwrap();
    assert!(!quit.busy());
    assert!(run::<()>(
        &q,
        &key,
        &quit,
        || panic!("decided Quit"),
        |_| panic!(),
        || panic!(),
        |_| panic!()
    )
    .is_err());
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_lost_original_after_choice_releases_key_gate_without_consumption() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let drops = Arc::new(AtomicUsize::new(0));
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(intent(&drops)),
        |_| Ok(true),
        || Err("original window unavailable".into()),
        |_| panic!("no replacement window"),
    );
    assert!(result.unwrap_err().contains("original window"));
    assert_eq!(drops.load(Ordering::SeqCst), 1);
    assert!(key.try_lock().is_ok());
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_quit_rechecked_after_main_thread_window_interval() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let stop = Mutex::new(());
    let held = RefCell::new(None);
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(()),
        |_| Ok(true),
        || {
            *held.borrow_mut() = Some(crate::app_quit::admit_quit(&quit, &stop).unwrap());
            assert!(
                key.try_lock().is_err(),
                "Quit cannot settle with key operation held"
            );
            Ok(())
        },
        |_| panic!("final Quit check must refuse"),
    );
    assert!(result.is_err());
    drop(held);
    assert!(key.try_lock().is_ok());
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_winning_gate_keeps_quit_out_until_actual_provider_return() {
    let key = Arc::new(Mutex::new(()));
    let quit = Arc::new(AppQuit::default());
    let q = Arc::new(Questions::new());
    let (started, at) = std::sync::mpsc::channel();
    let (resume, go) = std::sync::mpsc::channel();
    let k = key.clone();
    let z = quit.clone();
    let question = q.clone();
    let worker = std::thread::spawn(move || {
        run(
            &question,
            &k,
            &z,
            || Ok(()),
            |_| Ok(true),
            || Ok(()),
            |_| {
                started.send(()).unwrap();
                go.recv_timeout(std::time::Duration::from_secs(5)).unwrap();
                Ok(())
            },
        )
    });
    at.recv_timeout(std::time::Duration::from_secs(5)).unwrap();
    let stop = Mutex::new(());
    let held = crate::app_quit::admit_quit(&quit, &stop).unwrap();
    assert!(
        matches!(key.try_lock(), Err(std::sync::TryLockError::WouldBlock)),
        "same existing Quit key_setup admission fails"
    );
    assert!(quit.proceeding().is_none());
    assert!(q.acquire().is_err());
    drop(held);
    resume.send(()).unwrap();
    assert_eq!(
        worker.join().unwrap().unwrap(),
        Outcome::ProviderReturnedSuccess
    );
    assert!(key.try_lock().is_ok());
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_provider_stale_or_failure_never_retries_and_releases_gates() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let drops = Arc::new(AtomicUsize::new(0));
    let calls = AtomicUsize::new(0);
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(intent(&drops)),
        |_| Ok(true),
        || Ok(()),
        |_| {
            calls.fetch_add(1, Ordering::SeqCst);
            Err("prepared provider source changed".into())
        },
    );
    assert!(result.unwrap_err().contains("source changed"));
    assert_eq!(calls.load(Ordering::SeqCst), 1);
    assert_eq!(drops.load(Ordering::SeqCst), 1);
    assert!(key.try_lock().is_ok());
    assert!(q.acquire().is_ok());
}
#[test]
fn seal_enrollment_statement_names_exact_prepared_scope_and_safe_choices() {
    let preview = serde_json::json!({"app_data":"/invented/AppData","service":"invalid.example.seal","account":"synthetic","access_group":"SYNTHETIC0.invalid.example.app","marker":{"committed_key_ids":[],"pending_key_id":null}});
    let shown = statement(&preview).unwrap();
    assert!(shown.text.contains("invalid.example.seal"));
    assert!(shown.text.contains("synthetic"));
    for (how, result) in ns::dialog_model::outcomes(&ns::act_buttons(LEAVE, PREPARE)) {
        assert_eq!(ns::chose(&result, PREPARE), how == "middle");
    }
    let mut fresh = preview.clone();
    fresh["marker"] = Value::Null;
    let text = statement(&fresh).unwrap().text;
    assert!(text.contains("none observed"));
    assert!(!text.contains("IDs: null"));
    assert!(statement(&Value::Null).is_err());
}

#[test]
fn seal_enrollment_provider_unwind_is_unknown_and_does_not_poison_shared_quit_gate() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let drops = Arc::new(AtomicUsize::new(0));
    let calls = AtomicUsize::new(0);
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(intent(&drops)),
        |_| Ok(true),
        || Ok(()),
        |_| {
            calls.fetch_add(1, Ordering::SeqCst);
            panic!("synthetic provider unwind")
        },
    );
    assert!(result.unwrap_err().contains("outcome unknown; not retried"));
    assert_eq!(calls.load(Ordering::SeqCst), 1);
    assert_eq!(drops.load(Ordering::SeqCst), 1);
    assert!(!key.is_poisoned());
    assert!(q.acquire().is_ok());
    let stop = Mutex::new(());
    let held = crate::app_quit::admit_quit(&quit, &stop).unwrap();
    let key_held = key
        .try_lock()
        .expect("Quit and API-key setup remain usable");
    drop(key_held);
    drop(held);
    assert_eq!(
        run(
            &q,
            &key,
            &quit,
            || Ok(intent(&drops)),
            |_| Ok(true),
            || Ok(()),
            |_| Ok(())
        )
        .unwrap(),
        Outcome::ProviderReturnedSuccess
    );
    assert_eq!(drops.load(Ordering::SeqCst), 2);
}

#[test]
fn seal_enrollment_preexisting_poison_is_unavailable_without_clearing_it() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        let _held = key.lock().unwrap();
        panic!("unrelated synthetic poison");
    }));
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(()),
        |_| Ok(true),
        || panic!("poisoned admission"),
        |_| panic!("no provider"),
    );
    assert!(result.unwrap_err().contains("admission is unavailable"));
    assert!(key.is_poisoned());
    assert!(q.acquire().is_ok());
}

#[test]
fn seal_enrollment_window_validation_unwind_also_leaves_shared_gate_usable() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let drops = Arc::new(AtomicUsize::new(0));
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(intent(&drops)),
        |_| Ok(true),
        || panic!("synthetic window check unwind"),
        |_| panic!("must not consume"),
    );
    assert!(result.unwrap_err().contains("outcome unknown"));
    assert!(!key.is_poisoned());
    assert!(key.try_lock().is_ok());
    assert!(q.acquire().is_ok());
    assert_eq!(drops.load(Ordering::SeqCst), 1);
}
#[test]
fn seal_enrollment_quit_refusal_precedes_busy_key_wording_after_choice() {
    let q = Questions::new();
    let key = Mutex::new(());
    let quit = AppQuit::default();
    let stop = Mutex::new(());
    let quit_guard = RefCell::new(None);
    let key_guard = RefCell::new(None);
    let result = run(
        &q,
        &key,
        &quit,
        || Ok(()),
        |_| {
            *quit_guard.borrow_mut() = Some(crate::app_quit::admit_quit(&quit, &stop).unwrap());
            *key_guard.borrow_mut() = Some(key.lock().unwrap());
            Ok(true)
        },
        || panic!(),
        |_| panic!(),
    );
    assert!(result.unwrap_err().contains("App is quitting"));
    drop(key_guard);
    drop(quit_guard);
    assert!(q.acquire().is_ok());
}
