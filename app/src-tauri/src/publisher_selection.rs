//! Authority comes only from compiler-included build outputs, never disk/IPC.
//! Public projections are derivatives, not a selection or live-start capability.
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
include!(concat!(env!("OUT_DIR"), "/publisher_selection.rs"));

/// No Deserialize, public fields or caller-input constructor. The selector below
/// can construct this only from the compiled constants of this exact App build.
pub(crate) struct CompiledPublisherSelection {
    requirement: &'static str,
    binding_digest: &'static str,
    public_projection_digest: &'static str,
}
impl CompiledPublisherSelection {
    pub(crate) fn requirement(&self) -> &'static str {
        self.requirement
    }
}
fn hash(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
fn shape(value: &Value, schema: &str) -> Result<(), String> {
    let schema: Value =
        serde_json::from_str(schema).map_err(|_| "compiled publisher schema invalid")?;
    jsonschema::validator_for(&schema)
        .map_err(|_| "compiled publisher schema invalid")?
        .validate(value)
        .map_err(|_| "compiled publisher binding shape invalid".into())
}
/// Semantic checking returns no authority. Only selected(), with no arguments,
/// may wrap compiler-included values in the process-local type.
fn validate_artifacts(
    requirement: &str,
    raw: &str,
    digest: &str,
    public: &str,
    public_digest: &str,
) -> Result<(), String> {
    if hash(raw.as_bytes()) != digest || hash(public.as_bytes()) != public_digest {
        return Err("compiled publisher artifact byte digest differs".into());
    }
    let binding: Value =
        serde_json::from_str(raw).map_err(|_| "compiled publisher binding invalid")?;
    let projection: Value =
        serde_json::from_str(public).map_err(|_| "compiled publisher projection invalid")?;
    shape(
        &binding,
        include_str!("../schemas/publisher-build-binding.s1.schema.json"),
    )?;
    shape(
        &projection,
        include_str!("../schemas/publisher-build-public-projection.s1.schema.json"),
    )?;
    for (key, bytes) in [
        (
            "template_sha256",
            include_bytes!("../build_support/developer-id-application.s1.requirement-template.txt")
                .as_slice(),
        ),
        (
            "generator_sha256",
            include_bytes!("../build_support/publisher_selection.rs").as_slice(),
        ),
        ("recipe_sha256", include_bytes!("../build.rs").as_slice()),
        (
            "input_schema_sha256",
            include_bytes!("../schemas/publisher-build-selection.s1.schema.json").as_slice(),
        ),
        (
            "cargo_manifest_sha256",
            include_bytes!("../Cargo.toml").as_slice(),
        ),
        (
            "cargo_lock_sha256",
            include_bytes!("../Cargo.lock").as_slice(),
        ),
        (
            "binding_schema_sha256",
            include_bytes!("../schemas/publisher-build-binding.s1.schema.json").as_slice(),
        ),
        (
            "public_projection_schema_sha256",
            include_bytes!("../schemas/publisher-build-public-projection.s1.schema.json")
                .as_slice(),
        ),
    ] {
        if binding[key] != hash(bytes) {
            return Err("compiled publisher recipe identity differs".into());
        }
    }
    if binding["requirement_sha256"] != hash(requirement.as_bytes())
        || binding["build_context_sha256"]
            != hash(
                &serde_json::to_vec(&binding["build_context"])
                    .map_err(|_| "compiled publisher context invalid")?,
            )
        || binding["production_bundle_identifier"]
            != binding["build_context"]["application_identifier"]
        || binding["build_context"]["package_version"] != env!("CARGO_PKG_VERSION")
        || projection["original_binding_sha256"] != digest
    {
        return Err("compiled publisher requirement/context join differs".into());
    }
    let expected_requirement =
        include_str!("../build_support/developer-id-application.s1.requirement-template.txt")
            .replace(
                "{{production_bundle_identifier}}",
                &format!(
                    "\"{}\"",
                    binding["production_bundle_identifier"].as_str().unwrap()
                ),
            )
            .replace(
                "{{developer_id_team_identifier}}",
                &format!(
                    "\"{}\"",
                    binding["developer_id_team_identifier"].as_str().unwrap()
                ),
            );
    if requirement != expected_requirement {
        return Err("compiled publisher requirement differs from independent template".into());
    }
    for key in [
        "input_sha256",
        "requirement_sha256",
        "template_sha256",
        "generator_sha256",
        "recipe_sha256",
        "input_schema_sha256",
        "cargo_manifest_sha256",
        "cargo_lock_sha256",
        "binding_schema_sha256",
        "public_projection_schema_sha256",
        "build_context_sha256",
    ] {
        if projection[key] != binding[key] {
            return Err("publisher public projection differs from original".into());
        }
    }
    Ok(())
}
pub(crate) fn selected() -> Result<Option<CompiledPublisherSelection>, String> {
    match (
        COMPILED_PUBLISHER_REQUIREMENT,
        COMPILED_PUBLISHER_BINDING_JSON,
        COMPILED_PUBLISHER_BINDING_SHA256,
        COMPILED_PUBLISHER_PUBLIC_PROJECTION_JSON,
        COMPILED_PUBLISHER_PUBLIC_PROJECTION_SHA256,
    ) {
        (None, None, None, None, None) => Ok(None),
        (Some(requirement), Some(raw), Some(digest), Some(public), Some(public_digest)) => {
            if !cfg!(chirality_publisher_selected)
                || cfg!(test)
                || cfg!(debug_assertions)
                || cfg!(dev)
                || !cfg!(target_os = "macos")
                || !cfg!(target_arch = "aarch64")
                || !cfg!(feature = "distribution-successor")
                || !cfg!(feature = "custom-protocol")
                || cfg!(feature = "synthetic-distribution-anchor")
            {
                return Err(
                    "compiled publisher selection unavailable outside production macOS successor"
                        .into(),
                );
            }
            validate_artifacts(requirement, raw, digest, public, public_digest)?;
            Ok(Some(CompiledPublisherSelection {
                requirement,
                binding_digest: digest,
                public_projection_digest: public_digest,
            }))
        }
        _ => Err("compiled publisher selection is incomplete".into()),
    }
}
/// Diagnostics bind original and derivative separately. This metadata is not a
/// constructor or proof of live installed integrity, signing or qualification.
pub(crate) fn identity() -> Value {
    match selected() {
        Ok(Some(selection)) => {
            json!({"format":"compiled-publisher-selection.s1","state":"selected-production","originalBindingSha256":selection.binding_digest,"publicProjectionSha256":selection.public_projection_digest,"requirementSha256":hash(selection.requirement.as_bytes()),"limit":"Compiled build association only; no live authority from serialized metadata"})
        }
        Ok(None) => json!({"format":"compiled-publisher-selection.s1","state":"unselected"}),
        Err(_) => {
            json!({"format":"compiled-publisher-selection.s1","state":"invalid","limit":"Production must refuse"})
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[cfg(unix)]
    mod recipe {
        include!("publisher_recipe_tests.rs");
    }
    #[test]
    fn publisher_default_none_has_no_runtime_override_route() {
        if std::env::var_os("SYNTHETIC_PUBLISHER_OVERRIDE_CHILD").is_some() {
            assert!(selected().unwrap().is_none());
            assert_eq!(identity()["state"], "unselected");
            return;
        }
        assert!(COMPILED_PUBLISHER_REQUIREMENT.is_none());
        let result = std::process::Command::new(std::env::current_exe().unwrap())
            .args([
                "--exact",
                "publisher_selection::tests::publisher_default_none_has_no_runtime_override_route",
                "--nocapture",
            ])
            .env("SYNTHETIC_PUBLISHER_OVERRIDE_CHILD", "1")
            .env("CHIRALITY_PUBLISHER_SELECTION", "production-v1")
            .env(
                "CHIRALITY_PUBLISHER_INPUT_FILE",
                "/must-not-read/synthetic-publisher.json",
            )
            .env("CHIRALITY_PUBLISHER_INPUT_SHA256", "a".repeat(64))
            .env("CHIRALITY_ALLOW_UNVERIFIED", "1")
            .output()
            .unwrap();
        assert!(
            result.status.success(),
            "{}",
            String::from_utf8_lossy(&result.stderr)
        );
    }
}
