#[test]
fn records_store_writer_binding_f4_open_run_keeps_entries_and_end_pending_under_lease() {
    let peer = Peer::new();
    let mut root = declared(&peer);
    let reference = open_run(&peer, &mut root, "thread");
    let owner = root.runs[&reference].clone();
    let project = &peer.fixture.root;
    let log = crate::records::supply::run_log(project, &reference).unwrap();
    let before = std::fs::read(&log).unwrap();
    let registry = crate::records_store::store_root()
        .unwrap()
        .join("roots.jsonl");
    let roots_before = std::fs::read(&registry).unwrap();
    std::fs::write(&registry, b"").unwrap();
    let reason = crate::records_store::attach(project, false)
        .unwrap()
        .refusal
        .unwrap();
    let mut run = owner.lock().unwrap();
    run.observe_checkpoints(&recorder_view(
        &peer,
        &[json!({"id":"m-f4","type":"agentMessage","text":"Spacing report"})],
    ));
    let shown = run.view(&reference);
    let pending: Vec<_> = shown["lifecycle"]["records"]
        .as_array()
        .unwrap()
        .iter()
        .filter(|r| r["written"] == false)
        .cloned()
        .collect();
    assert!(
        pending.len() >= 2,
        "arrival and disposition retained: {}",
        shown["lifecycle"]
    );
    assert!(
        pending[0]["limit"].as_str().unwrap().contains(&reason),
        "{pending:?}"
    );
    assert_eq!(shown["pendingRecords"], true);
    assert_eq!(std::fs::read(&log).unwrap(), before);
    let refused = crate::records_store::adopt(project).unwrap_err();
    assert!(
        refused.contains("still in use"),
        "live lease is not bypassed: {refused}"
    );
    // The open run's next ordinary observation flushes the original queue
    // after outside restoration; no person retry act is needed while open.
    std::fs::write(&registry, &roots_before).unwrap();
    run.observe_checkpoints(&recorder_view(
        &peer,
        &[json!({"id":"m-f4","type":"agentMessage","text":"Spacing report"})],
    ));
    assert!(run.entries.iter().all(|e| !e.pending()));
    assert!(run.retention_activity.is_some());
    // A second outside removal, then an explicit end, exercises the wait
    // after end and the existing App retry button's production method.
    let before = std::fs::read(&log).unwrap();
    std::fs::write(&registry, b"").unwrap();
    run.observe_checkpoints(&recorder_view(
        &peer,
        &[
            json!({"id":"m-f4","type":"agentMessage","text":"Spacing report"}),
            json!({"id":"m-f4-again","type":"agentMessage","text":"Spacing report"}),
        ],
    ));
    assert!(run.entries.iter().any(|e| e.pending()));
    run.end_run(None, None).unwrap();
    assert!(run.lifecycle == RunLifecycle::Ended);
    assert!(run
        .entries
        .iter()
        .any(|e| e.kind == "run_ended" && e.pending()));
    assert!(
        run.retention_activity.is_some(),
        "ending alone keeps the lease while records wait"
    );
    let refused = crate::records_store::adopt(project).unwrap_err();
    assert!(
        refused.contains("still in use"),
        "no adoption even after end while records wait: {refused}"
    );
    run.retry_records().unwrap();
    assert_eq!(std::fs::read(&log).unwrap(), before);
    assert_eq!(std::fs::read(&registry).unwrap(), b"");
    let waiting: Vec<_> = run
        .entries
        .iter()
        .filter(|e| e.pending())
        .map(|e| (e.record_id.clone(), e.body.clone()))
        .collect();
    // Outside restoration of the original roots history, before quitting,
    // restores this same association without changing the held lease.
    std::fs::write(&registry, roots_before).unwrap();
    run.observe_checkpoints(&recorder_view(&peer, &[]));
    assert!(
        run.entries.iter().any(|e| e.pending()),
        "ended runs do not flush on an observation tick"
    );
    run.retry_records().unwrap();
    assert!(run.entries.iter().all(|e| !e.pending()));
    let (written, limits) = crate::records::read_log(&log);
    assert!(limits.is_empty(), "{limits:?}");
    let mut last = None;
    for (id, body) in waiting {
        let at = written.iter().position(|e| e["recordId"] == id).unwrap();
        assert!(
            last.is_none_or(|previous| previous < at),
            "pending entries retain observation order"
        );
        assert_eq!(written[at]["body"], body);
        assert!(written[at + 1..]
            .iter()
            .any(|e| e["kind"] == "evidence_limit"
                && e["body"]["label"] == "record write failed"
                && e["body"]["subjectRef"] == id));
        last = Some(at);
    }
}

#[test]
fn records_store_writer_binding_f4_role_refusal_is_visible_without_pending_retry() {
    let fixture = Fixture::new();
    let project = &fixture.root;
    crate::records::append_project(project, None, "f4", "evidence_limit", &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"retained","detail":"invented F4 history"})).unwrap();
    let dir = crate::records_store::attach(project, false)
        .unwrap()
        .dir
        .unwrap();
    let registry = crate::records_store::store_root()
        .unwrap()
        .join("roots.jsonl");
    std::fs::write(&registry, b"").unwrap();
    let reason = crate::records_store::attach(project, false)
        .unwrap()
        .refusal
        .unwrap();
    let mut history = HistorySession::default();
    history.configure_role_log(project);
    let shown = history.role_refused(
        "sup:f4",
        &json!({"appSession":"f4","home":"fixture","spawnCounter":1}),
        None,
        None,
        "invented pre-send refusal",
        true,
    );
    assert_eq!(shown["state"], "not-confirmed");
    let message = shown["limit"].as_str().unwrap();
    assert!(
        message.contains("not recorded") && message.contains(&reason),
        "{shown}"
    );
    assert_eq!(std::fs::read(&registry).unwrap(), b"");
    assert!(!dir.join("role-supply/observations.jsonl").exists());
}

#[test]
fn records_store_writer_binding_f4_workflow_message_preparation_reports_not_sent() {
    let peer = Peer::new();
    let mut root = peer.registered();
    crate::records::append_project(&peer.fixture.root, None, "f4", "evidence_limit", &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"retained","detail":"invented F4 history"})).unwrap();
    let registry = crate::records_store::store_root()
        .unwrap()
        .join("roots.jsonl");
    std::fs::write(&registry, b"").unwrap();
    let reason = crate::records_store::attach(&peer.fixture.root, false)
        .unwrap()
        .refusal
        .unwrap();
    let error = root
        .prepare_run(
            peer.home.clone(),
            &peer.generation,
            "thread",
            "person text".into(),
            peer.project(),
        )
        .unwrap_err();
    assert!(error.contains(&reason), "{error}");
    assert!(root.runs.is_empty());
    assert_eq!(peer.turn_starts(), 0);
    assert_eq!(std::fs::read(&registry).unwrap(), b"");
}
