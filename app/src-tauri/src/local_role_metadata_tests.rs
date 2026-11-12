use super::*;

fn task_binding(thread: &str) -> crate::role_lifecycle::RoleBinding {
    use crate::role_supply::{Composition, Guidance, Role};
    let common = Guidance::seeded("AGENTS.md", "fixture-release", b"Invented common guidance".to_vec(), b"Invented common guidance").unwrap();
    let role = Guidance::seeded("agents/AGENT_TASK.md", "fixture-release", b"Invented TASK guidance".to_vec(), b"Invented TASK guidance").unwrap();
    let composition = Composition::new(&common, Some((Role::TASK, &role)), None, true).unwrap();
    let mut native = history_resume("idle", true);
    native["thread"]["id"] = json!(thread);
    crate::role_lifecycle::PreparedStart::new("conversation-home", g(), json!(91), "req:original", "sup:original", &composition).unwrap()
        .observe(&g(), &json!({"id":91,"method":"thread/start","params":{"developerInstructions":composition.text,"cwd":"/invented"}}), &json!({"id":91,"result":native})).unwrap()
}

#[test]
fn local_provider_continue_preserves_role_through_history_reconcile_after_generation_restart() {
    use crate::native_local_provider::{MODEL, PROVIDER};
    let host = host();
    bind_local_history(&host);
    let mut receiver = crate::runtime_session::HistorySession::default();
    receiver.synchronize(&host.snapshot());
    let original = task_binding("stored");
    let original_evidence = original.evidence();
    receiver.bind(original).unwrap();
    let mut generation = g();
    generation["spawnCounter"] = json!(2);
    {
        let mut i = host.inner.0.lock().unwrap();
        i.generation = generation.clone();
        i.journal.begin_generation(generation.clone());
        i.threads.clear();
        i.successor_status.as_mut().unwrap()["verificationGeneration"] = generation.clone();
    }
    receiver.reconcile(&host);
    let history = receiver.history_mut().unwrap();
    let list = history.list_threads(None, crate::native_history::Direction::Desc).unwrap();
    history.receive(&list, "conversation-home", &generation, &json!({"data":[history_thread("notLoaded")],"nextCursor":null})).unwrap();
    history.select("stored").unwrap();
    let query = history.continue_query().unwrap();
    let mut native = history_resume("idle", true);
    native["modelProvider"] = json!(PROVIDER);
    native["model"] = json!(MODEL);
    let (received, frames) = local_peer_exchange(&host, access_provider::tests::local_167_config(), "/invented", native, || -> Result<(), String> {
        let dispatch = host.history_dispatch(&query)?;
        receiver.dispatched(dispatch.clone());
        host.history_wait(&dispatch, Duration::from_secs(2))?;
        receiver.reconcile(&host);
        Ok(())
    });
    received.unwrap();
    assert_eq!(frames.iter().find(|f|f["method"]=="thread/resume").unwrap()["params"], json!({"threadId":"stored","excludeTurns":true,"cwd":"/invented"}));
    assert!(host.snapshot()["threads"].as_array().unwrap().iter().any(|t|t["threadId"]=="stored" && t["generation"]==generation), "known-role Continue must be operationally admitted");
    assert_eq!(receiver.role("conversation-home", "stored")["standing"], "app-observed");
    assert_eq!(receiver.binding("conversation-home", "stored").unwrap().evidence(), original_evidence, "Continue preserves original role bytes and provenance");
    assert!(!receiver.snapshot(None)["receivingLimits"].as_array().unwrap().iter().any(|v|v.as_str().is_some_and(|s|s.contains("resume role evidence refused"))));
}

#[test]
fn local_provider_fork_inherits_role_through_history_reconcile_with_classified_cwd() {
    use crate::native_local_provider::{MODEL, PROVIDER};
    let host = host();
    bind_local_history(&host);
    host.inner.0.lock().unwrap().threads.push(json!({"generation":g(),"threadId":"started","model":MODEL,"modelProvider":PROVIDER,"cwd":"/invented"}));
    let mut receiver = crate::runtime_session::HistorySession::default();
    receiver.synchronize(&host.snapshot());
    let original = task_binding("started");
    let original_evidence = original.evidence();
    receiver.bind(original).unwrap();
    let mut native = history_resume("idle", true);
    native["thread"]["id"] = json!("forked");
    native["thread"]["forkedFromId"] = json!("started");
    native["modelProvider"] = json!(PROVIDER);
    native["model"] = json!(MODEL);
    let (received, frames) = local_peer_exchange(&host, access_provider::tests::local_167_config(), "/invented", native, || -> Result<Value, String> {
        let receipt = host.thread_fork_dispatch(&g(), "started")?;
        receiver.fork_dispatched_with_supply(receipt.clone(), "started", "sup:fork")?;
        host.source_request_wait(&receipt, Duration::from_secs(2))?;
        receiver.reconcile(&host);
        receiver.fork_result(&receipt).ok_or_else(|| "fork reconciliation result absent".to_string())?
    });
    let result = received.unwrap();
    assert_eq!(result["role"]["role"]["standing"], "app-observed", "{result}");
    assert_eq!(frames.iter().find(|f|f["method"]=="thread/fork").unwrap()["params"], json!({"threadId":"started","deferGoalContinuation":true,"cwd":"/invented"}));
    assert_eq!(receiver.role("conversation-home", "forked")["role"], "TASK");
    assert_eq!(receiver.binding("conversation-home", "forked").unwrap().supply_ref(), "sup:fork");
    assert_eq!(receiver.binding("conversation-home", "started").unwrap().evidence(), original_evidence, "fork leaves source guidance unchanged");
}
