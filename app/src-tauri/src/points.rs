//! DEL-02-03 REQ-008: a point placed in conversation (PRD V4-AUT-07, V4-AUT-08).
//!
//! When the person asks the agent to place a point, the agent reports it
//! through one App-offered dynamic tool, [`TOOL`]. The host admits the call,
//! checks its arguments against [`input_schema`], and records the placement:
//!
//! 1. one `point_placed` entry in the App's records store, in the part of the
//!    store that belongs to the conversation's project, through DEL-04-03's
//!    writer ([`crate::records::append_project`], log [`WRITER`]). It keeps the
//!    validated arguments as admitted (supplied text, never authority), their
//!    digest, the call's source binding, the run reading and the placer facts
//!    the App observed;
//! 2. then one pointer tag on the conversation in the App ledger (DEL-01-02,
//!    owner [`TAG_OWNER`]): the point reference, the record identity, the
//!    source binding, the run reading, the observed placer facts and the
//!    digest. No supplied text goes into the ledger;
//! 3. then the receipt.
//!
//! A point is shown only where a pointer tag and its record join (see
//! [`join`]). A record can exist with no pointer: the App quit or the ledger
//! refused between steps 1 and 2. Such a record is never shown as a point;
//! a reader of the store sees an ordinary `point_placed` entry. The host
//! completes its pointer from the record's own binding the next time it reads
//! that conversation's records (before a later placement there, and when the
//! conversation is resumed), and a placement is one per call: the record is
//! found again by its call identity and never written twice.
//!
//! Nothing here reads the supplier's history, holds a run, answers any other
//! supplier request, or performs or offers an act. The App never makes this
//! call itself: `item/tool/call` is a request Codex raises for the model's own
//! tool call, and the App only receives and answers it.
use serde_json::{json, Value};

/// The tool's name as Codex offers it to the model.
pub const TOOL: &str = "chirality_point_v1";
/// The named App rule that answers it in the request register.
pub(crate) const RULE: &str = "app-rule:point-record";
/// The REC tag owner of the conversation's pointers (DEL-01-02 tags).
pub(crate) const TAG_OWNER: &str = "DEL-02-03/point";
/// The RS entry kind (DEL-04-03 RS_RECORD.schema.json `pointPlaced`).
pub(crate) const KIND: &str = "point_placed";
/// The writer whose log in the project's store subtree holds the points
/// (`acts/<key(WRITER)>.jsonl`, a log outside any run).
pub(crate) const WRITER: &str = "app-writer:points";
/// The record body's own version.
pub(crate) const VERSION: u64 = 1;
/// The App's own limit on one placement's arguments (bytes of their canonical JSON).
pub const ARGUMENT_LIMIT: usize = 16 * 1024;
/// The App's own limit on the points one conversation holds.
pub const POINTS_PER_CONVERSATION: usize = 100;
/// The digest method: SHA-256 (lowercase hex) of the arguments in the App's
/// canonical JSON (`crate::canonical`: keys in code-point order, no whitespace).
pub(crate) const DIGEST_METHOD: &str = "chirality.app.point-arguments.sha256/v1";

/// The tool as offered, version 1: its name, its description (the only
/// guidance the agent gets for it) and its closed argument schema. Kept as a
/// file so that the recorded-replay double (supplier_checks/recorded_replay.py)
/// declares the same bytes as the App's alternative on a start.
const DEFINITION: &str = include_str!("point_tool_v1.json");

/// The `dynamicTools` entry offered on `thread/start` (FunctionDynamicToolSpec).
pub fn definition() -> Value {
    serde_json::from_str(DEFINITION).expect("point_tool_v1.json is JSON")
}
/// SHA-256 of the definition as offered, for the offer pointer.
pub(crate) fn definition_digest() -> String {
    crate::util::sha256_hex(&serde_json::to_vec(&definition()).expect("definition serializes"))
}
/// Version 1's closed argument schema. The record body's `arguments` carries
/// the same schema (RS_RECORD.schema.json `$defs/pointArguments`).
pub(crate) fn input_schema() -> Value {
    definition()["inputSchema"].clone()
}
fn validator() -> Result<&'static jsonschema::Validator, String> {
    static VALIDATOR: std::sync::OnceLock<Result<jsonschema::Validator, String>> = std::sync::OnceLock::new();
    VALIDATOR
        .get_or_init(|| jsonschema::options().offline().build(&input_schema()).map_err(|e| e.to_string()))
        .as_ref()
        .map_err(Clone::clone)
}
/// The arguments' canonical bytes, within the App's own limit.
fn canonical(arguments: &Value) -> Result<String, String> {
    let mut out = String::new();
    crate::canonical::canonical(arguments, &mut out).map_err(|_| "the arguments hold a number the App does not record".to_owned())?;
    Ok(out)
}
/// Checks `arguments` against version 1. The error is the App's sentence.
pub(crate) fn validate(arguments: &Value) -> Result<(), String> {
    let bytes = canonical(arguments).map_err(|e| format!("The arguments are not valid for {TOOL} version 1 ({e}); no point was recorded."))?;
    if bytes.len() > ARGUMENT_LIMIT {
        return Err(format!("The arguments are larger than the App's own limit of {ARGUMENT_LIMIT} bytes for one point; no point was recorded."));
    }
    let validator = validator().map_err(|e| format!("The App could not check the arguments ({e}); no point was recorded."))?;
    if let Some(error) = validator.iter_errors(arguments).next() {
        return Err(format!("The arguments are not valid for {TOOL} version 1 ({} at {}); no point was recorded.", error.masked(), error.instance_path()));
    }
    Ok(())
}
/// The digest of the arguments under [`DIGEST_METHOD`].
pub(crate) fn digest(arguments: &Value) -> Result<String, String> {
    Ok(crate::util::sha256_hex(canonical(arguments)?.as_bytes()))
}

/// The call identity a placement is bound to: the home and full generation,
/// the conversation, the turn, the call and the request identity.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct Source {
    pub home: String,
    pub home_class: String,
    pub generation: String,
    pub thread: String,
    pub turn: String,
    pub call: String,
    pub request: Value,
}
impl Source {
    pub fn value(&self) -> Value {
        json!({"home":self.home,"homeClass":self.home_class,"generation":self.generation,"thread":self.thread,"turn":self.turn,"call":self.call,"request":self.request})
    }
    fn matches(&self, v: &Value) -> bool {
        *v == self.value()
    }
}

/// The record body of one placement (RS `pointPlaced`).
#[allow(clippy::too_many_arguments)]
pub(crate) fn record_body(point: &str, source: &Source, project: &str, run: &Value, placer: &Value, arguments: &Value, digest: &str, at: &str) -> Value {
    json!({"version":VERSION,"point":point,"source":source.value(),"project":project,"run":run,"placer":placer,
        "arguments":arguments,"argumentsDigest":{"method":DIGEST_METHOD,"value":digest},"recordedAt":at})
}
/// The pointer tag value for a written record: everything but the supplied text.
pub(crate) fn pointer(entry: &Value) -> Result<String, String> {
    let b = &entry["body"];
    let value = json!({"v":1,"kind":"placed","point":b["point"],"record":entry["recordId"],"source":b["source"],"project":b["project"],
        "run":b["run"],"placer":b["placer"],"digest":b["argumentsDigest"]});
    let mut out = String::new();
    crate::canonical::canonical(&value, &mut out)?;
    Ok(out)
}
/// The offer pointer written when a conversation the App started with the
/// tool is first indexed under a project.
pub(crate) fn offer_pointer(home: &str, generation: &str, thread: &str) -> String {
    let mut out = String::new();
    crate::canonical::canonical(&json!({"v":1,"kind":"offered","home":home,"generation":generation,"thread":thread,"definition":definition_digest()}), &mut out)
        .expect("offer pointer is canonical");
    out
}
/// A tag value of this owner, decoded; anything else is not a pointer.
pub(crate) fn decode(raw: &str) -> Option<Value> {
    let v: Value = serde_json::from_str(raw).ok()?;
    (v["v"] == 1 && matches!(v["kind"].as_str(), Some("placed" | "offered"))).then_some(v)
}

/// The persistence sentences of a receipt (closed, the App's own words).
pub(crate) const KEPT: &str = "The point and its terms are kept in the App's records for this conversation's project, and the conversation's pointer to them is saved.";
pub(crate) fn pointer_pending(reason: &str) -> String {
    format!("The point and its terms are kept in the App's records for this conversation's project, but the conversation's pointer to them could not be saved ({reason}); the App completes it when it next can.")
}
const STANDING: &str = "Recording a point holds nothing, tells no one, waits for no answer and performs no act. A pause it asks for is your cooperation.";
/// The receipt: recorded (with the reference and persistence) or not
/// recorded (with the reason). It contains no human answer.
pub(crate) fn receipt(point: Option<&str>, reason: Option<&str>, persistence: Option<&str>, run: &Value) -> Value {
    let recorded = point.is_some();
    let text = json!({"receipt":"chirality.point.receipt/1","state":if recorded {"recorded"} else {"not recorded"},
        "point":point,"reason":reason,"persistence":persistence,"run":run,"standing":STANDING}).to_string();
    json!({"contentItems":[{"type":"inputText","text":text}],"success":recorded})
}

/// One `point_placed` entry read from the points log, with its line.
#[derive(Clone, Debug)]
pub(crate) struct Line {
    pub no: usize,
    pub entry: Value,
}
/// The points log as the store's reader reads it: its point entries, and the
/// first line at which the log stops being whole (with the reason).
#[derive(Clone, Debug, Default)]
pub(crate) struct LogReading {
    pub entries: Vec<Line>,
    pub first_limit: Option<(usize, String)>,
}
impl LogReading {
    /// R-2 as the records capability reads a log (`records_access::ProjectPaths`):
    /// `records_index::open_log`, then `record_lines::parse`, line by line.
    pub(crate) fn read(path: &std::path::Path) -> Result<Self, String> {
        use std::io::Read;
        let mut bytes = Vec::new();
        match crate::records_index::open_log(path) {
            Ok(mut file) => { file.read_to_end(&mut bytes).map_err(|e| format!("the App's points log could not be read ({e})"))?; }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(Self::default()),
            Err(e) => return Err(format!("the App's points log could not be read ({e})")),
        }
        let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        let parsed = crate::record_lines::parse(&bytes, &name, 0, 0, 1, Default::default());
        let mut read = Self::default();
        let note = |no: usize, why: String, read: &mut Self| { if read.first_limit.is_none() { read.first_limit = Some((no, why)); } };
        for line in parsed.lines {
            if let Some(broken) = &line.broken { note(line.no, broken.clone(), &mut read); }
            if line.entries.is_empty() { note(line.no, format!("line {} of the points log is not a readable record", line.no), &mut read); }
            else if let Some(first) = line.limits.first() { note(line.no, first.clone(), &mut read); }
            for entry in line.entries.into_iter().filter(|e| e["kind"] == KIND) {
                read.entries.push(Line { no: line.no, entry });
            }
        }
        if parsed.chain.unchained > 0 { note(1, format!("{} line(s) of the points log carry no chain link", parsed.chain.unchained), &mut read); }
        if let Some(removed) = crate::record_lines::links_removed(path, &name, &parsed.chain) { note(1, removed, &mut read); }
        // A torn tail follows every complete line: it limits nothing before it.
        Ok(read)
    }
    /// The records bound to one call identity.
    pub(crate) fn for_call(&self, source: &Source) -> Vec<&Line> {
        self.entries.iter().filter(|l| source.matches(&l.entry["body"]["source"])).collect()
    }
}

/// What the App knows of the conversation a pointer is joined for.
pub(crate) struct Conversation<'a> {
    pub home: &'a str,
    pub home_class: &'a str,
    pub thread: &'a str,
    pub project: &'a str,
}
fn not_read(reason: impl Into<String>) -> Value {
    json!({"state":"not read","reason":reason.into()})
}
/// One pointer joined to its record. The terms are shown only from a record
/// that joins whole: one entry with the pointer's reference and identity, of
/// this conversation and project, read whole up to its line, whose arguments
/// are valid for version 1 and whose recomputed digest equals the record's
/// and the pointer's. Otherwise the point stays recorded, terms not read.
pub(crate) fn join(pointer: &Value, log: &Result<LogReading, String>, conversation: &Conversation) -> Value {
    let mut view = json!({"point":pointer["point"],"turn":pointer["source"]["turn"],"call":pointer["source"]["call"],
        "run":pointer["run"],"placer":pointer["placer"],"recordedAt":null});
    let terms = (|| {
        let src = &pointer["source"];
        if src["home"] != conversation.home || src["homeClass"] != conversation.home_class || src["thread"] != conversation.thread || pointer["project"] != conversation.project {
            return not_read("the pointer does not belong to this conversation and project");
        }
        let log = match log {
            Ok(log) => log,
            Err(e) => return not_read(format!("the App's records for this conversation's project could not be read: {e}")),
        };
        let same: Vec<&Line> = log.entries.iter().filter(|l| l.entry["body"]["point"] == pointer["point"]).collect();
        let line = match same.as_slice() {
            [] => return not_read("no record with this point's reference was found in the App's records"),
            [one] => *one,
            _ => return not_read("the App's records hold this point's reference more than once"),
        };
        if let Some((no, why)) = &log.first_limit {
            if *no <= line.no {
                return not_read(format!("the points log is not whole at or before this point's record: {why}"));
            }
        }
        let body = &line.entry["body"];
        if line.entry["recordId"] != pointer["record"] || body["source"] != *src || body["project"] != pointer["project"] {
            return not_read("the record found does not belong to this pointer");
        }
        if validate(&body["arguments"]).is_err() {
            return not_read("the recorded terms are not valid for version 1 of the point tool");
        }
        let recomputed = digest(&body["arguments"]).unwrap_or_default();
        if body["argumentsDigest"] != json!({"method":DIGEST_METHOD,"value":recomputed}) || pointer["digest"] != body["argumentsDigest"] {
            return not_read("the recorded terms do not match the digest kept with the pointer");
        }
        json!({"state":"read","arguments":body["arguments"]})
    })();
    if terms["state"] == "read" {
        if let Ok(log) = log {
            if let Some(line) = log.entries.iter().find(|l| l.entry["body"]["point"] == pointer["point"]) {
                view["recordedAt"] = line.entry["body"]["recordedAt"].clone();
            }
        }
    }
    view["terms"] = terms;
    view
}

#[cfg(test)]
#[path = "points_tests.rs"]
mod tests;
