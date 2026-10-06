//! Synthetic native-source controls; no supplier/process/model execution.
use super::*;
use crate::recovery::{ExplicitAppProjectContext, AppProjectSource};
struct Fixture {host:Host, root:PathBuf, g:Value}
impl Fixture {
    fn new()->Self {
        let root=std::env::temp_dir().join(opaque_id("rec-custody-").unwrap());std::fs::create_dir(&root).unwrap();
        let host=Host::new();host.configure_recovery(root.join("ledger.jsonl")).unwrap();
        let g={let mut i=host.inner.0.lock().unwrap();let g=json!({"appSession":i.app_session,"home":"owned-physical-home","spawnCounter":1});i.generation=g.clone();i.home="owned-physical-home".into();i.spawn_counter=1;i.state="ready".into();i.threads.push(json!({"generation":g,"threadId":"t"}));g};
        Self{host,root,g}
    }
    fn index(&self){self.host.observe_conversation_project(&self.g,"t",Some("H-acct"),&ExplicitAppProjectContext::known("P",AppProjectSource::ConfiguredDirectory).unwrap()).unwrap();}
    fn frame(&self,method:&str,params:Value){self.host.on_line(&serde_json::to_vec(&json!({"method":method,"params":params})).unwrap(),&self.g);}
    fn turn(&self,status:&str){self.frame(if status=="inProgress"{"turn/started"}else{"turn/completed"},json!({"threadId":"t","turn":{"id":"u","status":status,"items":[]}}));}
    fn item(&self,method:&str,id:&str){self.frame(method,json!({"threadId":"t","turnId":"u","item":{"id":id,"type":"commandExecution","status":"inProgress","command":"NEVER_PERSIST_THIS","output":"NEVER_COPY_OUTPUT"}}));}
    fn close(&self){Host::close_generation(&mut self.host.inner.0.lock().unwrap());self.host.flush_recovery_observations();}
    fn rows(&self)->Vec<Value>{self.host.snapshot()["recovery"]["entries"].as_array().unwrap().clone()}
}
impl Drop for Fixture{fn drop(&mut self){let _=std::fs::remove_dir_all(&self.root);}}
fn validate_event(event:&Value){let schema:Value=serde_json::from_str(include_str!("../resources/runtime_core/recovery.custody-event.schema.json")).unwrap();jsonschema::options().offline().build(&schema).unwrap().validate(event).unwrap();}
#[test]
fn source_to_durable_loss_and_restart_without_ui_poll(){
    let f=Fixture::new();f.index();f.turn("inProgress");f.item("item/started","i");
    f.close();let view=f.host.recovery_custody().snapshot();let event=&view["live"]["events"][0];validate_event(event);
    assert_eq!(event["inFlightItems"][0]["itemId"],"i");assert_eq!(event["cause"],"supplier-exit");
    let rows=f.rows();let index=rows.iter().rev().find(|r|r["kind"]=="conversation_index").unwrap();
    assert_eq!(index["lastObservedExecution"]["state"],"observation-lost");assert_eq!(index["lastObservedExecution"]["openItems"][0]["itemId"],"i");
    let bytes=std::fs::read_to_string(f.root.join("ledger.jsonl")).unwrap();assert!(!bytes.contains("NEVER_"));
    let mut reopened=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();reopened.start_session("new-app-session","candidate").unwrap();
    let restored=crate::recovery::RecoveryCustodyView::from_owner("new-app-session",Some(&reopened.snapshot()),json!({}),0,None).snapshot();
    validate_event(&restored["restartEvents"][0]);assert_eq!(restored["restartEvents"][0]["priorSessionEnd"],"ended-without-record");assert_eq!(restored["automaticResume"],false);
    assert_eq!(f.host.snapshot()["clientRequests"],json!([]));
    let before=f.rows();f.close();let again=f.host.recovery_custody().snapshot();assert_eq!(f.rows(),before);assert_eq!(again["live"]["events"].as_array().unwrap().len(),1);
}
#[test]
fn terminal_completion_and_foreign_receipts_do_not_revive_custody(){
    let f=Fixture::new();f.index();f.turn("inProgress");f.item("item/started","i");f.item("item/completed","i");f.item("item/started","i");
    f.turn("completed");f.turn("inProgress");f.item("item/started","late");
    let foreign=json!({"appSession":f.g["appSession"],"home":"other","spawnCounter":1});
    f.host.on_line(&serde_json::to_vec(&json!({"method":"item/started","params":{"threadId":"t","turnId":"u","item":{"id":"foreign","type":"reasoning"}}})).unwrap(),&foreign);
    f.close();let view=f.host.recovery_custody().snapshot();let event=&view["live"]["events"][0];validate_event(event);assert_eq!(event["liveTurns"],json!([]));assert_eq!(event["inFlightItems"],json!([]));
    let mut reopened=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();reopened.start_session("next","c").unwrap();assert_eq!(crate::recovery::RecoveryCustodyView::from_owner("next",Some(&reopened.snapshot()),json!({}),0,None).snapshot()["restartEvents"],json!([]));
}
#[test]
fn missing_index_stays_hot_only_and_status_has_no_write_effect(){
    let f=Fixture::new();f.turn("inProgress");f.item("item/started","i");let before=f.rows();let _=f.host.recovery_custody();assert_eq!(f.rows(),before);
    f.close();assert!(f.rows().iter().all(|r|r["kind"]!="conversation_index"));let view=f.host.recovery_custody().snapshot();assert_eq!(view["live"]["events"],json!([]));assert!(!view["live"]["limits"].as_array().unwrap().is_empty());assert_eq!(view["live"]["observations"][0]["openItems"][0]["itemId"],"i");
}
#[test]
fn queued_facts_stay_distinct_and_context_tags_survive(){
    let f=Fixture::new();f.index();
    // Emulate a legitimate prior owning tag append using the actual ledger.
    {let mut i=f.host.inner.0.lock().unwrap();let ledger=i.recovery.as_ref().unwrap().clone();let mut l=ledger.lock().unwrap();let mut row=l.snapshot()["entries"].as_array().unwrap().iter().rev().find(|r|r["kind"]=="conversation_index").unwrap().clone();row["tags"]=json!([{"owner":"receiver","value":"opaque","seq":1}]);l.append(row).unwrap();i.recovery_snapshot=Some(l.snapshot());}
    f.host.observe_conversation_project(&f.g,"t",Some("H-acct"),&ExplicitAppProjectContext::known("Q",AppProjectSource::OpenedDirectory).unwrap()).unwrap();
    let writer=f.host.recovery_writer.lock().unwrap();f.turn("inProgress");f.item("item/started","i");
    let view=f.host.recovery_custody().snapshot();assert!(view["pendingPointerFacts"].as_u64().unwrap()>0);assert_eq!(view["historicalConversations"][0]["index"]["lastObservedExecution"]["state"],"indexed");
    let before=f.rows();let _=f.host.recovery_custody();assert_eq!(f.rows(),before);drop(writer);f.host.flush_recovery_observations();
    let rows=f.rows();let last=rows.iter().rev().find(|r|r["kind"]=="conversation_index").unwrap();assert_eq!(last["project"],"P");assert_eq!(last["tags"][0]["value"],"opaque");assert_eq!(last["lastObservedExecution"]["state"],"turn-live");
}
#[test]
fn append_failure_keeps_original_execution_rows_for_later_flush(){
    let f=Fixture::new();f.index();let path=f.root.join("ledger.jsonl");let backup=f.root.join("original");std::fs::rename(&path,&backup).unwrap();std::fs::create_dir(&path).unwrap();
    f.turn("inProgress");f.item("item/started","i");f.close();let pending=f.host.snapshot()["recoveryPendingObservations"].clone();assert!(!pending.as_array().unwrap().is_empty());assert!(!f.host.recovery_custody().snapshot()["limits"].as_array().unwrap().is_empty());
    std::fs::remove_dir(&path).unwrap();std::fs::rename(&backup,&path).unwrap();f.host.flush_recovery_observations();let rows=f.rows();for row in pending.as_array().unwrap(){assert_eq!(rows.iter().filter(|r|*r==row).count(),1);}assert_eq!(f.host.recovery_custody().snapshot()["pendingPointerFacts"],0);
}
#[test]
fn delayed_older_generation_row_cannot_replace_newer_cold_observation(){
    let f=Fixture::new();f.index();f.turn("inProgress");f.item("item/started","i");let old=f.rows().iter().rev().find(|r|r["kind"]=="conversation_index").unwrap().clone();
    let mut current=old.clone();let next=json!({"appSession":f.g["appSession"],"home":f.g["home"],"spawnCounter":2});current["lastLoadedGeneration"]=json!(crate::recovery::generation_ref(&next).unwrap());current["lastObservedExecution"]=json!({"state":"loaded-idle","at":"new"});
    let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();ledger.append(current).unwrap();ledger.append(old).unwrap();ledger.start_session("new","c").unwrap();
    let view=crate::recovery::RecoveryCustodyView::from_owner("new",Some(&ledger.snapshot()),json!({}),0,None).snapshot();assert_eq!(view["historicalConversations"][0]["index"]["lastObservedExecution"]["state"],"loaded-idle");assert_eq!(view["restartEvents"],json!([]));
}
#[test]
fn rc1_item_only_and_competing_turn_pointers_survive_reopen_without_live_inference(){
    for competing in [false,true] {
        let f=Fixture::new();f.index();if competing{f.turn("inProgress");}
        f.frame("item/started",json!({"threadId":"t","turnId":"other-turn","item":{"id":"orphan","type":"reasoning"}}));f.close();
        let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();ledger.start_session("new","c").unwrap();
        let view=crate::recovery::RecoveryCustodyView::from_owner("new",Some(&ledger.snapshot()),json!({}),0,None).snapshot();
        let pointers=&view["historicalConversations"][0]["index"]["lastObservedExecution"]["openItems"];
        assert!(pointers.as_array().is_some_and(|a|a.iter().any(|i|i["itemId"]=="orphan")),"known item pointer disappeared");
        if !competing {assert!(view["historicalConversations"][0]["index"]["lastObservedExecution"]["liveTurn"].is_null());assert_eq!(view["restartEvents"],json!([]));}
    }
}
#[test]
fn rc3_terminal_method_with_active_status_never_revives_custody(){
    let f=Fixture::new();f.index();f.frame("turn/completed",json!({"threadId":"t","turn":{"id":"u","status":"inProgress","items":[]}}));
    f.item("item/started","late");f.close();let view=f.host.recovery_custody().snapshot();
    assert_eq!(view["live"]["events"][0]["liveTurns"],json!([]));assert_eq!(view["live"]["events"][0]["inFlightItems"],json!([]));
    let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();ledger.start_session("next","c").unwrap();assert_eq!(crate::recovery::RecoveryCustodyView::from_owner("next",Some(&ledger.snapshot()),json!({}),0,None).snapshot()["restartEvents"],json!([]));
}
#[test]
fn source_quit_loss_and_clean_end_require_actual_live_pointer(){
    let f=Fixture::new();f.index();f.turn("inProgress");f.item("item/started","i");
    f.host.stop("owned source fixture","App quit").unwrap();
    let custody=f.host.app_runtime_custody().unwrap();assert_eq!(custody.record_app_session_end(&[]).unwrap()["write"],"confirmed");
    let live=f.host.recovery_custody().snapshot();assert_eq!(live["live"]["events"][0]["cause"],"app-quit");validate_event(&live["live"]["events"][0]);
    let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();ledger.start_session("relaunch","c").unwrap();let v=crate::recovery::RecoveryCustodyView::from_owner("relaunch",Some(&ledger.snapshot()),json!({}),0,None).snapshot();validate_event(&v["restartEvents"][0]);assert_eq!(v["restartEvents"][0]["priorSessionEnd"],"quit-with-live-work");
    // Clean App metadata after a different loss does not prove live-at-quit.
    let f=Fixture::new();f.index();f.turn("inProgress");f.close();f.host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();ledger.start_session("relaunch","c").unwrap();let v=crate::recovery::RecoveryCustodyView::from_owner("relaunch",Some(&ledger.snapshot()),json!({}),0,None).snapshot();assert_eq!(v["restartEvents"],json!([]));assert!(!v["limits"].as_array().unwrap().is_empty());
}
#[test]
fn separate_home_equal_labels_and_fork_provenance_remain_separate(){
    let f=Fixture::new();f.index();
    {let mut i=f.host.inner.0.lock().unwrap();let owner=i.recovery.as_ref().unwrap().clone();let mut ledger=owner.lock().unwrap();let mut row=ledger.snapshot()["entries"].as_array().unwrap().last().unwrap().clone();row["forkedFrom"]=json!("source-thread");ledger.append(row).unwrap();i.recovery_snapshot=Some(ledger.snapshot());}
    f.turn("inProgress");f.item("item/started","i");f.close();
    let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();let mut row=ledger.snapshot()["entries"].as_array().unwrap().last().unwrap().clone();let g=json!({"appSession":f.g["appSession"],"home":"separate-physical-home","spawnCounter":1});row["home"]=json!("H-key");row["lastLoadedGeneration"]=json!(crate::recovery::generation_ref(&g).unwrap());row["project"]=json!("other-project");ledger.append(row).unwrap();ledger.start_session("relaunch","c").unwrap();
    let v=crate::recovery::RecoveryCustodyView::from_owner("relaunch",Some(&ledger.snapshot()),json!({}),0,None).snapshot();assert_eq!(v["historicalConversations"].as_array().unwrap().len(),2);assert_eq!(v["restartEvents"].as_array().unwrap().len(),2);for e in v["restartEvents"].as_array().unwrap(){validate_event(e);}assert_eq!(v["historicalConversations"][0]["index"]["forkedFrom"],"source-thread");
}
#[test]
fn unavailable_and_legacy_generation_projection_retains_limits_without_actions(){
    let v=crate::recovery::RecoveryCustodyView::from_owner("new",None,json!({}),0,Some("history unreadable")).snapshot();assert_eq!(v["restartEvents"],json!([]));assert!(!v["limits"].as_array().unwrap().is_empty());
    let f=Fixture::new();f.index();let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();let mut row=ledger.snapshot()["entries"].as_array().unwrap().last().unwrap().clone();row["lastLoadedGeneration"]=json!("legacy-unqualified-generation");ledger.append(row).unwrap();ledger.start_session("new","c").unwrap();let v=crate::recovery::RecoveryCustodyView::from_owner("new",Some(&ledger.snapshot()),json!({}),0,None).snapshot();assert_eq!(v["restartEvents"],json!([]));assert!(v["limits"].as_array().unwrap().iter().any(|s|s.as_str().unwrap().contains("canonical full generation")));assert_eq!(v["automaticResume"],false);
}
#[test]
fn cold03_item_only_competing_turns_and_same_labels_retain_exact_associations(){
    for competing in [false,true] {
        let f=Fixture::new();f.index();if competing{f.turn("inProgress");}
        for turn in ["turn-A","turn-B"] {f.frame("item/started",json!({"threadId":"t","turnId":turn,"item":{"id":"same-item","type":"mcpToolCall"}}));}
        f.close();let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();ledger.start_session("cold03","candidate").unwrap();
        let view=crate::recovery::RecoveryCustodyView::from_owner("cold03",Some(&ledger.snapshot()),json!({}),0,None).snapshot();let row=&view["historicalConversations"][0];
        let items=row["index"]["lastObservedExecution"]["openItems"].as_array().unwrap();assert_eq!(items.len(),2);
        assert_eq!(items.iter().map(|i|i["turnId"].as_str().unwrap()).collect::<Vec<_>>(),vec!["turn-A","turn-B"]);
        let associations=row["openItemAssociations"].as_array().unwrap();assert_eq!(associations.len(),2);
        for (association,turn) in associations.iter().zip(["turn-A","turn-B"]) {assert_eq!(association["turnId"],turn);assert_eq!(association["fullTuple"]["generation"],f.g);assert_eq!(association["fullTuple"]["home"],"H-acct");assert_eq!(association["fullTuple"]["threadId"],"t");assert_eq!(association["fullTuple"]["itemId"],"same-item");assert_eq!(association["correlation"],"known persisted association");}
        if !competing {assert!(row["index"]["lastObservedExecution"]["liveTurn"].is_null());assert_eq!(view["restartEvents"],json!([]));}
        else {assert_eq!(row["index"]["lastObservedExecution"]["liveTurn"],"u");assert_eq!(view["restartEvents"][0]["liveTurnsAtEnd"][0]["turnId"],"u");}
    }
}
#[test]
fn cold03_item_completion_and_terminal_settle_only_matching_turn_tuples(){
    for terminal in [false,true] {
        let f=Fixture::new();f.index();
        for turn in ["turn-A","turn-B"]{f.frame("item/started",json!({"threadId":"t","turnId":turn,"item":{"id":"same-item","type":"reasoning"}}));}
        if terminal {f.frame("turn/completed",json!({"threadId":"t","turn":{"id":"turn-A","status":"completed","items":[]}}));}
        else {f.frame("item/completed",json!({"threadId":"t","turnId":"turn-A","item":{"id":"same-item","type":"reasoning"}}));}
        f.frame("item/started",json!({"threadId":"t","turnId":"turn-A","item":{"id":"same-item","type":"reasoning"}}));f.close();
        let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();ledger.start_session("cold03","candidate").unwrap();let view=crate::recovery::RecoveryCustodyView::from_owner("cold03",Some(&ledger.snapshot()),json!({}),0,None).snapshot();
        let items=view["historicalConversations"][0]["index"]["lastObservedExecution"]["openItems"].as_array().unwrap();assert_eq!(items.len(),1);assert_eq!(items[0]["turnId"],"turn-B");assert_eq!(view["restartEvents"],json!([]));
    }
}
#[test]
fn cold03_legacy_unknown_stays_unknown_beside_live_turn_without_migration(){
    let f=Fixture::new();f.index();let mut ledger=RecoveryLedger::open(f.root.join("ledger.jsonl")).unwrap();let mut row=ledger.snapshot()["entries"].as_array().unwrap().last().unwrap().clone();
    row["lastObservedExecution"]=json!({"state":"turn-live","at":"old","liveTurn":"not-an-item-association","openItems":[{"itemId":"legacy","itemType":"reasoning"},{"turnId":"known-turn","itemId":"new","itemType":"reasoning"}]});ledger.append(row).unwrap();let prior=std::fs::read(f.root.join("ledger.jsonl")).unwrap();ledger.start_session("cold03","c").unwrap();
    let view=crate::recovery::RecoveryCustodyView::from_owner("cold03",Some(&ledger.snapshot()),json!({}),0,None).snapshot();let items=view["historicalConversations"][0]["openItemAssociations"].as_array().unwrap();assert!(items[0]["turnId"].is_null());assert!(items[0]["fullTuple"].is_null());assert_eq!(items[0]["correlation"],"unknown; historical row supplies no per-item turn");assert_eq!(items[1]["turnId"],"known-turn");assert!(!items[1]["fullTuple"].is_null());assert!(std::fs::read(f.root.join("ledger.jsonl")).unwrap().starts_with(&prior));
}
#[test]
fn cold03_exact_adopted_schema_examples_and_old_reader_boundary(){
    let new:Value=serde_json::from_str(include_str!("../resources/runtime_core/recovery.app-ledger-entry.schema.json")).unwrap();let old:Value=serde_json::from_str(include_str!("../resources/runtime_core/recovery.app-ledger-entry.v0.2.schema.json")).unwrap();
    assert_eq!(new["$id"],"urn:chirality:app-v4:del-01-02:app-ledger-entry:0.3");assert_eq!(old["$id"],"urn:chirality:app-v4:del-01-02:app-ledger-entry:0.2");let newer=jsonschema::options().offline().build(&new).unwrap();let older=jsonschema::options().offline().build(&old).unwrap();
    let examples=[(include_str!("../resources/runtime_core/recovery.app-ledger-entry.item-turn.item-only.valid.json"),true,false),(include_str!("../resources/runtime_core/recovery.app-ledger-entry.item-turn.competing-turns.valid.json"),true,false),(include_str!("../resources/runtime_core/recovery.app-ledger-entry.item-turn.legacy-unknown.valid.json"),true,true),(include_str!("../resources/runtime_core/recovery.app-ledger-entry.item-turn.empty-turn.invalid.json"),false,false),(include_str!("../resources/runtime_core/recovery.app-ledger-entry.item-turn.null-turn.invalid.json"),false,false),(include_str!("../resources/runtime_core/recovery.app-ledger-entry.item-turn.payload.invalid.json"),false,false)];
    for (bytes,n,o) in examples {let row:Value=serde_json::from_str(bytes).unwrap();assert_eq!(newer.is_valid(&row),n);assert_eq!(older.is_valid(&row),o);}
}
