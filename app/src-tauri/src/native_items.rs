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
fn identity(content: &Value) -> Value {
    // NPTD U-08 is explicitly TEST VALUE, not authoritative content identity.
    let bytes = serde_json::to_vec(content).expect("JSON Value serialization");
    json!({"method":"sha256/canonical-json/npt-v0 (TEST VALUE; HOSTING U-08)","value":sha256_hex(&bytes)})
}

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
    /// Order in which this view first received each item; a receipt reading,
    /// not a native sequence or a claim about when Codex produced the item.
    next_order: u64,
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
            types_pin: "0.160.0".into(),
            version: Value::Null,
            supplier_standing: Value::Null,
            distribution_evidence: Value::Null,
            items: BTreeMap::new(),
            turns: BTreeMap::new(),
            revisions: Vec::new(),
            descendants: BTreeMap::new(),
            goals: BTreeMap::new(),
            checklist_gaps: Vec::new(),
            next_order: 0,
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
        // Unknown native frames also advance the all-frame cursor. They stay
        // inspectable in hosting's unmodified ordered journal.
        match frame["method"].as_str() {
            Some("item/started" | "item/completed") => {
                self.item(
                    text(p, "threadId")?,
                    text(p, "turnId")?,
                    &p["item"],
                    frame["method"] == "item/completed",
                    false,
                    Some(frame.clone()),
                )?;
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
                    let preview = row["preview"].as_str().unwrap_or("").to_string()
                        + p["delta"].as_str().ok_or("invalid plan delta")?;
                    row["preview"] = json!(preview);
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
                let key = native_key(thread, turn, id);
                let order = self.next_order;
                let row=self.items.entry(key).or_insert_with(||json!({"threadId":thread,"turnId":turn,"native":{"id":id,"type":kind},"displayState":"in-progress","standing":"live-observed","observationEnded":false,"observedOrder":order}));
                if row["observedOrder"] == order {
                    self.next_order += 1;
                }
                if row["displayState"] == "in-progress" {
                    if kind == "reasoning" {
                        let index = p["summaryIndex"].as_u64().ok_or("invalid summary index")? as usize;
                        if index > 4096 {
                            return Err("summary index out of range".into());
                        }
                        let mut parts = row["summaryPreview"].as_array().cloned().unwrap_or_default();
                        while parts.len() <= index {
                            parts.push(json!(""));
                        }
                        parts[index] = json!(parts[index].as_str().unwrap_or("").to_string() + delta);
                        row["summaryPreview"] = json!(parts);
                    } else {
                        row["preview"] = json!(row["preview"].as_str().unwrap_or("").to_string() + delta);
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
                self.turn(text(p, "threadId")?, &p["turn"])?;
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
            if let Some(id) = native["agentThreadId"].as_str() {
                self.descendants.entry(id.into()).or_insert_with(||json!({"threadId":id,"parentThreadId":thread,"parentSource":"subAgentActivity containing thread (inference)","lastNativeActivity":native,"guidance":"not-known","observationEnded":false}));
            }
        }
        self.items.insert(key, row);
        Ok(())
    }
    fn turn(&mut self, thread: &str, native: &Value) -> Result<(), String> {
        let turn = text(native, "id")?;
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
            }
            "thread/turns/list" => {
                for turn in result["data"].as_array().ok_or("turn history absent")? {
                    for item in turn["items"].as_array().into_iter().flatten() {
                        self.item(thread, text(turn, "id")?, item, item["status"] != "inProgress", true, None)?;
                    }
                    self.turn(thread, turn)?;
                }
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
                        self.turn(thread, turn)?;
                    }
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
        json!({"home":self.home,"generation":self.generation,"position":self.position,"supplierStanding":self.supplier_standing,"distributionEvidence":self.distribution_evidence,
            "items":self.items.values().collect::<Vec<_>>(),"revisions":self.revisions,"descendants":self.descendants.values().collect::<Vec<_>>(),
            "turns":self.turns.values().collect::<Vec<_>>(),
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
            json!("codex 0.160.0"),
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
