// Real workflow/observer/read paths with an invented native peer, no supplier.
use crate::records_store;

struct StoreFixture {
    path: PathBuf,
    configured: Option<Result<records_store::Store, String>>,
}
impl StoreFixture {
    fn new() -> Self {
        let path = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("store-controls-lifecycle-").unwrap());
        std::fs::create_dir(&path).unwrap();
        let configured = records_store::configured_for_test();
        records_store::use_store_for_test(Some(Ok(records_store::Store {
            root: path.clone(),
            placement: records_store::Placement::Test,
            limits: vec![],
        })));
        Self { path, configured }
    }
    fn new_process(&self) {
        // The same reset as records_store_tests::new_process, using the
        // existing public test helpers rather than exposing its private module.
        crate::records_index::close_all();
        records_store::restore_configured_for_test(self.configured.clone());
    }
}
impl Drop for StoreFixture {
    fn drop(&mut self) {
        self.new_process();
        records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.path);
    }
}

fn assert_in_place(project: &std::path::Path, step: &str, reading: &Value) {
    let home = records_store::readable_home(project)
        .unwrap_or_else(|e| panic!("{step}: {e}; reading: {reading}"));
    assert!(
        home.in_store().is_none(),
        "{step}: unexpectedly routed to the store"
    );
    assert!(
        !reading.to_string().contains("not known"),
        "{step}: {reading}"
    );
    let (entries, limits) = crate::storage::read_all(project);
    assert!(
        entries.iter().any(|e| e["kind"] == "run_ended"),
        "{step}: {entries:?}, {limits:?}"
    );
    assert!(
        !format!("{limits:?}").contains("not known"),
        "{step}: {limits:?}"
    );
    let status = records_store::status(Some(project));
    assert_eq!(status["project"]["importNeeded"], true, "{step}: {status}");
    assert!(
        !status.to_string().contains("not known"),
        "{step}: {status}"
    );
}

#[test]
fn records_store_app_control_lifecycle_keeps_older_records_in_place() {
    let store = StoreFixture::new();
    let mut peer = Peer::new();
    let project = peer.fixture.root.clone();
    let mut workflow = peer.registered();
    let run = open_run(&peer, &mut workflow, "thread");
    workflow
        .end_plain(&run, &crate::host_tick::receive_view(&peer.home))
        .unwrap();
    assert!(rs_for(&peer, &run).iter().any(|e| e["kind"] == "run_ended"));
    let dir = records_store::attach(&project, false).unwrap().dir.unwrap();
    crate::records_index::close_all();
    // Generate the run beforehand through the real workflow fixture: an
    // attached project with in-place records refuses new workflow writes until
    // imported. Move these genuine bytes to the earlier App's project location;
    // neither run records nor the observer's control are invented by this test.
    let legacy = project.join(".chirality/records");
    std::fs::create_dir_all(&legacy).unwrap();
    for name in ["runs", "acts", "workflow"] {
        if dir.join(name).exists() {
            std::fs::rename(dir.join(name), legacy.join(name)).unwrap();
        }
    }
    assert!(!dir.join("imports.jsonl").exists());
    assert!(!records_store::payload::holds_records(&dir).unwrap());
    store.new_process();

    // The App's startup opens the store and attaches the configured project.
    records_store::current().unwrap();
    records_store::create_at_startup().unwrap();
    let attachment = records_store::attach(&project, true).unwrap();
    assert_eq!(attachment.dir.as_deref(), Some(dir.as_path()));
    assert!(records_store::recover_at_startup().unwrap().is_empty());
    assert_in_place(&project, "first start and attachment", &json!({}));

    // A refused ordinary workflow preparation must not leave an unknown name.
    let attempt = workflow.prepare_run(
        peer.home.clone(),
        &peer.generation,
        "thread",
        "new run refused until import".into(),
        Some(&project),
    );
    let error = match attempt {
        Err(error) => error,
        Ok(reference) => workflow.runs[&reference]
            .lock()
            .unwrap()
            .send()
            .unwrap_err(),
    };
    assert!(error.contains("import needed"), "{error}");
    assert_in_place(&project, "refused workflow write", &json!(error));

    let mut observer = crate::after_run_end::Observer::default();
    observer.observe(&project);
    assert!(
        dir.join(".after-run-end.lock").is_file(),
        "real observer must open its control"
    );
    assert_in_place(&project, "post-end observer tick", &observer.view());

    let capability = crate::records_access::RecordsCapability::new(&project).unwrap();
    for (n, arguments) in [
        json!({"operation":"list_runs"}),
        json!({"operation":"read_run","run":run}),
        json!({"operation":"read_acts"}),
    ]
    .into_iter()
    .enumerate()
    {
        let answer = capability.answer(
            &crate::records_access::Call {
                app_session: "app-session:controls-fixture".into(),
                generation: "generation:controls".into(),
                request: json!(n),
                thread: "thread".into(),
                turn: "turn".into(),
                call: format!("call-{n}"),
                arguments,
            },
            Some(project.to_str().unwrap()),
        );
        assert_eq!(answer["success"], true, "{answer}");
        assert_in_place(&project, &format!("records-tool operation {n}"), &answer);
    }
    assert!(dir.join("reads/records-reads.jsonl").is_file());
    assert_in_place(
        &project,
        "status read",
        &records_store::status(Some(&project)),
    );

    drop(capability);
    drop(observer);
    drop(workflow);
    peer.home
        .host
        .stop_scoped(&peer.generation, "fixture person", "App quit")
        .unwrap();
    peer.home.host.end_process_for_test();
    // Retain only the disk fixture across quit; release the HomeSession and
    // all other runtime objects before resetting the store's process caches.
    let _files = std::mem::replace(
        &mut peer.fixture,
        Fixture {
            root: PathBuf::new(),
            package: PathBuf::new(),
        },
    );
    drop(peer);
    store.new_process();
    assert_in_place(&project, "quit and process reset", &json!({}));

    records_store::current().unwrap();
    records_store::create_at_startup().unwrap();
    records_store::attach(&project, true).unwrap();
    assert!(records_store::recover_at_startup().unwrap().is_empty());
    assert_in_place(&project, "second start and attachment", &json!({}));
    let mut observer = crate::after_run_end::Observer::default();
    observer.observe(&project);
    assert_in_place(&project, "observer tick after restart", &observer.view());
}
