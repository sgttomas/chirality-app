use super::platform::Stage;
use super::*;
use serde_json::json;
use std::{
    fs,
    os::unix::fs::{symlink, PermissionsExt},
    sync::{Arc, Barrier},
};
const KEY: &str = "12345678-1234-4234-8234-123456789abc";
struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let path = std::env::temp_dir().join(crate::util::opaque_id("route-store-test-").unwrap());
        fs::create_dir(&path).unwrap();
        Self(path.canonicalize().unwrap())
    }
    fn project(&self) -> PathBuf {
        let p = self.0.join("project");
        fs::create_dir(&p).unwrap();
        p
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn account(id: &str) -> Value {
    json!({"format":"chirality.connector.route-account", "formatVersion":"0.2", "account_id":id,
        "question":{"id":"Q-test", "text":"What can be supported?", "at_revision":"invented-fixture"},
        "trigger":{"connector":"pec", "why":"source unavailable"}, "sources":[], "facts":[],
        "gaps":[{"gap":"source unreadable", "effect":"answer unsupported", "responsible":"fixture owner"}],
        "conclusions":{"supported":[], "unsupported":[{"conclusion":"answer", "why":"no source read"}],
            "prohibited":["no_work","ready","permitted","correct_by_presence"]},
        "duties":[
            {"duty":"locate_compare","actor_role":"agent","standing":"prepared","reason":"fixture only"},
            {"duty":"review_integrate","actor_role":"manager","standing":"outstanding","reason":"not performed"},
            {"duty":"cross_undertaking_coordination","actor_role":"person","standing":"not_required","reason":"bounded fixture"}],
        "recorder":{"kind":"tool","identity":"invented fixture"},
        "written_at":"fixture-constant", "written_at_source":"build_constant"})
}
fn failure() -> StoreError {
    StoreError::new(ErrorKind::Io, "injected interruption")
}

#[test]
fn embedded_schemas_match_maintained_design_and_validate_exact_versions() {
    let design = Path::new(env!("CARGO_MANIFEST_DIR")).join("../../execution/PKG-07_PEC receiving and connector fallback/1_Working/DEL-07-02_Connector limitation and source-file recovery paths/Design");
    for (name, text) in RESOURCES {
        assert_eq!(fs::read_to_string(design.join(name)).unwrap(), *text);
    }
    let v2 = account("ra:v2");
    validate_account(&v2).unwrap();
    let mut v1 = v2.clone();
    v1["formatVersion"] = json!("0.1");
    v1["account_id"] = json!("ra:v1");
    assert_eq!(
        validate_account(&v1).unwrap_err().kind,
        ErrorKind::InvalidAccount
    );
    v1["sources"] = json!([{"source_id":"fixture", "path":"invented.md", "revision":"fixture", "sha256":"a".repeat(64), "role":"test"}]);
    validate_account(&v1).unwrap();
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let r1 = store.write(&v1).unwrap();
    let r2 = store.write(&v2).unwrap();
    drop(store);
    let cold = ProjectRouteStore::open(&p).unwrap();
    assert_eq!(cold.resolve(&r1).unwrap().account, v1);
    assert_eq!(cold.resolve(&r2).unwrap().account, v2);
    let mut mislabeled = v2.clone();
    mislabeled["formatVersion"] = json!("0.3");
    assert_eq!(
        validate_account(&mislabeled).unwrap_err().kind,
        ErrorKind::InvalidAccount
    );
    for bad in ["0.4", "", "1"] {
        let mut v = v2.clone();
        v["formatVersion"] = json!(bad);
        assert_eq!(
            validate_account(&v).unwrap_err().kind,
            ErrorKind::UnsupportedFormat
        );
    }
    for field in ["facts", "gaps", "conclusions"] {
        let mut v = v2.clone();
        match field {
            "facts" => {
                v["facts"] = json!([{"fact_id":"f", "statement":"invented", "source_id":"missing", "anchor":"x"}])
            }
            "gaps" => v["gaps"] = json!([]),
            _ => {
                v["conclusions"]["supported"] =
                    json!([{"statement":"unsupported", "basis":"source_route"}])
            }
        }
        assert!(validate_account(&v).is_err());
    }
    let mut duty = v2.clone();
    duty["duties"][0]["standing"] = json!("performed");
    assert!(validate_account(&duty).is_err());
    duty["duties"][0]["actor"] = json!("claimed actor");
    duty["duties"][0]["evidence"] = json!("unverified claim");
    validate_account(&duty).unwrap(); // shape does not establish actual performance.
}
#[test]
fn round_trip_restart_project_move_and_symlink_selected_root() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let alias = scratch.0.join("alias");
    symlink(&p, &alias).unwrap();
    let store = ProjectRouteStore::open(&alias).unwrap();
    assert_eq!(store.resolved_project(), p);
    let data = account("ra:unrelated-governed-id");
    let reference = store.write(&data).unwrap();
    assert!(canonical_name(
        reference.relative_path.rsplit('/').next().unwrap()
    ));
    assert!(!reference.relative_path.contains("unrelated"));
    assert_eq!(
        fs::read(p.join(&reference.relative_path)).unwrap(),
        serde_json::to_vec(&data).unwrap()
    );
    let moved = scratch.0.join("moved");
    fs::rename(&p, &moved).unwrap();
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::LocationMismatch
    );
    let cold = ProjectRouteStore::open(&moved).unwrap();
    let discovery = cold.discover();
    assert!(discovery.enumeration_complete);
    assert!(discovery.issues.is_empty());
    assert_eq!(discovery.accounts.len(), 1);
    assert_eq!(cold.resolve(&reference).unwrap().account, data);
    assert_eq!(cold.discover().accounts.len(), 1); // repeated enumeration gets a fresh offset.
}
#[test]
fn invalid_accounts_and_paths_create_nothing() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let mut invalid = account("../../escape");
    assert!(store.write(&invalid).is_err());
    assert!(!p.join(".chirality").exists());
    invalid = account("ra:test");
    invalid["format"] = json!("wrong");
    assert!(store.write(&invalid).is_err());
    assert!(ProjectRouteStore::open(Path::new(".")).is_err());
    assert!(ProjectRouteStore::open(&p.join("../project")).is_err());
    let mut reference = store.write(&account("ra:test")).unwrap();
    for path in [
        "../escape.json",
        "/absolute.json",
        "a//b",
        "a/./b",
        "a/../b",
        "C:\\escape",
        "a\\b",
    ] {
        reference.relative_path = path.into();
        assert_eq!(
            store.resolve(&reference).unwrap_err().kind,
            ErrorKind::InvalidInput
        );
    }
}
#[test]
fn collision_and_failed_repeated_writes_preserve_original_bytes() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let reference = store
        .write_inner(&account("ra:first"), KEY, |_| Ok(()))
        .unwrap();
    let bytes = fs::read(p.join(&reference.relative_path)).unwrap();
    for _ in 0..2 {
        let err = store
            .write_inner(&account("ra:second"), KEY, |_| Ok(()))
            .unwrap_err();
        assert_eq!(err.kind, ErrorKind::Collision);
        assert!(!err.uncertain_commit);
        assert!(err.temporary_leftover.is_some());
        assert_eq!(fs::read(p.join(&reference.relative_path)).unwrap(), bytes);
    }
    assert_eq!(store.discover().accounts.len(), 1);
    assert_eq!(
        store
            .discover()
            .issues
            .iter()
            .filter(|i| i.kind == ErrorKind::TemporaryLeftover)
            .count(),
        2
    );
}
#[test]
fn malformed_unknown_duplicate_temporary_and_link_entries_stay_visible() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    assert!(store.discover().directory_absent);
    let reference = store.write(&account("ra:duplicate")).unwrap();
    store.write(&account("ra:duplicate")).unwrap();
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::DuplicateIdentity
    );
    let d = p.join(DIRECTORY);
    fs::write(d.join(format!("{KEY}.json")), b"{").unwrap();
    let mut unknown = account("ra:unknown");
    unknown["formatVersion"] = json!("100");
    fs::write(
        d.join("22345678-1234-4234-8234-123456789abc.json"),
        serde_json::to_vec(&unknown).unwrap(),
    )
    .unwrap();
    fs::write(d.join(".route-interrupted.tmp"), b"partial").unwrap();
    fs::write(d.join("ra:bad.json"), b"{}").unwrap();
    symlink(
        p.join(&reference.relative_path),
        d.join("32345678-1234-4234-8234-123456789abc.json"),
    )
    .unwrap();
    fs::create_dir(d.join("42345678-1234-4234-8234-123456789abc.json")).unwrap();
    let snapshot = store.discover();
    assert!(snapshot.enumeration_complete);
    assert!(!snapshot.directory_absent);
    assert_eq!(snapshot.by_account_id["ra:duplicate"].len(), 2);
    for kind in [
        ErrorKind::InvalidAccount,
        ErrorKind::UnsupportedFormat,
        ErrorKind::TemporaryLeftover,
        ErrorKind::InvalidName,
        ErrorKind::UnsafeEntry,
        ErrorKind::DuplicateIdentity,
    ] {
        assert!(snapshot.issues.iter().any(|i| i.kind == kind), "{kind:?}");
    }
}
#[test]
fn every_ancestor_symlink_and_non_directory_refuse_without_relocation() {
    for depth in 0..PARTS.len() {
        for link in [true, false] {
            let scratch = Scratch::new();
            let p = scratch.project();
            let outside = scratch.0.join("outside");
            fs::create_dir(&outside).unwrap();
            let mut parent = p.clone();
            for part in &PARTS[..depth] {
                parent.push(part);
                fs::create_dir(&parent).unwrap();
            }
            let target = parent.join(PARTS[depth]);
            if link {
                symlink(&outside, &target).unwrap();
            } else {
                fs::write(&target, b"not a directory").unwrap();
            }
            let store = ProjectRouteStore::open(&p).unwrap();
            assert!(store.write(&account("ra:test")).is_err());
            let d = store.discover();
            assert!(!d.enumeration_complete);
            assert!(!d.directory_absent);
            assert!(!d.issues.is_empty());
            assert_eq!(fs::read_dir(&outside).unwrap().count(), 0);
        }
    }
}
#[test]
fn target_links_fifo_unreadable_and_changed_binding_refuse() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let reference = store.write(&account("ra:test")).unwrap();
    let target = p.join(DIRECTORY).join(format!("{KEY}.json"));
    symlink(p.join(&reference.relative_path), &target).unwrap();
    let err = store
        .write_inner(&account("ra:other"), KEY, |_| Ok(()))
        .unwrap_err();
    assert_eq!(err.kind, ErrorKind::Collision);
    fs::remove_file(&target).unwrap();
    fs::hard_link(p.join(&reference.relative_path), &target).unwrap();
    assert_eq!(
        store
            .write_inner(&account("ra:other"), KEY, |_| Ok(()))
            .unwrap_err()
            .kind,
        ErrorKind::Collision
    );
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::UnsafeEntry
    );
    fs::remove_file(&target).unwrap();
    let n = std::ffi::CString::new(target.as_os_str().as_encoded_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(n.as_ptr(), 0o600) }, 0);
    assert!(store
        .discover()
        .issues
        .iter()
        .any(|i| i.kind == ErrorKind::UnsafeEntry));
    fs::remove_file(&target).unwrap();
    let file = p.join(&reference.relative_path);
    fs::set_permissions(&file, fs::Permissions::from_mode(0)).unwrap();
    assert!(!store.discover().issues.is_empty());
    fs::set_permissions(&file, fs::Permissions::from_mode(0o600)).unwrap();
    let original = fs::read(&file).unwrap();
    fs::write(&file, serde_json::to_vec(&account("ra:changed")).unwrap()).unwrap();
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::ChangedContent
    );
    fs::write(&file, &original).unwrap();
    let saved = p.join("saved");
    fs::rename(&file, &saved).unwrap();
    fs::write(&file, &original).unwrap();
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::ChangedContent
    );
    fs::remove_file(file).unwrap();
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::Missing
    );
}
#[test]
fn unwritable_directory_is_definite_and_never_relocated() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    store.write(&account("ra:first")).unwrap();
    let d = p.join(DIRECTORY);
    fs::set_permissions(&d, fs::Permissions::from_mode(0o500)).unwrap();
    let result = store.write(&account("ra:blocked"));
    fs::set_permissions(&d, fs::Permissions::from_mode(0o700)).unwrap();
    let error = result.unwrap_err();
    assert!(!error.uncertain_commit);
    assert_eq!(store.discover().accounts.len(), 1);
}
#[test]
fn real_rename_race_retains_capability_reports_uncertainty_and_reconciles() {
    for depth in 0..=PARTS.len() {
        let scratch = Scratch::new();
        let p = scratch.project();
        let store = ProjectRouteStore::open(&p).unwrap();
        let original = PARTS[..depth].iter().fold(p.clone(), |p, s| p.join(s));
        let moved = scratch.0.join("moved");
        let err = store
            .write_inner(&account("ra:race"), KEY, |stage| {
                if stage == Stage::TempSynced {
                    fs::rename(&original, &moved).unwrap();
                    fs::create_dir(&original).unwrap();
                }
                Ok(())
            })
            .unwrap_err();
        assert!(err.uncertain_commit);
        assert_eq!(err.kind, ErrorKind::LocationMismatch);
        assert_eq!(fs::read_dir(&original).unwrap().count(), 0); // replacement receives no write.
        let published = PARTS[depth..]
            .iter()
            .fold(moved.clone(), |p, s| p.join(s))
            .join(format!("{KEY}.json"));
        assert_eq!(
            crate::util::sha256_hex(&fs::read(&published).unwrap()),
            err.attempt.as_ref().unwrap().sha256
        );
        assert!(store.reconcile(err.attempt.as_ref().unwrap()).is_err());
        fs::remove_dir(&original).unwrap();
        fs::rename(&moved, &original).unwrap();
        let cold = ProjectRouteStore::open(&p).unwrap();
        assert_eq!(
            cold.reconcile(err.attempt.as_ref().unwrap())
                .unwrap()
                .account["account_id"],
            "ra:race"
        );
        assert_eq!(cold.discover().accounts.len(), 1); // no automatic retry.
    }
}
#[test]
fn prewrite_substitution_aborts_and_transient_move_is_not_continuous_containment() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let d = p.join(DIRECTORY);
    let moved = scratch.0.join("moved");
    let error = store
        .write_inner(&account("ra:pre"), KEY, |stage| {
            if stage == Stage::BeforeWrite {
                fs::rename(&d, &moved).unwrap();
                fs::create_dir(&d).unwrap();
            }
            Ok(())
        })
        .unwrap_err();
    assert!(!error.uncertain_commit);
    assert_eq!(error.kind, ErrorKind::LocationMismatch);
    assert_eq!(fs::read_dir(&moved).unwrap().count(), 0);
    fs::remove_dir(&d).unwrap();
    fs::rename(&moved, &d).unwrap();
    let reference = store
        .write_inner(&account("ra:transient"), KEY, |stage| {
            if stage == Stage::TempSynced {
                fs::rename(&d, &moved).unwrap();
                fs::create_dir(&d).unwrap();
            }
            if stage == Stage::Published {
                assert!(moved.join(format!("{KEY}.json")).exists()); // publication occurred outside current project tree.
                assert_eq!(fs::read_dir(&d).unwrap().count(), 0);
                fs::remove_dir(&d).unwrap();
                fs::rename(&moved, &d).unwrap();
            }
            Ok(())
        })
        .unwrap(); // pre/post observations match; cannot disprove the transient move.
    store.resolve(&reference).unwrap();
    fs::rename(&d, &moved).unwrap();
    fs::create_dir(&d).unwrap();
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::LocationMismatch
    );
}
#[test]
fn injected_failures_before_and_after_publication_preserve_recovery_details() {
    for stage in [
        Stage::BeforeWrite,
        Stage::TempSynced,
        Stage::Published,
        Stage::Verified,
    ] {
        let scratch = Scratch::new();
        let p = scratch.project();
        let store = ProjectRouteStore::open(&p).unwrap();
        let e = store
            .write_inner(&account("ra:interrupted"), KEY, |s| {
                if s == stage {
                    Err(failure())
                } else {
                    Ok(())
                }
            })
            .unwrap_err();
        assert!(e.attempt.is_some());
        assert_eq!(e.temporary_leftover.is_some(), stage == Stage::TempSynced);
        let after_publish = matches!(stage, Stage::Published | Stage::Verified);
        assert_eq!(e.uncertain_commit, after_publish);
        assert_eq!(store.discover().accounts.len(), usize::from(after_publish));
        if after_publish {
            store.reconcile(e.attempt.as_ref().unwrap()).unwrap();
        } else {
            assert!(!p.join(DIRECTORY).join(format!("{KEY}.json")).exists());
        }
    }
}
#[test]
fn concurrent_distinct_writers_and_identical_target_contention() {
    for same in [false, true] {
        let scratch = Scratch::new();
        let p = scratch.project();
        let barrier = Arc::new(Barrier::new(8));
        let threads: Vec<_> = (0..8)
            .map(|i| {
                let p = p.clone();
                let barrier = barrier.clone();
                std::thread::spawn(move || {
                    let store = ProjectRouteStore::open(&p).unwrap();
                    let data = account(&format!("ra:writer-{i}"));
                    let key = if same {
                        KEY.into()
                    } else {
                        crate::util::opaque_id("").unwrap()
                    };
                    store.write_inner(&data, &key, |s| {
                        if s == Stage::TempSynced {
                            barrier.wait();
                        }
                        Ok(())
                    })
                })
            })
            .collect();
        let results: Vec<_> = threads.into_iter().map(|t| t.join().unwrap()).collect();
        assert_eq!(
            results.iter().filter(|r| r.is_ok()).count(),
            if same { 1 } else { 8 }
        );
        for e in results.iter().filter_map(|r| r.as_ref().err()) {
            assert_eq!(e.kind, ErrorKind::Collision);
            assert!(!e.uncertain_commit);
        }
        let store = ProjectRouteStore::open(&p).unwrap();
        let d = store.discover();
        assert_eq!(
            d.issues
                .iter()
                .filter(|i| i.kind == ErrorKind::TemporaryLeftover)
                .count(),
            if same { 7 } else { 0 }
        );
        assert_eq!(d.accounts.len(), if same { 1 } else { 8 });
        for r in results.into_iter().filter_map(|r| r.ok()) {
            store.resolve(&r).unwrap();
        }
    }
}
#[test]
fn explicit_legacy_binding_reads_only_supplied_path() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let mut reference = store.write(&account("ra:legacy")).unwrap();
    fs::rename(p.join(&reference.relative_path), p.join("legacy.json")).unwrap();
    reference.relative_path = "legacy.json".into();
    reference.directories.truncate(1);
    assert!(store.discover().accounts.is_empty());
    assert_eq!(
        store.resolve(&reference).unwrap().account["account_id"],
        "ra:legacy"
    );
}
#[test]
fn abrupt_process_exit_leaves_visible_pre_and_post_publication_evidence() {
    for phase in ["before", "after"] {
        let scratch = Scratch::new();
        let p = scratch.project();
        let status = std::process::Command::new(std::env::current_exe().unwrap())
            .args([
                "--exact",
                "connector_route_store::tests::interruption_child",
                "--nocapture",
            ])
            .env("CHIRALITY_ROUTE_TEST_PROJECT", &p)
            .env("CHIRALITY_ROUTE_TEST_PHASE", phase)
            .status()
            .unwrap();
        assert_eq!(status.code(), Some(73));
        let store = ProjectRouteStore::open(&p).unwrap();
        let d = store.discover();
        assert_eq!(
            d.issues
                .iter()
                .any(|i| i.kind == ErrorKind::TemporaryLeftover),
            phase == "before"
        );
        let target = p.join(DIRECTORY).join(format!("{KEY}.json"));
        assert_eq!(target.exists(), phase == "after");
        if phase == "after" {
            assert!(d.issues.is_empty());
            assert_eq!(d.accounts.len(), 1);
            store.resolve(&d.accounts[0].reference).unwrap();
            // Cold inspection is not proof that the interrupted writer completed
            // its sync/postcheck or ever returned a successful binding.
        }
    }
}
#[test]
fn interruption_child() {
    let Ok(project) = std::env::var("CHIRALITY_ROUTE_TEST_PROJECT") else {
        return;
    };
    let phase = std::env::var("CHIRALITY_ROUTE_TEST_PHASE").unwrap();
    let store = ProjectRouteStore::open(Path::new(&project)).unwrap();
    store
        .write_inner(&account("ra:abrupt"), KEY, |stage| {
            if (phase == "before" && stage == Stage::TempSynced)
                || (phase == "after" && stage == Stage::Published)
            {
                std::process::exit(73);
            }
            Ok(())
        })
        .unwrap();
}

#[test]
fn postpublication_readback_detects_content_and_identity_tampering() {
    for identical_bytes in [false, true] {
        let scratch = Scratch::new();
        let p = scratch.project();
        let store = ProjectRouteStore::open(&p).unwrap();
        let target = p.join(DIRECTORY).join(format!("{KEY}.json"));
        let error = store
            .write_inner(&account("ra:original"), KEY, |stage| {
                if stage == Stage::Published {
                    if identical_bytes {
                        let bytes = fs::read(&target).unwrap();
                        fs::remove_file(&target).unwrap();
                        fs::write(&target, bytes).unwrap();
                    } else {
                        fs::write(
                            &target,
                            serde_json::to_vec(&account("ra:tampered")).unwrap(),
                        )
                        .unwrap();
                    }
                }
                Ok(())
            })
            .unwrap_err();
        assert!(error.uncertain_commit);
        assert_eq!(error.kind, ErrorKind::ChangedContent);
        assert!(target.exists());
        assert!(store.reconcile(error.attempt.as_ref().unwrap()).is_err());
        assert_eq!(fs::read_dir(p.join(DIRECTORY)).unwrap().count(), 1);
    }
}

#[test]
fn postpublication_symlink_substitution_never_follows_replacement() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let d = p.join(DIRECTORY);
    let moved = scratch.0.join("moved");
    let outside = scratch.0.join("outside");
    fs::create_dir(&outside).unwrap();
    let error = store
        .write_inner(&account("ra:link-race"), KEY, |stage| {
            if stage == Stage::TempSynced {
                fs::rename(&d, &moved).unwrap();
                symlink(&outside, &d).unwrap();
            }
            Ok(())
        })
        .unwrap_err();
    assert!(error.uncertain_commit);
    assert_eq!(error.kind, ErrorKind::LocationMismatch);
    assert_eq!(fs::read_dir(outside).unwrap().count(), 0);
    assert!(moved.join(format!("{KEY}.json")).exists());
    assert!(store.reconcile(error.attempt.as_ref().unwrap()).is_err());
}

#[test]
fn retained_temporary_and_unreadable_directory_are_not_empty_discovery() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let d = p.join(DIRECTORY);
    let error = store
        .write_inner(&account("ra:cleanup"), KEY, |stage| {
            if stage == Stage::TempSynced {
                fs::set_permissions(&d, fs::Permissions::from_mode(0o500)).unwrap();
                return Err(failure());
            }
            Ok(())
        })
        .unwrap_err();
    fs::set_permissions(&d, fs::Permissions::from_mode(0o700)).unwrap();
    assert!(!error.uncertain_commit);
    assert!(error.temporary_leftover.is_some());
    let recovery = store.discover();
    assert!(recovery.accounts.is_empty());
    assert!(!recovery.directory_absent);
    assert!(recovery
        .issues
        .iter()
        .any(|i| i.kind == ErrorKind::TemporaryLeftover));
    assert!(!d.join(format!("{KEY}.json")).exists());
    fs::set_permissions(&d, fs::Permissions::from_mode(0)).unwrap();
    let unreadable = store.discover();
    fs::set_permissions(&d, fs::Permissions::from_mode(0o700)).unwrap();
    assert!(!unreadable.enumeration_complete);
    assert!(!unreadable.directory_absent);
    assert!(!unreadable.issues.is_empty());
}

// Independent review R1 reproduction retained with corrected expectations:
// an observed foreign temporary is never a source or cleanup destination.
#[test]
fn substituted_temporary_is_neither_published_nor_removed() {
    for fail_before_publication in [false, true] {
        for same_bytes in [false, true] {
            let scratch = Scratch::new();
            let p = scratch.project();
            let store = ProjectRouteStore::open(&p).unwrap();
            let original = account("ra:original");
            let foreign = serde_json::to_vec(&account(if same_bytes {
                "ra:original"
            } else {
                "ra:foreign"
            }))
            .unwrap();
            let mut replacement = None;
            let error = store
                .write_inner(&original, KEY, |stage| {
                    if stage == Stage::TempSynced {
                        let temp = fs::read_dir(p.join(DIRECTORY))
                            .unwrap()
                            .map(|e| e.unwrap().path())
                            .find(|p| p.extension().is_some_and(|e| e == "tmp"))
                            .unwrap();
                        fs::rename(&temp, p.join("original-private-bytes")).unwrap();
                        fs::write(&temp, &foreign).unwrap();
                        replacement = Some(temp);
                        if fail_before_publication {
                            return Err(failure());
                        }
                    }
                    Ok(())
                })
                .unwrap_err();
            assert!(!error.uncertain_commit);
            assert!(error.temporary_leftover.is_some());
            assert_eq!(fs::read(replacement.unwrap()).unwrap(), foreign);
            assert_eq!(
                fs::read(p.join("original-private-bytes")).unwrap(),
                serde_json::to_vec(&original).unwrap()
            );
            assert!(!p.join(DIRECTORY).join(format!("{KEY}.json")).exists());
            if !fail_before_publication {
                assert_eq!(error.kind, ErrorKind::ChangedContent);
            }
        }
    }
}

#[test]
fn publication_consumes_temp_and_preserves_later_same_name_entry() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let mut temporary = None;
    let original = account("ra:original");
    let error = store
        .write_inner(&original, KEY, |stage| {
            if stage == Stage::TempChecked {
                temporary = Some(
                    fs::read_dir(p.join(DIRECTORY))
                        .unwrap()
                        .map(|e| e.unwrap().path())
                        .find(|p| p.extension().is_some_and(|e| e == "tmp"))
                        .unwrap(),
                );
            }
            if stage == Stage::Published {
                let temp = temporary.as_ref().unwrap();
                assert!(!temp.exists());
                fs::write(temp, b"unrelated later entry").unwrap();
                return Err(failure());
            }
            Ok(())
        })
        .unwrap_err();
    assert!(error.uncertain_commit);
    assert!(error.temporary_leftover.is_none());
    assert_eq!(
        fs::read(temporary.unwrap()).unwrap(),
        b"unrelated later entry"
    );
    assert_eq!(
        fs::read(p.join(DIRECTORY).join(format!("{KEY}.json"))).unwrap(),
        serde_json::to_vec(&original).unwrap()
    );
    assert_eq!(
        error
            .attempt
            .as_ref()
            .unwrap()
            .observed_final
            .as_ref()
            .unwrap()
            .state,
        "observed"
    );
}

#[test]
fn source_name_race_after_final_check_is_exposed_without_rollback_or_retry() {
    for variant in ["foreign", "identical", "symlink", "directory"] {
        for collision in [false, true] {
            let scratch = Scratch::new();
            let p = scratch.project();
            let store = ProjectRouteStore::open(&p).unwrap();
            let original = account("ra:original");
            let intended = serde_json::to_vec(&original).unwrap();
            let foreign = serde_json::to_vec(&account(if variant == "identical" {
                "ra:original"
            } else {
                "ra:foreign"
            }))
            .unwrap();
            let target = p.join(DIRECTORY).join(format!("{KEY}.json"));
            let saved = p.join("original-aside");
            let mut temporary = None;
            let error = store
                .write_inner(&original, KEY, |stage| {
                    if stage == Stage::TempChecked {
                        let temp = fs::read_dir(p.join(DIRECTORY))
                            .unwrap()
                            .map(|e| e.unwrap().path())
                            .find(|p| p.extension().is_some_and(|e| e == "tmp"))
                            .unwrap();
                        fs::rename(&temp, &saved).unwrap();
                        match variant {
                            "symlink" => {
                                fs::write(p.join("foreign-source"), b"link target preserved")
                                    .unwrap();
                                symlink(p.join("foreign-source"), &temp).unwrap();
                            }
                            "directory" => {
                                fs::create_dir(&temp).unwrap();
                                fs::write(temp.join("preserved"), b"directory content").unwrap();
                            }
                            _ => fs::write(&temp, &foreign).unwrap(),
                        }
                        if collision {
                            fs::write(&target, b"prior target preserved").unwrap();
                        }
                        temporary = Some(temp);
                    }
                    Ok(())
                })
                .unwrap_err();
            assert_eq!(fs::read(&saved).unwrap(), intended);
            let temp = temporary.unwrap();
            if collision {
                assert_eq!(error.kind, ErrorKind::Collision);
                assert!(!error.uncertain_commit);
                assert!(error.temporary_leftover.is_some());
                assert!(fs::symlink_metadata(&temp).is_ok());
                assert_eq!(fs::read(&target).unwrap(), b"prior target preserved");
            } else {
                assert!(error.uncertain_commit);
                assert!(error.temporary_leftover.is_none());
                assert!(fs::symlink_metadata(&temp).is_err()); // exclusive rename moved the foreign source name.
                let observation = error
                    .attempt
                    .as_ref()
                    .unwrap()
                    .observed_final
                    .as_ref()
                    .unwrap();
                match variant {
                    "symlink" => {
                        assert!(fs::symlink_metadata(&target)
                            .unwrap()
                            .file_type()
                            .is_symlink());
                        assert_eq!(
                            fs::read(p.join("foreign-source")).unwrap(),
                            b"link target preserved"
                        );
                        assert_eq!(observation.state, "unreadable");
                    }
                    "directory" => {
                        assert_eq!(
                            fs::read(target.join("preserved")).unwrap(),
                            b"directory content"
                        );
                        assert_eq!(observation.file_type.as_deref(), Some("nonregular"));
                    }
                    _ => {
                        assert_eq!(fs::read(&target).unwrap(), foreign);
                        assert_eq!(
                            observation.sha256.as_deref(),
                            Some(crate::util::sha256_hex(&foreign).as_str())
                        );
                        assert_ne!(observation.file, error.attempt.as_ref().unwrap().file);
                        let discovered = store.discover();
                        assert_eq!(discovered.accounts.len(), 1);
                        // A schema-valid foreign discovery is only inspected content;
                        // it cannot reconcile the original writer's binding.
                    }
                }
                assert!(store.reconcile(error.attempt.as_ref().unwrap()).is_err());
            }
        }
    }
}

#[test]
fn observed_nonregular_source_substitutions_refuse_before_publication() {
    for variant in ["symlink", "directory", "missing"] {
        let scratch = Scratch::new();
        let p = scratch.project();
        let store = ProjectRouteStore::open(&p).unwrap();
        let mut replacement = None;
        let error = store
            .write_inner(&account("ra:original"), KEY, |stage| {
                if stage == Stage::TempSynced {
                    let temp = fs::read_dir(p.join(DIRECTORY))
                        .unwrap()
                        .map(|e| e.unwrap().path())
                        .find(|p| p.extension().is_some_and(|e| e == "tmp"))
                        .unwrap();
                    fs::rename(&temp, p.join("original-aside")).unwrap();
                    match variant {
                        "symlink" => symlink(p.join("original-aside"), &temp).unwrap(),
                        "directory" => fs::create_dir(&temp).unwrap(),
                        _ => {}
                    }
                    replacement = Some(temp);
                }
                Ok(())
            })
            .unwrap_err();
        assert!(!error.uncertain_commit);
        assert!(error.temporary_leftover.is_some());
        assert!(!p.join(DIRECTORY).join(format!("{KEY}.json")).exists());
        assert_eq!(
            fs::symlink_metadata(replacement.unwrap()).is_ok(),
            variant != "missing"
        );
        assert!(p.join("original-aside").exists());
    }
}

#[test]
fn unsupported_exclusive_rename_flag_refuses_without_fallback() {
    use std::os::fd::AsRawFd;
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let error = store
        .write_using(
            &account("ra:unsupported"),
            KEY,
            |_| Ok(()),
            |dir, from, to| {
                let from = std::ffi::CString::new(from).unwrap();
                let to = std::ffi::CString::new(to).unwrap();
                #[cfg(target_os = "macos")]
                let rc = unsafe {
                    libc::renameatx_np(
                        dir.as_raw_fd(),
                        from.as_ptr(),
                        dir.as_raw_fd(),
                        to.as_ptr(),
                        0x8000_0000,
                    )
                };
                #[cfg(target_os = "linux")]
                let rc = unsafe {
                    libc::renameat2(
                        dir.as_raw_fd(),
                        from.as_ptr(),
                        dir.as_raw_fd(),
                        to.as_ptr(),
                        0x8000_0000,
                    )
                };
                assert_eq!(rc, -1);
                Err(std::io::Error::last_os_error())
            },
        )
        .unwrap_err();
    assert_eq!(error.kind, ErrorKind::UnsupportedCapability);
    assert!(!error.uncertain_commit);
    assert!(error.temporary_leftover.is_some());
    assert!(!p.join(DIRECTORY).join(format!("{KEY}.json")).exists());
    assert_eq!(fs::read_dir(p.join(DIRECTORY)).unwrap().count(), 1);
}

#[test]
fn ambiguous_syscall_failure_reports_absent_observation_and_retains_temporary() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open(&p).unwrap();
    let error = store
        .write_using(
            &account("ra:ambiguous"),
            KEY,
            |_| Ok(()),
            |_, _, _| Err(std::io::Error::from_raw_os_error(libc::EIO)),
        )
        .unwrap_err();
    assert!(error.uncertain_commit);
    assert!(error.temporary_leftover.is_some());
    let attempt = error.attempt.as_ref().unwrap();
    assert_eq!(attempt.observed_final.as_ref().unwrap().state, "absent");
    assert!(p.join(&attempt.temporary_relative_path).exists());
    assert!(attempt.file.is_some());
    assert!(!p.join(&attempt.relative_path).exists());
    assert_eq!(
        store.reconcile(attempt).unwrap_err().kind,
        ErrorKind::Missing
    );
}
