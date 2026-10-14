use super::*;
use std::{
    io::{BufRead, BufReader},
    process::{Child, ChildStdout, Stdio},
    sync::Arc,
};
const CANARY: &str = "INVENTED_PRIVATE_PROVIDER_CANARY_481";
struct Peer {
    host: Arc<Host>,
    child: Child,
    wire: BufReader<ChildStdout>,
    g: Value,
}
impl Peer {
    fn new(home: &str) -> Self {
        Self::with_ledger(home, None)
    }
    fn with_ledger(home: &str, path: Option<std::path::PathBuf>) -> Self {
        let host = Arc::new(Host::new());
        if let Some(path) = path {
            host.configure_recovery(path).unwrap();
        }
        let session = host.inner.0.lock().unwrap().app_session.clone();
        let g = json!({"appSession":if session.is_empty(){"synthetic-access"}else{&session},"home":home,"spawnCounter":1});
        {
            let mut i = host.inner.0.lock().unwrap();
            i.generation = g.clone();
            i.state = "ready".into();
            i.supplier_standing = Some("synthetic; no provider contact".into());
        }
        let mut child = Command::new("/bin/cat")
            .env_clear()
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let wire = BufReader::new(child.stdout.take().unwrap());
        Self {
            host,
            child,
            wire,
            g,
        }
    }
    fn frame(&mut self) -> Value {
        let mut s = String::new();
        self.wire.read_line(&mut s).unwrap();
        serde_json::from_str(&s).unwrap()
    }
    fn answer(&self, result: Value) {
        *self.host.before_provider_wait.lock().unwrap() = Some(Box::new(move |host, source| {
            host.on_line(
                &serde_json::to_vec(&json!({"id":source.request_id(),"result":result})).unwrap(),
                source.generation(),
            );
            // This is before the private waiter consumes raw data. Concurrent public
            // snapshots/source evidence/capture journals already contain projection only.
            assert!(!host.snapshot().to_string().contains(CANARY));
            assert!(!source.evidence().to_string().contains(CANARY));
            assert!(!host.kept_replies().1.contains(CANARY));
        }));
    }
    fn read(&self, entry: &str, provider: &str) -> Result<ProviderAdmission, String> {
        self.host.provider_admission_read_within(
            &self.g,
            "/invented/work",
            entry,
            provider,
            "chosen-model",
            Duration::from_millis(30),
        )
    }
    fn safe(&self) {
        assert!(!self.host.snapshot().to_string().contains(CANARY));
        assert!(!self.host.kept_replies().1.contains(CANARY));
        assert!(!self
            .host
            .recorded_recovery_entries()
            .to_string()
            .contains(CANARY));
    }
}
impl Drop for Peer {
    fn drop(&mut self) {
        *self.host.stdin.lock().unwrap() = None;
        self.child.wait().unwrap();
    }
}
fn config(defs: Value) -> Value {
    json!({"config":{"model_provider":"different-default","model_providers":defs,"developer_instructions":CANARY},"origins":{}})
}
fn local() -> Value {
    json!({"name":"invented anonymous","base_url":"https://example.invalid/v1","wire_api":"responses","requires_openai_auth":false,"env_key":null,"auth":null,"aws":null,"gateway_oauth":null,"experimental_bearer_token":null,"http_headers":null,"env_http_headers":null,"query_params":null})
}
#[test]
fn access_provider_mislabeling_unknown_and_credential_elements_refuse_before_start() {
    let mut peer = Peer::new("account");
    let mut authenticated = local();
    authenticated["env_key"] = json!(CANARY);
    peer.answer(config(
        json!({"anonymous":local(),"auth-provider":authenticated}),
    ));
    for (entry, provider) in [
        ("chatgpt-account", "auth-provider"),
        ("api-key", "anonymous"),
        ("local-provider", "openai"),
        ("local-provider", "unknown"),
        ("local-provider", "auth-provider"),
    ] {
        let error = peer
            .read(entry, provider)
            .err()
            .expect("incompatible definition refused");
        assert!(!error.contains(CANARY));
        assert!(error.contains("no thread/start"));
        assert_eq!(peer.frame()["method"], "config/read");
        peer.safe();
    }
    let requests = peer.host.snapshot()["clientRequests"].clone();
    assert!(requests
        .as_array()
        .unwrap()
        .iter()
        .all(|r| r["method"] == "config/read"));
}
#[test]
fn access_provider_anonymous_nonloopback_and_builtin_controls_keep_exact_destination() {
    for (entry, provider, defs) in [
        ("local-provider", "anonymous", json!({"anonymous":local()})),
        ("chatgpt-account", "openai", json!({})),
        ("api-key", "openai", json!({})),
    ] {
        let mut peer = Peer::new(if entry == "api-key" { "key" } else { "account" });
        peer.answer(config(defs));
        let proof = peer.read(entry, provider).unwrap();
        let read = peer.frame();
        assert_eq!(
            read["params"],
            json!({"cwd":"/invented/work","includeLayers":true})
        );
        let receipt = peer
            .host
            .thread_start_with_access_dispatch(&proof, "synthetic guidance é")
            .unwrap();
        let sent = peer.frame();
        assert_eq!(sent["method"], "thread/start");
        assert_eq!(sent["params"]["cwd"], "/invented/work");
        assert_eq!(sent["params"]["modelProvider"], provider);
        assert_eq!(sent["params"]["model"], "chosen-model");
        assert_eq!(
            sent["params"]["developerInstructions"],
            "synthetic guidance é"
        );
        assert_eq!(receipt.evidence()["writeResult"], "written");
        peer.safe();
    }
}
#[test]
fn access_provider_shadowed_partial_unknown_transport_and_auth_maps_are_unavailable() {
    let mut fixtures = vec![(
        "chatgpt-account",
        "openai",
        config(json!({"openai":local()})),
    )];
    for (field, value) in [
        ("http_headers", json!({"Authorization":CANARY})),
        ("env_http_headers", json!({"api-key":CANARY})),
        ("query_params", json!({"access_token":CANARY})),
        ("http_headers", json!({"unknown-header":CANARY})),
        ("unknown-new-auth", json!(CANARY)),
        ("wire_api", json!("chat")),
        ("base_url", json!("file:///invented/file")),
        (
            "base_url",
            json!(format!("https://example.invalid/v1?api_key={CANARY}")),
        ),
    ] {
        let mut def = local();
        def[field] = value;
        fixtures.push((
            "local-provider",
            "anonymous",
            config(json!({"anonymous":def})),
        ));
    }
    fixtures.push((
        "local-provider",
        "anonymous",
        json!({"config":{},"origins":{}}),
    ));
    let mut partial = local();
    partial.as_object_mut().unwrap().remove("auth");
    fixtures.push((
        "local-provider",
        "anonymous",
        config(json!({"anonymous":partial})),
    ));
    for (entry, provider, result) in fixtures {
        let mut peer = Peer::new("home");
        peer.answer(result);
        assert!(peer.read(entry, provider).is_err());
        assert_eq!(peer.frame()["method"], "config/read");
        peer.safe();
    }
}
#[test]
fn access_provider_private_error_malformed_timeout_and_late_reply_never_publish_config() {
    for mode in ["error", "malformed", "timeout", "nonprotocol"] {
        let mut peer = Peer::new("home");
        let m = mode;
        *peer.host.before_provider_wait.lock().unwrap() = Some(Box::new(move |host, source| {
            if m == "error" {
                host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"error":{"code":-32000,"message":CANARY,"data":CANARY}})).unwrap(),source.generation());
            }
            if m == "malformed" {
                host.on_line(
                    &serde_json::to_vec(
                        &json!({"id":source.request_id(),"result":{"config":CANARY}}),
                    )
                    .unwrap(),
                    source.generation(),
                );
            }
            if m == "nonprotocol" {
                host.on_line(CANARY.as_bytes(), source.generation());
            }
            assert!(!host.snapshot().to_string().contains(CANARY));
            assert!(!source.evidence().to_string().contains(CANARY));
        }));
        let error = peer.read("local-provider", "anonymous").err().unwrap();
        assert!(!error.contains(CANARY));
        let read = peer.frame();
        peer.host.on_line(
            &serde_json::to_vec(
                &json!({"id":read["id"],"result":config(json!({"anonymous":local()}))}),
            )
            .unwrap(),
            &peer.g,
        );
        peer.safe();
        let i = peer.host.inner.0.lock().unwrap();
        let e = i.source_requests.get(&read["id"].to_string()).unwrap();
        assert!(
            e.request.receiver.lock().unwrap().try_recv().is_err()
                || e.response.as_ref().unwrap()["privateConfigWithheld"] == true
        );
    }
}
#[test]
fn access_provider_other_host_closed_replaced_and_changed_destination_do_not_start() {
    let mut peer = Peer::new("home-a");
    peer.answer(config(json!({})));
    let proof = peer.read("chatgpt-account", "openai").unwrap();
    peer.frame();
    let other = Peer::new("home-b");
    assert!(other
        .host
        .thread_start_with_access_dispatch(&proof, "guidance")
        .is_err());
    {
        let i = peer.host.inner.0.lock().unwrap();
        assert!(peer
            .host
            .check_provider_admission(
                &i,
                &proof,
                &json!({"cwd":"/other","model":"chosen-model","modelProvider":"openai"})
            )
            .is_err());
    }
    {
        let mut i = peer.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
        i.generation["spawnCounter"] = json!(2);
    }
    assert!(peer
        .host
        .thread_start_with_access_dispatch(&proof, "guidance")
        .is_err());
    assert_eq!(
        peer.host.snapshot()["clientRequests"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|r| r["method"] == "thread/start")
            .count(),
        0
    );
}
#[test]
fn access_provider_queued_start_rechecks_original_receipt_after_source_close() {
    let mut peer = Peer::new("home");
    peer.answer(config(json!({})));
    let proof = peer.read("chatgpt-account", "openai").unwrap();
    peer.frame();
    let held = peer.host.frame_write.lock().unwrap();
    let host = Arc::clone(&peer.host);
    let worker =
        std::thread::spawn(move || host.thread_start_with_access_dispatch(&proof, "guidance"));
    let deadline = std::time::Instant::now() + Duration::from_secs(2);
    loop {
        if peer
            .host
            .inner
            .0
            .lock()
            .unwrap()
            .source_requests
            .values()
            .any(|e| e.request.frame["method"] == "thread/start")
        {
            break;
        }
        assert!(std::time::Instant::now() < deadline);
        std::thread::sleep(Duration::from_millis(1));
    }
    {
        let mut i = peer.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
    }
    drop(held);
    let receipt = worker.join().unwrap().unwrap();
    assert_eq!(receipt.evidence()["actualWriteAttemptObserved"], false);
    assert!(receipt.evidence()["sentFrame"].is_null());
    assert_eq!(receipt.generation(), &peer.g);
    assert_eq!(receipt.attempted_frame()["params"]["model"], "chosen-model");
    assert_eq!(
        receipt.attempted_frame()["params"]["modelProvider"],
        "openai"
    );
    assert_eq!(receipt.attempted_frame()["params"]["cwd"], "/invented/work");
}
#[test]
fn access_provider_source_closed_during_private_read_cannot_mint_proof() {
    let mut peer = Peer::new("home");
    *peer.host.before_provider_wait.lock().unwrap() = Some(Box::new(|host, source| {
        host.on_line(
            &serde_json::to_vec(&json!({"id":source.request_id(),"result":config(json!({}))}))
                .unwrap(),
            source.generation(),
        );
        Host::close_generation(&mut host.inner.0.lock().unwrap());
    }));
    assert!(peer.read("chatgpt-account", "openai").is_err());
    assert_eq!(peer.frame()["method"], "config/read");
    peer.safe();
}
#[test]
fn access_provider_newer_same_source_folder_read_invalidates_older_admission() {
    let mut peer = Peer::new("home");
    peer.answer(config(json!({"anonymous":local()})));
    let old = peer.read("local-provider", "anonymous").unwrap();
    peer.frame();
    let mut changed = local();
    changed["http_headers"] = json!({"Authorization":CANARY});
    peer.answer(config(json!({"anonymous":changed})));
    assert!(peer.read("local-provider", "anonymous").is_err());
    peer.frame();
    assert!(peer
        .host
        .thread_start_with_access_dispatch(&old, "guidance")
        .is_err());
    peer.safe();
    peer.answer(json!({"config":{},"origins":{}}));
    assert!(peer.read("local-provider", "anonymous").is_err());
    peer.frame();
    assert!(peer
        .host
        .thread_start_with_access_dispatch(&old, "guidance")
        .is_err());
    peer.answer(config(json!({"anonymous":local()})));
    let new = peer.read("local-provider", "anonymous").unwrap();
    peer.frame();
    assert!(peer
        .host
        .thread_start_with_access_dispatch(&old, "guidance")
        .is_err());
    peer.host
        .thread_start_with_access_dispatch(&new, "guidance")
        .unwrap();
    assert_eq!(peer.frame()["method"], "thread/start");
}
#[test]
fn access_provider_actual_private_refusal_output_has_only_safe_public_consumers() {
    let root =
        std::path::PathBuf::from("/private/tmp").join(opaque_id("access-provider-test-").unwrap());
    let project = root.join("project");
    std::fs::create_dir_all(&project).unwrap();
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
        root: root.join("store"),
        placement: crate::records_store::Placement::Test,
        limits: vec![],
    })));
    let path = root.join("recovery.jsonl");
    let mut peer = Peer::with_ledger("home", Some(path.clone()));
    let mut authenticated = local();
    authenticated["experimental_bearer_token"] = json!(CANARY);
    peer.answer(config(json!({"authenticated":authenticated})));
    let refusal = peer.read("local-provider", "authenticated").err().unwrap();
    peer.frame();
    peer.safe();
    // This is the same maintained refusal publisher/quoted reader used by the
    // shared native Start/Continue-as/clean-trial wrapper. No person act claimed.
    let mut history = crate::runtime_session::HistorySession::default();
    history.configure_role_log(&project);
    let published = history.role_refused(
        "sup:synthetic-access-refusal",
        &peer.g,
        None,
        Some(false),
        &refusal,
        true,
    );
    assert_eq!(published["state"], "written");
    let quoted = history.read_role_supply("home", None);
    assert!(quoted["observations"].as_array().unwrap().len() > 0);
    let packet = json!({"refusal":refusal,"snapshot":peer.host.snapshot(),"recordedRecovery":peer.host.recorded_recovery_entries(),"roleSupplyRecord":published,"quotedRole":quoted});
    assert!(!packet.to_string().contains(CANARY));
    if let Ok(folder) = std::env::var("CHIRALITY_TEST_OUTPUT_DIRECTORY") {
        std::fs::write(
            std::path::Path::new(&folder).join("access-provider-private.json"),
            serde_json::to_vec_pretty(&packet).unwrap(),
        )
        .unwrap();
    }
    drop(peer);
    crate::records_store::use_store_for_test(None);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn access_provider_unrelated_folder_read_preserves_original_source_admission() {
    let mut peer = Peer::new("home");
    peer.answer(config(json!({"anonymous":local()})));
    let original = peer.read("local-provider", "anonymous").unwrap();
    peer.frame();
    peer.answer(json!({"config":{},"origins":{}}));
    assert!(peer
        .host
        .provider_admission_read_within(
            &peer.g,
            "/invented/other",
            "local-provider",
            "anonymous",
            "chosen-model",
            Duration::from_millis(30)
        )
        .is_err());
    assert_eq!(peer.frame()["params"]["cwd"], "/invented/other");
    peer.host
        .thread_start_with_access_dispatch(&original, "guidance")
        .unwrap();
    assert_eq!(peer.frame()["params"]["cwd"], "/invented/work");
}
#[test]
fn access_provider_delegation_config_read_invalidates_only_its_known_folder() {
    let mut peer = Peer::new("home");
    peer.answer(config(json!({})));
    let old = peer.read("chatgpt-account", "openai").unwrap();
    peer.frame();
    // This is the existing delegation transport, not a private admission read.
    let other = peer
        .host
        .request_begin_scoped(
            "config/read",
            json!({"includeLayers":false}),
            json!({"kind":"synthetic delegation"}),
            false,
            Some(&peer.g),
        )
        .unwrap();
    peer.frame();
    peer.host.on_line(
        &serde_json::to_vec(&json!({"id":other.request_id(),"result":{"config":{},"origins":{}}}))
            .unwrap(),
        &peer.g,
    );
    {
        let i = peer.host.inner.0.lock().unwrap();
        peer.host
            .check_provider_admission(
                &i,
                &old,
                &json!({"cwd":"/invented/work","modelProvider":"openai","model":"chosen-model"}),
            )
            .unwrap();
    }
    let newer = peer
        .host
        .request_begin_scoped(
            "config/read",
            json!({"cwd":"/invented/work","includeLayers":false}),
            json!({"kind":"synthetic delegation"}),
            false,
            Some(&peer.g),
        )
        .unwrap();
    peer.frame();
    peer.host.on_line(
        &serde_json::to_vec(&json!({"id":newer.request_id(),"result":{"config":{},"origins":{}}}))
            .unwrap(),
        &peer.g,
    );
    assert!(peer
        .host
        .thread_start_with_access_dispatch(&old, "guidance")
        .is_err());
}
#[test]
fn access_provider_malformed_objects_wrong_ids_and_correlated_envelopes_stay_private() {
    for mode in [
        "malformed-object",
        "wrong-id",
        "method-present",
        "contradictory",
        "wrong-known-id",
    ] {
        let mut peer = Peer::new("home");
        let m = mode;
        *peer.host.before_provider_wait.lock().unwrap() = Some(Box::new(move |host, source| {
            let frame = match m {
                "malformed-object" => json!({"unattributed":CANARY}),
                "wrong-id" => json!({"id":900000,"result":config(json!({"anonymous":local()}))}),
                "method-present" => {
                    json!({"id":source.request_id(),"method":"invented/malformed","params":{"secret":CANARY},"result":config(json!({"anonymous":local()}))})
                }
                "contradictory" => {
                    json!({"id":source.request_id(),"result":config(json!({"anonymous":local()})),"error":{"code":-32000,"message":CANARY}})
                }
                _ => {
                    let other = host
                        .request_begin_scoped(
                            "model/list",
                            json!({}),
                            json!({"kind":"synthetic other"}),
                            false,
                            Some(source.generation()),
                        )
                        .unwrap();
                    json!({"id":other.request_id(),"result":config(json!({"anonymous":local()}))})
                }
            };
            host.on_line(&serde_json::to_vec(&frame).unwrap(), source.generation());
            assert!(!host.snapshot().to_string().contains(CANARY));
            assert!(!source.evidence().to_string().contains(CANARY));
            assert!(!host.kept_replies().1.contains(CANARY));
        }));
        assert!(peer.read("local-provider", "anonymous").is_err());
        assert_eq!(peer.frame()["method"], "config/read");
        if mode == "wrong-known-id" {
            assert_eq!(peer.frame()["method"], "model/list");
        }
        peer.safe();
        let i = peer.host.inner.0.lock().unwrap();
        assert!(i
            .source_requests
            .values()
            .filter(|e| e.private_config)
            .all(|e| e
                .response
                .as_ref()
                .is_none_or(|r| r.get("result").is_none())));
    }
}
#[test]
fn access_provider_client_server_id_collision_preserves_actual_request_and_reply() {
    let mut peer = Peer::new("home");
    peer.host.inner.0.lock().unwrap().declared_capabilities = Some(json!({"experimentalApi":true}));
    *peer.host.before_provider_wait.lock().unwrap() = Some(Box::new(|host, source| {
        host.on_line(
            &serde_json::to_vec(
                &json!({"id":source.request_id(),"method":"currentTime/read","params":{}}),
            )
            .unwrap(),
            source.generation(),
        );
        {
            let i = host.inner.0.lock().unwrap();
            assert!(i.source_requests[&source.request_id().to_string()]
                .response
                .is_none());
            assert_eq!(i.server_requests.entries().len(), 1);
        }
        host.on_line(
            &serde_json::to_vec(&json!({"id":source.request_id(),"result":config(json!({}))}))
                .unwrap(),
            source.generation(),
        );
    }));
    let proof = peer.read("chatgpt-account", "openai").unwrap();
    let read = peer.frame();
    assert_eq!(read["method"], "config/read");
    let reply = peer.frame();
    assert_eq!(reply["id"], read["id"]);
    assert!(reply["result"]["currentTimeAt"].as_u64().is_some());
    let server = peer.host.snapshot()["serverRequests"].clone();
    assert_eq!(server[0]["method"], "currentTime/read");
    assert_eq!(server[0]["replyWriteResult"], "written");
    peer.host
        .thread_start_with_access_dispatch(&proof, "guidance")
        .unwrap();
    assert_eq!(peer.frame()["method"], "thread/start");
    peer.safe();
}
#[test]
fn access_provider_known_metadata_field_shapes_cannot_hide_modeled_malformed_data() {
    // Modeled malformed supplier data, not a live supplier or credential-bypass witness.
    for (field, value) in [
        ("name", json!({"private":CANARY})),
        ("name", Value::Null),
        ("env_key_instructions", json!([CANARY])),
        ("model_catalog_url", json!({"private":CANARY})),
        ("request_max_retries", json!(-1)),
        ("request_max_retries", json!(1.5)),
        ("stream_max_retries", json!({"private":CANARY})),
        ("stream_idle_timeout_ms", json!([CANARY])),
        ("websocket_connect_timeout_ms", json!(false)),
        ("supports_websockets", json!({"private":CANARY})),
        ("supports_standalone_web_search", Value::Null),
        ("http_headers", json!({"Accept":{"private":CANARY}})),
        ("env_key", json!({"private":CANARY})),
        ("aws", json!([CANARY])),
    ] {
        let mut peer = Peer::new("home");
        let mut def = local();
        def[field] = value;
        peer.answer(config(json!({"anonymous":def})));
        assert!(peer.read("local-provider", "anonymous").is_err());
        peer.frame();
        peer.safe();
    }
    let mut peer = Peer::new("home");
    let mut def = local();
    def["env_key_instructions"] = Value::Null;
    def["request_max_retries"] = json!(0);
    def["stream_max_retries"] = json!(u64::MAX);
    def["stream_idle_timeout_ms"] = Value::Null;
    def["websocket_connect_timeout_ms"] = json!(1000);
    def["supports_websockets"] = json!(false);
    def["supports_standalone_web_search"] = json!(false);
    peer.answer(config(json!({"anonymous":def})));
    peer.read("local-provider", "anonymous").unwrap();
    peer.frame();
    peer.safe();
}
