//! Actual Host/register inputs for the waiting-overview renderer regression.
use crate::{home_resources::HomeClass, hosting::{Host, HostConfig}, runtime_session::{HomeRouter, HomeSession}};
use serde_json::{json, Value};
use std::{path::PathBuf, sync::Arc, time::{Duration, Instant}};

struct Fixture { root: PathBuf, router: HomeRouter }
impl Fixture {
    fn new() -> Self {
        let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("waiting-overview-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let bin = root.join("peer.py");
        std::fs::write(&bin, r#"#!/usr/bin/python3
import json,sys
if '--version' in sys.argv:
 print('codex-cli 0.160.0');sys.exit(0)
def emit(x): print(json.dumps(x),flush=True)
for line in sys.stdin:
 f=json.loads(line);m=f.get('method')
 if m=='initialize': emit({'id':f['id'],'result':{'userAgent':'synthetic-waiting-overview'}})
 elif m=='thread/start': emit({'id':f['id'],'result':{'thread':{'id':'shared-thread','status':{'type':'idle'}},'model':'synthetic','modelProvider':'synthetic'}})
 elif m=='fixture/emit':
  for frame in f['params']['frames']: emit(frame)
  emit({'id':f['id'],'result':{}})
 elif m=='config/read': emit({'id':f['id'],'result':{'config':{},'origins':{}}})
"#).unwrap();
        use std::os::unix::fs::PermissionsExt;
        std::fs::set_permissions(&bin, std::fs::Permissions::from_mode(0o700)).unwrap();
        let account = Arc::new(Host::new());
        let key = Arc::new(Host::new_with_app_custody(account.app_runtime_custody().unwrap()).unwrap());
        let mut sessions = Vec::new();
        for (class, host) in [(HomeClass::Account, account), (HomeClass::ApiKey, key)] {
            let home = root.join(class.as_str()); let probe = root.join(format!("probe-{}", class.as_str()));
            std::fs::create_dir(&home).unwrap(); std::fs::create_dir(&probe).unwrap();
            let mut config = HostConfig::new(bin.clone(), home, probe, root.clone());
            config.allow_unverified_dev = true; config.wait_limit = Duration::from_secs(2);
            host.start(&config, "synthetic waiting-overview fixture").unwrap();
            host.thread_start_selected(root.to_str().unwrap(), "synthetic", "synthetic").unwrap();
            sessions.push(Arc::new(HomeSession::new(class, host, Ok(config)).unwrap()));
        }
        let mut router = HomeRouter::new(sessions.remove(0)).unwrap(); router.bind_key(sessions.remove(0)).unwrap();
        Self { root, router }
    }
    fn emit(&self, class: HomeClass, frames: Vec<Value>) {
        self.router.entry(class).unwrap().host.request("fixture/emit", json!({"frames":frames}), json!({"kind":"person-directed"})).unwrap();
    }
    fn status(&mut self, class: HomeClass) -> Value {
        self.router.activate(class).unwrap();
        // Use the same all-home metadata producer as host_status. Native request
        // content remains solely in this ordinary active-home snapshot.
        let mut status = self.router.active().host.snapshot();
        status["homeRouting"] = self.router.snapshot();
        status["waitingRequests"] = crate::waiting_requests::overview(&self.router);
        status
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        for home in self.router.entries() { let _ = home.host.stop("waiting fixture cleanup", "finished"); }
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn question(id: Value, thread: Option<&str>) -> Value {
    let mut params = json!({"turnId":"synthetic-turn","itemId":"synthetic-item","questions":[{"id":"q","header":"Synthetic question","question":"Private synthetic question content","isOther":false,"isSecret":false,"options":[{"label":"One","description":"Synthetic"}]}]});
    if let Some(thread) = thread { params["threadId"] = json!(thread); }
    json!({"id":id,"method":"item/tool/requestUserInput","params":params})
}
#[test]
fn actual_two_home_waiting_overview_dto() {
    let mut f = Fixture::new();
    f.emit(HomeClass::Account, vec![question(json!(7),Some("shared-thread")), question(json!("7"),Some("shared-thread")), question(json!("unattributed"),None)]);
    let mut key_question=question(json!(7),Some("shared-thread"));
    key_question["params"]["questions"][0]["question"]=json!("Private synthetic key question content");
    f.emit(HomeClass::ApiKey, vec![key_question]);
    let deadline = Instant::now() + Duration::from_secs(1);
    while f.router.entry(HomeClass::Account).unwrap().host.snapshot()["serverRequests"].as_array().unwrap().len() != 3 && Instant::now() < deadline { std::thread::sleep(Duration::from_millis(5)); }
    let account = f.status(HomeClass::Account); let key = f.status(HomeClass::ApiKey);
    assert_eq!(account["serverRequests"].as_array().unwrap().len(), 3);
    assert_eq!(key["serverRequests"].as_array().unwrap().len(), 1);
    assert!(f.router.entry(HomeClass::Account).unwrap().host.snapshot()["serverRequests"].as_array().unwrap().iter().all(|r|r["state"]=="outstanding"));
    let groups = account["waitingRequests"]["groups"].as_array().unwrap();
    assert_eq!(groups.len(), 3);
    assert_eq!(groups.iter().map(|g|g["count"].as_u64().unwrap()).sum::<u64>(),4,"number 7 and string 7 remain two real register entries, separate from the other home's number 7");
    assert!(!account["waitingRequests"].to_string().contains("Private synthetic"));
    assert!(!account["waitingRequests"].to_string().contains("requestIdentity"));
    let generation = account["generation"].clone();
    let open_account = crate::waiting_requests::open(&mut f.router,"account",&generation,&json!("shared-thread")).unwrap();
    assert_eq!(open_account["threadLoaded"],true);
    let open_unnamed = crate::waiting_requests::open(&mut f.router,"account",&generation,&Value::Null).unwrap();
    assert_eq!(open_unnamed["threadLoaded"],false);
    let open_key=crate::waiting_requests::open(&mut f.router,"api-key",&key["generation"],&json!("shared-thread")).unwrap();
    let mut native = crate::native_waiting::Registry::default();
    let entries = native.project(&account["waitingRequests"]);
    assert!(!serde_json::to_string(&entries).unwrap().contains("Private synthetic"));
    let mut intents = serde_json::Map::new();
    for entry in &entries {
        let before = f.router.active().class();
        native.select(&entry.id, &f.router).unwrap();
        native.checkpoint("mounted-App-fixture", 0).unwrap();
        let claim = native.claim("mounted-App-fixture", &f.router);
        assert_eq!(f.router.active().class(), before, "selection and claim never activate a home before renderer admission");
        let name = if claim["target"]["threadId"].is_null() { "unnamed" } else { claim["target"]["modeHomeClass"].as_str().unwrap() };
        intents.insert(name.to_owned(), claim.clone());
        native.finish("mounted-App-fixture", claim["intentId"].as_str().unwrap()).unwrap();
    }
    println!("WAITING_REQUESTS_DTO:{}", json!({"account":account,"api-key":key,"navigation":{"account":open_account,"api-key":open_key,"unnamed":open_unnamed},"native":{"entries":entries,"intents":intents}}));
}

#[test]
fn only_current_person_waiting_groups_are_counted_and_opened() {
    let mut f = Fixture::new();
    f.emit(HomeClass::Account,vec![question(json!("live"),Some("unloaded-thread")),question(json!("settled"),Some("settled-thread")),
        json!({"method":"serverRequest/resolved","params":{"threadId":"settled-thread","requestId":"settled"}}),
        json!({"id":"named","method":"currentTime/read","params":{}}),json!({"id":"unsupported","method":"synthetic/unsupported","params":{}})]);
    let status = f.status(HomeClass::ApiKey);
    let account = f.router.entry(HomeClass::Account).unwrap(); let snapshot = account.host.snapshot();
    assert!(snapshot["serverRequests"].as_array().unwrap().iter().any(|r|r["requestIdentity"]=="named"&&r["originClass"]=="named-service"));
    assert!(snapshot["serverRequests"].as_array().unwrap().iter().any(|r|r["requestIdentity"]=="settled"&&r["state"]=="resolved-by-supplier"));
    assert_eq!(status["waitingRequests"]["groups"].as_array().unwrap().len(),1);
    let mut menu = crate::native_waiting::Registry::default();
    let entries = menu.project(&status["waitingRequests"]);
    assert_eq!(entries.len(), 1, "native menu uses ready, current, person-answerable overview eligibility");
    assert_eq!(entries[0].label, "account · conversation unloaded-thread: 1");
    assert_eq!(status["waitingRequests"]["groups"][0]["threadId"],"unloaded-thread");
    let generation=snapshot["generation"].clone();
    assert!(crate::waiting_requests::open(&mut f.router,"api-key",&generation,&json!("unloaded-thread")).is_err());
    assert_eq!(f.router.active().class(),HomeClass::ApiKey,"source collision cannot switch home");
    assert!(crate::waiting_requests::open(&mut f.router,"account",&generation,&json!("settled-thread")).is_err());
    let unloaded=crate::waiting_requests::open(&mut f.router,"account",&generation,&json!("unloaded-thread")).unwrap();
    assert_eq!(unloaded["threadLoaded"],false,"navigation must not load/resume an unknown conversation");
    let after=account.host.snapshot();
    assert_eq!(after["clientRequests"],snapshot["clientRequests"],"projection/navigation dispatch no native request");
    assert_eq!(after["serverRequests"],snapshot["serverRequests"],"projection/navigation settle no request");
}

#[test]
fn replaced_full_generation_never_retargets_a_same_named_successor_group() {
    let mut f=Fixture::new();f.emit(HomeClass::Account,vec![question(json!(7),Some("shared-thread"))]);
    let old=f.status(HomeClass::Account);let account=f.router.entry(HomeClass::Account).unwrap();
    account.host.stop("waiting regression", "source replacement").unwrap();
    assert!(crate::waiting_requests::overview(&f.router)["groups"].as_array().unwrap().is_empty());
    account.host.start(account.host_config.as_ref().unwrap(),"synthetic replacement").unwrap();
    f.emit(HomeClass::Account,vec![question(json!(7),Some("shared-thread"))]);
    f.router.activate(HomeClass::ApiKey).unwrap();
    let refused=crate::waiting_requests::open(&mut f.router,"account",&old["generation"],&json!("shared-thread")).unwrap_err();
    assert_eq!(f.router.active().class(),HomeClass::ApiKey);
    let fresh=f.status(HomeClass::ApiKey);
    assert_ne!(fresh["waitingRequests"]["groups"][0]["generation"],old["generation"]);
    assert_eq!(fresh["waitingRequests"]["groups"][0]["count"],1,"closed predecessor is excluded");
    println!("WAITING_REQUESTS_STALE_DTO:{}",json!({"old":old,"fresh":fresh,"error":refused}));
}


#[test]
fn native_waiting_equal_count_replacement_retires_original_ids_and_escapes_only_labels() {
    let mut f = Fixture::new();
    f.emit(HomeClass::Account, vec![question(json!("first"), Some("shared-thread"))]);
    let mut menu = crate::native_waiting::Registry::default();
    let original = menu.project(&crate::waiting_requests::overview(&f.router));
    let special = "R&D && <literal> / 家 \"quoted\"";
    f.emit(HomeClass::Account, vec![json!({"method":"serverRequest/resolved","params":{"threadId":"shared-thread","requestId":"first"}}), question(json!("replacement"), Some(special))]);
    let before = f.router.entry(HomeClass::Account).unwrap().host.snapshot();
    let replacement = menu.project(&crate::waiting_requests::overview(&f.router));
    assert_eq!(original.len(), replacement.len());
    assert_ne!(original[0].id, replacement[0].id);
    assert!(replacement[0].label.contains(special), "projection keeps the native identity literal");
    assert_eq!(crate::native_waiting::literal_label(&replacement[0].label), "account · conversation R&&D &&&& <literal> / 家 \"quoted\": 1");
    assert!(menu.select(&original[0].id, &f.router).unwrap_err().contains("retired"));
    assert!(menu.select("chirality-waiting-item-unknown", &f.router).is_err());
    f.router.activate(HomeClass::ApiKey).unwrap();
    menu.select(&replacement[0].id, &f.router).unwrap();
    menu.checkpoint("literal-consumer", 0).unwrap();
    let claim = menu.claim("literal-consumer", &f.router);
    assert_eq!(claim["target"]["threadId"], special, "label escaping cannot alter the dispatched target");
    assert_eq!(f.router.active().class(), HomeClass::ApiKey);
    let opened = crate::waiting_requests::open(&mut f.router, "account", &claim["target"]["generation"], &claim["target"]["threadId"]).unwrap();
    assert_eq!(opened["threadLoaded"], false);
    let account_status = f.status(HomeClass::Account);
    let key_status = f.status(HomeClass::ApiKey);
    println!("WAITING_NATIVE_SPECIAL_DTO:{}", json!({"claim":claim,"account":account_status,"api-key":key_status,"opened":opened}));
    let after = f.router.entry(HomeClass::Account).unwrap().host.snapshot();
    assert_eq!(after["clientRequests"], before["clientRequests"]);
    assert_eq!(after["serverRequests"], before["serverRequests"]);
    // Returning to an earlier target also receives a new ID, never its retired ID.
    f.emit(HomeClass::Account, vec![question(json!("again"), Some("shared-thread"))]);
    let again = menu.project(&crate::waiting_requests::overview(&f.router));
    assert!(again.iter().all(|e|e.id != original[0].id));
    f.emit(HomeClass::Account, vec![question(json!("another"), Some(special))]);
    let changed_count = menu.project(&crate::waiting_requests::overview(&f.router));
    assert_ne!(again[0].id, changed_count[0].id, "changed per-conversation counts refresh the menu");
    assert!(changed_count[0].label.ends_with(": 2"));
}

#[test]
fn native_waiting_delivery_is_single_use_and_reload_busy_and_source_closure_refuse() {
    let mut f = Fixture::new();
    f.emit(HomeClass::Account, vec![question(json!("live"), Some("shared-thread"))]);
    let mut menu = crate::native_waiting::Registry::default();
    let entries = menu.project(&crate::waiting_requests::overview(&f.router));
    f.router.activate(HomeClass::ApiKey).unwrap();
    let before = f.router.entry(HomeClass::Account).unwrap().host.snapshot();
    menu.select(&entries[0].id, &f.router).unwrap();
    assert!(menu.select(&entries[0].id, &f.router).unwrap_err().contains("pending"));
    menu.checkpoint("window-1", 0).unwrap();
    let claim = menu.claim("window-1", &f.router);
    assert_eq!(claim["target"]["generation"], before["generation"]);
    assert!(menu.claim("window-1", &f.router).is_null(), "polling cannot redeliver a claimed intent");
    assert!(menu.finish("wrong-window", claim["intentId"].as_str().unwrap()).is_err());
    let reload_refusal = menu.claim("reloaded-window", &f.router);
    assert!(reload_refusal["refused"].as_str().unwrap().contains("reload"));
    assert!(menu.finish("window-1", claim["intentId"].as_str().unwrap()).is_err());
    assert!(menu.claim("reloaded-window", &f.router).is_null());
    menu.checkpoint("window-2", 0).unwrap();
    menu.select(&entries[0].id, &f.router).unwrap();
    let retry = menu.claim("window-2", &f.router);
    menu.finish("window-2", retry["intentId"].as_str().unwrap()).unwrap();
    assert!(menu.claim("window-2", &f.router).is_null());
    menu.checkpoint("lost-IPC", 0).unwrap();
    menu.select(&entries[0].id, &f.router).unwrap();
    menu.claim("lost-IPC", &f.router);
    menu.abandon("another-consumer");
    assert!(menu.select(&entries[0].id, &f.router).is_err());
    menu.abandon("lost-IPC");
    assert!(menu.claim("lost-IPC", &f.router).is_null());
    assert_eq!(f.router.active().class(), HomeClass::ApiKey, "dispatch/claim/finish never navigate");
    assert_eq!(f.router.entry(HomeClass::Account).unwrap().host.snapshot()["clientRequests"], before["clientRequests"]);
    menu.select(&entries[0].id, &f.router).unwrap();
    f.emit(HomeClass::Account, vec![json!({"method":"serverRequest/resolved","params":{"threadId":"shared-thread","requestId":"live"}})]);
    let closure_refusal = menu.claim("window-3", &f.router);
    assert!(closure_refusal["refused"].as_str().unwrap().contains("no current waiting"));
    println!("WAITING_NATIVE_REFUSALS_DTO:{}", json!({"reload":reload_refusal,"closure":closure_refusal}));
    assert!(menu.select(&entries[0].id, &f.router).is_err(), "a still-visible stale menu item must use full waiting validation");
    assert_eq!(f.router.active().class(), HomeClass::ApiKey);
}

#[test]
fn native_waiting_closed_h5_cannot_retarget_same_thread_in_successor() {
    let mut f = Fixture::new();
    f.emit(HomeClass::Account, vec![question(json!(7), Some("shared-thread"))]);
    let mut menu = crate::native_waiting::Registry::default();
    let old = menu.project(&crate::waiting_requests::overview(&f.router));
    menu.select(&old[0].id, &f.router).unwrap();
    let account = f.router.entry(HomeClass::Account).unwrap();
    account.host.stop("native waiting regression", "source replacement").unwrap();
    account.host.start(account.host_config.as_ref().unwrap(), "synthetic replacement").unwrap();
    f.emit(HomeClass::Account, vec![question(json!(7), Some("shared-thread"))]);
    f.router.activate(HomeClass::ApiKey).unwrap();
    assert!(menu.claim("window", &f.router)["refused"].as_str().unwrap().contains("no longer current"));
    assert!(menu.select(&old[0].id, &f.router).is_err());
    let fresh = menu.project(&crate::waiting_requests::overview(&f.router));
    assert_ne!(old[0].id, fresh[0].id);
    assert_eq!(f.router.active().class(), HomeClass::ApiKey);
}


#[test]
fn native_waiting_partial_menu_failure_republishes_when_desired_returns_to_previous_success() {
    let f = Fixture::new();
    f.emit(HomeClass::Account, vec![question(json!(1), Some("shared-thread"))]);
    f.emit(HomeClass::ApiKey, vec![question(json!(2), Some("shared-thread"))]);
    let mut registry = crate::native_waiting::Registry::default();
    let original = registry.project(&crate::waiting_requests::overview(&f.router));
    assert_eq!(original.len(), 2);
    let mut reordered = original.clone(); reordered.reverse();
    let mut observer = crate::native_waiting::MenuObserver::default();
    let mut native = Vec::new(); let mut updates = 0;
    observer.publish(original.clone(), |entries| { updates += 1; native = entries.to_vec(); Ok::<_, &str>(()) }).unwrap();
    let failure = observer.publish(reordered, |entries| {
        updates += 1; native.clear(); native.push(entries[0].clone());
        Err("synthetic partial native menu mutation")
    });
    assert!(failure.is_err());
    observer.publish(original.clone(), |entries| { updates += 1; native = entries.to_vec(); Ok::<_, &str>(()) }).unwrap();
    assert_eq!(native, original, "returning to the old desired menu must repair a partially mutated native menu");
    assert_eq!(updates, 3);
    observer.publish(original, |_| { updates += 1; Ok::<_, &str>(()) }).unwrap();
    assert_eq!(updates, 3, "only a fully successful unchanged publication can be skipped");
}


#[test]
fn native_waiting_checkpoint_binds_selection_before_lost_wake_and_keeps_later_click_usable() {
    let mut f = Fixture::new();
    f.emit(HomeClass::Account, vec![question(json!(1), Some("shared-thread"))]);
    f.router.activate(HomeClass::ApiKey).unwrap();
    let before = f.router.entry(HomeClass::Account).unwrap().host.snapshot();
    let mut registry = crate::native_waiting::Registry::default();
    let entries = registry.project(&crate::waiting_requests::overview(&f.router));
    registry.checkpoint("window", 0).unwrap();
    registry.select(&entries[0].id, &f.router).unwrap(); // its wake is lost
    registry.checkpoint("window", 1).unwrap(); // acknowledged newer UI choice
    assert!(registry.claim("window", &f.router)["refused"].as_str().unwrap().contains("older or uncertain"));
    // A new click after acknowledgment remains usable; an unchanged-UI delayed
    // claim also retains its checkpoint and is delivered exactly once.
    registry.select(&entries[0].id, &f.router).unwrap();
    let fresh = registry.claim("window", &f.router);
    assert_eq!(fresh["checkpoint"], json!({"consumer":"window","revision":1}));
    assert_eq!(fresh["target"]["generation"], before["generation"]);
    assert!(registry.claim("window", &f.router).is_null());
    registry.finish("window", fresh["intentId"].as_str().unwrap()).unwrap();
    assert!(registry.checkpoint("window", 0).is_err(), "late checkpoint cannot restore an older basis");
    registry.select(&entries[0].id, &f.router).unwrap();
    registry.checkpoint("new-window", 0).unwrap();
    assert!(registry.claim("new-window", &f.router)["refused"].as_str().unwrap().contains("older or uncertain"),
        "a queued pre-reload selection is not relabeled to the new consumer");
    let mut startup = crate::native_waiting::Registry::default();
    let initial = startup.project(&crate::waiting_requests::overview(&f.router));
    startup.select(&initial[0].id, &f.router).unwrap();
    startup.checkpoint("first-attachment", 0).unwrap();
    assert_eq!(startup.claim("first-attachment", &f.router)["checkpoint"], json!({"consumer":"first-attachment","revision":0}));
    let mut edited_startup = crate::native_waiting::Registry::default();
    let initial = edited_startup.project(&crate::waiting_requests::overview(&f.router));
    edited_startup.select(&initial[0].id, &f.router).unwrap();
    edited_startup.checkpoint("edited-before-attachment", 1).unwrap();
    assert!(edited_startup.claim("edited-before-attachment", &f.router)["refused"].as_str().unwrap().contains("older or uncertain"),
        "a first checkpoint after a UI edit cannot adopt an unbound startup selection");
    edited_startup.select(&initial[0].id, &f.router).unwrap();
    assert_eq!(edited_startup.claim("edited-before-attachment", &f.router)["checkpoint"], json!({"consumer":"edited-before-attachment","revision":1}));
    assert_eq!(f.router.active().class(), HomeClass::ApiKey, "UI handshake and claim do not activate homes");
    assert_eq!(f.router.entry(HomeClass::Account).unwrap().host.snapshot()["clientRequests"], before["clientRequests"]);
}
