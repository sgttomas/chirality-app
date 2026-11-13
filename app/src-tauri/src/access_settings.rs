//! Explicit, private config/read -> two allowlisted supplier-reported settings.
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

fn project(read: &PrivateConfigReading, class: &str) -> Result<Value, String> {
    let reflections = PrivateReflections::new(&read.config).map_err(|_| LIMIT.to_owned())?;
    let view = json!({
        "state":"observed",
        "scope":{"generation":read.source.generation(),"modeHomeClass":class,"readRevision":read.source.request_ref},
        "credentialStore":setting(&read.config,"cli_auth_credentials_store", &["cli_auth_credentials_store"]),
        "plugins":setting(&read.config,"features.plugins", &["features","plugins"])
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
            .map_err(|e| crate::hosting::reading_gate::reading_or(e, || LIMIT.to_owned()))?;
        self.check_provider_read(&self.inner.0.lock().unwrap(), &read.source, cwd)
            .map_err(|_| LIMIT.to_owned())?;
        let view = project(&read, class)?;
        self.check_provider_read(&self.inner.0.lock().unwrap(), &read.source, cwd)
            .map_err(|_| LIMIT.to_owned())?;
        Ok(view)
    }
}
