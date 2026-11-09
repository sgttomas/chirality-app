//! App-only assurance preference. No file, environment or renderer value is authority.
use crate::workflow_workspace::registration::AssuranceLevel;
use serde_json::{json, Value};
use std::sync::{Arc, Mutex};

pub(crate) type Policy = Arc<Mutex<AssuranceLevel>>;
struct Resolved { default: AssuranceLevel, reason: String, chosen: bool, epoch: u64 }
pub(crate) struct Settings {
    pub(crate) policy: Policy,
    resolved: Mutex<Option<Resolved>>,
    identity: String,
}
impl Default for Settings {
    fn default() -> Self {
        Self { policy: Arc::new(Mutex::new(AssuranceLevel::Robust)), resolved: Mutex::new(None), identity: crate::util::opaque_id("assurance:").expect("App assurance identity") }
    }
}
impl Settings {
    fn resolve(&self) {
        let mut state = self.resolved.lock().unwrap();
        if state.is_none() { Self::resolve_with(&self.policy, &mut state, crate::capture_seal::keychain_available()); }
    }
    fn resolve_with(policy: &Policy, state: &mut Option<Resolved>, available: Result<(), String>) {
        if state.is_some() { return; }
        let (level, reason) = match available {
            Ok(()) => (AssuranceLevel::Robust, "Gated SEAL-C keychain provider works on this installation".into()),
            Err(reason) => (AssuranceLevel::Relaxed, format!("Gated SEAL-C keychain provider unavailable: {reason}; the owner's initial default is relaxed")),
        };
        *policy.lock().unwrap() = level;
        *state = Some(Resolved { default: level, reason, chosen: false, epoch: 0 });
    }
    pub(crate) fn policy(&self) -> Policy { self.resolve(); self.policy.clone() }
    pub(crate) fn view(&self) -> Value {
        self.resolve();
        let state = self.resolved.lock().unwrap(); let state = state.as_ref().unwrap();
        json!({"level":self.policy.lock().unwrap().label(),"default":state.default.label(),"defaultReason":state.reason,"chosenInSession":state.chosen,"scope":"App setting held only in host process memory. A level chosen in this session resets to the default on relaunch.","lowering":"Choosing relaxed requires a person's native confirmation; a command or file cannot lower the level."})
    }
    /// Raising needs no act; requesting relaxed through this plain path refuses.
    pub(crate) fn request(&self, level: AssuranceLevel) -> Result<(), String> {
        self.resolve();
        if level == AssuranceLevel::Relaxed { return Err("Lowering requires a person's native act; a plain command cannot choose relaxed".into()); }
        let mut state = self.resolved.lock().unwrap(); let state = state.as_mut().unwrap();
        *self.policy.lock().unwrap() = level; state.chosen = true; state.epoch += 1; Ok(())
    }
    pub(crate) fn lowering_context(&self) -> (String, u64) {
        self.resolve(); (self.identity.clone(), self.resolved.lock().unwrap().as_ref().unwrap().epoch)
    }
    pub(crate) fn lower(&self, event: crate::act_control::ConfirmedAssuranceAct) -> Result<(), String> {
        self.resolve();
        let mut state = self.resolved.lock().unwrap(); let state = state.as_mut().unwrap();
        if !event.matches(&self.identity, state.epoch) { return Err("App assurance setting changed while the native question was open; no lowering".into()); }
        *self.policy.lock().unwrap() = AssuranceLevel::Relaxed; state.chosen = true; state.epoch += 1; Ok(())
    }
}
#[cfg(test)] mod tests {
    use super::*;
    #[test] fn default_is_resolved_once_from_keychain_availability() {
        for available in [true, false] {
            let settings = Settings::default();
            let result = if available { Ok(()) } else { Err("not enrolled".into()) };
            Settings::resolve_with(&settings.policy, &mut settings.resolved.lock().unwrap(), result);
            assert_eq!(settings.view()["level"], if available { "robust" } else { "relaxed" });
            settings.request(AssuranceLevel::Robust).unwrap();
            Settings::resolve_with(&settings.policy, &mut settings.resolved.lock().unwrap(), Err("locked later".into()));
            assert_eq!(settings.view()["level"], "robust", "explicit robust never auto-lowers");
        }
    }
    #[test] fn lowering_needs_original_native_act_and_never_reads_an_agent_file() {
        let settings = Settings::default(); settings.request(AssuranceLevel::Robust).unwrap();
        assert!(settings.request(AssuranceLevel::Relaxed).is_err());
        let scratch = std::env::temp_dir().join(crate::util::opaque_id("assurance-test-").unwrap());
        std::fs::create_dir(&scratch).unwrap();
        std::fs::write(scratch.join("settings.json"), r#"{"assurance":"relaxed"}"#).unwrap();
        assert_eq!(settings.view()["level"], "robust", "no path or file ingestion exists");
        let (id, epoch) = settings.lowering_context();
        settings.request(AssuranceLevel::Robust).unwrap();
        assert!(settings.lower(crate::act_control::ConfirmedAssuranceAct::synthetic(id, epoch)).is_err());
        let (id, epoch) = settings.lowering_context();
        settings.lower(crate::act_control::ConfirmedAssuranceAct::synthetic(id, epoch)).unwrap();
        assert_eq!(settings.view()["level"], "relaxed");
        std::fs::remove_dir_all(scratch).unwrap();
    }
}
