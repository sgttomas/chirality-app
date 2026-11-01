//! Private lifetime of one native lifecycle question. No public control surface.
//! An expired or uncertain question cannot authorize a lifecycle action.
use std::time::Instant;

pub(super) const EXPIRED: &str =
    "Native lifecycle question expired; no choice was made and no act was authorized";

pub(super) struct Lease {
    id: u64,
    deadline: Instant,
    cancellation_requested: bool,
}
impl Lease {
    pub(super) fn new(id: u64, deadline: Instant) -> Self {
        Self {
            id,
            deadline,
            cancellation_requested: false,
        }
    }
    pub(super) fn is_for(&self, id: u64) -> bool {
        self.id == id
    }
    /// Called before the one exact-sheet end request, never after it. A late
    /// native completion remains nonaffirmative even if it reports an act.
    pub(super) fn request_expiry(&mut self, id: u64, now: Instant) -> bool {
        if !self.is_for(id) || now < self.deadline || self.cancellation_requested {
            return false;
        }
        self.cancellation_requested = true;
        true
    }
    /// Time is checked at interpretation too: a delayed main-queue timer must
    /// not permit a positive callback after the question's lifetime ended.
    pub(super) fn result_allowed(&self, id: u64, now: Instant) -> Result<(), String> {
        if !self.is_for(id) {
            return Err("Native lifecycle question identity changed; no act authorized".into());
        }
        if self.cancellation_requested || now >= self.deadline {
            Err(EXPIRED.into())
        } else {
            Ok(())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;
    #[test]
    fn before_deadline_may_answer_but_cannot_expire() {
        let now = Instant::now();
        let mut lease = Lease::new(1, now + Duration::from_secs(30));
        assert!(!lease.request_expiry(1, now));
        assert!(lease.result_allowed(1, now).is_ok());
    }
    #[test]
    fn exact_deadline_and_late_callback_cannot_authorize_even_before_timer_runs() {
        let end = Instant::now();
        let lease = Lease::new(1, end);
        assert_eq!(lease.result_allowed(1, end).unwrap_err(), EXPIRED);
        assert!(lease
            .result_allowed(1, end + Duration::from_secs(1))
            .is_err());
    }
    #[test]
    fn expiry_is_consumed_before_native_end_and_never_repeated() {
        let end = Instant::now();
        let mut lease = Lease::new(1, end);
        assert!(lease.request_expiry(1, end));
        assert!(!lease.request_expiry(1, end));
        assert!(lease.result_allowed(1, end).is_err());
    }
    #[test]
    fn stale_timer_cannot_cancel_the_next_question() {
        let end = Instant::now();
        let mut next = Lease::new(2, end);
        assert!(!next.request_expiry(1, end));
        assert!(next.request_expiry(2, end));
    }
    #[test]
    fn stale_callback_cannot_authorize_the_next_question() {
        let now = Instant::now();
        let next = Lease::new(2, now + Duration::from_secs(30));
        assert!(next.result_allowed(1, now).is_err());
        assert!(next.result_allowed(2, now).is_ok());
    }
}
