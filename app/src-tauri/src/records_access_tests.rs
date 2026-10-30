//! The agents' records capability (RS §13.9): scope, bounds, quoting, the read
//! log, refusals, and a fake-peer journey in which the agent calls it.
use super::*;
use std::time::{Duration, Instant};

struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let path = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("records-access-").unwrap());
        std::fs::create_dir_all(path.join("app-data/runtime")).unwrap();
        Self(path)
    }
    fn project(&self, name: &str) -> PathBuf {
        let p = self.0.join(name);
        std::fs::create_dir_all(&p).unwrap();
        p
    }
    fn read_log(&self) -> PathBuf {
        self.0.join("app-data/runtime/records-reads.jsonl")
    }
    fn logged(&self) -> Vec<Value> {
        std::fs::read_to_string(self.read_log()).unwrap_or_default().lines().map(|l| serde_json::from_str(l).unwrap()).collect()
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

/// `entries` schema-valid RS entries of run `run` by one writer; every third
/// a large one when `large`.
fn write_run(project: &Path, run: &str, entries: usize, marker: &str, large: bool) {
    use std::io::Write;
    let log = crate::storage::project_log(project, Some(run), "app-writer:local").unwrap();
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    let mut out = std::fs::OpenOptions::new().create(true).append(true).open(&log).unwrap();
    for seq in 1..=entries as u64 {
        let (kind, body) = if seq == 1 {
            ("evidence_limit", json!({"label":"unresolvable reference","subjectRef":marker,"detail":"first"}))
        } else if seq == entries as u64 {
            ("run_ended", json!({"stoppedBy":"the person","cause":"ended by the person","waitingArrivals":[]}))
        } else {
            let detail = if large && seq % 3 == 0 { "x".repeat(ENTRY_LIMIT + 10) } else { format!("{marker} {seq}") };
            ("evidence_limit", json!({"label":"unresolvable reference","subjectRef":marker,"detail":detail}))
        };
        let entry = crate::records::envelope(kind, &crate::records::APP_WRITER, body, format!("rec:app:{marker}-{run}-{seq}"), seq, Some(run), Some("2026-10-12T00:00:00.000Z"));
        writeln!(out, "{entry}").unwrap();
    }
}
/// One A7 act record outside any run, on `subject`, citing capture `id`, and
/// the capture's evidence file in the project (never returned).
fn write_act(project: &Path, id: &str, subject: &str, secret: &str) {
    use std::io::Write;
    let capture = json!({"format":"chirality.aac.capture-evidence","formatVersion":"0.3","captureId":id,"offerId":format!("offer:{id}"),
        "offerDigest":{"method":"aac-offer-digest/0.1","value":"0".repeat(64)},"choice":"act","actKind":"A7",
        "actor":{"osAccount":"fixture","identityVerified":false},"boundSubject":[subject],"boundContent":[{"method":"chirality.app.exact-bytes.sha256/v1","value":crate::util::sha256_hex(b"v1")}],
        "scope":"The summary file.","purpose":"You decide.","capturedAt":"2026-10-12T00:00:00.000Z","surface":"App interface","inputSource":"host-native-confirmation",
        "answers":{"standing":"no arrival: a standing act (RC-6)"},"evidenceLimits":["identity not verified"]});
    let path = crate::storage::write_capture_path(project, id).unwrap();
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    let mut evidence = capture.clone();
    evidence["fixtureSecret"] = json!(secret);
    std::fs::write(path, serde_json::to_vec(&evidence).unwrap()).unwrap();
    let kind = crate::records::capture_record_kind(&capture).unwrap();
    let log = crate::storage::project_log(project, None, "fixture-act-writer").unwrap();
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    let seq = crate::records::read_log(&log).0.len() as u64 + 1;
    let entry = crate::records::envelope(kind, &crate::records::APP_INTERFACE, crate::act_control::act_body(&capture), format!("rec:app:act-{id}"), seq, None, None);
    let mut out = std::fs::OpenOptions::new().create(true).append(true).open(&log).unwrap();
    writeln!(out, "{entry}").unwrap();
}
fn call(n: u64, arguments: Value) -> Call {
    Call { app_session: "app-session:fixture".into(), generation: "g:fixture".into(), request: json!(n), thread: "thread".into(), turn: "turn".into(), call: format!("call-{n}"), arguments }
}
fn returned(answer: &Value) -> Value {
    assert_eq!(answer["contentItems"].as_array().unwrap().len(), 1);
    assert_eq!(answer["contentItems"][0]["type"], "inputText");
    serde_json::from_str(answer["contentItems"][0]["text"].as_str().unwrap()).unwrap()
}
fn capability(f: &Scratch, project: &Path) -> RecordsCapability {
    RecordsCapability::at(project, f.read_log()).unwrap()
}

#[test]
fn the_definition_is_a_valid_dynamic_tool_and_the_log_schema_is_the_design_copy() {
    assert_eq!(LOG_SCHEMA.as_bytes(), include_bytes!("../../../execution/PKG-04/DEL-04-03/Work/records-read-log.entry.schema.json"), "the resource copy is byte-identical to the Design schema");
    let mut schema: Value = serde_json::from_str(include_str!("../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json")).unwrap();
    schema["$ref"] = json!("#/definitions/v2/DynamicToolSpec");
    jsonschema::options().offline().build(&schema).unwrap().validate(&definition()).unwrap();
    jsonschema::options().build(&definition()["inputSchema"]).unwrap();
}

#[test]
fn only_this_projects_records_are_returned_never_keys_captures_or_another_project() {
    let f = Scratch::new();
    let (a, b) = (f.project("project-a"), f.project("project-b"));
    write_run(&a, "run:a", 4, "MARK-A", false);
    write_run(&b, "run:b", 4, "MARK-B", false);
    write_act(&a, "cap:a1", "out/summary.md", "CAPTURE-BYTES-A");
    // Keys and other files under the project: never read.
    std::fs::create_dir_all(a.join(".chirality/keys")).unwrap();
    std::fs::write(a.join(".chirality/keys/seal.jsonl"), "{\"key\":\"SECRET-KEY\"}\n").unwrap();
    let keys = f.0.join("app-data/capture-seal");
    std::fs::create_dir_all(&keys).unwrap();
    std::fs::write(keys.join("key.jsonl"), "SECRET-KEY-OUTSIDE\n").unwrap();
    let cap = capability(&f, &a);
    let mut text = String::new();
    for (n, args) in [(1, json!({"operation":"list_runs"})), (2, json!({"operation":"read_run","run":"run:a"})), (3, json!({"operation":"read_acts"})), (4, json!({"operation":"read_run","run":"run:b"}))] {
        let answer = cap.answer(&call(n, args), Some(a.to_str().unwrap()));
        assert_eq!(answer["success"], true);
        text.push_str(answer["contentItems"][0]["text"].as_str().unwrap());
    }
    assert!(text.contains("MARK-A") && text.contains("rec:app:act-cap:a1"), "this project's runs and acts");
    for never in ["MARK-B", "run:b\",\"entries", "SECRET-KEY", "CAPTURE-BYTES-A", a.to_str().unwrap(), f.0.to_str().unwrap()] {
        assert!(!text.contains(never), "{never} returned");
    }
    let other = returned(&cap.answer(&call(5, json!({"operation":"read_run","run":"run:b"})), Some(a.to_str().unwrap())));
    assert_eq!(other["items"], json!([]), "another project's run is not in this project's records");
    // A conversation in another project is refused, and the refusal is recorded.
    let refused = cap.answer(&call(6, json!({"operation":"list_runs"})), Some(b.to_str().unwrap()));
    assert_eq!(refused["success"], false);
    assert!(returned(&refused)["refused"].as_str().unwrap().contains("not in this App's current project"));
    assert_eq!(f.logged().last().unwrap()["outcome"], "refused");
    assert!(!cap.offered_for(b.to_str().unwrap()) && cap.offered_for(a.to_str().unwrap()));
    assert!(RecordsCapability::at(&a, a.join("reads.jsonl")).is_err(), "the read log is never in the project");
}

#[test]
fn pages_are_bounded_and_continue_by_cursor() {
    let f = Scratch::new();
    let a = f.project("project");
    write_run(&a, "run:big", 120, "BIG", true);
    let cap = capability(&f, &a);
    let first = returned(&cap.answer(&call(1, json!({"operation":"read_run","run":"run:big"})), Some(a.to_str().unwrap())));
    assert_eq!(first["items"].as_array().unwrap().len(), DEFAULT_ITEMS);
    assert_eq!(first["next"], "o:20");
    let mut seen = 0;
    let mut cursor = Value::Null;
    let mut n = 10;
    loop {
        let mut args = json!({"operation":"read_run","run":"run:big","limit":MAX_ITEMS});
        if !cursor.is_null() { args["cursor"] = cursor.clone(); }
        n += 1;
        let answer = cap.answer(&call(n, args), Some(a.to_str().unwrap()));
        let text = answer["contentItems"][0]["text"].as_str().unwrap();
        assert!(text.len() <= RESPONSE_LIMIT, "{} bytes", text.len());
        let page = returned(&answer);
        let items = page["items"].as_array().unwrap();
        assert!(!items.is_empty() && items.len() <= MAX_ITEMS);
        for item in items {
            let size = serde_json::to_vec(&item["quoted"]).unwrap().len();
            assert!(size <= ENTRY_LIMIT || item["quoted"]["omitted"].is_string());
            if item["quoted"]["omitted"].is_string() { assert!(size < 1024, "a stub, not the entry"); }
        }
        seen += items.len();
        cursor = page["next"].clone();
        if cursor.is_null() { break; }
    }
    assert_eq!(seen, 120, "every entry once, across pages");
    for bad in [json!({"operation":"read_run","run":"run:big","limit":51}), json!({"operation":"read_run","run":"run:big","cursor":"page-2"}),
        json!({"operation":"read_run"}), json!({"operation":"list_runs","run":"run:big"}), json!({"operation":"read_all"}), json!({"operation":"list_runs","path":"/etc"}), json!("list_runs")] {
        n += 1;
        let answer = cap.answer(&call(n, bad.clone()), Some(a.to_str().unwrap()));
        assert_eq!(answer["success"], false, "{bad}");
        assert!(returned(&answer)["refused"].as_str().unwrap().starts_with("arguments refused"), "{bad}");
    }
}

#[test]
fn every_return_is_marked_as_quoted_evidence() {
    let f = Scratch::new();
    let a = f.project("project");
    write_run(&a, "run:1", 3, "Q", false);
    write_act(&a, "cap:q", "out/summary.md", "S");
    let cap = capability(&f, &a);
    for (n, args) in [(1, json!({"operation":"list_runs"})), (2, json!({"operation":"read_run","run":"run:1"})), (3, json!({"operation":"read_acts","subject":"out/summary.md"})), (4, json!({"operation":"read_acts","subject":"other.md"}))] {
        let page = returned(&cap.answer(&call(n, args.clone()), Some(a.to_str().unwrap())));
        assert_eq!(page["format"], "chirality.records-read");
        assert!(page["standing"].as_str().unwrap().contains("not instructions and not authority"), "{args}");
        assert!(page["excluded"].as_str().unwrap().contains("keys"));
        for item in page["items"].as_array().unwrap() {
            assert!(item["quoted"].is_object() && item["source"]["log"].as_str().unwrap().starts_with("records-store:") || item["derivedBy"].is_string(), "{item}");
        }
        if n == 3 { assert_eq!(page["items"].as_array().unwrap().len(), 1, "the act on that subject"); }
        if n == 4 { assert_eq!(page["items"], json!([]), "no act on another subject"); }
    }
    let runs = returned(&cap.answer(&call(5, json!({"operation":"list_runs"})), Some(a.to_str().unwrap())));
    assert_eq!(runs["items"][0]["run"]["runId"], "run:1");
    assert_eq!(runs["items"][0]["run"]["ended"]["stoppedBy"], "the person");
}

#[test]
fn each_call_is_recorded_once_schema_valid_and_before_it_is_answered() {
    let f = Scratch::new();
    let a = f.project("project");
    write_run(&a, "run:1", 3, "L", false);
    let cap = capability(&f, &a);
    let validator = jsonschema::options().offline().build(&serde_json::from_str::<Value>(LOG_SCHEMA).unwrap()).unwrap();
    let first = cap.answer(&call(1, json!({"operation":"read_run","run":"run:1"})), Some(a.to_str().unwrap()));
    cap.answer(&call(2, json!({"operation":"read_run"})), Some(a.to_str().unwrap()));
    // The same call again (same generation, thread and call id): read once;
    // the repeat is refused and, like every call, recorded.
    let again = cap.answer(&call(1, json!({"operation":"read_run","run":"run:1"})), Some(a.to_str().unwrap()));
    assert_eq!(again["success"], false);
    assert!(returned(&again)["refused"].as_str().unwrap().contains("answered already"));
    let logged = f.logged();
    assert_eq!(logged.len(), 3, "every call is one line");
    assert_eq!((logged[2]["callId"].as_str(), logged[2]["outcome"].as_str()), (Some("call-1"), Some("refused")));
    for entry in &logged { validator.validate(entry).unwrap_or_else(|e| panic!("{e}: {entry}")); }
    let ids: HashSet<&str> = logged.iter().map(|e| e["readId"].as_str().unwrap()).collect();
    assert_eq!(ids.len(), 3, "each line its own read identity");
    assert_eq!(logged[0]["outcome"], "returned");
    assert_eq!(logged[0]["readId"], returned(&first)["readId"]);
    assert_eq!(logged[0]["returned"]["content"]["value"], json!(crate::util::sha256_hex(first["contentItems"][0]["text"].as_str().unwrap().as_bytes())), "the returned bytes' identity");
    assert_eq!(logged[0]["returned"]["recordIds"].as_array().unwrap().len(), 3);
    assert_eq!((logged[1]["outcome"].as_str(), logged[1]["refusal"].is_string()), (Some("refused"), true));
    assert_eq!(cap.snapshot()["recentReads"].as_array().unwrap().len(), 3);
    // A read that cannot be recorded returns nothing.
    std::fs::remove_dir_all(f.0.join("app-data/runtime")).unwrap();
    let unrecorded = cap.answer(&call(3, json!({"operation":"read_run","run":"run:1"})), Some(a.to_str().unwrap()));
    assert_eq!(unrecorded["success"], false);
    let page = returned(&unrecorded);
    assert!(page["refused"].as_str().unwrap().contains("could not be recorded") && page["items"] == json!([]), "{page}");
    // A torn final line in the log refuses further appends; its bytes stay.
    std::fs::create_dir_all(f.0.join("app-data/runtime")).unwrap();
    std::fs::write(f.read_log(), b"{\"torn\":").unwrap();
    assert_eq!(cap.answer(&call(4, json!({"operation":"list_runs"})), Some(a.to_str().unwrap()))["success"], false);
    assert_eq!(std::fs::read(f.read_log()).unwrap(), b"{\"torn\":");
    assert!(cap.snapshot()["readLogLimit"].as_str().unwrap().contains("unclosed final line"), "the cause is shown with the capability");
}

fn text_of(answer: &Value) -> &str {
    answer["contentItems"][0]["text"].as_str().unwrap()
}
fn write_lines(project: &Path, run: &str, lines: &[String]) {
    let log = crate::storage::project_log(project, Some(run), "app-writer:local").unwrap();
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    std::fs::write(&log, lines.iter().map(|l| format!("{l}\n")).collect::<String>()).unwrap();
}

// #1313 review B1 probes: the bound holds on the final text, and no refused
// line's content or validator text is returned.
#[test]
fn probe_refused_lines_large_identities_and_large_workflow_names_stay_bounded() {
    let f = Scratch::new();
    let a = f.project("project");
    let cap = capability(&f, &a);
    // (a) 25 lines whose seq is a 4 KB string: refused by the reader.
    let refused: Vec<String> = (0..25).map(|n| json!({"format":"chirality.rs.record","formatVersion":"0.1","recordId":format!("rec:bad-{n}"),"kind":"evidence_limit",
        "recorder":{"role":"App writer","identity":"app-writer:local"},"context":{"surface":"App"},"runId":"run:a","seq":format!("REFUSED-CONTENT-{}", "s".repeat(4096)),
        "writtenAt":"w","body":{"label":"unresolvable reference","subjectRef":"x","detail":"y"}}).to_string()).collect();
    write_lines(&a, "run:a", &refused);
    let answer = cap.answer(&call(1, json!({"operation":"read_run","run":"run:a"})), Some(a.to_str().unwrap()));
    assert!(text_of(&answer).len() <= RESPONSE_LIMIT, "{} bytes", text_of(&answer).len());
    assert!(!text_of(&answer).contains("REFUSED-CONTENT"), "refused content is never returned");
    let page = returned(&answer);
    assert!(page["limits"].as_array().unwrap().iter().all(|l| l.as_str().unwrap().len() <= 400 && !l.as_str().unwrap().contains("schema")), "{}", page["limits"]);
    assert!(page["limits"][0].as_str().unwrap().contains("line 1 is not a valid record (not read)"));
    // (b) a 40 KB recordId: returned as a stub whose fields are bounded.
    let b = f.project("project-b");
    let big_id = format!("rec:app:{}", "r".repeat(40 * 1024));
    let entry = crate::records::envelope("evidence_limit", &crate::records::APP_WRITER, json!({"label":"unresolvable reference","subjectRef":"x","detail":"y"}), big_id.clone(), 1, Some("run:b"), None);
    write_lines(&b, "run:b", &[entry.to_string()]);
    let cap_b = capability(&f, &b);
    for (n, args) in [(2, json!({"operation":"read_run","run":"run:b"})), (3, json!({"operation":"list_runs"}))] {
        let answer = cap_b.answer(&call(n, args), Some(b.to_str().unwrap()));
        assert!(text_of(&answer).len() <= RESPONSE_LIMIT, "{} bytes", text_of(&answer).len());
        assert!(!text_of(&answer).contains(&big_id));
    }
    assert!(f.logged().iter().all(|e| serde_json::to_string(e).unwrap().len() < 8 * 1024), "the read log's entries are bounded too");
    // (c) a 60 KB workflow name in run_opened.
    let c = f.project("project-c");
    let mut opened: Value = serde_json::from_str(include_str!("../../../execution/PKG-04/DEL-04-03/Work/RS_RECORD.valid.app-run.example.jsonl").lines().next().unwrap()).unwrap();
    opened["runId"] = json!("run:c");
    opened["body"]["runId"] = json!("run:c");
    opened["body"]["workflow"]["name"] = json!("W".repeat(60 * 1024));
    write_lines(&c, "run:c", &[opened.to_string()]);
    let cap_c = capability(&f, &c);
    for (n, args) in [(4, json!({"operation":"list_runs"})), (5, json!({"operation":"read_run","run":"run:c"}))] {
        let answer = cap_c.answer(&call(n, args), Some(c.to_str().unwrap()));
        let text = text_of(&answer);
        assert!(text.len() <= RESPONSE_LIMIT && !text.contains(&"W".repeat(1024)), "{} bytes", text.len());
    }
    // The bound is applied to the final text: a page that does not fit keeps fewer items.
    let d = f.project("project-d");
    let lines: Vec<String> = (1..=60).map(|seq| crate::records::envelope("evidence_limit", &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"x","detail":"d".repeat(ENTRY_LIMIT - 600)}), format!("rec:app:d-{seq}"), seq, Some("run:d"), None).to_string()).collect();
    write_lines(&d, "run:d", &lines);
    let cap_d = capability(&f, &d);
    let page = cap_d.answer(&call(7, json!({"operation":"read_run","run":"run:d","limit":50})), Some(d.to_str().unwrap()));
    assert!(text_of(&page).len() <= RESPONSE_LIMIT);
    let page = returned(&page);
    let kept = page["items"].as_array().unwrap().len();
    assert!(kept >= 1 && kept < 50 && page["next"] == json!(format!("o:{kept}")), "{kept} {}", page["next"]);
}

#[test]
fn library_acts_are_never_returned_and_lines_are_the_files_own() {
    let f = Scratch::new();
    let a = f.project("project");
    // The project is also a workflow library: its A15 acts log is the library's.
    let library = crate::storage::library_log(&a);
    std::fs::create_dir_all(library.parent().unwrap()).unwrap();
    let a15 = crate::records::envelope("evidence_limit", &crate::records::APP_INTERFACE, json!({"label":"unresolvable reference","subjectRef":"LIBRARY-ACT","detail":"y"}), "rec:app:lib-1".into(), 1, None, None);
    std::fs::write(&library, format!("{a15}\n")).unwrap();
    // A run log with an invalid line and a blank line before its entries.
    let first = crate::records::envelope("evidence_limit", &crate::records::APP_WRITER, json!({"label":"unresolvable reference","subjectRef":"x","detail":"first"}), "rec:app:l-1".into(), 1, Some("run:l"), None);
    let second = crate::records::envelope("evidence_limit", &crate::records::APP_WRITER, json!({"label":"unresolvable reference","subjectRef":"x","detail":"second"}), "rec:app:l-2".into(), 2, Some("run:l"), None);
    write_lines(&a, "run:l", &["{\"not\":\"a record\"}".into(), String::new(), first.to_string(), second.to_string()]);
    let cap = capability(&f, &a);
    let acts = cap.answer(&call(1, json!({"operation":"read_acts"})), Some(a.to_str().unwrap()));
    let run = cap.answer(&call(2, json!({"operation":"read_run","run":"run:l"})), Some(a.to_str().unwrap()));
    for answer in [&acts, &run] { assert!(!text_of(answer).contains("LIBRARY-ACT") && !text_of(answer).contains("rec:app:lib-1")); }
    let page = returned(&run);
    assert_eq!(page["items"].as_array().unwrap().iter().map(|i| i["source"]["line"].as_u64().unwrap()).collect::<Vec<_>>(), [3, 4], "the file's own lines");
    assert!(page["limits"].as_array().unwrap().iter().any(|l| l.as_str().unwrap().ends_with("line 1 is not a valid record (not read)")));
}

#[test]
fn only_the_canonical_cursor_continues_a_page() {
    let f = Scratch::new();
    let a = f.project("project");
    write_run(&a, "run:c", 30, "C", false);
    let cap = capability(&f, &a);
    let next = returned(&cap.answer(&call(1, json!({"operation":"read_run","run":"run:c"})), Some(a.to_str().unwrap())))["next"].clone();
    assert_eq!(next, "o:20");
    for (n, cursor) in [(2, "o:+20"), (3, "o:020"), (4, "o: 20"), (5, "o:20 "), (6, "o:-1")] {
        let answer = cap.answer(&call(n, json!({"operation":"read_run","run":"run:c","cursor":cursor})), Some(a.to_str().unwrap()));
        assert_eq!(answer["success"], false, "{cursor}");
    }
    let rest = returned(&cap.answer(&call(7, json!({"operation":"read_run","run":"run:c","cursor":next})), Some(a.to_str().unwrap())));
    assert_eq!(rest["items"].as_array().unwrap().len(), 10);
    assert!(rest["next"].is_null());
}

/// A fake Codex: answers the handshake, `thread/start` and `turn/start`; after
/// a turn starts it calls the offered records tool twice, as the model would.
const PEER: &str = r#"#!/usr/bin/python3
import sys,json,os
if '--version' in sys.argv:
 print('codex-cli 0.160.0');sys.exit(0)
def emit(v):print(json.dumps(v),flush=True)
def thread(cwd,identity='thread'):return {'id':identity,'cliVersion':'0.160.0','createdAt':1,'updatedAt':2,'cwd':cwd,'ephemeral':False,'modelProvider':'fixture-provider','preview':'fixture','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':'idle'},'turns':[]}
threads={}
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log:log.write(json.dumps(f)+'\n')
 method=f.get('method')
 if 'id' not in f or method is None:continue
 if method=='initialize':emit({'id':f['id'],'result':{'userAgent':'records-capability-fixture'}})
 elif method=='thread/start':
  cwd=f['params'].get('cwd') or os.getcwd()
  threads['thread']=cwd
  emit({'id':f['id'],'result':{'thread':thread(cwd),'model':f['params'].get('model'),'modelProvider':f['params'].get('modelProvider'),'cwd':cwd,'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}})
 elif method=='thread/fork':
  src=f['params']['threadId'];cwd=threads[src]
  if os.path.exists('fork-cwd'):cwd=open('fork-cwd').read()
  t=thread(cwd,'fork');t['forkedFromId']=src;threads['fork']=cwd
  emit({'id':f['id'],'result':{'thread':t,'model':'fixture-model','modelProvider':'fixture-provider','cwd':cwd,'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}})
 elif method=='turn/start':
  tid=f['params']['threadId']
  emit({'id':f['id'],'result':{'turn':{'id':'turn','status':'inProgress','items':[],'error':None,'itemsView':'summary'}}})
  emit({'id':'records-call-1','method':'item/tool/call','params':{'threadId':tid,'turnId':'turn','callId':'call-1','tool':'chirality_records_read_v1','namespace':None,'arguments':{'operation':'read_run','run':'run:journey'}}})
  emit({'id':'records-call-2','method':'item/tool/call','params':{'threadId':tid,'turnId':'turn','callId':'call-2','tool':'chirality_records_read_v1','namespace':None,'arguments':{'operation':'read_run'}}})
  emit({'id':'other-tool','method':'item/tool/call','params':{'threadId':tid,'turnId':'turn','callId':'call-3','tool':'not_offered','namespace':None,'arguments':{}}})
 else:emit({'id':f['id'],'result':{}})
"#;

#[test]
fn fake_peer_journey_the_agent_reads_this_projects_records_through_the_host() {
    use std::os::unix::fs::PermissionsExt;
    let f = Scratch::new();
    let project = f.project("project");
    for name in ["account", "probe"] { std::fs::create_dir_all(f.0.join(name)).unwrap(); }
    write_run(&project, "run:journey", 3, "JOURNEY", false);
    let script = f.0.join("peer.py");
    std::fs::write(&script, PEER).unwrap();
    std::fs::set_permissions(&script, std::fs::Permissions::from_mode(0o700)).unwrap();
    let mut cfg = crate::hosting::HostConfig::new(script, f.0.join("account"), f.0.join("probe"), project.clone());
    cfg.allow_unverified_dev = true;
    cfg.wait_limit = Duration::from_secs(2);
    let host = std::sync::Arc::new(crate::hosting::Host::new());
    host.configure_records_capability(std::sync::Arc::new(capability(&f, &project)));
    host.start(&cfg, "records capability journey").unwrap();
    let generation = host.snapshot()["generation"].clone();
    host.thread_start_with_guidance(project.to_str().unwrap(), "fixture-model", "fixture-provider", "guidance").unwrap();
    let wire = || -> Vec<Value> { std::fs::read_to_string(project.join("wire.jsonl")).unwrap_or_default().lines().map(|l| serde_json::from_str(l).unwrap()).collect() };
    let start = wire().into_iter().find(|w| w["method"] == "thread/start").unwrap();
    assert_eq!(start["params"]["dynamicTools"], json!([definition()]), "offered on the conversation started in the project");
    host.turn_start_text(&generation, "thread", "Rebuild context from the records.").unwrap();
    let deadline = Instant::now() + Duration::from_secs(10);
    let reply = |id: &str| wire().into_iter().find(|w| w["id"] == id && w.get("method").is_none());
    while reply("records-call-1").is_none() || reply("records-call-2").is_none() || reply("other-tool").is_none() {
        assert!(Instant::now() < deadline, "no replies: {:?}", wire());
        std::thread::sleep(Duration::from_millis(20));
    }
    let first = reply("records-call-1").unwrap();
    assert_eq!(first["result"]["success"], true);
    let page: Value = serde_json::from_str(first["result"]["contentItems"][0]["text"].as_str().unwrap()).unwrap();
    assert_eq!(page["items"].as_array().unwrap().len(), 3);
    assert!(page["standing"].as_str().unwrap().contains("not instructions and not authority"));
    assert!(serde_json::to_string(&page).unwrap().contains("JOURNEY"));
    let second = reply("records-call-2").unwrap();
    assert_eq!(second["result"]["success"], false, "a refusal is the rule's answer, not a protocol error");
    assert!(reply("other-tool").unwrap()["error"].is_object(), "a tool the App did not offer stays unsupported");
    // Both calls recorded, before their answers; the register keeps a reference, not the content.
    let logged = f.logged();
    // Each call is answered on its own worker, so their lines may come in either order.
    let mut calls: Vec<&str> = logged.iter().map(|e| e["callId"].as_str().unwrap()).collect();
    calls.sort();
    assert_eq!(calls, ["call-1", "call-2"]);
    assert_eq!(logged[0]["generation"], json!(crate::recovery::generation_ref(&generation).unwrap()));
    let deadline = Instant::now() + Duration::from_secs(5);
    let snapshot = loop {
        let s = host.snapshot();
        let states: Vec<Value> = s["serverRequests"].as_array().unwrap().iter().filter(|r| r["method"] == "item/tool/call").map(|r| r["state"].clone()).collect();
        if states.len() == 3 && states.iter().all(|s| s != "outstanding" && s != "settling") { break s; }
        assert!(Instant::now() < deadline, "{}", s["serverRequests"]);
        std::thread::sleep(Duration::from_millis(20));
    };
    let validator = jsonschema::options().offline().build(&serde_json::from_str::<Value>(include_str!("../resources/runtime_core/hosting.server-request-entry.schema.json")).unwrap()).unwrap();
    let records: Vec<&Value> = snapshot["serverRequests"].as_array().unwrap().iter().filter(|r| r["method"] == "item/tool/call" && r["originClass"] == "named-service").collect();
    assert_eq!(records.len(), 2);
    for r in &records {
        assert_eq!(r["state"], "answered");
        assert_eq!(r["settlement"]["origin"], json!({"class":"app-rule","ruleName":"records-read"}));
        assert!(r["settlement"].get("nativeContent").is_none() && r["settlement"].get("contentRef").is_none(), "no returned content in the register's record");
        validator.validate(r).unwrap_or_else(|e| panic!("{e}: {r}"));
    }
    // The read log, joined by generation and request identity, accounts for each answer.
    for r in &records {
        assert!(logged.iter().any(|e| e["requestIdentity"] == json!(serde_json::to_string(&r["requestIdentity"]).unwrap())));
    }
    assert!(!serde_json::to_string(&snapshot).unwrap().contains("JOURNEY"), "the host status carries no returned records");
    assert_eq!(snapshot["recordsCapability"]["recentReads"].as_array().unwrap().len(), 2);
    host.stop("fixture", "journey done").ok();
}

/// The forked tool reaches the actual Host rule only from a known offered
/// source in the current generation. A changed native cwd still refuses data.
#[test]
fn records_access_fork_inherits_only_known_offer_and_keeps_project_scope() {
    use std::os::unix::fs::PermissionsExt;
    for mode in ["offered", "unoffered", "foreign-cwd"] {
        let f = Scratch::new();
        let project = f.project("project");
        let other = f.project("other-project");
        for name in ["account", "probe"] { std::fs::create_dir_all(f.0.join(name)).unwrap(); }
        write_run(&project, "run:journey", 3, "FORK_PROJECT_EVIDENCE", false);
        let script = f.0.join("peer.py");
        std::fs::write(&script, PEER).unwrap();
        std::fs::set_permissions(&script, std::fs::Permissions::from_mode(0o700)).unwrap();
        let mut cfg = crate::hosting::HostConfig::new(script, f.0.join("account"), f.0.join("probe"), project.clone());
        cfg.allow_unverified_dev = true;
        cfg.wait_limit = Duration::from_secs(2);
        let host = std::sync::Arc::new(crate::hosting::Host::new());
        host.configure_records_capability(std::sync::Arc::new(capability(&f, &project)));
        host.start(&cfg, "records fork fixture").unwrap();
        let generation = host.snapshot()["generation"].clone();
        let source = if mode == "unoffered" { &other } else { &project };
        host.thread_start_with_guidance(source.to_str().unwrap(), "fixture-model", "fixture-provider", "guidance").unwrap();
        let fork_cwd = if mode == "foreign-cwd" { &other } else { &project };
        std::fs::write(project.join("fork-cwd"), fork_cwd.to_str().unwrap()).unwrap();
        let request = host.thread_fork_dispatch(&generation, "thread").unwrap();
        host.source_request_wait(&request, Duration::from_secs(2)).unwrap();
        let fork = host.thread_fork_finish(&request).unwrap();
        assert_eq!(fork["threadId"], "fork");
        let wire = || -> Vec<Value> { std::fs::read_to_string(project.join("wire.jsonl")).unwrap_or_default().lines().map(|l| serde_json::from_str(l).unwrap()).collect() };
        let outbound = wire().into_iter().find(|w| w["method"] == "thread/fork").unwrap();
        assert_eq!(outbound["params"], json!({"threadId":"thread","deferGoalContinuation":true}));
        host.turn_start_text(&generation, "fork", "Read the records in this project.").unwrap();
        let deadline = Instant::now() + Duration::from_secs(10);
        let reply = |id: &str| wire().into_iter().find(|w| w["id"] == id && w.get("method").is_none());
        while reply("records-call-1").is_none() || reply("records-call-2").is_none() || reply("other-tool").is_none() {
            assert!(Instant::now() < deadline, "{mode}: no replies: {:?}", wire());
            std::thread::sleep(Duration::from_millis(20));
        }
        let first = reply("records-call-1").unwrap();
        if mode == "unoffered" {
            assert!(first["error"].is_object(), "a same-cwd fork cannot mint an unknown source's offer");
            assert!(f.logged().is_empty());
        } else {
            assert_eq!(first["result"]["success"], mode == "offered");
            let page: Value = serde_json::from_str(first["result"]["contentItems"][0]["text"].as_str().unwrap()).unwrap();
            assert_eq!(page["items"].as_array().unwrap().len(), if mode == "offered" { 3 } else { 0 });
            assert_eq!(f.logged().len(), 2, "offered calls are recorded, returned or refused");
            assert!(f.logged().iter().all(|r| r["threadId"] == "fork"));
            let snapshot = host.snapshot();
            let first = snapshot["serverRequests"].as_array().unwrap().iter().find(|r| r["requestIdentity"] == "records-call-1").unwrap();
            assert_eq!(first["originClass"], "named-service");
            assert_eq!(first["settlement"]["origin"], json!({"class":"app-rule","ruleName":"records-read"}));
        }
        assert!(reply("other-tool").unwrap()["error"].is_object());
        host.stop("fixture", "records fork done").ok();
    }
}

// #1313 re-review M2: only path-valued fields are rewritten, as typed markers,
// after resolving aliases; every other string is quoted exactly.
#[test]
fn only_path_fields_are_rewritten_as_typed_markers_and_free_text_is_exact() {
    let f = Scratch::new();
    let a = f.project("project");
    // (b) the project spelled as it was configured, through an alias: a
    // symbolic link to it. Another link to it, never configured, is not
    // followed: a path is resolved only under the project's two spellings.
    let alias = f.0.join("alias");
    std::os::unix::fs::symlink(&a, &alias).unwrap();
    let other = f.0.join("other-link");
    std::os::unix::fs::symlink(&a, &other).unwrap();
    let mut opened: Value = serde_json::from_str(include_str!("../../../execution/PKG-04/DEL-04-03/Work/RS_RECORD.valid.app-run.example.jsonl").lines().next().unwrap()).unwrap();
    opened["runId"] = json!("run:p");
    opened["body"]["runId"] = json!("run:p");
    opened["body"]["workflow"]["sourceRoot"] = json!(format!("{}/workflows/lib", alias.display()));
    let mut prose = opened.clone();
    prose["recordId"] = json!("rec:app:p-2");
    prose["seq"] = json!(2);
    prose["kind"] = json!("evidence_limit");
    // (a) a slash-led phrase, (c) a path inside prose, (d) a literal that looks like a marker.
    prose["body"] = json!({"label":"unresolvable reference","subjectRef":"<project>/x","detail":"/compact was run by the person; see /Users/someone/notes"});
    write_lines(&a, "run:p", &[opened.to_string(), prose.to_string()]);
    write_act(&a, "cap:in", &format!("{}/out/summary.md", alias.display()), "S");
    write_act(&a, "cap:out", "/etc/hosts", "S");
    write_act(&a, "cap:link", &format!("{}/out/summary.md", other.display()), "S");
    write_act(&a, "cap:dots", &format!("{}/../alias/out/summary.md", a.display()), "S");
    write_act(&a, "cap:net", "/net/records-fixture-host/share/x", "S");
    let cap = capability(&f, &alias);
    let page = returned(&cap.answer(&call(1, json!({"operation":"read_run","run":"run:p"})), Some(a.to_str().unwrap())));
    assert_eq!(page["items"][0]["quoted"]["body"]["workflow"]["sourceRoot"], json!({"rewrittenPath":"<project>/workflows/lib"}), "resolved through the alias");
    assert_eq!(page["items"][0]["pathsRewritten"], 1);
    let body = &page["items"][1]["quoted"]["body"];
    assert_eq!(body["detail"], "/compact was run by the person; see /Users/someone/notes", "free text is quoted exactly");
    assert_eq!(body["subjectRef"], "<project>/x", "a literal stays a string; a rewritten path is an object");
    assert_eq!(page["items"][1]["pathsRewritten"], 0);
    let runs = returned(&cap.answer(&call(2, json!({"operation":"list_runs"})), Some(a.to_str().unwrap())));
    assert_eq!(runs["items"][0]["run"]["opened"]["workflow"]["sourceRoot"], json!({"rewrittenPath":"<project>/workflows/lib"}));
    let acts = returned(&cap.answer(&call(3, json!({"operation":"read_acts"})), Some(a.to_str().unwrap())));
    let subjects: Vec<Value> = acts["items"].as_array().unwrap().iter().map(|i| i["quoted"]["body"]["boundSubject"].clone()).collect();
    let withheld = json!([{"withheldPath":"outside-project"}]);
    assert_eq!(subjects.iter().filter(|s| **s == json!([{"rewrittenPath":"<project>/out/summary.md"}])).count(), 1, "only the configured spelling: {subjects:?}");
    assert_eq!(subjects.iter().filter(|s| **s == withheld).count(), 4, "/etc/hosts, the unconfigured link, the `..` path and /net, unresolved: {subjects:?}");
    let text = serde_json::to_string(&acts).unwrap();
    for hidden in ["/etc/hosts", alias.to_str().unwrap(), other.to_str().unwrap(), "/net/"] {
        assert!(!text.contains(hidden), "{hidden}");
    }
}

/// A run log an earlier build wrote in the project (§13.7), read in place
/// until the person imports it.
fn write_legacy_run(project: &Path, run: &str, marker: &str) {
    use std::io::Write;
    let log = project.join(".chirality/records").join(crate::storage::log_rel(Some(run), "app-writer:local"));
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    let mut out = std::fs::OpenOptions::new().create(true).append(true).open(&log).unwrap();
    let entry = crate::records::envelope("evidence_limit", &crate::records::APP_WRITER, json!({"label":"unresolvable reference","subjectRef":marker,"detail":"legacy"}),
        format!("rec:app:{marker}-1"), 1, Some(run), Some("2026-10-12T00:00:00.000Z"));
    writeln!(out, "{entry}").unwrap();
}
fn lines(path: &Path) -> Vec<Value> {
    std::fs::read_to_string(path).unwrap_or_default().lines().map(|l| serde_json::from_str(l).unwrap()).collect()
}

/// §13.9 / U-STORE-6: each read is recorded in the project's records store
/// folder, before the project's records are imported (they are read in place)
/// and after (they are read from the store). The App-wide read log of an
/// earlier build stays in App data unchanged and is only shown.
#[test]
fn reads_are_recorded_in_the_projects_store_folder_before_and_after_import() {
    let f = Scratch::new();
    let p = f.project("legacy-project");
    write_legacy_run(&p, "run:old", "MARK-LEGACY");
    std::fs::write(f.read_log(), "{\"earlier\":\"App-wide read\"}\n").unwrap();
    let app_wide = std::fs::read(f.read_log()).unwrap();
    let cap = RecordsCapability::new(&p).unwrap().with_legacy_read_log(&f.read_log());
    // An agent's read never mints the project's identity: refused visibly.
    let unminted = cap.answer(&call(9, json!({"operation":"list_runs"})), Some(p.to_str().unwrap()));
    assert_eq!(unminted["success"], false);
    assert!(returned(&unminted)["refused"].as_str().unwrap().contains("no records store identity yet"), "{unminted}");
    assert!(!p.join(crate::records_store::PROJECT_LINK).exists(), "nothing minted");
    // The App mints it when it opens the project.
    crate::records_store::attach(&p, true).unwrap();
    let before = cap.answer(&call(1, json!({"operation":"read_run","run":"run:old"})), Some(p.to_str().unwrap()));
    assert_eq!(before["success"], true, "{before}");
    assert!(before["contentItems"][0]["text"].as_str().unwrap().contains("MARK-LEGACY"), "the legacy records are read in place");
    let log = crate::records_store::read_log_path(&p).unwrap();
    assert!(log.starts_with(crate::records_store::store_root().unwrap()), "{}", log.display());
    assert_eq!(lines(&log).len(), 1);
    assert_eq!(lines(&log)[0]["outcome"], "returned");
    let status = crate::records_store::status(Some(&p));
    assert_eq!(status["project"]["importNeeded"], true, "a read does not make the store hold the records: {status}");
    // After the import the records are read from the store; reads go on in
    // the same log.
    assert_eq!(crate::records_store::import(&p).unwrap()["state"], "imported");
    let after = cap.answer(&call(2, json!({"operation":"read_run","run":"run:old"})), Some(p.to_str().unwrap()));
    assert!(after["contentItems"][0]["text"].as_str().unwrap().contains("MARK-LEGACY"));
    assert!(after["contentItems"][0]["text"].as_str().unwrap().contains("records-store:"), "read from the store copy");
    assert_eq!(lines(&log).len(), 2);
    let snapshot = cap.snapshot();
    assert_eq!(snapshot["readLog"], log.to_string_lossy().as_ref());
    assert!(snapshot["readLogPlace"].as_str().unwrap().contains("records store"));
    assert_eq!(snapshot["legacyReadLog"]["bytes"], app_wide.len());
    assert!(snapshot["legacyReadLog"]["standing"].as_str().unwrap().contains("not imported"));
    assert_eq!(std::fs::read(f.read_log()).unwrap(), app_wide, "the App-wide log is never written or rewritten");
}
/// A project the store cannot attach (its link is missing): the read is
/// refused, visibly, and recorded nowhere else.
#[test]
fn a_read_that_cannot_be_recorded_in_the_store_is_refused_and_written_nowhere() {
    let f = Scratch::new();
    let p = f.project("unlinked");
    write_run(&p, "run:a", 2, "MARK-A", false);
    std::fs::remove_file(p.join(crate::records_store::PROJECT_LINK)).unwrap();
    let cap = RecordsCapability::new(&p).unwrap();
    let answer = cap.answer(&call(1, json!({"operation":"list_runs"})), Some(p.to_str().unwrap()));
    assert_eq!(answer["success"], false);
    let refused = returned(&answer)["refused"].as_str().unwrap().to_owned();
    assert!(refused.contains("could not be recorded") && refused.contains("link missing"), "{refused}");
    assert!(!refused.contains("MARK-A"));
    assert!(!f.read_log().exists(), "nothing in App data");
    assert!(cap.snapshot()["readLogLimit"].as_str().unwrap().contains("link missing"));
}
/// The records store unavailable: the read is refused, never recorded in App data.
#[test]
fn without_a_records_store_reads_are_refused() {
    let f = Scratch::new();
    let p = f.project("no-store");
    let cap = RecordsCapability::new(&p).unwrap();
    crate::records_store::use_store_for_test(Some(Err("no records store configured".into())));
    let answer = cap.answer(&call(1, json!({"operation":"list_runs"})), Some(p.to_str().unwrap()));
    crate::records_store::use_store_for_test(None);
    assert_eq!(answer["success"], false);
    assert!(returned(&answer)["refused"].as_str().unwrap().contains("records store unavailable"));
    assert!(!f.read_log().exists());
}

#[test]
fn records_access_source_refuses_named_pipe_without_waiting_for_its_writer() {
    use crate::records_store::{self, Placement, Store};
    use std::os::unix::{ffi::OsStrExt, fs::OpenOptionsExt};
    struct StoreOverride;
    impl Drop for StoreOverride {
        fn drop(&mut self) {
            records_store::use_store_for_test(None);
        }
    }
    for store_owned in [true, false] {
        let f = Scratch::new();
        let project = f.project(if store_owned {
            "store-project"
        } else {
            "legacy-project"
        });
        let store = f.project("records-store");
        let configured = Store {
            root: store,
            placement: Placement::Test,
            limits: vec![],
        };
        records_store::use_store_for_test(Some(Ok(configured.clone())));
        let _override = StoreOverride;
        let regular_id = if store_owned {
            crate::records::append_project(&project, Some("run:pipe-fixture"), "app-writer:fixture", "evidence_limit", &crate::records::APP_WRITER,
                json!({"label":"unresolvable reference","subjectRef":"invented regular record beside a pipe"})).unwrap()["recordId"].as_str().unwrap().to_owned()
        } else {
            let entry = crate::records::envelope(
                "evidence_limit",
                &crate::records::APP_WRITER,
                json!({"label":"unresolvable reference","subjectRef":"invented regular legacy record beside a pipe"}),
                "rec:app:regular-pipe-fixture".into(),
                1,
                Some("run:pipe-fixture"),
                None,
            );
            let path = project.join(".chirality/records/runs/fixture/regular.jsonl");
            std::fs::create_dir_all(path.parent().unwrap()).unwrap();
            std::fs::write(path, format!("{entry}\n")).unwrap();
            records_store::attach(&project, true).unwrap();
            assert!(!records_store::home(&project).unwrap().store_mode);
            entry["recordId"].as_str().unwrap().to_owned()
        };
        let group_entries = if store_owned {
            let log = crate::storage::project_log(
                &project,
                Some("run:pipe-fixture"),
                "app-writer:fixture",
            )
            .unwrap();
            let specs = (0..2).map(|n| crate::records::Spec {
                kind: "evidence_limit", recorder: &crate::records::APP_WRITER,
                body: json!({"label":"unresolvable reference","subjectRef":format!("invented regular group member {n}")}),
                id: format!("rec:app:pipe-group-{n}"), observed_at: None,
            }).collect();
            crate::records::append_group(
                &log,
                specs,
                Some("run:pipe-fixture"),
                crate::records::RecordSet::Complete,
            )
            .unwrap()
        } else {
            vec![]
        };
        let pipe = if store_owned {
            records_store::attach(&project, false)
                .unwrap()
                .dir
                .unwrap()
                .join("acts/000-pipe-fixture.jsonl")
        } else {
            project.join(".chirality/records/runs/fixture/000-pipe-fixture.jsonl")
        };
        std::fs::create_dir_all(pipe.parent().unwrap()).unwrap();
        let name = std::ffi::CString::new(pipe.as_os_str().as_bytes()).unwrap();
        assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
        assert!(
            crate::storage::discover(&project).unwrap().contains(&pipe),
            "discovery semantics remain unchanged"
        );
        let expected_limit = format!(
            "{}: not readable (no entry of it is returned)",
            crate::storage::log_label(&project, &pipe)
        );
        // The only writer stays open until the completion check. Closing it
        // releases an old blocking reader before any assertion can fail.
        let mut writer = std::fs::OpenOptions::new()
            .read(true)
            .write(true)
            .custom_flags(libc::O_NONBLOCK)
            .open(&pipe)
            .unwrap();
        let entry = crate::records::envelope(
            "evidence_limit",
            &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented pipe bytes must not be read"}),
            "rec:app:pipe-fixture".into(),
            1,
            Some("run:pipe-fixture"),
            None,
        );
        writer.write_all(format!("{entry}\n").as_bytes()).unwrap();
        let (done, completion) = std::sync::mpsc::channel();
        let reader = std::thread::spawn(move || {
            records_store::use_store_for_test(Some(Ok(configured)));
            let corpus = ProjectPaths::new(&project).read();
            records_store::use_store_for_test(None);
            done.send(corpus).unwrap();
        });
        let early = completion.recv_timeout(Duration::from_secs(2));
        let completed_before_writer_closed = early.is_ok();
        drop(writer);
        let corpus = early.unwrap_or_else(|_| {
            completion
                .recv_timeout(Duration::from_secs(2))
                .expect("closed controlled writer releases owned reader")
        });
        reader.join().unwrap();
        assert!(
            completed_before_writer_closed,
            "reader waited for a named pipe's writer"
        );
        assert!(
            corpus.limits.contains(&expected_limit),
            "{:?}",
            corpus.limits
        );
        assert!(corpus
            .entries
            .iter()
            .all(|e| e.entry["recordId"] != "rec:app:pipe-fixture"));
        for entry in group_entries {
            assert!(
                corpus.entries.iter().any(|e| e.entry == entry),
                "regular group members retain their exact parsed entries beside the pipe"
            );
        }
        assert!(
            corpus
                .entries
                .iter()
                .any(|e| e.entry["recordId"] == regular_id),
            "regular records remain readable beside the refused pipe"
        );
    }
}

#[test]
fn records_access_parent_substitution_refuses_links_or_reads_the_already_held_original() {
    use crate::records_store::{self, Placement, Store};
    struct StoreOverride;
    impl Drop for StoreOverride {
        fn drop(&mut self) { records_store::use_store_for_test(None); }
    }
    for (store_owned, parent_already_open) in [(true, false), (false, false), (true, true), (false, true)] {
        let f = Scratch::new();
        let project = f.project("intended-project");
        let other = f.project("second-invented-project");
        records_store::use_store_for_test(Some(Ok(Store {
            root: f.project("records-store"), placement: Placement::Test, limits: vec![],
        })));
        let _store = StoreOverride;
        let mut fixtures = Vec::new();
        for (root, marker) in [(&project, "INTENDED-SOURCE"), (&other, "SECOND-FIXTURE-MARKER")] {
            let body = json!({"label":"unresolvable reference","subjectRef":marker});
            let (log, entry) = if store_owned {
                let entry = crate::records::append_project(root, Some("run:source-association"), "app-writer:source-fixture", "evidence_limit", &crate::records::APP_WRITER, body).unwrap();
                (crate::storage::project_log(root, Some("run:source-association"), "app-writer:source-fixture").unwrap(), entry)
            } else {
                let entry = crate::records::envelope("evidence_limit", &crate::records::APP_WRITER, body, format!("rec:app:{marker}"), 1, Some("run:source-association"), None);
                let log = root.join(".chirality/records/runs/fixture/writer.jsonl");
                std::fs::create_dir_all(log.parent().unwrap()).unwrap();
                std::fs::write(&log, format!("{entry}\n")).unwrap();
                records_store::attach(root, true).unwrap();
                assert!(!records_store::home(root).unwrap().store_mode);
                (log, entry)
            };
            fixtures.push((log, entry["recordId"].as_str().unwrap().to_owned()));
        }
        let cap = capability(&f, &project);
        let identity = cap.project_identity().unwrap();
        let baseline = returned(&cap.answer(&call(0, json!({"operation":"read_run","run":"run:source-association"})), project.to_str()));
        assert_eq!(baseline["items"].as_array().unwrap().len(), 1);
        assert_eq!(baseline["items"][0]["quoted"]["recordId"], fixtures[0].1);
        let (log, _) = &fixtures[0];
        let expected_limit = format!("{}: not readable (no entry of it is returned)", crate::storage::log_label(&project, log));
        let parent = log.parent().unwrap().to_owned();
        let other_parent = fixtures[1].0.parent().unwrap().to_owned();
        let held = f.0.join("original-invented-run-parent");
        let moved = held.clone();
        let after_directory = parent_already_open.then(|| parent.clone());
        let _hook = crate::records_index::log_open_hook_for_test(log, after_directory.as_deref(), 0, move || {
            std::fs::rename(&parent, &moved).unwrap();
            std::os::unix::fs::symlink(&other_parent, &parent).unwrap();
        });
        let response = cap.answer(&call(1, json!({"operation":"read_run","run":"run:source-association"})), project.to_str());
        assert!(held.is_dir(), "the deterministic after-check substitution ran");
        assert_eq!(identity, cap.project_identity().unwrap(), "the physical project itself did not change");
        assert_eq!(response["success"], true, "the existing incomplete page remains a returned, recorded page");
        let page = returned(&response);
        let limits = if parent_already_open {
            assert_eq!(page["items"], baseline["items"], "the held original retains its exact parsed entries and source");
            assert_eq!(page["limits"], baseline["limits"], "the original regular/legacy limits stay unchanged");
            assert!(response.to_string().contains("INTENDED-SOURCE"));
            baseline["limits"].as_array().unwrap().len()
        } else {
            assert_eq!(page["items"], json!([]));
            assert_eq!(page["limits"], json!([expected_limit, "no readable entries for run run:source-association"]));
            2 // The existing read_run limit also names the unreadable run.
        };
        assert_eq!(page["limits"].as_array().unwrap().len(), limits);
        assert!(!response.to_string().contains("SECOND-FIXTURE-MARKER"));
        assert!(!response.to_string().contains(&fixtures[1].1));
        let logged = f.logged();
        assert_eq!(logged.len(), 2);
        assert_eq!(logged[1]["outcome"], "returned");
        assert_eq!(logged[1]["returned"]["items"], usize::from(parent_already_open));
        assert_eq!(logged[1]["returned"]["limits"], limits);
        assert_eq!(logged[1]["returned"]["recordIds"], if parent_already_open { json!([fixtures[0].1]) } else { json!([]) });
    }
}

#[test]
fn records_continuity_physical_project_changed_during_source_read_is_a_logged_refusal() {
    struct ReplacingSource { project: PathBuf, old: PathBuf }
    impl RecordsSource for ReplacingSource {
        fn read(&self) -> Corpus {
            std::fs::rename(&self.project,&self.old).unwrap();std::fs::create_dir(&self.project).unwrap();
            let record=crate::records::envelope("evidence_limit",&crate::records::APP_WRITER,json!({"label":"unresolvable reference","subjectRef":"NEW-PROJECT-SECRET","detail":"invented foreign records"}),"rec:foreign-project".into(),1,Some("run:foreign"),None);
            Corpus { entries:vec![SourcedEntry {entry:record,log:"invented foreign source".into(),line:1}],limits:vec![] }
        }
    }
    let f=Scratch::new();let project=f.project("project");let cap=RecordsCapability::with_source(&project,Box::new(ReplacingSource{project:project.clone(),old:f.0.join("original-project")}),f.read_log()).unwrap();
    let response=cap.answer(&call(1,json!({"operation":"list_runs"})),project.to_str());
    assert_eq!(response["success"],false);assert!(!response.to_string().contains("NEW-PROJECT-SECRET"));assert!(!response.to_string().contains("run:foreign"));
    let log=f.logged();assert_eq!(log.len(),1);assert_eq!(log[0]["outcome"],"refused");assert!(log[0]["refusal"].as_str().unwrap().contains("physical project changed"));
}
