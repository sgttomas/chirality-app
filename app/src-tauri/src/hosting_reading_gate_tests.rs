//! Configuration readings of one generation are made one at a time (`reading_gate`): stand-in
//! children only (`/bin/cat` echoes what reaches Codex's input; `/bin/sleep` never reads it).
use super::*;
use reading_gate::{ReadingStage, READING_GATE, READING_WITHDRAWN};
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

/// An ordinary admission is not passed over by the App's own readers, and succeeds beside the
/// tick. Two App readers read again and again (the delegation reading in a loop, every request
/// answered at once): the admission's reading always gets its turn within its budget (never the
/// gate sentence); a superseded admission is the accepted window after its reply. Then with the
/// tick at its own pace (one delegation reading per interval) the admissions succeed.
#[test]
fn an_admission_is_not_passed_over_by_the_apps_own_readers() {
    let rig = Rig::new();
    let stop = Arc::new(std::sync::atomic::AtomicBool::new(false));
    std::thread::scope(|scope| {
        // Codex's stand-in: answers every frame at once.
        scope.spawn(|| {
            while !stop.load(std::sync::atomic::Ordering::SeqCst) {
                let Ok(frame) = rig.frames.lock().unwrap().recv_timeout(Duration::from_millis(20)) else { continue };
                let result = match frame["method"].as_str() { Some("config/read") => cfg(), Some("model/list") => json!({"data":[]}), _ => json!({}) };
                rig.answer(&frame, result);
            }
        });
        let readers = Arc::new(std::sync::atomic::AtomicUsize::new(2));
        let paced = Arc::new(std::sync::atomic::AtomicBool::new(false));
        for _ in 0..2 {
            let (host, g, stop, readers, paced) = (rig.host.clone(), rig.g.clone(), stop.clone(), readers.clone(), paced.clone());
            scope.spawn(move || {
                while !stop.load(std::sync::atomic::Ordering::SeqCst) {
                    if paced.load(std::sync::atomic::Ordering::SeqCst) {
                        // One reader stays, at the tick's own pace.
                        if readers.fetch_sub(1, std::sync::atomic::Ordering::SeqCst) > 1 { return; }
                        readers.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                        host.delegation_signals_read_within(&g, "thread", json!({"kind":"app-rule","name":"delegation-availability-read"}), Duration::from_secs(2));
                        std::thread::sleep(crate::host_tick::INTERVAL);
                        continue;
                    }
                    host.delegation_signals_read_within(&g, "thread", json!({"kind":"app-rule","name":"delegation-availability-read"}), Duration::from_secs(2));
                }
            });
        }
        std::thread::sleep(Duration::from_millis(100));
        let mut admitted = 0;
        for attempt in 0..20 {
            match admit(&rig.host, &rig.g, Duration::from_secs(2)) {
                Ok(_) => admitted += 1,
                Err(e) => assert_ne!(e, READING_GATE, "admission {attempt} passed over"),
            }
        }
        assert!(admitted > 0, "admissions get through between the App's readings");
        paced.store(true, std::sync::atomic::Ordering::SeqCst);
        std::thread::sleep(Duration::from_millis(1200));
        let mut succeeded = 0;
        for _ in 0..5 {
            if let Ok(proof) = admit(&rig.host, &rig.g, Duration::from_secs(2)) {
                if rig.host.thread_start_with_access_dispatch(&proof, "guidance").is_ok() { succeeded += 1; }
            }
            std::thread::sleep(Duration::from_millis(150));
        }
        assert!(succeeded >= 4, "beside the tick at its own pace, admissions and their starts succeed: {succeeded} of 5");
        stop.store(true, std::sync::atomic::Ordering::SeqCst);
    });
}

/// The gate's wait expiring: the gate sentence, nothing registered, nothing on Codex's input.
#[test]
fn the_gate_wait_expiring_gives_the_gate_sentence_and_registers_nothing() {
    let rig = Rig::new();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let first = std::thread::spawn(move || read(&host, &g, json!({"cwd":W,"includeLayers":false}), LONG));
    let held = rig.frame();
    let (requests, pending) = (rig.requests(), rig.pending());
    assert_eq!(read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), Duration::from_millis(150)).err().unwrap(), READING_GATE);
    assert_eq!(admit(&rig.host, &rig.g, Duration::from_millis(150)).err().unwrap(), READING_GATE, "an admission passes the sentence on as it is");
    assert_eq!(rig.host.effective_access_settings_read_within(&rig.g, W, "account", Duration::from_millis(150)).err().unwrap(), READING_GATE, "the settings reading too");
    assert_eq!(rig.host.account_requirements_read_until(&rig.g, Instant::now() + Duration::from_millis(150)).err().unwrap(), READING_GATE, "a requirements reading too");
    assert_eq!((rig.requests(), rig.pending()), (requests, pending), "nothing registered, nothing pending");
    rig.none(Duration::from_millis(100));
    rig.answer(&held, cfg());
    first.join().unwrap().unwrap();
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
/// told it was not sent.
#[test]
fn withdrawal_and_write_admission_exclude_each_other_in_both_orders() {
    let rig = Rig::new();
    *rig.host.reading_after_register.lock().unwrap() = Some(Box::new(|_| std::thread::sleep(Duration::from_millis(200))));
    assert_eq!(read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), Duration::from_millis(100)).err().unwrap(), READING_WITHDRAWN);
    assert!(rig.stage().is_none() && rig.current().is_none());
    rig.none(Duration::from_millis(100));
    *rig.host.before_request_write.lock().unwrap() = Some(Box::new(|_| std::thread::sleep(Duration::from_millis(200))));
    let source = read(&rig.host, &rig.g, json!({"cwd":W,"includeLayers":false}), Duration::from_millis(100)).expect("admitted before its deadline: written");
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
    assert_eq!(rig.stage(), Some((Some(second["id"].to_string()), ReadingStage::AwaitingReply)), "the first's cleanup left the successor alone");
    assert_eq!(rig.current(), Some(request_ref(&second["id"], &rig.host)));
    rig.answer(&written_first, cfg());
    assert_eq!(rig.stage(), Some((Some(second["id"].to_string()), ReadingStage::AwaitingReply)), "a duplicate reply releases nothing");
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
    rig.host.on_line(&serde_json::to_vec(&json!({"id":frame["id"],"result":cfg()})).unwrap(), &rig.g);
    assert!(matches!(rig.stage(), Some((Some(_), ReadingStage::AwaitingReply))), "a reply naming the old generation releases nothing");
    rig.host.on_line(&serde_json::to_vec(&json!({"id":frame["id"],"result":cfg()})).unwrap(), &next);
    fresh.join().unwrap().unwrap();
    assert!(rig.stage().is_none());
}

/// A real blocked pipe write (a stand-in that never reads, its pipe filled by the reading's own
/// large frame): the reading stays outstanding, later readings get the gate sentence, and the
/// blocked one is never told it was not sent; a write error after the attempt leaves the reading
/// outstanding as well.
#[test]
fn a_blocked_or_failed_write_keeps_its_reading_outstanding_and_is_never_called_not_sent() {
    let rig = Rig::new();
    let mut sleeper = Command::new("/bin/sleep").arg("30").env_clear().stdin(Stdio::piped()).stdout(Stdio::null()).stderr(Stdio::null()).spawn().unwrap();
    *rig.host.stdin.lock().unwrap() = sleeper.stdin.take();
    let (host, g) = (rig.host.clone(), rig.g.clone());
    let blocked = std::thread::spawn(move || read(&host, &g, json!({"cwd":"x".repeat(4 * 1024 * 1024),"includeLayers":false}), Duration::from_millis(300)));
    let deadline = Instant::now() + LONG;
    while !matches!(rig.stage(), Some((Some(_), ReadingStage::WriteStarted))) { assert!(Instant::now() < deadline); std::thread::sleep(Duration::from_millis(5)); }
    std::thread::sleep(Duration::from_millis(400));
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
