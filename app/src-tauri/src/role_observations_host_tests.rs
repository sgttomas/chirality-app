// Actual Host/private-receipt joining with invented pipe peers; no supplier/provider witness.
use super::*;
fn role_observations_exchange<F>(
    host: &Arc<Host>,
    generation: &Value,
    response: Value,
    operation: F,
) -> (Result<Value, String>, Value)
where
    F: FnOnce() -> Result<Value, String>,
{
    let mut child = Command::new("/bin/cat")
        .env_clear()
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .unwrap();
    *host.stdin.lock().unwrap() = child.stdin.take();
    let stdout = child.stdout.take().unwrap();
    let me = Arc::clone(host);
    let generation = generation.clone();
    let (tx, rx) = channel();
    let worker = std::thread::spawn(move || {
        let mut line = String::new();
        BufReader::new(stdout).read_line(&mut line).unwrap();
        let outbound: Value = serde_json::from_str(&line).unwrap();
        tx.send(outbound.clone()).unwrap();
        let mut response = response;
        response["id"] = outbound["id"].clone();
        me.on_line(&serde_json::to_vec(&response).unwrap(), &generation);
    });
    let result = operation();
    let outbound = rx.recv().unwrap();
    worker.join().unwrap();
    *host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
    (result, outbound)
}
#[test]
fn actual_start_fork_continue_as_store_and_fresh_quoted_history() {
    use crate::native_history::Direction;
    use crate::role_supply::{Composition, Guidance, Role};
    use crate::runtime_session::HistorySession;
    let root = std::path::PathBuf::from("/private/tmp")
        .join(crate::util::opaque_id("role-log-diagnosis-").unwrap());
    std::fs::create_dir_all(root.join("project")).unwrap();
    let project = root.join("project");
    let store = root.join("records-store");
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
        root: store.clone(),
        placement: crate::records_store::Placement::Test,
        limits: vec![],
    })));
    crate::records_store::attach(&project, true).unwrap();
    let ledger = root.join("app/runtime/recovery.ledger.jsonl");
    std::fs::create_dir_all(ledger.parent().unwrap()).unwrap();
    let host = Arc::new(Host::new());
    host.inner.0.lock().unwrap().app_session = "conversation-session".into();
    host.configure_recovery(ledger.clone()).unwrap();
    {
        let mut i = host.inner.0.lock().unwrap();
        i.state = "ready".into();
        i.generation = g();
        i.home = "conversation-home".into();
        i.spawn_counter = 1;
    }
    let mut hot = HistorySession::default();
    hot.configure_role_log(&project);
    hot.synchronize(&host.snapshot());
    let common = Guidance::seeded(
        "AGENTS.md",
        "test-release",
        b"Exact common\r\n".to_vec(),
        b"default common",
    )
    .unwrap();
    let guidance = Guidance::seeded(
        "agents/AGENT_HELP_HUMAN.md",
        "test-release",
        b"Exact HELP_HUMAN\r\n".to_vec(),
        b"default role",
    )
    .unwrap();
    let composition =
        Composition::new(&common, Some((Role::HELP_HUMAN, &guidance)), false).unwrap();
    let mut native = history_resume("idle", true);
    native["thread"]["id"] = json!("role-origin");
    native["cwd"] = json!(project);
    native["thread"]["cwd"] = json!(project);
    let mut original = None;
    let (result, outbound) = exchange(&host, Some(json!({"result":native})), vec![], || {
        let receipt = host.thread_start_with_guidance_dispatch(
            &g(),
            project.to_str().unwrap(),
            "selected",
            "configured",
            &composition.text,
        )?;
        hot.start_dispatched_selected(
            receipt.clone(),
            &composition,
            "sup:diagnosis-origin",
            None,
            Some(false),
        )?;
        let evidence = host.source_request_wait(&receipt, Duration::from_millis(100))?;
        original = Some(receipt);
        Ok(evidence)
    });
    assert_eq!(result.unwrap()["writeResult"], "written");
    assert_eq!(
        outbound["params"]["developerInstructions"],
        composition.text
    );
    hot.reconcile(&host);
    assert!(hot.start_admitted(original.as_ref().unwrap()));
    assert_eq!(
        hot.role("conversation-home", "role-origin")["role"],
        "HELP_HUMAN"
    );
    let mut fork_native = history_resume("idle", true);
    fork_native["thread"]["id"] = json!("role-fork");
    fork_native["thread"]["forkedFromId"] = json!("role-origin");
    fork_native["cwd"] = json!(project);
    fork_native["thread"]["cwd"] = json!(project);
    let mut fork = None;
    let (result, outbound) = exchange(&host, Some(json!({"result":fork_native})), vec![], || {
        let receipt = host.thread_fork_dispatch(&g(), "role-origin")?;
        hot.fork_dispatched(receipt.clone(), "role-origin")?;
        let evidence = host.source_request_wait(&receipt, Duration::from_millis(100))?;
        fork = Some(receipt);
        Ok(evidence)
    });
    assert_eq!(result.unwrap()["writeResult"], "written");
    assert_eq!(
        outbound["params"],
        json!({"threadId":"role-origin","deferGoalContinuation":true})
    );
    let fork = fork.unwrap();
    hot.reconcile(&host);
    assert!(hot.fork_result(&fork).unwrap().is_ok());
    assert_eq!(
        hot.role("conversation-home", "role-fork")["role"],
        "HELP_HUMAN"
    );
    let mut handoffs = crate::conversation_roles::Handoffs::default();
    let source_role = hot
        .binding("conversation-home", "role-origin")
        .unwrap()
        .role_in_force("conversation-home", "role-origin");
    let (id, text) = handoffs
        .reserve(&g(), "role-origin", source_role, Some(Role::WORKING_ITEMS))
        .unwrap();
    let (result, outbound) = exchange(
        &host,
        Some(json!({"result":{"turn":turn("inProgress")}})),
        vec![],
        || host.turn_start_text(&g(), "role-origin", &text),
    );
    handoffs.sent(&id, result).unwrap();
    assert_eq!(outbound["method"], "turn/start");
    let relation = handoffs
        .continuation(&id, &g(), Some(Role::WORKING_ITEMS))
        .unwrap();
    assert_eq!(relation["sourceStartRecord"], "sup:diagnosis-origin");
    let guidance = Guidance::seeded(
        "agents/AGENT_WORKING_ITEMS.md",
        "test-release",
        b"Exact WORKING_ITEMS\r\n".to_vec(),
        b"default role",
    )
    .unwrap();
    let next = Composition::new(&common, Some((Role::WORKING_ITEMS, &guidance)), false).unwrap();
    let mut next_native = history_resume("idle", true);
    next_native["thread"]["id"] = json!("role-continued");
    next_native["cwd"] = json!(project);
    next_native["thread"]["cwd"] = json!(project);
    let mut continued = None;
    let (result, outbound) = exchange(&host, Some(json!({"result":next_native})), vec![], || {
        let receipt = host.thread_start_with_guidance_dispatch(
            &g(),
            project.to_str().unwrap(),
            "selected",
            "configured",
            &next.text,
        )?;
        hot.start_dispatched_continuing(
            receipt.clone(),
            &next,
            "sup:diagnosis-continued",
            Some(relation.clone()),
        )?;
        let evidence = host.source_request_wait(&receipt, Duration::from_millis(100))?;
        continued = Some(receipt);
        Ok(evidence)
    });
    assert_eq!(result.unwrap()["writeResult"], "written");
    assert_eq!(outbound["params"]["developerInstructions"], next.text);
    hot.reconcile(&host);
    assert!(hot.start_admitted(continued.as_ref().unwrap()));
    assert_eq!(
        hot.role("conversation-home", "role-continued")["role"],
        "WORKING_ITEMS"
    );
    assert_eq!(
        hot.binding("conversation-home", "role-continued")
            .unwrap()
            .relation()["from"],
        relation
    );
    assert_eq!(
        hot.role("conversation-home", "role-origin")["role"],
        "HELP_HUMAN"
    );
    host.observe_conversation_project(
        &g(),
        "role-origin",
        Some("H-acct"),
        &crate::recovery::ExplicitAppProjectContext::known(
            project.to_str().unwrap(),
            crate::recovery::AppProjectSource::OpenedDirectory,
        )
        .unwrap(),
    )
    .unwrap();
    host.flush_recovery_observations();
    let durable = host.recorded_recovery_entries();
    assert!(!durable.as_array().unwrap().is_empty());
    assert!(!durable.to_string().contains("chirality.role.supply"));
    assert!(!durable.to_string().contains("Exact common"));
    fn count_role_records(path: &std::path::Path) -> usize {
        let mut count = 0;
        for entry in std::fs::read_dir(path).unwrap() {
            let entry = entry.unwrap();
            if entry.file_type().unwrap().is_dir() {
                count += count_role_records(&entry.path());
            } else if let Ok(text) = std::fs::read_to_string(entry.path()) {
                for line in text.lines() {
                    if let Ok(row) = serde_json::from_str::<Value>(line) {
                        if row.to_string().contains("chirality.role.supply") {
                            count += 1;
                        }
                    }
                }
            }
        }
        count
    }
    let count = count_role_records(&store);
    let cold_host = Arc::new(Host::new());
    cold_host.configure_recovery(ledger).unwrap();
    let cold_generation = {
        let mut i = cold_host.inner.0.lock().unwrap();
        let generation =
            json!({"appSession":i.app_session,"home":"conversation-home","spawnCounter":1});
        i.generation = generation.clone();
        i.home = "conversation-home".into();
        i.spawn_counter = 1;
        i.state = "ready".into();
        generation
    };
    assert_ne!(cold_generation["appSession"], g()["appSession"]);
    let mut cold = HistorySession::default();
    cold.configure_role_log(&project);
    cold.synchronize(&cold_host.snapshot());
    let quoted = cold.read_role_supply("conversation-home", Some("role-origin"));
    assert_eq!(
        quoted["observations"][0]["sourceBytes"]["composed"],
        composition.text
    );
    assert_eq!(quoted["observations"][0]["record"]["adoption"], "unknown");
    assert!(cold_host
        .recorded_recovery_entries()
        .as_array()
        .unwrap()
        .iter()
        .any(|e| e["kind"] == "conversation_index"));
    let query = cold
        .prepare(
            &cold_host.snapshot(),
            &cold_generation,
            0,
            "list",
            None,
            Direction::Desc,
            None,
        )
        .unwrap();
    let mut thread = history_thread("notLoaded");
    thread["id"] = json!("role-origin");
    thread["cwd"] = json!(project);
    let mut receipt = None;
    let (result, _) = role_observations_exchange(
        &cold_host,
        &cold_generation,
        json!({"result":{"data":[thread],"nextCursor":null}}),
        || {
            let r = cold_host.history_dispatch(&query)?;
            let evidence = cold_host.history_wait(&r, Duration::from_millis(100))?;
            receipt = Some(r);
            Ok(evidence)
        },
    );
    assert_eq!(result.unwrap()["writeResult"], "written");
    cold.dispatched(receipt.unwrap());
    cold.reconcile(&cold_host);
    cold.select(&cold_host.snapshot(), &cold_generation, 0, "role-origin")
        .unwrap();
    let query = cold
        .prepare(
            &cold_host.snapshot(),
            &cold_generation,
            1,
            "continue",
            None,
            Direction::Desc,
            None,
        )
        .unwrap();
    let mut resumed = history_resume("idle", true);
    resumed["thread"]["id"] = json!("role-origin");
    resumed["cwd"] = json!(project);
    resumed["thread"]["cwd"] = json!(project);
    let mut receipt = None;
    let (result, outbound) = role_observations_exchange(
        &cold_host,
        &cold_generation,
        json!({"result":resumed}),
        || {
            let r = cold_host.history_dispatch(&query)?;
            let evidence = cold_host.history_wait(&r, Duration::from_millis(100))?;
            receipt = Some(r);
            Ok(evidence)
        },
    );
    assert_eq!(result.unwrap()["writeResult"], "written");
    assert_eq!(outbound["params"], json!({"threadId":"role-origin","excludeTurns":true}));
    cold.dispatched(receipt.unwrap());
    cold.reconcile(&cold_host);
    assert!(cold_host.snapshot()["threads"]
        .as_array()
        .unwrap()
        .iter()
        .any(|r| r["threadId"] == "role-origin"));
    for thread in ["role-origin", "role-fork", "role-continued"] {
        assert_eq!(
            cold.role("conversation-home", thread)["standing"],
            "unknown"
        );
    }
    crate::records_store::use_store_for_test(None);
    assert_eq!(count, 3, "one supply account per actual start/fork");
    std::fs::remove_dir_all(root).unwrap();
}

struct RoleFixture {
    root: PathBuf,
    project: PathBuf,
    host: Arc<Host>,
    history: crate::runtime_session::HistorySession,
    composition: crate::role_supply::Composition,
}
impl RoleFixture {
    fn new() -> Self {
        let root =
            PathBuf::from("/private/tmp").join(crate::util::opaque_id("role-host-test-").unwrap());
        let project = root.join("project");
        std::fs::create_dir_all(&project).unwrap();
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
            root: root.join("store"),
            placement: crate::records_store::Placement::Test,
            limits: vec![],
        })));
        let host = host();
        let mut history = crate::runtime_session::HistorySession::default();
        history.configure_role_log(&project);
        history.synchronize(&host.snapshot());
        use crate::role_supply::{Composition, Guidance, Role};
        let common = Guidance::seeded(
            "AGENTS.md",
            "fixture",
            b"App common\r\n".to_vec(),
            b"default",
        )
        .unwrap();
        let role = Guidance::seeded(
            "agents/AGENT_HELP_HUMAN.md",
            "fixture",
            b"App role\r\n".to_vec(),
            b"default",
        )
        .unwrap();
        let composition =
            Composition::new(&common, Some((Role::HELP_HUMAN, &role)), false).unwrap();
        Self {
            root,
            project,
            host,
            history,
            composition,
        }
    }
    fn start(&mut self, name: &str, supply: &str, response: Option<Value>) -> SourceRequest {
        let mut receipt = None;
        let (result, outbound) = exchange(&self.host, response, vec![], || {
            let r = self.host.thread_start_with_guidance_dispatch(
                &g(),
                self.project.to_str().unwrap(),
                "selected",
                "configured",
                &self.composition.text,
            )?;
            self.history.start_dispatched_selected(
                r.clone(),
                &self.composition,
                supply,
                None,
                None,
            )?;
            let e = self
                .host
                .source_request_wait(&r, Duration::from_millis(100))?;
            receipt = Some(r);
            Ok(e)
        });
        assert_eq!(result.unwrap()["writeResult"], "written");
        assert_eq!(outbound["method"], "thread/start");
        let r = receipt.unwrap();
        self.history.reconcile(&self.host);
        if !name.is_empty() {
            assert_eq!(
                self.history.role("conversation-home", name)["standing"],
                "unknown"
            );
        }
        r
    }
    fn view(&self) -> Value {
        self.history.read_role_supply("conversation-home", None)
    }
}
impl Drop for RoleFixture {
    fn drop(&mut self) {
        crate::records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn role_native(name: &str) -> Value {
    let mut native = history_resume("idle", true);
    native["thread"]["id"] = json!(name);
    native["nativeBase"] = json!("invented private native base sentinel");
    native["nativeTranscript"] = json!("invented private native transcript sentinel");
    native["credentials"] = json!("invented credential sentinel");
    native
}
#[test]
fn actual_unknown_late_error_malformed_and_refusal_keep_source_and_non_adoption() {
    let mut f = RoleFixture::new();
    let receipt = f.start("late-thread", "sup:late", None);
    let first = f.view();
    assert_eq!(first["observations"][0]["record"]["outcome"], "unknown");
    assert_eq!(
        first["observations"][0]["record"]["selection"]["preselected"],
        Value::Null
    );
    let original = first["observations"][0]["record"].clone();
    assert!(f.history.role_publication("conversation-home","late-thread").unwrap().is_none());
    f.host.on_line(
        &serde_json::to_vec(
            &json!({"id":receipt.request_id(),"result":role_native("late-thread")}),
        )
        .unwrap(),
        &g(),
    );
    f.history.reconcile(&f.host);
    assert!(f.history.start_admitted(&receipt));
    assert_eq!(
        f.history.role("conversation-home", "late-thread")["role"],
        "HELP_HUMAN"
    );
    let late = f.view();
    assert_eq!(late["observations"].as_array().unwrap().len(), 2);
    assert_eq!(late["observations"][0]["record"], original);
    assert_eq!(late["observations"][1]["record"]["outcome"], "supplied");
    let publication=f.history.role_publication("conversation-home","late-thread").unwrap().unwrap();
    assert!(publication.verify_target(&f.project,"conversation-home","late-thread").is_ok());
    assert!(publication.reference().contains(late["observations"][1]["record"]["observationId"].as_str().unwrap()));
    assert!(!publication.reference().contains(original["observationId"].as_str().unwrap()));
    f.start(
        "",
        "sup:error",
        Some(json!({"error":{"code":-1,"message":"invented refusal"}})),
    );
    f.start(
        "bad",
        "sup:malformed",
        Some(json!({"result":{"thread":{"id":"bad"}}})),
    );
    f.start(
        "mixed",
        "sup:mixed",
        Some(json!({"result":role_native("mixed"),"error":{"code":-1,"message":"mixed"}})),
    );
    let publication = f.history.role_refused(
        "sup:refused",
        &g(),
        Some(crate::role_supply::Role::TASK),
        Some(false),
        "TASK is not a conversation role; no send",
        true,
    );
    assert_eq!(publication["state"], "written");
    let before = f.view();
    f.history.reconcile(&f.host);
    assert_eq!(f.view(), before);
    assert_eq!(before["observations"].as_array().unwrap().len(), 6);
    assert_eq!(
        before["observations"][2]["record"]["outcome"],
        "request-failed"
    );
    assert_eq!(before["observations"][3]["record"]["outcome"], "unknown");
    assert_eq!(before["observations"][4]["record"]["outcome"], "unknown");
    assert_eq!(
        before["observations"][5]["record"]["outcome"],
        "refused-before-send"
    );
    let stored = before.to_string();
    for secret in [
        "invented private native base sentinel",
        "invented private native transcript sentinel",
        "invented credential sentinel",
    ] {
        assert!(!stored.contains(secret));
    }
    assert!(before["observations"]
        .as_array()
        .unwrap()
        .iter()
        .all(|row| row["record"]["adoption"] == "unknown"));
}
#[test]
fn actual_record_failure_does_not_lose_native_effect_or_retry_after_store_returns() {
    let mut f = RoleFixture::new();
    let mut receipt = None;
    let (result, _) = exchange(
        &f.host,
        Some(json!({"result":role_native("known-native")})),
        vec![],
        || {
            let r = f.host.thread_start_with_guidance_dispatch(
                &g(),
                f.project.to_str().unwrap(),
                "selected",
                "configured",
                &f.composition.text,
            )?;
            f.history.start_dispatched_selected(
                r.clone(),
                &f.composition,
                "sup:write-failure",
                None,
                Some(false),
            )?;
            let e = f.host.source_request_wait(&r, Duration::from_millis(100))?;
            receipt = Some(r);
            Ok(e)
        },
    );
    assert_eq!(result.unwrap()["writeResult"], "written");
    crate::records_store::use_store_for_test(Some(Err("invented persistence failure".into())));
    f.history.reconcile(&f.host);
    let receipt = receipt.unwrap();
    assert!(f.history.start_admitted(&receipt));
    assert_eq!(
        f.history.role("conversation-home", "known-native")["role"],
        "HELP_HUMAN"
    );
    assert_eq!(
        f.history.role_record_status("sup:write-failure")["state"],
        "not-confirmed"
    );
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
        root: f.root.join("store"),
        placement: crate::records_store::Placement::Test,
        limits: vec![],
    })));
    let requests = f.host.client_requests().len();
    f.history.reconcile(&f.host);
    assert_eq!(f.host.client_requests().len(), requests);
    assert_eq!(
        f.history.role_record_status("sup:write-failure")["state"],
        "not-confirmed"
    );
    assert!(f.view()["observations"].as_array().unwrap().is_empty());
}
#[test]
fn actual_late_fork_and_cold_source_unknown_never_assume_role_from_file_or_metadata() {
    let mut f = RoleFixture::new();
    let original = f.start(
        "",
        "sup:origin",
        Some(json!({"result":role_native("source")})),
    );
    assert!(f.history.start_admitted(&original));
    let mut fork = None;
    let (result, outbound) = exchange(&f.host, None, vec![], || {
        let r = f.host.thread_fork_dispatch(&g(), "source")?;
        f.history.fork_dispatched(r.clone(), "source")?;
        let e = f.host.source_request_wait(&r, Duration::from_millis(100))?;
        fork = Some(r);
        Ok(e)
    });
    assert_eq!(result.unwrap()["writeResult"], "written");
    assert_eq!(
        outbound["params"],
        json!({"threadId":"source","deferGoalContinuation":true})
    );
    f.history.reconcile(&f.host);
    let fork = fork.unwrap();
    assert!(f.history.fork_result(&fork).is_none());
    let mut native = role_native("fork");
    native["thread"]["forkedFromId"] = json!("source");
    f.host.on_line(
        &serde_json::to_vec(&json!({"id":fork.request_id(),"result":native})).unwrap(),
        &g(),
    );
    f.history.reconcile(&f.host);
    assert!(f.history.fork_result(&fork).unwrap().is_ok());
    assert_eq!(
        f.history.role("conversation-home", "fork")["role"],
        "HELP_HUMAN"
    );
    assert_eq!(f.view()["observations"].as_array().unwrap().len(), 3);
    let mut cold = crate::runtime_session::HistorySession::default();
    cold.configure_role_log(&f.project);
    assert_eq!(
        cold.role("conversation-home", "source")["standing"],
        "unknown"
    );
    assert_eq!(
        cold.read_role_supply("conversation-home", Some("source"))["observations"][0]["record"]
            ["outcome"],
        "supplied"
    );
    let mut receipt = None;
    let mut native = role_native("cold-fork");
    native["thread"]["forkedFromId"] = json!("source");
    let (result, _) = exchange(&f.host, Some(json!({"result":native})), vec![], || {
        let r = f.host.thread_fork_dispatch(&g(), "source")?;
        cold.fork_dispatched(r.clone(), "source")?;
        let e = f.host.source_request_wait(&r, Duration::from_millis(100))?;
        receipt = Some(r);
        Ok(e)
    });
    assert_eq!(result.unwrap()["writeResult"], "written");
    cold.reconcile(&f.host);
    assert!(cold.fork_result(&receipt.unwrap()).unwrap().is_ok());
    assert_eq!(
        cold.role("conversation-home", "cold-fork")["standing"],
        "unknown"
    );
    let last = cold.read_role_supply("conversation-home", Some("cold-fork"));
    assert_eq!(
        last["observations"][0]["record"]["selection"]["role"],
        "unknown"
    );
    assert_eq!(last["observations"][0]["record"]["outcome"], "unknown");
}
#[test]
fn actual_failed_write_and_superseded_generation_remain_unknown() {
    let mut f = RoleFixture::new();
    install_broken_test_input(&f.host);
    let receipt = f
        .host
        .thread_start_with_guidance_dispatch(
            &g(),
            f.project.to_str().unwrap(),
            "selected",
            "configured",
            &f.composition.text,
        )
        .unwrap();
    f.history
        .start_dispatched(receipt.clone(), &f.composition, "sup:broken")
        .unwrap();
    f.history.reconcile(&f.host);
    let view = f.view();
    assert_eq!(
        view["observations"][0]["record"]["request"]["writeResult"],
        "write-failed"
    );
    assert!(view["observations"][0]["record"].get("carried").is_none());
    assert!(!f.history.start_admitted(&receipt));
    let receipt = f.start("lost", "sup:lost", None);
    {
        let mut i = f.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
        i.generation["spawnCounter"] = json!(2);
        i.state = "ready".into();
    }
    f.history.reconcile(&f.host);
    f.host.on_line(
        &serde_json::to_vec(&json!({"id":receipt.request_id(),"result":role_native("lost")}))
            .unwrap(),
        &g(),
    );
    f.history.reconcile(&f.host);
    assert_eq!(
        f.history.role("conversation-home", "lost")["standing"],
        "unknown"
    );
    assert!(!f.history.start_admitted(&receipt));
    assert!(f.view()["observations"]
        .as_array()
        .unwrap()
        .iter()
        .all(|row| row["record"]["outcome"] == "unknown"));
}

#[test]
fn actual_preselection_flag_and_role_set_identity_are_kept_out_of_native_params() {
    let mut f = RoleFixture::new();
    use crate::role_supply::{Composition, Guidance, Role};
    let mut registry: Value = serde_json::from_slice(crate::role_supply::BUNDLED_ROLE_SET).unwrap();
    for role in registry["roles"].as_array_mut().unwrap() {
        role["default_for_new_chat"] = json!(role["name"] == "HELP_HUMAN");
    }
    let raw = serde_json::to_vec(&registry).unwrap();
    let common = Guidance::seeded(
        "AGENTS.md",
        "fixture",
        b"App common\r\n".to_vec(),
        b"default",
    )
    .unwrap();
    let role = Guidance::seeded(
        "agents/AGENT_HELP_HUMAN.md",
        "fixture",
        b"App role\r\n".to_vec(),
        b"default",
    )
    .unwrap();
    f.composition =
        Composition::with_role_set(&common, Some((Role::HELP_HUMAN, &role)), false, &raw).unwrap();
    let (result, outbound) = exchange(
        &f.host,
        Some(json!({"result":role_native("preselected")})),
        vec![],
        || {
            let receipt = f.host.thread_start_with_guidance_dispatch(
                &g(),
                f.project.to_str().unwrap(),
                "selected",
                "configured",
                &f.composition.text,
            )?;
            f.history.start_dispatched_selected(
                receipt.clone(),
                &f.composition,
                "sup:preselected",
                None,
                Some(true),
            )?;
            f.host
                .source_request_wait(&receipt, Duration::from_millis(100))
        },
    );
    assert_eq!(result.unwrap()["writeResult"], "written");
    assert!(outbound["params"].get("preselected").is_none());
    f.history.reconcile(&f.host);
    let view = f.view();
    assert_eq!(
        view["observations"][0]["record"]["selection"]["preselected"],
        true
    );
    assert_eq!(
        view["observations"][0]["record"]["selection"]["roleSet"],
        crate::role_supply::content(&raw)
    );
}

#[test]
fn actual_early_fork_refusal_records_an_attempt_without_a_native_request() {
    let mut f = RoleFixture::new();
    f.start(
        "",
        "sup:origin",
        Some(json!({"result":role_native("source")})),
    );
    let home = crate::runtime_session::HomeSession::new(
        crate::home_resources::HomeClass::Account,
        f.host.clone(),
        Err("unused fixture config".into()),
    )
    .unwrap();
    *home.history.lock().unwrap() = std::mem::take(&mut f.history);
    let before = f.host.client_requests().len();
    let error = crate::conversation_roles::fork_conversation(
        &home,
        &g(),
        "missing-source",
        Duration::from_millis(10),
    )
    .unwrap_err();
    assert!(error.contains("refused-not-sent") && error.contains("role supply observation"));
    assert_eq!(f.host.client_requests().len(), before);
    let view = home
        .history
        .lock()
        .unwrap()
        .read_role_supply("conversation-home", None);
    let attempt = &view["observations"][1]["record"];
    assert_eq!(attempt["trigger"], "fork");
    assert_eq!(attempt["outcome"], "refused-before-send");
    assert_eq!(attempt["selection"]["role"], "unknown");
    assert_eq!(attempt["request"]["writeResult"], "not-attempted");
    assert_eq!(attempt["request"]["generation"], g());
    assert!(attempt["request"]["requestRef"].is_null());
    assert!(attempt.get("carried").is_none());
    assert!(attempt["thread"].is_null());
}
#[test]
fn resolved_continue_as_refusal_keeps_its_known_relation_and_role_set_without_carrier() {
    let mut f = RoleFixture::new();
    f.start(
        "",
        "sup:origin",
        Some(json!({"result":role_native("source")})),
    );
    let source = f
        .history
        .binding("conversation-home", "source")
        .unwrap()
        .role_in_force("conversation-home", "source");
    let mut handoffs = crate::conversation_roles::Handoffs::default();
    let (id, _) = handoffs
        .reserve(
            &g(),
            "source",
            source,
            Some(crate::role_supply::Role::WORKING_ITEMS),
        )
        .unwrap();
    let relation = handoffs
        .continuation(&id, &g(), Some(crate::role_supply::Role::WORKING_ITEMS))
        .unwrap();
    let before = f.host.client_requests().len();
    let publication = f.history.role_refused_continuing(
        "sup:refused-continuation",
        &g(),
        Some(crate::role_supply::Role::WORKING_ITEMS),
        Some(false),
        "editable guidance file unavailable",
        true,
        Some(relation.clone()),
    );
    assert_eq!(publication["state"], "written");
    assert_eq!(f.host.client_requests().len(), before);
    let view = f.view();
    let row = &view["observations"][1]["record"];
    assert_eq!(row["lineage"]["continuedFrom"], relation);
    assert_eq!(
        row["selection"]["roleSet"],
        crate::role_supply::content(crate::role_supply::BUNDLED_ROLE_SET)
    );
    assert!(row.get("carried").is_none() && row.get("appBytes").is_none());
    assert!(row["request"]["requestIdentity"].is_null());
    assert_eq!(row["outcome"], "refused-before-send");
    assert_eq!(
        view["observations"][1]["lineageObservations"][0]["outcome"],
        "supplied"
    );
}

#[test]
fn actual_host_tick_records_late_start_and_fork_without_web_view_polling() {
    let mut f = RoleFixture::new();
    let start = f.start("", "sup:tick-start", None);
    let home = Arc::new(
        crate::runtime_session::HomeSession::new(
            crate::home_resources::HomeClass::Account,
            f.host.clone(),
            Err("unused fixture config".into()),
        )
        .unwrap(),
    );
    *home.history.lock().unwrap() = std::mem::take(&mut f.history);
    let homes = Mutex::new(crate::runtime_session::HomeRouter::new(home.clone()).unwrap());
    let workflows = Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    let requests = f.host.client_requests().len();
    f.host.on_line(
        &serde_json::to_vec(&json!({"id":start.request_id(),"result":role_native("tick-source")}))
            .unwrap(),
        &g(),
    );
    // This is host_status's history projection. It establishes no new role
    // and writes no observation even though the private reply is now present.
    let projected = home.history.lock().unwrap().snapshot(None);
    assert_eq!(projected["startReceipts"][0]["outcome"], "pending");
    assert_eq!(projected["startReceipts"][0]["waitingEnded"], true);
    assert!(!home.history.lock().unwrap().start_admitted(&start));
    assert_eq!(
        home.history
            .lock()
            .unwrap()
            .read_role_supply("conversation-home", None)["observations"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    // The tick is the only reconciler after the actual reply. There is no
    // host_status/read/history command or web-view polling in this path.
    crate::host_tick::tick_project(&homes, &workflows, Some(&f.project));
    assert!(home.history.lock().unwrap().start_admitted(&start));
    assert_eq!(
        home.history
            .lock()
            .unwrap()
            .role("conversation-home", "tick-source")["role"],
        "HELP_HUMAN"
    );
    assert_eq!(
        f.host.client_requests().len(),
        requests,
        "tick never resends native work"
    );
    let view = home
        .history
        .lock()
        .unwrap()
        .read_role_supply("conversation-home", None);
    assert_eq!(
        view["observations"]
            .as_array()
            .unwrap()
            .iter()
            .map(|r| r["record"]["outcome"].as_str().unwrap())
            .collect::<Vec<_>>(),
        ["unknown", "supplied"]
    );
    let receipts = home.history.lock().unwrap().snapshot(None)["startReceipts"].clone();
    assert_eq!(receipts[0]["supplyRef"], "sup:tick-start");
    assert_eq!(receipts[0]["selection"], "HELP_HUMAN");
    assert_eq!(receipts[0]["carried"], f.composition.carried);
    // The production roleSupply/nativeHistory join after the original call
    // ended unknown. Consumers may render these genuine fixture receipts;
    // this is App/Host evidence, never a native GUI or supplier witness.
    println!(
        "ROLE_LATE_DTO:{}",
        json!({"state":"start-failed-or-unknown","supplyRef":"sup:tick-start","selection":f.composition.role,"roleSet":f.composition.role_set_identity(),"generation":g(),"carried":f.composition.carried,"originalStartReceipts":receipts})
    );
    let (result, frame) = exchange(&f.host, None, vec![], || {
        crate::conversation_roles::fork_conversation(
            &home,
            &g(),
            "tick-source",
            Duration::from_millis(10),
        )
    });
    assert!(result.is_err());
    assert_eq!(frame["method"], "thread/fork");
    assert!(frame["params"].get("developerInstructions").is_none());
    let requests = f.host.client_requests().len();
    let mut native = role_native("tick-fork");
    native["thread"]["forkedFromId"] = json!("tick-source");
    f.host.on_line(
        &serde_json::to_vec(&json!({"id":frame["id"],"result":native})).unwrap(),
        &g(),
    );
    crate::host_tick::tick_project(&homes, &workflows, Some(&f.project));
    assert_eq!(
        home.history
            .lock()
            .unwrap()
            .role("conversation-home", "tick-fork")["role"],
        "HELP_HUMAN"
    );
    for _ in 0..2 {
        crate::host_tick::tick_project(&homes, &workflows, Some(&f.project));
    }
    let view = home
        .history
        .lock()
        .unwrap()
        .read_role_supply("conversation-home", None);
    assert_eq!(
        view["observations"]
            .as_array()
            .unwrap()
            .iter()
            .map(|r| r["record"]["outcome"].as_str().unwrap())
            .collect::<Vec<_>>(),
        ["unknown", "supplied", "unknown", "inherited"]
    );
    assert_eq!(
        f.host.client_requests().len(),
        requests,
        "no native start/fork replay from ticks"
    );
}

#[test]
fn actual_host_tick_keeps_late_closed_or_replaced_generation_unknown() {
    for replaced in [false, true] {
        let mut f = RoleFixture::new();
        let start = f.start("", "sup:tick-closed", None);
        let home = Arc::new(
            crate::runtime_session::HomeSession::new(
                crate::home_resources::HomeClass::Account,
                f.host.clone(),
                Err("unused fixture config".into()),
            )
            .unwrap(),
        );
        *home.history.lock().unwrap() = std::mem::take(&mut f.history);
        let homes = Mutex::new(crate::runtime_session::HomeRouter::new(home.clone()).unwrap());
        let workflows = Mutex::new(crate::runtime_session::WorkflowRootSession::default());
        let requests = f.host.client_requests().len();
        {
            let mut inner = f.host.inner.0.lock().unwrap();
            Host::close_generation(&mut inner);
            if replaced {
                inner.generation["spawnCounter"] = json!(2);
            }
        }
        f.host.on_line(
            &serde_json::to_vec(
                &json!({"id":start.request_id(),"result":role_native("must-not-admit")}),
            )
            .unwrap(),
            &g(),
        );
        crate::host_tick::tick_project(&homes, &workflows, Some(&f.project));
        assert!(!home.history.lock().unwrap().start_admitted(&start));
        assert_eq!(
            home.history
                .lock()
                .unwrap()
                .role("conversation-home", "must-not-admit")["standing"],
            "unknown"
        );
        assert_eq!(f.host.client_requests().len(), requests);
        let view = home
            .history
            .lock()
            .unwrap()
            .read_role_supply("conversation-home", None);
        assert!(view["observations"]
            .as_array()
            .unwrap()
            .iter()
            .all(|r| r["record"]["outcome"] == "unknown"));
    }
}
