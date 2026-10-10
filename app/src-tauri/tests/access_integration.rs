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

#[test]
fn root_key_admission_uses_current_fixed_ledger_and_genuine_shared_session() {
    use chirality_app_v4_lib::runtime_session::{
        prepare_native_key_namespace, reviewed_ledger_path, RecoveryStartup,
    };
    let fixture = Fixture::new();
    let set = freeze_root_home_descriptors(
        &fixture.data,
        &fixture.cfg,
        Some(fixture.data.join("key")),
        fixture.targets.clone(),
    )
    .unwrap();
    let current =
        freeze_root_home_descriptors(&fixture.data, &fixture.cfg, None, fixture.targets.clone())
            .unwrap()
            .native_namespaces(false)
            .unwrap();
    let account = Arc::new(Host::new());
    let mut startup = RecoveryStartup::default();
    assert_eq!(
        startup.initialize_with_namespaces(
            &account,
            Ok(&fixture.data),
            Some(&fixture.cfg.codex_home),
            Ok(current),
        )["state"],
        "configured"
    );
    let cap = account.app_runtime_custody().unwrap();
    let leaf = reviewed_ledger_path(&fixture.data);
    let before = std::fs::read(&leaf).unwrap();
    let admitted = prepare_native_key_namespace(&set, &fixture.data, &cap).unwrap();
    assert_eq!(
        admitted.observation["rec"]["state"],
        "prospective REC leaf/native namespace metadata disjoint"
    );
    assert_eq!(std::fs::read(&leaf).unwrap(), before);
    assert_eq!(admitted.attachment.root(), fixture.data.as_path());
    let peer = Host::new_with_app_custody(cap.clone()).unwrap();
    assert!(Arc::ptr_eq(&peer.app_runtime_custody().unwrap(), &cap));
    let mut peer_startup = RecoveryStartup::default();
    peer_startup.adopt_shared_source(&peer);
    assert_eq!(peer_startup.snapshot()["state"], "shared-source-configured");
    assert_eq!(std::fs::read(&leaf).unwrap(), before);
    // Current use must recheck the actual setup links, not retain a success flag.
    #[cfg(unix)]
    {
        std::fs::remove_file(fixture.data.join("key/skills")).unwrap();
        std::os::unix::fs::symlink(
            fixture.data.join("runtime"),
            fixture.data.join("key/skills"),
        )
        .unwrap();
        assert!(admitted
            .attachment
            .supplies_path("submission:00000000-0000-4000-8000-000000000001")
            .is_err());
        assert!(cap
            .preflight_native_namespaces(&admitted.namespaces)
            .is_err());
        assert_eq!(std::fs::read(&leaf).unwrap(), before);
    }
}

#[test]
fn prospective_key_drift_refuses_setup_without_vetoing_current_account_binding() {
    use chirality_app_v4_lib::runtime_session::{
        prepare_native_key_namespace, reviewed_ledger_path, RecoveryStartup,
    };
    let fixture = Fixture::new();
    let key = fixture.data.join("key");
    let set = freeze_root_home_descriptors(
        &fixture.data,
        &fixture.cfg,
        Some(key.clone()),
        fixture.targets.clone(),
    )
    .unwrap();
    let current = set.native_namespaces(false).unwrap();
    let host = Host::new();
    let mut startup = RecoveryStartup::default();
    assert_eq!(
        startup.initialize_with_namespaces(
            &host,
            Ok(&fixture.data),
            Some(&fixture.cfg.codex_home),
            Ok(current.clone())
        )["state"],
        "configured"
    );
    let cap = host.app_runtime_custody().unwrap();
    let leaf = reviewed_ledger_path(&fixture.data);
    let before = std::fs::read(&leaf).unwrap();
    #[cfg(unix)]
    {
        std::os::unix::fs::symlink(&fixture.cfg.codex_home, &key).unwrap();
        assert!(prepare_native_key_namespace(&set, &fixture.data, &cap).is_err());
        assert!(set.revalidate().is_err());
        set.validate_binding(HomeClass::Account, &fixture.cfg)
            .unwrap();
        assert!(!fixture.cfg.codex_home.join("config.toml").exists());
        assert_eq!(std::fs::read(&leaf).unwrap(), before);
        cap.bind_native_namespaces(current).unwrap();
        assert_eq!(std::fs::read_link(&key).unwrap(), fixture.cfg.codex_home);
    }
}

#[test]
fn redirected_fixed_rec_leaf_refuses_before_key_creation_and_preserves_canary() {
    use chirality_app_v4_lib::runtime_session::{
        prepare_native_key_namespace, reviewed_ledger_path, RecoveryStartup,
    };
    let fixture = Fixture::new();
    let key = fixture.data.join("key");
    let set = freeze_root_home_descriptors(
        &fixture.data,
        &fixture.cfg,
        Some(key.clone()),
        fixture.targets.clone(),
    )
    .unwrap();
    let host = Host::new();
    let mut startup = RecoveryStartup::default();
    startup.initialize_with_namespaces(
        &host,
        Ok(&fixture.data),
        Some(&fixture.cfg.codex_home),
        Ok(set.native_namespaces(false).unwrap()),
    );
    let cap = host.app_runtime_custody().unwrap();
    let leaf = reviewed_ledger_path(&fixture.data);
    let saved = fixture.data.join("runtime/saved-own-ledger");
    let before = std::fs::read(&leaf).unwrap();
    #[cfg(unix)]
    {
        let canary = fixture.targets[0].as_ref().unwrap();
        let untouched = std::fs::read(canary).unwrap();
        std::fs::rename(&leaf, &saved).unwrap();
        std::os::unix::fs::symlink(canary, &leaf).unwrap();
        assert!(prepare_native_key_namespace(&set, &fixture.data, &cap).is_err());
        assert!(!key.exists());
        assert_eq!(std::fs::read(canary).unwrap(), untouched);
        assert_eq!(std::fs::read(&saved).unwrap(), before);
        set.validate_binding(HomeClass::Account, &fixture.cfg)
            .unwrap();
        std::fs::remove_file(&leaf).unwrap();
        std::fs::rename(&saved, &leaf).unwrap();
        let admitted = prepare_native_key_namespace(&set, &fixture.data, &cap).unwrap();
        assert_eq!(
            admitted.observation["rec"]["state"],
            "prospective REC leaf/native namespace metadata disjoint"
        );
        assert_eq!(std::fs::read(&leaf).unwrap(), before);
    }
}

#[cfg(unix)]
fn frame_peer(fixture: &Fixture) -> HostConfig {
    use std::os::unix::fs::PermissionsExt;
    let peer = fixture.root.join("owned-synthetic-frame-peer.py");
    std::fs::write(&peer, r#"#!/usr/bin/python3
import json, os, sys
# This is an owned fixture, never the stock supplier or a version witness.
if '--version' in sys.argv:
    print('codex-cli 0.160.0')
    sys.exit(0)
def emit(value):
    print(json.dumps(value), flush=True)
sequence = 0
for line in sys.stdin:
    frame = json.loads(line)
    method = frame.get('method')
    if method == 'initialize':
        emit({'id':frame['id'], 'result':{'userAgent':'unqualified-owned-fixture'}})
    elif method == 'synthetic/ordinary':
        sequence += 1
        emit({'id':frame['id'], 'result':{'unchanged':frame['params'], 'fixtureHome':os.environ['CODEX_HOME']}})
        emit({'id':'fixture-request-' + str(sequence), 'method':'item/fileChange/requestApproval', 'params':{'threadId':'same-thread', 'turnId':'fixture-turn', 'itemId':'fixture-item', 'availableDecisions':['accept','decline']}})
    elif str(frame.get('id','')).startswith('fixture-request-'):
        emit({'method':'serverRequest/resolved', 'params':{'requestId':frame['id']}})
"#).unwrap();
    std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
    let mut config = fixture.cfg.clone();
    config.codex_bin = peer;
    config.cwd = fixture.root.clone();
    config.allow_unverified_dev = true;
    config.wait_limit = std::time::Duration::from_secs(2);
    config
}
#[cfg(unix)]
struct StartedFixture(Arc<Host>);
#[cfg(unix)]
impl Drop for StartedFixture {
    fn drop(&mut self) {
        let _ = self
            .0
            .stop("owned fixture cleanup", "bounded synthetic test finished");
    }
}
#[cfg(unix)]
fn ordinary_fixture_roundtrip(
    host: &Host,
    generation: &serde_json::Value,
    expected_home: &std::path::Path,
    text: &str,
) {
    use serde_json::json;
    let response = host
        .request(
            "synthetic/ordinary",
            json!({"text":text}),
            json!({"kind":"app-rule","name":"owned fixture"}),
        )
        .unwrap();
    assert_eq!(response["result"]["unchanged"]["text"], text);
    assert_eq!(
        response["result"]["fixtureHome"],
        expected_home.to_str().unwrap()
    );
    let deadline = std::time::Instant::now() + std::time::Duration::from_secs(2);
    let request = loop {
        let snapshot = host.snapshot();
        if let Some(request) = snapshot["serverRequests"]
            .as_array()
            .unwrap()
            .iter()
            .find(|r| r["state"] == "outstanding")
        {
            break request["requestIdentity"].clone();
        }
        assert!(
            std::time::Instant::now() < deadline,
            "owned fixture request was not observed"
        );
        std::thread::sleep(std::time::Duration::from_millis(2));
    };
    let reply = host
        .answer_server_request(
            generation,
            &request,
            &json!({"decision":"decline"}),
            "app-rule:owned-fixture-negative",
            None,
        )
        .unwrap();
    assert_eq!(reply["replyWriteResult"], "written");
}
#[test]
#[cfg(unix)]
fn connected_root_sources_keep_ordinary_input_reply_and_scoped_stop_during_key_and_ledger_drift() {
    use chirality_app_v4_lib::runtime_session::{
        prepare_native_key_namespace, reviewed_ledger_path, RecoveryStartup,
    };
    let fixture = Fixture::new();
    let config = frame_peer(&fixture);
    let key_path = fixture.data.join("key");
    let set = freeze_root_home_descriptors(
        &fixture.data,
        &config,
        Some(key_path.clone()),
        fixture.targets.clone(),
    )
    .unwrap();
    let host = Arc::new(Host::new());
    let account_guard = StartedFixture(host.clone());
    let mut startup = RecoveryStartup::default();
    assert_eq!(
        startup.initialize_with_namespaces(
            &host,
            Ok(&fixture.data),
            Some(&config.codex_home),
            Ok(set.native_namespaces(false).unwrap())
        )["state"],
        "configured"
    );
    host.start(&config, "owned synthetic frame fixture")
        .unwrap();
    assert_eq!(
        host.snapshot()["supplierStanding"],
        "unverified-development"
    );
    let account_generation = host.snapshot()["generation"].clone();
    let account =
        Arc::new(HomeSession::new(HomeClass::Account, host.clone(), Ok(config.clone())).unwrap());
    let mut router = HomeRouter::new(account).unwrap();
    let cap = host.app_runtime_custody().unwrap();
    // Original saved consumer revalidated the prospective key here and refused
    // account input. The criterion stays account availability with zero key setup.
    std::os::unix::fs::symlink(&config.codex_home, &key_path).unwrap();
    assert!(prepare_native_key_namespace(&set, &fixture.data, &cap).is_err());
    set.validate_binding(HomeClass::Account, &config).unwrap();
    ordinary_fixture_roundtrip(
        &host,
        &account_generation,
        &config.codex_home,
        "account after bad prospective key",
    );
    std::fs::remove_file(&key_path).unwrap();
    let admitted = prepare_native_key_namespace(&set, &fixture.data, &cap).unwrap();
    let peer = Arc::new(Host::new_with_app_custody(cap.clone()).unwrap());
    let key_guard = StartedFixture(peer.clone());
    let mut key_config = config.clone();
    key_config.codex_home = key_path.clone();
    peer.start(&key_config, "owned separate synthetic frame fixture")
        .unwrap();
    let key_generation = peer.snapshot()["generation"].clone();
    assert_eq!(
        account_generation["appSession"],
        key_generation["appSession"]
    );
    assert_ne!(account_generation["home"], key_generation["home"]);
    let key = Arc::new(HomeSession::new(HomeClass::ApiKey, peer.clone(), Ok(key_config)).unwrap());
    router.bind_key(key).unwrap();
    router.activate(HomeClass::ApiKey).unwrap();
    assert!(Arc::ptr_eq(
        router.for_generation(&account_generation).unwrap().source(),
        &host
    ));
    assert!(Arc::ptr_eq(
        router.for_generation(&key_generation).unwrap().source(),
        &peer
    ));
    ordinary_fixture_roundtrip(&peer, &key_generation, &key_path, "key original source");
    let leaf = reviewed_ledger_path(&fixture.data);
    let saved = fixture.data.join("runtime/saved-ledger");
    std::fs::rename(&leaf, &saved).unwrap();
    // The ledger append opens with create(true), so a late asynchronous
    // record from the round trip above can recreate the leaf right after the
    // rename. Read the saved ledger after the move, and plant the link
    // atomically over whatever is at the leaf now (link at a temporary name in
    // the same folder, then rename over the leaf).
    let before = std::fs::read(&saved).unwrap();
    let canary = fixture.targets[0].as_ref().unwrap();
    let untouched = std::fs::read(canary).unwrap();
    let planted = leaf.with_file_name("recovery.ledger.jsonl.planted-link");
    std::os::unix::fs::symlink(canary, &planted).unwrap();
    std::fs::rename(&planted, &leaf).unwrap();
    assert!(std::fs::symlink_metadata(&leaf).unwrap().file_type().is_symlink());
    assert!(prepare_native_key_namespace(&set, &fixture.data, &cap).is_err());
    assert!(cap
        .preflight_native_namespaces(&admitted.namespaces)
        .is_err());
    ordinary_fixture_roundtrip(
        &host,
        &account_generation,
        &config.codex_home,
        "account despite unavailable persistence",
    );
    let mut foreign = account_generation.clone();
    foreign["home"] = key_generation["home"].clone();
    assert!(host
        .stop_scoped(&foreign, "fixture", "foreign stop must refuse")
        .is_err());
    assert_eq!(host.snapshot()["state"], "ready");
    host.stop_scoped(
        &account_generation,
        "fixture",
        "stop while ledger redirected",
    )
    .unwrap();
    assert_eq!(peer.snapshot()["state"], "ready");
    peer.stop_scoped(&key_generation, "fixture", "original key source only")
        .unwrap();
    assert_eq!(std::fs::read(canary).unwrap(), untouched);
    assert_eq!(std::fs::read(&saved).unwrap(), before);
    drop(key_guard);
    drop(account_guard);
}

#[test]
#[cfg(unix)]
fn initially_redirected_rec_leaf_retains_actual_descriptor_and_restored_advisory_boundary() {
    use chirality_app_v4_lib::runtime_session::{
        prepare_native_key_namespace, reviewed_ledger_path, RecoveryStartup,
    };
    let fixture = Fixture::new();
    let key = fixture.data.join("key");
    let set = freeze_root_home_descriptors(
        &fixture.data,
        &fixture.cfg,
        Some(key.clone()),
        fixture.targets.clone(),
    )
    .unwrap();
    let leaf = reviewed_ledger_path(&fixture.data);
    std::fs::create_dir_all(leaf.parent().unwrap()).unwrap();
    let canary = fixture.targets[0].as_ref().unwrap();
    let untouched = std::fs::read(canary).unwrap();
    std::os::unix::fs::symlink(canary, &leaf).unwrap();
    let host = Host::new();
    let mut startup = RecoveryStartup::default();
    let initial = startup.initialize_with_namespaces(
        &host,
        Ok(&fixture.data),
        Some(&fixture.cfg.codex_home),
        Ok(set.native_namespaces(false).unwrap()),
    );
    assert_eq!(initial["state"], "initialization-failed");
    assert_eq!(initial["blocksSupplierStart"], false);
    let cap = host.app_runtime_custody().unwrap();
    assert!(cap
        .preflight_native_namespaces(&set.native_namespaces(true).unwrap())
        .is_err());
    assert!(!key.exists());
    assert_eq!(std::fs::read(canary).unwrap(), untouched);
    std::fs::remove_file(&leaf).unwrap();
    // This check must use the initially received actual leaf, even though its
    // original guarded open failed; a restored path is no persistence retry.
    cap.preflight_native_namespaces(&set.native_namespaces(true).unwrap())
        .unwrap();
    assert!(!host.shared_recovery_observation()["limit"].is_null());
    let admitted = prepare_native_key_namespace(&set, &fixture.data, &cap).unwrap();
    assert_eq!(admitted.observation["rec"]["ledgerUnavailable"], true);
    assert_eq!(admitted.observation["rec"]["bindingCommitted"], false);
    assert!(!leaf.exists());
    assert_eq!(host.shared_recovery_observation()["configured"], false);
    assert_eq!(std::fs::read(canary).unwrap(), untouched);
    set.validate_binding(HomeClass::Account, &fixture.cfg)
        .unwrap();
}
