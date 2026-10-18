use std::collections::BTreeSet;
// Actual synthetic Host protocol and REC ledger; no supplier or human witness.
fn reopen_clean_root(peer: &Peer) -> Mutex<WorkflowRootSession> {
    let mut root = WorkflowRootSession::default();
    root.set_app_user_data(peer.fixture.root.join("app-data"));
    root.open_library(
        peer.fixture.root.clone(),
        "project",
        peer.project(),
        Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(
            &peer.fixture.root,
        )))),
    )
    .unwrap();
    root.observe_drafts(&json!([])).unwrap();
    Mutex::new(root)
}
fn send_clean(peer: &Peer, root: &Mutex<WorkflowRootSession>) -> String {
    let reference = root
        .lock()
        .unwrap()
        .prepare_trial(
            "clean",
            DRAFT,
            Some((&peer.generation, "thread")),
            Some(&peer.home),
            peer.project(),
        )
        .unwrap()["reference"]
        .as_str()
        .unwrap()
        .to_owned();
    let config = peer.home.host_config.as_ref().unwrap();
    let thread = peer
        .home
        .host
        .thread_start_with_guidance(
            config.cwd.to_str().unwrap(),
            "fixture-model",
            "fixture-provider",
            "existing role unchanged",
        )
        .unwrap()["result"]["thread"]["id"]
        .as_str()
        .unwrap()
        .to_owned();
    let project = crate::recovery::ExplicitAppProjectContext::known(
        "fixture App project",
        crate::recovery::AppProjectSource::ConfiguredDirectory,
    )
    .unwrap();
    peer.home
        .host
        .observe_conversation_project(&peer.generation, &thread, Some("H-acct"), &project)
        .unwrap();
    trial_flows::start_clean_trial(
        root,
        &reference,
        || Ok(json!({"startGeneration":peer.generation,"result":{"thread":{"id":thread}}})),
        |generation, thread| {
            trial_flows::send_trial(
                root,
                &peer.home,
                &reference,
                generation,
                thread,
                "Invented clean input",
            )
        },
    )
    .unwrap();
    reference
}
fn restart_status(root: &Mutex<WorkflowRootSession>, homes: &[Arc<HomeSession>]) -> Value {
    let mut view = historical_trial_snapshot(root);
    trial_flows::decorate_restart_sources(root, homes, &mut view);
    view
}
fn restart_row(status: &Value, reference: &str) -> Value {
    status["drafts"]["drafts"]
        .as_array()
        .unwrap()
        .iter()
        .flat_map(|draft| draft["trials"].as_array().unwrap())
        .find(|row| row["reference"] == reference)
        .unwrap()
        .clone()
}
#[test]
fn clean_trial_restart_actual_host_read_and_feedback() {
    let mut peer = historical_trial_peer();
    let root = Mutex::new(trial_root(&peer));
    let reference = send_clean(&peer, &root);
    let second = send_clean(&peer, &root);
    let hot_home = trial_flows::trial_home(&root, &[peer.home.clone()], &reference).unwrap();
    trial_flows::read_trial_again(&root, &hot_home, &reference, &json!({})).unwrap();
    let old_generation = peer.generation.clone();
    let starts = peer.turn_starts();
    drop(root);
    historical_trial_new_process(&mut peer);
    assert_ne!(peer.generation, old_generation);
    let cold = reopen_clean_root(&peer);
    let homes = [peer.home.clone()];
    let restored = restart_status(&cold, &homes);
    let row = restart_row(&restored, &reference);
    assert_eq!(row["readAgain"]["offered"], true);
    assert!(row["sourceLimit"].is_null());
    assert_eq!(row["authoringConversation"], "thread");
    assert!(row["authoringSourceLimit"]
        .as_str()
        .unwrap()
        .contains("not established"));
    let home = trial_flows::trial_home(&cold, &[peer.home.clone()], &reference).expect(
        "future clean positive ACK must retain a source for explicit post-restart Read again",
    );
    let read = trial_flows::read_trial_again(&cold, &home, &reference, &json!({})).unwrap();
    let after_read = restart_status(&cold, &homes);
    let left = json!({"trial":reference});
    let right = json!({"trial":second});
    let compare =
        trial_flows::compare_with_homes(&cold, &homes, peer.project(), &left, &right).unwrap();
    assert_eq!(compare["left"]["summary"]["turns"], 1, "{compare}");
    let pending = trial_flows::bring_back_with_homes(
        &cold,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        Some(&reference),
        None,
        &peer.generation,
        "thread",
        false,
    )
    .unwrap();
    assert!(pending["id"].is_string());
    let pending_root = restart_status(&cold, &homes);
    assert!(pending_root["pendingBringBacks"][0]["transcript"]
        .as_str()
        .unwrap()
        .contains("Invented historical native result"));
    assert_eq!(
        peer.turn_starts(),
        starts,
        "read and feedback prefill never send"
    );
    assert!(cold.lock().unwrap().runs.is_empty());
    assert!(cold.lock().unwrap().selected.is_empty());
    let result = trial_flows::send_bring_back(
        &cold,
        &peer.home,
        pending["id"].as_str().unwrap(),
        &peer.generation,
        "thread",
        "Invented explicit assessment",
    )
    .unwrap();
    assert_eq!(
        peer.turn_starts(),
        starts + 1,
        "only the separate explicit feedback send dispatches"
    );
    let packet = json!({"restored":restored,"afterRead":after_read,"readResult":read,
        "compare":{"left":left,"right":right,"result":compare},"bringBack":{"result":pending,"root":pending_root},
        "target":{"generation":peer.generation,"threadId":"thread"},"conversations":peer.home.host.snapshot()["threads"],
        "send":{"result":result,"root":restart_status(&cold,&homes),"personText":"Invented explicit assessment"},"reference":reference});
    println!("CLEAN_TRIAL_RESTART_DTO:{}", packet);
}

fn source_link_path(root: &Mutex<WorkflowRootSession>, reference: &str) -> PathBuf {
    let (_, proof) = root.lock().unwrap().trials.source_link(reference).unwrap();
    use std::os::unix::ffi::OsStringExt;
    let bytes: Vec<u8> =
        serde_json::from_value(proof["physical"][0]["path"]["bytes"].clone()).unwrap();
    PathBuf::from(std::ffi::OsString::from_vec(bytes))
}
fn pointer_values(peer: &Peer, reference: &str) -> Vec<String> {
    peer.home
        .host
        .trial_recovery_rows()
        .unwrap()
        .1
        .iter()
        .flat_map(|row| row["tags"].as_array().into_iter().flatten())
        .filter(|tag| tag["owner"] == trial_flows::restart_source::owner(reference))
        .filter_map(|tag| tag["value"].as_str())
        .filter(|raw| {
            serde_json::from_str::<Value>(raw).unwrap()["link"]["trial"]["reference"] == reference
        })
        .map(str::to_owned)
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect()
}
fn history_reads(peer: &Peer) -> usize {
    peer.wire()
        .iter()
        .filter(|frame| {
            matches!(
                frame["method"].as_str(),
                Some("thread/turns/list" | "thread/items/list")
            )
        })
        .count()
}

#[test]
fn clean_trial_restart_exact_link_and_source_negatives() {
    for mode in [
        "link-replaced",
        "link-changed",
        "link-whitespace-changed",
        "link-dir-replaced",
        "native-home-replaced",
        "rec-replaced",
        "conflicting",
        "unsupported",
    ] {
        let mut peer = historical_trial_peer();
        let root = Mutex::new(trial_root(&peer));
        let reference = send_clean(&peer, &root);
        let path = source_link_path(&root, &reference);
        if mode == "conflicting" || mode == "unsupported" {
            let mut pointer: Value =
                serde_json::from_str(&pointer_values(&peer, &reference)[0]).unwrap();
            if mode == "unsupported" {
                pointer["version"] = json!(2);
            } else {
                pointer["generation"]["spawnCounter"] = json!(99);
            }
            let thread = pointer["link"]["trial"]["clean_conversation"]
                .as_str()
                .unwrap();
            let result = peer.home.host.tag_conversation(
                &peer.generation,
                thread,
                Some("H-acct"),
                &trial_flows::restart_source::owner(&reference),
                &pointer.to_string(),
            );
            assert_eq!(result["persistence"], "durable App metadata");
        }
        drop(root);
        historical_trial_new_process(&mut peer);
        let cold = reopen_clean_root(&peer);
        match mode {
            "link-replaced" => {
                let bytes = std::fs::read(&path).unwrap();
                std::fs::rename(&path, path.with_extension("original")).unwrap();
                std::fs::write(&path, bytes).unwrap();
            }
            "link-changed" => {
                let mut value: Value =
                    serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
                value["time"] = json!("different valid time");
                std::fs::write(&path, serde_json::to_vec(&value).unwrap()).unwrap();
            }
            "link-whitespace-changed" => {
                use std::os::unix::fs::MetadataExt;

                let before = std::fs::read(&path).unwrap();
                let metadata = std::fs::metadata(&path).unwrap();
                let mut changed = before.clone();
                changed.extend_from_slice(b" \n\t");
                // Rewrite in place: only exact-byte correspondence may reject this link.
                std::fs::write(&path, changed).unwrap();
                let after = std::fs::read(&path).unwrap();
                let after_metadata = std::fs::metadata(&path).unwrap();
                assert_ne!(before, after);
                assert_eq!(
                    serde_json::from_slice::<Value>(&before).unwrap(),
                    serde_json::from_slice::<Value>(&after).unwrap()
                );
                assert_eq!(metadata.dev(), after_metadata.dev());
                assert_eq!(metadata.ino(), after_metadata.ino());
            }
            "link-duplicate" => {
                std::fs::copy(&path, path.with_file_name("duplicate.json")).unwrap();
            }
            "link-dir-replaced" => {
                let dir = path.parent().unwrap();
                let old = dir.with_extension("original");
                std::fs::rename(dir, &old).unwrap();
                std::fs::create_dir(dir).unwrap();
                for entry in std::fs::read_dir(&old).unwrap() {
                    let p = entry.unwrap().path();
                    std::fs::copy(&p, dir.join(p.file_name().unwrap())).unwrap();
                }
            }
            "native-home-replaced" => {
                let home = &peer.home.host_config.as_ref().unwrap().codex_home;
                std::fs::rename(home, home.with_extension("original")).unwrap();
                std::fs::create_dir(home).unwrap();
            }
            "rec-replaced" => {
                let db = peer.home.host.trial_recovery_rows().unwrap().0;
                std::fs::rename(&db, db.with_extension("original")).unwrap();
                std::fs::write(db, b"not the original REC store").unwrap();
            }
            _ => {}
        }
        let reads = history_reads(&peer);
        let error = trial_flows::trial_home(&cold, &[peer.home.clone()], &reference)
            .err()
            .expect(mode);
        assert!(!error.is_empty());
        assert!(
            trial_flows::bring_back_with_homes(
                &cold,
                &[peer.home.clone()],
                peer.project(),
                &peer.home,
                Some(&reference),
                None,
                &peer.generation,
                "thread",
                false
            )
            .is_err(),
            "{mode}"
        );
        assert_eq!(
            history_reads(&peer),
            reads,
            "{mode}: invalid source must not query"
        );
        assert!(historical_trial_snapshot(&cold)["pendingBringBacks"]
            .as_array()
            .unwrap()
            .is_empty());
    }
}

#[test]
fn clean_trial_restart_metadata_only_retry_keeps_pointer_and_never_resends() {
    for failure in ["before", "after"] {
        let mut peer = historical_trial_peer();
        let root = Mutex::new(trial_root(&peer));
        trial_flows::restart_source::FAIL_METADATA.with(|hook| hook.set(Some(failure)));
        let reference = send_clean(&peer, &root);
        let row = restart_row(&historical_trial_snapshot(&root), &reference);
        assert_eq!(
            row["sourceMetadata"]["state"], "save not confirmed",
            "{row}"
        );
        assert_eq!(row["sourceMetadata"]["persistence"], "not confirmed");
        println!(
            "CLEAN_TRIAL_RESTART_METADATA_DTO:{}",
            json!({"phase":"unconfirmed-held","row":row})
        );
        let observed = pointer_values(&peer, &reference);
        assert_eq!(observed.len(), usize::from(failure == "after"));
        let link = std::fs::read(source_link_path(&root, &reference)).unwrap();
        let starts = peer.turn_starts();
        trial_flows::read_trial_again(&root, &peer.home, &reference, &json!({})).unwrap();
        let saved = pointer_values(&peer, &reference);
        assert_eq!(saved.len(), 1);
        if failure == "after" {
            assert_eq!(
                saved, observed,
                "late metadata retry preserves exact original pointer"
            );
        }
        assert_eq!(
            std::fs::read(source_link_path(&root, &reference)).unwrap(),
            link
        );
        assert_eq!(peer.turn_starts(), starts);
        assert_eq!(
            restart_row(&historical_trial_snapshot(&root), &reference)["sourceMetadata"]
                ["persistence"],
            "durable App metadata"
        );
        drop(root);
        historical_trial_new_process(&mut peer);
        let cold = reopen_clean_root(&peer);
        assert!(trial_flows::trial_home(&cold, &[peer.home.clone()], &reference).is_ok());
    }
}

#[test]
fn clean_trial_restart_changed_link_after_native_wait_prevents_prefill() {
    let mut peer = historical_trial_peer();
    let root = Mutex::new(trial_root(&peer));
    let reference = send_clean(&peer, &root);
    let path = source_link_path(&root, &reference);
    drop(root);
    historical_trial_new_process(&mut peer);
    let cold = reopen_clean_root(&peer);
    let before = restart_status(&cold, &[peer.home.clone()]);
    let queries = peer
        .wire()
        .iter()
        .filter(|f| f["method"] == "thread/turns/list")
        .count();
    peer.set_mode("learning-read-mode", "slow");
    let reason = std::thread::scope(|scope| {
        let request = scope.spawn(|| {
            trial_flows::bring_back_with_homes(
                &cold,
                &[peer.home.clone()],
                peer.project(),
                &peer.home,
                Some(&reference),
                None,
                &peer.generation,
                "thread",
                false,
            )
        });
        historical_trial_wait_for_query(&peer, queries);
        let bytes = std::fs::read(&path).unwrap();
        std::fs::rename(&path, path.with_extension("original")).unwrap();
        std::fs::write(&path, bytes).unwrap();
        request.join().unwrap().unwrap_err()
    });
    let after = restart_status(&cold, &[peer.home.clone()]);
    assert!(after["pendingBringBacks"].as_array().unwrap().is_empty());
    println!(
        "CLEAN_TRIAL_RESTART_REFUSAL_DTO:{}",
        json!({"reason":reason,"rootBefore":before,"rootAfter":after,"reference":reference})
    );
}

#[test]
fn clean_trial_restart_missing_snapshot_is_informative_not_native_source_authority() {
    let mut peer = historical_trial_peer();
    let root = Mutex::new(trial_root(&peer));
    let reference = send_clean(&peer, &root);
    let link = root
        .lock()
        .unwrap()
        .trials
        .link(&reference)
        .unwrap()
        .clone();
    let folder = crate::workflow_workspace::package_copy::content_folder(
        &peer.fixture.root,
        crate::workflow_workspace::TRIAL_AREA,
        DRAFT,
        link["content"]["value"].as_str().unwrap(),
    );
    std::fs::remove_dir_all(&folder).unwrap();
    drop(root);
    historical_trial_new_process(&mut peer);
    let cold = reopen_clean_root(&peer);
    let home = trial_flows::trial_home(&cold, &[peer.home.clone()], &reference).unwrap();
    let result = trial_flows::read_trial_again(&cold, &home, &reference, &json!({})).unwrap();
    assert_eq!(result["recorded"][0]["fidelity"]["state"], "not checked");
    assert!(result.to_string().contains("snapshot"));
    let pending = trial_flows::bring_back_with_homes(
        &cold,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        Some(&reference),
        None,
        &peer.generation,
        "thread",
        false,
    )
    .unwrap();
    assert!(pending["id"].is_string());
    assert_eq!(
        restart_row(&restart_status(&cold, &[peer.home.clone()]), &reference)["snapshot"]["state"],
        "not available"
    );
}

#[test]
fn clean_trial_restart_unrelated_metadata_and_nonutf8_source_are_independent() {
    use std::os::unix::ffi::OsStringExt;
    let mut peer = historical_trial_peer();
    let root = Mutex::new(trial_root(&peer));
    let reference = send_clean(&peer, &root);
    let path = source_link_path(&root, &reference);
    // Neither malformed/large unrelated JSON nor an invalid alias filename is
    // another canonical TrialLink source. They remain listing diagnostics.
    std::fs::write(
        path.parent().unwrap().join("unrelated.json"),
        vec![b'x'; 1024 * 1024],
    )
    .unwrap();
    std::fs::copy(&path, path.parent().unwrap().join("alias.json")).unwrap();
    let thread = root.lock().unwrap().trials.link(&reference).unwrap()["trial"]
        ["clean_conversation"]
        .as_str()
        .unwrap()
        .to_owned();
    let unrelated =
        trial_flows::restart_source::owner("trial:00000000-0000-4000-8000-000000000000");
    assert_eq!(
        peer.home.host.tag_conversation(
            &peer.generation,
            &thread,
            Some("H-acct"),
            &unrelated,
            &"x".repeat(1024 * 1024)
        )["persistence"],
        "durable App metadata"
    );
    drop(root);
    historical_trial_new_process(&mut peer);
    let cold = reopen_clean_root(&peer);
    let status = restart_status(&cold, &[peer.home.clone()]);
    assert!(status["trialPointerLimits"].as_array().unwrap().len() >= 2);
    assert!(trial_flows::trial_home(&cold, &[peer.home.clone()], &reference).is_ok());
    let directory = peer
        .fixture
        .root
        .join(std::ffi::OsString::from_vec(b"native-\xff-source".to_vec()));
    match std::fs::create_dir(&directory) {
        Ok(()) => {
            let file = directory.join("plain");
            std::fs::write(&file, b"source identity").unwrap();
            let identity =
                crate::workflow_workspace::registration::drafts::trials::source_physical(
                    &file, false,
                )
                .unwrap();
            assert_eq!(
                identity[0]["path"],
                crate::attachments::native_path_identity(&file)
            );
        }
        Err(error) if error.raw_os_error() == Some(libc::EILSEQ) => {
            // macOS rejects such a filename before any source exists. The
            // source reader refuses it; the identity encoding is still lossless.
            assert!(
                crate::workflow_workspace::registration::drafts::trials::source_physical(
                    &directory, true
                )
                .is_err()
            );
            assert!(
                crate::attachments::native_path_identity(&directory)["bytes"]
                    .as_array()
                    .unwrap()
                    .contains(&json!(255))
            );
        }
        Err(error) => panic!("unexpected native fixture path failure: {error}"),
    }
}

#[test]
fn clean_trial_restart_positive_producer_rejects_forged_frames_foreign_hosts_and_closed_source() {
    let peer = historical_trial_peer();
    let other = Peer::new();
    let root = Mutex::new(trial_root(&peer));
    let reference = send_clean(&peer, &root);
    let frame = peer
        .wire()
        .into_iter()
        .rev()
        .find(|frame| frame["method"] == "turn/start")
        .unwrap();
    let params = &frame["params"];
    let texts: Vec<_> = params["input"]
        .as_array()
        .unwrap()
        .iter()
        .map(|element| element["text"].as_str().unwrap())
        .collect();
    let thread = params["threadId"].as_str().unwrap();
    let client = params["clientUserMessageId"].as_str().unwrap();
    let positive = peer
        .home
        .host
        .positive_text_start(&peer.generation, &frame["id"], thread, &texts, client)
        .unwrap();
    assert!(other
        .home
        .host
        .check_positive_text_start(&positive)
        .is_err());
    assert!(peer
        .home
        .host
        .positive_text_start(
            &peer.generation,
            &frame["id"],
            thread,
            &["replacement text"],
            client
        )
        .is_err());
    assert!(peer
        .home
        .host
        .positive_text_start(
            &peer.generation,
            &frame["id"],
            thread,
            &texts,
            "foreign client"
        )
        .is_err());
    assert!(peer
        .home
        .host
        .positive_text_start(&peer.generation, &frame["id"], "thread", &texts, client)
        .is_err());
    assert!(peer
        .home
        .host
        .positive_text_start(
            &peer.generation,
            &json!("not-an-actual-request"),
            thread,
            &texts,
            client
        )
        .is_err());
    peer.home
        .host
        .stop("fixture source closure", "test")
        .unwrap();
    assert!(peer.home.host.check_positive_text_start(&positive).is_err());
    assert_eq!(
        pointer_values(&peer, &reference).len(),
        1,
        "a later source closure does not erase saved historical metadata"
    );
    assert!(trial_flows::read_trial_again(&root, &peer.home, &reference, &json!({})).is_err());
    let metadata =
        restart_row(&historical_trial_snapshot(&root), &reference)["sourceMetadata"].clone();
    assert_eq!(metadata["state"], "saved; current revalidation unavailable");
    assert_eq!(
        metadata["persistence"],
        "durable App metadata previously confirmed"
    );
    println!(
        "CLEAN_TRIAL_RESTART_METADATA_DTO:{}",
        json!({"phase":"saved-unavailable","row":restart_row(&historical_trial_snapshot(&root), &reference)})
    );
}

#[test]
fn clean_trial_restart_typed_metadata_retry_after_same_host_child_restart() {
    let mut peer = historical_trial_peer();
    let root = Mutex::new(trial_root(&peer));
    trial_flows::restart_source::FAIL_METADATA.with(|hook| hook.set(Some("before")));
    let reference = send_clean(&peer, &root);
    let original = restart_row(&historical_trial_snapshot(&root), &reference)["sourceMetadata"]
        ["pointerIdentity"]
        .clone();
    let starts = peer.turn_starts();
    peer.home
        .host
        .stop("fixture same Host restart", "test")
        .unwrap();
    let new_generation = peer.relaunch();
    assert_ne!(new_generation, peer.generation);
    // The source thread must be current for tag append, but the pointer and
    // original REC occurrence stay bound to the old full generation.
    peer.home
        .host
        .thread_start_with_guidance(
            peer.fixture.root.to_str().unwrap(),
            "fixture-model",
            "fixture-provider",
            "existing role unchanged",
        )
        .unwrap();
    assert!(
        trial_flows::read_trial_again(&root, &peer.home, &reference, &json!({})).is_err(),
        "hot source is still stale; only metadata is continued"
    );
    let metadata =
        restart_row(&historical_trial_snapshot(&root), &reference)["sourceMetadata"].clone();
    assert_eq!(metadata["state"], "saved", "{metadata}");
    assert_eq!(metadata["pointerIdentity"], original);
    assert_eq!(peer.turn_starts(), starts);
    drop(root);
    peer.generation = new_generation;
    historical_trial_new_process(&mut peer);
    let cold = reopen_clean_root(&peer);
    assert!(trial_flows::trial_home(&cold, &[peer.home.clone()], &reference).is_ok());
}

#[test]
fn clean_trial_restart_original_tag_occurrence_and_native_home_are_required() {
    let mut peer = historical_trial_peer();
    let root = Mutex::new(trial_root(&peer));
    let reference = send_clean(&peer, &root);
    let thread = root.lock().unwrap().trials.link(&reference).unwrap()["trial"]
        ["clean_conversation"]
        .as_str()
        .unwrap()
        .to_owned();
    let old_session = peer.generation["appSession"].clone();
    let ledger = peer
        .fixture
        .root
        .join("app-data/runtime/recovery.ledger.jsonl");
    drop(root);
    historical_trial_new_process(&mut peer);
    let cold = reopen_clean_root(&peer);
    let foreign = Peer::new();
    foreign
        .home
        .host
        .stop(
            "fixture replace Host with shared REC before startup",
            "test",
        )
        .unwrap();
    let foreign_host = Arc::new(crate::hosting::Host::new());
    foreign_host.configure_recovery(ledger).unwrap();
    let foreign_config = foreign.home.host_config.as_ref().unwrap().clone();
    foreign_host
        .start(&foreign_config, "invented other native home sharing REC")
        .unwrap();
    foreign_host
        .thread_start_with_guidance(
            foreign_config.cwd.to_str().unwrap(),
            "fixture-model",
            "fixture-provider",
            "existing role unchanged",
        )
        .unwrap();
    let foreign_home = Arc::new(
        HomeSession::new(
            crate::home_resources::HomeClass::Account,
            foreign_host.clone(),
            Ok(foreign_config),
        )
        .unwrap(),
    );
    let reads = history_reads(&foreign);
    assert!(
        trial_flows::trial_home(&cold, &[foreign_home], &reference).is_err(),
        "same class/shared REC cannot redirect to another actual native home"
    );
    assert_eq!(history_reads(&foreign), reads);
    foreign_host
        .stop("foreign source refusal complete", "test")
        .unwrap();
    let config = peer.home.host_config.as_ref().unwrap();
    peer.home
        .host
        .thread_start_with_guidance(
            config.cwd.to_str().unwrap(),
            "fixture-model",
            "fixture-provider",
            "existing role unchanged",
        )
        .unwrap();
    peer.home.host.tag_conversation(
        &peer.generation,
        &thread,
        Some("H-acct"),
        "fixture-later-tag",
        "unrelated new fact",
    );
    let (database, _) = peer.home.host.trial_recovery_rows().unwrap();
    // Adversarial fixture alters ONLY the synthetic App DB: retain an inherited
    // pointer row, remove the original pointer occurrence, keep original index.
    let connection = rusqlite::Connection::open(&database).unwrap();
    let entries: Vec<(i64, String)> = connection
        .prepare("SELECT seq, entry FROM ledger_entry")
        .unwrap()
        .query_map([], |row| Ok((row.get(0)?, row.get(1)?)))
        .unwrap()
        .map(Result::unwrap)
        .collect();
    connection
        .execute_batch("DROP TRIGGER ledger_entry_never_deleted")
        .unwrap();
    let owner = trial_flows::restart_source::owner(&reference);
    for (sequence, raw) in entries {
        let value: Value = serde_json::from_str(&raw).unwrap();
        if value["session"] == old_session
            && value["tags"]
                .as_array()
                .into_iter()
                .flatten()
                .any(|tag| tag["owner"] == owner)
        {
            connection
                .execute("DELETE FROM ledger_entry WHERE seq = ?1", [sequence])
                .unwrap();
        }
    }
    let error = trial_flows::trial_home(&cold, &[peer.home.clone()], &reference)
        .err()
        .unwrap();
    assert!(error.contains("original-session"), "{error}");
}

#[test]
fn clean_trial_restart_rec_change_after_wait_refuses_compare_and_prefill() {
    for action in ["compare", "bring-back"] {
        let mut peer = historical_trial_peer();
        let root = Mutex::new(trial_root(&peer));
        let reference = send_clean(&peer, &root);
        let second = send_clean(&peer, &root);
        drop(root);
        historical_trial_new_process(&mut peer);
        let cold = reopen_clean_root(&peer);
        let before = restart_status(&cold, &[peer.home.clone()]);
        let queries = peer
            .wire()
            .iter()
            .filter(|frame| frame["method"] == "thread/turns/list")
            .count();
        peer.set_mode("learning-read-mode", "slow");
        let result = std::thread::scope(|scope| {
            let request = scope.spawn(|| {
                if action == "compare" {
                    trial_flows::compare_with_homes(
                        &cold,
                        &[peer.home.clone()],
                        peer.project(),
                        &json!({"trial":reference}),
                        &json!({"trial":second}),
                    )
                } else {
                    trial_flows::bring_back_with_homes(
                        &cold,
                        &[peer.home.clone()],
                        peer.project(),
                        &peer.home,
                        Some(&reference),
                        None,
                        &peer.generation,
                        "thread",
                        false,
                    )
                }
            });
            historical_trial_wait_for_query(&peer, queries);
            let database = peer.home.host.trial_recovery_rows().unwrap().0;
            std::fs::rename(&database, database.with_extension("original")).unwrap();
            std::fs::write(&database, b"replacement cannot supply original REC source").unwrap();
            request.join().unwrap()
        });
        let reason = result.expect_err("changed REC may not publish stale read data");
        if action == "bring-back" {
            println!(
                "CLEAN_TRIAL_RESTART_REFUSAL_DTO:{}",
                json!({"reason":reason,"rootBefore":before,"rootAfter":restart_status(&cold,&[peer.home.clone()]),"reference":reference})
            );
        }
        assert!(historical_trial_snapshot(&cold)["pendingBringBacks"]
            .as_array()
            .unwrap()
            .is_empty());
    }
}

#[test]
fn clean_trial_restart_legacy_and_delegated_cold_sources_stay_unknown() {
    let peer = Peer::new(); // No REC occurrence: never fabricate one from names.
    let root = Mutex::new(trial_root(&peer));
    let clean = send_clean(&peer, &root);
    let unheld = restart_row(&historical_trial_snapshot(&root), &clean);
    assert_eq!(unheld["sourceMetadata"]["heldMetadata"], false);
    println!(
        "CLEAN_TRIAL_RESTART_METADATA_DTO:{}",
        json!({"phase":"unheld","row":unheld})
    );
    let delegated = root
        .lock()
        .unwrap()
        .prepare_trial(
            "delegated",
            DRAFT,
            Some((&peer.generation, "thread")),
            Some(&peer.home),
            peer.project(),
        )
        .unwrap()["reference"]
        .as_str()
        .unwrap()
        .to_owned();
    trial_flows::send_trial(
        &root,
        &peer.home,
        &delegated,
        &peer.generation,
        "thread",
        "Invented delegated request",
    )
    .unwrap();
    drop(root);
    let cold = reopen_clean_root(&peer);
    let status = restart_status(&cold, &[peer.home.clone()]);
    let rows = vec![
        restart_row(&status, &clean),
        restart_row(&status, &delegated),
    ];
    let reads = history_reads(&peer);
    for reference in [&clean, &delegated] {
        assert!(trial_flows::trial_home(&cold, &[peer.home.clone()], reference).is_err());
        assert!(trial_flows::bring_back_with_homes(
            &cold,
            &[peer.home.clone()],
            peer.project(),
            &peer.home,
            Some(reference),
            None,
            &peer.generation,
            "thread",
            false
        )
        .is_err());
    }
    assert_eq!(history_reads(&peer), reads);
    assert!(rows
        .iter()
        .all(|row| row["readAgain"]["offered"] == false && row["sourceLimit"].is_string()));
    println!(
        "CLEAN_TRIAL_RESTART_UNQUALIFIED_DTO:{}",
        json!({"unqualifiedRows":rows})
    );
}

#[test]
fn clean_trial_restart_read_again_rechecks_source_and_link_after_wait() {
    for changed in ["link", "source"] {
        let mut peer = historical_trial_peer();
        let root = Mutex::new(trial_root(&peer));
        let reference = send_clean(&peer, &root);
        let path = source_link_path(&root, &reference);
        drop(root);
        historical_trial_new_process(&mut peer);
        let cold = reopen_clean_root(&peer);
        let before = peer
            .wire()
            .iter()
            .filter(|frame| frame["method"] == "thread/items/list")
            .count();
        peer.set_mode("learning-read-mode", "slow");
        let result = std::thread::scope(|scope| {
            let request = scope
                .spawn(|| trial_flows::read_trial_again(&cold, &peer.home, &reference, &json!({})));
            let until = std::time::Instant::now() + Duration::from_secs(3);
            while peer
                .wire()
                .iter()
                .filter(|frame| frame["method"] == "thread/items/list")
                .count()
                <= before
            {
                assert!(
                    std::time::Instant::now() < until,
                    "owned cold read reached native peer"
                );
                std::thread::sleep(Duration::from_millis(5));
            }
            assert!(
                cold.try_lock().is_ok(),
                "no workflow-root lock across native wait"
            );
            if changed == "link" {
                let bytes = std::fs::read(&path).unwrap();
                std::fs::rename(&path, path.with_extension("original")).unwrap();
                std::fs::write(&path, bytes).unwrap();
            } else {
                peer.home
                    .host
                    .stop("fixture cold source closed during read", "test")
                    .unwrap();
            }
            request.join().unwrap()
        });
        assert!(result.is_err());
        assert!(
            cold.lock()
                .unwrap()
                .trials
                .observations(&reference)
                .is_empty(),
            "no stale fidelity observation appended"
        );
    }
}

#[test]
fn clean_trial_restart_definite_refusal_and_unknown_ack_never_publish_pointer() {
    for mode in ["error", "exit"] {
        let peer = historical_trial_peer();
        let root = Mutex::new(trial_root(&peer));
        let reference = root
            .lock()
            .unwrap()
            .prepare_trial(
                "clean",
                DRAFT,
                Some((&peer.generation, "thread")),
                Some(&peer.home),
                peer.project(),
            )
            .unwrap()["reference"]
            .as_str()
            .unwrap()
            .to_owned();
        let thread = peer.second_thread();
        let project = crate::recovery::ExplicitAppProjectContext::known(
            "fixture App project",
            crate::recovery::AppProjectSource::ConfiguredDirectory,
        )
        .unwrap();
        peer.home
            .host
            .observe_conversation_project(&peer.generation, &thread, Some("H-acct"), &project)
            .unwrap();
        peer.set_mode("turn-mode", mode);
        let result = trial_flows::start_clean_trial(
            &root,
            &reference,
            || Ok(json!({"startGeneration":peer.generation,"result":{"thread":{"id":thread}}})),
            |generation, thread| {
                trial_flows::send_trial(
                    &root,
                    &peer.home,
                    &reference,
                    generation,
                    thread,
                    "Invented refusal control",
                )
            },
        );
        assert!(result.is_err());
        assert!(root.lock().unwrap().trials.link(&reference).is_none());
        assert!(pointer_values(&peer, &reference).is_empty());
        let frame = peer
            .wire()
            .into_iter()
            .rev()
            .find(|frame| frame["method"] == "turn/start")
            .unwrap();
        let texts: Vec<_> = frame["params"]["input"]
            .as_array()
            .unwrap()
            .iter()
            .map(|item| item["text"].as_str().unwrap())
            .collect();
        assert!(peer
            .home
            .host
            .positive_text_start(
                &peer.generation,
                &frame["id"],
                &thread,
                &texts,
                frame["params"]["clientUserMessageId"].as_str().unwrap()
            )
            .is_err());
    }
}
