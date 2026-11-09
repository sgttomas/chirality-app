//! Opaque native act for lowering the App's workflow-approval policy to
//! "Allow disk records". No IPC Boolean, JSON, file, or ordinary button press
//! constructs this event.
pub(crate) struct ConfirmedAssuranceAct { settings: String, epoch: u64 }
impl ConfirmedAssuranceAct {
    pub(crate) fn matches(&self, settings: &str, epoch: u64) -> bool { self.settings == settings && self.epoch == epoch }
    #[cfg(test)] pub(crate) fn synthetic(settings: String, epoch: u64) -> Self { Self { settings, epoch } }
}
pub(crate) fn confirm_assurance_lowering(window: &tauri::Window, settings: String, epoch: u64, protected: bool) -> Result<Option<ConfirmedAssuranceAct>, String> {
    let kept = if protected {
        "Your choice is stored in your keychain and kept across launches."
    } else {
        "Your choice is stored in this App's settings file and kept across launches. Until keychain protection is set up, an agent able to write that file could also change it."
    };
    let statement = super::native_statement::NativeStatement { text: format!("Allow disk records for registered workflows?\n\nA registered revision may then run in any App session after a fresh check that its ledger entry, A15 record and stored bytes agree on disk. That does not verify who approved it: an agent able to write the library ledger, A15 record and store bytes could make a workflow runnable without a person's approval.\n\n{kept}\n\nOnly Allow disk records records this native act. Keep verified approval is the default and changes nothing."), in_app: None };
    if crate::native_lifecycle_confirmation::confirm(window, "Chirality — workflow approval", Ok(statement), "Keep verified approval", "Allow disk records")? {
        Ok(Some(ConfirmedAssuranceAct { settings, epoch }))
    } else { Ok(None) }
}
