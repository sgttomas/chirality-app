//! DEL-01-01/05: one App at a time on a Codex home. Invented homes in
//! scratch folders; nothing is created inside a home.
use super::*;
use std::io::{BufRead, BufReader, Write as _};
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
    let (hold_a, claim) = claim_host(&home, a, weak(&first), &starting_a).unwrap();
    assert!(hold_a.is_some());
    // The same Host starting again keeps its hold.
    drop(claim);
    let (again, claim) = claim_host(&home, a, weak(&first), &starting_a).unwrap();
    assert!(again.is_none());
    drop(claim);
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
    let (hold_b, claim_b) = claim_host(&home, b, weak(&second), &starting_b).unwrap();
    drop(claim_b);
    drop(hold_a);
    second.0.store(true, Ordering::SeqCst);
    assert!(claim_host(&home, a, weak(&first), &starting_a).is_err(), "the home stays with its taker");
    // A dropped Host's home is free.
    drop(hold_b);
    let (hold, _claim) = claim_host(&home, a, weak(&first), &starting_a).unwrap();
    assert!(hold.is_some());
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
    let (hold, claim) = claim_host(&home, next_id(), weak(&host), &starting).expect("the App's own Host is not refused by its receiving source");
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
        Ok((hold, claim)) => {
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
    let (hold, _claim) = claim_host(&home, next_id(), weak(&here), &starting).expect("a killed holder strands no one");
    assert!(hold.is_some());
    assert!(contents(&home).is_empty());
    std::fs::remove_dir_all(home.parent().unwrap()).unwrap();
}
