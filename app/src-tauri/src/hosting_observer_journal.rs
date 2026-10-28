//! Disposable observer replay after the Host's sensitive-data projection.
//!
//! Both positioned source envelopes and diagnostics consume the selected entry
//! and serialized UTF-8 byte budgets. Byte counts include the complete envelope,
//! without a trailing newline; they do not measure Rust heap, unread delivery,
//! held handshake input or input-wire storage. This module changes no protocol
//! admission, source processing, request custody or recording authority.

use serde_json::{json, Value};
use std::collections::VecDeque;
use std::io::{self, Write};
use std::ops::Index;

const DEFAULT_MAX_FRAMES: usize = 4096;
const DEFAULT_MAX_SERIALIZED_BYTES: usize = 16 * 1024 * 1024;

struct Envelope {
    value: Value,
    bytes: usize,
}

// Count the serializer's actual output without allocating a second complete
// serialized copy. Overflow refuses measurement rather than wrapping its size.
#[derive(Default)]
struct SerializedBytes(usize);

impl Write for SerializedBytes {
    fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
        self.0 = self
            .0
            .checked_add(bytes.len())
            .ok_or_else(|| io::Error::other("serialized observer envelope size overflow"))?;
        Ok(bytes.len())
    }

    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

fn serialized_bytes(value: &Value) -> Option<usize> {
    let mut count = SerializedBytes::default();
    serde_json::to_writer(&mut count, value).ok()?;
    Some(count.0)
}

pub(super) struct ObserverJournal {
    scope: Option<Value>,
    entries: VecDeque<Envelope>,
    max_frames: usize,
    max_serialized_bytes: usize,
    retained_bytes: usize,
    delivered: u64,
    omitted: u64,
    omitted_frames: u64,
    omitted_bytes: u64,
    oversized_primary: u64,
    oversized_diagnostic: u64,
    serialization_failures: u64,
}

impl Default for ObserverJournal {
    fn default() -> Self {
        Self::with_limits(DEFAULT_MAX_FRAMES, DEFAULT_MAX_SERIALIZED_BYTES)
    }
}

impl ObserverJournal {
    pub(super) fn with_limits(entries: usize, bytes: usize) -> Self {
        Self {
            scope: None,
            entries: VecDeque::new(),
            max_frames: entries,
            max_serialized_bytes: bytes,
            retained_bytes: 0,
            delivered: 0,
            omitted: 0,
            omitted_frames: 0,
            omitted_bytes: 0,
            oversized_primary: 0,
            oversized_diagnostic: 0,
            serialization_failures: 0,
        }
    }

    // Only the Host begins an actual full source. Incoming JSON never changes
    // scope. Repeating the same source cannot reset its existing omission floor.
    pub(super) fn begin_generation(&mut self, generation: Value) {
        if self.scope.as_ref() == Some(&generation) {
            return;
        }
        *self = Self {
            scope: Some(generation),
            ..Self::with_limits(self.max_frames, self.max_serialized_bytes)
        };
    }

    pub(super) fn scope(&self) -> Option<&Value> {
        self.scope.as_ref()
    }

    fn primary_position(&self, envelope: &Value) -> Option<u64> {
        let generation = self.scope.as_ref()?;
        // Public-only diagnostics can refer to a receipt position too, but
        // only an actual projected native envelope carries a `frame` member.
        // Its content may be malformed/null; this is not protocol admission.
        (envelope.get("frame").is_some() && envelope.get("generation") == Some(generation))
            .then(|| envelope.get("position").and_then(Value::as_u64))
            .flatten()
    }

    fn note_omission(&mut self, position: Option<u64>, bytes: Option<usize>) {
        if let Some(position) = position {
            self.omitted = self.omitted.max(position);
        }
        self.omitted_frames = self.omitted_frames.saturating_add(1);
        if let Some(bytes) = bytes {
            self.omitted_bytes = self
                .omitted_bytes
                .saturating_add(u64::try_from(bytes).unwrap_or(u64::MAX));
        }
    }

    fn evict_front(&mut self) {
        if let Some(envelope) = self.entries.pop_front() {
            self.retained_bytes -= envelope.bytes;
            self.note_omission(self.primary_position(&envelope.value), Some(envelope.bytes));
        }
    }

    pub(super) fn push(&mut self, envelope: Value) {
        let position = self.primary_position(&envelope);
        if let Some(position) = position {
            self.delivered = self.delivered.max(position);
        }
        let Some(bytes) = serialized_bytes(&envelope) else {
            // No exact size can be retained. A primary omission also discards
            // its preceding replay prefix so it cannot hide a receipt hole.
            if position.is_some() {
                self.clear();
            }
            self.serialization_failures = self.serialization_failures.saturating_add(1);
            self.note_omission(position, None);
            return;
        };
        if bytes > self.max_serialized_bytes {
            if position.is_some() {
                self.clear();
                self.oversized_primary = self.oversized_primary.saturating_add(1);
            } else {
                self.oversized_diagnostic = self.oversized_diagnostic.saturating_add(1);
            }
            self.note_omission(position, Some(bytes));
            return;
        }
        // Subtraction is safe after the oversized check. Evict before adding
        // so retained-byte and entry arithmetic cannot wrap at usize::MAX.
        while !self.entries.is_empty()
            && (self.entries.len() >= self.max_frames
                || self.retained_bytes > self.max_serialized_bytes - bytes)
        {
            self.evict_front();
        }
        if self.max_frames == 0 {
            self.note_omission(position, Some(bytes));
            return;
        }
        self.retained_bytes += bytes;
        self.entries.push_back(Envelope {
            value: envelope,
            bytes,
        });
    }

    pub(super) fn extend(&mut self, envelopes: impl IntoIterator<Item = Value>) {
        for envelope in envelopes {
            self.push(envelope);
        }
    }

    pub(super) fn iter(&self) -> impl DoubleEndedIterator<Item = &Value> + ExactSizeIterator + '_ {
        self.entries.iter().map(|envelope| &envelope.value)
    }

    pub(super) fn first(&self) -> Option<&Value> {
        self.entries.front().map(|envelope| &envelope.value)
    }

    pub(super) fn last(&self) -> Option<&Value> {
        self.entries.back().map(|envelope| &envelope.value)
    }

    pub(super) fn get(&self, index: usize) -> Option<&Value> {
        self.entries.get(index).map(|envelope| &envelope.value)
    }

    pub(super) fn len(&self) -> usize {
        self.entries.len()
    }

    pub(super) fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    pub(super) fn clear(&mut self) {
        while !self.entries.is_empty() {
            self.evict_front();
        }
    }

    pub(super) fn omitted_through(&self) -> u64 {
        self.omitted
    }

    pub(super) fn delivered_through(&self) -> u64 {
        self.delivered
    }

    pub(super) fn retention(&self) -> Value {
        json!({
            "generation":self.scope,
            "maxFrames":self.max_frames,"maxSerializedBytes":self.max_serialized_bytes,
            "retainedFrames":self.len(),"retainedSerializedBytes":self.retained_bytes,
            "deliveredThrough":self.delivered,"omittedThrough":self.omitted,
            "omittedFrames":self.omitted_frames,"omittedSerializedBytes":self.omitted_bytes,
            "oversizedPrimaryFrames":self.oversized_primary,"oversizedDiagnosticFrames":self.oversized_diagnostic,
            "serializationFailureFrames":self.serialization_failures,
            "metric":"serialized projected UTF-8 envelope including metadata/unknown fields; no trailing newline",
            "standing":"disposable observer replay; omission counts saturate and exclude unmeasurable bytes; not a total-memory or custody bound"
        })
    }
}

impl Index<usize> for ObserverJournal {
    type Output = Value;

    fn index(&self, index: usize) -> &Self::Output {
        &self.entries[index].value
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn generation(counter: u64) -> Value {
        json!({"appSession":"observer-session","home":"observer-home","spawnCounter":counter})
    }

    fn frame(position: u64) -> Value {
        json!({"generation":generation(1),"position":position,"class":"notification",
            "frame":{"method":"supplier/unknown","params":{"text":"é\n包括\"\\","nested":[null,true,1,1.5]},
                     "emittedAtMs":77,"unknown":{"retained":"unchanged"}},
            "boundaryExtra":{"also":"included"}})
    }

    fn journal(entries: usize, bytes: usize) -> ObserverJournal {
        let mut journal = ObserverJournal::with_limits(entries, bytes);
        journal.begin_generation(generation(1));
        journal
    }

    fn kept(journal: &ObserverJournal) -> Vec<Value> {
        journal.iter().cloned().collect()
    }

    fn bytes(value: &Value) -> usize {
        serde_json::to_vec(value).unwrap().len()
    }

    #[test]
    fn selected_defaults_and_empty_replay_metadata_are_explicit() {
        let journal = ObserverJournal::default();
        assert!(journal.is_empty());
        assert_eq!(journal.scope(), None);
        assert_eq!(journal.delivered_through(), 0);
        assert_eq!(journal.omitted_through(), 0);
        let retention = journal.retention();
        assert_eq!(retention["maxFrames"], 4096);
        assert_eq!(retention["maxSerializedBytes"], 16 * 1024 * 1024);
        assert_eq!(retention["retainedSerializedBytes"], 0);
    }

    #[test]
    fn entry_bound_keeps_exact_suffix_and_floor_boundary() {
        let mut journal = journal(2, usize::MAX);
        let first = frame(1);
        let second = frame(2);
        let third = frame(3);
        journal.extend([first.clone(), second.clone()]);
        assert_eq!(kept(&journal), vec![first, second.clone()]);
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (0, 2)
        );
        journal.push(third.clone());
        assert_eq!(kept(&journal), vec![second.clone(), third.clone()]);
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (1, 3)
        );
        // Exactly the omitted-through cursor remains a continuity boundary:
        // replay after it is the complete retained primary suffix.
        let after_floor = journal
            .iter()
            .filter(|value| value["position"].as_u64().unwrap() > journal.omitted_through())
            .cloned()
            .collect::<Vec<_>>();
        assert_eq!(after_floor, vec![second, third]);
        assert_eq!(journal.retention()["omittedFrames"], 1);
    }

    #[test]
    fn byte_bound_counts_utf8_escaping_metadata_and_unknown_fields_without_newline() {
        let first = frame(1);
        let second = frame(2);
        let total = bytes(&first) + bytes(&second);
        assert_eq!(serialized_bytes(&first), Some(bytes(&first)));
        assert_ne!(
            bytes(&first),
            serde_json::to_string(&first).unwrap().chars().count()
        );
        let mut exact = journal(10, total);
        exact.extend([first.clone(), second.clone()]);
        assert_eq!(kept(&exact), vec![first.clone(), second.clone()]);
        assert_eq!(exact.retention()["retainedSerializedBytes"], total);
        let mut one_less = journal(10, total - 1);
        one_less.extend([first, second.clone()]);
        assert_eq!(kept(&one_less), vec![second.clone()]);
        assert_eq!(
            one_less.retention()["retainedSerializedBytes"],
            bytes(&second)
        );
        assert_eq!(one_less.omitted_through(), 1);
    }

    #[test]
    fn both_budgets_apply_and_diagnostics_cannot_form_an_unbounded_side_channel() {
        let primary = frame(1);
        let diagnostic = json!({"class":"unpositioned","reason":"bounded diagnostic"});
        // Isolate each limit so one cannot conceal a missing diagnostic budget.
        for (entries, byte_limit) in [(2, usize::MAX), (10, bytes(&primary) + bytes(&diagnostic))] {
            let mut journal = journal(entries, byte_limit);
            journal.extend([primary.clone(), diagnostic.clone(), diagnostic.clone()]);
            assert_eq!(kept(&journal), vec![diagnostic.clone(), diagnostic.clone()]);
            assert_eq!(journal.omitted_through(), 1);
            assert_eq!(journal.delivered_through(), 1);
            assert_eq!(journal.len(), 2);
            assert_eq!(
                journal.retention()["retainedSerializedBytes"],
                2 * bytes(&diagnostic)
            );
        }
    }

    #[test]
    fn oversized_primary_is_omitted_whole_and_discards_preceding_replay_prefix() {
        let first = frame(1);
        let diagnostic = json!({"class":"unpositioned","extra":"preceding diagnostic"});
        let mut journal = journal(10, bytes(&first) + bytes(&diagnostic));
        journal.extend([first.clone(), diagnostic.clone()]);
        let mut oversized = frame(2);
        oversized["frame"]["params"]["text"] = json!("x".repeat(2048));
        journal.push(oversized.clone());
        assert!(journal.is_empty());
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (2, 2)
        );
        let retention = journal.retention();
        assert_eq!(retention["oversizedPrimaryFrames"], 1);
        assert_eq!(retention["omittedFrames"], 3);
        assert_eq!(
            retention["omittedSerializedBytes"],
            bytes(&first) + bytes(&diagnostic) + bytes(&oversized)
        );
        let later = frame(3);
        journal.push(later.clone());
        assert_eq!(kept(&journal), vec![later]);
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (2, 3)
        );
        assert_eq!(
            oversized["frame"]["params"]["text"].as_str().unwrap().len(),
            2048
        );
    }

    #[test]
    fn oversized_unpositioned_or_foreign_diagnostic_does_not_discard_primary_prefix() {
        let primary = frame(1);
        let mut journal = journal(10, bytes(&primary));
        journal.push(primary.clone());
        let unpositioned =
            json!({"generation":generation(1),"class":"unpositioned","extra":"x".repeat(2048)});
        let mut foreign = frame(u64::MAX);
        foreign["generation"] = generation(2);
        foreign["frame"]["params"]["text"] = json!("x".repeat(2048));
        journal.extend([unpositioned, foreign]);
        assert_eq!(kept(&journal), vec![primary]);
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (0, 1)
        );
        assert_eq!(journal.retention()["oversizedDiagnosticFrames"], 2);
        assert_eq!(journal.scope(), Some(&generation(1)));
    }

    #[test]
    fn positioned_public_diagnostics_count_both_budgets_without_source_coverage() {
        let primary = frame(1);
        let diagnostic = json!({"generation":generation(1),"position":u64::MAX,
            "class":"private-auth-request-reply","replyWriteResult":"written"});
        for (entries, byte_limit) in [(2, usize::MAX), (10, bytes(&primary) + bytes(&diagnostic))] {
            let mut journal = journal(entries, byte_limit);
            journal.extend([primary.clone(), diagnostic.clone()]);
            assert_eq!(kept(&journal), vec![primary.clone(), diagnostic.clone()]);
            assert_eq!(
                (journal.omitted_through(), journal.delivered_through()),
                (0, 1)
            );
            assert_eq!(
                journal.retention()["retainedSerializedBytes"],
                bytes(&primary) + bytes(&diagnostic)
            );
            journal.push(diagnostic.clone());
            assert_eq!(kept(&journal), vec![diagnostic.clone(), diagnostic.clone()]);
            assert_eq!(
                (journal.omitted_through(), journal.delivered_through()),
                (1, 1)
            );
            journal.clear();
            assert_eq!(
                (journal.omitted_through(), journal.delivered_through()),
                (1, 1)
            );
        }
    }

    #[test]
    fn oversized_positioned_auth_diagnostic_cannot_drop_primary_prefix_or_make_a_hole() {
        let primary = frame(1);
        let mut journal = journal(10, bytes(&primary));
        journal.push(primary.clone());
        let diagnostic = json!({"generation":generation(1),"position":u64::MAX,
            "class":"private-auth-request-reply","unknown":"x".repeat(2048)});
        journal.push(diagnostic.clone());
        assert_eq!(kept(&journal), vec![primary]);
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (0, 1)
        );
        assert_eq!(journal.retention()["oversizedDiagnosticFrames"], 1);
        assert_eq!(journal.retention()["oversizedPrimaryFrames"], 0);
        assert_eq!(
            journal.retention()["omittedSerializedBytes"],
            bytes(&diagnostic)
        );
        // A malformed/null native frame still belongs to source receipt order.
        journal.push(
            json!({"generation":generation(1),"position":2,"class":"malformed","frame":null}),
        );
        assert_eq!(journal.delivered_through(), 2);
        journal.clear();
        assert_eq!(journal.omitted_through(), 2);
    }

    #[test]
    fn full_source_and_position_qualification_alone_advance_highwater_and_floor() {
        let mut journal = journal(1, usize::MAX);
        journal.push(frame(4));
        let mut diagnostics = vec![json!({"position":u64::MAX,"class":"missing-generation"})];
        for field in ["home", "appSession", "spawnCounter"] {
            let mut foreign = frame(u64::MAX);
            foreign["generation"][field] = if field == "spawnCounter" {
                json!(2)
            } else {
                json!("foreign")
            };
            diagnostics.push(foreign);
        }
        for position in [
            Value::Null,
            json!("999"),
            json!(-1),
            json!(1.5),
            json!(true),
        ] {
            let mut diagnostic = frame(999);
            diagnostic["position"] = position;
            diagnostics.push(diagnostic);
        }
        diagnostics.push(
            json!({"generation":generation(1),"receiptPosition":u64::MAX,"class":"unpositioned"}),
        );
        for diagnostic in diagnostics {
            journal.push(diagnostic);
            assert_eq!(
                (journal.omitted_through(), journal.delivered_through()),
                (4, 4)
            );
            assert_eq!(journal.scope(), Some(&generation(1)));
        }
        journal.clear();
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (4, 4)
        );
    }

    #[test]
    fn clear_advances_floor_without_resetting_highwater_or_diagnostics() {
        let mut journal = journal(10, usize::MAX);
        journal.extend([frame(1), frame(2), json!({"class":"diagnostic"})]);
        journal.clear();
        assert!(journal.is_empty());
        assert_eq!(journal.retention()["retainedSerializedBytes"], 0);
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (2, 2)
        );
        assert_eq!(journal.retention()["omittedFrames"], 3);
        journal.clear();
        assert_eq!(journal.retention()["omittedFrames"], 3);
        journal.push(frame(3));
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (2, 3)
        );
    }

    #[test]
    fn actual_source_change_resets_storage_and_counters_but_same_scope_is_idempotent() {
        let mut journal = journal(1, usize::MAX);
        journal.extend([frame(1), frame(2)]);
        journal.begin_generation(generation(1));
        assert_eq!(kept(&journal), vec![frame(2)]);
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (1, 2)
        );
        journal.begin_generation(generation(2));
        assert!(journal.is_empty());
        assert_eq!(journal.scope(), Some(&generation(2)));
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (0, 0)
        );
        assert_eq!(journal.retention()["omittedFrames"], 0);
        assert_eq!(journal.retention()["retainedSerializedBytes"], 0);
        // Late old-source input is diagnostic and cannot re-scope the journal.
        journal.push(frame(u64::MAX));
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (0, 0)
        );
        assert_eq!(journal.scope(), Some(&generation(2)));
        let mut actual = frame(1);
        actual["generation"] = generation(2);
        journal.push(actual.clone());
        assert_eq!(kept(&journal), vec![actual]);
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (0, 1)
        );
    }

    #[test]
    fn no_implicit_scope_and_zero_or_tiny_test_budgets_are_truthful() {
        let mut unscoped = ObserverJournal::with_limits(0, usize::MAX);
        unscoped.push(frame(99));
        assert_eq!(
            (unscoped.omitted_through(), unscoped.delivered_through()),
            (0, 0)
        );
        assert_eq!(unscoped.scope(), None);
        for (entries, bytes) in [(0, usize::MAX), (10, 0), (0, 0), (1, 1)] {
            let mut journal = journal(entries, bytes);
            journal.push(frame(7));
            assert!(journal.is_empty());
            assert_eq!(journal.retention()["retainedSerializedBytes"], 0);
            assert_eq!(
                (journal.omitted_through(), journal.delivered_through()),
                (7, 7)
            );
        }
    }

    #[test]
    fn public_iteration_and_indexing_preserve_values_in_source_order() {
        let mut journal = journal(3, usize::MAX);
        let original = [frame(1), frame(2), frame(3)];
        journal.extend(original.clone());
        assert_eq!(journal.iter().len(), 3);
        assert_eq!(journal.first(), Some(&original[0]));
        assert_eq!(journal.last(), Some(&original[2]));
        assert_eq!(journal.get(1), Some(&original[1]));
        assert_eq!(journal.get(3), None);
        assert_eq!(journal[1], original[1]);
        assert_eq!(
            journal.iter().rev().cloned().collect::<Vec<_>>(),
            original.iter().rev().cloned().collect::<Vec<_>>()
        );
        assert_eq!(kept(&journal), original);
        assert_eq!(
            journal.retention()["retainedSerializedBytes"],
            original.iter().map(bytes).sum::<usize>()
        );
    }

    #[test]
    fn highwater_uses_supplied_max_positions_and_diagnostic_counters_saturate() {
        let mut journal = journal(0, usize::MAX);
        journal.omitted_frames = u64::MAX - 1;
        journal.omitted_bytes = u64::MAX - 1;
        journal.push(frame(u64::MAX));
        journal.push(frame(u64::MAX));
        assert_eq!(
            (journal.omitted_through(), journal.delivered_through()),
            (u64::MAX, u64::MAX)
        );
        assert_eq!(journal.retention()["omittedFrames"], u64::MAX);
        assert_eq!(journal.retention()["omittedSerializedBytes"], u64::MAX);
        let mut counter = SerializedBytes(usize::MAX);
        assert!(counter.write(b"x").is_err());
        assert_eq!(counter.0, usize::MAX);
    }
}
