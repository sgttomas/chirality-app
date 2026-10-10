//! The current-phase checkpoint recorder, first slice (DEL-02-03 EXEC §2.4
//! RC-1…RC-10, §2.5 AW-6, AW-7, AE-5; §2.6 A-2, A-5, A-9, A-11, A-12). The
//! EXEC Design text and its entry-body schema are DRAFT/PROPOSED.
//!
//! What it records, in the run's own RS log, through the App writer:
//! - CE-1 `checkpoint_listed` for each recognized declared checkpoint at run
//!   start, with whether this App evaluates its arrival;
//! - CE-3 `checkpoint_arrival` (with its CE-18 `disposition_change`
//!   *waiting*) only from native items this App observed live: a completed
//!   `agentMessage` whose first non-empty line, trimmed, equals a message
//!   output's designating line exactly (AW-6, WD OP-1…OP-4), or a completed
//!   `fileChange` whose changes include a file output's declared path (AW-7);
//! - CE-12 `continued_past` once per waiting arrival, for the first agent run
//!   action (RC-9) the App received after the arrival, and CE-11
//!   `run_resumed` for the first run action after an arrival's record reads
//!   *performed*;
//! - the waiting arrivals listed by CE-17 `run_ended` (`waiting`).
//!
//! Recording is not a reaction (RC-4): nothing here sends, asks, opens,
//! pauses or refuses anything; the outputs are entries for the run record and
//! nothing else. No act is counted (CE-5/CE-6 are not implemented), so an
//! arrival stays *waiting*: reached, with no act recorded against it here.
//! Each arrival says so in its limits.
use serde_json::{json, Value};
use std::collections::BTreeSet;

/// The App's exact-byte content method (RS §6.2a, CC-CONTENT-RX).
const EXACT_BYTES: &str = "chirality.app.exact-bytes.sha256/v1";
const NO_ACT_COUNTING: &str = "Acts are not counted by this App yet (EXEC CE-5/CE-6): an earlier or later act on this subject is not evaluated against this arrival, so waiting means only that no act is recorded against it here.";
const MESSAGE_LIMIT: &str = "The designating line marks where the agent put the output; it does not show that the content is what the declaration describes (AW-6).";
const FILE_LIMIT: &str = "The change's path is compared with the declared project-relative path as text, after removing the project root from an absolute path; how Codex reports file paths is not observed (AW-7, O-8, U-E26).";
/// RC-9 run actions at the definition pin; agent messages, reasoning and plans are conversation.
const RUN_ACTIONS: [&str; 7] = ["mcpToolCall", "dynamicToolCall", "commandExecution", "fileChange", "collabAgentToolCall", "webSearch", "imageGeneration"];

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
#[derive(Clone, Debug)]
enum Trigger {
    /// AW-6: the output's designating line.
    Message { output: String, line: String },
    /// AW-7: the output's project-relative path.
    File { output: String, path: String },
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
/// are read from the run's entries.
#[derive(Clone, Debug, Default)]
pub(crate) struct CheckpointRecorder {
    listed: Vec<Listed>,
    arrivals: Vec<Arrival>,
    seen_completions: BTreeSet<String>,
    seen_starts: BTreeSet<String>,
    limit: Option<String>,
}

/// One recorder output: the RS entry kind and its CE body.
pub(crate) type Output = (&'static str, Value);

/// Where the run is, as the recorder needs it.
pub(crate) struct RunScope<'a> {
    pub home: &'a str,
    pub conversation: &'a str,
    pub start: crate::run_offers::RunStart,
    pub project_root: &'a std::path::Path,
}

impl CheckpointRecorder {
    /// A-2 / CE-1: the checkpoints of the resolved declaration (RP-5). Only
    /// recognized checkpoints are listed; an invalid or not-established one
    /// creates no arrival (§4.14) and is shown with its finding by the run
    /// panel, not written here (CE-2 is not implemented).
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
        let mut recorder = Self::default();
        let mut written = Vec::new();
        for element in declaration.elements.get("checkpoints").into_iter().flatten().filter(|e| e.reading == Reading::Recognized) {
            let v = &element.value;
            let (Some(name), Some(act), Some(subject)) = (v["name"].as_str(), v["required_act"].as_str(), v["subject"]["class"].as_str().and_then(subject_class)) else { continue };
            let rw = &v["reached_when"];
            let kind = rw["kind"].as_str().unwrap_or_default();
            let (trigger, status, reason) = match kind {
                "output_produced" => match rw["output"].as_str().and_then(|n| output(n).map(|o| (n, o))) {
                    Some((n, o)) if o["form"] == "message" && o["designating_line"].is_string() => (
                        Trigger::Message { output: n.into(), line: o["designating_line"].as_str().unwrap().into() },
                        "evaluable with limit",
                        format!("AW-6: a completed agent message whose first non-empty line is exactly \"{}\". {MESSAGE_LIMIT}", o["designating_line"].as_str().unwrap()),
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
                "before_dispatch" => (Trigger::None, "not evaluable", "Tool-call arrivals (AW-1…AW-4) are not evaluated by this App yet. No arrival will be recorded.".into()),
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
            "arrivals":self.arrivals.len(),"limit":self.limit,
            "standing":"Recorded only from native items this App observed live; recording sends, asks or pauses nothing (RC-4). Acts are not counted yet (CE-5/CE-6)."})
    }

    /// Reads the run's native rows once each, in receipt order, and returns
    /// the entries to write (CE-3 with CE-18, CE-11, CE-12). `entries` is the
    /// run's record so far, which decides each arrival's disposition.
    pub(crate) fn observe(&mut self, view: &Value, scope: &RunScope, entries: &[Value]) -> Vec<Output> {
        if view["home"] != scope.home || self.listed.is_empty() {
            return vec![];
        }
        let session = view["generation"]["appSession"].clone();
        enum Event<'a> {
            Completed(&'a Value),
            Started(&'a Value),
        }
        let mut events: Vec<((u64, u64), String, Event)> = Vec::new();
        for row in view["items"].as_array().into_iter().flatten() {
            if row["threadId"] != scope.conversation || row["standing"] != "live-observed" || row["receipt"]["generation"]["appSession"] != session {
                continue;
            }
            let (Some(turn), Some(item), Some(spawn)) = (row["turnId"].as_str(), row["native"]["id"].as_str(), row["receipt"]["generation"]["spawnCounter"].as_u64()) else { continue };
            let in_run = crate::run_offers::turn_order(view, scope.conversation, turn).is_some_and(|order| scope.start.includes(order));
            if !in_run {
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
        events.sort_by(|a, b| a.0.cmp(&b.0));
        let mut written: Vec<Output> = Vec::new();
        for (at, key, event) in events {
            match event {
                Event::Completed(row) => {
                    self.seen_completions.insert(key);
                    for (index, referents, limit) in self.matches(row, scope) {
                        let listed = self.listed[index].clone();
                        let ordinal = 1 + self.arrivals.iter().filter(|a| a.checkpoint == listed.name).count() as u64;
                        let completed = row["sourceFrame"]["params"]["completedAtMs"].as_i64();
                        let time = match completed {
                            Some(ms) => json!({"value":crate::util::rfc3339_from_ms(ms),"source":"supplier_item_time"}),
                            None => json!({"value":crate::util::now_rfc3339(),"source":"app_observation_time"}),
                        };
                        let arrival = Arrival { checkpoint: listed.name.clone(), ordinal, act: listed.act.clone(), at, continued: false, resumed: false };
                        written.push(("checkpoint_arrival", json!({"checkpoint":listed.name,"requiredAct":listed.act,"subjectClass":listed.subject,
                            "governed":listed.governed,"arrivalOrdinal":ordinal,
                            "event":{"source":"native_item","ref":item_ref(row, scope.conversation),"evidencedTime":time},
                            "referents":referents,"purpose":listed.purpose,"scope":listed.scope,
                            "limits":[limit,NO_ACT_COUNTING],"requestObservation":{"state":"not yet observed"}})));
                        written.push(("disposition_change", json!({"arrival":arrival.reference(),"disposition":"waiting","annotations":[]})));
                        self.arrivals.push(arrival);
                    }
                }
                Event::Started(row) => {
                    self.seen_starts.insert(key);
                    if !run_action(row) {
                        continue;
                    }
                    let reference = item_ref(row, scope.conversation);
                    // The start time is still in hand only while the start frame is the row's latest.
                    let time = row["sourceFrame"]["params"]["startedAtMs"].as_i64().filter(|_| row["sourceFrame"]["method"] == "item/started")
                        .map(crate::util::rfc3339_from_ms).unwrap_or_else(crate::util::now_rfc3339);
                    for arrival in self.arrivals.iter_mut().filter(|a| a.at < at) {
                        match disposition(entries, &written, &arrival.reference()).as_deref() {
                            Some("waiting") if !arrival.continued => {
                                arrival.continued = true;
                                written.push(("continued_past", json!({"arrival":arrival.reference(),"actionRef":reference,"actKind":arrival.act})));
                            }
                            Some("performed") if !arrival.resumed => {
                                arrival.resumed = true;
                                written.push(("run_resumed", json!({"arrival":arrival.reference(),"firstActionRef":reference,"time":time})));
                            }
                            _ => {}
                        }
                    }
                }
            }
        }
        written
    }

    /// Which listed checkpoints a completed row meets, each with its bound
    /// referents and its arrival limit. Anything else meets none.
    fn matches(&self, row: &Value, scope: &RunScope) -> Vec<(usize, Vec<Value>, &'static str)> {
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
                    found.push((index, referents(listed, output, &format!("agentMessage {}", native["id"].as_str().unwrap_or_default()), content), MESSAGE_LIMIT));
                }
                Trigger::File { output, path } if native["type"] == "fileChange" && native["status"] == "completed" => {
                    let paths: Vec<&str> = native["changes"].as_array().into_iter().flatten()
                        .flat_map(|c| [c["path"].as_str(), c["kind"]["move_path"].as_str()]).flatten().collect();
                    if !paths.iter().any(|p| same_path(p, path, scope.project_root)) {
                        continue;
                    }
                    let content = json!({"notObtainable":true,"reason":"file content identity not read: this arrival is recorded from the native fileChange item only, and a later read could show later content (AW-7)"});
                    found.push((index, referents(listed, output, path, content), FILE_LIMIT));
                }
                _ => {}
            }
        }
        found
    }
}

/// The first non-empty line of a message, trimmed (WD OP-1).
fn first_line(text: &str) -> Option<&str> {
    text.lines().map(str::trim).find(|l| !l.is_empty())
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
/// CE-17 `waitingArrivals` from RS entries (`kind`, `body`) of one run, in
/// arrival order: every arrival whose latest disposition is *waiting*.
pub(crate) fn waiting_arrivals(entries: &[Value]) -> Vec<Value> {
    entries.iter().filter(|e| e["kind"] == "checkpoint_arrival")
        .map(|e| json!({"checkpoint":e["body"]["checkpoint"],"arrivalOrdinal":e["body"]["arrivalOrdinal"]}))
        .filter(|arrival| disposition(entries, &[], arrival).as_deref() == Some("waiting"))
        .collect()
}

#[cfg(test)]
#[path = "checkpoint_recorder_tests.rs"]
pub(crate) mod tests;
