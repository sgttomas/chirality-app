//! Stop Codex, Restart Codex and the App quit when Codex has stopped reading
//! its input while a turn is live (DEL-01-02 AC-001…AC-006; release target
//! exit criterion 4). One stop limit bounds every interrupt's wait for the
//! interrupt gate and the frame writer and the wait for an interrupt whose
//! own write has begun; the sequence then reaches the step that ends the
//! Codex process. What each stop request records follows what happened:
//! sent, not sent (no write began), or write outcome unknown (a write began
//! and did not complete).
//!
//! The peer is a Python stand-in for Codex started through the Host's own
//! start path. It establishes no supplier behaviour. Expectations here are
//! written from the assignment, not read from the code under test.
use super::*;
use crate::runtime_session::{HomeSession, WorkflowRootSession};
use std::path::PathBuf;
use std::time::Instant;

/// Answers the handshake and `thread/start`, acknowledges an interrupt and
/// completes its turn interrupted. It reads its input without buffering, a
/// chunk at a time; once the file `stop-reading` exists it stops reading
/// for good (writing `stopped-reading`), so the input pipe fills and a write
/// to it blocks. Its process does not end when its input closes.
const PEER: &str = r#"#!/usr/bin/python3
import sys,json,threading,time,os,select
if '--version' in sys.argv:
 print('codex-cli 0.167.0');sys.exit(0)
lock=threading.Lock()
def emit(v):
 with lock: print(json.dumps(v),flush=True)
def events():
 while True:
  try:
   os.rename('queued-event.json','reading-event.json')
   with open('reading-event.json') as f: v=json.load(f)
   os.unlink('reading-event.json');emit(v)
  except FileNotFoundError: pass
  time.sleep(0.002)
threading.Thread(target=events,daemon=True).start()
starts=[0]
def handle(f):
 m=f.get('method')
 with open('wire.jsonl','a') as log: log.write(json.dumps({'method':m})+'\n')
 if m=='initialize': result={'userAgent':'unqualified-stop-fixture'}
 elif m=='thread/start':
  starts[0]+=1
  t={'id':'thread' if starts[0]==1 else 'thread-%d'%starts[0],'cliVersion':'0.167.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'stop fixture','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':'idle'},'turns':[]}
  result={'thread':t,'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
 elif m=='turn/steer': result={'turnId':f['params']['expectedTurnId']}
 elif m=='turn/interrupt':
  emit({'id':f['id'],'result':{}})
  emit({'method':'turn/completed','params':{'threadId':f['params']['threadId'],'turn':{'id':f['params']['turnId'],'status':'interrupted','items':[],'error':None,'itemsView':'summary'}}})
  return
 else: return
 emit({'id':f['id'],'result':result})
buf=b''
while True:
 if os.path.exists('stop-reading'):
  open('stopped-reading','w').close()
  while True: time.sleep(1)
 r,_,_=select.select([0],[],[],0.005)
 if not r: continue
 chunk=os.read(0,65536)
 if not chunk: break
 buf+=chunk
 while b'\n' in buf:
  line,buf=buf.split(b'\n',1)
  handle(json.loads(line))
"#;

/// The stop limit these tests give Stop, Restart and the quit.
const LIMIT: Duration = Duration::from_secs(1);
/// HOSTING §4.5's own waits after the limit: up to 3 s for the process group
/// to empty after the input closes, then the kill and up to 3 s for the end
/// of output; one more second for scheduling.
const ENDING: Duration = Duration::from_secs(7);
/// The reading the assigner gives for a write that began and did not complete.
const SEND_UNKNOWN: &str = "Stop requested; the interrupt's write began and its completion was not observed, so whether it reached Codex is not known.";
/// No text shown for the turn says it was interrupted.
fn assert_no_interrupted(shown: &[Value]) {
    for v in shown {
        assert!(!v.to_string().to_lowercase().contains("interrupted"), "{v}");
    }
}
/// The reason the assigner gives for an interrupt not written in time.
const NOT_READING: &str = "the interrupt could not be written within the stop limit";

/// `_custody`: the root held as the App holds its App data before it opens a
/// ledger, so that a later App session on it models a relaunch.
struct Fixture {
    root: PathBuf,
    cfg: HostConfig,
    home: Arc<HomeSession>,
    generation: Value,
    held: Vec<std::thread::JoinHandle<()>>,
    _custody: crate::AppDataCustody,
}
impl Fixture {
    fn new() -> Self {
        use std::os::unix::fs::PermissionsExt;
        let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("stop-bound-").unwrap());
        for name in ["account", "probe"] {
            std::fs::create_dir_all(root.join(name)).unwrap();
        }
        let _custody = crate::hold_app_data_for_test(&root).unwrap();
        let peer = root.join("peer.py");
        std::fs::write(&peer, PEER).unwrap();
        std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
        let mut cfg = HostConfig::new(peer, root.join("account"), root.join("probe"), root.clone());
        cfg.allow_unverified_dev = true;
        cfg.wait_limit = Duration::from_secs(2);
        let host = Arc::new(Host::new());
        host.configure_recovery(root.join("recovery.ledger.jsonl")).unwrap();
        host.start(&cfg, "stop fixture").unwrap();
        let generation = host.snapshot()["generation"].clone();
        host.thread_start_selected(&root.to_string_lossy(), "fixture-model", "fixture-provider").unwrap();
        let home = Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account, host, Ok(cfg.clone())).unwrap());
        Self { root, cfg, home, generation, held: Vec::new(), _custody }
    }
    fn host(&self) -> &Arc<Host> {
        &self.home.host
    }
    fn ledger(&self) -> PathBuf {
        self.root.join("recovery.ledger.jsonl")
    }
    fn live_turn(&self, thread: &str, id: &str) {
        let tmp = self.root.join("new-event.json");
        let event = json!({"method":"turn/started","params":{"threadId":thread,"turn":{"id":id,"status":"inProgress","items":[],"error":null,"itemsView":"summary"}}});
        std::fs::write(&tmp, serde_json::to_vec(&event).unwrap()).unwrap();
        let deadline = Instant::now() + Duration::from_secs(3);
        while self.root.join("queued-event.json").exists() {
            assert!(Instant::now() < deadline, "previous event not taken");
            std::thread::sleep(Duration::from_millis(2));
        }
        std::fs::rename(tmp, self.root.join("queued-event.json")).unwrap();
        while self.host().conversation_turn(&self.generation, thread, id).is_none() {
            assert!(Instant::now() < deadline, "turn/started not received");
            std::thread::sleep(Duration::from_millis(5));
        }
    }
    /// The stand-in stops reading its input from now on.
    fn stop_reading(&self) {
        std::fs::write(self.root.join("stop-reading"), "").unwrap();
        let deadline = Instant::now() + Duration::from_secs(3);
        while !self.root.join("stopped-reading").exists() {
            assert!(Instant::now() < deadline, "stand-in did not stop reading");
            std::thread::sleep(Duration::from_millis(5));
        }
    }
    /// A steer of 4 MiB through the Host's own request path: Codex is not
    /// reading, so its write fills the pipe and blocks holding the frame
    /// writer, until the Codex process group is ended.
    fn blocked_writer(&mut self, thread: &str, turn: &str) {
        let host = Arc::clone(self.host());
        let (generation, thread, turn) = (self.generation.clone(), thread.to_owned(), turn.to_owned());
        self.held.push(std::thread::spawn(move || {
            let _ = host.turn_steer_text(&generation, &thread, &turn, &"x".repeat(4 << 20));
        }));
        let deadline = Instant::now() + Duration::from_secs(3);
        loop {
            let writing = self.host().inner.0.lock().unwrap().source_requests.values().any(|e| e.request.frame["method"] == "turn/steer" && e.write_attempt_in_progress);
            if writing && self.host().frame_write.try_lock().is_err() {
                break;
            }
            assert!(Instant::now() < deadline, "the steer's write did not begin");
            std::thread::sleep(Duration::from_millis(5));
        }
        // Long enough for the pipe to fill; the write stays in progress.
        std::thread::sleep(Duration::from_millis(200));
        assert!(self.host().frame_write.try_lock().is_err(), "the blocked write holds the frame writer");
    }
    /// Fills Codex's input pipe outside the Host's frame writer, so that the
    /// next frame the Host writes (the interrupt) begins and blocks with the
    /// frame writer free until then. The writer's own copy of the pipe fails
    /// once the Codex process group is ended.
    fn fill_pipe(&mut self) {
        use std::os::fd::AsFd;
        let fd = self.host().stdin.lock().unwrap().as_ref().unwrap().as_fd().try_clone_to_owned().unwrap();
        let mut file = std::fs::File::from(fd);
        let (tx, rx) = channel();
        self.held.push(std::thread::spawn(move || {
            tx.send(()).unwrap();
            let _ = file.write_all(&vec![b' '; 4 << 20]);
        }));
        rx.recv().unwrap();
        std::thread::sleep(Duration::from_millis(300));
        assert!(self.host().frame_write.try_lock().is_ok(), "the frame writer is free; only the pipe is full");
    }
    /// The interrupt gate, the App's recovery writer and the frame writer are
    /// all free again (allowing the ended writes a moment to return).
    fn assert_nothing_held(&self) {
        let deadline = Instant::now() + Duration::from_secs(3);
        loop {
            let host = self.host();
            let free = host.interrupt_gate.try_lock().is_ok() && host.recovery_writer.try_lock().is_ok() && host.frame_write.try_lock().is_ok();
            if free {
                return;
            }
            assert!(Instant::now() < deadline, "a lock is still held: gate {}, recovery writer {}, frame writer {}",
                host.interrupt_gate.try_lock().is_err(), host.recovery_writer.try_lock().is_err(), host.frame_write.try_lock().is_err());
            std::thread::sleep(Duration::from_millis(10));
        }
    }
    /// Start Codex again in this home, as Start Codex does.
    fn start_again(&self) -> Result<Value, String> {
        let _ = std::fs::remove_file(self.root.join("stop-reading"));
        let _ = std::fs::remove_file(self.root.join("stopped-reading"));
        self.host().start(&self.cfg, "the person: Start Codex")
    }
    /// The current Codex process's group (its leader's process id).
    fn group(&self) -> i32 {
        self.host().child.lock().unwrap().as_ref().expect("a Codex process").id() as i32
    }
    /// Codex is stopped and no process of that group is left.
    fn group_ended(&self, group: i32) -> bool {
        self.host().snapshot()["state"] == "stopped" && unsafe { libc::kill(-group, 0) } != 0
    }
    /// This App session's stop-request rows for a turn, as the person is shown them.
    fn rows(host: &Host, turn: &str) -> Vec<Value> {
        host.snapshot()["stopRequests"]["records"].as_array().unwrap().iter().filter(|r| r["turnId"] == turn).cloned().collect()
    }
    /// A later App session on the same ledger: the earlier App's process has
    /// ended (one App at a time on this data), the startup closure of the
    /// earlier session's stop requests runs, then a Host reads the rows.
    fn relaunch(&self) -> (Vec<Value>, Vec<Value>) {
        self.host().end_process_for_test();
        crate::recovery::RecoveryLedger::open(self.ledger()).unwrap();
        let before = crate::recovery::stored_entries(&self.ledger());
        let mut ledger = crate::recovery::RecoveryLedger::open(self.ledger()).unwrap();
        ledger.start_session("relaunch", "candidate").unwrap();
        drop(ledger);
        let after = crate::recovery::stored_entries(&self.ledger());
        let added: Vec<Value> = after[before.len()..].iter().filter(|e| e["kind"] == "stop_request").cloned().collect();
        let relaunched = Host::new();
        relaunched.configure_recovery(self.ledger()).unwrap();
        let rows = relaunched.snapshot()["stopRequests"]["records"].as_array().unwrap().clone();
        (added, rows)
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = self.home.host.stop("stop fixture cleanup", "test ended");
        for held in self.held.drain(..) {
            let _ = held.join();
        }
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

/// Runs Stop or Restart on another thread and waits for it no longer than
/// the stop limit plus the ending step's own waits.
fn stop_within(f: &Fixture, restart: bool) -> (Value, Duration) {
    let (home, generation, cfg) = (Arc::clone(&f.home), f.generation.clone(), f.cfg.clone());
    let root = f.root.clone();
    let (tx, rx) = channel();
    std::thread::spawn(move || {
        let workflows = Mutex::new(WorkflowRootSession::default());
        let begin = Instant::now();
        let host = Arc::clone(&home.host);
        let out = crate::codex_stop::stop_native_home_within(&home, &workflows, &generation, restart, "fixture person", LIMIT, |_| true, move || {
            let _ = std::fs::remove_file(root.join("stop-reading"));
            let _ = std::fs::remove_file(root.join("stopped-reading"));
            host.start(&cfg, "the person: Restart Codex")
        });
        let _ = tx.send((out, begin.elapsed()));
    });
    let start = if restart { Duration::from_secs(3) } else { Duration::ZERO };
    let (out, took) = rx.recv_timeout(LIMIT + ENDING + start).expect("Stop did not reach the ending step within the stop limit and the ending step's own waits");
    eprintln!("stop-bound: {} returned after {took:?}", if restart { "Restart" } else { "Stop" });
    (out.unwrap(), took)
}

fn stop_record_of(out: &Value, turn: &str) -> Value {
    out["turns"].as_array().unwrap().iter().find(|t| t["turnId"] == turn).unwrap()["stopRequest"].clone()
}

/// Codex has stopped reading and another write holds the frame writer.
/// Stop gives up on the interrupt's write at the stop limit, records it not
/// sent with the reason, ends the Codex process, and leaves nothing held;
/// Start then works. The account at once, at the next start in that home and
/// after a relaunch is a stop not sent; never an interrupted turn.
#[test]
fn stop_with_a_blocked_writer_records_not_sent_and_ends_codex() {
    let mut f = Fixture::new();
    f.live_turn("thread", "turn-1");
    f.stop_reading();
    f.blocked_writer("thread", "turn-1");
    let group = f.group();
    let (out, took) = stop_within(&f, false);
    assert!(took >= LIMIT, "the interrupt was waited for up to the limit: {took:?}");
    assert!(took < LIMIT + ENDING, "{took:?}");
    assert_eq!(out["state"], "stopped", "{out}");
    assert!(f.group_ended(group), "the stand-in's process group is ended");
    let turn = &out["turns"][0];
    assert_eq!(turn["interruptRequest"]["state"], "not sent", "{turn}");
    assert_eq!(turn["interruptRequest"]["reading"], NOT_READING);
    assert!(turn["codexReported"].is_null());
    // At once: the stop request as the person is shown it.
    let record = stop_record_of(&out, "turn-1");
    assert_eq!((record["state"].as_str(), record["send"].as_str()), (Some("not-sent"), Some("not-sent(not-ready)")), "{record}");
    assert_eq!(record["reading"], format!("Stop not sent: {NOT_READING}"));
    assert!(record["label"].is_null(), "no outcome label: {record}");
    assert!(turn["label"].is_null(), "no Stop label for an interrupt not sent: {turn}");
    assert_no_interrupted(&[turn["label"].clone(), turn["interruptRequest"].clone(), record.clone()]);
    assert_eq!(f.attempted_interrupts("turn-1"), 0, "not sent: no write began");
    f.assert_nothing_held();
    // The next start in that home: not refused, and the same account.
    f.start_again().unwrap();
    assert_eq!(f.host().snapshot()["state"], "ready");
    let rows = Fixture::rows(f.host(), "turn-1");
    assert_eq!(rows.len(), 1, "{rows:?}");
    assert_eq!((rows[0]["state"].as_str(), rows[0]["reading"].as_str()), (Some("not-sent"), Some(&*format!("Stop not sent: {NOT_READING}"))));
    assert!(rows[0]["label"].is_null());
    assert_no_interrupted(&rows);
    // After quitting and reopening: no closure is written for it, and the
    // earlier session's row reads the same.
    let _ = f.host().stop("fixture", "end of session");
    let (added, rows) = f.relaunch();
    assert!(added.iter().all(|e| e["record"]["turnId"] != "turn-1"), "the startup closure writes nothing for a stop not sent: {added:?}");
    let row = rows.iter().find(|r| r["turnId"] == "turn-1").unwrap();
    assert_eq!((row["earlierSession"].as_bool(), row["state"].as_str(), row["reading"].as_str()), (Some(true), Some("not-sent"), Some(&*format!("Stop not sent: {NOT_READING}"))));
    assert!(row["label"].is_null(), "{row}");
    assert_no_interrupted(&[row.clone()]);
}

/// Restart is Stop followed by a start: the same bounded stop, then Codex
/// started again in that home.
#[test]
fn restart_with_a_blocked_writer_stops_then_starts() {
    let mut f = Fixture::new();
    f.live_turn("thread", "turn-1");
    f.stop_reading();
    f.blocked_writer("thread", "turn-1");
    let (out, took) = stop_within(&f, true);
    assert!(took < LIMIT + ENDING + Duration::from_secs(3), "{took:?}");
    assert_eq!(out["state"], "stopped", "{out}");
    assert_eq!(out["turns"][0]["interruptRequest"]["state"], "not sent");
    assert_eq!(out["turns"][0]["interruptRequest"]["reading"], NOT_READING);
    assert!(out["turns"][0]["label"].is_null());
    assert_eq!(stop_record_of(&out, "turn-1")["reading"], format!("Stop not sent: {NOT_READING}"));
    assert_eq!(f.attempted_interrupts("turn-1"), 0);
    assert_eq!(out["start"]["state"], "started", "{out}");
    let now = f.host().snapshot();
    assert_eq!(now["state"], "ready");
    assert_ne!(now["generation"], f.generation);
    f.assert_nothing_held();
}

/// The menu quit with a blocked writer: the same bounded interrupt, then the
/// quit's settlement ends the Codex process and the session ends *quit*,
/// carrying the stop request as not sent.
#[test]
fn quit_with_a_blocked_writer_records_not_sent_and_settles() {
    let mut f = Fixture::new();
    f.live_turn("thread", "turn-1");
    f.stop_reading();
    f.blocked_writer("thread", "turn-1");
    let group = f.group();
    let home = Arc::clone(&f.home);
    let (tx, rx) = channel();
    std::thread::spawn(move || {
        let workflows = Mutex::new(WorkflowRootSession::default());
        let begin = Instant::now();
        let mut ops = crate::app_quit::HostQuit::new(vec![Arc::clone(&home)], &workflows, "fixture person", |_: &Value| -> Result<bool, String> { Ok(true) });
        let decision = crate::app_quit::quit_sequence(&mut ops, LIMIT);
        drop(ops);
        let app = crate::app_quit::AppQuit::default();
        let allowed = app.allow(&decision, |ids| crate::app_quit::finish_exit(&[Arc::clone(&home)], Some(ids.to_vec())));
        let _ = tx.send((decision, allowed, begin.elapsed()));
    });
    let (decision, allowed, took) = rx.recv_timeout(LIMIT + ENDING).expect("the quit did not reach its settlement within the stop limit and the ending step's own waits");
    eprintln!("stop-bound: quit sequence and settlement returned after {took:?}");
    assert!(took < LIMIT + ENDING, "{took:?}");
    let crate::app_quit::Decision::Quit(out) = decision else { panic!("{decision:?}") };
    assert_eq!(out["turns"][0]["interruptRequest"]["state"], "not sent", "{out}");
    assert_eq!(out["turns"][0]["interruptRequest"]["reading"], NOT_READING);
    assert!(allowed.unwrap(), "the processes were settled, so the quit may proceed");
    assert_eq!(f.attempted_interrupts("turn-1"), 0, "not sent: no write began");
    assert!(f.group_ended(group));
    f.assert_nothing_held();
    let rows = crate::recovery::stored_entries(&f.ledger());
    let ended = rows.iter().find(|e| e["kind"] == "session_ended").unwrap();
    assert_eq!(ended["stopRequests"][0]["state"], "not-sent", "{ended}");
    let (added, rows) = f.relaunch();
    assert!(added.is_empty(), "{added:?}");
    let row = rows.iter().find(|r| r["turnId"] == "turn-1").unwrap();
    assert_eq!((row["cause"].as_str(), row["reading"].as_str()), (Some("quit"), Some(&*format!("Stop not sent: {NOT_READING}"))));
    assert!(row["label"].is_null());
}

/// Codex stops reading with its pipe full while the frame writer is free:
/// Stop's own interrupt write begins and blocks. Stop waits for it only to
/// the stop limit and goes on to end the process; the write then fails. The
/// record says neither sent nor not sent: it stays at its request, noted
/// that the write's outcome is unknown. The account at the three moments
/// is a stop requested whose arrival at Codex is not known; never an
/// interrupted turn.
#[test]
fn stop_whose_own_write_blocks_records_the_write_outcome_unknown() {
    let mut f = Fixture::new();
    f.live_turn("thread", "turn-1");
    f.stop_reading();
    f.fill_pipe();
    let group = f.group();
    let (out, took) = stop_within(&f, false);
    assert!(took < LIMIT + ENDING, "{took:?}");
    assert_eq!(out["state"], "stopped", "{out}");
    assert!(f.group_ended(group));
    let turn = &out["turns"][0];
    assert_eq!(turn["interruptRequest"]["state"], "write outcome unknown", "{turn}");
    assert!(turn["interruptRequest"]["reading"].as_str().unwrap().contains("whether it reached Codex is not known"), "{turn}");
    f.assert_nothing_held();
    assert!(turn["label"].is_null(), "no Stop label for an interrupt not written: {turn}");
    // The interrupt's thread records SR-13 after its write fails.
    let row = f.wait_for_state("turn-1", "send-unknown");
    assert_eq!((row["send"].as_str(), row["response"].as_str(), row["transition"].as_str()), (Some("unknown(write-incomplete)"), Some("unknown-no-response"), Some("SR-13")), "{row}");
    assert_eq!(row["reading"], SEND_UNKNOWN);
    assert_eq!(row["persistence"], "recorded in the App ledger", "no note: the record says it");
    assert_no_interrupted(&[turn["label"].clone(), turn["interruptRequest"].clone(), row.clone()]);
    assert_eq!(f.attempted_interrupts("turn-1"), 1, "SR-13 only where a write began");
    let ledger: Vec<Value> = crate::recovery::stored_entries(&f.ledger()).into_iter().filter(|e| e["kind"] == "stop_request" && e["record"]["turnId"] == "turn-1").collect();
    assert_eq!(ledger.iter().map(|e| e["record"]["transition"].as_str().unwrap()).collect::<Vec<_>>(), ["SR-01", "SR-13"], "no SR-02, SR-03 or SR-08 for it: {ledger:?}");
    // The next start in that home (its generation has closed).
    f.start_again().unwrap();
    assert_eq!(f.host().snapshot()["state"], "ready");
    let rows = Fixture::rows(f.host(), "turn-1");
    assert_eq!(rows.len(), 1);
    assert_eq!((rows[0]["state"].as_str(), rows[0]["reading"].as_str()), (Some("send-unknown"), Some(SEND_UNKNOWN)));
    assert_no_interrupted(&rows);
    // After quitting and reopening.
    let _ = f.host().stop("fixture", "end of session");
    let (added, rows) = f.relaunch();
    assert!(added.iter().all(|e| e["record"]["turnId"] != "turn-1"), "{added:?}");
    let row = rows.iter().find(|r| r["turnId"] == "turn-1").unwrap();
    assert_eq!((row["earlierSession"].as_bool(), row["state"].as_str(), row["reading"].as_str()), (Some(true), Some("send-unknown"), Some(SEND_UNKNOWN)));
    assert_no_interrupted(&[row.clone()]);
}

/// Two live turns; the frame writer is held at first, becomes free in time
/// for the first interrupt, and is held again before the second: the first
/// is written and acknowledged, the second is not sent with the reason, and
/// Stop ends Codex within the limit.
#[test]
fn two_live_turns_with_the_writer_free_in_time_for_one() {
    let f = Fixture::new();
    f.host().thread_start_selected(&f.root.to_string_lossy(), "fixture-model", "fixture-provider").unwrap();
    f.live_turn("thread", "turn-1");
    f.live_turn("thread-2", "turn-2");
    let (release_tx, release_rx) = channel::<()>();
    let release_rx = Arc::new(Mutex::new(release_rx));
    // Held now, free 300 ms later.
    {
        let host = Arc::clone(f.host());
        let (held_tx, held_rx) = channel();
        std::thread::spawn(move || {
            let _serial = host.frame_write.lock().unwrap();
            held_tx.send(()).unwrap();
            std::thread::sleep(Duration::from_millis(300));
        });
        held_rx.recv().unwrap();
    }
    // Taken again right after the first interrupt's send.
    {
        let host = Arc::clone(f.host());
        let release = Arc::clone(&release_rx);
        *f.host().after_interrupt_send.lock().unwrap() = Some(Box::new(move || {
            let (held_tx, held_rx) = channel();
            std::thread::spawn(move || {
                let _serial = host.frame_write.lock().unwrap();
                held_tx.send(()).unwrap();
                let _ = release.lock().unwrap().recv_timeout(Duration::from_secs(20));
            });
            held_rx.recv().unwrap();
        }));
    }
    let (out, took) = stop_within(&f, false);
    let _ = release_tx.send(());
    assert!(took < LIMIT + ENDING, "{took:?}");
    let by = |id: &str| out["turns"].as_array().unwrap().iter().find(|t| t["turnId"] == id).unwrap().clone();
    let (first, second) = (by("turn-1"), by("turn-2"));
    assert_eq!(first["interruptRequest"]["state"], "acknowledged", "{first}");
    assert_eq!(first["codexReported"], "interrupted");
    assert_eq!(second["interruptRequest"]["state"], "not sent", "{second}");
    assert_eq!(second["interruptRequest"]["reading"], NOT_READING);
    assert_eq!(second["stopRequest"]["reading"], format!("Stop not sent: {NOT_READING}"));
    assert_eq!(f.wire_interrupts(), 1);
    assert_eq!(out["state"], "stopped");
    // At once: the written turn keeps today's label; the unsent one has none.
    assert_eq!(first["label"], "interrupted by Stop Codex");
    assert!(second["label"].is_null(), "{second}");
    assert_no_interrupted(&[second["label"].clone(), second["interruptRequest"].clone(), second["stopRequest"].clone()]);
    assert_eq!((f.attempted_interrupts("turn-1"), f.attempted_interrupts("turn-2")), (1, 0));
    f.assert_nothing_held();
    // The next start in that home.
    f.start_again().unwrap();
    let written = f.wait_for_state("turn-1", "settled");
    assert_eq!(written["label"], "interrupted by Stop Codex");
    let unsent = Fixture::rows(f.host(), "turn-2");
    assert_eq!(unsent.len(), 1);
    assert_eq!(unsent[0]["reading"], format!("Stop not sent: {NOT_READING}"));
    assert_no_interrupted(&unsent);
    // After quitting and reopening.
    let _ = f.host().stop("fixture", "end of session");
    let (_, rows) = f.relaunch();
    let row = |turn: &str| rows.iter().find(|r| r["turnId"] == turn).unwrap().clone();
    assert_eq!(row("turn-1")["label"], "interrupted by Stop Codex");
    assert_eq!(row("turn-2")["reading"], format!("Stop not sent: {NOT_READING}"));
    assert_no_interrupted(&[row("turn-2")]);
}

/// The person's own Interrupt is pressed while the stand-in is not reading: it waits
/// for the frame writer without a bound (its present behaviour) and holds the
/// interrupt gate. Stop does not wait on that gate past the stop limit: its
/// interrupt of the same turn is refused by the request's own guard (nothing
/// recorded), and its interrupt of another turn is recorded not sent.
#[test]
fn stop_does_not_wait_past_the_limit_on_a_person_interrupt_holding_the_gate() {
    let mut f = Fixture::new();
    f.host().thread_start_selected(&f.root.to_string_lossy(), "fixture-model", "fixture-provider").unwrap();
    f.live_turn("thread", "turn-1");
    f.live_turn("thread-2", "turn-2");
    f.stop_reading();
    f.blocked_writer("thread", "turn-1");
    {
        let host = Arc::clone(f.host());
        let generation = f.generation.clone();
        f.held.push(std::thread::spawn(move || {
            let _ = host.turn_interrupt(&generation, "thread", "turn-1", "H-acct", &crate::stop_records::person("fixture person"));
        }));
    }
    let deadline = Instant::now() + Duration::from_secs(3);
    while f.host().interrupt_gate.try_lock().is_ok() {
        assert!(Instant::now() < deadline, "the person's interrupt did not take the gate");
        std::thread::sleep(Duration::from_millis(5));
    }
    let (out, took) = stop_within(&f, false);
    assert!(took < LIMIT + ENDING, "{took:?}");
    assert_eq!(out["state"], "stopped");
    let by = |id: &str| out["turns"].as_array().unwrap().iter().find(|t| t["turnId"] == id).unwrap().clone();
    let (same, other) = (by("turn-1"), by("turn-2"));
    assert_eq!(same["interruptRequest"]["state"], "not sent", "{same}");
    assert!(same["stopRequest"].is_null(), "a refusal at the request's guard records nothing: {same}");
    assert_eq!(other["interruptRequest"]["state"], "not sent", "{other}");
    assert!(other["interruptRequest"]["reading"].as_str().unwrap().starts_with(NOT_READING), "{other}");
    // Its thread starts after the deadline, withdrawn from the start; it
    // records SR-01 and SR-03 only if it gets there before the process stop
    // closes the generation. Either way nothing says it was sent.
    assert!(other["stopRequest"].is_null() || other["stopRequest"]["state"] == "not-sent", "{other}");
    assert!(same["label"].is_null() && other["label"].is_null(), "{same} {other}");
    assert_eq!((f.attempted_interrupts("turn-2"), f.attempted_interrupts("turn-1")), (0, 0), "no Stop interrupt was attempted, nor the person's");
    assert_eq!(f.wire_interrupts(), 0);
    f.assert_nothing_held();
    f.start_again().unwrap();
}

impl Fixture {
    /// Interrupt requests to that turn whose write was attempted.
    fn attempted_interrupts(&self, turn: &str) -> usize {
        self.host().inner.0.lock().unwrap().source_requests.values()
            .filter(|e| e.request.frame["method"] == "turn/interrupt" && e.request.frame["params"]["turnId"] == turn && e.attempt_position.is_some()).count()
    }
    /// Waits until the turn's stop-request row has this state.
    fn wait_for_state(&self, turn: &str, state: &str) -> Value {
        let deadline = Instant::now() + Duration::from_secs(3);
        loop {
            let rows = Self::rows(self.host(), turn);
            if let Some(row) = rows.iter().find(|r| r["state"] == state) {
                return row.clone();
            }
            assert!(Instant::now() < deadline, "no {state} row: {rows:?}");
            std::thread::sleep(Duration::from_millis(10));
        }
    }
    fn wire_interrupts(&self) -> usize {
        std::fs::read_to_string(self.root.join("wire.jsonl")).unwrap_or_default().lines().filter(|l| l.contains("turn/interrupt")).count()
    }
}

// ---- The recovery writer held, and the withdraw-or-write decision.

/// Holds the App's recovery writer from inside the interrupt's thread, just
/// before that thread takes it, until `release` is sent.
fn hold_recovery_writer_at_the_interrupt(host: &Arc<Host>) -> Sender<()> {
    let (release_tx, release_rx) = channel::<()>();
    let writer = Arc::clone(&host.recovery_writer);
    *host.before_interrupt_records.lock().unwrap() = Some(Box::new(move || {
        let (held_tx, held_rx) = channel();
        std::thread::spawn(move || {
            let _held = writer.lock().unwrap();
            held_tx.send(()).unwrap();
            let _ = release_rx.recv_timeout(Duration::from_secs(30));
        });
        held_rx.recv().unwrap();
    }));
    release_tx
}

/// The recovery writer (not the frame writer, not the interrupt gate) is held
/// when the interrupt's thread needs it. Stop does not wait for it past the
/// stop limit: the interrupt is not sent and Codex is stopped; once the
/// writer is free the thread writes nothing.
#[test]
fn stop_with_the_recovery_writer_held_does_not_wait_past_its_limit() {
    let f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let release = hold_recovery_writer_at_the_interrupt(f.host());
    let (out, took) = stop_within(&f, false);
    let _ = release.send(());
    assert!(took < LIMIT + Duration::from_secs(2), "Stop waited past its limit: {took:?}");
    assert_eq!(out["state"], "stopped", "{out}");
    let turn = &out["turns"][0];
    assert_eq!((turn["interruptRequest"]["state"].as_str(), turn["interruptRequest"]["reading"].as_str()), (Some("not sent"), Some(NOT_READING)), "{turn}");
    assert!(turn["label"].is_null());
    assert_no_interrupted(&[turn.clone()]);
    f.assert_nothing_held();
    assert_eq!((f.attempted_interrupts("turn-1"), f.wire_interrupts()), (0, 0), "the released thread wrote nothing");
}

/// The same for the menu quit's interrupt phase (`quit_sequence`). The
/// recovery writer is released BEFORE `finish_exit` runs, so this shows that
/// the quit's interrupts do not wait past their limit on a held recovery
/// writer. It does not show a bounded full quit while that writer stays held.
#[test]
fn the_quits_interrupt_phase_does_not_wait_past_its_limit_on_a_held_recovery_writer() {
    let f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let release = hold_recovery_writer_at_the_interrupt(f.host());
    let workflows = Mutex::new(WorkflowRootSession::default());
    let begin = Instant::now();
    let mut ops = crate::app_quit::HostQuit::new(vec![Arc::clone(&f.home)], &workflows, "fixture person", |_: &Value| -> Result<bool, String> { Ok(true) });
    let decision = crate::app_quit::quit_sequence(&mut ops, LIMIT);
    let took = begin.elapsed();
    drop(ops);
    let _ = release.send(());
    assert!(took < LIMIT + Duration::from_secs(1), "the quit's interrupts waited past the limit: {took:?}");
    let crate::app_quit::Decision::Quit(out) = decision else { panic!("{decision:?}") };
    assert_eq!(out["turns"][0]["interruptRequest"]["state"], "not sent", "{out}");
    let app = crate::app_quit::AppQuit::default();
    assert!(app.allow(&crate::app_quit::Decision::Quit(out), |ids| crate::app_quit::finish_exit(&[Arc::clone(&f.home)], Some(ids.to_vec()))).unwrap());
    f.assert_nothing_held();
    assert_eq!(f.wire_interrupts(), 0);
}

/// Forced order 1: the caller withdraws first. The thread is held just
/// before the withdraw-or-write decision until the caller has returned "not
/// sent"; released, it writes nothing and records not sent.
#[test]
fn withdrawal_first_means_the_interrupt_is_never_written() {
    let f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let (at_tx, at_rx) = channel::<()>();
    let (go_tx, go_rx) = channel::<()>();
    *f.host().before_interrupt_decision.lock().unwrap() = Some(Box::new(move || {
        at_tx.send(()).unwrap();
        let _ = go_rx.recv_timeout(Duration::from_secs(30));
    }));
    let (host, generation) = (Arc::clone(f.host()), f.generation.clone());
    let caller = std::thread::spawn(move || host.turn_interrupt_within(&generation, "thread", "turn-1", crate::stop_records::Cause::CodexStop, "H-acct", &crate::stop_records::person("fixture person"), Instant::now() + Duration::from_millis(300)));
    at_rx.recv_timeout(Duration::from_secs(5)).expect("the thread reached the decision");
    let result = caller.join().unwrap();
    let InterruptSend::NotSent(reason) = result else { panic!("withdrawn first: the result is not sent") };
    assert_eq!(reason, NOT_READING);
    go_tx.send(()).unwrap();
    let row = f.wait_for_state("turn-1", "not-sent");
    assert_eq!(row["reading"], format!("Stop not sent: {NOT_READING}"));
    assert_eq!((f.attempted_interrupts("turn-1"), f.wire_interrupts()), (0, 0), "nothing written after not sent was returned");
    f.assert_nothing_held();
}

/// Forced order 2: the thread begins the write first. It is held right after
/// deciding to write, until the caller's deadline has passed; the caller's
/// result is "write outcome unknown", never "not sent". Released, the write
/// completes and the record follows what happened (sent).
#[test]
fn a_begun_write_is_never_reported_not_sent() {
    let f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let (decided_tx, decided_rx) = channel::<()>();
    let (go_tx, go_rx) = channel::<()>();
    *f.host().after_interrupt_decision.lock().unwrap() = Some(Box::new(move || {
        decided_tx.send(()).unwrap();
        let _ = go_rx.recv_timeout(Duration::from_secs(30));
    }));
    let (host, generation) = (Arc::clone(f.host()), f.generation.clone());
    let caller = std::thread::spawn(move || host.turn_interrupt_within(&generation, "thread", "turn-1", crate::stop_records::Cause::CodexStop, "H-acct", &crate::stop_records::person("fixture person"), Instant::now() + Duration::from_millis(300)));
    decided_rx.recv_timeout(Duration::from_secs(5)).expect("the thread decided to write");
    let result = caller.join().unwrap();
    let InterruptSend::WriteUnknown(reason) = result else { panic!("a begun write: the result is write outcome unknown") };
    assert!(reason.contains("its completion was not observed"), "{reason}");
    go_tx.send(()).unwrap();
    let row = f.wait_for_state("turn-1", "settled");
    assert_eq!((row["send"].as_str(), row["codexReported"].as_str()), (Some("sent"), Some("interrupted")), "the write completed after the deadline: recorded sent");
    assert_eq!(f.attempted_interrupts("turn-1"), 1);
    f.assert_nothing_held();
}

/// A write that reaches its admission after the stop limit is withdrawn there,
/// under the phase lock, even when the caller has not yet withdrawn it: it is
/// not sent and nothing is written.
#[test]
fn a_write_reaching_admission_after_the_limit_is_withdrawn_there() {
    let late = WriteBound { deadline: Instant::now() - Duration::from_millis(1), phase: Arc::new(Mutex::new(SendPhase::Pending)), gave_up: Mutex::new(None) };
    assert_eq!(late.begin_write().unwrap_err(), NOT_WRITTEN_IN_LIMIT);
    assert_eq!(*late.phase.lock().unwrap(), SendPhase::Withdrawn);
    assert_eq!(late.gave_up.lock().unwrap().as_deref(), Some(NOT_WRITTEN_IN_LIMIT));
    assert!(late.withdrawn());
    // Before the limit the write may begin, and once begun it stays begun.
    let early = WriteBound { deadline: Instant::now() + LIMIT, phase: Arc::new(Mutex::new(SendPhase::Pending)), gave_up: Mutex::new(None) };
    assert!(early.begin_write().is_ok());
    assert_eq!(*early.phase.lock().unwrap(), SendPhase::Writing);
    // The clock never reclassifies a write that began: past its limit it is
    // still begun, never withdrawn, so the caller reads it as of unknown
    // outcome (or sent, once it completes), never as not sent
    // (`stop_whose_own_write_blocks_records_the_write_outcome_unknown`).
    let begun = WriteBound { deadline: Instant::now() - Duration::from_millis(1), phase: Arc::new(Mutex::new(SendPhase::Writing)), gave_up: Mutex::new(None) };
    assert!(!begun.withdrawn());
    assert_eq!(*begun.phase.lock().unwrap(), SendPhase::Writing);
    assert!(begun.gave_up.lock().unwrap().is_none());
}

/// An interrupt the caller has withdrawn at the limit keeps that reason even
/// when the Codex process is already ending by the time its thread next looks
/// (the ending Stop began after the withdrawal): the record and the turn give
/// one reason.
#[test]
fn a_withdrawn_interrupt_keeps_the_limit_as_its_reason_when_the_process_is_ending() {
    let f = Fixture::new();
    let held = Mutex::new(());
    let _writer = held.lock().unwrap();
    let withdrawn = WriteBound { deadline: Instant::now() + LIMIT, phase: Arc::new(Mutex::new(SendPhase::Withdrawn)), gave_up: Mutex::new(None) };
    // A generation other than the current one: the process is ending for this interrupt.
    let ending = json!("gen:a-generation-that-has-ended");
    let reason = f.host().lock_within(&held, &withdrawn, &ending, NOT_WRITTEN_IN_LIMIT).err();
    assert_eq!(reason.as_deref(), Some(NOT_WRITTEN_IN_LIMIT));
    assert_eq!(withdrawn.gave_up.lock().unwrap().as_deref(), Some(NOT_WRITTEN_IN_LIMIT));
    // Not withdrawn and before the limit, an ending process is the reason.
    let pending = WriteBound { deadline: Instant::now() + LIMIT, phase: Arc::new(Mutex::new(SendPhase::Pending)), gave_up: Mutex::new(None) };
    assert_eq!(f.host().lock_within(&held, &pending, &ending, NOT_WRITTEN_IN_LIMIT).err().as_deref(), Some(PROCESS_ENDING));
}

/// The same through the request itself, with no caller to withdraw: an
/// interrupt whose bound has already passed when it reaches admission is
/// refused there. Nothing is registered as attempted and nothing reaches
/// Codex's input.
#[test]
fn an_interrupt_reaching_admission_after_the_limit_is_not_written() {
    let f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let late = WriteBound { deadline: Instant::now() - Duration::from_millis(1), phase: Arc::new(Mutex::new(SendPhase::Pending)), gave_up: Mutex::new(None) };
    let attempts = |host: &Host| host.inner.0.lock().unwrap().source_requests.values().filter(|e| e.write_attempt_in_progress || e.attempt_position.is_some()).count();
    let (before, wire) = (attempts(f.host()), f.wire_interrupts());
    let refused = f.host().request_begin_with_access_offer_guarded("turn/interrupt", json!({"threadId":"thread","turnId":"turn-1"}), json!({"kind":"person-directed"}), false, Some(&f.generation), false, None, None, None, None, false, None, None, None, None, Some(&late));
    // The request is registered and its write is refused at admission: no
    // attempt is observed and nothing is written.
    let source = refused.expect("the request is registered and its write refused");
    assert_eq!(source.write_attempt_observed(), Some(false));
    assert_eq!(source.evidence()["actualWriteAttemptObserved"], false);
    assert_ne!(source.evidence()["writeResult"], "written");
    assert_eq!(late.gave_up.lock().unwrap().as_deref(), Some(NOT_WRITTEN_IN_LIMIT));
    assert_eq!(*late.phase.lock().unwrap(), SendPhase::Withdrawn);
    assert_eq!(attempts(f.host()), before, "nothing registered as attempted");
    assert_eq!(f.wire_interrupts(), wire, "nothing reached Codex's input");
    assert_eq!(f.attempted_interrupts("turn-1"), 0);
    f.assert_nothing_held();
}

/// A configuration reading and a bounded interrupt are exclusive by
/// construction: a request that names both a reading deadline and an
/// interrupt bound is refused before anything is taken, so nothing is
/// registered, nothing is written and the bound's decision is untouched.
#[test]
fn a_request_with_both_a_reading_deadline_and_an_interrupt_bound_is_refused() {
    let f = Fixture::new();
    f.live_turn("thread", "turn-1");
    for (method, params) in [("turn/interrupt", json!({"threadId":"thread","turnId":"turn-1"})), ("config/read", json!({}))] {
        let limit = WriteBound { deadline: Instant::now() + LIMIT, phase: Arc::new(Mutex::new(SendPhase::Pending)), gave_up: Mutex::new(None) };
        let count = |host: &Host| {
            let i = host.inner.0.lock().unwrap();
            (i.next_id, i.source_requests.len(), i.client_requests.len(), i.pending.len(), i.interrupt_requests.len())
        };
        let before = count(f.host());
        let wire = f.wire_interrupts();
        let refused = f.host().request_begin_with_access_offer_guarded(method, params, json!({"kind":"person-directed"}), false, Some(&f.generation), false, None, None, None, None, false, None, None, None, Some(Instant::now() + LIMIT), Some(&limit));
        assert_eq!(refused.err().as_deref(), Some("a configuration reading is never an interrupt; nothing sent"), "{method}");
        assert_eq!(count(f.host()), before, "{method}: nothing registered");
        assert_eq!(f.wire_interrupts(), wire, "{method}: nothing written");
        assert_eq!(*limit.phase.lock().unwrap(), SendPhase::Pending, "{method}: no write began");
        assert!(limit.gave_up.lock().unwrap().is_none(), "{method}");
    }
    assert_eq!(f.attempted_interrupts("turn-1"), 0);
    f.assert_nothing_held();
}

/// A turn start sent, or being sent, that the App has not yet associated with
/// a turn is live work at the quit, Stop Codex and logout: Codex may be
/// starting a turn the App cannot yet interrupt. Only the reply to its request
/// associates it with a turn. Each of the three callers of the shared
/// assessment counts it beside the turns observed, names it in what the person
/// reads, and goes on only by the person's choice.
mod a_turn_start_not_yet_answered {
    use super::*;
    use crate::app_quit::{quit_sequence, Decision, HostQuit};
    use crate::act_control::native_statement::{codex_stop_statement, logout_statement, quit_statement};

    /// The sentence the person reads at a quit, written here independently of
    /// the code that forms it.
    const QUITTING: &str = "A turn start has been sent, or is being sent, to Codex. The App has not yet associated this start with a turn it can interrupt, so it cannot ask Codex to stop it; it may be one of the turns listed. Quitting stops Codex wherever that turn has got to: it may not have begun, or may have done part of its work, and its outcome may remain unknown. It is not reported as interrupted.";

    /// A turn/start of `text` sent on its own thread through the Host's own
    /// request path (the stand-in never answers it); waits until the Host
    /// lists a new start with the given write state, and returns its request identity.
    fn send_turn_start(f: &mut Fixture, text: String, write: &str) -> Value {
        let before: Vec<Value> = f.host().snapshot()["unansweredTurnStarts"].as_array().unwrap().iter().map(|s| s["requestIdentity"].clone()).collect();
        let host = Arc::clone(f.host());
        let generation = f.generation.clone();
        f.held.push(std::thread::spawn(move || { let _ = host.turn_start_text(&generation, "thread", &text); }));
        let deadline = Instant::now() + Duration::from_secs(3);
        loop {
            if let Some(start) = f.host().snapshot()["unansweredTurnStarts"].as_array().unwrap().iter().find(|s| s["write"] == write && !before.contains(&s["requestIdentity"])) {
                return start["requestIdentity"].clone();
            }
            assert!(Instant::now() < deadline, "the turn start is not listed as {write}: {}", f.host().snapshot()["unansweredTurnStarts"]);
            std::thread::sleep(Duration::from_millis(5));
        }
    }
    /// Codex's frame, emitted by the stand-in (whether or not it reads its input).
    fn emit(f: &Fixture, frame: &Value) {
        let tmp = f.root.join("new-event.json");
        std::fs::write(&tmp, serde_json::to_vec(frame).unwrap()).unwrap();
        let deadline = Instant::now() + Duration::from_secs(3);
        while f.root.join("queued-event.json").exists() {
            assert!(Instant::now() < deadline, "previous event not taken");
            std::thread::sleep(Duration::from_millis(2));
        }
        std::fs::rename(tmp, f.root.join("queued-event.json")).unwrap();
    }
    fn turn(id: &str, status: &str) -> Value {
        json!({"id":id,"status":status,"items":[],"error":null,"itemsView":"summary"})
    }
    fn until(what: &str, done: impl Fn() -> bool) {
        let deadline = Instant::now() + Duration::from_secs(3);
        while !done() {
            assert!(Instant::now() < deadline, "{what}");
            std::thread::sleep(Duration::from_millis(5));
        }
    }
    /// Codex's reply to the turn start, naming its turn; waits until the Host has it.
    fn reply(f: &Fixture, request: &Value, id: &str) {
        emit(f, &json!({"id":request,"result":{"turn":turn(id, "inProgress")}}));
        until("the reply was not received", || f.host().inner.0.lock().unwrap().source_requests.get(&request.to_string()).is_some_and(|e| e.response.is_some()));
    }
    fn completed(f: &Fixture, id: &str) {
        emit(f, &json!({"method":"turn/completed","params":{"threadId":"thread","turn":turn(id, "completed")}}));
        until("turn/completed not received", || f.host().conversation_turn(&f.generation, "thread", id).is_some_and(|t| t["nativeTurn"]["status"] == "completed"));
    }
    fn starts(view: &Value) -> Vec<Value> { view["observedUnansweredTurnStarts"].as_array().cloned().unwrap_or_default() }
    fn live(view: &Value) -> Vec<Value> { view["observedLiveTurns"].as_array().cloned().unwrap_or_default() }
    /// The quit, through its own sequence: what it asked, the person keeping
    /// the App running; None where it asked nothing.
    fn quit_asks(f: &Fixture) -> Option<Value> {
        let workflows = Mutex::new(WorkflowRootSession::default());
        let mut asked = None;
        let mut quit = HostQuit::new(vec![Arc::clone(&f.home)], &workflows, "Invented Person", |view: &Value| { asked = Some(view.clone()); Ok(false) });
        let decision = quit_sequence(&mut quit, LIMIT);
        drop(quit);
        match decision {
            Decision::Cancelled(_) => asked,
            Decision::Quit(done) => { assert_eq!(done["asked"], false, "{done}"); None }
            other => panic!("{other:?}"),
        }
    }
    fn stop_asks(f: &Fixture) -> Value {
        let workflows = Mutex::new(WorkflowRootSession::default());
        crate::codex_stop::assess(&f.home, &workflows, &f.generation, false).unwrap().view().clone()
    }
    fn logout_asks(f: &Fixture) -> Value {
        let mut asked = None;
        let result = crate::runtime_session::logout_native_home(&f.home, None, &f.generation, |view| { asked = Some(view.clone()); false }).unwrap();
        assert_eq!(result["state"], "native confirmation cancelled; no logout request", "{result}");
        asked.unwrap()
    }
    /// At each caller: (turns observed in progress, starts), the quit having
    /// asked. A second turn in progress on one thread is listed as an
    /// unresolved turn observation, which is live work too; both count here.
    fn counts(f: &Fixture) -> Vec<(usize, usize)> {
        let quit = quit_asks(f).expect("the quit asks: work is live");
        [quit, stop_asks(f), logout_asks(f)].iter().map(|v| {
            let unresolved = v["coverage"]["turns"]["unresolved"].as_array().map_or(0, Vec::len);
            (live(v).len() + unresolved, starts(v).len())
        }).collect()
    }
    fn counted(view: &Value, write: &str) {
        let starts = starts(view);
        assert_eq!(starts.len(), 1, "{view}");
        assert_eq!((starts[0]["threadId"].as_str(), starts[0]["write"].as_str()), (Some("thread"), Some(write)), "{view}");
        assert!(live(view).is_empty(), "no turn identity, so not a live turn that can be interrupted: {view}");
    }
    fn named(text: &str, sentence: Option<String>) {
        assert!(text.contains("Turn start not yet associated with a turn: thread (request #"), "{text}");
        assert!(text.contains("It may be one of the turns listed here; the App has not yet associated this start with a turn it can interrupt."), "{text}");
        assert!(text.contains("0 live turns") && text.contains("1 turn starts not yet associated with a turn"), "{text}");
        if let Some(sentence) = sentence { assert!(text.contains(&sentence), "{text}"); }
    }

    #[test]
    fn written_with_no_response_at_each_caller() {
        let mut f = Fixture::new();
        send_turn_start(&mut f, "hello".into(), "written");
        let (quit, stop, logout) = (quit_asks(&f).unwrap(), stop_asks(&f), logout_asks(&f));
        for view in [&quit, &stop, &logout] { counted(view, "written"); }
        named(&quit_statement(&quit).unwrap().text, Some(QUITTING.into()));
        named(&codex_stop_statement(&stop).unwrap().text, Some(QUITTING.replace("Quitting stops", "Stopping Codex stops")));
        named(&logout_statement(&logout).unwrap().text, None);
    }

    #[test]
    fn held_mid_write_at_each_caller() {
        let mut f = Fixture::new();
        f.stop_reading();
        send_turn_start(&mut f, "x".repeat(4 << 20), "in-progress");
        let (quit, stop, logout) = (quit_asks(&f).unwrap(), stop_asks(&f), logout_asks(&f));
        for view in [&quit, &stop, &logout] { counted(view, "in-progress"); }
        named(&quit_statement(&quit).unwrap().text, Some(QUITTING.into()));
    }

    /// Round 1, finding 1: Codex's reply arrives while the start's write is
    /// still being recorded. The Host keeps the reply until the write is
    /// recorded; until then the start is still counted, at every caller.
    #[test]
    fn a_reply_before_the_write_is_recorded_leaves_it_counted() {
        let mut f = Fixture::new();
        f.stop_reading();
        let request = send_turn_start(&mut f, "x".repeat(4 << 20), "in-progress");
        reply(&f, &request, "turn-1");
        assert!(f.host().inner.0.lock().unwrap().source_requests.get(&request.to_string()).unwrap().write_attempt_in_progress, "the write is still in progress");
        assert_eq!(counts(&f), [(0, 1); 3], "counted, never dropped between the reply and the write's record");
    }

    /// The reply arrives while the person is being asked. The start neither
    /// disappears nor is counted again beside the turn it became: the quit
    /// asks again, with that turn as one live turn, now with its identity.
    #[test]
    fn a_reply_arriving_during_the_confirmation() {
        let mut f = Fixture::new();
        let request = send_turn_start(&mut f, "hello".into(), "written");
        let workflows = Mutex::new(WorkflowRootSession::default());
        let mut asked = Vec::new();
        let mut quit = HostQuit::new(vec![Arc::clone(&f.home)], &workflows, "Invented Person", |view: &Value| {
            asked.push(view.clone());
            if asked.len() == 1 { reply(&f, &request, "turn-1"); Ok(true) } else { Ok(false) }
        });
        let decision = quit_sequence(&mut quit, LIMIT);
        drop(quit);
        assert!(matches!(decision, Decision::Cancelled(_)), "{decision:?}");
        assert_eq!(asked.len(), 2, "asked again once the start became a turn: {asked:?}");
        counted(&asked[0], "written");
        assert_eq!(asked[1]["changedWhileAsking"], true);
        assert!(starts(&asked[1]).is_empty(), "not counted a second time: {}", asked[1]);
        let turns = live(&asked[1]);
        assert_eq!((turns.len(), turns[0]["threadId"].as_str(), turns[0]["turnId"].as_str()), (1, Some("thread"), Some("turn-1")), "it did not disappear: {}", asked[1]);
    }

    /// Round 1, finding 2, as the INTERLOCUTOR corrected it: only the reply to
    /// a start's request associates it with a turn. Before the reply, a notice
    /// of a turn on its thread does not; the start is listed beside it. After
    /// the reply the start is that turn, counted once, whichever came first.
    #[test]
    fn only_the_reply_associates_a_start_with_its_turn_whichever_arrives_first() {
        for notice_first in [true, false] {
            let mut f = Fixture::new();
            let request = send_turn_start(&mut f, "hello".into(), "written");
            if notice_first {
                f.live_turn("thread", "turn-1");
                assert_eq!(counts(&f), [(1, 1); 3], "a notice alone associates nothing: the start is listed beside the turn");
                reply(&f, &request, "turn-1");
            } else {
                reply(&f, &request, "turn-1");
                assert_eq!(counts(&f), [(1, 0); 3], "the reply associates the start with its turn");
                f.live_turn("thread", "turn-1");
            }
            assert_eq!(counts(&f), [(1, 0); 3], "notice first: {notice_first}");
            completed(&f, "turn-1");
            assert!(quit_asks(&f).is_none(), "the start does not come back once its turn ended (notice first: {notice_first})");
        }
    }

    /// The notice of an OLDER turn arrives late, after a newer start was sent:
    /// the newer start stays listed until its own reply.
    #[test]
    fn a_late_notice_of_an_older_turn_does_not_take_a_newer_start() {
        let mut f = Fixture::new();
        let request = send_turn_start(&mut f, "newer".into(), "written");
        f.live_turn("thread", "older-turn");
        assert_eq!(counts(&f), [(1, 1); 3]);
        reply(&f, &request, "turn-2");
        assert_eq!(counts(&f), [(2, 0); 3]);
    }

    /// A second start on a thread whose first start's turn is live is counted
    /// as its own start, beside that turn; so is a start beside an older turn.
    #[test]
    fn a_second_start_beside_a_live_turn_is_its_own_start() {
        let mut f = Fixture::new();
        let first = send_turn_start(&mut f, "first".into(), "written");
        reply(&f, &first, "turn-1");
        send_turn_start(&mut f, "second".into(), "written");
        assert_eq!(counts(&f), [(1, 1); 3]);
        let mut f = Fixture::new();
        f.live_turn("thread", "older-turn");
        send_turn_start(&mut f, "newer".into(), "written");
        assert_eq!(counts(&f), [(1, 1); 3]);
    }

    /// An unresolved start makes the quit and Stop Codex ask; it never becomes
    /// a refusal the person's confirmation cannot pass. Confirmed, each goes on.
    #[test]
    fn the_persons_yes_goes_ahead_past_an_unresolved_start() {
        let mut f = Fixture::new();
        send_turn_start(&mut f, "hello".into(), "written");
        let workflows = Mutex::new(WorkflowRootSession::default());
        let mut asked = 0;
        let mut quit = HostQuit::new(vec![Arc::clone(&f.home)], &workflows, "Invented Person", |_: &Value| { asked += 1; Ok(true) });
        let decision = quit_sequence(&mut quit, LIMIT);
        drop(quit);
        assert_eq!(asked, 1, "asked once");
        match decision { Decision::Quit(done) => assert_eq!(done["asked"], true, "{done}"), other => panic!("the confirmed quit goes on: {other:?}") }
        f.host().reopen_to_new_turns(&f.generation);
        let mut asked = 0;
        let stopped = crate::codex_stop::stop_native_home_within(&f.home, &workflows, &f.generation, false, "Invented Person", LIMIT, |_| { asked += 1; true }, || Ok(Value::Null));
        assert_eq!(asked, 1, "asked once");
        assert!(stopped.is_ok(), "the confirmed stop goes on: {stopped:?}");
        assert_eq!(f.host().snapshot()["state"], "stopped");
    }

    /// Round 1, finding 4: once the generation is closed, none of its starts is listed.
    #[test]
    fn a_closed_generation_lists_no_start() {
        let mut f = Fixture::new();
        send_turn_start(&mut f, "hello".into(), "written");
        let _ = f.host().stop("Invented Person", "test");
        assert_eq!(f.host().snapshot()["unansweredTurnStarts"], json!([]));
    }
}
