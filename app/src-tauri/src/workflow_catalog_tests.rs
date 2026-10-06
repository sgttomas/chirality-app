//! Same-crate retained tests; original test bodies preserved from integration target.
use crate::workflow_workspace;
use crate::{role_supply, workflow_declaration, util};
use workflow_workspace::{
    development_catalog::{DevelopmentCatalog, NAME, STANDING},
    Snapshot,
};

struct Copy(std::path::PathBuf);
static COPY_SEQUENCE: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
impl Copy {
    fn new() -> Self {
        let root = std::env::temp_dir().join(format!(
            "chirality-catalog-{}-{}-{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos(),
            COPY_SEQUENCE.fetch_add(1, std::sync::atomic::Ordering::Relaxed)
        ));
        std::fs::create_dir(&root).unwrap();
        Self(root)
    }
    fn package(&self) -> std::path::PathBuf {
        self.0.join(NAME)
    }
    fn populate(&self) {
        DevelopmentCatalog::load()
            .unwrap()
            .select_embedded()
            .snapshot()
            .publish_new(&self.package())
            .unwrap();
    }
}
impl Drop for Copy {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

#[test]
fn actual_embedded_package_preserves_full_tuple_and_both_files() {
    let catalog = DevelopmentCatalog::load().unwrap();
    let selection = catalog.select_embedded();
    let id = selection.identity();
    assert_eq!(
        (&*id.kind, &*id.origin, &*id.source_root, &*id.name),
        ("workflow", "bundled", "chirality-root", NAME)
    );
    assert_eq!(
        id.revision,
        "1b1733864cd89fd6d8ca74bf3e2084ff1105c1fc7d76537eefb42e2ae9a41e83"
    );
    assert_eq!(selection.snapshot().files().len(), 2);
    assert!(selection.snapshot().files().contains_key("REVIEW-NOTES.md"));
    assert!(selection
        .snapshot()
        .workflow_text()
        .contains("(REVIEW-NOTES.md)"));
    assert_eq!(catalog.standing(), STANDING);
    assert!(id.derived_from.is_none());
}

#[test]
fn exact_holding_copy_preserves_origin_and_location_then_detects_mutation() {
    let copy = Copy::new();
    copy.populate();
    let catalog = DevelopmentCatalog::load().unwrap();
    let held = catalog.recognize_holding_copy(&copy.package()).unwrap();
    assert_eq!(held.selection().identity(), catalog.identity());
    assert_eq!(held.package_path(), copy.package());
    held.verify_current().unwrap();
    std::fs::write(copy.package().join("REVIEW-NOTES.md"), "changed notes").unwrap();
    assert!(held.verify_current().is_err());
    assert!(catalog.recognize_holding_copy(&copy.package()).is_err());
    assert_eq!(held.selection().identity(), catalog.identity());
}

#[test]
fn additional_or_missing_file_is_not_the_admitted_package() {
    let copy = Copy::new();
    copy.populate();
    let catalog = DevelopmentCatalog::load().unwrap();
    std::fs::write(copy.package().join("extra.txt"), "extra").unwrap();
    assert!(catalog.recognize_holding_copy(&copy.package()).is_err());
    std::fs::remove_file(copy.package().join("extra.txt")).unwrap();
    std::fs::remove_file(copy.package().join("REVIEW-NOTES.md")).unwrap();
    assert!(catalog.recognize_holding_copy(&copy.package()).is_err());
}

#[test]
fn equal_bytes_under_other_name_or_relative_location_cannot_be_recognized() {
    let copy = Copy::new();
    copy.populate();
    let catalog = DevelopmentCatalog::load().unwrap();
    let other = copy.0.join("other-name");
    std::fs::rename(copy.package(), &other).unwrap();
    assert!(catalog.recognize_holding_copy(&other).is_err());
    assert!(catalog
        .recognize_holding_copy(std::path::Path::new(NAME))
        .is_err());
}

#[test]
fn same_name_other_origin_collision_does_not_rebind_catalog_selection() {
    let catalog = DevelopmentCatalog::load().unwrap();
    let mut other = catalog.identity().clone();
    other.origin = "project".into();
    other.source_root = "project-source".into();
    let entries = [other, catalog.identity().clone()];
    assert_eq!(workflow_workspace::collisions(NAME, &entries).len(), 2);
    assert_eq!(catalog.select_embedded().identity(), catalog.identity());
}

#[cfg(unix)]
#[test]
fn non_regular_holding_copy_cannot_be_recognized() {
    let copy = Copy::new();
    copy.populate();
    let notes = copy.package().join("REVIEW-NOTES.md");
    std::fs::remove_file(&notes).unwrap();
    std::os::unix::fs::symlink(copy.package().join("WORKFLOW.md"), notes).unwrap();
    assert!(DevelopmentCatalog::load()
        .unwrap()
        .recognize_holding_copy(&copy.package())
        .is_err());
}

#[test]
fn tuple_claims_are_data_and_do_not_change_fixed_catalog_admission() {
    let catalog = DevelopmentCatalog::load().unwrap();
    let mut arbitrary = catalog.select_embedded().snapshot().files().clone();
    arbitrary.insert(
        "WORKFLOW.md".into(),
        b"---\nname: coordinated-knowledge-work\n---\nChanged method\n".to_vec(),
    );
    let arbitrary = Snapshot::from_files(arbitrary).unwrap();
    let claimed = arbitrary
        .identity("bundled", "chirality-root", NAME, None)
        .unwrap();
    assert_ne!(claimed, *catalog.identity());
    assert_eq!(catalog.select_embedded().identity(), catalog.identity());
}

#[test]
fn development_provenance_survives_holding_and_run_preparation() {
    use workflow_workspace::{PreparedRunText, RunScope, SelectionAdmission};
    let copy = Copy::new();
    copy.populate();
    let catalog = DevelopmentCatalog::load().unwrap();
    let held = catalog.recognize_holding_copy(&copy.package()).unwrap();
    let scope = RunScope {
        run: "run-development".into(),
        conversation: "thread-test".into(),
        home: "home-test".into(),
        generation: serde_json::json!({"appSession":"session-test","home":"home-test","spawnCounter":1}),
        source_root: "chirality-root".into(),
        holding_library: copy.0.to_string_lossy().into_owned(),
        selection_ref: "selection-development-test".into(),
        revision_store: copy.package(),
    };
    let prepared = PreparedRunText::start(held.selection(), scope, NAME, None).unwrap();
    assert_eq!(prepared.admission(), held.selection().admission());
    assert_eq!(prepared.admission().standing(), STANDING);
    match prepared.admission() {
        SelectionAdmission::DevelopmentCatalog {
            source_map_sha256,
            tranche,
        } => {
            assert_eq!(
                source_map_sha256,
                &util::sha256_hex(include_bytes!(
                    "../resources/development_workflows/SOURCE_MAP.json"
                ))
            );
            assert_eq!(tranche, "APP-V4-GROUP-A-DEVELOPMENT-WORKFLOW-20261005");
        }
        _ => panic!("development package lost its owning provenance"),
    }
    // Observation metadata does not change the canonical WR record schema.
    assert!(prepared.record().get("admission").is_none());
}
