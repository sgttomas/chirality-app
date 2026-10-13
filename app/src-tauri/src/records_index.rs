//! A bounded, in-process index of one project's RS logs for the writer's
//! guards and the act read (RS §13.2 CC-ID, §13.7 Failures, §14.1 W-0/W-1,
//! §14.2 R-2/R-4/R-5). Not a store: the logs stay the only record, and the
//! index is rebuilt from them whenever they change.
//!
//! What it keeps for each discovered log: the file's identity and stamp
//! (device, inode, size, modification and change times), the readable
//! entries' record identities with their byte positions and `seq`, the limits
//! that leave the log incomplete (an unreadable or invalid line, a sequence
//! gap, a W-0 name that does not match its line), and a torn final line apart
//! (a partial, never an entry). Across logs it counts each identity, so a
//! duplicate is a limit as in `storage::read_all`. Memory grows linearly with
//! the total number of entries (one small record per entry: its identity,
//! position, `seq` and two optional references).
//!
//! How it stays correct:
//! - Each refresh walks the records tree again (a directory is listed again
//!   only when its own stamp changed; a symlink is refused as
//!   `storage::discover` refuses it) and takes every log's stamp. A log whose
//!   stamp is unchanged is not read.
//! - A log that only grew (same device and inode, a larger size), with the
//!   4 KiB before its last complete line unchanged, is read from that line
//!   on. Any other change (another inode, the same size, a shrink, a change
//!   before that point) reads the whole log again.
//! - A writer's first use of its owning log in this process reads that log
//!   in full.
//! - A background verifier (`verify`) re-lists every directory and re-reads
//!   every log in full, once every `VERIFY_INTERVAL` (60 s, or
//!   `CHIRALITY_RECORDS_VERIFY_SECS`), outside the index lock. A log that
//!   differs from its indexed state is replaced.
//! - A line read again from its stored position (entries by identity, the act
//!   read's claims) is parsed and validated again and must still hold the
//!   indexed identity and `seq`. Otherwise the read fails as incomplete, and
//!   that log is read in full at the next refresh.
//!
//! Remaining blind spot, stated: an in-place edit of a log's earlier bytes
//! made together with an append (so the log only grew), outside the kept
//! 4 KiB, is seen at the latest by the verifier's next pass: within
//! `VERIFY_INTERVAL` plus one pass, which takes about as long as one full
//! read of the project (2–5 s at 10,000 runs). The same bound applies to a
//! log added to a directory whose stamp did not change (a coarse-timestamp
//! file system). Before that, a guard may answer from the earlier bytes.
use serde_json::{json, Value};
use std::cell::RefCell;
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
struct Line { id: Option<String>, offset: u64, len: usize, seq: u64, act: bool, corrects: Option<String>, late_subject: Option<String>, member: Option<usize> }
#[derive(Clone, Default, PartialEq)]
struct LogState {
    /// This log's number in the index (identities name logs by number).
    number: u32,
    stamp: Option<Stamp>,
    /// Where the next read starts: the start of the last complete line.
    prefix_end: u64,
    prefix_lines: usize,
    prefix_seq: u64,
    prefix_limits: Vec<String>,
    prefix_entries: Vec<Line>,
    /// Up to GUARD bytes before `prefix_end`, as last read.
    guard: Vec<u8>,
    tail_limits: Vec<String>,
    tail_entries: Vec<Line>,
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
    fn entries(&self) -> impl Iterator<Item = &Line> { self.prefix_entries.iter().chain(&self.tail_entries) }
    fn limits(&self) -> impl Iterator<Item = &String> { self.prefix_limits.iter().chain(&self.tail_limits) }
    /// What a full read of the log establishes (positions, not how it was read).
    fn reading(&self) -> (Vec<&Line>, Vec<&String>, &Option<String>, &crate::record_lines::Chain) { (self.entries().collect(), self.limits().collect(), &self.partial, &self.chain) }
}
type Dirs = HashMap<PathBuf, (Stamp, Vec<(PathBuf, bool)>)>;
#[derive(Default)]
pub(crate) struct ProjectIndex {
    dirs: Dirs,
    logs: BTreeMap<PathBuf, LogState>,
    /// Each identity, with the number of every log holding it (once per entry).
    ids: HashMap<String, Vec<u32>>,
    act_ids: HashMap<String, u32>,
    /// Identities held more than once.
    duplicates: BTreeMap<String, usize>,
    numbers: HashMap<u32, PathBuf>,
    next_number: u32,
    discovery_error: Option<String>,
    /// Increased whenever the act-relevant entries may have changed.
    act_epoch: u64,
    /// Logs the next refresh reads in full: a line read again no longer held
    /// its indexed entry.
    suspect: RefCell<BTreeSet<PathBuf>>,
    /// Owning logs a writer has used in this process (each read in full first).
    writer_opened: BTreeSet<PathBuf>,
}
static INDEXES: Mutex<Vec<(PathBuf, ProjectIndex)>> = Mutex::new(Vec::new());
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
    let result = f(&index);
    all.insert(0, (key, index));
    all.truncate(INDEXED_PROJECTS);
    result
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
    serde_json::json!({"state":"as the records index last read it","method":crate::record_lines::LINE_METHOD,"logs":ix.logs.len(),
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
fn start_verifier() {
    VERIFIER.call_once(|| {
        let every = std::env::var("CHIRALITY_RECORDS_VERIFY_SECS").ok().and_then(|s| s.parse().ok()).unwrap_or(VERIFY_INTERVAL).max(1);
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
pub(crate) fn verify(root: &Path) -> usize {
    let (paths, dirs, error) = discover_tree(root, &Dirs::new());
    let numbers: Vec<(PathBuf, Option<u32>)> = {
        let all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
        let Some((_, index)) = all.iter().find(|(r, _)| r == root) else { return 0 };
        paths.iter().map(|p| (p.clone(), index.logs.get(p).map(|l| l.number))).collect()
    };
    if error.is_none() {
        let mut all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
        if let Some((_, index)) = all.iter_mut().find(|(r, _)| r == root) {
            index.dirs = dirs;
        }
    }
    let mut replaced = 0;
    for (path, number) in numbers {
        let Some(number) = number else { continue };
        let stamp = stamp_of(&path);
        let fresh = read_state(&path, stamp, number, None);
        let mut all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
        let Some((_, index)) = all.iter_mut().find(|(r, _)| r == root) else { return replaced };
        let Some(current) = index.logs.get(&path).cloned() else { continue };
        if current.stamp != stamp || stamp_of(&path) != stamp || current.reading() == fresh.reading() {
            continue;
        }
        index.install(&path, Some(current), fresh, false);
        replaced += 1;
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
        for (id, n) in &self.duplicates {
            for _ in 1..*n { out.push(format!("duplicate record identity: {id}")); }
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
    pub(crate) fn holds(&self, id: &str) -> bool { self.ids.contains_key(id) }
    /// Every readable entry holding `id`, read again from its log and checked.
    pub(crate) fn entries_with(&self, id: &str) -> Result<Vec<Value>, String> {
        let Some(numbers) = self.ids.get(id) else { return Ok(vec![]) };
        let numbers: BTreeSet<u32> = numbers.iter().copied().collect();
        let mut out = Vec::new();
        for path in numbers.iter().filter_map(|n| self.numbers.get(n)) {
            if let Some(log) = self.logs.get(path) {
                out.extend(self.read_lines(path, log.entries().filter(|l| l.id.as_deref() == Some(id)))?);
            }
        }
        Ok(out)
    }
    /// Every readable "record write failed" limit naming `subject` (W-2), read again and checked.
    pub(crate) fn late_limits_for(&self, subject: &str) -> Result<Vec<Value>, String> {
        let mut out = Vec::new();
        for (path, log) in &self.logs {
            out.extend(self.read_lines(path, log.entries().filter(|l| l.late_subject.as_deref() == Some(subject)))?);
        }
        Ok(out)
    }
    /// The owning log's state: its limits, its torn tail and its next `seq`.
    pub(crate) fn own(&self, log: &Path) -> Option<OwnLog> {
        self.logs.get(log).map(|s| OwnLog {
            limits: s.limits().cloned().collect(), partial: s.partial.is_some(),
            next_seq: s.entries().map(|l| l.seq).max().unwrap_or(0).checked_add(1), complete_end: s.complete_end,
            complete_lines: if s.complete_end > 0 { s.prefix_lines + 1 } else { 0 },
            chain_last: s.chain.last.clone(),
        })

    }
    pub(crate) fn act_epoch(&self) -> u64 { self.act_epoch }
    /// RS §14.2 R-1…R-6 claims for the act read: every act record (or
    /// correction), every target a correction names, and every entry sharing
    /// an identity with one of those, read again from their logs and checked.
    pub(crate) fn act_claims(&self) -> Result<Vec<Value>, String> {
        let mut wanted: BTreeSet<String> = BTreeSet::new();
        for log in self.logs.values() {
            for line in log.entries().filter(|l| l.act) {
                wanted.extend(line.id.clone());
                wanted.extend(line.corrects.clone());
            }
        }
        let mut claims = Vec::new();
        for (path, log) in &self.logs {
            for record in self.read_lines(path, log.entries().filter(|l| l.act || l.id.as_ref().is_some_and(|id| wanted.contains(id))))? {
                claims.push(json!({"source":{"log":path.to_string_lossy(),"seq":record["seq"]},"record":record}));
            }
        }
        Ok(claims)
    }
    /// Every discovered log (sorted).
    pub(crate) fn paths(&self) -> Vec<PathBuf> { self.logs.keys().cloned().collect() }

    /// The given entries of one log, read with one open (in log order). Each
    /// line is parsed and validated again (RS R-4) and must still hold the
    /// indexed identity and `seq`; otherwise the read fails, and the log is
    /// read in full at the next refresh.
    fn read_lines<'a>(&self, path: &Path, lines: impl Iterator<Item = &'a Line>) -> Result<Vec<Value>, String> {
        use std::io::{Read, Seek, SeekFrom};
        let mut lines = lines.peekable();
        if lines.peek().is_none() { return Ok(vec![]); }
        let failed = |why: String| {
            self.suspect.borrow_mut().insert(path.to_path_buf());
            Err(format!("{}: {why}; the log is read again in full", path.display()))
        };
        let mut f = match std::fs::File::open(path) { Ok(f) => f, Err(e) => return failed(e.to_string()) };
        let validator = crate::schema_validation::bundled();
        let mut out = Vec::new();
        for line in lines {
            let mut b = vec![0u8; line.len];
            if let Err(e) = f.seek(SeekFrom::Start(line.offset)).and_then(|_| f.read_exact(&mut b)) {
                return failed(format!("the entry at byte {} is no longer there ({e})", line.offset));
            }
            // The line decoded whole (an entry, or a group taken whole), then its entry.
            let decoded = match &validator {
                Ok(val) => crate::record_lines::decode_line(&b, val).map_err(|e| format!("{e:?}")),
                Err(e) => Err(e.clone()),
            };
            let entries = match decoded {
                Ok((entries, _)) => entries,
                Err(e) => return failed(format!("the line at byte {} no longer reads as written ({e})", line.offset)),
            };
            let Some(v) = entries.into_iter().nth(line.member.unwrap_or(0)) else {
                return failed(format!("the group at byte {} no longer holds its entry", line.offset));
            };

            if v["recordId"].as_str() != line.id.as_deref() || v["seq"].as_u64() != Some(line.seq) {
                return failed(format!("the entry at byte {} no longer holds the indexed identity and seq", line.offset));
            }
            out.push(v);
        }
        Ok(out)
    }

    fn refresh(&mut self, root: &Path) {
        let (paths, dirs, error) = discover_tree(root, &self.dirs);
        if error.is_none() { self.dirs = dirs; }
        self.discovery_error = error;
        let found: BTreeSet<PathBuf> = paths.into_iter().collect();
        let gone: Vec<PathBuf> = self.logs.keys().filter(|p| !found.contains(*p)).cloned().collect();
        for path in gone {
            if let Some(old) = self.logs.remove(&path) {
                self.count(old.number, old.entries(), -1);
                self.numbers.remove(&old.number);
                if old.entries().any(|l| l.act) { self.act_epoch += 1; }
            }
        }
        for path in found {
            self.refresh_log(&path);
        }
    }
    fn count<'a>(&mut self, number: u32, lines: impl Iterator<Item = &'a Line>, by: i64) {
        for line in lines {
            let Some(id) = line.id.clone() else { continue };
            let holders = self.ids.entry(id.clone()).or_default();
            if by > 0 {
                holders.push(number);
            } else if let Some(at) = holders.iter().position(|n| *n == number) {
                holders.swap_remove(at);
            }
            let held = holders.len();
            if held == 0 { self.ids.remove(&id); }
            if held > 1 { self.duplicates.insert(id.clone(), held); } else { self.duplicates.remove(&id); }
            if line.act {
                let n = self.act_ids.entry(id.clone()).or_insert(0);
                *n = (*n as i64 + by).max(0) as u32;
                if *n == 0 { self.act_ids.remove(&id); }
            }
        }
    }
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
        let new = read_state(path, stamp, number, if incremental { old.clone() } else { None });
        self.install(path, old, new, incremental);
    }
    /// Puts a log's new state in place, adjusting identity counts and the act epoch.
    fn install(&mut self, path: &Path, old: Option<LogState>, new: LogState, incremental: bool) {
        let number = new.number;
        if let Some(o) = &old {
            if incremental { self.count(number, o.tail_entries.iter(), -1); } else { self.count(number, o.entries(), -1); }
        }
        let had_act = old.as_ref().is_some_and(|o| o.entries().any(|l| l.act));
        let added: Vec<Line> = if incremental {
            let kept = old.as_ref().map_or(0, |o| o.prefix_entries.len());
            new.prefix_entries[kept..].iter().chain(&new.tail_entries).cloned().collect()
        } else {
            new.entries().cloned().collect()
        };
        // The act read is recomputed when a log holding act records changes, or
        // when a new entry shares an identity with one (a conflict to show).
        let touches_acts = had_act || new.entries().any(|l| l.act)
            || added.iter().any(|l| l.id.as_ref().is_some_and(|id| self.act_ids.contains_key(id)));
        if touches_acts { self.act_epoch += 1; }
        self.count(number, added.iter(), 1);
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
fn read_state(path: &Path, stamp: Option<Stamp>, number: u32, from: Option<LogState>) -> LogState {
    let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let mut state = from.unwrap_or(LogState { number, ..LogState::default() });
    state.number = number;
    state.stamp = stamp;
    state.tail_limits.clear();
    state.tail_entries.clear();
    state.tail_notes.clear();
    state.partial = None;
    let bytes = match std::fs::File::open(path).and_then(|mut f| {
        use std::io::{Read, Seek, SeekFrom};
        f.seek(SeekFrom::Start(state.prefix_end))?;
        let mut b = Vec::new();
        f.read_to_end(&mut b)?;
        Ok(b)
    }) {
        Ok(b) => b,
        Err(e) => return LogState { number, stamp, tail_limits: vec![format!("incomplete record: {}: {e}", path.display())], ..LogState::default() },
    };
    // R-2 as RS §13.8 reads it (one entry or one group per line, each line
    // linked to the one before), continued from the stable prefix.
    // Everything before the last complete line becomes the stable prefix: each
    // line is kept back until the next one shows it is not the last.
    let mut held: Option<crate::record_lines::ParsedLine> = None;
    let mut count = 0usize;
    let take = |state: &mut LogState, line: crate::record_lines::ParsedLine, into_prefix: bool| {
        let grouped = line.entries.len() > 1;
        let entries = line.entries.iter().enumerate().map(|(k, v)| Line {
            id: v["recordId"].as_str().map(str::to_owned), offset: line.offset, len: line.len, seq: v["seq"].as_u64().unwrap_or(0),
            act: act_kind(v), corrects: v["corrects"].as_str().map(str::to_owned),
            late_subject: (v["kind"] == "evidence_limit" && v["body"]["label"] == "record write failed").then(|| v["body"]["subjectRef"].as_str().map(str::to_owned)).flatten(),
            member: grouped.then_some(k),
        });
        if into_prefix {
            state.prefix_entries.extend(entries);
            state.prefix_limits.extend(line.limits);
            state.prefix_notes.extend(line.notes);
        } else {
            state.tail_entries.extend(entries);
            state.tail_limits.extend(line.limits);
            state.tail_notes.extend(line.notes);
        }
    };
    let parsed = {
        let state = &mut state;
        crate::record_lines::parse_with(&bytes, &name, state.prefix_lines, state.prefix_end, state.prefix_seq.max(1), state.prefix_chain.clone(), &mut |line| {
            count += 1;
            if let Some(before) = held.replace(line) {
                take(state, before, true);
            }
        })
    };
    let last = held.map(|line| {
        let kept = (line.offset, line.expected_before, line.chain_before.clone());
        take(&mut state, line, false);
        kept
    });
    if let Some((offset, expected_before, chain_before)) = last {
        state.prefix_lines += count - 1;
        // The expected seq and the chain where the last complete line starts.
        state.prefix_seq = expected_before;
        state.prefix_chain = chain_before;
        state.prefix_end = offset;
        state.complete_end = parsed.tail_offset;
    }
    state.chain = parsed.chain;
    state.partial = parsed.partial_tail;
    state.tail_limits.extend(crate::record_lines::links_removed(path, &name, &state.chain));
    let guard_from = state.prefix_end.saturating_sub(GUARD);
    state.guard = read_at(path, guard_from, (state.prefix_end - guard_from) as usize).unwrap_or_default();
    state
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
    let mut f = std::fs::File::open(path).ok()?;
    f.seek(SeekFrom::Start(offset)).ok()?;
    let mut b = vec![0u8; len];
    f.read_exact(&mut b).ok()?;
    Some(b)
}

#[cfg(test)]
#[path = "records_index_tests.rs"]
mod tests;
