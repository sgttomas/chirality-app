//! RECOVERY VC-R-05 through the real Host against an owned app-server peer:
//! a live turn with an in-flight item and an outstanding request, a stale
//! rendered view, a supplier exit, restart, recovery reads, a read failure and
//! the person's retry, an exit during recovery (CV-22), SR-09, and a relaunch
//! (CV-19). The peer is a fixture; it establishes no supplier behaviour.
use super::*;
use crate::recovery::{AppProjectSource, ExplicitAppProjectContext};
use crate::runtime_session::HomeSession;
use std::path::PathBuf;
use std::time::Instant;

/// `read-mode`: `ok` (default), `error` (thread/read answers an error) or
/// `exit` (the peer exits on thread/read). `history-turns`: the turns
/// thread/turns/list reports, newest first; `history-pages` splits them into
/// pages of that size.
const PEER: &str = r#"#!/usr/bin/python3
import sys,json,threading,time,os
if '--version' in sys.argv:
 print('codex-cli 0.160.0');sys.exit(0)
lock=threading.Lock()
def emit(v):
 with lock: print(json.dumps(v),flush=True)
def events():
 while True:
  if os.path.exists('crash-now'): os._exit(3)
  try:
   os.rename('queued-event.json','reading-event.json')
   with open('reading-event.json') as f: v=json.load(f)
   os.unlink('reading-event.json');emit(v)
  except FileNotFoundError: pass
  time.sleep(0.002)
threading.Thread(target=events,daemon=True).start()
def read(name,default):
 return open(name).read().strip() if os.path.exists(name) else default
def thread(tid):
 return {'id':tid,'cliVersion':'0.160.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'recovery fixture','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':'notLoaded'},'turns':[]}
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log: log.write(json.dumps(f)+'\n')
 m=f.get('method')
 if m=='initialize': result={'userAgent':'unqualified-recovery-fixture'}
 elif m=='thread/start':
  t=thread('thread');t['status']={'type':'idle'}
  result={'thread':t,'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
 elif m=='thread/read':
  mode=read('read-mode','ok')
  if mode=='exit': os._exit(4)
  if mode=='silent': continue
  if mode=='error':
   emit({'id':f['id'],'error':{'code':-32600,'message':'fixture: thread not found'}});continue
  result={'thread':thread(f['params']['threadId'])}
 elif m=='thread/turns/list':
  turns=json.loads(read('history-turns','[]'));size=int(read('history-pages','100'))
  start=int(f['params'].get('cursor') or 0)
  data=[{'id':t['id'],'status':t['status'],'items':[],'error':None,'itemsView':'summary'} for t in turns[start:start+size]]
  result={'data':data,'nextCursor':str(start+size) if start+size<len(turns) else None}
 else: continue
 emit({'id':f['id'],'result':result})
"#;

struct Fixture { root: PathBuf, cfg: HostConfig, home: Arc<HomeSession>, first: Value }
impl Fixture {
    fn new() -> Self {
        use std::os::unix::fs::PermissionsExt;
        let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(opaque_id("recovery-reads-").unwrap());
        for name in ["account", "probe"] { std::fs::create_dir_all(root.join(name)).unwrap(); }
        let peer = root.join("peer.py");
        std::fs::write(&peer, PEER).unwrap();
        std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
        let mut cfg = HostConfig::new(peer, root.join("account"), root.join("probe"), root.clone());
        cfg.allow_unverified_dev = true;
        cfg.wait_limit = Duration::from_secs(2);
        let home = Self::session(&root, &cfg);
        let first = home.host.snapshot()["generation"].clone();
        home.host.thread_start_selected(&root.to_string_lossy(), "fixture-model", "fixture-provider").unwrap();
        home.host.observe_conversation_project(&first, "thread", Some("H-acct"), &ExplicitAppProjectContext::known("P", AppProjectSource::ConfiguredDirectory).unwrap()).unwrap();
        Self { root, cfg, home, first }
    }
    /// A started Host with the App ledger (a new App session each time).
    fn session(root: &std::path::Path, cfg: &HostConfig) -> Arc<HomeSession> {
        let host = Arc::new(Host::new());
        host.configure_recovery(root.join("recovery.ledger.jsonl")).unwrap();
        host.start(cfg, "recovery fixture").unwrap();
        Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account, host, Ok(cfg.clone())).unwrap())
    }
    fn set(&self, name: &str, value: &str) { std::fs::write(self.root.join(name), value).unwrap(); }
    fn history(&self, turns: Value) { self.set("history-turns", &turns.to_string()); }
    fn emit(&self, event: Value) {
        let tmp = self.root.join("new-event.json");
        std::fs::write(&tmp, serde_json::to_vec(&event).unwrap()).unwrap();
        let deadline = Instant::now() + Duration::from_secs(3);
        while self.root.join("queued-event.json").exists() {
            assert!(Instant::now() < deadline, "previous event not taken");
            std::thread::sleep(Duration::from_millis(2));
        }
        std::fs::rename(tmp, self.root.join("queued-event.json")).unwrap();
    }
    fn until(&self, what: &str, done: impl Fn() -> bool) {
        let deadline = Instant::now() + Duration::from_secs(5);
        while !done() { assert!(Instant::now() < deadline, "{what} not observed"); std::thread::sleep(Duration::from_millis(5)); }
    }
    /// A live turn with an in-flight command item and an outstanding request.
    fn live_work(&self) {
        self.emit(json!({"method":"turn/started","params":{"threadId":"thread","turn":{"id":"turn-1","status":"inProgress","items":[],"error":null,"itemsView":"summary"}}}));
        self.until("turn/started", || self.home.host.conversation_turn(&self.first, "thread", "turn-1").is_some());
        self.emit(json!({"method":"item/started","params":{"threadId":"thread","turnId":"turn-1","item":{"id":"item-1","type":"commandExecution","status":"inProgress","command":"NEVER_PERSIST_THIS"}}}));
        self.emit(json!({"id":7,"method":"item/fileChange/requestApproval","params":{"threadId":"thread","turnId":"turn-1","itemId":"item-1"}}));
        self.until("the request", || self.home.host.snapshot()["serverRequests"].as_array().is_some_and(|r| r.iter().any(|e| e["state"] == "outstanding")));
    }
    fn crash(&self) {
        self.set("crash-now", "");
        self.until("unexpected exit", || self.home.host.snapshot()["state"] == "exited-unexpectedly");
        std::fs::remove_file(self.root.join("crash-now")).unwrap();
    }
    /// Restart Codex after the exit: the process is stopped (LT-17…LT-23 from
    /// `exited-unexpectedly`) and started again (HOSTING §4.6).
    fn restart(&self) {
        let generation = self.home.host.snapshot()["generation"].clone();
        self.home.host.stop_scoped(&generation, "the person", "Restart Codex").unwrap();
        self.home.host.start(&self.cfg, "the person: Restart Codex").unwrap();
    }
    fn wire(&self) -> Vec<Value> {
        std::fs::read_to_string(self.root.join("wire.jsonl")).unwrap_or_default().lines().map(|l| serde_json::from_str(l).unwrap()).collect()
    }
    fn methods(&self) -> Vec<String> { self.wire().iter().map(|f| f["method"].as_str().unwrap_or("").to_owned()).collect() }
    fn ledger(&self) -> Vec<Value> {
        std::fs::read_to_string(self.root.join("recovery.ledger.jsonl")).unwrap().lines().map(|l| serde_json::from_str(l).unwrap()).collect()
    }
    fn states(&self) -> Vec<String> {
        self.ledger().iter().filter(|r| r["kind"] == "conversation_index").map(|r| r["lastObservedExecution"]["state"].as_str().unwrap().to_owned()).collect()
    }
    fn events(home: &HomeSession, kind: &str) -> Vec<Value> {
        home.host.recovery_custody().snapshot()["live"]["events"].as_array().unwrap().iter().filter(|e| e["kind"] == kind).cloned().collect()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = self.home.host.stop("recovery fixture cleanup", "test ended");
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn validate_event(event: &Value) {
    let schema: Value = serde_json::from_str(include_str!("../resources/runtime_core/recovery.custody-event.schema.json")).unwrap();
    let validator = jsonschema::options().offline().build(&schema).unwrap();
    assert!(validator.is_valid(event), "custody event schema refused {event}");
}

#[test]
fn vcr05_exit_restart_read_failure_retry_and_recovery_from_codex() {
    let f = Fixture::new();
    f.live_work();
    // A stale rendered view: the turn and its item as last received live.
    crate::host_tick::receive_view(&f.home);
    f.crash();
    let lost = Fixture::events(&f.home, "observation_lost");
    assert_eq!(lost.len(), 1);
    validate_event(&lost[0]);
    assert_eq!(lost[0]["liveTurns"], json!([{"threadId":"thread","turnId":"turn-1"}]));
    assert_eq!(lost[0]["inFlightItems"][0]["itemId"], "item-1");
    assert_eq!(lost[0]["outstandingEntries"][0]["method"], "item/fileChange/requestApproval");
    // Nothing is read before the home's process is ready again.
    assert_eq!(crate::host_tick::recovery_tick_home(&f.home), 0);
    let before = f.wire().len();

    // CV-11 then CV-14: the reads fail; the conversation is unavailable.
    f.set("read-mode", "error");
    f.restart();
    let second = f.home.host.snapshot()["generation"].clone();
    assert_ne!(second, f.first);
    assert_eq!(crate::host_tick::recovery_tick_home(&f.home), 0, "no page from a failed read");
    let failed = Fixture::events(&f.home, "observation_recovered");
    assert_eq!(failed.len(), 1);
    validate_event(&failed[0]);
    assert_eq!((failed[0]["priorEvents"].as_str(), failed[0]["home"].as_str()), (Some("unavailable"), Some("H-acct")));
    assert!(failed[0]["unavailableReason"].as_str().unwrap().contains("fixture: thread not found"), "{}", failed[0]);
    assert_eq!(failed[0]["generation"], crate::recovery::generation_ref(&second).unwrap(), "read in the new generation");
    // Not read again in the same generation until the person asks.
    crate::host_tick::recovery_tick_home(&f.home);
    assert_eq!(f.methods().iter().filter(|m| *m == "thread/read").count(), 1);
    assert!(f.home.host.recovery_retry("other-thread").is_err());

    // CV-15 then CV-13: the person's retry; Codex reports the turn interrupted.
    f.set("read-mode", "ok");
    f.history(json!([{"id":"turn-1","status":"interrupted"}]));
    f.home.host.recovery_retry("thread").unwrap();
    assert_eq!(crate::host_tick::recovery_tick_home(&f.home), 2);
    let recovered = Fixture::events(&f.home, "observation_recovered");
    assert_eq!(recovered.len(), 2);
    validate_event(&recovered[1]);
    assert_eq!(recovered[1]["priorEvents"], "accessible");
    assert_eq!(recovered[1]["turns"], json!([{"turnId":"turn-1","supplierStatus":"interrupted","appReading":"recovered from Codex: interrupted"}]));
    let outcome = Fixture::events(&f.home, "turn_outcome");
    assert_eq!(outcome.len(), 1);
    validate_event(&outcome[0]);
    assert_eq!((outcome[0]["outcome"].as_str(), outcome[0]["source"].as_str()), (Some("interrupted"), Some("recovered-from-supplier")));
    assert_eq!(outcome[0]["itemsNotCompleted"], json!([{"itemId":"item-1","itemType":"commandExecution","settled":"not completed (turn ended)"}]));
    assert!(outcome[0].get("cause").is_none(), "no stop request: cause not observed");

    // Only history reads after the restart, on the new process: no prompt re-sent, no resume.
    let after: Vec<Value> = f.wire()[before..].to_vec();
    let methods: Vec<&str> = after.iter().map(|w| w["method"].as_str().unwrap_or("")).collect();
    assert_eq!(methods, ["initialize", "initialized", "thread/read", "thread/read", "thread/turns/list"]);
    assert_eq!(after[2]["params"], json!({"threadId":"thread","includeTurns":false}));
    assert_eq!(after[4]["params"], json!({"threadId":"thread","sortDirection":"desc","itemsView":"summary"}));
    let reads: Vec<Value> = f.home.host.client_requests().into_iter().filter(|r| r["method"] == "thread/read" || r["method"] == "thread/turns/list").collect();
    assert!(reads.iter().all(|r| r["initiator"] == json!({"kind":"app-rule","name":"recovery-read"}) && r["generation"] == second), "{reads:?}");
    // The old request stays ended; it is never answered in the new generation.
    assert_eq!(f.home.host.answer_server_request(&f.first, &json!(7), &json!({"decision":"accept"}), "person-via-interaction", Some("person:x (identity not verified)")).unwrap_err(), "generation-closed");

    // The custody state and the ledger: append-only, schema-valid, no content.
    let observation = f.home.host.recovery_custody().snapshot()["live"]["observations"].as_array().unwrap().iter()
        .find(|o| o["generation"] == crate::recovery::generation_ref(&f.first).unwrap()).unwrap().clone();
    assert_eq!((observation["state"].as_str(), observation["liveTurn"].is_null()), (Some("indexed"), true));
    let states = f.states();
    let lost_at = states.iter().position(|s| s == "observation-lost").unwrap();
    assert_eq!(states[lost_at..], ["observation-lost", "recovering", "unavailable", "recovering", "indexed"]);
    let bytes = std::fs::read_to_string(f.root.join("recovery.ledger.jsonl")).unwrap();
    assert!(!bytes.contains("NEVER_"));
    crate::recovery::RecoveryLedger::open(f.root.join("recovery.ledger.jsonl")).unwrap();
    // The stale rendered view is replaced: the ready generation's view has
    // the recovered turn, and the prior one stays observation-ended.
    let view = crate::host_tick::receive_view(&f.home);
    let status = f.home.runtime.lock().unwrap().receive(&f.home.host.observe(&second, 0));
    assert_eq!(status["observerRecovery"]["recoveryPagesRead"], 2);
    assert_eq!(status["observerRecovery"]["historyRebuilt"], false, "metadata and turn summaries only");
    let turns = view["turns"].as_array().unwrap();
    assert_eq!(turns.iter().filter(|t| t["id"] == "turn-1").map(|t| t["status"].clone()).collect::<Vec<_>>(), [json!("interrupted")], "{view}");
    // The stale live reading stays only in the prior, observation-ended view.
    let prior = &status["priorNativeViews"][0]["view"]["turns"];
    assert!(prior.as_array().unwrap().iter().any(|t| t["id"] == "turn-1" && t["status"] == "inProgress"), "{prior}");
    assert_eq!(status["priorNativeViews"][0]["standing"], "observation-ended; not live custody");
    // A later ready reads nothing more.
    assert_eq!(crate::host_tick::recovery_tick_home(&f.home), 0);
}

#[test]
fn cv22_exit_during_recovery_returns_to_pending_and_resumes_at_next_ready() {
    let f = Fixture::new();
    f.live_work();
    f.crash();
    f.set("read-mode", "exit");
    f.restart();
    crate::host_tick::recovery_tick_home(&f.home);
    f.until("exit during recovery", || f.home.host.snapshot()["state"] == "exited-unexpectedly");
    assert!(Fixture::events(&f.home, "observation_recovered").is_empty(), "CV-22 records no recovery event");
    let observation = f.home.host.recovery_custody().snapshot()["live"]["observations"].as_array().unwrap().iter()
        .find(|o| o["generation"] == crate::recovery::generation_ref(&f.first).unwrap()).unwrap().clone();
    assert_eq!(observation["state"], "recovery-pending");
    assert_eq!(f.states().last().unwrap(), "recovery-pending");
    // The next ready: Codex reports the turn still inProgress, so the outcome stays unknown.
    f.set("read-mode", "ok");
    f.history(json!([{"id":"turn-1","status":"inProgress"}]));
    f.restart();
    assert_eq!(crate::host_tick::recovery_tick_home(&f.home), 2);
    let recovered = Fixture::events(&f.home, "observation_recovered");
    assert_eq!(recovered.len(), 1);
    validate_event(&recovered[0]);
    assert_eq!(recovered[0]["turns"][0]["supplierStatus"], "inProgress");
    assert!(recovered[0]["turns"][0]["appReading"].as_str().unwrap().starts_with("outcome unknown"));
    let outcome = &Fixture::events(&f.home, "turn_outcome")[0];
    validate_event(outcome);
    assert_eq!((outcome["outcome"].as_str(), outcome["source"].as_str()), (Some("unknown"), Some("not-observed")));
    assert!(outcome.get("itemsNotCompleted").is_none(), "items settle only when Codex reports the turn ended");
    assert_eq!(f.states().last().unwrap(), "indexed");
}

#[test]
fn sr09_outcome_unknown_stop_request_recovers_status_from_history() {
    let f = Fixture::new();
    f.live_work();
    // The peer never answers this interrupt: SR-02, then SR-08 at the exit.
    let written = f.home.host.turn_interrupt_begin(&f.first, "thread", "turn-1", crate::stop_records::Cause::PersonInterrupt, "H-acct", &crate::stop_records::person("fixture person")).unwrap();
    assert_eq!(written.evidence()["writeResult"], "written");
    f.crash();
    let record = |home: &HomeSession| home.host.snapshot()["stopRequests"]["records"][0].clone();
    assert_eq!((record(&f.home)["state"].as_str(), record(&f.home)["transition"].as_str()), (Some("outcome-unknown"), Some("SR-08")));
    f.history(json!([{"id":"turn-1","status":"interrupted"}]));
    f.restart();
    crate::host_tick::recovery_tick_home(&f.home);
    let now = record(&f.home);
    assert_eq!((now["state"].as_str(), now["transition"].as_str(), now["label"].as_str(), now["codexReported"].as_str()), (Some("outcome-recovered"), Some("SR-09"), Some("interrupted by the person"), Some("interrupted")));
    assert_eq!(now["persistence"], "recorded in the App ledger");
    let entry = f.ledger().into_iter().rev().find(|e| e["kind"] == "stop_request").unwrap();
    crate::stop_records::validate(&entry["record"]).unwrap();
    assert_eq!((entry["record"]["outcomeSource"].as_str(), entry["record"]["turnOutcome"].as_str()), (Some("recovered-from-supplier"), Some("interrupted")));
    let outcome = &Fixture::events(&f.home, "turn_outcome")[0];
    validate_event(outcome);
    assert_eq!((outcome["cause"].as_str(), outcome["stopRequest"].as_str()), (Some("person-interrupt"), entry["record"]["stopRequestId"].as_str()));
    let turns = &Fixture::events(&f.home, "observation_recovered")[0]["turns"][0];
    assert_eq!(turns["appReading"], "interrupted by the person; Codex reports: interrupted");
}

#[test]
fn cv19_relaunch_recovers_an_earlier_session_conversation_and_its_stop_request() {
    let f = Fixture::new();
    f.live_work();
    f.home.host.turn_interrupt_begin(&f.first, "thread", "turn-1", crate::stop_records::Cause::PersonInterrupt, "H-acct", &crate::stop_records::person("fixture person")).unwrap();
    // The App ends without a record; the relaunched App has its own session.
    f.crash();
    let _ = f.home.host.stop("fixture", "test relaunch");
    // Many turns since: the lost turn is on the second page of history.
    f.history(json!([{"id":"turn-3","status":"completed"},{"id":"turn-2","status":"completed"},{"id":"turn-1","status":"failed"}]));
    f.set("history-pages", "2");
    let relaunched = Fixture::session(&f.root, &f.cfg);
    let wire = f.wire().len();
    let restart = relaunched.host.recovery_custody().snapshot()["restartEvents"].clone();
    assert_eq!(restart[0]["priorSessionEnd"], "ended-without-record");
    assert_eq!(crate::host_tick::recovery_tick_home(&relaunched), 3, "thread/read and two turn pages");
    let reads: Vec<String> = f.wire()[wire..].iter().map(|w| w["method"].as_str().unwrap().to_owned()).collect();
    assert_eq!(reads, ["thread/read", "thread/turns/list", "thread/turns/list"]);
    let recovered = &Fixture::events(&relaunched, "observation_recovered")[0];
    validate_event(recovered);
    assert_eq!(recovered["appSession"], relaunched.host.snapshot()["generation"]["appSession"]);
    let outcome = &Fixture::events(&relaunched, "turn_outcome")[0];
    validate_event(outcome);
    assert_eq!((outcome["outcome"].as_str(), outcome["cause"].as_str()), (Some("failed"), Some("person-interrupt")));
    // The earlier session's request: SR-08 at startup, then SR-09 here.
    let transitions: Vec<String> = f.ledger().iter().filter(|e| e["kind"] == "stop_request").map(|e| e["record"]["transition"].as_str().unwrap().to_owned()).collect();
    assert_eq!(transitions.iter().rev().take(2).rev().cloned().collect::<Vec<_>>(), ["SR-08", "SR-09"]);
    let back = relaunched.host.snapshot()["stopRequests"]["records"][0].clone();
    assert_eq!((back["label"].as_str(), back["earlierSession"].as_bool()), (Some("failed (stop requested)"), Some(true)));
    // The restart fact stays; the conversation reads indexed.
    let view = relaunched.host.recovery_custody().snapshot();
    assert_eq!(view["restartEvents"], restart);
    assert_eq!(view["historicalConversations"][0]["index"]["lastObservedExecution"]["state"], "indexed");
    assert_eq!(f.states().last().unwrap(), "indexed");
    // A third session finds nothing left to recover.
    let _ = relaunched.host.stop("fixture", "test relaunch");
    let third = Fixture::session(&f.root, &f.cfg);
    let wire = f.wire().len();
    assert_eq!(crate::host_tick::recovery_tick_home(&third), 0);
    assert_eq!(f.wire().len(), wire);
    let _ = third.host.stop("fixture", "test ended");
}

#[test]
fn restart_codex_with_a_live_turn_recovers_it_with_the_stop_label_and_history_note() {
    let f = Fixture::new();
    f.live_work();
    let workflows = std::sync::Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    let (host, cfg) = (f.home.host.clone(), f.cfg.clone());
    // The peer answers no interrupt: the turn is live at the stop (SR-08).
    let out = crate::codex_stop::stop_native_home_within(&f.home, &workflows, &f.first, true, "fixture person", Duration::from_millis(300), |_| true, move || host.start(&cfg, "the person: Restart Codex")).unwrap();
    assert_eq!(out["start"]["state"], "started", "{out}");
    f.history(json!([{"id":"turn-1","status":"interrupted"}]));
    assert_eq!(crate::host_tick::recovery_tick_home(&f.home), 2);
    let turn = &Fixture::events(&f.home, "observation_recovered")[0]["turns"][0];
    assert_eq!(turn["appReading"], "interrupted by Stop Codex; Codex reports: interrupted");
    assert_eq!(turn["historyNote"], "graceful-stop abort note (Codex 0.158.0, observed OBS-2)");
    let outcome = &Fixture::events(&f.home, "turn_outcome")[0];
    validate_event(outcome);
    assert_eq!(outcome["cause"], "codex-stop");
    assert_eq!(f.home.host.snapshot()["stopRequests"]["records"][0]["label"], "interrupted by Stop Codex");
    assert!(!f.methods().iter().any(|m| matches!(m.as_str(), "thread/resume" | "turn/start" | "turn/steer")), "nothing continued or re-sent");
}

#[test]
fn a_turn_absent_from_history_stays_unknown() {
    let f = Fixture::new();
    f.live_work();
    f.crash();
    f.restart();
    assert_eq!(crate::host_tick::recovery_tick_home(&f.home), 2);
    let recovered = &Fixture::events(&f.home, "observation_recovered")[0];
    validate_event(recovered);
    assert_eq!(recovered["turns"], json!([{"turnId":"turn-1","supplierStatus":"absent","appReading":"outcome unknown (turn not in Codex history)"}]));
    let outcome = &Fixture::events(&f.home, "turn_outcome")[0];
    assert_eq!((outcome["outcome"].as_str(), outcome["source"].as_str()), (Some("unknown"), Some("not-observed")));
}

#[test]
fn an_unanswered_read_is_unavailable_and_a_retry_while_not_ready_waits_for_ready() {
    let f = Fixture::new();
    f.live_work();
    f.crash();
    // The person's retry before Codex is ready is kept for the next ready.
    f.set("read-mode", "silent");
    f.restart();
    let pages = f.home.host.recovery_reads(Duration::from_millis(300));
    assert!(pages.is_empty());
    let failed = &Fixture::events(&f.home, "observation_recovered")[0];
    validate_event(failed);
    assert!(failed["unavailableReason"].as_str().unwrap().contains("thread/read returned no result"), "{failed}");
    f.crash();
    f.home.host.recovery_retry("thread").unwrap();
    assert!(f.home.host.recovery_reads(Duration::from_millis(300)).is_empty(), "not ready: nothing read");
    f.set("read-mode", "ok");
    f.history(json!([{"id":"turn-1","status":"completed"}]));
    f.restart();
    assert_eq!(f.home.host.recovery_reads(Duration::from_secs(2)).len(), 2);
    assert_eq!(f.states().last().unwrap(), "indexed");
}

#[test]
fn sr09_transition_is_only_from_outcome_unknown_with_a_final_status() {
    let generation = json!({"appSession":"s","home":"h","spawnCounter":1});
    let mut request = crate::stop_records::StopRequest::requested(&generation, "H-acct", "t", "u", crate::stop_records::Cause::Quit, &crate::stop_records::person("p")).unwrap();
    assert!(request.recovered("interrupted").unwrap().is_none(), "requested is not outcome-unknown");
    request.sent("client:1", &json!(1)).unwrap();
    request.generation_closed().unwrap().unwrap();
    assert!(request.recovered("inProgress").unwrap().is_none(), "no final status");
    let record = request.recovered("completed").unwrap().unwrap();
    crate::stop_records::validate(&record).unwrap();
    assert_eq!((record["outcomeLabel"].as_str(), record["transition"].as_str()), (Some("completed (quit requested)"), Some("SR-09")));
    assert!(request.recovered("interrupted").unwrap().is_none(), "recovered once");
    let back = crate::stop_records::StopRequest::from_record(&record).unwrap();
    assert_eq!(back.generation(), &generation);
}
