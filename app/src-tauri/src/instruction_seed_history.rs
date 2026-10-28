//! Declared initial seed history, separate from reviewed-default classification.
use super::{content, Role, CONTENT_METHOD};
use serde::Deserialize;
use serde_json::{json, Value};
use std::collections::BTreeSet;

pub(super) const MAX_BYTES: u64 = 16 * 1024;

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Identity { method: String, value: String }
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Created {
    path: String,
    #[serde(rename = "defaultContent")]
    default_content: Identity,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Preserved { path: String, origin: String }
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Record { format: String, release: String, created: Vec<Created>, preserved: Vec<Preserved> }

pub(super) fn unknown(reason: &str) -> Value {
    json!({"status":"unestablished","reason":reason})
}

pub(super) fn report(raw: &[u8], path: &str, supplied: &[u8]) -> Value {
    let parsed = (|| -> Option<Value> {
        // Struct deserialization rejects duplicate and unexpected fields.
        let record: Record = serde_json::from_slice(raw).ok()?;
        if record.format != "chirality.instruction-seed-record/1" || record.release.is_empty() { return None; }
        let expected: BTreeSet<String> = std::iter::once("AGENTS.md".to_owned())
            .chain(Role::ALL.iter().map(|r| format!("agents/AGENT_{}.md", r.name()))).collect();
        let mut seen = BTreeSet::new();
        for entry in &record.created {
            if !expected.contains(&entry.path) || !seen.insert(entry.path.clone())
                || entry.default_content.method != CONTENT_METHOD
                || entry.default_content.value.len() != 64
                || !entry.default_content.value.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)) { return None; }
        }
        for entry in &record.preserved {
            if !expected.contains(&entry.path) || !seen.insert(entry.path.clone()) || entry.origin != "unknown" { return None; }
        }
        if seen != expected { return None; }
        let Some(entry) = record.created.iter().find(|e| e.path == path) else {
            return Some(unknown("preserved-path"));
        };
        let default = json!({"method":entry.default_content.method,"value":entry.default_content.value});
        Some(json!({"status":"declared","standing":"mutable seed-record declaration; creation custody not authenticated",
            "record":{"path":".seed-record.json","content":content(raw)},
            "release":record.release,"defaultContent":default,
            "matchesSuppliedContent":content(supplied)==default}))
    })();
    parsed.unwrap_or_else(|| unknown("invalid"))
}
