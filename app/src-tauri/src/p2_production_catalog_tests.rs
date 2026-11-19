use super::{production_catalog::*, SelectionAdmission, Snapshot};
use std::path::PathBuf;
const NAME: &str = "coordinated-knowledge-work";
/// A bundled package with several files, some in subfolders.
const NESTED: &str = "data-app-spec";
/// The source tree the build bundles as the App's `workflows/` resources.
fn source_tree() -> PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/production_workflows")
}
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
        self.0.join(".chirality/workflows").join(NAME)
    }
    fn populate(&self) {
        ProductionCatalog::load()
            .unwrap()
            .select_source(NAME)
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
    let selected = catalog.select_source(NAME);
    assert_eq!(selected.identity().source_root, RELEASE_SUBJECT);
    assert_eq!(selected.identity().origin, "bundled");
    assert!(matches!(
        selected.admission(),
        SelectionAdmission::ProductionBundle { .. }
    ));
    assert_eq!(
        Snapshot::capture(&source_tree().join(NAME)).unwrap().files(),
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
    assert_eq!(catalog.source()["tag"], "library-v3.4.0");
    assert_ne!(
        catalog.identity(NAME).unwrap().source_root,
        super::development_catalog::DevelopmentCatalog::load()
            .unwrap()
            .identity()
            .source_root
    );
}
// DEL-02-02 AC-014, App side: the catalog is exactly the manifest's packages,
// each resolves from the tree the build bundles with the manifest's bytes and
// revision, and the tree holds no workflow the manifest does not name. That
// the manifest's set is the selected Library's is the generator's comparison
// with the release archive (tools/library_workflows).
#[test]
fn every_manifest_workflow_resolves_from_the_bundled_tree_and_no_other() {
    let catalog = ProductionCatalog::load().unwrap();
    assert_eq!(
        crate::util::sha256_hex(catalog.manifest()),
        SELECTED_BUNDLED_MANIFEST_SHA256,
        "the compiled manifest is the selected subject"
    );
    let root = source_tree();
    assert_eq!(std::fs::read(root.join("MANIFEST.json")).unwrap(), catalog.manifest());
    let manifest: serde_json::Value = serde_json::from_slice(catalog.manifest()).unwrap();
    let rows = manifest["packages"].as_array().unwrap();
    assert_eq!(rows.len(), catalog.entries().count());
    let mut folders: Vec<String> = std::fs::read_dir(&root)
        .unwrap()
        .map(|e| e.unwrap())
        .filter(|e| e.file_type().unwrap().is_dir())
        .map(|e| e.file_name().into_string().unwrap())
        .collect();
    folders.sort();
    let names: Vec<String> = catalog.entries().map(|e| e.identity().name.clone()).collect();
    assert_eq!(folders, names, "the bundled tree and the catalog name the same workflows");
    for (entry, row) in catalog.entries().zip(rows) {
        let identity = entry.identity();
        assert_eq!(row["name"], identity.name.as_str());
        let resolved = catalog.select_bundle_package(&root, &identity.name).unwrap();
        let selection = resolved.selection();
        assert_eq!(selection.identity(), identity);
        assert_eq!((identity.origin.as_str(), identity.source_root.as_str()), ("bundled", RELEASE_SUBJECT));
        assert_eq!(selection.snapshot().revision(), row["revision"].as_str().unwrap());
        assert_eq!(selection.snapshot().files().len(), row["files"].as_array().unwrap().len());
        assert_eq!(super::declared_name(selection.snapshot()).as_deref(), Some(identity.name.as_str()));
        assert!(entry.listing()["description"].as_str().is_some_and(|d| !d.is_empty()), "{}", identity.name);
        assert!(entry.listing()["navigation"]["category"].is_string(), "{}", identity.name);
        assert_eq!(entry.listing()["libraryExecution"], row["library_execution"]);
        assert_eq!(entry.listing()["libraryPathsNamed"], row["library_paths_named"]);
        assert!(row["library_paths_named"].is_array() && row.get("library_execution").is_some(), "{}", identity.name);
        resolved.verify_current().unwrap();
        // Resolved, not yet from this App's recorded installed root: a candidate.
        assert!(ProductionCatalog::bundled_run_admission(selection).is_err());
    }
}
// DEL-02-03, the listing aid: a kept verification answers only for the facts it verified, and only
// once they are settled; a package that changes while it is verified is not kept.
#[test]
fn a_kept_verification_answers_only_for_the_same_settled_facts() {
    use std::time::Duration;
    use super::development_catalog::{listed_or_verified, listing_keeps, SETTLED};
    let library = Library::new();
    let catalog = ProductionCatalog::load().unwrap();
    let root = library.0.join("listing-aid");
    std::fs::create_dir(&root).unwrap();
    std::fs::write(root.join("MANIFEST.json"), catalog.manifest()).unwrap();
    let package = root.join(NESTED);
    let source = catalog.select_source(NESTED);
    source.snapshot().publish_new(&package).unwrap();
    let verified = std::cell::Cell::new(0);
    let listed = |margin: Duration| listed_or_verified(&package, margin, || {
        verified.set(verified.get() + 1);
        catalog.select_bundle_package(&root, NESTED).map(|_| serde_json::json!("read"))
    });
    let read = Ok(serde_json::json!("read"));
    // With no margin asked: verified once, then answered from what was kept.
    assert_eq!(listed(Duration::ZERO), (read.clone(), false));
    assert_eq!(listed(Duration::ZERO), (read.clone(), true));
    assert_eq!(verified.get(), 1);
    assert!(listing_keeps(&package));
    // With the margin the listing uses: files written a moment ago are not settled, so each
    // listing verifies again, however many times it is asked.
    assert_eq!(listed(SETTLED), (read.clone(), false));
    assert_eq!(listed(SETTLED), (read.clone(), false));
    assert_eq!(verified.get(), 3);
    // A rewrite of the same size with its modification time put back is verified again, and refused.
    let nested = source.snapshot().files().keys().find(|path| path.contains('/')).unwrap().clone();
    let file = package.join(&nested);
    let kept = std::fs::read(&file).unwrap();
    let modified = std::fs::metadata(&file).unwrap().modified().unwrap();
    assert_eq!(listed(Duration::ZERO), (read.clone(), true));
    std::thread::sleep(Duration::from_millis(30));
    let mut bytes = kept.clone();
    bytes[0] ^= 1;
    std::fs::write(&file, &bytes).unwrap();
    std::fs::File::options().write(true).open(&file).unwrap().set_modified(modified).unwrap();
    assert_eq!((std::fs::metadata(&file).unwrap().len(), std::fs::metadata(&file).unwrap().modified().unwrap()), (kept.len() as u64, modified));
    let (refused, from_kept) = listed(Duration::ZERO);
    assert!(refused.unwrap_err().contains("revision not verified") && !from_kept);
    std::fs::write(&file, &kept).unwrap();
    assert_eq!(listed(Duration::ZERO), (read.clone(), false));
    assert_eq!(listed(Duration::ZERO), (read.clone(), true));
    // A package that changes while it is being verified: this answer is the verification's, and
    // nothing is kept from it, so the next listing verifies the changed package and refuses it.
    // (The file is written again first, with its own bytes, so that this listing has to verify.)
    std::thread::sleep(Duration::from_millis(30));
    std::fs::write(&file, &kept).unwrap();
    let during = listed_or_verified(&package, Duration::ZERO, || {
        let result = catalog.select_bundle_package(&root, NESTED).map(|_| serde_json::json!("read"));
        std::fs::write(&file, &bytes).unwrap();
        std::fs::File::options().write(true).open(&file).unwrap().set_modified(modified).unwrap();
        result
    });
    assert_eq!(during, (read.clone(), false));
    assert!(!listing_keeps(&package), "nothing is kept from a verification the package changed under");
    let (refused, from_kept) = listed(Duration::ZERO);
    assert!(refused.is_err() && !from_kept);
}
// The settled rule alone: every modification and status-change time at least the margin older
// than the start of the verification, and a path whose times cannot be placed never settled.
#[test]
fn facts_are_settled_only_when_every_time_is_older_than_the_margin() {
    use super::development_catalog::{settled, FileFacts};
    use std::time::{Duration, UNIX_EPOCH};
    let began = UNIX_EPOCH + Duration::from_secs(1000);
    let margin = Duration::from_secs(2);
    let at = |seconds: u64, nanoseconds: u32| UNIX_EPOCH + Duration::new(seconds, nanoseconds);
    let fact = |modified: Option<std::time::SystemTime>, changed: Option<(i64, i64)>| -> FileFacts {
        (PathBuf::from("/p/f"), 0, 1, modified, changed.map(|(seconds, nanoseconds)| (1, 2, seconds, nanoseconds)))
    };
    let old = fact(Some(at(998, 0)), Some((998, 0)));
    assert!(settled(&[old.clone()], began, margin), "exactly the margin older");
    for (why, unsettled) in [
        ("modified inside the margin", fact(Some(at(998, 1)), Some((990, 0)))),
        ("status changed inside the margin", fact(Some(at(990, 0)), Some((998, 1)))),
        ("status changed in the same second as the verification", fact(Some(at(990, 0)), Some((1000, 0)))),
        ("status changed after the verification began", fact(Some(at(990, 0)), Some((1001, 0)))),
        ("no modification time", fact(None, Some((990, 0)))),
        ("a status-change time that cannot be placed", fact(Some(at(990, 0)), Some((-1, 0)))),
    ] {
        assert!(!settled(&[unsettled.clone()], began, margin), "{why}");
        assert!(!settled(&[old.clone(), unsettled], began, margin), "{why}: one unsettled path is enough");
    }
    // Where the platform gives no status-change time, the modification time alone.
    assert!(settled(&[fact(Some(at(998, 0)), None)], began, margin));
    assert!(!settled(&[fact(Some(at(999, 0)), None)], began, margin));
    // A margin reaching before the clock's own beginning settles nothing.
    assert!(!settled(&[old], UNIX_EPOCH, Duration::MAX));
}
// A package the manifest names is admitted only with exactly its own files and
// bytes: an added file, a changed byte in a subfolder, a missing file, and
// another bundled workflow's bytes under its name are each refused.
#[test]
fn bundled_package_with_other_bytes_is_refused_under_any_bundled_name() {
    let library = Library::new();
    let catalog = ProductionCatalog::load().unwrap();
    let root = library.0.join("bundle-workflows");
    std::fs::create_dir(&root).unwrap();
    std::fs::write(root.join("MANIFEST.json"), catalog.manifest()).unwrap();
    let package = root.join(NESTED);
    let source = catalog.select_source(NESTED);
    assert!(source.snapshot().files().keys().any(|path| path.contains('/')), "a nested package");
    source.snapshot().publish_new(&package).unwrap();
    let resolved = catalog.select_bundle_package(&root, NESTED).unwrap();
    resolved.verify_current().unwrap();
    let nested = source.snapshot().files().keys().find(|path| path.contains('/')).unwrap().clone();
    let kept = std::fs::read(package.join(&nested)).unwrap();
    for change in ["added", "changed", "removed"] {
        match change {
            "added" => std::fs::write(package.join("extra.md"), b"extra").unwrap(),
            "changed" => {
                let mut bytes = kept.clone();
                bytes[0] ^= 1;
                std::fs::write(package.join(&nested), bytes).unwrap()
            }
            _ => std::fs::remove_file(package.join(&nested)).unwrap(),
        }
        assert!(resolved.verify_current().is_err(), "{change}");
        let error = catalog.select_bundle_package(&root, NESTED).err().unwrap();
        assert!(error.contains("revision not verified"), "{change}: {error}");
        assert!(catalog.listed_admission(&root, NESTED).is_err(), "{change}");
        let _ = std::fs::remove_file(package.join("extra.md"));
        std::fs::write(package.join(&nested), &kept).unwrap();
        resolved.verify_current().unwrap();
        catalog.listed_admission(&root, NESTED).unwrap();
    }
    // Another bundled workflow's exact bytes under this name are not this workflow.
    catalog.select_source(NAME).snapshot().publish_new(&root.join("create-workflow")).unwrap();
    let error = catalog.select_bundle_package(&root, "create-workflow").err().unwrap();
    assert!(error.contains("revision not verified"), "{error}");
    // A folder the manifest does not name is not in the catalog, whatever it holds.
    source.snapshot().publish_new(&root.join("not-in-the-manifest")).unwrap();
    let error = catalog.select_bundle_package(&root, "not-in-the-manifest").err().unwrap();
    assert!(error.contains("name not in production catalog"), "{error}");
}
// The compiled manifest is admitted only in the form the generator writes.
#[test]
fn manifest_in_another_form_is_not_admitted() {
    let catalog = ProductionCatalog::load().unwrap();
    let manifest: serde_json::Value = serde_json::from_slice(catalog.manifest()).unwrap();
    let parse = |value: &serde_json::Value| ProductionCatalog::parse(value.to_string().as_bytes()).map(|_| ());
    parse(&manifest).unwrap();
    let cases: [(&str, fn(&mut serde_json::Value)); 7] = [
        ("release subject", |m| m["release_subject"] = "chirality-library:another".into()),
        ("shipped history claimed", |m| m["historical_shipped_revisions"] = serde_json::json!(["r"])),
        ("no packages", |m| m["packages"] = serde_json::json!([])),
        ("name twice", |m| { let first = m["packages"][0].clone(); m["packages"].as_array_mut().unwrap().push(first) }),
        ("revision method", |m| m["packages"][0]["revision_method"] = "another/v1".into()),
        ("revision form", |m| m["packages"][0]["revision"] = "short".into()),
        ("name form", |m| { m["packages"][0]["name"] = "../escape".into(); m["packages"][0]["source_path"] = "workflows/../escape".into() }),
    ];
    for (case, change) in cases {
        let mut changed = manifest.clone();
        change(&mut changed);
        assert!(parse(&changed).is_err(), "{case}");
    }
}
#[test]
fn holding_copy_preserves_tuple_and_refuses_changed_or_additional_bytes() {
    let library = Library::new();
    library.populate();
    let catalog = ProductionCatalog::load().unwrap();
    let held = catalog
        .recognize_holding_copy(&library.0, NAME)
        .unwrap();
    assert_eq!(held.selection().identity(), catalog.identity(NAME).unwrap());
    assert_eq!(held.package_path(), library.package());
    held.verify_current().unwrap();
    std::fs::write(library.package().join("extra.txt"), "changed").unwrap();
    assert!(held.verify_current().is_err());
    assert!(catalog
        .recognize_holding_copy(&library.0, NAME)
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
        .recognize_holding_copy(&library.0, NAME)
        .unwrap();
    let ledger = library.0.join(".chirality/workflow-registry.jsonl");
    std::fs::write(&ledger, "{broken}\n").unwrap();
    assert!(held.verify_current().is_err());
    assert!(catalog
        .recognize_holding_copy(&library.0, NAME)
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
            NAME
        )
        .is_err());
    let library = Library::new();
    std::fs::create_dir_all(library.0.join(".chirality/workflow-drafts")).unwrap();
    catalog
        .select_source(NAME)
        .snapshot()
        .publish_new(
            &library
                .0
                .join(".chirality/workflow-drafts")
                .join(NAME),
        )
        .unwrap();
    assert!(catalog
        .recognize_holding_copy(&library.0, NAME)
        .is_err());
    #[cfg(unix)]
    {
        std::os::unix::fs::symlink(
            library
                .0
                .join(".chirality/workflow-drafts")
                .join(NAME),
            library.package(),
        )
        .unwrap();
        assert!(catalog
            .recognize_holding_copy(&library.0, NAME)
            .is_err());
    }
}

#[test]
fn existing_registered_slot_refuses_even_byte_equal_copy_and_rechecks_selection() {
    let library = Library::new();
    library.populate();
    let catalog = ProductionCatalog::load().unwrap();
    let held = catalog
        .recognize_holding_copy(&library.0, NAME)
        .unwrap();
    let selected = held.selection().clone();
    let identity = serde_json::json!({"kind":"workflow","origin":"project","source_root":"fixture","name":NAME,"revision":"existing","revision_method":"fixture-method"});
    let line = serde_json::json!({"record_kind":"library_entry","ledger_seq":1,"outcome":"registered","identity":identity,"sequence":1,"prior_revision":null,"disposition":"new workflow","reviewed_draft":{"draft":{"draft_location":"project","draft_root":"fixture","name":NAME},"content":{"method":"fixture-method","value":"existing"}},"act":{"record_id":"rec:fixture:1","capture_evidence":"cap:fixture:1"},"store_path":"workflow-revisions/coordinated-knowledge-work/existing/coordinated-knowledge-work","written_at":"fixture-time","evidence_limits":["synthetic registry observation; no human act"]});
    super::wr_validate("library_entry", &line).unwrap();
    std::fs::write(
        library.0.join(".chirality/workflow-registry.jsonl"),
        format!("{}\n", line),
    )
    .unwrap();
    let error = catalog
        .recognize_holding_copy(&library.0, NAME)
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
    let package = root.join(NAME);
    catalog
        .select_source(NAME)
        .snapshot()
        .publish_new(&package)
        .unwrap();
    assert!(catalog
        .select_bundle_package(&root, NAME)
        .is_err());
    std::fs::write(root.join("MANIFEST.json"), catalog.manifest()).unwrap();
    let resolved = catalog
        .select_bundle_package(&root, NAME)
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

#[cfg(unix)]
fn p2_fifo_refuses_without_blocking(
    path: &std::path::Path,
    check: impl FnOnce() -> Result<(), String> + Send + 'static,
) {
    use std::os::unix::{ffi::OsStrExt, fs::OpenOptionsExt};
    let name = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    // The anchor bounds even a regression: a blocking read is released when the
    // deadline drops this writer. A healthy reader refuses before that happens.
    let anchor = std::fs::OpenOptions::new()
        .read(true)
        .write(true)
        .custom_flags(libc::O_NONBLOCK)
        .open(path)
        .unwrap();
    let (tx, rx) = std::sync::mpsc::channel();
    let thread = std::thread::spawn(move || {
        tx.send(check()).unwrap();
    });
    let answer = rx.recv_timeout(std::time::Duration::from_secs(2));
    drop(anchor);
    thread.join().unwrap();
    let error = answer
        .expect("FIFO read blocked until its writer was released")
        .unwrap_err();
    assert!(error.contains("not a regular file"), "{error}");
}
#[cfg(unix)]
#[test]
fn p2_fifo_manifest_is_refused_at_selection_and_use_without_blocking() {
    let library = Library::new();
    let catalog = ProductionCatalog::load().unwrap();
    let root = library.0.join("bundle");
    std::fs::create_dir(&root).unwrap();
    let path = root.join("MANIFEST.json");
    std::fs::write(&path, catalog.manifest()).unwrap();
    catalog
        .select_source(NAME)
        .snapshot()
        .publish_new(&root.join(NAME))
        .unwrap();
    let selected = catalog
        .select_bundle_package(&root, NAME)
        .unwrap();
    std::fs::remove_file(&path).unwrap();
    p2_fifo_refuses_without_blocking(&path, move || {
        let error = ProductionCatalog::load()?
            .select_bundle_package(&root, NAME)
            .err()
            .unwrap();
        assert!(error.contains("not a regular file"), "{error}");
        selected.verify_current()
    });
}
#[cfg(unix)]
#[test]
fn p2_fifo_registry_is_refused_at_recognition_and_use_without_blocking() {
    let library = Library::new();
    library.populate();
    let catalog = ProductionCatalog::load().unwrap();
    let selected = catalog
        .recognize_holding_copy(&library.0, NAME)
        .unwrap();
    let path = library.0.join(".chirality/workflow-registry.jsonl");
    let root = library.0.clone();
    p2_fifo_refuses_without_blocking(&path, move || {
        let error = ProductionCatalog::load()?
            .recognize_holding_copy(&root, NAME)
            .err()
            .unwrap();
        assert!(error.contains("not a regular file"), "{error}");
        selected.verify_current()
    });
}

// BUNDLED-RUN-01 (WR LS-5): only the selected subject, resolved from a bundle
// root, is admitted; the embedded copy and a library holding copy are not.
#[test]
fn bundled_run_admission_is_closed_to_the_selected_installed_subject() {
    let catalog = ProductionCatalog::load().unwrap();
    assert_eq!(
        crate::util::sha256_hex(catalog.manifest()),
        SELECTED_BUNDLED_MANIFEST_SHA256,
        "the compiled manifest is the selected subject"
    );
    let embedded = catalog.select_source(NAME);
    assert!(ProductionCatalog::bundled_run_admission(&embedded).is_err());
    assert_eq!(embedded.admission().standing(), PRODUCTION_STANDING);

    let library = Library::new();
    library.populate();
    let held = catalog
        .recognize_holding_copy(&library.0, NAME)
        .unwrap();
    assert!(ProductionCatalog::bundled_run_admission(held.selection()).is_err());
    assert_eq!(held.selection().admission().standing(), PRODUCTION_STANDING);

    let root = library.0.join("bundle-workflows");
    std::fs::create_dir(&root).unwrap();
    std::fs::write(root.join("MANIFEST.json"), catalog.manifest()).unwrap();
    embedded
        .snapshot()
        .publish_new(&root.join(NAME))
        .unwrap();
    let resolved = catalog
        .select_bundle_package(&root, NAME)
        .unwrap();
    let unknown = ProductionCatalog::bundled_run_admission(resolved.selection()).unwrap_err();
    assert!(unknown.contains("not known"), "{unknown}");
    super::development_catalog::record_installed_root(library.0.join("elsewhere")).unwrap();
    let elsewhere = ProductionCatalog::bundled_run_admission(resolved.selection()).unwrap_err();
    assert!(elsewhere.contains("not resolved from this App's installed resources"), "{elsewhere}");
    assert!(super::development_catalog::record_installed_root(root.clone()).is_err(), "no rebinding");
    assert_eq!(resolved.selection().admission().standing(), BUNDLED_STANDING);
    // A separate thread records this App's actual root; there the same
    // installed resolution is admitted.
    let selection = resolved.selection().clone();
    let expected = root.clone();
    std::thread::spawn(move || {
        super::development_catalog::record_installed_root(expected.clone()).unwrap();
        assert_eq!(
            ProductionCatalog::bundled_run_admission(&selection).unwrap(),
            expected.as_path()
        );
    })
    .join()
    .unwrap();
    assert!(
        catalog.select_bundle_package(&root, "other-name").is_err(),
        "unknown name is not in the catalog"
    );
}
