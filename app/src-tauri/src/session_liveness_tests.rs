//! DEL-01-02: App session liveness on the App ledger. Invented sessions in
//! scratch folders; the only processes are this test binary.
use super::*;
use crate::desktop_startup::DesktopSetup;
use crate::hosting::Host;
use crate::recovery::{stored_entries, RecoveryLedger, NOT_CHECKED, STILL_RUNNING};
use serde_json::{json, Value};
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
/// This process holds `data` as its App data, as the App does at startup.
fn hold_app_data(data: &Path) -> crate::AppDataCustody {
    crate::hold_app_data_for_test(data).unwrap()
}
fn silent(liveness: Liveness) -> bool {
    matches!(liveness, Liveness::Silent(_))
}

/// A lock file can only ever say that its session is alive: held while its
/// session lives; free, missing or anything else says nothing.
#[test]
fn a_lock_reads_held_while_its_session_lives_and_says_nothing_otherwise() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    assert!(silent(probe(&ledger, "app-session:a", false)), "no file, no lock declared");
    assert!(silent(probe(&ledger, "app-session:a", true)), "no file for a session that took its lock here");
    let hold = Hold::acquire(&ledger, "app-session:a").unwrap();
    assert_eq!(std::fs::read(hold.path()).unwrap(), b"app-session:a", "the file names its session");
    assert_eq!(hold.path(), lock_path(&ledger, "app-session:a"));
    assert_eq!(probe(&ledger, "app-session:a", true), Liveness::Held);
    assert_eq!(probe(&ledger, "app-session:a", false), Liveness::Held);
    assert!(silent(probe(&ledger, "app-session:b", false)), "one session's lock is not another's");
    sweep(&ledger, &["app-session:a"].into());
    assert!(hold.path().exists(), "a held file is never swept");
    // A killed process: the file stays and its lock is free, which says nothing.
    hold.release_as_if_killed();
    assert!(silent(probe(&ledger, "app-session:a", true)));
    sweep(&ledger, &Default::default());
    assert!(hold.path().exists(), "a file is kept until the ledger records its session's end");
    sweep(&ledger, &["app-session:a"].into());
    assert!(!hold.path().exists(), "once its end is recorded, a free file that names it is swept");
    drop(hold);
    // A holder that goes leaves its file, free, as the end of a process does.
    let hold = Hold::acquire(&ledger, "app-session:c").unwrap();
    let path = hold.path().to_owned();
    drop(hold);
    assert!(path.exists());
    assert!(silent(probe(&ledger, "app-session:c", true)));
    // A free file that names another session is never swept for this one.
    std::fs::write(&path, b"app-session:other").unwrap();
    sweep(&ledger, &["app-session:c"].into());
    assert!(path.exists());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_check_that_cannot_be_made_is_never_read_as_ended() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    std::fs::create_dir(directory(&ledger)).unwrap();
    for declared in [false, true] {
        // A directory where the lock file should be.
        std::fs::create_dir_all(lock_path(&ledger, "app-session:dir")).unwrap();
        assert!(silent(probe(&ledger, "app-session:dir", declared)));
        // An unreadable lock file.
        let unreadable = lock_path(&ledger, "app-session:unreadable");
        std::fs::write(&unreadable, b"app-session:unreadable").unwrap();
        std::fs::set_permissions(&unreadable, std::fs::Permissions::from_mode(0o000)).unwrap();
        assert!(silent(probe(&ledger, "app-session:unreadable", declared)));
        // A symbolic link is not followed.
        let _ = std::fs::remove_file(lock_path(&ledger, "app-session:link"));
        std::os::unix::fs::symlink(&unreadable, lock_path(&ledger, "app-session:link")).unwrap();
        assert!(silent(probe(&ledger, "app-session:link", declared)));
        std::fs::set_permissions(&unreadable, std::fs::Permissions::from_mode(0o600)).unwrap();
        // The liveness location is not a directory.
        let other = root.join("other.ledger.jsonl");
        let _ = std::fs::write(directory(&other), b"not a directory");
        assert!(silent(probe(&other, "app-session:x", declared)));
    }
    // A startup over an unchecked earlier session writes nothing and infers nothing.
    let mut earlier = RecoveryLedger::open(ledger.clone()).unwrap();
    earlier.start_session("app-session:dir", "invented").unwrap();
    drop(earlier);
    let before = stored_entries(&ledger);
    let refused = RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:later", "invented").unwrap_err();
    assert!(refused.contains(NOT_CHECKED), "{refused}");
    assert_eq!(stored_entries(&ledger), before);
    // With nothing in the way the earlier session (which declared no lock) is
    // still not read as ended without this App holding the App data
    // (Decision A: one rule for every earlier session) ...
    std::fs::remove_dir(lock_path(&ledger, "app-session:dir")).unwrap();
    let refused = RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:later", "invented").unwrap_err();
    assert!(refused.contains(NOT_CHECKED), "{refused}");
    assert_eq!(stored_entries(&ledger), before);
    // ... and is, with it.
    let _held = hold_app_data(&root);
    RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:later", "invented").unwrap();
    let starts = session_starts(&stored_entries(&ledger));
    assert_eq!(starts.last().unwrap()["previousSessionEnd"], "ended-without-record");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_session_start_is_refused_when_another_writer_appended_since_the_ledger_was_read() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    let _held = hold_app_data(&root);
    RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:first", "invented").unwrap();
    let mut stale = RecoveryLedger::open(ledger.clone()).unwrap();
    RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:second", "invented").unwrap();
    let before = stored_entries(&ledger);
    let refused = stale.start_session("app-session:third", "invented").unwrap_err();
    assert!(refused.contains(crate::recovery::store::CHANGED_SINCE_READ), "{refused}");
    assert_eq!(stored_entries(&ledger), before, "nothing recorded");
    std::fs::remove_dir_all(root).unwrap();
}

/// A session of this build says in its session_started that it took its lock;
/// a session started without one does not.
#[test]
fn a_session_that_holds_its_lock_says_so_in_its_session_start() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    let _custody = hold_app_data(&root);
    let host = Host::new();
    host.configure_recovery(ledger.clone()).unwrap();
    let held = session_starts(&stored_entries(&ledger)).pop().unwrap();
    assert_eq!(held[FIELD], true, "{held}");
    host.end_process_for_test();
    RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:lockless", "invented").unwrap();
    let lockless = session_starts(&stored_entries(&ledger)).pop().unwrap();
    assert!(lockless.get(FIELD).is_none(), "{lockless}");
    // A hold is accepted only for its own session on its own ledger.
    let other = Hold::acquire(&ledger, "app-session:other").unwrap();
    let refused = RecoveryLedger::open(ledger.clone()).unwrap().start_session_held("app-session:mismatch", "invented", &other).unwrap_err();
    assert!(refused.contains("not this session's"), "{refused}");
    drop(other);
    std::fs::remove_dir_all(root).unwrap();
}

/// A ledger written before the field: its sessions carry no `livenessLock`
/// and have no lock file. They are read by the same rule as every other
/// earlier session (Decision A): without this App holding the App data that
/// contains the ledger the session start is refused and nothing is written;
/// with it, and the session not alive here, it is ended without a record. A
/// person whose last session of an earlier build crashed is read as before,
/// since the App holds its App data before it opens the ledger on both routes.
#[test]
fn a_ledger_written_before_the_field_is_read_by_the_one_rule() {
    for evidence in [false, true] {
        let root = root();
        std::fs::create_dir(root.join("runtime")).unwrap();
        let ledger = root.join("runtime/recovery.ledger.jsonl");
        // As an earlier build wrote it: a session start with no field, no lock.
        RecoveryLedger::open(ledger.clone()).unwrap().start_session("app-session:earlier-build", "invented").unwrap();
        assert!(!directory(&ledger).join(file_name("app-session:earlier-build")).exists());
        let _held = evidence.then(|| hold_app_data(&root));
        let before = stored_entries(&ledger);
        let next = Host::new();
        let result = next.configure_recovery(ledger.clone());
        if evidence {
            result.unwrap();
            let start = session_starts(&stored_entries(&ledger)).pop().unwrap();
            assert_eq!(start["previousSession"], "app-session:earlier-build");
            assert_eq!(start["previousSessionEnd"], "ended-without-record");
            assert_eq!(start[FIELD], true);
        } else {
            let refused = result.unwrap_err();
            assert!(refused.contains(NOT_CHECKED) && refused.contains("declared no liveness lock"), "{refused}");
            assert_eq!(stored_entries(&ledger), before, "nothing written");
        }
        drop(next);
        std::fs::remove_dir_all(root).unwrap();
    }
}

/// Every probe outcome other than a held lock, for a session of this build
/// whose process has ended, each without and with the rule's custody (this
/// App holds the App data directory that contains the ledger). Without it the
/// next session start is refused and nothing is written; with it the earlier
/// session is read as ended without a record. A free file that names the
/// session is no exception: it is what a copy put in place of a live
/// session's lock looks like.
#[test]
fn every_unheld_lock_outcome_reads_as_ended_only_under_this_apps_custody_of_its_data() {
    let cases: [(&str, fn(&Path, &str)); 8] = [
        ("left free and naming it (its process killed)", |_, _| {}),
        ("replaced by a free copy that names it", |path, _| {
            let text = std::fs::read(path).unwrap();
            std::fs::rename(path, path.with_extension("original")).unwrap();
            std::fs::write(path, text).unwrap();
        }),
        ("unreadable (it cannot be opened)", |path, _| {
            std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o000)).unwrap();
        }),
        ("removed", |path, _| std::fs::remove_file(path).unwrap()),
        ("replaced by another file", |path, _| {
            std::fs::remove_file(path).unwrap();
            std::fs::write(path, b"").unwrap();
        }),
        ("replaced by a file with a wrong identity", |path, _| {
            std::fs::remove_file(path).unwrap();
            std::fs::write(path, b"app-session:someone-else").unwrap();
        }),
        ("replaced by a directory", |path, _| {
            std::fs::remove_file(path).unwrap();
            std::fs::create_dir(path).unwrap();
        }),
        ("its whole liveness directory removed", |path, _| std::fs::remove_dir_all(path.parent().unwrap()).unwrap()),
    ];
    for (case, change) in cases {
        for evidence in [false, true] {
            let root = root();
            std::fs::create_dir(root.join("runtime")).unwrap();
            let ledger = root.join("runtime/recovery.ledger.jsonl");
            let first = Host::new();
            first.configure_recovery(ledger.clone()).unwrap();
            let earlier = first.shared_recovery_observation()["appSession"].as_str().unwrap().to_owned();
            first.end_process_for_test();
            let path = lock_path(&ledger, &earlier);
            change(&path, &earlier);
            assert!(silent(probe(&ledger, &earlier, true)), "{case}");
            let held = evidence.then(|| hold_app_data(&root));
            let before = stored_entries(&ledger);
            let next = Host::new();
            let result = next.configure_recovery(ledger.clone());
            if evidence {
                result.unwrap_or_else(|e| panic!("{case}: {e}"));
                let start = session_starts(&stored_entries(&ledger)).pop().unwrap();
                assert_eq!(start["previousSession"], earlier.as_str(), "{case}");
                assert_eq!(start["previousSessionEnd"], "ended-without-record", "{case}");
            } else {
                let refused = result.unwrap_err();
                assert!(refused.contains(NOT_CHECKED), "{case}: {refused}");
                assert_eq!(stored_entries(&ledger), before, "{case}: nothing written");
                assert!(next.recovery_custody().snapshot()["restartEvents"].as_array().unwrap().is_empty(), "{case}");
                assert!(next.recovery_custody().snapshot()["limits"].to_string().contains("not treated as ended"), "{case}: shown as a limit");
            }
            drop(next);
            drop(held);
            drop(first);
            std::fs::remove_dir_all(root).unwrap();
        }
    }
}

/// The positive evidence is the held directory's identity, not a path: App
/// data held elsewhere is no evidence; the held directory reached through
/// another spelling is; a directory put in its place at the same path is not.
#[test]
fn the_evidence_is_the_held_app_data_by_identity() {
    let root = root();
    let data = root.join("data");
    std::fs::create_dir_all(data.join("runtime")).unwrap();
    let ledger = data.join("runtime/recovery.ledger.jsonl");
    std::fs::create_dir_all(directory(&ledger)).unwrap();
    std::fs::write(lock_path(&ledger, "app-session:gone"), b"").unwrap();
    assert!(establish_ended(&ledger, "app-session:gone").is_err(), "nothing held");
    let elsewhere = root.join("elsewhere");
    std::fs::create_dir(&elsewhere).unwrap();
    let other = hold_app_data(&elsewhere);
    assert!(establish_ended(&ledger, "app-session:gone").is_err(), "other App data is no evidence");
    drop(other);
    let held = hold_app_data(&data);
    establish_ended(&ledger, "app-session:gone").unwrap();
    std::os::unix::fs::symlink(&data, root.join("alias")).unwrap();
    establish_ended(&root.join("alias/runtime/recovery.ledger.jsonl"), "app-session:gone").expect("the same directory by another spelling");
    // The held directory is moved away and another is put at its path.
    std::fs::rename(&data, root.join("moved")).unwrap();
    std::fs::create_dir_all(data.join("runtime")).unwrap();
    assert!(establish_ended(&ledger, "app-session:gone").is_err(), "a replacement at the same path is not the held directory");
    establish_ended(&root.join("moved/runtime/recovery.ledger.jsonl"), "app-session:gone").expect("the held directory where it now is");
    drop(held);
    assert!(establish_ended(&root.join("moved/runtime/recovery.ledger.jsonl"), "app-session:gone").is_err(), "released");
    std::fs::remove_dir_all(root).unwrap();
}

/// A session whose hold is alive in this process is never read as ended,
/// with custody of its App data, whatever its lock file shows: removed, or
/// replaced by a free copy that names it (the same-process form of the
/// reviewer's copied lock).
#[test]
fn a_session_alive_in_this_process_is_never_read_as_ended() {
    let changes: [(&str, fn(&Path)); 2] = [
        ("removed", |path| std::fs::remove_file(path).unwrap()),
        ("replaced by a free copy that names it", |path| {
            let text = std::fs::read(path).unwrap();
            std::fs::rename(path, path.with_extension("original")).unwrap();
            std::fs::write(path, text).unwrap();
        }),
    ];
    for (case, change) in changes {
        let root = root();
        std::fs::create_dir(root.join("runtime")).unwrap();
        let ledger = root.join("runtime/recovery.ledger.jsonl");
        let _held = hold_app_data(&root);
        let first = Host::new();
        first.configure_recovery(ledger.clone()).unwrap();
        let live = first.shared_recovery_observation()["appSession"].as_str().unwrap().to_owned();
        change(&lock_path(&ledger, &live));
        assert!(silent(probe(&ledger, &live, true)), "{case}");
        let before = stored_entries(&ledger);
        let refused = Host::new().configure_recovery(ledger.clone()).unwrap_err();
        assert!(refused.contains(NOT_CHECKED) && refused.contains("held in this process"), "{case}: {refused}");
        assert_eq!(stored_entries(&ledger), before, "{case}");
        drop(first);
        std::fs::remove_dir_all(root).unwrap();
    }
}

/// A stale file stays until a later session start records its session's end;
/// after that the earlier session's reading rests on the record, not the file.
#[test]
fn a_stale_file_is_removed_only_after_its_sessions_end_is_recorded() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    let _custody = hold_app_data(&root);
    let first = Host::new();
    first.configure_recovery(ledger.clone()).unwrap();
    let a = first.shared_recovery_observation()["appSession"].as_str().unwrap().to_owned();
    first.end_process_for_test();
    assert!(lock_path(&ledger, &a).exists());
    let second = Host::new();
    second.configure_recovery(ledger.clone()).unwrap();
    let b = second.shared_recovery_observation()["appSession"].as_str().unwrap().to_owned();
    assert!(!lock_path(&ledger, &a).exists(), "the second start recorded the first's end, then swept its file");
    second.end_process_for_test();
    // A third start reads the first from the record and the second from its file.
    let third = Host::new();
    third.configure_recovery(ledger.clone()).unwrap();
    let start = session_starts(&stored_entries(&ledger)).pop().unwrap();
    assert_eq!(start["previousSession"], b.as_str());
    assert!(!lock_path(&ledger, &b).exists());
    drop((first, second, third));
    std::fs::remove_dir_all(root).unwrap();
}

/// Old and new together. A row of a later version this reader does not know
/// (here a session start with an unknown field, as a later build might add)
/// is not read: the ledger does not open and recovery shows the limit. That
/// is what a 0.4 reader does with this build's `livenessLock`: the 0.4 schema
/// refuses the row.
#[test]
fn a_reader_refuses_a_row_of_a_version_it_does_not_know_and_reads_nothing_in_part() {
    let root = root();
    let ledger = root.join("recovery.ledger.jsonl");
    let host = Host::new();
    host.configure_recovery(ledger.clone()).unwrap();
    host.end_process_for_test();
    let row = session_starts(&stored_entries(&ledger)).pop().unwrap();
    let v04: Value = serde_json::from_str(include_str!("../resources/runtime_core/recovery.app-ledger-entry.v0.4.schema.json")).unwrap();
    let v04 = jsonschema::options().offline().build(&v04).unwrap();
    assert!(!v04.is_valid(&row), "a 0.4 reader cannot read this build's session start");
    let mut without = row.clone();
    without.as_object_mut().unwrap().remove(FIELD);
    assert!(v04.is_valid(&without), "the field is the only difference");
    // This build's reader on a row it does not know, stored as any row is.
    let mut newer = row.clone();
    newer["session"] = json!("app-session:newer-build");
    newer["laterField"] = json!(true);
    crate::recovery::store::Store::open(&crate::recovery::database_path(&ledger), false, false)
        .unwrap()
        .insert_batch(&[newer])
        .unwrap();
    let refused = RecoveryLedger::open(ledger.clone()).err().expect("a row this reader does not know is not read");
    assert!(refused.contains("App history unavailable"), "{refused}");
    let next = Host::new();
    assert!(next.configure_recovery(ledger.clone()).is_err());
    drop(next);
    std::fs::remove_dir_all(root).unwrap();
}

/// The child half of the two-process tests: an App session's start on the
/// ledger, holding the App data that contains it when one is named, then it
/// lives until it is killed (or its stdin closes).
#[test]
fn killed_app_session_peer() {
    let Some(ledger) = std::env::var_os("CHIRALITY_KILLED_SESSION_LEDGER") else {
        return;
    };
    let _data = std::env::var_os("CHIRALITY_KILLED_SESSION_APP_DATA").map(|data| hold_app_data(Path::new(&data)));
    let host = Host::new();
    host.configure_recovery(PathBuf::from(ledger)).unwrap();
    let session = host.shared_recovery_observation()["appSession"].as_str().unwrap().to_owned();
    println!("LIVE {session}");
    std::io::Write::flush(&mut std::io::stdout()).unwrap();
    let mut line = String::new();
    let _ = std::io::stdin().read_line(&mut line);
}
fn live_peer(ledger: &Path, data: Option<&Path>) -> (std::process::Child, String) {
    let mut command = std::process::Command::new(std::env::current_exe().unwrap());
    command
        .args(["--exact", "session_liveness::tests::killed_app_session_peer", "--nocapture", "--test-threads=1"])
        .env("CHIRALITY_KILLED_SESSION_LEDGER", ledger)
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped());
    if let Some(data) = data {
        command.env("CHIRALITY_KILLED_SESSION_APP_DATA", data);
    }
    let mut child = command.spawn().unwrap();
    let mut lines = BufReader::new(child.stdout.take().unwrap()).lines();
    let session = loop {
        let line = lines.next().expect("peer reported its session").unwrap();
        // libtest prints "test <name> ... " before the body, without a newline.
        if let Some((_, session)) = line.split_once("LIVE ") {
            break session.trim().to_owned();
        }
    };
    (child, session)
}

/// A lock left by a killed App (SIGKILL) strands no one: while the App lives
/// the next startup is refused and writes nothing; once it is killed the next
/// App holds the App data, starts normally, reads it as ended without a record
/// exactly as before locks existed, and its stale lock file is removed once
/// that end is recorded.
#[test]
fn a_killed_app_session_reads_as_ended_without_a_record_and_its_stale_lock_is_removed() {
    let root = root();
    std::fs::create_dir(root.join("runtime")).unwrap();
    let ledger = root.join("runtime/recovery.ledger.jsonl");
    let (mut child, killed) = live_peer(&ledger, Some(&root));
    assert_eq!(probe(&ledger, &killed, true), Liveness::Held);
    let before = stored_entries(&ledger);
    let second = Host::new();
    let refused = second.configure_recovery(ledger.clone()).unwrap_err();
    assert!(refused.contains(STILL_RUNNING), "{refused}");
    assert_eq!(stored_entries(&ledger), before, "nothing written while the earlier App lives");
    assert!(second.recovery_custody().snapshot()["restartEvents"].as_array().unwrap().is_empty());
    assert_eq!(unsafe { libc::kill(child.id() as i32, libc::SIGKILL) }, 0);
    child.wait().unwrap();
    assert!(silent(probe(&ledger, &killed, true)), "the kernel released the killed App's lock; its file stays");
    let _held = hold_app_data(&root);
    let next = Arc::new(Host::new());
    next.configure_recovery(ledger.clone()).unwrap();
    let start = session_starts(&stored_entries(&ledger)).pop().unwrap();
    assert_eq!(start["previousSession"], killed.as_str());
    assert_eq!(start["previousSessionEnd"], "ended-without-record");
    assert!(!lock_path(&ledger, &killed).exists(), "the stale lock file was removed once its end was recorded");
    let current = start["session"].as_str().unwrap();
    assert_eq!(probe(&ledger, current, true), Liveness::Held);
    drop(next);
    std::fs::remove_dir_all(root).unwrap();
}

/// The reviewer's reproduction, as a maintained test. A live App session (its
/// own process, holding its App data) has its lock file deleted from outside;
/// a second process's startup on the same ledger is refused and writes
/// nothing, because it cannot hold that App data. Once the first is killed,
/// the second holds the App data and reads the session (still without a lock
/// file) as ended without a record.
#[test]
fn a_live_sessions_deleted_lock_file_is_never_read_as_ended() {
    let root = root();
    std::fs::create_dir(root.join("runtime")).unwrap();
    let ledger = root.join("runtime/recovery.ledger.jsonl");
    let (mut child, live) = live_peer(&ledger, Some(&root));
    std::fs::remove_file(lock_path(&ledger, &live)).unwrap();
    let before = stored_entries(&ledger);
    // Without the evidence: this process does not hold the App data (another App does).
    let mut setup = DesktopSetup::new(Ok(root.clone()), Err("no resources in this fixture".into()));
    assert!(setup.hold_environment_data(&root).is_err(), "another App holds this App data");
    let second = Host::new();
    let refused = second.configure_recovery(ledger.clone()).unwrap_err();
    assert!(refused.contains(NOT_CHECKED), "{refused}");
    assert_eq!(stored_entries(&ledger), before, "no session start naming the live session ended");
    assert!(stored_entries(&ledger).iter().all(|e| e["previousSessionEnd"] != "ended-without-record"));
    drop(second);
    assert_eq!(unsafe { libc::kill(child.id() as i32, libc::SIGKILL) }, 0);
    child.wait().unwrap();
    // With the evidence: the first App is gone and this one holds the App data.
    let _held = hold_app_data(&root);
    let next = Host::new();
    next.configure_recovery(ledger.clone()).unwrap();
    let start = session_starts(&stored_entries(&ledger)).pop().unwrap();
    assert_eq!(start["previousSession"], live.as_str());
    assert_eq!(start["previousSessionEnd"], "ended-without-record");
    drop(next);
    std::fs::remove_dir_all(root).unwrap();
}

/// The reviewer's copied lock (round 2, finding 1), as a maintained test. A
/// live App session in its own process, holding its App data; its lock file is
/// renamed away and a free copy carrying the same identity is put at its path.
/// A second process's startup on the same ledger is refused and writes
/// nothing: the copy says nothing, and this process cannot hold that App data.
#[test]
fn a_free_copy_of_a_live_sessions_lock_is_never_read_as_ended() {
    let root = root();
    std::fs::create_dir(root.join("runtime")).unwrap();
    let ledger = root.join("runtime/recovery.ledger.jsonl");
    let (mut child, live) = live_peer(&ledger, Some(&root));
    let path = lock_path(&ledger, &live);
    let text = std::fs::read(&path).unwrap();
    std::fs::rename(&path, root.join("original.lock")).unwrap();
    std::fs::write(&path, text).unwrap();
    assert!(silent(probe(&ledger, &live, true)));
    let before = stored_entries(&ledger);
    assert!(crate::hold_app_data_for_test(&root).is_err(), "the live App holds this App data");
    let second = Host::new();
    let refused = second.configure_recovery(ledger.clone()).unwrap_err();
    assert!(refused.contains(NOT_CHECKED), "{refused}");
    assert_eq!(stored_entries(&ledger), before, "no session start naming the live session ended");
    assert!(child.try_wait().unwrap().is_none(), "the peer is still alive");
    drop(second);
    drop(child.stdin.take());
    child.wait().unwrap();
    std::fs::remove_dir_all(root).unwrap();
}

/// The child half of the reviewer's legacy reproduction: a session started
/// with no liveness lock (as a build before the field wrote it), holding the
/// App data that contains the ledger when one is named, alive until its stdin
/// closes.
#[test]
fn lockless_app_session_peer() {
    let Some(ledger) = std::env::var_os("CHIRALITY_LOCKLESS_SESSION_LEDGER") else {
        return;
    };
    let _data = std::env::var_os("CHIRALITY_LOCKLESS_SESSION_APP_DATA").map(|data| hold_app_data(Path::new(&data)));
    let mut ledger = RecoveryLedger::open(PathBuf::from(ledger)).unwrap();
    ledger.start_session("legacy-live-session", "old-producer-model").unwrap();
    println!("LIVE legacy-live-session");
    std::io::Write::flush(&mut std::io::stdout()).unwrap();
    let mut line = String::new();
    let _ = std::io::stdin().read_line(&mut line);
}

/// The reviewer's legacy reproduction (round 2, finding 3), as a maintained
/// test. A live session that declared no lock, in its own process: a second
/// process's startup without custody of the App data is refused and writes
/// nothing, whether or not the live process holds that App data. (A build
/// before the App data hold, started on the environment route, holds nothing;
/// a later App that holds the same App data then reads such a session as
/// ended. That is the stated limit, app/README.md; it is not exercised here.)
#[test]
fn a_live_session_that_declared_no_lock_is_never_read_as_ended_without_custody() {
    for peer_holds_data in [false, true] {
        let root = root();
        std::fs::create_dir(root.join("runtime")).unwrap();
        let ledger = root.join("runtime/recovery.ledger.jsonl");
        let mut command = std::process::Command::new(std::env::current_exe().unwrap());
        command
            .args(["--exact", "session_liveness::tests::lockless_app_session_peer", "--nocapture", "--test-threads=1"])
            .env("CHIRALITY_LOCKLESS_SESSION_LEDGER", &ledger)
            .stdin(std::process::Stdio::piped())
            .stdout(std::process::Stdio::piped());
        if peer_holds_data {
            command.env("CHIRALITY_LOCKLESS_SESSION_APP_DATA", &root);
        }
        let mut child = command.spawn().unwrap();
        let mut lines = BufReader::new(child.stdout.take().unwrap()).lines();
        while !lines.next().expect("peer reported").unwrap().contains("LIVE ") {}
        let before = stored_entries(&ledger);
        let second = Host::new();
        let refused = second.configure_recovery(ledger.clone()).unwrap_err();
        assert!(refused.contains(NOT_CHECKED), "{peer_holds_data}: {refused}");
        assert_eq!(stored_entries(&ledger), before, "{peer_holds_data}: nothing written");
        assert!(child.try_wait().unwrap().is_none());
        drop(second);
        drop(child.stdin.take());
        child.wait().unwrap();
        std::fs::remove_dir_all(root).unwrap();
    }
}
