//! Shared closed vocabulary for act evidence. Classification and presentation
//! are derived here; only the cause name is persisted on evidence_limit.
use serde::{Deserialize, Serialize};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Standing { Settled, ReadLimit }

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum ActEvidenceCause {
    NoSeal,
    SealMethodUnsupported,
    SealMalformed,
    ProviderInvalid,
    ProviderMismatch,
    SealInvalid,
    CaptureFactsUnencodable,
    ProviderNotEligible,
    AuthorityUnavailable,
    SealRootUnavailable,
    KeychainUnavailable,
    ProtectionInconsistent,
    ContinuityUnavailable,
    KeyNotHeld,
    KeyMaterialInvalid,
    KeyStorageUnsafe,
    SealSourceChanged,
    SealOperationBusy,
    SealWriteUnavailable,
    SealEntropyUnavailable,
    KeychainProviderUnavailableOnThisBuild,
    CaptureMissing,
    CaptureInvalid,
    RecordDiffersFromCapture,
    SharedCapture,
    ConflictingIdentity,
    NotCapturingSurface,
    AnotherActKind,
    ContentNoLongerCurrent,
    ActOnOtherContent,
    IncomparableMethod,
    CaptureUnreadable,
    RelationUnresolved,
    ActsNotRead,
    ContentNotObtainable,
    SubjectAbsent,
}
impl ActEvidenceCause {
    pub const ALL: &'static [Self] = &[
        Self::NoSeal,
        Self::SealMethodUnsupported,
        Self::SealMalformed,
        Self::ProviderInvalid,
        Self::ProviderMismatch,
        Self::SealInvalid,
        Self::CaptureFactsUnencodable,
        Self::ProviderNotEligible,
        Self::AuthorityUnavailable,
        Self::SealRootUnavailable,
        Self::KeychainUnavailable,
        Self::ProtectionInconsistent,
        Self::ContinuityUnavailable,
        Self::KeyNotHeld,
        Self::KeyMaterialInvalid,
        Self::KeyStorageUnsafe,
        Self::SealSourceChanged,
        Self::SealOperationBusy,
        Self::SealWriteUnavailable,
        Self::SealEntropyUnavailable,
        Self::KeychainProviderUnavailableOnThisBuild,
        Self::CaptureMissing,
        Self::CaptureInvalid,
        Self::RecordDiffersFromCapture,
        Self::SharedCapture,
        Self::ConflictingIdentity,
        Self::NotCapturingSurface,
        Self::AnotherActKind,
        Self::ContentNoLongerCurrent,
        Self::ActOnOtherContent,
        Self::IncomparableMethod,
        Self::CaptureUnreadable,
        Self::RelationUnresolved,
        Self::ActsNotRead,
        Self::ContentNotObtainable,
        Self::SubjectAbsent,
    ];
    pub fn standing(self) -> Standing {
        match self {
            Self::NoSeal => Standing::Settled,
            Self::SealMethodUnsupported => Standing::Settled,
            Self::SealMalformed => Standing::Settled,
            Self::ProviderInvalid => Standing::Settled,
            Self::ProviderMismatch => Standing::Settled,
            Self::SealInvalid => Standing::Settled,
            Self::CaptureFactsUnencodable => Standing::Settled,
            Self::ProviderNotEligible => Standing::Settled,
            Self::AuthorityUnavailable => Standing::ReadLimit,
            Self::SealRootUnavailable => Standing::ReadLimit,
            Self::KeychainUnavailable => Standing::ReadLimit,
            Self::ProtectionInconsistent => Standing::ReadLimit,
            Self::ContinuityUnavailable => Standing::ReadLimit,
            Self::KeyNotHeld => Standing::ReadLimit,
            Self::KeyMaterialInvalid => Standing::ReadLimit,
            Self::KeyStorageUnsafe => Standing::ReadLimit,
            Self::SealSourceChanged => Standing::ReadLimit,
            Self::SealOperationBusy => Standing::ReadLimit,
            Self::SealWriteUnavailable => Standing::ReadLimit,
            Self::SealEntropyUnavailable => Standing::ReadLimit,
            Self::KeychainProviderUnavailableOnThisBuild => Standing::ReadLimit,
            Self::CaptureMissing => Standing::Settled,
            Self::CaptureInvalid => Standing::Settled,
            Self::RecordDiffersFromCapture => Standing::Settled,
            Self::SharedCapture => Standing::Settled,
            Self::ConflictingIdentity => Standing::Settled,
            Self::NotCapturingSurface => Standing::Settled,
            Self::AnotherActKind => Standing::Settled,
            Self::ContentNoLongerCurrent => Standing::Settled,
            Self::ActOnOtherContent => Standing::Settled,
            Self::IncomparableMethod => Standing::Settled,
            Self::CaptureUnreadable => Standing::ReadLimit,
            Self::RelationUnresolved => Standing::ReadLimit,
            Self::ActsNotRead => Standing::ReadLimit,
            Self::ContentNotObtainable => Standing::ReadLimit,
            Self::SubjectAbsent => Standing::ReadLimit,
        }
    }
    /// Execution owns observation/counting sentences. Their callers retain
    /// raw detail when this returns None; there are no placeholder sentences.
    pub fn sentence(self, detail: &str) -> Option<String> {
        match self {
            Self::NoSeal => Some("No seal is present on this capture. Who wrote it is not established. This capture will never be sealed later. To obtain a counted act, perform the act again.".into()),
            Self::SealMethodUnsupported => Some("This capture's seal method is not supported here; its seal is not verifiable.".into()),
            Self::SealMalformed => Some("This capture's seal is malformed; its seal is not verifiable.".into()),
            Self::ProviderInvalid => Some("This capture's provider label is invalid; its seal is not verifiable.".into()),
            Self::ProviderMismatch => Some("This capture claims the keychain provider but the verifying key comes from the key file; the claim is not verifiable as labelled.".into()),
            Self::SealInvalid => Some("The seal does not match this capture's covered facts under the named provider's key. The capture remains a recorded claim.".into()),
            Self::CaptureFactsUnencodable => Some("These capture facts cannot be encoded for seal verification; its seal is not verifiable.".into()),
            Self::ProviderNotEligible => Some("The file-key seal cannot supply keychain-verified workflow approval. Confirm A15 in this session, or enrol and make a new approval for future sessions.".into()),
            Self::AuthorityUnavailable => Some("The App's installed keychain lookup identity cannot be validated now. No file key is substituted. Check the installed App and check again.".into()),
            Self::SealRootUnavailable => Some("The installation's sealing-key location cannot be used here. No alternative key is substituted. Restore access to the original installation and check again.".into()),
            Self::KeychainUnavailable => Some(format!("Keychain verification is unavailable now ({detail}). No file key is substituted. Unlock or restore this App's access, then check again.")),
            Self::ProtectionInconsistent => Some("Earlier keychain protection is indicated, but its current evidence does not agree. No file key is substituted. Open Recover capture verification.".into()),
            Self::ContinuityUnavailable => Some("The original keychain continuity is unavailable or incomplete. No file key is substituted. Open Recover capture verification; existing choices stay recorded.".into()),
            Self::KeyNotHeld => Some("This installation does not currently hold the named key. The recorded choice is kept; verification is pending. Restore the original key/installation if available, then check again.".into()),
            Self::KeyMaterialInvalid => Some("The named provider's key material cannot be used as recorded. No substitute key is used. Recover capture verification and check again.".into()),
            Self::KeyStorageUnsafe => Some("The named key storage fails its safety checks. It is not used; restore the original safe storage and check again.".into()),
            Self::SealSourceChanged => Some("The key or protection evidence changed while it was checked. No seal result is available from that read; check again.".into()),
            Self::SealOperationBusy => Some("Another key operation is in progress, or its coordination is unavailable. No weaker key is substituted; check again.".into()),
            Self::SealWriteUnavailable => Some("A seal could not be completed because key storage could not be written reliably. Check storage and check again.".into()),
            Self::SealEntropyUnavailable => Some("A new sealing key could not be generated now. No key was substituted. Check again when key generation is available.".into()),
            Self::KeychainProviderUnavailableOnThisBuild => Some("This capture was sealed with the keychain key, which this build of the App cannot reach (an unsigned or development build). The recorded choice is kept; open it in the signed App to verify.".into()),
            Self::CaptureMissing => None,
            Self::CaptureInvalid => None,
            Self::RecordDiffersFromCapture => None,
            Self::SharedCapture => None,
            Self::ConflictingIdentity => None,
            Self::NotCapturingSurface => None,
            Self::AnotherActKind => None,
            Self::ContentNoLongerCurrent => None,
            Self::ActOnOtherContent => None,
            Self::IncomparableMethod => None,
            Self::CaptureUnreadable => None,
            Self::RelationUnresolved => None,
            Self::ActsNotRead => None,
            Self::ContentNotObtainable => None,
            Self::SubjectAbsent => None,
        }
    }
}

/// Decide the cause at the failing primitive; preserve its original detail.
/// There is deliberately no From<String>, wildcard cause or English parser.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct EvidenceFailure {
    pub cause: ActEvidenceCause,
    pub detail: String,
}
impl EvidenceFailure {
    pub fn new(cause: ActEvidenceCause, detail: impl Into<String>) -> Self {
        Self { cause, detail: detail.into() }
    }
    pub fn with_detail(mut self, detail: impl Into<String>) -> Self {
        self.detail = detail.into();
        self
    }
    pub fn display_sentence(&self) -> String {
        self.cause.sentence(&self.detail).unwrap_or_else(|| self.detail.clone())
    }
    #[cfg(test)]
    pub fn contains(&self, needle: &str) -> bool { self.detail.contains(needle) }
}
impl std::fmt::Display for EvidenceFailure {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str(&self.detail) }
}
impl std::error::Error for EvidenceFailure {}
impl From<EvidenceFailure> for String {
    fn from(value: EvidenceFailure) -> Self { value.detail }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn schema_enum_equals_the_shared_cause_enum() {
        let schema: serde_json::Value = serde_json::from_str(include_str!("../schemas/RS_RECORD.schema.json")).unwrap();
        let encoded: std::collections::BTreeSet<_> = ActEvidenceCause::ALL.iter().map(|cause| serde_json::to_value(cause).unwrap().as_str().unwrap().to_owned()).collect();
        let declared: std::collections::BTreeSet<_> = schema["$defs"]["evidenceLimit"]["properties"]["cause"]["enum"].as_array().unwrap().iter().map(|v| v.as_str().unwrap().to_owned()).collect();
        assert_eq!(encoded, declared);
        assert_eq!(encoded.len(), ActEvidenceCause::ALL.len());
    }
    #[test]
    fn every_cause_has_a_standing_and_only_seal_causes_have_sentences() {
        for cause in ActEvidenceCause::ALL {
            let _ = cause.standing();
            let observation = matches!(cause,
                ActEvidenceCause::CaptureMissing |
                ActEvidenceCause::CaptureInvalid |
                ActEvidenceCause::RecordDiffersFromCapture |
                ActEvidenceCause::SharedCapture |
                ActEvidenceCause::ConflictingIdentity |
                ActEvidenceCause::NotCapturingSurface |
                ActEvidenceCause::AnotherActKind |
                ActEvidenceCause::ContentNoLongerCurrent |
                ActEvidenceCause::ActOnOtherContent |
                ActEvidenceCause::IncomparableMethod |
                ActEvidenceCause::CaptureUnreadable |
                ActEvidenceCause::RelationUnresolved |
                ActEvidenceCause::ActsNotRead |
                ActEvidenceCause::ContentNotObtainable |
                ActEvidenceCause::SubjectAbsent
            );
            assert_eq!(cause.sentence("invented detail").is_none(), observation, "{cause:?}");
        }
    }
}
