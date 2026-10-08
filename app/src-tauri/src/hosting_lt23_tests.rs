use super::*;
use crate::hosting::AppRuntimeCustody;
use std::sync::mpsc;

fn ready(selected: bool) -> (Fixture, Arc<Host>, Arc<AppRuntimeCustody>, Value) {
    let f = Fixture::new("pass");
    let h = Arc::new(Host::new());
    attach_selected_store(&h, &f, selected.then_some("reference/expected.json"));
    let cap = h.app_runtime_custody().unwrap();
    let g = h.start(&f.cfg, "synthetic LT23").unwrap()["generation"].clone();
    (f, h, cap, g)
}
fn settle(h: &Host, cap: &AppRuntimeCustody, g: &Value) -> Value {
    let end = std::time::Instant::now() + Duration::from_secs(10);
    while cap.terminal_publication.state.lock().unwrap().active {
        assert!(
            std::time::Instant::now() < end,
            "test worker did not complete"
        );
        std::thread::sleep(Duration::from_millis(5));
    }
    h.distribution_evidence(g)
}
fn block(cap: &AppRuntimeCustody) -> (mpsc::Receiver<()>, mpsc::Sender<()>) {
    let (tx, rx) = mpsc::channel();
    let (go, wait) = mpsc::channel();
    *cap.terminal_publication.before_work.lock().unwrap() = Some(Box::new(move || {
        tx.send(()).unwrap();
        wait.recv_timeout(Duration::from_secs(15)).unwrap();
    }));
    (rx, go)
}
#[test]
fn lt23_actual_selected_stop_readback_retains_entire_event_and_lt09_bytes() {
    let (_f, h, cap, g) = ready(true);
    let prior = h
        .inner
        .0
        .lock()
        .unwrap()
        .successor_reference
        .clone()
        .unwrap();
    let store = h.distribution_store_for_admission(true).unwrap().unwrap();
    let old = store.read_s1(&g, &prior).unwrap();
    let mut receiver = crate::runtime_session::RuntimeSession::default();
    assert_eq!(receiver.receive(&h.observe(&Value::Null, 0))["nativeView"]["distributionEvidence"]["state"], "read");
    assert_eq!(
        h.stop("synthetic person", "LT23 control").unwrap()["state"],
        "stopped"
    );
    let got = settle(&h, &cap, &g);
    assert_eq!(got["state"], "read", "{got}");
    let event = h
        .lifecycle_events()
        .into_iter()
        .find(|e| e["transitionId"] == "LT-23")
        .unwrap();
    assert_eq!(got["evidence"]["lifecycle"]["legacy_event"], event);
    assert_eq!(got["evidence"]["artifact"], old["artifact"]);
    assert_eq!(
        got["evidence"]["reference"]["observed"],
        old["reference"]["observed"]
    );
    assert_eq!(store.read_s1(&g, &prior).unwrap(), old);
    let native = receiver.receive(&h.observe(&Value::Null, 0));
    assert_eq!(native["nativeView"]["distributionEvidence"], got);
    assert_eq!(native["nativeView"]["supplierStanding"], "unverified-development");
    assert!(h.stop("synthetic", "repeat").is_err());
    for key in ["sequence", "generation", "transitionId"] {
        let mut wrong = event.clone();
        wrong[key] = match key {
            "sequence" => json!(0),
            "generation" => json!({"appSession":"wrong"}),
            _ => json!("LT-12"),
        };
        assert!(store.publish_lt23(&g, &prior, &wrong).is_err(), "{key}");
    }
    let terminal = h
        .inner
        .0
        .lock()
        .unwrap()
        .successor_reference
        .clone()
        .unwrap();
    assert!(
        store.publish_lt23(&g, &terminal, &event).is_err(),
        "terminal is not an LT09 predecessor"
    );
}
#[test]
fn lt23_blocked_publication_does_not_block_stop_and_then_installs() {
    let (_f, h, cap, g) = ready(false);
    let (rx, go) = block(&cap);
    let (tx, done) = mpsc::channel();
    let source = h.clone();
    std::thread::spawn(move || {
        tx.send(source.stop("synthetic", "blocked artifact"))
            .unwrap();
    });
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    assert_eq!(
        done.recv_timeout(Duration::from_secs(2)).unwrap().unwrap()["state"],
        "stopped"
    );
    assert_eq!(h.distribution_evidence(&g)["state"], "pending");
    go.send(()).unwrap();
    assert_eq!(settle(&h, &cap, &g)["state"], "read");
}
#[test]
fn lt23_panic_and_spawn_failure_settle_pending_and_release_permit() {
    for panic_worker in [true, false] {
        let (_f, h, cap, g) = ready(false);
        if panic_worker {
            *cap.terminal_publication.before_work.lock().unwrap() =
                Some(Box::new(|| panic!("injected publication panic")));
        } else {
            cap.terminal_publication
                .fail_spawn
                .store(true, std::sync::atomic::Ordering::SeqCst);
        }
        h.stop("synthetic", "failure control").unwrap();
        let got = settle(&h, &cap, &g);
        assert_eq!(got["state"], "unavailable");
        assert!(!h.inner.0.lock().unwrap().successor_terminal_pending);
        assert!(got["reason"].as_str().unwrap().contains(if panic_worker {
            "panicked"
        } else {
            "spawn failure"
        }));
    }
}
#[test]
fn lt23_one_app_permit_survives_host_drop_and_refuses_other_home_without_queue() {
    let (_f, h, cap, g) = ready(false);
    let (rx, go) = block(&cap);
    h.stop("synthetic", "retire").unwrap();
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let weak = Arc::downgrade(&h.inner);
    drop(h);
    assert!(weak.upgrade().is_none(), "job must not hold Host/Inner");
    let f2 = Fixture::new("pass");
    let next = Arc::new(Host::new_with_app_custody(cap.clone()).unwrap());
    attach_store(&next, &f2);
    let g2 = next.start(&f2.cfg, "other home").unwrap()["generation"].clone();
    assert_ne!(g["home"], g2["home"]);
    next.stop("synthetic", "busy").unwrap();
    assert!(next.distribution_evidence(&g2)["reason"]
        .as_str()
        .unwrap()
        .contains("busy"));
    go.send(()).unwrap();
    let after = settle(&next, &cap, &g2);
    assert_eq!(after["state"], "unavailable", "no automatic retry");
}
#[test]
fn lt23_closing_disables_install_and_new_jobs_without_wait() {
    let (_f, h, cap, g) = ready(false);
    let (rx, go) = block(&cap);
    h.stop("synthetic", "closing").unwrap();
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    cap.close_distribution_publication();
    assert_eq!(h.distribution_evidence(&g)["state"], "unavailable");
    go.send(()).unwrap();
    assert_eq!(settle(&h, &cap, &g)["state"], "unavailable");
    let (_f2, h2, cap2, g2) = ready(false);
    cap2.close_distribution_publication();
    h2.stop("synthetic", "already closing").unwrap();
    assert!(!cap2.terminal_publication.state.lock().unwrap().active);
    assert_eq!(h2.distribution_evidence(&g2)["state"], "unavailable");
}
#[test]
fn lt23_restart_during_publication_cannot_mutate_new_source() {
    let (f, h, cap, g) = ready(false);
    let (rx, go) = block(&cap);
    h.stop("synthetic", "restart").unwrap();
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let next = h.start(&f.cfg, "new source").unwrap()["generation"].clone();
    assert_ne!(g, next);
    let before = h.distribution_evidence(&next);
    go.send(()).unwrap();
    assert_eq!(settle(&h, &cap, &next), before);
    h.stop("synthetic", "done").unwrap();
    settle(&h, &cap, &next);
}
#[test]
fn lt23_ineligible_stop_reserves_sequence_against_late_lt09_success_and_error() {
    for damage in [false, true] {
        let f = Fixture::new("pass");
        let h = Arc::new(Host::new());
        let data = attach_store(&h, &f);
        let cap = h.app_runtime_custody().unwrap();
        let (tx, rx) = mpsc::channel();
        let (go, wait) = mpsc::channel();
        *h.before_s1_lt09_publish.lock().unwrap() = Some(Box::new(move || {
            tx.send(()).unwrap();
            wait.recv_timeout(Duration::from_secs(15)).unwrap();
        }));
        let source = h.clone();
        let cfg = f.cfg.clone();
        let start = std::thread::spawn(move || source.start(&cfg, "late LT09"));
        rx.recv_timeout(Duration::from_secs(10)).unwrap();
        let g = h.snapshot()["generation"].clone();
        h.stop("synthetic", "ineligible").unwrap();
        let before = h.distribution_evidence(&g);
        assert_eq!(before["state"], "unavailable");
        if damage {
            std::fs::rename(data.join("runtime/distribution"), data.join("original")).unwrap();
            std::fs::create_dir(data.join("runtime/distribution")).unwrap();
        }
        go.send(()).unwrap();
        let _ = start.join().unwrap();
        assert_eq!(h.distribution_evidence(&g), before);
        assert!(!cap.terminal_publication.state.lock().unwrap().active);
    }
}
#[test]
fn lt23_immediate_completion_is_never_overwritten_by_pending() {
    for fail in [false, true] {
        let (_f, h, cap, g) = ready(false);
        if fail {
            *cap.terminal_publication.before_work.lock().unwrap() =
                Some(Box::new(|| panic!("immediate failure")));
        }
        let controller = cap.terminal_publication.clone();
        *cap.terminal_publication.after_spawn.lock().unwrap() = Some(Box::new(move || {
            let end = std::time::Instant::now() + Duration::from_secs(10);
            while controller.lock_state().active {
                assert!(std::time::Instant::now() < end);
                std::thread::sleep(Duration::from_millis(5));
            }
        }));
        h.stop("synthetic", "immediate completion").unwrap();
        assert_eq!(
            h.distribution_evidence(&g)["state"],
            if fail { "unavailable" } else { "read" }
        );
        assert!(!h.inner.0.lock().unwrap().successor_terminal_pending);
    }
}
#[test]
fn lt23_controller_poison_is_failclosed_without_stop_panic() {
    let (_f, h, cap, g) = ready(false);
    let c = cap.terminal_publication.clone();
    let _ = std::panic::catch_unwind(move || {
        let _state = c.state.lock().unwrap();
        panic!("injected controller poison");
    });
    h.stop("synthetic", "poison").unwrap();
    assert_eq!(h.distribution_evidence(&g)["state"], "unavailable");
    cap.close_distribution_publication();
    assert!(cap.terminal_publication.lock_state().closing);
}
#[test]
fn lt23_store_lease_blocks_admission_but_not_stop_then_rechecks_tamper() {
    let (_f, h, cap, g) = ready(false);
    let store = h.distribution_store_for_admission(true).unwrap().unwrap();
    let authority = store.namespace_authority();
    let (tx, rx) = mpsc::channel();
    let (go, wait) = mpsc::channel();
    store.before_s1_audit(move || {
        tx.send(()).unwrap();
        wait.recv_timeout(Duration::from_secs(15)).unwrap();
    });
    h.stop("synthetic", "held store lease").unwrap();
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    assert_eq!(h.snapshot()["state"], "stopped");
    assert!(authority.admission(0).is_err());
    go.send(()).unwrap();
    assert_eq!(settle(&h, &cap, &g)["state"], "read");
    assert!(authority.admission(0).is_ok());
}
#[test]
fn lt23_substituted_root_refuses_without_installing_terminal() {
    let (f, h, cap, g) = ready(false);
    let (rx, go) = block(&cap);
    h.stop("synthetic", "substitute root").unwrap();
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let root = f.root.join("app-data/runtime/distribution");
    std::fs::rename(&root, f.root.join("saved-distribution")).unwrap();
    std::fs::create_dir(&root).unwrap();
    std::fs::set_permissions(&root, std::fs::Permissions::from_mode(0o700)).unwrap();
    go.send(()).unwrap();
    assert_eq!(settle(&h, &cap, &g)["state"], "unavailable");
    assert_eq!(std::fs::read_dir(root).unwrap().count(), 0);
}
#[test]
fn lt23_forced_synthetic_stop_preserves_actual_exit_and_descendant_facts() {
    let f = Fixture::new("pass");
    let bin = f.root.join("vendor/bin/codex");
    let mut code = std::fs::read_to_string(&bin).unwrap();
    code.push_str("\ntime.sleep(30)\n");
    std::fs::write(&bin, code).unwrap();
    let h = Arc::new(Host::new());
    attach_store(&h, &f);
    let cap = h.app_runtime_custody().unwrap();
    let g = h.start(&f.cfg, "forced fixture").unwrap()["generation"].clone();
    h.stop("synthetic", "forced fixture").unwrap();
    let result = settle(&h, &cap, &g);
    assert_eq!(result["state"], "read", "{result}");
    let event = h
        .lifecycle_events()
        .into_iter()
        .find(|e| e["transitionId"] == "LT-23")
        .unwrap();
    assert_eq!(event["exitFacts"]["forcedAfterGrace"], true);
    assert_eq!(result["evidence"]["lifecycle"]["legacy_event"], event);
}
#[test]
fn lt23_closing_before_terminal_capture_blocks_paused_lt09_install() {
    let f = Fixture::new("pass");
    let h = Arc::new(Host::new());
    attach_store(&h, &f);
    let cap = h.app_runtime_custody().unwrap();
    let (tx, rx) = mpsc::channel();
    let (go, wait) = mpsc::channel();
    *h.before_s1_lt09_publish.lock().unwrap() = Some(Box::new(move || {
        tx.send(()).unwrap();
        wait.recv_timeout(Duration::from_secs(15)).unwrap();
    }));
    let source = h.clone();
    let cfg = f.cfg.clone();
    let start = std::thread::spawn(move || source.start(&cfg, "closing LT09"));
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let prior = serde_json::to_value(
        h.inner
            .0
            .lock()
            .unwrap()
            .successor_reference
            .clone()
            .unwrap(),
    )
    .unwrap();
    cap.close_distribution_publication();
    go.send(()).unwrap();
    assert!(start.join().unwrap().unwrap_err().contains("closing"));
    let i = h.inner.0.lock().unwrap();
    assert!(!i.successor_lt09_installed);
    assert_eq!(
        serde_json::to_value(i.successor_reference.clone().unwrap()).unwrap(),
        prior
    );
    drop(i);
    h.stop("synthetic", "closing cleanup").unwrap();
    assert!(!cap.terminal_publication.lock_state().active);
}
#[test]
fn lt23_handshaking_and_prespawn_stops_do_not_invent_predecessor() {
    for prespawn in [false, true] {
        let f = Fixture::new("pass");
        let h = Arc::new(Host::new());
        attach_store(&h, &f);
        let cap = h.app_runtime_custody().unwrap();
        let (paused, resume) = if prespawn {
            pause_at(&h.before_successor_gate)
        } else {
            pause_at(&h.before_successor_settlement)
        };
        let source = h.clone();
        let cfg = f.cfg.clone();
        let start = std::thread::spawn(move || source.start(&cfg, "unsupported Stop"));
        paused.recv_timeout(Duration::from_secs(10)).unwrap();
        h.stop("synthetic", "unsupported source phase").unwrap();
        let g = h.snapshot()["generation"].clone();
        assert!(!cap.terminal_publication.lock_state().active);
        assert!(!h.inner.0.lock().unwrap().successor_lt09_installed);
        let evidence = h.distribution_evidence(&g);
        assert!(
            evidence.is_null() || evidence["state"] == "unavailable",
            "{evidence}"
        );
        resume.send(()).unwrap();
        assert!(start.join().unwrap().is_err());
    }
}
#[test]
fn lt23_inflight_lt09_read_cannot_return_as_current_after_terminal_capture() {
    let (_f, h, cap, g) = ready(false);
    let store = h.distribution_store_for_admission(true).unwrap().unwrap();
    let (tx, rx) = mpsc::channel();
    let (go, wait) = mpsc::channel();
    store.before_s1_audit(move || {
        tx.send(()).unwrap();
        wait.recv_timeout(Duration::from_secs(15)).unwrap();
    });
    let source = h.clone();
    let generation = g.clone();
    let read = std::thread::spawn(move || source.distribution_evidence(&generation));
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    // Keep the terminal worker out of Store until the original read is released.
    let (worker_started, worker_go) = block(&cap);
    h.stop("synthetic", "read race").unwrap();
    worker_started
        .recv_timeout(Duration::from_secs(10))
        .unwrap();
    go.send(()).unwrap();
    let old = read.join().unwrap();
    assert_eq!(old["state"], "unavailable");
    assert!(old["reason"].as_str().unwrap().contains("source changed"));
    worker_go.send(()).unwrap();
    assert_eq!(settle(&h, &cap, &g)["state"], "read");
}
#[test]
fn lt23_closing_linearizes_after_short_installer_without_waiting_for_io() {
    let (_f, h, cap, g) = ready(false);
    let (tx, rx) = mpsc::channel();
    let (go, wait) = mpsc::channel();
    *cap.terminal_publication.before_install.lock().unwrap() = Some(Box::new(move || {
        tx.send(()).unwrap();
        wait.recv_timeout(Duration::from_secs(15)).unwrap();
    }));
    h.stop("synthetic", "installer closing order").unwrap();
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let (done, closed) = mpsc::channel();
    let custody = cap.clone();
    let closer = std::thread::spawn(move || {
        custody.close_distribution_publication();
        done.send(()).unwrap();
    });
    assert!(closed.recv_timeout(Duration::from_millis(30)).is_err());
    go.send(()).unwrap();
    closed.recv_timeout(Duration::from_secs(2)).unwrap();
    closer.join().unwrap();
    assert_eq!(
        settle(&h, &cap, &g)["state"],
        "read",
        "installation linearized before closing remains actual"
    );
}
#[test]
fn lt23_session_end_disables_worker_install_before_waiting_on_rec_writer() {
    let (_f, h, cap, g) = ready(false);
    let (rx, go) = block(&cap);
    h.stop("synthetic", "session end").unwrap();
    rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let writer = cap.writer.lock().unwrap();
    let custody = cap.clone();
    let (done, ended) = mpsc::channel();
    let end = std::thread::spawn(move || {
        done.send(custody.record_app_session_end(&[])).unwrap();
    });
    let limit = std::time::Instant::now() + Duration::from_secs(2);
    while !cap.terminal_publication.lock_state().closing {
        assert!(std::time::Instant::now() < limit);
        std::thread::yield_now();
    }
    assert!(ended.try_recv().is_err());
    assert_eq!(h.distribution_evidence(&g)["state"], "unavailable");
    drop(writer);
    ended.recv_timeout(Duration::from_secs(2)).unwrap().unwrap();
    end.join().unwrap();
    assert!(
        cap.terminal_publication.lock_state().active,
        "session end did not join worker"
    );
    go.send(()).unwrap();
    assert_eq!(settle(&h, &cap, &g)["state"], "unavailable");
}
#[test]
fn lt23_stale_and_closing_panics_do_not_settle_another_source() {
    for closing in [false, true] {
        let (f, h, cap, g) = ready(false);
        let (tx, rx) = mpsc::channel();
        let (go, wait) = mpsc::channel();
        *cap.terminal_publication.before_work.lock().unwrap() = Some(Box::new(move || {
            tx.send(()).unwrap();
            wait.recv_timeout(Duration::from_secs(15)).unwrap();
            panic!("late worker panic");
        }));
        h.stop("synthetic", "late panic").unwrap();
        rx.recv_timeout(Duration::from_secs(10)).unwrap();
        let target = if closing {
            cap.close_distribution_publication();
            g
        } else {
            h.start(&f.cfg, "new source").unwrap()["generation"].clone()
        };
        let before = h.distribution_evidence(&target);
        go.send(()).unwrap();
        assert_eq!(settle(&h, &cap, &target), before);
        if !closing {
            h.stop("synthetic", "cleanup").unwrap();
            settle(&h, &cap, &target);
        }
    }
}
