//! A derived SQLite query index of one project's authoritative RS logs.
//! Identities, positions and cross-run membership sets live on disk; memory
//! keeps log/directory state and at most two parsed lines while rebuilding.
//! Each process starts from the logs, using its own disposable database in
//! the store's `indexes/` directory (or a private temporary cache if the store
//! cannot host a cache). No existing database is trusted on cold start.
//!
//! Refresh, writer-first-open, 4 KiB growth guard and the full verifier retain
//! their source-read rules. Every returned record is reread and validated from
//! its source log, including its complete group, identity, seq and exact line
//! digest. A changed/deleted/corrupt cache is rebuilt; query errors use a full
//! source scan. The logs remain readable even when no cache can be created.
//! The growth-guard blind spot remains bounded by the verifier interval plus
//! a full pass; cold starts still validate every log. Full act projections
//! remain proportional to the requested result, independently of this cache.
use serde_json::{json, Value};
use std::cell::{Cell, RefCell};
use sha2::{Digest, Sha256};
#[path = "records_query.rs"]
mod query;
use std::collections::{BTreeMap, BTreeSet, HashMap};
use std::os::unix::fs::MetadataExt;
use std::path::{Path, PathBuf};
use std::sync::Mutex;

const GUARD: u64 = 4096;
const INDEXED_PROJECTS: usize = 4;
/// How often the background verifier starts a full pass (seconds).
pub(crate) const VERIFY_INTERVAL: u64 = 60;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub(crate) struct Stamp { dev: u64, ino: u64, size: u64, mtime: i64, mtime_ns: i64, ctime: i64, ctime_ns: i64 }
impl Stamp {
    pub(crate) fn of(m: &std::fs::Metadata) -> Self {
        Self { dev: m.dev(), ino: m.ino(), size: m.len(), mtime: m.mtime(), mtime_ns: m.mtime_nsec(), ctime: m.ctime(), ctime_ns: m.ctime_nsec() }
    }
}
#[derive(Clone, Debug, PartialEq)]
/// One entry, at its line: `member` is its place in a group line (RS §13.8).
struct Line { id: Option<String>, offset: u64, len: usize, seq: u64, act: bool, corrects: Option<String>, late_subject: Option<String>, member: Option<usize>, digest: String }
#[derive(Clone, Default)]
struct LogState {
    /// This log's number in the index (identities name logs by number).
    number: u32,
    revision: u64,
    prefix_proof: Option<String>,
    stamp: Option<Stamp>,
    /// Where the next read starts: the start of the last complete line.
    prefix_end: u64,
    prefix_lines: usize,
    prefix_seq: u64,
    prefix_limits: Vec<String>,
    prefix_max_seq: u64,
    prefix_has_act: bool,
    prefix_digest: Sha256,
    /// Up to GUARD bytes before `prefix_end`, as last read.
    guard: Vec<u8>,
    tail_limits: Vec<String>,
    max_seq: u64,
    has_act: bool,
    digest: String,
    partial: Option<String>,
    /// The end of the last complete line (where a torn tail starts).
    complete_end: u64,
    /// The chain where the last complete line starts, and after it.
    prefix_chain: crate::record_lines::Chain,
    chain: crate::record_lines::Chain,
    /// Limits that do not make the log incomplete (torn lines W-0 named).
    prefix_notes: Vec<String>,
    tail_notes: Vec<String>,
}
impl LogState {
    fn limits(&self) -> impl Iterator<Item = &String> { self.prefix_limits.iter().chain(&self.tail_limits) }
    fn reading(&self) -> (&str, Vec<&String>, &Option<String>, &crate::record_lines::Chain) { (&self.digest, self.limits().collect(), &self.partial, &self.chain) }
}

type Dirs = HashMap<PathBuf, (Stamp, Vec<(PathBuf, bool)>)>;
#[derive(Default)]
pub(crate) struct ProjectIndex {
    dirs: Dirs,
    logs: BTreeMap<PathBuf, LogState>,
    db: Option<query::QueryDb>,
    cache_fault: Cell<bool>,
    root: PathBuf,
    numbers: HashMap<u32, PathBuf>,
    next_number: u32,
    generation: u64,
    discovery_revision: u64,
    discovery_error: Option<String>,
    /// Increased whenever the act-relevant entries may have changed.
    act_epoch: u64,
    /// Logs the next refresh reads in full: a line read again no longer held
    /// its indexed entry.
    suspect: RefCell<BTreeSet<PathBuf>>,
    /// Owning logs a writer has used in this process (each read in full first).
    writer_opened: BTreeSet<PathBuf>,
    /// When a refresh, and a verifier pass, last ended (milliseconds since the epoch).
    refreshed_ms: Option<i64>,
    verified_ms: Option<i64>,
}
fn now_ms() -> i64 {
    std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map(|d| d.as_millis() as i64).unwrap_or(0)
}
static INDEXES: Mutex<Vec<(PathBuf, ProjectIndex)>> = Mutex::new(Vec::new());
static LOG_REVISION: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(1);
fn next_revision() -> u64 { LOG_REVISION.fetch_add(1, std::sync::atomic::Ordering::Relaxed) }
static ACT_EPOCH: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(1);
fn next_act_epoch() -> u64 { ACT_EPOCH.fetch_add(1, std::sync::atomic::Ordering::Relaxed) }
static VERIFIER: std::sync::Once = std::sync::Once::new();

/// Refreshes `root`'s index and gives it to `f`, under the index lock.
pub(crate) fn with_index<R>(root: &Path, f: impl FnOnce(&ProjectIndex) -> R) -> R {
    with_index_for(root, None, f)
}
/// As [`with_index`], for a writer about to use its owning `log`: the first
/// time in this process, that log is read in full.
pub(crate) fn with_index_writing<R>(root: &Path, log: &Path, f: impl FnOnce(&ProjectIndex) -> R) -> R {
    with_index_for(root, Some(log), f)
}
fn with_index_for<R>(root: &Path, log: Option<&Path>, f: impl FnOnce(&ProjectIndex) -> R) -> R {
    start_verifier();
    let mut all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
    let position = all.iter().position(|(r, _)| r == root);
    let (key, mut index) = match position { Some(i) => all.remove(i), None => (root.to_path_buf(), ProjectIndex::default()) };
    if let Some(log) = log {
        if index.writer_opened.insert(log.to_path_buf()) {
            index.suspect.borrow_mut().insert(log.to_path_buf());
        }
    }
    index.refresh(root);
    index.refreshed_ms = Some(now_ms());
    let result = f(&index);
    all.insert(0, (key, index));
    all.truncate(INDEXED_PROJECTS);
    result
}
/// Release the retained process-owned caches on the App's normal exit.
/// A crash may leave disposable files; never sweep unowned/replaced leaves.
pub(crate) fn close_all() {
    INDEXES.lock().unwrap_or_else(|p| p.into_inner()).clear();
}
/// How many log names the host status carries for each chain state.
pub(crate) const STATUS_NAMES: usize = 5;
/// RS §13.8 Tamper-evidence, for the host's status (polled every second):
/// bounded counts of the logs by chain state, and at most [`STATUS_NAMES`]
/// names of logs with a broken chain or unchained (legacy) lines. Only the
/// cached index is looked at, under its lock; nothing is read or refreshed
/// here, so it shows the index as its last reader, writer or verifier pass
/// left it. Heads come on demand ([`chain_heads`]). Signed checkpoints wait
/// for App signing (OI-011).
pub(crate) fn chain_status(root: Option<&Path>) -> Value {
    let signed = "not written: signed checkpoints wait for App signing (OI-011)";
    let Some(root) = root else { return serde_json::json!({"state":"no project open","signedCheckpoints":signed}) };
    let all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
    let Some((_, ix)) = all.iter().find(|(r, _)| r == root) else {
        return serde_json::json!({"state":"not read yet in this process","signedCheckpoints":signed});
    };
    let (mut chained, mut legacy, mut broken) = (0usize, 0usize, 0usize);
    let (mut broken_logs, mut legacy_logs) = (Vec::new(), Vec::new());
    for (path, log) in &ix.logs {
        let name = || path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        if log.limits().any(|l| l.contains("chain broken")) {
            broken += 1;
            if broken_logs.len() < STATUS_NAMES { broken_logs.push(name()); }
        }
        if log.chain.unchained > 0 {
            legacy += 1;
            if legacy_logs.len() < STATUS_NAMES { legacy_logs.push(name()); }
        }
        if log.chain.linked { chained += 1; }
    }
    let at = |ms: Option<i64>| ms.map(crate::util::rfc3339_from_ms);
    serde_json::json!({"state":"as the records index last read it","readAt":at(ix.refreshed_ms),"verifiedAt":at(ix.verified_ms),
        "discoveryLimit":ix.discovery_error,"verifierEverySeconds":verify_interval(),"method":crate::record_lines::LINE_METHOD,"logs":ix.logs.len(),
        "chained":chained,"legacy":legacy,"broken":broken,"brokenLogs":broken_logs,"legacyLogs":legacy_logs,
        "heads":"on demand (host command records_chain_heads)","signedCheckpoints":signed})
}
/// Each log's chain head and the chain limits, as the bounded index reads
/// them now (refreshed): on demand, for the person and later for export.
pub(crate) fn chain_heads(root: &Path) -> Value {
    with_index(root, |ix| serde_json::json!({"method":crate::record_lines::LINE_METHOD,"logs":ix.chains(),
        "broken":ix.limits().into_iter().filter(|l| l.contains("chain broken")).collect::<Vec<_>>(),"notes":ix.notes(),
        "signedCheckpoints":"not written: signed checkpoints wait for App signing (OI-011)"}))
}
/// Seconds between verifier passes (`CHIRALITY_RECORDS_VERIFY_SECS`).
fn verify_interval() -> u64 {
    std::env::var("CHIRALITY_RECORDS_VERIFY_SECS").ok().and_then(|s| s.parse().ok()).unwrap_or(VERIFY_INTERVAL).max(1)
}
fn start_verifier() {
    VERIFIER.call_once(|| {
        let every = verify_interval();
        let _ = std::thread::Builder::new().name("records-index-verifier".into()).spawn(move || loop {
            std::thread::sleep(std::time::Duration::from_secs(every));
            let roots: Vec<PathBuf> = INDEXES.lock().unwrap_or_else(|p| p.into_inner()).iter().map(|(r, _)| r.clone()).collect();
            for root in roots { verify(&root); }
        });
    });
}
/// One full verification pass of `root`'s index, outside the index lock:
/// every directory listed again and every log read again in full. A log whose
/// stamp is unchanged since this pass read it, but whose indexed state differs
/// from the full read, is replaced. Returns how many logs were replaced.
#[cfg(test)]
thread_local! { static VERIFY_READ_HOOK: RefCell<Option<Box<dyn FnOnce()>>> = RefCell::new(None); }
pub(crate) fn verify(root: &Path) -> usize {
    // Capture the index before discovery too: a reader's newer discovery
    // error or tree must not be overwritten by this pass's older listing.
    let (generation, discovery_revision, old_logs) = {
        let all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
        let Some((_, index)) = all.iter().find(|(r, _)| r == root) else { return 0 };
        (index.generation, index.discovery_revision, index.logs.clone())
    };
    let (paths, dirs, error) = discover_tree(root, &Dirs::new());
    let found: BTreeSet<_> = paths.iter().cloned().collect();
    let (snapshots, gone) = {
        let mut all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
        let Some((_, index)) = all.iter_mut().find(|(r, _)| r == root) else { return 0 };
        if index.generation != generation { return 0; }
        if let Some(error) = error {
            if index.discovery_revision == discovery_revision {
                index.discovery_error = Some(error); index.discovery_revision = next_revision();
                index.verified_ms = Some(now_ms());
            }
            return 0;
        }
        let gone: Vec<_> = old_logs.iter().filter(|(p, _)| !found.contains(*p)).map(|(p, s)| (p.clone(), s.revision)).collect();
        let snapshots: Vec<_> = paths.into_iter().map(|path| {
            let old = old_logs.get(&path).cloned();
            let number = old.as_ref().map(|s| s.number).unwrap_or_else(|| { index.next_number += 1; index.next_number });
            (path, number, old)
        }).collect();
        (snapshots, gone)
    };
    // This database is new and process-owned. It is not loaded from a foreign
    // cache; every staged position comes from the full authoritative read.
    let mut staged = query::QueryDb::open(root).ok();
    let mut replaced = 0;
    for (path, number, snapshot) in snapshots {
        let stamp = stamp_of(&path);
        let mut cache_ok = staged.as_ref().is_some_and(|db| db.begin_log(number, 0).is_ok());
        let mut fresh = read_state(&path, stamp, number, None, snapshot.as_ref().map(|s| s.prefix_end), &mut |line| {
            #[cfg(test)]
            VERIFY_READ_HOOK.with(|h| { if let Some(hook) = h.borrow_mut().take() { hook(); } });
            if cache_ok && staged.as_ref().is_some_and(|db| db.insert(number, &line).is_err()) { cache_ok = false; }
        });
        if fresh.limits().any(|l| l.starts_with("incomplete record:")) {
            if let Some(db) = &staged { if db.clear_log(number).is_err() { cache_ok = false; } }
        }
        if let Some(db) = &mut staged { if db.finish_log(cache_ok).is_err() { cache_ok = false; } }
        let mut all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
        let Some((_, index)) = all.iter_mut().find(|(r, _)| r == root) else { return replaced };
        if index.generation != generation || stamp_of(&path) != stamp { continue; }
        let current = index.logs.get(&path);
        // A reader/writer/rebuild that changed this log while the pass was
        // reading it wins. A reserved number is never applied to its successor.
        if current.map(|s| s.revision) != snapshot.as_ref().map(|s| s.revision) { continue; }
        if current.is_some_and(|s| s.stamp == stamp && s.reading() == fresh.reading()) { continue; }
        let from = snapshot.as_ref().filter(|s| fresh.prefix_proof.as_deref() == Some(&format!("{:x}", s.prefix_digest.clone().finalize())))
            .map_or(0, |s| s.prefix_end);
        let touched_before = snapshot.as_ref().is_some_and(|s| s.has_act || index.touches_acts(number, from));
        // SQL copies positions only. No JSON/schema/source parsing occurs
        // under INDEXES, and a proved unchanged prefix is not recopied.
        let copied = cache_ok && match (&mut index.db, &staged) {
            (Some(main), Some(staged)) => main.copy_log(staged, number, from, || stamp_of(&path) == stamp).is_ok(),
            _ => false,
        };
        if !copied { index.cache_fault.set(true); index.db = None; }
        let touches = touched_before || fresh.has_act || index.touches_acts(number, from);
        if touches { index.act_epoch = next_act_epoch(); }
        fresh.revision = next_revision();
        index.numbers.insert(number, path.clone());
        index.logs.insert(path, fresh);
        replaced += 1;
    }
    let mut all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
    if let Some((_, index)) = all.iter_mut().find(|(r, _)| r == root) {
        if index.generation == generation {
            for (path, revision) in gone {
                // Incomplete discovery never reaches here. A recreated leaf
                // is not proved absent by the earlier complete listing.
                if index.logs.get(&path).is_some_and(|s| s.revision == revision)
                    && std::fs::symlink_metadata(&path).is_err_and(|e| e.kind() == std::io::ErrorKind::NotFound) {
                    if let Some(old) = index.logs.remove(&path) {
                        if old.has_act || index.touches_acts(old.number, 0) { index.act_epoch = next_act_epoch(); }
                        if let Some(db) = &mut index.db { if db.remove(old.number).is_err() { index.cache_fault.set(true); index.db = None; } }
                        index.numbers.remove(&old.number);
                        replaced += 1;
                    }
                }
            }
            if index.discovery_revision == discovery_revision && index.logs.keys().all(|p| found.contains(p)) {
                if index.dirs != dirs || index.discovery_error.is_some() { index.discovery_revision = next_revision(); }
                index.dirs = dirs;
                index.discovery_error = None;
            }
            index.verified_ms = Some(now_ms());
        }
    }
    replaced
}

fn act_kind(v: &Value) -> bool {
    matches!(v["kind"].as_str(), Some("human_act" | "act_declined")) || v.get("corrects").is_some()
}
fn stamp_of(path: &Path) -> Option<Stamp> {
    match std::fs::symlink_metadata(path) {
        Ok(m) if m.file_type().is_symlink() => None,
        Ok(m) => Some(Stamp::of(&m)),
        Err(_) => None,
    }
}

impl ProjectIndex {
    /// The limits that leave the set incomplete: discovery, each log's
    /// unreadable, invalid or out-of-sequence lines, and duplicate identities.
    pub(crate) fn limits(&self) -> Vec<String> {
        let mut out: Vec<String> = self.discovery_error.iter().cloned().collect();
        for log in self.logs.values() { out.extend(log.limits().cloned()); }
        let duplicate = self.db.as_ref().filter(|d| d.unchanged()).and_then(|d| d.duplicates().ok());
        if let Some(duplicate) = duplicate { out.extend(duplicate); }
        else {
            self.cache_fault.set(true);
            let mut ids = HashMap::<String, usize>::new();
            let result = self.source_lines(&mut |_, l| { if let Some(id) = l.id { *ids.entry(id).or_default() += 1; } Ok(()) });
            for (id, n) in ids { for _ in 1..n { out.push(format!("duplicate record identity: {id}")); } }
            if let Err(e) = result { if !out.contains(&e) { out.push(e); } }
        }
        out
    }
    /// Each log's torn final line (a partial, never an entry; RS §14.2 R-2).
    pub(crate) fn partials(&self) -> Vec<String> { self.logs.values().filter_map(|l| l.partial.clone()).collect() }
    /// Each log's chain as the index last read it (RS §13.8 Tamper-evidence):
    /// its head (the identity of its last link line), lines and unchained lines.
    pub(crate) fn chains(&self) -> Vec<Value> {
        self.logs.iter().map(|(path, log)| serde_json::json!({"log":path.display().to_string(),"head":log.chain.last,"lines":log.chain.lines,
            "linked":log.chain.linked,"unchained":log.chain.unchained})).collect()
    }
    /// Limits that do not make the set incomplete (RS §13.8): each log's
    /// unchained (legacy) lines, and torn lines W-0 named (not chain links).
    pub(crate) fn notes(&self) -> Vec<String> {
        let mut out = Vec::new();
        for (path, log) in &self.logs {
            out.extend(log.prefix_notes.iter().chain(&log.tail_notes).cloned());
            out.extend(log.chain.unchained_note(&path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default()));
        }
        out
    }
    pub(crate) fn discovery_failed(&self) -> bool { self.discovery_error.is_some() }
    /// Whether a readable entry holds `id`.
    pub(crate) fn holds(&self, id: &str) -> bool {
        if let Some(found) = self.db.as_ref().filter(|d| d.unchanged()).and_then(|d| d.holds(id).ok()) { return found; }
        self.cache_fault.set(true);
        let mut found = false;
        // If source discovery/read fails, absence is not established. Fail
        // closed for an identity guard, while ordinary reads expose the error.
        self.source_lines(&mut |_, l| { found |= l.id.as_deref() == Some(id); Ok(()) }).is_err() || found
    }
    /// Every readable entry holding `id`, reread from its authoritative log.
    pub(crate) fn entries_with(&self, id: &str) -> Result<Vec<Value>, String> {
        self.selected("WHERE id=?", Some(id), |l| l.id.as_deref() == Some(id))
    }
    /// Every readable W-2 limit naming `subject`, reread and checked.
    pub(crate) fn late_limits_for(&self, subject: &str) -> Result<Vec<Value>, String> {
        self.selected("WHERE late_subject=?", Some(subject), |l| l.late_subject.as_deref() == Some(subject))
    }
    /// The owning log's state: its limits, its torn tail and its next `seq`.
    pub(crate) fn own(&self, log: &Path) -> Option<OwnLog> {
        self.logs.get(log).map(|s| OwnLog {
            limits: s.limits().cloned().collect(), partial: s.partial.is_some(),
            next_seq: s.max_seq.checked_add(1), complete_end: s.complete_end,
            complete_lines: if s.complete_end > 0 { s.prefix_lines + 1 } else { 0 },
            chain_last: s.chain.last.clone(),
        })

    }
    pub(crate) fn act_epoch(&self) -> u64 { self.act_epoch }
    /// RS §14.2 R-1…R-6 claims for the act read: every act record (or
    /// correction), every target a correction names, and every entry sharing
    /// an identity with one of those, read again from their logs and checked.
    pub(crate) fn act_claims(&self) -> Result<Vec<Value>, String> {
        let mut claims = Vec::new();
        let mut file = None;
        let mut read = |number: u32, line: Line, claims: &mut Vec<Value>| -> Result<(), String> {
            let path = self.numbers.get(&number).ok_or("index log no longer discovered")?;
            let record = self.read_line(path, &line, &mut file)?;
            claims.push(json!({"source":{"log":path.to_string_lossy(),"seq":record["seq"]},"record":record}));
            Ok(())
        };
        if let Some(db) = self.db.as_ref().filter(|d| d.unchanged()) {
            let result = db.lines("WHERE act=1 OR id IN(SELECT id FROM entries WHERE act=1 UNION SELECT corrects FROM entries WHERE act=1 AND corrects IS NOT NULL)", None, |n, l| read(n, l, &mut claims));
            if result.is_ok() { return Ok(claims); }
            self.cache_fault.set(true);
            // A source discrepancy is reported now, then rebuilt on refresh.
            if !self.suspect.borrow().is_empty() { return result.map(|_| claims); }
            claims.clear();
        }
        self.cache_fault.set(true);
        let mut wanted = BTreeSet::new();
        self.source_lines(&mut |_, line| { if line.act { wanted.extend(line.id); wanted.extend(line.corrects); } Ok(()) })?;
        self.source_lines(&mut |number, line| {
            if line.act || line.id.as_ref().is_some_and(|id| wanted.contains(id)) { read(number, line, &mut claims)?; }
            Ok(())
        })?;
        Ok(claims)
    }
    /// Current source revision for a consumer retaining a validated log read.
    pub(crate) fn log_revision(&self, path: &Path) -> Option<u64> { self.logs.get(path).map(|s|s.revision) }
    /// One discovered log's entries, through the same checked source-line
    /// reader as act claims. A failed cache query never establishes absence.
    pub(crate) fn entries_in_log(&self, path: &Path) -> Result<Vec<Value>,String> {
        let number=self.logs.get(path).ok_or("record log no longer discovered")?.number;
        let mut out=Vec::new();let mut file=None;
        let mut read=|n:u32,line:Line| { if n==number {out.push(self.read_line(path,&line,&mut file)?);} Ok(()) };
        if let Some(db)=self.db.as_ref().filter(|d|d.unchanged()) {
            let result=db.lines("WHERE log=?",Some(&number.to_string()),&mut read);
            if result.is_ok(){return Ok(out);}
            self.cache_fault.set(true);
            if !self.suspect.borrow().is_empty(){return result.map(|_|out);}
        }
        out.clear();self.cache_fault.set(true);
        self.source_lines(&mut |n,line|{if n==number{out.push(self.read_line(path,&line,&mut file)?);}Ok(())})?;
        Ok(out)
    }
    /// Every discovered log (sorted).
    pub(crate) fn paths(&self) -> Vec<PathBuf> { self.logs.keys().cloned().collect() }

    fn selected(&self, predicate: &str, value: Option<&str>, matches: impl Fn(&Line) -> bool) -> Result<Vec<Value>, String> {
        let mut out = Vec::new();
        let mut file = None;
        let mut read = |number: u32, line: Line| -> Result<(), String> {
            let path = self.numbers.get(&number).ok_or("index log no longer discovered")?;
            out.push(self.read_line(path, &line, &mut file)?); Ok(())
        };
        if let Some(db) = self.db.as_ref().filter(|d| d.unchanged()) {
            let result = db.lines(predicate, value, &mut read);
            if result.is_ok() { return Ok(out); }
            self.cache_fault.set(true);
            if !self.suspect.borrow().is_empty() { return result.map(|_| out); }
        }
        out.clear();
        self.cache_fault.set(true);
        self.source_lines(&mut |number, line| {
            if matches(&line) {
                let path = self.numbers.get(&number).ok_or("index log no longer discovered")?;
                out.push(self.read_line(path, &line, &mut file)?);
            }
            Ok(())
        })?;
        Ok(out)
    }
    /// Cache failure fallback: stream and validate sources, keeping only the
    /// selected result. Never return SQLite bodies or interpret absence from
    /// a failed query as absence from the logs.
    fn source_lines(&self, each: &mut dyn FnMut(u32, Line) -> Result<(), String>) -> Result<(), String> {
        if let Some(error) = &self.discovery_error { return Err(error.clone()); }
        for (path, old) in &self.logs {
            let mut error = None;
            let state = read_state(path, stamp_of(path), old.number, None, None, &mut |line| {
                if error.is_none() { error = each(old.number, line).err(); }
            });
            if let Some(error) = error { return Err(error); }
            // Existing semantic limits are reported by limits(); an unreadable
            // file must also prevent a fallback from establishing absence.
            if state.limits().any(|l| l.starts_with("incomplete record:")) { return Err(state.limits().cloned().collect::<Vec<_>>().join("; ")); }
        }
        Ok(())
    }
    fn read_line(&self, path: &Path, line: &Line, opened: &mut Option<(PathBuf, std::fs::File)>) -> Result<Value, String> {
        use std::io::{Read, Seek, SeekFrom};
        let failed = |why: String| {
            self.suspect.borrow_mut().insert(path.to_path_buf());
            Err(format!("{}: {why}; the log is read again in full", path.display()))
        };
        // Query ordering groups positions by log: keep one source open, with
        // no descriptor or positions set growing with the number of entries.
        if opened.as_ref().is_none_or(|(p, _)| p != path) {
            let f = match open_log(path) { Ok(f) => f, Err(e) => return failed(e.to_string()) };
            *opened = Some((path.to_path_buf(), f));
        }
        let f = &mut opened.as_mut().expect("opened log").1;
        // A path replaced while a query is running cannot silently keep reading
        // an old descriptor as if it were still the discovered owning file.
        if f.metadata().ok().map(|m| Stamp::of(&m)) != stamp_of(path) { return failed("the owning log changed while it was read".into()); }
        let mut b = vec![0; line.len];
        if let Err(e) = f.seek(SeekFrom::Start(line.offset)).and_then(|_| f.read_exact(&mut b)) { return failed(format!("the entry at byte {} is no longer there ({e})", line.offset)); }
        if crate::record_lines::line_identity(&b) != line.digest { return failed(format!("the line at byte {} no longer holds its indexed bytes", line.offset)); }
        let decoded = crate::schema_validation::bundled().and_then(|val| crate::record_lines::decode_line(&b, val).map_err(|e| format!("{e:?}")));
        let entries = match decoded { Ok((entries, _)) => entries, Err(e) => return failed(format!("the line at byte {} no longer reads as written ({e})", line.offset)) };
        let Some(v) = entries.into_iter().nth(line.member.unwrap_or(0)) else { return failed(format!("the group at byte {} no longer holds its entry", line.offset)); };
        if v["recordId"].as_str() != line.id.as_deref() || v["seq"].as_u64() != Some(line.seq) { return failed(format!("the entry at byte {} no longer holds the indexed identity and seq", line.offset)); }
        Ok(v)
    }

    fn refresh(&mut self, root: &Path) {
        self.root = root.to_path_buf();
        // Deletion, replacement, unexpected writes and query errors invalidate
        // the whole derivative cache. New process/index instances always rebuild.
        if self.cache_fault.replace(false) || self.db.as_ref().is_none_or(|d| !d.unchanged()) {
            self.db = query::QueryDb::open(root).ok();
            self.logs.clear(); self.numbers.clear(); self.next_number = 0;
            self.act_epoch = next_act_epoch();
            self.generation = next_revision();
        }
        let (paths, dirs, error) = discover_tree(root, &self.dirs);
        if self.discovery_error != error || (error.is_none() && self.dirs != dirs) { self.discovery_revision = next_revision(); }
        if error.is_none() { self.dirs = dirs; }
        self.discovery_error = error;
        let found: BTreeSet<PathBuf> = paths.into_iter().collect();
        let gone: Vec<PathBuf> = self.logs.keys().filter(|p| !found.contains(*p)).cloned().collect();
        for path in gone {
            if let Some(old) = self.logs.remove(&path) {
                if old.has_act || self.touches_acts(old.number, 0) { self.act_epoch = next_act_epoch(); }
                if let Some(db) = &mut self.db { if db.remove(old.number).is_err() { self.cache_fault.set(true); } }
                self.numbers.remove(&old.number);
            }
        }
        for path in found { self.refresh_log(&path); }
        // A partially written/broken SQLite cache cannot establish membership.
        // Source-scan fallback covers this same request, rebuild on the next.
        if self.cache_fault.get() { self.db = None; }
    }
    fn touches_acts(&self, number: u32, from: u64) -> bool { self.db.as_ref().and_then(|d| d.touches_acts(number, from).ok()).unwrap_or(true) }
    fn refresh_log(&mut self, path: &Path) {
        let stamp = stamp_of(path);
        let old = self.logs.get(path).cloned();
        let suspect = self.suspect.borrow_mut().remove(path);
        if let (Some(s), Some(o)) = (stamp, &old) {
            if o.stamp == Some(s) && !suspect { return; }
        }
        // Only grown (same file, larger), with the bytes before the last
        // complete line unchanged: read from that line. Otherwise in full.
        let incremental = !suspect && match (stamp, &old) {
            (Some(s), Some(o)) => o.stamp.is_some_and(|os| os.dev == s.dev && os.ino == s.ino && s.size > os.size)
                && read_at(path, o.prefix_end.saturating_sub(GUARD), (o.prefix_end - o.prefix_end.saturating_sub(GUARD)) as usize).is_some_and(|b| b == o.guard),
            _ => false,
        };
        let number = match &old { Some(o) => o.number, None => { self.next_number += 1; self.numbers.insert(self.next_number, path.to_path_buf()); self.next_number } };
        let from = if incremental { old.as_ref().map_or(0, |o| o.prefix_end) } else { 0 };
        let touched_before = old.as_ref().is_some_and(|o| o.has_act || self.touches_acts(number, from));
        let mut cache_ok = self.db.as_ref().is_some_and(|db| db.begin_log(number, from).is_ok());
        let mut new = read_state(path, stamp, number, if incremental { old.clone() } else { None }, None, &mut |line| {
            if cache_ok && self.db.as_ref().is_some_and(|db| db.insert(number, &line).is_err()) { cache_ok = false; }
        });
        if new.limits().any(|l| l.starts_with("incomplete record:")) {
            // An I/O failure is a source limit, not a cache failure. Discard
            // every position from this failed full/incremental read; keep
            // indexing other sources so ordinary incomplete-set behavior stays.
            if let Some(db) = &self.db { if db.clear_log(number).is_err() { cache_ok = false; } }
        }
        if let Some(db) = &mut self.db { if db.finish_log(cache_ok).is_err() { cache_ok = false; } }
        if !cache_ok { self.cache_fault.set(true); }
        let touches = touched_before || new.has_act || self.touches_acts(number, from);
        if touches { self.act_epoch = next_act_epoch(); }
        new.revision = next_revision();
        self.logs.insert(path.to_path_buf(), new);
    }

}

/// `storage::discover`'s walk; a directory whose stamp equals its entry in
/// `cached` is not listed again. Returns the logs, the directories as listed
/// now, and a discovery failure.
fn discover_tree(root: &Path, cached: &Dirs) -> (Vec<PathBuf>, Dirs, Option<String>) {
    let mut out = Vec::new();
    let mut dirs = Dirs::new();
    let fail = |e: String| (vec![], Dirs::new(), Some(e));
    let sources = match crate::storage::sources(root) { Ok(s) => s, Err(e) => return fail(e) };
    for dir in &sources.walk {
        if let Err(e) = crate::storage::check_path(dir) { return fail(e); }
    }
    let mut todo = sources.walk.clone();
    while let Some(dir) = todo.pop() {
        let meta = match std::fs::symlink_metadata(&dir) {
            Ok(m) => m,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => continue,
            Err(e) => return fail(format!("incomplete record discovery: {}: {e}", dir.display())),
        };
        if meta.file_type().is_symlink() { return fail(format!("owning path contains symlink: {}", dir.display())); }
        let stamp = Stamp::of(&meta);
        let children = match cached.get(&dir) {
            Some((s, c)) if *s == stamp => c.clone(),
            _ => {
                let rd = match std::fs::read_dir(&dir) {
                    Ok(rd) => rd,
                    Err(e) => return fail(format!("incomplete record discovery: {}: {e}", dir.display())),
                };
                let mut children = Vec::new();
                for entry in rd {
                    let entry = match entry { Ok(e) => e, Err(e) => return fail(e.to_string()) };
                    let path = entry.path();
                    let kind = match std::fs::symlink_metadata(&path) { Ok(m) => m.file_type(), Err(e) => return fail(e.to_string()) };
                    if kind.is_symlink() { return fail(format!("owning path contains symlink: {}", path.display())); }
                    if kind.is_dir() { children.push((path, true)); }
                    else if path.extension().is_some_and(|e| e == "jsonl") { children.push((path, false)); }
                }
                children
            }
        };
        dirs.insert(dir.clone(), (stamp, children.clone()));
        for (path, is_dir) in children {
            if is_dir { todo.push(path); } else { out.push(path); }
        }
    }
    out.extend(sources.files);
    out.retain(|p| !sources.exclude.contains(p));
    out.sort();
    out.dedup();
    (out, dirs, None)
}

/// A log's state read from disk: from `from`'s last complete line when given
/// (the log only grew), or in full. Lines are read on their bytes, so a line
/// torn inside a character is still a partial (or, named by W-0, kept unread).
fn read_state(path: &Path, stamp: Option<Stamp>, number: u32, from: Option<LogState>, proof_at: Option<u64>, each: &mut dyn FnMut(Line)) -> LogState {
    use std::io::{BufReader, Read, Seek, SeekFrom};
    let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let mut state = from.unwrap_or(LogState { number, ..LogState::default() });
    state.number = number; state.stamp = stamp;
    state.tail_limits.clear(); state.tail_notes.clear(); state.partial = None;
    state.max_seq = state.prefix_max_seq; state.has_act = state.prefix_has_act; state.prefix_proof = None;
    // A refused source is not a successfully observed stamp. Retrying it on
    // refresh is essential when the same owning file becomes readable again.
    let failure = |e: String| LogState { number, stamp: None, tail_limits: vec![format!("incomplete record: {}: {e}", path.display())], ..LogState::default() };
    let expected = match stamp {
        Some(stamp) => stamp,
        None => return failure("the owning log stamp could not be read".into()),
    };
    let mut file = match open_log(path) { Ok(f) => f, Err(e) => return failure(e.to_string()) };
    let opened = match file.metadata() { Ok(m) => Stamp::of(&m), Err(e) => return failure(e.to_string()) };
    if opened != expected {
        return failure("the owning log changed before it was opened".into());
    }
    if let Err(e) = file.seek(SeekFrom::Start(state.prefix_end)) { return failure(e.to_string()); }
    let mut held: Option<crate::record_lines::ParsedLine> = None;
    let mut count = 0usize;
    let mut digest = state.prefix_digest.clone();
    let mut take = |state: &mut LogState, line: crate::record_lines::ParsedLine, into_prefix: bool| {
        if proof_at == Some(line.offset) { state.prefix_proof = Some(format!("{:x}", digest.clone().finalize())); }
        digest.update(line.digest.as_bytes());
        let grouped = line.entries.len() > 1;
        for (k, v) in line.entries.iter().enumerate() {
            let l = Line { id:v["recordId"].as_str().map(str::to_owned), offset:line.offset, len:line.len, seq:v["seq"].as_u64().unwrap_or(0), act:act_kind(v), corrects:v["corrects"].as_str().map(str::to_owned),
                late_subject:(v["kind"] == "evidence_limit" && v["body"]["label"] == "record write failed").then(|| v["body"]["subjectRef"].as_str().map(str::to_owned)).flatten(), member:grouped.then_some(k), digest:line.digest.clone() };
            state.max_seq = state.max_seq.max(l.seq); state.has_act |= l.act; each(l);
        }
        if into_prefix {
            state.prefix_max_seq = state.max_seq; state.prefix_has_act = state.has_act; state.prefix_digest = digest.clone();
            state.prefix_limits.extend(line.limits); state.prefix_notes.extend(line.notes);
        } else { state.tail_limits.extend(line.limits); state.tail_notes.extend(line.notes); }
    };
    let parsed = crate::record_lines::parse_reader(BufReader::new(&mut file), &name, state.prefix_lines, state.prefix_end, state.prefix_seq.max(1), state.prefix_chain.clone(), &mut |line| {
        count += 1;
        if let Some(before) = held.replace(line) { take(&mut state, before, true); }
    });
    let parsed = match parsed { Ok(p) => p, Err(e) => return failure(e.to_string()) };
    if let Some(line) = held {
        state.prefix_lines += count - 1; state.prefix_seq = line.expected_before; state.prefix_chain = line.chain_before.clone(); state.prefix_end = line.offset;
        take(&mut state, line, false);
    }
    state.complete_end = parsed.tail_offset;
    state.digest = format!("{:x}", digest.finalize());
    if proof_at == Some(state.complete_end) { state.prefix_proof = Some(state.digest.clone()); }
    state.chain = parsed.chain; state.partial = parsed.partial_tail;
    state.tail_limits.extend(crate::record_lines::links_removed(path, &name, &state.chain));
    let guard_from = state.prefix_end.saturating_sub(GUARD);
    let mut guard = vec![0; (state.prefix_end - guard_from) as usize];
    state.guard = file.seek(SeekFrom::Start(guard_from)).and_then(|_| file.read_exact(&mut guard)).map(|_| guard).unwrap_or_default();
    let after = match file.metadata() { Ok(m) => Stamp::of(&m), Err(e) => return failure(e.to_string()) };
    if after != expected || stamp_of(path) != Some(expected) {
        return failure("the owning log changed while it was read".into());
    }
    state
}
/// Open every component relative to a held directory without following links.
/// The final nonblocking descriptor must be a regular log, for both readers.
pub(crate) fn open_log(path: &Path) -> std::io::Result<std::fs::File> {
    open_node(path, false)
}
/// The same component-bound open, for a caller enumerating a held directory.
pub(crate) fn open_directory(path: &Path) -> std::io::Result<std::fs::File> {
    open_node(path, true)
}
fn open_node(path: &Path, directory: bool) -> std::io::Result<std::fs::File> {
    use std::os::fd::{AsRawFd, FromRawFd};
    use std::os::unix::ffi::OsStrExt;
    use std::os::unix::fs::OpenOptionsExt;
    crate::storage::check_path(path).map_err(std::io::Error::other)?;
    #[cfg(test)]
    log_open_hook(path, None);

    let mut components = Vec::new();
    for component in path.components() {
        match component {
            std::path::Component::RootDir => {},
            std::path::Component::Prefix(_) => return Err(std::io::Error::other("unsupported record path prefix")),
            other => components.push(other.as_os_str()),
        }
    }
    let leaf = components.pop();
    if leaf.is_none() && !directory { return Err(std::io::Error::other("record log has no leaf")); }
    let base = if path.is_absolute() { Path::new("/") } else { Path::new(".") };
    let mut parent = std::fs::OpenOptions::new().read(true)
        .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(base)?;
    let open_at = |parent: &std::fs::File, name: &std::ffi::OsStr, directory: bool| {
        let name = std::ffi::CString::new(name.as_bytes()).map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidInput, e))?;
        let flags = libc::O_RDONLY | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC
            | if directory { libc::O_DIRECTORY } else { 0 };
        let descriptor = unsafe { libc::openat(parent.as_raw_fd(), name.as_ptr(), flags) };
        if descriptor < 0 { Err(std::io::Error::last_os_error()) }
        else { Ok(unsafe { std::fs::File::from_raw_fd(descriptor) }) }
    };
    #[cfg(test)]
    let mut opened_path = base.to_owned();
    for component in components {
        parent = open_at(&parent, component, true)?;
        #[cfg(test)]
        {
            opened_path.push(component);
            log_open_hook(path, Some(&opened_path));
        }
    }
    let f = match leaf { Some(leaf) => open_at(&parent, leaf, directory)?, None => parent };
    let metadata = f.metadata()?;
    if directory && !metadata.is_dir() { return Err(std::io::Error::other("source folder is not a directory")); }
    if !directory && !metadata.is_file() { return Err(std::io::Error::other("record log is not a regular file")); }
    Ok(f)
}
#[cfg(test)]
type LogOpenHook = (PathBuf, Option<PathBuf>, usize, Box<dyn FnOnce()>);
#[cfg(test)]
thread_local! {
    static LOG_OPEN_HOOK: std::cell::RefCell<Option<LogOpenHook>> = const { std::cell::RefCell::new(None) };
}
#[cfg(test)]
pub(crate) struct LogOpenHookGuard;
#[cfg(test)]
impl Drop for LogOpenHookGuard {
    fn drop(&mut self) { LOG_OPEN_HOOK.with(|h| { h.borrow_mut().take(); }); }
}
#[cfg(test)]
pub(crate) fn log_open_hook_for_test(path: &Path, after_directory: Option<&Path>, skip_matching_opens: usize, hook: impl FnOnce() + 'static) -> LogOpenHookGuard {
    LOG_OPEN_HOOK.with(|h| *h.borrow_mut() = Some((path.to_owned(), after_directory.map(Path::to_owned), skip_matching_opens, Box::new(hook))));
    LogOpenHookGuard
}
#[cfg(test)]
fn log_open_hook(path: &Path, after_directory: Option<&Path>) {
    let hook = LOG_OPEN_HOOK.with(|h| {
        let mut held = h.borrow_mut();
        if let Some((p, dir, skip, _)) = held.as_mut() {
            if p == path && dir.as_deref() == after_directory {
                if *skip > 0 { *skip -= 1; } else { return held.take().map(|h| h.3); }
            }
        }
        None
    });
    if let Some(hook) = hook { hook(); }
}
/// The owning log as the index reads it.
pub(crate) struct OwnLog {
    pub limits: Vec<String>,
    pub partial: bool,
    pub next_seq: Option<u64>,
    pub complete_end: u64,
    pub complete_lines: usize,
    /// The identity of its last link line (its chain head), if any.
    pub chain_last: Option<String>,
}

fn read_at(path: &Path, offset: u64, len: usize) -> Option<Vec<u8>> {
    use std::io::{Read, Seek, SeekFrom};
    let mut f = open_log(path).ok()?;
    f.seek(SeekFrom::Start(offset)).ok()?;
    let mut b = vec![0u8; len];
    f.read_exact(&mut b).ok()?;
    Some(b)
}

#[cfg(test)]
#[path = "records_index_tests.rs"]
mod tests;
