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
        let outcome = document["outcome"]["value"].as_str().unwrap();
        if let Some(result) = document.get("host_result") {
            let request = document["request_kind"].as_str().unwrap();
            let id = if result.get("kind").is_some() { crate::proposal::STATE }
                else if result.get("entries").is_some() { crate::catalog::CATALOG }
                else if result.get("outcome").is_some() { crate::catalog::READ }
                else { return Err("domain-invalid dispatch: host result contract not isolated".into()); };
            contracts()?.validate(id, result)?;
            if id == crate::proposal::STATE {
                crate::proposal::validate_host_state(result)?;
                if !matches!(request,"submission"|"observation"|"change_call") || result["proposal_identity"] != document["proposal_identity"] {
                    return Err("domain-invalid dispatch: wrong request/result proposal family or identity".into());
                }
            } else if matches!(request,"submission"|"observation") &&
                (id != crate::catalog::READ || result["outcome"] == "success") {
                return Err("domain-invalid dispatch: unrelated host result cannot establish submission outcome".into());
            }
            // Unknown is an observer overlay, never rewritten into a stronger
            // result. Every positive host report must be supported by this exact
            // isolated artifact; native completion and permission add no effect.
            if outcome != "outcome_unknown" {
                if document["outcome"]["reporter"] != "host" { return Err("domain-invalid dispatch: host result reporter mismatch".into()); }
                let supported = if id == crate::proposal::STATE {
                    match result["kind"].as_str().unwrap() {
                        "recorded_state" => {
                            let summary = result["derived_state"]["summary"].as_str().unwrap();
                            if outcome == "recorded_state" { true }
                            else { request == "submission" && result["answered_from_recorded_state"] != true && outcome == summary &&
                                matches!(summary,"queued"|"applied"|"refused_invalid"|"refused_stale"|"refused_not_permitted"|"application_error") }
                        }
                        "identity_conflict" => outcome == "refused_identity_conflict",
                        "not_known_to_host" => outcome == "not_known_to_host",
                        _ => false,
                    }
                } else if id == crate::catalog::READ { result["outcome"] == outcome }
                else { request == "discovery" && outcome == "success" };
                if !supported { return Err("domain-invalid dispatch: outcome exceeds or contradicts isolated host result; effect unknown".into()); }
            }
        } else if matches!(outcome,"applied"|"queued"|"recorded_state"|"refused_identity_conflict"|"not_known_to_host"|"application_error"|"refused_invalid"|"refused_stale"|"refused_not_permitted") || document["outcome"]["reporter"] == "host" {
            return Err("domain-invalid dispatch: native status cannot establish absent host outcome; effect unknown".into());
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
