//! Offline hosting contract checks; supplier double performs no network operation.
mod common;
use chirality_app_v4_lib::hosting::{Host, HostConfig};
use common::ScratchDirectory;
use serde_json::json;
use std::os::unix::fs::PermissionsExt;
use std::sync::Arc;

fn config(root: &ScratchDirectory) -> HostConfig {
    let bin = root.join("codex-double");
    std::fs::write(&bin, r#"#!/usr/bin/env python3
import sys,json
if '--version' in sys.argv:
 print('codex-cli 0.160.0'); sys.exit(0)
for line in sys.stdin:
 f=json.loads(line)
 if 'id' not in f: continue
 if f['method']=='initialize':
  print(json.dumps({'method':'test/early','params':{'native':True},'emittedAtMs':1}),flush=True)
  result={'userAgent':'codex/0.160.0'}
 else: result={'thread':{'id':'same-thread-id','status':{'type':'idle'}},'model':'configured-model','modelProvider':'configured-provider'}
 print(json.dumps({'id':f['id'],'result':result}),flush=True)
"#).unwrap();
    std::fs::set_permissions(&bin, std::fs::Permissions::from_mode(0o700)).unwrap();
    let mut cfg = HostConfig::new(bin, root.join("home"), root.join("probe"), root.to_path_buf());
    std::fs::create_dir_all(&cfg.codex_home).unwrap();
    std::fs::create_dir_all(&cfg.probe_home).unwrap();
    cfg.allow_unverified_dev = true;
    cfg
}

#[test]
fn matching_binary_is_only_development_and_mismatch_cannot_be_bypassed() {
    let root = ScratchDirectory::new("hostcontract");
    let mut cfg = config(&root);
    cfg.expected_sha256 = Some(chirality_app_v4_lib::util::sha256_hex(&std::fs::read(&cfg.codex_bin).unwrap()));
    let host = Arc::new(Host::new());
    let ready = host.start(&cfg, "test").unwrap();
    assert_eq!(ready["verification"]["result"], "unverifiable");
    assert_eq!(ready["supplierStanding"], "unverified-development");
    assert!(host.lifecycle_events().iter().any(|e| e["transitionId"] == "LT-24"));
    assert!(!host.lifecycle_events().iter().any(|e| e["transitionId"] == "LT-04"));
    host.stop("test", "done").unwrap();
    assert_eq!(host.lifecycle_events().last().unwrap()["supplierStanding"], "unverified-development");
    cfg.expected_sha256 = Some("0".repeat(64));
    assert!(host.start(&cfg, "test").is_err());
    assert_eq!(host.state(), "refused");
    assert_eq!(host.snapshot()["verification"]["result"], "mismatch");
}

#[test]
fn identity_separates_instances_homes_and_spawns_and_frames_stay_native() {
    let root = ScratchDirectory::new("hostidentity");
    let cfg = config(&root);
    let first = Arc::new(Host::new());
    let second = Arc::new(Host::new());
    assert!(first.snapshot()["generation"].is_null());
    let g1 = first.start(&cfg, "test").unwrap()["generation"].clone();
    let g2 = second.start(&cfg, "test").unwrap()["generation"].clone();
    assert_ne!(g1["appSession"], g2["appSession"]);
    assert_eq!(g1["home"], g2["home"]);
    assert_eq!(g1["spawnCounter"], g2["spawnCounter"]);
    assert!(first.thread_start(".").is_err());
    assert!(first.thread_start_selected(".", "", "configured-provider").is_err());
    first.thread_start_selected(".", "configured-model", "configured-provider").unwrap();
    let snapshot = first.snapshot();
    assert_eq!(snapshot["threads"][0]["generation"], g1);
    assert_eq!(snapshot["threads"][0]["reportedDestination"]["scope"], "thread");
    assert_eq!(snapshot["networkDisclosure"]["entries"][1]["purpose"], "model");
    assert_eq!(snapshot["networkDisclosure"]["observationSourceVersion"], "0.158.0");
    assert_eq!(snapshot["networkDisclosure"]["currentSupplierVersion"], "0.160.0");
    let positions: Vec<u64> = first.journal().iter().filter_map(|e| e["position"].as_u64()).collect();
    assert!(positions.windows(2).all(|w| w[0] < w[1]));
    let early = first.journal().into_iter().find(|e| e["frame"]["method"]=="test/early").unwrap();
    assert_eq!(early["generation"], g1);
    assert_eq!(early["frame"], json!({"method":"test/early","params":{"native":true},"emittedAtMs":1}));
    assert!(first.client_requests().iter().all(|r| r["generation"] == g1));
    first.stop("test", "done").unwrap();
    second.stop("test", "done").unwrap();
    let mut other_home = cfg.clone();
    other_home.codex_home = root.join("other-home");
    std::fs::create_dir(&other_home.codex_home).unwrap();
    let g3 = first.start(&other_home, "test").unwrap()["generation"].clone();
    assert_eq!(g1["appSession"], g3["appSession"]);
    assert_ne!(g1["home"], g3["home"]);
    assert_eq!(g3["spawnCounter"], 2);
    first.stop("test", "done").unwrap();
}

#[test]
fn unqualified_start_requires_explicit_development_option() {
    let root = ScratchDirectory::new("hostrefusal");
    let mut cfg = config(&root);
    cfg.allow_unverified_dev = false;
    let host = Arc::new(Host::new());
    assert!(host.start(&cfg, "test").is_err());
    assert!(host.child_pid().is_none());
    assert_eq!(host.snapshot()["generation"], serde_json::Value::Null);
}

#[test]
fn version_label_and_handshake_mismatches_refuse_readiness() {
    let root = ScratchDirectory::new("hostversion");
    let cfg = config(&root);
    let original = std::fs::read_to_string(&cfg.codex_bin).unwrap();
    std::fs::write(&cfg.codex_bin, original.replace("codex-cli 0.160.0", "codex-cli 0.159.0")).unwrap();
    let host = Arc::new(Host::new());
    assert!(host.start(&cfg, "test").is_err());
    assert_eq!(host.state(), "refused");
    assert!(host.child_pid().is_none());
    std::fs::write(&cfg.codex_bin, original.replace("codex/0.160.0", "codex/0.159.0")).unwrap();
    assert!(host.start(&cfg, "test").is_err());
    assert_ne!(host.state(), "ready");
    assert_eq!(host.snapshot()["versionIdentity"]["handshakeReportedIdentity"], json!({"userAgent":"codex/0.159.0"}));
    assert_eq!(host.snapshot()["versionIdentity"]["handshakeConsistency"], "contradicts-declared-pin");
    assert!(!host.lifecycle_events().iter().any(|e| e["transitionId"] == "LT-09"));
    let failed_generation = host.snapshot()["generation"].clone();
    let failed_frames: Vec<_> = host.journal().into_iter().filter(|e| e.get("frame").is_some()).collect();
    assert_eq!(failed_frames.len(), 2);
    assert_eq!(failed_frames[0]["frame"], json!({"method":"test/early","params":{"native":true},"emittedAtMs":1}));
    assert_eq!(failed_frames[1]["frame"], json!({"id":1,"result":{"userAgent":"codex/0.159.0"}}));
    assert_eq!(failed_frames[0]["position"], 1);
    assert_eq!(failed_frames[1]["position"], 2);
    assert!(failed_frames.iter().all(|e| e["generation"] == failed_generation && e["generationNeverReady"] == true));
    host.stop("test", "prepare next explicit start").unwrap();
    std::fs::write(&cfg.codex_bin, &original).unwrap();
    let next = host.start(&cfg, "test").unwrap();
    assert_ne!(next["generation"], failed_generation);
    let retained: Vec<_> = host.journal().into_iter().filter(|e| e["generation"] == failed_generation && e.get("frame").is_some()).collect();
    assert_eq!(retained, failed_frames);
    host.stop("test", "done").unwrap();
}

#[test]
fn observed_label_mismatch_stays_mismatch_when_probe_removes_binary() {
    let root = ScratchDirectory::new("hostreadfailure");
    let cfg = config(&root);
    std::fs::write(&cfg.codex_bin, r#"#!/usr/bin/env python3
import os,sys
os.unlink(sys.argv[0])
print('codex-cli 0.159.0')
"#).unwrap();
    let host = Arc::new(Host::new());
    assert!(host.start(&cfg, "test").is_err());
    assert!(!cfg.codex_bin.exists());
    assert_eq!(host.snapshot()["verification"]["result"], "mismatch");
    assert_eq!(host.snapshot()["verification"]["element"], "observed version label");
    assert_eq!(host.state(), "refused");
    assert!(host.child_pid().is_none());
}
