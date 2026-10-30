//! Bounded label IO over actual retained process-group custody.
use super::process_group_custody::OwnedProcess;
use serde_json::{json, Value};
use std::io::Read;
use std::os::fd::AsRawFd;
use std::os::unix::process::ExitStatusExt;
use std::sync::Arc;
use std::time::{Duration, Instant};

/// Cleanup never reconstructs authority from a PID. Unknown custody stays
/// retained by the owner and its retirement observer; detached groups are not
/// covered by the original-group census.
pub(crate) fn settle(process: &Arc<OwnedProcess>, grace: Duration) -> Result<Value, String> {
    let deadline = Instant::now() + grace;
    while !process.release_if_empty().empty() && Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(5));
    }
    let (forced, error) = process.force_if_needed();
    let deadline = Instant::now() + Duration::from_secs(1);
    let mut census = process.release_if_empty();
    while !census.empty() && Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(5));
        census = process.release_if_empty();
    }
    let exit = process.observe_exit();
    process.maintain();
    match (exit, census.empty(), error) {
        (Ok(Some(status)), true, None) => Ok(json!({
            "exitFacts":{"exitCode":status.code(),"signal":status.signal(),"forcedAfterGrace":forced},
            "descendants":census.report()})),
        (exit, _, error) => Err(format!("owned process settlement unavailable: exit={exit:?}; descendants={}; signal={error:?}", census.report())),
    }
}

pub(crate) fn read_label(
    process: &Arc<OwnedProcess>, wait: Duration, admitted: impl Fn() -> Result<(), String>,
) -> Result<String, String> {
    let result = (|| {
        let mut out = process.take_stdout().ok_or("label probe stdout unavailable")?;
        let mut err = process.take_stderr().ok_or("label probe stderr unavailable")?;
        for fd in [out.as_raw_fd(), err.as_raw_fd()] {
            if unsafe { libc::fcntl(fd, libc::F_SETFL, libc::O_NONBLOCK) } < 0 {
                return Err("cannot bound label probe pipes".into());
            }
        }
        let deadline = Instant::now() + wait.min(Duration::from_secs(20));
        let mut bytes = Vec::new();
        let mut count = 0usize;
        loop {
            admitted()?;
            if Instant::now() >= deadline { return Err("label probe timed out".into()); }
            for (pipe, retain) in [(&mut out as &mut dyn Read, true), (&mut err as &mut dyn Read, false)] {
                let mut chunk = [0u8; 4096];
                for _ in 0..17 {
                    match pipe.read(&mut chunk) {
                        Ok(0) => break,
                        Ok(n) => {
                            count += n;
                            if count > 65536 { return Err("label probe output limit exceeded".into()); }
                            if retain { bytes.extend_from_slice(&chunk[..n]); }
                        }
                        Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => break,
                        Err(e) => return Err(format!("label probe read failed: {e}")),
                    }
                }
            }
            if let Some(status) = process.observe_exit()? {
                if !status.success() { return Err(format!("label probe unsuccessful: {status}")); }
                for (pipe, retain) in [(&mut out as &mut dyn Read, true), (&mut err as &mut dyn Read, false)] {
                    let mut tail = [0u8; 65537];
                    match pipe.read(&mut tail) {
                        Ok(n) => { count += n; if retain { bytes.extend_from_slice(&tail[..n]); } }
                        Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => (),
                        Err(e) => return Err(e.to_string()),
                    }
                }
                if count > 65536 { return Err("label probe output limit exceeded".into()); }
                admitted()?;
                return String::from_utf8(bytes).map_err(|_| "non UTF-8 label probe output".into());
            }
            std::thread::sleep(Duration::from_millis(5));
        }
    })();
    let cleanup = settle(process, Duration::ZERO);
    match (result, cleanup) {
        (result, Ok(_)) => result,
        (result, Err(error)) => Err(format!("label probe cleanup failed: {error}; probe result: {}", result.err().unwrap_or_else(|| "label observed but not admitted".into()))),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use super::super::{Host, HostConfig, process_group_custody::Census};
    use std::path::PathBuf;
    use std::os::unix::fs::PermissionsExt;

    struct Fixture { root: PathBuf, cfg: HostConfig }
    impl Fixture {
        fn new(body: &str) -> Self {
            let root = std::env::temp_dir().canonicalize().unwrap()
                .join(crate::util::opaque_id("legacy-probe-").unwrap());
            for name in ["account", "probe"] { std::fs::create_dir_all(root.join(name)).unwrap(); }
            let bin = root.join("supplier-fixture");
            std::fs::write(&bin, format!(r#"#!/usr/bin/env python3
import os,sys,time,json
if '--version' in sys.argv:
 assert os.environ['CODEX_HOME'].endswith('/probe')
 assert os.getcwd()==os.environ['CODEX_HOME']
 assert not any(name in os.environ for name in ['OPENAI_API_KEY','CODEX_API_KEY','CODEX_ACCESS_TOKEN'])
 {body}
 print('codex-cli 0.160.0'); sys.exit(0)
for line in sys.stdin:
 f=json.loads(line)
 if 'id' in f: print(json.dumps({{'id':f['id'],'result':{{'userAgent':'codex/0.160.0'}}}}),flush=True)
"#)).unwrap();
            std::fs::set_permissions(&bin, std::fs::Permissions::from_mode(0o700)).unwrap();
            let mut cfg = HostConfig::new(bin, root.join("account"), root.join("probe"), root.clone());
            cfg.allow_unverified_dev = true;
            cfg.wait_limit = Duration::from_secs(2);
            Self { root, cfg }
        }
        fn entered(&self) {
            let deadline = Instant::now() + Duration::from_secs(2);
            while !self.root.join("probe/entered").exists() && Instant::now() < deadline {
                std::thread::sleep(Duration::from_millis(5));
            }
            assert!(self.root.join("probe/entered").exists());
        }
    }
    impl Drop for Fixture { fn drop(&mut self) { let _ = std::fs::remove_dir_all(&self.root); } }
    const HANG: &str = "open('entered','w').close(); time.sleep(5)";

    #[test]
    fn legacy_probe_hang_and_both_noisy_pipes_are_bounded_without_generation() {
        for (body, expected) in [("time.sleep(5)", "timed out"),
            ("sys.stdout.write('x'*100000); sys.stdout.flush()", "output limit"),
            ("sys.stderr.write('x'*100000); sys.stderr.flush()", "output limit")] {
            let mut f = Fixture::new(body);
            f.cfg.wait_limit = Duration::from_millis(500);
            let host = Arc::new(Host::new());
            let start = Instant::now();
            let error = host.start(&f.cfg, "fixture").unwrap_err();
            assert!(error.contains(expected), "expected {expected}: {error}");
            assert!(start.elapsed() < Duration::from_secs(3));
            assert!(host.snapshot()["generation"].is_null());
            assert!(host.probe_processes.lock().unwrap().is_empty());
        }
    }

    #[test]
    fn legacy_probe_stop_cancels_actual_attempt_without_stale_publication() {
        let f = Fixture::new(HANG);
        let host = Arc::new(Host::new());
        let h = host.clone(); let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        f.entered();
        let process = host.probe_processes.lock().unwrap()[0].1.clone();
        host.stop("fixture", "cancel pending probe").unwrap();
        let before = host.snapshot();
        assert!(worker.join().unwrap().is_err());
        assert_eq!(host.snapshot(), before);
        assert!(process.released());
        let good = Fixture::new("pass");
        let ready = host.start(&good.cfg, "fixture").unwrap();
        assert_eq!(ready["state"], "ready");
        assert_eq!(ready["supplierStanding"], "unverified-development");
        host.stop("fixture", "done").unwrap();
    }

    #[test]
    fn quit_fence_cancels_probe_and_blocks_new_starts_until_reopened() {
        let f = Fixture::new(HANG);
        let host = Arc::new(Host::new());
        let h = host.clone(); let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        f.entered();
        host.begin_quit();
        host.settle_for_quit("fixture", "quit").unwrap();
        assert!(worker.join().unwrap().is_err());
        assert!(host.start(&f.cfg, "fixture").unwrap_err().contains("quit"));
        host.cancel_quit();
        let good = Fixture::new("pass");
        host.start(&good.cfg, "fixture").unwrap();
        host.begin_quit();
        let settlement = host.settle_for_quit("fixture", "quit").unwrap();
        assert_eq!(settlement["ownedProcesses"][0]["settlement"]["descendants"]["surviving"], 0);
    }

    #[test]
    fn unknown_probe_cleanup_retains_custody_and_quit_can_retry() {
        let f = Fixture::new(HANG);
        let host = Arc::new(Host::new());
        let h = host.clone(); let cfg = f.cfg.clone();
        let worker = std::thread::spawn(move || h.start(&cfg, "fixture"));
        f.entered();
        let process = host.probe_processes.lock().unwrap()[0].1.clone();
        *process.census_override.lock().unwrap() = Some(Census::Unknown("fixture census unavailable".into()));
        let stopped = host.stop("fixture", "cancel pending probe");
        let started = worker.join().unwrap();
        assert!(stopped.unwrap_err().contains("settlement unavailable"));
        assert!(started.is_err());
        assert!(!process.released());
        assert_eq!(host.probe_processes.lock().unwrap().len(), 1);
        assert!(host.start(&f.cfg, "fixture").unwrap_err().contains("prior label probe settlement"));
        host.begin_quit();
        assert!(host.settle_for_quit("fixture", "quit").is_err());
        *process.census_override.lock().unwrap() = None;
        host.settle_for_quit("fixture", "quit retry").unwrap();
        assert!(process.released());
    }

    #[test]
    fn stopped_state_without_actual_source_custody_cannot_authorize_quit() {
        let host = Host::new();
        {
            let mut inner = host.inner.0.lock().unwrap();
            inner.state = "stopped".into();
            inner.generation = json!({"appSession":"fixture","home":"fixture","spawnCounter":1});
        }
        host.begin_quit();
        assert!(host.settle_for_quit("fixture", "quit").unwrap_err().contains("no actual retained process"));
    }
}
