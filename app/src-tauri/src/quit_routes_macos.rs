//! The system's request to quit, asked as the menu's Quit asks (DEL-01-02
//! DEF-6, K-4, REQ-005, AC-006).
//!
//! The Dock's Quit, Command-Tab then Q, logout and shutdown send `terminate:`
//! to the application. The event loop library (tao 0.35.2) registers an
//! application delegate class that implements `applicationWillTerminate:` and
//! no `applicationShouldTerminate:`, so without this module AppKit goes
//! straight to the exit handler: no question, no interrupt, and the session
//! end recorded as system-terminated. At startup this module adds
//! `applicationShouldTerminate:` to the delegate's class, so that every such
//! route runs the one quit path (`request_quit_with` in `lib.rs`) and the App
//! ends only once that path has decided the quit.
//!
//! The answer is [`app_quit::on_should_terminate`] under
//! [`app_quit::TERMINATION_BEHAVIOUR`]: with "later" the reply is given on the
//! main thread exactly once by [`app_quit::TerminationReply`], yes only when
//! the quit is decided and settled; with "cancel" the termination is declined
//! at once and the quit path ends the App itself. A termination the system
//! forces without asking (a signal, Force Quit, power loss) never reaches
//! this method and keeps the limited system path.
//!
//! The method is added only if the class does not already respond to the
//! selector; any failure leaves the App starting as before and is said in
//! the App's diagnostics (standard error).

use crate::app_quit::{self, TerminationAnswer, TerminationReply};
use objc2::encode::Encode;
use objc2::runtime::{AnyClass, AnyObject, Imp, Sel};
use objc2::{ffi, sel, MainThreadMarker};
use objc2_app_kit::{NSApplication, NSApplicationTerminateReply};
use std::ffi::CString;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::OnceLock;

/// The App this method serves, set once at installation.
static APP: OnceLock<tauri::AppHandle> = OnceLock::new();
/// True from a "later" answer until its reply has been given on the main
/// thread.
static REPLY_PENDING: AtomicBool = AtomicBool::new(false);

/// What installation found.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Installed {
    /// The method was added to the delegate's class.
    Added,
    /// The class already responds to the selector (a later library version):
    /// nothing was installed and the library's answer stands.
    AlreadyResponds,
}

/// `NSApplicationTerminateReply applicationShouldTerminate:(NSApplication *)`.
fn selector() -> Sel {
    sel!(applicationShouldTerminate:)
}
fn type_encoding() -> CString {
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
    match found {
        Ok(Installed::Added) => eprintln!("chirality: quit routes: the system's request to quit (Dock, app switcher, logout, shutdown) asks as Quit does ({:?} behaviour)", app_quit::TERMINATION_BEHAVIOUR),
        Ok(Installed::AlreadyResponds) => eprintln!("chirality: quit routes: the application delegate already answers applicationShouldTerminate:; nothing installed, so the system's request to quit is answered by the event loop library, not by the quit question"),
        Err(error) => eprintln!("chirality: quit routes: not installed ({error}); the system's request to quit ends the App without the quit question, as a system termination"),
    }
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

type ShouldTerminate = extern "C-unwind" fn(&AnyObject, Sel, *mut AnyObject) -> NSApplicationTerminateReply;

/// `applicationShouldTerminate:`. AppKit calls it on the main thread.
extern "C-unwind" fn should_terminate(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
    // A fault here keeps the system's request as it was before this module:
    // terminate now, by the limited system path.
    std::panic::catch_unwind(answer).unwrap_or(NSApplicationTerminateReply::TerminateNow)
}
fn answer() -> NSApplicationTerminateReply {
    let Some(app) = APP.get() else { return NSApplicationTerminateReply::TerminateNow };
    let decided = tauri::Manager::try_state::<crate::AppState>(app).is_some_and(|state| state.app_quit.proceeding().is_some());
    match app_quit::on_should_terminate(decided, REPLY_PENDING.load(Ordering::SeqCst), app_quit::TERMINATION_BEHAVIOUR) {
        TerminationAnswer::Now => NSApplicationTerminateReply::TerminateNow,
        TerminationAnswer::CancelPending => NSApplicationTerminateReply::TerminateCancel,
        TerminationAnswer::CancelAndAsk => {
            crate::request_quit_with(app.clone(), None);
            NSApplicationTerminateReply::TerminateCancel
        }
        TerminationAnswer::LaterAndAsk => {
            REPLY_PENDING.store(true, Ordering::SeqCst);
            crate::request_quit_with(app.clone(), Some(TerminationReply::new(reply_on_main)));
            NSApplicationTerminateReply::TerminateLater
        }
    }
}
/// `replyToApplicationShouldTerminate:` on the main thread, after this
/// method has returned "later" (also when the reply is given from it).
fn reply_on_main(yes: bool) {
    dispatch2::DispatchQueue::main().exec_async(move || {
        REPLY_PENDING.store(false, Ordering::SeqCst);
        if let Some(mtm) = MainThreadMarker::new() {
            NSApplication::sharedApplication(mtm).replyToApplicationShouldTerminate(yes);
        }
    });
}

#[cfg(test)]
mod tests {
    use super::*;
    use objc2::runtime::{ClassBuilder, NSObject};
    use objc2::{msg_send, ClassType};

    extern "C-unwind" fn fixed(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
        NSApplicationTerminateReply::TerminateLater
    }
    extern "C-unwind" fn other(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
        NSApplicationTerminateReply::TerminateNow
    }
    fn throwaway(name: &str) -> &'static AnyClass {
        let name = CString::new(format!("ChiralityQuitRoutesTest{name}{}", std::process::id())).unwrap();
        ClassBuilder::new(&name, NSObject::class()).unwrap().register()
    }

    #[test]
    fn the_encoding_is_an_unsigned_reply_taking_an_object() {
        assert_eq!(type_encoding().to_str().unwrap(), "Q@:@");
    }

    /// Against a throwaway class (not the application's delegate; no
    /// NSApplication is started): the method is added, answers through the
    /// runtime, and a second installation leaves the first in place.
    #[test]
    fn installs_once_on_a_class_that_does_not_respond() {
        let class = throwaway("Add");
        assert!(!class.responds_to(selector()));
        let first = unsafe { install_on(class, std::mem::transmute::<ShouldTerminate, Imp>(fixed)) };
        assert_eq!(first, Ok(Installed::Added));
        assert!(class.responds_to(selector()));
        let again = unsafe { install_on(class, std::mem::transmute::<ShouldTerminate, Imp>(other)) };
        assert_eq!(again, Ok(Installed::AlreadyResponds));
        let object: objc2::rc::Retained<AnyObject> = unsafe { msg_send![class, new] };
        let answer: NSApplicationTerminateReply = unsafe { msg_send![&*object, applicationShouldTerminate: std::ptr::null_mut::<AnyObject>()] };
        assert_eq!(answer, NSApplicationTerminateReply::TerminateLater);
    }

    #[test]
    fn a_class_that_already_responds_is_left_alone() {
        let name = CString::new(format!("ChiralityQuitRoutesTestHas{}", std::process::id())).unwrap();
        let mut builder = ClassBuilder::new(&name, NSObject::class()).unwrap();
        unsafe { builder.add_method(selector(), other as extern "C-unwind" fn(_, _, _) -> _) };
        let class = builder.register();
        let found = unsafe { install_on(class, std::mem::transmute::<ShouldTerminate, Imp>(fixed)) };
        assert_eq!(found, Ok(Installed::AlreadyResponds));
        let object: objc2::rc::Retained<AnyObject> = unsafe { msg_send![class, new] };
        let answer: NSApplicationTerminateReply = unsafe { msg_send![&*object, applicationShouldTerminate: std::ptr::null_mut::<AnyObject>()] };
        assert_eq!(answer, NSApplicationTerminateReply::TerminateNow);
    }
}
