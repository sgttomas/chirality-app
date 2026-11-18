//! The system's request to quit (DEL-01-02 DEF-6, K-4, REQ-005, AC-006).
//!
//! Tao's delegate implements `applicationWillTerminate:`. At startup the App
//! attempts to add `applicationShouldTerminate:` to its class. When AppKit
//! calls the installed method, it returns `NSTerminateCancel`. An eligible
//! request enters the App's own quit path. A decided quit can request
//! programmatic exit through Wry and tao. The event loop stops with `stop:`
//! and exits without calling this selector. Runtime registration alone does
//! not establish delivery for a Dock Quit, the app switcher or a system
//! session operation.
//!
//! The delegate returns Cancel. Fault reporting and any wait for App state or
//! the original window happen outside the selector. The selector reads and
//! sets only the quit reservation (`app_quit::QuitReservation`), published
//! with the App handle before the method is added, and hands a reserved
//! attempt to a new thread; it takes no lock and writes no output.
//!
//! The method is added only if the class does not already respond to the
//! selector; what installation found is said on standard error, and a
//! failure leaves the App starting as before.

use crate::app_quit;
use objc2::encode::Encode;
use objc2::runtime::{AnyClass, AnyObject, Imp, Sel};
use objc2::{ffi, sel, MainThreadMarker};
use objc2_app_kit::{NSApplication, NSApplicationTerminateReply};
use std::ffi::CString;
use std::sync::{Arc, OnceLock};

/// The App handle and its quit reservation, published once at installation
/// before the method is added.
static BINDING: OnceLock<(tauri::AppHandle, Arc<app_quit::QuitReservation>)> = OnceLock::new();

/// What installation found.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Installed {
    /// The method was added to the delegate's class.
    Added,
    /// The class already responds to the selector: this hook was skipped.
    AlreadyResponds,
}

/// `NSApplicationTerminateReply applicationShouldTerminate:(NSApplication *)`.
pub(crate) fn selector() -> Sel {
    sel!(applicationShouldTerminate:)
}
pub(crate) fn type_encoding() -> CString {
    let types = format!(
        "{}{}{}{}",
        NSApplicationTerminateReply::ENCODING,
        <*mut AnyObject as Encode>::ENCODING,
        <Sel as Encode>::ENCODING,
        <*mut AnyObject as Encode>::ENCODING
    );
    CString::new(types).expect("an encoding has no interior NUL")
}

/// Add `imp` as the class's `applicationShouldTerminate:` unless the class
/// already responds to it.
///
/// # Safety
/// `imp` must be an `extern "C-unwind" fn(&AnyObject, Sel, *mut AnyObject) ->
/// NSApplicationTerminateReply`, transmuted.
pub(crate) unsafe fn install_on(class: &AnyClass, imp: Imp) -> Result<Installed, String> {
    if class.responds_to(selector()) {
        return Ok(Installed::AlreadyResponds);
    }
    let types = type_encoding();
    // SAFETY: the class is registered; adding a method the class does not
    // have is what the runtime permits at any time; `types` matches `imp`.
    let added = unsafe { ffi::class_addMethod(class as *const AnyClass as *mut AnyClass, selector(), imp, types.as_ptr()) };
    if added.as_bool() {
        Ok(Installed::Added)
    } else {
        Err(format!("the runtime refused to add {} to {}", selector().name().to_string_lossy(), class.name().to_string_lossy()))
    }
}

/// Install on the application delegate's class. Main thread, after the
/// event loop has created and set its delegate (Tauri's setup runs from the
/// delegate's `applicationDidFinishLaunching:`). Never fails the start: what
/// held is said in the diagnostics.
pub(crate) fn install(app: &tauri::AppHandle) {
    let found = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| install_delegate(app)))
        .unwrap_or_else(|_| Err("installation panicked".into()));
    app_quit::diagnostic(&match found {
        Ok(Installed::Added) => "quit routes: applicationShouldTerminate: was added to the application delegate's class; whether AppKit calls it is not established here".into(),
        Ok(Installed::AlreadyResponds) => "quit routes: the application delegate's class already responds to applicationShouldTerminate:, so this hook was skipped".into(),
        Err(error) => format!("quit routes: this attempt could not add applicationShouldTerminate: ({error})"),
    });
}
fn install_delegate(app: &tauri::AppHandle) -> Result<Installed, String> {
    let mtm = MainThreadMarker::new().ok_or("not on the main thread")?;
    let delegate = NSApplication::sharedApplication(mtm).delegate().ok_or("the application has no delegate")?;
    // SAFETY: a delegate is an Objective-C object; reading its class is safe.
    let object: &AnyObject = unsafe { &*(objc2::rc::Retained::as_ptr(&delegate) as *const AnyObject) };
    let class = object.class();
    let reservation = Arc::clone(tauri::Manager::state::<crate::AppState>(app).app_quit.reservation());
    if BINDING.set((app.clone(), reservation)).is_err() {
        return Err("already installed once".into());
    }
    // SAFETY: `should_terminate` has the signature `install_on` requires.
    unsafe { install_on(class, std::mem::transmute::<ShouldTerminate, Imp>(should_terminate)) }
}

pub(crate) type ShouldTerminate = extern "C-unwind" fn(&AnyObject, Sel, *mut AnyObject) -> NSApplicationTerminateReply;

/// `applicationShouldTerminate:`. AppKit calls it on the main thread.
pub(crate) extern "C-unwind" fn should_terminate(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
    answer_terminate(BINDING.get(), |app, token| {
        crate::hand_off_quit(app.clone(), app_quit::QuitRoute::System, token);
    })
}
/// The selector's binding: always Cancel. With a binding, one
/// [`app_quit::system_request`] that reads and sets only the reservation and
/// hands a reserved attempt off; a hand-off that fails drops the token, which
/// releases the reservation, and is not reported here. A panic is caught and
/// its payload dropped.
pub(crate) fn answer_terminate<H>(binding: Option<&(H, Arc<app_quit::QuitReservation>)>, hand_off: impl FnOnce(&H, app_quit::QuitToken)) -> NSApplicationTerminateReply {
    if let Some((handle, reservation)) = binding {
        let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| app_quit::system_request(reservation, |token| hand_off(handle, token))));
    }
    NSApplicationTerminateReply::TerminateCancel
}

// Tests: `app_quit_tests.rs` (`macos_quit_routes`), in the `app_quit::tests`
// pull-request cohort.
