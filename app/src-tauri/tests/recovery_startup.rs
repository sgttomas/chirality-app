//! Actual Host.configure_recovery plus the shared startup helper. Starter callbacks
//! are explicit synthetic observations: no supplier process/native window is run.
use chirality_app_v4_lib::{
    hosting::Host,
    native_requests::RequestRegister,
    recovery::{database_path, RecoveryLedger},
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
            host.recorded_recovery_entries()[0]["kind"],
            "session_started"
        );
        assert!(database_path(&path).exists(), "the ledger database is written before the start");
        assert!(!path.exists(), "no JSON Lines ledger is written");
        Ok(json!({"syntheticStartCallback":"observed configured Host before start"}))
    })
    .unwrap();
    assert!(result["syntheticStartCallback"].is_string());
    let before = std::fs::read(database_path(&path)).unwrap();
    let other = scratch.0.join("must-not-relocate");
    start_with_recovery(&host, &startup, Ok(&other), Some(&codex), || Ok(())).unwrap();
    assert_eq!(std::fs::read(database_path(&path)).unwrap(), before);
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
    assert_eq!(status["database"], database_path(&path).to_str().unwrap());
    assert_eq!(RecoveryLedger::open(path.clone()).unwrap().recorded_entries().as_array().unwrap().len(), 1);
}
/// DEL-01-02 §7 (SQLite direction): a JSON Lines ledger of an earlier build
/// is imported once; its torn tail is reported as a limit, never stored as an
/// entry, and the file is never written. A later start imports nothing again.
#[test]
fn malformed_tail_is_a_limit_of_the_import_and_the_file_is_never_written() {
    let scratch = Scratch::new();
    let root = scratch.0.join("app-data");
    let path = reviewed_ledger_path(&root);
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    let complete = json!({"kind":"session_started","session":"old-session","at":"synthetic","previousSessionEnd":"none","candidate":"synthetic"});
    let mut legacy = serde_json::to_vec(&complete).unwrap();
    legacy.push(b'\n');
    legacy.extend_from_slice(br#"{"kind":"session_ended","session":"old-sess"#);
    std::fs::write(&path, &legacy).unwrap();
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    let called = std::cell::Cell::new(false);
    start_with_recovery(&host, &startup, Ok(&root), None, || {
        called.set(true);
        assert_eq!(host.recorded_recovery_entries()[0], complete, "the complete line is imported");
        Ok(())
    })
    .unwrap();
    assert!(called.get());
    assert_eq!(std::fs::read(&path).unwrap(), legacy);
    let status = startup.lock().unwrap().snapshot();
    assert_eq!(status["state"], "configured");
    assert_eq!(status["historyFile"], "existing");
    let import = &host.snapshot()["recovery"]["store"]["legacyImport"];
    assert_eq!(import["state"], "imported", "{import}");
    assert_eq!(import["importedLines"], 1);
    assert_eq!(import["byteLength"], legacy.len());
    assert!(import["limit"].as_str().unwrap().contains("not newline-closed"), "{import}");
    let entries = host.recorded_recovery_entries().as_array().unwrap().clone();
    assert_eq!(entries.len(), 2, "the import and this session's start; the torn tail is no entry");
    assert_eq!(entries[1]["previousSessionEnd"], "ended-without-record");
    // A later App start reads the database; the file is not imported twice.
    let next = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    start_with_recovery(&next, &startup, Ok(&root), None, || Ok(())).unwrap();
    assert_eq!(next.snapshot()["recovery"]["store"]["legacyImport"]["state"], "imported earlier");
    assert_eq!(next.recorded_recovery_entries().as_array().unwrap().len(), 3);
    assert_eq!(std::fs::read(path).unwrap(), legacy);
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
    let database = database_path(&path);
    let before = std::fs::read(&database).unwrap();
    std::fs::set_permissions(&database, std::fs::Permissions::from_mode(0o400)).unwrap();
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
    assert_eq!(std::fs::read(&database).unwrap(), before);
    std::fs::set_permissions(database, std::fs::Permissions::from_mode(0o600)).unwrap();
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
    let before = RecoveryLedger::open(path.clone()).unwrap().recorded_entries().as_array().unwrap().clone();
    let host = Host::new();
    let startup = Mutex::new(RecoveryStartup::default());
    start_with_recovery(&host, &startup, Ok(&root), None, || Ok(())).unwrap();
    let after = RecoveryLedger::open(path.clone()).unwrap().recorded_entries().as_array().unwrap().clone();
    assert!(after.starts_with(&before), "earlier entries are kept as they were");
    assert!(!serde_json::to_string(&after).unwrap().contains("synthetic-must-not-copy"));
    assert!(!String::from_utf8_lossy(&std::fs::read(database_path(&path)).unwrap()).contains("synthetic-must-not-copy"));
    let snapshot = host.snapshot();
    assert_eq!(snapshot["recovery"]["oldRequestsAnswerable"], false);
    assert!(snapshot["serverRequests"].as_array().unwrap().is_empty());
    let entries = host.recorded_recovery_entries();
    let entries = entries.as_array().unwrap();
    let start_position = entries.iter().rposition(|e| e["kind"] == "session_started").unwrap();
    assert_eq!(
        entries[start_position]["previousSessionEnd"],
        "ended-without-record"
    );
    let ending_position = entries.iter().position(|e| e["transition"] == "RQ-06").unwrap();
    assert!(ending_position > start_position);
    let ending = &entries[ending_position];
    assert_eq!(ending["state"], "closed");
    assert_eq!(ending["requestIdentity"], "\"old-request\"");
    assert_eq!(ending["context"], "app-ended-without-record");
    assert_eq!(ending["replyWrite"], "not-attempted");
    assert_eq!(ending["acknowledgment"], "not-observed");
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
    assert!(!alternate.join("recovery.ledger.sqlite").exists());
    assert!(host.snapshot()["recovery"].is_null());
}
