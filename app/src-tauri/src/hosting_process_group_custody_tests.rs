use super::*;
use crate::hosting::process_group_custody::{Census, OwnedProcess};
use std::sync::Mutex;

fn until(predicate: impl Fn() -> bool) {
    let end = Instant::now() + Duration::from_secs(8);
    while !predicate() {
        assert!(Instant::now() < end, "owned fixture deadline");
        std::thread::sleep(Duration::from_millis(5));
    }
}
fn ready(body: &str) -> (Fixture, Arc<Host>, Value, Arc<OwnedProcess>) {
    let mut f = Fixture::new("pass");
    f.cfg.distribution = None;
    let code=format!("#!/usr/bin/env python3\nimport os,sys,json,subprocess,time\nif '--version' in sys.argv: print('codex-cli 0.160.0'); sys.exit(0)\n{body}\nfor line in sys.stdin:\n f=json.loads(line)\n if f.get('method')=='fixture/exit': sys.exit(7)\n if f.get('method')=='fixture/close-output':\n  os.close(1); time.sleep(30)\n if 'id' in f: print(json.dumps({{'id':f['id'],'result':{{'userAgent':'codex/0.160.0'}}}}),flush=True)\n");
    std::fs::write(&f.cfg.codex_bin, code).unwrap();
    let h = Arc::new(Host::new());
    let g = h.start(&f.cfg, "synthetic custody peer").unwrap()["generation"].clone();
    let process = h.child.lock().unwrap().clone().unwrap();
    (f, h, g, process)
}
struct Cleanup(Arc<OwnedProcess>);
impl Drop for Cleanup {
    fn drop(&mut self) {
        self.0.abort_spawn();
    }
}
fn proof(process: &Arc<OwnedProcess>) -> Arc<Mutex<Vec<&'static str>>> {
    let calls = Arc::new(Mutex::new(Vec::new()));
    let kept = calls.clone();
    *process.before_group_operation.lock().unwrap() = Some(Box::new(move |pid, operation| {
        let mut info = unsafe { std::mem::zeroed::<libc::siginfo_t>() };
        assert_eq!(
            unsafe {
                libc::waitid(
                    libc::P_PID,
                    pid as libc::id_t,
                    &mut info,
                    libc::WEXITED | libc::WNOHANG | libc::WNOWAIT,
                )
            },
            0,
            "every numeric group operation retains the original Child reservation"
        );
        kept.lock().unwrap().push(operation);
    }));
    calls
}
fn exit(h: &Host, g: &Value) {
    h.write_frame_scoped(&json!({"method":"fixture/exit","params":{}}), Some(g))
        .unwrap();
}

#[test]
fn process_group_custody_ready_eof_keeps_descendant_until_later_stop() {
    let (_f,h,g,p)=ready("subprocess.Popen(['/bin/sleep','30'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)");
    let _cleanup = Cleanup(p.clone());
    let calls = proof(&p);
    exit(&h, &g);
    until(|| h.state() == "exited-unexpectedly");
    assert!(
        matches!(p.census(), Census::Complete(1)),
        "unexpected EOF must preserve the actual live descendant"
    );
    assert!(!p.released());
    h.stop("synthetic", "later Stop").unwrap();
    until(|| p.released());
    let event = h
        .lifecycle_events()
        .into_iter()
        .find(|e| e["transitionId"] == "LT-23")
        .unwrap();
    assert_eq!(event["exitFacts"]["exitCode"], 7);
    assert_eq!(event["exitFacts"]["forcedAfterGrace"], true);
    assert_eq!(event["descendants"]["surviving"], 0);
    assert!(calls.lock().unwrap().contains(&"signal"));
    let before = calls.lock().unwrap().len();
    assert_eq!(p.force_if_needed(), (false, None));
    assert!(p.signal(libc::SIGKILL).is_err());
    assert!(p.census().empty());
    assert_eq!(
        calls.lock().unwrap().len(),
        before,
        "retired authority never addresses its numeric group"
    );
}
#[test]
fn process_group_custody_ready_eof_natural_cleanup_and_later_stop_do_not_force_zombie() {
    let (_f,h,g,p)=ready("subprocess.Popen(['/bin/sleep','0.4'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)");
    let _cleanup = Cleanup(p.clone());
    let calls = proof(&p);
    exit(&h, &g);
    until(|| h.state() == "exited-unexpectedly");
    until(|| p.released());
    assert_eq!(p.observe_exit().unwrap().unwrap().code(), Some(7));
    let before = calls.lock().unwrap().len();
    h.stop("synthetic", "after natural cleanup").unwrap();
    let event = h.lifecycle_events().last().unwrap().clone();
    assert_eq!(event["exitFacts"]["forcedAfterGrace"], false);
    assert_eq!(event["descendants"]["surviving"], 0);
    assert_eq!(event["exitFacts"]["exitCode"], 7);
    assert_eq!(calls.lock().unwrap().len(), before);
}
#[test]
fn process_group_custody_live_leader_closing_output_does_not_lock_out_stop() {
    let (_f, h, g, p) = ready("pass");
    let _cleanup = Cleanup(p.clone());
    let calls = proof(&p);
    h.write_frame_scoped(
        &json!({"method":"fixture/close-output","params":{}}),
        Some(&g),
    )
    .unwrap();
    std::thread::sleep(Duration::from_millis(100));
    assert!(p.observe_exit().unwrap().is_none());
    let began = Instant::now();
    h.stop("synthetic", "stdout closed while alive").unwrap();
    assert!(began.elapsed() < Duration::from_secs(7));
    until(|| p.released());
    let event = h.lifecycle_events().last().unwrap().clone();
    assert_eq!(event["exitFacts"]["signal"], libc::SIGKILL.to_string());
    assert_eq!(event["exitFacts"]["forcedAfterGrace"], true);
    assert!(calls.lock().unwrap().contains(&"signal"));
}
#[test]
fn process_group_custody_old_slot_replacement_does_not_wait_or_signal_successor() {
    let (f,h,g,old)=ready("subprocess.Popen(['/bin/sleep','0.6'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)");
    let _old_cleanup = Cleanup(old.clone());
    let (arrived, settle) = pause_at(&h.before_eof_gate);
    exit(&h, &g);
    arrived.recv_timeout(Duration::from_secs(5)).unwrap();
    // Synthetic admission allows slot replacement while the old reader is held.
    // Production direct exited/halted start policy is unchanged.
    h.inner.0.lock().unwrap().state = "stopped".into();
    let fresh = h.start(&f.cfg, "synthetic replacement admission").unwrap()["generation"].clone();
    let successor = h.child.lock().unwrap().clone().unwrap();
    let _new_cleanup = Cleanup(successor.clone());
    assert_ne!(fresh, g);
    assert!(h
        .retired_processes
        .lock()
        .unwrap()
        .iter()
        .any(|p| p.id() == old.id()));
    settle.send(()).unwrap();
    until(|| old.released());
    assert_eq!(h.snapshot()["generation"], fresh);
    assert_eq!(h.state(), "ready");
    assert!(successor.observe_exit().unwrap().is_none());
    h.stop("synthetic", "successor cleanup").unwrap();
}
#[test]
fn process_group_custody_unknown_census_is_null_in_actual_current_publish_readback() {
    let f = Fixture::new("pass");
    let h = Arc::new(Host::new());
    attach_store(&h, &f);
    let cap = h.app_runtime_custody().unwrap();
    let g = h.start(&f.cfg, "synthetic unavailable census").unwrap()["generation"].clone();
    let p = h.child.lock().unwrap().clone().unwrap();
    let _cleanup = Cleanup(p.clone());
    *p.census_override.lock().unwrap() = Some(Census::Unknown(
        "invented partial owned-group inventory".into(),
    ));
    h.stop("synthetic", "unknown census").unwrap();
    let end = Instant::now() + Duration::from_secs(10);
    while cap.terminal_publication.lock_state().active {
        assert!(Instant::now() < end);
        std::thread::sleep(Duration::from_millis(5));
    }
    let event = h.lifecycle_events().last().unwrap().clone();
    assert_eq!(event["transitionId"], "LT-23");
    assert_eq!(event["descendants"]["checked"], false);
    assert!(event["descendants"]["surviving"].is_null());
    assert!(event["descendants"]["handling"]
        .as_str()
        .unwrap()
        .starts_with("unavailable: "));
    assert!(!p.released());
    let read = h.distribution_evidence(&g);
    assert_eq!(read["state"], "read", "{read}");
    assert_eq!(
        read["evidence"]["lifecycle"]["format"],
        "lifecycle-event.s1.v0.10"
    );
    assert_eq!(read["evidence"]["lifecycle"]["legacy_event"], event);
    if let Some(out) = std::env::var_os("CHIRALITY_TEST_OUTPUT_DIRECTORY") {
        std::fs::write(
            PathBuf::from(out).join("process-group-custody-current.json"),
            serde_json::to_vec(&read).unwrap(),
        )
        .unwrap();
    }
    *p.census_override.lock().unwrap() = None;
    until(|| p.released());
}

#[test]
fn process_group_custody_modeled_eintr_at_live_stdout_eof_never_infers_exit() {
    let (_f, h, g, p) = ready("pass");
    let _cleanup = Cleanup(p.clone());
    // Explicit modeled SDK return, not an actual signal-interruption witness.
    p.waitid_errors.lock().unwrap().push_back(libc::EINTR);
    h.write_frame_scoped(
        &json!({"method":"fixture/close-output","params":{}}),
        Some(&g),
    )
    .unwrap();
    until(|| p.waitid_errors.lock().unwrap().is_empty());
    assert!(p.observe_exit().unwrap().is_none());
    assert_eq!(h.state(), "ready");
    assert!(!h
        .lifecycle_events()
        .iter()
        .any(|e| e["transitionId"] == "LT-12"));
    assert!(!h.inner.0.lock().unwrap().server_requests.is_closed(&g));
    h.stop("synthetic", "modeled interruption cleanup").unwrap();
    until(|| p.released());
    assert_eq!(
        h.lifecycle_events().last().unwrap()["exitFacts"]["signal"],
        libc::SIGKILL.to_string()
    );
}
#[test]
fn process_group_custody_modeled_nonterminal_wait_error_keeps_observer_and_stop_available() {
    let (_f, h, g, p) = ready("pass");
    let _cleanup = Cleanup(p.clone());
    p.waitid_errors.lock().unwrap().push_back(libc::EIO); // modeled, not an OS witness
    h.write_frame_scoped(
        &json!({"method":"fixture/close-output","params":{}}),
        Some(&g),
    )
    .unwrap();
    until(|| {
        h.journal()
            .iter()
            .any(|e| e["class"] == "process-exit-observation-unavailable")
    });
    assert!(p.observe_exit().unwrap().is_none());
    assert!(!p.released());
    assert_eq!(h.state(), "ready");
    assert!(!h
        .lifecycle_events()
        .iter()
        .any(|e| e["transitionId"] == "LT-12"));
    assert!(!h.inner.0.lock().unwrap().server_requests.is_closed(&g));
    assert_eq!(
        h.journal()
            .iter()
            .filter(|e| e["class"] == "process-exit-observation-unavailable")
            .count(),
        1
    );
    h.stop("synthetic", "observation recovery cleanup").unwrap();
    until(|| p.released());
    let terminal = h.lifecycle_events().last().unwrap().clone();
    assert_eq!(terminal["transitionId"], "LT-23");
    assert_eq!(terminal["exitFacts"]["signal"], libc::SIGKILL.to_string());
}
