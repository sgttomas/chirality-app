//! Offline parent/result stand-ins; no platform handles are dereferenced.
use super::*;
use std::cell::Cell;

struct Handles {
    available: Cell<bool>,
    display: bool,
    reads: Cell<usize>,
}
impl Handles {
    fn new(display: bool) -> Self {
        Self { available: Cell::new(true), display, reads: Cell::new(0) }
    }
}
impl HasWindowHandle for Handles {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
        self.reads.set(self.reads.get() + 1);
        if !self.available.get() { return Err(HandleError::Unavailable); }
        // No pointer and never passed to native code.
        Ok(unsafe { WindowHandle::borrow_raw(raw_window_handle::WebWindowHandle::new(23).into()) })
    }
}
impl HasDisplayHandle for Handles {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
        self.reads.set(self.reads.get() + 1);
        if self.display && self.available.get() { Ok(DisplayHandle::web()) }
        else { Err(HandleError::Unavailable) }
    }
}

#[test]
fn original_handles_are_cached_before_plugin_parent_lookup() {
    let original = Handles::new(true);
    checked_parent(&original, |parent| {
        original.available.set(false);
        for _ in 0..2 {
            assert_eq!(parent.window_handle().unwrap().as_raw(), raw_window_handle::WebWindowHandle::new(23).into());
            assert_eq!(parent.display_handle().unwrap(), DisplayHandle::web());
        }
    }).unwrap();
    assert_eq!(original.reads.get(), 2, "plugin sees only cached successful borrows");
}

#[test]
fn missing_original_window_or_display_refuses_without_presenting() {
    for display in [false, true] {
        let original = Handles::new(display);
        original.available.set(!display);
        assert_eq!(checked_parent(&original, |_| panic!("no parentless fallback")).unwrap_err(), UNAVAILABLE);
    }
}

#[test]
fn destroyed_original_refuses_register_and_reconfirm_without_reselection() {
    for act in ["Register", "Re-confirm"] {
        let original = Handles::new(true);
        checked_parent(&original, |_| ()).unwrap();
        original.available.set(false);
        assert_eq!(result_in_original(&original, MessageDialogResult::Custom(act.into()), act).unwrap_err(), UNAVAILABLE);
        // No affirmative means no capture, even if the original was destroyed.
        assert!(matches!(result_in_original(&original, MessageDialogResult::Cancel, act).unwrap(), MessageDialogResult::Cancel));
    }
}

#[test]
fn missing_callback_result_is_refusal_not_an_act_or_cancellation() {
    let (send, receive) = mpsc::channel();
    drop(send);
    assert!(receive_result(receive).unwrap_err().contains("nothing captured"));
}
