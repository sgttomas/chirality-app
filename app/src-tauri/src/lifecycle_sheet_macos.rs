//! Exact App-created sheet lifetime; no AX discovery or public cancellation API.
//! This backend is staged separately from PR68; product lifetime selection and
//! controller admission remain prerequisites before wiring it into live use.
use super::lease::Lease;
use block2::RcBlock;
use objc2::{rc::Retained, MainThreadMarker};
use objc2_app_kit::{NSAlert, NSAlertStyle, NSModalResponseCancel, NSView, NSWindow};
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
    blocked: bool,
}
thread_local! { static PENDING: RefCell<Option<Pending>> = const { RefCell::new(None) }; }
static NEXT_ID: AtomicU64 = AtomicU64::new(1);
const UNSUPPORTED: &str =
    "Original native lifecycle sheet could not be safely dismissed; original custody remains held";

fn same(a: &NSWindow, b: &NSWindow) -> bool {
    std::ptr::eq(a, b)
}
fn original_relation(p: &Pending) -> bool {
    p.sheet
        .sheetParent()
        .is_some_and(|parent| same(&parent, &p.parent))
        && p.parent
            .attachedSheet()
            .is_some_and(|sheet| same(&sheet, &p.sheet))
}
fn finish(id: u64, response: isize) {
    let pending = PENDING.with(|cell| {
        let mut slot = cell.borrow_mut();
        if slot.as_ref().is_some_and(|p| p.lease.is_for(id)) {
            slot.take()
        } else {
            None
        }
    });
    let Some(mut p) = pending else {
        return;
    };
    // Only the exact sheet created for this question is ordered out. This is
    // required by the endSheet completion lifecycle, never a discovered window.
    if p.sheet
        .sheetParent()
        .is_some_and(|parent| !same(&parent, &p.parent))
    {
        p.blocked = true;
        eprintln!("chirality: {UNSUPPORTED}");
        PENDING.with(|cell| *cell.borrow_mut() = Some(p));
        return;
    }
    p.sheet.orderOut(None);
    if p.sheet.sheetParent().is_some()
        || p.sheet.isVisible()
        || p.parent.sheets().iter().any(|sheet| same(&sheet, &p.sheet))
    {
        p.blocked = true;
        eprintln!("chirality: {UNSUPPORTED}");
        PENDING.with(|cell| *cell.borrow_mut() = Some(p));
        return; // do not release the question gate before actual dismissal
    }
    let result = p.lease.result_allowed(id, Instant::now()).and_then(|()| {
        let label = response
            .checked_sub(1000)
            .and_then(|index| usize::try_from(index).ok())
            .and_then(|index| p.labels.get(index))
            .ok_or_else(|| {
                "Native lifecycle sheet ended without a recognized choice; no act authorized"
                    .to_string()
            })?;
        Ok(if p.labels.len() == 1 && label == "OK" {
            MessageDialogResult::Ok
        } else {
            MessageDialogResult::Custom(label.clone())
        })
    });
    let _ = p.send.send(result);
    // Dropping p releases the retained original alert and window after its
    // completion and dismissal; a stale timer holds only the never-reused id.
}
fn expire(id: u64) {
    let target = PENDING.with(|cell| {
        let mut slot = cell.borrow_mut();
        let p = slot.as_mut().filter(|p| p.lease.is_for(id))?;
        if p.blocked || !p.lease.request_expiry(id, Instant::now()) {
            return None;
        }
        if !original_relation(p) {
            p.blocked = true;
            eprintln!("chirality: {UNSUPPORTED}");
            return None;
        }
        Some((p.parent.clone(), p.sheet.clone()))
    });
    if let Some((parent, sheet)) = target {
        // Expiry is consumed before dispatch; the exact original relation was
        // just checked on this main-thread turn. The callback reports refusal.
        parent.endSheet_returnCode(&sheet, NSModalResponseCancel);
    }
}

pub(super) fn show(
    parent: &impl HasWindowHandle,
    title: String,
    text: String,
    buttons: MessageDialogButtons,
    lifetime: Duration,
    send: Sender<Result<MessageDialogResult, String>>,
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
    if !parent.sheets().is_empty() || PENDING.with(|cell| cell.borrow().is_some()) {
        return Err("Another sheet is open; lifecycle question not queued".into());
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
            blocked: false,
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
