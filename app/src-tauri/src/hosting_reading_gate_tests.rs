//! Configuration readings of one generation are made one at a time (`reading_gate`): stand-in
//! children only (`/bin/cat` echoes what reaches Codex's input; `/bin/sleep` never reads it).
use super::*;
use reading_gate::{settlement, ReadingStage, Unsettled, READING_GATE, READING_WITHDRAWN};
use std::io::{BufRead, BufReader};
use std::sync::mpsc::{channel, Receiver};
use std::time::{Duration, Instant};

const W: &str = "/invented/work";
const LONG: Duration = Duration::from_secs(5);

struct Rig {
    host: Arc<Host>,
    g: Value,
    child: Option<std::process::Child>,
    frames: Mutex<Receiver<Value>>,
}
impl Rig {
    fn new() -> Self {
        let host = Arc::new(Host::new());
        let g = json!({"appSession":"reading-gate-session","home":"reading-gate-home","spawnCounter":1});
        {
            let mut i = host.inner.0.lock().unwrap();
            i.generation = g.clone();
            i.state = "ready".into();
            i.supplier_standing = Some("synthetic; no provider contact".into());
            i.threads.push(json!({"generation":g,"threadId":"thread","cwd":"/invented/other","modelProvider":"openai"}));
        }
        let (child, frames) = Self::echo(&host);
        Rig { host, g, child: Some(child), frames: Mutex::new(frames) }
    }
    fn echo(host: &Host) -> (std::process::Child, Receiver<Value>) {
        let mut child = Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let stdout = child.stdout.take().unwrap();
        let (tx, rx) = channel();
        std::thread::spawn(move || {
            for line in BufReader::new(stdout).lines() {
                let Ok(line) = line else { break };
                if let Ok(frame) = serde_json::from_str::<Value>(&line) { if tx.send(frame).is_err() { break; } }
            }
        });
        (child, rx)
    }
    /// The next frame that reached Codex's input.
    fn frame(&self) -> Value { self.frames.lock().unwrap().recv_timeout(LONG).expect("a frame on Codex's input") }
    /// Nothing more reaches Codex's input within `wait`.
    fn none(&self, wait: Duration) {
        if let Ok(frame) = self.frames.lock().unwrap().recv_timeout(wait) { panic!("nothing should reach Codex's input, but {frame} did"); }
    }
    fn answer(&self, frame: &Value, result: Value) {
        self.host.on_line(&serde_json::to_vec(&json!({"id":frame["id"],"result":result})).unwrap(), &self.g);
    }
    fn error(&self, frame: &Value) {
        self.host.on_line(&serde_json::to_vec(&json!({"id":frame["id"],"error":{"code":-32603,"message":"invented"}})).unwrap(), &self.g);
    }
    fn current(&self) -> Option<String> { self.host.reading_current_for_test() }
    fn stage(&self) -> Option<(Option<String>, ReadingStage)> { self.host.reading_stage_for_test() }
    fn requests(&self) -> usize { self.host.inner.0.lock().unwrap().source_requests.len() }
    fn pending(&self) -> usize { self.host.inner.0.lock().unwrap().pending.len() }
    /// Signals once when the next reading finds the reservation held.
    fn on_waiting(&self) -> Receiver<()> {
        let (tx, rx) = channel();
        *self.host.reading_waiting.lock().unwrap() = Some(Box::new(move |_| { let _ = tx.send(()); }));
        rx
    }
    fn close(&self) {
        let mut i = self.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
    }
}
impl Drop for Rig {
    fn drop(&mut self) {
        *self.host.stdin.lock().unwrap() = None;
        if let Some(mut child) = self.child.take() { let _ = child.kill(); let _ = child.wait(); }
    }
}
fn cfg() -> Value { json!({"config":{"model_provider":"openai","model_providers":{}},"origins":{}}) }
fn admit(host: &Host, g: &Value, wait: Duration) -> Result<ProviderAdmission, String> {
    host.provider_admission_read_within(g, W, "chatgpt-account", "openai", "chosen-model", wait)
}
fn read(host: &Host, g: &Value, params: Value, wait: Duration) -> Result<SourceRequest, String> {
    host.request_reading("config/read", params, json!({"kind":"synthetic reader"}), g, false, Instant::now() + wait)
}
fn request_ref(frame_id: &Value, host: &Host) -> String {
    host.inner.0.lock().unwrap().source_requests[&frame_id.to_string()].request.request_ref.clone()
}

/// A first reading left unanswered keeps a second caller unregistered (the newest is still the
/// first; nothing of the second reaches Codex) until the first is answered; then the second
/// registers and proceeds. The competitor is each kind of reading; the second is a new start's
/// admission, which then starts.
#[test]
fn a_second_reading_registers_only_after_the_first_is_answered_and_the_start_then_proceeds() {
    for competitor in ["settings", "delegation-transport", "no-folder", "other-spelling", "requirements"] {
        let rig = Rig::new();
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let first = std::thread::spawn(move || match competitor {
            "settings" => host.effective_access_settings_read_within(&g, W, "account", LONG).map(|_| ()),
            "delegation-transport" => read(&host, &g, json!({"cwd":"/invented/other","includeLayers":false}), LONG).map(|_| ()),
            "no-folder" => read(&host, &g, json!({"includeLayers":false}), LONG).map(|_| ()),
            "other-spelling" => read(&host, &g, json!({"cwd":"/invented/work/","includeLayers":false}), LONG).map(|_| ()),
            _ => host.account_requirements_read_until(&g, Instant::now() + LONG).map(|_| ()),
        });
        let held = rig.frame();
        let held_ref = request_ref(&held["id"], &rig.host);
        let waiting = rig.on_waiting();
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let second = std::thread::spawn(move || admit(&host, &g, LONG));
        waiting.recv_timeout(LONG).expect("the admission finds the reservation held");
        std::thread::sleep(Duration::from_millis(100));
        assert_eq!(rig.current(), Some(held_ref.clone()), "{competitor}: the newest reading is still the first");
        assert_eq!(rig.stage().unwrap().0, Some(held["id"].to_string()), "{competitor}: the reservation names the first");
        rig.none(Duration::from_millis(150));
        // The first is answered: the admission registers, is written and answered.
        let first_result = if competitor == "requirements" { json!({"requirements":null}) } else { cfg() };
        rig.answer(&held, first_result);
        let admission = rig.frame();
        assert_eq!((admission["method"].as_str(), admission["params"]["cwd"].as_str()), (Some("config/read"), Some(W)), "{competitor}");
        rig.answer(&admission, cfg());
        let proof = second.join().unwrap().unwrap_or_else(|e| panic!("{competitor}: {e}"));
        let _ = first.join().unwrap();
        rig.host.thread_start_with_access_dispatch(&proof, "guidance").unwrap();
        assert_eq!(rig.frame()["method"], "thread/start", "{competitor}: the start proceeds on its own reading");
        assert!(rig.stage().is_none(), "{competitor}: nothing outstanding");
    }
}

/// The tick's delegation reading and the model list read go through the gate: with a reading
/// outstanding, each waits within its own budget and reports the gate sentence as its cause.
#[test]
fn the_delegation_and_model_list_readings_wait_at_the_gate() {
    let rig = Rig::new();
    rig.host.inner.0.lock().unwrap().server_cwd = Some(W.into());
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let first = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
    let held = rig.frame();
    let signals = rig.host.delegation_signals_read_within(&rig.g, "thread", json!({"kind":"app-rule","name":"delegation-availability-read"}), Duration::from_millis(300));
    assert!(signals.to_string().contains(READING_GATE), "the delegation reading names the gate: {signals}");
    let catalog = rig.host.model_catalog_read(&rig.g);
    assert!(catalog.to_string().contains(READING_GATE), "the model list read names the gate: {catalog}");
    // Only non-reading requests may have been sent meanwhile.
    while let Ok(frame) = rig.frames.lock().unwrap().recv_timeout(Duration::from_millis(100)) {
        assert_ne!(frame["method"], "config/read", "no second configuration reading reached Codex");
    }
    rig.answer(&held, cfg());
    first.join().unwrap().unwrap();
}

/// The reviewer's interval: a reading that registers after a request's final check and before
/// its write reaches Codex after that request's bytes.
#[test]
fn a_reading_registered_after_a_final_check_reaches_codex_after_that_request() {
    let rig = Rig::new();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let admitting = std::thread::spawn(move || admit(&host, &g, LONG));
    let frame = rig.frame();
    rig.answer(&frame, cfg());
    let proof = admitting.join().unwrap().unwrap();
    let (registered_tx, registered) = channel();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let reader: Arc<Mutex<Option<std::thread::JoinHandle<Result<SourceRequest, String>>>>> = Arc::default();
    let slot = reader.clone();
    *rig.host.before_request_write.lock().unwrap() = Some(Box::new(move |h| {
        *h.reading_after_register.lock().unwrap() = Some(Box::new(move |_| { let _ = registered_tx.send(()); }));
        *slot.lock().unwrap() = Some(std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG)));
        registered.recv_timeout(LONG).expect("the reading registers while the start holds the writer");
    }));
    rig.host.thread_start_with_access_dispatch(&proof, "guidance").unwrap();
    assert_eq!(rig.frame()["method"], "thread/start", "the admitted request's bytes are first");
    let later = rig.frame();
    assert_eq!(later["method"], "config/read", "then the reading's");
    rig.answer(&later, cfg());
    reader.lock().unwrap().take().unwrap().join().unwrap().unwrap();
}

/// Waiters are served in arrival order: an admission that began waiting first is the next reading
/// registered, before App readers that began waiting after it, every time.
#[test]
fn an_admission_waiting_first_is_served_before_app_readers_that_came_after() {
    let wait_for = |rig: &Rig, n: usize| {
        let deadline = Instant::now() + LONG;
        while rig.host.reading_waiting_count_for_test() < n { assert!(Instant::now() < deadline, "{n} waiting"); std::thread::sleep(Duration::from_millis(2)); }
    };
    for round in 0..10 {
        let rig = Rig::new();
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let first = std::thread::spawn(move || read(&host, &g, json!({"cwd":"/invented/other","includeLayers":false}), LONG));
        let held = rig.frame();
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let admission = std::thread::spawn(move || admit(&host, &g, LONG));
        wait_for(&rig, 1);
        let readers: Vec<_> = (0..4).map(|_| {
            let (host, g) = (rig.host.clone(), rig.g.clone());
            std::thread::spawn(move || read(&host, &g, json!({"cwd":"/invented/other","includeLayers":false}), LONG))
        }).collect();
        wait_for(&rig, 5);
        rig.answer(&held, cfg());
        let next = rig.frame();
        assert_eq!((next["params"]["cwd"].as_str(), next["params"]["includeLayers"].as_bool()), (Some(W), Some(true)), "round {round}: the admission is served first");
        rig.answer(&next, cfg());
        // Its reply frees the reservation and a reader already waiting registers at once, so the
        // admission's own proof may already be superseded: the decided window after a reply.
        let _ = admission.join().unwrap();
        for _ in 0..4 { let frame = rig.frame(); rig.answer(&frame, cfg()); }
        for reader in readers { reader.join().unwrap().unwrap(); }
        first.join().unwrap().unwrap();
    }
}

/// The gate's wait expiring, with one reading outstanding and never answered (the stand-in silent):
/// each later reading returns the gate sentence within its own deadline, the settings reading (which
/// reaches the person) included; nothing registered, nothing on Codex's input.
#[test]
fn the_gate_wait_expiring_gives_the_gate_sentence_and_registers_nothing() {
    let rig = Rig::new();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let first = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
    let _never_answered = rig.frame();
    first.join().unwrap().unwrap();
    let (requests, pending) = (rig.requests(), rig.pending());
    let budget = Duration::from_millis(150);
    let within = |label: &str, call: &dyn Fn() -> Option<String>| {
        let started = Instant::now();
        assert_eq!(call().as_deref(), Some(READING_GATE), "{label}");
        assert!(started.elapsed() < budget + Duration::from_millis(250), "{label}: returned within its own deadline ({:?})", started.elapsed());
    };
    within("a reading", &|| read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), budget).err());
    within("an admission passes the sentence on as it is", &|| admit(&rig.host, &rig.g, budget).err());
    within("the settings reading too", &|| rig.host.effective_access_settings_read_within(&rig.g, W, "account", budget).err());
    within("a requirements reading too", &|| rig.host.account_requirements_read_until(&rig.g, Instant::now() + budget).err());
    assert_eq!((rig.requests(), rig.pending()), (requests, pending), "nothing registered, nothing pending");
    rig.none(Duration::from_millis(100));
}

/// A valid terminal envelope ends the exchange even when its result is not usable: a result with
/// no configuration object, or one naming no definition the entry can use, supplies no proof, yet
/// the reservation is released and the next reading registers at once.
#[test]
fn an_unusable_result_supplies_no_proof_but_releases_the_reservation() {
    for (label, entry, provider, result) in [
        ("no configuration object", "chatgpt-account", "openai", json!({"origins":{}})),
        ("no usable provider definition", "local-provider", "anonymous", cfg()),
    ] {
        let rig = Rig::new();
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let admitting = std::thread::spawn(move || host.provider_admission_read_within(&g, W, entry, provider, "chosen-model", LONG));
        let frame = rig.frame();
        rig.answer(&frame, result);
        assert!(admitting.join().unwrap().is_err(), "{label}: no proof");
        assert!(rig.stage().is_none(), "{label}: the exchange is finished and the reservation released");
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let next = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
        let after = rig.frame();
        assert_ne!(after["id"], frame["id"], "{label}: the next reading registered at once");
        rig.answer(&after, cfg());
        next.join().unwrap().unwrap();
    }
}

/// A reply after its caller gave up: the reservation is held meanwhile and a later admission is
/// refused at the gate; on the late reply it is free, the abandoned reading admits nothing, and a
/// new admission makes its own reading.
#[test]
fn a_late_reply_frees_the_reservation_and_the_abandoned_reading_admits_nothing() {
    let rig = Rig::new();
    assert!(admit(&rig.host, &rig.g, Duration::from_millis(100)).is_err(), "the caller gives up");
    let abandoned = rig.frame();
    assert_eq!(rig.stage(), Some((Some(abandoned["id"].to_string()), ReadingStage::Abandoned)));
    assert_eq!(admit(&rig.host, &rig.g, Duration::from_millis(150)).err().unwrap(), READING_GATE, "held meanwhile");
    rig.none(Duration::from_millis(50));
    rig.answer(&abandoned, cfg());
    assert!(rig.stage().is_none(), "the late reply frees the reservation");
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let fresh = std::thread::spawn(move || admit(&host, &g, LONG));
    let own = rig.frame();
    assert_ne!(own["id"], abandoned["id"], "a new reading of its own");
    rig.answer(&own, cfg());
    let proof = fresh.join().unwrap().unwrap();
    rig.host.thread_start_with_access_dispatch(&proof, "guidance").unwrap();
    assert_eq!(rig.frame()["method"], "thread/start");
}

/// An error reply frees the reservation and makes no proof; a withdrawn reading frees it too. In
/// both, no older proof is current again.
#[test]
fn an_error_reply_or_a_withdrawal_frees_the_reservation_and_restores_no_older_proof() {
    for ending in ["error", "withdrawn"] {
        let rig = Rig::new();
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let admitting = std::thread::spawn(move || admit(&host, &g, LONG));
        let frame = rig.frame();
        rig.answer(&frame, cfg());
        let older = admitting.join().unwrap().unwrap();
        if ending == "error" {
            let (host, g) = (rig.host.clone(), rig.g.clone());
            let errored = std::thread::spawn(move || admit(&host, &g, LONG));
            let frame = rig.frame();
            rig.error(&frame);
            assert!(errored.join().unwrap().is_err(), "an error makes no proof");
        } else {
            let writer = rig.host.frame_write.lock().unwrap();
            assert_eq!(read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), Duration::from_millis(100)).err().unwrap(), READING_WITHDRAWN);
            drop(writer);
            assert!(rig.current().is_none(), "withdrawn: no reading is current");
            rig.none(Duration::from_millis(100));
        }
        assert!(rig.stage().is_none(), "{ending}: the reservation is free");
        assert!(rig.host.thread_start_with_access_dispatch(&older, "guidance").is_err(), "{ending}: the older proof is not current again");
        rig.none(Duration::from_millis(50));
    }
}

/// Withdrawal and write admission are exclusive, in both orders: a reading whose deadline is found
/// passed once it has the writer is withdrawn and writes nothing; a reading admitted to its write
/// before its deadline is written even if the deadline passes during the write, and is never
/// told it was not sent. The second reading's limit is LONG, so the work before its write does not
/// use it up, and it is held at the write until that deadline has passed.
#[test]
fn withdrawal_and_write_admission_exclude_each_other_in_both_orders() {
    let rig = Rig::new();
    *rig.host.reading_after_register.lock().unwrap() = Some(Box::new(|_| std::thread::sleep(Duration::from_millis(200))));
    assert_eq!(read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), Duration::from_millis(100)).err().unwrap(), READING_WITHDRAWN);
    assert!(rig.stage().is_none() && rig.current().is_none());
    rig.none(Duration::from_millis(100));
    let deadline = Instant::now() + LONG;
    *rig.host.before_request_write.lock().unwrap() = Some(Box::new(move |_| std::thread::sleep((deadline + Duration::from_millis(100)).saturating_duration_since(Instant::now()))));
    let source = rig.host.request_reading("config/read", json!({"cwd":W,"includeLayers":false}), json!({"kind":"synthetic reader"}), &rig.g, false, deadline).expect("admitted before its deadline: written");
    assert!(Instant::now() > deadline, "its deadline passed during the write");
    let frame = rig.frame();
    assert_eq!(frame["id"], *source.request_id());
    assert_eq!(rig.stage(), Some((Some(frame["id"].to_string()), ReadingStage::AwaitingReply)), "outstanding, never withdrawn");
    rig.answer(&frame, cfg());
    assert!(rig.stage().is_none());
}

/// A caller that goes away (here: its thread unwinding) before its write withdraws the reading,
/// at Reserved and at Registered; after WriteStarted it only abandons, and the reading stays
/// outstanding until the generation closes.
#[test]
fn a_caller_unwinding_withdraws_before_its_write_and_abandons_after() {
    for stage in ["reserved", "registered", "write-started"] {
        let rig = Rig::new();
        match stage {
            "reserved" => *rig.host.reading_after_reserve.lock().unwrap() = Some(Box::new(|_| panic!("invented unwinding at Reserved"))),
            "registered" => *rig.host.reading_after_register.lock().unwrap() = Some(Box::new(|_| panic!("invented unwinding at Registered"))),
            _ => *rig.host.before_request_write.lock().unwrap() = Some(Box::new(|_| panic!("invented unwinding after WriteStarted"))),
        }
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let unwound = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG)).join();
        assert!(unwound.is_err(), "{stage}: the caller's thread unwound");
        rig.none(Duration::from_millis(100));
        if stage == "write-started" {
            assert!(matches!(rig.stage(), Some((Some(_), ReadingStage::WriteStarted))), "{stage}: outstanding");
            assert_eq!(read(&rig.host, &rig.g, json!({"cwd":W}), Duration::from_millis(100)).err().unwrap(), READING_GATE, "{stage}");
            rig.close();
            assert!(rig.stage().is_none(), "{stage}: it ends with the generation");
        } else {
            assert!(rig.stage().is_none(), "{stage}: withdrawn");
            assert!(rig.current().is_none(), "{stage}: no reading is current");
            assert_eq!(rig.pending(), 0, "{stage}: nothing pending");
            let (host, g) = (rig.host.clone(), rig.g.clone());
            let next = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
            let frame = rig.frame();
            rig.answer(&frame, cfg());
            next.join().unwrap().unwrap();
        }
    }
}

/// A reply that releases the reservation before its sender's own cleanup has run, with another
/// reading already registered: the cleanup does not touch the successor, nor does a duplicate
/// reply.
#[test]
fn a_reply_before_its_senders_cleanup_never_clears_a_successor() {
    let rig = Rig::new();
    let (registered_tx, registered) = channel();
    let successor: Arc<Mutex<Option<std::thread::JoinHandle<Result<SourceRequest, String>>>>> = Arc::default();
    let slot = successor.clone();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    *rig.host.before_request_write.lock().unwrap() = Some(Box::new(move |h| {
        // The first reading is admitted to its write: its reply arrives now, before its write and
        // its cleanup, and a second reading registers and waits for the writer.
        let (id, generation) = { let i = h.inner.0.lock().unwrap(); (i.reading_slot.as_ref().unwrap().request_id.clone().unwrap(), i.generation.clone()) };
        h.on_line(&serde_json::to_vec(&json!({"id":serde_json::from_str::<Value>(&id).unwrap(),"result":cfg()})).unwrap(), &generation);
        *h.reading_after_register.lock().unwrap() = Some(Box::new(move |_| { let _ = registered_tx.send(()); }));
        *slot.lock().unwrap() = Some(std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG)));
        registered.recv_timeout(LONG).unwrap();
    }));
    let first = read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), LONG).unwrap();
    let written_first = rig.frame();
    assert_eq!(written_first["id"], *first.request_id());
    let second = rig.frame();
    assert_ne!(second["id"], written_first["id"]);
    // Seeing the echoed frame does not mean its sender's post-write step has run: either
    // outstanding stage, naming the successor.
    let outstanding = |rig: &Rig| matches!(rig.stage(), Some((Some(id), ReadingStage::WriteStarted | ReadingStage::AwaitingReply)) if id == second["id"].to_string());
    assert!(outstanding(&rig), "the first's cleanup left the successor alone: {:?}", rig.stage());
    assert_eq!(rig.current(), Some(request_ref(&second["id"], &rig.host)));
    rig.answer(&written_first, cfg());
    assert!(outstanding(&rig), "a duplicate reply releases nothing: {:?}", rig.stage());
    rig.answer(&second, cfg());
    successor.lock().unwrap().take().unwrap().join().unwrap().unwrap();
    assert!(rig.stage().is_none());
}

/// The generation closed with a reading outstanding: its waiter is released, the next
/// generation's first reading is not held up, and the old generation's late reply releases
/// nothing of the new one's.
#[test]
fn a_close_ends_the_reading_and_an_old_generations_late_reply_touches_nothing() {
    let rig = Rig::new();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let waiting = std::thread::spawn(move || admit(&host, &g, LONG));
    let old = rig.frame();
    let started = Instant::now();
    rig.close();
    assert!(waiting.join().unwrap().is_err(), "the waiter is released");
    assert!(started.elapsed() < Duration::from_secs(2));
    let next = json!({"appSession":"reading-gate-session","home":"reading-gate-home","spawnCounter":2});
    { let mut i = rig.host.inner.0.lock().unwrap(); i.generation = next.clone(); i.state = "ready".into(); }
    let (host, g) = (rig.host.clone(), next.clone());
    let fresh = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
    let frame = rig.frame();
    assert_ne!(frame["id"], old["id"]);
    // A reply naming the old generation and this request's identity releases nothing, at the
    // release itself (the frame reader also discards a line of a generation no longer current).
    assert!(!Host::reading_reply_locked(&mut rig.host.inner.0.lock().unwrap(), &rig.g, &frame["id"].to_string()), "another generation's reply releases nothing");
    rig.host.on_line(&serde_json::to_vec(&json!({"id":frame["id"],"result":cfg()})).unwrap(), &rig.g);
    assert!(matches!(rig.stage(), Some((Some(id), ReadingStage::WriteStarted | ReadingStage::AwaitingReply)) if id == frame["id"].to_string()), "a reply naming the old generation releases nothing: {:?}", rig.stage());
    rig.host.on_line(&serde_json::to_vec(&json!({"id":frame["id"],"result":cfg()})).unwrap(), &next);
    fresh.join().unwrap().unwrap();
    assert!(rig.stage().is_none());
}

/// A real blocked pipe write (a stand-in that never reads, its pipe filled by the reading's own
/// large frame): the reading stays outstanding, later readings get the gate sentence, and the
/// blocked one is never told it was not sent; a write error after the attempt leaves the reading
/// outstanding as well.
///
/// The blocked reading's limit is counted from the call, before its large frame is built and the
/// writer taken, and no write begins once it has passed; it is LONG, so that work does not use it
/// up, and the test waits it out before asking whether the reading is still outstanding. A return
/// before the write is observed fails, whatever it says and whenever it is noticed.
#[test]
fn a_blocked_or_failed_write_keeps_its_reading_outstanding_and_is_never_called_not_sent() {
    let rig = Rig::new();
    let mut sleeper = Command::new("/bin/sleep").arg("30").env_clear().stdin(Stdio::piped()).stdout(Stdio::null()).stderr(Stdio::null()).spawn().unwrap();
    *rig.host.stdin.lock().unwrap() = sleeper.stdin.take();
    let (host, g, deadline) = (rig.host.clone(), rig.g.clone(), Instant::now() + LONG);
    let blocked = std::thread::spawn(move || host.request_reading("config/read", json!({"cwd":"x".repeat(4 * 1024 * 1024),"includeLayers":false}), json!({"kind":"synthetic reader"}), &g, false, deadline));
    while !matches!(rig.stage(), Some((Some(_), ReadingStage::WriteStarted))) {
        if blocked.is_finished() {
            panic!("the blocked reading returned before it was observed inside its write (withdrawn, or a stand-in that reads its input?): {:?}", blocked.join().unwrap().map(|_| rig.stage()));
        }
        assert!(Instant::now() < deadline + LONG, "the blocked reading neither started its write nor returned");
        std::thread::sleep(Duration::from_millis(5));
    }
    std::thread::sleep((deadline + Duration::from_millis(100)).saturating_duration_since(Instant::now()));
    assert!(matches!(rig.stage(), Some((Some(_), ReadingStage::WriteStarted))), "inside the write past its deadline: still outstanding");
    assert!(!blocked.is_finished(), "the caller inside the write cannot be timed out");
    assert_eq!(read(&rig.host, &rig.g, json!({"cwd":W}), Duration::from_millis(150)).err().unwrap(), READING_GATE);
    sleeper.kill().unwrap(); sleeper.wait().unwrap();
    let result = blocked.join().unwrap();
    assert!(result.as_ref().err().is_none_or(|e| !e.contains("not sent")), "the attempted write is never called not sent: {:?}", result.as_ref().err());
    assert!(matches!(rig.stage(), Some((Some(_), ReadingStage::WriteFailed))), "a write error after the attempt: still outstanding");
    assert_eq!(read(&rig.host, &rig.g, json!({"cwd":W}), Duration::from_millis(150)).err().unwrap(), READING_GATE);
    rig.close();
    assert!(rig.stage().is_none());
    // A write that fails at once (an input that cannot be written) is outstanding too.
    let rig = Rig::new();
    let _kept = install_broken_test_input(&rig.host);
    let failed = read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), LONG).expect("an attempted write is not refused as not sent");
    assert_eq!(failed.evidence()["writeResult"], "write-failed");
    assert!(matches!(rig.stage(), Some((Some(_), ReadingStage::WriteFailed))));
    assert_eq!(admit(&rig.host, &rig.g, Duration::from_millis(150)).err().unwrap(), READING_GATE);
}

/// Only a well-formed terminal reply releases a reading: an envelope with both a result and an
/// error is contradictory (settlement rejects it) and leaves the reading outstanding, so a reading
/// started meanwhile does not register until the genuine reply arrives.
#[test]
fn a_contradictory_envelope_releases_nothing_and_only_the_genuine_reply_does() {
    let rig = Rig::new();
    read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), LONG).unwrap();
    let held = rig.frame();
    let held_ref = request_ref(&held["id"], &rig.host);
    rig.host.on_line(&serde_json::to_vec(&json!({"id":held["id"],"result":cfg(),"error":{"code":-32603,"message":"invented"}})).unwrap(), &rig.g);
    assert!(matches!(rig.stage(), Some((Some(id), _)) if id == held["id"].to_string()), "a contradictory envelope releases nothing: {:?}", rig.stage());
    assert!(!rig.host.inner.0.lock().unwrap().pending.contains_key(&held["id"].to_string()), "handling the malformed frame removed the original waiter");
    let waiting = rig.on_waiting();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let next = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
    waiting.recv_timeout(LONG).expect("the next reading finds the reservation held");
    std::thread::sleep(Duration::from_millis(100));
    assert_eq!(rig.current(), Some(held_ref), "the next reading has not registered");
    rig.none(Duration::from_millis(150));
    rig.answer(&held, cfg());
    let frame = rig.frame();
    assert_ne!(frame["id"], held["id"], "the genuine reply released it: the next reading registered");
    rig.answer(&frame, cfg());
    next.join().unwrap().unwrap();
}

/// A reply settlement rejects releases nothing, whatever its shape: an error with no integer code and
/// string message (an empty error object, a code that is not an integer) leaves the reading
/// outstanding; the later reply settlement accepts releases it, and a reading queued meanwhile
/// registers only then.
#[test]
fn an_error_settlement_rejects_releases_nothing_and_only_the_later_valid_reply_does() {
    for (label, error, valid_error) in [
        ("an empty error object", json!({}), false),
        ("a code that is not an integer", json!({"code":"-32603","message":"invented"}), true),
        ("a fractional code", json!({"code":-32603.5,"message":"invented"}), false),
    ] {
        let rig = Rig::new();
        read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), LONG).unwrap();
        let held = rig.frame();
        let held_ref = request_ref(&held["id"], &rig.host);
        rig.host.on_line(&serde_json::to_vec(&json!({"id":held["id"],"error":error})).unwrap(), &rig.g);
        assert!(matches!(rig.stage(), Some((Some(id), _)) if id == held["id"].to_string()), "{label}: releases nothing: {:?}", rig.stage());
        let waiting = rig.on_waiting();
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let next = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
        waiting.recv_timeout(LONG).expect("the next reading finds the reservation held");
        std::thread::sleep(Duration::from_millis(100));
        assert_eq!(rig.current(), Some(held_ref), "{label}: the next reading has not registered");
        rig.none(Duration::from_millis(150));
        if valid_error { rig.error(&held); } else { rig.answer(&held, cfg()); }
        let frame = rig.frame();
        assert_ne!(frame["id"], held["id"], "{label}: the valid reply released it and the next reading registered");
        rig.answer(&frame, cfg());
        next.join().unwrap().unwrap();
    }
}

/// Settlement keeps its own refusal for each way it rejects a reply, and accepts a valid error and a
/// valid result; the release uses this same test (`reading_gate::settlement`).
#[test]
fn settlement_keeps_its_refusal_for_each_way_a_reply_is_rejected() {
    const ENVELOPE: &str = "Native reply envelope malformed/contradictory; canonical settlement projection unavailable";
    const ERROR: &str = "Actual native error code/message unavailable; no invented canonical error";
    const RESULT: &str = "Native reply result missing; canonical settlement projection unavailable";
    for (frame, expected) in [
        (json!({"id":7,"result":{},"error":{"code":1,"message":"m"}}), ENVELOPE),
        (json!({"id":8,"result":{}}), ENVELOPE),
        (json!({"id":7,"method":"invented","result":{}}), ENVELOPE),
        (json!([7]), ENVELOPE),
        (json!({"id":7,"error":{}}), ERROR),
        (json!({"id":7,"error":{"code":"1","message":"m"}}), ERROR),
        (json!({"id":7,"error":{"code":1}}), ERROR),
        (json!({"id":7}), RESULT),
    ] {
        let mut record = json!({"requestIdentity":7});
        let verdict = settlement(&frame, record.get("requestIdentity"));
        assert_eq!(Host::completed_client_response(&mut record, Some(&frame), Some(1), Some(verdict)).unwrap_err(), expected, "{frame}");
    }
    let mut record = json!({"requestIdentity":7});
    assert_eq!(Host::completed_client_response(&mut record, Some(&json!({"id":7,"result":{}})), Some(1), None).unwrap_err(), ENVELOPE, "a reply with no verdict taken at receipt is not accepted");
    for (frame, outcome) in [(json!({"id":7,"error":{"code":-32603,"message":"m"}}), "response-observed-error"), (json!({"id":7,"result":{}}), "response-observed-result")] {
        let mut record = json!({"requestIdentity":7});
        let verdict = settlement(&frame, record.get("requestIdentity"));
        Host::completed_client_response(&mut record, Some(&frame), Some(2), Some(verdict)).unwrap();
        assert_eq!(record["outcome"], outcome);
    }
}

/// Settlement's verdict is taken on the reply exactly as Codex sent it, before the host's privacy
/// projections. A private configuration reading's error with a code and no message, and a
/// requirements reading's error with no message or a message that is not a string, are rejected as
/// sent, though each projection (`access_provider::withheld`, `auth_rpc::project_received_frame`)
/// replaces the message with a fixed one. Each leaves the reading held; the later valid reply
/// releases it, and a reading queued meanwhile registers only then. Lines go through `on_line`.
#[test]
fn a_reply_invalid_as_codex_sent_it_releases_nothing_though_its_projection_looks_valid() {
    for (label, error) in [
        ("private configuration, no message", json!({"code":-32603})),
        ("requirements, no message", json!({"code":-32603})),
        ("requirements, a message that is not a string", json!({"code":-32603,"message":7})),
    ] {
        let rig = Rig::new();
        let private = label.starts_with("private");
        let admitting = if private {
            let (host, g) = (rig.host.clone(), rig.g.clone());
            Some(std::thread::spawn(move || admit(&host, &g, LONG)))
        } else {
            rig.host.account_requirements_read_until(&rig.g, Instant::now() + LONG).unwrap();
            None
        };
        let held = rig.frame();
        assert_eq!(held["method"], if private { "config/read" } else { "configRequirements/read" }, "{label}");
        let held_ref = request_ref(&held["id"], &rig.host);
        rig.host.on_line(&serde_json::to_vec(&json!({"id":held["id"],"error":error})).unwrap(), &rig.g);
        if let Some(admitting) = admitting { assert!(admitting.join().unwrap().is_err(), "{label}: no proof"); }
        {
            let i = rig.host.inner.0.lock().unwrap();
            let e = &i.source_requests[&held["id"].to_string()];
            assert!(e.response.as_ref().is_some_and(|r| r["error"]["message"].is_string()), "{label}: the stored reply was projected to a valid-looking error: {:?}", e.response);
            assert_eq!(e.native_settlement, Some(Err(Unsettled::ErrorShape)), "{label}: the verdict was taken on the reply as sent");
            assert_eq!(e.source_limit.as_deref(), Some("Actual native error code/message unavailable; no invented canonical error"), "{label}: settlement refused it with the same verdict");
        }
        assert!(matches!(rig.stage(), Some((Some(id), _)) if id == held["id"].to_string()), "{label}: releases nothing: {:?}", rig.stage());
        let waiting = rig.on_waiting();
        let (host, g) = (rig.host.clone(), rig.g.clone());
        let next = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
        waiting.recv_timeout(LONG).expect("the next reading finds the reservation held");
        std::thread::sleep(Duration::from_millis(100));
        assert_eq!(rig.current(), Some(held_ref), "{label}: the next reading has not registered");
        rig.none(Duration::from_millis(150));
        rig.error(&held);
        let frame = rig.frame();
        assert_ne!(frame["id"], held["id"], "{label}: the valid reply released it and the next reading registered");
        rig.answer(&frame, cfg());
        next.join().unwrap().unwrap();
    }
}

/// The generic synchronous route gives a reading one deadline from the call's start: time spent
/// waiting for the reservation leaves only the remainder for the reply.
#[test]
fn the_generic_route_waits_for_a_readings_reply_only_for_what_remains_of_its_deadline() {
    let rig = Rig::new();
    read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), LONG).unwrap();
    let held = rig.frame();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let started = Instant::now();
    let generic = std::thread::spawn(move || {
        let result = host.request_inner_scoped("config/read", json!({"cwd":W,"includeLayers":false}), json!({"kind":"synthetic generic"}), Duration::from_millis(1000), false, Some(&g));
        (result, started.elapsed())
    });
    std::thread::sleep(Duration::from_millis(600));
    rig.answer(&held, cfg());
    assert_eq!(rig.frame()["method"], "config/read", "registered once the reservation was free, and left unanswered");
    let (result, elapsed) = generic.join().unwrap();
    assert!(result.is_err(), "no reply within its deadline");
    assert!(elapsed < Duration::from_millis(1350), "the whole call is bounded by its one deadline: {elapsed:?}");
}

fn continue_query(rig: &Rig) -> HistoryQuery {
    let mut view = NativeHistory::new("reading-gate-home", rig.g.clone()).unwrap();
    let q = view.list_threads(None, crate::native_history::Direction::Desc).unwrap();
    let stored = json!({"id":"stored","cliVersion":"0.167.0","createdAt":1,"updatedAt":2,"cwd":"/invented","ephemeral":false,"modelProvider":"openai","preview":"invented","projectId":null,"sessionId":"native-session","source":"appServer","status":{"type":"notLoaded"},"turns":[]});
    view.receive(&q, "reading-gate-home", &rig.g, &json!({"data":[stored],"nextCursor":null})).unwrap();
    view.select("stored").unwrap();
    view.continue_query().unwrap()
}

/// Option A's account Continue and fork rest on their own configuration reading: with an earlier
/// reading of the generation unanswered, the operation's reading is not registered (nothing of it
/// on Codex's input) until that reading is answered; then it registers, is answered, and the
/// operation is sent. Each kind of competitor.
#[test]
fn an_account_continue_or_fork_reads_only_after_an_earlier_reading_is_answered() {
    for operation in ["thread/resume", "thread/fork"] {
        for competitor in ["settings", "delegation-transport", "no-folder", "other-spelling", "requirements"] {
            let rig = Rig::new();
            rig.host.inner.0.lock().unwrap().server_cwd = Some(W.into());
            let (host, g) = (rig.host.clone(), rig.g.clone());
            let first = std::thread::spawn(move || match competitor {
                "settings" => host.effective_access_settings_read_within(&g, W, "account", LONG).map(|_| ()),
                "delegation-transport" => read(&host, &g, json!({"cwd":"/invented/other","includeLayers":false}), LONG).map(|_| ()),
                "no-folder" => read(&host, &g, json!({"includeLayers":false}), LONG).map(|_| ()),
                "other-spelling" => read(&host, &g, json!({"cwd":"/invented/work/","includeLayers":false}), LONG).map(|_| ()),
                _ => host.account_requirements_read_until(&g, Instant::now() + LONG).map(|_| ()),
            });
            let held = rig.frame();
            let held_ref = request_ref(&held["id"], &rig.host);
            let waiting = rig.on_waiting();
            let query = continue_query(&rig);
            let (host, g) = (rig.host.clone(), rig.g.clone());
            let second = std::thread::spawn(move || if operation == "thread/resume" { host.history_dispatch(&query).map(|_| ()) } else { host.thread_fork_dispatch(&g, "thread").map(|_| ()) });
            waiting.recv_timeout(LONG).expect("the operation's reading finds the reservation held");
            std::thread::sleep(Duration::from_millis(100));
            assert_eq!(rig.current(), Some(held_ref.clone()), "{operation} {competitor}: the newest is still the first");
            rig.none(Duration::from_millis(150));
            rig.answer(&held, if competitor == "requirements" { json!({"requirements":null}) } else { cfg() });
            let reading = rig.frame();
            assert_eq!((reading["method"].as_str(), reading["params"]["cwd"].as_str()), (Some("config/read"), Some(W)), "{operation} {competitor}");
            rig.answer(&reading, cfg());
            assert_eq!(rig.frame()["method"], operation, "{operation} {competitor}: sent on its own reading");
            second.join().unwrap().unwrap_or_else(|e| panic!("{operation} {competitor}: {e}"));
            let _ = first.join().unwrap();
        }
    }
}

/// A requirements reading that registers between an account Continue's final check and its write
/// reaches Codex after the Continue's bytes.
#[test]
fn a_requirements_reading_after_continues_final_check_reaches_codex_after_it() {
    let rig = Rig::new();
    rig.host.inner.0.lock().unwrap().server_cwd = Some(W.into());
    let query = continue_query(&rig);
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let reader: Arc<Mutex<Option<std::thread::JoinHandle<Result<SourceRequest, String>>>>> = Arc::default();
    let slot = reader.clone();
    let (registered_tx, registered) = channel();
    let host_for = rig.host.clone();
    let continuing = std::thread::spawn(move || host_for.history_dispatch(&query).map(|_| ()));
    let reading = rig.frame();
    // The Continue's own reading is answered; its request is then held after its final check.
    *rig.host.before_request_write.lock().unwrap() = Some(Box::new(move |h| {
        *h.reading_after_register.lock().unwrap() = Some(Box::new(move |_| { let _ = registered_tx.send(()); }));
        *slot.lock().unwrap() = Some(std::thread::spawn(move || host.account_requirements_read_until(&g, Instant::now() + LONG)));
        registered.recv_timeout(LONG).expect("the requirements reading registers while the Continue holds the writer");
    }));
    rig.answer(&reading, cfg());
    assert_eq!(rig.frame()["method"], "thread/resume", "the Continue's bytes are first");
    let requirements = rig.frame();
    assert_eq!(requirements["method"], "configRequirements/read", "then the requirements reading's");
    continuing.join().unwrap().unwrap();
    rig.answer(&requirements, json!({"requirements":null}));
    reader.lock().unwrap().take().unwrap().join().unwrap().unwrap();
}

/// An account Continue or fork refused at its own configuration reading passes the sentence on as it
/// is (`cloud_continuation_admission`), as a start's admission does: nothing of the operation is
/// registered or reaches Codex, and the fork's role-supply record takes it as refused before send,
/// with the sentence alone as its message. The gate: an earlier reading is left unanswered. The
/// withdrawal: the reservation is free and the frame writer is held past the deadline.
#[test]
fn an_account_continue_or_fork_refused_at_its_reading_passes_the_sentence_on_and_is_known_not_sent() {
    for operation in ["thread/resume", "thread/fork"] {
        for sentence in [READING_GATE, READING_WITHDRAWN] {
            let rig = Rig::new();
            rig.host.inner.0.lock().unwrap().server_cwd = Some(W.into());
            *rig.host.continuation_reading_budget.lock().unwrap() = Some(Duration::from_millis(150));
            if sentence == READING_GATE {
                read(&rig.host, &rig.g, json!({"cwd":"/invented/other","includeLayers":false}), LONG).unwrap();
                let _never_answered = rig.frame();
            }
            let query = continue_query(&rig);
            let home = crate::runtime_session::HomeSession::new(crate::home_resources::HomeClass::Account, rig.host.clone(), Err("synthetic reading-gate home".into())).unwrap();
            let (requests, pending) = (rig.requests(), rig.pending());
            let writer = (sentence == READING_WITHDRAWN).then(|| rig.host.frame_write.lock().unwrap());
            let refused = if operation == "thread/resume" {
                rig.host.history_dispatch(&query).map(|_| ()).unwrap_err()
            } else {
                crate::conversation_roles::fork_conversation_tracked(&home, &rig.g, "thread", LONG, |_| panic!("{operation}: nothing is dispatched")).map(|_| ()).unwrap_err()
            };
            drop(writer);
            assert_eq!(refused, sentence, "{operation}: the sentence alone, not the built-in-provider refusal");
            assert!(crate::conversation_roles::fork_refused_before_send(&refused), "{operation}: recorded as refused before send");
            assert_eq!(crate::role_supply_refusal(&refused, &"invented publication"), sentence, "{operation}: nothing is shown with the sentence");
            if sentence == READING_GATE {
                assert_eq!((rig.requests(), rig.pending()), (requests, pending), "{operation}: at the gate nothing is registered, nothing pending");
            } else {
                assert_eq!(rig.pending(), pending, "{operation}: withdrawn, nothing pending");
                assert!(rig.current().is_none() && rig.stage().is_none(), "{operation}: withdrawn, no reading is current and the reservation is free");
            }
            rig.none(Duration::from_millis(100));
        }
    }
}
