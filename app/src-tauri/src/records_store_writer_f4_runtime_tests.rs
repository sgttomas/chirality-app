// Outside damage confined to the first writer admission. The association is
// already restored before the App's next step; only this WR admission failed.
fn refuse_first_wr_binding() {
    use crate::workflow_workspace::publication::{AFTER_INITIAL_WRITER_BINDING, BEFORE_INITIAL_WRITER_BINDING};
    let registry = crate::records_store::store_root().unwrap().join("roots.jsonl");
    let before = std::fs::read(&registry).unwrap();
    let at = registry.clone();
    BEFORE_INITIAL_WRITER_BINDING.with(|slot| *slot.borrow_mut() = Some(Box::new(move || {
        std::fs::write(at, b"").unwrap();
    })));
    AFTER_INITIAL_WRITER_BINDING.with(|slot| *slot.borrow_mut() = Some(Box::new(move || {
        std::fs::write(registry, before).unwrap();
    })));
}

fn assert_unsaved_wr_message(message: &str) {
    for words in ["not saved", "this App process only", "lost on quit", "cannot be saved from within the App", "Original admission refusal:"] {
        assert!(message.contains(words), "missing {words:?}: {message}");
    }
}

#[test]
fn records_store_writer_binding_f4_initial_wr_refusal_says_start_again_and_never_sends() {
    let peer = Peer::new();
    let mut root = declared(&peer);
    refuse_first_wr_binding();
    let reference = root.prepare_run(peer.home.clone(), &peer.generation, "thread", "original text".into(), peer.project()).unwrap();
    let owner = root.runs[&reference].clone();
    let mut run = owner.lock().unwrap();
    let view = run.view(&reference);
    assert!(view["publication"]["state"].as_str().unwrap().contains("not saved"), "{view}");
    let error = run.send().unwrap_err();
    assert_unsaved_wr_message(&error);
    assert!(error.contains("nothing was sent") && error.contains("start again"), "{error}");
    let retried = run.retry_records().unwrap_err();
    assert_unsaved_wr_message(&retried);
    assert_eq!(peer.turn_starts(), 0);
    assert!(peer.fixture.wr_files().is_empty());
    drop(run);
    let fresh = root.prepare_run(peer.home.clone(), &peer.generation, "thread", "original text".into(), peer.project()).unwrap();
    assert_ne!(fresh, reference);
    root.runs[&fresh].lock().unwrap().send().unwrap();
    assert_eq!(peer.turn_starts(), 1, "only the fresh start sends, using the synthetic native peer");
}

#[test]
fn records_store_writer_binding_f4_initial_notice_refusal_is_plain_for_hot_and_reopened_ends() {
    use crate::workflow_workspace::publication::{PreparedEndPublication, ProjectRecords};
    for reopened in [false, true] {
        let peer = Peer::new();
        let mut root = declared(&peer);
        let reference = open_run(&peer, &mut root, "thread");
        let owner = root.runs[&reference].clone();
        let mut run = owner.lock().unwrap();
        run.end_run(None, None).unwrap();
        let project = ProjectRecords::open(&peer.fixture.root).unwrap();
        refuse_first_wr_binding();
        let publication = PreparedEndPublication::for_turn(&project, run.prepared(), run.end.as_ref().unwrap(), run.published.as_ref().unwrap().run_text_record(), WR_WRITER, &crate::util::now_rfc3339(), &peer.generation).unwrap();
        let before = peer.fixture.wr_files();
        if reopened {
            let mut end = ReopenedEnd {
                learning_pointers: Default::default(), home: peer.home.clone(), project,
                run: reference.clone(), conversation: "thread".into(), notice: NoticeState::Prepared(publication),
                notice_record_failure: None, notice_flag: Default::default(), status: Value::Null,
            };
            let view = end.view();
            assert_unsaved_wr_message(view["endNotice"]["admissionRefusal"].as_str().unwrap_or(""));
            let result = end.retry_notice_record().unwrap();
            assert_unsaved_wr_message(result["limit"].as_str().unwrap_or(""));
            assert_eq!(result["retryAvailable"], false, "{result}");
            end.skip_end_notice().unwrap();
        } else {
            run.notice = NoticeState::Prepared(publication);
            let view = run.view(&reference);
            assert_unsaved_wr_message(view["endNotice"]["admissionRefusal"].as_str().unwrap_or(""));
            let result = run.retry_notice_record();
            assert_unsaved_wr_message(result["limit"].as_str().unwrap_or(""));
            assert_eq!(result["retryAvailable"], false, "{result}");
            run.skip_end_notice().unwrap();
        }
        assert_eq!(peer.fixture.wr_files(), before, "the refused notice is never rebound");
        assert_eq!(peer.turn_starts(), 1, "no effect repeats");
        assert!(peer.fixture.rs_entries().iter().any(|e| e["kind"] == "run_ended"));
    }
}

#[test]
fn records_store_writer_binding_f4_initial_check_refusal_says_not_saved_and_retry_cannot_save_it() {
    let peer = Peer::new();
    let mut root = declared(&peer);
    let reference = open_run(&peer, &mut root, "thread");
    peer.select_history();
    let owner = root.runs[&reference].clone();
    let mut run = owner.lock().unwrap();
    run.project = crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    refuse_first_wr_binding();
    let result = run.check_native_supply().unwrap();
    let check = &result["check"];
    assert_unsaved_wr_message(check["publicationLimit"].as_str().unwrap_or(""));
    assert_eq!(check["publicationState"], "not saved; cannot be saved from within the App");
    let id = check["reference"].clone();
    let before = peer.fixture.wr_files();
    let (reads, starts) = (item_reads(&peer), peer.turn_starts());
    let retried = run.retry_records().unwrap();
    assert_unsaved_wr_message(retried["checks"][0]["publicationLimit"].as_str().unwrap_or(""));
    assert_eq!(retried["checks"][0]["reference"], id);
    assert_eq!(peer.fixture.wr_files(), before);
    assert_eq!((item_reads(&peer), peer.turn_starts()), (reads, starts));
    run.check_native_supply().unwrap();
    assert_eq!(run.view(&reference)["checks"][1]["published"], true, "a new check records its new observation, never the original refused check");
    assert!(run.project.resolve(id.as_str().unwrap()).is_err());
}

#[test]
fn records_store_writer_binding_f4_initial_reopened_notice_refusal_keeps_the_saved_end() {
    use crate::workflow_workspace::publication::BEFORE_INITIAL_WRITER_BINDING;
    let peer = Peer::new();
    let mut root = declared(&peer);
    let reference = open_run(&peer, &mut root, "thread");
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let before = std::fs::read(&log).unwrap();
    drop(root);
    let registry = crate::records_store::store_root().unwrap().join("roots.jsonl");
    BEFORE_INITIAL_WRITER_BINDING.with(|slot| *slot.borrow_mut() = Some(Box::new(move || {
        std::fs::write(registry, b"").unwrap();
    })));
    let mut fresh = WorkflowRootSession::default();
    let ended = fresh.end_recorded_run(&peer.fixture.root, &reference, "thread", false, Some(peer.home.clone())).unwrap();
    assert_unsaved_wr_message(ended["endNotice"]["admissionRefusal"].as_str().unwrap_or(""));
    let saved_end = std::fs::read(&log).unwrap();
    assert!(saved_end.starts_with(&before));
    assert!(crate::records::read_log(&log).0.iter().any(|e| e["kind"] == "run_ended"));
    peer.home.host.stop("synthetic fixture", "release the supplier's activity before the confirmation").unwrap();
    crate::records_store::adopt(&peer.fixture.root).unwrap();
    let files = peer.fixture.wr_files();
    let end = fresh.reopened_end(&reference).unwrap();
    let mut end = end.lock().unwrap();
    let retried = end.retry_notice_record().unwrap();
    assert_unsaved_wr_message(retried["limit"].as_str().unwrap_or(""));
    assert_eq!(peer.fixture.wr_files(), files);
    assert_eq!(std::fs::read(&log).unwrap(), saved_end);
    assert_eq!(peer.turn_starts(), 1);
}

#[test]
fn records_store_writer_binding_wr_nonfreezing_persistent_f4_refuses_reopened_end_without_queueing() {
    let peer = Peer::new();
    let mut root = declared(&peer);
    let reference = open_run(&peer, &mut root, "thread");
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let before = std::fs::read(&log).unwrap();
    let registry = crate::records_store::store_root().unwrap().join("roots.jsonl");
    std::fs::write(&registry, b"").unwrap();
    let reason = crate::records_store::attach(&peer.fixture.root, false).unwrap().refusal.unwrap();
    let mut fresh = WorkflowRootSession::default();
    assert!(fresh.end_recorded_run(&peer.fixture.root, &reference, "thread", false, Some(peer.home.clone())).is_err());
    assert_eq!(std::fs::read(&log).unwrap(), before);
    assert!(fresh.runs.is_empty() && fresh.reopened_ends.is_empty() && fresh.notice_flags.is_empty());
    assert!(!crate::records::read_log(&log).0.iter().any(|entry| entry["kind"] == "run_ended"));
    assert!(crate::records_store::write_dir(&peer.fixture.root).unwrap_err().contains(&reason));
}

#[test]
fn records_store_writer_binding_wr_nonfreezing_live_supply_check_retries_after_roots_restoration() {
    let peer = Peer::new();
    let mut root = declared(&peer);
    let reference = open_run(&peer, &mut root, "thread");
    peer.select_history();
    let registry = crate::records_store::store_root().unwrap().join("roots.jsonl");
    let roots = std::fs::read(&registry).unwrap();
    std::fs::write(&registry, b"").unwrap();
    let owner = root.runs[&reference].clone();
    let mut run = owner.lock().unwrap();
    let result = run.check_native_supply().unwrap();
    let check = result["check"].clone();
    assert_eq!(check["published"], false);
    assert!(check["publicationLimit"].as_str().unwrap().contains("project identity kept, not attached"));
    let (reads, starts) = (item_reads(&peer), peer.turn_starts());
    std::fs::write(registry, roots).unwrap();
    let result = run.retry_records().unwrap();
    assert_eq!(result["checks"][0]["published"], true, "{result}");
    assert_eq!(result["checks"][0]["reference"], check["reference"]);
    assert_eq!(result["checks"][0]["readAt"], check["readAt"]);
    assert_eq!((item_reads(&peer), peer.turn_starts()), (reads, starts));
    let record = run.project.resolve(check["reference"].as_str().unwrap()).unwrap();
    assert_eq!(record.body()["read_at"], check["readAt"]);
}

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
