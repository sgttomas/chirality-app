use super::*;
#[test]
fn stop_admission_original_d2_probe_release_cannot_resurrect_either_route(){
    for successor in [false,true] {for failure in [false,true] {
        let mut f=Fixture::new("open(os.environ['CODEX_HOME']+'/entered','w').close()\n while not os.path.exists(os.environ['CODEX_HOME']+'/release'): time.sleep(0.005)");
        f.cfg.wait_limit=Duration::from_secs(12);if !successor{f.cfg.distribution=None;}
        if failure {let path=f.root.join("vendor/bin/codex");let s=std::fs::read_to_string(&path).unwrap().replace(" print('codex-cli 0.160.0'); sys.exit(0)"," sys.exit(7)");std::fs::write(path,s).unwrap();}
        let h=Arc::new(Host::new());let source=h.clone();let cfg=f.cfg.clone();let start=std::thread::spawn(move||source.start(&cfg,"blocked probe"));
        let end=std::time::Instant::now()+Duration::from_secs(5);while !f.root.join("probe/entered").exists(){assert!(std::time::Instant::now()<end);std::thread::sleep(Duration::from_millis(5));}
        assert_eq!(h.state(),"verifying");assert!(h.child_pid().is_none());
        let begin=std::time::Instant::now();assert_eq!(h.stop("synthetic","cancel before release").unwrap()["state"],"stopped");assert!(begin.elapsed()<Duration::from_secs(1));
        let events=h.lifecycle_events();let lt20=events.last().unwrap();assert_eq!(lt20["transitionId"],"LT-20");assert_eq!(lt20["actor"],"synthetic");assert_eq!(lt20["stopRecord"]["reason"],"cancel before release");
        for k in ["exitFacts","closedGeneration","descendants"]{assert!(lt20.get(k).is_none());}
        let before=h.snapshot();std::fs::write(f.root.join("probe/release"),b"release").unwrap();assert!(start.join().unwrap().is_err());
        assert_eq!(h.state(),"stopped");assert!(h.child_pid().is_none());assert_eq!(h.lifecycle_events(),events);assert_eq!(h.snapshot(),before);
    }}
}
fn route(successor:bool)->Fixture{let mut f=Fixture::new("pass");if !successor{f.cfg.distribution=None;}f}
#[test]
fn stop_admission_cancel_before_final_gate_and_newer_attempt(){
    for successor in [false,true] {for newer in [false,true]{
        let f=route(successor);let h=Arc::new(Host::new());let(rx,go)=pause_at(&h.before_successor_gate);let source=h.clone();let cfg=f.cfg.clone();let start=std::thread::spawn(move||source.start(&cfg,"old admission"));
        rx.recv_timeout(Duration::from_secs(5)).unwrap();h.stop("synthetic","cancel").unwrap();
        if newer{h.start(&f.cfg,"new attempt").unwrap();}
        let before=h.snapshot();let events=h.lifecycle_events();go.send(()).unwrap();assert!(start.join().unwrap().is_err());assert_eq!(h.snapshot(),before);assert_eq!(h.lifecycle_events(),events);
        if newer{h.stop("synthetic","cleanup").unwrap();}
    }}
}
#[test]
fn stop_admission_check_through_spawn_blocks_stop_until_custody_published(){
    for successor in [false,true]{
        let f=route(successor);let h=Arc::new(Host::new());let(rx,go)=pause_at(&h.after_successor_check);let(published,resume)=pause_at(&h.after_successor_publish);
        let source=h.clone();let cfg=f.cfg.clone();let start=std::thread::spawn(move||source.start(&cfg,"admission wins"));rx.recv_timeout(Duration::from_secs(5)).unwrap();
        let(source,tx)=(h.clone(),std::sync::mpsc::channel());let stop=std::thread::spawn(move||{let result=source.stop("synthetic","gate race");tx.0.send(result).unwrap();});
        assert!(tx.1.recv_timeout(Duration::from_millis(100)).is_err());go.send(()).unwrap();
        published.recv_timeout(Duration::from_secs(5)).unwrap();
        tx.1.recv_timeout(Duration::from_secs(6)).unwrap().unwrap();resume.send(()).unwrap();
        let _=start.join().unwrap();stop.join().unwrap();assert_eq!(h.state(),"stopped");assert!(h.child.lock().unwrap().as_mut().unwrap().try_wait().unwrap().is_some());
    }
}
#[test]
fn stop_admission_late_handshake_success_error_and_contradiction_never_mutate_new_source(){
    for successor in [false,true]{for outcome in 0..3{
        let f=route(successor);let h=Arc::new(Host::new());let(rx,go)=pause_at(&h.before_successor_settlement);let source=h.clone();let cfg=f.cfg.clone();let start=std::thread::spawn(move||source.start(&cfg,"old handshake"));rx.recv_timeout(Duration::from_secs(5)).unwrap();
        let old=h.snapshot()["generation"].clone();let attempt=h.inner.0.lock().unwrap().start_attempt;h.stop("synthetic","before settlement").unwrap();let stopped=h.snapshot();go.send(()).unwrap();assert!(start.join().unwrap().is_err());assert_eq!(h.snapshot(),stopped);
        h.start(&f.cfg,"replacement").unwrap();let before=h.snapshot();let response=match outcome{0=>Ok(json!({"result":{"userAgent":"codex/0.160.0"}})),1=>Err("late error".into()),_=>Ok(json!({"result":{"userAgent":"codex/9.0.0"}}))};
        assert!(h.finish_start_handshake(&old,attempt,json!({}),response,successor).is_err());assert_eq!(h.snapshot(),before);h.stop("synthetic","cleanup").unwrap();
    }}
}
#[test]
fn stop_admission_lt20_preserves_historical_pid_pipe_and_rec_cause(){
    for successor in [false,true]{
        let f=route(successor);let h=Arc::new(Host::new());let old=h.start(&f.cfg,"prior source").unwrap()["generation"].clone();h.inner.0.lock().unwrap().execution_custody.bind(&old,"diagnostic-thread",&json!({"home":"synthetic-account"}));h.on_line(&serde_json::to_vec(&json!({"method":"turn/started","params":{"threadId":"diagnostic-thread","turn":{"id":"diagnostic-turn","status":"inProgress","items":[]}}})).unwrap(),&old);h.stop("prior actor","prior source stop").unwrap();
        let(rx,go)=pause_at(&h.before_successor_gate);let source=h.clone();let cfg=f.cfg.clone();let start=std::thread::spawn(move||source.start(&cfg,"cancel new attempt"));rx.recv_timeout(Duration::from_secs(5)).unwrap();
        let before={let i=h.inner.0.lock().unwrap();json!({"generation":i.generation,"pid":i.child_pid,"stopRecord":i.stop_record,"journal":i.journal,"requests":i.server_requests.entries(),"execution":i.execution_custody.snapshot(),"pending":i.pending_recovery.facts.lock().unwrap().iter().cloned().collect::<Vec<_>>()})};
        // This hook is before stdin close, group probes/signals, EOF wait and closure.
        // If the LT20 branch falls through, panic before any historical process action.
        *h.before_stop_cleanup.lock().unwrap()=Some(Box::new(||panic!("LT20 entered historical cleanup")));
        h.stop("new actor","cancel current verification").unwrap();assert!(h.before_stop_cleanup.lock().unwrap().is_some());h.before_stop_cleanup.lock().unwrap().take();
        assert!(before["execution"].to_string().contains("supplier-stop"),"first loss cause must actually be observed");
        let after={let i=h.inner.0.lock().unwrap();json!({"generation":i.generation,"pid":i.child_pid,"stopRecord":i.stop_record,"journal":i.journal,"requests":i.server_requests.entries(),"execution":i.execution_custody.snapshot(),"pending":i.pending_recovery.facts.lock().unwrap().iter().cloned().collect::<Vec<_>>()})};assert_eq!(after,before);
        h.on_eof(&old);let i=h.inner.0.lock().unwrap();assert_eq!(i.stop_record,before["stopRecord"].as_object().map(|_|before["stopRecord"].clone()));assert_eq!(i.execution_custody.snapshot(),before["execution"]);drop(i);
        go.send(()).unwrap();assert!(start.join().unwrap().is_err());
    }
}
#[test]
fn stop_admission_inconsistent_marker_and_counter_exhaustion_refuse_before_mutation(){
    for mode in 0..3{
        let h=Host::new();{let mut i=h.inner.0.lock().unwrap();i.state="verifying".into();i.start_attempt=if mode==2{u64::MAX}else{4};i.start_admission=match mode{0=>None,1=>Some(crate::hosting::StartAdmission::Installed{attempt:4,generation:json!({"historical":true})}),_=>Some(crate::hosting::StartAdmission::NotSpawned(u64::MAX))};}
        let before=h.snapshot();assert!(h.stop("synthetic","invalid").is_err());assert_eq!(h.snapshot(),before);assert!(h.lifecycle_events().is_empty());
    }
    let f=route(false);let h=Arc::new(Host::new());h.inner.0.lock().unwrap().start_attempt=u64::MAX;let before=h.snapshot();assert!(h.start(&f.cfg,"overflow").is_err());assert_eq!(h.snapshot(),before);assert!(h.lifecycle_events().is_empty());
}
