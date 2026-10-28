// RE-7 / REC conversation identity: a bare native thread ID is home-scoped.
#[test]
fn home_qualified_hot_run_two_homes_open_concurrently() {
    let a = Peer::new();
    let b = Peer::new();
    let mut root = a.registered();
    let first = open_run(&a, &mut root, "thread");
    choose_fixture_chat(&b, &mut root, "thread");
    let second = root.prepare_run(b.home.clone(), &b.generation, "thread", "B".into(), Some(&a.fixture.root)).expect("a distinct actual home is a distinct conversation");
    root.runs[&second].lock().unwrap().send().unwrap();
    assert_eq!(root.runs[&first].lock().unwrap().lifecycle, RunLifecycle::Open);
    assert_eq!(root.runs[&second].lock().unwrap().lifecycle, RunLifecycle::Open);
    assert_eq!(a.turn_starts(), 1);
    assert_eq!(b.turn_starts(), 1);
    for (peer, run) in [(&a, &first), (&b, &second)] {
        let denied = root.prepare_run(peer.home.clone(), &peer.generation, "thread", "again".into(), Some(&a.fixture.root));
        assert!(denied.as_ref().is_err_and(|e| e.contains("live") && e.contains(run)), "{denied:?}");
    }
    let entries = a.fixture.rs_entries();
    assert_eq!(entries.iter().filter(|e| e["kind"] == "run_opened").count(), 2);
    assert!(!entries.iter().any(|e| e["kind"] == "run_ended"));
}

fn hot_run_reading(peer: &Peer, run: &str) -> crate::records::supply::RecordedRun {
    let project = crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    crate::records::supply::read_project_runs(&project, &[]).runs.into_iter().find(|r| r.run == run).unwrap()
}
fn hot_run_proved(root: &WorkflowRootSession, peer: &Peer, other: &Peer, recorded: &crate::records::supply::RecordedRun) -> bool {
    let project = crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    root.hot_run_in_other_home(recorded, other.generation["home"].as_str().unwrap(), "thread", &project)
}
fn hot_run_rewrite(log: &std::path::Path, entries: &[Value]) {
    let text: String = entries.iter().map(|entry| format!("{entry}\n")).collect();
    std::fs::write(log, crate::record_lines::fixture::rechain(text.as_bytes())).unwrap();
}

#[test]
fn home_qualified_hot_run_exact_original_opening_required() {
    let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
    let run = open_run(&a, &mut root, "thread");
    let recorded = hot_run_reading(&a, &run);
    let log = crate::records::supply::run_log(&a.fixture.root, &run).unwrap();
    let bytes = std::fs::read(&log).unwrap();
    let entries = rs_for(&a, &run);
    assert!(hot_run_proved(&root, &a, &b, &recorded));
    for field in ["recordId", "observedAt", "body"] {
        let mut changed = entries.clone();
        let opening = changed.iter_mut().find(|e| e["kind"] == "run_opened").unwrap();
        match field {
            "recordId" => opening["recordId"] = json!(crate::util::opaque_id("rec:app:").unwrap()),
            "observedAt" => opening["observedAt"] = json!("2000-01-01T00:00:00Z"),
            _ => opening["body"]["workflow"]["name"] = json!("different-workflow"),
        }
        hot_run_rewrite(&log, &changed);
        assert!(!hot_run_proved(&root, &a, &b, &recorded), "changed {field}");
        std::fs::write(&log, &bytes).unwrap();
    }
    // A unique identity in a foreign owning log is not the original source.
    let foreign = crate::storage::project_log(&a.fixture.root, Some(&run), "foreign-owning-writer").unwrap();
    std::fs::rename(&log, &foreign).unwrap();
    assert!(!hot_run_proved(&root, &a, &b, &recorded));
    std::fs::rename(&foreign, &log).unwrap();
    // A second opening is conflicting even when it quotes the same body/time.
    let mut duplicate = entries.clone();
    let mut opening = duplicate.iter().find(|e| e["kind"] == "run_opened").unwrap().clone();
    opening["recordId"] = json!(crate::util::opaque_id("rec:app:").unwrap());
    opening["seq"] = json!(duplicate.last().unwrap()["seq"].as_u64().unwrap() + 1);
    duplicate.push(opening); hot_run_rewrite(&log, &duplicate);
    assert!(!hot_run_proved(&root, &a, &b, &recorded));
    choose_fixture_chat(&b, &mut root, "thread");
    assert!(root.prepare_run(b.home.clone(), &b.generation, "thread", "B".into(), Some(&a.fixture.root)).is_err());
    std::fs::write(&log, &bytes).unwrap();
    std::fs::remove_file(&log).unwrap();
    assert!(!hot_run_proved(&root, &a, &b, &recorded), "a held run ID alone cannot establish the missing opening");
}

#[test]
fn home_qualified_hot_run_busy_missing_and_cold_proof_refuse() {
    let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
    let run = open_run(&a, &mut root, "thread");
    choose_fixture_chat(&b, &mut root, "thread");
    let owner = root.runs[&run].clone();
    let held = owner.lock().unwrap();
    assert!(root.prepare_run(b.home.clone(), &b.generation, "thread", "B".into(), Some(&a.fixture.root)).is_err(), "busy original owner is unknown");
    drop(held);
    let original = owner.lock().unwrap().entries.iter().find(|e| e.kind == "run_opened").unwrap().clone();
    owner.lock().unwrap().entries.retain(|e| e.kind != "run_opened");
    assert!(root.prepare_run(b.home.clone(), &b.generation, "thread", "B".into(), Some(&a.fixture.root)).is_err(), "missing original opening cannot be replaced by the file claim");
    owner.lock().unwrap().entries.push(original);
    let mut fresh = WorkflowRootSession::default(); fresh.selected = std::mem::take(&mut root.selected);
    assert!(fresh.prepare_run(b.home.clone(), &b.generation, "thread", "B".into(), Some(&a.fixture.root)).is_err(), "cold rows have no native-home proof");
}

#[test]
fn home_qualified_hot_run_landed_unconfirmed_uses_held_pending_identity() {
    let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
    let run = root.prepare_run(a.home.clone(), &a.generation, "thread", "A".into(), a.project()).unwrap();
    let log = crate::records::supply::run_log(&a.fixture.root, &run).unwrap();
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    crate::storage::fail_directory_for_test(Some(log.parent().unwrap().to_owned()));
    root.runs[&run].lock().unwrap().send().unwrap();
    crate::storage::fail_directory_for_test(None);
    { let held = root.runs[&run].lock().unwrap();
      let original = held.entries.iter().find(|e| e.kind == "run_opened").unwrap();
      assert!(original.written.is_none() && original.failure.is_some(), "original callback remains unconfirmed");
    }
    let recorded = hot_run_reading(&a, &run);
    assert!(hot_run_proved(&root, &a, &b, &recorded), "the exact original pending entry landed");
    choose_fixture_chat(&b, &mut root, "thread");
    let second = root.prepare_run(b.home.clone(), &b.generation, "thread", "B".into(), Some(&a.fixture.root)).unwrap();
    root.runs[&second].lock().unwrap().send().unwrap();
    assert_eq!(a.turn_starts(), 1); assert_eq!(b.turn_starts(), 1);
    assert_eq!(root.runs[&run].lock().unwrap().lifecycle, RunLifecycle::Open);
}

#[test]
fn home_qualified_hot_run_physical_source_and_store_association_required() {
    let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
    let run = open_run(&a, &mut root, "thread"); let recorded = hot_run_reading(&a, &run);
    assert!(hot_run_proved(&root, &a, &b, &recorded));
    let alias = a.fixture.root.with_extension("alias");
    std::os::unix::fs::symlink(&a.fixture.root, &alias).unwrap();
    assert!(crate::workflow_workspace::publication::ProjectRecords::open(&alias).is_err());
    std::fs::remove_file(alias).unwrap();
    // Same path and same project link, different physical project directory.
    let link = a.fixture.root.join(".chirality/project.json"); let link_bytes = std::fs::read(&link).unwrap();
    let moved = a.fixture.root.with_extension("moved"); std::fs::rename(&a.fixture.root, &moved).unwrap();
    std::fs::create_dir_all(link.parent().unwrap()).unwrap(); std::fs::write(&link, &link_bytes).unwrap();
    assert!(!hot_run_proved(&root, &a, &b, &recorded));
    std::fs::remove_dir_all(&a.fixture.root).unwrap(); std::fs::rename(&moved, &a.fixture.root).unwrap();
    assert!(hot_run_proved(&root, &a, &b, &recorded));
    // The store's governing identity survives a changed but readable link.
    // This is not a different association; an unusable link is unknown.
    let other_link = std::fs::read(b.fixture.root.join(".chirality/project.json")).unwrap();
    std::fs::write(&link, other_link).unwrap();
    assert!(hot_run_proved(&root, &a, &b, &recorded));
    std::fs::remove_file(&link).unwrap();
    assert!(!hot_run_proved(&root, &a, &b, &recorded));
    std::fs::write(&link, &link_bytes).unwrap();
    assert!(hot_run_proved(&root, &a, &b, &recorded));
    // Same records-home spelling and bytes, different physical store directory.
    let project = crate::workflow_workspace::publication::ProjectRecords::open(&a.fixture.root).unwrap();
    let store = project.source_binding().unwrap().records_root().to_owned();
    let moved_store = store.with_extension("moved"); std::fs::rename(&store, &moved_store).unwrap();
    std::fs::create_dir(&store).unwrap();
    assert!(!hot_run_proved(&root, &a, &b, &recorded));
    std::fs::remove_dir(&store).unwrap(); std::fs::rename(&moved_store, &store).unwrap();
}


fn hot_run_copy_tree(from: &std::path::Path, to: &std::path::Path) {
    std::fs::create_dir(to).unwrap();
    for entry in std::fs::read_dir(from).unwrap() {
        let entry = entry.unwrap(); let destination = to.join(entry.file_name());
        if entry.file_type().unwrap().is_dir() { hot_run_copy_tree(&entry.path(), &destination); }
        else { assert!(entry.file_type().unwrap().is_file()); std::fs::copy(entry.path(), destination).unwrap(); }
    }
}
#[test]
fn home_qualified_hot_run_original_store_pin_precedes_native_send() {
    let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
    let run = root.prepare_run(a.home.clone(), &a.generation, "thread", "A".into(), a.project()).unwrap();
    { let held = root.runs[&run].lock().unwrap();
      assert!(held.project.original_source_binding().is_err(), "preparation has not yet published WR/native input");
      assert!(!held.attempted && held.published.is_none()); }
    root.runs[&run].lock().unwrap().send().unwrap();
    let recorded = hot_run_reading(&a, &run);
    let store = { let held = root.runs[&run].lock().unwrap();
        assert!(held.attempted && held.published.is_some());
        held.project.original_source_binding().unwrap().records_root().to_owned() };
    assert!(hot_run_proved(&root, &a, &b, &recorded));
    // A newly opened handle cannot retroactively take custody of the opening.
    let original = { let mut held = root.runs[&run].lock().unwrap();
        std::mem::replace(&mut held.project, crate::workflow_workspace::publication::ProjectRecords::open(&a.fixture.root).unwrap()) };
    assert!(!hot_run_proved(&root, &a, &b, &recorded));
    root.runs[&run].lock().unwrap().project = original;
    // Exact copied source bytes in a new same-named store cannot borrow its scope.
    let moved = store.with_extension("moved"); std::fs::rename(&store, &moved).unwrap();
    hot_run_copy_tree(&moved, &store);
    assert!(!hot_run_proved(&root, &a, &b, &recorded));
    std::fs::remove_dir_all(&store).unwrap(); std::fs::rename(&moved, &store).unwrap();
    assert!(hot_run_proved(&root, &a, &b, &recorded));
}


#[test]
fn home_qualified_hot_run_changed_store_keeps_original_association() {
    let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
    let run = open_run(&a, &mut root, "thread"); let recorded = hot_run_reading(&a, &run);
    let configured = crate::records_store::current().unwrap();
    let source = root.runs[&run].lock().unwrap().project.original_source_binding().unwrap().records_root().to_owned();
    let alternate = a.fixture.root.with_extension("different-store");
    std::fs::create_dir(&alternate).unwrap(); std::fs::create_dir(alternate.join("projects")).unwrap();
    for name in ["store.json", "roots.jsonl"] { std::fs::copy(configured.root.join(name), alternate.join(name)).unwrap(); }
    hot_run_copy_tree(&source, &alternate.join("projects").join(source.file_name().unwrap()));
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: alternate.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    let proved = hot_run_proved(&root, &a, &b, &recorded);
    crate::records_store::use_store_for_test(None);
    assert!(!proved, "the same project/path/source bytes in another store are not the originally held records source");
    assert!(hot_run_proved(&root, &a, &b, &recorded));
    std::fs::remove_dir_all(alternate).unwrap();
}

#[test]
fn home_qualified_hot_run_owning_log_nonplain_members_refuse_regular_alias_preserves_source() {
    let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
    let run = open_run(&a, &mut root, "thread"); let recorded = hot_run_reading(&a, &run);
    let log = crate::records::supply::run_log(&a.fixture.root, &run).unwrap();
    let saved = log.with_extension("saved"); std::fs::rename(&log, &saved).unwrap();
    for kind in ["symlink", "directory", "hardlink", "fifo"] {
        match kind {
            "symlink" => std::os::unix::fs::symlink(&saved, &log).unwrap(),
            "directory" => std::fs::create_dir(&log).unwrap(),
            "hardlink" => std::fs::hard_link(&saved, &log).unwrap(),
            _ => {
                use std::os::unix::ffi::OsStrExt;
                let path = std::ffi::CString::new(log.as_os_str().as_bytes()).unwrap();
                assert_eq!(unsafe { libc::mkfifo(path.as_ptr(), 0o600) }, 0);
            }
        }
        let start = std::time::Instant::now();
        let proved = hot_run_proved(&root, &a, &b, &recorded);
        // RS's checked reader admits regular hard-linked logs. This second
        // non-log name still denotes the same inode, not another parsed claim.
        assert_eq!(proved, kind == "hardlink", "owning member {kind}");
        assert!(start.elapsed() < Duration::from_secs(1), "{kind} source proof must not wait for input");
        if kind == "directory" { std::fs::remove_dir(&log).unwrap(); }
        else { std::fs::remove_file(&log).unwrap(); }
    }
    std::fs::rename(saved, log).unwrap();
}


#[test]
fn home_qualified_hot_run_current_endings_between_reads_keep_refusal() {
    let mut admitted = Vec::new();
    for conflicting in [false, true] {
        let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
        let run = open_run(&a, &mut root, "thread");
        choose_fixture_chat(&b, &mut root, "thread");
        let owner = root.runs[&run].clone();
        let original_run = run.clone();
        let project = a.fixture.root.clone();
        let log = crate::records::supply::run_log(&project, &run).unwrap();
        AFTER_RUN_PRIOR_READING.with(|hook| *hook.borrow_mut() = Some(Box::new(move || {
            owner.lock().unwrap().end_run(None, None).unwrap();
            if conflicting {
                let (mut entries, limits) = crate::storage::read_all(&project);
                assert!(limits.is_empty());
                entries.retain(|e| e["runId"] == run);
                let mut duplicate = entries.iter().find(|e| e["kind"] == "run_ended").unwrap().clone();
                duplicate["recordId"] = json!(crate::util::opaque_id("rec:app:").unwrap());
                duplicate["seq"] = json!(entries.last().unwrap()["seq"].as_u64().unwrap() + 1);
                entries.push(duplicate); hot_run_rewrite(&log, &entries);
            }
        })));
        let outcome = root.prepare_run(b.home.clone(), &b.generation, "thread", "B".into(), Some(&a.fixture.root));
        if outcome.is_ok() { admitted.push(conflicting); }
        else { assert_eq!(root.runs.len(), 1, "no successor prepared from stale lifecycle evidence"); }
        assert_eq!(a.turn_starts(), 1); assert_eq!(b.turn_starts(), 0);
        let current = hot_run_reading(&a, &original_run);
        assert!(if conflicting { matches!(current.lifecycle, crate::records::supply::RecordedLifecycle::Unknown(_)) }
            else { matches!(current.lifecycle, crate::records::supply::RecordedLifecycle::Ended { .. }) });
    }
    assert!(admitted.is_empty(), "fresh endings must not exclude the stale possibly-live projection; wrongly admitted conflicting flags: {admitted:?}");
}

#[test]
fn home_qualified_hot_run_append_after_index_refresh_keeps_refusal() {
    let a = Peer::new(); let b = Peer::new(); let mut root = a.registered();
    let run = open_run(&a, &mut root, "thread"); choose_fixture_chat(&b, &mut root, "thread");
    let mut entries = rs_for(&a, &run);
    let mut ending = entries.iter().find(|e| e["kind"] == "run_opened").unwrap().clone();
    ending["kind"] = json!("run_ended");
    ending["body"] = json!({"stoppedBy":"the person", "cause":"ended by the person", "waitingArrivals":[]});
    for _ in 0..2 {
        ending["recordId"] = json!(crate::util::opaque_id("rec:app:").unwrap());
        ending["seq"] = json!(entries.last().unwrap()["seq"].as_u64().unwrap() + 1);
        entries.push(ending.clone());
    }
    let log = crate::records::supply::run_log(&a.fixture.root, &run).unwrap();
    let project = a.fixture.root.clone();
    let query_cut = std::rc::Rc::new(std::cell::Cell::new(false)); let hit = query_cut.clone();
    let guard = std::rc::Rc::new(std::cell::RefCell::new(None)); let hook_guard = guard.clone();
    AFTER_RUN_PRIOR_READING.with(|hook| *hook.borrow_mut() = Some(Box::new(move || {
        // The old lifecycle is now held. Warm the query positions before the
        // mutation; the next owning-log open is the query's checked line read.
        crate::records_index::with_index(&project, |_| {});
        let changed = log.clone();
        *hook_guard.borrow_mut() = Some(crate::records_index::log_open_hook_for_test(&log, None, 0, move || {
            hot_run_rewrite(&changed, &entries); hit.set(true);
        }));
    })));
    let outcome = root.prepare_run(b.home.clone(), &b.generation, "thread", "B".into(), Some(&a.fixture.root));
    drop(guard.borrow_mut().take());
    assert!(query_cut.get(), "the source mutation must occur at the checked query read");
    assert!(outcome.is_err(), "unchanged indexed lines do not establish absence of newly appended conflicting endings");
    assert_eq!(root.runs.len(), 1); assert_eq!(a.turn_starts(), 1); assert_eq!(b.turn_starts(), 0);
    assert!(matches!(hot_run_reading(&a, &run).lifecycle, crate::records::supply::RecordedLifecycle::Unknown(_)));
}
