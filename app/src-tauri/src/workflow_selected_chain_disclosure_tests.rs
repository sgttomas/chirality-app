// Selected successor B through the actual host_status composition. The local
// synthetic Host supplies original role receipts; no supplier or native act.
fn selected_chain_fixture(bound_role: bool) -> (Peer, Peer, WorkflowRootSession, String, String) {
    selected_chain_fixture_with_declaration(bound_role, false)
}

fn selected_chain_fixture_with_declaration(
    bound_role: bool,
    duplicate: bool,
) -> (Peer, Peer, WorkflowRootSession, String, String) {
    let peer = Peer::new();
    let other = Peer::new();
    let mut root = peer.registered();
    let successor = other.registered_with(|draft| {
        let path = draft.join("WORKFLOW.md");
        let mut declaration: Value =
            serde_json::from_str(crate::checkpoint_recorder::tests::DECLARATION).unwrap();
        declaration["compatible_roles"] = json!(["HELP_HUMAN"]);
        let mut text = std::fs::read_to_string(&path).unwrap();
        let block = format!("\n```workflow-declaration\n{declaration}\n```\n");
        text.push_str(&block);
        if duplicate {
            text.push_str(&block);
        }
        std::fs::write(path, text).unwrap();
    });
    let thread = if bound_role {
        role_r3_start(
            &peer,
            &role_r3_composition(Some(crate::role_supply::Role::WORKING_ITEMS), false),
        )
    } else {
        "thread".into()
    };
    let current = role_r3_open(&peer, &mut root, &thread);
    let (review, revision) = review_of(&successor);
    root.libraries.extend(successor.libraries);
    root.reviews.extend(successor.reviews);
    root.select_hot_registered_copy(
        &crate::workflow_selection::Chat::in_home(&peer.home, &thread),
        &review,
        &revision,
    )
    .unwrap();
    (peer, other, root, thread, current)
}

fn selected_chain_status(root: &Mutex<WorkflowRootSession>, peer: &Peer, view: &Value) -> Value {
    let mut status = peer.home.host.snapshot();
    status["nativeView"] = view.clone();
    status["roleSupply"] = peer.home.role_supply_status.lock().unwrap().clone();
    let (_, history) = crate::host_tick::project_status_history(&peer.home, &mut status, || {
        Err("fixture has no current instruction folder".into())
    });
    let projected_history = status["nativeHistory"].clone();
    let projected_threads = status["threads"].clone();
    status["workflowRoot"] = crate::host_tick::workflow_status_after_history(
        root,
        &peer.home,
        &status["nativeView"],
        true,
        history,
    );
    crate::workflow_selection::publish_context(&mut status, &peer.home);
    assert_eq!(status["nativeHistory"], projected_history);
    assert_eq!(status["threads"], projected_threads);
    status
}

fn selected_row<'a>(status: &'a Value, peer: &Peer, thread: &str) -> &'a Value {
    status["workflowRoot"]["selections"]
        .as_array()
        .unwrap()
        .iter()
        .find(|row| row["sourceRef"] == peer.home.workflow_source_ref && row["threadId"] == thread)
        .unwrap()
}

#[test]
fn selected_chain_actual_status_reports_b_before_the_ordinary_choice() {
    let mut packets = Vec::new();
    for bound_role in [true, false] {
        let (peer, other, root, thread, current) = selected_chain_fixture(bound_role);
        let view = crate::host_tick::receive_view(&peer.home);
        let before = root.snapshot();
        let records = peer.fixture.rs_entries();
        let other_records = other.fixture.rs_entries();
        let files = selected_chain_files(&peer.fixture.root);
        let other_files = selected_chain_files(&other.fixture.root);
        let wire = peer.wire();
        let other_wire = other.wire();
        let root = Mutex::new(root);
        let status = selected_chain_status(&root, &peer, &view);
        let selected = &selected_row(&status, &peer, &thread)["selection"];
        let report = &selected["compatibility"];
        assert!(report.is_object(), "selected B needs its own before-choice advisory; A's run report is not B's: {selected}");
        assert_eq!(report["occasionLabel"], "CK-1 selected candidate");
        assert_eq!(report["publication"]["state"], "not published");
        assert_eq!(
            report["preparation"]["basis"]["generation"],
            peer.generation
        );
        assert_eq!(report["preparation"]["basis"]["conversation"], thread);
        let chat = crate::workflow_selection::Chat::in_home(&peer.home, &thread);
        let guard = root.lock().unwrap();
        let choice = &guard.selected[&chat];
        assert_eq!(selected["reference"], choice.reference);
        assert_eq!(selected["identity"], json!(choice.selection.identity()));
        assert_eq!(report["preparation"]["workflow"], selected["identity"]);
        assert_eq!(
            report["holdingLibrary"],
            choice.package.parent().unwrap().to_str().unwrap()
        );
        assert_ne!(
            guard.runs[&current].lock().unwrap().prepared().workflow(),
            choice.selection.identity()
        );
        assert_eq!(
            guard.runs[&current].lock().unwrap().lifecycle,
            RunLifecycle::Open
        );
        assert_eq!(
            guard.snapshot(),
            before,
            "display cannot select, prepare, end, start or replace a run/header"
        );
        drop(guard);
        let role = &report["preparation"]["role"];
        if bound_role {
            assert_eq!(role["standing"], "app-observed");
            assert_eq!(role["role"], "WORKING_ITEMS");
            assert!(role["supply_ref"].is_string());
            assert_eq!(report["preparation"]["check"]["result"], "unsupported");
        } else {
            assert_eq!(role["standing"], "unknown");
            assert!(role["reason"].as_str().unwrap().contains("not established"));
            assert!(
                role.get("role").is_none(),
                "unknown is never deliberate no-role"
            );
            assert_eq!(report["preparation"]["check"]["result"], "not_established");
        }
        assert!(!report["preparation"]["requirements"]
            .as_array()
            .unwrap()
            .is_empty());
        assert_eq!(
            status["workflowRoot"]["context"]["sourceRef"],
            peer.home.workflow_source_ref
        );
        assert_eq!(
            status["workflowRoot"]["context"]["generation"],
            peer.generation
        );
        assert_eq!(peer.fixture.rs_entries(), records);
        assert_eq!(other.fixture.rs_entries(), other_records);
        assert_eq!(selected_chain_files(&peer.fixture.root), files);
        assert_eq!(selected_chain_files(&other.fixture.root), other_files);
        assert_eq!(peer.wire(), wire, "status sends no native request");
        assert_eq!(other.wire(), other_wire);
        packets.push(
            json!({"case":if bound_role {"fixed-role mismatch"} else {"unknown original role"},
            "threadId":thread,"currentRun":current,"hostStatus":status}),
        );
    }
    println!(
        "SELECTED_CHAIN_DISCLOSURE_DTO:{}",
        json!({"cases":packets,
        "standing":"actual project_status_history → workflow_status_after_history → publish_context; read-only selected B beside open A"})
    );
}

fn selected_chain_files(root: &std::path::Path) -> std::collections::BTreeMap<PathBuf, Vec<u8>> {
    fn read(
        root: &std::path::Path,
        at: &std::path::Path,
        files: &mut std::collections::BTreeMap<PathBuf, Vec<u8>>,
    ) {
        for entry in std::fs::read_dir(at).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                read(root, &path, files);
            } else {
                files.insert(
                    path.strip_prefix(root).unwrap().into(),
                    std::fs::read(path).unwrap(),
                );
            }
        }
    }
    let mut files = std::collections::BTreeMap::new();
    read(root, root, &mut files);
    files
}

fn selected_chain_context(
    status: &Value,
    peer: &Peer,
    thread: &str,
) -> crate::workflow_selection::Context {
    let mut context = status["workflowRoot"]["context"].clone();
    context["threadId"] = json!(thread);
    context["selectionRef"] = selected_row(status, peer, thread)["selection"]["reference"].clone();
    context["inspectionRef"] = status["workflowRoot"]["inspection"]["reference"].clone();
    context["libraryRef"] = status["workflowRoot"]["activeLibrary"].clone();
    serde_json::from_value(context).unwrap()
}

// Existing manual command admission, not a new advisory DTO/authority seam.
fn selected_chain_press(
    root: &Mutex<WorkflowRootSession>,
    peer: &Peer,
    status: &Value,
    thread: &str,
    current: &str,
    project: Option<&std::path::Path>,
) -> Result<String, String> {
    let context = selected_chain_context(status, peer, thread);
    let view = crate::host_tick::receive_view(&peer.home);
    let mut root = root.lock().unwrap();
    let chat = context.verify_home(&peer.home)?.unwrap();
    root.verify_choice_context(&context, Some(&chat))?;
    root.end_and_start_viewed(
        &view,
        current,
        peer.home.clone(),
        &context.generation,
        thread,
        "person's ordinary choice".into(),
        project,
    )
}

#[test]
fn selected_chain_nonpass_unknown_and_unavailable_keep_the_ordinary_choice() {
    for (bound_role, duplicate, unavailable) in [
        (true, false, false),
        (false, false, false),
        (true, true, false),
        (true, false, true),
    ] {
        let (peer, _other, root, thread, current) =
            selected_chain_fixture_with_declaration(bound_role, duplicate);
        let mut view = crate::host_tick::receive_view(&peer.home);
        if unavailable {
            view["generation"]["spawnCounter"] = json!(999);
        }
        let root = Mutex::new(root);
        let status = selected_chain_status(&root, &peer, &view);
        let selected = &selected_row(&status, &peer, &thread)["selection"];
        assert_eq!(selected["runnable"], true);
        if duplicate {
            assert_eq!(
                selected["compatibility"]["preparation"]["declaration"]["reading"],
                "not_established"
            );
            assert_eq!(
                selected["compatibility"]["preparation"]["check"]["result"],
                "not_established"
            );
        }
        if unavailable {
            assert_eq!(selected["compatibility"]["state"], "no evaluation");
            assert!(selected["compatibility"]["limit"].is_string());
            assert!(selected["compatibility"]["preparation"].is_null());
        }
        let before = root.lock().unwrap().snapshot();
        let records = peer.fixture.rs_entries();
        let wire = peer.wire();
        assert!(
            selected_chain_press(&root, &peer, &status, &thread, &current, None)
                .unwrap_err()
                .contains("live run was not ended")
        );
        assert_eq!(
            root.lock().unwrap().snapshot(),
            before,
            "B prerequisites still precede A's end"
        );
        assert_eq!(peer.fixture.rs_entries(), records);
        assert_eq!(peer.wire(), wire);
        let next =
            selected_chain_press(&root, &peer, &status, &thread, &current, peer.project()).unwrap();
        assert_eq!(
            peer.turn_starts(),
            1,
            "disclosure and preparation add no native turn"
        );
        assert_ne!(
            root.lock().unwrap().runs[&current]
                .lock()
                .unwrap()
                .lifecycle,
            RunLifecycle::Open
        );
        {
            let root = root.lock().unwrap();
            let run = root.runs[&next].lock().unwrap();
            assert_eq!(run.follows.as_deref(), Some(current.as_str()));
            assert_eq!(json!(run.prepared().workflow()), selected["identity"]);
            assert_eq!(run.lifecycle, RunLifecycle::Prepared);
            assert_eq!(
                run.prepared().scope().selection_ref,
                selected["reference"].as_str().unwrap()
            );
        }
        start_workflow_run(&root, &next).unwrap();
        let root = root.lock().unwrap();
        let run = root.runs[&next].lock().unwrap();
        assert_eq!(run.lifecycle, RunLifecycle::Open);
        if !unavailable {
            assert_eq!(
                run.view(&next)["compatibility"][0]["preparation"]["role"],
                selected["compatibility"]["preparation"]["role"]
            );
        }
        assert!(peer
            .fixture
            .rs_entries()
            .iter()
            .all(|r| r["kind"] != "compatibility_report_ref"));
    }
}

#[test]
fn selected_chain_genuine_role_contention_stays_unknown_without_replacing_the_fixed_role() {
    let (peer, _other, root, thread, current) = selected_chain_fixture(true);
    let view = crate::host_tick::receive_view(&peer.home);
    let root = Mutex::new(root);
    let status = selected_chain_status(&root, &peer, &view);
    let known = selected_row(&status, &peer, &thread)["selection"]["compatibility"]["preparation"]
        ["role"]
        .clone();
    let before = root.lock().unwrap().snapshot();
    let held = peer.home.history.lock().unwrap();
    let busy = crate::host_tick::workflow_status(&root, &peer.home, &view, true);
    let packet = json!({"workflowRoot":busy});
    let role =
        &selected_row(&packet, &peer, &thread)["selection"]["compatibility"]["preparation"]["role"];
    assert_eq!(role["standing"], "unknown");
    assert!(role["reason"].as_str().unwrap().contains("busy"));
    assert!(role.get("role").is_none());
    drop(held);
    assert_eq!(root.lock().unwrap().snapshot(), before);
    let next =
        selected_chain_press(&root, &peer, &status, &thread, &current, peer.project()).unwrap();
    let root = root.lock().unwrap();
    assert_eq!(
        root.runs[&next].lock().unwrap().view(&next)["compatibility"][0]["preparation"]["role"],
        known
    );
}

#[test]
fn selected_chain_unavailable_original_revision_and_generation_never_substitute_a_or_active_library(
) {
    let (peer, _other, root, thread, current) = selected_chain_fixture(true);
    let view = crate::host_tick::receive_view(&peer.home);
    let root = Mutex::new(root);
    let status = selected_chain_status(&root, &peer, &view);
    let chat = crate::workflow_selection::Chat::in_home(&peer.home, &thread);
    let package = root.lock().unwrap().selected[&chat].package.clone();
    let path = package.join("WORKFLOW.md");
    let original = std::fs::read(&path).unwrap();
    std::fs::write(&path, b"changed selected B, not a different closed choice").unwrap();
    let before = root.lock().unwrap().snapshot();
    let records = peer.fixture.rs_entries();
    let wire = peer.wire();
    let changed = selected_chain_status(&root, &peer, &view);
    let row = &selected_row(&changed, &peer, &thread)["selection"];
    assert_eq!(
        row["identity"],
        selected_row(&status, &peer, &thread)["selection"]["identity"]
    );
    assert_eq!(
        row["reference"],
        selected_row(&status, &peer, &thread)["selection"]["reference"]
    );
    assert_eq!(
        row["runnable"], true,
        "view does not change existing admission semantics"
    );
    assert_eq!(row["compatibility"]["state"], "no evaluation");
    assert!(row["compatibility"]["limit"]
        .as_str()
        .unwrap()
        .contains("revision not verified"));
    assert!(
        selected_chain_press(&root, &peer, &changed, &thread, &current, peer.project()).is_err()
    );
    assert_eq!(root.lock().unwrap().snapshot(), before);
    assert_eq!(
        root.lock().unwrap().runs[&current]
            .lock()
            .unwrap()
            .lifecycle,
        RunLifecycle::Open
    );
    assert_eq!(peer.fixture.rs_entries(), records);
    assert_eq!(peer.wire(), wire);
    std::fs::write(path, original).unwrap();
    let mut foreign = view.clone();
    foreign["generation"]["spawnCounter"] = json!(999);
    let stale = selected_chain_status(&root, &peer, &foreign);
    assert_eq!(
        selected_row(&stale, &peer, &thread)["selection"]["compatibility"]["state"],
        "no evaluation"
    );
    assert!(
        selected_row(&stale, &peer, &thread)["selection"]["compatibility"]["limit"]
            .as_str()
            .unwrap()
            .contains("generation")
    );
    let restored = selected_chain_status(&root, &peer, &view);
    assert_eq!(
        selected_row(&restored, &peer, &thread)["selection"]["compatibility"]["preparation"]
            ["workflow"],
        row["identity"]
    );
}

#[test]
fn selected_chain_same_thread_id_in_another_home_and_no_chat_inspection_are_not_targets() {
    let (peer, other, mut root, thread, _current) = selected_chain_fixture(true);
    let other_thread = role_r3_start(
        &other,
        &role_r3_composition(Some(crate::role_supply::Role::HELP_HUMAN), false),
    );
    assert_eq!(
        thread, other_thread,
        "same bare native ID in disjoint owning Homes"
    );
    let chat = crate::workflow_selection::Chat::in_home(&peer.home, &thread);
    let identity = root.selected[&chat].selection.identity().clone();
    let (review, revision) = root
        .reviews
        .iter()
        .find_map(|(reference, review)| {
            let review = review.lock().unwrap();
            review
                .registered
                .values()
                .any(|r| r.identity() == &identity)
                .then(|| (reference.clone(), identity.revision.clone()))
        })
        .unwrap();
    root.select_hot_registered_copy(
        &crate::workflow_selection::Chat::in_home(&other.home, &other_thread),
        &review,
        &revision,
    )
    .unwrap();
    root.select_development_copy(None, peer.fixture.package.clone())
        .unwrap();
    let peer_view = crate::host_tick::receive_view(&peer.home);
    let other_view = crate::host_tick::receive_view(&other.home);
    let root = Mutex::new(root);
    let before = root.lock().unwrap().snapshot();
    let status = selected_chain_status(&root, &peer, &peer_view);
    assert_eq!(
        selected_row(&status, &peer, &thread)["selection"]["compatibility"]["preparation"]["role"]
            ["role"],
        "WORKING_ITEMS"
    );
    assert!(selected_row(&status, &other, &thread)["selection"]
        .get("compatibility")
        .is_none());
    assert!(status["workflowRoot"]["inspection"]
        .get("compatibility")
        .is_none());
    let status = selected_chain_status(&root, &other, &other_view);
    assert_eq!(
        selected_row(&status, &other, &thread)["selection"]["compatibility"]["preparation"]["role"]
            ["role"],
        "HELP_HUMAN"
    );
    assert!(selected_row(&status, &peer, &thread)["selection"]
        .get("compatibility")
        .is_none());
    assert_eq!(root.lock().unwrap().snapshot(), before);
}
