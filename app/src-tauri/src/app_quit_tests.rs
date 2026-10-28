//! K-4 / SQ-Q quit sequence and the DEF-1 window rules, against doubles;
//! the real-Host cases are in `codex_stop_tests.rs` (`real_host_quit_*`).
use super::*;
use serde_json::json;

fn material(turns: &[&str], requests: usize, children: usize) -> Value {
    let g = json!({"appSession":"s","home":"h","spawnCounter":1});
    merge(
        vec![(json!({"modeHomeClass":"account","generation":g,"state":"ready"}), json!({
            "observedLiveTurns": turns.iter().map(|t| json!({"generation":g,"threadId":"thread","turnId":t,"status":"inProgress"})).collect::<Vec<_>>(),
            "observedOutstandingRequests": (0..requests).map(|i| json!({"generation":g,"requestIdentity":i,"method":"item/commandExecution/requestApproval","threadId":"thread"})).collect::<Vec<_>>(),
            "observedActiveChildren": (0..children).map(|i| json!({"generation":g,"threadId":format!("child-{i}"),"parentThreadId":"thread","reportedStatus":"running"})).collect::<Vec<_>>(),
        }))],
        vec![],
        vec![],
    )
}

/// A scripted world: successive assessments, the person's answers, and a log
/// of every call in order.
struct Double {
    materials: Vec<Value>,
    answers: Vec<Result<bool, String>>,
    log: Vec<String>,
    shown: Vec<Value>,
    ended: bool,
}
impl Double {
    fn new(materials: Vec<Value>, answers: Vec<Result<bool, String>>) -> Self {
        Self { materials, answers, log: vec![], shown: vec![], ended: true }
    }
    fn run(&mut self) -> Decision {
        quit_sequence(self, Duration::from_millis(200))
    }
}
impl Interrupts for Double {
    type Pending = String;
    fn interrupt(&mut self, turn: &Value) -> Result<String, String> {
        let id = turn["turnId"].as_str().unwrap().to_owned();
        self.log.push(format!("interrupt {id}"));
        Ok(id)
    }
    fn acknowledgment(&mut self, pending: &String, _wait: Duration) -> Result<Value, String> {
        self.log.push(format!("ack {pending}"));
        Ok(json!({"result":{}}))
    }
    fn turn_reading(&mut self, _turn: &Value) -> Option<Value> {
        self.ended.then(|| json!({"terminalEventObserved":true,"nativeTurn":{"status":"interrupted"}}))
    }
}
impl QuitOps for Double {
    fn assess(&mut self) -> Assessment {
        self.log.push("assess".into());
        let m = if self.materials.len() > 1 { self.materials.remove(0) } else { self.materials[0].clone() };
        Assessment::new(m)
    }
    fn record_requested(&mut self, material: &Value) -> Value {
        self.log.push(format!("quit_requested {}", material["observedLiveTurns"].as_array().map_or(0, Vec::len)));
        json!({"state":"recorded"})
    }
    fn confirm(&mut self, view: &Value) -> Result<bool, String> {
        self.log.push("ask".into());
        self.shown.push(view.clone());
        self.answers.remove(0)
    }
    fn record_answered(&mut self, confirmed: bool) -> Value {
        self.log.push(format!("quit_answered {}", if confirmed { "confirmed" } else { "cancelled" }));
        json!({"state":"recorded"})
    }
    fn close_to_new_turns(&mut self) {
        self.log.push("close".into());
    }
    fn reopen_to_new_turns(&mut self) {
        self.log.push("reopen".into());
    }
    fn stop_record(&mut self, turn: &Value) -> Value {
        json!({"stopRequestId":format!("stop:{}",turn["turnId"].as_str().unwrap()),"state":"settled","cause":"quit"})
    }
}

#[test]
fn nothing_live_records_empty_lists_asks_nothing_and_quits() {
    let mut d = Double::new(vec![material(&[], 0, 0)], vec![]);
    let Decision::Quit(out) = d.run() else { panic!("AS-03 quits") };
    assert_eq!(d.log, ["assess", "quit_requested 0", "close", "assess"], "AS-03: closed to new turns, assessed again, nothing asked or sent");
    assert_eq!(out["asked"], false);
    assert_eq!(out["stopRequests"], json!([]));
}

#[test]
fn work_started_before_the_as03_close_is_asked() {
    let mut d = Double::new(vec![material(&[], 0, 0), material(&["turn-1"], 0, 0), material(&["turn-1"], 0, 0)], vec![Ok(false)]);
    assert!(matches!(d.run(), Decision::Cancelled(_)));
    assert_eq!(d.log, ["assess", "quit_requested 0", "close", "assess", "reopen", "quit_requested 1", "ask", "reopen", "quit_answered cancelled"]);
}

#[test]
fn quit_and_codex_stop_admit_one_another_only_when_neither_is_under_way() {
    let (quit, stop_gate) = (AppQuit::default(), Mutex::new(()));
    let restart = stop_gate.lock().unwrap();
    assert!(admit_quit(&quit, &stop_gate).unwrap_err().contains("Stop or Restart Codex is under way"), "a quit during Stop/Restart is refused");
    assert!(!quit.busy(), "a refused quit holds nothing");
    drop(restart);
    let held = admit_quit(&quit, &stop_gate).unwrap();
    assert!(admit_codex_stop(&quit).is_err(), "Stop/Restart is refused while a quit is under way");
    assert!(crate::codex_stop::question_gate(&stop_gate).is_err(), "and its gate is held");
    assert!(admit_quit(&quit, &stop_gate).unwrap_err().contains("already open"));
    drop(held);
    assert!(admit_codex_stop(&quit).is_ok());
}

#[test]
fn codex_stop_is_refused_after_a_decided_quit_releases_its_guards() {
    // The quit thread drops its guards right after asking the App to exit,
    // before `RunEvent::Exit`; Stop/Restart must stay refused meanwhile.
    let (quit, stop_gate) = (AppQuit::default(), Mutex::new(()));
    let held = admit_quit(&quit, &stop_gate).unwrap();
    assert!(quit.allow(&Decision::Quit(json!({"stopRequests":["stop:a"]}))));
    drop(held);
    assert!(!quit.busy(), "the guards are released");
    let refused = admit_codex_stop(&quit).unwrap_err();
    assert!(refused.contains("quitting") && refused.contains("Stop or Restart Codex was not started"), "{refused}");
}

#[test]
fn busy_reads_a_flag_and_never_makes_a_quit_find_the_gate_taken() {
    let quit = AppQuit::default();
    assert!(!quit.busy());
    let guard = quit.gate().expect("gate");
    assert!(quit.busy(), "busy while a question guard is alive");
    assert!(quit.gate().is_none(), "a second question is not opened while one is");
    drop(guard);
    assert!(!quit.busy(), "not busy once the guard is dropped");
    // A Quit pressed while Stop/Restart Codex probes `busy()` must always get
    // the gate: poll `busy()` continuously while opening the gate many times.
    let stop = std::sync::atomic::AtomicBool::new(false);
    let polls = std::sync::atomic::AtomicUsize::new(0);
    std::thread::scope(|s| {
        s.spawn(|| {
            while !stop.load(std::sync::atomic::Ordering::SeqCst) {
                let _ = quit.busy();
                polls.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            }
        });
        while polls.load(std::sync::atomic::Ordering::SeqCst) == 0 {
            std::thread::yield_now();
        }
        let mut dropped = 0;
        for _ in 0..200_000 {
            match quit.gate() {
                Some(guard) => drop(guard),
                None => dropped += 1,
            }
        }
        stop.store(true, std::sync::atomic::Ordering::SeqCst);
        assert_eq!(dropped, 0, "a Quit was found the gate taken by a busy() probe {dropped} times");
    });
}

#[test]
fn keep_running_or_cancel_records_cancelled_and_changes_nothing() {
    let mut d = Double::new(vec![material(&["turn-1"], 1, 1)], vec![Ok(false)]);
    let Decision::Cancelled(out) = d.run() else { panic!("AS-05 keeps running") };
    assert_eq!(d.log, ["assess", "quit_requested 1", "ask", "reopen", "quit_answered cancelled"]);
    assert!(!d.log.iter().any(|l| l.starts_with("interrupt") || l == "close"), "nothing closed or sent");
    assert_eq!(d.shown[0]["observedLiveTurns"][0]["turnId"], "turn-1", "the question lists live turns");
    assert_eq!(d.shown[0]["observedOutstandingRequests"].as_array().unwrap().len(), 1, "and waiting requests");
    assert_eq!(d.shown[0]["observedActiveChildren"].as_array().unwrap().len(), 1, "and delegated agents");
    assert_eq!(out["state"], "cancelled");
    let mut app = AppQuit::default();
    assert!(!app.allow(&Decision::Cancelled(out)));
    assert!(app.proceeding().is_none(), "a cancel never lets the App exit");
    let _ = &mut app;
}

#[test]
fn a_question_that_cannot_be_shown_records_no_answer_and_keeps_running() {
    let mut d = Double::new(vec![material(&["turn-1"], 0, 0)], vec![Err("statement refused".into())]);
    let decision = d.run();
    assert!(matches!(decision, Decision::NotAsked(_)), "{decision:?}");
    assert!(!d.log.iter().any(|l| l.starts_with("quit_answered") || l.starts_with("interrupt")), "{:?}", d.log);
    assert!(!AppQuit::default().allow(&decision));
}

#[test]
fn confirm_records_the_answer_before_each_quit_interrupt_and_names_the_stop_requests() {
    let m = material(&["turn-1", "turn-2"], 1, 0);
    let mut d = Double::new(vec![m.clone(), m], vec![Ok(true)]);
    let decision = d.run();
    assert_eq!(d.log, ["assess", "quit_requested 2", "ask", "close", "assess", "quit_answered confirmed", "interrupt turn-1", "interrupt turn-2", "ack turn-1", "ack turn-2"],
        "SR-01 for every turn after the recorded answer and before any wait");
    let app = AppQuit::default();
    assert!(app.allow(&decision));
    assert_eq!(app.proceeding(), Some(vec!["stop:turn-1".to_owned(), "stop:turn-2".to_owned()]));
    let Decision::Quit(out) = decision else { unreachable!() };
    assert_eq!(out["turns"][0]["codexReported"], "interrupted");
}

#[test]
fn a_list_changed_while_asking_is_recorded_and_asked_again() {
    let (a, b) = (material(&["turn-1"], 0, 0), material(&["turn-1", "turn-2"], 0, 0));
    let mut d = Double::new(vec![a, b.clone(), b], vec![Ok(true), Ok(true)]);
    assert!(matches!(d.run(), Decision::Quit(_)));
    assert_eq!(d.log, ["assess", "quit_requested 1", "ask", "close", "assess", "reopen", "quit_requested 2", "ask", "close", "assess", "quit_answered confirmed", "interrupt turn-1", "interrupt turn-2", "ack turn-1", "ack turn-2"]);
    assert_eq!(d.shown[1]["changedWhileAsking"], true);
    // A cancel on the second question changes nothing.
    let (a, b) = (material(&["turn-1"], 0, 0), material(&["turn-1", "turn-2"], 0, 0));
    let mut d = Double::new(vec![a, b], vec![Ok(true), Ok(false)]);
    assert!(matches!(d.run(), Decision::Cancelled(_)));
    assert!(!d.log.iter().any(|l| l.starts_with("interrupt")));
    assert_eq!(d.log.last().unwrap(), "quit_answered cancelled");
}

#[test]
fn work_that_ended_while_asking_needs_no_second_question() {
    let mut d = Double::new(vec![material(&["turn-1"], 0, 0), material(&[], 0, 0)], vec![Ok(true)]);
    assert!(matches!(d.run(), Decision::Quit(_)));
    assert_eq!(d.log.iter().filter(|l| *l == "ask").count(), 1);
    assert!(!d.log.iter().any(|l| l.starts_with("interrupt")));
}

#[test]
fn an_unsettled_turn_waits_only_until_the_quit_wait_limit() {
    let m = material(&["turn-1"], 0, 0);
    let mut d = Double::new(vec![m.clone(), m], vec![Ok(true)]);
    d.ended = false;
    let started = Instant::now();
    let Decision::Quit(out) = d.run() else { panic!() };
    assert!(started.elapsed() >= Duration::from_millis(200) && started.elapsed() < Duration::from_secs(5));
    assert!(out["turns"][0]["codexReported"].is_null(), "not observed ended");
}

#[test]
fn live_work_guard_counts_unknowns_but_not_runs_alone() {
    assert!(!has_live_work(&material(&[], 0, 0)));
    assert!(has_live_work(&material(&["t"], 0, 0)));
    assert!(has_live_work(&material(&[], 1, 0)));
    assert!(has_live_work(&material(&[], 0, 1)));
    let mut m = material(&[], 0, 0);
    m["knownChildActivityUnknown"] = json!([{"threadId":"c"}]);
    assert!(has_live_work(&m), "a child of unknown activity asks");
    let mut m = material(&[], 0, 0);
    m["assessmentLimits"] = json!(["account: assessment failed"]);
    assert!(has_live_work(&m), "a ready home not assessed asks");
    let mut m = material(&[], 0, 0);
    m["runsInForce"] = json!([{"run":"run:x"}]);
    assert!(!has_live_work(&m), "a run in force alone asks nothing: quit ends no run");
}

#[test]
fn exit_requests_and_session_end() {
    assert_eq!(on_exit_requested(true, None), ExitAction::Allow);
    assert_eq!(on_exit_requested(true, Some(0)), ExitAction::Allow);
    assert_eq!(on_exit_requested(false, None), ExitAction::Keep, "the last window going away is DEF-1, not quit");
    assert_eq!(on_exit_requested(false, Some(0)), ExitAction::AskQuit, "an undecided exit asks first");
    assert_eq!(session_end(None, &[]), ("system-terminated", vec![]));
    let records = [json!({"stopRequestId":"stop:a","state":"sent"}), json!({"stopRequestId":"stop:a","state":"outcome-unknown"}), json!({"stopRequestId":"stop:b","state":"settled"})];
    assert_eq!(session_end(Some(vec!["stop:a".into()]), &records), ("quit", vec![json!({"stopRequestId":"stop:a","state":"outcome-unknown"})]));
}

#[test]
fn one_quit_question_at_a_time() {
    let app = AppQuit::default();
    let first = app.gate();
    assert!(first.is_some());
    assert!(app.gate().is_none());
    drop(first);
    assert!(app.gate().is_some());
}

#[test]
fn waiting_indicator_counts_current_outstanding_supplier_requests_only() {
    let g = json!({"appSession":"s","home":"h","spawnCounter":2});
    let old = json!({"appSession":"s","home":"h","spawnCounter":1});
    let a = json!({"generation":g,"serverRequests":[
        {"generation":g,"state":"outstanding","nativeParameters":{"threadId":"t1"}},
        {"generation":g,"state":"outstanding","nativeParameters":{"threadId":"t2"}},
        {"generation":g,"state":"answered","nativeParameters":{"threadId":"t3"}},
        {"generation":old,"state":"outstanding","nativeParameters":{"threadId":"t4"}}]});
    let k = json!({"appSession":"s","home":"k","spawnCounter":1});
    let b = json!({"generation":k,"serverRequests":[{"generation":k,"state":"outstanding","nativeParameters":{"threadId":"t1"}}]});
    assert_eq!(waiting_requests(&[a, b]), json!({"count":3,"conversations":["t1","t2"]}));
    assert_eq!(waiting_requests(&[json!({"generation":null,"serverRequests":[{"generation":null,"state":"outstanding"}]})])["count"], 0);
}

#[test]
fn only_the_explicit_quit_button_proceeds() {
    use crate::act_control::native_statement::{act_buttons, chose, dialog_model, KEEP_RUNNING, QUIT_APP};
    for (how, result) in dialog_model::outcomes(&act_buttons(KEEP_RUNNING, QUIT_APP)) {
        assert_eq!(chose(&result, QUIT_APP), how == "middle", "{how}");
    }
}

#[test]
fn the_question_lists_every_item_or_names_the_assessment() {
    use crate::act_control::native_statement::quit_statement;
    let mut m = material(&["turn-1"], 1, 1);
    m["runsInForce"] = json!([{"workflow":{"name":"wf"},"run":"run:1","conversation":"thread","state":"open"}]);
    let view = Assessment::new(m).view;
    let text = quit_statement(&view).unwrap().text;
    for needle in ["Live turn: thread / turn-1", "Outstanding request:", "Active child: child-0", "Workflow run in force: wf", "quitting ends no run", "Keep running (the default)"] {
        assert!(text.contains(needle), "{needle} missing: {text}");
    }
    let many = material(&(0..400).map(|i| Box::leak(format!("turn-{i}").into_boxed_str()) as &str).collect::<Vec<_>>(), 0, 0);
    let long = quit_statement(&Assessment::new(many).view).unwrap();
    assert!(long.in_app.is_some(), "a long list is shown in full in the App and named by digest");
}
