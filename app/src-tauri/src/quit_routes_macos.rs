//! The system's request to quit (DEL-01-02 DEF-6, K-4, REQ-005, AC-006).
//!
//! The Dock's Quit and Command-Tab then Q send `terminate:` to the
//! application, as logout, restart and shutdown do. The event loop library
//! (tao 0.35.2) registers an application delegate class that implements
//! `applicationWillTerminate:` and no `applicationShouldTerminate:`, so
//! without this module AppKit goes straight to the exit handler: no question,
//! no interrupt, and the limited system path. At startup the App attempts to
//! add `applicationShouldTerminate:` to that class.
//!
//! When AppKit calls the installed method, it declines the request at once
//! (`NSTerminateCancel`), always, also when nothing is live: the App never
//! makes the system wait, and only its own quit path ends it. What the method
//! starts is [`app_quit::on_system_quit_request`]: with no quit under way and
//! none decided, the same quit path the menu's Quit starts (it asks only if
//! work is live, settles, records and then exits the App itself with
//! `app.exit(0)`); with a quit under way, nothing (that quit is in front of
//! the person); with a quit decided, nothing (its own exit is in flight). A
//! fault in the method is caught and said; the request is still declined.
//!
//! No exit of the App's own re-enters this method: `app.exit(0)` ends through
//! Wry's `RequestExit`, tao's `[NSApp stop:]`, `AppState::exit` and
//! `process::exit` (tao `macos/event_loop.rs` `run`, `app_state.rs`
//! `cleared`/`exit`; Tauri `AppHandle::exit`, whose fallback is also
//! `process::exit`), and neither tao nor Tauri sends `terminate:`. So there
//! is no authorised exit for this method to let through, and it declines
//! every request.
//!
//! Force Quit, an unhandled fatal signal or power loss never reaches this
//! method or the exit handler. The method is added only if the class does not
//! already respond to the selector; what installation found is said on
//! standard error, and a failure leaves the App starting as before.

use crate::app_quit;
use objc2::encode::Encode;
use objc2::runtime::{AnyClass, AnyObject, Imp, Sel};
use objc2::{ffi, sel, MainThreadMarker};
use objc2_app_kit::{NSApplication, NSApplicationTerminateReply};
use std::ffi::CString;
use std::sync::OnceLock;

/// The App this method serves, set once at installation.
static APP: OnceLock<tauri::AppHandle> = OnceLock::new();

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
    if APP.set(app.clone()).is_err() {
        return Err("already installed once".into());
    }
    // SAFETY: `should_terminate` has the signature `install_on` requires.
    unsafe { install_on(class, std::mem::transmute::<ShouldTerminate, Imp>(should_terminate)) }
}

pub(crate) type ShouldTerminate = extern "C-unwind" fn(&AnyObject, Sel, *mut AnyObject) -> NSApplicationTerminateReply;

/// `applicationShouldTerminate:`. AppKit calls it on the main thread. It
/// always declines; see the module comment.
pub(crate) extern "C-unwind" fn should_terminate(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
    if let Some(app) = APP.get() {
        let held = || {
            let state = tauri::Manager::try_state::<crate::AppState>(app).expect("the App state is managed before installation");
            (state.app_quit.proceeding().is_some(), state.app_quit.busy())
        };
        app_quit::handle_system_quit_request(held, || crate::request_quit_with(app.clone(), app_quit::QuitRoute::System));
    }
    NSApplicationTerminateReply::TerminateCancel
}

// Tests: `app_quit_tests.rs` (`macos_quit_routes`), in the `app_quit::tests`
// pull-request cohort.
