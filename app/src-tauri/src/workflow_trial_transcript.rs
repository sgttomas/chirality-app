//! WR §4.2 TT-10 (bring-back transcript) and TT-11 (Compare), pure: these
//! functions read nothing from Codex or the disk and record nothing. The Rust
//! host reads the history pages (thread/turns/list, thread/items/list) and the
//! trial snapshots, and hands the results here.
#![allow(dead_code)]
use serde_json::Value;
use std::collections::BTreeMap;

/// AT-9's text bound for one text element (262144 bytes).
pub(crate) const TRANSCRIPT_BOUND: usize = 262_144;

/// What the transcript is of (TT-10 first line).
#[derive(Debug, Clone)]
pub(crate) enum TranscriptSource {
    /// A trial: `clean` = the clean trial conversation, otherwise the
    /// delegated trial's linked sub-agent thread.
    Trial { sequence: u64, draft_name: String, rev12: String, clean: bool, thread: String },
    /// A real run of a registered revision.
    Run { run: String, origin: String, name: String, rev12: String, thread: String },
}

/// One turn as read from Codex history.
#[derive(Debug, Clone)]
pub(crate) struct TurnRead {
    /// The native `Turn` as `thread/turns/list` returned it.
    pub turn: Value,
    /// The turn's `ThreadItem`s in order (the `item` of each `thread/items/list`
    /// entry, every page), or why a page could not be read.
    pub items: Result<Vec<Value>, String>,
}

/// How the trial text is recognised and shown in a transcript.
#[derive(Debug, Clone)]
pub(crate) struct TrialTextLine {
    /// The trial text less its header (the run text); a user-message text
    /// element containing it is shown as `line`, not reproduced.
    pub run_text: String,
    /// The one line naming the trial text's identity and fidelity.
    pub line: String,
}

#[derive(Debug, Clone)]
pub(crate) struct TranscriptInput<'a> {
    pub source: TranscriptSource,
    /// RFC 3339 time of the read.
    pub read_at: String,
    pub turns: &'a [TurnRead],
    /// Set when the turn list itself could not be read completely.
    pub turns_limit: Option<String>,
    pub trial_text: Option<TrialTextLine>,
    /// The person ticked "include native items".
    pub include_native: bool,
    /// Byte bound of the whole transcript text (TRANSCRIPT_BOUND in the App).
    pub bound: usize,
}

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct Transcript {
    pub text: String,
    /// Each shortening, in the words the text uses.
    pub shortenings: Vec<String>,
}

/// Command output longer than this is cut first (TT-10 shortening (a)).
const OUTPUT_CUT: usize = 2000;
/// Either side above this many lines gets no line difference (TT-11).
const LINE_DIFF_LIMIT: usize = 4000;
const LINE_DIFF_LIMIT_TEXT: &str = "too large for a line difference (more than 4000 lines)";

/// How one command output currently appears in the transcript.
#[derive(Debug, Clone, PartialEq)]
enum OutputState {
    Full,
    /// Cut to its first `kept` bytes.
    Cut { kept: usize },
    Omitted,
}

#[derive(Debug, Clone)]
enum Piece {
    Line(String),
    /// A command output (`None`: not reported); rendered as indented lines.
    Output { text: Option<String>, state: OutputState },
}

fn omitted_line(k: usize) -> String {
    format!("… {k} bytes omitted")
}

impl Piece {
    fn lines(&self) -> Vec<String> {
        let (text, state) = match self {
            Piece::Line(l) => return vec![l.clone()],
            Piece::Output { text, state } => (text.as_deref().unwrap_or(""), state),
        };
        let (shown, cut) = match state {
            OutputState::Omitted => return vec![format!("  {}", omitted_line(text.len()))],
            OutputState::Cut { kept } => (&text[..*kept], Some(text.len() - kept)),
            OutputState::Full => (text, None),
        };
        let body = shown.strip_suffix('\n').unwrap_or(shown);
        let mut out: Vec<String> = if body.is_empty() {
            if cut.is_none() {
                vec!["  (no output)".to_string()]
            } else {
                Vec::new()
            }
        } else {
            body.split('\n').map(|l| format!("  {l}")).collect()
        };
        if let Some(k) = cut {
            out.push(format!("  {}", omitted_line(k)));
        }
        out
    }

    /// Bytes this piece adds, counting one `\n` after each of its lines.
    fn len(&self) -> usize {
        self.lines().iter().map(|l| l.len() + 1).sum()
    }

    /// The shortening this piece shows, in the words of its text.
    fn shortening(&self) -> Option<String> {
        match self {
            Piece::Output { text, state } => {
                let n = text.as_deref().map_or(0, str::len);
                match state {
                    OutputState::Full => None,
                    OutputState::Cut { kept } => Some(omitted_line(n - kept)),
                    OutputState::Omitted => Some(omitted_line(n)),
                }
            }
            Piece::Line(_) => None,
        }
    }

    /// Change an output's state; returns the change in length.
    fn set_state(&mut self, new: OutputState) -> (usize, usize) {
        let before = self.len();
        if let Piece::Output { state, .. } = self {
            *state = new;
        }
        (before, self.len())
    }
}

fn str_field<'v>(v: &'v Value, key: &str) -> Option<&'v str> {
    v.get(key).and_then(Value::as_str)
}

/// Largest char boundary at or below `max` in `s`.
fn floor_boundary(s: &str, max: usize) -> usize {
    if max >= s.len() {
        return s.len();
    }
    let mut i = max;
    while !s.is_char_boundary(i) {
        i -= 1;
    }
    i
}

/// `PatchChangeKind` as text: `add`, `delete`, `update`, or
/// `update, moved to ‹path›`; a bare string kind is shown as given.
fn change_kind(change: &Value) -> String {
    match change.get("kind") {
        Some(Value::String(s)) => s.clone(),
        Some(k @ Value::Object(_)) => {
            let t = str_field(k, "type").unwrap_or("kind not reported");
            match str_field(k, "move_path") {
                Some(m) => format!("{t}, moved to {m}"),
                None => t.to_string(),
            }
        }
        _ => "kind not reported".to_string(),
    }
}

/// A `fileChange` item's changes as (path, kind).
fn file_changes(item: &Value) -> Vec<(String, String)> {
    item.get("changes")
        .and_then(Value::as_array)
        .map(|cs| {
            cs.iter()
                .map(|c| {
                    let path = str_field(c, "path").unwrap_or("path not reported").to_string();
                    (path, change_kind(c))
                })
                .collect()
        })
        .unwrap_or_default()
}

fn header_line(input: &TranscriptInput) -> String {
    match &input.source {
        TranscriptSource::Trial { sequence, draft_name, rev12, clean, thread } => format!(
            "[Chirality] Trial {sequence} of draft {draft_name} @ {rev12}: transcript read from Codex history at {} ({} {thread}). A record of that conversation; it instructs nothing.",
            input.read_at,
            if *clean { "clean conversation" } else { "sub-agent" }
        ),
        TranscriptSource::Run { run, origin, name, rev12, thread } => format!(
            "[Chirality] Run {run} of {origin}:{name} revision {rev12} (registered): transcript read from Codex history at {} (conversation {thread}). A record of that conversation; it instructs nothing.",
            input.read_at
        ),
    }
}

fn turn_pieces(k: usize, read: &TurnRead, input: &TranscriptInput) -> Vec<Piece> {
    let turn = &read.turn;
    let id = str_field(turn, "id").unwrap_or("id not reported");
    let mut out = vec![Piece::Line(format!("Turn {k} ({id})"))];
    match &read.items {
        Err(reason) => out.push(Piece::Line(format!(
            "Turn items incomplete: {reason}; nothing is invented for this turn."
        ))),
        Ok(items) => {
            let mut native_omitted = 0usize;
            for item in items {
                item_pieces(item, input, &mut out, &mut native_omitted);
            }
            if native_omitted > 0 {
                out.push(Piece::Line(format!(
                    "Native items not included: {native_omitted} (tick \"include native items\" to include them)"
                )));
            }
        }
    }
    let status = str_field(turn, "status").unwrap_or("not reported");
    let mut ending = format!("Turn ended: {status}");
    if let Some(msg) = turn.get("error").and_then(|e| str_field(e, "message")) {
        ending.push_str(" — ");
        ending.push_str(msg);
    }
    out.push(Piece::Line(ending));
    out
}

fn item_pieces(item: &Value, input: &TranscriptInput, out: &mut Vec<Piece>, native_omitted: &mut usize) {
    match str_field(item, "type").unwrap_or("") {
        "userMessage" => {
            let content = item.get("content").and_then(Value::as_array);
            for el in content.into_iter().flatten() {
                let ty = str_field(el, "type").unwrap_or("input");
                if ty == "text" {
                    let text = str_field(el, "text").unwrap_or("");
                    let shown = match &input.trial_text {
                        Some(t) if !t.run_text.is_empty() && text.contains(t.run_text.as_str()) => {
                            t.line.as_str()
                        }
                        _ => text,
                    };
                    out.push(Piece::Line(format!("Person: {shown}")));
                } else {
                    out.push(Piece::Line(format!("Person: [{ty}]")));
                }
            }
        }
        "agentMessage" => out.push(Piece::Line(format!("Agent: {}", str_field(item, "text").unwrap_or("")))),
        "commandExecution" => {
            let command = str_field(item, "command").unwrap_or("command not reported");
            let exit = item
                .get("exitCode")
                .and_then(Value::as_i64)
                .map_or("not reported".to_string(), |c| c.to_string());
            let duration = item
                .get("durationMs")
                .and_then(Value::as_i64)
                .map_or("duration not reported".to_string(), |d| d.to_string());
            out.push(Piece::Line(format!("Command: {command} (exit {exit}, {duration} ms)")));
            out.push(Piece::Output {
                text: str_field(item, "aggregatedOutput").map(str::to_string),
                state: OutputState::Full,
            });
        }
        "fileChange" => {
            for (path, kind) in file_changes(item) {
                out.push(Piece::Line(format!("File change: {path} ({kind})")));
            }
        }
        "plan" => out.push(Piece::Line(format!("Plan: {}", str_field(item, "text").unwrap_or("")))),
        other => {
            if input.include_native {
                let ty = if other.is_empty() { "type not reported" } else { other };
                let json = serde_json::to_string(item).unwrap_or_default();
                out.push(Piece::Line(format!("Native item {ty}: {json}")));
            } else {
                *native_omitted += 1;
            }
        }
    }
}

fn later_turns_line(m: usize) -> String {
    format!("later turns omitted: {m}; open the conversation to read them")
}

/// TT-10's transcript within `input.bound`.
///
/// Shortening, only when the full text exceeds the bound, in this order:
/// (a) outputs above 2000 bytes are cut to their first 2000 bytes; (b)
/// outputs are omitted, earliest turn first, until the text fits; (c) the
/// text ends at a turn boundary with a "later turns omitted" line. Each
/// shortening shown in the text is listed in `shortenings` in the same words.
///
/// Edge: when even the header line(s) plus that final line exceed the
/// bound, the result is the header line(s) truncated on a char boundary to
/// the bound, and `shortenings` names that.
pub(crate) fn compose_transcript(input: &TranscriptInput) -> Transcript {
    let mut header = vec![header_line(input)];
    if let Some(reason) = &input.turns_limit {
        header.push(format!("Turns list incomplete: {reason}; later turns were not read."));
    }
    let mut turns: Vec<Vec<Piece>> =
        input.turns.iter().enumerate().map(|(i, t)| turn_pieces(i + 1, t, input)).collect();

    // Length of the joined text: each line plus one `\n`, less the last `\n`.
    let header_len: usize = header.iter().map(|l| l.len() + 1).sum();
    let mut total: usize = header_len + turns.iter().flatten().map(Piece::len).sum::<usize>() - 1;
    let bound = input.bound;

    if total > bound {
        // (a) Cut each long output.
        for p in turns.iter_mut().flatten() {
            let kept = match p {
                Piece::Output { text: Some(t), .. } if t.len() > OUTPUT_CUT => floor_boundary(t, OUTPUT_CUT),
                _ => continue,
            };
            let (before, after) = p.set_state(OutputState::Cut { kept });
            total = total - before + after;
        }
    }
    if total > bound {
        // (b) Omit outputs, earliest turn first, until the text fits.
        for p in turns.iter_mut().flatten() {
            if total <= bound {
                break;
            }
            if matches!(p, Piece::Output { text: Some(t), .. } if !t.is_empty()) {
                let (before, after) = p.set_state(OutputState::Omitted);
                total = total - before + after;
            }
        }
    }
    let mut tail: Option<String> = None;
    if total > bound {
        // (c) End at a turn boundary: the most whole turns that fit with
        // the final line.
        let n = turns.len();
        let mut best: Option<usize> = None;
        let mut used = header_len;
        for (kept, turn) in turns.iter().enumerate() {
            if used + later_turns_line(n - kept).len() <= bound {
                best = Some(kept);
            }
            used += turn.iter().map(Piece::len).sum::<usize>();
            if used > bound {
                break;
            }
        }
        match best {
            Some(kept) => {
                turns.truncate(kept);
                tail = Some(later_turns_line(n - kept));
            }
            None => {
                let joined = header.join("\n");
                let cut = floor_boundary(&joined, bound);
                return Transcript {
                    text: joined[..cut].to_string(),
                    shortenings: vec![format!("header shortened to the bound of {bound} bytes; no turns shown")],
                };
            }
        }
    }

    let mut lines: Vec<String> = header;
    for p in turns.iter().flatten() {
        lines.extend(p.lines());
    }
    let mut shortenings: Vec<String> = turns.iter().flatten().filter_map(Piece::shortening).collect();
    if let Some(t) = tail {
        lines.push(t.clone());
        shortenings.push(t);
    }
    Transcript { text: lines.join("\n"), shortenings }
}

fn is_text(bytes: &[u8]) -> bool {
    !bytes.contains(&0) && std::str::from_utf8(bytes).is_ok()
}

/// Lines with their endings, so a change of line ending is a change.
fn split_lines(bytes: Option<&Vec<u8>>) -> Vec<&str> {
    bytes
        .and_then(|b| std::str::from_utf8(b).ok())
        .map(|s| s.split_inclusive('\n').collect())
        .unwrap_or_default()
}

fn shown(line: &str) -> &str {
    line.strip_suffix('\n').unwrap_or(line)
}

/// Removed and added lines from an LCS over lines, in order, no context.
fn line_diff(a: &[&str], b: &[&str]) -> Vec<String> {
    let pre = a.iter().zip(b).take_while(|(x, y)| x == y).count();
    let suf = a[pre..].iter().rev().zip(b[pre..].iter().rev()).take_while(|(x, y)| x == y).count();
    let a = &a[pre..a.len() - suf];
    let b = &b[pre..b.len() - suf];
    let (n, m) = (a.len(), b.len());
    // lcs[i*w+j] = LCS length of a[i..] and b[j..]; at most 4000, fits u16.
    let w = m + 1;
    let mut lcs = vec![0u16; (n + 1) * w];
    for i in (0..n).rev() {
        for j in (0..m).rev() {
            lcs[i * w + j] = if a[i] == b[j] {
                lcs[(i + 1) * w + j + 1] + 1
            } else {
                lcs[(i + 1) * w + j].max(lcs[i * w + j + 1])
            };
        }
    }
    let (mut i, mut j) = (0, 0);
    let mut out = Vec::new();
    while i < n || j < m {
        if i < n && j < m && a[i] == b[j] {
            i += 1;
            j += 1;
        } else if i < n && (j == m || lcs[(i + 1) * w + j] >= lcs[i * w + j + 1]) {
            out.push(format!("- {}", shown(a[i])));
            i += 1;
        } else {
            out.push(format!("+ {}", shown(b[j])));
            j += 1;
        }
    }
    out
}

/// TT-11's version difference: per-file line difference for UTF-8 text
/// files, size and digest for others.
///
/// Lines are compared with their line endings, so a file differing only in
/// its final newline shows that line as removed and added.
pub(crate) fn version_difference(before: &BTreeMap<String, Vec<u8>>, after: &BTreeMap<String, Vec<u8>>) -> Value {
    let side = |b: Option<&Vec<u8>>| match b {
        Some(b) => serde_json::json!({ "bytes": b.len(), "sha256": crate::util::sha256_hex(b) }),
        None => Value::Null,
    };
    let mut paths: Vec<&String> = before.keys().chain(after.keys()).collect();
    paths.sort_by(|x, y| x.as_bytes().cmp(y.as_bytes()));
    paths.dedup();
    let mut files = Vec::new();
    let mut unchanged = 0u64;
    for path in paths {
        let (b, a) = (before.get(path), after.get(path));
        let change = match (b, a) {
            (Some(x), Some(y)) if x == y => {
                unchanged += 1;
                continue;
            }
            (Some(_), Some(_)) => "changed",
            (None, Some(_)) => "added",
            _ => "removed",
        };
        let text = b.is_none_or(|x| is_text(x)) && a.is_none_or(|y| is_text(y));
        let (lines, limit) = if text {
            let (bl, al) = (split_lines(b), split_lines(a));
            if bl.len() > LINE_DIFF_LIMIT || al.len() > LINE_DIFF_LIMIT {
                (Value::Null, Value::String(LINE_DIFF_LIMIT_TEXT.to_string()))
            } else {
                (Value::from(line_diff(&bl, &al)), Value::Null)
            }
        } else {
            (Value::Null, Value::Null)
        };
        files.push(serde_json::json!({
            "path": path,
            "change": change,
            "before": side(b),
            "after": side(a),
            "text": text,
            "lines": lines,
            "limit": limit,
        }));
    }
    serde_json::json!({
        "files": files,
        "unchanged": unchanged,
        "standing": "difference between the two versions' files; scores and judges nothing",
    })
}

/// TT-11's side of a comparison read from history: turns and endings,
/// commands run and failed, file changes reported, the final agent message.
pub(crate) fn activity_summary(turns: &[TurnRead], turns_limit: Option<&str>) -> Value {
    let mut endings = Vec::new();
    let mut commands = Vec::new();
    let mut failed = 0u64;
    let mut changes = Vec::new();
    let mut final_message: Option<&str> = None;
    let mut limits = Vec::new();
    if let Some(reason) = turns_limit {
        limits.push(format!("turns list incomplete: {reason}"));
    }
    for read in turns {
        let id = str_field(&read.turn, "id").unwrap_or("id not reported");
        let status = read.turn.get("status").cloned().unwrap_or(Value::Null);
        endings.push(serde_json::json!({ "turn": id, "status": status }));
        let items = match &read.items {
            Ok(items) => items,
            Err(reason) => {
                limits.push(format!("turn {id}: items not read ({reason})"));
                continue;
            }
        };
        for item in items {
            match str_field(item, "type").unwrap_or("") {
                "commandExecution" => {
                    let exit = item.get("exitCode").cloned().unwrap_or(Value::Null);
                    let status = item.get("status").cloned().unwrap_or(Value::Null);
                    let nonzero = exit.as_i64().is_some_and(|c| c != 0);
                    let refused = matches!(status.as_str(), Some("failed") | Some("declined"));
                    if nonzero || refused {
                        failed += 1;
                    }
                    commands.push(serde_json::json!({
                        "command": item.get("command").cloned().unwrap_or(Value::Null),
                        "exitCode": exit,
                        "status": status,
                    }));
                }
                "fileChange" => {
                    for (path, kind) in file_changes(item) {
                        changes.push(serde_json::json!({ "path": path, "kind": kind }));
                    }
                }
                "agentMessage" => {
                    if let Some(t) = str_field(item, "text") {
                        final_message = Some(t);
                    }
                }
                _ => {}
            }
        }
    }
    serde_json::json!({
        "turns": turns.len(),
        "endings": endings,
        "commands": { "run": commands.len(), "failed": failed, "list": commands },
        "fileChanges": changes,
        "finalAgentMessage": final_message,
        "limits": limits,
    })
}

#[cfg(test)]
#[path = "workflow_trial_transcript_tests.rs"]
mod tests;

