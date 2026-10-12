use super::*;
use crate::run_offers::RunStart;

fn g(spawn: u64) -> Value {
    json!({"appSession":"session","home":"home","spawnCounter":spawn})
}
fn row(turn: &str, item: &str, order: u64) -> Value {
    json!({"threadId":"thread","turnId":turn,"native":{"id":item,"type":"userMessage"},"standing":"live-observed","observedOrder":order,"receipt":{"generation":g(1)}})
}
/// A native view of the run's conversation: rows per turn, the turns' native
/// status, re-routes and the host's thread rows.
struct View {
    rows: Vec<Value>,
    turns: Vec<(String, String)>,
    reroutes: Vec<Value>,
    threads: Vec<Value>,
    access: Vec<Value>,
}
impl View {
    fn new() -> Self {
        Self { rows: vec![], turns: vec![], reroutes: vec![], threads: vec![], access: vec![] }
    }
    fn turn(mut self, id: &str, order: u64, status: &str) -> Self {
        self.rows.push(row(id, &format!("{id}-user"), order));
        self.turns.push((id.into(), status.into()));
        self
    }
    fn reroute(mut self, turn: &str, position: u64, to: &str) -> Self {
        self.reroutes.push(json!({"threadId":"thread","turnId":turn,"fromModel":"gpt-x","toModel":to,"reason":"highRiskCyberActivity","generation":g(1),"receiptPosition":position,"standing":"live-observed"}));
        self
    }
    fn started_by_app(mut self) -> Self {
        self.threads.push(json!({"generation":g(1),"threadId":"thread","model":"gpt-x","modelProvider":"openai",
            "requestedDestination":{"source":"person-selected","model":"gpt-x","modelProvider":"openai"},
            "reportedDestination":{"scope":"thread","model":"gpt-x","modelProvider":"openai"}}));
        self.access.push(json!({"threadId":"thread","entryId":"chatgpt-account"}));
        self
    }
    fn value(&self) -> Value {
        json!({"home":"home","generation":g(1),"items":self.rows,
            "turnRecords":self.turns.iter().map(|(t,_)|json!({"threadId":"thread","turnId":t})).collect::<Vec<_>>(),
            "turns":self.turns.iter().map(|(t,s)|json!({"id":t,"status":s})).collect::<Vec<_>>(),
            "modelReroutes":self.reroutes,"hostThreads":self.threads,"conversationAccess":self.access})
    }
}
fn scope(start: u64) -> RunScope<'static> {
    RunScope { home: "home", conversation: "thread", start: RunStart::At(start), start_spawn: 1 }
}
/// Every body validates against RS `$defs/modelTurn` (the App's embedded copy).
fn valid(bodies: &[Value]) {
    let schema: Value = serde_json::from_str(include_str!("../schemas/RS_RECORD.schema.json")).unwrap();
    let validator = jsonschema::options().offline().build(&schema["$defs"]["modelTurn"]).unwrap();
    for body in bodies {
        validator.validate(body).unwrap_or_else(|e| panic!("{body}: {e}"));
    }
}

#[test]
fn turns_and_a_reroute_are_recorded_per_turn_with_the_thread_report_beside_them() {
    let mut recorder = ModelTurnRecorder::default();
    let view = View::new().started_by_app().turn("t1", 1, "completed").turn("t2", 2, "completed").reroute("t2", 40, "gpt-safe");
    let bodies = recorder.observe(&view.value(), &scope(1));
    valid(&bodies);
    assert_eq!(bodies, vec![
        json!({"scope":"thread","requested":"openai/gpt-x","effective":"openai/gpt-x","destinationClass":"user-chosen cloud"}),
        json!({"turn":1,"scope":"turn","requested":"openai/gpt-x","effective":"unknown","reroute":false,"destinationClass":"user-chosen cloud"}),
        json!({"turn":2,"scope":"turn","requested":"openai/gpt-x","effective":"gpt-safe","reroute":true,"destinationClass":"user-chosen cloud"}),
    ], "the thread report is never copied into a turn (U-27)");
    assert!(recorder.observe(&view.value(), &scope(1)).is_empty(), "no duplicates on a later tick");
    assert!(recorder.end().is_empty(), "nothing left for the run's end");
}

#[test]
fn a_turn_with_no_report_is_unknown_and_an_unstarted_conversation_requests_unknown() {
    let mut recorder = ModelTurnRecorder::default();
    let bodies = recorder.observe(&View::new().turn("t1", 1, "interrupted").value(), &scope(1));
    valid(&bodies);
    assert_eq!(bodies, vec![json!({"turn":1,"scope":"turn","requested":"unknown","effective":"unknown","reroute":false,"destinationClass":"unknown"})]);
}

#[test]
fn a_thread_only_report_has_scope_thread_and_no_turn() {
    let mut recorder = ModelTurnRecorder::default();
    // A resumed conversation: the host reports the thread's model; no turn yet.
    let mut view = View::new();
    view.threads.push(json!({"generation":g(1),"threadId":"thread","model":"gpt-y","modelProvider":"lmstudio"}));
    view.access.push(json!({"threadId":"thread","entryId":"local-provider"}));
    let bodies = recorder.observe(&view.value(), &scope(1));
    valid(&bodies);
    assert_eq!(bodies, vec![json!({"scope":"thread","requested":"unknown","effective":"lmstudio/gpt-y","destinationClass":"local model server"})]);
    assert!(bodies[0].get("turn").is_none());
    assert!(recorder.observe(&view.value(), &scope(1)).is_empty());
}

#[test]
fn an_entry_is_due_when_its_turn_ends_or_at_the_run_end() {
    let mut recorder = ModelTurnRecorder::default();
    let live = View::new().started_by_app().turn("t1", 1, "inProgress");
    let bodies = recorder.observe(&live.value(), &scope(1));
    assert_eq!(bodies.len(), 1, "only the thread report while the turn is live: {bodies:?}");
    // A re-route during the turn is held for the turn's entry.
    let live = live.reroute("t1", 9, "gpt-safe");
    assert!(recorder.observe(&live.value(), &scope(1)).is_empty());
    let ended = recorder.end();
    valid(&ended);
    assert_eq!(ended, vec![json!({"turn":1,"scope":"turn","requested":"openai/gpt-x","effective":"gpt-safe","reroute":true,"destinationClass":"user-chosen cloud"})]);
    assert!(recorder.end().is_empty());
}

#[test]
fn a_reroute_after_its_turns_entry_is_a_further_entry_for_that_turn() {
    let mut recorder = ModelTurnRecorder::default();
    let view = View::new().started_by_app().turn("t1", 1, "completed");
    assert_eq!(recorder.observe(&view.value(), &scope(1)).len(), 2);
    let late = recorder.observe(&view.reroute("t1", 50, "gpt-safe").value(), &scope(1));
    valid(&late);
    assert_eq!(late, vec![json!({"turn":1,"scope":"turn","requested":"openai/gpt-x","effective":"gpt-safe","reroute":true,"destinationClass":"user-chosen cloud"})]);
}

#[test]
fn turns_before_the_run_start_and_other_threads_are_not_the_runs() {
    let mut recorder = ModelTurnRecorder::default();
    let mut view = View::new().turn("before", 1, "completed").turn("start", 5, "completed").reroute("before", 3, "gpt-safe");
    view.rows.push(json!({"threadId":"other","turnId":"o","native":{"id":"o-user","type":"userMessage"},"standing":"live-observed","observedOrder":6,"receipt":{"generation":g(1)}}));
    view.rows.push(json!({"threadId":"thread","turnId":"recovered","native":{"id":"r","type":"userMessage"},"standing":"recovered-from-supplier","observedOrder":7}));
    let bodies = recorder.observe(&view.value(), &scope(5));
    assert_eq!(bodies, vec![json!({"turn":1,"scope":"turn","requested":"unknown","effective":"unknown","reroute":false,"destinationClass":"unknown"})], "only the start turn, ordinal 1");
    assert!(recorder.observe(&View::new().value(), &scope(5)).is_empty());
    // Another home's view records nothing.
    let mut foreign = view.value();
    foreign["home"] = json!("other-home");
    assert!(ModelTurnRecorder::default().observe(&foreign, &scope(5)).is_empty());
}
