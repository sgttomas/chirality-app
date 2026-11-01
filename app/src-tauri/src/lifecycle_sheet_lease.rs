//! Private lifetime of one native lifecycle question. No public control surface.
//! An expired or uncertain question cannot authorize a lifecycle action.
use std::time::{Duration, Instant};

pub(super) const EXPIRED: &str =
    "Native lifecycle question expired; no choice was made and no act was authorized";

pub(super) struct Lease {
    id: u64,
    deadline: Instant,
    cancellation_requested: bool,
    completion: Option<(isize, Instant)>,
    checks: u8,
    early_timers: u8,
    held: bool,
}
impl Lease {
    pub(super) fn new(id: u64, deadline: Instant) -> Self {
        Self {
            id,
            deadline,
            cancellation_requested: false,
            completion: None,
            checks: 0,
            early_timers: 0,
            held: false,
        }
    }
    pub(super) fn is_for(&self, id: u64) -> bool {
        self.id == id
    }
    /// Called before the one exact-sheet end request, never after it. A late
    /// native completion remains nonaffirmative even if it reports an act.
    pub(super) fn request_expiry(&mut self, id: u64, now: Instant) -> bool {
        if !self.is_for(id)
            || now < self.deadline
            || self.cancellation_requested
            || self.completion.is_some()
            || self.held
        {
            return false;
        }
        self.cancellation_requested = true;
        true
    }
    pub(super) fn timer(&mut self, id: u64, now: Instant) -> Timer {
        if !self.is_for(id) || self.held || self.completion.is_some() || self.cancellation_requested
        {
            return Timer::Ignore;
        }
        if now < self.deadline {
            if self.early_timers >= 2 {
                self.held = true;
                return Timer::Hold;
            }
            self.early_timers += 1;
            return Timer::After(self.deadline.duration_since(now));
        }
        if self.request_expiry(id, now) {
            Timer::End
        } else {
            Timer::Ignore
        }
    }
    pub(super) fn has_completion(&self) -> bool {
        self.completion.is_some()
    }
    pub(super) fn hold(&mut self) {
        self.held = true;
    }
    pub(super) fn completion(&mut self, id: u64, response: isize, now: Instant) -> bool {
        if !self.is_for(id) || self.completion.is_some() {
            return false;
        }
        self.completion = Some((response, now));
        true
    }
    pub(super) fn verify(&mut self, id: u64, now: Instant, facts: Dismissal) -> Verify {
        if !self.is_for(id) {
            return Verify::Ignore;
        }
        let Some((response, started)) = self.completion else {
            return Verify::Ignore;
        };
        if facts.parent_changed {
            self.hold();
            return Verify::Hold;
        }
        if !facts.parent_present && !facts.visible && !facts.listed {
            return Verify::Released(response);
        }
        if self.checks >= 20 || now.saturating_duration_since(started) >= Duration::from_secs(1) {
            self.hold();
            return Verify::Hold;
        }
        self.checks += 1;
        Verify::Later
    }
    /// Time is checked at interpretation too: a delayed main-queue timer must
    /// not permit a positive callback after the question's lifetime ended.
    pub(super) fn result_allowed(&self, id: u64, now: Instant) -> Result<(), String> {
        if !self.is_for(id) {
            return Err("Native lifecycle question identity changed; no act authorized".into());
        }
        if self.held {
            return Err("Native lifecycle sheet was held; no act authorized".into());
        }
        if self.cancellation_requested || now >= self.deadline {
            Err(EXPIRED.into())
        } else {
            Ok(())
        }
    }
}

#[derive(Debug, PartialEq)]
pub(super) enum Timer {
    Ignore,
    After(Duration),
    End,
    Hold,
}
#[derive(Debug, PartialEq)]
pub(super) enum Verify {
    Ignore,
    Later,
    Hold,
    Released(isize),
}
pub(super) struct Dismissal {
    pub parent_present: bool,
    pub parent_changed: bool,
    pub visible: bool,
    pub listed: bool,
}
pub(super) fn admit(
    visible: bool,
    miniaturized: bool,
    parent_is_sheet: bool,
    has_sheets: bool,
    app_modal: bool,
    occupied: bool,
) -> Result<(), String> {
    if !visible || miniaturized || parent_is_sheet || has_sheets || app_modal || occupied {
        Err("Original App window unavailable or another modal is open; lifecycle question not queued".into())
    } else {
        Ok(())
    }
}
pub(super) fn choice_index(response: isize, count: usize) -> Result<usize, String> {
    response
        .checked_sub(1000)
        .and_then(|i| usize::try_from(i).ok())
        .filter(|i| (count == 1 || count == 3) && *i < count)
        .ok_or_else(|| {
            "Native lifecycle sheet ended without a recognized choice; no act authorized".into()
        })
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
    fn attached() -> Dismissal {
        Dismissal {
            parent_present: true,
            parent_changed: false,
            visible: true,
            listed: true,
        }
    }
    fn detached() -> Dismissal {
        Dismissal {
            parent_present: false,
            parent_changed: false,
            visible: false,
            listed: false,
        }
    }
    #[test]
    fn early_timer_reschedules_without_moving_deadline_or_repeating_end() {
        let start = Instant::now();
        let end = start + Duration::from_secs(30);
        let mut lease = Lease::new(1, end);
        assert_eq!(lease.timer(1, start), Timer::After(Duration::from_secs(30)));
        assert_eq!(lease.timer(1, end), Timer::End);
        assert_eq!(lease.timer(1, end), Timer::Ignore);
        assert!(lease.result_allowed(1, end).is_err());
    }
    #[test]
    fn repeated_early_timer_becomes_visible_hold() {
        let now = Instant::now();
        let mut lease = Lease::new(1, now + Duration::from_secs(30));
        for _ in 0..2 {
            assert!(matches!(lease.timer(1, now), Timer::After(_)));
        }
        assert_eq!(lease.timer(1, now), Timer::Hold);
        assert!(lease.result_allowed(1, now).is_err());
    }
    #[test]
    fn completion_waits_for_later_detachment_without_permanent_first_read_hold() {
        let now = Instant::now();
        let mut lease = Lease::new(1, now + Duration::from_secs(30));
        assert!(lease.completion(1, 1001, now));
        assert_eq!(lease.verify(1, now, attached()), Verify::Later);
        assert_eq!(
            lease.verify(1, now + Duration::from_millis(50), detached()),
            Verify::Released(1001)
        );
        assert!(lease
            .result_allowed(1, now + Duration::from_millis(50))
            .is_ok());
        assert_eq!(lease.timer(1, now + Duration::from_secs(31)), Timer::Ignore);
    }
    #[test]
    fn failed_detachment_is_bounded_and_never_authorizes() {
        let now = Instant::now();
        let mut lease = Lease::new(1, now + Duration::from_secs(30));
        lease.completion(1, 1001, now);
        for _ in 0..20 {
            assert_eq!(lease.verify(1, now, attached()), Verify::Later);
        }
        assert_eq!(lease.verify(1, now, attached()), Verify::Hold);
        assert!(lease.result_allowed(1, now).is_err());
    }
    #[test]
    fn held_expiry_then_late_completion_can_release_only_as_refusal() {
        let now = Instant::now();
        let mut lease = Lease::new(1, now);
        assert_eq!(lease.timer(1, now), Timer::End);
        lease.hold();
        assert!(lease.completion(1, 1001, now + Duration::from_millis(20)));
        assert_eq!(
            lease.verify(1, now + Duration::from_millis(30), detached()),
            Verify::Released(1001)
        );
        assert!(lease
            .result_allowed(1, now + Duration::from_millis(30))
            .is_err());
    }
    #[test]
    fn native_response_mapping_refuses_unknown_and_single_ok_overflow() {
        for code in [0, -1000, -1001, 1003, isize::MIN, isize::MAX] {
            assert!(choice_index(code, 3).is_err());
        }
        for i in 0..3 {
            assert_eq!(choice_index(1000 + i, 3).unwrap(), i as usize);
        }
        assert_eq!(choice_index(1000, 1).unwrap(), 0);
        assert!(choice_index(1001, 1).is_err());
    }
    #[test]
    fn occupied_hidden_miniaturized_or_modal_parent_never_admits() {
        assert!(admit(true, false, false, false, false, false).is_ok());
        for v in [
            (false, false, false, false, false, false),
            (true, true, false, false, false, false),
            (true, false, true, false, false, false),
            (true, false, false, true, false, false),
            (true, false, false, false, true, false),
            (true, false, false, false, false, true),
        ] {
            assert!(admit(v.0, v.1, v.2, v.3, v.4, v.5).is_err());
        }
    }
}
