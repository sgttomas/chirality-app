//! App-owned receiving seam over an explicitly supplied local host boundary.
//! No endpoint discovery, native command parsing, credential or network code.
use crate::catalog::contracts;
use crate::proposal::{BoundProposal, SubmissionCustody};
use serde_json::Value;
pub const CHANNEL: &str = "urn:chirality:app-v4:proposed:channel-status";
pub const DISPATCH: &str = "urn:chirality:app-v4:proposed:external-dispatch-record";
#[derive(Clone, Debug)]
pub struct Channel { document: Value, bytes: Vec<u8> }
impl Channel {
    pub fn receive(bytes: &[u8]) -> Result<Self, String> {
        let document: Value = serde_json::from_slice(bytes).map_err(|e| format!("schema-invalid JSON: {e}"))?;
        contracts()?.validate(CHANNEL, &document)?;
        if document["channel_state"] == "enabled" && (document["host_enablement"]["record"] != "in_force" ||
            document["app_side_configuration"]["present"] != true || document["endpoint"]["reachable"] != "yes") {
            return Err("domain-invalid channel: enabled lacks supplied enablement/configuration/endpoint".into());
        }
        Ok(Self { document, bytes: bytes.to_vec() })
    }
    pub fn document(&self) -> &Value { &self.document }
    pub fn original_bytes(&self) -> &[u8] { &self.bytes }
    pub fn enabled(&self) -> bool { self.document["channel_state"] == "enabled" }
    /// The injected boundary is the only effectful operation. Receipt failure
    /// retains bound bytes and reports uncertainty, never native-success applied.
    pub fn submit<F>(&self, proposal: BoundProposal, custody: &mut SubmissionCustody, boundary: F) -> Result<(), String>
    where F: FnOnce(&[u8]) -> Result<Vec<u8>, String> {
        if !self.enabled() { return Err("channel_not_enabled: no dispatch".into()); }
        if proposal.host_identity() != &self.document["host_identity"] { return Err("domain-invalid channel: different host".into()); }
        let identity = proposal.identity().to_string();
        let bytes = proposal.original_bytes().to_vec();
        custody.begin(proposal)?;
        match boundary(&bytes) {
            Ok(receipt) => {
                if let Err(reason) = custody.observe(&identity, &receipt) {
                    custody.outcome_missing(&identity, "app", &format!("host result not established: {reason}"))?;
                }
            }
            Err(reason) => custody.outcome_missing(&identity, "app", &reason)?,
        }
        Ok(())
    }
}
#[derive(Clone, Debug)]
pub struct DispatchAccount { document: Value, bytes: Vec<u8>, pub missing: Vec<&'static str> }
impl DispatchAccount {
    pub fn receive(bytes: &[u8]) -> Result<Self, String> {
        let document: Value = serde_json::from_slice(bytes).map_err(|e| format!("schema-invalid JSON: {e}"))?;
        contracts()?.validate(DISPATCH, &document)?;
        if let Some(result) = document.get("host_result") {
            let id = if result.get("kind").is_some() { crate::proposal::STATE }
                else if result.get("entries").is_some() { crate::catalog::CATALOG }
                else if result.get("outcome").is_some() { crate::catalog::READ }
                else { return Err("domain-invalid dispatch: host result contract not isolated".into()); };
            contracts()?.validate(id, result)?;
            if result.get("proposal_identity").is_some() && result["proposal_identity"] != document["proposal_identity"] {
                return Err("domain-invalid dispatch: different proposal host result".into());
            }
        } else if matches!(document["outcome"]["value"].as_str(), Some("applied"|"queued"|"recorded_state")) {
            return Err("domain-invalid dispatch: native status cannot establish host outcome".into());
        }
        // LOOP §6.2 / ADAPTER §5.1. Optional receipt fields never silently
        // become supplied; missing facts are an explicit receiving account.
        let mut missing = Vec::new();
        for (meaning, field) in [("origin", "origin_observed"), ("grant_in_force", "grant_in_force"),
            ("requested_mode", "requested_mode"), ("governing_checkpoint_constraint", "constraint_carriage"),
            ("relied_on_basis", "relied_on_basis"), ("catalog_edition", "edition"),
            ("proposal_identity", "proposal_identity"), ("proposal_minted_by", "proposal_minted_by"),
            ("reason", "reason")] {
            if document.get(field).is_none() { missing.push(meaning); }
        }
        if document["operation"].get("operation_version").is_none() { missing.push("entry_version"); }
        Ok(Self { document, bytes: bytes.to_vec(), missing })
    }
    pub fn document(&self) -> &Value { &self.document }
    pub fn original_bytes(&self) -> &[u8] { &self.bytes }
}
