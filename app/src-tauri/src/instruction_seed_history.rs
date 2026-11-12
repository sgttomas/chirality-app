//! Declared initial seed history, separate from reviewed-default classification.
use super::{content, Role, CONTENT_METHOD, DELEGATION_GUIDANCE_PATH};
use serde::Deserialize;
use serde_json::{json, Value};
use std::collections::BTreeSet;

pub(super) const MAX_BYTES: u64 = 16 * 1024;
/// The record the first seed of a store writes once.
pub(crate) const SEED_RECORD: &str = ".seed-record.json";
pub(crate) const SEED_FORMAT: &str = "chirality.instruction-seed-record/1";
/// The record written once when a later release adds a file to a store that
/// was first seeded without it.
pub(crate) const ADDITION_FORMAT: &str = "chirality.instruction-seed-addition/1";
const DELEGATION_ADDITION: &str = ".seed-addition-DELEGATION_RECORDS.json";
/// The marker that a later addition was begun. It is no record of a placement.
pub(crate) const ADDITION_BEGUN_FORMAT: &str = "chirality.instruction-seed-addition-begun/1";
const DELEGATION_ADDITION_BEGUN: &str = ".seed-addition-DELEGATION_RECORDS.begun.json";

/// The addition record of a file a later release adds to an existing store.
pub(crate) fn addition_record(path: &str) -> Option<&'static str> {
    (path == DELEGATION_GUIDANCE_PATH).then_some(DELEGATION_ADDITION)
}
/// The marker written before a later-added file is made visible, and removed
/// once its addition record is written. It claims only that the placement
/// was begun.
pub(crate) fn addition_begun(path: &str) -> Option<&'static str> {
    (path == DELEGATION_GUIDANCE_PATH).then_some(DELEGATION_ADDITION_BEGUN)
}

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

/// The paths the first seed record names, when it is well formed.
pub(crate) fn seeded_paths(raw: &[u8]) -> Option<BTreeSet<String>> {
    parse(SEED_RECORD, raw)
}

fn parse(name: &str, raw: &[u8]) -> Option<BTreeSet<String>> {
    // Struct deserialization rejects duplicate and unexpected fields.
    let record: Record = serde_json::from_slice(raw).ok()?;
    if record.release.is_empty() { return None; }
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
    let valid = if name == SEED_RECORD {
        record.format == SEED_FORMAT && seeded_sets().contains(&seen)
    } else {
        record.format == ADDITION_FORMAT && seen.len() == 1
            && seen.iter().all(|p| addition_record(p) == Some(name))
    };
    valid.then_some(seen)
}

pub(super) fn unknown(reason: &str) -> Value {
    json!({"status":"unestablished","reason":reason})
}

pub(super) fn report(name: &str, raw: &[u8], path: &str, supplied: &[u8]) -> Value {
    let parsed = (|| -> Option<Value> {
        let seen = parse(name, raw)?;
        if !seen.contains(path) {
            // A first seed record that predates this file declares nothing
            // of it; its addition record is the one that would.
            return Some(unknown("missing"));
        }
        let record: Record = serde_json::from_slice(raw).ok()?;
        let Some(entry) = record.created.iter().find(|e| e.path == path) else {
            return Some(unknown("preserved-path"));
        };
        let default = json!({"method":entry.default_content.method,"value":entry.default_content.value});
        Some(json!({"status":"declared","standing":"mutable seed-record declaration; creation custody not authenticated",
            "record":{"path":name,"content":content(raw)},
            "release":record.release,"defaultContent":default,
            "matchesSuppliedContent":content(supplied)==default}))
    })();
    parsed.unwrap_or_else(|| unknown("invalid"))
}
