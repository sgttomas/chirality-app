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
    let design = Path::new(env!("CARGO_MANIFEST_DIR")).join("../../execution/PKG-07/DEL-07-02/Design");
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let r1 = store.write(&v1).unwrap();
    let r2 = store.write(&v2).unwrap();
    drop(store);
    let cold = ProjectRouteStore::open_for_write(&p).unwrap();
    assert_eq!(cold.resolve(&r1).unwrap().account, v1);
    assert_eq!(cold.resolve(&r2).unwrap().account, v2);
    let mut mislabeled = v2.clone();
    mislabeled["formatVersion"] = json!("0.3");
    assert_eq!(
        validate_account(&mislabeled).unwrap_err().kind,
        ErrorKind::InvalidAccount
    );
    for bad in ["0.5", "", "1"] {
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
    let store = ProjectRouteStore::open_for_write(&alias).unwrap();
    assert_eq!(store.resolved_project(), p);
    let data = account("ra:unrelated-governed-id");
    let reference = store.write(&data).unwrap();
    assert!(canonical_name(
        reference.relative_path.rsplit('/').next().unwrap()
    ));
    assert!(!reference.relative_path.contains("unrelated"));
    assert_eq!(
        fs::read(store.anchor().join(&reference.relative_path)).unwrap(),
        serde_json::to_vec(&data).unwrap()
    );
    let moved = scratch.0.join("moved");
    fs::rename(&p, &moved).unwrap();
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::LocationMismatch
    );
    // RS §13.8: a moved project attaches nothing until the person adopts it.
    let unadopted = ProjectRouteStore::open(&moved).unwrap();
    assert!(unadopted.discover().directory_absent, "read in place: nothing there");
    assert!(unadopted.location().contains("nothing written"), "{}", unadopted.location());
    crate::records_store::adopt(&moved).unwrap();
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
    // Reading mints no project identity (RS §13.8): nothing is created.
    let reader = ProjectRouteStore::open(&p).unwrap();
    let mut invalid = account("../../escape");
    assert!(reader.write(&invalid).is_err());
    assert!(!p.join(".chirality").exists());
    assert!(reader.discover().directory_absent);
    assert!(!p.join(".chirality").exists());
    // A reader opened with no identity in the store writes nowhere.
    let refused = reader.write(&account("ra:test")).unwrap_err();
    assert_eq!(refused.kind, ErrorKind::RecordingRefused, "{refused}");
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    invalid = account("ra:test");
    invalid["format"] = json!("wrong");
    assert!(store.write(&invalid).is_err());
    assert!(!store.accounts_directory().exists(), "an invalid account creates no folder");
    assert!(!p.join(".chirality/records").exists(), "and nothing in the project but its identity link");
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let reference = store
        .write_inner(&account("ra:first"), KEY, |_| Ok(()))
        .unwrap();
    let bytes = fs::read(store.anchor().join(&reference.relative_path)).unwrap();
    for _ in 0..2 {
        let err = store
            .write_inner(&account("ra:second"), KEY, |_| Ok(()))
            .unwrap_err();
        assert_eq!(err.kind, ErrorKind::Collision);
        assert!(!err.uncertain_commit);
        assert!(err.temporary_leftover.is_some());
        assert_eq!(fs::read(store.anchor().join(&reference.relative_path)).unwrap(), bytes);
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    assert!(store.discover().directory_absent);
    let reference = store.write(&account("ra:duplicate")).unwrap();
    store.write(&account("ra:duplicate")).unwrap();
    assert_eq!(
        store.resolve(&reference).unwrap_err().kind,
        ErrorKind::DuplicateIdentity
    );
    let d = store.accounts_directory();
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
        store.anchor().join(&reference.relative_path),
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
    // The account folder chain in the records store below the project's own
    // store folder (`connectors`, `route-accounts`).
    for depth in 0..2 {
        for link in [true, false] {
            let scratch = Scratch::new();
            let p = scratch.project();
            let outside = scratch.0.join("outside");
            fs::create_dir(&outside).unwrap();
            let store = ProjectRouteStore::open_for_write(&p).unwrap();
            let accounts = store.accounts_directory();
            let parts = [accounts.parent().unwrap().to_path_buf(), accounts.clone()];
            if depth == 1 {
                fs::create_dir_all(&parts[0]).unwrap();
            }
            let target = &parts[depth];
            if link {
                symlink(&outside, target).unwrap();
            } else {
                fs::write(target, b"not a directory").unwrap();
            }
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let reference = store.write(&account("ra:test")).unwrap();
    let target = store.accounts_directory().join(format!("{KEY}.json"));
    symlink(store.anchor().join(&reference.relative_path), &target).unwrap();
    let err = store
        .write_inner(&account("ra:other"), KEY, |_| Ok(()))
        .unwrap_err();
    assert_eq!(err.kind, ErrorKind::Collision);
    fs::remove_file(&target).unwrap();
    fs::hard_link(store.anchor().join(&reference.relative_path), &target).unwrap();
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
    let file = store.anchor().join(&reference.relative_path);
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    store.write(&account("ra:first")).unwrap();
    let d = store.accounts_directory();
    fs::set_permissions(&d, fs::Permissions::from_mode(0o500)).unwrap();
    let result = store.write(&account("ra:blocked"));
    fs::set_permissions(&d, fs::Permissions::from_mode(0o700)).unwrap();
    let error = result.unwrap_err();
    assert!(!error.uncertain_commit);
    assert_eq!(store.discover().accounts.len(), 1);
}
#[test]
fn real_rename_race_retains_capability_reports_uncertainty_and_reconciles() {
    for depth in 0..3 {
        let scratch = Scratch::new();
        let p = scratch.project();
        let store = ProjectRouteStore::open_for_write(&p).unwrap();
        // The project's store folder, `connectors` or `route-accounts`, made
        // by a first account so each exists before the race.
        store.write(&account("ra:before")).unwrap();
        let accounts = store.accounts_directory();
        let chain = [accounts.parent().unwrap().parent().unwrap().to_path_buf(), accounts.parent().unwrap().to_path_buf(), accounts.clone()];
        let original = chain[depth].clone();
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
        let published = moved.join(accounts.strip_prefix(&original).unwrap()).join(format!("{KEY}.json"));
        assert_eq!(
            crate::util::sha256_hex(&fs::read(&published).unwrap()),
            err.attempt.as_ref().unwrap().sha256
        );
        assert!(store.reconcile(err.attempt.as_ref().unwrap()).is_err());
        fs::remove_dir(&original).unwrap();
        fs::rename(&moved, &original).unwrap();
        let cold = ProjectRouteStore::open_for_write(&p).unwrap();
        assert_eq!(
            cold.reconcile(err.attempt.as_ref().unwrap())
                .unwrap()
                .account["account_id"],
            "ra:race"
        );
        assert_eq!(cold.discover().accounts.len(), 2); // the first, and no automatic retry.
    }
}
#[test]
fn prewrite_substitution_aborts_and_transient_move_is_not_continuous_containment() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let d = store.accounts_directory();
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
        let store = ProjectRouteStore::open_for_write(&p).unwrap();
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
            assert!(!store.accounts_directory().join(format!("{KEY}.json")).exists());
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
                    let store = ProjectRouteStore::open_for_write(&p).unwrap();
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
        let store = ProjectRouteStore::open_for_write(&p).unwrap();
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let mut reference = store.write(&account("ra:legacy")).unwrap();
    // An explicitly supplied binding outside the canonical account folder (one
    // folder up, in the project's store folder) is read at that path only.
    let elsewhere = store.accounts_directory().parent().unwrap().join("legacy.json");
    fs::rename(store.anchor().join(&reference.relative_path), &elsewhere).unwrap();
    let mut parts: Vec<&str> = reference.relative_path.split('/').collect();
    parts.truncate(parts.len() - 2);
    reference.relative_path = format!("{}/legacy.json", parts.join("/"));
    reference.directories.truncate(reference.directories.len() - 1);
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
            // The child writes in this process's records store.
            .env(crate::records_store::OVERRIDE_ENV, crate::records_store::store_root().unwrap())
            .status()
            .unwrap();
        assert_eq!(status.code(), Some(73));
        let store = ProjectRouteStore::open_for_write(&p).unwrap();
        let d = store.discover();
        assert_eq!(
            d.issues
                .iter()
                .any(|i| i.kind == ErrorKind::TemporaryLeftover),
            phase == "before"
        );
        let target = store.accounts_directory().join(format!("{KEY}.json"));
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
    let store = ProjectRouteStore::open_for_write(Path::new(&project)).unwrap();
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
        let store = ProjectRouteStore::open_for_write(&p).unwrap();
        let target = store.accounts_directory().join(format!("{KEY}.json"));
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
        assert_eq!(fs::read_dir(store.accounts_directory()).unwrap().count(), 1);
    }
}

#[test]
fn postpublication_symlink_substitution_never_follows_replacement() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let d = store.accounts_directory();
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let d = store.accounts_directory();
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
            let store = ProjectRouteStore::open_for_write(&p).unwrap();
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
                        let temp = fs::read_dir(store.accounts_directory())
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
            assert!(!store.accounts_directory().join(format!("{KEY}.json")).exists());
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let mut temporary = None;
    let original = account("ra:original");
    let error = store
        .write_inner(&original, KEY, |stage| {
            if stage == Stage::TempChecked {
                temporary = Some(
                    fs::read_dir(store.accounts_directory())
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
        fs::read(store.accounts_directory().join(format!("{KEY}.json"))).unwrap(),
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
            let store = ProjectRouteStore::open_for_write(&p).unwrap();
            let original = account("ra:original");
            let intended = serde_json::to_vec(&original).unwrap();
            let foreign = serde_json::to_vec(&account(if variant == "identical" {
                "ra:original"
            } else {
                "ra:foreign"
            }))
            .unwrap();
            let target = store.accounts_directory().join(format!("{KEY}.json"));
            let saved = p.join("original-aside");
            let mut temporary = None;
            let error = store
                .write_inner(&original, KEY, |stage| {
                    if stage == Stage::TempChecked {
                        let temp = fs::read_dir(store.accounts_directory())
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
        let store = ProjectRouteStore::open_for_write(&p).unwrap();
        let mut replacement = None;
        let error = store
            .write_inner(&account("ra:original"), KEY, |stage| {
                if stage == Stage::TempSynced {
                    let temp = fs::read_dir(store.accounts_directory())
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
        assert!(!store.accounts_directory().join(format!("{KEY}.json")).exists());
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
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
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
    assert!(!store.accounts_directory().join(format!("{KEY}.json")).exists());
    assert_eq!(fs::read_dir(store.accounts_directory()).unwrap().count(), 1);
}

#[test]
fn ambiguous_syscall_failure_reports_absent_observation_and_retains_temporary() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
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
    assert!(store.anchor().join(&attempt.temporary_relative_path).exists());
    assert!(attempt.file.is_some());
    assert!(!store.anchor().join(&attempt.relative_path).exists());
    assert_eq!(
        store.reconcile(attempt).unwrap_err().kind,
        ErrorKind::Missing
    );
}

fn inspection_fixture() -> (Scratch, PathBuf, ProjectRouteStore, BoundReference) {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    let binding = store
        .write(&crate::connector_materialization::tests::direct_account())
        .unwrap();
    (scratch, p, store, binding)
}
#[test]
fn published_inspection_direct_only_ignores_hostile_unrelated_and_duplicate_accounts() {
    let (_scratch, p, store, binding) = inspection_fixture();
    let dir = store.accounts_directory();
    let unrelated = fs::File::create(dir.join("unrelated-large.json")).unwrap();
    unrelated.set_len(64 * 1024 * 1024).unwrap();
    fs::copy(
        store.anchor().join(&binding.relative_path),
        dir.join(format!("{KEY}.json")),
    )
    .unwrap();
    let (result, operations) =
        super::platform::audit_inspection(|| store.inspect_published(&binding, &p));
    println!("direct inspection acquisition accounting: {operations:?}");
    assert_eq!(result["status"], "current_match");
    assert!(
        operations
            .iter()
            .all(|x| x != "enumerate" && !x.contains("unrelated-large") && !x.contains(KEY)),
        "{operations:?}"
    );
    assert!(
        store.resolve(&binding).is_err(),
        "full resolver still detects ambiguity"
    );
}
#[test]
fn published_inspection_missing_replaced_links_fifo_and_root_refusals() {
    for kind in 0..6 {
        let (_scratch, p, store, binding) = inspection_fixture();
        let path = store.anchor().join(&binding.relative_path);
        let saved = path.with_extension("saved");
        fs::rename(&path, &saved).unwrap();
        match kind {
            0 => {}
            1 => {
                fs::copy(&saved, &path).unwrap();
            }
            2 => {
                symlink(&saved, &path).unwrap();
            }
            3 => {
                fs::hard_link(&saved, &path).unwrap();
            }
            4 => {
                use std::os::unix::ffi::OsStrExt;
                let name = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
                assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
            }
            _ => {
                fs::rename(&saved, &path).unwrap();
                let moved = p.with_extension("moved");
                fs::rename(&p, &moved).unwrap();
                fs::create_dir(&p).unwrap();
            }
        }
        let result = store.inspect_published(&binding, &p);
        assert_eq!(
            result["status"],
            match kind {
                0 => "missing",
                1 | 5 => "changed",
                _ => "unsafe",
            },
            "{kind}: {result}"
        );
    }
}
#[test]
fn published_inspection_actual_growth_sentinel_and_io_error_are_unavailable() {
    use super::platform::InspectionStep;
    let (_scratch, p, store, binding) = inspection_fixture();
    let grown = store.inspect_published_with(&binding, &p, |step| {
        if step == InspectionStep::BeforeRead {
            fs::OpenOptions::new()
                .write(true)
                .open(store.anchor().join(&binding.relative_path))?
                .set_len((crate::connector_materialization::BYTE_LIMIT + 1) as u64)?;
        }
        Ok(())
    });
    assert_eq!(grown["status"], "unavailable");
    let failure = store.inspect_published_with(&binding, &p, |_| {
        Err(std::io::Error::from_raw_os_error(libc::EMFILE))
    });
    assert_eq!(failure["status"], "unavailable");
    assert!(failure["detail"]
        .as_str()
        .unwrap()
        .contains("inspection read"));
}
#[test]
fn published_inspection_post_read_replacement_and_ancestor_change_are_not_match() {
    use super::platform::InspectionStep;
    for ancestor in [false, true] {
        let (_scratch, p, store, binding) = inspection_fixture();
        let result = store.inspect_published_with(&binding, &p, |step| {
            if step == InspectionStep::BeforePostcheck {
                let path = if ancestor {
                    store.accounts_directory().parent().unwrap().to_path_buf()
                } else {
                    store.anchor().join(&binding.relative_path)
                };
                let moved = path.with_extension("moved");
                fs::rename(&path, &moved)?;
                if ancestor {
                    fs::create_dir(&path)?;
                } else {
                    fs::copy(&moved, &path)?;
                }
            }
            Ok(())
        });
        assert_eq!(result["status"], "changed");
    }
}
#[test]
fn published_inspection_strict_json_and_semantic_checks_not_just_matching_hash() {
    for bytes in [
        b"{\"formatVersion\":\"0.3\",\"formatVersion\":\"0.3\"}".to_vec(),
        vec![b'['; 200],
        b"{\"formatVersion\":\"0.3\",\"account_id\":\"wrong\"}".to_vec(),
    ] {
        let (_scratch, p, store, mut binding) = inspection_fixture();
        fs::write(store.anchor().join(&binding.relative_path), &bytes).unwrap();
        binding.sha256 = crate::util::sha256_hex(&bytes);
        assert_eq!(store.inspect_published(&binding, &p)["status"], "changed");
    }
    let (_scratch, p, store, mut binding) = inspection_fixture();
    for version in ["0.1", "0.2", "0.5"] {
        binding.format_version = version.into();
        assert_eq!(
            store.inspect_published(&binding, &p)["status"],
            "unavailable"
        );
    }
}

#[test]
fn published_inspection_unsafe_ancestors_and_valid_deep_json_refuse() {
    for kind in 0..3 {
        let (_scratch, p, store, binding) = inspection_fixture();
        let ancestor = store.accounts_directory().parent().unwrap().to_path_buf();
        let saved = ancestor.with_extension("saved-control");
        fs::rename(&ancestor, &saved).unwrap();
        match kind {
            0 => symlink(&saved, &ancestor).unwrap(),
            1 => {
                fs::write(&ancestor, b"not directory").unwrap();
            }
            _ => {
                use std::os::unix::ffi::OsStrExt;
                let name = std::ffi::CString::new(ancestor.as_os_str().as_bytes()).unwrap();
                assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
            }
        }
        assert_eq!(store.inspect_published(&binding, &p)["status"], "unsafe");
    }
    let (_scratch, p, store, mut binding) = inspection_fixture();
    let bytes = format!("{}0{}", "[".repeat(200), "]".repeat(200)).into_bytes();
    fs::write(store.anchor().join(&binding.relative_path), &bytes).unwrap();
    binding.sha256 = crate::util::sha256_hex(&bytes);
    let result = store.inspect_published(&binding, &p);
    assert_eq!(result["status"], "changed");
    assert!(result["detail"].as_str().unwrap().contains("depth"));
}

#[test]
fn published_inspection_hash_then_private_binding_semantic_version_checks() {
    let (_scratch, p, store, mut binding) = inspection_fixture();
    let path = store.anchor().join(&binding.relative_path);
    let mut account: Value = serde_json::from_slice(&fs::read(&path).unwrap()).unwrap();
    account["duties"][1] = account["duties"][0].clone();
    let bytes = serde_json::to_vec(&account).unwrap();
    fs::write(&path, &bytes).unwrap();
    let actual = store.inspect_published(&binding, &p);
    assert_eq!(actual["status"], "changed");
    assert!(actual["detail"].as_str().unwrap().contains("raw account hash"));
    // Only a private test reference is altered to reach validation after hash comparison.
    // The production command accepts no reference or account bytes from its caller.
    binding.sha256 = crate::util::sha256_hex(&bytes);
    let semantic = store.inspect_published(&binding, &p);
    assert_eq!(semantic["status"], "changed");
    assert!(semantic["detail"].as_str().unwrap().contains("semantic/schema"));
    account["formatVersion"] = json!("0.4");
    let bytes = serde_json::to_vec(&account).unwrap();
    fs::write(&path, &bytes).unwrap();
    binding.sha256 = crate::util::sha256_hex(&bytes);
    assert!(store.inspect_published(&binding, &p)["detail"].as_str().unwrap().contains("ID/version"));
}

// ---- RS §13.8 "Split by who writes": accounts in the records store ----

/// An account an earlier build wrote in the project, at its earlier place.
fn legacy_account(p: &Path, name: &str, data: &Value) -> PathBuf {
    let dir = p.join(LEGACY_DIRECTORY);
    fs::create_dir_all(&dir).unwrap();
    let path = dir.join(name);
    fs::write(&path, serde_json::to_vec(data).unwrap()).unwrap();
    path
}
fn snapshot(dir: &Path) -> BTreeMap<String, Vec<u8>> {
    fs::read_dir(dir)
        .unwrap()
        .map(|e| {
            let e = e.unwrap();
            (e.file_name().to_string_lossy().into_owned(), fs::read(e.path()).unwrap_or_default())
        })
        .collect()
}
#[test]
fn accounts_in_the_project_are_read_in_place_until_imported_then_only_from_the_store() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let data = account("ra:legacy");
    legacy_account(&p, &format!("{KEY}.json"), &data);
    fs::write(p.join(LEGACY_DIRECTORY).join(".route-interrupted.tmp"), b"partial").unwrap();
    let originals = snapshot(&p.join(LEGACY_DIRECTORY));
    // Before the import: read in place; nothing written anywhere.
    let in_place = ProjectRouteStore::open(&p).unwrap();
    assert!(in_place.location().contains("import needed"), "{}", in_place.location());
    let before = in_place.discover();
    assert_eq!(before.accounts.len(), 1);
    assert!(before.issues.iter().any(|i| i.kind == ErrorKind::TemporaryLeftover));
    let held = before.accounts[0].reference.clone();
    assert!(held.relative_path.starts_with(LEGACY_DIRECTORY));
    assert_eq!(in_place.resolve(&held).unwrap().account, data);
    let refused = in_place.write(&account("ra:new")).unwrap_err();
    assert_eq!(refused.kind, ErrorKind::RecordingRefused);
    assert!(refused.detail.contains("import needed"), "{refused}");
    let refused = ProjectRouteStore::open_for_write(&p).unwrap_err();
    assert!(refused.detail.contains("import needed"), "{refused}");
    // The accounts are project history like the §13.7 records: no other
    // recording until they are imported either.
    assert!(crate::records_store::write_dir(&p).unwrap_err().contains("import needed"));
    // The import copies both entries byte for byte; the originals stay.
    let imported = crate::records_store::import(&p).unwrap();
    assert_eq!((imported["state"].as_str(), imported["copied"].as_u64()), (Some("imported"), Some(2)), "{imported}");
    assert_eq!(snapshot(&p.join(LEGACY_DIRECTORY)), originals, "originals never rewritten or deleted");
    let store = ProjectRouteStore::open(&p).unwrap();
    assert!(store.location().contains("records store"), "{}", store.location());
    assert_eq!(snapshot(&store.accounts_directory()), originals, "byte-identical copies");
    let after = store.discover();
    assert_eq!(after.accounts.len(), 1, "read once, from the store");
    assert!(after.issues.iter().any(|i| i.kind == ErrorKind::TemporaryLeftover), "the leftover is still shown");
    let fresh = after.accounts[0].reference.clone();
    assert!(fresh.relative_path.starts_with("projects/"));
    assert_eq!(fresh.sha256, held.sha256);
    // A binding taken before the import names the original: explicit
    // reconciliation, never silently the copy.
    let mismatch = store.resolve(&held).unwrap_err();
    assert_eq!(mismatch.kind, ErrorKind::LocationMismatch);
    assert!(mismatch.detail.contains("reconcile explicitly"), "{mismatch}");
    assert_eq!(store.resolve(&fresh).unwrap().account, data);
    // Writes go to the store now, never to the project.
    let writer = ProjectRouteStore::open_for_write(&p).unwrap();
    let written = writer.write(&account("ra:new")).unwrap();
    assert_eq!(writer.resolve(&written).unwrap().account["account_id"], "ra:new");
    assert_eq!(snapshot(&p.join(LEGACY_DIRECTORY)), originals);
    // An account that appears in the project later is not read; it is a note.
    legacy_account(&p, "22345678-1234-4234-8234-123456789abc.json", &account("ra:late"));
    assert_eq!(ProjectRouteStore::open(&p).unwrap().discover().accounts.len(), 2);
    let notes = crate::records_store::notes(&p);
    assert!(notes.iter().any(|n| n.contains("22345678-1234-4234-8234-123456789abc.json") && n.contains("not read")), "{notes:?}");
}
#[test]
fn unsafe_account_entries_are_never_imported_as_clean_copies() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let good = legacy_account(&p, &format!("{KEY}.json"), &account("ra:good"));
    let linked = p.join(LEGACY_DIRECTORY).join("22345678-1234-4234-8234-123456789abc.json");
    fs::hard_link(&good, scratch.0.join("second-link")).unwrap();
    symlink(&good, &linked).unwrap();
    let in_place = ProjectRouteStore::open(&p).unwrap().discover();
    assert_eq!(in_place.accounts.len(), 0, "in place, the hard-linked file and the link are both refused");
    let imported = crate::records_store::import(&p).unwrap();
    let conflicts = imported["conflicts"].to_string();
    assert!(conflicts.contains("hard-linked") && conflicts.contains("symbolic link"), "{imported}");
    assert_eq!(imported["copied"], 0);
    let store = ProjectRouteStore::open(&p).unwrap();
    assert!(!store.accounts_directory().exists(), "nothing copied");
    assert!(store.discover().accounts.is_empty());
    // Repeating the import records nothing new for the same refusals.
    let again = crate::records_store::import(&p).unwrap();
    assert!(again["importId"].is_null(), "{again}");
    assert!(crate::records_store::notes(&p).iter().filter(|n| n.contains("not read")).count() >= 2);
}
#[test]
fn an_unavailable_records_store_reads_in_place_refuses_writes_and_relocates_nothing() {
    let scratch = Scratch::new();
    let p = scratch.project();
    legacy_account(&p, &format!("{KEY}.json"), &account("ra:legacy"));
    let before = snapshot(&p.join(LEGACY_DIRECTORY));
    crate::records_store::use_store_for_test(Some(Err("no records store configured".into())));
    // As the §13.7 records: a folder with no link is read in place.
    let reader = ProjectRouteStore::open(&p).unwrap();
    let discovery = reader.discover();
    let write = reader.write(&account("ra:new")).unwrap_err();
    let for_write = ProjectRouteStore::open_for_write(&p).unwrap_err();
    crate::records_store::use_store_for_test(None);
    assert_eq!(discovery.accounts.len(), 1);
    assert!(discovery.location.contains("records store unavailable"), "{}", discovery.location);
    for e in [write, for_write] {
        assert_eq!(e.kind, ErrorKind::RecordingRefused);
        assert!(e.detail.contains("records store unavailable"), "{e}");
    }
    assert_eq!(snapshot(&p.join(LEGACY_DIRECTORY)), before, "nothing written in the project");
    assert!(!p.join(crate::records_store::PROJECT_LINK).exists());
    // A linked project with the store unavailable is an error, not read in place.
    let linked = scratch.0.join("linked");
    fs::create_dir(&linked).unwrap();
    crate::records_store::attach(&linked, true).unwrap();
    crate::records_store::use_store_for_test(Some(Err("no records store configured".into())));
    let refused = ProjectRouteStore::open(&linked).unwrap_err();
    crate::records_store::use_store_for_test(None);
    assert_eq!(refused.kind, ErrorKind::RecordingRefused);
}
/// A writer that passed the permission check and then waited behind an
/// import that stopped after its "started" line writes nothing: the
/// permission is checked again once the writer lock is held.
#[test]
fn a_writer_waiting_behind_an_import_that_did_not_complete_writes_nothing() {
    let scratch = Scratch::new();
    let p = scratch.project();
    let store = ProjectRouteStore::open_for_write(&p).unwrap();
    store.write(&account("ra:first")).unwrap();
    let dir = store.accounts_directory().parent().unwrap().parent().unwrap().to_path_buf();
    // Held as an import holds it, exclusively.
    let import_lock = crate::storage::lock(&dir.join(".writer.lock")).unwrap();
    let writer = std::thread::spawn(move || store.write(&account("ra:waiting")));
    std::thread::sleep(std::time::Duration::from_millis(400));
    // The import stops after its "started" line (a late import: the store held the records).
    let line = json!({"format":"chirality.records-store.import","formatVersion":"0.1","event":"started","importId":"import:interrupted","at":"2026-10-12T00:00:00.000Z","root":p.display().to_string(),"method":"sha-256 of the exact bytes","census":[],"storeHeld":true,"resumes":null});
    let mut text = serde_json::to_vec(&line).unwrap();
    text.push(b'\n');
    use std::io::Write as _;
    fs::OpenOptions::new().create(true).append(true).open(dir.join("imports.jsonl")).unwrap().write_all(&text).unwrap();
    drop(import_lock);
    let refused = writer.join().unwrap().unwrap_err();
    assert_eq!(refused.kind, ErrorKind::RecordingRefused, "{refused}");
    assert!(refused.detail.contains("import incomplete"), "{refused}");
    let reader = ProjectRouteStore::open(&p).unwrap();
    assert_eq!(reader.discover().accounts.len(), 1, "only the first account");
}
