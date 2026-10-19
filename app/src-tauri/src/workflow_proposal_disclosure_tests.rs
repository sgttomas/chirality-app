// Actual production status producer before the existing ordinary choice.
// Existing Root receiving-view fixture; actual local Host role receipts,
// registered snapshots and EXEC evaluator. No real supplier or native act.
#[test]
fn proposed_run_actual_candidate_report_dto_before_choice() {
    let mut packets = Vec::new();
    for bound_role in [false, true] {
        let (peer, root, view) = disclosure_fixture(bound_role);
        let before = root.snapshot();
        let records_before = peer.fixture.rs_entries();
        let workflow_files_before = peer.fixture.wr_files();
        let wire_before = peer.wire();
        let original_offer = root.offers(&view)[0].clone();
        let root = Mutex::new(root);
        let mut status = peer.home.host.snapshot();
        status["nativeView"] = view.clone();
        status["roleSupply"] = peer.home.role_supply_status.lock().unwrap().clone();
        let (instructions, history) =
            crate::host_tick::project_status_history(&peer.home, &mut status, || {
                Err("fixture has no current instruction folder".into())
            });
        let projected_history = status["nativeHistory"].clone();
        let projected_threads = status["threads"].clone();
        assert!(instructions.is_err());
        if bound_role {
            let thread = view["items"][1]["threadId"].as_str().unwrap();
            let row = status["threads"]
                .as_array()
                .unwrap()
                .iter()
                .find(|row| row["threadId"] == thread)
                .unwrap();
            assert_eq!(row["appRole"]["standing"], "app-observed");
            assert_eq!(row["appRole"]["role"], "WORKING_ITEMS");
        }
        status["workflowRoot"] = crate::host_tick::workflow_status_after_history(
            &root,
            &peer.home,
            &status["nativeView"],
            true,
            history,
        );
        assert_eq!(
            status["nativeHistory"], projected_history,
            "workflow composition preserves the history projection"
        );
        assert_eq!(
            status["threads"], projected_threads,
            "workflow composition preserves the thread/role projection"
        );
        let candidate_offer = status["workflowRoot"]["offers"][0].clone();
        let compatibility = &candidate_offer["proposal"]["compatibility"];
        assert_eq!(compatibility["publication"]["state"], "not published");
        if bound_role {
            assert_eq!(compatibility["preparation"]["role"]["standing"],"app-observed",
                "the actual host_status history/workflow composition must not hide its own original role as busy");
            assert!(candidate_offer["proposal"]["context"]["roleSupplyRef"].is_string());
        } else {
            let role = &compatibility["preparation"]["role"];
            assert_eq!(role["standing"], "unknown");
            assert!(role["reason"].as_str().unwrap().contains("not established"));
            assert!(
                role.get("role").is_none(),
                "absent original binding is not deliberate no-role"
            );
            assert!(candidate_offer["proposal"]["context"]["roleSupplyRef"].is_null());
        }
        assert_eq!(
            compatibility["preparation"]["check"]["result"],
            if bound_role {
                "unsupported"
            } else {
                "not_established"
            }
        );
        assert_eq!(
            root.lock().unwrap().snapshot(),
            before,
            "disclosure cannot select, prepare, end or open a run"
        );
        {
            let root = root.lock().unwrap();
            assert!(root.selected.is_empty() && root.runs.is_empty());
        }
        assert_eq!(
            peer.fixture.rs_entries(),
            records_before,
            "no record from disclosure"
        );
        assert_eq!(peer.fixture.wr_files(), workflow_files_before);
        assert_eq!(
            peer.wire(),
            wire_before,
            "no native request or turn from disclosure"
        );
        assert_eq!(
            candidate_offer["proposal"]["context"]["workflow"],
            original_offer["proposal"]["resolution"]["workflow"]
        );
        packets.push(json!({"case":if bound_role {"fixed-role mismatch"} else {"unknown original role"},"generation":peer.generation,
            "originalOffer":original_offer,"offer":candidate_offer,"rootBefore":before,"rootAfter":root.lock().unwrap().snapshot()}));
    }
    println!(
        "PROPOSED_RUN_DISCLOSURE_DTO:{}",
        json!({"cases":packets,"standing":"production host_status history/thread/workflow composition; disclosure is read-only"})
    );
}

fn disclosure_fixture(bound_role: bool) -> (Peer, WorkflowRootSession, Value) {
    let peer = Peer::new();
    let mut root = peer.registered_with(|draft| {
        let path = draft.join("WORKFLOW.md");
        let mut declaration: Value =
            serde_json::from_str(crate::checkpoint_recorder::tests::DECLARATION).unwrap();
        declaration["compatible_roles"] = json!(["HELP_HUMAN"]);
        let mut text = std::fs::read_to_string(&path).unwrap();
        text.push_str(&format!("\n```workflow-declaration\n{declaration}\n```\n"));
        std::fs::write(path, text).unwrap();
    });
    // Setup is complete before observing a proposal. The proposal itself
    // is never inserted into the person's selected state.
    root.selected.clear();
    let thread = if bound_role {
        role_r3_start(
            &peer,
            &role_r3_composition(Some(crate::role_supply::Role::WORKING_ITEMS), false),
        )
    } else {
        "thread".into()
    };
    let mut view = offer_view(
        &peer,
        &[(
            "proposal-turn",
            "proposal-message",
            1,
            PROPOSED,
            "live-observed",
        )],
    );
    for item in view["items"].as_array_mut().unwrap() {
        item["threadId"] = json!(thread);
    }
    (peer, root, view)
}

fn disclosed_offer(root: &WorkflowRootSession, peer: &Peer, view: &Value) -> Value {
    root.offers_for_home(view, &peer.home)[0].clone()
}
fn disclosed_press(
    root: &mut WorkflowRootSession,
    peer: &Peer,
    view: &Value,
    offer: &Value,
) -> Result<String, String> {
    let context: ProposalContext =
        serde_json::from_value(offer["proposal"]["context"].clone()).unwrap();
    root.start_proposed_disclosed(
        view,
        peer.home.clone(),
        &peer.generation,
        &offer["message"],
        offer["proposal"]["runInForce"]["run"].as_str(),
        String::new(),
        peer.project(),
        &context,
    )
}

#[test]
fn proposed_run_disclosure_unknown_and_unsupported_keep_the_ordinary_start() {
    for bound_role in [false, true] {
        let (peer, mut root, view) = disclosure_fixture(bound_role);
        let offer = disclosed_offer(&root, &peer, &view);
        let role = offer["proposal"]["compatibility"]["preparation"]["role"].clone();
        assert!(root.selected.is_empty() && root.runs.is_empty());
        let next = disclosed_press(&mut root, &peer, &view, &offer).unwrap();
        assert_eq!(
            peer.turn_starts(),
            0,
            "preparation remains separate from native dispatch"
        );
        let root = Mutex::new(root);
        start_workflow_run(&root, &next).unwrap();
        assert_eq!(peer.turn_starts(), 1);
        let root = root.lock().unwrap();
        let run = root.runs[&next].lock().unwrap();
        assert_eq!(
            json!(run.prepared().workflow()),
            offer["proposal"]["context"]["workflow"]
        );
        assert_eq!(
            run.view(&next)["compatibility"][0]["preparation"]["role"],
            role
        );
        assert_eq!(
            run.compatibility.len(),
            2,
            "CK-1 and fresh CK-2 remain run evaluations"
        );
        assert_eq!(run.lifecycle, RunLifecycle::Open);
        assert!(peer
            .fixture
            .rs_entries()
            .iter()
            .all(|r| r["kind"] != "compatibility_report_ref"));
    }
}

#[test]
fn proposed_run_disclosure_busy_role_is_unknown_and_does_not_block_original_choice() {
    let (peer, mut root, view) = disclosure_fixture(true);
    let known = disclosed_offer(&root, &peer, &view);
    assert!(known["proposal"]["context"]["roleSupplyRef"].is_string());
    let held = peer.home.history.lock().unwrap();
    let busy = disclosed_offer(&root, &peer, &view);
    let role = &busy["proposal"]["compatibility"]["preparation"]["role"];
    assert_eq!(role["standing"], "unknown");
    assert!(role["reason"].as_str().unwrap().contains("busy"));
    assert!(
        role.get("role").is_none(),
        "Unknown is not deliberate no-role"
    );
    assert!(busy["proposal"]["context"].is_object());
    let next = disclosed_press(&mut root, &peer, &view, &known).unwrap();
    assert_eq!(peer.turn_starts(), 0);
    assert_eq!(
        root.runs[&next].lock().unwrap().lifecycle,
        RunLifecycle::Prepared
    );
    drop(held);
}

#[test]
fn proposed_run_disclosure_refuses_changed_display_context_without_effects() {
    let (peer, mut root, view) = disclosure_fixture(true);
    let offer = disclosed_offer(&root, &peer, &view);
    let before = root.snapshot();
    let records = peer.fixture.rs_entries();
    let wire = peer.wire();
    for change in [
        "source",
        "home",
        "app session",
        "native home",
        "generation",
        "thread",
        "turn",
        "message",
        "proposal",
        "run",
        "library",
        "holding",
        "origin",
        "source root",
        "name",
        "revision",
        "method",
        "lineage",
        "role source",
    ] {
        let mut stale = offer.clone();
        let context = &mut stale["proposal"]["context"];
        match change {
            "source" => context["sourceRef"] = json!("another App source"),
            "home" => context["home"] = json!("another native home"),
            "app session" => context["generation"]["appSession"] = json!("another App session"),
            "native home" => context["generation"]["home"] = json!("another generation home"),
            "generation" => context["generation"]["spawnCounter"] = json!(999),
            "thread" => context["message"]["threadId"] = json!("another thread"),
            "turn" => context["message"]["turnId"] = json!("another turn"),
            "message" => context["message"]["itemId"] = json!("another item"),
            "proposal" => context["proposed"] = json!("user:another-workflow"),
            "run" => context["runRef"] = json!("run:workflow:not-the-displayed-run"),
            "library" => context["libraryRef"] = json!("another opened library"),
            "holding" => context["holdingLibrary"] = json!("/another/holding/library"),
            "origin" => context["workflow"]["origin"] = json!("user"),
            "source root" => context["workflow"]["source_root"] = json!("/another/source/root"),
            "name" => context["workflow"]["name"] = json!("another-workflow"),
            "revision" => context["workflow"]["revision"] = json!("0".repeat(64)),
            "method" => context["workflow"]["revision_method"] = json!("another-method"),
            "lineage" => context["workflow"]["derived_from"] = context["workflow"].clone(),
            "role source" => context["roleSupplyRef"] = json!("sup:another-original-role"),
            _ => unreachable!(),
        }
        assert!(
            disclosed_press(&mut root, &peer, &view, &stale).is_err(),
            "{change}"
        );
        assert_eq!(
            root.snapshot(),
            before,
            "{change}: no selection/preparation/lifecycle change"
        );
        assert_eq!(peer.fixture.rs_entries(), records, "{change}: no record");
        assert_eq!(peer.wire(), wire, "{change}: no native request");
    }
}

#[test]
fn proposed_run_disclosure_supersession_and_foreign_generation_refuse_without_retarget() {
    let (peer, mut root, view) = disclosure_fixture(false);
    let offer = disclosed_offer(&root, &peer, &view);
    let before = root.snapshot();
    let mut newer = view.clone();
    let mut message = newer["items"][1].clone();
    message["native"]["id"] = json!("newer-proposal");
    message["observedOrder"] = json!(2);
    newer["items"].as_array_mut().unwrap().push(message);
    assert!(disclosed_press(&mut root, &peer, &newer, &offer).is_err());
    assert_eq!(root.snapshot(), before);
    let mut foreign = view.clone();
    foreign["generation"]["spawnCounter"] = json!(999);
    assert!(root
        .offers_for_home(&foreign, &peer.home)
        .as_array()
        .unwrap()
        .is_empty());
    assert!(disclosed_press(&mut root, &peer, &foreign, &offer).is_err());
    assert_eq!(root.snapshot(), before);
    root.note_selection(&view, "thread");
    assert!(
        disclosed_press(&mut root, &peer, &view, &offer).is_err(),
        "the person's later choice supersedes the offer (PR-5)"
    );
    assert_eq!(root.snapshot(), before);
    assert_eq!(peer.turn_starts(), 0);
}

#[test]
fn proposed_run_disclosure_chain_keeps_b_prerequisites_before_a_end() {
    let (peer, mut root, _) = disclosure_fixture(false);
    let a = open_run(&peer, &mut root, "thread");
    let view = offer_view(
        &peer,
        &[(
            "proposal-turn",
            "proposal-message",
            1,
            PROPOSED,
            "live-observed",
        )],
    );
    let offer = disclosed_offer(&root, &peer, &view);
    assert_eq!(offer["proposal"]["context"]["runRef"], a);
    let context: ProposalContext =
        serde_json::from_value(offer["proposal"]["context"].clone()).unwrap();
    let before = root.snapshot();
    let records = peer.fixture.rs_entries();
    let wire = peer.wire();
    assert!(root
        .start_proposed_disclosed(
            &view,
            peer.home.clone(),
            &peer.generation,
            &offer["message"],
            Some(&a),
            String::new(),
            None,
            &context
        )
        .is_err());
    assert_eq!(
        root.snapshot(),
        before,
        "failed B prerequisites preserve A and the prior selection"
    );
    assert_eq!(root.runs[&a].lock().unwrap().lifecycle, RunLifecycle::Open);
    assert_eq!(peer.fixture.rs_entries(), records);
    assert_eq!(peer.wire(), wire);
    let b = disclosed_press(&mut root, &peer, &view, &offer).unwrap();
    assert_eq!(
        root.runs[&b].lock().unwrap().follows.as_deref(),
        Some(a.as_str())
    );
    assert_eq!(
        root.runs[&b].lock().unwrap().lifecycle,
        RunLifecycle::Prepared
    );
    assert_ne!(root.runs[&a].lock().unwrap().lifecycle, RunLifecycle::Open);
    let root = Mutex::new(root);
    start_workflow_run(&root, &b).unwrap();
    assert_eq!(
        root.lock().unwrap().runs[&b].lock().unwrap().lifecycle,
        RunLifecycle::Open
    );
}
