use super::*;
use std::{
    io::{BufRead, BufReader},
    process::{Child, ChildStdout, Stdio},
    sync::Arc,
};
const CANARY: &str = "INVENTED_PRIVATE_PROVIDER_CANARY_481";
#[test]
fn access_provider_endpoint_generic_write_cannot_mint_private_context_or_send() {
    let peer = Peer::new("invented-home");
    for method in ["config/batchWrite", "config/value/write"] {
        assert!(peer
            .host
            .request(
                method,
                json!({"expectedVersion":CANARY,"filePath":CANARY,"edits":[]}),
                json!({"kind":"person-directed"})
            )
            .is_err());
    }
    assert_eq!(
        peer.host.snapshot()["clientRequests"]
            .as_array()
            .unwrap()
            .len(),
        0
    );
    peer.safe();
}

pub(crate) struct Peer {
    pub(crate) host: Arc<Host>,
    child: Child,
    wire: BufReader<ChildStdout>,
    pub(crate) g: Value,
}
impl Peer {
    pub(crate) fn endpoint_credentialed_start(&self) {
        let mut definition = local();
        definition["experimental_bearer_token"] = json!(CANARY);
        self.answer(config(json!({"fixture.dot":definition})));
    }
    pub(crate) fn endpoint_wire_count(&self) -> usize {
        self.host
            .inner
            .0
            .lock()
            .unwrap()
            .source_requests
            .values()
            .filter(|e| e.written)
            .count()
    }
    pub(crate) fn endpoint_replies(
        &self,
        target: std::path::PathBuf,
        layer: std::path::PathBuf,
        id: &str,
        endpoint: &str,
    ) {
        self.endpoint_replies_mode(target, layer, id, endpoint, "ok");
    }
    pub(crate) fn endpoint_replies_mode(
        &self,
        target: std::path::PathBuf,
        layer: std::path::PathBuf,
        id: &str,
        endpoint: &str,
        mode: &str,
    ) {
        let id = id.to_owned();
        let endpoint = endpoint.to_owned();
        let mode = mode.to_owned();
        let changed = Arc::new(Mutex::new(false));
        *self.host.before_provider_wait.lock().unwrap() = Some(Box::new(move |host, source| {
            if source.attempted_frame()["method"] == "config/read"
                && *changed.lock().unwrap()
            {
                if mode == "override-reread-timeout" {
                    return;
                }
                if mode == "override-reread-error" {
                    host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"error":{"code":-32000,"message":CANARY,"data":{"nested":CANARY}}})).unwrap(),source.generation());
                    return;
                }
            }
            let mut response = if source.attempted_frame()["method"] == "config/batchWrite" {
                let next = target.with_file_name("invented-native-replacement");
                std::fs::write(&next, b"invented peer target effect, no supplier").unwrap();
                std::fs::rename(next, &target).unwrap();
                *changed.lock().unwrap() = true;
                if mode == "error" {
                    host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"error":{"code":-32000,"message":CANARY,"data":{"nested":CANARY}}})).unwrap(),source.generation());
                    return;
                }
                if mode == "timeout" {
                    return;
                }
                if mode == "closed" {
                    host.inner.0.lock().unwrap().generation["spawnCounter"] = json!(2);
                }
                if mode == "collision" {
                    host.inner.0.lock().unwrap().declared_capabilities =
                        Some(json!({"experimentalApi":true}));
                    host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"method":"currentTime/read","params":{}})).unwrap(),source.generation());
                }
                let overridden = mode == "override" || mode.starts_with("override-");
                json!({"filePath":target,"version":CANARY,"status":if overridden{"okOverridden"}else{"ok"},"overriddenMetadata":if overridden{json!({"message":CANARY,"effectiveValue":{"private":CANARY},"overridingLayer":{"name":{"type":"user","file":layer},"version":CANARY}})}else{Value::Null}})
            } else {
                let mut definition = local();
                definition["base_url"] = json!(if *changed.lock().unwrap() {
                    endpoint.as_str()
                } else {
                    "https://example.invalid/old"
                });
                let definitions = json!({id.clone():definition,"credentialed":{"name":"not offered","experimental_bearer_token":CANARY}});
                json!({"config":{"model_providers":definitions,"developer_instructions":CANARY},"origins":{},"layers":[{"name":{"type":"user","file":layer},"config":{"model_providers":definitions},"version":if *changed.lock().unwrap(){CANARY}else{"INVENTED_PRIVATE_OLD_VERSION"}}]})
            };
            if source.attempted_frame()["method"] == "config/read" {
                if mode == "session-only" {
                    response["layers"][0]["config"] = json!({});
                }
                if mode == "definition-mismatch" {
                    response["layers"][0]["config"]["model_providers"][&id]["name"] =
                        json!("different user-layer name");
                }
                if *changed.lock().unwrap() && mode == "sibling-settings" {
                    response["config"]["developer_instructions"] =
                        json!("OTHER_INVENTED_PRIVATE_SETTING");
                }
                if *changed.lock().unwrap() && mode == "reread-version" {
                    response["layers"][0]["version"] = json!("DIFFERENT_PRIVATE_NATIVE_VERSION");
                }
            }
            let write = source.attempted_frame()["method"] == "config/batchWrite";
            if write && mode == "invalid-ack-target" {
                response["filePath"] = json!(CANARY);
            }
            if write && mode == "invalid-ack-shape" {
                response["status"] = json!(CANARY);
            }
            host.on_line(
                &serde_json::to_vec(&json!({"id":if write && mode == "unmatched-ack" {json!(999999)} else {source.request_id().clone()},"result":response})).unwrap(),
                source.generation(),
            );
            // The real private ACK has arrived before this controlled drift.
            // No source/generation or reply bytes are rewritten to cause it.
            if write {
                match mode.as_str() {
                    "ack-target-missing" => std::fs::remove_file(&target).unwrap(),
                    "ack-link-missing" | "override-link-missing" => std::fs::remove_file(&layer).unwrap(),
                    "ack-link-replaced" => {
                        std::fs::remove_file(&layer).unwrap();
                        std::os::unix::fs::symlink(&target, &layer).unwrap();
                    }
                    _ => {}
                }
            }
            assert!(!source.attempted_frame().to_string().contains(CANARY));
            assert!(!source.evidence().to_string().contains(CANARY));
            assert!(!host.snapshot().to_string().contains(CANARY));
            assert!(!host.kept_replies().1.contains(CANARY));
        }));
    }
    pub(crate) fn endpoint_late_reply(&self) {
        let request = self
            .host
            .inner
            .0
            .lock()
            .unwrap()
            .source_requests
            .values()
            .find(|e| e.request.frame["method"] == "config/batchWrite")
            .unwrap()
            .request
            .clone();
        self.host.on_line(&serde_json::to_vec(&json!({"id":request.request_id(),"result":{"filePath":CANARY,"version":CANARY,"status":"okOverridden","overriddenMetadata":{"message":CANARY,"effectiveValue":CANARY}}})).unwrap(),request.generation());
    }
    pub(crate) fn endpoint_private_taps(&self) {
        self.safe();
        let entries = self
            .host
            .inner
            .0
            .lock()
            .unwrap()
            .source_requests
            .values()
            .map(|e| e.request.clone())
            .collect::<Vec<_>>();
        for entry in entries {
            let value = entry.evidence();
            assert!(!value.to_string().contains(CANARY));
            assert!(!value.to_string().contains("INVENTED_PRIVATE_OLD_VERSION"));
            if entry.attempted_frame()["method"] == "config/batchWrite" {
                assert_eq!(
                    entry.attempted_frame()["params"],
                    json!({"privateEndpointWriteWithheld":true})
                );
            }
        }
        assert!(!json!(self.host.journal()).to_string().contains(CANARY));
    }
    pub(crate) fn continuation_frame(&mut self) -> Value {
        use std::os::fd::AsRawFd;
        let descriptor = self.wire.get_ref().as_raw_fd();
        let flags = unsafe { libc::fcntl(descriptor, libc::F_GETFL) };
        assert!(flags >= 0);
        assert_eq!(
            unsafe { libc::fcntl(descriptor, libc::F_SETFL, flags | libc::O_NONBLOCK) },
            0
        );
        let deadline = std::time::Instant::now() + Duration::from_secs(2);
        let mut line = String::new();
        loop {
            match self.wire.read_line(&mut line) {
                Ok(0) => panic!("invented Peer closed before expected config/read"),
                Ok(_) if line.ends_with('\n') => return serde_json::from_str(&line).unwrap(),
                Ok(_) => {}
                Err(e)
                    if matches!(
                        e.kind(),
                        std::io::ErrorKind::WouldBlock | std::io::ErrorKind::Interrupted
                    ) => {}
                Err(_) => panic!("invented Peer frame unavailable"),
            }
            let remaining = deadline.saturating_duration_since(std::time::Instant::now());
            assert!(
                !remaining.is_zero(),
                "invented config/read frame unavailable within fixture bound"
            );
            let mut fd = libc::pollfd {
                fd: descriptor,
                events: libc::POLLIN,
                revents: 0,
            };
            assert!(
                unsafe { libc::poll(&mut fd, 1, remaining.as_millis().max(1) as i32) } > 0,
                "invented Peer frame timed out"
            );
        }
    }
    pub(crate) fn continuation_private_taps(&self) {
        self.safe();
        let packet = json!({"snapshot":self.host.snapshot(),"journal":self.host.journal(),"replies":self.host.kept_replies().1,"recovery":self.host.recorded_recovery_entries()});
        for marker in [
            CANARY,
            "INVENTED_NATIVE_VERSION_PRIVATE_52",
            "native-invented-version",
        ] {
            assert!(!packet.to_string().contains(marker));
        }
        let entries = self
            .host
            .inner
            .0
            .lock()
            .unwrap()
            .source_requests
            .values()
            .map(|entry| {
                (
                    entry.request.clone(),
                    entry.private_config,
                    entry.response.clone(),
                )
            })
            .collect::<Vec<_>>();
        for (request, private, response) in entries {
            assert_eq!(
                request.frame["method"], "config/read",
                "continuation dispatches no model/thread/start"
            );
            assert!(private);
            let evidence = request.evidence();
            for marker in [
                CANARY,
                "INVENTED_NATIVE_VERSION_PRIVATE_52",
                "native-invented-version",
            ] {
                assert!(!evidence.to_string().contains(marker));
            }
            assert!(response
                .as_ref()
                .is_none_or(|r| r.get("result").is_none() || r["privateConfigWithheld"] == true));
        }
    }
    pub(crate) fn supersede_config_generation(&self) {
        self.host.inner.0.lock().unwrap().generation["spawnCounter"] = json!(2);
    }
    pub(crate) fn unanswered_config_read(&self) -> Arc<Mutex<Option<SourceRequest>>> {
        let receipt = Arc::new(Mutex::new(None));
        let save = receipt.clone();
        *self.host.before_provider_wait.lock().unwrap() = Some(Box::new(move |_, source| {
            *save.lock().unwrap() = Some(source.clone());
        }));
        receipt
    }
    pub(crate) fn config_read_error(&self) {
        *self.host.before_provider_wait.lock().unwrap() = Some(Box::new(|host, source| {
            host.on_line(&serde_json::to_vec(&json!({"id":source.request_id(),"error":{"code":-32000,"message":CANARY,"data":{"private":CANARY}}})).unwrap(),source.generation())
        }));
    }
    pub(crate) fn for_config_continuation(host: Arc<Host>, home: &std::path::Path) -> Self {
        let home = format!(
            "app-home:{}",
            sha256_hex(home.as_os_str().as_encoded_bytes())
        );
        let session = host.inner.0.lock().unwrap().app_session.clone();
        let g = json!({"appSession":if session.is_empty(){"synthetic-continuation"}else{&session},"home":home,"spawnCounter":1});
        {
            let mut i = host.inner.0.lock().unwrap();
            i.generation = g.clone();
            i.state = "ready".into();
            i.home = home;
            i.supplier_standing = Some("invented Peer only; no native supplier".into());
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
    pub(crate) fn frame(&mut self) -> Value {
        let mut s = String::new();
        self.wire.read_line(&mut s).unwrap();
        serde_json::from_str(&s).unwrap()
    }
    pub(crate) fn answer(&self, result: Value) {
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
    pub(crate) fn safe(&self) {
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
fn project_scope() -> Value {
    json!({"reference":"/invented/work","sourceCaption":"explicit fixture project","standing":"frozen fixture source"})
}
#[test]
fn access_provider_configured_observation_mounted_join() {
    let Ok(directory) = std::env::var("CHIRALITY_PROVIDER_JOIN") else {
        return;
    };
    let directory = std::path::PathBuf::from(directory);
    let root = std::env::temp_dir().join(opaque_id("provider-join-invented-").unwrap());
    std::fs::create_dir(&root).unwrap();
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
        root: root.join("records"),
        placement: crate::records_store::Placement::Test,
        limits: vec![],
    })));
    let mut peer = Peer::with_ledger("invented-account", Some(root.join("recovery.jsonl")));
    let host_view = |peer: &Peer| {
        let mut view = peer.host.snapshot();
        view["homeRouting"] = json!({"activeModeHomeClass":"account"});
        view["currentAppProjectContext"] = project_scope();
        view["configuredProviderReadRevision"] = peer
            .host
            .configured_provider_revision(&peer.g, "/invented/work");
        view
    };
    let write = |name: &str, value: &Value| {
        assert!(!value.to_string().contains(CANARY));
        assert!(!value.to_string().contains("RowSecret37"));
        let temporary = directory.join(format!("{name}.tmp"));
        std::fs::write(&temporary, serde_json::to_vec(value).unwrap()).unwrap();
        std::fs::rename(temporary, directory.join(name)).unwrap();
    };
    write("ready.json", &host_view(&peer));
    for sequence in 0..32 {
        let path = directory.join(format!("command-{sequence}.json"));
        let deadline = std::time::Instant::now() + Duration::from_secs(15);
        while !path.exists() {
            assert!(
                std::time::Instant::now() < deadline,
                "mounted fixture command timed out"
            );
            std::thread::sleep(Duration::from_millis(5));
        }
        let bytes = std::fs::read(path).unwrap();
        assert!(bytes.len() <= 4096);
        let command: Value = serde_json::from_slice(&bytes).unwrap();
        if command["command"] == "finish" {
            break;
        }
        let mut credentialed = local();
        credentialed["experimental_bearer_token"] = json!("RowSecret37");
        peer.answer(config(
            json!({"anonymous":local(),"credentialed":credentialed}),
        ));
        let result = match command["command"].as_str().unwrap() {
            "read_configured_providers" => {
                assert_eq!(command["args"]["generation"], peer.g);
                assert_eq!(command["args"]["modeHomeClass"], "account");
                let view = inventory(&peer);
                assert_eq!(peer.frame()["method"], "config/read");
                view
            }
            "thread_start" => {
                let args = &command["args"];
                assert_eq!(args["modeHomeClass"], "account");
                if std::env::var("CHIRALITY_PROVIDER_JOIN_CHANGE").as_deref() == Ok("credentialed")
                {
                    let mut changed = local();
                    changed["experimental_bearer_token"] = json!(CANARY);
                    peer.answer(config(json!({"anonymous":changed})));
                }
                // Same Peer/source as listing, actual fresh private Start read;
                // UI-selected provider/model/entry pass unchanged, never DTO proof.
                let admission = peer.host.provider_admission_read_within(
                    &peer.g,
                    "/invented/work",
                    args["entryId"].as_str().unwrap(),
                    args["modelProvider"].as_str().unwrap(),
                    args["model"].as_str().unwrap(),
                    Duration::from_millis(30),
                );
                assert_eq!(peer.frame()["method"], "config/read");
                match admission {
                    Err(error) => Err(error),
                    Ok(proof) => {
                        let receipt = peer
                            .host
                            .thread_start_with_access_dispatch(&proof, "invented explicit guidance")
                            .unwrap();
                        let frame = peer.frame();
                        assert_eq!(frame["method"], "thread/start");
                        assert_eq!(frame["params"]["modelProvider"], args["modelProvider"]);
                        assert_eq!(frame["params"]["model"], args["model"]);
                        assert_eq!(receipt.evidence()["writeResult"], "written");
                        // The invented peer supplies no native start acknowledgment.
                        Err("Invented peer: exact thread/start written; outcome unknown; no automatic retry".into())
                    }
                }
            }
            _ => panic!("unexpected fixture command"),
        };
        peer.safe();
        let response = match result {
            Ok(value) => json!({"ok":true,"value":value}),
            Err(error) => json!({"ok":false,"error":error}),
        };
        write(
            &format!("response-{sequence}.json"),
            &json!({"response":response,"host":host_view(&peer),"recordedRecovery":peer.host.recorded_recovery_entries()}),
        );
    }
    drop(peer);
    crate::records_store::use_store_for_test(None);
    std::fs::remove_dir_all(root).unwrap();
}
fn inventory(peer: &Peer) -> Result<Value, String> {
    peer.host.configured_provider_read_within(
        &peer.g,
        "/invented/work",
        &project_scope(),
        Duration::from_millis(30),
    )
}
#[test]
fn access_provider_configured_projection_joins_private_read_and_fresh_start() {
    let mut peer = Peer::new("account");
    let mut credentialed = local();
    credentialed["experimental_bearer_token"] = json!("PrivateToken91");
    peer.answer(config(
        json!({"anonymous":local(),"credentialed":credentialed}),
    ));
    let view = inventory(&peer).unwrap();
    assert_eq!(
        view["rows"],
        json!([{"id":"anonymous","label":"Configured local provider","endpoint":"https://example.invalid/v1","wireApi":"responses"}])
    );
    assert_eq!(view["scope"]["generation"], peer.g);
    assert_eq!(view["scope"]["projectContext"], project_scope());
    assert_eq!(
        view["scope"]["readRevision"],
        peer.host
            .configured_provider_revision(&peer.g, "/invented/work")
    );
    assert!(!view.to_string().contains("PrivateToken91"));
    assert_eq!(peer.frame()["method"], "config/read");
    assert_eq!(
        peer.host.snapshot()["clientRequests"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    // Listing supplied no proof. A fresh actual Start reads the changed current
    // definition and refuses before thread/start; the old displayed row cannot admit it.
    let mut changed = local();
    changed["experimental_bearer_token"] = json!(CANARY);
    peer.answer(config(json!({"anonymous":changed})));
    assert!(peer.read("local-provider", "anonymous").is_err());
    assert_eq!(peer.frame()["method"], "config/read");
    assert_eq!(
        peer.host.snapshot()["clientRequests"]
            .as_array()
            .unwrap()
            .len(),
        2
    );
    peer.answer(config(json!({"anonymous":local()})));
    let proof = peer.read("local-provider", "anonymous").unwrap();
    assert_eq!(peer.frame()["method"], "config/read");
    peer.host
        .thread_start_with_access_dispatch(&proof, "invented explicit guidance")
        .unwrap();
    assert_eq!(peer.frame()["method"], "thread/start");
    peer.safe();
}
#[test]
fn access_provider_configured_projection_excludes_all_source_known_reflections_and_short_values() {
    for secret in [CANARY, "RowSecret37", "q", ""] {
        for reflection in [
            "id",
            "name",
            "endpoint-path",
            "endpoint-fragment",
            "encoded-path",
        ] {
            let mut peer = Peer::new("account");
            let mut reflected = local();
            let id = if reflection == "id" {
                secret
            } else {
                "reflected"
            };
            match reflection {
                "name" => reflected["name"] = json!(secret),
                "endpoint-path" => {
                    reflected["base_url"] = json!(format!("https://example.invalid/v1/{secret}"))
                }
                "endpoint-fragment" => {
                    reflected["base_url"] = json!(format!("https://example.invalid/v1#{secret}"))
                }
                "encoded-path" => {
                    reflected["base_url"] = json!(format!(
                        "https://example.invalid/v1/{}",
                        secret
                            .bytes()
                            .map(|b| format!("%{b:02X}"))
                            .collect::<String>()
                    ))
                }
                _ => {}
            }
            let mut credentialed = local();
            credentialed["experimental_bearer_token"] = json!(secret);
            peer.answer(config(
                json!({id:reflected,"independent":local(),"credentialed":credentialed}),
            ));
            let view = inventory(&peer);
            if let Ok(view) = view {
                assert!(!view.to_string().contains(secret), "{reflection}");
                let rows = view["rows"].as_array().unwrap();
                assert!(rows.iter().any(|row| row["id"] == "independent"));
                if reflection != "name" {
                    assert!(!rows.iter().any(|row| row["id"] == id));
                }
                assert!(rows
                    .iter()
                    .all(|row| row["label"] == "Configured local provider"));
            }
            assert_eq!(peer.frame()["method"], "config/read");
            peer.safe();
        }
    }
}
#[test]
fn access_provider_configured_projection_unknown_shapes_and_budgets_are_fixed_unavailable() {
    for mutation in [
        "unknown",
        "null",
        "untyped",
        "nested-array",
        "depth",
        "nodes",
        "bytes",
        "basic",
        "encoded",
        "auth-url",
    ] {
        let mut peer = Peer::new("account");
        let credentialed = local();
        let mut response = config(json!({"independent":local(),"credentialed":credentialed}));
        match mutation {
            "unknown" => {
                response["config"]["model_providers"]["credentialed"]["new-private-role"] =
                    json!(CANARY)
            }
            "null" => response["config"]["model_providers"] = Value::Null,
            "untyped" => {
                response["config"]["model_providers"]["credentialed"]["auth"] = json!(CANARY)
            }
            "nested-array" => {
                response["config"]["model_providers"]["credentialed"]["auth"] =
                    json!({"secret":[CANARY]})
            }
            "depth" => {
                let mut value = json!(CANARY);
                for _ in 0..26 {
                    value = json!({"nested":value});
                }
                response["extra"] = value;
            }
            "nodes" => response["extra"] = json!(vec![Value::Null; 4100]),
            "bytes" => response["extra"] = json!("x".repeat(262_145)),
            "basic" => {
                response["config"]["model_providers"]["credentialed"]["http_headers"] =
                    json!({"Authorization":format!("Basic {CANARY}")})
            }
            "encoded" => {
                response["config"]["model_providers"]["credentialed"]["auth"] =
                    json!({"token":format!("Bearer \"{CANARY}\"")})
            }
            "auth-url" => {
                response["extra"] =
                    json!({"authUrl":format!("https://example.invalid/login?token={CANARY}")})
            }
            _ => unreachable!(),
        }
        peer.answer(response);
        let view = inventory(&peer);
        if matches!(mutation, "encoded" | "auth-url") {
            let view = view.unwrap();
            assert!(!view.to_string().contains(CANARY));
            assert!(view["rows"]
                .as_array()
                .unwrap()
                .iter()
                .any(|row| row["id"] == "independent"));
        } else {
            assert_eq!(view.unwrap_err(), OBSERVATION_LIMIT);
        }
        assert_eq!(peer.frame()["method"], "config/read");
        peer.safe();
    }
}
#[test]
fn access_provider_configured_projection_scans_nested_and_filtered_url_channels_before_rows() {
    for channel in [
        "auth",
        "gateway",
        "aws",
        "headers",
        "env",
        "query",
        "url-user",
        "url-query",
        "url-fragment",
        "json-bearer",
        "canonical-host",
    ] {
        let mut peer = Peer::new("account");
        let secret = "RowSecret37";
        let mut reflected = local();
        if channel == "canonical-host" {
            reflected["base_url"] = json!("https://rowsecret37.invalid/v1");
        }
        let mut response =
            config(json!({secret:local(),"reflected":reflected,"independent":local()}));
        let extra = match channel {
            "auth" => json!({"auth":{"nested":{"token":secret}}}),
            "gateway" => json!({"gateway_oauth":{"nested":{"clientSecret":secret}}}),
            "aws" => json!({"aws":{"secretAccessKey":secret}}),
            "headers" => json!({"headers":{"Authorization":format!("Bearer {secret}")}}),
            "env" => json!({"env":{"UNRECOGNIZED_NAME":secret}}),
            "query" => json!({"query_params":{"untyped":secret}}),
            "url-user" => json!({"base_url":format!("https://{secret}@example.invalid/v1")}),
            "url-query" => {
                json!({"model_catalog_url":format!("https://example.invalid/models?untyped={secret}")})
            }
            "url-fragment" => json!({"base_url":format!("https://example.invalid/v1#{secret}")}),
            "json-bearer" => json!({"token":format!("Bearer \"{secret}\"")}),
            "canonical-host" => json!({"token":secret}),
            _ => unreachable!(),
        };
        response["layers"] = json!([{"name":"invented-layer","version":"invented","config":extra}]);
        // Put arbitrary validated-response data outside typed layers metadata;
        // ConfigReadResponse allows additional private fields, still scanned.
        let extra = response["layers"][0]["config"].clone();
        response.as_object_mut().unwrap().remove("layers");
        response["extra"] = extra;
        peer.answer(response);
        let view = inventory(&peer).unwrap();
        assert!(!view
            .to_string()
            .to_ascii_lowercase()
            .contains(&secret.to_ascii_lowercase()));
        assert!(view["rows"]
            .as_array()
            .unwrap()
            .iter()
            .any(|r| r["id"] == "independent"));
        assert!(!view["rows"]
            .as_array()
            .unwrap()
            .iter()
            .any(|r| r["id"] == secret));
        if channel == "canonical-host" {
            assert!(!view["rows"]
                .as_array()
                .unwrap()
                .iter()
                .any(|r| r["id"] == "reflected"));
        }
        peer.frame();
        peer.safe();
    }
}
#[test]
fn access_provider_configured_display_declines_do_not_restrict_private_operation_identifiers() {
    for (id,endpoint,publish) in [
        ("Provider.UPPER_42-name".to_owned(),"https://example.invalid/v1".to_owned(),true),
        ("p".repeat(64),"http://example.invalid/".to_owned(),true),
        ("1provider".to_owned(),"https://example.invalid/v1".to_owned(),false),
        ("private id with spaces".to_owned(),"https://example.invalid/v1".to_owned(),false),
        ("p".repeat(65),"https://example.invalid/v1".to_owned(),false),
        ("non-ascii-é".to_owned(),"https://example.invalid/v1".to_owned(),false),
        ("provider".to_owned(),"https://example.invalid/v1#private-fragment".to_owned(),false),
        ("provider".to_owned(),"https://example.invalid/%70rivate".to_owned(),false),
        ("provider".to_owned(),"https://example.invalid/a/../v1".to_owned(),false),
        ("provider".to_owned(),"https://EXAMPLE.invalid/v1".to_owned(),false),
        ("provider".to_owned(),format!("https://example.invalid/{}","x".repeat(2048)),false),
    ] {
        let mut peer=Peer::new("account"); let mut definition=local();definition["base_url"]=json!(endpoint);
        peer.answer(config(json!({id.clone():definition})));
        let view=inventory(&peer).unwrap();peer.frame();
        assert_eq!(view["rows"].as_array().unwrap().len(),usize::from(publish));
        if publish {assert_eq!(view["rows"][0]["id"],id);assert_eq!(view["rows"][0]["endpoint"],endpoint);}
        // No display predicate was added to the original private Start policy.
        assert!(peer.read("local-provider",&id).is_ok());peer.frame();peer.safe();
    }
}
#[test]
fn access_provider_configured_projection_errors_late_and_exact_source_mismatches_stay_private() {
    for mode in [
        "error",
        "malformed",
        "wrong-id",
        "method",
        "timeout",
        "closed",
        "generation",
        "revision",
        "cwd",
        "receipt",
        "pipe",
        "write",
    ] {
        let mut peer = Peer::new("account");
        *peer.host.before_provider_wait.lock().unwrap() = Some(Box::new(move |host, source| {
            let frame = match mode {
                "error" => {
                    json!({"id":source.request_id(),"error":{"code":-32000,"message":CANARY,"data":CANARY}})
                }
                "malformed" => json!({"id":source.request_id(),"result":{"config":CANARY}}),
                "wrong-id" => json!({"id":900000,"result":config(json!({"independent":local()}))}),
                "method" => {
                    json!({"id":source.request_id(),"method":"invented/bad","result":config(json!({"independent":local()}))})
                }
                _ => {
                    json!({"id":source.request_id(),"result":config(json!({"independent":local()}))})
                }
            };
            if mode != "timeout" {
                host.on_line(&serde_json::to_vec(&frame).unwrap(), source.generation());
            }
            if mode == "revision" {
                host.request_begin_scoped(
                    "config/read",
                    json!({"cwd":"/invented/work","includeLayers":false}),
                    json!({"kind":"synthetic competing reader"}),
                    false,
                    Some(source.generation()),
                )
                .unwrap();
            }
            let mut i = host.inner.0.lock().unwrap();
            match mode {
                "closed" => {
                    Host::close_generation(&mut i);
                }
                "generation" => i.generation["spawnCounter"] = json!(2),
                "cwd" => {
                    i.source_requests
                        .get_mut(&source.request_id().to_string())
                        .unwrap()
                        .request
                        .frame["params"]["cwd"] = json!("/invented/other")
                }
                "receipt" => i
                    .source_requests
                    .get_mut(&source.request_id().to_string())
                    .unwrap()
                    .request
                    .request_ref
                    .push_str("-replaced"),
                "pipe" => i.attachment_pipe_epoch += 1,
                "write" => {
                    i.source_requests
                        .get_mut(&source.request_id().to_string())
                        .unwrap()
                        .write_error = Some("invented write conflict".into())
                }
                _ => {}
            }
        }));
        assert_eq!(inventory(&peer).unwrap_err(), OBSERVATION_LIMIT, "{mode}");
        let read = peer.frame();
        assert_eq!(read["method"], "config/read");
        if mode == "revision" {
            assert_eq!(peer.frame()["method"], "config/read");
        }
        peer.host.on_line(
            &serde_json::to_vec(&json!({"id":read["id"],"result":config(json!({"late":local()}))}))
                .unwrap(),
            &peer.g,
        );
        peer.safe();
        let i = peer.host.inner.0.lock().unwrap();
        let e = i.source_requests.get(&read["id"].to_string()).unwrap();
        assert!(
            e.request.receiver.lock().unwrap().try_recv().is_err()
                || e.response
                    .as_ref()
                    .is_some_and(|r| r["privateConfigWithheld"] == true)
        );
        assert!(!i
            .client_requests
            .iter()
            .any(|r| r["method"] == "thread/start"));
    }
}
#[test]
fn access_provider_configured_read_supersedes_claimed_start_without_stranding_selection() {
    let mut peer = Peer::new("account");
    peer.answer(config(json!({"anonymous":local()})));
    let proof = peer.read("local-provider", "anonymous").unwrap();
    peer.frame();
    let mut selected = crate::access::ConversationSelection::new_explicit(
        "invented-attempt",
        Some("/invented/work"),
    )
    .unwrap();
    selected
        .choose("local-provider", "anonymous", "chosen-model", false)
        .unwrap();
    selected.start_params(&peer.g, "account", false).unwrap();
    let mut slot = None;
    crate::runtime_session::claim_start(&mut slot, selected, || Ok("invented-supply".into()))
        .unwrap();
    assert_eq!(slot.as_ref().unwrap().snapshot()["state"], "starting");
    let view = inventory(&peer).unwrap();
    peer.frame();
    assert_eq!(view["rows"][0]["id"], "anonymous");
    let result = peer
        .host
        .thread_start_with_access_dispatch(&proof, "invented explicit guidance")
        .map(|_| Value::Null);
    assert!(result.is_err());
    assert!(crate::runtime_session::finalize_start_attempt(
        slot.as_mut().unwrap(),
        "invented-attempt",
        &peer.g,
        &peer.g,
        result
    )
    .is_err());
    assert_eq!(slot.as_ref().unwrap().snapshot()["state"], "start-failed");
    assert_eq!(
        peer.host.snapshot()["clientRequests"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|r| r["method"] == "thread/start")
            .count(),
        0
    );
    peer.safe();
}
#[test]
fn access_provider_private_admission_does_not_declassify_reflected_metadata() {
    // The genuine private read may establish Start eligibility while arbitrary
    // metadata still repeats a private value. This is not a public display DTO.
    for reflection in [
        "id",
        "name",
        "endpoint-path",
        "endpoint-fragment",
        "encoded-path",
    ] {
        let mut peer = Peer::new("account");
        let mut definition = local();
        let provider = if reflection == "id" {
            CANARY
        } else {
            "anonymous"
        };
        match reflection {
            "id" => {}
            "name" => definition["name"] = json!(CANARY),
            "endpoint-path" => {
                definition["base_url"] = json!(format!("https://example.invalid/v1/{CANARY}"))
            }
            "endpoint-fragment" => {
                definition["base_url"] = json!(format!("https://example.invalid/v1#{CANARY}"))
            }
            "encoded-path" => {
                let encoded: String = CANARY.bytes().map(|b| format!("%{b:02X}")).collect();
                definition["base_url"] = json!(format!("https://example.invalid/v1/{encoded}"));
            }
            _ => unreachable!(),
        }
        let mut credentialed = local();
        credentialed["experimental_bearer_token"] = json!(CANARY);
        let result =
            config(json!({provider: definition, "separate-credentialed-entry": credentialed}));
        peer.answer(result);
        let proof = peer.read("local-provider", provider).unwrap();
        assert_eq!(proof.provider, provider);
        let frame = peer.frame();
        assert_eq!(frame["method"], "config/read");
        assert_eq!(
            frame["params"],
            json!({"cwd":"/invented/work","includeLayers":true})
        );
        assert!(!proof.source.evidence().to_string().contains(CANARY));
        peer.safe();
        assert_eq!(
            peer.host.snapshot()["clientRequests"]
                .as_array()
                .unwrap()
                .len(),
            1
        );
        // No listing/selection/model request or native thread/start is sent.
    }
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
#[test]
fn access_provider_actual_private_read_records_conform_to_canonical_schema() {
    let schema: Value = serde_json::from_str(include_str!(
        "../resources/hosting/hosting.client-request-record.schema.json"
    ))
    .unwrap();
    let validator = jsonschema::options().offline().build(&schema).unwrap();
    for mode in [
        "success",
        "native-error",
        "entry-refused",
        "malformed-result",
        "timeout",
        "not-ready",
    ] {
        let mut peer = Peer::new("home");
        if mode == "not-ready" {
            peer.host.inner.0.lock().unwrap().state = "stopped".into();
        } else {
            let m = mode;
            *peer.host.before_provider_wait.lock().unwrap() = Some(Box::new(
                move |host, source| {
                    let frame = match m {
                        "success" => {
                            Some(json!({"id":source.request_id(),"result":config(json!({}))}))
                        }
                        "native-error" => Some(
                            json!({"id":source.request_id(),"error":{"code":-32603,"message":CANARY,"data":{"private":CANARY}}}),
                        ),
                        "entry-refused" => {
                            let mut def = local();
                            def["env_key"] = json!(CANARY);
                            Some(
                                json!({"id":source.request_id(),"result":config(json!({"anonymous":def}))}),
                            )
                        }
                        "malformed-result" => {
                            Some(json!({"id":source.request_id(),"result":{"config":CANARY}}))
                        }
                        _ => None,
                    };
                    if let Some(frame) = frame {
                        host.on_line(&serde_json::to_vec(&frame).unwrap(), source.generation());
                    }
                },
            ));
        }
        let result = peer.read(
            if mode == "entry-refused" {
                "local-provider"
            } else {
                "chatgpt-account"
            },
            if mode == "entry-refused" {
                "anonymous"
            } else {
                "openai"
            },
        );
        assert_eq!(result.is_ok(), mode == "success");
        if mode != "not-ready" {
            assert_eq!(peer.frame()["method"], "config/read");
        }
        let rows = peer.host.snapshot()["clientRequests"].clone();
        assert_eq!(rows.as_array().unwrap().len(), 1);
        let row = &rows[0];
        assert_eq!(
            row["initiator"],
            json!({"kind":"app-rule","name":"access-provider-admission"})
        );
        validator
            .validate(row)
            .unwrap_or_else(|error| panic!("{mode}: {error}"));
        assert_eq!(
            row["outcome"],
            match mode {
                "native-error" => "response-observed-error",
                "timeout" => "pending",
                "not-ready" => "refused-not-sent",
                _ => "response-observed-result",
            }
        );
        peer.safe();
    }
}
fn child_fixture() -> (std::path::PathBuf, Value) {
    let root = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(opaque_id("child-dispatch-").unwrap());
    std::fs::create_dir_all(root.join("home")).unwrap();
    std::fs::write(root.join("home/config.toml"), "").unwrap();
    let mut value = config(json!({}));
    value["layers"] = json!([
    {"name":{"type":"sessionFlags"},"version":"s","config":{"cli_auth_credentials_store":"file"}},
    {"name":{"type":"user","file":root.join("home/config.toml"),"profile":null},"version":"u","config":{}},
    {"name":{"type":"system","file":root.join("system/config.toml")},"version":"y","config":{}}
    ]);
    crate::runtime_session::seed_instructions(&root.join("instructions")).unwrap();
    (root, value)
}
#[test]
fn native_children_actual_private_start_has_exact_published_role_keys() {
    let (root, value) = child_fixture();
    let mut peer = child_peer();
    peer.answer(value);
    let mut proof = peer.read("chatgpt-account", "openai").unwrap();
    assert_eq!(peer.frame()["params"]["includeLayers"], true);
    let mut composition = crate::runtime_session::compose_role(
        &root.join("instructions"),
        Some(crate::role_supply::Role::HELP_HUMAN),
    )
    .unwrap();
    peer.host
        .prepare_role_children(
            &mut proof,
            &mut composition,
            &root.join("instructions"),
            &root,
        )
        .unwrap();
    assert_eq!(peer.frame()["method"], "config/read");
    assert_eq!(composition.children.len(), 3);
    let receipt = peer
        .host
        .thread_start_with_role_dispatch(&proof, &composition)
        .unwrap();
    let sent = peer.frame();
    assert_eq!(sent, receipt.evidence()["sentFrame"]);
    assert_eq!(sent["params"]["config"], composition.native_config());
    assert_eq!(sent["params"]["developerInstructions"], composition.text);
    for child in &composition.children {
        let parsed: toml::Value =
            toml::from_str(&std::fs::read_to_string(&child.path).unwrap()).unwrap();
        assert_eq!(
            parsed["developer_instructions"].as_str(),
            Some(child.composition.text.as_str())
        );
    }
    peer.safe();
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_queued_mutation_cannot_promote_or_strip_prepared_supply() {
    for mutation in ["added", "deleted", "file", "receipt"] {
        let (root, value) = child_fixture();
        let mut peer = child_peer();
        peer.answer(value.clone());
        let mut proof = peer.read("chatgpt-account", "openai").unwrap();
        peer.frame();
        let mut composition = crate::runtime_session::compose_role(
            &root.join("instructions"),
            Some(crate::role_supply::Role::WORKING_ITEMS),
        )
        .unwrap();
        peer.host
            .prepare_role_children(
                &mut proof,
                &mut composition,
                &root.join("instructions"),
                &root,
            )
            .unwrap();
        assert_eq!(peer.frame()["method"], "config/read");
        assert_eq!(composition.children.len(), 1);
        let held = peer.host.frame_write.lock().unwrap();
        let host = Arc::clone(&peer.host);
        let worker =
            std::thread::spawn(move || host.thread_start_with_role_dispatch(&proof, &composition));
        let deadline = std::time::Instant::now() + Duration::from_secs(2);
        while !peer
            .host
            .inner
            .0
            .lock()
            .unwrap()
            .source_requests
            .values()
            .any(|e| e.request.frame["method"] == "thread/start")
        {
            assert!(std::time::Instant::now() < deadline);
            std::thread::sleep(Duration::from_millis(1));
        }
        match mutation {
            "added" => {
                std::fs::create_dir_all(root.join("home/agents")).unwrap();
                std::fs::write(root.join("home/agents/person.toml"),"name = \"TASK\"\ndescription = \"person\"\ndeveloper_instructions = \"person\"\n").unwrap();
            }
            "deleted" => {
                std::fs::remove_file(root.join("home/config.toml")).unwrap();
            }
            "file" => {
                let dir = root.join("native-child-roles");
                let file = std::fs::read_dir(dir)
                    .unwrap()
                    .next()
                    .unwrap()
                    .unwrap()
                    .path();
                std::fs::set_permissions(
                    &file,
                    std::os::unix::fs::PermissionsExt::from_mode(0o600),
                )
                .unwrap();
                std::fs::write(file, "changed").unwrap();
            }
            "receipt" => {
                let mut i = peer.host.inner.0.lock().unwrap();
                i.provider_read_revisions.insert(
                    "/invented/work".into(),
                    (peer.g.clone(), "newer-private-read".into()),
                );
            }
            _ => unreachable!(),
        }
        drop(held);
        let receipt = worker.join().unwrap().unwrap();
        let evidence = receipt.evidence();
        assert_ne!(evidence["writeResult"], "written");
        assert!(evidence["sentFrame"].is_null());
        assert!(
            receipt.attempted_frame()["params"]["config"]["agents.TASK.config_file"].is_string(),
            "registered intended bytes retained; never stripped into misleading supply"
        );
        peer.safe();
        std::fs::remove_dir_all(root).unwrap();
    }
}
#[test]
fn native_children_current_raw_alias_cannot_hide_behind_older_native_layer() {
    let (root, value) = child_fixture();
    let mut peer = child_peer();
    peer.answer(value);
    let mut proof = peer.read("chatgpt-account", "openai").unwrap();
    peer.frame();
    std::fs::write(
        root.join("home/config.toml"),
        "[agents.ALIAS]\nconfig_file = \"person.toml\"\n",
    )
    .unwrap();
    std::fs::write(root.join("home/person.toml"),"name = \"TASK\"\ndescription = \"private\"\ndeveloper_instructions = \"PERSONAL_SOURCE_CANARY\"\n").unwrap();
    let mut composition = crate::runtime_session::compose_role(
        &root.join("instructions"),
        Some(crate::role_supply::Role::WORKING_ITEMS),
    )
    .unwrap();
    peer.host
        .prepare_role_children(
            &mut proof,
            &mut composition,
            &root.join("instructions"),
            &root,
        )
        .unwrap();
    assert!(composition.children.is_empty());
    let receipt = peer
        .host
        .thread_start_with_role_dispatch(&proof, &composition)
        .unwrap();
    assert!(peer.frame()["params"].get("config").is_none());
    assert_eq!(receipt.evidence()["writeResult"], "written");
    assert!(!peer
        .host
        .snapshot()
        .to_string()
        .contains("PERSONAL_SOURCE_CANARY"));
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_new_native_read_cannot_promote_changed_trust() {
    let (root, mut value) = child_fixture();
    value["layers"].as_array_mut().unwrap().push(json!({"name":{"type":"project","dotCodexFolder":root.join("project/.codex")},"version":"p","config":{},"disabledReason":"untrusted"}));
    std::fs::create_dir_all(root.join("project/.codex/agents")).unwrap();
    std::fs::write(
        root.join("project/.codex/agents/task.toml"),
        "name = \"TASK\"\ndescription = \"person\"\ndeveloper_instructions = \"person\"\n",
    )
    .unwrap();
    let mut peer = child_peer();
    peer.answer(value.clone());
    let mut proof = peer.read("chatgpt-account", "openai").unwrap();
    peer.frame();
    value["layers"][3]
        .as_object_mut()
        .unwrap()
        .remove("disabledReason");
    value["layers"][3]["version"] = json!("new");
    peer.answer(value);
    let mut composition = crate::runtime_session::compose_role(
        &root.join("instructions"),
        Some(crate::role_supply::Role::WORKING_ITEMS),
    )
    .unwrap();
    peer.host
        .prepare_role_children(
            &mut proof,
            &mut composition,
            &root.join("instructions"),
            &root,
        )
        .unwrap();
    assert_eq!(peer.frame()["method"], "config/read");
    assert!(composition.children.is_empty());
    peer.host
        .thread_start_with_role_dispatch(&proof, &composition)
        .unwrap();
    assert!(peer.frame()["params"].get("config").is_none());
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_source_io_does_not_hold_stop_or_host_state_locks() {
    let (root, value) = child_fixture();
    let mut peer = child_peer();
    peer.answer(value);
    let mut proof = peer.read("chatgpt-account", "openai").unwrap();
    peer.frame();
    let mut composition = crate::runtime_session::compose_role(
        &root.join("instructions"),
        Some(crate::role_supply::Role::WORKING_ITEMS),
    )
    .unwrap();
    peer.host
        .prepare_role_children(
            &mut proof,
            &mut composition,
            &root.join("instructions"),
            &root,
        )
        .unwrap();
    peer.frame();
    let (paused_tx, paused_rx) = std::sync::mpsc::channel();
    let (go_tx, go_rx) = std::sync::mpsc::channel();
    let host = Arc::clone(&peer.host);
    let worker = std::thread::spawn(move || {
        crate::child_roles::BEFORE_RECHECK.with(|hook| {
            *hook.borrow_mut() = Some(Box::new(move || {
                paused_tx.send(()).unwrap();
                go_rx.recv_timeout(Duration::from_secs(2)).unwrap();
            }))
        });
        host.thread_start_with_role_dispatch(&proof, &composition)
    });
    paused_rx.recv_timeout(Duration::from_secs(2)).unwrap();
    {
        let _gate = peer
            .host
            .attachment_gate
            .try_lock()
            .expect("Stop gate remains available during source IO");
        let mut i = peer
            .host
            .inner
            .0
            .try_lock()
            .expect("native state remains available during source IO");
        Host::close_generation(&mut i);
    }
    go_tx.send(()).unwrap();
    assert!(worker.join().unwrap().is_err());
    std::fs::remove_dir_all(root).unwrap();
}

fn child_peer() -> Peer {
    let peer = Peer::new("child-home");
    peer.host.inner.0.lock().unwrap().version_identity = Some(
        json!({"declaredPin":"0.160.0","distributionContentIdentity":[{"path":"bin/codex","identity":{"algorithm":"sha-256","value":"112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b"}}]}),
    );
    peer
}
fn child_thread(id: &str, parent: Option<&str>, role: Option<&str>) -> Value {
    json!({"id":id,"cliVersion":"0.160.0","createdAt":1,"updatedAt":2,"cwd":"/invented/work","ephemeral":false,"modelProvider":"openai","preview":"synthetic","projectId":null,"sessionId":"synthetic-session","source":if let Some(parent)=parent{json!({"subAgent":{"thread_spawn":{"parent_thread_id":parent,"depth":1,"agent_role":role}}})}else{json!("appServer")},"status":{"type":"idle"},"turns":[],"agentRole":role,"parentThreadId":parent,"forkedFromId":null})
}
fn child_parent() -> (
    std::path::PathBuf,
    Peer,
    crate::role_lifecycle::RoleBindings,
    crate::role_supply::Composition,
) {
    child_parent_edited(false)
}
fn child_parent_edited(
    edited: bool,
) -> (
    std::path::PathBuf,
    Peer,
    crate::role_lifecycle::RoleBindings,
    crate::role_supply::Composition,
) {
    let (root, value) = child_fixture();
    let mut peer = child_peer();
    peer.answer(value);
    let mut proof = peer.read("chatgpt-account", "openai").unwrap();
    peer.frame();
    if edited {
        use std::io::Write;
        let mut file = std::fs::OpenOptions::new()
            .append(true)
            .open(root.join("instructions/agents/AGENT_TASK.md"))
            .unwrap();
        file.write_all(b"\nSynthetic edited guidance\n").unwrap();
    }
    let mut c = crate::runtime_session::compose_role(
        &root.join("instructions"),
        Some(crate::role_supply::Role::WORKING_ITEMS),
    )
    .unwrap();
    peer.host
        .prepare_role_children(&mut proof, &mut c, &root.join("instructions"), &root)
        .unwrap();
    peer.frame();
    let receipt = peer
        .host
        .thread_start_with_role_dispatch(&proof, &c)
        .unwrap();
    let sent = peer.frame();
    let response = json!({"id":receipt.request_id(),"result":{"thread":child_thread("parent",None,None),"model":"chosen-model","modelProvider":"openai","cwd":"/invented/work","approvalPolicy":"on-request","approvalsReviewer":"user","sandbox":{"type":"readOnly"}}});
    peer.host.native_frame_for_test(&peer.g, &response);
    let binding = crate::role_lifecycle::PreparedStart::new(
        "child-home",
        peer.g.clone(),
        receipt.request_id().clone(),
        receipt.request_ref(),
        "sup:parent",
        &c,
    )
    .unwrap()
    .observe(&peer.g, &sent, &response)
    .unwrap();
    let mut roles = crate::role_lifecycle::RoleBindings::default();
    roles.insert(binding).unwrap();
    (root, peer, roles, c)
}
fn child_event(peer: &Peer, parent: &str, child: &str, item: &str) {
    peer.host.native_frame_for_test(&peer.g,&json!({"method":"item/completed","params":{"completedAtMs":1,"threadId":parent,"turnId":format!("turn-{parent}"),"item":{"type":"subAgentActivity","id":item,"kind":"started","agentThreadId":child,"agentPath":"/root/synthetic"}}}));
}
#[test]
fn native_child_guidance_actual_event_metadata_and_deferred_task_delegation() {
    let (root, mut peer, roles, _) = child_parent();
    std::fs::create_dir(root.join("project")).unwrap();
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
        root: root.join("record-store"),
        placement: crate::records_store::Placement::Test,
        limits: vec![],
    })));
    let log = std::sync::Arc::new(
        crate::role_observations::RoleLog::open(&root.join("project")).unwrap(),
    );
    let log_source = Ok(log.clone());
    let mut associations = crate::native_child_guidance::ChildGuidance::default();
    child_event(&peer, "parent", "child", "spawn-child");
    child_event(&peer, "child", "grandchild", "spawn-grandchild");
    assert_eq!(peer.host.observed_child_starts().len(), 2);
    associations.reconcile(&peer.host, &roles, Some(&log_source));
    assert_eq!(associations.limits(), json!([]));
    let read = peer.frame();
    assert_eq!(
        read["params"],
        json!({"threadId":"child","includeTurns":false})
    );
    peer.host.native_frame_for_test(&peer.g,&json!({"id":read["id"],"result":{"thread":child_thread("child",Some("parent"),Some("TASK"))}}));
    associations.reconcile(&peer.host, &roles, Some(&log_source));
    let child = associations.for_thread("child-home", "child");
    assert_eq!(child["standing"], "app-observed-child-supply");
    assert_eq!(child["parentSupplyRef"], "sup:parent");
    assert_eq!(child["providerAdoption"], "unknown");
    assert_eq!(
        associations.limits().as_array().unwrap().len(),
        1,
        "descendant before parent metadata still records TASK delegation"
    );
    assert_eq!(associations.limits()[0]["standing"], "stated-not-enforced");
    associations.reconcile(&peer.host, &roles, Some(&log_source));
    assert_eq!(associations.limits().as_array().unwrap().len(), 1);
    {
        let mut i = peer.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
        i.generation["spawnCounter"] = json!(2);
    }
    assert_eq!(
        associations.for_thread("child-home", "child")["standing"],
        "app-observed-child-supply",
        "original child evidence survives source ending"
    );
    let read = log.read("child-home", None);
    assert_eq!(read["observations"].as_array().unwrap().len(), 2, "{read}");
    let child_record = read["observations"]
        .as_array()
        .unwrap()
        .iter()
        .find(|r| r["record"]["outcome"] == "native-child-associated")
        .unwrap();
    assert!(
        child_record["sourceBytes"]["composed"].is_string(),
        "{read}"
    );
    assert_eq!(child_record["record"]["request"]["method"], "thread/read");
    assert_eq!(read["currentRoleAuthorityRestored"], false);
    crate::records_store::use_store_for_test(None);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_child_guidance_rejects_role_parent_fork_and_source_mismatches() {
    for case in [
        "role",
        "parent",
        "source",
        "fork",
        "id",
        "tampered-file",
        "resumed-parent",
    ] {
        let (root, mut peer, roles, c) = child_parent();
        let mut associations = crate::native_child_guidance::ChildGuidance::default();
        child_event(&peer, "parent", "child", "spawn-child");
        associations.reconcile(&peer.host, &roles, None);
        let read = peer.frame();
        let mut thread = child_thread("child", Some("parent"), Some("TASK"));
        match case {
            "role" => {
                thread["agentRole"] = json!("worker");
                thread["source"]["subAgent"]["thread_spawn"]["agent_role"] = json!("worker");
            }
            "parent" => thread["parentThreadId"] = json!("foreign"),
            "source" => {
                thread["source"]["subAgent"]["thread_spawn"]["parent_thread_id"] = json!("foreign")
            }
            "fork" => thread["forkedFromId"] = json!("copied-thread"),
            "id" => thread["id"] = json!("another"),
            "tampered-file" => {
                let file = &c.children[0].path;
                std::fs::set_permissions(file, std::os::unix::fs::PermissionsExt::from_mode(0o600))
                    .unwrap();
                std::fs::write(file, "changed").unwrap();
            }
            "resumed-parent" => {
                peer.host
                    .request_begin_scoped(
                        "thread/resume",
                        json!({"threadId":"parent"}),
                        json!({"kind":"person-directed"}),
                        false,
                        Some(&peer.g),
                    )
                    .unwrap();
                assert_eq!(peer.frame()["method"], "thread/resume");
            }
            _ => unreachable!(),
        };
        peer.host.native_frame_for_test(
            &peer.g,
            &json!({"id":read["id"],"result":{"thread":thread}}),
        );
        associations.reconcile(&peer.host, &roles, None);
        assert!(
            associations.for_thread("child-home", "child").is_null(),
            "{case}"
        );
        assert_eq!(
            associations.snapshot()[0]["guidance"]["standing"],
            "unknown",
            "{case}"
        );
        std::fs::remove_dir_all(root).unwrap();
    }
}
#[test]
fn native_child_guidance_uncompleted_self_fork_and_foreign_generation_have_no_authority() {
    let (root, peer, roles, _) = child_parent();
    let mut associations = crate::native_child_guidance::ChildGuidance::default();
    peer.host.native_frame_for_test(&peer.g,&json!({"method":"item/started","params":{"threadId":"parent","turnId":"turn-parent","item":{"type":"subAgentActivity","id":"started-only","kind":"started","agentThreadId":"uncompleted","agentPath":"/root/synthetic"}}}));
    child_event(&peer, "parent", "parent", "self");
    child_event(&peer, "fork-copy", "child", "copied");
    let mut foreign = peer.g.clone();
    foreign["spawnCounter"] = json!(99);
    peer.host.native_frame_for_test(&foreign,&json!({"method":"item/completed","params":{"completedAtMs":1,"threadId":"parent","turnId":"turn-parent","item":{"type":"subAgentActivity","id":"foreign","kind":"started","agentThreadId":"foreign-child","agentPath":"/root/synthetic"}}}));
    associations.reconcile(&peer.host, &roles, None);
    assert!(associations
        .for_thread("child-home", "uncompleted")
        .is_null());
    assert!(associations.for_thread("child-home", "parent").is_null());
    assert!(associations.for_thread("child-home", "child").is_null());
    assert!(associations
        .for_thread("child-home", "foreign-child")
        .is_null());
    assert!(!peer.host.snapshot()["clientRequests"]
        .as_array()
        .unwrap()
        .iter()
        .any(|r| r["method"] == "thread/read"));
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_absent_or_different_acting_supplier_identity_withholds_only_children() {
    for pin in [
        Value::Null,
        json!({"declaredPin":"0.160.0","distributionContentIdentity":[{"path":"bin/codex","identity":{"algorithm":"sha-256","value":"different"}}]}),
    ] {
        let (root, value) = child_fixture();
        let mut peer = child_peer();
        peer.host.inner.0.lock().unwrap().version_identity = (!pin.is_null()).then_some(pin);
        peer.answer(value);
        let mut proof = peer.read("chatgpt-account", "openai").unwrap();
        peer.frame();
        let mut c = crate::runtime_session::compose_role(
            &root.join("instructions"),
            Some(crate::role_supply::Role::WORKING_ITEMS),
        )
        .unwrap();
        peer.host
            .prepare_role_children(&mut proof, &mut c, &root.join("instructions"), &root)
            .unwrap();
        assert!(c.children.is_empty());
        assert_eq!(
            c.carried["nativeChildRoles"][3]["reason"],
            "mechanism-not-supported-at-pin"
        );
        peer.host
            .thread_start_with_role_dispatch(&proof, &c)
            .unwrap();
        let frame = peer.frame();
        assert_eq!(frame["method"], "thread/start");
        assert!(frame["params"].get("config").is_none());
        assert_eq!(frame["params"]["developerInstructions"], c.text);
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[test]
fn native_child_guidance_modified_task_keeps_unknown_limit_standing() {
    let (root, mut peer, roles, _) = child_parent_edited(true);
    let mut associations = crate::native_child_guidance::ChildGuidance::default();
    child_event(&peer, "parent", "child", "spawn-child");
    child_event(&peer, "child", "grandchild", "spawn-grandchild");
    associations.reconcile(&peer.host, &roles, None);
    let read = peer.frame();
    peer.host.native_frame_for_test(&peer.g,&json!({"id":read["id"],"result":{"thread":child_thread("child",Some("parent"),Some("TASK"))}}));
    associations.reconcile(&peer.host, &roles, None);
    let limits = associations.limits();
    assert_eq!(limits[0]["standing"], "unknown");
    assert!(limits[0]["presentedAs"]
        .as_str()
        .unwrap()
        .contains("unknown"));
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_child_guidance_warm_resume_restart_compares_original_without_new_authority() {
    let (root, mut peer, roles, _) = child_parent();
    let mut associations = crate::native_child_guidance::ChildGuidance::default();
    child_event(&peer, "parent", "child", "spawn-child");
    associations.reconcile(&peer.host, &roles, None);
    let read = peer.frame();
    peer.host.native_frame_for_test(&peer.g,&json!({"id":read["id"],"result":{"thread":child_thread("child",Some("parent"),Some("TASK"))}}));
    associations.reconcile(&peer.host, &roles, None);
    let original = associations.for_thread("child-home", "child");
    peer.host
        .request_begin_scoped(
            "thread/resume",
            json!({"threadId":"child"}),
            json!({"kind":"person-directed"}),
            false,
            Some(&peer.g),
        )
        .unwrap();
    peer.frame();
    child_event(&peer, "child", "after-resume", "delegate-after-resume");
    associations.reconcile(&peer.host, &roles, None);
    assert_eq!(
        associations.limits()[0]["originalAssociation"]["generation"],
        peer.g
    );
    assert_eq!(associations.limits()[0]["actionGeneration"], peer.g);
    let mut later = peer.g.clone();
    later["spawnCounter"] = json!(2);
    {
        let mut i = peer.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
        i.generation = later.clone();
        i.state = "ready".into();
    }
    let action = |generation: &Value, parent: &str, child: &str, item: &str| {
        peer.host.native_frame_for_test(generation,&json!({"method":"item/completed","params":{"completedAtMs":1,"threadId":parent,"turnId":format!("turn-{parent}"),"item":{"type":"subAgentActivity","id":item,"kind":"started","agentThreadId":child,"agentPath":"/root/synthetic"}}}))
    };
    action(&later, "child", "after-restart", "delegate-after-restart");
    action(&later, "parent", "new-unknown", "new-child-after-restart");
    associations.reconcile(&peer.host, &roles, None);
    assert_eq!(associations.for_thread("child-home", "child"), original);
    assert!(associations
        .for_thread("child-home", "new-unknown")
        .is_null());
    let limits = associations.limits();
    assert_eq!(limits.as_array().unwrap().len(), 2);
    assert_eq!(limits[1]["originalAssociation"]["generation"], peer.g);
    assert_eq!(limits[1]["actionGeneration"], later);
    assert_eq!(
        limits[1]["basis"],
        "comparison-with-original-child-guidance"
    );
    assert!(limits[1].get("roleInForce").is_none());
    let mut foreign = later.clone();
    foreign["appSession"] = json!("foreign-session");
    {
        peer.host.inner.0.lock().unwrap().generation = foreign.clone();
    }
    action(&foreign, "child", "foreign-child", "foreign-action");
    associations.reconcile(&peer.host, &roles, None);
    assert_eq!(associations.limits().as_array().unwrap().len(), 2);
    assert!(associations
        .for_thread("child-home", "foreign-child")
        .is_null());
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_child_guidance_private_receipt_queue_survives_journal_burst_and_close() {
    let (root, mut peer, roles, _) = child_parent();
    let mut associations = crate::native_child_guidance::ChildGuidance::default();
    let burst = |peer: &Peer| {
        for n in 0..4200 {
            peer.host.native_frame_for_test(&peer.g,&json!({"method":"item/agentMessage/delta","params":{"threadId":"parent","turnId":"burst","itemId":"unrelated","delta":format!("{n}")}}));
        }
    };
    child_event(&peer, "parent", "child", "evicted-child-start");
    burst(&peer);
    assert!(!peer
        .host
        .journal()
        .iter()
        .any(|r| r["frame"]["params"]["item"]["id"] == "evicted-child-start"));
    assert_eq!(peer.host.observed_child_starts().len(), 1);
    associations.reconcile(&peer.host, &roles, None);
    assert!(peer.host.observed_child_starts().is_empty());
    let read = peer.frame();
    peer.host.native_frame_for_test(&peer.g,&json!({"id":read["id"],"result":{"thread":child_thread("child",Some("parent"),Some("TASK"))}}));
    associations.reconcile(&peer.host, &roles, None);
    assert_eq!(
        associations.for_thread("child-home", "child")["standing"],
        "app-observed-child-supply"
    );
    child_event(&peer, "child", "grandchild", "evicted-task-delegation");
    burst(&peer);
    assert!(!peer
        .host
        .journal()
        .iter()
        .any(|r| r["frame"]["params"]["item"]["id"] == "evicted-task-delegation"));
    {
        let mut i = peer.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
        i.state = "stopped".into();
    }
    assert_eq!(peer.host.observed_child_starts().len(), 1);
    associations.reconcile(&peer.host, &roles, None);
    assert!(peer.host.observed_child_starts().is_empty());
    assert_eq!(associations.limits().as_array().unwrap().len(), 1);
    assert_eq!(
        associations.limits()[0]["itemId"],
        "evicted-task-delegation"
    );
    assert!(associations
        .for_thread("child-home", "grandchild")
        .is_null());
    associations.reconcile(&peer.host, &roles, None);
    assert_eq!(associations.limits().as_array().unwrap().len(), 1);
    std::fs::remove_dir_all(root).unwrap();
}
