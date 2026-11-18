//! K-4 / SQ-Q quit sequence and the DEF-1 window rules, against doubles;
//! the real-Host cases are in `codex_stop_tests.rs` (`real_host_quit_*`).
use super::*;

#[test]
fn native_exit_permission_requires_settlement_and_failure_is_retryable() {
    let app = AppQuit::default();
    let decision = Decision::Quit(json!({"stopRequests":["stop:pending"]}));
    let failure = app.allow(&decision, |ids| {
        assert_eq!(ids, &["stop:pending"]);
        assert!(app.proceeding().is_none(), "no native exit permission during settlement");
        Err("original reserved group census unavailable".into())
    }).unwrap_err();
    assert!(failure.contains("census unavailable"));
    assert!(app.proceeding().is_none());
    assert_eq!(on_exit_requested(false, Some(0)), ExitAction::AskQuit);
    assert!(app.allow(&decision, |_| Ok(json!({"write":"unknown","limit":"ledger unavailable"}))).unwrap(),
        "Q-7 recording failure does not block an actually settled exit");
    assert_eq!(app.proceeding(), Some(vec!["stop:pending".into()]));
}
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
    settlement: Result<Value, String>,
}
impl Double {
    fn new(materials: Vec<Value>, answers: Vec<Result<bool, String>>) -> Self {
        Self { materials, answers, log: vec![], shown: vec![], ended: true, settlement: Ok(Value::Null) }
    }
    fn run(&mut self) -> Decision {
        quit_sequence(self, Duration::from_millis(200))
    }
}
impl Interrupts for Double {
    type Pending = String;
    fn interrupt(&mut self, turn: &Value, _deadline: Instant) -> Result<String, crate::codex_stop::Unsent> {
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
    fn settle(&mut self, _stop_requests: &[String]) -> Result<Value, String> {
        self.log.push("settle".into());
        self.settlement.clone()
    }
    fn roster(&self) -> Vec<Arc<HomeSession>> {
        vec![]
    }
    fn lift_settlement_fences(&mut self) {
        self.log.push("lift".into());
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
    assert!(quit.allow(&Decision::Quit(json!({"stopRequests":["stop:a"]})), |_| Ok(Value::Null)).unwrap());
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
    assert!(!app.allow(&Decision::Cancelled(out), |_| panic!("cancel cannot settle")).unwrap());
    assert!(app.proceeding().is_none(), "a cancel never lets the App exit");
    let _ = &mut app;
}

#[test]
fn a_question_that_cannot_be_shown_records_no_answer_and_keeps_running() {
    let mut d = Double::new(vec![material(&["turn-1"], 0, 0)], vec![Err("statement refused".into())]);
    let decision = d.run();
    assert!(matches!(decision, Decision::NotAsked(_)), "{decision:?}");
    assert!(!d.log.iter().any(|l| l.starts_with("quit_answered") || l.starts_with("interrupt")), "{:?}", d.log);
    assert!(!AppQuit::default().allow(&decision, |_| Ok(Value::Null)).unwrap());
}

#[test]
fn confirm_records_the_answer_before_each_quit_interrupt_and_names_the_stop_requests() {
    let m = material(&["turn-1", "turn-2"], 1, 0);
    let mut d = Double::new(vec![m.clone(), m], vec![Ok(true)]);
    let decision = d.run();
    assert_eq!(d.log, ["assess", "quit_requested 2", "ask", "close", "assess", "quit_answered confirmed", "interrupt turn-1", "interrupt turn-2", "ack turn-1", "ack turn-2"],
        "SR-01 for every turn after the recorded answer and before any wait");
    let app = AppQuit::default();
    assert!(app.allow(&decision, |_| Ok(Value::Null)).unwrap());
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

/// The quit path every route runs (`run_quit`) and what the App does with
/// the system's request to quit (`on_system_quit_request`,
/// `handle_system_quit_request`), driven with doubles; the roster test uses
/// real `HomeSession`s over unstarted Hosts and the production `HostQuit`.
mod system_quit_routes {
    use super::*;
    use std::cell::{Cell, RefCell};
    use std::sync::atomic::AtomicUsize;
    use std::sync::mpsc;

    /// The Double borrowed, so that its log can be read after `run_quit`.
    /// `before_confirm` lets a test hold the question open; `fault` panics
    /// at the named step, as a poisoned Host lock would.
    struct Borrowed<'a> {
        d: &'a mut Double,
        before_confirm: Option<Box<dyn FnMut() + Send + 'a>>,
        fault: Option<&'static str>,
    }
    impl<'a> Borrowed<'a> {
        fn new(d: &'a mut Double) -> Self {
            Self { d, before_confirm: None, fault: None }
        }
        fn at(&self, step: &str) {
            if self.fault == Some(step) {
                panic!("injected fault at {step}");
            }
        }
    }
    impl Interrupts for Borrowed<'_> {
        type Pending = String;
        fn interrupt(&mut self, turn: &Value, deadline: Instant) -> Result<String, crate::codex_stop::Unsent> { self.d.interrupt(turn, deadline) }
        fn acknowledgment(&mut self, pending: &String, wait: Duration) -> Result<Value, String> { self.d.acknowledgment(pending, wait) }
        fn turn_reading(&mut self, turn: &Value) -> Option<Value> { self.d.turn_reading(turn) }
    }
    impl QuitOps for Borrowed<'_> {
        fn assess(&mut self) -> Assessment { self.at("assess"); self.d.assess() }
        fn record_requested(&mut self, material: &Value) -> Value { self.d.record_requested(material) }
        fn confirm(&mut self, view: &Value) -> Result<bool, String> {
            if let Some(hold) = self.before_confirm.as_mut() { hold() }
            self.d.confirm(view)
        }
        fn record_answered(&mut self, confirmed: bool) -> Value { self.d.record_answered(confirmed) }
        fn close_to_new_turns(&mut self) { self.d.close_to_new_turns() }
        fn reopen_to_new_turns(&mut self) { self.d.reopen_to_new_turns() }
        fn stop_record(&mut self, turn: &Value) -> Value { self.d.stop_record(turn) }
        fn settle(&mut self, ids: &[String]) -> Result<Value, String> { self.at("settle"); self.d.settle(ids) }
        fn roster(&self) -> Vec<Arc<HomeSession>> { self.d.roster() }
        fn lift_settlement_fences(&mut self) { self.d.lift_settlement_fences() }
    }

    /// The App's three gates.
    #[derive(Default)]
    struct Held {
        quit: AppQuit,
        stop_gate: Mutex<()>,
        key_setup: Mutex<()>,
    }
    impl Held {
        fn gates(&self) -> QuitGates<'_> {
            QuitGates { quit: &self.quit, stop_gate: &self.stop_gate, key_setup: &self.key_setup }
        }
    }
    /// What one run did: its ending, what the person was told and how many
    /// exits it asked for.
    struct Ran {
        ending: QuitEnding,
        told: Vec<String>,
        exits: usize,
    }
    fn run_with(held: &Held, route: QuitRoute, ops: Borrowed<'_>) -> Ran {
        let told = RefCell::new(Vec::new());
        let exits = Cell::new(0);
        let ending = run_quit(held.gates(), route, Duration::from_millis(50), || ops, |_, message| told.borrow_mut().push(message), || exits.set(exits.get() + 1));
        Ran { ending, told: told.into_inner(), exits: exits.get() }
    }
    fn run(held: &Held, route: QuitRoute, d: &mut Double) -> Ran {
        run_with(held, route, Borrowed::new(d))
    }
    fn live() -> Value {
        material(&["turn-1"], 1, 1)
    }

    #[test]
    fn the_system_request_decision_for_every_combination() {
        use SystemQuitRequest::*;
        assert_eq!(on_system_quit_request(false, false), StartQuit);
        assert_eq!(on_system_quit_request(false, true), UnderWay);
        assert_eq!(on_system_quit_request(true, false), Decided);
        assert_eq!(on_system_quit_request(true, true), Decided);
    }

    #[test]
    fn the_system_request_starts_the_quit_path_only_when_none_is_under_way_or_decided() {
        for (held, starts) in [((false, false), true), ((false, true), false), ((true, false), false), ((true, true), false)] {
            let mut started = 0;
            let request = handle_system_quit_request(|| held, || started += 1);
            assert_eq!((request.is_some(), started), (true, usize::from(starts)), "{held:?}");
        }
    }

    #[test]
    fn a_fault_in_the_system_request_starts_nothing_and_is_caught() {
        let mut started = false;
        assert_eq!(handle_system_quit_request(|| panic!("injected fault reading the App's state"), || started = true), None);
        assert!(!started);
        assert_eq!(handle_system_quit_request(|| (false, false), || panic!("injected fault starting the quit")), None, "a fault while starting is caught too");
        assert_eq!(handle_system_quit_request(|| (false, false), || {}), Some(SystemQuitRequest::StartQuit), "the next request is handled normally");
    }

    /// The App's own exit is the only authorised one: after a decided quit,
    /// `app.exit(0)` arrives as `ExitRequested` and is allowed, while an
    /// independent system request starts nothing and its quit path, if one
    /// was started on a stale reading, asks for no exit. A person's Quit
    /// after the decision asks for the exit again, as main does.
    #[test]
    fn during_a_decided_quit_the_authorised_exit_proceeds_and_an_independent_request_adds_none() {
        let held = Held::default();
        let mut d = Double::new(vec![material(&[], 0, 0)], vec![]);
        assert_eq!(run(&held, QuitRoute::Person, &mut d).exits, 1, "the deciding run asks for one exit");
        assert_eq!(on_exit_requested(held.quit.proceeding().is_some(), Some(0)), ExitAction::Allow, "that exit is allowed");
        assert_eq!(on_system_quit_request(held.quit.proceeding().is_some(), held.quit.busy()), SystemQuitRequest::Decided, "a system request starts nothing");
        let mut after = Double::new(vec![live()], vec![]);
        let system = run(&held, QuitRoute::System, &mut after);
        assert_eq!((system.ending, system.exits), (QuitEnding::AlreadyDecided, 0));
        let person = run(&held, QuitRoute::Person, &mut after);
        assert_eq!((person.ending, person.exits), (QuitEnding::AlreadyDecided, 1), "a person's Quit retries the exit");
        assert!(after.log.is_empty(), "nothing assessed, recorded or settled: {:?}", after.log);
    }

    /// The stale-read schedule: a worker reads "not decided" at the fast
    /// check, is delayed, another run decides and releases admission, then
    /// the delayed worker continues (`run_quit_admitted` is exactly that
    /// continuation).
    #[test]
    fn a_worker_delayed_between_its_check_and_admission_does_nothing_once_another_decided() {
        let held = Held::default();
        assert!(held.quit.proceeding().is_none(), "the delayed worker's fast check reads not decided");
        let mut owner = Double::new(vec![live(), live()], vec![Ok(true)]);
        assert_eq!(run(&held, QuitRoute::Person, &mut owner).ending, QuitEnding::Decided);
        assert!(!held.quit.busy(), "the owner released admission");
        for (route, exits) in [(QuitRoute::System, 0), (QuitRoute::Person, 1)] {
            let mut stale = Double::new(vec![live(), live()], vec![Ok(true)]);
            let told = RefCell::new(Vec::<String>::new());
            let count = Cell::new(0);
            let ending = run_quit_admitted(held.gates(), route, Duration::from_millis(50), || Borrowed::new(&mut stale), |_, m| told.borrow_mut().push(m), || count.set(count.get() + 1));
            assert_eq!((ending, count.get()), (QuitEnding::AlreadyDecided, exits), "{route:?}");
            assert!(stale.log.is_empty() && told.borrow().is_empty(), "nothing recorded, asked, settled or told: {:?}", stale.log);
        }
    }

    #[test]
    fn a_second_request_while_the_question_is_open_is_ignored() {
        let held = Held::default();
        let (opened, open) = mpsc::channel();
        let (release, released) = mpsc::channel::<()>();
        let exits = AtomicUsize::new(0);
        let mut first = Double::new(vec![live(), live()], vec![Ok(true)]);
        let mut second = Double::new(vec![live()], vec![]);
        std::thread::scope(|s| {
            let held = &held;
            let exits = &exits;
            let owner = s.spawn(move || {
                let mut ops = Borrowed::new(&mut first);
                ops.before_confirm = Some(Box::new(move || { opened.send(()).unwrap(); released.recv().unwrap() }));
                run_quit(held.gates(), QuitRoute::Person, Duration::from_millis(50), || ops, |_, _| {}, || { exits.fetch_add(1, Ordering::SeqCst); })
            });
            open.recv().unwrap();
            assert_eq!(on_system_quit_request(held.quit.proceeding().is_some(), held.quit.busy()), SystemQuitRequest::UnderWay, "a system request starts nothing");
            let while_open = run(held, QuitRoute::System, &mut second);
            assert_eq!((while_open.ending, while_open.exits), (QuitEnding::AlreadyOpen, 0), "a worker started anyway is ignored");
            release.send(()).unwrap();
            assert_eq!(owner.join().unwrap(), QuitEnding::Decided);
        });
        assert_eq!(exits.load(Ordering::SeqCst), 1);
        assert!(second.log.is_empty());
    }

    #[test]
    fn each_ending_of_the_quit_path() {
        for route in [QuitRoute::Person, QuitRoute::System] {
            // Nothing live: nothing asked, settled, one exit.
            let held = Held::default();
            let mut d = Double::new(vec![material(&[], 0, 0)], vec![]);
            let ran = run(&held, route, &mut d);
            assert_eq!((ran.ending, ran.exits), (QuitEnding::Decided, 1), "{route:?}");
            assert!(!d.log.contains(&"ask".to_owned()) && d.log.contains(&"settle".to_owned()));
            // Confirmed: interrupts before settlement, one exit.
            let held = Held::default();
            let mut d = Double::new(vec![live(), live()], vec![Ok(true)]);
            assert_eq!(run(&held, route, &mut d).exits, 1);
            let (interrupt, settle) = (d.log.iter().position(|l| l == "interrupt turn-1").unwrap(), d.log.iter().position(|l| l == "settle").unwrap());
            assert!(interrupt < settle && held.quit.proceeding().is_some());
        }
        // Kept running: nothing interrupted or settled, no exit.
        let held = Held::default();
        let mut d = Double::new(vec![live()], vec![Ok(false)]);
        let ran = run(&held, QuitRoute::System, &mut d);
        assert_eq!((ran.ending, ran.exits), (QuitEnding::KeptRunning, 0));
        assert!(!d.log.iter().any(|l| l.starts_with("interrupt") || l == "settle"));
        // The question could not be shown.
        let held = Held::default();
        let mut d = Double::new(vec![live()], vec![Err("no window".into())]);
        assert_eq!(run(&held, QuitRoute::Person, &mut d).ending, QuitEnding::NotAsked);
        // Settlement refused after the answer was recorded and interrupts
        // sent: told, reopened, not proceeding, no exit.
        let held = Held::default();
        let mut d = Double::new(vec![live(), live()], vec![Ok(true)]);
        d.settlement = Err("census unavailable".into());
        let ran = run(&held, QuitRoute::Person, &mut d);
        assert_eq!((ran.ending, ran.exits, ran.told), (QuitEnding::SettlementRefused, 0, vec!["census unavailable".to_owned()]));
        assert!(d.log.contains(&"quit_answered confirmed".to_owned()) && d.log.contains(&"interrupt turn-1".to_owned()), "the answer and interrupts stand: {:?}", d.log);
        assert_eq!(d.log.last().unwrap(), "reopen");
        assert!(held.quit.proceeding().is_none());
        // Stop or Restart Codex under way: told, nothing recorded.
        let held = Held::default();
        let restart = held.stop_gate.lock().unwrap();
        let mut d = Double::new(vec![live()], vec![]);
        let ran = run(&held, QuitRoute::Person, &mut d);
        drop(restart);
        assert_eq!(ran.ending, QuitEnding::AdmissionRefused);
        assert!(d.log.is_empty() && ran.told[0].contains("Stop or Restart Codex is under way"));
        // An explicit key operation under way (the real gate held).
        let held = Held::default();
        let key = held.key_setup.lock().unwrap();
        let mut d = Double::new(vec![live()], vec![]);
        let ran = run(&held, QuitRoute::Person, &mut d);
        drop(key);
        assert_eq!((ran.ending, ran.told), (QuitEnding::KeyOperationBusy, vec![QUIT_KEY_BUSY.to_owned()]));
        assert!(d.log.is_empty());
    }

    /// The first request after the gate is poisoned is declined in words
    /// that follow from the lock state; the retry reaches the decision.
    fn declines_once_then_quits(held: &Held) {
        assert!(held.key_setup.is_poisoned());
        let mut d = Double::new(vec![live(), live()], vec![Ok(true)]);
        let first = run(held, QuitRoute::System, &mut d);
        assert_eq!((first.ending, first.exits), (QuitEnding::KeySetupUncertain, 0));
        assert_eq!(first.told, [QUIT_KEY_UNCERTAIN]);
        assert!(d.log.is_empty(), "nothing recorded or asked: {:?}", d.log);
        assert!(!held.key_setup.is_poisoned() && !held.quit.busy(), "the gate is recovered and admission released");
        let retry = run(held, QuitRoute::Person, &mut d);
        assert_eq!((retry.ending, retry.exits), (QuitEnding::Decided, 1), "the retry reaches the normal quit decision");
        assert!(d.log.contains(&"ask".to_owned()) && d.log.contains(&"settle".to_owned()));
    }

    #[test]
    fn a_gate_poisoned_by_another_operation_declines_once_and_the_retry_quits() {
        let held = Held::default();
        let poisoned = std::thread::scope(|s| s.spawn(|| { let _key = held.key_setup.lock().unwrap(); panic!("an earlier key setup failed") }).join());
        assert!(poisoned.is_err());
        declines_once_then_quits(&held);
    }

    #[test]
    fn a_gate_poisoned_by_the_quit_worker_itself_declines_once_and_the_retry_quits() {
        // The worker panics while holding the gate (here, reading the roster
        // in `ops`, outside the caught sequence).
        let held = Held::default();
        let unwound = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            run_quit(held.gates(), QuitRoute::Person, Duration::from_millis(50), || -> Borrowed<'static> { panic!("the quit worker failed") }, |_, _| {}, || {})
        }));
        assert!(unwound.is_err() && !held.quit.busy(), "admission is released by the unwinding");
        declines_once_then_quits(&held);
    }

    #[test]
    fn a_fault_while_assessing_or_settling_is_told_lifts_fences_and_poisons_nothing() {
        for step in ["assess", "settle"] {
            let held = Held::default();
            let mut d = Double::new(vec![live(), live()], vec![Ok(true)]);
            let mut ops = Borrowed::new(&mut d);
            ops.fault = Some(step);
            let ran = run_with(&held, QuitRoute::Person, ops);
            assert_eq!((ran.ending, ran.exits, ran.told), (QuitEnding::Faulted, 0, vec![QUIT_FAULTED.to_owned()]), "{step}");
            assert!(d.log.ends_with(&["lift".to_owned(), "reopen".to_owned()]), "{step}: {:?}", d.log);
            assert!(!held.key_setup.is_poisoned() && !held.quit.busy() && held.quit.proceeding().is_none(), "{step}");
            let mut retry = Double::new(vec![live(), live()], vec![Ok(true)]);
            assert_eq!(run(&held, QuitRoute::Person, &mut retry).ending, QuitEnding::Decided, "{step}: the retry quits");
        }
    }

    /// The roster through a poisoned home-router lock reaches the production
    /// binding (`read_roster`, `HostQuit`, `run_quit`), and exit cleanup then
    /// uses the roster the decided quit settled without reading the router.
    #[test]
    fn a_poisoned_home_router_is_read_and_exit_cleanup_uses_the_settled_roster() {
        let account = Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account, Arc::new(crate::hosting::Host::new()), Err("no configuration in this test".into())).unwrap());
        let router = Mutex::new(crate::runtime_session::HomeRouter::new(Arc::clone(&account)).unwrap());
        let poisoned = std::thread::scope(|s| s.spawn(|| { let _r = router.lock().unwrap(); panic!("a panic under the home router lock") }).join());
        assert!(poisoned.is_err() && router.is_poisoned());
        let held = Held::default();
        let workflows = Mutex::new(WorkflowRootSession::default());
        let exits = Cell::new(0);
        let ending = run_quit(held.gates(), QuitRoute::Person, Duration::from_millis(50), || {
            let (homes, active) = read_roster(&router);
            assert!(Arc::ptr_eq(&active, &account));
            HostQuit::new(homes, &workflows, "fixture person", |_: &Value| -> Result<bool, String> { panic!("nothing is live, nothing is asked") })
        }, |_, m| panic!("nothing is refused: {m}"), || exits.set(exits.get() + 1));
        assert_eq!((ending, exits.get()), (QuitEnding::Decided, 1));
        let cleanup = held.quit.exit_roster(|| panic!("a decided quit's cleanup does not read the router"));
        assert!(cleanup.len() == 1 && Arc::ptr_eq(&cleanup[0], &account), "the settled roster");
        // Without a decided quit, cleanup reads the router, through poison.
        let undecided = AppQuit::default();
        assert!(Arc::ptr_eq(&undecided.exit_roster(|| read_roster(&router).0)[0], &account));
    }

    #[test]
    fn admission_refusals_map_to_their_endings() {
        let (quit, gate) = (AppQuit::default(), Mutex::new(()));
        let held = admit_quit(&quit, &gate).unwrap();
        assert_eq!(refusal_ending(&admit_quit(&quit, &gate).unwrap_err()), QuitEnding::AlreadyOpen);
        drop(held);
        let restart = gate.lock().unwrap();
        assert_eq!(refusal_ending(&admit_quit(&quit, &gate).unwrap_err()), QuitEnding::AdmissionRefused);
        drop(restart);
    }
}

/// The macOS delegate method's registration (`quit_routes_macos`), against
/// throwaway Objective-C classes created here: not the application's
/// delegate, and no NSApplication is started.
#[cfg(target_os = "macos")]
mod macos_quit_routes {
    use crate::quit_routes_macos::{install_on, selector, should_terminate, type_encoding, Installed, ShouldTerminate};
    use objc2::runtime::{AnyClass, AnyObject, ClassBuilder, Imp, NSObject, Sel};
    use objc2::{msg_send, ClassType};
    use objc2_app_kit::NSApplicationTerminateReply;
    use std::ffi::CString;

    // Fixed implementations; their answers only tell the two apart.
    extern "C-unwind" fn first(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
        NSApplicationTerminateReply::TerminateLater
    }
    extern "C-unwind" fn other(_this: &AnyObject, _sel: Sel, _sender: *mut AnyObject) -> NSApplicationTerminateReply {
        NSApplicationTerminateReply::TerminateNow
    }
    fn imp(f: ShouldTerminate) -> Imp {
        unsafe { std::mem::transmute::<ShouldTerminate, Imp>(f) }
    }
    fn throwaway(name: &str) -> &'static AnyClass {
        let name = CString::new(format!("ChiralityQuitRoutesTest{name}{}", std::process::id())).unwrap();
        ClassBuilder::new(&name, NSObject::class()).unwrap().register()
    }
    fn ask(class: &AnyClass) -> NSApplicationTerminateReply {
        let object: objc2::rc::Retained<AnyObject> = unsafe { msg_send![class, new] };
        unsafe { msg_send![&*object, applicationShouldTerminate: std::ptr::null_mut::<AnyObject>()] }
    }

    #[test]
    fn the_encoding_is_an_unsigned_reply_taking_an_object() {
        assert_eq!(type_encoding().to_str().unwrap(), "Q@:@");
    }

    /// The method is added, answers through the runtime, and a second
    /// installation leaves the first in place.
    #[test]
    fn installs_once_on_a_class_that_does_not_respond() {
        let class = throwaway("Add");
        assert!(!class.responds_to(selector()));
        assert_eq!(unsafe { install_on(class, imp(first)) }, Ok(Installed::Added));
        assert!(class.responds_to(selector()));
        assert_eq!(unsafe { install_on(class, imp(other)) }, Ok(Installed::AlreadyResponds));
        assert_eq!(ask(class), NSApplicationTerminateReply::TerminateLater, "the first implementation stays");
    }

    /// The production method, installed on a throwaway class and sent the
    /// selector through the runtime (the App handle is not set in tests, so
    /// it starts nothing): it declines.
    #[test]
    fn the_production_method_declines() {
        let class = throwaway("Production");
        assert_eq!(unsafe { install_on(class, imp(should_terminate)) }, Ok(Installed::Added));
        assert_eq!(ask(class), NSApplicationTerminateReply::TerminateCancel);
    }

    #[test]
    fn a_class_that_already_responds_is_left_alone() {
        let name = CString::new(format!("ChiralityQuitRoutesTestHas{}", std::process::id())).unwrap();
        let mut builder = ClassBuilder::new(&name, NSObject::class()).unwrap();
        unsafe { builder.add_method(selector(), other as extern "C-unwind" fn(_, _, _) -> _) };
        let class = builder.register();
        assert_eq!(unsafe { install_on(class, imp(first)) }, Ok(Installed::AlreadyResponds));
        assert_eq!(ask(class), NSApplicationTerminateReply::TerminateNow, "the class's own implementation stays");
    }
}
