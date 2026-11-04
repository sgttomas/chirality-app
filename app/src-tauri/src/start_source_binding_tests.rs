// Person-directed new starts (New conversation, Continue as, a clean trial)
// are bound to the full generation the person's choice was bound to at press,
// and to its home class. Uses the maintained local protocol peer; no
// supplier, credential or model.
use crate::home_resources::HomeClass;

fn starts_in(cwd: &std::path::Path) -> usize {
    std::fs::read_to_string(cwd.join("wire.jsonl")).unwrap_or_default().lines()
        .filter(|l| serde_json::from_str::<Value>(l).unwrap()["method"] == "thread/start").count()
}
fn thread_starts(peer: &Peer) -> usize {
    starts_in(&peer.fixture.root)
}
/// A separate key home sharing the account home's App session custody, with
/// its own folder (and so its own peer wire log).
struct KeyHome {
    home: Arc<HomeSession>,
    generation: Value,
    cwd: PathBuf,
}
impl KeyHome {
    fn beside(account: &Peer) -> Self {
        let mut config = account.home.host_config.clone().unwrap();
        let cwd = account.fixture.root.join("key-home");
        for dir in ["", "account", "probe"] { std::fs::create_dir_all(cwd.join(dir)).unwrap(); }
        (config.codex_home, config.probe_home, config.cwd) = (cwd.join("account"), cwd.join("probe"), cwd.clone());
        let host = Arc::new(crate::hosting::Host::new_with_app_custody(account.home.host.app_runtime_custody().unwrap()).unwrap());
        host.start(&config, "owned key fixture").unwrap();
        let generation = host.snapshot()["generation"].clone();
        Self { home: Arc::new(HomeSession::new(HomeClass::ApiKey, host, Ok(config)).unwrap()), generation, cwd }
    }
}
impl Drop for KeyHome {
    fn drop(&mut self) { let _ = self.home.host.stop("owned key fixture", "test ended"); }
}
fn routed(account: &Peer, key: Option<&KeyHome>) -> Mutex<HomeRouter> {
    let mut router = HomeRouter::new(account.home.clone()).unwrap();
    if let Some(key) = key {
        router.bind_key(key.home.clone()).unwrap();
    }
    Mutex::new(router)
}
/// A same-class replacement: the supplier is stopped and started again.
fn replaced(peer: &Peer) -> Value {
    peer.home.host.stop("fixture", "replaced source").unwrap();
    peer.relaunch()
}

#[test]
fn a_new_start_binds_only_the_exact_current_source_of_its_home_class() {
    let account = Peer::new();
    let key = KeyHome::beside(&account);
    let homes = routed(&account, Some(&key));
    let starts = (thread_starts(&account), starts_in(&key.cwd));
    let router = homes.lock().unwrap();
    // The matching source works, for each class.
    assert!(Arc::ptr_eq(&router.start_source(HomeClass::Account, &account.generation).unwrap(), &account.home));
    assert!(Arc::ptr_eq(&router.start_source(HomeClass::ApiKey, &key.generation).unwrap(), &key.home));
    // Home/class mismatch: the other home's generation never selects this class's home.
    let mismatch = router.start_source(HomeClass::ApiKey, &account.generation).err().unwrap();
    assert!(mismatch.contains("changed since you chose it"), "{mismatch}");
    assert!(router.start_source(HomeClass::Account, &key.generation).is_err());
    // An incomplete or altered tuple is refused; no part of it is filled in.
    for broken in [json!(null), json!("generation"), json!({}),
        json!({"appSession":account.generation["appSession"],"home":account.generation["home"]}),
        { let mut g = account.generation.clone(); g["extra"] = json!(1); g }] {
        let refused = router.start_source(HomeClass::Account, &broken).err().unwrap();
        assert!(refused.contains("full generation required"), "{broken}: {refused}");
    }
    for field in ["appSession", "home"] {
        let mut other = account.generation.clone();
        other[field] = json!("another");
        assert!(router.start_source(HomeClass::Account, &other).err().unwrap().contains("changed since you chose it"));
    }
    let mut later = account.generation.clone();
    later["spawnCounter"] = json!(account.generation["spawnCounter"].as_u64().unwrap() + 1);
    assert!(router.start_source(HomeClass::Account, &later).is_err(), "a stale or future spawn counter is not this source");
    // Without a key home, the key class has no source and no account fallback.
    drop(router);
    let only = routed(&account, None);
    assert!(only.lock().unwrap().start_source(HomeClass::ApiKey, &account.generation).err().unwrap().contains("no account fallback"));
    assert!(only.lock().unwrap().start_source(HomeClass::Probe, &account.generation).is_err());
    assert_eq!((thread_starts(&account), starts_in(&key.cwd)), starts, "no thread/start on any refusal");
}

#[test]
fn a_replaced_or_closed_source_is_refused_and_never_recaptured() {
    let peer = Peer::new();
    let homes = routed(&peer, None);
    let chosen = peer.generation.clone();
    // Same-class replacement: a restarted supplier is a new generation.
    let replacement = replaced(&peer);
    assert_ne!(replacement, chosen);
    let starts = thread_starts(&peer);
    assert!(homes.lock().unwrap().start_source(HomeClass::Account, &chosen).err().unwrap().contains("changed since you chose it"));
    assert!(homes.lock().unwrap().start_source(HomeClass::Account, &replacement).is_ok(), "the current source still works");
    // Source change during preparation: the pre-claim recheck refuses, and the
    // Host itself refuses a dispatch carrying the original generation; nothing
    // is sent under the replacement.
    assert!(check_start_source(&peer.home, &chosen).is_err());
    let cwd = peer.fixture.root.to_string_lossy().into_owned();
    assert!(peer.home.host.thread_start_with_guidance_dispatch(&chosen, &cwd, "fixture-model", "fixture-provider", "role").is_err());
    assert_eq!(thread_starts(&peer), starts, "no thread/start for the original source after its replacement");
    // Closed: after stop, the last generation is not a start source.
    peer.home.host.stop("fixture", "closed source").unwrap();
    let closed = homes.lock().unwrap().start_source(HomeClass::Account, &replacement).err().unwrap();
    assert!(closed.contains("closed or not ready") || closed.contains("changed since you chose it"), "{closed}");
    assert_eq!(thread_starts(&peer), starts);
}

#[test]
fn a_clean_trial_with_a_changed_source_is_refused_before_its_begin_and_keeps_the_prefill() {
    let peer = Peer::new();
    let homes = routed(&peer, None);
    let root = Mutex::new(trial_root(&peer));
    let reference = root.lock().unwrap().prepare_trial("clean", DRAFT, None, Some(&peer.home), peer.project()).unwrap()["reference"].as_str().unwrap().to_owned();
    let chosen = peer.generation.clone();
    let replacement = replaced(&peer);
    let (starts, turns, rs) = (thread_starts(&peer), peer.turn_starts(), peer.fixture.rs_entries());
    let refused = trial_flows::start_bound_clean_trial(&root, &homes, HomeClass::Account, &chosen, &reference,
        |_| panic!("no start for a changed source"), |_, _, _| panic!("nothing is sent")).err().unwrap();
    assert!(refused.prefill_kept && refused.contains("changed since you chose it"), "{refused}");
    assert!(pending_refs(&root).contains(&reference), "the pre-fill is kept");
    assert_eq!((thread_starts(&peer), peer.turn_starts(), peer.fixture.rs_entries()), (starts, turns, rs), "no native start, send or record");
    // A class with no source is refused the same way.
    assert!(trial_flows::start_bound_clean_trial(&root, &homes, HomeClass::ApiKey, &replacement, &reference,
        |_| panic!("no start"), |_, _, _| panic!("nothing is sent")).err().unwrap().prefill_kept);
    // The matching source starts the trial in the bound home (the refusals
    // left no begin step in flight, so this press is not refused as one).
    let mut started_in = None;
    let sent = trial_flows::start_bound_clean_trial(&root, &homes, HomeClass::Account, &replacement, &reference,
        |home| { started_in = Some(home.clone()); Ok(json!({"startGeneration":replacement,"result":{"thread":{"id":"thread"}}})) },
        |home, generation, thread| trial_flows::send_trial(&root, home, &reference, generation, thread, "")).unwrap();
    assert!(Arc::ptr_eq(started_in.as_ref().unwrap(), &peer.home));
    assert_eq!(sent["conversation"]["generation"], replacement);
    assert_eq!(peer.turn_starts(), turns + 1);
}
