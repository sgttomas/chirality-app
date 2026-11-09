//! Opaque native act for the App's process-local assurance preference.
//! No IPC Boolean, JSON, file, or ordinary button press constructs this event.
pub(crate) struct ConfirmedAssuranceAct { settings: String, epoch: u64 }
impl ConfirmedAssuranceAct {
    pub(crate) fn matches(&self, settings: &str, epoch: u64) -> bool { self.settings == settings && self.epoch == epoch }
    #[cfg(test)] pub(crate) fn synthetic(settings: String, epoch: u64) -> Self { Self { settings, epoch } }
}
pub(crate) fn confirm_assurance_lowering(window: &tauri::Window, settings: String, epoch: u64) -> Result<Option<ConfirmedAssuranceAct>, String> {
    let statement = super::native_statement::NativeStatement { text: "Choose relaxed workflow assurance for this App session?\n\nRegistered revisions may run after a fresh disk check without verifying a capture seal. An agent able to write the library ledger, A15 record and store bytes could make a workflow runnable without a person's approval.\n\nOnly Choose relaxed records this native act. Keep current assurance is the default and changes nothing. This session's level resets to the default on relaunch.".into(), in_app: None };
    if crate::native_lifecycle_confirmation::confirm(window, "Chirality — workflow assurance", Ok(statement), "Keep current assurance", "Choose relaxed")? {
        Ok(Some(ConfirmedAssuranceAct { settings, epoch }))
    } else { Ok(None) }
}
