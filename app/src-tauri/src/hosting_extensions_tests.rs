//! DEL-01-05: plugins and connected apps are read for display after the reply that names a
//! conversation's thread, with that thread's id, off the request's path; the home's base reading is
//! shown only as the home's base; nothing is refused or held back by a reading.
use super::*;
use super::extensions::*;
use std::io::{BufRead, BufReader};
use std::time::Instant;

fn g() -> Value { json!({"appSession":"extensions-session","home":"extensions-home","spawnCounter":1}) }
fn g2() -> Value { json!({"appSession":"extensions-session","home":"extensions-home","spawnCounter":2}) }
fn entry(name: &str, enabled: bool) -> Value { json!({"name":name,"enabled":enabled,"defaultEnabled":false,"stage":"stable"}) }
fn off() -> Vec<Value> { vec![entry("plugins", false), entry("apps", false), entry("memories", true)] }
fn on() -> Vec<Value> { vec![entry("plugins", true), entry("apps", true)] }
fn origin(layer: &str) -> Value { json!({"name":{"type":layer},"version":"invented-version"}) }
fn reply_to(host: &Host, source: &SourceRequest, result: Value) {
    host.on_line(&serde_json::to_vec(&json!({"id": source.request_id(), "result": result})).unwrap(), source.generation());
}
/// The thread a conversation request's reply names.
fn thread_of(frame: &Value) -> String {
    match frame["method"].as_str() { Some("thread/start") => "started".into(), Some("thread/fork") => "forked".into(), _ => frame["params"]["threadId"].as_str().unwrap_or("saved").into() }
}
fn conversation_reply(frame: &Value) -> Value {
    json!({"id":frame["id"],"result":{"thread":{"id":thread_of(frame),"status":"idle"},"model":"m","modelProvider":"p","cwd":"/invented/work"}})
}

/// One answer to the reading.
#[derive(Clone)]
enum Answer { Entries(Vec<Value>), Error, Silent, Endless, Result(Value), BaseAndThread(Vec<Value>, Vec<Value>) }

/// A ready Host whose readings are on and whose input is an echo double: the reader thread keeps
/// every frame written, in the order it reached Codex's input, and answers a conversation request
/// as Codex would; the hook answers the reading with `answer`. `events` is the order on the wire:
/// each frame received, and each conversation reply as it is given.
struct Run { host: Arc<Host>, frames: Arc<Mutex<Vec<Value>>>, events: Arc<Mutex<Vec<String>>>, child: std::process::Child, reader: Option<std::thread::JoinHandle<()>> }
impl Run {
    fn new(answer: Answer) -> Self {
        let host = Arc::new(Host::new());
        { let mut i = host.inner.0.lock().unwrap(); i.generation = g(); i.journal.begin_generation(g()); i.state = "ready".into(); i.supplier_standing = Some("unverified-development".into()); i.feature_read_wait = Some(Duration::from_millis(300)); }
        host.feature_readings_for_test();
        let pages = Arc::new(Mutex::new(0usize));
        *host.feature_read_reply.lock().unwrap() = Some(Box::new(move |host, source| {
            let result = match &answer {
                Answer::Entries(entries) => json!({"data": entries, "nextCursor": null}),
                Answer::Error => { host.on_line(&serde_json::to_vec(&json!({"id": source.request_id(), "error": {"code": -32603, "message": "invented failure"}})).unwrap(), source.generation()); return; }
                Answer::Silent => return,
                Answer::Endless => { let mut n = pages.lock().unwrap(); *n += 1; json!({"data": [], "nextCursor": format!("page-{n}")}) }
                Answer::Result(result) => result.clone(),
                // Codex's base configuration differs from the thread's project's.
                Answer::BaseAndThread(base, thread) => json!({"data": if source.frame["params"].get("threadId").is_some() { thread } else { base }, "nextCursor": null}),
            };
            reply_to(host, source, result);
        }));
        let mut child = std::process::Command::new("/bin/cat").env_clear().stdin(std::process::Stdio::piped()).stdout(std::process::Stdio::piped()).stderr(std::process::Stdio::null()).spawn().unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let stdout = child.stdout.take().unwrap();
        let (frames, events) = (Arc::new(Mutex::new(Vec::new())), Arc::new(Mutex::new(Vec::new())));
        let (me, seen, order) = (Arc::clone(&host), Arc::clone(&frames), Arc::clone(&events));
        let reader = std::thread::spawn(move || {
            for line in BufReader::new(stdout).lines() {
                let Ok(line) = line else { break };
                let frame: Value = serde_json::from_str(&line).unwrap();
                let method = frame["method"].as_str().unwrap_or("").to_owned();
                seen.lock().unwrap().push(frame.clone());
                order.lock().unwrap().push(format!("in {method}"));
                if extensions::loads_conversation(&method) {
                    order.lock().unwrap().push(format!("reply {method}"));
                    me.on_line(&serde_json::to_vec(&conversation_reply(&frame)).unwrap(), &g());
                }
            }
        });
        Run { host, frames, events, child, reader: Some(reader) }
    }
    fn start(&self) -> Result<Value, String> { self.host.thread_start_selected("/invented/work", "m", "p") }
    fn continue_with(&self, method: &str) -> Result<Value, String> {
        self.host.request_inner_scoped(method, json!({"threadId":"saved"}), json!({"kind":"person-directed"}), Duration::from_secs(1), false, Some(&g()))
    }
    /// The conversation's reading once it is no longer being read.
    fn read(&self, thread: &str) -> Value { settled(|| self.host.extensions_record_for_test(thread)) }
    fn base(&self) -> Value { settled(|| Some(self.host.snapshot()["extensionsBase"].clone()).filter(|b| !b.is_null())) }
    /// A requirements reading of this generation answered with `frame` (`id` filled in).
    fn requirements_reply(&self, frame: Value) {
        let source = self.host.request_begin_scoped("configRequirements/read", json!({}), json!({"kind":"person-directed"}), false, Some(&g())).unwrap();
        let mut frame = frame; frame["id"] = source.request_id().clone();
        self.host.on_line(&serde_json::to_vec(&frame).unwrap(), &g());
        let _ = self.host.source_request_wait(&source, Duration::from_millis(200));
    }
    fn events(&self) -> Vec<String> { self.events.lock().unwrap().clone() }
    fn feature_frames(&self) -> Vec<Value> { self.frames.lock().unwrap().iter().filter(|f| f["method"] == FEATURE_LIST).cloned().collect() }
    fn finish(mut self) -> Value {
        *self.host.stdin.lock().unwrap() = None;
        self.child.wait().unwrap();
        self.reader.take().unwrap().join().unwrap();
        self.host.snapshot()
    }
}
fn settled(look: impl Fn() -> Option<Value>) -> Value {
    let deadline = Instant::now() + Duration::from_secs(3);
    loop {
        if let Some(record) = look().filter(|r| r["plugins"]["notReadBecause"] != "reading") { return record; }
        assert!(Instant::now() < deadline, "the reading did not finish: {:?}", look());
        std::thread::sleep(Duration::from_millis(5));
    }
}

/// After the reply, never before the request: start, resume and fork, each with its thread's id.
#[test]
fn each_conversation_request_is_read_for_after_its_reply_with_its_thread() {
    for method in ["thread/start", "thread/resume", "thread/fork"] {
        let run = Run::new(Answer::Entries(vec![entry("plugins", true), entry("apps", false)]));
        let reply = if method == "thread/start" { run.start() } else { run.continue_with(method) };
        assert!(reply.is_ok(), "{method}: {reply:?}");
        let thread = match method { "thread/start" => "started", "thread/fork" => "forked", _ => "saved" };
        let record = run.read(thread);
        assert_eq!(run.events(), [format!("in {method}"), format!("reply {method}"), format!("in {FEATURE_LIST}")], "{method}: the reading reaches Codex only after the reply");
        assert_eq!(run.feature_frames()[0]["params"], json!({"threadId": thread}), "{method}: the thread's id is sent");
        assert_eq!((&record["generation"], record["request"].as_str(), record["threadId"].as_str()), (&g(), Some(method), Some(thread)));
        assert_eq!((record["plugins"]["state"].as_str(), record["apps"]["state"].as_str()), (Some("on"), Some("off")), "{method}");
        for feature in ["plugins", "apps"] {
            assert_eq!((record[feature]["source"].as_str(), &record[feature]["notReadBecause"], &record[feature]["requirementsReadAt"]), (Some("not-established"), &Value::Null, &Value::Null), "{method}: no evidence of where it comes from");
            assert!(record[feature]["readAt"].as_str().is_some_and(|t| t.ends_with('Z')));
        }
        assert_eq!(record["evidence"], json!({"origins":"none","requirements":"none"}));
        let status = run.finish();
        if method == "thread/start" {
            assert_eq!(status["threads"][0]["extensions"], record, "shown on the conversation's own row");
            let read = status["clientRequests"].as_array().unwrap().iter().find(|r| r["method"] == FEATURE_LIST).unwrap().clone();
            assert_eq!((&read["initiator"], &read["generation"]), (&json!({"kind":"app-rule","name":"feature-state-read"}), &g()));
        }
        assert!(status["extensionsBase"].is_null(), "no base reading was made");
    }
}

#[test]
fn each_feature_reads_on_off_or_not_read_and_nothing_is_refused() {
    let cases: Vec<(&str, Answer, (&str, Option<&str>), (&str, Option<&str>))> = vec![
        ("plugins on", Answer::Entries(vec![entry("plugins", true), entry("apps", false)]), ("on", None), ("off", None)),
        ("apps on", Answer::Entries(vec![entry("plugins", false), entry("apps", true)]), ("off", None), ("on", None)),
        ("apps missing", Answer::Entries(vec![entry("plugins", true)]), ("on", None), ("not-read", Some("missing"))),
        ("plugins duplicated", Answer::Entries(vec![entry("plugins", false), entry("plugins", false), entry("apps", false)]), ("not-read", Some("duplicate")), ("off", None)),
        ("malformed apps entry", Answer::Entries(vec![entry("plugins", false), json!({"name":"apps","enabled":"false","defaultEnabled":false,"stage":"stable"})]), ("off", None), ("not-read", Some("malformed-entry"))),
        ("unknown stage", Answer::Entries(vec![json!({"name":"plugins","enabled":false,"defaultEnabled":false,"stage":"invented"}), entry("apps", true)]), ("not-read", Some("malformed-entry")), ("on", None)),
        ("unnamed entry", Answer::Entries(vec![entry("plugins", false), entry("apps", false), json!({"enabled":true})]), ("not-read", Some("unnamed-entry")), ("not-read", Some("unnamed-entry"))),
        ("error reply", Answer::Error, ("not-read", Some("error-reply")), ("not-read", Some("error-reply"))),
        ("no reply", Answer::Silent, ("not-read", Some("not-answered")), ("not-read", Some("not-answered"))),
        ("endless pages", Answer::Endless, ("not-read", Some("page-limit")), ("not-read", Some("page-limit"))),
        ("data not a list", Answer::Result(json!({"data":{"plugins":false},"nextCursor":null})), ("not-read", Some("malformed-reply")), ("not-read", Some("malformed-reply"))),
        ("cursor not text", Answer::Result(json!({"data":off(),"nextCursor":7})), ("not-read", Some("malformed-reply")), ("not-read", Some("malformed-reply"))),
    ];
    for (case, answer, plugins, apps) in cases {
        let endless = matches!(answer, Answer::Endless);
        let run = Run::new(answer);
        assert!(run.start().is_ok(), "{case}: the start is sent and answered whatever the reading");
        let record = run.read("started");
        let pages = run.feature_frames();
        assert_eq!(pages.len(), if endless { FEATURE_PAGE_LIMIT } else { 1 }, "{case}: the page bound holds");
        assert!(pages.iter().all(|p| p["params"]["threadId"] == "started"), "{case}: every page names the thread");
        for (feature, (state, because)) in [("plugins", plugins), ("apps", apps)] {
            assert_eq!((record[feature]["state"].as_str(), record[feature]["notReadBecause"].as_str()), (Some(state), because), "{case}: {feature}");
        }
        let status = run.finish();
        assert_eq!(status["clientRequests"].as_array().unwrap().iter().filter(|r| r["method"] == "thread/start").count(), 1, "{case}");
    }
}

#[test]
fn pages_carry_the_thread_and_the_cursor_and_are_read_together() {
    let run = Run::new(Answer::Silent);
    *run.host.feature_read_reply.lock().unwrap() = Some(Box::new(|host, source| {
        let result = if source.frame["params"] == json!({"threadId":"started"}) { json!({"data":[entry("plugins", true)],"nextCursor":"second"}) }
            else { assert_eq!(source.frame["params"], json!({"threadId":"started","cursor":"second"})); json!({"data":[entry("apps", false)],"nextCursor":null}) };
        reply_to(host, source, result);
    }));
    run.start().unwrap();
    let record = run.read("started");
    assert_eq!(run.feature_frames().len(), 2);
    assert_eq!((record["plugins"]["state"].as_str(), record["apps"]["state"].as_str()), (Some("on"), Some("off")));
    run.finish();
}

/// The start is answered while the reading has not even begun to wait: the reading is no part of
/// it. A reading not answered is not read at its one deadline.
#[test]
fn an_unanswered_reading_holds_nothing_and_is_not_read_at_its_deadline() {
    let run = Run::new(Answer::Silent);
    let began = Instant::now();
    assert!(run.start().is_ok());
    assert_eq!(run.host.extensions_record_for_test("started").unwrap()["plugins"]["notReadBecause"], "reading", "the start returned while the reading was still under way");
    let record = run.read("started");
    let took = began.elapsed();
    assert!(took >= Duration::from_millis(290) && took < Duration::from_millis(1200), "{took:?}");
    assert_eq!((record["apps"]["state"].as_str(), record["apps"]["notReadBecause"].as_str()), (Some("not-read"), Some("not-answered")));
    run.finish();
}

/// A base reading of plugins off and a conversation whose project turns them on: the conversation
/// shows on, and off is shown only as the home's base, before project settings.
#[test]
fn a_differing_base_shows_only_as_the_homes_base() {
    let run = Run::new(Answer::BaseAndThread(off(), on()));
    run.host.extensions_after_ready(&g());
    let base = run.base();
    assert_eq!((base["plugins"]["state"].as_str(), base["scope"].as_str()), (Some("off"), Some(BASE_SCOPE)));
    assert!(base.get("threadId").is_none() && base["request"].is_null());
    run.start().unwrap();
    let conversation = run.read("started");
    let frames = run.feature_frames();
    assert_eq!((frames[0]["params"].clone(), frames[1]["params"].clone()), (json!({}), json!({"threadId":"started"})));
    let status = run.finish();
    let row = &status["threads"][0]["extensions"];
    assert_eq!((row["plugins"]["state"].as_str(), row["apps"]["state"].as_str()), (Some("on"), Some("on")), "the conversation's own state");
    assert_eq!(row, &conversation);
    assert!(row.get("scope").is_none(), "a conversation's reading is not the base");
    assert_eq!((status["extensionsBase"]["plugins"]["state"].as_str(), status["extensionsBase"]["scope"].as_str()), (Some("off"), Some(BASE_SCOPE)));
}

/// A pipe that no one reads, filled; the open reader end is returned.
fn full_pipe(host: &Host) -> (std::fs::File, i32) {
    use std::os::fd::{FromRawFd, OwnedFd};
    let mut fds = [0; 2];
    assert_eq!(unsafe { libc::pipe(fds.as_mut_ptr()) }, 0);
    let read = unsafe { std::fs::File::from_raw_fd(fds[0]) };
    let write = unsafe { OwnedFd::from_raw_fd(fds[1]) };
    fill(fds[1]);
    *host.stdin.lock().unwrap() = Some(ChildStdin::from(write));
    (read, fds[1])
}
/// Fills the pipe whose writer end is `fd`, and leaves it blocking as it was.
fn fill(fd: i32) {
    let flags = unsafe { libc::fcntl(fd, libc::F_GETFL) };
    assert!(flags >= 0);
    assert_eq!(unsafe { libc::fcntl(fd, libc::F_SETFL, flags | libc::O_NONBLOCK) }, 0);
    let filler = [b'\n'; 4096];
    loop {
        let n = unsafe { libc::write(fd, filler.as_ptr().cast(), filler.len()) };
        if n < 0 { assert_eq!(std::io::Error::last_os_error().kind(), std::io::ErrorKind::WouldBlock); break; }
    }
    assert_eq!(unsafe { libc::fcntl(fd, libc::F_SETFL, flags) }, 0);
}
fn pending(host: &Host, method: &str) -> Vec<bool> {
    host.inner.0.lock().unwrap().source_requests.values().filter(|e| e.request.frame["method"] == method).map(|e| e.write_attempt_in_progress).collect()
}

/// Review 356, F1, ported: with Codex's input full, the start is registered and being written at
/// once; no reading stands before it. The reading follows its reply once Codex reads again.
#[test]
fn with_codex_input_full_the_start_is_not_held_behind_a_reading() {
    let run = Run::new(Answer::Entries(on()));
    let (read, _) = full_pipe(&run.host);
    let host = Arc::clone(&run.host);
    let (done_tx, done) = std::sync::mpsc::channel();
    let worker = std::thread::spawn(move || { done_tx.send(host.thread_start_selected("/invented/work", "m", "p")).unwrap(); });
    std::thread::sleep(Duration::from_millis(400));
    assert!(matches!(done.try_recv(), Err(std::sync::mpsc::TryRecvError::Empty)), "the start waits on Codex's input, as any frame would");
    assert_eq!(pending(&run.host, "thread/start"), [true], "the start itself is registered and its write is under way");
    assert!(pending(&run.host, FEATURE_LIST).is_empty(), "no reading was made before it");
    let host = Arc::clone(&run.host);
    let order = Arc::new(Mutex::new(Vec::new()));
    let seen = Arc::clone(&order);
    let drainer = std::thread::spawn(move || {
        for line in BufReader::new(read).lines() {
            let line = line.unwrap();
            if line.is_empty() { continue; }
            let frame: Value = serde_json::from_str(&line).unwrap();
            seen.lock().unwrap().push(frame["method"].as_str().unwrap_or("").to_owned());
            if frame["method"] == "thread/start" { host.on_line(&serde_json::to_vec(&conversation_reply(&frame)).unwrap(), &g()); }
        }
    });
    assert!(done.recv_timeout(Duration::from_secs(3)).unwrap().is_ok());
    worker.join().unwrap();
    let record = run.read("started");
    assert_eq!(record["plugins"]["state"], "on");
    *run.host.stdin.lock().unwrap() = None;
    drainer.join().unwrap();
    assert_eq!(*order.lock().unwrap(), ["thread/start", FEATURE_LIST]);
    run.finish();
}

/// The request for each conversation method, as a test sends it.
fn conversation_params(method: &str) -> Value {
    if method == "thread/start" { json!({"model":"m","modelProvider":"p"}) } else { json!({"threadId":"saved"}) }
}
fn feature_attempts(host: &Host) -> Vec<Option<u64>> {
    host.inner.0.lock().unwrap().source_requests.values().filter(|e| e.request.frame["method"] == FEATURE_LIST).map(|e| e.attempt_position).collect()
}

/// Review 356, R1 (base form): the home's base reading meets Codex's input full. It writes
/// nothing, releases the frame writer at once and is not read, not sent; a start, resume or fork
/// that comes after it is not held by it and goes to its own write.
#[test]
fn a_base_reading_that_meets_codex_input_full_holds_no_later_request() {
    for method in ["thread/start", "thread/resume", "thread/fork"] {
        let run = Run::new(Answer::Silent);
        let (read, _) = full_pipe(&run.host);
        run.host.extensions_after_ready(&g());
        let base = run.base();
        assert_eq!((base["plugins"]["state"].as_str(), base["plugins"]["notReadBecause"].as_str()), (Some("not-read"), Some("not-sent")));
        assert_eq!(feature_attempts(&run.host), [None], "the reading made no write attempt");
        assert!(run.host.frame_write.try_lock().is_ok(), "the frame writer is free");
        let host = Arc::clone(&run.host);
        let (done_tx, done) = std::sync::mpsc::channel();
        let worker = std::thread::spawn(move || { done_tx.send(host.request_begin_scoped(method, conversation_params(method), json!({"kind":"person-directed"}), false, Some(&g())).map(|_| ())).unwrap(); });
        let deadline = Instant::now() + Duration::from_secs(2);
        while pending(&run.host, method) != [true] { assert!(Instant::now() < deadline, "{method} did not reach its own write"); std::thread::sleep(Duration::from_millis(2)); }
        drop(read);
        let _ = done.recv_timeout(Duration::from_secs(3)).unwrap();
        worker.join().unwrap();
        run.finish();
    }
}

/// Review 356, R1 (thread form): the reading made after a start's reply meets Codex's input full
/// and is not read, not sent, with the writer released; the next start, resume or fork goes to its
/// own write and completes once Codex reads again. The reading's late arrival changes nothing.
#[test]
fn a_conversation_reading_that_meets_codex_input_full_holds_no_next_request() {
    use std::os::fd::{FromRawFd, OwnedFd};
    for method in ["thread/start", "thread/resume", "thread/fork"] {
        let run = Run::new(Answer::Silent);
        let mut fds = [0; 2];
        assert_eq!(unsafe { libc::pipe(fds.as_mut_ptr()) }, 0);
        let read = unsafe { std::fs::File::from_raw_fd(fds[0]) };
        *run.host.stdin.lock().unwrap() = Some(ChildStdin::from(unsafe { OwnedFd::from_raw_fd(fds[1]) }));
        let (writer, host) = (fds[1], Arc::clone(&run.host));
        let (drain_tx, drain) = std::sync::mpsc::channel::<()>();
        let seen = Arc::new(Mutex::new(Vec::new()));
        let order = Arc::clone(&seen);
        // Codex's side: it reads the start, stops reading with its input full and answers the
        // start; when told, it reads again and answers what it reads.
        let codex = std::thread::spawn(move || {
            let mut lines = BufReader::new(read).lines();
            let first: Value = serde_json::from_str(&lines.next().unwrap().unwrap()).unwrap();
            assert_eq!(first["method"], "thread/start");
            fill(writer);
            host.on_line(&serde_json::to_vec(&conversation_reply(&first)).unwrap(), &g());
            drain.recv().unwrap();
            for line in lines {
                let Ok(line) = line else { break };
                if line.trim().is_empty() { continue; }
                let frame: Value = serde_json::from_str(&line).unwrap();
                order.lock().unwrap().push(frame["method"].as_str().unwrap_or("").to_owned());
                if extensions::loads_conversation(frame["method"].as_str().unwrap_or("")) { host.on_line(&serde_json::to_vec(&conversation_reply(&frame)).unwrap(), &g()); }
            }
        });
        assert!(run.start().is_ok());
        let record = run.read("started");
        assert_eq!((record["plugins"]["state"].as_str(), record["plugins"]["notReadBecause"].as_str()), (Some("not-read"), Some("not-sent")));
        assert_eq!(feature_attempts(&run.host), [None], "the reading made no write attempt");
        assert!(run.host.frame_write.try_lock().is_ok(), "the frame writer is free");
        let host = Arc::clone(&run.host);
        let (done_tx, done) = std::sync::mpsc::channel();
        let worker = std::thread::spawn(move || done_tx.send(host.request_inner_scoped(method, conversation_params(method), json!({"kind":"person-directed"}), Duration::from_secs(2), false, Some(&g()))).unwrap());
        let deadline = Instant::now() + Duration::from_secs(2);
        while !pending(&run.host, method).contains(&true) { assert!(Instant::now() < deadline, "{method} did not reach its own write"); std::thread::sleep(Duration::from_millis(2)); }
        drain_tx.send(()).unwrap();
        assert!(done.recv_timeout(Duration::from_secs(3)).unwrap().is_ok(), "{method} completes once Codex reads again");
        worker.join().unwrap();
        let thread = match method { "thread/start" => "started", "thread/fork" => "forked", _ => "saved" };
        run.read(thread);
        *run.host.stdin.lock().unwrap() = None;
        codex.join().unwrap();
        assert_eq!(seen.lock().unwrap().first().map(String::as_str), Some(method), "the next request was the first frame Codex read after its input was full");
        // A second start names the same thread, and its own reading replaces the first.
        if method != "thread/start" { assert_eq!(run.host.extensions_record_for_test("started").unwrap(), record, "the first reading stays not sent"); }
        run.finish();
    }
}

/// A page longer than one atomic write to Codex's input is not written: the writer is not taken
/// into a write that could be split or wait.
#[test]
fn a_frame_longer_than_one_atomic_write_is_not_written() {
    let (read, write) = std::os::unix::net::UnixStream::pair().unwrap();
    let file = std::fs::File::from(std::os::fd::OwnedFd::from(write));
    assert_eq!(frame_fits_now(&file, libc::PIPE_BUF), Ok(()));
    assert_eq!(frame_fits_now(&file, libc::PIPE_BUF + 1), Err(FRAME_TOO_LONG.into()));
    drop(read);
    let run = Run::new(Answer::Entries(on()));
    let long = "c".repeat(libc::PIPE_BUF);
    *run.host.feature_read_reply.lock().unwrap() = Some(Box::new(move |host, source| reply_to(host, source, json!({"data": on(), "nextCursor": long}))));
    run.host.extensions_after_ready(&g());
    let base = run.base();
    assert_eq!(base["plugins"]["notReadBecause"], "not-sent", "the second page, carrying the long cursor, was not written");
    assert_eq!(feature_attempts(&run.host).iter().filter(|a| a.is_some()).count(), 1, "only the first page was written");
    run.finish();
}

/// Review 356, F3, ported: the wait for the frame writer is counted in the one deadline, not again
/// after it.
#[test]
fn the_deadline_is_counted_once_across_the_writer_wait() {
    let run = Run::new(Answer::Silent);
    run.host.hold_frame_writer_for_test(Duration::from_millis(230));
    let began = Instant::now();
    let outcome = run.host.feature_list_read(&g(), Some("started"), began + Duration::from_millis(300));
    let took = began.elapsed();
    assert_eq!(outcome, Err("not-answered"));
    assert!(took >= Duration::from_millis(290) && took < Duration::from_millis(480), "the reply waited only for what remained: {took:?}");
    assert_eq!(pending(&run.host, FEATURE_LIST), [false], "written once the writer was free");
    run.finish();
}

/// A reading waiting for the frame writer is not written ahead of another request waiting for it
/// too, whether that request waits on the writer's lock (a conversation request) or asks for it
/// again and again (a requirements reading): the request goes first.
#[test]
fn a_waiting_reading_is_not_written_ahead_of_another_waiting_request() {
    for round in 0..8 {
        let run = Run::new(Answer::Entries(off()));
        let (release, released) = std::sync::mpsc::channel::<()>();
        let (held_tx, held) = std::sync::mpsc::channel();
        let holder = Arc::clone(&run.host);
        let holding = std::thread::spawn(move || { let _writer = holder.frame_write.lock().unwrap(); held_tx.send(()).unwrap(); released.recv().unwrap(); });
        held.recv().unwrap();
        let reader = Arc::clone(&run.host);
        let reading = std::thread::spawn(move || reader.feature_list_read(&g(), Some("earlier"), Instant::now() + Duration::from_secs(2)));
        std::thread::sleep(Duration::from_millis(30));
        let requester = Arc::clone(&run.host);
        // A conversation request waits on the writer's lock; a requirements reading asks for it
        // again and again, as the reading itself does.
        let method = if round % 2 == 0 { "thread/resume" } else { "configRequirements/read" };
        let request = std::thread::spawn(move || if method == "thread/resume" {
            requester.request_inner_scoped(method, json!({"threadId":"saved"}), json!({"kind":"person-directed"}), Duration::from_secs(2), false, Some(&g())).map(|_| ())
        } else { requester.account_requirements_read_until(&g(), Instant::now() + Duration::from_secs(2)).map(|_| ()) });
        std::thread::sleep(Duration::from_millis(30));
        release.send(()).unwrap();
        holding.join().unwrap();
        assert!(request.join().unwrap().is_ok());
        assert!(reading.join().unwrap().is_ok());
        let received = || run.events().into_iter().filter(|e| e.starts_with("in ")).take(2).collect::<Vec<String>>();
        let deadline = Instant::now() + Duration::from_secs(2);
        while received().len() < 2 { assert!(Instant::now() < deadline, "round {round}: {:?}", run.events()); std::thread::sleep(Duration::from_millis(5)); }
        let first = received();
        assert_eq!(first, [format!("in {method}"), format!("in {FEATURE_LIST}")], "round {round}");
        run.finish();
    }
}

/// Review 356, F5, ported: closing and replacing the generation drops every reading of it and the
/// base; so does a request refused because its generation was replaced; and a reading finishing
/// after its generation closed changes nothing.
#[test]
fn closing_or_replacing_the_generation_drops_its_readings() {
    let run = Run::new(Answer::Entries(on()));
    run.host.extensions_after_ready(&g());
    run.base();
    run.start().unwrap();
    assert_eq!(run.read("started")["plugins"]["state"], "on");
    {
        let mut i = run.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
        i.generation = g2(); i.journal.begin_generation(g2()); i.state = "ready".into();
    }
    assert!(!run.host.extensions_kept_for_test(), "nothing of the closed generation is kept");
    let status = run.host.snapshot();
    assert!(status["extensionsBase"].is_null());
    assert!(status["threads"].as_array().unwrap().iter().all(|t| t.get("extensions").is_none()));
    run.finish();

    // A replacement without a close seen here, then a request bound to the replaced generation.
    let run = Run::new(Answer::Entries(on()));
    run.host.extensions_after_ready(&g());
    run.base();
    run.start().unwrap();
    run.read("started");
    { let mut i = run.host.inner.0.lock().unwrap(); i.generation = g2(); i.journal.begin_generation(g2()); }
    let refused = run.host.request_inner_scoped("thread/resume", json!({"threadId":"started"}), json!({"kind":"person-directed"}), Duration::from_millis(300), false, Some(&g())).unwrap_err();
    assert!(refused.contains("generation changed before request registration"), "{refused}");
    assert!(!run.host.extensions_kept_for_test(), "the refusal drops the replaced generation's readings");
    run.finish();

    // Review 356, R4: a replacement seen only by status drops the replaced generation's
    // admissions and requirements times too, not only what is shown.
    let run = Run::new(Answer::Entries(on()));
    run.requirements_reply(json!({"result":{"requirements":null}}));
    run.host.extensions_after_ready(&g());
    run.base();
    run.start().unwrap();
    run.read("started");
    let unanswered = run.host.request_begin_scoped("thread/resume", json!({"threadId":"saved"}), json!({"kind":"person-directed"}), false, Some(&g()));
    {
        let mut i = run.host.inner.0.lock().unwrap();
        let key = i.source_requests.iter().find(|(_, e)| e.request.frame["method"] == "thread/resume").map(|(k, _)| k.clone()).unwrap();
        i.extensions_admitted.insert(key, Admitted::default());
        assert!(!i.requirements_read_at.is_empty());
        i.generation = g2(); i.journal.begin_generation(g2());
    }
    let status = run.host.snapshot();
    assert!(status["extensionsBase"].is_null());
    assert!(!run.host.extensions_kept_for_test(), "nothing of the replaced generation is kept");
    drop(unanswered);
    run.finish();

    // A reading of G1 still under way when G1 closes.
    let run = Run::new(Answer::Silent);
    *run.host.feature_read_reply.lock().unwrap() = Some(Box::new(|host, source| {
        { let mut i = host.inner.0.lock().unwrap(); Host::close_generation(&mut i); i.generation = g2(); i.journal.begin_generation(g2()); i.state = "ready".into(); }
        reply_to(host, source, json!({"data": on(), "nextCursor": null}));
    }));
    run.start().unwrap();
    std::thread::sleep(Duration::from_millis(500));
    assert!(run.host.extensions_record_for_test("started").is_none(), "a late reading of a closed generation is not kept");
    run.finish();
}

/// Review 356, F4, ported: pins only from a reply that settled correctly, correlated, as a result
/// with no error, in the native shape; otherwise no pin evidence, so a home, project or default
/// source is not established.
#[test]
fn requirements_count_only_from_a_successful_native_reply() {
    let user = json!({"features.plugins": origin("user")});
    let cases: Vec<(&str, Vec<Value>, Option<Value>)> = vec![
        ("nothing pinned", vec![json!({"result":{"requirements":null}})], Some(json!({}))),
        ("plugins pinned", vec![json!({"result":{"requirements":{"featureRequirements":{"plugins":false}}}})], Some(json!({"plugins":false}))),
        ("result together with an error", vec![json!({"result":{"requirements":null},"error":{"code":-32603,"message":"invented failure"}})], None),
        ("pinned, together with an error", vec![json!({"result":{"requirements":{"featureRequirements":{"plugins":false}}},"error":{"code":-32603,"message":"invented failure"}})], None),
        ("an error", vec![json!({"error":{"code":-32603,"message":"invented failure"}})], None),
        ("requirements not an object", vec![json!({"result":{"requirements":[]}})], None),
        ("no result", vec![json!({"jsonrpc":"2.0"})], None),
        ("a later malformed reply after a good one", vec![json!({"result":{"requirements":null}}), json!({"result":{"requirements":7}})], None),
    ];
    for (case, replies, expected) in cases {
        let run = Run::new(Answer::Entries(off()));
        for reply in replies { run.requirements_reply(reply); }
        let evidence = { let i = run.host.inner.0.lock().unwrap(); Host::requirements_evidence(&i, &g()) };
        assert_eq!(evidence.as_ref().map(|(pins, _)| pins.clone()), expected, "{case}");
        if let Some((_, at)) = &evidence { assert!(at.as_deref().is_some_and(|t| t.ends_with('Z')), "{case}: when it was read"); }
        let pins = evidence.as_ref().map(|(pins, _)| pins);
        let from_home = source(Feature::Plugins, Some(&user), pins);
        match case {
            "nothing pinned" => assert_eq!(from_home, Source::ThisHome),
            "plugins pinned" => assert_eq!(from_home, Source::OutsideApp),
            _ => assert_eq!(from_home, Source::NotEstablished, "{case}"),
        }
        run.start().unwrap();
        let record = run.read("started");
        let (expected_source, expected_evidence) = if case == "plugins pinned" { ("outside-app", "read") } else if expected.is_some() { ("not-established", "read") } else { ("not-established", "none") };
        assert_eq!((record["plugins"]["source"].as_str(), record["evidence"]["requirements"].as_str()), (Some(expected_source), Some(expected_evidence)), "{case}");
        assert_eq!(record["plugins"]["requirementsReadAt"].is_string(), expected.is_some(), "{case}: the requirements reading's time travels with the source");
        run.finish();
    }
}

/// Origins only from the admitting reading made for the folder Codex reports for the thread.
#[test]
fn origins_come_only_from_a_reading_of_the_threads_own_folder() {
    let origins = json!({"features.plugins": origin("user")});
    let admitted = Admitted { cwd: Some("/invented/work".into()), origins: Some(origins.clone()) };
    for (cwd, expected) in [(Some("/invented/work"), (Some(origins.clone()), "admitting-reading-same-folder")), (Some("/invented/other"), (None, "admitting-reading-other-folder")), (None, (None, "admitting-reading-other-folder"))] {
        let found = extensions_origins_for_test(Some(&admitted), cwd);
        assert_eq!((found.0, found.1), expected, "{cwd:?}");
    }
    assert_eq!(extensions_origins_for_test(Some(&Admitted { cwd: None, origins: Some(origins) }), None).1, "admitting-reading-other-folder", "a reading of no named folder is no reading of the thread's");
    assert_eq!(extensions_origins_for_test(None, Some("/invented/work")), (None, "none"));
}

/// Every source from the evidence, and `connectors` prevailing over `apps`.
#[test]
fn each_source_follows_its_evidence() {
    use Feature::{Apps, Plugins};
    let nothing_pinned = json!({});
    let o = |pairs: &[(&str, &str)]| Value::Object(pairs.iter().map(|(k, l)| (k.to_string(), origin(l))).collect());
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "user")])), Some(&json!({"plugins":false}))), Source::OutsideApp);
    assert_eq!(source(Apps, None, Some(&json!({"connectors":true}))), Source::OutsideApp);
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "user")])), Some(&nothing_pinned)), Source::ThisHome);
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "project")])), Some(&nothing_pinned)), Source::Project);
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "user")])), None), Source::NotEstablished, "requirements not read");
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "project")])), None), Source::NotEstablished, "requirements not read");
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "mdm")])), None), Source::OutsideApp, "a managed origin is evidence on its own");
    for managed in ["mdm", "system", "enterpriseManaged", "legacyManagedConfigTomlFromFile", "legacyManagedConfigTomlFromMdm"] {
        assert_eq!(source(Plugins, Some(&o(&[("features.plugins", managed)])), Some(&nothing_pinned)), Source::OutsideApp, "{managed}");
    }
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "packagedDefaults")])), Some(&nothing_pinned)), Source::Default);
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "packagedDefaults")])), None), Source::NotEstablished);
    for unnamed in ["sessionFlags", "invented"] {
        assert_eq!(source(Plugins, Some(&o(&[("features.plugins", unnamed)])), Some(&nothing_pinned)), Source::NotEstablished, "{unnamed}");
    }
    assert_eq!(source(Apps, Some(&o(&[("features.plugins", "user")])), Some(&nothing_pinned)), Source::Default);
    assert_eq!(source(Apps, Some(&o(&[])), None), Source::NotEstablished, "requirements not read");
    assert_eq!(source(Apps, None, Some(&nothing_pinned)), Source::NotEstablished, "origins not read");
    assert_eq!(source(Apps, Some(&o(&[("features.apps", "user"), ("features.connectors", "mdm")])), Some(&nothing_pinned)), Source::OutsideApp);
    assert_eq!(source(Apps, Some(&o(&[("features.apps", "mdm"), ("features.connectors", "user")])), Some(&nothing_pinned)), Source::ThisHome);
    assert_eq!(source(Apps, Some(&o(&[("features.apps", "project")])), Some(&nothing_pinned)), Source::Project);
    assert_eq!(evaluate(&[], Plugins), Observed { state: State::NotRead, not_read_because: Some("missing") });
    assert_ne!(State::NotRead, State::Off);
}

#[test]
fn requirement_pins_keep_only_these_features_as_values() {
    assert_eq!(requirement_pins(&json!({"result":{"requirements":null}})), Some(json!({})));
    assert_eq!(requirement_pins(&json!({"result":{"requirements":{"featureRequirements":null}}})), Some(json!({})));
    assert_eq!(requirement_pins(&json!({"result":{"requirements":{"featureRequirements":{"plugins":false,"other":true}}}})), Some(json!({"plugins":false})));
    assert_eq!(requirement_pins(&json!({"result":{"requirements":{"featureRequirements":{"apps":"on"}}}})), None);
    assert_eq!(requirement_pins(&json!({"result":{"requirements":[]}})), None);
    assert_eq!(requirement_pins(&json!({"error":{"code":1,"message":"m"}})), None);
    assert_eq!(requirement_pins(&json!({"result":{"requirements":null},"error":{"code":1,"message":"m"}})), None, "a result with an error is no answer");
    let raw = json!({"jsonrpc":"2.0","id":1,"result":{"requirements":{"featureRequirements":{"plugins":true,"apps":"x","secret":true}}}});
    let (projected, _) = auth_rpc::project_frame(&raw, Some("configRequirements/read"));
    assert_eq!(projected["result"]["requirements"]["featureRequirements"], json!({"plugins":true,"apps":auth_rpc::REDACTED}));
}

/// The dedicated local home is not read for.
#[test]
fn the_local_home_is_not_read_for() {
    let host = Arc::new(Host::new());
    { let mut i = host.inner.0.lock().unwrap(); i.generation = g(); i.state = "ready".into(); i.local_provider = Some(access_provider::LocalProviderBinding::for_test("extensions-home", "/invented/work")); }
    host.feature_readings_for_test();
    *host.feature_read_reply.lock().unwrap() = Some(Box::new(|_, _| panic!("no reading in the local home")));
    host.extensions_after_ready(&g());
    assert!(host.inner.0.lock().unwrap().extensions_base.is_none());
    // A start reply in the local home begins no reading either.
    let source = host.request_begin_scoped("thread/start", json!({"model":"m","modelProvider":"p"}), json!({"kind":"person-directed"}), false, Some(&g()));
    if let Ok(source) = source {
        let mut i = host.inner.0.lock().unwrap();
        let reply = json!({"id":source.request_id(),"result":{"thread":{"id":"local","status":"idle"},"cwd":"/invented/work"}});
        assert!(Host::extensions_on_reply(&mut i, &source.request_id().to_string(), &g(), &reply, true).is_none());
    }
    assert!(host.snapshot()["extensionsBase"].is_null());
}
