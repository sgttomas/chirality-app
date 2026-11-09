//! Owner decisions A, B and C (2026-11-09): persistence, defaults, recovery and
//! lowering of the workflow approval policy, on in-memory stores and the
//! in-memory keychain backend. No native dialog, SecItem or App instance.
use super::*;
use crate::capture_seal_keychain::tests::InMemoryKeychain;

fn file() -> Arc<MemoryStore> { Arc::new(MemoryStore::default()) }
fn unprotected(file: &Arc<MemoryStore>) -> Settings { Settings::with_stores(|| None, Box::new(file.clone())) }
fn keychain() -> Option<Box<dyn Store>> { Some(Box::new(Keychain)) }
fn lower(settings: &Settings) -> Result<(), String> {
    let (id, epoch, _) = settings.lowering_context();
    settings.lower(crate::act_control::ConfirmedAssuranceAct::synthetic(id, epoch))
}

#[test]
fn first_use_default_is_relaxed_without_keychain_and_persists_across_relaunch() {
    let store = file();
    let first = unprotected(&store);
    assert_eq!(first.level(), AssuranceLevel::Relaxed);
    assert_eq!(first.view()["policy"], RELAXED_NAME);
    assert_eq!(first.view()["verification"]["available"], false);
    assert!(first.view()["storage"].as_str().unwrap().contains("an agent able to write that file could change"));
    assert_eq!(*store.writes.lock().unwrap(), vec![AssuranceLevel::Relaxed], "the first-use default is recorded");
    first.require_verified().unwrap();
    // Relaunch: a new process reads the stored choice, not the default.
    let relaunched = unprotected(&store);
    assert_eq!(relaunched.level(), AssuranceLevel::Robust);
    assert_eq!(relaunched.view()["policy"], ROBUST_NAME);
    assert_eq!(relaunched.view()["robustWithoutVerification"], "Session confirmation required; persistent verification unavailable");
}

#[test]
fn lowering_needs_the_native_act_for_the_current_epoch() {
    let store = file();
    let settings = unprotected(&store);
    settings.require_verified().unwrap();
    let (id, epoch, protected) = settings.lowering_context();
    assert!(!protected);
    settings.require_verified().unwrap(); // the setting changed while the question was open
    assert!(settings.lower(crate::act_control::ConfirmedAssuranceAct::synthetic(id, epoch)).is_err());
    assert_eq!(settings.level(), AssuranceLevel::Robust);
    lower(&settings).unwrap();
    assert_eq!(settings.level(), AssuranceLevel::Relaxed);
    assert_eq!(unprotected(&store).level(), AssuranceLevel::Relaxed, "a person's lowering persists");
}

#[test]
fn an_unreadable_settings_file_never_relaxes() {
    let store = file();
    *store.value.lock().unwrap() = Some(Err("stored App setting is corrupt".into()));
    let settings = unprotected(&store);
    assert_eq!(settings.level(), AssuranceLevel::Robust);
    assert!(store.writes.lock().unwrap().is_empty(), "nothing is rewritten automatically");
}

#[test]
fn agent_writable_project_files_and_ipc_values_cannot_change_the_policy() {
    // Only the App settings store is read; there is no path, project file,
    // environment value or IPC Boolean input. A file planted elsewhere is inert.
    let store = file();
    let settings = unprotected(&store);
    settings.require_verified().unwrap();
    let scratch = std::env::temp_dir().join(crate::util::opaque_id("assurance-test-").unwrap());
    std::fs::create_dir_all(scratch.join(".chirality")).unwrap();
    std::fs::write(scratch.join(".chirality/workflow-approval-policy.json"), r#"{"format":"chirality.app.workflow-approval-policy-setting","level":"relaxed"}"#).unwrap();
    assert_eq!(settings.level(), AssuranceLevel::Robust);
    assert_eq!(unprotected(&store).level(), AssuranceLevel::Robust);
    std::fs::remove_dir_all(scratch).unwrap();
}

#[test]
fn keychain_default_is_robust_and_lowering_under_protection_needs_the_native_act() {
    let chain = InMemoryKeychain::install(true);
    let store = file();
    *store.value.lock().unwrap() = Some(Ok(Stored::Level(AssuranceLevel::Relaxed)));
    let settings = Settings::with_stores(keychain, Box::new(store.clone()));
    // Enrolled with no policy item: recovery, never relaxed, even though the
    // unprotected settings file says relaxed.
    assert_eq!(settings.level(), AssuranceLevel::Robust);
    assert_eq!(settings.view()["verification"]["state"], "recovery required");
    assert!(lower(&settings).is_err(), "no lowering while recovery is required");
    settings.after_enrollment().unwrap();
    assert_eq!(settings.view()["verification"]["state"], "set up");
    assert_eq!(settings.level(), AssuranceLevel::Robust, "the default where keychain protection works");
    assert_eq!(chain.policy_items(), 1);
    lower(&settings).unwrap();
    assert_eq!(chain.policy_items(), 2);
    assert!(store.writes.lock().unwrap().is_empty(), "protected choices never go to the settings file");
    let relaunched = Settings::with_stores(keychain, Box::new(store.clone()));
    assert_eq!(relaunched.level(), AssuranceLevel::Relaxed, "the person's protected choice persists");
    assert!(relaunched.view()["storage"].as_str().unwrap().contains("keychain"));
}

#[test]
fn keychain_error_at_startup_and_missing_locked_or_corrupt_policy_need_recovery() {
    let chain = InMemoryKeychain::install(true);
    let store = file();
    *store.value.lock().unwrap() = Some(Ok(Stored::Level(AssuranceLevel::Relaxed)));
    let setup = Settings::with_stores(keychain, Box::new(store.clone()));
    setup.after_enrollment().unwrap();
    lower(&setup).unwrap();
    // Locked at startup: the stored relaxed choice is not readable, so robust.
    chain.lock();
    let locked = Settings::with_stores(keychain, Box::new(store.clone()));
    assert_eq!(locked.level(), AssuranceLevel::Robust);
    assert_eq!(locked.view()["verification"]["state"], "recovery required");
    assert!(lower(&locked).is_err());
    locked.recheck();
    assert_eq!(locked.level(), AssuranceLevel::Robust, "still locked");
    chain.unlock();
    locked.recheck();
    assert_eq!(locked.level(), AssuranceLevel::Relaxed, "re-reading applies the person's stored choice");
    // Corrupt: robust until restored; restoring is raising.
    chain.corrupt_policy();
    let corrupt = Settings::with_stores(keychain, Box::new(store.clone()));
    assert_eq!(corrupt.level(), AssuranceLevel::Robust);
    corrupt.require_verified().unwrap();
    assert_eq!(corrupt.view()["verification"]["state"], "set up");
    // A keychain error never falls back to the agent-writable settings file.
    drop(chain);
    let missing_provider = Settings::with_stores(|| Some(Box::new(Keychain) as Box<dyn Store>), Box::new(store.clone()));
    assert_eq!(missing_provider.level(), AssuranceLevel::Robust);
}

#[test]
fn explicitly_set_robust_is_never_lowered_automatically() {
    let store = file();
    let settings = unprotected(&store);
    settings.require_verified().unwrap();
    *store.write_error.lock().unwrap() = Some("disk full".into());
    assert!(lower(&settings).is_err(), "an unsaved lowering does not apply");
    assert_eq!(settings.level(), AssuranceLevel::Robust);
    settings.recheck(); // only a protected recovery re-reads
    assert_eq!(settings.level(), AssuranceLevel::Robust);
}

#[test]
fn restoring_after_a_locked_start_never_reports_protection_without_enrollment() {
    // Never enrolled, keychain locked at startup: recovery, robust.
    let chain = InMemoryKeychain::install(false);
    chain.lock();
    let store = file();
    let settings = Settings::with_stores(keychain, Box::new(store.clone()));
    assert_eq!(settings.level(), AssuranceLevel::Robust);
    assert_eq!(settings.view()["verification"]["state"], "recovery required");
    chain.unlock();
    settings.require_verified().unwrap();
    assert_eq!(settings.view()["verification"]["state"], "not set up", "no seal key, so no protection is claimed");
    assert_eq!(settings.view()["verification"]["available"], false);
    assert_eq!(chain.policy_items(), 0, "no keychain policy without enrollment");
    assert_eq!(store.writes.lock().unwrap().last(), Some(&AssuranceLevel::Robust));
}

#[test]
fn a_lost_latest_protected_item_needs_recovery_and_never_rolls_back() {
    let chain = InMemoryKeychain::install(true);
    let store = file();
    let settings = Settings::with_stores(keychain, Box::new(store.clone()));
    settings.after_enrollment().unwrap(); // 1 = robust
    lower(&settings).unwrap(); // 2 = relaxed
    settings.require_verified().unwrap(); // 3 = robust
    chain.remove_latest_policy();
    let relaunched = Settings::with_stores(keychain, Box::new(store.clone()));
    assert_eq!(relaunched.level(), AssuranceLevel::Robust, "never the earlier relaxed item");
    assert_eq!(relaunched.view()["verification"]["state"], "recovery required");
    relaunched.require_verified().unwrap();
    assert_eq!(relaunched.view()["verification"]["state"], "set up");
}

#[test]
fn a_lost_seal_key_never_falls_back_to_a_relaxed_settings_file() {
    let chain = InMemoryKeychain::install(true);
    let store = file();
    *store.value.lock().unwrap() = Some(Ok(Stored::Level(AssuranceLevel::Relaxed)));
    let settings = Settings::with_stores(keychain, Box::new(store.clone()));
    settings.after_enrollment().unwrap();
    chain.remove_sentinel();
    let relaunched = Settings::with_stores(keychain, Box::new(store.clone()));
    assert_eq!(relaunched.level(), AssuranceLevel::Robust, "never the file's relaxed");
    assert_eq!(relaunched.view()["verification"]["state"], "recovery required");
    assert!(relaunched.require_verified().is_err(), "restoration that does not read back is not reported as success");
    assert_eq!(relaunched.level(), AssuranceLevel::Robust);
}
