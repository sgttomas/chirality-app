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
//! The installed method makes one atomic reservation attempt and returns
//! Cancel. A worker outside the selector performs App handle and window work
//! and reports faults. That worker is a thread started at installation, before
//! the method is added, and it owns its clone of the App handle; if it cannot
//! start, the method is not added. The method reads the reservation word
//! (`app_quit::QUIT_RESERVATION`) as its first act, reserves only if the word
//! is unchanged, and wakes the worker. A further request that reaches the
//! App's quit admission while an attempt is reserved starts nothing. A system
//! event not yet delivered to the App cannot be told apart from a new request.
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
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::OnceLock;

/// The worker for the system's request, outside the selector.
pub(crate) struct Consumer {
    /// The reserved word the selector hands over (`QuitToken::hand_over`);
    /// zero when empty. At most one is pending: only one attempt is reserved.
    pending: AtomicU64,
    /// The worker's thread, set once it has started.
    thread: OnceLock<std::thread::Thread>,
}
impl Consumer {
    pub(crate) const fn new() -> Self {
        Self { pending: AtomicU64::new(0), thread: OnceLock::new() }
    }
    /// Record the worker's thread. Before this, the selector reserves nothing.
    pub(crate) fn started(&self, thread: std::thread::Thread) -> Result<(), String> {
        self.thread.set(thread).map_err(|_| "already installed once".to_owned())
    }
    /// The worker's loop: wait to be woken, then run each attempt handed over.
    /// A fault in an attempt is caught here and reported; dropping the token
    /// while unwinding has already released the reservation.
    pub(crate) fn serve(&self, reservation: &'static app_quit::QuitReservation, run: impl Fn(app_quit::QuitToken)) {
        loop {
            std::thread::park();
            while let Some(reserved) = self.take() {
                let token = app_quit::QuitToken::adopt(reservation, reserved);
                if std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| run(token))).is_err() {
                    app_quit::diagnostic("quit routes: a fault ended the system's quit attempt on its worker");
                }
            }
        }
    }
    fn take(&self) -> Option<u64> {
        match self.pending.swap(0, Ordering::SeqCst) {
            0 => None,
            reserved => Some(reserved),
        }
    }
    #[cfg(test)]
    pub(crate) fn is_pending(&self) -> bool {
        self.pending.load(Ordering::SeqCst) != 0
    }
}
static CONSUMER: Consumer = Consumer::new();

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
    if class.responds_to(selector()) {
        return Ok(Installed::AlreadyResponds);
    }
    // The worker is settled before the method is published.
    if CONSUMER.thread.get().is_some() {
        return Err("already installed once".into());
    }
    let app = app.clone();
    let worker = std::thread::Builder::new()
        .name("chirality-system-quit".into())
        .spawn(move || CONSUMER.serve(&app_quit::QUIT_RESERVATION, |token| crate::quit_worker(app.clone(), app_quit::QuitRoute::System, token)))
        .map_err(|error| format!("its worker thread could not start ({error})"))?;
    CONSUMER.started(worker.thread().clone())?;
    // SAFETY: `should_terminate` has the signature `install_on` requires.
    unsafe { install_on(class, std::mem::transmute::<ShouldTerminate, Imp>(should_terminate)) }
}

pub(crate) type ShouldTerminate = extern "C-unwind" fn(&AnyObject, Sel, *mut AnyObject) -> NSApplicationTerminateReply;

/// `applicationShouldTerminate:`. AppKit calls it on the main thread.
pub(crate) extern "C-unwind" fn should_terminate(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
    answer_terminate(&app_quit::QUIT_RESERVATION, &CONSUMER)
}
/// The selector's body: read the reservation word, then one compare and
/// exchange; a granted reservation is handed to the worker, which is woken.
/// Always Cancel.
///
/// Nothing here can unwind, so the panic hook never runs in the selector:
/// atomic loads and stores, one compare and exchange, `OnceLock::get` (an
/// atomic load) and `Thread::unpark`. In the pinned Rust 1.97.1 standard
/// library for Apple targets, `unpark` swaps the thread parker's state
/// atomically and, if the worker is parked, calls
/// `dispatch_semaphore_signal` (`std/src/sys/sync/thread_parking/darwin.rs`),
/// which wakes a waiter and does not wait. None of these allocates, takes a
/// lock or writes output.
pub(crate) fn answer_terminate(reservation: &'static app_quit::QuitReservation, consumer: &Consumer) -> NSApplicationTerminateReply {
    let observed = reservation.observe();
    if let Some(worker) = consumer.thread.get() {
        app_quit::system_request(reservation, observed, |token| {
            consumer.pending.store(token.hand_over(), Ordering::SeqCst);
            worker.unpark();
        });
    }
    NSApplicationTerminateReply::TerminateCancel
}

// Tests: `app_quit_tests.rs` (`macos_quit_routes`), in the `app_quit::tests`
// pull-request cohort.
