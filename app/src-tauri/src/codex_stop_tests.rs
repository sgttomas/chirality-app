//! Stop Codex / Restart Codex: the sequence through `stop_or_restart` with a
//! recording double, the command glue, the native question text, and the real
//! Host binding (`stop_native_home_within`) against an owned app-server peer.
//! The peer is a fixture; it establishes no supplier behaviour.
use super::*;

fn view_material(turns: Value, requests: Value, runs: Value) -> Value {
    json!({"modeHomeClass":"account","generation":{"appSession":"s","home":"h","spawnCounter":1},"state":"ready","notReady":null,
        "observedLiveTurns":turns,"observedOutstandingRequests":requests,"observedActiveChildren":[],"knownChildActivityUnknown":[],
        "coverage":{"turns":{"unresolved":[]}},"runsInForce":runs})
}
fn live(turn: &str) -> Value {
    json!({"generation":{"appSession":"s","home":"h","spawnCounter":1},"threadId":"thread","turnId":turn,"status":"inProgress","source":"turn/started"})
}
fn ended(status: &str) -> Option<Value> {
    Some(json!({"terminalEventObserved":true,"nativeTurn":{"status":status}}))
}

/// Records every operation in order. `ends` gives each turn's reading;
/// `unacknowledged` turns never acknowledge (the double waits out the budget).
struct Ops {
    log: Vec<String>,
    materials: Vec<Value>,
    answers: Vec<bool>,
    asked: Vec<Value>,
    ends: fn(&str) -> Option<Value>,
    unacknowledged: Vec<&'static str>,
    waits: Vec<Duration>,
    stop_ok: bool,
    fail_second_assess: bool,
}
impl Ops {
    fn new(materials: Vec<Value>, answers: Vec<bool>) -> Self {
        Self { log: vec![], materials, answers, asked: vec![], ends: |_| None, unacknowledged: vec![], waits: vec![], stop_ok: true, fail_second_assess: false }
    }
    fn run(&mut self, restart: bool) -> Result<Value, String> {
        stop_or_restart(self, restart, Duration::from_millis(150))
    }
}
impl StopOps for Ops {
    type Pending = String;
    fn assess(&mut self) -> Result<Assessment, String> {
        self.log.push("assess".into());
        if self.fail_second_assess && self.log.iter().filter(|l| *l == "assess").count() == 2 {
            return Err("Codex changed since this view".into());
        }
        let next = if self.materials.len() > 1 { self.materials.remove(0) } else { self.materials[0].clone() };
        Ok(Assessment::new(next, false))
    }
    fn confirm(&mut self, view: &Value) -> bool {
        self.log.push("ask".into());
        self.asked.push(view.clone());
        self.answers.remove(0)
    }
    fn close_to_new_turns(&mut self) -> Result<(), String> {
        self.log.push("close".into());
        Ok(())
    }
    fn reopen_to_new_turns(&mut self) {
        self.log.push("reopen".into());
    }
    fn interrupt(&mut self, turn: &Value) -> Result<String, String> {
        let id = turn["turnId"].as_str().unwrap().to_owned();
        self.log.push(format!("interrupt {id}"));
        Ok(id)
    }
    fn acknowledgment(&mut self, pending: &String, wait: Duration) -> Result<Value, String> {
        self.log.push(format!("ack {pending}"));
        self.waits.push(wait);
        if self.unacknowledged.contains(&pending.as_str()) {
            std::thread::sleep(wait);
            return Err("no acknowledgment within the wait".into());
        }
        Ok(json!({"id":1,"result":{}}))
    }
    fn turn_reading(&mut self, turn: &Value) -> Option<Value> {
        (self.ends)(turn["turnId"].as_str().unwrap())
    }
    fn stop(&mut self) -> Result<Value, String> {
        self.log.push("stop".into());
        if self.stop_ok { Ok(json!({"state":"stopped"})) } else { Err("stop not accepted in state stopping".into()) }
    }
    fn start(&mut self) -> Result<Value, String> {
        self.log.push("start".into());
        Ok(json!({"state":"ready"}))
    }
}

#[test]
fn cancel_leaves_codex_running_and_sends_nothing() {
    for restart in [false, true] {
        let mut ops = Ops::new(vec![view_material(json!([live("t1")]), json!([{"method":"item/tool/requestUserInput","requestIdentity":7,"threadId":"thread"}]), json!([]))], vec![false]);
        let out = ops.run(restart).unwrap();
        assert_eq!(out["state"], "cancelled");
        assert!(out["reading"].as_str().unwrap().contains("Nothing was interrupted, stopped or sent"));
        assert_eq!(ops.log, ["assess", "ask"], "cancel: not closed to new turns, no interrupt, no stop, no start");
        assert_eq!(ops.asked[0]["observedLiveTurns"][0]["turnId"], "t1", "the question showed the live turn");
    }
}

#[test]
fn confirm_closes_to_new_turns_writes_every_interrupt_then_waits_then_stops() {
    let mut ops = Ops::new(vec![view_material(json!([live("t1"), live("t2"), live("t3"), live("t4")]), json!([]), json!([]))], vec![true]);
    ops.ends = |turn| match turn {
        "t1" => ended("interrupted"),
        "t2" => ended("completed"),
        "t3" => ended("failed"),
        _ => None,
    };
    let out = ops.run(false).unwrap();
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "interrupt t1", "interrupt t2", "interrupt t3", "interrupt t4", "ack t1", "ack t2", "ack t3", "ack t4", "stop"],
        "closed before the final reassessment; all interrupts written before any wait; the stop last");
    assert_eq!(out["state"], "stopped");
    let labels: Vec<&str> = out["turns"].as_array().unwrap().iter().map(|t| t["label"].as_str().unwrap()).collect();
    assert_eq!(labels, ["interrupted by Stop Codex", "completed (Stop Codex requested)", "failed (Stop Codex requested)", "interrupted by Stop Codex (final status not observed)"]);
    // t4 was acknowledged but never observed ended: the acknowledgment is not its end.
    let t4 = &out["turns"][3];
    assert_eq!(t4["interruptRequest"]["state"], "acknowledged");
    assert!(t4["interruptRequest"]["reading"].as_str().unwrap().contains("not the turn's end"));
    assert!(t4["codexReported"].is_null());
    assert!(out["historyNote"].as_str().unwrap().contains("comes from this stop"), "G-5 note for a turn live at the stop");
    assert_eq!(out["standing"], "your operational choice; not a recorded act");
    assert!(out["records"].as_str().unwrap().contains("writes no recovery stop record"));
    assert!(out["start"].is_null() && out["conversations"].is_null());
}

#[test]
fn every_label_is_one_of_the_four_schema_values() {
    let four = ["interrupted by Stop Codex", "completed (Stop Codex requested)", "failed (Stop Codex requested)", "interrupted by Stop Codex (final status not observed)"];
    // DEL-01-02 recovery.stop-request.schema.json, `outcomeLabel` enum.
    let schema = include_str!("../../../execution/PKG-01/DEL-01-02/Design/recovery.stop-request.schema.json");
    let enumerated = &schema[schema.find("\"outcomeLabel\"").unwrap()..];
    let enumerated = &enumerated[..enumerated.find(']').unwrap()];
    for status in [Some("interrupted"), Some("completed"), Some("failed"), Some("inProgress"), Some("other"), None] {
        let label = outcome_label(status);
        assert!(four.contains(&label), "{status:?}: {label}");
        assert!(enumerated.contains(&format!("\"{label}\"")), "{label} is a schema outcomeLabel value");
    }
}

#[test]
fn an_unacknowledged_first_interrupt_does_not_starve_the_others() {
    let mut ops = Ops::new(vec![view_material(json!([live("t1"), live("t2")]), json!([]), json!([]))], vec![true]);
    ops.unacknowledged = vec!["t1"];
    ops.ends = |turn| if turn == "t2" { ended("interrupted") } else { None };
    let begin = Instant::now();
    let out = ops.run(false).unwrap();
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "interrupt t1", "interrupt t2", "ack t1", "ack t2", "stop"], "t2 was written before t1's wait");
    assert!(ops.waits[1] < Duration::from_millis(20), "t2's acknowledgment is read on the shared deadline, not a fresh budget");
    assert!(begin.elapsed() < Duration::from_millis(400), "one stop wait limit in all");
    assert_eq!(out["turns"][0]["interruptRequest"]["state"], "sent; not acknowledged");
    assert_eq!(out["turns"][0]["label"], "interrupted by Stop Codex (final status not observed)");
    assert_eq!(out["turns"][1]["interruptRequest"]["state"], "acknowledged");
    assert_eq!(out["turns"][1]["label"], "interrupted by Stop Codex");
}

#[test]
fn all_turns_ended_before_the_limit_stop_without_waiting_it_out() {
    let mut ops = Ops::new(vec![view_material(json!([live("t1")]), json!([]), json!([]))], vec![true]);
    ops.ends = |_| ended("interrupted");
    let begin = Instant::now();
    let out = ops.run(false).unwrap();
    assert!(begin.elapsed() < Duration::from_millis(140));
    assert!(out["historyNote"].is_null());
    assert_eq!(out["turns"][0]["codexReported"], "interrupted");
}

#[test]
fn no_live_work_is_a_simple_confirmation_and_sends_no_interrupt() {
    let mut ops = Ops::new(vec![view_material(json!([]), json!([]), json!([]))], vec![true]);
    let out = ops.run(false).unwrap();
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "stop"]);
    assert_eq!(out["turns"], json!([]));
    let statement = crate::act_control::native_statement::codex_stop_statement(&ops.asked[0]).unwrap();
    assert!(statement.in_app.is_none());
    assert!(statement.text.starts_with("Stop Codex for this home?"));
    assert!(statement.text.contains("Observed: no live turns, waiting requests, delegated agents or workflow runs in force."));
    assert!(statement.text.contains("Stop Codex stops this Codex process."));
    assert!(!statement.text.contains("interrupts each live turn"), "no interrupt wording without live work");
    assert!(statement.text.contains("Keep Codex running (the default) and Cancel change nothing"));
}

#[test]
fn a_list_changed_on_confirm_is_asked_again_and_a_cancel_then_changes_nothing() {
    let first = view_material(json!([live("t1")]), json!([]), json!([]));
    let second = view_material(json!([live("t1"), live("t2")]), json!([]), json!([]));
    let mut ops = Ops::new(vec![first, second.clone(), second], vec![true, false]);
    let out = ops.run(false).unwrap();
    assert_eq!(out["state"], "cancelled");
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "reopen", "ask"], "reopened to new turns and asked again; nothing sent");
    assert_eq!(ops.asked[1]["changedWhileAsking"], true);
    assert_eq!(ops.asked[1]["observedLiveTurns"].as_array().unwrap().len(), 2);
    assert!(crate::act_control::native_statement::codex_stop_statement(&ops.asked[1]).unwrap().text.contains("Live work changed while this question was open"));
}

#[test]
fn a_list_changed_on_confirm_then_confirmed_again_interrupts_the_current_list() {
    let first = view_material(json!([live("t1")]), json!([]), json!([]));
    let second = view_material(json!([live("t1"), live("t2")]), json!([]), json!([]));
    let mut ops = Ops::new(vec![first, second.clone(), second], vec![true, true]);
    ops.ends = |_| ended("interrupted");
    let out = ops.run(false).unwrap();
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "reopen", "ask", "close", "assess", "interrupt t1", "interrupt t2", "ack t1", "ack t2", "stop"]);
    assert_eq!(out["state"], "stopped");
    assert_eq!(out["assessment"]["observedLiveTurns"].as_array().unwrap().len(), 2, "the outcome names the list the person confirmed");
}

#[test]
fn an_assessment_failing_after_confirm_reopens_and_stops_nothing() {
    let mut ops = Ops::new(vec![view_material(json!([live("t1")]), json!([]), json!([]))], vec![true]);
    ops.fail_second_assess = true;
    let error = ops.run(false).unwrap_err();
    assert!(error.contains("Nothing was interrupted or stopped"));
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "reopen"]);
}

#[test]
fn restart_starts_once_after_the_stop_and_continues_no_conversation() {
    let mut ops = Ops::new(vec![view_material(json!([live("t1")]), json!([]), json!([]))], vec![true]);
    ops.ends = |_| ended("interrupted");
    let out = ops.run(true).unwrap();
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "interrupt t1", "ack t1", "stop", "start"], "start follows the stop; no resume or other operation");
    assert_eq!(out["action"], "Restart Codex");
    assert_eq!(out["start"]["state"], "started");
    assert!(out["conversations"].as_str().unwrap().contains("No conversation was continued automatically"));
    assert_eq!(out["turns"][0]["label"], "interrupted by Stop Codex", "Restart's interrupts carry cause codex-stop");
}

#[test]
fn a_refused_stop_is_a_refusal_with_no_turn_label_and_reopens_to_new_turns() {
    let mut ops = Ops::new(vec![view_material(json!([live("t1")]), json!([]), json!([]))], vec![true]);
    ops.stop_ok = false;
    let out = ops.run(true).unwrap();
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "interrupt t1", "ack t1", "stop", "reopen"], "no second process; reopened");
    assert_eq!(out["state"], "stop refused");
    assert_eq!(out["stop"]["state"], "refused");
    assert_eq!(out["start"]["state"], "not started");
    assert!(out["turns"][0]["label"].is_null(), "no Stop label when Codex was not stopped");
    assert!(out["historyNote"].is_null() && out["conversations"].is_null());
}

#[test]
fn command_glue_gate_precheck_and_result_mapping() {
    // Gate: busy refuses; a poisoned gate is recovered, not busy forever.
    let gate = std::sync::Arc::new(Mutex::new(()));
    {
        let _held = question_gate(&gate).unwrap();
        assert!(question_gate(&gate).unwrap_err().contains("already open"));
    }
    let poison = gate.clone();
    let _ = std::thread::spawn(move || {
        let _guard = poison.lock().unwrap();
        panic!("poison the gate");
    })
    .join();
    assert!(gate.is_poisoned());
    assert!(question_gate(&gate).is_ok(), "a poisoned gate is recovered");
    // Restart precheck: either failure refuses before anything is asked.
    assert!(restart_precheck(Ok(()), || Ok(())).is_ok());
    assert!(restart_precheck(Err("CHIRALITY_CODEX_BIN is not set".into()), || panic!("not reached")).unwrap_err().contains("cannot start Codex again here (CHIRALITY_CODEX_BIN is not set); nothing stopped"));
    assert!(restart_precheck(Ok(()), || Err("binding changed".into())).unwrap_err().contains("(binding changed); nothing stopped"));
    // Result mapping.
    let kept = Mutex::new(Vec::new());
    let cancelled = json!({"action":"Stop Codex","state":"cancelled"});
    assert_eq!(finish(&kept, "Stop Codex", None, Ok(cancelled.clone())).unwrap(), cancelled);
    assert!(kept.lock().unwrap().is_empty(), "a cancel is not kept");
    assert_eq!(finish(&kept, "Stop Codex", Some("statement too long".into()), Ok(cancelled)).unwrap_err(), "statement too long", "a presentation refusal is a refusal, never a cancel");
    assert!(kept.lock().unwrap().is_empty());
    let refused = json!({"action":"Stop Codex","state":"stop refused","stop":{"state":"refused","reading":"stop already requested"}});
    assert_eq!(finish(&kept, "Stop Codex", None, Ok(refused)).unwrap_err(), "Stop Codex: Codex was not stopped: stop already requested");
    assert_eq!(kept.lock().unwrap().len(), 1, "a confirmed, refused stop is kept for display");
    assert!(finish(&kept, "Stop Codex", None, Err("Codex changed".into())).is_err());
    for n in 0..30 {
        finish(&kept, "Stop Codex", None, Ok(json!({"state":"stopped","n":n}))).unwrap();
    }
    let kept = kept.lock().unwrap();
    assert_eq!(kept.len(), OUTCOMES_KEPT);
    assert_eq!(kept.last().unwrap()["n"], 29, "newest kept, oldest dropped");
}

#[test]
fn question_lists_every_item_and_falls_back_to_a_named_assessment_when_long() {
    let runs = json!([{"run":"run-1","conversation":"thread","workflow":{"origin":"project","name":"coordinated-knowledge-work"},"state":"open"}]);
    let requests = json!([{"method":"item/commandExecution/requestApproval","requestIdentity":3,"threadId":"thread"}]);
    let mut view = Assessment::new(view_material(json!([live("t1")]), requests, runs.clone()), true).view().clone();
    let s = crate::act_control::native_statement::codex_stop_statement(&view).unwrap();
    assert!(s.in_app.is_none());
    for expected in ["Restart Codex for this home?", "Live turn: thread / t1", "Outstanding request: item/commandExecution/requestApproval #3 in thread",
        "Workflow run in force: coordinated-knowledge-work (run run-1) in thread", "waits up to 10 s", "and starts it again",
        "not answered", "ends no run", "continue one yourself", "not a recorded act", "Restart Codex proceeds; Keep Codex running (the default)"] {
        assert!(s.text.contains(expected), "missing {expected:?} in\n{}", s.text);
    }
    view["observedLiveTurns"] = json!((0..40).map(|n| live(&format!("turn-{n}"))).collect::<Vec<_>>());
    let s = crate::act_control::native_statement::codex_stop_statement(&view).unwrap();
    let shown = s.in_app.expect("too long for the alert: shown whole in the App");
    assert_eq!(shown.content, view);
    assert!(s.text.contains(&shown.digest) && s.text.contains("Observed: 40 live turns"));
    assert!(s.text.lines().count() <= crate::act_control::native_statement::MAX_LINES);
}

#[test]
fn a_not_ready_process_is_reported_and_nothing_is_sent_to_it() {
    let mut material = view_material(json!([]), json!([]), json!([]));
    material["state"] = json!("handshaking");
    material["notReady"] = json!("Codex is handshaking, not ready: live work cannot be observed and nothing is sent to it; only the process is stopped");
    let mut ops = Ops::new(vec![material], vec![true]);
    let out = ops.run(false).unwrap();
    assert_eq!(ops.log, ["assess", "ask", "close", "assess", "stop"], "no interrupt to a process that is not ready");
    let s = crate::act_control::native_statement::codex_stop_statement(&ops.asked[0]).unwrap();
    assert!(s.text.contains("state handshaking") && s.text.contains("nothing is sent to it; only the process is stopped."));
    assert_eq!(out["state"], "stopped");
}

#[test]
fn only_the_explicit_stop_button_proceeds() {
    use crate::act_control::native_statement::{act_buttons, chose, dialog_model, KEEP_CODEX, RESTART_CODEX, STOP_CODEX};
    for act in [STOP_CODEX, RESTART_CODEX] {
        for (how, result) in dialog_model::outcomes(&act_buttons(KEEP_CODEX, act)) {
            assert_eq!(chose(&result, act), how == "middle", "{act}: {how}");
        }
    }
}

#[cfg(unix)]
mod real_host {
    use super::*;
    use crate::hosting::{Host, HostConfig};
    use crate::runtime_session::{HomeSession, WorkflowRootSession};
    use std::path::PathBuf;
    use std::sync::Arc;

    /// interrupt-mode: `complete` (default) acknowledges and completes the turn
    /// interrupted; `silent` answers nothing; `silent-first` ignores the first
    /// interrupt and completes the others.
    const PEER: &str = r#"#!/usr/bin/python3
import sys,json,threading,time,os
if '--version' in sys.argv:
 print('codex-cli 0.160.0');sys.exit(0)
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
def mode():
 return open('interrupt-mode').read().strip() if os.path.exists('interrupt-mode') else 'complete'
interrupts=[0];starts=[0]
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log: log.write(json.dumps(f)+'\n')
 m=f.get('method')
 if m=='initialize': result={'userAgent':'unqualified-stop-fixture'}
 elif m=='thread/start':
  starts[0]+=1
  t={'id':'thread' if starts[0]==1 else 'thread-%d'%starts[0],'cliVersion':'0.160.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'stop fixture','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':'idle'},'turns':[]}
  result={'thread':t,'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
 elif m=='turn/steer': result={'turnId':f['params']['expectedTurnId']}
 elif m=='turn/interrupt':
  interrupts[0]+=1
  if mode()=='silent' or (mode()=='silent-first' and interrupts[0]==1): continue
  emit({'id':f['id'],'result':{}})
  emit({'method':'turn/completed','params':{'threadId':f['params']['threadId'],'turn':{'id':f['params']['turnId'],'status':'interrupted','items':[],'error':None,'itemsView':'summary'}}})
  continue
 else: continue
 emit({'id':f['id'],'result':result})
"#;

    struct Fixture {
        root: PathBuf,
        cfg: HostConfig,
        home: Arc<HomeSession>,
        generation: Value,
    }
    impl Fixture {
        fn new() -> Self {
            use std::os::unix::fs::PermissionsExt;
            let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("codex-stop-").unwrap());
            for name in ["account", "probe"] {
                std::fs::create_dir_all(root.join(name)).unwrap();
            }
            let peer = root.join("peer.py");
            std::fs::write(&peer, PEER).unwrap();
            std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
            let mut cfg = HostConfig::new(peer, root.join("account"), root.join("probe"), root.clone());
            cfg.allow_unverified_dev = true;
            cfg.wait_limit = Duration::from_secs(2);
            let host = Arc::new(Host::new());
            host.start(&cfg, "stop fixture").unwrap();
            let generation = host.snapshot()["generation"].clone();
            host.thread_start_selected(&root.to_string_lossy(), "fixture-model", "fixture-provider").unwrap();
            let home = Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account, host, Ok(cfg.clone())).unwrap());
            Self { root, cfg, home, generation }
        }
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
        fn live_turn(&self, id: &str) {
            self.live_turn_in("thread", id)
        }
        fn live_turn_in(&self, thread: &str, id: &str) {
            self.emit(json!({"method":"turn/started","params":{"threadId":thread,"turn":{"id":id,"status":"inProgress","items":[],"error":null,"itemsView":"summary"}}}));
            let deadline = Instant::now() + Duration::from_secs(3);
            while self.home.host.conversation_turn(&self.generation, thread, id).is_none() {
                assert!(Instant::now() < deadline, "turn/started not received");
                std::thread::sleep(Duration::from_millis(5));
            }
        }
        fn wire(&self) -> Vec<String> {
            std::fs::read_to_string(self.root.join("wire.jsonl")).unwrap_or_default().lines()
                .map(|l| serde_json::from_str::<Value>(l).unwrap()["method"].as_str().unwrap_or("").to_owned()).collect()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = self.home.host.stop("stop fixture cleanup", "test ended");
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }

    #[test]
    fn real_host_cancel_leaves_codex_running_and_writes_nothing() {
        let f = Fixture::new();
        f.live_turn("turn-1");
        let (wire, lifecycle) = (f.wire(), f.home.host.lifecycle_events().len());
        let workflows = std::sync::Mutex::new(WorkflowRootSession::default());
        let mut shown = Vec::new();
        let out = stop_native_home(&f.home, &workflows, &f.generation, false, |view| { shown.push(view.clone()); false }, || panic!("no start")).unwrap();
        assert_eq!(out["state"], "cancelled");
        assert_eq!(shown.len(), 1);
        assert_eq!(shown[0]["observedLiveTurns"][0]["turnId"], "turn-1", "the question lists the observed live turn");
        assert_eq!(f.home.host.snapshot()["state"], "ready");
        assert_eq!(f.home.host.snapshot()["generation"], f.generation);
        assert_eq!(f.wire(), wire, "nothing written to Codex");
        assert_eq!(f.home.host.lifecycle_events().len(), lifecycle, "no stop transition");
        // Not closed to new turns: an ordinary send still reaches the wire.
        let _ = f.home.host.turn_steer_text(&f.generation, "thread", "turn-1", "still open");
        assert_eq!(f.wire().last().unwrap(), "turn/steer");
    }

    #[test]
    fn real_host_closed_to_new_turns_refuses_start_and_steer_but_not_interrupt() {
        let f = Fixture::new();
        f.live_turn("turn-1");
        f.home.host.close_to_new_turns(&f.generation).unwrap();
        let wire = f.wire();
        let start = f.home.host.turn_start_text(&f.generation, "thread", "late text").unwrap_err();
        assert!(start.contains("Stop Codex was confirmed") && start.contains("turn/start"), "{start}");
        let steer = f.home.host.turn_steer_text(&f.generation, "thread", "turn-1", "late steer").unwrap_err();
        assert!(steer.contains("Stop Codex was confirmed") && steer.contains("turn/steer"), "{steer}");
        assert_eq!(f.wire(), wire, "nothing written for a refused turn or steer");
        let written = f.home.host.turn_interrupt_begin(&f.generation, "thread", "turn-1").unwrap();
        assert!(f.home.host.turn_interrupt_acknowledgment(&written, Duration::from_secs(2)).is_ok());
        assert_eq!(f.wire().last().unwrap(), "turn/interrupt", "interrupts are still sent");
        // A refused stop reopens; another process is never closed by this one.
        f.home.host.reopen_to_new_turns(&f.generation);
        f.live_turn("turn-2");
        let _ = f.home.host.turn_steer_text(&f.generation, "thread", "turn-2", "after reopen");
        assert_eq!(f.wire().last().unwrap(), "turn/steer");
        let mut other = f.generation.clone();
        other["spawnCounter"] = json!(99);
        assert!(f.home.host.close_to_new_turns(&other).is_err());
    }

    #[test]
    fn real_host_confirm_interrupts_then_stops_and_labels_the_turn() {
        let f = Fixture::new();
        f.live_turn("turn-1");
        let workflows = std::sync::Mutex::new(WorkflowRootSession::default());
        let out = stop_native_home_within(&f.home, &workflows, &f.generation, false, Duration::from_secs(3), |_| true, || panic!("no start")).unwrap();
        assert_eq!(f.wire(), ["initialize", "initialized", "thread/start", "turn/interrupt"], "one interrupt, then the input closed");
        assert_eq!(out["state"], "stopped");
        assert_eq!(out["turns"][0]["interruptRequest"]["state"], "acknowledged");
        assert_eq!(out["turns"][0]["codexReported"], "interrupted", "observed turn/completed, not the acknowledgment");
        assert_eq!(out["turns"][0]["label"], "interrupted by Stop Codex");
        assert_eq!(f.home.host.snapshot()["state"], "stopped");
        let events = f.home.host.lifecycle_events();
        let stop = events.iter().find(|e| e["transitionId"] == "LT-17").expect("deliberate stop from ready");
        assert_eq!(stop["stopRecord"]["reason"], "Stop Codex");
        assert_eq!(stop["actor"], "the person");
    }

    #[test]
    fn real_host_unanswered_first_interrupt_does_not_starve_the_second() {
        let f = Fixture::new();
        std::fs::write(f.root.join("interrupt-mode"), "silent-first").unwrap();
        // A second conversation, so each has its own live turn (one per thread).
        f.home.host.thread_start_selected(&f.root.to_string_lossy(), "fixture-model", "fixture-provider").unwrap();
        f.live_turn_in("thread", "turn-1");
        f.live_turn_in("thread-2", "turn-2");
        let workflows = std::sync::Mutex::new(WorkflowRootSession::default());
        let begin = Instant::now();
        let out = stop_native_home_within(&f.home, &workflows, &f.generation, false, Duration::from_millis(800), |_| true, || panic!("no start")).unwrap();
        // The stop wait limit, then at most HOSTING's grace and exit wait.
        assert!(begin.elapsed() < Duration::from_millis(800) + Duration::from_secs(7));
        assert_eq!(f.wire().iter().filter(|m| *m == "turn/interrupt").count(), 2, "both interrupts written");
        let turns = out["turns"].as_array().unwrap();
        let by = |id: &str| turns.iter().find(|t| t["turnId"] == id).unwrap().clone();
        // Turns are listed in a stable order, so turn-1's interrupt is written
        // first, and the peer ignores the first interrupt it receives.
        assert_eq!(turns[0]["turnId"], "turn-1");
        let (silent, answered) = (by("turn-1"), by("turn-2"));
        assert_eq!(silent["interruptRequest"]["state"], "sent; not acknowledged");
        assert_eq!(silent["label"], "interrupted by Stop Codex (final status not observed)");
        assert_eq!(answered["interruptRequest"]["state"], "acknowledged");
        assert_eq!(answered["label"], "interrupted by Stop Codex");
        assert_eq!(f.home.host.snapshot()["state"], "stopped");
    }

    #[test]
    fn real_host_restart_starts_a_new_process_and_continues_no_conversation() {
        let f = Fixture::new();
        f.live_turn("turn-1");
        let workflows = std::sync::Mutex::new(WorkflowRootSession::default());
        let host = f.home.host.clone();
        let cfg = f.cfg.clone();
        let out = stop_native_home_within(&f.home, &workflows, &f.generation, true, Duration::from_secs(3), |view| view["restart"] == true, move || host.start(&cfg, "the person: Restart Codex")).unwrap();
        assert_eq!(out["start"]["state"], "started");
        let now = f.home.host.snapshot();
        assert_eq!(now["state"], "ready");
        assert_ne!(now["generation"], f.generation, "a new Codex process");
        assert_eq!(out["start"]["codex"]["generation"], now["generation"]);
        let current = now["threads"].as_array().unwrap().iter().filter(|t| t["generation"] == now["generation"]).count();
        assert_eq!(current, 0, "no conversation is loaded in the new process until the person continues one");
        assert_eq!(f.wire(), ["initialize", "initialized", "thread/start", "turn/interrupt", "initialize", "initialized"], "no thread/resume or other request after the restart");
    }

    #[test]
    fn real_host_refuses_a_changed_or_stopped_generation_without_asking() {
        let f = Fixture::new();
        let workflows = std::sync::Mutex::new(WorkflowRootSession::default());
        let mut other = f.generation.clone();
        other["spawnCounter"] = json!(99);
        let refused = stop_native_home(&f.home, &workflows, &other, false, |_| panic!("not asked"), || panic!("no start")).unwrap_err();
        assert!(refused.contains("Nothing stopped"));
        assert_eq!(f.home.host.snapshot()["state"], "ready");
        f.home.host.stop("fixture", "stopped elsewhere").unwrap();
        let refused = stop_native_home(&f.home, &workflows, &f.generation, true, |_| panic!("not asked"), || panic!("no start")).unwrap_err();
        assert!(refused.contains("not running") && refused.contains("use Start Codex"));
    }
}
