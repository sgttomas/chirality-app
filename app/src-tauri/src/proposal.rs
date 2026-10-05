//! Bound App-side proposal custody. This module neither applies host changes
//! nor mints host content identities. Host one-effect enforcement is external.
use crate::catalog::{contracts, BoundRead, Catalog};
use serde_json::Value;
use std::collections::{HashMap, HashSet};
pub const PROPOSAL: &str = "urn:chirality:app-v4:proposed:proposal";
pub const STATE: &str = "urn:chirality:app-v4:proposed:proposal-state";
#[derive(Clone, Debug)]
pub struct BoundProposal { document: Value, bytes: Vec<u8>, reads: Vec<BoundRead>, host: Value }
impl BoundProposal {
    pub fn receive(bytes: &[u8], catalog: &Catalog, reads: &[BoundRead]) -> Result<Self, String> {
        let document: Value = serde_json::from_slice(bytes).map_err(|e| format!("schema-invalid JSON: {e}"))?;
        contracts()?.validate(PROPOSAL, &document)?;
        if reads.is_empty() || reads.iter().any(|r| !r.citable || r.host_identity() != &catalog.document()["host_identity"]) {
            return Err("domain-invalid proposal: citable same-host original reads required".into());
        }
        for basis in document["relied_on_basis"].as_array().unwrap() {
            if !reads.iter().any(|r| r.basis() == basis || r.document()["views"].as_array().unwrap().iter().any(|v| v.get("basis") == Some(basis))) {
                return Err("domain-invalid proposal: cited basis not observed in original reads".into());
            }
        }
        let mut items = HashSet::new();
        for item in document["items"].as_array().unwrap() {
            if !items.insert(item["item_identity"].as_str().unwrap()) { return Err("domain-invalid proposal: duplicate item identity".into()); }
            let entry = catalog.entry(item["operation_identity"].as_str().unwrap(), item["operation_version"].as_str().unwrap())
                .ok_or("domain-invalid proposal: undiscovered operation/version")?;
            if entry["effects"]["kind"] != "change" { return Err("domain-invalid proposal: item operation is not a change".into()); }
            for target in item["relied_on_targets"].as_array().unwrap() {
                let observed = reads.iter().any(|read| read.document()["views"].as_array().unwrap().iter().any(|view| {
                    let basis = view.get("basis").unwrap_or(read.basis());
                    document["relied_on_basis"].as_array().unwrap().contains(basis) &&
                    view["tables"].as_array().unwrap().iter().any(|table| table["rows"].as_array().unwrap().iter().any(|row| {
                        let s = &row["subject"];
                        ["subject_identity", "subject_content_identity", "identity_method"].iter().all(|f| s[*f] == target[*f])
                    }))
                }));
                if !observed { return Err("domain-invalid proposal: target identity/content not observed on cited basis".into()); }
            }
        }
        Ok(Self { document, bytes: bytes.to_vec(), reads: reads.to_vec(), host: catalog.document()["host_identity"].clone() })
    }
    pub fn document(&self) -> &Value { &self.document }
    pub fn original_bytes(&self) -> &[u8] { &self.bytes }
    pub fn original_reads(&self) -> &[BoundRead] { &self.reads }
    pub fn host_identity(&self) -> &Value { &self.host }
    pub fn identity(&self) -> &str { self.document["proposal_identity"]["value"].as_str().unwrap() }
    pub fn receive_state(&self, bytes: &[u8]) -> Result<HostObservation, String> {
        let document: Value = serde_json::from_slice(bytes).map_err(|e| format!("schema-invalid JSON: {e}"))?;
        validate_host_state(&document)?;
        if document["proposal_identity"] != self.identity() { return Err("domain-invalid state: proposal identity mismatch".into()); }
        if document["kind"] == "recorded_state" {
            let source = self.document["items"].as_array().unwrap();
            let observed = document["items"].as_array().unwrap();
            let mut ids = HashSet::new();
            for item in observed {
                let id = item["item_identity"].as_str().unwrap();
                if !ids.insert(id) || !source.iter().any(|i| i["item_identity"] == id) { return Err("domain-invalid state: duplicate/foreign item".into()); }
                if let Some(applied) = item.get("applied") {
                    if !self.document["relied_on_basis"].as_array().unwrap().contains(&applied["relied_on_basis"]) {
                        return Err("domain-invalid state: application retargeted original relied-on basis".into());
                    }
                }
            }
            if ids.len() != source.len() { return Err("domain-invalid state: missing item".into()); }
        }
        Ok(HostObservation { document, bytes: bytes.to_vec() })
    }
}
/// Shared P semantic receiving oracle, also used for retained dispatch results.
/// Shape success does not establish a human act; supplied references are only
/// claims being checked for internal consistency, never native act capture.
pub fn validate_host_state(document: &Value) -> Result<(), String> {
    contracts()?.validate(STATE, document)?;
    if document["kind"] != "recorded_state" { return Ok(()); }
    let items = document["items"].as_array().unwrap();
    let mut counts = serde_json::Map::new(); let mut ids = HashSet::new();
    for item in items {
        if !ids.insert(item["item_identity"].as_str().unwrap()) { return Err("domain-invalid state: duplicate item identity".into()); }
        let state = item["state"].as_str().unwrap();
        let act = item["decision"]["act_kind"].as_str();
        let required = match state { "accepted" => Some("A5"), "rejected" => Some("A10"), "withdrawn" => Some("A11"), _ => None };
        if required.is_some() && act != required { return Err(format!("domain-invalid state: {state} requires {}",required.unwrap())); }
        if let Some(applied) = item.get("applied") {
            if !matches!(state,"applied"|"applied_then_reversed") { return Err("domain-invalid state: applied association on non-applied item".into()); }
            if applied["branch"] == "after_acceptance" && act != Some("A5") { return Err("domain-invalid state: after_acceptance requires supplied A5".into()); }
            if applied["branch"] == "direct_under_grant" && act.is_some() { return Err("domain-invalid state: direct application never implies acceptance".into()); }
        }
        if matches!(state,"drafted"|"validated"|"queued"|"left_queue") && act.is_some() {
            return Err("domain-invalid state: decision inconsistent with undecided state".into());
        }
        if matches!(state,"refused_stale"|"refused_invalid"|"refused_not_permitted"|"application_error") && act.is_some() && act != Some("A5") {
            return Err("domain-invalid state: application refusal/error retains only A5".into());
        }
        let count = counts.entry(state.to_string()).or_insert(Value::from(0)); *count = Value::from(count.as_u64().unwrap()+1);
    }
    let summary = if counts.len()==1 { counts.keys().next().unwrap().as_str() } else { "mixed" };
    let open = items.iter().any(|i| matches!(i["state"].as_str(),Some("drafted"|"validated"|"queued"|"accepted")));
    let decided = items.iter().all(|i| i.get("decision").is_some_and(|d| matches!(d["act_kind"].as_str(),Some("A5"|"A10"))) || i.get("item_left").is_some());
    if document["derived_state"]["summary"] != summary || document["derived_state"]["counts"] != Value::Object(counts) || document["derived_state"]["open"] != open || document["derived_state"]["all_items_decided"] != decided {
        return Err("domain-invalid state: derived state stronger than items".into());
    }
    Ok(())
}
#[derive(Clone, Debug)]
pub struct HostObservation { document: Value, bytes: Vec<u8> }
impl HostObservation {
    pub fn document(&self) -> &Value { &self.document }
    pub fn original_bytes(&self) -> &[u8] { &self.bytes }
}
#[derive(Clone, Debug)]
pub enum SubmissionObservation { Sent, InvalidHostClaim { bytes: Vec<u8>, reason: String }, OutcomeUnknown { observer: String, reason: String }, Host(HostObservation) }
#[derive(Default)]
pub struct SubmissionCustody { proposals: HashMap<String, BoundProposal>, observations: HashMap<String, Vec<SubmissionObservation>> }
impl SubmissionCustody {
    /// First send only. Repeated identity is handled before any new-basis check;
    /// no retransmission is authorized here while host dedup scope is unselected.
    pub fn begin(&mut self, proposal: BoundProposal) -> Result<(), String> {
        if let Some(old) = self.proposals.get(proposal.identity()) {
            if old.original_bytes() != proposal.original_bytes() { return Err("identity_content_changed: original bytes retained; host identity method unselected".into()); }
            return Err("observe_before_resubmission: one-effect host mechanism unselected".into());
        }
        self.observations.insert(proposal.identity().to_string(), vec![SubmissionObservation::Sent]);
        self.proposals.insert(proposal.identity().to_string(), proposal); Ok(())
    }
    /// Transport acknowledgment is deliberately insufficient; absent host
    /// outcome stays unknown, including after detach or restart supplied by host.
    pub fn outcome_missing(&mut self, identity: &str, observer: &str, reason: &str) -> Result<(), String> {
        self.observations.get_mut(identity).ok_or("unknown proposal custody")?.push(SubmissionObservation::OutcomeUnknown { observer: observer.into(), reason: reason.into() }); Ok(())
    }
    pub fn observe(&mut self, identity: &str, bytes: &[u8]) -> Result<(), String> {
        let result = self.proposals.get(identity).ok_or("unknown proposal custody")?.receive_state(bytes);
        match result {
            Ok(observation) => { self.observations.get_mut(identity).unwrap().push(SubmissionObservation::Host(observation)); Ok(()) }
            Err(reason) => {
                self.observations.get_mut(identity).unwrap().push(SubmissionObservation::InvalidHostClaim { bytes: bytes.to_vec(), reason: reason.clone() });
                Err(reason)
            }
        }
    }
    pub fn history(&self, identity: &str) -> Option<&[SubmissionObservation]> { self.observations.get(identity).map(Vec::as_slice) }
    pub fn bound(&self, identity: &str) -> Option<&BoundProposal> { self.proposals.get(identity) }
}
