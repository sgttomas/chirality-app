//! DEL-01-01/05: one App at a time on a Codex home. Invented homes in
//! scratch folders; nothing is created inside a home.
use super::*;
use std::io::{BufRead, BufReader, Write as _};
use std::path::PathBuf;
use std::sync::atomic::AtomicBool;

struct Owner(AtomicBool);
impl HoldOwner for Owner {
    fn may_have_child(&self) -> bool {
        self.0.load(Ordering::SeqCst)
    }
}
fn owner(busy: bool) -> Arc<Owner> {
    Arc::new(Owner(AtomicBool::new(busy)))
}
fn weak(owner: &Arc<Owner>) -> Weak<dyn HoldOwner> {
    Arc::downgrade(owner) as Weak<dyn HoldOwner>
}
fn home() -> PathBuf {
    let root = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(crate::util::opaque_id("home-hold-").unwrap());
    std::fs::create_dir_all(root.join("home")).unwrap();
    root.join("home")
}
fn contents(home: &Path) -> Vec<PathBuf> {
    std::fs::read_dir(home).unwrap().map(|e| e.unwrap().path()).collect()
}

#[test]
fn one_host_at_a_time_in_a_process_and_a_home_passes_only_from_an_idle_one() {
    let home = home();
    let (first, second) = (owner(true), owner(false));
    let (a, b) = (next_id(), next_id());
    let starting_a = Arc::new(AtomicUsize::new(0));
    let starting_b = Arc::new(AtomicUsize::new(0));
    let (hold_a, claim, _) = claim_host(&home, a, weak(&first), &starting_a).unwrap();
    // The same Host starting again gets a hold of its own; letting that one
    // go (a start call refused later) keeps the home held by the first.
    drop(claim);
    let (again, claim, _) = claim_host(&home, a, weak(&first), &starting_a).unwrap();
    drop(again);
    drop(claim);
    assert!(peer(&home).contains("REFUSED"), "still held by the first hold");
    // A start under way, or a child that may be alive, keeps the home.
    first.0.store(false, Ordering::SeqCst);
    let claim = claim_host(&home, a, weak(&first), &starting_a).unwrap().1;
    assert!(claim_host(&home, b, weak(&second), &starting_b).is_err(), "a start in progress");
    drop(claim);
    first.0.store(true, Ordering::SeqCst);
    assert!(claim_host(&home, b, weak(&second), &starting_b).is_err(), "a child that may be alive");
    // The same home by another spelling is the same home.
    let alias = home.parent().unwrap().join("alias");
    std::os::unix::fs::symlink(&home, &alias).unwrap();
    assert!(claim_host(&alias, b, weak(&second), &starting_b).is_err());
    // An idle Host's home can be taken; its later release does not free it.
    first.0.store(false, Ordering::SeqCst);
    let (hold_b, claim_b, _) = claim_host(&home, b, weak(&second), &starting_b).unwrap();
    drop(claim_b);
    drop(hold_a);
    second.0.store(true, Ordering::SeqCst);
    assert!(claim_host(&home, a, weak(&first), &starting_a).is_err(), "the home stays with its taker");
    // A dropped Host's home is free.
    drop(hold_b);
    let (_hold, _claim, _) = claim_host(&home, a, weak(&first), &starting_a).unwrap();
    assert!(contents(&home).is_empty(), "nothing is created inside a home");
    std::fs::remove_dir_all(home.parent().unwrap()).unwrap();
}

#[test]
fn the_receiving_source_and_the_host_share_one_lock_on_a_home() {
    let home = home();
    let file = File::open(&home).unwrap();
    let receiving = hold_receiving(&file).unwrap();
    assert!(hold_receiving(&File::open(&home).unwrap()).is_err(), "one receiving holder");
    let host = owner(true);
    let starting = Arc::new(AtomicUsize::new(0));
    let (hold, claim, _) = claim_host(&home, next_id(), weak(&host), &starting).expect("the App's own Host is not refused by its receiving source");
    drop(claim);
    drop(receiving);
    // The Host keeps the home locked after the receiving source lets go.
    let seen = peer(&home);
    assert!(seen.contains("REFUSED"), "{seen}");
    drop(hold);
    let seen = peer(&home);
    assert!(seen.contains("HELD"), "{seen}");
    assert!(contents(&home).is_empty());
    std::fs::remove_dir_all(home.parent().unwrap()).unwrap();
}

/// Another process's view of `home`: `HELD` when it could take the Host role
/// (then it lets go), otherwise `REFUSED` with the reason.
fn peer(home: &Path) -> String {
    let out = std::process::Command::new(std::env::current_exe().unwrap())
        .args(["--exact", "home_hold::tests::home_hold_peer", "--nocapture", "--test-threads=1"])
        .env("CHIRALITY_HOME_HOLD_PEER", home)
        .env("CHIRALITY_HOME_HOLD_PEER_MODE", "probe")
        .output()
        .unwrap();
    assert!(out.status.success(), "{}", String::from_utf8_lossy(&out.stderr));
    String::from_utf8_lossy(&out.stdout).into_owned()
}

#[test]
fn home_hold_peer() {
    let Some(home) = std::env::var_os("CHIRALITY_HOME_HOLD_PEER") else {
        return;
    };
    let mode = std::env::var("CHIRALITY_HOME_HOLD_PEER_MODE").unwrap();
    let holder = owner(true);
    let starting = Arc::new(AtomicUsize::new(0));
    match claim_host(Path::new(&home), next_id(), weak(&holder), &starting) {
        Ok((hold, claim, _)) => {
            println!("HELD");
            std::io::stdout().flush().unwrap();
            if mode == "keep" {
                let mut line = String::new();
                let _ = std::io::stdin().read_line(&mut line);
            }
            drop((hold, claim));
        }
        Err(reason) => println!("REFUSED {reason}"),
    }
}

/// Across processes: a home another process holds is refused with the plain
/// reason; once that process is killed (SIGKILL) the home can be held.
#[test]
fn a_home_held_by_another_process_is_refused_until_that_process_is_killed() {
    let home = home();
    let mut child = std::process::Command::new(std::env::current_exe().unwrap())
        .args(["--exact", "home_hold::tests::home_hold_peer", "--nocapture", "--test-threads=1"])
        .env("CHIRALITY_HOME_HOLD_PEER", &home)
        .env("CHIRALITY_HOME_HOLD_PEER_MODE", "keep")
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .unwrap();
    let mut lines = BufReader::new(child.stdout.take().unwrap()).lines();
    loop {
        let line = lines.next().expect("peer reported").unwrap();
        // libtest prints "test <name> ... " before the body, without a newline.
        assert!(!line.contains("REFUSED"), "{line}");
        if line.ends_with("HELD") {
            break;
        }
    }
    let here = owner(true);
    let starting = Arc::new(AtomicUsize::new(0));
    assert_eq!(claim_host(&home, next_id(), weak(&here), &starting).err().as_deref(), Some(IN_USE));
    assert!(hold_receiving(&File::open(&home).unwrap()).is_err());
    assert_eq!(unsafe { libc::kill(child.id() as i32, libc::SIGKILL) }, 0);
    child.wait().unwrap();
    let (_hold, _claim, _) = claim_host(&home, next_id(), weak(&here), &starting).expect("a killed holder strands no one");
    assert!(contents(&home).is_empty());
    std::fs::remove_dir_all(home.parent().unwrap()).unwrap();
}

/// A home that does not exist is refused, and nothing is created; there is
/// no in-process-only hold of a path.
#[test]
fn a_missing_home_is_refused_and_nothing_is_created() {
    let home = home();
    let missing = home.join("not-there");
    let holder = owner(false);
    let starting = Arc::new(AtomicUsize::new(0));
    assert_eq!(claim_host(&missing, next_id(), weak(&holder), &starting).err().as_deref(), Some(MISSING));
    assert_eq!(starting.load(Ordering::SeqCst), 0, "no start claim is left behind");
    assert!(!missing.exists());
    std::fs::remove_dir_all(home.parent().unwrap()).unwrap();
}

/// A holder that is gone while its slot is still registered is busy, never
/// idle, and the refusal says this App holds the home (not who else might).
#[test]
fn a_holder_that_is_gone_while_its_hold_is_kept_is_busy() {
    let home = home();
    let gone = owner(false);
    let starting = Arc::new(AtomicUsize::new(0));
    let (hold, claim, _) = claim_host(&home, next_id(), weak(&gone), &starting).unwrap();
    drop(claim);
    drop(gone);
    let other = owner(false);
    let refused = claim_host(&home, next_id(), weak(&other), &Arc::new(AtomicUsize::new(0))).err().unwrap();
    assert_eq!(refused, IN_USE_HERE);
    drop(hold);
    assert!(claim_host(&home, next_id(), weak(&other), &Arc::new(AtomicUsize::new(0))).is_ok(), "free once the hold is released");
    std::fs::remove_dir_all(home.parent().unwrap()).unwrap();
}

/// The path is checked against the held directory's identity: the same
/// directory by another spelling passes; a replacement, a removal, or a file
/// at the path is refused.
#[test]
fn a_home_path_is_admitted_only_while_it_names_the_held_directory() {
    let home = home();
    let holder = owner(true);
    let starting = Arc::new(AtomicUsize::new(0));
    let (hold, _claim, identity) = claim_host(&home, next_id(), weak(&holder), &starting).unwrap();
    still_names(&home, identity).unwrap();
    let alias = home.parent().unwrap().join("alias");
    std::os::unix::fs::symlink(&home, &alias).unwrap();
    still_names(&alias, identity).unwrap();
    let moved = home.parent().unwrap().join("moved");
    std::fs::rename(&home, &moved).unwrap();
    assert_eq!(still_names(&home, identity).err().as_deref(), Some(REPLACED), "removed");
    std::fs::create_dir(&home).unwrap();
    assert_eq!(still_names(&home, identity).err().as_deref(), Some(REPLACED), "replaced by another directory");
    std::fs::remove_dir(&home).unwrap();
    std::fs::write(&home, b"").unwrap();
    assert_eq!(still_names(&home, identity).err().as_deref(), Some(REPLACED), "replaced by a file");
    still_names(&moved, identity).unwrap();
    drop(hold);
    std::fs::remove_dir_all(home.parent().unwrap()).unwrap();
}

/// A Host's home kept for a process group it started that has not settled,
/// when neither the group's retirement monitor nor the keeper thread could be
/// started: a later start is refused and told why ([`KEPT`]); each later
/// attempt retries the monitor, so once the group has ended and its
/// settlement is established the home passes, and custody was never released
/// before that.
#[test]
fn a_kept_home_says_why_and_a_later_attempt_retries_the_settlement_monitor() {
    use crate::hosting::process_group_custody::OwnedProcess;
    use std::os::unix::process::CommandExt;
    let home = home();
    let gone = owner(false);
    let starting = Arc::new(AtomicUsize::new(0));
    let (hold, claim, _) = claim_host(&home, next_id(), weak(&gone), &starting).unwrap();
    drop(claim);
    let release = home.parent().unwrap().join("release");
    let process = OwnedProcess::spawn(
        std::process::Command::new("/bin/sh")
            .arg("-c")
            .arg(format!("while [ ! -e '{}' ]; do sleep 0.01; done", release.display()))
            .stdin(std::process::Stdio::null())
            .stdout(std::process::Stdio::null())
            .stderr(std::process::Stdio::null())
            .process_group(0),
    )
    .unwrap();
    drop(gone);
    keep_with_no_monitor_or_keeper_for_test(vec![hold], vec![Arc::clone(&process)]);
    let other = owner(false);
    let starting = Arc::new(AtomicUsize::new(0));
    // While the group lives: refused, and the home stays locked across processes.
    for _ in 0..3 {
        assert_eq!(claim_host(&home, next_id(), weak(&other), &starting).err().as_deref(), Some(KEPT));
    }
    assert!(peer(&home).contains("REFUSED"), "custody is kept");
    std::fs::write(&release, b"").unwrap();
    // The first refusal above started the monitor that establishes settlement.
    let deadline = std::time::Instant::now() + std::time::Duration::from_secs(5);
    let taken = loop {
        match claim_host(&home, next_id(), weak(&other), &starting) {
            Ok(taken) => break taken,
            Err(reason) => {
                assert_eq!(reason, KEPT);
                assert!(std::time::Instant::now() < deadline, "settlement was never established");
                std::thread::sleep(std::time::Duration::from_millis(20));
            }
        }
    };
    assert!(process.settled());
    drop(taken);
    assert!(peer(&home).contains("HELD"), "released once the taker lets go");
    std::fs::remove_dir_all(home.parent().unwrap()).unwrap();
}
