use super::*;
use std::sync::Mutex;
#[derive(Default)]
struct Mock {
    items: Mutex<BTreeMap<String, Vec<u8>>>,
    reads: Mutex<Vec<ItemIdentity>>,
    adds: Mutex<usize>,
    read_error: Mutex<Option<BackendError>>,
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
    fn run(&self, b: &Mock, o: Operation, key: u8) -> Result<Material, String> {
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
fn seal_keychain_none_never_touches_platform_and_unsigned_file_route_stays() {
    assert!(KEYCHAIN_SELECTION.is_none());
    assert!(KeychainAuthority::current().is_err());
    assert!(!selected_route());
    assert!(enroll_initial(Path::new("/must-not-read")).is_err());
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
        .contains("migration prohibited"));
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
