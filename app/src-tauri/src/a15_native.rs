//! Native-only A15 event producer. No production constructor or serde surface.
use crate::act_control::{native_statement, A15OfferRef, ActControl, HotA15Result};
use crate::workflow_workspace::registration::ReviewSession;
use serde_json::Value;
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
/// The act button's label. Only an explicit choice of it captures.
pub(crate) const REGISTER: &str = "Register";
/// The alert's buttons. Register stays in the first (ok) slot and Cancel in the
/// cancel slot: tauri-plugin-dialog 2.7.2 maps any unmatched or aborted modal
/// result (rfd `Cancel`) to the cancel-slot label, so that slot must never be
/// the act. Moving Cancel to the default position therefore needs another
/// button layout (returned to the caller, J6), not a swap.
pub(crate) fn a15_buttons() -> MessageDialogButtons {
    MessageDialogButtons::OkCancelCustom(REGISTER.into(), "Cancel".into())
}
/// Actual host-native path. Root owns retained session/library/home state and
/// supplies observed actor/context from current_actor_context_for, with actual
/// owning-home/library/session rechecks inside observe. No webview DTO reaches
/// these arguments. Closure supplies facts; only actual blocking_show creates
/// the opaque event. Holding the session prevents replacement while current()
/// additionally rereads actual live entries/slot before and after the dialog.
///
/// J6 D-1: the alert carries the bounded statement only; the complete review is
/// shown in the App and named in the statement by reference and digest. Only
/// the explicit Register result captures.
pub(crate) fn confirm_native(
    app: &tauri::AppHandle,
    control: &mut ActControl,
    session: &ReviewSession,
    offer: &A15OfferRef,
    observe: impl FnMut() -> Result<(Value, Value), String>,
) -> Result<Option<HotA15Result>, String> {
    confirm_with_adapter(control, session, offer, observe, |text| {
        app.dialog()
            .message(text)
            .title("Chirality — register workflow")
            .kind(MessageDialogKind::Warning)
            .buttons(a15_buttons())
            .blocking_show_with_result()
    })
}
fn confirm_with_adapter(
    control: &mut ActControl,
    session: &ReviewSession,
    offer: &A15OfferRef,
    mut observe: impl FnMut() -> Result<(Value, Value), String>,
    choose: impl FnOnce(String) -> MessageDialogResult,
) -> Result<Option<HotA15Result>, String> {
    let (actor, context) = observe()?;
    let text = {
        let current = session.current()?;
        control.a15_confirmation_text(offer, &current, &actor, &context)?
    };
    let offer_id = offer.id().to_owned();
    let offer_digest = control.frozen_a15_offer_digest(offer)?.clone();
    control.present_a15(offer)?;
    if !native_statement::chose(&choose(text), REGISTER) {
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
    choose: impl FnOnce(String) -> MessageDialogResult,
) -> Result<Option<HotA15Result>, String> {
    confirm_with_adapter(control, session, offer, observe, choose)
}
