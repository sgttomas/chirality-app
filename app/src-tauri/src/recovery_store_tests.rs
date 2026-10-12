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
    let written = ledger.recorded_entries().clone();
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
    assert_eq!(ledger.recorded_entries(), json!(earlier));
    ledger.start_session("new", "c").unwrap();
    assert_eq!(ledger.recorded_entries()[2]["previousSessionEnd"], "clean", "the imported history is read as before");
    drop(ledger);
    // The import is recorded with its source; a relaunch does not import again.
    let ledger = f.open();
    assert_eq!(ledger.legacy_import()["state"], "imported earlier");
    assert_eq!(ledger.recorded_entries().as_array().unwrap().len(), 3);
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
    assert_eq!(ledger.recorded_entries(), json!([started("old")]));
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
    assert_eq!(ledger.recorded_entries(), json!([started("old")]));
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
    assert_eq!(again.recorded_entries(), json!([started("old")]));
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
    assert_eq!(ledger.recorded_entries(), json!([started("old")]));
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
    assert_eq!(ledger.recorded_entries().as_array().unwrap().len(), 1);
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

// ---- The held entries (DEL-01-02 §7): bounded, and read as the whole ledger is.

fn generation(session: &str) -> Value {
    json!({"appSession":session,"home":"home-1","spawnCounter":1})
}
fn index_row(session: &str, thread: &str, tags: Value, state: &str, item: Option<&str>) -> Value {
    let reference = crate::recovery::generation_ref(&generation(session)).unwrap();
    let mut execution = json!({"state":state,"at":"2026-10-12T00:00:00.000Z"});
    if state == "turn-live" {
        execution["liveTurn"] = json!("turn-1");
        execution["openItems"] = json!(item.map(|i| vec![json!({"turnId":"turn-1","itemId":i,"itemType":"commandExecution"})]).unwrap_or_default());
    }
    json!({"kind":"conversation_index","session":session,"at":"2026-10-12T00:00:00.000Z","threadId":thread,"home":"H-acct","project":"P",
        "tags":tags,"lastObservedExecution":execution,"lastLoadedGeneration":reference})
}
fn request(session: &str, id: u64, state: &str) -> Value {
    let mut r = json!({"generation":generation(session),"requestId":id,"method":"item/commandExecution/requestApproval",
        "nativeParameters":{"threadId":"A","turnId":"turn-1","itemId":format!("item-{id}")},"state":state,"replyWriteResult":"not-attempted","classification":"known-answerable"});
    if state == "answered" {
        r["replyWriteResult"] = json!("written");
        r["settlement"] = json!({"origin":"person-via-interaction","actor":"person:p (identity not verified)","content":{"decision":"accept"}});
    }
    r
}
/// Three App sessions: conversations re-indexed per item, a tag added and a
/// delayed row without it, requests answered, left listed and re-listed after
/// closing, and a stop request left sent.
fn eventful_ledger(f: &Scratch) {
    use crate::stop_records::{ledger_entry, person, Cause, StopRequest};
    let mut ledger = f.open();
    ledger.start_session("s1", "c").unwrap();
    for n in 0..6 {
        for thread in ["A", "B"] {
            ledger.append(index_row("s1", thread, json!([]), "turn-live", Some(&format!("i{n}")))).unwrap();
            ledger.append(index_row("s1", thread, json!([]), "turn-live", None)).unwrap();
        }
    }
    let tag = json!([{"owner":"receiver","value":"run:1","seq":1}]);
    ledger.append(index_row("s1", "A", tag.clone(), "turn-live", None)).unwrap();
    // Queued before the tag and recorded after it: the latest row lacks the tag.
    ledger.append(index_row("s1", "A", json!([]), "observation-lost", Some("i9"))).unwrap();
    ledger.request_summary(&request("s1", 1, "outstanding")).unwrap();
    ledger.request_summary(&request("s1", 1, "answered")).unwrap();
    ledger.request_summary(&request("s1", 2, "outstanding")).unwrap();
    ledger.request_summary(&request("s1", 3, "outstanding")).unwrap();
    ledger.request_summary(&request("s1", 3, "answered")).unwrap();
    ledger.request_summary(&request("s1", 3, "outstanding")).unwrap();
    let mut stop = StopRequest::requested(&generation("s1"), "H-acct", "A", "turn-1", Cause::PersonInterrupt, &person("p")).unwrap();
    ledger.append(ledger_entry("s1", stop.record())).unwrap();
    stop.sent("app:client:1", &json!(7)).unwrap();
    ledger.append(ledger_entry("s1", stop.record())).unwrap();
    drop(ledger);
    // s1 ended without a record: s2's start closes request 2 (RQ-06) and the stop request (SR-08).
    let mut ledger = f.open();
    ledger.start_session("s2", "c").unwrap();
    for n in 0..4 {
        ledger.append(index_row("s2", "A", tag.clone(), "turn-live", Some(&format!("j{n}")))).unwrap();
    }
    ledger.append(index_row("s2", "A", tag.clone(), "indexed", None)).unwrap();
    ledger.request_summary(&request("s2", 4, "outstanding")).unwrap();
    ledger.request_summary(&request("s2", 4, "answered")).unwrap();
    ledger.append(ended("s2")).unwrap();
    drop(ledger);
    f.open().start_session("s3", "c").unwrap();
}

#[test]
fn the_held_entries_read_as_the_whole_ledger_reads() {
    let f = Scratch::new();
    eventful_ledger(&f);
    let ledger = f.open();
    let held = ledger.current_entries().to_vec();
    let all = ledger.recorded_entries().as_array().unwrap().clone();
    assert!(held.len() * 2 < all.len(), "{} held of {}", held.len(), all.len());
    // Every held entry is a recorded one, in ledger order.
    let mut rest = all.iter();
    assert!(held.iter().all(|h| rest.any(|a| a == h)));
    use crate::recovery::{latest_execution_rows, recorded_startup_request_events, startup_request_closures, tags_of, History, RecoveryCustodyView};
    assert_eq!(latest_execution_rows(History::new(&held, &[])), latest_execution_rows(History::new(&all, &[])));
    let at = |mut rows: Vec<Value>| { for r in &mut rows { r["at"] = json!("at"); } rows };
    let (h, hl) = startup_request_closures(&held, "s4");
    let (a, al) = startup_request_closures(&all, "s4");
    assert_eq!((at(h), hl), (at(a), al));
    assert!(startup_request_closures(&all, "s4").1.iter().any(|l| l.contains("later listed summary")), "the re-listed request's limit is kept");
    assert_eq!(recorded_startup_request_events(&held), recorded_startup_request_events(&all));
    assert_eq!(recorded_startup_request_events(&all).len(), 1, "request 2's RQ-06 ending");
    for thread in ["A", "B"] {
        assert_eq!(tags_of(&held, "H-acct", thread, "receiver"), tags_of(&all, "H-acct", thread, "receiver"));
    }
    assert_eq!(tags_of(&held, "H-acct", "A", "receiver").len(), 1, "the tag survives the delayed row without it");
    assert_eq!(crate::stop_records::outcomes(&held, &[], "s3"), crate::stop_records::outcomes(&all, &[], "s3"));
    let view = |rows: &[Value]| {
        let mut v = RecoveryCustodyView::from_owner("s3", Some(rows), json!({}), 0, None).snapshot();
        let mut limits: Vec<Value> = v["limits"].as_array().unwrap().clone();
        limits.sort_by_key(|l| l.to_string());
        limits.dedup();
        v["limits"] = json!(limits);
        v
    };
    assert_eq!(view(&held), view(&all), "the custody view (limits read as a set)");
    // In this process a request closed here stays held: a repeated summary is
    // recognised against it, as against the whole ledger.
    let mut ledger = f.open();
    ledger.request_summary(&request("s3", 5, "outstanding")).unwrap();
    ledger.request_summary(&request("s3", 5, "answered")).unwrap();
    let again = request("s3", 5, "answered");
    let all = ledger.recorded_entries().as_array().unwrap().clone();
    assert_eq!(
        crate::recovery::RecoveryLedger::request_summary_entry_in(&again, History::new(ledger.current_entries(), &[])).unwrap(),
        crate::recovery::RecoveryLedger::request_summary_entry(&again, &all).unwrap(),
    );
    assert!(crate::recovery::RecoveryLedger::request_summary_entry(&again, &all).unwrap().is_none());
}

#[test]
fn an_index_column_that_disagrees_with_its_entry_refuses_the_open() {
    let f = Scratch::new();
    let mut ledger = f.open();
    ledger.start_session("s", "c").unwrap();
    ledger.append(index_row("s", "A", json!([]), "indexed", None)).unwrap();
    drop(ledger);
    // Outside the App: the triggers dropped and a column rewritten.
    let db = rusqlite::Connection::open(database_path(&f.ledger_path())).unwrap();
    db.execute_batch("DROP TRIGGER ledger_entry_never_rewritten; UPDATE ledger_entry SET currency = 'other' WHERE kind = 'conversation_index';").unwrap();
    drop(db);
    let refused = RecoveryLedger::open(f.ledger_path()).err().unwrap();
    assert!(refused.contains("index columns do not match"), "{refused}");
}

/// A JSON Lines ledger of `rows` entries over ten conversations: per item an
/// index row as it opens and as it closes, and every eighth item a request
/// answered (two summaries).
fn scale_jsonl(path: &Path, rows: usize) {
    use std::io::Write;
    let mut out = std::io::BufWriter::new(std::fs::File::create(path).unwrap());
    writeln!(out, "{}", started("scale")).unwrap();
    let mut written = 1;
    let mut item = 0u64;
    while written < rows {
        item += 1;
        let thread = format!("thread-{}", item % 10);
        let mut lines = vec![index_row("scale", &thread, json!([]), "turn-live", Some(&format!("item-{item}"))), index_row("scale", &thread, json!([]), "turn-live", None)];
        if item % 8 == 0 {
            for state in ["outstanding", "answered"] {
                lines.push(RecoveryLedger::request_summary_entry(&request("scale", item, state), &[]).unwrap().unwrap());
            }
        }
        for line in lines.into_iter().take(rows - written) {
            writeln!(out, "{line}").unwrap();
            written += 1;
        }
    }
}

// The scale check (DEL-01-02 §7; the 2026-10-12 measurement): from 1,000 to
// 100,000 rows over the same conversations, the host holds the same entries,
// its status carries no more, and one fact (an append and the observation the
// host caches) costs no more; nothing is copied per fact.
#[test]
fn host_status_and_one_fact_stay_flat_from_1k_to_100k_rows() {
    let measure = |rows: usize| {
        let f = Scratch::new();
        scale_jsonl(&f.ledger_path(), rows);
        let host = crate::hosting::Host::new();
        host.configure_recovery(f.ledger_path()).unwrap();
        let held = host.recovery_entries().len();
        let status = serde_json::to_vec(&host.snapshot()).unwrap().len();
        let mut ledger = f.open();
        assert_eq!(ledger.recorded_count().unwrap(), rows as u64 + 1, "every row imported, and the new session's marker");
        let start = std::time::Instant::now();
        for n in 0..20 {
            ledger.append(index_row("scale", &format!("thread-{}", n % 10), json!([]), "indexed", None)).unwrap();
            let observation = ledger.observation();
            assert!(observation.rows.len() <= held + 1);
        }
        let fact = start.elapsed() / 20;
        (held, status, fact)
    };
    let (small_held, small_status, small_fact) = measure(1_000);
    let (large_held, large_status, large_fact) = measure(100_000);
    println!("scale: held {small_held} / {large_held}, status {small_status} / {large_status} bytes, one fact {small_fact:?} / {large_fact:?}");
    assert_eq!(small_held, large_held, "the held entries do not grow with the ledger");
    assert!(large_status <= small_status + 64, "host status {small_status} -> {large_status} bytes");
    assert!(large_fact <= small_fact * 4 + std::time::Duration::from_millis(20), "one fact {small_fact:?} -> {large_fact:?}");
}
