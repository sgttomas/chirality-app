//! Crash and torn-write witnesses for the two append-only writers: the App
//! recovery ledger (`recovery::RecoveryLedger::append`, DEL-01-02 §7) and the
//! RS run/act log writer (`records::append_reserved`, RS §14.1).
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
/// Drop an unclosed ledger tail (the test's own repair, so the next kill starts
/// from a closed file; the ledger does not repair it).
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
        "ledger-short" | "rs-short" | "rs-short-only" => {
            let target = if mode == "ledger-short" { path.clone() } else { rs_log(&path) };
            let line = if mode == "ledger-short" { serde_json::to_vec(&ledger_entry()).unwrap().len() } else { 2048 };
            let size = std::fs::metadata(&target).map(|m| m.len()).unwrap_or(0);
            let mut ledger = (mode == "ledger-short").then(|| crate::recovery::RecoveryLedger::open(path.clone()).unwrap());
            let mut attempt = || match &mut ledger { Some(l) => l.append(ledger_entry()), None => append(&target, "evidence_limit", &APP_WRITER, rs_body(1800)).map(|_| ()) };
            unsafe { libc::signal(libc::SIGXFSZ, libc::SIG_IGN); }
            let mut limit = libc::rlimit { rlim_cur: 0, rlim_max: 0 };
            unsafe { libc::getrlimit(libc::RLIMIT_FSIZE, &mut limit); }
            let original = limit.rlim_cur;
            limit.rlim_cur = size + (line as u64) / 2;
            unsafe { libc::setrlimit(libc::RLIMIT_FSIZE, &limit); }
            let first = attempt();
            limit.rlim_cur = original;
            unsafe { libc::setrlimit(libc::RLIMIT_FSIZE, &limit); }
            let second = if mode == "rs-short-only" { Ok(()) } else { attempt() };
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

// DEL-01-02 §7: after a SIGKILL at a random point of the ledger writer's loop,
// every complete line parses and validates, at most the final line is torn,
// and a reopened ledger reads every complete line and appends again; an
// unclosed tail is refused by the reader ("not newline-closed; bytes
// preserved"), never read as a record, and its bytes are left as they are.
#[test]
fn sigkill_mid_ledger_append_leaves_complete_lines_or_a_refused_torn_tail() {
    let dir = scratch("ledger-kill-");
    let path = dir.join("recovery.ledger.jsonl");
    let mut rng = Rng::new();
    let (mut torn, mut appended) = (0, 0);
    for round in 0..kills() {
        kill_mid_loop("ledger-loop", &path, &path, &mut rng);
        let (complete, tail) = lines(&path);
        for line in &complete {
            crate::recovery::RecoveryLedger::validate_pointer_entry(&serde_json::from_slice(line).unwrap()).unwrap();
        }
        appended = complete.len();
        if tail.is_empty() {
            let mut ledger = crate::recovery::RecoveryLedger::open(path.clone()).unwrap_or_else(|e| panic!("round {round}: {e}"));
            assert_eq!(ledger.snapshot()["entries"].as_array().unwrap().len(), complete.len());
            ledger.append(ledger_entry()).unwrap();
        } else {
            torn += 1;
            let bytes = std::fs::read(&path).unwrap();
            let error = crate::recovery::RecoveryLedger::open(path.clone()).err().unwrap();
            assert!(error.contains("final ledger record is not newline-closed; bytes preserved"), "{error}");
            assert_eq!(std::fs::read(&path).unwrap(), bytes, "the reader leaves the bytes");
            cut_tail(&path);
        }
    }
    println!("ledger: {} kills, {torn} torn tails, {appended} complete lines", kills());
    std::fs::remove_dir_all(dir).unwrap();
}

// RS §14.1/§14.2: after a SIGKILL at a random point of the RS writer's loop
// (48 KiB lines), the reader returns every complete entry in sequence and
// reports an unclosed tail only as "partial entry at end (not read)"; a
// reopened writer appends, after W-0 on a torn one (the torn bytes kept).
#[test]
fn sigkill_mid_rs_append_leaves_complete_entries_or_a_recovered_torn_tail() {
    let root = scratch("rs-kill-");
    let log = rs_log(&root);
    let mut rng = Rng::new();
    let (mut torn, mut entries) = (0, 0);
    for round in 0..kills() {
        kill_mid_loop("rs-loop", &root, &log, &mut rng);
        let (read, limits) = read_log(&log);
        let (complete, tail) = lines(&log);
        let text: Vec<String> = complete.iter().map(|l| String::from_utf8_lossy(l).into_owned()).collect();
        let recovered = recovered_partial_lines(&text.iter().map(String::as_str).collect::<Vec<_>>()).len();
        assert_eq!(read.len() + recovered, complete.len(), "round {round}: every complete line not named by W-0 is an entry");
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
            append(&log, "evidence_limit", &APP_WRITER, rs_body(16)).unwrap();
            assert!(std::fs::read(&log).unwrap().starts_with(&bytes), "the torn bytes are kept");
            let (read, limits) = read_log(&log);
            assert!(limits.is_empty(), "{limits:?}");
            assert_eq!(read[read.len() - 2]["body"]["label"], PARTIAL_NOT_RECOVERED);
        }
    }
    println!("rs: {} kills, {torn} torn tails, {entries} complete entries", kills());
    std::fs::remove_dir_all(root).unwrap();
}

// A short write (RLIMIT_FSIZE: part of the line lands, then EFBIG) in a child:
// the ledger reports the append not confirmed and keeps nothing in memory; its
// next append in the same process refuses ("unclosed final record; bytes
// preserved"); a reopened ledger refuses the file; the bytes stay as written.
#[test]
fn a_short_ledger_write_is_reported_and_its_torn_tail_refused() {
    let dir = scratch("ledger-short-");
    let path = dir.join("recovery.ledger.jsonl");
    let mut ledger = crate::recovery::RecoveryLedger::open(path.clone()).unwrap();
    for _ in 0..3 { ledger.append(ledger_entry()).unwrap(); }
    let result = result_of(&child("ledger-short", &path).output().unwrap());
    let first = result["first"].as_str().unwrap_or_else(|| panic!("{result}"));
    assert!(first.starts_with("recovery ledger append not confirmed"), "{result}");
    assert!(result["second"].as_str().unwrap().contains("unclosed final record; bytes preserved"), "{result}");
    let (complete, tail) = lines(&path);
    assert_eq!(complete.len(), 3);
    assert!(!tail.is_empty(), "part of the line landed: {} bytes", tail.len());
    let bytes = std::fs::read(&path).unwrap();
    assert!(crate::recovery::RecoveryLedger::open(path.clone()).err().unwrap().contains("not newline-closed; bytes preserved"));
    assert_eq!(std::fs::read(&path).unwrap(), bytes);
    println!("ledger short write: {} of {} bytes landed; {first}", tail.len(), serde_json::to_vec(&ledger_entry()).unwrap().len() + 1);
    std::fs::remove_dir_all(dir).unwrap();
}

// The RS writer under a short write (RS §14.1 W-0, FC-2; §13.7 Failures): the
// append reports a write error and leaves a torn tail, which the reader
// reports only as a partial. Other logs of the project stay writable beside
// it, while a genuinely unreadable line elsewhere still leaves the set
// incomplete for an open run's append. The reopened writer terminates the torn
// line in place (its bytes kept), appends "partial entry not recovered" naming
// it, and continues the log in sequence; identities are still checked.
#[test]
fn a_short_rs_write_is_recovered_by_the_reopened_writer_and_blocks_no_other_log() {
    let root = scratch("rs-short-");
    let log = rs_log(&root);
    for _ in 0..3 { append(&log, "evidence_limit", &APP_WRITER, rs_body(16)).unwrap(); }
    let result = result_of(&child("rs-short-only", &root).output().unwrap());
    let first = result["first"].as_str().unwrap_or_else(|| panic!("{result}"));
    assert!(first.starts_with("write: "), "{result}");
    let (complete, tail) = lines(&log);
    assert_eq!(complete.len(), 3);
    assert!(!tail.is_empty());
    let torn_bytes = std::fs::read(&log).unwrap();
    let name = log.file_name().unwrap().to_string_lossy().into_owned();
    assert_eq!(read_log(&log).1, [format!("{name}: partial entry at end (not read)")]);
    // Another log of the project is writable beside the torn tail (open-run mode).
    let run_entry = append_project_reserved(&root, "run:durability", "app-writer:local", "evidence_limit", &APP_WRITER, rs_body(16), "rec:app:durability-1", "2026-10-12T00:00:00.000Z");
    assert!(run_entry.is_ok(), "{run_entry:?}");
    assert_eq!(std::fs::read(&log).unwrap(), torn_bytes, "another writer never repairs this log");
    // A genuinely unreadable line in another log still leaves the set incomplete.
    let broken = crate::storage::project_log(&root, None, "broken-writer");
    std::fs::write(&broken, b"{\"not an entry\"\n").unwrap();
    let refused = append_project_reserved(&root, "run:durability", "app-writer:local", "evidence_limit", &APP_WRITER, rs_body(16), "rec:app:durability-2", "2026-10-12T00:00:00.000Z").unwrap_err();
    assert!(refused.contains("record-set conflict/incomplete"), "{refused}");
    std::fs::remove_file(&broken).unwrap();
    // The reopened writer: W-0, then the entry.
    let entry = append(&log, "evidence_limit", &APP_WRITER, rs_body(16)).unwrap();
    let after = std::fs::read(&log).unwrap();
    assert!(after.starts_with(&torn_bytes) && after[torn_bytes.len()] == b'\n', "terminated in place, never truncated or edited");
    let (read, limits) = read_log(&log);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(read.iter().map(|e| e["seq"].as_u64().unwrap()).collect::<Vec<_>>(), [1, 2, 3, 4, 5]);
    let limit = &read[3];
    assert_eq!((limit["kind"].as_str(), limit["body"]["label"].as_str(), limit["body"]["subjectRef"].as_str()), (Some("evidence_limit"), Some(PARTIAL_NOT_RECOVERED), Some("line 4")));
    assert!(limit["body"]["detail"].as_str().unwrap().contains(&crate::util::sha256_hex(&tail)), "{limit}");
    assert_eq!(read[4]["recordId"], entry["recordId"]);
    // The torn line is never read, here or by the project reader.
    let (all, all_limits) = crate::storage::read_all(&root);
    assert!(all_limits.is_empty(), "{all_limits:?}");
    assert_eq!(all.len(), 6);
    // Duplicates and identity conflicts are still refused.
    let conflict = append_with_id(&log, "evidence_limit", &APP_WRITER, rs_body(16), read[0]["recordId"].as_str().unwrap()).unwrap_err();
    assert!(conflict.contains("record identity conflict"), "{conflict}");
    let elsewhere = append_with_id(&log, "evidence_limit", &APP_WRITER, rs_body(16), "rec:app:durability-1").unwrap_err();
    assert!(elsewhere.contains("record identity conflict"), "{elsewhere}");
    // The same in one child process: its second append recovers the tail.
    let again = scratch("rs-short-again-");
    for _ in 0..2 { append(&rs_log(&again), "evidence_limit", &APP_WRITER, rs_body(16)).unwrap(); }
    let result = result_of(&child("rs-short", &again).output().unwrap());
    assert!(result["first"].is_string() && result["second"].is_null(), "{result}");
    assert_eq!(read_log(&rs_log(&again)).0.len(), 4);
    println!("rs short write: {} of a line landed; reopened writer recovered it", tail.len());
    std::fs::remove_dir_all(again).unwrap();
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
