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

// ---- The App quit with the recovery writer held: nothing waits without a bound.

/// The quit wait limit, HOSTING §4.5's waits for one home's process, and the
/// recording wait, as the assignment states them.
const PER_HOME_ENDING: Duration = Duration::from_millis(6200);
const SLACK: Duration = Duration::from_secs(2);

impl Fixture {
    /// An approval request from Codex, outstanding in this home.
    fn outstanding_approval(&self, id: u64, thread: &str, turn: &str) {
        let frame = json!({"id":id,"method":"item/commandExecution/requestApproval","params":{"threadId":thread,"turnId":turn,"itemId":"item"}});
        self.host().on_line(&serde_json::to_vec(&frame).unwrap(), &self.generation);
        let outstanding = self.host().snapshot()["serverRequests"].as_array().unwrap().iter().any(|r| r["requestIdentity"] == id && r["state"] == "outstanding");
        assert!(outstanding, "{}", self.host().snapshot()["serverRequests"]);
    }
    /// A test thread takes the App's recovery writer now and holds it until
    /// the returned sender is used or dropped.
    fn hold_recovery_writer(&mut self) -> Sender<()> {
        let writer = Arc::clone(&self.host().recovery_writer);
        let (held_tx, held_rx) = channel();
        let (release_tx, release_rx) = channel::<()>();
        self.held.push(std::thread::spawn(move || {
            let _held = writer.lock().unwrap();
            held_tx.send(()).unwrap();
            let _ = release_rx.recv();
        }));
        held_rx.recv().unwrap();
        release_tx
    }
    /// Takes the recovery writer from the settlement of the quit (after the
    /// quit's question and answer were recorded) and holds it until the
    /// returned sender is used or dropped.
    fn hold_recovery_writer_from_settlement(&self) -> Sender<()> {
        let writer = Arc::clone(&self.host().recovery_writer);
        let (release_tx, release_rx) = channel::<()>();
        *self.host().before_quit_stop.lock().unwrap() = Some(Box::new(move || {
            let (held_tx, held_rx) = channel();
            std::thread::spawn(move || {
                let _held = writer.lock().unwrap();
                held_tx.send(()).unwrap();
                let _ = release_rx.recv();
            });
            held_rx.recv().unwrap();
        }));
        release_tx
    }
    /// After the writer is released, the session end the quit's recording
    /// thread was still waiting to write is observed written (or refused), so
    /// that nothing of this App session is still writing when the fixture is
    /// removed.
    fn await_late_session_end(&self) {
        let deadline = Instant::now() + Duration::from_secs(10);
        loop {
            let observed = self.host().runtime_custody.lock().unwrap().as_ref().map(|c| c.snapshot()["sessionEndObservation"].clone()).unwrap_or(Value::Null);
            if !observed.is_null() {
                return;
            }
            assert!(Instant::now() < deadline, "the late session end was not observed");
            std::thread::sleep(Duration::from_millis(10));
        }
    }
    /// The next start on this ledger while this App session's process is
    /// modelled ended (its liveness lock released, as the kernel releases it)
    /// without taking anything this session still holds: the new session's
    /// start entry and the custody view it reads.
    fn next_start(&self) -> (Value, Value, Vec<Value>) {
        self.host().release_session_lock_for_test();
        let mut ledger = crate::recovery::RecoveryLedger::open(self.ledger()).unwrap();
        ledger.start_session("next-start", "candidate").unwrap();
        let entries = ledger.recorded_entries().as_array().unwrap().clone();
        let start = entries.iter().rev().find(|e| e["kind"] == "session_started").unwrap().clone();
        let view = crate::recovery::RecoveryCustodyView::from_owner("next-start", Some(ledger.current_entries()), json!({}), 0, None).snapshot();
        (start, view, entries)
    }
}

/// Runs the person's quit (the question answered Quit) and its exit
/// settlement on another thread, and waits for it no longer than `bound`.
fn person_quit_within(f: &Fixture, wait_limit: Duration, bound: Duration) -> (crate::app_quit::Decision, Result<Value, String>, Duration) {
    let home = Arc::clone(&f.home);
    let (tx, rx) = channel();
    std::thread::spawn(move || {
        let workflows = Mutex::new(WorkflowRootSession::default());
        let begin = Instant::now();
        let mut ops = crate::app_quit::HostQuit::new(vec![Arc::clone(&home)], &workflows, "fixture person", |_: &Value| -> Result<bool, String> { Ok(true) });
        let decision = crate::app_quit::quit_sequence(&mut ops, wait_limit);
        drop(ops);
        let app = crate::app_quit::AppQuit::default();
        let mut observed = Err("not settled".to_owned());
        let _ = app.allow(&decision, |ids| {
            observed = crate::app_quit::finish_exit(&[Arc::clone(&home)], Some(ids.to_vec()));
            observed.clone()
        });
        let _ = tx.send((decision, observed, begin.elapsed()));
    });
    rx.recv_timeout(bound).unwrap_or_else(|_| panic!("the quit did not complete within {bound:?}"))
}

/// The ledger kinds of the quit, in ledger order.
fn quit_kinds(rows: &[Value]) -> Vec<String> {
    rows.iter().filter_map(|e| match e["kind"].as_str().unwrap() {
        "quit_requested" => Some("quit_requested".to_owned()),
        "quit_answered" => Some(format!("quit_answered {}", e["answer"].as_str().unwrap())),
        "stop_request" => Some(format!("stop_request {} {}", e["record"]["transition"].as_str().unwrap(), e["record"]["cause"].as_str().unwrap())),
        "session_ended" => Some(format!("session_ended {}", e["how"].as_str().unwrap())),
        _ => None,
    }).collect()
}

/// (3) An outstanding approval does not refuse the quit: it is listed in the
/// question, nothing answers it, and it ends unanswered with the process.
#[test]
fn an_outstanding_approval_does_not_refuse_the_quit_and_ends_unanswered() {
    let f = Fixture::new();
    f.outstanding_approval(41, "thread", "turn-1");
    let group = f.group();
    let home = Arc::clone(&f.home);
    let workflows = Mutex::new(WorkflowRootSession::default());
    let mut shown = Vec::new();
    let mut ops = crate::app_quit::HostQuit::new(vec![Arc::clone(&home)], &workflows, "fixture person", |view: &Value| -> Result<bool, String> { shown.push(view.clone()); Ok(true) });
    let decision = crate::app_quit::quit_sequence(&mut ops, LIMIT);
    drop(ops);
    assert_eq!(shown.len(), 1, "asked once");
    assert_eq!(shown[0]["observedOutstandingRequests"][0]["requestIdentity"], 41, "{}", shown[0]);
    let crate::app_quit::Decision::Quit(out) = &decision else { panic!("{decision:?}") };
    assert_eq!(out["outstandingRequests"], "Not answered by the App; they end unanswered with the Codex processes (U-10).");
    let app = crate::app_quit::AppQuit::default();
    assert!(app.allow(&decision, |ids| crate::app_quit::finish_exit(&[Arc::clone(&home)], Some(ids.to_vec()))).unwrap());
    assert!(f.group_ended(group));
    let wire = std::fs::read_to_string(f.root.join("wire.jsonl")).unwrap_or_default();
    assert!(wire.lines().all(|l| l != r#"{"method": null}"#), "nothing was written in answer: {wire}");
    let request = f.host().snapshot()["serverRequests"].as_array().unwrap().iter().find(|r| r["requestIdentity"] == 41).cloned().unwrap();
    assert_ne!(request["state"], "outstanding", "{request}");
    assert_eq!(request["replyWriteResult"], "not-attempted", "{request}");
    let ended: Vec<Value> = crate::recovery::stored_entries(&f.ledger()).into_iter().filter(|e| e["kind"] == "register_entry_summary" && e["requestIdentity"] == "41" && e["state"] == "closed").collect();
    assert_eq!(ended.len(), 1, "{ended:?}");
    assert_eq!(ended[0]["endedAs"], "ended-unanswered(process-exit)", "{}", ended[0]);
}

/// (4) The recovery writer held by a test thread for the whole quit: the
/// question and answer are queued, not waited for; the interrupts wait their
/// limit; every home's processes are settled; the recording waits its bound
/// and the quit proceeds, reporting the session end as not confirmed.
#[test]
fn a_quit_with_the_recovery_writer_held_throughout_settles_and_proceeds_within_its_bounds() {
    let mut f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let group = f.group();
    let release = f.hold_recovery_writer();
    let bound = crate::app_quit::QUIT_WAIT_LIMIT + PER_HOME_ENDING + Duration::from_secs(10) + SLACK;
    let (decision, observed, took) = person_quit_within(&f, crate::app_quit::QUIT_WAIT_LIMIT, bound);
    eprintln!("stop-bound: quit with the writer held returned after {took:?}");
    let crate::app_quit::Decision::Quit(out) = decision else { panic!("{decision:?}") };
    assert_eq!(out["records"][0]["state"], "not yet recorded", "{out}");
    assert_eq!(out["turns"][0]["interruptRequest"]["state"], "not sent", "{out}");
    assert!(f.group_ended(group), "every home's processes are settled");
    let observed = observed.expect("the quit proceeds");
    assert_eq!(observed["write"], "not-confirmed", "{observed}");
    assert!(!observed.to_string().contains("not recorded") && !observed.to_string().contains("not written"), "{observed}");
    // The person's quit shows this notice, with OK only, before it exits.
    assert_eq!(crate::app_quit::RECORDING_WAIT_LIMIT, Duration::from_secs(10));
    assert_eq!(crate::app_quit::RECORDING_NOT_CONFIRMED, "Chirality is quitting. The App's own processes for every Codex home have ended. Recording the end of this session was not confirmed within 10 seconds, so the record may or may not have been written; the next start reads it as it finds it.");
    assert_eq!(crate::app_quit::recording_notice(&observed), Some(crate::app_quit::RECORDING_NOT_CONFIRMED));
    assert!(!crate::recovery::stored_entries(&f.ledger()).iter().any(|e| e["kind"] == "session_ended"));
    let _ = release.send(());
    f.await_late_session_end();
}

/// (6) The session end not committed: the next start applies Decision A to
/// the earlier session, its open request takes open-at-App-session-end, and
/// the next-start notice says the quit was confirmed and no end was found.
#[test]
fn a_confirmed_quit_whose_end_was_not_written_is_read_by_decision_a_with_the_notice() {
    let f = Fixture::new();
    f.outstanding_approval(42, "thread", "turn-1");
    // A live turn: its interrupt writes the queued question and answer before
    // it is sent, so the confirmed quit is in the ledger before settlement.
    f.live_turn("thread", "turn-1");
    let release = f.hold_recovery_writer_from_settlement();
    let bound = LIMIT + PER_HOME_ENDING + Duration::from_secs(10) + SLACK;
    let (_, observed, _) = person_quit_within(&f, LIMIT, bound);
    assert_eq!(observed.unwrap()["write"], "not-confirmed");
    let (start, view, entries) = f.next_start();
    assert!(entries.iter().any(|e| e["kind"] == "quit_answered" && e["answer"] == "confirmed"), "the confirmed quit is in the ledger");
    assert!(!entries.iter().any(|e| e["kind"] == "session_ended"));
    assert_eq!(start["previousSessionEnd"], "ended-without-record", "{start}");
    let endings: Vec<&Value> = entries.iter().filter(|e| e["kind"] == "register_entry_summary" && e["requestIdentity"] == "42" && e["state"] == "closed").collect();
    assert_eq!(endings.len(), 1, "{endings:?}");
    assert_eq!((endings[0]["endedAs"].as_str(), endings[0]["transition"].as_str()), (Some(crate::recovery::OPEN_AT_APP_SESSION_END), Some("RQ-06")));
    assert_eq!(view["requestEndEvents"][0]["kind"], "request_open_at_app_session_end", "{view}");
    assert_eq!(view["priorSessionNotice"], "The previous session's quit was confirmed, but no record of that session's end was found. Requests it left open are shown as open at that session's end; whether they were answered is not known.");
    assert!(!view.to_string().to_lowercase().contains("crash"), "{view}");
    let _ = release.send(());
    f.await_late_session_end();
}

/// (6) No quit entry at all for the earlier session (none was drained): the
/// existing reading for a session whose end is not established, and no
/// next-start notice.
#[test]
fn an_earlier_session_with_no_quit_entry_keeps_the_not_established_reading_and_no_notice() {
    let mut f = Fixture::new();
    f.outstanding_approval(43, "thread", "turn-1");
    let release = f.hold_recovery_writer();
    let bound = LIMIT + PER_HOME_ENDING + Duration::from_secs(10) + SLACK;
    let (_, observed, _) = person_quit_within(&f, LIMIT, bound);
    assert_eq!(observed.unwrap()["write"], "not-confirmed");
    let (start, view, entries) = f.next_start();
    assert!(!entries.iter().any(|e| e["kind"] == "quit_requested" || e["kind"] == "quit_answered"), "no quit entry was written");
    assert_eq!(start["previousSessionEnd"], "ended-without-record", "{start}");
    assert!(view["priorSessionNotice"].is_null(), "{view}");
    assert!(!view.to_string().to_lowercase().contains("crash"), "{view}");
    let _ = release.send(());
    f.await_late_session_end();
}

/// (7) With the writer free and one home, the ledger order of the quit is as
/// before: the question, the answer, the stop rows, then the session end. The
/// order is this home's queue order; across homes no order is claimed.
#[test]
fn with_the_writer_free_the_quits_ledger_order_is_unchanged() {
    let f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let (_, observed, _) = person_quit_within(&f, LIMIT, LIMIT + PER_HOME_ENDING + SLACK);
    let observed = observed.unwrap();
    assert_eq!(observed["write"], "confirmed");
    assert_eq!(crate::app_quit::recording_notice(&observed), None, "the confirmed write shows no notice");
    let kinds = quit_kinds(&crate::recovery::stored_entries(&f.ledger()));
    assert_eq!(kinds, ["quit_requested", "quit_answered confirmed", "stop_request SR-01 quit", "stop_request SR-02 quit", "stop_request SR-04 quit", "stop_request SR-06 quit", "session_ended quit"], "{kinds:?}");
}

/// (8) Custody not yet cached and the writer held: the exit settlement fences
/// and settles at once, before any wait on the writer.
#[test]
fn uncached_custody_with_the_writer_held_does_not_delay_fencing_or_settlement() {
    let mut f = Fixture::new();
    assert!(f.host().runtime_custody.lock().unwrap().is_none(), "custody not cached");
    let group = f.group();
    let (settling_tx, settling_rx) = channel();
    *f.host().before_quit_stop.lock().unwrap() = Some(Box::new(move || { let _ = settling_tx.send(Instant::now()); }));
    let release = f.hold_recovery_writer();
    let home = Arc::clone(&f.home);
    let (tx, rx) = channel();
    let begin = Instant::now();
    std::thread::spawn(move || { let _ = tx.send(crate::app_quit::finish_exit(&[home], Some(vec![]))); });
    let settling = settling_rx.recv_timeout(Duration::from_secs(1)).expect("settlement began without waiting on the writer");
    assert!(settling - begin < Duration::from_secs(1));
    let observed = rx.recv_timeout(PER_HOME_ENDING + Duration::from_secs(10) + SLACK).expect("bounded").unwrap();
    assert!(f.group_ended(group));
    assert_eq!(observed["write"], "not-confirmed", "{observed}");
    let _ = release.send(());
    f.await_late_session_end();
}

/// (9) The system's exit (no person asked to quit) with the writer held: its
/// early session-end write waits only its bound, then every home is fenced and
/// settled; no notice is shown; the next start carries it.
#[test]
fn the_system_exit_with_the_writer_held_completes_within_its_bound_without_a_notice() {
    let mut f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let group = f.group();
    let release = f.hold_recovery_writer();
    let home = Arc::clone(&f.home);
    let (tx, rx) = channel();
    let begin = Instant::now();
    std::thread::spawn(move || { let _ = tx.send(crate::app_quit::finish_exit(&[home], None)); });
    let observed = rx.recv_timeout(Duration::from_secs(10) + PER_HOME_ENDING + SLACK).expect("the system exit completed within its bound");
    eprintln!("stop-bound: system exit with the writer held returned after {:?}", begin.elapsed());
    let observed = observed.unwrap();
    assert_eq!(observed["write"], "not-confirmed", "{observed}");
    assert!(observed["notice"].is_null(), "no waiting notice on the system path: {observed}");
    assert!(f.group_ended(group));
    let (start, view, _) = f.next_start();
    assert_eq!(start["previousSessionEnd"], "ended-without-record");
    assert!(view["priorSessionNotice"].is_null());
    let _ = release.send(());
    f.await_late_session_end();
}

/// (5) The session end committed but its report not observed within the
/// bound: the quit says it was not confirmed; the next start reads the ledger,
/// finds the end and honours it, with no unrecorded-session ending and no
/// next-start notice.
#[test]
fn a_session_end_committed_but_not_observed_in_time_is_found_and_honoured_at_the_next_start() {
    let f = Fixture::new();
    f.outstanding_approval(44, "thread", "turn-1");
    let (written_tx, written_rx) = channel::<()>();
    let (report_tx, report_rx) = channel::<()>();
    *f.host().after_quit_recording.lock().unwrap() = Some(Box::new(move || {
        let _ = written_tx.send(());
        let _ = report_rx.recv();
    }));
    let bound = LIMIT + PER_HOME_ENDING + crate::app_quit::RECORDING_WAIT_LIMIT + SLACK;
    let (_, observed, took) = person_quit_within(&f, LIMIT, bound);
    let observed = observed.expect("the quit proceeds");
    assert!(took >= crate::app_quit::RECORDING_WAIT_LIMIT, "{took:?}");
    assert_eq!(observed["write"], "not-confirmed", "{observed}");
    assert_eq!(crate::app_quit::recording_notice(&observed), Some(crate::app_quit::RECORDING_NOT_CONFIRMED));
    written_rx.recv_timeout(Duration::from_secs(1)).expect("the write returned before the report was held");
    let (start, view, entries) = f.next_start();
    assert_eq!(entries.iter().filter(|e| e["kind"] == "session_ended" && e["how"] == "quit").count(), 1, "the committed end is in the ledger");
    assert_eq!(start["previousSessionEnd"], "quit-with-live-work", "the end is honoured: {start}");
    assert!(!entries.iter().any(|e| e["kind"] == "register_entry_summary" && e["transition"] == "RQ-06"), "no unrecorded-session ending");
    assert_eq!(view["requestEndEvents"], json!([]), "{view}");
    assert!(view["priorSessionNotice"].is_null(), "{view}");
    let _ = report_tx.send(());
}

// ---- Quit and a key operation holding the App's key setup.

/// Quit's admission past the key setup, against this fixture's home, with
/// the offer answered `answer`; returns the admission, whether the offer was
/// shown (and with what words), and how long the admission took.
fn admit_key(f: &Fixture, key: &Mutex<()>, hold: &Mutex<Option<crate::app_quit::KeyHold>>, answer: Result<bool, String>) -> (String, Option<String>, Duration) {
    let mut shown = None;
    let begin = Instant::now();
    let admission = crate::app_quit::admit_key_setup(key, hold, &[Arc::clone(&f.home)], |text| { shown = Some(text.to_owned()); answer.clone() }, crate::app_quit::KEY_RELEASE_WAIT_LIMIT);
    let took = begin.elapsed();
    let outcome = match admission {
        crate::app_quit::KeyAdmission::Admitted(_) => "admitted".to_owned(),
        crate::app_quit::KeyAdmission::Refused(reason) => format!("refused: {reason}"),
        crate::app_quit::KeyAdmission::KeptRunning => "kept running".to_owned(),
        crate::app_quit::KeyAdmission::NotAsked(reason) => format!("not asked: {reason}"),
    };
    (outcome, shown, took)
}
/// A key operation on another thread: it holds the key setup, publishes
/// `published`, and lets go only once this fixture's Codex is observed
/// stopped (the Codex it waits on has ended), or never when `lets_go` is
/// false (until the returned sender is used or dropped).
fn key_operation(f: &Fixture, key: &Arc<Mutex<()>>, hold: &Arc<Mutex<Option<crate::app_quit::KeyHold>>>, published: Option<crate::app_quit::KeyHold>, lets_go: bool) -> (Sender<()>, std::thread::JoinHandle<bool>) {
    let (key, hold, host) = (Arc::clone(key), Arc::clone(hold), Arc::clone(f.host()));
    let (held_tx, held_rx) = channel();
    let (end_tx, end_rx) = channel::<()>();
    let operation = std::thread::spawn(move || {
        let _setup = key.lock().unwrap();
        *hold.lock().unwrap() = published;
        held_tx.send(()).unwrap();
        loop {
            if lets_go && host.snapshot()["state"] == "stopped" {
                *hold.lock().unwrap() = None;
                return true;
            }
            match end_rx.recv_timeout(Duration::from_millis(5)) {
                Err(std::sync::mpsc::RecvTimeoutError::Timeout) => {}
                _ => { *hold.lock().unwrap() = None; return false; }
            }
        }
    });
    held_rx.recv().unwrap();
    (end_tx, operation)
}
fn quit_entries(f: &Fixture) -> usize {
    crate::recovery::stored_entries(&f.ledger()).iter().filter(|e| matches!(e["kind"].as_str(), Some("quit_requested" | "quit_answered" | "session_ended"))).count()
}

/// (1) A key operation holds the key setup and has published nothing, or that
/// it is asking the person: Quit is refused with today's words at once;
/// nothing is asked, recorded or stopped.
#[test]
fn a_held_key_setup_that_published_nothing_or_asks_the_person_refuses_with_todays_words() {
    let f = Fixture::new();
    let (key, hold) = (Arc::new(Mutex::new(())), Arc::new(Mutex::new(None)));
    for published in [None, Some(crate::app_quit::KeyHold::Asking)] {
        let (end, operation) = key_operation(&f, &key, &hold, published, false);
        let (outcome, shown, took) = admit_key(&f, &key, &hold, Ok(true));
        assert_eq!(outcome, "refused: An explicit key operation is under way. The App is still running; choose Quit again when that operation has finished.");
        assert_eq!(crate::app_quit::KEY_OPERATION_UNDER_WAY, "An explicit key operation is under way. The App is still running; choose Quit again when that operation has finished.");
        assert!(shown.is_none(), "nothing asked");
        assert!(took < Duration::from_millis(500), "{took:?}");
        assert_eq!(f.host().snapshot()["state"], "ready", "nothing stopped");
        assert_eq!(quit_entries(&f), 0, "nothing recorded");
        end.send(()).unwrap();
        assert!(!operation.join().unwrap());
    }
    // Free: the quit takes it.
    let (outcome, shown, _) = admit_key(&f, &key, &hold, Ok(true));
    assert_eq!((outcome.as_str(), shown), ("admitted", None));
}

/// (2) A key operation waiting on a home's Codex: the offer names it. Keep
/// running changes nothing. Quit anyway stops that home's Codex first; the
/// operation lets go within the bound and the quit settles.
#[test]
fn a_key_operation_waiting_on_a_homes_codex_is_offered_and_ended_as_part_of_quitting() {
    use crate::app_quit::KeyHold;
    use crate::home_resources::HomeClass;
    assert_eq!(crate::app_quit::key_wait_offer(HomeClass::LocalProvider), "A local model settings change is waiting for Codex for the local model home. Quit anyway: Codex for that home is stopped first, and the settings are not changed.");
    assert_eq!(crate::app_quit::key_still_held(HomeClass::LocalProvider), "A key operation for the local model home still holds the App's key setup 10 seconds after Codex for that home was stopped. The App is still running.");
    let f = Fixture::new();
    let group = f.group();
    let (key, hold) = (Arc::new(Mutex::new(())), Arc::new(Mutex::new(None)));
    let (end, operation) = key_operation(&f, &key, &hold, Some(KeyHold::WaitingOnCodex(HomeClass::Account)), true);
    // Declined: nothing.
    let (outcome, shown, _) = admit_key(&f, &key, &hold, Ok(false));
    assert_eq!(outcome, "kept running");
    assert_eq!(shown.as_deref(), Some("An account settings change is waiting for Codex for the account home. Quit anyway: Codex for that home is stopped first, and the settings are not changed."));
    assert_eq!(f.host().snapshot()["state"], "ready", "nothing stopped");
    assert!(key.try_lock().is_err(), "the operation still holds the key setup");
    assert_eq!(quit_entries(&f), 0, "nothing recorded");
    // Accepted: that home's Codex is stopped first, then the operation lets go.
    let (tx, rx) = channel();
    {
        let (key, hold, home) = (Arc::clone(&key), Arc::clone(&hold), Arc::clone(&f.home));
        std::thread::spawn(move || {
            let begin = Instant::now();
            let admission = crate::app_quit::admit_key_setup(&key, &hold, &[Arc::clone(&home)], |_| Ok(true), crate::app_quit::KEY_RELEASE_WAIT_LIMIT);
            let admitted = matches!(admission, crate::app_quit::KeyAdmission::Admitted(_));
            let took = begin.elapsed();
            // The quit continues holding the key setup, and settles.
            let workflows = Mutex::new(WorkflowRootSession::default());
            let mut ops = crate::app_quit::HostQuit::new(vec![Arc::clone(&home)], &workflows, "fixture person", |_: &Value| -> Result<bool, String> { Ok(true) });
            let decision = crate::app_quit::quit_sequence(&mut ops, LIMIT);
            drop(ops);
            let allowed = crate::app_quit::AppQuit::default().allow(&decision, |ids| crate::app_quit::finish_exit(&[Arc::clone(&home)], Some(ids.to_vec())));
            drop(admission);
            let _ = tx.send((admitted, took, allowed));
        });
    }
    let (admitted, took, allowed) = rx.recv_timeout(PER_HOME_ENDING + crate::app_quit::KEY_RELEASE_WAIT_LIMIT + PER_HOME_ENDING + crate::app_quit::RECORDING_WAIT_LIMIT + SLACK).expect("bounded");
    assert!(operation.join().unwrap(), "the operation let go after it observed its Codex stopped");
    drop(end);
    assert!(admitted, "the key setup was released within the bound");
    assert!(took < PER_HOME_ENDING + SLACK, "{took:?}");
    assert!(f.group_ended(group));
    let stop = f.host().lifecycle_events().into_iter().find(|e| e["transitionId"] == "LT-17").expect("Codex for that home was stopped");
    assert_eq!((stop["actor"].as_str(), stop["stopRecord"]["reason"].as_str()), (Some("the person"), Some(crate::app_quit::QUIT_STOP_REASON)));
    assert!(allowed.unwrap(), "the quit settles");
    assert_eq!(quit_entries(&f), 2, "the quit's own records only: its request and the session end");
}

/// (2) The same, and the operation does not let go: Quit anyway stops that
/// home's Codex, waits the bound, then refuses, naming it.
#[test]
fn a_key_operation_that_does_not_let_go_after_its_codex_is_stopped_refuses_the_quit_at_the_bound() {
    use crate::app_quit::KeyHold;
    use crate::home_resources::HomeClass;
    let f = Fixture::new();
    let group = f.group();
    let (key, hold) = (Arc::new(Mutex::new(())), Arc::new(Mutex::new(None)));
    let (end, operation) = key_operation(&f, &key, &hold, Some(KeyHold::WaitingOnCodex(HomeClass::Account)), false);
    let (outcome, shown, took) = admit_key(&f, &key, &hold, Ok(true));
    assert!(shown.is_some());
    assert_eq!(outcome, "refused: A key operation for the account home still holds the App's key setup 10 seconds after Codex for that home was stopped. The App is still running.");
    assert!(!outcome.contains("retry") && !outcome.contains("again"), "no claim about retrying");
    assert!(took >= crate::app_quit::KEY_RELEASE_WAIT_LIMIT && took < crate::app_quit::KEY_RELEASE_WAIT_LIMIT + PER_HOME_ENDING + SLACK, "{took:?}");
    assert!(f.group_ended(group), "Codex for that home was stopped first");
    assert_eq!(quit_entries(&f), 0, "nothing recorded");
    end.send(()).unwrap();
    assert!(!operation.join().unwrap());
}

/// A session-end recording that fails before any write (here: no App-owned
/// account home) still gives the person's quit its notice, with the host's own
/// reason, and says the end was not recorded: nothing was written.
#[test]
fn a_session_end_failure_before_the_bound_gives_the_persons_quit_the_notice_with_the_hosts_reason() {
    // No App-owned account home: the recording thread returns the host's own
    // failure at once, well before the bound.
    let home = Arc::new(HomeSession::new(crate::home_resources::HomeClass::ApiKey, Arc::new(Host::new()), Err("no supplier (fixture)".into())).unwrap());
    let begin = Instant::now();
    let observation = crate::app_quit::finish_exit(&[Arc::clone(&home)], Some(Vec::new())).unwrap();
    assert!(begin.elapsed() < crate::app_quit::RECORDING_WAIT_LIMIT, "a failure returned before the bound is not waited out");
    assert_eq!(observation["write"], "not-confirmed", "{observation}");
    let reason = observation["limit"].as_str().unwrap().to_owned();
    assert_eq!(reason, "no App-owned account home");
    assert_eq!(crate::app_quit::recording_notice(&observation), Some("Chirality is quitting. The App's own processes for every Codex home have ended. The end of this session was not recorded (no App-owned account home); the next start reads the ledger as it finds it."));
    // The system path shows no notice, whatever the write did.
    let system = crate::app_quit::finish_exit(&[home], None);
    assert!(system.as_ref().map(|o| o.get("notice").is_none()).unwrap_or(true), "{system:?}");
}

// ---- Round 1 of the bounded quit: nothing drains on the quit's thread, every
// unconfirmed result is told, and every wait the quit takes has its bound.

impl Fixture {
    /// A test thread takes the App ledger itself (not the recovery writer) and
    /// holds it until the returned sender is used or dropped: an append in
    /// progress, or a stalled sync, as any drain would meet it.
    fn hold_ledger(&mut self) -> Sender<()> {
        let ledger = self.host().inner.0.lock().unwrap().recovery.clone().unwrap();
        let (held_tx, held_rx) = channel();
        let (release_tx, release_rx) = channel::<()>();
        self.held.push(std::thread::spawn(move || {
            let _held = ledger.lock().unwrap();
            held_tx.send(()).unwrap();
            let _ = release_rx.recv();
        }));
        held_rx.recv().unwrap();
        release_tx
    }
}

/// F1 (the reader's reproduction): with the recovery writer free and the
/// ledger held, recording the quit's question and answer returns at once:
/// both are queued, neither is written on the quit's thread.
#[test]
fn the_quits_question_and_answer_wait_on_no_ledger_even_with_the_writer_free() {
    let mut f = Fixture::new();
    let release = f.hold_ledger();
    assert!(f.host().recovery_writer.try_lock().is_ok(), "the writer is free");
    let host = Arc::clone(f.host());
    let (tx, rx) = channel();
    std::thread::spawn(move || {
        let actor = crate::stop_records::person("fixture person");
        let _ = tx.send((host.record_quit_requested(&actor, &json!({})), host.record_quit_answered(&actor, true)));
    });
    let (requested, answered) = rx.recv_timeout(Duration::from_millis(300)).expect("returned without waiting on the ledger");
    for record in [&requested, &answered] {
        assert_eq!(record["state"], "not yet recorded", "{record}");
    }
    let _ = release.send(());
}

/// F1: the ledger held through the whole of a person's quit with a live turn.
/// The question and answer are queued, the interrupt waits its limit, the
/// settlement's stop and the reader's end of output drain nothing (the home is
/// fenced), the processes end, and only the recording thread waits, for its
/// bound. Released, that thread writes the queued facts and then the end.
#[test]
fn a_held_ledger_delays_no_part_of_the_quit_but_its_bounded_recording() {
    let mut f = Fixture::new();
    f.live_turn("thread", "turn-1");
    let group = f.group();
    let release = f.hold_ledger();
    let bound = LIMIT + PER_HOME_ENDING + crate::app_quit::RECORDING_WAIT_LIMIT + SLACK;
    let (decision, observed, took) = person_quit_within(&f, LIMIT, bound);
    eprintln!("stop-bound: quit with the ledger held returned after {took:?}");
    let crate::app_quit::Decision::Quit(out) = decision else { panic!("{decision:?}") };
    assert_eq!(out["records"][0]["state"], "not yet recorded", "{out}");
    assert!(f.group_ended(group), "every home's processes are settled");
    assert!(f.host().drains_deferred_to_quit(), "from the fence on, the quit's recording drains");
    let observed = observed.expect("the quit proceeds");
    assert_eq!(observed["write"], "not-confirmed", "{observed}");
    assert_eq!(crate::app_quit::recording_notice(&observed), Some(crate::app_quit::RECORDING_NOT_CONFIRMED));
    let _ = release.send(());
    f.await_late_session_end();
    let kinds = quit_kinds(&crate::recovery::stored_entries(&f.ledger()));
    assert_eq!(kinds.first().map(String::as_str), Some("quit_requested"), "{kinds:?}");
    assert_eq!(kinds.last().map(String::as_str), Some("session_ended quit"), "the queued facts are written before the end: {kinds:?}");
}

/// F1: the quit's own stop of a home (the key offer's) with the ledger held
/// ends that home's Codex within the stop's own waits and leaves its facts
/// queued; Stop Codex outside the quit is unchanged.
#[test]
fn the_quits_own_stop_ends_codex_without_waiting_on_the_ledger() {
    let mut f = Fixture::new();
    let group = f.group();
    let release = f.hold_ledger();
    let host = Arc::clone(f.host());
    let (tx, rx) = channel();
    std::thread::spawn(move || { let _ = tx.send(host.stop_for_quit("the person", crate::app_quit::QUIT_STOP_REASON, Instant::now() + Duration::from_secs(10))); });
    let stopped = rx.recv_timeout(PER_HOME_ENDING + SLACK).expect("the stop did not wait on the ledger");
    assert_eq!(stopped.unwrap()["state"], "stopped");
    assert!(f.group_ended(group));
    let _ = release.send(());
}

/// F2: every session-end result other than the confirmed write gives the
/// person's quit a notice with the host's own reason; the system path shows
/// none. Unknown: the ledger refused the append.
#[test]
fn an_unknown_session_end_write_gives_the_persons_quit_the_notice_with_the_hosts_reason() {
    let f = Fixture::new();
    let db = rusqlite::Connection::open(crate::recovery::store::database_path(&f.ledger())).unwrap();
    db.execute_batch("CREATE TRIGGER fixture_refuse_end BEFORE INSERT ON ledger_entry WHEN NEW.kind='session_ended' BEGIN SELECT RAISE(ABORT, 'fixture session end refused'); END;").unwrap();
    let observed = crate::app_quit::finish_exit(&[Arc::clone(&f.home)], Some(vec![])).unwrap();
    assert_eq!(observed["write"], "unknown", "{observed}");
    let reason = observed["limit"].as_str().unwrap();
    assert!(reason.contains("fixture session end refused"), "the host's own reason: {reason}");
    assert_eq!(crate::app_quit::recording_notice(&observed), Some(format!("Chirality is quitting. The App's own processes for every Codex home have ended. Recording the end of this session was not confirmed ({reason}), so the record may or may not have been written; the next start reads it as it finds it.").as_str()));
}

/// F2: not attempted (the account home has no ledger): the notice says the end
/// was not recorded, with the host's own reason; the system path shows none.
#[test]
fn a_session_end_not_attempted_gives_the_persons_quit_the_not_recorded_notice() {
    let account = || Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account, Arc::new(Host::new()), Err("no supplier (fixture)".into())).unwrap());
    let observed = crate::app_quit::finish_exit(&[account()], Some(vec![])).unwrap();
    assert_eq!(observed["write"], "not-attempted", "{observed}");
    assert_eq!(observed["limit"], "ledger unavailable; App end observed in memory only");
    assert_eq!(crate::app_quit::recording_notice(&observed), Some("Chirality is quitting. The App's own processes for every Codex home have ended. The end of this session was not recorded (ledger unavailable; App end observed in memory only); the next start reads the ledger as it finds it."));
    let system = crate::app_quit::finish_exit(&[account()], None).unwrap();
    assert_eq!(system["write"], "not-attempted");
    assert!(system.get("notice").is_none(), "{system}");
}

/// F3: a home whose observation another App activity holds (as the tick
/// holds it while it waits on file I/O) is not read past the assessment's
/// bound; the question shows it as not read, and it counts as live work.
#[test]
fn a_held_home_observation_is_shown_as_not_read_within_the_assessment_bound() {
    let f = Fixture::new();
    let home = Arc::clone(&f.home);
    let (held_tx, held_rx) = channel();
    let (release_tx, release_rx) = channel::<()>();
    let holder = std::thread::spawn(move || {
        let _held = home.runtime.lock().unwrap();
        held_tx.send(()).unwrap();
        let _ = release_rx.recv();
    });
    held_rx.recv().unwrap();
    let workflows = Mutex::new(WorkflowRootSession::default());
    let mut shown = Vec::new();
    let begin = Instant::now();
    let mut ops = crate::app_quit::HostQuit::new(vec![Arc::clone(&f.home)], &workflows, "fixture person", |view: &Value| -> Result<bool, String> { shown.push(view.clone()); Ok(false) });
    let decision = crate::app_quit::quit_sequence(&mut ops, LIMIT);
    let took = begin.elapsed();
    drop(ops);
    let _ = release_tx.send(());
    holder.join().unwrap();
    assert!(matches!(decision, crate::app_quit::Decision::Cancelled(_)), "{decision:?}");
    assert!(took >= crate::app_quit::QUIT_ASSESSMENT_WAIT_LIMIT && took < crate::app_quit::QUIT_ASSESSMENT_WAIT_LIMIT + SLACK, "{took:?}");
    assert_eq!(shown.len(), 1, "asked: what could not be read is possibly live");
    assert_eq!(shown[0]["assessmentLimits"], json!(["account home: live work could not be read within 5 seconds"]), "{}", shown[0]);
    assert_eq!(crate::app_quit::live_work_not_read(crate::home_resources::HomeClass::Account), "account home: live work could not be read within 5 seconds");
}

/// F3: the App's workflow runs held past the bound are shown as not read.
#[test]
fn held_workflow_runs_are_shown_as_not_read_within_the_assessment_bound() {
    let f = Fixture::new();
    let workflows = Arc::new(Mutex::new(WorkflowRootSession::default()));
    let (held_tx, held_rx) = channel();
    let (release_tx, release_rx) = channel::<()>();
    let held = Arc::clone(&workflows);
    let holder = std::thread::spawn(move || {
        let _held = held.lock().unwrap();
        held_tx.send(()).unwrap();
        let _ = release_rx.recv();
    });
    held_rx.recv().unwrap();
    let begin = Instant::now();
    let (_, runs, limits) = crate::app_quit::assess_homes(&[Arc::clone(&f.home)], &workflows, Instant::now() + crate::app_quit::QUIT_ASSESSMENT_WAIT_LIMIT);
    let took = begin.elapsed();
    let _ = release_tx.send(());
    holder.join().unwrap();
    assert!(took < crate::app_quit::QUIT_ASSESSMENT_WAIT_LIMIT + SLACK, "{took:?}");
    assert!(runs.is_empty());
    assert_eq!(limits, vec![json!("Workflow runs could not be read within 5 seconds")]);
}

/// F3: an App activity holding a home's source gate past the fencing bound:
/// the person's quit is refused with the sentence, nothing is fenced, settled
/// or recorded, and the App keeps running. The sentence says what this quit
/// had done (round 2's R2-5): no start is established, and interrupts it had
/// already asked for are not withdrawn.
#[test]
fn a_start_holding_the_source_gate_past_the_bound_refuses_the_persons_quit() {
    use crate::home_resources::HomeClass;
    use crate::app_quit::Asked;
    let none = Asked::default();
    assert_eq!(crate::app_quit::gate_not_free(HomeClass::Account, none), "The quit's 10-second fencing interval ended before the request gate of Codex for the account home was free, so this quit stopped there: it stopped no Codex process and recorded no end of this session. The App is still running.");
    // Counted from the stop records: sent, write outcome unknown, not sent.
    let records = vec![json!({"stopRequestId":"a","state":"requested"}), json!({"stopRequestId":"a","state":"sent"}),
        json!({"stopRequestId":"b","state":"send-unknown"}), json!({"stopRequestId":"c","state":"not-sent"}), json!({"stopRequestId":"d","state":"outcome-unknown"})];
    let asked = Asked::of(&["a".into(), "b".into(), "c".into(), "d".into()], &records);
    assert_eq!(asked, Asked { sent: 2, unknown: 1 }, "a not-sent request is not counted as asked");
    assert_eq!(crate::app_quit::gate_not_free(HomeClass::Account, asked), "This quit had already sent Codex 2 interrupt requests for running turns; they are not withdrawn. Whether 1 more interrupt request was sent is not known. The quit's 10-second fencing interval ended before the request gate of Codex for the account home was free, so this quit stopped there: it stopped no Codex process and recorded no end of this session. The App is still running.");
    assert_eq!(crate::app_quit::settlement_unavailable(Asked { sent: 1, unknown: 0 }, &[HomeClass::Account], &["key: failed".into()]), "This quit had already sent Codex 1 interrupt request for a running turn; it is not withdrawn. It stopped Codex for the account home. The App is still running: owned supplier settlement is unavailable (key: failed). No quit session-end record was written. Supervision is retained; inspect Host diagnostics before retrying Quit.");
    for words in [crate::app_quit::gate_not_free(HomeClass::Account, asked), crate::app_quit::settlement_unavailable(none, &[], &["x".into()])] {
        for claim in ["did not begin", "start is under way", "Nothing was interrupted", "for 10 seconds"] {
            assert!(!words.contains(claim), "{words}");
        }
    }
    let f = Fixture::new();
    let group = f.group();
    let host = Arc::clone(f.host());
    let (held_tx, held_rx) = channel();
    let (release_tx, release_rx) = channel::<()>();
    let holder = std::thread::spawn(move || {
        let _gate = host.attachment_gate.lock().unwrap();
        held_tx.send(()).unwrap();
        let _ = release_rx.recv();
    });
    held_rx.recv().unwrap();
    let begin = Instant::now();
    let refused = crate::app_quit::finish_exit(&[Arc::clone(&f.home)], Some(vec![]));
    let took = begin.elapsed();
    let _ = release_tx.send(());
    holder.join().unwrap();
    assert_eq!(refused.unwrap_err(), crate::app_quit::gate_not_free(HomeClass::Account, crate::app_quit::Asked::default()));
    assert!(took >= crate::app_quit::QUIT_FENCE_WAIT_LIMIT && took < crate::app_quit::QUIT_FENCE_WAIT_LIMIT + SLACK, "{took:?}");
    assert!(!f.host().quit_fence.load(std::sync::atomic::Ordering::SeqCst) && !f.host().drains_deferred_to_quit(), "nothing stays fenced");
    assert!(!f.group_ended(group), "nothing was stopped");
    assert_eq!(f.host().snapshot()["state"], "ready");
    assert!(!crate::recovery::stored_entries(&f.ledger()).iter().any(|e| e["kind"] == "session_ended"), "nothing recorded");
}

/// F6: the key operation finishes while the person reads the offer. Their
/// answer applied to what the offer named, which no longer holds: the hold is
/// read again, the key setup is free, and the quit takes it without stopping
/// anything.
#[test]
fn a_key_operation_that_finishes_while_the_offer_is_open_is_not_stopped() {
    use crate::app_quit::KeyHold;
    use crate::home_resources::HomeClass;
    let f = Fixture::new();
    let (key, hold) = (Arc::new(Mutex::new(())), Arc::new(Mutex::new(None)));
    let (end, operation) = key_operation(&f, &key, &hold, Some(KeyHold::WaitingOnCodex(HomeClass::Account)), false);
    let mut finishing = Some((end, operation));
    let mut offers = 0;
    let admission = crate::app_quit::admit_key_setup(&key, &hold, &[Arc::clone(&f.home)], |_| {
        offers += 1;
        if let Some((end, operation)) = finishing.take() {
            end.send(()).unwrap();
            assert!(!operation.join().unwrap());
        }
        Ok(true)
    }, crate::app_quit::KEY_RELEASE_WAIT_LIMIT);
    assert!(matches!(admission, crate::app_quit::KeyAdmission::Admitted(_)), "{admission:?}");
    assert_eq!(offers, 1);
    assert_eq!(f.host().snapshot()["state"], "ready", "nothing stopped");
}

/// F6: the operation turns to asking the person while the offer is open: read
/// again, the quit is refused with today's words and nothing is stopped.
#[test]
fn a_key_hold_that_changes_while_the_offer_is_open_is_assessed_again() {
    use crate::app_quit::KeyHold;
    use crate::home_resources::HomeClass;
    let f = Fixture::new();
    let (key, hold) = (Arc::new(Mutex::new(())), Arc::new(Mutex::new(None)));
    let (end, operation) = key_operation(&f, &key, &hold, Some(KeyHold::WaitingOnCodex(HomeClass::Account)), false);
    let changed = Arc::clone(&hold);
    let admission = crate::app_quit::admit_key_setup(&key, &hold, &[Arc::clone(&f.home)], |_| {
        *changed.lock().unwrap() = Some(KeyHold::Asking);
        Ok(true)
    }, crate::app_quit::KEY_RELEASE_WAIT_LIMIT);
    let crate::app_quit::KeyAdmission::Refused(reason) = admission else { panic!("{admission:?}") };
    assert_eq!(reason, crate::app_quit::KEY_OPERATION_UNDER_WAY);
    assert_eq!(f.host().snapshot()["state"], "ready", "nothing stopped");
    end.send(()).unwrap();
    assert!(!operation.join().unwrap());
}

/// The bounded acquisition every quit-side lock uses: a mutex held past the
/// deadline is not had, and the wait ends at the deadline.
#[test]
fn a_lock_held_past_its_deadline_is_not_waited_for() {
    let mutex = Arc::new(Mutex::new(()));
    let (held_tx, held_rx) = channel();
    let (release_tx, release_rx) = channel::<()>();
    let held = Arc::clone(&mutex);
    let holder = std::thread::spawn(move || {
        let _held = held.lock().unwrap();
        held_tx.send(()).unwrap();
        let _ = release_rx.recv();
    });
    held_rx.recv().unwrap();
    let begin = Instant::now();
    assert!(crate::util::lock_by(&mutex, Instant::now() + Duration::from_millis(200)).is_none());
    let took = begin.elapsed();
    assert!(took >= Duration::from_millis(200) && took < Duration::from_millis(700), "{took:?}");
    let _ = release_tx.send(());
    holder.join().unwrap();
    assert!(crate::util::lock_by(&mutex, Instant::now()).is_some(), "free, it is had at once");
}

/// Round 2 (the reader's reproduction): the quit's acknowledgment wait for a
/// written interrupt Codex never acknowledges ends at its limit without
/// waiting on the ledger, even with the recovery writer free; its SR-10 stays
/// queued for the quit's bounded recording. Stop Codex's own wait is unchanged.
#[test]
fn the_quits_acknowledgment_wait_ends_at_its_limit_without_waiting_on_the_ledger() {
    use crate::codex_stop::Interrupts;
    let mut f = Fixture::new();
    f.live_turn("thread", "turn-ack");
    f.stop_reading();
    let sent = f.host().turn_interrupt_within(&f.generation, "thread", "turn-ack", crate::stop_records::Cause::Quit, "account", &crate::stop_records::person("fixture person"), Instant::now() + Duration::from_secs(2));
    let InterruptSend::Written(source) = sent else { panic!("the interrupt was written") };
    let release = f.hold_ledger();
    assert!(f.host().recovery_writer.try_lock().is_ok(), "the writer is free");
    let home = Arc::clone(&f.home);
    let host = Arc::clone(f.host());
    let (tx, rx) = channel();
    std::thread::spawn(move || {
        let workflows = Mutex::new(WorkflowRootSession::default());
        let mut ops = crate::app_quit::HostQuit::new(vec![home], &workflows, "fixture person", |_: &Value| -> Result<bool, String> { Ok(true) });
        let _ = tx.send(ops.acknowledgment(&(host, source), Duration::from_millis(30)));
    });
    let outcome = rx.recv_timeout(Duration::from_millis(300)).expect("the acknowledgment wait ended at its limit, not after the ledger");
    assert!(outcome.is_err(), "Codex never acknowledged: {outcome:?}");
    let _ = release.send(());
}

/// Round 2's R2-1, the quit's side: a home whose Host state is held (by any
/// activity) does not hold the assessment past its deadline. The home's state
/// is read on its reader thread, the home is shown as not read, and the
/// assessment returns.
#[test]
fn a_home_whose_state_is_held_does_not_hold_the_quit_assessment_past_its_deadline() {
    let f = Fixture::new();
    let workflows = Mutex::new(WorkflowRootSession::default());
    let (held_tx, held_rx) = channel();
    let (release_tx, release_rx) = channel::<()>();
    let host = Arc::clone(f.host());
    let holder = std::thread::spawn(move || {
        let _held = host.inner.0.lock().unwrap();
        held_tx.send(()).unwrap();
        let _ = release_rx.recv();
    });
    held_rx.recv().unwrap();
    let begin = Instant::now();
    let (rows, runs, limits) = crate::app_quit::assess_homes(&[Arc::clone(&f.home)], &workflows, Instant::now() + Duration::from_millis(300));
    let took = begin.elapsed();
    let _ = release_tx.send(());
    holder.join().unwrap();
    assert!(took < Duration::from_millis(300) + SLACK, "{took:?}");
    assert!(rows.is_empty() && runs.is_empty(), "nothing is said of the home's state: {rows:?}");
    assert_eq!(limits, vec![json!(crate::app_quit::live_work_not_read(crate::home_resources::HomeClass::Account))]);
}

/// The exit's delegation ending (P28): the exit waits for its worker at most
/// until the deadline, whatever the worker does; a writer that never returns
/// does not hold the exit, and each outcome has its log line.
#[test]
fn the_exits_delegation_ending_never_holds_the_exit_past_its_deadline() {
    let by = Instant::now() + Duration::from_millis(300);
    let (_never, blocked) = channel::<()>();
    let begin = Instant::now();
    let logged = crate::app_quit::end_delegation_within(by, move |_| { let _ = blocked.recv(); true });
    assert!(begin.elapsed() < Duration::from_millis(300) + SLACK, "{:?}", begin.elapsed());
    assert_eq!(logged.as_deref(), Some("ending this session's delegation observations did not finish within 5 seconds; what it had not written is left as a crash leaves it"));
    let given = Arc::new(Mutex::new(None));
    let seen = Arc::clone(&given);
    assert_eq!(crate::app_quit::end_delegation_within(by + Duration::from_secs(5), move |deadline| { *seen.lock().unwrap() = Some(deadline); true }), None, "ended: nothing logged");
    assert_eq!(*given.lock().unwrap(), Some(by + Duration::from_secs(5)), "the worker takes the links by the exit's own deadline");
    assert_eq!(crate::app_quit::end_delegation_within(Instant::now() + Duration::from_secs(5), |_| false).as_deref(),
        Some("delegation observation not ended: the App's conversation links were held by another App activity for 5 seconds"));
}

/// The system path's lock-order inversion: a successor start used to read the
/// session end with the Host state held, while the session-end write holds its
/// observation and then takes the Host state. The check now reads the session
/// end before taking the Host state (one order), so the two cannot wait on each
/// other: here the write holds the observation and then takes the Host state,
/// and the check, run meanwhile, waits for the write and then sees the end.
#[test]
fn a_successor_check_and_the_session_end_write_take_their_locks_in_one_order() {
    let f = Fixture::new();
    let host = Arc::clone(f.host());
    let custody = host.app_runtime_custody().unwrap();
    let cfg = f.home.host_config.as_ref().unwrap().clone();
    assert!(host.successor_prospective_held(&cfg).1.is_ok(), "nothing ended: the prospective generation");
    let (held_tx, held_rx) = channel();
    let (writer_host, writer_custody) = (Arc::clone(&host), Arc::clone(&custody));
    let writer = std::thread::spawn(move || {
        let mut observed = writer_custody.end_observation.lock().unwrap();
        held_tx.send(()).unwrap();
        std::thread::sleep(Duration::from_millis(200));
        // As the session-end write's drain does: the home's Host state, with the observation held.
        drop(writer_host.inner.0.lock().unwrap());
        *observed = Some(json!({"ended":"invented"}));
    });
    held_rx.recv().unwrap();
    let (done_tx, done_rx) = channel();
    let checker = Arc::clone(&host);
    std::thread::spawn(move || { let refused = checker.successor_prospective_held(&cfg).1; let _ = done_tx.send(refused); });
    let Ok(refused) = done_rx.recv_timeout(Duration::from_secs(5)) else {
        // Deadlocked: the fixture's own teardown would wait on the same locks.
        std::mem::forget(f);
        panic!("the check and the write wait on each other");
    };
    writer.join().unwrap();
    assert_eq!(refused.unwrap_err(), "App session ended; successor start refused");
}

/// P26a: a refusal releases what the quit held before its notice, which waits
/// for the person: while the notice is shown, the Stop/Restart gate and the
/// key setup are free.
#[test]
fn a_quit_refusal_releases_its_holds_before_its_notice() {
    let (gate, key_setup) = (Mutex::new(()), Mutex::new(()));
    let free_while_shown = std::cell::Cell::new(false);
    crate::app_quit::refuse_after_releasing((gate.lock().unwrap(), key_setup.lock().unwrap()), || {
        free_while_shown.set(gate.try_lock().is_ok() && key_setup.try_lock().is_ok());
    });
    assert!(free_while_shown.get(), "the notice is shown with nothing the quit held still held");
}

/// P21 and R3-4: settlement takes each home's request gate within the quit's
/// bound. A holder that is not a start (any App request to that Codex) and
/// that never lets go refuses the settlement at the bound, before anything of
/// that home is ended: its process group is still there (asked of the
/// operating system), the Host still reads it as running, and no stop was
/// recorded for it.
#[test]
fn settlement_does_not_wait_past_its_bound_on_a_held_request_gate() {
    let f = Fixture::new();
    let group = f.group();
    let host = Arc::clone(f.host());
    host.begin_quit_by(Instant::now() + Duration::from_secs(1)).unwrap();
    let (held_tx, held_rx) = channel();
    let (release_tx, release_rx) = channel::<()>();
    let holder = Arc::clone(&host);
    let holding = std::thread::spawn(move || {
        let _gate = holder.attachment_gate.lock().unwrap();
        held_tx.send(()).unwrap();
        let _ = release_rx.recv();
    });
    held_rx.recv().unwrap();
    let begin = Instant::now();
    let settled = host.settle_for_quit("the person", "quit");
    let took = begin.elapsed();
    let alive = unsafe { libc::kill(-group, 0) } == 0;
    let state = host.snapshot()["state"].clone();
    let _ = release_tx.send(());
    holding.join().unwrap();
    assert!(took >= crate::app_quit::QUIT_FENCE_WAIT_LIMIT && took < crate::app_quit::QUIT_FENCE_WAIT_LIMIT + SLACK, "{took:?}");
    let error = settled.unwrap_err();
    assert!(error.contains(crate::hosting::QUIT_GATE_NOT_FREE), "{error}");
    assert!(alive, "the home's process group was not ended");
    assert_eq!(state, "ready", "the Host still reads the home as running, and that is true");
    assert!(!host.journal().iter().any(|e| e["class"] == "codex-stop" || e["observation"]["ownedProcesses"].as_array().is_some_and(|p| !p.is_empty())), "no stop and no process settlement");
    host.cancel_quit();
}

/// R3-1: a value released off its thread is never dropped on the caller,
/// whether its thread cannot start or cannot receive it; released normally,
/// it is dropped on its own thread.
#[test]
fn a_release_off_thread_never_drops_on_the_caller() {
    use crate::util::{release_off_thread, Released};
    struct Watched(Arc<Mutex<Option<std::thread::ThreadId>>>);
    impl Drop for Watched { fn drop(&mut self) { *self.0.lock().unwrap() = Some(std::thread::current().id()); } }
    let caller = std::thread::current().id();
    let by = Instant::now() + Duration::from_secs(5);
    // The thread cannot start: the release is dropped unrun, and the value leaked.
    let dropped = Arc::new(Mutex::new(None));
    let value = Watched(Arc::clone(&dropped));
    assert_eq!(release_off_thread(|release| { drop(release); Err(std::io::Error::other("no thread")) }, || Some(value), by), Released::NotStarted);
    assert_eq!(*dropped.lock().unwrap(), None, "not dropped on the caller; left as a crash leaves it");
    // The thread started but ends without receiving: the handover fails, and the value is leaked.
    let dropped = Arc::new(Mutex::new(None));
    let value = Watched(Arc::clone(&dropped));
    assert_eq!(release_off_thread(|release| { std::thread::spawn(move || drop(release)).join().unwrap(); Ok(()) }, || Some(value), by), Released::NotHanded);
    assert_eq!(*dropped.lock().unwrap(), None, "not dropped on the caller; left as a crash leaves it");
    // Released normally: dropped on its own thread.
    let dropped = Arc::new(Mutex::new(None));
    let value = Watched(Arc::clone(&dropped));
    assert_eq!(release_off_thread(|release| std::thread::Builder::new().spawn(release).map(|_| ()), || Some(value), by), Released::Done);
    let on = dropped.lock().unwrap().expect("dropped");
    assert_ne!(on, caller, "dropped on its own thread");
}
