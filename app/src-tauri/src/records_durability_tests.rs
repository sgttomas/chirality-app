//! Crash and torn-write witnesses for the two append-only writers: the App
//! recovery ledger (`recovery::RecoveryLedger::append`, DEL-01-02 §7; its
//! SQLite database) and the RS run/act log writer (`records::append_reserved`,
//! RS §14.1).
//!
//! A real child process (this test binary, re-run on `durability_child`)
//! appends in a loop and is SIGKILLed at random points; a short write is
//! produced in a child by `RLIMIT_FSIZE` (the kernel writes what fits, then
//! refuses with EFBIG). Each result is checked from the bytes on disk and by
//! reopening the reader and the writer. What this cannot show: loss of data
//! the OS acknowledged but had not reached the device at a power failure;
//! `sync_data`/`sync_all` are called, but whether the device honours them is
//! not observable from a process (a killed process leaves the page cache intact).
use super::*;
use std::io::{BufRead, BufReader};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};

const CHILD: &str = "records::durability_tests::durability_child";
const LEDGER_SESSION: &str = "app-session:durability";

fn scratch(prefix: &str) -> PathBuf {
    let p = std::env::temp_dir().join(crate::util::opaque_id(prefix).unwrap());
    std::fs::create_dir_all(&p).unwrap();
    std::fs::canonicalize(p).unwrap()
}
/// A small xorshift generator; the seed is printed so a run can be repeated
/// (`CHIRALITY_DURABILITY_SEED`).
struct Rng(u64);
impl Rng {
    fn new() -> Self {
        let seed = std::env::var("CHIRALITY_DURABILITY_SEED").ok().and_then(|s| s.parse().ok())
            .unwrap_or_else(|| std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos() as u64 | 1);
        println!("durability seed {seed}");
        Self(seed)
    }
    fn below(&mut self, n: u64) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0 % n.max(1)
    }
}
fn kills() -> usize {
    std::env::var("CHIRALITY_DURABILITY_KILLS").ok().and_then(|s| s.parse().ok()).unwrap_or(12)
}
fn child(mode: &str, path: &Path) -> Command {
    let mut c = Command::new(std::env::current_exe().unwrap());
    c.args([CHILD, "--exact", "--ignored", "--nocapture", "--test-threads=1"])
        .env("CHIRALITY_DURABILITY_CHILD", mode)
        .env("CHIRALITY_DURABILITY_PATH", path)
        .stdout(Stdio::piped())
        .stderr(Stdio::null());
    c
}
/// The child's one result line.
fn result_of(output: &std::process::Output) -> Value {
    let text = String::from_utf8_lossy(&output.stdout);
    let line = text.lines().find_map(|l| l.split_once("DURABILITY-RESULT ").map(|(_, r)| r)).unwrap_or_else(|| panic!("no child result: {text}"));
    serde_json::from_str(line).unwrap()
}
fn ledger_entry() -> Value {
    crate::recovery::RecoveryLedger::session_end_entry(LEDGER_SESSION, "quit", &[]).unwrap()
}
fn rs_body(pad: usize) -> Value {
    json!({"label":"unresolvable reference","subjectRef":"durability witness","detail":"x".repeat(pad)})
}
/// The RS log a witness writes, in project `root`.
fn rs_log(root: &Path) -> PathBuf {
    crate::storage::project_log(root, None, "durability-writer")
}
/// The bytes on disk, split at LF: the complete lines and the unclosed tail.
fn lines(path: &Path) -> (Vec<Vec<u8>>, Vec<u8>) {
    let bytes = std::fs::read(path).unwrap_or_default();
    let mut parts: Vec<Vec<u8>> = bytes.split(|b| *b == b'\n').map(<[u8]>::to_vec).collect();
    let tail = parts.pop().unwrap_or_default();
    (parts, tail)
}
/// Drop an unclosed tail (the test's own repair, so the next kill starts from
/// a closed file; neither writer repairs it, W-0 repair is not implemented).
fn cut_tail(path: &Path) {
    let bytes = std::fs::read(path).unwrap();
    let keep = bytes.iter().rposition(|b| *b == b'\n').map_or(0, |i| i + 1);
    std::fs::write(path, &bytes[..keep]).unwrap();
}

/// The child: `ledger-loop` / `rs-loop` append until killed; `ledger-short` /
/// `rs-short` set the file-size limit so the next append lands only part of
/// its line, then lift the limit and append again. Does nothing unless run by
/// a witness below.
#[test]
#[ignore = "child process of the durability witnesses"]
fn durability_child() {
    let (Ok(mode), Ok(path)) = (std::env::var("CHIRALITY_DURABILITY_CHILD"), std::env::var("CHIRALITY_DURABILITY_PATH")) else { return };
    let path = PathBuf::from(path);
    fn report(v: Value) -> ! { println!("DURABILITY-RESULT {v}"); std::process::exit(0) }
    match mode.as_str() {
        "ledger-loop" => {
            let mut ledger = match crate::recovery::RecoveryLedger::open(path) { Ok(l) => l, Err(e) => report(json!({"open":e})) };
            loop {
                if let Err(e) = ledger.append(ledger_entry()) { report(json!({"append":e})) }
            }
        }
        "rs-loop" => {
            let log = rs_log(&path);
            loop {
                if let Err(e) = append(&log, "evidence_limit", &APP_WRITER, rs_body(48 * 1024)) { report(json!({"append":e})) }
            }
        }
        "ledger-short" | "rs-short" => {
            let target = if mode == "ledger-short" { crate::recovery::database_path(&path) } else { rs_log(&path) };
            let size = std::fs::metadata(&target).map(|m| m.len()).unwrap_or(0);
            // The ledger: a batch that needs new database pages, so its commit
            // writes past the limit (the database's size) after the journal.
            let line = if mode == "ledger-short" { 0 } else { 2048 };
            let mut ledger = (mode == "ledger-short").then(|| crate::recovery::RecoveryLedger::open(path.clone()).unwrap());
            let mut attempt = || match &mut ledger { Some(l) => l.append_batch(vec![ledger_entry(); 64]), None => append(&target, "evidence_limit", &APP_WRITER, rs_body(1800)).map(|_| ()) };
            unsafe { libc::signal(libc::SIGXFSZ, libc::SIG_IGN); }
            let mut limit = libc::rlimit { rlim_cur: 0, rlim_max: 0 };
            unsafe { libc::getrlimit(libc::RLIMIT_FSIZE, &mut limit); }
            let original = limit.rlim_cur;
            limit.rlim_cur = size + (line as u64) / 2;
            unsafe { libc::setrlimit(libc::RLIMIT_FSIZE, &limit); }
            let first = attempt();
            limit.rlim_cur = original;
            unsafe { libc::setrlimit(libc::RLIMIT_FSIZE, &limit); }
            let second = attempt();
            report(json!({"first":first.err(),"second":second.err(),"sizeBefore":size}));
        }
        other => panic!("unknown child mode {other}"),
    }
}

/// Starts the loop child, waits until it has grown the file, lets it run a
/// random while more, and SIGKILLs it.
fn kill_mid_loop(mode: &str, path: &Path, file: &Path, rng: &mut Rng) {
    let before = std::fs::metadata(file).map(|m| m.len()).unwrap_or(0);
    let mut c = child(mode, path).spawn().unwrap();
    let deadline = Instant::now() + Duration::from_secs(20);
    while std::fs::metadata(file).map(|m| m.len()).unwrap_or(0) <= before {
        assert!(Instant::now() < deadline, "{mode}: the child never appended");
        if let Ok(Some(status)) = c.try_wait() {
            let mut out = String::new();
            BufReader::new(c.stdout.take().unwrap()).lines().for_each(|l| { out.push_str(&l.unwrap()); });
            panic!("{mode}: the child stopped before being killed ({status}): {out}");
        }
        std::thread::sleep(Duration::from_micros(200));
    }
    std::thread::sleep(Duration::from_micros(rng.below(30_000)));
    unsafe { libc::kill(c.id() as i32, libc::SIGKILL); }
    c.wait().unwrap();
}

/// Every entry the ledger database holds, read on a separate connection after
/// SQLite's own integrity check (the open also rolls back a hot journal).
fn ledger_rows(path: &Path) -> Vec<Value> {
    let db = rusqlite::Connection::open(crate::recovery::database_path(path)).unwrap();
    let check: String = db.query_row("PRAGMA integrity_check", [], |r| r.get(0)).unwrap();
    assert_eq!(check, "ok");
    let mut statement = db.prepare("SELECT entry FROM ledger_entry ORDER BY seq").unwrap();
    let rows = statement.query_map([], |r| r.get::<_, String>(0)).unwrap();
    rows.map(|r| serde_json::from_str(&r.unwrap()).unwrap()).collect()
}

// DEL-01-02 §7: after a SIGKILL at a random point of the ledger writer's loop,
// the database passes its integrity check, every entry validates, no
// committed entry is lost (the count only grows), and a reopened ledger
// appends again. A transaction cut by the kill leaves nothing of itself: its
// journal is rolled back by the next open, so there is no torn tail to refuse.
#[test]
fn sigkill_mid_ledger_append_leaves_only_committed_entries() {
    let dir = scratch("ledger-kill-");
    let path = dir.join("recovery.ledger.jsonl");
    let database = crate::recovery::database_path(&path);
    let mut journal = database.as_os_str().to_owned();
    journal.push("-journal");
    let journal = PathBuf::from(journal);
    let mut rng = Rng::new();
    let (mut hot, mut appended) = (0, 0);
    for round in 0..kills() {
        kill_mid_loop("ledger-loop", &path, &database, &mut rng);
        if std::fs::symlink_metadata(&journal).is_ok() { hot += 1; }
        let rows = ledger_rows(&path);
        for row in &rows {
            crate::recovery::RecoveryLedger::validate_pointer_entry(row).unwrap();
        }
        assert!(rows.len() >= appended, "round {round}: {} entries after {appended}", rows.len());
        let mut ledger = crate::recovery::RecoveryLedger::open(path.clone()).unwrap_or_else(|e| panic!("round {round}: {e}"));
        ledger.append(ledger_entry()).unwrap();
        drop(ledger);
        appended = ledger_rows(&path).len();
        assert!(!path.exists(), "no JSON Lines file is written");
    }
    println!("ledger: {} kills, {hot} left a journal, {appended} entries", kills());
    std::fs::remove_dir_all(dir).unwrap();
}

// RS §14.1/§14.2: after a SIGKILL at a random point of the RS writer's loop
// (48 KiB lines), the reader returns every complete entry in sequence and
// reports an unclosed tail only as "partial entry at end (not read)"; a
// reopened writer appends to a closed log, and refuses (nothing written) on a
// torn one: W-0 repair, which RS FC-2 designs, is not implemented.
#[test]
fn sigkill_mid_rs_append_leaves_complete_entries_or_a_refused_torn_tail() {
    let root = scratch("rs-kill-");
    let log = rs_log(&root);
    let mut rng = Rng::new();
    let (mut torn, mut entries) = (0, 0);
    for round in 0..kills() {
        kill_mid_loop("rs-loop", &root, &log, &mut rng);
        let (read, limits) = read_log(&log);
        let (complete, tail) = lines(&log);
        assert_eq!(read.len(), complete.len(), "round {round}: every complete line is an entry");
        assert_eq!(read.iter().map(|e| e["seq"].as_u64().unwrap()).collect::<Vec<_>>(), (1..=read.len() as u64).collect::<Vec<_>>());
        entries = read.len();
        if tail.is_empty() {
            assert!(limits.is_empty(), "round {round}: {limits:?}");
            append(&log, "evidence_limit", &APP_WRITER, rs_body(16)).unwrap();
        } else {
            torn += 1;
            assert_eq!(limits.len(), 1, "{limits:?}");
            assert!(limits[0].ends_with("partial entry at end (not read)"), "{limits:?}");
            let bytes = std::fs::read(&log).unwrap();
            let error = append(&log, "evidence_limit", &APP_WRITER, rs_body(16)).unwrap_err();
            assert!(error.contains("partial line"), "{error}");
            assert_eq!(std::fs::read(&log).unwrap(), bytes, "nothing written");
            cut_tail(&log);
        }
    }
    println!("rs: {} kills, {torn} torn tails, {entries} complete entries", kills());
    std::fs::remove_dir_all(root).unwrap();
}

// A short write (RLIMIT_FSIZE at the database's size: the commit's write of
// new pages fails with EFBIG) in a child: the ledger reports the batch not
// confirmed and keeps none of it; once the limit is lifted the same writer's
// next batch is recorded whole; the database passes its integrity check and
// holds the earlier entries and that batch only.
#[test]
fn a_short_ledger_write_is_reported_and_leaves_nothing_of_its_batch() {
    let dir = scratch("ledger-short-");
    let path = dir.join("recovery.ledger.jsonl");
    let mut ledger = crate::recovery::RecoveryLedger::open(path.clone()).unwrap();
    for _ in 0..3 { ledger.append(ledger_entry()).unwrap(); }
    drop(ledger);
    let result = result_of(&child("ledger-short", &path).output().unwrap());
    let first = result["first"].as_str().unwrap_or_else(|| panic!("{result}"));
    assert!(first.starts_with("recovery ledger append not confirmed"), "{result}");
    assert!(result["second"].is_null(), "{result}");
    assert_eq!(ledger_rows(&path).len(), 3 + 64, "the failed batch left nothing; the next is whole");
    drop(crate::recovery::RecoveryLedger::open(path.clone()).unwrap());
    println!("ledger short write: {first}");
    std::fs::remove_dir_all(dir).unwrap();
}

// The RS writer under a short write: the append reports a write error; the log
// keeps a torn tail the reader reports as a limit; the next append to that log
// refuses with nothing written; and, because the writer requires a complete
// project record set (RecordSet::Complete), an append to any other log of the
// project refuses too until the tail is dealt with. Only the person's explicit
// end (ReadableBesideIncomplete) records beside it.
#[test]
fn a_short_rs_write_is_reported_and_blocks_the_project_record_set() {
    let root = scratch("rs-short-");
    let log = rs_log(&root);
    for _ in 0..3 { append(&log, "evidence_limit", &APP_WRITER, rs_body(16)).unwrap(); }
    let result = result_of(&child("rs-short", &root).output().unwrap());
    let first = result["first"].as_str().unwrap_or_else(|| panic!("{result}"));
    assert!(first.starts_with("write: "), "{result}");
    assert!(result["second"].as_str().unwrap().contains("partial line"), "{result}");
    let (read, limits) = read_log(&log);
    assert_eq!(read.len(), 3);
    assert!(limits == [format!("{}: partial entry at end (not read)", log.file_name().unwrap().to_string_lossy())], "{limits:?}");
    let other = crate::storage::project_log(&root, Some("run:durability"), "app-writer:local");
    let error = append_project_reserved(&root, "run:durability", "app-writer:local", "evidence_limit", &APP_WRITER, rs_body(16), "rec:app:durability-1", "2026-10-12T00:00:00.000Z").unwrap_err();
    assert!(error.contains("record-set conflict/incomplete"), "{error}");
    assert!(!other.exists(), "nothing written to the other log");
    let late = append_project_reserved_in(&root, "run:durability", "app-writer:local", "evidence_limit", &APP_WRITER, rs_body(16), "rec:app:durability-1", "2026-10-12T00:00:00.000Z", RecordSet::ReadableBesideIncomplete);
    assert!(late.is_ok(), "{late:?}");
    std::fs::remove_dir_all(root).unwrap();
}

// An injected directory-sync failure after the line is written and the file
// synced (storage::fail_directory_for_test): the caller is told the append
// failed, the reader shows the complete entry, and a retry with the same
// reserved identity refuses ("record identity conflict"), so no duplicate.
#[test]
fn an_uncertain_rs_sync_leaves_the_entry_and_a_retry_writes_no_duplicate() {
    let root = scratch("rs-sync-");
    let log = rs_log(&root);
    append(&log, "evidence_limit", &APP_WRITER, rs_body(16)).unwrap();
    crate::storage::fail_directory_for_test(Some(log.parent().unwrap().to_path_buf()));
    let failed = append_with_id(&log, "evidence_limit", &APP_WRITER, rs_body(16), "rec:app:durability-sync");
    crate::storage::fail_directory_for_test(None);
    assert!(failed.as_ref().is_err_and(|e| e.contains("injected failure")), "{failed:?}");
    let (read, limits) = read_log(&log);
    assert!(limits.is_empty());
    assert_eq!(read.last().unwrap()["recordId"], "rec:app:durability-sync", "the line landed although the caller saw a failure");
    let retry = append_with_id(&log, "evidence_limit", &APP_WRITER, rs_body(16), "rec:app:durability-sync").unwrap_err();
    assert!(retry.contains("record identity conflict"), "{retry}");
    assert_eq!(read_log(&log).0.len(), 2);
    std::fs::remove_dir_all(root).unwrap();
}
