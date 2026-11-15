use super::*;
use std::sync::Mutex;
use std::os::unix::fs::PermissionsExt;
#[derive(Default)]
struct Mock {
    items: Mutex<BTreeMap<String, Vec<u8>>>,
    reads: Mutex<Vec<ItemIdentity>>,
    adds: Mutex<usize>,
    read_error: Mutex<Option<BackendError>>,
    read_errors: Mutex<BTreeMap<String, BackendError>>,
    add_mode: Mutex<u8>,
}
fn name(i: &ItemIdentity) -> String {
    format!("{}|{}|{}", i.service, i.account, i.access_group)
}
impl Backend for Mock {
    fn read(&self, i: &ItemIdentity) -> Result<Vec<u8>, BackendError> {
        self.reads.lock().unwrap().push(i.clone());
        if let Some(error) = self.read_error.lock().unwrap().clone() {
            return Err(error);
        }
        if let Some(error) = self.read_errors.lock().unwrap().get(&name(i)).cloned() { return Err(error) }
        self.items
            .lock()
            .unwrap()
            .get(&name(i))
            .cloned()
            .ok_or(BackendError::Missing)
    }
    fn add(&self, i: &ItemIdentity, bytes: &[u8]) -> Result<(), BackendError> {
        *self.adds.lock().unwrap() += 1;
        let mode = *self.add_mode.lock().unwrap();
        if mode == 1 {
            return Err(BackendError::Unavailable(-25308));
        }
        if mode == 3 {
            return Err(BackendError::Duplicate);
        }
        let mut items = self.items.lock().unwrap();
        if items.contains_key(&name(i)) {
            return Err(BackendError::Duplicate);
        }
        items.insert(
            name(i),
            if mode == 4 {
                vec![7; 32]
            } else {
                bytes.to_vec()
            },
        );
        if mode == 2 {
            return Err(BackendError::Unavailable(-1));
        }
        Ok(())
    }
}
struct Fixture {
    root: PathBuf,
    dir: PathBuf,
    legacy: PathBuf,
    identity: ItemIdentity,
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("seal-keychain-").unwrap());
        fs::create_dir(&root).unwrap();
        Self {
            dir: root.join("continuity"),
            legacy: root.join("legacy"),
            root,
            identity: ItemIdentity {
                service: "invalid.example.seal-c".into(),
                account: "synthetic-installation".into(),
                access_group: "SYNTHETIC0.invalid.example.group".into(),
            },
        }
    }
    fn run(&self, b: &Mock, o: Operation, key: u8) -> Result<Material, EvidenceFailure> {
        operate(
            &self.dir,
            &self.legacy,
            &self.identity,
            true,
            b,
            o,
            &mut || Ok([key; 32]),
        )
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.root);
    }
}
#[test]
fn seal_keychain_selection_is_exact_own_app_namespace() {
    let s = KEYCHAIN_SELECTION.as_ref().expect("selected source namespace");
    assert_eq!(s.bundle_identifier, "com.chirality.app");
    assert_eq!(s.team_identifier, "8A7JL35U4S");
    assert_eq!(s.service, "com.chirality.app.v4.capture-seal");
    assert_eq!(s.account, "installation-keyring");
    // Default own-App group: exactly <prefix>.<bundle>, never a wildcard or shared group.
    assert_eq!(s.access_group, format!("{}.{}", s.team_identifier, s.bundle_identifier));
    assert!(s.allow_first_enrollment);
    validate_identity(&ItemIdentity {
        service: s.service.into(),
        account: s.account.into(),
        access_group: s.access_group.into(),
    })
    .unwrap();
}
#[test]
fn seal_keychain_unselected_publisher_never_touches_platform_and_file_route_stays() {
    // Source selection is present, but test builds can never compile a publisher
    // selection, so authority, the keychain route and enrollment stay unavailable.
    assert!(KEYCHAIN_SELECTION.is_some());
    assert!(!cfg!(chirality_publisher_selected));
    assert!(!enrollment_compiled_available());
    assert!(KeychainAuthority::current().is_err());
    assert!(!selected_route());
    assert!(prepare_enrollment().is_err());
    assert!(dispatch(Path::new("/must-not-read/legacy"), Operation::Seal).is_none());
}
#[test]
fn seal_keychain_new_enrollment_rotation_retains_prior_keys_without_file_secrets() {
    let f = Fixture::new();
    let b = Mock::default();
    let first = f.run(&b, Operation::Enroll, 1).unwrap();
    assert_eq!(first.keys[&first.current], [1; 32]);
    let second = f.run(&b, Operation::Rotate, 2).unwrap();
    assert_eq!(second.keys.len(), 2);
    assert_eq!(second.keys[&first.current], [1; 32]);
    assert_eq!(
        f.run(&b, Operation::Verify, 99).unwrap().current,
        second.current
    );
    assert_eq!(*b.adds.lock().unwrap(), 2);
    let text = fs::read_to_string(f.dir.join(MARKER)).unwrap();
    assert!(!text.contains(&"01".repeat(32)));
    assert!(!text.contains(&"02".repeat(32)));
    assert!(!f.legacy.exists());
    assert_eq!(fs::read_dir(&f.dir).unwrap().count(), 2);
}
#[test]
fn seal_keychain_crash_before_reservation_and_enrollment_loss_never_regenerate() {
    let f = Fixture::new();
    let b = Mock::default();
    // Crash after directory/lock creation but before durable reservation: no add.
    drop(guard(&f.dir, true).unwrap());
    assert!(f.run(&b, Operation::Seal, 1).is_err());
    assert!(f.run(&b, Operation::Rotate, 1).is_err());
    assert_eq!(*b.adds.lock().unwrap(), 0);
    let f = Fixture::new();
    f.run(&b, Operation::Enroll, 1).unwrap();
    fs::remove_file(f.dir.join(MARKER)).unwrap();
    assert!(f.run(&b, Operation::Enroll, 2).is_err());
    assert_eq!(*b.adds.lock().unwrap(), 1);
    // Losing the entire marker directory still hits the fixed primary item.
    fs::remove_dir_all(&f.dir).unwrap();
    assert!(f.run(&b, Operation::Enroll, 2).is_err());
    assert_eq!(*b.adds.lock().unwrap(), 1);
}
#[test]
fn seal_keychain_pending_missing_duplicate_and_unknown_add_outcome() {
    for mode in [1, 2, 3, 4] {
        let f = Fixture::new();
        let b = Mock::default();
        *b.add_mode.lock().unwrap() = mode;
        assert!(f.run(&b, Operation::Enroll, 1).is_err());
        let m = load(&f.dir, &f.identity).unwrap().unwrap();
        assert!(m.pending.is_some());
        assert!(m.keys.is_empty());
        *b.add_mode.lock().unwrap() = 0;
        let recovered = f.run(&b, Operation::Enroll, 9);
        if mode == 2 {
            assert_eq!(recovered.unwrap().keys[&key_id(&[1; 32])], [1; 32]);
        } else {
            assert!(recovered.is_err());
        }
        assert_eq!(*b.adds.lock().unwrap(), 1, "no retry add for mode {mode}");
    }
}
#[test]
fn seal_keychain_crash_after_reservation_add_and_readback_recovery() {
    let f = Fixture::new();
    let b = Mock::default();
    let _guard = guard(&f.dir, true).unwrap();
    let key = [3; 32];
    let reference = keyref(&key);
    let m = Marker {
        format: "capture-seal-keychain-continuity.s1".into(),
        scope_sha256: scope(&f.identity),
        keys: vec![],
        pending: Some(reference),
    };
    publish(&f.dir, &m).unwrap();
    drop(_guard);
    assert!(f.run(&b, Operation::Seal, 4).is_err());
    assert_eq!(*b.adds.lock().unwrap(), 0);
    // Simulate add completed before crash; marker was not committed. Verify does
    // not mutate/recover; write path proves actual bytes then commits them.
    b.items
        .lock()
        .unwrap()
        .insert(name(&f.identity), key.to_vec());
    assert!(f.run(&b, Operation::Verify, 4).is_err());
    assert!(load(&f.dir, &f.identity)
        .unwrap()
        .unwrap()
        .pending
        .is_some());
    assert_eq!(
        f.run(&b, Operation::Enroll, 4).unwrap().current,
        key_id(&key)
    );
    assert_eq!(*b.adds.lock().unwrap(), 0);
}
#[test]
fn seal_keychain_scope_and_unavailable_malformed_items_refuse_without_fallback() {
    let f = Fixture::new();
    let b = Mock::default();
    f.run(&b, Operation::Enroll, 1).unwrap();
    for error in [
        BackendError::Missing,
        BackendError::Unavailable(-25308),
        BackendError::Unavailable(-25293),
        BackendError::Invalid,
    ] {
        *b.read_error.lock().unwrap() = Some(error);
        assert!(f.run(&b, Operation::Verify, 9).is_err());
        assert!(f.run(&b, Operation::Rotate, 9).is_err());
    }
    *b.read_error.lock().unwrap() = None;
    for bad in [vec![], vec![0; 31], vec![2; 32]] {
        b.items.lock().unwrap().insert(name(&f.identity), bad);
        assert!(f.run(&b, Operation::Verify, 9).is_err());
    }
    let mut other = f.identity.clone();
    other.access_group = "OTHER00000.invalid.example.group".into();
    let reads = b.reads.lock().unwrap().len();
    assert!(operate(
        &f.dir,
        &f.legacy,
        &other,
        true,
        &b,
        Operation::Seal,
        &mut || Ok([9; 32])
    )
    .is_err());
    assert_eq!(b.reads.lock().unwrap().len(), reads);
    assert_eq!(*b.adds.lock().unwrap(), 1);
}
#[test]
fn seal_keychain_busy_and_legacy_namespace_refuse_without_key_mutation() {
    let f = Fixture::new();
    let b = Mock::default();
    let lock = guard(&f.dir, true).unwrap();
    assert!(f
        .run(&b, Operation::Verify, 1)
        .err()
        .unwrap()
        .contains("busy"));
    drop(lock);
    assert_eq!(*b.adds.lock().unwrap(), 0);
    let f = Fixture::new();
    fs::create_dir(&f.legacy).unwrap();
    fs::write(
        f.legacy.join("keys.json"),
        b"invented legacy bytes never read",
    )
    .unwrap();
    assert!(f
        .run(&b, Operation::Enroll, 1)
        .err()
        .unwrap()
        .contains("retained file-key source unsafe"));
    assert!(b.reads.lock().unwrap().is_empty());
    assert_eq!(
        fs::read(f.legacy.join("keys.json")).unwrap(),
        b"invented legacy bytes never read"
    );
}
#[test]
fn seal_keychain_rotation_unknown_preserves_old_commit_and_prior_key_ids() {
    let f = Fixture::new();
    let b = Mock::default();
    let first = f.run(&b, Operation::Enroll, 1).unwrap();
    *b.add_mode.lock().unwrap() = 2;
    assert!(f.run(&b, Operation::Rotate, 2).is_err());
    let m = load(&f.dir, &f.identity).unwrap().unwrap();
    assert_eq!(m.keys[0].id, first.current);
    assert!(m.pending.is_some());
    *b.add_mode.lock().unwrap() = 0;
    let next = f.run(&b, Operation::Rotate, 3).unwrap();
    assert_eq!(next.keys.len(), 2);
    assert!(next.keys.contains_key(&first.current));
    assert_eq!(*b.adds.lock().unwrap(), 2);
}

#[test]
fn seal_keychain_real_capture_dispatch_cache_refresh_and_rotation_keep_old_seals() {
    let fixture = std::rc::Rc::new(Fixture::new());
    let backend = std::rc::Rc::new(Mock::default());
    let project = fixture.root.join("project");
    fs::create_dir(&project).unwrap();
    crate::capture_seal::set_folder_for_test(Some(Some(fixture.legacy.clone())));
    let f = fixture.clone();
    let b = backend.clone();
    let counter = std::cell::Cell::new(0u8);
    TEST_PROVIDER.with(|slot| {
        *slot.borrow_mut() = Some(Box::new(move |_, operation| {
            counter.set(counter.get() + 1);
            f.run(&b, operation, counter.get())
        }))
    });
    struct Reset;
    impl Drop for Reset {
        fn drop(&mut self) {
            TEST_PROVIDER.with(|slot| *slot.borrow_mut() = None);
            crate::capture_seal::set_folder_for_test(None);
        }
    }
    let _reset = Reset;
    fixture.run(&backend, Operation::Enroll, 1).unwrap();
    let mut overlapping = serde_json::json!({"captureId":"overlap"});
    assert!(crate::capture_seal::seal(
        &fixture.root.join("capture-seal-keychain"),
        &mut overlapping
    )
    .is_err());
    assert_eq!(*backend.adds.lock().unwrap(), 1);

    let mut capture = serde_json::json!({"captureId":"invented","actKind":"A6","choice":"act"});
    crate::capture_seal::seal(&project, &mut capture).unwrap();
    let original = capture.clone();
    crate::capture_seal::verify(&project, &capture).unwrap();
    let prior_basis = crate::capture_seal::verification_basis(&project);
    *backend.read_error.lock().unwrap() = Some(BackendError::Unavailable(-25308));
    assert_ne!(
        crate::capture_seal::verification_basis(&project),
        prior_basis
    );
    assert!(crate::capture_seal::verify(&project, &capture)
        .err()
        .unwrap()
        .contains("not verified here"));
    let mut unsealed = serde_json::json!({"captureId":"new"});
    let error = crate::capture_seal::seal(&project, &mut unsealed)
        .err()
        .unwrap();
    assert!(crate::capture_seal::unsealed_limit(&error).contains("not counted"));
    assert!(unsealed.get("seal").is_none());
    assert!(!fixture.legacy.exists());
    *backend.read_error.lock().unwrap() = None;
    crate::capture_seal::rotate().unwrap();
    crate::capture_seal::verify(&project, &original).unwrap();
    *backend.add_mode.lock().unwrap() = 1;
    assert!(crate::capture_seal::rotate().is_err());
    let pending_bytes = fs::read(fixture.dir.join(MARKER)).unwrap();
    crate::capture_seal::verify(&project, &original).unwrap();
    assert_eq!(fs::read(fixture.dir.join(MARKER)).unwrap(), pending_bytes);

    assert_eq!(capture, original);
}
#[test]
fn seal_keychain_native_capability_rejects_foreign_namespace_and_test_calls_cannot_touch_keychain()
{
    let f = Fixture::new();
    let resources = f.root.join("Synthetic.app/Contents/Resources");
    fs::create_dir_all(&resources).unwrap();
    let authority = KeychainAuthority {
        identity: f.identity.clone(),
        allow_first: true,
        publisher_subject: serde_json::json!({"bundle":"invalid.example.synthetic","team":"SYNTHETIC0","binding":"a".repeat(64)}),
        _installed: crate::installed_custody::synthetic_for_tests(&resources).unwrap(),
    };
    let native = macos::NativeBackend::new(&authority);
    let mut other = f.identity.clone();
    other.access_group = "wrong".into();
    assert_eq!(native.read(&other), Err(BackendError::Invalid));
    assert_eq!(native.add(&other, &[1; 32]), Err(BackendError::Invalid));
    other = f.identity.clone();
    other.account.push_str(".rotation.not-a-key-id");
    assert_eq!(native.read(&other), Err(BackendError::Invalid));
    // Test build wrappers return failure without linking calls to actual SecItem operations.
    assert!(matches!(
        native.read(&f.identity),
        Err(BackendError::Unavailable(_))
    ));
    assert!(matches!(
        native.add(&f.identity, &[1; 32]),
        Err(BackendError::Unavailable(_))
    ));
}

#[test]
fn seal_keychain_only_explicit_enrollment_can_create_after_loss() {
    let f = Fixture::new();
    let b = Mock::default();
    assert!(f.run(&b, Operation::Seal, 1).is_err());
    assert!(f.run(&b, Operation::Rotate, 1).is_err());
    assert!(!f.dir.exists());
    assert_eq!(*b.adds.lock().unwrap(), 0);
    f.run(&b, Operation::Enroll, 1).unwrap();
    // Even loss of all local continuity evidence AND the backend item cannot
    // make an ordinary capture silently create a replacement installation key.
    fs::remove_dir_all(&f.dir).unwrap();
    b.items.lock().unwrap().clear();
    assert!(f.run(&b, Operation::Seal, 2).is_err());
    assert!(f.run(&b, Operation::Verify, 2).is_err());
    assert!(f.run(&b, Operation::Rotate, 2).is_err());
    assert_eq!(*b.adds.lock().unwrap(), 1);
}

#[test]
fn seal_keychain_readback_failure_retains_reservation_and_requires_observation() {
    let f = Fixture::new();
    let b = Mock::default();
    let key = [4; 32];
    let _guard = guard(&f.dir, true).unwrap();
    publish(
        &f.dir,
        &Marker {
            format: "capture-seal-keychain-continuity.s1".into(),
            scope_sha256: scope(&f.identity),
            keys: vec![],
            pending: Some(keyref(&key)),
        },
    )
    .unwrap();
    drop(_guard);
    b.items
        .lock()
        .unwrap()
        .insert(name(&f.identity), key.to_vec());
    *b.read_error.lock().unwrap() = Some(BackendError::Unavailable(-25308));
    assert!(f.run(&b, Operation::Seal, 9).is_err());
    assert!(load(&f.dir, &f.identity)
        .unwrap()
        .unwrap()
        .pending
        .is_some());
    assert_eq!(*b.adds.lock().unwrap(), 0);
    *b.read_error.lock().unwrap() = None;
    assert_eq!(
        f.run(&b, Operation::Enroll, 9).unwrap().current,
        key_id(&key)
    );
    assert_eq!(*b.adds.lock().unwrap(), 0);
}

#[test]
fn seal_keychain_pending_rotation_with_lost_prior_key_does_not_commit() {
    let f = Fixture::new();
    let b = Mock::default();
    f.run(&b, Operation::Enroll, 1).unwrap();
    *b.add_mode.lock().unwrap() = 2;
    assert!(f.run(&b, Operation::Rotate, 2).is_err());
    b.items.lock().unwrap().remove(&name(&f.identity));
    let before = fs::read(f.dir.join(MARKER)).unwrap();
    assert!(f.run(&b, Operation::Rotate, 3).is_err());
    assert_eq!(fs::read(f.dir.join(MARKER)).unwrap(), before);
    assert_eq!(*b.adds.lock().unwrap(), 2);
}

#[test]
fn seal_keychain_temporary_initial_denial_does_not_poison_enrollment() {
    let f = Fixture::new();
    let b = Mock::default();
    *b.read_error.lock().unwrap() = Some(BackendError::Unavailable(-34018));
    assert!(f.run(&b, Operation::Enroll, 1).is_err());
    assert!(!f.dir.exists());
    *b.read_error.lock().unwrap() = None;
    assert!(f.run(&b, Operation::Enroll, 1).is_ok());
    assert_eq!(*b.adds.lock().unwrap(), 1);
}
#[test]
fn seal_keychain_pending_rotation_preserves_historical_verification_and_single_key_read() {
    let f = Fixture::new();
    let b = Mock::default();
    let first = f.run(&b, Operation::Enroll, 1).unwrap();
    *b.add_mode.lock().unwrap() = 1;
    assert!(f.run(&b, Operation::Rotate, 2).is_err());
    let marker = fs::read(f.dir.join(MARKER)).unwrap();
    b.reads.lock().unwrap().clear();
    let held = f
        .run(&b, Operation::VerifyKey(first.current.clone()), 9)
        .unwrap();
    assert_eq!(held.keys[&first.current], [1; 32]);
    assert_eq!(b.reads.lock().unwrap().len(), 1);
    assert_eq!(fs::read(f.dir.join(MARKER)).unwrap(), marker);
    assert_eq!(*b.adds.lock().unwrap(), 2);
    assert_eq!(
        f.run(&b, Operation::Seal, 9).unwrap().current,
        first.current
    );
    assert_eq!(fs::read(f.dir.join(MARKER)).unwrap(), marker);
    assert_eq!(*b.adds.lock().unwrap(), 2);
}
#[test]
fn seal_keychain_seal_waits_for_shared_verification_without_losing_capture() {
    let f = std::sync::Arc::new(Fixture::new());
    let b = std::sync::Arc::new(Mock::default());
    f.run(&b, Operation::Enroll, 1).unwrap();
    let held = guard_mode(&f.dir, false, true, false).unwrap();
    let (tx, rx) = std::sync::mpsc::channel();
    let f2 = f.clone();
    let b2 = b.clone();
    let worker = std::thread::spawn(move || {
        let material = f2.run(&b2, Operation::Seal, 9).unwrap();
        tx.send(material.current).unwrap();
    });
    assert!(matches!(
        rx.recv_timeout(std::time::Duration::from_millis(30)),
        Err(std::sync::mpsc::RecvTimeoutError::Timeout)
    ));
    drop(held);
    assert_eq!(
        rx.recv_timeout(std::time::Duration::from_secs(5)).unwrap(),
        key_id(&[1; 32])
    );
    worker.join().unwrap();
    assert_eq!(*b.adds.lock().unwrap(), 1);
}

#[test]
fn seal_keychain_authority_is_process_local_reused_and_failed_refresh_revokes() {
    let f = Fixture::new();
    let resources = f.root.join("Synthetic.app/Contents/Resources");
    fs::create_dir_all(&resources).unwrap();
    let state = Mutex::new(None);
    let calls = std::cell::Cell::new(0);
    let make = || {
        calls.set(calls.get() + 1);
        Ok(KeychainAuthority {
            identity: f.identity.clone(),
            allow_first: true,
            publisher_subject: serde_json::json!({"bundle":"invalid.example.synthetic","team":"SYNTHETIC0","binding":"a".repeat(64)}),
            _installed: crate::installed_custody::synthetic_for_tests(&resources).unwrap(),
        })
    };
    let first = cached_authority(&state, false, make).unwrap();
    let next = cached_authority(&state, false, make).unwrap();
    assert!(std::sync::Arc::ptr_eq(&first, &next));
    assert_eq!(calls.get(), 1);
    cached_authority(&state, true, make).unwrap();
    assert_eq!(calls.get(), 2);
    assert!(cached_authority(&state, true, || Err("synthetic changed bundle".into())).is_err());
    assert!(state.lock().unwrap().is_none());
    assert!(cached_authority(&state, false, || Err("still unavailable".into())).is_err());
}
#[test]
fn seal_keychain_closed_marker_requires_explicit_pending() {
    let f = Fixture::new();
    let b = Mock::default();
    f.run(&b, Operation::Enroll, 1).unwrap();
    let mut raw: serde_json::Value =
        serde_json::from_slice(&fs::read(f.dir.join(MARKER)).unwrap()).unwrap();
    raw.as_object_mut().unwrap().remove("pending");
    fs::write(f.dir.join(MARKER), serde_json::to_vec(&raw).unwrap()).unwrap();
    assert!(f.run(&b, Operation::Verify, 1).is_err());
}

#[test]
fn seal_keychain_two_initial_enrollments_serialize_one_add() {
    let f = std::sync::Arc::new(Fixture::new());
    let b = std::sync::Arc::new(Mock::default());
    let barrier = std::sync::Arc::new(std::sync::Barrier::new(2));
    let mut threads = vec![];
    for key in [1, 2] {
        let f = f.clone();
        let b = b.clone();
        let barrier = barrier.clone();
        threads.push(std::thread::spawn(move || {
            barrier.wait();
            f.run(&b, Operation::Enroll, key).unwrap().current
        }));
    }
    let a = threads.remove(0).join().unwrap();
    let other = threads.remove(0).join().unwrap();
    assert_eq!(a, other);
    assert_eq!(*b.adds.lock().unwrap(), 1);
}

#[test]
fn seal_keychain_seal_reads_only_current_even_if_old_rotation_item_lost() {
    let f = Fixture::new();
    let b = Mock::default();
    let first = f.run(&b, Operation::Enroll, 1).unwrap();
    let rotated = f.run(&b, Operation::Rotate, 2).unwrap();
    b.items.lock().unwrap().remove(&name(&f.identity));
    b.reads.lock().unwrap().clear();
    let held = f.run(&b, Operation::Seal, 9).unwrap();
    assert_eq!(held.current, rotated.current);
    assert_eq!(held.keys.len(), 1);
    assert_eq!(b.reads.lock().unwrap().len(), 1);
    assert!(f.run(&b, Operation::VerifyKey(first.current), 9).is_err());
    assert!(f.run(&b, Operation::Rotate, 9).is_err());
}
#[test]
fn seal_keychain_explicit_enrollment_retries_unreserved_entropy_failure() {
    let f = Fixture::new();
    let b = Mock::default();
    assert!(operate(
        &f.dir,
        &f.legacy,
        &f.identity,
        true,
        &b,
        Operation::Enroll,
        &mut || Err("synthetic entropy unavailable".into())
    )
    .is_err());
    assert!(f.dir.exists());
    assert!(!f.dir.join(MARKER).exists());
    assert!(f.run(&b, Operation::Seal, 1).is_err());
    assert!(f.run(&b, Operation::Enroll, 1).is_ok());
    assert_eq!(*b.adds.lock().unwrap(), 1);
}
#[test]
fn seal_keychain_disappearing_existing_directory_never_gets_recreated() {
    let f = Fixture::new();
    let b = Mock::default();
    f.run(&b, Operation::Enroll, 1).unwrap();
    let dir = f.dir.clone();
    BEFORE_GUARD
        .with(|hook| *hook.borrow_mut() = Some(Box::new(move || fs::remove_dir_all(dir).unwrap())));
    assert!(f.run(&b, Operation::Enroll, 2).is_err());
    assert!(!f.dir.exists());
    assert_eq!(*b.adds.lock().unwrap(), 1);
}

fn enrollment_fixture() -> (Fixture, KeychainAuthority) {
    let mut f = Fixture::new();
    f.dir = f.root.join("capture-seal-keychain");
    f.legacy = f.root.join(crate::capture_seal::KEY_FOLDER);
    crate::capture_seal::set_folder_for_test(Some(Some(f.legacy.clone())));
    let resources = f.root.join("Synthetic.app/Contents/Resources");
    fs::create_dir_all(&resources).unwrap();
    let authority = KeychainAuthority {
        identity: f.identity.clone(),
        allow_first: true,
        publisher_subject: serde_json::json!({"bundle":"invalid.example.synthetic","team":"SYNTHETIC0","binding":"a".repeat(64)}),
        _installed: crate::installed_custody::synthetic_for_tests(&resources).unwrap(),
    };
    (f, authority)
}
#[test]
fn seal_prepared_read_only_drop_and_none_gate_do_not_touch_backend_or_files() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    let names = || {
        let mut names = fs::read_dir(&f.root)
            .unwrap()
            .map(|e| e.unwrap().file_name())
            .collect::<Vec<_>>();
        names.sort();
        names
    };
    let before = names();
    let p = prepare_subject(&f.root, &a).unwrap();
    assert_eq!(names(), before);
    assert_eq!(p.preview()["continuity_directory_present"], false);
    assert!(p.preview()["marker_sha256"].is_null());
    drop(p);
    assert_eq!(names(), before);
    assert!(b.reads.lock().unwrap().is_empty());
    assert_eq!(*b.adds.lock().unwrap(), 0);
    assert!(prepare_enrollment().is_err());
    let p = prepare_subject(&f.root, &a).unwrap();
    assert!(enroll_initial(p).is_err());
    assert_eq!(names(), before);
    assert!(dispatch(&f.legacy, Operation::Enroll).unwrap().is_err());
    assert_eq!(names(), before);
}
#[test]
fn seal_prepared_competing_absence_intents_allow_only_original_one_add() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    let first = prepare_subject(&f.root, &a).unwrap();
    let second = prepare_subject(&f.root, &a).unwrap();
    assert_ne!(first.preview()["attempt"], second.preview()["attempt"]);
    consume_prepared(first, &a, &b, &mut || Ok([1; 32])).unwrap();
    let reads = b.reads.lock().unwrap().len();
    assert!(consume_prepared(second, &a, &b, &mut || panic!("stale cannot generate")).is_err());
    assert_eq!(b.reads.lock().unwrap().len(), reads);
    assert_eq!(*b.adds.lock().unwrap(), 1);
}
#[test]
fn seal_prepared_policy_and_permission_drift_refuse_before_lock_or_backend() {
    for case in 0..4 {
        let (f, mut a) = enrollment_fixture();
        let b = Mock::default();
        let intent = prepare_subject(&f.root, &a).unwrap();
        match case {
            0 => a.identity.access_group = "OTHER00000.invalid.example.group".into(),
            1 => a.allow_first = false,
            2 => a.publisher_subject["binding"] = serde_json::json!("b".repeat(64)),
            _ => a.identity.service = "invalid.example.other".into(),
        }
        assert!(consume_prepared(intent, &a, &b, &mut || panic!(
            "changed policy cannot generate"
        ))
        .is_err());
        assert!(!f.root.join(".seal-c-enrollment.lock").exists());
        assert!(!f.dir.exists());
        assert!(b.reads.lock().unwrap().is_empty());
    }
}
#[test]
fn seal_prepared_root_replacement_and_legacy_appearance_refuse_before_backend() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    let intent = prepare_subject(&f.root, &a).unwrap();
    let moved = f.root.with_extension("held-original");
    fs::rename(&f.root, &moved).unwrap();
    fs::create_dir(&f.root).unwrap();
    assert!(consume_prepared(intent, &a, &b, &mut || panic!("replaced root")).is_err());
    assert!(b.reads.lock().unwrap().is_empty());
    fs::remove_dir_all(moved).unwrap();
    let (f, a) = enrollment_fixture();
    let intent = prepare_subject(&f.root, &a).unwrap();
    fs::create_dir(&f.legacy).unwrap();
    assert!(consume_prepared(intent, &a, &b, &mut || panic!("legacy changed")).is_err());
    assert!(b.reads.lock().unwrap().is_empty());
}
#[test]
fn seal_prepared_in_lock_absence_join_precedes_fresh_keychain_read() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    let intent = prepare_subject(&f.root, &a).unwrap();
    let dir = f.dir.clone();
    BEFORE_ENROLLMENT_JOIN.with(|slot| {
        *slot.borrow_mut() = Some(Box::new(move || {
            fs::DirBuilder::new().mode(0o700).create(dir).unwrap()
        }))
    });
    assert!(consume_prepared(intent, &a, &b, &mut || panic!("changed absence")).is_err());
    assert!(b.reads.lock().unwrap().is_empty());
    assert_eq!(*b.adds.lock().unwrap(), 0);
}
#[test]
fn seal_prepared_exact_marker_join_under_continuity_lock_precedes_readback() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    f.run(&b, Operation::Enroll, 1).unwrap();
    let intent = prepare_subject(&f.root, &a).unwrap();
    let marker = f.dir.join(MARKER);
    let mut raw = fs::read(&marker).unwrap();
    raw.push(b'\n');
    let reads = b.reads.lock().unwrap().len();
    BEFORE_GUARD
        .with(|slot| *slot.borrow_mut() = Some(Box::new(move || fs::write(marker, raw).unwrap())));
    assert!(consume_prepared(intent, &a, &b, &mut || panic!("changed marker")).is_err());
    assert_eq!(b.reads.lock().unwrap().len(), reads);
    assert_eq!(*b.adds.lock().unwrap(), 1);
}
#[test]
fn seal_prepared_marker_replacement_with_identical_bytes_refuses() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    f.run(&b, Operation::Enroll, 1).unwrap();
    let intent = prepare_subject(&f.root, &a).unwrap();
    let raw = fs::read(f.dir.join(MARKER)).unwrap();
    let replacement = f.dir.join("replacement");
    fs::write(&replacement, raw).unwrap();
    use std::os::unix::fs::PermissionsExt;
    fs::set_permissions(&replacement, fs::Permissions::from_mode(0o600)).unwrap();
    fs::rename(replacement, f.dir.join(MARKER)).unwrap();
    let reads = b.reads.lock().unwrap().len();
    assert!(consume_prepared(intent, &a, &b, &mut || panic!("replacement")).is_err());
    assert_eq!(b.reads.lock().unwrap().len(), reads);
}
#[test]
fn seal_prepared_pending_completion_keeps_original_subject_and_competitor_stale() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    *b.add_mode.lock().unwrap() = 2;
    assert!(f.run(&b, Operation::Enroll, 1).is_err());
    let first = prepare_subject(&f.root, &a).unwrap();
    let second = prepare_subject(&f.root, &a).unwrap();
    assert_eq!(
        first.preview()["marker"]["pending_key_id"],
        key_id(&[1; 32])
    );
    let held =
        consume_prepared(first, &a, &b, &mut || panic!("pending cannot regenerate")).unwrap();
    assert_eq!(held.current, key_id(&[1; 32]));
    let reads = b.reads.lock().unwrap().len();
    assert!(consume_prepared(second, &a, &b, &mut || panic!("stale pending")).is_err());
    assert_eq!(b.reads.lock().unwrap().len(), reads);
    assert_eq!(*b.adds.lock().unwrap(), 1);
}
#[test]
fn seal_prepared_pending_missing_stays_preserved_and_normal_paths_cannot_enroll() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    *b.add_mode.lock().unwrap() = 1;
    assert!(f.run(&b, Operation::Enroll, 1).is_err());
    let before = fs::read(f.dir.join(MARKER)).unwrap();
    let intent = prepare_subject(&f.root, &a).unwrap();
    assert!(consume_prepared(intent, &a, &b, &mut || panic!(
        "missing pending must not regenerate"
    ))
    .is_err());
    assert_eq!(fs::read(f.dir.join(MARKER)).unwrap(), before);
    assert_eq!(*b.adds.lock().unwrap(), 1);
}

#[test]
fn seal_prepared_holds_descriptors_not_locks_across_confirmation() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    f.run(&b, Operation::Enroll, 1).unwrap();
    let reads = b.reads.lock().unwrap().len();
    let p = prepare_subject(&f.root, &a).unwrap();
    let guard = guard_mode(&f.dir, false, false, false)
        .unwrap()
        .expect("intent must not hold a lock");
    drop(guard);
    assert_eq!(b.reads.lock().unwrap().len(), reads);
    consume_prepared(p, &a, &b, &mut || panic!("already committed")).unwrap();
    assert_eq!(*b.adds.lock().unwrap(), 1);
}
#[test]
fn seal_prepared_directory_permissions_and_replacement_refuse() {
    use std::os::unix::fs::PermissionsExt;
    for replace in [false, true] {
        let (f, a) = enrollment_fixture();
        let b = Mock::default();
        f.run(&b, Operation::Enroll, 1).unwrap();
        let p = prepare_subject(&f.root, &a).unwrap();
        if replace {
            let moved = f.root.join("original-continuity");
            fs::rename(&f.dir, moved).unwrap();
            fs::DirBuilder::new().mode(0o700).create(&f.dir).unwrap();
        } else {
            fs::set_permissions(&f.dir, fs::Permissions::from_mode(0o755)).unwrap();
        }
        let reads = b.reads.lock().unwrap().len();
        assert!(consume_prepared(p, &a, &b, &mut || panic!("changed physical source")).is_err());
        assert_eq!(b.reads.lock().unwrap().len(), reads);
    }
}

#[test]
fn seal_prepared_exact_post_join_presence_gap_refuses_before_backend_effects() {
    for was_present in [false, true] {
        let (f, a) = enrollment_fixture();
        let b = Mock::default();
        if was_present {
            f.run(&b, Operation::Enroll, 1).unwrap();
        }
        let intent = prepare_subject(&f.root, &a).unwrap();
        let dir = f.dir.clone();
        let moved = f.root.join("moved-continuity");
        AFTER_ENROLLMENT_JOIN.with(|slot| {
            *slot.borrow_mut() = Some(Box::new(move || {
                if was_present {
                    fs::rename(dir, moved).unwrap();
                } else {
                    fs::DirBuilder::new().mode(0o700).create(dir).unwrap();
                }
            }))
        });
        let reads = b.reads.lock().unwrap().len();
        let adds = *b.adds.lock().unwrap();
        assert!(
            consume_prepared(intent, &a, &b, &mut || panic!("gap cannot generate"))
                .err()
                .unwrap()
                .contains("changed after enrollment join")
        );
        assert_eq!(b.reads.lock().unwrap().len(), reads);
        assert_eq!(*b.adds.lock().unwrap(), adds);
        if was_present {
            assert!(!f.dir.exists(), "must not recreate after disappearance");
        }
    }
}
#[test]
fn seal_prepared_root_is_installed_source_with_no_caller_path_or_fallback() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    let unrelated = f.root.join("unrelated");
    fs::create_dir(&unrelated).unwrap();
    struct Reset;
    impl Drop for Reset {
        fn drop(&mut self) {
            crate::capture_seal::set_folder_for_test(None);
        }
    }
    let _reset = Reset;
    crate::capture_seal::set_folder_for_test(Some(Some(f.legacy.clone())));
    let intent = prepare_installed_subject(&a).unwrap();
    assert_eq!(intent.app_data, f.root);
    assert_ne!(intent.app_data, unrelated);
    drop(intent);
    for source in [
        None,
        Some(PathBuf::from("relative/capture-seal")),
        Some(unrelated.clone()),
    ] {
        crate::capture_seal::set_folder_for_test(Some(source));
        assert!(prepare_installed_subject(&a).is_err());
    }
    crate::capture_seal::set_folder_for_test(Some(Some(f.root.join("missing/capture-seal"))));
    assert!(prepare_installed_subject(&a).is_err());
    assert!(!f.root.join("missing").exists());
    assert!(b.reads.lock().unwrap().is_empty());
    assert_eq!(*b.adds.lock().unwrap(), 0);
    assert!(!f.dir.exists());
}

#[test]
fn seal_prepared_installed_root_change_revokes_original_intent() {
    let (f, a) = enrollment_fixture();
    let b = Mock::default();
    let intent = prepare_installed_subject(&a).unwrap();
    let other = f.root.join("other-installation");
    fs::create_dir(&other).unwrap();
    crate::capture_seal::set_folder_for_test(Some(Some(
        other.join(crate::capture_seal::KEY_FOLDER),
    )));
    assert!(consume_prepared(intent, &a, &b, &mut || panic!("changed installed root")).is_err());
    assert!(b.reads.lock().unwrap().is_empty());
    assert!(!f.dir.exists());
    crate::capture_seal::set_folder_for_test(None);
}


/// An enrolled installation on the existing in-memory backend (`Mock`, through
/// the real `operate` and policy item code), installed as this thread's
/// provider for capture sealing and the workflow approval policy. Dropping it
/// removes the provider: the build then reads as having no keychain.
pub(crate) struct InMemoryKeychain {
    fixture: std::rc::Rc<Fixture>,
    backend: std::rc::Rc<Mock>,
}
impl InMemoryKeychain {
    pub(crate) fn install(enrolled: bool) -> Self {
        let fixture = std::rc::Rc::new(Fixture::new());
        let backend = std::rc::Rc::new(Mock::default());
        if enrolled {
            fixture.run(&backend, Operation::Enroll, 9).unwrap();
        }
        let (f, b) = (fixture.clone(), backend.clone());
        TEST_PROVIDER.with(|slot| *slot.borrow_mut() = Some(Box::new(move |_, operation| f.run(&b, operation, 9))));
        let (f, b) = (fixture.clone(), backend.clone());
        set_policy_provider_for_test(Some(Box::new(move |operation| match operation {
            PolicyOp::Read => read_policy(&*b, &f.identity, Some(&f.root.join(POLICY_HEAD))),
            PolicyOp::Write(level) => write_policy(&*b, &f.identity, level, Some(&f.root.join(POLICY_HEAD))).and_then(|()| read_policy(&*b, &f.identity, Some(&f.root.join(POLICY_HEAD)))),
        })));
        Self { fixture, backend }
    }
    /// Locked / denied: every read fails as the native backend reports it.
    pub(crate) fn lock(&self) { *self.backend.read_error.lock().unwrap() = Some(BackendError::Unavailable(-25308)); }
    pub(crate) fn unlock(&self) { *self.backend.read_error.lock().unwrap() = None; }
    pub(crate) fn corrupt_policy(&self) {
        let mut items = self.backend.items.lock().unwrap();
        let key = items.keys().filter(|k| k.contains(".assurance-policy.")).max().cloned().expect("a policy item");
        items.insert(key, b"not a policy".to_vec());
    }
    pub(crate) fn remove_sentinel(&self) {
        let i = &self.fixture.identity;
        self.backend.items.lock().unwrap().remove(&format!("{}|{}|{}", i.service, i.account, i.access_group)).expect("sentinel");
    }
    pub(crate) fn remove_latest_policy(&self) {
        let mut items = self.backend.items.lock().unwrap();
        let key = items.keys().filter(|k| k.contains(".assurance-policy.")).max().cloned().expect("a policy item");
        items.remove(&key);
    }
    pub(crate) fn policy_items(&self) -> usize {
        self.backend.items.lock().unwrap().keys().filter(|k| k.contains(".assurance-policy.")).count()
    }
}
impl Drop for InMemoryKeychain {
    fn drop(&mut self) {
        TEST_PROVIDER.with(|slot| *slot.borrow_mut() = None);
        set_policy_provider_for_test(None);
    }
}

#[test]
fn policy_items_are_add_only_sequenced_and_never_read_absent_on_error() {
    let f = Fixture::new();
    let b = Mock::default();
    let head = f.root.join(POLICY_HEAD);
    let read = || read_policy(&b, &f.identity, Some(&head));
    let write = |level| write_policy(&b, &f.identity, level, Some(&head));
    assert!(matches!(read().unwrap(), PolicyRead::Absent { enrolled: false }));
    assert!(write("robust").is_err(), "no policy item without keychain protection");
    f.run(&b, Operation::Enroll, 3).unwrap();
    assert!(matches!(read().unwrap(), PolicyRead::Absent { enrolled: true }), "enrolled with no policy needs recovery");
    write("robust").unwrap();
    write("relaxed").unwrap();
    assert!(matches!(read().unwrap(), PolicyRead::Stored(l) if l == "relaxed"));
    write("robust").unwrap();
    assert!(matches!(read().unwrap(), PolicyRead::Stored(l) if l == "robust"));
    assert!(write("other").is_err());
    assert_eq!(b.items.lock().unwrap().keys().filter(|k| k.contains(".assurance-policy.")).count(), 3);
    let numbered = ItemIdentity { service: f.identity.service.clone(), account: format!("{}.assurance-policy.{:016x}", f.identity.account, 2), access_group: f.identity.access_group.clone() };
    assert_eq!(policy_sequence(&f.identity, &numbered), Some(2));
    let outside = ItemIdentity { account: format!("{}.assurance-policy.zz", f.identity.account), ..numbered.clone() };
    assert_eq!(policy_sequence(&f.identity, &outside), None);
    // Locked: an error, never "absent" and never a level.
    *b.read_error.lock().unwrap() = Some(BackendError::Unavailable(-25308));
    assert!(read().unwrap_err().contains("locked"));
    assert!(write("relaxed").is_err());
    *b.read_error.lock().unwrap() = None;
    // Lost tail (1=robust, 2=relaxed, 3=robust; 3 lost): never rolls back to relaxed.
    let name = |n: u64| format!("{}|{}.assurance-policy.{:016x}|{}", f.identity.service, f.identity.account, n, f.identity.access_group);
    let third = b.items.lock().unwrap().remove(&name(3)).unwrap();
    assert!(read().unwrap_err().contains("missing; recovery required"), "recorded head beyond the present items");
    // Intermediate gap: the later (latest) item is still found, not hidden.
    b.items.lock().unwrap().insert(name(3), third);
    let second = b.items.lock().unwrap().remove(&name(2)).unwrap();
    assert!(matches!(read().unwrap(), PolicyRead::Stored(l) if l == "robust"));
    b.items.lock().unwrap().insert(name(2), second);
    // Corrupt latest item: an error until a new item is added.
    b.items.lock().unwrap().insert(name(3), b"{}".to_vec());
    assert!(read().unwrap_err().contains("corrupt"));
    write("robust").unwrap();
    assert!(matches!(read().unwrap(), PolicyRead::Stored(l) if l == "robust"));
    // Recovery after a lost tail adds past every recorded sequence.
    b.items.lock().unwrap().remove(&name(4)).unwrap();
    assert!(read().is_err());
    write("robust").unwrap();
    assert!(matches!(read().unwrap(), PolicyRead::Stored(l) if l == "robust"));
    assert!(b.items.lock().unwrap().contains_key(&name(5)));
    // A long run of missing items before the recorded head hides nothing,
    // and recovery past it reads back.
    for n in 1..=4 { b.items.lock().unwrap().remove(&name(n)); }
    write("relaxed").unwrap(); // 6
    for n in 7..=15 { assert!(!b.items.lock().unwrap().contains_key(&name(n))); }
    let sixth = b.items.lock().unwrap().remove(&name(6)).unwrap();
    b.items.lock().unwrap().insert(name(16), sixth.clone());
    fs::write(&head, br#"{"sequence":16}"#).unwrap();
    assert!(read().unwrap_err().contains("corrupt"), "item 16 is read through the head even after a long gap");
    b.items.lock().unwrap().remove(&name(16));
    assert!(read().unwrap_err().contains("missing; recovery required"));
    write("robust").unwrap(); // 17
    assert!(matches!(read().unwrap(), PolicyRead::Stored(l) if l == "robust"));
    // A lost seal key with policy evidence remaining is recovery, not first use.
    let sentinel = format!("{}|{}|{}", f.identity.service, f.identity.account, f.identity.access_group);
    b.items.lock().unwrap().remove(&sentinel).unwrap();
    assert!(read().unwrap_err().contains("seal key is missing"));
    fs::remove_file(&head).unwrap();
    assert!(read().unwrap_err().contains("seal key is missing"), "policy items alone still show protection was set up");
}

/// Agent 0's P1 cases: discovery covers the whole bounded range, whatever the
/// App-data head says; a corrupt or unreadable head fails closed on read and write.
#[test]
fn policy_discovery_is_authoritative_over_the_whole_range() {
    let f = Fixture::new();
    let b = Mock::default();
    let head = f.root.join(POLICY_HEAD);
    let name = |n: u64| format!("{}|{}.assurance-policy.{:016x}|{}", f.identity.service, f.identity.account, n, f.identity.access_group);
    let put = |n: u64, level: &str| { b.items.lock().unwrap().insert(name(n), serde_json::to_vec(&serde_json::json!({"format":POLICY_FORMAT,"sequence":n,"level":level})).unwrap()); };
    let read = || read_policy(&b, &f.identity, Some(&head));
    f.run(&b, Operation::Enroll, 3).unwrap();
    // Item 2 relaxed, item 16 robust (beyond any eight-item window), between missing.
    put(2, "relaxed");
    put(16, "robust");
    for recorded in [None, Some(r#"{"sequence":0}"#)] {
        match recorded { Some(text) => fs::write(&head, text).unwrap(), None => { let _ = fs::remove_file(&head); } }
        assert!(matches!(read().unwrap(), PolicyRead::Stored(l) if l == "robust"), "head {recorded:?}: never the earlier relaxed item");
    }
    // A far item at the very end of the range is found too.
    put(POLICY_MAX, "relaxed");
    assert!(matches!(read().unwrap(), PolicyRead::Stored(l) if l == "relaxed"));
    assert!(write_policy(&b, &f.identity, "robust", Some(&head)).unwrap_err().contains("exhausted"), "never written below a later item");
    b.items.lock().unwrap().remove(&name(POLICY_MAX));
    // Corrupt or unreadable head: read and write fail closed.
    fs::write(&head, b"not json").unwrap();
    assert!(read().unwrap_err().contains("head record is corrupt"));
    assert!(write_policy(&b, &f.identity, "robust", Some(&head)).unwrap_err().contains("head record is corrupt"));
    fs::write(&head, format!(r#"{{"sequence":{}}}"#, POLICY_MAX + 1)).unwrap();
    assert!(read().is_err() && write_policy(&b, &f.identity, "robust", Some(&head)).is_err(), "a head beyond the range is corrupt");
    let _ = fs::remove_file(&head);
    fs::create_dir(&head).unwrap();
    assert!(read().unwrap_err().contains("head not readable"));
    assert!(write_policy(&b, &f.identity, "robust", Some(&head)).unwrap_err().contains("head not readable"));
    fs::remove_dir(&head).unwrap();
    assert_eq!(b.items.lock().unwrap().keys().filter(|k| k.contains(".assurance-policy.")).count(), 2, "no item written on a refused write");
    // Writing with a zero head and items present goes past every present item.
    fs::write(&head, r#"{"sequence":0}"#).unwrap();
    write_policy(&b, &f.identity, "relaxed", Some(&head)).unwrap();
    assert!(b.items.lock().unwrap().contains_key(&name(17)));
    // Missing seal key with only a far item present: recovery, never absent.
    let sentinel = format!("{}|{}|{}", f.identity.service, f.identity.account, f.identity.access_group);
    b.items.lock().unwrap().retain(|k, _| k == &name(16) || k == &sentinel);
    b.items.lock().unwrap().remove(&sentinel);
    let _ = fs::remove_file(&head);
    assert!(read().unwrap_err().contains("seal key is missing"));
}

#[test]
fn capture_seal_keychain_read_key_preserves_backend_causes() {
    let f = Fixture::new();
    let b = Mock::default();
    let ring = f.run(&b, Operation::Enroll, 9).unwrap();
    let marker = load(&f.dir, &f.identity).unwrap().unwrap();
    let reference = &marker.keys[0];
    assert_eq!(read_key(&b, &f.identity, 0, reference).unwrap(), ring.keys[&reference.id]);
    for (error, cause) in [
        (BackendError::Missing, Cause::KeyNotHeld),
        (BackendError::Unavailable(-25308), Cause::KeychainUnavailable),
        (BackendError::Unavailable(-25293), Cause::KeychainUnavailable),
        (BackendError::Invalid, Cause::KeyMaterialInvalid),
        (BackendError::Duplicate, Cause::ProtectionInconsistent),
    ] {
        *b.read_error.lock().unwrap() = Some(error);
        assert_eq!(read_key(&b, &f.identity, 0, reference).unwrap_err().cause, cause);
        *b.read_error.lock().unwrap() = None;
        assert!(read_key(&b, &f.identity, 0, reference).is_ok());
    }
    b.items.lock().unwrap().insert(name(&f.identity), vec![1]);
    assert_eq!(read_key(&b, &f.identity, 0, reference).unwrap_err().cause, Cause::KeyMaterialInvalid);
}

/// A synthetic selected installation that exercises real authority comparison,
/// absence selection, provider dispatch and the existing native coordinator.
/// The backend and installed identity are mocks, not installed qualification.
pub(crate) struct SelectedInstallation {
    fixture: std::rc::Rc<Fixture>,
    authority: std::rc::Rc<KeychainAuthority>,
    backend: std::rc::Rc<Mock>,
    previous_store: Result<crate::records_store::Store, String>,
}
impl SelectedInstallation {
    pub(crate) fn on_unselected_build<R>(&self, read: impl FnOnce() -> R) -> R {
        let selected = TEST_INSTALLATION.with(|slot| slot.borrow_mut().take());
        crate::checkpoint_recorder::forget_act_read_for_test();
        let result = read();
        TEST_INSTALLATION.with(|slot| *slot.borrow_mut() = selected);
        crate::checkpoint_recorder::forget_act_read_for_test();
        result
    }
    pub(crate) fn new() -> Self {
        let (f, a) = enrollment_fixture();
        Self::from_parts(f, a)
    }
    fn from_parts(f: Fixture, a: KeychainAuthority) -> Self {
        let fixture = std::rc::Rc::new(f);
        let authority = std::rc::Rc::new(a);
        let backend = std::rc::Rc::new(Mock::default());
        let previous_store = crate::records_store::current();
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: fixture.root.join("invented-records-store"), placement: crate::records_store::Placement::Test, limits: vec![] })));
        TEST_INSTALLATION.with(|slot| *slot.borrow_mut() = Some(TestInstallation {
            authority: authority.clone(), expected: authority.enrollment_policy(), backend: backend.clone(),
            inventory: vec![fixture.root.join("invented-capture-inventory")],
        }));
        Self { fixture, authority, backend, previous_store }
    }
    pub(crate) fn enroll(&self) -> Result<(), String> {
        crate::seal_c_enrollment::confirm_provider_for_test(
            || prepare_subject(&self.fixture.root, &self.authority),
            |intent| {
                consume_prepared(intent, &self.authority, &*self.backend, &mut || Ok([9;32]))?;
                write_policy(&*self.backend, &self.fixture.identity, "robust", Some(&self.fixture.root.join(POLICY_HEAD)))
            },
        )
    }
    pub(crate) fn lock(&self) { *self.backend.read_error.lock().unwrap() = Some(BackendError::Unavailable(-25308)); }
    pub(crate) fn unlock(&self) { *self.backend.read_error.lock().unwrap() = None; }
    /// Confirm before the file operation starts; replace its held join only
    /// after its last check, then commit through the real enrolment path.
    pub(crate) fn enroll_at_attachment(&self, restore_join: bool) {
        let authority = self.authority.clone();
        let backend = self.backend.clone();
        let root = self.fixture.root.clone();
        let prepared_root = root.clone();
        let prepared_authority = authority.clone();
        crate::seal_c_enrollment::confirm_provider_for_test(
            || prepare_subject(&prepared_root, &prepared_authority),
            |intent| {
                let root = root.clone();
                crate::capture_seal::BEFORE_ATTACHMENT.with(|slot| *slot.borrow_mut() = Some(Box::new(move || {
                    let join = root.join(".seal-c-enrollment.lock");
                    let held = root.join("invented-held-join");
                    fs::rename(&join, &held).unwrap();
                    consume_prepared(intent, &authority, &*backend, &mut || Ok([9;32])).unwrap();
                    write_policy(&*backend, &authority.identity, "robust", Some(&root.join(POLICY_HEAD))).unwrap();
                    if restore_join {
                        fs::remove_file(&join).unwrap();
                        fs::rename(held, join).unwrap();
                    }
                })));
                Ok(())
            },
        ).unwrap();
    }
    /// Replace the latest policy item's bytes (corruption in the keychain).
    pub(crate) fn root(&self) -> &Path { &self.fixture.root }
    pub(crate) fn include_capture_store(&self, path: PathBuf) {
        TEST_INSTALLATION.with(|slot| slot.borrow_mut().as_mut().unwrap().inventory.push(path));
    }
    fn clear_protected_state(&self) {
        self.backend.items.lock().unwrap().clear();
        let _ = fs::remove_dir_all(&self.fixture.dir);
        let _ = fs::remove_file(self.fixture.root.join(POLICY_HEAD));
    }
    fn new_process_observation(&self) { admission::forget(&self.fixture.root); }
    fn ordinary_capture(&self) -> serde_json::Value { serde_json::json!({"captureId":"cap:invented-provider-pair","choice":"act","actKind":"A4"}) }
    fn project(&self) -> PathBuf {
        let p = self.fixture.root.with_file_name(format!("{}-project", self.fixture.root.file_name().unwrap().to_string_lossy()));
        fs::create_dir_all(&p).unwrap(); p
    }
}
impl Drop for SelectedInstallation {
    fn drop(&mut self) {
        crate::records_store::use_store_for_test(Some(self.previous_store.clone()));
        TEST_INSTALLATION.with(|s| *s.borrow_mut() = None);
        TEST_PROVIDER.with(|s| *s.borrow_mut() = None);
        crate::capture_seal::set_folder_for_test(None);
        crate::capture_seal::BEFORE_ATTACHMENT.with(|s| *s.borrow_mut() = None);
        admission::forget(&self.fixture.root);
        admission::forget_libraries(&self.fixture.root);
        let p = self.fixture.root.with_file_name(format!("{}-project", self.fixture.root.file_name().unwrap().to_string_lossy()));
        let _ = fs::remove_dir_all(p);
    }
}
#[test]
fn capture_seal_signed_absence_then_real_enrollment_retains_old_file_evidence() {
    let f = SelectedInstallation::new(); let project = f.project();
    let mut old = f.ordinary_capture();
    assert_eq!(crate::capture_seal::seal(&project, &mut old).unwrap().verified_with, crate::capture_seal::SealProvider::FileKey);
    let bytes = old.clone();
    assert!(crate::capture_seal::verify(&project, &old).unwrap().sentence().contains("sealed with the App's key file, not your keychain"));
    f.enroll().unwrap();
    let mut new = f.ordinary_capture();
    assert_eq!(crate::capture_seal::seal(&project, &mut new).unwrap().verified_with, crate::capture_seal::SealProvider::Keychain);
    assert_eq!(crate::capture_seal::verify(&project, &old).unwrap().verified_with, crate::capture_seal::SealProvider::FileKey);
    assert_eq!(old, bytes);
    let continuity = fs::read(f.fixture.dir.join(MARKER)).unwrap();
    fs::remove_dir_all(&f.fixture.dir).unwrap();
    assert_eq!(crate::capture_seal::seal(&project, &mut f.ordinary_capture()).unwrap_err().cause, Cause::ContinuityUnavailable);
    fs::create_dir(&f.fixture.dir).unwrap();
    fs::set_permissions(&f.fixture.dir, std::os::unix::fs::PermissionsExt::from_mode(0o700)).unwrap();
    fs::write(f.fixture.dir.join(MARKER), &continuity).unwrap();
    fs::set_permissions(f.fixture.dir.join(MARKER), std::os::unix::fs::PermissionsExt::from_mode(0o600)).unwrap();
    assert_eq!(crate::capture_seal::verify(&project, &new).unwrap_err().cause, Cause::SealOperationBusy);
    assert!(!f.fixture.dir.join(".continuity.lock").exists(), "verification does not repair an incomplete restoration");
    // The fixture restores the missing control explicitly; a reader cannot.
    OpenOptions::new().write(true).create_new(true).mode(0o600)
        .open(f.fixture.dir.join(".continuity.lock")).unwrap();
    crate::capture_seal::verify(&project, &new).unwrap();
    fs::remove_file(f.fixture.dir.join(MARKER)).unwrap();
    assert_eq!(crate::capture_seal::seal(&project, &mut f.ordinary_capture()).unwrap_err().cause, Cause::ContinuityUnavailable);
    fs::write(f.fixture.dir.join(MARKER), &continuity).unwrap();
    fs::set_permissions(f.fixture.dir.join(MARKER), std::os::unix::fs::PermissionsExt::from_mode(0o600)).unwrap();
    crate::capture_seal::verify(&project, &new).unwrap();
    fs::remove_dir_all(&f.fixture.legacy).unwrap();
    assert_eq!(crate::capture_seal::verify(&project, &old).unwrap_err().cause, Cause::KeyNotHeld);
    assert_eq!(old, bytes);
}
#[test]
fn capture_seal_signed_absence_requires_each_veto_to_be_absent() {
    for veto in ["directory", "pending", "head-zero", "head-corrupt", "capture", "memory"] {
        let f = SelectedInstallation::new(); let p = f.project();
        crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap();
        match veto {
            "directory" => { fs::create_dir(&f.fixture.dir).unwrap(); },
            "pending" => {
                *f.backend.add_mode.lock().unwrap() = 1;
                assert!(f.enroll().is_err());
                assert!(load(&f.fixture.dir, &f.fixture.identity).unwrap().unwrap().pending.is_some());
            },
            "head-zero" | "head-corrupt" => {
                f.enroll().unwrap(); f.clear_protected_state(); f.new_process_observation();
                fs::write(f.root().join(POLICY_HEAD), if veto == "head-zero" { b"{\"sequence\":0}".as_slice() } else { b"bad head".as_slice() }).unwrap();
            },
            "capture" => {
                f.enroll().unwrap();
                let mut capture = f.ordinary_capture(); crate::capture_seal::seal(&p, &mut capture).unwrap();
                f.clear_protected_state(); f.new_process_observation();
                let store = f.root().join("invented-capture-inventory"); fs::create_dir(&store).unwrap();
                fs::write(store.join("capture.json"), serde_json::to_vec(&capture).unwrap()).unwrap();
            },
            "memory" => { f.enroll().unwrap(); crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap(); f.clear_protected_state(); },
            _ => unreachable!(),
        }
        let mut refused = f.ordinary_capture();
        assert!(crate::capture_seal::seal(&p, &mut refused).is_err(), "{veto}");
        assert!(refused.get("seal").is_none()); assert!(refused.get("sealProvider").is_none());
        f.clear_protected_state();
        let _ = fs::remove_dir_all(f.root().join("invented-capture-inventory"));
        f.new_process_observation();
        assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap().verified_with, crate::capture_seal::SealProvider::FileKey, "{veto}");
    }
}
#[test]
fn capture_seal_ordinary_policy_preferences_are_never_protection_vetoes() {
    let f = SelectedInstallation::new(); let p = f.project();
    for level in ["relaxed", "robust"] {
        fs::write(f.root().join("workflow-approval-policy.json"), serde_json::to_vec(&serde_json::json!({"format":"chirality.app.workflow-approval-policy-setting","formatVersion":"1","level":level,"writtenAt":"2026-11-14T00:00:00Z"})).unwrap()).unwrap();
        assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap().verified_with, crate::capture_seal::SealProvider::FileKey);
        f.enroll().unwrap();
        assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap().verified_with, crate::capture_seal::SealProvider::Keychain);
        f.clear_protected_state(); f.new_process_observation();
    }
}
#[test]
fn capture_seal_locked_denied_late_failed_and_wrong_identity_reads_never_grant_file() {
    let f = SelectedInstallation::new(); let p = f.project();
    crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap();
    for code in [-25308, -25293, -1] {
        *f.backend.read_error.lock().unwrap() = Some(BackendError::Unavailable(code));
        assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap_err().cause, Cause::KeychainUnavailable);
        f.unlock(); crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap();
    }
    f.backend.read_errors.lock().unwrap().insert(name(&policy_item(&f.fixture.identity, 256)), BackendError::Unavailable(-25308));
    assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap_err().cause, Cause::KeychainUnavailable);
    f.backend.read_errors.lock().unwrap().clear();
    crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap();
    f.backend.reads.lock().unwrap().clear();
    TEST_INSTALLATION.with(|slot| slot.borrow_mut().as_mut().unwrap().expected.identity.access_group.push_str(".wrong"));
    assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap_err().cause, Cause::AuthorityUnavailable);
    assert!(f.backend.reads.lock().unwrap().is_empty());
    TEST_INSTALLATION.with(|slot| slot.borrow_mut().as_mut().unwrap().expected = f.authority.enrollment_policy());
    crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap();
    f.backend.items.lock().unwrap().insert(name(&f.fixture.identity), vec![1]);
    assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap_err().cause, Cause::KeyMaterialInvalid);
    f.backend.items.lock().unwrap().clear();
    assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap_err().cause, Cause::ProtectionInconsistent,
        "even malformed protected-item presence was observed; removing it cannot erase this process's veto");
    f.new_process_observation();
    crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap();
    let inventory = f.root().join("invented-capture-inventory"); fs::create_dir(&inventory).unwrap();
    let original: serde_json::Value = serde_json::from_str(include_str!("../schemas/fixtures/aac.capture-evidence.example.valid.json")).unwrap();
    let valid = serde_json::to_vec(&original["instances"][2]).unwrap();
    fs::write(inventory.join("capture.json"), &valid).unwrap();
    crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap();
    for broken in [b"not JSON".as_slice(), b"{}".as_slice(), b"null".as_slice()] {
        fs::write(inventory.join("capture.json"), broken).unwrap();
        assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap_err().cause, Cause::ProtectionInconsistent);
        fs::write(inventory.join("capture.json"), &valid).unwrap();
        crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap();
    }
}
#[test]
fn capture_seal_policy_only_far_item_and_head_deletion_never_authorize_file() {
    let f = SelectedInstallation::new(); let p = f.project();
    crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap(); f.enroll().unwrap();
    let mut original = f.ordinary_capture(); crate::capture_seal::seal(&p, &mut original).unwrap();
    fs::write(f.root().join(POLICY_HEAD), b"{\"sequence\":255}").unwrap();
    write_policy(&*f.backend, &f.fixture.identity, "robust", Some(&f.root().join(POLICY_HEAD))).unwrap();
    let sentinel = f.backend.items.lock().unwrap().remove(&name(&f.fixture.identity)).unwrap();
    fs::remove_file(f.root().join(POLICY_HEAD)).unwrap();
    assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap_err().cause, Cause::ProtectionInconsistent);
    f.backend.items.lock().unwrap().insert(name(&f.fixture.identity), sentinel);
    crate::capture_seal::verify(&p, &original).unwrap();
    assert_eq!(crate::capture_seal::seal(&p, &mut f.ordinary_capture()).unwrap().verified_with, crate::capture_seal::SealProvider::Keychain);
}
#[test]
fn capture_seal_prepared_retained_ring_is_frozen_and_never_imported() {
    let f = SelectedInstallation::new(); let p = f.project();
    let mut original=f.ordinary_capture(); crate::capture_seal::seal(&p,&mut original).unwrap();
    let before=fs::read(f.fixture.legacy.join("keys.json")).unwrap();
    let prepared=prepare_subject(f.root(),&f.authority).unwrap();
    assert_eq!(prepared.preview()["legacy_directory_observed_absent"], false);
    let moved=f.root().join("held-original-keys"); fs::rename(f.fixture.legacy.join("keys.json"),&moved).unwrap();
    fs::write(f.fixture.legacy.join("keys.json"),&before).unwrap();
    fs::set_permissions(f.fixture.legacy.join("keys.json"),std::os::unix::fs::PermissionsExt::from_mode(0o600)).unwrap();
    assert!(consume_prepared(prepared,&f.authority,&*f.backend,&mut || Ok([9;32])).is_err());
    assert_eq!(*f.backend.adds.lock().unwrap(),0);
    fs::remove_file(f.fixture.legacy.join("keys.json")).unwrap(); fs::rename(moved,f.fixture.legacy.join("keys.json")).unwrap();
    f.enroll().unwrap();
    assert_eq!(fs::read(f.fixture.legacy.join("keys.json")).unwrap(),before);
    assert_ne!(original["seal"]["value"].as_str().unwrap().split(':').next().unwrap(),key_id(&[9;32]));
    crate::capture_seal::verify(&p,&original).unwrap();
}

#[test]
fn capture_seal_total_loss_exposes_the_stated_continuity_exclusion_and_unknown_inventory_refuses() {
    let f=SelectedInstallation::new();let p=f.project();
    crate::capture_seal::seal(&p,&mut f.ordinary_capture()).unwrap();
    let configured=crate::records_store::current();
    crate::records_store::use_store_for_test(Some(Err("invented unavailable inventory".into())));
    assert_eq!(crate::capture_seal::seal(&p,&mut f.ordinary_capture()).unwrap_err().cause,Cause::ProtectionInconsistent);
    crate::records_store::use_store_for_test(Some(configured));
    crate::capture_seal::seal(&p,&mut f.ordinary_capture()).unwrap();
    f.enroll().unwrap();
    assert_eq!(crate::capture_seal::seal(&p,&mut f.ordinary_capture()).unwrap().verified_with,crate::capture_seal::SealProvider::Keychain);
    f.clear_protected_state();
    assert!(crate::capture_seal::seal(&p,&mut f.ordinary_capture()).is_err(),"surviving process memory vetoes");
    let status=std::process::Command::new(std::env::current_exe().unwrap())
        .args(["--exact","capture_seal_keychain::tests::capture_seal_total_loss_fresh_process_probe","--ignored","--nocapture","--test-threads=1"])
        .env("CHIRALITY_SEAL_RESET_FIXTURE_ROOT",f.root()).status().unwrap();
    assert!(status.success(),"complete loss or coherent pre-protection rollback is excluded, not prevented");
}

#[test]
#[ignore = "invoked only by the complete-loss parent with its invented installation"]
fn capture_seal_total_loss_fresh_process_probe() {
    let root=PathBuf::from(std::env::var_os("CHIRALITY_SEAL_RESET_FIXTURE_ROOT").expect("parent fixture required"));
    assert!(root.starts_with(fs::canonicalize(std::env::temp_dir()).unwrap()));
    let (mut f,mut authority)=enrollment_fixture();
    fs::remove_dir_all(&f.root).unwrap();
    f.root=root;f.dir=f.root.join("capture-seal-keychain");f.legacy=f.root.join(crate::capture_seal::KEY_FOLDER);
    crate::capture_seal::set_folder_for_test(Some(Some(f.legacy.clone())));
    authority._installed=crate::installed_custody::synthetic_for_tests(&f.root.join("Synthetic.app/Contents/Resources")).unwrap();
    let installation=SelectedInstallation::from_parts(f,authority);let project=installation.project();
    assert_eq!(crate::capture_seal::seal(&project,&mut installation.ordinary_capture()).unwrap().verified_with,crate::capture_seal::SealProvider::FileKey,
        "a real fresh process observes the same empty protected namespace and absent vetoes as first use");
}

#[test]
fn capture_seal_intact_enrollment_join_serializes_file_attachment_before_protection() {
    let f=SelectedInstallation::new();let p=f.project();
    crate::capture_seal::seal(&p,&mut f.ordinary_capture()).unwrap();
    let prepared=prepare_subject(f.root(),&f.authority).unwrap();
    let store=crate::records_store::current();
    let legacy=f.fixture.legacy.clone();
    let (start_tx,start_rx)=std::sync::mpsc::channel();
    let (done_tx,done_rx)=std::sync::mpsc::channel();
    std::thread::scope(|scope| {
        let authority=&*f.authority;let backend=&*f.backend;
        let worker=scope.spawn(move || {
            crate::records_store::use_store_for_test(Some(store));
            crate::capture_seal::set_folder_for_test(Some(Some(legacy)));
            start_rx.recv().unwrap();
            consume_prepared(prepared,authority,backend,&mut || Ok([9;32])).unwrap();
            let _ = done_tx.send(()); // the hook drops its receiver after attachment
        });
        crate::capture_seal::BEFORE_ATTACHMENT.with(|slot| *slot.borrow_mut()=Some(Box::new(move || {
            start_tx.send(()).unwrap();
            assert!(matches!(done_rx.recv_timeout(std::time::Duration::from_millis(30)),Err(std::sync::mpsc::RecvTimeoutError::Timeout)),"enrolment must wait for the intact file-operation join");
        })));
        let mut file=f.ordinary_capture();crate::capture_seal::seal(&p,&mut file).unwrap();
        assert_eq!(file["sealProvider"],"file-key");
        worker.join().unwrap();
    });
    assert_eq!(crate::capture_seal::seal(&p,&mut f.ordinary_capture()).unwrap().verified_with,crate::capture_seal::SealProvider::Keychain);
}

#[test]
fn capture_seal_detected_enrollment_join_replacement_refuses_before_attachment() {
    let f=SelectedInstallation::new();let p=f.project();
    crate::capture_seal::seal(&p,&mut f.ordinary_capture()).unwrap();
    struct Replacing<'a> { backend:&'a Mock, reads:std::cell::Cell<usize>, root:PathBuf, sentinel:ItemIdentity }
    impl Backend for Replacing<'_> {
        fn read(&self,item:&ItemIdentity)->Result<Vec<u8>,BackendError> {
            if item==&self.sentinel {
                self.reads.set(self.reads.get()+1);
                if self.reads.get()==2 {
                    let join=self.root.join(".seal-c-enrollment.lock");fs::rename(&join,self.root.join("held-original-join")).unwrap();
                    OpenOptions::new().write(true).create_new(true).mode(0o600).open(join).unwrap();
                }
            }
            self.backend.read(item)
        }
        fn add(&self,item:&ItemIdentity,bytes:&[u8])->Result<(),BackendError> {self.backend.add(item,bytes)}
    }
    let backend=Replacing {backend:&f.backend,reads:std::cell::Cell::new(0),root:f.root().to_owned(),sentinel:f.fixture.identity.clone()};
    let called=std::cell::Cell::new(false);
    let result=admission::with_material(&f.fixture.legacy,&p,&f.authority,&backend,Some(&[]),|_| {called.set(true);Ok(())});
    assert_eq!(result.unwrap_err().cause,Cause::SealSourceChanged);assert!(!called.get());
    crate::capture_seal::seal(&p,&mut f.ordinary_capture()).unwrap();
}

// Review regressions publish through the real A16 writer. Native confirmation
// is the existing fixture stand-in, never a person or a running App.
fn review_publish(project: &Path) -> serde_json::Value {
    use crate::act_control::{person, ActControl, InputSource};
    fs::create_dir_all(project.join("project/decisions")).unwrap();
    fs::copy(Path::new(env!("CARGO_MANIFEST_DIR")).join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json"), project.join("project/decisions/PKG-1.json")).unwrap();
    crate::recorder::identify_packages(project).unwrap();
    let (entries, limits) = crate::storage::read_all(project); assert!(limits.is_empty(), "{limits:?}");
    let request = entries.iter().find(|e| e["kind"] == "act_request").expect("the package request remains recorded");
    let mut control = ActControl::new(project);
    let offer = control.compose_a16(request["recordId"].as_str().unwrap()).unwrap();
    let id = offer["offerId"].as_str().unwrap();
    let actor = person(Some("Review fixture person"), Some("review fixture account"));
    control.confirmation_text(id, "ALT-2", &actor).unwrap();
    control.present(id).unwrap();
    let out = control.confirm(id, "ALT-2", InputSource::HostNativeConfirmation, actor).unwrap();
    assert_eq!(out["recordDurable"], true, "{out}");
    let path = crate::storage::capture_file_for(project, &out["capture"]).unwrap();
    assert_eq!(serde_json::from_slice::<serde_json::Value>(&fs::read(path).unwrap()).unwrap(), out["capture"]);
    out["capture"].clone()
}
fn review_unsealed(project: &Path) -> serde_json::Value {
    let capture = review_publish(project);
    assert!(capture.get("sealProvider").is_none(), "inventory/protection refusal must not publish a file seal: {capture}");
    capture
}
#[test]
fn capture_seal_decision_standing_never_creates_or_repairs_a_continuity_lock() {
    fn snapshot(root: &Path) -> BTreeMap<PathBuf, (u32, u64, Vec<u8>)> {
        fn visit(root: &Path, path: &Path, out: &mut BTreeMap<PathBuf, (u32, u64, Vec<u8>)>) {
            let metadata = fs::symlink_metadata(path).unwrap();
            let bytes = if metadata.file_type().is_symlink() {
                use std::os::unix::ffi::OsStrExt;
                fs::read_link(path).unwrap().as_os_str().as_bytes().to_vec()
            } else if metadata.is_file() {
                fs::read(path).unwrap()
            } else {
                Vec::new()
            };
            out.insert(path.strip_prefix(root).unwrap().to_owned(), (metadata.mode(), metadata.ino(), bytes));
            if metadata.is_dir() {
                for entry in fs::read_dir(path).unwrap() {
                    visit(root, &entry.unwrap().path(), out);
                }
            }
        }
        let mut result = BTreeMap::new();
        visit(root, root, &mut result);
        result
    }
    let f = SelectedInstallation::new();
    let project = f.project();
    f.enroll().unwrap();
    assert_eq!(review_publish(&project)["sealProvider"], "keychain");
    let lock = f.fixture.dir.join(".continuity.lock");
    let held = f.fixture.dir.join("invented-held-lock");
    let read = |expected: &str| {
        let before = (snapshot(f.root()), snapshot(&project));
        let adds = *f.backend.adds.lock().unwrap();
        let view = crate::decision_view::derive(&project, &[]);
        assert_eq!(view["rows"][0]["state"], "decided", "{view}");
        assert_eq!(view["rows"][0]["decision"]["captureSeal"]["presentation"], expected, "{view}");
        assert_eq!((snapshot(f.root()), snapshot(&project)), before, "a standing read changed files");
        assert_eq!(*f.backend.adds.lock().unwrap(), adds, "a standing read added a protected item");
    };
    read("keychain-verified");
    fs::rename(&lock, &held).unwrap();
    read("unavailable");
    assert!(!lock.exists(), "verification must not recreate a missing lock");
    std::os::unix::fs::symlink(&held, &lock).unwrap();
    read("unavailable");
    fs::remove_file(&lock).unwrap();
    fs::hard_link(&held, &lock).unwrap();
    read("unavailable");
    fs::remove_file(&lock).unwrap();
    fs::rename(&held, &lock).unwrap();
    fs::set_permissions(&lock, fs::Permissions::from_mode(0o400)).unwrap();
    read("keychain-verified");
}
fn review_inventory_unsealed(project: &Path) {
    let capture = review_unsealed(project);
    assert!(capture["evidenceLimits"].to_string().contains("Recover capture verification"), "{capture}");
}
#[test]
fn capture_seal_review_library_inventory_survives_a_fresh_process() { review_library_inventory(false); }
#[test]
fn capture_seal_review_unreadable_library_survives_a_fresh_process() { review_library_inventory(true); }
fn review_library_inventory(unreadable: bool) {
    {
        let f = SelectedInstallation::new(); let project = f.project();
        assert_eq!(review_publish(&project)["sealProvider"], "file-key");
        let library = project.join("external-library"); fs::create_dir(&library).unwrap();
        let _owner = crate::workflow_workspace::registration::LibraryOwner::open(library.clone(), "user", "review-library").unwrap();
        if unreadable {
            fs::remove_dir(&library).unwrap(); fs::write(&library, b"no readable library directory").unwrap();
        } else {
            f.enroll().unwrap();
            let examples: serde_json::Value = serde_json::from_str(include_str!("../schemas/fixtures/aac.capture-evidence.example.valid.json")).unwrap();
            let mut capture = examples["instances"].as_array().unwrap().iter().find(|c| c["actKind"] == "A15").unwrap().clone();
            crate::capture_seal::seal(&library, &mut capture).unwrap();
            let path = crate::storage::capture_file_for(&library, &capture).unwrap();
            crate::storage::create_json(&path, &capture).unwrap();
            f.clear_protected_state(); admission::forget(f.root());
        }
        review_inventory_unsealed(&project); // permitted -> veto while that library is open
        let status = std::process::Command::new(std::env::current_exe().unwrap())
            .args(["--exact", "capture_seal_keychain::tests::capture_seal_review_library_fresh_process_probe", "--ignored", "--nocapture", "--test-threads=1"])
            .env("CHIRALITY_SEAL_LIBRARY_FIXTURE_ROOT", f.root()).status().unwrap();
        assert!(status.success(), "a retained library must veto in a real new process without being reopened");
    }
}
#[test]
#[ignore = "parent-owned invented installation; never opens the retained library"]
fn capture_seal_review_library_fresh_process_probe() {
    let root = PathBuf::from(std::env::var_os("CHIRALITY_SEAL_LIBRARY_FIXTURE_ROOT").expect("parent fixture required"));
    assert!(root.starts_with(fs::canonicalize(std::env::temp_dir()).unwrap()));
    let (mut f, mut a) = enrollment_fixture(); fs::remove_dir_all(&f.root).unwrap();
    f.root = root; f.dir = f.root.join("capture-seal-keychain"); f.legacy = f.root.join(crate::capture_seal::KEY_FOLDER);
    crate::capture_seal::set_folder_for_test(Some(Some(f.legacy.clone())));
    a._installed = crate::installed_custody::synthetic_for_tests(&f.root.join("Synthetic.app/Contents/Resources")).unwrap();
    let installation = SelectedInstallation::from_parts(f, a);
    if std::env::var_os("CHIRALITY_SEAL_LIBRARY_REWRITE_BOUNDARY").is_some() {
        assert_eq!(review_publish(&installation.project())["sealProvider"], "file-key",
            "boundary: a valid list rewrite can hide a retained library in a fresh process");
    } else {
        review_inventory_unsealed(&installation.project());
    }
    // The parent owns these invented files, including the retained capture.
    // Do not run the fixture's project-deleting Drop in this child process.
    std::mem::forget(installation);
}
fn review_damaged_library_list(bytes: &[u8]) {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    fs::write(f.root().join("capture-seal-libraries.json"), bytes).unwrap();
    review_inventory_unsealed(&project);
}
#[test]
fn capture_seal_review_empty_library_list_refuses() { review_damaged_library_list(b""); }
#[test]
fn capture_seal_review_truncated_library_list_refuses() { review_damaged_library_list(br#"{"format":"chirality.app.capture-seal-library-inventory/v1","roots":["#); }
#[test]
fn capture_seal_review_malformed_library_list_refuses() { review_damaged_library_list(b"not JSON"); }
#[test]
fn capture_seal_review_unknown_shape_library_list_refuses() { review_damaged_library_list(b"{}"); }
#[test]
fn capture_seal_review_a_complete_list_naming_no_library_refuses() {
    // Permitted: a complete list naming one readable library with no capture still admits.
    let f = SelectedInstallation::new(); let project = f.project();
    let library = project.join("external-library"); fs::create_dir(&library).unwrap();
    let list = |roots: Vec<PathBuf>| serde_json::to_vec(&serde_json::json!({
        "format": "chirality.app.capture-seal-library-inventory/v1", "roots": roots, "complete": true})).unwrap();
    fs::write(f.root().join("capture-seal-libraries.json"), list(vec![fs::canonicalize(&library).unwrap()])).unwrap();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    // Spoiled: the same complete document naming no library, which the App never writes.
    fs::write(f.root().join("capture-seal-libraries.json"), list(Vec::new())).unwrap();
    let capture = review_unsealed(&project);
    assert!(capture["evidenceLimits"].to_string().contains("names no library"), "{capture}");
    assert!(capture["evidenceLimits"].to_string().contains("Recover capture verification"), "{capture}");
}
#[test]
fn capture_seal_review_observed_sentinel_survives_corrupt_head_then_loss() {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    f.enroll().unwrap(); admission::forget(f.root()); // new process has not observed it yet
    fs::write(f.root().join(POLICY_HEAD), b"corrupt").unwrap();
    review_unsealed(&project);
    f.clear_protected_state();
    review_unsealed(&project); // old code forgot the sentinel after the corrupt head
}
#[test]
fn capture_seal_review_observed_policy_survives_later_error_then_loss() {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    f.enroll().unwrap(); admission::forget(f.root());
    f.backend.items.lock().unwrap().remove(&name(&f.fixture.identity));
    fs::remove_file(f.root().join(POLICY_HEAD)).unwrap();
    f.backend.read_errors.lock().unwrap().insert(name(&policy_item(&f.fixture.identity, 2)), BackendError::Unavailable(-25308));
    review_unsealed(&project);
    f.clear_protected_state(); f.backend.read_errors.lock().unwrap().clear();
    review_unsealed(&project); // policy 1 was seen before policy 2 failed
}
#[test]
fn capture_seal_review_named_verification_survives_disappearance() {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    f.enroll().unwrap();
    let mut capture = f.ordinary_capture(); crate::capture_seal::seal(&project, &mut capture).unwrap();
    admission::forget(f.root());
    assert_eq!(crate::capture_seal::verify(&project, &capture).unwrap().verified_with, crate::capture_seal::SealProvider::Keychain);
    f.clear_protected_state();
    review_unsealed(&project);
}

#[test]
fn capture_seal_review_production_dispatch_remembers_named_verification() {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    f.enroll().unwrap();
    let mut capture = f.ordinary_capture(); crate::capture_seal::seal(&project, &mut capture).unwrap();
    let id = capture["seal"]["value"].as_str().unwrap().split(':').next().unwrap();
    admission::forget(f.root());
    // Authority and OS reads are injected at the boundary, below the single
    // production dispatch body. There is no synthetic success-memory branch.
    let material = dispatch(&f.fixture.legacy, Operation::VerifyKey(id.into())).unwrap().unwrap();
    assert_eq!(material.provider, crate::capture_seal::SealProvider::Keychain);
    f.clear_protected_state();
    review_unsealed(&project);
}

#[test]
fn capture_seal_review_library_list_adds_roots_without_pruning_and_recovers_read_only() {
    let f = SelectedInstallation::new(); let project = f.project();
    let roots = [project.join("known-first"), project.join("known-second")];
    for root in &roots {
        fs::create_dir(root).unwrap();
        crate::workflow_workspace::registration::LibraryOwner::open(root.clone(), "user", "review-library").unwrap();
    }
    let list = f.root().join("capture-seal-libraries.json");
    let original = fs::read(&list).unwrap();
    let value: serde_json::Value = serde_json::from_slice(&original).unwrap();
    assert_eq!(value["complete"], true);
    assert_eq!(value["roots"].as_array().unwrap().len(), 2);
    assert_eq!(review_publish(&project)["sealProvider"], "file-key", "knowing readable empty libraries grants no stronger standing");
    let moved = project.join("retained-second"); fs::rename(&roots[1], &moved).unwrap();
    crate::workflow_workspace::registration::LibraryOwner::open(roots[0].clone(), "user", "review-library").unwrap();
    assert_eq!(fs::read(&list).unwrap(), original, "opening another library never prunes the unavailable root");
    review_inventory_unsealed(&project);
    fs::rename(moved, &roots[1]).unwrap();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    assert_eq!(fs::read(&list).unwrap(), original, "recovery observes the original complete inventory without editing it");
}

#[test]
fn capture_seal_review_reopening_a_live_library_restores_its_lost_list_entry() {
    let f = SelectedInstallation::new(); let project = f.project();
    let library = project.join("live-library"); fs::create_dir(&library).unwrap();
    let mut root = crate::runtime_session::WorkflowRootSession::default();
    let first = root.open_library(library.clone(), "user", None, std::sync::Arc::new(std::sync::Mutex::new(None))).unwrap();
    let list = f.root().join("capture-seal-libraries.json");
    let original = fs::read(&list).unwrap();
    fs::remove_file(&list).unwrap(); // removable local trace; no removal act
    let reopened = root.open_library(library, "user", None, std::sync::Arc::new(std::sync::Mutex::new(None))).unwrap();
    assert_eq!(first, reopened);
    assert_eq!(fs::read(&list).unwrap(), original, "the already-open context must re-register its root on a new opening");
}

// Repair 3: access to a library is separate from admission of a file seal.
fn repair3_library(root: &Path, name: &str) -> PathBuf {
    let library = root.join(name);
    let entry = library.join(".chirality/workflows/sample");
    fs::create_dir_all(&entry).unwrap();
    fs::write(entry.join("WORKFLOW.md"), b"---\nname: sample\n---\n# Method\nInvented review work.\n").unwrap();
    library
}
fn repair3_open(root: &mut crate::runtime_session::WorkflowRootSession, library: &Path) -> String {
    let id = root.open_library(library.into(), "user", None, std::sync::Arc::new(std::sync::Mutex::new(None)))
        .expect("inventory failure must not prevent opening the library");
    let view = root.snapshot();
    let row = view["libraries"].as_array().unwrap().iter().find(|row| row["reference"] == id).unwrap();
    assert!(row["entryListing"]["entries"].as_array().unwrap().iter().any(|e| e["name"] == "sample" && e["reviewable"] == true), "{row}");
    id
}
fn repair3_refused(f: &SelectedInstallation, project: &Path) {
    let error = crate::capture_seal::seal(project, &mut f.ordinary_capture()).unwrap_err();
    assert_eq!(error.cause, Cause::ProtectionInconsistent);
    assert!(error.detail.starts_with("Library protection inventory is incomplete:"), "{error:?}");
    assert!(error.detail.contains("Recover capture verification"), "{error:?}");
    let capture = review_unsealed(project);
    assert!(capture["evidenceLimits"].to_string().contains("Library protection inventory is incomplete:"), "{capture}");
}
#[test]
fn capture_seal_repair3_new_library_opens_with_damaged_list_and_retries_on_reopen() {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    let library = repair3_library(&project, "new-library");
    let list = f.root().join("capture-seal-libraries.json");
    fs::write(&list, b"truncated list").unwrap();
    let mut runtime = crate::runtime_session::WorkflowRootSession::default();
    let id = repair3_open(&mut runtime, &library);
    repair3_refused(&f, &project);
    fs::remove_file(&list).unwrap();
    // Removing the damaged file does not discard a root observed this process.
    repair3_refused(&f, &project);
    assert_eq!(repair3_open(&mut runtime, &library), id);
    let roots: serde_json::Value = serde_json::from_slice(&fs::read(&list).unwrap()).unwrap();
    assert_eq!(roots["roots"], serde_json::json!([library]));
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
}
#[test]
fn capture_seal_repair3_new_library_opens_when_list_cannot_be_written() {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    let library = repair3_library(&project, "new-library");
    let list = f.root().join("capture-seal-libraries.json");
    fs::set_permissions(f.root(), fs::Permissions::from_mode(0o500)).unwrap();
    let mut runtime = crate::runtime_session::WorkflowRootSession::default();
    let opened = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        let id = repair3_open(&mut runtime, &library);
        assert!(!list.exists(), "the read-only folder must actually have prevented list publication");
        repair3_refused(&f, &project); // still read-only: admission holds its join without retrying a write
        id
    }));
    // Always restore fixture ownership before an assertion failure unwinds.
    fs::set_permissions(f.root(), fs::Permissions::from_mode(0o700)).unwrap();
    let id = opened.unwrap();
    repair3_refused(&f, &project); // writable again, but the remembered root is still not persisted
    assert_eq!(repair3_open(&mut runtime, &library), id);
    assert!(list.is_file());
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
}
#[test]
fn capture_seal_repair3_already_open_library_reopens_with_damaged_list() {
    let f = SelectedInstallation::new(); let project = f.project();
    let library = repair3_library(&project, "existing-library");
    let mut runtime = crate::runtime_session::WorkflowRootSession::default();
    let id = repair3_open(&mut runtime, &library);
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    let list = f.root().join("capture-seal-libraries.json");
    let original = fs::read(&list).unwrap();
    fs::write(&list, b"truncated list").unwrap();
    assert_eq!(repair3_open(&mut runtime, &library), id);
    repair3_refused(&f, &project);
    fs::write(&list, &original).unwrap();
    assert_eq!(repair3_open(&mut runtime, &library), id);
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
}
#[test]
fn capture_seal_repair3_pending_root_capture_vetoes_and_keychain_sealing_is_unaffected() {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    f.enroll().unwrap();
    let library = repair3_library(&project, "pending-library");
    let examples: serde_json::Value = serde_json::from_str(include_str!("../schemas/fixtures/aac.capture-evidence.example.valid.json")).unwrap();
    let mut capture = examples["instances"].as_array().unwrap().iter().find(|c| c["actKind"] == "A15").unwrap().clone();
    crate::capture_seal::seal(&library, &mut capture).unwrap();
    let path = crate::storage::capture_file_for(&library, &capture).unwrap();
    crate::storage::create_json(&path, &capture).unwrap(); let original = fs::read(&path).unwrap();
    let list = f.root().join("capture-seal-libraries.json");
    fs::write(&list, b"damaged list").unwrap();
    let mut runtime = crate::runtime_session::WorkflowRootSession::default();
    repair3_open(&mut runtime, &library);
    let keychain_capture = review_publish(&project);
    assert_eq!(keychain_capture["sealProvider"], "keychain", "inventory never gates keychain sealing");
    // Isolate the remembered library veto from this project's keychain capture.
    fs::remove_file(crate::storage::capture_file_for(&project, &keychain_capture).unwrap()).unwrap();
    f.clear_protected_state(); admission::forget(f.root());
    // A valid list can no longer hide a root already observed in this process.
    let other = repair3_library(&project, "other-library");
    fs::write(&list, serde_json::to_vec(&serde_json::json!({"format":"chirality.app.capture-seal-library-inventory/v1","roots":[other],"complete":true})).unwrap()).unwrap();
    let error = crate::capture_seal::seal(&project, &mut f.ordinary_capture()).unwrap_err();
    assert_eq!(error.cause, Cause::ProtectionInconsistent);
    // A found sign, not an incomplete inventory: the earlier words are kept.
    assert!(!error.detail.contains("inventory is incomplete"), "{error:?}");
    assert!(error.detail.contains("keychain-labelled capture survives in a known library"), "remembered roots must be scanned as well as listed roots: {error:?}");
    assert_eq!(fs::read(path).unwrap(), original);
}

#[test]
fn capture_seal_boundary_valid_library_list_rewrite_admits_file_key_in_a_fresh_process() {
    for subset in [false, true] {
        let f = SelectedInstallation::new(); let project = f.project();
        assert_eq!(review_publish(&project)["sealProvider"], "file-key");
        f.enroll().unwrap();
        let retained = repair3_library(&project, "retained-library");
        let examples: serde_json::Value = serde_json::from_str(include_str!("../schemas/fixtures/aac.capture-evidence.example.valid.json")).unwrap();
        let mut capture = examples["instances"].as_array().unwrap().iter().find(|c| c["actKind"] == "A15").unwrap().clone();
        crate::capture_seal::seal(&retained, &mut capture).unwrap();
        let path = crate::storage::capture_file_for(&retained, &capture).unwrap();
        crate::storage::create_json(&path, &capture).unwrap(); let original = fs::read(&path).unwrap();
        let other = repair3_library(&project, "other-readable-library");
        let list = f.root().join("capture-seal-libraries.json");
        let write = |roots: Vec<PathBuf>| fs::write(&list, serde_json::to_vec(&serde_json::json!({
            "format":"chirality.app.capture-seal-library-inventory/v1","roots":roots,"complete":true})).unwrap()).unwrap();
        write(if subset {vec![retained.clone(), other.clone()]} else {vec![retained.clone()]});
        f.clear_protected_state(); admission::forget(f.root());
        review_inventory_unsealed(&project); // intact-list control
        write(vec![other]); // redirect, then separately omit one root from a subset
        let status = std::process::Command::new(std::env::current_exe().unwrap())
            .args(["--exact", "capture_seal_keychain::tests::capture_seal_review_library_fresh_process_probe", "--ignored", "--nocapture", "--test-threads=1"])
            .env("CHIRALITY_SEAL_LIBRARY_FIXTURE_ROOT", f.root())
            .env("CHIRALITY_SEAL_LIBRARY_REWRITE_BOUNDARY", "1").status().unwrap();
        assert!(status.success(), "boundary must show file admission after a valid rewrite, subset={subset}");
        assert_eq!(fs::read(path).unwrap(), original, "the omitted keychain capture is unchanged");
    }
}

#[test]
fn capture_seal_repair3_unreadable_list_still_allows_library_access() {
    let f = SelectedInstallation::new(); let project = f.project();
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
    let library = repair3_library(&project, "new-library");
    let list = f.root().join("capture-seal-libraries.json");
    fs::create_dir(&list).unwrap(); // present, but not a readable regular list
    let mut runtime = crate::runtime_session::WorkflowRootSession::default();
    let id = repair3_open(&mut runtime, &library);
    repair3_refused(&f, &project);
    fs::remove_dir(&list).unwrap();
    assert_eq!(repair3_open(&mut runtime, &library), id);
    assert_eq!(review_publish(&project)["sealProvider"], "file-key");
}
