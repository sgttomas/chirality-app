use super::*;

struct Fixture {
    base: PathBuf,
    root: PathBuf,
    store: PathBuf,
    bag: PathBuf,
    project: String,
}
fn actor() -> Value {
    crate::act_control::person(Some("Invented restore actor"), Some("fixture"))
}
fn observed() -> Value {
    json!({"fixture":"native restore test double"})
}
impl Fixture {
    fn new() -> Self {
        let base = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("package-identity-").unwrap());
        let root = base.join("project");
        std::fs::create_dir_all(&root).unwrap();
        let choose = |store: PathBuf| {
            use_store_for_test(Some(Ok(Store {
                root: store,
                placement: Placement::Test,
                limits: vec![],
            })))
        };
        choose(base.join("source-store"));
        crate::records::append_project(
            &root,
            None,
            "writer:restore",
            "evidence_limit",
            &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented restore source"}),
        )
        .unwrap();
        let project = attach(&root, false).unwrap().project.unwrap();
        let bag = base.join("exports/bag");
        std::fs::create_dir_all(bag.parent().unwrap()).unwrap();
        crate::records_export::export(&root, &bag).unwrap();
        let store = base.join("new-store");
        choose(store.clone());
        Self {
            base,
            root,
            store,
            bag,
            project,
        }
    }
    fn minted(&self) -> PathBuf {
        std::fs::remove_file(self.root.join(PROJECT_LINK)).unwrap();
        attach(&self.root, true).unwrap().dir.unwrap()
    }
    fn restore(&self) -> Plan {
        prepare_restore(&self.root, &self.bag, &actor(), &observed()).unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        STOP.with(|s| s.borrow_mut().take());
        BEFORE_LINK.with(|h| h.borrow_mut().take());
        use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.base);
    }
}

#[test]
fn package_identity_linkless_native_restore_creates_original_identity_without_minting() {
    let f = Fixture::new();
    std::fs::remove_file(f.root.join(PROJECT_LINK)).unwrap();
    assert!(prepare(&f.root, &f.bag, &actor(), &observed()).is_err());
    let plan = f.restore();
    assert!(plan.intent.link_before.is_none());
    assert!(plan.intent.association.is_some());
    let result = apply(plan, &actor(), &observed()).unwrap();
    assert_eq!(result["projectId"], f.project);
    assert_eq!(
        attach(&f.root, false).unwrap().project,
        Some(f.project.clone())
    );
    assert!(complete_exists(&project_dir(&f.store, &f.project)));
}

#[test]
fn package_identity_unused_startup_identity_is_released_with_all_its_bytes_preserved() {
    let f = Fixture::new();
    let q = f.minted();
    let before = bag::payload_inventory(&q).unwrap();
    let plan = f.restore();
    let old = plan
        .intent
        .association
        .as_ref()
        .unwrap()
        .prior
        .as_ref()
        .unwrap()
        .project
        .clone();
    assert_ne!(old, f.project);
    apply(plan, &actor(), &observed()).unwrap();
    assert_eq!(bag::payload_inventory(&q).unwrap(), before);
    assert!(roots_of(&roots(&f.store).unwrap(), &old).is_empty());
    assert_eq!(
        attach(&f.root, false).unwrap().project,
        Some(f.project.clone())
    );
    assert!(crate::storage::create_json(
        &q.join("late-queued.json"),
        &json!({"fixture":"stale queued write"})
    )
    .is_err());
    assert!(!q.join("late-queued.json").exists());
    assert!(writer_lock(&q, false)
        .err()
        .unwrap()
        .contains("association changed"));
}

#[test]
fn package_identity_prior_used_held_closed_or_ambiguous_identity_is_never_replaced() {
    for variant in [
        "used",
        "held",
        "closed",
        "unknown",
        "empty-unknown",
        "another-root",
    ] {
        let f = Fixture::new();
        let q = f.minted();
        match variant {
            "used" => {
                crate::records::append_project(
                    &f.root,
                    None,
                    "writer:q",
                    "evidence_limit",
                    &crate::records::APP_WRITER,
                    json!({"label":"unresolvable reference","subjectRef":"used prior"}),
                )
                .unwrap();
            }
            "held" | "closed" => {
                let action = if variant == "held" {
                    "set-hold"
                } else {
                    "close"
                };
                let p = retention::prepare(&f.root, action, None, &actor(), &observed()).unwrap();
                retention::apply(p, &actor(), &observed()).unwrap();
            }
            "empty-unknown" => {
                std::fs::create_dir(q.join("unexplained-empty")).unwrap();
            }
            "unknown" => {
                bag::create_or_match(&controls(&q).unwrap().join("unknown.json"), b"{}").unwrap();
            }
            "another-root" => {
                let other = f.base.join("other");
                std::fs::create_dir(&other).unwrap();
                let old = attach(&f.root, false).unwrap().project.unwrap();
                append_line(&f.store.join("roots.jsonl"),&json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":old,"root":other,"how":"adopted"})).unwrap();
            }
            _ => unreachable!(),
        }
        let link = plain(&f.root.join(PROJECT_LINK)).unwrap();
        let data = bag::payload_inventory(&q).unwrap();
        assert!(
            prepare_restore(&f.root, &f.bag, &actor(), &observed()).is_err(),
            "{variant}"
        );
        assert_eq!(plain(&f.root.join(PROJECT_LINK)).unwrap(), link);
        assert_eq!(bag::payload_inventory(&q).unwrap(), data);
    }
}

#[test]
fn package_identity_roots_interruption_retries_same_original_and_fences_startup_and_queued_q() {
    let f = Fixture::new();
    let q = f.minted();
    let before = bag::payload_inventory(&q).unwrap();
    let plan = f.restore();
    let id = plan.intent.id.clone();
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert!(attach(&f.root, true).is_err());
    assert!(writer_lock(&q, false).is_err());
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    assert_eq!(retry.intent.id, id);
    apply(retry, &actor(), &observed()).unwrap();
    assert_eq!(bag::payload_inventory(&q).unwrap(), before);
}

#[test]
fn package_identity_missing_project_reference_and_link_are_recovered_from_one_active_original() {
    let f = Fixture::new();
    let _q = f.minted();
    let plan = f.restore();
    let intent = plan.intent.clone();
    bag::fail_control_before_publish_for_test(Some(intent.path().unwrap()));
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert!(!intent.path().unwrap().exists());
    assert!(active(&f.store).join("intent.json").exists());
    std::fs::remove_file(f.root.join(PROJECT_LINK)).unwrap();
    SEEN.lock()
        .unwrap_or_else(|p| p.into_inner())
        .remove(&intent.dir());
    UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .remove(&intent.dir());
    assert!(attach(&f.root, true).is_err());
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    assert_eq!(retry.intent.id, intent.id);
    apply(retry, &actor(), &observed()).unwrap();
    let stored = plain(&intent.path().unwrap()).unwrap();
    assert_eq!(
        bag::parse_json_unique(&stored).unwrap()["format"],
        REFERENCE
    );
    assert_eq!(std::fs::read_dir(active(&f.store)).unwrap().count(), 1);
}

#[test]
fn package_identity_late_unrelated_link_is_never_adopted_as_a_new_overwrite_precondition() {
    let f = Fixture::new();
    let q = f.minted();
    let before = bag::payload_inventory(&q).unwrap();
    let plan = f.restore();
    let path = f.root.join(PROJECT_LINK);
    let unrelated = json_bytes(&link_value(
        "chirality-project:unrelated-late-link",
        "different-store",
    ))
    .unwrap();
    let changed = unrelated.clone();
    let target = path.clone();
    BEFORE_LINK.with(|h| {
        *h.borrow_mut() = Some(Box::new(move || {
            std::fs::write(target, changed).unwrap();
        }))
    });
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert_eq!(plain(&path).unwrap(), unrelated);
    assert_eq!(bag::payload_inventory(&q).unwrap(), before);
}

#[test]
fn package_identity_historical_root_locators_keep_imported_prefix_held_when_older_project_reference_disappears(
) {
    let f = Fixture::new();
    let _q = f.minted();
    apply(f.restore(), &actor(), &observed()).unwrap();
    let older = resolve_root(&f.root).unwrap().unwrap();
    let dir = older.dir();
    let log = older
        .copied
        .keys()
        .find(|name| name.ends_with(".jsonl"))
        .unwrap()
        .clone();
    let original = plain(&dir.join(&log)).unwrap();
    assert_eq!(
        quoted_prefix(&dir, &log, &original).unwrap(),
        older.copied[&log].bytes
    );
    new_identity(&f.root).unwrap();
    apply(f.restore(), &actor(), &observed()).unwrap();
    let newer = resolve_root(&f.root).unwrap().unwrap();
    assert_ne!(older.id, newer.id);
    assert!(history(&f.store, &older.id).join("intent.json").exists());
    std::fs::remove_file(older.path().unwrap()).unwrap();
    SEEN.lock().unwrap_or_else(|p| p.into_inner()).remove(&dir);
    let required = required_intents(&dir).unwrap();
    assert!(required.contains(&older.id) && required.contains(&newer.id));
    assert!(
        quoted_prefix(&dir, &log, &original).is_err(),
        "a missing older local reference must withhold provenance, never turn the prefix native"
    );
    let raw = intent_bytes(&older).unwrap();
    older
        .publish(&older.path().unwrap(), &entry_bytes(&older, &raw).unwrap())
        .unwrap();
    assert_eq!(
        quoted_prefix(&dir, &log, &original).unwrap(),
        older.copied[&log].bytes
    );
    std::fs::remove_file(history(&f.store, &older.id).join("intent.json")).unwrap();
    assert!(
        required_intents(&dir).is_err(),
        "locators cannot reconstruct a missing original native act"
    );
}

#[test]
fn package_identity_same_byte_original_replacement_invalidates_provenance_and_native_review() {
    let f = Fixture::new();
    let _q = f.minted();
    let plan = f.restore();
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    let intent = retry.intent.clone();
    let raw = intent_bytes(&intent).unwrap();
    let first = original_context(&intent, &raw).unwrap();
    let original_path = PathBuf::from(first["path"].as_str().unwrap());
    let alternate = original_path.with_file_name("same-byte-replacement");
    bag::create_or_match(&alternate, &raw).unwrap();
    std::fs::rename(&alternate, &original_path).unwrap();
    assert_ne!(original_context(&intent, &raw).unwrap(), first);
    assert!(apply(retry, &actor(), &observed()).is_err());
    assert_eq!(plain(&original_path).unwrap(), raw);
}

#[test]
fn package_identity_completed_restore_releases_an_old_path_for_a_new_physical_project() {
    let f = Fixture::new();
    let _q = f.minted();
    let plan = f.restore();
    let intent = plan.intent.clone();
    apply(plan, &actor(), &observed()).unwrap();
    let raw = intent_bytes(&intent).unwrap();
    let payload = bag::payload_inventory(&intent.dir()).unwrap();
    let moved = f.base.join("moved-project");
    std::fs::rename(&f.root, &moved).unwrap();
    adopt(&moved).unwrap();
    std::fs::create_dir(&f.root).unwrap();
    assert!(resolve_root(&f.root).unwrap().is_none());
    let fresh = attach(&f.root, true).unwrap();
    assert_ne!(fresh.project.as_deref(), Some(f.project.as_str()));
    assert!(fresh.refusal.is_none());
    assert!(resolve_root(&f.root).unwrap().is_none());
    assert_eq!(super::super::status(&f.root)["state"], "none");
    assert_eq!(
        attach(&moved, false).unwrap().project,
        Some(f.project.clone())
    );
    assert_eq!(intent_bytes(&intent).unwrap(), raw);
    assert_eq!(bag::payload_inventory(&intent.dir()).unwrap(), payload);
}

#[test]
fn package_identity_unfinished_restore_keeps_its_physical_root_fence() {
    let f = Fixture::new();
    let _q = f.minted();
    let plan = f.restore();
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    std::fs::rename(&f.root, f.base.join("unfinished-project-moved")).unwrap();
    std::fs::create_dir(&f.root).unwrap();
    assert!(resolve_root(&f.root).is_err());
    assert!(attach(&f.root, true).is_err());
}

#[test]
fn package_identity_lost_roots_registry_does_not_release_a_completed_physical_root() {
    for truncated in [false, true] {
        let f = Fixture::new();
        let _q = f.minted();
        let plan = f.restore();
        apply(plan, &actor(), &observed()).unwrap();
        std::fs::rename(&f.root, f.base.join("retained-project")).unwrap();
        std::fs::create_dir(&f.root).unwrap();
        let registry = f.store.join("roots.jsonl");
        if truncated {
            std::fs::write(&registry, b"").unwrap();
        } else {
            std::fs::remove_file(&registry).unwrap();
        }
        assert!(
            resolve_root(&f.root).is_err(),
            "lost registry is not a root release"
        );
        assert!(attach(&f.root, true).is_err());
    }
}
