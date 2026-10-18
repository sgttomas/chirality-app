//! Source-connected synthetic Root consumer checks. No supplier/native process.
use super::*;
use crate::{
    home_resources::HomeClass,
    runtime_session::{HomeRouter, HomeSession},
};
struct Fixture {
    root: PathBuf,
    host: Arc<Host>,
    home: Arc<HomeSession>,
    router: Mutex<HomeRouter>,
    generation: Value,
}
impl Fixture {
    fn new(index: bool) -> Self {
        let root = std::env::temp_dir().canonicalize().unwrap().join(opaque_id("recovery-root-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let host = Arc::new(Host::new());
        host.configure_recovery(root.join("ledger.jsonl")).unwrap();
        let generation = {
            let mut i = host.inner.0.lock().unwrap();
            let g = json!({"appSession":i.app_session,"home":"synthetic-original-home","spawnCounter":1});
            i.generation = g.clone();
            i.home = "synthetic-original-home".into();
            i.spawn_counter = 1;
            i.state = "ready".into();
            i.threads
                .push(json!({"generation":g,"threadId":"same-thread"}));
            g
        };
        if index {
            host.observe_conversation_project(
                &generation,
                "same-thread",
                Some("H-acct"),
                &crate::recovery::ExplicitAppProjectContext::known(
                    "original-project",
                    crate::recovery::AppProjectSource::ConfiguredDirectory,
                )
                .unwrap(),
            )
            .unwrap();
        }
        let home = Arc::new(
            HomeSession::new(
                HomeClass::Account,
                host.clone(),
                Err("offline synthetic host".into()),
            )
            .unwrap(),
        );
        let router = Mutex::new(HomeRouter::new(home.clone()).unwrap());
        Self {
            root,
            host,
            home,
            router,
            generation,
        }
    }
    fn item(&self, turn: &str) {
        self.host.on_line(&serde_json::to_vec(&json!({"method":"item/started","params":{"threadId":"same-thread","turnId":turn,"item":{"id":"same-item","type":"reasoning","text":"NATIVE_PAYLOAD_NOT_IN_LEDGER"}}})).unwrap(),&self.generation);
    }
    fn read(&self) -> Value {
        crate::read_recovery_custody_from_root(
            &self.router,
            HomeClass::Account.as_str(),
            &self.generation,
        )
        .unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

fn cold_request_summary_case(context: Option<&str>) {
    use crate::native_requests::RequestRegister;
    let root = std::env::temp_dir().canonicalize().unwrap().join(opaque_id("cold-request-summary-").unwrap());
    std::fs::create_dir(&root).unwrap();
    let path = root.join("ledger.jsonl");
    let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
    ledger.start_session("old-request-session", "synthetic-candidate").unwrap();
    let generation = json!({"appSession":"old-request-session","home":"original-request-home","spawnCounter":1});
    let mut register = RequestRegister::default();
    register.receive(&generation, 1, &json!({"id":"old-question","method":"item/tool/requestUserInput","params":{"threadId":"old-thread","turnId":"old-turn","itemId":"old-item","questions":[]}}), &json!({})).unwrap();
    ledger.request_summary(&register.entries()[0]).unwrap();
    if let Some(context) = context {
        register.close_for(&generation, context);
        ledger.request_summary(&register.entries()[0]).unwrap();
        ledger.append(RecoveryLedger::session_end_entry("old-request-session", "quit", &[]).unwrap()).unwrap();
    }
    drop(ledger);
    let host = Arc::new(Host::new());
    host.configure_recovery(path.clone()).unwrap();
    let original = crate::recovery::stored_entries(&path).into_iter().rev().find(|row| row["kind"] == "register_entry_summary").unwrap();
    assert_eq!(original["transition"], if context.is_some() { "RQ-04" } else { "RQ-06" });
    let home = Arc::new(HomeSession::new(HomeClass::Account, host.clone(), Err("synthetic metadata-only source".into())).unwrap());
    let router = Mutex::new(HomeRouter::new(home).unwrap());
    let before = crate::recovery::stored_entries(&path);
    let view = crate::read_recovery_request_history_from_root(&router, HomeClass::Account.as_str(), &Value::Null, None).unwrap();
    assert_eq!(crate::recovery::stored_entries(&path), before, "the historical read must not append, flush or reconstruct requests");
    assert_eq!(host.snapshot()["serverRequests"], json!([]));
    assert_eq!(host.snapshot()["clientRequests"], json!([]));
    assert_eq!(view["page"]["entries"].as_array().unwrap().len(), 1, "a persisted {} request ending must remain readable after cold reopen", original["transition"]);
    assert_eq!(view["page"]["entries"][0]["summary"], original);
    assert_eq!(view["page"]["entries"][0]["sourceGeneration"], generation);
    assert_eq!(view["page"]["entries"][0]["requestIdentityType"], "string");
    assert_eq!(view["page"]["oldRequestsAnswerable"], false);
    println!("REQUEST_HISTORY_DTO {}", json!({"scenario":context.unwrap_or("app-ended-without-record"),"view":view}));
    drop(router); drop(host);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn recovery_root_cold_recorded_request_endings_remain_readable() {
    for context in ["app-quit", "supplier-stop"] { cold_request_summary_case(Some(context)); }
}

#[test]
fn recovery_root_cold_unclean_request_ending_control_remains_readable() {
    cold_request_summary_case(None);
}

#[test]
fn recovery_root_cold_request_history_rejects_foreign_busy_and_changed_sources_without_io_under_inner() {
    let f = Fixture::new(false);
    let read = || crate::read_recovery_request_history_from_root(&f.router, HomeClass::Account.as_str(), &f.generation, None);
    assert!(crate::read_recovery_request_history_from_root(&f.router, HomeClass::ApiKey.as_str(), &f.generation, None).is_err());
    assert!(crate::read_recovery_request_history_from_root(&f.router, HomeClass::Account.as_str(), &Value::Null, None).is_err());
    let ledger = f.host.inner.0.lock().unwrap().recovery.clone().unwrap();
    let held = ledger.lock().unwrap();
    let started = std::time::Instant::now();
    assert!(read().unwrap_err().contains("busy"));
    assert!(started.elapsed() < std::time::Duration::from_secs(1));
    assert_eq!(f.read()["source"]["generation"], f.generation, "the original cached custody reader remains independent from the ledger lock");
    drop(held);
    let source = f.host.clone();
    crate::recovery::store::AFTER_TERMINAL_READ.with(|slot| *slot.borrow_mut()=Some(Box::new(move || {
        let mut inner = source.inner.0.try_lock().expect("no Host Inner guard spans actual SQLite read");
        inner.generation["spawnCounter"] = json!(2);
    })));
    assert!(read().unwrap_err().contains("changed"));
    assert_eq!(f.host.snapshot()["clientRequests"], json!([]));
    assert_eq!(f.host.snapshot()["serverRequests"], json!([]));
}
#[test]
fn recovery_root_actual_source_queue_durable_reopen_remains_pointer_only() {
    let f = Fixture::new(true);
    let writer = f.host.recovery_writer.lock().unwrap();
    f.item("turn-A");
    f.item("turn-B");
    let bytes = crate::recovery::stored_entries(&f.root.join("ledger.jsonl"));
    let view = f.read();
    assert_eq!(crate::recovery::stored_entries(&f.root.join("ledger.jsonl")), bytes);
    assert_eq!(view["source"]["generation"], f.generation);
    assert!(view["custody"]["pendingPointerFacts"].as_u64().unwrap() > 0);
    assert_eq!(
        view["custody"]["historicalConversations"][0]["index"]["lastObservedExecution"]["state"],
        "indexed"
    );
    assert_eq!(
        view["custody"]["live"]["observations"][0]["openItems"]
            .as_array()
            .unwrap()
            .len(),
        2
    );
    assert!(view["custody"]["live"]["observations"][0]["liveTurn"].is_null());
    drop(writer);
    f.host.flush_recovery_observations();
    let view = f.read();
    assert_eq!(view["custody"]["pendingPointerFacts"], 0);
    let associations = view["custody"]["historicalConversations"][0]["openItemAssociations"]
        .as_array()
        .unwrap();
    assert_eq!(associations.len(), 2);
    assert_eq!(associations[0]["turnId"], "turn-A");
    assert_eq!(associations[1]["turnId"], "turn-B");
    assert_eq!(associations[0]["generation"], f.generation);
    Host::close_generation(&mut f.host.inner.0.lock().unwrap());
    f.host.flush_recovery_observations();
    let next = Arc::new(Host::new());
    next.configure_recovery(f.root.join("ledger.jsonl"))
        .unwrap();
    let home = Arc::new(
        HomeSession::new(HomeClass::Account, next.clone(), Err("no supplier".into())).unwrap(),
    );
    let router = Mutex::new(HomeRouter::new(home).unwrap());
    let bytes = crate::recovery::stored_entries(&f.root.join("ledger.jsonl"));
    let reopened =
        crate::read_recovery_custody_from_root(&router, HomeClass::Account.as_str(), &Value::Null)
            .unwrap();
    assert_eq!(crate::recovery::stored_entries(&f.root.join("ledger.jsonl")), bytes);
    assert_eq!(reopened["source"]["generation"], Value::Null);
    assert_eq!(
        reopened["custody"]["historicalConversations"][0]["executionGeneration"],
        f.generation
    );
    assert_eq!(
        reopened["custody"]["historicalConversations"][0]["openItemAssociations"],
        json!(associations)
    );
    assert_eq!(reopened["custody"]["restartEvents"], json!([]));
    assert_eq!(reopened["custody"]["automaticResume"], false);
    assert_eq!(next.snapshot()["clientRequests"], json!([]));
    assert!(!serde_json::to_string(&bytes).unwrap().contains("NATIVE_PAYLOAD"));
    assert!(!String::from_utf8_lossy(&crate::recovery::stored_bytes(&f.root.join("ledger.jsonl"))).contains("NATIVE_PAYLOAD"));
}
#[test]
fn recovery_root_missing_project_index_stays_memory_only_and_read_never_flushes() {
    let f = Fixture::new(false);
    f.item("known-source-turn");
    Host::close_generation(&mut f.host.inner.0.lock().unwrap());
    f.host.flush_recovery_observations();
    let bytes = crate::recovery::stored_entries(&f.root.join("ledger.jsonl"));
    let view = f.read();
    assert_eq!(crate::recovery::stored_entries(&f.root.join("ledger.jsonl")), bytes);
    assert_eq!(
        view["custody"]["live"]["observations"][0]["indexKnown"],
        false
    );
    assert!(!view["custody"]["live"]["limits"]
        .as_array()
        .unwrap()
        .is_empty());
    assert_eq!(view["custody"]["historicalConversations"], json!([]));
    assert_eq!(view["custody"]["restartEvents"], json!([]));
}
#[test]
fn recovery_root_foreign_home_generation_and_busy_root_cannot_retarget() {
    let f = Fixture::new(true);
    let other = Fixture::new(true);
    f.item("original-turn");
    other.item("foreign-turn");
    assert!(crate::read_recovery_custody_from_root(
        &f.router,
        HomeClass::ApiKey.as_str(),
        &f.generation
    )
    .is_err());
    assert!(crate::read_recovery_custody_from_root(
        &f.router,
        HomeClass::Account.as_str(),
        &other.generation
    )
    .is_err());
    let mut later = f.generation.clone();
    later["spawnCounter"] = json!(2);
    assert!(
        crate::read_recovery_custody_from_root(&f.router, HomeClass::Account.as_str(), &later)
            .is_err()
    );
    let guard = f.router.lock().unwrap();
    assert!(crate::read_recovery_custody_from_root(
        &f.router,
        HomeClass::Account.as_str(),
        &f.generation
    )
    .is_err());
    drop(guard);
    assert_eq!(
        f.read()["custody"]["historicalConversations"][0]["openItemAssociations"][0]["turnId"],
        "original-turn"
    );
    // The consumer does not acquire the writer, history, runtime or ledger locks.
    let writer = f.host.recovery_writer.lock().unwrap();
    let history = f.home.history.lock().unwrap();
    let runtime = f.home.runtime.lock().unwrap();
    let ledger = f.host.inner.0.lock().unwrap().recovery.clone().unwrap();
    let ledger_guard = ledger.lock().unwrap();
    let before = crate::recovery::stored_entries(&f.root.join("ledger.jsonl"));
    let view = f.read();
    assert_eq!(view["source"]["generation"], f.generation);
    assert_eq!(crate::recovery::stored_entries(&f.root.join("ledger.jsonl")), before);
    drop(ledger_guard);
    drop(runtime);
    drop(history);
    drop(writer);
}
#[test]
fn recovery_root_reopen_preserves_legacy_unknown_and_distinct_metadata_source() {
    let f = Fixture::new(true);
    f.item("known-turn");
    let mut ledger = RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();
    let mut row = ledger.recorded_entries()
        .as_array()
        .unwrap()
        .iter()
        .rev()
        .find(|r| r["kind"] == "conversation_index")
        .unwrap()
        .clone();
    row["lastObservedExecution"]["openItems"]
        .as_array_mut()
        .unwrap()
        .push(json!({"itemId":"legacy-item","itemType":"reasoning"}));
    row["lastObservedExecution"]["liveTurn"] = json!("not-a-legacy-association");
    ledger.append(row.clone()).unwrap();
    let prefix = crate::recovery::stored_entries(&f.root.join("ledger.jsonl"));
    let next = Arc::new(Host::new());
    next.configure_recovery(f.root.join("ledger.jsonl"))
        .unwrap();
    let next_session = next.shared_recovery_observation()["appSession"].clone();
    // Actual legacy metadata row append retains original execution generation.
    let mut new_ledger = RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();
    row["session"] = next_session.clone();
    row["tags"] = json!([{"owner":"synthetic-receiver","value":"later-metadata","seq":1}]);
    new_ledger.append(row).unwrap();
    next.inner.0.lock().unwrap().recovery_snapshot = Some(new_ledger.observation());
    let home = HomeSession::new(HomeClass::Account, next.clone(), Err("offline".into())).unwrap();
    let view =
        crate::recovery_root_view::read(&home, HomeClass::Account.as_str(), &Value::Null).unwrap();
    let historical = &view["custody"]["historicalConversations"][0];
    assert_eq!(historical["executionGeneration"], f.generation);
    assert_eq!(historical["metadataIndex"]["session"], next_session);
    let items = historical["openItemAssociations"].as_array().unwrap();
    let old = items.iter().find(|i| i["itemId"] == "legacy-item").unwrap();
    assert!(old["turnId"].is_null());
    assert!(old["fullTuple"].is_null());
    assert!(old["correlation"].as_str().unwrap().contains("unknown"));
    assert!(crate::recovery::stored_entries(&f.root.join("ledger.jsonl"))
        .starts_with(&prefix));
}
