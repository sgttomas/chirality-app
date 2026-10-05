//! Step 1: the main process hosts the stock Codex App Server and completes
//! `initialize` then `thread/start` (HOSTING_BOUNDARY.md §4.2, §5, §4.5).
//!
//! Needs CHIRALITY_CODEX_BIN (the stock 0.160.0 binary). Fails if it is not set,
//! unless CHIRALITY_SKIP_CODEX=1 is set explicitly. Uses a scratch CODEX_HOME made
//! with `mktemp -d` below `std::env::temp_dir()`; never a real Codex home; no sign-in;
//! no credential. The scratch home's config.toml stands in for the person's own
//! configuration: plugins off, analytics off, and a model provider on 127.0.0.1
//! port 9 where no server runs. This configures the model target; it does not
//! enforce network isolation. Actual sampled socket observations are described
//! in EVIDENCE.md, observation N-1. No model turn is started.

mod common;
use common::{evidence_output, ScratchDirectory};

use chirality_app_v4_lib::hosting::{Host, HostConfig};
use serde_json::{json, Value};
use std::process::Command;
use std::sync::Arc;
use std::time::{Duration, Instant};

const PERSON_CONFIG_STAND_IN: &str = r#"# Test stand-in for the person's Codex configuration (written by tests/handshake.rs).
model_provider = "skeleton_local"
model = "skeleton-no-model"

[model_providers.skeleton_local]
name = "skeleton local (no server running)"
base_url = "http://127.0.0.1:9/v1"
wire_api = "responses"

[features]
plugins = false

[analytics]
enabled = false
"#;

fn internet_sockets(pgid: i32) -> Vec<String> {
    let out = Command::new("lsof").args(["-n", "-P", "-a", "-i", "-g", &pgid.to_string()]).output();
    match out {
        Ok(o) => String::from_utf8_lossy(&o.stdout).lines().skip(1).map(|l| l.to_string()).collect(),
        Err(_) => vec!["lsof not available".into()],
    }
}

#[test]
fn hosts_codex_initialize_then_thread_start() {
    let Ok(bin) = std::env::var("CHIRALITY_CODEX_BIN") else {
        if std::env::var("CHIRALITY_SKIP_CODEX").as_deref() == Ok("1") {
            eprintln!("SKIPPED explicitly: CHIRALITY_SKIP_CODEX=1");
            return;
        }
        panic!("CHIRALITY_CODEX_BIN is not set (set CHIRALITY_SKIP_CODEX=1 to skip explicitly)");
    };
    let home = ScratchDirectory::new("cxh");
    let probe = ScratchDirectory::new("cxp");
    let cwd = ScratchDirectory::new("cxw");
    std::fs::write(home.join("config.toml"), PERSON_CONFIG_STAND_IN).unwrap();

    let mut cfg = HostConfig::new(bin.into(), home.to_path_buf(), probe.to_path_buf(), cwd.to_path_buf());
    cfg.expected_sha256 = std::env::var("CHIRALITY_CODEX_EXPECTED_SHA256").ok();
    cfg.allow_unverified_dev = true; // current full distribution qualification is absent

    let host = Arc::new(Host::new());
    // CR-03: a request before ready is refused and not sent.
    assert!(host.request("thread/start", json!({}), json!({"kind": "person-directed"})).is_err());

    let t0 = Instant::now();
    let ready = host.start(&cfg, "app-startup").expect("start reaches ready");
    assert_eq!(ready["state"], "ready");
    let generation = ready["generation"].clone();
    assert_eq!(generation["spawnCounter"], 1);
    assert!(generation["appSession"].as_str().unwrap().starts_with("app-session:"));
    assert_eq!(ready["supplierStanding"], "unverified-development");
    assert_eq!(ready["verification"]["result"], "unverifiable");
    let vi = &ready["versionIdentity"];
    assert_eq!(vi["observedVersionLabel"], "codex-cli 0.160.0");
    assert_eq!(vi["handshakeConsistency"], "consistent");
    assert_eq!(vi["handshakeReportedIdentity"]["codexHome"], json!(home.display().to_string()));
    assert_eq!(ready["declaredCapabilities"], json!({"experimentalApi": true, "requestAttestation": false, "explicitGatewayOauth": true}));

    // H4/H6: the notification that arrives with the initialize response was held,
    // then delivered with ready, unchanged, including emittedAtMs.
    let journal = host.journal();
    let rc = journal.iter().find(|e| e["frame"]["method"] == "remoteControl/status/changed")
        .expect("remoteControl/status/changed delivered");
    assert_eq!(rc["generation"], generation);
    assert!(rc["frame"].get("emittedAtMs").is_some());

    let r = host.thread_start_selected(&cwd.display().to_string(), "skeleton-no-model", "skeleton_local").expect("thread/start answered");
    assert_eq!(r["result"]["modelProvider"], "skeleton_local");
    assert_eq!(r["result"]["model"], "skeleton-no-model");
    assert_eq!(host.snapshot()["networkDisclosure"]["entries"][1]["phase"], "thread-start");
    let thread_id = r["result"]["thread"]["id"].as_str().unwrap().to_string();
    assert!(!thread_id.is_empty());
    let elapsed_ready_to_thread = t0.elapsed();

    // thread/started notification observed, same generation.
    let deadline = Instant::now() + Duration::from_secs(5);
    while !host.journal().iter().any(|e| e["frame"]["method"] == "thread/started") && Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(50));
    }
    assert!(host.journal().iter().any(|e| e["frame"]["method"] == "thread/started" && e["generation"] == generation));

    let pgid = host.child_pid().unwrap();
    let sockets = internet_sockets(pgid);
    assert!(sockets.is_empty(), "Codex opened internet sockets: {sockets:?}");

    let reqs = host.client_requests();
    let init = reqs.iter().find(|r| r["method"] == "initialize").unwrap();
    assert_eq!(init["outcome"], "response-observed-result");
    let ts = reqs.iter().find(|r| r["method"] == "thread/start" && r["generation"] == generation).unwrap();
    assert_eq!(ts["outcome"], "response-observed-result");
    assert_eq!(ts["initiator"]["kind"], "person-directed");

    // §4.5 deliberate stop: stop record, close input, the whole group ends.
    host.stop("the person", "test end").unwrap();
    assert_eq!(host.state(), "stopped");
    let lts: Vec<String> = host.lifecycle_events().iter().map(|e| e["transitionId"].as_str().unwrap().to_string()).collect();
    assert_eq!(lts, ["LT-01", "LT-24", "LT-06", "LT-09", "LT-17", "LT-23"]);
    let last = host.lifecycle_events().last().cloned().unwrap();
    assert_eq!(last["descendants"]["surviving"], 0);
    // After the stop: a request is refused, not sent.
    assert!(host.request("thread/start", json!({}), json!({"kind": "person-directed"})).is_err());

    // Records for the schema test (tests/validate-records.test.mjs).
    let out = evidence_output();
    std::fs::create_dir_all(&out).unwrap();
    let evidence = json!({
        "lifecycleEvents": host.lifecycle_events(),
        "clientRequests": host.client_requests(),
        "threadId": thread_id,
        "codexHome": home.display().to_string(),
        "elapsedStartToThreadMs": elapsed_ready_to_thread.as_millis() as u64,
        "internetSocketsAfterThreadStart": sockets,
        "modelTurnExercised": false,
    });
    std::fs::write(out.join("hosting-records.json"), serde_json::to_vec_pretty(&evidence).unwrap()).unwrap();
    let v: Value = evidence;
    eprintln!("lifecycle: {lts:?}; thread {}; start->thread {} ms", v["threadId"], v["elapsedStartToThreadMs"]);
}
