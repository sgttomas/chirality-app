//! Actual Tauri resource mapping for the compiled reference; no supplier/App execution.
use chirality_app_v4_lib::{distribution_preflight::digest, util};
use serde_json::Value;
use std::{collections::{BTreeSet, HashMap}, fs, path::{Path, PathBuf}};
use tauri::utils::resources::ResourcePaths;

struct Staging(PathBuf);
impl Staging {
    fn new() -> Self {
        let path=std::env::temp_dir().canonicalize().unwrap().join(util::opaque_id("attested-map-").unwrap());
        fs::create_dir(&path).unwrap(); Self(path)
    }
}
impl Drop for Staging { fn drop(&mut self) { let _=fs::remove_dir_all(&self.0); } }

fn value(path: &Path) -> Value { serde_json::from_slice(&fs::read(path).unwrap()).unwrap() }
fn reference(root: &Path, r: &Value, paths: &mut BTreeSet<String>) -> Value {
    let path=r["path"].as_str().unwrap();
    assert!(!Path::new(path).is_absolute() && !Path::new(path).components().any(|c|c==std::path::Component::ParentDir));
    let raw=fs::read(root.join(path)).unwrap(); assert_eq!(digest(&raw),r["sha256"]);
    paths.insert(path.to_owned()); serde_json::from_slice(&raw).unwrap_or(Value::Null)
}
fn closure(root: &Path) -> BTreeSet<String> {
    let raw=fs::read(root.join("build-selection.s2.json")).unwrap();
    assert_eq!(digest(&raw),"49df30f500af353c5cc141bf939515a21ab9438c92d2fd61ed435c831bcd0fea");
    let selection:Value=serde_json::from_slice(&raw).unwrap();
    let mut paths=BTreeSet::from(["build-selection.s2.json".to_owned()]);
    let e=reference(root,&selection["expected"],&mut paths);let a=reference(root,&selection["attestation"],&mut paths);
    assert_eq!(a["expected_reference"],selection["expected"]);
    for r in [&e["label_evidence"],&e["generation_correspondence"],&e["generated"]["provenance"],&e["generated"]["version_advance"],
        &e["archive"]["acquisition_authorization"],&e["archive"]["custody"],&e["archive"]["extraction_procedure"],
        &a["review_evidence"],&a["adoption"]["through_help_human"],&a["adoption"]["evidence"]] {reference(root,r,&mut paths);}
    paths
}

#[test]
fn tauri_maps_the_exact_compiled_reference_closure_into_its_native_resource_namespace() {
    let rust=Path::new(env!("CARGO_MANIFEST_DIR"));let config=rust.join("../packaging/unsigned");
    let ordinary=value(&config.join("tauri.development.conf.json"));
    let overlay=value(&config.join("tauri.attested-reference.conf.json"));
    let source=rust.join("resources/distribution-reference");let paths=closure(&source);
    let mut expected=ordinary.clone();
    for path in &paths {expected["bundle"]["resources"][format!("resources/distribution-reference/{path}")]=Value::String(format!("distribution-reference/{path}"));}
    assert_eq!(overlay,expected,"base identity, signing and workflow/role mappings remain part of the explicit route");
    let mappings:HashMap<String,String>=overlay["bundle"]["resources"].as_object().unwrap().iter()
        .filter(|(_,v)|v.as_str().unwrap().starts_with("distribution-reference/"))
        .map(|(s,d)|(rust.join(s).to_str().unwrap().to_owned(),d.as_str().unwrap().to_owned())).collect();
    let staging=Staging::new();let mut targets=BTreeSet::new();
    for resource in ResourcePaths::from_map(&mappings,false).iter() {
        let resource=resource.unwrap();assert!(targets.insert(resource.target().to_path_buf()),"duplicate resource target");
        let dest=staging.0.join(resource.target());fs::create_dir_all(dest.parent().unwrap()).unwrap();fs::copy(resource.path(),&dest).unwrap();
        assert_eq!(fs::read(&dest).unwrap(),fs::read(resource.path()).unwrap());
    }
    assert_eq!(targets,paths.iter().map(|p|PathBuf::from("distribution-reference").join(p)).collect());
    assert_eq!(closure(&staging.0.join("distribution-reference")),paths,"the actual SDK targets preserve every digest-bound edge");
    assert_eq!(paths.len(),12);
    let default=value(&rust.join("tauri.conf.json"));
    assert!(default["bundle"]["resources"].as_object().unwrap().values().all(|v|!v.as_str().unwrap().starts_with("distribution-reference/")),"default route remains separately selected");
}
