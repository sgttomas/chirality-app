//! Full observed/lifecycle S1 value checks plus explicit fail-closed issuer limit.
//! This named reader does not confer supplier qualification or live custody.
use crate::distribution_preflight::{digest, equal, selection::Selected, Artifact, Inventory};
use serde_json::{json, Value};
use std::collections::BTreeMap;
pub(crate) type Files = BTreeMap<String, Vec<u8>>;
const OBS: &str =
    include_str!("../resources/distribution-successor/observed-verification.s1.schema.json");
const OBS_S4: &str = include_str!("../resources/distribution-successor/observed-verification.s4.schema.json");
const LIFE_S4: &str = include_str!("../resources/distribution-successor/lifecycle-event.s4.schema.json");
const LIFE: &str =
    include_str!("../resources/distribution-successor/lifecycle-event.s1.schema.json");
const LIFE_CURRENT: &str = include_str!("../resources/distribution-successor/lifecycle-event.s1.v0.10.schema.json");
const TRANSITIONS: &str =
    include_str!("../resources/distribution-successor/lifecycle-transitions.s1.json");
pub(crate) fn identity() -> Value {
    json!({"semanticRevision":"observed-lifecycle-reader.s4.v1","stringIdentity":crate::distribution_preflight::selection::string_identity_basis(),"readerSourceSha256":digest(include_bytes!("distribution_s1.rs")),"closureReaderSha256":digest(include_bytes!("distribution_selection.rs")),"storeReaderSha256":digest(include_bytes!("distribution_store_s1.rs")),"storeGuardsSha256":digest(include_bytes!("distribution_store.rs")),"namespaceAuthoritySourceSha256":digest(include_bytes!("attachment_custody.rs")),"preflightReaderSha256":digest(include_bytes!("distribution_preflight.rs")),"factsSchemaSha256":digest(include_bytes!("../resources/distribution-successor/distribution-preflight-facts.s3.schema.json")),"transportSchemaSha256":digest(include_bytes!("../resources/distribution-successor/distribution-closure-transport.s3.schema.json")),"labelJoin":crate::distribution_semantics::label_join_identity(),"schemas":{"expected-reference.s1":digest(include_bytes!("../resources/distribution-successor/expected-reference.s1.schema.json")),"adoption-attestation.s1":digest(include_bytes!("../resources/distribution-successor/adoption-attestation.s1.schema.json")),"observed-verification.s1":digest(OBS.as_bytes()),"lifecycle-event.s1":digest(LIFE.as_bytes()),"lifecycle-event.s1.v0.10":digest(LIFE_CURRENT.as_bytes())},"transitionsSha256":digest(TRANSITIONS.as_bytes()),"transitionProvenance":serde_json::from_str::<Value>(include_str!("../resources/distribution-successor/lifecycle-transitions.s1.provenance.json")).expect("compiled transition provenance"),"installedObserverSourceSha256":digest(include_bytes!("installed_custody.rs")),"installedSchemaSha256":digest(include_bytes!("../resources/distribution-successor/installed-custody-observation.s4.schema.json")),"s4ObservedSchemaSha256":digest(OBS_S4.as_bytes()),"s4LifecycleSchemaSha256":digest(LIFE_S4.as_bytes()),"limit":"S4 evidence semantics only; no disk payload grants live authority; historical S3 refuses custody pass"})
}
pub(crate) fn shape(value: &Value, schema: &str) -> Result<(), String> {
    let schema: Value = serde_json::from_str(schema).map_err(|e| e.to_string())?;
    jsonschema::validator_for(&schema)
        .map_err(|e| e.to_string())?
        .validate(value)
        .map_err(|e| e.to_string())
}
pub(crate) fn bytes<'a>(files: &'a Files, reference: &Value) -> Result<&'a [u8], String> {
    let r: Artifact = serde_json::from_value(reference.clone()).map_err(|e| e.to_string())?;
    if r.path
        .split('/')
        .any(|p| p.is_empty() || p == "." || p == ".." || p.contains(['\\', '\0', '\n', '\r']))
    {
        return Err("noncontained artifact path".into());
    }
    let raw = files.get(&r.path).ok_or("referenced artifact absent")?;
    if digest(raw) != r.sha256 {
        return Err("referenced artifact byte digest mismatch".into());
    }
    Ok(raw)
}
fn value(files: &Files, reference: &Value) -> Result<Value, String> {
    serde_json::from_slice(bytes(files, reference)?).map_err(|e| e.to_string())
}
fn inventory(value: &Value) -> Result<Inventory, String> {
    let inv: Inventory = serde_json::from_value(value.clone()).map_err(|e| e.to_string())?;
    if inv.method != "codex-vendor-tree-v1" || inv.algorithm != "sha-256" {
        return Err("inventory method differs".into());
    }
    let mut entries = BTreeMap::new();
    for e in &inv.entries {
        if e.mode > 0o7777 || !(e.kind == "file" || e.kind == "dir") {
            return Err("inventory entry type/mode".into());
        }
        if e.path != "."
            && e.path.split('/').any(|p| {
                p.is_empty() || p == "." || p == ".." || p.contains(['\\', '\0', '\n', '\r'])
            })
        {
            return Err("inventory path".into());
        }
        if entries.insert(e.path.as_str(), e).is_some() {
            return Err("duplicate inventory path".into());
        }
        if e.kind == "file"
            && (e.size.is_none()
                || e.sha256.as_ref().is_none_or(|s| {
                    s.len() != 64
                        || !s
                            .bytes()
                            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
                }))
        {
            return Err("invalid file digest/size".into());
        }
    }
    for (path, kind) in [
        (".", "dir"),
        ("bin", "dir"),
        ("codex-path", "dir"),
        ("codex-resources", "dir"),
        ("bin/codex", "file"),
        ("codex-package.json", "file"),
    ] {
        if entries.get(path).is_none_or(|e| e.kind != kind) {
            return Err(format!("missing required inventory member {path}"));
        }
    }
    for path in entries.keys().filter(|p| **p != ".") {
        let parent = path.rsplit_once('/').map(|p| p.0).unwrap_or(".");
        if entries.get(parent).is_none_or(|e| e.kind != "dir") {
            return Err("inventory parent absent".into());
        }
    }
    let manifest = entries
        .values()
        .filter(|e| e.kind == "file")
        .map(|e| format!("{}  {}\n", e.sha256.as_ref().unwrap(), e.path))
        .collect::<String>();
    if digest(manifest.as_bytes()) != inv.manifest_sha256 {
        return Err("inventory manifest differs".into());
    }
    Ok(inv)
}
pub(crate) fn observed(
    o: &Value,
    files: &Files,
    selected: Option<&Selected>,
) -> Result<String, String> {
    let s4 = o["format"] == "observed-verification.s4";
    shape(o, if s4 { OBS_S4 } else { OBS })?;
    let mut mismatch = false;
    let mut gap = false;
    for (name, check) in o["checks"].as_object().unwrap() {
        match check["outcome"].as_str().unwrap() {
            "mismatch" => mismatch = true,
            "pass" => (),
            _ => gap = true,
        }
        if check["evidence"].is_null() {
            gap = true;
        } else {
            let raw = bytes(files, &check["evidence"])?;
            if s4 && name != "custody" {
                let facts:Value=serde_json::from_slice(raw).map_err(|_|"S4 preflight evidence is opaque")?;
                if facts["format"]!="distribution-preflight-facts.s3" {return Err("S4 preflight evidence format unsupported".into());}
            }
            if let Ok(facts) = serde_json::from_slice::<Value>(raw) {
                if facts["format"] == "distribution-preflight-facts.s3" {
                    shape(&facts,include_str!("../resources/distribution-successor/distribution-preflight-facts.s3.schema.json"))?;
                    for key in [
                        "generation",
                        "inventory",
                        "raw_version_label",
                        "configuration",
                    ] {
                        if facts[key] != o[key] {
                            return Err(format!("named preflight facts differ: {key}"));
                        }
                    }
                }
            }
        }
    }
    // An opaque evidence payload or a caller's check flag is not an issuer.
    if o["checks"]["custody"]["outcome"] == "pass" {
        if !s4 { return Err("installed custody issuer unsupported by historical observed-lifecycle-reader.s3.v0.10".into()); }
        validate_installed(o, files, selected.ok_or("installed observation requires selected reference")?)?;
    } else if s4 {
        return Err("S4 observation requires installed custody pass".into());
    }
    let observed_inventory = if o["inventory"].is_null() {
        gap = true;
        None
    } else {
        match inventory(&o["inventory"]) {
            Ok(i) => Some(i),
            Err(_) => {
                mismatch = true;
                None
            }
        }
    };
    if let Some(selected) = selected {
        selected.check_mirror(files)?;
        if o["expected_reference"] != serde_json::to_value(selected.expected_ref()).unwrap()
            || o["adoption_attestation"]
                != serde_json::to_value(selected.attestation_ref()).unwrap()
        {
            return Err("selected observation reference/attestation differs".into());
        }
        let e = selected.expected()?;
        let expected_inventory = inventory(&e["inventory"])?;
        if e["pin"] != o["pin"] || e["platform"] != o["platform"] || e["launcher"] != o["launcher"]
        {
            mismatch = true;
        }
        if observed_inventory
            .as_ref()
            .is_some_and(|i| !equal(&expected_inventory, i))
        {
            mismatch = true;
        }
        if !o["generated"].is_null() && o["generated"] != e["generated"] {
            mismatch = true;
        }
    } else {
        if !o["expected_reference"].is_null() || !o["adoption_attestation"].is_null() {
            return Err("non-null reference lacks compiled association".into());
        }
        gap = true;
    }
    if o["generated"].is_null() {
        gap = true;
    } else {
        if o["generated"]["pin"] != o["pin"] {
            mismatch = true;
        }
        for key in ["provenance", "version_advance"] {
            bytes(files, &o["generated"][key])?;
        }
    }
    match o["raw_version_label"].as_str() {
        None => {
            gap = true;
            if !o["observed_label"].is_null() {
                mismatch = true;
            }
        }
        Some(raw) => {
            let normalized = raw.strip_suffix('\n').unwrap_or(raw);
            let event = json!({"versionIdentity":{"observedVersionLabel":normalized,"declaredPin":o["pin"]}});
            if crate::distribution_semantics::validate_label_join(&event, o).is_err() {
                mismatch = true;
            }
        }
    }
    if o["observed_label"].is_null() {
        gap = true;
    } else if o["observed_label"] != o["pin"] {
        mismatch = true;
    }
    let c = &o["configuration"];
    let root = c["resolved_root"].as_str().unwrap().trim_end_matches('/');
    let prefix = c["path_prefix"].as_str().unwrap();
    if prefix.contains([':', '\0'])
        || c["resolved_executable"] != format!("{root}/bin/codex")
        || prefix != format!("{root}/codex-path")
        || c["probe_home"] == c["account_home"]
    {
        mismatch = true;
    }
    for name in o["launcher"]["removed_wrapper_variables"]
        .as_array()
        .unwrap()
    {
        if !c["removed_environment_names"]
            .as_array()
            .unwrap()
            .contains(name)
        {
            mismatch = true;
        }
    }
    let actual = if mismatch {
        "mismatch"
    } else if gap {
        "unverifiable"
    } else {
        if !s4 { return Err("verified outcome requires unavailable installed issuer".into()); }
        "verified"
    };
    if o["outcome"] != actual {
        return Err(format!("claimed observation outcome differs from {actual}"));
    }
    Ok(actual.into())
}
pub(crate) fn lifecycle(
    l: &Value,
    files: &Files,
    selected: Option<&Selected>,
) -> Result<String, String> {
    let schema=match l["format"].as_str() {
        Some("lifecycle-event.s1")=>LIFE,
        Some("lifecycle-event.s1.v0.10")=>LIFE_CURRENT,
        Some("lifecycle-event.s4")=>LIFE_S4,
        _=>return Err("unsupported lifecycle envelope format".into()),
    };
    shape(l, schema)?;
    let e = &l["legacy_event"];
    let transitions: Value = serde_json::from_str(TRANSITIONS).map_err(|e| e.to_string())?;
    if transitions[e["transitionId"].as_str().unwrap()]
        != json!([e["fromState"], e["event"], e["toState"]])
    {
        return Err("legacy transition table violation".into());
    }
    if l["verification_artifact"].is_null() {
        if !l["verification_generation"].is_null()
            || !matches!(
                e["transitionId"].as_str().unwrap(),
                "LT-01" | "LT-02" | "LT-03" | "LT-15" | "LT-16" | "LT-20" | "LT-21" | "LT-22"
            )
            || e.get("verificationResult").is_some()
            || e.get("versionIdentity").is_some()
            || e["supplierStanding"] == "verified-pin"
        {
            return Err("verification artifact required".into());
        }
        return Ok("verification-not-yet-available".into());
    }
    let o = value(files, &l["verification_artifact"])?;
    if l["format"] != "lifecycle-event.s4" && o["format"] == "observed-verification.s4" { return Err("historical lifecycle reader refuses S4 evidence".into()); }
    if l["format"] == "lifecycle-event.s4" && o["format"] != "observed-verification.s4" { return Err("S4 lifecycle requires S4 observation".into()); }
    let outcome = observed(&o, files, selected)?;
    if l["verification_generation"] != o["generation"]
        || (!e["generation"].is_null() && e["generation"] != o["generation"])
    {
        return Err("lifecycle generation differs".into());
    }
    if let Some(v) = e.get("verificationResult") {
        if v["result"] != outcome {
            return Err("lifecycle outcome differs".into());
        }
    }
    if e["transitionId"] == "LT-04" && (outcome != "verified" || o["phase"] != "pre-spawn") {
        return Err("LT-04 requires pre-spawn verified".into());
    }
    if e["transitionId"] == "LT-24"
        && (outcome != "unverifiable"
            || o["phase"] != "pre-spawn"
            || o["observed_label"].is_null()
            || o["raw_version_label"].is_null())
    {
        return Err("LT-24 cannot waive contradiction".into());
    }
    if (e["supplierStanding"] == "verified-pin" && outcome != "verified")
        || (l["format"] == "lifecycle-event.s4" && outcome == "verified" && e["supplierStanding"] != "verified-pin") {
        return Err("lifecycle standing differs".into());
    }
    if e.get("versionIdentity").is_some() {
        crate::distribution_semantics::validate_label_join(e, &o)?;
    }
    Ok(outcome)
}

#[cfg(test)]
mod lifecycle_profile_tests {
    use super::*;
    #[test]
    fn process_group_custody_current_profile_and_legacy_dispatch_keep_unknown_distinct(){
        let event=json!({"recordKind":"lifecycle-event","sequence":1,"transitionId":"LT-01","generation":null,"fromState":"absent","event":"start-requested","toState":"verifying","at":"synthetic","descendants":{"checked":false,"surviving":0}});
        let mut old=json!({"format":"lifecycle-event.s1","legacy_event":event,"verification_artifact":null,"verification_generation":null});
        let files=Files::new();assert!(lifecycle(&old,&files,None).is_ok(),"legacy checked:false/0 remains readable");
        old["format"]=json!("lifecycle-event.s1.v0.10");assert!(lifecycle(&old,&files,None).is_err(),"current unknown cannot be zero");
        old["legacy_event"]["descendants"]=json!({"checked":false,"surviving":null,"handling":"unavailable: synthetic partial census"});assert!(lifecycle(&old,&files,None).is_ok());
        for bad in [json!({"checked":true,"surviving":null}),json!({"checked":true,"surviving":-1}),json!({"checked":false,"surviving":null}),json!({"checked":false,"surviving":null,"handling":"none surviving"})]{old["legacy_event"]["descendants"]=bad;assert!(lifecycle(&old,&files,None).is_err());}
        old["legacy_event"]["descendants"]=json!({"checked":true,"surviving":0,"handling":"none surviving"});assert!(lifecycle(&old,&files,None).is_ok());old["format"]=json!("lifecycle-event.future");assert!(lifecycle(&old,&files,None).is_err());
    }
}

/// Historical semantic revision remains fail-closed even for new-shaped inputs.
#[cfg(test)]
pub(crate) fn observed_s3(o: &Value, files: &Files, selected: Option<&Selected>) -> Result<String,String> {
    shape(o, OBS)?;
    observed(o, files, selected)
}

fn validate_installed(o:&Value, files:&Files, selected:&Selected)->Result<(),String> {
    let evidence=value(files,&o["checks"]["custody"]["evidence"])?;
    shape(&evidence,include_str!("../resources/distribution-successor/installed-custody-observation.s4.schema.json"))?;
    let object=evidence.as_object().ok_or("installed evidence is not an object")?;
    let fields=["format","generation","inventory","selection","app","standing","limits"];
    if object.len()!=fields.len() || fields.iter().any(|key|!object.contains_key(*key))
        || evidence["format"]!="installed-custody-observation.s4"
        || evidence["standing"]!="process-observation-evidence-only"
        || evidence["limits"]!=json!(["No live authority from serialized evidence", "No package, installer, quarantine or notarization qualification"])
    { return Err("unknown or incomplete installed custody evidence".into()); }
    if evidence["generation"]!=o["generation"] || evidence["inventory"]!=o["inventory"]
        || evidence["selection"]!=selected.association()
    { return Err("installed custody generation/inventory/selection differs".into()); }
    crate::installed_custody::validate_evidence(&evidence["app"])?;
    let root=o["configuration"]["resolved_root"].as_str().ok_or("supplier root absent")?;
    if root!=format!("{}/codex",evidence["app"]["location"]["resources"].as_str().ok_or("installed resources absent")?) {
        return Err("installed bundle and supplier root differ".into());
    }
    Ok(())
}
