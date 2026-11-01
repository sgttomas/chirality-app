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
