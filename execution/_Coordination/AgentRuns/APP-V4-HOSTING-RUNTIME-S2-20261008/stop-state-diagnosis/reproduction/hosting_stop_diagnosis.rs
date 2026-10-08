use super::*;
#[test]
fn stop_diagnosis_seeded_no_child_state_matrix(){
    let table:Value=serde_json::from_str(include_str!("../resources/distribution-successor/lifecycle-transitions.s1.json")).unwrap();
    for state in ["absent","refused","stopped","stopping","ready","handshaking","spawning","verifying","restart-waiting","halted-after-repeated-failure","exited-unexpectedly"] {
        let h=Host::new();{let mut i=h.inner.0.lock().unwrap();i.state=state.into();assert!(i.child_pid.is_none());}
        let begin=std::time::Instant::now();let result=h.stop("synthetic diagnostic","seeded state, no child");let elapsed=begin.elapsed().as_millis();
        let i=h.inner.0.lock().unwrap();let rows:Vec<Value>=i.lifecycle.iter().map(|e|json!({"actual":e,"declaredTuple":table[e["transitionId"].as_str().unwrap()],"tupleMatches":table[e["transitionId"].as_str().unwrap()]==json!([e["fromState"],e["event"],e["toState"]])})).collect();
        println!("STOP_DIAG {}",json!({"kind":"seeded-no-child-not-reachability-proof","entry":state,"result":result,"elapsedMs":elapsed,"generation":i.generation,"pid":i.child_pid,"rows":rows,"journal":i.journal,"serverRequests":i.server_requests.entries()}));
    }
}
#[test]
fn stop_diagnosis_actual_invented_child_eof_and_stop_orderings(){
    for eof_first in [false,true] {
        let f=Fixture::new("pass");let path=f.root.join("vendor/bin/codex");let code=std::fs::read_to_string(&path).unwrap().replace(" f=json.loads(line)"," f=json.loads(line)\n if f.get('method')=='fixture/exit': sys.exit(7)");let code=code.replace(" if 'id' in f:"," if f.get('method')=='fixture/request':\n  print(json.dumps({'id':'supplier-request','method':'item/fileChange/requestApproval','params':{'threadId':'t','itemId':'i'}}),flush=True)\n if f.get('method')=='fixture/unanswered': continue\n if 'id' in f:");std::fs::write(path,code).unwrap();
        let h=Arc::new(Host::new());let g=h.start(&f.cfg,"synthetic diagnosis").unwrap()["generation"].clone();
        h.write_frame_scoped(&json!({"jsonrpc":"2.0","method":"fixture/request"}),Some(&g)).unwrap();
        let end=std::time::Instant::now()+Duration::from_secs(5);while h.snapshot()["serverRequests"].as_array().unwrap().is_empty(){assert!(std::time::Instant::now()<end);std::thread::sleep(Duration::from_millis(5));}
        let _pending=h.request_begin_scoped("fixture/unanswered",json!({}),json!({"kind":"person-directed"}),false,Some(&g)).unwrap();
        if eof_first {h.write_frame_scoped(&json!({"jsonrpc":"2.0","method":"fixture/exit"}),Some(&g)).unwrap();let end=std::time::Instant::now()+Duration::from_secs(5);while h.state()!="exited-unexpectedly"{assert!(std::time::Instant::now()<end);std::thread::sleep(Duration::from_millis(5));}}
        let before={let i=h.inner.0.lock().unwrap();json!({"state":i.state,"events":i.lifecycle,"journal":i.journal})};
        let begin=std::time::Instant::now();let result=h.stop("synthetic diagnostic","order control");let elapsed=begin.elapsed().as_millis();let i=h.inner.0.lock().unwrap();
        println!("STOP_DIAG {}",json!({"kind":"actual-invented-child","eofFirst":eof_first,"generation":g,"before":before,"result":result,"elapsedMs":elapsed,"afterEvents":i.lifecycle,"afterJournal":i.journal,"clientRequests":i.client_requests,"serverRequests":i.server_requests.entries()}));
        assert_eq!(i.state,"stopped");
    }
}
#[test]
fn stop_diagnosis_actual_verify_gate_legacy_and_successor(){
    for successor in [false,true] {
        let mut f=Fixture::new("open(os.environ['CODEX_HOME']+'/entered','w').close()\n while not os.path.exists(os.environ['CODEX_HOME']+'/release'): time.sleep(0.005)");
        f.cfg.wait_limit=Duration::from_secs(12);if !successor{f.cfg.distribution=None;}
        let h=Arc::new(Host::new());let source=h.clone();let cfg=f.cfg.clone();let start=std::thread::spawn(move||source.start(&cfg,"diagnostic blocked probe"));
        let end=std::time::Instant::now()+Duration::from_secs(5);while !f.root.join("probe/entered").exists(){assert!(std::time::Instant::now()<end);std::thread::sleep(Duration::from_millis(5));}
        assert_eq!(h.state(),"verifying");assert!(h.child_pid().is_none());
        let begin=std::time::Instant::now();let stopped=h.stop("synthetic diagnostic","during version probe");let elapsed=begin.elapsed().as_millis();let at_stop=h.snapshot();
        std::fs::write(f.root.join("probe/release"),b"release").unwrap();let resumed=start.join().unwrap();
        println!("STOP_DIAG {}",json!({"kind":"actual-blocked-version-probe","successor":successor,"stopResult":stopped,"elapsedMs":elapsed,"atStop":at_stop,"startResult":resumed,"afterState":h.state(),"afterPidPresent":h.child_pid().is_some(),"events":h.lifecycle_events()}));
        if h.state()=="ready"{h.stop("synthetic diagnostic","cleanup late launch").unwrap();}
    }
}
