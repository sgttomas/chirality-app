// WR TT-3b/TT-10/TT-11: private hot source and authoring tuples stay distinct.
// Uses the maintained local protocol peer; no supplier, credential or model.
fn authoring_clean_in(
    author: &Peer,
    trial: &Peer,
    root: &Mutex<WorkflowRootSession>,
    thread: &str,
    with_author: bool,
) -> String {
    let authoring = with_author.then_some((&author.generation, "thread"));
    let reference = root.lock().unwrap().prepare_trial("clean", DRAFT, authoring, Some(&author.home), author.project()).unwrap()["reference"].as_str().unwrap().to_owned();
    trial_flows::start_clean_trial(root, &reference,
        || Ok(json!({"startGeneration":trial.generation,"result":{"thread":{"id":thread}}})),
        |generation, thread| trial_flows::send_trial(root, &trial.home, &reference, generation, thread, "")).unwrap();
    reference
}
fn authoring_status(root: &Mutex<WorkflowRootSession>) -> Value {
    let root = root.lock().unwrap();
    let mut status = root.snapshot();
    root.decorate_status(&mut status, &json!({}));
    status
}
fn authoring_row(status: &Value, reference: &str) -> Value {
    status["drafts"]["drafts"].as_array().unwrap().iter()
        .flat_map(|draft| draft["trials"].as_array().unwrap())
        .find(|row| row["reference"] == reference).unwrap().clone()
}
fn authoring_history_reads(peer: &Peer) -> usize {
    peer.wire().iter().filter(|frame| matches!(frame["method"].as_str(), Some("thread/turns/list" | "thread/items/list"))).count()
}
fn authoring_reopen(peer: &Peer) -> WorkflowRootSession {
    let mut root = WorkflowRootSession::default();
    root.set_app_user_data(peer.fixture.root.join("app-data"));
    let control = Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&peer.fixture.root))));
    root.open_library(peer.fixture.root.clone(), "project", peer.project(), control).unwrap();
    root.observe_drafts(&json!([])).unwrap();
    root
}

#[test]
fn trial_authoring_hot_collision_cold_unknown_and_current_source_packet() {
    let a = Peer::new();
    let b = Peer::new();
    // Both homes contain both the authoring ID and the clean trial's ID.
    a.second_thread();
    let clean = b.second_thread();
    let root = Mutex::new(trial_root(&a));
    let reference = authoring_clean_in(&a, &b, &root, &clean, true);
    let homes = vec![a.home.clone(), b.home.clone()];
    let source = trial_flows::trial_home(&root, &homes, &reference).unwrap();
    assert!(Arc::ptr_eq(&source, &b.home));
    let before = (authoring_history_reads(&a), authoring_history_reads(&b));
    trial_flows::read_trial_again(&root, &source, &reference, &json!({})).unwrap();
    trial_flows::compare_with_homes(&root, &homes, a.project(), &json!({"trial":reference}), &json!({"trial":reference})).unwrap();
    assert_eq!(authoring_history_reads(&a), before.0, "trial history stays in B despite both bare-ID collisions");
    assert!(authoring_history_reads(&b) > before.1);
    let again = trial_flows::trial_again(&root, &reference, &homes, a.project()).unwrap();
    assert_eq!(again["authoring"], json!({"generation":a.generation,"threadId":"thread"}));
    root.lock().unwrap().cancel_trial(again["reference"].as_str().unwrap()).unwrap();
    let run = open_run(&a, &mut root.lock().unwrap(), "thread");
    let hot = authoring_status(&root);
    let hot_row = authoring_row(&hot, &reference);
    // This is a newly acknowledged send, but Peer::new has no REC store:
    // its saved link is not a qualified future restart pointer.
    assert_eq!(hot_row["sourceMetadata"]["heldMetadata"], false);
    assert_eq!(hot_row["sourceMetadata"]["persistence"], "not confirmed");
    assert!(a.home.host.trial_recovery_rows().is_err());
    assert!(b.home.host.trial_recovery_rows().is_err());
    assert_eq!(hot_row["authoringConversation"], again["authoring"]);
    assert_eq!(hot["runBringBackDefaults"][0]["authoring"], again["authoring"]);

    // Reload the genuine saved link without REC evidence: names alone supply no source.
    let cold = Mutex::new(authoring_reopen(&a));
    let cold_row = authoring_row(&authoring_status(&cold), &reference);
    assert_eq!(cold_row["authoringConversation"], "thread");
    assert!(cold_row["sourceLimit"].as_str().unwrap().contains("not established"));
    assert_eq!(cold.lock().unwrap().trials.link(&reference), root.lock().unwrap().trials.link(&reference), "the actual acknowledged link survives reopening unchanged");
    let reads = (authoring_history_reads(&a), authoring_history_reads(&b));
    let starts = (a.turn_starts(), b.turn_starts());
    let source_limit = trial_flows::trial_home(&cold, &homes, &reference).err().expect("an unproven saved link has no native source");
    assert!(trial_flows::trial_home(&cold, std::slice::from_ref(&b.home), &reference).is_err(), "even a unique loaded bare ID supplies no cold source");
    assert!(trial_flows::read_trial_again(&cold, &b.home, &reference, &json!({})).is_err());
    assert!(trial_flows::bring_back_with_homes(&cold, &homes, a.project(), &a.home, Some(&reference), None, &a.generation, "thread", false).is_err());
    let comparison = trial_flows::compare_with_homes(&cold, &homes, a.project(), &json!({"trial":reference}), &json!({"trial":reference})).unwrap();
    for side in ["left", "right"] {
        let summary = &comparison[side]["summary"];
        assert_eq!(summary["turns"], 0);
        assert_eq!(summary["endings"], json!([]));
        assert_eq!(summary["commands"], json!({"run":0,"failed":0,"list":[]}));
        assert_eq!(summary["fileChanges"], json!([]));
        assert!(summary["finalAgentMessage"].is_null());
        let limits = summary["limits"].as_array().unwrap();
        assert!(!limits.is_empty());
        assert!(limits.contains(&json!(source_limit)), "Compare discloses the native-source refusal on each side: {summary}");
    }
    assert!(authoring_status(&cold)["pendingBringBacks"].as_array().unwrap().is_empty(), "source refusal leaves no feedback prefill");
    assert_eq!((a.turn_starts(), b.turn_starts()), starts, "cold inspection sends nothing");
    assert_eq!((authoring_history_reads(&a), authoring_history_reads(&b)), reads, "cold inspection does not query an inferred home");
    let cold_again = trial_flows::trial_again(&cold, &reference, &homes, a.project()).unwrap();
    assert!(cold_again["authoring"].is_null());
    assert!(cold_again["authoringLimit"].as_str().unwrap().contains("not established"));
    cold.lock().unwrap().cancel_trial(cold_again["reference"].as_str().unwrap()).unwrap();

    // A newer saved link must not borrow an older hot trial's authoring default.
    let fresh = b.home.host.thread_start_with_guidance(&b.fixture.root.to_string_lossy(), "fixture-model", "fixture-provider", "existing role unchanged").unwrap()["result"]["thread"]["id"].as_str().unwrap().to_owned();
    let latest = authoring_clean_in(&a, &b, &cold, &fresh, false);
    let authorless_again = trial_flows::trial_again(&cold, &latest, &homes, a.project()).unwrap();
    assert!(authorless_again["authoring"].is_null(), "an explicitly authorless hot clean trial stays authorless");
    assert!(authorless_again["authoringLimit"].is_null(), "known no-author selection is not cold unknown provenance");
    cold.lock().unwrap().cancel_trial(authorless_again["reference"].as_str().unwrap()).unwrap();
    root.lock().unwrap().trials = links(&a);
    let latest_status = authoring_status(&root);
    assert!(latest_status["runBringBackDefaults"].as_array().unwrap().iter().find(|entry| entry["run"] == run).unwrap()["authoring"].is_null());
    assert!(authoring_row(&latest_status, &latest)["sourceLimit"].is_string());

    let packet = json!({"hotTrial":hot_row,"coldTrial":cold_row,"hotDefaults":hot["runBringBackDefaults"],
        "latestUnknownDefaults":latest_status["runBringBackDefaults"],"run":run,"runView":hot["runs"][0],"authoring":again["authoring"],
        "aConversations":a.home.host.snapshot()["threads"],"bConversations":b.home.host.snapshot()["threads"]});
    if let Some(directory) = std::env::var_os("CHIRALITY_TRIAL_AUTHORING_TEST_OUTPUT") {
        std::fs::write(std::path::PathBuf::from(directory).join("trial-authoring.json"), serde_json::to_vec_pretty(&packet).unwrap()).unwrap();
    }
}

#[test]
fn trial_authoring_closed_or_missing_original_never_uses_current_same_id() {
    let a = Peer::new();
    let b = Peer::new();
    let clean = b.second_thread();
    let root = Mutex::new(trial_root(&a));
    let reference = authoring_clean_in(&a, &b, &root, &clean, true);
    let b_only = vec![b.home.clone()];
    let before = b.wire().len();
    assert!(trial_flows::trial_again(&root, &reference, &b_only, a.project()).is_err());
    assert_eq!(b.wire().len(), before, "missing A does not read or select B's authoring ID");
    a.home.host.stop("fixture source closure", "test").unwrap();
    let new_a = a.relaunch();
    assert_ne!(new_a, a.generation);
    let homes = vec![a.home.clone(), b.home.clone()];
    assert!(trial_flows::trial_again(&root, &reference, &homes, a.project()).is_err(), "A's new generation cannot inherit the old default");
    assert!(Arc::ptr_eq(&trial_flows::trial_home(&root, &homes, &reference).unwrap(), &b.home), "closing authoring A does not move the trial's B history");
    // An explicit current target is an ordinary new choice, not old source proof.
    let feedback = trial_flows::bring_back_with_homes(&root, &homes, a.project(), &a.home, Some(&reference), None, &new_a, "thread", false).unwrap();
    let status = authoring_status(&root);
    assert_eq!(status["pendingBringBacks"][0]["target"], json!({"generation":new_a,"threadId":"thread"}));
    trial_flows::cancel_bring_back(&root, feedback["id"].as_str().unwrap()).unwrap();
    b.home.host.stop("fixture source closure", "test").unwrap();
    let new_b = b.relaunch();
    b.second_thread();
    assert_ne!(new_b, b.generation);
    let reads = (authoring_history_reads(&a), authoring_history_reads(&b));
    assert!(trial_flows::trial_home(&root, &homes, &reference).is_err());
    assert!(trial_flows::read_trial_again(&root, &b.home, &reference, &json!({})).is_err());
    assert!(trial_flows::bring_back_with_homes(&root, &homes, a.project(), &a.home, Some(&reference), None, &new_a, "thread", false).is_err());
    assert_eq!((authoring_history_reads(&a), authoring_history_reads(&b)), reads, "closed original source does not query a loaded successor with the same ID");
}

#[test]
fn trial_authoring_feedback_rechecks_source_target_and_link_after_history_wait() {
    for changed in ["source", "target", "link"] {
        let a = Peer::new();
        let b = Peer::new();
        let clean = b.second_thread();
        let root = Mutex::new(trial_root(&a));
        let reference = authoring_clean_in(&a, &b, &root, &clean, true);
        let homes = vec![a.home.clone(), b.home.clone()];
        let starts = (a.turn_starts(), b.turn_starts());
        b.set_mode("items-mode", "hold");
        let result = std::thread::scope(|scope| {
            let request = scope.spawn(|| trial_flows::bring_back_with_homes(&root, &homes, a.project(), &a.home, Some(&reference), None, &a.generation, "thread", false));
            let deadline = std::time::Instant::now() + Duration::from_secs(5);
            while !b.fixture.root.join("items-held").exists() && std::time::Instant::now() < deadline {
                std::thread::sleep(Duration::from_millis(5));
            }
            // The peer's barrier expires after ten seconds and Peer::Drop stops
            // its owned child, including when an assertion aborts this test.
            assert!(b.fixture.root.join("items-held").exists(), "history reached the owned peer barrier");
            match changed {
                "source" => {
                    b.home.host.stop("fixture source changed during history", "test").unwrap();
                    assert_ne!(b.relaunch(), b.generation);
                    b.second_thread();
                }
                "target" => {
                    a.home.host.stop("fixture target changed during history", "test").unwrap();
                    assert_ne!(a.relaunch(), a.generation);
                }
                "link" => {
                    root.lock().unwrap().trials = crate::workflow_workspace::registration::drafts::trials::TrialLinks::open(&a.fixture.root.join("other-trial-store"));
                }
                _ => unreachable!(),
            }
            b.set_mode("items-mode", "");
            request.join().unwrap()
        });
        assert!(result.is_err(), "a changed {changed} cannot publish feedback in another generation");
        assert!(authoring_status(&root)["pendingBringBacks"].as_array().unwrap().is_empty());
        assert_eq!((a.turn_starts(), b.turn_starts()), starts, "a feedback read sends nothing");
    }
}
