use super::*;
use crate::hosting::AppRuntimeCustody;

fn fixture() -> Fixture {
    let f=Fixture::new("pass");
    let path=f.root.join("vendor/bin/codex");
    let code=std::fs::read_to_string(&path).unwrap().replace(" f=json.loads(line)"," f=json.loads(line)\n if f.get('method')=='fixture/exit': sys.exit(f['params']['code'])");
    std::fs::write(path,code).unwrap();
    f
}
fn wait_closed(h:&Host,cap:&AppRuntimeCustody,g:&Value)->Value {
    let until=std::time::Instant::now()+Duration::from_secs(10);
    loop {
        let got=h.distribution_evidence(g);
        if h.snapshot()["state"]=="exited-unexpectedly" && !cap.terminal_publication.lock_state().active && got["state"]!="pending" && got["generation"]==*g && !got["reason"].as_str().unwrap_or("").contains("not admitted") {return got;}
        assert!(std::time::Instant::now()<until,"LT12 harness deadline: {got}");
        std::thread::sleep(Duration::from_millis(5));
    }
}
#[test]
fn lt12_actual_selected_eof_retains_whole_event_and_original_lt09() {
    for code in [0,7] {
        let f=fixture();let h=Arc::new(Host::new());
        attach_selected_store(&h,&f,Some("reference/expected.json"));
        let cap=h.app_runtime_custody().unwrap();
        let g=h.start(&f.cfg,"synthetic LT12").unwrap()["generation"].clone();
        let prior=h.inner.0.lock().unwrap().successor_lt09_reference.clone().unwrap();
        let store=h.distribution_store_for_admission(true).unwrap().unwrap();
        let old=store.read_s1(&g,&prior).unwrap();
        let mut receiver=crate::runtime_session::RuntimeSession::default();
        assert_eq!(receiver.receive(&h.observe(&Value::Null,0))["nativeView"]["distributionEvidence"]["state"],"read");
        h.write_frame_scoped(&json!({"jsonrpc":"2.0","method":"fixture/exit","params":{"code":code}}),Some(&g)).unwrap();
        let got=wait_closed(&h,&cap,&g);assert_eq!(got["state"],"read","{got}");
        let event=h.lifecycle_events().into_iter().find(|e|e["transitionId"]=="LT-12").unwrap();
        assert_eq!(got["evidence"]["lifecycle"]["legacy_event"],event);
        assert_eq!(event["exitFacts"]["exitCode"],code);assert!(event.get("descendants").is_none());
        assert_eq!(got["evidence"]["artifact"],old["artifact"]);
        assert_eq!(store.read_s1(&g,&prior).unwrap(),old);
        assert_eq!(receiver.receive(&h.observe(&Value::Null,0))["nativeView"]["distributionEvidence"],got);
        let mut fresh=crate::runtime_session::RuntimeSession::default();
        assert!(fresh.receive(&h.observe(&Value::Null,0))["nativeView"]["distributionEvidence"].is_null());
        assert!(h.start(&f.cfg,"no direct restart").is_err());
    }
}

fn ready()->(Fixture,Arc<Host>,Arc<AppRuntimeCustody>,Value) {
    let f=fixture();let h=Arc::new(Host::new());attach_store(&h,&f);
    let cap=h.app_runtime_custody().unwrap();let g=h.start(&f.cfg,"LT12 schedule").unwrap()["generation"].clone();(f,h,cap,g)
}
fn exit(h:&Host,g:&Value){h.write_frame_scoped(&json!({"jsonrpc":"2.0","method":"fixture/exit","params":{"code":0}}),Some(g)).unwrap();}
fn idle(cap:&AppRuntimeCustody){let end=std::time::Instant::now()+Duration::from_secs(15);while cap.terminal_publication.lock_state().active {assert!(std::time::Instant::now()<end);std::thread::sleep(Duration::from_millis(5));}}
#[test]
fn lt12_then_lt23_uses_original_predecessor_without_repairing_legacy_gap(){
    let (_f,h,cap,g)=ready();let prior=h.inner.0.lock().unwrap().successor_lt09_reference.clone().unwrap();
    exit(&h,&g);assert_eq!(wait_closed(&h,&cap,&g)["state"],"read");
    h.stop("synthetic","after EOF").unwrap();idle(&cap);
    let got=h.distribution_evidence(&g);assert_eq!(got["state"],"read","{got}");
    let events=h.lifecycle_events();let terminal=events.iter().find(|e|e["transitionId"]=="LT-23").unwrap();
    assert_eq!(got["evidence"]["lifecycle"]["legacy_event"],*terminal);
    assert!(terminal["exitFacts"]["exitCode"].is_null(),"existing missing journal fact must not be synthesized");
    assert!(events.iter().any(|e|e["transitionId"]=="LT-19"&&e["fromState"]=="exited-unexpectedly"),"existing invalid intermediate row remains explicit");
    assert_eq!(serde_json::to_value(h.inner.0.lock().unwrap().successor_lt09_reference.clone().unwrap()).unwrap(),serde_json::to_value(prior).unwrap());
}
#[test]
fn lt12_pending_stop_invalidates_before_terminal_and_late_result_cannot_install(){
    {
        let (_f,h,cap,g)=ready();let (rx,go)=pause_at(&cap.terminal_publication.before_work);
        exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();
        assert_eq!(h.distribution_evidence(&g)["state"],"pending");
        let source=h.clone();let stop=std::thread::spawn(move||source.stop("synthetic","pending LT12"));
        let end=std::time::Instant::now()+Duration::from_secs(5);while h.snapshot()["state"]!="stopping"{assert!(std::time::Instant::now()<end);std::thread::yield_now();}
        assert_eq!(h.distribution_evidence(&g)["state"],"unavailable");
        // Keep the sole job active through LT23 admission: no queued retry.
        stop.join().unwrap().unwrap();let before=h.distribution_evidence(&g);assert_eq!(before["state"],"unavailable");
        go.send(()).unwrap();idle(&cap);assert_eq!(h.distribution_evidence(&g),before);
    }
}
#[test]
fn lt12_stop_wins_eof_gate_and_emits_only_lt23(){
    let (_f,h,cap,g)=ready();let (rx,go)=pause_at(&h.before_eof_gate);exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let source=h.clone();let stop=std::thread::spawn(move||source.stop("synthetic","wins EOF"));
    let end=std::time::Instant::now()+Duration::from_secs(5);while h.snapshot()["state"]!="stopping"{assert!(std::time::Instant::now()<end);std::thread::yield_now();}
    go.send(()).unwrap();stop.join().unwrap().unwrap();idle(&cap);
    assert!(!h.lifecycle_events().iter().any(|e|e["transitionId"]=="LT-12"));
    assert_eq!(h.distribution_evidence(&g)["evidence"]["lifecycle"]["legacy_event"]["transitionId"],"LT-23");
}
#[test]
fn lt12_late_lt09_success_and_error_cannot_override_ineligible_eof(){
    for damage in [false,true] {
        let f=fixture();let h=Arc::new(Host::new());let data=attach_store(&h,&f);let cap=h.app_runtime_custody().unwrap();
        let (rx,go)=pause_at(&h.before_s1_lt09_publish);let source=h.clone();let cfg=f.cfg.clone();let start=std::thread::spawn(move||source.start(&cfg,"late LT09"));
        rx.recv_timeout(Duration::from_secs(10)).unwrap();let g=h.snapshot()["generation"].clone();exit(&h,&g);
        let before=wait_closed(&h,&cap,&g);assert_eq!(before["state"],"unavailable");
        if damage {std::fs::rename(data.join("runtime/distribution"),data.join("original")).unwrap();std::fs::create_dir(data.join("runtime/distribution")).unwrap();}
        go.send(()).unwrap();let _=start.join().unwrap();assert_eq!(h.distribution_evidence(&g),before);
        assert!(h.inner.0.lock().unwrap().successor_lt09_reference.is_none());
    }
}
#[test]
fn lt12_spawn_failure_panic_and_immediate_completion_settle(){
    for mode in 0..3 {
        let (_f,h,cap,g)=ready();
        if mode==0 {cap.terminal_publication.fail_spawn.store(true,std::sync::atomic::Ordering::SeqCst);}
        if mode==1 {*cap.terminal_publication.before_work.lock().unwrap()=Some(Box::new(||panic!("synthetic LT12 worker panic")));}
        let controller=cap.terminal_publication.clone();*cap.terminal_publication.after_spawn.lock().unwrap()=Some(Box::new(move||{let end=std::time::Instant::now()+Duration::from_secs(10);while controller.lock_state().active{assert!(std::time::Instant::now()<end);std::thread::sleep(Duration::from_millis(5));}}));
        exit(&h,&g);let got=wait_closed(&h,&cap,&g);assert_eq!(got["state"],if mode==2{"read"}else{"unavailable"},"{got}");
        assert!(!h.inner.0.lock().unwrap().successor_terminal_pending);
    }
}
#[test]
fn lt12_restart_invalidates_late_success_error_and_panic(){
    for mode in 0..3 {
        let (f,h,cap,g)=ready();let (tx,rx)=std::sync::mpsc::channel();let (go,wait)=std::sync::mpsc::channel();
        *cap.terminal_publication.before_work.lock().unwrap()=Some(Box::new(move||{tx.send(()).unwrap();wait.recv_timeout(Duration::from_secs(15)).unwrap();if mode==2{panic!("stale LT12");}}));
        exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();h.stop("synthetic","restart").unwrap();
        let next=h.start(&f.cfg,"next generation").unwrap()["generation"].clone();let before=h.distribution_evidence(&next);
        if mode==1 {let root=f.root.join("app-data/runtime/distribution");std::fs::rename(&root,f.root.join("old-distribution")).unwrap();std::fs::create_dir(&root).unwrap();}
        go.send(()).unwrap();idle(&cap);
        if mode!=1 {assert_eq!(h.distribution_evidence(&next),before);}else{assert!(h.inner.0.lock().unwrap().successor_artifact_error.is_none());}
        assert_eq!(h.snapshot()["generation"],next);h.stop("synthetic","done").unwrap();idle(&cap);
    }
}
#[test]
fn lt12_closing_before_and_during_worker_disables_install(){
    for before in [false,true] {
        let (_f,h,cap,g)=ready();
        if before {cap.close_distribution_publication();exit(&h,&g);assert_eq!(wait_closed(&h,&cap,&g)["state"],"unavailable");}
        else {let (rx,go)=pause_at(&cap.terminal_publication.before_work);exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();cap.close_distribution_publication();go.send(()).unwrap();idle(&cap);assert_eq!(h.distribution_evidence(&g)["state"],"unavailable");}
        let i=h.inner.0.lock().unwrap();assert_eq!(serde_json::to_value(&i.successor_reference).unwrap(),serde_json::to_value(&i.successor_lt09_reference).unwrap());
    }
}
#[test]
fn lt12_one_app_permit_refuses_other_home_without_queue(){
    let (_f,h,cap,g)=ready();let (rx,go)=pause_at(&cap.terminal_publication.before_work);exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let f2=fixture();let h2=Arc::new(Host::new_with_app_custody(cap.clone()).unwrap());attach_store(&h2,&f2);let g2=h2.start(&f2.cfg,"other home").unwrap()["generation"].clone();
    exit(&h2,&g2);let end=std::time::Instant::now()+Duration::from_secs(10);while h2.snapshot()["state"]!="exited-unexpectedly"{assert!(std::time::Instant::now()<end);std::thread::yield_now();}
    // The first job owns the single permit, independent of home.
    let end=std::time::Instant::now()+Duration::from_secs(10);loop{let got=h2.distribution_evidence(&g2);if got["reason"].as_str().unwrap_or("").contains("busy"){break;}assert!(std::time::Instant::now()<end);std::thread::yield_now();}
    go.send(()).unwrap();idle(&cap);assert_eq!(h2.distribution_evidence(&g2)["state"],"unavailable");
}
#[test]
fn lt12_store_lease_and_replaced_root_controls(){
    for replace in [false,true] {
        let (f,h,cap,g)=ready();let store=h.distribution_store_for_admission(true).unwrap().unwrap();let authority=store.namespace_authority();
        let (tx,rx)=std::sync::mpsc::channel();let (go,wait)=std::sync::mpsc::channel();
        if replace {*cap.terminal_publication.before_work.lock().unwrap()=Some(Box::new(move||{tx.send(()).unwrap();wait.recv_timeout(Duration::from_secs(15)).unwrap();}));}
        else {store.before_s1_audit(move||{tx.send(()).unwrap();wait.recv_timeout(Duration::from_secs(15)).unwrap();});}
        exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();assert_eq!(h.snapshot()["state"],"exited-unexpectedly");
        let root=f.root.join("app-data/runtime/distribution");
        if replace {std::fs::rename(&root,f.root.join("saved")).unwrap();std::fs::create_dir(&root).unwrap();std::fs::set_permissions(&root,std::fs::Permissions::from_mode(0o700)).unwrap();}else{assert!(authority.admission(0).is_err());}
        go.send(()).unwrap();let got=wait_closed(&h,&cap,&g);assert_eq!(got["state"],if replace{"unavailable"}else{"read"});
        if replace {assert_eq!(std::fs::read_dir(root).unwrap().count(),0);}else{assert!(authority.admission(0).is_ok());}
    }
}
#[test]
fn lt12_exact_row_state_tuple_sequence_predecessor_and_repeated_eof(){
    let (_f,h,cap,g)=ready();exit(&h,&g);let got=wait_closed(&h,&cap,&g);assert_eq!(got["state"],"read");
    let event=h.lifecycle_events().into_iter().find(|e|e["transitionId"]=="LT-12").unwrap();
    let (prior,current,token)={let i=h.inner.0.lock().unwrap();(i.successor_lt09_reference.clone().unwrap(),i.successor_reference.clone().unwrap(),crate::hosting::TerminalToken{attempt:i.start_attempt,generation:g.clone(),sequence:i.successor_publication_sequence,kind:crate::hosting::TerminalKind::UnexpectedExit})};
    let store=h.distribution_store_for_admission(true).unwrap().unwrap();
    for key in ["transitionId","generation","sequence"] {let mut wrong=event.clone();wrong[key]=match key{"transitionId"=>json!("LT-23"),"sequence"=>json!(0),_=>json!({"appSession":"foreign"})};assert!(store.publish_lt12(&g,&prior,&wrong).is_err());}
    assert!(store.publish_lt12(&g,&current,&event).is_err());assert!(store.publish_lt23(&g,&prior,&event).is_err());
    for field in 0..4 {let mut wrong=token.clone();match field{0=>wrong.attempt+=1,1=>wrong.sequence+=1,2=>wrong.generation=json!({"foreign":true}),_=>wrong.kind=crate::hosting::TerminalKind::Stopped};wrong.unavailable(&h.inner,"must not install".into());assert_eq!(h.distribution_evidence(&g),got);}
    h.on_eof(&g);h.on_eof(&json!({"foreign":true}));
    assert_eq!(h.lifecycle_events().iter().filter(|e|e["transitionId"]=="LT-12").count(),1);assert_eq!(h.distribution_evidence(&g),got);
}
#[test]
fn lt12_missing_private_predecessor_or_app_custody_refuses(){
    for missing_cap in [false,true] {let (_f,h,cap,g)=ready();if missing_cap{*h.runtime_custody.lock().unwrap()=None;}else{h.inner.0.lock().unwrap().successor_lt09_reference=None;}
        exit(&h,&g);assert_eq!(wait_closed(&h,&cap,&g)["state"],"unavailable");assert!(!cap.terminal_publication.lock_state().active);
    }
}
#[test]
fn lt12_captured_request_closure_counts_survive_repeated_eof(){
    let f=fixture();let path=f.root.join("vendor/bin/codex");let code=std::fs::read_to_string(&path).unwrap().replace(" if 'id' in f:"," if f.get('method')=='fixture/request':\\n  print(json.dumps({'id':'supplier-request','method':'item/fileChange/requestApproval','params':{'threadId':'t','itemId':'i'}}),flush=True)\\n if f.get('method')=='fixture/unanswered': continue\\n if 'id' in f:").replace("\\n","\n");std::fs::write(path,code).unwrap();
    let h=Arc::new(Host::new());attach_store(&h,&f);let cap=h.app_runtime_custody().unwrap();let g=h.start(&f.cfg,"closure counts").unwrap()["generation"].clone();
    h.write_frame_scoped(&json!({"jsonrpc":"2.0","method":"fixture/request"}),Some(&g)).unwrap();
    let end=std::time::Instant::now()+Duration::from_secs(5);while h.snapshot()["serverRequests"].as_array().unwrap().is_empty(){assert!(std::time::Instant::now()<end);std::thread::yield_now();}
    let _request=h.request_begin_scoped("fixture/unanswered",json!({}),json!({"kind":"person-directed"}),false,Some(&g)).unwrap();
    let (rx,go)=pause_at(&cap.terminal_publication.before_work);exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();
    let event=h.lifecycle_events().into_iter().find(|e|e["transitionId"]=="LT-12").unwrap();assert_eq!(event["closedGeneration"],json!({"unknownNoResponse":1,"endedUnanswered":1}));
    assert_eq!(h.snapshot()["serverRequests"][0]["state"],"ended-unanswered");
    assert!(h.client_requests().iter().any(|r|r["outcome"]=="unknown-no-response"));
    h.on_eof(&g);go.send(()).unwrap();let got=wait_closed(&h,&cap,&g);assert_eq!(got["evidence"]["lifecycle"]["legacy_event"],event);
}
#[test]
fn lt12_superseded_eof_after_gate_does_not_close_new_source(){
    let (f,h,cap,g)=ready();let (rx,go)=pause_at(&h.before_eof_gate);exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();
    h.stop("synthetic","old EOF held").unwrap();idle(&cap);let next=h.start(&f.cfg,"replacement").unwrap()["generation"].clone();
    let before=h.distribution_evidence(&next);go.send(()).unwrap();
    let end=std::time::Instant::now()+Duration::from_secs(5);loop{if h.inner.0.lock().unwrap().journal.iter().any(|e|e["class"]=="superseded-generation-eof"){break;}assert!(std::time::Instant::now()<end);std::thread::yield_now();}
    assert_eq!(h.snapshot()["state"],"ready");assert_eq!(h.distribution_evidence(&next),before);assert!(!h.lifecycle_events().iter().any(|e|e["transitionId"]=="LT-12"));
    h.stop("synthetic","done").unwrap();idle(&cap);
}
#[test]
fn lt12_selected_source_or_predecessor_tamper_refuses(){
    for source in [false,true] {
        let f=fixture();let h=Arc::new(Host::new());attach_selected_store(&h,&f,Some("reference/expected.json"));let cap=h.app_runtime_custody().unwrap();let g=h.start(&f.cfg,"selected tamper").unwrap()["generation"].clone();
        let prior=serde_json::to_value(&h.inner.0.lock().unwrap().successor_lt09_reference).unwrap();
        let (rx,go)=pause_at(&cap.terminal_publication.before_work);exit(&h,&g);rx.recv_timeout(Duration::from_secs(10)).unwrap();
        let path=if source {f.root.join("reference-source/reference/expected.json")}else{f.root.join("app-data/runtime/distribution").join(prior["publication"].as_str().unwrap()).join(".chirality-s1/observed.json")};
        assert!(path.exists(),"{}",path.display());std::fs::write(path,b"{}").unwrap();go.send(()).unwrap();assert_eq!(wait_closed(&h,&cap,&g)["state"],"unavailable");
    }
}
