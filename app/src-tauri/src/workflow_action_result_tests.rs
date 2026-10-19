// Actual ordinary draft mutation result for the mounted WorkflowRootPanel
// consumer. No registration, native supplier, run, or person's act is involved.
fn action_result_status(root: &Mutex<WorkflowRootSession>, home: &HomeSession) -> Value {
    let mut status = home.host.snapshot();
    status["nativeView"] = crate::host_tick::receive_view(home);
    status["roleSupply"] = home.role_supply_status.lock().unwrap().clone();
    let (_, history) = crate::host_tick::project_status_history(home, &mut status, || {
        Err("fixture has no current instruction folder".into())
    });
    status["workflowRoot"] = crate::host_tick::workflow_status_after_history(
        root,
        home,
        &status["nativeView"],
        true,
        history,
    );
    crate::workflow_selection::publish_context(&mut status, home);
    status
}

// Same fields workflowArguments adds for explicit no-chat inspection.
fn action_result_args(status: &Value, name: &str) -> Value {
    let root = &status["workflowRoot"];
    let mut context = root["context"].clone();
    context["threadId"] = Value::Null;
    context["selectionRef"] = Value::Null;
    context["inspectionRef"] = root["inspection"]["reference"].clone();
    context["libraryRef"] = root["activeLibrary"].clone();
    json!({"name":name,"context":context})
}

// lib.rs workflow_create_draft checks the active Home before Root, rechecks
// Home/choice/library after acquiring Root, then calls create_selected_draft.
// Reuse that existing guarded controller; do not construct a result or bypass
// any of those preconditions. The Tauri State/AppHandle wrapper is not invoked.
fn action_result_create(
    root: &Mutex<WorkflowRootSession>,
    homes: &Mutex<HomeRouter>,
    args: &Value,
) -> Result<Value, String> {
    let context: crate::workflow_selection::Context =
        serde_json::from_value(args["context"].clone()).unwrap();
    crate::workflow_selection::with_choice(
        root,
        &context,
        || homes.lock().unwrap().active(),
        |root, _, chat| {
            root.verify_library_context(&context)?;
            root.create_selected_draft(chat, args["name"].as_str().unwrap())
        },
    )
}

#[test]
fn workflow_action_actual_create_result_precedes_explicit_draft_observation() {
    let fixture = Fixture::new();
    let home = Arc::new(
        HomeSession::new(
            crate::home_resources::HomeClass::Account,
            Arc::new(crate::hosting::Host::new()),
            Err("fixture: no native supplier contact".into()),
        )
        .unwrap(),
    );
    let homes = Mutex::new(HomeRouter::new(home.clone()).unwrap());
    let app_data = fixture.root.join("app-data");
    let mut session = WorkflowRootSession::default();
    session.set_app_user_data(app_data.clone());
    let library = session
        .open_project_library(Some(&fixture.root), Arc::new(Mutex::new(None)))
        .unwrap();
    session
        .select_development_copy(None, fixture.package.clone())
        .unwrap();
    session.observe_drafts(&json!([])).unwrap();
    let base = session
        .inspected
        .as_ref()
        .unwrap()
        .selection
        .identity()
        .clone();
    let source_bytes = session
        .inspected
        .as_ref()
        .unwrap()
        .selection
        .snapshot()
        .files()
        .clone();
    let name = base.name.clone();
    let target = fixture.root.join(".chirality/workflow-drafts").join(&name);
    assert!(
        !target.exists(),
        "ordinary creation starts with an absent target"
    );
    let root = Mutex::new(session);
    let before = action_result_status(&root, &home);
    let args = action_result_args(&before, &name);
    let source_library = before["workflowRoot"]["libraries"]
        .as_array()
        .unwrap()
        .iter()
        .find(|row| row["reference"] == library)
        .unwrap()
        .clone();
    let cached = before["workflowRoot"]["drafts"].clone();
    assert_eq!(cached["drafts"], json!([]));
    let records_before = fixture.rs_entries();
    let wr_before = fixture.wr_files();
    let requests_before = home.host.client_requests();
    // The actual production mutation Value is retained without any amendment.
    let native_result = action_result_create(&root, &homes, &args).unwrap();
    assert_eq!(
        native_result["state"],
        "draft copied from actual closed selection"
    );
    assert_eq!(native_result["library"], library);
    assert_eq!(native_result["name"], name);
    assert_eq!(native_result["base"], json!(base));
    assert_eq!(
        native_result["registration"],
        "not captured/registered; edit then Review"
    );
    assert_eq!(
        crate::workflow_workspace::Snapshot::capture(&target)
            .unwrap()
            .files(),
        &source_bytes
    );
    let base_files: Vec<_> =
        std::fs::read_dir(app_data.join(crate::workflow_workspace::registration::BASE_STORE))
            .unwrap()
            .map(|entry| entry.unwrap().path())
            .filter(|path| !path.file_name().unwrap().to_string_lossy().starts_with('.'))
            .collect();
    assert_eq!(base_files.len(), 1);
    let base_bytes = std::fs::read(&base_files[0]).unwrap();
    let base_record: Value = serde_json::from_slice(&base_bytes).unwrap();
    assert_eq!(base_record["base"], json!(base));
    assert_eq!(base_record["base_recorded_by"], "app");
    assert_eq!(base_record["content"]["value"], base.revision);
    // A status read does not scan the draft folder. The completed file write
    // and receipt exist even while the panel's last draft observation is empty.
    let after_write = action_result_status(&root, &home);
    assert_eq!(after_write["workflowRoot"]["drafts"], cached);
    assert_eq!(
        after_write["workflowRoot"]["context"],
        before["workflowRoot"]["context"]
    );
    assert_eq!(
        after_write["workflowRoot"]["inspection"],
        before["workflowRoot"]["inspection"]
    );
    let before_refusal = root.lock().unwrap().snapshot();
    let refusal = action_result_create(&root, &homes, &args).unwrap_err();
    assert_eq!(refusal, "Existing draft preserved; no overwrite");
    assert_eq!(root.lock().unwrap().snapshot(), before_refusal);
    assert_eq!(
        crate::workflow_workspace::Snapshot::capture(&target)
            .unwrap()
            .files(),
        &source_bytes
    );
    assert_eq!(std::fs::read(&base_files[0]).unwrap(), base_bytes);
    // workflow_observe_drafts uses the same original Home/library checks and
    // Root observation. No selection, preparation, act, or dispatch follows.
    let context: crate::workflow_selection::Context =
        serde_json::from_value(args["context"].clone()).unwrap();
    context
        .verify_home(&homes.lock().unwrap().active())
        .unwrap();
    let view = crate::host_tick::receive_view(&home);
    let observed_result = WorkflowRootSession::with_library_context(
        &root,
        &context,
        || homes.lock().unwrap().active(),
        |root, _| root.observe_drafts(&view["items"]),
    )
    .unwrap();
    let after_observed = action_result_status(&root, &home);
    assert_eq!(
        after_observed["workflowRoot"]["drafts"],
        observed_result["drafts"]
    );
    let row = observed_result["drafts"]["drafts"]
        .as_array()
        .unwrap()
        .iter()
        .find(|row| row["name"] == name)
        .unwrap();
    assert_eq!(row["state"], "draft");
    assert_eq!(row["attribution"], json!({"kind":"app action"}));
    assert_eq!(row["reference"]["base"], json!(base));
    assert_eq!(row["reference"]["base_recorded_by"], "app");
    assert_eq!(row["content"]["value"], base.revision);
    let transitions = observed_result["drafts"]["transitions"].as_array().unwrap();
    assert_eq!(transitions.len(), 1);
    assert_eq!(transitions[0]["event"], "written");
    assert_eq!(transitions[0]["attribution"], json!({"kind":"app action"}));
    assert_eq!(std::fs::read(&base_files[0]).unwrap(), base_bytes);
    assert_eq!(
        crate::workflow_workspace::Snapshot::capture(&target)
            .unwrap()
            .files(),
        &source_bytes
    );
    assert_eq!(fixture.rs_entries(), records_before);
    assert_eq!(fixture.wr_files(), wr_before);
    assert_eq!(home.host.client_requests(), requests_before);
    let session = root.lock().unwrap();
    assert!(session.selected.is_empty() && session.reviews.is_empty() && session.runs.is_empty());
    assert!(!fixture
        .root
        .join(".chirality/workflow-registry.jsonl")
        .exists());
    println!(
        "WORKFLOW_ACTION_RESULT_DTO:{}",
        json!({
            "command":"workflow_create_draft","args":args,
            "source":{"closedBase":base,"library":source_library,"inspection":before["workflowRoot"]["inspection"]},
            "beforeHostStatus":before,"nativeResult":native_result,
            "afterWriteHostStatus":after_write,
            "explicitObservation":{"command":"workflow_observe_drafts","args":{"context":args["context"]},"nativeResult":observed_result},
            "afterObservedHostStatus":after_observed,
            "existingTargetRefusal":{"command":"workflow_create_draft","args":args,"nativeError":refusal},
            "fileEvidence":{"target":crate::attachments::native_path_identity(&target),"exactCopy":true,
                "copiedFiles":source_bytes.keys().collect::<Vec<_>>(),"baseRecord":base_record},
            "standing":{
                "producer":"actual with_choice/verify_library_context → Root.create_selected_draft; unchanged mutation Value",
                "status":"actual absent Host snapshot, native receiving view, history projection/release, workflow status and published context",
                "fixtureInputs":"fresh explicit project and App data directories; closed development-copy inspection; no current instruction folder; projectLibraryAvailable=true",
                "platformLimit":"Tauri State/AppHandle and platform-only App status/setup projections are not invoked or fabricated",
                "effects":"draft bytes and App-kept base only; explicit observation adds the draft list/transition; no human act, registration, run or native request",
                "errorLimit":"existing-target refusal is before copying; generic command rejection can follow partial I/O and does not establish nothing written"
            }
        })
    );
}
