use super::*;

fn fixture(successor: bool, body: &str) -> Fixture {
    let mut f = Fixture::new("pass");
    if !successor { f.cfg.distribution = None; }
    peer(&f, body);
    f
}
fn peer(f: &Fixture, body: &str) {
    let code = format!("#!/usr/bin/env python3\nimport sys,json\nif '--version' in sys.argv:\n print('codex-cli 0.160.0'); sys.exit(0)\n{body}\n");
    std::fs::write(&f.cfg.codex_bin, code).unwrap();
}
fn until(h: &Host, predicate: impl Fn(&Host) -> bool) {
    let end = Instant::now() + Duration::from_secs(5);
    while !predicate(h) {
        assert!(Instant::now() < end, "startup fixture deadline: {}", h.snapshot());
        std::thread::sleep(Duration::from_millis(5));
    }
}
fn failures(h: &Host) -> Vec<Value> {
    h.lifecycle_events().into_iter().filter(|e| e["transitionId"] == "LT-11").collect()
}
const READY: &str = "for line in sys.stdin:\n f=json.loads(line)\n if 'id' in f: print(json.dumps({'id':f['id'],'result':{'userAgent':'codex/0.160.0'}}),flush=True)";
const EARLY_EXIT: &str = "print(json.dumps({'method':'fixture/never-ready','params':{'synthetic':True}}),flush=True)\nprint('invented startup refusal',file=sys.stderr,flush=True)\nsys.exit(7)";

#[test]
fn startup_refusal_eof_ends_only_its_own_surviving_descendant_group() {
    struct Descendant(i32);
    impl Drop for Descendant {
        fn drop(&mut self) { if self.0 > 0 { unsafe { libc::kill(self.0, libc::SIGKILL); } } }
    }
    for successor in [false, true] {
        let f = fixture(successor, "import os,subprocess\nchild=subprocess.Popen(['/bin/sleep','30'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\nwith open(os.environ['CODEX_HOME']+'/owned-descendant','w') as out: out.write(str(child.pid))\nsys.exit(7)");
        let h = Arc::new(Host::new());
        let (proof, observed) = std::sync::mpsc::channel();
        let descendant_path = f.cfg.codex_home.join("owned-descendant");
        *h.before_startup_eof_signal.lock().unwrap() = Some(Box::new(move |pid| {
            let mut info = unsafe { std::mem::zeroed::<libc::siginfo_t>() };
            // WNOWAIT observes the owned child's status without releasing its PID.
            let unreaped = unsafe { libc::waitid(libc::P_PID, pid as libc::id_t, &mut info,
                libc::WEXITED | libc::WNOHANG | libc::WNOWAIT) } == 0;
            let descendant = std::fs::read_to_string(descendant_path).ok().and_then(|v| v.parse::<i32>().ok());
            let survived = descendant.is_some_and(|pid| pid > 0 && unsafe { libc::kill(pid, 0) } == 0);
            proof.send((unreaped, survived)).unwrap();
        }));
        let (published, dispatch) = pause_at(&h.after_successor_publish);
        let (eof, settle_eof) = pause_at(&h.before_eof_gate);
        let source = h.clone(); let cfg = f.cfg.clone();
        let start = std::thread::spawn(move || source.start(&cfg, "synthetic descendant startup"));
        published.recv_timeout(Duration::from_secs(5)).unwrap(); eof.recv_timeout(Duration::from_secs(5)).unwrap();
        let pid: i32 = std::fs::read_to_string(f.cfg.codex_home.join("owned-descendant")).unwrap().parse().unwrap();
        assert!(pid > 0); let mut owned = Descendant(pid);
        let (unreaped, survived) = observed.recv_timeout(Duration::from_secs(5)).unwrap();
        let g = h.snapshot()["generation"].clone();
        settle_eof.send(()).unwrap();
        until(&h, |h| h.state() == "halted-after-repeated-failure");
        dispatch.send(()).unwrap(); assert!(start.join().unwrap().is_err());
        until(&h, |_| unsafe { libc::kill(pid, 0) } != 0);
        owned.0 = 0; // The observed ended child needs no cleanup signal.
        assert!(unreaped, "startup group signal must precede reaping the owning child");
        assert!(survived, "owned descendant must actually survive its parent before cleanup");
        assert_eq!(failures(&h).len(), 1); assert_eq!(failures(&h)[0]["exitFacts"]["exitCode"], 7);
        assert_eq!(failures(&h)[0]["generation"], g);
        drop(owned);
    }
}

#[test]
fn startup_refusal_eof_before_initialize_settles_first_start_and_restart() {
    for successor in [false, true] { for restart in [false, true] {
        let f = fixture(successor, READY);
        let h = Arc::new(Host::new());
        if restart {
            h.start(&f.cfg, "synthetic prior start").unwrap();
            h.stop("synthetic", "restart fixture").unwrap();
        }
        peer(&f, EARLY_EXIT);
        let (published, dispatch) = pause_at(&h.after_successor_publish);
        let (eof, settle) = pause_at(&h.before_eof_gate);
        let source = h.clone(); let cfg = f.cfg.clone();
        let start = std::thread::spawn(move || source.start(&cfg, "synthetic early exit"));
        published.recv_timeout(Duration::from_secs(5)).unwrap();
        eof.recv_timeout(Duration::from_secs(5)).unwrap();
        until(&h, |h| h.inner.0.lock().unwrap().stderr_bytes > 0);
        let g = h.snapshot()["generation"].clone();
        settle.send(()).unwrap();
        until(&h, |h| h.state() == "halted-after-repeated-failure");
        dispatch.send(()).unwrap();
        assert!(start.join().unwrap().is_err());
        assert_eq!(h.state(), "halted-after-repeated-failure");
        let events = failures(&h); assert_eq!(events.len(), 1);
        let event = &events[0];
        assert_eq!(event["generation"], g);
        assert_eq!(event["fromState"], "handshaking");
        assert_eq!(event["failureCount"], 1);
        assert_eq!(event["exitFacts"]["exitCode"], 7);
        assert_eq!(event["exitFacts"]["diagnosticOutputBytes"], b"invented startup refusal\n".len());
        assert_eq!(event["exitFacts"]["lastReceiptPosition"], 1);
        assert_eq!(event["closedGeneration"]["unknownNoResponse"], 0);
        let frame = h.journal().into_iter().find(|f| f["frame"]["method"] == "fixture/never-ready").unwrap();
        assert_eq!(frame["generation"], g); assert_eq!(frame["generationNeverReady"], true);
        let before = h.snapshot(); h.on_eof(&g); assert_eq!(h.snapshot(), before);
        assert_eq!(failures(&h).len(), 1);
    }}
}

#[test]
fn startup_refusal_eof_with_initialize_pending_settles_without_second_lt11() {
    for successor in [false, true] {
        let f = fixture(successor, "for line in sys.stdin:\n f=json.loads(line)\n if f.get('method')=='initialize': sys.exit(9)");
        let h = Arc::new(Host::new());
        assert!(h.start(&f.cfg, "synthetic initialize refusal").is_err());
        let g = h.snapshot()["generation"].clone();
        until(&h, |h| h.state() == "halted-after-repeated-failure");
        assert!(h.inner.0.lock().unwrap().server_requests.is_closed(&g));
        assert_eq!(h.state(), "halted-after-repeated-failure");
        let events = failures(&h); assert_eq!(events.len(), 1);
        assert_eq!(events[0]["exitFacts"]["exitCode"], 9);
        assert_eq!(events[0]["closedGeneration"]["unknownNoResponse"], 1);
        assert_eq!(h.snapshot()["clientRequests"][0]["outcome"], "unknown-no-response");
    }
}

#[test]
fn startup_refusal_known_initialize_reply_then_eof_never_becomes_ready() {
    for successor in [false, true] {
        let f = fixture(successor, "for line in sys.stdin:\n f=json.loads(line)\n if f.get('method')=='initialize':\n  print(json.dumps({'id':f['id'],'result':{'userAgent':'codex/0.160.0'}}),flush=True)\n  sys.exit(0)");
        let h = Arc::new(Host::new());
        let (eof, settle_eof) = pause_at(&h.before_eof_gate);
        let (reply, settle_reply) = pause_at(&h.before_successor_settlement);
        let source = h.clone(); let cfg = f.cfg.clone();
        let start = std::thread::spawn(move || source.start(&cfg, "synthetic replied then exited"));
        reply.recv_timeout(Duration::from_secs(5)).unwrap();
        eof.recv_timeout(Duration::from_secs(5)).unwrap();
        let g = h.snapshot()["generation"].clone();
        assert_eq!(h.client_requests()[0]["outcome"], "response-observed-result");
        settle_eof.send(()).unwrap();
        until(&h, |h| h.state() == "halted-after-repeated-failure");
        let before = h.snapshot();
        settle_reply.send(()).unwrap(); assert!(start.join().unwrap().is_err());
        assert_eq!(h.snapshot(), before);
        assert_eq!(failures(&h).len(), 1);
        assert_eq!(failures(&h)[0]["exitFacts"]["exitCode"], 0);
        assert_eq!(failures(&h)[0]["closedGeneration"]["unknownNoResponse"], 0);
        assert!(!h.lifecycle_events().iter().any(|e| e["transitionId"] == "LT-09"));
        assert!(h.journal().iter().any(|f| f["generation"] == g && f["generationNeverReady"] == true && f["frame"]["result"]["userAgent"] == "codex/0.160.0"));
    }
}

#[test]
fn startup_refusal_stop_or_app_quit_winning_eof_remains_stopped() {
    for successor in [false, true] { for reason in ["synthetic Stop", "App quit"] {
        let f = fixture(successor, EARLY_EXIT); let h = Arc::new(Host::new());
        let (published, dispatch) = pause_at(&h.after_successor_publish);
        let (eof, settle_eof) = pause_at(&h.before_eof_gate);
        let source = h.clone(); let cfg = f.cfg.clone();
        let start = std::thread::spawn(move || source.start(&cfg, "synthetic stop race"));
        published.recv_timeout(Duration::from_secs(5)).unwrap(); eof.recv_timeout(Duration::from_secs(5)).unwrap();
        let source = h.clone(); let stop = std::thread::spawn(move || source.stop("synthetic", reason));
        until(&h, |h| h.state() == "stopping");
        settle_eof.send(()).unwrap(); stop.join().unwrap().unwrap();
        let before = h.snapshot(); dispatch.send(()).unwrap(); assert!(start.join().unwrap().is_err());
        assert_eq!(h.snapshot(), before); assert_eq!(h.state(), "stopped"); assert!(failures(&h).is_empty());
        assert!(h.journal().iter().any(|f| f["frame"]["method"] == "fixture/never-ready" && f["generationNeverReady"] == true));
        assert_eq!(h.lifecycle_events().last().unwrap()["transitionId"], "LT-23");
        assert_eq!(h.lifecycle_events().last().unwrap()["exitFacts"]["exitCode"], 7);
    }}
}

#[test]
fn startup_refusal_stale_eof_and_late_handshake_cannot_close_ready_successor() {
    for successor in [false, true] {
        let f = fixture(successor, EARLY_EXIT); let h = Arc::new(Host::new());
        let (published, dispatch) = pause_at(&h.after_successor_publish);
        let (eof, settle_eof) = pause_at(&h.before_eof_gate);
        let source = h.clone(); let cfg = f.cfg.clone();
        let start = std::thread::spawn(move || source.start(&cfg, "synthetic old source"));
        published.recv_timeout(Duration::from_secs(5)).unwrap(); eof.recv_timeout(Duration::from_secs(5)).unwrap();
        let old = h.snapshot()["generation"].clone(); let attempt = h.inner.0.lock().unwrap().start_attempt;
        h.stop("synthetic", "replace before old EOF").unwrap();
        dispatch.send(()).unwrap(); assert!(start.join().unwrap().is_err());
        peer(&f, READY); let next = h.start(&f.cfg, "synthetic successor").unwrap()["generation"].clone();
        assert_ne!(old, next); let events = h.lifecycle_events();
        settle_eof.send(()).unwrap();
        until(&h, |h| h.journal().iter().any(|f| f["class"] == "superseded-generation-eof"));
        assert_eq!(h.state(), "ready"); assert_eq!(h.lifecycle_events(), events);
        assert!(!h.inner.0.lock().unwrap().server_requests.is_closed(&next));
        let before = h.snapshot();
        for response in [Ok(json!({"result":{"userAgent":"codex/0.160.0"}})), Err("old error".into()), Ok(json!({"error":{"code":-1,"message":"old error"}}))] {
            assert!(h.finish_start_handshake(&old, attempt, json!({}), response, successor).is_err());
            assert_eq!(h.snapshot(), before);
        }
        h.stop("synthetic", "fixture complete").unwrap();
    }
}

#[test]
#[ignore = "Opt-in cached stock binary; fresh file-auth homes, macOS localhost-only OS sandbox, no model/login calls"]
fn startup_refusal_stock_config_control_and_first_start_restart_refusal() {
    use std::os::unix::fs::PermissionsExt;
    let binary = PathBuf::from(std::env::var_os("CHIRALITY_CODEX_BIN").expect("cached stock binary required"));
    assert_eq!(crate::util::sha256_hex(&std::fs::read(&binary).unwrap()), "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b");
    for restart in [false, true] {
        let mut f = fixture(false, READY);
        let temporary_home = |name: &str| {
            use std::os::unix::ffi::OsStringExt;
            let created = std::process::Command::new("mktemp").arg("-d").arg(f.root.join(format!("{name}-XXXXXX"))).output().unwrap();
            assert!(created.status.success());
            PathBuf::from(std::ffi::OsString::from_vec(created.stdout.strip_suffix(b"\n").unwrap().to_vec()))
        };
        f.cfg.codex_home = temporary_home("account");
        f.cfg.probe_home = temporary_home("probe");
        let sandbox = f.root.join("network.sb");
        std::fs::write(&sandbox, "(version 1)\n(allow default)\n(deny network*)\n(allow network-outbound (remote ip \"localhost:*\"))\n(allow network-inbound (local ip \"localhost:*\"))\n").unwrap();
        let quote = |p: &Path| format!("'{}'", p.to_str().unwrap().replace('\'', "'\\''"));
        std::fs::write(&f.cfg.codex_bin, format!("#!/bin/sh\nexec /usr/bin/sandbox-exec -f {} {} \"$@\"\n", quote(&sandbox), quote(&binary))).unwrap();
        std::fs::set_permissions(&f.cfg.codex_bin, std::fs::Permissions::from_mode(0o700)).unwrap();
        let config = |policy: &str| format!("cli_auth_credentials_store=\"file\"\nmodel_provider=\"openai\"\nmodel=\"gpt-6.1-sol\"\napproval_policy=\"{policy}\"\nsandbox_mode=\"workspace-write\"\n[features]\nplugins=false\n[analytics]\nenabled=false\n");
        std::fs::write(f.cfg.probe_home.join("config.toml"), config("on-request")).unwrap();
        let h = Arc::new(Host::new());
        if restart {
            std::fs::write(f.cfg.codex_home.join("config.toml"), config("on-request")).unwrap();
            assert_eq!(h.start(&f.cfg, "stock credential-free control").unwrap()["state"], "ready");
            h.stop("synthetic", "stock restart fixture").unwrap();
        }
        std::fs::write(f.cfg.codex_home.join("config.toml"), config("untrusted")).unwrap();
        let source = h.clone();
        *h.before_eof_gate.lock().unwrap() = Some(Box::new(move || until(&source, |h| h.inner.0.lock().unwrap().stderr_bytes > 0)));
        let start = Instant::now(); assert!(h.start(&f.cfg, "stock unsupported-config fixture").is_err());
        until(&h, |h| h.state() == "halted-after-repeated-failure");
        assert!(start.elapsed() < Duration::from_secs(5));
        let events = failures(&h); assert_eq!(events.len(), 1);
        assert_eq!(events[0]["exitFacts"]["exitCode"], 1);
        assert!(events[0]["exitFacts"]["diagnosticOutputBytes"].as_u64().unwrap() > 0);
        assert_eq!(events[0]["generation"]["spawnCounter"], if restart { 2 } else { 1 });
        assert!(!f.cfg.codex_home.join("auth.json").exists());
        assert!(!f.cfg.probe_home.join("auth.json").exists());
    }
}
