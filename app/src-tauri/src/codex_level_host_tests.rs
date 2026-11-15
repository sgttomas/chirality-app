//! DEL-01-01, PRD V4-AUT-06: the level the Host writes in every start, resume, fork and turn start, from the
//! level in force when the frame is built, bound to the request and kept with it.
use super::*;
use crate::codex_level::{self as cl, Method, Target};

const FOUR: [&str; 4] = ["thread/start", "thread/resume", "thread/fork", "turn/start"];

fn g() -> Value {
    json!({"appSession":"level-session","home":"level-home","spawnCounter":1})
}
fn ready(host: Host) -> Arc<Host> {
    let host = Arc::new(host);
    {
        let mut i = host.inner.0.lock().unwrap();
        i.state = "ready".into();
        i.generation = g();
        i.journal.begin_generation(g());
        i.threads.push(json!({"generation":g(),"threadId":"thread","cwd":"/invented","model":"selected","modelProvider":"selected-provider"}));
    }
    host
}
fn host() -> Arc<Host> {
    ready(Host::new())
}
fn admit_thread(host: &Host, thread: &str) {
    host.inner.0.lock().unwrap().threads.push(json!({"generation":g(),"threadId":thread,"cwd":"/invented","model":"selected","modelProvider":"selected-provider"}));
}
fn text() -> Value {
    json!([{"type":"text","text":"invented","text_elements":[]}])
}
/// The params each method is built with, before any level.
fn built(method: &str) -> Value {
    match method {
        "thread/start" => json!({"cwd":"/invented","model":"selected","modelProvider":"selected-provider"}),
        "thread/resume" => json!({"threadId":"thread","excludeTurns":true}),
        "thread/fork" => json!({"threadId":"thread","deferGoalContinuation":true}),
        "turn/start" => json!({"threadId":"thread","input":text()}),
        _ => unreachable!(),
    }
}
/// The expected wire params, written out field by field from the level table rather than through `merge`.
fn with_fields(built: &Value, level: &cl::Level, method: Method) -> Value {
    let mut out = built.clone();
    out["approvalPolicy"] = json!(level.approval_policy);
    out["approvalsReviewer"] = json!("user");
    match method {
        Method::TurnStart => out["sandboxPolicy"] = level.sandbox_policy.clone(),
        _ => {
            out["sandbox"] = json!(level.sandbox);
            if out.get("config").is_none() {
                out["config"] = json!({});
            }
            if let Some(options) = &level.workspace_write {
                out["config"]["sandbox_workspace_write"] = options.clone();
            }
            // The one trust entry: this test Host makes no settings reading, so it is untrusted, for the project root of
            // the conversation's folder (`/invented`, the test Host's working folder, where nothing names another).
            out["config"]["projects"] = untrusted();
        }
    }
    out
}
fn untrusted() -> Value {
    json!({"/invented": {"trust_level": "untrusted"}})
}
/// What the Host adds to `method`'s params at `level` in these tests.
fn added(level: &cl::Level, method: Method) -> serde_json::Map<String, Value> {
    cl::additions(level, method, Some(&untrusted()))
}
fn level(id: &str) -> &'static cl::Level {
    cl::level(id).unwrap()
}
fn send(host: &Host, method: &str, params: Value) -> Result<SourceRequest, String> {
    host.request_begin_scoped(method, params, json!({"kind":"person-directed"}), false, Some(&g()))
}
/// What a refusal must leave untouched: no id reserved, nothing recorded, pending or written.
fn counts(host: &Host) -> (u64, usize, usize, usize, u64) {
    let i = host.inner.0.lock().unwrap();
    (i.next_id, i.source_requests.len(), i.client_requests.len(), i.pending.len(), i.send_position)
}
fn reply(host: &Host, frame: Value) {
    host.on_line(&serde_json::to_vec(&frame).unwrap(), &g());
}
fn turn(status: &str) -> Value {
    json!({"id":"turn","status":status,"items":[],"itemsView":"full","nativeExtra":{"unchanged":true}})
}

/// A stand-in for Codex's input: every frame the Host writes, in order.
struct Wire {
    child: std::process::Child,
    frames: Receiver<Value>,
}
impl Wire {
    fn attach(host: &Host) -> Self {
        let mut child = Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let stdout = child.stdout.take().unwrap();
        let (tx, rx) = channel();
        std::thread::spawn(move || {
            let mut reader = BufReader::new(stdout);
            loop {
                let mut line = String::new();
                match reader.read_line(&mut line) {
                    Ok(0) | Err(_) => break,
                    Ok(_) => {
                        let _ = tx.send(serde_json::from_str::<Value>(&line).unwrap());
                    }
                }
            }
        });
        Wire { child, frames: rx }
    }
    fn next(&self) -> Value {
        self.frames.recv_timeout(Duration::from_secs(5)).expect("a frame was written")
    }
    fn nothing(&self) -> bool {
        self.frames.recv_timeout(Duration::from_millis(200)).is_err()
    }
    fn close(mut self, host: &Host) {
        *host.stdin.lock().unwrap() = None;
        assert!(self.child.wait().unwrap().success());
    }
}

#[test]
fn each_of_the_four_frames_carries_exactly_the_level() {
    for id in ["edits", "supervised", "full"] {
        let host = host();
        host.set_default_level(id).unwrap();
        let wire = Wire::attach(&host);
        for method in FOUR {
            let m = Method::of(method).unwrap();
            let source = send(&host, method, built(method)).unwrap();
            let written = wire.next();
            assert_eq!(written["method"], method);
            assert_eq!(written["params"], with_fields(&built(method), level(id), m), "{id} {method}");
            assert!(cl::carries_exactly_fields(&built(method), &written["params"], &added(level(id), m)));
            // The frame the Host keeps is the frame it wrote, level included.
            assert_eq!(source.attempted_frame(), &written);
            assert_eq!(source.evidence()["sentFrame"], written);
            assert_eq!(source.level_sent_id(), Some((id, m)));
            assert_eq!(source.level_sent().unwrap().fields, added(level(id), m));
        }
        wire.close(&host);
    }
}

#[test]
fn a_frame_that_would_carry_other_than_exactly_its_level_writes_nothing() {
    let host = host();
    let wire = Wire::attach(&host);
    type Tamper = fn(&mut Value);
    let tampers: [(&str, Tamper); 4] = [
        ("an extra field", |p| p["invented"] = json!(true)),
        ("a level field missing", |p| {
            p.as_object_mut().unwrap().remove("approvalsReviewer");
        }),
        ("a level field changed", |p| p["approvalPolicy"] = json!("never")),
        ("a built field changed", |p| p["model"] = json!("other")),
    ];
    for method in FOUR {
        for (what, tamper) in tampers {
            *host.after_level_merge.lock().unwrap() = Some(Box::new(move |p: &mut Value| tamper(p)));
            let before = counts(&host);
            let refused = send(&host, method, built(method)).err().unwrap();
            assert!(refused.contains("other than exactly its level"), "{method} {what}: {refused}");
            assert_eq!(counts(&host), before, "{method} {what}: nothing reserved, recorded or pending");
        }
    }
    assert!(wire.nothing(), "nothing written");
    // The check itself, apart from the Host.
    let edits = level("edits");
    let start = built("thread/start");
    let mut sent = with_fields(&start, edits, Method::ThreadStart);
    assert!(cl::carries_exactly_fields(&start, &sent, &added(edits, Method::ThreadStart)));
    sent["config"]["invented"] = json!(1);
    assert!(!cl::carries_exactly_fields(&start, &sent, &added(edits, Method::ThreadStart)), "an extra configuration key");
    assert!(!cl::carries_exactly_fields(&start, &with_fields(&start, level("full"), Method::ThreadStart), &added(edits, Method::ThreadStart)), "another level");
    wire.close(&host);
}

#[test]
fn with_no_level_chosen_the_four_are_refused_before_anything_is_written() {
    let host = ready(Host::new_without_level());
    let wire = Wire::attach(&host);
    for method in FOUR {
        assert_eq!(host.level_for(method, &built(method)), None);
        let before = counts(&host);
        let refused = send(&host, method, built(method)).err().unwrap();
        assert!(refused.contains("no level chosen"), "{method}: {refused}");
        assert_eq!(counts(&host), before, "{method}: nothing reserved, recorded or pending");
    }
    assert!(wire.nothing(), "nothing written");
    // A method that carries no level is sent as before.
    let read = send(&host, "thread/read", json!({"threadId":"thread","includeTurns":false})).unwrap();
    assert_eq!(wire.next()["params"], json!({"threadId":"thread","includeTurns":false}));
    assert!(read.level_sent().is_none());
    wire.close(&host);
}

#[test]
fn a_configuration_collision_refuses_and_the_childrens_configuration_survives() {
    let host = host();
    let wire = Wire::attach(&host);
    for method in ["thread/start", "thread/resume", "thread/fork"] {
        let mut params = built(method);
        params["config"] = json!({"sandbox_workspace_write":{"network_access":true}});
        let before = counts(&host);
        let refused = send(&host, method, params).err().unwrap();
        assert!(refused.contains("level field already present: config.sandbox_workspace_write"), "{method}: {refused}");
        assert_eq!(counts(&host), before);
    }
    // Params arriving with a level field already in them are refused: the level is their only source.
    for method in FOUR {
        for key in cl::LEVEL_KEYS {
            let mut params = built(method);
            params[key] = json!("invented");
            let refused = send(&host, method, params).err().unwrap();
            assert!(refused.contains(&format!("level field already present: {key}")), "{method} {key}: {refused}");
        }
    }
    assert!(wire.nothing());
    let children = json!({"agents.HELPER.description":"invented helper","agents.HELPER.config_file":"/invented/helper.toml"});
    for id in ["edits", "full"] {
        host.set_default_level(id).unwrap();
        let mut params = built("thread/start");
        params["config"] = children.clone();
        send(&host, "thread/start", params.clone()).unwrap();
        let written = wire.next();
        let config = written["params"]["config"].as_object().unwrap();
        for (key, value) in children.as_object().unwrap() {
            assert_eq!(config.get(key), Some(value), "{id}: {key} unchanged");
        }
        let mut want = children.clone();
        if let Some(options) = &level(id).workspace_write {
            want["sandbox_workspace_write"] = options.clone();
        }
        want["projects"] = untrusted();
        assert_eq!(written["params"]["config"], want, "{id}: the children's keys plus exactly the level's");
        assert_eq!(written["params"], with_fields(&params, level(id), Method::ThreadStart));
    }
    wire.close(&host);
}

#[test]
fn a_steer_an_interrupt_and_a_read_carry_no_level() {
    let host = host();
    let wire = Wire::attach(&host);
    reply(&host, json!({"method":"turn/started","params":{"threadId":"thread","turn":turn("inProgress")}}));
    let cases = [
        ("turn/steer", json!({"threadId":"thread","expectedTurnId":"turn","input":text()})),
        ("turn/interrupt", json!({"threadId":"thread","turnId":"turn"})),
        ("thread/read", json!({"threadId":"thread","includeTurns":false})),
    ];
    for (method, params) in cases {
        assert_eq!(host.level_for(method, &params), None);
        let source = send(&host, method, params.clone()).unwrap();
        let written = wire.next();
        assert_eq!(written["method"], method);
        assert_eq!(written["params"], params, "{method}: exactly as built");
        assert!(source.level_sent().is_none());
    }
    wire.close(&host);
}

#[test]
fn a_conversations_own_choice_beats_the_default_for_its_turns_resumes_and_forks() {
    let host = host();
    let wire = Wire::attach(&host);
    host.set_thread_level("thread", "supervised").unwrap();
    for method in FOUR {
        let want = if method == "thread/start" { "edits" } else { "supervised" };
        assert_eq!(host.level_for(method, &built(method)).map(|l| l.id.as_str()), Some(want), "{method}");
        let source = send(&host, method, built(method)).unwrap();
        assert_eq!(wire.next()["params"], with_fields(&built(method), level(want), Method::of(method).unwrap()), "{method}");
        assert_eq!(source.level_sent().unwrap().level.id, want);
    }
    // Another conversation without a choice takes the default.
    admit_thread(&host, "other");
    let params = json!({"threadId":"other","input":text()});
    send(&host, "turn/start", params.clone()).unwrap();
    assert_eq!(wire.next()["params"], with_fields(&params, level("edits"), Method::TurnStart));
    wire.close(&host);
}

#[test]
fn a_production_host_has_no_level() {
    // `Host::new` is `new_without_level` in every build but `cfg(test)`, where it alone adds "edits".
    let host = Host::new_without_level();
    {
        let i = host.inner.0.lock().unwrap();
        assert!(i.default_level.is_none());
        assert!(i.thread_levels.is_empty());
        assert!(i.new_conversation_level.is_none());
    }
    assert_eq!(host.default_level(), None);
    for method in FOUR {
        assert_eq!(host.level_for(method, &built(method)), None, "{method}");
    }
    assert_eq!(Host::new().default_level().map(|l| l.id.as_str()), Some("edits"));
    assert!(host.set_default_level("invented").is_err(), "only a level of the table can be chosen");
    assert_eq!(host.default_level(), None);
}

#[test]
fn the_local_checks_still_refuse_keys_that_are_neither_children_nor_level() {
    use crate::native_local_provider::{LocalSettings, PROVIDER};
    let host = Host::new();
    let generation = json!({"appSession":"level-local","home":"local-level-home","spawnCounter":1});
    let model = LocalSettings::legacy().model().to_owned();
    {
        let mut i = host.inner.0.lock().unwrap();
        i.state = "ready".into();
        i.generation = generation.clone();
        i.version_identity = Some(json!({"declaredPin":"0.167.0","distributionContentIdentity":[{"path":"bin/codex","identity":{"algorithm":"sha-256","value":"030316ecfbb41f4e7946e584b0063ef333b7a36cd312ba349f2f6869e39b62cc"}}]}));
        i.successor_status = Some(json!({"verificationGeneration":generation,"inventory":{"manifest_sha256":"158dd67072236253a694ca06d9bf7bfdebbe20d4a197bbf675433cbdddea7e7b"}}));
        i.threads.push(json!({"generation":generation,"threadId":"thread","model":model,"modelProvider":PROVIDER}));
        i.local_provider = Some(access_provider::LocalProviderBinding::for_test("local-level-home", "/invented/work"));
    }
    let source = SourceRequest { source: std::sync::Weak::new(), generation: generation.clone(), frame: json!({"id":0}), level: None, request_ref: "invented-reading".into(), receiver: Arc::new(Mutex::new(channel().1)) };
    let proof = ProviderAdmission::local_for_test(source, "/invented/work", &model);
    let check = |method: &str, params: &Value| {
        let i = host.inner.0.lock().unwrap();
        Host::check_local_request(&i, method, params, Some(&generation), false, false, false, Some(&proof))
    };
    let start = json!({"cwd":"/invented/work","modelProvider":PROVIDER,"model":model});
    let resume = json!({"threadId":"thread","excludeTurns":true,"cwd":"/invented/work"});
    let fork = json!({"threadId":"thread","deferGoalContinuation":true,"cwd":"/invented/work"});
    for (method, params) in [("thread/start", &start), ("thread/resume", &resume), ("thread/fork", &fork)] {
        assert!(check(method, params).is_ok(), "{method}: the packet as built passes");
        // A resume or fork is exactly its three keys; a start's configuration is exactly its children's (below).
        let mut extra = params.clone();
        if method == "thread/start" { extra["config"] = json!({"invented_key":true}); } else { extra["invented"] = json!(true); }
        assert!(check(method, &extra).is_err(), "{method}: a key that is neither children nor level is refused");
        // The check sees the params as built: level fields arriving in them are refused there too.
        let leveled = with_fields(params, level("edits"), Method::of(method).unwrap());
        assert!(check(method, &leveled).is_err(), "{method}: level fields in the params as built are refused");
    }
    let mut configured = start.clone();
    configured["config"] = json!({"agents.HELPER.description":"invented"});
    assert!(check("thread/start", &configured).is_err(), "children keys with no prepared children are refused too");
}

#[test]
fn a_later_check_uses_the_level_bound_to_the_frame() {
    let host = host();
    let wire = Wire::attach(&host);
    let params = json!({"threadId":"thread","input":text(),"clientUserMessageId":"client-1"});
    let source = send(&host, "turn/start", params.clone()).unwrap();
    let written = wire.next();
    reply(&host, json!({"id":written["id"],"result":{"turn":turn("inProgress")}}));
    host.set_default_level("supervised").unwrap();
    host.set_thread_level("thread", "full").unwrap();
    let now = host.level_for("turn/start", &params).unwrap();
    assert_ne!(cl::expected_with_level(&params, Some(now), Method::TurnStart).unwrap(), written["params"], "the level in force now differs");
    let positive = host.positive_text_start(&g(), &written["id"], "thread", &["invented"], "client-1");
    assert!(positive.is_ok(), "the check holds against the level the frame carried: {:?}", positive.err());
    assert_eq!(source.level_sent().unwrap().level.id, "edits");
    wire.close(&host);
}

#[test]
fn a_frame_built_before_a_level_change_is_not_written_after_it() {
    // Evidence: the level revision bound to the frame at its build (`Bound::revision`), checked against the
    // Host's revision at the final admission, with the frame writer held (`Host::check_level_current`).
    for method in FOUR {
        let host = host();
        let wire = Wire::attach(&host);
        for change in ["default", "conversation", "new-conversation"] {
            let serial = host.frame_write.lock().unwrap();
            let before = host.inner.0.lock().unwrap().source_requests.len();
            let sender = Arc::clone(&host);
            let pending = std::thread::spawn(move || send(&sender, method, built(method)));
            let deadline = std::time::Instant::now() + Duration::from_secs(5);
            while host.inner.0.lock().unwrap().source_requests.len() == before {
                assert!(std::time::Instant::now() < deadline, "{method}: the frame was built and registered");
                std::thread::yield_now();
            }
            match change {
                "default" => host.set_default_level("supervised").unwrap(),
                "conversation" => host.set_thread_level("thread", "full").unwrap(),
                _ => host.choose_new_conversation_level(None).unwrap(),
            }
            drop(serial);
            // The request is returned with its refusal kept: no write attempt, nothing recorded as sent.
            let source = pending.join().unwrap().unwrap();
            let limit = host.inner.0.lock().unwrap().source_requests[&source.request_id().to_string()].source_limit.clone().unwrap_or_default();
            assert!(limit.contains("the level changed"), "{method} {change}: {limit}");
            assert!(source.evidence()["sentFrame"].is_null(), "{method} {change}");
            assert_eq!(source.write_attempt_observed(), Some(false), "{method} {change}");
            assert!(wire.nothing(), "{method} {change}: nothing written");
        }
        assert_eq!(host.inner.0.lock().unwrap().send_position, 0, "{method}");
        // A frame admitted after the changes carries the level now in force for its conversation.
        let want = if method == "thread/start" { "supervised" } else { "full" };
        send(&host, method, built(method)).unwrap();
        assert_eq!(wire.next()["params"], with_fields(&built(method), level(want), Method::of(method).unwrap()), "{method}");
        wire.close(&host);
    }
}

#[test]
fn each_frame_carries_its_intended_conversations_level_and_never_anothers() {
    // Evidence: the conversation the frame is for (`threadId`, or the start or fork that creates one) and the
    // person's choice for it, read once under the registration lock (`Host::resolve_level`).
    for method in FOUR {
        let host = host();
        let wire = Wire::attach(&host);
        // The default is "edits"; the intended conversation's own choice differs, and so does the other one.
        let (intended, other) = match method {
            // A start: the choice for the conversation it creates, not the default.
            "thread/start" => { host.choose_new_conversation_level(Some("supervised")).unwrap(); ("supervised", "edits") }
            // A fork: the new conversation's choice, not its source's.
            "thread/fork" => { host.set_thread_level("thread", "full").unwrap(); host.choose_new_conversation_level(Some("supervised")).unwrap(); ("supervised", "full") }
            // A resume or turn: the conversation's own choice, not the default.
            _ => { host.set_thread_level("thread", "supervised").unwrap(); ("supervised", "edits") }
        };
        let m = Method::of(method).unwrap();
        send(&host, method, built(method)).unwrap();
        let written = wire.next()["params"].clone();
        assert_eq!(written, with_fields(&built(method), level(intended), m), "{method}: the intended conversation's level");
        assert_ne!(written, with_fields(&built(method), level(other), m), "{method}: another conversation's level does not match");
        assert!(!cl::carries_exactly_fields(&built(method), &written, &added(level(other), m)), "{method}");
        wire.close(&host);
    }
}

/// The attachment turn's builder (`prepare_attachment_turn_led`), the second place a frame is built.
fn attachment() -> (std::path::PathBuf, Arc<AttachmentCustody>, Vec<SelectedTextAttachment>) {
    let root = std::env::temp_dir().join(opaque_id("level-attachment-").unwrap());
    std::fs::create_dir(&root).unwrap();
    let root = root.canonicalize().unwrap();
    let owner = Arc::new(AttachmentCustody::open(&root.join("app"), &root.join("codex")).unwrap());
    let path = root.join("invented.txt");
    std::fs::write(&path, "invented bytes").unwrap();
    (root.clone(), owner, vec![SelectedTextAttachment::from_native_selection(path, None).unwrap()])
}

#[test]
fn the_attachment_turn_carries_exactly_its_level_and_is_refused_without_or_after_a_change() {
    // (a) the valid case: the prepared frame carries exactly the level, and the frame written is that frame.
    let host = host();
    let (root, owner, selections) = attachment();
    let wire = Wire::attach(&host);
    let prepared = host.prepare_attachment_turn(Arc::clone(&owner), &g(), "thread", None, "invented", &selections).unwrap();
    assert_eq!(prepared.source().attempted_frame()["params"], with_fields(&prepared.built, level("edits"), Method::TurnStart));
    assert_eq!(prepared.source().level_sent_id(), Some(("edits", Method::TurnStart)));
    host.dispatch_attachment_turn(&prepared).unwrap();
    assert_eq!(&wire.next(), prepared.source().attempted_frame());
    // (d) the conversation's own choice, not the default.
    host.set_thread_level("thread", "supervised").unwrap();
    let chosen = host.prepare_attachment_turn(Arc::clone(&owner), &g(), "thread", None, "invented", &selections).unwrap();
    assert_eq!(chosen.source().attempted_frame()["params"], with_fields(&chosen.built, level("supervised"), Method::TurnStart));
    // (c) a change between preparation and dispatch: refused, nothing written.
    host.set_default_level("full").unwrap();
    let refused = host.dispatch_attachment_turn(&chosen).err().unwrap();
    assert!(refused.contains("the level changed"), "{refused}");
    assert!(chosen.source().evidence()["sentFrame"].is_null());
    assert!(wire.nothing());
    wire.close(&host);
    // (b) no level: refused at preparation, nothing reserved or recorded.
    let unleveled = ready(Host::new_without_level());
    let wire = Wire::attach(&unleveled);
    let before = counts(&unleveled);
    let none = unleveled.prepare_attachment_turn(Arc::clone(&owner), &g(), "thread", None, "invented", &selections).err().unwrap();
    assert!(none.contains("no level chosen"), "{none}");
    assert_eq!(counts(&unleveled), before);
    assert!(wire.nothing());
    wire.close(&unleveled);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_start_takes_the_new_conversations_choice_and_the_reply_keeps_it() {
    let host = host();
    let wire = Wire::attach(&host);
    host.choose_new_conversation_level(Some("supervised")).unwrap();
    assert_eq!(host.level_for("thread/start", &json!({})).unwrap().id, "supervised");
    assert_eq!(host.level_for("turn/start", &built("turn/start")).unwrap().id, "edits", "the default is unchanged");
    let source = send(&host, "thread/start", built("thread/start")).unwrap();
    let written = wire.next();
    assert_eq!(written["params"], with_fields(&built("thread/start"), level("supervised"), Method::ThreadStart));
    assert_eq!(source.level_sent().unwrap().target, Target::New);
    assert_eq!(host.level_for("thread/start", &json!({})).unwrap().id, "edits", "the choice is taken by the start it was bound to");
    reply(&host, json!({"id":written["id"],"result":{"thread":{"id":"created"}}}));
    assert_eq!(host.thread_level("created").unwrap().id, "supervised", "the created conversation keeps the level sent");
    // Never the default reread at the reply, nor later.
    host.set_default_level("full").unwrap();
    admit_thread(&host, "created");
    let params = json!({"threadId":"created","input":text()});
    send(&host, "turn/start", params.clone()).unwrap();
    assert_eq!(wire.next()["params"], with_fields(&params, level("supervised"), Method::TurnStart));
    // An error reply records nothing.
    let refused = send(&host, "thread/start", built("thread/start")).unwrap();
    reply(&host, json!({"id":refused.request_id(),"error":{"code":-1,"message":"invented"}}));
    wire.next();
    assert_eq!(host.inner.0.lock().unwrap().thread_levels.len(), 1);
    wire.close(&host);
}

#[test]
fn a_fork_binds_the_new_conversations_level_not_its_sources() {
    let host = host();
    let wire = Wire::attach(&host);
    host.set_thread_level("thread", "supervised").unwrap();
    host.choose_new_conversation_level(Some("edits-network")).unwrap();
    let source = send(&host, "thread/fork", built("thread/fork")).unwrap();
    let written = wire.next();
    assert_eq!(written["params"], with_fields(&built("thread/fork"), level("edits-network"), Method::ThreadFork));
    assert_eq!(source.level_sent().unwrap().target, Target::ForkOf("thread".into()));
    reply(&host, json!({"id":written["id"],"result":{"thread":{"id":"forked","forkedFromId":"thread"}}}));
    assert_eq!(host.thread_level("forked").unwrap().id, "edits-network");
    assert_eq!(host.thread_level("thread").unwrap().id, "supervised", "the source keeps its own");
    // Without a choice, a fork takes its source's level, and the new conversation keeps what was sent.
    let again = send(&host, "thread/fork", built("thread/fork")).unwrap();
    let written = wire.next();
    assert_eq!(written["params"], with_fields(&built("thread/fork"), level("supervised"), Method::ThreadFork));
    reply(&host, json!({"id":again.request_id(),"result":{"thread":{"id":"forked-again"}}}));
    host.set_thread_level("thread", "full").unwrap();
    assert_eq!(host.thread_level("forked-again").unwrap().id, "supervised");
    wire.close(&host);
}
