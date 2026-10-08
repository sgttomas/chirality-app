//! Explicit staged successor route. No S3 issuer or installed-custody verifier
//! exists yet, so production always refuses. Development checks never qualify.
use super::{HostConfig, CREDENTIAL_VARS, DECLARED_PIN};
use crate::distribution_preflight::{self as tree, Inventory, LaunchPlan};
use serde_json::{json, Value};
use std::io::Read;
use std::os::fd::AsRawFd;
use std::os::unix::process::CommandExt;
use std::path::{Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::time::{Duration, Instant};

#[derive(Clone, Debug)]
pub(crate) enum Distribution {
    Production { resources: PathBuf },
    Development { root: PathBuf },
}
impl Distribution {
    pub(crate) fn vendor_root(&self) -> PathBuf {
        match self { Self::Production { resources } => resources.join("codex"), Self::Development { root } => root.clone() }
    }

    pub(crate) fn development_from_binary(binary: &Path) -> Result<Self, String> {
        if binary.file_name().is_none_or(|n| n != "codex")
            || binary
                .parent()
                .and_then(Path::file_name)
                .is_none_or(|n| n != "bin")
        {
            return Err("successor development requires vendor-root/bin/codex".into());
        }
        Ok(Self::Development {
            root: binary
                .parent()
                .unwrap()
                .parent()
                .ok_or("vendor root absent")?
                .to_owned(),
        })
    }
}
/// Called only by native setup with Tauri's resource directory. Public legacy
/// binary/assertion/development fields cannot replace this production root.
pub(crate) fn production_config(
    resources: PathBuf,
    account: PathBuf,
    probe: PathBuf,
    cwd: PathBuf,
) -> HostConfig {
    let mut cfg = HostConfig::new(resources.join("codex/bin/codex"), account, probe, cwd);
    cfg.distribution = Some(Distribution::Production { resources });
    cfg
}
pub(crate) struct Prepared {
    pub plan: LaunchPlan,
    root: PathBuf,
    inventory: Inventory,
    pub label: String,
    pub verification: Value,
    pub status: Value,
}
impl Prepared {
    pub fn revalidate(&self) -> Result<(), String> {
        tree::revalidate(&self.root, &self.inventory)
            .map(|_| ())
            .map_err(|e| format!("mismatch: {e}"))
    }
    pub fn legacy_inventory(&self) -> Vec<Value> {
        self.inventory
            .entries
            .iter()
            .filter_map(|e| {
                e.sha256.as_ref().map(
                    |sha| json!({"path":e.path,"identity":{"algorithm":"sha-256","value":sha}}),
                )
            })
            .collect()
    }
}
pub(crate) fn configure(cmd: &mut Command, plan: &LaunchPlan) {
    cmd.env("PATH", &plan.path);
    for name in CREDENTIAL_VARS.iter().copied().chain(plan.removed) {
        cmd.env_remove(name);
    }
}
fn isolated(root: &Path, cfg: &HostConfig) -> Result<(), String> {
    // Canonical equality also catches ancestor aliases. Scanner checks vendor
    // no-follow traversal independently; homes must already have been admitted.
    let root = root.canonicalize().map_err(|e| e.to_string())?;
    let account = cfg.codex_home.canonicalize().map_err(|e| e.to_string())?;
    let probe = cfg.probe_home.canonicalize().map_err(|e| e.to_string())?;
    for (a, b) in [(&root, &account), (&root, &probe), (&account, &probe)] {
        if a.starts_with(b) || b.starts_with(a) {
            return Err("mismatch: vendor/probe/account domains overlap".into());
        }
    }
    Ok(())
}
pub(crate) fn prepare(
    distribution: &Distribution,
    cfg: &HostConfig,
    generation: &Value,
) -> Result<Prepared, String> {
    let root = match distribution {
        Distribution::Production { resources } => {
            // Verify the compiled association before any supplier execution.
            // Even future matching reference bytes cannot fabricate trust.
            tree::production_reference(&resources.join("distribution-reference"))?;
            return Err(
                "installed integrity/stable custody issuer unavailable; production refused".into(),
            );
        }
        Distribution::Development { root } => root,
    };
    isolated(root, cfg)?;
    let inventory = tree::scan(root).map_err(|e| format!("mismatch: {e}"))?;
    let inherited = std::env::var_os("PATH")
        .map(|p| p.into_string().map_err(|_| "non UTF-8 inherited PATH"))
        .transpose()?;
    let plan = tree::plan(root, inherited.as_deref()).map_err(|e| format!("mismatch: {e}"))?;
    if let Some(expected) = &cfg.expected_sha256 {
        let measured = inventory
            .entries
            .iter()
            .find(|e| e.path == "bin/codex")
            .and_then(|e| e.sha256.as_deref());
        if measured.is_none_or(|s| !s.eq_ignore_ascii_case(expected)) {
            return Err("mismatch: development binary assertion".into());
        }
    }
    if !super::generated_outputs_match() {
        return Err("mismatch: maintained generated outputs".into());
    }
    let label = probe(&plan, cfg)?;
    if label.strip_suffix('\n').unwrap_or(&label) != format!("codex-cli {DECLARED_PIN}") {
        return Err("mismatch: observed version label".into());
    }
    let status = json!({"format":"host-successor-attempt.s2","verificationGeneration":generation,"inventory":inventory,
        "standing":"unverified-development","resolvedExecutable":plan.executable,"pathPrefix":root.join("codex-path"),
        "rawVersionLabel":label,"limits":["No S3-qualified reference or installed integrity/custody issuer","S1 observation/lifecycle artifact publication not implemented; attempt may have a separate durable reference","Bounded filesystem observations, not an atomic snapshot; check-to-exec race remains"]});
    Ok(Prepared {
        plan,
        root: root.clone(),
        inventory,
        label: label.trim_end_matches('\n').into(),
        verification: json!({"result":"unverifiable","reason":"staged successor development; qualified reference and installed custody unavailable"}),
        status,
    })
}
pub(crate) fn terminate(child: &mut Child) {
    // Spawned by this module/Host in its own process group; never a user process.
    unsafe {
        libc::kill(-(child.id() as i32), libc::SIGKILL);
    }
    let _ = child.kill();
    let _ = child.wait();
}
fn probe(plan: &LaunchPlan, cfg: &HostConfig) -> Result<String, String> {
    let mut command = Command::new(&plan.executable);
    configure(&mut command, plan);
    for flag in &cfg.session_flags {
        command.args(["-c", flag]);
    }
    command
        .arg("--version")
        .env("CODEX_HOME", &cfg.probe_home)
        .current_dir(&cfg.probe_home)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .process_group(0);
    let mut child = command
        .spawn()
        .map_err(|e| format!("label probe unavailable: {e}"))?;
    let mut out = child.stdout.take().unwrap();
    let mut err = child.stderr.take().unwrap();
    for fd in [out.as_raw_fd(), err.as_raw_fd()] {
        if unsafe { libc::fcntl(fd, libc::F_SETFL, libc::O_NONBLOCK) } < 0 {
            terminate(&mut child);
            return Err("cannot bound label probe pipes".into());
        }
    }
    let deadline = Instant::now() + cfg.wait_limit.min(Duration::from_secs(20));
    let mut bytes = Vec::new();
    let mut count = 0usize;
    let result = (|| {
        loop {
            for (pipe, retain) in [
                (&mut out as &mut dyn Read, true),
                (&mut err as &mut dyn Read, false),
            ] {
                let mut chunk = [0u8; 4096];
                // Bound each drain too: a continuously writing child must not
                // prevent timeout/status observation.
                for _ in 0..17 {
                    match pipe.read(&mut chunk) {
                        Ok(0) => break,
                        Ok(n) => {
                            count += n;
                            if count > 65536 {
                                return Err("label probe output limit exceeded".into());
                            }
                            if retain {
                                bytes.extend_from_slice(&chunk[..n]);
                            }
                        }
                        Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => break,
                        Err(e) => return Err(format!("label probe read failed: {e}")),
                    }
                }
            }
            // Observe exit without reaping: the owned leader reserves PID/PGID
            // until group cleanup, so no recycled unrelated group is signalled.
            let mut info: libc::siginfo_t = unsafe { std::mem::zeroed() };
            if unsafe {
                libc::waitid(
                    libc::P_PID,
                    child.id(),
                    &mut info,
                    libc::WEXITED | libc::WNOHANG | libc::WNOWAIT,
                )
            } < 0
            {
                return Err(std::io::Error::last_os_error().to_string());
            }
            if unsafe { info.si_pid() } != 0 {
                if info.si_code != libc::CLD_EXITED || unsafe { info.si_status() } != 0 {
                    return Err("label probe unsuccessful".into());
                }
                // Pipes were drained before status; perform one final bounded
                // read after exit for bytes written between drain and exit observation.
                let mut tail = [0u8; 65537];
                match out.read(&mut tail) {
                    Ok(n) => {
                        count += n;
                        bytes.extend_from_slice(&tail[..n]);
                    }
                    Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => (),
                    Err(e) => return Err(e.to_string()),
                }
                if count > 65536 {
                    return Err("label probe output limit exceeded".into());
                }
                return String::from_utf8(bytes).map_err(|_| "non UTF-8 label probe output".into());
            }
            if Instant::now() >= deadline {
                return Err("label probe timed out".into());
            }
            std::thread::sleep(Duration::from_millis(5));
        }
    })();
    terminate(&mut child); // also closes descendants retaining probe pipes
    result
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::hosting::Host;
    use std::os::unix::fs::PermissionsExt;
    use std::sync::Arc;
    struct Fixture {
        root: PathBuf,
        cfg: HostConfig,
    }
    impl Fixture {
        fn new(probe: &str) -> Self {
            let root = std::env::temp_dir()
                .canonicalize()
                .unwrap()
                .join(crate::util::opaque_id("h3b-").unwrap());
            for d in ["vendor/bin", "vendor/codex-path", "account", "probe"] {
                std::fs::create_dir_all(root.join(d)).unwrap();
            }
            let bin = root.join("vendor/bin/codex");
            let code = format!(
                r#"#!/usr/bin/env python3
import os,sys,json,time
if '--version' in sys.argv:
 {probe}
 print('codex-cli 0.160.0'); sys.exit(0)
for line in sys.stdin:
 f=json.loads(line)
 if 'id' in f:
  print(json.dumps({{'id':f['id'],'result':{{'userAgent':'codex/0.160.0'}}}}),flush=True)
"#
            );
            std::fs::write(&bin, code).unwrap();
            std::fs::set_permissions(&bin, std::fs::Permissions::from_mode(0o700)).unwrap();
            let mut cfg = HostConfig::new(
                bin.clone(),
                root.join("account"),
                root.join("probe"),
                root.clone(),
            );
            cfg.distribution = Some(Distribution::development_from_binary(&bin).unwrap());
            cfg.allow_unverified_dev = true;
            cfg.wait_limit = Duration::from_secs(2);
            Self { root, cfg }
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    fn actual_host_successor_two_spawns_keep_exact_prospective_generation() {
        let f=Fixture::new("assert os.environ['CODEX_HOME'].endswith('/probe'); assert os.environ['PATH'].split(':')[0].endswith('/vendor/codex-path'); assert 'CODEX_MANAGED_BY_NPM' not in os.environ");
        let host = Arc::new(Host::new());
        for counter in [1, 2] {
            let ready = host.start(&f.cfg, "fixture").unwrap();
            assert_eq!(ready["generation"]["spawnCounter"], counter);
            assert_eq!(
                ready["distributionSuccessor"]["verificationGeneration"],
                ready["generation"]
            );
            assert_eq!(ready["supplierStanding"], "unverified-development");
            assert_eq!(ready["versionIdentity"]["declaredPin"], "0.160.0");
            let mut receiver = crate::runtime_session::RuntimeSession::default();
            let received = receiver.receive(&host.observe(&Value::Null, 0));
            assert_eq!(received["nativeView"]["generation"], ready["generation"]);
            assert_eq!(
                received["nativeView"]["supplierStanding"],
                "unverified-development"
            );
            host.stop("fixture", "test complete").unwrap();
        }
    }
    #[test]
    fn actual_host_lt09_passes_explicit_successor_label_join() {
        let f = Fixture::new("pass");
        let host = Arc::new(Host::new());
        let ready = host.start(&f.cfg, "fixture").unwrap();
        let event = host.lifecycle_events().into_iter()
            .find(|e| e["transitionId"] == "LT-09").unwrap();
        let observation = json!({
            "raw_version_label": ready["distributionSuccessor"]["rawVersionLabel"],
            "observed_label": "0.160.0", "pin": "0.160.0"
        });
        assert_eq!(event["versionIdentity"]["observedVersionLabel"], "codex-cli 0.160.0");
        let result = crate::distribution_semantics::validate_label_join(&event, &observation);
        host.stop("fixture", "label join complete").unwrap();
        result.unwrap();
        assert_eq!(crate::distribution_semantics::label_join_identity()["semanticRevision"], "lifecycle-label-join.s2");
    }
    fn attach_store(host: &Host, f: &Fixture) -> PathBuf {
        use crate::hosting::attachment_custody::{NativeHomeNamespace, NativeNamespaceBindings};
        use crate::home_resources::{ExistingHomeReference, HomeClass};
        let home=ExistingHomeReference::new(f.cfg.codex_home.clone(),HomeClass::Account).unwrap();
        let probe=ExistingHomeReference::new(f.cfg.probe_home.clone(),HomeClass::Probe).unwrap();
        let namespaces=NativeNamespaceBindings::from_root(vec![NativeHomeNamespace::received(&home,None),NativeHomeNamespace::received(&probe,None)]).unwrap();
        let data=f.root.join("app-data");std::fs::create_dir(&data).unwrap();
        let store=crate::distribution_store::Store::open(&data,&f.root.join("vendor"),namespaces).unwrap();
        host.configure_distribution_store(Ok(store));data
    }
    #[test]
    fn actual_host_attempt_publication_readback_and_tamper_refusal() {
        let f=Fixture::new("pass");let host=Arc::new(Host::new());let data=attach_store(&host,&f);
        let ready=host.start(&f.cfg,"fixture").unwrap();
        let g=ready["generation"].clone();
        let evidence=host.distribution_evidence(&g);
        host.stop("fixture","store test complete").unwrap();
        assert_eq!(evidence["state"],"read", "{evidence}");
        assert_eq!(evidence["evidence"]["artifact"]["verificationGeneration"],g);
        assert_eq!(evidence["evidence"]["transport"]["sourceSelection"],Value::Null);
        let name=evidence["evidence"]["reference"]["publication"].as_str().unwrap();
        let artifact=data.join("runtime/distribution").join(name).join("attempt.json");
        let bytes=std::fs::read(&artifact).unwrap();
        assert_eq!(tree::digest(&bytes),evidence["evidence"]["reference"]["attemptSha256"]);
        assert_eq!(host.distribution_evidence(&json!({"appSession":"foreign","home":g["home"],"spawnCounter":1}))["state"],"unavailable");
        std::fs::write(&artifact,b"{}").unwrap();
        assert_eq!(host.distribution_evidence(&g)["state"],"unavailable");
    }
    #[test]
    fn native_view_rechecks_artifacts_and_preserves_legacy_standing() {
        let f=Fixture::new("pass");let host=Arc::new(Host::new());let data=attach_store(&host,&f);
        let ready=host.start(&f.cfg,"fixture").unwrap();
        let mut receiver=crate::runtime_session::RuntimeSession::default();
        let view=receiver.receive(&host.observe(&Value::Null,0));
        assert_eq!(view["nativeView"]["distributionEvidence"]["state"],"read");
        assert_eq!(view["nativeView"]["supplierStanding"],"unverified-development");
        let evidence=host.distribution_evidence(&ready["generation"]);
        let name=evidence["evidence"]["reference"]["publication"].as_str().unwrap();
        std::fs::write(data.join("runtime/distribution").join(name).join("injected"),b"extra").unwrap();
        let changed=receiver.receive(&host.observe(&ready["generation"],0));
        host.stop("fixture","native adapter test complete").unwrap();
        assert_eq!(changed["nativeView"]["distributionEvidence"]["state"],"unavailable");
        assert_eq!(changed["nativeView"]["supplierStanding"],"unverified-development");
    }
    #[test]
    fn store_configuration_failure_refuses_before_live_custody() {
        let f=Fixture::new("pass");let host=Arc::new(Host::new());
        host.configure_distribution_store(Err("fixture store failure".into()));
        assert!(host.start(&f.cfg,"fixture").unwrap_err().contains("fixture store failure"));
        assert!(host.snapshot()["generation"].is_null());
        assert!(host.child.lock().unwrap().is_none());
        let native = Arc::new(Host::new());
        let mut cfg = f.cfg.clone();
        cfg.require_distribution_artifacts = true;
        assert!(native.start(&cfg,"fixture").unwrap_err().contains("store not configured"));
        assert!(native.snapshot()["generation"].is_null());
        assert!(native.child.lock().unwrap().is_none());
    }
    #[test]
    fn production_cannot_be_overridden_by_development_fields() {
        let f = Fixture::new("pass");
        let mut cfg = production_config(
            f.root.clone(),
            f.cfg.codex_home.clone(),
            f.cfg.probe_home.clone(),
            f.root.clone(),
        );
        cfg.codex_bin = f.cfg.codex_bin.clone();
        cfg.allow_unverified_dev = true;
        cfg.expected_sha256 = Some(tree::digest(&std::fs::read(&cfg.codex_bin).unwrap()));
        let host = Arc::new(Host::new());
        assert!(host
            .start(&cfg, "fixture")
            .unwrap_err()
            .contains("compiled selection absent"));
        assert!(host.snapshot()["generation"].is_null());
        assert_eq!(host.snapshot()["state"], "refused");
        assert!(host.child.lock().unwrap().is_none());
    }
    #[test]
    fn mutation_during_probe_refuses_before_child_custody() {
        let f = Fixture::new(
            "open(os.path.join(os.path.dirname(__file__),'../changed'),'w').write('mutation')",
        );
        let host = Arc::new(Host::new());
        assert!(host.start(&f.cfg, "fixture").is_err());
        assert!(host.snapshot()["generation"].is_null());
        assert_eq!(host.snapshot()["verification"]["result"], "mismatch");
        assert!(host.child.lock().unwrap().is_none());
    }
    #[test]
    fn stalled_probe_does_not_hold_app_writer_and_is_bounded() {
        let mut f = Fixture::new(
            "open(os.path.join(os.environ['CODEX_HOME'],'entered'),'w').close(); time.sleep(10)",
        );
        f.cfg.wait_limit = Duration::from_millis(150);
        let host = Arc::new(Host::new());
        let h = Arc::clone(&host);
        let cfg = f.cfg.clone();
        let begin = Instant::now();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        while !f.root.join("probe/entered").exists() && begin.elapsed() < Duration::from_secs(1) {
            std::thread::sleep(Duration::from_millis(5));
        }
        assert!(host.recovery_writer.try_lock().is_ok());
        assert!(worker.join().unwrap().unwrap_err().contains("timed out"));
        assert!(begin.elapsed() < Duration::from_secs(2));
        assert!(host.snapshot()["generation"].is_null());
    }
    #[test]
    fn changed_counter_refuses_stale_attempt_without_consuming_another_counter() {
        let f = Fixture::new(
            "open(os.path.join(os.environ['CODEX_HOME'],'entered'),'w').close(); time.sleep(0.2)",
        );
        let host = Arc::new(Host::new());
        let h = Arc::clone(&host);
        let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        let begin = Instant::now();
        while !f.root.join("probe/entered").exists() && begin.elapsed() < Duration::from_secs(1) {
            std::thread::sleep(Duration::from_millis(5));
        }
        assert!(f.root.join("probe/entered").exists());
        let home = format!(
            "app-home:{}",
            crate::util::sha256_hex(f.cfg.codex_home.as_os_str().as_encoded_bytes())
        );
        {
            let _guard = host.recovery_writer.lock().unwrap();
            host.spawn_counters.lock().unwrap().insert(home.clone(), 1);
        }
        assert!(worker
            .join()
            .unwrap()
            .unwrap_err()
            .contains("prospective generation"));
        assert!(host.snapshot()["generation"].is_null());
        assert_eq!(host.spawn_counters.lock().unwrap()[&home], 1);
    }
    #[test]
    fn output_flood_and_home_overlap_refuse() {
        let f = Fixture::new("sys.stdout.write('x'*70000); sys.stdout.flush()");
        let host = Arc::new(Host::new());
        assert!(host
            .start(&f.cfg, "fixture")
            .unwrap_err()
            .contains("output limit"));
        let mut cfg = f.cfg.clone();
        cfg.probe_home = cfg.codex_home.clone();
        assert!(host.start(&cfg, "fixture").unwrap_err().contains("overlap"));
    }
    #[test]
    fn stale_probe_error_does_not_overwrite_successor_state() {
        let f=Fixture::new("open(os.path.join(os.environ['CODEX_HOME'],'entered'),'w').close(); time.sleep(0.2); sys.exit(2)");
        let host = Arc::new(Host::new());
        let h = Arc::clone(&host);
        let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        let begin = Instant::now();
        while !f.root.join("probe/entered").exists() && begin.elapsed() < Duration::from_secs(1) {
            std::thread::sleep(Duration::from_millis(5));
        }
        assert!(f.root.join("probe/entered").exists());
        {
            let mut inner = host.inner.0.lock().unwrap();
            inner.start_attempt += 1;
            inner.state = "ready".into();
        }
        let before = host.snapshot();
        assert!(worker
            .join()
            .unwrap()
            .unwrap_err()
            .contains("stale start attempt"));
        assert_eq!(host.snapshot(), before);
    }
    #[test]
    fn relocation_and_spawn_failure_preserve_counter_and_cleanup() {
        let mut f = Fixture::new("pass");
        let moved = f.root.join("relocated");
        std::fs::rename(f.root.join("vendor"), &moved).unwrap();
        f.cfg.codex_bin = moved.join("bin/codex");
        f.cfg.distribution = Some(Distribution::development_from_binary(&f.cfg.codex_bin).unwrap());
        let host = Arc::new(Host::new());
        let ready = host.start(&f.cfg, "fixture").unwrap();
        assert_eq!(
            ready["distributionSuccessor"]["pathPrefix"],
            moved.join("codex-path").to_str().unwrap()
        );
        host.stop("fixture", "done").unwrap();
        let fresh = Arc::new(Host::new());
        f.cfg.cwd = f.root.join("absent-cwd");
        assert!(fresh
            .start(&f.cfg, "fixture")
            .unwrap_err()
            .contains("spawn failed"));
        assert!(fresh.snapshot()["generation"].is_null());
        assert!(fresh.spawn_counters.lock().unwrap().is_empty());
        assert!(fresh.child.lock().unwrap().is_none());
    }
    #[test]
    fn launcher_removes_credentials_and_wrapper_settings() {
        let f = Fixture::new("pass");
        let plan = tree::plan(&f.root.join("vendor"), Some("inherited:remainder")).unwrap();
        let mut cmd = Command::new("unused");
        configure(&mut cmd, &plan);
        let env: std::collections::HashMap<_, _> = cmd.get_envs().collect();
        for name in CREDENTIAL_VARS.iter().copied().chain(plan.removed) {
            assert_eq!(env.get(std::ffi::OsStr::new(name)), Some(&None));
        }
        assert_eq!(
            env[std::ffi::OsStr::new("PATH")].unwrap(),
            std::ffi::OsStr::new(&plan.path)
        );
    }

    #[test]
    fn exited_probe_leader_keeps_descendants_owned_until_cleanup() {
        let f=Fixture::new("pid=os.fork(); (time.sleep(0.3),open(os.path.join(os.environ['CODEX_HOME'],'survived'),'w').close()) if pid==0 else None; sys.exit(0) if pid==0 else None");
        let host = Arc::new(Host::new());
        host.start(&f.cfg, "fixture").unwrap();
        host.stop("fixture", "done").unwrap();
        std::thread::sleep(Duration::from_millis(400));
        assert!(!f.root.join("probe/survived").exists());
    }
    #[test]
    fn busy_writer_after_audit_refuses_instead_of_waiting_with_stale_scan() {
        let f = Fixture::new(
            "open(os.path.join(os.environ['CODEX_HOME'],'entered'),'w').close(); time.sleep(0.2)",
        );
        let host = Arc::new(Host::new());
        let h = Arc::clone(&host);
        let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        let begin = Instant::now();
        while !f.root.join("probe/entered").exists() && begin.elapsed() < Duration::from_secs(1) {
            std::thread::sleep(Duration::from_millis(5));
        }
        assert!(f.root.join("probe/entered").exists());
        let _guard = host.recovery_writer.lock().unwrap();
        assert!(worker.join().unwrap().unwrap_err().contains("writer busy"));
        assert!(host.snapshot()["generation"].is_null());
        assert!(host.spawn_counters.lock().unwrap().is_empty());
    }
    fn pause_at(
        hook: &std::sync::Mutex<Option<Box<dyn FnOnce() + Send>>>,
    ) -> (std::sync::mpsc::Receiver<()>, std::sync::mpsc::Sender<()>) {
        let (arrive, arrived) = std::sync::mpsc::channel();
        let (resume, resumed) = std::sync::mpsc::channel();
        *hook.lock().unwrap() = Some(Box::new(move || {
            arrive.send(()).unwrap();
            resumed.recv_timeout(Duration::from_secs(10)).unwrap();
        }));
        (arrived, resume)
    }
    #[test]
    fn stop_winning_before_final_gate_prevents_spawn() {
        let f = Fixture::new("pass");
        let host = Arc::new(Host::new());
        let (paused, resume) = pause_at(&host.before_successor_gate);
        let h = Arc::clone(&host);
        let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        paused.recv_timeout(Duration::from_secs(3)).unwrap();
        host.stop("fixture", "cancel pending start").unwrap();
        assert_eq!(host.state(), "stopped");
        let before = host.snapshot();
        resume.send(()).unwrap();
        assert!(worker.join().unwrap().is_err());
        assert_eq!(host.snapshot(), before);
        assert!(host.child.lock().unwrap().is_none());
        assert!(host.spawn_counters.lock().unwrap().is_empty());
    }
    #[test]
    fn stop_after_final_check_waits_for_published_child_then_stops_it() {
        let f = Fixture::new("pass");
        let host = Arc::new(Host::new());
        let (checked, continue_spawn) = pause_at(&host.after_successor_check);
        let (published, continue_handshake) = pause_at(&host.after_successor_publish);
        let h = Arc::clone(&host);
        let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        checked.recv_timeout(Duration::from_secs(3)).unwrap();
        assert!(host.attachment_gate.try_lock().is_err());
        let (stopped_tx, stopped_rx) = std::sync::mpsc::channel();
        let h = Arc::clone(&host);
        let stopper = std::thread::spawn(move || {
            stopped_tx
                .send(h.stop("fixture", "cancel checked start"))
                .unwrap()
        });
        assert!(stopped_rx.recv_timeout(Duration::from_millis(50)).is_err());
        continue_spawn.send(()).unwrap();
        published.recv_timeout(Duration::from_secs(3)).unwrap();
        stopped_rx
            .recv_timeout(Duration::from_secs(5))
            .unwrap()
            .unwrap();
        stopper.join().unwrap();
        assert_eq!(host.state(), "stopped");
        let before = host.snapshot();
        continue_handshake.send(()).unwrap();
        assert!(worker.join().unwrap().is_err());
        assert_eq!(host.snapshot(), before);
        // Host retains the reaped Child handle as historical process evidence.
        // This ordering legitimately spawned; prove it ended rather than
        // incorrectly requiring the never-spawned ordering's empty handle.
        assert!(host
            .child
            .lock()
            .unwrap()
            .as_mut()
            .unwrap()
            .try_wait()
            .unwrap()
            .is_some());
        assert_eq!(
            host.lifecycle_events().last().unwrap()["descendants"]["surviving"],
            0
        );
        assert_eq!(before["generation"]["spawnCounter"], 1);
        assert!(!host
            .lifecycle_events()
            .iter()
            .any(|e| e["transitionId"] == "LT-09"));
    }
    #[test]
    fn stopped_handshake_response_cannot_revive_or_fail_a_later_source() {
        let f = Fixture::new("pass");
        let host = Arc::new(Host::new());
        let (response_arrived, resume) = pause_at(&host.before_successor_settlement);
        let h = Arc::clone(&host);
        let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        response_arrived
            .recv_timeout(Duration::from_secs(3))
            .unwrap();
        let old = host.snapshot()["generation"].clone();
        let old_attempt = host.inner.0.lock().unwrap().start_attempt;
        host.stop("fixture", "cancel handshake completion").unwrap();
        let stopped = host.snapshot();
        resume.send(()).unwrap();
        assert!(worker.join().unwrap().is_err());
        assert_eq!(host.snapshot(), stopped);
        host.start(&f.cfg, "fixture successor").unwrap();
        let next = host.snapshot();
        assert!(host
            .finish_successor_handshake(
                &old,
                old_attempt,
                json!({}),
                Err("old transport failure".into())
            )
            .is_err());
        assert_eq!(host.snapshot(), next);
        host.stop("fixture", "cleanup").unwrap();
    }
    #[test]
    fn busy_source_gate_after_audit_refuses_without_waiting() {
        let f = Fixture::new("pass");
        let host = Arc::new(Host::new());
        let (paused, resume) = pause_at(&host.before_successor_gate);
        let h = Arc::clone(&host);
        let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        paused.recv_timeout(Duration::from_secs(3)).unwrap();
        let _gate = host.attachment_gate.lock().unwrap();
        resume.send(()).unwrap();
        assert!(worker
            .join()
            .unwrap()
            .unwrap_err()
            .contains("source gate busy"));
        assert!(host.snapshot()["generation"].is_null());
        assert!(host.spawn_counters.lock().unwrap().is_empty());
    }
    #[test]
    fn successor_handshake_mismatch_retains_observed_diagnostic_and_refuses_ready() {
        let f = Fixture::new("pass");
        let source = std::fs::read_to_string(&f.cfg.codex_bin)
            .unwrap()
            .replace("codex/0.160.0", "codex/0.159.0");
        std::fs::write(&f.cfg.codex_bin, source).unwrap();
        let host = Arc::new(Host::new());
        assert!(host
            .start(&f.cfg, "fixture")
            .unwrap_err()
            .contains("contradicts declared pin"));
        assert_eq!(host.state(), "halted-after-repeated-failure");
        assert_eq!(
            host.snapshot()["versionIdentity"]["handshakeConsistency"],
            "contradicts-declared-pin"
        );
        assert!(!host
            .lifecycle_events()
            .iter()
            .any(|e| e["transitionId"] == "LT-09"));
        assert!(host.child.lock().unwrap().as_mut().unwrap().wait().is_ok());
    }
}
