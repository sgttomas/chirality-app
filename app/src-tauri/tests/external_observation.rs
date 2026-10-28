#[path = "../src/schema_validation.rs"] mod schema_validation;
#[path = "../src/catalog.rs"] mod catalog;
#[path = "../src/receiving.rs"] mod receiving;
#[path = "../src/external_observation.rs"] mod external_observation;
use external_observation::{ExternalObservation, SelectedPaths};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
struct Files(PathBuf);
impl Files {
    fn new() -> Self {
        static NEXT: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);
        let dir = std::env::temp_dir().join(format!("chirality-external-observation-{}-{}-{}",std::process::id(),std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos(),NEXT.fetch_add(1,std::sync::atomic::Ordering::Relaxed)));
        std::fs::create_dir(&dir).unwrap(); Self(dir)
    }
    fn write(&self, name: &str, bytes: &[u8]) -> PathBuf { let p=self.0.join(name);std::fs::write(&p,bytes).unwrap();p }
    fn selected(&self, read: &[u8], counterpart: Option<&[u8]>) -> SelectedPaths {
        SelectedPaths { catalog:self.write("catalog.json",&fixture("catalog.example-valid.json")), read:self.write("read.json",read), counterpart:counterpart.map(|b|self.write("counterpart.json",b)) }
    }
}
impl Drop for Files { fn drop(&mut self) { std::fs::remove_dir_all(&self.0).unwrap(); } }
fn fixture(name: &str) -> Vec<u8> {std::fs::read(Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/catalog_adapter").join(name)).unwrap()}
fn read_fixture() -> Value {serde_json::from_slice(&fixture("read_result.example-valid.json")).unwrap()}
#[test]
fn selected_files_to_complete_snapshot_keeps_bytes_content_and_missing_comparison() {
    let files=Files::new();let mut read=read_fixture();
    // Invented fixture additions exercise preservation under C RR-1/RR-2;
    // they are not newly observed host outputs or human acts.
    read["views"][0]["diagnostics"]=json!([{"diagnostic_identity":"diagnostic:test","severity":"warning","statement":"source limitation","attachments":[{"attaches_to":"row","reference":"S-2"}]}]);
    let raw=serde_json::to_vec_pretty(&read).unwrap();let paths=files.selected(&raw,None);
    let state=ExternalObservation::load(paths.clone());let view=state.snapshot();
    assert_eq!(view["read"]["assessment"],"received");assert_eq!(view["read"]["originalDocument"],read);
    assert_eq!(state.read_evidence().original_bytes().unwrap(),raw);assert_eq!(state.read_evidence().selected_path(),paths.read);
    assert_eq!(view["reportedCurrency"],read["standing"]["currency"]);assert_eq!(view["currencyMeaning"],"as reported in this observation");
    assert_eq!(view["comparison"],"host_table_not_supplied");assert_eq!(view["hostOrigin"],"unverified");assert_eq!(view["qualification"],"not_established");assert_eq!(view["dispatch"],"none");
    assert_eq!(std::fs::read_dir(&files.0).unwrap().count(),2); // no output/copy created
    std::fs::write(&paths.read,b"{}").unwrap();assert_eq!(state.read_evidence().original_bytes().unwrap(),raw);assert_eq!(state.snapshot(),view);
}
#[test]
fn supplied_counterpart_comparison_preserves_both_original_documents() {
    let files=Files::new();let raw=fixture("read_result.example-valid.json");let mut counterpart=read_fixture();counterpart["surface"]="H".into();
    let host=serde_json::to_vec(&counterpart).unwrap();let state=ExternalObservation::load(files.selected(&raw,Some(&host)));
    assert_eq!(state.snapshot()["comparison"],"same_meaningful_supplied_content");assert_eq!(state.counterpart_evidence().unwrap().original_bytes().unwrap(),host);
    counterpart["standing"]["known_limitations"]=json!(["separate supplied limitation"]);let host=serde_json::to_vec(&counterpart).unwrap();
    let state=ExternalObservation::load(files.selected(&raw,Some(&host)));
    assert_eq!(state.snapshot()["comparison"],"different_meaningful_supplied_content");assert_eq!(state.snapshot()["counterpart"]["originalDocument"],counterpart);
}
#[test]
fn malformed_invalid_and_unavailable_are_retained_without_upgrading() {
    let files=Files::new();
    for raw in [b"{".to_vec(), vec![0xff,0x00],b"{}".to_vec()] {
        let state=ExternalObservation::load(files.selected(&raw,None));assert!(state.bound_read().is_none());assert_eq!(state.read_evidence().original_bytes().unwrap(),raw);
        assert!(state.read_evidence().reason().is_some());assert!(state.snapshot()["reportedCurrency"].is_null());assert!(state.snapshot()["basisCitationAssessment"].is_null());
    }
    let mut read=read_fixture();read["operation"]["operation_version"]="undiscovered-version".into();let raw=serde_json::to_vec(&read).unwrap();
    let state=ExternalObservation::load(files.selected(&raw,None));assert_eq!(state.read_evidence().assessment(),"invalid");assert_eq!(state.read_evidence().original_document(),Some(&read));assert!(state.read_evidence().reason().unwrap().contains("undiscovered"));
    let mut paths=files.selected(&fixture("read_result.example-valid.json"),None);paths.read=files.0.join("missing.json");let state=ExternalObservation::load(paths);
    assert_eq!(state.read_evidence().assessment(),"unavailable");assert!(state.read_evidence().original_bytes().is_none());assert!(state.bound_read().is_none());
}
#[test]
fn invalid_catalog_and_counterpart_do_not_turn_claims_into_received_reads() {
    let files=Files::new();let raw=fixture("read_result.example-valid.json");let paths=files.selected(&raw,Some(b"{}"));
    let state=ExternalObservation::load(paths.clone());assert!(state.bound_read().is_some());assert_eq!(state.snapshot()["comparison"],"comparison_not_established_counterpart");
    assert_eq!(state.counterpart_evidence().unwrap().original_bytes().unwrap(),b"{}");
    std::fs::write(&paths.catalog,b"{}").unwrap();let state=ExternalObservation::load(paths);
    assert_eq!(state.catalog_evidence().assessment(),"invalid");assert_eq!(state.read_evidence().assessment(),"prerequisite_unavailable");assert_eq!(state.read_evidence().original_bytes().unwrap(),raw);assert!(state.bound_read().is_none());
}
#[test]
fn unavailable_host_result_is_a_retained_non_success_observation() {
    let files=Files::new();let raw=fixture("read_result.example-valid-2.json");let state=ExternalObservation::load(files.selected(&raw,None));
    assert_eq!(state.read_evidence().assessment(),"received");assert_eq!(state.snapshot()["read"]["originalDocument"]["outcome"],"unavailable");assert!(state.bound_read().is_none());assert!(state.snapshot()["reportedCurrency"].is_null());assert_eq!(state.read_evidence().original_bytes().unwrap(),raw);
}
#[test]
fn incomplete_or_missing_lineage_is_visible_and_never_identity_verification() {
    let files=Files::new();let mut read=read_fixture();read["basis"]["model_revision"]=json!({"not_supplied":"omitted"});let raw=serde_json::to_vec(&read).unwrap();
    let state=ExternalObservation::load(files.selected(&raw,None));assert_eq!(state.snapshot()["basisCitationAssessment"],"incomplete");assert_eq!(state.snapshot()["hostOrigin"],"unverified");
    let raw=fixture("read_result.example-valid-3.json");let paths=files.selected(&raw,None);let mut cat:Value=serde_json::from_slice(&fixture("catalog.example-valid.json")).unwrap();cat["basis_profile"]["workspace_identity"]="not_supplied".into();cat["basis_profile"]["generation"]="not_supplied".into();std::fs::write(&paths.catalog,serde_json::to_vec(&cat).unwrap()).unwrap();
    let state=ExternalObservation::load(paths);assert_eq!(state.snapshot()["evidenceLimits"],json!(["basis_lineage_not_supplied"]));assert_eq!(state.snapshot()["hostOrigin"],"unverified");
}
#[cfg(unix)]
#[test]
fn non_utf8_unavailable_selected_path_preserves_native_identity_without_snapshot_panic() {
    use std::os::unix::ffi::{OsStrExt, OsStringExt};
    let files=Files::new();let mut paths=files.selected(&fixture("read_result.example-valid.json"),None);
    // Exact independently reproduced filename: read-[ff].json. It is not
    // created and no real native selector witness is claimed by this test.
    paths.read=files.0.join(std::ffi::OsString::from_vec(b"read-\xff.json".to_vec()));
    let selected=paths.read.clone();let expected=selected.as_os_str().as_bytes().to_vec();
    let state=ExternalObservation::load(paths);assert_eq!(state.read_evidence().selected_path().as_os_str().as_bytes(),expected);
    let snapshot=state.snapshot();assert_eq!(snapshot["read"]["assessment"],"unavailable");
    assert_eq!(snapshot["read"]["selectedPath"]["encoding"],"unix_bytes");
    assert_eq!(snapshot["read"]["selectedPath"]["bytes"],json!(expected));
    assert_eq!(snapshot["read"]["displayPath"],selected.to_string_lossy().as_ref());
    assert!(snapshot["read"]["pathDisplayLimit"].as_str().unwrap().contains("lossy"));
    assert!(snapshot["read"]["originalBytes"].is_null());assert!(snapshot["read"]["originalDocument"].is_null());
    assert!(snapshot["reportedCurrency"].is_null());assert!(snapshot["basisCitationAssessment"].is_null());assert!(state.bound_read().is_none());
    serde_json::to_vec(&snapshot).unwrap(); // whole main-process snapshot serializes
}
#[test]
fn normal_unicode_selected_path_has_exact_identity_and_unqualified_display() {
    let files=Files::new();let mut paths=files.selected(&fixture("read_result.example-valid.json"),None);
    paths.read=files.write("résultat-Δ.json",&fixture("read_result.example-valid.json"));let selected=paths.read.clone();
    let state=ExternalObservation::load(paths);let snapshot=state.snapshot();assert_eq!(snapshot["read"]["assessment"],"received");
    assert_eq!(snapshot["read"]["displayPath"],selected.to_str().unwrap());assert!(snapshot["read"]["pathDisplayLimit"].is_null());
    #[cfg(unix)] {use std::os::unix::ffi::OsStrExt;assert_eq!(snapshot["read"]["selectedPath"]["bytes"],json!(selected.as_os_str().as_bytes()));}
    #[cfg(windows)] {use std::os::windows::ffi::OsStrExt;assert_eq!(snapshot["read"]["selectedPath"]["codeUnits"],json!(selected.as_os_str().encode_wide().collect::<Vec<u16>>()));}
    assert_eq!(state.read_evidence().selected_path(),selected);serde_json::to_vec(&snapshot).unwrap();
}
