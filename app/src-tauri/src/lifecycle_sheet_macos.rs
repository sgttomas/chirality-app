//! Exact App-created sheet lifetime; no AX discovery or public cancellation API.
//! This backend is staged separately from PR68; product lifetime selection and
//! controller admission remain prerequisites before wiring it into live use.
use super::lease::{self, Dismissal, Lease, Timer, Verify};
use block2::RcBlock;
use objc2::{rc::Retained, MainThreadMarker};
use objc2_app_kit::{
    NSAlert, NSAlertStyle, NSApplication, NSModalResponseCancel, NSView, NSWindow,
};
use objc2_foundation::NSString;
use raw_window_handle::{HasWindowHandle, RawWindowHandle};
use std::{
    cell::RefCell,
    sync::{
        atomic::{AtomicU64, Ordering},
        mpsc::Sender,
    },
    time::{Duration, Instant},
};
use tauri_plugin_dialog::{MessageDialogButtons, MessageDialogResult};

struct Pending {
    parent: Retained<NSWindow>,
    _alert: Retained<NSAlert>,
    sheet: Retained<NSWindow>,
    labels: Vec<String>,
    lease: Lease,
    send: Sender<Result<MessageDialogResult, String>>,
    status: Sender<Status>,
    reported_hold: bool,
}
thread_local! { static PENDING: RefCell<Option<Pending>> = const { RefCell::new(None) }; }
static NEXT_ID: AtomicU64 = AtomicU64::new(1);
const UNSUPPORTED: &str =
    "Original native lifecycle sheet could not be safely dismissed; original custody remains held";

fn same(a: &NSWindow, b: &NSWindow) -> bool {
    std::ptr::eq(a, b)
}
/// Separate from the result channel: unsupported custody is observable even
/// while the final result and native ownership remain withheld.
#[derive(Debug)]
pub(super) enum Status {
    Held(&'static str),
}

fn held(id: u64) {
    PENDING.with(|cell| {
        if let Some(p) = cell.borrow_mut().as_mut().filter(|p| p.lease.is_for(id)) {
            p.lease.hold();
            if !p.reported_hold {
                p.reported_hold = true;
                eprintln!("chirality: {UNSUPPORTED}");
                let _ = p.status.send(Status::Held(UNSUPPORTED));
            }
        }
    });
}
fn target(id: u64) -> Option<(Retained<NSWindow>, Retained<NSWindow>)> {
    PENDING.with(|cell| {
        cell.borrow()
            .as_ref()
            .filter(|p| p.lease.is_for(id))
            .map(|p| (p.parent.clone(), p.sheet.clone()))
    })
}
fn later(id: u64, delay: Duration, work: fn(u64)) {
    let Ok(when) = dispatch2::DispatchTime::try_from(delay) else {
        held(id);
        return;
    };
    // dispatch2 0.3.1 after currently always returns Ok. Do not treat this as
    // proof the main queue will run or that native dismissal will complete.
    if dispatch2::DispatchQueue::main()
        .after(when, move || work(id))
        .is_err()
    {
        held(id);
    }
}
fn verify(id: u64) {
    let Some((parent, sheet)) = target(id) else {
        return;
    };
    let relation = sheet.sheetParent();
    let facts = Dismissal {
        parent_present: relation.is_some(),
        parent_changed: relation.is_some_and(|p| !same(&p, &parent)),
        visible: sheet.isVisible(),
        listed: parent.sheets().iter().any(|s| same(&s, &sheet)),
    };
    let decision = PENDING.with(|cell| {
        cell.borrow_mut()
            .as_mut()
            .filter(|p| p.lease.is_for(id))
            .map_or(Verify::Ignore, |p| {
                p.lease.verify(id, Instant::now(), facts)
            })
    });
    match decision {
        Verify::Ignore => {}
        Verify::Later => later(id, Duration::from_millis(50), verify),
        Verify::Hold => held(id),
        Verify::Released(response) => {
            let pending = PENDING.with(|cell| {
                let mut slot = cell.borrow_mut();
                if slot.as_ref().is_some_and(|p| p.lease.is_for(id)) {
                    slot.take()
                } else {
                    None
                }
            });
            if let Some(p) = pending {
                let result = p.lease.result_allowed(id, Instant::now()).and_then(|()| {
                    let index = lease::choice_index(response, p.labels.len())?;
                    Ok(if p.labels.len() == 1 {
                        MessageDialogResult::Ok
                    } else {
                        MessageDialogResult::Custom(p.labels[index].clone())
                    })
                });
                let _ = p.send.send(result);
            }
        }
    }
}
fn finish(id: u64, response: isize) {
    let first = PENDING.with(|cell| {
        cell.borrow_mut()
            .as_mut()
            .filter(|p| p.lease.is_for(id))
            .is_some_and(|p| p.lease.completion(id, response, Instant::now()))
    });
    if !first {
        return;
    }
    let Some((parent, sheet)) = target(id) else {
        return;
    };
    if sheet.sheetParent().is_some_and(|p| !same(&p, &parent)) {
        held(id);
        return;
    }
    // Keep the slot throughout native completion. AppKit may still be ending
    // the sheet here: order out once, then verify on later main-queue turns.
    sheet.orderOut(None);
    later(id, Duration::from_millis(50), verify);
}
fn completion_due(id: u64) {
    let missing = PENDING.with(|cell| {
        cell.borrow()
            .as_ref()
            .filter(|p| p.lease.is_for(id))
            .is_some_and(|p| !p.lease.has_completion())
    });
    if missing {
        held(id);
    }
}
fn expire(id: u64) {
    let action = PENDING.with(|cell| {
        cell.borrow_mut()
            .as_mut()
            .filter(|p| p.lease.is_for(id))
            .map_or(Timer::Ignore, |p| p.lease.timer(id, Instant::now()))
    });
    match action {
        Timer::Ignore => {}
        Timer::Hold => held(id),
        Timer::After(remaining) => later(id, remaining, expire),
        Timer::End => {
            let Some((parent, sheet)) = target(id) else {
                return;
            };
            if !sheet.sheetParent().is_some_and(|p| same(&p, &parent))
                || !parent.attachedSheet().is_some_and(|s| same(&s, &sheet))
            {
                held(id);
                return;
            }
            // Lease consumed first; no RefCell borrow crosses the native call.
            // A button may already be ending before its completion callback;
            // that AppKit race is still a native qualification prerequisite.
            parent.endSheet_returnCode(&sheet, NSModalResponseCancel);
            later(id, Duration::from_secs(1), completion_due);
        }
    }
}

pub(super) fn show(
    parent: &impl HasWindowHandle,
    title: String,
    text: String,
    buttons: MessageDialogButtons,
    lifetime: Duration,
    send: Sender<Result<MessageDialogResult, String>>,
    status: Sender<Status>,
) -> Result<(), String> {
    let mtm =
        MainThreadMarker::new().ok_or("Lifecycle sheet must be created on the main thread")?;
    if lifetime.is_zero() {
        return Err("Lifecycle sheet lifetime unavailable".into());
    }
    let labels = match buttons {
        MessageDialogButtons::YesNoCancelCustom(keep, act, cancel) => vec![keep, act, cancel],
        MessageDialogButtons::Ok => vec!["OK".into()],
        _ => return Err("Unsupported lifecycle sheet choices".into()),
    };
    let handle = parent
        .window_handle()
        .map_err(|_| "Original App window unavailable")?;
    let RawWindowHandle::AppKit(handle) = handle.as_raw() else {
        return Err("Original AppKit window required".into());
    };
    // SAFETY: the successful borrowed Tauri AppKit handle belongs to the retained
    // invoker. Access and retain occur synchronously on the main thread.
    let view = unsafe { Retained::retain(handle.ns_view.cast::<NSView>().as_ptr()) }
        .ok_or("Original App view unavailable")?;
    let parent = view.window().ok_or("Original App window unavailable")?;
    let app = NSApplication::sharedApplication(mtm);
    lease::admit(
        parent.isVisible(),
        parent.isMiniaturized(),
        parent.sheetParent().is_some(),
        !parent.sheets().is_empty(),
        app.modalWindow().is_some(),
        PENDING.with(|cell| cell.borrow().is_some()),
    )?;
    if !app.isRunning() {
        return Err("App event loop unavailable; lifecycle question not shown".into());
    }
    let id = NEXT_ID
        .fetch_update(Ordering::Relaxed, Ordering::Relaxed, |id| id.checked_add(1))
        .map_err(|_| "Lifecycle question identity exhausted")?;
    let alert = NSAlert::new(mtm);
    alert.setMessageText(&NSString::from_str(&title));
    alert.setInformativeText(&NSString::from_str(&text));
    alert.setAlertStyle(NSAlertStyle::Informational);
    for label in &labels {
        alert.addButtonWithTitle(&NSString::from_str(label));
    }
    let sheet = alert.window();
    let deadline = Instant::now()
        .checked_add(lifetime)
        .ok_or("Lifecycle deadline unavailable")?;
    let when =
        dispatch2::DispatchTime::try_from(lifetime).map_err(|_| "Lifecycle timer unavailable")?;
    // Store the exact retained pair before presentation/callback; no raw pointer
    // or native object is sent to another thread, and there is no external key.
    PENDING.with(|cell| {
        *cell.borrow_mut() = Some(Pending {
            parent: parent.clone(),
            _alert: alert.clone(),
            sheet,
            labels,
            lease: Lease::new(id, deadline),
            send,
            status,
            reported_hold: false,
        })
    });
    if dispatch2::DispatchQueue::main()
        .after(when, move || expire(id))
        .is_err()
    {
        PENDING.with(|cell| {
            cell.borrow_mut().take();
        });
        return Err("Lifecycle timer could not be scheduled; question not shown".into());
    }
    let completion = RcBlock::new(move |response| finish(id, response));
    alert.beginSheetModalForWindow_completionHandler(&parent, Some(&completion));
    Ok(())
}
