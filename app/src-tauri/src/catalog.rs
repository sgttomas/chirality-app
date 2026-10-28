//! App-local supplied contracts; no network or host identity canonicalization.
use serde_json::Value;
use jsonschema::Validator;
use std::collections::{HashMap, HashSet};
use std::sync::OnceLock;
pub const RESOURCES: &[(&str, &str)] = &[
 ("LOOP_DESTINATION_REQUEST.schema.json", include_str!("../resources/catalog_adapter/LOOP_DESTINATION_REQUEST.schema.json")),
 ("LOOP_TOOL_CALL.schema.json", include_str!("../resources/catalog_adapter/LOOP_TOOL_CALL.schema.json")),
 ("PANEL_RETURN_INPUT.schema.json", include_str!("../resources/catalog_adapter/PANEL_RETURN_INPUT.schema.json")),
 ("catalog.schema.json", include_str!("../resources/catalog_adapter/catalog.schema.json")),
 ("channel_status.schema.json", include_str!("../resources/catalog_adapter/channel_status.schema.json")),
 ("checkpoint_observation.schema.json", include_str!("../resources/catalog_adapter/checkpoint_observation.schema.json")),
 ("edition_change_event.schema.json", include_str!("../resources/catalog_adapter/edition_change_event.schema.json")),
 ("external_dispatch_record.schema.json", include_str!("../resources/catalog_adapter/external_dispatch_record.schema.json")),
 ("proposal.schema.json", include_str!("../resources/catalog_adapter/proposal.schema.json")),
 ("proposal_state.schema.json", include_str!("../resources/catalog_adapter/proposal_state.schema.json")),
 ("read_result.schema.json", include_str!("../resources/catalog_adapter/read_result.schema.json")),
];
pub const IDS: &[&str] = &[
 "urn:chirality:app-v4:del-05-01:destination-request:0.1",
 "chirality:app-v4/DEL-05-01/LOOP_TOOL_CALL/0.1",
 "chirality:app-v4/DEL-05-02/PANEL_RETURN_INPUT/0.1",
 "urn:chirality:app-v4:proposed:catalog",
 "urn:chirality:app-v4:proposed:channel-status",
 "urn:chirality:app-v4:proposed:checkpoint-observation",
 "urn:chirality:app-v4:proposed:edition-change-event",
 "urn:chirality:app-v4:proposed:external-dispatch-record",
 "urn:chirality:app-v4:proposed:proposal",
 "urn:chirality:app-v4:proposed:proposal-state",
 "urn:chirality:app-v4:proposed:read-result",
];
pub struct Contracts(HashMap<String, Validator>);
impl Contracts {
    pub fn from_resources(resources: &[(&str, &str)]) -> Result<Self, String> {
        let validators = crate::schema_validation::compile_targets(resources, IDS, IDS)?;
        Ok(Self(IDS.iter().map(|id| id.to_string()).zip(validators).collect()))
    }
    pub fn validate(&self, id: &str, value: &Value) -> Result<(), String> {
        self.0.get(id).ok_or_else(|| format!("unknown contract: {id}"))?
            .validate(value).map_err(|e| format!("schema-invalid: {e}"))
    }
}
pub fn contracts() -> Result<&'static Contracts, String> {
    static VALUE: OnceLock<Result<Contracts, String>> = OnceLock::new();
    VALUE.get_or_init(|| Contracts::from_resources(RESOURCES)).as_ref().map_err(Clone::clone)
}
pub const CATALOG: &str = "urn:chirality:app-v4:proposed:catalog";
pub const READ: &str = "urn:chirality:app-v4:proposed:read-result";
#[derive(Clone, Debug)]
pub struct Catalog { document: Value, bytes: Vec<u8> }
impl Catalog {
    pub fn receive(bytes: &[u8]) -> Result<Self, String> {
        let document: Value = serde_json::from_slice(bytes).map_err(|e| format!("schema-invalid JSON: {e}"))?;
        contracts()?.validate(CATALOG, &document)?;
        let mut operations = HashSet::new();
        for entry in document["entries"].as_array().unwrap() {
            if !operations.insert(entry["operation_identity"].as_str().unwrap()) {
                return Err("domain-invalid catalog: duplicate operation identity".into());
            }
            let args = entry["input"]["arguments"].as_array().unwrap();
            let mut names = HashSet::new();
            for arg in args {
                if !names.insert(arg["argument_name"].as_str().unwrap()) {
                    return Err("domain-invalid catalog: duplicate argument name".into());
                }
            }
            let contact = &entry["effects"]["external_contact"];
            if contact["destination_form"] == "from_argument" &&
                !names.contains(contact["argument_name"].as_str().unwrap()) {
                return Err("domain-invalid catalog CX-1: undeclared destination argument".into());
            }
        }
        Ok(Self { document, bytes: bytes.to_vec() })
    }
    pub fn document(&self) -> &Value { &self.document }
    pub fn original_bytes(&self) -> &[u8] { &self.bytes }
    pub fn entry(&self, identity: &str, version: &str) -> Option<&Value> {
        self.document["entries"].as_array()?.iter().find(|e|
            e["operation_identity"] == identity && e["operation_version"] == version)
    }
    pub fn receive_read(&self, bytes: &[u8]) -> Result<ReadObservation, String> {
        let document: Value = serde_json::from_slice(bytes).map_err(|e| format!("schema-invalid JSON: {e}"))?;
        contracts()?.validate(READ, &document)?;
        if document["outcome"] != "success" {
            return Ok(ReadObservation::NonSuccess { document, bytes: bytes.to_vec() });
        }
        if document["edition"] != self.document["edition"] {
            return Err("domain-invalid read: undiscovered edition".into());
        }
        let entry = self.entry(document["operation"]["operation_identity"].as_str().unwrap(),
            document["operation"]["operation_version"].as_str().unwrap())
            .ok_or("domain-invalid read: undiscovered operation/version")?;
        let surface = document["surface"].as_str().unwrap();
        if entry["exposure"][surface] != "exposed" {
            return Err("domain-invalid read: surface not exposed".into());
        }
        for check in document["standing"]["host_checks"].as_array().unwrap() {
            if !entry["result"]["named_host_checks"].as_array().unwrap().contains(&check["check_name"]) {
                return Err("domain-invalid read: undeclared host check".into());
            }
        }
        let profile = &self.document["basis_profile"];
        let mut limits = Vec::new();
        let mut citable = true;
        let mut bases = vec![&document["basis"]];
        for view in document["views"].as_array().unwrap() {
            if let Some(basis) = view.get("basis") { bases.push(basis); }
        }
        for basis in bases {
            for field in ["workspace_identity", "generation", "model_revision", "canonical_content_identity", "identity_method"] {
                let value = &basis[field];
                if value.is_string() { continue; }
                if ["workspace_identity", "generation"].contains(&field) &&
                    value["not_supplied"] == "host_declares_none" && profile[field] == "not_supplied" {
                    if !limits.contains(&"basis_lineage_not_supplied".to_string()) { limits.push("basis_lineage_not_supplied".into()); }
                } else { citable = false; }
            }
        }
        Ok(ReadObservation::Success(BoundRead { document, bytes: bytes.to_vec(),
            host_identity: self.document["host_identity"].clone(), profile: profile.clone(), citable, limits }))
    }
}
#[derive(Clone, Debug)]
pub struct BoundRead {
    document: Value, bytes: Vec<u8>, host_identity: Value, profile: Value,
    pub citable: bool, pub limits: Vec<String>,
}
impl BoundRead {
    pub fn document(&self) -> &Value { &self.document }
    pub fn original_bytes(&self) -> &[u8] { &self.bytes }
    pub fn host_identity(&self) -> &Value { &self.host_identity }
    pub fn profile(&self) -> &Value { &self.profile }
    pub fn basis(&self) -> &Value { &self.document["basis"] }
}
#[derive(Clone, Debug)]
pub enum ReadObservation { Success(BoundRead), NonSuccess { document: Value, bytes: Vec<u8> } }
#[derive(Debug, PartialEq, Eq)]
pub enum BasisComparison { Same, Changed, Incomparable }
/// Absent lineage or unlike identity methods cannot prove same or changed.
pub fn compare_basis(a: &Value, b: &Value) -> BasisComparison {
    for field in ["workspace_identity", "generation", "identity_method"] {
        if !a[field].is_string() || !b[field].is_string() || a[field] != b[field] {
            return BasisComparison::Incomparable;
        }
    }
    for field in ["canonical_content_identity", "model_revision"] {
        if !a[field].is_string() || !b[field].is_string() { return BasisComparison::Incomparable; }
    }
    if a == b { BasisComparison::Same } else { BasisComparison::Changed }
}
