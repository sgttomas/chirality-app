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
        // The real location: the system's temporary folder is reached through a link, and the reader
        // follows no link above a package.
        let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(format!(
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

// The reader's boundary above a package folder (DEL-02-01, Revision). On macOS the package folder is opened
// with the system's whole-path no-link flag, so a symbolic link at any component from the filesystem root to
// the folder is refused by the open itself. Invented packages in the real temporary folder only.
mod package_root {
    use super::*;
    use std::os::unix::fs::{symlink, PermissionsExt};
    use std::path::{Path, PathBuf};
    const LINK: &str = workflow_workspace::LINK_IN_PACKAGE_PATH;

    struct Scratch(PathBuf);
    impl Scratch {
        fn new() -> Self {
            let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(util::opaque_id("package-root-").unwrap());
            std::fs::create_dir(&root).unwrap();
            Self(root)
        }
        /// A package folder at `relative`, with one file.
        fn package(&self, relative: &str) -> PathBuf {
            let package = self.0.join(relative);
            std::fs::create_dir_all(&package).unwrap();
            std::fs::write(package.join("WORKFLOW.md"), b"---\nname: invented\ndescription: An invented workflow.\n---\nInvented text.\n").unwrap();
            package
        }
    }
    impl Drop for Scratch {
        fn drop(&mut self) {
            // A test here removes read permission from a folder; give it back before removing the tree.
            fn open_up(at: &Path) {
                if std::fs::symlink_metadata(at).is_ok_and(|m| m.is_dir()) {
                    let _ = std::fs::set_permissions(at, std::fs::Permissions::from_mode(0o755));
                    for entry in std::fs::read_dir(at).into_iter().flatten().flatten() { open_up(&entry.path()); }
                }
            }
            open_up(&self.0);
            let _ = std::fs::remove_dir_all(&self.0);
        }
    }
    fn refused_for_a_link(path: &Path, link: &Path) {
        // An open without the whole-path flag reads through the link: this is what the refusal is not.
        assert!(std::fs::read(path.join("WORKFLOW.md")).is_ok(), "an ordinary read follows the link, so the files are reachable");
        let error = Snapshot::capture(path).expect_err("the reader must refuse a link above the package folder; if this read succeeded, the system ignored O_NOFOLLOW_ANY here");
        assert!(error.contains(LINK), "the refusal is the reader's own, for a link in the path: {error}");
        assert!(error.contains(&format!("({} is a link)", link.display())), "the link found on looking is named: {error}");
    }

    #[cfg(target_os = "macos")]
    #[test]
    fn a_link_at_any_folder_above_a_package_is_refused_by_the_open_itself() {
        let s = Scratch::new();
        let real = s.package("real/library/package");
        assert_eq!(Snapshot::capture(&real).unwrap().files().len(), 1, "by its real location the package is read");
        // The folder two above the package is a link.
        symlink(s.0.join("real"), s.0.join("linked")).unwrap();
        refused_for_a_link(&s.0.join("linked/library/package"), &s.0.join("linked"));
        // The folder directly above the package is a link.
        symlink(s.0.join("real/library"), s.0.join("real/library-link")).unwrap();
        refused_for_a_link(&s.0.join("real/library-link/package"), &s.0.join("real/library-link"));
        // Two links on the way: the first one found from the root is the one named.
        refused_for_a_link(&s.0.join("linked/library-link/package"), &s.0.join("linked"));
        // The package folder itself is a link: refused, as before this change.
        symlink(&real, s.0.join("real/library/package-link")).unwrap();
        assert!(Snapshot::capture(&s.0.join("real/library/package-link")).unwrap_err().starts_with("non-regular package root"));
        // The system's own links: the temporary folder spelled through one is refused; spelled by its real location it is read.
        let spelled = std::env::temp_dir().join(s.0.file_name().unwrap()).join("real/library/package");
        if spelled != real {
            let error = Snapshot::capture(&spelled).unwrap_err();
            assert!(error.contains(LINK), "{error}");
        }
    }

    // Within one capture, after the open: the listing and every entry come from the opened folder itself.
    // The path is swapped under the reader (the folder moved aside and another put in its place, then a link
    // put there) and what is read is still the folder that was opened.
    #[test]
    fn after_the_open_a_capture_reads_the_opened_folder_whatever_the_path_then_names() {
        let s = Scratch::new();
        let package = s.package("library/package");
        std::fs::create_dir(package.join("notes")).unwrap();
        std::fs::write(package.join("notes/first.md"), b"first").unwrap();
        let opened = workflow_workspace::open_package_root(&package).unwrap();
        // Another folder now stands at the path, with other files.
        std::fs::rename(s.0.join("library"), s.0.join("moved")).unwrap();
        let other = s.package("library/package");
        std::fs::write(other.join("WORKFLOW.md"), b"other text").unwrap();
        std::fs::write(other.join("other-only.md"), b"other").unwrap();
        let read = |dir: &std::fs::File| {
            let (mut files, mut budget) = (std::collections::BTreeMap::new(), (0usize, 0u64));
            workflow_workspace::walk_fd(dir, &package, "", &mut files, &mut budget).map(|()| files)
        };
        let files = read(&opened).unwrap();
        assert_eq!(files.keys().map(String::as_str).collect::<Vec<_>>(), ["WORKFLOW.md", "notes/first.md"], "the opened folder's own listing, not the path's");
        assert!(files["WORKFLOW.md"].starts_with(b"---\nname: invented"), "the opened folder's own bytes");
        // The folder above becomes a link to yet another place: the same.
        std::fs::remove_dir_all(s.0.join("library")).unwrap();
        symlink(s.0.join("moved"), s.0.join("library")).unwrap();
        assert_eq!(read(&opened).unwrap(), files);
        // And with nothing at the path at all.
        std::fs::remove_file(s.0.join("library")).unwrap();
        assert_eq!(read(&opened).unwrap(), files);
        assert_eq!(workflow_workspace::names_in(&opened).unwrap().len(), 2, "listed through the descriptor, twice over");
    }

    #[test]
    fn what_a_plain_open_reaches_without_a_link_is_still_read() {
        let s = Scratch::new();
        // A folder above the package that may be passed through but not listed.
        let package = s.package("closed/library/package");
        std::fs::set_permissions(s.0.join("closed"), std::fs::Permissions::from_mode(0o311)).unwrap();
        assert!(std::fs::read_dir(s.0.join("closed")).is_err(), "the folder above cannot be listed");
        assert_eq!(Snapshot::capture(&package).unwrap().files().len(), 1, "search permission above the package is enough, as for any open");
        // Folder names the system allows above a package.
        for name in ["with space", "back\\slash", "new\nline", "carriage\rreturn", "…unicode é"] {
            let package = s.package(&format!("{name}/package"));
            assert_eq!(Snapshot::capture(&package).unwrap().files().len(), 1, "{name:?}");
        }
    }

    #[test]
    fn an_absent_folder_and_a_non_regular_entry_are_said_as_before() {
        let s = Scratch::new();
        let absent = Snapshot::capture(&s.0.join("library/absent")).unwrap_err();
        assert!(!absent.contains(LINK) && !absent.starts_with("non-regular package root"), "an absent folder is not called a link or a non-regular root: {absent}");
        let package = s.package("library/package");
        let fifo = std::ffi::CString::new(package.join("pipe").to_str().unwrap()).unwrap();
        assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
        assert!(Snapshot::capture(&package).unwrap_err().starts_with("HY-3: non-regular entry"), "a FIFO is refused without blocking");
        std::fs::remove_file(package.join("pipe")).unwrap();
        symlink(package.join("WORKFLOW.md"), package.join("linked.md")).unwrap();
        assert!(Snapshot::capture(&package).unwrap_err().starts_with("HY-3: non-regular entry"), "a link inside the package is refused");
        let file = s.0.join("library/a-file");
        std::fs::write(&file, b"not a folder").unwrap();
        assert!(Snapshot::capture(&file).unwrap_err().starts_with("non-regular package root"), "a file where a package folder should be");
    }

    #[test]
    fn a_path_that_is_not_fixed_is_refused_and_never_resolved() {
        let s = Scratch::new();
        let package = s.package("library/package");
        s.package("library/other");
        // Each of these names the same folder to the system; none is read.
        for (path, why) in [
            (s.0.join("library/other/../package"), "`.` or `..`"),
            (s.0.join("library/./package"), "`.` or `..`"),
            (s.0.join("library/package/."), "`.` or `..`"),
            (PathBuf::from(format!("{}/library/package/..", s.0.display())), "`.` or `..`"),
            (PathBuf::from("library/package"), "fixed absolute path"),
            (PathBuf::from("./library/package"), "fixed absolute path"),
        ] {
            let error = Snapshot::capture(&path).unwrap_err();
            assert!(error.contains(why), "{}: {error}", path.display());
        }
        assert_eq!(Snapshot::capture(&package).unwrap().files().len(), 1);
        // A name that only contains dots is a name, not a component to resolve.
        assert_eq!(Snapshot::capture(&s.package("library/..name/...")).unwrap().files().len(), 1);
    }

    #[cfg(target_os = "macos")]
    #[test]
    fn a_development_holding_copy_reached_through_a_link_is_refused_in_words() {
        let copy = Copy::new();
        copy.populate();
        let catalog = DevelopmentCatalog::load().unwrap();
        catalog.recognize_holding_copy(&copy.package()).expect("by its real location the holding copy is recognised");
        let link = copy.0.with_extension("link");
        symlink(&copy.0, &link).unwrap();
        let error = catalog.recognize_holding_copy(&link.join(NAME)).err().expect("a holding copy picked through a linked folder is refused");
        let _ = std::fs::remove_file(&link);
        assert!(error.contains(LINK) && error.contains(&format!("({} is a link)", link.display())), "{error}");
        assert!(error.contains("Choose the holding copy by the real location of its folder"), "{error}");
    }
}

