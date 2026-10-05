
fn planned_probe_fixture(root:&std::path::Path)->(ExistingHomeReference,OwnedHomePlan,PathBuf){
    let(account,_,_)=refs(root);let app=root.join("app");
    let probe=OwnedHomePlan::new(app.clone(),app.join("probe"),HomeClass::Probe,None).unwrap();
    probe.prepare().unwrap();(account,probe,app)
}
fn planned_probe_binding(account:&ExistingHomeReference,probe:&OwnedHomePlan)->Result<Arc<NativeNamespaceBindings>,String>{
    NativeNamespaceBindings::from_root(vec![NativeHomeNamespace::received(account,None),NativeHomeNamespace::planned(probe)])
}
fn direct_probe_entries(probe:&OwnedHomePlan){
    std::fs::write(probe.native_path().join("config.toml"),"synthetic probe config").unwrap();
    std::fs::write(probe.native_path().join("AGENTS.md"),"synthetic probe guidance").unwrap();
    std::fs::create_dir(probe.native_path().join("skills")).unwrap();
}
#[test]
fn namespace_planned_probe_direct_entries_before_binding_remain_usable(){
    let root=scratch();let(account,probe,app)=planned_probe_fixture(&root);direct_probe_entries(&probe);
    let result=planned_probe_binding(&account,&probe);let error=result.as_ref().err().cloned();
    if result.is_err(){std::fs::remove_dir_all(&root).unwrap();}
    let scope=result.unwrap_or_else(|_|panic!("safe direct planned Probe must bind: {:?}",error));
    let owner=AttachmentCustody::open_with_namespaces(&app,Arc::clone(&scope)).unwrap();
    let mut ledger=RecoveryLedger::open_with_namespaces(app.join("recovery.ledger.jsonl"),scope).unwrap();
    ledger.append(started()).unwrap();
    assert!(owner.supplies_path("submission:00000000-0000-4000-8000-000000000001").is_ok());
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn namespace_planned_probe_direct_entries_after_binding_remain_usable(){
    let root=scratch();let(account,probe,app)=planned_probe_fixture(&root);
    let scope=planned_probe_binding(&account,&probe).unwrap();
    let owner=AttachmentCustody::open_with_namespaces(&app,Arc::clone(&scope)).unwrap();
    let leaf=app.join("recovery.ledger.jsonl");let mut ledger=RecoveryLedger::open_with_namespaces(leaf.clone(),scope).unwrap();
    ledger.append(started()).unwrap();let before=std::fs::read(&leaf).unwrap();direct_probe_entries(&probe);
    assert!(owner.supplies_path("submission:00000000-0000-4000-8000-000000000001").is_ok());
    ledger.append(json!({"kind":"session_ended","session":"synthetic-session","at":"now","how":"quit","stopRequests":[]})).unwrap();
    assert!(std::fs::read(&leaf).unwrap().len()>before.len());std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn namespace_planned_probe_foreign_unresolved_and_wrong_types_refuse(){
    use std::os::unix::fs::symlink;
    for (name,directory) in [("config.toml",false),("AGENTS.md",false),("skills",true)]{
        for kind in ["foreign","unresolved","wrong-type"]{
            let root=scratch();let(account,probe,app)=planned_probe_fixture(&root);
            let scope=planned_probe_binding(&account,&probe).unwrap();
            let owner=AttachmentCustody::open_with_namespaces(&app,Arc::clone(&scope)).unwrap();
            let leaf=app.join("recovery.ledger.jsonl");let mut ledger=RecoveryLedger::open_with_namespaces(leaf.clone(),scope).unwrap();
            ledger.append(started()).unwrap();let before=std::fs::read(&leaf).unwrap();let slot=probe.native_path().join(name);
            match kind{
                "foreign"=>symlink(root.join(if directory{"shared/skills"}else if name=="config.toml"{"shared/config.toml"}else{"shared/AGENTS.md"}),&slot).unwrap(),
                "unresolved"=>symlink(root.join("missing-resource"),&slot).unwrap(),
                _=>if directory{std::fs::write(&slot,"wrong type").unwrap()}else{std::fs::create_dir(&slot).unwrap()},
            }
            assert!(planned_probe_binding(&account,&probe).is_err(),"{name} {kind}");
            assert!(owner.supplies_path("submission:00000000-0000-4000-8000-000000000001").is_err(),"{name} {kind}");
            assert!(ledger.append(json!({"kind":"session_ended","session":"synthetic-session","at":"now","how":"quit","stopRequests":[]})).is_err(),"{name} {kind}");
            assert_eq!(std::fs::read(&leaf).unwrap(),before);std::fs::remove_dir_all(root).unwrap();
        }
    }
}
