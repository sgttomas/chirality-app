//! Synthetic Root descriptors and actual consuming helpers; no native secure
//! panel, credential store or supplier invoked. Private-pipeline joins are Core tests.
use chirality_app_v4_lib::{
    home_resources::HomeClass,
    hosting::{Host, HostConfig},
    runtime_session::{freeze_root_home_descriptors, HomeRouter, HomeSession},
};
use std::{path::PathBuf, sync::Arc};
struct Fixture {
    root: PathBuf,
    data: PathBuf,
    cfg: HostConfig,
    targets: [Option<PathBuf>; 3],
}
impl Fixture {
    fn new() -> Self {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(format!(
                "chirality-access-consumer-{}",
                chirality_app_v4_lib::util::opaque_id("fixture:").unwrap()
            ));
        let data = root.join("app");
        let account = root.join("existing-account");
        let probe = root.join("outside-probe");
        let user = root.join("supplied-resources");
        for path in [&data, &account, &probe, &user] {
            std::fs::create_dir_all(path).unwrap();
        }
        let config = user.join("config.toml");
        let agents = user.join("AGENTS.md");
        let skills = user.join("skills");
        std::fs::write(&config, b"model = 'synthetic-user-choice'\n").unwrap();
        std::fs::write(&agents, b"synthetic user guidance\n").unwrap();
        std::fs::create_dir(&skills).unwrap();
        let cfg = HostConfig::new(
            root.join("never-executed-supplier"),
            account,
            probe,
            root.join("native-cwd-distinct"),
        );
        Self {
            root,
            data,
            cfg,
            targets: [Some(config), Some(agents), Some(skills)],
        }
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
#[test]
fn explicit_existing_account_outside_probe_and_owned_key_do_not_relocate_or_copy() {
    let fixture = Fixture::new();
    let key = fixture.data.join("key-home");
    let set = freeze_root_home_descriptors(
        &fixture.data,
        &fixture.cfg,
        Some(key.clone()),
        fixture.targets.clone(),
    )
    .unwrap();
    assert!(!key.exists());
    let before = fixture.targets[..2]
        .iter()
        .map(|p| std::fs::read(p.as_ref().unwrap()).unwrap())
        .collect::<Vec<_>>();
    set.prepare_key().unwrap();
    assert!(fixture.cfg.codex_home.is_dir());
    assert!(fixture.cfg.probe_home.is_dir());
    for (name, target) in ["config.toml", "AGENTS.md", "skills"]
        .iter()
        .zip(fixture.targets.iter())
    {
        assert_eq!(
            std::fs::read_link(key.join(name)).unwrap(),
            *target.as_ref().unwrap()
        );
    }
    assert!(!key.join("auth.json").exists());
    assert!(!key.join("sessions").exists());
    assert_eq!(
        before,
        fixture.targets[..2]
            .iter()
            .map(|p| std::fs::read(p.as_ref().unwrap()).unwrap())
            .collect::<Vec<_>>()
    );
    let mut key_config = fixture.cfg.clone();
    key_config.codex_home = key.clone();
    set.validate_binding(HomeClass::ApiKey, &key_config)
        .unwrap();
    assert!(set
        .validate_binding(HomeClass::Account, &key_config)
        .is_err());
    assert_eq!(set.inspect()["keyConfigured"], true);
    assert!(set.inspect()["existingAccountResources"]
        .as_str()
        .unwrap()
        .contains("not established"));
}
#[test]
fn absence_invalid_key_and_whole_actual_set_changes_never_fall_back() {
    let fixture = Fixture::new();
    let absent =
        freeze_root_home_descriptors(&fixture.data, &fixture.cfg, None, [None, None, None])
            .unwrap();
    assert!(absent.key_plan().is_err());
    assert_eq!(absent.inspect()["keyConfigured"], false);
    assert!(freeze_root_home_descriptors(
        &fixture.data,
        &fixture.cfg,
        Some(fixture.root.join("outside-owned-root")),
        fixture.targets.clone()
    )
    .is_err());
    assert!(freeze_root_home_descriptors(
        &fixture.data,
        &fixture.cfg,
        Some(fixture.data.join("key")),
        [None, None, None]
    )
    .is_err());
    let mut overlap = fixture.cfg.clone();
    overlap.probe_home = fixture.cfg.codex_home.clone();
    assert!(freeze_root_home_descriptors(
        &fixture.data,
        &overlap,
        Some(fixture.data.join("key")),
        fixture.targets.clone()
    )
    .is_err());
    let set = freeze_root_home_descriptors(
        &fixture.data,
        &fixture.cfg,
        Some(fixture.data.join("key")),
        fixture.targets.clone(),
    )
    .unwrap();
    #[cfg(unix)]
    {
        std::fs::remove_dir(&fixture.cfg.probe_home).unwrap();
        std::os::unix::fs::symlink(&fixture.cfg.codex_home, &fixture.cfg.probe_home).unwrap();
        assert!(set.prepare_key().is_err());
        assert!(!fixture.data.join("key").exists());
        assert!(set
            .validate_binding(HomeClass::Account, &fixture.cfg)
            .is_err());
    }
}
#[test]
fn active_home_choice_retains_original_private_sources_and_has_no_unknown_fallback() {
    let fixture = Fixture::new();
    let account = Arc::new(
        HomeSession::new(
            HomeClass::Account,
            Arc::new(Host::new()),
            Ok(fixture.cfg.clone()),
        )
        .unwrap(),
    );
    let mut router = HomeRouter::new(account.clone()).unwrap();
    assert!(router.activate(HomeClass::ApiKey).is_err());
    assert!(router.activate(HomeClass::Probe).is_err());
    let mut config = fixture.cfg.clone();
    config.codex_home = fixture.data.join("key");
    let unrelated = Arc::new(
        HomeSession::new(HomeClass::ApiKey, Arc::new(Host::new()), Ok(config.clone())).unwrap(),
    );
    assert!(router.bind_key(unrelated).is_err());
    let peer = Host::new_with_app_custody(account.source().app_runtime_custody().unwrap()).unwrap();
    let key = Arc::new(HomeSession::new(HomeClass::ApiKey, Arc::new(peer), Ok(config)).unwrap());
    router.bind_key(key.clone()).unwrap();
    router.activate(HomeClass::ApiKey).unwrap();
    assert!(Arc::ptr_eq(router.active().source(), key.source()));
    assert!(Arc::ptr_eq(
        router.entry(HomeClass::Account).unwrap().source(),
        account.source()
    ));
    assert!(router.bind_key(key).is_err());
    assert!(router
        .for_generation(
            &serde_json::json!({"appSession":"unobserved","home":"foreign","spawnCounter":1})
        )
        .is_err());
    assert!(router
        .for_generation(&serde_json::json!({"home":"account"}))
        .is_err());
    router.activate(HomeClass::Account).unwrap();
    assert!(Arc::ptr_eq(router.active().source(), account.source()));
}

#[test]
fn fresh_probe_resolves_allocation_parent_without_relocating_existing_references() {
    let fixture = Fixture::new();
    #[cfg(unix)]
    {
        let alias = fixture.root.join("os-temp-alias");
        std::os::unix::fs::symlink(&fixture.cfg.probe_home, &alias).unwrap();
        let probe = chirality_app_v4_lib::runtime_session::allocate_fresh_probe(&alias).unwrap();
        assert_eq!(probe.parent(), Some(fixture.cfg.probe_home.as_path()));
        assert!(probe.is_dir());
        assert!(fixture.cfg.probe_home.is_dir());
        assert_eq!(std::fs::read_link(&alias).unwrap(), fixture.cfg.probe_home);
        assert!(chirality_app_v4_lib::runtime_session::allocate_fresh_probe(
            &fixture.root.join("missing-parent")
        )
        .is_err());
    }
}
