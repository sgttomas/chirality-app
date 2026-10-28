// Actual registered source -> external project TX-7 copy -> original Host send.
// The peer and native registration are local synthetic fixtures, never a supplier/person witness.
struct SupplyFixture {
    peer: Peer,
    root: Mutex<WorkflowRootSession>,
    project: PathBuf,
    reference: String,
    copy: PathBuf,
    expected: crate::workflow_workspace::Snapshot,
}
impl SupplyFixture {
    fn new() -> Self {
        let peer = Peer::new();
        let mut root = peer.registered();
        let project = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("workflow-supply-dispatch-").unwrap());
        std::fs::create_dir(&project).unwrap();
        let reference = root
            .prepare_run(
                peer.home.clone(),
                &peer.generation,
                "thread",
                "person".into(),
                Some(&project),
            )
            .unwrap();
        let (copy, expected) = {
            let run = root.runs[&reference].lock().unwrap();
            assert!(run.status["otherFiles"]["basis"]
                .as_str()
                .unwrap()
                .starts_with("supply copy in the project"));
            (
                project.join(run.status["otherFiles"]["folder"].as_str().unwrap()),
                run.selection.snapshot().clone(),
            )
        };
        assert_eq!(
            crate::workflow_workspace::Snapshot::capture(&copy)
                .unwrap()
                .files(),
            expected.files()
        );
        Self {
            peer,
            root: Mutex::new(root),
            project,
            reference,
            copy,
            expected,
        }
    }
    fn run(&self) -> Arc<Mutex<WorkflowRun>> {
        self.root.lock().unwrap().runs[&self.reference].clone()
    }
    fn assert_original_store(&self) {
        let run = self.run();
        let run = run.lock().unwrap();
        assert_eq!(
            crate::workflow_workspace::Snapshot::capture(&run.prepared().scope().revision_store)
                .unwrap()
                .files(),
            self.expected.files()
        );
    }
}
impl Drop for SupplyFixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.project);
    }
}

fn refuses_changed_copy(mode: &str) {
    let f = SupplyFixture::new();
    let before = f.run().lock().unwrap().view(&f.reference);
    let text = f.run().lock().unwrap().prepared().text().to_owned();
    let starts = f.peer.turn_starts();
    match mode {
        "changed" => std::fs::write(
            f.copy.join("REVIEW-NOTES.md"),
            b"different resource bytes after Prepare",
        )
        .unwrap(),
        "missing" => std::fs::remove_dir_all(&f.copy).unwrap(),
        _ => unreachable!(),
    }
    f.assert_original_store();
    let result = start_workflow_run(&f.root, &f.reference);
    let run = f.run();
    let run = run.lock().unwrap();
    assert!(
        result.is_err(),
        "{mode}: changed generated supporting copy was sent: {result:?}"
    );
    assert!(
        !run.attempted && run.source.is_none(),
        "{mode}: refusal must precede the native attempt"
    );
    assert_eq!(f.peer.turn_starts(), starts, "{mode}: no native turn/start");
    assert_eq!(run.prepared().text(), text);
    assert_eq!(run.view(&f.reference)["runText"], before["runText"]);
    assert_eq!(run.lifecycle, RunLifecycle::Prepared);
    assert_eq!(run.status["sent"], false);
    assert_eq!(run.status["supplied"], "not supplied");
    match mode {
        "changed" => assert_eq!(
            std::fs::read(f.copy.join("REVIEW-NOTES.md")).unwrap(),
            b"different resource bytes after Prepare"
        ),
        "missing" => assert!(!f.copy.exists()),
        _ => unreachable!(),
    }
}
#[test]
fn workflow_supply_dispatch_changed_copy_is_refused_before_send() {
    refuses_changed_copy("changed");
}
#[test]
fn workflow_supply_dispatch_missing_copy_is_refused_before_send() {
    refuses_changed_copy("missing");
}

#[test]
fn workflow_supply_dispatch_restoration_and_final_boundary_dto() {
    let mut cases = vec![];
    for prepublished in [false, true] {
        let f = SupplyFixture::new();
        let prepared = f.run().lock().unwrap().view(&f.reference);
        let original_text = f.run().lock().unwrap().prepared().text().to_owned();
        let before = f.peer.turn_starts();
        let path = f.copy.join("REVIEW-NOTES.md");
        if prepublished {
            let path = path.clone();
            BEFORE_GENERATED_FILES_DISPATCH.with(|hook| {
                *hook.borrow_mut() = Some(Box::new(move || {
                    std::fs::write(path, b"changed after publication/evaluation").unwrap()
                }))
            });
        } else {
            std::fs::write(&path, b"changed before publication").unwrap();
        }
        let error = start_workflow_run(&f.root, &f.reference).unwrap_err();
        let (refused, after_refusal_text) = {
            let run = f.run();
            let run = run.lock().unwrap();
            assert_eq!(run.published.is_some(), prepublished);
            assert!(!run.attempted && run.source.is_none());
            assert_eq!(run.lifecycle, RunLifecycle::Prepared);
            (run.view(&f.reference), run.prepared().text().to_owned())
        };
        let refused_starts = f.peer.turn_starts();
        assert_eq!(refused_starts, before);
        assert_eq!(after_refusal_text, original_text);
        f.assert_original_store();
        assert_eq!(refused["status"]["sent"], false);
        assert_eq!(refused["status"]["supplied"], "not supplied");
        for field in ["selection", "runText"] {
            if prepublished {
                assert_eq!(
                    refused["status"]["records"][field]["state"],
                    "recorded (resolves)"
                );
            } else {
                assert!(matches!(
                    refused["status"]["records"][field]["state"].as_str(),
                    Some("not recorded" | "not confirmed")
                ));
                if refused["status"]["records"][field]["state"] == "not confirmed" {
                    assert!(
                        refused["status"]["records"][field]["limit"].is_string(),
                        "unavailable readback is disclosed, never changed to absence"
                    );
                }
            }
        }
        if prepublished {
            let again = start_workflow_run(&f.root, &f.reference);
            assert!(
                again.is_err(),
                "already-published retry still checks the generated copy"
            );
            assert_eq!(
                f.run().lock().unwrap().view(&f.reference)["publication"],
                refused["publication"]
            );
            assert_eq!(f.peer.turn_starts(), before);
        }
        std::fs::write(&path, &f.expected.files()["REVIEW-NOTES.md"]).unwrap();
        let result = start_workflow_run(&f.root, &f.reference).unwrap();
        let (restored, after_restored_text) = {
            let run = f.run();
            let run = run.lock().unwrap();
            assert!(run.attempted && run.source.is_some());
            (run.view(&f.reference), run.prepared().text().to_owned())
        };
        assert_eq!(after_restored_text, original_text);
        assert_eq!(f.peer.turn_starts(), before + 1);
        assert_eq!(
            last_turn_start(&f.peer)["params"]["input"][0]["text"],
            original_text
        );
        assert_eq!(
            last_turn_start(&f.peer)["params"]["clientUserMessageId"],
            f.run().lock().unwrap().client_id
        );
        cases.push(json!({"prepublished":prepublished,"prepared":prepared,"refused":refused,"restored":restored,"error":error,"result":result,"originalText":original_text,"afterRefusalText":after_refusal_text,"afterRestoredText":after_restored_text,"nativeStarts":{"before":before,"refused":refused_starts,"restored":f.peer.turn_starts()}}));
    }
    println!("WORKFLOW_SUPPLY_DISPATCH_DTO:{}", json!({"cases":cases}));
}

#[test]
fn workflow_supply_dispatch_direct_source_after_retry_records_requires_original_revision() {
    let peer = Peer::new();
    let mut root = peer.registered();
    let reference = root
        .prepare_run(
            peer.home.clone(),
            &peer.generation,
            "thread",
            "person".into(),
            peer.project(),
        )
        .unwrap();
    let root = Mutex::new(root);
    let run = root.lock().unwrap().runs[&reference].clone();
    let (resource, original, text, publication) = {
        let mut run = run.lock().unwrap();
        assert_eq!(
            run.status["otherFiles"]["basis"],
            "holding folder inside the project"
        );
        run.retry_records().unwrap();
        assert!(run.published.is_some() && !run.attempted);
        (
            run.prepared()
                .scope()
                .revision_store
                .join("REVIEW-NOTES.md"),
            run.selection.snapshot().files()["REVIEW-NOTES.md"].clone(),
            run.prepared().text().to_owned(),
            run.view(&reference)["publication"].clone(),
        )
    };
    let prepared = run.lock().unwrap().view(&reference);
    let starts = peer.turn_starts();
    std::fs::write(
        &resource,
        b"changed original source after metadata publication",
    )
    .unwrap();
    let result = start_workflow_run(&root, &reference);
    assert!(
        result.is_err(),
        "already published original revision was sent after mutation: {result:?}"
    );
    let error = result.unwrap_err();
    assert!(!run.lock().unwrap().attempted);
    assert_eq!(peer.turn_starts(), starts);
    assert_eq!(
        run.lock().unwrap().view(&reference)["publication"],
        publication
    );
    let refused = run.lock().unwrap().view(&reference);
    assert_eq!(
        refused["status"]["state"],
        "selected revision source changed or unavailable; nothing sent"
    );
    assert_eq!(refused["status"]["supplied"], "not supplied");
    let after_refusal = run.lock().unwrap().prepared().text().to_owned();
    std::fs::write(&resource, original).unwrap();
    let result = start_workflow_run(&root, &reference).unwrap();
    assert_eq!(peer.turn_starts(), starts + 1);
    assert_eq!(last_turn_start(&peer)["params"]["input"][0]["text"], text);
    println!(
        "WORKFLOW_SUPPLY_SOURCE_DISPATCH_DTO:{}",
        json!({"prepublished":true,"prepared":prepared,"refused":refused,"restored":run.lock().unwrap().view(&reference),"error":error,"result":result,"originalText":text,"afterRefusalText":after_refusal,"nativeStarts":{"before":starts,"refused":starts,"restored":peer.turn_starts()}})
    );
}

#[test]
fn workflow_supply_dispatch_unsafe_or_extra_copy_is_refused_without_repair() {
    use std::os::unix::{
        ffi::OsStrExt,
        fs::{symlink, FileTypeExt},
    };
    for mode in [
        "folder alias",
        "ancestor alias",
        "resource alias",
        "fifo",
        "extra file",
        "non-folder",
    ] {
        let f = SupplyFixture::new();
        let resource = f.copy.join("REVIEW-NOTES.md");
        let mut linked = None;
        match mode {
            "folder alias" => {
                let aside = f.copy.with_extension("kept");
                std::fs::rename(&f.copy, &aside).unwrap();
                symlink(&aside, &f.copy).unwrap();
                linked = Some((f.copy.clone(), aside));
            }
            "ancestor alias" => {
                let parent = f.copy.parent().unwrap();
                let aside = parent.with_extension("kept");
                std::fs::rename(parent, &aside).unwrap();
                symlink(&aside, parent).unwrap();
                linked = Some((parent.to_path_buf(), aside));
            }
            "resource alias" => {
                let aside = f.project.join("kept-resource");
                std::fs::rename(&resource, &aside).unwrap();
                symlink(&aside, &resource).unwrap();
                linked = Some((resource.clone(), aside));
            }
            "fifo" => {
                std::fs::remove_file(&resource).unwrap();
                let path = std::ffi::CString::new(resource.as_os_str().as_bytes()).unwrap();
                assert_eq!(unsafe { libc::mkfifo(path.as_ptr(), 0o600) }, 0);
            }
            "extra file" => {
                std::fs::write(f.copy.join("unlisted-resource.txt"), b"unexpected content").unwrap()
            }
            _ => {
                std::fs::remove_dir_all(&f.copy).unwrap();
                std::fs::write(&f.copy, b"not a package folder").unwrap();
            }
        }
        let starts = f.peer.turn_starts();
        let begin = std::time::Instant::now();
        assert!(start_workflow_run(&f.root, &f.reference).is_err(), "{mode}");
        assert!(
            begin.elapsed() < Duration::from_secs(3),
            "{mode}: refusal must not block on non-regular input"
        );
        assert_eq!(f.peer.turn_starts(), starts);
        assert!(!f.run().lock().unwrap().attempted);
        if let Some((path, target)) = linked {
            assert_eq!(
                std::fs::read_link(&path).unwrap(),
                target,
                "{mode}: refused alias left unchanged"
            );
        }
        if mode == "fifo" {
            assert!(std::fs::symlink_metadata(&resource)
                .unwrap()
                .file_type()
                .is_fifo());
        }
        if mode == "extra file" {
            assert_eq!(
                std::fs::read(f.copy.join("unlisted-resource.txt")).unwrap(),
                b"unexpected content"
            );
        }
        if mode == "non-folder" {
            assert_eq!(std::fs::read(&f.copy).unwrap(), b"not a package folder");
        }
        f.assert_original_store();
    }
}

#[test]
fn workflow_supply_dispatch_keeps_original_store_guard_and_no_resend() {
    let f = SupplyFixture::new();
    let original = f
        .run()
        .lock()
        .unwrap()
        .prepared()
        .scope()
        .revision_store
        .clone();
    std::fs::write(
        original.join("REVIEW-NOTES.md"),
        b"changed original revision",
    )
    .unwrap();
    let starts = f.peer.turn_starts();
    let error = start_workflow_run(&f.root, &f.reference).unwrap_err();
    assert!(
        error.contains("linked workflow revision no longer resolves exactly"),
        "{error}"
    );
    assert!(!f.run().lock().unwrap().attempted);
    assert_eq!(f.peer.turn_starts(), starts);
    std::fs::write(
        original.join("REVIEW-NOTES.md"),
        &f.expected.files()["REVIEW-NOTES.md"],
    )
    .unwrap();
    start_workflow_run(&f.root, &f.reference).unwrap();
    let sent = f.run().lock().unwrap().status.clone();
    let starts = f.peer.turn_starts();
    std::fs::write(
        f.copy.join("REVIEW-NOTES.md"),
        b"changed after actual native attempt",
    )
    .unwrap();
    assert!(start_workflow_run(&f.root, &f.reference)
        .unwrap_err()
        .contains("no resend"));
    assert_eq!(f.peer.turn_starts(), starts);
    assert_eq!(
        f.run().lock().unwrap().status,
        sent,
        "later file change does not relabel the actual prior send"
    );
}

#[test]
fn workflow_supply_dispatch_refusal_releases_notice_holds_and_keeps_chain_withdrawal() {
    for one_step in [false, true] {
        let f = SupplyFixture::new();
        start_workflow_run(&f.root, &f.reference).unwrap();
        let next = {
            let mut root = f.root.lock().unwrap();
            if one_step {
                let view = offer_view(&f.peer, &[("turn", "m", 1, "Working.", "live-observed")]);
                root.end_and_start_viewed(
                    &view,
                    &f.reference,
                    f.peer.home.clone(),
                    &f.peer.generation,
                    "thread",
                    "next".into(),
                    Some(&f.project),
                )
                .unwrap()
            } else {
                root.runs[&f.reference]
                    .lock()
                    .unwrap()
                    .end_run(None, None)
                    .unwrap();
                root.prepare_run(
                    f.peer.home.clone(),
                    &f.peer.generation,
                    "thread",
                    "next".into(),
                    Some(&f.project),
                )
                .unwrap()
            }
        };
        std::fs::write(
            f.copy.join("REVIEW-NOTES.md"),
            b"changed before chained dispatch",
        )
        .unwrap();
        let starts = f.peer.turn_starts();
        assert!(start_workflow_run(&f.root, &next).is_err());
        assert_eq!(f.peer.turn_starts(), starts);
        {
            let root = f.root.lock().unwrap();
            let prior = root.runs[&f.reference].lock().unwrap();
            let successor = root.runs[&next].lock().unwrap();
            assert_eq!(prior.lifecycle, RunLifecycle::Ended);
            assert!(matches!(prior.notice, NoticeState::AwaitingTurn));
            assert!(prior.notice_held_by_start.is_none());
            assert!(!successor.attempted && successor.source.is_none());
            assert_eq!(successor.withdrawn.is_some(), one_step);
            assert!(successor.status["retry"]
                .as_str()
                .unwrap()
                .contains("withdrawn chained successor"));
        }
        std::fs::write(
            f.copy.join("REVIEW-NOTES.md"),
            &f.expected.files()["REVIEW-NOTES.md"],
        )
        .unwrap();
        if one_step {
            assert!(start_workflow_run(&f.root, &next)
                .unwrap_err()
                .contains("withdrawn"));
        } else {
            start_workflow_run(&f.root, &next).unwrap();
            assert_eq!(f.peer.turn_starts(), starts + 1);
        }
    }
}
