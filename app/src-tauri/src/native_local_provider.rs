//! The selected oMLX route. Nonsecret configuration is App-owned; only Codex writes auth.json.
//! This module never reads a credential, retries a credential frame or accepts one from IPC.
use crate::{
    home_resources::{HomeClass, OwnedHomePlan},
    hosting::HostConfig,
    runtime_session::HomeSession,
};
use serde_json::{json, Value};
use std::{io::Write, path::Path, sync::Mutex, time::Duration};

pub(crate) const PROVIDER: &str = "chirality-omlx";
pub(crate) const ENDPOINT: &str = "http://127.0.0.1:8000/v1";
pub(crate) const MODEL: &str = "mlx-community/Qwen3.6-35B-A3B-8bit";
pub(crate) const ENTRY: &str = "local-provider-keyed";
pub(crate) const LIMIT: &str =
    "Local oMLX source unavailable; no fallback or automatic credential retry";
const CONFIG: &str = "model_provider = \"chirality-omlx\"\nmodel = \"mlx-community/Qwen3.6-35B-A3B-8bit\"\ncli_auth_credentials_store = \"file\"\n[features]\nplugins = false\napi_key_model_discovery = false\n[model_providers.chirality-omlx]\nname = \"oMLX\"\nbase_url = \"http://127.0.0.1:8000/v1\"\nwire_api = \"responses\"\nrequires_openai_auth = true\n";

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
/// Check metadata only for Codex credential slots; never parse or copy their contents.
pub(crate) fn check(plan: &OwnedHomePlan) -> Result<(), String> {
    if plan.class() != HomeClass::LocalProvider {
        return Err(LIMIT.into());
    }
    crate::storage::check_path(plan.native_path()).map_err(|_| LIMIT)?;
    private_metadata(plan.native_path(), true)?;
    let config = plan.native_path().join("config.toml");
    private_metadata(&config, false)?;
    if std::fs::read(config).map_err(|_| LIMIT)? != CONFIG.as_bytes() {
        return Err(LIMIT.into());
    }
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
pub(crate) fn prepare(plan: &OwnedHomePlan) -> Result<(), String> {
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
        let path = plan.native_path().join("config.toml");
        match std::fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(&path)
        {
            Ok(mut file) => {
                file.write_all(CONFIG.as_bytes()).map_err(|_| LIMIT)?;
                file.sync_all().map_err(|_| LIMIT)?;
                crate::storage::sync_dir(plan.native_path())?;
            }
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(_) => return Err(LIMIT.into()),
        }
    }
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
    check(plan)
}
/// Whole-provider replacement at highest config precedence prevents project/default routing drift.
/// All flags are fixed nonsecret source text. No inherited account session overrides are copied.
pub(crate) fn config(base: &HostConfig, plan: &OwnedHomePlan) -> Result<HostConfig, String> {
    check(plan)?;
    require_no_admin_layers()?;
    let mut config = base.clone();
    config.codex_home = plan.native_path().into();
    config.process_lock = Some(plan.native_path().join(PROCESS_LOCK));
    config.session_flags = vec![
        "analytics.enabled=false".into(), "features.plugins=false".into(),
        // Session flags merge into lower layers; a foreign catalogue URL must never receive the home key.
        "features.api_key_model_discovery=false".into(),
        "cli_auth_credentials_store=\"file\"".into(),
        format!("model_provider=\"{PROVIDER}\""), format!("model=\"{MODEL}\""),
        format!("model_providers.{PROVIDER}={{name=\"oMLX\",base_url=\"{ENDPOINT}\",wire_api=\"responses\",requires_openai_auth=true}}"),
    ];
    Ok(config)
}
/// App-owned lock file in every Codex home the App starts Codex on. A Codex the App starts there
/// inherits the locked descriptor, so the lock is held while that Codex, or anything it started
/// that kept the descriptor, lives. Not auth.lock, not Codex's.
pub(crate) const PROCESS_LOCK: &str = "chirality-codex-process.lock";
/// What a held lock establishes is only that something holds it: the sentence names what may,
/// and asserts neither which nor for how long.
pub(crate) const EARLIER_PROCESS: &str = "The App's lock for the local model home is held, so Codex was not started there. A Codex process started earlier for that home, a program it started, or another copy of the App may hold it. Try again in a minute. If it stays held, whatever holds it has to end before Codex can start there; the App cannot tell which program it is.";
/// The refusal when the App cannot open or lock its lock file at all.
pub(crate) const PROCESS_LOCK_UNAVAILABLE: &str = "The App could not check that no earlier Codex process for the local model home is running, so Codex was not started there.";
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
pub(crate) fn fixed_selection(entry: &str, provider: &str, model: &str) -> Result<(), String> {
    if entry != ENTRY || provider != PROVIDER || model != MODEL {
        return Err(LIMIT.into());
    }
    Ok(())
}
pub(crate) fn view(generation: Value, configured: bool) -> Value {
    json!({"modeHomeClass":"local-provider","entryId":ENTRY,"providerId":PROVIDER,"endpoint":ENDPOINT,"model":MODEL,"generation":generation,"credentialState":if configured {"configured-not-verified"} else {"entry-required"},"credentialCustody":"Codex auth.json in the dedicated local home; App never reads it","validity":"not verified by configuration, login acknowledgment or account type"})
}
fn source(home: &HomeSession, plan: &OwnedHomePlan, generation: &Value) -> Result<(), String> {
    check(plan)?;
    require_no_admin_layers()?;
    if generation["home"] != plan.opaque_home_id()
        || home.class() != HomeClass::LocalProvider
        || home.host_config.as_ref().map_err(|_| LIMIT)?.codex_home != plan.native_path()
    {
        return Err(LIMIT.into());
    }
    crate::runtime_session::check_start_source(home, generation).map_err(|_| LIMIT)?;
    home.host.require_local_destination(generation)
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
    source(home, plan, generation)?;
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
        .provider_admission_read(generation, cwd, ENTRY, PROVIDER, MODEL)?;
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
        return Ok(view(generation.clone(), false));
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
/// Codex's own account report for this exact local generation: `account/read` with
/// `refreshToken:false`. Only the reported account kind is used. The App never opens auth.json,
/// sees a key or claims validity. No account means entry is required; an error, a stale source,
/// an unestablished reply or any non-API-key account refuses without a state claim.
pub(crate) fn observe(
    home: &HomeSession,
    plan: &OwnedHomePlan,
    generation: &Value,
) -> Result<Value, String> {
    source(home, plan, generation)?;
    let read = home.host.account_read_no_refresh_scoped(generation)?;
    home.account_sources.lock().unwrap().push(read.clone());
    home.host
        .source_request_wait(&read, Duration::from_secs(20))
        .map_err(|_| LIMIT)?;
    let e = read.evidence();
    if e["outcome"] != "response-observed-result"
        || e["authResponseShapeValid"] != true
        || e["sourceCurrent"] != true
        || e["response"]["result"].get("account").is_none()
    {
        return Err(LIMIT.into());
    }
    let configured = match &e["response"]["result"]["account"] {
        Value::Null => false,
        account if account["type"] == "apiKey" => true,
        _ => return Err(LIMIT.into()),
    };
    source(home, plan, generation)?;
    Ok(view(generation.clone(), configured))
}

#[cfg(all(test, unix))]
mod tests {
    use super::*;
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
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
    /// The typed route: the dedicated local home is bound only with its own lock file's path.
    #[test]
    fn local_process_lock_binding_requires_the_homes_own_lock_path() {
        let (root, plan) = fixture();
        prepare(&plan).unwrap();
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
    #[test]
    fn native_local_provider_fixed_nonsecret_config_is_private_create_only_and_has_no_account_links(
    ) {
        let (root, plan) = fixture();
        prepare(&plan).unwrap();
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
        for v in ["openai", "", "another-provider"] {
            assert!(fixed_selection(ENTRY, v, MODEL).is_err());
        }
        for v in ["", "different-model"] {
            assert!(fixed_selection(ENTRY, PROVIDER, v).is_err());
        }
        assert!(fixed_selection("api-key", PROVIDER, MODEL).is_err());
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
        assert!(CONFIG.contains("[features]\nplugins = false\napi_key_model_discovery = false\n"));
        let (root, plan) = fixture();
        prepare(&plan).unwrap();
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
            prepare(&plan).unwrap();
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
            assert!(check(&plan).is_err(), "{case}");
            assert!(
                prepare(&plan).is_err(),
                "{case}: no chmod/migration/overwrite"
            );
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
        let dto = view(g, true);
        assert_eq!(dto["credentialState"], "configured-not-verified");
        assert_eq!(dto["modeHomeClass"], "local-provider");
        assert_eq!(dto["entryId"], ENTRY);
        assert!(!dto.to_string().contains("apiKey"));
    }
}
