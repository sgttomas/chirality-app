//! Pure synthetic parent pins. These are NOT Host admission, native-origin or policy witnesses.
use serde_json::{json, Value};
struct LoginSourcePin {
    generation: Value,
    rpc_id: Value,
    request_ref: String,
    mode: oauth_control::OAuthMode,
}
struct EventPin {
    generation: Value,
    receipt_position: u64,
}
#[path = "../src/oauth_control.rs"]
mod oauth_control;
use oauth_control::*;
use std::{sync::mpsc, thread, time::Duration};
fn pin(mode: OAuthMode) -> LoginSourcePin {
    LoginSourcePin {
        generation: json!({"appSession":"synthetic-session","home":"synthetic-home-byte-id","spawnCounter":1}),
        rpc_id: json!(1),
        request_ref: "synthetic-source-ref".into(),
        mode,
    }
}
fn event(pin: &LoginSourcePin, position: u64) -> EventPin {
    EventPin {
        generation: pin.generation.clone(),
        receipt_position: position,
    }
}
fn browser() -> Value {
    json!({"type":"chatgpt","loginId":"CANARY_PRIVATE_ID","authUrl":"https://synthetic.invalid/CANARY_AUTH_URL","unexpected_CANARY":"CANARY_UNEXPECTED_PAYLOAD"})
}
fn device() -> Value {
    json!({"type":"chatgptDeviceCode","loginId":"CANARY_PRIVATE_ID","verificationUrl":"https://synthetic.invalid/CANARY_VERIFY_URL","userCode":"CANARY_USER_CODE"})
}
fn ready(pin: &LoginSourcePin) -> Controller {
    let mut c = Controller::begin(pin);
    c.write_completed(pin, WriteFinish::Written);
    c.start_response(
        pin,
        &if pin.mode == OAuthMode::Chatgpt {
            browser()
        } else {
            device()
        },
    );
    c
}
fn completed(id: Option<&str>, success: bool) -> Value {
    json!({"loginId":id,"success":success,"error":"CANARY_ERROR_ECHO/CANARY_PRIVATE_ID/CANARY_USER_CODE"})
}
fn assert_safe(c: &Controller) {
    let text = format!("{:?} {:?}", c, c.observation());
    for secret in [
        "CANARY_PRIVATE_ID",
        "CANARY_AUTH_URL",
        "CANARY_VERIFY_URL",
        "CANARY_USER_CODE",
        "CANARY_ERROR_ECHO",
        "CANARY_UNEXPECTED_PAYLOAD",
    ] {
        assert!(
            !text.contains(secret),
            "safe observation/debug leaked synthetic material"
        );
    }
    assert!(text.contains("redacted/unavailable"));
}

#[test]
fn original_subset_stages_until_actual_write_and_browser_is_consumed_once() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = Controller::begin(&p);
    assert_eq!(c.start_response(&p, &browser()).phase, Phase::AwaitingWrite);
    assert!(matches!(
        c.take_presentation(&p),
        Err(Limit::WriteNotFinished)
    ));
    assert!(matches!(c.cancel_intent(&p), Err(Limit::NoPendingControl)));
    assert_eq!(
        c.write_completed(&p, WriteFinish::Written).phase,
        Phase::Pending
    );
    let permit = c.take_presentation(&p).unwrap();
    assert!(matches!(
        c.take_presentation(&p),
        Err(Limit::AlreadyPresented)
    ));
    assert_eq!(
        permit.deliver(
            || Ok(()),
            |view, lease| {
                assert!(lease.is_active());
                match view {
                    PresentationView::Browser { auth_url } => {
                        assert_eq!(auth_url, "https://synthetic.invalid/CANARY_AUTH_URL")
                    }
                    _ => panic!("wrong mode"),
                };
                NativePresentationResult::Presented
            }
        ),
        DeliveryResult::Presented
    );
    assert!(c.observation().cancel_available);
    assert_safe(&c);
}

#[test]
fn scope_matches_all_h5_fields_typed_rpc_source_ref_and_mode() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = Controller::begin(&p);
    for field in ["appSession", "home", "spawnCounter"] {
        let mut foreign = pin(OAuthMode::Chatgpt);
        foreign.generation[field] = json!("other");
        assert_eq!(
            c.start_response(&foreign, &browser()).limit,
            Some(Limit::DifferentSource)
        );
    }
    let mut foreign = pin(OAuthMode::Chatgpt);
    foreign.rpc_id = json!("1");
    assert_eq!(
        c.start_response(&foreign, &browser()).limit,
        Some(Limit::DifferentSource)
    );
    foreign = pin(OAuthMode::Chatgpt);
    foreign.request_ref = "other-ref".into();
    assert_eq!(
        c.write_completed(&foreign, WriteFinish::Written).limit,
        Some(Limit::DifferentSource)
    );
    foreign = pin(OAuthMode::DeviceCode);
    assert_eq!(
        c.start_response(&foreign, &device()).limit,
        Some(Limit::DifferentSource)
    );
    assert_eq!(
        c.start_response(&p, &device()).limit,
        Some(Limit::WrongMode)
    );
    assert_eq!(c.observation().phase, Phase::AwaitingWrite);
    assert_safe(&c);
}

#[test]
fn current_source_and_terminal_races_suppress_taken_presentation() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = ready(&p);
    let permit = c.take_presentation(&p).unwrap();
    c.complete(&event(&p, 1), &completed(Some("CANARY_PRIVATE_ID"), true));
    assert_eq!(
        permit.deliver(|| Ok(()), |_, _| panic!("stale native presentation")),
        DeliveryResult::Revoked
    );
    let mut c = ready(&p);
    let permit = c.take_presentation(&p).unwrap();
    assert_eq!(
        permit.deliver(|| Err(()), |_, _| panic!("unavailable native source")),
        DeliveryResult::CurrentSourceUnavailable
    );
    let mut racing = ready(&p);
    let permit = racing.take_presentation(&p).unwrap();
    assert_eq!(
        permit.deliver(
            || {
                racing.complete(&event(&p, 1), &completed(Some("CANARY_PRIVATE_ID"), true));
                Ok(())
            },
            |_, _| panic!("completion during source recheck must suppress native display")
        ),
        DeliveryResult::Revoked
    );
    assert_safe(&c);
    assert_safe(&racing);
}

#[test]
fn device_modal_receives_terminal_revocation_without_controller_lock() {
    let p = pin(OAuthMode::DeviceCode);
    let mut c = ready(&p);
    let permit = c.take_presentation(&p).unwrap();
    let (tx, rx) = mpsc::channel();
    let worker = thread::spawn(move || {
        permit.deliver(
            || Ok(()),
            |view, lease| {
                match view {
                    PresentationView::Device {
                        verification_url,
                        user_code,
                    } => {
                        assert_eq!(
                            verification_url,
                            "https://synthetic.invalid/CANARY_VERIFY_URL"
                        );
                        assert_eq!(user_code, "CANARY_USER_CODE");
                    }
                    _ => panic!("wrong mode"),
                }
                tx.send(()).unwrap();
                assert_eq!(
                    lease.wait(Duration::from_secs(2)),
                    Some(RevocationReason::Completed)
                );
                assert!(!lease.is_active());
                NativePresentationResult::Dismissed
            },
        )
    });
    rx.recv_timeout(Duration::from_secs(2)).unwrap();
    assert_eq!(
        c.complete(&event(&p, 1), &completed(Some("CANARY_PRIVATE_ID"), true))
            .phase,
        Phase::CompletedSuccess
    );
    assert_eq!(worker.join().unwrap(), DeliveryResult::Dismissed);
    assert_safe(&c);
}

#[test]
fn display_dismissal_preserves_private_cancel_and_status_is_actual() {
    let p = pin(OAuthMode::DeviceCode);
    let mut c = ready(&p);
    let permit = c.take_presentation(&p).unwrap();
    c.dismiss_presentation(&p);
    assert_eq!(
        permit.deliver(|| Ok(()), |_, _| panic!("dismissed display")),
        DeliveryResult::Revoked
    );
    assert_eq!(c.observation().phase, Phase::Pending);
    assert!(c.observation().cancel_available);
    let cancel = c.cancel_intent(&p).unwrap();
    let mut wire_id = None;
    cancel
        .with_login_id(|| Ok(()), |id| wire_id = Some(id.to_string()))
        .unwrap();
    assert_eq!(wire_id.as_deref(), Some("CANARY_PRIVATE_ID"));
    drop(wire_id); // designated transient synthetic wire only
    assert!(matches!(
        c.cancel_intent(&p),
        Err(Limit::CancelAlreadyAttempted)
    ));
    assert_eq!(
        c.cancel_completed(&p, CancelFinish::NotFound).phase,
        Phase::Cancelled
    );
    assert_safe(&c);
}

#[test]
fn cancel_uncertainty_is_not_cancellation_or_retry_and_terminal_can_still_match() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = ready(&p);
    let _permit = c.cancel_intent(&p).unwrap();
    let obs = c.cancel_completed(&p, CancelFinish::Unknown);
    assert_eq!(obs.phase, Phase::CancellationUnknown);
    assert_eq!(obs.limit, Some(Limit::CancelOutcomeUnknown));
    assert!(!obs.cancel_available);
    assert!(matches!(
        c.cancel_intent(&p),
        Err(Limit::CancelAlreadyAttempted)
    ));
    assert_eq!(
        c.complete(&event(&p, 1), &completed(Some("CANARY_PRIVATE_ID"), false))
            .phase,
        Phase::CompletedFailure
    );
    assert_safe(&c);
}

#[test]
fn stale_cancel_permit_and_foreign_completion_never_emit_control() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = ready(&p);
    let permit = c.cancel_intent(&p).unwrap();
    let mut foreign = pin(OAuthMode::Chatgpt);
    foreign.generation["home"] = json!("other-home");
    assert_eq!(
        c.cancel_completed(&foreign, CancelFinish::Cancelled).limit,
        Some(Limit::DifferentSource)
    );
    assert_eq!(c.observation().phase, Phase::Cancelling);
    c.complete(&event(&p, 1), &completed(Some("CANARY_PRIVATE_ID"), true));
    assert_eq!(
        permit.with_login_id(|| Ok(()), |_| panic!("obsolete cancel serialized")),
        Err(Limit::NoPendingControl)
    );
    assert_safe(&c);
}

#[test]
fn missing_null_other_and_foreign_identity_are_distinct_unmatched_limits() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = ready(&p);
    assert_eq!(
        c.complete(&event(&p, 1), &json!({"success":true})).limit,
        Some(Limit::IdentityUnavailable)
    );
    assert_eq!(
        c.complete(&event(&p, 2), &completed(None, true)).limit,
        Some(Limit::IdentityUnavailable)
    );
    assert_eq!(
        c.complete(&event(&p, 3), &completed(Some("OTHER_PRIVATE_ID"), true))
            .limit,
        Some(Limit::OtherLoginId)
    );
    let mut foreign = event(&p, 4);
    foreign.generation["appSession"] = json!("another-session");
    assert_eq!(
        c.complete(&foreign, &completed(Some("CANARY_PRIVATE_ID"), true))
            .limit,
        Some(Limit::DifferentSource)
    );
    assert_eq!(c.observation().phase, Phase::Pending);
    assert!(c.observation().cancel_available);
    assert_safe(&c);
}

#[test]
fn early_completion_before_reply_and_before_write_is_preserved_not_presented() {
    let p = pin(OAuthMode::DeviceCode);
    let mut c = Controller::begin(&p);
    assert_eq!(
        c.complete(&event(&p, 1), &completed(Some("OTHER_PRIVATE_ID"), true))
            .phase,
        Phase::AwaitingWrite
    );
    assert_eq!(
        c.complete(&event(&p, 2), &completed(Some("CANARY_PRIVATE_ID"), true))
            .phase,
        Phase::AwaitingWrite
    );
    assert_eq!(c.start_response(&p, &device()).phase, Phase::AwaitingWrite);
    assert_eq!(c.observation().write, None);
    let obs = c.write_completed(&p, WriteFinish::Written);
    assert_eq!(obs.phase, Phase::CompletedSuccess);
    assert_eq!(obs.write, Some(WriteFinish::Written));
    assert!(!obs.presentation_available);
    assert!(c.take_presentation(&p).is_err());
    assert_safe(&c);
}

#[test]
fn early_completion_after_reply_does_not_invent_finished_write() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = Controller::begin(&p);
    c.start_response(&p, &browser());
    assert_eq!(
        c.complete(&event(&p, 1), &completed(Some("CANARY_PRIVATE_ID"), true))
            .phase,
        Phase::AwaitingWrite
    );
    assert_eq!(c.observation().write, None);
    assert_eq!(
        c.write_completed(&p, WriteFinish::Failed).phase,
        Phase::Unknown
    );
    assert!(c.take_presentation(&p).is_err());
    assert_safe(&c);
}

#[test]
fn source_loss_and_owner_drop_revoke_active_modal_with_honest_unknown() {
    let p = pin(OAuthMode::DeviceCode);
    let mut c = ready(&p);
    let permit = c.take_presentation(&p).unwrap();
    let (tx, rx) = mpsc::channel();
    let worker = thread::spawn(move || {
        permit.deliver(
            || Ok(()),
            |_, lease| {
                tx.send(()).unwrap();
                assert_eq!(
                    lease.wait(Duration::from_secs(2)),
                    Some(RevocationReason::SourceLost)
                );
                assert!(!lease.is_active());
                NativePresentationResult::Unavailable
            },
        )
    });
    rx.recv_timeout(Duration::from_secs(2)).unwrap();
    assert_eq!(c.source_lost(&p.generation).phase, Phase::Unknown);
    assert_eq!(worker.join().unwrap(), DeliveryResult::Unavailable);
    assert!(c.cancel_intent(&p).is_err());
    assert_safe(&c);
    let mut c = ready(&p);
    let permit = c.take_presentation(&p).unwrap();
    drop(c);
    assert_eq!(
        permit.deliver(|| Ok(()), |_, _| panic!("dropped source control")),
        DeliveryResult::Revoked
    );
}

#[test]
fn malformed_original_subset_and_duplicate_receipt_do_not_create_terminal() {
    let p = pin(OAuthMode::DeviceCode);
    let mut c = Controller::begin(&p);
    c.write_completed(&p, WriteFinish::Written);
    assert_eq!(
        c.start_response(
            &p,
            &json!({"type":"chatgptDeviceCode","loginId":"CANARY_PRIVATE_ID"})
        )
        .limit,
        Some(Limit::InvalidShape)
    );
    assert!(!c.observation().cancel_available);
    c.start_response(&p, &device());
    assert_eq!(
        c.complete(
            &event(&p, 1),
            &json!({"loginId":"CANARY_PRIVATE_ID","success":"true"})
        )
        .limit,
        Some(Limit::InvalidShape)
    );
    assert_eq!(
        c.complete(&event(&p, 1), &completed(Some("CANARY_PRIVATE_ID"), true))
            .limit,
        Some(Limit::DuplicateReceipt)
    );
    assert_eq!(c.observation().phase, Phase::Pending);
    assert_safe(&c);
}

#[test]
fn bounded_early_observation_limit_never_guesses_or_presents() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = Controller::begin(&p);
    for i in 1..=8 {
        c.complete(
            &event(&p, i),
            &completed(Some("UNMATCHED_PRIVATE_ID"), true),
        );
    }
    assert_eq!(
        c.complete(&event(&p, 9), &completed(Some("CANARY_PRIVATE_ID"), true))
            .limit,
        Some(Limit::EarlyBufferFull)
    );
    c.start_response(&p, &browser());
    let obs = c.write_completed(&p, WriteFinish::Written);
    assert_eq!(obs.phase, Phase::Unknown);
    assert_eq!(obs.limit, Some(Limit::EarlyBufferFull));
    assert!(!obs.presentation_available);
    assert_safe(&c);
}

#[test]
fn actual_terminal_fact_is_not_rewritten_by_later_source_loss() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = ready(&p);
    c.complete(&event(&p, 1), &completed(Some("CANARY_PRIVATE_ID"), true));
    let obs = c.source_lost(&p.generation);
    assert_eq!(obs.phase, Phase::CompletedSuccess);
    assert_eq!(obs.limit, Some(Limit::SourceUnavailable));
    assert!(!obs.cancel_available);
    assert_safe(&c);
}

#[test]
fn failed_current_source_cancel_serializes_nothing_and_write_source_loss_is_unknown() {
    let p = pin(OAuthMode::Chatgpt);
    let mut c = ready(&p);
    let permit = c.cancel_intent(&p).unwrap();
    assert_eq!(
        permit.with_login_id(|| Err(()), |_| panic!("wrong source serialization")),
        Err(Limit::SourceUnavailable)
    );
    c.cancel_completed(&p, CancelFinish::Unknown);
    assert_safe(&c);
    let mut c = Controller::begin(&p);
    c.start_response(&p, &browser());
    assert_eq!(
        c.write_completed(&p, WriteFinish::SourceUnavailable).phase,
        Phase::Unknown
    );
    assert!(c.take_presentation(&p).is_err());
    assert_safe(&c);
}
