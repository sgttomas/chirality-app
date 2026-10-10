//! The checkpoint recorder's first slice: CE-1 listing, AW-6/AW-7 arrivals
//! from live-observed native items only, CE-12/CE-11 from RC-9 run actions,
//! CE-17 waiting arrivals, and the EXEC entry-body schema.
use super::*;

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
fn entries(outputs: &[Output]) -> Vec<Value> {
    outputs.iter().map(|(k, b)| json!({"kind":k,"body":b})).collect()
}

#[test]
fn ce1_lists_recognized_checkpoints_with_their_evaluability() {
    let (recorder, listed) = CheckpointRecorder::start(Ok(declaration()));
    valid(&listed);
    let names: Vec<&str> = listed.iter().map(|(_, b)| b["checkpoint"].as_str().unwrap()).collect();
    assert_eq!(names, ["CP-check", "CP-rely", "CP-accept"], "the invalid checkpoint is never listed (§4.14)");
    assert!(listed.iter().all(|(k, _)| *k == "checkpoint_listed"));
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
    let mut outputs = recorder.observe(&v, &scope(&root), &entries(&listed));
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
    assert!(arrival["limits"].as_array().unwrap().iter().any(|l| l.as_str().unwrap().contains("not counted")));
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
    assert!(recorder.observe(&v, &scope(&root), &recorded).is_empty(), "each item is read once");
    // A later agent command adds no second continued_past; the person's own command never does.
    let mut more = items.clone();
    more.push(row("turn-1", command("c1", "userShell"), 10, Some(18), None));
    more.push(row("turn-1", command("c2", "agent"), 11, Some(19), None));
    assert!(recorder.observe(&view(more.clone()), &scope(&root), &recorded).is_empty());
    // CE-11: once the record reads the arrival performed, the next run action is its resume point.
    recorded.push(json!({"kind":"disposition_change","body":{"arrival":{"checkpoint":"CP-check","arrivalOrdinal":1},"disposition":"performed","performanceOrdinal":1}}));
    more.push(row("turn-1", command("c3", "agent"), 12, Some(20), None));
    outputs = recorder.observe(&view(more), &scope(&root), &recorded);
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
    let outputs = recorder.observe(&view(items.clone()), &scope(&root), &[]);
    let ordinals: Vec<u64> = outputs.iter().filter(|(k, _)| *k == "checkpoint_arrival").map(|(_, b)| b["arrivalOrdinal"].as_u64().unwrap()).collect();
    assert_eq!(ordinals, [1, 2], "OP-4: each completed message carrying the line is a production");
    let (mut fresh, _) = CheckpointRecorder::start(Ok(declaration()));
    let mut unknown = scope(&root);
    unknown.start = crate::run_offers::RunStart::Unknown;
    assert!(fresh.observe(&view(items.clone()), &unknown, &[]).is_empty(), "a run whose start is not in this view records nothing");
    let mut other = view(items.clone());
    other["home"] = json!("another-home");
    assert!(fresh.observe(&other, &scope(&root), &[]).is_empty(), "another home's view");
    let mut other_session = view(items);
    for item in other_session["items"].as_array_mut().unwrap() { item["receipt"]["generation"]["appSession"] = json!("earlier"); }
    assert!(fresh.observe(&other_session, &scope(&root), &[]).is_empty(), "rows not received in this App session");
}

#[test]
fn file_paths_compare_as_text_against_the_project_root() {
    let root = std::path::Path::new("/project/root");
    assert!(same_path("out/summary.md", "out/summary.md", root));
    assert!(same_path("/project/root/out/summary.md", "out/summary.md", root));
    assert!(!same_path("/project/rootx/out/summary.md", "out/summary.md", root));
    assert!(!same_path("/elsewhere/out/summary.md", "out/summary.md", root));
    assert!(!same_path("./out/summary.md", "out/summary.md", root), "no normalization is claimed (U-E26)");
    assert_eq!(first_line("\n \t\n  x  \ny"), Some("x"));
    assert_eq!(first_line(" \n "), None);
}
