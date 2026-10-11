//! The checkpoint recorder's first slice: CE-1 listing, AW-6/AW-7 arrivals
//! from live-observed native items only, CE-12/CE-11 from RC-9 run actions,
//! CE-17 waiting arrivals, and the EXEC entry-body schema.
use super::*;

thread_local! {
    /// Called by `file_content` between the read and its recheck (tests only).
    pub(crate) static DURING_READ: std::cell::RefCell<Option<Box<dyn Fn(&std::path::Path)>>> = const { std::cell::RefCell::new(None) };
}

pub(crate) const DECLARATION: &str = r#"{
 "declaration_contract_version": "WD-v0.8",
 "required_tools": [{"name":"add-support","class":"host_operation","operation":"OP-C4","versions":["v1"],"purpose":"Propose added supports.","necessity":"required","stages":["Propose"]}],
 "returned_outputs": [
  {"name":"report","meaning":"The spacing report.","form":"message","destination":"the person","promised_standing":["reported by the agent"],"designating_line":"Spacing report"},
  {"name":"summary","meaning":"The written summary.","form":"file","destination":"the project","promised_standing":["written by the agent"],"path":"out/summary.md"}
 ],
 "checkpoints": [
  {"name":"CP-check","required_act":"A4","reached_when":{"kind":"output_produced","output":"report"},"subject":{"class":"named_output","output":"report"},"position":"After the report","scope":"The report.","purpose":"You record your own checking of the report.","actor":"the_person","expected_act_evidence":{"capturing_surface":"app_act_control","description":"Mark checked in the App."},"on_subject_absent":{"path":"stop"}},
  {"name":"CP-rely","required_act":"A7","reached_when":{"kind":"output_produced","output":"summary"},"subject":{"class":"named_output","output":"summary"},"position":"After the summary","scope":"The summary file.","purpose":"You decide to rely on the summary.","actor":"the_person","expected_act_evidence":{"capturing_surface":"app_act_control","description":"Rely in the App."},"governed":"yes"},
  {"name":"CP-accept","required_act":"A5","reached_when":{"kind":"host_outcome","tools":["add-support"],"outcome":"queued"},"subject":{"class":"change_items_of_named_proposal"},"position":"Wait for acceptance","scope":"Per change item.","purpose":"You decide each change.","actor":"the_person","expected_act_evidence":{"capturing_surface":"host_act_facility","description":"The host's act record."}},
  {"name":"CP-bad","required_act":"A16","reached_when":{"kind":"output_produced","output":"report"},"subject":{"class":"named_output","output":"report"},"position":"x","scope":"x","purpose":"x","actor":"the_person","expected_act_evidence":{"capturing_surface":"app_act_control","description":"x"}}
 ]
}"#;

/// A WORKFLOW.md carrying the fixture declaration.
pub(crate) fn workflow_text() -> String {
    format!("# Fixture workflow\n\nInvented for tests.\n\n```workflow-declaration\n{DECLARATION}\n```\n")
}
fn declaration() -> crate::workflow_declaration::Declaration {
    crate::workflow_declaration::read(&workflow_text()).unwrap()
}
fn g(counter: u64) -> Value {
    json!({"appSession":"session","home":"native-home","spawnCounter":counter})
}
/// A live-observed row of `thread`, received in generation `g(1)` at the given positions.
fn row(turn: &str, item: Value, order: u64, started: Option<u64>, completed: Option<u64>) -> Value {
    let mut receipt = json!({"generation":g(1)});
    if let Some(p) = started { receipt["started"] = json!(p); }
    if let Some(p) = completed { receipt["completed"] = json!(p); }
    let mut row = json!({"threadId":"thread","turnId":turn,"native":item,"displayState":if completed.is_some(){"completed"}else{"in-progress"},"standing":"live-observed","observedOrder":order,"receipt":receipt});
    if started.is_some() { row["startNative"] = item.clone(); }
    if completed.is_some() { row["sourceFrame"] = json!({"method":"item/completed","params":{"completedAtMs":1_790_000_000_123i64}}); }
    row
}
fn message(id: &str, text: &str) -> Value { json!({"id":id,"type":"agentMessage","text":text}) }
fn command(id: &str, source: &str) -> Value { json!({"id":id,"type":"commandExecution","source":source,"command":"x","status":"inProgress"}) }
fn file(id: &str, path: &str, status: &str) -> Value { json!({"id":id,"type":"fileChange","status":status,"changes":[{"path":path,"kind":{"type":"add"},"diff":""}]}) }
fn view(items: Vec<Value>) -> Value {
    json!({"home":"native-home","generation":g(1),"items":items})
}
fn scope<'a>(root: &'a std::path::Path) -> RunScope<'a> {
    RunScope { home: "native-home", conversation: "thread", start: crate::run_offers::RunStart::At(1), project_root: root }
}
fn validator() -> jsonschema::Validator {
    let schema: Value = serde_json::from_str(include_str!("../schemas/checkpoint-record-entries.schema.json")).unwrap();
    jsonschema::options().offline().build(&schema).unwrap()
}
fn valid(outputs: &[Output]) {
    let v = validator();
    for (kind, body) in outputs {
        let output = json!({"kind":kind,"observedAt":"2026-10-10T00:00:00.000Z","body":body});
        assert!(v.is_valid(&output), "{output}: {:?}", v.iter_errors(&output).map(|e| e.to_string()).collect::<Vec<_>>());
    }
}
/// Observes with no act records in the project.
fn obs(recorder: &mut CheckpointRecorder, view: &Value, scope: &RunScope, entries: &[Value]) -> Vec<Output> {
    recorder.observe(view, scope, entries, &mut || Ok(ActRead::default()))
}
fn entries(outputs: &[Output]) -> Vec<Value> {
    outputs.iter().map(|(k, b)| json!({"kind":k,"body":b})).collect()
}

#[test]
fn ce1_lists_recognized_checkpoints_with_their_evaluability() {
    let (recorder, listed) = CheckpointRecorder::start(Ok(declaration()));
    valid(&listed);
    let names: Vec<&str> = listed.iter().filter(|(k, _)| *k == "checkpoint_listed").map(|(_, b)| b["checkpoint"].as_str().unwrap()).collect();
    assert_eq!(names, ["CP-check", "CP-rely", "CP-accept"], "the invalid checkpoint is never listed (§4.14)");
    assert_eq!(listed[3], ("declaration_finding", json!({"checkpoint":"CP-bad","finding":"invalid","code":"FB-03"})), "CE-2 reports it instead");
    assert_eq!(listed[0].1["evaluability"]["status"], "evaluable with limit");
    assert!(listed[0].1["evaluability"]["reason"].as_str().unwrap().contains("\"Spacing report\""));
    assert_eq!(listed[0].1["onSubjectAbsent"], "stop");
    assert_eq!(listed[1].1["governed"], true, "governed is listed and changes nothing (PH-9)");
    assert!(listed[1].1["evaluability"]["reason"].as_str().unwrap().contains("out/summary.md"));
    assert_eq!(listed[2].1["evaluability"]["status"], "not evaluable");
    assert_eq!(recorder.view()["listed"].as_array().unwrap().len(), 3);
    let (unreadable, none) = CheckpointRecorder::start(Err("bytes differ".into()));
    assert!(none.is_empty());
    assert!(unreadable.view()["limit"].as_str().unwrap().contains("declaration not resolvable"));
}

#[test]
fn arrivals_come_only_from_live_completed_items_that_meet_the_declaration() {
    let root = std::path::PathBuf::from("/project/root");
    let (mut recorder, listed) = CheckpointRecorder::start(Ok(declaration()));
    let items = vec![
        row("turn-0", message("before", "Spacing report"), 0, Some(1), Some(2)), // a turn before the run started
        row("turn-1", json!({"id":"start","type":"userMessage","content":[]}), 1, Some(3), Some(3)),
        row("turn-1", message("m1", "  \n  Spacing report  \nThe findings."), 2, Some(4), Some(6)),
        row("turn-1", message("m2", "Report follows\nSpacing report"), 3, Some(5), Some(7)), // first line differs
        row("turn-1", message("m3", "spacing report"), 4, Some(8), Some(9)), // case differs
        row("turn-1", file("f1", "/project/root/out/summary.md", "completed"), 5, Some(10), Some(11)),
        row("turn-1", file("f2", "/project/root/out/other.md", "completed"), 6, Some(12), Some(13)),
        row("turn-1", file("f3", "out/summary.md", "failed"), 7, Some(14), Some(15)), // not completed
        row("turn-1", message("m4", "Spacing report"), 8, Some(16), None), // still streaming
    ];
    let mut recovered = row("turn-1", message("m5", "Spacing report"), 9, None, Some(17));
    recovered["standing"] = json!("recovered-from-supplier");
    let mut all = items.clone();
    all.push(recovered);
    // The turn ordering puts turn-0 before the run's start turn (order 1).
    let mut v = view(all);
    v["items"][0]["observedOrder"] = json!(0);
    let mut outputs = obs(&mut recorder, &v, &scope(&root), &entries(&listed));
    valid(&outputs);
    // f1, f2 and f3 started after m1's arrival: f1's start is the first run action after it.
    let kinds: Vec<&str> = outputs.iter().map(|(k, _)| *k).collect();
    assert_eq!(kinds, ["checkpoint_arrival", "disposition_change", "continued_past", "checkpoint_arrival", "disposition_change", "continued_past"], "{outputs:#?}");
    let arrival = &outputs[0].1;
    assert_eq!((arrival["checkpoint"].as_str(), arrival["arrivalOrdinal"].as_u64(), arrival["event"]["ref"].as_str()), (Some("CP-check"), Some(1), Some("item:thread/turn-1/m1")));
    assert_eq!(arrival["event"]["evidencedTime"], json!({"value":"2026-09-21T14:13:20.123Z","source":"supplier_item_time"}));
    assert_eq!(arrival["referents"][0]["content"]["method"], "chirality.app.exact-bytes.sha256/v1");
    assert_eq!(arrival["referents"][0]["content"]["value"], crate::util::sha256_hex("  \n  Spacing report  \nThe findings.".as_bytes()));
    assert_eq!(arrival["requestObservation"], json!({"state":"not yet observed"}));
    assert!(arrival["limits"].as_array().unwrap().iter().any(|l| l == MESSAGE_ACT_LIMIT), "no act control binds an agent message");
    assert_eq!(outputs[1].1, json!({"arrival":{"checkpoint":"CP-check","arrivalOrdinal":1},"disposition":"waiting","annotations":[]}));
    assert_eq!(outputs[2].1["actionRef"], "item:thread/turn-1/f1");
    let file_arrival = &outputs[3].1;
    assert_eq!((file_arrival["checkpoint"].as_str(), file_arrival["governed"].as_bool()), (Some("CP-rely"), Some(true)));
    assert_eq!(file_arrival["referents"][0]["content"]["notObtainable"], true);
    assert_eq!(outputs[5].1["arrival"]["checkpoint"], "CP-rely");
    assert_eq!(outputs[5].1["actionRef"], "item:thread/turn-1/f2");
    // Reading the same view again records nothing new.
    let mut recorded = entries(&listed);
    recorded.extend(entries(&outputs));
    assert!(obs(&mut recorder, &v, &scope(&root), &recorded).is_empty(), "each item is read once");
    // A later agent command adds no second continued_past; the person's own command never does.
    let mut more = items.clone();
    more.push(row("turn-1", command("c1", "userShell"), 10, Some(18), None));
    more.push(row("turn-1", command("c2", "agent"), 11, Some(19), None));
    assert!(obs(&mut recorder, &view(more.clone()), &scope(&root), &recorded).is_empty());
    // CE-11: once the record reads the arrival performed, the next run action is its resume point.
    recorded.push(json!({"kind":"disposition_change","body":{"arrival":{"checkpoint":"CP-check","arrivalOrdinal":1},"disposition":"performed","performanceOrdinal":1}}));
    let mut c3 = row("turn-1", command("c3", "agent"), 12, Some(20), None);
    c3["sourceFrame"] = json!({"method":"item/started","params":{"startedAtMs":1_790_000_000_500i64}});
    more.push(c3);
    outputs = obs(&mut recorder, &view(more), &scope(&root), &recorded);
    valid(&outputs);
    assert_eq!(outputs.len(), 1);
    assert_eq!((outputs[0].0, outputs[0].1["firstActionRef"].as_str()), ("run_resumed", Some("item:thread/turn-1/c3")));
    assert_eq!(waiting_arrivals(&recorded), vec![json!({"checkpoint":"CP-rely","arrivalOrdinal":1})], "only the arrival still waiting in the record");
}

#[test]
fn each_production_arrives_and_nothing_arrives_outside_the_run() {
    let root = std::path::PathBuf::from("/project/root");
    let (mut recorder, _) = CheckpointRecorder::start(Ok(declaration()));
    let items = vec![
        row("turn-1", json!({"id":"start","type":"userMessage","content":[]}), 1, Some(1), Some(1)),
        row("turn-1", message("m1", "Spacing report"), 2, Some(2), Some(3)),
        row("turn-2", message("m2", "Spacing report\nagain"), 3, Some(4), Some(5)),
    ];
    let outputs = obs(&mut recorder, &view(items.clone()), &scope(&root), &[]);
    let ordinals: Vec<u64> = outputs.iter().filter(|(k, _)| *k == "checkpoint_arrival").map(|(_, b)| b["arrivalOrdinal"].as_u64().unwrap()).collect();
    assert_eq!(ordinals, [1, 2], "OP-4: each completed message carrying the line is a production");
    let (mut fresh, _) = CheckpointRecorder::start(Ok(declaration()));
    let mut unknown = scope(&root);
    unknown.start = crate::run_offers::RunStart::Unknown;
    assert!(obs(&mut fresh, &view(items.clone()), &unknown, &[]).is_empty(), "a run whose start is not in this view records nothing");
    let mut other = view(items.clone());
    other["home"] = json!("another-home");
    assert!(obs(&mut fresh, &other, &scope(&root), &[]).is_empty(), "another home's view");
    let mut other_session = view(items);
    for item in other_session["items"].as_array_mut().unwrap() { item["receipt"]["generation"]["appSession"] = json!("earlier"); }
    assert!(obs(&mut fresh, &other_session, &scope(&root), &[]).is_empty(), "rows not received in this App session");
}

// AW-7 as read here: only a change that produces the declared path arrives.
// A delete, or a move away from it, is not a production of the output.
#[test]
fn a_delete_or_a_move_away_from_the_declared_path_is_not_an_arrival() {
    let root = std::path::PathBuf::from("/project/root");
    let change = |id: &str, path: &str, kind: Value| json!({"id":id,"type":"fileChange","status":"completed","changes":[{"path":path,"kind":kind,"diff":""}]});
    let arrivals = |item: Value| {
        let (mut recorder, _) = CheckpointRecorder::start(Ok(declaration()));
        let items = vec![row("turn-1", json!({"id":"start","type":"userMessage","content":[]}), 1, Some(1), Some(1)), row("turn-1", item, 2, Some(2), Some(3))];
        obs(&mut recorder, &view(items), &scope(&root), &[]).iter().filter(|(k, _)| *k == "checkpoint_arrival").count()
    };
    assert_eq!(arrivals(change("d", "out/summary.md", json!({"type":"delete"}))), 0, "a delete produces nothing");
    assert_eq!(arrivals(change("m", "out/summary.md", json!({"type":"update","move_path":"out/elsewhere.md"}))), 0, "a move's source is not produced");
    assert_eq!(arrivals(change("t", "out/draft.md", json!({"type":"update","move_path":"out/summary.md"}))), 1, "a move onto the declared path produces it");
    assert_eq!(arrivals(change("u", "out/summary.md", json!({"type":"update","move_path":null}))), 1, "an update in place");
    assert_eq!(arrivals(change("u2", "/project/root/out/summary.md", json!({"type":"update"}))), 1, "an update without move_path, absolute path");
    assert_eq!(arrivals(change("a", "out/summary.md", json!({"type":"add"}))), 1);
    assert_eq!(arrivals(change("x", "out/summary.md", json!({"type":"rename"}))), 0, "an unknown change kind produces nothing");
}

#[test]
fn file_paths_compare_normalized_against_the_project_root() {
    let root = std::path::Path::new("/project/root");
    assert!(same_path("out/summary.md", "out/summary.md", root));
    assert!(same_path("/project/root/out/summary.md", "out/summary.md", root));
    assert!(same_path("./out//summary.md", "out/summary.md", root), "`.` segments and repeated separators are normalized on both sides");
    assert!(same_path("out/summary.md", "./out/summary.md", root));
    assert!(!same_path("/project/rootx/out/summary.md", "out/summary.md", root));
    assert!(!same_path("/elsewhere/out/summary.md", "out/summary.md", root));
    assert!(!same_path("out/../out/summary.md", "out/summary.md", root), "a path with `..` never matches");
    assert_eq!(normal("./a//b/./c"), Some("a/b/c".into()));
    assert_eq!((normal("/a"), normal("a/../b"), normal("./")), (None, None, None));
    assert_eq!(first_line("\n \t\n  x  \ny"), Some("x"));
    assert_eq!(first_line(" \n "), None);
}

// ---- Act counting (CE-5, CE-6, CE-8), requests (CE-4), findings (CE-2), AW-3 ----

const BEFORE: &str = "2026-09-21T14:00:00.000Z";
const AT: &str = "2026-09-21T14:13:20.123Z"; // the file change's completedAtMs
const AFTER: &str = "2026-09-21T15:00:00.000Z";
const LATER: &str = "2026-09-21T16:00:00.000Z";

/// A temporary project with `out/summary.md` holding `content`.
fn project(content: &str) -> std::path::PathBuf {
    let root = std::env::temp_dir().join(crate::util::opaque_id("checkpoint-acts-").unwrap());
    std::fs::create_dir_all(root.join("out")).unwrap();
    std::fs::write(root.join("out/summary.md"), content).unwrap();
    std::fs::canonicalize(root).unwrap()
}
fn digest(content: &str) -> Value {
    json!({"method":EXACT_BYTES,"value":crate::util::sha256_hex(content.as_bytes())})
}
/// The capture object the App act control writes for a file act or decline.
fn capture_of(choice: &str, kind: &str, file: &std::path::Path, content: &Value, time: &str) -> Value {
    let id = crate::util::opaque_id("cap:").unwrap();
    let capture = json!({"format":"chirality.aac.capture-evidence","formatVersion":"0.3","captureId":id,"offerId":format!("offer:{id}"),
        "offerDigest":{"method":"aac-offer-digest/0.1","value":"0".repeat(64)},"choice":choice,"actKind":kind,
        "actor":{"osAccount":"fixture","identityVerified":false},"boundSubject":[file.to_str().unwrap()],"boundContent":[content],
        "scope":"The summary file.","purpose":"You decide.","capturedAt":time,"surface":"App interface","inputSource":"host-native-confirmation",
        "answers":{"standing":"no arrival: a standing act (RC-6)"},"evidenceLimits":["identity not verified"]});
    crate::schema_validation::validate_capture(&capture).unwrap();
    capture
}
fn store(root: &std::path::Path, capture: &Value) {
    let path = crate::storage::capture_path(root, capture["captureId"].as_str().unwrap());
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    std::fs::write(path, serde_json::to_vec(capture).unwrap()).unwrap();
}
/// The record for a capture, as the App writer appends it, by `recorder`.
fn record_for(root: &std::path::Path, capture: &Value, recorder: &crate::records::Recorder) -> String {
    let kind = crate::records::capture_record_kind(capture).unwrap();
    crate::records::append(&root.join(crate::recorder::LOG), kind, recorder, crate::act_control::act_body(capture)).unwrap()["recordId"].as_str().unwrap().to_owned()
}
/// A file act as the App act control leaves it: capture stored, record written by the capturing surface.
fn act(root: &std::path::Path, kind: &str, file: &std::path::Path, content: &str, time: &str) -> String {
    let capture = capture_of("act", kind, file, &digest(content), time);
    store(root, &capture);
    record_for(root, &capture, &crate::records::APP_INTERFACE)
}
fn decline(root: &std::path::Path, kind: &str, file: &std::path::Path, content: &str, time: &str) -> String {
    let capture = capture_of("decline", kind, file, &digest(content), time);
    store(root, &capture);
    record_for(root, &capture, &crate::records::APP_INTERFACE)
}
fn start_row() -> Value {
    row("turn-1", json!({"id":"start","type":"userMessage","content":[]}), 1, Some(1), Some(1))
}
/// The run's start turn, then a completed agent change that produces `path`
/// (completed at 2026-09-21T14:13:20.123Z).
fn change_view(path: &str) -> Value {
    view(vec![start_row(), row("turn-1", file("f1", path, "completed"), 2, Some(2), Some(3))])
}
fn file_view() -> Value {
    change_view("out/summary.md")
}
/// Every output is a valid EXEC body (the RS-only limit kind aside) and a conformant RS run entry.
fn conformant(outputs: &[Output]) {
    let exec: Vec<Output> = outputs.iter().filter(|(k, _)| *k != "evidence_limit").cloned().collect();
    valid(&exec);
    for (kind, body) in outputs {
        if let Some(why) = crate::records::nonconformance(kind, body, "rec:app:fixture", "run:workflow:fixture", "2026-10-10T00:00:00.000Z") {
            panic!("{kind} {body}: {why}");
        }
    }
}
/// Starts a recorder, observes `view` with the project's act records as read now.
fn observe_view(root: &std::path::Path, view: &Value) -> (Vec<Value>, Vec<Output>, ActRead) {
    let read = project_act_records(root).unwrap();
    let (mut recorder, listed) = CheckpointRecorder::start(Ok(declaration()));
    let outputs = recorder.observe(view, &scope(root), &entries(&listed), &mut || Ok(read.clone()));
    let mut all = entries(&listed);
    all.extend(entries(&outputs));
    (all, outputs, read)
}
fn observe_with(root: &std::path::Path) -> (Vec<Value>, Vec<Output>, ActRead) {
    observe_view(root, &file_view())
}
fn kinds(outputs: &[Output]) -> Vec<&str> {
    outputs.iter().map(|(k, _)| *k).collect()
}
const RELY: &str = "output summary: file out/summary.md";

// AW-7 binds the file's content as read; CE-5/CE-6 after the arrival, in capture order;
// the first counting act decides (§4.6); CE-17 then lists nothing; re-reading adds nothing.
#[test]
fn acts_after_the_arrival_are_counted_against_the_files_content() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    let a4 = act(&root, "A4", &file, "v1", AFTER);
    let old = act(&root, "A7", &file, "v0", "2026-09-21T15:30:00.000Z");
    let rely = act(&root, "A7", &file, "v1", LATER);
    act(&root, "A7", &file, "v1", "2026-09-21T17:00:00.000Z");
    act(&root, "A7", &root.join("out/other.md"), "v1", AFTER);
    let (all, outputs, read) = observe_with(&root);
    conformant(&outputs);
    assert_eq!(read.acts.len(), 5);
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change", "act_not_counted", "disposition_change", "act_not_counted", "disposition_change", "act_counted", "disposition_change"], "{outputs:#?}");
    assert_eq!(outputs[0].1["referents"][0], json!({"subject":RELY,"content":{"method":EXACT_BYTES,"value":crate::util::sha256_hex(b"v1"),"scope":"the file's bytes as the App read them after observing the completed change"}}));
    assert!(outputs[0].1["limits"].as_array().unwrap().iter().any(|l| l == FILE_READ_LIMIT));
    assert!(outputs[0].1["limits"].as_array().unwrap().iter().any(|l| l.as_str().unwrap().contains("A capture is a readable claim; its native origin is not verified.")), "the run record says native origin is unverified");
    let arrival = json!({"checkpoint":"CP-rely","arrivalOrdinal":1});
    assert_eq!(outputs[2].1, json!({"arrival":arrival,"act":{"recordId":a4,"actKind":"A4","capturedAt":AFTER,"capturingSurface":"app_act_control"},"reason":"another act kind","capturedBeforeArrival":false}));
    assert_eq!(outputs[3].1["disposition"], "waiting");
    assert_eq!((outputs[4].1["act"]["recordId"].as_str(), outputs[4].1["reason"].as_str()), (Some(old.as_str()), Some("act on other content")));
    assert_eq!(outputs[5].1["annotations"][0]["label"], "act on other content");
    assert_eq!(outputs[6].1, json!({"arrival":arrival,"act":{"recordId":rely,"actKind":"A7","capturedAt":LATER,"capturingSurface":"app_act_control"},"relation":"after arrival","referents":[RELY]}));
    assert_eq!(outputs[7].1, json!({"arrival":arrival,"disposition":"performed","performanceOrdinal":1,"answeredBy":[rely],"annotations":[]}));
    assert!(waiting_arrivals(&all).is_empty(), "the performed arrival is not listed as waiting (CI-20 (h))");
    assert!(count_acts(&all, &read, &root).is_empty(), "rebuildable: acts already cited are not read again (RC-10)");
    // While the arrival still waits, an act already not counted is not cited again.
    let waiting: Vec<Value> = all.iter().take_while(|e| e["kind"] != "act_counted").cloned().collect();
    let mut first_two = read.clone();
    first_two.acts.retain(|a| a["record"]["recordId"] == a4.as_str() || a["record"]["recordId"] == old.as_str());
    assert!(count_acts(&waiting, &first_two, &root).is_empty(), "the not-counted acts are cited once");
    std::fs::remove_dir_all(root).unwrap();
}

// SP-6 (K1-2): an earlier act on the current content counts at the arrival; an earlier act
// on older content or of another kind is "prior act not counted" with its reason.
#[test]
fn earlier_acts_count_only_on_current_content() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    let stale = act(&root, "A7", &file, "v0", "2026-09-21T13:00:00.000Z");
    let check = act(&root, "A4", &file, "v1", "2026-09-21T13:30:00.000Z");
    let rely = act(&root, "A7", &file, "v1", BEFORE);
    let (all, outputs, _) = observe_with(&root);
    conformant(&outputs);
    assert_eq!(kinds(&outputs)[2..], ["act_not_counted", "disposition_change", "act_not_counted", "disposition_change", "act_counted", "disposition_change"]);
    assert_eq!((outputs[2].1["reason"].as_str(), outputs[2].1["capturedBeforeArrival"].as_bool()), (Some("content no longer current"), Some(true)));
    assert_eq!(outputs[3].1["annotations"], json!([{"label":"prior act not counted","actRef":stale,"reason":"content no longer current"}]));
    assert_eq!(outputs[5].1["annotations"], json!([{"label":"prior act not counted","actRef":check,"reason":"another act kind"}]));
    assert_eq!(outputs[6].1["relation"], "earlier act");
    assert_eq!(outputs[7].1["annotations"], json!([{"label":"by earlier act","actRef":rely,"time":BEFORE,"referents":[RELY]}]));
    assert!(waiting_arrivals(&all).is_empty());
    std::fs::remove_dir_all(root).unwrap();
}

// m-3 (CI-20 (h) reading): before the arrival, the latest decision of the required kind on the
// current content governs; an earlier one on that content is superseded.
#[test]
fn the_latest_decision_before_the_arrival_governs() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    act(&root, "A7", &file, "v1", "2026-09-21T13:00:00.000Z");
    let no = decline(&root, "A7", &file, "v1", "2026-09-21T13:30:00.000Z");
    decline(&root, "A7", &file, "v0", BEFORE); // on other content: not a decision on this content
    let (all, outputs, _) = observe_with(&root);
    conformant(&outputs);
    assert_eq!(kinds(&outputs)[2..], ["arrival_declined", "disposition_change"], "{outputs:#?}");
    assert_eq!((outputs[2].1["declinedEventRef"].as_str(), outputs[3].1["disposition"].as_str()), (Some(no.as_str()), Some("resolved negatively")));
    assert!(waiting_arrivals(&all).is_empty());
    // The other order: a decline, then the act, both before the arrival.
    let root2 = project("v1");
    let file2 = root2.join("out/summary.md");
    decline(&root2, "A7", &file2, "v1", "2026-09-21T13:00:00.000Z");
    let rely = act(&root2, "A7", &file2, "v1", "2026-09-21T13:30:00.000Z");
    let (_, outputs, _) = observe_with(&root2);
    assert_eq!(kinds(&outputs)[2..], ["act_counted", "disposition_change"], "{outputs:#?}");
    assert_eq!((outputs[2].1["act"]["recordId"].as_str(), outputs[2].1["relation"].as_str()), (Some(rely.as_str()), Some("earlier act")));
    std::fs::remove_dir_all(root).unwrap();
    std::fs::remove_dir_all(root2).unwrap();
}

// CE-8: after the arrival, a decline of the required kind on the current content resolves it
// negatively; another kind or other content does not; acts after that are not read.
#[test]
fn a_decline_after_the_arrival_resolves_it_negatively() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    decline(&root, "A4", &file, "v1", AFTER);
    decline(&root, "A7", &file, "v0", "2026-09-21T15:10:00.000Z");
    let no = decline(&root, "A7", &file, "v1", "2026-09-21T15:30:00.000Z");
    act(&root, "A7", &file, "v1", LATER);
    let (all, outputs, _) = observe_with(&root);
    conformant(&outputs);
    assert_eq!(kinds(&outputs)[2..], ["arrival_declined", "disposition_change"], "{outputs:#?}");
    assert_eq!(outputs[2].1["declinedEventRef"], no.as_str());
    assert_eq!(outputs[3].1["disposition"], "resolved negatively");
    assert!(waiting_arrivals(&all).is_empty());
    std::fs::remove_dir_all(root).unwrap();
}

// B-1 (SP-3, PH-4, RS R-8, §13.7): a record counts only through the one capture object it cites,
// corresponding to it and written by the capturing surface. A missing or mismatched capture, a
// record another recorder wrote, or two records on one capture never become acts: each adds an
// "unresolvable reference" limit, once, and the arrival stays waiting.
#[test]
fn records_not_verified_against_their_capture_count_nothing() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    // Missing capture: the record cites a capture that is not in the store.
    let missing = record_for(&root, &capture_of("act", "A7", &file, &digest("v1"), AFTER), &crate::records::APP_INTERFACE);
    // Mismatched capture: the stored capture says another purpose than the record.
    let capture = capture_of("act", "A7", &file, &digest("v1"), AFTER);
    let mismatched = record_for(&root, &capture, &crate::records::APP_INTERFACE);
    let mut altered = capture.clone();
    altered["purpose"] = json!("Something else.");
    store(&root, &altered);
    // An agent-written record: a real capture, but not written by the capturing surface.
    let capture = capture_of("act", "A7", &file, &digest("v1"), AFTER);
    store(&root, &capture);
    let agent = record_for(&root, &capture, &crate::records::APP_WRITER);
    // Two records on one capture (R-8).
    let capture = capture_of("act", "A7", &file, &digest("v1"), AFTER);
    store(&root, &capture);
    let first = record_for(&root, &capture, &crate::records::APP_INTERFACE);
    let second = record_for(&root, &capture, &crate::records::APP_INTERFACE);
    let (all, outputs, read) = observe_with(&root);
    conformant(&outputs);
    assert!(read.acts.is_empty(), "{:#?}", read.acts);
    assert_eq!(read.unresolved.len(), 5);
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change", "evidence_limit", "evidence_limit", "evidence_limit", "evidence_limit", "evidence_limit"]);
    let limited: BTreeSet<&str> = outputs[2..].iter().map(|(_, b)| b["subjectRef"].as_str().unwrap()).collect();
    assert_eq!(limited, BTreeSet::from([missing.as_str(), mismatched.as_str(), agent.as_str(), first.as_str(), second.as_str()]));
    assert!(outputs[2..].iter().all(|(_, b)| b["label"] == "unresolvable reference"));
    let reason = |id: &str| read.unresolved.iter().find(|u| u["record"]["recordId"] == id).unwrap()["reason"].as_str().unwrap().to_owned();
    assert!(reason(&missing).starts_with("capture evidence not resolved"), "{}", reason(&missing));
    assert_eq!(reason(&mismatched), "the record differs from the capture it cites");
    assert_eq!(reason(&agent), "not written by the App's capturing surface (PH-4)");
    assert_eq!(reason(&first), "several records cite one capture (RS R-8)");
    assert_eq!(waiting_arrivals(&all), vec![json!({"checkpoint":"CP-rely","arrivalOrdinal":1})]);
    assert!(count_acts(&all, &read, &root).is_empty(), "each limit is written once");
    std::fs::remove_dir_all(root).unwrap();
}

// m-c 1: a record whose bound content differs from its capture's is not an act, even
// when the record's content is the arrival's.
#[test]
fn a_record_whose_content_differs_from_its_capture_does_not_count() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    let capture = capture_of("act", "A7", &file, &digest("v0"), AFTER);
    store(&root, &capture);
    let mut body = crate::act_control::act_body(&capture);
    body["boundContent"] = json!([digest("v1")]);
    let id = crate::records::append(&root.join(crate::recorder::LOG), "human_act", &crate::records::APP_INTERFACE, body).unwrap()["recordId"].as_str().unwrap().to_owned();
    let (all, outputs, read) = observe_with(&root);
    assert!(read.acts.is_empty());
    assert_eq!((read.unresolved[0]["record"]["recordId"].as_str(), read.unresolved[0]["reason"].as_str()), (Some(id.as_str()), Some("the record differs from the capture it cites")));
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change", "evidence_limit"]);
    assert_eq!(waiting_arrivals(&all).len(), 1);
    std::fs::remove_dir_all(root).unwrap();
}

// m-c 2: a file that changes while it is read is not obtainable (RS §6.2a coherent snapshot).
#[test]
fn a_file_changed_during_the_read_is_not_obtainable() {
    let root = project("v1");
    DURING_READ.with(|hook| *hook.borrow_mut() = Some(Box::new(|file: &std::path::Path| {
        let mut f = std::fs::OpenOptions::new().append(true).open(file).unwrap();
        std::io::Write::write_all(&mut f, b" and more").unwrap();
    })));
    let content = file_content(&root, "out/summary.md");
    DURING_READ.with(|hook| *hook.borrow_mut() = None);
    assert_eq!(content["notObtainable"], true, "{content}");
    assert!(content["reason"].as_str().unwrap().starts_with("the file changed while it was read"));
    assert_eq!(file_content(&root, "out/summary.md")["value"], crate::util::sha256_hex(b"v1 and more"), "read again once it is still");
    std::fs::remove_dir_all(root).unwrap();
}

// m-b: the limit written when the act records cannot be read at an end is a conformant RS entry.
#[test]
fn the_unread_acts_limit_is_conformant() {
    let limit = acts_unread_limit("the project's record set is incomplete");
    conformant(&[limit.clone()]);
    assert_eq!(limit.1["label"], "unresolvable reference");
    assert!(limit.1["detail"].as_str().unwrap().contains("record set is incomplete"));
}

// m-2 (RS R-6): a corrected act record is not current, so it never counts; its correction
// counts only if it corresponds to the capture.
#[test]
fn a_corrected_act_does_not_count() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    let capture = capture_of("act", "A7", &file, &digest("v1"), AFTER);
    store(&root, &capture);
    let original = crate::records::append(&root.join(crate::recorder::LOG), "human_act", &crate::records::APP_INTERFACE, crate::act_control::act_body(&capture)).unwrap();
    let mut correction = original.clone();
    correction["recordId"] = json!(crate::util::opaque_id("rec:app:").unwrap());
    correction["seq"] = json!(original["seq"].as_u64().unwrap() + 1);
    correction["corrects"] = original["recordId"].clone();
    correction["correctionReason"] = json!("purpose restated");
    correction["body"]["purpose"] = json!("A restated purpose.");
    crate::schema_validation::bundled().unwrap().validate(&correction).unwrap();
    let mut line = serde_json::to_string(&correction).unwrap();
    line.push('\n');
    let mut log = std::fs::OpenOptions::new().append(true).open(root.join(crate::recorder::LOG)).unwrap();
    std::io::Write::write_all(&mut log, line.as_bytes()).unwrap();
    let (all, outputs, read) = observe_with(&root);
    assert!(read.acts.is_empty());
    assert_eq!(read.unresolved.len(), 1, "only the correction is current, and it differs from the capture");
    assert_eq!(read.unresolved[0]["record"]["recordId"], correction["recordId"]);
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change", "evidence_limit"]);
    assert_eq!(waiting_arrivals(&all).len(), 1);
    std::fs::remove_dir_all(root).unwrap();
}

// m-7: an act captured at exactly the arrival's time is "after arrival"; a capture under
// another content method is incomparable (SB-1): neither counted nor said to differ.
#[test]
fn boundary_time_and_content_method() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    act(&root, "A7", &file, "v1", AT);
    let (_, outputs, _) = observe_with(&root);
    assert_eq!(outputs[2].1["relation"], "after arrival", "{outputs:#?}");
    let root2 = project("v1");
    let file2 = root2.join("out/summary.md");
    let legacy = json!({"method":crate::util::LEGACY_FILE_IDENTITY_METHOD,"value":crate::util::sha256_hex(b"v1")});
    let capture = capture_of("act", "A7", &file2, &legacy, AFTER);
    store(&root2, &capture);
    record_for(&root2, &capture, &crate::records::APP_INTERFACE);
    let (all, outputs, read) = observe_with(&root2);
    assert_eq!(read.acts.len(), 1);
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change"], "the same hex under another method is not the same content");
    assert_eq!(waiting_arrivals(&all).len(), 1);
    std::fs::remove_dir_all(root).unwrap();
    std::fs::remove_dir_all(root2).unwrap();
}

// m-1: AW-7 reads only a regular file inside the project, as one snapshot, without blocking.
#[test]
fn file_content_reads_only_a_regular_file_inside_the_project() {
    let root = project("v1");
    let outside = project("secret");
    assert_eq!(file_content(&root, "out/summary.md")["value"], crate::util::sha256_hex(b"v1"));
    assert_eq!(file_content(&root, "./out//summary.md")["value"], crate::util::sha256_hex(b"v1"));
    std::os::unix::fs::symlink(outside.join("out/summary.md"), root.join("out/link.md")).unwrap();
    let fifo = root.join("out/fifo");
    assert_eq!(unsafe { libc::mkfifo(std::ffi::CString::new(fifo.to_str().unwrap()).unwrap().as_ptr(), 0o600) }, 0);
    let started = std::time::Instant::now();
    for (declared, why) in [("out/link.md", "a link out of the project"), ("../x", "`..`"), ("out", "a directory"), ("out/fifo", "a FIFO"), ("out/missing.md", "absent")] {
        assert_eq!(file_content(&root, declared)["notObtainable"], true, "{why}");
    }
    assert!(started.elapsed() < std::time::Duration::from_secs(2), "a FIFO never blocks the read");
    std::fs::remove_dir_all(root).unwrap();
    std::fs::remove_dir_all(outside).unwrap();
}

// m-8: a change reported as `./out/summary.md`, or a declared path through a linked
// directory, binds the same file the act control names.
#[test]
fn normalized_and_linked_paths_bind_the_acted_file() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    let rely = act(&root, "A7", &file, "v1", AFTER);
    let (_, outputs, _) = observe_view(&root, &change_view("./out/summary.md"));
    assert_eq!(outputs[0].1["referents"][0]["subject"], RELY);
    assert_eq!(outputs[2].1["act"]["recordId"], rely.as_str(), "{outputs:#?}");
    // The declared output reached through a linked directory.
    std::os::unix::fs::symlink(root.join("out"), root.join("link")).unwrap();
    let text = workflow_text().replace("\"path\":\"out/summary.md\"", "\"path\":\"link/summary.md\"");
    let read = project_act_records(&root).unwrap();
    let (mut recorder, listed) = CheckpointRecorder::start(Ok(crate::workflow_declaration::read(&text).unwrap()));
    let outputs = recorder.observe(&change_view("link/summary.md"), &scope(&root), &entries(&listed), &mut || Ok(read.clone()));
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change", "act_counted", "disposition_change"], "{outputs:#?}");
    std::fs::remove_dir_all(root).unwrap();
}

// A message arrival binds no act, even one on a file named like the message; a file that is
// not readable binds none (A-5, SP-4).
#[test]
fn unidentified_or_unreadable_subjects_bind_no_act() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    act(&root, "A7", &file, "v1", AFTER);
    std::fs::remove_file(&file).unwrap();
    let (all, outputs, _) = observe_with(&root);
    assert_eq!(outputs[0].1["referents"][0]["content"]["notObtainable"], true);
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change"]);
    assert_eq!(waiting_arrivals(&all).len(), 1);
    let named = root.join("agentMessage m1");
    std::fs::write(&named, "Spacing report").unwrap();
    act(&root, "A4", &named, "Spacing report", AFTER);
    let items = vec![start_row(), row("turn-1", message("m1", "Spacing report"), 2, Some(2), Some(3))];
    let (_, outputs, _) = observe_view(&root, &view(items));
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change"]);
    std::fs::remove_dir_all(root).unwrap();
}

// RC-2: act records that cannot be read count nothing and are read again at the next
// observation; the arrival's act is then counted although no new native item arrived.
#[test]
fn unreadable_act_records_are_retried_and_counted_later() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    act(&root, "A7", &file, "v1", AFTER);
    let read = project_act_records(&root).unwrap();
    let (mut recorder, listed) = CheckpointRecorder::start(Ok(declaration()));
    let first = recorder.observe(&file_view(), &scope(&root), &entries(&listed), &mut || Err("incomplete".into()));
    assert_eq!(kinds(&first), ["checkpoint_arrival", "disposition_change"]);
    assert!(recorder.view()["actsLimit"].as_str().unwrap().contains("incomplete"));
    let mut all = entries(&listed);
    all.extend(entries(&first));
    let mut reads = 0;
    let second = recorder.observe(&file_view(), &scope(&root), &all, &mut || { reads += 1; Ok(read.clone()) });
    assert_eq!(kinds(&second), ["act_counted", "disposition_change"]);
    assert_eq!(reads, 1, "read once per observation");
    assert!(recorder.view()["actsLimit"].is_null());
    all.extend(entries(&second));
    let mut reads = 0;
    assert!(recorder.observe(&file_view(), &scope(&root), &all, &mut || { reads += 1; Ok(ActRead::default()) }).is_empty());
    assert_eq!(reads, 0, "nothing waits, so nothing is read");
    std::fs::remove_dir_all(root).unwrap();
}

// A-9: the resume point is the first run action evidenced as started after the counted act;
// an action started before the act carries continued_past (m-6), and with no start time no
// resume point is claimed.
#[test]
fn the_resume_point_follows_the_counted_act() {
    let root = project("v1");
    let file = root.join("out/summary.md");
    act(&root, "A7", &file, "v1", AFTER);
    let read = project_act_records(&root).unwrap();
    let started = |id: &str, n: u64, ms: Option<i64>| {
        let mut r = row("turn-1", command(id, "agent"), n, Some(10 * n), None);
        if let Some(ms) = ms {
            r["sourceFrame"] = json!({"method":"item/started","params":{"startedAtMs":ms}});
        }
        r
    };
    let after_act = 1_790_005_000_000i64; // 15:36:40, after the act at 15:00
    let before_act = 1_790_001_000_000i64; // 14:16:40
    for (rows, expected) in [
        (vec![started("c1", 3, Some(before_act)), started("c2", 4, Some(after_act))], vec!["continued_past", "run_resumed"]),
        (vec![started("c1", 3, None), started("c2", 4, Some(after_act))], vec![]),
    ] {
        let (mut recorder, listed) = CheckpointRecorder::start(Ok(declaration()));
        let mut items = file_view()["items"].as_array().unwrap().clone();
        let first = recorder.observe(&view(items.clone()), &scope(&root), &entries(&listed), &mut || Ok(ActRead::default()));
        let mut all = entries(&listed);
        all.extend(entries(&first));
        // The person's act is read; the agent's commands follow in a later observation.
        let counted = recorder.observe(&view(items.clone()), &scope(&root), &all, &mut || Ok(read.clone()));
        assert_eq!(kinds(&counted), ["act_counted", "disposition_change"]);
        all.extend(entries(&counted));
        items.extend(rows);
        let outputs = recorder.observe(&view(items), &scope(&root), &all, &mut || Ok(read.clone()));
        conformant(&outputs);
        assert_eq!(kinds(&outputs), expected, "{outputs:#?}");
        if let Some((_, resumed)) = outputs.iter().find(|(k, _)| *k == "run_resumed") {
            assert_eq!((resumed["firstActionRef"].as_str(), resumed["time"].as_str()), (Some("item:thread/turn-1/c2"), Some("2026-09-21T15:36:40.000Z")));
        }
        if let Some((_, past)) = outputs.iter().find(|(k, _)| *k == "continued_past") {
            assert_eq!(past["actionRef"], "item:thread/turn-1/c1");
        }
    }
    std::fs::remove_dir_all(root).unwrap();
}

// CE-4 (RC-5): a person-input request or an MCP elicitation received in the run while an
// arrival waits; associated only when exactly one waits; none recorded when none waits.
#[test]
fn requests_are_recorded_only_while_an_arrival_waits() {
    let root = std::path::PathBuf::from("/project/root");
    let request = |id: u64, method: &str, turn: &str, position: u64| json!({"requestIdentity":id,"generation":g(1),"method":method,"nativeParameters":{"threadId":"thread","turnId":turn,"itemId":"x"},"receiptPosition":position,"state":"outstanding"});
    let mut items = vec![start_row(), row("turn-1", message("m1", "Spacing report"), 2, Some(4), Some(5)), row("turn-0", message("m0", "earlier"), 0, Some(0), Some(0))];
    let mut v = view(items.clone());
    v["serverRequests"] = json!([request(1, "item/tool/requestUserInput", "turn-1", 3), request(2, "item/tool/requestUserInput", "turn-1", 6),
        request(3, "mcpServer/elicitation/request", "turn-1", 7), request(4, "item/commandExecution/requestApproval", "turn-1", 8), request(5, "item/tool/requestUserInput", "turn-0", 9)]);
    let (mut recorder, listed) = CheckpointRecorder::start(Ok(declaration()));
    let outputs = obs(&mut recorder, &v, &scope(&root), &entries(&listed));
    conformant(&outputs);
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change", "act_request", "act_request"], "before the arrival, an approval and a turn outside the run record none: {outputs:#?}");
    let one = &outputs[2].1;
    assert_eq!((one["form"].as_str(), one["requester"]["kind"].as_str(), one["association"].as_str()), (Some("supplier person-input request"), Some("agent"), Some("associated with the current arrival")));
    assert_eq!(one["arrival"], json!({"checkpoint":"CP-check","arrivalOrdinal":1}));
    assert_eq!((one["actKind"].as_str(), one["subject"].as_str(), one["purpose"].as_str()), (Some("not named by the request"), Some("not named by the request"), Some("not named by the request")));
    assert_eq!(one["evidence"]["ref"], "server-request:1/2");
    assert_eq!((outputs[3].1["form"].as_str(), outputs[3].1["requester"]["kind"].as_str()), (Some("MCP elicitation"), Some("not established (MCP server or agent)")));
    let mut all = entries(&listed);
    all.extend(entries(&outputs));
    assert!(obs(&mut recorder, &v, &scope(&root), &all).is_empty(), "each request is read once");
    // Two arrivals waiting: no association.
    items.push(row("turn-1", message("m2", "Spacing report"), 3, Some(10), Some(11)));
    let mut v = view(items);
    v["serverRequests"] = json!([request(6, "item/tool/requestUserInput", "turn-1", 12)]);
    let outputs = obs(&mut recorder, &v, &scope(&root), &all);
    conformant(&outputs);
    let body = &outputs.iter().find(|(k, _)| *k == "act_request").unwrap().1;
    assert_eq!(body["association"], "arrival association not established");
    assert!(body.get("arrival").is_none());
}

// AW-3: a kind (a) checkpoint on a harness capability with an active presence rule arrives
// at the start of each agent item of its kind; an inactive name or a host operation is not
// evaluable; a not-established checkpoint is CE-2 FB-04.
#[test]
fn harness_capability_calls_arrive_at_item_start() {
    let mut d: Value = serde_json::from_str(DECLARATION).unwrap();
    d["required_tools"].as_array_mut().unwrap().extend([
        json!({"name":"shell","class":"harness_capability","capability":"shell-command","purpose":"run","necessity":"required","stages":["Method"]}),
        json!({"name":"plan","class":"harness_capability","capability":"plan-update","purpose":"plan","necessity":"required","stages":["Method"]}),
    ]);
    let cp = |name: &str, tool: &str| json!({"name":name,"required_act":"A4","reached_when":{"kind":"before_dispatch","tool":tool},"subject":{"class":"targets_of_held_call"},"position":"before","scope":"s","purpose":"p","actor":"the_person","expected_act_evidence":{"capturing_surface":"app_act_control","description":"A4"}});
    d["checkpoints"] = json!([cp("CP-shell", "shell"), cp("CP-plan", "plan"), cp("CP-host", "add-support"), {"name":"CP-half"}]);
    let text = format!("# Fixture\n\n```workflow-declaration\n{d}\n```\n");
    let (mut recorder, listed) = CheckpointRecorder::start(Ok(crate::workflow_declaration::read(&text).unwrap()));
    conformant(&listed);
    let status: Vec<(&str, &str)> = listed.iter().filter(|(k, _)| *k == "checkpoint_listed").map(|(_, b)| (b["checkpoint"].as_str().unwrap(), b["evaluability"]["status"].as_str().unwrap())).collect();
    assert_eq!(status, [("CP-shell", "evaluable with limit"), ("CP-plan", "not evaluable"), ("CP-host", "not evaluable")], "{listed:#?}");
    assert_eq!(listed[3], ("declaration_finding", json!({"checkpoint":"CP-half","finding":"not established","code":"FB-04"})));
    let root = std::path::PathBuf::from("/project/root");
    let mut agent = row("turn-1", command("c2", "agent"), 3, Some(4), None);
    agent["sourceFrame"] = json!({"method":"item/started","params":{"startedAtMs":1_790_000_000_000i64}});
    let items = vec![start_row(), row("turn-1", command("c1", "userShell"), 2, Some(2), None), agent];
    let outputs = obs(&mut recorder, &view(items), &scope(&root), &entries(&listed));
    conformant(&outputs);
    assert_eq!(kinds(&outputs), ["checkpoint_arrival", "disposition_change"], "the person's own command is not the run's call");
    let arrival = &outputs[0].1;
    assert_eq!((arrival["checkpoint"].as_str(), arrival["event"]["ref"].as_str()), (Some("CP-shell"), Some("item:thread/turn-1/c2")));
    assert_eq!(arrival["event"]["evidencedTime"]["source"], "supplier_item_time");
    assert_eq!(arrival["limits"][0], CALL_LIMIT);
    assert_eq!(arrival["referents"][0]["content"]["notObtainable"], true);
}
