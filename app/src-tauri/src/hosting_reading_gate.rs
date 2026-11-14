//! Configuration readings of one Codex generation are made one at a time.
//!
//! A reading is a `config/read` or a `configRequirements/read` request. It is registered, and so
//! becomes the newest reading of its generation, only when no earlier reading of that generation
//! is outstanding; it is outstanding from its registration until its own terminal reply (a result
//! or an error) arrives or the generation closes. A caller that stops waiting does not end it. So
//! the newest registered reading is always the latest one Codex completed. It says nothing about
//! whether settings on disk are still what that reading reported.
//!
//! One place: the reservation and its stage live in the host's state (`Inner::reading_slot`), and
//! a reading's stage changes only under the host's state lock, each change checking the stage it
//! expects. Waiters wait on the host's state condition variable, which releases the lock while
//! they wait; nothing waits on it holding the frame writer or the attachment gate (the
//! reservation is taken before the request path takes either).
//!
//! One absolute deadline (the call's start plus the caller's budget) bounds the wait for the
//! reservation, the wait for the frame writer and the wait for the reply. The write of the bytes
//! itself has no bound: a caller inside a blocked write cannot be timed out, and the reading stays
//! outstanding.
use super::*;

/// Shown when the generation's reservation was still held by an earlier reading when this
/// reading's deadline passed. "Configuration" covers both reading methods, `config/read` and
/// `configRequirements/read`. Nothing was registered and nothing was written.
pub(crate) const READING_GATE: &str = "An earlier configuration reading for this home was still pending when the wait ended. This configuration request was not sent. You can try again after that reading finishes or Codex for this home is restarted.";
/// Shown when a registered reading's deadline passed before it could take the frame writer, or was
/// found passed once it had it. "Configuration" covers both reading methods. Nothing was written;
/// never given for a write that was attempted.
pub(crate) const READING_WITHDRAWN: &str = "This configuration request was not sent because its time limit expired while waiting to write to Codex for this home.";
/// Before either sentence when the configuration reading after a confirmed provider write fails
/// that way: the write's known outcome comes first and is not put in doubt by the sentence.
pub(crate) const WRITE_THEN_READING: &str = "Write observed; no retry. Reading the configuration again afterwards: ";
/// The deadline a reading gets when its sender names none (the generic request route).
pub(crate) const READING_DEFAULT_BUDGET: Duration = Duration::from_secs(10);
/// The longest a waiter sleeps before looking at the generation again: a close is seen without
/// relying on a notification.
const READING_POLL: Duration = Duration::from_millis(50);

pub(super) fn is_reading(method: &str) -> bool {
    matches!(method, "config/read" | "configRequirements/read")
}
/// Why settlement does not take a reply as the terminal reply to its request.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(super) enum Unsettled {
    /// Not an object, another request's id, a method, or both a result and an error.
    Envelope,
    /// An error without an integer code and a string message.
    ErrorShape,
    /// Neither a result nor an error.
    NoResult,
}
/// The one test of a terminal reply that settlement accepts: an object naming the request's own
/// id, with no method, exactly one of a result and an error, and an error carrying an integer code
/// and a string message. `completed_client_response` and a reading's release both use it, so a
/// reply settlement rejects never releases a reading; it stays outstanding until a reply settlement
/// accepts or the generation's close. A well-formed result whose content supplies no usable
/// configuration still settles, and releases.
pub(super) fn settlement(frame: &Value, id: Option<&Value>) -> Result<(), Unsettled> {
    if !frame.is_object() || frame.get("id") != id || frame.get("method").is_some() || frame.get("error").is_some() && frame.get("result").is_some() {
        return Err(Unsettled::Envelope);
    }
    match (frame.get("error"), frame.get("result")) {
        (Some(error), _) if error["code"].as_i64().is_none() || !error["message"].is_string() => Err(Unsettled::ErrorShape),
        (None, None) => Err(Unsettled::NoResult),
        _ => Ok(()),
    }
}
/// The child-role known-phase prefix, defined beside the reread it describes.
pub(crate) use super::access_provider::CHILD_ROLES_IN_PLACE;
/// Whether a message is a reading refusal, exactly: either sentence alone, or the child-role
/// known-phase prefix (`access_provider::CHILD_ROLES_IN_PLACE`) followed by either sentence alone.
/// Nothing else counts, however it ends: a later message that happens to end in a sentence after
/// another prefix (the write-then-reading prefix, for one) is not a refusal before send. The fork's
/// role-supply record, `role_supply_refusal` and the clean trial start all decide on this.
pub(crate) fn carries_reading_sentence(message: &str) -> bool {
    reading_sentence(message) || message.strip_prefix(CHILD_ROLES_IN_PLACE).is_some_and(reading_sentence)
}
/// Whether an error is one of the two sentences a sender must pass on as it is.
pub(crate) fn reading_sentence(error: &str) -> bool {
    error == READING_GATE || error == READING_WITHDRAWN
}
/// The error a sender shows: either sentence as it is, otherwise its own.
pub(crate) fn reading_or(error: String, own: impl FnOnce() -> String) -> String {
    if reading_sentence(&error) { error } else { own() }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(super) enum ReadingStage {
    /// The reservation is taken; nothing is registered.
    Reserved,
    /// Registered under the host's state lock; the newest reading of the generation; not written.
    Registered,
    /// Admitted to its write, frame writer held: from here it is never withdrawn.
    WriteStarted,
    /// Written; waiting for its terminal reply.
    AwaitingReply,
    /// The write returned an error after it was attempted: bytes may have reached Codex, so it
    /// stays outstanding until a reply or the generation's close.
    WriteFailed,
    /// Its caller stopped waiting; it holds no proof and never will.
    Abandoned,
}
/// The generation's one place for an outstanding reading.
#[derive(Clone, Debug)]
pub(super) struct ReadingSlot {
    pub(super) token: u64,
    pub(super) generation: Value,
    pub(super) request_id: Option<String>,
    pub(super) request_ref: Option<String>,
    pub(super) stage: ReadingStage,
}
/// Which request is the newest reading of its generation. A configuration reading's folder is
/// kept so that a proof stays bound to its own folder; a requirements reading has none and no
/// proof matches it.
#[derive(Clone, Debug, PartialEq)]
pub(super) struct ReadingCurrent {
    pub(super) generation: Value,
    pub(super) request_ref: String,
    pub(super) method: String,
    pub(super) cwd: Option<String>,
}
#[derive(Default, Debug)]
pub(super) struct ReadingQueue {
    next_token: u64,
    next_ticket: u64,
    /// Waiting callers in arrival order: the reservation goes to the earliest, so no caller is
    /// passed over by later ones.
    waiting: std::collections::BTreeSet<u64>,
}

/// A caller's hold on the reservation, from the wait until its write is admitted. Dropping it
/// before `WriteStarted` (an error return, a panic unwinding) withdraws the reading under the
/// host's state lock; after `WriteStarted` it does nothing (the reading stays outstanding).
pub(super) struct ReadingHold {
    inner: Arc<(Mutex<Inner>, Condvar)>,
    pub(super) token: u64,
    ticket: Option<u64>,
    pub(super) deadline: std::time::Instant,
}
impl Drop for ReadingHold {
    fn drop(&mut self) {
        let (lock, cv) = &*self.inner;
        let mut i = lock.lock().unwrap_or_else(|p| p.into_inner());
        if let Some(ticket) = self.ticket.take() { i.reading_queue.waiting.remove(&ticket); }
        let reason = "the reading's sender ended before its write";
        Host::reading_withdraw_locked(&mut i, self.token, reason);
        cv.notify_all();
    }
}

impl Host {
    /// Waits, holding no lock while it waits, until this generation's reservation is free and this
    /// caller is the earliest waiting, or the deadline passes (`READING_GATE`), or the generation
    /// is no longer current and ready (today's refusal for a changed generation).
    pub(super) fn reading_reserve(&self, method: &str, generation: Option<&Value>, deadline: std::time::Instant) -> Result<ReadingHold, String> {
        let (lock, cv) = &*self.inner;
        let mut i = lock.lock().unwrap();
        let generation = generation.cloned().unwrap_or_else(|| i.generation.clone());
        i.reading_queue.next_ticket += 1;
        let ticket = i.reading_queue.next_ticket;
        i.reading_queue.waiting.insert(ticket);
        // From here the ticket is removed on every path, a panic included.
        let mut hold = ReadingHold { inner: Arc::clone(&self.inner), token: 0, ticket: Some(ticket), deadline };
        #[cfg(test)] let mut announced = false;
        loop {
            if i.generation != generation || i.server_requests.is_closed(&generation) {
                drop(i);
                return Err(format!("refused-not-sent: {method} generation changed before request registration"));
            }
            // Not ready: no reservation is taken and registration refuses it as it does today
            // (with its not-ready record); a reservation token of 0 names no slot.
            if i.state != "ready" { i.reading_queue.waiting.remove(&ticket); hold.ticket = None; return Ok(hold); }
            let free = i.reading_slot.as_ref().is_none_or(|slot| slot.generation != i.generation);
            if free && i.reading_queue.waiting.first() == Some(&ticket) {
                i.reading_queue.waiting.remove(&ticket);
                hold.ticket = None;
                i.reading_queue.next_token += 1;
                let token = i.reading_queue.next_token;
                hold.token = token;
                i.reading_slot = Some(ReadingSlot { token, generation, request_id: None, request_ref: None, stage: ReadingStage::Reserved });
                return Ok(hold);
            }
            let now = std::time::Instant::now();
            if now >= deadline {
                drop(i);
                return Err(READING_GATE.into());
            }
            #[cfg(test)] if !announced {
                announced = true;
                let hook = self.reading_waiting.lock().unwrap().take();
                if let Some(h) = hook { drop(i); h(self); i = lock.lock().unwrap(); continue; }
            }
            i = cv.wait_timeout(i, (deadline - now).min(READING_POLL)).unwrap().0;
        }
    }
    /// Reserved to Registered, under the host's state lock at registration: this request becomes
    /// the newest reading of the generation, and every earlier proof of it, of any folder, is no
    /// longer current.
    pub(super) fn reading_register_locked(i: &mut Inner, hold: &ReadingHold, request: &SourceRequest, method: &str) -> Result<(), String> {
        let slot = i.reading_slot.as_mut().filter(|s| s.token == hold.token && s.stage == ReadingStage::Reserved)
            .ok_or_else(|| format!("refused-not-sent: {method} reservation ended before registration"))?;
        slot.request_id = Some(request.request_id().to_string());
        slot.request_ref = Some(request.request_ref.clone());
        slot.stage = ReadingStage::Registered;
        let cwd = (method == "config/read").then(|| request.frame["params"]["cwd"].as_str().filter(|c| !c.is_empty()).map(str::to_owned)).flatten();
        i.reading_current = Some(ReadingCurrent { generation: request.generation.clone(), request_ref: request.request_ref.clone(), method: method.into(), cwd });
        Ok(())
    }
    /// Registered to WriteStarted, under the host's state lock with the frame writer held: only if
    /// the deadline has not passed and the stage is still Registered.
    pub(super) fn reading_write_started_locked(i: &mut Inner, hold: &ReadingHold) -> Result<(), String> {
        if std::time::Instant::now() >= hold.deadline { return Err(READING_WITHDRAWN.into()); }
        let slot = i.reading_slot.as_mut().filter(|s| s.token == hold.token && s.stage == ReadingStage::Registered)
            .ok_or_else(|| READING_WITHDRAWN.to_owned())?;
        slot.stage = ReadingStage::WriteStarted;
        Ok(())
    }
    /// After the write: WriteStarted to AwaitingReply, or to WriteFailed. Nothing if the reply
    /// already released the reservation.
    pub(super) fn reading_written_locked(i: &mut Inner, token: u64, ok: bool) {
        if let Some(slot) = i.reading_slot.as_mut().filter(|s| s.token == token && s.stage == ReadingStage::WriteStarted) {
            slot.stage = if ok { ReadingStage::AwaitingReply } else { ReadingStage::WriteFailed };
        }
    }
    /// Reserved or Registered to Withdrawn, matching the token: the reservation is released, the
    /// pending entry is removed, and if it had registered no reading is current (nothing older is
    /// restored). Never after WriteStarted.
    pub(super) fn reading_withdraw_locked(i: &mut Inner, token: u64, reason: &str) -> bool {
        let Some(slot) = i.reading_slot.as_ref().filter(|s| s.token == token && matches!(s.stage, ReadingStage::Reserved | ReadingStage::Registered)).cloned() else { return false };
        i.reading_slot = None;
        if let (Some(id), Some(request_ref)) = (&slot.request_id, &slot.request_ref) {
            i.pending.remove(id);
            if i.reading_current.as_ref().is_some_and(|c| &c.request_ref == request_ref) { i.reading_current = None; }
            if let Some(e) = i.source_requests.get_mut(id) {
                if e.attempt_position.is_none() && e.source_limit.is_none() {
                    e.source_limit = Some(format!("No actual write attempt: reserved source invalidated/refused before pipe commit: {reason}; native reply facts retained if present"));
                }
            }
        }
        true
    }
    /// A terminal reply (result or error) with this generation and request identity releases the
    /// reservation. A reply naming another generation or request releases nothing.
    pub(super) fn reading_reply_locked(i: &mut Inner, generation: &Value, id: &str) -> bool {
        if i.reading_slot.as_ref().is_some_and(|s| &s.generation == generation && s.request_id.as_deref() == Some(id)
            && matches!(s.stage, ReadingStage::WriteStarted | ReadingStage::AwaitingReply | ReadingStage::WriteFailed | ReadingStage::Abandoned)) {
            i.reading_slot = None;
            return true;
        }
        false
    }
    /// The caller stopped waiting: AwaitingReply to Abandoned; the reservation stays held.
    pub(super) fn reading_abandoned_locked(i: &mut Inner, generation: &Value, id: &str) {
        if let Some(slot) = i.reading_slot.as_mut().filter(|s| &s.generation == generation && s.request_id.as_deref() == Some(id) && s.stage == ReadingStage::AwaitingReply) {
            slot.stage = ReadingStage::Abandoned;
        }
    }
    /// The generation closes: its reservation and its currency end with it.
    pub(super) fn reading_close_locked(i: &mut Inner, generation: &Value) {
        if i.reading_slot.as_ref().is_some_and(|s| &s.generation == generation) { i.reading_slot = None; }
        if i.reading_current.as_ref().is_some_and(|c| &c.generation == generation) { i.reading_current = None; }
    }
    /// Whether this request is the newest reading of its generation.
    pub(super) fn reading_is_current(i: &Inner, generation: &Value, request_ref: &str) -> bool {
        i.reading_current.as_ref().is_some_and(|c| &c.generation == generation && c.request_ref == request_ref)
    }
    /// The newest reading's request reference, when it is a configuration reading of this folder
    /// in this generation: the revision the settings reading and the native confirmations compare.
    pub(super) fn reading_revision(i: &Inner, generation: &Value, cwd: &str) -> Value {
        i.reading_current.as_ref()
            .filter(|c| &c.generation == generation && c.method == "config/read" && c.cwd.as_deref() == Some(cwd))
            .map(|c| json!(c.request_ref)).unwrap_or(Value::Null)
    }
    /// A configuration or requirements reading with an absolute deadline.
    pub(crate) fn request_reading(&self, method: &str, params: Value, initiator: Value, generation: &Value, private_config: bool, deadline: std::time::Instant) -> Result<SourceRequest, String> {
        if !is_reading(method) { return Err("not a configuration reading".into()); }
        auth_rpc::generic_guard(method, &params)?;
        self.request_begin_with_access_offer_guarded(method, params, initiator, false, Some(generation), false, None, None, None, None, private_config, None, None, None, Some(deadline), None)
    }
    /// The requirements reading with its sender's absolute deadline.
    pub(crate) fn account_requirements_read_until(&self, generation: &Value, deadline: std::time::Instant) -> Result<SourceRequest, String> {
        self.request_reading("configRequirements/read", json!({}), json!({"kind":"person-directed"}), generation, false, deadline)
    }
    #[cfg(test)]
    /// Holds the frame writer from another thread for `hold`; returns once it is held.
    pub(crate) fn hold_frame_writer_for_test(self: &Arc<Self>, hold: std::time::Duration) {
        let (held_tx, held) = std::sync::mpsc::channel();
        let host = Arc::clone(self);
        std::thread::spawn(move || { let _writer = host.frame_write.lock().unwrap(); let _ = held_tx.send(()); std::thread::sleep(hold); });
        held.recv().unwrap();
    }
    pub(crate) fn reading_stage_for_test(&self) -> Option<(Option<String>, ReadingStage)> {
        self.inner.0.lock().unwrap().reading_slot.as_ref().map(|s| (s.request_id.clone(), s.stage))
    }
    /// How many callers are waiting for the reservation.
    #[cfg(test)]
    pub(crate) fn reading_waiting_count_for_test(&self) -> usize {
        self.inner.0.lock().unwrap().reading_queue.waiting.len()
    }
    /// The request identity the reservation names, if any.
    #[cfg(test)]
    pub(crate) fn reading_request_id_for_test(&self) -> Option<String> {
        self.inner.0.lock().unwrap().reading_slot.as_ref().and_then(|s| s.request_id.clone())
    }
    /// The method of the request whose write is in progress, if any.
    #[cfg(test)]
    pub(crate) fn writing_method_for_test(&self) -> Option<String> {
        self.inner.0.lock().unwrap().source_requests.values().find(|e| e.write_attempt_in_progress).map(|e| e.request.frame["method"].as_str().unwrap_or("").to_owned())
    }
    #[cfg(test)]
    pub(crate) fn reading_current_for_test(&self) -> Option<String> {
        self.inner.0.lock().unwrap().reading_current.as_ref().map(|c| c.request_ref.clone())
    }
}
