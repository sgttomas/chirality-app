//! Parent-only ignored connected stock witness, compiled ONLY into an immutable
//! copied candidate context. No maintained product dependency or proof factory.
use super::*;
use std::{
    path::PathBuf,
    sync::{
        atomic::{AtomicBool, Ordering},
        Arc,
    },
    time::{Duration, Instant},
};
const MODEL: &str = "gpt-6.1-sol";
const PROVIDER: &str = "parent_loopback_400";
struct Guard {
    root: PathBuf,
    host: Arc<crate::hosting::Host>,
    done: Arc<AtomicBool>,
    worker: Option<std::thread::JoinHandle<()>>,
}
impl Drop for Guard {
    fn drop(&mut self) {
        self.done.store(true, Ordering::Release);
        let before = self.host.snapshot();
        let stopped = self
            .host
            .stop("Parent witness cleanup", "bounded fixture finished");
        if let Some(worker) = self.worker.take() {
            let _ = worker.join();
        }
        let report = json!({"beforeCleanup":before,"stopResult":format!("{:?}",stopped),"afterCleanup":self.host.snapshot(),"panicking":std::thread::panicking()});
        let _ = std::fs::write(
            self.root.join("host-final-snapshot.json"),
            serde_json::to_vec_pretty(&report).unwrap(),
        );
    }
}
fn history_receive(
    home: &HomeSession,
    query: crate::native_history::HistoryQuery,
) -> Result<(), String> {
    let dispatch = home.host.history_dispatch(&query)?;
    home.history.lock().unwrap().dispatched(dispatch.clone());
    home.host.history_wait(&dispatch, Duration::from_secs(20))?;
    home.history.lock().unwrap().reconcile(&home.host);
    Ok(())
}
#[test]
#[ignore = "Parent-only real stock execution; never run from ordinary child Cargo checks"]
fn parent_only_stock_workflow_roundtrip() {
    assert_eq!(
        std::env::var("CHIRALITY_PARENT_WORKFLOW_WITNESS").as_deref(),
        Ok("reviewed-parent-only"),
        "explicit Parent execution flag required"
    );
    let root =
        PathBuf::from(std::env::var_os("CHIRALITY_WITNESS_ROOT").expect("Parent mktemp root"));
    assert_eq!(root.canonicalize().unwrap(), root);
    assert!(root.is_absolute());
    let binary = PathBuf::from(
        std::env::var_os("CHIRALITY_WITNESS_BINARY").expect("Parent complete supplier binary"),
    );
    let expected = std::env::var("CHIRALITY_WITNESS_BINARY_SHA256")
        .expect("Parent authoritative main checksum");
    let home_path = root.join("codex-home");
    let probe = root.join("probe-home");
    let workspace = root.join("workspace");
    let package = root
        .join("holding")
        .join(crate::workflow_workspace::development_catalog::NAME);
    let library = root.join("library");
    for p in [&home_path, &probe, &workspace, &package, &library] {
        assert!(
            p.is_dir(),
            "Parent must supply only owned fresh physical inputs"
        );
        assert_eq!(p.canonicalize().unwrap(), *p);
    }
    assert!(!home_path.join("auth.json").exists());
    assert!(!probe.join("auth.json").exists());
    let invocation: serde_json::Value =
        serde_json::from_slice(&std::fs::read(root.join("launch-binding.json")).unwrap()).unwrap();
    assert_eq!(invocation["developmentStart"]["transition"], "LT-24");
    assert_eq!(
        invocation["developmentStart"]["supplierStanding"],
        "unverified-development"
    );
    assert_eq!(
        invocation["developmentStart"]["qualifiedDistribution"],
        false
    );
    let mut cfg = crate::hosting::HostConfig::new(binary, home_path, probe, workspace.clone());
    cfg.allow_unverified_dev = invocation["developmentStart"]["allowUnverifiedDev"]
        .as_bool()
        .expect("explicit Parent LT-24 choice required");
    assert!(
        cfg.allow_unverified_dev,
        "Parent must explicitly select LT-24 for this development witness"
    );
    cfg.expected_sha256 = Some(expected);
    cfg.wait_limit = Duration::from_secs(20);
    cfg.session_flags = vec![
        "analytics.enabled=false".into(),
        "features.plugins=false".into(),
        "model_reasoning_effort=\"medium\"".into(),
    ];
    let host = Arc::new(crate::hosting::Host::new());
    let done = Arc::new(AtomicBool::new(false));
    let aborted = Arc::new(AtomicBool::new(false));
    let observed = host.clone();
    let stop = done.clone();
    let failure = aborted.clone();
    let snapshot_path = root.join("host-latest-snapshot.json");
    let worker = std::thread::spawn(move || {
        while !stop.load(Ordering::Acquire) {
            let snapshot = observed.snapshot();
            let temp = snapshot_path.with_extension("tmp");
            if std::fs::write(&temp, serde_json::to_vec_pretty(&snapshot).unwrap()).is_ok() {
                let _ = std::fs::rename(&temp, &snapshot_path);
            }
            let unexpected = snapshot["serverRequests"]
                .as_array()
                .is_some_and(|r| !r.is_empty())
                || snapshot["journal"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .any(|e| {
                        e["frame"]["method"] == "item/started"
                            && e["frame"]["params"]["item"]["type"]
                                .as_str()
                                .is_some_and(|t| {
                                    !matches!(
                                        t,
                                        "userMessage" | "agentMessage" | "reasoning" | "plan"
                                    )
                                })
                    });
            if unexpected {
                failure.store(true, Ordering::Release);
                let _ = observed.stop(
                    "Parent witness abort",
                    "unexpected request/tool; no human grant",
                );
                break;
            }
            std::thread::sleep(Duration::from_millis(10));
        }
    });
    let _guard = Guard {
        root: root.clone(),
        host: host.clone(),
        done,
        worker: Some(worker),
    };
    let ready = host
        .start(
            &cfg,
            "Parent explicit LT-24 unverified-development stock witness",
        )
        .unwrap();
    assert_eq!(ready["supplierStanding"], "unverified-development");
    assert_eq!(ready["verification"]["result"], "unverifiable");
    assert!(ready["lifecycle"]
        .as_array()
        .unwrap()
        .iter()
        .any(|event| event["transitionId"] == "LT-24"
            && event["event"] == "development-start-authorized"));
    let generation = host.snapshot()["generation"].clone();
    let guidance_root = root.join("instructions");
    seed_instructions(&guidance_root).unwrap();
    let composition = compose_role(
        &guidance_root,
        Some(crate::role_supply::Role::WORKING_ITEMS),
    )
    .unwrap();
    composition.verify().unwrap();
    let response = host
        .thread_start_with_guidance(
            workspace.to_str().unwrap(),
            MODEL,
            PROVIDER,
            &composition.text,
        )
        .unwrap();
    let thread = response["result"]["thread"]["id"]
        .as_str()
        .expect("actual native thread")
        .to_owned();
    let home = Arc::new(
        HomeSession::new(
            crate::home_resources::HomeClass::Account,
            host.clone(),
            Ok(cfg),
        )
        .unwrap(),
    );
    let mut workflow = WorkflowRootSession::default();
    workflow.select_development_copy(package).unwrap();
    workflow
        .open_library(
            library,
            "project",
            None,
            Arc::new(std::sync::Mutex::new(None)),
        )
        .unwrap(); // Context only; no A15/capture.
    let reference=workflow.prepare_run(home.clone(),&generation,&thread,"Parent owned HTTP400 fixture. Do not invoke tools or request permission. No real model prediction occurs.".into()).unwrap();
    let run = workflow.runs[&reference].clone();
    let mut run = run.lock().unwrap();
    run.send().unwrap();
    assert!(run.source.is_some());
    assert_eq!(run.status["adoption"], "unknown");
    let turn = run
        .turn_id
        .clone()
        .expect("genuine native turn identity even if failed");
    let deadline = Instant::now() + Duration::from_secs(40);
    loop {
        assert!(
            !aborted.load(Ordering::Acquire),
            "unexpected request/tool aborted source"
        );
        let snapshot = host.snapshot();
        let terminal = snapshot["conversationTurns"]
            .as_array()
            .into_iter()
            .flatten()
            .find(|t| {
                t["generation"] == generation && t["threadId"] == thread && t["turnId"] == turn
            })
            .and_then(|t| t["nativeTurn"]["status"].as_str())
            .map(str::to_owned);
        if terminal.as_deref() == Some("failed") {
            break;
        }
        assert!(
            Instant::now() < deadline,
            "bounded native failed-turn observation missing"
        );
        std::thread::sleep(Duration::from_millis(20));
    }
    // Native list/turn material comes only from actual dispatch/Host receipts;
    // no JSON injection into NativeHistory and no synthetic page constructor.
    let mut cursor = None;
    let mut seen = std::collections::HashSet::new();
    loop {
        let query = {
            let mut receiver = home.history.lock().unwrap();
            receiver.reconcile(&host);
            receiver
                .history_mut()
                .unwrap()
                .list_threads(cursor.as_deref(), crate::native_history::Direction::Asc)
                .unwrap()
        };
        history_receive(&home, query).unwrap();
        if home
            .history
            .lock()
            .unwrap()
            .history_mut()
            .unwrap()
            .select(&thread)
            .is_ok()
        {
            break;
        }
        let snapshot = home.history.lock().unwrap().history().unwrap().snapshot();
        let next = snapshot["listPage"]["nextCursor"]
            .as_str()
            .map(str::to_owned)
            .expect("original thread absent; no guessed ID admission");
        assert!(seen.insert(next.clone()), "list cursor loop");
        cursor = Some(next);
    }
    let query = home
        .history
        .lock()
        .unwrap()
        .history_mut()
        .unwrap()
        .turns_page(None, crate::native_history::Direction::Asc)
        .unwrap();
    history_receive(&home, query).unwrap();
    let supply = run.check_native_supply().unwrap();
    assert_eq!(supply["adoption"], "unknown");
    assert!(matches!(supply["comparison"]["state"].as_str(),Some("equal_claimed_text"|"text_differs_workflow_bytes_equal")),"actual current native userMessage must retain exact selected workflow bytes; native text packaging may differ");
    assert!(supply["pageCount"].as_u64().is_some_and(|n| n >= 1));
    assert!(!aborted.load(Ordering::Acquire));
    let report = json!({"invocation":invocation,"standing":"native failed-turn source comparison; cause unknown pending Parent observation correlation","supplierStanding":ready["supplierStanding"],"verification":ready["verification"],"sourceGeneration":generation,"thread":thread,"turn":turn,"selection":workflow.snapshot()["selection"],"preparedRecord":run.prepared.record(),"source":run.source.as_ref().unwrap().evidence(),"nativeFailedTurn":host.snapshot()["conversationTurns"],"supply":supply,"adoption":"unknown","runStanding":"no active/completed workflow execution inferred","nativeA15":"not performed","sourceQualification":"main checksum/complete package provenance separate from model/supplier qualification","roleComposition":composition.carried});
    std::fs::write(
        root.join("witness-result.json"),
        serde_json::to_vec_pretty(&report).unwrap(),
    )
    .unwrap();
}
