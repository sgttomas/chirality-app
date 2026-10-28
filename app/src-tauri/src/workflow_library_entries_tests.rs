fn entry_package(fixture: &Fixture, name: &str) -> PathBuf {
    let path = fixture.root.join(".chirality/workflows").join(name);
    std::fs::create_dir_all(&path).unwrap();
    std::fs::write(
        path.join("WORKFLOW.md"),
        format!("---\nname: {name}\n---\n# Existing method\nUse the supporting notes.\n"),
    )
    .unwrap();
    std::fs::write(path.join("notes.txt"), b"Existing supporting file\n").unwrap();
    path
}
fn entry_library(root: &WorkflowRootSession) -> Value {
    let status = root.snapshot();
    status["libraries"]
        .as_array()
        .unwrap()
        .iter()
        .find(|library| library["reference"] == status["activeLibrary"])
        .unwrap()
        .clone()
}
#[test]
fn library_entries_opened_unregistered_package_is_discoverable() {
    let fixture = Fixture::new();
    entry_package(&fixture, "sample");
    let mut root = WorkflowRootSession::default();
    root.open_library(
        fixture.root.clone(),
        "project",
        Some(&fixture.root),
        Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(
            &fixture.root,
        )))),
    )
    .unwrap();
    let library = entry_library(&root);
    assert!(library["registered"].as_array().unwrap().is_empty());
    assert!(library["entryListing"]["entries"].as_array().is_some_and(|rows| rows.iter().any(|entry| entry["name"] == "sample" && entry["reviewable"] == true)),
        "Opening a library must expose its actual valid unregistered entry, without typing an undisclosed name: {library}");
}

fn no_supplier_home() -> Arc<HomeSession> {
    Arc::new(
        HomeSession::new(
            crate::home_resources::HomeClass::Account,
            Arc::new(crate::hosting::Host::new()),
            Err("fixture: no native supplier contact".into()),
        )
        .unwrap(),
    )
}
fn opened_entry_root(fixture: &Fixture) -> WorkflowRootSession {
    let mut root = WorkflowRootSession::default();
    root.open_library(
        fixture.root.clone(),
        "project",
        Some(&fixture.root),
        Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(
            &fixture.root,
        )))),
    )
    .unwrap();
    root
}
fn entry_ref(library: &Value, name: &str) -> String {
    library["entryListing"]["entries"]
        .as_array()
        .unwrap()
        .iter()
        .find(|entry| entry["name"] == name)
        .unwrap()["reference"]
        .as_str()
        .unwrap()
        .to_owned()
}
fn entry_host(root: &WorkflowRootSession, home: &HomeSession) -> Value {
    let mut host = home.host.snapshot();
    host["workflowRoot"] = root.snapshot();
    host["nativeHistory"] = home.history.lock().unwrap().snapshot(None);
    crate::workflow_selection::publish_context(&mut host, home);
    host
}
fn entry_selection(library: &Value, refs: &[String]) -> Value {
    json!({"libraryRef":library["reference"],"listingRef":library["entryListing"]["reference"],"entryRefs":refs})
}
fn entry_capture(review: &WorkflowReviewContext) -> crate::act_control::HotA15Result {
    let current = review.review.as_ref().unwrap().current().unwrap();
    let offer = review.offer.as_ref().unwrap();
    let actor =
        crate::act_control::person(Some("synthetic listed-entry fixture"), Some("fixture OS"));
    let context = json!({"library":review.library.reference,"nativeQualification":false});
    let mut control = review.library.control.lock().unwrap();
    let control = control.as_mut().unwrap();
    control
        .a15_confirmation_text(offer, &current, &actor, &context)
        .unwrap();
    control.present_a15(offer).unwrap();
    let event = crate::a15_native::ConfirmedA15Event::synthetic_for_test(
        offer.id().into(),
        control.frozen_a15_offer_digest(offer).unwrap().clone(),
        actor,
        context,
    );
    control
        .confirm_a15_after_native_event(offer, event, &current)
        .unwrap()
}
fn entry_tree(root: &std::path::Path) -> std::collections::BTreeMap<PathBuf, Value> {
    use std::os::unix::fs::MetadataExt;
    fn visit(
        root: &std::path::Path,
        path: &std::path::Path,
        tree: &mut std::collections::BTreeMap<PathBuf, Value>,
    ) {
        let meta = std::fs::symlink_metadata(path).unwrap();
        tree.insert(
            path.strip_prefix(root).unwrap().to_path_buf(),
            json!({"inode":meta.ino(),"modified":meta.mtime(),"nanos":meta.mtime_nsec(),
            "bytes":if meta.is_file(){Some(std::fs::read(path).unwrap())}else{None}}),
        );
        if meta.is_dir() {
            for entry in std::fs::read_dir(path).unwrap() {
                visit(root, &entry.unwrap().path(), tree);
            }
        }
    }
    let mut tree = Default::default();
    visit(root, root, &mut tree);
    tree
}
#[test]
fn library_entries_captured_pending_continuation_preserves_sources_and_settled_outcomes() {
    for settled_state in ["registered", "not completed"] {
        for replacement in ["library", "entry"] {
            let fixture = Fixture::new();
            let settled_path = entry_package(&fixture, "alpha");
            let pending_path = entry_package(&fixture, "beta");
            let mut root = opened_entry_root(&fixture);
            let library = entry_library(&root);
            let refs = ["alpha", "beta"].map(|name| entry_ref(&library, name));
            root.review_library_entries(
                no_supplier_home(),
                json!({}),
                library["reference"].as_str().unwrap(),
                library["entryListing"]["reference"].as_str().unwrap(),
                &refs,
            )
            .unwrap();
            let review_ref = root.active_review.clone().unwrap();
            let mut review = root.reviews[&review_ref].lock().unwrap();
            let result = entry_capture(&review);
            // A durable success or refusal alongside a recoverable storage failure.
            if settled_state == "not completed" {
                std::fs::write(settled_path.join("notes.txt"), b"changed after capture").unwrap();
            }
            let blocker = fixture.root.join(".chirality/workflow-revisions/beta");
            std::fs::create_dir_all(blocker.parent().unwrap()).unwrap();
            std::fs::write(&blocker, b"temporary storage obstruction").unwrap();
            review.attempted_native = true;
            review.accept_result(result).unwrap();
            assert_eq!(review.status["entries"][0]["state"], settled_state);
            assert_eq!(
                review.status["entries"][1]["state"],
                "pending; not registered"
            );
            let settled = review.status["entries"][0].clone();
            let original_act_log =
                std::fs::read(crate::storage::library_log(&fixture.root)).unwrap();
            let offer = review.offer.as_ref().unwrap().id().to_owned();
            let registered_count = usize::from(settled_state == "registered");
            assert_eq!(review.registered.len(), registered_count);
            std::fs::remove_file(blocker).unwrap();
            let path = if replacement == "library" {
                fixture.root.clone()
            } else {
                pending_path
            };
            let original = path.with_extension("original");
            std::fs::rename(&path, &original).unwrap();
            if replacement == "library" {
                std::fs::create_dir(&path).unwrap();
                entry_package(&fixture, "alpha");
                entry_package(&fixture, "beta");
            } else {
                entry_package(&fixture, "beta");
            }
            let replacement_before = entry_tree(&fixture.root);
            let original_before = entry_tree(&original);
            for _ in 0..2 {
                review.advance();
            }
            assert_eq!(review.status["entries"][0], settled);
            assert!(review.status["entries"][1]["reason"]
                .as_str()
                .unwrap()
                .contains("original listed"));
            assert_eq!(
                review.status["entries"][1]["state"],
                "pending; not registered"
            );
            assert_eq!(review.registered.len(), registered_count);
            assert!(
                review.transaction.is_some() && review.review.is_none() && review.attempted_native
            );
            assert_eq!(review.offer.as_ref().unwrap().id(), offer);
            assert_eq!(
                entry_tree(&fixture.root),
                replacement_before,
                "{replacement}: no lock/store/ledger/capture/record writes"
            );
            assert_eq!(entry_tree(&original), original_before);
            std::fs::remove_dir_all(&path).unwrap();
            std::fs::rename(&original, &path).unwrap();
            review.advance();
            assert_eq!(review.status["entries"][0], settled);
            assert_eq!(review.status["entries"][1]["state"], "registered");
            if settled_state == "registered" {
                assert_eq!(
                    review.status["entries"][0]["actRef"],
                    review.status["entries"][1]["actRef"]
                );
            }
            assert_eq!(review.registered.len(), registered_count + 1);
            assert_eq!(
                std::fs::read(crate::storage::library_log(&fixture.root)).unwrap(),
                original_act_log,
                "resuming the original attempt captures or records no second A15"
            );
        }
    }
}
#[test]
fn library_entries_single_and_direct_typed_paths_keep_singular_in_place_registration() {
    for listed in [true, false] {
        let fixture = Fixture::new();
        let path = entry_package(&fixture, "sample");
        let original = crate::workflow_workspace::Snapshot::capture(&path).unwrap();
        let mut root = opened_entry_root(&fixture);
        let home = no_supplier_home();
        if listed {
            let library = entry_library(&root);
            root.review_library_entries(
                home.clone(),
                json!({}),
                library["reference"].as_str().unwrap(),
                library["entryListing"]["reference"].as_str().unwrap(),
                &[entry_ref(&library, "sample")],
            )
            .unwrap();
        } else {
            root.begin_review(home.clone(), json!({}), vec!["sample".into()], true)
                .unwrap();
        }
        let review_ref = root.active_review.clone().unwrap();
        let mut review = root.reviews[&review_ref].lock().unwrap();
        assert_eq!(
            review
                .review
                .as_ref()
                .unwrap()
                .current()
                .unwrap()
                .descriptor_kind(),
            "a15_descriptor"
        );
        assert!(
            review.status["presentation"]["entries"][0]["reviewed_reference"]
                .as_str()
                .unwrap()
                .starts_with("entry:project:sample@")
        );
        let result = entry_capture(&review);
        review.attempted_native = true;
        review.accept_result(result).unwrap();
        assert_eq!(review.status["entries"][0]["state"], "registered");
        let registered = review.registered.values().next().unwrap();
        assert_eq!(
            registered.identity().source_root,
            fixture.root.to_str().unwrap()
        );
        assert_eq!(registered.identity().revision, original.revision());
        assert_eq!(
            crate::workflow_workspace::Snapshot::capture(&path)
                .unwrap()
                .files(),
            original.files()
        );
        assert!(!fixture.root.join(".chirality/workflow-drafts").exists());
        assert!(
            root.selected.is_empty()
                && root.runs.is_empty()
                && home.host.client_requests().is_empty()
        );
    }
}
fn entry_context(
    root: &WorkflowRootSession,
    home: &HomeSession,
) -> crate::workflow_selection::Context {
    let mut context = entry_host(root, home)["workflowRoot"]["context"].clone();
    context["libraryRef"] = json!(root.active_library);
    serde_json::from_value(context).unwrap()
}
#[test]
fn library_entries_commands_refuse_stale_home_generation_history_and_library() {
    let fixture = Fixture::new();
    entry_package(&fixture, "sample");
    let root = Mutex::new(opened_entry_root(&fixture));
    let home = no_supplier_home();
    let other_home = no_supplier_home();
    let library = entry_library(&root.lock().unwrap());
    let context = entry_context(&root.lock().unwrap(), &home);
    let before = root.lock().unwrap().snapshot();
    let files = entry_tree(&fixture.root);
    for operation in ["refresh", "review"] {
        for change in ["home source", "generation", "history", "library"] {
            let mut stale = context.clone();
            match change {
                "home source" => stale.source_ref = other_home.workflow_source_ref.clone(),
                "generation" => stale.generation = json!({"stale":true}),
                "history" => stale.history_epoch = Some(u64::MAX),
                "library" => stale.library_ref = Some("not the displayed library".into()),
                _ => unreachable!(),
            }
            let result = WorkflowRootSession::with_library_context(
                &root,
                &stale,
                || home.clone(),
                |root, home| {
                    if operation == "refresh" {
                        root.observe_library_entries(library["reference"].as_str().unwrap())
                    } else {
                        root.review_library_entries(
                            home,
                            json!({}),
                            library["reference"].as_str().unwrap(),
                            library["entryListing"]["reference"].as_str().unwrap(),
                            &[entry_ref(&library, "sample")],
                        )
                    }
                },
            );
            assert!(result.is_err(), "{operation}/{change}");
            assert_eq!(root.lock().unwrap().snapshot(), before);
            assert_eq!(entry_tree(&fixture.root), files);
        }
    }
}
#[test]
fn library_entries_queued_command_rechecks_home_after_waiting_for_root() {
    let fixture = Fixture::new();
    entry_package(&fixture, "sample");
    let root = Arc::new(Mutex::new(opened_entry_root(&fixture)));
    let home = no_supplier_home();
    let other_home = no_supplier_home();
    let context = entry_context(&root.lock().unwrap(), &home);
    let active = Arc::new(Mutex::new(home));
    let held = root.lock().unwrap();
    let before = held.snapshot();
    let (observed, wait) = std::sync::mpsc::channel();
    let shared = root.clone();
    let source = active.clone();
    let worker = std::thread::spawn(move || {
        let seen = std::cell::Cell::new(false);
        WorkflowRootSession::with_library_context(
            &shared,
            &context,
            || {
                let home = source.lock().unwrap().clone();
                if !seen.replace(true) {
                    observed.send(()).unwrap();
                }
                home
            },
            |_, _| Err::<Value, _>("stale command reached its mutation".into()),
        )
    });
    wait.recv_timeout(Duration::from_secs(5)).unwrap();
    *active.lock().unwrap() = other_home;
    drop(held);
    assert!(worker
        .join()
        .unwrap()
        .unwrap_err()
        .contains("home source changed"));
    assert_eq!(root.lock().unwrap().snapshot(), before);
}
#[test]
fn library_entries_real_observation_ordered_subset_to_existing_review_packet() {
    let fixture = Fixture::new();
    let first = entry_package(&fixture, "alpha");
    let second = entry_package(&fixture, "beta");
    let first_bytes = crate::workflow_workspace::Snapshot::capture(&first)
        .unwrap()
        .files()
        .clone();
    let second_bytes = crate::workflow_workspace::Snapshot::capture(&second)
        .unwrap()
        .files()
        .clone();
    let mut root = opened_entry_root(&fixture);
    let home = no_supplier_home();
    let initial = entry_host(&root, &home);
    let original_listing = entry_library(&root);
    let unchosen = entry_package(&fixture, "gamma");
    assert_eq!(
        entry_library(&root)["entryListing"],
        original_listing["entryListing"],
        "status does not scan new files"
    );
    let library_ref = root.active_library.clone().unwrap();
    root.observe_library_entries(&library_ref).unwrap();
    let library = entry_library(&root);
    assert_ne!(
        library["entryListing"]["reference"],
        original_listing["entryListing"]["reference"]
    );
    let refs = vec![entry_ref(&library, "beta"), entry_ref(&library, "alpha")];
    let selection = entry_selection(&library, &refs);
    let refreshed = entry_host(&root, &home);
    std::fs::write(
        unchosen.join("notes.txt"),
        b"Unchosen content changed; not part of review\n",
    )
    .unwrap();
    root.review_library_entries(
        home.clone(),
        json!({"fixture":"absent native source"}),
        &library_ref,
        selection["listingRef"].as_str().unwrap(),
        &refs,
    )
    .unwrap();
    let reviewed = entry_host(&root, &home);
    let review_ref = root.active_review.clone().unwrap();
    let review = root.reviews[&review_ref].lock().unwrap();
    let presentation = &review.status["presentation"];
    let names: Vec<_> = presentation["entries"]
        .as_array()
        .unwrap()
        .iter()
        .map(|entry| entry["identity"]["name"].as_str().unwrap().to_owned())
        .collect();
    assert_eq!(names, vec!["beta", "alpha"]);
    assert_eq!(
        review
            .review
            .as_ref()
            .unwrap()
            .current()
            .unwrap()
            .descriptor_kind(),
        "a15_multi_descriptor"
    );
    assert!(!review.attempted_native);
    assert!(review.transaction.is_none());
    assert!(review.registered.is_empty());
    drop(review);
    assert!(root.selected.is_empty() && root.runs.is_empty());
    assert_eq!(
        crate::workflow_workspace::Snapshot::capture(&first)
            .unwrap()
            .files(),
        &first_bytes
    );
    assert_eq!(
        crate::workflow_workspace::Snapshot::capture(&second)
            .unwrap()
            .files(),
        &second_bytes
    );
    assert!(home.host.client_requests().is_empty());
    println!(
        "LISTED_LIBRARY_ENTRIES_DTO:{}",
        json!({"initial":initial["workflowRoot"],"refreshed":refreshed["workflowRoot"],"reviewed":reviewed["workflowRoot"],"host":refreshed,"selection":selection,"orderedNames":names})
    );
}
#[test]
fn library_entries_stale_refs_source_and_content_refuse_without_review() {
    let mut packets = Vec::new();
    for change in [
        "content",
        "entry replacement",
        "library replacement",
        "library switch",
        "refresh",
        "foreign reference",
        "duplicate reference",
    ] {
        let fixture = Fixture::new();
        let path = entry_package(&fixture, "sample");
        let mut root = opened_entry_root(&fixture);
        let library = entry_library(&root);
        let reference = entry_ref(&library, "sample");
        let refs = vec![reference.clone()];
        let selection = entry_selection(&library, &refs);
        let home = no_supplier_home();
        let before = entry_host(&root, &home);
        let mut chosen = refs;
        match change {
            "content" => std::fs::write(path.join("notes.txt"), b"Different bytes\n").unwrap(),
            "entry replacement" => {
                std::fs::rename(&path, path.with_extension("original")).unwrap();
                entry_package(&fixture, "sample");
            }
            "library replacement" => {
                std::fs::rename(&fixture.root, fixture.root.with_extension("original")).unwrap();
                std::fs::create_dir(&fixture.root).unwrap();
                entry_package(&fixture, "sample");
            }
            "library switch" => {
                let other = fixture.root.join("other-library");
                std::fs::create_dir(&other).unwrap();
                root.open_library(other, "user", None, Arc::new(Mutex::new(None)))
                    .unwrap();
            }
            "refresh" => {
                root.observe_library_entries(selection["libraryRef"].as_str().unwrap())
                    .unwrap();
            }
            "foreign reference" => chosen = vec!["workflow-library-entry:not-held".into()],
            "duplicate reference" => chosen.push(reference),
            _ => unreachable!(),
        }
        let error = root
            .review_library_entries(
                home.clone(),
                json!({}),
                selection["libraryRef"].as_str().unwrap(),
                selection["listingRef"].as_str().unwrap(),
                &chosen,
            )
            .unwrap_err();
        assert!(
            root.reviews.is_empty(),
            "{change}: failed entry operation creates no hot review/offer"
        );
        assert!(root.active_review.is_none());
        let mut actual_selection = selection.clone();
        actual_selection["entryRefs"] = json!(chosen);
        packets.push(json!({"error":error,"before":before["workflowRoot"],"after":entry_host(&root,&home)["workflowRoot"],"selection":actual_selection,"change":change,"host":before}));
        if change == "library replacement" {
            std::fs::remove_dir_all(&fixture.root).unwrap();
            std::fs::rename(fixture.root.with_extension("original"), &fixture.root).unwrap();
        }
    }
    println!(
        "LISTED_LIBRARY_ENTRIES_REFUSALS_DTO:{}",
        json!({"refusals":packets})
    );
}
#[test]
fn library_entries_hygiene_nonregular_and_ledger_limits_preserve_healthy_entry() {
    use std::os::unix::{ffi::OsStrExt, fs::symlink};
    let fixture = Fixture::new();
    entry_package(&fixture, "healthy");
    let bad = entry_package(&fixture, "bad-name");
    std::fs::write(bad.join("WORKFLOW.md"), b"---\nname: other\n---\n").unwrap();
    let os = entry_package(&fixture, "os-entry");
    std::fs::write(os.join(".DS_Store"), b"refused hygiene").unwrap();
    let missing = entry_package(&fixture, "missing");
    std::fs::remove_file(missing.join("WORKFLOW.md")).unwrap();
    let wrong = entry_package(&fixture, "utf8");
    std::fs::write(wrong.join("WORKFLOW.md"), b"\xff").unwrap();
    let fifo = entry_package(&fixture, "fifo");
    let name = std::ffi::CString::new(fifo.join("producer").as_os_str().as_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    symlink(
        fixture.root.join("not-a-source"),
        fixture.root.join(".chirality/workflows/alias"),
    )
    .unwrap();
    let oversized = entry_package(&fixture, "oversized");
    let file = std::fs::File::create(oversized.join("large")).unwrap();
    file.set_len(crate::workflow_workspace::PACKAGE_MAX_BYTES + 1)
        .unwrap();
    let mut root = opened_entry_root(&fixture);
    let library = entry_library(&root);
    let rows = library["entryListing"]["entries"].as_array().unwrap();
    assert_eq!(
        rows.iter().filter(|row| row["reviewable"] == true).count(),
        1
    );
    assert_eq!(
        rows.iter().find(|row| row["name"] == "healthy").unwrap()["reviewable"],
        true
    );
    assert!(rows
        .iter()
        .filter(|row| row["name"] != "healthy")
        .all(|row| row["reviewable"] == false && row["limit"].is_string()));
    std::fs::write(
        fixture.root.join(".chirality/workflow-registry.jsonl"),
        b"not a healthy ledger\n",
    )
    .unwrap();
    let reference = root.active_library.clone().unwrap();
    root.observe_library_entries(&reference).unwrap();
    let unavailable = entry_library(&root);
    assert_eq!(unavailable["entryListing"]["state"], "unavailable");
    assert!(unavailable["entryListing"]["entries"]
        .as_array()
        .unwrap()
        .is_empty());
    println!(
        "LISTED_LIBRARY_ENTRIES_LIMITS_DTO:{}",
        json!({"healthyWithLimits":library,"unavailable":root.snapshot()})
    );
}
#[test]
fn library_entries_absent_empty_and_later_changes_are_explicit_observations() {
    let fixture = Fixture::new();
    let mut root = opened_entry_root(&fixture);
    assert_eq!(entry_library(&root)["entryListing"]["state"], "absent");
    let absent = root.snapshot();
    std::fs::create_dir_all(fixture.root.join(".chirality/workflows")).unwrap();
    let reference = root.active_library.clone().unwrap();
    root.observe_library_entries(&reference).unwrap();
    assert_eq!(entry_library(&root)["entryListing"]["state"], "observed");
    assert!(entry_library(&root)["entryListing"]["entries"]
        .as_array()
        .unwrap()
        .is_empty());
    let empty = root.snapshot();
    entry_package(&fixture, "later");
    assert!(entry_library(&root)["entryListing"]["entries"]
        .as_array()
        .unwrap()
        .is_empty());
    root.observe_library_entries(&reference).unwrap();
    assert_eq!(
        entry_library(&root)["entryListing"]["entries"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    println!(
        "LISTED_LIBRARY_ENTRIES_EMPTY_DTO:{}",
        json!({"absent":absent,"empty":empty})
    );
}
#[test]
fn library_entries_registered_changed_copy_and_incomplete_claims_are_not_ds7() {
    let fixture = Fixture::new();
    let mut root = fixture.registered();
    let library = root.active_library.clone().unwrap();
    root.observe_library_entries(&library).unwrap();
    let row = entry_library(&root)["entryListing"]["entries"]
        .as_array()
        .unwrap()[0]
        .clone();
    assert_eq!(row["state"], "registered copy as read");
    assert_eq!(row["reviewable"], false);
    let path = fixture
        .root
        .join(".chirality/workflows/coordinated-knowledge-work/REVIEW-NOTES.md");
    std::fs::write(&path, b"Published copy differs from registered store\n").unwrap();
    root.observe_library_entries(&library).unwrap();
    let row = entry_library(&root)["entryListing"]["entries"]
        .as_array()
        .unwrap()[0]
        .clone();
    assert_eq!(row["state"], "library copy changed outside registration");
    assert_eq!(row["reviewable"], false);
    let log = crate::storage::library_log(&fixture.root);
    std::fs::remove_file(log).unwrap();
    root.observe_library_entries(&library).unwrap();
    let row = entry_library(&root)["entryListing"]["entries"]
        .as_array()
        .unwrap()[0]
        .clone();
    assert_eq!(row["state"], "registration record incomplete or unreadable");
    assert_eq!(row["reviewable"], false);
}
