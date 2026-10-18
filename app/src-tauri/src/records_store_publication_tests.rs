// Separate App processes initialize one actual selected store. Only scheduling
// is injected; identity publication, strict reading and project attachment are real.
use super::*;
use std::os::unix::fs::MetadataExt;
use std::process::{Child, Command, Output, Stdio};
use std::time::{Duration, Instant};

const CHILD_TEST: &str = "records_store::tests::publication::store_publication_child";
const WAIT: Duration = Duration::from_secs(15);

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
struct Release(PathBuf);
impl Release {
    fn now(&self) {
        std::fs::write(&self.0, b"release actual identity publication").unwrap();
    }
}
impl Drop for Release {
    fn drop(&mut self) {
        let _ = std::fs::write(&self.0, b"release on cleanup");
    }
}
struct Process(Option<Child>);
impl Process {
    fn spawn(root: &Path, mode: &str) -> Self {
        Self(Some(
            Command::new(std::env::current_exe().unwrap())
                .env_clear()
                .env("CHIRALITY_STORE_PUBLICATION_ROOT", root)
                .env("CHIRALITY_STORE_PUBLICATION_MODE", mode)
                .args(["--exact", CHILD_TEST, "--nocapture"])
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .unwrap(),
        ))
    }
    fn finish(&mut self) -> Output {
        let deadline = Instant::now() + WAIT;
        while self.0.as_mut().unwrap().try_wait().unwrap().is_none() {
            assert!(
                Instant::now() < deadline,
                "store-publication child timed out"
            );
            std::thread::sleep(Duration::from_millis(5));
        }
        self.0.take().unwrap().wait_with_output().unwrap()
    }
}
impl Drop for Process {
    fn drop(&mut self) {
        if let Some(child) = self.0.as_mut() {
            let _ = child.kill();
            let _ = child.wait();
        }
    }
}
fn marker(root: &Path, name: &str, value: &Value) {
    let temporary = root.join(format!("{name}.tmp"));
    std::fs::write(&temporary, serde_json::to_vec(value).unwrap()).unwrap();
    std::fs::rename(temporary, root.join(name)).unwrap();
}
fn wait_for(path: &Path) {
    let deadline = Instant::now() + WAIT;
    while !path.exists() {
        assert!(
            Instant::now() < deadline,
            "missing child marker: {}",
            path.display()
        );
        std::thread::sleep(Duration::from_millis(5));
    }
}
fn selected_store(root: &Path, name: &str, project: &Path) -> Store {
    std::fs::create_dir_all(project).unwrap();
    for_app(
        Some(root.join(name)),
        Ok(&root.join("app-data")),
        true,
        Some(project),
        &[],
    )
    .unwrap()
}
fn strict_cold_identities(root: &Path) {
    for kind in [
        "hard-link",
        "symlink",
        "malformed",
        "wrong-format",
        "directory",
        "fifo",
    ] {
        let project = root.join(format!("project-{kind}"));
        let selected = selected_store(root, kind, &project);
        let store = selected.root.clone();
        configure(Ok(selected));
        opened().unwrap();
        let identity = store.join("store.json");
        let original = std::fs::read(&identity).unwrap();
        let retained = store.join("retained-original");
        match kind {
            "hard-link" => std::fs::hard_link(&identity, &retained).unwrap(),
            "symlink" => {
                std::fs::rename(&identity, &retained).unwrap();
                std::os::unix::fs::symlink(&retained, &identity).unwrap();
            }
            "malformed" => std::fs::write(&identity, b"{").unwrap(),
            "wrong-format" => std::fs::write(
                &identity,
                b"{\"format\":\"not-a-records-store\",\"storeId\":\"untrusted\"}\n",
            )
            .unwrap(),
            "directory" => {
                std::fs::remove_file(&identity).unwrap();
                std::fs::create_dir(&identity).unwrap();
            }
            "fifo" => {
                std::fs::remove_file(&identity).unwrap();
                let path = std::ffi::CString::new(identity.as_os_str().as_encoded_bytes()).unwrap();
                assert_eq!(unsafe { libc::mkfifo(path.as_ptr(), 0o600) }, 0);
            }
            _ => unreachable!(),
        }
        *OPENED.lock().unwrap() = None;
        let guard = storage::try_lock_exclusive(&store.join(".store-bootstrap.lock")).unwrap();
        assert!(
            guard.is_some(),
            "there is no cooperating publisher for {kind}"
        );
        drop(guard);
        let started = Instant::now();
        let error = opened().unwrap_err();
        assert!(
            started.elapsed() < Duration::from_secs(1),
            "refused special members must not block: {kind}"
        );
        match kind {
            "hard-link" => {
                assert_eq!(std::fs::metadata(&identity).unwrap().nlink(), 2);
                assert_eq!(std::fs::read(&identity).unwrap(), original);
                assert_eq!(std::fs::read(&retained).unwrap(), original);
            }
            "symlink" => {
                assert!(std::fs::symlink_metadata(&identity)
                    .unwrap()
                    .file_type()
                    .is_symlink());
                assert_eq!(std::fs::read(&retained).unwrap(), original);
            }
            "malformed" => assert_eq!(std::fs::read(&identity).unwrap(), b"{"),
            "wrong-format" => assert_eq!(
                std::fs::read(&identity).unwrap(),
                b"{\"format\":\"not-a-records-store\",\"storeId\":\"untrusted\"}\n"
            ),
            "directory" => assert!(identity.is_dir()),
            "fifo" => {
                use std::os::unix::fs::FileTypeExt;
                assert!(std::fs::symlink_metadata(&identity)
                    .unwrap()
                    .file_type()
                    .is_fifo());
            }
            _ => unreachable!(),
        }
        println!("STRICT_COLD_IDENTITY kind={kind} refused={error}");
    }
}
fn existing_cold_status(root: &Path) {
    for control in ["directory", "absent"] {
        let project = root.join(format!("project-cold-{control}"));
        let selected = selected_store(root, &format!("cold-{control}"), &project);
        let store = selected.root.clone();
        configure(Ok(selected.clone()));
        let (_, original_id) = opened().unwrap();
        let identity = store.join("store.json");
        let original = std::fs::read(&identity).unwrap();
        let bootstrap = store.join(".store-bootstrap.lock");
        std::fs::remove_file(&bootstrap).unwrap();
        if control == "directory" {
            std::fs::create_dir(&bootstrap).unwrap();
        }
        // This is a genuine existing identity with a cold process cache. A
        // status read must not need a writable or usable bootstrap control.
        configure(Ok(selected));
        let observed = status(None);
        assert_eq!(
            observed["state"], "available",
            "valid existing identity must remain readable with {control} control: {observed}"
        );
        assert_eq!(observed["storeId"], original_id);
        assert_eq!(std::fs::read(&identity).unwrap(), original);
        assert_eq!(std::fs::metadata(&identity).unwrap().nlink(), 1);
        if control == "directory" {
            assert!(bootstrap.is_dir());
        } else {
            assert!(
                !bootstrap.exists(),
                "cold status must not create a new control file"
            );
        }
        println!("EXISTING_COLD_STATUS control={control} available=true sameIdentity=true controlUntouched=true");
    }
}

fn cached_identities(root: &Path) {
    for kind in ["missing-root", "missing-identity", "changed-id"] {
        let project = root.join(format!("project-{kind}"));
        let selected = selected_store(root, kind, &project);
        let store = selected.root.clone();
        configure(Ok(selected));
        let accepted = opened().unwrap();
        assert_eq!(
            opened().unwrap(),
            accepted,
            "unchanged cached readmission keeps the identity"
        );
        let identity = store.join("store.json");
        let original = std::fs::read(&identity).unwrap();
        let retained = root.join(format!("retained-{kind}"));
        match kind {
            "missing-root" => std::fs::rename(&store, &retained).unwrap(),
            "missing-identity" => std::fs::remove_file(&identity).unwrap(),
            "changed-id" => {
                let mut changed: Value = serde_json::from_slice(&original).unwrap();
                changed["storeId"] = json!("records-store:changed-negative-control");
                std::fs::write(&identity, serde_json::to_vec(&changed).unwrap()).unwrap();
            }
            _ => unreachable!(),
        }
        let error = opened().unwrap_err();
        match kind {
            "missing-root" => {
                assert!(!store.exists());
                assert_eq!(
                    std::fs::read(retained.join("store.json")).unwrap(),
                    original
                );
            }
            "missing-identity" => assert!(
                !identity.exists(),
                "no replacement identity after cached loss"
            ),
            "changed-id" => {
                let changed: Value =
                    serde_json::from_slice(&std::fs::read(identity).unwrap()).unwrap();
                assert_eq!(changed["storeId"], "records-store:changed-negative-control");
            }
            _ => unreachable!(),
        }
        println!("CACHED_IDENTITY kind={kind} refused={error}");
    }
}
fn held_existing_locks(root: &Path) {
    let project = root.join("held-lock-project");
    let selected = selected_store(root, "held-lock-store", &project);
    let store = selected.root.clone();
    configure(Ok(selected));
    let attached = attach(&project, true).unwrap();
    let dir = attached.dir.unwrap();
    let original = opened().unwrap();
    let _store = store_lock(&store).unwrap();
    let _writer = writer_lock(&dir, false).unwrap();
    let other = selected_store(root, "cache-evicting-store", &root.join("other-project"));
    let other = std::thread::spawn(move || {
        use_store_for_test(Some(Ok(other)));
        let result = opened();
        use_store_for_test(None);
        result.unwrap()
    })
    .join()
    .unwrap();
    assert_ne!(other, original);
    assert_eq!(OPENED.lock().unwrap().as_ref().unwrap().1, other.0);
    // Real import/adopt ordering can already hold store -> writer here. A
    // cold cache must not reacquire either of those non-reentrant OS locks.
    assert_eq!(opened().unwrap(), original);
    write_permitted(&dir, &project).unwrap();
    let bootstrap = storage::try_lock_exclusive(&store.join(".store-bootstrap.lock")).unwrap();
    assert!(
        bootstrap.is_some(),
        "bootstrap ownership is not retained by the returned identity"
    );
    drop(bootstrap);
    // Also exercise the coordinated fallback under both higher-level locks.
    // The persistent hard link remains invalid even after bootstrap admission.
    let identity = store.join("store.json");
    let bytes = std::fs::read(&identity).unwrap();
    let alias = store.join("persistent-hard-link");
    std::fs::hard_link(&identity, &alias).unwrap();
    *OPENED.lock().unwrap() = None;
    assert!(opened().unwrap_err().contains("non-plain member"));
    assert_eq!(std::fs::metadata(&identity).unwrap().nlink(), 2);
    assert_eq!(std::fs::read(&identity).unwrap(), bytes);
    std::fs::remove_file(alias).unwrap();
    println!("HELD_LOCKS_READMISSION originalIdentity={} cacheEviction=actual-other-store-opened strictFallback=refused-persistent-hardlink completed=true", original.1);
}
fn isolated(mode: &str) {
    let root = Scratch(folder("store-publication-controls-"));
    let mut child = Process::spawn(&root.0, mode);
    let output = child.finish();
    println!(
        "STORE_PUBLICATION_CONTROL {mode} status={} stdout={} stderr={}",
        output.status,
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(output.status.success(), "{mode}");
}

#[test]
fn store_publication_child() {
    let Some(root) = std::env::var_os("CHIRALITY_STORE_PUBLICATION_ROOT").map(PathBuf::from) else {
        return;
    };
    let mode = std::env::var("CHIRALITY_STORE_PUBLICATION_MODE").unwrap();
    match mode.as_str() {
        "strict-cold" => {
            strict_cold_identities(&root);
            return;
        }
        "cached" => {
            cached_identities(&root);
            return;
        }
        "existing-cold-status" => {
            existing_cold_status(&root);
            return;
        }
        "held-locks" => {
            held_existing_locks(&root);
            return;
        }
        _ => (),
    }
    let project = root.join(if mode == "publisher" {
        "project-a"
    } else {
        "project-b"
    });
    let selected = for_app(
        Some(root.join("store")),
        Ok(&root.join("app-data")),
        true,
        Some(&project),
        &[],
    )
    .unwrap();
    configure(Ok(selected));
    if mode == "publisher" {
        let pause_root = root.clone();
        storage::after_create_link_for_test(Some(Box::new(move |path| {
            assert_eq!(path, pause_root.join("store/store.json"));
            let bytes = std::fs::read(path).unwrap();
            let identity: Value = serde_json::from_slice(&bytes).unwrap();
            marker(
                &pause_root,
                "published.json",
                &json!({"pid":std::process::id(),"nlink":std::fs::metadata(path).unwrap().nlink(),"storeId":identity["storeId"],"sha256":crate::util::sha256_hex(&bytes)}),
            );
            wait_for(&pause_root.join("release"));
        })));
    } else {
        let blocked_root = root.clone();
        bootstrap_blocked_for_test(Some(Box::new(move || {
            marker(
                &blocked_root,
                "reader-blocked.json",
                &json!({"pid":std::process::id(),"lockAttempt":"actual nonblocking bootstrap acquisition refused while publisher holds lock"}),
            );
        })));
    }
    marker(
        &root,
        &format!("{mode}-entered.json"),
        &json!({"pid":std::process::id()}),
    );
    let result = attach(&project, true);
    let observed = json!({"pid":std::process::id(),"mode":mode,"result":result.as_ref().map(|a|a.view()).map_err(Clone::clone)});
    marker(&root, &format!("{mode}-completed.json"), &observed);
    println!("STORE_PUBLICATION_CHILD {observed}");
    assert!(
        result.is_ok(),
        "cooperating App initialization must complete after publication: {observed}"
    );
}

#[test]
fn store_publication_cooperating_initializers_wait_for_completed_identity() {
    let root = Scratch(folder("store-publication-cooperation-"));
    for name in ["project-a", "project-b", "app-data"] {
        std::fs::create_dir(root.0.join(name)).unwrap();
    }
    let mut publisher = Process::spawn(&root.0, "publisher");
    let release = Release(root.0.join("release"));
    wait_for(&root.0.join("published.json"));
    let identity = root.0.join("store/store.json");
    let original = std::fs::read(&identity).unwrap();
    let original_id: Value = serde_json::from_slice(&original).unwrap();
    assert_eq!(std::fs::metadata(&identity).unwrap().nlink(), 2);
    let mut reader = Process::spawn(&root.0, "reader");
    wait_for(&root.0.join("reader-entered.json"));
    let deadline = Instant::now() + WAIT;
    while !root.0.join("reader-completed.json").exists()
        && !root.0.join("reader-blocked.json").exists()
    {
        assert!(
            Instant::now() < deadline,
            "reader neither completed nor reached blocked bootstrap acquisition"
        );
        std::thread::sleep(Duration::from_millis(5));
    }
    let completed_while_publishing = root.0.join("reader-completed.json").exists();
    let blocked_on_bootstrap = root.0.join("reader-blocked.json").exists();
    let reader_link_while_publishing = root.0.join("project-b").join(PROJECT_LINK).exists();
    release.now();
    let publisher = publisher.finish();
    let reader = reader.finish();
    for (name, output) in [("publisher", &publisher), ("reader", &reader)] {
        println!(
            "STORE_PUBLICATION_PROCESS {name} status={} stdout={} stderr={}",
            output.status,
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
    }
    assert!(publisher.status.success());
    assert!(
        reader.status.success(),
        "cooperating opener refused instead of waiting for original identity"
    );
    assert!(
        blocked_on_bootstrap,
        "reader must encounter the actual publisher's bootstrap lock"
    );
    assert!(
        !completed_while_publishing,
        "cooperating opener returned before create-once publication completed"
    );
    assert!(
        !reader_link_while_publishing,
        "reader must not mint its project identity before store publication completes"
    );
    println!(
        "STORE_BOOTSTRAP_BLOCKED {}",
        std::fs::read_to_string(root.0.join("reader-blocked.json")).unwrap()
    );
    assert_eq!(std::fs::metadata(&identity).unwrap().nlink(), 1);
    assert_eq!(std::fs::read(&identity).unwrap(), original);
    for project in ["project-a", "project-b"] {
        let link: Value = serde_json::from_slice(
            &std::fs::read(root.0.join(project).join(PROJECT_LINK)).unwrap(),
        )
        .unwrap();
        assert_eq!(link["storeId"], original_id["storeId"]);
    }
    println!(
        "STORE_PUBLICATION_COMPLETED originalId={} originalSha256={} finalNlink=1",
        original_id["storeId"],
        crate::util::sha256_hex(&original)
    );
}

#[test]
fn store_publication_strict_cold_identity_refusals_keep_original_members() {
    isolated("strict-cold");
}
#[test]
fn store_publication_cached_identity_loss_or_change_mints_no_replacement() {
    isolated("cached");
}
#[test]
fn store_publication_existing_valid_cold_status_needs_no_bootstrap_control_write() {
    isolated("existing-cold-status");
}
#[test]
fn store_publication_cache_eviction_under_existing_store_and_writer_locks_does_not_deadlock() {
    isolated("held-locks");
}
