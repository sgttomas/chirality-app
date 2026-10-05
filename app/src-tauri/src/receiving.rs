//! Local LOOP/PANEL receiving projections only. No model loop, network policy,
//! credential handling, private host mutation, or real host qualification.
use crate::catalog::{contracts, BoundRead, Catalog};
use serde_json::Value;
use std::collections::HashMap;
pub const TOOL_CALL: &str = "chirality:app-v4/DEL-05-01/LOOP_TOOL_CALL/0.1";
pub const DESTINATION: &str = "urn:chirality:app-v4:del-05-01:destination-request:0.1";
pub const PANEL: &str = "chirality:app-v4/DEL-05-02/PANEL_RETURN_INPUT/0.1";
#[derive(Debug)]
pub struct CallProjection { pub supplied: Value, pub ready_for_host_validation: bool, pub refusal: Option<String> }
/// All input schema checks precede catalog/domain checks. This consumes the
/// host's already assembled call form; it does not reconstruct supplier chunks.
pub fn receive_calls(calls: &[Value], catalog: &Catalog) -> Result<Vec<CallProjection>, String> {
    for call in calls { contracts()?.validate(TOOL_CALL, call)?; }
    let mut correlations = HashMap::new();
    for call in calls {
        if let Some(id) = call["call_correlation_identity"].as_str() { *correlations.entry(id).or_insert(0) += 1; }
    }
    let global = calls.iter().find_map(|c| match c["response_termination"].as_str() {
        Some("length-truncated") => Some("truncated response: no call dispatched"),
        Some("ended-without-reason") => Some("interrupted response: no call dispatched"),
        Some("content-filtered") => Some("filtered response: no call dispatched"),
        _ => None,
    });
    Ok(calls.iter().map(|call| {
        let mut refusal = global.map(str::to_string);
        if refusal.is_none() && call["rejection"].is_object() { refusal = Some(call["rejection"]["reason"].as_str().unwrap().into()); }
        if refusal.is_none() && (call["parse_state"] != "complete" || call["response_termination"] == "deprecated-function-call") {
            refusal = Some("malformed received call".into());
        }
        if refusal.is_none() && correlations.get(call["call_correlation_identity"].as_str().unwrap_or("")).copied().unwrap_or(0) > 1 {
            refusal = Some("duplicate correlation identity".into());
        }
        if refusal.is_none() {
            let entry = catalog.document()["entries"].as_array().unwrap().iter().find(|e| e["operation_identity"] == call["operation_reference"]);
            match entry {
                None => refusal = Some("not offered in discovered edition".into()),
                Some(entry) if entry["exposure"]["E"] != "exposed" => refusal = Some("not exposed on embedded surface".into()),
                Some(_) if call["argument_text"].as_str().is_none_or(|t| t.is_empty()) => refusal = Some("malformed: empty argument text".into()),
                Some(entry) => {
                    // Validate custody of supplied parsed value, never repair it.
                    let parsed: Result<Value, _> = serde_json::from_str(call["argument_text"].as_str().unwrap());
                    if parsed.as_ref().ok() != Some(&call["argument_value"]) { refusal = Some("malformed: argument text/value mismatch".into()); }
                    else if let Err(reason) = validate_offered_arguments(entry, &call["argument_value"]) { refusal = Some(reason); }
                }
            }
        }
        CallProjection { supplied: call.clone(), ready_for_host_validation: refusal.is_none(), refusal }
    }).collect())
}
/// V-3 checks exactly the declarations supplied in this edition. Catalog
/// descriptors do not supply enumeration choices or nested structured schemas;
/// those missing prerequisites hold readiness rather than invent a narrower V-3.
fn validate_offered_arguments(entry: &Value, value: &Value) -> Result<(), String> {
    let args = value.as_object().ok_or("V-3: arguments must be an object")?;
    let declared = entry["input"]["arguments"].as_array().unwrap();
    for name in args.keys() {
        if !declared.iter().any(|a| a["argument_name"] == *name) {
            return Err(format!("V-3: undeclared argument {name}; original value retained"));
        }
    }
    for arg in declared {
        let name = arg["argument_name"].as_str().unwrap();
        let Some(value) = args.get(name) else {
            if arg["required"] == true { return Err(format!("V-3: missing required argument {name}")); }
            continue;
        };
        let valid = match arg["value_kind"].as_str().unwrap() {
            "number" => value.is_number(), "text" => value.is_string(),
            "identity" => value.as_str().is_some_and(|s| !s.is_empty()),
            "boolean" => value.is_boolean(),
            "enumeration" | "basis_descriptor" | "carried_call" => {
                return Err(format!("V-3: complete supplied input schema unavailable for {name}; readiness held"));
            }
            _ => false,
        };
        if !valid { return Err(format!("V-3: wrong value kind for {name}")); }
    }
    Ok(())
}
#[derive(Clone, Debug)]
pub struct ModelChoice { pub interface_basis: String, pub model: String, pub destination: String }
pub fn supplied_model(choice: Option<ModelChoice>) -> Result<ModelChoice, String> {
    let choice = choice.ok_or("run not started — no model selected")?;
    if choice.interface_basis.is_empty() || choice.model.is_empty() || choice.destination.is_empty() {
        return Err("run not started — incomplete supplied model/destination choice".into());
    }
    Ok(choice)
}
#[derive(Clone, Debug)]
pub struct ReceivedDocument { document: Value, bytes: Vec<u8> }
impl ReceivedDocument {
    pub fn document(&self) -> &Value { &self.document }
    pub fn original_bytes(&self) -> &[u8] { &self.bytes }
    fn receive(id: &str, bytes: &[u8]) -> Result<Self, String> {
        let document: Value = serde_json::from_slice(bytes).map_err(|e| format!("schema-invalid JSON: {e}"))?;
        contracts()?.validate(id, &document)?; Ok(Self { document, bytes: bytes.to_vec() })
    }
}
pub fn receive_destination(bytes: &[u8]) -> Result<ReceivedDocument, String> { ReceivedDocument::receive(DESTINATION, bytes) }
pub fn receive_panel_input(bytes: &[u8]) -> Result<ReceivedDocument, String> { ReceivedDocument::receive(PANEL, bytes) }
#[derive(Debug, PartialEq, Eq)]
pub enum PanelComparison { SameMeaningfulContent, DifferentMeaningfulContent, HostTableNotSupplied }
/// Compares supplied original host table observations, including diagnostics,
/// standing and bindings. Surface/presentation differs; no upward summary.
pub fn compare_panel(read: &BoundRead, host_table: Option<&BoundRead>) -> PanelComparison {
    let Some(host) = host_table else { return PanelComparison::HostTableNotSupplied; };
    if read.host_identity() == host.host_identity() && ["operation","edition","basis","views","standing"].iter().all(|f| read.document()[*f] == host.document()[*f]) {
        PanelComparison::SameMeaningfulContent
    } else { PanelComparison::DifferentMeaningfulContent }
}
