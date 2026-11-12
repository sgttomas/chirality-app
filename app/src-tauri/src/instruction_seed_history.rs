//! Declared initial seed history, separate from reviewed-default classification.
use super::{content, Role, CONTENT_METHOD, DELEGATION_GUIDANCE_PATH};
use serde::Deserialize;
use serde_json::{json, Value};
use std::collections::BTreeSet;

pub(super) const MAX_BYTES: u64 = 16 * 1024;
/// The record the first seed of a store writes once.
pub(crate) const SEED_RECORD: &str = ".seed-record.json";
pub(crate) const SEED_FORMAT: &str = "chirality.instruction-seed-record/1";

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

/// The paths a first seed record names: the five of a store first seeded
/// before the delegation guidance was shipped, or the six of one seeded since.
fn seeded_sets() -> [BTreeSet<String>; 2] {
    let before: BTreeSet<String> = std::iter::once("AGENTS.md".to_owned())
        .chain(Role::ALL.iter().map(|r| format!("agents/AGENT_{}.md", r.name()))).collect();
    let mut since = before.clone();
    since.insert(DELEGATION_GUIDANCE_PATH.to_owned());
    [before, since]
}

/// The paths a first seed record names, when it is valid: either set above.
fn parse(raw: &[u8]) -> Option<BTreeSet<String>> {
    // Struct deserialization rejects duplicate and unexpected fields.
    let record: Record = serde_json::from_slice(raw).ok()?;
    if record.format != SEED_FORMAT || record.release.is_empty() { return None; }
    let mut seen = BTreeSet::new();
    for entry in &record.created {
        if !super::guidance_path(&entry.path) || !seen.insert(entry.path.clone())
            || entry.default_content.method != CONTENT_METHOD
            || entry.default_content.value.len() != 64
            || !entry.default_content.value.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)) { return None; }
    }
    for entry in &record.preserved {
        if !super::guidance_path(&entry.path) || !seen.insert(entry.path.clone()) || entry.origin != "unknown" { return None; }
    }
    seeded_sets().contains(&seen).then_some(seen)
}

pub(super) fn unknown(reason: &str) -> Value {
    json!({"status":"unestablished","reason":reason})
}

pub(super) fn report(raw: &[u8], path: &str, supplied: &[u8]) -> Value {
    let parsed = (|| -> Option<Value> {
        let seen = parse(raw)?;
        if !seen.contains(path) {
            // A first seed record from before the delegation guidance was
            // shipped declares nothing of it.
            return Some(unknown("missing"));
        }
        let record: Record = serde_json::from_slice(raw).ok()?;
        let Some(entry) = record.created.iter().find(|e| e.path == path) else {
            return Some(unknown("preserved-path"));
        };
        let default = json!({"method":entry.default_content.method,"value":entry.default_content.value});
        Some(json!({"status":"declared","standing":"mutable seed-record declaration; creation custody not authenticated",
            "record":{"path":SEED_RECORD,"content":content(raw)},
            "release":record.release,"defaultContent":default,
            "matchesSuppliedContent":content(supplied)==default}))
    })();
    parsed.unwrap_or_else(|| unknown("invalid"))
}
