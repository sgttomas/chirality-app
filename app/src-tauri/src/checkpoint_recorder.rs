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
//!   (RS §6, written by the App act control), each verified against the one
//!   capture object it cites ([`project_act_records`]), with their CE-18 labels
//!   (SP-1…SP-8, SP-6 earlier acts included; [`count_acts`]);
//! - CE-12 `continued_past` once per waiting arrival, for the first agent run
//!   action (RC-9) the App received after the arrival, and CE-11
//!   `run_resumed` for the first run action started after the act that made
//!   an arrival *performed*;
//! - CE-10 `act_lapsed` (with its CE-18 label where the transition table
//!   writes one) while the run is live, when the App reads the file an act
//!   answering an arrival is bound to and its content identity differs, the
//!   file is absent, or the identity cannot be compared or read
//!   ([`observe_lapses`]; RC-8, PH-8, A-10; RS L-1…L-6, L-11);
//! - the waiting arrivals listed by CE-17 `run_ended` (`waiting`).
//!
//! Recording is not a reaction (RC-4): nothing here sends, asks, opens,
//! pauses, re-holds or refuses anything; the outputs are entries for the run
//! record and nothing else. CE-7 never arises in an App run: A5 is valid only
//! at a host outcome (FB-16), which this App does not evaluate (AW-8…AW-10).
//! Nothing is observed after the run's end, so no *after run end* lapse
//! (CE-10) and no CE-16 `act_after_run_end` is written.
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::path::Path;

/// The App's exact-byte content method (RS §6.2a, CC-CONTENT-RX).
const EXACT_BYTES: &str = "chirality.app.exact-bytes.sha256/v1";
const ACT_COUNTING: &str = "Acts are counted from the App-file act and decline records in this project's record set, each only through the capture object it cites (SP-3; the App act control's captures): an act of the required kind bound to this referent's content counts, an earlier one included (SP-6). A capture counts only when its seal verifies under a key this App installation holds (AAC §6.3 SEAL-C); an unsealed capture, or one sealed by another installation, is not verified here and not counted. A seal shows a holder of this installation's key wrote the capture, not that a person acted or who: any process that can read the key, a same-user process or an agent whose sandbox can read the App data folder included, could seal. Acts on host content and A12 control relations are not observed by this App.";
const MESSAGE_ACT_LIMIT: &str = "No App act control binds an act to an agent message (CAP-1 binds App files by content identity), so no act can be counted for this arrival.";
const MESSAGE_LIMIT: &str = "The designating line marks where the agent put the output; it does not show that the content is what the declaration describes (AW-6).";
const FILE_LIMIT: &str = "Only an add, an in-place update or a move onto the declared path counts; a delete or a move away does not (this App's reading of AW-7). The path is compared with the declared project-relative path after removing the project root from an absolute path and normalizing `.` segments and repeated separators on both sides; a path with `..` never matches; how Codex reports file paths is not observed (O-8, U-E26).";
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
    /// CE-10: the exact-byte identity last read of each bound file, with the
    /// file's metadata stamp then; read again only when the stamp changes.
    contents: std::collections::BTreeMap<String, Seen>,
}

/// A regular file's device, inode, size and modification and change times.
type Stamp = (u64, u64, u64, i64, i64, i64, i64);
/// A bound file's identity as last read, its stamp then and when it was read
/// (seconds since the epoch).
#[derive(Clone, Debug)]
struct Seen {
    stamp: Stamp,
    value: String,
    read_at: i64,
}
fn stamp(m: &std::fs::Metadata) -> Stamp {
    use std::os::unix::fs::MetadataExt;
    (m.dev(), m.ino(), m.len(), m.mtime(), m.mtime_nsec(), m.ctime(), m.ctime_nsec())
}

/// One recorder output: the RS entry kind and its CE body.
pub(crate) type Output = (&'static str, Value);
/// The project's human-act and act-declined records, read only when needed.
pub(crate) type ActSource<'a> = &'a mut dyn FnMut() -> Result<ActRead, String>;

/// The project's App-file acts and declines as the recorder may count them.
/// `acts` are `{record, capture}`: current (uncorrected) records written by
/// the App's capturing surface whose one cited capture object resolves,
/// validates and says what the record says (SP-3, RS R-8, HA-1).
/// `unresolved` are `{record, reason}`: records that claim a file act but
/// cannot be so verified; they never become acts (RS §13.7) and are shown as
/// an "unresolvable reference" limit on an arrival whose file they name.
#[derive(Clone, Debug, Default)]
pub(crate) struct ActRead {
    pub acts: Vec<Value>,
    pub unresolved: Vec<Value>,
}

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
        // The act records, read at most once per observation and only while an
        // arrival waits or has a performance whose content can lapse.
        let mut records: Option<ActRead> = None;
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
                                        } else if !arrival.continued {
                                            // Started before the act that answered: it went on past the
                                            // checkpoint, although the act was counted first (PH-7).
                                            arrival.continued = true;
                                            written.push(("continued_past", json!({"arrival":arrival.reference(),"actionRef":reference,"actKind":arrival.act})));
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
        // CE-10 after the received items: the files are read now, after every item
        // this view delivered, so a resume point among them precedes the lapse
        // observation (RC-8, HD-5). Acts are then counted again against the content
        // now current (EXEC §2.4.3).
        self.lapses(entries, &mut written, scope.project_root, &mut *acts, &mut records);
        self.count(entries, &mut written, scope.project_root, &mut *acts, &mut records);
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
    fn count(&mut self, entries: &[Value], written: &mut Vec<Output>, root: &Path, acts: &mut dyn FnMut() -> Result<ActRead, String>, records: &mut Option<ActRead>) {
        let all: Vec<Value> = entries.iter().cloned().chain(written.iter().map(|(k, b)| json!({"kind":k,"body":b}))).collect();
        if waiting_arrivals(&all).is_empty() || !self.read_acts(acts, records) {
            return;
        }
        if let Some(read) = records.as_ref() {
            written.extend(count_acts(&all, read, root));
        }
    }

    /// CE-10 for the arrivals with a performance, from the project's act
    /// records (read once, lazily) and the bound files as the App reads them
    /// now ([`observe_lapses`]). A read of the act records that fails claims
    /// no lapse and no currency (A-10). A lapse before the resume point opens
    /// the way for a new resume point after the next performance (CE-11).
    fn lapses(&mut self, entries: &[Value], written: &mut Vec<Output>, root: &Path, acts: &mut dyn FnMut() -> Result<ActRead, String>, records: &mut Option<ActRead>) {
        let all: Vec<Value> = entries.iter().cloned().chain(written.iter().map(|(k, b)| json!({"kind":k,"body":b}))).collect();
        if !lapse_evaluable(&all) || !self.read_acts(acts, records) {
            return;
        }
        let Some(read) = records.as_ref() else { return };
        let cache = &mut self.contents;
        let outputs = observe_lapses(&all, read, &crate::util::now_rfc3339(), &mut |subject| cached_content(cache, root, subject));
        for (_, body) in outputs.iter().filter(|(k, b)| *k == "act_lapsed" && b["when"] == "before resume") {
            for arrival in self.arrivals.iter_mut().filter(|a| a.reference() == body["arrival"]) {
                arrival.resumed = false;
            }
        }
        written.extend(outputs);
    }

    /// The project's act records for this observation, read at most once; a
    /// failed read is kept as the recorder's acts limit and retried next time.
    fn read_acts(&mut self, acts: &mut dyn FnMut() -> Result<ActRead, String>, records: &mut Option<ActRead>) -> bool {
        if records.is_some() {
            return true;
        }
        match acts() {
            Ok(read) => {
                self.acts_limit = None;
                *records = Some(read);
                true
            }
            Err(e) => {
                self.acts_limit = Some(format!("act records not read; no act counted and no lapse observed at this observation: {e}"));
                false
            }
        }
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
                    found.push((index, referents(listed, output, &format!("file {}", normal(path).unwrap_or_else(|| path.clone())), file_content(scope.project_root, path)), vec![FILE_LIMIT, FILE_READ_LIMIT]));
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

/// The largest file whose content identity AW-7 reads.
const FILE_READ_CAP: u64 = 256 * 1024 * 1024;
/// AW-7's bound content: the exact bytes of the declared file in the project,
/// read now as one coherent snapshot (RS §6.2a): a regular file inside the
/// project, opened without following a final link and without blocking,
/// hashed as it streams, with its identity and times unchanged across the
/// read. Anything else is not obtainable, so no act can count for it.
fn file_content(root: &Path, declared: &str) -> Value {
    let read = normal(declared).ok_or_else(|| "the declared path is not a plain project-relative path".to_owned())
        .and_then(|rel| exact_bytes(root, Path::new(&rel)));
    match read {
        Ok(value) => json!({"method":EXACT_BYTES,"value":value,"scope":"the file's bytes as the App read them after observing the completed change"}),
        Err(reason) => json!({"notObtainable":true,"reason":format!("{reason}; no act can be counted for this referent (SP-4)")}),
    }
}

/// The exact-byte identity (RS §6.2a) of `path` in the project, relative to
/// its root or absolute inside it, read as one coherent snapshot as AW-7
/// reads it.
fn exact_bytes(root: &Path, path: &Path) -> Result<String, String> {
    use sha2::Digest;
    use std::io::Read;
    use std::os::unix::fs::OpenOptionsExt;
    let root = std::fs::canonicalize(root).map_err(|e| format!("project root not readable: {e}"))?;
    let file = std::fs::canonicalize(root.join(path)).map_err(|e| format!("file not readable: {e}"))?;
    if !file.starts_with(&root) || file == root {
        return Err("the declared path resolves outside the project".into());
    }
    let named = std::fs::symlink_metadata(&file).map_err(|e| format!("file not readable: {e}"))?;
    if !named.file_type().is_file() {
        return Err("not a regular file".into());
    }
    let mut f = std::fs::OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(&file).map_err(|e| format!("file not readable: {e}"))?;
    let before = f.metadata().map_err(|e| e.to_string())?;
    if !before.is_file() || stamp(&before) != stamp(&named) {
        return Err("not the regular file named by the path".into());
    }
    if before.len() > FILE_READ_CAP {
        return Err(format!("larger than {FILE_READ_CAP} bytes; not read"));
    }
    let mut hasher = sha2::Sha256::new();
    let mut buf = vec![0u8; 64 * 1024];
    let mut total = 0u64;
    loop {
        let n = f.read(&mut buf).map_err(|e| format!("file not readable: {e}"))?;
        if n == 0 {
            break;
        }
        total += n as u64;
        if total > FILE_READ_CAP {
            return Err(format!("larger than {FILE_READ_CAP} bytes; not read"));
        }
        hasher.update(&buf[..n]);
    }
    #[cfg(test)]
    tests::DURING_READ.with(|hook| if let Some(hook) = hook.borrow().as_ref() { hook(&file) });
    let after = f.metadata().map_err(|e| e.to_string())?;
    let named_after = std::fs::symlink_metadata(&file).map_err(|e| e.to_string())?;
    if stamp(&before) != stamp(&after) || stamp(&after) != stamp(&named_after) {
        return Err("the file changed while it was read".into());
    }
    Ok(format!("{:x}", hasher.finalize()))
}

/// A bound App file's current content as the App reads it now (RS §7 L-1,
/// L-3, L-4): its exact-byte identity, absent (nothing at the bound path), or
/// not obtainable with the reason.
#[derive(Clone, Debug, PartialEq)]
pub(crate) enum Current {
    Present(String),
    Absent,
    Unavailable(String),
}
/// The current content of an act's bound subject, an absolute path inside
/// the project as the act control names it.
pub(crate) fn current_content(root: &Path, subject: &Path) -> Current {
    match exact_bytes(root, subject) {
        Ok(value) => Current::Present(value),
        Err(reason) => {
            let contained = std::fs::canonicalize(root).is_ok_and(|root| subject.starts_with(&root) && subject != root)
                && subject.components().all(|c| matches!(c, std::path::Component::RootDir | std::path::Component::Normal(_)));
            if contained && std::fs::symlink_metadata(subject).is_err_and(|e| e.kind() == std::io::ErrorKind::NotFound) {
                Current::Absent
            } else {
                Current::Unavailable(reason)
            }
        }
    }
}
/// [`current_content`] read again only when the regular file's stamp has
/// changed since the identity in `cache` was read (as the act records are
/// read again only when their fingerprint changes). An identity read less
/// than two seconds after the file's change time is not reused, so that a
/// rewrite within a coarse timestamp's same second is still read.
fn cached_content(cache: &mut std::collections::BTreeMap<String, Seen>, root: &Path, subject: &Path) -> Current {
    let key = subject.to_string_lossy().into_owned();
    let before = std::fs::symlink_metadata(subject).ok().filter(std::fs::Metadata::is_file).map(|m| stamp(&m));
    if let (Some(now), Some(seen)) = (before, cache.get(&key)) {
        if now == seen.stamp && seen.read_at > now.5 + 1 {
            return Current::Present(seen.value.clone());
        }
    }
    let read_at = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map_or(0, |d| d.as_secs() as i64);
    let read = current_content(root, subject);
    match (&read, before) {
        (Current::Present(value), Some(stamp)) => {
            cache.insert(key, Seen { stamp, value: value.clone(), read_at });
        }
        _ => {
            cache.remove(&key);
        }
    }
    read
}

/// RFC 3339 UTC text with milliseconds, as the App and `rfc3339_from_ms`
/// write it, so that two such times order as text.
fn comparable(time: &str) -> bool {
    let b = time.as_bytes();
    b.len() == 24 && b[4] == b'-' && b[10] == b'T' && b[19] == b'.' && b[23] == b'Z'
}

/// CE-5, CE-6, CE-8 (EXEC §2.4.3, §4.5 SP-1…SP-8, RC-7) over a run's
/// entries (`kind`, `body`) and the project's verified acts ([`ActRead`]).
/// Rebuildable (RC-10): an act already cited for an arrival is not read
/// again, and only arrivals whose latest label is *waiting* are evaluated.
///
/// An act is on an arrival's subject when the arrival's one referent is the
/// declared file of a named output (AW-7) and the act's bound subject is that
/// file as resolved in the project now. Content is compared only under the
/// same method (SB-1); under another method it is incomparable and neither
/// counts nor is said to differ. In capture order, until the arrival is
/// decided (§4.6: the first decides):
/// - before the arrival, the latest decision of the required kind on the
///   current content governs: an act makes the arrival *performed* "by
///   earlier act" (SP-6); a decline resolves it negatively (CE-8); earlier
///   decisions of that kind on that content are superseded;
/// - at or after the arrival, a decline of the required kind on the current
///   content resolves it negatively, and an act of the required kind on the
///   current content counts (CE-5);
/// - an act of another kind is not counted, "another act kind" (CE-6);
/// - an act of the required kind on other content is not counted: "content
///   no longer current" before the arrival, "act on other content" after it.
///
/// A referent whose content is not obtainable binds no act (A-5, SP-4). After
/// a recorded lapse (CE-10) the content compared is the one the latest
/// determinate lapse observation read; while the subject is absent no act
/// counts (§4.7). A record that claims an act on the arrival's file but
/// cannot be verified against its capture adds an "unresolvable reference"
/// limit, once.
pub(crate) fn count_acts(entries: &[Value], read: &ActRead, root: &Path) -> Vec<Output> {
    let root = std::fs::canonicalize(root).unwrap_or_else(|_| root.to_path_buf());
    let mut out: Vec<Output> = Vec::new();
    let named = |record: &Value| -> Value {
        let b = &record["body"];
        if record["kind"] == "act_declined" { b["subject"].clone() } else { b["boundSubject"].clone() }
    };
    for arrival_entry in entries.iter().filter(|e| e["kind"] == "checkpoint_arrival") {
        let body = &arrival_entry["body"];
        let arrival = json!({"checkpoint":body["checkpoint"],"arrivalOrdinal":body["arrivalOrdinal"]});
        let referents = body["referents"].as_array().map(Vec::as_slice).unwrap_or_default();
        let ([referent], Some(required), Some(arrived)) = (referents, body["requiredAct"].as_str(), body["event"]["evidencedTime"]["value"].as_str()) else { continue };
        // After a recorded lapse the referent needs an act on its current content
        // (EXEC §2.4.3 CE-10 rows; §4.7 RH-2): the content the latest determinate
        // lapse observation read, and none while the subject is absent (§4.7).
        let content = match observed_content(entries, &arrival) {
            None => &referent["content"],
            Some(c1) if c1.is_object() => c1,
            Some(_) => continue,
        };
        let (Some(subject), Some(method), Some(value)) = (referent["subject"].as_str(), content["method"].as_str(), content["value"].as_str()) else { continue };
        if !subject.starts_with("output ") || !comparable(arrived) {
            continue;
        }
        // The arrival's file, resolved now as the act control resolves its subjects.
        let files: Vec<std::path::PathBuf> = subject.match_indices(": file ")
            .filter_map(|(i, m)| normal(&subject[i + m.len()..]))
            .filter_map(|rel| std::fs::canonicalize(root.join(rel)).ok())
            .filter(|f| f.starts_with(&root) && *f != root)
            .collect();
        if files.is_empty() {
            continue;
        }
        let on_subject = |subjects: &Value| -> Option<usize> {
            subjects.as_array()?.iter().position(|s| s.as_str().is_some_and(|p| files.iter().any(|f| Path::new(p) == f)))
        };
        let pending = |out: &[Output]| -> Vec<Value> { out.iter().map(|(k, b)| json!({"kind":k,"body":b})).collect() };
        if disposition(entries, &out, &arrival).as_deref() != Some("waiting") {
            continue;
        }
        for unresolved in &read.unresolved {
            let record = &unresolved["record"];
            let Some(id) = record["recordId"].as_str() else { continue };
            let shown = pending(&out);
            let limited = entries.iter().chain(shown.iter()).any(|e| e["kind"] == "evidence_limit" && e["body"]["label"] == "unresolvable reference" && e["body"]["subjectRef"] == id);
            if !limited && on_subject(&named(record)).is_some() {
                out.push(("evidence_limit", json!({"label":"unresolvable reference","subjectRef":id,
                    "detail":format!("{}; not counted as an act (RS §13.7)", unresolved["reason"].as_str().unwrap_or("capture evidence not resolved"))})));
            }
        }
        // (time, record identity, record, kind, content) of each verified act or decline on this file.
        let mut candidates: Vec<(&str, &str, &Value, &str, &Value)> = read.acts.iter().filter_map(|a| {
            let record = &a["record"];
            let b = &record["body"];
            let id = record["recordId"].as_str()?;
            let index = on_subject(&named(record))?;
            if record["kind"] == "act_declined" {
                Some((b["time"].as_str().filter(|t| comparable(t))?, id, record, b["declinedKind"].as_str()?, &a["capture"]["boundContent"][index]))
            } else {
                Some((b["captureTime"].as_str().filter(|t| comparable(t))?, id, record, b["actKind"].as_str()?, &b["boundContent"][index]))
            }
        }).collect();
        candidates.sort_by(|a, b| (a.0, a.1).cmp(&(b.0, b.1)));
        // SB-1: Some(equal) under the same method; None when incomparable.
        let same = |content: &Value| -> Option<bool> { (content["method"] == method).then(|| content["value"] == value) };
        let governing = candidates.iter().filter(|c| c.0 < arrived && c.3 == required && same(c.4) == Some(true)).last().map(|c| c.1);
        for (time, id, record, kind, content) in candidates {
            let before = time < arrived;
            if before && kind == required && same(content) == Some(true) && Some(id) != governing {
                continue; // superseded by a later decision before the arrival
            }
            let shown = pending(&out);
            let seen = |k: &str, b: &Value| b["arrival"] == arrival && match k {
                "act_counted" | "act_not_counted" => b["act"]["recordId"] == id,
                "arrival_declined" => b["declinedEventRef"] == id,
                _ => false,
            };
            if entries.iter().chain(shown.iter()).any(|e| seen(e["kind"].as_str().unwrap_or_default(), &e["body"])) {
                continue;
            }
            if disposition(entries, &out, &arrival).as_deref() != Some("waiting") {
                break;
            }
            if record["kind"] == "act_declined" {
                if kind == required && same(content) == Some(true) {
                    out.push(("arrival_declined", json!({"arrival":arrival,"declinedEventRef":id})));
                    out.push(("disposition_change", json!({"arrival":arrival,"disposition":"resolved negatively","annotations":[]})));
                }
                continue;
            }
            if !ACT_KINDS.contains(&kind) {
                continue;
            }
            let act = json!({"recordId":id,"actKind":kind,"capturedAt":time,"capturingSurface":"app_act_control"});
            let reason = if kind != required {
                "another act kind"
            } else {
                match same(content) {
                    None => continue, // incomparable methods (SB-1): neither counted nor said to differ
                    Some(true) => {
                        // The next performance ordinal (RS L-12): a lapse label repeats the ordinal it lapses.
                        let ordinal = 1 + entries.iter().chain(shown.iter())
                            .filter(|e| e["kind"] == "disposition_change" && e["body"]["arrival"] == arrival)
                            .filter_map(|e| e["body"]["performanceOrdinal"].as_u64()).max().unwrap_or(0);
                        out.push(("act_counted", json!({"arrival":arrival,"act":act,"relation":if before {"earlier act"} else {"after arrival"},"referents":[subject]})));
                        let annotations = if before { json!([{"label":"by earlier act","actRef":id,"time":time,"referents":[subject]}]) } else { json!([]) };
                        out.push(("disposition_change", json!({"arrival":arrival,"disposition":"performed","performanceOrdinal":ordinal,"answeredBy":[id],"annotations":annotations})));
                        continue;
                    }
                    Some(false) if before => "content no longer current",
                    Some(false) => "act on other content",
                }
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

/// A lapse state that says nothing about the content (RS L-2, L-3).
fn unknown_state(state: &Value) -> bool {
    state.as_str().is_some_and(|s| s.starts_with("unknown"))
}
/// The `c1` of the latest determinate `act_lapsed` recorded for an arrival:
/// the content identity it read, or "subject absent". None when no lapse
/// observation with a known state is recorded.
fn observed_content<'a>(entries: &'a [Value], arrival: &Value) -> Option<&'a Value> {
    entries.iter().filter(|e| e["kind"] == "act_lapsed" && e["body"]["arrival"] == *arrival && !unknown_state(&e["body"]["state"]))
        .last().map(|e| &e["body"]["c1"])
}
/// The latest performance of an arrival: its first CE-18 label with the
/// highest performance ordinal, and that label's position in `entries`.
fn latest_performance<'a>(entries: &'a [Value], arrival: &Value) -> Option<(usize, &'a Value)> {
    let labels = || entries.iter().enumerate().filter(|(_, e)| e["kind"] == "disposition_change" && e["body"]["arrival"] == *arrival);
    let top = labels().filter_map(|(_, e)| e["body"]["performanceOrdinal"].as_u64()).max()?;
    labels().find(|(_, e)| e["body"]["disposition"] == "performed" && e["body"]["performanceOrdinal"].as_u64() == Some(top)).map(|(i, e)| (i, &e["body"]))
}
/// Whether any arrival in a run's entries has a performance whose acts' content
/// can still lapse while the run is live: its latest label is *performed*, or
/// *waiting* again after a lapse before the resume point (EXEC §2.4.3).
pub(crate) fn lapse_evaluable(entries: &[Value]) -> bool {
    entries.iter().filter(|e| e["kind"] == "checkpoint_arrival").any(|e| {
        let arrival = json!({"checkpoint":e["body"]["checkpoint"],"arrivalOrdinal":e["body"]["arrivalOrdinal"]});
        matches!(disposition(entries, &[], &arrival).as_deref(), Some("performed" | "waiting")) && latest_performance(entries, &arrival).is_some()
    })
}

/// CE-10 (EXEC §2.4.2, §2.4.3 CE-10 rows, RC-8, PH-8, §2.6 A-10; RS §7 L-1…L-6,
/// L-11, L-12) for a live run, from its entries (`kind`, `body`), the
/// project's verified acts ([`ActRead`]) and `current`, which reads a bound
/// file now. Observation only: nothing is sent, re-held or refused, and no
/// act record is changed (RC-4, PH-8, L-8).
///
/// For each arrival whose latest label is *performed*, or *waiting* again
/// after a lapse, each act its latest performance cites (`answeredBy`) that
/// is a current verified App-file act with one bound subject is compared with
/// that file's content now (`standing::compare`, as the file-act view
/// compares): the act's bound content `c0` against `c1` under the same method.
/// A changed identity is *lapsed*, a missing file *lapsed (subject absent)*,
/// another method *unknown (incomparable)*, an unreadable file *unknown
/// (unavailable)*, and the content back at `c0` after a recorded lapse
/// "matches c0 again after observed lapse". The same content is nothing.
/// Each entry cites the act, its bound subject as the act record names it,
/// `c0`, `c1`, the observation time `now`, the arrival, and *before resume*
/// unless the arrival is *performed* and a `run_resumed` follows its latest
/// performance (HD-5: measured against the recorded resume point).
///
/// An entry is written only when the observation differs from the latest
/// one recorded for that arrival and act: a known state from the latest known
/// one (state and `c1`), an unknown state from the latest one of any state.
/// A recorded *lapsed* or *lapsed (subject absent)* with no label for the
/// arrival after it (its label's write failed, RS W-2) gets that label once,
/// with the recorded lapse's time and *when*.
/// Only *lapsed* and *lapsed (subject absent)* write a CE-18 label: before
/// the resume point the arrival is *waiting* "waiting — lapsed at ‹t›" (and
/// "subject absent"); after it, it stays *performed* with "act lapsed at ‹t›"
/// and its ordinal and acts (RC-8). An unknown state claims no lapse and no
/// currency (A-10), and the effect of content back at `c0` is RS U-12, so
/// neither changes a label.
pub(crate) fn observe_lapses(entries: &[Value], read: &ActRead, now: &str, current: &mut dyn FnMut(&Path) -> Current) -> Vec<Output> {
    use crate::standing::{compare, CurrentContent, Lapse};
    let mut out: Vec<Output> = Vec::new();
    let pending = |out: &[Output]| -> Vec<Value> { entries.iter().cloned().chain(out.iter().map(|(k, b)| json!({"kind":k,"body":b}))).collect() };
    for arrival_entry in entries.iter().filter(|e| e["kind"] == "checkpoint_arrival") {
        let body = &arrival_entry["body"];
        let arrival = json!({"checkpoint":body["checkpoint"],"arrivalOrdinal":body["arrivalOrdinal"]});
        let referents = body["referents"].as_array().map(Vec::as_slice).unwrap_or_default();
        let [referent] = referents else { continue };
        let Some(shown) = referent["subject"].as_str() else { continue };
        let all = pending(&out);
        let latest = disposition(&all, &[], &arrival);
        if !matches!(latest.as_deref(), Some("performed" | "waiting")) {
            continue;
        }
        let Some((at, performance)) = latest_performance(&all, &arrival) else { continue };
        let resumed = all[at + 1..].iter().any(|e| e["kind"] == "run_resumed" && e["body"]["arrival"] == arrival);
        let when = if latest.as_deref() == Some("performed") && resumed { "after resume" } else { "before resume" };
        let (ordinal, answered) = (performance["performanceOrdinal"].clone(), performance["answeredBy"].clone());
        for id in answered.as_array().into_iter().flatten().filter_map(Value::as_str) {
            let Some(act) = read.acts.iter().map(|a| &a["record"]).find(|r| r["kind"] == "human_act" && r["recordId"] == id) else { continue };
            let b = &act["body"];
            let (Some([subject]), Some([c0])) = (b["boundSubject"].as_array().map(Vec::as_slice), b["boundContent"].as_array().map(Vec::as_slice)) else { continue };
            let (Some(path), Some(m0), Some(v0)) = (subject.as_str(), c0["method"].as_str(), c0["value"].as_str()) else { continue };
            let all = pending(&out);
            let prior: Vec<&Value> = all.iter().filter(|e| e["kind"] == "act_lapsed" && e["body"]["arrival"] == arrival && e["body"]["act"]["recordId"] == id).map(|e| &e["body"]).collect();
            let observed = prior.iter().any(|p| matches!(p["state"].as_str(), Some("lapsed" | "lapsed (subject absent)" | "partially lapsed")));
            let bound = crate::act_policy::ContentIdentity { method: m0.into(), value: v0.into() };
            let now_content = current(Path::new(path));
            let present = match &now_content {
                Current::Present(value) => Some(crate::act_policy::ContentIdentity { method: EXACT_BYTES.into(), value: value.clone() }),
                _ => None,
            };
            let state = compare(&bound, match (&now_content, &present) {
                (_, Some(identity)) => CurrentContent::Present(identity),
                (Current::Absent, _) => CurrentContent::Absent,
                _ => CurrentContent::Unavailable,
            }, observed);
            let identity = || json!({"method":EXACT_BYTES,"value":present.as_ref().map(|p| p.value.clone())});
            let (state, c1) = match (state, &now_content) {
                (Lapse::Lapsed, _) => ("lapsed", identity()),
                (Lapse::SubjectAbsent, _) => ("lapsed (subject absent)", json!("subject absent")),
                (Lapse::MatchesAgainAfterLapse, _) => ("matches c0 again after observed lapse", identity()),
                (Lapse::Incomparable, _) => ("unknown (incomparable)", identity()),
                (Lapse::Unavailable, Current::Unavailable(reason)) => ("unknown (unavailable)", json!({"notObtainable":true,"reason":format!("{reason}; no lapse and no currency is claimed (A-10)")})),
                _ => continue,
            };
            let repeated = if state.starts_with("unknown") {
                prior.last().is_some_and(|p| p["state"] == state)
            } else {
                prior.iter().rev().find(|p| !unknown_state(&p["state"])).is_some_and(|p| p["state"] == state && p["c1"] == c1)
            };
            // The lapse whose label is written: this observation, or a recorded one
            // that has no label after it (its label's write failed; RS W-2).
            let (time, when) = if repeated {
                let Some(position) = all.iter().rposition(|e| e["kind"] == "act_lapsed" && e["body"]["arrival"] == arrival && e["body"]["act"]["recordId"] == id) else { continue };
                let recorded = &all[position]["body"];
                let labelled = all[position + 1..].iter().any(|e| e["kind"] == "disposition_change" && e["body"]["arrival"] == arrival);
                if labelled || recorded["state"] != state || !matches!(state, "lapsed" | "lapsed (subject absent)") {
                    continue;
                }
                (recorded["time"].as_str().unwrap_or(now).to_owned(), recorded["when"].as_str().unwrap_or(when).to_owned())
            } else {
                out.push(("act_lapsed", json!({"act":{"recordId":id,"actKind":b["actKind"],"capturedAt":b["captureTime"],"capturingSurface":"app_act_control"},
                    "state":state,"referents":[path],"c0":c0,"c1":c1,"time":now,"arrival":arrival,"when":when})));
                (now.to_owned(), when.to_owned())
            };
            if !matches!(state, "lapsed" | "lapsed (subject absent)") {
                continue;
            }
            if when == "after resume" {
                out.push(("disposition_change", json!({"arrival":arrival,"disposition":"performed","performanceOrdinal":ordinal,"answeredBy":answered,
                    "annotations":[{"label":"act lapsed at","actRefs":[id],"time":time,"referents":[shown]}]})));
            } else {
                let mut annotations = vec![json!({"label":"waiting — lapsed at","actRefs":[id],"time":time,"referents":[shown]})];
                if state == "lapsed (subject absent)" {
                    annotations.push(json!({"label":"subject absent","referents":[shown]}));
                }
                out.push(("disposition_change", json!({"arrival":arrival,"disposition":"waiting","annotations":annotations})));
            }
        }
    }
    out
}

/// At the person's end of a run (EXEC A-11, CE-17), live or after a relaunch,
/// before `run_ended`: CE-10 for content changed since the last observation,
/// then CE-5, CE-6, CE-8 for acts recorded since, from the run's entries
/// (RC-10). While an arrival waits and the act records cannot be read, the
/// limit naming them ([`acts_unread_limit`]); the end is not refused.
pub(crate) fn end_observations(entries: &[Value], root: &Path) -> Vec<Output> {
    let waiting = !waiting_arrivals(entries).is_empty();
    if !waiting && !lapse_evaluable(entries) {
        return vec![];
    }
    match project_act_records(root) {
        Ok(read) => {
            let mut out = observe_lapses(entries, &read, &crate::util::now_rfc3339(), &mut |subject| current_content(root, subject));
            let all: Vec<Value> = entries.iter().cloned().chain(out.iter().map(|(k, b)| json!({"kind":k,"body":b}))).collect();
            out.extend(count_acts(&all, &read, root));
            out
        }
        Err(e) if waiting => vec![acts_unread_limit(&e)],
        Err(_) => vec![],
    }
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
/// A project-relative path with `.` segments and repeated separators
/// removed; None for an absolute path, an empty one or one with `..`.
fn normal(path: &str) -> Option<String> {
    let parts: Vec<&str> = path.split('/').filter(|p| !p.is_empty() && *p != ".").collect();
    (!path.starts_with('/') && !parts.is_empty() && !parts.contains(&"..")).then(|| parts.join("/"))
}
/// AW-7: the change's path against the declared project-relative path, both
/// normalized the same way; an absolute path counts only inside the root.
fn same_path(changed: &str, declared: &str, root: &std::path::Path) -> bool {
    let root = root.to_string_lossy();
    let relative = if changed.starts_with('/') {
        match changed.strip_prefix(root.as_ref()).and_then(|rest| rest.strip_prefix('/')) {
            Some(rest) => rest,
            None => return false,
        }
    } else {
        changed
    };
    normal(relative).is_some_and(|r| Some(r) == normal(declared))
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
/// The project's App-file acts and declines (A4, A6, A7), each verified
/// against the one capture object it cites, as `file_act_view` reads them:
/// the record set read once with its correction relations (RS W-3, R-6), a
/// corrected record skipped, the recorder the App's capturing surface (PH-4),
/// the capture resolved from the capture store, schema-checked, sealed
/// under a key this installation holds (AAC §6.3 SEAL-C) and
/// corresponding in kind, choice, actor, subject, content, scope, purpose and
/// time, and one record per capture (RS R-8). An incomplete record set is not
/// read: nothing is counted from part of it.
pub(crate) fn project_act_records(root: &Path) -> Result<ActRead, String> {
    let root = std::fs::canonicalize(root).map_err(|e| format!("project root not readable: {e}"))?;
    let paths = crate::storage::discover(&root)?;
    let projected = crate::decision_view::record_relations::read_logs(&paths);
    if let Some(limits) = projected["readLimits"].as_array().filter(|l| !l.is_empty()) {
        return Err(format!("the project's record set is incomplete: {limits:?}"));
    }
    let nonconformant: BTreeSet<&str> = projected["diagnostics"].as_array().into_iter().flatten()
        .filter(|d| d["state"] == "nonconformant").filter_map(|d| d["recordId"].as_str()).collect();
    let mut read = ActRead::default();
    let mut seen: BTreeSet<String> = BTreeSet::new();
    let mut by_capture: std::collections::BTreeMap<String, Vec<String>> = std::collections::BTreeMap::new();
    for claim in projected["claims"].as_array().into_iter().flatten() {
        let record = &claim["record"];
        let decline = record["kind"] == "act_declined";
        let b = &record["body"];
        let kind = if decline { &b["declinedKind"] } else { &b["actKind"] };
        if !(decline || record["kind"] == "human_act") || !matches!(kind.as_str(), Some("A4" | "A6" | "A7")) {
            continue;
        }
        let Some(id) = record["recordId"].as_str() else { continue };
        if nonconformant.contains(id) || !seen.insert(id.to_owned()) {
            continue;
        }
        if claim["correctedBy"].as_array().is_some_and(|c| !c.is_empty()) {
            continue; // a corrected record is not current (RS R-6)
        }
        let verified: Result<Value, String> = if let Some(limit) = claim["relationLimit"].as_str() {
            Err(format!("record relation not resolved: {limit}"))
        } else if claim["identityResolution"] == "conflicting identity" {
            Err("conflicting record identity".into())
        } else if record["recorder"]["role"] != crate::records::APP_INTERFACE.role || record["recorder"]["identity"] != crate::records::APP_INTERFACE.identity {
            Err("not written by the App's capturing surface (PH-4)".into())
        } else {
            match crate::file_act_view::capture(&root, b) {
                Err(e) => Err(format!("capture evidence not resolved: {e}")),
                Ok(capture) if !crate::file_act_view::corresponds(&capture, record) => Err("the record differs from the capture it cites".into()),
                Ok(capture) => Ok(capture),
            }
        };
        match verified {
            Ok(capture) => {
                by_capture.entry(capture["captureId"].as_str().unwrap_or_default().to_owned()).or_default().push(id.to_owned());
                read.acts.push(json!({"record":record,"capture":capture}));
            }
            Err(reason) => read.unresolved.push(json!({"record":record,"reason":reason})),
        }
    }
    // RS R-8: one capture is one act; records sharing a capture are none of them acts.
    let shared: BTreeSet<&String> = by_capture.values().filter(|ids| ids.len() > 1).flatten().collect();
    if !shared.is_empty() {
        let (kept, refused): (Vec<Value>, Vec<Value>) = read.acts.into_iter().partition(|a| a["record"]["recordId"].as_str().is_none_or(|id| !shared.contains(&id.to_owned())));
        read.acts = kept;
        read.unresolved.extend(refused.into_iter().map(|a| json!({"record":a["record"],"reason":"several records cite one capture (RS R-8)"})));
    }
    Ok(read)
}
/// The limit written before `run_ended` when the person ends a run while an
/// arrival waits and the act records cannot be read (EXEC A-11: the person's
/// explicit end ends the run; it is not refused).
pub(crate) fn acts_unread_limit(reason: &str) -> Output {
    ("evidence_limit", json!({"label":"unresolvable reference","subjectRef":"the project's act records",
        "detail":format!("The project's act records could not be read when the run ended, so acts recorded since the last observation were not counted and waitingArrivals may list an arrival whose act was done: {reason}")}))
}
/// A fingerprint of the project's record logs and capture store (paths,
/// sizes and modification times): the act records are read again only when
/// it changes.
pub(crate) fn act_records_fingerprint(root: &Path) -> Option<Vec<(String, u64, i64, i64)>> {
    use std::os::unix::fs::MetadataExt;
    let mut paths = crate::storage::discover(root).ok()?;
    let store = crate::storage::capture_path(root, "x");
    if let Some(dir) = store.parent() {
        paths.push(dir.to_path_buf());
        if let Ok(entries) = std::fs::read_dir(dir) {
            paths.extend(entries.filter_map(|e| e.ok().map(|e| e.path())));
        }
    }
    paths.sort();
    Some(paths.into_iter().map(|p| {
        let m = std::fs::metadata(&p).ok();
        (p.to_string_lossy().into_owned(), m.as_ref().map_or(0, |m| m.len()), m.as_ref().map_or(0, |m| m.mtime()), m.as_ref().map_or(0, |m| m.mtime_nsec()))
    }).collect())
}

#[cfg(test)]
#[path = "checkpoint_recorder_tests.rs"]
pub(crate) mod tests;
