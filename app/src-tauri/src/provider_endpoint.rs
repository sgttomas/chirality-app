//! Endpoint-only private offers and versioned writes. No renderer/native reply
//! can manufacture an offer, write context or current-object acceptance.
use super::{
    access_provider::{self, PrivateConfigPurpose, PrivateConfigReading},
    config_resource_continuation as continuation, *,
};
use crate::{AppState, PendingConfigResource};
use tauri_plugin_dialog::MessageDialogResult;

pub(crate) const WRITE_ACTION: &str = "Write endpoint change";
pub(crate) const OFFER_LIFETIME: Duration = Duration::from_secs(300);
pub(crate) fn expire_offer(
    controller: &Arc<Mutex<Controller>>,
    token: &str,
    wait: Duration,
) -> Result<(), String> {
    let receiver = {
        let mut c = controller.lock().map_err(|_| LIMIT)?;
        if let Some(offer) = c.offer.as_mut().filter(|o| o.view["token"] == token) {
            offer.expires = std::time::Instant::now() + wait;
        }
        if c.expiry_signal.is_none() {
            let (send, receive) = std::sync::mpsc::sync_channel(1);
            c.expiry_signal = Some(send);
            Some(receive)
        } else {
            None
        }
    };
    if let Some(receive) = receiver {
        let weak = Arc::downgrade(controller);
        std::thread::Builder::new()
            .name("endpoint-offer-expiry".into())
            .spawn(move || loop {
                let deadline = {
                    let Some(c) = weak.upgrade() else {
                        return;
                    };
                    let Ok(mut c) = c.lock() else {
                        return;
                    };
                    if c.offer
                        .as_ref()
                        .is_some_and(|o| o.expires <= std::time::Instant::now())
                    {
                        let _ = c.invalidate();
                        c.offer = None;
                    }
                    c.offer.as_ref().map(|o| o.expires)
                };
                match deadline {
                    Some(deadline) => match receive
                        .recv_timeout(deadline.saturating_duration_since(std::time::Instant::now()))
                    {
                        Err(std::sync::mpsc::RecvTimeoutError::Disconnected) => return,
                        _ => {}
                    },
                    None => {
                        if receive.recv().is_err() {
                            return;
                        }
                    }
                }
            })
            .map_err(|_| {
                if let Ok(mut c) = controller.lock() {
                    c.expiry_signal = None;
                    c.offer = None;
                }
                LIMIT.to_owned()
            })?;
    }
    if let Some(send) = controller.lock().map_err(|_| LIMIT)?.expiry_signal.as_ref() {
        let _ = send.try_send(());
    }
    Ok(())
}
#[derive(Default)]
pub(crate) struct Controller {
    pub(crate) epoch: String,
    pub(crate) offer: Option<Offer>,
    pub(crate) saving: Option<String>,
    expiry_signal: Option<std::sync::mpsc::SyncSender<()>>,
}
impl Controller {
    pub(crate) fn invalidate(&mut self) -> Result<(), String> {
        self.epoch = opaque_id("endpoint-source-epoch-").map_err(|_| LIMIT)?;
        self.offer = None;
        Ok(())
    }
    pub(crate) fn retire_source(
        &mut self,
        home: &Arc<crate::runtime_session::HomeSession>,
        generation: &Value,
        ready: bool,
    ) {
        if self.offer.as_ref().is_some_and(|o| {
            !ready || !Arc::ptr_eq(home, &o.pending.home) || o.pending.generation != *generation
        }) {
            let _ = self.invalidate();
            self.offer = None;
        }
    }
}
const LIMIT: &str = "Endpoint edit unavailable; private values and native diagnostics withheld";
pub(super) fn withheld(frame: &Value) -> Value {
    let mut view = access_provider::withheld(frame);
    if view["error"].is_object() {
        view["error"]["message"]=json!("Native endpoint write reported an error; private diagnostic withheld; filesystem effects unknown");
    }
    view
}
pub(crate) struct Offer {
    pending: PendingConfigResource,
    reading: PrivateConfigReading,
    version: String,
    target: PathBuf,
    id: String,
    endpoint: String,
    view: Value,
    expires: std::time::Instant,
}
pub(super) struct EndpointWrite<'a> {
    offer: &'a Offer,
    state: &'a AppState,
}
enum WriteFailure {
    NotSent,
    Unknown,
}
impl EndpointWrite<'_> {
    pub(super) fn params(&self) -> Value {
        json!({"edits":[{"keyPath":format!("model_providers.{}.base_url",serde_json::to_string(&self.offer.id).unwrap()),"value":self.offer.endpoint,"mergeStrategy":"replace"}],"filePath":self.offer.target,"expectedVersion":self.offer.version,"reloadUserConfig":false})
    }
    pub(super) fn check(&self, host: &Host, inner: &Inner) -> Result<(), String> {
        if !std::ptr::eq(host, self.offer.pending.home.host.as_ref()) {
            return Err(LIMIT.into());
        }
        if self.state.endpoint_edits.lock().map_err(|_| LIMIT)?.epoch
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
    pub(super) fn cwd(&self) -> &str {
        &self.offer.pending.cwd
    }
}
fn context(state: &AppState, pending: &PendingConfigResource) -> Result<(), String> {
    if state.endpoint_edits.lock().map_err(|_| LIMIT)?.epoch != pending.endpoint_epoch {
        return Err(LIMIT.into());
    }
    if !Arc::ptr_eq(
        &state.homes.try_lock().map_err(|_| LIMIT)?.active(),
        &pending.home,
    ) || pending.home.host.snapshot()["generation"] != pending.generation
    {
        return Err(LIMIT.into());
    }
    state
        .home_bootstrap
        .try_lock()
        .map_err(|_| LIMIT)?
        .as_ref()
        .map_err(|_| LIMIT)?
        .validate_binding(
            crate::home_resources::HomeClass::Account,
            pending.home.host_config.as_ref().map_err(|_| LIMIT)?,
        )
        .map_err(|_| LIMIT.to_owned())
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
    fn current(&self, state: &AppState) -> Result<(), String> {
        if self.expires <= std::time::Instant::now() {
            return Err(LIMIT.into());
        }
        context(state, &self.pending)?;
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
}
pub(crate) fn offer(state: &AppState, id: &str, endpoint: &str) -> Result<Offer, String> {
    let pending = crate::begin_config_resource_continuation(state).map_err(|_| LIMIT.to_owned())?;
    let host = &pending.home.host;
    let read = host
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
            PrivateConfigPurpose::EndpointOffer,
        )
        .map_err(|_| LIMIT.to_owned())?;
    host.check_provider_read(&host.inner.0.lock().unwrap(), &read.source, &pending.cwd)
        .map_err(|_| LIMIT.to_owned())?;
    let target = pending.slot.target().map_err(|_| LIMIT)?;
    target.to_str().ok_or(LIMIT)?; // No lossy native filePath or implicit fallback.
    let receiving = pending.slot.receiving_config().map_err(|_| LIMIT)?;
    state
        .desktop_setup
        .as_ref()
        .ok_or(LIMIT)?
        .try_lock()
        .map_err(|_| LIMIT)?
        .check_endpoint_before_write(&pending.slot)
        .map_err(|_| LIMIT)?;
    let layer = continuation::user_layer(&read.config, &target, &receiving).map_err(|_| LIMIT)?;
    let token = opaque_id("provider-endpoint-offer-").map_err(|_| LIMIT)?;
    let view = access_provider::endpoint_offer_fields(
        &read,
        &state.project_context.view(),
        id,
        endpoint,
        &token,
        layer,
    )
    .map_err(|_| LIMIT)?;
    let version = layer["version"].as_str().ok_or(LIMIT)?.to_owned();
    Ok(Offer {
        pending,
        reading: read,
        version,
        target,
        id: id.into(),
        endpoint: endpoint.into(),
        view,
        expires: std::time::Instant::now() + OFFER_LIFETIME,
    })
}

pub(crate) fn save(
    state: &AppState,
    offer: Offer,
    confirm_write: impl FnOnce(&Value) -> Result<MessageDialogResult, String>,
    confirm_source: impl FnOnce(
        &continuation::Candidate,
        &Value,
    ) -> Result<Option<continuation::ReviewedCurrentObject>, ()>,
) -> Result<Value, String> {
    offer.current(state)?;
    let result = confirm_write(&offer.view)?;
    if !crate::act_control::native_statement::chose(&result, WRITE_ACTION) {
        return Ok(json!({"state":"not-sent","message":"No endpoint write sent"}));
    }
    offer.current(state)?;
    let write = EndpointWrite {
        offer: &offer,
        state,
    };
    let reply = match offer.pending.home.host.endpoint_write(&write) {
        Ok(reply) => reply,
        Err(WriteFailure::NotSent) => {
            return Ok(
                json!({"state":"refused-not-sent","message":"Endpoint change refused before any write attempt"}),
            )
        }
        Err(WriteFailure::Unknown) => {
            return Ok(
                json!({"state":"unknown","message":"Endpoint write outcome unknown; no retry or source continuation"}),
            )
        }
    };
    let status = reply["status"].as_str().ok_or(LIMIT)?.to_owned();
    let version = reply["version"]
        .as_str()
        .filter(|s| !s.is_empty() && s.len() <= 4096)
        .ok_or(LIMIT)?
        .to_owned();
    if reply["filePath"].as_str() != offer.target.to_str() {
        return Ok(
            json!({"state":"unknown","message":"Write reply did not establish the expected target; no source continuation"}),
        );
    }
    drop(reply); // Raw override/error-capable body does not span the next question.

    // endpoint_write already validated the native schema, target and source.
    // Later filesystem/read/review/publication failures cannot erase those
    // fixed write facts, and cannot establish source continuation either.
    let unconfirmed = if status == "okOverridden" {
        "overridden"
    } else {
        "write-observed-source-unconfirmed"
    };
    let mut observed = false;
    let result = (|| -> Result<bool, String> {
        let public = offer.view.clone();
        let provider = offer.id.clone();
        let endpoint = offer.endpoint.clone();
        let receiving = offer.pending.slot.receiving_config().map_err(|_| LIMIT)?;
        let target = offer.target.clone();
        let old_config = offer.reading.config["config"].clone();
        let old_layer = continuation::user_layer(&offer.reading.config, &target, &receiving)
            .map_err(|_| LIMIT)?["config"]
            .clone();
        drop(offer.reading);
        drop(offer.version);
        crate::complete_config_resource_continuation(state, offer.pending, |candidate| {
            let (reading, native_version) = candidate.private_reading();
            if native_version != version
                || reading["config"]["model_providers"][&provider]["base_url"] != endpoint
                || status != "ok"
            {
                return Ok(None);
            }
            // Reapply the same response-wide publication predicate to the new
            // private source before presenting any current-object review effects.
            let layer = continuation::user_layer(reading, &target, &receiving)?;
            // Reported sibling settings must be unchanged. This private comparison
            // is not byte preservation, a public fingerprint or writer provenance.
            let mut before = old_config;
            let mut after = reading["config"].clone();
            before["model_providers"][&provider]["base_url"] = Value::Null;
            after["model_providers"][&provider]["base_url"] = Value::Null;
            let mut before_layer = old_layer;
            let mut after_layer = layer["config"].clone();
            before_layer["model_providers"][&provider]["base_url"] = Value::Null;
            after_layer["model_providers"][&provider]["base_url"] = Value::Null;
            if before != after || before_layer != after_layer {
                return Ok(None);
            }
            drop((before, after, before_layer, after_layer, version));
            let post_view = access_provider::endpoint_offer_fields(
                candidate.private_source(),
                &state.project_context.view(),
                &provider,
                &endpoint,
                public["token"].as_str().ok_or(())?,
                layer,
            )
            .map_err(|_| ())?;
            observed = true;
            confirm_source(candidate, &post_view)
        })
    })();
    match result {
        Ok(true) => Ok(
            json!({"state":"continued","message":"Endpoint write and current source continuation observed; current choices remain unchanged"}),
        ),
        Ok(false) => Ok(
            json!({"state":unconfirmed,"message":"Write observed; the current source has not been continued","endpointRereadMatched":observed}),
        ),
        Err(_) => Ok(
            json!({"state":unconfirmed,"message":"Write observed; current source continuation unavailable or unknown; no retry"}),
        ),
    }
}

impl Host {
    fn endpoint_write(&self, write: &EndpointWrite<'_>) -> Result<Value, WriteFailure> {
        write.before_write().map_err(|_| WriteFailure::NotSent)?;
        let params = write.params();
        Self::validate_native_result("ConfigBatchWriteParams", &params)
            .map_err(|_| WriteFailure::NotSent)?;
        let source = self
            .request_begin_with_access_offer_guarded(
                "config/batchWrite",
                params,
                json!({"kind":"person-directed","name":"provider-endpoint-change"}),
                false,
                Some(&write.offer.pending.generation),
                false,
                None,
                None,
                None,
                None,
                true,
                None,
                None,
                Some(write),
            )
            .map_err(|_| WriteFailure::NotSent)?;
        let failure = || {
            if source.write_attempt_observed() == Some(false) {
                WriteFailure::NotSent
            } else {
                WriteFailure::Unknown
            }
        };
        #[cfg(test)]
        if let Some(hook) = self.before_provider_wait.lock().unwrap().as_ref() {
            hook(self, &source);
        }
        let received = source.receiver.lock().unwrap().recv_timeout(
            write
                .offer
                .pending
                .home
                .host_config
                .as_ref()
                .map_err(|_| failure())?
                .wait_limit
                .min(Duration::from_secs(10)),
        );
        self.delegation_wait_ended(&source);
        while source.receiver.lock().unwrap().try_recv().is_ok() {}
        let frame = received.map_err(|_| failure())?;
        if frame.get("id") != Some(source.request_id())
            || frame.get("method").is_some()
            || frame.get("error").is_some()
        {
            return Err(failure());
        }
        let result = frame.get("result").ok_or_else(failure)?;
        Self::validate_native_result("ConfigWriteResponse", result).map_err(|_| failure())?;
        let inner = self.inner.0.lock().unwrap();
        let e = inner
            .source_requests
            .get(&source.request_id().to_string())
            .ok_or(WriteFailure::Unknown)?;
        if inner.generation != *source.generation()
            || inner.state != "ready"
            || inner.server_requests.is_closed(source.generation())
            || e.request.request_ref() != source.request_ref()
            || !e.private_config
            || !e.written
            || e.write_error.is_some()
            || e.source_limit.is_some()
            || e.write_attempt_in_progress
            || e.response_position
                .is_none_or(|position| position <= e.turn_model_cut)
            || e.source_pipe
                .is_none_or(|(epoch, _)| epoch != inner.attachment_pipe_epoch)
        {
            return Err(WriteFailure::Unknown);
        }
        if result["version"]
            .as_str()
            .is_none_or(|s| s.is_empty() || s.len() > 4096)
            || result["filePath"].as_str() != write.offer.target.to_str()
        {
            return Err(WriteFailure::Unknown);
        }
        Ok(result.clone())
    }
}
