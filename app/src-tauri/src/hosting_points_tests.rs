//! DEL-02-03 REQ-008: a point placed through constructed supplier frames, its
//! record in the records store, its pointer in the App ledger, its receipt and
//! reply, and the conversation's reading. No Codex, no App: an admitted
//! thread, the App's own ledger, a test records store, the Host's own point
//! recorder (its worker and bounded queue) and, where the reply is observed, a
//! test reply pipe. What these tests do not observe: a process ending exactly
//! between the record and its pointer (a ledger that refuses the pointer
//! stands for it), and the production Continue path (the resume step is
//! called directly).
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
/// The Host's self-reference, as `start` sets it, and the test store on its
/// point recorder's thread.
fn start(host: &Arc<Host>, root: &Path) {
    *host.this.lock().unwrap() = Arc::downgrade(host);
    let root = root.to_path_buf();
    host.inner.0.lock().unwrap().points.hooks.worker_setup = Some(Arc::new(move || use_store(&root)));
}
fn generation(host: &Host, spawn: u64) -> Value {
    json!({"appSession":host.inner.0.lock().unwrap().app_session,"home":HOME,"spawnCounter":spawn})
}
/// A Host whose generation is ready, holding the conversations, the records
/// capability in `project`, and the point tool's offer for `offered`.
fn admitted(host: &Arc<Host>, project: &Path, reads: &Path, g: &Value, threads: &[&str], offered: &[&str]) {
    host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(project, reads.to_path_buf()).unwrap()), context(project));
    let mut i = host.inner.0.lock().unwrap();
    i.generation = g.clone();
    i.state = "ready".into();
    for thread in threads {
        i.threads.push(json!({"generation":g,"threadId":thread,"cwd":project}));
        if offered.contains(thread) {
            Host::note_point_offer(&mut i, g, &json!(thread), &json!({"dynamicTools":[crate::records_access::definition(), points::definition()]}));
        }
    }
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
        start(&host, &root);
        host.configure_recovery(ledger.clone()).unwrap();
        let g = generation(&host, 1);
        admitted(&host, &project, &root.join("app/reads.jsonl"), &g, &["thread", "other", "unindexed", "plain"], &["thread", "other", "unindexed"]);
        for thread in ["thread", "other", "plain"] { host.observe_conversation_project(&g, thread, Some("H-acct"), &context(&project)).unwrap(); }
        Self { root, project, ledger, host, g, _custody: Some(custody) }
    }
    fn frame(&self, id: &str, thread: &str, call: &str, arguments: &Value) -> Vec<u8> {
        serde_json::to_vec(&json!({"id":id,"method":"item/tool/call","params":{"threadId":thread,"turnId":"turn-1","callId":call,"tool":points::TOOL,"namespace":null,"arguments":arguments}})).unwrap()
    }
    fn drain(&self) {
        self.host.drain_points_for_test();
    }
    /// One call through the frame receiver and the point recorder; the receipt prepared.
    fn place(&self, id: &str, thread: &str, call: &str, arguments: &Value) -> Value {
        let before = self.receipts().len();
        self.host.on_line(&self.frame(id, thread, call, arguments), &self.g);
        self.drain();
        let receipts = self.receipts();
        assert_eq!(receipts.len(), before + 1, "one receipt per admitted call");
        text(receipts.last().unwrap())
    }
    fn receipts(&self) -> Vec<Value> {
        self.host.inner.0.lock().unwrap().points.hooks.receipts.clone()
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
    fn tags(&self, thread: &str, kind: &str) -> Vec<Value> {
        self.host.tags_of("H-acct", thread, points::TAG_OWNER).iter().filter_map(|t| points::decode(t["value"].as_str().unwrap())).filter(|v| v["kind"] == kind).collect()
    }
    fn placed(&self, thread: &str) -> Vec<Value> {
        self.tags(thread, "placed")
    }
    /// The conversation's row as the status path gives it, once the point
    /// recorder has published whatever that read asked it to read.
    fn view(host: &Host, thread: &str) -> Value {
        let row = |host: &Host| host.snapshot()["points"].as_array().unwrap().iter().find(|v| v["threadId"] == thread).cloned().unwrap();
        let mut seen = row(host);
        for _ in 0..4 {
            let reasons = seen["reading"]["reasons"].to_string();
            if !(reasons.contains("it is reading them")) { break; }
            host.drain_points_for_test();
            seen = row(host);
        }
        seen
    }
    /// A relaunch: this Host ends as a killed process does; a new Host opens
    /// the same ledger and store, resumes the conversations, and runs what an
    /// explicit Continue runs for points.
    fn relaunch(&mut self) {
        self.host.end_process_for_test();
        self._custody = None;
        self._custody = Some(crate::hold_app_data_for_test(&self.root.join("app")).unwrap());
        let host = Arc::new(Host::new());
        start(&host, &self.root);
        host.configure_recovery(self.ledger.clone()).unwrap();
        self.g = generation(&host, 1);
        admitted(&host, &self.project, &self.root.join("app/reads.jsonl"), &self.g, &["thread", "other", "plain"], &[]);
        for thread in ["thread", "other", "plain"] { host.restore_point_offer(&self.g, thread); }
        host.drain_points_for_test();
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
    fn hooks(&self) -> std::sync::MutexGuard<'_, super::super::Inner> {
        self.host.inner.0.lock().unwrap()
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
fn small(n: usize) -> Value {
    json!({"version":1,"operation":"place","label":format!("L{n}")})
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
/// Records and placed pointers of a conversation, counted from another thread.
fn counts(host: &Arc<Host>, project: &Path, thread: &'static str) -> impl Fn() -> (usize, usize) + Send + 'static {
    let (host, project) = (Arc::clone(host), project.to_path_buf());
    move || {
        let log = crate::records_store::attach(&project, false).ok().and_then(|a| a.dir).map(|d| d.join(crate::storage::log_rel(None, points::WRITER)));
        let records = log.filter(|p| p.exists()).map(|p| crate::records::read_log(&p).0.iter().filter(|e| e["kind"] == points::KIND).count()).unwrap_or(0);
        let pointers = host.tags_of("H-acct", thread, points::TAG_OWNER).iter().filter(|t| t["value"].as_str().unwrap().contains("\"placed\"")).count();
        (records, pointers)
    }
}

#[test]
fn a_placement_writes_the_record_then_the_pointer_then_answers_recorded() {
    let f = Fixture::new();
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    assert_eq!(receipt["state"], "recorded", "{receipt}");
    assert_eq!(receipt["persistence"], points::KEPT);
    assert_eq!(receipt["run"], json!({"state":"no run"}));
    let point = receipt["point"].as_str().unwrap();
    let records = f.records();
    assert_eq!(records.len(), 1);
    let body = &records[0]["body"];
    assert_eq!(body["point"], point);
    assert_eq!(body["arguments"], full_terms());
    assert_eq!(body["argumentsDigest"]["value"], crate::util::sha256_hex({ let mut s = String::new(); crate::canonical::canonical(&full_terms(), &mut s).unwrap(); s }.as_bytes()));
    assert_eq!(body["source"], json!({"home":HOME,"homeClass":"H-acct","generation":crate::recovery::generation_ref(&f.g).unwrap(),"thread":"thread","turn":"turn-1","call":"call-1","request":"1"}));
    assert_eq!(body["project"], f.project.to_str().unwrap());
    let store = json!(crate::records_store::attach(&f.project, false).unwrap().project.unwrap());
    assert_eq!(body["storeProject"], store);
    assert_eq!(body["observed"], json!({"caller":"agent-through-point-tool","turnStart":"not-observed","delegation":"not-established"}));
    // The pointer holds identities and the digest only.
    let placed = f.placed("thread");
    assert_eq!(placed.len(), 1);
    assert_eq!(placed[0]["record"], records[0]["recordId"]);
    assert_eq!(placed[0]["storeProject"], store);
    assert!(placed[0].get("run").is_none() && placed[0].get("observed").is_none() && placed[0].get("placer").is_none());
    // The offer pointer of the start, and the one bound to the store project before the first record.
    let offers = f.tags("thread", "offered");
    assert_eq!(offers.len(), 2, "{offers:?}");
    assert!(offers[0].get("storeProject").is_none());
    assert_eq!(offers[1]["storeProject"], store);
    assert_eq!(offers[1]["project"], f.project.to_str().unwrap());
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["offer"]["state"], "offered at start in this App session");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"][0]["point"], point);
    assert_eq!(view["points"][0]["terms"], json!({"state":"read","arguments":full_terms()}));
    assert_eq!(view["points"][0]["run"], json!({"state":"no run"}));
    assert_eq!(view["points"][0]["observed"]["turnStart"], "not-observed");
    let entry = f.host.inner.0.lock().unwrap().server_requests.records().into_iter().find(|r| r["requestIdentity"] == "1").unwrap();
    assert_eq!(entry["originClass"], "named-service");
    assert_eq!(entry["settlement"]["origin"]["ruleName"], "point-record");
    assert!(entry["settlement"].get("nativeContent").is_none());
}

/// Finding 1: the panel reads `host_status`, whose snapshot is the native
/// projection the runtime receives; the points are on it.
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

/// Finding 1: a status read binds no store, reads no log and waits for no
/// placement: with the point recorder busy and the placement guard held, it
/// returns what was published; a changed log reads as not whole until the
/// recorder has read it again.
#[test]
fn a_status_read_takes_the_published_reading_and_never_waits_for_the_recorder() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    let (release, held) = std::sync::mpsc::channel::<()>();
    let (busy, started) = std::sync::mpsc::channel::<()>();
    let sender = f.hooks().points.queue.clone().unwrap();
    sender.send(Job::Run(Box::new(move || { let _guard = one_at_a_time(); let _ = busy.send(()); let _ = held.recv(); }))).unwrap();
    started.recv().unwrap();
    let begun = std::time::Instant::now();
    let row = f.host.snapshot()["points"].as_array().unwrap().iter().find(|v| v["threadId"] == "thread").cloned().unwrap();
    assert!(begun.elapsed() < std::time::Duration::from_secs(5));
    assert_eq!(row["reading"]["whole"], true, "{row}");
    assert_eq!(row["points"][0]["terms"]["state"], "read");
    // The log changes while the recorder is busy: not whole, with the reason, until it reads again.
    let log = f.log();
    let bytes = std::fs::read(&log).unwrap();
    std::fs::write(&log, &bytes).unwrap();
    let row = f.host.snapshot()["points"].as_array().unwrap().iter().find(|v| v["threadId"] == "thread").cloned().unwrap();
    assert_eq!(row["reading"]["whole"], false);
    assert!(Fixture::reasons(&row).contains("it is reading them again"), "{row}");
    release.send(()).unwrap();
    assert_eq!(Fixture::view(&f.host, "thread")["reading"]["whole"], true);
}

/// Finding 1: the queue is bounded; a call it cannot take is refused with the
/// App's sentence and answered, never placed on the receiver.
#[test]
fn a_call_the_recorder_cannot_take_is_refused_and_answered_from_the_receiver() {
    let f = Fixture::new();
    let mut pipe = reply_pipe(&f.host);
    f.place("0", "thread", "call-0", &full_terms());
    written(&mut pipe);
    let (release, held) = std::sync::mpsc::channel::<()>();
    let (busy, started) = std::sync::mpsc::channel::<()>();
    let sender = f.hooks().points.queue.clone().unwrap();
    sender.send(Job::Run(Box::new(move || { let _ = busy.send(()); let _ = held.recv(); }))).unwrap();
    started.recv().unwrap();
    for _ in 0..QUEUE { sender.try_send(Job::Run(Box::new(|| {}))).unwrap(); }
    f.host.on_line(&f.frame("1", "thread", "call-1", &full_terms()), &f.g);
    let replies = written(&mut pipe);
    assert_eq!(replies.len(), 1, "answered from the receiver");
    let receipt = text(&replies[0]["result"]);
    assert_eq!(receipt["state"], "not recorded");
    assert_eq!(receipt["reason"], "The App's point recorder could not take this call now, so no point was recorded.");
    release.send(()).unwrap();
    f.drain();
    assert_eq!(f.records().len(), 1);
}

/// Finding 7 and 11: through the real receiver and a test reply pipe, the
/// record is written before its pointer, and both before the reply; a
/// repeated request identity is refused and not answered again, in the same
/// generation and after it closed, and writes nothing.
#[test]
fn through_the_receiver_the_record_precedes_the_pointer_which_precedes_the_reply_and_a_repeat_is_not_answered_again() {
    let f = Fixture::new();
    let mut pipe = reply_pipe(&f.host);
    let seen = Arc::new(std::sync::Mutex::new(vec![]));
    let count = counts(&f.host, &f.project, "thread");
    let (after, before) = (Arc::clone(&seen), Arc::clone(&seen));
    let count_after = counts(&f.host, &f.project, "thread");
    { let mut i = f.hooks();
      i.points.hooks.after_append = Some(Box::new(move || after.lock().unwrap().push(("after the record", count_after()))));
      i.points.hooks.before_reply = Some(Box::new(move || before.lock().unwrap().push(("before the reply", count())))); }
    f.host.on_line(&f.frame("7", "thread", "call-1", &full_terms()), &f.g);
    f.drain();
    assert_eq!(*seen.lock().unwrap(), vec![("after the record", (1, 0)), ("before the reply", (1, 1))], "record, then pointer, then reply");
    let replies = written(&mut pipe);
    assert_eq!(replies.len(), 1);
    assert_eq!(replies[0]["id"], "7");
    assert_eq!(text(&replies[0]["result"])["state"], "recorded");
    f.host.on_line(&f.frame("7", "thread", "call-1", &full_terms()), &f.g);
    f.drain();
    assert!(written(&mut pipe).is_empty(), "the first answer stands; no second reply");
    assert_eq!(f.records().len(), 1);
    assert!(f.host.snapshot()["journal"].as_array().unwrap().iter().any(|j| j["reason"] == "duplicate-request-identity"), "journaled");
    { let mut i = f.host.inner.0.lock().unwrap(); Host::close_generation(&mut i); }
    f.host.on_line(&f.frame("7", "thread", "call-1", &full_terms()), &f.g);
    f.host.on_line(&f.frame("8", "thread", "call-2", &full_terms()), &f.g);
    f.drain();
    assert!(written(&mut pipe).is_empty());
    assert_eq!(f.records().len(), 1);
    assert_eq!(f.placed("thread").len(), 1);
}

/// A new request identity carrying the same call identifier in the same
/// conversation and turn is another placement: the record is keyed on both.
#[test]
fn a_new_request_identity_with_the_same_call_identifier_is_another_placement() {
    let f = Fixture::new();
    let a = f.place("1", "thread", "call-1", &full_terms());
    let b = f.place("2", "thread", "call-1", &full_terms());
    assert_eq!((a["state"].clone(), b["state"].clone()), (json!("recorded"), json!("recorded")));
    assert_ne!(a["point"], b["point"]);
    assert_eq!(f.records().len(), 2);
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
    let receipt = f.place("5", "unindexed", "call-5", &full_terms());
    assert_eq!(receipt["reason"], "No App project is known for this conversation, so the point could not be kept; no point was placed.");
    assert!(f.records().is_empty());
    assert!(f.placed("thread").is_empty());
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"], json!([]));
    assert_eq!(view["refused"].as_array().unwrap().len(), 4);
    assert_eq!(view["reading"]["whole"], true);
    f.host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(&f.root.join("other-project"), f.root.join("app/reads.jsonl")).unwrap()), context(&f.root.join("other-project")));
    let receipt = f.place("6", "thread", "call-6", &full_terms());
    assert_eq!(receipt["reason"], "This conversation's App project is not the project the App has open now, so the point could not be kept; no point was placed.");
    f.host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(&f.project, f.root.join("app/reads.jsonl")).unwrap()), context(&f.project));
    let before = (files(&f.project), files(&f.root.join("store")));
    f.host.on_points_worker(|| crate::records_store::use_store_for_test(Some(Err("invented store refusal".into()))));
    let receipt = f.place("7", "thread", "call-7", &full_terms());
    let root = f.root.clone();
    f.host.on_points_worker(move || use_store(&root));
    assert_eq!((files(&f.project), files(&f.root.join("store"))), before, "nothing written in the project or the store");
    assert!(receipt["reason"].as_str().unwrap().starts_with("The App's records store did not take the point (") && receipt["reason"].as_str().unwrap().contains("invented store refusal"), "{receipt}");
    assert!(f.records().is_empty());
    assert!(f.placed("thread").is_empty());
}

/// Calls naming the point tool that the host does not admit as point calls
/// get the register's true sentence on the reply pipe, and write nothing.
#[test]
fn calls_not_admitted_as_point_calls_are_answered_with_a_true_sentence_and_write_nothing() {
    let f = Fixture::new();
    let mut pipe = reply_pipe(&f.host);
    { let mut i = f.host.inner.0.lock().unwrap(); let g = f.g.clone(); i.threads.push(json!({"generation":g,"threadId":"fork","cwd":f.project})); }
    let reply = |pipe: &mut std::fs::File, id: &str| -> String {
        let replies = written(pipe);
        assert_eq!(replies.len(), 1, "{replies:?}");
        assert_eq!(replies[0]["id"], id);
        replies[0]["error"]["message"].as_str().unwrap_or_else(|| panic!("{}", replies[0])).to_owned()
    };
    f.host.on_line(&f.frame("1", "fork", "call-1", &full_terms()), &f.g);
    assert_eq!(reply(&mut pipe, "1"), "This App session did not offer chirality_point_v1 to this conversation; no point was recorded");
    f.host.on_line(&serde_json::to_vec(&json!({"id":"2","method":"item/tool/call","params":{"threadId":"thread","turnId":"t","callId":"c","tool":points::TOOL,"namespace":"other","arguments":full_terms()}})).unwrap(), &f.g);
    assert_eq!(reply(&mut pipe, "2"), "The App offers chirality_point_v1 with no namespace; this call names a namespace, so it is not the App's point tool and no point was recorded");
    f.host.on_line(&serde_json::to_vec(&json!({"id":"3","method":"item/tool/call","result":{},"params":{"threadId":"thread","turnId":"t","callId":"c","tool":points::TOOL,"arguments":full_terms()}})).unwrap(), &f.g);
    assert_eq!(reply(&mut pipe, "3"), "This call to chirality_point_v1 is not framed as a tool call request; no point was recorded");
    // Finding 7: a protocol version other than 2.0.
    f.host.on_line(&serde_json::to_vec(&json!({"jsonrpc":false,"id":"4","method":"item/tool/call","params":{"threadId":"thread","turnId":"t","callId":"c","tool":points::TOOL,"arguments":full_terms()}})).unwrap(), &f.g);
    assert_eq!(reply(&mut pipe, "4"), "This call to chirality_point_v1 is not framed as a tool call request; no point was recorded");
    // Finding 7: a frame the generic classifier takes as malformed, with an identity the App can answer.
    f.host.on_line(&serde_json::to_vec(&json!({"id":"5","method":"item/tool/call","observation":"x","params":{"threadId":"thread","turnId":"t","callId":"c","tool":points::TOOL,"arguments":full_terms()}})).unwrap(), &f.g);
    assert_eq!(reply(&mut pipe, "5"), "This call to chirality_point_v1 is not framed as a tool call request; no point was recorded");
    let stale = json!({"appSession":"stale","home":HOME,"spawnCounter":9});
    f.host.on_line(&f.frame("6", "thread", "call-6", &full_terms()), &stale);
    f.drain();
    assert!(written(&mut pipe).is_empty());
    assert!(f.receipts().is_empty());
    assert!(f.records().is_empty());
    assert!(f.placed("thread").is_empty() && f.placed("fork").is_empty());
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
    f.host.note_conversation_run(&f.g, "thread", "run:workflow:c", "open");
    f.host.note_conversation_run(&f.g, "other", "run:workflow:d", "open");
    assert_eq!(f.place("5", "other", "c5", &full_terms())["run"], json!({"state":"in run","run":"run:workflow:d"}));
}

/// Finding 10: Codex restarted in the same App session: the conversation's
/// restored offer keeps the generation it was first made in, and the run
/// reading comes from what the App knows across that boundary.
#[test]
fn after_codex_restarts_in_the_same_app_session_the_run_reading_says_what_the_app_knows() {
    let f = Fixture::new();
    f.host.note_conversation_run(&f.g, "thread", "run:workflow:a", "open");
    let g2 = generation(&f.host, 2);
    admitted(&f.host, &f.project, &f.root.join("app/reads.jsonl"), &g2, &["thread", "other"], &[]);
    f.host.restore_point_offer(&g2, "thread");
    f.host.restore_point_offer(&g2, "other");
    f.drain();
    let place = |id: &str, thread: &str| {
        f.host.on_line(&f.frame(id, thread, id, &full_terms()), &g2);
        f.drain();
        let receipt = text(f.receipts().last().unwrap());
        assert_eq!(receipt["state"], "recorded", "{receipt}");
        assert_eq!(f.records().last().unwrap()["body"]["run"], receipt["run"], "the record holds the reading");
        receipt
    };
    assert_eq!(place("1", "thread")["run"], json!({"state":"not established","reason":"codex-restarted-run-unknown"}));
    assert_eq!(place("2", "other")["run"], json!({"state":"no run"}), "began in this App session with no run open");
    f.host.note_conversation_run(&g2, "thread", "run:workflow:b", "open");
    assert_eq!(place("3", "thread")["run"], json!({"state":"in run","run":"run:workflow:b"}));
    assert_eq!(Fixture::view(&f.host, "thread")["offer"]["state"], "offered when this conversation started; restored when it was resumed");
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
    let receipt = f.place("9", "thread", "call-9", &full_terms());
    assert_eq!(receipt["state"], "recorded");
    assert_eq!(receipt["run"], json!({"state":"not established","reason":"resumed-earlier-run-unknown"}));
    let other = Fixture::view(&f.host, "other");
    assert_eq!(other["points"], json!([]));
    assert_eq!(other["reading"]["whole"], true, "{other}");
}

/// The INTERLOCUTOR's case: the record is written, and the pointer is not
/// saved before the App quits (a ledger that refuses it stands for the quit).
/// After the relaunch, with no further placement, the conversation's
/// resumption completes the pointer and the panel shows the one point.
#[test]
fn a_record_written_without_its_pointer_before_a_quit_is_shown_after_resume_once() {
    let mut f = Fixture::new();
    f.place("0", "thread", "call-0", &small(0));
    let aside = f.displace_ledger();
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    assert_eq!(receipt["state"], "recorded", "{receipt}");
    assert!(receipt["persistence"].as_str().unwrap().contains("could not be saved ("), "{receipt}");
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"].as_array().unwrap().len(), 1);
    assert_eq!(view["reading"]["whole"], false, "never whole while a pointer is owed");
    assert!(Fixture::reasons(&view).contains("could not be saved"), "{view}");
    f.restore_ledger(&aside);
    f.relaunch();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"].as_array().unwrap().len(), 2);
    assert_eq!(view["points"][1]["point"], receipt["point"]);
    assert_eq!(view["points"][1]["terms"]["arguments"], full_terms());
    assert_eq!(f.records().len(), 2, "exactly the two records");
    f.relaunch();
    assert_eq!(f.placed("thread").len(), 2, "completed once");
}

/// The conversation's binding to its records is kept before its first
/// record: where it cannot be kept, nothing is written.
#[test]
fn a_first_placement_whose_binding_cannot_be_kept_writes_nothing() {
    let f = Fixture::new();
    let aside = f.displace_ledger();
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    f.restore_ledger(&aside);
    assert_eq!(receipt["state"], "not recorded", "{receipt}");
    assert!(receipt["reason"].as_str().unwrap().starts_with("The conversation's binding to its records could not be saved ("), "{receipt}");
    assert!(f.records().is_empty());
}

/// Where the App cannot establish that a record without a pointer is this
/// conversation's, the panel shows that, never "no point".
#[test]
fn a_record_that_cannot_be_established_after_a_relaunch_reads_as_uncertain_not_as_none() {
    let mut f = Fixture::new();
    f.place("0", "thread", "call-0", &small(0));
    let aside = f.displace_ledger();
    f.place("1", "thread", "call-1", &full_terms());
    f.restore_ledger(&aside);
    let original = std::fs::read_to_string(f.log()).unwrap();
    std::fs::write(f.log(), original.replacen("the checking engineer", "the CHECKING engineer", 1)).unwrap();
    f.relaunch();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], false, "{view}");
    assert!(Fixture::reasons(&view).contains("a record naming this conversation could not be established"), "{view}");
    assert_eq!(f.placed("thread").len(), 1, "no pointer for a record that is not sound");
}

/// Finding 3: on an indexed resume the App always accounts for the records:
/// a log whose only line is unreadable reads as not whole, never as none
/// recorded; and a sound record of a conversation holding no tag at all is
/// found and shown.
#[test]
fn an_indexed_resume_accounts_for_the_records_whatever_tags_the_conversation_holds() {
    let mut f = Fixture::new();
    f.place("1", "other", "call-1", &small(1));
    let log = f.log();
    let first = std::fs::read(&log).unwrap();
    std::fs::write(&log, b"not a record\n").unwrap();
    f.relaunch();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"], json!([]));
    assert_eq!(view["reading"]["whole"], false, "{view}");
    assert!(Fixture::reasons(&view).contains("the points log is not whole from line 1"), "{view}");
    // A sound record naming "plain", which holds no tag of this owner.
    std::fs::write(&log, &first).unwrap();
    let store = crate::records_store::attach(&f.project, false).unwrap().project.unwrap();
    let source = points::Source { home: HOME.into(), home_class: "H-acct".into(), generation: crate::recovery::generation_ref(&f.g).unwrap(), thread: "plain".into(), turn: "t".into(), call: "c".into(), request: json!("r") };
    let digest = points::digest(&small(2)).unwrap();
    let body = points::record_body("pt-00000000-0000-4000-8000-000000000002", &source, f.project.to_str().unwrap(), &store, &points::run_none(), &points::observed(None, false), &small(2), &digest, "t");
    crate::records::append_reserved(&log, points::KIND, &crate::records::APP_WRITER, body, "rec:app:00000000-0000-4000-8000-000000000002".into(), None, None, crate::records::RecordSet::Complete, crate::schema_validation::bundled()).unwrap();
    assert!(f.tags("plain", "offered").is_empty() && f.placed("plain").is_empty());
    f.relaunch();
    let view = Fixture::view(&f.host, "plain");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"][0]["terms"]["arguments"], small(2));
}

#[test]
fn a_pointer_owed_in_this_session_is_completed_before_a_later_call() {
    let f = Fixture::new();
    f.place("0", "thread", "call-0", &small(0));
    let aside = f.displace_ledger();
    let first = f.place("1", "thread", "call-1", &full_terms());
    f.restore_ledger(&aside);
    let second = f.place("2", "thread", "call-2", &full_terms());
    assert_eq!(second["persistence"], points::KEPT);
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    let shown: Vec<&Value> = view["points"].as_array().unwrap().iter().map(|p| &p["point"]).collect();
    assert_eq!(shown.len(), 3);
    assert_eq!((shown[1], shown[2]), (&first["point"], &second["point"]));
}

/// Finding 2 and 11: an append error through the receiver is resolved by
/// reading the log again: a line that landed is recorded, a log read whole
/// without it is a refusal, and anything else is not established; the same
/// call met again is never doubled, and the writer's own tail recovery runs
/// before a later placement.
#[test]
fn an_append_error_through_the_receiver_is_resolved_by_reading_the_log_again_and_never_doubles_a_call() {
    let f = Fixture::new();
    assert_eq!(f.place("1", "thread", "call-1", &full_terms())["state"], "recorded");
    let dir = f.log().parent().unwrap().to_path_buf();
    f.host.on_points_worker(move || crate::storage::fail_directory_for_test(Some(dir)));
    let landed = f.place("2", "thread", "call-2", &full_terms());
    f.host.on_points_worker(|| crate::storage::fail_directory_for_test(None));
    assert_eq!(landed["state"], "recorded", "{landed}");
    assert_eq!(f.placed("thread").len(), 2);
    f.hooks().points.hooks.append = Some(Box::new(|_, _, _| Err("injected: nothing landed".into())));
    let refused = f.place("3", "thread", "call-3", &full_terms());
    assert_eq!(refused["state"], "not recorded", "{refused}");
    assert!(refused["reason"].as_str().unwrap().contains("injected: nothing landed"));
    // The line lands without its newline and the writer reports an error.
    f.hooks().points.hooks.append = Some(Box::new(|log, body, id| {
        let entry = crate::records::append_reserved(log, points::KIND, &crate::records::APP_WRITER, body, id, None, None, crate::records::RecordSet::Complete, crate::schema_validation::bundled())?;
        let bytes = std::fs::read(log).unwrap();
        std::fs::write(log, &bytes[..bytes.len() - 1]).unwrap();
        let _ = entry;
        Err("injected: the sync was not confirmed".into())
    }));
    let uncertain = f.place("4", "thread", "call-4", &full_terms());
    assert_eq!(uncertain["state"], "not established", "{uncertain}");
    assert!(uncertain["point"].as_str().is_some());
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], false, "{view}");
    // A later call: the writer's tail recovery terminates that line first; it is one record.
    assert_eq!(f.place("5", "thread", "call-5", &full_terms())["state"], "recorded");
    let calls: Vec<Value> = f.records().iter().map(|r| r["body"]["source"]["call"].clone()).collect();
    assert_eq!(calls.iter().filter(|c| **c == "call-4").count(), 1, "{calls:?}");
    assert_eq!(calls.iter().filter(|c| **c == "call-3").count(), 0);
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"].as_array().unwrap().len(), 4, "the call-4 record completed before the later placement");
}

/// Finding 2: the App's own limit counts the sound records after the
/// writer's tail recovery: a whole 100th line that lost its newline is
/// counted, and a record that is not sound is not.
#[test]
fn the_limit_counts_sound_records_after_tail_recovery() {
    let f = Fixture::new();
    for n in 0..points::POINTS_PER_CONVERSATION {
        assert_eq!(f.place(&format!("p{n}"), "thread", &format!("c{n}"), &small(n))["state"], "recorded");
    }
    let bytes = std::fs::read(f.log()).unwrap();
    std::fs::write(f.log(), &bytes[..bytes.len() - 1]).unwrap();
    let refused = f.place("over", "thread", "over", &full_terms());
    assert_eq!(refused["reason"], "This conversation already holds the App's own limit of 100 points; no point was recorded.", "{refused}");
    assert_eq!(f.records().len(), points::POINTS_PER_CONVERSATION);
    // The last record's terms altered (the release's unsigned-chain limit: no
    // later line's link breaks): it is not sound, so it is not counted.
    let text = std::fs::read_to_string(f.log()).unwrap();
    let at = text.rfind("\"label\":\"L99\"").unwrap();
    std::fs::write(f.log(), format!("{}\"label\":\"LXX\"{}", &text[..at], &text[at + "\"label\":\"L99\"".len()..])).unwrap();
    assert_eq!(f.place("after", "thread", "after", &full_terms())["state"], "recorded");
    assert_eq!(f.records().len(), points::POINTS_PER_CONVERSATION + 1);
    assert_eq!(f.place("again", "thread", "again", &full_terms())["state"], "not recorded");
}

/// One placement at a time: two calls racing at 99 points place one.
#[test]
fn two_calls_racing_at_the_limit_place_exactly_one() {
    let f = Fixture::new();
    for n in 0..points::POINTS_PER_CONVERSATION - 1 {
        assert_eq!(f.place(&format!("p{n}"), "thread", &format!("c{n}"), &small(n))["state"], "recorded");
    }
    let racers: Vec<_> = ["r1", "r2"].into_iter().map(|id| {
        let (host, g) = (Arc::clone(&f.host), f.g.clone());
        let frame = f.frame(id, "thread", id, &full_terms());
        std::thread::spawn(move || host.on_line(&frame, &g))
    }).collect();
    for r in racers { r.join().unwrap(); }
    f.drain();
    let receipts = f.receipts();
    let last: Vec<Value> = receipts[receipts.len() - 2..].iter().map(text).collect();
    assert_eq!(last.iter().filter(|r| r["state"] == "recorded").count(), 1, "{last:?}");
    assert_eq!(last.iter().find(|r| r["state"] == "not recorded").unwrap()["reason"], "This conversation already holds the App's own limit of 100 points; no point was recorded.");
    assert_eq!(f.records().len(), points::POINTS_PER_CONVERSATION);
}

/// Finding 3: the reading's scope comes from the ledger and the store, not
/// from the offer.
#[test]
fn a_conversation_whose_offer_is_not_restored_still_reads_its_points() {
    let mut f = Fixture::new();
    f.host.inner.0.lock().unwrap().points.offers.push(Offer { generation: f.g.clone(), thread: "plain".into(), home: Some("H-acct".into()), basis: "start", origin: f.g.clone() });
    let point = f.place("1", "plain", "call-1", &full_terms())["point"].clone();
    f.relaunch();
    let view = Fixture::view(&f.host, "plain");
    assert_eq!(view["offer"]["state"], "offered when this conversation started; restored when it was resumed", "its bound offer pointer restores it");
    assert_eq!(view["reading"]["whole"], true, "{view}");
    assert_eq!(view["points"][0]["point"], point);
    // Without any offer restored (another definition offered now), the points are still read.
    for t in f.host.inner.0.lock().unwrap().points.offers.iter_mut() { t.basis = "start"; }
    f.host.inner.0.lock().unwrap().points.offers.clear();
    let view = Fixture::view(&f.host, "plain");
    assert_eq!(view["offer"]["state"], "not offered in this App session");
    assert_eq!(view["points"][0]["terms"]["arguments"], full_terms());
}

/// Finding 4: one standard of evidence for display, and every failed join in
/// the conversation's reading.
#[test]
fn altered_truncated_missing_or_doubled_records_show_the_point_with_terms_not_read() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    f.place("2", "thread", "call-2", &full_terms());
    let reason = |n: usize| Fixture::view(&f.host, "thread")["points"][n]["terms"]["reason"].as_str().unwrap_or("read").to_owned();
    let original = std::fs::read_to_string(f.log()).unwrap();
    std::fs::write(f.log(), original.replacen("the checking engineer", "the CHECKING engineer", 1)).unwrap();
    assert!(reason(0).contains("do not match their recorded digest"), "{}", reason(0));
    assert!(reason(1).contains("not whole at or before"), "{}", reason(1));
    let view = Fixture::view(&f.host, "thread");
    assert!(view["points"][0]["run"].is_null(), "nothing of an unsound record is shown");
    assert!(Fixture::reasons(&view).contains("the terms of point"), "every failed join reaches the reading: {view}");
    let cut = original.trim_end_matches('\n');
    std::fs::write(f.log(), &cut[..cut.len() - 40]).unwrap();
    assert_eq!(reason(0), "read");
    assert!(reason(1).contains("no record with this point's reference"), "{}", reason(1));
    assert!(Fixture::reasons(&Fixture::view(&f.host, "thread")).contains("ends with an unfinished line"));
    let third = f.place("3", "thread", "call-3", &full_terms());
    assert_eq!(third["state"], "recorded", "{third}");
    assert_eq!(reason(2), "read", "a fragment set aside does not block later records");
    let now = std::fs::read_to_string(f.log()).unwrap();
    let first_id = f.records()[0]["recordId"].as_str().unwrap().to_owned();
    let third_id = f.records().last().unwrap()["recordId"].as_str().unwrap().to_owned();
    std::fs::write(f.log(), now.replacen(&third_id, &first_id, 1)).unwrap();
    assert!(reason(0).contains("record identity more than once"), "{}", reason(0));
    let broken: Vec<&str> = now.lines().collect();
    let broken = format!("{}\nnot a record\n{}\n", broken[0], broken[1..].join("\n"));
    std::fs::write(f.log(), &broken).unwrap();
    let refused = f.place("4", "thread", "call-4", &full_terms());
    assert_eq!(refused["state"], "not recorded", "{refused}");
    assert!(refused["reason"].as_str().unwrap().starts_with("The App could not read this project's points log whole ("), "{refused}");
    assert_eq!(std::fs::read_to_string(f.log()).unwrap(), broken, "nothing written");
    std::fs::write(f.log(), &now).unwrap();
    std::fs::remove_file(f.log()).unwrap();
    assert!(reason(0).contains("points log was not found") || reason(0).contains("could not read"), "{}", reason(0));
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], false);
    assert_eq!(view["points"].as_array().unwrap().len(), 3, "still recorded, terms not read");
}

/// Finding 5: a record identity held again in another act log of the same
/// project is not sound: the store's project-wide index is consulted.
#[test]
fn a_record_identity_held_again_elsewhere_in_the_project_is_not_sound() {
    let f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    let line = std::fs::read_to_string(f.log()).unwrap();
    let elsewhere = f.log().parent().unwrap().join(crate::storage::log_rel(None, "app-writer:copy").rsplit('/').next().unwrap());
    std::fs::write(&elsewhere, &line).unwrap();
    // The recorder's next reading of the project (here, a placement in
    // another conversation) consults the project-wide index; the store's
    // writer itself refuses to append while an identity is held twice.
    let refused = f.place("2", "other", "call-2", &small(2));
    assert_eq!(refused["state"], "not recorded", "{refused}");
    assert!(refused["reason"].as_str().unwrap().starts_with("The App's records store did not take the point ("), "{refused}");
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"][0]["terms"]["state"], "not read", "{view}");
    assert!(view["points"][0]["terms"]["reason"].as_str().unwrap().contains("more than once in this project"), "{view}");
    assert_eq!(view["reading"]["whole"], false);
}

/// DEL-04-03 REQ-012 through the host, and what the store's line reader does
/// first: only the version string changed reads as a newer minor version (or
/// refuses an unknown major one); a newer entry with a field the store's
/// schema does not know is refused by the store's line reader, so the point
/// shows its terms not read and the reading is not whole.
#[test]
fn the_host_reading_shows_what_the_version_rules_observe() {
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
    std::fs::write(f.log(), original.replacen("\"formatVersion\":\"0.1\"", "\"formatVersion\":\"0.2\",\"later\":true", 1)).unwrap();
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"][0]["terms"]["state"], "not read", "{view}");
    assert_eq!(view["reading"]["whole"], false);
}

/// Finding 4: the conversation's records binding is the store's project
/// identity, kept before its first record. With an actual new identity at the
/// same folder, the conversation's points read as kept elsewhere, a placement
/// is refused, and a mark of uncertainty about the earlier records is not
/// cleared by a reading of the new ones.
#[test]
fn a_new_identity_at_the_same_folder_is_never_read_or_written_as_the_conversations_records() {
    let mut f = Fixture::new();
    f.place("1", "thread", "call-1", &full_terms());
    f.hooks().points.hooks.append = Some(Box::new(|log, body, id| {
        crate::records::append_reserved(log, points::KIND, &crate::records::APP_WRITER, body, id, None, None, crate::records::RecordSet::Complete, crate::schema_validation::bundled())?;
        let bytes = std::fs::read(log).unwrap();
        std::fs::write(log, &bytes[..bytes.len() - 1]).unwrap();
        Err("injected".into())
    }));
    assert_eq!(f.place("2", "thread", "call-2", &full_terms())["state"], "not established");
    let before = crate::records_store::attach(&f.project, false).unwrap().project.unwrap();
    crate::records_store::new_identity(&f.project).unwrap();
    let after = crate::records_store::attach(&f.project, false).unwrap().project.unwrap();
    assert_ne!(before, after);
    let refused = f.place("3", "thread", "call-3", &full_terms());
    assert_eq!(refused["reason"], "This conversation's points are kept in other records than the records this project folder belongs to now, so the point could not be kept; no point was placed.");
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["reading"]["whole"], false, "{view}");
    // The new identity has no records yet: the store reads this folder's
    // records in place, so none of the conversation's points are read from it.
    assert_eq!(view["points"][0]["terms"]["state"], "not read", "{view}");
    assert!(Fixture::reasons(&view).contains("read in place"), "{view}");
    assert!(Fixture::reasons(&view).contains("the write reported injected"), "the uncertainty about the earlier records stands: {view}");
    f.relaunch();
    let refused = f.place("4", "thread", "call-4", &full_terms());
    assert_eq!(refused["state"], "not recorded");
    assert!(refused["reason"].as_str().unwrap().contains("other records"), "{refused}");
    assert_eq!(Fixture::view(&f.host, "thread")["points"][0]["terms"]["state"], "not read");
}

/// Finding 7: publication against the generation's closure. A generation
/// closed before the append writes nothing; one closed after the record was
/// written leaves the record with its pointer and the unsent receipt stated.
#[test]
fn a_generation_closing_while_the_recorder_works_leaves_nothing_or_the_record_its_pointer_and_a_stated_outcome() {
    let f = Fixture::new();
    let mut pipe = reply_pipe(&f.host);
    let host = Arc::clone(&f.host);
    f.hooks().points.hooks.before_append = Some(Box::new(move || { let mut i = host.inner.0.lock().unwrap(); Host::close_generation(&mut i); }));
    f.host.on_line(&f.frame("1", "thread", "call-1", &full_terms()), &f.g);
    f.drain();
    assert_eq!(text(f.receipts().last().unwrap())["reason"], "This Codex session ended before the point could be recorded; no point was placed.");
    assert!(f.records().is_empty() && f.placed("thread").is_empty());
    assert!(written(&mut pipe).is_empty(), "no reply on a closed generation");

    let f = Fixture::new();
    let mut pipe = reply_pipe(&f.host);
    let host = Arc::clone(&f.host);
    f.hooks().points.hooks.append = Some(Box::new(move |log, body, id| {
        let entry = crate::records::append_reserved(log, points::KIND, &crate::records::APP_WRITER, body, id, None, None, crate::records::RecordSet::Complete, crate::schema_validation::bundled());
        let mut i = host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
        entry
    }));
    f.host.on_line(&f.frame("1", "thread", "call-1", &full_terms()), &f.g);
    f.drain();
    assert_eq!(text(f.receipts().last().unwrap())["state"], "recorded");
    assert_eq!(f.records().len(), 1);
    assert_eq!(f.placed("thread").len(), 1, "the pointer is saved though the generation closed");
    assert!(written(&mut pipe).is_empty());
    assert!(f.host.snapshot()["journal"].as_array().unwrap().iter().any(|j| j["class"] == "point-call-not-answered"));
    let unsent = f.hooks().points.unsent.clone();
    assert_eq!(unsent.len(), 1);
    assert_eq!(unsent[0].1, f.records()[0]["body"]["point"].as_str().unwrap());
}

/// Finding 11: a project closed after the call was admitted refuses the
/// placement before anything is written.
#[test]
fn a_project_closed_after_admission_refuses_before_anything_is_written() {
    let f = Fixture::new();
    f.place("0", "thread", "call-0", &small(0));
    let bytes = std::fs::read(f.log()).unwrap();
    let project = f.project.clone();
    f.hooks().points.hooks.on_admitted = Some(Box::new(move || {
        let actor = crate::act_control::person(Some("Invented fixture person"), Some("invented-fixture-account"));
        let observed = json!({"fixture":"native context test double; no actual human act"});
        crate::records_retention::prepare(&project, "close", None, &actor, &observed).and_then(|p| crate::records_retention::apply(p, &actor, &observed)).unwrap();
    }));
    let receipt = f.place("1", "thread", "call-1", &full_terms());
    assert_eq!(receipt["state"], "not recorded", "{receipt}");
    assert!(receipt["reason"].as_str().unwrap().starts_with("The App's records store did not take the point"), "{receipt}");
    assert_eq!(std::fs::read(f.log()).unwrap(), bytes);
    assert_eq!(f.placed("thread").len(), 1);
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
/// to any record; and the export the disposal relied on, imported as a
/// package into another store at the same folder, is never shown in this
/// App's voice (finding 9).
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

    // The export the disposal relied on, imported as a package into another
    // store at the same folder, read by the original Host and ledger.
    let destination = f.root.join("destination-store");
    let set = move || crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: destination.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    set();
    f.host.on_points_worker(set.clone());
    let plan = crate::records_store::package::prepare(&f.project, &current, &actor, &observed).unwrap();
    assert_eq!(crate::records_store::package::apply(plan, &actor, &observed).unwrap()["state"], "package imported");
    let imported = crate::records_store::project_dir(&f.root.join("destination-store"), &project).join(&rel);
    assert_eq!(std::fs::read(&imported).unwrap(), bytes);
    let reading = points::LogReading::read(&imported).unwrap();
    assert_eq!(reading.lines.len(), 1);
    assert!(reading.soundness(0).is_ok(), "the log alone holds a sound entry");
    let view = Fixture::view(&f.host, "thread");
    assert_eq!(view["points"][0]["terms"]["state"], "not read", "{view}");
    assert_eq!(view["points"][0]["terms"]["reason"], points::IMPORTED, "{view}");
    assert!(view["points"][0]["observed"].is_null(), "nothing of it in the App's voice");
}
