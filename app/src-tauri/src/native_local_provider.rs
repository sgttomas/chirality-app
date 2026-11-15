//! The dedicated local home. Its nonsecret configuration is App-owned and generated from the
//! person's local model settings; only Codex writes auth.json. This module never reads a
//! credential, opens auth.json, retries a credential frame or accepts one from IPC.
use crate::{
    act_control::native_statement as ns,
    home_resources::{HomeClass, OwnedHomePlan},
    hosting::HostConfig,
    runtime_session::HomeSession,
};
use raw_window_handle::{
    DisplayHandle, HandleError, HasDisplayHandle, HasWindowHandle, WindowHandle,
};
use serde_json::{json, Value};
use std::{
    io::{Read, Write},
    path::Path,
    sync::{mpsc, Mutex},
    time::Duration,
};
use tauri_plugin_dialog::{DialogExt, MessageDialogKind, MessageDialogResult};

pub(crate) const PROVIDER: &str = "chirality-omlx";
/// The address offered until the person sets one. An offer only; never written unasked.
pub(crate) const OFFERED_ENDPOINT: &str = "http://127.0.0.1:8000/v1";
/// The model an earlier build wrote. Such a file is read as these values through the canonical form.
#[cfg(test)]
const LEGACY_MODEL: &str = "mlx-community/Qwen3.6-35B-A3B-8bit";
/// Fixture values only: production code compares with the settings in force.
#[cfg(test)]
pub(crate) const ENDPOINT: &str = OFFERED_ENDPOINT;
#[cfg(test)]
pub(crate) const MODEL: &str = LEGACY_MODEL;
pub(crate) const ENTRY: &str = "local-provider-keyed";
pub(crate) const LIMIT: &str =
    "Local oMLX source unavailable; no fallback or automatic credential retry";
pub(crate) const UNSET: &str = "Local model settings are not set; set the server address and model name first. Nothing was prepared.";
/// True both when the settings changed and when a change was begun and did not complete, and when
/// the file was changed outside the App after the connection was prepared.
pub(crate) const RELAUNCH: &str = "The local model settings changed, or a change to them was begun, after the local connection was prepared in this session; quit and reopen the App to use the local connection. It is unavailable until then.";
pub(crate) const EARLIER: &str =
    "This conversation was started under earlier local model settings; it is not continued.";
/// The refusal once this App session has seen a key and the App's record of its address is gone
/// together with the key file: Codex may still hold the key. It names no address.
pub(crate) const KEY_ADDRESS_LOST: &str = "A key was saved or entered for the local model home in this App session, and the App no longer has its record of the server address it was entered for, so nothing more is sent there. Quit and reopen the App, then prepare the local connection again.";
/// The refusal for a key file with no record. It names no address: the App cannot establish one.
pub(crate) const KEY_ADDRESS_UNRECORDED: &str = "A key is saved in the dedicated local home, but the App has no record of the server address it was entered for, so it will not use that key. Nothing was started.";
/// The settings_view reason token for a key-address mismatch.
const KEY_ADDRESS_MISMATCH_REASON: &str = "key-address-mismatch";
const RECORD_UNWRITTEN: &str = "The App could not record the server address the key is entered for; the key field was not opened and nothing was sent.";
const RECORD_NOT_REMOVED: &str = "Codex removed the saved key, but the App could not remove its record of the server address the key was entered for; the local model settings were not changed.";
/// As RECORD_NOT_REMOVED, where no key file was present before Codex's sign-out.
const RECORD_NOT_REMOVED_NO_KEY: &str = "Codex reports no saved key, but the App could not remove its record of the server address a key was entered for; the local model settings were not changed.";
/// App-owned, beside config.toml: the one address the saved key was entered for, and a newline.
const KEY_ADDRESS: &str = "key-address";
pub(crate) const KEY_ENTRY_BEGUN: &str = "Key entry was used in this Codex session, and Codex may still be saving that key. Restart Codex for the local model home, then change the address. The local model settings were not changed.";
pub(crate) const PREPARE_FIRST: &str = "Prepare the local connection first, so that Codex can remove the saved key; the local model settings were not changed.";
/// The save waited `ACCOUNT_WAIT` for the frame writer lock and did not get it, so the binding was
/// not marked and nothing was changed. What that shows is that the lock was not free; its holder
/// may have been writing or waiting on something before its write.
pub(crate) const WRITE_IN_PROGRESS: &str = "The App could not get its turn to write to Codex for the local model home within 20 seconds, so the local model settings were not changed. Try again.";
pub(crate) const WRITE_IN_PROGRESS_KEY_REMOVED: &str = "Codex removed the saved key, but the App could not get its turn to write to Codex for the local model home within 20 seconds, so the local model settings were not changed. Try again.";
pub(crate) const WRITE_IN_PROGRESS_NO_KEY: &str = "Codex reports no saved key, but the App could not get its turn to write to Codex for the local model home within 20 seconds, so the local model settings were not changed. Try again.";
const SIGN_OUT_UNCONFIRMED: &str = "Codex's removal of the saved key could not be confirmed; the local model settings were not changed. Prepare the local connection and try again.";
const ADDRESS_RULE: &str = "The server address must be http:// or https:// on 127.0.0.1 or [::1], with an optional port from 1 to 65535 and a path of letters, digits and . _ ~ / - only; nothing was saved.";
const MODEL_RULE: &str = "The model name must be 1 to 128 characters of letters, digits and . _ : / @ + - only; nothing was saved.";
const CHANGED: &str =
    "The local model settings changed while you were deciding; nothing was saved. Review them again.";
const UNCONFIRMED: &str = "The new local model settings were written but could not be confirmed; read the settings again before relying on them.";
pub(crate) const SAVE_ACTION: &str = "Save local model settings";
const LEAVE: &str = "Leave settings unchanged";
const TITLE: &str = "Local model settings";
const ACCOUNT_WAIT: Duration = Duration::from_secs(20);

/// The person's nonsecret local model settings: the server address and the model name. Constructed
/// only through validation; the key is never one of them. Provider id, interface and the key
/// requirement are fixed (chirality-omlx, Responses, a key always required).
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct LocalSettings {
    endpoint: String,
    model: String,
}
impl LocalSettings {
    /// Fail closed: nothing is trimmed or corrected; an invalid value is refused.
    pub(crate) fn new(endpoint: &str, model: &str) -> Result<Self, String> {
        if !valid_endpoint(endpoint) {
            return Err(ADDRESS_RULE.into());
        }
        if !valid_model(model) {
            return Err(MODEL_RULE.into());
        }
        Ok(Self {
            endpoint: endpoint.into(),
            model: model.into(),
        })
    }
    pub(crate) fn endpoint(&self) -> &str {
        &self.endpoint
    }
    pub(crate) fn model(&self) -> &str {
        &self.model
    }
    pub(crate) fn json(&self) -> Value {
        json!({"endpoint":self.endpoint,"model":self.model})
    }
    /// What a home prepared by an earlier build holds.
    #[cfg(test)]
    pub(crate) fn legacy() -> Self {
        Self {
            endpoint: OFFERED_ENDPOINT.into(),
            model: LEGACY_MODEL.into(),
        }
    }
}
/// Loopback only, by exact literal host. Every accepted byte is safe inside a TOML basic string
/// and a session-flag string.
fn valid_endpoint(text: &str) -> bool {
    if text.len() > 2048 {
        return false;
    }
    let Some(rest) = text
        .strip_prefix("http://")
        .or_else(|| text.strip_prefix("https://"))
    else {
        return false;
    };
    let Some(rest) = rest
        .strip_prefix("127.0.0.1")
        .or_else(|| rest.strip_prefix("[::1]"))
    else {
        return false;
    };
    let (port, path) = rest.split_at(rest.find('/').unwrap_or(rest.len()));
    if !port.is_empty() {
        let Some(digits) = port.strip_prefix(':') else {
            return false;
        };
        if digits.is_empty()
            || digits.len() > 5
            || digits.starts_with('0')
            || !digits.bytes().all(|b| b.is_ascii_digit())
            || !digits.parse::<u32>().is_ok_and(|p| (1..=65535).contains(&p))
        {
            return false;
        }
    }
    if !path
        .bytes()
        .all(|b| b.is_ascii_alphanumeric() || b"._~/-".contains(&b))
    {
        return false;
    }
    // Defence in depth: the standard parser must see the same loopback host and no extras.
    tauri::Url::parse(text).is_ok_and(|url| {
        matches!(url.host_str(), Some("127.0.0.1" | "[::1]"))
            && url.username().is_empty()
            && url.password().is_none()
            && url.query().is_none()
            && url.fragment().is_none()
    })
}
fn valid_model(text: &str) -> bool {
    (1..=128).contains(&text.len())
        && text
            .bytes()
            .all(|b| b.is_ascii_alphanumeric() || b"._:/@+-".contains(&b))
}
/// The one canonical form of the home's config.toml. For the legacy settings it is byte for byte
/// the file earlier builds wrote, so such a home keeps working unchanged.
pub(crate) fn canonical(s: &LocalSettings) -> String {
    format!("model_provider = \"chirality-omlx\"\nmodel = \"{}\"\ncli_auth_credentials_store = \"file\"\n[features]\nplugins = false\napi_key_model_discovery = false\n[model_providers.chirality-omlx]\nname = \"oMLX\"\nbase_url = \"{}\"\nwire_api = \"responses\"\nrequires_openai_auth = true\n", s.model, s.endpoint)
}
/// Exact reader for the canonical form: read three values, regenerate, require byte equality.
fn parse(bytes: &[u8]) -> Option<LocalSettings> {
    let text = std::str::from_utf8(bytes).ok()?;
    let lines: Vec<&str> = text.split('\n').collect();
    if lines.len() != 12 {
        return None;
    }
    let quoted = |line: &str, key: &str| {
        line.strip_prefix(key)?
            .strip_prefix(" = \"")?
            .strip_suffix('"')
            .map(str::to_owned)
    };
    let model = quoted(lines[1], "model")?;
    let endpoint = quoted(lines[8], "base_url")?;
    let settings = LocalSettings::new(&endpoint, &model).ok()?;
    (canonical(&settings).as_bytes() == bytes).then_some(settings)
}
/// The session flags for one settings value: whole-provider replacement at highest config
/// precedence prevents project/default routing drift. No inherited account override is copied.
pub(crate) fn session_flags(s: &LocalSettings) -> Vec<String> {
    vec![
        "analytics.enabled=false".into(),
        "features.plugins=false".into(),
        // Session flags merge into lower layers; a foreign catalogue URL must never receive the home key.
        "features.api_key_model_discovery=false".into(),
        "cli_auth_credentials_store=\"file\"".into(),
        format!("model_provider=\"{PROVIDER}\""),
        format!("model=\"{}\"", s.model),
        format!("model_providers.{PROVIDER}={{name=\"oMLX\",base_url=\"{}\",wire_api=\"responses\",requires_openai_auth=true}}", s.endpoint),
    ]
}

/// Native, nonserializable once-per-generation entry state. An unknown result is never retried.
#[derive(Default)]
pub(crate) struct CredentialEntry {
    attempted: Mutex<Vec<Value>>,
}
impl CredentialEntry {
    fn begin(&self, generation: &Value) -> Result<(), String> {
        let mut attempts = self.attempted.try_lock().map_err(|_| LIMIT)?;
        if attempts.contains(generation) {
            return Err(LIMIT.into());
        }
        attempts.push(generation.clone());
        Ok(())
    }
    /// Whether a key entry was begun in this Codex session. A state that cannot be read counts
    /// as begun.
    pub(crate) fn begun(&self, generation: &Value) -> bool {
        self.attempted
            .try_lock()
            .map_or(true, |attempts| attempts.contains(generation))
    }
    /// Whether an attempt for this generation can still begin (and begins it).
    #[cfg(test)]
    pub(crate) fn begin_for_test(&self, generation: &Value) -> bool {
        self.begin(generation).is_ok()
    }
}
fn private_metadata(path: &Path, directory: bool) -> Result<(), String> {
    let m = std::fs::symlink_metadata(path).map_err(|_| LIMIT)?;
    if m.file_type().is_symlink() || (directory && !m.is_dir()) || (!directory && !m.is_file()) {
        return Err(LIMIT.into());
    }
    #[cfg(unix)]
    {
        use std::os::unix::fs::MetadataExt;
        if m.uid() != unsafe { libc::geteuid() }
            || m.mode() & 0o077 != 0
            || (!directory && m.nlink() != 1)
        {
            return Err(LIMIT.into());
        }
    }
    #[cfg(not(unix))]
    {
        return Err(LIMIT.into());
    }
    Ok(())
}
/// Present or unestablished, never opened: only absence is absence.
fn absent(path: &Path) -> bool {
    matches!(std::fs::symlink_metadata(path), Err(e) if e.kind() == std::io::ErrorKind::NotFound)
}
/// The home's own conditions, apart from config.toml's contents. Credential slots are checked by
/// metadata only; their contents are never parsed or copied.
fn check_home(plan: &OwnedHomePlan) -> Result<(), String> {
    if plan.class() != HomeClass::LocalProvider {
        return Err(LIMIT.into());
    }
    crate::storage::check_path(plan.native_path()).map_err(|_| LIMIT)?;
    private_metadata(plan.native_path(), true)?;
    for slot in ["auth.json", "auth.lock"] {
        let path = plan.native_path().join(slot);
        match std::fs::symlink_metadata(&path) {
            Ok(_) => private_metadata(&path, false)?,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
            Err(_) => return Err(LIMIT.into()),
        }
    }
    // No account configuration, global guidance or skill link can enter this home.
    for slot in ["AGENTS.md", "skills"] {
        match std::fs::symlink_metadata(plan.native_path().join(slot)) {
            Ok(m)
                if m.file_type().is_symlink()
                    || (slot == "skills" && !m.is_dir())
                    || (slot == "AGENTS.md" && !m.is_file()) =>
            {
                return Err(LIMIT.into())
            }
            Ok(_) => {}
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
            Err(_) => return Err(LIMIT.into()),
        }
    }
    Ok(())
}
fn read_config(plan: &OwnedHomePlan) -> Result<LocalSettings, String> {
    let path = plan.native_path().join("config.toml");
    private_metadata(&path, false)?;
    let mut bytes = Vec::new();
    std::fs::File::open(&path)
        .map_err(|_| LIMIT)?
        .take(8192)
        .read_to_end(&mut bytes)
        .map_err(|_| LIMIT)?;
    parse(&bytes).ok_or_else(|| LIMIT.to_owned())
}
/// The one byte form of the key-address record.
fn record_bytes(address: &str) -> String {
    format!("{address}\n")
}
/// Strict reader of the key-address record: absent, or private and exactly one validated address
/// and a newline. Anything else refuses; nothing is repaired.
fn read_key_address(plan: &OwnedHomePlan) -> Result<Option<String>, String> {
    let path = plan.native_path().join(KEY_ADDRESS);
    match std::fs::symlink_metadata(&path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),
        Err(_) => return Err(LIMIT.into()),
        Ok(_) => private_metadata(&path, false)?,
    }
    let mut options = std::fs::OpenOptions::new();
    options.read(true);
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        options.custom_flags(libc::O_NOFOLLOW);
    }
    let mut bytes = Vec::new();
    options
        .open(&path)
        .map_err(|_| LIMIT)?
        .take(4096)
        .read_to_end(&mut bytes)
        .map_err(|_| LIMIT)?;
    let address = std::str::from_utf8(&bytes)
        .ok()
        .and_then(|text| text.strip_suffix('\n'))
        .filter(|address| valid_endpoint(address))
        .ok_or(LIMIT)?;
    if record_bytes(address).as_bytes() != bytes.as_slice() {
        return Err(LIMIT.into());
    }
    Ok(Some(address.to_owned()))
}
/// Records the address a key is about to be entered for: a private temporary file, written and
/// synced, renamed over the record, the directory synced, then read back strictly. Holds the
/// address only; never a key or anything derived from one.
fn write_key_address(plan: &OwnedHomePlan, address: &str) -> Result<(), String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::write_key_address");
    if !valid_endpoint(address) {
        return Err(RECORD_UNWRITTEN.into());
    }
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        let home = plan.native_path();
        let temporary = home.join(format!(
            ".{}.tmp",
            crate::util::opaque_id("key-address-").map_err(|_| RECORD_UNWRITTEN)?
        ));
        let staged = (|| -> Result<(), String> {
            let mut file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .mode(0o600)
                .custom_flags(libc::O_NOFOLLOW)
                .open(&temporary)
                .map_err(|_| RECORD_UNWRITTEN)?;
            file.write_all(record_bytes(address).as_bytes())
                .map_err(|_| RECORD_UNWRITTEN)?;
            file.sync_all().map_err(|_| RECORD_UNWRITTEN)?;
            drop(file);
            private_metadata(&temporary, false).map_err(|_| RECORD_UNWRITTEN)?;
            std::fs::rename(&temporary, home.join(KEY_ADDRESS)).map_err(|_| RECORD_UNWRITTEN)?;
            Ok(())
        })();
        if staged.is_err() {
            let _ = std::fs::remove_file(&temporary);
        }
        staged?;
        crate::storage::sync_dir(home).map_err(|_| RECORD_UNWRITTEN)?;
    }
    #[cfg(not(unix))]
    {
        let _ = plan;
        return Err(RECORD_UNWRITTEN.into());
    }
    if read_key_address(plan).ok().flatten().as_deref() != Some(address) {
        return Err(RECORD_UNWRITTEN.into());
    }
    Ok(())
}
/// Removes the record after Codex itself reported no account. Removal is confirmed by absence.
fn remove_key_address(plan: &OwnedHomePlan) -> Result<(), String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::remove_key_address");
    let path = plan.native_path().join(KEY_ADDRESS);
    match std::fs::remove_file(&path) {
        Ok(()) => {}
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
        Err(_) => return Err(RECORD_NOT_REMOVED.into()),
    }
    crate::storage::sync_dir(plan.native_path()).map_err(|_| RECORD_NOT_REMOVED)?;
    if !absent(&path) {
        return Err(RECORD_NOT_REMOVED.into());
    }
    Ok(())
}
/// A saved key is used only at the address it was entered for, as the App's own record states.
///
/// The record is always valid or absent. While auth.json is absent (by metadata; a slot that
/// cannot be established absent counts as present) there is no key and the record does not
/// decide anything. With a key file, the record must name exactly the address set.
///
/// The record is written and read back before the native key field opens (submit), so a key file
/// this build helped create always has one. A key file without a record has no address the App
/// can establish, and refuses at every address: there is no exception.
fn key_address_state(plan: &OwnedHomePlan, settings: &LocalSettings) -> Result<Option<KeyMismatch>, String> {
    key_address_state_seen(plan, settings, false).map(|(mismatch, _)| mismatch)
}
/// As `key_address_state`, for a bound session. `key_seen`: this session has seen a key (a key
/// file found present by an earlier check, or a key entry begun or acknowledged). Codex may still
/// hold that key in memory after its file is gone, so once seen the record must be present and name
/// the address set whether or not the key file is still there. Also returns whether the key file
/// is present now (metadata only), so the caller can remember it.
fn key_address_state_seen(plan: &OwnedHomePlan, settings: &LocalSettings, key_seen: bool) -> Result<(Option<KeyMismatch>, bool), String> {
    let record = read_key_address(plan)?;
    let present = !absent(&plan.native_path().join("auth.json"));
    if !present && !key_seen {
        return Ok((None, false));
    }
    Ok((match record {
        Some(address) if address == settings.endpoint => None,
        recorded => Some(KeyMismatch {
            set: settings.endpoint.clone(),
            recorded,
            file_present: present,
        }),
    }, present))
}
fn key_address_check(plan: &OwnedHomePlan, settings: &LocalSettings) -> Result<(), String> {
    match key_address_state(plan, settings)? {
        None => Ok(()),
        Some(mismatch) => Err(mismatch.sentence()),
    }
}
/// A saved key whose address is not the one set. Both values are validated, nonsecret addresses;
/// `recorded` is None for a key file without a record.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct KeyMismatch {
    set: String,
    recorded: Option<String>,
    /// Whether the key file is present; false only for a key this session has seen whose file is gone.
    file_present: bool,
}
impl KeyMismatch {
    pub(crate) fn sentence(&self) -> String {
        match &self.recorded {
            Some(recorded) => format!("The local model server address now set is {}, and the saved key was entered for {recorded}. The App will not use that key with another address. Set the address back to {recorded}.", self.set),
            None if self.file_present => KEY_ADDRESS_UNRECORDED.into(),
            None => KEY_ADDRESS_LOST.into(),
        }
    }
}
/// Whether Codex's key file is positively present and private (metadata only; never opened).
fn key_file_present(plan: &OwnedHomePlan) -> bool {
    let path = plan.native_path().join("auth.json");
    std::fs::symlink_metadata(&path).is_ok() && private_metadata(&path, false).is_ok()
}
/// The file's settings with every home condition checked, apart from the key's address: only for
/// the compare-and-replace of a save, whose caller has established that condition itself.
fn settings_file(plan: &OwnedHomePlan) -> Result<LocalSettings, String> {
    check_home(plan)?;
    read_config(plan)
}
/// The settings the home's file holds now, with every home condition checked, including that a
/// saved key was entered for the address set. Every binding and use reads through here.
pub(crate) fn current(plan: &OwnedHomePlan) -> Result<LocalSettings, String> {
    let settings = settings_file(plan)?;
    key_address_check(plan, &settings)?;
    Ok(settings)
}
/// Every bound operation: the file must still hold exactly the settings in force for this
/// Codex process. A file changed after binding refuses until the App is reopened.
pub(crate) fn check(plan: &OwnedHomePlan, in_force: &LocalSettings) -> Result<(), String> {
    check_seen(plan, in_force, false).map(|_| ())
}
/// `check` for a bound session that may have seen a key (see `key_address_state_seen`). Returns
/// whether the key file is present now, for the session to remember.
pub(crate) fn check_seen(plan: &OwnedHomePlan, in_force: &LocalSettings, key_seen: bool) -> Result<bool, String> {
    let settings = settings_file(plan)?;
    let (mismatch, present) = key_address_state_seen(plan, &settings, key_seen)?;
    if let Some(mismatch) = mismatch {
        return Err(mismatch.sentence());
    }
    if settings != *in_force {
        return Err(RELAUNCH.into());
    }
    Ok(present)
}
/// The settings as stored, without starting anything: None when no settings file exists yet.
pub(crate) fn stored(plan: &OwnedHomePlan) -> Result<Option<LocalSettings>, String> {
    if plan.class() != HomeClass::LocalProvider {
        return Err(LIMIT.into());
    }
    crate::storage::check_path(plan.native_path()).map_err(|_| LIMIT)?;
    if absent(plan.native_path()) {
        return Ok(None);
    }
    private_metadata(plan.native_path(), true)?;
    if absent(&plan.native_path().join("config.toml")) {
        return Ok(None);
    }
    read_config(plan).map(Some)
}
/// The page's reading: the stored settings and, when a saved key was entered for another
/// address, that mismatch.
pub(crate) struct Reading {
    settings: Option<LocalSettings>,
    mismatch: Option<KeyMismatch>,
}
pub(crate) fn read(plan: &OwnedHomePlan) -> Result<Reading, String> {
    let settings = stored(plan)?;
    let mismatch = match &settings {
        Some(settings) => key_address_state(plan, settings)?,
        None => None,
    };
    Ok(Reading { settings, mismatch })
}
/// Prepare an already-set home for binding. Never writes settings or defaults.
pub(crate) fn prepare(plan: &OwnedHomePlan) -> Result<LocalSettings, String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::prepare");
    if stored(plan)?.is_none() {
        return Err(UNSET.into());
    }
    check_home(plan)?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        match std::fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(plan.native_path().join("auth.lock"))
        {
            Ok(file) => {
                file.sync_all().map_err(|_| LIMIT)?;
                crate::storage::sync_dir(plan.native_path())?;
            }
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(_) => return Err(LIMIT.into()),
        }
    }
    current(plan)
}
/// First settings: create the home, then put a complete, private, synced config.toml in place
/// only where none exists. The file is staged in a private temporary file in the same folder and
/// renamed with RENAME_EXCL (one atomic rename that fails with EEXIST if config.toml exists), so
/// config.toml is never seen partly written; the folder is synced and the file read back strictly.
/// A failure before the rename leaves neither config.toml nor the temporary file.
fn write_initial(plan: &OwnedHomePlan, settings: &LocalSettings) -> Result<(), String> {
    write_initial_staged(plan, settings, |_| Ok(()))
}
/// `staged` runs after the temporary file is complete and synced, before it is put in place: the
/// tests' point of failure.
fn write_initial_staged(
    plan: &OwnedHomePlan,
    settings: &LocalSettings,
    staged: impl FnOnce(&Path) -> Result<(), String>,
) -> Result<(), String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::write_initial_staged");
    if plan.class() != HomeClass::LocalProvider {
        return Err(LIMIT.into());
    }
    crate::storage::check_path(plan.native_path()).map_err(|_| LIMIT)?;
    #[cfg(target_os = "macos")]
    {
        use std::os::unix::fs::{DirBuilderExt, OpenOptionsExt};
        let mut builder = std::fs::DirBuilder::new();
        builder.mode(0o700);
        match builder.create(plan.native_path()) {
            Ok(()) => crate::storage::sync_dir(plan.native_path().parent().ok_or(LIMIT)?)?,
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(_) => return Err(LIMIT.into()),
        }
        private_metadata(plan.native_path(), true)?;
        // A credential slot without settings is not a first time.
        if !absent(&plan.native_path().join("auth.json")) {
            return Err(LIMIT.into());
        }
        let home = plan.native_path();
        let target = home.join("config.toml");
        if !absent(&target) {
            return Err(CHANGED.into());
        }
        let temporary = home.join(format!(".{}.tmp", crate::util::opaque_id("config-")?));
        let placed = (|| -> Result<(), String> {
            let mut file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .mode(0o600)
                .custom_flags(libc::O_NOFOLLOW)
                .open(&temporary)
                .map_err(|_| UNCONFIRMED)?;
            file.write_all(canonical(settings).as_bytes())
                .map_err(|_| UNCONFIRMED)?;
            file.sync_all().map_err(|_| UNCONFIRMED)?;
            drop(file);
            private_metadata(&temporary, false).map_err(|_| UNCONFIRMED)?;
            staged(&temporary)?;
            rename_exclusive(&temporary, &target)
        })();
        if placed.is_err() {
            let _ = std::fs::remove_file(&temporary);
            let _ = crate::storage::sync_dir(home);
        }
        placed?;
        crate::storage::sync_dir(home).map_err(|_| UNCONFIRMED)?;
    }
    #[cfg(not(target_os = "macos"))]
    {
        let _ = (settings, staged);
        return Err(LIMIT.into());
    }
    if read_config(plan).ok().as_ref() != Some(settings) {
        return Err(UNCONFIRMED.into());
    }
    Ok(())
}
/// rename(2) with RENAME_EXCL: atomic, and EEXIST when `to` exists (an existing target is never
/// replaced). A file system without RENAME_EXCL refuses (ENOTSUP), which also fails closed.
#[cfg(target_os = "macos")]
fn rename_exclusive(from: &Path, to: &Path) -> Result<(), String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::rename_exclusive");
    use std::os::unix::ffi::OsStrExt;
    let from = std::ffi::CString::new(from.as_os_str().as_bytes()).map_err(|_| LIMIT)?;
    let to = std::ffi::CString::new(to.as_os_str().as_bytes()).map_err(|_| LIMIT)?;
    if unsafe { libc::renamex_np(from.as_ptr(), to.as_ptr(), libc::RENAME_EXCL) } == 0 {
        return Ok(());
    }
    Err(match std::io::Error::last_os_error().raw_os_error() {
        Some(libc::EEXIST) => CHANGED.into(),
        _ => UNCONFIRMED.into(),
    })
}
/// Changed settings: atomic replacement in the same directory. Nothing else in the home is touched.
fn replace(plan: &OwnedHomePlan, before: &LocalSettings, after: &LocalSettings) -> Result<(), String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::replace");
    if settings_file(plan)? != *before {
        return Err(CHANGED.into());
    }
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        let home = plan.native_path();
        let temporary = home.join(format!(".{}.tmp", crate::util::opaque_id("config-")?));
        let staged = (|| -> Result<(), String> {
            let mut file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .mode(0o600)
                .custom_flags(libc::O_NOFOLLOW)
                .open(&temporary)
                .map_err(|_| LIMIT)?;
            file.write_all(canonical(after).as_bytes()).map_err(|_| LIMIT)?;
            file.sync_all().map_err(|_| LIMIT)?;
            drop(file);
            private_metadata(&temporary, false)?;
            if settings_file(plan)? != *before {
                return Err(CHANGED.into());
            }
            std::fs::rename(&temporary, home.join("config.toml")).map_err(|_| LIMIT)?;
            Ok(())
        })();
        if staged.is_err() {
            let _ = std::fs::remove_file(&temporary);
        }
        staged?;
        crate::storage::sync_dir(home).map_err(|_| UNCONFIRMED)?;
    }
    #[cfg(not(unix))]
    {
        let _ = after;
        return Err(LIMIT.into());
    }
    if settings_file(plan).ok().as_ref() != Some(after) {
        return Err(UNCONFIRMED.into());
    }
    Ok(())
}
/// The session flags for the settings the home's file holds now.
pub(crate) fn config(base: &HostConfig, plan: &OwnedHomePlan) -> Result<HostConfig, String> {
    let settings = current(plan)?;
    require_no_admin_layers()?;
    let mut config = base.clone();
    config.codex_home = plan.native_path().into();
    config.session_flags = session_flags(&settings);
    config.process_lock = Some(plan.native_path().join(PROCESS_LOCK));
    Ok(config)
}
/// App-owned lock file in every Codex home the App starts Codex on. A Codex the App starts there
/// is given the locked descriptor, so the lock is held while that Codex, or anything it started
/// that kept the descriptor, keeps it open. Not auth.lock, not Codex's.
pub(crate) const PROCESS_LOCK: &str = "chirality-codex-process.lock";
/// What a held lock establishes is only that something holds it: the sentence names what may,
/// and asserts neither which nor for how long.
pub(crate) const EARLIER_PROCESS: &str = "The App's lock for the local model home is held, so Codex was not started there. A Codex process started earlier for that home, a program it started, or another copy of the App may hold it. Try again in a minute. If it stays held, whatever holds it has to let go of it or end before Codex can start there; the App cannot tell which program it is.";
/// The refusal when the App cannot open or lock its lock file at all.
pub(crate) const PROCESS_LOCK_UNAVAILABLE: &str = "The App could not take its lock for the local model home, so Codex was not started there.";
/// What trying the App's process lock of a home found, when it was not taken.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum ProcessLockRefusal {
    /// Another open file description holds it.
    Held,
    /// A link, a file not private to this user, a hard-linked file or any other failure: the lock
    /// could not be tried, which never reads as free.
    Unavailable,
}
/// The checks and the exclusive, non-waiting flock on the opened lock file.
#[cfg(unix)]
fn lock_opened(file: std::fs::File) -> Result<std::fs::File, ProcessLockRefusal> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::lock_opened");
    use std::os::fd::AsRawFd;
    use std::os::unix::fs::MetadataExt;
    let m = file.metadata().map_err(|_| ProcessLockRefusal::Unavailable)?;
    if !m.is_file() || m.uid() != unsafe { libc::geteuid() } || m.mode() & 0o077 != 0 || m.nlink() != 1 {
        return Err(ProcessLockRefusal::Unavailable);
    }
    // Descriptors 0 to 2 are replaced by the child's standard streams before the pre-exec step.
    if file.as_raw_fd() <= libc::STDERR_FILENO {
        return Err(ProcessLockRefusal::Unavailable);
    }
    if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } != 0 {
        return Err(if std::io::Error::last_os_error().raw_os_error() == Some(libc::EWOULDBLOCK) {
            ProcessLockRefusal::Held
        } else {
            ProcessLockRefusal::Unavailable
        });
    }
    Ok(file)
}
/// The lock every start of Codex takes, for every home: the App's lock file inside the home
/// directory `home` (an opened directory the caller has established is the one it holds), created
/// private if absent and opened by name inside that directory, never through a link. Exclusive and
/// non-waiting. The returned descriptor is close-on-exec; the start clears that in the Codex
/// child only.
#[cfg(unix)]
pub(crate) fn take_process_lock_in(home: &std::fs::File) -> Result<std::fs::File, ProcessLockRefusal> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::take_process_lock_in");
    use std::os::fd::{AsRawFd, FromRawFd};
    let name = std::ffi::CString::new(PROCESS_LOCK).map_err(|_| ProcessLockRefusal::Unavailable)?;
    let fd = unsafe {
        libc::openat(
            home.as_raw_fd(),
            name.as_ptr(),
            libc::O_RDWR | libc::O_CREAT | libc::O_NOFOLLOW | libc::O_CLOEXEC,
            0o600 as libc::c_uint,
        )
    };
    if fd < 0 {
        return Err(ProcessLockRefusal::Unavailable);
    }
    lock_opened(unsafe { std::fs::File::from_raw_fd(fd) })
}
#[cfg(not(unix))]
pub(crate) fn take_process_lock_in(_: &std::fs::File) -> Result<std::fs::File, ProcessLockRefusal> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("native_local_provider::take_process_lock_in");
    Err(ProcessLockRefusal::Unavailable)
}
/// Opens (creating it private if absent) the App's lock file by path and takes an exclusive,
/// non-waiting flock: the same file and the same checks as a start's own lock
/// ([`take_process_lock_in`]), for a holder or a contender that is not a start. Held by another
/// open file description: EARLIER_PROCESS. A link, a file not private to this user, a hard-linked
/// file or any other failure: PROCESS_LOCK_UNAVAILABLE.
#[cfg(all(test, unix))]
pub(crate) fn take_process_lock(path: &Path) -> Result<std::fs::File, String> {
    use std::os::unix::fs::OpenOptionsExt;
    let file = std::fs::OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(false)
        .mode(0o600)
        .custom_flags(libc::O_NOFOLLOW)
        .open(path)
        .map_err(|_| PROCESS_LOCK_UNAVAILABLE)?;
    lock_opened(file).map_err(|refusal| match refusal {
        ProcessLockRefusal::Held => EARLIER_PROCESS.into(),
        ProcessLockRefusal::Unavailable => PROCESS_LOCK_UNAVAILABLE.into(),
    })
}
/// Configuration from outside the dedicated local home, which is meant to share nothing. Codex 0.167
/// applies requirements.toml and the legacy managed_config.toml (and macOS managed preferences)
/// ABOVE session flags, so the fixed flags cannot hold the provider, catalogue or auth settings
/// against them. The system config.toml ranks below session flags but can set what the flags do not
/// pin, such as the sandbox, MCP servers, hooks and a notifier. Fail closed on presence, or where
/// presence cannot be established; never parse or copy contents.
const ADMIN_FILES: &[&str] = &["/etc/codex/managed_config.toml", "/etc/codex/requirements.toml", "/etc/codex/config.toml"];
pub(crate) fn require_no_admin_layers() -> Result<(), String> {
    let files: Vec<&Path> = ADMIN_FILES.iter().map(Path::new).collect();
    admin_sources_absent(&files, managed_preferences_present)
}
fn admin_sources_absent(
    files: &[&Path],
    managed_preferences: impl FnOnce() -> Result<bool, ()>,
) -> Result<(), String> {
    for file in files {
        if !matches!(std::fs::symlink_metadata(file), Err(e) if e.kind() == std::io::ErrorKind::NotFound) {
            return Err(LIMIT.into());
        }
    }
    match managed_preferences() {
        Ok(false) => Ok(()),
        _ => Err(LIMIT.into()),
    }
}
#[cfg(target_os = "macos")]
fn managed_preferences_present() -> Result<bool, ()> {
    use std::ffi::{c_char, c_void, CStr};
    type Ref = *const c_void;
    #[link(name = "CoreFoundation", kind = "framework")]
    extern "C" {
        fn CFStringCreateWithCString(allocator: Ref, text: *const c_char, encoding: u32) -> Ref;
        fn CFPreferencesCopyAppValue(key: Ref, application: Ref) -> Ref;
        fn CFRelease(value: Ref);
    }
    const UTF8: u32 = 0x0800_0100;
    struct Owned(Ref);
    impl Drop for Owned {
        fn drop(&mut self) {
            unsafe { CFRelease(self.0) }
        }
    }
    let string = |text: &CStr| {
        let value = unsafe { CFStringCreateWithCString(std::ptr::null(), text.as_ptr(), UTF8) };
        if value.is_null() { Err(()) } else { Ok(Owned(value)) }
    };
    // The same domain and keys Codex reads; presence alone refuses, the value is released unread.
    let application = string(c"com.openai.codex")?;
    for key in [c"config_toml_base64", c"requirements_toml_base64"] {
        let key = string(key)?;
        let value = unsafe { CFPreferencesCopyAppValue(key.0, application.0) };
        if !value.is_null() {
            drop(Owned(value));
            return Ok(true);
        }
    }
    Ok(false)
}
#[cfg(not(target_os = "macos"))]
fn managed_preferences_present() -> Result<bool, ()> {
    Err(())
}
/// The dedicated local entry with the provider and the model name in force.
pub(crate) fn fixed_selection(
    settings: &LocalSettings,
    entry: &str,
    provider: &str,
    model: &str,
) -> Result<(), String> {
    if entry != ENTRY || provider != PROVIDER || model != settings.model {
        return Err(LIMIT.into());
    }
    Ok(())
}
/// Shape only, for a holder without the bound Host; the Host's guards compare with the settings in force.
pub(crate) fn selection_shape(entry: &str, provider: &str, model: &str) -> Result<(), String> {
    if entry != ENTRY || provider != PROVIDER || !valid_model(model) {
        return Err(LIMIT.into());
    }
    Ok(())
}
/// The view for the web view: the settings in force and Codex's reported account kind only.
pub(crate) fn view(settings: &LocalSettings, generation: Value, configured: bool) -> Value {
    json!({"modeHomeClass":"local-provider","entryId":ENTRY,"providerId":PROVIDER,"endpoint":settings.endpoint,"model":settings.model,"generation":generation,"credentialState":if configured {"configured-not-verified"} else {"entry-required"},"credentialCustody":"Codex auth.json in the dedicated local home; App never reads it","validity":"not verified by configuration, login acknowledgment or account type"})
}
fn source(home: &HomeSession, plan: &OwnedHomePlan, generation: &Value) -> Result<LocalSettings, String> {
    if home.host.local_superseded() {
        return Err(RELAUNCH.into());
    }
    let settings = home.host.local_settings()?;
    // The bound session's own check: it remembers a key once seen (see `check_seen`).
    home.host.check_local_home()?;
    require_no_admin_layers()?;
    if generation["home"] != plan.opaque_home_id()
        || home.class() != HomeClass::LocalProvider
        || home.host_config.as_ref().map_err(|_| LIMIT)?.codex_home != plan.native_path()
    {
        return Err(LIMIT.into());
    }
    crate::runtime_session::check_start_source(home, generation).map_err(|_| LIMIT)?;
    home.host.require_local_destination(generation)?;
    Ok(settings)
}
/// Every key remains in a native callback and the existing private account pipe. No public secret DTO.
pub(crate) fn submit(
    home: &HomeSession,
    plan: &OwnedHomePlan,
    generation: &Value,
    entry_state: &CredentialEntry,
    window_current: impl Fn() -> Result<(), String>,
    entry: impl FnOnce(&str) -> Result<Option<String>, ()>,
) -> Result<Value, String> {
    let settings = source(home, plan, generation)?;
    window_current()?;
    let cwd = home
        .host_config
        .as_ref()
        .map_err(|_| LIMIT)?
        .cwd
        .to_str()
        .ok_or(LIMIT)?;
    // Readings of one generation are made one at a time and each supersedes every earlier proof,
    // so the requirements reading comes first and the configuration reading the key entry rests
    // on last. The requirements reply is still what decides whether a key may be entered.
    let deadline = std::time::Instant::now() + Duration::from_secs(20);
    let policy = home.host.account_requirements_read_until(generation, deadline)?;
    home.account_sources.lock().unwrap().push(policy.clone());
    home.host
        .source_request_wait(&policy, deadline.saturating_duration_since(std::time::Instant::now()))
        .map_err(|_| LIMIT)?;
    let _proof = home
        .host
        .provider_admission_read(generation, cwd, ENTRY, PROVIDER, &settings.model)?;
    source(home, plan, generation)?;
    window_current()?;
    // Before a key can exist: record the address in force for the Codex process that will receive
    // it, and read it back. Without that record the key field is not opened. A cancelled or failed
    // entry leaves a record with no key file, which decides nothing and is rewritten at next entry.
    write_key_address(plan, settings.endpoint())?;
    source(home, plan, generation)?;
    window_current()?;
    // Consumed even on cancel or unknown outcome. A replacement source is a separate explicit act.
    entry_state.begin(generation)?;
    // From here a key may exist for this session even before its file does.
    home.host.note_local_key();
    let request = home
        .host
        .account_login_api_key_from_native_entry(generation, Some(&policy), || {
            // The field names the address this process is bound to, from the checked source above.
            let input = entry(settings.endpoint())?;
            if source(home, plan, generation).is_err() || window_current().is_err() {
                return Err(());
            }
            Ok(input)
        })
        .map_err(|_| LIMIT)?;
    let Some(request) = request else {
        return Ok(view(&settings, generation.clone(), false));
    };
    home.account_sources.lock().unwrap().push(request.clone());
    home.host
        .source_request_wait(&request, Duration::from_secs(20))
        .map_err(|_| LIMIT)?;
    let e = request.evidence();
    if e["outcome"] != "response-observed-result"
        || e["authResponseShapeValid"] != true
        || e["sourceCurrent"] != true
    {
        return Err(LIMIT.into());
    }
    home.host.note_local_key();
    let observed = observe(home, plan, generation)?;
    if observed["credentialState"] != "configured-not-verified" {
        return Err(LIMIT.into());
    }
    window_current()?;
    Ok(observed)
}
/// Codex's own `account/read` with `refreshToken:false` for this exact generation; returns
/// whether Codex reports no account (`true`) or an API-key account (`false`). Anything else,
/// an error, a stale source or an unestablished reply refuses without a state claim.
fn reported_account(home: &HomeSession, generation: &Value, wait: Duration) -> Result<Option<bool>, String> {
    let read = home.host.account_read_no_refresh_scoped(generation)?;
    home.account_sources.lock().unwrap().push(read.clone());
    home.host
        .source_request_wait(&read, wait)
        .map_err(|_| LIMIT)?;
    let e = read.evidence();
    if e["outcome"] != "response-observed-result"
        || e["authResponseShapeValid"] != true
        || e["sourceCurrent"] != true
        || e["response"]["result"].get("account").is_none()
    {
        return Err(LIMIT.into());
    }
    Ok(match &e["response"]["result"]["account"] {
        Value::Null => Some(true),
        account if account["type"] == "apiKey" => Some(false),
        _ => None,
    })
}
/// Codex's own account report for this exact local generation. Only the reported account kind is
/// used. The App never opens auth.json, sees a key or claims validity. No account means entry is
/// required; any other account kind refuses without a state claim.
pub(crate) fn observe(
    home: &HomeSession,
    plan: &OwnedHomePlan,
    generation: &Value,
) -> Result<Value, String> {
    let settings = source(home, plan, generation)?;
    let configured = match reported_account(home, generation, ACCOUNT_WAIT)? {
        Some(none) => !none,
        None => return Err(LIMIT.into()),
    };
    if source(home, plan, generation)? != settings {
        return Err(LIMIT.into());
    }
    Ok(view(&settings, generation.clone(), configured))
}
/// Codex's own sign-out in the bound home, then Codex's own report of no account. Never reads,
/// moves or deletes auth.json itself. `key_present`: Codex's key file was positively present
/// (metadata only) before the sign-out, so a removal can be claimed.
fn sign_out(home: &HomeSession, plan: &OwnedHomePlan, generation: &Value, wait: Duration, key_present: bool) -> Result<(), String> {
    source(home, plan, generation).map_err(|_| PREPARE_FIRST)?;
    let request = home
        .host
        .account_logout_scoped(generation)
        .map_err(|_| PREPARE_FIRST)?;
    home.account_sources.lock().unwrap().push(request.clone());
    let waited = home
        .host
        .source_request_wait(&request, wait);
    let e = request.evidence();
    if waited.is_err()
        || e["outcome"] != "response-observed-result"
        || e["authResponseShapeValid"] != true
        || e["sourceCurrent"] != true
    {
        return Err(SIGN_OUT_UNCONFIRMED.into());
    }
    if let Some(selection) = home.access_selection.lock().unwrap().as_mut() {
        if selection.snapshot()["selection"]["entryId"] == ENTRY
            && selection.owning_generation() == Some(generation)
        {
            let _ = selection.unavailable("Codex reported logout for this entry before the local model settings changed; no home transfer or credential-file inspection");
        }
    }
    source(home, plan, generation).map_err(|_| SIGN_OUT_UNCONFIRMED)?;
    if reported_account(home, generation, wait).map_err(|_| SIGN_OUT_UNCONFIRMED)? != Some(true) {
        return Err(SIGN_OUT_UNCONFIRMED.into());
    }
    source(home, plan, generation).map_err(|_| SIGN_OUT_UNCONFIRMED)?;
    // Codex itself reported no account. The binding is superseded first, so nothing in this home
    // reaches a model once the record is gone; then the record is removed, before config.toml is
    // written. Unconfirmed removal changes no settings.
    home.host.supersede_local(wait).map_err(|error| match (error == WRITE_IN_PROGRESS, key_present) {
        (true, true) => WRITE_IN_PROGRESS_KEY_REMOVED.to_owned(),
        (true, false) => WRITE_IN_PROGRESS_NO_KEY.to_owned(),
        _ => error,
    })?;
    remove_key_address(plan).map_err(|error| if key_present { error } else { RECORD_NOT_REMOVED_NO_KEY.to_owned() })?;
    Ok(())
}
/// The read the web view calls: the App-owned file only; nothing is started.
/// With a key-address mismatch the state is "unavailable" but the stored settings are still shown,
/// with the reason token and the recorded address (null without a record), so the page can say
/// what the refusal says and offer setting the address back.
/// `superseded`: a change to the bound home's settings was begun through the App in this session,
/// so a relaunch is required even when the file again equals the settings in force (or the change
/// did not complete). `relaunchReason` says which is established: "settings-differ" when the file's
/// settings differ from those in force, otherwise "change-begun" when only the begun change requires
/// it; null when no relaunch is required.
pub(crate) fn settings_view(
    reading: Result<Reading, String>,
    in_force: Option<&LocalSettings>,
    superseded: bool,
) -> Value {
    let (state, settings, mismatch) = match &reading {
        Ok(Reading { settings: None, .. }) => ("unset", None, None),
        Ok(Reading { settings: Some(settings), mismatch: None }) => ("set", Some(settings), None),
        Ok(Reading { settings: Some(settings), mismatch: Some(m) }) => ("unavailable", Some(settings), Some(m)),
        Err(_) => ("unavailable", None, None),
    };
    let reason = mismatch.map(|_| KEY_ADDRESS_MISMATCH_REASON);
    let key_address = mismatch.and_then(|m| m.recorded.clone());
    let differ = matches!((settings, in_force), (Some(s), Some(f)) if s != f);
    let relaunch_reason = if differ { Some("settings-differ") } else if superseded { Some("change-begun") } else { None };
    json!({"state":state,"settings":settings.map(LocalSettings::json),"offered":{"endpoint":OFFERED_ENDPOINT},"inForce":in_force.map(LocalSettings::json),"relaunchRequired":relaunch_reason.is_some(),"relaunchReason":relaunch_reason,"reason":reason,"keyAddress":key_address})
}
fn effects(
    before: Option<&LocalSettings>,
    after: &LocalSettings,
    sign_out: bool,
    restore: bool,
    in_use: bool,
) -> Result<ns::NativeStatement, String> {
    let row = |name: &str, old: &str, new: &str| {
        if old == new {
            format!("{name}: {new} (unchanged)")
        } else {
            format!("{name}: {old}, changes to {new}")
        }
    };
    let mut lines = Vec::new();
    match before {
        None => {
            lines.push("Set the local model settings and create the dedicated local home.".to_owned());
            lines.push(format!("Server address: {}", after.endpoint));
            lines.push(format!("Model name: {}", after.model));
            lines.push("The local server requires a key, entered separately after this.".to_owned());
        }
        Some(b) => {
            lines.push("Change the local model settings.".to_owned());
            lines.push(row("Server address", &b.endpoint, &after.endpoint));
            lines.push(row("Model name", &b.model, &after.model));
            if sign_out {
                lines.push("The saved key is removed first, through Codex's own sign-out, so a key entered for one server is not sent to another. The key must be entered again.".into());
                lines.push(format!("Conversations already started with model name {} continue, with the server at the new address.", after.model));
            } else if restore {
                lines.push(format!("The server address is set back to {}, the address the saved key was entered for. The saved key is kept.", after.endpoint));
                lines.push(format!("Conversations already started with model name {} continue.", after.model));
            } else {
                lines.push("The saved key is kept.".into());
                lines.push(format!("Conversations already started with model name {} continue.", after.model));
            }
            if b.model != after.model {
                lines.push(format!("Conversations started with another model name, including {}, will not be continued.", b.model));
            } else {
                lines.push("Conversations started with another model name will not be continued.".into());
            }
        }
    }
    if in_use {
        lines.push("The local connection is in use in this session: the change takes effect after the App is quit and reopened, and the local connection is unavailable until then.".into());
    }
    lines.push("The key is never one of these settings.".into());
    let text = lines.join("\n");
    ns::whole_or_in_app(
        TITLE,
        "local model settings effects",
        text.clone(),
        &json!({"effects":text}),
        |digest| format!("{SAVE_ACTION}. The complete effects are shown in the App under Content named by an open native confirmation. sha-256: {digest}"),
    )
}
/// Validated settings, one native confirmation, then the change. Cancel changes nothing. A change
/// of address first has Codex remove a saved key in the bound home and report no account; without
/// that, nothing is changed. A model-only change keeps the key. auth.json is never opened by the App.
/// An address change waits for a Codex session in which no key entry was begun. A key entry
/// that was handed to Codex may still write its key after the App has stopped waiting for the
/// reply, and the address record must not move under it. Restarting Codex ends that process
/// before the next one starts in this home.
pub(crate) fn check_no_key_entry_before_address_change(
    plan: &OwnedHomePlan,
    proposed: &LocalSettings,
    generation: &Value,
    entry: &CredentialEntry,
) -> Result<(), String> {
    let address_changes = stored(plan)?.is_some_and(|saved| saved.endpoint != proposed.endpoint);
    if address_changes && entry.begun(generation) {
        return Err(KEY_ENTRY_BEGUN.into());
    }
    Ok(())
}
pub(crate) fn save(
    plan: &OwnedHomePlan,
    proposed: LocalSettings,
    in_use: Option<&HomeSession>,
    window_current: impl Fn() -> Result<(), String>,
    confirm: impl FnOnce(&ns::NativeStatement, &str) -> Result<MessageDialogResult, String>,
) -> Result<Value, String> {
    save_within(plan, proposed, in_use, window_current, confirm, ACCOUNT_WAIT)
}
pub(crate) fn save_within(
    plan: &OwnedHomePlan,
    proposed: LocalSettings,
    in_use: Option<&HomeSession>,
    window_current: impl Fn() -> Result<(), String>,
    confirm: impl FnOnce(&ns::NativeStatement, &str) -> Result<MessageDialogResult, String>,
    wait: Duration,
) -> Result<Value, String> {
    let in_force = in_use.and_then(|home| home.host.local_settings().ok());
    // `signedOut`: Codex's sign-out ran in this save and Codex then reported no account.
    // `keyRemoved`: that, and Codex's key file was positively present before it (metadata only);
    // without a key file present nothing is claimed removed.
    let outcome = |outcome: &str, signed_out: bool, removed: bool| {
        let superseded = in_use.is_some_and(|home| home.host.local_superseded());
        let mut view = settings_view(read(plan), in_force.as_ref(), superseded);
        view["outcome"] = json!(outcome);
        view["signedOut"] = json!(signed_out);
        view["keyRemoved"] = json!(signed_out && removed);
        view
    };
    let before = stored(plan)?;
    if before.as_ref() == Some(&proposed) {
        return Ok(outcome("unchanged", false, false));
    }
    if before.is_none() && (in_use.is_some() || !absent(&plan.native_path().join("auth.json"))) {
        return Err(LIMIT.into());
    }
    let address_changes = before
        .as_ref()
        .is_some_and(|b| b.endpoint != proposed.endpoint);
    // The one address change that keeps the key: back to exactly the address the App recorded for
    // the saved key, with Codex's key file present. Every read is strict; anything not
    // established is an ordinary change, which removes the key first.
    let restoring = || {
        address_changes
            && matches!(read_key_address(plan), Ok(Some(recorded)) if recorded == proposed.endpoint)
            && key_file_present(plan)
    };
    let restore = restoring();
    let needs_sign_out = address_changes && !restore;
    // A change that keeps the key keeps it only where it was entered for. (An address change
    // establishes this through the bound home's source check before Codex signs out.)
    let key_kept = || match (&before, needs_sign_out, restore) {
        (_, _, true) if !restoring() => Err(CHANGED.to_owned()),
        (Some(b), false, false) => key_address_check(plan, b),
        _ => Ok(()),
    };
    key_kept()?;
    // The bound, ready home whose settings in force are still the file's: Codex can sign out there.
    let ready = || -> Result<(&HomeSession, Value), String> {
        let home = in_use.ok_or(PREPARE_FIRST)?;
        let snapshot = home.host.snapshot();
        if snapshot["state"] != "ready"
            || home.host.local_settings().ok() != before
            || in_force != before
        {
            return Err(PREPARE_FIRST.into());
        }
        let generation = snapshot["generation"].clone();
        source(home, plan, &generation).map_err(|_| PREPARE_FIRST)?;
        Ok((home, generation))
    };
    let signing = if needs_sign_out { Some(ready()?) } else { None };
    window_current()?;
    let statement = effects(before.as_ref(), &proposed, needs_sign_out, restore, in_use.is_some())?;
    let result = ns::showing_in_app(statement.in_app.as_ref(), || confirm(&statement, SAVE_ACTION))?;
    if !ns::chose(&result, SAVE_ACTION) {
        return Ok(outcome("cancelled", false, false));
    }
    window_current()?;
    if stored(plan)? != before {
        return Err(CHANGED.into());
    }
    key_kept()?;
    let mut key_present = false;
    if let Some((home, generation)) = &signing {
        let (again, now) = ready()?;
        if !std::ptr::eq(again, *home) || now != *generation {
            return Err(PREPARE_FIRST.into());
        }
        key_present = key_file_present(plan);
        sign_out(home, plan, generation, wait, key_present)?;
    }
    // A home bound in this session is superseded before the new file can exist: from here the
    // central guard admits nothing to a model in it, whether or not the write below completes.
    // After a sign-out in this save the mark is already set and this returns at once.
    if let Some(home) = in_use {
        home.host.supersede_local(wait)?;
    }
    let written = match &before {
        None => write_initial(plan, &proposed),
        Some(before) => replace(plan, before, &proposed),
    };
    // Codex's sign-out is already observed; never let a write failure hide it.
    written.map_err(|error| match (signing.is_some(), key_present) {
        (true, true) => format!("Codex removed the saved key; {error}"),
        (true, false) => format!("Codex reports no saved key; {error}"),
        _ => error,
    })?;
    Ok(outcome("saved", signing.is_some(), key_present))
}

/// The plugin's parent() silently ignores failed handle lookups. Only these already successful
/// borrowed handles are supplied to it, on the main thread.
struct Parent<'a> {
    window: WindowHandle<'a>,
    display: DisplayHandle<'a>,
}
impl HasWindowHandle for Parent<'_> {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
        Ok(self.window)
    }
}
impl HasDisplayHandle for Parent<'_> {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
        Ok(self.display)
    }
}
const WINDOW_LIMIT: &str =
    "Original App window could not confirm the local model settings; nothing was saved";
fn with_parent<T>(
    original: &(impl HasWindowHandle + HasDisplayHandle),
    present: impl FnOnce(&Parent<'_>) -> T,
) -> Result<T, String> {
    let parent = Parent {
        window: original.window_handle().map_err(|_| WINDOW_LIMIT)?,
        display: original.display_handle().map_err(|_| WINDOW_LIMIT)?,
    };
    Ok(present(&parent))
}
fn result_in_parent(
    original: &(impl HasWindowHandle + HasDisplayHandle),
    result: MessageDialogResult,
    action: &str,
) -> Result<MessageDialogResult, String> {
    if ns::chose(&result, action) {
        with_parent(original, |_| ())?;
    }
    Ok(result)
}
/// One native question parented to the invoking window; an affirmative answer is accepted only
/// after the same original window's handles are checked again.
pub(crate) fn confirm_native(
    invoking: &tauri::Window,
    statement: &ns::NativeStatement,
    action: &str,
) -> Result<MessageDialogResult, String> {
    let (send, receive) = mpsc::channel();
    let window = invoking.clone();
    let text = statement.text.clone();
    let action = action.to_owned();
    invoking
        .run_on_main_thread(move || {
            let callback_send = send.clone();
            let callback_window = window.clone();
            let shown = with_parent(&window, |parent| {
                window
                    .dialog()
                    .message(text)
                    .title(TITLE)
                    .kind(MessageDialogKind::Info)
                    .buttons(ns::act_buttons(LEAVE, &action))
                    .parent(parent)
                    .show_with_result(move |result| {
                        if !ns::chose(&result, &action) {
                            let _ = callback_send.send(Ok(result));
                            return;
                        }
                        let original = callback_window.clone();
                        let failure = callback_send.clone();
                        if callback_window
                            .run_on_main_thread(move || {
                                let _ = callback_send.send(result_in_parent(&original, result, &action));
                            })
                            .is_err()
                        {
                            let _ = failure.send(Err(WINDOW_LIMIT.into()));
                        }
                    });
            });
            if let Err(error) = shown {
                let _ = send.send(Err(error));
            }
        })
        .map_err(|_| WINDOW_LIMIT.to_owned())?;
    receive.recv().map_err(|_| WINDOW_LIMIT.to_owned())?
}
/// Fixture: a home whose first settings were saved and which was then prepared.
#[cfg(test)]
pub(crate) fn prepare_for_test(plan: &OwnedHomePlan, settings: &LocalSettings) {
    write_initial(plan, settings).unwrap();
    prepare(plan).unwrap();
}

#[cfg(all(test, unix))]
mod tests {
    use super::*;
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
    /// The exact bytes earlier builds wrote; a home holding them keeps working unchanged.
    const LEGACY_CONFIG: &str = "model_provider = \"chirality-omlx\"\nmodel = \"mlx-community/Qwen3.6-35B-A3B-8bit\"\ncli_auth_credentials_store = \"file\"\n[features]\nplugins = false\napi_key_model_discovery = false\n[model_providers.chirality-omlx]\nname = \"oMLX\"\nbase_url = \"http://127.0.0.1:8000/v1\"\nwire_api = \"responses\"\nrequires_openai_auth = true\n";
    const CANARY: &str = "INVENTED_LOCAL_SETTINGS_KEY_CANARY_733";
    fn fixture() -> (std::path::PathBuf, OwnedHomePlan) {
        let root = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("local-custody-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let plan = OwnedHomePlan::new(
            root.clone(),
            root.join("local"),
            HomeClass::LocalProvider,
            None,
        )
        .unwrap();
        (root, plan)
    }
    /// A home as an earlier build prepared it (and as a first save writes the legacy values).
    fn seed(plan: &OwnedHomePlan) {
        prepare_for_test(plan, &LocalSettings::legacy());
    }
    fn accept(_: &ns::NativeStatement, action: &str) -> Result<MessageDialogResult, String> {
        Ok(MessageDialogResult::Custom(action.into()))
    }
    /// The typed route: the dedicated local home is bound only with its own lock file's path.
    #[test]
    fn local_process_lock_binding_requires_the_homes_own_lock_path() {
        let (root, plan) = fixture();
        seed(&plan);
        let base = HostConfig::new(root.join("not-an-executable"), root.join("account"), root.join("probe"), root.clone());
        let cfg = config(&base, &plan).unwrap();
        assert_eq!(cfg.process_lock.as_deref(), Some(plan.native_path().join(PROCESS_LOCK).as_path()));
        for wrong in [None, Some(root.join("account").join(PROCESS_LOCK)), Some(plan.native_path().join("auth.lock"))] {
            let mut changed = cfg.clone();
            changed.process_lock = wrong;
            assert!(crate::hosting::Host::new().bind_local_destination(&changed, &plan).is_err());
        }
        crate::hosting::Host::new().bind_local_destination(&cfg, &plan).unwrap();
        std::fs::remove_dir_all(root).unwrap();
    }
    /// The App never removes, replaces or recreates a home's process lock file: preparing,
    /// checking and configuring the dedicated local home again while its lock is held leaves the
    /// same file, still held. (No other App code removes or renames anything inside a Codex
    /// home; an account home that already exists is never prepared again.)
    #[test]
    fn preparing_the_local_home_again_leaves_a_held_process_lock_file_as_it_is() {
        use std::os::unix::fs::MetadataExt;
        let (root, plan) = fixture();
        let settings = LocalSettings::legacy();
        prepare_for_test(&plan, &settings);
        let path = plan.native_path().join(PROCESS_LOCK);
        let held = take_process_lock(&path).unwrap();
        let before = std::fs::symlink_metadata(&path).unwrap();
        let base = HostConfig::new(root.join("not-an-executable"), root.join("account"), root.join("probe"), root.clone());
        for _ in 0..2 {
            prepare(&plan).unwrap();
            check(&plan, &settings).unwrap();
            config(&base, &plan).unwrap();
        }
        let after = std::fs::symlink_metadata(&path).unwrap();
        assert_eq!((after.dev(), after.ino(), after.nlink(), after.mode()), (before.dev(), before.ino(), before.nlink(), before.mode()), "the same file");
        assert_eq!(take_process_lock(&path).unwrap_err(), EARLIER_PROCESS, "still held by the first holder");
        drop(held);
        drop(take_process_lock(&path).expect("free once that holder lets go"));
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_provider_fixed_nonsecret_config_is_private_create_only_and_has_no_account_links(
    ) {
        let (root, plan) = fixture();
        seed(&plan);
        prepare(&plan).unwrap();
        assert_eq!(
            std::fs::metadata(plan.native_path()).unwrap().mode() & 0o777,
            0o700
        );
        for name in ["config.toml", "auth.lock"] {
            assert_eq!(
                std::fs::metadata(plan.native_path().join(name))
                    .unwrap()
                    .mode()
                    & 0o777,
                0o600
            );
        }
        assert!(!plan.native_path().join("auth.json").exists());
        let base = HostConfig::new(
            root.join("not-an-executable"),
            root.join("account"),
            root.join("probe"),
            root.clone(),
        );
        let cfg = config(&base, &plan).unwrap();
        assert_eq!(base.codex_home, root.join("account"));
        assert_eq!(cfg.codex_home, plan.native_path());
        let text = cfg.session_flags.join("\n");
        for absent in [
            "apiKey",
            "experimental_bearer_token",
            "env_key",
            "OPENAI_API_KEY",
            "auth.json",
        ] {
            assert!(!text.contains(absent));
        }
        assert!(
            text.contains(ENDPOINT)
                && text.contains(MODEL)
                && text.contains("requires_openai_auth=true")
        );
        let s = LocalSettings::legacy();
        for v in ["openai", "", "another-provider"] {
            assert!(fixed_selection(&s, ENTRY, v, MODEL).is_err());
        }
        for v in ["", "different-model"] {
            assert!(fixed_selection(&s, ENTRY, PROVIDER, v).is_err());
        }
        assert!(fixed_selection(&s, "api-key", PROVIDER, MODEL).is_err());
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_provider_the_system_config_file_refuses_like_managed_configuration() {
        assert!(ADMIN_FILES.contains(&"/etc/codex/config.toml"));
        let (root, _plan) = fixture();
        // The same name in a scratch folder: absent passes, present refuses, unexaminable refuses.
        let etc = root.join("etc-codex");
        std::fs::create_dir(&etc).unwrap();
        let system = etc.join("config.toml");
        assert!(admin_sources_absent(&[system.as_path()], || Ok(false)).is_ok(), "absent");
        std::fs::write(&system, "unparsed").unwrap();
        assert_eq!(admin_sources_absent(&[system.as_path()], || Ok(false)).unwrap_err(), LIMIT, "present");
        std::fs::remove_file(&system).unwrap();
        std::fs::set_permissions(&etc, std::fs::Permissions::from_mode(0o000)).unwrap();
        let unexaminable = admin_sources_absent(&[system.as_path()], || Ok(false));
        std::fs::set_permissions(&etc, std::fs::Permissions::from_mode(0o700)).unwrap();
        assert_eq!(unexaminable.unwrap_err(), LIMIT, "presence cannot be established");
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_provider_admin_layers_above_session_flags_refuse_without_reading() {
        let (root, _plan) = fixture();
        let absent = root.join("absent.toml");
        assert!(admin_sources_absent(&[absent.as_path()], || Ok(false)).is_ok());
        let present = root.join("managed_config.toml");
        std::fs::write(&present, "unparsed").unwrap();
        assert!(admin_sources_absent(&[absent.as_path(), present.as_path()], || Ok(false)).is_err());
        let link = root.join("link.toml");
        std::os::unix::fs::symlink(root.join("dangling"), &link).unwrap();
        assert!(admin_sources_absent(&[link.as_path()], || Ok(false)).is_err(), "a dangling link is not absence");
        assert!(admin_sources_absent(&[absent.as_path()], || Ok(true)).is_err());
        assert!(admin_sources_absent(&[absent.as_path()], || Err(())).is_err(), "unknown preference state fails closed");
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_provider_disables_api_key_catalogue_discovery_in_file_and_session_flags() {
        let s = LocalSettings::new("http://[::1]:9000/api/v1", "org/model-1").unwrap();
        assert!(canonical(&s).contains("[features]\nplugins = false\napi_key_model_discovery = false\n"));
        assert!(canonical(&s).contains("cli_auth_credentials_store = \"file\"\n"));
        assert!(canonical(&s).ends_with("requires_openai_auth = true\n"), "a local server always requires a key");
        assert!(session_flags(&s).iter().any(|f| f.ends_with("requires_openai_auth=true}")));
        let (root, plan) = fixture();
        seed(&plan);
        let base = HostConfig::new(root.join("x"), root.join("account"), root.join("probe"), root.clone());
        let flags = config(&base, &plan).unwrap().session_flags;
        assert!(flags.iter().any(|f| f == "features.api_key_model_discovery=false"));
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_provider_rejects_unsafe_modes_links_hardlinks_and_drift_without_repair() {
        for case in [
            "home-mode",
            "config-mode",
            "config-link",
            "config-hardlink",
            "config-drift",
            "auth-mode",
            "auth-link",
        ] {
            let (root, plan) = fixture();
            seed(&plan);
            let cfg = plan.native_path().join("config.toml");
            match case {
                "home-mode" => std::fs::set_permissions(
                    plan.native_path(),
                    std::fs::Permissions::from_mode(0o755),
                )
                .unwrap(),
                "config-mode" => {
                    std::fs::set_permissions(&cfg, std::fs::Permissions::from_mode(0o644)).unwrap()
                }
                "config-link" => {
                    std::fs::rename(&cfg, root.join("saved")).unwrap();
                    std::os::unix::fs::symlink(root.join("saved"), &cfg).unwrap();
                }
                "config-hardlink" => std::fs::hard_link(&cfg, root.join("alias")).unwrap(),
                "config-drift" => std::fs::write(&cfg, "model_provider=\"openai\"\n").unwrap(),
                "auth-mode" => std::fs::write(
                    plan.native_path().join("auth.json"),
                    "invented credential file; do not read",
                )
                .unwrap(),
                "auth-link" => std::os::unix::fs::symlink(
                    root.join("not-read"),
                    plan.native_path().join("auth.json"),
                )
                .unwrap(),
                _ => unreachable!(),
            }
            assert!(check(&plan, &LocalSettings::legacy()).is_err(), "{case}");
            assert!(
                prepare(&plan).is_err(),
                "{case}: no chmod/migration/overwrite"
            );
            let changed = LocalSettings::new(ENDPOINT, "other-model").unwrap();
            assert!(save(&plan, changed, None, || Ok(()), accept).is_err(), "{case}: no settings write over an unsafe home");
            std::fs::remove_dir_all(root).unwrap();
        }
    }
    #[test]
    fn native_local_provider_entry_once_includes_unknown_or_cancelled_attempt_and_dto_has_no_secret(
    ) {
        let entry = CredentialEntry::default();
        let g = json!({"appSession":"s","home":"h","spawnCounter":1});
        entry.begin(&g).unwrap();
        assert!(entry.begin(&g).is_err());
        let mut later = g.clone();
        later["spawnCounter"] = json!(2);
        entry.begin(&later).unwrap();
        let dto = view(&LocalSettings::legacy(), g, true);
        assert_eq!(dto["credentialState"], "configured-not-verified");
        assert_eq!(dto["modeHomeClass"], "local-provider");
        assert_eq!(dto["entryId"], ENTRY);
        assert!(dto.get("keyRequired").is_none());
        assert!(!dto.to_string().contains("apiKey"));
    }
    #[test]
    fn native_local_settings_validation_refuses_every_non_loopback_or_unsafe_value_without_correction() {
        for good in [
            "http://127.0.0.1:8000/v1",
            "https://127.0.0.1:8000/v1",
            "http://[::1]:8000/v1",
            "http://127.0.0.1",
            "http://127.0.0.1/",
            "http://127.0.0.1:1/a.b_c~d/e-f",
            "http://127.0.0.1:65535/v1",
        ] {
            assert!(LocalSettings::new(good, "m").is_ok(), "{good}");
        }
        let long_path = format!("http://127.0.0.1:8000/{}", "a".repeat(2048 - 22));
        assert_eq!(long_path.len(), 2048);
        assert!(LocalSettings::new(&long_path, "m").is_ok(), "2048 bytes");
        let too_long = format!("{long_path}a");
        for bad in [
            "http://localhost:8000/v1",
            "http://192.168.1.20:8000/v1",
            "http://10.0.0.1/v1",
            "http://127.0.0.2:8000/v1",
            "http://127.0.0.10:8000/v1",
            "http://0x7f000001/v1",
            "http://[::2]:8000/v1",
            "http://[0:0:0:0:0:0:0:1]/v1",
            "ftp://127.0.0.1/v1",
            "HTTP://127.0.0.1/v1",
            "127.0.0.1:8000/v1",
            "http://user@127.0.0.1:8000/v1",
            "http://user:pw@127.0.0.1:8000/v1",
            "http://127.0.0.1@example.invalid/v1",
            "http://127.0.0.1:8000@example.invalid/v1",
            "http://127.0.0.1.example.invalid/v1",
            "http://127.0.0.1:0/v1",
            "http://127.0.0.1:65536/v1",
            "http://127.0.0.1:08000/v1",
            "http://127.0.0.1:/v1",
            "http://127.0.0.1:80a/v1",
            "http://127.0.0.1:8000/v1?key=x",
            "http://127.0.0.1:8000/v1#x",
            "http://127.0.0.1:8000/v%31",
            "http://127.0.0.1:8000/v 1",
            "http://127.0.0.1:8000/v1 ",
            " http://127.0.0.1:8000/v1",
            "http://127.0.0.1:8000/v1\n",
            "http://127.0.0.1:8000/v1\"",
            "http://127.0.0.1:8000/v1\\",
            "http://127.0.0.1:8000/é",
            "",
            too_long.as_str(),
        ] {
            assert_eq!(LocalSettings::new(bad, "m").unwrap_err(), ADDRESS_RULE, "{bad:?}");
        }
        let max = "m".repeat(128);
        for good in ["m", "mlx-community/Qwen3.6-35B-A3B-8bit", "a.b_c:d/e@f+g-h", max.as_str()] {
            assert!(LocalSettings::new(ENDPOINT, good).is_ok(), "{good}");
        }
        let over = "m".repeat(129);
        for bad in ["", "a\"b", "a\nb", "a b", "a\\b", " m", "m ", "a'b", "a=b", "a#b", "a{b}", "a,b", "é", over.as_str()] {
            assert_eq!(LocalSettings::new(ENDPOINT, bad).unwrap_err(), MODEL_RULE, "{bad:?}");
        }
        assert!(!ADDRESS_RULE.contains("8000") && !MODEL_RULE.contains("Qwen"), "refusals carry no submitted value");
    }
    #[test]
    fn native_local_settings_canonical_bytes_round_trip_legacy_is_accepted_and_hand_edits_refused() {
        assert_eq!(canonical(&LocalSettings::legacy()), LEGACY_CONFIG);
        assert_eq!(parse(LEGACY_CONFIG.as_bytes()), Some(LocalSettings::legacy()));
        assert_eq!(LocalSettings::legacy().json(), json!({"endpoint":"http://127.0.0.1:8000/v1","model":"mlx-community/Qwen3.6-35B-A3B-8bit"}));
        for s in [
            LocalSettings::new("http://[::1]:1234/a/b", "model@1+x").unwrap(),
            LocalSettings::new("https://127.0.0.1", "m").unwrap(),
        ] {
            assert_eq!(parse(canonical(&s).as_bytes()), Some(s.clone()));
            let flags = session_flags(&s).join("\n");
            assert!(flags.contains(&format!("model=\"{}\"", s.model())));
            assert!(flags.contains(&format!("base_url=\"{}\"", s.endpoint())));
            assert!(flags.contains("requires_openai_auth=true"));
        }
        let canonical_text = canonical(&LocalSettings::new("http://127.0.0.1:8000/v1", "m").unwrap());
        for edited in [
            canonical_text.replace("model = \"m\"", "model =  \"m\""),
            canonical_text.replace("\n[features]", "\n# comment\n[features]"),
            canonical_text.replace("plugins = false", "plugins = true"),
            canonical_text.replace("name = \"oMLX\"", "name = \"other\""),
            canonical_text.replace("wire_api = \"responses\"", "wire_api = \"chat\""),
            canonical_text.replace("requires_openai_auth = true", "requires_openai_auth = false"),
            canonical_text.replace("requires_openai_auth = true", "requires_openai_auth = True"),
            canonical_text.replace("127.0.0.1", "localhost"),
            canonical_text.replace("model = \"m\"", "model = \"m\\\"\""),
            format!("{canonical_text}env_key = \"X\"\n"),
            canonical_text.trim_end().to_owned(),
            canonical_text.replace('\n', "\r\n"),
            format!("\u{feff}{canonical_text}"),
        ] {
            assert_eq!(parse(edited.as_bytes()), None, "{edited:?}");
        }
        assert_eq!(parse(&[0xff, 0xfe]), None);
    }
    #[test]
    fn native_local_settings_unset_prepare_refuses_and_first_save_creates_only_after_confirmation() {
        let (root, plan) = fixture();
        assert_eq!(stored(&plan), Ok(None));
        assert_eq!(prepare(&plan).unwrap_err(), UNSET);
        assert!(!plan.native_path().exists(), "no defaults written");
        let view = settings_view(read(&plan), None, false);
        assert_eq!(view, json!({"state":"unset","settings":null,"offered":{"endpoint":"http://127.0.0.1:8000/v1"},"inForce":null,"relaunchRequired":false,"relaunchReason":null,"reason":null,"keyAddress":null}));
        let chosen = LocalSettings::new("http://127.0.0.1:9000/v1", "org/model").unwrap();
        for cancel in [MessageDialogResult::Cancel, MessageDialogResult::Custom(LEAVE.into()), MessageDialogResult::Custom(format!("{SAVE_ACTION} "))] {
            let mut asked = None;
            let out = save(&plan, chosen.clone(), None, || Ok(()), |s, a| { asked = Some((s.text.clone(), a.to_owned())); Ok(cancel.clone()) }).unwrap();
            assert_eq!(out["outcome"], "cancelled");
            assert!(!plan.native_path().exists(), "Cancel changes nothing");
            let (text, action) = asked.unwrap();
            assert_eq!(action, SAVE_ACTION);
            assert!(text.contains("Server address: http://127.0.0.1:9000/v1") && text.contains("Model name: org/model") && text.contains("requires a key"));
        }
        assert!(save(&plan, chosen.clone(), None, || Err("window gone".into()), accept).is_err());
        assert!(!plan.native_path().exists());
        let out = save(&plan, chosen.clone(), None, || Ok(()), accept).unwrap();
        assert_eq!(out["outcome"], "saved");
        assert_eq!(out["keyRemoved"], false);
        assert_eq!(out["state"], "set");
        assert_eq!(out["settings"], chosen.json());
        assert_eq!(std::fs::metadata(plan.native_path()).unwrap().mode() & 0o777, 0o700);
        assert_eq!(std::fs::metadata(plan.native_path().join("config.toml")).unwrap().mode() & 0o777, 0o600);
        assert_eq!(std::fs::read_to_string(plan.native_path().join("config.toml")).unwrap(), canonical(&chosen));
        assert_eq!(prepare(&plan).unwrap(), chosen);
        assert_eq!(save(&plan, chosen.clone(), None, || Ok(()), |_, _| panic!("no question for no change")).unwrap()["outcome"], "unchanged");
        std::fs::remove_dir_all(root).unwrap();
        // A credential slot without settings is not a first time: refuse without opening it.
        let (root, plan) = fixture();
        std::fs::create_dir(plan.native_path()).unwrap();
        std::fs::set_permissions(plan.native_path(), std::fs::Permissions::from_mode(0o700)).unwrap();
        std::fs::write(plan.native_path().join("auth.json"), CANARY).unwrap();
        let error = save(&plan, chosen, None, || Ok(()), accept).unwrap_err();
        assert!(!error.contains(CANARY));
        assert!(!plan.native_path().join("config.toml").exists());
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_settings_model_only_change_replaces_atomically_and_address_change_needs_a_prepared_home() {
        let (root, plan) = fixture();
        seed(&plan);
        std::fs::write(plan.native_path().join("auth.json"), CANARY).unwrap();
        std::fs::set_permissions(plan.native_path().join("auth.json"), std::fs::Permissions::from_mode(0o600)).unwrap();
        write_key_address(&plan, ENDPOINT).unwrap();
        let auth_before = std::fs::metadata(plan.native_path().join("auth.json")).unwrap();
        // An address change: without a prepared, ready home Codex cannot remove the key.
        for endpoint in ["http://127.0.0.1:9000/v1", "http://[::1]:8000/v1", "https://127.0.0.1:8000/v1"] {
            let next = LocalSettings::new(endpoint, MODEL).unwrap();
            let error = save(&plan, next, None, || Ok(()), |_, _| panic!("no question that cannot be acted on")).unwrap_err();
            assert_eq!(error, PREPARE_FIRST);
            assert_eq!(std::fs::read_to_string(plan.native_path().join("config.toml")).unwrap(), LEGACY_CONFIG);
        }
        // Model only: no sign-out, the key stays, the file is replaced whole.
        let next = LocalSettings::new(ENDPOINT, "org/next-model").unwrap();
        let mut asked = String::new();
        let out = save(&plan, next.clone(), None, || Ok(()), |s, a| { asked = s.text.clone(); accept(s, a) }).unwrap();
        assert!(asked.contains("Model name: mlx-community/Qwen3.6-35B-A3B-8bit, changes to org/next-model"));
        assert!(asked.contains("will not be continued") && asked.contains("saved key is kept") && !asked.contains("sign-out") && !asked.contains("quit and reopen"));
        assert_eq!(out["outcome"], "saved");
        assert_eq!(out["keyRemoved"], false);
        assert_eq!(std::fs::read_to_string(plan.native_path().join("config.toml")).unwrap(), canonical(&next));
        let m = std::fs::metadata(plan.native_path().join("config.toml")).unwrap();
        assert_eq!((m.mode() & 0o777, m.nlink()), (0o600, 1));
        let auth_after = std::fs::metadata(plan.native_path().join("auth.json")).unwrap();
        assert_eq!((auth_before.ino(), auth_before.mtime(), auth_before.len()), (auth_after.ino(), auth_after.mtime(), auth_after.len()), "the key's file is not touched");
        let names: Vec<_> = std::fs::read_dir(plan.native_path()).unwrap().map(|e| e.unwrap().file_name().into_string().unwrap()).collect();
        assert!(names.iter().all(|n| ["config.toml", "auth.lock", "auth.json", "key-address"].contains(&n.as_str())), "no temporary left: {names:?}");
        assert!(!format!("{out}{asked}").contains(CANARY));
        // A file changed after binding refuses every bound check until the App binds again.
        assert_eq!(check(&plan, &LocalSettings::legacy()).unwrap_err(), RELAUNCH);
        assert!(check(&plan, &next).is_ok());
        let view = settings_view(read(&plan), Some(&LocalSettings::legacy()), false);
        assert_eq!(view["relaunchRequired"], true);
        assert_eq!(view["inForce"], LocalSettings::legacy().json());
        assert_eq!(settings_view(read(&plan), Some(&next), false)["relaunchRequired"], false);
        std::fs::write(plan.native_path().join("config.toml"), "hand edited\n").unwrap();
        let view = settings_view(read(&plan), Some(&next), false);
        assert_eq!((view["state"].as_str(), view["settings"].is_null()), (Some("unavailable"), true));
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_settings_question_states_every_consequence_and_requires_the_original_window() {
        let before = LocalSettings::legacy();
        let after = LocalSettings::new("http://[::1]:9000/v1", "other").unwrap();
        let s = effects(Some(&before), &after, true, false, true).unwrap();
        for part in ["Server address: http://127.0.0.1:8000/v1, changes to http://[::1]:9000/v1", "Model name: mlx-community/Qwen3.6-35B-A3B-8bit, changes to other", "Codex's own sign-out", "must be entered again", "model name other continue, with the server at the new address", "including mlx-community/Qwen3.6-35B-A3B-8bit, will not be continued", "quit and reopen", "never one of these settings"] {
            assert!(s.text.contains(part), "{part}");
        }
        let long = LocalSettings::new(&format!("http://127.0.0.1/{}", "a".repeat(1900)), "m").unwrap();
        let s = effects(Some(&before), &long, true, false, false).unwrap();
        assert!(s.in_app.is_some() && s.text.contains("sha-256"), "long effects are shown whole in the App");
        struct Handles(bool, bool);
        impl HasWindowHandle for Handles {
            fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
                if !self.0 { return Err(HandleError::Unavailable); }
                Ok(unsafe { WindowHandle::borrow_raw(raw_window_handle::RawWindowHandle::Web(raw_window_handle::WebWindowHandle::new(7))) })
            }
        }
        impl HasDisplayHandle for Handles {
            fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
                if !self.1 { return Err(HandleError::Unavailable); }
                Ok(unsafe { DisplayHandle::borrow_raw(raw_window_handle::RawDisplayHandle::Web(raw_window_handle::WebDisplayHandle::new())) })
            }
        }
        for (w, d) in [(false, true), (true, false), (false, false)] {
            assert!(result_in_parent(&Handles(w, d), MessageDialogResult::Custom(SAVE_ACTION.into()), SAVE_ACTION).is_err());
            assert!(with_parent(&Handles(w, d), |_| ()).is_err());
        }
        assert!(result_in_parent(&Handles(true, true), MessageDialogResult::Custom(SAVE_ACTION.into()), SAVE_ACTION).is_ok());
    }

    fn private_write(path: &std::path::Path, bytes: &str) {
        std::fs::write(path, bytes).unwrap();
        std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o600)).unwrap();
    }
    fn base(root: &std::path::Path) -> HostConfig {
        HostConfig::new(root.join("not-run"), root.join("account"), root.join("probe"), root.to_path_buf())
    }
    /// A key entry handed to Codex may still write its key after the App stopped waiting. An
    /// address change in the same Codex session is refused; a model-only change, an unchanged
    /// address and another Codex session are not.
    #[test]
    fn native_local_settings_address_change_waits_for_a_codex_session_without_key_entry() {
        let (root, plan) = fixture();
        let a = LocalSettings::new("http://127.0.0.1:9100/v1", "org/m").unwrap();
        let b = LocalSettings::new("http://127.0.0.1:9200/v1", "org/m").unwrap();
        let model_only = LocalSettings::new("http://127.0.0.1:9100/v1", "org/other").unwrap();
        let (first, second) = (json!({"home":"h","spawnCounter":1}), json!({"home":"h","spawnCounter":2}));
        let entry = CredentialEntry::default();
        // Nothing saved yet: a first save changes no address.
        assert!(check_no_key_entry_before_address_change(&plan, &b, &first, &entry).is_ok());
        prepare_for_test(&plan, &a);
        assert!(!entry.begun(&first));
        assert!(check_no_key_entry_before_address_change(&plan, &b, &first, &entry).is_ok());
        assert!(entry.begin_for_test(&first));
        assert!(entry.begun(&first) && !entry.begun(&second));
        assert_eq!(check_no_key_entry_before_address_change(&plan, &b, &first, &entry).unwrap_err(), KEY_ENTRY_BEGUN);
        assert!(check_no_key_entry_before_address_change(&plan, &model_only, &first, &entry).is_ok());
        assert!(check_no_key_entry_before_address_change(&plan, &a, &first, &entry).is_ok());
        assert!(check_no_key_entry_before_address_change(&plan, &b, &second, &entry).is_ok(), "a new Codex session");
        // A state that cannot be read counts as begun.
        let held = entry.attempted.lock().unwrap();
        assert!(entry.begun(&second));
        assert_eq!(check_no_key_entry_before_address_change(&plan, &b, &second, &entry).unwrap_err(), KEY_ENTRY_BEGUN);
        drop(held);
        assert!(!KEY_ENTRY_BEGUN.contains("9100") && !KEY_ENTRY_BEGUN.contains('/'));
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_settings_key_address_refuses_a_hand_edited_address_while_a_key_is_saved() {
        let (root, plan) = fixture();
        let a = LocalSettings::new("http://127.0.0.1:9100/v1", "org/m").unwrap();
        let b = LocalSettings::new("http://127.0.0.1:9200/v1", "org/m").unwrap();
        prepare_for_test(&plan, &a);
        assert!(!plan.native_path().join(KEY_ADDRESS).exists(), "a first save creates no record");
        write_key_address(&plan, a.endpoint()).unwrap();
        let record = plan.native_path().join(KEY_ADDRESS);
        assert_eq!(std::fs::read(&record).unwrap(), b"http://127.0.0.1:9100/v1\n", "exactly one address and a newline");
        let m = std::fs::metadata(&record).unwrap();
        assert_eq!((m.mode() & 0o777, m.nlink()), (0o600, 1));
        private_write(&plan.native_path().join("auth.json"), CANARY);
        assert_eq!(current(&plan).unwrap(), a);
        assert!(check(&plan, &a).is_ok() && prepare(&plan).is_ok() && config(&base(&root), &plan).is_ok());
        // The hand edit: only base_url, canonical form, private mode kept.
        private_write(&plan.native_path().join("config.toml"), &canonical(&b));
        assert_eq!(stored(&plan), Ok(Some(b.clone())), "the file itself is canonical");
        let refusal = "The local model server address now set is http://127.0.0.1:9200/v1, and the saved key was entered for http://127.0.0.1:9100/v1. The App will not use that key with another address. Set the address back to http://127.0.0.1:9100/v1.";
        assert_eq!(current(&plan).unwrap_err(), refusal, "the two addresses and nothing else");
        assert!(!refusal.contains(CANARY) && !refusal.contains("org/m"));
        assert_eq!(check(&plan, &b).unwrap_err(), refusal);
        assert_eq!(prepare(&plan).unwrap_err(), refusal);
        assert_eq!(config(&base(&root), &plan).unwrap_err(), refusal);
        let mut flags = base(&root);
        flags.codex_home = plan.native_path().into();
        flags.session_flags = session_flags(&b);
        assert_eq!(crate::hosting::Host::new().bind_local_destination(&flags, &plan).unwrap_err(), refusal, "nothing is bound to B");
        let view = settings_view(read(&plan), None, false);
        assert_eq!((view["state"].as_str(), view["reason"].as_str(), view["keyAddress"].as_str()), (Some("unavailable"), Some("key-address-mismatch"), Some("http://127.0.0.1:9100/v1")));
        assert_eq!(view["settings"], b.json(), "the address set, for the page's sentence");
        assert!(!view.to_string().contains(CANARY));
        // A model-only change cannot keep the key at B either.
        let model_only = LocalSettings::new(b.endpoint(), "org/other").unwrap();
        assert_eq!(save(&plan, model_only, None, || Ok(()), |_, _| panic!("no question")).unwrap_err(), refusal);
        assert_eq!(std::fs::read_to_string(plan.native_path().join("config.toml")).unwrap(), canonical(&b));
        // A Restart Codex re-checks with the settings in force (A): a record changed by hand refuses too.
        private_write(&plan.native_path().join("config.toml"), &canonical(&a));
        assert!(check(&plan, &a).is_ok());
        private_write(&record, "http://127.0.0.1:9200/v1\n");
        assert!(check(&plan, &a).unwrap_err().starts_with("The local model server address now set is http://127.0.0.1:9100/v1, and the saved key was entered for http://127.0.0.1:9200/v1."));
        private_write(&record, "http://127.0.0.1:9100/v1\n");
        assert!(check(&plan, &a).is_ok());
        assert_eq!(settings_view(read(&plan), None, false)["reason"], Value::Null);
        // Without a key file the record decides nothing; a stale one is harmless but must be valid.
        std::fs::remove_file(plan.native_path().join("auth.json")).unwrap();
        private_write(&plan.native_path().join("config.toml"), &canonical(&b));
        assert_eq!(current(&plan).unwrap(), b);
        assert!(!std::fs::read_to_string(&record).unwrap().contains(CANARY));
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_settings_key_file_without_a_record_refuses_at_every_address() {
        for endpoint in [
            "http://127.0.0.1:8000/v1",
            "http://127.0.0.1:9100/v1",
            "http://[::1]:8000/v1",
            "https://127.0.0.1:8000/v1",
        ] {
            let (root, plan) = fixture();
            seed(&plan);
            private_write(&plan.native_path().join("auth.json"), CANARY);
            let settings = LocalSettings::new(endpoint, MODEL).unwrap();
            private_write(&plan.native_path().join("config.toml"), &canonical(&settings));
            assert_eq!(current(&plan).unwrap_err(), KEY_ADDRESS_UNRECORDED, "{endpoint}");
            assert_eq!(check(&plan, &settings).unwrap_err(), KEY_ADDRESS_UNRECORDED, "{endpoint}");
            assert_eq!(prepare(&plan).unwrap_err(), KEY_ADDRESS_UNRECORDED, "{endpoint}");
            assert!(config(&base(&root), &plan).is_err(), "{endpoint}");
            let view = settings_view(read(&plan), None, false);
            assert_eq!((view["state"].as_str(), view["reason"].as_str(), view["keyAddress"].is_null()), (Some("unavailable"), Some("key-address-mismatch"), true), "{endpoint}: no record, no recorded address");
            assert_eq!(view["settings"], settings.json());
            // No record: no address change through the App keeps or reaches the key.
            let other = LocalSettings::new(if endpoint.contains("9100") { "http://127.0.0.1:8000/v1" } else { "http://127.0.0.1:9100/v1" }, MODEL).unwrap();
            assert_eq!(save(&plan, other, None, || Ok(()), |_, _| panic!("no question")).unwrap_err(), PREPARE_FIRST);
            let model_only = LocalSettings::new(endpoint, "org/other").unwrap();
            assert_eq!(save(&plan, model_only, None, || Ok(()), |_, _| panic!("no question")).unwrap_err(), KEY_ADDRESS_UNRECORDED);
            assert_eq!(std::fs::read_to_string(plan.native_path().join("config.toml")).unwrap(), canonical(&settings));
            std::fs::remove_dir_all(root).unwrap();
        }
        assert!(!KEY_ADDRESS_UNRECORDED.contains("http"), "names no address");
    }
    #[test]
    fn native_local_settings_key_address_record_that_is_not_exact_and_private_refuses() {
        for with_key in [true, false] {
            for case in ["no-newline", "two-newlines", "crlf", "two-addresses", "not-loopback", "empty", "garbage", "key-like", "mode", "symlink", "hardlink", "directory"] {
                let (root, plan) = fixture();
                seed(&plan);
                if with_key {
                    private_write(&plan.native_path().join("auth.json"), CANARY);
                }
                let record = plan.native_path().join(KEY_ADDRESS);
                match case {
                    "no-newline" => private_write(&record, ENDPOINT),
                    "two-newlines" => private_write(&record, &format!("{ENDPOINT}\n\n")),
                    "crlf" => private_write(&record, &format!("{ENDPOINT}\r\n")),
                    "two-addresses" => private_write(&record, &format!("{ENDPOINT}\n{ENDPOINT}\n")),
                    "not-loopback" => private_write(&record, "http://localhost:8000/v1\n"),
                    "empty" => private_write(&record, ""),
                    "garbage" => private_write(&record, "\u{feff}http://127.0.0.1:8000/v1\n"),
                    "key-like" => private_write(&record, &format!("{ENDPOINT}\n{CANARY}\n")),
                    "mode" => {
                        std::fs::write(&record, format!("{ENDPOINT}\n")).unwrap();
                        std::fs::set_permissions(&record, std::fs::Permissions::from_mode(0o644)).unwrap();
                    }
                    "symlink" => {
                        private_write(&root.join("elsewhere"), &format!("{ENDPOINT}\n"));
                        std::os::unix::fs::symlink(root.join("elsewhere"), &record).unwrap();
                    }
                    "hardlink" => {
                        private_write(&record, &format!("{ENDPOINT}\n"));
                        std::fs::hard_link(&record, root.join("alias")).unwrap();
                    }
                    "directory" => std::fs::create_dir(&record).unwrap(),
                    _ => unreachable!(),
                }
                let label = format!("{case} with key {with_key}");
                assert!(current(&plan).is_err(), "{label}");
                assert!(check(&plan, &LocalSettings::legacy()).is_err(), "{label}");
                assert!(prepare(&plan).is_err(), "{label}");
                let view = settings_view(read(&plan), None, false);
                assert_eq!(view["state"], "unavailable", "{label}");
                assert!(!view.to_string().contains(CANARY));
                std::fs::remove_dir_all(root).unwrap();
            }
        }
        let (root, plan) = fixture();
        seed(&plan);
        assert_eq!(write_key_address(&plan, "http://localhost/v1").unwrap_err(), RECORD_UNWRITTEN, "only a validated address is written");
        assert!(!plan.native_path().join(KEY_ADDRESS).exists());
        assert!(remove_key_address(&plan).is_ok(), "absence is removal");
        write_key_address(&plan, ENDPOINT).unwrap();
        write_key_address(&plan, "http://[::1]:9/x").unwrap();
        assert_eq!(std::fs::read(plan.native_path().join(KEY_ADDRESS)).unwrap(), b"http://[::1]:9/x\n");
        remove_key_address(&plan).unwrap();
        assert!(absent(&plan.native_path().join(KEY_ADDRESS)));
        let names: Vec<_> = std::fs::read_dir(plan.native_path()).unwrap().map(|e| e.unwrap().file_name().into_string().unwrap()).collect();
        assert!(names.iter().all(|n| ["config.toml", "auth.lock"].contains(&n.as_str())), "no temporary left: {names:?}");
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[cfg(all(test, target_os = "macos"))]
mod first_save_tests {
    use super::*;
    fn fixture() -> (std::path::PathBuf, OwnedHomePlan) {
        let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("local-first-save-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let plan = OwnedHomePlan::new(root.clone(), root.join("local"), HomeClass::LocalProvider, None).unwrap();
        (root, plan)
    }
    fn names(plan: &OwnedHomePlan) -> Vec<String> {
        let mut names: Vec<_> = std::fs::read_dir(plan.native_path()).unwrap().map(|e| e.unwrap().file_name().into_string().unwrap()).collect();
        names.sort();
        names
    }
    #[test]
    fn native_local_settings_first_save_failing_after_the_temporary_file_is_written_leaves_no_config_and_no_temporary() {
        let (root, plan) = fixture();
        let settings = LocalSettings::new("http://127.0.0.1:9100/v1", "org/m").unwrap();
        let mut seen = None;
        let error = write_initial_staged(&plan, &settings, |temporary| {
            // The staged file is whole, private and synced before anything is put in place.
            seen = Some(std::fs::read_to_string(temporary).unwrap());
            assert!(absent(&plan.native_path().join("config.toml")));
            Err(UNCONFIRMED.into())
        })
        .unwrap_err();
        assert_eq!(error, UNCONFIRMED);
        assert_eq!(seen.as_deref(), Some(canonical(&settings).as_str()));
        assert!(names(&plan).is_empty(), "no config.toml and no temporary file: {:?}", names(&plan));
        assert_eq!(stored(&plan), Ok(None), "the home reads as unset, so a later save is a first save again");
        write_initial(&plan, &settings).unwrap();
        assert_eq!(stored(&plan), Ok(Some(settings)));
        assert_eq!(names(&plan), ["config.toml"]);
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_settings_first_save_never_replaces_an_existing_config() {
        let (root, plan) = fixture();
        let settings = LocalSettings::new("http://127.0.0.1:9100/v1", "org/m").unwrap();
        let earlier = canonical(&LocalSettings::new("http://127.0.0.1:9200/v1", "org/other").unwrap());
        let target = plan.native_path().join("config.toml");
        // A config.toml appearing between the check and the rename: RENAME_EXCL refuses it.
        let error = write_initial_staged(&plan, &settings, |_| {
            std::fs::write(&target, &earlier).unwrap();
            Ok(())
        })
        .unwrap_err();
        assert_eq!(error, CHANGED);
        assert_eq!(std::fs::read_to_string(&target).unwrap(), earlier, "the existing file is untouched");
        assert_eq!(names(&plan), ["config.toml"], "no temporary file left");
        // One already there before the save: refused before anything is staged.
        assert_eq!(write_initial_staged(&plan, &settings, |_| panic!("nothing staged")).unwrap_err(), CHANGED);
        assert_eq!(std::fs::read_to_string(&target).unwrap(), earlier);
        assert_eq!(names(&plan), ["config.toml"]);
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[cfg(all(test, unix))]
mod restore_tests {
    use super::*;
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
    const CANARY: &str = "INVENTED_LOCAL_RESTORE_KEY_CANARY_419";
    fn private_write(path: &std::path::Path, bytes: &str) {
        std::fs::write(path, bytes).unwrap();
        std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o600)).unwrap();
    }
    /// A key entered for A, then config.toml hand-edited to B.
    fn mismatched(key: bool) -> (std::path::PathBuf, OwnedHomePlan, LocalSettings, LocalSettings) {
        let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("local-restore-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let plan = OwnedHomePlan::new(root.clone(), root.join("local"), HomeClass::LocalProvider, None).unwrap();
        let a = LocalSettings::new("http://127.0.0.1:9100/v1", "org/m").unwrap();
        let b = LocalSettings::new("http://127.0.0.1:9200/v1", "org/m").unwrap();
        prepare_for_test(&plan, &a);
        write_key_address(&plan, a.endpoint()).unwrap();
        if key {
            private_write(&plan.native_path().join("auth.json"), CANARY);
        }
        private_write(&plan.native_path().join("config.toml"), &canonical(&b));
        (root, plan, a, b)
    }
    fn file(plan: &OwnedHomePlan) -> String {
        std::fs::read_to_string(plan.native_path().join("config.toml")).unwrap()
    }
    #[test]
    fn native_local_settings_restore_to_the_recorded_address_keeps_the_key_after_confirmation() {
        let (root, plan, a, b) = mismatched(true);
        let auth = plan.native_path().join("auth.json");
        let auth_before = std::fs::metadata(&auth).unwrap();
        let back = LocalSettings::new(a.endpoint(), "org/m").unwrap();
        // Cancel changes nothing; the question says what is done.
        let mut asked = String::new();
        let out = save(&plan, back.clone(), None, || Ok(()), |s, _| { asked = s.text.clone(); Ok(MessageDialogResult::Cancel) }).unwrap();
        assert_eq!(out["outcome"], "cancelled");
        assert_eq!(file(&plan), canonical(&b));
        assert!(asked.contains("set back to http://127.0.0.1:9100/v1, the address the saved key was entered for") && asked.contains("The saved key is kept."), "{asked}");
        assert!(!asked.contains("sign-out") && !asked.contains("entered again") && !asked.contains(CANARY));
        // Confirmed: the address is set back, no sign-out (no home is bound at all here), key kept.
        let out = save(&plan, back.clone(), None, || Ok(()), |s, action| Ok(MessageDialogResult::Custom(if s.text.contains("set back") { action.into() } else { "no".into() }))).unwrap();
        assert_eq!((out["outcome"].as_str(), out["keyRemoved"].as_bool(), out["state"].as_str(), out["reason"].is_null()), (Some("saved"), Some(false), Some("set"), true));
        assert_eq!(file(&plan), canonical(&back));
        assert_eq!(current(&plan).unwrap(), back);
        assert_eq!(std::fs::read(plan.native_path().join(KEY_ADDRESS)).unwrap(), b"http://127.0.0.1:9100/v1\n", "the record is unchanged");
        let auth_after = std::fs::metadata(&auth).unwrap();
        assert_eq!((auth_before.ino(), auth_before.mtime(), auth_before.len()), (auth_after.ino(), auth_after.mtime(), auth_after.len()), "the key's file is not touched");
        // The restore may also carry a model change; the key stays at its own address.
        std::fs::remove_dir_all(root).unwrap();
        let (root, plan, a, _) = mismatched(true);
        let back = LocalSettings::new(a.endpoint(), "org/other").unwrap();
        assert_eq!(save(&plan, back.clone(), None, || Ok(()), |_, action| Ok(MessageDialogResult::Custom(action.into()))).unwrap()["outcome"], "saved");
        assert_eq!(current(&plan).unwrap(), back);
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_settings_restore_is_refused_for_any_other_address_or_an_unestablished_record_or_key() {
        let confirm = |_: &ns::NativeStatement, _: &str| -> Result<MessageDialogResult, String> { panic!("no question that cannot be acted on") };
        // Any other address is an ordinary change: it needs Codex's sign-out in a bound home.
        for other in ["http://127.0.0.1:9300/v1", "http://127.0.0.1:9100/v1/", "http://[::1]:9100/v1", "https://127.0.0.1:9100/v1"] {
            let (root, plan, _, b) = mismatched(true);
            assert_eq!(save(&plan, LocalSettings::new(other, "org/m").unwrap(), None, || Ok(()), confirm).unwrap_err(), PREPARE_FIRST, "{other}");
            assert_eq!(file(&plan), canonical(&b));
            std::fs::remove_dir_all(root).unwrap();
        }
        for case in ["record-missing", "record-malformed", "record-link", "record-mode", "key-absent", "key-link", "key-mode"] {
            let (root, plan, a, b) = mismatched(!case.starts_with("key-absent"));
            let record = plan.native_path().join(KEY_ADDRESS);
            let auth = plan.native_path().join("auth.json");
            match case {
                "record-missing" => std::fs::remove_file(&record).unwrap(),
                "record-malformed" => private_write(&record, "http://127.0.0.1:9100/v1"),
                "record-link" => {
                    std::fs::rename(&record, root.join("elsewhere")).unwrap();
                    std::os::unix::fs::symlink(root.join("elsewhere"), &record).unwrap();
                }
                "record-mode" => std::fs::set_permissions(&record, std::fs::Permissions::from_mode(0o644)).unwrap(),
                "key-absent" => {}
                "key-link" => {
                    std::fs::rename(&auth, root.join("not-read")).unwrap();
                    std::os::unix::fs::symlink(root.join("not-read"), &auth).unwrap();
                }
                "key-mode" => std::fs::set_permissions(&auth, std::fs::Permissions::from_mode(0o644)).unwrap(),
                _ => unreachable!(),
            }
            let back = LocalSettings::new(a.endpoint(), "org/m").unwrap();
            let error = save(&plan, back, None, || Ok(()), confirm).unwrap_err();
            assert!(!error.contains(CANARY), "{case}");
            assert_eq!(file(&plan), canonical(&b), "{case}: nothing written");
            std::fs::remove_dir_all(root).unwrap();
        }
        // The record changing while the person decides refuses the restore without writing.
        let (root, plan, a, b) = mismatched(true);
        let back = LocalSettings::new(a.endpoint(), "org/m").unwrap();
        let record = plan.native_path().join(KEY_ADDRESS);
        let error = save(&plan, back, None, || Ok(()), |_, action| { private_write(&record, "http://127.0.0.1:9200/v1\n"); Ok(MessageDialogResult::Custom(action.into())) }).unwrap_err();
        assert_eq!(error, CHANGED);
        assert_eq!(file(&plan), canonical(&b));
        std::fs::remove_dir_all(root).unwrap();
    }
}
