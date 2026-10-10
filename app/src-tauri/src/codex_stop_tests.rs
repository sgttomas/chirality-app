//! Stop Codex / Restart Codex: the sequence through `stop_or_restart` with
//! recording doubles, the native question text, and the real Host binding
//! (`stop_native_home_within`) against an owned app-server peer. The peer is a
//! fixture; it establishes no supplier behaviour.
use super::*;
use std::cell::RefCell;

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

/// Records every operation in order; turn endings come from `ends`.
struct Ops {
    log: RefCell<Vec<String>>,
    materials: RefCell<Vec<Value>>,
    answers: RefCell<Vec<bool>>,
    asked: RefCell<Vec<Value>>,
}
impl Ops {
    fn new(materials: Vec<Value>, answers: Vec<bool>) -> Self {
        Self { log: RefCell::new(vec![]), materials: RefCell::new(materials), answers: RefCell::new(answers), asked: RefCell::new(vec![]) }
    }
    fn run(&self, restart: bool, stop_ok: bool, ends: impl Fn(&str) -> Option<Value>) -> Result<Value, String> {
        stop_or_restart(
            restart,
            Duration::from_millis(150),
            || {
                self.log.borrow_mut().push("assess".into());
                let mut m = self.materials.borrow_mut();
                let next = if m.len() > 1 { m.remove(0) } else { m[0].clone() };
                Ok(Assessment::new(next, restart))
            },
            |view| {
                self.log.borrow_mut().push("ask".into());
                self.asked.borrow_mut().push(view.clone());
                self.answers.borrow_mut().remove(0)
            },
            |turn, wait| {
                assert!(wait <= Duration::from_millis(150), "each interrupt is bounded by the stop wait limit");
                self.log.borrow_mut().push(format!("interrupt {}", turn["turnId"].as_str().unwrap()));
                Ok(json!({"id":1,"result":{}}))
            },
            |turn| ends(turn["turnId"].as_str().unwrap()),
            || {
                self.log.borrow_mut().push("stop".into());
                if stop_ok { Ok(json!({"state":"stopped"})) } else { Err("stop not accepted in state stopping".into()) }
            },
            || {
                self.log.borrow_mut().push("start".into());
                Ok(json!({"state":"ready"}))
            },
        )
    }
    fn log(&self) -> Vec<String> {
        self.log.borrow().clone()
    }
}

#[test]
fn cancel_leaves_codex_running_and_sends_nothing() {
    for restart in [false, true] {
        let ops = Ops::new(vec![view_material(json!([live("t1")]), json!([{"method":"item/tool/requestUserInput","requestIdentity":7,"threadId":"thread"}]), json!([]))], vec![false]);
        let out = ops.run(restart, true, |_| None).unwrap();
        assert_eq!(out["state"], "cancelled");
        assert!(out["reading"].as_str().unwrap().contains("Nothing was interrupted, stopped or sent"));
        assert_eq!(ops.log(), ["assess", "ask"], "cancel: no interrupt, no stop, no start");
        assert_eq!(ops.asked.borrow()[0]["observedLiveTurns"][0]["turnId"], "t1", "the question showed the live turn");
    }
}

#[test]
fn confirm_interrupts_each_live_turn_then_stops_with_labels_from_turn_status_only() {
    let ops = Ops::new(vec![view_material(json!([live("t1"), live("t2"), live("t3"), live("t4")]), json!([]), json!([]))], vec![true]);
    let out = ops.run(false, true, |turn| match turn {
        "t1" => ended("interrupted"),
        "t2" => ended("completed"),
        "t3" => ended("failed"),
        _ => None,
    }).unwrap();
    assert_eq!(ops.log(), ["assess", "ask", "assess", "interrupt t1", "interrupt t2", "interrupt t3", "interrupt t4", "stop"], "interrupts are requested before the stop");
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
fn all_turns_ended_before_the_limit_stop_without_waiting_it_out() {
    let ops = Ops::new(vec![view_material(json!([live("t1")]), json!([]), json!([]))], vec![true]);
    let begin = Instant::now();
    let out = ops.run(false, true, |_| ended("interrupted")).unwrap();
    assert!(begin.elapsed() < Duration::from_millis(140));
    assert!(out["historyNote"].is_null());
    assert_eq!(out["turns"][0]["codexReported"], "interrupted");
}

#[test]
fn no_live_work_is_a_simple_confirmation_and_sends_no_interrupt() {
    let ops = Ops::new(vec![view_material(json!([]), json!([]), json!([]))], vec![true]);
    let out = ops.run(false, true, |_| None).unwrap();
    assert_eq!(ops.log(), ["assess", "ask", "assess", "stop"]);
    assert_eq!(out["turns"], json!([]));
    let statement = crate::act_control::native_statement::codex_stop_statement(&ops.asked.borrow()[0]).unwrap();
    assert!(statement.in_app.is_none());
    assert!(statement.text.starts_with("Stop Codex for this home?"));
    assert!(statement.text.contains("Observed: no live turns, waiting requests, delegated agents or workflow runs in force."));
    assert!(statement.text.contains("Stop Codex stops this Codex process."));
    assert!(!statement.text.contains("interrupts each live turn"), "no interrupt wording without live work");
    assert!(statement.text.contains("Keep Codex running (the default) and Cancel change nothing"));
}

#[test]
fn live_work_changing_while_asked_asks_again_with_the_current_list() {
    let first = view_material(json!([live("t1")]), json!([]), json!([]));
    let second = view_material(json!([live("t1"), live("t2")]), json!([]), json!([]));
    let ops = Ops::new(vec![first, second.clone(), second], vec![true, false]);
    let out = ops.run(false, true, |_| None).unwrap();
    assert_eq!(out["state"], "cancelled");
    assert_eq!(ops.log(), ["assess", "ask", "assess", "ask"], "the changed list is asked again; nothing sent");
    let asked = ops.asked.borrow();
    assert_eq!(asked[1]["changedWhileAsking"], true);
    assert_eq!(asked[1]["observedLiveTurns"].as_array().unwrap().len(), 2);
    assert!(crate::act_control::native_statement::codex_stop_statement(&asked[1]).unwrap().text.contains("Live work changed while this question was open"));
}

#[test]
fn an_assessment_failing_after_confirm_stops_nothing() {
    let ops = Ops::new(vec![view_material(json!([live("t1")]), json!([]), json!([]))], vec![true]);
    let calls = RefCell::new(0);
    let result = stop_or_restart(false, Duration::from_millis(50),
        || { *calls.borrow_mut() += 1; if *calls.borrow() == 1 { Ok(Assessment::new(ops.materials.borrow()[0].clone(), false)) } else { Err("Codex changed since this view".into()) } },
        |_| true,
        |_, _| panic!("no interrupt after a failed reassessment"),
        |_| None,
        || panic!("no stop after a failed reassessment"),
        || panic!("no start"));
    assert!(result.unwrap_err().contains("Nothing was interrupted or stopped"));
}

#[test]
fn restart_starts_once_after_the_stop_and_continues_no_conversation() {
    let ops = Ops::new(vec![view_material(json!([live("t1")]), json!([]), json!([]))], vec![true]);
    let out = ops.run(true, true, |_| ended("interrupted")).unwrap();
    assert_eq!(ops.log(), ["assess", "ask", "assess", "interrupt t1", "stop", "start"], "start follows the stop; no resume or other operation");
    assert_eq!(out["action"], "Restart Codex");
    assert_eq!(out["start"]["state"], "started");
    assert!(out["conversations"].as_str().unwrap().contains("No conversation was continued automatically"));
    assert_eq!(out["turns"][0]["label"], "interrupted by Stop Codex", "Restart's interrupts carry cause codex-stop");
    // A refused stop does not start a second process.
    let ops = Ops::new(vec![view_material(json!([live("t1")]), json!([]), json!([]))], vec![true]);
    let out = ops.run(true, false, |_| None).unwrap();
    assert_eq!(ops.log(), ["assess", "ask", "assess", "interrupt t1", "stop"]);
    assert_eq!(out["state"], "stop refused");
    assert_eq!(out["start"]["state"], "not started");
    assert_eq!(out["turns"][0]["label"], "outcome unknown (Stop Codex requested)", "not stopped and not observed ended");
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
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log: log.write(json.dumps(f)+'\n')
 m=f.get('method')
 if m=='initialize': result={'userAgent':'unqualified-stop-fixture'}
 elif m=='thread/start':
  t={'id':'thread','cliVersion':'0.160.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'stop fixture','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':'idle'},'turns':[]}
  result={'thread':t,'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
 elif m=='turn/interrupt':
  if mode()=='silent': continue
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
            std::fs::rename(tmp, self.root.join("queued-event.json")).unwrap();
        }
        fn live_turn(&self, id: &str) {
            self.emit(json!({"method":"turn/started","params":{"threadId":"thread","turn":{"id":id,"status":"inProgress","items":[],"error":null,"itemsView":"summary"}}}));
            let deadline = Instant::now() + Duration::from_secs(3);
            while self.home.host.conversation_turn(&self.generation, "thread", id).is_none() {
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
    fn real_host_unanswered_interrupt_still_stops_within_the_limit() {
        let f = Fixture::new();
        std::fs::write(f.root.join("interrupt-mode"), "silent").unwrap();
        f.live_turn("turn-1");
        let workflows = std::sync::Mutex::new(WorkflowRootSession::default());
        let begin = Instant::now();
        let out = stop_native_home_within(&f.home, &workflows, &f.generation, false, Duration::from_millis(600), |_| true, || panic!("no start")).unwrap();
        // The stop wait limit, then at most HOSTING's grace and exit wait.
        assert!(begin.elapsed() < Duration::from_millis(600) + Duration::from_secs(7));
        assert_eq!(out["turns"][0]["interruptRequest"]["state"], "not acknowledged");
        assert_eq!(out["turns"][0]["label"], "interrupted by Stop Codex (final status not observed)");
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
        let wire = f.wire();
        assert_eq!(wire, ["initialize", "initialized", "thread/start", "turn/interrupt", "initialize", "initialized"], "no thread/resume or other request after the restart");
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
