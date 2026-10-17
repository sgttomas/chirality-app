use super::*;
use crate::records_store::{self, Placement, Store};
use serde_json::json;
use std::os::unix::fs::PermissionsExt;

struct Fixture {
    root: PathBuf,
    project: PathBuf,
    bag: PathBuf,
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir().join(crate::util::opaque_id("package-custody-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let root = std::fs::canonicalize(root).unwrap();
        let project = root.join("project");
        let store = root.join("store");
        for path in [&project, &store] {
            std::fs::create_dir(path).unwrap();
        }
        records_store::use_store_for_test(Some(Ok(Store {
            root: store.clone(),
            placement: Placement::Test,
            limits: vec![],
        })));
        crate::records::append_project(&project, Some("run:package-fixture"), "writer:package-fixture", "evidence_limit", &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented package custody fixture"})).unwrap();
        let bag = root.join("bag");
        Self { root, project, bag }
    }
    fn dir(&self) -> PathBuf {
        records_store::home(&self.project)
            .unwrap()
            .attachment
            .dir
            .unwrap()
    }
    fn export(&self) {
        crate::records_export::export(&self.project, &self.bag).unwrap();
    }
    fn stage(&self) -> PathBuf {
        self.root.join("stage")
    }
    fn add(&self, relative: &str, bytes: &[u8]) {
        let path = self.dir().join(relative);
        std::fs::create_dir_all(path.parent().unwrap()).unwrap();
        std::fs::write(path, bytes).unwrap();
    }
    fn rehash(&self) {
        let data = custody(&self.bag).unwrap();
        let encoded = |path: &str| {
            path.replace('%', "%25")
                .replace('\r', "%0D")
                .replace('\n', "%0A")
        };
        let mut manifest = String::new();
        for (path, member) in &data.members {
            if path.starts_with("data/") {
                manifest.push_str(&format!("{}  {}\n", member.sha256, encoded(path)));
            }
        }
        std::fs::write(self.bag.join("manifest-sha256.txt"), manifest).unwrap();
        self.rehash_tags();
    }
    fn rehash_tags(&self) {
        let mut manifest = String::new();
        for name in TAGS {
            if self.bag.join(name).exists() {
                manifest.push_str(&format!(
                    "{}  {name}\n",
                    crate::util::sha256_hex(&std::fs::read(self.bag.join(name)).unwrap())
                ));
            }
        }
        std::fs::write(self.bag.join("tagmanifest-sha256.txt"), manifest).unwrap();
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        AFTER_CENSUS.with(|h| h.borrow_mut().take());
        DURING_READ.with(|h| h.borrow_mut().take());
        BEFORE_CONTROL_REPLACE.with(|h| h.borrow_mut().take());
        STOP_RESTORE.with(|flag| flag.set(false));
        FAIL_PUBLICATION_SYNC.with(|flag| flag.set(false));
        fail_control_before_publish_for_test(None);
        records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

#[test]
fn records_package_exact_private_snapshot_keeps_source_and_all_evidence_bytes() {
    let f = Fixture::new();
    f.add(
        "connectors/.interrupted.tmp",
        b"interrupted\0publication\xff",
    );
    f.add("connectors/retained.lock", b"ordinary retained evidence");
    f.add("connectors/name %\r\n.json", b"opaque bytes");
    std::fs::create_dir_all(f.dir().join("connectors/empty")).unwrap();
    let log = crate::storage::project_log(
        &f.project,
        Some("run:package-fixture"),
        "writer:package-fixture",
    )
    .unwrap();
    let specs = (0..2).map(|i| crate::records::Spec { kind: "evidence_limit", recorder: &crate::records::APP_WRITER,
        body: json!({"label":"unresolvable reference","subjectRef":format!("invented grouped fixture {i}")}),
        id: crate::util::opaque_id("rec:app:").unwrap(), observed_at: None }).collect();
    crate::records::append_group(
        &log,
        specs,
        Some("run:package-fixture"),
        crate::records::RecordSet::Complete,
    )
    .unwrap();
    f.export();
    let original = custody(&f.bag).unwrap();
    let snapshot = snapshot(&f.bag, &f.stage()).unwrap();
    assert_eq!(snapshot.root(), f.stage());
    assert_eq!(
        snapshot.project_id(),
        snapshot.project_record()["projectId"]
    );
    assert_eq!(
        snapshot.administration()["projectId"],
        snapshot.project_id()
    );
    assert_eq!(
        snapshot.identity(),
        original.members["tagmanifest-sha256.txt"].sha256
    );
    assert_eq!(snapshot.payload()["connectors/.interrupted.tmp"].bytes, 24);
    let staged = custody(snapshot.root()).unwrap();
    assert_eq!(original.members, staged.members);
    assert_eq!(
        original.census.keys().collect::<Vec<_>>(),
        staged.census.keys().collect::<Vec<_>>()
    );
    for (path, stamp) in &staged.census {
        assert_eq!(
            stamp.mode & 0o777,
            if stamp.directory() { 0o700 } else { 0o600 },
            "{path}"
        );
        if stamp.regular() {
            assert_eq!(stamp.links, 1);
        }
    }
    snapshot.verify_unchanged().unwrap();
    snapshot.source_unchanged().unwrap();
    original.unchanged().unwrap();
    assert_eq!(
        original.census,
        scan(&original.directory).unwrap(),
        "source modes and first-observed stamps unchanged"
    );
}

#[test]
fn records_package_recovery_reopens_stage_without_original_source_claim() {
    let f = Fixture::new();
    f.export();
    let snapshot = snapshot(&f.bag, &f.stage()).unwrap();
    let identity = snapshot.identity().to_owned();
    std::fs::rename(&f.bag, f.root.join("source-moved")).unwrap();
    assert!(snapshot.source_unchanged().is_err());
    snapshot.verify_unchanged().unwrap();
    let recovered = inspect(&f.stage()).unwrap();
    assert_eq!(recovered.identity(), identity);
    recovered.source_unchanged().unwrap();
    recovered.verify_unchanged().unwrap();
}

#[test]
fn records_package_never_overwrites_destination_or_writes_inside_source() {
    let f = Fixture::new();
    f.export();
    std::fs::create_dir(f.stage()).unwrap();
    std::fs::write(f.stage().join("retained"), b"untouched").unwrap();
    assert!(snapshot(&f.bag, &f.stage())
        .unwrap_err()
        .contains("nothing overwritten"));
    assert_eq!(
        std::fs::read(f.stage().join("retained")).unwrap(),
        b"untouched"
    );
    assert!(snapshot(&f.bag, &f.bag.join("stage"))
        .unwrap_err()
        .contains("outside"));
    assert!(!f.bag.join("stage").exists());
}

#[test]
fn records_package_refuses_leaf_and_ancestor_links_hardlinks_and_fifos() {
    use std::os::unix::ffi::OsStrExt;
    for variant in ["symlink", "ancestor", "hardlink", "fifo"] {
        let f = Fixture::new();
        f.export();
        let path = f.bag.join("verify.py");
        let bytes = std::fs::read(&path).unwrap();
        let elsewhere = f.root.join("external");
        std::fs::write(&elsewhere, &bytes).unwrap();
        if variant == "ancestor" {
            let alias = f.root.join("alias");
            std::os::unix::fs::symlink(&f.bag, &alias).unwrap();
            assert!(snapshot(&alias, &f.stage()).is_err());
            continue;
        }
        std::fs::remove_file(&path).unwrap();
        match variant {
            "symlink" => std::os::unix::fs::symlink(&elsewhere, &path).unwrap(),
            "hardlink" => std::fs::hard_link(&elsewhere, &path).unwrap(),
            "fifo" => {
                let name = CString::new(path.as_os_str().as_bytes()).unwrap();
                assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
            }
            _ => unreachable!(),
        }
        let started = std::time::Instant::now();
        assert!(snapshot(&f.bag, &f.stage()).is_err(), "{variant}");
        assert!(started.elapsed() < std::time::Duration::from_secs(2));
        assert_eq!(std::fs::read(&elsewhere).unwrap(), bytes);
        assert!(!f.stage().exists());
    }
}

#[test]
fn records_package_refuses_unsafe_manifest_paths_and_duplicate_aliases() {
    for member in [
        "../outside",
        "/absolute",
        "data/../outside",
        "data//project.json",
        "data/./project.json",
        "data/%2Fproject.json",
        "data/project.json%00",
    ] {
        let f = Fixture::new();
        f.export();
        let manifest = f.bag.join("manifest-sha256.txt");
        let original = std::fs::read_to_string(&manifest).unwrap();
        let line = format!("{}  {member}\n", "0".repeat(64));
        std::fs::write(&manifest, original + &line).unwrap();
        f.rehash_tags();
        assert!(snapshot(&f.bag, &f.stage()).is_err(), "{member}");
    }
    let f = Fixture::new();
    f.export();
    let path = f.bag.join("manifest-sha256.txt");
    let original = std::fs::read_to_string(&path).unwrap();
    std::fs::write(
        &path,
        format!("{original}{}\n", original.lines().next().unwrap()),
    )
    .unwrap();
    f.rehash_tags();
    assert!(snapshot(&f.bag, &f.stage())
        .unwrap_err()
        .contains("duplicate"));
}

#[test]
fn records_package_refuses_changed_project_and_bag_info_identity_or_legacy_profile() {
    for variant in [
        "format",
        "version",
        "identity",
        "bag-info",
        "duplicate-external",
        "admin-envelope",
        "legacy",
    ] {
        let f = Fixture::new();
        f.export();
        match variant {
            "format" | "version" | "identity" => {
                let path = f.bag.join("data/project.json");
                let mut project: Value =
                    serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
                project[match variant {
                    "format" => "format",
                    "version" => "formatVersion",
                    _ => "projectId",
                }] = json!(if variant == "identity" {
                    ""
                } else {
                    "unsupported"
                });
                std::fs::write(path, serde_json::to_vec(&project).unwrap()).unwrap();
                f.rehash();
            }
            "bag-info" => {
                std::fs::write(
                    f.bag.join("bag-info.txt"),
                    "External-Identifier: different-project\n",
                )
                .unwrap();
                f.rehash_tags();
            }
            "duplicate-external" => {
                let path = f.bag.join("bag-info.txt");
                let info = std::fs::read_to_string(&path).unwrap();
                std::fs::write(path, format!("{info}{}\n", info.lines().next().unwrap())).unwrap();
                f.rehash_tags();
            }
            "admin-envelope" => {
                let path = f.bag.join(ADMIN);
                let mut admin: Value =
                    serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
                admin["projectKey"] = json!("0".repeat(64));
                std::fs::write(path, serde_json::to_vec(&admin).unwrap()).unwrap();
                f.rehash_tags();
            }
            "legacy" => {
                std::fs::remove_file(f.bag.join(ADMIN)).unwrap();
                f.rehash_tags();
                assert!(
                    crate::records_export::verify(&f.bag).is_ok(),
                    "legacy byte verification remains available"
                );
            }
            _ => unreachable!(),
        }
        assert!(snapshot(&f.bag, &f.stage()).is_err(), "{variant}");
    }
}

#[test]
fn records_package_refuses_active_controls_but_retains_malformed_logs_and_unknown_evidence() {
    for (control, directory) in [
        (".writer.lock", false),
        ("captures/.capture.lock", false),
        (".writer.lock", true),
    ] {
        let f = Fixture::new();
        f.export();
        let path = f.bag.join("data").join(control);
        std::fs::create_dir_all(path.parent().unwrap()).unwrap();
        if directory {
            std::fs::create_dir(path).unwrap();
        } else {
            std::fs::write(path, b"forged owning control").unwrap();
        }
        f.rehash();
        assert!(snapshot(&f.bag, &f.stage())
            .unwrap_err()
            .contains("active owning control"));
    }
    let f = Fixture::new();
    // A malformed source log is preserved evidence, not repaired or promoted.
    f.add("runs/malformed/writer.jsonl", b"{broken}\npartial");
    f.add("connectors/.unknown.tmp", b"opaque retained bytes");
    f.export();
    let snapshot = snapshot(&f.bag, &f.stage()).unwrap();
    assert_eq!(
        std::fs::read(snapshot.root().join("data/runs/malformed/writer.jsonl")).unwrap(),
        b"{broken}\npartial"
    );
    assert!(snapshot.payload().contains_key("connectors/.unknown.tmp"));
}

#[test]
fn records_package_source_replacement_mutation_and_late_inventory_are_refused() {
    for variant in ["file", "directory", "root", "late", "during-read"] {
        let f = Fixture::new();
        f.add("connectors/evidence", b"original evidence");
        f.export();
        let bag = f.bag.clone();
        let external = f.root.join("external");
        std::fs::create_dir(&external).unwrap();
        std::fs::write(external.join("evidence"), b"outside evidence").unwrap();
        AFTER_CENSUS.with(|h| {
            *h.borrow_mut() = Some(Box::new(move || match variant {
                "file" => {
                    let path = bag.join("data/project.json");
                    std::fs::remove_file(&path).unwrap();
                    std::os::unix::fs::symlink(external.join("evidence"), path).unwrap();
                }
                "directory" => {
                    std::fs::rename(bag.join("data/connectors"), bag.join("data/old-connectors"))
                        .unwrap();
                    std::os::unix::fs::symlink(&external, bag.join("data/connectors")).unwrap();
                }
                "root" => {
                    std::fs::rename(&bag, bag.with_file_name("original-bag")).unwrap();
                    std::os::unix::fs::symlink(&external, &bag).unwrap();
                }
                "late" => {
                    std::fs::create_dir(bag.join("empty-late-directory")).unwrap();
                }
                "during-read" => {
                    DURING_READ.with(|h| {
                        *h.borrow_mut() = Some(Box::new(move |relative| {
                            assert_eq!(relative, "bag-info.txt");
                            std::fs::write(bag.join(relative), b"changed while reading").unwrap();
                        }))
                    });
                }
                _ => unreachable!(),
            }))
        });
        assert!(snapshot(&f.bag, &f.stage()).is_err(), "{variant}");
        assert_eq!(
            std::fs::read(f.root.join("external/evidence")).unwrap(),
            b"outside evidence"
        );
    }
}

#[test]
fn records_package_owned_stage_changes_and_destination_alias_collisions_are_refused() {
    let f = Fixture::new();
    f.export();
    let held = snapshot(&f.bag, &f.stage()).unwrap();
    std::fs::write(
        f.stage().join("data/project.json"),
        b"different stage bytes",
    )
    .unwrap();
    assert!(held.verify_unchanged().is_err());
    assert!(inspect(&f.stage()).is_err());
    held.source_unchanged().unwrap();

    let f = Fixture::new();
    f.export();
    let stage = f.stage();
    AFTER_CENSUS.with(|h| {
        *h.borrow_mut() = Some(Box::new(move || {
            // O_EXCL/mkdirat expose target filesystem aliases instead of merging
            // two differently spelled source names into a single target member.
            std::fs::write(stage.join("bag-info.txt"), b"existing target member").unwrap();
        }))
    });
    assert!(snapshot(&f.bag, &f.stage())
        .unwrap_err()
        .contains("aliased name"));
    assert_eq!(
        std::fs::read(f.stage().join("bag-info.txt")).unwrap(),
        b"existing target member"
    );
}

#[test]
fn records_package_inspect_refuses_an_existing_stage_with_public_permissions() {
    let f = Fixture::new();
    f.export();
    snapshot(&f.bag, &f.stage()).unwrap();
    let path = f.stage().join("verify.py");
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o644)).unwrap();
    assert!(inspect(&f.stage()).unwrap_err().contains("not private"));
}

#[test]
fn records_package_payload_inventory_is_complete_and_omits_only_plain_owning_controls() {
    let f = Fixture::new();
    f.export();
    let snapshot = snapshot(&f.bag, &f.stage()).unwrap();
    let data = snapshot.root().join("data");
    std::fs::write(data.join(".writer.lock"), b"").unwrap();
    std::fs::create_dir_all(data.join("captures")).unwrap();
    std::fs::write(data.join("captures/.capture.lock"), b"").unwrap();
    std::fs::create_dir_all(data.join("connectors")).unwrap();
    std::fs::write(data.join("connectors/.unknown.tmp"), b"retained").unwrap();
    std::fs::write(data.join("connectors/unknown.lock"), b"retained").unwrap();
    let inventory = payload_inventory(&data).unwrap();
    assert!(!inventory.contains_key(".writer.lock"));
    assert!(!inventory.contains_key("captures/.capture.lock"));
    assert!(inventory.contains_key("connectors/.unknown.tmp"));
    assert!(inventory.contains_key("connectors/unknown.lock"));
    assert!(payload_inventory(&f.root.join("absent"))
        .unwrap()
        .is_empty());
    let hard = f.root.join("hard-control");
    std::fs::hard_link(data.join(".writer.lock"), &hard).unwrap();
    assert!(
        payload_inventory(&data).is_err(),
        "an aliased control is refused rather than omitted"
    );
    std::fs::remove_file(&hard).unwrap();
    std::fs::remove_file(data.join(".writer.lock")).unwrap();
    std::fs::create_dir(data.join(".writer.lock")).unwrap();
    assert!(
        payload_inventory(&data).is_err(),
        "an empty directory cannot impersonate an omitted owning control"
    );
}

#[test]
fn records_package_member_restoration_resumes_exact_scratch_prefix_and_never_replaces() {
    let f = Fixture::new();
    let bytes: Vec<_> = (0..200_000).map(|i| (i % 251) as u8).collect();
    f.add("connectors/large", &bytes);
    f.export();
    let held = snapshot(&f.bag, &f.stage()).unwrap();
    let source = held.root().join("data/connectors/large");
    let target = f.root.join("restored");
    let scratch = f.root.join("intent/member.part");
    let expected = &held.payload()["connectors/large"];
    STOP_RESTORE.with(|flag| flag.set(true));
    assert!(
        restore_member(&source, &target, "connectors/large", &scratch, expected)
            .unwrap_err()
            .contains("interrupted")
    );
    assert!(!target.join("connectors/large").exists());
    let prefix = std::fs::read(&scratch).unwrap();
    assert!(prefix.len() < bytes.len());
    assert_eq!(prefix, bytes[..prefix.len()]);
    assert!(restore_member(&source, &target, "connectors/large", &scratch, expected).unwrap());
    assert_eq!(
        std::fs::read(target.join("connectors/large")).unwrap(),
        bytes
    );
    assert!(!scratch.exists());
    assert!(!restore_member(&source, &target, "connectors/large", &scratch, expected).unwrap());
    held.verify_unchanged().unwrap();
    held.source_unchanged().unwrap();
    let inventory = payload_inventory(&target).unwrap();
    assert_eq!(inventory["connectors/large"], *expected);
    assert_eq!(
        std::fs::metadata(target.join("connectors")).unwrap().mode() & 0o777,
        0o700
    );
    assert_eq!(
        std::fs::metadata(target.join("connectors/large"))
            .unwrap()
            .mode()
            & 0o777,
        0o600
    );

    std::fs::write(
        target.join("connectors/large"),
        b"existing conflicting bytes",
    )
    .unwrap();
    assert!(
        restore_member(&source, &target, "connectors/large", &scratch, expected)
            .unwrap_err()
            .contains("nothing overwritten")
    );
    assert_eq!(
        std::fs::read(target.join("connectors/large")).unwrap(),
        b"existing conflicting bytes"
    );
}

#[test]
fn records_package_member_restoration_preserves_conflicting_scratch_and_refuses_linked_targets() {
    for variant in [
        "scratch",
        "target-link",
        "parent-link",
        "source-link",
        "traversal",
    ] {
        let f = Fixture::new();
        f.export();
        let held = snapshot(&f.bag, &f.stage()).unwrap();
        let mut source = held.root().join("data/project.json");
        let target = f.root.join("restored");
        let scratch = f.root.join("scratch.part");
        let outside = f.root.join("external");
        std::fs::write(&outside, b"outside evidence").unwrap();
        let expected = &held.payload()["project.json"];
        let relative = if variant == "traversal" {
            "../external"
        } else {
            "nested/project.json"
        };
        match variant {
            "scratch" => {
                std::fs::write(&scratch, b"wrong").unwrap();
                std::fs::set_permissions(&scratch, std::fs::Permissions::from_mode(0o600)).unwrap();
            }
            "target-link" => {
                std::fs::create_dir_all(target.join("nested")).unwrap();
                std::os::unix::fs::symlink(&outside, target.join("nested/project.json")).unwrap();
            }
            "parent-link" => {
                std::fs::create_dir_all(&target).unwrap();
                std::os::unix::fs::symlink(&f.root, target.join("nested")).unwrap();
            }
            "source-link" => {
                let alias = f.root.join("source-alias");
                std::os::unix::fs::symlink(&source, &alias).unwrap();
                source = alias;
            }
            _ => {}
        }
        assert!(
            restore_member(&source, &target, relative, &scratch, expected).is_err(),
            "{variant}"
        );
        assert_eq!(std::fs::read(&outside).unwrap(), b"outside evidence");
        if variant == "scratch" {
            assert_eq!(std::fs::read(&scratch).unwrap(), b"wrong");
        }
    }
}

#[test]
fn records_package_small_controls_publish_whole_bytes_once_and_match_exactly() {
    let f = Fixture::new();
    let path = f.root.join("administration/imports/intent.json");
    let bytes = b"{\n  \"format\": \"invented exact control\"\n}\n";
    create_or_match(&path, bytes).unwrap();
    let first = std::fs::metadata(&path).unwrap();
    assert_eq!(first.mode() & 0o777, 0o600);
    assert_eq!(first.nlink(), 1);
    create_or_match(&path, bytes).unwrap();
    assert_eq!(std::fs::metadata(&path).unwrap().ino(), first.ino());
    assert_eq!(std::fs::read(&path).unwrap(), bytes);
    assert!(create_or_match(&path, b"different bytes")
        .unwrap_err()
        .contains("nothing overwritten"));
    assert_eq!(std::fs::read(&path).unwrap(), bytes);
    let linked = f.root.join("linked-control");
    std::os::unix::fs::symlink(&path, &linked).unwrap();
    assert!(create_or_match(&linked, bytes).is_err());
    assert_eq!(std::fs::read(&path).unwrap(), bytes);
}

#[test]
fn records_package_publication_uncertainty_keeps_complete_members_and_controls_for_reconciliation()
{
    let f = Fixture::new();
    f.export();
    let held = snapshot(&f.bag, &f.stage()).unwrap();
    let source = held.root().join("data/project.json");
    let target = f.root.join("restored");
    let scratch = f.root.join("intent/member.part");
    let expected = &held.payload()["project.json"];
    FAIL_PUBLICATION_SYNC.with(|flag| flag.set(true));
    let error = restore_member(&source, &target, "project.json", &scratch, expected).unwrap_err();
    assert!(error.contains("durability uncertain"));
    assert_eq!(
        payload_inventory(&target).unwrap()["project.json"],
        *expected
    );
    assert!(!restore_member(&source, &target, "project.json", &scratch, expected).unwrap());
    held.verify_unchanged().unwrap();

    let control = f.root.join("administration/import-intent.json");
    let bytes = b"{\"exact\":\"complete control\"}\n";
    FAIL_PUBLICATION_SYNC.with(|flag| flag.set(true));
    assert!(create_or_match(&control, bytes)
        .unwrap_err()
        .contains("durability uncertain"));
    assert_eq!(std::fs::read(&control).unwrap(), bytes);
    let inode = std::fs::metadata(&control).unwrap().ino();
    create_or_match(&control, bytes).unwrap();
    assert_eq!(std::fs::metadata(&control).unwrap().ino(), inode);
}

#[test]
fn records_package_target_filesystem_aliases_are_refused_instead_of_counted_as_existing() {
    for (existing, requested) in [
        ("Record.json", "record.json"),
        ("e\u{301}.json", "\u{e9}.json"),
    ] {
        let f = Fixture::new();
        f.export();
        let held = snapshot(&f.bag, &f.stage()).unwrap();
        let source = held.root().join("data/project.json");
        let target = f.root.join("restored");
        std::fs::create_dir(&target).unwrap();
        let bytes = std::fs::read(&source).unwrap();
        std::fs::write(target.join(existing), &bytes).unwrap();
        let aliased = target.join(requested).exists();
        let result = restore_member(
            &source,
            &target,
            requested,
            &f.root.join("member.part"),
            &held.payload()["project.json"],
        );
        if aliased {
            assert!(result.unwrap_err().contains("aliases another spelling"));
        } else {
            assert!(
                result.unwrap(),
                "distinct names on this filesystem must both survive"
            );
        }
        assert_eq!(std::fs::read(target.join(existing)).unwrap(), bytes);
    }
}

#[test]
fn records_package_mutable_association_replacement_binds_original_and_reconciles_exact_retry() {
    let f = Fixture::new();
    let path = f.root.join("association/.chirality/project.json");
    let original = b"{ \"store\": \"prior\" }\n";
    let replacement = b"{ \"store\": \"chosen current\" }\n";
    create_or_match(&path, original).unwrap();
    let first = std::fs::metadata(&path).unwrap().ino();
    assert!(replace_control(&path, b"unequal original", replacement)
        .unwrap_err()
        .contains("nothing replaced"));
    assert_eq!(std::fs::read(&path).unwrap(), original);
    replace_control(&path, original, replacement).unwrap();
    let second = std::fs::metadata(&path).unwrap();
    assert_ne!(first, second.ino());
    assert_eq!(second.nlink(), 1);
    assert_eq!(second.mode() & 0o777, 0o600);
    replace_control(&path, original, replacement).unwrap();
    assert_eq!(std::fs::metadata(&path).unwrap().ino(), second.ino());
    assert_eq!(std::fs::read(&path).unwrap(), replacement);
    let linked = f.root.join("linked-association/.chirality/project.json");
    std::fs::create_dir_all(linked.parent().unwrap()).unwrap();
    std::os::unix::fs::symlink(&path, &linked).unwrap();
    assert!(replace_control(&linked, replacement, original).is_err());
    assert_eq!(std::fs::read(&path).unwrap(), replacement);
}

#[test]
fn records_package_mutable_association_refuses_a_changed_original_and_recovers_uncertain_replacement(
) {
    let f = Fixture::new();
    let path = f.root.join("association/.chirality/project.json");
    create_or_match(&path, b"confirmed original").unwrap();
    let raced = path.clone();
    BEFORE_CONTROL_REPLACE.with(|h| {
        *h.borrow_mut() = Some(Box::new(move || {
            std::fs::write(raced, b"new outside bytes").unwrap();
        }))
    });
    assert!(
        replace_control(&path, b"confirmed original", b"replacement")
            .unwrap_err()
            .contains("changed before publication")
    );
    assert_eq!(std::fs::read(&path).unwrap(), b"new outside bytes");
    FAIL_PUBLICATION_SYNC.with(|flag| flag.set(true));
    assert!(replace_control(&path, b"new outside bytes", b"replacement")
        .unwrap_err()
        .contains("durability uncertain"));
    assert_eq!(std::fs::read(&path).unwrap(), b"replacement");
    let inode = std::fs::metadata(&path).unwrap().ino();
    replace_control(&path, b"new outside bytes", b"replacement").unwrap();
    assert_eq!(std::fs::metadata(&path).unwrap().ino(), inode);
}

#[test]
fn records_package_operational_envelopes_reject_duplicate_json_keys_without_changing_source_bytes()
{
    for (name, member) in [
        (
            "data/project.json",
            "\"format\":\"chirality.records-store.project\",",
        ),
        ("records-administration.json", "\"formatVersion\":\"0.1\","),
        (
            "records-administration.json",
            "\"uninterpreted\":{\"claim\":1,\"claim\":2},",
        ),
        (
            "records-chain-heads.json",
            "\"format\":\"chirality.records-export-chain-heads\",",
        ),
    ] {
        let f = Fixture::new();
        f.export();
        let path = f.bag.join(name);
        let original = std::fs::read_to_string(&path).unwrap();
        let duplicate = original.replacen('{', &format!("{{{member}"), 1);
        std::fs::write(&path, &duplicate).unwrap();
        f.rehash();
        assert!(
            crate::records_export::verify(&f.bag).is_ok(),
            "ordinary byte verification does not admit the operational envelope"
        );
        let source = custody(&f.bag).unwrap();
        assert!(
            snapshot(&f.bag, &f.stage())
                .unwrap_err()
                .contains("duplicate JSON object key"),
            "{name}"
        );
        source.unchanged().unwrap();
        assert_eq!(std::fs::read(&path).unwrap(), duplicate.as_bytes());
    }
}

#[test]
fn records_package_staged_controls_keep_failed_partial_bytes_outside_journal_and_payload() {
    for relative in [
        "journal/intent.json",
        "journal/completed.json",
        "payload/import-receipt.json",
    ] {
        let f = Fixture::new();
        let path = f.root.join(relative);
        let staging = f.root.join("intent-owned/control-staging");
        let bytes = b"{ \"exact\": \"complete original control bytes\" }\r\n";
        fail_control_before_publish_for_test(Some(path.clone()));
        let error = create_or_match_staged(&path, bytes, &staging).unwrap_err();
        assert!(error.contains("before publication"));
        assert!(!path.exists());
        assert!(
            std::fs::read_dir(path.parent().unwrap())
                .unwrap()
                .next()
                .is_none(),
            "strict final inventory remains empty"
        );
        let temporary: Vec<_> = std::fs::read_dir(&staging)
            .unwrap()
            .map(|e| e.unwrap().path())
            .collect();
        assert_eq!(temporary.len(), 1);
        let partial = std::fs::read(&temporary[0]).unwrap();
        assert!(!partial.is_empty() && partial.len() < bytes.len());
        assert_eq!(partial, bytes[..partial.len()]);
        assert_eq!(
            std::fs::metadata(&temporary[0]).unwrap().mode() & 0o777,
            0o600
        );
        assert_eq!(std::fs::metadata(&staging).unwrap().mode() & 0o777, 0o700);
        create_or_match_staged(&path, bytes, &staging).unwrap();
        assert_eq!(std::fs::read(&path).unwrap(), bytes);
        assert_eq!(
            std::fs::read(&temporary[0]).unwrap(),
            partial,
            "unpublished evidence is never removed or rewritten"
        );
        let inode = std::fs::metadata(&path).unwrap().ino();
        create_or_match_staged(&path, bytes, &staging).unwrap();
        assert_eq!(std::fs::metadata(&path).unwrap().ino(), inode);
        assert_eq!(
            std::fs::read_dir(path.parent().unwrap()).unwrap().count(),
            1
        );
        assert!(
            create_or_match_staged(&path, b"conflicting control", &staging)
                .unwrap_err()
                .contains("nothing overwritten")
        );
        assert_eq!(std::fs::read(&path).unwrap(), bytes);
    }
}

#[test]
fn records_package_staged_control_fault_is_path_specific_once_and_retains_uncertain_complete_bytes()
{
    let f = Fixture::new();
    let wanted = f.root.join("journal/wanted.json");
    let other = f.root.join("journal/other.json");
    let staging = f.root.join("intent-owned/control-staging");
    let bytes = b"{\"intended\":true}\n";
    fail_control_before_publish_for_test(Some(wanted.clone()));
    create_or_match_staged(&other, bytes, &staging).unwrap();
    assert!(create_or_match_staged(&wanted, bytes, &staging).is_err());
    assert!(!wanted.exists());
    FAIL_PUBLICATION_SYNC.with(|flag| flag.set(true));
    assert!(create_or_match_staged(&wanted, bytes, &staging)
        .unwrap_err()
        .contains("durability uncertain"));
    assert_eq!(std::fs::read(&wanted).unwrap(), bytes);
    let inode = std::fs::metadata(&wanted).unwrap().ino();
    create_or_match_staged(&wanted, bytes, &staging).unwrap();
    assert_eq!(std::fs::metadata(&wanted).unwrap().ino(), inode);
}

#[test]
fn records_package_staged_controls_refuse_overlapping_public_or_linked_staging() {
    let f = Fixture::new();
    let journal = f.root.join("journal");
    let path = journal.join("intent.json");
    assert!(
        create_or_match_staged(&path, b"control", &journal.join("temporary"))
            .unwrap_err()
            .contains("separate")
    );
    let public = f.root.join("public-staging");
    std::fs::create_dir(&public).unwrap();
    std::fs::set_permissions(&public, std::fs::Permissions::from_mode(0o755)).unwrap();
    assert!(create_or_match_staged(&path, b"control", &public)
        .unwrap_err()
        .contains("not private"));
    let linked = f.root.join("linked-staging");
    std::os::unix::fs::symlink(&public, &linked).unwrap();
    assert!(create_or_match_staged(&path, b"control", &linked).is_err());
    assert!(!path.exists());
    assert!(std::fs::read_dir(&public).unwrap().next().is_none());
}
