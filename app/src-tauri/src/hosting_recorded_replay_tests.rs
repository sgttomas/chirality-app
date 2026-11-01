//! Recorded supplier traffic through the actual App process/stdio/recovery seam.
//! The peer is unverified development equipment, not stock Codex or an examined
//! App candidate. Original redacted recordings and EXP records remain unchanged.
use super::*;
use crate::recovery::{AppProjectSource, ExplicitAppProjectContext};
use crate::runtime_session::HomeSession;
use std::os::unix::fs::PermissionsExt;
use std::time::Instant;

const RECORDINGS: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../../execution/PKG-01/DEL-01-01/Work/prototype/st5/recordings"
);
const PEER: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../supplier_checks/recorded_replay.py"
);

// Replay fixtures are independent App processes. Give each test thread its own
// records-store identity rather than racing the process-wide default store's
// initial publication. Retention checks remain enabled on the real Host path.
struct OwnStore(PathBuf);
impl OwnStore {
    fn new() -> Self {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(opaque_id("recorded-seam-store-").unwrap());
        std::fs::create_dir_all(&root).unwrap();
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
            root: root.clone(),
            placement: crate::records_store::Placement::Test,
            limits: vec![],
        })));
        Self(root)
    }
}
impl Drop for OwnStore {
    fn drop(&mut self) {
        crate::records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

struct Fixture {
    root: PathBuf,
    cfg: HostConfig,
    home: Arc<HomeSession>,
    recording: Value,
    generation: Value,
    _store: OwnStore,
}

impl Fixture {
    fn new(scenario: &str, indexed: bool) -> Self {
        let store = OwnStore::new();
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(opaque_id("recorded-seam-").unwrap());
        for name in ["account", "probe"] {
            std::fs::create_dir_all(root.join(name)).unwrap();
        }
        let path = PathBuf::from(RECORDINGS).join(format!("{scenario}.recording.json"));
        let bytes = std::fs::read(&path).unwrap();
        let recording: Value = serde_json::from_slice(&bytes).unwrap();
        let digest = crate::util::sha256_hex(&bytes);
        std::fs::write(root.join("generation"), "1").unwrap();
        // Only our scratch wrapper is executed. The recorded command text is
        // supplier data; no shell, model, account or original path is invoked.
        let wrapper = format!(
            r#"#!/usr/bin/env python3
import pathlib,runpy,sys
root=pathlib.Path({root})
generation=(root/'generation').read_text().strip()
profile='app' if generation=='1' else 'app-recovery'
if generation=='2' and (root/'profile').exists():
 profile=(root/'profile').read_text().strip()
args=[{peer},'--recording',{recording},'--sha256',{digest},'--generation',generation,'--audit',str(root/('audit-'+generation+'.jsonl')),'--profile',profile]
if {pause} and generation=='1':
 args += ['--pause-after-frame','28','--release',str(root/'release')]
if profile=='app-continue':
 args += ['--pause-after-frame','32','--release',str(root/'release')]
sys.argv=args+['--']+sys.argv[1:]
runpy.run_path({peer},run_name='__main__')
"#,
            root = json!(root.to_str().unwrap()),
            peer = json!(PEER),
            recording = json!(path.to_str().unwrap()),
            digest = json!(digest),
            pause = if scenario == "nv04" { "True" } else { "False" }
        );
        let executable = root.join("recorded-peer");
        std::fs::write(&executable, wrapper).unwrap();
        std::fs::set_permissions(&executable, std::fs::Permissions::from_mode(0o700)).unwrap();
        let mut cfg = HostConfig::new(
            executable,
            root.join("account"),
            root.join("probe"),
            root.clone(),
        );
        cfg.allow_unverified_dev = true;
        cfg.wait_limit = Duration::from_secs(3);
        let host = Arc::new(Host::new());
        host.configure_recovery(root.join("recovery.ledger.jsonl"))
            .unwrap();
        let ready = host.start(&cfg, "recorded replay test").unwrap();
        assert_eq!(ready["supplierStanding"], "unverified-development");
        assert_eq!(ready["verification"]["result"], "unverifiable");
        let generation = ready["generation"].clone();
        let home = Arc::new(
            HomeSession::new(
                crate::home_resources::HomeClass::Account,
                host,
                Ok(cfg.clone()),
            )
            .unwrap(),
        );
        let fixture = Self {
            root,
            cfg,
            home,
            recording,
            generation,
            _store: store,
        };
        let result = &fixture.recording["frames"][5]["frame"]["result"];
        fixture
            .home
            .host
            .thread_start_selected(
                "<WORKSPACE>",
                result["model"].as_str().unwrap(),
                result["modelProvider"].as_str().unwrap(),
            )
            .unwrap();
        if indexed {
            fixture
                .home
                .host
                .observe_conversation_project(
                    &fixture.generation,
                    fixture.thread(),
                    Some("H-acct"),
                    &ExplicitAppProjectContext::known(
                        "P-recorded-replay",
                        AppProjectSource::ConfiguredDirectory,
                    )
                    .unwrap(),
                )
                .unwrap();
        }
        crate::host_tick::receive_view(&fixture.home);
        fixture
            .home
            .host
            .turn_start_text(&fixture.generation, fixture.thread(), fixture.text())
            .unwrap();
        fixture
    }

    fn thread(&self) -> &str {
        self.recording["frames"][7]["frame"]["params"]["threadId"]
            .as_str()
            .unwrap()
    }
    fn text(&self) -> &str {
        self.recording["frames"][7]["frame"]["params"]["input"][0]["text"]
            .as_str()
            .unwrap()
    }
    fn until(&self, description: &str, predicate: impl Fn() -> bool) {
        let deadline = Instant::now() + Duration::from_secs(5);
        while !predicate() {
            assert!(
                Instant::now() < deadline,
                "{description}: state={} audit={}",
                self.home.host.state(),
                std::fs::read_to_string(self.root.join(
                    if self.root.join("audit-2.jsonl").exists() {
                        "audit-2.jsonl"
                    } else {
                        "audit-1.jsonl"
                    }
                ))
                .unwrap_or_default()
            );
            std::thread::sleep(Duration::from_millis(5));
        }
    }
    fn ledger(&self) -> Vec<Value> {
        // Independently reopen the persisted fixture ledger, but exclude this
        // Host's concurrent writer while inspecting SQLite's transient journal.
        // Keep the product's physical single-link guard and disk-read assertion.
        let ledger = self.home.host.inner.0.lock().unwrap().recovery.clone().unwrap();
        let _writer = ledger.lock().unwrap();
        crate::recovery::stored_entries(&self.root.join("recovery.ledger.jsonl"))
    }
    fn audit(&self, stage: u64) -> Vec<Value> {
        std::fs::read_to_string(self.root.join(format!("audit-{stage}.jsonl")))
            .unwrap()
            .split_inclusive('\n')
            .filter(|line| line.ends_with('\n'))
            .map(|line| serde_json::from_str(line).unwrap())
            .collect()
    }
    fn assert_recorded_frames(&self, generation: &Value, stage: u64) {
        let audit = self.audit(stage);
        assert!(
            audit
                .iter()
                .any(|e| e["event"] == "finish" && e["remaining_frame_indices"] == json!([])),
            "{audit:?}"
        );
        assert!(!audit.iter().any(|e| e["event"] == "error"), "{audit:?}");
        let expected = audit
            .iter()
            .filter(|e| matches!(e["event"].as_str(), Some("frame" | "constructed-frame")) && e["direction"] == "codex->app")
            .map(|e| {
                if e["event"]=="constructed-frame" {
                    assert_eq!(e["recipe"],"thread-list-envelope-from-thread-read");
                    assert_eq!(e["source_frame_index"],25);
                    assert!(e.get("frame_index").is_none(),"constructed catalog has no recorded frame index");
                    return json!({"id":e["actual_rpc_id"],"result":{"data":[self.recording["frames"][25]["frame"]["result"]["thread"]],"nextCursor":null}});
                }
                let mut frame = self.recording["frames"]
                    [e["frame_index"].as_u64().unwrap() as usize]["frame"]
                    .clone();
                if e["kind"] == "reply" {
                    frame["id"] = e["actual_rpc_id"].clone();
                }
                frame
            })
            .collect::<Vec<_>>();
        let actual = self
            .home
            .host
            .journal()
            .into_iter()
            .filter(|e| e["generation"] == *generation)
            .filter_map(|e| e.get("frame").cloned())
            .collect::<Vec<_>>();
        assert_eq!(actual, expected, "every delivered supplier payload must equal its recorded value except correlated reply ID");
    }
    fn lose_acknowledgment(&self) -> SourceRequest {
        self.until("recorded approval received", || {
            self.home.host.snapshot()["serverRequests"]
                .as_array()
                .unwrap()
                .iter()
                .any(|r| r["requestIdentity"] == 0)
        });
        assert!(
            self.home
                .host
                .answer_server_request(
                    &self.generation,
                    &json!("0"),
                    &json!({"decision":"accept"}),
                    "person-via-interaction",
                    Some("person:invented replay actor (identity not verified)")
                )
                .is_err(),
            "typed server request identities stay distinct"
        );
        let written = self
            .home
            .host
            .answer_server_request(
                &self.generation,
                &json!(0),
                &json!({"decision":"accept"}),
                "person-via-interaction",
                Some("person:invented replay actor (identity not verified)"),
            )
            .unwrap();
        assert_eq!(
            written,
            json!({"replyWriteResult":"written","acknowledgment":"not-observed"})
        );
        // Gate the replay's real EOF on this actual unanswered write, rather
        // than a timing race with answer settlement or a synthetic state edit.
        let source = self
            .home
            .host
            .request_begin_scoped(
                "thread/turns/list",
                self.recording["frames"][18]["frame"]["params"].clone(),
                json!({"kind":"person-directed"}),
                false,
                Some(&self.generation),
            )
            .unwrap();
        self.until("recorded process loss", || {
            self.home.host.state() == "exited-unexpectedly"
        });
        // EOF publication and the queued durable write are separate. Wait for
        // the actual ledger fact rather than treating the lifecycle label as
        // evidence that its append has already finished.
        self.until("lost acknowledgment persisted", || {
            self.home.host.flush_recovery_observations();
            self.ledger()
                .iter()
                .any(|entry| entry["transition"] == "RQ-05")
        });
        source
    }
    fn restart(&self) -> Value {
        self.home
            .host
            .stop_scoped(&self.generation, "recorded replay test", "Restart Codex")
            .unwrap();
        std::fs::write(self.root.join("generation"), "2").unwrap();
        self.home
            .host
            .start(&self.cfg, "recorded replay test restart")
            .unwrap()["generation"]
            .clone()
    }
    fn relaunch(&mut self) -> Value {
        self.home
            .host
            .stop("recorded replay old App cleanup", "done")
            .unwrap();
        std::fs::write(self.root.join("generation"), "2").unwrap();
        let host = Arc::new(Host::new());
        host.configure_recovery(self.root.join("recovery.ledger.jsonl"))
            .unwrap();
        let generation = host
            .start(&self.cfg, "recorded replay new App session")
            .unwrap()["generation"]
            .clone();
        self.home = Arc::new(
            HomeSession::new(
                crate::home_resources::HomeClass::Account,
                host,
                Ok(self.cfg.clone()),
            )
            .unwrap(),
        );
        generation
    }

    fn prepare_continue(&self) -> (Value, HistoryDispatch) {
        std::fs::write(self.root.join("profile"), "app-continue").unwrap();
        let generation = self.restart();
        assert_eq!(crate::host_tick::recovery_tick_home(&self.home), 2);
        self.home
            .host
            .request(
                "thread/loaded/list",
                json!({}),
                json!({"kind":"person-directed"}),
            )
            .unwrap();
        {
            let mut history = self.home.history.lock().unwrap();
            assert!(
                history
                    .select(&self.home.host.snapshot(), &generation, 0, self.thread())
                    .is_err(),
                "loaded IDs and recovered turns do not supply a selectable history catalog"
            );
        }
        let catalog = self.history_action(&generation, 0, "list");
        let result = self
            .home
            .host
            .history_wait(&catalog, Duration::from_secs(2))
            .unwrap();
        assert_eq!(result["response"]["result"],json!({"data":[self.recording["frames"][25]["frame"]["result"]["thread"]],"nextCursor":null}),"catalog envelope/membership is constructed; its thread metadata is unchanged recorded data");
        {
            let mut history = self.home.history.lock().unwrap();
            history.reconcile(&self.home.host);
            history
                .select(&self.home.host.snapshot(), &generation, 0, self.thread())
                .unwrap();
        }
        assert!(
            !self
                .home
                .host
                .client_requests()
                .iter()
                .any(|r| r["generation"] == generation && r["method"] == "thread/resume"),
            "recovery, catalog and selection cannot resume"
        );
        assert!(!self.home.host.snapshot()["threads"]
            .as_array()
            .unwrap()
            .iter()
            .any(|t| t["generation"] == generation));
        let resume = self.history_action(&generation, 1, "continue");
        assert_eq!(
            resume.source().attempted_frame()["params"],
            json!({"threadId":self.thread(),"excludeTurns":true})
        );
        self.until("recorded idle before resume reply", || {
            self.audit(2)
                .iter()
                .any(|e| e["event"] == "paused" && e["frame_index"] == 32)
        });
        self.home.history.lock().unwrap().reconcile(&self.home.host);
        assert!(
            !self.home.host.snapshot()["threads"]
                .as_array()
                .unwrap()
                .iter()
                .any(|t| t["generation"] == generation),
            "an idle notification is not a successful Continue receipt"
        );
        (generation, resume)
    }

    fn history_action(&self, generation: &Value, epoch: u64, action: &str) -> HistoryDispatch {
        let query = {
            let mut history = self.home.history.lock().unwrap();
            history.reconcile(&self.home.host);
            history
                .prepare(
                    &self.home.host.snapshot(),
                    generation,
                    epoch,
                    action,
                    None,
                    crate::native_history::Direction::Desc,
                    None,
                )
                .unwrap()
        };
        let receipt = self.home.host.history_dispatch(&query).unwrap();
        self.home
            .history
            .lock()
            .unwrap()
            .dispatched(receipt.clone());
        receipt
    }
}

impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = self.home.host.stop("recorded replay cleanup", "done");
        if let Err(error) = std::fs::remove_dir_all(&self.root) {
            assert!(std::thread::panicking(), "replay scratch cleanup: {error}");
        }
    }
}

#[test]
fn recorded_continue_admits_only_after_its_original_late_reply_and_keeps_unknown_role_standing() {
    let f = Fixture::new("st5", true);
    f.lose_acknowledgment();
    let (generation, resume) = f.prepare_continue();
    let waiting = f
        .home
        .host
        .history_wait(&resume, Duration::from_millis(20))
        .unwrap();
    assert_eq!(waiting["writeResult"], "written");
    assert_eq!(waiting["waitingEnded"], true);
    assert!(waiting["response"].is_null());
    f.home.history.lock().unwrap().reconcile(&f.home.host);
    assert!(!f.home.host.snapshot()["threads"]
        .as_array()
        .unwrap()
        .iter()
        .any(|t| t["generation"] == generation));
    std::fs::write(
        f.root.join("release"),
        "person still selected original Continue source",
    )
    .unwrap();
    f.until("late Continue admission", || {
        f.home.history.lock().unwrap().reconcile(&f.home.host);
        f.home.host.snapshot()["threads"]
            .as_array()
            .unwrap()
            .iter()
            .any(|t| t["generation"] == generation && t["nativeResumeObserved"] == true)
    });
    let history = f.home.history.lock().unwrap().snapshot(None);
    let admission = history["dispatches"]
        .as_array()
        .unwrap()
        .iter()
        .find(|d| d["requestRef"] == resume.source().request_ref())
        .unwrap()["activeAdmission"]
        .clone();
    assert_eq!(admission["resumeRequestRef"], resume.source().request_ref());
    assert_eq!(admission["threadId"], f.thread());
    assert_eq!(admission["nativeResumeObserved"], true);
    // This fixture supplied no original App role authority. Native resume
    // cannot create one from supplier metadata.
    assert_eq!(admission["appRole"]["standing"], "unknown");
    for _ in 0..3 {
        f.home.history.lock().unwrap().reconcile(&f.home.host);
    }
    let threads = f.home.host.snapshot()["threads"]
        .as_array()
        .unwrap()
        .clone();
    assert_eq!(
        threads
            .iter()
            .filter(|t| t["generation"] == generation)
            .count(),
        1
    );
    let sent = f
        .home
        .host
        .client_requests()
        .into_iter()
        .filter(|r| r["generation"] == generation)
        .map(|r| r["method"].as_str().unwrap().to_owned())
        .collect::<Vec<_>>();
    assert_eq!(
        sent,
        [
            "initialize",
            "thread/read",
            "thread/turns/list",
            "thread/loaded/list",
            "thread/list",
            "thread/resume"
        ]
    );
    assert_eq!(
        f.ledger()
            .iter()
            .filter(|r| r["transition"] == "RQ-05" && r["acknowledgment"] == "not-observed")
            .count(),
        1
    );
    f.home
        .host
        .stop("recorded Continue cleanup", "done")
        .unwrap();
    f.assert_recorded_frames(&generation, 2);
    let audit = f.audit(2);
    assert_eq!(
        audit
            .iter()
            .filter(|e| e["event"] == "constructed-frame")
            .count(),
        2
    );
    let binding = audit.iter().find(|e| e["event"] == "binding").unwrap();
    let adapted_resume = audit
        .iter()
        .find(|e| e["event"] == "frame" && e["frame_index"] == 30 && e["direction"] == "app->codex")
        .unwrap();
    assert_eq!(
        adapted_resume["adaptations"],
        json!(["thread/resume.excludeTurns:add-true-request-only;recorded-reply-unchanged"])
    );
    assert_eq!(binding["outside_segment_frame_indices"], json!([]));
}

#[test]
fn recorded_continue_reply_cannot_admit_after_the_selected_epoch_changes() {
    let f = Fixture::new("st5", true);
    f.lose_acknowledgment();
    let (generation, resume) = f.prepare_continue();
    f.home
        .history
        .lock()
        .unwrap()
        .select(&f.home.host.snapshot(), &generation, 1, f.thread())
        .unwrap();
    std::fs::write(
        f.root.join("release"),
        "selection changed while original reply pending",
    )
    .unwrap();
    let evidence = f
        .home
        .host
        .history_wait(&resume, Duration::from_secs(2))
        .unwrap();
    assert!(
        evidence["response"].get("result").is_some(),
        "native result still observed at original source"
    );
    f.home.history.lock().unwrap().reconcile(&f.home.host);
    assert!(!f.home.host.snapshot()["threads"]
        .as_array()
        .unwrap()
        .iter()
        .any(|t| t["generation"] == generation));
    let history = f.home.history.lock().unwrap().snapshot(None);
    assert_eq!(history["selectionEpoch"], 2);
    let receipt = history["dispatches"]
        .as_array()
        .unwrap()
        .iter()
        .find(|d| d["requestRef"] == resume.source().request_ref())
        .unwrap();
    assert!(receipt.get("activeAdmission").is_none());
    assert_eq!(
        f.home
            .host
            .client_requests()
            .iter()
            .filter(|r| r["generation"] == generation && r["method"] == "thread/resume")
            .count(),
        1
    );
    f.home
        .host
        .stop("recorded Continue cleanup", "done")
        .unwrap();
    f.assert_recorded_frames(&generation, 2);
}

#[test]
fn recorded_st5_preserves_unknown_ack_and_recovers_from_actual_history_reads() {
    let f = Fixture::new("st5", true);
    let unanswered = f.lose_acknowledgment();
    f.assert_recorded_frames(&f.generation, 1);
    let evidence = f.home.host.source_request_status(&unanswered).unwrap();
    assert_eq!(evidence["writeResult"], "written");
    assert_eq!(evidence["outcome"], "unknown-no-response");
    let live = f.home.host.recovery_custody().snapshot();
    assert_eq!(
        live["live"]["events"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|e| e["kind"] == "acknowledgment_not_observed")
            .count(),
        1,
        "{live}"
    );
    let lost = f
        .ledger()
        .into_iter()
        .filter(|e| e["transition"] == "RQ-05")
        .collect::<Vec<_>>();
    assert_eq!(
        lost.len(),
        1,
        "one durable lost acknowledgment, not success inferred from writing"
    );
    assert_eq!(lost[0]["replyWrite"], "written");
    assert_eq!(lost[0]["acknowledgment"], "not-observed");
    let second = f.restart();
    assert_ne!(second, f.generation);
    assert_eq!(
        crate::host_tick::recovery_tick_home(&f.home),
        2,
        "the actual automatic reader must consume metadata and turn history"
    );
    let view = crate::host_tick::receive_view(&f.home);
    let recorded_turn = &f.recording["frames"][27]["frame"]["result"]["data"][0];
    assert!(
        view["turns"]
            .as_array()
            .unwrap()
            .iter()
            .any(|t| t["id"] == recorded_turn["id"] && t["status"] == recorded_turn["status"]),
        "{view}"
    );
    let requests = f
        .home
        .host
        .client_requests()
        .into_iter()
        .filter(|r| r["generation"] == second)
        .collect::<Vec<_>>();
    assert_eq!(
        requests
            .iter()
            .map(|r| r["method"].as_str().unwrap())
            .collect::<Vec<_>>(),
        ["initialize", "thread/read", "thread/turns/list"]
    );
    assert!(
        requests[1..]
            .iter()
            .all(|r| r["initiator"] == json!({"kind":"app-rule","name":"recovery-read"})),
        "{requests:?}"
    );
    assert!(f
        .home
        .host
        .answer_server_request(
            &f.generation,
            &json!(0),
            &json!({"decision":"accept"}),
            "person-via-interaction",
            Some("person:invented replay actor (identity not verified)")
        )
        .is_err());
    let retained = f.home.host.snapshot()["serverRequests"]
        .as_array()
        .unwrap()
        .clone();
    assert_eq!(retained.len(), 1, "original request evidence is retained");
    assert!(
        retained
            .iter()
            .all(|r| r["generation"] == f.generation && r["closedGeneration"] == true),
        "no old answer becomes a successor request: {retained:?}"
    );
    assert_eq!(
        crate::host_tick::recovery_tick_home(&f.home),
        0,
        "no automatic resend, resume or duplicate pass"
    );
    assert_eq!(
        f.ledger()
            .iter()
            .filter(|r| r["transition"] == "RQ-05")
            .count(),
        1
    );
    f.home.host.stop("recorded replay test", "done").unwrap();
    f.assert_recorded_frames(&second, 2);
    let audit = f.audit(2);
    let binding = audit.iter().find(|e| e["event"] == "binding").unwrap();
    assert_eq!(
        binding["outside_segment_frame_indices"],
        json!([28, 29, 30, 31, 32, 33, 34]),
        "unplayed explicit-resume tail is disclosed"
    );
    assert!(
        audit
            .iter()
            .any(|e| e["kind"] == "reply" && e["recorded_rpc_id"] != e["actual_rpc_id"]),
        "actual Host RPC counter continues across generations"
    );
}

#[test]
fn recorded_st5_without_app_index_cannot_claim_an_automatic_recovery() {
    let f = Fixture::new("st5", false);
    f.lose_acknowledgment();
    let second = f.restart();
    assert_eq!(crate::host_tick::recovery_tick_home(&f.home), 0);
    assert_eq!(
        f.home
            .host
            .client_requests()
            .iter()
            .filter(|r| r["generation"] == second && r["method"] != "initialize")
            .count(),
        0
    );
}

#[test]
fn recorded_st5_new_app_session_uses_persisted_index_without_reviving_old_answer() {
    let mut f = Fixture::new("st5", true);
    f.lose_acknowledgment();
    f.assert_recorded_frames(&f.generation, 1);
    let lost = f
        .ledger()
        .into_iter()
        .find(|e| e["transition"] == "RQ-05")
        .unwrap();
    let next = f.relaunch();
    assert_ne!(next["appSession"], f.generation["appSession"]);
    assert_eq!(next["home"], f.generation["home"]);
    assert_eq!(
        f.home.host.snapshot()["recovery"]["oldRequestsAnswerable"],
        false
    );
    assert!(f.home.host.snapshot()["serverRequests"]
        .as_array()
        .unwrap()
        .is_empty());
    assert!(f
        .home
        .host
        .answer_server_request(
            &f.generation,
            &json!(0),
            &json!({"decision":"accept"}),
            "person-via-interaction",
            Some("person:invented replay actor (identity not verified)")
        )
        .is_err());
    assert_eq!(
        crate::host_tick::recovery_tick_home(&f.home),
        2,
        "cold recovery is driven by the persisted App index"
    );
    let view = crate::host_tick::receive_view(&f.home);
    let recorded_turn = &f.recording["frames"][27]["frame"]["result"]["data"][0];
    assert!(
        view["turns"]
            .as_array()
            .unwrap()
            .iter()
            .any(|t| t["id"] == recorded_turn["id"] && t["status"] == recorded_turn["status"]),
        "{view}"
    );
    let retained = f
        .ledger()
        .into_iter()
        .filter(|e| e["transition"] == "RQ-05")
        .collect::<Vec<_>>();
    assert_eq!(
        retained,
        vec![lost],
        "new App session must preserve the original lost-acknowledgment fact exactly"
    );
    let requests = f.home.host.client_requests();
    assert_eq!(
        requests
            .iter()
            .map(|r| r["method"].as_str().unwrap())
            .collect::<Vec<_>>(),
        ["initialize", "thread/read", "thread/turns/list"]
    );
    f.home
        .host
        .stop("recorded replay new App cleanup", "done")
        .unwrap();
    f.assert_recorded_frames(&next, 2);
}

#[test]
fn recorded_nv04_parent_completion_keeps_its_child_live_until_separate_completion() {
    let f = Fixture::new("nv04", true);
    let parent_turn = f.recording["frames"][28]["frame"]["params"]["turn"]["id"].clone();
    let child_thread = f.recording["frames"][21]["frame"]["params"]["threadId"].clone();
    let child_turn = f.recording["frames"][21]["frame"]["params"]["turn"]["id"].clone();
    f.until("parent completed before child", || {
        let view = crate::host_tick::receive_view(&f.home);
        view["turns"]
            .as_array()
            .unwrap()
            .iter()
            .any(|t| t["id"] == parent_turn && t["status"] == "completed")
    });
    let before = crate::host_tick::receive_view(&f.home);
    assert!(
        before["turns"]
            .as_array()
            .unwrap()
            .iter()
            .any(|t| t["id"] == child_turn && t["status"] == "inProgress"),
        "{before}"
    );
    assert!(before["turnRecords"]
        .as_array()
        .unwrap()
        .iter()
        .any(|t| t["turnId"] == child_turn && t["threadId"] == child_thread));
    assert!(before["descendants"]
        .as_array()
        .unwrap()
        .iter()
        .any(|d| d["threadId"] == child_thread
            && d["parentThreadId"] == f.thread()
            && d["observationEnded"] == false));
    std::fs::write(f.root.join("release"), "release recorded child frames").unwrap();
    f.until("child completed separately", || {
        let view = crate::host_tick::receive_view(&f.home);
        view["turns"]
            .as_array()
            .unwrap()
            .iter()
            .any(|t| t["id"] == child_turn && t["status"] == "completed")
    });
    f.home
        .host
        .request(
            "thread/loaded/list",
            json!({}),
            json!({"kind":"person-directed"}),
        )
        .unwrap();
    assert_eq!(
        f.home.host.state(),
        "ready",
        "peer exhaustion must not invent an unexpected supplier exit"
    );
    f.home.host.stop("recorded replay test", "done").unwrap();
    f.assert_recorded_frames(&f.generation, 1);
}
