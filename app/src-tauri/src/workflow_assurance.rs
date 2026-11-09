//! The person's workflow-approval policy (owner decisions A, B and C,
//! 2026-11-09). Two policies:
//! - "Allow disk records" (relaxed): fresh LS-1 disk consistency admits a
//!   registered revision across sessions; approval authenticity is unverified.
//! - "Require verified approval" (robust): a matching native A15 held in this
//!   process, or an approval verified by keychain seal across sessions once
//!   keychain protection is set up.
//!
//! The choice persists across launches, outside any project. Before keychain
//! protection is set up it lives in the App's settings file in AppData; an
//! agent able to write that file could change it (decision B, disclosed). Once
//! set up it lives in the keychain through the gated SEAL-C provider and
//! lowering needs a native act. No project file or IPC value lowers it, and no
//! keychain or verification failure lowers it: a missing, locked or corrupt
//! protected policy reads as "Require verified approval" with recovery offered.
use crate::workflow_workspace::registration::AssuranceLevel;
use serde_json::{json, Value};
use std::{
    path::PathBuf,
    sync::{Arc, Mutex},
};

/// The level the library owners apply; updated only by `Settings`.
pub(crate) type Policy = Arc<Mutex<AssuranceLevel>>;

pub(crate) const RELAXED_NAME: &str = "Allow disk records";
pub(crate) const ROBUST_NAME: &str = "Require verified approval";
const SETTINGS_FILE: &str = "workflow-approval-policy.json";
const SETTINGS_FORMAT: &str = "chirality.app.workflow-approval-policy-setting";

pub(crate) fn policy_name(level: AssuranceLevel) -> &'static str {
    match level {
        AssuranceLevel::Relaxed => RELAXED_NAME,
        AssuranceLevel::Robust => ROBUST_NAME,
    }
}
fn parse(level: &str) -> Option<AssuranceLevel> {
    match level {
        "robust" => Some(AssuranceLevel::Robust),
        "relaxed" => Some(AssuranceLevel::Relaxed),
        _ => None,
    }
}

/// What a store holds. `Absent { enrolled }` distinguishes "never stored" from
/// a protected installation whose policy item is missing.
pub(crate) enum Stored {
    Level(AssuranceLevel),
    Absent { enrolled: bool },
}
/// A place the policy persists. The keychain store is `None` on a build
/// without a selected keychain provider (unsigned or development).
pub(crate) trait Store: Send + Sync {
    fn read(&self) -> Result<Stored, String>;
    fn write(&self, level: AssuranceLevel) -> Result<(), String>;
}

/// The App's settings file in AppData (decision B). Agent-writable; disclosed.
struct SettingsFile;
static FOLDER: Mutex<Option<PathBuf>> = Mutex::new(None);
/// Install the App data folder at startup (as `capture_seal::install`).
pub(crate) fn install(app_data: &std::path::Path) {
    *FOLDER.lock().unwrap() = Some(app_data.to_path_buf());
}
impl SettingsFile {
    fn path() -> Result<PathBuf, String> {
        FOLDER.lock().unwrap().as_ref().map(|f| f.join(SETTINGS_FILE)).ok_or_else(|| "App settings folder unavailable".into())
    }
}
impl Store for SettingsFile {
    fn read(&self) -> Result<Stored, String> {
        let path = Self::path()?;
        let bytes = match std::fs::read(&path) {
            Ok(bytes) => bytes,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(Stored::Absent { enrolled: false }),
            Err(e) => return Err(format!("App settings not readable: {e}")),
        };
        let value: Value = serde_json::from_slice(&bytes).map_err(|_| "stored App setting is corrupt".to_owned())?;
        match (value["format"] == SETTINGS_FORMAT, value["level"].as_str().and_then(parse)) {
            (true, Some(level)) => Ok(Stored::Level(level)),
            _ => Err("stored App setting is corrupt".into()),
        }
    }
    fn write(&self, level: AssuranceLevel) -> Result<(), String> {
        let path = Self::path()?;
        if let Some(parent) = path.parent() { crate::storage::ensure_directory(parent)?; }
        let temp = path.with_extension(format!("{}.tmp", crate::util::opaque_id("")?));
        let bytes = serde_json::to_vec_pretty(&json!({"format":SETTINGS_FORMAT,"level":level.label(),"writtenAt":crate::util::now_rfc3339()})).map_err(|e| e.to_string())?;
        std::fs::write(&temp, bytes).and_then(|()| std::fs::rename(&temp, &path)).map_err(|e| { let _ = std::fs::remove_file(&temp); format!("App setting not saved: {e}") })
    }
}

/// The keychain-held policy through the gated SEAL-C provider.
struct Keychain;
impl Store for Keychain {
    fn read(&self) -> Result<Stored, String> {
        use crate::capture_seal_keychain::{policy, PolicyOp, PolicyRead};
        match policy(PolicyOp::Read).ok_or("keychain provider not on this build")?? {
            PolicyRead::Stored(level) => parse(&level).map(Stored::Level).ok_or_else(|| "stored workflow approval policy is corrupt".into()),
            PolicyRead::Absent { enrolled } => Ok(Stored::Absent { enrolled }),
        }
    }
    fn write(&self, level: AssuranceLevel) -> Result<(), String> {
        use crate::capture_seal_keychain::{policy, PolicyOp};
        policy(PolicyOp::Write(level.label())).ok_or("keychain provider not on this build")?.map(|_| ())
    }
}
fn keychain_store() -> Option<Box<dyn Store>> {
    use crate::capture_seal_keychain::{policy, PolicyOp};
    // Presence of the provider is a fixed property of this build; its read
    // result is observed again by `Keychain::read`.
    policy(PolicyOp::Read).map(|_| Box::new(Keychain) as Box<dyn Store>)
}

/// Whether persistent verification (keychain protection) is available.
#[derive(Clone, Debug, PartialEq)]
enum Protection {
    /// No selected keychain provider in this build (unsigned or development).
    NotOnThisBuild,
    /// Provider present; the person has not set protection up.
    NotSetUp,
    SetUp,
    /// Protected, but the policy is missing, locked, corrupt or unreadable.
    Recovery(String),
}
struct State {
    protection: Protection,
    /// How the level was reached, for the view.
    source: String,
    note: Option<String>,
    epoch: u64,
}
pub(crate) struct Settings {
    policy: Policy,
    state: Mutex<Option<State>>,
    identity: String,
    keychain: Box<dyn Fn() -> Option<Box<dyn Store>> + Send + Sync>,
    file: Box<dyn Store>,
}
impl Default for Settings {
    fn default() -> Self {
        #[cfg(test)]
        {
            return Self::with_stores(|| None, Box::new(MemoryStore::default()));
        }
        #[allow(unreachable_code)]
        Self::with_stores(keychain_store, Box::new(SettingsFile))
    }
}
impl Settings {
    pub(crate) fn with_stores(keychain: impl Fn() -> Option<Box<dyn Store>> + Send + Sync + 'static, file: Box<dyn Store>) -> Self {
        Self {
            // Until resolved, nothing relaxes: the applied level starts robust.
            policy: Arc::new(Mutex::new(AssuranceLevel::Robust)),
            state: Mutex::new(None),
            identity: crate::util::opaque_id("assurance:").expect("App assurance identity"),
            keychain: Box::new(keychain),
            file,
        }
    }
    fn set(&self, level: AssuranceLevel) { *self.policy.lock().unwrap() = level; }
    /// Read the persisted choice. Never lowers on a failure; a first use with
    /// nothing stored takes the owner's default (robust where keychain
    /// protection works, otherwise relaxed) and records it.
    fn load(&self) -> State {
        match (self.keychain)() {
            Some(store) => match store.read() {
                Ok(Stored::Level(level)) => {
                    self.set(level);
                    return State { protection: Protection::SetUp, source: "Stored in your keychain".into(), note: None, epoch: 0 };
                }
                Ok(Stored::Absent { enrolled: true }) => {
                    self.set(AssuranceLevel::Robust);
                    return State { protection: Protection::Recovery("keychain protection is set up but its stored policy is missing".into()), source: "Protected policy unavailable; verified approval required until recovered".into(), note: None, epoch: 0 };
                }
                Err(cause) => {
                    self.set(AssuranceLevel::Robust);
                    return State { protection: Protection::Recovery(cause), source: "Protected policy unavailable; verified approval required until recovered".into(), note: None, epoch: 0 };
                }
                Ok(Stored::Absent { enrolled: false }) => self.load_file(Protection::NotSetUp),
            },
            None => self.load_file(Protection::NotOnThisBuild),
        }
    }
    fn load_file(&self, protection: Protection) -> State {
        match self.file.read() {
            Ok(Stored::Level(level)) => {
                self.set(level);
                State { protection, source: "Stored in this App's settings".into(), note: None, epoch: 0 }
            }
            Ok(Stored::Absent { .. }) => {
                // First use: keychain protection does not work here, so the
                // owner's default is relaxed. Recorded so later launches keep it.
                self.set(AssuranceLevel::Relaxed);
                let note = self.file.write(AssuranceLevel::Relaxed).err().map(|e| format!("First-use default not saved: {e}"));
                State { protection, source: "First-use default: keychain protection is not set up, so disk records are allowed".into(), note, epoch: 0 }
            }
            Err(cause) => {
                self.set(AssuranceLevel::Robust);
                State { protection, source: "Stored setting unreadable; verified approval required until you choose again".into(), note: Some(cause), epoch: 0 }
            }
        }
    }
    fn with_state<T>(&self, f: impl FnOnce(&mut State) -> T) -> T {
        let mut state = self.state.lock().unwrap();
        if state.is_none() { *state = Some(self.load()); }
        f(state.as_mut().unwrap())
    }
    /// The applied level, shared with library owners.
    pub(crate) fn policy(&self) -> Policy { self.with_state(|_| ()); self.policy.clone() }
    pub(crate) fn level(&self) -> AssuranceLevel { self.with_state(|_| ()); *self.policy.lock().unwrap() }
    pub(crate) fn protected(&self) -> bool { self.with_state(|s| matches!(s.protection, Protection::SetUp | Protection::Recovery(_))) }
    pub(crate) fn view(&self) -> Value {
        self.with_state(|s| {
            let level = *self.policy.lock().unwrap();
            let (state, available, detail) = match &s.protection {
                Protection::NotOnThisBuild => ("unavailable on this build", false, crate::capture_seal_keychain::enrollment_unavailable_reason().unwrap_or("This build has no keychain provider.").to_owned()),
                Protection::NotSetUp => ("not set up", false, "Keychain protection is not set up. Approvals cannot be verified across sessions.".to_owned()),
                Protection::SetUp => ("set up", true, "Approvals sealed with your keychain are verified across sessions.".to_owned()),
                Protection::Recovery(cause) => ("recovery required", false, format!("{cause}. Verified approval is required until recovered; nothing is relaxed automatically.")),
            };
            let storage = if matches!(s.protection, Protection::SetUp | Protection::Recovery(_)) {
                "Stored in your keychain. Choosing \"Allow disk records\" needs your native confirmation."
            } else {
                "Stored in this App's settings file, outside any project. Until keychain protection is set up, an agent able to write that file could change this setting."
            };
            json!({"level":level.label(),"policy":policy_name(level),"source":s.source,"note":s.note,
                "verification":{"state":state,"available":available,"detail":detail},
                "storage":storage,
                "robustWithoutVerification":"Session confirmation required; persistent verification unavailable",
                "lowering":"Choosing \"Allow disk records\" needs your native confirmation; no command or project file lowers it.",
                "protect":{"offered":matches!(s.protection, Protection::NotSetUp) && crate::capture_seal_keychain::enrollment_unavailable_reason().is_none(),
                    "reason":match &s.protection { Protection::SetUp => Some("Keychain protection is set up.".to_owned()), Protection::Recovery(_) => Some("Recover the protected policy first.".to_owned()), _ => crate::capture_seal_keychain::enrollment_unavailable_reason().map(str::to_owned) }}})
        })
    }
    /// "Require verified approval": raising needs no act. Under recovery the
    /// protection state is read again first; the keychain is written only
    /// where protection (the seal key) exists, so restoring a policy never
    /// reports protection that enrollment did not set up.
    pub(crate) fn require_verified(&self) -> Result<(), String> {
        let mut state = self.state.lock().unwrap();
        if state.is_none() { *state = Some(self.load()); }
        let s = state.as_mut().unwrap();
        let epoch = s.epoch + 1;
        if matches!(s.protection, Protection::Recovery(_)) {
            *s = self.load();
        }
        self.set(AssuranceLevel::Robust);
        s.epoch = epoch;
        let written = match &s.protection {
            Protection::SetUp | Protection::Recovery(_) => {
                (self.keychain)().ok_or("keychain provider not on this build".to_owned()).and_then(|store| store.write(AssuranceLevel::Robust))
            }
            _ => self.file.write(AssuranceLevel::Robust),
        };
        match written {
            Ok(()) => {
                let protected = matches!(s.protection, Protection::SetUp | Protection::Recovery(_));
                if protected {
                    // Read back what the keychain now holds; success only if
                    // the restoration actually reads back.
                    *s = self.load();
                    s.epoch = epoch;
                    if let Protection::Recovery(cause) = &s.protection {
                        let cause = cause.clone();
                        self.set(AssuranceLevel::Robust);
                        return Err(format!("Verified approval applies now, but the protected policy still needs recovery: {cause}"));
                    }
                } else {
                    s.source = "Stored in this App's settings".into();
                    s.note = None;
                }
                self.set(AssuranceLevel::Robust);
                Ok(())
            }
            Err(cause) => { s.note = Some(format!("Not saved: {cause}")); Err(format!("Verified approval applies now but was not saved: {cause}")) }
        }
    }
    pub(crate) fn lowering_context(&self) -> (String, u64, bool) {
        self.with_state(|s| (self.identity.clone(), s.epoch, matches!(s.protection, Protection::SetUp | Protection::Recovery(_))))
    }
    /// "Allow disk records": only with the opaque native act for this epoch.
    pub(crate) fn lower(&self, event: crate::act_control::ConfirmedAssuranceAct) -> Result<(), String> {
        self.with_state(|s| {
            if !event.matches(&self.identity, s.epoch) {
                return Err("The approval setting changed while the native question was open; nothing lowered".into());
            }
            let written = match &s.protection {
                Protection::Recovery(cause) => return Err(format!("Recover the protected policy first ({cause}); nothing lowered")),
                Protection::SetUp => (self.keychain)().ok_or("keychain provider not on this build".to_owned()).and_then(|store| store.write(AssuranceLevel::Relaxed)),
                _ => self.file.write(AssuranceLevel::Relaxed),
            };
            written.map_err(|cause| format!("Nothing lowered: {cause}"))?;
            self.set(AssuranceLevel::Relaxed);
            s.epoch += 1;
            s.note = None;
            Ok(())
        })
    }
    /// "Check again" for a protected policy that needed recovery. Re-reading
    /// can only apply a stored choice; a failure still requires verification.
    pub(crate) fn recheck(&self) {
        let mut state = self.state.lock().unwrap();
        let epoch = state.as_ref().map_or(0, |s| s.epoch) + 1;
        if state.as_ref().is_none_or(|s| matches!(s.protection, Protection::Recovery(_))) {
            let mut fresh = self.load();
            fresh.epoch = epoch;
            *state = Some(fresh);
        }
    }
    /// After the person's keychain enrollment act: store "Require verified
    /// approval" in the keychain (the default where keychain protection works).
    pub(crate) fn after_enrollment(&self) -> Result<(), String> {
        let mut state = self.state.lock().unwrap();
        let written = (self.keychain)().ok_or("keychain provider not on this build".to_owned()).and_then(|store| store.write(AssuranceLevel::Robust));
        self.set(AssuranceLevel::Robust);
        let epoch = state.as_ref().map_or(0, |s| s.epoch) + 1;
        let mut fresh = self.load();
        fresh.epoch = epoch;
        *state = Some(fresh);
        written
    }
}

/// In-memory store for tests and the test default.
#[derive(Default)]
pub(crate) struct MemoryStore {
    pub(crate) value: Mutex<Option<Result<Stored, String>>>,
    pub(crate) write_error: Mutex<Option<String>>,
    pub(crate) writes: Mutex<Vec<AssuranceLevel>>,
}
impl Store for MemoryStore {
    fn read(&self) -> Result<Stored, String> {
        match &*self.value.lock().unwrap() {
            None => Ok(Stored::Absent { enrolled: false }),
            Some(Ok(Stored::Level(level))) => Ok(Stored::Level(*level)),
            Some(Ok(Stored::Absent { enrolled })) => Ok(Stored::Absent { enrolled: *enrolled }),
            Some(Err(cause)) => Err(cause.clone()),
        }
    }
    fn write(&self, level: AssuranceLevel) -> Result<(), String> {
        if let Some(cause) = self.write_error.lock().unwrap().clone() { return Err(cause); }
        self.writes.lock().unwrap().push(level);
        *self.value.lock().unwrap() = Some(Ok(Stored::Level(level)));
        Ok(())
    }
}
impl<T: Store + ?Sized> Store for Arc<T> {
    fn read(&self) -> Result<Stored, String> { (**self).read() }
    fn write(&self, level: AssuranceLevel) -> Result<(), String> { (**self).write(level) }
}

#[cfg(test)]
#[path = "workflow_assurance_tests.rs"]
mod tests;
