//! Explicit, private config/read -> two allowlisted supplier-reported settings and
//! the default provider the person's own settings name.
//! No auth files, requirements, config writes or inferred defaults/custody.
use super::access_provider::{PrivateConfigPurpose, PrivateConfigReading, PrivateReflections};
use super::*;

const LIMIT: &str = "Effective access settings unavailable; original source changed or private reading could not be established. Private diagnostics withheld.";

// Fixed categories only. Never publish native paths, profile names, versions,
// domain/key, enterprise identifiers, disabled reasons or arbitrary layer data.
fn source_kind(name: &Value) -> Option<&'static str> {
    match name["type"].as_str()? {
        "packagedDefaults" => Some("packagedDefaults"),
        "mdm" => Some("mdm"),
        "system" => Some("system"),
        "enterpriseManaged" => Some("enterpriseManaged"),
        "user" => Some("user"),
        "project" => Some("project"),
        "sessionFlags" => Some("sessionFlags"),
        "legacyManagedConfigTomlFromFile" => Some("legacyManagedConfigTomlFromFile"),
        "legacyManagedConfigTomlFromMdm" => Some("legacyManagedConfigTomlFromMdm"),
        _ => None,
    }
}

fn setting(read: &Value, key: &str, path: &[&str]) -> Value {
    let at = |config: &Value| path.iter().fold(config, |v, part| &v[*part]).clone();
    let value = at(&read["config"]);
    let valid = if key == "cli_auth_credentials_store" {
        matches!(
            value.as_str(),
            Some("file" | "keyring" | "auto" | "ephemeral")
        )
    } else {
        value.is_boolean()
    };
    if !valid {
        return json!({"state":"unknown","value":null,"source":{"state":"unknown"}});
    }
    let mut source = json!({"state":"unknown"});
    // An exact leaf origin, or the enclosing features table's reported origin.
    // Both require a unique enabled layer with identical metadata AND value.
    let origin_key = if read["origins"].get(key).is_some() {
        key
    } else {
        path[0]
    };
    if let (Some(origin), Some(layers)) =
        (read["origins"].get(origin_key), read["layers"].as_array())
    {
        let matching: Vec<_> = layers
            .iter()
            .enumerate()
            .filter(|(_, layer)| {
                layer["name"] == origin["name"]
                    && layer["version"] == origin["version"]
                    && layer["disabledReason"].is_null()
                    && at(&layer["config"]) == value
            })
            .collect();
        if let [(index, layer)] = matching.as_slice() {
            if let Some(kind) = source_kind(&layer["name"]) {
                source = json!({"state":"reported","kind":kind,"layerIndex":index,"originKey":origin_key});
            }
        }
    }
    json!({"state":"reported","value":value,"source":source})
}

/// What the person's own Codex settings name as their default provider: the `model_provider` field
/// of the one enabled user layer's configuration, a displayable identifier only. "none" only when
/// that layer's configuration is an object without the field (or with it null); "unknown" when no
/// single enabled user layer was reported, its configuration is not an object, or the name is not
/// displayable. Never the effective value: in the account home that is the App's own session setting.
fn user_layer_model_provider(read: &Value) -> Value {
    let unknown = || json!({"state":"unknown","value":null});
    let Some(layers) = read["layers"].as_array() else { return unknown(); };
    let user: Vec<&Value> = layers.iter().filter(|l| l["name"]["type"] == "user" && l["disabledReason"].is_null()).collect();
    let [layer] = user.as_slice() else { return unknown(); };
    let Some(config) = layer["config"].as_object() else { return unknown(); };
    match config.get("model_provider").unwrap_or(&Value::Null) {
        Value::Null => json!({"state":"none","value":null}),
        Value::String(name) if name.len() <= 64 && name.chars().next().is_some_and(|c| c.is_ascii_alphabetic())
            && name.chars().all(|c| c.is_ascii_alphanumeric() || matches!(c, '.' | '_' | '-')) => json!({"state":"reported","value":name}),
        _ => unknown(),
    }
}

fn project(read: &PrivateConfigReading, class: &str) -> Result<Value, String> {
    let reflections = PrivateReflections::new(&read.config).map_err(|_| LIMIT.to_owned())?;
    let view = json!({
        "state":"observed",
        "scope":{"generation":read.source.generation(),"modeHomeClass":class,"readRevision":read.source.request_ref},
        "credentialStore":setting(&read.config,"cli_auth_credentials_store", &["cli_auth_credentials_store"]),
        "plugins":setting(&read.config,"features.plugins", &["features","plugins"]),
        "personDefaultProvider":user_layer_model_provider(&read.config)
    });
    if reflections.excludes_value(&view) {
        return Err(LIMIT.into());
    }
    Ok(view)
}

impl Host {
    pub(crate) fn effective_access_settings_read(
        &self,
        generation: &Value,
        cwd: &str,
        class: &str,
    ) -> Result<Value, String> {
        self.effective_access_settings_read_within(generation, cwd, class, Duration::from_secs(10))
    }
    pub(crate) fn effective_access_settings_read_within(
        &self,
        generation: &Value,
        cwd: &str,
        class: &str,
        wait: Duration,
    ) -> Result<Value, String> {
        if !matches!(class, "account" | "api-key") {
            return Err(LIMIT.into());
        }
        let read = self
            .private_provider_config_read(
                generation,
                cwd,
                wait,
                PrivateConfigPurpose::AccessSettings,
            )
            .map_err(|_| LIMIT.to_owned())?;
        self.check_provider_read(&self.inner.0.lock().unwrap(), &read.source, cwd)
            .map_err(|_| LIMIT.to_owned())?;
        let view = project(&read, class)?;
        self.check_provider_read(&self.inner.0.lock().unwrap(), &read.source, cwd)
            .map_err(|_| LIMIT.to_owned())?;
        Ok(view)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn access_settings_user_layer_model_provider_is_none_only_for_an_object_configuration_without_one() {
        let read = |config: Value| user_layer_model_provider(&json!({"layers":[{"name":{"type":"user"},"disabledReason":null,"config":config}]}));
        assert_eq!(read(json!({})), json!({"state":"none","value":null}));
        assert_eq!(read(json!({"model_provider":null})), json!({"state":"none","value":null}));
        assert_eq!(read(json!({"model_provider":"local-lab"})), json!({"state":"reported","value":"local-lab"}));
        for config in [Value::Null, json!("model_provider = \"x\""), json!([]), json!(3), json!(true)] {
            assert_eq!(read(config.clone()), json!({"state":"unknown","value":null}), "{config}");
        }
        assert_eq!(user_layer_model_provider(&json!({"layers":[{"name":{"type":"user"},"disabledReason":null}]})), json!({"state":"unknown","value":null}), "no configuration at all");
    }
}
