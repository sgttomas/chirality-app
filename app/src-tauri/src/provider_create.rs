//! One explicitly reviewed absent-ID addition, never a generic/upsert permit.
use super::{
    access_provider::{self, PrivateConfigPurpose, PrivateConfigReading},
    config_resource_continuation as continuation,
    provider_endpoint::{self, PrivateWrite, WriteFailure},
    *,
};
use crate::{AppState, PendingConfigResource};
use std::path::Path;
use tauri_plugin_dialog::MessageDialogResult;

pub(crate) const WRITE_ACTION: &str = "Add local provider";
const LIMIT: &str = "Provider Add unavailable; private values and native diagnostics withheld";
pub(crate) struct Offer {
    pending: PendingConfigResource,
    reading: PrivateConfigReading,
    target: PathBuf,
    version: String,
    id: String,
    name: String,
    endpoint: String,
    view: Value,
    pub(super) expires: std::time::Instant,
}
impl Offer {
    pub(crate) fn view(&self) -> Value {
        self.view.clone()
    }
    pub(crate) fn epoch(&self) -> &str {
        &self.pending.endpoint_epoch
    }
    pub(crate) fn remaining(&self) -> Duration {
        self.expires
            .saturating_duration_since(std::time::Instant::now())
    }
    pub(super) fn source_differs(
        &self,
        home: &Arc<crate::runtime_session::HomeSession>,
        generation: &Value,
        ready: bool,
    ) -> bool {
        !ready || !Arc::ptr_eq(home, &self.pending.home) || self.pending.generation != *generation
    }
    fn literal(&self) -> Value {
        json!({"name":self.name,"base_url":self.endpoint,"wire_api":"responses","requires_openai_auth":false})
    }
    fn current(&self, state: &AppState) -> Result<(), String> {
        if self.remaining().is_zero() {
            return Err(LIMIT.into());
        }
        provider_endpoint::context(state, &self.pending).map_err(|_| LIMIT)?;
        self.pending
            .home
            .host
            .check_provider_read(
                &self.pending.home.host.inner.0.lock().unwrap(),
                &self.reading.source,
                &self.pending.cwd,
            )
            .map_err(|_| LIMIT)?;
        state
            .desktop_setup
            .as_ref()
            .ok_or(LIMIT)?
            .try_lock()
            .map_err(|_| LIMIT)?
            .check_endpoint_before_write(&self.pending.slot)
            .map_err(|_| LIMIT.to_owned())
    }
    fn review(
        &self,
        state: &AppState,
        read: &PrivateConfigReading,
        reported: bool,
    ) -> Result<Value, String> {
        let receiving = self.pending.slot.receiving_config().map_err(|_| LIMIT)?;
        let layer =
            continuation::user_layer(&read.config, &self.target, &receiving).map_err(|_| LIMIT)?;
        access_provider::create_offer_fields(
            read,
            &state.project_context.view(),
            &self.id,
            &self.name,
            &self.endpoint,
            self.view["token"].as_str().ok_or(LIMIT)?,
            layer,
            reported,
        )
        .map_err(|_| LIMIT.to_owned())
    }
    fn reread_unchanged(&mut self, state: &AppState) -> Result<(), String> {
        self.current(state)?;
        let read = read(&self.pending)?;
        // A fresh receipt can replace the private read only at EXACT reviewed
        // version/configuration equality. It never rebases the Add intention.
        if read.config != self.reading.config {
            return Err(LIMIT.into());
        }
        self.review(state, &read, false)?;
        self.reading = read;
        self.current(state)
    }
}
fn read(pending: &PendingConfigResource) -> Result<PrivateConfigReading, String> {
    let reading = pending
        .home
        .host
        .private_provider_config_read(
            &pending.generation,
            &pending.cwd,
            pending
                .home
                .host_config
                .as_ref()
                .map_err(|_| LIMIT)?
                .wait_limit
                .min(Duration::from_secs(10)),
            PrivateConfigPurpose::CreateOffer,
        )
        .map_err(|_| LIMIT)?;
    pending
        .home
        .host
        .check_provider_read(
            &pending.home.host.inner.0.lock().unwrap(),
            &reading.source,
            &pending.cwd,
        )
        .map_err(|_| LIMIT)?;
    Ok(reading)
}
pub(crate) fn offer(
    state: &AppState,
    id: &str,
    name: &str,
    endpoint: &str,
) -> Result<Offer, String> {
    let pending = crate::begin_config_resource_continuation(state).map_err(|_| LIMIT)?;
    let reading = read(&pending)?;
    let target = pending.slot.target().map_err(|_| LIMIT)?;
    target.to_str().ok_or(LIMIT)?;
    let receiving = pending.slot.receiving_config().map_err(|_| LIMIT)?;
    let layer =
        continuation::user_layer(&reading.config, &target, &receiving).map_err(|_| LIMIT)?;
    let version = layer["version"].as_str().ok_or(LIMIT)?.to_owned();
    let token = opaque_id("provider-create-offer-").map_err(|_| LIMIT)?;
    let view = access_provider::create_offer_fields(
        &reading,
        &state.project_context.view(),
        id,
        name,
        endpoint,
        &token,
        layer,
        false,
    )
    .map_err(|_| LIMIT)?;
    let result = Offer {
        pending,
        reading,
        target,
        version,
        id: id.into(),
        name: name.into(),
        endpoint: endpoint.into(),
        view,
        expires: std::time::Instant::now() + provider_endpoint::OFFER_LIFETIME,
    };
    result.current(state)?;
    Ok(result)
}

// Fields and construction stay in this module. An endpoint permit cannot
// authorize this literal whole-object addition, or vice versa.
pub(super) struct CreateWrite<'a> {
    offer: &'a Offer,
    state: &'a AppState,
    window_current: &'a dyn Fn() -> Result<(), String>,
}
impl CreateWrite<'_> {
    pub(super) fn params(&self) -> Value {
        json!({"edits":[{"keyPath":format!("model_providers.{}",serde_json::to_string(&self.offer.id).unwrap()),"value":self.offer.literal(),"mergeStrategy":"replace"}],"filePath":self.offer.target,"expectedVersion":self.offer.version,"reloadUserConfig":false})
    }
    pub(super) fn check(&self, host: &Host, inner: &Inner) -> Result<(), String> {
        if !std::ptr::eq(host, self.offer.pending.home.host.as_ref())
            || self.state.endpoint_edits.lock().map_err(|_| LIMIT)?.epoch
                != self.offer.pending.endpoint_epoch
            || !Arc::ptr_eq(
                &self.state.homes.try_lock().map_err(|_| LIMIT)?.active(),
                &self.offer.pending.home,
            )
        {
            return Err(LIMIT.into());
        }
        host.check_provider_read(inner, &self.offer.reading.source, &self.offer.pending.cwd)
            .map_err(|_| LIMIT.to_owned())
    }
    pub(super) fn before_write(&self) -> Result<(), String> {
        self.offer.current(self.state)?;
        (self.window_current)()?;
        self.offer.current(self.state)
    }
    pub(super) fn mark_attempt(&self) -> Result<(), String> {
        self.state
            .desktop_setup
            .as_ref()
            .ok_or(LIMIT)?
            .try_lock()
            .map_err(|_| LIMIT)?
            .endpoint_write_attempt(&self.offer.pending.slot)
            .map_err(|_| LIMIT.to_owned())
    }
    pub(super) fn pending(&self) -> &PendingConfigResource {
        &self.offer.pending
    }
    pub(super) fn target(&self) -> &Path {
        &self.offer.target
    }
}
pub(super) fn withheld(frame: &Value) -> Value {
    let mut view = access_provider::withheld(frame);
    if view["error"].is_object() {
        view["error"]["message"]=json!("Native provider Add reported an error; private diagnostic withheld; filesystem effects unknown");
    }
    view
}
/// These are pinned diagnostic roles, not control events or server requests.
/// A notification has no RPC association; its raw body may include config/OS
/// metadata. Keep only its actual method on the private Add source.
pub(super) fn diagnostic(frame: &Value) -> Option<Value> {
    if frame.get("id").is_some() {
        return None;
    }
    let method = frame["method"].as_str()?;
    if !matches!(
        method,
        "configWarning"
            | "warning"
            | "guardianWarning"
            | "deprecationNotice"
            | "windows/worldWritableWarning"
    ) {
        return None;
    }
    Some(
        json!({"method":method,"params":{"privateProviderCreateWithheld":true,"observation":"Configuration diagnostic observed on private Add source; details and path withheld; no RPC association inferred"}}),
    )
}
pub(crate) fn save(
    state: &AppState,
    mut offer: Offer,
    window_current: impl Fn() -> Result<(), String>,
    before: impl FnOnce(&Value) -> Result<MessageDialogResult, String>,
    after: impl FnOnce(
        &continuation::Candidate,
        &Value,
    ) -> Result<Option<continuation::ReviewedCurrentObject>, ()>,
) -> Result<Value, String> {
    offer.current(state)?;
    if !crate::act_control::native_statement::chose(&before(&offer.view)?, WRITE_ACTION) {
        return Ok(json!({"state":"not-sent"}));
    }
    offer.reread_unchanged(state)?;
    let permit = CreateWrite {
        offer: &offer,
        state,
        window_current: &window_current,
    };
    let reply = match offer
        .pending
        .home
        .host
        .provider_write(&PrivateWrite::Create(&permit))
    {
        Ok(reply) => reply,
        Err(WriteFailure::NotSent) => return Ok(json!({"state":"refused-not-sent"})),
        Err(WriteFailure::Unknown) => return Ok(json!({"state":"unknown"})),
        Err(WriteFailure::ObservedSourceUnavailable { overridden }) => return Ok(json!({"state":if overridden {"overridden"} else {"write-observed-source-unconfirmed"}})),
    };
    // These fixed facts survive ALL subsequent fallible work, including loss
    // of a path needed to prepare the current-object readmission.
    let overridden = reply["status"] == "okOverridden";
    let version = reply["version"].as_str().ok_or(LIMIT)?.to_owned();
    drop(reply);
    let result = (|| -> Result<bool, String> {
        let receiving = offer.pending.slot.receiving_config().map_err(|_| LIMIT)?;
        let old_layer = continuation::user_layer(&offer.reading.config, &offer.target, &receiving)
            .map_err(|_| LIMIT)?["config"]
            .clone();
        let old_config = offer.reading.config["config"].clone();
        let target = offer.target.clone();
        let public = offer.view.clone();
        let (id, name, endpoint) = (offer.id, offer.name, offer.endpoint);
        drop(offer.reading);
        drop(offer.version);
        crate::complete_config_resource_continuation(state, offer.pending, |candidate| {
            if overridden || candidate.private_reading().1 != version {
                return Ok(None);
            }
            let read = candidate.private_source();
            let layer = continuation::user_layer(&read.config, &target, &receiving)?;
            let effects = access_provider::create_offer_fields(
                read,
                &state.project_context.view(),
                &id,
                &name,
                &endpoint,
                public["token"].as_str().ok_or(())?,
                layer,
                true,
            )
            .map_err(|_| ())?;
            let mut effective = read.config["config"].clone();
            let mut user = layer["config"].clone();
            effective["model_providers"]
                .as_object_mut()
                .ok_or(())?
                .remove(&id);
            user["model_providers"]
                .as_object_mut()
                .ok_or(())?
                .remove(&id);
            if effective != old_config || user != old_layer {
                return Ok(None);
            }
            drop((effective, user, old_config, old_layer, version));
            after(candidate, &effects)
        })
    })();
    Ok(
        json!({"state":if result==Ok(true) {"continued"}else if overridden{"overridden"}else{"write-observed-source-unconfirmed"}}),
    )
}
