//! Native execution views, scoped to an explicit receiving home. No disk copy
//! of supplier history; no completion/review/acceptance inferred from tool status.
use crate::util::sha256_hex;
use serde_json::{json, Value};
use std::collections::BTreeMap;

fn enc(value: &str) -> String {
    const ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    let bytes = value.as_bytes();
    let mut out = String::new();
    for part in bytes.chunks(3) {
        let a = part[0] as u32;
        let b = part.get(1).copied().unwrap_or(0) as u32;
        let c = part.get(2).copied().unwrap_or(0) as u32;
        let n = (a << 16) | (b << 8) | c;
        out.push(ALPHABET[((n >> 18) & 63) as usize] as char);
        out.push(ALPHABET[((n >> 12) & 63) as usize] as char);
        if part.len() > 1 {
            out.push(ALPHABET[((n >> 6) & 63) as usize] as char);
        }
        if part.len() > 2 {
            out.push(ALPHABET[(n & 63) as usize] as char);
        }
    }
    out
}
fn text<'a>(v: &'a Value, key: &str) -> Result<&'a str, String> {
    v.get(key)
        .and_then(Value::as_str)
        .filter(|s| !s.is_empty())
        .ok_or_else(|| format!("missing {key}"))
}
fn valid_generation(g: &Value) -> bool {
    g.as_object().map(|o| o.len() == 3).unwrap_or(false)
        && text(g, "appSession").is_ok()
        && text(g, "home").is_ok()
        && g["spawnCounter"].as_u64().unwrap_or(0) > 0
}
fn native_key(thread: &str, turn: &str, item: &str) -> String {
    format!("{}.{}.{}", enc(thread), enc(turn), enc(item))
}
pub fn revision_key(reference: &Value) -> Result<String, String> {
    let thread = text(reference, "threadId")?;
    let turn = text(reference, "turnId")?;
    match text(reference, "kind")? {
        "plan-item" => Ok(format!(
            "pi:v2:{}",
            native_key(thread, turn, text(reference, "itemId")?)
        )),
        "checklist" => {
            let g = &reference["generation"];
            if !valid_generation(g) {
                return Err("invalid full generation".into());
            }
            let pos = reference["receiptPosition"]
                .as_u64()
                .ok_or("invalid receipt position")?;
            Ok(format!(
                "cl:v2:{}.{}.{}.{}.{}.{}",
                enc(text(g, "appSession")?),
                enc(text(g, "home")?),
                g["spawnCounter"],
                enc(thread),
                enc(turn),
                pos
            ))
        }
        _ => Err("unknown revision kind".into()),
    }
}
/// Error notifications kept for one turn: the newest, numbered from the first received.
const TURN_ERROR_LIMIT: usize = 32;
/// Unreadable frames named `error` kept for one turn: the newest, numbered from the first received.
const UNREADABLE_TURN_ERROR_LIMIT: usize = 8;
/// Streamed previews keep at most this many bytes, the latest text, labelled truncated.
const PREVIEW_LIMIT: usize = 256 * 1024;
fn append_preview(row: &mut Value, delta: &str) {
    if !row["preview"].is_string() {
        row["preview"] = json!("");
    }
    if let Value::String(preview) = &mut row["preview"] {
        preview.push_str(delta);
        if preview.len() > PREVIEW_LIMIT {
            let mut cut = preview.len() - PREVIEW_LIMIT;
            while !preview.is_char_boundary(cut) {
                cut += 1;
            }
            preview.drain(..cut);
            row["previewTruncated"] = json!(true);
        }
    }
}
fn identity(content: &Value) -> Value {
    // NPTD U-08 is explicitly TEST VALUE, not authoritative content identity.
    let bytes = serde_json::to_vec(content).expect("JSON Value serialization");
    json!({"method":"sha256/canonical-json/npt-v0 (TEST VALUE; HOSTING U-08)","value":sha256_hex(&bytes)})
}

#[derive(Clone)]
pub struct NativeView {
    home: String,
    generation: Option<Value>,
    closed: Vec<Value>,
    position: Option<u64>,
    types_pin: String,
    version: Value,
    supplier_standing: Value,
    distribution_evidence: Value,
    items: BTreeMap<String, Value>,
    turns: BTreeMap<(String, String), Value>,
    revisions: Vec<Value>,
    descendants: BTreeMap<String, Value>,
    goals: BTreeMap<String, Value>,
    checklist_gaps: Vec<Value>,
    /// HOSTING §8.3: `model/rerouted` notifications received live, in receipt
    /// order (read-only observations; nothing is sent in reply).
    reroutes: Vec<Value>,
    /// The supplier's `error` notifications received live, in receipt order,
    /// each as sent. Codex history carries no retry notice, so these exist
    /// only for generations this view observed.
    turn_errors: Vec<Value>,
    /// Error notices that named a thread and turn but did not match the pinned
    /// type: kept as that, with the reason, and given no retry meaning.
    unreadable_turn_errors: Vec<Value>,
    /// Order in which this view first received each item; a receipt reading,
    /// not a native sequence or a claim about when Codex produced the item.
    next_order: u64,
    /// What is established, per conversation, about the agent's question that
    /// does not wait (`agentMessage` with `delivery` `async` and questions).
    /// A conversation is a key here once it has been read in this generation;
    /// each entry is updated as an observation is consumed, never recomputed
    /// from `observedOrder`. Nothing here is persisted.
    asked: BTreeMap<String, AskedState>,
}

/// One conversation's reading: the item that established it (its turn and
/// id), or none where the conversation was read from its start with nothing
/// decisive since, and the question waiting, if any.
#[derive(Clone, Debug, PartialEq)]
struct AskedState {
    anchor: Option<(String, String)>,
    waiting: Option<Value>,
}

/// An item that decides the reading: a message from the person, or the
/// agent's question that does not wait.
enum Decisive {
    Person,
    Question,
}
fn decisive(native: &Value) -> Option<Decisive> {
    match native["type"].as_str() {
        Some("userMessage") => Some(Decisive::Person),
        Some("agentMessage")
            if native["delivery"] == "async"
                && native["questions"].as_array().is_some_and(|q| !q.is_empty()) =>
        {
            Some(Decisive::Question)
        }
        _ => None,
    }
}
/// The waiting entry for a question item. The agent's titles and options are
/// kept byte for byte; an entry whose questions do not have the pinned shape
/// (0.169.0 `AsyncUserInputQuestion`: a title, and options as text or absent)
/// is kept with its reason and no questions, never cut or reworded.
fn asked_entry(thread: &str, turn: &str, native: &Value) -> Value {
    let mut entry = json!({"threadId":thread,"turnId":turn,"itemId":native["id"]});
    let shaped = native["questions"].as_array().and_then(|questions| {
        questions
            .iter()
            .map(|q| {
                let object = q.as_object()?;
                if object.keys().any(|k| k != "title" && k != "options") {
                    return None;
                }
                let title = q["title"].as_str()?;
                let options = match &q["options"] {
                    Value::Null => Value::Null,
                    Value::Array(options) if options.iter().all(Value::is_string) => q["options"].clone(),
                    _ => return None,
                };
                Some(json!({"title":title,"options":options}))
            })
            .collect::<Option<Vec<_>>>()
    });
    match shaped {
        Some(questions) => entry["questions"] = json!(questions),
        None => entry["refused"] = json!("its questions do not have the pinned shape (a title, and options as text or absent); not shown"),
    }
    entry
}

/// What a home's native view establishes about one conversation's question
/// that does not wait. `NotRead` means the conversation's items have not been
/// read in the view's generation, never that nothing is waiting. The caller
/// reads the snapshot's `observationEnded` to know whether it is current.
#[derive(Clone, Debug, PartialEq)]
#[cfg_attr(not(test), allow(dead_code))]
pub(crate) enum AskedQuestion {
    Waiting(Value),
    None,
    NotRead,
}
/// A pure reading of a native view snapshot (`NativeView::snapshot`); it makes
/// no supplier read. The navigator's read is its caller (another lane).
#[cfg_attr(not(test), allow(dead_code))]
pub(crate) fn asked_question(snapshot: &Value, thread: &str) -> AskedQuestion {
    let asked = &snapshot["askedQuestions"];
    if let Some(entry) = asked["waiting"].as_array().into_iter().flatten().find(|e| e["threadId"] == thread) {
        return AskedQuestion::Waiting(entry.clone());
    }
    if asked["read"].as_array().into_iter().flatten().any(|t| t == thread) {
        AskedQuestion::None
    } else {
        AskedQuestion::NotRead
    }
}
impl NativeView {
    pub fn new(home: String) -> Result<Self, String> {
        if home.is_empty() {
            return Err("receiving home must be explicit".into());
        }
        Ok(Self {
            home,
            generation: None,
            closed: Vec::new(),
            position: None,
            types_pin: crate::hosting::DECLARED_PIN.into(),
            version: Value::Null,
            supplier_standing: Value::Null,
            distribution_evidence: Value::Null,
            items: BTreeMap::new(),
            turns: BTreeMap::new(),
            revisions: Vec::new(),
            descendants: BTreeMap::new(),
            goals: BTreeMap::new(),
            checklist_gaps: Vec::new(),
            reroutes: Vec::new(),
            turn_errors: Vec::new(),
            unreadable_turn_errors: Vec::new(),
            next_order: 0,
            asked: BTreeMap::new(),
        })
    }
    /// Display adapter only. The Host owns exact-byte at-use checks; this value
    /// grants no supplier standing or live custody and remains outside legacy identity.
    pub(crate) fn receive_distribution_evidence(&mut self, value: &Value) {
        self.distribution_evidence = if value.is_null() || self.generation.as_ref() == Some(&value["generation"]) {
            value.clone()
        } else { json!({"state":"unavailable","reason":"foreign generation evidence"}) };
    }
    pub fn ready(
        &mut self,
        generation: Value,
        version: Value,
        supplier_standing: Value,
    ) -> Result<(), String> {
        if !valid_generation(&generation) || generation["home"] != self.home {
            return Err("foreign or malformed ready generation".into());
        }
        if let Some(current) = &self.generation {
            if *current == generation {
                return Ok(());
            }
            if !self.closed.contains(current) {
                return Err("old generation still open".into());
            }
            if current["appSession"] != generation["appSession"] {
                return Err("new App session requires a new view".into());
            }
        }
        if self.closed.contains(&generation) {
            return Err("closed generation".into());
        }
        self.generation = Some(generation);
        self.position = None;
        self.version = version;
        self.supplier_standing = supplier_standing;
        Ok(())
    }
    pub fn close(&mut self, generation: &Value) -> Result<(), String> {
        if self.generation.as_ref() != Some(generation) {
            return Err("foreign generation close".into());
        }
        if self.closed.contains(generation) {
            return Ok(());
        }
        self.closed.push(generation.clone());
        for revision in self.revisions.iter().filter(|r| r["kind"] == "checklist") {
            let gap = json!({"threadId":revision["threadId"],"turnId":revision["turnId"],"reason":"checklist updates are not kept in Codex history; not recoverable after restart or relaunch"});
            if !self.checklist_gaps.contains(&gap) {
                self.checklist_gaps.push(gap);
            }
        }
        self.revisions.retain(|r| r["kind"] != "checklist");
        for item in self.items.values_mut() {
            if item["displayState"] == "in-progress" {
                item["displayState"] = json!("unknown");
                item["observationEnded"] = json!(true);
            }
        }
        for child in self.descendants.values_mut() {
            child["observationEnded"] = json!(true);
        }
        for error in self.turn_errors.iter_mut().chain(self.unreadable_turn_errors.iter_mut()).filter(|e| e["generation"] == *generation) {
            error["observationEnded"] = json!(true);
        }
        Ok(())
    }
    pub fn consume(&mut self, envelope: &Value) -> Result<(), String> {
        let g = &envelope["generation"];
        if !valid_generation(g) || self.generation.as_ref() != Some(g) || self.closed.contains(g) {
            return Err("foreign, unready or closed generation".into());
        }
        let pos = envelope["position"]
            .as_u64()
            .ok_or("missing receipt position")?;
        if self.position.map(|last| pos <= last).unwrap_or(false) {
            return Err("duplicate or out-of-order receipt".into());
        }
        let frame = &envelope["frame"];
        let p = &frame["params"];
        // Any frame naming an error notice's thread and turn that was received
        // after it, other than a further error notice the view accepts: the
        // App's own receipt fact, which says nothing about why the turn moved on.
        if frame["method"] != "error" {
            let turn = p.get("turnId").or_else(|| p["turn"].get("id"));
            if let (Some(thread), Some(turn)) = (p["threadId"].as_str(), turn.and_then(Value::as_str)) {
                self.later_frame_for_turn(g, thread, turn);
            }
        }
        // Unknown native frames also advance the all-frame cursor. They stay
        // inspectable in hosting's unmodified ordered journal.
        match frame["method"].as_str() {
            Some("item/started" | "item/completed") => {
                let completed = frame["method"] == "item/completed";
                self.item(
                    text(p, "threadId")?,
                    text(p, "turnId")?,
                    &p["item"],
                    completed,
                    false,
                    Some(frame.clone()),
                )?;
                // Receipt positions of the item's start and completion in this
                // generation: the App's receiving order, never a native sequence.
                let key = native_key(text(p, "threadId")?, text(p, "turnId")?, text(&p["item"], "id")?);
                if let Some(row) = self.items.get_mut(&key) {
                    if row["receipt"]["generation"] != *g {
                        row["receipt"] = json!({"generation": g});
                    }
                    row["receipt"][if completed { "completed" } else { "started" }] = json!(pos);
                }
                self.asked_live(text(p, "threadId")?, text(p, "turnId")?, &p["item"], completed);
            }
            Some("item/plan/delta") => {
                let thread = text(p, "threadId")?;
                let turn = text(p, "turnId")?;
                let id = text(p, "itemId")?;
                let key = native_key(thread, turn, id);
                let order = self.next_order;
                let row=self.items.entry(key).or_insert_with(||json!({"threadId":thread,"turnId":turn,"native":{"id":id,"type":"plan"},"displayState":"in-progress","observedOrder":order}));
                if row["observedOrder"] == order {
                    self.next_order += 1;
                }
                if row["displayState"] == "in-progress" {
                    append_preview(row, p["delta"].as_str().ok_or("invalid plan delta")?);
                    row["previewStanding"] = json!("in progress; may differ from completed plan");
                }
            }
            Some(method @ ("item/agentMessage/delta" | "item/commandExecution/outputDelta" | "item/reasoning/summaryTextDelta")) => {
                // Streamed text is a preview of an in-progress item only; the
                // completed native item replaces the whole row (and the preview).
                let thread = text(p, "threadId")?;
                let turn = text(p, "turnId")?;
                let id = text(p, "itemId")?;
                let delta = p["delta"].as_str().ok_or("invalid delta")?;
                let kind = match method {
                    "item/agentMessage/delta" => "agentMessage",
                    "item/commandExecution/outputDelta" => "commandExecution",
                    _ => "reasoning",
                };
                let summary_index = if kind == "reasoning" {
                    let index = p["summaryIndex"].as_u64().ok_or("invalid summary index")? as usize;
                    if index > 4096 {
                        return Err("summary index out of range".into());
                    }
                    index
                } else {
                    0
                };
                let key = native_key(thread, turn, id);
                let order = self.next_order;
                let row=self.items.entry(key).or_insert_with(||json!({"threadId":thread,"turnId":turn,"native":{"id":id,"type":kind},"displayState":"in-progress","standing":"live-observed","observationEnded":false,"observedOrder":order}));
                if row["observedOrder"] == order {
                    self.next_order += 1;
                }
                if row["displayState"] == "in-progress" {
                    if kind == "reasoning" {
                        let index = summary_index;
                        let held: usize = row["summaryPreview"].as_array().map(|a| a.iter().filter_map(Value::as_str).map(str::len).sum()).unwrap_or(0);
                        if held >= PREVIEW_LIMIT {
                            row["previewTruncated"] = json!(true);
                        } else {
                            if !row["summaryPreview"].is_array() {
                                row["summaryPreview"] = json!([]);
                            }
                            let parts = row["summaryPreview"].as_array_mut().expect("array set above");
                            while parts.len() <= index {
                                parts.push(json!(""));
                            }
                            if let Value::String(part) = &mut parts[index] {
                                part.push_str(delta);
                            }
                        }
                    } else {
                        append_preview(row, delta);
                    }
                    row["previewStanding"] = json!("streamed so far; may differ from the completed item");
                }
            }
            Some("turn/plan/updated") => {
                let thread = text(p, "threadId")?;
                let turn = text(p, "turnId")?;
                let content = json!({"explanation":p["explanation"],"steps":p["plan"]});
                let previous = self.revisions.iter().rev().find(|r| {
                    r["kind"] == "checklist" && r["threadId"] == thread && r["turnId"] == turn
                });
                let ordinal = previous
                    .map(|r| r["ordinal"].as_u64().unwrap() + 1)
                    .unwrap_or(1);
                let unchanged = previous.map(|r| r["content"] == content).unwrap_or(false);
                let mut revision = json!({"kind":"checklist","threadId":thread,"turnId":turn,"generation":g,"receiptPosition":pos,
                    "ordinal":ordinal,"content":content,"contentIdentity":identity(&content),"standing":"live-observed",
                    "unchangedFromPrevious":unchanged,"afterTurnEnd":self.turns.get(&(thread.into(),turn.into())).map(|t|t["status"]!="inProgress").unwrap_or(false),
                    "producedInMode":"not-known","typesPin":self.types_pin,"observedVersionLabel":self.version});
                revision["revisionId"] = json!(revision_key(&revision)?);
                self.revisions.push(revision);
            }
            Some("turn/started" | "turn/completed") => {
                self.turn(text(p, "threadId")?, &p["turn"], false)?;
            }
            Some("model/rerouted") => {
                // HOSTING §8.3 (0.160.0 ModelReroutedNotification): a supplier
                // report naming its thread and turn. Observed only.
                let field = |name: &str| text(p, name).map(str::to_owned);
                self.reroutes.push(json!({"threadId":field("threadId")?,"turnId":field("turnId")?,"fromModel":field("fromModel")?,"toModel":field("toModel")?,
                    "reason":p["reason"],"generation":g,"receiptPosition":pos,"standing":"live-observed"}));
            }
            Some("error") => {
                // 0.169.0 ErrorNotification: the supplier's report of an error
                // in a turn and whether it will retry. Kept as sent, never
                // reworded. Only a notification that matches the pinned type
                // is given that meaning: a frame carrying a request identity,
                // or params the type does not describe, is refused, and where
                // it names a thread and turn it is kept as unreadable.
                let refusal = if frame.get("id").is_some() {
                    Some("a server request named error is not the error notification".to_owned())
                } else {
                    crate::hosting::Host::validate_native_result("ErrorNotification", p).err()
                };
                if let Some(reason) = refusal {
                    if let (Some(thread), Some(turn)) = (p["threadId"].as_str().filter(|s| !s.is_empty()), p["turnId"].as_str().filter(|s| !s.is_empty())) {
                        self.later_frame_for_turn(g, thread, turn);
                        let same = |e: &Value| e["generation"] == *g && e["threadId"] == thread && e["turnId"] == turn;
                        let ordinal = self.unreadable_turn_errors.iter().rev().find(|e| same(e)).and_then(|e| e["ordinalInTurn"].as_u64()).unwrap_or(0) + 1;
                        let first = self.turn_first_notice_order(g, thread, turn).unwrap_or(self.next_order);
                        if self.unreadable_turn_errors.iter().filter(|e| same(e)).count() >= UNREADABLE_TURN_ERROR_LIMIT {
                            if let Some(oldest) = self.unreadable_turn_errors.iter().position(|e| same(e)) {
                                self.unreadable_turn_errors.remove(oldest);
                            }
                        }
                        // `kind` keeps what the host does know: a request carrying an
                        // identity is not the notification at all.
                        self.unreadable_turn_errors.push(json!({"threadId":thread,"turnId":turn,"generation":g,"receiptPosition":pos,"ordinalInTurn":ordinal,
                            "observedOrder":self.next_order,"turnFirstObservedOrder":first,
                            "kind":if frame.get("id").is_some() { "server-request-named-error" } else { "not-the-pinned-error-notification" },
                            "reason":"its meaning and retry state are not established","standing":"live-observed"}));
                        self.next_order += 1;
                    }
                    // The frame was received and refused: its receipt is consumed, so
                    // the same envelope cannot be taken again.
                    self.position = Some(pos);
                    return Err(format!("error notice refused: {reason}"));
                }
                let thread = text(p, "threadId")?;
                let turn = text(p, "turnId")?;
                let will_retry = p["willRetry"].as_bool().ok_or("missing willRetry")?;
                let same = |e: &Value| e["generation"] == *g && e["threadId"] == thread && e["turnId"] == turn;
                let ordinal = self.turn_errors.iter().rev().find(|e| same(e)).and_then(|e| e["ordinalInTurn"].as_u64()).unwrap_or(0) + 1;
                // The turn's place in the receiving order is its first notice's,
                // carried by every later one so that the cap below cannot move it.
                let first = self.turn_first_notice_order(g, thread, turn).unwrap_or(self.next_order);
                // The newest of a turn are kept; `ordinalInTurn` shows any gap.
                if self.turn_errors.iter().filter(|e| same(e)).count() >= TURN_ERROR_LIMIT {
                    if let Some(oldest) = self.turn_errors.iter().position(|e| same(e)) {
                        self.turn_errors.remove(oldest);
                    }
                }
                // `observedOrder` places the notice in this view's receiving order beside its items.
                self.turn_errors.push(json!({"threadId":thread,"turnId":turn,"error":p["error"],"willRetry":will_retry,"generation":g,
                    "receiptPosition":pos,"ordinalInTurn":ordinal,"observedOrder":self.next_order,"turnFirstObservedOrder":first,"laterFrameForTurn":false,"standing":"live-observed"}));
                self.next_order += 1;
            }
            Some("thread/goal/updated") => {
                self.goals.insert(
                    text(p, "threadId")?.into(),
                    json!({"native":p["goal"],"source":frame["method"],"position":pos}),
                );
            }
            Some("thread/goal/cleared") => {
                self.goals.insert(
                    text(p, "threadId")?.into(),
                    json!({"native":null,"source":frame["method"],"position":pos}),
                );
            }
            _ => {}
        }
        self.position = Some(pos);
        Ok(())
    }
    /// The receiving order of the first notice, readable or not, held for this turn.
    fn turn_first_notice_order(&self, generation: &Value, thread: &str, turn: &str) -> Option<u64> {
        self.turn_errors.iter().chain(self.unreadable_turn_errors.iter())
            .filter(|e| e["generation"] == *generation && e["threadId"] == thread && e["turnId"] == turn)
            .filter_map(|e| e["turnFirstObservedOrder"].as_u64()).min()
    }
    fn later_frame_for_turn(&mut self, generation: &Value, thread: &str, turn: &str) {
        for error in self.turn_errors.iter_mut().filter(|e| e["generation"] == *generation && e["threadId"] == thread && e["turnId"] == turn) {
            error["laterFrameForTurn"] = json!(true);
        }
    }
    fn item(
        &mut self,
        thread: &str,
        turn: &str,
        native: &Value,
        completed: bool,
        recovered: bool,
        frame: Option<Value>,
    ) -> Result<(), String> {
        let id = text(native, "id")?;
        let key = native_key(thread, turn, id);
        let kind = text(native, "type")?;
        // A history page can be older than frames already received: it fills
        // absent, unknown or not-completed rows but never replaces a terminal one.
        if recovered {
            if let Some(old) = self.items.get(&key) {
                if matches!(old["displayState"].as_str(), Some("completed" | "failed" | "declined" | "interrupted")) {
                    return Ok(());
                }
            }
        }
        let status = native["status"].as_str();
        let state = if recovered && status == Some("inProgress") {
            "unknown"
        } else if completed {
            status.unwrap_or("completed")
        } else {
            "in-progress"
        };
        let mut row = json!({"threadId":thread,"turnId":turn,"native":native,"displayState":state,
            "standing":if recovered{"recovered-from-supplier"}else{"live-observed"},"observationEnded":false});
        if let Some(old) = self.items.get(&key) {
            if let Some(start) = old.get("startNative") {
                row["startNative"] = start.clone();
            }
            if let Some(receipt) = old.get("receipt") {
                row["receipt"] = receipt.clone();
            }
            row["observedOrder"] = old["observedOrder"].clone();
        }
        if row["observedOrder"].is_null() {
            row["observedOrder"] = json!(self.next_order);
            self.next_order += 1;
        }
        if !completed {
            row["startNative"] = native.clone();
        }
        if let Some(frame) = frame {
            row["sourceFrame"] = frame;
        }
        if kind == "plan" && completed {
            let revision_id = format!("pi:v2:{key}");
            let ordinal = self
                .revisions
                .iter()
                .filter(|r| r["kind"] == "plan-item" && r["threadId"] == thread)
                .count()
                + 1;
            let content = json!({"text":native["text"]});
            let revision = json!({"revisionId":revision_id,"kind":"plan-item","threadId":thread,"turnId":turn,"itemId":id,
                "ordinal":ordinal,"content":content,"contentIdentity":identity(&content),"standing":if recovered{"recovered-from-supplier"}else{"live-observed"},
                "producedInMode":"not-known","typesPin":self.types_pin,"observedVersionLabel":self.version});
            if let Some(existing) = self
                .revisions
                .iter_mut()
                .find(|r| r["revisionId"] == revision_id)
            {
                let ordinal = existing["ordinal"].clone();
                *existing = revision;
                existing["ordinal"] = ordinal;
            } else {
                self.revisions.push(revision);
            }
        }
        if kind == "collabAgentToolCall" {
            if let Some(ids) = native["receiverThreadIds"].as_array() {
                for child in ids {
                    let id = child.as_str().ok_or("invalid child identity")?;
                    let node=self.descendants.entry(id.into()).or_insert_with(||json!({"threadId":id,"parentThreadId":native["senderThreadId"],"parentSource":"collabAgentToolCall.senderThreadId","guidance":"not-known"}));
                    node["lastNativeCall"] = native.clone();
                    node["statusSource"] = json!("collabAgentToolCall.agentsStates");
                    node["lastObservedStatus"] = native["agentsStates"]
                        .get(id)
                        .cloned()
                        .unwrap_or(Value::Null);
                    node["observationEnded"] = json!(false);
                }
            }
        } else if kind == "subAgentActivity" {
            // The containing thread is inferred to be the parent only when the
            // named thread is not the containing thread itself, not the root
            // agent (`agentPath` "/root"), and not already known as the
            // containing thread's ancestor: a sub-agent's own history can carry
            // activity naming its parent (trial witness 2026-10-10, where the
            // parent was shown as a "descendant of" its own child).
            // A `started` row is shown in the thread that spawned the named
            // one. It corrects only a purely inferred parent: it drops an
            // inverted inference of the containing thread under the named one
            // (only where the named thread can then be placed under it) and
            // re-parents a node whose parent was inferred, whatever the
            // arrival order (a grandchild's activity read before its
            // ancestors', as in history recovery). A parent set by a `started`
            // row or by `collabAgentToolCall.senderThreadId` is never removed
            // or moved, and the ancestor guard holds for the correction too:
            // a descendant's own `started` row naming one of its ancestors (a
            // sub-agent with forked context can carry its spawner's rows)
            // changes nothing.
            const INFERRED: &str = "subAgentActivity containing thread (inference)";
            const STARTED: &str = "subAgentActivity started (spawning thread)";
            let names_root = native["agentPath"].as_str() == Some("/root");
            if let Some(id) = native["agentThreadId"].as_str().filter(|id| *id != thread && !names_root && !self.path_names_ancestor(native, thread)) {
                let started = native["kind"] == "started";
                // The inverted inference is dropped only where the correction
                // then takes effect: the named thread is not yet a node, or its
                // own parent is only inferred. Where its parent is set (by a
                // `started` row or a collab call) the row is a forked copy and
                // changes nothing, so the containing thread is kept (review of
                // #1260: a grandchild inferred under its parent, whose forked
                // history names that parent as started, was dropped).
                let correctable = self.descendants.get(id).is_none_or(|n| n["parentSource"] == INFERRED);
                if started && correctable && self.descendants.get(thread).is_some_and(|n| n["parentThreadId"] == id && n["parentSource"] == INFERRED) {
                    self.descendants.remove(thread);
                }
                if !self.is_ancestor(id, thread) {
                    if started {
                        if let Some(node) = self.descendants.get_mut(id).filter(|n| n["parentSource"] == INFERRED) {
                            node["parentThreadId"] = json!(thread);
                            node["parentSource"] = json!(STARTED);
                        }
                    }
                    let source = if started { STARTED } else { INFERRED };
                    self.descendants.entry(id.into()).or_insert_with(||json!({"threadId":id,"parentThreadId":thread,"parentSource":source,"lastNativeActivity":native,"guidance":"not-known","observationEnded":false}));
                }
            }
        }
        self.items.insert(key, row);
        Ok(())
    }
    /// The row names an agent whose `agentPath` is an ancestor of the
    /// containing thread's known path (from the containing thread's own node).
    fn path_names_ancestor(&self, native: &Value, thread: &str) -> bool {
        let (Some(named), Some(own)) = (native["agentPath"].as_str(), self.descendants.get(thread).and_then(|n| n["lastNativeActivity"]["agentPath"].as_str())) else { return false };
        own.starts_with(&format!("{named}/"))
    }
    /// `candidate` is `thread`'s parent, or an ancestor of it, among the known
    /// descendant nodes (bounded walk; a cycle ends it).
    fn is_ancestor(&self, candidate: &str, thread: &str) -> bool {
        let mut current = thread.to_owned();
        for _ in 0..=self.descendants.len() {
            match self.descendants.get(&current).and_then(|n| n["parentThreadId"].as_str()) {
                Some(parent) if parent == candidate => return true,
                Some(parent) => current = parent.to_owned(),
                None => return false,
            }
        }
        false
    }
    fn turn(&mut self, thread: &str, native: &Value, recovered: bool) -> Result<(), String> {
        let turn = text(native, "id")?;
        if recovered && native["status"] == "inProgress" {
            if let Some(old) = self.turns.get(&(thread.to_string(), turn.to_string())) {
                if old["status"] != "inProgress" {
                    return Ok(());
                }
            }
        }
        if native["status"] != "inProgress" {
            for item in self.items.values_mut() {
                if item["threadId"] == thread
                    && item["turnId"] == turn
                    && matches!(
                        item["displayState"].as_str(),
                        Some("in-progress" | "unknown")
                    )
                {
                    item["displayState"] = json!("not-completed");
                    item["endReason"] = json!("turn ended without item completion");
                }
            }
        }
        self.turns
            .insert((thread.into(), turn.into()), native.clone());
        Ok(())
    }
    /// A native history read always carries owning-home context outside its payload.
    pub fn history(
        &mut self,
        home: &str,
        method: &str,
        params: &Value,
        result: &Value,
    ) -> Result<(), String> {
        if home != self.home {
            return Err("foreign history home".into());
        }
        let thread = text(params, "threadId")?;
        match method {
            "thread/items/list" => {
                crate::native_history::require_complete_item_outputs(result)?;
                let mut entries: Vec<&Value> = result["data"].as_array().ok_or("items history absent")?.iter().collect();
                // Receipt order follows conversation order within a page.
                if params["sortDirection"] == "desc" {
                    entries.reverse();
                }
                for entry in entries {
                    let native = entry.get("item").unwrap_or(entry);
                    let turn = entry
                        .get("turnId")
                        .and_then(Value::as_str)
                        .or_else(|| params["turnId"].as_str())
                        .ok_or("history turn absent")?;
                    self.item(
                        thread,
                        turn,
                        native,
                        native["status"] != "inProgress",
                        true,
                        None,
                    )?;
                }
                // A list of one turn's items cannot say whether a later turn
                // exists, so only a list across the conversation is read.
                if params["turnId"].as_str().is_none() {
                    let ascending = params["sortDirection"] != "desc";
                    let mut turns: Vec<(String, Vec<Value>, bool)> = Vec::new();
                    for entry in result["data"].as_array().into_iter().flatten() {
                        let native = entry.get("item").unwrap_or(entry);
                        let turn = entry["turnId"].as_str().unwrap_or_default().to_owned();
                        match turns.last_mut() {
                            Some((last, items, _)) if *last == turn => items.push(native.clone()),
                            _ => turns.push((turn, vec![native.clone()], true)),
                        }
                    }
                    // Each turn's items in conversation order, as a turn carries them.
                    if !ascending {
                        for (_, items, _) in turns.iter_mut() {
                            items.reverse();
                        }
                    }
                    self.asked_history(thread, turns, ascending, params, result);
                }
            }
            "thread/turns/list" => {
                let mut turns: Vec<&Value> = result["data"].as_array().ok_or("turn history absent")?.iter().collect();
                // Turns default to descending; receive them in conversation order.
                if params["sortDirection"] != "asc" {
                    turns.reverse();
                }
                for turn in turns {
                    for item in turn["items"].as_array().into_iter().flatten() {
                        self.item(thread, text(turn, "id")?, item, item["status"] != "inProgress", true, None)?;
                    }
                    self.turn(thread, turn, true)?;
                }
                let ascending = params["sortDirection"] == "asc";
                self.asked_history(thread, Self::asked_turns(result["data"].as_array()), ascending, params, result);
            }
            "thread/read" => {
                let native = &result["thread"];
                if native["id"] != thread {
                    return Err("history thread mismatch".into());
                }
                if let Some(node) = self.descendants.get_mut(thread) {
                    node["nativeThread"] = native.clone();
                    node["guidance"] = json!("not-known");
                    node["observationEnded"] = json!(false);
                }
                if let Some(turns) = native["turns"].as_array() {
                    for turn in turns {
                        if let Some(items) = turn["items"].as_array() {
                            for item in items {
                                self.item(
                                    thread,
                                    text(turn, "id")?,
                                    item,
                                    item["status"] != "inProgress",
                                    true,
                                    None,
                                )?;
                            }
                        }
                        self.turn(thread, turn, true)?;
                    }
                }
                // Turns are only present when asked for; without them the read
                // says nothing about the conversation's messages.
                if params["includeTurns"] == true {
                    self.asked_history(thread, Self::asked_turns(native["turns"].as_array()), true, &json!({}), &json!({}));
                }
            }
            "thread/goal/get" => {
                self.goals.insert(
                    thread.into(),
                    json!({"native":result["goal"],"source":"thread/goal/get"}),
                );
            }
            _ => return Err("unsupported native history read".into()),
        }
        Ok(())
    }
    /// A conversation is read from its start where this generation's own
    /// `thread/start` reply named it: every later item of it is received here.
    pub(crate) fn asked_thread_started(&mut self, thread: &str) {
        if self.is_closed() || thread.is_empty() {
            return;
        }
        self.asked.entry(thread.into()).or_insert(AskedState { anchor: None, waiting: None });
    }
    /// The turns a `thread/resume` or `thread/fork` reply carries, read for
    /// the conversation it names. The reply is the conversation's newest end,
    /// but only a decisive item establishes anything: an empty `turns` (as the
    /// App's own resume asks, with `excludeTurns`) says nothing.
    pub(crate) fn asked_continuation_reply(&mut self, result: &Value) {
        let thread = &result["thread"];
        let Some(id) = thread["id"].as_str().filter(|s| !s.is_empty()) else { return };
        if thread["turns"].as_array().is_none_or(Vec::is_empty) {
            return;
        }
        // Turns and their items arrive oldest first; read them newest first.
        let mut turns = Self::asked_turns(thread["turns"].as_array());
        turns.reverse();
        for (_, items, _) in turns.iter_mut() {
            items.reverse();
        }
        self.asked_read(id, turns, true, false);
    }
    fn is_closed(&self) -> bool {
        self.generation.as_ref().is_some_and(|g| self.closed.contains(g))
    }
    /// Turns as (id, items, whether its items are all present): a turn whose
    /// `itemsView` is `summary` or `notLoaded` may leave items out.
    fn asked_turns(turns: Option<&Vec<Value>>) -> Vec<(String, Vec<Value>, bool)> {
        turns
            .into_iter()
            .flatten()
            .map(|t| {
                let full = t.get("itemsView").is_none_or(|v| v.is_null() || *v == "full");
                (t["id"].as_str().unwrap_or_default().to_owned(), t["items"].as_array().cloned().unwrap_or_default(), full)
            })
            .collect()
    }
    fn asked_live(&mut self, thread: &str, turn: &str, native: &Value, completed: bool) {
        let id = native["id"].as_str().unwrap_or_default();
        let waiting = match decisive(native) {
            Some(Decisive::Question) if completed => Some(asked_entry(thread, turn, native)),
            Some(Decisive::Person) => None,
            _ => return,
        };
        self.asked.insert(thread.into(), AskedState { anchor: Some((turn.into(), id.into())), waiting });
    }
    /// A paged history response: `turns` in the response's own order. It is
    /// the conversation's newest end when it is the first page newest first,
    /// or the last page oldest first; it is the whole conversation when it is
    /// both the first page and the last.
    fn asked_history(&mut self, thread: &str, turns: Vec<(String, Vec<Value>, bool)>, ascending: bool, params: &Value, result: &Value) {
        let first_page = params["cursor"].is_null();
        let last_page = result["nextCursor"].is_null();
        let newest_end = if ascending { last_page } else { first_page };
        let mut turns = turns;
        if ascending {
            turns.reverse();
        }
        for (_, items, _) in turns.iter_mut() {
            items.reverse();
        }
        if newest_end {
            self.asked_read(thread, turns, true, first_page && last_page);
        }
    }
    /// Read newest to oldest (`turns` and their items already in that order).
    /// The first message from the person met means none is waiting; the first
    /// question met means that one is waiting; meeting neither means none only
    /// where the reading is the whole conversation. A turn whose items may be
    /// incomplete ends the reading. Against what is already established, a
    /// reading applies only where it is at least as new: the established item
    /// is in it at or after (older than) what it found, or what it found is in
    /// a turn newer than the established item's turn. A history read can be
    /// older than items received live, and the two share no reliable order.
    fn asked_read(&mut self, thread: &str, turns: Vec<(String, Vec<Value>, bool)>, newest_end: bool, whole: bool) {
        if self.is_closed() || !newest_end {
            return;
        }
        let order: Vec<&str> = turns.iter().map(|(t, _, _)| t.as_str()).collect();
        let mut seen: Vec<(usize, &str, &Value)> = Vec::new();
        let mut complete = true;
        for (index, (turn, items, full)) in turns.iter().enumerate() {
            if !full {
                complete = false;
                break;
            }
            for item in items {
                seen.push((index, turn.as_str(), item));
            }
        }
        let found = seen.iter().position(|(_, _, item)| decisive(item).is_some());
        let reading = match found {
            Some(k) => {
                let (_, turn, item) = seen[k];
                let waiting = matches!(decisive(item), Some(Decisive::Question)).then(|| asked_entry(thread, turn, item));
                AskedState { anchor: Some((turn.into(), item["id"].as_str().unwrap_or_default().into())), waiting }
            }
            None if whole && complete => AskedState { anchor: None, waiting: None },
            None => return,
        };
        let applies = match self.asked.get(thread).and_then(|s| s.anchor.as_ref()) {
            None => true,
            Some((anchor_turn, anchor_item)) => {
                let at = seen.iter().position(|(_, t, i)| t == anchor_turn && i["id"] == anchor_item.as_str());
                match (found, at) {
                    (Some(k), Some(a)) => k <= a,
                    (Some(k), None) => order.iter().position(|t| t == anchor_turn).is_some_and(|a| seen[k].0 < a),
                    (None, _) => false,
                }
            }
        };
        if applies {
            self.asked.insert(thread.into(), reading);
        }
    }
    fn asked_snapshot(&self) -> Value {
        json!({"read":self.asked.keys().collect::<Vec<_>>(),
            "waiting":self.asked.values().filter_map(|s| s.waiting.clone()).collect::<Vec<_>>()})
    }
    pub fn snapshot_with_requests(&self, requests: &[Value]) -> Value {
        let mut snapshot = self.snapshot();
        for item in snapshot["items"].as_array_mut().unwrap() {
            let request = requests.iter().rev().find(|r| {
                self.generation.as_ref() == Some(&r["generation"])
                    && !self.closed.contains(&r["generation"])
                    && r["nativeParameters"]["threadId"] == item["threadId"]
                    && r["nativeParameters"]["turnId"] == item["turnId"]
                    && r["nativeParameters"]["itemId"] == item["native"]["id"]
            });
            if let Some(request) = request {
                item["requestRef"] = json!({"generation":request["generation"],"requestIdentity":request["requestIdentity"]});
                item["settlementOrigin"] = request["settlement"]
                    .get("origin")
                    .cloned()
                    .unwrap_or(Value::Null);
                if request["state"] == "outstanding"
                    && self.generation.as_ref() == Some(&request["generation"])
                {
                    item["displayState"] = json!("waiting-on-request");
                }
            }
        }
        snapshot
    }
    pub fn snapshot(&self) -> Value {
        json!({"home":self.home,"generation":self.generation,"position":self.position,
            // True once this view's generation has closed: nothing here is a current reading then.
            "observationEnded":self.generation.as_ref().is_some_and(|g|self.closed.contains(g)),"supplierStanding":self.supplier_standing,"distributionEvidence":self.distribution_evidence,
            "items":self.items.values().collect::<Vec<_>>(),"revisions":self.revisions,"descendants":self.descendants.values().collect::<Vec<_>>(),
            "turns":self.turns.values().collect::<Vec<_>>(),
            "modelReroutes":self.reroutes,
            "turnErrors":self.turn_errors,"unreadableTurnErrors":self.unreadable_turn_errors,
            // The agent's questions that do not wait: the conversations read in
            // this generation, and the latest question of each not followed by a
            // message from the person. A conversation not listed is not read.
            "askedQuestions":self.asked_snapshot(),
            "turnRecords":self.turns.keys().map(|(thread,turn)|json!({"threadId":thread,"turnId":turn})).collect::<Vec<_>>(),"typesPin":self.types_pin,"goals":self.goals,"checklistGaps":self.checklist_gaps,
            "limits":["Tool success is not checking, acceptance or reliance.","Parent completion says nothing about children.","Child completion, return, review and integration are not inferred.","Plan item references require this receiving home namespace; standalone cross-home export remains unsupported."]})
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn g(counter: u64) -> Value {
        json!({"appSession":"s:é","home":"h","spawnCounter":counter})
    }
    fn view() -> NativeView {
        let mut v = NativeView::new("h".into()).unwrap();
        v.ready(
            g(1),
            json!("codex 0.169.0"),
            json!("unverified-development"),
        )
        .unwrap();
        v
    }
    fn frame(v: &mut NativeView, pos: u64, method: &str, params: Value) {
        v.consume(
            &json!({"generation":g(1),"position":pos,"frame":{"method":method,"params":params}}),
        )
        .unwrap();
    }
    #[test]
    fn replay_constructed_design_plans_keeps_native_and_generated_revision_keys() {
        let mut view = NativeView::new("fixture-account-home".into()).unwrap();
        for line in include_str!("../resources/runtime_core/plans.constructed.jsonl").lines() {
            let row: Value = serde_json::from_str(line).unwrap();
            match row["ev"].as_str().unwrap() {
                "ready" => view
                    .ready(
                        row["g"].clone(),
                        row["record"]["observedLabel"].clone(),
                        json!("unverified-development"),
                    )
                    .unwrap(),
                "frame" => view
                    .consume(
                        &json!({"generation":row["g"],"position":row["pos"],"frame":row["frame"]}),
                    )
                    .unwrap(),
                "read" => view
                    .history(
                        row["home"].as_str().unwrap(),
                        row["method"].as_str().unwrap(),
                        &row["params"],
                        &row["result"],
                    )
                    .unwrap(),
                _ => panic!("unsupported fixture event"),
            }
        }
        let snapshot = view.snapshot();
        let revisions = snapshot["revisions"].as_array().unwrap();
        assert_eq!(revisions.len(), 5);
        let schema: Value = serde_json::from_str(include_str!(
            "../resources/runtime_core/npt.plan-revision.schema.json"
        ))
        .unwrap();
        let validator = jsonschema::options().offline().build(&schema).unwrap();
        for revision in revisions {
            assert_eq!(revision["revisionId"], revision_key(revision).unwrap());
            validator.validate(revision).unwrap();
        }
        assert_eq!(revisions[3]["unchangedFromPrevious"], true);
        assert_eq!(snapshot["supplierStanding"], "unverified-development");
    }
    #[test]
    fn scope_and_receipt_guards_and_checklist_restart_gap() {
        let mut v = view();
        let params = json!({"threadId":"t:.é","turnId":"u:","explanation":null,"plan":[{"step":"work","status":"pending"}]});
        frame(&mut v, 1, "turn/plan/updated", params.clone());
        let reference = v.snapshot()["revisions"][0].clone();
        assert_eq!(v.snapshot()["typesPin"], crate::hosting::DECLARED_PIN);
        assert_eq!(reference["typesPin"], crate::hosting::DECLARED_PIN);
        assert_eq!(reference["revisionId"], "cl:v2:czrDqQ.aA.1.dDouw6k.dTo.1");
        for foreign in [
            json!(1),
            json!({"appSession":"foreign","home":"h","spawnCounter":1}),
            json!({"appSession":"s:é","home":"other","spawnCounter":1}),
        ] {
            assert!(v.consume(&json!({"generation":foreign,"position":2,"frame":{"method":"turn/plan/updated","params":params}})).is_err());
        }
        assert!(v
            .consume(&json!({"generation":g(1),"position":1,"frame":{}}))
            .is_err());
        assert!(v.ready(g(2), Value::Null, Value::Null).is_err());
        v.close(&g(1)).unwrap();
        v.ready(g(2), Value::Null, Value::Null).unwrap();
        assert!(v.close(&g(1)).is_err());
        assert_eq!(v.snapshot()["revisions"], json!([]));
        assert_eq!(v.snapshot()["checklistGaps"].as_array().unwrap().len(), 1);
        assert!(v
            .history(
                "other",
                "thread/items/list",
                &json!({"threadId":"t"}),
                &json!({"data":[]})
            )
            .is_err());
    }
    #[test]
    fn native_completed_plan_replaces_preview_and_same_id_in_different_turn_does_not_alias() {
        let mut v = view();
        frame(
            &mut v,
            1,
            "item/plan/delta",
            json!({"threadId":"t","turnId":"u","itemId":"i","delta":"preview"}),
        );
        frame(
            &mut v,
            2,
            "item/completed",
            json!({"threadId":"t","turnId":"u","item":{"id":"i","type":"plan","text":"final","nativeExtra":true}}),
        );
        frame(
            &mut v,
            3,
            "item/completed",
            json!({"threadId":"t","turnId":"u2","item":{"id":"i","type":"plan","text":"other"}}),
        );
        let snapshot = v.snapshot();
        assert_eq!(snapshot["items"].as_array().unwrap().len(), 2);
        assert_eq!(snapshot["revisions"].as_array().unwrap().len(), 2);
        assert!(snapshot["items"]
            .as_array()
            .unwrap()
            .iter()
            .any(|i| i["native"]["nativeExtra"] == true));
        assert!(!serde_json::to_string(&snapshot["items"])
            .unwrap()
            .contains("preview"));
    }
    #[test]
    fn tool_status_children_and_turn_end_do_not_manufacture_outcomes() {
        let mut v = view();
        frame(
            &mut v,
            1,
            "item/started",
            json!({"threadId":"p","turnId":"u","item":{"id":"cmd","type":"commandExecution","status":"inProgress","source":"agent"}}),
        );
        frame(
            &mut v,
            2,
            "item/completed",
            json!({"threadId":"p","turnId":"u","item":{"id":"spawn","type":"collabAgentToolCall","status":"completed","senderThreadId":"p","receiverThreadIds":["child"],"agentsStates":{"child":{"status":"running"}},"requestedModel":"model"}}),
        );
        frame(
            &mut v,
            3,
            "item/started",
            json!({"threadId":"child","turnId":"child-turn","item":{"id":"future","type":"futureTool","raw":42}}),
        );
        frame(
            &mut v,
            4,
            "turn/completed",
            json!({"threadId":"p","turn":{"id":"u","status":"interrupted"}}),
        );
        let snapshot = v.snapshot();
        assert_eq!(
            snapshot["descendants"][0]["lastObservedStatus"]["status"],
            "running"
        );
        assert!(snapshot["items"]
            .as_array()
            .unwrap()
            .iter()
            .any(|i| i["native"]["id"] == "cmd" && i["displayState"] == "not-completed"));
        assert!(snapshot["items"]
            .as_array()
            .unwrap()
            .iter()
            .any(|i| i["native"]["id"] == "future"
                && i["displayState"] == "in-progress"
                && i["native"]["raw"] == 42));
        v.close(&g(1)).unwrap();
        assert_eq!(v.snapshot()["descendants"][0]["observationEnded"], true);
    }
    // Trial witness 2026-10-10 (c): the parent viewing its child. The child's
    // own history carries subAgentActivity naming the parent; that never makes
    // the parent a descendant of its child.
    #[test]
    fn sub_agent_activity_in_a_child_naming_its_parent_does_not_invert_the_relation() {
        for path in [json!("/root"), Value::Null] {
            let mut v = view();
            frame(&mut v, 1, "item/completed", json!({"threadId":"parent","turnId":"u","item":{"id":"a1","type":"subAgentActivity","kind":"started","agentPath":"/root/summarize_trial","agentThreadId":"child"}}));
            frame(&mut v, 2, "item/completed", json!({"threadId":"child","turnId":"c","item":{"id":"a2","type":"subAgentActivity","kind":"interacted","agentPath":path,"agentThreadId":"parent"}}));
            frame(&mut v, 3, "item/completed", json!({"threadId":"child","turnId":"c","item":{"id":"a3","type":"subAgentActivity","kind":"interacted","agentThreadId":"child"}}));
            let nodes = v.snapshot()["descendants"].as_array().unwrap().clone();
            assert_eq!(nodes.len(), 1, "{nodes:?}");
            assert_eq!((&nodes[0]["threadId"], &nodes[0]["parentThreadId"]), (&json!("child"), &json!("parent")));
        }
        // A thread named as the root agent is never a descendant.
        let mut v = view();
        frame(&mut v, 1, "item/completed", json!({"threadId":"child","turnId":"c","item":{"id":"a","type":"subAgentActivity","kind":"interacted","agentPath":"/root","agentThreadId":"parent"}}));
        assert_eq!(v.snapshot()["descendants"], json!([]));
        // A grandchild is still placed under the child that shows its activity.
        let mut v = view();
        frame(&mut v, 1, "item/completed", json!({"threadId":"parent","turnId":"u","item":{"id":"a1","type":"subAgentActivity","agentPath":"/root/a","agentThreadId":"child"}}));
        frame(&mut v, 2, "item/completed", json!({"threadId":"child","turnId":"c","item":{"id":"a2","type":"subAgentActivity","agentPath":"/root/a/b","agentThreadId":"grandchild"}}));
        let nodes = v.snapshot()["descendants"].as_array().unwrap().clone();
        assert!(nodes.iter().any(|n| n["threadId"] == "grandchild" && n["parentThreadId"] == "child"), "{nodes:?}");
    }
    // Review of #1260 (2, 4): arrival order. A descendant's activity naming
    // its parent, seen before the parent's own `started` row (history recovery,
    // or no agentPath), is corrected by that row; no cycle is left.
    #[test]
    fn a_started_row_corrects_an_inference_made_in_the_wrong_order() {
        let started = |id: &str, at: &str, child: &str, path: &str| json!({"threadId":at,"turnId":"u","item":{"id":id,"type":"subAgentActivity","kind":"started","agentPath":path,"agentThreadId":child}});
        let interacted = |id: &str, at: &str, other: &str| json!({"threadId":at,"turnId":"c","item":{"id":id,"type":"subAgentActivity","kind":"interacted","agentThreadId":other}});
        let parents = |v: &NativeView| {
            let mut pairs: Vec<(String, String)> = v.snapshot()["descendants"].as_array().unwrap().iter()
                .map(|n| (n["threadId"].as_str().unwrap().to_owned(), n["parentThreadId"].as_str().unwrap().to_owned())).collect();
            pairs.sort();
            pairs
        };
        // Depth 1: the child's row naming its parent arrives first.
        let mut v = view();
        frame(&mut v, 1, "item/completed", interacted("i1", "child", "parent"));
        frame(&mut v, 2, "item/completed", started("s1", "parent", "child", "/root/a"));
        assert_eq!(parents(&v), vec![("child".into(), "parent".into())]);
        // Depth 2: the grandchild's row naming the child, then the child's started row, then the parent's.
        let mut v = view();
        frame(&mut v, 1, "item/completed", interacted("i1", "grandchild", "child"));
        frame(&mut v, 2, "item/completed", started("s1", "child", "grandchild", "/root/a/b"));
        frame(&mut v, 3, "item/completed", started("s2", "parent", "child", "/root/a"));
        assert_eq!(parents(&v), vec![("child".into(), "parent".into()), ("grandchild".into(), "child".into())]);
        // A started row never overrides the parent a collab call names.
        let mut v = view();
        frame(&mut v, 1, "item/completed", json!({"threadId":"p","turnId":"u","item":{"id":"spawn","type":"collabAgentToolCall","status":"completed","senderThreadId":"p","receiverThreadIds":["child"],"agentsStates":{}}}));
        frame(&mut v, 2, "item/completed", started("s1", "other", "child", "/root/x"));
        assert_eq!(parents(&v), vec![("child".into(), "p".into())]);
        // Recheck of #1260 (steal probe): a descendant's own `started` row
        // naming its ancestor (forked context copying its spawner's rows)
        // neither moves the ancestor nor drops the descendant.
        let mut v = view();
        frame(&mut v, 1, "item/completed", started("s1", "parent", "child", "/root/a"));
        frame(&mut v, 2, "item/completed", started("s2", "child", "grandchild", "/root/a/b"));
        frame(&mut v, 3, "item/completed", started("s3", "grandchild", "child", "/root/a"));
        assert_eq!(parents(&v), vec![("child".into(), "parent".into()), ("grandchild".into(), "child".into())]);
        // The same without agentPath, by the ancestor guard alone.
        let bare = |id: &str, at: &str, child: &str| json!({"threadId":at,"turnId":"u","item":{"id":id,"type":"subAgentActivity","kind":"started","agentThreadId":child}});
        let mut v = view();
        frame(&mut v, 1, "item/completed", bare("s1", "parent", "child"));
        frame(&mut v, 2, "item/completed", bare("s2", "child", "grandchild"));
        frame(&mut v, 3, "item/completed", bare("s3", "grandchild", "child"));
        assert_eq!(parents(&v), vec![("child".into(), "parent".into()), ("grandchild".into(), "child".into())]);
        // Depth 1 without agentPath: a child's `started` row naming its parent
        // never makes the parent a descendant of the child.
        let mut v = view();
        frame(&mut v, 1, "item/completed", bare("s1", "parent", "child"));
        frame(&mut v, 2, "item/completed", bare("s2", "child", "parent"));
        assert_eq!(parents(&v), vec![("child".into(), "parent".into())]);
        assert_eq!(v.snapshot()["descendants"][0]["parentSource"], "subAgentActivity started (spawning thread)");
        // A parent set by a `started` row is not moved by another thread's `started` row.
        frame(&mut v, 3, "item/completed", bare("s3", "other", "child"));
        assert_eq!(parents(&v), vec![("child".into(), "parent".into())]);
    }
    // Review of #1260 (leftovers). (a) A grandchild known only from its
    // parent's non-`started` row, with no agentPath anywhere, whose forked
    // history carries a `started` row naming that parent, is kept: the
    // parent's own parent is set, so the row cannot be a correction.
    // (b) The agentPath-prefix guard: a grandchild's `started` row naming the
    // child by an ancestor path changes nothing, even where the child's parent
    // is only inferred (so only the path guard stops the inversion).
    #[test]
    fn a_forked_started_row_naming_a_set_parent_keeps_the_descendant() {
        let parents = |v: &NativeView| {
            let mut pairs: Vec<(String, String)> = v.snapshot()["descendants"].as_array().unwrap().iter()
                .map(|n| (n["threadId"].as_str().unwrap().to_owned(), n["parentThreadId"].as_str().unwrap().to_owned())).collect();
            pairs.sort();
            pairs
        };
        let row = |id: &str, at: &str, kind: &str, other: &str, path: Option<&str>| {
            let mut item = json!({"id":id,"type":"subAgentActivity","kind":kind,"agentThreadId":other});
            if let Some(path) = path {
                item["agentPath"] = json!(path);
            }
            json!({"threadId":at,"turnId":"u","item":item})
        };
        let expected: Vec<(String, String)> = vec![("child".into(), "parent".into()), ("grandchild".into(), "child".into())];
        // (a) No agentPath on any row.
        let mut v = view();
        frame(&mut v, 1, "item/completed", row("s1", "parent", "started", "child", None));
        frame(&mut v, 2, "item/completed", row("i1", "child", "interacted", "grandchild", None));
        frame(&mut v, 3, "item/completed", row("s2", "grandchild", "started", "child", None));
        assert_eq!(parents(&v), expected);
        // (b) As the review case states it: parent `started` child; child
        // `interacted` grandchild at "/root/a/b"; grandchild `started` child at "/root/a".
        let mut v = view();
        frame(&mut v, 1, "item/completed", row("s1", "parent", "started", "child", None));
        frame(&mut v, 2, "item/completed", row("i1", "child", "interacted", "grandchild", Some("/root/a/b")));
        frame(&mut v, 3, "item/completed", row("s2", "grandchild", "started", "child", Some("/root/a")));
        assert_eq!(parents(&v), expected);
        // (b') The same with the child's parent only inferred: here the path
        // guard alone keeps the child under its parent and the grandchild.
        let mut v = view();
        frame(&mut v, 1, "item/completed", row("i0", "parent", "interacted", "child", Some("/root/a")));
        frame(&mut v, 2, "item/completed", row("i1", "child", "interacted", "grandchild", Some("/root/a/b")));
        frame(&mut v, 3, "item/completed", row("s2", "grandchild", "started", "child", Some("/root/a")));
        assert_eq!(parents(&v), expected);
    }
    #[test]
    fn streamed_deltas_are_previews_replaced_by_the_completed_item() {
        let mut v = view();
        let d = |item: &str, delta: &str| json!({"threadId":"t","turnId":"u","itemId":item,"delta":delta});
        frame(&mut v, 1, "item/started", json!({"threadId":"t","turnId":"u","item":{"id":"m","type":"agentMessage","text":""}}));
        frame(&mut v, 2, "item/agentMessage/delta", d("m", "Hel"));
        frame(&mut v, 3, "item/agentMessage/delta", d("m", "lo"));
        frame(&mut v, 4, "item/commandExecution/outputDelta", d("c", "out"));
        frame(&mut v, 5, "item/reasoning/summaryTextDelta", json!({"threadId":"t","turnId":"u","itemId":"r","delta":"second","summaryIndex":1}));
        let row = |v: &NativeView, id: &str| v.snapshot()["items"].as_array().unwrap().iter().find(|i| i["native"]["id"] == id).unwrap().clone();
        assert_eq!(row(&v, "m")["preview"], "Hello");
        assert_eq!(row(&v, "m")["displayState"], "in-progress");
        assert_eq!(row(&v, "c")["native"]["type"], "commandExecution");
        assert_eq!(row(&v, "r")["summaryPreview"], json!(["", "second"]));
        assert!(v.consume(&json!({"generation":g(1),"position":6,"frame":{"method":"item/reasoning/summaryTextDelta","params":{"threadId":"t","turnId":"u","itemId":"r","delta":"x","summaryIndex":100000}}})).is_err());
        frame(&mut v, 7, "item/completed", json!({"threadId":"t","turnId":"u","item":{"id":"m","type":"agentMessage","text":"Hello!"}}));
        assert!(row(&v, "m").get("preview").is_none());
        assert_eq!(row(&v, "m")["native"]["text"], "Hello!");
        frame(&mut v, 8, "item/agentMessage/delta", d("m", " late"));
        assert!(row(&v, "m").get("preview").is_none(), "a delta after completion does not reopen the item");
        frame(&mut v, 9, "turn/completed", json!({"threadId":"t","turn":{"id":"u","status":"interrupted"}}));
        assert_eq!(row(&v, "c")["displayState"], "not-completed");
        assert_eq!(row(&v, "c")["preview"], "out", "partial output stays with its not-completed state");
    }
    // HOSTING §8.3: `model/rerouted` (0.169.0 ModelReroutedNotification) is kept
    // as a live observation naming its thread and turn; a malformed one is refused.
    #[test]
    fn model_rerouted_is_observed_with_its_turn_and_receipt() {
        let mut v = view();
        frame(&mut v, 3, "model/rerouted", json!({"threadId":"t","turnId":"u","fromModel":"a","toModel":"b","reason":"highRiskCyberActivity"}));
        assert_eq!(v.snapshot()["modelReroutes"], json!([{"threadId":"t","turnId":"u","fromModel":"a","toModel":"b","reason":"highRiskCyberActivity","generation":g(1),"receiptPosition":3,"standing":"live-observed"}]));
        let refused = v.consume(&json!({"generation":g(1),"position":4,"frame":{"method":"model/rerouted","params":{"threadId":"t","fromModel":"a","toModel":"b"}}}));
        assert!(refused.is_err_and(|e| e.contains("turnId")));
        assert_eq!(v.snapshot()["modelReroutes"].as_array().unwrap().len(), 1);
    }
    // The case observed against an unreachable model: the turn starts, an
    // item completes, then the supplier repeats its retry notice.
    #[test]
    fn turn_error_notifications_are_kept_as_sent_with_their_retry_state() {
        let mut v = view();
        let error = json!({"message":"Reconnecting... waiting for network","additionalDetails":"Connection failed: error sending request","codexErrorInfo":{"responseStreamDisconnected":{"httpStatusCode":null}}});
        let notice = |retry: bool| json!({"threadId":"t","turnId":"u","error":error,"willRetry":retry});
        frame(&mut v, 1, "turn/started", json!({"threadId":"t","turn":{"id":"u","status":"inProgress"}}));
        frame(&mut v, 2, "item/completed", json!({"threadId":"t","turnId":"u","item":{"id":"m","type":"userMessage","content":[]}}));
        frame(&mut v, 3, "error", notice(true));
        frame(&mut v, 4, "error", notice(true));
        assert_eq!(v.snapshot()["turnErrors"], json!([
            {"threadId":"t","turnId":"u","error":error,"willRetry":true,"generation":g(1),"receiptPosition":3,"ordinalInTurn":1,"observedOrder":1,"turnFirstObservedOrder":1,"laterFrameForTurn":false,"standing":"live-observed"},
            {"threadId":"t","turnId":"u","error":error,"willRetry":true,"generation":g(1),"receiptPosition":4,"ordinalInTurn":2,"observedOrder":2,"turnFirstObservedOrder":1,"laterFrameForTurn":false,"standing":"live-observed"}]));
        // Another conversation's frame and an error for another turn change nothing here.
        frame(&mut v, 5, "item/started", json!({"threadId":"other","turnId":"u","item":{"id":"x","type":"agentMessage","text":""}}));
        frame(&mut v, 6, "error", json!({"threadId":"t","turnId":"w","error":{"message":"m"},"willRetry":false}));
        let errors = v.snapshot()["turnErrors"].clone();
        assert!(errors.as_array().unwrap().iter().all(|e| e["laterFrameForTurn"] == false));
        assert_eq!(errors[2]["ordinalInTurn"], 1);
        assert_eq!(errors[2]["willRetry"], false);
        // A later frame naming the turn marks the errors before it, and only those.
        frame(&mut v, 7, "item/agentMessage/delta", json!({"threadId":"t","turnId":"u","itemId":"a","delta":"hi"}));
        let errors = v.snapshot()["turnErrors"].clone();
        assert_eq!((errors[0]["laterFrameForTurn"].clone(), errors[1]["laterFrameForTurn"].clone(), errors[2]["laterFrameForTurn"].clone()), (json!(true), json!(true), json!(false)));
        frame(&mut v, 8, "error", notice(true));
        assert_eq!(v.snapshot()["turnErrors"][3]["laterFrameForTurn"], false);
        assert_eq!(v.snapshot()["turnErrors"][3]["ordinalInTurn"], 3);
        frame(&mut v, 9, "turn/completed", json!({"threadId":"t","turn":{"id":"u","status":"failed"}}));
        assert_eq!(v.snapshot()["turnErrors"][3]["laterFrameForTurn"], true);
        // When the generation closes the entries stay, each marked as no longer observed.
        assert_eq!(v.snapshot()["observationEnded"], false);
        v.close(&g(1)).unwrap();
        assert_eq!(v.snapshot()["observationEnded"], true);
        let closed = v.snapshot()["turnErrors"].clone();
        assert_eq!(closed.as_array().unwrap().len(), 4, "the close keeps every notice");
        assert!(closed.as_array().unwrap().iter().all(|e| e["observationEnded"] == true));
        assert_eq!(closed[3]["laterFrameForTurn"], true, "what arrived before the close is still what arrived");
    }
    // A frame the pinned ErrorNotification does not describe is given no retry
    // meaning. Where it names a thread and turn it is kept as unreadable, and
    // it counts as a later frame for the notices before it.
    #[test]
    fn an_error_notice_the_pinned_type_does_not_describe_is_refused_and_kept_as_unreadable() {
        let mut v = view();
        let refused = |v: &mut NativeView, pos: u64, frame: Value| v.consume(&json!({"generation":g(1),"position":pos,"frame":frame})).unwrap_err();
        frame(&mut v, 1, "error", json!({"threadId":"t","turnId":"u","error":{"message":"first"},"willRetry":true}));
        let mut pos = 1;
        for error in [json!({"message":"m","additionalDetails":42}), json!({"message":"m","codexErrorInfo":42}), json!({"message":"m","misalignment":"invalid"}), json!({"additionalDetails":"no message"}), json!("text")] {
            pos += 1;
            let reason = refused(&mut v, pos, json!({"method":"error","params":{"threadId":"t","turnId":"u","error":error,"willRetry":true}}));
            assert!(reason.starts_with("error notice refused: native ErrorNotification schema"), "{reason}");
        }
        pos += 1;
        assert!(refused(&mut v, pos, json!({"method":"error","params":{"threadId":"t","turnId":"u","error":{"message":"m"}}})).contains("willRetry"));
        // A server request that happens to be named `error` is not the notification, whatever its params.
        pos += 1;
        assert_eq!(refused(&mut v, pos, json!({"id":7,"method":"error","params":{"threadId":"t","turnId":"u","error":{"message":"m"},"willRetry":true}})), "error notice refused: a server request named error is not the error notification");
        let snapshot = v.snapshot();
        assert_eq!(snapshot["turnErrors"].as_array().unwrap().len(), 1, "none of them became a notice");
        assert_eq!(snapshot["turnErrors"][0]["laterFrameForTurn"], true, "a refused later notice is still a later frame for the turn");
        let unreadable = snapshot["unreadableTurnErrors"].as_array().unwrap();
        assert_eq!(unreadable.len(), 7);
        assert_eq!(unreadable[0], json!({"threadId":"t","turnId":"u","generation":g(1),"receiptPosition":2,"ordinalInTurn":1,"observedOrder":1,"turnFirstObservedOrder":0,
            "kind":"not-the-pinned-error-notification","reason":"its meaning and retry state are not established","standing":"live-observed"}));
        assert_eq!(unreadable[6]["kind"], "server-request-named-error", "what the host does know of the frame is kept");
        assert_eq!(unreadable[6]["ordinalInTurn"], 7);
        assert!(unreadable.iter().all(|e| e.get("willRetry").is_none() && e.get("error").is_none()));
        // A refused frame's receipt is consumed: the same envelope cannot be taken again.
        let again = refused(&mut v, pos, json!({"id":7,"method":"error","params":{"threadId":"t","turnId":"u","error":{"message":"m"},"willRetry":true}}));
        assert_eq!(again, "duplicate or out-of-order receipt");
        assert_eq!(v.snapshot()["unreadableTurnErrors"].as_array().unwrap().len(), 7);
        // One that names no thread or turn cannot be placed and is only refused.
        for params in [json!({"threadId":"t","error":{"message":"m"},"willRetry":true}), json!({"turnId":"u","error":{"message":"m"},"willRetry":true}), json!({})] {
            pos += 1;
            refused(&mut v, pos, json!({"method":"error","params":params}));
        }
        assert_eq!(v.snapshot()["unreadableTurnErrors"].as_array().unwrap().len(), 7);
        // A well-formed notice with every optional field is accepted whole.
        let whole = json!({"message":"blocked","additionalDetails":null,"codexErrorInfo":"other"});
        frame(&mut v, pos + 1, "error", json!({"threadId":"t","turnId":"u","error":whole,"willRetry":false}));
        assert_eq!(v.snapshot()["turnErrors"][1]["error"], whole);
        v.close(&g(1)).unwrap();
        assert!(v.snapshot()["unreadableTurnErrors"].as_array().unwrap().iter().all(|e| e["observationEnded"] == true));
    }
    #[test]
    fn turn_errors_keep_the_newest_of_a_turn_and_number_them_from_the_first() {
        let mut v = view();
        for n in 1..=(TURN_ERROR_LIMIT as u64 + 3) {
            frame(&mut v, n, "error", json!({"threadId":"t","turnId":"u","error":{"message":format!("attempt {n}")},"willRetry":true}));
        }
        frame(&mut v, 100, "error", json!({"threadId":"t","turnId":"w","error":{"message":"other turn"},"willRetry":true}));
        let snapshot = v.snapshot();
        let kept: Vec<&Value> = snapshot["turnErrors"].as_array().unwrap().iter().filter(|e| e["turnId"] == "u").collect();
        assert_eq!(kept.len(), TURN_ERROR_LIMIT);
        assert_eq!(kept[0]["ordinalInTurn"], 4);
        assert_eq!(kept[TURN_ERROR_LIMIT - 1]["ordinalInTurn"], TURN_ERROR_LIMIT as u64 + 3);
        assert_eq!(kept[TURN_ERROR_LIMIT - 1]["error"]["message"], format!("attempt {}", TURN_ERROR_LIMIT + 3));
        assert_eq!(snapshot["turnErrors"].as_array().unwrap().len(), TURN_ERROR_LIMIT + 1);
    }
    // Unreadable frames are bounded for each turn, not for the whole view:
    // many in one turn never hide another turn's or another conversation's,
    // and what was dropped is counted.
    #[test]
    fn unreadable_error_frames_are_kept_per_turn_and_numbered_from_the_first() {
        let mut v = view();
        let malformed = |thread: &str, turn: &str| json!({"method":"error","params":{"threadId":thread,"turnId":turn,"error":{"message":"m","codexErrorInfo":42},"willRetry":true}});
        let mut pos = 0;
        for _ in 0..(UNREADABLE_TURN_ERROR_LIMIT + 30) {
            pos += 1;
            v.consume(&json!({"generation":g(1),"position":pos,"frame":malformed("t","noisy")})).unwrap_err();
        }
        for (thread, turn) in [("t", "quiet"), ("other", "noisy")] {
            pos += 1;
            v.consume(&json!({"generation":g(1),"position":pos,"frame":malformed(thread, turn)})).unwrap_err();
        }
        let snapshot = v.snapshot();
        let of = |thread: &str, turn: &str| snapshot["unreadableTurnErrors"].as_array().unwrap().iter().filter(|e| e["threadId"] == thread && e["turnId"] == turn).cloned().collect::<Vec<_>>();
        let noisy = of("t", "noisy");
        assert_eq!(noisy.len(), UNREADABLE_TURN_ERROR_LIMIT);
        assert_eq!(noisy.last().unwrap()["ordinalInTurn"], UNREADABLE_TURN_ERROR_LIMIT as u64 + 30, "the count of what was received survives the cap");
        assert_eq!(noisy[0]["turnFirstObservedOrder"], 0, "and so does the turn's place");
        assert_eq!(of("t", "quiet").len(), 1, "another turn's single frame is still kept");
        assert_eq!(of("other", "noisy").len(), 1, "and another conversation's");
        assert_eq!(of("other", "noisy")[0]["ordinalInTurn"], 1);
    }
    // The cap removes a turn's oldest notices; the turn's place in the
    // receiving order must not move with them.
    #[test]
    fn a_turns_place_in_the_receiving_order_survives_the_cap_on_its_notices() {
        let mut v = view();
        frame(&mut v, 1, "error", json!({"threadId":"t","turnId":"a","error":{"message":"first of a"},"willRetry":true}));
        frame(&mut v, 2, "item/completed", json!({"threadId":"t","turnId":"b","item":{"id":"m","type":"userMessage","content":[]}}));
        for n in 0..(TURN_ERROR_LIMIT as u64 + 1) {
            frame(&mut v, 3 + n, "error", json!({"threadId":"t","turnId":"a","error":{"message":"more of a"},"willRetry":true}));
        }
        let snapshot = v.snapshot();
        let of_a: Vec<&Value> = snapshot["turnErrors"].as_array().unwrap().iter().filter(|e| e["turnId"] == "a").collect();
        assert_eq!(of_a.len(), TURN_ERROR_LIMIT);
        assert!(of_a.iter().all(|e| e["error"]["message"] == "more of a"), "the first notice itself is gone");
        let b = snapshot["items"].as_array().unwrap().iter().find(|i| i["native"]["id"] == "m").unwrap()["observedOrder"].as_u64().unwrap();
        assert!(of_a.iter().all(|e| e["turnFirstObservedOrder"].as_u64().unwrap() < b), "turn a was first received before turn b, and still reads so");
        assert!(of_a.iter().all(|e| e["observedOrder"].as_u64().unwrap() > b), "though every notice kept arrived after it");
    }
    // A turn known only by its error notice keeps its place in the receiving order.
    #[test]
    fn an_error_notice_takes_its_place_in_the_receiving_order_beside_items() {
        let mut v = view();
        frame(&mut v, 1, "error", json!({"threadId":"t","turnId":"first","error":{"message":"m"},"willRetry":true}));
        frame(&mut v, 2, "item/completed", json!({"threadId":"t","turnId":"second","item":{"id":"m","type":"userMessage","content":[]}}));
        let snapshot = v.snapshot();
        let item = snapshot["items"].as_array().unwrap().iter().find(|i| i["native"]["id"] == "m").unwrap();
        assert!(snapshot["turnErrors"][0]["observedOrder"].as_u64().unwrap() < item["observedOrder"].as_u64().unwrap());
    }
    #[test]
    fn a_stale_history_page_never_overwrites_newer_live_state() {
        let stale = json!({"data":[{"id":"u","status":"inProgress","items":[{"id":"c","type":"commandExecution","status":"inProgress","command":"x","cwd":"/","commandActions":[]}]}]});
        let row = |v: &NativeView, id: &str| v.snapshot()["items"].as_array().unwrap().iter().find(|i| i["native"]["id"] == id).unwrap().clone();
        let live = |v: &mut NativeView, from: u64| {
            frame(v, from, "turn/started", json!({"threadId":"t","turn":{"id":"u","status":"inProgress"}}));
            frame(v, from + 1, "item/started", json!({"threadId":"t","turnId":"u","item":{"id":"c","type":"commandExecution","status":"inProgress"}}));
            frame(v, from + 2, "item/completed", json!({"threadId":"t","turnId":"u","item":{"id":"c","type":"commandExecution","status":"completed","exitCode":0}}));
        };
        // Page lands after item completion, before turn completion.
        let mut v = view();
        live(&mut v, 1);
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &stale).unwrap();
        assert_eq!(row(&v, "c")["displayState"], "completed");
        assert_eq!(row(&v, "c")["standing"], "live-observed");
        frame(&mut v, 4, "turn/completed", json!({"threadId":"t","turn":{"id":"u","status":"completed"}}));
        assert_eq!(row(&v, "c")["displayState"], "completed", "an observed completion is never reread as not-completed");
        // Page lands after turn completion.
        let mut v = view();
        live(&mut v, 1);
        frame(&mut v, 4, "turn/completed", json!({"threadId":"t","turn":{"id":"u","status":"completed"}}));
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &stale).unwrap();
        assert_eq!(v.snapshot()["turns"][0]["status"], "completed", "a stale inProgress turn does not reopen a completed one");
        assert_eq!(row(&v, "c")["displayState"], "completed");
        // History still fills what live observation lacks.
        let mut v = view();
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &json!({"data":[{"id":"u","status":"completed","items":[{"id":"m","type":"agentMessage","text":"from history"}]}]})).unwrap();
        assert_eq!(row(&v, "m")["standing"], "recovered-from-supplier");
    }
    #[test]
    fn descending_turn_pages_arrive_in_conversation_order_and_previews_are_capped() {
        let mut v = view();
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &json!({"data":[
            {"id":"later","status":"completed","items":[{"id":"p2","type":"plan","text":"second"}]},
            {"id":"earlier","status":"completed","items":[{"id":"p1","type":"plan","text":"first"}]}]})).unwrap();
        let revisions = v.snapshot()["revisions"].clone();
        let ordinal = |id: &str| revisions.as_array().unwrap().iter().find(|r| r["itemId"] == id).unwrap()["ordinal"].as_u64().unwrap();
        assert!(ordinal("p1") < ordinal("p2"));
        frame(&mut v, 1, "item/started", json!({"threadId":"t","turnId":"u","item":{"id":"c","type":"commandExecution","status":"inProgress"}}));
        let chunk = "é".repeat(40 * 1024);
        for pos in 2..10 {
            frame(&mut v, pos, "item/commandExecution/outputDelta", json!({"threadId":"t","turnId":"u","itemId":"c","delta":chunk}));
        }
        let snapshot = v.snapshot();
        let c = snapshot["items"].as_array().unwrap().iter().find(|i| i["native"]["id"] == "c").unwrap();
        assert!(c["preview"].as_str().unwrap().len() <= PREVIEW_LIMIT);
        assert!(c["preview"].as_str().unwrap().ends_with('é'));
        assert_eq!(c["previewTruncated"], true);
    }
    #[test]
    fn deferred_item_history_is_refused_before_mutating_the_view() {
        let mut view = view();
        let before = view.snapshot();
        let page = json!({"data":[
            {"turnId":"u","item":{"id":"first","type":"agentMessage","text":"complete"}},
            {"turnId":"u","outputDeferred":true,"item":{"id":"second","type":"agentMessage","text":""}}
        ],"nextCursor":null});
        assert!(view.history("h", "thread/items/list", &json!({"threadId":"t","turnId":"u"}), &page).is_err());
        assert_eq!(view.snapshot(), before, "a page with deferred output cannot partly become complete history");
    }
    #[test]
    fn deferred_item_history_is_refused_by_the_workspace_response_reader() {
        let mut page = json!({"data":[{"turnId":"u","outputDeferred":true,
            "item":{"id":"message","type":"agentMessage","text":""}}],"nextCursor":null});
        assert!(crate::native_history::validate_read_response("thread/items/list", &page).is_err());
        page["data"][0]["outputDeferred"] = json!(false);
        assert!(crate::native_history::validate_read_response("thread/items/list", &page).is_ok());
    }
    #[test]
    fn observed_order_follows_first_receipt_not_identity_sort() {
        let mut v = view();
        let item = |id: &str, status: &str| json!({"threadId":"t","turnId":"u","item":{"id":id,"type":"commandExecution","status":status}});
        frame(&mut v, 1, "item/started", item("z-first", "inProgress"));
        frame(&mut v, 2, "item/plan/delta", json!({"threadId":"t","turnId":"u","itemId":"m-plan","delta":"p"}));
        frame(&mut v, 3, "item/started", item("a-third", "inProgress"));
        frame(&mut v, 4, "item/completed", item("z-first", "completed"));
        frame(&mut v, 5, "item/completed", json!({"threadId":"t","turnId":"u","item":{"id":"m-plan","type":"plan","text":"final"}}));
        v.history("h", "thread/items/list", &json!({"threadId":"t","turnId":"u"}), &json!({"data":[{"id":"a-third","type":"commandExecution","status":"completed"},{"id":"b-history","type":"agentMessage","text":"x"}]})).unwrap();
        let snapshot = v.snapshot();
        let order = |id: &str| snapshot["items"].as_array().unwrap().iter().find(|i| i["native"]["id"] == id).unwrap()["observedOrder"].as_u64().unwrap();
        assert_eq!([order("z-first"), order("m-plan"), order("a-third"), order("b-history")], [0, 1, 2, 3]);
        assert_eq!(snapshot["items"][0]["native"]["id"], "a-third");
        v.history("h", "thread/items/list", &json!({"threadId":"t","turnId":"w","sortDirection":"desc"}), &json!({"data":[{"id":"later","type":"agentMessage","text":"2"},{"id":"earlier","type":"userMessage","content":[]}]})).unwrap();
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &json!({"data":[{"id":"x","status":"completed","items":[{"id":"x1","type":"userMessage","content":[]},{"id":"x2","type":"agentMessage","text":"a"}]}]})).unwrap();
        let snapshot = v.snapshot();
        let order = |id: &str| snapshot["items"].as_array().unwrap().iter().find(|i| i["native"]["id"] == id).unwrap()["observedOrder"].as_u64().unwrap();
        assert!(order("earlier") < order("later"), "a descending page is received in conversation order");
        assert!(order("x1") < order("x2"));
        assert_eq!(snapshot["items"].as_array().unwrap().iter().find(|i| i["native"]["id"] == "x2").unwrap()["standing"], "recovered-from-supplier");
        frame(&mut v, 6, "turn/started", json!({"threadId":"t","turn":{"id":"u","status":"inProgress"}}));
        assert_eq!(v.snapshot()["turnRecords"], json!([{"threadId":"t","turnId":"u"},{"threadId":"t","turnId":"x"}]));
    }
}

#[cfg(test)]
mod request_overlay_repair_tests {
    use super::*;
    #[test]
    fn overlay_requires_full_active_generation_before_attaching_any_request_fact() {
        let current = json!({"appSession":"s","home":"h","spawnCounter":2});
        let mut v = NativeView::new("h".into()).unwrap();
        v.ready(current.clone(), Value::Null, Value::Null).unwrap();
        v.consume(&json!({"generation":current,"position":1,"frame":{"method":"item/started","params":{"threadId":"t","turnId":"u","item":{"id":"i","type":"commandExecution","status":"inProgress"}}}})).unwrap();
        let request = |g: Value, id: &str| json!({"generation":g,"requestIdentity":id,"state":"outstanding","nativeParameters":{"threadId":"t","turnId":"u","itemId":"i"},"settlement":{"origin":{"class":"person-via-interaction","actorRef":"invented"}}});
        let live = request(current.clone(), "live");
        for foreign in [
            json!({"appSession":"foreign","home":"h","spawnCounter":2}),
            json!({"appSession":"s","home":"h","spawnCounter":1}),
            json!({"appSession":"s","home":"foreign","spawnCounter":2}),
            json!(2),
        ] {
            let stale = request(foreign, "stale");
            let only = v.snapshot_with_requests(&[stale.clone()]);
            assert!(only["items"][0].get("requestRef").is_none());
            assert!(only["items"][0].get("settlementOrigin").is_none());
            assert_eq!(only["items"][0]["displayState"], "in-progress");
            let mixed = v.snapshot_with_requests(&[live.clone(), stale]);
            assert_eq!(mixed["items"][0]["requestRef"]["requestIdentity"], "live");
            assert_eq!(mixed["items"][0]["displayState"], "waiting-on-request");
        }
        v.close(&current).unwrap();
        let closed = v.snapshot_with_requests(&[live]);
        assert!(closed["items"][0].get("requestRef").is_none());
        assert!(closed["items"][0].get("settlementOrigin").is_none());
    }
}

/// The agent's question that does not wait: what the view establishes, rule by rule.
#[cfg(test)]
mod asked_question_tests {
    use super::*;
    fn g(counter: u64) -> Value {
        json!({"appSession":"s","home":"h","spawnCounter":counter})
    }
    fn view() -> NativeView {
        let mut v = NativeView::new("h".into()).unwrap();
        v.ready(g(1), Value::Null, Value::Null).unwrap();
        v
    }
    fn live(v: &mut NativeView, pos: u64, method: &str, thread: &str, turn: &str, item: Value) {
        v.consume(&json!({"generation":g(1),"position":pos,"frame":{"method":method,"params":{"threadId":thread,"turnId":turn,"item":item}}})).unwrap();
    }
    fn question(id: &str, title: &str) -> Value {
        json!({"id":id,"type":"agentMessage","text":title,"delivery":"async","questions":[{"title":title,"options":["Invented one","Invented two"]}]})
    }
    fn person(id: &str) -> Value {
        json!({"id":id,"type":"userMessage","content":[{"type":"text","text":"invented reply"}]})
    }
    fn agent(id: &str) -> Value {
        json!({"id":id,"type":"agentMessage","text":"invented text"})
    }
    fn state(v: &NativeView, thread: &str) -> AskedQuestion {
        asked_question(&v.snapshot(), thread)
    }
    fn waiting_item(v: &NativeView, thread: &str) -> Option<String> {
        match state(v, thread) {
            AskedQuestion::Waiting(e) => Some(e["itemId"].as_str().unwrap().to_owned()),
            _ => None,
        }
    }
    /// A turns/list page newest first (the supplier's default order).
    fn turns_desc(turns: Value) -> Value {
        json!({"data":turns,"nextCursor":null})
    }

    #[test]
    fn a_live_question_sets_the_waiting_entry_exactly_as_given() {
        let mut v = view();
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead);
        let title = "Invented\nline\u{0007} « title »";
        let mut q = question("call_1", title);
        q["questions"] = json!([{"title":title,"options":["A\u{202e}b"]},{"title":"free only"}]);
        live(&mut v, 1, "item/started", "t", "u", q.clone());
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead, "a started item is not yet the question");
        live(&mut v, 2, "item/completed", "t", "u", q);
        let AskedQuestion::Waiting(entry) = state(&v, "t") else { panic!("not waiting") };
        assert_eq!(entry, json!({"threadId":"t","turnId":"u","itemId":"call_1",
            "questions":[{"title":title,"options":["A\u{202e}b"]},{"title":"free only","options":null}]}));
        assert_eq!(v.snapshot()["askedQuestions"], json!({"read":["t"],"waiting":[entry]}));
    }
    #[test]
    fn a_live_message_from_the_person_after_it_clears_it_and_marks_nothing_answered() {
        let mut v = view();
        live(&mut v, 1, "item/completed", "t", "u", question("q", "Invented?"));
        live(&mut v, 2, "item/completed", "t", "u", agent("after"));
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q"), "the agent's own later text does not clear it");
        live(&mut v, 3, "item/started", "t", "u2", person("p"));
        assert_eq!(state(&v, "t"), AskedQuestion::None);
        assert!(!serde_json::to_string(&v.snapshot()["askedQuestions"]).unwrap().contains("answer"));
    }
    #[test]
    fn a_second_question_replaces_the_first() {
        let mut v = view();
        live(&mut v, 1, "item/completed", "t", "u", question("q1", "First?"));
        live(&mut v, 2, "item/completed", "t", "u", question("q2", "Second?"));
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q2"));
        assert_eq!(v.snapshot()["askedQuestions"]["waiting"].as_array().unwrap().len(), 1);
    }
    #[test]
    fn an_item_without_async_delivery_or_with_no_questions_is_not_a_question() {
        let mut v = view();
        let mut no_delivery = question("a", "x");
        no_delivery.as_object_mut().unwrap().remove("delivery");
        let mut other_delivery = question("b", "x");
        other_delivery["delivery"] = json!("sync");
        let mut empty = question("c", "x");
        empty["questions"] = json!([]);
        let mut null = question("d", "x");
        null["questions"] = Value::Null;
        for (pos, item) in [no_delivery, other_delivery, empty, null].into_iter().enumerate() {
            live(&mut v, pos as u64 + 1, "item/completed", "t", "u", item);
        }
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead);
        // And in history: such an item is passed over, not taken as the question.
        let mut empty = question("e", "x");
        empty["questions"] = json!([]);
        v.history("h", "thread/turns/list", &json!({"threadId":"t2"}), &turns_desc(json!([{"id":"u","status":"completed","items":[person("p"),question("q","Real?"),empty]}]))).unwrap();
        assert_eq!(waiting_item(&v, "t2").as_deref(), Some("q"));
    }
    #[test]
    fn questions_of_another_shape_are_kept_as_refused_never_cut() {
        let mut v = view();
        let mut q = question("q", "x");
        q["questions"] = json!([{"title":"ok"},{"title":7}]);
        live(&mut v, 1, "item/completed", "t", "u", q);
        let AskedQuestion::Waiting(entry) = state(&v, "t") else { panic!() };
        assert!(entry.get("questions").is_none());
        assert!(entry["refused"].as_str().unwrap().contains("pinned shape"));
        // A long title is kept whole.
        let long = "é".repeat(300_000);
        live(&mut v, 2, "item/completed", "t", "u", question("q2", &long));
        let AskedQuestion::Waiting(entry) = state(&v, "t") else { panic!() };
        assert_eq!(entry["questions"][0]["title"].as_str().unwrap(), long);
    }
    #[test]
    fn ordering_trap_a_history_read_of_older_messages_leaves_a_live_question_waiting() {
        let mut v = view();
        live(&mut v, 1, "item/completed", "t", "u3", question("q", "Live?"));
        // The newest page as Codex gave it before the question: the person's
        // messages in older turns, and the question's own turn without it.
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([
            {"id":"u3","status":"inProgress","items":[person("p3")]},
            {"id":"u2","status":"completed","items":[person("p2"),agent("a2")]}]))).unwrap();
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q"));
        // A page that does not hold the question's turn at all leaves it too.
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([{"id":"u1","status":"completed","items":[person("p1")]}]))).unwrap();
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q"));
    }
    #[test]
    fn a_history_read_where_the_persons_message_is_newer_than_the_question_clears_it() {
        let mut v = view();
        live(&mut v, 1, "item/completed", "t", "u1", question("q", "Live?"));
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([
            {"id":"u2","status":"completed","items":[person("p2"),agent("a2")]},
            {"id":"u1","status":"completed","items":[person("p1"),question("q","Live?"),agent("a1")]}]))).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::None);
        // Oldest first, as the last page, it reads the same.
        let mut v = view();
        live(&mut v, 1, "item/completed", "t", "u1", question("q", "Live?"));
        v.history("h", "thread/turns/list", &json!({"threadId":"t","sortDirection":"asc","cursor":"c"}), &json!({"data":[
            {"id":"u1","status":"completed","items":[person("p1"),question("q","Live?")]},
            {"id":"u2","status":"completed","items":[person("p2")]}],"nextCursor":null})).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::None);
        // A newer turn holding the person's message clears it even where the
        // page's copy of the question's turn lacks the question.
        let mut v = view();
        live(&mut v, 1, "item/completed", "t", "u1", question("q", "Live?"));
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([
            {"id":"u2","status":"completed","items":[person("p2")]},
            {"id":"u1","status":"completed","items":[person("p1")]}]))).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::None);
    }
    #[test]
    fn a_history_read_decides_an_unread_conversation_newest_first() {
        let mut v = view();
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([
            {"id":"u2","status":"completed","items":[person("p2"),question("q2","Newer?"),agent("a2")]},
            {"id":"u1","status":"completed","items":[person("p1"),question("q1","Older?")]}]))).unwrap();
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q2"));
        let mut v = view();
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([
            {"id":"u2","status":"completed","items":[person("p2"),agent("a2")]},
            {"id":"u1","status":"completed","items":[person("p1"),question("q1","Older?")]}]))).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::None);
        // An items list across the conversation, newest first.
        let mut v = view();
        v.history("h", "thread/items/list", &json!({"threadId":"t","sortDirection":"desc"}), &json!({"data":[
            {"turnId":"u2","item":question("q2","Newer?")},{"turnId":"u2","item":person("p2")},{"turnId":"u1","item":person("p1")}],"nextCursor":"more"})).unwrap();
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q2"));
    }
    #[test]
    fn a_page_that_does_not_decide_establishes_nothing() {
        // Not the newest page: a cursor newest first.
        let mut v = view();
        v.history("h", "thread/turns/list", &json!({"threadId":"t","cursor":"c"}), &turns_desc(json!([
            {"id":"u1","status":"completed","items":[person("p1"),question("q1","Old?")]}]))).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead);
        // Oldest first with a next cursor: not the newest end.
        v.history("h", "thread/turns/list", &json!({"threadId":"t","sortDirection":"asc"}), &json!({"data":[
            {"id":"u1","status":"completed","items":[question("q1","Old?")]}],"nextCursor":"more"})).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead);
        // The newest page with a next cursor that meets neither.
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &json!({"data":[
            {"id":"u9","status":"completed","items":[agent("a9")]}],"nextCursor":"more"})).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead);
        // One turn's items cannot say whether a later turn exists.
        v.history("h", "thread/items/list", &json!({"threadId":"t","turnId":"u1","sortDirection":"desc"}), &json!({"data":[question("q1","Old?")]})).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead);
        // A turn summary may leave items out: the reading stops at it.
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([
            {"id":"u2","status":"completed","itemsView":"summary","items":[agent("a2")]},
            {"id":"u1","status":"completed","items":[question("q1","Old?")]}]))).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead);
        // A metadata read without turns says nothing.
        v.history("h", "thread/read", &json!({"threadId":"t","includeTurns":false}), &json!({"thread":{"id":"t","turns":[]}})).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::NotRead);
        // The whole conversation meeting neither: none waiting.
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([{"id":"u9","status":"completed","items":[agent("a9")]}]))).unwrap();
        assert_eq!(state(&v, "t"), AskedQuestion::None);
        // A summary turn holding the question still decides, where it is newest.
        let mut v = view();
        v.history("h", "thread/turns/list", &json!({"threadId":"t"}), &turns_desc(json!([
            {"id":"u2","status":"completed","items":[person("p2"),question("q2","New?")]},
            {"id":"u1","status":"completed","itemsView":"summary","items":[]}]))).unwrap();
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q2"));
    }
    #[test]
    fn a_full_read_with_turns_decides_and_a_whole_empty_conversation_is_none() {
        let mut v = view();
        v.history("h", "thread/read", &json!({"threadId":"t","includeTurns":true}), &json!({"thread":{"id":"t","turns":[
            {"id":"u1","status":"completed","items":[person("p1"),question("q1","Asked?"),agent("a1")]}]}})).unwrap();
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q1"));
        v.history("h", "thread/read", &json!({"threadId":"e","includeTurns":true}), &json!({"thread":{"id":"e","turns":[]}})).unwrap();
        assert_eq!(state(&v, "e"), AskedQuestion::None);
    }
    #[test]
    fn a_conversation_started_here_is_read_from_its_start() {
        let mut v = view();
        v.asked_thread_started("t");
        assert_eq!(state(&v, "t"), AskedQuestion::None);
        live(&mut v, 1, "item/completed", "t", "u", person("p"));
        live(&mut v, 2, "item/completed", "t", "u", question("q", "Asked?"));
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q"));
        // Starting again changes nothing already established.
        v.asked_thread_started("t");
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q"));
    }
    #[test]
    fn a_continuation_reply_decides_only_from_the_turns_it_carries() {
        let mut v = view();
        v.asked_continuation_reply(&json!({"thread":{"id":"resumed","turns":[]}}));
        assert_eq!(state(&v, "resumed"), AskedQuestion::NotRead, "a resume without turns says nothing");
        v.asked_continuation_reply(&json!({"thread":{"id":"fork","turns":[
            {"id":"u1","status":"completed","items":[person("p1"),question("q1","Asked?")]}]}}));
        assert_eq!(waiting_item(&v, "fork").as_deref(), Some("q1"));
        v.asked_continuation_reply(&json!({"thread":{"id":"quiet","turns":[{"id":"u1","status":"completed","items":[agent("a1")]}]}}));
        assert_eq!(state(&v, "quiet"), AskedQuestion::NotRead, "a reply meeting neither is not taken as the whole conversation");
    }
    #[test]
    fn a_childs_question_is_kept_under_the_childs_own_thread() {
        let mut v = view();
        v.consume(&json!({"generation":g(1),"position":1,"frame":{"method":"item/completed","params":{"threadId":"parent","turnId":"u","item":
            {"id":"spawn","type":"collabAgentToolCall","status":"completed","senderThreadId":"parent","receiverThreadIds":["child"],"agentsStates":{}}}}})).unwrap();
        v.asked_thread_started("parent");
        live(&mut v, 2, "item/completed", "child", "cu", question("cq", "Child asks?"));
        assert_eq!(waiting_item(&v, "child").as_deref(), Some("cq"));
        assert_eq!(state(&v, "parent"), AskedQuestion::None);
        assert_eq!(v.snapshot()["askedQuestions"]["waiting"][0]["threadId"], "child");
    }
    #[test]
    fn a_closed_generation_keeps_what_was_last_read_and_takes_nothing_more() {
        let mut v = view();
        live(&mut v, 1, "item/completed", "t", "u", question("q", "Asked?"));
        v.close(&g(1)).unwrap();
        let snapshot = v.snapshot();
        assert_eq!(snapshot["observationEnded"], true);
        assert_eq!(waiting_item(&v, "t").as_deref(), Some("q"));
        assert!(v.consume(&json!({"generation":g(1),"position":2,"frame":{"method":"item/completed","params":{"threadId":"t","turnId":"u2","item":person("p")}}})).is_err());
        v.asked_thread_started("other");
        v.asked_continuation_reply(&json!({"thread":{"id":"t","turns":[{"id":"u2","status":"completed","items":[person("p")]}]}}));
        assert_eq!(v.snapshot()["askedQuestions"], snapshot["askedQuestions"]);
        // The next generation's view starts with nothing read.
        let mut next = NativeView::new("h".into()).unwrap();
        next.ready(g(2), Value::Null, Value::Null).unwrap();
        assert_eq!(asked_question(&next.snapshot(), "t"), AskedQuestion::NotRead);
    }
    #[test]
    fn the_accessor_reads_a_snapshot_and_nothing_else() {
        assert_eq!(asked_question(&Value::Null, "t"), AskedQuestion::NotRead);
        let snapshot = json!({"askedQuestions":{"read":["a","b"],"waiting":[{"threadId":"b","turnId":"u","itemId":"q","questions":[{"title":"x","options":null}]}]}});
        assert_eq!(asked_question(&snapshot, "a"), AskedQuestion::None);
        assert!(matches!(asked_question(&snapshot, "b"), AskedQuestion::Waiting(e) if e["itemId"] == "q"));
        assert_eq!(asked_question(&snapshot, "c"), AskedQuestion::NotRead);
    }
    #[test]
    fn waiting_entries_are_sorted_by_conversation() {
        let mut v = view();
        live(&mut v, 1, "item/completed", "z", "u", question("qz", "Z?"));
        live(&mut v, 2, "item/completed", "a", "u", question("qa", "A?"));
        let asked = v.snapshot()["askedQuestions"].clone();
        assert_eq!(asked["read"], json!(["a","z"]));
        assert_eq!(asked["waiting"].as_array().unwrap().iter().map(|e| e["threadId"].clone()).collect::<Vec<_>>(), vec![json!("a"), json!("z")]);
    }
}
