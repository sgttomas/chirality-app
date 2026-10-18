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
    println!("WAITING_REQUESTS_DTO:{}", json!({"account":account,"api-key":key,"navigation":{"account":open_account,"api-key":open_key,"unnamed":open_unnamed}}));
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
