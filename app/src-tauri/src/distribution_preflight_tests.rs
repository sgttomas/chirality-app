use super::*;
use std::{
    fs,
    os::unix::fs::{symlink, PermissionsExt},
    sync::atomic::{AtomicU64, Ordering},
};
static NEXT: AtomicU64 = AtomicU64::new(0);
struct Fixture {
    base: std::path::PathBuf,
    tree: std::path::PathBuf,
    selected: Artifact,
    generated: serde_json::Value,
}
impl Fixture {
    fn new() -> Self {
        let base = std::env::temp_dir().canonicalize().unwrap().join(format!(
            "distribution-s2-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir(&base).unwrap();
        let tree = base.join("vendor");
        fs::create_dir(&tree).unwrap();
        for p in ["bin", "codex-path", "codex-resources", "empty"] {
            fs::create_dir(tree.join(p)).unwrap();
        }
        fs::write(tree.join("bin/codex"), b"synthetic never executed").unwrap();
        fs::set_permissions(tree.join("bin/codex"), fs::Permissions::from_mode(0o755)).unwrap();
        fs::write(tree.join("codex-package.json"), b"{}").unwrap();
        let mut expected: serde_json::Value = serde_json::from_str(include_str!(
            "../resources/distribution-successor/synthetic-expected.json"
        ))
        .unwrap();
        expected["inventory"] = serde_json::to_value(scan(&tree).unwrap()).unwrap();
        let generated = expected["generated"].clone();
        let bytes = serde_json::to_vec(&expected).unwrap();
        fs::write(base.join("expected.json"), &bytes).unwrap();
        let er = Artifact {
            path: "expected.json".into(),
            sha256: digest(&bytes),
        };
        let mut att: serde_json::Value = serde_json::from_str(include_str!(
            "../resources/distribution-successor/synthetic-attestation.json"
        ))
        .unwrap();
        att["expected_reference"] = serde_json::to_value(&er).unwrap();
        let bytes = serde_json::to_vec(&att).unwrap();
        fs::write(base.join("attestation.json"), &bytes).unwrap();
        fs::write(
            base.join("synthetic-evidence.json"),
            include_bytes!("../resources/distribution-successor/synthetic-evidence.json"),
        )
        .unwrap();
        Self {
            base: base.clone(),
            tree,
            selected: {
                let selection = Selection {
                    format: "build-selection.s2".into(),
                    method: "codex-vendor-tree-v1".into(),
                    schema_ids: [
                        "expected-reference.s1".into(),
                        "adoption-attestation.s1".into(),
                    ],
                    expected: er,
                    attestation: Artifact {
                        path: "attestation.json".into(),
                        sha256: digest(&bytes),
                    },
                };
                let raw = serde_json::to_vec(&selection).unwrap();
                fs::write(base.join("selection.json"), &raw).unwrap();
                Artifact {
                    path: "selection.json".into(),
                    sha256: digest(&raw),
                }
            },
            generated,
        }
    }
    fn run(&self) -> Result<serde_json::Value, String> {
        staged_start(
            &self.base,
            &self.tree,
            &self.selected,
            &self.generated,
            Some(":/a::"),
            generation(),
            |plan| {
                assert!(plan.path.ends_with("::/a::"));
                Ok("codex-cli 9.9.9\n".into())
            },
            |_| {
                Ok(
                    serde_json::json!({"appSession":"synthetic-session","home":"synthetic-home","spawnCounter":1}),
                )
            },
        )
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.base);
    }
}
#[test]
fn connected_synthetic_start_is_never_verified() {
    let f = Fixture::new();
    let r = f.run().unwrap();
    assert_eq!(r["outcome"], "unverifiable");
    assert_eq!(r["generation"]["spawnCounter"], 1);
    assert!(!production_available());
}
#[test]
fn modes_empty_directories_and_bytes_are_identity() {
    for mutation in 0..4 {
        let f = Fixture::new();
        match mutation {
            0 => fs::set_permissions(&f.tree, fs::Permissions::from_mode(0o700)).unwrap(),
            1 => fs::remove_dir(f.tree.join("empty")).unwrap(),
            2 => fs::write(f.tree.join("bin/codex"), b"changed").unwrap(),
            _ => fs::set_permissions(f.tree.join("bin/codex"), fs::Permissions::from_mode(0o700))
                .unwrap(),
        };
        assert!(f.run().is_err());
    }
}
#[test]
fn symlink_hardlink_and_root_alias_refuse() {
    let f = Fixture::new();
    symlink("bin/codex", f.tree.join("alias")).unwrap();
    assert!(scan(&f.tree).is_err());
    fs::remove_file(f.tree.join("alias")).unwrap();
    fs::hard_link(f.tree.join("bin/codex"), f.tree.join("hard")).unwrap();
    assert!(scan(&f.tree).is_err());
    fs::remove_file(f.tree.join("hard")).unwrap();
    symlink(&f.tree, f.base.join("root-alias")).unwrap();
    assert!(scan(&f.base.join("root-alias")).is_err());
}
#[test]
fn pre_spawn_mutation_blocks_launch() {
    let f = Fixture::new();
    let r = staged_start(
        &f.base,
        &f.tree,
        &f.selected,
        &f.generated,
        None,
        generation(),
        |_| {
            fs::write(f.tree.join("bin/codex"), b"raced").unwrap();
            Ok("codex-cli 9.9.9".into())
        },
        |_| panic!("must not launch"),
    );
    assert!(r.is_err());
}
#[test]
fn exact_artifact_bytes_and_selection_refuse_tampering() {
    let f = Fixture::new();
    let path = f.base.join("expected.json");
    let mut bytes = fs::read(&path).unwrap();
    bytes.push(b' ');
    fs::write(path, bytes).unwrap();
    assert!(f.run().is_err());
}
#[test]
fn generated_label_and_path_contradictions_refuse() {
    let f = Fixture::new();
    assert!(staged_start(
        &f.base,
        &f.tree,
        &f.selected,
        &serde_json::json!({}),
        None,
        generation(),
        |_| panic!("must not probe"),
        |_| panic!("must not launch")
    )
    .is_err());
    assert!(staged_start(
        &f.base,
        &f.tree,
        &f.selected,
        &f.generated,
        None,
        generation(),
        |_| Ok("codex-cli 0.0.0".into()),
        |_| panic!("must not launch")
    )
    .is_err());
    assert!(plan(Path::new("/synthetic:relocation"), None).is_err());
}
#[test]
fn duplicate_inventory_is_never_equal() {
    let f = Fixture::new();
    let a = scan(&f.tree).unwrap();
    let mut b = a.clone();
    b.entries.push(b.entries[0].clone());
    assert!(!equal(&a, &b));
}

#[test]
fn wrong_tree_never_reaches_label() {
    let f = Fixture::new();
    fs::write(f.tree.join("extra"), b"unexpected").unwrap();
    assert!(staged_start(
        &f.base,
        &f.tree,
        &f.selected,
        &f.generated,
        None,
        generation(),
        |_| panic!("must not probe"),
        |_| panic!("must not launch")
    )
    .is_err());
}
#[test]
fn unknown_schema_and_wrong_attestation_subject_refuse() {
    for field in ["format", "expected_reference"] {
        let f = Fixture::new();
        let mut a: serde_json::Value =
            serde_json::from_slice(&fs::read(f.base.join("attestation.json")).unwrap()).unwrap();
        if field == "format" {
            a[field] = "adoption-attestation.unknown".into();
        } else {
            a[field]["sha256"] = "0".repeat(64).into();
        }
        let bytes = serde_json::to_vec(&a).unwrap();
        fs::write(f.base.join("attestation.json"), &bytes).unwrap();
        let mut selected: Selection =
            serde_json::from_slice(&fs::read(f.base.join("selection.json")).unwrap()).unwrap();
        selected.attestation.sha256 = digest(&bytes);
        let raw = serde_json::to_vec(&selected).unwrap();
        fs::write(f.base.join("selection.json"), &raw).unwrap();
        let selected = Artifact {
            path: "selection.json".into(),
            sha256: digest(&raw),
        };
        assert!(resolve(&f.base, &selected).is_err());
    }
}
#[test]
fn special_and_invalid_names_refuse_without_blocking() {
    use std::os::unix::ffi::OsStringExt;
    let f = Fixture::new();
    let fifo = CString::new(f.tree.join("fifo").to_str().unwrap()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
    assert!(scan(&f.tree).is_err());
    fs::remove_file(f.tree.join("fifo")).unwrap();
    let invalid = std::ffi::OsString::from_vec(vec![0xff]);
    match fs::write(f.tree.join(&invalid), b"x") {
        Ok(()) => assert!(scan(&f.tree).is_err()),
        Err(e) => assert_eq!(
            e.raw_os_error(),
            Some(libc::EILSEQ),
            "filesystem itself refuses invalid UTF-8"
        ),
    }
}

fn generation() -> serde_json::Value {
    serde_json::json!({"appSession":"synthetic-session","home":"synthetic-home","spawnCounter":1})
}
#[test]
fn wrong_build_anchor_and_foreign_generation_refuse() {
    let f = Fixture::new();
    let wrong = Artifact {
        path: f.selected.path.clone(),
        sha256: "0".repeat(64),
    };
    assert!(resolve(&f.base, &wrong).is_err());
    assert!(staged_start(
        &f.base,
        &f.tree,
        &f.selected,
        &f.generated,
        None,
        generation(),
        |_| Ok("codex-cli 9.9.9".into()),
        |_| Ok(
            serde_json::json!({"appSession":"foreign","home":"synthetic-home","spawnCounter":1})
        )
    )
    .is_err());
    assert!(staged_start(
        &f.base,
        &f.tree,
        &f.selected,
        &f.generated,
        None,
        serde_json::json!({}),
        |_| panic!("must not probe"),
        |_| panic!("must not launch")
    )
    .is_err());
}

// Reviewer regression: writing an earlier file does not update its parent dir.
#[test]
fn earlier_file_mutation_during_later_read_is_detected() {
    earlier_file_mutation(false);
}
#[test]
fn same_size_mutation_with_restored_mtime_is_detected() {
    earlier_file_mutation(true);
}
fn earlier_file_mutation(restore_mtime: bool) {
    let f = Fixture::new();
    let p = f.base.join("race");
    fs::create_dir(&p).unwrap();
    fs::write(p.join("a"), b"old").unwrap();
    let original = fs::metadata(p.join("a")).unwrap();
    let large = fs::File::create(p.join("b")).unwrap();
    large.set_len(512 * 1024 * 1024).unwrap();
    let change = p.join("a");
    let thread = std::thread::spawn(move || {
        std::thread::sleep(std::time::Duration::from_millis(25));
        fs::write(&change, b"new").unwrap();
        if restore_mtime {
            fs::OpenOptions::new()
                .write(true)
                .open(&change)
                .unwrap()
                .set_times(fs::FileTimes::new().set_modified(original.modified().unwrap()))
                .unwrap();
            let after = fs::metadata(&change).unwrap();
            assert_eq!(
                (original.mtime(), original.mtime_nsec()),
                (after.mtime(), after.mtime_nsec())
            );
            assert_eq!(original.size(), after.size());
            assert_ne!(
                (original.ctime(), original.ctime_nsec()),
                (after.ctime(), after.ctime_nsec())
            );
        }
    });
    let result = scan(&p);
    thread.join().unwrap();
    assert!(
        result.is_err(),
        "scan accepted an earlier-file mutation while hashing later file: {result:?}"
    );
}
