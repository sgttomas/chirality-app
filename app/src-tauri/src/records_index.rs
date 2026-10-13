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
struct Line { id: Option<String>, offset: u64, len: usize, seq: u64, act: bool, corrects: Option<String>, late_subject: Option<String> }
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
}
impl LogState {
    fn entries(&self) -> impl Iterator<Item = &Line> { self.prefix_entries.iter().chain(&self.tail_entries) }
    fn limits(&self) -> impl Iterator<Item = &String> { self.prefix_limits.iter().chain(&self.tail_limits) }
    /// What a full read of the log establishes (positions, not how it was read).
    fn reading(&self) -> (Vec<&Line>, Vec<&String>, &Option<String>) { (self.entries().collect(), self.limits().collect(), &self.partial) }
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
            let Ok(v) = serde_json::from_slice::<Value>(b.strip_suffix(b"\r").unwrap_or(&b)) else {
                return failed(format!("the entry at byte {} no longer parses", line.offset));
            };
            if let Err(e) = validator.as_ref().map_err(|e| e.clone()).and_then(|val| val.validate(&v)) {
                return failed(format!("the entry at byte {} is no longer valid: {e}", line.offset));
            }
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
    let mut segments: Vec<(u64, &[u8])> = Vec::new();
    let mut at = 0usize;
    for part in bytes.split(|b| *b == b'\n') {
        segments.push((state.prefix_end + at as u64, part));
        at += part.len() + 1;
    }
    let tail = segments.pop().unwrap_or((state.prefix_end, b""));
    let complete_bytes = &bytes[..bytes.len() - tail.1.len()];
    let (recovered, mismatched) = crate::records::recovered_partial_lines(complete_bytes, state.prefix_lines);
    let mismatched: HashMap<usize, String> = mismatched.into_iter().collect();
    let validator = crate::schema_validation::bundled();
    let mut expected = state.prefix_seq.max(1);
    let mut results: Vec<(u64, Result<Option<Line>, String>, u64)> = Vec::new();
    for (i, (offset, raw)) in segments.iter().enumerate() {
        let n = state.prefix_lines + i;
        let before = expected;
        if let Some(m) = mismatched.get(&i) {
            results.push((*offset, Err(format!("{name}: {m}")), before));
        }
        let text = std::str::from_utf8(raw.strip_suffix(b"\r").unwrap_or(raw));
        let outcome = if recovered.contains(&i) || text.is_ok_and(|t| t.trim().is_empty()) {
            Ok(None)
        } else {
            match text.ok().and_then(|t| serde_json::from_str::<Value>(t).ok()) {
                Some(v) => match validator.as_ref().map_err(|e| e.clone()).and_then(|val| val.validate(&v)) {
                    Ok(()) => {
                        let seq = v["seq"].as_u64().unwrap_or(0);
                        let entry = Line { id: v["recordId"].as_str().map(str::to_owned), offset: *offset, len: raw.len(), seq, act: act_kind(&v), corrects: v["corrects"].as_str().map(str::to_owned),
                            late_subject: (v["kind"] == "evidence_limit" && v["body"]["label"] == "record write failed").then(|| v["body"]["subjectRef"].as_str().map(str::to_owned)).flatten() };
                        if seq != expected {
                            results.push((*offset, Err(format!("{name}: sequence incomplete/disagrees: expected {expected}, found {seq} at line {}", n + 1)), before));
                        }
                        expected = seq.checked_add(1).unwrap_or(seq);
                        Ok(Some(entry))
                    }
                    Err(e) => Err(format!("{name}: invalid line {}: {e}", n + 1)),
                },
                None => Err(format!("{name}: unreadable line {}", n + 1)),
            }
        };
        results.push((*offset, outcome, before));
    }
    // Everything before the last complete line becomes the stable prefix.
    let last_start = segments.last().map(|(o, _)| *o);
    for (offset, outcome, _) in results.iter() {
        let into_prefix = last_start.is_some_and(|s| *offset < s);
        match (outcome, into_prefix) {
            (Ok(Some(l)), true) => state.prefix_entries.push(l.clone()),
            (Ok(Some(l)), false) => state.tail_entries.push(l.clone()),
            (Err(e), true) => state.prefix_limits.push(e.clone()),
            (Err(e), false) => state.tail_limits.push(e.clone()),
            (Ok(None), _) => {}
        }
    }
    if let Some(start) = last_start {
        state.prefix_lines += segments.len() - 1;
        // The expected seq where the last complete line starts.
        state.prefix_seq = results.iter().find(|(o, _, _)| *o == start).map(|(_, _, b)| *b).unwrap_or(expected);
        state.prefix_end = start;
        state.complete_end = tail.0;
    }
    if !tail.1.is_empty() && !tail.1.iter().all(u8::is_ascii_whitespace) {
        state.partial = Some(format!("{name}: partial entry at end (not read)"));
    }
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
