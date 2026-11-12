use super::*;

struct Fixture {
    base: PathBuf,
    root: PathBuf,
    source: PathBuf,
    destination: PathBuf,
    bag: PathBuf,
    project: String,
    original: BTreeMap<String, bag::Member>,
}
fn actor() -> Value {
    crate::act_control::person(Some("Invented fixture"), Some("fixture-account"))
}
fn observed() -> Value {
    json!({"fixture":"native context test double; no actual human act"})
}
impl Fixture {
    fn new() -> Self {
        Self::named("project")
    }
    fn named(name: &str) -> Self {
        let base = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("package-import-test-").unwrap());
        let root = base.join(name);
        std::fs::create_dir_all(&root).unwrap();
        let source = base.join("source-store");
        let destination = base.join("destination-store");
        Self::choose(&source);
        crate::records::append_project(
            &root,
            Some("run:fixture"),
            "app-writer:local",
            "evidence_limit",
            &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented fixture"}),
        )
        .unwrap();
        let attachment = attach(&root, false).unwrap();
        let project = attachment.project.unwrap();
        let dir = attachment.dir.unwrap();
        let log =
            crate::storage::project_log(&root, Some("run:fixture"), "app-writer:local").unwrap();
        let specs = (0..2)
            .map(|n| crate::records::Spec {
                kind: "evidence_limit",
                recorder: &crate::records::APP_WRITER,
                body: json!({"label":"unresolvable reference","subjectRef":format!("group {n}")}),
                id: format!("rec:app:group-{n}"),
                observed_at: None,
            })
            .collect();
        crate::records::append_group(
            &log,
            specs,
            Some("run:fixture"),
            crate::records::RecordSet::Complete,
        )
        .unwrap();
        std::fs::create_dir_all(dir.join("connectors")).unwrap();
        std::fs::write(
            dir.join("connectors/.route-interrupted.tmp"),
            b"original interrupted bytes",
        )
        .unwrap();
        std::fs::write(
            dir.join("connectors/retained.lock"),
            b"ordinary retained evidence",
        )
        .unwrap();
        let bag = base.join("export/bag");
        std::fs::create_dir_all(bag.parent().unwrap()).unwrap();
        crate::records_export::export(&root, &bag).unwrap();
        let original = bag::payload_inventory(&dir).unwrap();
        Self::choose(&destination);
        Self {
            base,
            root,
            source,
            destination,
            bag,
            project,
            original,
        }
    }
    fn choose(path: &Path) {
        use_store_for_test(Some(Ok(Store {
            root: path.into(),
            placement: Placement::Test,
            limits: vec![],
        })));
    }
    fn dir(&self) -> PathBuf {
        project_dir(&self.destination, &self.project)
    }
    fn plan(&self) -> Plan {
        prepare(&self.root, &self.bag, &actor(), &observed()).unwrap()
    }
    fn import(&self) -> Value {
        apply(self.plan(), &actor(), &observed()).unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.base);
    }
}

#[test]
fn package_import_preserves_original_identity_bytes_groups_and_source() {
    let f = Fixture::new();
    let source_before = bag::payload_inventory(&project_dir(&f.source, &f.project)).unwrap();
    let package_before = std::fs::read(f.bag.join("tagmanifest-sha256.txt")).unwrap();
    let result = f.import();
    assert_eq!(result["state"], "package imported");
    let current = bag::payload_inventory(&f.dir()).unwrap();
    for (name, m) in &f.original {
        assert_eq!(current.get(name), Some(m), "{name}");
    }
    assert_eq!(
        source_before,
        bag::payload_inventory(&project_dir(&f.source, &f.project)).unwrap()
    );
    assert_eq!(
        package_before,
        std::fs::read(f.bag.join("tagmanifest-sha256.txt")).unwrap()
    );
    assert!(crate::records_export::verify(&f.bag).is_ok());
    assert_eq!(
        attach(&f.root, false).unwrap().project.as_deref(),
        Some(f.project.as_str())
    );
    assert!(home(&f.root).unwrap().store_mode);
    assert_eq!(status(&f.root)["state"], "complete");
    let bag2 = f.base.join("export/reexport");
    crate::records_export::export(&f.root, &bag2).unwrap();
    assert!(bag2.join("data/package-imports").is_dir());
}

#[test]
fn package_import_interrupted_phases_fence_reads_and_resume_same_intent() {
    for at in [
        "payload",
        "administration",
        "roots-partial",
        "roots",
        "link",
        "completion",
        "completion-published",
    ] {
        let f = Fixture::new();
        let plan = f.plan();
        let id = plan.intent.id.clone();
        STOP.with(|s| *s.borrow_mut() = Some(at));
        assert!(apply(plan, &actor(), &observed())
            .unwrap_err()
            .contains("test interruption"));
        assert_eq!(status(&f.root)["state"], "incomplete");
        assert!(home(&f.root).is_err(), "{at}: read must remain fenced");
        assert!(
            write_dir(&f.root).is_err(),
            "{at}: writes must remain fenced"
        );
        // Model restart: durable evidence, not volatile uncertainty, must fence.
        // A visible completed control must be reconciled in this process. A
        // cold process may use it if it actually survived the interruption.
        if at != "completion-published" {
            UNCERTAIN.lock().unwrap().remove(&f.dir());
        }
        assert!(require_complete(&f.dir()).is_err());
        let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
        assert_eq!(retry.intent.id, id);
        apply(retry, &actor(), &observed()).unwrap();
        assert!(require_complete(&f.dir()).is_ok());
        assert_eq!(entries(&f.dir()).unwrap().len(), 1);
        for (name, m) in &f.original {
            assert_eq!(bag::payload_inventory(&f.dir()).unwrap().get(name), Some(m));
        }
    }
}

#[test]
fn package_import_refuses_changed_context_and_conflicts_without_replacement() {
    let f = Fixture::new();
    let plan = f.plan();
    let original = std::fs::read(f.root.join(PROJECT_LINK)).unwrap();
    std::fs::write(f.root.join(PROJECT_LINK), b"different local association").unwrap();
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert!(entries(&f.dir()).unwrap().is_empty());
    std::fs::write(f.root.join(PROJECT_LINK), original).unwrap();
    let conflict = f.dir().join("connectors/retained.lock");
    std::fs::create_dir_all(conflict.parent().unwrap()).unwrap();
    std::fs::write(&conflict, b"different target bytes").unwrap();
    assert!(prepare(&f.root, &f.bag, &actor(), &observed()).is_err());
    assert_eq!(std::fs::read(conflict).unwrap(), b"different target bytes");
}

#[test]
fn package_import_refuses_group_member_identity_collision_in_another_target_log() {
    let f = Fixture::new();
    std::fs::create_dir_all(f.dir().join("acts")).unwrap();
    std::fs::write(
        f.dir().join("acts/other.jsonl"),
        b"{\"recordId\":\"rec:app:group-1\"}\n",
    )
    .unwrap();
    let error = prepare(&f.root, &f.bag, &actor(), &observed())
        .err()
        .unwrap();
    assert!(error.contains("group-1"), "{error}");
    assert!(entries(&f.dir()).unwrap().is_empty());
}

#[test]
fn package_import_revalidation_refuses_actor_source_or_target_mutation() {
    let f = Fixture::new();
    let plan = f.plan();
    assert!(apply(plan, &actor(), &json!({"changed":true})).is_err());
    let plan = f.plan();
    std::fs::write(f.dir().join("unreviewed"), b"new local bytes").unwrap();
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert!(entries(&f.dir()).unwrap().is_empty());
    std::fs::remove_file(f.dir().join("unreviewed")).unwrap();
    let plan = f.plan();
    std::fs::write(f.bag.join("bag-info.txt"), b"source changed").unwrap();
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert!(entries(&f.dir()).unwrap().is_empty());
}

#[test]
fn package_import_recovery_refuses_edited_original_or_staged_package() {
    for edit_stage in [false, true] {
        let f = Fixture::new();
        let plan = f.plan();
        let stage = plan.intent.stage.clone();
        STOP.with(|s| *s.borrow_mut() = Some("payload"));
        assert!(apply(plan, &actor(), &observed()).is_err());
        if edit_stage {
            std::fs::write(stage.join("bag-info.txt"), b"edited after intent").unwrap();
        } else {
            let name = f.original.keys().next().unwrap();
            let path = f.dir().join(name);
            std::fs::create_dir_all(path.parent().unwrap()).unwrap();
            std::fs::write(path, b"conflicting partial publication").unwrap();
        }
        assert!(prepare_resume(&f.root, &actor(), &observed()).is_err());
        assert!(require_complete(&f.dir()).is_err());
    }
}

#[test]
fn package_import_existing_newer_hold_and_closure_survive_recovery() {
    let f = Fixture::new();
    Fixture::choose(&f.source);
    for action in ["set-hold", "close"] {
        let plan = retention::prepare(&f.root, action, None, &actor(), &observed()).unwrap();
        retention::apply(plan, &actor(), &observed()).unwrap();
    }
    // Restore a missing payload member from an older package into the same store.
    let dir = project_dir(&f.source, &f.project);
    std::fs::remove_file(dir.join("connectors/retained.lock")).unwrap();
    let plan = prepare(&f.root, &f.bag, &actor(), &observed()).unwrap();
    apply(plan, &actor(), &observed()).unwrap();
    let state = retention::view(&dir);
    assert_eq!(state["closed"], true);
    assert_eq!(state["legalHold"], true);
    assert!(write_dir(&f.root).is_err());
    assert!(home(&f.root).unwrap().store_mode);
}

#[test]
fn package_import_never_mints_over_missing_or_different_project_identity() {
    let f = Fixture::new();
    std::fs::remove_file(f.root.join(PROJECT_LINK)).unwrap();
    assert!(prepare(&f.root, &f.bag, &actor(), &observed()).is_err());
    assert!(!f.root.join(PROJECT_LINK).exists());
    std::fs::write(
        f.root.join(PROJECT_LINK),
        json_bytes(&link_value("chirality-project:other", "other-store")).unwrap(),
    )
    .unwrap();
    assert!(prepare(&f.root, &f.bag, &actor(), &observed()).is_err());
    assert!(
        matches!(read_link(&f.root),Link::Present{project,..} if project=="chirality-project:other")
    );
}

#[test]
fn package_import_second_interruption_resumes_only_its_own_intent() {
    for at in ["payload", "completion-published"] {
        let f = Fixture::new();
        f.import();
        Fixture::choose(&f.source);
        std::fs::write(
            project_dir(&f.source, &f.project).join("additional-evidence.json"),
            b"new exact source member",
        )
        .unwrap();
        let second = f.base.join("export/second");
        crate::records_export::export(&f.root, &second).unwrap();
        Fixture::choose(&f.destination);
        let plan = prepare(&f.root, &second, &actor(), &observed()).unwrap();
        let id = plan.intent.id.clone();
        STOP.with(|s| *s.borrow_mut() = Some(at));
        assert!(apply(plan, &actor(), &observed()).is_err());
        assert_eq!(status(&f.root)["importId"], id);
        let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
        assert_eq!(retry.intent.id, id);
        apply(retry, &actor(), &observed()).unwrap();
        assert_eq!(entries(&f.dir()).unwrap().len(), 2);
        assert!(require_complete(&f.dir()).is_ok());
    }
}

#[test]
fn package_import_exact_repeat_is_idempotent_and_keeps_original_origin() {
    let f = Fixture::new();
    f.import();
    let before = bag::payload_inventory(&f.dir()).unwrap();
    let origin = provenance_context(&f.dir()).unwrap();
    let result = f.import();
    assert_eq!(result["state"], "package already present");
    assert_eq!(bag::payload_inventory(&f.dir()).unwrap(), before);
    assert_eq!(provenance_context(&f.dir()).unwrap(), origin);
    assert_eq!(entries(&f.dir()).unwrap().len(), 1);
}

#[test]
fn package_import_partial_control_publications_leave_recoverable_private_evidence() {
    for control in ["intent", "receipt", "completion"] {
        let f = Fixture::new();
        let plan = f.plan();
        let i = plan.intent.clone();
        let path = match control {
            "intent" => i.path().unwrap(),
            "receipt" => f.dir().join(i.receipt_relative()),
            _ => i.completion_path().unwrap(),
        };
        bag::fail_control_before_publish_for_test(Some(path));
        assert!(apply(plan, &actor(), &observed()).is_err());
        assert!(
            std::fs::read_dir(i.stage.parent().unwrap().join("control-staging"))
                .unwrap()
                .count()
                > 0
        );
        // No partial temporary enters either authoritative inventory.
        let controls = std::fs::read_dir(journal(&f.dir()).unwrap())
            .unwrap()
            .map(|e| e.unwrap().file_name().to_string_lossy().into_owned())
            .collect::<Vec<_>>();
        assert!(controls.iter().all(|n| !n.starts_with('.')));
        assert!(bag::payload_inventory(&f.dir())
            .unwrap()
            .keys()
            .all(|n| !n.contains(".tmp") || n == "connectors/.route-interrupted.tmp"));
        UNCERTAIN.lock().unwrap().remove(&f.dir());
        if control == "intent" {
            assert!(
                require_complete(&f.dir()).is_ok(),
                "no intent was published and no payload was admitted"
            );
            assert!(entries(&f.dir()).unwrap().is_empty());
            f.import();
        } else {
            assert!(require_complete(&f.dir()).is_err());
            let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
            assert_eq!(retry.intent.id, i.id);
            apply(retry, &actor(), &observed()).unwrap();
        }
        assert!(require_complete(&f.dir()).is_ok());
    }
}

#[test]
fn package_import_resume_preserves_unrelated_newer_roots_tail() {
    let f = Fixture::new();
    let plan = f.plan();
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    append_line(&f.destination.join("roots.jsonl"),&json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":"other-project","root":f.base.join("other-folder"),"how":"registered"})).unwrap();
    let before = std::fs::read(f.destination.join("roots.jsonl")).unwrap();
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    apply(retry, &actor(), &observed()).unwrap();
    assert_eq!(
        std::fs::read(f.destination.join("roots.jsonl")).unwrap(),
        before
    );
}

// ---- The registry's frozen write and the store's own appender ----

/// While an interrupted package import's frozen registry write is pending,
/// a registration, an adoption and a new identity each refuse and leave the
/// registry's bytes as they were, the startup recovery leaves them too, and
/// finishing the import then succeeds as before; afterwards the registry is
/// appended to again.
#[test]
fn package_import_pending_registry_write_holds_every_other_registry_append_until_finished() {
    for at in ["payload", "administration", "roots-partial"] {
        let f = Fixture::new();
        let plan = f.plan();
        assert!(plan.intent.roots_final.len() > plan.intent.roots_original.len(), "{at}: the import appends registry rows");
        STOP.with(|s| *s.borrow_mut() = Some(at));
        assert!(apply(plan, &actor(), &observed()).unwrap_err().contains("test interruption"));
        let path = f.destination.join("roots.jsonl");
        let before = std::fs::read(&path).ok();
        if at == "roots-partial" {
            assert!(!before.as_ref().unwrap().ends_with(b"\n"), "the frozen write left a fragment");
        }
        let pending = "package import's write to the registry of project folders is pending";
        let other = f.base.join("other-folder");
        std::fs::create_dir_all(&other).unwrap();
        let registration = attach(&other, true).unwrap_err();
        assert!(registration.contains(pending), "{at}: registration: {registration}");
        let renamed = f.base.join("renamed-folder");
        std::fs::create_dir_all(&renamed).unwrap();
        let identity = new_identity(&renamed).unwrap_err();
        assert!(identity.contains(pending), "{at}: new identity: {identity}");
        let adopted = f.base.join("adopted-folder");
        std::fs::create_dir_all(adopted.join(".chirality")).unwrap();
        let store_id: Value = serde_json::from_slice(&std::fs::read(f.destination.join("store.json")).unwrap()).unwrap();
        std::fs::write(adopted.join(PROJECT_LINK), serde_json::to_vec(&link_value("chirality-project:invented-adopted", store_id["storeId"].as_str().unwrap())).unwrap()).unwrap();
        let adoption = adopt(&adopted).unwrap_err();
        assert!(adoption.contains(pending), "{at}: adoption: {adoption}");
        let left = recover_at_startup().unwrap();
        if at == "roots-partial" {
            assert!(left.iter().any(|l| l.contains(pending)), "{at}: {left:?}");
        }
        assert_eq!(std::fs::read(&path).ok(), before, "{at}: the registry's bytes are unchanged");
        UNCERTAIN.lock().unwrap().remove(&f.dir());
        let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
        apply(retry, &actor(), &observed()).unwrap();
        assert!(require_complete(&f.dir()).is_ok(), "{at}: the import finishes");
        assert_eq!(attach(&f.root, false).unwrap().project.as_deref(), Some(f.project.as_str()));
        // The refused mint wrote the folder's link first (the link-first
        // order); the registry now takes its line.
        assert_eq!(attach(&other, true).unwrap().how, "registered", "{at}: then the registry is appended to again");
    }
}

/// Without a pending import, a fragment in the registry is closed and named,
/// and the package import's readers (its frozen-prefix comparison and its
/// registry reading) ignore the naming line and the set-aside line.
#[test]
fn package_import_readers_ignore_a_closed_and_named_fragment_in_a_later_tail() {
    let f = Fixture::new();
    let plan = f.plan();
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    let path = f.destination.join("roots.jsonl");
    let mut bytes = std::fs::read(&path).unwrap();
    bytes.extend(b"{\"format\":\"chirality.records-store.root\",\"how\":\"rele");
    std::fs::write(&path, &bytes).unwrap();
    *ROOTS.lock().unwrap() = None;
    assert!(recover_at_startup().unwrap().is_empty());
    let after = std::fs::read(&path).unwrap();
    assert!(after.starts_with(&bytes) && after.len() > bytes.len(), "closed and named");
    let read = lines::read(&after, &path);
    assert_eq!(read.set_aside.len(), 1);
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    apply(retry, &actor(), &observed()).unwrap();
    assert!(require_complete(&f.dir()).is_ok());
    assert_eq!(std::fs::read(&path).unwrap(), after, "the import's recovery wrote nothing more");
    assert_eq!(attach(&f.root, false).unwrap().project.as_deref(), Some(f.project.as_str()));
}

/// The package import's own registry write emits no raw 0x1E, even for a
/// project folder whose name holds one: serde_json escapes it.
#[test]
fn package_import_registry_write_emits_no_raw_record_separator() {
    let f = Fixture::named("project\u{1e}folder");
    f.import();
    let registry = std::fs::read(f.destination.join("roots.jsonl")).unwrap();
    assert!(!registry.contains(&lines::MARK));
    assert_eq!(attach(&f.root, false).unwrap().project.as_deref(), Some(f.project.as_str()));
}

/// A registry that already holds a closed and named fragment when an import
/// begins: the import freezes those bytes as its original prefix, and every
/// reading of them (the frozen-prefix comparison, the discovery of its own
/// intents from the frozen bytes, the root association) sets the fragment
/// aside and ignores its naming line.
#[test]
fn package_import_reads_a_registry_holding_a_named_fragment_before_it_began() {
    let f = Fixture::new();
    let store = opened().unwrap().0;
    let path = store.join("roots.jsonl");
    let other = json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":"chirality-project:invented-other","root":f.base.join("elsewhere"),"at":"2026-11-12T00:00:00.000Z","how":"registered"});
    let mut bytes = std::fs::read(&path).unwrap_or_default();
    bytes.extend(serde_json::to_vec(&other).unwrap());
    bytes.extend(b"\n{\"format\":\"chirality.records-store.root\",\"projectId\":\"");
    std::fs::write(&path, &bytes).unwrap();
    *ROOTS.lock().unwrap() = None;
    recover_at_startup().unwrap();
    let closed = std::fs::read(&path).unwrap();
    assert_eq!(lines::read(&closed, &path).set_aside.len(), 1);
    let plan = f.plan();
    assert_eq!(plan.intent.roots_original, closed, "the frozen prefix holds the named fragment");
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    UNCERTAIN.lock().unwrap().remove(&f.dir());
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    apply(retry, &actor(), &observed()).unwrap();
    assert!(require_complete(&f.dir()).is_ok());
    assert_eq!(status(&f.root)["state"], "complete");
    assert_eq!(attach(&f.root, false).unwrap().project.as_deref(), Some(f.project.as_str()));
    assert!(roots(&store).unwrap().iter().all(|r| r["format"] == ROOT_FORMAT));
}
