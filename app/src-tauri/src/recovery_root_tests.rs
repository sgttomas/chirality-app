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
        let root = std::env::temp_dir().join(opaque_id("recovery-root-").unwrap());
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
#[test]
fn recovery_root_actual_source_queue_durable_reopen_remains_pointer_only() {
    let f = Fixture::new(true);
    let writer = f.host.recovery_writer.lock().unwrap();
    f.item("turn-A");
    f.item("turn-B");
    let bytes = std::fs::read(f.root.join("ledger.jsonl")).unwrap();
    let view = f.read();
    assert_eq!(std::fs::read(f.root.join("ledger.jsonl")).unwrap(), bytes);
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
    let bytes = std::fs::read(f.root.join("ledger.jsonl")).unwrap();
    let reopened =
        crate::read_recovery_custody_from_root(&router, HomeClass::Account.as_str(), &Value::Null)
            .unwrap();
    assert_eq!(std::fs::read(f.root.join("ledger.jsonl")).unwrap(), bytes);
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
    assert!(!String::from_utf8(bytes).unwrap().contains("NATIVE_PAYLOAD"));
}
#[test]
fn recovery_root_missing_project_index_stays_memory_only_and_read_never_flushes() {
    let f = Fixture::new(false);
    f.item("known-source-turn");
    Host::close_generation(&mut f.host.inner.0.lock().unwrap());
    f.host.flush_recovery_observations();
    let bytes = std::fs::read(f.root.join("ledger.jsonl")).unwrap();
    let view = f.read();
    assert_eq!(std::fs::read(f.root.join("ledger.jsonl")).unwrap(), bytes);
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
    let before = std::fs::read(f.root.join("ledger.jsonl")).unwrap();
    let view = f.read();
    assert_eq!(view["source"]["generation"], f.generation);
    assert_eq!(std::fs::read(f.root.join("ledger.jsonl")).unwrap(), before);
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
    let mut row = ledger.snapshot()["entries"]
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
    let prefix = std::fs::read(f.root.join("ledger.jsonl")).unwrap();
    let next = Arc::new(Host::new());
    next.configure_recovery(f.root.join("ledger.jsonl"))
        .unwrap();
    let next_session = next.shared_recovery_observation()["appSession"].clone();
    // Actual legacy metadata row append retains original execution generation.
    let mut new_ledger = RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();
    row["session"] = next_session.clone();
    row["tags"] = json!([{"owner":"synthetic-receiver","value":"later-metadata","seq":1}]);
    new_ledger.append(row).unwrap();
    next.inner.0.lock().unwrap().recovery_snapshot = Some(new_ledger.snapshot());
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
    assert!(std::fs::read(f.root.join("ledger.jsonl"))
        .unwrap()
        .starts_with(&prefix));
}
