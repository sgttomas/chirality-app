//! Actual Host.configure_recovery plus the shared startup helper. Starter callbacks
//! are explicit synthetic observations: no supplier process/native window is run.
use chirality_app_v4_lib::{
    hosting::Host,
    native_requests::RequestRegister,
    recovery::RecoveryLedger,
    runtime_session::{reviewed_ledger_path, start_with_recovery, RecoveryStartup},
};
use serde_json::json;
use std::path::PathBuf;
use std::sync::Mutex;
struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let p = std::env::temp_dir()
            .join(chirality_app_v4_lib::util::opaque_id("ledger-startup-").unwrap());
        std::fs::create_dir(&p).unwrap();
        Self(p)
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        std::fs::remove_dir_all(&self.0).unwrap();
    }
}
#[test]
fn automatic_and_manual_start_helper_initialize_actual_host_once_at_fixed_app_path() {
    let scratch = Scratch::new();
    let root = scratch.0.join("app-data");
    let codex = scratch.0.join("codex-home");
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    let path = reviewed_ledger_path(&root);
    let result = start_with_recovery(&host, &startup, Ok(&root), Some(&codex), || {
        assert_eq!(startup.lock().unwrap().snapshot()["state"], "configured");
        assert_eq!(
            host.snapshot()["recovery"]["entries"][0]["kind"],
            "session_started"
        );
        assert!(path.exists());
        Ok(json!({"syntheticStartCallback":"observed configured Host before start"}))
    })
    .unwrap();
    assert!(result["syntheticStartCallback"].is_string());
    let before = std::fs::read(&path).unwrap();
    let other = scratch.0.join("must-not-relocate");
    start_with_recovery(&host, &startup, Ok(&other), Some(&codex), || Ok(())).unwrap();
    assert_eq!(std::fs::read(&path).unwrap(), before);
    assert!(!other.exists());
    assert!(!codex.exists());
    let status = startup.lock().unwrap().snapshot();
    assert_eq!(status["state"], "configured");
    assert_eq!(status["hostConfigured"], true);
    assert_eq!(status["directoryPublication"], "sync-calls-succeeded");
    assert_eq!(status["blocksSupplierStart"], false);
    assert_eq!(status["path"]["displayPath"], path.to_str().unwrap());
    assert_eq!(
        status["path"]["nativePath"]["bytes"],
        json!(path.as_os_str().as_encoded_bytes())
    );
    assert_eq!(std::str::from_utf8(&before).unwrap().lines().count(), 1);
}
#[test]
fn malformed_tail_refuses_configuration_preserves_bytes_and_still_runs_starter() {
    let scratch = Scratch::new();
    let root = scratch.0.join("app-data");
    let path = reviewed_ledger_path(&root);
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
    ledger.start_session("old-session", "synthetic").unwrap();
    drop(ledger);
    let mut tail = std::fs::read(&path).unwrap();
    assert_eq!(tail.pop(), Some(b'\n'));
    std::fs::write(&path, &tail).unwrap();
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    let called = std::cell::Cell::new(false);
    start_with_recovery(&host, &startup, Ok(&root), None, || {
        called.set(true);
        assert!(host.snapshot()["recovery"].is_null());
        Ok(())
    })
    .unwrap();
    assert!(called.get());
    assert_eq!(std::fs::read(&path).unwrap(), tail);
    let status = startup.lock().unwrap().snapshot();
    assert_eq!(status["state"], "initialization-failed");
    assert_eq!(status["hostConfigured"], false);
    assert!(status["configurationError"]
        .as_str()
        .unwrap()
        .contains("not newline-closed"));
    assert_eq!(status["blocksSupplierStart"], false);
    assert!(host.snapshot()["recoveryPersistenceError"].is_null()); // error custody is explicitly App startup-owned
    start_with_recovery(&host, &startup, Ok(&root), None, || Ok(())).unwrap();
    assert_eq!(std::fs::read(path).unwrap(), tail);
}
#[test]
fn unavailable_root_and_codex_home_collision_are_visible_without_fallback_or_suppressed_start() {
    let scratch = Scratch::new();
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    let failure = start_with_recovery(
        &host,
        &startup,
        Err("synthetic App user-data resolution failure"),
        None,
        || Err::<(), _>("synthetic supplier start result".into()),
    )
    .unwrap_err();
    assert_eq!(failure, "synthetic supplier start result");
    let status = startup.lock().unwrap().snapshot();
    assert_eq!(
        status["configurationError"],
        "synthetic App user-data resolution failure"
    );
    assert!(status["path"].is_null());
    assert!(host.snapshot()["recovery"].is_null());
    let root = scratch.0.join("codex-home/app-data");
    let codex = scratch.0.join("codex-home");
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    start_with_recovery(&host, &startup, Ok(&root), Some(&codex), || Ok(())).unwrap();
    let status = startup.lock().unwrap().snapshot();
    assert!(status["configurationError"]
        .as_str()
        .unwrap()
        .contains("inside the configured Codex home"));
    assert!(!codex.exists());
    assert!(!root.exists());
    let block = scratch.0.join("not-a-directory");
    std::fs::write(&block, b"synthetic existing bytes").unwrap();
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    start_with_recovery(&host, &startup, Ok(&block), None, || Ok(())).unwrap();
    assert_eq!(
        startup.lock().unwrap().snapshot()["state"],
        "initialization-failed"
    );
    assert_eq!(std::fs::read(block).unwrap(), b"synthetic existing bytes");
    assert!(host.snapshot()["recovery"].is_null());
}
#[cfg(unix)]
#[test]
fn unwritable_existing_ledger_reports_actual_permission_error_without_byte_changes() {
    use std::os::unix::fs::PermissionsExt;
    if unsafe { libc::geteuid() } == 0 {
        eprintln!("Permission refusal case not exercised under privileged euid 0");
        return;
    }
    let scratch = Scratch::new();
    let root = scratch.0.join("app-data");
    let path = reviewed_ledger_path(&root);
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
    ledger.start_session("previous", "synthetic").unwrap();
    drop(ledger);
    let before = std::fs::read(&path).unwrap();
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o400)).unwrap();
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    let called = std::cell::Cell::new(false);
    start_with_recovery(&host, &startup, Ok(&root), None, || {
        called.set(true);
        Ok(())
    })
    .unwrap();
    let status = startup.lock().unwrap().snapshot();
    assert_eq!(status["state"], "initialization-failed");
    assert_eq!(status["hostConfigured"], false);
    assert!(status["configurationError"].is_string());
    assert!(called.get());
    assert!(host.snapshot()["recovery"].is_null());
    assert_eq!(std::fs::read(&path).unwrap(), before);
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o600)).unwrap();
}
#[test]
fn existing_historical_pointer_entries_stay_nonanswerable_and_never_copy_native_payload() {
    let scratch = Scratch::new();
    let root = scratch.0.join("app-data");
    let path = reviewed_ledger_path(&root);
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    let generation = json!({"appSession":"old","home":"synthetic-home","spawnCounter":1});
    let mut register = RequestRegister::default();
    register.receive(&generation,1,&json!({"id":"old-request","method":"item/tool/requestUserInput","params":{"threadId":"t","questions":[{"id":"secret","text":"synthetic-must-not-copy","isSecret":true}]}}),&json!({})).unwrap();
    let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
    ledger.start_session("old", "synthetic").unwrap();
    ledger.request_summary(&register.entries()[0]).unwrap();
    drop(ledger);
    let before = std::fs::read(&path).unwrap();
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    start_with_recovery(&host, &startup, Ok(&root), None, || Ok(())).unwrap();
    let after = std::fs::read(&path).unwrap();
    assert!(after.starts_with(&before));
    assert!(!std::str::from_utf8(&after)
        .unwrap()
        .contains("synthetic-must-not-copy"));
    let snapshot = host.snapshot();
    assert_eq!(snapshot["recovery"]["oldRequestsAnswerable"], false);
    assert!(snapshot["serverRequests"].as_array().unwrap().is_empty());
    let entries = snapshot["recovery"]["entries"].as_array().unwrap();
    assert_eq!(
        entries.last().unwrap()["previousSessionEnd"],
        "ended-without-record"
    );
    assert_eq!(
        startup.lock().unwrap().snapshot()["historyFile"],
        "existing"
    );
}
#[cfg(unix)]
#[test]
fn linked_runtime_directory_is_refused_without_recording_at_another_location() {
    let scratch = Scratch::new();
    let root = scratch.0.join("app-data");
    let alternate = scratch.0.join("alternate");
    std::fs::create_dir(&root).unwrap();
    std::fs::create_dir(&alternate).unwrap();
    std::os::unix::fs::symlink(&alternate, root.join("runtime")).unwrap();
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    start_with_recovery(&host, &startup, Ok(&root), None, || Ok(())).unwrap();
    assert!(startup.lock().unwrap().snapshot()["configurationError"]
        .as_str()
        .unwrap()
        .contains("symbolic link"));
    assert!(!alternate.join("recovery.ledger.jsonl").exists());
    assert!(host.snapshot()["recovery"].is_null());
}
