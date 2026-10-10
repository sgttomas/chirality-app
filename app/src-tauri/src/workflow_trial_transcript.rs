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

/// TT-10's transcript within `input.bound`.
pub(crate) fn compose_transcript(input: &TranscriptInput) -> Transcript {
    let _ = input;
    unimplemented!("WR §17 step 7")
}

/// TT-11's version difference: per-file line difference for UTF-8 text
/// files, size and digest for others.
pub(crate) fn version_difference(before: &BTreeMap<String, Vec<u8>>, after: &BTreeMap<String, Vec<u8>>) -> Value {
    let _ = (before, after);
    unimplemented!("WR §17 step 8")
}

/// TT-11's side of a comparison read from history: turns and endings,
/// commands run and failed, file changes reported, the final agent message.
pub(crate) fn activity_summary(turns: &[TurnRead], turns_limit: Option<&str>) -> Value {
    let _ = (turns, turns_limit);
    unimplemented!("WR §17 step 8")
}
