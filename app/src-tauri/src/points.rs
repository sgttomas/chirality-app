//! DEL-02-03 REQ-008: a point placed in conversation (PRD V4-AUT-07, V4-AUT-08).
//!
//! When the person asks the agent to place a point, the agent reports it
//! through one App-offered dynamic tool, [`TOOL`]. The host admits the call,
//! checks its arguments against [`input_schema`], and records the placement,
//! one placement at a time:
//!
//! 1. one `point_placed` entry in the App's records store, in the part of the
//!    store that belongs to the conversation's project, through DEL-04-03's
//!    writer ([`crate::records::append_reserved`] on the project's points log,
//!    [`WRITER`], bound through the store's own binding). It keeps the
//!    validated arguments as admitted (supplied text, never authority), their
//!    digest, the call's identity, the store's project identity, and the run
//!    reading and what the App observed of the call, both in closed App forms;
//! 2. then one pointer tag on the conversation in the App ledger (DEL-01-02,
//!    owner [`TAG_OWNER`]): identities and the digest only (see [`pointer`]).
//!    No supplied text and no prose goes into the ledger;
//! 3. then the receipt: recorded, not recorded, or not established (the App
//!    could not establish whether the record was written).
//!
//! A point is shown only where a pointer tag and its record join, and the
//! record is sound ([`LogReading::soundness`]): one check used for
//! reconciliation, for the lookup of a call, and for display. A record can
//! exist with no pointer: the App quit or the ledger refused between steps 1
//! and 2. Such a record is never shown as a point; a reader of the store sees
//! an ordinary `point_placed` entry. The host completes its pointer from the
//! record's own call identity on two occasions only: before a later placement
//! in that conversation, and when the conversation is resumed.
//!
//! Nothing here reads the supplier's history, holds a run, answers any other
//! supplier request, or performs or offers an act. The App never makes this
//! call itself: `item/tool/call` is a request Codex raises for the model's own
//! tool call, and the App only receives and answers it.
use serde_json::{json, Value};
use std::collections::HashMap;

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
/// The App's own limit on the refused calls of one conversation it keeps for
/// the view in one App session.
pub const REFUSALS_KEPT: usize = 20;
/// The digest method: SHA-256 (lowercase hex) of the arguments in the App's
/// canonical JSON (`crate::canonical`: keys in code-point order, no whitespace).
pub(crate) const DIGEST_METHOD: &str = "chirality.app.point-arguments.sha256/v1";
/// The RS format and the major and minor version this reader knows (DEL-04-03 REQ-012).
const FORMAT: &str = "chirality.rs.record";
const KNOWN_MINOR: u64 = 1;
/// The acts a sign-off point names (PRD V4-AUT-07).
pub(crate) const SIGN_OFF_ACTS: [&str; 2] = ["engineering approval", "professional reliance"];

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
/// The canonical bytes of a value (keys in code-point order, integers only).
fn canonical(value: &Value) -> Result<String, String> {
    let mut out = String::new();
    crate::canonical::canonical(value, &mut out).map_err(|_| "the arguments hold a number the App does not record".to_owned())?;
    Ok(out)
}
/// The App's sentence for a sign-off point that names neither of its acts.
pub(crate) const SIGN_OFF_UNNAMED: &str = "A sign-off point names its act, engineering approval or professional reliance (PRD V4-AUT-07); these arguments name neither, so no point was recorded.";
/// Checks `arguments` against version 1. The error is the App's sentence.
pub(crate) fn validate(arguments: &Value) -> Result<(), String> {
    let bytes = canonical(arguments).map_err(|e| format!("The arguments are not valid for {TOOL} version 1 ({e}); no point was recorded."))?;
    if bytes.len() > ARGUMENT_LIMIT {
        return Err(format!("The arguments are larger than the App's own limit of {ARGUMENT_LIMIT} bytes for one point; no point was recorded."));
    }
    if arguments["kind"] == "sign-off" && !arguments["reservedAct"].as_str().is_some_and(|act| SIGN_OFF_ACTS.contains(&act)) {
        return Err(SIGN_OFF_UNNAMED.into());
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
}
/// The key a source is indexed by: its canonical bytes.
fn source_key(source: &Value) -> String {
    canonical(source).unwrap_or_else(|_| source.to_string())
}

/// The run reading at the call, in the App's closed form.
pub(crate) fn run_in(run: &str) -> Value { json!({"state":"in run","run":run}) }
pub(crate) fn run_none() -> Value { json!({"state":"no run"}) }
/// Its codes: `start-sent-not-yet-open` (a run's start sent in this
/// conversation, not yet seen open); `codex-restarted-run-unknown` (this App
/// session's Codex was restarted while a run of this conversation was open or
/// starting, and the App has not seen it since); `resumed-earlier-run-unknown`
/// (the conversation began in an earlier App session, whose runs the App
/// cannot tell).
pub(crate) fn run_not_established(code: &'static str) -> Value { json!({"state":"not established","reason":code}) }
/// What the App observed of the call, in its closed form.
pub(crate) fn observed(person_press: Option<&str>, app_started: bool) -> Value {
    match person_press {
        Some(reference) => json!({"caller":"agent-through-point-tool","turnStart":"person-press","requestRef":reference,"delegation":"not-established"}),
        None if app_started => json!({"caller":"agent-through-point-tool","turnStart":"app-not-person","delegation":"not-established"}),
        None => json!({"caller":"agent-through-point-tool","turnStart":"not-observed","delegation":"not-established"}),
    }
}

/// The record body of one placement (RS `pointPlaced`).
#[allow(clippy::too_many_arguments)]
pub(crate) fn record_body(point: &str, source: &Source, project: &str, store_project: &str, run: &Value, observed: &Value, arguments: &Value, digest: &str, at: &str) -> Value {
    json!({"version":VERSION,"point":point,"source":source.value(),"project":project,"storeProject":store_project,"run":run,"observed":observed,
        "arguments":arguments,"argumentsDigest":{"method":DIGEST_METHOD,"value":digest},"recordedAt":at})
}
/// The pointer tag value for a written record: identities and the digest
/// only: the point, the record identity, the call's identities, the App
/// project reference, the store's project identity and the digest. The run
/// and what the App observed are read from the verified record, never from
/// the pointer.
pub(crate) fn pointer(entry: &Value) -> Result<String, String> {
    let b = &entry["body"];
    let value = json!({"v":1,"kind":"placed","point":b["point"],"record":entry["recordId"],"source":b["source"],"project":b["project"],
        "storeProject":b["storeProject"],"digest":b["argumentsDigest"]});
    if decode(&value.to_string()).is_none() {
        return Err("the record's identities do not make a pointer".into());
    }
    canonical(&value)
}
/// The offer pointer written when a conversation the App started with the
/// tool is first indexed under a project.
pub(crate) fn offer_pointer(home: &str, generation: &str, thread: &str) -> String {
    canonical(&json!({"v":1,"kind":"offered","home":home,"generation":generation,"thread":thread,"definition":definition_digest()}))
        .expect("offer pointer is canonical")
}
/// The offer pointer that also carries the conversation's records binding:
/// the App project and the store's stable project identity, written before
/// the conversation's first record is appended in that store project.
pub(crate) fn bound_offer_pointer(home: &str, generation: &str, thread: &str, project: &str, store_project: &str) -> String {
    canonical(&json!({"v":1,"kind":"offered","home":home,"generation":generation,"thread":thread,"definition":definition_digest(),"project":project,"storeProject":store_project}))
        .expect("offer pointer is canonical")
}
/// The App's home classes a conversation is indexed under (DEL-01-02).
const HOME_CLASSES: [&str; 3] = ["H-acct", "H-key", "H-omlx"];
/// A full generation reference in its canonical form, of the Codex home `home`.
fn generation_of(reference: &Value, home: &Value) -> bool {
    let Some(reference) = reference.as_str() else { return false };
    crate::recovery::generation_from_ref(reference).ok()
        .is_some_and(|g| crate::recovery::generation_ref(&g).ok().as_deref() == Some(reference) && g["home"] == *home)
}
/// An App identity of the form `<prefix><lowercase hyphenated UUID>`.
fn app_id(value: &Value, prefix: &str) -> bool {
    value.as_str().and_then(|v| v.strip_prefix(prefix)).and_then(|u| uuid::Uuid::parse_str(u).ok().map(|id| id.hyphenated().to_string() == u)).unwrap_or(false)
}
/// A SHA-256 value object of the App's digest method: exactly its two keys,
/// the value 64 lowercase hexadecimal digits.
fn digest_object(v: &Value) -> bool {
    v.as_object().is_some_and(|o| o.len() == 2) && v["method"] == DIGEST_METHOD
        && v["value"].as_str().is_some_and(|d| d.len() == 64 && d.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)))
}
/// A tag value of this owner, decoded and checked whole: its exact keys, the
/// canonical generation and its Codex home, the App's identities and the
/// exact digest object. Anything else is not a pointer (it is reported as a
/// tag that could not be read, never ignored).
pub(crate) fn decode(raw: &str) -> Option<Value> {
    let v: Value = serde_json::from_str(raw).ok()?;
    let keys = |of: &Value, names: &[&str]| of.as_object().is_some_and(|o| o.len() == names.len() && names.iter().all(|n| o.contains_key(*n)));
    let text = |x: &Value| x.as_str().is_some_and(|s| !s.is_empty());
    let ok = match (v["v"].as_u64(), v["kind"].as_str()) {
        (Some(1), Some("placed")) => {
            let s = &v["source"];
            keys(&v, &["v", "kind", "point", "record", "source", "project", "storeProject", "digest"])
                && app_id(&v["point"], "pt-") && app_id(&v["record"], "rec:app:") && text(&v["project"]) && text(&v["storeProject"])
                && keys(s, &["home", "homeClass", "generation", "thread", "turn", "call", "request"])
                && text(&s["home"]) && s["homeClass"].as_str().is_some_and(|h| HOME_CLASSES.contains(&h)) && generation_of(&s["generation"], &s["home"])
                && ["thread", "turn", "call"].iter().all(|k| text(&s[*k])) && (s["request"].is_string() || s["request"].is_i64() || s["request"].is_u64())
                && digest_object(&v["digest"])
        }
        (Some(1), Some("offered")) => {
            let bound = v.get("storeProject").is_some();
            (if bound { keys(&v, &["v", "kind", "home", "generation", "thread", "definition", "project", "storeProject"]) && text(&v["project"]) && text(&v["storeProject"]) }
             else { keys(&v, &["v", "kind", "home", "generation", "thread", "definition"]) })
                && text(&v["home"]) && text(&v["thread"]) && generation_of(&v["generation"], &v["home"])
                && v["definition"].as_str().is_some_and(|d| d.len() == 64 && d.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)))
        }
        _ => false,
    };
    ok.then_some(v)
}

/// Whether a received frame is framed as a point call: a request (id and
/// method, no result or error, nothing else; a protocol version, where
/// given, of JSON-RPC 2.0), the tool's exact name, the
/// call's conversation, turn and call identities present and its arguments.
/// The namespace is checked by the caller.
pub(crate) fn frame_ok(frame: &Value) -> bool {
    let Some(o) = frame.as_object() else { return false };
    let text = |v: Option<&Value>| v.and_then(Value::as_str).is_some_and(|s| !s.is_empty());
    o.keys().all(|k| matches!(k.as_str(), "jsonrpc" | "id" | "method" | "params"))
        && o.get("jsonrpc").is_none_or(|v| v == "2.0")
        && frame["method"] == "item/tool/call"
        && (frame["id"].is_string() || frame["id"].is_i64() || frame["id"].is_u64())
        && frame["params"].as_object().is_some_and(|p| p.get("tool") == Some(&json!(TOOL))
            && text(p.get("threadId")) && text(p.get("turnId")) && text(p.get("callId")) && p.contains_key("arguments"))
}

/// The persistence sentences of a receipt (closed, the App's own words).
pub(crate) const KEPT: &str = "The point and its terms are kept in the App's records for this conversation's project, and the conversation's pointer to them is saved.";
pub(crate) fn pointer_pending(reason: &str) -> String {
    format!("The point and its terms are kept in the App's records for this conversation's project, but the conversation's pointer to them could not be saved ({reason}); the App completes it before a later placement in this conversation or when the conversation is resumed.")
}
pub(crate) fn not_established(reason: &str) -> String {
    format!("The App could not establish whether the point was recorded ({reason}). It does not place it again; it reads this conversation's records again before it shows their points.")
}
const STANDING: &str = "Recording a point holds nothing, tells no one, waits for no answer and performs no act. A pause it asks for is your cooperation.";
/// What one call came to.
pub(crate) enum Outcome {
    Recorded { point: String, persistence: String, run: Value },
    NotRecorded { reason: String },
    NotEstablished { point: Option<String>, reason: String },
}
/// The receipt: recorded (with the reference and persistence), not recorded
/// (with the reason), or not established (with the reference reserved for it
/// and the reason). It contains no human answer.
pub(crate) fn receipt(outcome: &Outcome, admitted_run: &Value) -> Value {
    let (state, point, reason, persistence, run) = match outcome {
        Outcome::Recorded { point, persistence, run } => ("recorded", Some(point.as_str()), None, Some(persistence.as_str()), run),
        Outcome::NotRecorded { reason } => ("not recorded", None, Some(reason.as_str()), None, admitted_run),
        Outcome::NotEstablished { point, reason } => ("not established", point.as_deref(), Some(reason.as_str()), None, admitted_run),
    };
    let text = json!({"receipt":"chirality.point.receipt/1","state":state,"point":point,"reason":reason,"persistence":persistence,"run":run,"standing":STANDING}).to_string();
    json!({"contentItems":[{"type":"inputText","text":text}],"success":state == "recorded"})
}

/// One `point_placed` entry read from the points log, with its line and
/// whether it is of a newer minor format version than this App knows.
#[derive(Clone, Debug)]
pub(crate) struct Line {
    pub no: usize,
    /// The byte offset at which its line begins in the log.
    pub start: usize,
    pub entry: Value,
    pub newer: Option<String>,
    sound: Result<(), String>,
}
/// What follows the last complete line of the log.
#[derive(Clone, Debug, Default, PartialEq)]
pub(crate) enum Tail {
    #[default]
    None,
    /// A whole point entry whose newline is missing: the writer terminates it
    /// at its next append, and it then reads as a record.
    Entry(Value),
    /// Bytes that are no whole entry: the writer sets them aside (W-0).
    Fragment,
}
/// The points log as the store's reader reads it (R-2, as
/// `records_access::ProjectPaths` reads a log): its point entries with the
/// soundness of each, the lines at which it stops being whole, the entries it
/// refused for their version, the torn fragments the writer set aside (notes,
/// not limits), and its unterminated tail.
#[derive(Clone, Debug, Default)]
pub(crate) struct LogReading {
    pub lines: Vec<Line>,
    pub limits: Vec<(usize, String)>,
    pub refused: Vec<(usize, String)>,
    pub set_aside: usize,
    pub tail: Tail,
    pub missing: bool,
    by_point: HashMap<String, Vec<usize>>,
    by_record: HashMap<String, Vec<usize>>,
    by_source: HashMap<String, Vec<usize>>,
    by_thread: HashMap<String, Vec<usize>>,
}
/// How the reader takes an entry's format and version (DEL-04-03 REQ-012):
/// known, a newer minor version (read as far as known), or refused.
fn version_of(entry: &Value) -> Result<Option<String>, String> {
    let version = entry["formatVersion"].as_str().unwrap_or_default();
    if entry["format"] != FORMAT {
        return Err(format!("an entry of format {} which this App does not read", entry["format"]));
    }
    let parts: Vec<&str> = version.split('.').collect();
    match (parts.as_slice(), parts.get(1).and_then(|m| m.parse::<u64>().ok())) {
        (["0", _], Some(KNOWN_MINOR)) => Ok(None),
        (["0", _], Some(minor)) if minor > KNOWN_MINOR => Ok(Some(version.to_owned())),
        _ => Err(format!("an entry of format version {version}, which this App does not read; nothing is inferred from it")),
    }
}
impl LogReading {
    #[cfg(test)]
    pub(crate) fn read(path: &std::path::Path) -> Result<Self, String> {
        Self::read_bytes(path).map(|(read, _)| read)
    }
    fn read_bytes(path: &std::path::Path) -> Result<(Self, Vec<u8>), String> {
        use std::io::Read;
        let mut bytes = Vec::new();
        match crate::records_index::open_log(path) {
            Ok(mut file) => { file.read_to_end(&mut bytes).map_err(|e| format!("the App's points log could not be read ({e})"))?; }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok((Self { missing: true, ..Self::default() }, bytes)),
            Err(e) => return Err(format!("the App's points log could not be read ({e})")),
        }
        Ok((Self::of_bytes(path, &bytes), bytes))
    }
    /// The log as the App reads it for a project: [`Self::read`], then what
    /// the store says beyond the log itself. `imported` gives the length of
    /// the log's prefix that a verified package import brought in (its lines
    /// are another App's observations, never shown in this App's voice), and
    /// `held` how many entries anywhere in the project's records hold a
    /// record identity (the store's index): a record whose identity is held
    /// more than once in the project is not sound.
    pub(crate) fn read_bound(path: &std::path::Path, imported: impl FnOnce(&[u8]) -> Result<u64, String>, held: impl Fn(&str) -> Result<usize, String>) -> Result<Self, String> {
        let (mut read, bytes) = Self::read_bytes(path)?;
        if !read.missing { read.bind_project(imported(&bytes), held); }
        Ok(read)
    }
    fn bind_project(&mut self, imported: Result<u64, String>, held: impl Fn(&str) -> Result<usize, String>) {
        match imported {
            Err(e) => {
                self.limits.insert(0, (1, format!("which lines of the points log came from an imported package could not be established ({e})")));
                let sound: Vec<Result<(), String>> = (0..self.lines.len()).map(|i| self.check(i)).collect();
                for (line, result) in self.lines.iter_mut().zip(sound) { line.sound = result; }
            }
            Ok(prefix) => for line in self.lines.iter_mut().filter(|l| l.sound.is_ok() && (l.start as u64) < prefix) {
                line.sound = Err(IMPORTED.into());
            },
        }
        for line in self.lines.iter_mut().filter(|l| l.sound.is_ok()) {
            match held(line.entry["recordId"].as_str().unwrap_or_default()) {
                Ok(1) => {}
                Ok(_) => line.sound = Err("the App's records hold this record identity more than once in this project".into()),
                Err(e) => line.sound = Err(format!("whether this record's identity is held once in this project's records could not be established ({e})")),
            }
        }
    }
    fn of_bytes(path: &std::path::Path, bytes: &[u8]) -> Self {
        let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        let parsed = crate::record_lines::parse(bytes, &name, 0, 0, 1, Default::default());
        let starts: Vec<usize> = std::iter::once(0).chain(bytes.iter().enumerate().filter(|(_, b)| **b == b'\n').map(|(i, _)| i + 1)).collect();
        let mut read = Self::default();
        for line in parsed.lines {
            if let Some(limit) = line.broken.clone().or_else(|| line.limits.first().cloned()) {
                read.limits.push((line.no, limit));
            } else if line.entries.is_empty() && !line.notes.is_empty() {
                // A torn line the writer closed and named (W-0): set aside, not a limit.
                read.set_aside += 1;
            }
            for entry in line.entries {
                match version_of(&entry) {
                    Err(why) => read.refused.push((line.no, format!("line {} of the points log holds {why}", line.no))),
                    Ok(newer) if entry["kind"] == KIND => read.lines.push(Line { no: line.no, start: starts.get(line.no.saturating_sub(1)).copied().unwrap_or(usize::MAX), entry, newer, sound: Ok(()) }),
                    Ok(_) => {}
                }
            }
        }
        if parsed.chain.unchained > 0 { read.limits.push((1, format!("{} line(s) of the points log carry no chain link", parsed.chain.unchained))); }
        if let Some(removed) = crate::record_lines::links_removed(path, &name, &parsed.chain) { read.limits.push((1, removed)); }
        let tail = bytes.get(parsed.tail_offset as usize..).unwrap_or_default();
        if !tail.iter().all(u8::is_ascii_whitespace) {
            read.tail = match serde_json::from_slice::<Value>(tail) {
                Ok(v) if v["kind"] == KIND => Tail::Entry(v),
                _ => Tail::Fragment,
            };
        }
        for (i, line) in read.lines.iter().enumerate() {
            let b = &line.entry["body"];
            let key = |v: &Value| v.as_str().map(str::to_owned).unwrap_or_else(|| v.to_string());
            read.by_point.entry(key(&b["point"])).or_default().push(i);
            read.by_record.entry(key(&line.entry["recordId"])).or_default().push(i);
            read.by_source.entry(source_key(&b["source"])).or_default().push(i);
            read.by_thread.entry(key(&b["source"]["thread"])).or_default().push(i);
        }
        let sound: Vec<Result<(), String>> = (0..read.lines.len()).map(|i| read.check(i)).collect();
        for (line, result) in read.lines.iter_mut().zip(sound) { line.sound = result; }
        read
    }
    /// The one soundness check (reconciliation, lookup of a call, display):
    /// before any limit of the log, unique by point reference, by record
    /// identity and by call source, valid for version 1, and its digest
    /// recomputed equal to the one recorded.
    fn check(&self, i: usize) -> Result<(), String> {
        let line = &self.lines[i];
        let b = &line.entry["body"];
        if let Some((_, why)) = self.limits.iter().find(|(no, _)| *no <= line.no) {
            return Err(format!("the points log is not whole at or before this record: {why}"));
        }
        let many = |map: &HashMap<String, Vec<usize>>, key: String| map.get(&key).is_some_and(|v| v.len() > 1);
        let key = |v: &Value| v.as_str().map(str::to_owned).unwrap_or_else(|| v.to_string());
        if many(&self.by_point, key(&b["point"])) { return Err("the App's records hold this point's reference more than once".into()); }
        if many(&self.by_record, key(&line.entry["recordId"])) { return Err("the App's records hold this record identity more than once".into()); }
        if many(&self.by_source, source_key(&b["source"])) { return Err("the App's records hold more than one record for this call".into()); }
        if validate(&b["arguments"]).is_err() { return Err("the recorded terms are not valid for version 1 of the point tool".into()); }
        if digest(&b["arguments"]).ok().as_deref() != b["argumentsDigest"]["value"].as_str() || b["argumentsDigest"]["method"] != DIGEST_METHOD {
            return Err("the recorded terms do not match their recorded digest".into());
        }
        Ok(())
    }
    pub(crate) fn soundness(&self, i: usize) -> &Result<(), String> {
        &self.lines[i].sound
    }
    /// The sound records of a conversation: what the App's own limit counts.
    pub(crate) fn sound_of(&self, conversation: &Conversation) -> usize {
        self.for_thread(conversation.thread).iter().filter(|i| self.lines[**i].sound.is_ok() && conversation.names(&self.lines[**i].entry["body"])).count()
    }
    /// The lines bound to one call identity.
    pub(crate) fn for_call(&self, source: &Source) -> Vec<usize> {
        self.by_source.get(&source_key(&source.value())).cloned().unwrap_or_default()
    }
    pub(crate) fn for_point(&self, point: &str) -> Vec<usize> {
        self.by_point.get(point).cloned().unwrap_or_default()
    }
    pub(crate) fn for_thread(&self, thread: &str) -> &[usize] {
        self.by_thread.get(thread).map(Vec::as_slice).unwrap_or_default()
    }
    /// Whether the unterminated tail is the record of this call.
    pub(crate) fn tail_is(&self, source: &Source) -> bool {
        matches!(&self.tail, Tail::Entry(v) if v["body"]["source"] == source.value())
    }
    /// Whether every line was read: no limit, no refused version, no tail.
    pub(crate) fn whole(&self) -> bool {
        self.limits.is_empty() && self.refused.is_empty() && self.tail == Tail::None
    }
    /// Why the log's inventory is not established, in the App's words.
    pub(crate) fn inventory_reasons(&self) -> Vec<String> {
        let mut reasons = Vec::new();
        if let Some((no, why)) = self.limits.first() { reasons.push(format!("the points log is not whole from line {no}: {why}")); }
        if let Some((_, why)) = self.refused.first() { reasons.push(why.clone()); }
        match self.tail {
            Tail::Entry(_) => reasons.push("the points log ends with a record that is not yet terminated".into()),
            Tail::Fragment => reasons.push("the points log ends with an unfinished line".into()),
            Tail::None => {}
        }
        reasons
    }
}

/// Why a record that came from an imported package is not shown in this
/// App's voice (DEL-04-03 REQ-010: imported records are quoted evidence).
pub(crate) const IMPORTED: &str = "the record came from an imported records package, so this App did not observe its placement and does not show it as its own";

/// What the App knows of the conversation a record or pointer is read for.
pub(crate) struct Conversation<'a> {
    pub home: &'a str,
    pub home_class: &'a str,
    pub thread: &'a str,
    pub project: &'a str,
    pub store_project: &'a str,
}
impl Conversation<'_> {
    /// Whether a record body or pointer names this conversation and project.
    pub(crate) fn names(&self, v: &Value) -> bool {
        let src = &v["source"];
        src["home"] == self.home && src["homeClass"] == self.home_class && src["thread"] == self.thread
            && v["project"] == self.project && v["storeProject"] == self.store_project
    }
}
fn not_read(reason: impl Into<String>) -> Value {
    json!({"state":"not read","reason":reason.into()})
}
/// One pointer joined to its record. The terms, the run reading and what
/// the App observed are shown only from a sound record that joins: of this
/// conversation and project, with the pointer's reference, record identity,
/// call identity, store project and digest. Otherwise the point stays
/// recorded with its terms not read, and nothing of the record is shown.
pub(crate) fn join(pointer: &Value, log: &Result<std::sync::Arc<LogReading>, String>, conversation: &Conversation) -> Value {
    let mut view = json!({"point":pointer["point"],"recordedAt":null,"run":null,"observed":null,"formatVersion":null});
    let terms = (|| {
        let mut same_store = pointer.clone();
        same_store["storeProject"] = json!(conversation.store_project);
        if !conversation.names(&same_store) {
            return not_read("the pointer does not belong to this conversation and project");
        }
        let log = match log {
            Ok(log) => log,
            Err(e) => return not_read(format!("the App's records for this conversation's project could not be read: {e}")),
        };
        if pointer["storeProject"] != conversation.store_project {
            return not_read("the pointer names other records than the records this project folder belongs to now");
        }
        let found = log.for_point(pointer["point"].as_str().unwrap_or_default());
        let Some(&i) = found.first() else {
            return not_read(if log.missing { "the points log was not found in this project's records" } else { "no record with this point's reference was found in the App's records" });
        };
        if let Err(why) = log.soundness(i) { return not_read(why.clone()); }
        let line = &log.lines[i];
        let body = &line.entry["body"];
        if line.entry["recordId"] != pointer["record"] || body["source"] != pointer["source"] || !conversation.names(body) {
            return not_read("the record found does not belong to this pointer");
        }
        if pointer["digest"] != body["argumentsDigest"] {
            return not_read("the recorded terms do not match the digest kept with the pointer");
        }
        view["recordedAt"] = body["recordedAt"].clone();
        view["run"] = body["run"].clone();
        view["observed"] = body["observed"].clone();
        view["formatVersion"] = line.newer.as_ref().map_or(Value::Null, |v| json!(v));
        json!({"state":"read","arguments":body["arguments"]})
    })();
    view["terms"] = terms;
    view
}

#[cfg(test)]
#[path = "points_tests.rs"]
mod tests;
