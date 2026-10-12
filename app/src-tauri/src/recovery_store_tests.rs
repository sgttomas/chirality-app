//! The App ledger's SQLite store (DEL-01-02 §7): append-only in the schema,
//! one transaction per batch, the JSON Lines import, visible failures.
use super::*;
use crate::recovery::{remove_test_ledger, RecoveryLedger};

struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let path = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("ledger-store-").unwrap());
        std::fs::create_dir(&path).unwrap();
        Self(path)
    }
    fn ledger_path(&self) -> PathBuf {
        self.0.join("recovery.ledger.jsonl")
    }
    fn open(&self) -> RecoveryLedger {
        RecoveryLedger::open(self.ledger_path()).unwrap()
    }
    fn entries(&self) -> Vec<Value> {
        crate::recovery::stored_entries(&self.ledger_path())
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        remove_test_ledger(&self.ledger_path());
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn started(session: &str) -> Value {
    json!({"kind":"session_started","session":session,"at":"synthetic","previousSessionEnd":"none","candidate":"c"})
}
fn ended(session: &str) -> Value {
    RecoveryLedger::session_end_entry(session, "quit", &[]).unwrap()
}
fn lines(entries: &[Value]) -> Vec<u8> {
    let mut bytes = Vec::new();
    for entry in entries {
        bytes.extend(serde_json::to_vec(entry).unwrap());
        bytes.push(b'\n');
    }
    bytes
}
fn outstanding(session: &str) -> Value {
    json!({"generation":{"appSession":session,"home":"home","spawnCounter":1},"requestId":1,"method":"item/fileChange/requestApproval",
        "state":"outstanding","replyWriteResult":"not-attempted","acknowledgment":null,"nativeParameters":{"threadId":"thread","itemId":"item"}})
}

#[test]
fn append_and_read_back_keep_the_exact_json_and_its_index_columns() {
    let f = Scratch::new();
    let mut ledger = f.open();
    assert!(!database_path(&f.ledger_path()).exists(), "nothing is created before the first write");
    ledger.start_session("s1", "c").unwrap();
    ledger.request_summary(&outstanding("s1")).unwrap();
    ledger.append(ended("s1")).unwrap();
    let written = ledger.snapshot()["entries"].clone();
    drop(ledger);
    assert_eq!(json!(f.entries()), written, "a reopen reads the same entries in the same order");
    assert!(!f.ledger_path().exists(), "no JSON Lines ledger is written");
    let ledger = f.open();
    let connection = ledger.store().unwrap().connection();
    let rows: Vec<(String, Option<String>, Option<String>, String, String)> = connection
        .prepare("SELECT kind, session, generation, origin, entry FROM ledger_entry ORDER BY seq").unwrap()
        .query_map([], |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?, r.get(3)?, r.get(4)?))).unwrap()
        .map(Result::unwrap).collect();
    assert_eq!(rows.iter().map(|r| r.0.as_str()).collect::<Vec<_>>(), ["session_started", "register_entry_summary", "session_ended"]);
    assert!(rows.iter().all(|r| r.1.as_deref() == Some("s1") && r.3 == "app"));
    assert_eq!(rows[1].2.as_deref(), written[1]["generation"].as_str());
    for (row, entry) in rows.iter().zip(written.as_array().unwrap()) {
        assert_eq!(&serde_json::from_str::<Value>(&row.4).unwrap(), entry, "stored as its exact JSON");
    }
}

#[test]
fn the_database_refuses_any_update_or_delete() {
    let f = Scratch::new();
    std::fs::write(f.ledger_path(), lines(&[started("old")])).unwrap();
    let ledger = f.open();
    let connection = ledger.store().unwrap().connection();
    for statement in [
        "UPDATE ledger_entry SET entry = '{}'",
        "DELETE FROM ledger_entry",
        "UPDATE legacy_import SET byte_length = 0",
        "DELETE FROM legacy_import",
        "UPDATE ledger_meta SET value = '0'",
        "DELETE FROM ledger_meta",
    ] {
        let refused = connection.execute(statement, []).unwrap_err().to_string();
        assert!(refused.contains("never"), "{statement}: {refused}");
    }
    drop(ledger);
    assert_eq!(f.entries(), vec![started("old")], "nothing was changed");
}

#[test]
fn a_batch_that_fails_midway_records_nothing() {
    let f = Scratch::new();
    let mut ledger = f.open();
    ledger.start_session("old", "c").unwrap();
    ledger.request_summary(&outstanding("old")).unwrap();
    drop(ledger);
    let before = f.entries();
    // The new session's marker and its RQ-06 ending are one transaction; it
    // fails after the marker is inserted.
    let mut ledger = f.open();
    FAIL_BATCH_AFTER.with(|n| n.set(Some(1)));
    let failed = ledger.start_session("new", "c").unwrap_err();
    assert!(failed.contains("injected failure inside the batch"), "{failed}");
    assert_eq!(f.entries(), before, "neither the marker nor the ending is recorded");
    assert!(ledger.start_session("new", "c").unwrap_err().contains("reopen"), "the failed writer is not reused");
    drop(ledger);
    let mut ledger = f.open();
    ledger.start_session("new", "c").unwrap();
    let after = f.entries();
    assert_eq!(after.len(), before.len() + 2);
    assert_eq!(after[before.len()]["kind"], "session_started");
    assert_eq!(after[before.len() + 1]["transition"], "RQ-06");
    let batches: Vec<i64> = ledger.store().unwrap().connection().prepare("SELECT batch FROM ledger_entry ORDER BY seq").unwrap()
        .query_map([], |r| r.get(0)).unwrap().map(Result::unwrap).collect();
    assert_eq!(batches[before.len()], batches[before.len() + 1], "the marker and its ending share one transaction");
}

#[test]
fn a_complete_json_lines_ledger_is_imported_once_and_never_written() {
    let f = Scratch::new();
    let earlier = vec![started("old"), ended("old")];
    let bytes = lines(&earlier);
    std::fs::write(f.ledger_path(), &bytes).unwrap();
    let mut ledger = f.open();
    let import = ledger.legacy_import().clone();
    assert_eq!(import["state"], "imported");
    assert_eq!(import["importedLines"], 2);
    assert_eq!(import["byteLength"], bytes.len());
    assert_eq!(import["content"], json!({"method":EXACT_BYTES,"value":crate::util::sha256_hex(&bytes)}));
    assert!(import["limit"].is_null());
    assert_eq!(ledger.snapshot()["entries"], json!(earlier));
    ledger.start_session("new", "c").unwrap();
    assert_eq!(ledger.snapshot()["entries"][2]["previousSessionEnd"], "clean", "the imported history is read as before");
    drop(ledger);
    // The import is recorded with its source; a relaunch does not import again.
    let ledger = f.open();
    assert_eq!(ledger.legacy_import()["state"], "imported earlier");
    assert_eq!(ledger.snapshot()["entries"].as_array().unwrap().len(), 3);
    let (path, length, lines_imported): (String, i64, i64) = ledger.store().unwrap().connection()
        .query_row("SELECT source_path, byte_length, imported_lines FROM legacy_import", [], |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?))).unwrap();
    assert_eq!((path.as_str(), length, lines_imported), (f.ledger_path().to_str().unwrap(), bytes.len() as i64, 2));
    let origins: Vec<String> = ledger.store().unwrap().connection().prepare("SELECT origin FROM ledger_entry ORDER BY seq").unwrap()
        .query_map([], |r| r.get(0)).unwrap().map(Result::unwrap).collect();
    assert_eq!(origins, ["legacy-import", "legacy-import", "app"]);
    assert_eq!(std::fs::read(f.ledger_path()).unwrap(), bytes, "the JSON Lines ledger is never written");
}

#[test]
fn a_torn_or_invalid_tail_is_a_limit_and_never_an_entry() {
    // Torn: the final line is not newline-closed.
    let f = Scratch::new();
    let mut bytes = lines(&[started("old")]);
    bytes.extend_from_slice(br#"{"kind":"session_ended","sess"#);
    std::fs::write(f.ledger_path(), &bytes).unwrap();
    let ledger = f.open();
    assert_eq!(ledger.snapshot()["entries"], json!([started("old")]));
    assert!(ledger.legacy_import()["limit"].as_str().unwrap().contains("not newline-closed"), "{}", ledger.legacy_import());
    drop(ledger);
    assert_eq!(std::fs::read(f.ledger_path()).unwrap(), bytes);
    // Invalid: a complete line that is not a ledger entry ends the import; the
    // later complete lines are not imported either.
    let g = Scratch::new();
    let mut bytes = lines(&[started("old")]);
    bytes.extend_from_slice(b"{\"kind\":\"session_started\",\"payload\":\"must-not-store\"}\n");
    bytes.extend(lines(&[ended("old")]));
    std::fs::write(g.ledger_path(), &bytes).unwrap();
    let ledger = g.open();
    assert_eq!(ledger.snapshot()["entries"], json!([started("old")]));
    let limit = ledger.legacy_import()["limit"].as_str().unwrap().to_owned();
    assert!(limit.contains("line 2") && limit.contains("is not a valid ledger entry") && limit.contains("2 newline-closed lines"), "{limit}");
    assert_eq!(ledger.legacy_import()["importedLines"], 1);
    drop(ledger);
    assert!(!String::from_utf8_lossy(&crate::recovery::stored_bytes(&g.ledger_path())).contains("must-not-store"), "{limit}");
    assert_eq!(std::fs::read(g.ledger_path()).unwrap(), bytes);
    // A relaunch reports the recorded import and imports nothing again.
    let again = g.open();
    assert_eq!(again.legacy_import()["state"], "imported earlier");
    assert_eq!(again.legacy_import()["limit"], json!(limit));
    assert_eq!(again.snapshot()["entries"], json!([started("old")]));
}

#[test]
fn a_changed_or_relocated_json_lines_ledger_is_not_imported_twice() {
    let f = Scratch::new();
    let first = lines(&[started("old")]);
    std::fs::write(f.ledger_path(), &first).unwrap();
    drop(f.open());
    // An earlier build appended after the import: reported, not imported.
    let mut changed = first.clone();
    changed.extend(lines(&[ended("old")]));
    std::fs::write(f.ledger_path(), &changed).unwrap();
    let ledger = f.open();
    assert_eq!(ledger.legacy_import()["state"], "changed since its import; not imported again");
    assert!(ledger.legacy_import()["limit"].as_str().unwrap().contains(&changed.len().to_string()));
    assert_eq!(ledger.snapshot()["entries"], json!([started("old")]));
    drop(ledger);
    // The same content under another name beside the database: matched by its content identity.
    std::fs::write(f.ledger_path(), &first).unwrap();
    let ledger = f.open();
    assert_eq!(ledger.legacy_import()["state"], "imported earlier");
    let imports: i64 = ledger.store().unwrap().connection().query_row("SELECT COUNT(*) FROM legacy_import", [], |r| r.get(0)).unwrap();
    assert_eq!(imports, 1);
    drop(ledger);
    // A database created without a JSON Lines ledger never imports one that appears later.
    let g = Scratch::new();
    g.open().start_session("new", "c").unwrap();
    std::fs::write(g.ledger_path(), &first).unwrap();
    let ledger = g.open();
    assert_eq!(ledger.legacy_import()["state"], "not imported");
    assert_eq!(ledger.snapshot()["entries"].as_array().unwrap().len(), 1);
}

#[test]
fn a_locked_or_unwritable_database_fails_visibly_without_fallback() {
    use std::os::unix::fs::PermissionsExt;
    let f = Scratch::new();
    let mut ledger = f.open();
    ledger.start_session("s", "c").unwrap();
    // Another App instance holds the database: the write is not confirmed.
    BUSY_TIMEOUT_MS.with(|t| t.set(Some(200)));
    let mut waiting = f.open();
    let other = rusqlite::Connection::open(database_path(&f.ledger_path())).unwrap();
    other.execute_batch("BEGIN EXCLUSIVE;").unwrap();
    let refused = waiting.append(ended("s")).unwrap_err();
    assert!(refused.contains("not confirmed") && refused.contains("locked"), "{refused}");
    other.execute_batch("COMMIT;").unwrap();
    BUSY_TIMEOUT_MS.with(|t| t.set(None));
    assert_eq!(f.entries(), vec![f.entries()[0].clone()], "nothing was recorded");
    drop(waiting);
    // A read-only database: opening reads it; a write is refused visibly.
    if unsafe { libc::geteuid() } != 0 {
        drop(ledger);
        let database = database_path(&f.ledger_path());
        std::fs::set_permissions(&database, std::fs::Permissions::from_mode(0o400)).unwrap();
        let mut read_only = f.open();
        let refused = read_only.append(ended("s")).unwrap_err();
        assert!(refused.contains("not confirmed") && refused.contains("readonly"), "{refused}");
        std::fs::set_permissions(&database, std::fs::Permissions::from_mode(0o600)).unwrap();
        assert!(!f.ledger_path().exists(), "no fallback location was written");
        assert_eq!(f.entries().len(), 1);
    }
}

#[test]
fn concurrent_app_instances_append_in_commit_order() {
    let f = Scratch::new();
    let mut first = f.open();
    first.start_session("a", "c").unwrap();
    let mut second = f.open();
    second.append(ended("a")).unwrap();
    first.append(started("b")).unwrap();
    let kinds: Vec<String> = f.entries().iter().map(|e| e["kind"].as_str().unwrap().to_owned()).collect();
    assert_eq!(kinds, ["session_started", "session_ended", "session_started"], "both instances' entries, in commit order");
}
