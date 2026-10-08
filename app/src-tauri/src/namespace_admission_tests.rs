use super::*;
use crate::runtime_session::{
    freeze_root_home_descriptors, prepare_native_key_namespace_coordinated, HomeBootstrapSet,
};
use attachment_custody::{AttachmentCustody, NamespaceAuthority};
use std::os::unix::fs::PermissionsExt;
use std::time::Instant;
struct Fixture {
    root: PathBuf,
    data: PathBuf,
    host: Arc<Host>,
    authority: Arc<NamespaceAuthority>,
    owner: Arc<AttachmentCustody>,
    bootstrap: HomeBootstrapSet,
    store: Arc<crate::distribution_store::Store>,
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(opaque_id("namespace-admit-").unwrap());
        let data = root.join("app");
        for p in [
            &data,
            &data.join("runtime"),
            &root.join("account"),
            &root.join("probe"),
            &root.join("shared/skills"),
            &root.join("vendor"),
        ] {
            std::fs::create_dir_all(p).unwrap();
            std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o700)).unwrap();
        }
        for name in ["config.toml", "AGENTS.md"] {
            std::fs::write(root.join("shared").join(name), b"synthetic").unwrap();
        }
        let cfg = HostConfig::new(
            root.join("never-executed"),
            root.join("account"),
            root.join("probe"),
            root.clone(),
        );
        let targets = [
            Some(root.join("shared/config.toml")),
            Some(root.join("shared/AGENTS.md")),
            Some(root.join("shared/skills")),
        ];
        let bootstrap =
            freeze_root_home_descriptors(&data, &cfg, Some(data.join("key")), targets).unwrap();
        let binding = bootstrap.native_namespaces(false).unwrap();
        let authority = NamespaceAuthority::new(binding.clone());
        let host = Arc::new(Host::new());
        host.configure_recovery_with_namespaces(
            data.join("runtime/recovery.ledger.jsonl"),
            binding.clone(),
        )
        .unwrap();
        let owner = Arc::new(AttachmentCustody::open_shared(&data, authority.clone()).unwrap());
        let store = crate::distribution_store::Store::with_authority(
            crate::distribution_store::Store::open(&data, &root.join("vendor"), binding).unwrap(),
            authority.clone(),
        )
        .unwrap();
        host.configure_distribution_store(Ok(store.clone()));
        Self {
            root,
            data,
            host,
            authority,
            owner,
            bootstrap,
            store,
        }
    }
    fn admit(&self) -> Result<crate::runtime_session::NativeKeyAdmission, String> {
        prepare_native_key_namespace_coordinated(
            &self.bootstrap,
            &self.data,
            &self.host.app_runtime_custody()?,
            &self.authority,
            &[self.store.clone()],
            |_| {},
        )
    }
    fn selections(&self) -> Vec<SelectedTextAttachment> {
        let path = self.root.join("input.txt");
        std::fs::write(&path, b"invented input").unwrap();
        vec![SelectedTextAttachment::from_native_selection(path, None).unwrap()]
    }
    fn live(&self) -> Value {
        app_custody_mock_home(&self.host, &self.root.join("account"))
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = self.host.stop("fixture", "namespace fixture complete");
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
#[test]
fn namespace_admission_busy_epoch_and_writer_leave_old_capabilities_usable() {
    let f = Fixture::new();
    let before = f.host.app_runtime_custody().unwrap().snapshot();
    let lease = f.owner.lease().unwrap();
    assert!(f.admit().err().unwrap().contains("busy"));
    assert_eq!(f.authority.lease().unwrap().epoch(), 0);
    drop(lease);
    assert!(f.owner.lease().is_ok());
    assert_eq!(f.host.app_runtime_custody().unwrap().snapshot(), before);
    let cap = f.host.app_runtime_custody().unwrap();
    let writer = cap.writer.lock().unwrap();
    assert!(f.admit().err().unwrap().contains("busy"));
    drop(writer);
    assert_eq!(f.authority.lease().unwrap().epoch(), 0);
    f.authority.test_epoch(u64::MAX);
    assert!(f.admit().err().unwrap().contains("exhausted"));
    assert_eq!(f.authority.lease().unwrap().epoch(), u64::MAX);
}
#[test]
fn namespace_admission_stale_clone_prepared_and_cold_read_do_not_replay() {
    let f = Fixture::new();
    let g = f.live();
    let packet = f
        .host
        .prepare_attachment_turn(f.owner.clone(), &g, "thread", None, "text", &f.selections())
        .unwrap();
    let old = f.owner.clone();
    let before = f.host.client_requests().len();
    let admitted = f.admit().unwrap();
    assert_eq!(f.authority.lease().unwrap().epoch(), 1);
    assert!(old.lease().err().unwrap().contains("stale"));
    assert!(f
        .host
        .dispatch_attachment_turn(&packet)
        .err()
        .unwrap()
        .contains("stale"));
    assert_eq!(f.host.inner.0.lock().unwrap().send_position, 0);
    assert_eq!(f.host.client_requests().len(), before);
    assert!(old
        .resolve_cold(packet.submission_ref())
        .get("clientMetadata")
        .is_none());
    let cold = f
        .host
        .resolve_attachment_submission(&admitted.attachment, packet.submission_ref());
    assert_eq!(cold["automaticRetry"], false);
    assert!(cold["nativeTurnRef"].is_null());
    assert!(cold.get("sourceWriteConfirmed").is_none());
    assert!(cold["dispatch"].as_str().unwrap().contains("cold"));
    std::fs::remove_file(f.data.join("key/skills")).unwrap();
    assert!(admitted
        .attachment
        .supplies_path(packet.submission_ref())
        .is_err());
}
#[test]
fn namespace_admission_postwrite_response_retained_when_old_link_persistence_refuses() {
    let f = Fixture::new();
    let g = f.live();
    let packet = f
        .host
        .prepare_attachment_turn(f.owner.clone(), &g, "thread", None, "text", &f.selections())
        .unwrap();
    let host = f.host.clone();
    let authority = f.authority.clone();
    let cap = host.app_runtime_custody().unwrap();
    let binding = f.bootstrap.native_namespaces(true).unwrap();
    f.bootstrap.prepare_key().unwrap();
    let attachment =
        AttachmentCustody::prepared_shared(&f.data, authority.clone(), binding.clone(), 1).unwrap();
    let store = f.store.clone();
    let response = json!({"id":packet.source.request_id(),"result":{"turn":complete_turn()}});
    let generation = g.clone();
    *f.host.after_attachment_namespace_write.lock().unwrap() = Some(Box::new(move || {
        let mut admission = authority.admission(0).unwrap();
        cap.commit_namespace_admission(&mut admission, binding, &[store], &attachment)
            .unwrap();
        drop(admission);
        host.on_line(&serde_json::to_vec(&response).unwrap(), &generation);
    }));
    let source = f.host.dispatch_attachment_turn(&packet).unwrap();
    assert_eq!(source.evidence()["writeResult"], "written");
    assert!(source.evidence()["response"].is_object());
    let result = f.host.persist_attachment_observation(&source);
    assert!(result.unwrap_err().contains("stale"));
    let evidence = f
        .host
        .attachment_wait(&source, Duration::from_millis(1))
        .unwrap();
    assert!(evidence["custodyLimit"]
        .as_str()
        .unwrap()
        .contains("unavailable"));
    assert_eq!(f.host.inner.0.lock().unwrap().send_position, 1);
    let current = Arc::new(AttachmentCustody::open_shared(&f.data, f.authority.clone()).unwrap());
    let cold = f
        .host
        .resolve_attachment_submission(&current, packet.submission_ref());
    assert!(cold["nativeTurnRef"].is_null());
    assert_eq!(cold["automaticRetry"], false);
    assert!(cold.get("nativeReplyObserved").is_none());
    assert!(cold["dispatch"].as_str().unwrap().contains("cold"));
}
#[test]
fn namespace_admission_final_geometry_failure_and_unavailable_rec_are_truthful() {
    let f = Fixture::new();
    let binding = f.bootstrap.native_namespaces(true).unwrap();
    f.bootstrap.prepare_key().unwrap();
    let attachment =
        AttachmentCustody::prepared_shared(&f.data, f.authority.clone(), binding.clone(), 1)
            .unwrap();
    let cap = f.host.app_runtime_custody().unwrap();
    let before = cap.snapshot();
    std::fs::remove_file(f.data.join("key/skills")).unwrap();
    let mut admission = f.authority.admission(0).unwrap();
    assert!(cap
        .commit_namespace_admission(&mut admission, binding, &[f.store.clone()], &attachment)
        .is_err());
    drop(admission);
    assert_eq!(f.authority.lease().unwrap().epoch(), 0);
    assert_eq!(cap.snapshot(), before);
    let f = Fixture::new();
    let original = f.host.app_runtime_custody().unwrap();
    let mut missing = AppRuntimeCustody {
        session: original.session.clone(),
        ledger: None,
        writer: original.writer.clone(),
        counters: original.counters.clone(),
        contexts: original.contexts.clone(),
        sources: Mutex::new(vec![]),
        initial_limit: Some("synthetic unavailable REC".into()),
        recovery_path: original.recovery_path.clone(),
        end_observation: Mutex::new(None),
        terminal_publication: original.terminal_publication.clone(),
    };
    let binding = f.bootstrap.native_namespaces(true).unwrap();
    f.bootstrap.prepare_key().unwrap();
    let attachment =
        AttachmentCustody::prepared_shared(&f.data, f.authority.clone(), binding.clone(), 1)
            .unwrap();
    let mut admission = f.authority.admission(0).unwrap();
    let observation = missing
        .commit_namespace_admission(
            &mut admission,
            binding.clone(),
            &[f.store.clone()],
            &attachment,
        )
        .unwrap();
    assert_eq!(observation["ledgerUnavailable"], true);
    assert_eq!(observation["bindingCommitted"], false);
    assert!(missing.ledger.is_none());
    drop(admission);
    missing.recovery_path = None;
    let mut admission = f.authority.admission(1).unwrap();
    assert!(missing
        .commit_namespace_admission(&mut admission, binding, &[], &attachment)
        .is_err());
    drop(admission);
    assert_eq!(f.authority.lease().unwrap().epoch(), 1);
}

#[test]
fn namespace_admission_postcommit_setup_failure_keeps_admitted_protection_and_no_registration_before_commit(
) {
    let f = Fixture::new();
    let cap = f.host.app_runtime_custody().unwrap();
    let before = cap.sources.lock().unwrap().len();
    let admitted = f.admit().unwrap();
    assert_eq!(cap.sources.lock().unwrap().len(), before);
    let status = Mutex::new(admitted.observation.clone());
    for stage in [
        "host construction",
        "home session construction",
        "router binding",
    ] {
        let result: Result<(), String> =
            crate::runtime_session::admitted_key_setup(&status, &admitted.observation, || {
                Err(format!("synthetic {stage} failure"))
            });
        assert!(result.is_err());
        assert_eq!(
            status.lock().unwrap()["state"],
            "protective namespace admitted; key setup unavailable"
        );
        assert_eq!(f.authority.lease().unwrap().epoch(), 1);
        assert!(f.owner.lease().is_err());
        assert!(admitted.attachment.lease().is_ok());
        assert_eq!(cap.sources.lock().unwrap().len(), before);
    }
}
#[test]
fn namespace_admission_writer_busy_at_commit_has_no_partial_assignment() {
    let f = Fixture::new();
    f.bootstrap.prepare_key().unwrap();
    let binding = f.bootstrap.native_namespaces(true).unwrap();
    let attachment =
        AttachmentCustody::prepared_shared(&f.data, f.authority.clone(), binding.clone(), 1)
            .unwrap();
    let cap = f.host.app_runtime_custody().unwrap();
    let writer = cap.writer.lock().unwrap();
    let mut admission = f.authority.admission(0).unwrap();
    assert!(cap
        .commit_namespace_admission(&mut admission, binding, &[f.store.clone()], &attachment)
        .unwrap_err()
        .contains("busy"));
    drop(admission);
    drop(writer);
    assert_eq!(f.authority.lease().unwrap().epoch(), 0);
    assert!(f.owner.lease().is_ok());
}
#[test]
fn namespace_admission_preparation_overlap_refuses_before_key_materialization() {
    let f = Fixture::new();
    let cfg = HostConfig::new(
        f.root.join("never"),
        f.root.join("account"),
        f.root.join("probe"),
        f.root.clone(),
    );
    let bad = freeze_root_home_descriptors(
        &f.data,
        &cfg,
        Some(f.data.join("runtime/distribution/key")),
        [
            Some(f.root.join("shared/config.toml")),
            Some(f.root.join("shared/AGENTS.md")),
            Some(f.root.join("shared/skills")),
        ],
    )
    .unwrap();
    let result = prepare_native_key_namespace_coordinated(
        &bad,
        &f.data,
        &f.host.app_runtime_custody().unwrap(),
        &f.authority,
        &[f.store.clone()],
        |_| panic!("must not install"),
    );
    assert!(result.is_err());
    assert!(!f.data.join("runtime/distribution/key").exists());
    assert_eq!(f.authority.lease().unwrap().epoch(), 0);
}

#[test]
#[ignore = "owned worker invoked by bounded watchdog"]
fn namespace_admission_blocked_write_worker() {
    let log = PathBuf::from(std::env::var_os("CHIRALITY_NS_WATCHDOG").unwrap());
    let f = Fixture::new();
    let mut child = Command::new("/bin/sleep")
        .arg("60")
        .env_clear()
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .process_group(0)
        .spawn()
        .unwrap();
    let pid = child.id() as i32;
    std::fs::write(log.join("pid"), pid.to_string()).unwrap();
    *f.host.stdin.lock().unwrap() = child.stdin.take();
    let stdout = child.stdout.take().unwrap();
    *f.host.child.lock().unwrap() = Some(child);
    let generation = {
        let mut i = f.host.inner.0.lock().unwrap();
        f.host
            .allocate_home_spawn(
                &mut i,
                format!(
                    "app-home:{}",
                    sha256_hex(f.root.join("account").as_os_str().as_encoded_bytes())
                ),
            )
            .unwrap();
        i.attachment_pipe_epoch += 1;
        i.child_pid = Some(pid);
        i.generation =
            json!({"appSession":i.app_session,"home":i.home,"spawnCounter":i.spawn_counter});
        i.state = "ready".into();
        let g = i.generation.clone();
        i.threads
            .push(json!({"generation":g,"threadId":"thread","cwd":"/synthetic"}));
        g
    };
    f.host.spawn_reader(stdout, generation.clone());
    let packet = Arc::new(
        f.host
            .prepare_attachment_turn(
                f.owner.clone(),
                &generation,
                "thread",
                None,
                &"x".repeat(4 * 1024 * 1024),
                &f.selections(),
            )
            .unwrap(),
    );
    let sender = f.host.clone();
    let prepared = packet.clone();
    let (tx, rx) = std::sync::mpsc::channel();
    let worker =
        std::thread::spawn(move || tx.send(sender.dispatch_attachment_turn(&prepared)).unwrap());
    let deadline = Instant::now() + Duration::from_secs(2);
    while f.host.inner.0.lock().unwrap().send_position == 0 && Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(5));
    }
    assert_eq!(f.host.inner.0.lock().unwrap().send_position, 1);
    assert!(matches!(
        rx.recv_timeout(Duration::from_millis(100)),
        Err(std::sync::mpsc::RecvTimeoutError::Timeout)
    ));
    assert!(f.admit().err().unwrap().contains("busy"));
    assert_eq!(f.authority.lease().unwrap().epoch(), 0);
    let started = Instant::now();
    f.host
        .stop("fixture", "namespace blocked write stop")
        .unwrap();
    assert!(started.elapsed() < Duration::from_secs(4));
    let source = rx.recv_timeout(Duration::from_secs(1)).unwrap().unwrap();
    worker.join().unwrap();
    assert_eq!(source.evidence()["writeResult"], "write-failed");
    assert_eq!(f.host.inner.0.lock().unwrap().send_position, 1);
    std::fs::write(
        log.join("passed"),
        b"busy admission unchanged; Stop/EOF completed; one write attempt",
    )
    .unwrap();
}
#[test]
fn namespace_admission_blocked_write_stop_has_bounded_watchdog() {
    let root = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(opaque_id("namespace-watch-").unwrap());
    std::fs::create_dir(&root).unwrap();
    let output = std::fs::File::create(root.join("output")).unwrap();
    let mut child=Command::new(std::env::current_exe().unwrap()).args(["--ignored","--exact","hosting::conversation_transport_tests::namespace_admission_tests::namespace_admission_blocked_write_worker","--nocapture"]).env_clear().env("CHIRALITY_NS_WATCHDOG",&root).stdin(Stdio::null()).stdout(Stdio::from(output)).stderr(Stdio::null()).process_group(0).spawn().unwrap();
    let deadline = Instant::now() + Duration::from_secs(7);
    let status = loop {
        if let Some(status) = child.try_wait().unwrap() {
            break Some(status);
        }
        if Instant::now() >= deadline {
            break None;
        }
        std::thread::sleep(Duration::from_millis(20));
    };
    if !status.as_ref().is_some_and(|s| s.success()) {
        if let Ok(pid) = std::fs::read_to_string(root.join("pid"))
            .and_then(|s| s.parse::<i32>().map_err(std::io::Error::other))
        {
            unsafe {
                libc::killpg(pid, libc::SIGKILL);
            }
        }
        if status.is_none() {
            unsafe {
                libc::killpg(child.id() as i32, libc::SIGKILL);
            }
            let _ = child.wait();
        }
    }
    let output = std::fs::read_to_string(root.join("output")).unwrap();
    assert!(
        status.as_ref().is_some_and(|s| s.success()),
        "watchdog: {status:?} {output}"
    );
    assert!(root.join("passed").exists());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn namespace_admission_actual_postcommit_host_construction_failure_is_not_rolled_back() {
    let f = Fixture::new();
    let admitted = f.admit().unwrap();
    let cap = f.host.app_runtime_custody().unwrap();
    let count = cap.sources.lock().unwrap().len();
    cap.record_app_session_end(&[]).unwrap();
    let status = Mutex::new(admitted.observation.clone());
    let result = crate::runtime_session::admitted_key_setup(&status, &admitted.observation, || {
        Host::new_with_app_custody(cap.clone())
    });
    assert!(result.is_err());
    assert_eq!(cap.sources.lock().unwrap().len(), count);
    assert_eq!(f.authority.lease().unwrap().epoch(), 1);
    assert_eq!(
        status.lock().unwrap()["state"],
        "protective namespace admitted; key setup unavailable"
    );
    assert!(admitted.attachment.lease().is_ok());
}

#[test]
fn namespace_admission_cannot_enter_between_cold_read_and_hot_join() {
    let f = Fixture::new();
    let g = f.live();
    let prepared = f
        .host
        .prepare_attachment_turn(f.owner.clone(), &g, "thread", None, "text", &f.selections())
        .unwrap();
    let authority = f.authority.clone();
    let reached = Arc::new(std::sync::atomic::AtomicBool::new(false));
    let check = reached.clone();
    *f.host.before_attachment_hot_join.lock().unwrap() = Some(Box::new(move || {
        assert!(authority.admission(0).err().unwrap().contains("busy"));
        check.store(true, std::sync::atomic::Ordering::SeqCst);
    }));
    let view = f
        .host
        .resolve_attachment_submission(&f.owner, prepared.submission_ref());
    assert!(reached.load(std::sync::atomic::Ordering::SeqCst));
    assert!(view["sourceStanding"]
        .as_str()
        .unwrap()
        .contains("genuine hot"));
    assert_eq!(f.authority.lease().unwrap().epoch(), 0);
    assert!(f.authority.admission(0).is_ok());
}
#[test]
fn namespace_admission_required_store_absence_and_failure_are_not_safe_omission() {
    let host = Host::new();
    assert!(host.distribution_store_for_admission(true).is_err());
    assert!(host
        .distribution_store_for_admission(false)
        .unwrap()
        .is_none());
    host.configure_distribution_store(Err("synthetic Store unavailable".into()));
    assert!(host.distribution_store_for_admission(false).is_err());
    assert!(host.distribution_store_for_admission(true).is_err());
}
