//! DEL-02-03 REQ-008: a point placed through constructed supplier frames, its
//! record in the records store, its pointer in the App ledger, its receipt and
//! reply, and the conversation's reading. No Codex, no App: an admitted
//! thread, the App's own ledger, a test records store and a test reply pipe.
use super::super::Host;
use super::*;
use crate::recovery::{AppProjectSource, ExplicitAppProjectContext};
use serde_json::{json, Value};
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
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
fn use_store(root: &Path) {
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: root.join("store"), placement: crate::records_store::Placement::Override, limits: vec![] })));
}
/// A Host whose generation is ready, holding the conversations, the records
/// capability in `project`, and the point tool's offer for `offered`.
fn admitted(host: &Arc<Host>, project: &Path, reads: &Path, threads: &[&str], offered: &[&str]) -> Value {
    host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(project, reads.to_path_buf()).unwrap()), context(project));
    let mut i = host.inner.0.lock().unwrap();
    let g = json!({"appSession":i.app_session,"home":HOME,"spawnCounter":1});
    i.generation = g.clone();
    i.state = "ready".into();
    for thread in threads {
        i.threads.push(json!({"generation":g,"threadId":thread,"cwd":project}));
        if offered.contains(thread) {
            Host::note_point_offer(&mut i, &g, &json!(thread), &json!({"dynamicTools":[crate::records_access::definition(), points::definition()]}));
        }
    }
    g
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("point-record-").unwrap());
        for dir in ["project", "other-project", "app", "store"] { std::fs::create_dir_all(root.join(dir)).unwrap(); }
        use_store(&root);
        let custody = crate::hold_app_data_for_test(&root.join("app")).unwrap();
        let project = root.join("project");
        let ledger = root.join("app/recovery.ledger.jsonl");
        let host = Arc::new(Host::new());
        host.configure_recovery(ledger.clone()).unwrap();
        let g = admitted(&host, &project, &root.join("app/reads.jsonl"), &["thread", "other", "unindexed", "plain"], &["thread", "other", "unindexed"]);
        for thread in ["thread", "other", "plain"] { host.observe_conversation_project(&g, thread, Some("H-acct"), &context(&project)).unwrap(); }
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
        text(receipts.last().unwrap())
    }
    fn receipts(&self) -> Vec<Value> {
        self.host.inner.0.lock().unwrap().points.receipts.clone()
    }
    /// The project's points log, as the store attaches it (read only).
    fn log(&self) -> PathBuf {
        match crate::records_store::attach(&self.project, false).ok().and_then(|a| a.dir) {
            Some(dir) => dir.join(crate::storage::log_rel(None, points::WRITER)),
            None => self.root.join("no-records-yet"),
        }
    }
    fn records(&self) -> Vec<Value> {
        if !self.log().exists() { return vec![]; }
        crate::records::read_log(&self.log()).0.into_iter().filter(|e| e["kind"] == points::KIND).collect()
    }
    fn placed(&self, thread: &str) -> Vec<Value> {
        self.host.tags_of("H-acct", thread, points::TAG_OWNER).iter().filter_map(|t| points::decode(t["value"].as_str().unwrap())).filter(|v| v["kind"] == "placed").collect()
    }
    fn view(host: &Host, thread: &str) -> Value {
        host.snapshot()["points"].as_array().unwrap().iter().find(|v| v["threadId"] == thread).cloned().unwrap()
    }
    /// A relaunch: this Host ends as a killed process does; a new Host opens
    /// the same ledger and store, resumes the conversations, and runs what an
    /// explicit Continue runs for points.
    fn relaunch(&mut self) {
        self.host.end_process_for_test();
        self._custody = None;
        self._custody = Some(crate::hold_app_data_for_test(&self.root.join("app")).unwrap());
        let host = Arc::new(Host::new());
        host.configure_recovery(self.ledger.clone()).unwrap();
        self.g = admitted(&host, &self.project, &self.root.join("app/reads.jsonl"), &["thread", "other", "plain"], &[]);
        for thread in ["thread", "other", "plain"] { host.restore_point_offer(&self.g, thread); }
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
    fn reasons(view: &Value) -> String {
        view["reading"]["reasons"].to_string()
    }
}
fn text(receipt: &Value) -> Value {
    serde_json::from_str(receipt["contentItems"][0]["text"].as_str().unwrap()).unwrap()
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
/// A reply pipe on the host: the read end, non-blocking.
fn reply_pipe(host: &Host) -> std::fs::File {
    let mut fds = [-1; 2];
    assert_eq!(unsafe { libc::pipe(fds.as_mut_ptr()) }, 0);
    let read = unsafe { OwnedFd::from_raw_fd(fds[0]) };
    let write = unsafe { OwnedFd::from_raw_fd(fds[1]) };
    for fd in [read.as_raw_fd(), write.as_raw_fd()] {
        let flags = unsafe { libc::fcntl(fd, libc::F_GETFD) };
        assert_eq!(unsafe { libc::fcntl(fd, libc::F_SETFD, flags | libc::FD_CLOEXEC) }, 0);
    }
    let flags = unsafe { libc::fcntl(read.as_raw_fd(), libc::F_GETFL) };
    assert_eq!(unsafe { libc::fcntl(read.as_raw_fd(), libc::F_SETFL, flags | libc::O_NONBLOCK) }, 0);
    *host.stdin.lock().unwrap() = Some(std::process::ChildStdin::from(write));
    std::fs::File::from(read)
}
/// The frames written to the pipe so far.
fn written(reader: &mut std::fs::File) -> Vec<Value> {
    use std::io::Read;
    let mut bytes = Vec::new();
    let mut buf = [0u8; 65536];
    loop {
        match reader.read(&mut buf) {
            Ok(0) => break,
            Ok(n) => bytes.extend_from_slice(&buf[..n]),
            Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => break,
            Err(e) => panic!("{e}"),
        }
    }
    String::from_utf8(bytes).unwrap().lines().map(|l| serde_json::from_str(l).unwrap()).collect()
}

#[test]
fn a_placement_writes_the_record_then_the_pointer_then_answers_recorded() {
    let f = Fixture::new();
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    assert_eq!(receipt["state"], "recorded", "{receipt}");
    assert_eq!(receipt["persistence"], points::KEPT);
    assert_eq!(receipt["run"], json!({"state":"no run"}));
    let point = receipt["point"].as_str().unwrap();
    // The record: one point_placed entry with the terms as admitted, their
    // digest, the call's identities and the store's project identity.
    let records = f.records();
    assert_eq!(records.len(), 1);
    let body = &records[0]["body"];
    assert_eq!(body["point"], point);
    assert_eq!(body["arguments"], full_terms());
    assert_eq!(body["argumentsDigest"]["value"], crate::util::sha256_hex({ let mut s = String::new(); crate::canonical::canonical(&full_terms(), &mut s).unwrap(); s }.as_bytes()));
    assert_eq!(body["source"], json!({"home":HOME,"homeClass":"H-acct","generation":crate::recovery::generation_ref(&f.g).unwrap(),"thread":"thread","turn":"turn-1","call":"call-1","request":"1"}));
    assert_eq!(body["project"], f.project.to_str().unwrap());
    assert_eq!(body["storeProject"], json!(crate::records_store::attach(&f.project, false).unwrap().project.unwrap()));
    assert_eq!(body["observed"], json!({"caller":"agent-through-point-tool","turnStart":"not-observed","delegation":"not-established"}));
    // The pointer: one placed tag naming that record, holding identities and the digest only.
    let placed = f.placed("thread");
    assert_eq!(placed.len(), 1);
    assert_eq!(placed[0]["record"], records[0]["recordId"]);
    assert_eq!(placed[0]["storeProject"], body["storeProject"]);
    assert!(placed[0].get("run").is_none() && placed[0].get("observed").is_none() && placed[0].get("placer").is_none());
    assert!(f.host.tags_of("H-acct", "thread", points::TAG_OWNER).iter().any(|t| points::decode(t["value"].as_str().unwrap()).is_some_and(|v| v["kind"] == "offered")), "the offer pointer was written at indexing");
    // The view reads the same record: terms as sent, the run and observation from the record.
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["offer"]["state"], "offered at start in this App session");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"][0]["point"], point);
    assert_eq!(view["points"][0]["terms"], json!({"state":"read","arguments":full_terms()}));
    assert_eq!(view["points"][0]["run"], json!({"state":"no run"}));
    assert_eq!(view["points"][0]["observed"]["turnStart"], "not-observed");
    // The register holds a named-service answer with the receipt by reference only.
    let entry = f.host.inner.0.lock().unwrap().server_requests.records().into_iter().find(|r| r["requestIdentity"] == "1").unwrap();
    assert_eq!(entry["originClass"], "named-service");
    assert_eq!(entry["settlement"]["origin"]["ruleName"], "point-record");
    assert!(entry["settlement"].get("nativeContent").is_none());
}

/// Finding 1: the conversation panel reads `host_status`, whose snapshot is
/// the native projection the runtime receives; the points are on it.
#[test]
fn the_status_payload_the_panel_reads_carries_the_conversations_points() {
    let f = Fixture::new();
    let point = f.place("1", "thread", "call-1", &full_terms())["point"].clone();
    let home = crate::runtime_session::HomeSession::new(crate::home_resources::HomeClass::Account, Arc::clone(&f.host), Err("no configuration in this test".into())).unwrap();
    let (observation, _) = home.runtime.lock().unwrap().receive_native(&home.host);
    let rows = observation["snapshot"]["points"].as_array().unwrap_or_else(|| panic!("no points on the status snapshot: {observation}"));
    let row = rows.iter().find(|r| r["threadId"] == "thread").unwrap();
    assert_eq!(row["points"][0]["point"], point);
    assert_eq!(row["points"][0]["terms"]["arguments"], full_terms());
    assert_eq!(row["reading"]["whole"], true);
}

/// Finding 7: through the real receiver and a test reply pipe, the record and
/// the pointer exist before the reply is written; the reply is the receipt; a
/// repeated request identity is refused and not answered again, in the same
/// generation and after it closed, and writes nothing.
#[test]
fn through_the_receiver_the_record_and_pointer_precede_the_reply_and_a_repeat_is_not_answered_again() {
    let f = Fixture::new();
    let mut pipe = reply_pipe(&f.host);
    let (host, log) = (Arc::clone(&f.host), f.project.clone());
    let seen = Arc::new(std::sync::Mutex::new(None));
    let at_reply = Arc::clone(&seen);
    f.host.inner.0.lock().unwrap().points.before_reply = Some(Box::new(move || {
        let attached = crate::records_store::attach(&log, false).ok().and_then(|a| a.dir).map(|d| d.join(crate::storage::log_rel(None, points::WRITER)));
        let records = attached.filter(|p| p.exists()).map(|p| crate::records::read_log(&p).0.len()).unwrap_or(0);
        let pointers = host.tags_of("H-acct", "thread", points::TAG_OWNER).iter().filter(|t| t["value"].as_str().unwrap().contains("\"placed\"")).count();
        *at_reply.lock().unwrap() = Some((records, pointers));
    }));
    f.host.on_line(&f.frame("7", "thread", "call-1", &full_terms()), &f.g);
    assert_eq!(*seen.lock().unwrap(), Some((1, 1)), "record and pointer were there before the reply was written");
    let replies = written(&mut pipe);
    assert_eq!(replies.len(), 1);
    assert_eq!(replies[0]["id"], "7");
    assert_eq!(text(&replies[0]["result"])["state"], "recorded");
    // The same request identity again in this generation: refused by the register, not answered.
    f.host.on_line(&f.frame("7", "thread", "call-1", &full_terms()), &f.g);
    assert!(written(&mut pipe).is_empty(), "the first answer stands; no second reply");
    assert_eq!(f.records().len(), 1);
    assert!(f.host.snapshot()["journal"].as_array().unwrap().iter().any(|j| j["reason"] == "duplicate-request-identity"), "journaled");
    // After the generation closed: refused, nothing written, no reply.
    { let mut i = f.host.inner.0.lock().unwrap(); Host::close_generation(&mut i); }
    f.host.on_line(&f.frame("7", "thread", "call-1", &full_terms()), &f.g);
    f.host.on_line(&f.frame("8", "thread", "call-2", &full_terms()), &f.g);
    assert!(written(&mut pipe).is_empty());
    assert_eq!(f.records().len(), 1);
    assert_eq!(f.placed("thread").len(), 1);
}

#[test]
fn nothing_of_the_terms_and_no_prose_reaches_the_ledger() {
    let f = Fixture::new();
    f.host.note_conversation_run(&f.g, "thread", "run:workflow:a", "start sent");
    assert_eq!(f.place("1", "thread", "call-1", &hostile())["state"], "recorded");
    assert_eq!(f.place("2", "thread", "call-2", &full_terms())["state"], "recorded");
    let bytes = String::from_utf8_lossy(&crate::recovery::stored_bytes(&f.ledger)).into_owned();
    for term in ["MARKER-HOSTILE", "the checking engineer", "drawings/A-101.pdf", "the drafting lead", "start-sent-not-yet-open", "agent-through-point-tool", "not-established"] {
        assert!(!bytes.contains(term), "{term} in the ledger's bytes");
    }
}

/// Every refusal the App can decide without writing comes before any write:
/// no point record and no pointer for that call.
#[test]
fn refusals_decided_before_any_write_leave_no_record_and_no_pointer() {
    let f = Fixture::new();
    for (id, arguments, expected) in [
        ("1", json!({"version":1,"operation":"place","assignee":"x"}), "not valid for chirality_point_v1 version 1"),
        ("2", json!({"version":1,"operation":"revise"}), "not valid for chirality_point_v1 version 1"),
        ("3", json!({"version":1,"operation":"place","agentStatement":"\u{10348}".repeat(1000),"whenItArises":"y".repeat(2000),"responseRequested":"z".repeat(2000),"resolvedWhen":"w".repeat(2000),"whoMustRespond":"\u{10348}".repeat(500),"whoIntegrates":"\u{10348}".repeat(500),"label":"\u{10348}".repeat(200),"concerns":{"content":"\u{10348}".repeat(1000),"revision":"r".repeat(200)}}), "the App's own limit of 16384 bytes"),
        ("4", json!({"version":1,"operation":"place","kind":"sign-off"}), "A sign-off point names its act"),
    ] {
        let receipt = f.place(id, "thread", &format!("call-{id}"), &arguments);
        assert_eq!(receipt["state"], "not recorded", "{receipt}");
        assert!(receipt["point"].is_null());
        assert!(receipt["reason"].as_str().unwrap().contains(expected), "{receipt}");
    }
    // A conversation with no project index.
    let receipt = f.place("5", "unindexed", "call-5", &full_terms());
    assert_eq!(receipt["reason"], "No App project is known for this conversation, so the point could not be kept; no point was placed.");
    assert!(f.records().is_empty());
    assert!(f.placed("thread").is_empty());
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"], json!([]));
    assert_eq!(view["refused"].as_array().unwrap().len(), 4);
    assert_eq!(view["reading"]["whole"], true);
    // Another project open now.
    f.host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(&f.root.join("other-project"), f.root.join("app/reads.jsonl")).unwrap()), context(&f.root.join("other-project")));
    let receipt = f.place("6", "thread", "call-6", &full_terms());
    assert_eq!(receipt["reason"], "This conversation's App project is not the project the App has open now, so the point could not be kept; no point was placed.");
    f.host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(&f.project, f.root.join("app/reads.jsonl")).unwrap()), context(&f.project));
    // The records store refused: nothing written in the project or the store.
    let before = (files(&f.project), files(&f.root.join("store")));
    crate::records_store::use_store_for_test(Some(Err("invented store refusal".into())));
    let receipt = f.place("7", "thread", "call-7", &full_terms());
    use_store(&f.root);
    assert_eq!((files(&f.project), files(&f.root.join("store"))), before, "nothing written in the project or the store");
    assert!(receipt["reason"].as_str().unwrap().starts_with("The App's records store did not take the point (") && receipt["reason"].as_str().unwrap().contains("invented store refusal"), "{receipt}");
    assert!(f.records().is_empty());
    assert!(f.placed("thread").is_empty());
}

/// Calls naming the point tool that the host does not admit as point calls
/// get the register's true sentence and write nothing.
#[test]
fn calls_not_admitted_as_point_calls_are_refused_with_a_true_sentence() {
    let f = Fixture::new();
    { let mut i = f.host.inner.0.lock().unwrap(); let g = f.g.clone(); i.threads.push(json!({"generation":g,"threadId":"fork","cwd":f.project})); }
    let message = |id: &str| f.host.inner.0.lock().unwrap().server_requests.entries().into_iter().find(|e| e["requestId"] == id).map(|e| e["settlement"]["error"]["message"].clone());
    // A conversation not offered the tool in this generation (a fork, a child, an unrestored resume).
    f.host.on_line(&f.frame("1", "fork", "call-1", &full_terms()), &f.g);
    assert_eq!(message("1").unwrap(), "This App session did not offer chirality_point_v1 to this conversation; no point was recorded");
    // A namespaced call of the same name in an offered conversation.
    f.host.on_line(&serde_json::to_vec(&json!({"id":"2","method":"item/tool/call","params":{"threadId":"thread","turnId":"t","callId":"c","tool":points::TOOL,"namespace":"other","arguments":full_terms()}})).unwrap(), &f.g);
    assert_eq!(message("2").unwrap(), "The App offers chirality_point_v1 with no namespace; this call names a namespace, so it is not the App's point tool and no point was recorded");
    // A frame with a result beside its method and identity, in an offered conversation.
    f.host.on_line(&serde_json::to_vec(&json!({"id":"3","method":"item/tool/call","result":{},"params":{"threadId":"thread","turnId":"t","callId":"c","tool":points::TOOL,"arguments":full_terms()}})).unwrap(), &f.g);
    assert_eq!(message("3").unwrap(), "This call to chirality_point_v1 is not framed as a tool call request; no point was recorded");
    // Another (stale) generation: not admitted at all.
    let stale = json!({"appSession":"stale","home":HOME,"spawnCounter":9});
    f.host.on_line(&f.frame("4", "thread", "call-4", &full_terms()), &stale);
    assert!(f.receipts().is_empty());
    assert!(f.records().is_empty());
}

#[test]
fn identical_arguments_in_another_call_are_a_second_point() {
    let f = Fixture::new();
    let first = f.place("1", "thread", "call-1", &full_terms());
    let second = f.place("2", "thread", "call-2", &full_terms());
    assert_ne!(second["point"], first["point"]);
    assert_eq!(f.records().len(), 2);
    assert_eq!(Fixture::view(&f.host, "thread")["points"].as_array().unwrap().len(), 2);
}

#[test]
fn the_run_reading_names_the_run_its_absence_or_why_it_is_not_established() {
    let f = Fixture::new();
    f.host.note_conversation_run(&f.g, "thread", "run:workflow:a", "open");
    assert_eq!(f.place("1", "thread", "c1", &full_terms())["run"], json!({"state":"in run","run":"run:workflow:a"}));
    f.host.note_conversation_run(&f.g, "thread", "run:workflow:a", "ended");
    assert_eq!(f.place("2", "thread", "c2", &full_terms())["run"], json!({"state":"no run"}));
    f.host.note_conversation_run(&f.g, "thread", "run:workflow:b", "start sent");
    assert_eq!(f.place("3", "thread", "c3", &full_terms())["run"], json!({"state":"not established","reason":"start-sent-not-yet-open"}));
    f.host.note_conversation_run(&f.g, "thread", "run:workflow:b", "not opened");
    assert_eq!(f.place("4", "thread", "c4", &full_terms())["run"], json!({"state":"no run"}));
    // A run of another conversation is never this one's.
    f.host.note_conversation_run(&f.g, "other", "run:workflow:c", "open");
    assert_eq!(f.place("5", "thread", "c5", &full_terms())["run"], json!({"state":"no run"}));
}

/// The App's own observation: a call in a turn the App started at the
/// person's press is recorded as such, with that request's reference.
#[test]
fn a_call_in_a_turn_the_person_started_is_recorded_as_observed_so() {
    let f = Fixture::new();
    let mut pipe = reply_pipe(&f.host);
    let (host, g) = (Arc::clone(&f.host), f.g.clone());
    let answer = std::thread::spawn(move || {
        let deadline = std::time::Instant::now() + std::time::Duration::from_secs(10);
        loop {
            if let Some(frame) = written(&mut pipe).into_iter().find(|f| f["method"] == "turn/start") {
                let reply = json!({"id":frame["id"],"result":{"turn":{"id":"turn-1","status":"inProgress","items":[],"itemsView":"full"}}});
                host.on_line(&serde_json::to_vec(&reply).unwrap(), &g);
                return pipe;
            }
            assert!(std::time::Instant::now() < deadline, "no turn/start written");
            std::thread::sleep(std::time::Duration::from_millis(5));
        }
    });
    f.host.turn_start_text(&f.g, "thread", "place a review point").unwrap();
    let _pipe = answer.join().unwrap();
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    assert_eq!(receipt["state"], "recorded", "{receipt}");
    let observed = &f.records()[0]["body"]["observed"];
    assert_eq!(observed["turnStart"], "person-press", "{observed}");
    assert!(observed["requestRef"].as_str().is_some_and(|r| !r.is_empty()));
    assert_eq!(observed["delegation"], "not-established");
    assert_eq!(Fixture::view(&f.host, "thread")["points"][0]["observed"]["turnStart"], "person-press");
}

#[test]
fn terms_after_a_relaunch_equal_the_decoded_values_sent() {
    let mut f = Fixture::new();
    let a = f.place("1", "thread", "call-1", &full_terms())["point"].clone();
    let b = f.place("2", "thread", "call-2", &hostile())["point"].clone();
    f.relaunch();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["offer"]["state"], "offered when this conversation started; restored when it was resumed");
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
    assert_eq!(receipt["run"], json!({"state":"not established","reason":"resumed-earlier-run-unknown"}));
    assert_eq!(Fixture::view(&f.host, "other")["points"], json!([]));
}

/// The INTERLOCUTOR's case: the record is written, then the App quits before
/// the pointer is saved. After the relaunch, with no further placement, the
/// conversation's resumption completes the pointer and the panel shows the
/// one point; until then the reading is never "none recorded".
#[test]
fn a_record_written_before_a_quit_without_its_pointer_is_shown_after_resume_once() {
    let mut f = Fixture::new();
    let aside = f.displace_ledger();
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    assert_eq!(receipt["state"], "recorded", "{receipt}");
    assert!(receipt["persistence"].as_str().unwrap().contains("could not be saved ("), "{receipt}");
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"], json!([]));
    assert_eq!(view["reading"]["whole"], false, "never whole while a pointer is owed");
    assert!(Fixture::reasons(&view).contains("could not be saved"), "{view}");
    f.restore_ledger(&aside);
    f.relaunch();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"].as_array().unwrap().len(), 1);
    assert_eq!(view["points"][0]["point"], receipt["point"]);
    assert_eq!(view["points"][0]["terms"]["arguments"], full_terms());
    assert_eq!(f.records().len(), 1, "exactly one record");
    f.relaunch();
    assert_eq!(f.placed("thread").len(), 1, "completed once");
}

/// Where the App cannot establish that a record without a pointer is this
/// conversation's, the panel shows that, never "no point".
#[test]
fn a_record_that_cannot_be_established_after_a_relaunch_reads_as_uncertain_not_as_none() {
    let mut f = Fixture::new();
    let aside = f.displace_ledger();
    f.place("1", "thread", "call-1", &full_terms());
    f.restore_ledger(&aside);
    let original = std::fs::read_to_string(f.log()).unwrap();
    std::fs::write(f.log(), original.replacen("the checking engineer", "the CHECKING engineer", 1)).unwrap();
    f.relaunch();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"], json!([]));
    assert_eq!(view["reading"]["whole"], false, "{view}");
    assert!(Fixture::reasons(&view).contains("a record naming this conversation could not be established"), "{view}");
    assert!(f.placed("thread").is_empty(), "no pointer for a record that is not sound");
}

#[test]
fn a_pointer_owed_in_this_session_is_completed_before_a_later_call() {
    let f = Fixture::new();
    let aside = f.displace_ledger();
    let first = f.place("1", "thread", "call-1", &full_terms());
    f.restore_ledger(&aside);
    let second = f.place("2", "thread", "call-2", &full_terms());
    assert_eq!(second["persistence"], points::KEPT);
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    let shown: Vec<&Value> = view["points"].as_array().unwrap().iter().map(|p| &p["point"]).collect();
    assert_eq!(shown, [&first["point"], &second["point"]]);
    assert_eq!(f.records().len(), 2);
}

/// Finding 2: after an append error the log is read again: the record found
/// sound is recorded; absent in a log read whole is a refusal; anything else
/// is "not established", and the same call met again is never doubled.
#[test]
fn an_append_error_is_resolved_by_reading_the_log_again_and_never_doubles_a_call() {
    let f = Fixture::new();
    assert_eq!(f.place("1", "thread", "call-1", &full_terms())["state"], "recorded");
    // The line lands but the directory sync fails: recorded, with its pointer.
    crate::storage::fail_directory_for_test(Some(f.log().parent().unwrap().to_path_buf()));
    let landed = f.place("2", "thread", "call-2", &full_terms());
    crate::storage::fail_directory_for_test(None);
    assert_eq!(landed["state"], "recorded", "{landed}");
    assert_eq!(f.records().len(), 2);
    assert_eq!(f.placed("thread").len(), 2);
    // Nothing lands (the log refuses the write): a refusal, nothing doubled.
    use std::os::unix::fs::PermissionsExt;
    std::fs::set_permissions(f.log(), std::fs::Permissions::from_mode(0o400)).unwrap();
    let refused = f.place("3", "thread", "call-3", &full_terms());
    std::fs::set_permissions(f.log(), std::fs::Permissions::from_mode(0o600)).unwrap();
    assert_eq!(refused["state"], "not recorded", "{refused}");
    assert_eq!(f.records().len(), 2);
    // A whole line of this call whose newline was lost: the same call met
    // again (as the lookup's guard) writes nothing and is not established.
    let aside = f.displace_ledger();
    let call = { let i = f.host.inner.0.lock().unwrap(); Host::point_call(&i, &f.g, &serde_json::from_slice(&f.frame("4", "thread", "call-4", &full_terms())).unwrap()) };
    f.host.answer_point_call(call);
    f.restore_ledger(&aside);
    let bytes = std::fs::read(f.log()).unwrap();
    std::fs::write(f.log(), &bytes[..bytes.len() - 1]).unwrap();
    let call = { let i = f.host.inner.0.lock().unwrap(); Host::point_call(&i, &f.g, &serde_json::from_slice(&f.frame("4", "thread", "call-4", &full_terms())).unwrap()) };
    f.host.answer_point_call(call);
    let again = text(f.receipts().last().unwrap());
    assert_eq!(again["state"], "not established", "{again}");
    assert!(again["reason"].as_str().unwrap().contains("not yet terminated"), "{again}");
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], false, "{view}");
    // A later call: the writer terminates that line; the call-4 record is one
    // record, its pointer owed until the next placement completes it.
    assert_eq!(f.place("5", "thread", "call-5", &full_terms())["state"], "recorded");
    let calls: Vec<Value> = f.records().iter().map(|r| r["body"]["source"]["call"].clone()).collect();
    assert_eq!(calls.iter().filter(|c| **c == "call-4").count(), 1, "{calls:?}");
    let owed = Fixture::view(&f.host, "thread");
    assert!(Fixture::reasons(&owed).contains("is in the App's records, but its pointer in this conversation could not be saved"), "owed until a named occasion: {owed}");
    assert_eq!(f.place("6", "thread", "call-6", &full_terms())["state"], "recorded");
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"].as_array().unwrap().len(), 5);
}

/// One placement at a time, and the App's own limit counted from the
/// conversation's durable records: two calls racing at 99 points place one.
#[test]
fn two_calls_racing_at_the_limit_place_exactly_one() {
    let f = Fixture::new();
    for n in 0..points::POINTS_PER_CONVERSATION - 1 {
        assert_eq!(f.place(&format!("p{n}"), "thread", &format!("c{n}"), &json!({"version":1,"operation":"place","label":format!("L{n}")}))["state"], "recorded");
    }
    let racers: Vec<_> = ["r1", "r2"].into_iter().map(|id| {
        let (host, g, root) = (Arc::clone(&f.host), f.g.clone(), f.root.clone());
        let frame = f.frame(id, "thread", id, &full_terms());
        std::thread::spawn(move || { use_store(&root); host.on_line(&frame, &g); crate::records_store::use_store_for_test(None); })
    }).collect();
    for r in racers { r.join().unwrap(); }
    let receipts = f.receipts();
    let last: Vec<Value> = receipts[receipts.len() - 2..].iter().map(text).collect();
    assert_eq!(last.iter().filter(|r| r["state"] == "recorded").count(), 1, "{last:?}");
    let refused = last.iter().find(|r| r["state"] == "not recorded").unwrap();
    assert_eq!(refused["reason"], "This conversation already holds the App's own limit of 100 points; no point was recorded.");
    assert_eq!(f.records().len(), points::POINTS_PER_CONVERSATION);
}

/// Finding 3: the reading's scope comes from the ledger and the store, not
/// from the offer: a conversation whose offer was not restored still shows
/// its points.
#[test]
fn a_conversation_whose_offer_is_not_restored_still_reads_its_points() {
    let mut f = Fixture::new();
    // "plain" holds a point but no offer pointer (as where only the offer tag was lost).
    f.host.inner.0.lock().unwrap().points.offers.push(Offer { generation: f.g.clone(), thread: "plain".into(), home: Some("H-acct".into()), basis: "start" });
    let point = f.place("1", "plain", "call-1", &full_terms())["point"].clone();
    f.relaunch();
    let view = Fixture::view(&f.host, "plain");
    assert_eq!(view["offer"]["state"], "not offered in this App session");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"][0]["point"], point);
    assert_eq!(view["points"][0]["terms"]["arguments"], full_terms());
}

/// Finding 4: one standard of evidence for display.
#[test]
fn altered_truncated_missing_or_doubled_records_show_the_point_with_terms_not_read() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    f.place("2", "thread", "call-2", &full_terms());
    let reason = |n: usize| Fixture::view(&f.host, "thread")["points"][n]["terms"]["reason"].as_str().unwrap_or("read").to_owned();
    let original = std::fs::read_to_string(f.log()).unwrap();
    // Altered: the first record's terms changed, its link untouched; the next line's link breaks.
    std::fs::write(f.log(), original.replacen("the checking engineer", "the CHECKING engineer", 1)).unwrap();
    assert!(reason(0).contains("do not match their recorded digest"), "{}", reason(0));
    assert!(reason(1).contains("not whole at or before"), "{}", reason(1));
    assert!(Fixture::view(&f.host, "thread")["points"][0]["run"].is_null(), "nothing of an unsound record is shown");
    // Truncated: the second record cut short; the first still reads, the reading is not whole.
    let cut = original.trim_end_matches('\n');
    std::fs::write(f.log(), &cut[..cut.len() - 40]).unwrap();
    assert_eq!(reason(0), "read");
    assert!(reason(1).contains("no record with this point's reference"), "{}", reason(1));
    assert!(Fixture::reasons(&Fixture::view(&f.host, "thread")).contains("ends with an unfinished line"));
    // A later placement: the writer sets the fragment aside (W-0); later sound points read.
    let third = f.place("3", "thread", "call-3", &full_terms());
    assert_eq!(third["state"], "recorded", "{third}");
    assert_eq!(reason(2), "read", "a fragment set aside does not block later records");
    // The last record's identity changed to the first's: neither is sound.
    let now = std::fs::read_to_string(f.log()).unwrap();
    let first_id = f.records()[0]["recordId"].as_str().unwrap().to_owned();
    let third_id = f.records().last().unwrap()["recordId"].as_str().unwrap().to_owned();
    std::fs::write(f.log(), now.replacen(&third_id, &first_id, 1)).unwrap();
    assert!(reason(0).contains("record identity more than once"), "{}", reason(0));
    // A broken line in the log: the App cannot establish that a call was not
    // recorded before, so it refuses before any write.
    let broken: Vec<&str> = now.lines().collect();
    let broken = format!("{}\nnot a record\n{}\n", broken[0], broken[1..].join("\n"));
    std::fs::write(f.log(), &broken).unwrap();
    let refused = f.place("4", "thread", "call-4", &full_terms());
    assert_eq!(refused["state"], "not recorded", "{refused}");
    assert!(refused["reason"].as_str().unwrap().starts_with("The App could not read this project's points log whole ("), "{refused}");
    assert_eq!(std::fs::read_to_string(f.log()).unwrap(), broken, "nothing written");
    std::fs::write(f.log(), &now).unwrap();
    // Missing: the log removed.
    std::fs::remove_file(f.log()).unwrap();
    // (The store then reads this project's records in place, where no points log is kept.)
    assert!(reason(0).contains("points log was not found") || reason(0).contains("could not be read"), "{}", reason(0));
    assert_eq!(Fixture::view(&f.host, "thread")["reading"]["whole"], false);
    assert_eq!(Fixture::view(&f.host, "thread")["points"].as_array().unwrap().len(), 3, "still recorded, terms not read");
}

/// Finding 9a through the host's reading: an unknown major version on the
/// last point line is not joined; a newer minor version is read as known.
#[test]
fn the_host_reading_refuses_an_unknown_version_and_reads_a_newer_minor_one_as_known() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    let original = std::fs::read_to_string(f.log()).unwrap();
    std::fs::write(f.log(), original.replacen("\"formatVersion\":\"0.1\"", "\"formatVersion\":\"9.0\"", 1)).unwrap();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"][0]["terms"]["state"], "not read", "{view}");
    assert!(Fixture::reasons(&view).contains("format version 9.0"), "{view}");
    std::fs::write(f.log(), original.replacen("\"formatVersion\":\"0.1\"", "\"formatVersion\":\"0.2\"", 1)).unwrap();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"][0]["terms"]["state"], "read", "{view}");
    assert_eq!(view["points"][0]["formatVersion"], "0.2");
}

/// Finding 5: the store's project identity binds placement and reading.
#[test]
fn a_pointer_of_other_records_and_an_unresolved_link_are_never_read_as_this_projects() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    // A pointer naming other records of this folder (as after the folder's records were replaced).
    let mut foreign = f.placed("thread")[0].clone();
    foreign["storeProject"] = json!("records-project:replaced");
    foreign["point"] = json!(crate::util::opaque_id("pt-").unwrap());
    let mut raw = String::new();
    crate::canonical::canonical(&foreign, &mut raw).unwrap();
    assert_eq!(f.host.tag_conversation(&f.g, "thread", Some("H-acct"), points::TAG_OWNER, &raw)["persistence"], "durable App metadata");
    let view = Fixture::view(&f.host, "thread");
    assert!(view["points"][1]["terms"]["reason"].as_str().unwrap().contains("other records than the records this project folder belongs to now"), "{view}");
    let refused = f.place("2", "thread", "call-2", &full_terms());
    assert_eq!(refused["reason"], "This conversation's points are kept in other records than the records this project folder belongs to now, so the point could not be kept; no point was placed.");
    assert_eq!(f.records().len(), 1);
    // The folder's link to its records removed: nothing is read from a cached path.
    let link = f.project.join(crate::records_store::PROJECT_LINK);
    let kept = std::fs::read(&link).unwrap();
    std::fs::remove_file(&link).unwrap();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"][0]["terms"]["state"], "not read", "{view}");
    assert_eq!(view["reading"]["whole"], false);
    std::fs::write(&link, kept).unwrap();
    assert_eq!(Fixture::view(&f.host, "thread")["points"][0]["terms"]["state"], "read");
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

/// The new kind is a record of the store like any other: the index finds it,
/// and the chain heads count its log.
#[test]
fn the_records_index_and_chain_heads_treat_a_point_record_as_any_record() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    let id = f.records()[0]["recordId"].as_str().unwrap().to_owned();
    let found = crate::records_index::with_index(&f.project, |ix| ix.entries_with(&id)).unwrap();
    assert_eq!(found.len(), 1);
    let heads = crate::records_index::chain_heads(&f.project);
    assert!(heads.to_string().contains(&crate::storage::log_rel(None, points::WRITER)) || heads.to_string().contains(points::WRITER), "{heads}");
}

/// DEL-04-03: export copies the points log byte for byte and both the App's
/// check and the package's own verifier accept it; a closed project keeps its
/// points readable and refuses a new one; a legal hold and disposal apply as
/// to any record (after disposal the point is shown with terms not read); and
/// the export the disposal relied on carries it into another store unchanged.
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
    let act = |action: &str, bag: Option<&Path>| crate::records_retention::prepare(&f.project, action, bag, &actor, &observed).and_then(|p| crate::records_retention::apply(p, &actor, &observed));
    act("set-hold", None).unwrap();
    act("close", None).unwrap();
    // Closed after admission: the point stays readable; a new one is refused before any write.
    assert_eq!(Fixture::view(&f.host, "thread")["points"][0]["terms"]["state"], "read");
    let closed = f.place("2", "thread", "call-2", &full_terms());
    assert_eq!(closed["state"], "not recorded");
    assert!(closed["reason"].as_str().unwrap().starts_with("The App's records store did not take the point"), "{closed}");
    assert_eq!(std::fs::read(&log).unwrap(), bytes);
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
    assert_eq!(view["points"].as_array().unwrap().len(), 1, "{view}");
    assert_eq!(view["points"][0]["terms"]["state"], "not read", "{view}");
    assert_eq!(f.place("3", "thread", "call-3", &full_terms())["state"], "not recorded");
    assert!(!log.exists());

    // The export the disposal relied on, imported as a package into another store.
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: f.root.join("destination-store"), placement: crate::records_store::Placement::Test, limits: vec![] })));
    let plan = crate::records_store::package::prepare(&f.project, &current, &actor, &observed).unwrap();
    assert_eq!(crate::records_store::package::apply(plan, &actor, &observed).unwrap()["state"], "package imported");
    let imported = crate::records_store::project_dir(&f.root.join("destination-store"), &project).join(&rel);
    assert_eq!(std::fs::read(&imported).unwrap(), bytes);
    let reading = points::LogReading::read(&imported).unwrap();
    assert_eq!(reading.lines.len(), 1);
    assert_eq!(reading.lines[0].entry["body"]["arguments"], full_terms());
    assert!(reading.soundness(0).is_ok());
}
