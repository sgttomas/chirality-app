//! Synthetic original request/register checks; no App, supplier or native UI runs.
use super::*;
use crate::native_requests::RequestRegister;
use std::cell::{Cell, RefCell};

fn fixture() -> (Value, Value, Value, Value, RequestRegister) {
    let generation = json!({"appSession":"fixture-session","home":"fixture-home","spawnCounter":3});
    let id = json!(7);
    let answer = json!({"decision":"accept"});
    let mut register = RequestRegister::default();
    register.receive(&generation, 1, &json!({
        "id":id,"method":"item/fileChange/requestApproval",
        "params":{"threadId":"fixture-thread","turnId":"fixture-turn","itemId":"fixture-item"}
    }), &json!({})).unwrap();
    let snapshot =
        json!({"generation":generation,"state":"ready","serverRequests":register.records()});
    let context = json!({"generation":generation,"hostState":"ready","displayName":"Fixture Person","osAccount":"fixture-user","codexAccount":null,"accountRevision":1});
    (generation, id, answer, json!([snapshot, context]), register)
}
fn affirmative() -> MessageDialogResult {
    MessageDialogResult::Custom(ns::SEND_ANSWER.into())
}

struct HandleFixture {
    window_reads: Cell<usize>,
    display_reads: Cell<usize>,
    display_available: bool,
}
impl HasWindowHandle for HandleFixture {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
        self.window_reads.set(self.window_reads.get() + 1);
        if self.window_reads.get() > 1 {
            return Err(HandleError::Unavailable);
        }
        // SAFETY: A Web ID contains no pointers. raw-window-handle's borrowed
        // handle guarantees explicitly exclude the validity of window IDs.
        // This value is inspected only; no platform consumer receives it.
        Ok(unsafe { WindowHandle::borrow_raw(raw_window_handle::WebWindowHandle::new(17).into()) })
    }
}
impl HasDisplayHandle for HandleFixture {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
        self.display_reads.set(self.display_reads.get() + 1);
        if self.display_available && self.display_reads.get() == 1 {
            Ok(DisplayHandle::web())
        } else {
            Err(HandleError::Unavailable)
        }
    }
}

#[test]
fn checked_parent_caches_both_original_handles_without_another_fallible_lookup() {
    let original = HandleFixture {
        window_reads: Cell::new(0),
        display_reads: Cell::new(0),
        display_available: true,
    };
    let parent = checked_parent(&original).unwrap();
    for _ in 0..2 {
        assert_eq!(
            parent.window_handle().unwrap().as_raw(),
            raw_window_handle::WebWindowHandle::new(17).into()
        );
        assert_eq!(parent.display_handle().unwrap(), DisplayHandle::web());
    }
    assert_eq!(original.window_reads.get(), 1);
    assert_eq!(original.display_reads.get(), 1);
}

// Models the error supplied by a destroyed/unavailable native window. No fake
// native pointer is constructed or passed to the platform dialog implementation.
struct UnavailableParent;
impl HasWindowHandle for UnavailableParent {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
        Err(HandleError::Unavailable)
    }
}
impl HasDisplayHandle for UnavailableParent {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
        Err(HandleError::Unavailable)
    }
}

#[test]
fn unavailable_parent_refuses_before_dialog_or_reply() {
    let (g, id, a, basis, _) = fixture();
    let shown = Cell::new(false);
    let written = Cell::new(false);
    let result = answer(
        &g,
        &id,
        &a,
        || (basis[0].clone(), basis[1].clone()),
        |_| {
            let _parent = checked_parent(&UnavailableParent)?;
            shown.set(true);
            Ok(affirmative())
        },
        |_| {
            written.set(true);
            Ok(Value::Null)
        },
    );
    assert_eq!(
        result.unwrap_err(),
        "Invoking App window unavailable; native answer confirmation refused"
    );
    assert!(!shown.get());
    assert!(!written.get());
}

#[test]
fn affirmative_parent_revalidation_error_refuses_before_reply() {
    let (g, id, a, basis, _) = fixture();
    let written = Cell::new(false);
    let result = answer(
        &g,
        &id,
        &a,
        || (basis[0].clone(), basis[1].clone()),
        |_| result_in_parent(&UnavailableParent, affirmative()),
        |_| {
            written.set(true);
            Ok(Value::Null)
        },
    );
    assert!(result.unwrap_err().contains("window unavailable"));
    assert!(!written.get());
}

#[test]
fn unavailable_display_refuses_before_presentation_or_reply() {
    let (g, id, a, basis, _) = fixture();
    let original = HandleFixture {
        window_reads: Cell::new(0),
        display_reads: Cell::new(0),
        display_available: false,
    };
    let result = answer(
        &g,
        &id,
        &a,
        || (basis[0].clone(), basis[1].clone()),
        |_| {
            let _parent = checked_parent(&original)?;
            panic!("unavailable display presented a dialog");
        },
        |_| panic!("unavailable display wrote a reply"),
    );
    assert_eq!(
        result.unwrap_err(),
        "Invoking App display unavailable; native answer confirmation refused"
    );
}

#[test]
fn default_cancel_abort_and_nonexact_affirmatives_never_reply() {
    for result in [
        MessageDialogResult::Custom(ns::DONT_SEND.into()),
        MessageDialogResult::Cancel,
        MessageDialogResult::Ok,
        MessageDialogResult::Yes,
        MessageDialogResult::No,
        MessageDialogResult::Custom("Cancel".into()),
        MessageDialogResult::Custom("send answer".into()),
        MessageDialogResult::Custom("Send answer ".into()),
    ] {
        let (g, id, a, basis, _) = fixture();
        let reads = Cell::new(0);
        let result = answer(
            &g,
            &id,
            &a,
            || {
                reads.set(reads.get() + 1);
                (basis[0].clone(), basis[1].clone())
            },
            |_| result_in_parent(&UnavailableParent, result),
            |_| panic!("nonaffirmative wrote a reply"),
        );
        assert_eq!(
            result.unwrap(),
            json!({"state":"dismissed","replyWriteResult":"not-attempted"})
        );
        assert_eq!(reads.get(), 1);
    }
}

#[test]
fn exact_affirmative_revalidates_original_request_and_preserves_native_reply_outcome() {
    let (g, id, a, basis, mut register) = fixture();
    let reads = Cell::new(0);
    let writes = Cell::new(0);
    let observed_outcome = json!({"replyWriteResult":"written","acknowledgment":"not-observed"});
    let result = answer(
        &g,
        &id,
        &a,
        || {
            reads.set(reads.get() + 1);
            (basis[0].clone(), basis[1].clone())
        },
        |statement| {
            assert!(statement.text.contains("item/fileChange/requestApproval"));
            assert!(statement
                .text
                .contains("Don't send (the default) and Cancel send nothing"));
            Ok(affirmative())
        },
        |actor| {
            assert_eq!(
                reads.get(),
                2,
                "original source must be rechecked before write"
            );
            let frame = register.prepare(&g, &id, &a, "person-via-interaction", Some(actor))?;
            assert_eq!(frame, json!({"id":7,"result":{"decision":"accept"}}));
            assert!(actor.contains("Fixture Person / fixture-user"));
            writes.set(writes.get() + 1);
            Ok(observed_outcome.clone())
        },
    )
    .unwrap();
    assert_eq!(result, observed_outcome);
    assert_eq!(writes.get(), 1);
}

#[test]
fn changed_original_generation_or_request_refuses_after_confirmation() {
    for mutation in [
        "appSession",
        "home",
        "spawnCounter",
        "missing",
        "typed-id",
        "settled",
        "not-ready",
    ] {
        let (g, id, a, basis, _) = fixture();
        let original = RefCell::new(basis);
        let result = answer(
            &g,
            &id,
            &a,
            || {
                let original = original.borrow();
                (original[0].clone(), original[1].clone())
            },
            |_| {
                let mut original = original.borrow_mut();
                match mutation {
                    "appSession" | "home" => {
                        original[0]["generation"][mutation] = json!("replacement")
                    }
                    "spawnCounter" => original[0]["generation"][mutation] = json!(4),
                    "missing" => original[0]["serverRequests"] = json!([]),
                    "typed-id" => original[0]["serverRequests"][0]["requestIdentity"] = json!("7"),
                    "settled" => original[0]["serverRequests"][0]["state"] = json!("answered"),
                    "not-ready" => original[0]["state"] = json!("stopped"),
                    _ => unreachable!(),
                }
                Ok(affirmative())
            },
            |_| panic!("changed original source wrote a reply"),
        );
        assert!(result.is_err(), "{mutation}");
    }
}

#[test]
fn changed_actor_or_owning_context_refuses_after_confirmation() {
    for field in [
        "displayName",
        "osAccount",
        "codexAccount",
        "accountRevision",
        "generation",
        "hostState",
    ] {
        let (g, id, a, basis, _) = fixture();
        let original = RefCell::new(basis);
        let result = answer(
            &g,
            &id,
            &a,
            || {
                let original = original.borrow();
                (original[0].clone(), original[1].clone())
            },
            |_| {
                original.borrow_mut()[1][field] = json!("changed");
                Ok(affirmative())
            },
            |_| panic!("changed actor/context wrote a reply"),
        );
        assert_eq!(result.unwrap_err(), "Attribution or owning host context changed during confirmation; review and confirm again");
    }
}

#[test]
fn invalid_initial_request_never_presents_or_writes_and_write_errors_stay_errors() {
    let (g, id, a, basis, _) = fixture();
    assert!(answer(
        &g,
        &json!("foreign"),
        &a,
        || (basis[0].clone(), basis[1].clone()),
        |_| panic!("invalid request presented"),
        |_| panic!("invalid request wrote")
    )
    .is_err());
    let error = "synthetic reply write failed; receipt unknown";
    assert_eq!(
        answer(
            &g,
            &id,
            &a,
            || (basis[0].clone(), basis[1].clone()),
            |_| Ok(affirmative()),
            |_| Err(error.into())
        )
        .unwrap_err(),
        error
    );
}
