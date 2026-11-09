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
const CONFIG: &str = "model_provider = \"chirality-omlx\"\nmodel = \"mlx-community/Qwen3.6-35B-A3B-8bit\"\ncli_auth_credentials_store = \"file\"\n[features]\nplugins = false\n[model_providers.chirality-omlx]\nname = \"oMLX\"\nbase_url = \"http://127.0.0.1:8000/v1\"\nwire_api = \"responses\"\nrequires_openai_auth = true\n";

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
    let mut config = base.clone();
    config.codex_home = plan.native_path().into();
    config.session_flags = vec![
        "analytics.enabled=false".into(), "features.plugins=false".into(),
        "cli_auth_credentials_store=\"file\"".into(),
        format!("model_provider=\"{PROVIDER}\""), format!("model=\"{MODEL}\""),
        format!("model_providers.{PROVIDER}={{name=\"oMLX\",base_url=\"{ENDPOINT}\",wire_api=\"responses\",requires_openai_auth=true}}"),
    ];
    Ok(config)
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
    source(home, plan, generation)?;
    let read = home.host.account_read_scoped(generation)?;
    home.account_sources.lock().unwrap().push(read.clone());
    home.host
        .source_request_wait(&read, Duration::from_secs(20))
        .map_err(|_| LIMIT)?;
    let e = read.evidence();
    if e["outcome"] != "response-observed-result"
        || e["authResponseShapeValid"] != true
        || e["response"]["result"]["account"]["type"] != "apiKey"
    {
        return Err(LIMIT.into());
    }
    source(home, plan, generation)?;
    window_current()?;
    Ok(view(generation.clone(), true))
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
