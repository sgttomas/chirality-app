//! One reading and one appender for the records store's own line files:
//! `<store>/roots.jsonl` (the registry of project folders),
//! `<store>/projects/<key>/imports.jsonl` (a project's legacy import
//! account) and `<store>/legacy-imports.jsonl` (the store's witness of legacy
//! imports).
//!
//! **The rule.** An append never changes the meaning of bytes already in the
//! file. A crash can still leave a fragment; a fragment is never given meaning
//! and never changes the meaning of anything else.
//!
//! **Closing a fragment.** A line the appender writes is one JSON text and a
//! newline, written in one write. If that write is cut short, the file ends in
//! a fragment (its last byte is not a newline). Before its next append, and
//! once at startup, under the store lock, the writer closes the fragment: it
//! writes the closure mark ([`MARK`], the byte 0x1E), a newline and a naming
//! line ([`UNREAD_FORMAT`]) that names the closed line by its number, exact
//! length and SHA-256, all in one write, and only then the line it was asked
//! to write. It never writes a bare newline.
//!
//! **Why the mark makes a closed fragment unreadable, whatever it held.** By
//! RFC 8259 §2 a JSON text is `ws value ws`, where `ws` is only the bytes
//! 0x20, 0x09, 0x0A and 0x0D; a value ends in `}`, `]`, `"`, a digit, or the
//! last letter of `true`, `false` or `null`; and inside a string (§7) the
//! unescaped characters are U+0020-U+0021, U+0023-U+005B and U+005D-U+10FFFF,
//! so a control character U+0000-U+001F appears only escaped (`\u001e`).
//! In UTF-8 the byte 0x1E encodes U+001E and nothing else (every byte of a
//! multi-byte sequence is 0x80 or above). So no JSON text contains a raw
//! 0x1E byte anywhere, and in particular none ends in one: a closed line,
//! which ends in the mark, can never be read as a JSON line, even when the
//! fragment was a whole JSON text that lost only its newline. The same
//! grammar is why no writer here emits the mark by accident: serde_json
//! escapes every control character in a string it writes (the tests hold it
//! for each writer).
//!
//! **Recognising the App's own interrupted closure.** If the closure write is
//! itself cut short after its mark and newline, the closed line is complete
//! and no naming line names it. Because only a closure writes a raw 0x1E, a
//! complete line that ends in the mark and that no later naming line names is
//! the App's own interrupted closure, and only that; the writer names it,
//! once. (Someone outside the App can write such a line by hand: the writer
//! then names it and it is set aside, its bytes kept and never read. That is
//! the one thing the mark lets an outside party cause.) A complete line that
//! cannot be read and does not end in the mark is never named: the file is
//! "not read whole", reading continues from its other lines, the limit is
//! returned, and the appender refuses to append to that file.
use crate::util::{now_rfc3339, sha256_hex};
use serde_json::{json, Value};
use std::path::Path;

/// The format of a naming line (a stored-format addition, decided by App Agent 0).
pub(crate) const UNREAD_FORMAT: &str = "chirality.records-store.unread-line";
const VERSION: &str = "0.1";
/// The closure mark: the ASCII record separator, which no JSON text contains raw.
pub(crate) const MARK: u8 = 0x1E;

/// The bytes that close the unterminated `tail`: the mark (unless the tail
/// already ends in it, from a closure cut short after its mark) and a newline.
/// Returns the closing bytes and the closed line's bytes (without its newline).
pub(crate) fn closure(tail: &[u8]) -> (Vec<u8>, Vec<u8>) {
    let mut closing = Vec::new();
    if !is_closed(tail) {
        closing.push(MARK);
    }
    let mut line = tail.to_vec();
    line.extend(&closing);
    closing.push(b'\n');
    (closing, line)
}
/// Whether a line (without its newline) is a closed fragment: it ends in the mark.
pub(crate) fn is_closed(line: &[u8]) -> bool {
    line.last() == Some(&MARK)
}

/// The naming line (with its newline) for line `number` (from 1) whose exact
/// bytes are `line`.
pub(crate) fn naming_line(number: usize, line: &[u8]) -> Result<Vec<u8>, String> {
    let value = json!({"format":UNREAD_FORMAT,"formatVersion":VERSION,"line":number,"length":line.len(),
        "sha256":sha256_hex(line),"at":now_rfc3339(),"by":"writer"});
    let mut bytes = serde_json::to_vec(&value).map_err(|e| e.to_string())?;
    bytes.push(b'\n');
    Ok(bytes)
}

/// A store line file as read.
#[derive(Debug, Default)]
pub(crate) struct Read {
    /// The readable lines in written order, naming lines left out.
    pub values: Vec<Value>,
    /// What the reading could not read or use, for the caller to show.
    pub limits: Vec<String>,
    /// False when a complete line cannot be read, is not named and is not a
    /// closed fragment: the file is not read whole and nothing is appended.
    pub whole: bool,
    /// Complete lines that end in the mark and that no naming line names
    /// (number from 1, exact bytes): the App's own closures cut short.
    pub unnamed_closures: Vec<(usize, Vec<u8>)>,
    /// The unterminated last bytes, never read.
    pub tail: Option<Vec<u8>>,
    /// The number of complete lines.
    pub complete_lines: usize,
    /// The line numbers set aside by a naming line (bytes kept, never read).
    pub set_aside: Vec<usize>,
}
impl Read {
    /// The readable lines, or the refusal when the file was not read whole.
    pub(crate) fn require_whole(self, path: &Path) -> Result<Vec<Value>, String> {
        if self.whole {
            Ok(self.values)
        } else {
            Err(not_read_whole(path, &self.limits))
        }
    }
    /// The bytes that close and name every fragment, written before an
    /// append (empty when there is nothing to close or name). Every prefix of
    /// them, if a write of them is cut short, is recovered by the next one.
    pub(crate) fn recovery(&self) -> Result<Vec<u8>, String> {
        let mut out = Vec::new();
        if let Some(tail) = &self.tail {
            // The closed tail becomes the line after the complete ones.
            let (closing, line) = closure(tail);
            out.extend(closing);
            out.extend(naming_line(self.complete_lines + 1, &line)?);
        }
        for (number, line) in &self.unnamed_closures {
            out.extend(naming_line(*number, line)?);
        }
        Ok(out)
    }
}

/// The refusal for a file that was not read whole.
pub(crate) fn not_read_whole(path: &Path, limits: &[String]) -> String {
    let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    format!("{name} was not read whole ({}); its bytes are kept and nothing in it changed", limits.join("; "))
}

/// The one reading of a store line file's `bytes`.
pub(crate) fn read(bytes: &[u8], path: &Path) -> Read {
    let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let end = bytes.iter().rposition(|b| *b == b'\n').map_or(0, |i| i + 1);
    let mut out = Read { whole: true, ..Read::default() };
    if end < bytes.len() {
        out.tail = Some(bytes[end..].to_vec());
        out.limits.push(format!("{name}: a partial line at the end ({} bytes) is not read", bytes.len() - end));
    }
    let lines: Vec<&[u8]> = if end == 0 { vec![] } else { bytes[..end - 1].split(|b| *b == b'\n').collect() };
    out.complete_lines = lines.len();
    let parsed: Vec<Option<Value>> = lines.iter().map(|l| serde_json::from_slice::<Value>(l).ok()).collect();
    // Each naming line sets aside the earlier line it names exactly, when that
    // line cannot be read; otherwise it sets nothing aside and is a limit.
    let mut named = std::collections::BTreeSet::new();
    for (i, value) in parsed.iter().enumerate() {
        let Some(value) = value.as_ref().filter(|v| v["format"] == UNREAD_FORMAT) else { continue };
        let own = i + 1;
        let target = value["line"].as_u64().map(|n| n as usize).filter(|n| *n >= 1 && *n < own);
        let exact = target.filter(|n| {
            let line = lines[n - 1];
            value["length"].as_u64() == Some(line.len() as u64) && value["sha256"].as_str() == Some(sha256_hex(line).as_str())
        });
        match exact {
            Some(n) if parsed[n - 1].is_some() => out.limits.push(format!("{name}: line {own} names line {n}, which can be read; it sets nothing aside")),
            Some(n) if !named.insert(n) => out.limits.push(format!("{name}: line {own} names line {n} again; it was already set aside")),
            Some(_) => {}
            None => out.limits.push(format!("{name}: line {own} names bytes that are not an earlier line of this file; it sets nothing aside")),
        }
    }
    for (i, (line, value)) in lines.iter().zip(&parsed).enumerate() {
        let number = i + 1;
        match value {
            Some(v) if v["format"] == UNREAD_FORMAT => {}
            Some(v) => out.values.push(v.clone()),
            // An empty line holds nothing to read (as before).
            None if line.is_empty() => {}
            None if named.contains(&number) => out.set_aside.push(number),
            None if is_closed(line) => {
                out.limits.push(format!("{name}: line {number} is a closed partial line not yet named; it is not read"));
                out.unnamed_closures.push((number, line.to_vec()));
            }
            None => {
                out.whole = false;
                out.limits.push(format!("{name}: line {number} cannot be read and is not named"));
            }
        }
    }
    out
}
