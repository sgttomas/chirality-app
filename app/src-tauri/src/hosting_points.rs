//! DEL-02-03 REQ-008: the host side of a point placed in conversation
//! ([`crate::points`]): the offer, admission of an actual live call, the
//! placement (record, then receipt), the conversation's binding to its
//! records, the offer restored on an explicit resume, the run marks, and the
//! conversation's reading for the interface.
//!
//! **Placement.** Each admitted call is placed on a worker of its own, as the
//! records capability answers its reads, so that the frame reader keeps
//! receiving; the placements are serialised by one guard, [`PLACEMENT`], held
//! for the whole of each, and process-wide (across Codex homes and projects).
//! A placement binds through the store's own writer binding
//! ([`crate::records_store::bind_writer`]) under the store's write admission
//! ([`crate::records_retention::write_path`]), held across the writer's tail
//! recovery, the reading, the lookup of the call, the count, the append and
//! the reading again. Each reading it makes is published, with the stamps of
//! the log and of the project's link to the store at the time it was read.
//!
//! **Rereading.** A log is read again on a worker of its own, at most one per
//! project at a time, when the status path finds its stamps changed, its
//! reading older than [`REFRESH`] or no reading, and when a conversation of
//! the project is resumed. It binds through the store's reader binding under
//! its read admission ([`crate::records_retention::read_path`]) and the
//! writer binding of an already attached project, which mint, register and
//! attach nothing; each binding is checked against the physical project
//! folder the records capability admitted.
//!
//! **What a status read costs.** The status path the conversation panel reads
//! binds no store and reads no log. Under the Host lock it copies the small
//! in-memory state (offers, marks, the published readings' handles, the
//! request register's replies of the point rule); outside it, it indexes the
//! ledger's conversation rows once per ledger revision (linear in those rows,
//! then reused), takes two file stamps (the points log's and the project
//! link's) for each project of a conversation it shows, and copies each
//! conversation's records from the published reading, whose soundness was
//! decided when it was read. Where a stamp differs from the published one,
//! nothing is published yet, or the reading is older than [`REFRESH`], the
//! conversation's reading says it is not whole, with that reason, and the log
//! is read again.
use crate::points::{self, Conversation, LogReading, Outcome, Source};
use crate::records_index::Stamp;
use serde_json::{json, Value};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};

/// One placement or reread at a time in this process, for the whole of it.
static PLACEMENT: Mutex<()> = Mutex::new(());
fn one_at_a_time() -> std::sync::MutexGuard<'static, ()> {
    PLACEMENT.lock().unwrap_or_else(|poisoned| poisoned.into_inner())
}
/// How long a published reading is used before the log is read again even
/// with its stamps unchanged: past it, the reading is not whole until a new
/// one is published.
pub(crate) const REFRESH: std::time::Duration = std::time::Duration::from_secs(60);

/// A conversation offered the point tool in a generation.
#[derive(Clone, Debug)]
pub(super) struct Offer {
    generation: Value,
    thread: String,
    /// The App's home class (H-acct, H-key, H-omlx), once the conversation is
    /// indexed under a project; without it no point can be kept.
    home: Option<String>,
    /// "start": offered on the thread/start this App session sent;
    /// "restored": an earlier offer, restored on explicit resume.
    basis: &'static str,
    /// The generation of the original offer (for "start", this one).
    origin: Value,
}
/// A call whose recording the App could not establish, with the records it
/// was bound to.
#[derive(Clone, Debug)]
struct Uncertain {
    thread: String,
    source: Source,
    store: String,
    reason: String,
}
/// A reading of a project's points log, made under the store's read or
/// write admission, with what the status path compares. `store` is the
/// store's project identity, or none where the project has no records in
/// the store (then no points log exists, and `log` is the project link).
#[derive(Clone)]
struct Published {
    at: std::time::Instant,
    log: PathBuf,
    link: PathBuf,
    stamps: (Option<Stamp>, Option<Stamp>),
    store: Option<String>,
    reading: Arc<LogReading>,
}
fn stamp(path: &Path) -> Result<Option<Stamp>, String> {
    match std::fs::symlink_metadata(path) {
        Ok(m) => Ok(Some(Stamp::of(&m))),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(e.to_string()),
    }
}
/// One conversation's tags of this owner in the ledger.
#[derive(Clone, Debug)]
struct ThreadIndex {
    /// The home class and App project the ledger indexes it under.
    scope: Result<Option<(String, String)>, String>,
    offered: Vec<Value>,
    bound: Vec<Value>,
    unread: usize,
}
impl ThreadIndex {
    fn empty() -> Self {
        ThreadIndex { scope: Ok(None), offered: vec![], bound: vec![], unread: 0 }
    }
    /// The store project this conversation of the Codex home `native` is
    /// bound to, from its binding tags.
    fn bound_store(&self, native: &str) -> Result<Option<String>, String> {
        let mut stores: Vec<&str> = self.bound.iter().filter(|v| v["home"] == native).filter_map(|v| v["storeProject"].as_str()).collect();
        stores.sort();
        stores.dedup();
        match stores.as_slice() {
            [] => Ok(None),
            [one] => Ok(Some((*one).to_owned())),
            _ => Err("this conversation is bound to more than one records project".into()),
        }
    }
}
/// The ledger's conversation rows, indexed once per ledger revision.
#[derive(Default)]
struct LedgerIndex {
    threads: HashMap<String, ThreadIndex>,
}
fn index_ledger(rows: &[Value]) -> LedgerIndex {
    let mut by_thread: HashMap<&str, Vec<&Value>> = HashMap::new();
    for row in rows.iter().filter(|r| r["kind"] == "conversation_index") {
        if let Some(thread) = row["threadId"].as_str() { by_thread.entry(thread).or_default().push(row); }
    }
    let threads = by_thread.into_iter().map(|(thread, rows)| (thread.to_owned(), thread_index(&rows))).collect();
    LedgerIndex { threads }
}
/// As `recovery::tags_of` and the conversation's index rows, for one conversation.
fn thread_index(rows: &[&Value]) -> ThreadIndex {
    let mut homes: Vec<&str> = rows.iter().filter_map(|r| r["home"].as_str()).collect();
    homes.sort();
    homes.dedup();
    let scope = match homes.as_slice() {
        [] => Ok(None),
        [home] => Ok(rows.iter().rev().find(|r| r["home"] == *home).and_then(|r| r["project"].as_str()).map(|p| (home.to_string(), p.to_owned()))),
        _ => Err("the App's ledger names this conversation in more than one home".to_owned()),
    };
    let mut index = ThreadIndex { scope, ..ThreadIndex::empty() };
    if let Ok(Some((home, _))) = &index.scope {
        let mut tags: Vec<&Value> = vec![];
        for row in rows.iter().filter(|r| r["home"] == home.as_str()) {
            for tag in row["tags"].as_array().into_iter().flatten() {
                if tag["owner"] == points::TAG_OWNER && !tags.contains(&tag) { tags.push(tag); }
            }
        }
        tags.sort_by_key(|t| t["seq"].as_u64().unwrap_or(0));
        for tag in tags {
            match tag["value"].as_str().and_then(points::decode) {
                Some(v) if v["kind"] == "bound" => index.bound.push(v),
                Some(v) => index.offered.push(v),
                None => index.unread += 1,
            }
        }
    }
    index
}

/// The writer's append, or a test's in its place.
type Append = Box<dyn FnOnce(&Path, Value, String) -> Result<Value, String> + Send>;

/// The points state this Host keeps in memory. Nothing here is a point: a
/// point is shown only from its record.
#[derive(Default)]
pub(super) struct State {
    offers: Vec<Offer>,
    /// (generation, conversation, run, mark): "start sent", "not opened", "open", "ended".
    runs: Vec<(Value, String, String, &'static str)>,
    /// Calls refused in this App session: (generation, conversation, {reason, at}).
    refused: Vec<(Value, String, Value)>,
    uncertain: Vec<Uncertain>,
    /// Why the App could not check a conversation's records on resume: (generation, conversation, reason).
    unchecked: Vec<(Value, String, String)>,
    /// Conversations resumed whose binding is saved, where it is missing, at
    /// the next reading of their project that holds a sound record of theirs.
    resumed: Vec<(Value, String)>,
    /// The latest reading of each App project's points log.
    published: HashMap<String, Published>,
    /// Projects whose log is being read again.
    rereading: Vec<String>,
    /// Why the App could not read a project's points log.
    faults: HashMap<String, String>,
    ledger: Option<(Arc<Vec<Value>>, Arc<LedgerIndex>)>,
    #[cfg(test)]
    pub(super) hooks: TestHooks,
}
/// Seams at the workers' boundaries (tests only).
#[cfg(test)]
#[derive(Default)]
pub(super) struct TestHooks {
    /// Receipts as prepared.
    pub receipts: Vec<Value>,
    /// Run on the worker as it takes a call, before the placement.
    pub on_admitted: Option<Box<dyn FnOnce() + Send>>,
    /// Run under the placement guard just before the append.
    pub before_append: Option<Box<dyn FnOnce() + Send>>,
    /// In place of the writer's append.
    pub append: Option<Append>,
    /// Run after the record is written, before its binding is saved.
    pub after_append: Option<Box<dyn FnOnce() + Send>>,
    /// Run with no Host lock held just before a reply is written.
    pub before_reply: Option<Box<dyn FnOnce() + Send>>,
    /// Run on each worker thread when it starts.
    pub worker_setup: Option<Arc<dyn Fn() + Send + Sync>>,
    /// The workers started, for a test to wait on.
    pub workers: Vec<std::thread::JoinHandle<()>>,
    /// Refuse to start workers, as when a thread cannot be created.
    pub no_workers: bool,
}
/// The App's refusal sentences.
const NO_PROJECT: &str = "No App project is known for this conversation, so the point could not be kept; no point was placed.";
const ENDED: &str = "This Codex session ended before the point could be recorded; no point was placed.";
const STORE_OTHER: &str = "This conversation's points are kept in other records than the records this project folder belongs to now, so the point could not be kept; no point was placed.";
fn kept_refusal(reason: &str) -> String {
    let mut chars = reason.chars();
    let first = chars.next().map(|c| c.to_uppercase().collect::<String>()).unwrap_or_default();
    format!("{first}{}, so the point could not be kept; no point was placed.", chars.as_str())
}
fn store_refused(e: &str) -> String {
    format!("The App's records store did not take the point ({e}), so it could not be kept; no point was placed.")
}
fn at_cap() -> String {
    format!("This conversation already holds the App's own limit of {} points; no point was recorded.", points::POINTS_PER_CONVERSATION)
}
/// The App's reasons a conversation's reading is not whole.
const OTHER_OPEN: &str = "this conversation's App project is not the project the App has open now";
const NOT_YET_READ: &str = "the App has not yet read this conversation's records in this App session; it is reading them";
const READING_AGAIN: &str = "this conversation's records changed since the App last read them; it is reading them again";
const EXPIRED: &str = "the App last read this conversation's records more than a minute ago; it is reading them again";
const BOUND_OTHER: &str = "this conversation's points are kept in other records than the records this project folder belongs to now";
const BOUND_NONE: &str = "this conversation is bound to records in the App's records store, but this project folder has none there now";
const BOUND_NO_LOG: &str = "this conversation is bound to its project's records, but the points log was not found in them";
const BOUND_NO_RECORD: &str = "this conversation is bound to its project's records, but they hold no record of it";

/// One admitted call, with what the App observed at its admission.
pub(super) struct Call {
    generation: Value,
    thread: String,
    turn: String,
    call: String,
    request: Value,
    arguments: Value,
    home: Option<String>,
    run: Value,
    observed: Value,
}

fn same_folder(bound: (u64, u64), physical: &Value) -> Result<(), String> {
    if (physical["device"].as_u64(), physical["inode"].as_u64()) == (Some(bound.0), Some(bound.1)) { Ok(()) }
    else { Err("the project folder the records store binds is not the folder the App admitted for this project".into()) }
}
/// The App's reading of a points log under an admission: the log, what a
/// verified package import brought into it, and the store's project-wide
/// index of record identities.
fn read_log(root: &Path, dir: &Path, log: &Path) -> Result<LogReading, String> {
    let relative = crate::storage::log_rel(None, points::WRITER);
    LogReading::read_bound(log,
        |bytes| match crate::records_store::package::completed(dir)? {
            false => Ok(0),
            true => crate::records_store::package::quoted_prefix(dir, &relative, bytes),
        },
        |id| crate::records_index::with_index(root, |ix| ix.entries_with(id)).map(|found| found.len()))
}
/// A read of a project's points log, bound through the store's reader binding
/// and held under its read admission for the whole read.
struct Read {
    store: Option<String>,
    log: PathBuf,
    link: PathBuf,
    stamps: (Option<Stamp>, Option<Stamp>),
    reading: LogReading,
}
fn read_bound(root: &Path, physical: &Value) -> Result<Read, String> {
    let reader = crate::records_store::bind_reader(root, crate::records_store::ReaderDecision::Records)?;
    reader.prove().map_err(String::from)?;
    same_folder(reader.project_folder(), physical)?;
    let link = root.join(crate::records_store::PROJECT_LINK);
    // The store's identity for this project, from its binding of an already
    // attached project (it mints nothing); both bindings name one folder.
    let attached = crate::records_store::bind_writer_if_attached(root)?;
    let (dir, attached) = match (reader.records_folder(), attached) {
        (Some((dir, _)), Some(attached)) => (dir, attached),
        // The store holds no records of this project (its reader reads the
        // project's records in place): no points log exists.
        (None, attached) => {
            if attached.as_ref().is_some_and(|a| a.project_folder() != reader.project_folder()) {
                return Err("the project's records association changed while it was read".into());
            }
            let log = attached.as_ref().map_or_else(|| link.clone(), |a| a.records_dir().join(crate::storage::log_rel(None, points::WRITER)));
            let stamps = (stamp(&log)?, stamp(&link)?);
            reader.prove().map_err(String::from)?;
            return Ok(Read { store: attached.map(|a| a.project_id().to_owned()), log, link, stamps, reading: LogReading::missing() });
        }
        (Some(_), None) => return Err("the project's records association changed while it was read".into()),
    };
    if attached.project_folder() != reader.project_folder() || attached.records_dir() != dir {
        return Err("the project's records association changed while it was read".into());
    }
    let _admission = crate::records_retention::read_path(dir)?;
    let log = dir.join(crate::storage::log_rel(None, points::WRITER));
    let stamps = (stamp(&log)?, stamp(&link)?);
    let reading = read_log(root, dir, &log)?;
    reader.prove().map_err(String::from)?;
    if (stamp(&log)?, stamp(&link)?) != stamps { return Err("this project's points log changed while the App read it".into()); }
    Ok(Read { store: Some(attached.project_id().to_owned()), log, link, stamps, reading })
}
/// The receipt of a recorded point as the request register observed its
/// reply: written, not written, or not known.
/// A reply never attempted is not written once its request has ended
/// without it; while it is still being sent its outcome is not known.
fn receipt_state(result: &str, state: &str) -> &'static str {
    match (result, state) {
        ("written", _) => "written",
        ("write-failed", _) | ("not-attempted", "ended-unanswered" | "resolved-by-supplier") => "not written",
        _ => "not known",
    }
}

impl super::Host {
    /// Called where a `thread/start` result is admitted: the start's own
    /// parameters carried the point tool's definition exactly once.
    pub(super) fn note_point_offer(i: &mut super::Inner, generation: &Value, thread: &Value, params: &Value) {
        let offered = params["dynamicTools"].as_array().is_some_and(|tools| {
            let named: Vec<&Value> = tools.iter().filter(|t| t["name"] == points::TOOL).collect();
            named.len() == 1 && *named[0] == points::definition()
        });
        if let (true, Some(thread)) = (offered, thread.as_str()) {
            if !i.points.offers.iter().any(|o| o.generation == *generation && o.thread == thread) {
                i.points.offers.push(Offer { generation: generation.clone(), thread: thread.into(), home: None, basis: "start", origin: generation.clone() });
            }
        }
    }
    /// Where the conversation is indexed under its project at start: its home
    /// class is taken for the offer, and the offer pointer is written.
    pub(super) fn persist_point_offer(&self, generation: &Value, thread: &str, home: Option<&str>) {
        let Some(home) = home else { return };
        let offered = {
            let mut i = self.inner.0.lock().unwrap();
            match i.points.offers.iter_mut().find(|o| o.generation == *generation && o.thread == thread && o.basis == "start") {
                Some(offer) => { offer.home = Some(home.into()); true }
                None => false,
            }
        };
        let (Some(native), Ok(reference)) = (generation["home"].as_str(), crate::recovery::generation_ref(generation)) else { return };
        if offered {
            let _ = self.tag_conversation(generation, thread, Some(home), points::TAG_OWNER, &points::offer_pointer(native, &reference, thread));
        }
    }
    /// The run marks DEL-02-03's run makes for its conversation.
    pub(crate) fn note_conversation_run(&self, generation: &Value, thread: &str, run: &str, mark: &'static str) {
        let mut i = self.inner.0.lock().unwrap();
        i.points.runs.retain(|(g, t, r, _)| !(g == generation && t == thread && r == run));
        i.points.runs.push((generation.clone(), thread.into(), run.into(), mark));
    }
    /// The latest run mark of a conversation in a generation (tests).
    #[cfg(test)]
    pub(crate) fn run_mark_for_test(&self, generation: &Value, thread: &str) -> Option<&'static str> {
        self.inner.0.lock().unwrap().points.runs.iter().rev().find(|(g, t, _, _)| g == generation && t == thread).map(|(_, _, _, mark)| *mark)
    }
    /// The checks a received line meets to be a point call: the current
    /// generation, a well-formed server request (no result or error, the
    /// call's identities present) not on a private account channel, the exact
    /// tool with no namespace, from a conversation offered it in this
    /// generation. It reads the state only.
    pub(super) fn point_call_look(i: &super::Inner, generation: &Value, frame: &Value, private_auth: bool) -> bool {
        i.generation == *generation && !i.server_requests.is_closed(generation)
            && super::frame_class(frame) == "server-request" && !private_auth
            && points::frame_ok(frame) && frame["params"]["namespace"].is_null()
            && i.points.offers.iter().any(|o| o.generation == *generation && frame["params"]["threadId"] == o.thread.as_str())
    }
    /// A frame naming the point tool that the generic classifier does not
    /// take as a server request, but that carries a request identity the App
    /// can answer: routed through the request register, so that the agent is
    /// told it was not taken as a point call.
    pub(super) fn point_named_unframed(frame: &Value) -> bool {
        super::frame_class(frame) == "malformed" && frame["method"] == "item/tool/call" && frame["params"]["tool"] == points::TOOL
            && (frame["id"].is_string() || frame["id"].is_i64() || frame["id"].is_u64())
    }
    /// The run reading at admission. From this generation's run marks where
    /// it has one; otherwise from what the App knows across the boundary the
    /// conversation crossed: a run open or starting in it before this App
    /// session's Codex was restarted is not established; a conversation that
    /// began in an earlier App session cannot tell that session's runs; and
    /// one that began in this App session with no run open has none.
    fn run_at(i: &super::Inner, generation: &Value, thread: &str, offer: Option<&Offer>) -> Value {
        let mark = |same: &dyn Fn(&Value) -> bool| i.points.runs.iter().rev().find(|(g, t, _, _)| same(g) && *t == thread).map(|(_, _, run, mark)| (run.clone(), *mark));
        match mark(&|g| g == generation) {
            Some((run, "open")) => return points::run_in(&run),
            Some((_, "start sent")) => return points::run_not_established("start-sent-not-yet-open"),
            Some(_) => return points::run_none(),
            None => {}
        }
        let session = &generation["appSession"];
        if let Some((_, "open" | "start sent")) = mark(&|g| g["appSession"] == *session) {
            return points::run_not_established("codex-restarted-run-unknown");
        }
        match offer {
            Some(o) if o.basis == "restored" && o.origin["appSession"] != *session => points::run_not_established("resumed-earlier-run-unknown"),
            _ => points::run_none(),
        }
    }
    /// The facts of an admitted point call, read under Inner at its admission.
    pub(super) fn point_call(i: &super::Inner, generation: &Value, frame: &Value) -> Call {
        let p = &frame["params"];
        let s = |v: &Value| v.as_str().unwrap_or_default().to_owned();
        let thread = s(&p["threadId"]);
        let offer = i.points.offers.iter().find(|o| o.generation == *generation && o.thread == thread);
        let run = Self::run_at(i, generation, &thread, offer);
        let turn = s(&p["turnId"]);
        let started = i.conversation_turns.iter().find(|t| t["generation"] == *generation && t["threadId"] == thread.as_str() && t["turnId"] == turn.as_str())
            .and_then(|t| t.get("appTurnStart")).and_then(|sent| sent["requestRef"].as_str());
        let observed = match started {
            Some(reference) => {
                let person = i.source_requests.values().any(|e| e.request.generation == *generation && e.request.request_ref == reference && e.observation_base["initiator"]["kind"] == "person-directed");
                points::observed(person.then_some(reference), true)
            }
            None => points::observed(None, false),
        };
        Call { generation: generation.clone(), thread, turn, call: s(&p["callId"]), request: frame["id"].clone(), arguments: p["arguments"].clone(),
            home: offer.and_then(|o| o.home.clone()), run, observed }
    }
    /// A worker of its own for `work`, as the records capability answers its
    /// reads: the work travels in a slot, so that where a worker cannot be
    /// created the slot hands it back to be done by the caller.
    fn on_worker<T: Send + 'static>(&self, name: &str, work: T, run: impl FnOnce(&super::Host, T) + Send + 'static) -> Option<T> {
        let host = self.this.lock().unwrap().upgrade();
        #[cfg(test)]
        let (setup, refused) = { let i = self.inner.0.lock().unwrap(); (i.points.hooks.worker_setup.clone(), i.points.hooks.no_workers) };
        #[cfg(test)]
        let host = host.filter(|_| !refused);
        let slot = Arc::new(Mutex::new(Some(work)));
        let spawned = host.and_then(|host| {
            let taken = Arc::clone(&slot);
            std::thread::Builder::new().name(name.into()).spawn(move || {
                #[cfg(test)]
                if let Some(setup) = setup { setup(); }
                if let Some(work) = taken.lock().unwrap().take() { run(&host, work); }
            }).ok()
        });
        match spawned {
            #[cfg(test)]
            Some(handle) => { self.inner.0.lock().unwrap().points.hooks.workers.push(handle); None }
            #[cfg(not(test))]
            Some(_) => None,
            None => slot.lock().unwrap().take(),
        }
    }
    /// The receiver hands an admitted call to a worker of its own. Where no
    /// worker can be created the call is placed here, inline, as the records
    /// capability answers a read it cannot hand to a worker: never
    /// unanswered.
    pub(super) fn dispatch_point_call(&self, call: Call) {
        if let Some(call) = self.on_worker("point-record", call, |host, call| host.answer_point_call(call)) {
            self.answer_point_call(call);
        }
    }
    fn answer_point_call(&self, call: Call) {
        #[cfg(test)]
        { let hook = self.inner.0.lock().unwrap().points.hooks.on_admitted.take(); if let Some(hook) = hook { hook(); } }
        let outcome = self.place_point(&call);
        self.deliver(&call, outcome);
    }
    /// A reread of a project's points log, off the receiver and off the
    /// status path, at most one in flight per project. Where no worker can be
    /// created nothing is read now: the reading stays not whole, and the next
    /// status read asks again.
    fn reread(&self, project: &str) {
        {
            let mut i = self.inner.0.lock().unwrap();
            if i.points.rereading.iter().any(|p| p == project) { return; }
            i.points.rereading.push(project.to_owned());
        }
        if self.on_worker("point-read", project.to_owned(), |host, project| host.read_again(&project)).is_some() {
            self.inner.0.lock().unwrap().points.rereading.retain(|p| p != project);
        }
    }
    fn read_again(&self, project: &str) {
        let read = {
            let _one = one_at_a_time();
            self.open_project(project).and_then(|(root, physical)| read_bound(&root, &physical))
        };
        let reading = {
            let mut i = self.inner.0.lock().unwrap();
            i.points.rereading.retain(|p| p != project);
            match read {
                Ok(read) => { i.points.faults.remove(project); Some(Self::publish(&mut i, project, read)) }
                Err(reason) => { i.points.published.remove(project); i.points.faults.insert(project.to_owned(), reason); None }
            }
        };
        let Some((reading, Some(store))) = reading else { return };
        // A resumed conversation of this project with a sound record and no
        // binding is bound now.
        let resumed: Vec<(Value, String)> = std::mem::take(&mut self.inner.0.lock().unwrap().points.resumed);
        let mut kept = vec![];
        for (generation, thread) in resumed {
            let index = self.thread_of(&thread);
            match &index.scope {
                Ok(Some((home, p))) if p == project => {
                    let native = generation["home"].as_str().unwrap_or_default();
                    let conversation = Conversation { home: native, home_class: home, thread: &thread, project, store_project: &store };
                    if matches!(index.bound_store(native), Ok(None)) && reading.sound_of(&conversation) > 0 {
                        let _ = self.keep_tag(&generation, &thread, home, &points::binding_pointer(native, &thread, project, &store));
                    }
                }
                _ => kept.push((generation, thread)),
            }
        }
        self.inner.0.lock().unwrap().points.resumed.extend(kept);
    }
    fn publish(i: &mut super::Inner, project: &str, read: Read) -> (Arc<LogReading>, Option<String>) {
        let reading = Arc::new(read.reading);
        let store = read.store.clone();
        i.points.published.insert(project.to_owned(), Published { at: std::time::Instant::now(), log: read.log, link: read.link, stamps: read.stamps, store: read.store, reading: Arc::clone(&reading) });
        (reading, store)
    }
    /// The receipt, prepared and written as the register's named replies
    /// are. Whether it was written is the register's own observation of the
    /// request, which the conversation's reading shows.
    fn deliver(&self, call: &Call, outcome: Outcome) {
        let receipt = points::receipt(&outcome, &call.run);
        let point = match &outcome { Outcome::Recorded { point, .. } => Some(point.clone()), Outcome::NotEstablished { point, .. } => point.clone(), Outcome::NotRecorded { .. } => None };
        #[cfg(test)]
        self.inner.0.lock().unwrap().points.hooks.receipts.push(receipt.clone());
        let text = receipt["contentItems"][0]["text"].as_str().unwrap_or_default().to_owned();
        let reference = json!({"point":point,"bytes":text.len(),"content":{"method":crate::util::FILE_IDENTITY_METHOD,"value":crate::util::sha256_hex(text.as_bytes())},"success":receipt["success"]});
        let unsent = |reason: String| {
            self.inner.0.lock().unwrap().journal.push(json!({"generation":call.generation,"class":"point-call-not-answered","reason":reason,"requestIdentity":call.request}));
        };
        if let Err(reason) = self.check_local_reply() {
            unsent(reason);
            self.flush_recovery_observations();
            return;
        }
        let prepared = {
            let mut i = self.inner.0.lock().unwrap();
            i.server_requests.prepare_named_tool(&call.generation, &call.request, &receipt, points::RULE, reference)
                .and_then(|frame| self.capture_pipe(&i).map(|bound| (bound, frame)))
        };
        #[cfg(test)]
        { let hook = self.inner.0.lock().unwrap().points.hooks.before_reply.take(); if let Some(hook) = hook { hook(); } }
        match prepared {
            Ok((bound, frame)) => if let Err(reason) = self.write_reply(bound, &frame) { unsent(reason) },
            Err(reason) => unsent(reason),
        }
        self.flush_recovery_observations();
    }
    fn refuse(&self, call: &Call, reason: String) -> Outcome {
        let mut i = self.inner.0.lock().unwrap();
        let mine = i.points.refused.iter().filter(|(g, t, _)| *g == call.generation && *t == call.thread).count();
        if mine >= points::REFUSALS_KEPT {
            if let Some(at) = i.points.refused.iter().position(|(g, t, _)| *g == call.generation && *t == call.thread) { i.points.refused.remove(at); }
        }
        i.points.refused.push((call.generation.clone(), call.thread.clone(), json!({"reason":reason,"at":crate::util::now_rfc3339()})));
        Outcome::NotRecorded { reason }
    }
    /// A call whose recording the App could not establish: remembered with
    /// the records it was bound to, so that the conversation's reading is not
    /// whole until a reading of those records resolves it.
    fn not_established(&self, source: &Source, store: &str, point: Option<String>, reason: String) -> Outcome {
        self.inner.0.lock().unwrap().points.uncertain.push(Uncertain { thread: source.thread.clone(), source: source.clone(), store: store.into(), reason: reason.clone() });
        Outcome::NotEstablished { point, reason: points::not_established(&reason) }
    }
    /// The ledger's conversation rows and their index (rebuilt only when the
    /// ledger observation changed).
    fn ledger_index(&self) -> (Arc<Vec<Value>>, Arc<LedgerIndex>) {
        let (rows, held) = {
            let i = self.inner.0.lock().unwrap();
            let rows: Arc<Vec<Value>> = i.recovery_snapshot.as_ref().map(|o| Arc::clone(&o.rows)).unwrap_or_default();
            let held = i.points.ledger.as_ref().filter(|(r, _)| Arc::ptr_eq(r, &rows)).map(|(_, ix)| Arc::clone(ix));
            (rows, held)
        };
        if let Some(index) = held { return (rows, index); }
        let index = Arc::new(index_ledger(&rows));
        self.inner.0.lock().unwrap().points.ledger = Some((Arc::clone(&rows), Arc::clone(&index)));
        (rows, index)
    }
    fn thread_of(&self, thread: &str) -> ThreadIndex {
        self.ledger_index().1.threads.get(thread).cloned().unwrap_or_else(ThreadIndex::empty)
    }
    /// The open project's folder and its admitted physical identity, when the
    /// conversation's App project is the project the App has open now.
    fn open_project(&self, project: &str) -> Result<(PathBuf, Value), String> {
        let (capability, open) = {
            let i = self.inner.0.lock().unwrap();
            (i.records_capability.clone(), i.records_project_context.as_ref().and_then(|c| c.reference()).map(str::to_owned))
        };
        if open.as_deref() != Some(project) { return Err(OTHER_OPEN.into()); }
        let capability = capability.ok_or(OTHER_OPEN)?;
        let physical = capability.project_identity().map_err(|e| format!("this project's folder is not the folder the App admitted ({e})"))?;
        Ok((capability.project_folder().to_path_buf(), physical))
    }
    /// A tag of this owner on the conversation, through the Host's own
    /// `tag_conversation`: kept only where the ledger kept it durably, and
    /// refused, with its limit, where the conversation's generation is no
    /// longer current or the ledger did not keep it.
    fn keep_tag(&self, generation: &Value, thread: &str, home: &str, value: &str) -> Result<(), String> {
        let tagged = self.tag_conversation(generation, thread, Some(home), points::TAG_OWNER, value);
        if tagged["persistence"] == "durable App metadata" { Ok(()) } else { Err(tagged["limit"].as_str().unwrap_or("the tag was not kept").to_owned()) }
    }
    /// One placement, under the one placement guard for the whole of it and
    /// the store's write admission from the proof of its binding to the
    /// reading after the append: every refusal the App can decide without
    /// writing, then the writer's own tail recovery, then the reading, the
    /// lookup of this call and the count, the record (or the one already
    /// bound to this call), then the conversation's binding to its records.
    fn place_point(&self, call: &Call) -> Outcome {
        let _one = one_at_a_time();
        if let Err(reason) = points::validate(&call.arguments) { return self.refuse(call, reason); }
        let (Some(native), Ok(generation)) = (call.generation["home"].as_str(), crate::recovery::generation_ref(&call.generation)) else { return self.refuse(call, ENDED.into()) };
        let open = |host: &Self| { let i = host.inner.0.lock().unwrap(); Self::context_scope(&i, &call.generation, &call.thread, None).is_ok() };
        if !open(self) { return self.refuse(call, ENDED.into()); }
        let index = self.thread_of(&call.thread);
        let (home, project) = match &index.scope {
            Ok(Some(scope)) if call.home.as_deref() == Some(scope.0.as_str()) => scope.clone(),
            Ok(_) => return self.refuse(call, NO_PROJECT.into()),
            Err(reason) => return self.refuse(call, kept_refusal(reason)),
        };
        let bound_store = match index.bound_store(native) { Ok(bound) => bound, Err(reason) => return self.refuse(call, kept_refusal(&reason)) };
        let (root, physical) = match self.open_project(&project) { Ok(found) => found, Err(reason) => return self.refuse(call, kept_refusal(&reason)) };
        // The writer binding, the store's write admission held from here, and
        // the binding proved inside it (records_store::WriterBinding::prove_for_write).
        let binding = match crate::records_store::bind_writer(&root).and_then(|b| same_folder(b.project_folder(), &physical).map(|_| b)) {
            Ok(binding) => binding,
            Err(e) => return self.refuse(call, store_refused(&e)),
        };
        let _admission = match crate::records_retention::write_path(binding.records_dir()) { Ok(admission) => admission, Err(e) => return self.refuse(call, store_refused(&e)) };
        if let Err(e) = binding.prove_for_write() { return self.refuse(call, store_refused(&e)); }
        let store_project = binding.project_id().to_owned();
        if bound_store.as_deref().is_some_and(|bound| bound != store_project) { return self.refuse(call, STORE_OTHER.into()); }
        let dir = binding.records_dir().to_path_buf();
        let log = dir.join(crate::storage::log_rel(None, points::WRITER));
        let link = root.join(crate::records_store::PROJECT_LINK);
        let conversation = Conversation { home: native, home_class: &home, thread: &call.thread, project: &project, store_project: &store_project };
        let source = Source { home: native.into(), home_class: home.clone(), generation: generation.clone(), thread: call.thread.clone(), turn: call.turn.clone(), call: call.call.clone(), request: call.request.clone() };
        // The binding, saved once a sound record of the conversation is read
        // and the conversation has none: never before its first record.
        let mut unbound = bound_store.is_none();
        let mut bind = |host: &Self| if unbound && host.keep_tag(&call.generation, &call.thread, &home, &points::binding_pointer(native, &call.thread, &project, &store_project)).is_ok() { unbound = false; };
        // The writer's own tail recovery (RS W-0 at the writer's open): a
        // whole last line that lost its newline is terminated, a torn one set
        // aside, before anything is read or counted.
        if let Err(e) = crate::records::open_owning_log(&root, &log) { return self.refuse(call, store_refused(&e)); }
        let reread = |host: &Self| -> Result<Arc<LogReading>, String> {
            let stamps = (stamp(&log)?, stamp(&link)?);
            let reading = read_log(&root, &dir, &log)?;
            let mut i = host.inner.0.lock().unwrap();
            Ok(Self::publish(&mut i, &project, Read { store: Some(store_project.clone()), log: log.clone(), link: link.clone(), stamps, reading }).0)
        };
        let reading = match reread(self) { Ok(reading) => reading, Err(e) => return self.refuse(call, store_refused(&e)) };
        if reading.sound_of(&conversation) > 0 { bind(self); }
        // The call itself, met again: the lookup by its identity is the guard
        // that an unresolved write is never doubled.
        if reading.tail_is(&source) {
            return self.not_established(&source, &store_project, None, "the record for this call is the last line of the points log and is not yet terminated".into());
        }
        let existing = match reading.for_call(&source).as_slice() {
            [] => None,
            [i] if reading.soundness(*i).is_ok() && conversation.names(&reading.lines[*i].entry["body"]) => Some(reading.lines[*i].entry.clone()),
            _ => return self.not_established(&source, &store_project, None, "the App's records hold a record for this call that it cannot establish".into()),
        };
        let entry = match existing {
            Some(entry) => entry,
            None => {
                if !reading.whole() {
                    return self.refuse(call, format!("The App could not read this project's points log whole ({}), so it cannot establish that this call was not recorded before; no point was placed.", reading.inventory_reasons().join("; ")));
                }
                if reading.sound_of(&conversation) >= points::POINTS_PER_CONVERSATION { return self.refuse(call, at_cap()); }
                let (point, record) = match (crate::util::opaque_id("pt-"), crate::util::opaque_id("rec:app:")) {
                    (Ok(point), Ok(record)) => (point, record),
                    (Err(e), _) | (_, Err(e)) => return self.refuse(call, store_refused(&e)),
                };
                let digest = match points::digest(&call.arguments) { Ok(d) => d, Err(e) => return self.refuse(call, store_refused(&e)) };
                let body = points::record_body(&point, &source, &project, &store_project, &call.run, &call.observed, &call.arguments, &digest, &crate::util::now_rfc3339());
                #[cfg(test)]
                { let hook = self.inner.0.lock().unwrap().points.hooks.before_append.take(); if let Some(hook) = hook { hook(); } }
                // Publication admission against the generation's closure: a
                // closed generation is refused here with nothing written. A
                // record that lands after this check is a recorded point.
                if !open(self) { return self.refuse(call, ENDED.into()); }
                if let Err(e) = binding.prove_for_write() { return self.refuse(call, store_refused(&e)); }
                #[cfg(test)]
                let append = self.inner.0.lock().unwrap().points.hooks.append.take();
                #[cfg(not(test))]
                let append: Option<Append> = None;
                let written = match append {
                    Some(append) => append(&log, body, record.clone()),
                    None => crate::records::append_reserved(&log, points::KIND, &crate::records::APP_WRITER, body, record.clone(), None, None, crate::records::RecordSet::Complete, crate::schema_validation::bundled()),
                };
                match written {
                    Ok(entry) => { let _ = reread(self); entry }
                    // The writer can fail after the line, or part of it, was
                    // written: the log is read again before anything is said.
                    Err(e) => match reread(self) {
                        Ok(again) => match again.for_call(&source).as_slice() {
                            [i] if again.soundness(*i).is_ok() && conversation.names(&again.lines[*i].entry["body"]) => again.lines[*i].entry.clone(),
                            [] if again.whole() => return self.refuse(call, store_refused(&e)),
                            _ => return self.not_established(&source, &store_project, Some(point), format!("the write reported {e}, and the App's records do not show whether it landed")),
                        },
                        Err(again) => return self.not_established(&source, &store_project, Some(point), format!("the write reported {e}, and the points log could not be read again: {again}")),
                    },
                }
            }
        };
        #[cfg(test)]
        { let hook = self.inner.0.lock().unwrap().points.hooks.after_append.take(); if let Some(hook) = hook { hook(); } }
        // Where the binding cannot be saved now (Codex closed, or the ledger
        // did not keep it), the record stands and the point is shown; the
        // binding is saved at the next placement or resume that reads it.
        bind(self);
        Outcome::Recorded { point: entry["body"]["point"].as_str().unwrap_or_default().to_owned(), persistence: points::KEPT.to_owned(), run: entry["body"]["run"].clone() }
    }
    /// On an explicit resume (after `restore_records_receipt`): the earlier
    /// offer is restored from its tag when it names this Codex home and
    /// conversation and the definition offered now, keeping the generation it
    /// was first made in. Then, for any conversation the ledger indexes under
    /// a project, the project's points log is read again, and the
    /// conversation is bound to its records where it has a sound record and
    /// no binding.
    pub(super) fn restore_point_offer(&self, generation: &Value, thread: &str) {
        let native = generation["home"].as_str().unwrap_or_default().to_owned();
        {
            let _writer = self.recovery_writer.lock().unwrap();
            self.drain_recovery_owned();
            self.refresh_recovery_observation();
            let i = self.inner.0.lock().unwrap();
            if Self::context_scope(&i, generation, thread, None).is_err() { return; }
            if i.recovery_initialization_error.is_some() || i.recovery_error.is_some() || i.recovery_snapshot.is_none() {
                drop(i);
                return self.point_unchecked(generation, thread, "the App's recovery ledger could not be read");
            }
        }
        let index = self.thread_of(thread);
        let (home, project) = match &index.scope {
            Ok(Some(scope)) => scope.clone(),
            Ok(None) => return,
            Err(reason) => return self.point_unchecked(generation, thread, reason),
        };
        if let Some(origin) = index.offered.iter().find(|v| v["home"] == native.as_str() && v["thread"] == thread && v["definition"] == points::definition_digest())
            .and_then(|v| v["generation"].as_str()).and_then(|g| crate::recovery::generation_from_ref(g).ok()) {
            let mut i = self.inner.0.lock().unwrap();
            if Self::context_scope(&i, generation, thread, None).is_err() { return; }
            if !i.points.offers.iter().any(|o| o.generation == *generation && o.thread == thread) {
                i.points.offers.push(Offer { generation: generation.clone(), thread: thread.into(), home: Some(home.clone()), basis: "restored", origin });
            }
        }
        {
            let mut i = self.inner.0.lock().unwrap();
            if !i.points.resumed.iter().any(|(g, t)| g == generation && t == thread) { i.points.resumed.push((generation.clone(), thread.into())); }
            // A resume reads the log again whatever was published before.
            i.points.published.remove(&project);
        }
        if self.open_project(&project).is_ok() { self.reread(&project); }
    }
    fn point_unchecked(&self, generation: &Value, thread: &str, reason: &str) {
        self.inner.0.lock().unwrap().points.unchecked.push((generation.clone(), thread.into(), reason.into()));
    }
    /// Each current conversation's points as the App reads them now: every
    /// record of the project's points log that names the conversation by its
    /// own binding, in the reading last published. The status path binds no
    /// store and reads no log (see the module's account of its cost).
    pub(super) fn points_view(&self) -> Value {
        struct Row { thread: String, offer: Option<Offer>, refused: Vec<Value>, uncertain: Vec<Uncertain>, unchecked: Vec<String> }
        let (generation, health, threads, published, open, faults, rereading, replies) = {
            let i = self.inner.0.lock().unwrap();
            let generation = i.generation.clone();
            if generation.is_null() { return json!([]); }
            let health = if i.recovery_initialization_error.is_some() || i.recovery_error.is_some() || i.recovery_snapshot.is_none() {
                Some("the App's recovery ledger could not be read".to_owned())
            } else {
                i.recovery_snapshot.as_ref().and_then(|o| o.summary["historyLimits"].as_array().filter(|l| !l.is_empty()).map(|_| "the App's recovery ledger history is incomplete".to_owned()))
            };
            let threads: Vec<Row> = i.threads.iter().filter(|t| t["generation"] == generation).filter_map(|t| t["threadId"].as_str()).map(|thread| Row {
                thread: thread.into(), offer: i.points.offers.iter().find(|o| o.generation == generation && o.thread == thread).cloned(),
                refused: i.points.refused.iter().filter(|(g, t, _)| *g == generation && t == thread).map(|(_, _, r)| r.clone()).collect(),
                uncertain: i.points.uncertain.iter().filter(|u| u.thread == thread).cloned().collect(),
                unchecked: i.points.unchecked.iter().filter(|(g, t, _)| *g == generation && t == thread).map(|(_, _, why)| why.clone()).collect(),
            }).collect();
            (generation, health, threads, i.points.published.clone(), i.records_project_context.as_ref().and_then(|c| c.reference()).map(str::to_owned),
                i.points.faults.clone(), i.points.rereading.clone(), i.server_requests.named_replies(points::RULE))
        };
        let (_, index) = self.ledger_index();
        let native = generation["home"].as_str().unwrap_or_default().to_owned();
        // Each project's published reading, taken while its stamps match and
        // it is not older than the refresh limit.
        let mut fresh: HashMap<String, Result<Published, String>> = HashMap::new();
        let mut reread: Vec<String> = vec![];
        let (mut resolved_uncertain, mut checked_threads, mut later_refused) = (vec![], vec![], vec![]);
        let views: Vec<Value> = threads.into_iter().map(|row| {
            let mut reasons: Vec<String> = health.iter().cloned().collect();
            let offer = match &row.offer {
                Some(o) if o.basis == "start" => json!({"state":"offered at start in this App session"}),
                Some(_) => json!({"state":"offered when this conversation started; restored when it was resumed"}),
                None => json!({"state":"not offered in this App session"}),
            };
            let mut shown: Vec<Value> = vec![];
            let mut refused = row.refused.clone();
            let ti = index.threads.get(&row.thread).cloned().unwrap_or_else(ThreadIndex::empty);
            match &ti.scope {
                Err(why) => reasons.push(why.clone()),
                Ok(None) => {}
                Ok(Some((home, project))) => {
                    if ti.unread > 0 { reasons.push(format!("{} tag(s) of the App's point tool kept for this conversation could not be read", ti.unread)); }
                    let bound = ti.bound_store(&native);
                    if let Err(why) = &bound { reasons.push(why.clone()); }
                    let read = fresh.entry(project.clone()).or_insert_with(|| {
                        if open.as_deref() != Some(project.as_str()) { return Err(format!("the App could not read this conversation's records: {OTHER_OPEN}")); }
                        if let Some(reason) = faults.get(project) {
                            reread.push(project.clone());
                            return Err(format!("the App could not read this conversation's records ({reason}); it is reading them again"));
                        }
                        match published.get(project) {
                            None => { reread.push(project.clone()); Err(NOT_YET_READ.into()) }
                            Some(p) => match (stamp(&p.log), stamp(&p.link)) {
                                (Ok(log), Ok(link)) if (log, link) != p.stamps => { reread.push(project.clone()); Err(READING_AGAIN.into()) }
                                (Ok(_), Ok(_)) if p.at.elapsed() >= REFRESH => { reread.push(project.clone()); Err(EXPIRED.into()) }
                                (Ok(_), Ok(_)) => Ok(p.clone()),
                                _ => { reread.push(project.clone()); Err(READING_AGAIN.into()) }
                            },
                        }
                    }).clone();
                    match read {
                        Err(reason) => {
                            reasons.push(reason);
                            reasons.extend(row.uncertain.iter().map(|m| m.reason.clone()));
                            reasons.extend(row.unchecked.iter().cloned());
                        }
                        Ok(p) => {
                            let reading = &p.reading;
                            let store = p.store.clone().unwrap_or_default();
                            let conversation = Conversation { home: &native, home_class: home, thread: &row.thread, project, store_project: &store };
                            shown = if p.store.is_some() { points::show(reading, &conversation) } else { vec![] };
                            for view in &shown {
                                if view["terms"]["state"] != "read" { reasons.push(format!("the terms of point {} were not read: {}", view["point"].as_str().unwrap_or_default(), view["terms"]["reason"].as_str().unwrap_or_default())); }
                            }
                            match bound.as_ref().ok().cloned().flatten() {
                                Some(_) if p.store.is_none() => reasons.push(BOUND_NONE.into()),
                                Some(bound) if p.store.as_deref() != Some(bound.as_str()) => reasons.push(BOUND_OTHER.into()),
                                Some(_) if reading.missing => reasons.push(BOUND_NO_LOG.into()),
                                Some(_) if shown.is_empty() => reasons.push(BOUND_NO_RECORD.into()),
                                _ => {}
                            }
                            reasons.extend(reading.inventory_reasons());
                            for mark in &row.uncertain {
                                if p.store.as_deref() != Some(mark.store.as_str()) { reasons.push(mark.reason.clone()); continue; }
                                match reading.for_call(&mark.source).as_slice() {
                                    [i] if reading.soundness(*i).is_ok() => resolved_uncertain.push(mark.source.clone()),
                                    [] if reading.whole() => {
                                        resolved_uncertain.push(mark.source.clone());
                                        later_refused.push((row.thread.clone(), json!({"reason":"The App has since read this conversation's records whole: the call whose recording it could not establish was not recorded.","at":crate::util::now_rfc3339()})));
                                        refused.push(later_refused.last().unwrap().1.clone());
                                    }
                                    _ => reasons.push(mark.reason.clone()),
                                }
                            }
                            checked_threads.push(row.thread.clone());
                        }
                    }
                }
            }
            // The receipt of each point placed in this App session, as the
            // request register observed its reply; none for an earlier one.
            for view in shown.iter_mut() {
                let placed = view["source"]["generation"].as_str().and_then(|g| crate::recovery::generation_from_ref(g).ok());
                view["receipt"] = match placed {
                    Some(g) if g["appSession"] == generation["appSession"] => {
                        let found = replies.iter().find(|(rg, id, _, _)| *rg == g && *id == view["source"]["request"]);
                        json!(found.map_or("not known", |(_, _, result, state)| receipt_state(result, state)))
                    }
                    _ => Value::Null,
                };
                if let Some(o) = view.as_object_mut() { o.remove("source"); }
            }
            json!({"generation":generation,"threadId":row.thread,"offer":offer,
                "reading":{"whole":reasons.is_empty(),"reasons":reasons},"points":shown,"refused":refused})
        }).collect();
        reread.sort();
        reread.dedup();
        {
            let mut i = self.inner.0.lock().unwrap();
            i.points.uncertain.retain(|u| !resolved_uncertain.contains(&u.source));
            i.points.unchecked.retain(|(g, t, _)| !(*g == generation && checked_threads.contains(t)));
            for (thread, entry) in later_refused { i.points.refused.push((generation.clone(), thread, entry)); }
        }
        for project in reread.into_iter().filter(|p| !rereading.contains(p)) { self.reread(&project); }
        json!(views)
    }
    /// Waits until every worker this Host started for points, and any they
    /// started in turn, has finished (tests).
    #[cfg(test)]
    pub(super) fn drain_points_for_test(&self) {
        loop {
            let workers = std::mem::take(&mut self.inner.0.lock().unwrap().points.hooks.workers);
            if workers.is_empty() { return; }
            for worker in workers { let _ = worker.join(); }
        }
    }
}

#[cfg(test)]
#[path = "hosting_points_tests.rs"]
mod tests;
