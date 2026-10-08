use super::{production_catalog::*, SelectionAdmission, Snapshot};
use std::path::PathBuf;
struct Library(PathBuf);
impl Library {
    fn new() -> Self {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("p2-production-").unwrap());
        std::fs::create_dir_all(root.join(".chirality/workflows")).unwrap();
        Self(root)
    }
    fn package(&self) -> PathBuf {
        self.0
            .join(".chirality/workflows/coordinated-knowledge-work")
    }
    fn populate(&self) {
        ProductionCatalog::load()
            .unwrap()
            .select_embedded()
            .snapshot()
            .publish_new(&self.package())
            .unwrap();
    }
}
impl Drop for Library {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
#[test]
fn candidate_catalog_binds_current_source_without_claiming_release_history() {
    let catalog = ProductionCatalog::load().unwrap();
    let selected = catalog.select_embedded();
    assert_eq!(selected.identity().source_root, RELEASE_SUBJECT);
    assert_eq!(selected.identity().origin, "bundled");
    assert!(matches!(
        selected.admission(),
        SelectionAdmission::ProductionBundle { .. }
    ));
    let source = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../../../workflows/coordinated-knowledge-work");
    assert_eq!(
        Snapshot::capture(&source).unwrap().files(),
        selected.snapshot().files()
    );
    assert_eq!(
        selected.snapshot().declaration().unwrap().reading,
        crate::workflow_declaration::Reading::Undeclared
    );
    let manifest: serde_json::Value = serde_json::from_slice(catalog.manifest()).unwrap();
    assert_eq!(
        manifest["historical_shipped_revisions"],
        serde_json::json!([])
    );
    assert_eq!(manifest["recognize_v3"], false);
    assert_ne!(
        catalog.identity().source_root,
        super::development_catalog::DevelopmentCatalog::load()
            .unwrap()
            .identity()
            .source_root
    );
}
#[test]
fn holding_copy_preserves_tuple_and_refuses_changed_or_additional_bytes() {
    let library = Library::new();
    library.populate();
    let catalog = ProductionCatalog::load().unwrap();
    let held = catalog
        .recognize_holding_copy(&library.0, "coordinated-knowledge-work")
        .unwrap();
    assert_eq!(held.selection().identity(), catalog.identity());
    assert_eq!(held.package_path(), library.package());
    held.verify_current().unwrap();
    std::fs::write(library.package().join("extra.txt"), "changed").unwrap();
    assert!(held.verify_current().is_err());
    assert!(catalog
        .recognize_holding_copy(&library.0, "coordinated-knowledge-work")
        .is_err());
    assert!(catalog
        .recognize_holding_copy(&library.0, "other-name")
        .is_err());
}
#[test]
fn bad_registry_or_orphan_store_never_means_empty_slot() {
    let library = Library::new();
    library.populate();
    let catalog = ProductionCatalog::load().unwrap();
    let held = catalog
        .recognize_holding_copy(&library.0, "coordinated-knowledge-work")
        .unwrap();
    let ledger = library.0.join(".chirality/workflow-registry.jsonl");
    std::fs::write(&ledger, "{broken}\n").unwrap();
    assert!(held.verify_current().is_err());
    assert!(catalog
        .recognize_holding_copy(&library.0, "coordinated-knowledge-work")
        .is_err());
    std::fs::remove_file(ledger).unwrap();
    std::fs::create_dir_all(
        library
            .0
            .join(".chirality/workflow-revisions/coordinated-knowledge-work"),
    )
    .unwrap();
    assert!(held.verify_current().is_err());
}
#[test]
fn held_copy_rejects_drafts_relative_roots_and_links() {
    let catalog = ProductionCatalog::load().unwrap();
    assert!(catalog
        .recognize_holding_copy(
            std::path::Path::new("relative"),
            "coordinated-knowledge-work"
        )
        .is_err());
    let library = Library::new();
    std::fs::create_dir_all(library.0.join(".chirality/workflow-drafts")).unwrap();
    catalog
        .select_embedded()
        .snapshot()
        .publish_new(
            &library
                .0
                .join(".chirality/workflow-drafts/coordinated-knowledge-work"),
        )
        .unwrap();
    assert!(catalog
        .recognize_holding_copy(&library.0, "coordinated-knowledge-work")
        .is_err());
    #[cfg(unix)]
    {
        std::os::unix::fs::symlink(
            library
                .0
                .join(".chirality/workflow-drafts/coordinated-knowledge-work"),
            library.package(),
        )
        .unwrap();
        assert!(catalog
            .recognize_holding_copy(&library.0, "coordinated-knowledge-work")
            .is_err());
    }
}

#[test]
fn existing_registered_slot_refuses_even_byte_equal_copy_and_rechecks_selection() {
    let library = Library::new();
    library.populate();
    let catalog = ProductionCatalog::load().unwrap();
    let held = catalog
        .recognize_holding_copy(&library.0, "coordinated-knowledge-work")
        .unwrap();
    let selected = held.selection().clone();
    let identity = serde_json::json!({"kind":"workflow","origin":"project","source_root":"fixture","name":"coordinated-knowledge-work","revision":"existing","revision_method":"fixture-method"});
    let line = serde_json::json!({"record_kind":"library_entry","ledger_seq":1,"outcome":"registered","identity":identity,"sequence":1,"prior_revision":null,"disposition":"new workflow","reviewed_draft":{"draft":{"draft_location":"project","draft_root":"fixture","name":"coordinated-knowledge-work"},"content":{"method":"fixture-method","value":"existing"}},"act":{"record_id":"rec:fixture:1","capture_evidence":"cap:fixture:1"},"store_path":"workflow-revisions/coordinated-knowledge-work/existing/coordinated-knowledge-work","written_at":"fixture-time","evidence_limits":["synthetic registry observation; no human act"]});
    super::wr_validate("library_entry", &line).unwrap();
    std::fs::write(
        library.0.join(".chirality/workflow-registry.jsonl"),
        format!("{}\n", line),
    )
    .unwrap();
    let error = catalog
        .recognize_holding_copy(&library.0, "coordinated-knowledge-work")
        .err()
        .unwrap();
    assert!(error.contains("registered slot"), "{error}");
    assert!(selected.verify_store(&library.package()).is_err());
}

#[test]
fn installed_bundle_is_actual_resolution_and_manifest_changes_refuse_at_use() {
    let library = Library::new();
    let catalog = ProductionCatalog::load().unwrap();
    let root = library.0.join("bundle-workflows");
    std::fs::create_dir(&root).unwrap();
    let package = root.join("coordinated-knowledge-work");
    catalog
        .select_embedded()
        .snapshot()
        .publish_new(&package)
        .unwrap();
    assert!(catalog
        .select_bundle_package(&root, "coordinated-knowledge-work")
        .is_err());
    std::fs::write(root.join("MANIFEST.json"), catalog.manifest()).unwrap();
    let resolved = catalog
        .select_bundle_package(&root, "coordinated-knowledge-work")
        .unwrap();
    resolved.verify_current().unwrap();
    assert_eq!(resolved.package_path(), package);
    let selected = resolved.selection().clone();
    std::fs::write(root.join("MANIFEST.json"), b"{}").unwrap();
    assert!(selected.verify_store(&package).is_err());
    std::fs::write(root.join("MANIFEST.json"), catalog.manifest()).unwrap();
    std::fs::write(package.join("REVIEW-NOTES.md"), b"edited").unwrap();
    assert!(selected.verify_store(&package).is_err());
}
