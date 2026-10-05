//! Actual finite Root metadata bindings; no native/auth or resource contents read.
use chirality_app_v4_lib::{home_resources::{ExistingHomeReference,HomeClass,OwnedHomePlan,SharedResourceTargets},hosting::{Host,attachment_custody::{AttachmentCustody,NativeHomeNamespace,NativeNamespaceBindings}},recovery::RecoveryLedger,util};
use serde_json::{json,Value};use std::{path::PathBuf,sync::Arc};
fn scratch()->PathBuf{let p=std::env::temp_dir().join(util::opaque_id("native-namespaces-").unwrap());std::fs::create_dir(&p).unwrap();p.canonicalize().unwrap()}
fn refs(root:&std::path::Path)->(ExistingHomeReference,ExistingHomeReference,SharedResourceTargets){for n in ["account","probe","shared","shared/skills"]{std::fs::create_dir_all(root.join(n)).unwrap();}std::fs::write(root.join("shared/config.toml"),"synthetic configuration").unwrap();std::fs::write(root.join("shared/AGENTS.md"),"synthetic guidance").unwrap();(ExistingHomeReference::new(root.join("account"),HomeClass::Account).unwrap(),ExistingHomeReference::new(root.join("probe"),HomeClass::Probe).unwrap(),SharedResourceTargets{config_toml:root.join("shared/config.toml"),global_agents_md:root.join("shared/AGENTS.md"),skills:root.join("shared/skills")})}
fn binding(account:&ExistingHomeReference,probe:&ExistingHomeReference,key:Option<&OwnedHomePlan>)->Arc<NativeNamespaceBindings>{let mut homes=vec![NativeHomeNamespace::received(account,None),NativeHomeNamespace::received(probe,None)];if let Some(key)=key{homes.push(NativeHomeNamespace::planned(key));}NativeNamespaceBindings::from_root(homes).unwrap()}
fn started()->Value{json!({"kind":"session_started","session":"synthetic-session","at":"2026-10-05T00:00:00Z","previousSessionEnd":"none","candidate":"unqualified-fixture"})}
#[test]
fn namespace_benign_parent_key_preflight_setup_and_separate_rec_nir_use(){let root=scratch();let(account,probe,targets)=refs(&root);let a=root.join("app");let key=OwnedHomePlan::new(a.clone(),a.join("key"),HomeClass::ApiKey,Some(targets)).unwrap();let scope=binding(&account,&probe,Some(&key));std::fs::create_dir_all(a.join("runtime")).unwrap();let path=a.join("runtime/recovery.ledger.jsonl");let host=Host::new();host.configure_recovery_with_namespaces(path.clone(),Arc::clone(&scope)).unwrap();let cap=host.app_runtime_custody().unwrap();cap.preflight_native_namespaces(&scope).unwrap();assert!(!key.native_path().exists());key.prepare().unwrap();cap.bind_native_namespaces(Arc::clone(&scope)).unwrap();let owner=AttachmentCustody::open_with_namespaces(&a,scope).unwrap();assert_eq!(owner.root(),&a);let before=std::fs::read(&path).unwrap();assert!(cap.snapshot()["recovery"]["entries"].as_array().unwrap().len()==1);assert_eq!(std::fs::read(&path).unwrap(),before);std::fs::remove_dir_all(root).unwrap();}
#[test]
fn namespace_bad_prospective_home_preserves_healthy_original_ledger_and_binding(){let root=scratch();let(account,probe,targets)=refs(&root);let a=root.join("app");std::fs::create_dir_all(a.join("runtime")).unwrap();let path=a.join("runtime/recovery.ledger.jsonl");let current=binding(&account,&probe,None);let host=Host::new();host.configure_recovery_with_namespaces(path.clone(),Arc::clone(&current)).unwrap();let cap=host.app_runtime_custody().unwrap();let before=std::fs::read(&path).unwrap();let bad=OwnedHomePlan::new(a.clone(),a.join("runtime"),HomeClass::ApiKey,Some(targets)).unwrap();let proposed=NativeNamespaceBindings::from_root(vec![NativeHomeNamespace::received(&account,None),NativeHomeNamespace::received(&probe,None),NativeHomeNamespace::planned(&bad)]);if let Ok(proposed)=proposed{assert!(cap.preflight_native_namespaces(&proposed).is_err());}assert_eq!(std::fs::read(&path).unwrap(),before);assert!(!bad.native_path().join("config.toml").exists());cap.bind_native_namespaces(current).unwrap();cap.record_app_session_end(&[]).unwrap();assert!(std::fs::read_to_string(&path).unwrap().contains("session_ended"));std::fs::remove_dir_all(root).unwrap();}
#[test]
fn namespace_exact_skills_to_supply_and_config_to_ledger_targets_refuse(){for resource in ["skills","config"]{let root=scratch();let(account,probe,mut targets)=refs(&root);let a=root.join("app");std::fs::create_dir_all(a.join("runtime/nir/attachment-supplies")).unwrap();let leaf=a.join("runtime/recovery.ledger.jsonl");std::fs::write(&leaf,"").unwrap();if resource=="skills"{targets.skills=a.join("runtime/nir/attachment-supplies");}else{targets.config_toml=leaf.clone();}let key=OwnedHomePlan::new(a.clone(),a.join("key"),HomeClass::ApiKey,Some(targets)).unwrap();let scope=binding(&account,&probe,Some(&key));if resource=="skills"{assert!(AttachmentCustody::open_with_namespaces(&a,Arc::clone(&scope)).is_err());}else{assert!(RecoveryLedger::open_with_namespaces(leaf.clone(),Arc::clone(&scope)).is_err());}assert!(!key.native_path().exists());assert!(std::fs::read_to_string(&leaf).unwrap().is_empty());std::fs::remove_dir_all(root).unwrap();}}
#[test]
fn namespace_declared_source_redirect_and_current_link_drift_stop_metadata_only(){use std::os::unix::fs::symlink;let root=scratch();let(account,probe,targets)=refs(&root);let a=root.join("app");let key=OwnedHomePlan::new(a.clone(),a.join("key"),HomeClass::ApiKey,Some(targets.clone())).unwrap();let scope=binding(&account,&probe,Some(&key));key.prepare().unwrap();let owner=AttachmentCustody::open_with_namespaces(&a,Arc::clone(&scope)).unwrap();std::fs::create_dir_all(a.join("runtime")).unwrap();let leaf=a.join("runtime/recovery.ledger.jsonl");let mut ledger=RecoveryLedger::open_with_namespaces(leaf.clone(),scope).unwrap();ledger.append(started()).unwrap();let before=std::fs::read(&leaf).unwrap();std::fs::remove_file(key.native_path().join("skills")).unwrap();symlink(a.join("runtime"),key.native_path().join("skills")).unwrap();assert!(owner.supplies_path("submission:00000000-0000-4000-8000-000000000001").is_err());assert!(ledger.append(json!({"kind":"session_ended","session":"synthetic-session","at":"now","how":"quit","stopRequests":[]})).is_err());assert_eq!(std::fs::read(&leaf).unwrap(),before);assert!(NativeNamespaceBindings::from_root(vec![NativeHomeNamespace::received(&account,None),NativeHomeNamespace::received(&probe,None),NativeHomeNamespace::planned(&key)]).is_err());std::fs::remove_dir_all(root).unwrap();}
#[test]
fn namespace_legacy_absence_direct_slots_and_unknown_foreign_link_are_distinct(){use std::os::unix::fs::symlink;let root=scratch();let(account,probe,_)=refs(&root);let a=root.join("app");let scope=binding(&account,&probe,None);AttachmentCustody::open_with_namespaces(&a,scope).unwrap();std::fs::write(account.native_path().join("config.toml"),"direct native fixture").unwrap();std::fs::create_dir(account.native_path().join("skills")).unwrap();let direct=binding(&account,&probe,None);AttachmentCustody::open_with_namespaces(&a,direct).unwrap();std::fs::remove_dir(account.native_path().join("skills")).unwrap();symlink(root.join("shared/skills"),account.native_path().join("skills")).unwrap();assert!(NativeNamespaceBindings::from_root(vec![NativeHomeNamespace::received(&account,None),NativeHomeNamespace::received(&probe,None)]).is_err());assert!(NativeNamespaceBindings::from_root(vec![]).is_err());std::fs::remove_dir_all(root).unwrap();}
#[test]
fn namespace_rec_regular_single_link_leaf_and_parent_redirection_refuse_without_reads(){use std::os::unix::fs::symlink;let root=scratch();let(account,probe,_)=refs(&root);let scope=binding(&account,&probe,None);let a=root.join("app");std::fs::create_dir(&a).unwrap();let leaf=a.join("recovery.ledger.jsonl");let mut ledger=RecoveryLedger::open_with_namespaces(leaf.clone(),Arc::clone(&scope)).unwrap();ledger.append(started()).unwrap();let before=std::fs::read(&leaf).unwrap();std::fs::hard_link(&leaf,root.join("alias")).unwrap();assert!(ledger.append(json!({"kind":"session_ended","session":"synthetic-session","at":"now","how":"quit","stopRequests":[]})).is_err());assert!(RecoveryLedger::open_with_namespaces(leaf.clone(),Arc::clone(&scope)).is_err());assert_eq!(std::fs::read(&leaf).unwrap(),before);std::fs::remove_file(root.join("alias")).unwrap();std::fs::rename(&a,root.join("saved-app")).unwrap();symlink(root.join("saved-app"),&a).unwrap();assert!(ledger.append(started()).is_err());assert_eq!(std::fs::read(root.join("saved-app/recovery.ledger.jsonl")).unwrap(),before);std::fs::remove_dir_all(root).unwrap();}

#[test]
fn namespace_failed_guard_keeps_actual_declared_leaf_and_advisory_unavailable_after_restoration(){
    use std::os::unix::fs::symlink;
    let root=scratch();let(account,probe,targets)=refs(&root);let a=root.join("app");std::fs::create_dir_all(a.join("runtime")).unwrap();let leaf=a.join("runtime/recovery.ledger.jsonl");let untouched=root.join("native-source");std::fs::write(&untouched,"do not read/append").unwrap();symlink(&untouched,&leaf).unwrap();
    let scope=binding(&account,&probe,None);let host=Host::new();assert!(host.configure_recovery_with_namespaces(leaf.clone(),Arc::clone(&scope)).is_err());let cap=host.app_runtime_custody().unwrap();assert!(!host.shared_recovery_observation()["limit"].is_null());assert!(cap.preflight_native_namespaces(&scope).is_err());assert_eq!(std::fs::read_to_string(&untouched).unwrap(),"do not read/append");
    std::fs::remove_file(&leaf).unwrap();let key=OwnedHomePlan::new(a.clone(),a.join("key"),HomeClass::ApiKey,Some(targets)).unwrap();let proposed=binding(&account,&probe,Some(&key));cap.preflight_native_namespaces(&proposed).unwrap();let observed=cap.bind_native_namespaces(proposed).unwrap();assert_eq!(observed["ledgerUnavailable"],true);assert_eq!(observed["bindingCommitted"],false);assert!(!leaf.exists());assert!(!key.native_path().exists());assert_eq!(host.shared_recovery_observation()["configured"],false);std::fs::remove_dir_all(root).unwrap();
}

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
        for kind in ["foreign","unresolved","overlap","wrong-type"]{
            let root=scratch();let(account,probe,app)=planned_probe_fixture(&root);
            let scope=planned_probe_binding(&account,&probe).unwrap();
            let owner=AttachmentCustody::open_with_namespaces(&app,Arc::clone(&scope)).unwrap();
            let leaf=app.join("recovery.ledger.jsonl");let mut ledger=RecoveryLedger::open_with_namespaces(leaf.clone(),scope).unwrap();
            ledger.append(started()).unwrap();let before=std::fs::read(&leaf).unwrap();let slot=probe.native_path().join(name);
            match kind{
                "foreign"=>symlink(root.join(if directory{"shared/skills"}else if name=="config.toml"{"shared/config.toml"}else{"shared/AGENTS.md"}),&slot).unwrap(),
                "unresolved"=>symlink(root.join("missing-resource"),&slot).unwrap(),
                "overlap"=>symlink(if directory{app.join("runtime")}else{leaf.clone()},&slot).unwrap(),
                _=>if directory{std::fs::write(&slot,"wrong type").unwrap()}else{std::fs::create_dir(&slot).unwrap()},
            }
            assert!(planned_probe_binding(&account,&probe).is_err(),"{name} {kind}");
            assert!(owner.supplies_path("submission:00000000-0000-4000-8000-000000000001").is_err(),"{name} {kind}");
            assert!(ledger.append(json!({"kind":"session_ended","session":"synthetic-session","at":"now","how":"quit","stopRequests":[]})).is_err(),"{name} {kind}");
            assert_eq!(std::fs::read(&leaf).unwrap(),before);std::fs::remove_dir_all(root).unwrap();
        }
    }
}
