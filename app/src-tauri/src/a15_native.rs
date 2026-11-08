//! Native-only A15 event producer. No production constructor or serde surface.
use crate::act_control::{native_statement, A15OfferRef, A15Variant, ActControl, HotA15Result};
use crate::workflow_workspace::registration::ReviewSession;
use raw_window_handle::{DisplayHandle, HandleError, HasDisplayHandle, HasWindowHandle, WindowHandle};
use serde_json::Value;
use std::sync::mpsc;
use tauri_plugin_dialog::{DialogExt, MessageDialogButtons, MessageDialogKind, MessageDialogResult};

pub(crate) struct ConfirmedA15Event {
    offer_id: String,
    offer_digest: Value,
    actor: Value,
    owning_context: Value,
}
impl ConfirmedA15Event {
    pub(crate) fn offer_id(&self) -> &str {
        &self.offer_id
    }
    pub(crate) fn offer_digest(&self) -> &Value {
        &self.offer_digest
    }
    pub(crate) fn actor(&self) -> &Value {
        &self.actor
    }
    pub(crate) fn owning_context(&self) -> &Value {
        &self.owning_context
    }
    /// Synthetic unit-test witness only. Absent from an ordinary build.
    #[cfg(test)]
    pub(crate) fn synthetic_for_test(
        offer_id: String,
        offer_digest: Value,
        actor: Value,
        owning_context: Value,
    ) -> Self {
        Self {
            offer_id,
            offer_digest,
            actor,
            owning_context,
        }
    }
}
/// The alert's buttons (OWNER_DECISIONS "Native confirmation default key —
/// 2026-10-08"): [Don't ‹act› (default)] [‹Act›] [Cancel]. Return chooses the
/// first, which records nothing; tauri-plugin-dialog 2.7.2 reports any
/// unmatched, failed or aborted dialog as the third, "Cancel". Only the middle
/// label captures (`native_statement::chose`).
pub(crate) fn a15_buttons(variant: A15Variant) -> MessageDialogButtons {
    native_statement::act_buttons(variant.dont, variant.act)
}
/// Actual host-native path. Root owns retained session/library/home state and
/// supplies observed actor/context from current_actor_context_for, with actual
/// owning-home/library/session rechecks inside observe. No webview DTO reaches
/// these arguments. Closure supplies facts; only the explicit native sheet result creates
/// the opaque event. Holding the session prevents replacement while current()
/// additionally rereads actual live entries/slot before and after the dialog.
///
/// J6 D-1: the alert carries the bounded statement only; the complete review is
/// shown in the App (also while the alert is open) and named in the statement
/// by reference and digest. Only the explicit middle (act) result captures.
pub(crate) fn confirm_native(
    invoking: &tauri::Window,
    control: &mut ActControl,
    session: &ReviewSession,
    offer: &A15OfferRef,
    observe: impl FnMut() -> Result<(Value, Value), String>,
) -> Result<Option<HotA15Result>, String> {
    confirm_with_adapter(control, session, offer, observe, |text, buttons, act| {
        present_in_original(invoking, text, buttons, act)
    })
}

const UNAVAILABLE: &str = "Invoking App window unavailable; A15 confirmation refused";

// The plugin silently ignores failed parent lookups. Cache both handles before
// calling it so an unavailable original can never select a parentless alert.
struct Parent<'a> {
    window: WindowHandle<'a>,
    display: DisplayHandle<'a>,
}
impl HasWindowHandle for Parent<'_> {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> { Ok(self.window) }
}
impl HasDisplayHandle for Parent<'_> {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> { Ok(self.display) }
}
fn checked_parent<T>(
    original: &(impl HasWindowHandle + HasDisplayHandle),
    present: impl FnOnce(&Parent<'_>) -> T,
) -> Result<T, String> {
    let parent = Parent {
        window: original.window_handle().map_err(|_| UNAVAILABLE)?,
        display: original.display_handle().map_err(|_| UNAVAILABLE)?,
    };
    Ok(present(&parent))
}
fn result_in_original(
    original: &(impl HasWindowHandle + HasDisplayHandle),
    result: MessageDialogResult,
    act: &str,
) -> Result<MessageDialogResult, String> {
    if native_statement::chose(&result, act) { checked_parent(original, |_| ())?; }
    Ok(result)
}
fn receive_result(
    receive: mpsc::Receiver<Result<MessageDialogResult, String>>,
) -> Result<MessageDialogResult, String> {
    receive.recv().map_err(|_| "A15 confirmation ended without a result; nothing captured".to_string())?
}

// Only the async IPC worker waits. Validation, parenting and callback-based
// sheet presentation share one main-thread turn, using the actual IPC invoker.
fn present_in_original(
    invoking: &tauri::Window,
    text: String,
    buttons: MessageDialogButtons,
    act: &str,
) -> Result<MessageDialogResult, String> {
    let (send, receive) = mpsc::channel();
    let window = invoking.clone();
    let act = act.to_owned();
    invoking.run_on_main_thread(move || {
        let failure = send.clone();
        if let Err(error) = checked_parent(&window, |parent| {
            window.dialog().message(text).title("Chirality — register workflow")
                .kind(MessageDialogKind::Warning).buttons(buttons).parent(parent)
                .show_with_result({
                    let window = window.clone();
                    move |result| {
                        if !native_statement::chose(&result, &act) {
                            let _ = send.send(Ok(result));
                            return;
                        }
                        let original = window.clone();
                        let failure = send.clone();
                        if window.run_on_main_thread(move || {
                            let _ = send.send(result_in_original(&original, result, &act));
                        }).is_err() {
                            let _ = failure.send(Err(UNAVAILABLE.into()));
                        }
                    }
                });
        }) { let _ = failure.send(Err(error)); }
    }).map_err(|_| "Invoking App window could not present A15 confirmation".to_string())?;
    receive_result(receive)
}

fn confirm_with_adapter(
    control: &mut ActControl,
    session: &ReviewSession,
    offer: &A15OfferRef,
    mut observe: impl FnMut() -> Result<(Value, Value), String>,
    choose: impl FnOnce(String, MessageDialogButtons, &str) -> Result<MessageDialogResult, String>,
) -> Result<Option<HotA15Result>, String> {
    let (actor, context) = observe()?;
    let text = {
        let current = session.current()?;
        control.a15_confirmation_text(offer, &current, &actor, &context)?
    };
    let offer_id = offer.id().to_owned();
    let offer_digest = control.frozen_a15_offer_digest(offer)?.clone();
    let variant = control.a15_variant(offer)?;
    let in_app = control.a15_in_app(offer)?;
    control.present_a15(offer)?;
    let result = match native_statement::showing_in_app(Some(&in_app), || {
        choose(text, a15_buttons(variant), variant.act)
    }) {
        Ok(result) => result,
        Err(error) => {
            control.dismiss_a15(offer);
            return Err(error);
        }
    };
    if !native_statement::chose(&result, variant.act) {
        control.dismiss_a15(offer);
        return Ok(None);
    }
    let (current_actor, current_context) = match observe() {
        Ok(facts) => facts,
        Err(e) => {
            control.dismiss_a15(offer);
            return Err(e);
        }
    };
    if actor != current_actor || context != current_context {
        control.dismiss_a15(offer);
        return Err(
            "A15 attribution or owning host context changed; nothing captured; review again".into(),
        );
    }
    let current = match session.current() {
        Ok(view) => view,
        Err(e) => {
            control.dismiss_a15(offer);
            return Err(e);
        }
    };
    // Sole production event constructor. No Boolean, InputSource or file can
    // enter confirm_a15_after_native_event without the explicit Register choice.
    let event = ConfirmedA15Event {
        offer_id,
        offer_digest,
        actor,
        owning_context: context,
    };
    control
        .confirm_a15_after_native_event(offer, event, &current)
        .map(Some)
}

/// Synthetic native-dialog adapter, absent from every ordinary build.
#[cfg(test)]
pub(crate) fn synthetic_a15_native(
    control: &mut ActControl,
    session: &ReviewSession,
    offer: &A15OfferRef,
    observe: impl FnMut() -> Result<(Value, Value), String>,
    choose: impl FnOnce(String, MessageDialogButtons) -> MessageDialogResult,
) -> Result<Option<HotA15Result>, String> {
    confirm_with_adapter(control, session, offer, observe, |text, buttons, _| Ok(choose(text, buttons)))
}

#[cfg(test)]
pub(crate) fn synthetic_a15_native_result(
    control: &mut ActControl,
    session: &ReviewSession,
    offer: &A15OfferRef,
    observe: impl FnMut() -> Result<(Value, Value), String>,
    choose: impl FnOnce(String, MessageDialogButtons, &str) -> Result<MessageDialogResult, String>,
) -> Result<Option<HotA15Result>, String> {
    confirm_with_adapter(control, session, offer, observe, choose)
}

#[cfg(test)]
#[path = "a15_native_tests.rs"]
mod tests;
