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
    // J6: a statement that would not fit a readable native alert is refused
    // with its cause before it is shown; nothing is captured.
    let text = match crate::act_control::native_statement::bounded(
        "File act native confirmation",
        text,
    ) {
        Ok(text) => text,
        Err(error) => {
            control.dismiss_file_act(offer);
            return Err(error);
        }
    };
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

#[cfg(test)]
mod presentation_tests {
    //! Synthetic adapter only (J6): no native person or dialog is observed.
    use super::*;
    use crate::act_control::native_statement::{MAX_CHARS, MAX_LINES};
    fn workspace() -> (PathBuf, PathBuf) {
        let parent = std::fs::canonicalize(std::env::temp_dir()).unwrap();
        let root = parent.join(crate::util::opaque_id("file-act-native-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let path = root.join("output.txt");
        std::fs::write(&path, b"reviewed App output\n").unwrap();
        (root, path)
    }
    fn facts() -> Result<(Value, Value), String> {
        Ok((person(Some("Synthetic person"), Some("synthetic-os")), json!({"fixture":"owning home 1"})))
    }
    #[test]
    fn file_act_statement_is_bounded_and_complete_for_each_kind() {
        for kind in [FileActKind::Check, FileActKind::Approve, FileActKind::Rely] {
            let (root, path) = workspace();
            let mut control = ActControl::new(&root);
            let offer = control
                .compose_file_act(&path, kind, "one identified output", "test the selected act")
                .unwrap();
            let mut shown = String::new();
            let out = control
                .synthetic_file_native(&offer, facts, |text, _| {
                    shown = text;
                    MessageDialogResult::Custom("Cancel".into())
                })
                .unwrap();
            assert!(out.is_none(), "Cancel captures nothing");
            assert!(shown.lines().count() <= MAX_LINES && shown.chars().count() <= MAX_CHARS, "{shown}");
            for needle in [kind.wording(), "one identified output", "test the selected act", "identity not verified", "Cancel records nothing"] {
                assert!(shown.contains(needle), "{needle} in\n{shown}");
            }
            std::fs::remove_dir_all(root).unwrap();
        }
    }
    #[test]
    fn over_long_file_act_statement_is_refused_before_it_is_shown() {
        let (root, path) = workspace();
        let mut control = ActControl::new(&root);
        let purpose = "a purpose the person typed at length ".repeat(60);
        let offer = control
            .compose_file_act(&path, FileActKind::Check, "one identified output", &purpose)
            .unwrap();
        let mut shown = false;
        let err = control
            .synthetic_file_native(&offer, facts, |_, kind| {
                shown = true;
                MessageDialogResult::Custom(kind.wording().into())
            })
            .unwrap_err();
        assert!(!shown, "never presented");
        assert!(err.contains("exceeds the readable native confirmation"), "{err}");
        assert!(control.native_captures.is_empty());
        let (entries, _) = storage::read_all(&root);
        assert!(entries.is_empty());
        std::fs::remove_dir_all(root).unwrap();
    }
}
