use super::*;
use crate::hosting::{Host, SourceRequest};
use serde_json::json;
use std::io::Read;
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
use std::time::{Duration, Instant};

fn g() -> Value {
    json!({"appSession":"aa-app","home":"aa-home","spawnCounter":1})
}
fn reserve(h: &Host) -> Result<CaptureReservation, Reason> {
    let mut i = h.inner.0.lock().unwrap();
    let next = match i.aa_epoch.checked_add(1) {
        Some(n) => n,
        None => {
            if let Some(c) = i.aa_capture.as_mut() {
                c.refuse(Reason::Exhausted);
            }
            return Err(Reason::Exhausted);
        }
    };
    if let Some(c) = i.aa_capture.as_mut() {
        c.retire();
    }
    i.aa_epoch = next;
    Ok(CaptureReservation::new(&h.inner, next))
}
struct Pipe {
    h: Host,
    reader: std::fs::File,
}
impl Pipe {
    fn new() -> Self {
        let mut fds = [-1; 2];
        assert_eq!(unsafe { libc::pipe(fds.as_mut_ptr()) }, 0);
        let read = unsafe { OwnedFd::from_raw_fd(fds[0]) };
        let write = unsafe { OwnedFd::from_raw_fd(fds[1]) };
        for fd in [read.as_raw_fd(), write.as_raw_fd()] {
            let flags = unsafe { libc::fcntl(fd, libc::F_GETFD) };
            assert!(flags >= 0);
            assert_eq!(
                unsafe { libc::fcntl(fd, libc::F_SETFD, flags | libc::FD_CLOEXEC) },
                0
            );
        }
        let flags = unsafe { libc::fcntl(write.as_raw_fd(), libc::F_GETFL) };
        assert!(flags >= 0);
        assert_eq!(
            unsafe { libc::fcntl(write.as_raw_fd(), libc::F_SETFL, flags | libc::O_NONBLOCK) },
            0
        );
        let h = Host::new();
        *h.stdin.lock().unwrap() = Some(std::process::ChildStdin::from(write));
        {
            let mut i = h.inner.0.lock().unwrap();
            i.generation = g();
            i.state = "ready".into();
            i.threads
                .push(json!({"generation":g(),"threadId":"thread"}));
        }
        Self {
            h,
            reader: std::fs::File::from(read),
        }
    }
    fn request(&self, capture: bool, text: &str) -> SourceRequest {
        let reservation = if capture {
            Some(reserve(&self.h).unwrap())
        } else {
            None
        };
        self.h
            .request_begin_scoped_private(
                "turn/start",
                Host::text_turn_params("thread", text).unwrap(),
                json!({"kind":"synthetic"}),
                false,
                Some(&g()),
                false,
                None,
                reservation,
            )
            .unwrap()
    }
    fn drain(&mut self) -> Vec<u8> {
        let end = Instant::now() + Duration::from_millis(1000);
        let mut out = Vec::new();
        while out.last() != Some(&b'\n') {
            assert!(Instant::now() < end);
            let mut p = libc::pollfd {
                fd: self.reader.as_raw_fd(),
                events: libc::POLLIN,
                revents: 0,
            };
            let ms = (end - Instant::now()).as_millis().min(1000) as i32;
            assert!(unsafe { libc::poll(&mut p, 1, ms) } > 0);
            let mut bytes = [0; 2048];
            let n = self.reader.read(&mut bytes[..2048 - out.len()]).unwrap();
            assert!(n > 0);
            out.extend_from_slice(&bytes[..n]);
            assert!(out.len() <= 2048);
        }
        out
    }
    fn sent(&mut self, r: &SourceRequest) {
        let mut expected = serde_json::to_vec(&r.frame).unwrap();
        expected.push(b'\n');
        assert!(expected.len() <= 1024);
        assert_eq!(self.drain(), expected);
        assert!(self.h.inner.0.lock().unwrap().source_requests[&r.frame["id"].to_string()].written);
    }
}
fn response(id: &Value) -> Value {
    json!({"id":id,"result":{"turn":{"id":"turn","items":[],"status":"inProgress"}}})
}
fn item() -> Value {
    json!({"method":"item/completed","params":{"threadId":"thread","turnId":"turn","completedAtMs":42,"item":{"id":"item","type":"agentMessage","text":"answer","phase":"final_answer"}}})
}
fn terminal() -> Value {
    json!({"method":"turn/completed","params":{"threadId":"thread","turn":{"id":"turn","items":[],"status":"completed","error":null}}})
}
fn feed(h: &Host, v: &Value) {
    h.on_line(&serde_json::to_vec(v).unwrap(), &g());
}
fn state(h: &Host) -> Standing {
    h.inner
        .0
        .lock()
        .unwrap()
        .aa_capture
        .as_ref()
        .unwrap()
        .readout()
        .0
}
fn consistent(h: &Host) -> bool {
    matches!(state(h), Standing::ConsistentThroughReceipt(..))
}
fn all(h: &Host, id: &Value) {
    feed(h, &response(id));
    feed(h, &item());
    feed(h, &terminal());
}

#[test]
fn aa_cap_actual_pipe_join_and_late_response_conflict() {
    let mut p = Pipe::new();
    let r = p.request(true, "original");
    p.sent(&r);
    all(&p.h, &r.frame["id"]);
    assert!(consistent(&p.h));
    assert_eq!(
        p.h.inner
            .0
            .lock()
            .unwrap()
            .aa_capture
            .as_ref()
            .unwrap()
            .readout()
            .1,
        "nativeSchemaValidation=not-performed-by-core"
    );
    let revision =
        p.h.inner
            .0
            .lock()
            .unwrap()
            .aa_capture
            .as_ref()
            .unwrap()
            .revision;
    feed(&p.h, &response(&r.frame["id"]));
    assert!(consistent(&p.h));
    assert_eq!(
        p.h.inner
            .0
            .lock()
            .unwrap()
            .aa_capture
            .as_ref()
            .unwrap()
            .revision,
        revision
    );
    let mut bad = response(&r.frame["id"]);
    bad["result"]["turn"]["id"] = json!("other");
    feed(&p.h, &bad);
    assert_eq!(state(&p.h), Standing::Refused(Reason::Conflict));
    assert!(p.h.snapshot()["journal"]
        .as_array()
        .unwrap()
        .iter()
        .any(|v| v["class"] == "uncorrelated-response"));
}
#[test]
fn aa_cap_early_facts_wait_for_real_write_and_simulated_errors_never_qualify() {
    for failed in [
        None,
        Some("before real write"),
        Some("reported partial attempt; no kernel partial-write claim"),
    ] {
        let mut p = Pipe::new();
        *p.h.aa_before_write.lock().unwrap() = Some(Box::new(|h, r| {
            all(h, &r.frame["id"]);
            assert!(!consistent(h));
        }));
        *p.h.aa_simulated_write.lock().unwrap() = failed;
        let r = p.request(true, "small");
        if failed.is_none() {
            p.sent(&r);
            assert!(consistent(&p.h));
        } else {
            assert!(!consistent(&p.h));
            assert!(
                p.h.inner.0.lock().unwrap().source_requests[&r.frame["id"].to_string()]
                    .write_error
                    .as_ref()
                    .unwrap()
                    .contains("simulated")
            );
        }
    }
}
#[test]
fn aa_cap_closure_during_settlement_and_old_generation_never_revive() {
    let mut p = Pipe::new();
    *p.h.aa_after_write.lock().unwrap() = Some(Box::new(|h, r| {
        all(h, &r.frame["id"]);
        Host::close_generation(&mut h.inner.0.lock().unwrap());
    }));
    let r = p.request(true, "small");
    p.sent(&r);
    assert_eq!(state(&p.h), Standing::Refused(Reason::Closed));
    let before =
        p.h.inner
            .0
            .lock()
            .unwrap()
            .aa_capture
            .as_ref()
            .unwrap()
            .revision;
    feed(&p.h, &item());
    assert_eq!(
        p.h.inner
            .0
            .lock()
            .unwrap()
            .aa_capture
            .as_ref()
            .unwrap()
            .revision,
        before
    );
    assert!(p.h.snapshot()["journal"]
        .as_array()
        .unwrap()
        .iter()
        .any(|v| v["class"] == "closed-generation-frame"));
}
#[test]
fn aa_cap_same_identity_mutations_and_second_final_id_poison() {
    for change in ["id", "text", "phase", "extra", "timestamp"] {
        let mut p = Pipe::new();
        let r = p.request(true, "small");
        p.sent(&r);
        all(&p.h, &r.frame["id"]);
        let mut v = item();
        match change {
            "id" => v["params"]["item"]["id"] = json!("item2"),
            "text" => v["params"]["item"]["text"] = json!("changed"),
            "phase" => v["params"]["item"]["phase"] = json!("commentary"),
            "extra" => v["extra"] = json!(true),
            _ => v["params"]["completedAtMs"] = json!(43),
        }
        feed(&p.h, &v);
        assert!(matches!(state(&p.h), Standing::Refused(_)), "{change}");
    }
}
#[test]
fn aa_cap_unsupported_shapes_and_two_early_turns_refuse() {
    for which in 0..10 {
        let mut p = Pipe::new();
        let r = p.request(true, "small");
        p.sent(&r);
        feed(&p.h, &response(&r.frame["id"]));
        let mut a = item();
        let mut t = terminal();
        match which {
            0 => a["params"]["item"]["phase"] = Value::Null,
            1 => {
                a["params"]["item"].as_object_mut().unwrap().remove("phase");
            }
            2 => a["params"]["item"]["phase"] = json!("commentary"),
            3 => t["params"]["turn"]["status"] = json!("failed"),
            4 => t["params"]["turn"]["error"] = json!({}),
            5 => a["params"]["completedAtMs"] = json!("42"),
            6 => t["params"]["turn"]["id"] = json!("turn2"),
            7 => t["params"]["turn"]["status"] = json!("interrupted"),
            8 => feed(
                &p.h,
                &json!({"id":r.frame["id"],"error":{"code":-1,"message":"synthetic conflict"}}),
            ),
            _ => {
                let mut different = response(&r.frame["id"]);
                different["result"]["extra"] = json!(true);
                feed(&p.h, &different);
            }
        };
        feed(&p.h, &a);
        feed(&p.h, &t);
        assert!(!consistent(&p.h));
    }
}

fn core() -> (Host, Core) {
    let p = Pipe::new();
    let r = reserve(&p.h).unwrap();
    let f = json!({"id":1,"method":"turn/start","params":{"threadId":"thread","input":[{"type":"text","text":"x","text_elements":[]}]}});
    let c = Core::bind(r, &p.h.inner, 1, &g(), "ref", &f, Some((4, (5, 6))));
    (p.h, c)
}
#[test]
fn aa_cap_cut_binding_epoch_pipe_noattempt_and_counter_controls() {
    for wrong in 0..6 {
        let (h, mut c) = core();
        let mut gen = g();
        let mut epoch = 1;
        let mut pipe = (4, (5, 6));
        match wrong {
            0 => gen["appSession"] = json!("other"),
            1 => gen["home"] = json!("other"),
            2 => gen["spawnCounter"] = json!(2),
            3 => epoch = 2,
            4 => pipe.1 = (8, 9),
            _ => {}
        }
        c.prewrite(&gen, epoch, "ref", pipe, 10);
        if wrong == 5 {
            c.observe(&g(), 1, 4, 10, &item());
        }
        assert!(matches!(c.standing, Standing::Refused(_)));
        drop(h);
    }
    let (h, mut c) = core();
    c.settle(&g(), 1, "ref", Some((4, (5, 6))), true);
    assert_eq!(c.standing, Standing::Refused(Reason::NoAttempt));
    let other = Host::new();
    let r = reserve(&h).unwrap();
    let f = json!({});
    let c = Core::bind(r, &other.inner, 2, &g(), "ref", &f, None);
    assert_eq!(c.standing, Standing::Refused(Reason::Foreign));
    h.inner.0.lock().unwrap().aa_epoch = u64::MAX;
    assert!(matches!(reserve(&h), Err(Reason::Exhausted)));
    let (_, mut c) = core();
    c.prewrite(&g(), 1, "ref", (4, (5, 6)), 500);
    c.settle(&g(), 1, "ref", Some((4, (5, 6))), true);
    c.revision = u64::MAX;
    c.observe(&g(), 1, 4, 501, &item());
    assert_eq!(c.standing, Standing::Refused(Reason::Exhausted));
}
#[test]
fn aa_cap_pf1_numeric_limits_and_exact_stream_boundary() {
    let mut v = json!(0);
    for _ in 0..DEPTH {
        v = json!([v]);
    }
    assert!(pf1(&v).is_ok());
    assert_eq!(pf1(&json!([v])), Err(Reason::Limit));
    assert!(pf1(&json!(vec![0; WIDTH])).is_ok());
    assert_eq!(pf1(&json!(vec![0; WIDTH + 1])), Err(Reason::Limit));
    let mut map = serde_json::Map::new();
    for n in 0..WIDTH {
        map.insert(format!("k{n}"), Value::Null);
    }
    assert!(pf1(&Value::Object(map.clone())).is_ok());
    map.insert("over".into(), Value::Null);
    assert_eq!(pf1(&Value::Object(map)), Err(Reason::Limit));
    let mut nested = Value::Null;
    for _ in 0..DEPTH {
        nested = json!({"k":nested});
    }
    assert!(pf1(&nested).is_ok());
    assert_eq!(pf1(&json!({"k":nested})), Err(Reason::Limit));
    let object = |n: usize| {
        let mut o = serde_json::Map::new();
        for k in 0..n {
            o.insert(format!("k{k}"), Value::Null);
        }
        Value::Object(o)
    };
    let mut keyed = vec![object(128); 15];
    keyed.push(object(119));
    keyed.push(Value::Null);
    assert!(pf1(&Value::Array(keyed.clone())).is_ok());
    keyed.push(Value::Null);
    assert_eq!(pf1(&Value::Array(keyed)), Err(Reason::Limit));
    let mut arrays = vec![vec![0; 127]; 32];
    arrays[31].pop();
    let v = json!(arrays);
    assert!(pf1(&v).is_ok());
    arrays[31].push(0);
    assert_eq!(pf1(&json!(arrays)), Err(Reason::Limit));
    assert!(pf1(&json!("x".repeat(TEXT))).is_ok());
    assert_eq!(pf1(&json!("x".repeat(TEXT + 1))), Err(Reason::Limit));
    let mut o = serde_json::Map::new();
    o.insert("k".repeat(ID), Value::Null);
    assert!(pf1(&Value::Object(o)).is_ok());
    let mut o = serde_json::Map::new();
    o.insert("k".repeat(ID + 1), Value::Null);
    assert_eq!(pf1(&Value::Object(o)), Err(Reason::Limit));
    let a = json!([
        "x".repeat(TEXT),
        "x".repeat(TEXT),
        "x".repeat(TEXT),
        "x".repeat(65523)
    ]);
    assert_eq!(serde_json::to_vec(&a).unwrap().len(), FRAME);
    assert!(pf1(&a).is_ok());
    let a = json!([
        "x".repeat(TEXT),
        "x".repeat(TEXT),
        "x".repeat(TEXT),
        "x".repeat(65524)
    ]);
    assert_eq!(pf1(&a), Err(Reason::Limit));
    assert!(Identity::new(&"a".repeat(ID)).is_ok());
    assert_eq!(
        Identity::new(&"a".repeat(ID + 1)).err(),
        Some(Reason::Limit)
    );
}
#[test]
fn aa_cap_pf1_parsed_identity_and_native_schema_limit() {
    let actual = pf1(&json!({"a":1}))
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect::<String>();
    assert_eq!(
        actual,
        "c345651ef329c5661c9cb01d14602f441d267c0877dde7f2b4bf420c68f89b80"
    );
    assert_eq!(
        pf1(&serde_json::from_str::<Value>(r#"{"b":2,"a":1}"#).unwrap()),
        pf1(&json!({"a":1,"b":2}))
    );
    for (a, b) in [
        (json!([1, 2]), json!([2, 1])),
        (json!("text"), json!("text ")),
        (json!("é"), json!("e\u{301}")),
        (json!(1), json!(1.0)),
    ] {
        assert_ne!(pf1(&a), pf1(&b));
    }
    let mut p = Pipe::new();
    let r = p.request(true, "small");
    p.sent(&r);
    let mut subset_only = response(&r.frame["id"]);
    subset_only["result"]["turn"]["error"] = json!("invalid native TurnError type");
    feed(&p.h, &subset_only);
    feed(&p.h, &item());
    feed(&p.h, &terminal());
    assert!(consistent(&p.h));
    // Pinned schema /definitions/v2/Turn/error permits TurnError object or
    // null, not this string. The frozen response subset does not check it.
    // No full validator is called, and readout explicitly disclaims it.
    assert!(subset_only["result"]["turn"]["error"].is_string());
    assert_eq!(
        p.h.inner
            .0
            .lock()
            .unwrap()
            .aa_capture
            .as_ref()
            .unwrap()
            .readout()
            .1,
        "nativeSchemaValidation=not-performed-by-core"
    );
    assert!(scalar(&json!("x".repeat(ID))).is_ok());
    assert_eq!(scalar(&json!("x".repeat(ID + 1))), Err(Reason::Limit));
}
#[test]
fn aa_cap_retained_and_scratch_capacity_stay_fixed() {
    assert!(std::mem::size_of::<Core>() <= RETAINED);
    assert!(SORT_SCRATCH + 4096 <= SCRATCH);
    assert!(RETAINED + SCRATCH + 4096 <= INCREMENTAL);
    assert!(within_budget(RETAINED, SCRATCH, INCREMENTAL));
    assert!(!within_budget(RETAINED + 1, SCRATCH, INCREMENTAL));
    assert!(!within_budget(RETAINED, SCRATCH + 1, INCREMENTAL));
    assert!(!within_budget(RETAINED, SCRATCH, INCREMENTAL + 1));
    let (_, mut c) = core();
    c.prewrite(&g(), 1, "ref", (4, (5, 6)), 0);
    c.settle(&g(), 1, "ref", Some((4, (5, 6))), true);
    c.observe(&g(), 1, 4, 1, &response(&json!(1)));
    c.observe(&g(), 1, 4, 2, &item());
    c.observe(&g(), 1, 4, 3, &terminal());
    let size = c.readout().2;
    let revision = c.revision;
    for n in 4..1004 {
        c.observe(&g(), 1, 4, n, &item());
        c.observe(&g(), 1, 4, n, &json!({"method":"unrelated"}));
        assert_eq!(c.readout().2, size);
    }
    assert_eq!(c.revision, revision);
    println!("AA-CAP owned inline={} heap=0 sorted scratch={} plus4096 visitor/sink allowance; limits={}/{}/{}",size,SORT_SCRATCH,RETAINED,SCRATCH,INCREMENTAL);
}

#[test]
fn aa_cap_no_attempt_and_send_receipt_domains() {
    let p = Pipe::new();
    *p.h.stdin.lock().unwrap() = None;
    let r = p.request(true, "small");
    assert_eq!(state(&p.h), Standing::Refused(Reason::NoAttempt));
    assert!(!p.h.inner.0.lock().unwrap().source_requests[&r.frame["id"].to_string()].written);
    let mut p = Pipe::new();
    {
        let mut i = p.h.inner.0.lock().unwrap();
        i.send_position = 900;
        i.receipt_position = 4;
    }
    let r = p.request(true, "small");
    p.sent(&r);
    all(&p.h, &r.frame["id"]);
    assert!(consistent(&p.h));
    assert_eq!(
        p.h.inner.0.lock().unwrap().aa_capture.as_ref().unwrap().cut,
        Some(4)
    );
}
#[test]
fn aa_cap_foreign_threads_old_generation_and_reuse() {
    let mut p = Pipe::new();
    let r = p.request(true, "small");
    p.sent(&r);
    let mut v = item();
    v["params"]["threadId"] = json!("foreign");
    feed(&p.h, &v);
    v = item();
    v["method"] = json!("item/agentMessage/delta");
    feed(&p.h, &v);
    assert_eq!(state(&p.h), Standing::Pending);
    let mut wrong = g();
    wrong["home"] = json!("foreign");
    p.h.on_line(&serde_json::to_vec(&item()).unwrap(), &wrong);
    assert_eq!(state(&p.h), Standing::Pending);
    all(&p.h, &r.frame["id"]);
    assert!(consistent(&p.h));
    let old = reserve(&p.h).unwrap();
    let _new = reserve(&p.h).unwrap();
    assert!(!old.matches(&p.h.inner, p.h.inner.0.lock().unwrap().aa_epoch));
    assert_eq!(state(&p.h), Standing::Refused(Reason::Closed));
}
#[test]
fn aa_cap_absent_limit_poison_differential_protocol() {
    for condition in ["normal", "limit", "poison"] {
        let mut traces = Vec::new();
        for capture in [false, true] {
            let mut p = Pipe::new();
            let r = p.request(capture, "small");
            p.sent(&r);
            let reply = response(&r.frame["id"]);
            feed(&p.h, &reply);
            assert_eq!(r.receiver.lock().unwrap().try_recv().unwrap(), reply);
            let mut a = item();
            if condition == "limit" {
                a["params"]["item"]["text"] = json!("x".repeat(TEXT + 1));
            }
            feed(&p.h, &a);
            feed(&p.h, &terminal());
            if condition == "poison" {
                let mut bad = response(&r.frame["id"]);
                bad["result"]["turn"]["id"] = json!("wrong");
                feed(&p.h, &bad);
            }
            feed(
                &p.h,
                &json!({"method":"unknown/synthetic","params":{"preserved":true}}),
            );
            feed(
                &p.h,
                &json!({"id":"server-auto","method":"unknown/automatic","params":{}}),
            );
            let automatic = p.drain();
            assert!(serde_json::from_slice::<Value>(&automatic)
                .unwrap()
                .get("error")
                .is_some());
            let closed = Host::close_generation(&mut p.h.inner.0.lock().unwrap());
            let snapshot = p.h.snapshot();
            traces.push((
                snapshot["clientRequests"].clone(),
                snapshot["serverRequests"].clone(),
                snapshot["journal"].clone(),
                closed,
                automatic,
            ));
        }
        assert_eq!(traces[0], traces[1], "ordinary differential {condition}");
    }
}

// Only compiled for tests; thread-local cumulative allocation bounds peak too.
struct Meter;
thread_local! {static ON:std::cell::Cell<bool>=const{std::cell::Cell::new(false)};static BYTES:std::cell::Cell<usize>=const{std::cell::Cell::new(0)};}
#[global_allocator]
static AA_ALLOC: Meter = Meter;
fn account(n: usize) {
    let _ = ON.try_with(|on| {
        if on.get() {
            let _ = BYTES.try_with(|b| b.set(b.get().saturating_add(n)));
        }
    });
}
unsafe impl std::alloc::GlobalAlloc for Meter {
    unsafe fn alloc(&self, l: std::alloc::Layout) -> *mut u8 {
        account(l.size());
        unsafe { std::alloc::GlobalAlloc::alloc(&std::alloc::System, l) }
    }
    unsafe fn dealloc(&self, p: *mut u8, l: std::alloc::Layout) {
        unsafe { std::alloc::GlobalAlloc::dealloc(&std::alloc::System, p, l) }
    }
    unsafe fn realloc(&self, p: *mut u8, l: std::alloc::Layout, n: usize) -> *mut u8 {
        account(n);
        unsafe { std::alloc::GlobalAlloc::realloc(&std::alloc::System, p, l, n) }
    }
}
fn measured<T>(f: impl FnOnce() -> T) -> (T, usize) {
    BYTES.with(|n| n.set(0));
    ON.with(|n| n.set(true));
    let r = f();
    ON.with(|n| n.set(false));
    (r, BYTES.with(|n| n.get()))
}
#[test]
fn aa_cap_measured_stream_and_retained_allocations() {
    let a = json!([
        "x".repeat(TEXT),
        "x".repeat(TEXT),
        "x".repeat(TEXT),
        "x".repeat(65523)
    ]);
    let (r, n) = measured(|| pf1(&a));
    assert!(r.is_ok());
    assert_eq!(n, 0);
    let a = json!([
        "x".repeat(TEXT),
        "x".repeat(TEXT),
        "x".repeat(TEXT),
        "x".repeat(65524)
    ]);
    let (r, error) = measured(|| pf1(&a));
    assert_eq!(r, Err(Reason::Limit));
    assert!(error <= 4096);
    let (h, _) = core();
    let frame = json!({"id":1,"method":"turn/start","params":{"threadId":"thread","input":[{"type":"text","text":"x".repeat(TEXT),"text_elements":[]}]}});
    let gen = g();
    let r = reserve(&h).unwrap();
    let epoch = h.inner.0.lock().unwrap().aa_epoch;
    let (c, owned) =
        measured(|| Core::bind(r, &h.inner, epoch, &gen, "ref", &frame, Some((4, (5, 6)))));
    assert_eq!(c.standing, Standing::Pending);
    assert_eq!(owned, 0);
    println!("AA-CAP measured maxPF1 allocation={n}, rejected PF1 allocation={error}, bind allocation={owned}; inline={}, scratch={}",std::mem::size_of::<Core>(),SORT_SCRATCH);
}

#[test]
fn aa_cap_bound_id_text_caps_and_early_ambiguity() {
    for (field, limit) in [
        ("thread", ID),
        ("reference", ID),
        ("session", ID),
        ("home", ID),
        ("requestText", TEXT),
    ] {
        for over in [false, true] {
            let (h, _) = core();
            let r = reserve(&h).unwrap();
            let epoch = h.inner.0.lock().unwrap().aa_epoch;
            let mut gen = g();
            let mut frame = json!({"id":1,"method":"turn/start","params":{"threadId":"thread","input":[{"type":"text","text":"x","text_elements":[]}]}});
            let mut reference = "ref".to_owned();
            let value = "x".repeat(limit + usize::from(over));
            match field {
                "thread" => frame["params"]["threadId"] = json!(value),
                "reference" => reference = value,
                "session" => gen["appSession"] = json!(value),
                "home" => gen["home"] = json!(value),
                _ => frame["params"]["input"][0]["text"] = json!(value),
            }
            let c = Core::bind(
                r,
                &h.inner,
                epoch,
                &gen,
                &reference,
                &frame,
                Some((4, (5, 6))),
            );
            assert_eq!(
                matches!(c.standing, Standing::Pending),
                !over,
                "{field} over={over}"
            );
        }
    }
    for field in ["turnId", "itemId", "messageText"] {
        for over in [false, true] {
            let (_, mut c) = core();
            c.prewrite(&g(), 1, "ref", (4, (5, 6)), 0);
            let mut v = item();
            let value = "x".repeat(if field == "messageText" {
                TEXT + usize::from(over)
            } else {
                ID + usize::from(over)
            });
            match field {
                "turnId" => v["params"]["turnId"] = json!(value),
                "itemId" => v["params"]["item"]["id"] = json!(value),
                _ => v["params"]["item"]["text"] = json!(value),
            }
            c.observe(&g(), 1, 4, 1, &v);
            assert_eq!(
                matches!(c.standing, Standing::Pending),
                !over,
                "{field} over={over}"
            );
        }
    }
    let (_, mut c) = core();
    c.prewrite(&g(), 1, "ref", (4, (5, 6)), 10);
    c.observe(&g(), 1, 4, 11, &item());
    let mut second = terminal();
    second["params"]["turn"]["id"] = json!("other");
    c.observe(&g(), 1, 4, 12, &second);
    assert!(c.response.is_none());
    assert_eq!(c.standing, Standing::Refused(Reason::Conflict));
}
#[test]
fn aa_cap_object_sorting_allocations_and_epoch_exhaustion_retire() {
    let mut m = serde_json::Map::new();
    for n in 0..WIDTH {
        m.insert(format!("key{n:03}"), json!("x".repeat(1000)));
    }
    let v = Value::Object(m);
    let (r, bytes) = measured(|| pf1(&v));
    assert!(r.is_ok());
    assert_eq!(bytes, 0);
    let mut p = Pipe::new();
    let r = p.request(true, "small");
    p.sent(&r);
    all(&p.h, &r.frame["id"]);
    assert!(consistent(&p.h));
    p.h.inner.0.lock().unwrap().aa_epoch = u64::MAX;
    assert!(matches!(reserve(&p.h), Err(Reason::Exhausted)));
    assert_eq!(state(&p.h), Standing::Refused(Reason::Exhausted));
}

#[test]
fn aa_cap_pipe_replacement_after_write_invalidates_later_facts() {
    let mut p = Pipe::new();
    let r = p.request(true, "small");
    p.sent(&r);
    all(&p.h, &r.frame["id"]);
    assert!(consistent(&p.h));
    p.h.inner.0.lock().unwrap().attachment_pipe_epoch += 1;
    feed(&p.h, &item());
    assert_eq!(state(&p.h), Standing::Refused(Reason::Foreign));
}

#[test]
fn aa_cap_explicit_reservation_cannot_be_stolen_by_intervening_request() {
    let mut p = Pipe::new();
    let reservation = reserve(&p.h).unwrap();
    let other =
        p.h.request_begin_scoped_private(
            "thread/read",
            json!({"threadId":"thread"}),
            json!({"kind":"synthetic"}),
            false,
            Some(&g()),
            false,
            None,
            None,
        )
        .unwrap();
    p.sent(&other);
    assert!(p.h.inner.0.lock().unwrap().aa_capture.is_none());
    let selected =
        p.h.request_begin_scoped_private(
            "turn/start",
            Host::text_turn_params("thread", "chosen").unwrap(),
            json!({"kind":"synthetic"}),
            false,
            Some(&g()),
            false,
            None,
            Some(reservation),
        )
        .unwrap();
    p.sent(&selected);
    feed(&p.h, &response(&other.frame["id"]));
    assert_eq!(state(&p.h), Standing::Pending);
    all(&p.h, &selected.frame["id"]);
    assert!(consistent(&p.h));
}

#[test]
fn aa_cap_server_requests_cannot_supply_item_or_terminal_notification_facts() {
    for (item_id, terminal_id) in [(true, false), (false, true), (true, true)] {
        let mut ordinary = Vec::new();
        for capture in [false, true] {
            let mut p = Pipe::new();
            let r = p.request(capture, "small");
            p.sent(&r);
            feed(&p.h, &response(&r.frame["id"]));
            let mut a = item();
            let mut t = terminal();
            if item_id {
                a["id"] = json!(999);
            }
            if terminal_id {
                t["id"] = json!(998);
            }
            let mut replies = Vec::new();
            for (frame, has_id) in [(&a, item_id), (&t, terminal_id)] {
                feed(&p.h, frame);
                if has_id {
                    let bytes = p.drain();
                    let reply: Value = serde_json::from_slice(&bytes).unwrap();
                    assert_eq!(reply["id"], frame["id"]);
                    assert!(
                        reply.get("error").is_some(),
                        "ordinary mandatory error reply remains actual pipe IO"
                    );
                    replies.push(bytes);
                }
            }
            if capture {
                assert!(!consistent(&p.h));
                let i = p.h.inner.0.lock().unwrap();
                let core = i.aa_capture.as_ref().unwrap();
                assert_eq!(core.item.is_some(), !item_id);
                assert_eq!(core.terminal.is_some(), !terminal_id);
            }
            let snapshot = p.h.snapshot();
            let classified = snapshot["journal"]
                .as_array()
                .unwrap()
                .iter()
                .filter(|e| e["class"] == "server-request")
                .count();
            assert_eq!(classified, usize::from(item_id) + usize::from(terminal_id));
            ordinary.push((
                snapshot["clientRequests"].clone(),
                snapshot["serverRequests"].clone(),
                snapshot["journal"].clone(),
                replies,
            ));
        }
        assert_eq!(
            ordinary[0], ordinary[1],
            "capture cannot alter server-request handling"
        );
    }
}

#[test]
fn aa_cap_host_malformed_marker_cannot_supply_protocol_facts() {
    for which in [0, 1, 2] {
        let mut p = Pipe::new();
        let r = p.request(true, "small");
        p.sent(&r);
        let mut frames = [response(&r.frame["id"]), item(), terminal()];
        frames[which]["observation"] = json!("synthetic malformed marker");
        for frame in frames {
            feed(&p.h, &frame);
        }
        assert!(!consistent(&p.h));
        assert!(p.h.snapshot()["journal"]
            .as_array()
            .unwrap()
            .iter()
            .any(|v| v["class"] == "malformed"));
    }
}

#[test]
fn aa_cap_matching_rpc_id_still_requires_actual_response_class() {
    let mut p = Pipe::new();
    let r = p.request(true, "small");
    p.sent(&r);
    let mut server = item();
    server["id"] = r.frame["id"].clone();
    feed(&p.h, &server);
    let reply: Value = serde_json::from_slice(&p.drain()).unwrap();
    assert_eq!(reply["id"], r.frame["id"]);
    assert!(reply.get("error").is_some());
    assert_eq!(state(&p.h), Standing::Pending);
    feed(&p.h, &json!({"id":r.frame["id"]})); // Host malformed, not response
    assert_eq!(state(&p.h), Standing::Pending);
    all(&p.h, &r.frame["id"]);
    assert!(consistent(&p.h)); // later genuine response + notifications only
}
