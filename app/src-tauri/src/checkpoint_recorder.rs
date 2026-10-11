//! The current-phase checkpoint recorder (DEL-02-03 EXEC §2.4 RC-1…RC-10,
//! §2.5 AW-3, AW-6, AW-7, AE-2, AE-3, AE-5; §2.6 A-2, A-5…A-9, A-11, A-12).
//! The EXEC Design text and its entry-body schema are DRAFT/PROPOSED.
//!
//! What it records, in the run's own RS log, through the App writer:
//! - CE-1 `checkpoint_listed` for each recognized declared checkpoint at run
//!   start, with whether this App evaluates its arrival, and CE-2
//!   `declaration_finding` for each invalid or not-established one (§4.14);
//! - CE-3 `checkpoint_arrival` (with its CE-18 `disposition_change`
//!   *waiting*) only from native items this App observed live: a completed
//!   `agentMessage` whose first non-empty line, trimmed, equals a message
//!   output's designating line exactly (AW-6, WD OP-1…OP-4); a completed
//!   `fileChange` whose changes produce a file output's declared path (AW-7);
//!   or the start of an agent item of a harness capability's own item kind
//!   for a kind (a) checkpoint on that capability (AW-3);
//! - CE-4 `act_request` for a supplier person-input request or an MCP
//!   elicitation received in the run while an arrival waits (RC-5);
//! - CE-5 `act_counted`, CE-6 `act_not_counted` and CE-8 `arrival_declined`
//!   from the human-act and act-declined records in the project's record set
//!   (RS §6, written by the App act control), with their CE-18 labels
//!   (SP-1…SP-8, SP-6 earlier acts included; [`count_acts`]);
//! - CE-12 `continued_past` once per waiting arrival, for the first agent run
//!   action (RC-9) the App received after the arrival, and CE-11
//!   `run_resumed` for the first run action started after the act that made
//!   an arrival *performed*;
//! - the waiting arrivals listed by CE-17 `run_ended` (`waiting`).
//!
//! Recording is not a reaction (RC-4): nothing here sends, asks, opens,
//! pauses or refuses anything; the outputs are entries for the run record and
//! nothing else. CE-7 never arises in an App run: A5 is valid only at a host
//! outcome (FB-16), which this App does not evaluate (AW-8…AW-10).
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::path::Path;

/// The App's exact-byte content method (RS §6.2a, CC-CONTENT-RX).
const EXACT_BYTES: &str = "chirality.app.exact-bytes.sha256/v1";
const ACT_COUNTING: &str = "Acts are counted from the human-act and act-declined records in this project's record set (the App act control's captures): an act of the required kind bound to this referent's content counts, an earlier one included (SP-6). Acts on host content and A12 control relations are not observed by this App.";
const MESSAGE_ACT_LIMIT: &str = "No App act control binds an act to an agent message (CAP-1 binds App files by content identity), so no act can be counted for this arrival.";
const MESSAGE_LIMIT: &str = "The designating line marks where the agent put the output; it does not show that the content is what the declaration describes (AW-6).";
const FILE_LIMIT: &str = "Only an add, an in-place update or a move onto the declared path counts; a delete or a move away does not (this App's reading of AW-7). The path is compared with the declared project-relative path as text, after removing the project root from an absolute path; how Codex reports file paths is not observed (O-8, U-E26).";
const FILE_READ_LIMIT: &str = "The file's content identity was read by the App when it observed the completed change; a later change made before that read is not distinguished (AW-7).";
const CALL_LIMIT: &str = "arrival observed at call start; dispatch order not established";
/// RC-9 run actions at the definition pin; agent messages, reasoning and plans are conversation.
const RUN_ACTIONS: [&str; 7] = ["mcpToolCall", "dynamicToolCall", "commandExecution", "fileChange", "collabAgentToolCall", "webSearch", "imageGeneration"];
/// The act kinds an RS act reference may carry (EXEC `actRef`).
const ACT_KINDS: [&str; 10] = ["A4", "A5", "A6", "A7", "A10", "A11", "A12", "A13", "A15", "A16"];

fn subject_class(token: &str) -> Option<&'static str> {
    Some(match token {
        "change_items_of_named_proposal" => "change items of a named proposal",
        "named_output" => "named output",
        "objects_named_output_concerns" => "objects a named output concerns",
        "objects_changed_by_named_outcome" => "objects changed by a named outcome",
        "targets_of_held_call" => "targets of the held call",
        "grant_setting" => "grant setting",
        _ => return None,
    })
}
fn decision_path(token: &str) -> Option<&'static str> {
    Some(match token {
        "stop" => "stop",
        "return_to_stage" => "return to stage",
        "proceed_on_branch" => "proceed on branch",
        _ => return None,
    })
}
/// AW-3: a harness capability name whose presence rule is active (EV-3,
/// EV-3a), with its own item kind (WD-v0.8 §4.2.5 basis column). The names
/// with an inactive rule (`person-input-request`, `image-view`,
/// `plan-update`) have none and are not evaluable (U-E10).
fn capability_item_kind(name: &str) -> Option<&'static str> {
    Some(match name {
        "shell-command" => "commandExecution",
        "file-change" => "fileChange",
        "web-search" => "webSearch",
        "agent-delegation" => "collabAgentToolCall",
        "mcp-tool-call" => "mcpToolCall",
        "dynamic-tool-call" => "dynamicToolCall",
        "image-generation" => "imageGeneration",
        _ => return None,
    })
}
#[derive(Clone, Debug)]
enum Trigger {
    /// AW-6: the output's designating line.
    Message { output: String, line: String },
    /// AW-7: the output's project-relative path.
    File { output: String, path: String },
    /// AW-3: the start of an agent item of this kind.
    Capability { tool: String, kind: &'static str },
    /// Not evaluated by this App: no arrival is ever recorded for it.
    None,
}

#[derive(Clone, Debug)]
struct Listed {
    name: String,
    act: String,
    subject: &'static str,
    subject_output: Option<String>,
    governed: bool,
    purpose: String,
    scope: String,
    trigger: Trigger,
}

#[derive(Clone, Debug)]
struct Arrival {
    checkpoint: String,
    ordinal: u64,
    act: String,
    /// Receipt order of the observation that met it: (spawn counter, position).
    at: (u64, u64),
    continued: bool,
    resumed: bool,
}
impl Arrival {
    fn reference(&self) -> Value {
        json!({"checkpoint":self.checkpoint,"arrivalOrdinal":self.ordinal})
    }
}

/// One run's recorder. Its working state is disposable (RC-10): dispositions
/// and counted acts are read from the run's entries.
#[derive(Clone, Debug, Default)]
pub(crate) struct CheckpointRecorder {
    listed: Vec<Listed>,
    arrivals: Vec<Arrival>,
    seen_completions: BTreeSet<String>,
    seen_starts: BTreeSet<String>,
    seen_requests: BTreeSet<String>,
    limit: Option<String>,
    /// The last reason the project's act records could not be read, if any.
    acts_limit: Option<String>,
}

/// One recorder output: the RS entry kind and its CE body.
pub(crate) type Output = (&'static str, Value);
/// The project's human-act and act-declined records, read only when needed.
pub(crate) type ActSource<'a> = &'a mut dyn FnMut() -> Result<Vec<Value>, String>;

/// Where the run is, as the recorder needs it.
pub(crate) struct RunScope<'a> {
    pub home: &'a str,
    pub conversation: &'a str,
    pub start: crate::run_offers::RunStart,
    pub project_root: &'a std::path::Path,
}

impl CheckpointRecorder {
    /// A-2 / CE-1, CE-2: the checkpoints of the resolved declaration (RP-5).
    /// Recognized checkpoints are listed; an invalid or not-established one
    /// is written as a declaration finding and creates no arrival (§4.14).
    pub(crate) fn start(declaration: Result<crate::workflow_declaration::Declaration, String>) -> (Self, Vec<Output>) {
        use crate::workflow_declaration::Reading;
        let declaration = match declaration {
            Ok(d) => d,
            Err(error) => {
                let limit = format!("declaration not resolvable — reconstruction not verified ({error}); no arrival is evaluated in this run");
                return (Self { limit: Some(limit), ..Self::default() }, vec![]);
            }
        };
        let outputs: Vec<&Value> = declaration.elements.get("returned_outputs").into_iter().flatten()
            .filter(|e| e.reading == Reading::Recognized).map(|e| &e.value).collect();
        let output = |name: &str| outputs.iter().find(|o| o["name"] == name).copied();
        let tools: Vec<&Value> = declaration.elements.get("required_tools").into_iter().flatten()
            .filter(|e| e.reading == Reading::Recognized).map(|e| &e.value).collect();
        let tool = |name: &str| tools.iter().find(|t| t["name"] == name).copied();
        let mut recorder = Self::default();
        let mut written = Vec::new();
        for (position, element) in declaration.elements.get("checkpoints").into_iter().flatten().enumerate() {
            let v = &element.value;
            if matches!(element.reading, Reading::Invalid | Reading::NotEstablished) {
                written.extend(declaration_findings(v, position, &element.reading, &element.findings));
                continue;
            }
            if element.reading != Reading::Recognized {
                continue;
            }
            let (Some(name), Some(act), Some(subject)) = (v["name"].as_str(), v["required_act"].as_str(), v["subject"]["class"].as_str().and_then(subject_class)) else { continue };
            let rw = &v["reached_when"];
            let kind = rw["kind"].as_str().unwrap_or_default();
            let (trigger, status, reason) = match kind {
                "output_produced" => match rw["output"].as_str().and_then(|n| output(n).map(|o| (n, o))) {
                    Some((n, o)) if o["form"] == "message" && o["designating_line"].is_string() => (
                        Trigger::Message { output: n.into(), line: o["designating_line"].as_str().unwrap().into() },
                        "evaluable with limit",
                        format!("AW-6: a completed agent message whose first non-empty line is exactly \"{}\". {MESSAGE_LIMIT} {MESSAGE_ACT_LIMIT}", o["designating_line"].as_str().unwrap()),
                    ),
                    Some((n, o)) if o["form"] == "file" && o["path"].is_string() => (
                        Trigger::File { output: n.into(), path: o["path"].as_str().unwrap().into() },
                        "evaluable with limit",
                        format!("AW-7: a completed file change on {}. {FILE_LIMIT}", o["path"].as_str().unwrap()),
                    ),
                    Some((_, o)) if o["form"] == "host_change" => (Trigger::None, "not evaluable", "AW-5: the output is a host change; host outcomes need a host-supplied mapping this App does not have (AW-8, AW-9; ADAPTER NM-2). No arrival will be recorded.".into()),
                    Some((_, o)) => (Trigger::None, "not evaluable", format!("the output's form ({}) has no observation this App records an arrival from; only a message with a designating line (AW-6) or a file with a path (AW-7) has one. No arrival will be recorded.", o["form"].as_str().unwrap_or("not stated"))),
                    None => (Trigger::None, "not evaluable", "the produced output is not a usable declared output. No arrival will be recorded.".into()),
                },
                "before_dispatch" => match rw["tool"].as_str().and_then(|n| tool(n).map(|t| (n, t))) {
                    Some((n, t)) if t["class"] == "harness_capability" => match t["capability"].as_str().and_then(|c| capability_item_kind(c).map(|k| (c, k))) {
                        Some((capability, item)) => (
                            Trigger::Capability { tool: n.into(), kind: item },
                            "evaluable with limit",
                            format!("AW-3: the start of each agent item of kind {item} ({capability}), with the limit \"{CALL_LIMIT}\". The call's targets are not identified, so no act can be counted for such an arrival."),
                        ),
                        None => (Trigger::None, "not evaluable", format!("AW-3: the capability {} has no active presence rule, so its call cannot be observed (U-E10). No arrival will be recorded.", t["capability"].as_str().unwrap_or("not stated"))),
                    },
                    Some(_) => (Trigger::None, "not evaluable", "AW-1/AW-2: a host operation's call is recognized only through a host-supplied native-tool mapping or command form (ADAPTER NM-1, OM-1), which no host has supplied (AW-4, NM-2). No arrival will be recorded.".into()),
                    None => (Trigger::None, "not evaluable", "the dispatched tool is not a usable declared tool. No arrival will be recorded.".into()),
                },
                "host_outcome" => (Trigger::None, "not evaluable", "Host outcomes (AW-8…AW-10) need a host-supplied mapping or host reads this App does not have. No arrival will be recorded.".into()),
                _ => continue,
            };
            let listed = Listed {
                name: name.into(),
                act: act.into(),
                subject,
                subject_output: v["subject"]["output"].as_str().map(str::to_owned),
                governed: v["governed"] == "yes",
                purpose: v["purpose"].as_str().unwrap_or_default().into(),
                scope: v["scope"].as_str().unwrap_or_default().into(),
                trigger,
            };
            let mut body = json!({"checkpoint":listed.name,"requiredAct":listed.act,"reachedWhenKind":kind,"subjectClass":listed.subject,
                "governed":listed.governed,"purpose":listed.purpose,"scope":listed.scope,"evaluability":{"status":status,"reason":reason}});
            if v["fresh_act_required"] == "yes" {
                body["freshActRequired"] = json!(true);
            }
            if let Some(path) = v["on_subject_absent"]["path"].as_str().and_then(decision_path) {
                body["onSubjectAbsent"] = json!(path);
            }
            written.push(("checkpoint_listed", body));
            recorder.listed.push(listed);
        }
        (recorder, written)
    }

    pub(crate) fn view(&self) -> Value {
        json!({"listed":self.listed.iter().map(|l|json!({"checkpoint":l.name,"evaluated":!matches!(l.trigger,Trigger::None)})).collect::<Vec<_>>(),
            "arrivals":self.arrivals.len(),"limit":self.limit,"actsLimit":self.acts_limit,
            "standing":"Recorded only from native items this App observed live and from the human-act records in this project; recording sends, asks or pauses nothing (RC-4)."})
    }

    /// Reads the run's native rows and server requests once each, in receipt
    /// order, and the project's act records, and returns the entries to write
    /// (CE-3…CE-6, CE-8, CE-11, CE-12, CE-18). `entries` is the run's record
    /// so far, which decides each arrival's disposition.
    pub(crate) fn observe(&mut self, view: &Value, scope: &RunScope, entries: &[Value], acts: ActSource) -> Vec<Output> {
        if view["home"] != scope.home || self.listed.is_empty() {
            return vec![];
        }
        let session = view["generation"]["appSession"].clone();
        enum Event<'a> {
            Completed(&'a Value),
            Started(&'a Value),
            Request(&'a Value),
        }
        let in_run = |turn: &str| crate::run_offers::turn_order(view, scope.conversation, turn).is_some_and(|order| scope.start.includes(order));
        let mut events: Vec<((u64, u64), String, Event)> = Vec::new();
        for row in view["items"].as_array().into_iter().flatten() {
            if row["threadId"] != scope.conversation || row["standing"] != "live-observed" || row["receipt"]["generation"]["appSession"] != session {
                continue;
            }
            let (Some(turn), Some(item), Some(spawn)) = (row["turnId"].as_str(), row["native"]["id"].as_str(), row["receipt"]["generation"]["spawnCounter"].as_u64()) else { continue };
            if !in_run(turn) {
                continue;
            }
            let key = format!("{}\u{0}{turn}\u{0}{item}", scope.conversation);
            if let Some(position) = row["receipt"]["completed"].as_u64() {
                if !self.seen_completions.contains(&key) {
                    events.push(((spawn, position), key.clone(), Event::Completed(row)));
                }
            }
            if let Some(position) = row["receipt"]["started"].as_u64() {
                if !self.seen_starts.contains(&key) {
                    events.push(((spawn, position), key, Event::Started(row)));
                }
            }
        }
        for request in view["serverRequests"].as_array().into_iter().flatten() {
            if !matches!(request["method"].as_str(), Some("item/tool/requestUserInput" | "mcpServer/elicitation/request"))
                || request["generation"]["appSession"] != session
                || request["nativeParameters"]["threadId"] != scope.conversation
            {
                continue;
            }
            let (Some(turn), Some(spawn), Some(position)) = (request["nativeParameters"]["turnId"].as_str(), request["generation"]["spawnCounter"].as_u64(), request["receiptPosition"].as_u64()) else { continue };
            let key = format!("{spawn}\u{0}{}", request["requestIdentity"]);
            if in_run(turn) && !self.seen_requests.contains(&key) {
                events.push(((spawn, position), key, Event::Request(request)));
            }
        }
        events.sort_by(|a, b| a.0.cmp(&b.0));
        let mut written: Vec<Output> = Vec::new();
        // The act records, read at most once per observation and only while an arrival waits.
        let mut records: Option<Vec<Value>> = None;
        self.count(entries, &mut written, scope.project_root, &mut *acts, &mut records);
        for (at, key, event) in events {
            match event {
                Event::Completed(row) => {
                    self.seen_completions.insert(key);
                    let found = self.matches(row, scope);
                    if found.is_empty() {
                        continue;
                    }
                    let completed = row["sourceFrame"]["params"]["completedAtMs"].as_i64();
                    let time = match completed {
                        Some(ms) => json!({"value":crate::util::rfc3339_from_ms(ms),"source":"supplier_item_time"}),
                        None => json!({"value":crate::util::now_rfc3339(),"source":"app_observation_time"}),
                    };
                    for (index, referents, limits) in found {
                        written.extend(self.arrive(index, row, scope, at, &time, referents, limits));
                    }
                    self.count(entries, &mut written, scope.project_root, &mut *acts, &mut records);
                }
                Event::Started(row) => {
                    self.seen_starts.insert(key);
                    if !run_action(row) {
                        continue;
                    }
                    let reference = item_ref(row, scope.conversation);
                    // The start time is still in hand only while the start frame is the row's latest.
                    let supplier_time = row["sourceFrame"]["params"]["startedAtMs"].as_i64().filter(|_| row["sourceFrame"]["method"] == "item/started")
                        .map(crate::util::rfc3339_from_ms);
                    for arrival in self.arrivals.iter_mut().filter(|a| a.at < at) {
                        match disposition(entries, &written, &arrival.reference()).as_deref() {
                            Some("waiting") if !arrival.continued => {
                                arrival.continued = true;
                                written.push(("continued_past", json!({"arrival":arrival.reference(),"actionRef":reference,"actKind":arrival.act})));
                            }
                            Some("performed") if !arrival.resumed => {
                                // A-9: the resume point is claimed only where the action's start is
                                // evidenced at or after the performance; with no supplier start time
                                // the order is not established and no resume point is claimed.
                                let performed = performed_at(entries, &written, &arrival.reference());
                                match (&supplier_time, performed) {
                                    (Some(time), Some(performed)) if comparable(time) && comparable(&performed) => {
                                        if *time >= performed {
                                            arrival.resumed = true;
                                            written.push(("run_resumed", json!({"arrival":arrival.reference(),"firstActionRef":reference,"time":time})));
                                        }
                                    }
                                    _ => arrival.resumed = true,
                                }
                            }
                            _ => {}
                        }
                    }
                    // AW-3: each start of an item of a capability's own kind is an arrival (RW-4).
                    let time = match &supplier_time {
                        Some(value) => json!({"value":value,"source":"supplier_item_time"}),
                        None => json!({"value":crate::util::now_rfc3339(),"source":"app_observation_time"}),
                    };
                    let starts: Vec<(usize, String)> = self.listed.iter().enumerate().filter_map(|(i, l)| match &l.trigger {
                        Trigger::Capability { tool, kind } if row["startNative"]["type"] == *kind => Some((i, tool.clone())),
                        _ => None,
                    }).collect();
                    for (index, tool) in &starts {
                        let reason = format!("the targets of the {tool} call are not identified: the App binds no call arguments (never argument text, WD §4.3.6)");
                        let referents = vec![json!({"subject":format!("{} (call {})", self.listed[*index].subject, reference),"content":{"notObtainable":true,"reason":reason}})];
                        written.extend(self.arrive(*index, row, scope, at, &time, referents, vec![CALL_LIMIT]));
                    }
                    if !starts.is_empty() {
                        self.count(entries, &mut written, scope.project_root, &mut *acts, &mut records);
                    }
                }
                Event::Request(request) => {
                    self.seen_requests.insert(key);
                    let current: Vec<Value> = self.arrivals.iter().filter(|a| a.at < at).map(Arrival::reference)
                        .filter(|r| disposition(entries, &written, r).as_deref() == Some("waiting")).collect();
                    if let Some(body) = request_body(request, &current) {
                        written.push(("act_request", body));
                    }
                }
            }
        }
        written
    }

    /// CE-3 with its CE-18 *waiting* label: one arrival of a listed checkpoint.
    #[allow(clippy::too_many_arguments)]
    fn arrive(&mut self, index: usize, row: &Value, scope: &RunScope, at: (u64, u64), time: &Value, referents: Vec<Value>, limits: Vec<&str>) -> Vec<Output> {
        let listed = self.listed[index].clone();
        let ordinal = 1 + self.arrivals.iter().filter(|a| a.checkpoint == listed.name).count() as u64;
        let arrival = Arrival { checkpoint: listed.name.clone(), ordinal, act: listed.act.clone(), at, continued: false, resumed: false };
        let mut limits: Vec<&str> = limits;
        limits.push(ACT_COUNTING);
        let outputs = vec![
            ("checkpoint_arrival", json!({"checkpoint":listed.name,"requiredAct":listed.act,"subjectClass":listed.subject,
                "governed":listed.governed,"arrivalOrdinal":ordinal,
                "event":{"source":"native_item","ref":item_ref(row, scope.conversation),"evidencedTime":time},
                "referents":referents,"purpose":listed.purpose,"scope":listed.scope,
                "limits":limits,"requestObservation":{"state":"not yet observed"}})),
            ("disposition_change", json!({"arrival":arrival.reference(),"disposition":"waiting","annotations":[]})),
        ];
        self.arrivals.push(arrival);
        outputs
    }

    /// CE-5, CE-6, CE-8 for the arrivals still waiting, from the project's
    /// act records (read once, lazily). A read that fails counts nothing and
    /// is retried at the next observation; nothing is inferred (RC-2).
    fn count(&mut self, entries: &[Value], written: &mut Vec<Output>, root: &Path, acts: &mut dyn FnMut() -> Result<Vec<Value>, String>, records: &mut Option<Vec<Value>>) {
        let all: Vec<Value> = entries.iter().cloned().chain(written.iter().map(|(k, b)| json!({"kind":k,"body":b}))).collect();
        if waiting_arrivals(&all).is_empty() {
            return;
        }
        if records.is_none() {
            match acts() {
                Ok(read) => {
                    self.acts_limit = None;
                    *records = Some(read);
                }
                Err(e) => {
                    self.acts_limit = Some(format!("act records not read; no act counted at this observation: {e}"));
                    return;
                }
            }
        }
        written.extend(count_acts(&all, records.as_deref().unwrap_or_default(), root));
    }

    /// Which listed checkpoints a completed row meets, each with its bound
    /// referents and its arrival limits. Anything else meets none.
    fn matches(&self, row: &Value, scope: &RunScope) -> Vec<(usize, Vec<Value>, Vec<&'static str>)> {
        let native = &row["native"];
        let mut found = Vec::new();
        for (index, listed) in self.listed.iter().enumerate() {
            match &listed.trigger {
                Trigger::Message { output, line } if native["type"] == "agentMessage" && row["displayState"] == "completed" => {
                    let Some(text) = native["text"].as_str() else { continue };
                    if first_line(text) != Some(line.as_str()) {
                        continue;
                    }
                    let content = json!({"method":EXACT_BYTES,"value":crate::util::sha256_hex(text.as_bytes()),"scope":"the completed agentMessage text as received from Codex"});
                    found.push((index, referents(listed, output, &format!("agentMessage {}", native["id"].as_str().unwrap_or_default()), content), vec![MESSAGE_LIMIT, MESSAGE_ACT_LIMIT]));
                }
                Trigger::File { output, path } if native["type"] == "fileChange" && native["status"] == "completed" => {
                    let paths: Vec<&str> = native["changes"].as_array().into_iter().flatten().filter_map(produced_path).collect();
                    if !paths.iter().any(|p| same_path(p, path, scope.project_root)) {
                        continue;
                    }
                    found.push((index, referents(listed, output, &format!("file {path}"), file_content(scope.project_root, path)), vec![FILE_LIMIT, FILE_READ_LIMIT]));
                }
                _ => {}
            }
        }
        found
    }
}

/// CE-2: one finding per distinct WD code of an invalid or not-established
/// checkpoint (EXEC §4.14). A schema failure without a code is FB-04.
fn declaration_findings(v: &Value, position: usize, reading: &crate::workflow_declaration::Reading, findings: &[String]) -> Vec<Output> {
    use crate::workflow_declaration::Reading;
    let name = v["name"].as_str().filter(|n| !n.trim().is_empty()).map(str::to_owned).unwrap_or_else(|| format!("unnamed checkpoint (position {})", position + 1));
    let finding = if *reading == Reading::Invalid { "invalid" } else { "not established" };
    let mut codes: Vec<String> = Vec::new();
    for f in findings {
        let code: String = f.strip_prefix("FB-").map(|rest| format!("FB-{}", rest.chars().take_while(char::is_ascii_digit).collect::<String>())).unwrap_or_default();
        if code.len() > 3 && !codes.contains(&code) {
            codes.push(code);
        }
    }
    if codes.is_empty() {
        codes.push("FB-04".into());
    }
    codes.into_iter().map(|code| ("declaration_finding", json!({"checkpoint":name,"finding":finding,"code":code}))).collect()
}

/// CE-4 (RC-5): a supplier person-input request or an MCP elicitation,
/// received while at least one arrival waits. A person-input request carries
/// questions, never a structured act kind, subject or purpose, so those are
/// "not named by the request"; nothing is taken from the arrival.
fn request_body(request: &Value, current: &[Value]) -> Option<Value> {
    if current.is_empty() {
        return None;
    }
    let (requester, form) = match request["method"].as_str()? {
        "item/tool/requestUserInput" => ("agent", "supplier person-input request"),
        _ => ("not established (MCP server or agent)", "MCP elicitation"),
    };
    let identity = match &request["requestIdentity"] {
        Value::String(s) => s.clone(),
        other => other.to_string(),
    };
    let mut body = json!({"requester":{"kind":requester},"form":form,"actKind":"not named by the request","subject":"not named by the request",
        "purpose":"not named by the request","association":"arrival association not established",
        "evidence":{"kind":"conversation item","ref":format!("server-request:{}/{}", request["generation"]["spawnCounter"], identity),"resolutionAtWrite":"resolved"},
        "time":crate::util::now_rfc3339()});
    if let [only] = current {
        body["association"] = json!("associated with the current arrival");
        body["arrival"] = only.clone();
    }
    Some(body)
}

/// AW-7's bound content: the exact bytes of the declared file in the project,
/// read now; not obtainable when the file cannot be read inside the project.
fn file_content(root: &Path, declared: &str) -> Value {
    let read = (|| -> Result<Vec<u8>, String> {
        let root = std::fs::canonicalize(root).map_err(|e| format!("project root not readable: {e}"))?;
        let file = std::fs::canonicalize(root.join(declared)).map_err(|e| format!("file not readable: {e}"))?;
        if !file.starts_with(&root) {
            return Err("the declared path resolves outside the project".into());
        }
        std::fs::read(&file).map_err(|e| format!("file not readable: {e}"))
    })();
    match read {
        Ok(bytes) => json!({"method":EXACT_BYTES,"value":crate::util::sha256_hex(&bytes),"scope":"the file's bytes as the App read them after observing the completed change"}),
        Err(reason) => json!({"notObtainable":true,"reason":format!("{reason}; no act can be counted for this referent (SP-4)")}),
    }
}

/// RFC 3339 UTC text with milliseconds, as the App and `rfc3339_from_ms`
/// write it, so that two such times order as text.
fn comparable(time: &str) -> bool {
    let b = time.as_bytes();
    b.len() == 24 && b[4] == b'-' && b[10] == b'T' && b[19] == b'.' && b[23] == b'Z'
}

/// CE-5, CE-6, CE-8 (EXEC §2.4.3, §4.5 SP-1…SP-8, RC-7) over a run's
/// entries (`kind`, `body`) and the project's act records (RS entries).
/// Rebuildable (RC-10): an act already cited for an arrival is not read
/// again, and only arrivals whose latest label is *waiting* are evaluated.
///
/// An act is on an arrival's subject when the arrival's one referent is the
/// declared file of a named output (AW-7) and the act's bound subject names
/// that file in the project. Then, in capture order, until the arrival is
/// decided (§4.6: the first decides):
/// - an act-declined event of the required kind captured at or after the
///   arrival event resolves it negatively (CE-8);
/// - an act of another kind is not counted, "another act kind" (CE-6);
/// - an act of the required kind whose bound content equals the referent's
///   content counts (CE-5), "earlier act" when captured before the arrival
///   event (SP-6), and the arrival is *performed*;
/// - otherwise it is not counted: "content no longer current" when captured
///   before the arrival, "act on other content" after it (CE-6).
///
/// A referent whose content is not obtainable binds no act (A-5, SP-4). An
/// act record without resolved capture evidence, a decision actor and direct
/// capture is not an act for counting (SP-2, SP-3; PH-4).
pub(crate) fn count_acts(entries: &[Value], records: &[Value], root: &Path) -> Vec<Output> {
    let root = std::fs::canonicalize(root).unwrap_or_else(|_| root.to_path_buf());
    let mut out: Vec<Output> = Vec::new();
    for arrival_entry in entries.iter().filter(|e| e["kind"] == "checkpoint_arrival") {
        let body = &arrival_entry["body"];
        let arrival = json!({"checkpoint":body["checkpoint"],"arrivalOrdinal":body["arrivalOrdinal"]});
        let referents = body["referents"].as_array().map(Vec::as_slice).unwrap_or_default();
        let ([referent], Some(required), Some(arrived)) = (referents, body["requiredAct"].as_str(), body["event"]["evidencedTime"]["value"].as_str()) else { continue };
        let (Some(subject), Some(method), Some(value)) = (referent["subject"].as_str(), referent["content"]["method"].as_str(), referent["content"]["value"].as_str()) else { continue };
        if !subject.starts_with("output ") || !comparable(arrived) {
            continue;
        }
        let on_subject = |named: &Value| -> Option<usize> {
            named.as_array()?.iter().position(|s| {
                s.as_str().and_then(|p| Path::new(p).strip_prefix(&root).ok()).and_then(Path::to_str)
                    .is_some_and(|rel| !rel.is_empty() && subject.ends_with(&format!(": file {rel}")))
            })
        };
        let mut candidates: Vec<(&str, &str, &Value, usize)> = records.iter().filter_map(|r| {
            let id = r["recordId"].as_str()?;
            let b = &r["body"];
            let evidenced = b["captureEvidence"].as_array()?.iter().any(|e| e["kind"] == "capture evidence" && e["resolutionAtWrite"] == "resolved");
            match r["kind"].as_str()? {
                "human_act" if evidenced && b["recordingMode"] == "direct capture" && b["decisionActor"].is_object() => {
                    let time = b["captureTime"].as_str().filter(|t| comparable(t))?;
                    Some((time, id, r, on_subject(&b["boundSubject"])?))
                }
                "act_declined" if evidenced => {
                    let time = b["time"].as_str().filter(|t| comparable(t))?;
                    Some((time, id, r, on_subject(&b["subject"])?))
                }
                _ => None,
            }
        }).collect();
        candidates.sort_by(|a, b| (a.0, a.1).cmp(&(b.0, b.1)));
        for (time, id, record, index) in candidates {
            let pending: Vec<Value> = out.iter().map(|(k, b)| json!({"kind":k,"body":b})).collect();
            let seen = |kind: &str, b: &Value| b["arrival"] == arrival && match kind {
                "act_counted" | "act_not_counted" => b["act"]["recordId"] == id,
                "arrival_declined" => b["declinedEventRef"] == id,
                _ => false,
            };
            if entries.iter().chain(pending.iter()).any(|e| seen(e["kind"].as_str().unwrap_or_default(), &e["body"])) {
                continue;
            }
            if disposition(entries, &out, &arrival).as_deref() != Some("waiting") {
                break;
            }
            let b = &record["body"];
            let before = time < arrived;
            if record["kind"] == "act_declined" {
                if b["declinedKind"] == required && !before {
                    out.push(("arrival_declined", json!({"arrival":arrival,"declinedEventRef":id})));
                    out.push(("disposition_change", json!({"arrival":arrival,"disposition":"resolved negatively","annotations":[]})));
                }
                continue;
            }
            let Some(kind) = b["actKind"].as_str().filter(|k| ACT_KINDS.contains(k)) else { continue };
            let act = json!({"recordId":id,"actKind":kind,"capturedAt":time,"capturingSurface":"app_act_control"});
            let content = &b["boundContent"][index];
            let reason = if kind != required {
                "another act kind"
            } else if content["method"] == method && content["value"] == value {
                let ordinal = 1 + entries.iter().chain(pending.iter())
                    .filter(|e| e["kind"] == "disposition_change" && e["body"]["arrival"] == arrival && e["body"]["disposition"] == "performed").count();
                out.push(("act_counted", json!({"arrival":arrival,"act":act,"relation":if before {"earlier act"} else {"after arrival"},"referents":[subject]})));
                let annotations = if before { json!([{"label":"by earlier act","actRef":id,"time":time,"referents":[subject]}]) } else { json!([]) };
                out.push(("disposition_change", json!({"arrival":arrival,"disposition":"performed","performanceOrdinal":ordinal,"answeredBy":[id],"annotations":annotations})));
                continue;
            } else if before {
                "content no longer current"
            } else {
                "act on other content"
            };
            out.push(("act_not_counted", json!({"arrival":arrival,"act":act,"reason":reason,"capturedBeforeArrival":before})));
            let annotations = match (before, reason) {
                (true, _) => json!([{"label":"prior act not counted","actRef":id,"reason":reason}]),
                (false, "act on other content") => json!([{"label":"act on other content","actRefs":[id]}]),
                _ => json!([]),
            };
            out.push(("disposition_change", json!({"arrival":arrival,"disposition":"waiting","annotations":annotations})));
        }
    }
    out
}

/// The first non-empty line of a message, trimmed (WD OP-1).
fn first_line(text: &str) -> Option<&str> {
    text.lines().map(str::trim).find(|l| !l.is_empty())
}
/// AW-7 as this App reads it: the path a change *produces*. An `add` or an
/// in-place `update` produces its `path`; a moving `update` produces only its
/// destination `move_path`, never its source; a `delete` produces nothing.
/// Any other change kind produces nothing (PatchChangeKind at the pin).
fn produced_path(change: &Value) -> Option<&str> {
    let kind = &change["kind"];
    match kind["type"].as_str()? {
        "add" => change["path"].as_str(),
        "update" => match &kind["move_path"] {
            Value::Null => change["path"].as_str(),
            moved => moved.as_str(),
        },
        _ => None,
    }
}
/// AW-7: the change's path against the declared project-relative path.
fn same_path(changed: &str, declared: &str, root: &std::path::Path) -> bool {
    if changed == declared {
        return true;
    }
    let root = root.to_string_lossy();
    changed.strip_prefix(root.as_ref()).and_then(|rest| rest.strip_prefix('/')).is_some_and(|rest| rest == declared)
}
/// The bound subject (WD §4.3.6): the output itself for "named output";
/// any other class names objects this App does not identify.
fn referents(listed: &Listed, output: &str, item: &str, content: Value) -> Vec<Value> {
    if listed.subject == "named output" && listed.subject_output.as_deref().is_none_or(|o| o == output) {
        return vec![json!({"subject":format!("output {output}: {item}"),"content":content})];
    }
    vec![json!({"subject":format!("{} ({})", listed.subject, listed.subject_output.as_deref().unwrap_or(output)),
        "content":{"notObtainable":true,"reason":"the objects are not identified: this App reads no host or examination results that would name them"}})]
}
fn item_ref(row: &Value, conversation: &str) -> String {
    format!("item:{}/{}/{}", conversation, row["turnId"].as_str().unwrap_or_default(), row["native"]["id"].as_str().unwrap_or_default())
}
/// RC-9 at item start: the agent's own actions only; a `commandExecution`
/// counts only with source `agent` as reported when it started.
fn run_action(row: &Value) -> bool {
    let start = &row["startNative"];
    let kind = start["type"].as_str().unwrap_or_default();
    RUN_ACTIONS.contains(&kind) && (kind != "commandExecution" || start["source"] == "agent")
}
/// The latest recorded disposition of an arrival, from the run's entries
/// and the outputs not yet appended.
fn disposition(entries: &[Value], pending: &[Output], arrival: &Value) -> Option<String> {
    entries.iter().map(|e| (e["kind"].as_str().unwrap_or_default(), &e["body"]))
        .chain(pending.iter().map(|(k, b)| (*k, b)))
        .filter(|(k, b)| *k == "disposition_change" && b["arrival"] == *arrival)
        .last().and_then(|(_, b)| b["disposition"].as_str().map(str::to_owned))
}
/// When an arrival became *performed*: its arrival time, or the latest
/// capture time of an act counted for it after the arrival.
fn performed_at(entries: &[Value], pending: &[Output], arrival: &Value) -> Option<String> {
    let all = || entries.iter().map(|e| (e["kind"].as_str().unwrap_or_default(), &e["body"])).chain(pending.iter().map(|(k, b)| (*k, b)));
    let arrived = all().find(|(k, b)| *k == "checkpoint_arrival" && b["checkpoint"] == arrival["checkpoint"] && b["arrivalOrdinal"] == arrival["arrivalOrdinal"])
        .and_then(|(_, b)| b["event"]["evidencedTime"]["value"].as_str().map(str::to_owned))?;
    let latest = all().filter(|(k, b)| *k == "act_counted" && b["arrival"] == *arrival && b["relation"] == "after arrival")
        .filter_map(|(_, b)| b["act"]["capturedAt"].as_str().map(str::to_owned)).max();
    Some(latest.map_or(arrived.clone(), |t| t.max(arrived)))
}
/// CE-17 `waitingArrivals` from RS entries (`kind`, `body`) of one run, in
/// arrival order: every arrival whose latest disposition is *waiting*.
pub(crate) fn waiting_arrivals(entries: &[Value]) -> Vec<Value> {
    entries.iter().filter(|e| e["kind"] == "checkpoint_arrival")
        .map(|e| json!({"checkpoint":e["body"]["checkpoint"],"arrivalOrdinal":e["body"]["arrivalOrdinal"]}))
        .filter(|arrival| disposition(entries, &[], arrival).as_deref() == Some("waiting"))
        .collect()
}
/// The human-act and act-declined records of a project's record set; an
/// incomplete record set is not read (nothing is counted from part of it).
pub(crate) fn project_act_records(root: &Path) -> Result<Vec<Value>, String> {
    let (all, limits) = crate::storage::read_all(root);
    if !limits.is_empty() {
        return Err(format!("the project's record set is incomplete: {limits:?}"));
    }
    Ok(all.into_iter().filter(|e| matches!(e["kind"].as_str(), Some("human_act" | "act_declined"))).collect())
}

#[cfg(test)]
#[path = "checkpoint_recorder_tests.rs"]
pub(crate) mod tests;
