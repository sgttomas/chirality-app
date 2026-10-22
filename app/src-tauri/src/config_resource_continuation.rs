//! Private, one-shot reviewed-current-object readmission. No IPC, editor, native
//! writer, person-act record or provider admission is issued here. Native facts
//! describe the checked object; they cannot attest who replaced it.
use super::{
    access_provider::{PrivateConfigPurpose, PrivateConfigReading},
    Host,
};
use crate::desktop_startup::{ConfigSlotPreflight, DesktopSetup};
use serde_json::Value;
use std::{
    path::Path,
    sync::{Arc, Mutex},
    time::Duration,
};

const REFUSED: &str = "Config continuation refused; checked source/review unavailable or changed; no in-memory continuation";
#[cfg(test)]
pub(crate) use super::access_provider::tests::Peer as TestPeer;

// No Serde, Clone, public pointer, Boolean or renderer constructor.
pub(crate) struct ReviewedCurrentObject {
    token: String,
}
pub(crate) struct Candidate {
    token: String,
    reading: PrivateConfigReading,
    native_version: String,
}
impl Candidate {
    /// A trusted injected review must explicitly concern this candidate. Future
    /// real person/native presentation wiring is not provided by this core.
    pub(crate) fn accept_checked_current_object(&self) -> ReviewedCurrentObject {
        ReviewedCurrentObject {
            token: self.token.clone(),
        }
    }
    /// Private review basis only, never a DTO or publication permission. The
    /// borrow cannot outlive this one-shot candidate/request lifetime.
    pub(crate) fn private_reading(&self) -> (&Value, &str) {
        (&self.reading.config, &self.native_version)
    }
    #[cfg(test)]
    pub(crate) fn nonexact_for_test(&self) -> ReviewedCurrentObject {
        ReviewedCurrentObject {
            token: "different invented candidate".into(),
        }
    }
}

fn user_version(read: &Value, target: &Path) -> Result<String, ()> {
    let layers = read.get("layers").and_then(Value::as_array).ok_or(())?;
    if layers.len() > 128 {
        return Err(());
    }
    let mut version = None;
    for layer in layers {
        if layer["name"]["type"] != "user" || !layer["name"]["profile"].is_null() {
            continue;
        }
        let file = Path::new(layer["name"]["file"].as_str().ok_or(())?);
        // Accept only this canonical target, not a matching string/hash version
        // selected from another layer or an alias of the same inode.
        if file != target
            || std::fs::canonicalize(file).map_err(|_| ())? != target
            || !layer["disabledReason"].is_null()
            || version.is_some()
        {
            return Err(());
        }
        let value = layer["version"]
            .as_str()
            .filter(|v| !v.is_empty() && v.len() <= 4096)
            .ok_or(())?;
        version = Some(value.to_owned());
    }
    version.ok_or(())
}

fn current(host: &Host, read: &PrivateConfigReading) -> Result<(), String> {
    let inner = host.inner.0.lock().map_err(|_| REFUSED)?;
    host.check_provider_read(&inner, &read.source, &read.cwd)
        .map_err(|_| REFUSED.into())
}

/// Same private production core used by the Root adapter and joined fixtures.
/// Neither the private native wait nor the injected review holds desktop/Host
/// locks. Dropping/declining/errors consume this one-shot preflight.
pub(crate) fn complete(
    desktop: &Arc<Mutex<DesktopSetup>>,
    preflight: ConfigSlotPreflight,
    host: &Host,
    generation: &Value,
    cwd: &str,
    wait: Duration,
    context_current: impl Fn() -> Result<(), String>,
    review: impl FnOnce(&Candidate) -> Result<Option<ReviewedCurrentObject>, ()>,
) -> Result<bool, String> {
    let refused = || REFUSED.to_owned();
    context_current().map_err(|_| refused())?;
    let object = desktop
        .try_lock()
        .map_err(|_| refused())?
        .observe_config_candidate(&preflight)
        .map_err(|_| refused())?;
    let reading = host
        .private_provider_config_read(
            generation,
            cwd,
            wait,
            PrivateConfigPurpose::ConfigContinuation,
        )
        .map_err(|_| refused())?;
    current(host, &reading)?;
    object.check().map_err(|_| refused())?;
    desktop
        .try_lock()
        .map_err(|_| refused())?
        .check_config_candidate(&preflight, &object)
        .map_err(|_| refused())?;
    let native_version = user_version(&reading.config, &object.path().map_err(|_| refused())?)
        .map_err(|_| refused())?;
    let candidate = Candidate {
        token: crate::util::opaque_id("config-current-object-").map_err(|_| refused())?,
        reading,
        native_version,
    };
    let decision = review(&candidate).map_err(|_| refused())?;
    let Some(decision) = decision else {
        return Ok(false);
    };
    if decision.token != candidate.token {
        return Err(refused());
    }
    context_current().map_err(|_| refused())?;
    current(host, &candidate.reading)?;
    desktop
        .try_lock()
        .map_err(|_| refused())?
        .check_config_candidate(&preflight, &object)
        .map_err(|_| refused())?;
    // Native version/raw config remain transient for this exact review. They
    // are not serialized, returned, hashed, logged or admission capabilities.
    let _version = &candidate.native_version;
    desktop
        .try_lock()
        .map_err(|_| refused())?
        .publish_config_continuation(preflight, object, || {
            context_current().map_err(|_| refused())?;
            current(host, &candidate.reading)
        })
        .map_err(|error| {
            if error.starts_with("Config request publication outcome unknown;") {
                error
            } else {
                refused()
            }
        })?;
    Ok(true)
}
