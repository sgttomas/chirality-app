//! DEL-01-02: App session liveness on the App ledger. Invented sessions in
//! scratch folders; the only processes are this test binary.
use super::*;
use crate::hosting::Host;
use crate::recovery::{stored_entries, RecoveryLedger, NOT_CHECKED, STILL_RUNNING};
use serde_json::Value;
use std::io::{BufRead, BufReader};
use std::os::unix::fs::PermissionsExt;
use std::sync::Arc;

fn root() -> PathBuf {
    let root = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(crate::util::opaque_id("session-liveness-").unwrap());
    std::fs::create_dir(&root).unwrap();
    root
}
fn session_starts(entries: &[Value]) -> Vec<Value> {
    entries.iter().filter(|e| e["kind"] == "session_started").cloned().collect()
}

#[test]
fn a_lock_reads_held_while_its_session_lives_and_ended_after() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    assert_eq!(probe(&ledger, "app-session:a"), Liveness::Absent, "no file: an earlier build's session");
    let hold = Hold::acquire(&ledger, "app-session:a").unwrap();
    assert_eq!(std::fs::read(hold.path()).unwrap(), b"app-session:a", "the file names its session");
    assert_eq!(hold.path(), lock_path(&ledger, "app-session:a"));
    assert_eq!(probe(&ledger, "app-session:a"), Liveness::Held);
    assert_eq!(probe(&ledger, "app-session:b"), Liveness::Absent, "one session's lock is not another's");
    sweep(&ledger);
    assert!(hold.path().exists(), "a held file is never swept");
    // A killed process: the file stays and its lock is free.
    hold.release_as_if_killed();
    assert_eq!(probe(&ledger, "app-session:a"), Liveness::Free);
    sweep(&ledger);
    assert_eq!(probe(&ledger, "app-session:a"), Liveness::Absent, "a free file is swept");
    drop(hold);
    // An ended holder removes its own file.
    let hold = Hold::acquire(&ledger, "app-session:c").unwrap();
    let path = hold.path().to_owned();
    drop(hold);
    assert!(!path.exists());
    assert_eq!(probe(&ledger, "app-session:c"), Liveness::Absent);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_check_that_cannot_be_made_is_never_read_as_ended() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    std::fs::create_dir(directory(&ledger)).unwrap();
    // A directory where the lock file should be.
    std::fs::create_dir(lock_path(&ledger, "app-session:dir")).unwrap();
    assert!(matches!(probe(&ledger, "app-session:dir"), Liveness::Unknown(_)));
    // An unreadable lock file.
    let unreadable = lock_path(&ledger, "app-session:unreadable");
    std::fs::write(&unreadable, b"app-session:unreadable").unwrap();
    std::fs::set_permissions(&unreadable, std::fs::Permissions::from_mode(0o000)).unwrap();
    assert!(matches!(probe(&ledger, "app-session:unreadable"), Liveness::Unknown(_)));
    // A symbolic link is not followed.
    std::os::unix::fs::symlink(&unreadable, lock_path(&ledger, "app-session:link")).unwrap();
    assert!(matches!(probe(&ledger, "app-session:link"), Liveness::Unknown(_)));
    // The liveness location is not a directory.
    let other = root.join("other.ledger.jsonl");
    std::fs::write(directory(&other), b"not a directory").unwrap();
    assert!(matches!(probe(&other, "app-session:x"), Liveness::Unknown(_)));
    assert!(!Liveness::Unknown(String::new()).ended() && !Liveness::Held.ended());
    assert!(Liveness::Free.ended() && Liveness::Absent.ended());
    // A startup over an unchecked earlier session writes nothing and infers nothing.
    let mut earlier = RecoveryLedger::open(ledger.clone()).unwrap();
    earlier.start_session("app-session:dir", "invented").unwrap();
    drop(earlier);
    let before = stored_entries(&ledger);
    let refused = RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:later", "invented").unwrap_err();
    assert!(refused.contains(NOT_CHECKED), "{refused}");
    assert_eq!(stored_entries(&ledger), before);
    std::fs::remove_dir(lock_path(&ledger, "app-session:dir")).unwrap();
    RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:later", "invented").unwrap();
    let starts = session_starts(&stored_entries(&ledger));
    assert_eq!(starts.last().unwrap()["previousSessionEnd"], "ended-without-record");
    std::fs::set_permissions(&unreadable, std::fs::Permissions::from_mode(0o600)).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_session_start_is_refused_when_another_writer_appended_since_the_ledger_was_read() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:first", "invented").unwrap();
    let mut stale = RecoveryLedger::open(ledger.clone()).unwrap();
    RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:second", "invented").unwrap();
    let before = stored_entries(&ledger);
    let refused = stale.start_session("app-session:third", "invented").unwrap_err();
    assert!(refused.contains(crate::recovery::store::CHANGED_SINCE_READ), "{refused}");
    assert_eq!(stored_entries(&ledger), before, "nothing recorded");
    std::fs::remove_dir_all(root).unwrap();
}

/// The child half of the killed-App test: an App session's start on the
/// ledger, then it lives until it is killed (or its stdin closes).
#[test]
fn killed_app_session_peer() {
    let Some(ledger) = std::env::var_os("CHIRALITY_KILLED_SESSION_LEDGER") else {
        return;
    };
    let host = Host::new();
    host.configure_recovery(PathBuf::from(ledger)).unwrap();
    let session = host.shared_recovery_observation()["appSession"].as_str().unwrap().to_owned();
    println!("LIVE {session}");
    std::io::Write::flush(&mut std::io::stdout()).unwrap();
    let mut line = String::new();
    let _ = std::io::stdin().read_line(&mut line);
}

/// A lock left by a killed App (SIGKILL) strands no one: while the App lives
/// the next startup is refused and writes nothing; once it is killed the next
/// App starts normally, reads it as ended without a record exactly as before
/// locks existed, and its stale lock file is removed.
#[test]
fn a_killed_app_session_reads_as_ended_without_a_record_and_its_stale_lock_is_removed() {
    let root = root();
    std::fs::create_dir(root.join("runtime")).unwrap();
    let ledger = root.join("runtime/recovery.ledger.jsonl");
    let mut child = std::process::Command::new(std::env::current_exe().unwrap())
        .args(["--exact", "session_liveness::tests::killed_app_session_peer", "--nocapture", "--test-threads=1"])
        .env("CHIRALITY_KILLED_SESSION_LEDGER", &ledger)
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .unwrap();
    let mut lines = BufReader::new(child.stdout.take().unwrap()).lines();
    let killed = loop {
        let line = lines.next().expect("peer reported its session").unwrap();
        // libtest prints "test <name> ... " before the body, without a newline.
        if let Some((_, session)) = line.split_once("LIVE ") {
            break session.trim().to_owned();
        }
    };
    assert_eq!(probe(&ledger, &killed), Liveness::Held);
    let before = stored_entries(&ledger);
    let second = Host::new();
    let refused = second.configure_recovery(ledger.clone()).unwrap_err();
    assert!(refused.contains(STILL_RUNNING), "{refused}");
    assert_eq!(stored_entries(&ledger), before, "nothing written while the earlier App lives");
    assert!(second.recovery_custody().snapshot()["restartEvents"].as_array().unwrap().is_empty());
    assert_eq!(unsafe { libc::kill(child.id() as i32, libc::SIGKILL) }, 0);
    child.wait().unwrap();
    assert_eq!(probe(&ledger, &killed), Liveness::Free, "the kernel released the killed App's lock; its file stays");
    let next = Arc::new(Host::new());
    next.configure_recovery(ledger.clone()).unwrap();
    let start = session_starts(&stored_entries(&ledger)).pop().unwrap();
    assert_eq!(start["previousSession"], killed.as_str());
    assert_eq!(start["previousSessionEnd"], "ended-without-record");
    assert_eq!(probe(&ledger, &killed), Liveness::Absent, "the stale lock file was removed");
    let current = start["session"].as_str().unwrap();
    assert_eq!(probe(&ledger, current), Liveness::Held);
    drop(next);
    std::fs::remove_dir_all(root).unwrap();
}
