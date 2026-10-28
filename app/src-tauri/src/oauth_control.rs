//! Private child of hosting. Parent-owned pins admit original source fields before projection.
//! This controller neither authenticates pins nor sends frames or invokes native presentation.
use super::{EventPin, LoginSourcePin};
use serde_json::Value;
use std::sync::{
    atomic::{AtomicBool, Ordering},
    mpsc::{self, Receiver, Sender},
    Arc,
};
use std::time::Duration;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum OAuthMode {
    Chatgpt,
    DeviceCode,
}
impl OAuthMode {
    fn native_type(self) -> &'static str {
        match self {
            Self::Chatgpt => "chatgpt",
            Self::DeviceCode => "chatgptDeviceCode",
        }
    }
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum Phase {
    AwaitingWrite,
    AwaitingReply,
    Pending,
    Cancelling,
    CancellationUnknown,
    CompletedSuccess,
    CompletedFailure,
    Cancelled,
    Unknown,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum Limit {
    DifferentSource,
    InvalidShape,
    WrongMode,
    IdentityUnavailable,
    OtherLoginId,
    DuplicateReceipt,
    EarlyBufferFull,
    WriteNotFinished,
    SourceUnavailable,
    AlreadyPresented,
    NoPendingControl,
    CancelAlreadyAttempted,
    CancelOutcomeUnknown,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum WriteFinish {
    Written,
    Failed,
    SourceUnavailable,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum CancelFinish {
    Cancelled,
    NotFound,
    Unknown,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum RevocationReason {
    Completed,
    Cancelled,
    SourceLost,
    Dismissed,
    ControlDropped,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum NativePresentationResult {
    Presented,
    Dismissed,
    Unavailable,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum DeliveryResult {
    Presented,
    Dismissed,
    Unavailable,
    Revoked,
    CurrentSourceUnavailable,
}
#[derive(Clone, Debug, PartialEq)]
pub(super) struct Observation {
    pub(super) generation: Value,
    pub(super) rpc_id: Value,
    pub(super) pointer: String,
    pub(super) mode: OAuthMode,
    pub(super) phase: Phase,
    pub(super) write: Option<WriteFinish>,
    pub(super) limit: Option<Limit>,
    pub(super) presentation_available: bool,
    pub(super) cancel_available: bool,
    pub(super) original_control_material: &'static str,
}

// No Debug/Clone/Serde or raw getters on private native material.
enum Payload {
    Browser(String),
    Device {
        verification_url: String,
        user_code: String,
    },
}
pub(super) enum PresentationView<'a> {
    Browser {
        auth_url: &'a str,
    },
    Device {
        verification_url: &'a str,
        user_code: &'a str,
    },
}
pub(super) struct RevocationLease {
    active: Arc<AtomicBool>,
    receiver: Receiver<RevocationReason>,
}
impl RevocationLease {
    pub(super) fn is_active(&self) -> bool {
        self.active.load(Ordering::Acquire)
    }
    pub(super) fn wait(&self, timeout: Duration) -> Option<RevocationReason> {
        self.receiver.recv_timeout(timeout).ok()
    }
}
pub(super) struct PresentationPermit {
    payload: Payload,
    lease: RevocationLease,
}
impl PresentationPermit {
    /// Consume once outside every Host/controller/pipe lock. The native callback must monitor
    /// revocation and close/clear its native field while active; no public/JSON return of values.
    pub(super) fn deliver<F, C>(self, current_source: C, callback: F) -> DeliveryResult
    where
        C: FnOnce() -> Result<(), ()>,
        F: FnOnce(PresentationView<'_>, RevocationLease) -> NativePresentationResult,
    {
        if !self.lease.is_active() {
            return DeliveryResult::Revoked;
        }
        if current_source().is_err() {
            return DeliveryResult::CurrentSourceUnavailable;
        }
        if !self.lease.is_active() {
            return DeliveryResult::Revoked;
        }
        let view = match &self.payload {
            Payload::Browser(url) => PresentationView::Browser { auth_url: url },
            Payload::Device {
                verification_url,
                user_code,
            } => PresentationView::Device {
                verification_url,
                user_code,
            },
        };
        match callback(view, self.lease) {
            NativePresentationResult::Presented => DeliveryResult::Presented,
            NativePresentationResult::Dismissed => DeliveryResult::Dismissed,
            NativePresentationResult::Unavailable => DeliveryResult::Unavailable,
        }
        // Owned buffers drop on callback return (or unwind); no OS/browser erasure guarantee.
    }
}
pub(super) struct CancelPermit {
    login_id: String,
    active: Arc<AtomicBool>,
}
impl CancelPermit {
    /// Only the parent Host may serialize this borrow into its transient scoped frame.
    /// No controller lock or native/pipe IO belongs in the serialization callback.
    pub(super) fn with_login_id<C, F>(self, current_source: C, serialize: F) -> Result<(), Limit>
    where
        C: FnOnce() -> Result<(), ()>,
        F: FnOnce(&str),
    {
        if !self.active.load(Ordering::Acquire) {
            return Err(Limit::NoPendingControl);
        }
        current_source().map_err(|_| Limit::SourceUnavailable)?;
        if !self.active.load(Ordering::Acquire) {
            return Err(Limit::NoPendingControl);
        }
        serialize(&self.login_id);
        Ok(())
    }
}
struct PresentationSignal {
    active: Arc<AtomicBool>,
    sender: Sender<RevocationReason>,
}
struct Completion {
    login_id: String,
    success: bool,
    error_present: bool,
}
const MAX_EARLY_COMPLETIONS: usize = 8;
pub(super) struct Controller {
    generation: Value,
    rpc_id: Value,
    source_ref: String,
    mode: OAuthMode,
    phase: Phase,
    limit: Option<Limit>,
    write: Option<WriteFinish>,
    live: bool,
    login_id: Option<String>,
    payload: Option<Payload>,
    presentation_taken: bool,
    signal: Option<PresentationSignal>,
    control_active: Arc<AtomicBool>,
    cancel_attempted: bool,
    early: Vec<Completion>,
    last_receipt: Option<u64>,
}
impl std::fmt::Debug for Controller {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.observation().fmt(f)
    }
}
impl Controller {
    pub(super) fn begin(pin: &LoginSourcePin) -> Self {
        Self {
            generation: pin.generation.clone(),
            rpc_id: pin.rpc_id.clone(),
            source_ref: pin.request_ref.clone(),
            mode: pin.mode,
            phase: Phase::AwaitingWrite,
            limit: None,
            write: None,
            live: true,
            login_id: None,
            payload: None,
            presentation_taken: false,
            signal: None,
            control_active: Arc::new(AtomicBool::new(true)),
            cancel_attempted: false,
            early: Vec::new(),
            last_receipt: None,
        }
    }
    fn same_pin(&self, pin: &LoginSourcePin) -> bool {
        self.generation == pin.generation
            && self.rpc_id == pin.rpc_id
            && self.source_ref == pin.request_ref
            && self.mode == pin.mode
    }
    fn limited(&self, limit: Limit) -> Observation {
        let mut out = self.observation();
        out.limit = Some(limit);
        out
    }
    pub(super) fn observation(&self) -> Observation {
        Observation {
            generation: self.generation.clone(),
            rpc_id: self.rpc_id.clone(),
            pointer: format!("oauth-observation:{}", self.source_ref),
            mode: self.mode,
            phase: self.phase,
            write: self.write,
            limit: self.limit,
            presentation_available: self.live
                && self.phase == Phase::Pending
                && self.payload.is_some()
                && !self.presentation_taken,
            cancel_available: self.live
                && self.phase == Phase::Pending
                && self.login_id.is_some()
                && !self.cancel_attempted,
            original_control_material:
                "redacted/unavailable; observation pointer is not native control",
        }
    }
    fn revoke_presentation(&mut self, reason: RevocationReason) {
        self.payload = None;
        if let Some(signal) = self.signal.take() {
            signal.active.store(false, Ordering::Release);
            let _ = signal.sender.send(reason);
        }
    }
    fn finish(&mut self, phase: Phase, reason: RevocationReason) {
        self.phase = phase;
        self.limit = None;
        self.login_id = None;
        self.early.clear();
        self.control_active.store(false, Ordering::Release);
        self.revoke_presentation(reason);
    }
    fn apply_completion(&mut self, completion: Completion) -> bool {
        if self.login_id.as_deref() != Some(completion.login_id.as_str()) {
            return false;
        }
        let _error_present = completion.error_present; // Never retain native error text.
        self.finish(
            if completion.success {
                Phase::CompletedSuccess
            } else {
                Phase::CompletedFailure
            },
            RevocationReason::Completed,
        );
        true
    }
    /// Parent passes original RESULT object, already matched/schema-validated for this start pin.
    /// Local type checks defend the private subset; they do not replace native source admission.
    pub(super) fn start_response(
        &mut self,
        pin: &LoginSourcePin,
        original_result: &Value,
    ) -> Observation {
        if !self.same_pin(pin) {
            return self.limited(Limit::DifferentSource);
        }
        if !self.live {
            return self.limited(Limit::SourceUnavailable);
        }
        if self.login_id.is_some()
            || matches!(
                self.phase,
                Phase::CompletedSuccess | Phase::CompletedFailure | Phase::Cancelled
            )
        {
            return self.limited(Limit::NoPendingControl);
        }
        if original_result.get("type").and_then(Value::as_str) != Some(self.mode.native_type()) {
            return self.limited(Limit::WrongMode);
        }
        let Some(id) = original_result.get("loginId").and_then(Value::as_str) else {
            return self.limited(Limit::InvalidShape);
        };
        let payload = match self.mode {
            OAuthMode::Chatgpt => {
                let Some(url) = original_result.get("authUrl").and_then(Value::as_str) else {
                    return self.limited(Limit::InvalidShape);
                };
                Payload::Browser(url.into())
            }
            OAuthMode::DeviceCode => {
                let (Some(url), Some(code)) = (
                    original_result
                        .get("verificationUrl")
                        .and_then(Value::as_str),
                    original_result.get("userCode").and_then(Value::as_str),
                ) else {
                    return self.limited(Limit::InvalidShape);
                };
                Payload::Device {
                    verification_url: url.into(),
                    user_code: code.into(),
                }
            }
        };
        self.login_id = Some(id.into());
        self.payload = Some(payload);
        if self.write == Some(WriteFinish::Written) {
            self.phase = Phase::Pending;
        }
        if self.write == Some(WriteFinish::Failed) {
            self.phase = Phase::Unknown;
            self.payload = None;
        }
        if self.write == Some(WriteFinish::Written) {
            self.settle_early();
        }
        if self.limit == Some(Limit::EarlyBufferFull) && self.phase == Phase::Pending {
            self.phase = Phase::Unknown;
            self.payload = None;
        }
        self.observation()
    }
    fn settle_early(&mut self) {
        for completion in std::mem::take(&mut self.early) {
            if self.apply_completion(completion) {
                break;
            }
        }
    }
    /// Actual finished pipewrite/current source observation from Host, never predicted written.
    pub(super) fn write_completed(
        &mut self,
        pin: &LoginSourcePin,
        result: WriteFinish,
    ) -> Observation {
        if !self.same_pin(pin) {
            return self.limited(Limit::DifferentSource);
        }
        if !self.live {
            return self.limited(Limit::SourceUnavailable);
        }
        if self.write.is_some() {
            return self.limited(Limit::WriteNotFinished);
        }
        self.write = Some(result);
        match result {
            WriteFinish::Written => {
                if !matches!(
                    self.phase,
                    Phase::CompletedSuccess | Phase::CompletedFailure | Phase::Cancelled
                ) {
                    self.phase = if self.limit == Some(Limit::EarlyBufferFull) {
                        Phase::Unknown
                    } else if self.login_id.is_some() {
                        Phase::Pending
                    } else {
                        Phase::AwaitingReply
                    };
                    if self.login_id.is_some() {
                        self.settle_early();
                    }
                }
            }
            WriteFinish::Failed => {
                if !matches!(
                    self.phase,
                    Phase::CompletedSuccess | Phase::CompletedFailure | Phase::Cancelled
                ) {
                    self.phase = Phase::Unknown;
                    self.limit = Some(Limit::SourceUnavailable);
                }
                self.revoke_presentation(RevocationReason::SourceLost);
            }
            WriteFinish::SourceUnavailable => return self.source_lost(&pin.generation),
        }
        self.observation()
    }
    /// Original notification PARAMS only, under a parent-owned matched generation/receipt pin.
    pub(super) fn complete(&mut self, event: &EventPin, original_params: &Value) -> Observation {
        if self.generation != event.generation {
            return self.limited(Limit::DifferentSource);
        }
        if !self.live {
            return self.limited(Limit::SourceUnavailable);
        }
        if self
            .last_receipt
            .is_some_and(|p| event.receipt_position <= p)
        {
            return self.limited(Limit::DuplicateReceipt);
        }
        self.last_receipt = Some(event.receipt_position);
        let Some(success) = original_params.get("success").and_then(Value::as_bool) else {
            return self.limited(Limit::InvalidShape);
        };
        let Some(id) = original_params.get("loginId").and_then(Value::as_str) else {
            return self.limited(Limit::IdentityUnavailable);
        };
        let completion = Completion {
            login_id: id.into(),
            success,
            error_present: original_params.get("error").is_some_and(|e| !e.is_null()),
        };
        if self.write.is_none()
            || (self.login_id.is_none() && matches!(self.phase, Phase::AwaitingReply))
        {
            if self
                .login_id
                .as_deref()
                .is_some_and(|known| known != completion.login_id)
            {
                return self.limited(Limit::OtherLoginId);
            }
            if self.early.len() == MAX_EARLY_COMPLETIONS {
                self.phase = Phase::Unknown;
                self.limit = Some(Limit::EarlyBufferFull);
                return self.observation();
            }
            self.early.push(completion);
            return self.observation();
        }
        if self.apply_completion(completion) {
            self.observation()
        } else {
            self.limited(Limit::OtherLoginId)
        }
    }
    pub(super) fn take_presentation(
        &mut self,
        pin: &LoginSourcePin,
    ) -> Result<PresentationPermit, Limit> {
        if !self.same_pin(pin) {
            return Err(Limit::DifferentSource);
        }
        if !self.live {
            return Err(Limit::SourceUnavailable);
        }
        if self.write != Some(WriteFinish::Written) {
            return Err(Limit::WriteNotFinished);
        }
        if self.presentation_taken {
            return Err(Limit::AlreadyPresented);
        }
        if self.phase != Phase::Pending {
            return Err(Limit::NoPendingControl);
        }
        let payload = self.payload.take().ok_or(Limit::NoPendingControl)?;
        self.presentation_taken = true;
        let (sender, receiver) = mpsc::channel();
        let active = Arc::new(AtomicBool::new(true));
        self.signal = Some(PresentationSignal {
            active: active.clone(),
            sender,
        });
        Ok(PresentationPermit {
            payload,
            lease: RevocationLease { active, receiver },
        })
    }
    pub(super) fn dismiss_presentation(&mut self, pin: &LoginSourcePin) -> Observation {
        if !self.same_pin(pin) {
            return self.limited(Limit::DifferentSource);
        }
        self.revoke_presentation(RevocationReason::Dismissed);
        self.presentation_taken = true;
        self.observation() // No cancellation, ID teardown, signed-out or replacement inference.
    }
    pub(super) fn cancel_intent(&mut self, pin: &LoginSourcePin) -> Result<CancelPermit, Limit> {
        if !self.same_pin(pin) {
            return Err(Limit::DifferentSource);
        }
        if !self.live {
            return Err(Limit::SourceUnavailable);
        }
        if self.cancel_attempted {
            return Err(Limit::CancelAlreadyAttempted);
        }
        if self.phase != Phase::Pending || self.write != Some(WriteFinish::Written) {
            return Err(Limit::NoPendingControl);
        }
        let id = self
            .login_id
            .as_ref()
            .ok_or(Limit::NoPendingControl)?
            .clone();
        self.cancel_attempted = true;
        self.phase = Phase::Cancelling;
        Ok(CancelPermit {
            login_id: id,
            active: self.control_active.clone(),
        })
    }
    /// Host supplies this only after actual scoped/correlated native cancel status, or uncertainty.
    pub(super) fn cancel_completed(
        &mut self,
        pin: &LoginSourcePin,
        result: CancelFinish,
    ) -> Observation {
        if !self.same_pin(pin) {
            return self.limited(Limit::DifferentSource);
        }
        if !self.live {
            return self.limited(Limit::SourceUnavailable);
        }
        if !matches!(self.phase, Phase::Cancelling | Phase::CancellationUnknown) {
            return self.limited(Limit::NoPendingControl);
        }
        match result {
            CancelFinish::Cancelled | CancelFinish::NotFound => {
                self.finish(Phase::Cancelled, RevocationReason::Cancelled)
            }
            CancelFinish::Unknown => {
                self.phase = Phase::CancellationUnknown;
                self.limit = Some(Limit::CancelOutcomeUnknown);
                self.control_active.store(false, Ordering::Release);
                self.revoke_presentation(RevocationReason::SourceLost);
            }
        }
        self.observation()
    }
    pub(super) fn source_lost(&mut self, generation: &Value) -> Observation {
        if self.generation != *generation {
            return self.limited(Limit::DifferentSource);
        }
        self.live = false;
        if !matches!(
            self.phase,
            Phase::CompletedSuccess | Phase::CompletedFailure | Phase::Cancelled
        ) {
            self.phase = Phase::Unknown;
        }
        self.limit = Some(Limit::SourceUnavailable);
        self.login_id = None;
        self.early.clear();
        self.control_active.store(false, Ordering::Release);
        self.revoke_presentation(RevocationReason::SourceLost);
        self.observation()
    }
}
impl Drop for Controller {
    fn drop(&mut self) {
        self.control_active.store(false, Ordering::Release);
        self.revoke_presentation(RevocationReason::ControlDropped);
    }
}
