#![cfg(unix)]
use chirality_app_v4_lib::storage;
#[path = "../src/home_resources.rs"]
mod home_resources;
use home_resources::*;
use std::os::unix::{ffi::OsStringExt, fs::symlink};
use std::{path::PathBuf, process::Command};

struct Fixture(PathBuf);
impl Fixture {
    fn new() -> Self {
        // Synthetic candidate-home fixture only. Never ambient ~/.codex or a real credential root.
        let template = std::env::temp_dir().join("chirality-home-resources-XXXXXX");
        let output = Command::new("mktemp")
            .arg("-d")
            .arg(template)
            .output()
            .unwrap();
        assert!(output.status.success());
        let path = PathBuf::from(String::from_utf8(output.stdout).unwrap().trim());
        Self(std::fs::canonicalize(path).unwrap())
    }
    fn app(&self) -> PathBuf {
        self.0.join("app-data")
    }
    fn shared(&self) -> SharedResourceTargets {
        let root = self.0.join("synthetic-native-resources");
        std::fs::create_dir_all(root.join("skills")).unwrap();
        std::fs::write(root.join("config.toml"), b"# synthetic fixture, not a product default\nmodel_provider = \"fixture-provider\"\n[features]\nplugins = true\n").unwrap();
        std::fs::write(
            root.join("AGENTS.md"),
            b"Synthetic global guidance; no credential.\n",
        )
        .unwrap();
        std::fs::write(root.join("skills/fixture.txt"), b"synthetic skill\n").unwrap();
        std::fs::write(
            root.join("auth.json"),
            b"synthetic private sentinel; not a credential\n",
        )
        .unwrap();
        SharedResourceTargets {
            config_toml: root.join("config.toml"),
            global_agents_md: root.join("AGENTS.md"),
            skills: root.join("skills"),
        }
    }
    fn plan(
        &self,
        name: &str,
        class: HomeClass,
        shared: Option<SharedResourceTargets>,
    ) -> OwnedHomePlan {
        OwnedHomePlan::new(self.app(), self.app().join(name), class, shared).unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        std::fs::remove_dir_all(&self.0).unwrap();
    }
}

#[test]
fn account_and_key_share_only_explicit_resources_and_remain_distinct() {
    let f = Fixture::new();
    let sources = f.shared();
    let original = std::fs::read(&sources.config_toml).unwrap();
    let account = f.plan("account", HomeClass::Account, Some(sources.clone()));
    let key = f.plan("key", HomeClass::ApiKey, Some(sources.clone()));
    validate_distinct_account_homes(&account, &key).unwrap();
    for plan in [&account, &key] {
        let observed = plan.prepare().unwrap();
        assert_eq!(observed.resources.len(), 3);
        assert!(observed
            .resources
            .iter()
            .all(|r| r.state == ResourceState::Linked));
        assert_eq!(
            std::fs::read(plan.native_path().join("config.toml")).unwrap(),
            original
        );
        assert!(!plan.native_path().join("auth.json").exists());
        assert!(!plan.native_path().join("sessions").exists());
        assert_eq!(observed.native_path, plan.native_path());
        assert_ne!(observed.opaque_home_id, plan.class().as_str());
    }
    assert_ne!(account.opaque_home_id(), key.opaque_home_id());
    assert_eq!(std::fs::read(&sources.config_toml).unwrap(), original);
    assert_eq!(
        std::fs::read(sources.skills.join("fixture.txt")).unwrap(),
        b"synthetic skill\n"
    );
    assert_eq!(std::fs::read_dir(key.native_path()).unwrap().count(), 3);
    assert!(key
        .prepare()
        .unwrap()
        .resources
        .iter()
        .all(|r| r.state == ResourceState::Linked));
}

#[test]
fn same_nested_and_symlink_aliased_homes_are_not_two_accounts() {
    let f = Fixture::new();
    let s = f.shared();
    let account = f.plan("account", HomeClass::Account, Some(s.clone()));
    let same = f.plan("account", HomeClass::ApiKey, Some(s.clone()));
    assert!(validate_distinct_account_homes(&account, &same).is_err());
    let nested = OwnedHomePlan::new(
        f.app(),
        f.app().join("account/key"),
        HomeClass::ApiKey,
        Some(s.clone()),
    )
    .unwrap();
    assert!(validate_distinct_account_homes(&account, &nested).is_err());
    account.prepare().unwrap();
    symlink(account.native_path(), f.app().join("alias")).unwrap();
    assert!(
        OwnedHomePlan::new(f.app(), f.app().join("alias"), HomeClass::ApiKey, Some(s)).is_err()
    );
    assert!(std::fs::symlink_metadata(f.app().join("alias"))
        .unwrap()
        .file_type()
        .is_symlink());
}

#[test]
fn missing_targets_are_visible_and_never_copied_or_claimed_verified() {
    let f = Fixture::new();
    let root = f.0.join("missing-native-resources");
    let sources = SharedResourceTargets {
        config_toml: root.join("config.toml"),
        global_agents_md: root.join("AGENTS.md"),
        skills: root.join("skills"),
    };
    let key = f.plan("key", HomeClass::ApiKey, Some(sources));
    let observed = key.prepare().unwrap();
    assert!(observed
        .resources
        .iter()
        .all(|r| r.state == ResourceState::TargetMissing));
    assert!(key.resolved_config_write_target().is_err());
    assert!(!root.exists());
}

#[test]
fn foreign_links_and_ordinary_files_are_preserved_without_remap() {
    let f = Fixture::new();
    let s = f.shared();
    let key = f.plan("key", HomeClass::ApiKey, Some(s.clone()));
    std::fs::create_dir_all(key.native_path()).unwrap();
    let other = f.0.join("other-config.toml");
    std::fs::write(&other, b"foreign synthetic config").unwrap();
    symlink(&other, key.native_path().join("config.toml")).unwrap();
    std::fs::write(
        key.native_path().join("AGENTS.md"),
        b"local synthetic guidance",
    )
    .unwrap();
    let out = key.prepare().unwrap();
    assert_eq!(out.resources[0].state, ResourceState::Conflict);
    assert_eq!(out.resources[1].state, ResourceState::Conflict);
    assert_eq!(
        std::fs::read_link(key.native_path().join("config.toml")).unwrap(),
        other
    );
    assert_eq!(
        std::fs::read(key.native_path().join("AGENTS.md")).unwrap(),
        b"local synthetic guidance"
    );
    assert!(key.resolved_config_write_target().is_err());
}

#[test]
fn resolved_config_target_is_current_observation_and_broken_link_stays_broken() {
    let f = Fixture::new();
    let mut s = f.shared();
    let managed = s.config_toml.parent().unwrap().join("managed.toml");
    std::fs::rename(&s.config_toml, &managed).unwrap();
    symlink(&managed, &s.config_toml).unwrap();
    let key = f.plan("key", HomeClass::ApiKey, Some(s.clone()));
    key.prepare().unwrap();
    assert_eq!(
        key.resolved_config_write_target().unwrap(),
        std::fs::canonicalize(&managed).unwrap()
    );
    std::fs::remove_file(key.native_path().join("config.toml")).unwrap();
    std::fs::write(
        key.native_path().join("config.toml"),
        b"replacement local synthetic config",
    )
    .unwrap();
    assert!(key.resolved_config_write_target().is_err());
    assert_eq!(
        key.prepare().unwrap().resources[0].state,
        ResourceState::Conflict
    );
    assert_eq!(
        std::fs::read(key.native_path().join("config.toml")).unwrap(),
        b"replacement local synthetic config"
    );
    s.skills = managed; // explicit wrong-kind fixture; no target content is read by module.
    let wrong = f.plan("wrong-kind", HomeClass::ApiKey, Some(s));
    assert_eq!(
        wrong.prepare().unwrap().resources[2].state,
        ResourceState::TargetTypeMismatch
    );
}

#[test]
fn probe_and_unestablished_inputs_never_acquire_shared_settings() {
    let f = Fixture::new();
    let s = f.shared();
    assert!(OwnedHomePlan::new(f.app(), f.app().join("key"), HomeClass::ApiKey, None).is_err());
    assert!(OwnedHomePlan::new(
        f.app(),
        f.app().join("probe"),
        HomeClass::Probe,
        Some(s.clone())
    )
    .is_err());
    assert!(OwnedHomePlan::new(
        f.app(),
        f.0.join("outside"),
        HomeClass::ApiKey,
        Some(s.clone())
    )
    .is_err());
    assert!(OwnedHomePlan::new(
        f.app(),
        f.app().join("key/../alias"),
        HomeClass::ApiKey,
        Some(s)
    )
    .is_err());
    let probe = f.plan("probe", HomeClass::Probe, None);
    let out = probe.prepare().unwrap();
    assert!(out
        .resources
        .iter()
        .all(|r| r.state == ResourceState::NotSupplied));
    assert_eq!(std::fs::read_dir(probe.native_path()).unwrap().count(), 0);
    assert!(probe.resolved_config_write_target().is_err());
}

#[test]
fn owning_directory_redirection_is_refused_without_relocation() {
    let f = Fixture::new();
    let s = f.shared();
    let key = f.plan("key", HomeClass::ApiKey, Some(s));
    std::fs::create_dir_all(f.app()).unwrap();
    let foreign = f.0.join("foreign");
    std::fs::create_dir(&foreign).unwrap();
    symlink(&foreign, key.native_path()).unwrap();
    assert!(key.prepare().is_err());
    assert_eq!(std::fs::read_dir(&foreign).unwrap().count(), 0);
}

#[test]
fn native_path_bytes_not_lossy_display_determine_home_identity() {
    let f = Fixture::new();
    let s = f.shared();
    let a = f
        .app()
        .join(std::ffi::OsString::from_vec(b"home-\xff".to_vec()));
    let b = f
        .app()
        .join(std::ffi::OsString::from_vec(b"home-\xfe".to_vec()));
    let pa = OwnedHomePlan::new(f.app(), a.clone(), HomeClass::Account, Some(s.clone())).unwrap();
    let pb = OwnedHomePlan::new(f.app(), b.clone(), HomeClass::ApiKey, Some(s)).unwrap();
    assert_eq!(a.display().to_string(), b.display().to_string());
    assert_ne!(pa.opaque_home_id(), pb.opaque_home_id());
    assert_eq!(pa.native_path(), a);
    assert_eq!(pb.native_path(), b);
    // Pure OS-string identity check; no claim the host FS accepted these invalid-byte names.
}

#[test]
fn probe_is_also_a_distinct_private_home_at_root_binding() {
    let f = Fixture::new();
    let s = f.shared();
    let account = f.plan("account", HomeClass::Account, Some(s.clone()));
    let key = f.plan("key", HomeClass::ApiKey, Some(s));
    let probe_same = f.plan("key", HomeClass::Probe, None);
    assert!(validate_distinct_homes(&[&account, &key, &probe_same]).is_err());
    let probe = f.plan("probe", HomeClass::Probe, None);
    validate_distinct_homes(&[&account, &key, &probe]).unwrap();
    for h in [&account, &key, &probe] {
        h.prepare().unwrap();
    }
    validate_distinct_homes(&[&account, &key, &probe]).unwrap();
    // When the fixture filesystem folds case, distinct spellings must still refuse the same directory.
    let alternate =
        OwnedHomePlan::new(f.app(), f.app().join("ACCOUNT"), HomeClass::Probe, None).unwrap();
    if std::fs::canonicalize(alternate.native_path()).ok()
        == std::fs::canonicalize(account.native_path()).ok()
    {
        assert!(validate_distinct_homes(&[&account, &alternate]).is_err());
    }
    symlink(probe.native_path(), f.app().join("probe-alias")).unwrap();
    assert!(
        OwnedHomePlan::new(f.app(), f.app().join("probe-alias"), HomeClass::Probe, None).is_err()
    );
}

#[test]
fn missing_descendant_of_existing_alias_is_not_a_separate_home() {
    let f = Fixture::new();
    let sources = f.shared();
    let account = f.plan("account", HomeClass::Account, Some(sources.clone()));
    account.prepare().unwrap();
    let alias_parent = f.app().join("ACCOUNT");
    // Filesystem-conditioned fixture: assert real native identity before testing the alias branch.
    if alias_parent.is_dir() {
        use std::os::unix::fs::MetadataExt;
        let a = std::fs::metadata(account.native_path()).unwrap();
        let b = std::fs::metadata(&alias_parent).unwrap();
        assert_eq!((a.dev(), a.ino()), (b.dev(), b.ino()));
        let key = OwnedHomePlan::new(
            f.app(),
            alias_parent.join("new-key"),
            HomeClass::ApiKey,
            Some(sources.clone()),
        )
        .unwrap();
        assert!(validate_distinct_account_homes(&account, &key).is_err());
        assert!(validate_distinct_homes(&[&account, &key]).is_err());
    }
    let unrelated = f.plan("unrelated-missing-key", HomeClass::ApiKey, Some(sources));
    validate_distinct_account_homes(&account, &unrelated).unwrap();
    unrelated.prepare().unwrap();
    validate_distinct_account_homes(&account, &unrelated).unwrap();
}

#[test]
fn missing_resource_beneath_existing_receiving_alias_is_refused_before_setup() {
    let f = Fixture::new();
    let mut sources = f.shared();
    let receiving = f.app().join("receiving");
    std::fs::create_dir_all(&receiving).unwrap();
    let alias = f.app().join("RECEIVING");
    if alias.is_dir() {
        use std::os::unix::fs::MetadataExt;
        let a = std::fs::metadata(&receiving).unwrap();
        let b = std::fs::metadata(&alias).unwrap();
        assert_eq!((a.dev(), a.ino()), (b.dev(), b.ino()));
        sources.config_toml = alias.join("config.toml");
        assert!(OwnedHomePlan::new(f.app(), receiving, HomeClass::ApiKey, Some(sources)).is_err());
    }
}

#[test]
fn setup_rechecks_missing_source_alias_and_dangling_external_resources_stay_visible() {
    let f = Fixture::new();
    let mut sources = f.shared();
    let outside = f.0.join("not-yet-source");
    sources.config_toml = outside.join("config.toml");
    let key = f.plan("key", HomeClass::ApiKey, Some(sources));
    std::fs::create_dir_all(key.native_path()).unwrap();
    symlink(key.native_path(), &outside).unwrap();
    assert!(key.prepare().is_err());
    assert_eq!(std::fs::read_dir(key.native_path()).unwrap().count(), 0);
    std::fs::remove_file(&outside).unwrap();
    symlink(f.0.join("missing-external-source"), &outside).unwrap();
    assert_eq!(
        key.prepare().unwrap().resources[0].state,
        ResourceState::TargetMissing
    );
    assert_eq!(
        std::fs::read_link(key.native_path().join("config.toml")).unwrap(),
        outside.join("config.toml")
    );
}

#[test]
fn received_existing_account_and_probe_are_not_reallocated_into_app_data() {
    let f = Fixture::new();
    let sources = f.shared();
    let account_path = f.0.join("explicit-existing-account");
    let probe_path = f.0.join("explicit-existing-probe");
    std::fs::create_dir(&account_path).unwrap();
    std::fs::create_dir(&probe_path).unwrap();
    std::fs::write(
        account_path.join("private-fixture-sentinel"),
        b"unchanged synthetic data",
    )
    .unwrap();
    let account = ExistingHomeReference::new(account_path.clone(), HomeClass::Account).unwrap();
    let probe = ExistingHomeReference::new(probe_path.clone(), HomeClass::Probe).unwrap();
    let key = f.plan("new-key", HomeClass::ApiKey, Some(sources));
    let bindings = [
        HomeBinding::Existing(&account),
        HomeBinding::Existing(&probe),
        HomeBinding::Owned(&key),
    ];
    validate_home_bindings(&bindings).unwrap();
    key.prepare().unwrap();
    validate_home_bindings(&bindings).unwrap();
    for reference in [&account, &probe] {
        let observation = reference.inspect().unwrap();
        assert!(observation.resources.is_empty());
        assert_eq!(observation.native_path, reference.native_path());
        assert_eq!(observation.class, reference.class());
    }
    assert_eq!(std::fs::read_dir(&account_path).unwrap().count(), 1);
    assert_eq!(std::fs::read_dir(&probe_path).unwrap().count(), 0);
    assert_eq!(
        std::fs::read(account_path.join("private-fixture-sentinel")).unwrap(),
        b"unchanged synthetic data"
    );
    assert_eq!(bindings[0].native_path(), account_path);
    assert_ne!(account.opaque_home_id(), probe.opaque_home_id());
    assert!(ExistingHomeReference::new(account_path.clone(), HomeClass::ApiKey).is_err());
    assert!(ExistingHomeReference::new(f.0.join("missing-account"), HomeClass::Account).is_err());
    assert!(ExistingHomeReference::new(
        account_path.join("private-fixture-sentinel"),
        HomeClass::Account
    )
    .is_err());
}

#[test]
fn received_binding_overlap_and_changed_source_are_refused_without_repair() {
    let f = Fixture::new();
    let sources = f.shared();
    let account_path = f.0.join("existing-account");
    std::fs::create_dir(&account_path).unwrap();
    let account = ExistingHomeReference::new(account_path.clone(), HomeClass::Account).unwrap();
    let probe_same = ExistingHomeReference::new(account_path.clone(), HomeClass::Probe).unwrap();
    assert!(validate_home_bindings(&[
        HomeBinding::Existing(&account),
        HomeBinding::Existing(&probe_same)
    ])
    .is_err());
    let nested_key = OwnedHomePlan::new(
        f.0.clone(),
        account_path.join("new-key"),
        HomeClass::ApiKey,
        Some(sources.clone()),
    )
    .unwrap();
    assert!(validate_home_bindings(&[
        HomeBinding::Existing(&account),
        HomeBinding::Owned(&nested_key)
    ])
    .is_err());
    let case_alias = f.0.join("EXISTING-ACCOUNT");
    if case_alias.is_dir() {
        use std::os::unix::fs::MetadataExt;
        let a = std::fs::metadata(&account_path).unwrap();
        let b = std::fs::metadata(&case_alias).unwrap();
        assert_eq!((a.dev(), a.ino()), (b.dev(), b.ino()));
        let alias_probe = ExistingHomeReference::new(case_alias, HomeClass::Probe).unwrap();
        assert!(validate_home_bindings(&[
            HomeBinding::Existing(&account),
            HomeBinding::Existing(&alias_probe)
        ])
        .is_err());
    }
    let foreign = f.0.join("foreign");
    std::fs::create_dir(&foreign).unwrap();
    std::fs::remove_dir(&account_path).unwrap();
    symlink(&foreign, &account_path).unwrap();
    assert!(account.inspect().is_err());
    let key = f.plan("key", HomeClass::ApiKey, Some(sources));
    assert!(
        validate_home_bindings(&[HomeBinding::Existing(&account), HomeBinding::Owned(&key)])
            .is_err()
    );
    assert_eq!(std::fs::read_dir(&foreign).unwrap().count(), 0);
    assert!(std::fs::symlink_metadata(account_path)
        .unwrap()
        .file_type()
        .is_symlink());
}
