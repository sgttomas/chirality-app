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
pub(crate) const RELAUNCH: &str = "The local model settings changed in this session; quit and reopen the App to use them. The local connection is unavailable until then.";
pub(crate) const EARLIER: &str =
    "This conversation was started under earlier local model settings; it is not continued.";
pub(crate) const PREPARE_FIRST: &str = "Prepare the local connection first, so that Codex can remove the saved key; the local model settings were not changed.";
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
/// The settings the home's file holds now, with every home condition checked.
pub(crate) fn current(plan: &OwnedHomePlan) -> Result<LocalSettings, String> {
    check_home(plan)?;
    read_config(plan)
}
/// Every bound operation: the file must still hold exactly the settings in force for this
/// Codex process. A file changed after binding refuses until the App is reopened.
pub(crate) fn check(plan: &OwnedHomePlan, in_force: &LocalSettings) -> Result<(), String> {
    if current(plan)? != *in_force {
        return Err(RELAUNCH.into());
    }
    Ok(())
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
/// Prepare an already-set home for binding. Never writes settings or defaults.
pub(crate) fn prepare(plan: &OwnedHomePlan) -> Result<LocalSettings, String> {
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
/// First settings: create the home and its config.toml create-only, private and synced.
fn write_initial(plan: &OwnedHomePlan, settings: &LocalSettings) -> Result<(), String> {
    if plan.class() != HomeClass::LocalProvider {
        return Err(LIMIT.into());
    }
    crate::storage::check_path(plan.native_path()).map_err(|_| LIMIT)?;
    #[cfg(unix)]
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
        let mut file = std::fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(plan.native_path().join("config.toml"))
            .map_err(|_| CHANGED)?;
        file.write_all(canonical(settings).as_bytes())
            .map_err(|_| UNCONFIRMED)?;
        file.sync_all().map_err(|_| UNCONFIRMED)?;
        crate::storage::sync_dir(plan.native_path()).map_err(|_| UNCONFIRMED)?;
    }
    #[cfg(not(unix))]
    {
        let _ = settings;
        return Err(LIMIT.into());
    }
    if read_config(plan).ok().as_ref() != Some(settings) {
        return Err(UNCONFIRMED.into());
    }
    Ok(())
}
/// Changed settings: atomic replacement in the same directory. Nothing else in the home is touched.
fn replace(plan: &OwnedHomePlan, before: &LocalSettings, after: &LocalSettings) -> Result<(), String> {
    if current(plan)? != *before {
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
            if current(plan)? != *before {
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
    if current(plan).ok().as_ref() != Some(after) {
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
    Ok(config)
}
/// Codex 0.167 loads administrator configuration (legacy managed_config.toml, requirements.toml and
/// macOS managed preferences) ABOVE session flags, so the fixed flags cannot hold the provider,
/// catalogue or auth settings against it. Fail closed on presence; never parse or copy contents.
const ADMIN_FILES: &[&str] = &["/etc/codex/managed_config.toml", "/etc/codex/requirements.toml"];
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
    let settings = home.host.local_settings()?;
    check(plan, &settings)?;
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
    entry: impl FnOnce() -> Result<Option<String>, ()>,
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
    let _proof = home
        .host
        .provider_admission_read(generation, cwd, ENTRY, PROVIDER, &settings.model)?;
    let policy = home.host.account_requirements_read_scoped(generation)?;
    home.account_sources.lock().unwrap().push(policy.clone());
    home.host
        .source_request_wait(&policy, Duration::from_secs(20))
        .map_err(|_| LIMIT)?;
    source(home, plan, generation)?;
    window_current()?;
    // Consumed even on cancel or unknown outcome. A replacement source is a separate explicit act.
    entry_state.begin(generation)?;
    let request = home
        .host
        .account_login_api_key_from_native_entry(generation, Some(&policy), || {
            let input = entry()?;
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
/// moves or deletes auth.json itself.
fn sign_out(home: &HomeSession, plan: &OwnedHomePlan, generation: &Value, wait: Duration) -> Result<(), String> {
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
    Ok(())
}
/// The read the web view calls: the App-owned file only; nothing is started.
pub(crate) fn settings_view(
    stored: Result<Option<LocalSettings>, String>,
    in_force: Option<&LocalSettings>,
) -> Value {
    let (state, settings) = match &stored {
        Ok(None) => ("unset", None),
        Ok(Some(settings)) => ("set", Some(settings)),
        Err(_) => ("unavailable", None),
    };
    json!({"state":state,"settings":settings.map(LocalSettings::json),"offered":{"endpoint":OFFERED_ENDPOINT},"inForce":in_force.map(LocalSettings::json),"relaunchRequired":matches!((settings,in_force),(Some(s),Some(f)) if s!=f)})
}
fn effects(
    before: Option<&LocalSettings>,
    after: &LocalSettings,
    sign_out: bool,
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
    let outcome = |outcome: &str, removed: bool| {
        let mut view = settings_view(stored(plan), in_force.as_ref());
        view["outcome"] = json!(outcome);
        view["keyRemoved"] = json!(removed);
        view
    };
    let before = stored(plan)?;
    if before.as_ref() == Some(&proposed) {
        return Ok(outcome("unchanged", false));
    }
    if before.is_none() && (in_use.is_some() || !absent(&plan.native_path().join("auth.json"))) {
        return Err(LIMIT.into());
    }
    let needs_sign_out = before
        .as_ref()
        .is_some_and(|b| b.endpoint != proposed.endpoint);
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
    let statement = effects(before.as_ref(), &proposed, needs_sign_out, in_use.is_some())?;
    let result = ns::showing_in_app(statement.in_app.as_ref(), || confirm(&statement, SAVE_ACTION))?;
    if !ns::chose(&result, SAVE_ACTION) {
        return Ok(outcome("cancelled", false));
    }
    window_current()?;
    if stored(plan)? != before {
        return Err(CHANGED.into());
    }
    if let Some((home, generation)) = &signing {
        let (again, now) = ready()?;
        if !std::ptr::eq(again, *home) || now != *generation {
            return Err(PREPARE_FIRST.into());
        }
        sign_out(home, plan, generation, wait)?;
    }
    let written = match &before {
        None => write_initial(plan, &proposed),
        Some(before) => replace(plan, before, &proposed),
    };
    // Codex's removal of the key is already observed; never let a write failure hide it.
    written.map_err(|error| {
        if signing.is_some() {
            format!("Codex removed the saved key; {error}")
        } else {
            error
        }
    })?;
    Ok(outcome("saved", signing.is_some()))
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
        let view = settings_view(stored(&plan), None);
        assert_eq!(view, json!({"state":"unset","settings":null,"offered":{"endpoint":"http://127.0.0.1:8000/v1"},"inForce":null,"relaunchRequired":false}));
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
        assert!(names.iter().all(|n| ["config.toml", "auth.lock", "auth.json"].contains(&n.as_str())), "no temporary left: {names:?}");
        assert!(!format!("{out}{asked}").contains(CANARY));
        // A file changed after binding refuses every bound check until the App binds again.
        assert_eq!(check(&plan, &LocalSettings::legacy()).unwrap_err(), RELAUNCH);
        assert!(check(&plan, &next).is_ok());
        let view = settings_view(stored(&plan), Some(&LocalSettings::legacy()));
        assert_eq!(view["relaunchRequired"], true);
        assert_eq!(view["inForce"], LocalSettings::legacy().json());
        assert_eq!(settings_view(stored(&plan), Some(&next))["relaunchRequired"], false);
        std::fs::write(plan.native_path().join("config.toml"), "hand edited\n").unwrap();
        let view = settings_view(stored(&plan), Some(&next));
        assert_eq!((view["state"].as_str(), view["settings"].is_null()), (Some("unavailable"), true));
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn native_local_settings_question_states_every_consequence_and_requires_the_original_window() {
        let before = LocalSettings::legacy();
        let after = LocalSettings::new("http://[::1]:9000/v1", "other").unwrap();
        let s = effects(Some(&before), &after, true, true).unwrap();
        for part in ["Server address: http://127.0.0.1:8000/v1, changes to http://[::1]:9000/v1", "Model name: mlx-community/Qwen3.6-35B-A3B-8bit, changes to other", "Codex's own sign-out", "must be entered again", "model name other continue, with the server at the new address", "including mlx-community/Qwen3.6-35B-A3B-8bit, will not be continued", "quit and reopen", "never one of these settings"] {
            assert!(s.text.contains(part), "{part}");
        }
        let long = LocalSettings::new(&format!("http://127.0.0.1/{}", "a".repeat(1900)), "m").unwrap();
        let s = effects(Some(&before), &long, true, false).unwrap();
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
}
