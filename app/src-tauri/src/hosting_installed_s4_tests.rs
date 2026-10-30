// Synthetic source fixtures only. No supplier, model, signing or native App execution.
use super::*;
use crate::distribution_s1::{self, Files};
fn setup() -> (Fixture, PathBuf, Selected, Value) {
    let mut f=Fixture::new("raise Exception('must never execute')");
    let resources=f.root.join("Invented.app/Contents/Resources");
    std::fs::create_dir_all(&resources).unwrap();
    std::fs::rename(f.root.join("vendor"),resources.join("codex")).unwrap();
    std::fs::write(resources.join("noncodex.txt"),b"sealed fixture resource").unwrap();
    f.cfg.distribution=Some(Distribution::Production{resources:resources.clone()});
    let source=f.root.join("reference-source");
    let inv=serde_json::to_value(tree::scan(&resources.join("codex")).unwrap()).unwrap();
    let anchor=tree::selection::fixture_files(&source,&inv,"reference/expected.json");
    let selected=Selected::fixture(&source,anchor).unwrap();
    let g=json!({"appSession":"synthetic-s4","home":format!("app-home:{}",tree::digest(f.cfg.codex_home.as_os_str().as_encoded_bytes())),"spawnCounter":1});
    (f,resources,selected,g)
}
fn prepared(f:&Fixture,r:&Path,s:&Selected,g:&Value)->Prepared{
    prepare_installed(r,&f.cfg,g,Reference::Selected(s),|_,_|Ok("codex-cli 0.160.0\n".into()),crate::installed_custody::synthetic_for_tests).unwrap()
}
fn evidence(p:&Prepared,f:&Fixture,s:&Selected,g:&Value)->(Value,Files){
    let(mut o,facts)=p.observation(&f.cfg,g);
    o["expected_reference"]=serde_json::to_value(s.expected_ref()).unwrap();
    o["adoption_attestation"]=serde_json::to_value(s.attestation_ref()).unwrap();
    let mut files=s.files().clone();
    let raw=serde_json::to_vec(&facts).unwrap();
    let reference=json!({"path":"facts.json","sha256":tree::digest(&raw)});
    files.insert("facts.json".into(),raw);
    for c in o["checks"].as_object_mut().unwrap().values_mut(){c["evidence"]=reference.clone();}
    let app=p.installed.as_ref().unwrap().evidence();
    let record=json!({"format":"installed-custody-observation.s4","generation":g,"inventory":o["inventory"],"selection":s.association(),"app":app,"standing":"process-observation-evidence-only","limits":["No live authority from serialized evidence", "No package, installer, quarantine or notarization qualification"]});
    install(&mut o,&mut files,&record);
    (o,files)
}
fn install(o:&mut Value,files:&mut Files,record:&Value){let raw=serde_json::to_vec(record).unwrap();o["checks"]["custody"]["evidence"]=json!({"path":"installed.json","sha256":tree::digest(&raw)});files.insert("installed.json".into(),raw);}
#[test]
fn installed_s4_synthetic_verified_and_lt04_are_evidence_not_legacy_authority(){
    let(f,r,s,g)=setup();let p=prepared(&f,&r,&s,&g);let(o,mut files)=evidence(&p,&f,&s,&g);
    assert_eq!(distribution_s1::observed(&o,&files,Some(&s)).unwrap(),"verified");
    assert!(distribution_s1::observed_s3(&o,&files,Some(&s)).is_err());
    let raw=serde_json::to_vec(&o).unwrap();let reference=json!({"path":"observed.json","sha256":tree::digest(&raw)});files.insert("observed.json".into(),raw);
    let mut l=json!({"format":"lifecycle-event.s4","verification_artifact":reference,"verification_generation":g,"legacy_event":{"recordKind":"lifecycle-event","sequence":2,"transitionId":"LT-04","generation":g,"fromState":"verifying","event":"verification-passed","toState":"spawning","at":"synthetic","supplierStanding":"verified-pin","verificationResult":{"result":"verified"}}});
    assert_eq!(distribution_s1::lifecycle(&l,&files,Some(&s)).unwrap(),"verified");
    l["format"]=json!("lifecycle-event.s1.v0.10");assert!(distribution_s1::lifecycle(&l,&files,Some(&s)).is_err());
}
#[test]
fn installed_s4_rejects_opaque_null_unknown_and_mismatched_exact_joins(){
    let(f,r,s,g)=setup();let p=prepared(&f,&r,&s,&g);let(o,files)=evidence(&p,&f,&s,&g);
    let original:Value=serde_json::from_slice(&files["installed.json"]).unwrap();
    for (pointer,value) in [("/format",json!("future")),("/generation/spawnCounter",json!(2)),("/inventory/manifest_sha256",json!("0".repeat(64))),("/selection/compiledAnchor/sha256",json!("0".repeat(64))),("/app/dynamic/cdhash",json!("0".repeat(40))),("/app/requirement_sha256",json!("0".repeat(64))),("/app/standing",json!("installed-observation")),("/app/static/signature_flags",json!(2)),("/standing",json!("live-authority"))]{
        let(mut o,mut files,mut record)=(o.clone(),files.clone(),original.clone());*record.pointer_mut(pointer).unwrap()=value;install(&mut o,&mut files,&record);assert!(distribution_s1::observed(&o,&files,Some(&s)).is_err(),"{pointer}");
    }
    for record in [Value::Null,json!("opaque"),json!({})]{let(mut o,mut files)=(o.clone(),files.clone());install(&mut o,&mut files,&record);assert!(distribution_s1::observed(&o,&files,Some(&s)).is_err());}
    let mut altered=files.clone();altered.insert("installed.json".into(),serde_json::to_vec_pretty(&original).unwrap());assert!(distribution_s1::observed(&o,&altered,Some(&s)).is_err());
}
#[test]
fn installed_s4_noncodex_mutation_and_probe_mutation_refuse(){
    let(f,r,s,g)=setup();let p=prepared(&f,&r,&s,&g);
    std::fs::write(r.join("noncodex.txt"),b"mutated").unwrap();
    assert!(tree::revalidate(&p.root,&p.inventory).is_ok());assert!(p.revalidate().is_err());
    let result=prepare_installed(&r,&f.cfg,&g,Reference::Selected(&s),|_,_|{std::fs::write(r.join("noncodex.txt"),b"again").unwrap();Ok("codex-cli 0.160.0\n".into())},crate::installed_custody::synthetic_for_tests);
    assert!(result.is_err());
}
#[test]
fn installed_s4_none_and_tree_contradiction_refuse_before_probe(){
    let(f,r,s,g)=setup();
    let attempt=||prepare_with_probe(&Distribution::Production{resources:r.clone()},&f.cfg,&g,Reference::Selected(&s),|_,_|panic!("must not execute"));
    assert!(attempt().err().unwrap().contains("publisher requirement"));
    std::fs::write(r.join("codex/bin/codex"),b"contradiction").unwrap();
    assert!(attempt().err().unwrap().starts_with("mismatch:"));
}
#[test]
fn installed_s4_store_needs_typed_observation_and_projects_verified_pin(){
    use crate::hosting::attachment_custody::{NativeHomeNamespace,NativeNamespaceBindings};
    use crate::home_resources::{ExistingHomeReference,HomeClass};
    let(f,r,s,g)=setup();let p=prepared(&f,&r,&s,&g);
    let home=ExistingHomeReference::new(f.cfg.codex_home.clone(),HomeClass::Account).unwrap();
    assert_eq!(g["home"],home.opaque_home_id());
    let probe=ExistingHomeReference::new(f.cfg.probe_home.clone(),HomeClass::Probe).unwrap();
    let bindings=NativeNamespaceBindings::from_root(vec![NativeHomeNamespace::received(&home,None),NativeHomeNamespace::received(&probe,None)]).unwrap();
    let data=f.root.join("app-data");std::fs::create_dir(&data).unwrap();
    let store=crate::distribution_store::Store::open_selected(&data,&r.join("codex"),bindings,s).unwrap();
    let(o,facts)=p.observation(&f.cfg,&g);
    assert!(store.publish_observed(&g,o.clone(),facts.clone()).err().unwrap().contains("typed installed"));
    let reference=store.publish_observed_with_installed(&g,o,facts,p.installed.as_ref()).unwrap();
    let view=store.read_s1(&g,&reference).unwrap();assert_eq!(view["standing"],"verified-pin");
    let mut native=crate::native_items::NativeView::new(g["home"].as_str().unwrap().into()).unwrap();
    native.ready(g.clone(),json!("codex-cli 0.160.0"),view["standing"].clone()).unwrap();
    assert_eq!(native.snapshot()["supplierStanding"],"verified-pin");
    let installed_path=data.join("runtime/distribution").join(view["reference"]["publication"].as_str().unwrap()).join(".chirality-s1/installed.json");
    std::fs::write(installed_path,b"{}").unwrap();assert!(store.read_s1(&g,&reference).is_err());
}
#[test]
fn installed_s4_shared_start_preserves_legacy_and_development_standing(){
    for (verified,successor,expected) in [(true,true,"verified-pin"),(true,false,"verified"),(false,true,"unverified-development"),(false,false,"unverified-development")] {
        let mut native=crate::native_items::NativeView::new("synthetic-home".into()).unwrap();
        native.ready(json!({"appSession":"synthetic","home":"synthetic-home","spawnCounter":1}),json!("codex-cli 0.160.0"),json!(supplier_standing(verified,successor))).unwrap();
        assert_eq!(native.snapshot()["supplierStanding"],expected);
    }
    let(f,r,s,g)=setup();let(p,files)=evidence(&prepared(&f,&r,&s,&g),&f,&s,&g);
    let mut old=p.clone();old["format"]=json!("observed-verification.s1");
    assert!(distribution_s1::observed(&old,&files,Some(&s)).unwrap_err().contains("historical"));
}
