//! Explicit successor semantic method; not a complete S1 validator.
use serde_json::{json, Value};
use sha2::{Digest, Sha256};

pub const LABEL_JOIN_REVISION: &str = "lifecycle-label-join.s2";

/// Identity is computed from compiled bytes, never from a caller-provided claim.
/// The source digest is outside the source it describes (no stored self digest).
pub fn label_join_identity() -> Value {
    fn digest(bytes: &[u8]) -> String { format!("{:x}", Sha256::digest(bytes)) }
    json!({
        "semanticRevision": LABEL_JOIN_REVISION,
        "readerSourceSha256": digest(include_bytes!("distribution_semantics.rs")),
        "schemas": {
            "lifecycle-event.s1": digest(include_bytes!("../resources/distribution-successor/lifecycle-event.s1.schema.json")),
            "observed-verification.s1": digest(include_bytes!("../resources/distribution-successor/observed-verification.s1.schema.json"))
        },
        "scope": "version-label-join-only"
    })
}

fn parsed_full_label(label: &str) -> Option<&str> {
    let version = label.strip_prefix("codex-cli ")?;
    let parts: Vec<_> = version.split('.').collect();
    (parts.len() == 3 && parts.iter().all(|p| !p.is_empty() && p.bytes().all(|b| b.is_ascii_digit())))
        .then_some(version)
}

/// Validate only the label join for a version-bearing legacy event.
/// Caller must separately validate schemas, artifact bytes, generation, outcome,
/// reference/custody and all other applicable S1 semantics. Missing identity is
/// an error here; callers dispatch non-version-bearing events separately.
pub fn validate_label_join(legacy_event: &Value, observation: &Value) -> Result<(), String> {
    let identity = legacy_event.get("versionIdentity").ok_or("missing version identity")?;
    let legacy = identity["observedVersionLabel"].as_str().ok_or("missing legacy label")?;
    let raw = observation["raw_version_label"].as_str().ok_or("missing raw label")?;
    let normalized = raw.strip_suffix('\n').unwrap_or(raw);
    let parsed = parsed_full_label(normalized).ok_or("malformed raw label")?;
    if parsed_full_label(legacy) != Some(parsed)
        || legacy != normalized
        || observation["observed_label"].as_str() != Some(parsed)
        || observation["pin"].as_str() != Some(parsed)
        || identity["declaredPin"].as_str() != Some(parsed)
    {
        return Err("version label disagreement".into());
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    fn pair() -> (Value, Value) {
        (json!({"versionIdentity":{"observedVersionLabel":"codex-cli 0.160.0","declaredPin":"0.160.0"}}),
         json!({"raw_version_label":"codex-cli 0.160.0\n","observed_label":"0.160.0","pin":"0.160.0"}))
    }
    #[test]
    fn exact_optional_one_lf_and_no_other_normalization() {
        let (event, mut observation) = pair();
        assert!(validate_label_join(&event, &observation).is_ok());
        observation["raw_version_label"] = json!("codex-cli 0.160.0");
        assert!(validate_label_join(&event, &observation).is_ok());
        for raw in ["codex-cli 0.160.0\n\n", "codex-cli 0.160.0\r\n", "codex-cli 0.160.0 ",
            "Codex-cli 0.160.0", "codex 0.160.0", "0.160.0", "codex-cli 0.161.0", "codex-cli 0.160.0-suffix"] {
            observation["raw_version_label"] = json!(raw);
            assert!(validate_label_join(&event, &observation).is_err(), "{raw:?}");
        }
    }
    #[test]
    fn rejects_every_contradictory_or_missing_join_member() {
        for field in ["raw_version_label", "observed_label", "pin"] {
            for replacement in [Value::Null, json!("0.161.0")] {
                let (event, mut observation) = pair();
                observation[field] = replacement;
                assert!(validate_label_join(&event, &observation).is_err(), "{field}");
            }
            let (event, mut observation) = pair();
            observation.as_object_mut().unwrap().remove(field);
            assert!(validate_label_join(&event, &observation).is_err());
        }
        for field in ["observedVersionLabel", "declaredPin"] {
            for replacement in [Value::Null, json!("0.160.0"), json!("codex-cli 0.160.0\n"), json!("codex-cli 0.161.0")] {
                let (mut event, observation) = pair();
                event["versionIdentity"][field] = replacement;
                if field == "declaredPin" && event["versionIdentity"][field] == "0.160.0" { continue; }
                assert!(validate_label_join(&event, &observation).is_err(), "{field}");
            }
        }
        assert!(validate_label_join(&json!({}), &pair().1).is_err());
    }
}
