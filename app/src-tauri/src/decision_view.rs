//! Decision view model, derived from files only.
//!
//! DEL-06-02 DECISION_VIEW.md (DV-v0.1) §3 DV-1…DV-9, §4 row states, §6 failure
//! behaviour. A port of the Pass 4 prototype `E/decision_view.py`. It reads the RS
//! log and the package files the records cite; it writes nothing (DV-9).

#[path = "record_relations.rs"]
pub mod record_relations;

use crate::act_policy::ContentIdentity;
use crate::records;
use crate::standing::{compare, CurrentContent, Lapse};
use crate::util::{sha256_hex, FILE_IDENTITY_METHOD};
use serde_json::{json, Value};
use std::collections::{HashMap, HashSet};
use std::path::Path;

const PERSON_WORDING: &str = "identity not verified";
/// Row states. The two incomplete states are never a decision or a pending
/// request: an act log that could bear on the row was not fully read.
pub(crate) const PENDING: &str = "pending — awaiting the person's decision";
/// Every row read while an act log was not fully read begins with this.
pub(crate) const INCOMPLETE_PREFIX: &str = "act records incomplete; ";
pub(crate) const DECIDED_INCOMPLETE: &str = "act records incomplete; a deciding act was read";
pub(crate) const PENDING_INCOMPLETE: &str = "act records incomplete; no deciding act was read";
/// A decision whose package file's current bytes are not the content decided.
pub(crate) const LAPSED: &str = "decision lapsed — the package file is not the content decided";
/// A decision the package file's current bytes cannot confirm.
pub(crate) const PACKAGE_UNRESOLVED: &str =
    "unresolved — the package file's current bytes cannot confirm the decision";
/// An act whose bound content is not the package identity its request claims.
pub(crate) const BINDING_UNRESOLVED: &str =
    "unresolved — an act's bound content is not its request's package identity";

pub fn person_label(p: &Value) -> String {
    let names: Vec<&str> = ["displayName", "osAccount", "codexAccount", "hostActor"]
        .iter()
        .filter_map(|k| p.get(*k).and_then(|v| v.as_str()).filter(|s| !s.is_empty()))
        .collect();
    let who = if names.is_empty() {
        "person not named".to_string()
    } else {
        names.join(" / ")
    };
    // This reader verifies no identity, so it never shows one as verified; a
    // record that says otherwise is reported as saying so.
    if p.get("identityVerified") == Some(&json!(true)) {
        format!("{who} ({PERSON_WORDING}; the record claims it verified, a claim this reader does not verify)")
    } else {
        format!("{who} ({PERSON_WORDING})")
    }
}

/// One coherent current buffer; no record, capture, or native-origin admission.
#[derive(Clone)]
pub(crate) struct FileObservation {
    pub identity: Option<ContentIdentity>,
    pub absent: bool,
    /// The bytes read once, from which the package's own facts are taken.
    pub bytes: Option<Vec<u8>>,
}
impl FileObservation {
    /// The identity of bytes the caller has read once.
    pub(crate) fn of(bytes: Option<&[u8]>, absent: bool) -> Self {
        FileObservation {
            identity: bytes.map(|b| ContentIdentity {
                method: FILE_IDENTITY_METHOD.into(),
                value: sha256_hex(b),
            }),
            absent,
            bytes: bytes.map(<[u8]>::to_vec),
        }
    }
}
fn observe_file(root: &Path, reference: &str, limits: &mut Vec<String>) -> FileObservation {
    let rel = Path::new(reference);
    if reference.is_empty()
        || rel.is_absolute()
        || rel
            .components()
            .any(|c| !matches!(c, std::path::Component::Normal(_)))
    {
        limits.push(
            "package file reference is not a contained relative path; content not observed".into(),
        );
        return FileObservation::of(None, false);
    }
    let path = root.join(rel);
    if let Err(e) = crate::storage::check_path(&path) {
        limits.push(format!("package file content not observed: {e}"));
        return FileObservation::of(None, false);
    }
    match std::fs::read(path) {
        Ok(bytes) => FileObservation::of(Some(&bytes), false),
        Err(e) => FileObservation::of(None, e.kind() == std::io::ErrorKind::NotFound),
    }
}
fn identity(value: &Value) -> ContentIdentity {
    ContentIdentity {
        method: value["method"].as_str().unwrap_or("").into(),
        value: value["value"].as_str().unwrap_or("").into(),
    }
}
fn label(state: Lapse) -> &'static str {
    match state {
        Lapse::NotLapsed => "not lapsed",
        Lapse::Lapsed => "lapsed — the package changed after the decision",
        Lapse::SubjectAbsent => "lapsed (subject absent)",
        Lapse::MatchesAgainAfterLapse => "matches c0 again after observed lapse",
        Lapse::Incomparable => "unknown (incomparable)",
        Lapse::Unavailable => "unknown (unavailable)",
        Lapse::NotEvaluated => "not yet evaluated",
    }
}
/// Recorded lapse observations are claims too. Match the exact act, kind,
/// referent and original method/value; another act/package supplies no history.
fn lapse_history<'a>(
    entries: &'a [Value],
    act_id: &str,
    subject: &str,
    bound: &ContentIdentity,
    unresolved: &HashSet<String>,
) -> Vec<&'a Value> {
    entries
        .iter()
        .filter(|e| {
            let b = &e["body"];
            e["kind"] == "act_lapsed"
                && !unresolved.contains(e["recordId"].as_str().unwrap_or(""))
                && b["act"]["recordId"] == act_id
                && b["act"]["actKind"] == "A16"
                && b["referents"]
                    .as_array()
                    .is_some_and(|v| v.len() == 1 && v[0] == subject)
                && identity(&b["c0"]) == *bound
                && match b["state"].as_str() {
                    Some("lapsed" | "partially lapsed") => {
                        let changed = identity(&b["c1"]);
                        changed.method == bound.method
                            && !changed.value.is_empty()
                            && changed.value != bound.value
                    }
                    Some("lapsed (subject absent)") => b["c1"] == "subject absent",
                    _ => false,
                }
        })
        .collect()
}

fn same_capture(a: &Value, b: &Value) -> bool {
    let refs = |e: &Value| {
        e["body"]["captureEvidence"]
            .as_array()
            .map(|v| {
                v.iter()
                    .filter_map(|x| x["ref"].as_str().map(str::to_owned))
                    .collect::<HashSet<_>>()
            })
            .unwrap_or_default()
    };
    let a = refs(a);
    let b = refs(b);
    !a.is_empty() && a == b
}
fn reported_native_observation(e: &Value) -> bool {
    e["kind"] == "human_act"
        && e["body"]["actKind"] == "A16"
        && e["body"]["recordingMode"] == "direct capture"
        && e["recorder"]["role"] == records::APP_INTERFACE.role
        && e["recorder"]["identity"] == records::APP_INTERFACE.identity
        && e["observedAt"]
            .as_str()
            .is_some_and(|at| !at.is_empty() && e["body"]["captureTime"] == at)
}
fn same_capture_facts(a: &Value, b: &Value) -> bool {
    [
        "actKind",
        "actClass",
        "decisionActor",
        "boundSubject",
        "boundContent",
        "scope",
        "purpose",
        "captureTime",
    ]
    .iter()
    .all(|key| a["body"][key] == b["body"][key])
        && a["body"]["relations"]["requestRef"] == b["body"]["relations"]["requestRef"]
        && a["body"]["relations"]["alternativeChosen"]
            == b["body"]["relations"]["alternativeChosen"]
}
fn reaches(from: &str, target: &str, edges: &HashMap<String, Vec<String>>) -> bool {
    let mut todo = vec![from.to_owned()];
    let mut seen = HashSet::new();
    while let Some(at) = todo.pop() {
        if !seen.insert(at.clone()) {
            continue;
        }
        if let Some(next) = edges.get(&at) {
            if next.iter().any(|v| v == target) {
                return true;
            }
            todo.extend(next.iter().cloned());
        }
    }
    false
}

/// Where a record was read. Only an act in this installation's records store,
/// outside every imported prefix, can decide a package (DEL-04-03 Record
/// authority and REQ-010). Every other origin is listed as a claim.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub(crate) enum Origin {
    /// This installation's records store subtree for the project.
    Store,
    /// The project folder, which agents can write.
    ProjectFile,
    /// Inside the prefix a package import brought into the store.
    PackageImport,
    /// A copy the explicit legacy import brought in from the project folder.
    LegacyImport,
    /// The import accounting could not be read or no longer matches.
    Unknown,
}
impl Origin {
    pub(crate) fn label(self) -> &'static str {
        match self {
            Origin::Store => "this installation's records store",
            Origin::ProjectFile => "project-file claim",
            Origin::PackageImport => "imported package record (quoted evidence)",
            Origin::LegacyImport => "legacy-imported copy of a project file (quoted evidence)",
            Origin::Unknown => "origin not established",
        }
    }
}
/// The one rule for which origins may decide a package, kept in this one
/// place. As App Agent 0 decided: an act log that reached the store through
/// the explicit legacy import is quoted evidence only and never decides
/// anything, since an imported copy carries only the trust of the project
/// folder it came from (`records_store::IMPORT_STANDING`). Library
/// registration acts are not read by this view.
fn origin_decides(origin: Origin) -> bool {
    origin == Origin::Store
}
/// DEL-04-01 Person's acts and DEL-04-03 CLM-003: a record that names its
/// recorder as the decision actor is not conformant and is not an act.
fn names_recorder(act: &Value) -> bool {
    let Some(recorder) = act["recorder"]["identity"]
        .as_str()
        .map(str::trim)
        .filter(|s| !s.is_empty())
    else {
        return false;
    };
    // The standard library's full case mapping, upper then lower, after
    // trimming: STRASSE and Straße, and the Greek sigma forms, compare equal.
    // No normalization form is applied: composed and decomposed spellings of
    // one name compare as different. This is a conformance check of what the
    // record says; it authenticates no one.
    let fold = |s: &str| s.trim().to_uppercase().to_lowercase();
    let recorder = fold(recorder);
    ["displayName", "osAccount", "codexAccount", "hostActor"]
        .iter()
        .filter_map(|k| act["body"]["decisionActor"][*k].as_str())
        .any(|name| fold(name) == recorder)
}
/// The door. Every act-record line is classified here, once, into exactly one
/// of three classes, before any derivation sees it.
mod door {
    use super::{names_recorder, origin_decides, Origin};
    use serde_json::{json, Value};

    /// A record line the door admitted: read from this installation's store
    /// subtree for the project, outside every imported part that a whole and
    /// valid import account establishes, schema-conformant (it was read), and
    /// not naming its recorder as the decision actor. Its fields are private to
    /// this module and `classify` is its only constructor, so the derivation,
    /// which takes only this type, cannot be handed a claim or a record of
    /// unestablished origin.
    pub(crate) struct Authorized {
        record: Value,
        source: Value,
    }
    impl Authorized {
        pub(crate) fn record(&self) -> &Value {
            &self.record
        }
        pub(crate) fn source(&self) -> &Value {
            &self.source
        }
    }
    /// The linking facts of a decision request that is a claim, and nothing
    /// else a decision could rest on: an imported request can link, and can
    /// fail to link, and supplies none of the facts a decision rests on. Its
    /// body is kept for display only, marked as that request's claim.
    pub(crate) struct RequestLink {
        pub(crate) id: String,
        pub(crate) file: String,
        pub(crate) method: String,
        pub(crate) value: String,
        pub(crate) origin: Origin,
        pub(crate) shown: Value,
        pub(crate) source: Value,
    }
    pub(crate) enum Classified {
        Authorized(Authorized),
        /// Known not to be authorized.
        Claim { record: Value, source: Value, origin: Origin, reason: String },
        /// Its origin cannot be established.
        NotEstablished { record: Value, source: Value, reason: String },
    }
    pub(crate) fn classify(record: Value, source: Value, origin: Origin, why: Option<String>) -> Classified {
        if origin == Origin::Unknown {
            let reason = why.unwrap_or_else(|| origin.label().to_owned());
            return Classified::NotEstablished { record, source, reason };
        }
        if !origin_decides(origin) {
            return Classified::Claim { record, source, origin, reason: origin.label().to_owned() };
        }
        if names_recorder(&record) {
            let reason = format!(
                "the record names its recorder {} as the decision actor (nonconformant)",
                record["recorder"]["identity"].as_str().unwrap_or("?")
            );
            return Classified::Claim { record, source, origin, reason };
        }
        Classified::Authorized(Authorized { record, source })
    }
    /// A claim that is a decision request may link a row; nothing more.
    pub(crate) fn link(record: &Value, source: &Value, origin: Origin) -> Option<RequestLink> {
        if record["kind"] != "act_request" || record["body"].get("alternatives").is_none() {
            return None;
        }
        let ev = &record["body"]["evidence"];
        Some(RequestLink {
            id: record["recordId"].as_str()?.to_owned(),
            file: ev["ref"].as_str().unwrap_or("").to_owned(),
            method: ev["method"].as_str().unwrap_or("").to_owned(),
            value: ev["claimedIdentity"].as_str().unwrap_or("").to_owned(),
            origin,
            shown: record["body"].clone(),
            source: json!(source),
        })
    }
}

/// One act log as the caller read it, once.
pub(crate) struct LogSource {
    pub path: std::path::PathBuf,
    pub bytes: Result<Vec<u8>, String>,
}
/// The record sources a decision read is handed.
pub(crate) struct RecordSet {
    pub logs: Vec<LogSource>,
    /// The project's subtree of this installation's records store, when the
    /// store holds the project's records; `None` when they are read in place.
    pub store_dir: Option<std::path::PathBuf>,
    /// The subtree's `imports.jsonl`, absent as `Ok(None)`.
    pub imports: Result<Option<Vec<u8>>, String>,
    pub limits: Vec<String>,
}

/// The copies the explicit legacy import named, by store-relative path, each
/// with the length and SHA-256 of the bytes it copied. Read strictly: anything
/// not whole and well formed leaves origins unestablished, never "no imports".
/// An absent account (the caller passes none) is a project that never imported.
fn legacy_copies(bytes: &[u8]) -> Result<HashMap<String, Vec<(u64, String)>>, String> {
    if bytes.iter().all(u8::is_ascii_whitespace) {
        return Err("the project's import account is present but empty".into());
    }
    if !bytes.ends_with(b"\n") {
        return Err("the project's import account ends in a torn line".into());
    }
    let bad = |why: &str| Err(format!("the project's import account is not well formed: {why}"));
    let mut lines = Vec::new();
    for line in bytes.split(|b| *b == b'\n').filter(|l| !l.is_empty()) {
        let Ok(line) = serde_json::from_slice::<Value>(line) else {
            return bad("a line is not JSON");
        };
        if line["format"] != "chirality.records-store.import"
            || line["importId"].as_str().is_none_or(str::is_empty)
        {
            return bad("a line is not an import event");
        }
        let member = match line["event"].as_str() {
            Some("started") => "census",
            Some("completed") => "files",
            _ => return bad("a line is neither a started nor a completed event"),
        };
        let Some(files) = line[member].as_array() else {
            return bad(&format!("a {} event has no {member} list", line["event"].as_str().unwrap_or("")));
        };
        for file in files {
            let well_formed = file["copy"].as_str().is_some_and(|c| !c.is_empty())
                && file["sha256"].as_str().is_some_and(|h| h.len() == 64 && h.bytes().all(|b| b.is_ascii_hexdigit()))
                && file["bytes"].as_u64().is_some();
            if !well_formed {
                return bad("a file descriptor lacks a copy path, a sha256 digest or a byte count as a number");
            }
        }
        lines.push((line, member));
    }
    let done: HashSet<&str> = lines
        .iter()
        .filter(|(l, _)| l["event"] == "completed")
        .filter_map(|(l, _)| l["importId"].as_str())
        .collect();
    let mut out: HashMap<String, Vec<(u64, String)>> = HashMap::new();
    for (line, member) in &lines {
        // A started event without its completed one still names copies that
        // may exist; its census is evidence, checked against the bytes.
        if *member == "census" && done.contains(line["importId"].as_str().unwrap_or("")) {
            continue;
        }
        for file in line[*member].as_array().into_iter().flatten() {
            out.entry(file["copy"].as_str().unwrap_or("").to_owned())
                .or_default()
                .push((file["bytes"].as_u64().unwrap_or(0), file["sha256"].as_str().unwrap_or("").to_owned()));
        }
    }
    Ok(out)
}
/// The origin of each line of one log, from its place and the import accounts.
fn classifier(
    store_dir: Option<&Path>,
    path: &Path,
    bytes: &[u8],
    copies: &Result<HashMap<String, Vec<(u64, String)>>, String>,
) -> impl Fn(u64, u64) -> (Origin, Option<String>) {
    let rel = store_dir.and_then(|dir| path.strip_prefix(dir).ok().map(|r| (dir, r)));
    let (package, legacy): (Result<u64, String>, Result<u64, String>) = match rel {
        None => (Ok(0), Ok(0)),
        Some((dir, rel)) => {
            let rel = rel.to_string_lossy().into_owned();
            let package = crate::records_store::package::quoted_prefix(dir, &rel, bytes);
            let legacy = copies.as_ref().map_err(Clone::clone).and_then(|copies| {
                let mut prefix = 0;
                for (count, sha) in copies.get(&rel).into_iter().flatten() {
                    let n = usize::try_from(*count).map_err(|_| "copy length unsupported")?;
                    if n > bytes.len() || sha256_hex(&bytes[..n]) != *sha {
                        return Err(format!("{rel}: legacy-imported prefix no longer matches its import record"));
                    }
                    prefix = prefix.max(*count);
                }
                Ok(prefix)
            });
            (package, legacy)
        }
    };
    let in_store = rel.is_some();
    move |start, end| {
        if !in_store {
            return (Origin::ProjectFile, None);
        }
        let package = match &package {
            Ok(p) => *p,
            Err(e) => return (Origin::Unknown, Some(format!("package-import account: {e}"))),
        };
        let legacy = match &legacy {
            Ok(p) => *p,
            Err(e) => return (Origin::Unknown, Some(e.clone())),
        };
        if end <= package {
            (Origin::PackageImport, None)
        } else if start < package {
            (Origin::Unknown, Some("the line crosses the end of a package-imported part".into()))
        } else if end <= legacy {
            (Origin::LegacyImport, None)
        } else if start < legacy {
            (Origin::Unknown, Some("the line crosses the end of a legacy-imported part".into()))
        } else {
            (Origin::Store, None)
        }
    }
}
/// R-2 as `records::read_log_parts` reads it, keeping each entry's line span.
fn read_lines(path: &Path, bytes: &[u8]) -> (Vec<(Value, u64, u64)>, Vec<String>) {
    let name = path
        .file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default();
    let parsed = crate::record_lines::parse(bytes, &name, 0, 0, 1, Default::default());
    let mut out = Vec::new();
    let mut limits = Vec::new();
    for line in parsed.lines {
        limits.extend(line.limits);
        let end = line.offset + line.len as u64 + 1;
        for entry in line.entries {
            out.push((entry, line.offset, end));
        }
    }
    limits.extend(crate::record_lines::links_removed(path, &name, &parsed.chain));
    limits.extend(parsed.partial_tail);
    (out, limits)
}

/// The record set as it is read by path: the project's records home, never a
/// fallback to another location.
fn record_set(root: &Path, record_paths: &[&str]) -> RecordSet {
    let mut limits: Vec<String> = Vec::new();
    let home = crate::records_store::home(root);
    let store_dir = match &home {
        Ok(home) if home.store_mode => home.attachment.dir.clone(),
        _ => None,
    };
    // Owning-log provenance is retained for observation order, never performance order.
    let paths = if record_paths.is_empty() {
        match crate::storage::discover(root) {
            Ok(paths) => paths,
            Err(e) => {
                limits.push(e);
                Vec::new()
            }
        }
    } else {
        // A named log where it is read now: in the project's records store
        // subtree once it holds the project's records, otherwise in place.
        match &home {
            Ok(home)=>record_paths.iter().filter_map(|rp|{
                if home.store_mode && *rp==crate::storage::LEGACY_LOG {match crate::storage::registered_legacy_log(root){Ok(path)=>Some(path),Err(e)=>{limits.push(e);None}}}
                else if home.store_mode{home.attachment.dir.as_ref().map(|dir|dir.join(crate::storage::home_rel(rp)))}
                else{Some(root.join(rp))}
            }).collect(),
            Err(e)=>{limits.push(e.clone());Vec::new()}
        }
    };
    let mut logs = Vec::new();
    for path in paths {
        if let Err(e) = crate::storage::check_path(&path) {
            limits.push(e);
            continue;
        }
        match std::fs::read(&path) {
            Ok(bytes) => logs.push(LogSource { path, bytes: Ok(bytes) }),
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
            Err(e) => {
                let reason = format!("incomplete record: {}: {e}", path.display());
                logs.push(LogSource { path, bytes: Err(reason) });
            }
        }
    }
    let imports = match &store_dir {
        Some(dir) => match std::fs::read(dir.join("imports.jsonl")) {
            Ok(bytes) => Ok(Some(bytes)),
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(None),
            Err(e) => Err(format!("the project's import record is unreadable: {e}")),
        },
        None => Ok(None),
    };
    RecordSet {
        logs,
        store_dir,
        imports,
        limits,
    }
}

#[cfg(test)]
thread_local! { pub(crate) static PAIRS: std::cell::Cell<u64> = const { std::cell::Cell::new(0) }; }
#[inline]
fn pair_counted() {
    #[cfg(test)]
    PAIRS.with(|p| p.set(p.get() + 1));
}

pub fn derive(root: &Path, record_paths: &[&str]) -> Value {
    derive_from(root, record_set(root, record_paths), &mut |reference, limits| {
        observe_file(root, reference, limits)
    })
}

/// The decision view over a record set the caller read. `package` observes a
/// package file by its project-relative reference, once.
pub(crate) fn derive_from(
    root: &Path,
    set: RecordSet,
    package: &mut dyn FnMut(&str, &mut Vec<String>) -> FileObservation,
) -> Value {
    let RecordSet {
        logs,
        store_dir,
        imports,
        mut limits,
    } = set;
    let mut record_set_complete = limits.is_empty();
    // Sources not fully read: an unreadable or nonconformant line, a torn tail,
    // a log that could not be opened, a set that could not be discovered, or a
    // record whose origin cannot be established.
    let mut unread_sources: Vec<String> = limits.clone();
    let copies = match &imports {
        Ok(Some(bytes)) => legacy_copies(bytes),
        Ok(None) => Ok(HashMap::new()),
        Err(e) => Err(e.clone()),
    };
    if store_dir.is_some() {
        if let Err(e) = &copies {
            limits.push(format!("{e}; the origin of store records is not established"));
        }
    }
    // The door: every line classified once.
    let mut admitted: Vec<door::Authorized> = Vec::new();
    let mut claims: Vec<(Value, Value, Origin, String)> = Vec::new();
    let mut not_established: Vec<(Value, Value, String)> = Vec::new();
    let mut complete_logs = HashSet::new();
    let mut read_entries = 0;
    for log in logs {
        let label = crate::storage::log_label(root, &log.path);
        let bytes = match log.bytes {
            Ok(bytes) => bytes,
            Err(e) => {
                unread_sources.push(format!("{label}: {e}"));
                limits.push(e);
                record_set_complete = false;
                continue;
            }
        };
        let (read, found_limits) = read_lines(&log.path, &bytes);
        if found_limits.is_empty() {
            complete_logs.insert(label.clone());
        } else {
            record_set_complete = false;
            unread_sources.push(format!("{label}: {}", found_limits.join("; ")));
        }
        let classify = classifier(store_dir.as_deref(), &log.path, &bytes, &copies);
        for (e, start, end) in read {
            read_entries += 1;
            let source = json!({"log":label,"seq":e["seq"]});
            let (origin, why) = classify(start, end);
            match door::classify(e, source, origin, why) {
                door::Classified::Authorized(a) => admitted.push(a),
                door::Classified::Claim { record, source, origin, reason } => claims.push((record, source, origin, reason)),
                door::Classified::NotEstablished { record, source, reason } => not_established.push((record, source, reason)),
            }
        }
        limits.extend(found_limits);
    }
    // D: a record whose origin cannot be established makes the reading
    // incomplete, exactly as an unread line does. It is not known to be
    // unauthorized: it may be the person's own later act in a log the account
    // can no longer vouch for. Damage inside the store can therefore remove a
    // decision's standing and can never create one.
    for (record, source, reason) in &not_established {
        record_set_complete = false;
        unread_sources.push(format!(
            "{} seq {}: record {} of unestablished origin ({reason})",
            source["log"].as_str().unwrap_or(""),
            source["seq"],
            record["recordId"].as_str().unwrap_or("without an identity")
        ));
    }
    let links: Vec<door::RequestLink> = claims
        .iter()
        .filter_map(|(record, source, origin, _)| door::link(record, source, *origin))
        .collect();
    let derived = derive_rows(&admitted, &links, &complete_logs, package, &mut limits);
    let mut rows = derived.rows;
    // C: claims are attached afterwards, for display only, to the row they cite.
    attach_claims(&mut rows, &admitted, &claims, &mut limits);
    let view_claims: Vec<Value> = claims
        .iter()
        .filter(|(record, _, _, _)| {
            let id = record["recordId"].as_str().unwrap_or("");
            !rows.iter().any(|r| array_has(&r["claims"], id))
        })
        .map(claim_entry)
        .collect();
    // While any act log is not fully read, every row's state begins with the
    // incompleteness and no lapse is established; the comparison of the current
    // bytes is kept as an observation.
    if !record_set_complete {
        for row in rows.iter_mut() {
            let plain = row["state"].as_str().unwrap_or("").to_owned();
            row["state"] = json!(if plain == "decided" {
                DECIDED_INCOMPLETE.to_owned()
            } else if plain == PENDING {
                PENDING_INCOMPLETE.to_owned()
            } else {
                format!("{INCOMPLETE_PREFIX}{plain}")
            });
            let mut row_limits = row["limits"].as_array().cloned().unwrap_or_default();
            row_limits.push(json!(format!("act records not fully read: {}", unread_sources.join(" | "))));
            row["limits"] = json!(row_limits);
            let unestablished = |p: &mut Value| {
                if p.is_object() {
                    p["currentBytesObservation"] = json!(format!(
                        "an observation, not a lapse state: the package file's current bytes, compared with the bound content: {}",
                        p["currentContentComparison"].as_str().unwrap_or("not compared")
                    ));
                    p["lapse"] = json!("not established while act records are incomplete");
                    p["lapseShown"] = Value::Null;
                }
            };
            unestablished(&mut row["decision"]);
            if let Some(contenders) = row["contenders"].as_array_mut() {
                for p in contenders.iter_mut() {
                    unestablished(p);
                }
            }
        }
    }
    limits.extend(derived.view_tail);
    json!({"view": "decision packages (DEL-06-02; derived, not authority)", "rows": rows, "recordCorrections": derived.record_corrections,
        "recordSetComplete": record_set_complete,
        "readScope": {"entriesRead": read_entries, "decisionRecords": derived.decision_records,
            "authorized": admitted.len(), "claims": claims.len(), "notEstablished": not_established.len(),
            "authority": "only conforming act records in this installation's records store, outside every imported part, decide a package; other records are listed as claims; a record of unestablished origin makes the reading incomplete"},
        "claims": view_claims,
        "limits": limits, "unresolvedRecords": derived.unresolved})
}

fn array_has(list: &Value, id: &str) -> bool {
    list.as_array().is_some_and(|v| v.iter().any(|c| c["recordId"] == id))
}
/// One claim as it is shown: its origin in the reader's words, its identity,
/// recorder, the actor it names, and what it chose or claimed to do.
fn claim_entry((record, source, origin, reason): &(Value, Value, Origin, String)) -> Value {
    let b = &record["body"];
    json!({
        "recordId": record["recordId"],
        "act": record["recordId"],
        "kind": record["kind"],
        "origin": origin.label(),
        "reason": reason,
        "recordedBy": record["recorder"],
        "actor": if b["decisionActor"].is_object() { json!(person_label(&b["decisionActor"])) } else { Value::Null },
        "actKind": b["actKind"],
        "alternativeChosen": b["relations"]["alternativeChosen"],
        "request": b["relations"]["requestRef"],
        "claimedToCorrect": record.get("corrects"),
        "claimedToSupersede": b["relations"]["supersededBy"],
        "claimedToObserve": b["act"]["recordId"],
        "recordSources": [source],
        "decides": false,
    })
}
/// The request a record cites, followed through what it observes or corrects.
fn cited_request<'r>(
    record: &'r Value,
    by_id: &HashMap<&str, &'r Value>,
    depth: usize,
) -> Option<&'r str> {
    if depth > 8 {
        return None;
    }
    if record["kind"] == "act_request" {
        return record["recordId"].as_str();
    }
    if let Some(r) = record["body"]["relations"]["requestRef"].as_str() {
        return Some(r);
    }
    let next = record["body"]["act"]["recordId"].as_str().or_else(|| record["corrects"].as_str())?;
    cited_request(by_id.get(next)?, by_id, depth + 1)
}
fn attach_claims(
    rows: &mut [Value],
    admitted: &[door::Authorized],
    claims: &[(Value, Value, Origin, String)],
    limits: &mut Vec<String>,
) {
    let mut by_id: HashMap<&str, &Value> = HashMap::new();
    for a in admitted {
        if let Some(id) = a.record()["recordId"].as_str() {
            by_id.entry(id).or_insert(a.record());
        }
    }
    for (record, _, _, _) in claims {
        if let Some(id) = record["recordId"].as_str() {
            by_id.entry(id).or_insert(record);
        }
    }
    for claim in claims {
        let (record, _, _, reason) = claim;
        let id = record["recordId"].as_str().unwrap_or("");
        let row = cited_request(record, &by_id, 0).and_then(|request| {
            rows.iter().position(|r| {
                ["requests", "correctedRequests"].iter().any(|k| {
                    r[*k].as_array().is_some_and(|v| v.iter().any(|x| x == request))
                })
            })
        }).or_else(|| {
            // A claim request for a package a row already shows, by file and identity.
            (record["kind"] == "act_request").then(|| {
                let ev = &record["body"]["evidence"];
                rows.iter().position(|r| {
                    r["packageFile"] == ev["ref"]
                        && r["packageIdentity"]["method"] == ev["method"]
                        && r["packageIdentity"]["value"] == ev["claimedIdentity"]
                })
            }).flatten()
        });
        if let Some(i) = row {
            if !array_has(&rows[i]["claims"], id) {
                if let Some(list) = rows[i]["claims"].as_array_mut() {
                    list.push(claim_entry(claim));
                }
                let mut row_limits = rows[i]["limits"].as_array().cloned().unwrap_or_default();
                row_limits.push(json!(format!("{id}: {reason}; listed as a claim and decides nothing")));
                rows[i]["limits"] = json!(row_limits);
            }
        } else {
            limits.push(format!("{id}: {reason}; listed as a claim and decides nothing"));
        }
    }
}

/// What the derivation over authorized records gives back.
struct Derived {
    rows: Vec<Value>,
    record_corrections: Value,
    view_tail: Vec<String>,
    decision_records: usize,
    unresolved: Vec<Value>,
}
/// Rows, standing, ordering, grouping, duplicate resolution and lapse, from
/// authorized records alone. It takes `door::Authorized`, which only the door
/// constructs, so no claim or record of unestablished origin can reach it;
/// claim requests reach it only as `door::RequestLink`, which carries the link
/// and none of the facts a decision rests on.
fn derive_rows(
    authorized: &[door::Authorized],
    links: &[door::RequestLink],
    complete_logs: &HashSet<String>,
    package: &mut dyn FnMut(&str, &mut Vec<String>) -> FileObservation,
    limits: &mut Vec<String>,
) -> Derived {
    let all_entries: Vec<Value> = authorized.iter().map(|a| a.record().clone()).collect();
    let all_claims: Vec<Value> = authorized
        .iter()
        .map(|a| json!({"record": a.record(), "source": a.source()}))
        .collect();
    // §6: an act citing a request the log does not hold is a view limit, on no row.
    let mut request_ids: HashSet<&str> = all_entries
        .iter()
        .filter(|e| e["kind"] == "act_request")
        .filter_map(|e| e["recordId"].as_str())
        .collect();
    request_ids.extend(links.iter().map(|l| l.id.as_str()));
    let mut view_limits_tail = Vec::new();
    for a in all_entries.iter().filter(|e| e["kind"] == "human_act") {
        if let Some(r) = a["body"]["relations"]["requestRef"].as_str() {
            if !request_ids.contains(r) {
                view_limits_tail.push(format!(
                    "{}: cites request {r}, which this record set does not hold",
                    a["recordId"].as_str().unwrap_or("")
                ));
            }
        }
    }
    // Select the records that bear on decision requests before any pairwise
    // reasoning: requests with alternatives, the acts citing them, their lapse
    // observations, and every record a correction relation joins to these.
    let selected = {
        let id_of = |i: usize| all_entries[i]["recordId"].as_str().unwrap_or("");
        let mut packages: HashSet<&str> = all_entries
            .iter()
            .filter(|e| e["kind"] == "act_request" && e["body"].get("alternatives").is_some())
            .filter_map(|e| e["recordId"].as_str())
            .collect();
        packages.extend(links.iter().map(|l| l.id.as_str()));
        let mut by_id: HashMap<&str, Vec<usize>> = HashMap::new();
        let mut correctors: HashMap<&str, Vec<usize>> = HashMap::new();
        let mut lapses: HashMap<&str, Vec<usize>> = HashMap::new();
        for (i, e) in all_entries.iter().enumerate() {
            by_id.entry(id_of(i)).or_default().push(i);
            if let Some(t) = e["corrects"].as_str() {
                correctors.entry(t).or_default().push(i);
            }
            if e["kind"] == "act_lapsed" {
                if let Some(a) = e["body"]["act"]["recordId"].as_str() {
                    lapses.entry(a).or_default().push(i);
                }
            }
        }
        let mut chosen = vec![false; all_entries.len()];
        let mut todo: Vec<usize> = (0..all_entries.len())
            .filter(|&i| {
                let e = &all_entries[i];
                packages.contains(id_of(i))
                    || (e["kind"] == "human_act"
                        && e["body"]["relations"]["requestRef"]
                            .as_str()
                            .is_some_and(|r| packages.contains(r)))
            })
            .collect();
        while let Some(i) = todo.pop() {
            if std::mem::replace(&mut chosen[i], true) {
                continue;
            }
            let id = id_of(i);
            let e = &all_entries[i];
            let mut next: Vec<usize> = Vec::new();
            next.extend(correctors.get(id).into_iter().flatten());
            next.extend(lapses.get(id).into_iter().flatten());
            next.extend(by_id.get(id).into_iter().flatten());
            if let Some(t) = e["corrects"].as_str() {
                next.extend(by_id.get(t).into_iter().flatten());
            }
            if let Some(t) = e["body"]["relations"]["supersededBy"].as_str() {
                next.extend(by_id.get(t).into_iter().flatten());
            }
            todo.extend(next.into_iter().filter(|&j| !chosen[j]));
        }
        chosen
    };
    let mut entries = Vec::new();
    let mut source_claims = Vec::new();
    for (i, e) in all_entries.into_iter().enumerate() {
        if selected[i] {
            entries.push(e);
            source_claims.push(all_claims[i].clone());
        }
    }
    let mut sources: HashMap<String, Vec<Value>> = HashMap::new();
    for claim in &source_claims {
        if let Some(id) = claim["record"]["recordId"].as_str() {
            sources
                .entry(id.to_owned())
                .or_default()
                .push(claim["source"].clone());
        }
    }
    let record_corrections = record_relations::project_from_read_claims(&source_claims, &complete_logs);
    let mut grouped: HashMap<String, Vec<&Value>> = HashMap::new();
    for e in &entries {
        if let Some(id) = e["recordId"].as_str() {
            grouped.entry(id.to_owned()).or_default().push(e);
        }
    }
    let duplicates: HashSet<String> = grouped
        .iter()
        .filter(|(_, v)| v.iter().any(|e| *e != v[0]))
        .map(|(id, _)| id.clone())
        .collect();
    for (id, values) in &grouped {
        if values.len() > 1 && !duplicates.contains(id) {
            limits.push(format!(
                "identical copies of record {id}; one unchanged claim, all sources retained"
            ));
        }
    }
    for id in &duplicates {
        limits.push(format!("ambiguous duplicate record identity: {id}"));
    }
    let by_id: HashMap<String, &Value> = entries
        .iter()
        .filter_map(|e| {
            let id = e["recordId"].as_str()?;
            (!duplicates.contains(id)).then_some((id.to_owned(), e))
        })
        .collect();
    let mut invalid_corrections = HashSet::new();
    let mut correction_links: HashMap<String, String> = HashMap::new();
    for e in &entries {
        let Some(target) = e["corrects"].as_str() else {
            continue;
        };
        let id = e["recordId"].as_str().unwrap_or("");
        let reason = e["correctionReason"]
            .as_str()
            .is_some_and(|v| !v.is_empty());
        let target_entry = by_id.get(target);
        let same_kind = target_entry.is_some_and(|t| t["kind"] == e["kind"]);
        let contradicted_log_order =
            sources
                .get(id)
                .zip(sources.get(target))
                .is_some_and(|(a, b)| {
                    a.len() == 1
                        && b.len() == 1
                        && a[0]["log"] == b[0]["log"]
                        && a[0]["seq"].as_u64() <= b[0]["seq"].as_u64()
                });
        if duplicates.contains(id)
            || !reason
            || !same_kind
            || id == target
            || contradicted_log_order
        {
            invalid_corrections.insert(id.to_owned());
            limits.push(format!("{id}: correction target {target} unresolvable/ambiguous, wrong kind, missing reason or contradictory relation; not applied"));
        } else {
            correction_links.insert(id.to_owned(), target.to_owned());
        }
    }
    // Explicit links must not form a cycle, including cycles spanning independent logs.
    for id in correction_links.keys() {
        let mut seen = HashSet::new();
        let mut at = id.as_str();
        while let Some(target) = correction_links.get(at) {
            if !seen.insert(at.to_owned()) {
                invalid_corrections.extend(seen);
                limits.push(format!("{id}: cyclic correction relation; not applied"));
                break;
            }
            at = target;
        }
    }
    let mut edges: HashMap<String, Vec<String>> = HashMap::new();
    let mut corrected: HashMap<String, Vec<String>> = HashMap::new();
    for (id, target) in &correction_links {
        if !invalid_corrections.contains(id) && !invalid_corrections.contains(target) {
            edges.entry(target.clone()).or_default().push(id.clone());
            corrected
                .entry(target.clone())
                .or_default()
                .push(id.clone());
        }
    }
    // Same-stream corrections of a common target may order recorded corrections.
    // This rule never orders separate human performances or uses a wall clock.
    for (a, target_a) in &correction_links {
        for (b, target_b) in &correction_links {
            pair_counted();
            if a == b
                || target_a != target_b
                || invalid_corrections.contains(a)
                || invalid_corrections.contains(b)
            {
                continue;
            }
            if let Some((sa, sb)) = sources.get(a).zip(sources.get(b)) {
                if sa.len() == 1
                    && sb.len() == 1
                    && sa[0]["log"] == sb[0]["log"]
                    && complete_logs.contains(sa[0]["log"].as_str().unwrap_or(""))
                    && sa[0]["seq"].as_u64() < sb[0]["seq"].as_u64()
                {
                    edges.entry(a.clone()).or_default().push(b.clone());
                }
            }
        }
    }
    // P0's admitted native writer queue preserves original capture observation order,
    // including late writes before fresh continuation. Consume that bounded reported
    // stream contract, not mere seq or clock comparison, and never verify native origin.
    // Only records whose origin may decide are ordered by it.
    let mut admission_order = Vec::new();
    let native: Vec<&Value> = entries
        .iter()
        .filter(|e| {
            let id = e["recordId"].as_str().unwrap_or("");
            reported_native_observation(e)
                && e.get("corrects").is_none()
                && !duplicates.contains(id)
        })
        .collect();
    for a in &native {
        for b in &native {
            pair_counted();
            let aid = a["recordId"].as_str().unwrap_or("");
            let bid = b["recordId"].as_str().unwrap_or("");
            if aid == bid
                || same_capture(a, b)
                || a["body"]["relations"]["requestRef"] != b["body"]["relations"]["requestRef"]
            {
                continue;
            }
            if let Some((sa, sb)) = sources.get(aid).zip(sources.get(bid)) {
                if sa.len() == 1
                    && sb.len() == 1
                    && sa[0]["log"] == sb[0]["log"]
                    && complete_logs.contains(sa[0]["log"].as_str().unwrap_or(""))
                    && sa[0]["seq"].as_u64() < sb[0]["seq"].as_u64()
                {
                    edges
                        .entry(aid.to_owned())
                        .or_default()
                        .push(bid.to_owned());
                    admission_order.push(json!({"before":aid,"after":bid,"source":"reported ordered native capture admission stream (P0); not native-origin verification"}));
                }
            }
        }
    }
    // A separately stated supersession link is evidence of a recorded relation,
    // not native verification. A repeated capture is never a later performance.
    for e in &entries {
        let Some(target) = e["body"]["relations"]["supersededBy"].as_str() else {
            continue;
        };
        let id = e["recordId"].as_str().unwrap_or("");
        if let Some(t) = by_id.get(target) {
            if !duplicates.contains(id)
                && id != target
                && e["kind"] == "human_act"
                && t["kind"] == e["kind"]
                && e["body"]["actKind"] == t["body"]["actKind"]
                && e["body"]["relations"]["requestRef"] == t["body"]["relations"]["requestRef"]
                && !same_capture(e, t)
            {
                edges
                    .entry(id.to_owned())
                    .or_default()
                    .push(target.to_owned());
                continue;
            }
        }
        limits.push(format!("{id}: supersession target {target} unresolvable/ambiguous or not a distinct compatible capture; not applied"));
    }
    // Contradictory precedence cannot erase either contender.
    let cyclic: HashSet<String> = edges
        .keys()
        .filter(|id| {
            edges
                .get(*id)
                .is_some_and(|next| next.iter().any(|n| reaches(n, id, &edges)))
        })
        .cloned()
        .collect();
    for id in &cyclic {
        limits.push(format!(
            "{id}: cyclic precedence; current relation unresolved"
        ));
    }
    edges.retain(|id, _| !cyclic.contains(id));
    for next in edges.values_mut() {
        next.retain(|id| !cyclic.contains(id));
    }
    let unresolved_observations: HashSet<String> = duplicates
        .iter()
        .chain(invalid_corrections.iter())
        .chain(cyclic.iter())
        .cloned()
        .collect();
    // DEL-06-02 Several decisions: a correction stands in place of the entry it
    // corrects, before any request or act is judged; both stay listed.
    let corrected_away = |id: &str| corrected.contains_key(id);
    // A lapse observation a correction stands in place of is no lapse history.
    let mut not_history: HashSet<String> = unresolved_observations.clone();
    for e in entries.iter().filter(|e| e["kind"] == "act_lapsed") {
        let id = e["recordId"].as_str().unwrap_or("");
        if corrected_away(id) {
            not_history.insert(id.to_owned());
        }
    }
    // DV-1: a row per package. Requests are reconciled by the package they cite
    // (file path and content identity) before anything is decided.
    let mut seen_packages = HashSet::new();
    let requests: Vec<&Value> = entries
        .iter()
        .filter(|e| e["kind"] == "act_request" && e["body"].get("alternatives").is_some())
        .filter(|e| {
            duplicates.contains(e["recordId"].as_str().unwrap_or(""))
                || seen_packages.insert(e["recordId"].as_str().unwrap_or("").to_owned())
        })
        .collect();
    let package_key = |r: &Value| {
        let ev = &r["body"]["evidence"];
        (
            ev["ref"].as_str().unwrap_or("").to_owned(),
            ev["method"].as_str().unwrap_or("").to_owned(),
            ev["claimedIdentity"].as_str().unwrap_or("").to_owned(),
        )
    };
    // An authorized request is the request; a claim request sharing its record
    // identity is only a claim. A claim request may otherwise link a row.
    type Group<'g> = ((String, String, String), Vec<&'g Value>, Vec<String>, Vec<&'g door::RequestLink>);
    let mut groups: Vec<Group> = Vec::new();
    for r in requests.iter().copied().filter(|r| !corrected_away(r["recordId"].as_str().unwrap_or(""))) {
        let key = package_key(r);
        match groups.iter_mut().find(|g| g.0 == key) {
            Some(group) => group.1.push(r),
            None => groups.push((key, vec![r], Vec::new(), Vec::new())),
        }
    }
    let authorized_requests: HashSet<&str> = requests.iter().filter_map(|r| r["recordId"].as_str()).collect();
    let mut linked = HashSet::new();
    for l in links.iter().filter(|l| !authorized_requests.contains(l.id.as_str())) {
        if !linked.insert(l.id.as_str()) {
            continue;
        }
        let key = (l.file.clone(), l.method.clone(), l.value.clone());
        match groups.iter_mut().find(|g| g.0 == key) {
            Some(group) => group.3.push(l),
            None => groups.push((key, Vec::new(), Vec::new(), vec![l])),
        }
    }
    for r in requests.iter().copied().filter(|r| corrected_away(r["recordId"].as_str().unwrap_or(""))) {
        let id = r["recordId"].as_str().unwrap_or("");
        let mut heads = vec![id.to_owned()];
        let mut seen = HashSet::new();
        let mut standing = Vec::new();
        while let Some(at) = heads.pop() {
            if !seen.insert(at.clone()) {
                continue;
            }
            match corrected.get(&at) {
                Some(next) => heads.extend(next.iter().cloned()),
                None => standing.push(at),
            }
        }
        let mut placed = false;
        for group in groups.iter_mut() {
            if group.1.iter().any(|g| standing.iter().any(|s| g["recordId"] == json!(s))) {
                group.2.push(id.to_owned());
                placed = true;
            }
        }
        if !placed {
            limits.push(format!("{id}: request corrected by {}; no standing request with alternatives stands in its place", standing.join(", ")));
        }
    }
    let acts: Vec<&Value> = entries
        .iter()
        .filter(|e| e["kind"] == "human_act")
        .collect();
    let mut rows = Vec::new();
    for (_, group, corrected_requests, group_links) in &groups {
        // The facts a row shows come from its authorized request; a row resting
        // only on a claim request shows that request's facts, marked as its claim.
        let rests_on_claim = group.is_empty();
        let b: &Value = match group.first() {
            Some(p) => &p["body"],
            None => &group_links[0].shown,
        };
        let pid: &str = match group.first() {
            Some(p) => p["recordId"].as_str().unwrap_or(""),
            None => group_links[0].id.as_str(),
        };
        let mut request_ids: Vec<&str> = group.iter().filter_map(|r| r["recordId"].as_str()).collect();
        request_ids.extend(group_links.iter().map(|l| l.id.as_str()));
        let alts = b["alternatives"].as_array().cloned().unwrap_or_default();
        let cons = b["consequences"].as_array().cloned().unwrap_or_default();
        let alt_ids: Vec<&str> = alts.iter().filter_map(|a| a["id"].as_str()).collect();
        let mut row_limits: Vec<String> = Vec::new();
        // Only authorized requests can conflict; claim requests never do.
        let conflicting_requests = group.iter().any(|r| {
            ["actKind", "alternatives", "consequences", "subject", "purpose", "scope"]
                .iter()
                .any(|k| r["body"][*k] != b[*k])
        });
        if group.len() > 1 {
            row_limits.push(format!(
                "requests {} cite the same package file and content; they are read as one package",
                request_ids.join(", ")
            ));
        }
        if conflicting_requests {
            row_limits.push("requests for this one package disagree on its act, alternatives, consequences, subject, purpose or scope; no decision rests on them".into());
        }
        // DV-2
        if alt_ids.iter().collect::<HashSet<_>>().len() != alt_ids.len() {
            row_limits.push("alternative identities repeat within the package".into());
        }
        let mut orphans: Vec<&str> = cons
            .iter()
            .filter_map(|c| c["alternative"].as_str())
            .filter(|a| !alt_ids.contains(a))
            .collect();
        orphans.sort();
        orphans.dedup();
        if !orphans.is_empty() {
            row_limits.push(format!(
                "consequences name no alternative of the package: {orphans:?}"
            ));
        }
        let missing: Vec<&str> = alt_ids
            .iter()
            .copied()
            .filter(|a| !cons.iter().any(|c| c["alternative"] == json!(a)))
            .collect();
        if !missing.is_empty() {
            row_limits.push(format!("no consequence stated for: {missing:?}"));
        }
        // DV-3: the package file is observed once for this row.
        let file_ref = b["evidence"]["ref"].as_str().unwrap_or("");
        let now = package(file_ref, &mut row_limits);
        let requested = ContentIdentity {
            method: b["evidence"]["method"].as_str().unwrap_or("").into(),
            value: b["evidence"]["claimedIdentity"]
                .as_str()
                .unwrap_or("")
                .into(),
        };
        let request_state = compare(
            &requested,
            now.identity
                .as_ref()
                .map(CurrentContent::Present)
                .unwrap_or(CurrentContent::Unavailable),
            false,
        );
        match request_state {
            Lapse::Unavailable => row_limits.push("package file not available: its current content is unknown".into()),
            Lapse::Incomparable => row_limits.push("package request identity method is incomparable with current observed method; historical identities are not relabelled".into()),
            Lapse::Lapsed => row_limits.push("package file differs from the content the request recorded".into()),
            _ => {},
        }
        // The facts a decision rests on come from the package file's own current
        // bytes, where they are the content its request claims; otherwise from
        // an authorized request; never from a claim request.
        let file_facts: Option<Value> = now
            .bytes
            .as_ref()
            .filter(|_| now.identity.as_ref() == Some(&requested))
            .and_then(|bytes| serde_json::from_slice::<Value>(bytes).ok());
        let deciding_facts: Option<&Value> = file_facts.as_ref().or(group.first().map(|p| &p["body"]));
        let deciding_alternatives: Option<Vec<&str>> = deciding_facts.map(|f| {
            f["alternatives"].as_array().map(|v| v.iter().filter_map(|a| a["id"].as_str()).collect()).unwrap_or_default()
        });
        // DV-4, DV-5
        let mut decided: Vec<&Value> = Vec::new();
        let mut seen_acts = HashSet::new();
        let mut binding_unresolved = false;
        for a in acts.iter().copied().filter(|a| {
            let r = &a["body"]["relations"]["requestRef"];
            request_ids.iter().any(|id| r == id) || corrected_requests.iter().any(|id| r == id)
        }) {
            let ab = &a["body"];
            let rid = a["recordId"].as_str().unwrap_or("");
            if let Some(facts) = deciding_facts {
                if ab["actKind"] != facts["actKind"] {
                    row_limits.push(format!("{rid}: an act of kind {} cites this package; it is not the {} the package requests",
                        ab["actKind"].as_str().unwrap_or("?"), facts["actKind"].as_str().unwrap_or("?")));
                    continue;
                }
            }
            let chosen = ab["relations"]["alternativeChosen"].as_str();
            if let Some(named) = &deciding_alternatives {
                if ab["actKind"] == "A16" && !chosen.map(|c| named.contains(&c)).unwrap_or(false) {
                    row_limits.push(format!("{rid}: act not counted: chosen alternative {chosen:?} is not one the package names"));
                    continue;
                }
            }
            let cited = ab["relations"]["requestRef"].as_str().unwrap_or("");
            if corrected_requests.iter().any(|id| id == cited) {
                row_limits.push(format!("{rid}: cites request {cited}, which a correction stands in place of; it decides nothing"));
                continue;
            }
            // An act decides a request only where its bound content is the
            // package identity that request claims, by method and value.
            if !corrected_away(rid) {
                // The link: the cited request's claimed package identity, whatever
                // the request's origin.
                let cited_link = group_links.iter().find(|l| l.id == cited)
                    .map(|l| json!({"method":l.method,"claimedIdentity":l.value}));
                let cited_request = group.iter().find(|r| r["recordId"] == cited).map(|r| r["body"]["evidence"].clone());
                let claimed_value = cited_request.or(cited_link);
                let claimed = claimed_value.as_ref();
                let bound_content = ab["boundContent"].as_array();
                let comparable = |m: &Value, v: &Value| m.as_str().is_some_and(|x| !x.is_empty()) && v.as_str().is_some_and(|x| !x.is_empty());
                let matches = claimed.zip(bound_content).is_some_and(|(c, bc)| {
                    bc.len() == 1
                        && comparable(&bc[0]["method"], &bc[0]["value"])
                        && comparable(&c["method"], &c["claimedIdentity"])
                        && bc[0]["method"] == c["method"]
                        && bc[0]["value"] == c["claimedIdentity"]
                });
                if !matches {
                    binding_unresolved = true;
                    row_limits.push(format!(
                        "{rid}: bound content {} is not, or cannot be compared with, request {cited}'s package identity {}; the row is unresolved",
                        serde_json::to_string(&ab["boundContent"]).unwrap_or_default(),
                        claimed.map(|c| json!({"method":c["method"],"value":c["claimedIdentity"]}).to_string()).unwrap_or_else(|| "not found".into())
                    ));
                }
            }
            if duplicates.contains(rid) || seen_acts.insert(rid.to_owned()) {
                decided.push(a);
            }
        }
        let mut row = json!({
            "package": pid,
            "requests": request_ids,
            "correctedRequests": corrected_requests,
            "packageFile": file_ref,
            "packageIdentity": {"method": requested.method, "value": requested.value},
            "actRequested": b["actKind"],
            "subject": b["subject"],
            "purpose": b["purpose"],
            "scope": b.get("scope"),
            "requestedBy": b["requester"].get("identity").cloned().unwrap_or(json!("requester identity not established")),
            "alternatives": alts.iter().map(|a| json!({
                "id": a["id"], "statement": a["statement"],
                "consequences": cons.iter().filter(|c| c["alternative"] == a["id"]).map(|c| c["statement"].clone()).collect::<Vec<_>>()
            })).collect::<Vec<_>>(),
            "state": PENDING,
            "decision": Value::Null,
            "requestResolution": if request_ids.iter().any(|id| duplicates.contains(*id)) { "conflicting identity" } else if request_ids.iter().any(|id| sources.get(*id).is_some_and(|v|v.len()>1)) { "unique claim (identical copies)" } else { "unique claim" },
            "requestSources": sources.get(pid),
            "links": group_links.iter().map(|l| json!({"request":l.id,"origin":l.origin.label(),"source":l.source})).collect::<Vec<_>>(),
            "restsOnClaimRequest": rests_on_claim,
            "factsFrom": if rests_on_claim {
                json!({"request": pid, "origin": group_links[0].origin.label(), "standing": "these facts are that request's claim; an imported request can link, and can fail to link, and supplies none of the facts a decision rests on"})
            } else { json!({"request": pid, "origin": Origin::Store.label()}) },
            "claims": [],
            "limits": [],
        });
        // Retain a projection for each readable claim, including unresolved corrections.
        let mut projections = Vec::new();
        for a in &decided {
            let claim_limit_start = row_limits.len();
            let ab = &a["body"];
            let chosen = ab["relations"]["alternativeChosen"].as_str().unwrap_or("");
            let bound = identity(&ab["boundContent"][0]);
            let arid = a["recordId"].as_str().unwrap_or("");
            let expected_subject = format!(
                "decision package {}",
                ab["relations"]["requestRef"].as_str().unwrap_or(pid)
            );
            let scope_facts: &Value = deciding_facts.unwrap_or(&Value::Null);
            let expected_scope = scope_facts["scope"]
                .as_str()
                .filter(|s| !s.is_empty())
                .unwrap_or("not named by the package");
            let same_subject_scope = ab["actKind"] == "A16"
                && ab["boundSubject"]
                    .as_array()
                    .is_some_and(|v| v.len() == 1 && v[0] == expected_subject)
                && ab["boundContent"].as_array().is_some_and(|v| v.len() == 1)
                && (deciding_facts.is_none()
                    || (ab["scope"] == expected_scope && ab["purpose"] == scope_facts["purpose"]));
            let history_records: Vec<&str> = decided
                .iter()
                .filter(|other| same_capture(a, other) && same_capture_facts(a, other))
                .filter_map(|other| other["recordId"].as_str())
                .collect();
            let history: Vec<&Value> = history_records
                .iter()
                .flat_map(|id| {
                    lapse_history(
                        &entries,
                        id,
                        &expected_subject,
                        &bound,
                        &not_history,
                    )
                })
                .collect();
            let mut history_refs = history
                .iter()
                .map(|e| e["recordId"].clone())
                .collect::<Vec<_>>();
            history_refs.sort_by(|a, b| a.as_str().cmp(&b.as_str()));
            history_refs.dedup(); // identity display only
            let observation_claims: Vec<Value> = source_claims
                .iter()
                .filter(|c| {
                    c["record"]["kind"] == "act_lapsed"
                        && history_records
                            .iter()
                            .any(|id| c["record"]["body"]["act"]["recordId"] == *id)
                })
                .map(|c| {
                    let mut claim = c.clone();
                    claim["resolution"] = json!(if unresolved_observations
                        .contains(c["record"]["recordId"].as_str().unwrap_or(""))
                    {
                        "unknown/unresolvable observation identity or relation"
                    } else {
                        "unique recorded observation claim"
                    });
                    claim
                })
                .collect();
            let history_incomplete = observation_claims.iter().any(|c| {
                unresolved_observations.contains(c["record"]["recordId"].as_str().unwrap_or(""))
            });
            // A separate resolved witness establishes existential prior lapse even
            // when another observation is unresolved; it does not complete history.
            let history_unknown = history_incomplete && history.is_empty();
            if history_unknown {
                row_limits.push(format!("{arid}: past lapse history unknown; observation identity/relation is unresolved, current content is reported separately"));
            } else if history_incomplete {
                row_limits.push(format!("{arid}: prior lapse has an independent resolved recorded witness; total history remains incomplete with unresolved observations"));
            }
            for e in entries.iter().filter(|e| {
                e["kind"] == "act_lapsed"
                    && e["body"]["act"]["recordId"] == arid
                    && matches!(
                        e["body"]["state"].as_str(),
                        Some("lapsed" | "lapsed (subject absent)" | "partially lapsed")
                    )
            }) {
                if !history.iter().any(|accepted| std::ptr::eq(*accepted, e)) {
                    row_limits.push(format!("{}: recorded lapse observation does not establish a comparable change on this bound referent; not used as lapse history", e["recordId"].as_str().unwrap_or("?")));
                }
            }
            let state = if !same_subject_scope {
                row_limits.push("recorded act subject/scope/purpose does not match this package request; standing incomparable".into());
                Lapse::Incomparable
            } else {
                let current = if let Some(c) = now.identity.as_ref() {
                    CurrentContent::Present(c)
                } else if now.absent {
                    CurrentContent::Absent
                } else {
                    CurrentContent::Unavailable
                };
                compare(&bound, current, !history.is_empty())
            };
            if state == Lapse::Incomparable {
                row_limits.push("recorded act and current file identity are incomparable; no lapse or current human-act standing established".into());
            }
            if !history.is_empty() {
                row_limits.push(
                    "lapse history is a recorded observation claim; native origin not verified"
                        .into(),
                );
            }
            let current_content = now
                .identity
                .as_ref()
                .map(CurrentContent::Present)
                .unwrap_or(if now.absent {
                    CurrentContent::Absent
                } else {
                    CurrentContent::Unavailable
                });
            let current_relation = if !same_subject_scope {
                "incomparable subject/scope"
            } else {
                match compare(&bound, current_content, false) {
                    Lapse::NotLapsed => "matches bound content",
                    Lapse::Lapsed => "differs from bound content",
                    Lapse::SubjectAbsent => "subject absent",
                    Lapse::Incomparable => "incomparable content method",
                    _ => "current content unavailable",
                }
            };
            let lapse = if history_unknown {
                "unknown (lapse history unresolved)"
            } else {
                label(state)
            };
            // A standing observation of the past whose state is unknown: the row
            // says both without choosing between them.
            let unknown_past = state == Lapse::NotLapsed
                && entries.iter().any(|e| {
                    e["kind"] == "act_lapsed"
                        && history_records.iter().any(|id| e["body"]["act"]["recordId"] == *id)
                        && e["body"]["state"].as_str().is_some_and(|s| s.starts_with("unknown"))
                        && !not_history.contains(e["recordId"].as_str().unwrap_or(""))
                });
            let projection = json!({
                "act": arid,
                "actKind": ab["actKind"],
                "request": ab["relations"]["requestRef"],
                "alternativeChosen": chosen,
                "statement": alts.iter().find(|x| x["id"] == json!(chosen)).map(|x| x["statement"].clone()),
                // DV-8
                "decidedBy": person_label(&ab["decisionActor"]),
                "recordedBy": format!("{} {}", a["recorder"]["role"].as_str().unwrap_or(""), a["recorder"]["identity"].as_str().unwrap_or("")),
                "actRecord": {"decisionActor": ab["decisionActor"], "recorder": a["recorder"], "boundSubject": ab["boundSubject"],
                    "boundContent": ab["boundContent"], "scope": ab["scope"], "purpose": ab["purpose"]},
                "origin": Origin::Store.label(),
                "recordingMode": ab["recordingMode"],
                "captureProvenance": "recorded claim; native capture origin not verified by this unsealed reader",
                "captureEvidence": ab["captureEvidence"].as_array().map(|c| c.iter().map(|x| x["ref"].clone()).collect::<Vec<_>>()),
                "capturedAt": ab["captureTime"],
                "lapse": lapse,
                "lapseShown": if unknown_past {
                    json!("the current content is what was decided; whether it lapsed in between is not known")
                } else { Value::Null },
                "standingComparison": {"bound": ab["boundContent"][0], "current": now.identity.as_ref().map(|c| json!({"method":c.method,"value":c.value})), "recordedSubjectScopeMatchesRequest": same_subject_scope},
                "lapseHistory": history_refs,
                "lapseHistoryProvenance": "recorded observations; native origin not verified",
                "historyResolution": if history_unknown {"unknown/unresolvable past observation"} else if history_incomplete {"established prior lapse; history incomplete"} else {"resolved recorded history"},
                "historyIncomplete": history_incomplete,
                "lapseObservationClaims": observation_claims,
                "historyRecordRefs": history_records,
                "currentContentComparison": current_relation,
                "recordSources": sources.get(arid),
                "recordedAt": a["writtenAt"],
                "observedAt": a.get("observedAt"),
                "orderingMeaning": "recorded observations; entry order alone does not establish human performance chronology",
                "correctionTarget": a.get("corrects"),
                "correctedBy": corrected.get(arid),
                "relationUnresolved": duplicates.contains(arid) || invalid_corrections.contains(arid) || cyclic.contains(arid),
                "claimLimits": &row_limits[claim_limit_start..],
            });
            projections.push(projection);
        }
        let blocked = |a: &Value| {
            let id = a["recordId"].as_str().unwrap_or("");
            duplicates.contains(id) || invalid_corrections.contains(id) || cyclic.contains(id)
        };
        let eligible: Vec<&Value> = decided
            .iter()
            .copied()
            .filter(|a| !blocked(a) && !corrected_away(a["recordId"].as_str().unwrap_or("")))
            .collect();
        let maxima: Vec<&Value> = eligible
            .iter()
            .copied()
            .filter(|a| {
                !eligible.iter().any(|b| {
                    a["recordId"] != b["recordId"]
                        && reaches(
                            a["recordId"].as_str().unwrap_or(""),
                            b["recordId"].as_str().unwrap_or(""),
                            &edges,
                        )
                })
            })
            .collect();
        let conflict = maxima.iter().enumerate().any(|(i, a)| {
            maxima
                .iter()
                .skip(i + 1)
                .any(|b| same_capture(a, b) && !same_capture_facts(a, b))
        });
        if conflict {
            row_limits.push("recorders disagree: one capture has incompatible readable claims, not later performances".into());
        }
        let unresolved = decided.iter().any(|a| {
            duplicates.contains(a["recordId"].as_str().unwrap_or(""))
                || cyclic.contains(a["recordId"].as_str().unwrap_or(""))
        }) || request_ids.iter().any(|id| duplicates.contains(*id));
        let equivalent_capture = !maxima.is_empty()
            && maxima
                .iter()
                .all(|a| same_capture(a, maxima[0]) && same_capture_facts(a, maxima[0]));
        if (unresolved && !decided.is_empty())
            || (eligible.is_empty() && decided.iter().any(|a| blocked(a)))
            || (!eligible.is_empty() && maxima.len() != 1 && !equivalent_capture)
        {
            row["state"] = json!("ambiguous current standing");
            row_limits.push("ambiguous/unresolved current recorded claims; no warranted total order or later human performance".into());
        } else if let Some(current) = maxima
            .iter()
            .find(|a| a["body"]["recordingMode"] == "direct capture")
            .or_else(|| maxima.first())
        {
            row["state"] = json!("decided");
            let id = current["recordId"].as_str().unwrap_or("");
            let mut projection = projections
                .iter()
                .find(|p| p["act"] == id)
                .cloned()
                .unwrap();
            if equivalent_capture && maxima.len() > 1 {
                let direct_count = maxima
                    .iter()
                    .filter(|a| a["body"]["recordingMode"] == "direct capture")
                    .count();
                if direct_count != 1 {
                    projection["act"] = Value::Null;
                    projection["recordedBy"] =
                        json!("multiple records of the same capture; see contenders");
                    projection["recordedAt"] = Value::Null;
                    projection["observedAt"] = Value::Null;
                    projection["recordSources"] = json!(maxima
                        .iter()
                        .flat_map(|a| sources
                            .get(a["recordId"].as_str().unwrap_or(""))
                            .into_iter()
                            .flatten()
                            .cloned())
                        .collect::<Vec<_>>());
                }
            }
            let mut equivalent_ids = maxima
                .iter()
                .map(|a| a["recordId"].clone())
                .collect::<Vec<_>>();
            equivalent_ids.sort_by(|a, b| a.as_str().cmp(&b.as_str())); // display only; never precedence
            projection["orderingEvidence"] = json!(admission_order
                .iter()
                .filter(|w| maxima.iter().any(|a| a["recordId"] == w["after"]))
                .collect::<Vec<_>>());
            projection["equivalentCaptureRecords"] = json!(equivalent_ids);
            if equivalent_capture && maxima.len() > 1 {
                let mut histories = projections
                    .iter()
                    .filter(|p| maxima.iter().any(|a| a["recordId"] == p["act"]))
                    .flat_map(|p| p["lapseHistory"].as_array().unwrap().iter().cloned())
                    .collect::<Vec<_>>();
                histories.sort_by(|a, b| a.as_str().cmp(&b.as_str()));
                histories.dedup();
                projection["lapseHistory"] = json!(histories);
                let past_incomplete = projections.iter().any(|p| {
                    maxima.iter().any(|a| a["recordId"] == p["act"])
                        && p["historyIncomplete"] == true
                });
                let past_unknown =
                    past_incomplete && projection["lapseHistory"].as_array().unwrap().is_empty();
                projection["historyIncomplete"] = json!(past_incomplete);
                projection["lapseObservationClaims"] = json!(projections
                    .iter()
                    .filter(|p| maxima.iter().any(|a| a["recordId"] == p["act"]))
                    .flat_map(|p| p["lapseObservationClaims"]
                        .as_array()
                        .unwrap()
                        .iter()
                        .cloned())
                    .collect::<Vec<_>>());
                if past_unknown {
                    projection["historyResolution"] =
                        json!("unknown/unresolvable past observation");
                    projection["lapse"] = json!("unknown (lapse history unresolved)");
                } else if past_incomplete {
                    projection["historyResolution"] =
                        json!("established prior lapse; history incomplete");
                }
                // The facts agree; one capture's history may be linked through either record.
                let bound = identity(&current["body"]["boundContent"][0]);
                let current_content = now
                    .identity
                    .as_ref()
                    .map(CurrentContent::Present)
                    .unwrap_or(if now.absent {
                        CurrentContent::Absent
                    } else {
                        CurrentContent::Unavailable
                    });
                if !past_unknown
                    && projection["standingComparison"]["recordedSubjectScopeMatchesRequest"]
                        == true
                {
                    projection["lapse"] = json!(label(compare(
                        &bound,
                        current_content,
                        !projection["lapseHistory"].as_array().unwrap().is_empty()
                    )));
                }
            }
            projection["earlierActs"] = json!(decided.iter().filter(|a| a["recordId"]!=current["recordId"]).map(|a| {
                let aid=a["recordId"].as_str().unwrap_or("");
                let relation=if corrected.get(aid).is_some_and(|v|v.iter().any(|cid| reaches(cid,id,&edges) || cid==id)) { format!("corrected by {id}") }
                    else if corrected.contains_key(aid) { format!("corrected by {}", corrected[aid].join(", ")) }
                    else if reaches(aid,id,&edges) { if admission_order.iter().any(|w|w["before"]==aid && w["after"]==id) {format!("superseded by {id} (reported ordered native admission stream; origin unverified)")} else {format!("superseded by {id} (explicit recorded relation)")} }
                    else if same_capture(a,current) && same_capture_facts(a,current) { "same capture recorded again; not a later performance".into() }
                    else { "unresolved relation; claim retained".into() };
                json!({"act":aid,"relation":relation,"alternativeChosen":a["body"]["relations"]["alternativeChosen"]})
            }).collect::<Vec<_>>());
            row["decision"] = projection;
        }
        // E: a decision rests on the act and the package file's own current
        // bytes. The act's bound content must equal the cited request's claimed
        // package identity (checked above, as the link) and the file's current
        // bytes, and the file's own bytes must name the act's kind and the
        // alternative chosen. A request record supplies none of these facts.
        if row["state"] == "decided" {
            let current = maxima
                .iter()
                .find(|a| a["body"]["recordingMode"] == "direct capture")
                .or_else(|| maxima.first())
                .copied();
            if let Some(current) = current {
                let bound = identity(&current["body"]["boundContent"][0]);
                let chosen = current["body"]["relations"]["alternativeChosen"].as_str();
                let verdict: Result<(), (&str, String)> = match now.identity.as_ref() {
                    None if now.absent => Err((LAPSED, "the package file is absent".into())),
                    None => Err((PACKAGE_UNRESOLVED, "the package file's current bytes could not be read".into())),
                    Some(c) if c.method != bound.method => Err((PACKAGE_UNRESOLVED, format!(
                        "the act's bound content ({}) and the package file's current bytes ({}) are not identified by one method",
                        bound.method, c.method))),
                    Some(c) if c.value != bound.value => Err((LAPSED, "the package file's current bytes are not the content decided".into())),
                    Some(_) => {
                        let facts = now.bytes.as_ref().and_then(|b| serde_json::from_slice::<Value>(b).ok());
                        let names = facts.as_ref().is_some_and(|f| {
                            f["actKind"] == current["body"]["actKind"]
                                && (current["body"]["actKind"] != "A16"
                                    || f["alternatives"].as_array().is_some_and(|v| v.iter().any(|a| a["id"].as_str() == chosen && chosen.is_some())))
                        });
                        if names { Ok(()) } else {
                            Err((PACKAGE_UNRESOLVED, "the package file's current bytes do not name the act's kind and the alternative it chose".into()))
                        }
                    }
                };
                if let Err((state, why)) = verdict {
                    row["state"] = json!(state);
                    row_limits.push(format!("{}: {why}; not decided", current["recordId"].as_str().unwrap_or("")));
                    if state == PACKAGE_UNRESOLVED {
                        row["decision"] = Value::Null;
                    }
                }
            }
        }
        if binding_unresolved {
            row["state"] = json!(BINDING_UNRESOLVED);
            row["decision"] = Value::Null;
        }
        if request_ids.iter().any(|id| duplicates.contains(*id)) || conflicting_requests {
            row["state"] = json!("unresolvable request identity");
            row["decision"] = Value::Null;
            row_limits.push("request record identity has conflicting facts; no unique package/offer binding resolved".into());
        }
        row["currentCandidates"] = json!(maxima
            .iter()
            .map(|a| a["recordId"].clone())
            .collect::<Vec<_>>());
        row["contenders"] = json!(projections);
        row["limits"] = json!(row_limits);
        rows.push(row);
    }
    let unresolved_records: Vec<Value> = entries
        .iter()
        .filter(|e| {
            let id = e["recordId"].as_str().unwrap_or("");
            duplicates.contains(id) || invalid_corrections.contains(id)
        })
        .cloned()
        .collect();
    Derived {
        rows,
        record_corrections,
        view_tail: view_limits_tail,
        decision_records: entries.len(),
        unresolved: unresolved_records,
    }
}

#[cfg(test)]
#[path = "decision_view_tests.rs"]
mod tests;
