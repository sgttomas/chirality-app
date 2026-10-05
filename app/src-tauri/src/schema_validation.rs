//! W-1 validation of complete RS entries using maintained embedded schemas.
//! No repository paths, network, file retrieval, or unchecked fallback at runtime.
use jsonschema::{Draft, Registry, Retrieve, Uri, Validator};
use serde_json::Value;
use std::sync::OnceLock;

pub const RS_ID: &str = "urn:chirality:app-v4:del-04-03:rs-record:0.1";
pub const RESOURCES: &[(&str, &str)] = &[
    (
        "RS_RECORD.schema.json",
        include_str!("../schemas/RS_RECORD.schema.json"),
    ),
    (
        "checkpoint-record-entries.schema.json",
        include_str!("../schemas/checkpoint-record-entries.schema.json"),
    ),
    (
        "ACT_POLICY_CLASS_RECORD.schema.json",
        include_str!("../schemas/ACT_POLICY_CLASS_RECORD.schema.json"),
    ),
    (
        "AS_SETTINGS_IN.schema.json",
        include_str!("../schemas/AS_SETTINGS_IN.schema.json"),
    ),
    (
        "aac.offer.schema.json",
        include_str!("../schemas/aac.offer.schema.json"),
    ),
    (
        "aac.capture-evidence.schema.json",
        include_str!("../schemas/aac.capture-evidence.schema.json"),
    ),
];
const REQUIRED_IDS: &[&str] = &[
    RS_ID,
    "chirality:del-02-03/exec-checkpoint-entry-bodies/proposed-0.7",
    "urn:chirality:app-v4:del-04-01:policy-class-record:0.1",
    "urn:chirality:app-v4:del-04-02:settings-in:0.1",
];

const PACKAGE_REF: &str =
    "chirality:del-02-03/exec-checkpoint-entry-bodies/proposed-0.7#/$defs/decisionPackageFile";
const OFFER_ID: &str = "urn:chirality:app-v4:del-01-04:aac:offer:0.3";
const CAPTURE_ID: &str = "urn:chirality:app-v4:del-01-04:aac:capture-evidence:0.3";

struct NoRetrieval;
impl Retrieve for NoRetrieval {
    fn retrieve(
        &self,
        uri: &Uri<String>,
    ) -> Result<Value, Box<dyn std::error::Error + Send + Sync>> {
        Err(std::io::Error::new(
            std::io::ErrorKind::NotFound,
            format!("schema retrieval disabled: {uri}"),
        )
        .into())
    }
}

/// Shared declared-ID registry: no rewriting or automatic retrieval at either stage.
pub(crate) fn compile_targets(
    resources: &[(&str, &str)],
    required: &[&str],
    targets: &[&str],
) -> Result<Vec<Validator>, String> {
    let mut schemas = Vec::new();
    let mut ids = std::collections::HashSet::new();
    for (name, text) in resources {
        let schema: Value =
            serde_json::from_str(text).map_err(|e| format!("schema {name}: {e}"))?;
        let id = schema
            .get("$id")
            .and_then(Value::as_str)
            .ok_or_else(|| format!("schema {name}: missing $id"))?
            .to_owned();
        if !ids.insert(id.clone()) {
            return Err(format!("duplicate schema ID: {id}"));
        }
        if schema.get("$schema").and_then(Value::as_str)
            != Some("https://json-schema.org/draft/2020-12/schema")
        {
            return Err(format!("schema {name}: expected JSON Schema 2020-12"));
        }
        schemas.push((id, schema));
    }
    for id in required {
        if !ids.contains(*id) {
            return Err(format!("required schema unavailable: {id}"));
        }
    }
    let mut registry = Registry::new()
        .draft(Draft::Draft202012)
        .retriever(NoRetrieval);
    for (id, schema) in &schemas {
        registry = registry
            .add(id, schema.clone())
            .map_err(|e| format!("schema registry: {e}"))?;
    }
    let registry = registry
        .prepare()
        .map_err(|e| format!("schema registry: {e}"))?;
    let options = jsonschema::options()
        .with_draft(Draft::Draft202012)
        .with_registry(&registry)
        .offline();
    for (id, schema) in &schemas {
        options
            .build_map(schema)
            .map_err(|e| format!("schema build {id}: {e}"))?;
    }
    targets
        .iter()
        .map(|target| {
            options
                .build(&serde_json::json!({"$ref": target}))
                .map_err(|e| format!("schema target {target}: {e}"))
        })
        .collect()
}

pub struct RecordValidator(Validator);
impl RecordValidator {
    /// Compile by declared IDs only. Every resource is required and every reachable
    /// subschema is compiled, including definitions outside the root entry path.
    pub fn from_resources(resources: &[(&str, &str)]) -> Result<Self, String> {
        let mut validators = compile_targets(resources, REQUIRED_IDS, &[RS_ID])?;
        Ok(Self(validators.remove(0)))
    }

    pub fn validate(&self, entry: &Value) -> Result<(), String> {
        self.0
            .validate(entry)
            .map_err(|e| format!("RS W-1 validation refused: {e}"))
    }
}

/// Setup failure is retained and refuses every append; it never falls back.
pub fn bundled() -> Result<&'static RecordValidator, String> {
    static VALIDATOR: OnceLock<Result<RecordValidator, String>> = OnceLock::new();
    VALIDATOR
        .get_or_init(|| RecordValidator::from_resources(RESOURCES))
        .as_ref()
        .map_err(Clone::clone)
}

struct ActValidators {
    package: Validator,
    offer: Validator,
    capture: Validator,
}
impl ActValidators {
    fn from_resources(resources: &[(&str, &str)]) -> Result<Self, String> {
        let mut required = REQUIRED_IDS.to_vec();
        required.extend([OFFER_ID, CAPTURE_ID]);
        let mut validators =
            compile_targets(resources, &required, &[PACKAGE_REF, OFFER_ID, CAPTURE_ID])?
                .into_iter();
        Ok(Self {
            package: validators.next().unwrap(),
            offer: validators.next().unwrap(),
            capture: validators.next().unwrap(),
        })
    }
}
fn act_validators() -> Result<&'static ActValidators, String> {
    static VALIDATORS: OnceLock<Result<ActValidators, String>> = OnceLock::new();
    VALIDATORS
        .get_or_init(|| ActValidators::from_resources(RESOURCES))
        .as_ref()
        .map_err(Clone::clone)
}

/// Validate the complete source package file against EXEC's declared definition.
pub fn validate_package(package: &Value) -> Result<(), String> {
    act_validators()?
        .package
        .validate(package)
        .map_err(|e| format!("decision package validation refused: {e}"))
}
/// Validate the authoritative composed offer before presentation.
pub fn validate_offer(offer: &Value) -> Result<(), String> {
    act_validators()?
        .offer
        .validate(offer)
        .map_err(|e| format!("AAC offer validation refused: {e}"))
}
/// Validate the native capture object before persistence or RS append.
pub fn validate_capture(capture: &Value) -> Result<(), String> {
    act_validators()?
        .capture
        .validate(capture)
        .map_err(|e| format!("AAC capture validation refused: {e}"))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn act_targets_refuse_unavailable_or_invalid_aac_resources() {
        for omit in [4, 5] {
            let mut resources = RESOURCES.to_vec();
            resources.remove(omit);
            assert!(ActValidators::from_resources(&resources).is_err());
        }
        let mut invalid = RESOURCES.to_vec();
        invalid[5].1 = "{";
        assert!(ActValidators::from_resources(&invalid).is_err());
        let mut schema: Value = serde_json::from_str(RESOURCES[4].1).unwrap();
        schema["$defs"]["unavailable"] = serde_json::json!({"$ref": "https://example.invalid/aac"});
        let text = serde_json::to_string(&schema).unwrap();
        invalid[5] = RESOURCES[5];
        invalid[4].1 = &text;
        assert!(ActValidators::from_resources(&invalid).is_err());
    }
}
