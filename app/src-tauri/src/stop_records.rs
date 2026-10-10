//! REC stop requests (DEL-01-02 EXECUTION_AND_RECOVERY §3.4 SR-01…SR-12 and
//! its labels; §7 ledger kinds `stop_request` and `codex_stop`). The Design
//! text and both schemas are DRAFT/PROPOSED; this is their first App
//! implementation.
//!
//! One record per request to interrupt one turn, written before the request
//! is sent (SR-01) and again at each transition, append-only, into the App's
//! pointer-only recovery ledger. Request, transmission and observed result
//! stay apart: an empty `turn/interrupt` result is the supplier accepting the
//! request, never the turn's end. Records are validated against the embedded
//! `recovery.stop-request.schema.json` before they are queued for the ledger;
//! the ledger validates the wrapping entry again before it appends.
//!
//! A stop request is the person's operational choice, never a human act and
//! never a run end. Nothing here sends anything.
use serde_json::{json, Value};
use std::sync::OnceLock;

pub(crate) const SCHEMA: &str =
    include_str!("../resources/runtime_core/recovery.stop-request.schema.json");

fn validator() -> Result<&'static jsonschema::Validator, String> {
    static VALIDATOR: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
    VALIDATOR
        .get_or_init(|| {
            let schema: Value = serde_json::from_str(SCHEMA).map_err(|e| e.to_string())?;
            jsonschema::options().offline().build(&schema).map_err(|e| e.to_string())
        })
        .as_ref()
        .map_err(Clone::clone)
}

/// Validates one complete stop-request record.
pub(crate) fn validate(record: &Value) -> Result<(), String> {
    validator()?
        .validate(record)
        .map_err(|e| format!("stop-request schema refused the record: {e}"))
}

/// The three causes of a stop request (§3.4). The App offers no quit
/// question yet (K-4), so it never writes cause *quit*; the label table
/// still knows its words, for records read back.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Cause {
    PersonInterrupt,
    CodexStop,
}
impl Cause {
    pub fn token(self) -> &'static str {
        match self {
            Self::PersonInterrupt => "person-interrupt",
            Self::CodexStop => "codex-stop",
        }
    }
}

/// `outcomeLabel` for a cause and an outcome (*interrupted*, *completed*,
/// *failed* or *unknown*), in the schema's exact spellings.
pub(crate) fn label(cause: &str, outcome: &str) -> Option<&'static str> {
    Some(match (cause, outcome) {
        ("person-interrupt", "interrupted") => "interrupted by the person",
        ("person-interrupt", "completed") => "completed (stop requested)",
        ("person-interrupt", "failed") => "failed (stop requested)",
        ("person-interrupt", "unknown") => "outcome unknown (stop requested)",
        ("quit", "interrupted") => "interrupted by quit",
        ("quit", "completed") => "completed (quit requested)",
        ("quit", "failed") => "failed (quit requested)",
        ("quit", "unknown") => "interrupted by quit (final status not observed)",
        ("codex-stop", "interrupted") => "interrupted by Stop Codex",
        ("codex-stop", "completed") => "completed (Stop Codex requested)",
        ("codex-stop", "failed") => "failed (Stop Codex requested)",
        ("codex-stop", "unknown") => "interrupted by Stop Codex (final status not observed)",
        _ => return None,
    })
}

/// The App-owned home (DECISION-L L-1) for a home class as ACCESS names it.
pub(crate) fn home_class(class: &str) -> Option<&'static str> {
    match class {
        "account" => Some("H-acct"),
        "api-key" => Some("H-key"),
        _ => None,
    }
}

/// The person as the App observes them (K1-4): never verified.
pub fn person(identity: &str) -> Value {
    let identity = if identity.trim().is_empty() { "the person (no name set in the App)" } else { identity };
    json!({"kind":"person","identity":identity,"identityStatus":"identity not verified"})
}

/// The ledger entry that carries one stop-request record (§7 `stop_request`).
pub(crate) fn ledger_entry(session: &str, record: &Value) -> Value {
    json!({"kind":"stop_request","session":session,"at":crate::util::now_rfc3339(),"record":record})
}

/// One stop request, as this App process holds it: the latest record and the
/// ledger entry last queued for it.
pub(crate) struct StopRequest {
    record: Value,
    generation: Value,
    request_identity: Option<Value>,
    last_entry: Option<Value>,
    note: Option<String>,
}
impl StopRequest {
    /// SR-01: the request, before anything is sent. The caller has checked
    /// that the turn is live in the ready generation.
    pub(crate) fn requested(generation: &Value, home: &str, thread: &str, turn: &str, cause: Cause, requested_by: &Value) -> Result<Self, String> {
        let reference = crate::recovery::generation_ref(generation)?;
        let record = json!({
            "kind":"stop_request","stopRequestId":crate::util::opaque_id("stop:")?,
            "appSession":generation["appSession"],"home":home,"generation":reference,
            "threadId":thread,"turnId":turn,"cause":cause.token(),"requestedBy":requested_by,
            "requestedAt":crate::util::now_rfc3339(),"send":"pending","response":"pending",
            "turnOutcome":"pending","outcomeSource":"not-observed","state":"requested","transition":"SR-01"});
        validate(&record)?;
        Ok(Self { record, generation: generation.clone(), request_identity: None, last_entry: None, note: None })
    }
    pub(crate) fn id(&self) -> &str {
        self.record["stopRequestId"].as_str().unwrap_or_default()
    }
    pub(crate) fn record(&self) -> &Value {
        &self.record
    }
    pub(crate) fn generation(&self) -> &Value {
        &self.generation
    }
    pub(crate) fn request_identity(&self) -> Option<&Value> {
        self.request_identity.as_ref()
    }
    pub(crate) fn last_entry(&self) -> Option<&Value> {
        self.last_entry.as_ref()
    }
    pub(crate) fn note(&self) -> Option<&str> {
        self.note.as_deref()
    }
    pub(crate) fn queued(&mut self, entry: Value) {
        self.last_entry = Some(entry);
    }
    pub(crate) fn set_note(&mut self, note: impl Into<String>) {
        self.note = Some(note.into());
    }
    pub(crate) fn is_for(&self, generation: &Value, thread: &str, turn: &str) -> bool {
        self.generation == *generation && self.record["threadId"] == thread && self.record["turnId"] == turn
    }
    fn state(&self) -> &str {
        self.record["state"].as_str().unwrap_or_default()
    }
    /// A new record from the current one; validated before it replaces it.
    fn advance(&mut self, changes: Value) -> Result<Value, String> {
        let mut next = self.record.clone();
        for (key, value) in changes.as_object().ok_or("stop-request change must be an object")? {
            if value.is_null() {
                next.as_object_mut().unwrap().remove(key);
            } else {
                next[key] = value.clone();
            }
        }
        validate(&next)?;
        self.record = next.clone();
        Ok(next)
    }
    /// SR-02: the request was written to Codex (HOSTING §5.1, person-directed).
    pub(crate) fn sent(&mut self, client_request: &str, request_identity: &Value) -> Result<Value, String> {
        if self.state() != "requested" {
            return Err("stop request is not awaiting its send".into());
        }
        self.request_identity = Some(request_identity.clone());
        self.advance(json!({"send":"sent","clientRequest":client_request,"state":"sent","transition":"SR-02"}))
    }
    /// SR-03: nothing was sent. `write_failed` distinguishes a failed write
    /// from a request refused before any write; `reason` says which refusal.
    pub(crate) fn not_sent(&mut self, write_failed: bool, reason: &str) -> Result<Value, String> {
        if self.state() != "requested" {
            return Err("stop request is not awaiting its send".into());
        }
        let send = if write_failed { "not-sent(write-failed)" } else { "not-sent(not-ready)" };
        self.advance(json!({"send":send,"response":"not-applicable","responseError":reason,"state":"not-sent","transition":"SR-03"}))
    }
    /// SR-04, SR-05 or SR-12 from the correlated response to the request.
    pub(crate) fn response(&mut self, frame: &Value) -> Result<Option<Value>, String> {
        let error = frame.get("error");
        let result = frame.get("result");
        if error.is_none() && result.is_none() {
            return Ok(None);
        }
        let message = error.map(|e| e["message"].as_str().map(str::to_owned).unwrap_or_else(|| e.to_string()));
        match self.state() {
            "sent" if self.record["response"] == "pending" => {
                Ok(Some(match message {
                    Some(message) => self.advance(json!({"response":"error","responseError":message,"state":"refused","transition":"SR-05"}))?,
                    None => self.advance(json!({"response":"result","state":"accepted","transition":"SR-04"}))?,
                }))
            }
            // SR-12: after turn/completed; the outcome is unchanged. A closed
            // generation delivers no response, so `outcome-unknown` has none.
            "settled" if self.record["response"] == "pending" => {
                let mut changes = json!({"response":if message.is_some(){"error"}else{"result"},"transition":"SR-12"});
                if let Some(message) = message {
                    changes["responseError"] = json!(message);
                }
                Ok(Some(self.advance(changes)?))
            }
            _ => Ok(None),
        }
    }
    /// SR-06 / SR-07: `turn/completed` observed for the turn.
    pub(crate) fn turn_completed(&mut self, status: &str) -> Result<Option<Value>, String> {
        if !matches!(self.state(), "sent" | "accepted" | "refused") || !matches!(status, "interrupted" | "completed" | "failed") {
            return Ok(None);
        }
        let label = label(self.record["cause"].as_str().unwrap_or_default(), status).ok_or("stop request cause unknown")?;
        let transition = if status == "interrupted" { "SR-06" } else { "SR-07" };
        Ok(Some(self.advance(json!({"turnOutcome":status,"outcomeSource":"observed","outcomeLabel":label,"state":"settled","transition":transition}))?))
    }
    /// SR-08: the generation closed with no `turn/completed` observed.
    pub(crate) fn generation_closed(&mut self) -> Result<Option<Value>, String> {
        if !matches!(self.state(), "sent" | "accepted" | "refused") {
            return Ok(None);
        }
        let label = label(self.record["cause"].as_str().unwrap_or_default(), "unknown").ok_or("stop request cause unknown")?;
        let mut changes = json!({"turnOutcome":"unknown","outcomeSource":"not-observed","outcomeLabel":label,"state":"outcome-unknown","transition":"SR-08"});
        if self.record["response"] == "pending" {
            changes["response"] = json!("unknown-no-response");
        }
        Ok(Some(self.advance(changes)?))
    }
    /// SR-10: the caller's wait ended with no response; nothing else changes.
    pub(crate) fn waiting_ended(&mut self) -> Result<Option<Value>, String> {
        if self.state() != "sent" || self.record["response"] != "pending" || self.record["waitingEnded"] == true {
            return Ok(None);
        }
        Ok(Some(self.advance(json!({"waitingEnded":true,"transition":"SR-10"}))?))
    }
}

/// The ledger `codex_stop` entry (§7; C-12): the person, the home, restart or
/// not, and the live turns and requests the App observed when the person
/// confirmed. Validated by the ledger schema before it is queued.
pub(crate) fn codex_stop_entry(session: &str, actor: &Value, home: &str, restart: bool, material: &Value) -> Result<Value, String> {
    let live_turns: Vec<Value> = material["observedLiveTurns"].as_array().into_iter().flatten()
        .filter_map(|t| Some(json!({"threadId":t["threadId"].as_str()?,"turnId":t["turnId"].as_str()?})))
        .collect();
    let mut outstanding = Vec::new();
    for request in material["observedOutstandingRequests"].as_array().into_iter().flatten() {
        let generation = crate::recovery::generation_ref(&request["generation"])?;
        let identity = serde_json::to_string(&request["requestIdentity"]).map_err(|e| e.to_string())?;
        let mut row = json!({"generation":generation,"requestIdentity":identity,"method":request["method"]});
        if let Some(thread) = request["threadId"].as_str().filter(|s| !s.is_empty()) {
            row["subject"] = json!({"threadId":thread});
            if let Some(turn) = request["turnId"].as_str().filter(|s| !s.is_empty()) {
                row["subject"]["turnId"] = json!(turn);
            }
        }
        outstanding.push(row);
    }
    let entry = json!({"kind":"codex_stop","session":session,"at":crate::util::now_rfc3339(),"actor":actor,
        "homes":[home],"restart":restart,"liveTurns":live_turns,"outstandingEntries":outstanding});
    crate::recovery::RecoveryLedger::validate_pointer_entry(&entry)?;
    Ok(entry)
}

/// What the person is shown for one stop request: the record's own label
/// where it has one, otherwise a reading that claims nothing more than the
/// record holds. `earlier` is true for a request of an earlier App session.
/// The third value is true when the label is derived here and is not in any
/// record (R-2: an earlier session's request with no final status).
fn reading(record: &Value, earlier: bool) -> (Option<String>, String, bool) {
    let cause = record["cause"].as_str().unwrap_or_default();
    if let Some(label) = record["outcomeLabel"].as_str() {
        let reading = match record["state"].as_str() {
            Some("outcome-unknown") => "No final status was observed before Codex stopped.",
            Some("outcome-recovered") => "Final status recovered from Codex's history.",
            _ => "Final status observed when the turn ended.",
        };
        return (Some(label.to_owned()), reading.to_owned(), false);
    }
    let (label, reading) = match (record["state"].as_str().unwrap_or_default(), earlier) {
        ("not-sent", _) => (None, format!("Stop not sent: {}", record["responseError"].as_str().unwrap_or("reason not recorded"))),
        ("requested", true) => (None, "Stop requested; the App session ended before its send was recorded, so whether it was sent is not known.".into()),
        ("requested", false) => (None, "Stop requested; not yet sent.".into()),
        (_, true) => (
            label(cause, "unknown").map(str::to_owned),
            "The App session ended before a final status was recorded for this turn; this label is derived from that and is not written in any record.".into(),
        ),
        ("accepted", false) => (None, "Codex accepted the stop request. That is not the turn's end; its final status is not yet observed.".into()),
        ("refused", false) => (None, format!("Codex refused the stop request: {}", record["responseError"].as_str().unwrap_or("message not recorded"))),
        (_, false) => (None, "Stop requested; Codex's answer and the turn's final status are not yet observed.".into()),
    };
    let derived = label.is_some();
    (label, reading, derived)
}

/// The ledger's stop-request entries, indexed once as they are appended
/// (a snapshot does not re-validate or re-scan the whole ledger). The ledger
/// is append-only; if the snapshot no longer continues the indexed prefix
/// (another ledger, or a shorter one) the index is rebuilt.
#[derive(Debug, Default)]
pub(crate) struct LedgerIndex {
    seen: usize,
    last: Option<Value>,
    order: Vec<String>,
    latest: std::collections::BTreeMap<String, Value>,
    entries: std::collections::HashMap<String, Vec<Value>>,
    limits: Vec<String>,
}
impl LedgerIndex {
    pub(crate) fn update(&mut self, ledger: Option<&Value>) {
        let rows: &[Value] = ledger.and_then(|l| l["entries"].as_array()).map(Vec::as_slice).unwrap_or(&[]);
        let continues = self.seen <= rows.len() && (self.seen == 0 || rows.get(self.seen - 1) == self.last.as_ref());
        if !continues {
            *self = Self::default();
        }
        for entry in rows[self.seen..].iter().filter(|e| e["kind"] == "stop_request") {
            let record = &entry["record"];
            if let Err(error) = validate(record) {
                self.limits.push(format!("a stop_request ledger entry is not a valid stop-request record and is not shown: {error}"));
                continue;
            }
            let id = record["stopRequestId"].as_str().unwrap_or_default().to_owned();
            if !self.latest.contains_key(&id) {
                self.order.push(id.clone());
            }
            self.latest.insert(id.clone(), record.clone());
            self.entries.entry(id).or_default().push(entry.clone());
        }
        self.seen = rows.len();
        self.last = rows.last().cloned();
    }
    /// Whether this exact ledger entry is in the ledger (compared only with
    /// the entries of its own stop request).
    pub(crate) fn contains(&self, entry: &Value) -> bool {
        entry["record"]["stopRequestId"].as_str().and_then(|id| self.entries.get(id)).is_some_and(|rows| rows.contains(entry))
    }
}

/// The stop requests the App can show: every request in the ledger (latest
/// record per request, every App session) and this process's requests, each
/// with this process's own persistence reading. `current` names this App
/// session. Pointer facts only; Codex's own history is read separately.
pub(crate) fn outcomes(ledger: Option<&Value>, live: &[(Value, String)], current: &str) -> Value {
    let mut index = LedgerIndex::default();
    index.update(ledger);
    outcomes_indexed(&index, live, current)
}
pub(crate) fn outcomes_indexed(index: &LedgerIndex, live: &[(Value, String)], current: &str) -> Value {
    let mut order = index.order.clone();
    let mut latest: std::collections::BTreeMap<String, (Value, String)> =
        index.latest.iter().map(|(id, record)| (id.clone(), (record.clone(), "recorded in the App ledger".to_owned()))).collect();
    let limits = index.limits.clone();
    // This process knows more than the ledger about its own requests (a
    // transition that was not recorded, a record still queued): its reading
    // replaces the ledger's, and its newer record is shown.
    for (record, persistence) in live {
        let id = record["stopRequestId"].as_str().unwrap_or_default().to_owned();
        if !latest.contains_key(&id) {
            order.push(id.clone());
        }
        latest.insert(id, (record.clone(), persistence.clone()));
    }
    let rows: Vec<Value> = order.iter().filter_map(|id| latest.get(id)).map(|(record, persistence)| {
        let earlier = record["appSession"] != current;
        let (label, reading, derived) = reading(record, earlier);
        let reported = matches!(record["outcomeSource"].as_str(), Some("observed" | "recovered-from-supplier")).then(|| record["turnOutcome"].clone());
        json!({"stopRequestId":record["stopRequestId"],"appSession":record["appSession"],"earlierSession":earlier,"home":record["home"],
            "generation":record["generation"],"threadId":record["threadId"],"turnId":record["turnId"],"cause":record["cause"],
            "requestedAt":record["requestedAt"],"state":record["state"],"transition":record["transition"],"send":record["send"],
            "response":record["response"],"waitingEnded":record["waitingEnded"],"label":label,"labelDerived":derived,"reading":reading,"codexReported":reported,
            "persistence":persistence})
    }).collect();
    json!({"records":rows,"limits":limits,
        "standing":"App-observed stop requests (REC SR). A label comes from the turn's observed end or from the App's own record, never from an interrupt acknowledgment. Items and delegated agents at the outcome are not recorded by this App. Codex's own status for a turn is read from its history separately."})
}

#[cfg(test)]
#[path = "stop_records_tests.rs"]
mod tests;
