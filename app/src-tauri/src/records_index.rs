//! A bounded, in-process index of one project's RS logs for the writer's
//! guards and the act read (RS §13.2 CC-ID, §13.7 Failures, §14.1 W-0/W-1,
//! §14.2 R-2/R-4/R-5). Not a store: the logs stay the only record, and the
//! index is rebuilt from them whenever they change.
//!
//! What it keeps for each discovered log: the file's identity and stamp
//! (device, inode, size, modification time), the readable entries' record
//! identities with their byte positions, the limits that leave the log
//! incomplete (an unreadable or invalid line, a sequence gap), and a torn
//! final line apart (a partial, never an entry). Across logs it counts each
//! identity, so a duplicate is a limit as in `storage::read_all`.
//!
//! How it stays correct: each refresh walks the records tree again (a
//! directory is listed again only when its own stamp changed; a symlink is
//! refused as `storage::discover` refuses it) and takes every log's stamp. A
//! log whose stamp is unchanged is not read. One that only grew, with the
//! bytes before its last complete line unchanged (checked against a kept copy
//! of up to 4 KiB), is read from its last complete line on. Any other change
//! (another inode, a shrink, a change before that point) reads the log again
//! from its start. A refresh therefore reads only new bytes, and takes one
//! metadata call per log and per directory. What it cannot see is an
//! in-place rewrite of earlier bytes that leaves the size, the modification
//! time and the kept tail unchanged.
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet, HashMap};
use std::os::unix::fs::MetadataExt;
use std::path::{Path, PathBuf};
use std::sync::Mutex;

const GUARD: u64 = 4096;
const INDEXED_PROJECTS: usize = 4;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub(crate) struct Stamp { dev: u64, ino: u64, size: u64, mtime: i64, mtime_ns: i64 }
impl Stamp {
    pub(crate) fn of(m: &std::fs::Metadata) -> Self {
        Self { dev: m.dev(), ino: m.ino(), size: m.len(), mtime: m.mtime(), mtime_ns: m.mtime_nsec() }
    }
}
#[derive(Clone, Debug)]
struct Line { id: Option<String>, offset: u64, len: usize, seq: u64, act: bool, corrects: Option<String>, late_subject: Option<String> }
#[derive(Clone, Default)]
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
}
#[derive(Default)]
pub(crate) struct ProjectIndex {
    dirs: HashMap<PathBuf, (Stamp, Vec<(PathBuf, bool)>)>,
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
}
static INDEXES: Mutex<Vec<(PathBuf, ProjectIndex)>> = Mutex::new(Vec::new());

/// Refreshes `root`'s index and gives it to `f`, under the index lock.
pub(crate) fn with_index<R>(root: &Path, f: impl FnOnce(&ProjectIndex) -> R) -> R {
    let mut all = INDEXES.lock().unwrap_or_else(|p| p.into_inner());
    let position = all.iter().position(|(r, _)| r == root);
    let (key, mut index) = match position { Some(i) => all.remove(i), None => (root.to_path_buf(), ProjectIndex::default()) };
    index.refresh(root);
    let result = f(&index);
    all.insert(0, (key, index));
    all.truncate(INDEXED_PROJECTS);
    result
}

fn act_kind(v: &Value) -> bool {
    matches!(v["kind"].as_str(), Some("human_act" | "act_declined")) || v.get("corrects").is_some()
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
    /// Every readable entry holding `id`, read from its log (in log order).
    pub(crate) fn entries_with(&self, id: &str) -> Vec<Value> {
        let Some(numbers) = self.ids.get(id) else { return vec![] };
        let numbers: BTreeSet<u32> = numbers.iter().copied().collect();
        let paths: BTreeSet<&PathBuf> = numbers.iter().filter_map(|n| self.numbers.get(n)).collect();
        paths.into_iter().filter_map(|path| self.logs.get(path).map(|log| (path, log)))
            .flat_map(|(path, log)| read_lines(path, log.entries().filter(|l| l.id.as_deref() == Some(id)))).collect()
    }
    /// Every readable "record write failed" limit naming `subject` (W-2).
    pub(crate) fn late_limits_for(&self, subject: &str) -> Vec<Value> {
        self.logs.iter().flat_map(|(path, log)| read_lines(path, log.entries().filter(|l| l.late_subject.as_deref() == Some(subject)))).collect()
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
    /// an identity with one of those, read from their logs.
    pub(crate) fn act_claims(&self) -> Vec<Value> {
        let mut wanted: BTreeSet<String> = BTreeSet::new();
        for log in self.logs.values() {
            for line in log.entries().filter(|l| l.act) {
                wanted.extend(line.id.clone());
                wanted.extend(line.corrects.clone());
            }
        }
        let mut claims = Vec::new();
        for (path, log) in &self.logs {
            for record in read_lines(path, log.entries().filter(|l| l.act || l.id.as_ref().is_some_and(|id| wanted.contains(id)))) {
                claims.push(json!({"source":{"log":path.to_string_lossy(),"seq":record["seq"]},"record":record}));
            }
        }
        claims
    }
    /// Every discovered log (sorted).
    pub(crate) fn paths(&self) -> Vec<PathBuf> { self.logs.keys().cloned().collect() }

    fn refresh(&mut self, root: &Path) {
        let (paths, error) = self.discover(root);
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
    /// `storage::discover`'s walk, listing a directory again only when its own stamp changed.
    fn discover(&mut self, root: &Path) -> (Vec<PathBuf>, Option<String>) {
        let records = root.join(".chirality/records");
        let mut out = Vec::new();
        if let Err(e) = crate::storage::check_path(&records) { return (out, Some(e)); }
        let mut todo = vec![records];
        let mut seen_dirs = BTreeSet::new();
        while let Some(dir) = todo.pop() {
            let meta = match std::fs::symlink_metadata(&dir) {
                Ok(m) => m,
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => continue,
                Err(e) => return (vec![], Some(format!("incomplete record discovery: {}: {e}", dir.display()))),
            };
            if meta.file_type().is_symlink() { return (vec![], Some(format!("owning path contains symlink: {}", dir.display()))); }
            seen_dirs.insert(dir.clone());
            let stamp = Stamp::of(&meta);
            let children = match self.dirs.get(&dir) {
                Some((s, c)) if *s == stamp => c.clone(),
                _ => {
                    let rd = match std::fs::read_dir(&dir) {
                        Ok(rd) => rd,
                        Err(e) => return (vec![], Some(format!("incomplete record discovery: {}: {e}", dir.display()))),
                    };
                    let mut children = Vec::new();
                    for entry in rd {
                        let entry = match entry { Ok(e) => e, Err(e) => return (vec![], Some(e.to_string())) };
                        let path = entry.path();
                        let kind = match std::fs::symlink_metadata(&path) { Ok(m) => m.file_type(), Err(e) => return (vec![], Some(e.to_string())) };
                        if kind.is_symlink() { return (vec![], Some(format!("owning path contains symlink: {}", path.display()))); }
                        if kind.is_dir() { children.push((path, true)); }
                        else if path.extension().is_some_and(|e| e == "jsonl") { children.push((path, false)); }
                    }
                    self.dirs.insert(dir.clone(), (stamp, children.clone()));
                    children
                }
            };
            for (path, is_dir) in children {
                if is_dir { todo.push(path); } else { out.push(path); }
            }
        }
        self.dirs.retain(|d, _| seen_dirs.contains(d));
        let legacy = root.join(crate::storage::LEGACY_LOG);
        if let Err(e) = crate::storage::check_path(&legacy) { return (vec![], Some(e)); }
        if legacy.exists() { out.push(legacy); }
        out.sort();
        out.dedup();
        (out, None)
    }
    fn refresh_log(&mut self, path: &Path) {
        let stamp = match std::fs::symlink_metadata(path) {
            Ok(m) if m.file_type().is_symlink() => None,
            Ok(m) => Some(Stamp::of(&m)),
            Err(_) => None,
        };
        let old = self.logs.get(path).cloned();
        if let (Some(s), Some(o)) = (stamp, &old) {
            if o.stamp == Some(s) { return; }
        }
        let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        // Grown in place: read from the last complete line, if the bytes before it are unchanged.
        let incremental = match (stamp, &old) {
            (Some(s), Some(o)) => o.stamp.is_some_and(|os| os.dev == s.dev && os.ino == s.ino && s.size >= os.size)
                && read_at(path, o.prefix_end.saturating_sub(GUARD), (o.prefix_end - o.prefix_end.saturating_sub(GUARD)) as usize).is_some_and(|b| b == o.guard),
            _ => false,
        };
        let number = match &old { Some(o) => o.number, None => { self.next_number += 1; self.numbers.insert(self.next_number, path.to_path_buf()); self.next_number } };
        let mut state = if incremental { old.clone().unwrap() } else { LogState { number, ..LogState::default() } };
        if let Some(o) = &old {
            if incremental { self.count(number, o.tail_entries.iter(), -1); } else { self.count(number, o.entries(), -1); }
        }
        let had_act = old.as_ref().is_some_and(|o| o.entries().any(|l| l.act));
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
            Err(e) => {
                state = LogState { number, stamp, tail_limits: vec![format!("incomplete record: {}: {e}", path.display())], ..LogState::default() };
                self.logs.insert(path.to_path_buf(), state);
                if had_act { self.act_epoch += 1; }
                return;
            }
        };
        if std::str::from_utf8(&bytes).is_err() {
            state = LogState { number, stamp, tail_limits: vec![format!("incomplete record: {}: stream did not contain valid UTF-8", path.display())], ..LogState::default() };
            self.logs.insert(path.to_path_buf(), state);
            if had_act { self.act_epoch += 1; }
            return;
        }
        let text = std::str::from_utf8(&bytes).unwrap();
        let mut segments: Vec<(u64, &str)> = Vec::new();
        let mut at = 0usize;
        for part in text.split('\n') {
            segments.push((state.prefix_end + at as u64, part));
            at += part.len() + 1;
        }
        let tail = segments.pop().unwrap_or((state.prefix_end, ""));
        // `str::lines` strips a carriage return; so does the reader.
        let lines: Vec<&str> = segments.iter().map(|(_, l)| l.strip_suffix('\r').unwrap_or(l)).collect();
        let recovered = crate::records::recovered_partial_lines_from(&lines, state.prefix_lines);
        let validator = crate::schema_validation::bundled();
        let mut expected = state.prefix_seq.max(1);
        let mut results: Vec<(u64, Result<Option<Line>, String>, u64)> = Vec::new();
        for (i, line) in lines.iter().enumerate() {
            let (offset, raw) = segments[i];
            let n = state.prefix_lines + i;
            let before = expected;
            let outcome = if line.trim().is_empty() || recovered.contains(&i) {
                Ok(None)
            } else {
                match serde_json::from_str::<Value>(line) {
                    Ok(v) => match validator.as_ref().map_err(|e| e.clone()).and_then(|val| val.validate(&v)) {
                        Ok(()) => {
                            let seq = v["seq"].as_u64().unwrap_or(0);
                            let entry = Line { id: v["recordId"].as_str().map(str::to_owned), offset, len: raw.len(), seq, act: act_kind(&v), corrects: v["corrects"].as_str().map(str::to_owned),
                                late_subject: (v["kind"] == "evidence_limit" && v["body"]["label"] == "record write failed").then(|| v["body"]["subjectRef"].as_str().map(str::to_owned)).flatten() };
                            if seq != expected {
                                results.push((offset, Err(format!("{name}: sequence incomplete/disagrees: expected {expected}, found {seq} at line {}", n + 1)), before));
                            }
                            expected = seq.checked_add(1).unwrap_or(seq);
                            Ok(Some(entry))
                        }
                        Err(e) => Err(format!("{name}: invalid line {}: {e}", n + 1)),
                    },
                    Err(_) => Err(format!("{name}: unreadable line {}", n + 1)),
                }
            };
            results.push((offset, outcome, before));
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
            let moved = segments.len() - 1;
            state.prefix_lines += moved;
            // The expected seq where the last complete line starts.
            state.prefix_seq = results.iter().find(|(o, _, _)| *o == start).map(|(_, _, b)| *b).unwrap_or(expected);
            state.prefix_end = start;
            state.complete_end = tail.0;
        }
        if !tail.1.is_empty() {
            state.partial = Some(format!("{name}: partial entry at end (not read)"));
        }
        let guard_from = state.prefix_end.saturating_sub(GUARD);
        state.guard = read_at(path, guard_from, (state.prefix_end - guard_from) as usize).unwrap_or_default();
        let added: Vec<Line> = if incremental {
            let kept = old.as_ref().map_or(0, |o| o.prefix_entries.len());
            state.prefix_entries[kept..].iter().chain(&state.tail_entries).cloned().collect()
        } else {
            state.entries().cloned().collect()
        };
        // The act read is recomputed when a log holding act records changes, or
        // when a new entry shares an identity with one (a conflict to show).
        let touches_acts = had_act || state.entries().any(|l| l.act)
            || added.iter().any(|l| l.id.as_ref().is_some_and(|id| self.act_ids.contains_key(id)));
        if touches_acts { self.act_epoch += 1; }
        self.count(number, added.iter(), 1);
        self.logs.insert(path.to_path_buf(), state);
    }
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
/// The given entries of one log, read with one open (in log order).
fn read_lines<'a>(path: &Path, lines: impl Iterator<Item = &'a Line>) -> Vec<Value> {
    use std::io::{Read, Seek, SeekFrom};
    let mut lines = lines.peekable();
    if lines.peek().is_none() { return vec![]; }
    let Ok(mut f) = std::fs::File::open(path) else { return vec![] };
    let mut out = Vec::new();
    for line in lines {
        let mut b = vec![0u8; line.len];
        if f.seek(SeekFrom::Start(line.offset)).and_then(|_| f.read_exact(&mut b)).is_ok() {
            if let Ok(v) = serde_json::from_slice(&b) { out.push(v); }
        }
    }
    out
}

#[cfg(test)]
#[path = "records_index_tests.rs"]
mod tests;
