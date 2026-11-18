//! The system's request to quit, asked as the menu's Quit asks (DEL-01-02
//! DEF-6, K-4, REQ-005, AC-006).
//!
//! The Dock's Quit and Command-Tab then Q send `terminate:` to the
//! application, as logout and shutdown do. The event loop library (tao
//! 0.35.2) registers an application delegate class that implements
//! `applicationWillTerminate:` and no `applicationShouldTerminate:`, so
//! without this module AppKit goes straight to the exit handler: no question,
//! no interrupt, and the limited system path. At startup this module adds
//! `applicationShouldTerminate:` to the delegate's class, so that such a
//! request runs the one quit path (`app_quit::run_quit`) and the App ends only
//! once that path has decided the quit.
//!
//! The answer is [`app_quit::answer_termination`] under
//! [`app_quit::TERMINATION_BEHAVIOUR`]. With "later" the reply is given on the
//! main thread exactly once by [`app_quit::TerminationReply`], yes only from
//! the run that decided and settled the quit. A request while a quit is under
//! way, or while a reply is owed, is declined and starts nothing; a decided
//! quit answers "now". A fault before the answer declines. With "cancel" the
//! request is declined at once and the quit path ends the App itself.
//!
//! An abrupt end (Force Quit, an unhandled fatal signal, power loss) never
//! reaches this method or the exit handler. The method is added only if the
//! class does not already respond to the selector; what installation found is
//! said on standard error, and a failure leaves the App starting as before.

use crate::app_quit::{self, TerminationAnswer};
use objc2::encode::Encode;
use objc2::runtime::{AnyClass, AnyObject, Imp, Sel};
use objc2::{ffi, sel, MainThreadMarker};
use objc2_app_kit::{NSApplication, NSApplicationTerminateReply};
use std::ffi::CString;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::OnceLock;

/// The App this method serves, set once at installation.
static APP: OnceLock<tauri::AppHandle> = OnceLock::new();
/// True from a "later" answer until its reply is taken on the main thread
/// (or a fault declined the request before "later" was returned).
static REPLY_OWED: AtomicBool = AtomicBool::new(false);

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
    app_quit::diagnostic(&match found {
        Ok(Installed::Added) => format!("quit routes: applicationShouldTerminate: was added to the application delegate's class ({:?} behaviour); whether AppKit calls it is not established here", app_quit::TERMINATION_BEHAVIOUR),
        Ok(Installed::AlreadyResponds) => "quit routes: the application delegate's class already responds to applicationShouldTerminate:; nothing was installed, and the system's request to quit is answered by that implementation, not by this App".into(),
        Err(error) => format!("quit routes: applicationShouldTerminate: not installed ({error}); the system's request to quit is not routed through the quit question"),
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

type ShouldTerminate = extern "C-unwind" fn(&AnyObject, Sel, *mut AnyObject) -> NSApplicationTerminateReply;

/// `applicationShouldTerminate:`. AppKit calls it on the main thread.
extern "C-unwind" fn should_terminate(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
    let Some(app) = APP.get() else {
        app_quit::diagnostic("the system's request to quit was declined: the quit path is not available");
        return NSApplicationTerminateReply::TerminateCancel;
    };
    let held = || {
        let state = tauri::Manager::try_state::<crate::AppState>(app).expect("the App state is managed before installation");
        (state.app_quit.proceeding().is_some(), state.app_quit.busy())
    };
    let answer = app_quit::answer_termination(held, &REPLY_OWED, app_quit::TERMINATION_BEHAVIOUR, reply_on_main, |reply| crate::request_quit_with(app.clone(), reply));
    native_answer(answer)
}
fn native_answer(answer: TerminationAnswer) -> NSApplicationTerminateReply {
    match answer {
        TerminationAnswer::Now => NSApplicationTerminateReply::TerminateNow,
        TerminationAnswer::LaterAndAsk => NSApplicationTerminateReply::TerminateLater,
        TerminationAnswer::CancelAndAsk | TerminationAnswer::Decline | TerminationAnswer::DeclinedOnFault => NSApplicationTerminateReply::TerminateCancel,
    }
}
/// `replyToApplicationShouldTerminate:` on the main thread, only if a
/// "later" is genuinely owed: the flag is taken atomically there, so a reply
/// whose "later" was never given (a fault before the answer) does nothing.
fn reply_on_main(yes: bool) {
    dispatch2::DispatchQueue::main().exec_async(move || {
        if REPLY_OWED.swap(false, Ordering::SeqCst) {
            if let Some(mtm) = MainThreadMarker::new() {
                NSApplication::sharedApplication(mtm).replyToApplicationShouldTerminate(yes);
            }
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
