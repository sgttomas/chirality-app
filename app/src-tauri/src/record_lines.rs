//! RS record lines (RS §13.8 "Units written together" and "Tamper-evidence";
//! §14.1 W-1, §14.2 R-2 as §13.8 reads them): one entry or one group per line,
//! each line linked to the preceding complete line of its log.
//!
//! **Groups.** A group line is `{"format":"chirality.rs.group", ...,
//! "entries":[entry, entry, ...]}`: two or more entries one writer wrote in one
//! write because they must stand together (an `act_counted` and the
//! disposition change it makes, a lapse and its label, a request and its
//! requester limit). Its entries carry consecutive `seq`, one run (or none), and no
//! chain link of their own. A reader takes a group whole or reports the line
//! as a limit; it never reads half a group.
//!
//! **Chain.** Each line the App writes carries `prevLine` {method
//! `chirality.rs.line.sha256/v1`, value}: the SHA-256 of the exact bytes of
//! the preceding complete line of its log (without its line feed), or `null`
//! on the first line of a log. A line W-0 terminated after a torn write
//! (named by its "partial entry not recovered" limit) is not a link: the next
//! line links to the line before it, and the reader notes the gap. Lines with
//! no link before the first linked line are "unchained (legacy)", a limit
//! that does not make the log incomplete: an imported §13.7 log, or a store log
//! written before the chain. The first linked line after them links to the
//! last of them, so the chain starts there. A line with no link after a linked
//! line, or a link that does not name the preceding line, is a broken chain: a
//! limit that makes the log incomplete, never repaired.
//!
//! **Chain head.** A log's head is the identity of its last link line and the
//! number of its lines (`chain_head`), read from the log itself; an export
//! package (U-STORE-5) records it. Signed checkpoints, entries naming a head
//! they cover with a signature, wait for App signing (OI-011).
use serde_json::{json, Value};
use std::collections::BTreeSet;

/// The method designation of a line's content identity.
pub const LINE_METHOD: &str = "chirality.rs.line.sha256/v1";
/// The format name of a group line.
pub(crate) const GROUP_FORMAT: &str = "chirality.rs.group";
/// The limit label for lines that carry no chain link.
pub(crate) const UNCHAINED: &str = "unchained (legacy)";

/// The content identity of one line: SHA-256 of its exact bytes, without its
/// line feed (a trailing carriage return is part of the bytes).
pub fn line_identity(raw: &[u8]) -> String {
    crate::util::sha256_hex(raw)
}
/// The `prevLine` link naming `previous` (the identity of the preceding link
/// line), or the first line of a log.
pub fn link(previous: Option<&str>) -> Value {
    json!({"method": LINE_METHOD, "value": previous})
}

/// Why a line is not read.
#[derive(Debug, Clone, PartialEq)]
pub(crate) enum NotRead {
    /// Not text, or not JSON.
    Unreadable,
    /// JSON that the schema or the group rules refuse.
    Invalid(String),
}
/// One line decoded: its entries (one, or a group's) and its chain link.
pub(crate) fn decode_line(raw: &[u8], validator: &crate::schema_validation::RecordValidator) -> Result<(Vec<Value>, Option<Value>), NotRead> {
    let text = std::str::from_utf8(raw.strip_suffix(b"\r").unwrap_or(raw)).map_err(|_| NotRead::Unreadable)?;
    let v: Value = serde_json::from_str(text).map_err(|_| NotRead::Unreadable)?;
    if v["format"] == GROUP_FORMAT {
        validator.validate_group(&v).map_err(NotRead::Invalid)?;
        let entries = v["entries"].as_array().cloned().unwrap_or_default();
        group_rules(&entries).map_err(NotRead::Invalid)?;
        return Ok((entries, v.get("prevLine").cloned()));
    }
    validator.validate(&v).map_err(NotRead::Invalid)?;
    let link = v.get("prevLine").cloned();
    Ok((vec![v], link))
}
/// What a group must also be, beyond its schema: entries with consecutive
/// `seq`, of one run (or none), with distinct identities.
pub(crate) fn group_rules(entries: &[Value]) -> Result<(), String> {
    let run = &entries[0]["runId"];
    if entries.iter().any(|e| e["runId"] != *run) {
        return Err("a group's entries name different runs".into());
    }
    for pair in entries.windows(2) {
        if pair[1]["seq"].as_u64() != pair[0]["seq"].as_u64().and_then(|s| s.checked_add(1)) {
            return Err("a group's entries do not have consecutive seq".into());
        }
    }
    let ids: BTreeSet<&str> = entries.iter().filter_map(|e| e["recordId"].as_str()).collect();
    if ids.len() != entries.len() {
        return Err("a group holds one record identity twice".into());
    }
    Ok(())
}
/// Whether `raw` is a whole, valid line (an entry or a group).
pub(crate) fn is_valid_line(raw: &[u8]) -> bool {
    crate::schema_validation::bundled().ok().is_some_and(|v| decode_line(raw, v).is_ok())
}

/// The chain read so far in one log.
#[derive(Clone, Debug, Default, PartialEq)]
pub(crate) struct Chain {
    /// The identity of the last link line, if any line was read.
    pub last: Option<String>,
    /// Lines read (link lines, chained or not).
    pub lines: usize,
    /// A linked line has been read.
    pub linked: bool,
    /// Link lines read without a chain link before the first linked line.
    pub unchained: usize,
}
impl Chain {
    /// Takes one complete link line (`no` from 1) with its link, if it has one.
    pub(crate) fn step(&mut self, no: usize, raw: &[u8], link: Option<&Value>) -> Result<(), String> {
        let identity = line_identity(raw);
        let result = match link {
            None if self.linked => Err(format!("chain broken at line {no}: no chain link after linked lines; never repaired")),
            None => {
                self.unchained += 1;
                Ok(())
            }
            Some(l) => {
                self.linked = true;
                if l["method"] != LINE_METHOD {
                    Err(format!("chain broken at line {no}: unknown chain method {}", l["method"]))
                } else if l["value"].as_str() != self.last.as_deref() {
                    Err(match (&l["value"], &self.last) {
                        (Value::Null, Some(_)) => format!("chain broken at line {no}: it starts a new chain after earlier lines; never repaired"),
                        (v, Some(last)) => format!("chain broken at line {no}: it links to {v}, but the preceding line's identity is {last}; never repaired"),
                        (v, None) => format!("chain broken at line {no}: it links to {v}, but it is the first line of its log; never repaired"),
                    })
                } else {
                    Ok(())
                }
            }
        };
        self.last = Some(identity);
        self.lines += 1;
        result
    }
    /// The limit for unchained lines, if any (it does not make a log incomplete).
    pub(crate) fn unchained_note(&self, name: &str) -> Option<String> {
        (self.unchained > 0).then(|| if self.linked {
            format!("{name}: {UNCHAINED}: lines before the first linked line ({}) carry no chain link; the chain starts after them", self.unchained)
        } else {
            format!("{name}: {UNCHAINED}: no line carries a chain link ({} lines)", self.unchained)
        })
    }
}

/// The logs this process has read with a chain (RS §13.8).
static LINKED: std::sync::Mutex<BTreeSet<std::path::PathBuf>> = std::sync::Mutex::new(BTreeSet::new());
/// RS §13.8: a log this process read with a chain that now reads with
/// unchained lines and no link at all had its links removed. That is a broken
/// chain, never unchained (legacy). Remembered per process only, by the R-2
/// readers (`records::read_log_parts`, the bounded index).
pub(crate) fn links_removed(path: &std::path::Path, name: &str, chain: &Chain) -> Option<String> {
    let mut linked = LINKED.lock().unwrap_or_else(|p| p.into_inner());
    if chain.linked {
        linked.insert(path.to_path_buf());
        return None;
    }
    (chain.unchained > 0 && linked.contains(path))
        .then(|| format!("{name}: chain broken: read with a chain earlier in this process, it now has no line carrying a link; never repaired"))
}

/// One complete line as read.
#[derive(Clone, Debug)]
pub(crate) struct ParsedLine {
    /// From 1, in the whole log.
    pub no: usize,
    pub offset: u64,
    pub len: usize,
    /// The line's entries (none when it is not read).
    pub entries: Vec<Value>,
    /// Limits that make the log incomplete.
    pub limits: Vec<String>,
    /// Limits that do not (a torn line W-0 named: not a link).
    pub notes: Vec<String>,
    /// The expected `seq` and the chain as they stood before this line.
    pub expected_before: u64,
    pub chain_before: Chain,
}
/// A log (or its part after `first` complete lines) as read.
pub(crate) struct Parsed {
    pub lines: Vec<ParsedLine>,
    /// The unclosed final line: a partial, never an entry (R-2).
    pub partial_tail: Option<String>,
    /// Where the partial tail starts.
    pub tail_offset: u64,
    pub chain: Chain,
}
/// R-2 on `bytes`, the part of a log after its first `first` lines (starting
/// at byte `base`), with the `seq` expected next and the chain so far.
pub(crate) fn parse(bytes: &[u8], name: &str, first: usize, base: u64, expected: u64, chain: Chain) -> Parsed {
    let mut lines = Vec::new();
    let mut parsed = parse_with(bytes, name, first, base, expected, chain, &mut |line| lines.push(line));
    parsed.lines = lines;
    parsed
}
/// As [`parse`], handing each line to `each` as it is read (its entries are
/// not kept): a large log is never held as values at once. `lines` is empty.
pub(crate) fn parse_with(bytes: &[u8], name: &str, first: usize, base: u64, mut expected: u64, mut chain: Chain, each: &mut dyn FnMut(ParsedLine)) -> Parsed {
    let validator = crate::schema_validation::bundled();
    let mut segments: Vec<(u64, &[u8])> = Vec::new();
    let mut at = 0usize;
    for part in bytes.split(|b| *b == b'\n') {
        segments.push((base + at as u64, part));
        at += part.len() + 1;
    }
    let tail = segments.pop().unwrap_or((base, b""));
    let complete = &bytes[..bytes.len() - tail.1.len()];
    let (hidden, mismatched) = crate::records::recovered_partial_lines(complete, first);
    for (i, (offset, raw)) in segments.iter().enumerate() {
        let no = first + i + 1;
        let mut line = ParsedLine { no, offset: *offset, len: raw.len(), entries: vec![], limits: vec![], notes: vec![], expected_before: expected, chain_before: chain.clone() };
        for (_, m) in mismatched.iter().filter(|(k, _)| *k == i) {
            line.limits.push(format!("{name}: {m}"));
        }
        if hidden.contains(&i) {
            line.notes.push(format!("{name}: line {no} is a torn line W-0 terminated; it is not a chain link, and the next line links to the line before it"));
            each(line);
            continue;
        }
        if raw.strip_suffix(b"\r").unwrap_or(raw).iter().all(u8::is_ascii_whitespace) {
            each(line);
            continue;
        }
        let decoded = match &validator {
            Ok(v) => decode_line(raw, v),
            Err(e) => Err(NotRead::Invalid(e.clone())),
        };
        match decoded {
            Ok((entries, link)) => {
                if let Err(broken) = chain.step(no, raw, link.as_ref()) {
                    line.limits.push(format!("{name}: {broken}"));
                }
                for entry in &entries {
                    let seq = entry["seq"].as_u64().unwrap_or(0);
                    if seq != expected {
                        line.limits.push(format!("{name}: sequence incomplete/disagrees: expected {expected}, found {seq} at line {no}"));
                    }
                    expected = seq.checked_add(1).unwrap_or(seq);
                }
                line.entries = entries;
            }
            Err(not_read) => {
                // Already a limit; still the line the next one links to (its
                // bytes are complete), neither a link check nor unchained.
                chain.last = Some(line_identity(raw));
                chain.lines += 1;
                line.limits.push(match not_read {
                    NotRead::Unreadable => format!("{name}: unreadable line {no}"),
                    NotRead::Invalid(e) => format!("{name}: invalid line {no}: {e}"),
                });
            }
        }
        each(line);
    }
    let partial_tail = (!tail.1.is_empty() && !tail.1.iter().all(u8::is_ascii_whitespace)).then(|| format!("{name}: partial entry at end (not read)"));
    Parsed { lines: Vec::new(), partial_tail, tail_offset: tail.0, chain }
}

/// A log's chain head: the identity of its last link line and its line count
/// (what an export manifest records, U-STORE-5), with its chain limits.
/// Export is not built yet; today tests and the durability witnesses read it.
#[allow(dead_code)]
pub(crate) fn chain_head(path: &std::path::Path) -> Value {
    let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let bytes = match std::fs::read(path) {
        Ok(b) => b,
        Err(e) => return json!({"state":"unreadable","error":e.to_string()}),
    };
    let mut limits: Vec<String> = Vec::new();
    let parsed = parse_with(&bytes, &name, 0, 0, 1, Chain::default(), &mut |l| limits.extend(l.limits.into_iter().filter(|m| m.contains("chain broken"))));
    json!({"method":LINE_METHOD,"head":parsed.chain.last,"lines":parsed.chain.lines,"linked":parsed.chain.linked,
        "unchained":parsed.chain.unchained,"unchainedLimit":parsed.chain.unchained_note(&name),"broken":limits,
        "signedCheckpoints":"not written: they wait for App signing (OI-011)"})
}

#[cfg(test)]
#[path = "record_lines_tests.rs"]
mod tests;

/// Test fixtures that write lines by hand, as the App links them.
#[cfg(test)]
pub(crate) mod fixture {
    use super::*;
    /// The chain link the next line of `log` carries.
    pub(crate) fn next_link(log: &std::path::Path) -> Value {
        let bytes = std::fs::read(log).unwrap_or_default();
        link(parse(&bytes, "", 0, 0, 1, Chain::default()).chain.last.as_deref())
    }
    /// The log's bytes with every complete line linked again to the one before
    /// (a fixture's in-place edit, made consistent as the App would have written it).
    pub(crate) fn rechain(bytes: &[u8]) -> Vec<u8> {
        let mut out = Vec::new();
        let mut previous: Option<String> = None;
        let mut parts: Vec<&[u8]> = bytes.split(|b| *b == b'\n').collect();
        let tail = parts.pop().unwrap_or(b"");
        for raw in parts {
            let line = match serde_json::from_slice::<Value>(raw) {
                Ok(mut v) if v.is_object() => {
                    v["prevLine"] = link(previous.as_deref());
                    serde_json::to_vec(&v).unwrap()
                }
                _ => raw.to_vec(),
            };
            previous = Some(line_identity(&line));
            out.extend(&line);
            out.push(b'\n');
        }
        out.extend(tail);
        out
    }
}
