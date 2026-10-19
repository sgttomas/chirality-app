//! One original Continue-as send, retained only in this App process. Public
//! handoff IDs select existing private custody; they cannot supply a target,
//! restore a source, replace a role or reconstruct an original sender.
use super::*;
use crate::hosting::{HandoffSendObservation, Host, SourceRequest};
use crate::runtime_session::{HomeRouter, WorkflowRootSession};
use std::sync::{Arc, Mutex};
use std::time::Duration;

#[derive(Clone, Copy)]
enum Confirmed {
    Sent,
    NativeFailed,
}

#[derive(Clone)]
pub(super) struct Attempt {
    reference: String,
    generation: Value,
    thread: String,
    text: String,
    owner: Option<Arc<Host>>,
    source: Option<SourceRequest>,
    in_flight: bool,
    // Set only after the producer completed a branch before any dispatch.
    no_attempt: Option<String>,
    // Bounded observed fact only; raw native response stays in its Host source.
    confirmed: Option<Confirmed>,
}

impl Attempt {
    pub(super) fn draft_text(&self) -> &str {
        &self.text
    }
    fn observation(&self) -> HandoffSendObservation {
        if let Some(source) = &self.source {
            let observed = self
                .owner
                .as_ref()
                .map(|owner| {
                    owner.handoff_send_observation(
                        source,
                        &self.generation,
                        &self.thread,
                        &self.text,
                    )
                })
                .unwrap_or_else(|| {
                    HandoffSendObservation::Unknown("Original Host unavailable".into())
                });
            // A source observation cannot erase an already observed response.
            if matches!(observed, HandoffSendObservation::Unknown(_)) {
                return match self.confirmed {
                    Some(Confirmed::Sent) => HandoffSendObservation::Sent(Value::Null),
                    Some(Confirmed::NativeFailed) => {
                        HandoffSendObservation::NativeFailed(Value::Null)
                    }
                    None => observed,
                };
            }
            if self.in_flight && matches!(observed, HandoffSendObservation::NotAttempted(_)) {
                return HandoffSendObservation::Unknown(
                    "The original producer is still settling its pre-dispatch refusal".into(),
                );
            }
            observed
        } else if !self.in_flight {
            self.no_attempt
                .as_ref()
                .map(|reason| HandoffSendObservation::NotAttempted(reason.clone()))
                .unwrap_or_else(|| {
                    HandoffSendObservation::Unknown("Original source receipt unavailable".into())
                })
        } else {
            HandoffSendObservation::Unknown(
                "The original sender has not returned its receipt; no second send is allowed"
                    .into(),
            )
        }
    }
    fn observe(&mut self) {
        match self.observation() {
            HandoffSendObservation::Sent(_) => self.confirmed = Some(Confirmed::Sent),
            HandoffSendObservation::NativeFailed(_) => {
                self.confirmed = Some(Confirmed::NativeFailed)
            }
            _ => {}
        }
    }
    fn retryable(&self) -> bool {
        !self.in_flight && matches!(self.observation(), HandoffSendObservation::NotAttempted(_))
    }
    fn view(&self) -> Value {
        let (state, reason, response) = match self.observation() {
            HandoffSendObservation::NotAttempted(reason) => ("not-attempted", Some(reason), None),
            HandoffSendObservation::Sent(response) => {
                ("sent", None, (!response.is_null()).then_some(response))
            }
            HandoffSendObservation::NativeFailed(response) => (
                "native-failed",
                Some("The original request received a native error response".into()),
                (!response.is_null()).then_some(response),
            ),
            HandoffSendObservation::Unknown(reason) => (
                if self.in_flight { "sending" } else { "unknown" },
                Some(reason),
                None,
            ),
        };
        json!({"state":state,"attemptRef":self.reference,"target":{"generation":self.generation,"threadId":self.thread},
        "reason":reason,"nativeResponse":response,"readAvailable":true,"sourceCurrent":self.owner.as_ref().is_some_and(|owner| {
            self.source.as_ref().is_some_and(|source| owner.handoff_source_current(source))
        })})
    }
}

pub(super) fn view(handoff: &Handoff) -> Value {
    handoff
        .send_attempt
        .as_ref()
        .map(Attempt::view)
        .unwrap_or_else(|| json!({"state":"unsent"}))
}

/// No renderer target or bare RPC ID is accepted. A repeated invocation while
/// pending/unknown/acknowledged returns the original attempt without dispatch.
pub(crate) fn send_handoff(
    handoffs: &Mutex<Handoffs>,
    homes: &Mutex<HomeRouter>,
    workflows: &Mutex<WorkflowRootSession>,
    id: &str,
    text: &str,
) -> Result<Value, String> {
    send_handoff_wait(
        handoffs,
        homes,
        workflows,
        id,
        text,
        Duration::from_secs(20),
    )
}

pub(super) fn send_handoff_wait(
    handoffs: &Mutex<Handoffs>,
    homes: &Mutex<HomeRouter>,
    workflows: &Mutex<WorkflowRootSession>,
    id: &str,
    text: &str,
    wait: Duration,
) -> Result<Value, String> {
    let ticket = {
        let mut held = handoffs.lock().unwrap();
        let handoff = held
            .open
            .iter_mut()
            .find(|handoff| handoff.id == id)
            .ok_or("Original Continue-as handoff is no longer open")?;
        if let Some(attempt) = &handoff.send_attempt {
            if !attempt.retryable() {
                return Ok(attempt.view());
            }
        }
        let target = handoff
            .started
            .as_ref()
            .ok_or("The handoff has no admitted new conversation")?;
        let generation = target["generation"].clone();
        let thread = target["threadId"]
            .as_str()
            .filter(|thread| !thread.is_empty())
            .ok_or("Original admitted handoff target unavailable")?
            .to_owned();
        let attempt = Attempt {
            reference: crate::util::opaque_id("handoff-send:")?,
            generation,
            thread,
            text: text.into(),
            owner: handoff
                .native_owner
                .as_ref()
                .and_then(std::sync::Weak::upgrade),
            source: None,
            in_flight: true,
            no_attempt: None,
            confirmed: None,
        };
        handoff.send_attempt = Some(attempt.clone()); // latch before any native dispatch
        attempt
    };
    let mut on_source = |source: &SourceRequest| {
        let mut held = handoffs.lock().unwrap();
        if let Some(attempt) = held
            .open
            .iter_mut()
            .find(|handoff| handoff.id == id)
            .and_then(|handoff| handoff.send_attempt.as_mut())
            .filter(|attempt| attempt.reference == ticket.reference)
        {
            attempt.source = Some(source.clone());
        }
    };
    let pre_dispatch = (|| {
        if text.is_empty() {
            return Err("Text required; no native dispatch was made".to_string());
        }
        let home = homes.lock().unwrap().for_generation(&ticket.generation)?;
        if !ticket
            .owner
            .as_ref()
            .is_some_and(|owner| Arc::ptr_eq(owner, &home.host))
        {
            return Err(
                "Original handoff Host differs/unavailable; no replacement source used".into(),
            );
        }
        crate::runtime_session::current_conversation(
            &home.host.snapshot(),
            &ticket.generation,
            &ticket.thread,
        )?;
        Ok(home)
    })();
    let no_attempt = match pre_dispatch {
        Err(reason) => Some(reason), // this completed branch invoked no sender
        Ok(home) => {
            // Preserve conversation_send_text's notice-first ordinary route.
            if let Some(sent) = crate::runtime_session::send_with_pending_notice_observed(
                workflows,
                &ticket.generation,
                &ticket.thread,
                text,
                None,
                &mut on_source,
            ) {
                match sent.source {
                    Some(_) => None, // source was retained before wait, even NotWritten
                    None => Some("The ordinary notice producer completed before dispatch; the original notice remains governed by its existing result".into()),
                }
            } else {
                match home
                    .host
                    .handoff_text_begin(&ticket.generation, &ticket.thread, text)
                {
                    Err(reason) => Some(reason), // factory exited before actual dispatch
                    Ok(source) => {
                        on_source(&source);
                        home.host.handoff_text_wait(&source, wait);
                        None
                    }
                }
            }
        }
    };
    let mut held = handoffs.lock().unwrap();
    let attempt = held
        .open
        .iter_mut()
        .find(|handoff| handoff.id == id)
        .and_then(|handoff| handoff.send_attempt.as_mut())
        .filter(|attempt| attempt.reference == ticket.reference)
        .ok_or("Original handoff was closed; native outcome remains in its original source")?;
    attempt.in_flight = false;
    attempt.no_attempt = no_attempt;
    attempt.observe();
    Ok(attempt.view())
}

pub(crate) fn read_handoff_send(handoffs: &Mutex<Handoffs>, id: &str) -> Result<Value, String> {
    let mut held = handoffs.lock().unwrap();
    let handoff = held
        .open
        .iter_mut()
        .find(|handoff| handoff.id == id)
        .ok_or("Original Continue-as handoff is no longer open; no source reconstructed")?;
    if let Some(attempt) = &mut handoff.send_attempt {
        attempt.observe();
    }
    Ok(view(handoff))
}
