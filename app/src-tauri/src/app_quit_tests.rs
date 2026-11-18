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

/// The quit path every route runs (`run_quit`), and the answer to the
/// system's request to terminate (`answer_termination`), driven with doubles
/// and an injected replier in place of AppKit's
/// `replyToApplicationShouldTerminate:`.
mod system_quit_routes {
    use super::*;
    use std::cell::RefCell;
    use std::sync::atomic::AtomicUsize;
    use std::sync::mpsc;

    /// A reply guard whose replies are collected.
    fn replier() -> (TerminationReply, mpsc::Receiver<bool>) {
        let (send, receive) = mpsc::channel();
        (TerminationReply::new(move |yes| send.send(yes).unwrap()), receive)
    }
    fn replies(receive: &mpsc::Receiver<bool>) -> Vec<bool> {
        receive.try_iter().collect()
    }

    /// The Double borrowed, so that its log can be read after `run_quit`;
    /// `before_confirm` lets a test hold the question open.
    struct Borrowed<'a> {
        d: &'a mut Double,
        before_confirm: Option<Box<dyn FnMut() + Send + 'a>>,
    }
    impl Interrupts for Borrowed<'_> {
        type Pending = String;
        fn interrupt(&mut self, turn: &Value, deadline: Instant) -> Result<String, crate::codex_stop::Unsent> { self.d.interrupt(turn, deadline) }
        fn acknowledgment(&mut self, pending: &String, wait: Duration) -> Result<Value, String> { self.d.acknowledgment(pending, wait) }
        fn turn_reading(&mut self, turn: &Value) -> Option<Value> { self.d.turn_reading(turn) }
    }
    impl QuitOps for Borrowed<'_> {
        fn assess(&mut self) -> Assessment { self.d.assess() }
        fn record_requested(&mut self, material: &Value) -> Value { self.d.record_requested(material) }
        fn confirm(&mut self, view: &Value) -> Result<bool, String> {
            if let Some(hold) = self.before_confirm.as_mut() { hold() }
            self.d.confirm(view)
        }
        fn record_answered(&mut self, confirmed: bool) -> Value { self.d.record_answered(confirmed) }
        fn close_to_new_turns(&mut self) { self.d.close_to_new_turns() }
        fn reopen_to_new_turns(&mut self) { self.d.reopen_to_new_turns() }
        fn stop_record(&mut self, turn: &Value) -> Value { self.d.stop_record(turn) }
        fn settle(&mut self, ids: &[String]) -> Result<Value, String> { self.d.settle(ids) }
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
    fn run(held: &Held, d: &mut Double, reply: Option<TerminationReply>) -> Ran {
        let told = RefCell::new(Vec::new());
        let exits = AtomicUsize::new(0);
        let ending = run_quit(held.gates(), reply, Duration::from_millis(50), || Borrowed { d, before_confirm: None },
            |_, message| told.borrow_mut().push(message), || { exits.fetch_add(1, Ordering::SeqCst); });
        Ran { ending, told: told.into_inner(), exits: exits.into_inner() }
    }
    fn live() -> Value {
        material(&["turn-1"], 1, 1)
    }

    #[test]
    fn the_decision_for_every_combination() {
        use TerminationAnswer::*;
        use TerminationBehaviour::{Cancel, Later};
        // (decided, under way, reply owed) -> (with Later, with Cancel)
        let table = [
            ((false, false, false), (LaterAndAsk, CancelAndAsk)),
            ((false, false, true), (Decline, Decline)),
            ((false, true, false), (Decline, Decline)),
            ((false, true, true), (Decline, Decline)),
            ((true, false, false), (Now, Now)),
            ((true, false, true), (Decline, Decline)),
            ((true, true, false), (Now, Now)),
            ((true, true, true), (Decline, Decline)),
        ];
        for ((decided, under_way, owed), (later, cancel)) in table {
            assert_eq!(on_should_terminate(decided, under_way, owed, Later), later, "later: decided {decided}, under way {under_way}, owed {owed}");
            assert_eq!(on_should_terminate(decided, under_way, owed, Cancel), cancel, "cancel: decided {decided}, under way {under_way}, owed {owed}");
        }
    }

    /// `deliver` as the main dispatch queue runs it: after the answer is
    /// returned, acting only if it takes the owed flag.
    fn answer(held: (bool, bool), owed: &'static AtomicBool, behaviour: TerminationBehaviour, start: impl FnOnce(Option<TerminationReply>)) -> (TerminationAnswer, Vec<bool>) {
        let queued = std::sync::Arc::new(Mutex::new(Vec::new()));
        let queue = std::sync::Arc::clone(&queued);
        let answer = answer_termination(|| held, owed, behaviour, move |yes| queue.lock().unwrap().push(yes), start);
        let delivered = queued.lock().unwrap().drain(..).filter(|_| owed.swap(false, Ordering::SeqCst)).collect();
        (answer, delivered)
    }
    fn owed_flag() -> &'static AtomicBool {
        Box::leak(Box::new(AtomicBool::new(false)))
    }

    #[test]
    fn the_answer_starts_the_quit_path_only_when_it_asks() {
        let owed = owed_flag();
        let mut handed = None;
        let (later, delivered) = answer((false, false), owed, TerminationBehaviour::Later, |reply| handed = reply);
        assert_eq!((later, delivered, owed.load(Ordering::SeqCst)), (TerminationAnswer::LaterAndAsk, vec![], true), "a reply is owed");
        let owed_reply = handed.expect("the owed reply is handed to the quit path");
        let mut started = false;
        assert_eq!(answer((false, false), owed, TerminationBehaviour::Later, |_| started = true).0, TerminationAnswer::Decline, "a second request while the reply is owed");
        assert!(!started, "starts nothing");
        assert!(owed.load(Ordering::SeqCst), "the earlier request keeps its reply");
        drop(owed_reply);
        owed.store(false, Ordering::SeqCst);
        let mut started = false;
        assert_eq!(answer((false, true), owed, TerminationBehaviour::Later, |_| started = true).0, TerminationAnswer::Decline, "a quit under way");
        assert!(!started);
        assert_eq!(answer((true, true), owed, TerminationBehaviour::Later, |_| panic!("nothing starts")).0, TerminationAnswer::Now, "a decided quit");
        let mut started = None;
        assert_eq!(answer((false, false), owed, TerminationBehaviour::Cancel, |reply| started = Some(reply.is_some())).0, TerminationAnswer::CancelAndAsk);
        assert_eq!(started, Some(false), "cancel owes no reply");
        assert!(!owed.load(Ordering::SeqCst));
    }

    #[test]
    fn a_fault_before_the_answer_declines_and_leaves_no_stray_reply() {
        // The quit path's start panics after the reply guard was handed over:
        // the unwinding drops it (queueing no), and the request is declined.
        let owed = owed_flag();
        let (declined, delivered) = answer((false, false), owed, TerminationBehaviour::Later, |reply| {
            let _owned = reply;
            panic!("injected fault");
        });
        assert_eq!(declined, TerminationAnswer::DeclinedOnFault);
        assert!(!owed.load(Ordering::SeqCst), "nothing is owed");
        assert!(delivered.is_empty(), "the queued no finds no later owed and does nothing: {delivered:?}");
        // A fault reading what the App holds: declined, nothing started.
        let answered = answer_termination(|| panic!("injected fault"), owed, TerminationBehaviour::Later, |_| {}, |_| panic!("nothing starts"));
        assert_eq!(answered, TerminationAnswer::DeclinedOnFault);
        // The next request is answered normally.
        assert_eq!(answer((false, false), owed, TerminationBehaviour::Later, |reply| drop(reply)), (TerminationAnswer::LaterAndAsk, vec![false]));
    }

    #[test]
    fn the_reply_is_yes_only_for_the_decided_quit_and_given_once() {
        let (reply, receive) = replier();
        reply.finish(QuitEnding::Decided);
        assert_eq!(replies(&receive), [true], "yes once, and its drop adds nothing");
        for ending in [QuitEnding::AlreadyDecided, QuitEnding::AlreadyOpen, QuitEnding::AdmissionRefused, QuitEnding::KeyOperationBusy, QuitEnding::KeySetupUncertain, QuitEnding::KeptRunning, QuitEnding::NotAsked, QuitEnding::SettlementRefused] {
            let (reply, receive) = replier();
            reply.finish(ending);
            assert_eq!(replies(&receive), [false], "{ending:?}");
        }
        let (reply, receive) = replier();
        drop(reply);
        assert_eq!(replies(&receive), [false], "dropped unreplied: no");
    }

    #[test]
    fn a_panic_unwinding_through_the_quit_path_replies_no_once() {
        let held = Held::default();
        let (reply, receive) = replier();
        let unwound = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            run_quit(held.gates(), Some(reply), Duration::from_millis(50), || -> Borrowed<'static> { panic!("the quit path failed") }, |_, _| {}, || {})
        }));
        assert!(unwound.is_err());
        assert_eq!(replies(&receive), [false]);
        assert!(!held.quit.busy(), "admission is released by the unwinding");
    }

    #[test]
    fn each_ending_of_the_quit_path_through_run_quit() {
        // Nothing live: nothing asked, settled, the App ends (yes / one exit).
        let held = Held::default();
        let mut d = Double::new(vec![material(&[], 0, 0)], vec![]);
        let (reply, r) = replier();
        let ran = run(&held, &mut d, Some(reply));
        assert_eq!((ran.ending, replies(&r), ran.exits), (QuitEnding::Decided, vec![true], 0), "with a reply owed the system ends the App, not app.exit");
        assert!(!d.log.contains(&"ask".to_owned()) && d.log.contains(&"settle".to_owned()));
        // The same with no reply owed: one app.exit.
        let held = Held::default();
        let mut d = Double::new(vec![material(&[], 0, 0)], vec![]);
        assert_eq!(run(&held, &mut d, None).exits, 1);
        // Confirmed and settled: interrupts, then settlement, then yes.
        let held = Held::default();
        let mut d = Double::new(vec![live(), live()], vec![Ok(true)]);
        let (reply, r) = replier();
        assert_eq!(run(&held, &mut d, Some(reply)).ending, QuitEnding::Decided);
        assert_eq!(replies(&r), [true]);
        let (interrupt, settle) = (d.log.iter().position(|l| l == "interrupt turn-1").unwrap(), d.log.iter().position(|l| l == "settle").unwrap());
        assert!(interrupt < settle && held.quit.proceeding().is_some());
        // Kept running: no; nothing interrupted, nothing settled, no exit.
        let held = Held::default();
        let mut d = Double::new(vec![live()], vec![Ok(false)]);
        let (reply, r) = replier();
        let ran = run(&held, &mut d, Some(reply));
        assert_eq!((ran.ending, replies(&r), ran.exits), (QuitEnding::KeptRunning, vec![false], 0));
        assert!(!d.log.iter().any(|l| l.starts_with("interrupt") || l == "settle"));
        // The question could not be shown: no.
        let held = Held::default();
        let mut d = Double::new(vec![live()], vec![Err("no window".into())]);
        let (reply, r) = replier();
        assert_eq!(run(&held, &mut d, Some(reply)).ending, QuitEnding::NotAsked);
        assert_eq!(replies(&r), [false]);
        // Settlement refused after the answer was recorded and interrupts
        // sent: no, told, turns reopened, and the App is not proceeding.
        let held = Held::default();
        let mut d = Double::new(vec![live(), live()], vec![Ok(true)]);
        d.settlement = Err("census unavailable".into());
        let (reply, r) = replier();
        let ran = run(&held, &mut d, Some(reply));
        assert_eq!((ran.ending, replies(&r), ran.exits), (QuitEnding::SettlementRefused, vec![false], 0));
        assert!(d.log.contains(&"quit_answered confirmed".to_owned()) && d.log.contains(&"interrupt turn-1".to_owned()), "the answer and interrupts stand: {:?}", d.log);
        assert_eq!(d.log.last().unwrap(), "reopen");
        assert_eq!(ran.told, ["census unavailable"]);
        assert!(held.quit.proceeding().is_none());
        // Stop or Restart Codex under way: no, told, nothing recorded.
        let held = Held::default();
        let restart = held.stop_gate.lock().unwrap();
        let mut d = Double::new(vec![live()], vec![]);
        let (reply, r) = replier();
        let ran = run(&held, &mut d, Some(reply));
        drop(restart);
        assert_eq!((ran.ending, replies(&r)), (QuitEnding::AdmissionRefused, vec![false]));
        assert!(d.log.is_empty() && ran.told[0].contains("Stop or Restart Codex is under way"));
        // An explicit key operation under way: no, told, nothing recorded.
        let held = Held::default();
        let key = held.key_setup.lock().unwrap();
        let mut d = Double::new(vec![live()], vec![]);
        let (reply, r) = replier();
        let ran = run(&held, &mut d, Some(reply));
        drop(key);
        assert_eq!((ran.ending, replies(&r), ran.told), (QuitEnding::KeyOperationBusy, vec![false], vec![QUIT_KEY_BUSY.to_owned()]));
        assert!(d.log.is_empty());
    }

    #[test]
    fn a_poisoned_key_setup_gate_declines_once_in_true_words_and_the_retry_quits() {
        let held = Held::default();
        let poisoned = std::thread::scope(|s| s.spawn(|| { let _key = held.key_setup.lock().unwrap(); panic!("an earlier key setup failed") }).join());
        assert!(poisoned.is_err() && held.key_setup.is_poisoned());
        let mut d = Double::new(vec![live(), live()], vec![Ok(true)]);
        let (reply, r) = replier();
        let first = run(&held, &mut d, Some(reply));
        assert_eq!((first.ending, replies(&r), first.exits), (QuitEnding::KeySetupUncertain, vec![false], 0), "the first request gets its reply: no");
        assert_eq!(first.told, [QUIT_KEY_UNCERTAIN]);
        assert!(!first.told[0].contains("is under way"), "not told that a key operation is under way");
        assert!(d.log.is_empty(), "nothing recorded or asked: {:?}", d.log);
        assert!(!held.key_setup.is_poisoned() && !held.quit.busy(), "the gate is recovered and admission released");
        let (reply, r) = replier();
        let retry = run(&held, &mut d, Some(reply));
        assert_eq!((retry.ending, replies(&r)), (QuitEnding::Decided, vec![true]), "the retry reaches the normal quit decision");
        assert!(d.log.contains(&"ask".to_owned()) && d.log.contains(&"settle".to_owned()));
    }

    #[test]
    fn a_second_quit_records_settles_and_exits_nothing_while_one_is_open_or_after_it_decided() {
        let held = Held::default();
        let (opened, open) = mpsc::channel();
        let (release, released) = mpsc::channel::<()>();
        let exits = AtomicUsize::new(0);
        let mut first = Double::new(vec![live(), live()], vec![Ok(true)]);
        let mut second = Double::new(vec![live(), live()], vec![Ok(true)]);
        let mut third = Double::new(vec![live(), live()], vec![Ok(true)]);
        std::thread::scope(|s| {
            let exits = &exits;
            let held = &held;
            let owner = s.spawn(move || {
                let hold: Box<dyn FnMut() + Send> = Box::new(move || { opened.send(()).unwrap(); released.recv().unwrap() });
                run_quit(held.gates(), None, Duration::from_millis(50), || Borrowed { d: &mut first, before_confirm: Some(hold) }, |_, _| {}, || { exits.fetch_add(1, Ordering::SeqCst); })
            });
            open.recv().unwrap();
            // The question is open: a second request (a native one owing a
            // reply) is ignored and answered no.
            let (reply, r) = replier();
            let while_open = run(held, &mut second, Some(reply));
            assert_eq!((while_open.ending, replies(&r), while_open.exits), (QuitEnding::AlreadyOpen, vec![false], 0));
            release.send(()).unwrap();
            assert_eq!(owner.join().unwrap(), QuitEnding::Decided);
        });
        assert_eq!(exits.load(Ordering::SeqCst), 1, "one exit, from the run that decided");
        assert!(second.log.is_empty());
        // After the decision, admission is free again; the run that takes it
        // finds the quit decided under admission and does nothing more, with
        // or without a reply owed.
        let (reply, r) = replier();
        let after = run(&held, &mut third, Some(reply));
        assert_eq!((after.ending, replies(&r), after.exits), (QuitEnding::AlreadyDecided, vec![false], 0));
        assert_eq!(run(&held, &mut third, None).exits, 0);
        assert!(third.log.is_empty(), "nothing assessed, recorded or settled: {:?}", third.log);
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
