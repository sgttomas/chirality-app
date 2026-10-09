use super::*;
use crate::hosting::Host;
use crate::role_supply::Guidance;
use crate::runtime_session::HistorySession;
use std::io::Read;
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
use std::time::{Duration, Instant};

fn generation() -> Value {
    json!({"appSession":"call-app","home":"call-home","spawnCounter":1})
}
fn composition(role: Role) -> Composition {
    let common = Guidance::seeded(
        "AGENTS.md",
        "synthetic",
        b"Synthetic common.\n".to_vec(),
        b"Synthetic common.\n",
    )
    .unwrap();
    let bytes = b"Synthetic role guidance.\n";
    let role_doc = Guidance::seeded(
        &format!("agents/AGENT_{}.md", role.name()),
        "synthetic",
        bytes.to_vec(),
        bytes,
    )
    .unwrap();
    Composition::new(&common, Some((role, &role_doc)), role == Role::TASK).unwrap()
}
fn start_result() -> Value {
    json!({"thread":{"id":"thread","cliVersion":"0.160.0","createdAt":1,"updatedAt":2,"cwd":"/synthetic","ephemeral":false,"modelProvider":"synthetic","preview":"synthetic","projectId":null,"sessionId":"synthetic-native","source":"appServer","status":{"type":"idle"},"turns":[],"agentRole":"WORKING_ITEMS"},"model":"synthetic","modelProvider":"synthetic","cwd":"/synthetic","approvalPolicy":"on-request","approvalsReviewer":"user","sandbox":{"type":"readOnly"},"instructionSources":[]})
}
fn args() -> Value {
    json!({"base":{"path":"/synthetic/base.json","id":"base","byteLength":0,"sha256":"a".repeat(64)},"question":"question","claimIds":[]})
}
fn call(id: Value) -> Value {
    json!({"id":id,"method":"item/tool/call","params":{"threadId":"thread","turnId":"turn","callId":"call","tool":TOOL,"arguments":args()}})
}
fn feed(h: &Host, v: &Value) {
    h.on_line(&serde_json::to_vec(v).unwrap(), &generation());
}
fn resolution(h: &Host) {
    feed(
        h,
        &json!({"method":"serverRequest/resolved","params":{"threadId":"thread","requestId":10}}),
    );
}
struct Fixture {
    host: Host,
    reader: std::fs::File,
    history: HistorySession,
    composition: Composition,
}
impl Fixture {
    fn new(role: Role) -> Self {
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
        let host = Host::new();
        *host.stdin.lock().unwrap() = Some(std::process::ChildStdin::from(write));
        {
            let mut i = host.inner.0.lock().unwrap();
            i.state = "ready".into();
            i.generation = generation();
        }
        Self {
            host,
            reader: std::fs::File::from(read),
            history: HistorySession::default(),
            composition: composition(role),
        }
    }
    fn drain(&mut self) -> Value {
        let mut bytes = Vec::new();
        let deadline = Instant::now() + Duration::from_millis(1000);
        while bytes.last() != Some(&b'\n') {
            let remaining = deadline
                .checked_duration_since(Instant::now())
                .expect("pipe deadline");
            let mut poll = libc::pollfd {
                fd: self.reader.as_raw_fd(),
                events: libc::POLLIN,
                revents: 0,
            };
            assert!(
                unsafe { libc::poll(&mut poll, 1, remaining.as_millis().min(1000) as i32) } > 0
            );
            let mut buf = [0; 4096];
            let n = self.reader.read(&mut buf[..4096 - bytes.len()]).unwrap();
            assert!(n > 0);
            bytes.extend_from_slice(&buf[..n]);
            assert!(bytes.len() <= 4096);
        }
        assert!(bytes.len() <= 2048, "small actual fixture frame");
        serde_json::from_slice(&bytes).unwrap()
    }
    fn empty(&self) {
        let mut p = libc::pollfd {
            fd: self.reader.as_raw_fd(),
            events: libc::POLLIN,
            revents: 0,
        };
        assert_eq!(unsafe { libc::poll(&mut p, 1, 0) }, 0);
    }
    fn start(&mut self, offered: bool) -> SourceRequest {
        let receipt = if offered {
            self.host.cce_thread_start(
                &generation(),
                "/synthetic",
                &self.composition,
                "sup:synthetic",
            )
        } else {
            self.host.thread_start_with_guidance_dispatch(
                &generation(),
                "/synthetic",
                "synthetic",
                "synthetic",
                &self.composition.text,
            )
        }
        .unwrap();
        let actual = self.drain();
        assert_eq!(actual, receipt.frame);
        assert_eq!(actual["params"].get("dynamicTools").is_some(), offered);
        if offered {
            assert_eq!(actual["params"]["dynamicTools"], json!([definition()]));
        }
        self.history
            .start_dispatched(receipt.clone(), &self.composition, "sup:synthetic")
            .unwrap();
        feed(
            &self.host,
            &json!({"id":receipt.request_id(),"result":start_result()}),
        );
        self.history.reconcile(&self.host);
        assert!(self.history.binding("call-home", "thread").is_some());
        receipt
    }
    fn view(&self) -> Value {
        self.host
            .inner
            .0
            .lock()
            .unwrap()
            .cce_offer
            .as_ref()
            .and_then(Offer::inspect)
            .unwrap_or(Value::Null)
    }
}

#[test]
fn call_custody_actual_manager_insert_original_call_one_unavailable() {
    let mut f = Fixture::new(Role::WORKING_ITEMS);
    f.start(true);
    assert!(f
        .host
        .inner
        .0
        .lock()
        .unwrap()
        .cce_offer
        .as_ref()
        .unwrap()
        .alive());
    feed(&f.host, &call(json!(10)));
    let reply = f.drain();
    assert_eq!(reply, json!({"id":10,"result":unavailable()}));
    let records = f.host.inner.0.lock().unwrap().server_requests.records();
    assert_eq!(records[0]["originClass"], "named-service");
    assert_eq!(records[0]["state"], "answered");
    assert_eq!(records[0]["settlement"]["kind"], "answer");
    assert_eq!(
        records[0]["settlement"]["origin"],
        json!({"class":"app-rule","ruleName":"managed-service-unavailable"})
    );
    assert_eq!(
        records[0]["acknowledgmentObservation"]["status"],
        "not-observed"
    );
    assert_eq!(f.view()["state"], 3);
    assert!(f.host.child.lock().unwrap().is_none());
    assert!(f.host.inner.0.lock().unwrap().recovery.is_none());
    assert!(f.host.inner.0.lock().unwrap().aa_capture.is_none());
    feed(&f.host, &call(json!(10)));
    f.empty();
    assert_eq!(f.view()["state"], 3);
}
#[test]
fn call_custody_ordinary_start_and_unsupported_remain_ordinary() {
    let mut f = Fixture::new(Role::HELP_HUMAN);
    f.start(false);
    feed(&f.host, &call(json!(10)));
    assert_eq!(
        f.drain(),
        json!({"id":10,"error":{"code":-32601,"message":"App has no registered dynamic tools"}})
    );
    assert!(f.view().is_null());
    let r = f.host.inner.0.lock().unwrap().server_requests.records();
    assert_eq!(r[0]["classification"], "known-app-unsupported");
    assert_eq!(r[0]["originClass"], "none");
}
#[test]
fn call_custody_wrong_role_and_uninserted_offer_do_not_activate() {
    let f = Fixture::new(Role::TASK);
    assert!(f
        .host
        .cce_thread_start(&generation(), "/synthetic", &f.composition, "sup:synthetic")
        .is_err());
    assert!(f.host.client_requests().is_empty());
    f.empty();
    let mut f = Fixture::new(Role::WORKING_ITEMS);
    let r = f
        .host
        .cce_thread_start(&generation(), "/synthetic", &f.composition, "sup:synthetic")
        .unwrap();
    f.drain();
    feed(
        &f.host,
        &json!({"id":r.request_id(),"result":start_result()}),
    );
    f.host.thread_start_dispatch_finish(&r).unwrap();
    feed(&f.host, &call(json!(10)));
    assert!(f.drain().get("error").is_some());
    assert!(!f
        .host
        .inner
        .0
        .lock()
        .unwrap()
        .cce_offer
        .as_ref()
        .unwrap()
        .alive());
}
#[test]
fn call_custody_failed_role_insertion_never_uses_active_admission_flag() {
    let mut f = Fixture::new(Role::WORKING_ITEMS);
    let r = f
        .host
        .cce_thread_start(&generation(), "/synthetic", &f.composition, "sup:synthetic")
        .unwrap();
    f.drain();
    let response = json!({"id":r.request_id(),"result":start_result()});
    let fake = crate::role_lifecycle::PreparedStart::new(
        "call-home",
        generation(),
        r.request_id().clone(),
        r.request_ref(),
        "sup:synthetic",
        &f.composition,
    )
    .unwrap()
    .observe(&generation(), &r.frame, &response)
    .unwrap();
    f.history.bind(fake).unwrap();
    f.history
        .start_dispatched(r.clone(), &f.composition, "sup:synthetic")
        .unwrap();
    feed(&f.host, &response);
    f.history.reconcile(&f.host);
    assert!(
        f.history.start_admitted(&r),
        "existing reporting behavior retained, not a credential"
    );
    assert!(!f
        .host
        .inner
        .0
        .lock()
        .unwrap()
        .cce_offer
        .as_ref()
        .unwrap()
        .alive());
    feed(&f.host, &call(json!(10)));
    assert!(f.drain().get("error").is_some());
}
#[test]
fn call_custody_partial_or_failed_start_is_simulated_and_ineligible() {
    for mode in [
        "simulated failure",
        "simulated reported partial; not kernel evidence",
    ] {
        let mut f = Fixture::new(Role::WORKING_ITEMS);
        *f.host.cce_start_simulated_write.lock().unwrap() = Some(mode);
        let r = f
            .host
            .cce_thread_start(&generation(), "/synthetic", &f.composition, "sup:synthetic")
            .unwrap();
        f.empty();
        f.history
            .start_dispatched(r.clone(), &f.composition, "sup:synthetic")
            .unwrap();
        feed(
            &f.host,
            &json!({"id":r.request_id(),"result":start_result()}),
        );
        f.history.reconcile(&f.host);
        assert!(f.history.binding("call-home", "thread").is_none());
        assert!(!f
            .host
            .inner
            .0
            .lock()
            .unwrap()
            .cce_offer
            .as_ref()
            .unwrap()
            .alive());
        assert!(f.host.cce_original_start_pin(&r).is_err());
    }
}
#[test]
fn call_custody_argument_rejections_and_one_call_budget() {
    for mode in 0..6 {
        let mut f = Fixture::new(Role::HELP_HUMAN);
        f.start(true);
        let mut v = call(json!(10));
        match mode {
            0 => v["params"]["arguments"]["role"] = json!("TASK"),
            1 => {
                v["params"]["arguments"]["base"]["sha256"] = json!(format!("{}\n", "a".repeat(64)))
            }
            2 => v["params"]["arguments"]["claimIds"] = json!(["same", "same"]),
            3 => v["params"]["namespace"] = json!("unexpected"),
            4 => v["params"]["tool"] = json!("other"),
            _ => v["params"]["arguments"]["question"] = json!(""),
        };
        feed(&f.host, &v);
        assert!(f.drain().get("error").is_some());
        assert!(f.view().is_null());
    }
    let mut f = Fixture::new(Role::HELP_HUMAN);
    f.start(true);
    feed(&f.host, &call(json!(10)));
    f.drain();
    let before = f.view();
    feed(&f.host, &call(json!(11)));
    assert!(f.drain().get("error").is_some());
    assert_eq!(f.view(), before);
}
#[test]
fn call_custody_resolution_before_prepare_or_cut_prevents_reply() {
    for prepare in [true, false] {
        let mut f = Fixture::new(Role::HELP_HUMAN);
        f.start(true);
        let hook: Box<dyn FnOnce(&Host, &IncomingCall) + Send> = Box::new(|h, _| resolution(h));
        if prepare {
            *f.host.cce_before_prepare.lock().unwrap() = Some(hook);
        } else {
            *f.host.cce_before_cut.lock().unwrap() = Some(hook);
        }
        feed(&f.host, &call(json!(10)));
        f.empty();
        assert!(f.view()["state"] != 3);
        assert!(f.view()["resolution"].as_u64().unwrap() > 0);
    }
}
#[test]
fn call_custody_post_cut_resolution_does_not_unsend_or_imply_ack() {
    for after_write in [false, true] {
        let mut f = Fixture::new(Role::HELP_HUMAN);
        f.start(true);
        let hook: Box<dyn FnOnce(&Host, &IncomingCall) + Send> = Box::new(|h, _| resolution(h));
        if after_write {
            *f.host.cce_after_write.lock().unwrap() = Some(hook);
        } else {
            *f.host.cce_after_cut.lock().unwrap() = Some(hook);
        }
        feed(&f.host, &call(json!(10)));
        assert_eq!(f.drain()["result"], unavailable());
        assert_eq!(f.view()["state"], 3);
        let r = f.host.inner.0.lock().unwrap().server_requests.records();
        assert_eq!(r[0]["replyWriteResult"], "written");
        assert_eq!(r[0]["acknowledgmentObservation"]["status"], "not-observed");
    }
}
#[test]
fn call_custody_post_cut_closure_keeps_private_actual_write_not_canonical_success() {
    for new_generation in [false, true] {
        let mut f = Fixture::new(Role::HELP_HUMAN);
        f.start(true);
        *f.host.cce_after_cut.lock().unwrap() = Some(Box::new(move |h, _| {
            let mut i = h.inner.0.lock().unwrap();
            Host::close_generation(&mut i);
            if new_generation {
                i.generation["spawnCounter"] = json!(2);
            }
        }));
        feed(&f.host, &call(json!(10)));
        assert_eq!(f.drain()["result"], unavailable());
        assert_eq!(f.view()["state"], 3);
        assert_eq!(f.view()["canonicalUpdated"], false);
        let r = f.host.inner.0.lock().unwrap().server_requests.records();
        assert_eq!(r[0]["replyWriteResult"], "not-attempted");
        assert_eq!(r[0]["acknowledgmentObservation"]["status"], "not-observed");
    }
}
#[test]
fn call_custody_simulated_reply_error_and_retired_manager_do_not_deliver() {
    let mut f = Fixture::new(Role::HELP_HUMAN);
    f.start(true);
    *f.host.cce_simulated_write.lock().unwrap() =
        Some("reported partial; no actual kernel partial write");
    feed(&f.host, &call(json!(10)));
    f.empty();
    assert_eq!(f.view()["state"], 4);
    assert_eq!(
        f.host.inner.0.lock().unwrap().server_requests.records()[0]["replyWriteResult"],
        "write-failed"
    );
    feed(&f.host, &call(json!(10)));
    f.empty();
    let mut f = Fixture::new(Role::HELP_HUMAN);
    f.start(true);
    f.history = HistorySession::default();
    feed(&f.host, &call(json!(10)));
    assert!(f.drain().get("error").is_some());
    assert!(f.view().is_null());
}
#[test]
fn call_custody_oversized_rpc_uses_exact_ordinary_fallback_without_handle() {
    let mut replies = Vec::new();
    for offered in [false, true] {
        let mut f = Fixture::new(Role::HELP_HUMAN);
        f.start(offered);
        feed(&f.host, &call(json!("x".repeat(257))));
        replies.push(f.drain());
        assert!(f.view().is_null());
    }
    assert_eq!(replies[0], replies[1]);
}
#[test]
fn call_custody_shape_limits_are_explicit_not_base_acceptance() {
    assert!(arguments(&args()).is_ok());
    for (field, max) in [("path", PATH_LIMIT), ("id", ID_LIMIT)] {
        for over in [false, true] {
            let mut a = args();
            a["base"][field] = json!("x".repeat(max + usize::from(over)));
            assert_eq!(arguments(&a).is_ok(), !over);
        }
    }
    for over in [false, true] {
        let mut a = args();
        a["question"] = json!("x".repeat(ID_LIMIT + usize::from(over)));
        assert_eq!(arguments(&a).is_ok(), !over);
        let mut a = args();
        a["claimIds"] = json!((0..CLAIM_LIMIT + usize::from(over))
            .map(|n| format!("c{n}"))
            .collect::<Vec<_>>());
        assert_eq!(arguments(&a).is_ok(), !over);
    }
    let mut a = args();
    a["base"]["byteLength"] = json!(BYTE_LENGTH_MAX);
    assert!(arguments(&a).is_ok());
    a["base"]["byteLength"] = json!(BYTE_LENGTH_MAX + 1);
    assert!(arguments(&a).is_err());
    a["base"]["byteLength"] = json!(1.0);
    assert!(arguments(&a).is_ok());
    a["base"]["byteLength"] = json!(1.5);
    assert!(arguments(&a).is_err());
}

#[test]
fn call_custody_borrowed_validation_caps_and_fixed_storage() {
    for limit in [FRAME_LIMIT, ARGS_LIMIT, 4096, 65536] {
        assert!(count_bytes(&json!("x".repeat(limit - 2)), limit).is_ok());
        assert!(count_bytes(&json!("x".repeat(limit - 1)), limit).is_err());
    }
    assert!(bounded(&json!("x".repeat(8192)), FRAME_LIMIT, 8192).is_ok());
    assert!(bounded(&json!("x".repeat(8193)), FRAME_LIMIT, 8192).is_err());
    for over in [false, true] {
        let mut o = serde_json::Map::new();
        o.insert("k".repeat(256 + usize::from(over)), Value::Null);
        assert_eq!(bounded(&Value::Object(o), FRAME_LIMIT, 8192).is_ok(), !over);
        assert_eq!(
            bounded(&json!(vec![0; 64 + usize::from(over)]), FRAME_LIMIT, 8192).is_ok(),
            !over
        );
    }
    let mut nested = Value::Null;
    for _ in 0..8 {
        nested = json!([nested]);
    }
    assert!(bounded(&nested, FRAME_LIMIT, 8192).is_ok());
    assert!(bounded(&json!([nested]), FRAME_LIMIT, 8192).is_err());
    // Root + seven 64-leaf arrays + one 55-leaf array = exactly 512 nodes.
    let mut arrays = vec![json!(vec![0; 64]); 7];
    arrays.push(json!(vec![0; 55]));
    assert!(bounded(&json!(arrays), FRAME_LIMIT, 8192).is_ok());
    arrays[7] = json!(vec![0; 56]);
    assert!(bounded(&json!(arrays), FRAME_LIMIT, 8192).is_err());
    assert!(bounded(&definition(), 4096, 8192).is_ok());
    assert!(budget_ok(
        RETAINED_BOUND,
        super::super::request_event_join::SORT_SCRATCH + 4096,
        RETAINED_BOUND + super::super::request_event_join::SORT_SCRATCH + 4096
    ));
    assert!(!budget_ok(RETAINED_LIMIT + 1, 0, 0));
    assert!(!budget_ok(0, SCRATCH_LIMIT + 1, 0));
    assert!(!budget_ok(0, 0, INCREMENTAL_LIMIT + 1));
    eprintln!("core retained upper bound={RETAINED_BOUND}; fixed validation scratch={} (excludes existing Host/start schema storage)", super::super::request_event_join::SORT_SCRATCH + 4096);
}

#[test]
fn call_custody_identity_caps_and_original_source_refusals() {
    for over in [false, true] {
        assert_eq!(
            SmallId::new(&"x".repeat(256 + usize::from(over))).is_ok(),
            !over
        );
        assert_eq!(
            Rpc::new(&json!("x".repeat(256 + usize::from(over)))).is_ok(),
            !over
        );
        let mut g = generation();
        g["home"] = json!("x".repeat(256 + usize::from(over)));
        assert_eq!(Scope::new(&g).is_ok(), !over);
        let mut a = args();
        a["claimIds"] = json!(["x".repeat(256 + usize::from(over))]);
        assert_eq!(arguments(&a).is_ok(), !over);
    }
    for sha in [
        "A".repeat(64),
        "a".repeat(63),
        "a".repeat(65),
        format!("{}\n", "a".repeat(64)),
    ] {
        let mut a = args();
        a["base"]["sha256"] = json!(sha);
        assert!(arguments(&a).is_err());
    }
    let mut f = Fixture::new(Role::WORKING_ITEMS);
    f.start(true);
    for field in ["turnId", "callId"] {
        let mut v = call(json!(10));
        v["params"][field] = json!("x".repeat(257));
        feed(&f.host, &v);
        assert!(f.drain().get("error").is_some());
        assert!(f.view().is_null());
        // Existing duplicate RPC custody is intentionally not reset; use a new id.
        if field == "turnId" {
            break;
        }
    }
    let i = f.host.inner.0.lock().unwrap();
    let offer = i.cce_offer.as_ref().unwrap();
    let mut g = generation();
    g["spawnCounter"] = json!(2);
    assert!(offer.classify(&g, &call(json!(20))).unwrap().is_err());
    let mut v = call(json!(20));
    v["params"]["threadId"] = json!("foreign");
    assert!(offer.classify(&generation(), &v).unwrap().is_err());
    let mut v = call(json!(20));
    v["params"]["callId"] = json!("x".repeat(257));
    assert!(offer.classify(&generation(), &v).unwrap().is_err());
}

#[test]
fn call_custody_queued_reply_rechecks_resolution_after_writer_acquisition() {
    let mut f = Fixture::new(Role::HELP_HUMAN);
    f.start(true);
    std::thread::scope(|scope| {
        let writer = f.host.frame_write.lock().unwrap();
        let h = &f.host;
        let worker = scope.spawn(move || feed(h, &call(json!(10))));
        let deadline = Instant::now() + Duration::from_millis(1000);
        let prepared = loop {
            if f.view()["state"] == 1 {
                break true;
            }
            if Instant::now() >= deadline {
                break false;
            }
            std::thread::yield_now();
        };
        if prepared {
            resolution(&f.host);
        }
        drop(writer);
        worker.join().unwrap();
        assert!(
            prepared,
            "original reply must reach prepared while writer is held"
        );
    });
    f.empty();
    assert_eq!(f.view()["state"], 5);
    assert_eq!(f.view()["cut"], 0);
}

#[test]
fn call_custody_original_pointer_foreign_host_and_precut_retirement() {
    for mode in 0..3 {
        let mut f = Fixture::new(Role::HELP_HUMAN);
        f.start(true);
        *f.host.cce_before_cut.lock().unwrap() = Some(Box::new(move |h, original| {
            let foreign = Host::new();
            assert!(foreign.cce_reply_unavailable(original).is_err());
            let mut i = h.inner.0.lock().unwrap();
            let offer = i.cce_offer.as_mut().unwrap();
            assert!(offer.take().is_none(), "original handle is one-shot");
            let detached = IncomingCall {
                host: original.host.clone(),
                facts: Arc::new(CallFacts {
                    generation: original.facts.generation.clone(),
                    rpc: original.facts.rpc.clone(),
                    thread: original.facts.thread.clone(),
                    turn: original.facts.turn.clone(),
                    call_id: original.facts.call_id.clone(),
                    receipt: original.facts.receipt,
                    index: original.facts.index,
                    frame: original.facts.frame,
                    params: original.facts.params,
                    state: AtomicU8::new(0),
                    cut: AtomicU64::new(0),
                    resolution: AtomicU64::new(0),
                    canonical: AtomicBool::new(false),
                }),
            };
            assert!(
                !offer.original(&detached),
                "copied values do not recreate the original Arc"
            );
            if mode == 0 {
                offer.retire();
            } else if mode == 1 {
                i.generation["spawnCounter"] = json!(2);
            } else {
                Host::close_generation(&mut i);
            }
        }));
        feed(&f.host, &call(json!(10)));
        f.empty();
        assert_eq!(f.view()["state"], 5);
        assert_eq!(f.view()["cut"], 0);
    }
}

#[test]
fn call_custody_failed_invalid_and_uncorrelated_start_have_no_manager_handoff() {
    for mode in 0..3 {
        let mut f = Fixture::new(Role::HELP_HUMAN);
        let r = f
            .host
            .cce_thread_start(&generation(), "/synthetic", &f.composition, "sup:synthetic")
            .unwrap();
        f.drain();
        f.history
            .start_dispatched(r.clone(), &f.composition, "sup:synthetic")
            .unwrap();
        let reply = match mode {
            0 => json!({"id":r.request_id(),"error":{"code":-1,"message":"synthetic rejection"}}),
            1 => json!({"id":r.request_id(),"result":{"thread":{"id":"thread"}}}),
            _ => json!({"id":"unrelated-start","result":start_result()}),
        };
        feed(&f.host, &reply);
        f.history.reconcile(&f.host);
        assert!(f.history.binding("call-home", "thread").is_none());
        assert!(!f
            .host
            .inner
            .0
            .lock()
            .unwrap()
            .cce_offer
            .as_ref()
            .unwrap()
            .alive());
        feed(&f.host, &call(json!(10)));
        assert!(f.drain().get("error").is_some());
        assert!(f.view().is_null());
    }
}

#[test]
fn call_custody_rejected_second_invocation_cannot_cancel_first_preparation() {
    let mut f = Fixture::new(Role::HELP_HUMAN);
    f.start(true);
    *f.host.cce_before_cut.lock().unwrap() = Some(Box::new(|h, original| {
        assert_eq!(original.facts.state.load(Ordering::SeqCst), 1);
        assert!(h.cce_reply_unavailable(original).is_err());
        assert_eq!(original.facts.state.load(Ordering::SeqCst), 1,
            "rejected second invocation cannot cancel another invocation's preparation");
    }));
    feed(&f.host, &call(json!(10)));
    assert_eq!(f.drain(), json!({"id":10,"result":unavailable()}));
    f.empty();
    assert_eq!(f.view()["state"], 3);
    assert_eq!(f.view()["canonicalUpdated"], true);
}
