//! DEL-02-03 REQ-008: a point placed through constructed supplier frames, its
//! record in the records store, its pointer in the App ledger, its receipt and
//! the conversation's reading. No Codex, no App: an admitted thread, the
//! App's own ledger and a test records store.
use super::super::Host;
use crate::points;
use crate::recovery::{AppProjectSource, ExplicitAppProjectContext};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::sync::Arc;

const HOME: &str = "app-home:point-fixture";

struct Fixture {
    root: PathBuf,
    project: PathBuf,
    ledger: PathBuf,
    host: Arc<Host>,
    g: Value,
    _custody: Option<crate::AppDataCustody>,
}
impl Drop for Fixture {
    fn drop(&mut self) {
        crate::records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn context(project: &Path) -> ExplicitAppProjectContext {
    ExplicitAppProjectContext::known(project.to_str().unwrap(), AppProjectSource::ConfiguredDirectory).unwrap()
}
/// A Host whose generation is ready, holding the conversation, the records
/// capability in `project`, and (when `offered`) the point tool's offer.
fn admitted(host: &Arc<Host>, project: &Path, reads: &Path, threads: &[&str], offered: bool) -> Value {
    host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(project, reads.to_path_buf()).unwrap()), context(project));
    let mut i = host.inner.0.lock().unwrap();
    let g = json!({"appSession":i.app_session,"home":HOME,"spawnCounter":1});
    i.generation = g.clone();
    i.state = "ready".into();
    for thread in threads {
        i.threads.push(json!({"generation":g,"threadId":thread,"cwd":project}));
        if offered {
            Host::note_point_offer(&mut i, &g, &json!(thread), &json!({"dynamicTools":[crate::records_access::definition(), points::definition()]}));
        }
    }
    g
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("point-record-").unwrap());
        for dir in ["project", "other-project", "app", "store"] { std::fs::create_dir_all(root.join(dir)).unwrap(); }
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: root.join("store"), placement: crate::records_store::Placement::Override, limits: vec![] })));
        let custody = crate::hold_app_data_for_test(&root.join("app")).unwrap();
        let project = root.join("project");
        let ledger = root.join("app/recovery.ledger.jsonl");
        let host = Arc::new(Host::new());
        host.configure_recovery(ledger.clone()).unwrap();
        let g = admitted(&host, &project, &root.join("app/reads.jsonl"), &["thread", "other", "unindexed"], true);
        for thread in ["thread", "other"] { host.observe_conversation_project(&g, thread, Some("H-acct"), &context(&project)).unwrap(); }
        Self { root, project, ledger, host, g, _custody: Some(custody) }
    }
    fn frame(&self, id: &str, thread: &str, call: &str, arguments: &Value) -> Vec<u8> {
        serde_json::to_vec(&json!({"id":id,"method":"item/tool/call","params":{"threadId":thread,"turnId":"turn-1","callId":call,"tool":points::TOOL,"namespace":null,"arguments":arguments}})).unwrap()
    }
    /// One call through the frame receiver; the receipt the host prepared.
    fn place(&self, id: &str, thread: &str, call: &str, arguments: &Value) -> Value {
        let before = self.receipts().len();
        self.host.on_line(&self.frame(id, thread, call, arguments), &self.g);
        let receipts = self.receipts();
        assert_eq!(receipts.len(), before + 1, "one receipt per admitted call");
        serde_json::from_str(receipts.last().unwrap()["contentItems"][0]["text"].as_str().unwrap()).unwrap()
    }
    fn receipts(&self) -> Vec<Value> {
        self.host.inner.0.lock().unwrap().points.receipts.clone()
    }
    fn log(&self) -> PathBuf {
        crate::storage::project_log(&self.project, None, points::WRITER).unwrap()
    }
    fn records(&self) -> Vec<Value> {
        crate::records::read_log(&self.log()).0.into_iter().filter(|e| e["kind"] == points::KIND).collect()
    }
    fn view(host: &Host, thread: &str) -> Value {
        host.snapshot()["points"].as_array().unwrap().iter().find(|v| v["threadId"] == thread).cloned().unwrap()
    }
    /// A relaunch: this Host ends as a killed process does; a new Host opens
    /// the same ledger and store, resumes the conversation, and its offer and
    /// owed pointers are restored as on an explicit Continue.
    fn relaunch(&mut self) {
        self.host.end_process_for_test();
        self._custody = None;
        self._custody = Some(crate::hold_app_data_for_test(&self.root.join("app")).unwrap());
        let host = Arc::new(Host::new());
        host.configure_recovery(self.ledger.clone()).unwrap();
        self.g = admitted(&host, &self.project, &self.root.join("app/reads.jsonl"), &["thread", "other"], false);
        for thread in ["thread", "other"] { host.restore_point_offer(&self.g, thread); }
        self.host = host;
    }
    fn displace_ledger(&self) -> PathBuf {
        let path = crate::recovery::database_path(&self.ledger);
        let aside = self.root.join("app/displaced-ledger");
        std::fs::rename(&path, &aside).unwrap();
        std::fs::create_dir(&path).unwrap();
        aside
    }
    fn restore_ledger(&self, aside: &Path) {
        let path = crate::recovery::database_path(&self.ledger);
        std::fs::remove_dir(&path).unwrap();
        std::fs::rename(aside, &path).unwrap();
    }
}
/// Every file under `dir`, with its length.
fn files(dir: &Path) -> Vec<(PathBuf, u64)> {
    let mut out = Vec::new();
    let mut stack = vec![dir.to_path_buf()];
    while let Some(d) = stack.pop() {
        for e in std::fs::read_dir(&d).into_iter().flatten().flatten() {
            let m = e.metadata().unwrap();
            if m.is_dir() { stack.push(e.path()); } else { out.push((e.path(), m.len())); }
        }
    }
    out.sort();
    out
}
fn full_terms() -> Value {
    json!({"version":1,"operation":"place","label":"Before the drawing is issued","kind":"review",
        "whenItArises":"after the drawing set is complete","pause":"asks the agent to pause","pauseSetBy":"the person",
        "whoMustRespond":"the checking engineer","responseRequested":"read the set and say whether it can go",
        "resolvedWhen":"the engineer replies","concerns":{"content":"drawings/A-101.pdf","revision":"r3"},
        "whoIntegrates":"the drafting lead","placedOnRequestOf":"the person","agentStatement":"The person asked for a review point here."})
}
fn hostile() -> Value {
    json!({"version":1,"operation":"place","label":"\u{202E}evil\u{202C} MARKER-HOSTILE",
        "whoMustRespond":"Waiting on you\n# Approve now\u{200B}<button>Approve</button>","agentStatement":"\t\r\u{0007}\u{FEFF}"})
}

#[test]
fn a_placement_writes_the_record_then_the_pointer_then_answers_recorded() {
    let f = Fixture::new();
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    assert_eq!(receipt["state"], "recorded", "{receipt}");
    assert_eq!(receipt["persistence"], points::KEPT);
    assert_eq!(receipt["run"], json!({"state":"no run","reason":"no run open in this conversation in this App session"}));
    let point = receipt["point"].as_str().unwrap();
    // The record: one point_placed entry with the arguments as sent and their digest.
    let records = f.records();
    assert_eq!(records.len(), 1);
    let body = &records[0]["body"];
    assert_eq!(body["point"], point);
    assert_eq!(body["arguments"], full_terms());
    assert_eq!(body["argumentsDigest"]["value"], crate::util::sha256_hex({ let mut s = String::new(); crate::canonical::canonical(&full_terms(), &mut s).unwrap(); s }.as_bytes()));
    assert_eq!(body["source"]["thread"], "thread");
    assert_eq!(body["source"]["call"], "call-1");
    assert_eq!(body["source"]["request"], "1");
    assert_eq!(body["source"]["generation"], crate::recovery::generation_ref(&f.g).unwrap());
    assert_eq!(body["project"], f.project.to_str().unwrap());
    // The pointer: one placed tag naming that record, holding no supplied text.
    let tags = f.host.tags_of("H-acct", "thread", points::TAG_OWNER);
    let placed: Vec<Value> = tags.iter().filter_map(|t| points::decode(t["value"].as_str().unwrap())).filter(|v| v["kind"] == "placed").collect();
    assert_eq!(placed.len(), 1);
    assert_eq!(placed[0]["record"], records[0]["recordId"]);
    assert!(tags.iter().any(|t| points::decode(t["value"].as_str().unwrap()).is_some_and(|v| v["kind"] == "offered")), "the offer pointer was written at indexing");
    // The view reads the same record: terms as sent, marked read, reading whole.
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["offer"]["state"], "offered at start in this App session");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"][0]["point"], point);
    assert_eq!(view["points"][0]["terms"], json!({"state":"read","arguments":full_terms()}));
    assert_eq!(view["points"][0]["placer"]["observed"]["turnStartLimit"], "the App did not observe starting this turn");
    // The register holds a named-service answer with the receipt by reference only.
    let entry = f.host.inner.0.lock().unwrap().server_requests.records().into_iter().find(|r| r["requestIdentity"] == "1").unwrap();
    assert_eq!(entry["originClass"], "named-service");
    assert_eq!(entry["settlement"]["origin"]["ruleName"], "point-record");
    assert!(entry["settlement"].get("nativeContent").is_none());
}

#[test]
fn nothing_of_the_terms_reaches_the_ledger() {
    let f = Fixture::new();
    assert_eq!(f.place("1", "thread", "call-1", &hostile())["state"], "recorded");
    assert_eq!(f.place("2", "thread", "call-2", &full_terms())["state"], "recorded");
    let bytes = String::from_utf8_lossy(&crate::recovery::stored_bytes(&f.ledger)).into_owned();
    for term in ["MARKER-HOSTILE", "the checking engineer", "drawings/A-101.pdf", "the drafting lead"] {
        assert!(!bytes.contains(term), "{term} in the ledger's bytes");
    }
    assert!(!serde_json::to_string(&crate::recovery::stored_entries(&f.ledger)).unwrap().contains("MARKER-HOSTILE"));
}

#[test]
fn refused_calls_write_nothing_and_say_why() {
    let f = Fixture::new();
    for (id, arguments, expected) in [
        ("1", json!({"version":1,"operation":"place","assignee":"x"}), "not valid for chirality_point_v1 version 1"),
        ("2", json!({"version":1,"operation":"revise"}), "not valid for chirality_point_v1 version 1"),
        ("3", json!({"version":1,"operation":"place","agentStatement":"\u{10348}".repeat(1000),"whenItArises":"y".repeat(2000),"responseRequested":"z".repeat(2000),"resolvedWhen":"w".repeat(2000),"whoMustRespond":"\u{10348}".repeat(500),"whoIntegrates":"\u{10348}".repeat(500),"label":"\u{10348}".repeat(200),"concerns":{"content":"\u{10348}".repeat(1000),"revision":"r".repeat(200)}}), "the App's own limit of 16384 bytes"),
    ] {
        let receipt = f.place(id, "thread", &format!("call-{id}"), &arguments);
        assert_eq!(receipt["state"], "not recorded", "{receipt}");
        assert!(receipt["point"].is_null());
        assert!(receipt["reason"].as_str().unwrap().contains(expected), "{receipt}");
    }
    // A conversation with no project index: refused, nothing written anywhere.
    let receipt = f.place("4", "unindexed", "call-4", &full_terms());
    assert_eq!(receipt["reason"], "No App project is known for this conversation, so the point could not be kept; no point was placed.");
    assert!(f.records().is_empty());
    assert!(f.host.tags_of("H-acct", "thread", points::TAG_OWNER).iter().all(|t| points::decode(t["value"].as_str().unwrap()).unwrap()["kind"] == "offered"));
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"], json!([]));
    assert_eq!(view["refused"].as_array().unwrap().len(), 3);
    assert_eq!(view["reading"]["whole"], true);
    // The records store refused: refused, nothing written elsewhere.
    let before = (files(&f.root.join("project")), files(&f.root.join("store")));
    crate::records_store::use_store_for_test(Some(Err("invented store refusal".into())));
    let receipt = f.place("5", "thread", "call-5", &full_terms());
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: f.root.join("store"), placement: crate::records_store::Placement::Override, limits: vec![] })));
    assert_eq!((files(&f.root.join("project")), files(&f.root.join("store"))), before, "nothing written in the project or the store");
    assert_eq!(receipt["state"], "not recorded");
    assert!(receipt["reason"].as_str().unwrap().starts_with("The App's records store did not take the point (") && receipt["reason"].as_str().unwrap().contains("invented store refusal"), "{receipt}");
    assert!(f.records().is_empty());
}

#[test]
fn calls_the_app_did_not_offer_are_refused_by_the_register_and_write_nothing() {
    let f = Fixture::new();
    {
        let mut i = f.host.inner.0.lock().unwrap();
        let g = f.g.clone();
        i.threads.push(json!({"generation":g,"threadId":"fork","cwd":f.project}));
    }
    // A conversation not offered the tool in this generation (a fork, a child, an unrestored resume).
    f.host.on_line(&f.frame("1", "fork", "call-1", &full_terms()), &f.g);
    let entry = f.host.inner.0.lock().unwrap().server_requests.records().into_iter().find(|r| r["requestIdentity"] == "1").unwrap();
    assert_eq!(entry["classification"], "known-app-unsupported");
    let entries = f.host.inner.0.lock().unwrap().server_requests.entries();
    assert!(entries.iter().any(|e| e["requestId"] == "1" && e["settlement"]["error"]["message"] == "This App session did not offer chirality_point_v1 to this conversation; no point was recorded"), "{entries:?}");
    // Another (stale) generation: not admitted at all.
    let stale = json!({"appSession":"stale","home":HOME,"spawnCounter":9});
    f.host.on_line(&f.frame("2", "thread", "call-2", &full_terms()), &stale);
    assert!(f.receipts().is_empty());
    assert!(f.records().is_empty());
    // A namespaced call of the same name is not the App's tool either.
    f.host.on_line(&serde_json::to_vec(&json!({"id":"3","method":"item/tool/call","params":{"threadId":"thread","turnId":"t","callId":"c","tool":points::TOOL,"namespace":"other","arguments":full_terms()}})).unwrap(), &f.g);
    assert!(f.receipts().is_empty());
    assert!(f.records().is_empty());
}

#[test]
fn one_placement_per_call_and_identical_arguments_in_another_call_are_a_second_point() {
    let f = Fixture::new();
    let first = f.place("1", "thread", "call-1", &full_terms());
    // The same request identity again: the register refuses it; no second record, no answer.
    f.host.on_line(&f.frame("1", "thread", "call-1", &full_terms()), &f.g);
    assert_eq!(f.receipts().len(), 1);
    assert_eq!(f.records().len(), 1);
    // The same call identity answered again (as a recovery would): the same reference, one record.
    let call = { let i = f.host.inner.0.lock().unwrap(); Host::point_call(&i, &f.g, &serde_json::from_slice(&f.frame("1", "thread", "call-1", &full_terms())).unwrap()) };
    f.host.answer_point_call(call);
    let again: Value = serde_json::from_str(f.receipts().last().unwrap()["contentItems"][0]["text"].as_str().unwrap()).unwrap();
    assert_eq!(again["point"], first["point"]);
    assert_eq!(f.records().len(), 1);
    // Another call with the same arguments: a second point.
    let second = f.place("2", "thread", "call-2", &full_terms());
    assert_ne!(second["point"], first["point"]);
    assert_eq!(f.records().len(), 2);
    assert_eq!(Fixture::view(&f.host, "thread")["points"].as_array().unwrap().len(), 2);
}

#[test]
fn the_run_reading_names_the_run_its_absence_or_why_it_is_not_established() {
    let f = Fixture::new();
    f.host.note_conversation_run(&f.g, "thread", "run:A", "open");
    assert_eq!(f.place("1", "thread", "c1", &full_terms())["run"], json!({"state":"in run","run":"run:A"}));
    f.host.note_conversation_run(&f.g, "thread", "run:A", "ended");
    assert_eq!(f.place("2", "thread", "c2", &full_terms())["run"]["state"], "no run");
    f.host.note_conversation_run(&f.g, "thread", "run:B", "start sent");
    assert_eq!(f.place("3", "thread", "c3", &full_terms())["run"]["state"], "not established");
    f.host.note_conversation_run(&f.g, "thread", "run:B", "not opened");
    assert_eq!(f.place("4", "thread", "c4", &full_terms())["run"]["state"], "no run");
    // A run of another conversation is never this one's.
    f.host.note_conversation_run(&f.g, "other", "run:C", "open");
    assert_eq!(f.place("5", "thread", "c5", &full_terms())["run"]["state"], "no run");
}

#[test]
fn terms_after_a_relaunch_equal_the_arguments_sent_byte_exact() {
    let mut f = Fixture::new();
    let a = f.place("1", "thread", "call-1", &full_terms())["point"].clone();
    let b = f.place("2", "thread", "call-2", &hostile())["point"].clone();
    f.relaunch();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["offer"]["state"], "offered when this conversation started, restored after the App restarted");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    let points = view["points"].as_array().unwrap();
    assert_eq!(points.len(), 2);
    assert_eq!(points[0]["point"], a);
    assert_eq!(points[0]["terms"]["arguments"], full_terms());
    assert_eq!(points[1]["point"], b);
    assert_eq!(points[1]["terms"]["arguments"], hostile());
    assert_eq!(points[1]["terms"]["arguments"]["whoMustRespond"].as_str().unwrap().as_bytes(), hostile()["whoMustRespond"].as_str().unwrap().as_bytes());
    // The resumed conversation is offered again; its run reading cannot name an earlier session's run.
    let receipt = f.place("9", "thread", "call-9", &full_terms());
    assert_eq!(receipt["state"], "recorded");
    assert_eq!(receipt["run"]["state"], "not established");
    // The other conversation shows none of these.
    assert_eq!(Fixture::view(&f.host, "other")["points"], json!([]));
}

#[test]
fn a_record_whose_pointer_was_not_saved_is_recovered_once_and_never_doubled() {
    let mut f = Fixture::new();
    let aside = f.displace_ledger();
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    // The record exists, so the receipt says recorded, with the pointer not saved.
    assert_eq!(receipt["state"], "recorded", "{receipt}");
    assert!(receipt["persistence"].as_str().unwrap().starts_with("The point and its terms are kept in the App's records for this conversation's project, but the conversation's pointer to them could not be saved ("), "{receipt}");
    assert_eq!(f.records().len(), 1);
    // Until the pointer is saved the point is not shown and the reading is not whole, never empty-and-whole.
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"], json!([]));
    assert_eq!(view["reading"]["whole"], false);
    assert!(view["reading"]["reasons"].as_array().unwrap().iter().any(|r| r.as_str().unwrap().contains("could not be saved")), "{view}");
    f.restore_ledger(&aside);
    f.relaunch();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"].as_array().unwrap().len(), 1);
    assert_eq!(view["points"][0]["point"], receipt["point"]);
    assert_eq!(view["points"][0]["terms"]["arguments"], full_terms());
    assert_eq!(f.records().len(), 1, "exactly one record");
    // A further reopening completes nothing twice.
    f.relaunch();
    let placed = f.host.tags_of("H-acct", "thread", points::TAG_OWNER).iter().filter(|t| points::decode(t["value"].as_str().unwrap()).unwrap()["kind"] == "placed").count();
    assert_eq!(placed, 1);
}

#[test]
fn an_orphan_record_is_never_shown_and_recovery_never_joins_another_conversation_or_project() {
    let mut f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    // A record of "other" with no pointer, and one of the same conversation in another project.
    let other = f.records()[0].clone();
    let mut body = other["body"].clone();
    body["point"] = json!(crate::util::opaque_id("pt-").unwrap());
    body["source"]["thread"] = json!("other");
    body["source"]["call"] = json!("call-orphan");
    crate::records::append_project(&f.project, None, points::WRITER, points::KIND, &crate::records::APP_WRITER, body.clone()).unwrap();
    let mut foreign = other["body"].clone();
    foreign["point"] = json!(crate::util::opaque_id("pt-").unwrap());
    foreign["source"]["call"] = json!("call-foreign");
    foreign["project"] = json!(f.root.join("other-project").to_str().unwrap());
    crate::records::append_project(&f.root.join("other-project"), None, points::WRITER, points::KIND, &crate::records::APP_WRITER, foreign).unwrap();
    // The orphan is not shown where it belongs until its pointer is completed.
    assert_eq!(Fixture::view(&f.host, "other")["points"], json!([]));
    assert_eq!(Fixture::view(&f.host, "thread")["points"].as_array().unwrap().len(), 1);
    f.relaunch();
    // "other"'s orphan is completed for "other" only; the foreign project's record joins nothing.
    assert_eq!(Fixture::view(&f.host, "thread")["points"].as_array().unwrap().len(), 1);
    let others = Fixture::view(&f.host, "other");
    assert_eq!(others["points"].as_array().unwrap().len(), 1, "{others}");
    assert_eq!(others["points"][0]["point"], body["point"]);
    // A pointer naming this conversation but another project reads as not belonging.
    let pointer = json!({"point":body["point"],"record":"rec:x","source":body["source"],"project":"/elsewhere","run":body["run"],"placer":body["placer"],"digest":body["argumentsDigest"]});
    let conversation = points::Conversation { home: HOME, home_class: "H-acct", thread: "other", project: f.project.to_str().unwrap() };
    let joined = points::join(&pointer, &points::LogReading::read(&f.log()), &conversation);
    assert_eq!(joined["terms"]["state"], "not read");
}

#[test]
fn an_altered_truncated_missing_or_doubled_record_shows_the_point_with_terms_not_read() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    f.place("2", "thread", "call-2", &full_terms());
    let reason = |n: usize| Fixture::view(&f.host, "thread")["points"][n]["terms"]["reason"].as_str().unwrap_or("read").to_owned();
    let original = std::fs::read_to_string(f.log()).unwrap();
    // Altered: the first record's terms changed on disk, its link untouched.
    std::fs::write(f.log(), original.replacen("the checking engineer", "the CHECKING engineer", 1)).unwrap();
    assert!(reason(0).contains("do not match the digest"), "{}", reason(0));
    // ... which breaks the chain at the next line: the second is not read either.
    assert!(reason(1).contains("not whole at or before"), "{}", reason(1));
    // Truncated: the second record cut short.
    let cut = original.trim_end_matches('\n');
    std::fs::write(f.log(), &cut[..cut.len() - 40]).unwrap();
    assert_eq!(reason(0), "read");
    assert!(reason(1).contains("no record with this point's reference"), "{}", reason(1));
    // Missing: the log removed.
    std::fs::remove_file(f.log()).unwrap();
    assert!(reason(0).contains("no record with this point's reference"));
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"].as_array().unwrap().len(), 2, "still recorded, terms not read");
    // Doubled: the same reference written twice.
    std::fs::write(f.log(), &original).unwrap();
    let first = crate::records::read_log(&f.log()).0[0].clone();
    crate::records::append_project(&f.project, None, points::WRITER, points::KIND, &crate::records::APP_WRITER, first["body"].clone()).unwrap();
    assert!(reason(0).contains("more than once"), "{}", reason(0));
}

#[test]
fn the_view_marks_a_conversation_never_offered_and_one_with_none_recorded() {
    let f = Fixture::new();
    { let mut i = f.host.inner.0.lock().unwrap(); let g = f.g.clone(); i.threads.push(json!({"generation":g,"threadId":"fork"})); }
    let fork = Fixture::view(&f.host, "fork");
    assert_eq!(fork["offer"]["state"], "not offered in this App session");
    assert_eq!(fork["points"], json!([]));
    let none = Fixture::view(&f.host, "thread");
    assert_eq!(none["offer"]["state"], "offered at start in this App session");
    assert_eq!(none["reading"]["whole"], true);
    assert_eq!(none["points"], json!([]));
}

/// The new kind is a record of the store like any other: the index rebuilt
/// from the logs finds it, and the store's verification counts its log.
#[test]
fn the_records_index_and_chain_heads_treat_a_point_record_as_any_record() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    let id = f.records()[0]["recordId"].as_str().unwrap().to_owned();
    let found = crate::records_index::with_index(&f.project, |ix| ix.entries_with(&id)).unwrap();
    assert_eq!(found.len(), 1);
    let heads = crate::records_index::chain_heads(&f.project);
    assert!(heads.to_string().contains(points::WRITER) || heads.to_string().contains(&crate::storage::log_rel(None, points::WRITER)), "{heads}");
}

/// DEL-04-03: export copies the points log byte for byte and both the App's
/// check and the package's own verifier accept it; a legal hold, closure and
/// disposal apply to it as to any record (after disposal the conversation
/// still shows its point, with terms not read, and a new placement is refused
/// with nothing written); and the export the disposal relied on carries it
/// into another store unchanged by package import.
#[test]
fn export_standalone_check_package_import_hold_and_disposal_treat_a_point_record_as_any_record() {
    let f = Fixture::new();
    assert_eq!(f.place("1", "thread", "call-1", &full_terms())["state"], "recorded");
    let log = f.log();
    let source = crate::records_store::attach(&f.project, false).unwrap();
    let (dir, project) = (source.dir.unwrap(), source.project.unwrap());
    let rel = log.strip_prefix(&dir).unwrap().to_path_buf();
    let bytes = std::fs::read(&log).unwrap();
    let bag = f.root.join("export/bag");
    std::fs::create_dir_all(bag.parent().unwrap()).unwrap();
    crate::records_export::export(&f.project, &bag).unwrap();
    assert_eq!(std::fs::read(bag.join("data").join(&rel)).unwrap(), bytes);
    assert!(crate::records_export::verify(&bag).is_ok());
    let standalone = std::process::Command::new("python3").arg(bag.join("verify.py")).arg(&bag).output().unwrap();
    assert!(standalone.status.success(), "{}", String::from_utf8_lossy(&standalone.stderr));

    let actor = crate::act_control::person(Some("Invented fixture person"), Some("invented-fixture-account"));
    let observed = json!({"fixture":"native context test double; no actual human act"});
    let store = |root: PathBuf, placement| crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root, placement, limits: vec![] })));
    let act = |action: &str, bag: Option<&Path>| crate::records_retention::prepare(&f.project, action, bag, &actor, &observed).and_then(|p| crate::records_retention::apply(p, &actor, &observed));
    act("set-hold", None).unwrap();
    act("close", None).unwrap();
    let closed = f.place("2", "thread", "call-2", &full_terms());
    assert_eq!(closed["state"], "not recorded");
    assert!(closed["reason"].as_str().unwrap().starts_with("The App's records store did not take the point"), "{closed}");
    let held = f.root.join("export/held");
    crate::records_export::export(&f.project, &held).unwrap();
    assert!(act("dispose", Some(&held)).unwrap_err().contains("legal hold"));
    act("release-hold", None).unwrap();
    let current = f.root.join("export/current");
    crate::records_export::export(&f.project, &current).unwrap();
    assert_eq!(std::fs::read(current.join("data").join(&rel)).unwrap(), bytes);
    assert_eq!(act("dispose", Some(&current)).unwrap()["state"], "disposed");
    assert!(!log.exists());
    let view = Fixture::view(&f.host, "thread");
    let points = view["points"].as_array().unwrap();
    assert_eq!(points.len(), 1, "{view}");
    assert_eq!(points[0]["terms"]["state"], "not read", "{view}");
    assert_eq!(f.place("3", "thread", "call-3", &full_terms())["state"], "not recorded");
    assert!(!log.exists());

    // The export the disposal relied on, imported as a package into another store.
    store(f.root.join("destination-store"), crate::records_store::Placement::Test);
    let plan = crate::records_store::package::prepare(&f.project, &current, &actor, &observed).unwrap();
    assert_eq!(crate::records_store::package::apply(plan, &actor, &observed).unwrap()["state"], "package imported");
    let imported = crate::records_store::project_dir(&f.root.join("destination-store"), &project).join(&rel);
    assert_eq!(std::fs::read(&imported).unwrap(), bytes);
    let reading = points::LogReading::read(&imported).unwrap();
    assert_eq!(reading.entries.len(), 1);
    assert_eq!(reading.entries[0].entry["body"]["arguments"], full_terms());
}
