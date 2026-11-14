//! DEL-01-05: plugins and connected apps are read for display before every conversation start,
//! resume and fork, on the request's own generation, and the reading never refuses the request.
use super::*;
use super::extensions::*;
use std::io::{BufRead, BufReader};

fn g() -> Value { json!({"appSession":"extensions-session","home":"extensions-home","spawnCounter":1}) }
fn entry(name: &str, enabled: bool) -> Value { json!({"name":name,"enabled":enabled,"defaultEnabled":false,"stage":"stable"}) }
fn off() -> Vec<Value> { vec![entry("plugins", false), entry("apps", false), entry("memories", true)] }
fn origin(layer: &str) -> Value { json!({"name":{"type":layer},"version":"invented-version"}) }

/// One answer to the reading.
#[derive(Clone)]
enum Answer { Entries(Vec<Value>), Error, Silent, Endless, Result(Value) }

/// A ready Host whose input is an echo double: the reader thread collects every frame written and
/// answers a conversation request as Codex would; the hook answers the reading with `answer`.
struct Run { host: Arc<Host>, written: Arc<Mutex<Vec<Value>>>, child: std::process::Child, reader: Option<std::thread::JoinHandle<()>> }
impl Run {
    fn new(answer: Answer) -> Self {
        let host = Arc::new(Host::new());
        { let mut i = host.inner.0.lock().unwrap(); i.generation = g(); i.journal.begin_generation(g()); i.state = "ready".into(); i.supplier_standing = Some("unverified-development".into()); i.feature_read_wait = Some(Duration::from_millis(300)); }
        let pages = Arc::new(Mutex::new(0usize));
        *host.feature_read_reply.lock().unwrap() = Some(Box::new(move |host, source| {
            let reply = |result: Value| json!({"id": source.request_id(), "result": result});
            let frame = match &answer {
                Answer::Entries(entries) => reply(json!({"data": entries, "nextCursor": null})),
                Answer::Error => json!({"id": source.request_id(), "error": {"code": -32603, "message": "invented failure"}}),
                Answer::Silent => return,
                Answer::Endless => { let mut n = pages.lock().unwrap(); *n += 1; reply(json!({"data": [], "nextCursor": format!("page-{n}")})) }
                Answer::Result(result) => reply(result.clone()),
            };
            host.on_line(&serde_json::to_vec(&frame).unwrap(), source.generation());
        }));
        let mut child = std::process::Command::new("/bin/cat").env_clear().stdin(std::process::Stdio::piped()).stdout(std::process::Stdio::piped()).stderr(std::process::Stdio::null()).spawn().unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let stdout = child.stdout.take().unwrap();
        let written = Arc::new(Mutex::new(Vec::new()));
        let (me, seen) = (Arc::clone(&host), Arc::clone(&written));
        let reader = std::thread::spawn(move || {
            for line in BufReader::new(stdout).lines() {
                let Ok(line) = line else { break };
                let frame: Value = serde_json::from_str(&line).unwrap();
                seen.lock().unwrap().push(frame.clone());
                if extensions::loads_conversation(frame["method"].as_str().unwrap_or("")) {
                    let generation = me.snapshot()["generation"].clone();
                    let reply = json!({"id":frame["id"],"result":{"thread":{"id":"started","status":"idle"},"model":"m","modelProvider":"p","cwd":"/invented/work"}});
                    me.on_line(&serde_json::to_vec(&reply).unwrap(), &generation);
                }
            }
        });
        Run { host, written, child, reader: Some(reader) }
    }
    fn start(&self) -> Result<Value, String> { self.host.thread_start_selected("/invented/work", "m", "p") }
    /// A requirements reading of this generation answered with `requirements`, as the account view makes one.
    fn requirements_read(&self, requirements: Value) {
        let source = self.host.request_begin_scoped("configRequirements/read", json!({}), json!({"kind":"person-directed"}), false, Some(&g())).unwrap();
        self.host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"result":{"requirements":requirements}})).unwrap(), &g());
        self.host.source_request_wait(&source, Duration::from_secs(1)).unwrap();
    }
    fn finish(mut self) -> (Vec<String>, Value) {
        *self.host.stdin.lock().unwrap() = None;
        self.child.wait().unwrap();
        self.reader.take().unwrap().join().unwrap();
        let methods = self.written.lock().unwrap().iter().map(|f| f["method"].as_str().unwrap_or("").to_owned()).collect();
        (methods, self.host.snapshot())
    }
}

#[test]
fn the_reading_comes_first_on_its_generation_and_is_shown_without_holding_back_the_start() {
    let run = Run::new(Answer::Entries(off()));
    assert_eq!(run.start().unwrap()["result"]["thread"]["id"], "started");
    let (methods, status) = run.finish();
    assert_eq!(methods, ["experimentalFeature/list", "thread/start"]);
    let shown = &status["extensions"];
    assert_eq!((&shown["generation"], shown["request"].as_str()), (&g(), Some("thread/start")));
    for feature in ["plugins", "apps"] {
        assert_eq!((shown[feature]["state"].as_str(), shown[feature]["source"].as_str(), &shown[feature]["notReadBecause"]), (Some("off"), Some("not-established"), &Value::Null), "{feature}: no evidence of where it comes from");
        assert!(shown[feature]["readAt"].as_str().is_some_and(|t| t.ends_with('Z')));
    }
    assert_eq!(shown["evidence"], json!({"origins":"none","requirements":"none"}));
    let read = status["clientRequests"].as_array().unwrap().iter().find(|r| r["method"] == "experimentalFeature/list").unwrap().clone();
    assert_eq!((&read["initiator"], &read["generation"]), (&json!({"kind":"app-rule","name":"feature-state-read"}), &g()));
}

#[test]
fn each_feature_reads_on_off_or_not_read_and_nothing_is_refused() {
    let endless = Answer::Endless;
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
        ("endless pages", endless, ("not-read", Some("page-limit")), ("not-read", Some("page-limit"))),
        ("data not a list", Answer::Result(json!({"data":{"plugins":false},"nextCursor":null})), ("not-read", Some("malformed-reply")), ("not-read", Some("malformed-reply"))),
        ("cursor not text", Answer::Result(json!({"data":off(),"nextCursor":7})), ("not-read", Some("malformed-reply")), ("not-read", Some("malformed-reply"))),
    ];
    for (case, answer, plugins, apps) in cases {
        let endless_case = matches!(answer, Answer::Endless);
        let run = Run::new(answer);
        assert!(run.start().is_ok(), "{case}: the start is sent and answered whatever the reading");
        let (methods, status) = run.finish();
        assert_eq!(methods.iter().filter(|m| *m == "thread/start").count(), 1, "{case}: {methods:?}");
        assert_eq!(methods.iter().filter(|m| *m == "experimentalFeature/list").count(), if endless_case { FEATURE_PAGE_LIMIT } else { 1 }, "{case}: the page bound holds");
        let shown = &status["extensions"];
        for (feature, (state, because)) in [("plugins", plugins), ("apps", apps)] {
            assert_eq!((shown[feature]["state"].as_str(), shown[feature]["notReadBecause"].as_str()), (Some(state), because), "{case}: {feature}");
        }
    }
}

#[test]
fn pages_are_followed_to_the_last_and_read_together() {
    let run = Run::new(Answer::Entries(vec![]));
    *run.host.feature_read_reply.lock().unwrap() = Some(Box::new(|host, source| {
        let result = if source.frame["params"] == json!({}) { json!({"data":[entry("plugins", true)],"nextCursor":"second"}) }
            else { assert_eq!(source.frame["params"], json!({"cursor":"second"})); json!({"data":[entry("apps", false)],"nextCursor":null}) };
        host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"result":result})).unwrap(), source.generation());
    }));
    run.start().unwrap();
    let (methods, status) = run.finish();
    assert_eq!(methods, ["experimentalFeature/list", "experimentalFeature/list", "thread/start"]);
    assert_eq!((status["extensions"]["plugins"]["state"].as_str(), status["extensions"]["apps"]["state"].as_str()), (Some("on"), Some("off")));
}

/// A reading that is not answered within its bound holds the start back no longer.
#[test]
fn a_failed_reading_is_recorded_and_the_start_proceeds_within_the_bound() {
    let run = Run::new(Answer::Silent);
    let began = std::time::Instant::now();
    assert!(run.start().is_ok());
    assert!(began.elapsed() < Duration::from_secs(3), "{:?}", began.elapsed());
    let (methods, status) = run.finish();
    assert_eq!(methods, ["experimentalFeature/list", "thread/start"]);
    assert_eq!(status["extensions"]["apps"]["state"], "not-read");
}

#[test]
fn resume_and_fork_are_read_for_too() {
    for method in ["thread/resume", "thread/fork"] {
        let run = Run::new(Answer::Entries(vec![entry("plugins", true), entry("apps", true)]));
        run.host.request_inner_scoped(method, json!({"threadId":"saved"}), json!({"kind":"person-directed"}), Duration::from_millis(500), false, Some(&g())).unwrap();
        let (methods, status) = run.finish();
        assert_eq!(methods, ["experimentalFeature/list", method], "{method}");
        assert_eq!((status["extensions"]["request"].as_str(), status["extensions"]["apps"]["state"].as_str()), (Some(method), Some("on")));
    }
}

/// The reading is bound to its generation: a request registered on another generation than the
/// one read on shows not read, and a reading of G1 is never shown for G2.
#[test]
fn a_reading_from_another_generation_is_shown_as_not_read() {
    let g2 = json!({"appSession":"extensions-session","home":"extensions-home","spawnCounter":2});
    let run = Run::new(Answer::Entries(off()));
    let replacement = g2.clone();
    *run.host.feature_read_reply.lock().unwrap() = Some(Box::new(move |host, source| {
        host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"result":{"data":off(),"nextCursor":null}})).unwrap(), source.generation());
        let mut i = host.inner.0.lock().unwrap(); Host::close_generation(&mut i); i.generation = replacement.clone(); i.journal.begin_generation(replacement.clone()); i.state = "ready".into();
    }));
    // A request naming no generation: read on G1, registered on G2.
    run.host.request_inner_scoped("thread/start", json!({"model":"m","modelProvider":"p"}), json!({"kind":"person-directed"}), Duration::from_millis(500), false, None).unwrap();
    let shown = run.host.snapshot()["extensions"].clone();
    assert_eq!(shown["generation"], g());
    for feature in ["plugins", "apps"] { assert_eq!((shown[feature]["state"].as_str(), shown[feature]["notReadBecause"].as_str()), (Some("not-read"), Some("generation-changed"))); }
    // A request still bound to G1 is neither read for nor sent.
    *run.host.feature_read_reply.lock().unwrap() = Some(Box::new(|_, _| panic!("no reading for a replaced generation")));
    assert!(run.host.request_inner_scoped("thread/start", json!({"model":"m","modelProvider":"p"}), json!({"kind":"person-directed"}), Duration::from_millis(300), false, Some(&g())).unwrap_err().contains("generation changed before request registration"));
    let (methods, _) = run.finish();
    assert_eq!(methods.iter().filter(|m| *m == "experimentalFeature/list").count(), 1);
}

/// Pins from the generation's latest requirements reading: a pinned feature is set outside the
/// App; with nothing pinned and no origin evidence, the source stays not established, because no
/// origins were read.
#[test]
fn a_pinned_requirement_shows_the_feature_set_outside_the_app() {
    let run = Run::new(Answer::Entries(vec![entry("plugins", false), entry("apps", true)]));
    run.requirements_read(json!({"featureRequirements":{"connectors":true}}));
    run.start().unwrap();
    let (_, status) = run.finish();
    let shown = &status["extensions"];
    assert_eq!((shown["apps"]["state"].as_str(), shown["apps"]["source"].as_str()), (Some("on"), Some("outside-app")), "connectors is a name for apps");
    assert_eq!(shown["plugins"]["source"], "not-established");
    assert_eq!(shown["evidence"]["requirements"], "latest-reading");
}

/// A requirements reading of another generation is no evidence for this one.
#[test]
fn a_requirements_reading_of_another_generation_is_not_used() {
    let run = Run::new(Answer::Entries(off()));
    run.requirements_read(json!({"featureRequirements":{"plugins":false}}));
    let g2 = json!({"appSession":"extensions-session","home":"extensions-home","spawnCounter":2});
    { let mut i = run.host.inner.0.lock().unwrap(); Host::close_generation(&mut i); i.generation = g2.clone(); i.journal.begin_generation(g2.clone()); i.state = "ready".into(); }
    run.start().unwrap();
    let (_, status) = run.finish();
    assert_eq!((status["extensions"]["generation"].clone(), status["extensions"]["plugins"]["source"].as_str()), (g2, Some("not-established")));
}

/// Every source from the evidence, and `connectors` prevailing over `apps`.
#[test]
fn each_source_follows_its_evidence() {
    use Feature::{Apps, Plugins};
    let nothing_pinned = json!({});
    let o = |pairs: &[(&str, &str)]| Value::Object(pairs.iter().map(|(k, l)| (k.to_string(), origin(l))).collect());
    // Pinned: outside the App, whatever the origin.
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "user")])), Some(&json!({"plugins":false}))), Source::OutsideApp);
    assert_eq!(source(Apps, None, Some(&json!({"connectors":true}))), Source::OutsideApp);
    // Origins by layer.
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "user")])), None), Source::ThisHome);
    assert_eq!(source(Plugins, Some(&o(&[("features.plugins", "project")])), None), Source::Project);
    for managed in ["mdm", "system", "enterpriseManaged", "legacyManagedConfigTomlFromFile", "legacyManagedConfigTomlFromMdm"] {
        assert_eq!(source(Plugins, Some(&o(&[("features.plugins", managed)])), Some(&nothing_pinned)), Source::OutsideApp, "{managed}");
    }
    for unnamed in ["sessionFlags", "packagedDefaults", "invented"] {
        assert_eq!(source(Plugins, Some(&o(&[("features.plugins", unnamed)])), Some(&nothing_pinned)), Source::NotEstablished, "{unnamed}");
    }
    // No origin: Codex's default only when nothing is pinned on a requirements reading.
    assert_eq!(source(Apps, Some(&o(&[("features.plugins", "user")])), Some(&nothing_pinned)), Source::Default);
    assert_eq!(source(Apps, Some(&o(&[])), None), Source::NotEstablished, "requirements not read");
    assert_eq!(source(Apps, None, Some(&nothing_pinned)), Source::NotEstablished, "origins not read");
    // `connectors` is applied after `apps`: its origin decides where both are present.
    assert_eq!(source(Apps, Some(&o(&[("features.apps", "user"), ("features.connectors", "mdm")])), Some(&nothing_pinned)), Source::OutsideApp);
    assert_eq!(source(Apps, Some(&o(&[("features.apps", "mdm"), ("features.connectors", "user")])), None), Source::ThisHome);
    assert_eq!(source(Apps, Some(&o(&[("features.apps", "project")])), None), Source::Project);
    // The state is never off when not read.
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
    // The account projection keeps these pins as values and nothing else of the feature requirements.
    let raw = json!({"jsonrpc":"2.0","id":1,"result":{"requirements":{"featureRequirements":{"plugins":true,"apps":"x","secret":true}}}});
    let (projected, _) = auth_rpc::project_frame(&raw, Some("configRequirements/read"));
    assert_eq!(projected["result"]["requirements"]["featureRequirements"], json!({"plugins":true,"apps":auth_rpc::REDACTED}));
}

/// The dedicated local home is not read for.
#[test]
fn the_local_home_is_not_read_for() {
    let host = Host::new();
    { let mut i = host.inner.0.lock().unwrap(); i.generation = g(); i.state = "ready".into(); i.local_provider = Some(access_provider::LocalProviderBinding::for_test("extensions-home", "/invented/work")); }
    *host.feature_read_reply.lock().unwrap() = Some(Box::new(|_, _| panic!("no reading in the local home")));
    assert_eq!(host.extensions_read("thread/start", Some(&g()), None), None);
    assert_eq!(host.snapshot()["extensions"], Value::Null);
}

/// A reading that cannot take the frame writer within its bound is not sent and holds nothing back:
/// the start then waits for the writer as any request does.
#[test]
fn a_held_writer_leaves_the_reading_unsent_within_its_bound() {
    let run = Run::new(Answer::Entries(off()));
    run.host.hold_frame_writer_for_test(Duration::from_millis(800));
    assert!(run.start().is_ok());
    let (methods, status) = run.finish();
    assert_eq!(methods, ["thread/start"]);
    for feature in ["plugins", "apps"] { assert_eq!(status["extensions"][feature]["notReadBecause"], "not-sent"); }
}
