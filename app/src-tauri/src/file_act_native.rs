//! Sole production event constructor. The renderer cannot submit a native flag.
use super::*;
use tauri_plugin_dialog::{
    DialogExt, MessageDialogButtons, MessageDialogKind, MessageDialogResult,
};
pub(super) struct ConfirmedFileEvent {
    id: String,
    digest: Value,
    actor: Value,
    context: Value,
    choice: &'static str,
}
impl ConfirmedFileEvent {
    pub(super) fn id(&self) -> &str {
        &self.id
    }
    pub(super) fn digest(&self) -> &Value {
        &self.digest
    }
    pub(super) fn actor(&self) -> &Value {
        &self.actor
    }
    pub(super) fn context(&self) -> &Value {
        &self.context
    }
    pub(super) fn choice(&self) -> &str {
        self.choice
    }
    #[cfg(test)]
    pub(super) fn synthetic(
        id: String,
        digest: Value,
        actor: Value,
        context: Value,
        decline: bool,
    ) -> Self {
        Self {
            id,
            digest,
            actor,
            context,
            choice: if decline { "decline" } else { "act" },
        }
    }
}
/// Root supplies its actual observed actor/owning context; no renderer DTO.
/// Root must call off the UI thread, retain the original control, and ensure the
/// observed home/session/workspace still owns this control before and after.
pub(crate) fn confirm_file_native(
    app: &tauri::AppHandle,
    control: &mut ActControl,
    offer: &FileActOfferRef,
    observe: impl FnMut() -> Result<(Value, Value), String>,
) -> Result<Option<Value>, String> {
    confirm_with_adapter(control, offer, observe, |text, kind| {
        app.dialog()
            .message(text)
            .title("Chirality — act on App content")
            .kind(MessageDialogKind::Warning)
            .buttons(MessageDialogButtons::YesNoCancelCustom(
                kind.wording().into(),
                "Decline this act".into(),
                "Cancel".into(),
            ))
            .blocking_show_with_result()
    })
}
fn confirm_with_adapter(
    control: &mut ActControl,
    offer: &FileActOfferRef,
    mut observe: impl FnMut() -> Result<(Value, Value), String>,
    choose: impl FnOnce(String, FileActKind) -> MessageDialogResult,
) -> Result<Option<Value>, String> {
    let (actor, context) = observe()?;
    let (text, digest, kind) = control.freeze_file_native(offer, &actor, &context)?;
    let result = choose(text, kind);
    let choice = match result {
        MessageDialogResult::Custom(label) if label == kind.wording() => "act",
        MessageDialogResult::Custom(label) if label == "Decline this act" => "decline",
        _ => {
            control.dismiss_file_act(offer);
            return Ok(None);
        }
    };
    let (now_actor, now_context) = match observe() {
        Ok(v) => v,
        Err(e) => {
            control.dismiss_file_act(offer);
            return Err(e);
        }
    };
    if actor != now_actor || context != now_context {
        control.dismiss_file_act(offer);
        return Err("File act actor/owning context changed; nothing captured".into());
    }
    let event = ConfirmedFileEvent {
        id: offer.id.clone(),
        digest,
        actor,
        context,
        choice,
    };
    control.consume_file_event(offer, event).map(Some)
}

/// Synthetic native-dialog adapter, absent from every ordinary build.
#[cfg(test)]
impl ActControl {
    pub(crate) fn synthetic_file_native(
        &mut self,
        offer: &FileActOfferRef,
        observe: impl FnMut() -> Result<(Value, Value), String>,
        choose: impl FnOnce(String, FileActKind) -> MessageDialogResult,
    ) -> Result<Option<Value>, String> {
        confirm_with_adapter(self, offer, observe, choose)
    }
}
